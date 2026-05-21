# Data Dictionary — Schema `migration`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `migration`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `seq_errorbatch` | `migration` |  | needs_review | 852558 | 852558 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_uploadbatch` | `migration` |  | needs_review | 4050 | 4050 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Tables

Daftar table:

- [`migration.bankaccount_convert`](#table-migration-bankaccount-convert) — 3 kolom
- [`migration.cabang_reset_candidate`](#table-migration-cabang-reset-candidate) — 1 kolom
- [`migration.coaconv_account_laz_old`](#table-migration-coaconv-account-laz-old) — 17 kolom
- [`migration.coaconv_accounthierarchy_laz_old`](#table-migration-coaconv-accounthierarchy-laz-old) — 3 kolom
- [`migration.coaconv_accountinstance_laz_old`](#table-migration-coaconv-accountinstance-laz-old) — 20 kolom
- [`migration.coaconv_assetwakaf`](#table-migration-coaconv-assetwakaf) — 1 kolom
- [`migration.coaconv_balancesumitemmember_bck`](#table-migration-coaconv-balancesumitemmember-bck) — 3 kolom
- [`migration.coaconv_bankremove`](#table-migration-coaconv-bankremove) — 1 kolom
- [`migration.coaconv_bankwakaf`](#table-migration-coaconv-bankwakaf) — 1 kolom
- [`migration.coaconv_cashaccount_remove`](#table-migration-coaconv-cashaccount-remove) — 12 kolom
- [`migration.coaconv_cashaccount_wakaf`](#table-migration-coaconv-cashaccount-wakaf) — 12 kolom
- [`migration.coaconv_cashflowmember_bck`](#table-migration-coaconv-cashflowmember-bck) — 9 kolom
- [`migration.coaconv_dailybalance_laz_old`](#table-migration-coaconv-dailybalance-laz-old) — 20 kolom
- [`migration.coaconv_depreciableasset_wakaf`](#table-migration-coaconv-depreciableasset-wakaf) — 11 kolom
- [`migration.coaconv_financialaccount_remove`](#table-migration-coaconv-financialaccount-remove) — 12 kolom
- [`migration.coaconv_financialaccount_wakaf`](#table-migration-coaconv-financialaccount-wakaf) — 12 kolom
- [`migration.coaconv_fixedasset_wakaf`](#table-migration-coaconv-fixedasset-wakaf) — 20 kolom
- [`migration.coaconv_glinterface_tran_bck`](#table-migration-coaconv-glinterface-tran-bck) — 6 kolom
- [`migration.coaconv_glinterfacemember_perso_bck`](#table-migration-coaconv-glinterfacemember-perso-bck) — 6 kolom
- [`migration.coaconv_globalglinterface_bck`](#table-migration-coaconv-globalglinterface-bck) — 3 kolom
- [`migration.coaconv_journal_laz_bck`](#table-migration-coaconv-journal-laz-bck) — 28 kolom
- [`migration.coaconv_journal_remove_suspect`](#table-migration-coaconv-journal-remove-suspect) — 1 kolom
- [`migration.coaconv_journal_wakaf_bck`](#table-migration-coaconv-journal-wakaf-bck) — 28 kolom
- [`migration.coaconv_journal_wakaf_candidate`](#table-migration-coaconv-journal-wakaf-candidate) — 1 kolom
- [`migration.coaconv_journalitem_laz_bck`](#table-migration-coaconv-journalitem-laz-bck) — 36 kolom
- [`migration.coaconv_journalitem_laz_old`](#table-migration-coaconv-journalitem-laz-old) — 36 kolom
- [`migration.coaconv_journalitem_wakaf_bck`](#table-migration-coaconv-journalitem-wakaf-bck) — 36 kolom
- [`migration.coaconv_transaction_laz_noitem`](#table-migration-coaconv-transaction-laz-noitem) — 36 kolom
- [`migration.coaconv_transaction_remove_bck`](#table-migration-coaconv-transaction-remove-bck) — 36 kolom
- [`migration.coaconv_transaction_remove_suspect`](#table-migration-coaconv-transaction-remove-suspect) — 1 kolom
- [`migration.coaconv_transaction_wakaf_bck`](#table-migration-coaconv-transaction-wakaf-bck) — 36 kolom
- [`migration.coaconv_transaction_wakaf_candidate`](#table-migration-coaconv-transaction-wakaf-candidate) — 1 kolom
- [`migration.coaconv_transactionitem_laz_bck`](#table-migration-coaconv-transactionitem-laz-bck) — 17 kolom
- [`migration.coaconv_transactionitem_laz_old`](#table-migration-coaconv-transactionitem-laz-old) — 17 kolom
- [`migration.coaconv_transactionitem_remove_bck`](#table-migration-coaconv-transactionitem-remove-bck) — 17 kolom
- [`migration.coaconv_transactionitem_wakaf_bck`](#table-migration-coaconv-transactionitem-wakaf-bck) — 17 kolom
- [`migration.denomkhasanah`](#table-migration-denomkhasanah) — 6 kolom
- [`migration.depr_fix_journalitem`](#table-migration-depr-fix-journalitem) — 6 kolom
- [`migration.depr_fix_transactionitem`](#table-migration-depr-fix-transactionitem) — 6 kolom
- [`migration.enum_varchar`](#table-migration-enum-varchar) — 3 kolom
- [`migration.errorbatch`](#table-migration-errorbatch) — 6 kolom
- [`migration.errorcode`](#table-migration-errorcode) — 2 kolom
- [`migration.financialaccount_migbalance`](#table-migration-financialaccount-migbalance) — 2 kolom
- [`migration.glinterface_fidyah`](#table-migration-glinterface-fidyah) — 6 kolom
- [`migration.journalitem_repair`](#table-migration-journalitem-repair) — 4 kolom
- [`migration.kasteller`](#table-migration-kasteller) — 5 kolom
- [`migration.khasanah`](#table-migration-khasanah) — 5 kolom
- [`migration.konversi_kode_produk`](#table-migration-konversi-kode-produk) — 3 kolom
- [`migration.konversi_nomor_rekening`](#table-migration-konversi-nomor-rekening) — 3 kolom
- [`migration.list_glinterface`](#table-migration-list-glinterface) — 3 kolom
- [`migration.parameterglobal`](#table-migration-parameterglobal) — 6 kolom
- [`migration.produkdeposito`](#table-migration-produkdeposito) — 33 kolom
- [`migration.produkrencana`](#table-migration-produkrencana) — 47 kolom
- [`migration.produktabungan`](#table-migration-produktabungan) — 44 kolom
- [`migration.repair_journalblock_bck`](#table-migration-repair-journalblock-bck) — 9 kolom
- [`migration.repair_journalitemupload_bck`](#table-migration-repair-journalitemupload-bck) — 36 kolom
- [`migration.repair_journalupload_bck`](#table-migration-repair-journalupload-bck) — 28 kolom
- [`migration.repair_transaction_bck`](#table-migration-repair-transaction-bck) — 36 kolom
- [`migration.script_collection`](#table-migration-script-collection) — 4 kolom
- [`migration.templatemigration`](#table-migration-templatemigration) — 9 kolom
- [`migration.tmp_accountofficer`](#table-migration-tmp-accountofficer) — 4 kolom
- [`migration.tmp_bankcash`](#table-migration-tmp-bankcash) — 16 kolom
- [`migration.tmp_coa`](#table-migration-tmp-coa) — 10 kolom
- [`migration.tmp_denominasi_khasanah`](#table-migration-tmp-denominasi-khasanah) — 6 kolom
- [`migration.tmp_deposito`](#table-migration-tmp-deposito) — 67 kolom
- [`migration.tmp_donorinactivated`](#table-migration-tmp-donorinactivated) — 4 kolom
- [`migration.tmp_glinterface`](#table-migration-tmp-glinterface) — 7 kolom
- [`migration.tmp_histtransaksi_candidate`](#table-migration-tmp-histtransaksi-candidate) — 15 kolom
- [`migration.tmp_histtransaksi_tabgir`](#table-migration-tmp-histtransaksi-tabgir) — 11 kolom
- [`migration.tmp_histtransaksi_tabgir_bus`](#table-migration-tmp-histtransaksi-tabgir-bus) — 11 kolom
- [`migration.tmp_journal_candidate`](#table-migration-tmp-journal-candidate) — 5 kolom
- [`migration.tmp_journalitem_history`](#table-migration-tmp-journalitem-history) — 11 kolom
- [`migration.tmp_kasteller`](#table-migration-tmp-kasteller) — 7 kolom
- [`migration.tmp_khasanah`](#table-migration-tmp-khasanah) — 5 kolom
- [`migration.tmp_list_rek_disposisi_baghas`](#table-migration-tmp-list-rek-disposisi-baghas) — 5 kolom
- [`migration.tmp_mappingcoa`](#table-migration-tmp-mappingcoa) — 4 kolom
- [`migration.tmp_mig_trans`](#table-migration-tmp-mig-trans) — 3 kolom
- [`migration.tmp_nasabahindividu`](#table-migration-tmp-nasabahindividu) — 138 kolom
- [`migration.tmp_neracasaldo`](#table-migration-tmp-neracasaldo) — 6 kolom
- [`migration.tmp_neracasaldo_mapcoa`](#table-migration-tmp-neracasaldo-mapcoa) — 6 kolom
- [`migration.tmp_neracasaldo_nonmapping`](#table-migration-tmp-neracasaldo-nonmapping) — 6 kolom
- [`migration.tmp_rekeningliabilitas_update`](#table-migration-tmp-rekeningliabilitas-update) — 6 kolom
- [`migration.tmp_rekeningperantara`](#table-migration-tmp-rekeningperantara) — 8 kolom
- [`migration.tmp_repair_saldo`](#table-migration-tmp-repair-saldo) — 4 kolom
- [`migration.tmp_saldo_awal_rekening`](#table-migration-tmp-saldo-awal-rekening) — 4 kolom
- [`migration.tmp_tabgir`](#table-migration-tmp-tabgir) — 55 kolom
- [`migration.tmp_tabrencanarutin`](#table-migration-tmp-tabrencanarutin) — 60 kolom
- [`migration.tmp_tranjournal_candidate`](#table-migration-tmp-tranjournal-candidate) — 2 kolom
- [`migration.tmp_update_nama_rekening`](#table-migration-tmp-update-nama-rekening) — 5 kolom
- [`migration.tmp_userapp`](#table-migration-tmp-userapp) — 8 kolom
- [`migration.tmp_usertraining`](#table-migration-tmp-usertraining) — 5 kolom
- [`migration.uploadbatch`](#table-migration-uploadbatch) — 12 kolom

### Table `migration.bankaccount_convert` <a id="table-migration-bankaccount-convert"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `bankaccount_convert` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno_bank` | `character varying(20)` | NO |  | PK | YES | partial | synthetic_only | NO | needs_review |
| 2 | `account_code_baru` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `saldo_awal` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno_bank)` |  |

### Table `migration.cabang_reset_candidate` <a id="table-migration-cabang-reset-candidate"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `cabang_reset_candidate` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_cabang` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_account_laz_old` <a id="table-migration-coaconv-account-laz-old"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_account_laz_old` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `account_name` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `account_level` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `is_detail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `account_type` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `is_system` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `time_last_modified` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `fl_parent_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `time_create` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `fl_cpa_accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `fl_lpa_accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `isactivaoffbalancesheet` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `isrpvrakreportshow` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `isrpvaccount` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_accounthierarchy_laz_old` <a id="table-migration-coaconv-accounthierarchy-laz-old"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_accounthierarchy_laz_old` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accounthierarchy_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `fl_parentaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `fl_childaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_accountinstance_laz_old` <a id="table-migration-coaconv-accountinstance-laz-old"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_accountinstance_laz_old` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `fl_cpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `fl_lpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `balance_ratarata` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `balance_ratarata_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `trial_balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `trial_balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `balance_harilalu` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `balance_harilalu_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `isbolehinput` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `currency_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `dailybalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `periodebalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `dailyprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `periodeprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `balance_sign` | `numeric(1,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_assetwakaf` <a id="table-migration-coaconv-assetwakaf"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_assetwakaf` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `assetregnumber` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (assetregnumber)` |  |

### Table `migration.coaconv_balancesumitemmember_bck` <a id="table-migration-coaconv-balancesumitemmember-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_balancesumitemmember_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `memberid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `itemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_bankremove` <a id="table-migration-coaconv-bankremove"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_bankremove` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno_bank` | `character varying(20)` | NO |  | PK | YES | partial | synthetic_only | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno_bank)` |  |

### Table `migration.coaconv_bankwakaf` <a id="table-migration-coaconv-bankwakaf"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_bankwakaf` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno_bank` | `character varying(20)` | NO |  | PK | YES | partial | synthetic_only | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno_bank)` |  |

### Table `migration.coaconv_cashaccount_remove` <a id="table-migration-coaconv-cashaccount-remove"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_cashaccount_remove` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `accountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `balance` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `financialaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `openingdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `accountcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `lastdaybalance` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `lastdailybalanceid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `balancedeposit` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_cashaccount_wakaf` <a id="table-migration-coaconv-cashaccount-wakaf"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_cashaccount_wakaf` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `accountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `balance` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `financialaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `openingdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `accountcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `lastdaybalance` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `lastdailybalanceid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `balancedeposit` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_cashflowmember_bck` <a id="table-migration-coaconv-cashflowmember-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_cashflowmember_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `cfmemberid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `cfgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `trancodeexclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `trancodeinclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `journalcodeexclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `journalcodeinclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `additionalinfo` | `character varying(300)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_dailybalance_laz_old` <a id="table-migration-coaconv-dailybalance-laz-old"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_dailybalance_laz_old` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailybalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `balance_harilalu` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `balance_harilalu_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `balance_ratarata` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `balance_ratarata_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `trial_balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `trial_balance_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `balancecumulative` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `balancecumulative_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `datevalue` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `debit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `credit_ekuiv` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `fl_accountingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_depreciableasset_wakaf` <a id="table-migration-coaconv-depreciableasset-wakaf"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_depreciableasset_wakaf` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `deprassetid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `deprassetregnumber` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `registerdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `inputdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `inputuser` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `deprassettype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `deprassetname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `depreciationsequence` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `deprassetstate` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `depreciationaccumvalue` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_financialaccount_remove` <a id="table-migration-coaconv-financialaccount-remove"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_financialaccount_remove` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `accountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `balance` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `financialaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `openingdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `accountcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `lastdaybalance` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `lastdailybalanceid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `balancedeposit` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_financialaccount_wakaf` <a id="table-migration-coaconv-financialaccount-wakaf"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_financialaccount_wakaf` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `accountname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `balance` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `financialaccounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `openingdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `accountcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `lastdaybalance` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `lastdailybalanceid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `balancedeposit` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_fixedasset_wakaf` <a id="table-migration-coaconv-fixedasset-wakaf"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_fixedasset_wakaf` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `deprassetid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `isparent` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `fatypeid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `bookvalue` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `initvalue` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `depreciationvalue` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `model` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `description` | `character varying` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `lastdeprdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `nextdeprdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `isinsured` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `insuranceduedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `stnkduedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `fixedassetcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `retiredate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `retirereason` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `retiredescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `fixedassetstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_glinterface_tran_bck` <a id="table-migration-coaconv-glinterface-tran-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_glinterface_tran_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `interfaceid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `interfacecode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `accountname` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_glinterfacemember_perso_bck` <a id="table-migration-coaconv-glinterfacemember-perso-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_glinterfacemember_perso_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glimemberid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `glimembercode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_globalglinterface_bck` <a id="table-migration-coaconv-globalglinterface-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_globalglinterface_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glinterfacecode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `glinterfacename` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_journal_laz_bck` <a id="table-migration-coaconv-journal-laz-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_journal_laz_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journal_date_posting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `journal_date_last_modified` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `is_posted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `journal_type` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `lastitemno` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `is_partlychecked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `transaction_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `journal_state` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `serial_no` | `character varying(23)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `lock_userid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `fl_origin_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `source_app` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `source_app_class` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `source_app_ref` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `fl_accountingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_journal_remove_suspect` <a id="table-migration-coaconv-journal-remove-suspect"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_journal_remove_suspect` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_journal_wakaf_bck` <a id="table-migration-coaconv-journal-wakaf-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_journal_wakaf_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journal_date_posting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `journal_date_last_modified` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `is_posted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `journal_type` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `lastitemno` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `is_partlychecked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `transaction_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `journal_state` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `serial_no` | `character varying(23)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `lock_userid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `fl_origin_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `source_app` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `source_app_class` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `source_app_ref` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `fl_accountingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_journal_wakaf_candidate` <a id="table-migration-coaconv-journal-wakaf-candidate"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_journal_wakaf_candidate` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_journalitem_laz_bck` <a id="table-migration-coaconv-journalitem-laz-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_journalitem_laz_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journalitem_no` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `amount_debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `amount_credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `branch_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `valuta_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `rc_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `generic_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `fl_posting_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `fl_project_no` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `journalitemstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `userid_check` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `dateposting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `datelastmod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `datecreate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `journalitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `kode_kurs` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `nilai_kurs` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `rpv_main` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `subsystemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `subaccountcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `subaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `id_journalblock` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `transaksirak_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `source_class_id` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `source_key_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `additionaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_journalitem_laz_old` <a id="table-migration-coaconv-journalitem-laz-old"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_journalitem_laz_old` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journalitem_no` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `amount_debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `amount_credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `branch_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `valuta_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `rc_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `generic_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `fl_posting_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `fl_project_no` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `journalitemstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `userid_check` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `dateposting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `datelastmod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `datecreate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `journalitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `kode_kurs` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `nilai_kurs` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `rpv_main` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `subsystemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `subaccountcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `subaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `id_journalblock` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `transaksirak_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `source_class_id` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `source_key_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `additionaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_journalitem_wakaf_bck` <a id="table-migration-coaconv-journalitem-wakaf-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_journalitem_wakaf_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journalitem_no` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `amount_debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `amount_credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `branch_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `valuta_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `rc_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `generic_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `fl_posting_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `fl_project_no` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `journalitemstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `userid_check` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `dateposting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `datelastmod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `datecreate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `journalitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `kode_kurs` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `nilai_kurs` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `rpv_main` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `subsystemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `subaccountcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `subaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `id_journalblock` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `transaksirak_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `source_class_id` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `source_key_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `additionaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transaction_laz_noitem` <a id="table-migration-coaconv-transaction-laz-noitem"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transaction_laz_noitem` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `referenceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `inputer` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `authuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transactiontime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `authdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `authstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `isposted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `authaction` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `journalblockid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `channelcode` | `character varying` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `sponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 19 | `volunteerid` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `actualdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `paidto` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `donorno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 24 | `donorname` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 25 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `receivedfrom` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `channelaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 30 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `journalno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `hcbatchitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `authoperationmode` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `updatedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `journalerrordescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `flag_omit_journal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transaction_remove_bck` <a id="table-migration-coaconv-transaction-remove-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transaction_remove_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `referenceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `inputer` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `authuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transactiontime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `authdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `authstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `isposted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `authaction` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `journalblockid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `channelcode` | `character varying` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `sponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 19 | `volunteerid` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `actualdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `paidto` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `donorno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 24 | `donorname` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 25 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `receivedfrom` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `channelaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 30 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `journalno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `hcbatchitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `authoperationmode` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `updatedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `journalerrordescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `flag_omit_journal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transaction_remove_suspect` <a id="table-migration-coaconv-transaction-remove-suspect"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transaction_remove_suspect` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transaction_wakaf_bck` <a id="table-migration-coaconv-transaction-wakaf-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transaction_wakaf_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `referenceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `inputer` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `authuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transactiontime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `authdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `authstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `isposted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `authaction` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `journalblockid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `channelcode` | `character varying` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `sponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 19 | `volunteerid` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `actualdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `paidto` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `donorno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 24 | `donorname` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 25 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `receivedfrom` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `channelaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 30 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `journalno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `hcbatchitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `authoperationmode` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `updatedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `journalerrordescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `flag_omit_journal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transaction_wakaf_candidate` <a id="table-migration-coaconv-transaction-wakaf-candidate"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transaction_wakaf_candidate` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transactionitem_laz_bck` <a id="table-migration-coaconv-transactionitem-laz-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transactionitem_laz_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transactionitem_laz_old` <a id="table-migration-coaconv-transactionitem-laz-old"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transactionitem_laz_old` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transactionitem_remove_bck` <a id="table-migration-coaconv-transactionitem-remove-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transactionitem_remove_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.coaconv_transactionitem_wakaf_bck` <a id="table-migration-coaconv-transactionitem-wakaf-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `coaconv_transactionitem_wakaf_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `ekuivalenamount` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `parameterjournalid` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `glname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 15 | `refaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `rc_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.denomkhasanah` <a id="table-migration-denomkhasanah"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `denomkhasanah` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nama_rekening` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `nilai_denominasi` | `numeric(22,2)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `jenis_denominasi` | `character varying(1)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `jumlah_denominasi` | `numeric(22,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `jumlah_denominasi_tle` | `numeric(22,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.depr_fix_journalitem` <a id="table-migration-depr-fix-journalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `depr_fix_journalitem` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journalitem_no` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `fl_account_fix` | `text` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `accountinstance_id_fix` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.depr_fix_transactionitem` <a id="table-migration-depr-fix-transactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `depr_fix_transactionitem` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `refaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `glnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `journalno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `accountcode_fix` | `text` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.enum_varchar` <a id="table-migration-enum-varchar"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `enum_varchar` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | NO | needs_review |
| 2 | `enum_value` | `character varying(3)` | NO | NULL::character varying | PK | NO | none | reference_allowed | NO | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `migration.errorbatch` <a id="table-migration-errorbatch"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `errorbatch` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `err_id` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `id_batch` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `primarycode` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `error_code` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `additional_desc` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `line_number` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.errorcode` <a id="table-migration-errorcode"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `errorcode` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `error_code` | `character varying(4)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `error_description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.financialaccount_migbalance` <a id="table-migration-financialaccount-migbalance"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `financialaccount_migbalance` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | NO | needs_review |
| 2 | `saldo_awal` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno)` |  |

### Table `migration.glinterface_fidyah` <a id="table-migration-glinterface-fidyah"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `glinterface_fidyah` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `interfaceid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `interfacecode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `accountname` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.journalitem_repair` <a id="table-migration-journalitem-repair"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `journalitem_repair` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journalitem_no` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `account_code_baru` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.kasteller` <a id="table-migration-kasteller"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `kasteller` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_user` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `kode_valuta` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `status_rekening` | `numeric(22,0)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 5 | `saldo` | `numeric(22,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.khasanah` <a id="table-migration-khasanah"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `khasanah` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_cabang` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nomor_rekening` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `nama_rekening` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 4 | `kode_valuta` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `saldo` | `numeric(22,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.konversi_kode_produk` <a id="table-migration-konversi-kode-produk"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `konversi_kode_produk` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_produk` | `character varying(30)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `kode_cabang` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `kode_produk_baru` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.konversi_nomor_rekening` <a id="table-migration-konversi-nomor-rekening"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `konversi_nomor_rekening` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(30)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `kode_cabang` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `nomor_rekening_baru` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |

### Table `migration.list_glinterface` <a id="table-migration-list-glinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `list_glinterface` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `jenis_produk` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `kode_interface` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `deskripsi` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.parameterglobal` <a id="table-migration-parameterglobal"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `parameterglobal` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nilai_parameter_number` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `deskripsi` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `is_parameter_system` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `nilai_parameter_string` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.produkdeposito` <a id="table-migration-produkdeposito"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `produkdeposito` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_produk` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nama_produk` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `kode_valuta` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `saldo_minimum` | `numeric(38,16)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `masa_perjanjian` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `periode_perjanjian` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `is_kena_penalty` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `nominal_penalty` | `numeric(38,16)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `is_dapat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `nisbah_bonus_dasar` | `numeric(38,16)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `is_override_bagihasilkhusus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `jarak_periode_bagihasil` | `numeric(38,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `periode_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `disposisi_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `is_override_disposisi_bgh` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `is_kena_zakat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `presentase_zakat_bagi_hasil` | `numeric(38,16)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `is_override_zakatbagihasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `is_kena_pajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `tarif_pajak` | `numeric(38,16)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `is_override_tarifpajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `gl_saldo` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `gl_biaya_bgh` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `gl_pendapatan_lay` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `gl_pajak` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `gl_zakat` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `gl_cadangan_bgh` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `gl_jttn` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `gl_jttr` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `gl_hiba` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.produkrencana` <a id="table-migration-produkrencana"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `produkrencana` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_produk` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nama_produk` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `kode_valuta` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `jenis_akad` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `setoran_awal_minimum` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `minimal_setoran_rutin` | `numeric(38,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `jangka_waktu` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `grace_periode_gagal_debet` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `maksimal_gagal_debet` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `biaya_gagal_debet` | `numeric(38,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `biaya_penutupan_gagal_debet` | `numeric(38,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `is_dapat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `nisbah_bonus_dasar` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `is_override_bagihasilkhusus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `jarak_periode_bagihasil` | `numeric(38,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `periode_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `disposisi_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `is_override_disposisi_bgh` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `is_kena_zakat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `presentase_zakat_bagi_hasil` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `is_override_zakatbagihasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `is_kena_pajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `tarif_pajak` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `is_override_tarifpajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `is_kena_biayalayananumum` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `biaya_adm_bulanan` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `sumber_biaya_adm` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `is_blokir_debet` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `is_blokir_kredit` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `biaya_penutupan_rekening` | `numeric(18,2)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 32 | `is_override_biaya_penutupan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `is_tidak_dormant` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `jumlah_hari_jadi_tidak_aktif` | `numeric(38,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `tanggal_acuan_dormant` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `is_tutup_otomatis_dormant` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 37 | `jumlah_hari_tutup_otomatis` | `numeric(38,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 38 | `is_biaya_rekening_dormant` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 39 | `biaya_rekening_dormant` | `numeric(20,8)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 40 | `gl_saldo` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 41 | `gl_biaya_bgh` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 42 | `gl_pendapatan_lay` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 43 | `gl_pajak` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 44 | `gl_zakat` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 45 | `gl_cadangan_bgh` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 46 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 47 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.produktabungan` <a id="table-migration-produktabungan"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `produktabungan` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_produk` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nama_produk` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `kode_valuta` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `jenis_akad` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `setoran_awal_minimum` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `saldo_minimum` | `numeric(38,16)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `is_dapat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `nisbah_bonus_dasar` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `is_override_bagihasilkhusus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `jarak_periode_bagihasil` | `numeric(38,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `periode_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `disposisi_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `is_override_disposisi_bgh` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `is_kena_zakat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `presentase_zakat_bagi_hasil` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `is_override_zakatbagihasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `is_kena_pajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `tarif_pajak` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `is_override_tarifpajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `is_kena_biayalayananumum` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `biaya_adm_bulanan` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `sumber_biaya_adm` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `is_blokir_debet` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `is_blokir_kredit` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `biaya_penutupan_rekening` | `numeric(18,2)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 27 | `is_override_biaya_penutupan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `is_biaya_saldo_minimum` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `biaya_saldo_minimum` | `numeric(20,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `is_tidak_dormant` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `jumlah_hari_jadi_tidak_aktif` | `numeric(38,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `tanggal_acuan_dormant` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `is_tutup_otomatis_dormant` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `jumlah_hari_tutup_otomatis` | `numeric(38,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `is_biaya_rekening_dormant` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 36 | `biaya_rekening_dormant` | `numeric(20,8)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 37 | `gl_saldo` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 38 | `gl_biaya_bgh` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 39 | `gl_pendapatan_lay` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 40 | `gl_pajak` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 41 | `gl_zakat` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 42 | `gl_cadangan_bgh` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 43 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 44 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.repair_journalblock_bck` <a id="table-migration-repair-journalblock-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `repair_journalblock_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `system_id` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `class_id` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `key_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `id_journalblock` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `dataid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `journal_no` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `subsystemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transaction_tag` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.repair_journalitemupload_bck` <a id="table-migration-repair-journalitemupload-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `repair_journalitemupload_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journalitem_no` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `amount_debit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `amount_credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `branch_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `valuta_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `rc_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `generic_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `fl_posting_account` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `fl_project_no` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `journalitemstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `userid_check` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `dateposting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `datelastmod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `datecreate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `journalitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `kode_kurs` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `nilai_kurs` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `rpv_main` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `subsystemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `subaccountcode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `subaccountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `id_journalblock` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `transaksirak_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `source_class_id` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `source_key_id` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `additionaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.repair_journalupload_bck` <a id="table-migration-repair-journalupload-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `repair_journalupload_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journal_date_posting` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `userid_create` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `userid_last_modified` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `journal_date_last_modified` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `userid_posting` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `is_posted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `journal_type` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `lastitemno` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `is_partlychecked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `transaction_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `journal_state` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `serial_no` | `character varying(23)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `event_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `lock_userid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `fl_origin_journal` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `source_app` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `source_app_class` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `source_app_ref` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `fl_accountingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.repair_transaction_bck` <a id="table-migration-repair-transaction-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `repair_transaction_bck` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `transactiondate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `referenceno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `inputer` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `transactioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `authuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `transactiontime` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `authdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `authstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `batchid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `isposted` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `authaction` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `journalblockid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `channelcode` | `character varying` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `sponsorid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 19 | `volunteerid` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `actualdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `paidto` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `donorno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 24 | `donorname` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 25 | `amount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `currencycode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `receivedfrom` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `channelaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 30 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `journalno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `hcbatchitemid` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `authoperationmode` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `updatedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `journalerrordescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `flag_omit_journal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.script_collection` <a id="table-migration-script-collection"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `script_collection` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `script_code` | `character varying(15)` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |
| 2 | `script_name` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `script_description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `script_path` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (script_code)` |  |

### Table `migration.templatemigration` <a id="table-migration-templatemigration"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `templatemigration` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `tplcode` | `character varying(30)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `tplname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `tpldesc` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `tplfilename` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `modulecode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `tpltablename` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `tplmigrationscript` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `is_nonstandard_template` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `is_hidden_standard_upload` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_accountofficer` <a id="table-migration-tmp-accountofficer"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_accountofficer` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_ao` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nama_ao` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_bankcash` <a id="table-migration-tmp-bankcash"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_bankcash` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountno` | `character varying(30)` | NO |  | PK | YES | partial | synthetic_only | NO | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `currencycode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `cashcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `isamilaccount` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `productcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `bankaccountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 12 | `bankcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `isreconaccount` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `baris` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `id_batch` | `integer` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountno, id_batch)` |  |

### Table `migration.tmp_coa` <a id="table-migration-tmp-coa"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_coa` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `issystem` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `iscpaaccount` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_denominasi_khasanah` <a id="table-migration-tmp-denominasi-khasanah"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_denominasi_khasanah` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nilai_denominasi` | `numeric(36,10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `jenis_denominasi` | `character varying(1)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `jumlah_denominasi` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_deposito` <a id="table-migration-tmp-deposito"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_deposito` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nama_rekening` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `nomor_bilyet` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `kode_cabang` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `kode_valuta` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `keterangan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `nomor_nasabah` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 8 | `status_rekening` | `numeric(22,0)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 9 | `kode_produk` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `saldo` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `saldo_penempatan` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `tanggal_buka` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `tanggal_tutup` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `tanggal_jatuh_tempo_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `tanggal_jatuh_tempo_berikutnya` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `tanggal_aktifitas_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `kode_ao` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `status_confidential` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `kode_confidential` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `status_kelengkapan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `is_blokir` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `keterangan_blokir` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `blokir_oleh` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `sistem_pemblokir` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `is_dapat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 26 | `is_bagi_hasil_khusus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `nisbah_dasar` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `spesial_nisbah` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `aro_nisbah` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `disposisi_nominal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `rekening_disposisi_nominal` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 32 | `bank_transfer_nominal` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `penerima_transfer_nominal` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `disposisi_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `rekening_disposisi_baghas` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 36 | `bank_transfer_baghas` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 37 | `penerima_transfer_baghas` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 38 | `is_kena_zakat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 39 | `persentase_zakat_bagi_hasil` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 40 | `is_kena_pajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 41 | `tarif_pajak` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 42 | `kode_pajak` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 43 | `tanggal_baghas_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 44 | `tanggal_baghas_berikutnya` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 45 | `is_kena_biayalayananumum` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 46 | `is_kena_bea_materai` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 47 | `jenis_penduduk` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 48 | `kode_sumber_dana` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 49 | `kode_tujuan_pembukaan` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 50 | `alamat_kirim` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 51 | `user_input` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 52 | `user_otorisasi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 53 | `total_bagihasil` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 54 | `total_pajak` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 55 | `total_zakat` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 56 | `cadangan_baghas_kapitalisir` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 57 | `ekuivalen_rate` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 58 | `is_sudah_cetak_bilyet` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 59 | `is_sudah_disetor` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 60 | `masa_perjanjian` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 61 | `saldo_accrual_bagihasil` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 62 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 63 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 64 | `infotransfer_norekening` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 65 | `infotransfer_keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 66 | `infotransfer_bank` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 67 | `user_blokir` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_donorinactivated` <a id="table-migration-tmp-donorinactivated"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_donorinactivated` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | NO | needs_review |
| 2 | `donorname` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `lasttrxdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `id_batch` | `integer` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_batch, donorid)` |  |

### Table `migration.tmp_glinterface` <a id="table-migration-tmp-glinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_glinterface` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `id_batch` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `kode_tx_class` | `character varying(6)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `acc_type` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `kode_produk` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `kode_gl` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_histtransaksi_candidate` <a id="table-migration-tmp-histtransaksi-candidate"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_histtransaksi_candidate` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_transaksi` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `id_detil_transaksi` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `nomor_rekening` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 4 | `tanggal_transaksi` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `tanggal_input` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `nilai_mutasi` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `jenis_mutasi` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `keterangan` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `kode_transaksi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `nomor_referensi` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `user_input` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `user_otorisasi` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `kode_cabang_transaksi` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `jam_input` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_histtransaksi_tabgir` <a id="table-migration-tmp-histtransaksi-tabgir"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_histtransaksi_tabgir` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(30)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nomor_urut` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `nama_rekening` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 4 | `tanggal_transaksi` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `kode_transaksi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `jenis_mutasi` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `nilai_mutasi` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `keterangan` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_histtransaksi_tabgir_bus` <a id="table-migration-tmp-histtransaksi-tabgir-bus"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_histtransaksi_tabgir_bus` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(30)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nomor_urut` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `nama_rekening` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 4 | `tanggal_transaksi` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `kode_transaksi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `nominal_kredit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `nominal_debet` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `keterangan` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_journal_candidate` <a id="table-migration-tmp-journal-candidate"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_journal_candidate` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_date` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journal_no` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |
| 3 | `description` | `character varying(400)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `id_batch` | `integer` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |
| 5 | `reference_no` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_batch, journal_no)` |  |

### Table `migration.tmp_journalitem_history` <a id="table-migration-tmp-journalitem-history"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_journalitem_history` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_date` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `journal_no` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `account_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `branch_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `currency_code` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `amount_debet` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `amount_credit` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `description` | `character varying(400)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `baris` | `integer` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |
| 10 | `id_batch` | `integer` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |
| 11 | `reference_no` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_batch, baris)` |  |

### Table `migration.tmp_kasteller` <a id="table-migration-tmp-kasteller"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_kasteller` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_user` | `character varying(30)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `kode_valuta` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `status_rekening` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 5 | `saldo` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_khasanah` <a id="table-migration-tmp-khasanah"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_khasanah` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_cabang` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `kode_valuta` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `saldo` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_list_rek_disposisi_baghas` <a id="table-migration-tmp-list-rek-disposisi-baghas"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_list_rek_disposisi_baghas` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nomor_nasabah` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `kode_produk` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `saldo` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_mappingcoa` <a id="table-migration-tmp-mappingcoa"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_mappingcoa` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code_lama` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `account_code_baru` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_mig_trans` <a id="table-migration-tmp-mig-trans"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_mig_trans` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nomor_rekening` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `id_transaksi` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_nasabahindividu` <a id="table-migration-tmp-nasabahindividu"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_nasabahindividu` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_nasabah` | `character varying(30)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nama_nasabah` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `nama_singkat` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 4 | `nama_lengkap_tanpa_gelar` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 5 | `nama_ibu_kandung` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 6 | `nama_gadis_ibu_kandung` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 7 | `gelar_depan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `gelar_belakang` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `tempat_lahir` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `tanggal_lahir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `tanggal_buka` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `alamat_email` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 13 | `alamat_rumah_jalan` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 14 | `alamat_rumah_rt` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 15 | `alamat_rumah_rw` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 16 | `alamat_rumah_kelurahan` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 17 | `alamat_rumah_kecamatan` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 18 | `alamat_rumah_kota_kabupaten` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 19 | `alamat_rumah_provinsi` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 20 | `alamat_rumah_kode_pos` | `character varying(5)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 21 | `alamat_surat_jalan` | `character varying(150)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 22 | `alamat_surat_rt` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 23 | `alamat_surat_rw` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 24 | `alamat_surat_kelurahan` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 25 | `alamat_surat_kecamatan` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 26 | `alamat_surat_kode_pos` | `character varying(5)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 27 | `alamat_surat_kota_kabupaten` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 28 | `alamat_surat_provinsi` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 29 | `telepon_rumah_kode_negara` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `telepon_rumah_kode_area` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `telepon_rumah_nomor` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `telepon_hp_kode_negara` | `character varying(5)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 33 | `telepon_hp_nomor` | `character varying(15)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 34 | `fax_kode_negara` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `fax_kode_area` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `fax_nomor` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 37 | `status_keterkaitan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 38 | `jenis_penduduk` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 39 | `jenis_identitas` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 40 | `nomor_identitas` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 41 | `tanggal_terbit_identitas` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 42 | `tanggal_berakhir_identitas` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 43 | `nomor_npwp_individu` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 44 | `nomor_kitas` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 45 | `tanggal_kadaluarsa_kitas` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 46 | `is_external` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 47 | `id_external` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 48 | `kode_lembaga_external` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 49 | `nama_grup` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 50 | `kewarganegaraan` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 51 | `pekerjaan` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 52 | `jabatan_pekerjaan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 53 | `badan_hukum_pekerjaan` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 54 | `bidang_usaha_pekerjaan` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 55 | `sektor_ekonomi` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 56 | `nama_perusahaan_kerja` | `character varying(32)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 57 | `alamat_kerja_jalan` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 58 | `alamat_kerja_rt` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 59 | `alamat_kerja_rw` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 60 | `alamat_kerja_kelurahan` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 61 | `alamat_kerja_kecamatan` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 62 | `alamat_kerja_kode_pos` | `character varying(5)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 63 | `alamat_kerja_kota_kabupaten` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 64 | `alamat_kerja_provinsi` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 65 | `pendidikan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 66 | `telepon_kerja_kode_negara` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 67 | `telepon_kerja_kode_area` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 68 | `telepon_kerja_nomor` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 69 | `fax_kerja_kode_negara` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 70 | `fax_kerja_kode_area` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 71 | `fax_kerja_nomor` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 72 | `jenis_kelamin` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 73 | `agama` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 74 | `bahasa` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 75 | `status_perkawinan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 76 | `golongan_debitur` | `character varying(6)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 77 | `sid_din` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 78 | `sid_id_debitur` | `character varying(43)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 79 | `limit_nom_setor_tunai` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 80 | `limit_nom_setor_nontunai` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 81 | `limit_nom_tarik_tunai` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 82 | `limit_nom_tarik_nontunai` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 83 | `limit_frek_setor_tunai` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 84 | `limit_frek_setor_nontunai` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 85 | `limit_frek_tarik_tunai` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 86 | `limit_frek_tarik_nontunai` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 87 | `status_tempat_tinggal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 88 | `tanggal_mulai_menempati` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 89 | `faktor_resiko` | `character varying(6)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 90 | `resiko_identitas_nasabah` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 91 | `resiko_lokasi_usaha` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 92 | `resiko_profil_nasabah` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 93 | `resiko_jumlah_transaksi` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 94 | `resiko_kegiatan_usaha` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 95 | `resiko_struktur_kepemilikan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 96 | `resiko_info_lainnya` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 97 | `tujuan_buka_rekening` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 98 | `tujuan_penggunaan_dana` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 99 | `sumber_dana` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 100 | `sumber_dana_lainnya` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 101 | `penghasilan_utama_per_tahun` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 102 | `kode_ao` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 103 | `nama_keluarga_dihubungi` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 104 | `telepon_keluarga_dihubungi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 105 | `dati_ii_domisili` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 106 | `keterangan` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 107 | `keterangan_tambahan` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 108 | `alamat_kantor_i` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 109 | `alamat_kantor_ii` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 110 | `cif_lama` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 111 | `telp_kantor_i` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 112 | `telp_kantor_ii` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 113 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 114 | `hobi` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 115 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 116 | `tahun_menempati_rumah` | `numeric(10,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 117 | `bulan_menempati_rumah` | `numeric(10,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 118 | `jumlah_tanggungan_istri` | `numeric(10,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 119 | `jumlah_tanggungan_anak` | `numeric(10,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 120 | `jumlah_tanggungan_orangtua` | `numeric(10,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 121 | `pemberi_referensi` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 122 | `wilayah_referensi` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 123 | `user_input` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 124 | `user_otorisasi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 125 | `tanggal_ubah` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 126 | `jam_ubah` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 127 | `st_nasabah_induk` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 128 | `telepon_rumah_kode_area2` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 129 | `telepon_rumah_nomor2` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 130 | `telepon_kerja_kode_area2` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 131 | `telepon_kerja_nomor2` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 132 | `telepon_kerja_ext` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 133 | `telepon_kerja_ext2` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 134 | `user_update` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 135 | `tanggal_update` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 136 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 137 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 138 | `negara_asal` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_neracasaldo` <a id="table-migration-tmp-neracasaldo"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_neracasaldo` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `branch_code` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_neracasaldo_mapcoa` <a id="table-migration-tmp-neracasaldo-mapcoa"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_neracasaldo_mapcoa` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code_lama` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `branch_code` | `character varying(10)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_neracasaldo_nonmapping` <a id="table-migration-tmp-neracasaldo-nonmapping"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_neracasaldo_nonmapping` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |
| 2 | `branch_code` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |
| 3 | `balance` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `journal_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `baris` | `integer` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `id_batch` | `integer` | NO |  | PK | NO | none | reference_allowed | NO | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (account_code, branch_code, id_batch)` |  |

### Table `migration.tmp_rekeningliabilitas_update` <a id="table-migration-tmp-rekeningliabilitas-update"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_rekeningliabilitas_update` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `kode_marketing_pertama` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `kode_marketing_referensi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `kode_marketing_current` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_rekeningperantara` <a id="table-migration-tmp-rekeningperantara"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_rekeningperantara` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nama_rekening` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `kode_produk` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `kode_valuta` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `saldo` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_repair_saldo` <a id="table-migration-tmp-repair-saldo"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_repair_saldo` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `saldo_seharusnya` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `saldo_migrasi` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_saldo_awal_rekening` <a id="table-migration-tmp-saldo-awal-rekening"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_saldo_awal_rekening` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(30)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `saldo_awal` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_tabgir` <a id="table-migration-tmp-tabgir"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_tabgir` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nama_rekening` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `kode_cabang` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `kode_valuta` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `keterangan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `nomor_nasabah` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 7 | `jenis_rekening` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 8 | `join_account` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `nomor_nasabah_joinaccount` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 10 | `status_rekening` | `numeric` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 11 | `kode_produk` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `saldo` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `tanggal_buka` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `tanggal_aktifitas_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `kode_ao` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `status_confidential` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `kode_confidential` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `status_kelengkapan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `flag_blokir_debet_internal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `flag_blokir_kredit_internal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `flag_blokir_debet_eksternal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `flag_blokir_kredit_eksternal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `flag_dormant` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `flag_biaya_saldo_minimum` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `flag_biaya_rekening_tidakaktif` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 26 | `flag_biaya_atm` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `flag_cetak_nota` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `flag_cetak_passbook` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `is_blokir` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `keterangan_blokir` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `blokir_oleh` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `sistem_pemblokir` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `is_dapat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `is_bagi_hasil_khusus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `nisbah_bagi_hasil` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `spesial_nisbah` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 37 | `is_kena_zakat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 38 | `persentase_zakat_bagi_hasil` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 39 | `is_kena_pajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 40 | `tarif_pajak` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 41 | `is_kena_biayalayananumum` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 42 | `is_kena_bea_materai` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 43 | `kode_sumber_dana` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 44 | `kode_tujuan_pembukaan` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 45 | `alamat_kirim` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 46 | `kolektibilitas` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 47 | `bagi_hasil_terakhir` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 48 | `bagi_hasil_sebelumnya` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 49 | `tanggal_setor_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 50 | `tanggal_tarik_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 51 | `tanggal_tutup` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 52 | `user_input` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 53 | `user_otorisasi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 54 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 55 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_tabrencanarutin` <a id="table-migration-tmp-tabrencanarutin"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_tabrencanarutin` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nama_rekening` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `kode_cabang` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `kode_valuta` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `keterangan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `nomor_nasabah` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 7 | `jenis_rekening` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 8 | `join_account` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `nomor_nasabah_joinaccount` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 10 | `status_rekening` | `numeric` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 11 | `kode_produk` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `saldo` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 13 | `tanggal_buka` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 14 | `tanggal_aktifitas_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 15 | `kode_ao` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 16 | `status_confidential` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 17 | `kode_confidential` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 18 | `status_kelengkapan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 19 | `flag_blokir_debet_internal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 20 | `flag_blokir_kredit_internal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 21 | `flag_blokir_debet_eksternal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 22 | `flag_blokir_kredit_eksternal` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 23 | `flag_dormant` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 24 | `flag_biaya_saldo_minimum` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 25 | `flag_biaya_rekening_tidakaktif` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 26 | `flag_biaya_atm` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 27 | `flag_cetak_nota` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 28 | `flag_cetak_passbook` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 29 | `is_blokir` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 30 | `keterangan_blokir` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 31 | `blokir_oleh` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 32 | `sistem_pemblokir` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 33 | `is_dapat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 34 | `is_bagi_hasil_khusus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 35 | `nisbah_bagi_hasil` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 36 | `spesial_nisbah` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 37 | `is_kena_zakat_bagi_hasil` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 38 | `persentase_zakat_bagi_hasil` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 39 | `is_kena_pajak` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 40 | `tarif_pajak` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 41 | `is_kena_biayalayananumum` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 42 | `is_kena_bea_materai` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 43 | `kode_sumber_dana` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 44 | `kode_tujuan_pembukaan` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 45 | `alamat_kirim` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 46 | `kolektibilitas` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 47 | `bagi_hasil_terakhir` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 48 | `bagi_hasil_sebelumnya` | `numeric(22,8)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 49 | `tanggal_setor_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 50 | `tanggal_tarik_terakhir` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 51 | `tanggal_tutup` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 52 | `setoran_rutin` | `numeric(36,10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 53 | `jangka_waktu` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 54 | `tanggal_setoran_rutin` | `numeric(22,0)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 55 | `tanggal_jatuh_tempo` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 56 | `nomor_rekening_induk` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 57 | `user_input` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 58 | `user_otorisasi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 59 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 60 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_tranjournal_candidate` <a id="table-migration-tmp-tranjournal-candidate"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_tranjournal_candidate` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_transaksi` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `id_batch` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_update_nama_rekening` <a id="table-migration-tmp-update-nama-rekening"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_update_nama_rekening` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_rekening` | `character varying(20)` | NO |  |  | YES | partial | synthetic_only | NO | needs_review |
| 2 | `nama` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `alamat` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 4 | `id_individu` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `nomor_nasabah` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |

### Table `migration.tmp_userapp` <a id="table-migration-tmp-userapp"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_userapp` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_karyawan` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nama_lengkap` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `id_user` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `kode_departemen` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `role` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `baris` | `numeric` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.tmp_usertraining` <a id="table-migration-tmp-usertraining"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `tmp_usertraining` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor_karyawan` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `nama_lengkap` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 3 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `kode_departemen` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 5 | `role` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |

### Table `migration.uploadbatch` <a id="table-migration-uploadbatch"></a>

| Field | Value |
| --- | --- |
| Schema | `migration` |
| Table | `uploadbatch` |
| Domain | `Temporary` |
| Table Type | `temporary` |
| Classification | `internal` |
| Source of Truth | NO |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_batch` | `numeric` | NO |  |  | NO | none | reference_allowed | NO | needs_review |
| 2 | `upload_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 3 | `tplcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 4 | `upload_file_name` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | NO | needs_review |
| 5 | `user_input` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 6 | `user_auth` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 7 | `upload_state` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 8 | `verify_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 9 | `push_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 10 | `user_verify` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 11 | `user_push` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
| 12 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | NO | needs_review |
