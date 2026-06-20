# Data Dictionary — Schema `personalia`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `personalia`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `seq_achievement` | `personalia` |  | needs_review | 11 | 11 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_attendance` | `personalia` |  | needs_review | 2163 | 2163 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_careerhistory` | `personalia` |  | needs_review | 86 | 86 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_depreciableasset` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_depreciationprocesslog` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_disposisi` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_dokumen` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_education` | `personalia` |  | needs_review | 183 | 183 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_employeeactivehistory` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_employeedevelopmentprogram` | `personalia` |  | needs_review | 9 | 9 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_externalcontact` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_externalorganization` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_family` | `personalia` |  | needs_review | 147 | 147 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_fixedassettype` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterfacecontainer` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_glinterfacemember` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_individu` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_inventory` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_inventorystock` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_inventoryunit` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_jenisdokumen` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_offwork` | `personalia` |  | needs_review | 18 | 18 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_organizationexperience` | `personalia` |  | needs_review | 77 | 77 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_performanceappraisal` | `personalia` |  | needs_review | 4 | 4 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_performanceitem` | `personalia` |  | needs_review | 109 | 109 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_rankhistory` | `personalia` |  | needs_review | 69 | 69 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_regionarea` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_regionrepresentation` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_reimbursementrealization` | `personalia` |  | needs_review | 162 | 162 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_salaryhistory` | `personalia` |  | needs_review | 11 | 11 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_salaryitemhistory` | `personalia` |  | needs_review | 107 | 107 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_salaryitemparameter` | `personalia` |  | needs_review | 19 | 19 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_salaryitemscheme` | `personalia` |  | needs_review | 160 | 160 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_salaryscheme` | `personalia` |  | needs_review | 11 | 11 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_targetachievement` | `personalia` |  | needs_review | 2 | 2 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_training` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transaction` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_transactionitem` | `personalia` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_workexperience` | `personalia` |  | needs_review | 108 | 108 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Tables

Daftar table:

- [`personalia.achievement`](#table-personalia-achievement) — 5 kolom
- [`personalia.assettransaction`](#table-personalia-assettransaction) — 3 kolom
- [`personalia.assettransactionitem`](#table-personalia-assettransactionitem) — 7 kolom
- [`personalia.attendance`](#table-personalia-attendance) — 23 kolom
- [`personalia.attendancesymbols`](#table-personalia-attendancesymbols) — 3 kolom
- [`personalia.blobregistration`](#table-personalia-blobregistration) — 3 kolom
- [`personalia.branch`](#table-personalia-branch) — 5 kolom
- [`personalia.branchlocation`](#table-personalia-branchlocation) — 6 kolom
- [`personalia.careerhistory`](#table-personalia-careerhistory) — 5 kolom
- [`personalia.contracthistory`](#table-personalia-contracthistory) — 5 kolom
- [`personalia.custom_idgen`](#table-personalia-custom-idgen) — 4 kolom
- [`personalia.depreciableasset`](#table-personalia-depreciableasset) — 11 kolom
- [`personalia.depreciationprocesslog`](#table-personalia-depreciationprocesslog) — 4 kolom
- [`personalia.disposisi`](#table-personalia-disposisi) — 9 kolom
- [`personalia.dokumen`](#table-personalia-dokumen) — 13 kolom
- [`personalia.dokumenkeluar`](#table-personalia-dokumenkeluar) — 8 kolom
- [`personalia.dokumenmasuk`](#table-personalia-dokumenmasuk) — 7 kolom
- [`personalia.education`](#table-personalia-education) — 5 kolom
- [`personalia.employee`](#table-personalia-employee) — 19 kolom
- [`personalia.employeeactivehistory`](#table-personalia-employeeactivehistory) — 5 kolom
- [`personalia.employeedevelopmentprogram`](#table-personalia-employeedevelopmentprogram) — 8 kolom
- [`personalia.employeetraining`](#table-personalia-employeetraining) — 7 kolom
- [`personalia.enum_int`](#table-personalia-enum-int) — 3 kolom
- [`personalia.enum_varchar`](#table-personalia-enum-varchar) — 3 kolom
- [`personalia.externalcontact`](#table-personalia-externalcontact) — 5 kolom
- [`personalia.externalorganization`](#table-personalia-externalorganization) — 7 kolom
- [`personalia.family`](#table-personalia-family) — 9 kolom
- [`personalia.fixedasset`](#table-personalia-fixedasset) — 20 kolom
- [`personalia.fixedassettype`](#table-personalia-fixedassettype) — 9 kolom
- [`personalia.formaleducation`](#table-personalia-formaleducation) — 2 kolom
- [`personalia.glinterfacecontainer`](#table-personalia-glinterfacecontainer) — 3 kolom
- [`personalia.glinterfacemember`](#table-personalia-glinterfacemember) — 6 kolom
- [`personalia.healthplafond`](#table-personalia-healthplafond) — 8 kolom
- [`personalia.healthreimbursement`](#table-personalia-healthreimbursement) — 5 kolom
- [`personalia.id_gen`](#table-personalia-id-gen) — 3 kolom
- [`personalia.individu`](#table-personalia-individu) — 32 kolom
- [`personalia.innormalinvtransactitem`](#table-personalia-innormalinvtransactitem) — 2 kolom
- [`personalia.inventory`](#table-personalia-inventory) — 5 kolom
- [`personalia.inventorystock`](#table-personalia-inventorystock) — 4 kolom
- [`personalia.inventorytransaction`](#table-personalia-inventorytransaction) — 4 kolom
- [`personalia.inventorytransactionitem`](#table-personalia-inventorytransactionitem) — 11 kolom
- [`personalia.inventoryunit`](#table-personalia-inventoryunit) — 4 kolom
- [`personalia.invreceivetransaction`](#table-personalia-invreceivetransaction) — 3 kolom
- [`personalia.islamorganization`](#table-personalia-islamorganization) — 1 kolom
- [`personalia.islamorgcontactperson`](#table-personalia-islamorgcontactperson) — 1 kolom
- [`personalia.jenisdokumen`](#table-personalia-jenisdokumen) — 3 kolom
- [`personalia.journalist`](#table-personalia-journalist) — 1 kolom
- [`personalia.logincorporate`](#table-personalia-logincorporate) — 2 kolom
- [`personalia.newsagency`](#table-personalia-newsagency) — 1 kolom
- [`personalia.nonformaleducation`](#table-personalia-nonformaleducation) — 2 kolom
- [`personalia.normalinventory`](#table-personalia-normalinventory) — 1 kolom
- [`personalia.normalinvreceive`](#table-personalia-normalinvreceive) — 1 kolom
- [`personalia.normalinvretur`](#table-personalia-normalinvretur) — 1 kolom
- [`personalia.normalinvtransactitem`](#table-personalia-normalinvtransactitem) — 4 kolom
- [`personalia.offwork`](#table-personalia-offwork) — 20 kolom
- [`personalia.offworkmaternity`](#table-personalia-offworkmaternity) — 4 kolom
- [`personalia.offworkpermit`](#table-personalia-offworkpermit) — 3 kolom
- [`personalia.offworkplafond`](#table-personalia-offworkplafond) — 12 kolom
- [`personalia.offworkregular`](#table-personalia-offworkregular) — 4 kolom
- [`personalia.organizationexperience`](#table-personalia-organizationexperience) — 6 kolom
- [`personalia.outnormalinvtransactitem`](#table-personalia-outnormalinvtransactitem) — 2 kolom
- [`personalia.parameterglobal`](#table-personalia-parameterglobal) — 9 kolom
- [`personalia.parameterjournal`](#table-personalia-parameterjournal) — 4 kolom
- [`personalia.parameterjournalitem`](#table-personalia-parameterjournalitem) — 10 kolom
- [`personalia.performanceappraisal`](#table-personalia-performanceappraisal) — 22 kolom
- [`personalia.performanceitem`](#table-personalia-performanceitem) — 8 kolom
- [`personalia.performanceparameter`](#table-personalia-performanceparameter) — 8 kolom
- [`personalia.performanceworkunitparameter`](#table-personalia-performanceworkunitparameter) — 3 kolom
- [`personalia.position`](#table-personalia-position) — 5 kolom
- [`personalia.rankhistory`](#table-personalia-rankhistory) — 4 kolom
- [`personalia.regionarea`](#table-personalia-regionarea) — 3 kolom
- [`personalia.regionrepresentation`](#table-personalia-regionrepresentation) — 3 kolom
- [`personalia.reimbursementrealization`](#table-personalia-reimbursementrealization) — 9 kolom
- [`personalia.salaryhistory`](#table-personalia-salaryhistory) — 10 kolom
- [`personalia.salaryitemhistory`](#table-personalia-salaryitemhistory) — 5 kolom
- [`personalia.salaryitemparameter`](#table-personalia-salaryitemparameter) — 9 kolom
- [`personalia.salaryitemparametergroup`](#table-personalia-salaryitemparametergroup) — 2 kolom
- [`personalia.salaryitemscheme`](#table-personalia-salaryitemscheme) — 8 kolom
- [`personalia.salaryscheme`](#table-personalia-salaryscheme) — 4 kolom
- [`personalia.sessionblob`](#table-personalia-sessionblob) — 4 kolom
- [`personalia.targetachievement`](#table-personalia-targetachievement) — 19 kolom
- [`personalia.training`](#table-personalia-training) — 5 kolom
- [`personalia.trainingseminar`](#table-personalia-trainingseminar) — 3 kolom
- [`personalia.transaction`](#table-personalia-transaction) — 14 kolom
- [`personalia.transactionitem`](#table-personalia-transactionitem) — 6 kolom
- [`personalia.workexperience`](#table-personalia-workexperience) — 6 kolom
- [`personalia.workunit`](#table-personalia-workunit) — 5 kolom
- [`personalia.workunitposition`](#table-personalia-workunitposition) — 3 kolom

### Table `personalia.achievement` <a id="table-personalia-achievement"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `achievement` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `achievementname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `achievementid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `institution` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `achievementdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (achievementid)` |  |

### Table `personalia.assettransaction` <a id="table-personalia-assettransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `assettransaction` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `assettranstype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `processid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionid)` |  |

### Table `personalia.assettransactionitem` <a id="table-personalia-assettransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `assettransactionitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `deprassetid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `assettransitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deprcostaccount` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `depraccount` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `deprperiode` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `deprsequence` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `personalia.attendance` <a id="table-personalia-attendance"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `attendance` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `attendanceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `attendancedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `attendancestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `arrivalstatus` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `returntime` | `time(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `overtime1` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `overtime2` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `overtime3` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `overtime4` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `totalovertime` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `arrivaluserinput` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `arrivalterminalinput` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `returnuserinput` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `returnterminalinput` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `arriveovertime` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `returnovertime` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `arrivetime` | `time(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `overtime5` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `attendancesymbol` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `statusenum` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `arriveovertimeminute` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (attendanceid)` |  |

### Table `personalia.attendancesymbols` <a id="table-personalia-attendancesymbols"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `attendancesymbols` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `attendancesymbol` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `symboldescription` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `attendancestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (attendancesymbol)` |  |

### Table `personalia.blobregistration` <a id="table-personalia-blobregistration"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `blobregistration` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `actualfilename` | `character varying(128)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `istemporary` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `personalia.branch` <a id="table-personalia-branch"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `branch` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branchcode` | `character varying(3)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `shortcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (branchcode)` |  |

### Table `personalia.branchlocation` <a id="table-personalia-branchlocation"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `branchlocation` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branch_code` | `character varying(5)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `last_update` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `masterbranch_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (branch_code)` |  |

### Table `personalia.careerhistory` <a id="table-personalia-careerhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `careerhistory` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `careerhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workunitid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `positionid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `effectivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (careerhistoryid)` |  |

### Table `personalia.contracthistory` <a id="table-personalia-contracthistory"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `contracthistory` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `contractno` | `character varying(100)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `initialcontractperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `endcontractperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (contractno)` |  |

### Table `personalia.custom_idgen` <a id="table-personalia-custom-idgen"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `custom_idgen` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idname` | `character varying(30)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idcode` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `locked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idname, idcode)` |  |

### Table `personalia.depreciableasset` <a id="table-personalia-depreciableasset"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `depreciableasset` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `deprassetid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `deprassetregnumber` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `registerdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inputdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputuser` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `deprassettype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `deprassetname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `depreciationsequence` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `deprassetstate` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `depreciationaccumvalue` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `personalia.depreciationprocesslog` <a id="table-personalia-depreciationprocesslog"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `depreciationprocesslog` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `processid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `processdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `userid` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `processtime` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (processid)` |  |

### Table `personalia.disposisi` <a id="table-personalia-disposisi"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `disposisi` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `disposisiid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `dokumenid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `workunitid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `positionid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `namadisposisi` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `keterangandisposisi` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tanggal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `disposisioleh` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (disposisiid)` |  |

### Table `personalia.dokumen` <a id="table-personalia-dokumen"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `dokumen` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomor` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `perihal` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `tanggaldokumen` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `tipedokumen` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `filedokumen` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `dokumenid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 8 | `idjenisdokumen` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `userinput` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `userubah` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `tanggalinput` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `tanggalubah` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dokumenid)` |  |

### Table `personalia.dokumenkeluar` <a id="table-personalia-dokumenkeluar"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `dokumenkeluar` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `tujuan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `tanggalkirim` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `statuskirim` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `pic` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `jenisdokkeluar` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `dokumenid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 7 | `konseptor` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `workunitid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dokumenid)` |  |

### Table `personalia.dokumenmasuk` <a id="table-personalia-dokumenmasuk"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `dokumenmasuk` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pengirim` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `tanggalterima` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `diteruskanke` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `jenisdokmasuk` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `dokumenid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 6 | `ditujukanke` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nomoreksternaldokumen` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (dokumenid)` |  |

### Table `personalia.education` <a id="table-personalia-education"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `education` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `educationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `eduyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `eduinstitution` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `educationtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (educationid)` |  |

### Table `personalia.employee` <a id="table-personalia-employee"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `employee` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `supervisorid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `performanceappraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `targetachievementid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `workunitid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `positionid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `employeestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `employeeentrydate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `rank` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `salaryhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `careerhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `rankhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `edpid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `nonactivedescription` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `nonactivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `basicsalary` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `attendanceid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (employeeid)` |  |

### Table `personalia.employeeactivehistory` <a id="table-personalia-employeeactivehistory"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `employeeactivehistory` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `historyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `activestatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `changedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (historyid)` |  |

### Table `personalia.employeedevelopmentprogram` <a id="table-personalia-employeedevelopmentprogram"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `employeedevelopmentprogram` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `edpid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `edpfile` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `edplegalfile` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `evaluatoremployee` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `periodyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `edpdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (edpid)` |  |

### Table `personalia.employeetraining` <a id="table-personalia-employeetraining"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `employeetraining` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `trainingid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `trainingdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `trainingvalue` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `certificate` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `traininglocation` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `trainingdateend` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (trainingid)` |  |

### Table `personalia.enum_int` <a id="table-personalia-enum-int"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `enum_int` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `personalia.enum_varchar` <a id="table-personalia-enum-varchar"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `enum_varchar` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `enum_name` | `character varying(32)` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `enum_value` | `character varying(2)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `enum_description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (enum_name, enum_value)` |  |

### Table `personalia.externalcontact` <a id="table-personalia-externalcontact"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `externalcontact` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `extcontactid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `extcontacttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `extorgid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `extorgcontacttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (extcontactid)` |  |

### Table `personalia.externalorganization` <a id="table-personalia-externalorganization"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `externalorganization` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `extorgid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `extorgcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `extorgname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `extorgdescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `extorgaddress` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `extorgcity` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `extorgtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (extorgid)` |  |

### Table `personalia.family` <a id="table-personalia-family"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `family` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `familyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `gender` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `familyname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `birthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `birthplace` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `relationships` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `education` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `worksector` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (familyid)` |  |

### Table `personalia.fixedasset` <a id="table-personalia-fixedasset"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `fixedasset` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `deprassetid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `isparent` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fatypeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `bookvalue` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `initvalue` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `depreciationvalue` | `numeric(30,4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `model` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `description` | `character varying` | YES | 300 |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `lastdeprdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `nextdeprdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `isinsured` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `insuranceduedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `stnkduedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `fixedassetcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `fundentity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `retiredate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `retirereason` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `retiredescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `fixedassetstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (deprassetid)` |  |

### Table `personalia.fixedassettype` <a id="table-personalia-fixedassettype"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `fixedassettype` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fatypeid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `fatypecode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fatypedescription` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `fatypename` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `parenttypeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `isdepreciable` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `fatypedepreciationtime` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (fatypeid)` |  |

### Table `personalia.formaleducation` <a id="table-personalia-formaleducation"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `formaleducation` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `educationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `educationname` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (educationid)` |  |

### Table `personalia.glinterfacecontainer` <a id="table-personalia-glinterfacecontainer"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `glinterfacecontainer` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glicontainerid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `glicontainercode` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `glicontainername` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (glicontainerid)` |  |

### Table `personalia.glinterfacemember` <a id="table-personalia-glinterfacemember"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `glinterfacemember` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `glimemberid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `accountname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `glimembercode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `glicontainerid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (glimemberid)` |  |

### Table `personalia.healthplafond` <a id="table-personalia-healthplafond"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `healthplafond` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `empid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `outpatientplafond` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inpatientplafond` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `totalplafond` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `realization` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `finalbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `currentyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (employeeid)` |  |

### Table `personalia.healthreimbursement` <a id="table-personalia-healthreimbursement"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `healthreimbursement` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rank` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `reimbursementtype` | `character varying(2)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `maritalstatus` | `character varying(2)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `reimbursementvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rank, reimbursementtype, maritalstatus)` |  |

### Table `personalia.id_gen` <a id="table-personalia-id-gen"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `id_gen` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_code` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `locked` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_code)` |  |

### Table `personalia.individu` <a id="table-personalia-individu"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `individu` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `individuid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `addresscity` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `addresskecamatan` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `addresskelurahan` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `addresspostalcode` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `addressstate` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `addressstreet` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `addresssubdistrict` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `individuno` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `individutype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `individustatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `birthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `birthplace` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 16 | `gender` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `formaleducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `marital` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `religion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `identitytype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `identitynumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `phonenumber` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 23 | `initialname` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `mobilenumberpersonal` | `character varying(40)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 25 | `mobilenumbercorporate` | `character varying(40)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 26 | `emailpersonal` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 27 | `emailcorporate` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 28 | `photo1` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `photo2` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `photo3` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `dependent` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `accountno` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (individuid)` |  |

### Table `personalia.innormalinvtransactitem` <a id="table-personalia-innormalinvtransactitem"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `innormalinvtransactitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `inormalinvtitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `personalia.inventory` <a id="table-personalia-inventory"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `inventory` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `invid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `invcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `invname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `invtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `invunitid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (invid)` |  |

### Table `personalia.inventorystock` <a id="table-personalia-inventorystock"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `inventorystock` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `invstockid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `qty` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `invid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (invstockid)` |  |

### Table `personalia.inventorytransaction` <a id="table-personalia-inventorytransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `inventorytransaction` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `invtranstype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ponumber` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `receiveby` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionid)` |  |

### Table `personalia.inventorytransactionitem` <a id="table-personalia-inventorytransactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `inventorytransactionitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `qty` | `numeric(10,2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `invtransitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `invid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `normalinvtitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `innormalinvtitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `outnormalinvtitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `invintransitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `invouttransitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `invstockid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `qtybefore` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `personalia.inventoryunit` <a id="table-personalia-inventoryunit"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `inventoryunit` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `invunitid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `invunitcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `invunitname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (invunitid)` |  |

### Table `personalia.invreceivetransaction` <a id="table-personalia-invreceivetransaction"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `invreceivetransaction` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `ponumber` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `receiveby` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionid)` |  |

### Table `personalia.islamorganization` <a id="table-personalia-islamorganization"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `islamorganization` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `extorgid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (extorgid)` |  |

### Table `personalia.islamorgcontactperson` <a id="table-personalia-islamorgcontactperson"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `islamorgcontactperson` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `extcontactid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (extcontactid)` |  |

### Table `personalia.jenisdokumen` <a id="table-personalia-jenisdokumen"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `jenisdokumen` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idjenisdokumen` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `kodejenisdokumen` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `namajenisdokumen` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idjenisdokumen)` |  |

### Table `personalia.journalist` <a id="table-personalia-journalist"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `journalist` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `extcontactid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (extcontactid)` |  |

### Table `personalia.logincorporate` <a id="table-personalia-logincorporate"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `logincorporate` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `login` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (login)` |  |

### Table `personalia.newsagency` <a id="table-personalia-newsagency"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `newsagency` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `extorgid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (extorgid)` |  |

### Table `personalia.nonformaleducation` <a id="table-personalia-nonformaleducation"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `nonformaleducation` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `educationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `educationname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (educationid)` |  |

### Table `personalia.normalinventory` <a id="table-personalia-normalinventory"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `normalinventory` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `invid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (invid)` |  |

### Table `personalia.normalinvreceive` <a id="table-personalia-normalinvreceive"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `normalinvreceive` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `personalia.normalinvretur` <a id="table-personalia-normalinvretur"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `normalinvretur` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `personalia.normalinvtransactitem` <a id="table-personalia-normalinvtransactitem"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `normalinvtransactitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `normalinvtitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `innormalinvtitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `outnormalinvtitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `personalia.offwork` <a id="table-personalia-offwork"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `offwork` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `offworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `applicationdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `offworkbegin` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `offworkend` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `intervalday` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `applicationstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `offworkstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `userinput` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `dateinput` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `terminalinput` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `userapprover` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `dateapprover` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `terminalapprover` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `userproceed` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `dateproceed` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `terminalproceed` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `comebackworkdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `offworktype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `offworkaddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (offworkid)` |  |

### Table `personalia.offworkmaternity` <a id="table-personalia-offworkmaternity"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `offworkmaternity` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `offworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `maternitytype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `children` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `maternityestimatedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (offworkid)` |  |

### Table `personalia.offworkpermit` <a id="table-personalia-offworkpermit"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `offworkpermit` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `offworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `permitdescription` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (offworkid)` |  |

### Table `personalia.offworkplafond` <a id="table-personalia-offworkplafond"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `offworkplafond` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `previousyearplafond` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currentyearplafond` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `cutibesarbegin` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `currentyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `iscurrentallowancetaken` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ispreviousallowancetaken` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `empid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `iscutibesar` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `allowance` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `currentallowancedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `previousallowancedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (employeeid)` |  |

### Table `personalia.offworkregular` <a id="table-personalia-offworkregular"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `offworkregular` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `offworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `isallowancetaken` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `offworkyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `note` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (offworkid)` |  |

### Table `personalia.organizationexperience` <a id="table-personalia-organizationexperience"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `organizationexperience` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `organizationexperienceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `orgyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `orginstitution` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `orgposition` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `orgjobdesk` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (organizationexperienceid)` |  |

### Table `personalia.outnormalinvtransactitem` <a id="table-personalia-outnormalinvtransactitem"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `outnormalinvtransactitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `outnormalinvtitype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `personalia.parameterglobal` <a id="table-personalia-parameterglobal"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `parameterglobal` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_parameter` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_parameter` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_parameter_system` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nilai_parameter_string` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tag` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `default_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_parameter)` |  |

### Table `personalia.parameterjournal` <a id="table-personalia-parameterjournal"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `parameterjournal` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parameterjournalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `datasource` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `journalcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameterjournalid)` |  |

### Table `personalia.parameterjournalitem` <a id="table-personalia-parameterjournalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `parameterjournalitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parameterjournalitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchbase` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `basesign` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `currencybase` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `amountbase` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `ratebase` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `accountbase` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parameterjournalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameterjournalitemid)` |  |

### Table `personalia.performanceappraisal` <a id="table-personalia-performanceappraisal"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `performanceappraisal` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `performanceappraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `workunit` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `initialperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `endingperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `position` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `positioneffectivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `rank` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `rankeffectivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `lastsalary` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `appraisaldate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `totalvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `appraisalannotation` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `evaluatoremployee` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `inputuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `inputterminal` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `opinionannotation` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `generalvaluescale` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `employeeopinion` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `yearperiod` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `filelegalpa` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (performanceappraisalid)` |  |

### Table `personalia.performanceitem` <a id="table-personalia-performanceitem"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `performanceitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `performanceitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `value` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `subtotalvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `valueweightpercentage` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `performancevaluescale` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `parameterid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `performanceappraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (performanceitemid)` |  |

### Table `personalia.performanceparameter` <a id="table-personalia-performanceparameter"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `performanceparameter` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parameterid` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parametername` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `parentid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `isdetaillevel` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `weightpercentage` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameterid)` |  |

### Table `personalia.performanceworkunitparameter` <a id="table-personalia-performanceworkunitparameter"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `performanceworkunitparameter` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workunitid` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parameterid` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `weightpercentage` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workunitid, parameterid)` |  |

### Table `personalia.position` <a id="table-personalia-position"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `position` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `positionid` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `jobdescription` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nonactivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (positionid)` |  |

### Table `personalia.rankhistory` <a id="table-personalia-rankhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `rankhistory` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rankhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `rank` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `rankeffectivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rankhistoryid)` |  |

### Table `personalia.regionarea` <a id="table-personalia-regionarea"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `regionarea` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `regionareaid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `regionareacode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `regionareaname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (regionareaid)` |  |

### Table `personalia.regionrepresentation` <a id="table-personalia-regionrepresentation"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `regionrepresentation` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `regionrepresentionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `regionareaid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (regionrepresentionid)` |  |

### Table `personalia.reimbursementrealization` <a id="table-personalia-reimbursementrealization"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `reimbursementrealization` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `reimbursementrealizationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `reimbursementdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realizationvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nominal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `finalbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `beginbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isauthorized` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `islast` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (reimbursementrealizationid)` |  |

### Table `personalia.salaryhistory` <a id="table-personalia-salaryhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `salaryhistory` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `salaryreceiveddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workunit` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `position` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `salaryvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `salaryschemeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `monthperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `yearperiod` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryhistoryid)` |  |

### Table `personalia.salaryitemhistory` <a id="table-personalia-salaryitemhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `salaryitemhistory` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `salaryitemvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `salaryhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `salaryitemschemeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryitemid)` |  |

### Table `personalia.salaryitemparameter` <a id="table-personalia-salaryitemparameter"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `salaryitemparameter` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryitemparameterid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parametername` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `itemvaluedefault` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `formuladefault` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `salaryitemperiod` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `salaryitemtypedefault` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `parametergroupid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryitemparameterid)` |  |

### Table `personalia.salaryitemparametergroup` <a id="table-personalia-salaryitemparametergroup"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `salaryitemparametergroup` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parametergroupid` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parametergroupid)` |  |

### Table `personalia.salaryitemscheme` <a id="table-personalia-salaryitemscheme"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `salaryitemscheme` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryitemschemeid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `salaryitemschemename` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `itemvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `formula` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `salaryitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `salaryschemeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryitemschemeid)` |  |

### Table `personalia.salaryscheme` <a id="table-personalia-salaryscheme"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `salaryscheme` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryschemeid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `salaryschemename` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `positionid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryschemeid)` |  |

### Table `personalia.sessionblob` <a id="table-personalia-sessionblob"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `sessionblob` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sessionid` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `sessioncontext` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `id1` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `personalia.targetachievement` <a id="table-personalia-targetachievement"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `targetachievement` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `targetachievementid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `evaluatoremployee` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inputterminal` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `targetfile` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `achievementfile` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `targetdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `lastsalary` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `periodyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `workunit` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `positionid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `positioneffectivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `rank` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `rankeffectivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `achievementlegalfile` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `targetlegalfile` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `achievementdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (targetachievementid)` |  |

### Table `personalia.training` <a id="table-personalia-training"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `training` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `trainingid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `materi` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `institution` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `trainingtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (trainingid)` |  |

### Table `personalia.trainingseminar` <a id="table-personalia-trainingseminar"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `trainingseminar` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `trainingid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `status` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `year` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (trainingid)` |  |

### Table `personalia.transaction` <a id="table-personalia-transaction"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `transaction` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactiondate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `inputdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `editdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputuser` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `edituser` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `transactiontype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `transactionno` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `referencenumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `core_transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `authuser` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `authdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionid)` |  |

### Table `personalia.transactionitem` <a id="table-personalia-transactionitem"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `transactionitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `transactionitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `transactionitemtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchcode` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `transactionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `amount` | `numeric(30,8)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (transactionitemid)` |  |

### Table `personalia.workexperience` <a id="table-personalia-workexperience"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `workexperience` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workexperienceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `workinstitution` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `workposition` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `workjobdesk` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workexperienceid)` |  |

### Table `personalia.workunit` <a id="table-personalia-workunit"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `workunit` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workunitid` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nonactivedate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workunitid)` |  |

### Table `personalia.workunitposition` <a id="table-personalia-workunitposition"></a>

| Field | Value |
| --- | --- |
| Schema | `personalia` |
| Table | `workunitposition` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `confidential` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workunitid` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `positionid` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `jobdeskfile` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workunitid, positionid)` |  |
