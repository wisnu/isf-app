# DWH (Datamart) Schema — datadict

Generated dari `pg_dump mziss_laz -n dwh` pada 2026-05-27 (recovery snapshot).
Schema final state setelah migration 007 (drop stale unique indexes superseded by 004/006).

> **Catatan**: schema yang sama di-mirror sebagai `datamart.*` di `mziss_wakaf` (belum di-rename ke `dwh` — lihat `infra/db/migrations/README.md` outstanding work).

## Schema overview

- **dim_** = dimension table (master data: branch, donor, fund_type) — reference data
- **dm_** = data mart aggregate (pre-aggregated monthly grain × branch × fund_entity)
- **fact_** = fact table (event-level data, monthly grain)
- **etl_** = pipeline meta tables (run log + watermark)

Grain agregasi `dm_*` & `fact_*` umumnya: `(year, month, branch_key, fund_entity, …)`. Unique key include `fund_entity` sejak migration 007.

## `dim_branch`

| Column | Type | Null | Default |
|---|---|---|---|
| `branch_key` | `integer` | **NOT NULL** | `seq:dim_cabang_cabang_key_seq'::regclass)` |
| `branch_code` | `character varying(20)` | **NOT NULL** |  |
| `branch_name` | `character varying(60)` | nullable |  |
| `branch_type` | `character varying(2)` | nullable |  |
| `branch_status` | `character varying(1)` | nullable |  |
| `parent_branch_code` | `character varying(20)` | nullable |  |
| `region_code` | `character varying(3)` | nullable |  |
| `branch_level` | `smallint` | nullable |  |
| `is_active` | `character varying(1)` | nullable |  |
| `input_date` | `timestamp with time zone` | nullable |  |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |

## `dim_donor`

| Column | Type | Null | Default |
|---|---|---|---|
| `donorkey` | `bigint` | **NOT NULL** | `seq:dim_donatur_donorkey_seq'::regclass)` |
| `donorid` | `integer` | **NOT NULL** |  |
| `donorno` | `character varying(20)` | nullable |  |
| `donorname` | `character varying(200)` | nullable |  |
| `donortype` | `character varying(1)` | nullable |  |
| `donortype_label` | `character varying(20)` | nullable |  |
| `joindate` | `date` | nullable |  |
| `join_year` | `smallint` | nullable |  |
| `join_month` | `smallint` | nullable |  |
| `status` | `character varying(1)` | nullable |  |
| `branchcode` | `character varying(5)` | nullable |  |
| `economicsector` | `character varying(1)` | nullable |  |
| `donorgroup` | `character varying(1)` | nullable |  |
| `donorlevel_code` | `character varying(10)` | nullable |  |
| `donorlevel_desc` | `character varying(50)` | nullable |  |
| `contactperson` | `character varying(50)` | nullable |  |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |

## `dim_fund_type`

| Column | Type | Null | Default |
|---|---|---|---|
| `fund_entity_code` | `smallint` | **NOT NULL** |  |
| `fund_name_id` | `character varying(40)` | **NOT NULL** |  |
| `fund_name_en` | `character varying(40)` | **NOT NULL** |  |
| `fund_category` | `character varying(20)` | **NOT NULL** |  |
| `amil_max_pct` | `numeric(5,2)` | nullable |  |
| `is_active` | `boolean` | **NOT NULL** | `true` |

## `dm_account_balance`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:saldo_rekening_id_seq'::regclass)` |
| `accountno` | `character varying(30)` | **NOT NULL** |  |
| `accountname` | `character varying(50)` | nullable |  |
| `cashaccounttype` | `character varying(1)` | nullable |  |
| `bankname` | `character varying(100)` | nullable |  |
| `balance` | `numeric(18,2)` | **NOT NULL** | `0` |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |

## `dm_asnaf_monthly`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:asnaf_monthly_id_seq'::regclass)` |
| `realization_year` | `smallint` | **NOT NULL** |  |
| `realization_month` | `smallint` | **NOT NULL** |  |
| `ashnaf_code` | `character varying(1)` | **NOT NULL** |  |
| `ashnaf_name` | `character varying(50)` | nullable |  |
| `count_ashnaf` | `integer` | **NOT NULL** | `0` |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |
| `dist_amount` | `numeric(18,2)` | **NOT NULL** | `0` |

## `dm_authorization_summary`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:otorisasi_summary_id_seq'::regclass)` |
| `pending_count` | `integer` | **NOT NULL** | `0` |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |

## `dm_budget_realization`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:anggaran_realisasi_id_seq'::regclass)` |
| `budget_year` | `smallint` | **NOT NULL** |  |
| `ownerid` | `integer` | **NOT NULL** |  |
| `ownername` | `character varying(100)` | nullable |  |
| `budget_amount` | `numeric(18,2)` | **NOT NULL** | `0` |
| `realization_amount` | `numeric(18,2)` | **NOT NULL** | `0` |
| `pct_realization` | `numeric(6,1)` | **NOT NULL** | `0` |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |

## `dm_dist_monthly`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:dist_monthly_id_seq'::regclass)` |
| `dist_year` | `smallint` | **NOT NULL** |  |
| `dist_month` | `smallint` | **NOT NULL** |  |
| `accountno` | `character varying(30)` | nullable |  |
| `accountname` | `character varying(50)` | nullable |  |
| `productname` | `character varying(60)` | nullable |  |
| `dist_amount` | `numeric(18,2)` | **NOT NULL** | `0` |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |
| `fund_entity` | `smallint` | nullable |  |

## `dm_donor_monthly`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:donatur_monthly_id_seq'::regclass)` |
| `fund_year` | `smallint` | **NOT NULL** |  |
| `fund_month` | `smallint` | **NOT NULL** |  |
| `donor_active` | `integer` | **NOT NULL** | `0` |
| `donor_individual` | `integer` | **NOT NULL** | `0` |
| `donor_corporate` | `integer` | **NOT NULL** | `0` |
| `donor_new` | `integer` | **NOT NULL** | `0` |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |

## `dm_fund_monthly`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:fund_monthly_id_seq'::regclass)` |
| `fund_year` | `smallint` | **NOT NULL** |  |
| `fund_month` | `smallint` | **NOT NULL** |  |
| `accountno` | `character varying(30)` | nullable |  |
| `accountname` | `character varying(50)` | nullable |  |
| `fund_amount` | `numeric(18,2)` | **NOT NULL** | `0` |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |
| `productname` | `character varying(60)` | nullable |  |
| `fund_entity` | `smallint` | nullable |  |
| `transaction_count` | `integer` | **NOT NULL** | `0` |

## `dm_program_memo`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:memo_realisasi_id_seq'::regclass)` |
| `realmemoid` | `integer` | **NOT NULL** |  |
| `realmemonumber` | `character varying(100)` | nullable |  |
| `realmemosubject` | `character varying(100)` | nullable |  |
| `realmemoamount` | `numeric(18,2)` | nullable |  |
| `realizationmemotype` | `character varying(1)` | nullable |  |
| `realmemodate` | `date` | nullable |  |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |

## `etl_log`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:etl_log_id_seq'::regclass)` |
| `run_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `table_name` | `character varying(60)` | **NOT NULL** |  |
| `status` | `character varying(10)` | **NOT NULL** |  |
| `rows_affected` | `integer` | nullable |  |
| `duration_ms` | `integer` | nullable |  |
| `error_message` | `text` | nullable |  |

## `etl_watermark`

| Column | Type | Null | Default |
|---|---|---|---|
| `table_name` | `character varying(60)` | **NOT NULL** |  |
| `last_year` | `smallint` | nullable |  |
| `last_month` | `smallint` | nullable |  |
| `last_run_at` | `timestamp with time zone` | nullable |  |

## `fact_fundraising_monthly`

| Column | Type | Null | Default |
|---|---|---|---|
| `id` | `bigint` | **NOT NULL** | `seq:fact_penerimaan_monthly_id_seq'::regclass)` |
| `fund_year` | `smallint` | **NOT NULL** |  |
| `fund_month` | `smallint` | **NOT NULL** |  |
| `donorkey` | `bigint` | **NOT NULL** |  |
| `channel_accountno` | `character varying(30)` | nullable |  |
| `channel_accountname` | `character varying(50)` | nullable |  |
| `productname` | `character varying(60)` | nullable |  |
| `total_amount` | `numeric(18,2)` | **NOT NULL** | `0` |
| `count_transaksi` | `integer` | **NOT NULL** | `0` |
| `refreshed_at` | `timestamp with time zone` | **NOT NULL** | `now()` |
| `branch_key` | `integer` | nullable |  |
| `fund_entity` | `smallint` | nullable |  |

