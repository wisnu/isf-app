--
-- PostgreSQL database dump
--

\restrict c3ONBNGOP5XbWeXVx1Cp5BsGcgYpMRi7LdgxuUA60uqvlFwQqaFxMv95JruJarn

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
-- Name: datamart; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA datamart;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: anggaran_realisasi; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.anggaran_realisasi (
    id bigint NOT NULL,
    budget_year smallint NOT NULL,
    ownerid integer NOT NULL,
    ownername character varying(100),
    anggaran numeric(18,2) DEFAULT 0 NOT NULL,
    realisasi numeric(18,2) DEFAULT 0 NOT NULL,
    pct_realisasi numeric(6,1) DEFAULT 0 NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer
);


--
-- Name: anggaran_realisasi_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.anggaran_realisasi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: anggaran_realisasi_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.anggaran_realisasi_id_seq OWNED BY datamart.anggaran_realisasi.id;


--
-- Name: asnaf_monthly; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.asnaf_monthly (
    id bigint NOT NULL,
    realization_year smallint NOT NULL,
    realization_month smallint NOT NULL,
    ashnaf_code character varying(1) NOT NULL,
    ashnaf_name character varying(50),
    count_ashnaf integer DEFAULT 0 NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer,
    CONSTRAINT asnaf_monthly_realization_month_check CHECK (((realization_month >= 1) AND (realization_month <= 12)))
);


--
-- Name: asnaf_monthly_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.asnaf_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: asnaf_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.asnaf_monthly_id_seq OWNED BY datamart.asnaf_monthly.id;


--
-- Name: dim_cabang; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.dim_cabang (
    cabang_key integer NOT NULL,
    kode_cabang character varying(20) NOT NULL,
    nama_cabang character varying(60),
    tipe_cabang character varying(2),
    status_cabang character varying(1),
    kode_cabang_induk character varying(20),
    kode_wilayah character varying(3),
    level_cabang smallint,
    status_aktif character varying(1),
    tanggal_input timestamp with time zone,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: dim_cabang_cabang_key_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.dim_cabang_cabang_key_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dim_cabang_cabang_key_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.dim_cabang_cabang_key_seq OWNED BY datamart.dim_cabang.cabang_key;


--
-- Name: dim_donatur; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.dim_donatur (
    donorkey bigint NOT NULL,
    donorid integer NOT NULL,
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
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: dim_donatur_donorkey_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.dim_donatur_donorkey_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dim_donatur_donorkey_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.dim_donatur_donorkey_seq OWNED BY datamart.dim_donatur.donorkey;


--
-- Name: dist_monthly; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.dist_monthly (
    id bigint NOT NULL,
    dist_year smallint NOT NULL,
    dist_month smallint NOT NULL,
    accountno character varying(30),
    accountname character varying(50),
    productname character varying(60),
    dist_amount numeric(18,2) DEFAULT 0 NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer,
    CONSTRAINT dist_monthly_dist_month_check CHECK (((dist_month >= 1) AND (dist_month <= 12)))
);


--
-- Name: dist_monthly_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.dist_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: dist_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.dist_monthly_id_seq OWNED BY datamart.dist_monthly.id;


--
-- Name: donatur_monthly; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.donatur_monthly (
    id bigint NOT NULL,
    fund_year smallint NOT NULL,
    fund_month smallint NOT NULL,
    donatur_aktif integer DEFAULT 0 NOT NULL,
    donatur_individu integer DEFAULT 0 NOT NULL,
    donatur_korporat integer DEFAULT 0 NOT NULL,
    donatur_baru integer DEFAULT 0 NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer,
    CONSTRAINT donatur_monthly_fund_month_check CHECK (((fund_month >= 1) AND (fund_month <= 12)))
);


--
-- Name: donatur_monthly_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.donatur_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: donatur_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.donatur_monthly_id_seq OWNED BY datamart.donatur_monthly.id;


--
-- Name: etl_log; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.etl_log (
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
-- Name: etl_log_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.etl_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: etl_log_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.etl_log_id_seq OWNED BY datamart.etl_log.id;


--
-- Name: etl_watermark; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.etl_watermark (
    table_name character varying(60) NOT NULL,
    last_year smallint,
    last_month smallint,
    last_run_at timestamp with time zone
);


--
-- Name: fact_penerimaan_monthly; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.fact_penerimaan_monthly (
    id bigint NOT NULL,
    fund_year smallint NOT NULL,
    fund_month smallint NOT NULL,
    donorkey bigint NOT NULL,
    channel_accountno character varying(30),
    channel_accountname character varying(50),
    productname character varying(60),
    total_amount numeric(18,2) DEFAULT 0 NOT NULL,
    count_transaksi integer DEFAULT 0 NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer,
    CONSTRAINT fact_penerimaan_monthly_fund_month_check CHECK (((fund_month >= 1) AND (fund_month <= 12)))
);


--
-- Name: fact_penerimaan_monthly_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.fact_penerimaan_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fact_penerimaan_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.fact_penerimaan_monthly_id_seq OWNED BY datamart.fact_penerimaan_monthly.id;


--
-- Name: fund_monthly; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.fund_monthly (
    id bigint NOT NULL,
    fund_year smallint NOT NULL,
    fund_month smallint NOT NULL,
    accountno character varying(30),
    accountname character varying(50),
    fund_amount numeric(18,2) DEFAULT 0 NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer,
    CONSTRAINT fund_monthly_fund_month_check CHECK (((fund_month >= 1) AND (fund_month <= 12)))
);


--
-- Name: fund_monthly_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.fund_monthly_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fund_monthly_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.fund_monthly_id_seq OWNED BY datamart.fund_monthly.id;


--
-- Name: memo_realisasi; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.memo_realisasi (
    id bigint NOT NULL,
    realmemoid integer NOT NULL,
    realmemonumber character varying(100),
    realmemosubject character varying(100),
    realmemoamount numeric(18,2),
    realizationmemotype character varying(1),
    realmemodate date,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer
);


--
-- Name: memo_realisasi_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.memo_realisasi_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: memo_realisasi_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.memo_realisasi_id_seq OWNED BY datamart.memo_realisasi.id;


--
-- Name: otorisasi_summary; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.otorisasi_summary (
    id bigint NOT NULL,
    pending_count integer DEFAULT 0 NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer
);


--
-- Name: otorisasi_summary_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.otorisasi_summary_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: otorisasi_summary_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.otorisasi_summary_id_seq OWNED BY datamart.otorisasi_summary.id;


--
-- Name: saldo_rekening; Type: TABLE; Schema: datamart; Owner: -
--

CREATE TABLE datamart.saldo_rekening (
    id bigint NOT NULL,
    accountno character varying(30) NOT NULL,
    accountname character varying(50),
    cashaccounttype character varying(1),
    bankname character varying(100),
    balance numeric(18,2) DEFAULT 0 NOT NULL,
    refreshed_at timestamp with time zone DEFAULT now() NOT NULL,
    cabang_key integer
);


--
-- Name: saldo_rekening_id_seq; Type: SEQUENCE; Schema: datamart; Owner: -
--

CREATE SEQUENCE datamart.saldo_rekening_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: saldo_rekening_id_seq; Type: SEQUENCE OWNED BY; Schema: datamart; Owner: -
--

ALTER SEQUENCE datamart.saldo_rekening_id_seq OWNED BY datamart.saldo_rekening.id;


--
-- Name: anggaran_realisasi id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.anggaran_realisasi ALTER COLUMN id SET DEFAULT nextval('datamart.anggaran_realisasi_id_seq'::regclass);


--
-- Name: asnaf_monthly id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.asnaf_monthly ALTER COLUMN id SET DEFAULT nextval('datamart.asnaf_monthly_id_seq'::regclass);


--
-- Name: dim_cabang cabang_key; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.dim_cabang ALTER COLUMN cabang_key SET DEFAULT nextval('datamart.dim_cabang_cabang_key_seq'::regclass);


--
-- Name: dim_donatur donorkey; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.dim_donatur ALTER COLUMN donorkey SET DEFAULT nextval('datamart.dim_donatur_donorkey_seq'::regclass);


--
-- Name: dist_monthly id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.dist_monthly ALTER COLUMN id SET DEFAULT nextval('datamart.dist_monthly_id_seq'::regclass);


--
-- Name: donatur_monthly id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.donatur_monthly ALTER COLUMN id SET DEFAULT nextval('datamart.donatur_monthly_id_seq'::regclass);


--
-- Name: etl_log id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.etl_log ALTER COLUMN id SET DEFAULT nextval('datamart.etl_log_id_seq'::regclass);


--
-- Name: fact_penerimaan_monthly id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.fact_penerimaan_monthly ALTER COLUMN id SET DEFAULT nextval('datamart.fact_penerimaan_monthly_id_seq'::regclass);


--
-- Name: fund_monthly id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.fund_monthly ALTER COLUMN id SET DEFAULT nextval('datamart.fund_monthly_id_seq'::regclass);


--
-- Name: memo_realisasi id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.memo_realisasi ALTER COLUMN id SET DEFAULT nextval('datamart.memo_realisasi_id_seq'::regclass);


--
-- Name: otorisasi_summary id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.otorisasi_summary ALTER COLUMN id SET DEFAULT nextval('datamart.otorisasi_summary_id_seq'::regclass);


--
-- Name: saldo_rekening id; Type: DEFAULT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.saldo_rekening ALTER COLUMN id SET DEFAULT nextval('datamart.saldo_rekening_id_seq'::regclass);


--
-- Name: anggaran_realisasi anggaran_realisasi_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.anggaran_realisasi
    ADD CONSTRAINT anggaran_realisasi_pkey PRIMARY KEY (id);


--
-- Name: asnaf_monthly asnaf_monthly_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.asnaf_monthly
    ADD CONSTRAINT asnaf_monthly_pkey PRIMARY KEY (id);


--
-- Name: dim_cabang dim_cabang_kode_cabang_key; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.dim_cabang
    ADD CONSTRAINT dim_cabang_kode_cabang_key UNIQUE (kode_cabang);


--
-- Name: dim_cabang dim_cabang_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.dim_cabang
    ADD CONSTRAINT dim_cabang_pkey PRIMARY KEY (cabang_key);


--
-- Name: dim_donatur dim_donatur_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.dim_donatur
    ADD CONSTRAINT dim_donatur_pkey PRIMARY KEY (donorkey);


--
-- Name: dist_monthly dist_monthly_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.dist_monthly
    ADD CONSTRAINT dist_monthly_pkey PRIMARY KEY (id);


--
-- Name: donatur_monthly donatur_monthly_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.donatur_monthly
    ADD CONSTRAINT donatur_monthly_pkey PRIMARY KEY (id);


--
-- Name: etl_log etl_log_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.etl_log
    ADD CONSTRAINT etl_log_pkey PRIMARY KEY (id);


--
-- Name: etl_watermark etl_watermark_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.etl_watermark
    ADD CONSTRAINT etl_watermark_pkey PRIMARY KEY (table_name);


--
-- Name: fact_penerimaan_monthly fact_penerimaan_monthly_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.fact_penerimaan_monthly
    ADD CONSTRAINT fact_penerimaan_monthly_pkey PRIMARY KEY (id);


--
-- Name: fund_monthly fund_monthly_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.fund_monthly
    ADD CONSTRAINT fund_monthly_pkey PRIMARY KEY (id);


--
-- Name: memo_realisasi memo_realisasi_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.memo_realisasi
    ADD CONSTRAINT memo_realisasi_pkey PRIMARY KEY (id);


--
-- Name: otorisasi_summary otorisasi_summary_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.otorisasi_summary
    ADD CONSTRAINT otorisasi_summary_pkey PRIMARY KEY (id);


--
-- Name: saldo_rekening saldo_rekening_pkey; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.saldo_rekening
    ADD CONSTRAINT saldo_rekening_pkey PRIMARY KEY (id);


--
-- Name: dim_donatur uq_dim_donatur_donorid; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.dim_donatur
    ADD CONSTRAINT uq_dim_donatur_donorid UNIQUE (donorid);


--
-- Name: memo_realisasi uq_memo_realisasi_id; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.memo_realisasi
    ADD CONSTRAINT uq_memo_realisasi_id UNIQUE (realmemoid);


--
-- Name: saldo_rekening uq_saldo_rekening_accountno; Type: CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.saldo_rekening
    ADD CONSTRAINT uq_saldo_rekening_accountno UNIQUE (accountno);


--
-- Name: ix_anggaran_realisasi_cabang; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_anggaran_realisasi_cabang ON datamart.anggaran_realisasi USING btree (cabang_key, budget_year);


--
-- Name: ix_asnaf_monthly_cabang; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_asnaf_monthly_cabang ON datamart.asnaf_monthly USING btree (cabang_key, realization_year, realization_month);


--
-- Name: ix_dist_monthly_cabang; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_dist_monthly_cabang ON datamart.dist_monthly USING btree (cabang_key, dist_year, dist_month);


--
-- Name: ix_donatur_monthly_cabang; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_donatur_monthly_cabang ON datamart.donatur_monthly USING btree (cabang_key, fund_year, fund_month);


--
-- Name: ix_etl_log_run_at; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_etl_log_run_at ON datamart.etl_log USING btree (run_at DESC);


--
-- Name: ix_etl_log_table; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_etl_log_table ON datamart.etl_log USING btree (table_name, run_at DESC);


--
-- Name: ix_fact_penerimaan_donorkey; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_fact_penerimaan_donorkey ON datamart.fact_penerimaan_monthly USING btree (donorkey);


--
-- Name: ix_fact_penerimaan_monthly_cabang; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_fact_penerimaan_monthly_cabang ON datamart.fact_penerimaan_monthly USING btree (cabang_key, fund_year, fund_month);


--
-- Name: ix_fund_monthly_cabang; Type: INDEX; Schema: datamart; Owner: -
--

CREATE INDEX ix_fund_monthly_cabang ON datamart.fund_monthly USING btree (cabang_key, fund_year, fund_month);


--
-- Name: uix_anggaran_realisasi; Type: INDEX; Schema: datamart; Owner: -
--

CREATE UNIQUE INDEX uix_anggaran_realisasi ON datamart.anggaran_realisasi USING btree (budget_year, ownerid, COALESCE(cabang_key, 0));


--
-- Name: uix_asnaf_monthly; Type: INDEX; Schema: datamart; Owner: -
--

CREATE UNIQUE INDEX uix_asnaf_monthly ON datamart.asnaf_monthly USING btree (realization_year, realization_month, ashnaf_code, COALESCE(cabang_key, 0));


--
-- Name: uix_dist_monthly; Type: INDEX; Schema: datamart; Owner: -
--

CREATE UNIQUE INDEX uix_dist_monthly ON datamart.dist_monthly USING btree (dist_year, dist_month, accountno, productname, COALESCE(cabang_key, 0));


--
-- Name: uix_donatur_monthly; Type: INDEX; Schema: datamart; Owner: -
--

CREATE UNIQUE INDEX uix_donatur_monthly ON datamart.donatur_monthly USING btree (fund_year, fund_month, COALESCE(cabang_key, 0));


--
-- Name: uix_fact_penerimaan_monthly; Type: INDEX; Schema: datamart; Owner: -
--

CREATE UNIQUE INDEX uix_fact_penerimaan_monthly ON datamart.fact_penerimaan_monthly USING btree (fund_year, fund_month, donorkey, channel_accountno, productname, COALESCE(cabang_key, 0));


--
-- Name: uix_fund_monthly; Type: INDEX; Schema: datamart; Owner: -
--

CREATE UNIQUE INDEX uix_fund_monthly ON datamart.fund_monthly USING btree (fund_year, fund_month, accountno, COALESCE(cabang_key, 0));


--
-- Name: fact_penerimaan_monthly fact_penerimaan_monthly_donorkey_fkey; Type: FK CONSTRAINT; Schema: datamart; Owner: -
--

ALTER TABLE ONLY datamart.fact_penerimaan_monthly
    ADD CONSTRAINT fact_penerimaan_monthly_donorkey_fkey FOREIGN KEY (donorkey) REFERENCES datamart.dim_donatur(donorkey);


--
-- PostgreSQL database dump complete
--

\unrestrict c3ONBNGOP5XbWeXVx1Cp5BsGcgYpMRi7LdgxuUA60uqvlFwQqaFxMv95JruJarn

