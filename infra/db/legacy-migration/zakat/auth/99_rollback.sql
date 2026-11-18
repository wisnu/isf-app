-- 99_rollback.sql — Hapus schema isf_auth dari auth DB (user, kredensial, menu, audit log ikut hilang).
-- ⚠️ Setelah ini JANGAN start BFF sebelum init ulang: users kosong → BFF men-seed ADMIN/admin123.
DROP SCHEMA IF EXISTS isf_auth CASCADE;
