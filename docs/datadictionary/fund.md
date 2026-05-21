# Data Dictionary — Schema `fund`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `fund`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `seq_200` | `fund` |  | needs_review | 109 | 109 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_accounthierarchy` | `fund` |  | needs_review | 1059 | 1059 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_accountinstance` | `fund` |  | needs_review | 43251 | 43251 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_assetcategory` | `fund` |  | needs_review | 13 | 13 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bankaccountlist` | `fund` |  | needs_review | 5537 | 5537 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_batchupload` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bsz` | `fund` |  | needs_review | 63 | 63 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bszdetail` | `fund` |  | needs_review | 435 | 435 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_bsztransaction` | `fund` |  | needs_review | 83 | 83 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budget` | `fund` |  | needs_review | 11747 | 11747 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetitem` | `fund` |  | needs_review | 1251 | 1251 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetitemhierarchy` | `fund` |  | needs_review | 2192 | 2192 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetowner` | `fund` |  | needs_review | 17 | 17 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetownerhierarchy` | `fund` |  | needs_review | 94 | 94 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetperiod` | `fund` |  | needs_review | 118 | 118 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgetrevision` | `fund` |  | needs_review | 6 | 6 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_budgettransaction` | `fund` |  | needs_review | 3 | 3 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_colltarget` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_colltargetperiod` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_dailybalance` | `fund` |  | needs_review | 1391 | 1391 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_dinarcertificate` | `fund` |  | needs_review | 4 | 4 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_distributiontransferinfo` | `fund` |  | needs_review | 10 | 10 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donor` | `fund` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donorcommitment` | `fund` |  | needs_review | 6 | 6 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donorcommitmenthistory` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donorfieldhistory` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donorlevel` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_donortotalfund` | `fund` |  | needs_review | 4012 | 4012 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_emailbody` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_externaldebtor` | `fund` |  | needs_review | 40 | 40 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_fieldofwork` | `fund` |  | needs_review | 12 | 12 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterface` | `fund` |  | needs_review | 5467 | 5467 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterfacecontainer` | `fund` |  | needs_review | 26 | 26 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterfacemember` | `fund` |  | needs_review | 165 | 165 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_inbox` | `fund` |  | needs_review | 12362 | 12362 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_inboxhistory` | `fund` |  | needs_review | 1887 | 1887 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_investee` | `fund` |  | needs_review | 14 | 14 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_investmentcategory` | `fund` |  | needs_review | 7 | 7 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_invoice` | `fund` |  | needs_review | 22 | 22 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_journalblock` | `fund` |  | needs_review | 312 | 312 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_kurshistory` | `fund` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mapreconcile` | `fund` |  | needs_review | 52 | 52 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mapreconcileaccount` | `fund` |  | needs_review | 107 | 107 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_marketer` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_marketertarget` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mustahiq` | `fund` |  | needs_review | 15 | 15 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_parameterjournal` | `fund` |  | needs_review | 65 | 65 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_parameterjournalitem` | `fund` |  | needs_review | 205 | 205 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_product` | `fund` |  | needs_review | 139 | 139 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_producthierarchy` | `fund` |  | needs_review | 116 | 116 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_projectsponsor` | `fund` |  | needs_review | 27 | 27 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_projectsponsordisbursement` | `fund` |  | needs_review | 11 | 11 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_propinsi` | `fund` |  | needs_review | 37 | 37 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_reconcileaccountbalance` | `fund` |  | needs_review | 7290 | 7290 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_registerkurs` | `fund` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_senderemail` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_smslog` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_sponsor` | `fund` |  | needs_review | 68 | 68 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transaction` | `fund` |  | needs_review | 237516 | 237516 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transactionbatch` | `fund` |  | needs_review | 1128 | 1128 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transactionitem` | `fund` |  | needs_review | 483734 | 483734 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transrecongenlog` | `fund` |  | needs_review | 218745 | 218745 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_wakafcertificate` | `fund` |  | needs_review | 51 | 51 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_workarea` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_workbusinessarea` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_workposition` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_workunit` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_zakahobject` | `fund` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Tables

Daftar table:

- [`fund.bankaccountlist`](#table-fund-bankaccountlist) — 6 kolom
- [`fund.batchuploadphone`](#table-fund-batchuploadphone) — 2 kolom
- [`fund.batchuploadphoneitem`](#table-fund-batchuploadphoneitem) — 5 kolom
- [`fund.bsz`](#table-fund-bsz) — 6 kolom
- [`fund.bszdetail`](#table-fund-bszdetail) — 7 kolom
- [`fund.bsztransaction`](#table-fund-bsztransaction) — 3 kolom
- [`fund.colltarget`](#table-fund-colltarget) — 5 kolom
- [`fund.colltargetperiod`](#table-fund-colltargetperiod) — 4 kolom
- [`fund.corporatedonor`](#table-fund-corporatedonor) — 14 kolom
- [`fund.custom_idgen`](#table-fund-custom-idgen) — 4 kolom
- [`fund.donor`](#table-fund-donor) — 29 kolom
- [`fund.donorbankaccount`](#table-fund-donorbankaccount) — 2 kolom
- [`fund.donorcommitment`](#table-fund-donorcommitment) — 4 kolom
- [`fund.donorcommitmenthistory`](#table-fund-donorcommitmenthistory) — 6 kolom
- [`fund.donorfieldhistory`](#table-fund-donorfieldhistory) — 10 kolom
- [`fund.donorlevel`](#table-fund-donorlevel) — 3 kolom
- [`fund.donortotalfund`](#table-fund-donortotalfund) — 4 kolom
- [`fund.emailbody`](#table-fund-emailbody) — 9 kolom
- [`fund.enum_int`](#table-fund-enum-int) — 3 kolom
- [`fund.enum_varchar`](#table-fund-enum-varchar) — 3 kolom
- [`fund.fieldofwork`](#table-fund-fieldofwork) — 4 kolom
- [`fund.id_gen`](#table-fund-id-gen) — 3 kolom
- [`fund.individualdonor`](#table-fund-individualdonor) — 39 kolom
- [`fund.marketer`](#table-fund-marketer) — 15 kolom
- [`fund.marketertarget`](#table-fund-marketertarget) — 5 kolom
- [`fund.negara`](#table-fund-negara) — 2 kolom
- [`fund.parameter`](#table-fund-parameter) — 5 kolom
- [`fund.parameterglobal`](#table-fund-parameterglobal) — 9 kolom
- [`fund.propinsi`](#table-fund-propinsi) — 4 kolom
- [`fund.senderemail`](#table-fund-senderemail) — 11 kolom
- [`fund.smslog`](#table-fund-smslog) — 15 kolom
- [`fund.smslogdeleted`](#table-fund-smslogdeleted) — 14 kolom
- [`fund.tmp_area`](#table-fund-tmp-area) — 3 kolom
- [`fund.tmp_donor_deleted`](#table-fund-tmp-donor-deleted) — 3 kolom
- [`fund.workarea`](#table-fund-workarea) — 3 kolom
- [`fund.workbusinessarea`](#table-fund-workbusinessarea) — 3 kolom
- [`fund.workposition`](#table-fund-workposition) — 3 kolom
- [`fund.workunit`](#table-fund-workunit) — 3 kolom
- [`fund.zakahobject`](#table-fund-zakahobject) — 3 kolom

### Table `fund.bankaccountlist` <a id="table-fund-bankaccountlist"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `bankaccountlist` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankaccountid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bankaccountname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bankaccountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `bankaccountlisttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `bankcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isdefault` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankaccountid)` |  |

### Table `fund.batchuploadphone` <a id="table-fund-batchuploadphone"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `batchuploadphone` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_batch` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `batch_date` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_batch)` |  |

### Table `fund.batchuploadphoneitem` <a id="table-fund-batchuploadphoneitem"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `batchuploadphoneitem` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_batch` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `workidentitynumber` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `employeename` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mobilephonenew` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `mobilephoneold` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_batch, workidentitynumber)` |  |

### Table `fund.bsz` <a id="table-fund-bsz"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `bsz` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bszid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bsznumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `bszdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `bszperiodbegin` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `bszperiodend` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bszid)` |  |

### Table `fund.bszdetail` <a id="table-fund-bszdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `bszdetail` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bszdetailid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `bszid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `item` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `percentage` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `year` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `basicvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `zakahvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bszdetailid)` |  |

### Table `fund.bsztransaction` <a id="table-fund-bsztransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `bsztransaction` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bszid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionitemid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `bsztransactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bsztransactionid)` |  |

### Table `fund.colltarget` <a id="table-fund-colltarget"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `colltarget` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `targetid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `periodid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `targetamount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (targetid)` |  |

### Table `fund.colltargetperiod` <a id="table-fund-colltargetperiod"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `colltargetperiod` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `periodid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `periodvalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `periode_code` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `periodamount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (periodid)` |  |

### Table `fund.corporatedonor` <a id="table-fund-corporatedonor"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `corporatedonor` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `corporation` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `siupp` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `tdp` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `locationtype` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `ownertype` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `establisheddate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `establishedplace` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `contactperson` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `patronagecompany` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 11 | `cpname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `cpemail` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `cpphonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `cpmobilenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `fund.custom_idgen` <a id="table-fund-custom-idgen"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `custom_idgen` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
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

### Table `fund.donor` <a id="table-fund-donor"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `donor` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorname` | `character varying(200)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `addresskelurahan` | `character varying(100)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `addresssubdistrict` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `addresscity` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `addresspostalcode` | `character varying(10)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `phonenumber` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `fax` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `referenceby` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `donortype` | `character varying(1)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `addressstreet` | `character varying(200)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `addressstate` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `npwp` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `npwz` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `donorno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 16 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 17 | `joindate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `addresskecamatan` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 22 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `economicsector` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `donorlevelid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 25 | `donorgroup` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 26 | `input_user` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `input_date` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `nonactivedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `nonactiveuser` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `fund.donorbankaccount` <a id="table-fund-donorbankaccount"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `donorbankaccount` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bankaccountid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bankaccountid)` |  |

### Table `fund.donorcommitment` <a id="table-fund-donorcommitment"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `donorcommitment` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `commitmentid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `commitmentamount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (commitmentid)` |  |

### Table `fund.donorcommitmenthistory` <a id="table-fund-donorcommitmenthistory"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `donorcommitmenthistory` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `historyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `commitmentamount` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `dateinput` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `userinput` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (historyid)` |  |

### Table `fund.donorfieldhistory` <a id="table-fund-donorfieldhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `donorfieldhistory` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `historyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `fieldname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fieldvalueint` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `fieldvaluechar` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `fieldvaluetimestamp` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `dateinput` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fielddescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `fieldvaluedouble` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `userinput` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (historyid)` |  |

### Table `fund.donorlevel` <a id="table-fund-donorlevel"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `donorlevel` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorlevelid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `donorlevelcode` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `donorleveldescription` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorlevelid)` |  |

### Table `fund.donortotalfund` <a id="table-fund-donortotalfund"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `donortotalfund` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `totalfundid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `totalamount` | `numeric(38,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (totalfundid)` |  |

### Table `fund.emailbody` <a id="table-fund-emailbody"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `emailbody` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `emailbodyid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `jenisbody` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `subject` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `body` | `character varying(2000)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `userinput` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `userubah` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tanggalinput` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `tanggalubah` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (emailbodyid)` |  |

### Table `fund.enum_int` <a id="table-fund-enum-int"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `enum_int` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
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

### Table `fund.enum_varchar` <a id="table-fund-enum-varchar"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `enum_varchar` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO | NULL::character varying | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `character varying(3)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `fund.fieldofwork` <a id="table-fund-fieldofwork"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `fieldofwork` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fworkcode` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fworkname` | `character varying(60)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fnpwzcode` | `character varying(3)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fworkid)` |  |

### Table `fund.id_gen` <a id="table-fund-id-gen"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `id_gen` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
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

### Table `fund.individualdonor` <a id="table-fund-individualdonor"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `individualdonor` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `gender` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `birthplace` | `character varying(150)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `birthdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `identitytype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `religion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `identitynumber` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `language` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `lastformaleducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `incomepermonth` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `expensepermonth` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `maritalstate` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `officeaddress` | `character varying(200)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `officekelurahan` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `officesubdistrict` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `officecity` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `officestate` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `officepostalcode` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `officephonenumber` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 19 | `email` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 20 | `donorid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 21 | `mobilephone` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 22 | `idpropinsioffice` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `officekecamatan` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `corporatename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `jobposition` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `couplename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `fworkid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `child` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `isinternalemployee` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `workareaid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `workunitid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `workidentitynumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `statusrumah` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `workpositionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `workbusinessareaid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `workbusinessarea` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 37 | `workunit` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 38 | `workposition` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 39 | `workareaidinitial` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (donorid)` |  |

### Table `fund.marketer` <a id="table-fund-marketer"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `marketer` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `marketername` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `marketertype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `marketercode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `marketerid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 5 | `marketeraddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `marketermobilephone` | `character varying(14)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `cpname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `supervisiorid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `cpphonenumber` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 11 | `jenismarketer` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `joindate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `statusedit` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (marketerid)` |  |

### Table `fund.marketertarget` <a id="table-fund-marketertarget"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `marketertarget` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `targetid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `realizationamount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `year` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `targetamount` | `numeric(30,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `marketerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (targetid)` |  |

### Table `fund.negara` <a id="table-fund-negara"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `negara` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idnegara` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_negara` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idnegara)` |  |

### Table `fund.parameter` <a id="table-fund-parameter"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `parameter` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
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

### Table `fund.parameterglobal` <a id="table-fund-parameterglobal"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `parameterglobal` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(25)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_parameter` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_parameter` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_parameter_system` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nilai_parameter_string` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tag` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `default_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_parameter)` |  |

### Table `fund.propinsi` <a id="table-fund-propinsi"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `propinsi` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idpropinsi` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `propinsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kodepropinsi` | `character varying(3)` | YES | NULL::character varying | UK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idpropinsi)` |  |
| `kode_unik` | UNIQUE | `UNIQUE (kodepropinsi)` |  |

### Table `fund.senderemail` <a id="table-fund-senderemail"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `senderemail` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idsenderemail` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `username` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `password` | `character varying(20)` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 4 | `host` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `port` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `emailaddress` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `userinput` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `useredit` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `dateinput` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `dateedit` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idsenderemail)` |  |

### Table `fund.smslog` <a id="table-fund-smslog"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `smslog` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `log_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `phonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `outbox_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `message` | `character varying(300)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `messagetype` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `iscanceled` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `log_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `log_time` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `creatorid` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `userid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `reply_inboxid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `extmessageid` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `extmsgstatuscode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `extmsgstatusdesc` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (log_id)` |  |

### Table `fund.smslogdeleted` <a id="table-fund-smslogdeleted"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `smslogdeleted` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `log_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `phonenumber` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `outbox_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `message` | `character varying(300)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `messagetype` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `iscanceled` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `log_date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `log_time` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `creatorid` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `userid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `reply_inboxid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `deleted_datetime` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `deleted_userid` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (log_id)` |  |

### Table `fund.tmp_area` <a id="table-fund-tmp-area"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `tmp_area` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workidentitynumber` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `areaname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workareaid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `fund.tmp_donor_deleted` <a id="table-fund-tmp-donor-deleted"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `tmp_donor_deleted` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `donorid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `donorname` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `workidentitynumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `fund.workarea` <a id="table-fund-workarea"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `workarea` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workareaid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `workareacode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workareaname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workareaid)` |  |

### Table `fund.workbusinessarea` <a id="table-fund-workbusinessarea"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `workbusinessarea` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workbusinessareaid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `workbusinessareacode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workbusinessareaname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workbusinessareaid)` |  |

### Table `fund.workposition` <a id="table-fund-workposition"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `workposition` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workpositionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `workpositioncode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workpositionname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workpositionid)` |  |

### Table `fund.workunit` <a id="table-fund-workunit"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `workunit` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workunitid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `workunitcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workunitname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workunitid)` |  |

### Table `fund.zakahobject` <a id="table-fund-zakahobject"></a>

| Field | Value |
| --- | --- |
| Schema | `fund` |
| Table | `zakahobject` |
| Domain | `Funding` |
| Table Type | `transaction` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `zakahobjectid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `zakahobjectcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `zakahobjectname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (zakahobjectid)` |  |
