-- [DWH] Rename schema datamart -> dwh di mziss_wakaf
--
-- Menyelaraskan penamaan DWH wakaf dengan zakat (mziss_laz pakai `dwh`).
-- Aman: schema datamart berisi tabel + sequence saja (0 view, 0 function),
-- tidak ada cross-schema dependency, dan tidak ada referensi `datamart` di kode.
-- ALTER SCHEMA RENAME memindahkan semua objek (berbasis OID) sekaligus.
--
-- Idempotent & guarded — hanya rename bila `datamart` ada dan `dwh` belum ada.
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

DO $$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'dwh') THEN
    RAISE NOTICE 'Schema dwh sudah ada — skip (asumsi rename sudah pernah dijalankan).';
  ELSIF EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'datamart') THEN
    EXECUTE 'ALTER SCHEMA datamart RENAME TO dwh';
    RAISE NOTICE 'Renamed schema datamart -> dwh.';
  ELSE
    RAISE NOTICE 'Schema datamart tidak ditemukan — tidak ada yang di-rename.';
  END IF;
END $$;
