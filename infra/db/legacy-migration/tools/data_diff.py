#!/usr/bin/env python3
"""Bandingkan ISI tabel kecil (config/master) antara dua DB, per primary key.

Tujuan: menemukan data konfigurasi yang dibuat isf-app di DB dev (only_target /
changed) dan yang lebih baru di produksi (only_source), agar diputuskan mana yang
perlu dibawa oleh skrip migrasi.

Pemakaian:
  python3 data_diff.py --source mziss_laz_origin --target mziss_laz \
      --diff-json <out-dir>/diff.json --out <out-dir>/data-diff.json [--max-rows 20000]

  --diff-json : output compare_schema.py (dipakai daftar tabel + estimasi baris)
"""
import argparse
import json
import os

import psycopg2


def qident(t):
    s, n = t.split(".", 1)
    return f'"{s}"."{n}"'


def table_hash(cur, t):
    cur.execute(f"select count(*), md5(coalesce(string_agg(x::text,'|' order by x::text),'')) from {qident(t)} x")
    return cur.fetchone()


def columns(cur, t):
    cur.execute("select attname from pg_attribute where attrelid=%s::regclass and attnum>0 "
                "and not attisdropped order by attnum", (qident(t),))
    return [r[0] for r in cur.fetchall()]


def pk_cols(cur, t):
    cur.execute("""select array_agg(a.attname order by k.ord) from pg_constraint c
      cross join unnest(c.conkey) with ordinality k(attnum, ord)
      join pg_attribute a on a.attrelid=c.conrelid and a.attnum=k.attnum
      where c.conrelid=%s::regclass and c.contype='p'""", (qident(t),))
    return cur.fetchone()[0]


def keyed_rows(cur, t, key, common):
    k = ",".join(f'x."{c}"::text' for c in key)
    r = ",".join(f'x."{c}"' for c in common)
    cur.execute(f"select ({k}), md5(row({r})::text) from {qident(t)} x")
    return {a: b for a, b in cur.fetchall()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--diff-json", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-rows", type=int, default=20000)
    ap.add_argument("--host", default=os.environ.get("PGHOST", "localhost"))
    ap.add_argument("--port", default=os.environ.get("PGPORT", "5432"))
    ap.add_argument("--user", default=os.environ.get("PGUSER", "transaction"))
    ap.add_argument("--password", default=os.environ.get("PGPASSWORD", "solusi"))
    a = ap.parse_args()

    d = json.load(open(a.diff_json))
    cs = {db: psycopg2.connect(host=a.host, port=a.port, user=a.user, password=a.password, dbname=db)
          for db in (a.source, a.target)}
    src, tgt = cs[a.source].cursor(), cs[a.target].cursor()
    res = {}
    for t, e in d["row_estimates"].items():
        if t.startswith("migration.") or max(e["source"], e["target"]) > a.max_rows:
            continue
        if table_hash(src, t) == table_hash(tgt, t):
            continue
        common = [c for c in columns(src, t) if c in set(columns(tgt, t))]
        pk = pk_cols(tgt, t)
        key = pk or common
        o, g = keyed_rows(src, t, key, common), keyed_rows(tgt, t, key, common)
        only_t = [k for k in g if k not in o]
        only_s = [k for k in o if k not in g]
        chg = [k for k in g if k in o and o[k] != g[k]]
        res[t] = {"pk": pk, "n_only_target": len(only_t), "n_only_source": len(only_s),
                  "n_changed": len(chg), "only_target_sample": only_t[:20],
                  "changed_sample": chg[:20]}
        print(f"{t:42s} pk={'Y' if pk else 'N'} only_target={len(only_t):5d} "
              f"only_source={len(only_s):5d} changed={len(chg):5d}")
    with open(a.out, "w") as f:
        json.dump(res, f, indent=1, default=str)


if __name__ == "__main__":
    main()
