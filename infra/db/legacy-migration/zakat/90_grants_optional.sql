-- 90_grants_optional.sql — Hak akses untuk role aplikasi isf-app (OPSIONAL, jalankan terpisah)
--
-- Konteks: di produksi legacy setiap schema dimiliki role bernama sama
-- (accounting, enterprise, fund, personalia, program, school, transaction, ...)
-- dan dump TIDAK berisi GRANT. isf-app (api-python, report-api) konek dengan SATU
-- role (default dev: `transaction`) dan membaca/menulis lintas schema
-- (program.*, fund.*, personalia.*, enterprise.*, ...).
--
-- Jalankan sebagai superuser / pemilik schema:
--   psql -d <db> -v app_role=transaction -f 90_grants_optional.sql
--
-- Tidak perlu bila restore dilakukan dengan --no-owner sebagai role aplikasi
-- (semua objek otomatis dimiliki role tsb — seperti mziss_laz_origin di dev).

\if :{?app_role}
\else
  \echo 'ERROR: set -v app_role=<role aplikasi>'
  \quit
\endif

-- variabel psql tidak diinterpolasi di dalam $$...$$ → lewatkan via GUC sesi
SELECT set_config('isf_migration.app_role', :'app_role', false);

DO $$
DECLARE
  s text;
  r text := current_setting('isf_migration.app_role');
BEGIN
  FOR s IN SELECT nspname FROM pg_namespace
           WHERE nspname IN ('accounting','dashboard','enterprise','fund','personalia',
                             'program','school','transaction','dwh','otorisasi','public')
  LOOP
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO %I', s, r);
    EXECUTE format('GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA %I TO %I', s, r);
    EXECUTE format('GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA %I TO %I', s, r);
    EXECUTE format('GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA %I TO %I', s, r);
  END LOOP;
  RAISE NOTICE 'GRANT selesai untuk role %', r;
END $$;
