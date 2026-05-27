--
-- PostgreSQL database dump
--

\restrict 0KydJNq0qZDMxngVPpxF19dr1GdLBNsOXEFgjWHDHmOcKkJfzmYfOKxXyORScju

-- Dumped from database version 18.3
-- Dumped by pg_dump version 18.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: dwh; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA dwh;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dm_budget_realization; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dm_budget_realization (
    id bigint CONSTRAINT anggaran_realisasi_id_not_null NOT NULL,
    budget_year smallint CONSTRAINT anggaran_realisasi_budget_year_not_null NOT NULL,
    ownerid integer CONSTRAINT anggaran_realisasi_ownerid_not_null NOT NULL,
    ownername character varying(100),
    budget_amount numeric(18,2) DEFAULT 0 CONSTRAINT anggaran_realisasi_anggaran_not_null NOT NULL,
    realization_amount numeric(18,2) DEFAULT 0 CONSTRAINT anggaran_realisasi_realisasi_not_null NOT NULL,
    pct_realization numeric(6,1) DEFAULT 0 CONSTRAINT anggaran_realisasi_pct_realisasi_not_null NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT anggaran_realisasi_refreshed_at_not_null NOT NULL,
    branch_key integer
);


--
-- Name: anggaran_realisasi_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.anggaran_realisasi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: anggaran_realisasi_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.anggaran_realisasi_id_seq OWNED BY dwh.dm_budget_realization.id;


--
-- Name: dm_asnaf_monthly; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dm_asnaf_monthly (
    id bigint CONSTRAINT asnaf_monthly_id_not_null NOT NULL,
    realization_year smallint CONSTRAINT asnaf_monthly_realization_year_not_null NOT NULL,
    realization_month smallint CONSTRAINT asnaf_monthly_realization_month_not_null NOT NULL,
    ashnaf_code character varying(1) CONSTRAINT asnaf_monthly_ashnaf_code_not_null NOT NULL,
    ashnaf_name character varying(50),
    count_ashnaf integer DEFAULT 0 CONSTRAINT asnaf_monthly_count_ashnaf_not_null NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT asnaf_monthly_refreshed_at_not_null NOT NULL,
    branch_key integer,
    dist_amount numeric(18,2) DEFAULT 0 NOT NULL,
    CONSTRAINT asnaf_monthly_realization_month_check CHECK (((realization_month >= 1) AND (realization_month <= 12)))
);


--
-- Name: asnaf_monthly_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.asnaf_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: asnaf_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.asnaf_monthly_id_seq OWNED BY dwh.dm_asnaf_monthly.id;


--
-- Name: dim_branch; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dim_branch (
    branch_key integer CONSTRAINT dim_cabang_cabang_key_not_null NOT NULL,
    branch_code character varying(20) CONSTRAINT dim_cabang_kode_cabang_not_null NOT NULL,
    branch_name character varying(60),
    branch_type character varying(2),
    branch_status character varying(1),
    parent_branch_code character varying(20),
    region_code character varying(3),
    branch_level smallint,
    is_active character varying(1),
    input_date timestamp with time zone,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT dim_cabang_refreshed_at_not_null NOT NULL
);


--
-- Name: dim_cabang_cabang_key_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.dim_cabang_cabang_key_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dim_cabang_cabang_key_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.dim_cabang_cabang_key_seq OWNED BY dwh.dim_branch.branch_key;


--
-- Name: dim_donor; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dim_donor (
    donorkey bigint CONSTRAINT dim_donatur_donorkey_not_null NOT NULL,
    donorid integer CONSTRAINT dim_donatur_donorid_not_null NOT NULL,
    donorno character varying(20),
    donorname character varying(200),
    donortype character varying(1),
    donortype_label character varying(20),
    joindate date,
    join_year smallint,
    join_month smallint,
    status character varying(1),
    branchcode character varying(5),
    economicsector character varying(1),
    donorgroup character varying(1),
    donorlevel_code character varying(10),
    donorlevel_desc character varying(50),
    contactperson character varying(50),
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT dim_donatur_refreshed_at_not_null NOT NULL
);


--
-- Name: dim_donatur_donorkey_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.dim_donatur_donorkey_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dim_donatur_donorkey_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.dim_donatur_donorkey_seq OWNED BY dwh.dim_donor.donorkey;


--
-- Name: dim_fund_type; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dim_fund_type (
    fund_entity_code smallint NOT NULL,
    fund_name_id character varying(40) NOT NULL,
    fund_name_en character varying(40) NOT NULL,
    fund_category character varying(20) NOT NULL,
    amil_max_pct numeric(5,2),
    is_active boolean DEFAULT true NOT NULL
);


--
-- Name: dm_dist_monthly; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dm_dist_monthly (
    id bigint CONSTRAINT dist_monthly_id_not_null NOT NULL,
    dist_year smallint CONSTRAINT dist_monthly_dist_year_not_null NOT NULL,
    dist_month smallint CONSTRAINT dist_monthly_dist_month_not_null NOT NULL,
    accountno character varying(30),
    accountname character varying(50),
    productname character varying(60),
    dist_amount numeric(18,2) DEFAULT 0 CONSTRAINT dist_monthly_dist_amount_not_null NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT dist_monthly_refreshed_at_not_null NOT NULL,
    branch_key integer,
    fund_entity smallint,
    CONSTRAINT dist_monthly_dist_month_check CHECK (((dist_month >= 1) AND (dist_month <= 12)))
);


--
-- Name: dist_monthly_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.dist_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dist_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.dist_monthly_id_seq OWNED BY dwh.dm_dist_monthly.id;


--
-- Name: dm_account_balance; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dm_account_balance (
    id bigint CONSTRAINT saldo_rekening_id_not_null NOT NULL,
    accountno character varying(30) CONSTRAINT saldo_rekening_accountno_not_null NOT NULL,
    accountname character varying(50),
    cashaccounttype character varying(1),
    bankname character varying(100),
    balance numeric(18,2) DEFAULT 0 CONSTRAINT saldo_rekening_balance_not_null NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT saldo_rekening_refreshed_at_not_null NOT NULL,
    branch_key integer
);


--
-- Name: dm_authorization_summary; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dm_authorization_summary (
    id bigint CONSTRAINT otorisasi_summary_id_not_null NOT NULL,
    pending_count integer DEFAULT 0 CONSTRAINT otorisasi_summary_pending_count_not_null NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT otorisasi_summary_refreshed_at_not_null NOT NULL,
    branch_key integer
);


--
-- Name: dm_donor_monthly; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dm_donor_monthly (
    id bigint CONSTRAINT donatur_monthly_id_not_null NOT NULL,
    fund_year smallint CONSTRAINT donatur_monthly_fund_year_not_null NOT NULL,
    fund_month smallint CONSTRAINT donatur_monthly_fund_month_not_null NOT NULL,
    donor_active integer DEFAULT 0 CONSTRAINT donatur_monthly_donatur_aktif_not_null NOT NULL,
    donor_individual integer DEFAULT 0 CONSTRAINT donatur_monthly_donatur_individu_not_null NOT NULL,
    donor_corporate integer DEFAULT 0 CONSTRAINT donatur_monthly_donatur_korporat_not_null NOT NULL,
    donor_new integer DEFAULT 0 CONSTRAINT donatur_monthly_donatur_baru_not_null NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT donatur_monthly_refreshed_at_not_null NOT NULL,
    branch_key integer,
    CONSTRAINT donatur_monthly_fund_month_check CHECK (((fund_month >= 1) AND (fund_month <= 12)))
);


--
-- Name: dm_fund_monthly; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dm_fund_monthly (
    id bigint CONSTRAINT fund_monthly_id_not_null NOT NULL,
    fund_year smallint CONSTRAINT fund_monthly_fund_year_not_null NOT NULL,
    fund_month smallint CONSTRAINT fund_monthly_fund_month_not_null NOT NULL,
    accountno character varying(30),
    accountname character varying(50),
    fund_amount numeric(18,2) DEFAULT 0 CONSTRAINT fund_monthly_fund_amount_not_null NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT fund_monthly_refreshed_at_not_null NOT NULL,
    branch_key integer,
    productname character varying(60),
    fund_entity smallint,
    transaction_count integer DEFAULT 0 NOT NULL,
    CONSTRAINT fund_monthly_fund_month_check CHECK (((fund_month >= 1) AND (fund_month <= 12)))
);


--
-- Name: dm_program_memo; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.dm_program_memo (
    id bigint CONSTRAINT memo_realisasi_id_not_null NOT NULL,
    realmemoid integer CONSTRAINT memo_realisasi_realmemoid_not_null NOT NULL,
    realmemonumber character varying(100),
    realmemosubject character varying(100),
    realmemoamount numeric(18,2),
    realizationmemotype character varying(1),
    realmemodate date,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT memo_realisasi_refreshed_at_not_null NOT NULL,
    branch_key integer
);


--
-- Name: donatur_monthly_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.donatur_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: donatur_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.donatur_monthly_id_seq OWNED BY dwh.dm_donor_monthly.id;


--
-- Name: etl_log; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.etl_log (
    id bigint NOT NULL,
    run_at timestamp with time zone DEFAULT now() NOT NULL,
    table_name character varying(60) NOT NULL,
    status character varying(10) NOT NULL,
    rows_affected integer,
    duration_ms integer,
    error_message text,
    CONSTRAINT chk_etl_log_status CHECK (((status)::text = ANY ((ARRAY['SUCCESS'::character varying, 'FAILED'::character varying, 'PARTIAL'::character varying])::text[])))
);


--
-- Name: etl_log_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.etl_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: etl_log_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.etl_log_id_seq OWNED BY dwh.etl_log.id;


--
-- Name: etl_watermark; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.etl_watermark (
    table_name character varying(60) NOT NULL,
    last_year smallint,
    last_month smallint,
    last_run_at timestamp with time zone
);


--
-- Name: fact_fundraising_monthly; Type: TABLE; Schema: dwh; Owner: -
--

CREATE TABLE dwh.fact_fundraising_monthly (
    id bigint CONSTRAINT fact_penerimaan_monthly_id_not_null NOT NULL,
    fund_year smallint CONSTRAINT fact_penerimaan_monthly_fund_year_not_null NOT NULL,
    fund_month smallint CONSTRAINT fact_penerimaan_monthly_fund_month_not_null NOT NULL,
    donorkey bigint CONSTRAINT fact_penerimaan_monthly_donorkey_not_null NOT NULL,
    channel_accountno character varying(30),
    channel_accountname character varying(50),
    productname character varying(60),
    total_amount numeric(18,2) DEFAULT 0 CONSTRAINT fact_penerimaan_monthly_total_amount_not_null NOT NULL,
    count_transaksi integer DEFAULT 0 CONSTRAINT fact_penerimaan_monthly_count_transaksi_not_null NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() CONSTRAINT fact_penerimaan_monthly_refreshed_at_not_null NOT NULL,
    branch_key integer,
    fund_entity smallint,
    CONSTRAINT fact_penerimaan_monthly_fund_month_check CHECK (((fund_month >= 1) AND (fund_month <= 12)))
);


--
-- Name: fact_penerimaan_monthly_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.fact_penerimaan_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fact_penerimaan_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.fact_penerimaan_monthly_id_seq OWNED BY dwh.fact_fundraising_monthly.id;


--
-- Name: fund_monthly_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.fund_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fund_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.fund_monthly_id_seq OWNED BY dwh.dm_fund_monthly.id;


--
-- Name: memo_realisasi_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.memo_realisasi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: memo_realisasi_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.memo_realisasi_id_seq OWNED BY dwh.dm_program_memo.id;


--
-- Name: otorisasi_summary_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.otorisasi_summary_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: otorisasi_summary_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.otorisasi_summary_id_seq OWNED BY dwh.dm_authorization_summary.id;


--
-- Name: saldo_rekening_id_seq; Type: SEQUENCE; Schema: dwh; Owner: -
--

CREATE SEQUENCE dwh.saldo_rekening_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: saldo_rekening_id_seq; Type: SEQUENCE OWNED BY; Schema: dwh; Owner: -
--

ALTER SEQUENCE dwh.saldo_rekening_id_seq OWNED BY dwh.dm_account_balance.id;


--
-- Name: dim_branch branch_key; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dim_branch ALTER COLUMN branch_key SET DEFAULT nextval('dwh.dim_cabang_cabang_key_seq'::regclass);


--
-- Name: dim_donor donorkey; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dim_donor ALTER COLUMN donorkey SET DEFAULT nextval('dwh.dim_donatur_donorkey_seq'::regclass);


--
-- Name: dm_account_balance id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_account_balance ALTER COLUMN id SET DEFAULT nextval('dwh.saldo_rekening_id_seq'::regclass);


--
-- Name: dm_asnaf_monthly id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_asnaf_monthly ALTER COLUMN id SET DEFAULT nextval('dwh.asnaf_monthly_id_seq'::regclass);


--
-- Name: dm_authorization_summary id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_authorization_summary ALTER COLUMN id SET DEFAULT nextval('dwh.otorisasi_summary_id_seq'::regclass);


--
-- Name: dm_budget_realization id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_budget_realization ALTER COLUMN id SET DEFAULT nextval('dwh.anggaran_realisasi_id_seq'::regclass);


--
-- Name: dm_dist_monthly id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_dist_monthly ALTER COLUMN id SET DEFAULT nextval('dwh.dist_monthly_id_seq'::regclass);


--
-- Name: dm_donor_monthly id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_donor_monthly ALTER COLUMN id SET DEFAULT nextval('dwh.donatur_monthly_id_seq'::regclass);


--
-- Name: dm_fund_monthly id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_fund_monthly ALTER COLUMN id SET DEFAULT nextval('dwh.fund_monthly_id_seq'::regclass);


--
-- Name: dm_program_memo id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_program_memo ALTER COLUMN id SET DEFAULT nextval('dwh.memo_realisasi_id_seq'::regclass);


--
-- Name: etl_log id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.etl_log ALTER COLUMN id SET DEFAULT nextval('dwh.etl_log_id_seq'::regclass);


--
-- Name: fact_fundraising_monthly id; Type: DEFAULT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.fact_fundraising_monthly ALTER COLUMN id SET DEFAULT nextval('dwh.fact_penerimaan_monthly_id_seq'::regclass);


--
-- Name: dm_budget_realization anggaran_realisasi_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_budget_realization
    ADD CONSTRAINT anggaran_realisasi_pkey PRIMARY KEY (id);


--
-- Name: dm_asnaf_monthly asnaf_monthly_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_asnaf_monthly
    ADD CONSTRAINT asnaf_monthly_pkey PRIMARY KEY (id);


--
-- Name: dim_branch dim_cabang_kode_cabang_key; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dim_branch
    ADD CONSTRAINT dim_cabang_kode_cabang_key UNIQUE (branch_code);


--
-- Name: dim_branch dim_cabang_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dim_branch
    ADD CONSTRAINT dim_cabang_pkey PRIMARY KEY (branch_key);


--
-- Name: dim_donor dim_donatur_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dim_donor
    ADD CONSTRAINT dim_donatur_pkey PRIMARY KEY (donorkey);


--
-- Name: dim_fund_type dim_fund_type_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dim_fund_type
    ADD CONSTRAINT dim_fund_type_pkey PRIMARY KEY (fund_entity_code);


--
-- Name: dm_dist_monthly dist_monthly_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_dist_monthly
    ADD CONSTRAINT dist_monthly_pkey PRIMARY KEY (id);


--
-- Name: dm_donor_monthly donatur_monthly_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_donor_monthly
    ADD CONSTRAINT donatur_monthly_pkey PRIMARY KEY (id);


--
-- Name: etl_log etl_log_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.etl_log
    ADD CONSTRAINT etl_log_pkey PRIMARY KEY (id);


--
-- Name: etl_watermark etl_watermark_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.etl_watermark
    ADD CONSTRAINT etl_watermark_pkey PRIMARY KEY (table_name);


--
-- Name: fact_fundraising_monthly fact_penerimaan_monthly_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.fact_fundraising_monthly
    ADD CONSTRAINT fact_penerimaan_monthly_pkey PRIMARY KEY (id);


--
-- Name: dm_fund_monthly fund_monthly_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_fund_monthly
    ADD CONSTRAINT fund_monthly_pkey PRIMARY KEY (id);


--
-- Name: dm_program_memo memo_realisasi_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_program_memo
    ADD CONSTRAINT memo_realisasi_pkey PRIMARY KEY (id);


--
-- Name: dm_authorization_summary otorisasi_summary_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_authorization_summary
    ADD CONSTRAINT otorisasi_summary_pkey PRIMARY KEY (id);


--
-- Name: dm_account_balance saldo_rekening_pkey; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_account_balance
    ADD CONSTRAINT saldo_rekening_pkey PRIMARY KEY (id);


--
-- Name: dim_donor uq_dim_donatur_donorid; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dim_donor
    ADD CONSTRAINT uq_dim_donatur_donorid UNIQUE (donorid);


--
-- Name: dm_program_memo uq_memo_realisasi_id; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_program_memo
    ADD CONSTRAINT uq_memo_realisasi_id UNIQUE (realmemoid);


--
-- Name: dm_account_balance uq_saldo_rekening_accountno; Type: CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.dm_account_balance
    ADD CONSTRAINT uq_saldo_rekening_accountno UNIQUE (accountno);


--
-- Name: ix_anggaran_realisasi_cabang; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_anggaran_realisasi_cabang ON dwh.dm_budget_realization USING btree (branch_key, budget_year);


--
-- Name: ix_asnaf_monthly_cabang; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_asnaf_monthly_cabang ON dwh.dm_asnaf_monthly USING btree (branch_key, realization_year, realization_month);


--
-- Name: ix_dist_monthly_cabang; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_dist_monthly_cabang ON dwh.dm_dist_monthly USING btree (branch_key, dist_year, dist_month);


--
-- Name: ix_dm_dist_monthly_fund_entity; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_dm_dist_monthly_fund_entity ON dwh.dm_dist_monthly USING btree (fund_entity, dist_year, dist_month);


--
-- Name: ix_dm_fund_monthly_fund_entity; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_dm_fund_monthly_fund_entity ON dwh.dm_fund_monthly USING btree (fund_entity, fund_year, fund_month);


--
-- Name: ix_donatur_monthly_cabang; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_donatur_monthly_cabang ON dwh.dm_donor_monthly USING btree (branch_key, fund_year, fund_month);


--
-- Name: ix_etl_log_run_at; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_etl_log_run_at ON dwh.etl_log USING btree (run_at DESC);


--
-- Name: ix_etl_log_table; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_etl_log_table ON dwh.etl_log USING btree (table_name, run_at DESC);


--
-- Name: ix_fact_fundraising_fund_entity; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_fact_fundraising_fund_entity ON dwh.fact_fundraising_monthly USING btree (fund_entity, fund_year, fund_month);


--
-- Name: ix_fact_penerimaan_donorkey; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_fact_penerimaan_donorkey ON dwh.fact_fundraising_monthly USING btree (donorkey);


--
-- Name: ix_fact_penerimaan_monthly_cabang; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_fact_penerimaan_monthly_cabang ON dwh.fact_fundraising_monthly USING btree (branch_key, fund_year, fund_month);


--
-- Name: ix_fund_monthly_cabang; Type: INDEX; Schema: dwh; Owner: -
--

CREATE INDEX ix_fund_monthly_cabang ON dwh.dm_fund_monthly USING btree (branch_key, fund_year, fund_month);


--
-- Name: uix_anggaran_realisasi; Type: INDEX; Schema: dwh; Owner: -
--

CREATE UNIQUE INDEX uix_anggaran_realisasi ON dwh.dm_budget_realization USING btree (budget_year, ownerid, COALESCE(branch_key, 0));


--
-- Name: uix_asnaf_monthly; Type: INDEX; Schema: dwh; Owner: -
--

CREATE UNIQUE INDEX uix_asnaf_monthly ON dwh.dm_asnaf_monthly USING btree (realization_year, realization_month, ashnaf_code, COALESCE(branch_key, 0));


--
-- Name: uix_dm_dist_monthly; Type: INDEX; Schema: dwh; Owner: -
--

CREATE UNIQUE INDEX uix_dm_dist_monthly ON dwh.dm_dist_monthly USING btree (dist_year, dist_month, COALESCE(accountno, ''::character varying), COALESCE(productname, ''::character varying), COALESCE((fund_entity)::integer, 0), COALESCE(branch_key, 0));


--
-- Name: uix_dm_fund_monthly; Type: INDEX; Schema: dwh; Owner: -
--

CREATE UNIQUE INDEX uix_dm_fund_monthly ON dwh.dm_fund_monthly USING btree (fund_year, fund_month, accountno, fund_entity, COALESCE(branch_key, 0));


--
-- Name: uix_donatur_monthly; Type: INDEX; Schema: dwh; Owner: -
--

CREATE UNIQUE INDEX uix_donatur_monthly ON dwh.dm_donor_monthly USING btree (fund_year, fund_month, COALESCE(branch_key, 0));


--
-- Name: uix_fact_fundraising_monthly; Type: INDEX; Schema: dwh; Owner: -
--

CREATE UNIQUE INDEX uix_fact_fundraising_monthly ON dwh.fact_fundraising_monthly USING btree (fund_year, fund_month, donorkey, COALESCE(channel_accountno, ''::character varying), COALESCE(productname, ''::character varying), COALESCE((fund_entity)::integer, 0));


--
-- Name: fact_fundraising_monthly fact_penerimaan_monthly_donorkey_fkey; Type: FK CONSTRAINT; Schema: dwh; Owner: -
--

ALTER TABLE ONLY dwh.fact_fundraising_monthly
    ADD CONSTRAINT fact_penerimaan_monthly_donorkey_fkey FOREIGN KEY (donorkey) REFERENCES dwh.dim_donor(donorkey);


--
-- PostgreSQL database dump complete
--

\unrestrict 0KydJNq0qZDMxngVPpxF19dr1GdLBNsOXEFgjWHDHmOcKkJfzmYfOKxXyORScju

