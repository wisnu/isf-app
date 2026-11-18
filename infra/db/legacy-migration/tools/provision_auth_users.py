#!/usr/bin/env python3
"""Provisikan user produksi (enterprise.userapp) ke auth DB isf-app (isf_auth_<portal>).

Login isf-app butuh user di dua tempat:
  - business DB : enterprise.userapp (+ listperanuser, listcabangdiizinkan) → roles/cabang
  - auth DB     : isf_auth.users + user_credentials + tenant_memberships   → login
Tool ini menyinkronkan sisi auth dari sisi business (sumber kebenaran = legacy).

Password legacy disimpan oleh server "Corporate" DAF dengan encoding sendiri dan
TIDAK bisa dikonversi ke bcrypt. Maka setiap user AKTIF yang belum punya kredensial
diberi password sementara acak (bcrypt, sama seperti BFF) dan dicatat ke CSV
(mode 0600) untuk dibagikan admin. User diminta mengganti password setelah login
(menu Profil → Ganti Password).

Butuh: asyncpg + bcrypt (tersedia di image bff-api) — lihat run_auth_migration.sh.

Pemakaian:
  python provision_auth_users.py --business-dsn postgresql://... --auth-dsn postgresql://... \
      --out /out/initial-passwords.csv [--tenant perusahaan_a] [--reset-passwords] \
      [--deactivate-orphans] [--dry-run]
"""
import argparse
import asyncio
import csv
import os
import secrets
import sys

import asyncpg
import bcrypt

ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789"  # tanpa 0/O/1/l/I


def temp_password(n: int = 12) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(n))


def bcrypt_hash(pw: str) -> str:
    return bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--business-dsn", required=True)
    ap.add_argument("--auth-dsn", required=True)
    ap.add_argument("--out", required=True, help="CSV password sementara (dibuat mode 0600)")
    ap.add_argument("--tenant", default="perusahaan_a",
                    help="tenant default (sama dengan DEFAULT_TENANT appadmin/user/service.py)")
    ap.add_argument("--reset-passwords", action="store_true",
                    help="buat password sementara baru untuk SEMUA user aktif (bukan hanya yang belum punya)")
    ap.add_argument("--deactivate-orphans", action="store_true",
                    help="set status=inactive untuk user auth yang tidak ada di enterprise.userapp")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    biz = await asyncpg.connect(a.business_dsn, ssl=False)
    rows = await biz.fetch("""
        SELECT UPPER(TRIM(u.id_user)) AS id,
               COALESCE(NULLIF(TRIM(u.nama_user), ''), UPPER(TRIM(u.id_user))) AS display_name,
               u.status_profil, u.kunci_akses,
               (SELECT COUNT(*) FROM enterprise.listperanuser l WHERE l.id_user = u.id_user) AS n_roles
        FROM enterprise.userapp u
        WHERE TRIM(COALESCE(u.id_user, '')) <> ''
        ORDER BY 1""")
    await biz.close()

    ids = [r["id"] for r in rows]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        print(f"ERROR: id_user bentrok setelah UPPER(): {dup}", file=sys.stderr)
        return 2
    too_long = [r["id"] for r in rows if len(r["id"]) > 20]
    if too_long:
        print(f"ERROR: id_user > 20 char (isf_auth.users.id varchar(20)): {too_long}", file=sys.stderr)
        return 2

    auth = await asyncpg.connect(a.auth_dsn, ssl=False)
    issued: list[tuple[str, str, str]] = []
    stats = {"insert": 0, "update": 0, "inactive": 0, "no_role_active": [], "locked_active": [],
             "orphans": []}
    tr = auth.transaction()
    await tr.start()
    try:
        if not await auth.fetchval("SELECT 1 FROM isf_auth.tenants WHERE id=$1", a.tenant):
            raise SystemExit(f"ERROR: tenant '{a.tenant}' tidak ada — jalankan 12_reference_data.sql dulu")

        existing = {r["id"] for r in await auth.fetch("SELECT id FROM isf_auth.users")}
        has_cred = {r["user_id"] for r in await auth.fetch("SELECT user_id FROM isf_auth.user_credentials")}

        for r in rows:
            active = r["status_profil"] == "A"  # mapping sama dengan update_user_status()
            status = "active" if active else "inactive"
            if active and r["n_roles"] == 0:
                stats["no_role_active"].append(r["id"])
            if active and r["kunci_akses"] == "T":
                stats["locked_active"].append(r["id"])
            stats["update" if r["id"] in existing else "insert"] += 1
            stats["inactive"] += 0 if active else 1

            await auth.execute("""
                INSERT INTO isf_auth.users (id, username, display_name, status)
                VALUES (CAST($1 AS varchar), CAST($1 AS varchar), $2, $3)
                ON CONFLICT (id) DO UPDATE
                  SET display_name = EXCLUDED.display_name, status = EXCLUDED.status""",
                r["id"], r["display_name"][:200], status)
            await auth.execute("""
                INSERT INTO isf_auth.tenant_memberships (user_id, tenant_id, is_default)
                SELECT CAST($1 AS varchar), CAST($2 AS varchar), NOT EXISTS (SELECT 1 FROM isf_auth.tenant_memberships
                                           WHERE user_id = CAST($1 AS varchar) AND is_default)
                ON CONFLICT (user_id, tenant_id) DO NOTHING""", r["id"], a.tenant)

            if active and (a.reset_passwords or r["id"] not in has_cred):
                pw = temp_password()
                await auth.execute("""
                    INSERT INTO isf_auth.user_credentials (user_id, password_hash)
                    VALUES ($1, $2)
                    ON CONFLICT (user_id) DO UPDATE
                      SET password_hash = EXCLUDED.password_hash, updated_at = now()""",
                    r["id"], bcrypt_hash(pw))
                issued.append((r["id"], r["display_name"], pw))

        legacy_ids = set(ids)
        stats["orphans"] = sorted(u for u in existing if u not in legacy_ids)
        if a.deactivate_orphans and stats["orphans"]:
            await auth.execute("UPDATE isf_auth.users SET status='inactive' WHERE id = ANY($1::text[])",
                               stats["orphans"])

        if a.dry_run:
            await tr.rollback()
        else:
            await tr.commit()
    except BaseException:
        await tr.rollback()
        raise
    finally:
        await auth.close()

    if issued and not a.dry_run:
        old = os.umask(0o077)
        try:
            with open(a.out, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["username", "display_name", "temporary_password"])
                w.writerows(issued)
        finally:
            os.umask(old)
        os.chmod(a.out, 0o600)

    print(f"userapp legacy        : {len(rows)} (aktif {len(rows) - stats['inactive']}, nonaktif {stats['inactive']})")
    print(f"isf_auth.users        : insert {stats['insert']}, update {stats['update']}")
    print(f"password sementara    : {len(issued)}" + ("" if a.dry_run or not issued else f" → {a.out} (0600)"))
    if stats["no_role_active"]:
        print(f"WARN aktif tanpa peran (login OK tapi menu kosong): {stats['no_role_active']}")
    if stats["locked_active"]:
        print(f"WARN aktif tapi kunci_akses='T' di legacy (tetap active di isf-app): {stats['locked_active']}")
    if stats["orphans"]:
        verb = "di-nonaktifkan" if a.deactivate_orphans else "TIDAK diubah (pakai --deactivate-orphans)"
        print(f"WARN user auth tanpa userapp ({verb}): {stats['orphans']}")
    print("DRY-RUN: semua perubahan di-ROLLBACK" if a.dry_run else "OK")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
