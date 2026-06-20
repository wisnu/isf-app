# Glossary — Canonical Indonesian → English Naming

> Single source of truth for the `refactor-naming-english` effort.
> Portal: **zakat first** (`apps_zakat/`), mirror to wakaf in a follow-up.
> Every rename in `specs.md` / `plan.md` MUST trace back to a row here.

## 1. Domain / module names (files, folders, URL prefixes, functions)

| Indonesian | English (canonical) | Transaction code | Notes |
|---|---|---|---|
| penghimpunan | `fund-collection` (path) / `fund_collection` (py) | SD001 | already English in web-vue folder |
| penyaluran | `fund-distribution` / `fund_distribution` | DD001 | |
| piutang | `receivable` | EAR / PEAR | loan (Pinjam) / repay (Bayar) |
| uang-muka | `cash-advance` / `cash_advance` | KK | |
| uang-muka-pengembalian | `cash-advance-settlement` / `cash_advance_settlement` | LPJ | DECIDED 2026-06-20: "settlement" (LPJ = pertanggungjawaban) |
| transfer-antar-rekening | `inter-account-transfer` / `inter_account_transfer` | TI | |
| transaksi-umum / umum | `general-transaction` / `general_transaction` | GT | |
| transaksi-histori | `transaction-history` / `transaction_history` | — | |
| kas-kecil | `petty-cash` / `petty_cash` | — | account_interface = `KKC` |
| otorisasi | `authorization` | — | menu key already `...authorization` |
| pemilik-anggaran | `budget-owner` / `budget_owner` | — | |
| amil-income | `amil-income` (keep) | CI | already English |
| hc-zis | `hc-zis` (keep) | HC ZIS | acronym, keep |

## 2. Lookup sub-paths

| Old | New |
|---|---|
| `lookup/rekening` | `lookup/account` |
| `lookup/produk` | `lookup/product` |
| `lookup/kasbank` | `lookup/cash-bank` |
| `lookup/penyaluran` | `lookup/distribution` |
| `lookup/donor` | `lookup/donor` (keep) |
| `lookup/ashnaf` | `lookup/ashnaf` (keep — Islamic term) |
| `debitur` / `debitur-external` | `debtor` / `debtor-external` |
| `lookup/open-uang-muka` | `lookup/open-cash-advance` |

## 3. JSON field names (response/payload — the frontend contract)

| Indonesian field | English (canonical) | Where |
|---|---|---|
| no_rekening | account_no | penghimpunan items, upload ParsedRow (`rekening`→`account_no`) |
| tanggal | date | penghimpunan, upload, query params |
| keterangan | description | penghimpunan, upload |
| no_ref | reference_no | penghimpunan |
| total_kredit | total_credit | penghimpunan |
| nominal | amount | upload ParsedRow, general-transaction |
| pesan | message | penghimpunan validation |
| zakat_profesi | zakat_profession | penghimpunan product |
| zakat_maal | zakat_wealth | penghimpunan product |
| zakat_perusahaan | zakat_company | penghimpunan product |
| infaq_terikat | infaq_restricted | penghimpunan product |
| anak_yatim | orphan | penghimpunan product |
| anak_asuh | foster_child | penghimpunan product |
| titipan_wakaf | waqf_deposit | penghimpunan product |
| titipan_qurban | qurban_deposit | penghimpunan product |
| tanggal_transaksi | transaction_date | HC-ZIS, query param |
| namafile | filename | HC-ZIS |
| batch_period_desc | batch_period_description | HC-ZIS |
| anak_asuh_amount | foster_child_amount | HC-ZIS |
| anak_yatim_amount | orphan_amount | HC-ZIS |
| taqurma_amount | qurban_deposit_amount | HC-ZIS |
| ownerid | owner_id | parameter/budget-owner |
| ownercode | owner_code | parameter/budget-owner |
| ownername | owner_name | parameter/budget-owner |
| tglubah | updated_date | parameter/budget-owner |
| userpengubah | updated_by | parameter/budget-owner |
| terminalubah | updated_terminal | parameter/budget-owner |
| id_peran | role_id | identity profile, admin role-menu |
| nama_peran | role_name | identity profile, admin |
| kode_cabang | branch_code | identity profile |
| valuta_code | currency_code | transaction-history, also `currencycode` |
| ekuivalen_amount | equivalent_amount | amil-income |
| produk | product | dashboard, lookups |
| rekening | account | dashboard RekeningBundle |
| anggaran | budget | dashboard |
| saldo_awal / saldo_akhir / mutasi | opening_balance / closing_balance / movement | report payloads |

### camelCase → snake_case normalization (transaction-history, same legacy DB columns)
`transactionid→transaction_id`, `transactionno→transaction_no`, `transactiondate→transaction_date`,
`actualdate→actual_date`, `donorno→donor_no`, `donorname→donor_name`, `referenceno→reference_no`,
`isposted→is_posted`, `branchcode→branch_code`, `channelaccountno→channel_account_no`,
`channelname→channel_name`, `exttransactionid→external_transaction_id`, `subaccountcode→subaccount_code`,
`subaccountname→subaccount_name`, `debtorname→debtor_name`, `currencycode→currency_code`,
`cashaccountno→cash_account_no`, `cashaccounttype→cash_account_type`.

## 4. Query parameters

| Old | New |
|---|---|
| tanggal | date |
| tanggal_transaksi | transaction_date |
| jenisperiode | period_type |
| bulan | month |
| tahun | year |

## 5. ⛔ FREEZE — DO NOT RENAME (discriminators & domain codes)

These are **values/codes persisted in the DB or fixed Islamic terms**, not naming. Renaming
them requires data migration and/or breaks domain meaning. Treat as opaque.

| Item | Reason to freeze |
|---|---|
| `entity_type` **values** (`penghimpunan`, `penyaluran`, `piutang`, `transaksi_umum`, `bank`, …) | Stored in `otorisasi.submission.entity_type` + `otorisasi.entity_config` rows + dispatcher registry keys. Renaming = data migration of live submissions. **DECIDED 2026-06-20: FREEZE.** |
| `transactioncode`: SD001, DD001, KK, EAR, PEAR, TI, GT, CI | DB-persisted discriminator on `transaction.transaction` |
| `fund_entity` 1–5 (Zakat/Infaq/Wakaf/Amil/Non-halal) | numeric code |
| `debtor_type` E/X, `authstatus` T/P/R, `payment_type` K/C/B, `mutation_type` D/C | single-char codes |
| `account_interface` = KKC (petty cash) | DB value |
| **Islamic terms**: `ashnaf`, `zakat_fitrah`, `infaq`, `wakaf`/`waqf`, `qurban`, `amil` | domain vocabulary, keep |
| Actual **DB column names** (`no_rekening`, `ownerid`, `valuta_code`, `transactionid`, …) | legacy DB — alias in `SELECT ... AS english`, never `ALTER` |
| **Upload-batch product-key fields** (`no_rekening`, `tanggal`, `keterangan`, `no_ref`, `total_kredit`, `zakat_profesi/maal/fitrah/perusahaan`, `infaq_terikat`, `anak_yatim/asuh`, `titipan_wakaf/qurban`, `pesan`) in `transaction/schema.py` ParsedRow | FROZEN 2026-06-20: coupled to `PRODUCT_ID_MAP`/`FIELD_MAP` via getattr/dict-key, shared with `hc_zis_commit.py`, persisted in batch JSONB. Discriminator-like → rename would risk parse→commit pipeline. Only `/upload/penghimpunan`→`/upload/fund-collection` PATH renamed. |
