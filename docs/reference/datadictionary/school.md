# Data Dictionary — Schema `school`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `school`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `seq_transactionnumber` | `school` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Tables

Daftar table:

- [`school.academicvalue`](#table-school-academicvalue) — 7 kolom
- [`school.academicvalueitem`](#table-school-academicvalueitem) — 10 kolom
- [`school.academicvalueitemtemplate`](#table-school-academicvalueitemtemplate) — 11 kolom
- [`school.academicvaluetemplate`](#table-school-academicvaluetemplate) — 5 kolom
- [`school.achievement`](#table-school-achievement) — 5 kolom
- [`school.achievementactivities`](#table-school-achievementactivities) — 7 kolom
- [`school.activityappraisal`](#table-school-activityappraisal) — 11 kolom
- [`school.activityappraisalitem`](#table-school-activityappraisalitem) — 7 kolom
- [`school.activityappraisalitemtemplate`](#table-school-activityappraisalitemtemplate) — 14 kolom
- [`school.activityschool`](#table-school-activityschool) — 7 kolom
- [`school.agenda`](#table-school-agenda) — 4 kolom
- [`school.agendaitem`](#table-school-agendaitem) — 4 kolom
- [`school.agendaitemtemplate`](#table-school-agendaitemtemplate) — 5 kolom
- [`school.agendatemplate`](#table-school-agendatemplate) — 5 kolom
- [`school.appraisal`](#table-school-appraisal) — 13 kolom
- [`school.appraisalitem`](#table-school-appraisalitem) — 7 kolom
- [`school.appraisalitemgroup`](#table-school-appraisalitemgroup) — 2 kolom
- [`school.appraisalitemtemplate`](#table-school-appraisalitemtemplate) — 14 kolom
- [`school.appraisaltemplate`](#table-school-appraisaltemplate) — 4 kolom
- [`school.attendance`](#table-school-attendance) — 20 kolom
- [`school.careerhistory`](#table-school-careerhistory) — 5 kolom
- [`school.classhistory`](#table-school-classhistory) — 7 kolom
- [`school.club`](#table-school-club) — 5 kolom
- [`school.companion`](#table-school-companion) — 4 kolom
- [`school.companioncontract`](#table-school-companioncontract) — 14 kolom
- [`school.companionproduct`](#table-school-companionproduct) — 3 kolom
- [`school.companionvisit`](#table-school-companionvisit) — 9 kolom
- [`school.companionvisititem`](#table-school-companionvisititem) — 7 kolom
- [`school.companionvisititemtemplate`](#table-school-companionvisititemtemplate) — 12 kolom
- [`school.contracthistory`](#table-school-contracthistory) — 5 kolom
- [`school.custom_idgen`](#table-school-custom-idgen) — 4 kolom
- [`school.customer`](#table-school-customer) — 19 kolom
- [`school.customercorporate`](#table-school-customercorporate) — 7 kolom
- [`school.customerpersonal`](#table-school-customerpersonal) — 42 kolom
- [`school.education`](#table-school-education) — 8 kolom
- [`school.employee`](#table-school-employee) — 19 kolom
- [`school.employeedevelopmentprogram`](#table-school-employeedevelopmentprogram) — 9 kolom
- [`school.employeetraining`](#table-school-employeetraining) — 7 kolom
- [`school.enum_int`](#table-school-enum-int) — 3 kolom
- [`school.enum_varchar`](#table-school-enum-varchar) — 3 kolom
- [`school.equipment`](#table-school-equipment) — 6 kolom
- [`school.family`](#table-school-family) — 9 kolom
- [`school.formaleducation`](#table-school-formaleducation) — 4 kolom
- [`school.healthplafond`](#table-school-healthplafond) — 8 kolom
- [`school.healthreimbursement`](#table-school-healthreimbursement) — 5 kolom
- [`school.id_gen`](#table-school-id-gen) — 3 kolom
- [`school.individu`](#table-school-individu) — 34 kolom
- [`school.infrastructure`](#table-school-infrastructure) — 4 kolom
- [`school.logincorporate`](#table-school-logincorporate) — 2 kolom
- [`school.mustahiq`](#table-school-mustahiq) — 4 kolom
- [`school.mustahiqpersonal`](#table-school-mustahiqpersonal) — 1 kolom
- [`school.mustahiqproduct`](#table-school-mustahiqproduct) — 13 kolom
- [`school.negara`](#table-school-negara) — 2 kolom
- [`school.nonformaleducation`](#table-school-nonformaleducation) — 2 kolom
- [`school.officialreport`](#table-school-officialreport) — 6 kolom
- [`school.officialreportofdamage`](#table-school-officialreportofdamage) — 2 kolom
- [`school.officialreportofreplacement`](#table-school-officialreportofreplacement) — 2 kolom
- [`school.offwork`](#table-school-offwork) — 20 kolom
- [`school.offworkmaternity`](#table-school-offworkmaternity) — 4 kolom
- [`school.offworkpermit`](#table-school-offworkpermit) — 3 kolom
- [`school.offworkplafond`](#table-school-offworkplafond) — 12 kolom
- [`school.offworkregular`](#table-school-offworkregular) — 4 kolom
- [`school.organizationexperience`](#table-school-organizationexperience) — 6 kolom
- [`school.paemployee`](#table-school-paemployee) — 13 kolom
- [`school.parameterglobal`](#table-school-parameterglobal) — 9 kolom
- [`school.paschool`](#table-school-paschool) — 4 kolom
- [`school.performanceappraisal`](#table-school-performanceappraisal) — 11 kolom
- [`school.performanceitem`](#table-school-performanceitem) — 14 kolom
- [`school.performanceparameter`](#table-school-performanceparameter) — 9 kolom
- [`school.position`](#table-school-position) — 5 kolom
- [`school.pptemplate`](#table-school-pptemplate) — 5 kolom
- [`school.pptemplateitem`](#table-school-pptemplateitem) — 4 kolom
- [`school.product`](#table-school-product) — 24 kolom
- [`school.productgroup`](#table-school-productgroup) — 2 kolom
- [`school.program`](#table-school-program) — 3 kolom
- [`school.propinsi`](#table-school-propinsi) — 4 kolom
- [`school.rankhistory`](#table-school-rankhistory) — 4 kolom
- [`school.reimbursementrealization`](#table-school-reimbursementrealization) — 9 kolom
- [`school.salaryhistory`](#table-school-salaryhistory) — 10 kolom
- [`school.salaryitemhistory`](#table-school-salaryitemhistory) — 5 kolom
- [`school.salaryitemparameter`](#table-school-salaryitemparameter) — 9 kolom
- [`school.salaryitemparametergroup`](#table-school-salaryitemparametergroup) — 2 kolom
- [`school.salaryitemscheme`](#table-school-salaryitemscheme) — 8 kolom
- [`school.salaryscheme`](#table-school-salaryscheme) — 4 kolom
- [`school.schoolyear`](#table-school-schoolyear) — 2 kolom
- [`school.sessionblob`](#table-school-sessionblob) — 4 kolom
- [`school.sourcefound`](#table-school-sourcefound) — 3 kolom
- [`school.stockopname`](#table-school-stockopname) — 5 kolom
- [`school.stockopnameequipment`](#table-school-stockopnameequipment) — 6 kolom
- [`school.stockopnametools`](#table-school-stockopnametools) — 8 kolom
- [`school.student`](#table-school-student) — 9 kolom
- [`school.studentclass`](#table-school-studentclass) — 3 kolom
- [`school.studenthealth`](#table-school-studenthealth) — 7 kolom
- [`school.subject`](#table-school-subject) — 3 kolom
- [`school.targetachievement`](#table-school-targetachievement) — 20 kolom
- [`school.toollist`](#table-school-toollist) — 5 kolom
- [`school.tools`](#table-school-tools) — 10 kolom
- [`school.training`](#table-school-training) — 5 kolom
- [`school.trainingseminar`](#table-school-trainingseminar) — 3 kolom
- [`school.workexperience`](#table-school-workexperience) — 6 kolom
- [`school.workunit`](#table-school-workunit) — 5 kolom
- [`school.workunitposition`](#table-school-workunitposition) — 3 kolom

### Table `school.academicvalue` <a id="table-school-academicvalue"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `academicvalue` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `academicvalueid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `academicvaluetemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `date` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `yearschool` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `semester` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (academicvalueid)` |  |

### Table `school.academicvalueitem` <a id="table-school-academicvalueitem"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `academicvalueitem` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `academicvalueitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `academicvalueid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `academicvalueitemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `integervalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `floatvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `stringvalue` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `boolvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `valuedatatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `matpel` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kkm` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (academicvalueitemid)` |  |

### Table `school.academicvalueitemtemplate` <a id="table-school-academicvalueitemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `academicvalueitemtemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `academicvalueitemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `academicvaluetemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `subjectid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `integervaluestandard` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `floatvaluestandard` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `stringvaluestandard` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `boolvaluestandard` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `valuedatatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `matpel` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kkm` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (academicvalueitemtemplateid)` |  |

### Table `school.academicvaluetemplate` <a id="table-school-academicvaluetemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `academicvaluetemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `academicvaluetemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `templatename` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `semester` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `schoolyearcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (academicvaluetemplateid)` |  |

### Table `school.achievement` <a id="table-school-achievement"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `achievement` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `achievementname` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `achievementid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `institution` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `achievementdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (achievementid)` |  |

### Table `school.achievementactivities` <a id="table-school-achievementactivities"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `achievementactivities` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `achievementactivitiesid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `productid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `activityschoolid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `achievementname` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `institution` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `achievementdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (achievementactivitiesid)` |  |

### Table `school.activityappraisal` <a id="table-school-activityappraisal"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `activityappraisal` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `activityappraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `appraisaldate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `weekperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `monthperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `anualperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `appraisalyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `approvalstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `otherappraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `otherappraisalflag` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (activityappraisalid)` |  |

### Table `school.activityappraisalitem` <a id="table-school-activityappraisalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `activityappraisalitem` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `integervalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `floatvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `stringvalue` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `boolvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `activityappraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `itemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemid)` |  |

### Table `school.activityappraisalitemtemplate` <a id="table-school-activityappraisalitemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `activityappraisalitemtemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sequenceno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `integervaluestandard` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `floatvaluestandard` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `stringvaluestandard` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `boolvaluestandard` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `itemname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `groupname` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `valuedatatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `productgroupname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemtemplateid)` |  |

### Table `school.activityschool` <a id="table-school-activityschool"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `activityschool` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `activityschoolid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `activityname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `activitylocation` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `activitydate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `activitydescription` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `activitylevel` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `activitytype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (activityschoolid)` |  |

### Table `school.agenda` <a id="table-school-agenda"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `agenda` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `agendaid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendatemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (agendaid)` |  |

### Table `school.agendaitem` <a id="table-school-agendaitem"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `agendaitem` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `agendaid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendaitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `agendaitemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `attendance` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (agendaitemid)` |  |

### Table `school.agendaitemtemplate` <a id="table-school-agendaitemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `agendaitemtemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `agendaitemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendatemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `datevalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isevent` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `eventplanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (agendaitemtemplateid)` |  |

### Table `school.agendatemplate` <a id="table-school-agendatemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `agendatemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `agendatemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `agendaname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `monthvalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `quota` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `yearvalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (agendatemplateid)` |  |

### Table `school.appraisal` <a id="table-school-appraisal"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `appraisal` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `annualperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `appraisaldate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `appraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `appraisaltemplateid` | `integer` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 5 | `appraisalyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `approvalstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `monthperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `weekperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `appraisalsubject` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `subjectkeycount` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `subjectkey1` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `subjectkey2` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (appraisalid)` |  |

### Table `school.appraisalitem` <a id="table-school-appraisalitem"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `appraisalitem` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `appraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `boolvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `floatvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `integervalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `itemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 6 | `itemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `stringvalue` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemid)` |  |

### Table `school.appraisalitemgroup` <a id="table-school-appraisalitemgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `appraisalitemgroup` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `groupname` | `character varying(20)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (groupname)` |  |

### Table `school.appraisalitemtemplate` <a id="table-school-appraisalitemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `appraisalitemtemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `appraisaltemplateid` | `integer` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 2 | `boolvaluestandard` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `floatvaluestandard` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `integervaluestandard` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `islowlevel` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `itemname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `itemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 10 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `sequenceno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `valuedatatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `stringvaluestandard` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemtemplateid)` |  |

### Table `school.appraisaltemplate` <a id="table-school-appraisaltemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `appraisaltemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `appraisalname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `appraisaltemplateid` | `integer` | NO |  | PK | YES | full | synthetic_only | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `formula` | `character varying(285)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (appraisaltemplateid)` |  |

### Table `school.attendance` <a id="table-school-attendance"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `attendance` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `attendanceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `attendancedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `attendancestatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `arrivalstatus` | `character varying(2)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `returntime` | `time(6) without time zone` | YES | NULL::time without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `overtime1` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `overtime2` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `overtime3` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `overtime4` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `totalovertime` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `arrivaluserinput` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `arrivalterminalinput` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `returnuserinput` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `returnterminalinput` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `arriveovertime` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `returnovertime` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `arrivetime` | `time(6) without time zone` | YES | NULL::time without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `overtime5` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (attendanceid)` |  |

### Table `school.careerhistory` <a id="table-school-careerhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `careerhistory` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `careerhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workunitid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `positionid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `effectivedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (careerhistoryid)` |  |

### Table `school.classhistory` <a id="table-school-classhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `classhistory` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `classhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `studentclasscode` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `schoolyearcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `semester` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (classhistoryid)` |  |

### Table `school.club` <a id="table-school-club"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `club` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `clubid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `clubname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `clubstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `progress` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (clubid)` |  |

### Table `school.companion` <a id="table-school-companion"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `companion` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `companionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `companionextnumber` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (companionid)` |  |

### Table `school.companioncontract` <a id="table-school-companioncontract"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `companioncontract` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `contractno` | `character varying(100)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `initialcontractperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `endcontractperiod` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `documentfile` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `inputuser` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `inputdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `inputterminal` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `bmisupervisi` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `kabkota` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `companionexperience` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (contractno)` |  |

### Table `school.companionproduct` <a id="table-school-companionproduct"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `companionproduct` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `companionid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `contractno` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid, companionid)` |  |

### Table `school.companionvisit` <a id="table-school-companionvisit"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `companionvisit` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `companionvisitid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `visitingdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `visitingyear` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `weekperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `monthperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `annotation` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `approvalstatus` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (companionvisitid)` |  |

### Table `school.companionvisititem` <a id="table-school-companionvisititem"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `companionvisititem` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `itemtemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `companionvisitid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `integervalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `floatvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `stringvalue` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `boolvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemid)` |  |

### Table `school.companionvisititemtemplate` <a id="table-school-companionvisititemtemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `companionvisititemtemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `itemtemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sequenceno` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `itemname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `visitgroup` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `isactive` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `productgroupname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `valuedatatype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `answerchoice` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `parentitem` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `islowlevel` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (itemtemplateid)` |  |

### Table `school.contracthistory` <a id="table-school-contracthistory"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `contracthistory` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `contractno` | `character varying(100)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `initialcontractperiod` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `endcontractperiod` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (contractno)` |  |

### Table `school.custom_idgen` <a id="table-school-custom-idgen"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `custom_idgen` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `school.customer` <a id="table-school-customer"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `customer` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `customername` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `addresscity` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `addresskecamatan` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `addresskelurahan` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `addresspostalcode` | `character varying(10)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `addressstate` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `addressstreet` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `addresssubdistrict` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `branchcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `customerno` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 12 | `customerstatus` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `phonenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `customertype` | `character varying(2)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 17 | `fax` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `email` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 19 | `customernickname` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `school.customercorporate` <a id="table-school-customercorporate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `customercorporate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `cpname` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cpphonenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `cpmobilenumber` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `corporationnumber` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `corporationdate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `cctype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `school.customerpersonal` <a id="table-school-customerpersonal"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `customerpersonal` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `customerid` | `integer` | NO |  | PK | YES | partial | synthetic_only | YES | needs_review |
| 2 | `birthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `birthplace` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `identitytype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `identitynumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `formaleducation` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `gender` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `marital` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `religion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `totalfamily` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `worksector` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `customerpersonaltype` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 13 | `fathername` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `fatheroccupation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `fatherbirthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 16 | `fatherbirthplace` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 17 | `fathereducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `fatherphonenumber` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 19 | `mothername` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 20 | `motheroccupation` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 21 | `motherbirthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 22 | `motherbirthplace` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 23 | `mothereducation` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 24 | `motherphonenumber` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 25 | `guardianname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `guardianoccupation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `guardianbirthdate` | `timestamp(6) without time zone` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 28 | `guardianbirthplace` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 29 | `guardianeducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `guardianphonenumber` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 31 | `guardianaddress` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 32 | `educationcertificate` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `birthcertificate` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 34 | `familycard` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `photo` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `skhu` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 37 | `schoolorigin` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 38 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 39 | `sourcefoundid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 40 | `summemory` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 41 | `valueskhu` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 42 | `childerto` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (customerid)` |  |

### Table `school.education` <a id="table-school-education"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `education` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `educationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `eduyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `eduinstitution` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `educationtype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `description` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `alamat` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (educationid)` |  |

### Table `school.employee` <a id="table-school-employee"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `employee` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `supervisorid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `performanceappraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `targetachievementid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `workunitid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `positionid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `employeestatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `employeeentrydate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `rank` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `salaryhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `careerhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `rankhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `edpid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `nonactivedescription` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `nonactivedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `basicsalary` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (employeeid)` |  |

### Table `school.employeedevelopmentprogram` <a id="table-school-employeedevelopmentprogram"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `employeedevelopmentprogram` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `edpid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `edpfile` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `edplegalfile` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `evaluatoremployee` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `periodyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `edpdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `inputdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `schoolyearcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (edpid)` |  |

### Table `school.employeetraining` <a id="table-school-employeetraining"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `employeetraining` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `trainingid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `trainingdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `trainingvalue` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `certificate` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `traininglocation` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `trainingdateend` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (trainingid)` |  |

### Table `school.enum_int` <a id="table-school-enum-int"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `enum_int` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `school.enum_varchar` <a id="table-school-enum-varchar"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `enum_varchar` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `school.equipment` <a id="table-school-equipment"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `equipment` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `infrastructureid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `equipmentid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `equipmentname` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `quantity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `unit` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (equipmentid)` |  |

### Table `school.family` <a id="table-school-family"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `family` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `familyid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `gender` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `familyname` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `birthdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `birthplace` | `character varying(60)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `relationships` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `education` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `worksector` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (familyid)` |  |

### Table `school.formaleducation` <a id="table-school-formaleducation"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `formaleducation` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `educationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `educationname` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `fakultas` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `jurusan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (educationid)` |  |

### Table `school.healthplafond` <a id="table-school-healthplafond"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `healthplafond` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `empid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `outpatientplafond` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inpatientplafond` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `totalplafond` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `realization` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `finalbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `currentyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (employeeid)` |  |

### Table `school.healthreimbursement` <a id="table-school-healthreimbursement"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `healthreimbursement` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rank` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `reimbursementtype` | `character varying(2)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `maritalstatus` | `character varying(2)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `reimbursementvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rank, reimbursementtype, maritalstatus)` |  |

### Table `school.id_gen` <a id="table-school-id-gen"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `id_gen` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `school.individu` <a id="table-school-individu"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `individu` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `individuid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuname` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `addresscity` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `addresskecamatan` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `addresskelurahan` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `addresspostalcode` | `character varying(10)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `addressstate` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `addressstreet` | `character varying(200)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `addresssubdistrict` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `branchcode` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `individuno` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `individutype` | `character varying(2)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `individustatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `birthdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `birthplace` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 16 | `gender` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `formaleducation` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `marital` | `character varying(2)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `religion` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `identitytype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `identitynumber` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `phonenumber` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 23 | `initialname` | `character varying(3)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `mobilenumberpersonal` | `character varying(40)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 25 | `mobilenumbercorporate` | `character varying(40)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 26 | `emailpersonal` | `character varying(60)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 27 | `emailcorporate` | `character varying(60)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 28 | `photo1` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `photo2` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `photo3` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `dependent` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `accountno` | `character varying(20)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 33 | `idpropinsi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `alamattinggal` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (individuid)` |  |

### Table `school.infrastructure` <a id="table-school-infrastructure"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `infrastructure` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `infrastructureid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `infrastructurename` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (infrastructureid)` |  |

### Table `school.logincorporate` <a id="table-school-logincorporate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `logincorporate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `login` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (login)` |  |

### Table `school.mustahiq` <a id="table-school-mustahiq"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `mustahiq` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqtype` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `customerid` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqid)` |  |

### Table `school.mustahiqpersonal` <a id="table-school-mustahiqpersonal"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `mustahiqpersonal` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqid)` |  |

### Table `school.mustahiqproduct` <a id="table-school-mustahiqproduct"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `mustahiqproduct` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqextnumber` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `iseligible` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `noteligiblereason` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `mustahiqextfield` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `noteligibledate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `companionid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `noteligiblelegal` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `lastfundingperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `pendingfund` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `mustahiqtype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid, mustahiqid)` |  |

### Table `school.negara` <a id="table-school-negara"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `negara` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idnegara` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_negara` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idnegara)` |  |

### Table `school.nonformaleducation` <a id="table-school-nonformaleducation"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `nonformaleducation` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `educationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `educationname` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (educationid)` |  |

### Table `school.officialreport` <a id="table-school-officialreport"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `officialreport` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `officialreportid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `officialreporttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `officialreportdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (officialreportid)` |  |

### Table `school.officialreportofdamage` <a id="table-school-officialreportofdamage"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `officialreportofdamage` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `officialreportid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `damage` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (officialreportid)` |  |

### Table `school.officialreportofreplacement` <a id="table-school-officialreportofreplacement"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `officialreportofreplacement` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `officialreportid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `replacement` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (officialreportid)` |  |

### Table `school.offwork` <a id="table-school-offwork"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `offwork` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `offworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `applicationdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `offworkbegin` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `offworkend` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `intervalday` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `applicationstatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `offworkstatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `userinput` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `dateinput` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `terminalinput` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `userapprover` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `dateapprover` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `terminalapprover` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `userproceed` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `dateproceed` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `terminalproceed` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `comebackworkdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `offworktype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `offworkaddress` | `character varying(200)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (offworkid)` |  |

### Table `school.offworkmaternity` <a id="table-school-offworkmaternity"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `offworkmaternity` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `offworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `maternitytype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `children` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `maternityestimatedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (offworkid)` |  |

### Table `school.offworkpermit` <a id="table-school-offworkpermit"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `offworkpermit` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `offworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `permitdescription` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (offworkid)` |  |

### Table `school.offworkplafond` <a id="table-school-offworkplafond"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `offworkplafond` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `previousyearplafond` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `currentyearplafond` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `cutibesarbegin` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `currentyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `iscurrentallowancetaken` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `ispreviousallowancetaken` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `empid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `iscutibesar` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `allowance` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `currentallowancedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `previousallowancedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (employeeid)` |  |

### Table `school.offworkregular` <a id="table-school-offworkregular"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `offworkregular` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `offworkid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `isallowancetaken` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `offworkyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `note` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (offworkid)` |  |

### Table `school.organizationexperience` <a id="table-school-organizationexperience"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `organizationexperience` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `organizationexperienceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `orgyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `orginstitution` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `orgposition` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `orgjobdesk` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (organizationexperienceid)` |  |

### Table `school.paemployee` <a id="table-school-paemployee"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `paemployee` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `performanceappraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `workunit` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `position` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `employeeid` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `positioneffectivedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `rankeffectivedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `rank` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `lastsalary` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `evaluatoremployee` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `appraisalannotation` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `totalvaluepersonal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `totalvaluesupervisi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `totalvaluepartner` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (performanceappraisalid)` |  |

### Table `school.parameterglobal` <a id="table-school-parameterglobal"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `parameterglobal` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_parameter` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_parameter` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_parameter_system` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nilai_parameter_string` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tag` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `default_code` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_parameter)` |  |

### Table `school.paschool` <a id="table-school-paschool"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `paschool` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `performanceappraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `conclusion` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `suggestion` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (performanceappraisalid)` |  |

### Table `school.performanceappraisal` <a id="table-school-performanceappraisal"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `performanceappraisal` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `performanceappraisalid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `appraisaldate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `totalvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inputuser` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputterminal` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `inputdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `generalvaluescale` | `character varying(2)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `filelegalpa` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `schoolyearcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `pptemplateid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `patype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (performanceappraisalid)` |  |

### Table `school.performanceitem` <a id="table-school-performanceitem"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `performanceitem` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `performanceitemid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `value` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `subtotal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `performancevaluescale` | `character varying(2)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `performanceappraisalid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `parameterid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `itemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `valuepersonal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `valuesupervisi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `valuepartner` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `subtotalpersonal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `subtotalsupervisi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `subtotalpartner` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (performanceitemid)` |  |

### Table `school.performanceparameter` <a id="table-school-performanceparameter"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `performanceparameter` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parametername` | `character varying(100)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(500)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `isdetaillevel` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `parameterid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 7 | `parametercode` | `character varying(40)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `pptype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameterid)` |  |

### Table `school.position` <a id="table-school-position"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `position` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `positionid` | `character varying(50)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `jobdescription` | `character varying(500)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nonactivedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (positionid)` |  |

### Table `school.pptemplate` <a id="table-school-pptemplate"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `pptemplate` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pptemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `pptemplatename` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `pptemplatecode` | `character varying(20)` | YES |  | UK | NO | none | reference_allowed | YES | needs_review |
| 5 | `pptype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (pptemplateid)` |  |
| `pptemplate_pptemplatecode_key` | UNIQUE | `UNIQUE (pptemplatecode)` |  |

### Table `school.pptemplateitem` <a id="table-school-pptemplateitem"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `pptemplateitem` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pptemplateid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parameterid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 4 | `ppitemcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (pptemplateid, parameterid)` |  |

### Table `school.product` <a id="table-school-product"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `product` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `accountofcollection` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `accountofdistribution` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `percentageofamilfunds` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `producttype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `status` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `closeddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `fundcategory` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `fixedvalue` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `fixedvalueamount` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `parentproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `isdetail` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `productcode` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `multipackage` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `nishab` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `haul` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `rate` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `productgroupname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `isquotafull` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `mustahiqquota` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `currentquotaposition` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `school.productgroup` <a id="table-school-productgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `productgroup` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productgroupname` | `character varying(50)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productgroupname)` |  |

### Table `school.program` <a id="table-school-program"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `program` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `programaddress` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `programphonenumber` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid)` |  |

### Table `school.propinsi` <a id="table-school-propinsi"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `propinsi` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idpropinsi` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `idnegara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `propinsi` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kodepropinsi` | `character varying(3)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (idpropinsi)` |  |

### Table `school.rankhistory` <a id="table-school-rankhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `rankhistory` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `rankhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `rank` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `rankeffectivedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (rankhistoryid)` |  |

### Table `school.reimbursementrealization` <a id="table-school-reimbursementrealization"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `reimbursementrealization` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `reimbursementrealizationid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `reimbursementdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `realizationvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nominal` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `finalbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `beginbalance` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `isauthorized` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `islast` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (reimbursementrealizationid)` |  |

### Table `school.salaryhistory` <a id="table-school-salaryhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `salaryhistory` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryhistoryid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `salaryreceiveddate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workunit` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `position` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `description` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `salaryvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `salaryschemeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `monthperiod` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `yearperiod` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryhistoryid)` |  |

### Table `school.salaryitemhistory` <a id="table-school-salaryitemhistory"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `salaryitemhistory` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
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
| 5 | `description` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryitemid)` |  |

### Table `school.salaryitemparameter` <a id="table-school-salaryitemparameter"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `salaryitemparameter` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryitemparameterid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parametername` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `description` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `itemvaluedefault` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `formuladefault` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `salaryitemperiod` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `salaryitemtypedefault` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `parametergroupid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryitemparameterid)` |  |

### Table `school.salaryitemparametergroup` <a id="table-school-salaryitemparametergroup"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `salaryitemparametergroup` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parametergroupid` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parametergroupid)` |  |

### Table `school.salaryitemscheme` <a id="table-school-salaryitemscheme"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `salaryitemscheme` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryitemschemeid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `salaryitemschemename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `itemvalue` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `formula` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `salaryitemtype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `salaryschemeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryitemschemeid)` |  |

### Table `school.salaryscheme` <a id="table-school-salaryscheme"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `salaryscheme` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `salaryschemeid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `salaryschemename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `isactive` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `positionid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (salaryschemeid)` |  |

### Table `school.schoolyear` <a id="table-school-schoolyear"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `schoolyear` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `schoolyearcode` | `character varying(5)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `schoolyear` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (schoolyearcode)` |  |

### Table `school.sessionblob` <a id="table-school-sessionblob"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `sessionblob` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `school.sourcefound` <a id="table-school-sourcefound"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `sourcefound` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `sourcefoundid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `sourcefoundname` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (sourcefoundid)` |  |

### Table `school.stockopname` <a id="table-school-stockopname"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `stockopname` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `stockopnameid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `stockopnamedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inputdate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (stockopnameid)` |  |

### Table `school.stockopnameequipment` <a id="table-school-stockopnameequipment"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `stockopnameequipment` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `stockopnameid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `equipmentid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `quantity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `unit` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `equipmentname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `lokasi` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (stockopnameid, equipmentid)` |  |

### Table `school.stockopnametools` <a id="table-school-stockopnametools"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `stockopnametools` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `stockopnameid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `toolsid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `toolsname` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `goodcondition` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `brokencondition` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `replaced` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `unit` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `lokasi` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (stockopnameid, toolsid)` |  |

### Table `school.student` <a id="table-school-student"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `student` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `productid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `action` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `complaint` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `reference` | `character varying(150)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `studentclasscode` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `classhistoryid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `nonactivedate` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `nonactivedescription` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (productid, mustahiqid)` |  |

### Table `school.studentclass` <a id="table-school-studentclass"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `studentclass` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `studentclasscode` | `character varying(100)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `productid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (studentclasscode)` |  |

### Table `school.studenthealth` <a id="table-school-studenthealth"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `studenthealth` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `studenthealthid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `productid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `action` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `complaint` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `reference` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `datehealth` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (studenthealthid)` |  |

### Table `school.subject` <a id="table-school-subject"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `subject` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subjectid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `subjectname` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `subjectcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subjectid)` |  |

### Table `school.targetachievement` <a id="table-school-targetachievement"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `targetachievement` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `targetachievementid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `evaluatoremployee` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `inputdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `inputterminal` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `inputuser` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `targetfile` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `achievementfile` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `targetdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `lastsalary` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `periodyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `workunit` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `positionid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `positioneffectivedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `rank` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `rankeffectivedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `achievementlegalfile` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `targetlegalfile` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `achievementdate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `schoolyearcode` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (targetachievementid)` |  |

### Table `school.toollist` <a id="table-school-toollist"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `toollist` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `toolsid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `toollistid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `officialreportid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `quantity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (toollistid)` |  |

### Table `school.tools` <a id="table-school-tools"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `tools` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `infrastructureid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `toolsid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `toolsname` | `character varying(40)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `parentid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `quantity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `description` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `goodcondition` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `brokencondition` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `unit` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `replacement` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (toolsid)` |  |

### Table `school.training` <a id="table-school-training"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `training` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `trainingid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `materi` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `institution` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `trainingtype` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (trainingid)` |  |

### Table `school.trainingseminar` <a id="table-school-trainingseminar"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `trainingseminar` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `trainingid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `status` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `year` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (trainingid)` |  |

### Table `school.workexperience` <a id="table-school-workexperience"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `workexperience` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workexperienceid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `individuid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `workyear` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `workinstitution` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `workposition` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `workjobdesk` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workexperienceid)` |  |

### Table `school.workunit` <a id="table-school-workunit"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `workunit` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workunitid` | `character varying(50)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parentid` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `status` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nonactivedate` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workunitid)` |  |

### Table `school.workunitposition` <a id="table-school-workunitposition"></a>

| Field | Value |
| --- | --- |
| Schema | `school` |
| Table | `workunitposition` |
| Domain | `Needs Review` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `workunitid` | `character varying(50)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `positionid` | `character varying(50)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `jobdeskfile` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (workunitid, positionid)` |  |
