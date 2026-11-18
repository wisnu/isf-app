-- 00_preflight.sql — Pemeriksaan sebelum migrasi legacy → isf-app (portal ZAKAT)
-- Target  : DB legacy produksi (contoh: mziss_laz_origin, asal dump "isocial_laz", PG 12.22)
-- Sifat   : READ-ONLY. Gagal (RAISE EXCEPTION) bila prasyarat tidak terpenuhi,
--           sehingga run_migration.sh berhenti sebelum ada perubahan apa pun.
-- Kompatibel PostgreSQL 12+.

DO $$
DECLARE
  v_missing text;
BEGIN
  -- 1) Migrasi belum pernah dijalankan
  IF EXISTS (SELECT 1 FROM pg_namespace WHERE nspname IN ('otorisasi','dwh')) THEN
    RAISE EXCEPTION 'PREFLIGHT: schema otorisasi/dwh sudah ada — migrasi sudah pernah dijalankan (lihat 99_rollback.sql)';
  END IF;

  -- 2) Schema legacy wajib ada
  SELECT string_agg(s, ', ') INTO v_missing
  FROM unnest(ARRAY['accounting','enterprise','fund','personalia','program','transaction']) s
  WHERE NOT EXISTS (SELECT 1 FROM pg_namespace WHERE nspname = s);
  IF v_missing IS NOT NULL THEN
    RAISE EXCEPTION 'PREFLIGHT: schema legacy tidak ditemukan: % — apakah ini DB legacy zakat?', v_missing;
  END IF;

  -- 3) Tabel legacy yang akan di-ALTER wajib ada
  SELECT string_agg(t, ', ') INTO v_missing
  FROM unnest(ARRAY[
    'fund.individualdonor','transaction.batchupload','transaction.batchuploaditem',
    'transaction.budgetowner','transaction.humancapitalbatch','transaction.humancapitalbatchitem',
    'transaction.humancapitalpassedreport','transaction.transactiontype'
  ]) t
  WHERE to_regclass(t) IS NULL;
  IF v_missing IS NOT NULL THEN
    RAISE EXCEPTION 'PREFLIGHT: tabel legacy tidak ditemukan: %', v_missing;
  END IF;

  -- 4) Portal guard: DB zakat memakai transactioncode SD001 (penghimpunan)
  IF NOT EXISTS (SELECT 1 FROM transaction.transactiontype WHERE transactioncode = 'SD001') THEN
    RAISE EXCEPTION 'PREFLIGHT: transactiontype SD001 tidak ada — bukan DB zakat?';
  END IF;

  -- 5) Kolom yang dirujuk view dwh (harus ada di legacy)
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns
                 WHERE table_schema='transaction' AND table_name='transaction' AND column_name='batchid') THEN
    RAISE EXCEPTION 'PREFLIGHT: transaction.transaction.batchid tidak ada';
  END IF;

  RAISE NOTICE 'PREFLIGHT OK — server %, db %', current_setting('server_version'), current_database();
END $$;
