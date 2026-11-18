#!/usr/bin/env bash
# Migrasi struktur DB legacy (backup produksi) → struktur isf-app, portal ZAKAT.
#
# Pemakaian:
#   PGPASSWORD=... ./run_migration.sh <db_target> [--dry-run]
#
#   <db_target>  DB legacy hasil restore, mis. mziss_laz_origin
#   --dry-run    jalankan semua langkah lalu ROLLBACK (tidak ada perubahan permanen)
#
# Env: PGHOST (localhost) PGPORT (5432) PGUSER (transaction)
#
# Seluruh langkah 00–05 berjalan dalam SATU transaksi (psql --single-transaction
# + ON_ERROR_STOP): gagal di langkah mana pun → tidak ada perubahan sama sekali.
set -euo pipefail

DB="${1:?Usage: $0 <db_target> [--dry-run]}"
DRY="${2:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
export PGHOST="${PGHOST:-localhost}" PGPORT="${PGPORT:-5432}" PGUSER="${PGUSER:-transaction}"

FILES=(
  00_preflight.sql
  01_legacy_tables.sql
  02_schema_otorisasi.sql
  03_schema_dwh.sql
  04_reference_data.sql
  05_postcheck.sql
)

ARGS=(-X -v ON_ERROR_STOP=1 -d "$DB" --single-transaction)
for f in "${FILES[@]}"; do ARGS+=(-f "$HERE/$f"); done

if [[ "$DRY" == "--dry-run" ]]; then
  # ROLLBACK di akhir: tambahkan file sementara yang membatalkan transaksi.
  TMP="$(mktemp)"; trap 'rm -f "$TMP"' EXIT
  echo "ROLLBACK;" > "$TMP"
  # --single-transaction tidak bisa dipakai bersama ROLLBACK eksplisit → BEGIN manual.
  ARGS=(-X -v ON_ERROR_STOP=1 -d "$DB" -c 'BEGIN')
  for f in "${FILES[@]}"; do ARGS+=(-f "$HERE/$f"); done
  ARGS+=(-f "$TMP")
  echo ">> DRY-RUN pada $DB@$PGHOST:$PGPORT (akan di-ROLLBACK)"
else
  echo ">> MIGRASI pada $DB@$PGHOST:$PGPORT"
fi

START=$(date +%s)
psql "${ARGS[@]}"
echo ">> selesai dalam $(( $(date +%s) - START )) detik${DRY:+ (dry-run, tidak ada perubahan)}"
