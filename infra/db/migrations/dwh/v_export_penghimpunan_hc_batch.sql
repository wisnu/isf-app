-- DWH View: dwh.v_export_penghimpunan_hc_batch
-- Portal: zakat
-- Purpose: Export data penghimpunan berdasarkan HC Batch (varian lama)
-- Sumber: transaction.humancapitalbatch + transaction.humancapitalbatchitem + fund.donor + fund.individualdonor
-- Kolom output: 9 kolom untuk export Excel
-- Dipakai oleh: report-api/fundraising/export-penghimpunan-website/hc-batch

CREATE OR REPLACE VIEW dwh.v_export_penghimpunan_hc_batch AS
SELECT
  hbi.batchid                              AS batch_id,
  hb.batchperioddesc                      AS batch_name,
  CAST(hb.transactiondate AS DATE)        AS batch_date,
  COALESCE(d.donorno, CAST(hbi.donorid AS VARCHAR))  AS donor_number,
  COALESCE(d.donorname, hbi.name)         AS donor_name,
  ''                                      AS product_code,
  ''                                      AS product_name,
  CAST(COALESCE(hbi.amountzakat, 0) + COALESCE(hbi.amountinfaq, 0) +
       COALESCE(hbi.amountanakasuh, 0) + COALESCE(hbi.amountanakyatim, 0) +
       COALESCE(hbi.amountqurban, 0) + COALESCE(hbi.amountwakaf, 0) AS NUMERIC(20,4)) AS donation_amount,
  CAST(COALESCE(hbi.smslog_time, hb.transactiondate) AS DATE) AS donation_date
FROM transaction.humancapitalbatchitem hbi
LEFT JOIN transaction.humancapitalbatch hb
  ON hbi.batchid = hb.batchid
LEFT JOIN fund.donor d
  ON hbi.donorid = d.donorid
WHERE hbi.batchid IS NOT NULL;

COMMENT ON VIEW dwh.v_export_penghimpunan_hc_batch IS
'View untuk export penghimpunan per HC Batch. Menampilkan 9 kolom: batch_id, batch_name, batch_date, donor_number, donor_name, product_code, product_name, donation_amount, donation_date';
