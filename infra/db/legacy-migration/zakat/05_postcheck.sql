-- 05_postcheck.sql — Verifikasi setelah migrasi (dijalankan dalam transaksi yang sama;
-- bila ada assert gagal → seluruh migrasi di-ROLLBACK otomatis).
-- Angka ekspektasi = hasil diff mziss_laz_origin vs mziss_laz (2026-11-18).

SET client_min_messages = notice;  -- 02/03 (pg_dump) menyetel 'warning'

DO $$
DECLARE
  n int;
  v text;
BEGIN
  -- Schema & objek baru
  SELECT count(*) INTO n FROM information_schema.tables WHERE table_schema='otorisasi' AND table_type='BASE TABLE';
  IF n <> 3 THEN RAISE EXCEPTION 'POSTCHECK: otorisasi tables = % (expected 3)', n; END IF;

  SELECT count(*) INTO n FROM information_schema.tables WHERE table_schema='dwh' AND table_type='BASE TABLE';
  IF n <> 14 THEN RAISE EXCEPTION 'POSTCHECK: dwh tables = % (expected 14)', n; END IF;

  SELECT count(*) INTO n FROM information_schema.views WHERE table_schema='dwh';
  IF n <> 29 THEN RAISE EXCEPTION 'POSTCHECK: dwh views = % (expected 29)', n; END IF;

  -- Kolom baru di tabel legacy
  SELECT string_agg(x, ', ') INTO v FROM (VALUES
      ('fund','individualdonor','donorgroup'),
      ('transaction','batchupload','authstatus'),
      ('transaction','budgetowner','tglubah'),
      ('transaction','budgetowner','userpengubah'),
      ('transaction','budgetowner','terminalubah'),
      ('transaction','humancapitalbatch','namafile'),
      ('transaction','transactiontype','jenis_limit')) c(s,t,x)
  WHERE NOT EXISTS (SELECT 1 FROM information_schema.columns
                    WHERE table_schema=c.s AND table_name=c.t AND column_name=c.x);
  IF v IS NOT NULL THEN RAISE EXCEPTION 'POSTCHECK: kolom belum ada: %', v; END IF;

  -- Data config
  SELECT count(*) INTO n FROM otorisasi.entity_config;
  IF n < 16 THEN RAISE EXCEPTION 'POSTCHECK: entity_config = % (expected >= 16)', n; END IF;

  SELECT count(*) INTO n FROM transaction.transactiontype WHERE jenis_limit IS NULL;
  IF n > 0 THEN RAISE EXCEPTION 'POSTCHECK: % transactiontype tanpa jenis_limit', n; END IF;

  SELECT count(*) INTO n FROM transaction.batchupload
   WHERE authstatus = 'P' AND authorizeduser IS NOT NULL AND authorizeduser <> '';
  IF n > 0 THEN RAISE EXCEPTION 'POSTCHECK: % batch legacy ter-otorisasi masih P (risiko posting ganda)', n; END IF;

  -- Semua view dwh harus bisa dieksekusi terhadap data legacy (deteksi kolom/tipe hilang)
  FOR v IN SELECT table_name FROM information_schema.views WHERE table_schema='dwh' ORDER BY 1 LOOP
    EXECUTE format('SELECT 1 FROM dwh.%I LIMIT 0', v);
  END LOOP;

  RAISE NOTICE 'POSTCHECK OK';
END $$;

-- Ringkasan (informasi)
SELECT 'batchupload' AS item, authstatus AS key, count(*) AS n FROM transaction.batchupload GROUP BY 2
UNION ALL SELECT 'entity_config', NULL, count(*) FROM otorisasi.entity_config
UNION ALL SELECT 'dim_branch', NULL, count(*) FROM dwh.dim_branch
ORDER BY 1, 2;
