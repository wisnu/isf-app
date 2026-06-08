-- APPLY TO: mziss_laz, mziss_wakaf
-- ROLLBACK:
-- ALTER TABLE otorisasi.submission DROP CONSTRAINT IF EXISTS submission_status_check;
-- ALTER TABLE otorisasi.submission
--     ADD CONSTRAINT submission_status_check
--         CHECK (status IN ('DRAFT','PENDING','AUTHORIZED','REJECTED'));
-- ALTER TABLE otorisasi.submission DROP COLUMN IF EXISTS dispatch_error;

-- MIGRATION: Tambah status PROCESSING dan kolom dispatch_error ke otorisasi.submission
-- Dibutuhkan untuk async dispatch via FastAPI BackgroundTasks:
-- approve endpoint langsung return PROCESSING, dispatcher berjalan di background.

ALTER TABLE otorisasi.submission DROP CONSTRAINT IF EXISTS submission_status_check;
ALTER TABLE otorisasi.submission
    ADD CONSTRAINT submission_status_check
        CHECK (status IN ('DRAFT','PENDING','AUTHORIZED','REJECTED','PROCESSING'));

ALTER TABLE otorisasi.submission
    ADD COLUMN IF NOT EXISTS dispatch_error VARCHAR(500);
