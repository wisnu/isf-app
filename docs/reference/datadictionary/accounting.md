# Data Dictionary — Schema `accounting`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `accounting`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `seq_accounthierarchy` | `accounting` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_accountinstance` | `accounting` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_cashflowgroup` | `accounting` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_cashflowmember` | `accounting` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_custom_idgen` | `accounting` |  | needs_review | 45 | 45 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_dailybalance` | `accounting` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_fact_daily_balance` | `accounting` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_journalblock` | `accounting` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_journalcreation` | `accounting` |  | needs_review | 37 | 37 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_test` | `accounting` |  | needs_review | 103 | 103 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Views

| Nama | Schema | Catatan |
| --- | --- | --- |
| `account_off_bs` | `accounting` | needs_review (definisi view lihat DDL sumber) |
| `accountinstance_neraca` | `accounting` | needs_review (definisi view lihat DDL sumber) |
| `branchlocation` | `accounting` | needs_review (definisi view lihat DDL sumber) |
| `journalitem_neraca` | `accounting` | needs_review (definisi view lihat DDL sumber) |
| `journalitem_saldodana` | `accounting` | needs_review (definisi view lihat DDL sumber) |
| `userapp` | `accounting` | needs_review (definisi view lihat DDL sumber) |

## Tables

Daftar table:

- [`accounting.account`](#table-accounting-account) — 17 kolom
- [`accounting.accountdetail`](#table-accounting-accountdetail) — 2 kolom
- [`accounting.accountgroup`](#table-accounting-accountgroup) — 3 kolom
- [`accounting.accounthierarchy`](#table-accounting-accounthierarchy) — 3 kolom
- [`accounting.accountingday`](#table-accounting-accountingday) — 8 kolom
- [`accounting.accountingperiode`](#table-accounting-accountingperiode) — 9 kolom
- [`accounting.accountingyear`](#table-accounting-accountingyear) — 7 kolom
- [`accounting.accountinstance`](#table-accounting-accountinstance) — 19 kolom
- [`accounting.accountinterface`](#table-accounting-accountinterface) — 6 kolom
- [`accounting.accountinterfacemember`](#table-accounting-accountinterfacemember) — 3 kolom
- [`accounting.accountmanager`](#table-accounting-accountmanager) — 5 kolom
- [`accounting.accsubsystem`](#table-accounting-accsubsystem) — 13 kolom
- [`accounting.blobregistration`](#table-accounting-blobregistration) — 2 kolom
- [`accounting.branchlocation_old`](#table-accounting-branchlocation-old) — 7 kolom
- [`accounting.cashflowgroup`](#table-accounting-cashflowgroup) — 9 kolom
- [`accounting.cashflowmember`](#table-accounting-cashflowmember) — 9 kolom
- [`accounting.cpalpamapping`](#table-accounting-cpalpamapping) — 3 kolom
- [`accounting.currency`](#table-accounting-currency) — 30 kolom
- [`accounting.currency_pkpu`](#table-accounting-currency-pkpu) — 30 kolom
- [`accounting.custom_idgen`](#table-accounting-custom-idgen) — 4 kolom
- [`accounting.dailybalance`](#table-accounting-dailybalance) — 20 kolom
- [`accounting.dailyprojectbalance`](#table-accounting-dailyprojectbalance) — 21 kolom
- [`accounting.enum_int`](#table-accounting-enum-int) — 3 kolom
- [`accounting.enum_varchar`](#table-accounting-enum-varchar) — 3 kolom
- [`accounting.fact_daily_balance`](#table-accounting-fact-daily-balance) — 9 kolom
- [`accounting.hi_permil`](#table-accounting-hi-permil) — 8 kolom
- [`accounting.hipermildistribution`](#table-accounting-hipermildistribution) — 4 kolom
- [`accounting.id_gen`](#table-accounting-id-gen) — 3 kolom
- [`accounting.intrnewtransaction`](#table-accounting-intrnewtransaction) — 5 kolom
- [`accounting.intrpicktransaction`](#table-accounting-intrpicktransaction) — 3 kolom
- [`accounting.jenisrak`](#table-accounting-jenisrak) — 4 kolom
- [`accounting.journal`](#table-accounting-journal) — 28 kolom
- [`accounting.journalblock`](#table-accounting-journalblock) — 9 kolom
- [`accounting.journalcode`](#table-accounting-journalcode) — 8 kolom
- [`accounting.journaldeletion`](#table-accounting-journaldeletion) — 4 kolom
- [`accounting.journalitem`](#table-accounting-journalitem) — 36 kolom
- [`accounting.kurshistory`](#table-accounting-kurshistory) — 18 kolom
- [`accounting.mapaccount`](#table-accounting-mapaccount) — 2 kolom
- [`accounting.masterkurs`](#table-accounting-masterkurs) — 5 kolom
- [`accounting.parameter`](#table-accounting-parameter) — 5 kolom
- [`accounting.parameterglobaltes`](#table-accounting-parameterglobaltes) — 9 kolom
- [`accounting.periodebalance`](#table-accounting-periodebalance) — 18 kolom
- [`accounting.periodeprojectbalance`](#table-accounting-periodeprojectbalance) — 19 kolom
- [`accounting.project`](#table-accounting-project) — 8 kolom
- [`accounting.rakcabang`](#table-accounting-rakcabang) — 4 kolom
- [`accounting.rakpusat`](#table-accounting-rakpusat) — 3 kolom
- [`accounting.registerkurs`](#table-accounting-registerkurs) — 17 kolom
- [`accounting.revaluationhistory`](#table-accounting-revaluationhistory) — 6 kolom
- [`accounting.rpvaccount`](#table-accounting-rpvaccount) — 4 kolom
- [`accounting.rpvaccountdetail`](#table-accounting-rpvaccountdetail) — 6 kolom
- [`accounting.sim_logrun`](#table-accounting-sim-logrun) — 6 kolom
- [`accounting.snapshot_accountinstance`](#table-accounting-snapshot-accountinstance) — 21 kolom
- [`accounting.subsysteminteraction`](#table-accounting-subsysteminteraction) — 7 kolom
- [`accounting.tempcandidatejournal`](#table-accounting-tempcandidatejournal) — 11 kolom
- [`accounting.temptable`](#table-accounting-temptable) — 7 kolom
- [`accounting.temptable_RAK`](#table-accounting-temptable-rak) — 7 kolom
- [`accounting.temptable_ori`](#table-accounting-temptable-ori) — 7 kolom
- [`accounting.temptable_rpv`](#table-accounting-temptable-rpv) — 7 kolom
- [`accounting.temptabledata`](#table-accounting-temptabledata) — 7 kolom
- [`accounting.temptablenew`](#table-accounting-temptablenew) — 7 kolom
- [`accounting.transaksirak`](#table-accounting-transaksirak) — 12 kolom
- [`accounting.userapp_old`](#table-accounting-userapp-old) — 9 kolom
- [`accounting.usergroup`](#table-accounting-usergroup) — 5 kolom
- [`accounting.usergroupapp`](#table-accounting-usergroupapp) — 2 kolom
- [`accounting.vendor`](#table-accounting-vendor) — 5 kolom

### Table `accounting.account` <a id="table-accounting-account"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `account` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `account_code` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_name` | `character varying(100)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `account_level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `is_detail` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `account_type` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `is_system` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `userid_last_modified` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `time_last_modified` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fl_parent_account` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `userid_create` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `time_create` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `fl_cpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `fl_lpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `isactivaoffbalancesheet` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `isrpvrakreportshow` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `isrpvaccount` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (account_code)` |  |

### Table `accounting.accountdetail` <a id="table-accounting-accountdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountdetail` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_account` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fl_detail_account` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fl_account, fl_detail_account)` |  |

### Table `accounting.accountgroup` <a id="table-accounting-accountgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountgroup` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountgroup_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountgroup_name` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `accounting.accounthierarchy` <a id="table-accounting-accounthierarchy"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accounthierarchy` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accounthierarchy_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fl_parentaccountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_childaccountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accounthierarchy_id)` |  |

### Table `accounting.accountingday` <a id="table-accounting-accountingday"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountingday` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `periode_status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `islastperiod` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `periode_code` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 5 | `fl_accountingperiode` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 6 | `fl_accountingyear` | `character varying(4)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 7 | `datevalue` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isworkday` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periode_code, fl_accountingperiode, fl_accountingyear)` |  |

### Table `accounting.accountingperiode` <a id="table-accounting-accountingperiode"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountingperiode` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_accountingyear` | `character varying(4)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `periode_code` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `periode_status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_lastyearperiode` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `pcode_accday_end` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `pcode_accday_start` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fl_accountingperiode_start` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fl_accountingyear_start` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fl_accountingyear, periode_code)` |  |

### Table `accounting.accountingyear` <a id="table-accounting-accountingyear"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountingyear` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periode_code` | `character varying(4)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `periode_status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fl_current_periode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `pcode_accper_end` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `pcode_accper_start` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `fl_accountingyear_start` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periode_code)` |  |

### Table `accounting.accountinstance` <a id="table-accounting-accountinstance"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountinstance` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_cpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fl_lpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `isbolehinput` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `dailybalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periodebalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `dailyprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `periodeprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountinstance_id)` |  |

### Table `accounting.accountinterface` <a id="table-accounting-accountinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountinterface` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `interface_code` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `interface_type` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_active` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (interface_code)` |  |

### Table `accounting.accountinterfacemember` <a id="table-accounting-accountinterfacemember"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountinterfacemember` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `member_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `interface_code` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (member_id)` |  |

### Table `accounting.accountmanager` <a id="table-accounting-accountmanager"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accountmanager` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `amcode` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `rcno` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `employeename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (amcode)` |  |

### Table `accounting.accsubsystem` <a id="table-accounting-accsubsystem"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `accsubsystem` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsystemcode` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `titlesubsystem` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `servername` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `username` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `password` | `character varying(30)` | YES | NULL::character varying |  | YES | full | synthetic_only | YES | needs_review |
| 7 | `createjournalscriptid` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `sessionname` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `usecurrentlogin` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `authjournalscriptid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `applicationid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `oldstylescripting` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsystemcode)` |  |

### Table `accounting.blobregistration` <a id="table-accounting-blobregistration"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `blobregistration` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `actualfilename` | `character varying(128)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `accounting.branchlocation_old` <a id="table-accounting-branchlocation-old"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `branchlocation_old` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branch_code` | `character varying(5)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchname` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchstatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `masterbranch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `dataid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (branch_code)` |  |

### Table `accounting.cashflowgroup` <a id="table-accounting-cashflowgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `cashflowgroup` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `cfgroupid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `cfgroupcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cfgroupname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `cfgroupdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `cfsequencenumber` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cfparentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `cfgrouplevel` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `cfoperationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (cfgroupid)` |  |

### Table `accounting.cashflowmember` <a id="table-accounting-cashflowmember"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `cashflowmember` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `cfmemberid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `cfgroupid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mutationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `trancodeexclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `trancodeinclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `journalcodeexclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `journalcodeinclude` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `additionalinfo` | `character varying(300)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (cfmemberid)` |  |

### Table `accounting.cpalpamapping` <a id="table-accounting-cpalpamapping"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `cpalpamapping` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_lpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `fl_cpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cpalpamapping_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (cpalpamapping_id)` |  |

### Table `accounting.currency` <a id="table-accounting-currency"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `currency` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `currency_code` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(64)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currentvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdefault` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isstandard` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `centralbank_currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `short_name` | `character varying(10)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `full_name` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `country_owner` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kurs_buku` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kurs_beli_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kurs_jual_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `kurs_beli_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `kurs_jual_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kurs_beli_kantor_pusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kurs_jual_kantor_pusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `tanggal_limit` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `terminal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `user_otorisasi` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `tanggal_otorisasi` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `terminal_otorisasi` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `kurs_neraca` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `deviasi_maksimal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `kurs_reval` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `kurs_remittance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `symbol` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `symbol_says` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (currency_code)` |  |

### Table `accounting.currency_pkpu` <a id="table-accounting-currency-pkpu"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `currency_pkpu` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `currency_code` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(64)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currentvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdefault` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isstandard` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `centralbank_currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `short_name` | `character varying(10)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `full_name` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `country_owner` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kurs_buku` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kurs_beli_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kurs_jual_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `kurs_beli_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `kurs_jual_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kurs_beli_kantor_pusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kurs_jual_kantor_pusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `tanggal_limit` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `terminal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `user_otorisasi` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `tanggal_otorisasi` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `terminal_otorisasi` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `kurs_neraca` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `deviasi_maksimal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `kurs_reval` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `kurs_remittance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `symbol` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `symbol_says` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (currency_code)` |  |

### Table `accounting.custom_idgen` <a id="table-accounting-custom-idgen"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `custom_idgen` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idname` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idcode` | `character varying(50)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `locked` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idname, idcode)` |  |

### Table `accounting.dailybalance` <a id="table-accounting-dailybalance"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `dailybalance` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailybalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `datevalue` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `debit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `credit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dailybalance_id)` |  |

### Table `accounting.dailyprojectbalance` <a id="table-accounting-dailyprojectbalance"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `dailyprojectbalance` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `dailyprojectbalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `datevalue` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `debit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `credit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dailyprojectbalance_id)` |  |

### Table `accounting.enum_int` <a id="table-accounting-enum-int"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `enum_int` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `accounting.enum_varchar` <a id="table-accounting-enum-varchar"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `enum_varchar` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `character varying(2)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `accounting.fact_daily_balance` <a id="table-accounting-fact-daily-balance"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `fact_daily_balance` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fact_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fact_date` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fact_date_fmt` | `character varying(8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `currency_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `balance_ekiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fact_id)` |  |

### Table `accounting.hi_permil` <a id="table-accounting-hi-permil"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `hi_permil` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `p_year` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `p_month` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currency_code` | `character varying(3)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `day_number` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `process_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `id_hipermil` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 8 | `ekuiv_rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_hipermil)` |  |

### Table `accounting.hipermildistribution` <a id="table-accounting-hipermildistribution"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `hipermildistribution` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `distribution_id` | `character varying(2)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `hipermil_ratio` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ekuiv_rate_ratio` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `id_hipermil` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (distribution_id, id_hipermil)` |  |

### Table `accounting.id_gen` <a id="table-accounting-id-gen"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `id_gen` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_code` | `character varying(50)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `locked` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_code)` |  |

### Table `accounting.intrnewtransaction` <a id="table-accounting-intrnewtransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `intrnewtransaction` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsysteminteraction_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `dialogid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `processingscriptid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `numbertag` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `servermethodid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsysteminteraction_id)` |  |

### Table `accounting.intrpicktransaction` <a id="table-accounting-intrpicktransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `intrpicktransaction` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsysteminteraction_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `dialogid` | `character varying(80)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `numbertag` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsysteminteraction_id)` |  |

### Table `accounting.jenisrak` <a id="table-accounting-jenisrak"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `jenisrak` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `koderak` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountcode_rakpusat` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `jenisrak` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (koderak)` |  |

### Table `accounting.journal` <a id="table-accounting-journal"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `journal` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `journal_date_posting` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `userid_create` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `userid_last_modified` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `journal_date_last_modified` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `userid_posting` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `is_posted` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `journal_type` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `journal_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastitemno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `is_partlychecked` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `transaction_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `journal_state` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `serial_no` | `character varying(23)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `event_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `lock_userid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `fl_origin_journal` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `source_app` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `source_app_class` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `source_app_ref` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `fl_accountingperiode` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journal_no)` |  |

### Table `accounting.journalblock` <a id="table-accounting-journalblock"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `journalblock` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `system_id` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `class_id` | `character varying(32)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `key_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `id_journalblock` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 5 | `dataid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `journal_no` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `subsystemcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transaction_tag` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_journalblock)` |  |

### Table `accounting.journalcode` <a id="table-accounting-journalcode"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `journalcode` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `terminal_input` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_ubah` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `terminal_ubah` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `tanggal_ubah` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `journalcode_id` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journalcode_id)` |  |

### Table `accounting.journaldeletion` <a id="table-accounting-journaldeletion"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `journaldeletion` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `journal_no` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `user_terminal` | `character varying(23)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `process_time` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (journal_no)` |  |

### Table `accounting.journalitem` <a id="table-accounting-journalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `journalitem` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_journal` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `journalitem_no` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_account` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `amount_debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `amount_credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `branch_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `valuta_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `rc_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `generic_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `fl_posting_account` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `fl_project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `docoprstatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `userid_create` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `userid_last_modified` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `journalitemstatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `userid_posting` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `userid_check` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `dateposting` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `datelastmod` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `datecreate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `event_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `journalitemtype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `kode_kurs` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `nilai_kurs` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `rpv_main` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `subsystemcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `subaccountcode` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `id_journalcreation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `subaccountname` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `id_journalblock` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `transaksirak_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `source_class_id` | `character varying(32)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `source_key_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `additionaldescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fl_journal, journalitem_no)` |  |

### Table `accounting.kurshistory` <a id="table-accounting-kurshistory"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `kurshistory` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kurshistory_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `kurs_beli_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `kurs_jual_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kurs_beli_kantorpusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `kurs_jual_kantorpusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `kurs_beli_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kurs_jual_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kurs_buku` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `kurs_neraca` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `history_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `user_ubah` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `user_otorisasi` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `terminal_pengubah` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `terminal_otorisasi` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kurs_reval` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kurs_remittance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kurshistory_id)` |  |

### Table `accounting.mapaccount` <a id="table-accounting-mapaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `mapaccount` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `oldaccount` | `character varying(255)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `newaccount` | `character varying(255)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `accounting.masterkurs` <a id="table-accounting-masterkurs"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `masterkurs` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_kurs` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_kurs` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nama_field_currency` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `rpv_name` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_kurs)` |  |

### Table `accounting.parameter` <a id="table-accounting-parameter"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `parameter` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parametercode` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parametervalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `parameterstringvalue` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `parameterdatevalue` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parametercode)` |  |

### Table `accounting.parameterglobaltes` <a id="table-accounting-parameterglobaltes"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `parameterglobaltes` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_parameter` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_parameter` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_parameter_system` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nilai_parameter_string` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tag` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `default_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `accounting.periodebalance` <a id="table-accounting-periodebalance"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `periodebalance` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periodebalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `debit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `credit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periodebalance_id)` |  |

### Table `accounting.periodeprojectbalance` <a id="table-accounting-periodeprojectbalance"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `periodeprojectbalance` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periodeprojectbalance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `debit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `credit_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `fl_accountingyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `periode_code` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periodeprojectbalance_id)` |  |

### Table `accounting.project` <a id="table-accounting-project"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `project` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `project_no` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `name` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(255)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `manager` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `start_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `end_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `dailyprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `periodeprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (project_no)` |  |

### Table `accounting.rakcabang` <a id="table-accounting-rakcabang"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `rakcabang` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rakcabang_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `koderak` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rakcabang_id)` |  |

### Table `accounting.rakpusat` <a id="table-accounting-rakpusat"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `rakpusat` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rakpusat_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `koderak` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rakpusat_id)` |  |

### Table `accounting.registerkurs` <a id="table-accounting-registerkurs"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `registerkurs` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `registerkurs_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_ubah` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `terminal_ubah` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `tanggal_ubah` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `kurs_beli_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `kurs_jual_banknote` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kurs_tengah_bi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kurs_beli_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `kurs_jual_transfer` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kurs_buku` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kurs_beli_kantorpusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kurs_jual_kantorpusat` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `kurs_neraca` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `kode_register` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `kurs_reval` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kurs_remittance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (registerkurs_id)` |  |

### Table `accounting.revaluationhistory` <a id="table-accounting-revaluationhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `revaluationhistory` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `history_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `revaluation_date` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `average_exchangerate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `revaluation_exchangerate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (history_id)` |  |

### Table `accounting.rpvaccount` <a id="table-accounting-rpvaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `rpvaccount` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rpv_name` | `character varying(20)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `rpv_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `profit_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `loss_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rpv_name)` |  |

### Table `accounting.rpvaccountdetail` <a id="table-accounting-rpvaccountdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `rpvaccountdetail` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_valas` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountinstance_primer` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `rpvaccountdetail_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `currency_code` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 5 | `rpv_name` | `character varying(20)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 6 | `branch_code` | `character varying(5)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (currency_code, rpv_name, branch_code)` |  |

### Table `accounting.sim_logrun` <a id="table-accounting-sim-logrun"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `sim_logrun` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `logrun_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sim_userid` | `character varying` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `sim_type` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `completion_time` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `status` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(255)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (logrun_id)` |  |

### Table `accounting.snapshot_accountinstance` <a id="table-accounting-snapshot-accountinstance"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `snapshot_accountinstance` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountinstance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fl_cpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fl_lpa_accountinstance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `balance_ratarata` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `balance_ratarata_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `trial_balance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `trial_balance_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `balance_harilalu` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `balance_harilalu_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `isbolehinput` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `branch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `account_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `currency_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `dailybalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `periodebalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `dailyprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `periodeprojectbalance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `balancecumulative_ekuiv` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `balancecumulative` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `accounting.subsysteminteraction` <a id="table-accounting-subsysteminteraction"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `subsysteminteraction` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsysteminteraction_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `titleinteraction` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentssi_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `interactiontype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `intrmodel` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `subsystemcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsysteminteraction_id)` |  |

### Table `accounting.tempcandidatejournal` <a id="table-accounting-tempcandidatejournal"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `tempcandidatejournal` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `tempcandidatejournal_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branch_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `group_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kode_kurs` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kode_mutasi` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `nilai_kurs` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `nilai_mutasi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (tempcandidatejournal_id)` |  |

### Table `accounting.temptable` <a id="table-accounting-temptable"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `temptable` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `accounting.temptable_RAK` <a id="table-accounting-temptable-rak"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `temptable_RAK` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `accounting.temptable_ori` <a id="table-accounting-temptable-ori"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `temptable_ori` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountcode)` |  |

### Table `accounting.temptable_rpv` <a id="table-accounting-temptable-rpv"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `temptable_rpv` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `accounting.temptabledata` <a id="table-accounting-temptabledata"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `temptabledata` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `accounting.temptablenew` <a id="table-accounting-temptablenew"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `temptablenew` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountcode` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accounttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountparent` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `cpaaccountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (accountcode)` |  |

### Table `accounting.transaksirak` <a id="table-accounting-transaksirak"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `transaksirak` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `debit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `credit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cabangasal` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `cabangtujuan` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `jenistransaksirak` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `transaksirak_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 7 | `keterangan` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `statusterprosespusat` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `transaksirakterkait_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `journal_no` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `koderak` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transaksirak_id)` |  |

### Table `accounting.userapp_old` <a id="table-accounting-userapp-old"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `userapp_old` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `user_id` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `username` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nolimitlocation` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `login_count` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mod_user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `user_id1` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (user_id)` |  |

### Table `accounting.usergroup` <a id="table-accounting-usergroup"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `usergroup` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `group_id` | `character varying(8)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `groupname` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (group_id)` |  |

### Table `accounting.usergroupapp` <a id="table-accounting-usergroupapp"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `usergroupapp` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `user_id` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `group_id` | `character varying(8)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (user_id, group_id)` |  |

### Table `accounting.vendor` <a id="table-accounting-vendor"></a>

| Field | Value |
| --- | --- |
| Schema | `accounting` |
| Table | `vendor` |
| Domain | `Accounting` |
| Table Type | `transaction` |
| Classification | `restricted` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `name` | `character varying(40)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `address` | `character varying(60)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `post_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `tlp_no` | `character varying(14)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `vendor_no` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (vendor_no)` |  |
