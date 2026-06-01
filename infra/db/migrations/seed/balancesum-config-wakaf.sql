-- [REPORT-ACCT] Seed config BalanceSum* — portal wakaf (DB mziss_wakaf)
--
-- Config legacy (transaction.*) untuk laporan Arus Kas (AK_*) & Perubahan Dana (PD_*).
-- ⚠️ PORTAL-SPECIFIC: account mapping & item beda antar portal — JANGAN apply ke DB lain.
-- Di-recover dari mziss_wakaf. Idempotent (ON CONFLICT). itemid/memberid eksplisit (FK konsisten).
--
-- Apply: PGPASSWORD=solusi psql -h localhost -U transaction -d mziss_wakaf -f <file>

BEGIN;

INSERT INTO transaction.balancesumgroup (groupcode, groupname, groupdescription) VALUES
  ('AK_BAL', 'Arus Kas (Saldo Awal)', 'Saldo Awal Account untuk laporan Arus Kas'),
  ('AK_MUT', 'Arus Kas (Mutasi)', 'Summary Mutasi Account untuk laporan Arus Kas'),
  ('PD_BAL', 'Perubahan Dana (Saldo Awal)', 'Saldo Awal Account untuk laporan Perubahan Dana'),
  ('PD_MUT', 'Perubahan Dana (Mutasi)', 'Summary Mutasi Account untuk laporan Perubahan Dana')
ON CONFLICT (groupcode) DO UPDATE SET groupname=EXCLUDED.groupname, groupdescription=EXCLUDED.groupdescription;

INSERT INTO transaction.balancesumitem (itemid, itemcode, itemname, groupcode) VALUES
  (43, 'WakafCollProd', 'Wakaf Uang/Produktif', 'PD_MUT'),
  (44, 'WakafCollUang', 'Wakaf Melalui Uang', 'PD_MUT'),
  (45, 'WakafUkurUang', 'Wakaf Uang/Produktif', 'PD_MUT'),
  (46, 'WakafUkurAset', 'Wakaf Aset Tetap (Penyusutan)', 'PD_MUT'),
  (47, 'WakafAlihUang', 'Wakaf Melalui Uang', 'PD_MUT'),
  (48, 'WakafKelolaBagHas', 'Bagi Hasil', 'PD_MUT'),
  (49, 'WakafKelolaBeban', 'Beban Pengelolaan dan Pengembangan', 'PD_MUT'),
  (50, 'WakafKelolaNazhir', 'Bagian Nazhir atas Bagi Hasil Pengelolaan dan Pengembangan Aset Wakaf yang Sudah Terealisasi', 'PD_MUT'),
  (51, 'WakafBeban', 'Beban', 'PD_MUT'),
  (52, 'AsetNetoBalance', 'Saldo Awal Wakaf Permanen', 'PD_BAL'),
  (53, 'OpsPenerimaanWakaf', 'Penerimaan Wakaf', 'AK_MUT'),
  (54, 'OpsKelolaWakaf', 'Pengelolaan Dan Pengembangan Aset Wakaf', 'AK_MUT'),
  (55, 'OpsUtangPenyaluran', 'Utang Penyaluran', 'AK_MUT'),
  (56, 'OpsBeban', 'Beban Pengelolaan', 'AK_MUT'),
  (57, 'KasInvAset', 'Pembelian/Penjualan Aset', 'AK_MUT'),
  (58, 'KasInvLain', 'Pembelian/Penjualan Investasi Lain', 'AK_MUT'),
  (59, 'KasBalance', 'Saldo Awal Kas', 'AK_BAL')
ON CONFLICT (itemid) DO UPDATE SET itemcode=EXCLUDED.itemcode, itemname=EXCLUDED.itemname, groupcode=EXCLUDED.groupcode;

INSERT INTO transaction.balancesumitemmember (memberid, itemid, account_code) VALUES
  (451, 43, '410101'),
  (452, 44, '410102'),
  (453, 45, '410201'),
  (454, 46, '410202'),
  (455, 47, '410301'),
  (456, 48, '410401'),
  (457, 49, '410402'),
  (458, 50, '410403'),
  (459, 51, '500000'),
  (460, 52, '310000'),
  (461, 53, '410100'),
  (462, 53, '410200'),
  (463, 53, '410300'),
  (464, 54, '410400'),
  (465, 55, '210100'),
  (467, 56, '500001'),
  (468, 56, '500002'),
  (469, 56, '500003'),
  (470, 56, '500004'),
  (471, 56, '500005'),
  (472, 56, '500006'),
  (473, 56, '500007'),
  (474, 56, '500008'),
  (475, 57, '120100'),
  (476, 58, '120300'),
  (477, 59, '110100')
ON CONFLICT (memberid) DO UPDATE SET itemid=EXCLUDED.itemid, account_code=EXCLUDED.account_code;

COMMIT;
