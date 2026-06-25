-- DWH View: dwh.v_export_penghimpunan_website
-- Portal: zakat
-- Purpose: Export data penghimpunan berdasarkan date range dengan pivot 8 produk (varian New)
-- Sumber: transaction.transaction + transactionitem + accounttransactionitem + productaccount +
--         transaction.product + fund.donor + fund.individualdonor + fund.workarea
-- Kolom output: 32 kolom dengan pivot 8 jenis produk ZIS
-- Dipakai oleh: report-api/fundraising/export-penghimpunan-website/date-range

CREATE OR REPLACE VIEW dwh.v_export_penghimpunan_website AS
SELECT
  d.donorno                                 AS donor_number,
  d.donorname                               AS donor_name,
  COALESCE(id.gender, '')                   AS gender,
  CASE
    WHEN COALESCE(id.gender, '') = 'P' THEN 'Female'
    ELSE 'Male'
  END                                       AS gender_display,
  COALESCE(id.maritalstate, '')             AS marital_state,
  CASE
    WHEN id.maritalstate = 'K' THEN 'Menikah'
    WHEN id.maritalstate = 'B' THEN 'Belum Menikah'
    WHEN id.maritalstate = 'J' THEN 'Cerai'
    ELSE ''
  END                                       AS marital_display,
  COALESCE(d.addressstreet, '')             AS address,
  COALESCE(d.phonenumber, '')               AS phone_number,
  COALESCE(id.email, '')                    AS email,
  COALESCE(id.corporatename, '')            AS organization_name,
  COALESCE(id.isinternalemployee, '')       AS is_internal_employee,
  CASE
    WHEN id.isinternalemployee = 'T' THEN 'Ya'
    ELSE 'Tidak'
  END                                       AS employee_display,
  SUM(CAST(ti.amount AS NUMERIC(20,4)))     AS total_donation,
  MIN(CAST(t.actualdate AS DATE))           AS first_donation_date,
  MAX(CAST(t.actualdate AS DATE))           AS last_donation_date,
  COALESCE(SUM(CASE WHEN p.productcode IN ('0101', '0103') THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END), 0) AS nominal_zakat,
  COUNT(CASE WHEN p.productcode IN ('0101', '0103') THEN 1 END) AS nominal_zakat_count,
  COALESCE(SUM(CASE WHEN p.productcode = '0102' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END), 0) AS nominal_fitrah,
  COUNT(CASE WHEN p.productcode = '0102' THEN 1 END) AS nominal_fitrah_count,
  COALESCE(SUM(CASE WHEN p.productcode = '02021' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END), 0) AS nominal_infak_sedekah,
  COUNT(CASE WHEN p.productcode = '02021' THEN 1 END) AS nominal_infak_sedekah_count,
  COALESCE(SUM(CASE WHEN p.productcode = '02011' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END), 0) AS nominal_anak_asuh,
  COUNT(CASE WHEN p.productcode = '02011' THEN 1 END) AS nominal_anak_asuh_count,
  COALESCE(SUM(CASE WHEN p.productcode = '02012' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END), 0) AS nominal_anak_yatim,
  COUNT(CASE WHEN p.productcode = '02012' THEN 1 END) AS nominal_anak_yatim_count,
  COALESCE(SUM(CASE WHEN p.productcode = '02014' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END), 0) AS nominal_dpu,
  COUNT(CASE WHEN p.productcode = '02014' THEN 1 END) AS nominal_dpu_count,
  COALESCE(SUM(CASE WHEN p.productcode = '0301' THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END), 0) AS nominal_wakaf,
  COUNT(CASE WHEN p.productcode = '0301' THEN 1 END) AS nominal_wakaf_count,
  COALESCE(SUM(CASE WHEN p.productcode IN ('02013', '0401') THEN CAST(ti.amount AS NUMERIC(20,4)) ELSE 0 END), 0) AS nominal_qurban,
  COUNT(CASE WHEN p.productcode IN ('02013', '0401') THEN 1 END) AS nominal_qurban_count
FROM transaction.transaction t
INNER JOIN transaction.transactionitem ti
  ON t.transactionid = ti.transactionid
INNER JOIN transaction.accounttransactionitem ati
  ON ti.transactionitemid = ati.transactionitemid
INNER JOIN transaction.productaccount pa
  ON ati.accountno = pa.accountno
INNER JOIN transaction.product p
  ON pa.productid = p.productid
INNER JOIN fund.donor d
  ON t.donorid = d.donorid
LEFT JOIN fund.individualdonor id
  ON d.donorid = id.donorid
LEFT JOIN fund.workarea wa
  ON id.workareaid = wa.workareaid
GROUP BY
  d.donorid,
  d.donorno,
  d.donorname,
  id.donorid,
  id.gender,
  id.maritalstate,
  id.email,
  id.corporatename,
  id.isinternalemployee,
  d.addressstreet,
  d.phonenumber;

COMMENT ON VIEW dwh.v_export_penghimpunan_website IS
'View untuk export penghimpunan per date range dengan pivot 8 jenis produk ZIS. Menampilkan 32 kolom: donor info (14 kolom), total donation (3 kolom), dan 8 jenis produk × 2 kolom (nominal + count)';
