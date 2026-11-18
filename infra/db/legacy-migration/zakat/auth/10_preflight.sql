-- 10_preflight.sql — Guard sebelum membuat schema isf_auth di auth DB (isf_auth_<portal>)
-- READ-ONLY. Gagal bila auth DB sudah berisi schema isf_auth (gunakan mode sync-users
-- untuk DB yang sudah di-init). Kompatibel PostgreSQL 12+.
DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = 'isf_auth') THEN
    RAISE EXCEPTION 'PREFLIGHT(auth): schema isf_auth sudah ada di % — pakai "run_auth_migration.sh sync-users" atau 99_rollback.sql', current_database();
  END IF;
  IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname IN ('transaction','enterprise','program')) THEN
    RAISE EXCEPTION 'PREFLIGHT(auth): % berisi schema bisnis legacy — ini business DB, bukan auth DB', current_database();
  END IF;
  RAISE NOTICE 'PREFLIGHT(auth) OK — server %, db %', current_setting('server_version'), current_database();
END $$;
