#!/usr/bin/env bash
# Migrasi auth DB isf-app (isf_auth_<portal>) untuk data produksi legacy — portal ZAKAT.
#
# Pemakaian:
#   PGPASSWORD=... ./run_auth_migration.sh init       <business_db> <auth_db> [--dry-run] [--out FILE]
#   PGPASSWORD=... ./run_auth_migration.sh sync-users <business_db> <auth_db> [--dry-run] [--out FILE]
#
#   init        auth DB baru/kosong: 10 preflight → 11 schema → 12 menu/RBAC/tenant (satu transaksi),
#               lalu provisioning user dari enterprise.userapp, lalu 13 postcheck.
#   sync-users  auth DB sudah di-init: hanya provisioning user + postcheck (ulangi sebelum cut-over
#               untuk menangkap user baru legacy). Password yang sudah ada TIDAK diubah.
#   --dry-run   init: validasi SQL lalu ROLLBACK (provisioning dilewati);
#               sync-users: provisioning lalu ROLLBACK.
#   --out FILE  CSV password sementara (default: ./out/initial-passwords-<auth_db>-<ts>.csv, mode 0600)
#
# Prasyarat: auth DB sudah dibuat (createdb, owner = role aplikasi) dan business DB sudah
# dimigrasi (run_migration.sh). Provisioning butuh python + asyncpg + bcrypt; bila tidak ada
# di host, dijalankan di image bff-api (BFF_IMAGE, default localhost/isf-zakat-bff-api:dev).
#
# ⚠️ Jangan start bff-api ke auth DB ini sebelum langkah ini selesai: bila isf_auth.users
#    kosong, BFF otomatis men-seed akun demo ADMIN/admin123 (app/services/auth_seed.py).
set -euo pipefail

MODE="${1:?Usage: $0 init|sync-users <business_db> <auth_db> [--dry-run] [--out FILE]}"
BIZ_DB="${2:?business_db wajib}"
AUTH_DB="${3:?auth_db wajib}"
shift 3
DRY=""; OUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY=1; shift ;;
    --out) OUT="$2"; shift 2 ;;
    *) echo "argumen tidak dikenal: $1" >&2; exit 1 ;;
  esac
done

HERE="$(cd "$(dirname "$0")" && pwd)"
TOOLS="$(cd "$HERE/../tools" && pwd)"
export PGHOST="${PGHOST:-localhost}" PGPORT="${PGPORT:-5432}" PGUSER="${PGUSER:-transaction}"
BFF_IMAGE="${BFF_IMAGE:-localhost/isf-zakat-bff-api:dev}"
OUT="${OUT:-$PWD/out/initial-passwords-$AUTH_DB-$(date +%Y%m%d-%H%M%S).csv}"
mkdir -p "$(dirname "$OUT")"; OUT="$(cd "$(dirname "$OUT")" && pwd)/$(basename "$OUT")"

psql_auth() { psql -X -v ON_ERROR_STOP=1 -d "$AUTH_DB" "$@"; }

provision() {
  local args=(--business-dsn "postgresql://$PGUSER@$PGHOST:$PGPORT/$BIZ_DB"
              --auth-dsn "postgresql://$PGUSER@$PGHOST:$PGPORT/$AUTH_DB")
  [[ -n "$DRY" ]] && args+=(--dry-run)
  [[ -n "${EXTRA_PROVISION_ARGS:-}" ]] && read -r -a extra <<< "$EXTRA_PROVISION_ARGS" && args+=("${extra[@]}")
  if python3 -c 'import asyncpg, bcrypt' 2>/dev/null; then
    python3 "$TOOLS/provision_auth_users.py" "${args[@]}" --out "$OUT"
  else
    echo ">> python host tanpa asyncpg/bcrypt — menjalankan di image $BFF_IMAGE"
    podman run --rm --network host --security-opt label=disable \
      -e PGPASSWORD -v "$TOOLS:/tools:ro" -v "$(dirname "$OUT"):/out" \
      --entrypoint python "$BFF_IMAGE" /tools/provision_auth_users.py \
      "${args[@]}" --out "/out/$(basename "$OUT")"
  fi
}

echo ">> auth migration [$MODE${DRY:+, dry-run}] business=$BIZ_DB auth=$AUTH_DB @ $PGHOST:$PGPORT"

# Business DB harus sudah dimigrasi (otorisasi ada) — user identity dibaca dari sana.
psql -X -At -d "$BIZ_DB" -c "SELECT 1 FROM pg_namespace WHERE nspname='otorisasi'" | grep -q 1 \
  || { echo "ERROR: $BIZ_DB belum dimigrasi (jalankan run_migration.sh dulu)" >&2; exit 1; }

case "$MODE" in
  init)
    if [[ -n "$DRY" ]]; then
      psql_auth -c 'BEGIN' -f "$HERE/auth/10_preflight.sql" -f "$HERE/auth/11_schema_isf_auth.sql" \
                -f "$HERE/auth/12_reference_data.sql" -c 'ROLLBACK'
      echo ">> dry-run: SQL init valid, di-ROLLBACK (provisioning dilewati)"; exit 0
    fi
    psql_auth --single-transaction -f "$HERE/auth/10_preflight.sql" \
              -f "$HERE/auth/11_schema_isf_auth.sql" -f "$HERE/auth/12_reference_data.sql" >/dev/null
    echo ">> schema + data referensi isf_auth OK"
    provision
    ;;
  sync-users)
    provision
    [[ -n "$DRY" ]] && exit 0
    ;;
  *) echo "mode tidak dikenal: $MODE" >&2; exit 1 ;;
esac

psql_auth -f "$HERE/auth/13_postcheck.sql"
[[ -f "$OUT" ]] && echo ">> ⚠️  $OUT berisi password sementara (plaintext): bagikan lewat jalur aman lalu HAPUS file ini."
