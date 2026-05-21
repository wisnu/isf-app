# Data Dictionary — Schema `public`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `public`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `seq_menu` | `public` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_menuhierarchy` | `public` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_mustahiqadditionalinfo` | `public` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_rolemenulist` | `public` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_usermenulist` | `public` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Composite Types

### `public.history`

```sql
created_by integer,
	created_stamp timestamp(0) without time zone,
	created_db_user character varying(20),
	created_ip inet,
	updated_by integer,
	updated_stamp timestamp(6) without time zone,
	updated_db_user character varying(20),
	updated_ip inet
```

## Views

| Nama | Schema | Catatan |
| --- | --- | --- |
| `branchlocation` | `public` | needs_review (definisi view lihat DDL sumber) |

## Tables

Daftar table:

- [`public.accountdetail`](#table-public-accountdetail) — 2 kolom
- [`public.accountgroup`](#table-public-accountgroup) — 3 kolom
- [`public.accountinterface`](#table-public-accountinterface) — 6 kolom
- [`public.accountinterfacemember`](#table-public-accountinterfacemember) — 3 kolom
- [`public.accountmanager`](#table-public-accountmanager) — 5 kolom
- [`public.accsubsystem`](#table-public-accsubsystem) — 13 kolom
- [`public.appsubsystem`](#table-public-appsubsystem) — 9 kolom
- [`public.blobregistration`](#table-public-blobregistration) — 2 kolom
- [`public.branchlocation_old`](#table-public-branchlocation-old) — 7 kolom
- [`public.cpalpamapping`](#table-public-cpalpamapping) — 3 kolom
- [`public.currency_pkpu`](#table-public-currency-pkpu) — 30 kolom
- [`public.custom_idgen`](#table-public-custom-idgen) — 4 kolom
- [`public.daemons`](#table-public-daemons) — 2 kolom
- [`public.mustahiqadditionalinfo`](#table-public-mustahiqadditionalinfo) — 19 kolom
- [`public.tmp_migrasikodepos`](#table-public-tmp-migrasikodepos) — 12 kolom

### Table `public.accountdetail` <a id="table-public-accountdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `accountdetail` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_account` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `fl_detail_account` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.accountgroup` <a id="table-public-accountgroup"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `accountgroup` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `accountgroup_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `accountgroup_name` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `id` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.accountinterface` <a id="table-public-accountinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `accountinterface` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `interface_code` | `character varying(10)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `description` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `interface_type` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_active` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `currency_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.accountinterfacemember` <a id="table-public-accountinterfacemember"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `accountinterfacemember` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `member_id` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `interface_code` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `account_code` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.accountmanager` <a id="table-public-accountmanager"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `accountmanager` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `amcode` | `character varying(10)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `rcno` | `character varying(4)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `employeeid` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `employeename` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `project_no` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.accsubsystem` <a id="table-public-accsubsystem"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `accsubsystem` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsystemcode` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
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

### Table `public.appsubsystem` <a id="table-public-appsubsystem"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `appsubsystem` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `subsystem_code` | `character varying(5)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `subsystem_name` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `is_local` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `session_name` | `character varying(20)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `remote_host` | `character varying(23)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `remote_port` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `is_ssl` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `ssl_profile_name` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `remote_appid` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (subsystem_code)` |  |

### Table `public.blobregistration` <a id="table-public-blobregistration"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `blobregistration` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `actualfilename` | `character varying(128)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.branchlocation_old` <a id="table-public-branchlocation-old"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `branchlocation_old` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `branch_code` | `character varying(5)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `branchname` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `branchstatus` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `last_update` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `masterbranch_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `dataid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.cpalpamapping` <a id="table-public-cpalpamapping"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `cpalpamapping` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `fl_lpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `fl_cpa_accountcode` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `cpalpamapping_id` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.currency_pkpu` <a id="table-public-currency-pkpu"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `currency_pkpu` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `currency_code` | `character varying(20)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
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

### Table `public.custom_idgen` <a id="table-public-custom-idgen"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `custom_idgen` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `idname` | `character varying(30)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `idcode` | `character varying(50)` | NO | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `last_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `locked` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.daemons` <a id="table-public-daemons"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `daemons` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Start` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `Info` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `public.mustahiqadditionalinfo` <a id="table-public-mustahiqadditionalinfo"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `mustahiqadditionalinfo` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `mustahiqinfoid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `mustahiqproductid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `mustahiqid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `mustahiqinfotype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `mustahiqidsupervisor` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `schoolname` | `character varying(200)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `sd_kelas` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `sd_tahunawal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `sd_tahunakhir` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `smp_kelas` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `smp_tahunawal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `smp_tahunakhir` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `sma_kelas` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `sma_tahunawal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `sma_tahunakhir` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `achievement` | `character varying(500)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `universitas_kelas` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `universitas_tahunawal` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `universitas_tahunakhir` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (mustahiqinfoid)` |  |

### Table `public.tmp_migrasikodepos` <a id="table-public-tmp-migrasikodepos"></a>

| Field | Value |
| --- | --- |
| Schema | `public` |
| Table | `tmp_migrasikodepos` |
| Domain | `Unknown` |
| Table Type | `unknown` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `baris` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `kode_pos` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `desa` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `is_valid` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_auth` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `kecamatan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kode_kecamatan` | `character varying(7)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kota` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `kode_kota` | `character varying(7)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `propinsi` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kode_propinsi` | `character varying(7)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
