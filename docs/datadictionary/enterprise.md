# Data Dictionary — Schema `enterprise`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `enterprise`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `inbox_ID_seq` | `enterprise` | `enterprise.inbox.ID` | `enterprise.inbox.ID` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `outbox_ID_seq` | `enterprise` | `enterprise.outbox.ID` | `enterprise.outbox.ID` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `outbox_multipart_ID_seq` | `enterprise` | `enterprise.outbox_multipart.ID` | `enterprise.outbox_multipart.ID` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `pbk_ID_seq` | `enterprise` | `enterprise.pbk.ID` | `enterprise.pbk.ID` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `pbk_groups_ID_seq` | `enterprise` | `enterprise.pbk_groups.ID` | `enterprise.pbk_groups.ID` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `pbk_id_seq` | `enterprise` |  | needs_review | 3 | 3 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `sentitems_ID_seq` | `enterprise` | `enterprise.sentitems.ID` | `enterprise.sentitems.ID` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `seq_employee` | `enterprise` |  | needs_review | 727 | 727 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_gajiemployee` | `enterprise` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_kemampuanbahasaemployee` | `enterprise` |  | needs_review | 1 | 1 | 1 | 1 | YES | YES | Baseline existing, perlu mapping ke table.column |
| `seq_keterampilanemployee` | `enterprise` |  | needs_review | 1 | 1 | 1 | 1 | YES | YES | Baseline existing, perlu mapping ke table.column |
| `seq_limittransaksi` | `enterprise` |  | needs_review | 40 | 40 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_loginsession` | `enterprise` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_menu` | `enterprise` |  | needs_review | 11229 | 11229 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_menuhierarchy` | `enterprise` |  | needs_review | 21447 | 21447 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_otordata` | `enterprise` |  | needs_review | 29 | 29 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_otorentri` | `enterprise` |  | needs_review | 29 | 29 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_outbox` | `enterprise` |  | needs_review | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_pendidikanemployee` | `enterprise` |  | needs_review | 1 | 1 | 1 | 1 | YES | YES | Baseline existing, perlu mapping ke table.column |
| `seq_pengalamanemployee` | `enterprise` |  | needs_review | 1 | 1 | 1 | 1 | YES | YES | Baseline existing, perlu mapping ke table.column |
| `seq_rolemenulist` | `enterprise` |  | needs_review | 8231 | 8231 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_useraudit` | `enterprise` |  | needs_review | 13951 | 13951 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |
| `seq_usermenulist` | `enterprise` |  | needs_review | 17 | 17 | 1 | 1 | NO | YES | Baseline existing, perlu mapping ke table.column |

## Views

| Nama | Schema | Catatan |
| --- | --- | --- |
| `vemployee` | `enterprise` | needs_review (definisi view lihat DDL sumber) |

## Tables

Daftar table:

- [`enterprise.aplikasi`](#table-enterprise-aplikasi) — 8 kolom
- [`enterprise.appsubsystem`](#table-enterprise-appsubsystem) — 9 kolom
- [`enterprise.areacabang`](#table-enterprise-areacabang) — 2 kolom
- [`enterprise.backuppass`](#table-enterprise-backuppass) — 3 kolom
- [`enterprise.bpparallelstep`](#table-enterprise-bpparallelstep) — 5 kolom
- [`enterprise.bpparallelstepdetail`](#table-enterprise-bpparallelstepdetail) — 7 kolom
- [`enterprise.bpparallelstepinstance`](#table-enterprise-bpparallelstepinstance) — 3 kolom
- [`enterprise.bpprocess`](#table-enterprise-bpprocess) — 9 kolom
- [`enterprise.bpscenario`](#table-enterprise-bpscenario) — 2 kolom
- [`enterprise.bpscenarioinstance`](#table-enterprise-bpscenarioinstance) — 8 kolom
- [`enterprise.bpscript`](#table-enterprise-bpscript) — 4 kolom
- [`enterprise.bpstep`](#table-enterprise-bpstep) — 6 kolom
- [`enterprise.bpstepinstance`](#table-enterprise-bpstepinstance) — 9 kolom
- [`enterprise.cabang`](#table-enterprise-cabang) — 33 kolom
- [`enterprise.cabangbmi`](#table-enterprise-cabangbmi) — 3 kolom
- [`enterprise.custom_idgen`](#table-enterprise-custom-idgen) — 4 kolom
- [`enterprise.daemons`](#table-enterprise-daemons) — 2 kolom
- [`enterprise.departemen`](#table-enterprise-departemen) — 3 kolom
- [`enterprise.employee`](#table-enterprise-employee) — 39 kolom
- [`enterprise.enum_int`](#table-enterprise-enum-int) — 3 kolom
- [`enterprise.enum_varchar`](#table-enterprise-enum-varchar) — 3 kolom
- [`enterprise.executablefungsi`](#table-enterprise-executablefungsi) — 11 kolom
- [`enterprise.fungsi`](#table-enterprise-fungsi) — 5 kolom
- [`enterprise.gajiemployee`](#table-enterprise-gajiemployee) — 28 kolom
- [`enterprise.gammu`](#table-enterprise-gammu) — 1 kolom
- [`enterprise.glinterface`](#table-enterprise-glinterface) — 14 kolom
- [`enterprise.historikehadiran`](#table-enterprise-historikehadiran) — 7 kolom
- [`enterprise.id_gen`](#table-enterprise-id-gen) — 3 kolom
- [`enterprise.inbox`](#table-enterprise-inbox) — 12 kolom
- [`enterprise.inboxdeletedsms`](#table-enterprise-inboxdeletedsms) — 14 kolom
- [`enterprise.inboxparameter`](#table-enterprise-inboxparameter) — 5 kolom
- [`enterprise.jabatan`](#table-enterprise-jabatan) — 3 kolom
- [`enterprise.kantor`](#table-enterprise-kantor) — 10 kolom
- [`enterprise.kemampuanbahasaemployee`](#table-enterprise-kemampuanbahasaemployee) — 5 kolom
- [`enterprise.keterampilanemployee`](#table-enterprise-keterampilanemployee) — 4 kolom
- [`enterprise.limitoperasi`](#table-enterprise-limitoperasi) — 7 kolom
- [`enterprise.limittransaksi`](#table-enterprise-limittransaksi) — 6 kolom
- [`enterprise.listaplikasiperan`](#table-enterprise-listaplikasiperan) — 2 kolom
- [`enterprise.listaplikasiuser`](#table-enterprise-listaplikasiuser) — 3 kolom
- [`enterprise.listcabangdiizinkan`](#table-enterprise-listcabangdiizinkan) — 2 kolom
- [`enterprise.listfungsiaplikasiperan`](#table-enterprise-listfungsiaplikasiperan) — 3 kolom
- [`enterprise.listfungsiaplikasiuser`](#table-enterprise-listfungsiaplikasiuser) — 3 kolom
- [`enterprise.listperanuser`](#table-enterprise-listperanuser) — 3 kolom
- [`enterprise.listperanuser_bck`](#table-enterprise-listperanuser-bck) — 3 kolom
- [`enterprise.listterminaldiizinkan`](#table-enterprise-listterminaldiizinkan) — 2 kolom
- [`enterprise.loginsession`](#table-enterprise-loginsession) — 8 kolom
- [`enterprise.lokasi`](#table-enterprise-lokasi) — 3 kolom
- [`enterprise.menu`](#table-enterprise-menu) — 10 kolom
- [`enterprise.menuhierarchy`](#table-enterprise-menuhierarchy) — 3 kolom
- [`enterprise.otordata`](#table-enterprise-otordata) — 4 kolom
- [`enterprise.otorentri`](#table-enterprise-otorentri) — 18 kolom
- [`enterprise.otorentrihistori`](#table-enterprise-otorentrihistori) — 23 kolom
- [`enterprise.otorparameter`](#table-enterprise-otorparameter) — 7 kolom
- [`enterprise.otpkey`](#table-enterprise-otpkey) — 8 kolom
- [`enterprise.outbox`](#table-enterprise-outbox) — 18 kolom
- [`enterprise.outbox_bak`](#table-enterprise-outbox-bak) — 18 kolom
- [`enterprise.outbox_multipart`](#table-enterprise-outbox-multipart) — 7 kolom
- [`enterprise.outboxdeleted`](#table-enterprise-outboxdeleted) — 20 kolom
- [`enterprise.parameterglobal`](#table-enterprise-parameterglobal) — 7 kolom
- [`enterprise.pbk`](#table-enterprise-pbk) — 4 kolom
- [`enterprise.pbk_groups`](#table-enterprise-pbk-groups) — 2 kolom
- [`enterprise.pendidikanemployee`](#table-enterprise-pendidikanemployee) — 7 kolom
- [`enterprise.pengalamanemployee`](#table-enterprise-pengalamanemployee) — 7 kolom
- [`enterprise.peran`](#table-enterprise-peran) — 10 kolom
- [`enterprise.phones`](#table-enterprise-phones) — 12 kolom
- [`enterprise.publication`](#table-enterprise-publication) — 2 kolom
- [`enterprise.rekeningemployee`](#table-enterprise-rekeningemployee) — 6 kolom
- [`enterprise.rolemenulist`](#table-enterprise-rolemenulist) — 3 kolom
- [`enterprise.sentitems`](#table-enterprise-sentitems) — 19 kolom
- [`enterprise.subscribeitem`](#table-enterprise-subscribeitem) — 4 kolom
- [`enterprise.teller`](#table-enterprise-teller) — 2 kolom
- [`enterprise.terminal`](#table-enterprise-terminal) — 11 kolom
- [`enterprise.userapp`](#table-enterprise-userapp) — 37 kolom
- [`enterprise.useraudit`](#table-enterprise-useraudit) — 7 kolom
- [`enterprise.usermenulist`](#table-enterprise-usermenulist) — 3 kolom
- [`enterprise.usertbl`](#table-enterprise-usertbl) — 3 kolom

### Table `enterprise.aplikasi` <a id="table-enterprise-aplikasi"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `aplikasi` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_aplikasi` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_aplikasi` | `character varying(100)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `deskripsi` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nama_server` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `protokol_akses` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `lokasi_source` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `lokasi_session` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `nama_session` | `character varying(50)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_aplikasi)` |  |

### Table `enterprise.appsubsystem` <a id="table-enterprise-appsubsystem"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `appsubsystem` |
| Domain | `Entity` |
| Table Type | `master` |
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

### Table `enterprise.areacabang` <a id="table-enterprise-areacabang"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `areacabang` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_wilayah` | `character varying(3)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `keterangan` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_wilayah)` |  |

### Table `enterprise.backuppass` <a id="table-enterprise-backuppass"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `backuppass` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_user` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `password` | `character varying(32)` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 3 | `decode` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.bpparallelstep` <a id="table-enterprise-bpparallelstep"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpparallelstep` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parallel_step_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parameter_name` | `character varying(100)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `parameter_order` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `parameter_type` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `step_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parallel_step_id)` |  |

### Table `enterprise.bpparallelstepdetail` <a id="table-enterprise-bpparallelstepdetail"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpparallelstepdetail` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pstep_detail_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `svalue` | `character varying(500)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ivalue` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `parameter_type` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `unrestrict_next_step` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `parallel_step_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `disabled` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (pstep_detail_id)` |  |

### Table `enterprise.bpparallelstepinstance` <a id="table-enterprise-bpparallelstepinstance"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpparallelstepinstance` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pstepinst_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `stepinst_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `pstep_detail_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (pstepinst_id)` |  |

### Table `enterprise.bpprocess` <a id="table-enterprise-bpprocess"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpprocess` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `bpprocess_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `pid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `status` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `main_pid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `phost` | `character varying(24)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `error_info` | `character varying(255)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `step_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `ctlcommand` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `processed` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (bpprocess_id)` |  |

### Table `enterprise.bpscenario` <a id="table-enterprise-bpscenario"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpscenario` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `scenario_code` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `scenario_name` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (scenario_code)` |  |

### Table `enterprise.bpscenarioinstance` <a id="table-enterprise-bpscenarioinstance"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpscenarioinstance` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `instance_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `start_time` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `stop_time` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_id` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `terminal_id` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `status` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `main_pid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `scenario_code` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (instance_id)` |  |

### Table `enterprise.bpscript` <a id="table-enterprise-bpscript"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpscript` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `script_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `script_path` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kode_aplikasi` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (script_id)` |  |

### Table `enterprise.bpstep` <a id="table-enterprise-bpstep"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpstep` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `step_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `step_order` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `disabled` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `scenario_code` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `script_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (step_id)` |  |

### Table `enterprise.bpstepinstance` <a id="table-enterprise-bpstepinstance"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `bpstepinstance` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `stepinst_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `start_time` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `stop_time` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `status` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `step_error_message` | `character varying(255)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `main_pid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `pid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `step_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `instance_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (stepinst_id)` |  |

### Table `enterprise.cabang` <a id="table-enterprise-cabang"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `cabang` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_cabang` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_cabang` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `tipe_cabang` | `character varying(2)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `status_cabang` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `sandi_bi` | `character varying(7)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `zona_waktu` | `character varying(2)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `terminal_input` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `user_otorisasi` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `tanggal_otorisasi` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `terminal_otorisasi` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `kode_cabang_induk` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `status_aktif` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `status_otorisasi` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kode_wilayah` | `character varying(3)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `kode_kantor` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `branchid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `kode_singkat` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `kode_lokasi` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `status_akses` | `character(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `id_sandibi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `id_sandilokasi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `level_cabang` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `kode_wilayah_kliring` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `kantor_alamat` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 27 | `kantor_kode_pos` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `kantor_nama` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 29 | `kantor_npwp` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 30 | `kantor_telepon1` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `kantor_telepon2` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `kantor_telepon3` | `character varying(15)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `kantor_tipe` | `character varying(2)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_cabang)` |  |

### Table `enterprise.cabangbmi` <a id="table-enterprise-cabangbmi"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `cabangbmi` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_cabang` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `kode_cabang` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nama_cabang` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_cabang)` |  |

### Table `enterprise.custom_idgen` <a id="table-enterprise-custom-idgen"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `custom_idgen` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `enterprise.daemons` <a id="table-enterprise-daemons"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `daemons` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Start` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `Info` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.departemen` <a id="table-enterprise-departemen"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `departemen` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_departemen` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_departemen` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_departemen)` |  |

### Table `enterprise.employee` <a id="table-enterprise-employee"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `employee` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `alamat` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `agama` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `alamatsekarang` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `email` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `golongandarah` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `jeniskelamin` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `jumlahtanggungan` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `namaemployee` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `nomordplk` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `nomor_seluler` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `nomorindukpegawai` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `nomorjamsostek` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `nomorktp` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `nomorpaspor` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `npwp` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 16 | `npwz` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `pendidikanterakhir` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `statuspernikahan` | `character varying(1)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 19 | `tanggallahir` | `date` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `teleponkantor` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `teleponrumah` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `tempatlahir` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `titel` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `employeeid` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 25 | `inisial` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `nomor_karyawan` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `employeetype` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `kode_pos` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `nomor_telepon` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 30 | `nama_supervisor` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 31 | `is_supervisor` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 32 | `is_personalia` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `is_lemburberlaku` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `nomor_kartu` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `kode_departemen` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `kode_jabatan` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 37 | `id_cabangbmi` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 38 | `kode_cabang` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 39 | `nama_lengkap` | `character varying(200)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (employeeid)` |  |

### Table `enterprise.enum_int` <a id="table-enterprise-enum-int"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `enum_int` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `enterprise.enum_varchar` <a id="table-enterprise-enum-varchar"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `enum_varchar` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `enterprise.executablefungsi` <a id="table-enterprise-executablefungsi"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `executablefungsi` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `is_dual_control` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `level_dual_control` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `level_override` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `level_akses` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `hari_diperbolehkan_akses` | `character varying(7)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `waktu_boleh_diakses` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `waktu_selesai_diakses` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `id_fungsi` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 9 | `restriksi_hari_akses` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `restriksi_waktu_akses` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `limit_transaksi_user` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_fungsi)` |  |

### Table `enterprise.fungsi` <a id="table-enterprise-fungsi"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `fungsi` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_fungsi` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_fungsi` | `character varying(60)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `tipe_fungsi` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `id_parent_fungsi` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `kode_aplikasi` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_fungsi)` |  |

### Table `enterprise.gajiemployee` <a id="table-enterprise-gajiemployee"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `gajiemployee` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `nomorindukpegawai` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `bonusditerima` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `asuransi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `aqh` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `dplk` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `gajipokok` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `haricuti` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `iuranasuransi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `iuranjamsostek` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `iurandplk` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `pendapatanlain` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `potonganlain` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `rawatinap` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `rawatjalan` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `tanggal` | `date` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `thr` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `thrditerima` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `tunjangancuti` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `tunjangancutiditerima` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `tunjanganjabatan` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `tunjanganjamsostek` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `tunjangankehadiran` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `tunjangankesehatan` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `tunjangankesehatanditerima` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `tunjangankinerja` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `tunjanganpendidikan` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `tunjanganpulsa` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 28 | `employeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.gammu` <a id="table-enterprise-gammu"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `gammu` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Version` | `smallint` | NO | (0)::smallint |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.glinterface` <a id="table-enterprise-glinterface"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `glinterface` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_interface` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_interface` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `kode_account` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `kode_rc` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `terminal_input` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `user_perbarui` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `tanggal_perbarui` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `terminal_perbarui` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `id_interface` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 13 | `kode_valuta` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `kode_cabang` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_interface)` |  |

### Table `enterprise.historikehadiran` <a id="table-enterprise-historikehadiran"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `historikehadiran` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `tanggal` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_histori_kehadiran` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `waktu_datang` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `waktu_pulang` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nama_cabang` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `nama_departemen` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `nomor_karyawan` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_histori_kehadiran)` |  |

### Table `enterprise.id_gen` <a id="table-enterprise-id-gen"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `id_gen` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
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

### Table `enterprise.inbox` <a id="table-enterprise-inbox"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `inbox` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `UpdatedInDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `ReceivingDateTime` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `Text` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `SenderNumber` | `character varying(20)` | NO | ''::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `Coding` | `character varying(255)` | NO | 'Default_No_Compression'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `UDH` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `SMSCNumber` | `character varying(20)` | NO | ''::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `Class` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `TextDecoded` | `text` | NO | ''::text |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `ID` | `integer` | NO | nextval('enterprise.inbox_ID_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 11 | `RecipientID` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `Processed` | `boolean` | NO | false |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ID)` |  |

### Table `enterprise.inboxdeletedsms` <a id="table-enterprise-inboxdeletedsms"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `inboxdeletedsms` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `UpdatedInDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `ReceivingDateTime` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `Text` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `SenderNumber` | `character varying(20)` | NO | ''::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `Coding` | `character varying(255)` | NO | 'Default_No_Compression'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `UDH` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `SMSCNumber` | `character varying(20)` | NO | ''::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `Class` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `TextDecoded` | `text` | NO | ''::text |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `ID` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 11 | `RecipientID` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `Processed` | `boolean` | NO | false |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `DeletedDateTime` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `UserId` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ID)` |  |

### Table `enterprise.inboxparameter` <a id="table-enterprise-inboxparameter"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `inboxparameter` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `parameter_code` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(60)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `parameter_type` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `form_script_name` | `character varying(100)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `id_fungsi` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (parameter_code)` |  |

### Table `enterprise.jabatan` <a id="table-enterprise-jabatan"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `jabatan` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_jabatan` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_jabatan` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_jabatan)` |  |

### Table `enterprise.kantor` <a id="table-enterprise-kantor"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `kantor` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_kantor` | `character varying(5)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_kantor` | `character varying(100)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `tipe_kantor` | `character varying(2)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `alamat` | `character varying(200)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 5 | `nomor_npwp` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `kode_pos` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nomor_telepon1` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `nomor_telepon2` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `nomor_telepon3` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `kode_cabang` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_kantor)` |  |

### Table `enterprise.kemampuanbahasaemployee` <a id="table-enterprise-kemampuanbahasaemployee"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `kemampuanbahasaemployee` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kemampuanbahasaid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `namabahasa` | `integer` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `keahlianbicara` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `keahlianmenulis` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.keterampilanemployee` <a id="table-enterprise-keterampilanemployee"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `keterampilanemployee` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `keterampilanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `employeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `keahlianketerampilan` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `jenisketerampilan` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.limitoperasi` <a id="table-enterprise-limitoperasi"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `limitoperasi` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_limit_operasi` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `jenis_limit` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_limit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nilai_limit_akumulasi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `jumlah_item_limit` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `status_otorisasi` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `kode_cabang` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_limit_operasi)` |  |

### Table `enterprise.limittransaksi` <a id="table-enterprise-limittransaksi"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `limittransaksi` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_limit_transaksi` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `jenis_limit` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_limit` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `nilai_limit_akumulasi` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `jumlah_item_limit` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `id_user` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_limit_transaksi)` |  |

### Table `enterprise.listaplikasiperan` <a id="table-enterprise-listaplikasiperan"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `listaplikasiperan` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_aplikasi` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_peran` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_aplikasi, id_peran)` |  |

### Table `enterprise.listaplikasiuser` <a id="table-enterprise-listaplikasiuser"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `listaplikasiuser` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_listaplikasiuser` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_user` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `kode_aplikasi` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_listaplikasiuser)` |  |

### Table `enterprise.listcabangdiizinkan` <a id="table-enterprise-listcabangdiizinkan"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `listcabangdiizinkan` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_user` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `kode_cabang` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_user, kode_cabang)` |  |

### Table `enterprise.listfungsiaplikasiperan` <a id="table-enterprise-listfungsiaplikasiperan"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `listfungsiaplikasiperan` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_aplikasi` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_peran` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `id_fungsi` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_aplikasi, id_peran, id_fungsi)` |  |

### Table `enterprise.listfungsiaplikasiuser` <a id="table-enterprise-listfungsiaplikasiuser"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `listfungsiaplikasiuser` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_listfungsiaplikasiuser` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_fungsi` | `character varying(10)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `id_listaplikasiuser` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_listfungsiaplikasiuser)` |  |

### Table `enterprise.listperanuser` <a id="table-enterprise-listperanuser"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `listperanuser` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_peran` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_user` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 3 | `level_peranuser` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_peran, id_user)` |  |

### Table `enterprise.listperanuser_bck` <a id="table-enterprise-listperanuser-bck"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `listperanuser_bck` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_peran` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_user` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `level_peranuser` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.listterminaldiizinkan` <a id="table-enterprise-listterminaldiizinkan"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `listterminaldiizinkan` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_user` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_terminal` | `character varying(15)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_user, id_terminal)` |  |

### Table `enterprise.loginsession` <a id="table-enterprise-loginsession"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `loginsession` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `login_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `login_time` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `app_id` | `character varying(25)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `terminal_ip` | `character varying(25)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `session_id` | `character varying(25)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `last_access_time` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `user_id` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `branch_code` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (login_id)` |  |

### Table `enterprise.lokasi` <a id="table-enterprise-lokasi"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `lokasi` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_lokasi` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_lokasi` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `status_data` | `character(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.menu` <a id="table-enterprise-menu"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `menu` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `menu_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `menu_name` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `caption` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `menu_level` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `parent_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `filename_id` | `character varying(100)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `is_popup_menu` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `kode_aplikasi` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `is_main_menu` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `menu_idx` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (menu_id)` |  |

### Table `enterprise.menuhierarchy` <a id="table-enterprise-menuhierarchy"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `menuhierarchy` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `hierarchy_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `parent_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `child_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (hierarchy_id)` |  |

### Table `enterprise.otordata` <a id="table-enterprise-otordata"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `otordata` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_data` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `actualfilename` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `is_data_packet` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `createddate` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_data)` |  |

### Table `enterprise.otorentri` <a id="table-enterprise-otorentri"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `otorentri` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_otorisasi` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `tgl_input` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `user_input` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `terminal_input` | `character varying(25)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `tipe_target` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `info1` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `info2` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `nama_tabel` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 10 | `tipe_key` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `key_int` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `key_string` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `id_user` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `id_peran` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `kode_cabang` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `kode_entri` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `id_data` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `id_data1` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_otorisasi)` |  |

### Table `enterprise.otorentrihistori` <a id="table-enterprise-otorentrihistori"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `otorentrihistori` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_otorisasi` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `tgl_input` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `user_input` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `terminal_input` | `character varying(25)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `tipe_target` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `tgl_otorisasi` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `user_otorisasi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `terminal_otorisasi` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `status_otorisasi` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `keterangan` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `info1` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `info2` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `nama_entri` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 14 | `nama_tabel` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 15 | `tipe_key` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `key_int` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `key_string` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `id_data` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `id_user` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `id_peran` | `character varying(30)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `kode_cabang` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `id_data1` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `kode_entri` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_otorisasi)` |  |

### Table `enterprise.otorparameter` <a id="table-enterprise-otorparameter"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `otorparameter` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_entri` | `character varying(10)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `remote_form_id` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `method_id_save` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `method_id_reject` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nama_entri` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `classic_form_call` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `subsystem_code` | `character varying(5)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_entri)` |  |

### Table `enterprise.otpkey` <a id="table-enterprise-otpkey"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `otpkey` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `userid` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `token_base` | `character varying(16)` | YES | NULL::character varying |  | YES | full | synthetic_only | YES | needs_review |
| 3 | `t_challenge` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `key1` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `key2` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `key3` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `key4` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `key5` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (userid)` |  |

### Table `enterprise.outbox` <a id="table-enterprise-outbox"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `outbox` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `UpdatedInDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `InsertIntoDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `SendingDateTime` | `timestamp without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `SendBefore` | `time without time zone` | NO | '23:59:59'::time without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `SendAfter` | `time without time zone` | NO | '00:00:00'::time without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `Text` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `DestinationNumber` | `character varying(20)` | NO | ''::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `Coding` | `character varying(255)` | NO | 'Default_No_Compression'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `UDH` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `Class` | `integer` | YES | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `TextDecoded` | `text` | NO | ''::text |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `ID` | `integer` | NO | nextval('enterprise.outbox_ID_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 13 | `MultiPart` | `boolean` | NO | false |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `RelativeValidity` | `integer` | YES | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `SenderID` | `character varying(255)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `SendingTimeOut` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `DeliveryReport` | `character varying(10)` | YES | 'default'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `CreatorID` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ID)` |  |

### Table `enterprise.outbox_bak` <a id="table-enterprise-outbox-bak"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `outbox_bak` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `UpdatedInDB` | `timestamp(0) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `InsertIntoDB` | `timestamp(0) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `SendingDateTime` | `timestamp without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `SendBefore` | `time without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `SendAfter` | `time without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `Text` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `DestinationNumber` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `Coding` | `character varying(255)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `UDH` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `Class` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `TextDecoded` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `ID` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `MultiPart` | `boolean` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `RelativeValidity` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `SenderID` | `character varying(255)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `SendingTimeOut` | `timestamp(0) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `DeliveryReport` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `CreatorID` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.outbox_multipart` <a id="table-enterprise-outbox-multipart"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `outbox_multipart` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Text` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `Coding` | `character varying(255)` | NO | 'Default_No_Compression'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `UDH` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `Class` | `integer` | YES | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `TextDecoded` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `ID` | `integer` | NO | nextval('enterprise.outbox_multipart_ID_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 7 | `SequencePosition` | `integer` | NO | 1 | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ID, SequencePosition)` |  |

### Table `enterprise.outboxdeleted` <a id="table-enterprise-outboxdeleted"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `outboxdeleted` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `UpdatedInDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `InsertIntoDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `SendingDateTime` | `timestamp without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `SendBefore` | `time without time zone` | NO | '23:59:59'::time without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `SendAfter` | `time without time zone` | NO | '00:00:00'::time without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `Text` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `DestinationNumber` | `character varying(20)` | NO | ''::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `Coding` | `character varying(255)` | NO | 'Default_No_Compression'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `UDH` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `Class` | `integer` | YES | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `TextDecoded` | `text` | NO | ''::text |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `ID` | `integer` | NO | nextval('enterprise."outbox_ID_seq"'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 13 | `MultiPart` | `boolean` | NO | false |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `RelativeValidity` | `integer` | YES | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `SenderID` | `character varying(255)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `SendingTimeOut` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `DeliveryReport` | `character varying(10)` | YES | 'default'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `CreatorID` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `DeletedDateTime` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `UserId` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ID)` |  |

### Table `enterprise.parameterglobal` <a id="table-enterprise-parameterglobal"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `parameterglobal` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_parameter` | `character varying(10)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `tipe_parameter` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `nilai_parameter` | `double precision` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(60)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `is_parameter_system` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `nilai_parameter_tanggal` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `nilai_parameter_string` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (kode_parameter)` |  |

### Table `enterprise.pbk` <a id="table-enterprise-pbk"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `pbk` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `ID` | `integer` | NO | nextval('enterprise.pbk_ID_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `GroupID` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `Name` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `Number` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ID)` |  |

### Table `enterprise.pbk_groups` <a id="table-enterprise-pbk-groups"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `pbk_groups` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `Name` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `ID` | `integer` | NO | nextval('enterprise.pbk_groups_ID_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ID)` |  |

### Table `enterprise.pendidikanemployee` <a id="table-enterprise-pendidikanemployee"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `pendidikanemployee` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pendidikanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `tahun` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `pendidikan` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `lembaga` | `character varying(60)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `status` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `jenispendidikan` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `employeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.pengalamanemployee` <a id="table-enterprise-pengalamanemployee"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `pengalamanemployee` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `pengalamanid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `tahun` | `character varying(4)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `lembaga` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `jabatan` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `deskripsitugas` | `character varying(100)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `employeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `tipepengalaman` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

### Table `enterprise.peran` <a id="table-enterprise-peran"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `peran` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_peran` | `character varying(30)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_peran` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `terminal_input` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `user_perbarui` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `tanggal_perbarui` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `terminal_perbarui` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `status_peran` | `character(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_peran)` |  |

### Table `enterprise.phones` <a id="table-enterprise-phones"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `phones` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `ID` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `UpdatedInDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `InsertIntoDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `TimeOut` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `Send` | `boolean` | NO | false |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `Receive` | `boolean` | NO | false |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `IMEI` | `character varying(35)` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 8 | `Client` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `Battery` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `Signal` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `Sent` | `integer` | NO | 0 |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `Received` | `integer` | NO | 0 |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (IMEI)` |  |

### Table `enterprise.publication` <a id="table-enterprise-publication"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `publication` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `publication_code` | `character varying(5)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `description` | `character varying(100)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (publication_code)` |  |

### Table `enterprise.rekeningemployee` <a id="table-enterprise-rekeningemployee"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `rekeningemployee` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `employeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `nomorindukpegawai` | `character varying(10)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `namabank` | `character varying(60)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `cabang` | `character varying(50)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `nomorrekening` | `character varying(30)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 6 | `namarekening` | `character varying(50)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |

### Table `enterprise.rolemenulist` <a id="table-enterprise-rolemenulist"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `rolemenulist` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `list_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_peran` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `menu_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (list_id)` |  |

### Table `enterprise.sentitems` <a id="table-enterprise-sentitems"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `sentitems` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `UpdatedInDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 2 | `InsertIntoDB` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `SendingDateTime` | `timestamp(0) without time zone` | NO | ('now'::text)::timestamp(0) without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `DeliveryDateTime` | `timestamp(0) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `Text` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `DestinationNumber` | `character varying(20)` | NO | ''::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `Coding` | `character varying(255)` | NO | 'Default_No_Compression'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `UDH` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `SMSCNumber` | `character varying(20)` | NO | ''::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `Class` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `TextDecoded` | `text` | NO | ''::text |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `ID` | `integer` | NO | nextval('enterprise.sentitems_ID_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 13 | `SenderID` | `character varying(255)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `SequencePosition` | `integer` | NO | 1 | PK | NO | none | reference_allowed | YES | needs_review |
| 15 | `Status` | `character varying(255)` | NO | 'SendingOK'::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `StatusError` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `TPMR` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `RelativeValidity` | `integer` | NO | '-1'::integer |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `CreatorID` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (ID, SequencePosition)` |  |

### Table `enterprise.subscribeitem` <a id="table-enterprise-subscribeitem"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `subscribeitem` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_sitem` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `script_path` | `character varying(200)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `kode_aplikasi` | `character varying(30)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `publication_code` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_sitem)` |  |

### Table `enterprise.teller` <a id="table-enterprise-teller"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `teller` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `kode_rekening_teller` | `character varying(7)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 2 | `id_user` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_user)` |  |

### Table `enterprise.terminal` <a id="table-enterprise-terminal"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `terminal` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_terminal` | `character varying(15)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `nama_terminal` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 3 | `lokasi_terminal` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `deskripsi` | `character varying(50)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `terminal_input` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `user_perbarui` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 9 | `tanggal_perbarui` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `terminal_perbarui` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `kode_kantor` | `character varying(5)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_terminal)` |  |

### Table `enterprise.userapp` <a id="table-enterprise-userapp"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `userapp` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id_user` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `password` | `character varying(32)` | YES | NULL::character varying |  | YES | full | synthetic_only | YES | needs_review |
| 3 | `status_profil` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `level_user` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `tanggal_didaftarkan` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `tanggal_kadaluarsa` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `tanggal_password_kadaluarsa` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | YES | full | synthetic_only | YES | needs_review |
| 8 | `tanggal_ubah_password_terakhir` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | YES | full | synthetic_only | YES | needs_review |
| 9 | `tanggal_aktif_terakhir` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `tipe_akses_cabang` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `tipe_akses_terminal` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 12 | `hari_diperbolehkan_akses` | `character varying(7)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 13 | `status_restriksi_waktu` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 14 | `waktu_boleh_mulai` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 15 | `waktu_harus_selesai` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 16 | `maksimum_jumlah_login` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 17 | `user_input` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 18 | `tanggal_input` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 19 | `terminal_input` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 20 | `user_perbarui` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 21 | `tanggal_perbarui` | `timestamp(6) without time zone` | YES | NULL::timestamp without time zone |  | NO | none | reference_allowed | YES | needs_review |
| 22 | `terminal_perbarui` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 23 | `tipe_user` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 24 | `jumlah_login_gagal` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 25 | `jumlah_login_aktif` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 26 | `kunci_akses` | `character varying(1)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 27 | `nama_user` | `character varying(30)` | YES | NULL::character varying |  | YES | partial | synthetic_only | YES | needs_review |
| 28 | `jumlah_validasi_gagal` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 29 | `status_password` | `integer` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 30 | `maksimum_tidak_aktif` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 31 | `maksimum_ganti_password` | `integer` | YES |  |  | YES | full | synthetic_only | YES | needs_review |
| 32 | `no_urut_teller` | `character varying(3)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 33 | `id_terminal` | `character varying(15)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 34 | `kode_cabang` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 35 | `nomor_karyawan` | `character varying(20)` | YES | NULL::character varying |  | NO | none | reference_allowed | YES | needs_review |
| 36 | `employeeid` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 37 | `nolimitlocation` | `character varying(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id_user)` |  |

### Table `enterprise.useraudit` <a id="table-enterprise-useraudit"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `useraudit` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `audit_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_id` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `ip_address` | `character varying(25)` | YES |  |  | YES | partial | synthetic_only | YES | needs_review |
| 4 | `action_time` | `timestamp(6) without time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `operation_code` | `character varying(32)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `is_objaudit` | `character(1)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `app_id` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (audit_id)` |  |

### Table `enterprise.usermenulist` <a id="table-enterprise-usermenulist"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `usermenulist` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `list_id` | `integer` | NO |  | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `id_user` | `character varying(20)` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `menu_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (list_id)` |  |

### Table `enterprise.usertbl` <a id="table-enterprise-usertbl"></a>

| Field | Value |
| --- | --- |
| Schema | `enterprise` |
| Table | `usertbl` |
| Domain | `Entity` |
| Table Type | `master` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `userid` | `character varying(20)` | NO | NULL::character varying | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `enc_password1` | `character varying(16)` | YES | NULL::character varying |  | YES | full | synthetic_only | YES | needs_review |
| 3 | `enc_password2` | `character varying(16)` | YES | NULL::character varying |  | YES | full | synthetic_only | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (userid)` |  |
