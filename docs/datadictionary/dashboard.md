# Data Dictionary — Schema `dashboard`

Format mengikuti `docs/panduan_format_data_dictionary_corebanking.md`. Field heuristik (`Domain`, `Table Type`, `PII`, `Masking`, `Seed`, `Description`, `Catatan`) ditandai `needs_review` bila tidak dapat ditebak otomatis — silakan tune manual.

## Sequences: `dashboard`

| Nama | Schema | Owned By | Used By | Start | Last Value | Increment | Cache | Cycle | Baseline | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `auth_group_id_seq` | `dashboard` | `dashboard.auth_group.id` | `dashboard.auth_group.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `auth_group_permissions_id_seq` | `dashboard` | `dashboard.auth_group_permissions.id` | `dashboard.auth_group_permissions.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `auth_permission_id_seq` | `dashboard` | `dashboard.auth_permission.id` | `dashboard.auth_permission.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `auth_user_groups_id_seq` | `dashboard` | `dashboard.auth_user_groups.id` | `dashboard.auth_user_groups.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `auth_user_id_seq` | `dashboard` | `dashboard.auth_user.id` | `dashboard.auth_user.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `auth_user_user_permissions_id_seq` | `dashboard` | `dashboard.auth_user_user_permissions.id` | `dashboard.auth_user_user_permissions.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `django_admin_log_id_seq` | `dashboard` | `dashboard.django_admin_log.id` | `dashboard.django_admin_log.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `django_content_type_id_seq` | `dashboard` | `dashboard.django_content_type.id` | `dashboard.django_content_type.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |
| `django_migrations_id_seq` | `dashboard` | `dashboard.django_migrations.id` | `dashboard.django_migrations.id` | 1 | 1 | 1 | 1 | NO | YES | Baseline existing, mapping via OWNED BY / nextval default |

## Views

| Nama | Schema | Catatan |
| --- | --- | --- |
| `v_ashnaf_bymonthyear` | `dashboard` | needs_review (definisi view lihat DDL sumber) |
| `v_budget_bymonthyear` | `dashboard` | needs_review (definisi view lihat DDL sumber) |
| `v_dist_monthyear_byproduct` | `dashboard` | needs_review (definisi view lihat DDL sumber) |
| `v_fund_monthyear_bycash` | `dashboard` | needs_review (definisi view lihat DDL sumber) |

## Tables

Daftar table:

- [`dashboard.auth_group`](#table-dashboard-auth-group) — 2 kolom
- [`dashboard.auth_group_permissions`](#table-dashboard-auth-group-permissions) — 3 kolom
- [`dashboard.auth_permission`](#table-dashboard-auth-permission) — 4 kolom
- [`dashboard.auth_user`](#table-dashboard-auth-user) — 11 kolom
- [`dashboard.auth_user_groups`](#table-dashboard-auth-user-groups) — 3 kolom
- [`dashboard.auth_user_user_permissions`](#table-dashboard-auth-user-user-permissions) — 3 kolom
- [`dashboard.django_admin_log`](#table-dashboard-django-admin-log) — 8 kolom
- [`dashboard.django_content_type`](#table-dashboard-django-content-type) — 3 kolom
- [`dashboard.django_migrations`](#table-dashboard-django-migrations) — 4 kolom

### Table `dashboard.auth_group` <a id="table-dashboard-auth-group"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `auth_group` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.auth_group_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `name` | `character varying(80)` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |
| `auth_group_name_key` | UNIQUE | `UNIQUE (name)` |  |

### Table `dashboard.auth_group_permissions` <a id="table-dashboard-auth-group-permissions"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `auth_group_permissions` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.auth_group_permissions_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `group_id` | `integer` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |
| 3 | `permission_id` | `integer` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |
| `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` | UNIQUE | `UNIQUE (group_id, permission_id)` |  |

### Table `dashboard.auth_permission` <a id="table-dashboard-auth-permission"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `auth_permission` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.auth_permission_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `name` | `character varying(255)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `content_type_id` | `integer` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |
| 4 | `codename` | `character varying(100)` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |
| `auth_permission_content_type_id_codename_01ab375a_uniq` | UNIQUE | `UNIQUE (content_type_id, codename)` |  |

### Table `dashboard.auth_user` <a id="table-dashboard-auth-user"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `auth_user` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.auth_user_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `password` | `character varying(128)` | NO |  |  | YES | full | synthetic_only | YES | needs_review |
| 3 | `last_login` | `timestamp with time zone` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `is_superuser` | `boolean` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `username` | `character varying(30)` | NO |  | UK | YES | partial | synthetic_only | YES | needs_review |
| 6 | `first_name` | `character varying(30)` | NO |  |  | YES | partial | synthetic_only | YES | needs_review |
| 7 | `last_name` | `character varying(30)` | NO |  |  | YES | partial | synthetic_only | YES | needs_review |
| 8 | `email` | `character varying(254)` | NO |  |  | YES | partial | synthetic_only | YES | needs_review |
| 9 | `is_staff` | `boolean` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 10 | `is_active` | `boolean` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 11 | `date_joined` | `timestamp with time zone` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |
| `auth_user_username_key` | UNIQUE | `UNIQUE (username)` |  |

### Table `dashboard.auth_user_groups` <a id="table-dashboard-auth-user-groups"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `auth_user_groups` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.auth_user_groups_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_id` | `integer` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |
| 3 | `group_id` | `integer` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |
| `auth_user_groups_user_id_group_id_94350c0c_uniq` | UNIQUE | `UNIQUE (user_id, group_id)` |  |

### Table `dashboard.auth_user_user_permissions` <a id="table-dashboard-auth-user-user-permissions"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `auth_user_user_permissions` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.auth_user_user_permissions_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `user_id` | `integer` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |
| 3 | `permission_id` | `integer` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |
| `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` | UNIQUE | `UNIQUE (user_id, permission_id)` |  |

### Table `dashboard.django_admin_log` <a id="table-dashboard-django-admin-log"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `django_admin_log` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.django_admin_log_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `action_time` | `timestamp with time zone` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `object_id` | `text` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `object_repr` | `character varying(200)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 5 | `action_flag` | `smallint` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 6 | `change_message` | `text` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 7 | `content_type_id` | `integer` | YES |  |  | NO | none | reference_allowed | YES | needs_review |
| 8 | `user_id` | `integer` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |

### Table `dashboard.django_content_type` <a id="table-dashboard-django-content-type"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `django_content_type` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.django_content_type_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `app_label` | `character varying(100)` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |
| 3 | `model` | `character varying(100)` | NO |  | UK | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |
| `django_content_type_app_label_model_76bd3d3b_uniq` | UNIQUE | `UNIQUE (app_label, model)` |  |

### Table `dashboard.django_migrations` <a id="table-dashboard-django-migrations"></a>

| Field | Value |
| --- | --- |
| Schema | `dashboard` |
| Table | `django_migrations` |
| Domain | `Entity` |
| Table Type | `configuration` |
| Classification | `internal` |
| Source of Truth | YES |
| Legacy Combined Schema | NO |
| Future Schema Candidate |  |
| Description | needs_review |

| # | Kolom | Tipe | Nullable | Default | Key | PII | Masking | Seed | Source of Truth | Catatan |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `id` | `integer` | NO | nextval('dashboard.django_migrations_id_seq'::regclass) | PK | NO | none | reference_allowed | YES | needs_review |
| 2 | `app` | `character varying(255)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 3 | `name` | `character varying(255)` | NO |  |  | NO | none | reference_allowed | YES | needs_review |
| 4 | `applied` | `timestamp with time zone` | NO |  |  | NO | none | reference_allowed | YES | needs_review |

#### Constraints

| Nama | Tipe | Definisi | Catatan |
| --- | --- | --- | --- |
| (primary key) | PRIMARY KEY | `PRIMARY KEY (id)` |  |
