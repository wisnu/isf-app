--
-- PostgreSQL database dump
--

\restrict V5aqvig4dGypZstXReMn6jJFynAlG1jjSttvgqFcFCyepbweLHeUKnQrjsrchN3

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
-- Name: accounting; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA accounting;


ALTER SCHEMA accounting OWNER TO postgres;

--
-- Name: dashboard; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA dashboard;


ALTER SCHEMA dashboard OWNER TO postgres;

--
-- Name: enterprise; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA enterprise;


ALTER SCHEMA enterprise OWNER TO postgres;

--
-- Name: fund; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA fund;


ALTER SCHEMA fund OWNER TO postgres;

--
-- Name: migration; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA migration;


ALTER SCHEMA migration OWNER TO postgres;

--
-- Name: personalia; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA personalia;


ALTER SCHEMA personalia OWNER TO postgres;

--
-- Name: program; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA program;


ALTER SCHEMA program OWNER TO postgres;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: school; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA school;


ALTER SCHEMA school OWNER TO postgres;

--
-- Name: transaction; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA transaction;


ALTER SCHEMA transaction OWNER TO postgres;

--
-- Name: history; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.history AS (
	created_by integer,
	created_stamp timestamp(0) without time zone,
	created_db_user character varying(20),
	created_ip inet,
	updated_by integer,
	updated_stamp timestamp(6) without time zone,
	updated_db_user character varying(20),
	updated_ip inet
);


ALTER TYPE public.history OWNER TO postgres;

--
-- Name: yesno; Type: DOMAIN; Schema: public; Owner: postgres
--

CREATE DOMAIN public.yesno AS boolean;


ALTER DOMAIN public.yesno OWNER TO postgres;

--
-- Name: indonesian; Type: TEXT SEARCH CONFIGURATION; Schema: public; Owner: postgres
--

CREATE TEXT SEARCH CONFIGURATION public.indonesian (
    PARSER = pg_catalog."default" );

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR word WITH english_stem;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR numword WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR email WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR url WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR host WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR sfloat WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR version WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR hword_numpart WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR hword_part WITH english_stem;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR hword_asciipart WITH english_stem;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR numhword WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR asciihword WITH english_stem;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR hword WITH english_stem;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR url_path WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR file WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR "float" WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR "int" WITH simple;

ALTER TEXT SEARCH CONFIGURATION public.indonesian
    ADD MAPPING FOR uint WITH simple;


ALTER TEXT SEARCH CONFIGURATION public.indonesian OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.account (
    account_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    account_name character varying(100) DEFAULT NULL::character varying,
    account_level integer,
    is_detail character varying(1) DEFAULT NULL::character varying,
    account_type character varying(1) DEFAULT NULL::character varying,
    is_system character varying(1) DEFAULT NULL::character varying,
    userid_last_modified character varying(20) DEFAULT NULL::character varying,
    time_last_modified timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    fl_parent_account character varying(20) DEFAULT NULL::character varying,
    userid_create character varying(20) DEFAULT NULL::character varying,
    time_create timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    balance double precision,
    fl_cpa_accountcode character varying(20) DEFAULT NULL::character varying,
    fl_lpa_accountcode character varying(20) DEFAULT NULL::character varying,
    isactivaoffbalancesheet character varying(1) DEFAULT NULL::character varying,
    isrpvrakreportshow character varying(1) DEFAULT NULL::character varying,
    isrpvaccount character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE accounting.account OWNER TO postgres;

--
-- Name: account_off_bs; Type: VIEW; Schema: accounting; Owner: postgres
--

CREATE VIEW accounting.account_off_bs AS
 SELECT account_code,
    account_name,
    account_level,
    is_detail,
    account_type,
    is_system,
    userid_last_modified,
    time_last_modified,
    fl_parent_account,
    userid_create,
    time_create,
    balance,
    fl_cpa_accountcode,
    fl_lpa_accountcode,
    isactivaoffbalancesheet,
    isrpvrakreportshow,
    isrpvaccount
   FROM accounting.account
  WHERE ((account_type)::text = 'M'::text);


ALTER VIEW accounting.account_off_bs OWNER TO postgres;

--
-- Name: accountdetail; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountdetail (
    fl_account character varying(20) DEFAULT NULL::character varying NOT NULL,
    fl_detail_account character varying(20) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE accounting.accountdetail OWNER TO postgres;

--
-- Name: accountgroup; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountgroup (
    accountgroup_code character varying(5) DEFAULT NULL::character varying,
    accountgroup_name character varying(30) DEFAULT NULL::character varying,
    id integer NOT NULL
);


ALTER TABLE accounting.accountgroup OWNER TO postgres;

--
-- Name: accounthierarchy; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accounthierarchy (
    accounthierarchy_id integer NOT NULL,
    fl_parentaccountcode character varying(20) DEFAULT NULL::character varying,
    fl_childaccountcode character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.accounthierarchy OWNER TO postgres;

--
-- Name: accountingday; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountingday (
    description character varying(100) DEFAULT NULL::character varying,
    periode_status character varying(1) DEFAULT NULL::character varying,
    islastperiod character varying(1) DEFAULT NULL::character varying,
    periode_code integer NOT NULL,
    fl_accountingperiode integer NOT NULL,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying NOT NULL,
    datevalue timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    isworkday character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE accounting.accountingday OWNER TO postgres;

--
-- Name: accountingperiode; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountingperiode (
    fl_accountingyear character varying(4) DEFAULT NULL::character varying NOT NULL,
    periode_code integer NOT NULL,
    description character varying(100) DEFAULT NULL::character varying,
    periode_status character varying(1) DEFAULT NULL::character varying,
    is_lastyearperiode character varying(1) DEFAULT NULL::character varying,
    pcode_accday_end integer,
    pcode_accday_start integer,
    fl_accountingperiode_start integer,
    fl_accountingyear_start character varying(4) DEFAULT NULL::character varying
);


ALTER TABLE accounting.accountingperiode OWNER TO postgres;

--
-- Name: accountingyear; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountingyear (
    periode_code character varying(4) DEFAULT NULL::character varying NOT NULL,
    description character varying(100) DEFAULT NULL::character varying,
    periode_status character varying(1) DEFAULT NULL::character varying,
    fl_current_periode integer,
    pcode_accper_end integer,
    pcode_accper_start integer,
    fl_accountingyear_start character varying(4) DEFAULT NULL::character varying
);


ALTER TABLE accounting.accountingyear OWNER TO postgres;

--
-- Name: accountinstance; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountinstance (
    accountinstance_id integer NOT NULL,
    balance double precision,
    fl_cpa_accountinstance integer,
    fl_lpa_accountinstance integer,
    balance_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    isbolehinput character varying(1) DEFAULT NULL::character varying,
    branch_code character varying(5) DEFAULT NULL::character varying,
    account_code character varying(20) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying,
    dailybalance_id integer,
    periodebalance_id integer,
    dailyprojectbalance_id integer,
    periodeprojectbalance_id integer
);


ALTER TABLE accounting.accountinstance OWNER TO postgres;

--
-- Name: accountinstance_neraca; Type: VIEW; Schema: accounting; Owner: postgres
--

CREATE VIEW accounting.accountinstance_neraca AS
 SELECT ai.accountinstance_id,
    ai.account_code,
    ai.branch_code,
    ai.currency_code,
    a.account_name,
    a.account_type,
    a.account_level,
    a.is_detail,
    a.fl_parent_account
   FROM accounting.accountinstance ai,
    accounting.account a
  WHERE (((ai.account_code)::text = (a.account_code)::text) AND ((a.account_type)::text = ANY (ARRAY[('A'::character varying)::text, ('L'::character varying)::text, ('E'::character varying)::text])));


ALTER VIEW accounting.accountinstance_neraca OWNER TO postgres;

--
-- Name: accountinterface; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountinterface (
    interface_code character varying(10) DEFAULT NULL::character varying NOT NULL,
    account_code character varying(20) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    interface_type character varying(1) DEFAULT NULL::character varying,
    is_active character varying(1) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.accountinterface OWNER TO postgres;

--
-- Name: accountinterfacemember; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountinterfacemember (
    member_id integer NOT NULL,
    interface_code character varying(10) DEFAULT NULL::character varying,
    account_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.accountinterfacemember OWNER TO postgres;

--
-- Name: accountmanager; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accountmanager (
    amcode character varying(10) DEFAULT NULL::character varying NOT NULL,
    rcno character varying(4) DEFAULT NULL::character varying,
    employeeid character varying(20) DEFAULT NULL::character varying,
    employeename character varying(50) DEFAULT NULL::character varying,
    project_no character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE accounting.accountmanager OWNER TO postgres;

--
-- Name: accsubsystem; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.accsubsystem (
    subsystemcode character varying(20) DEFAULT NULL::character varying NOT NULL,
    titlesubsystem character varying(50) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    servername character varying(30) DEFAULT NULL::character varying,
    username character varying(20) DEFAULT NULL::character varying,
    password character varying(30) DEFAULT NULL::character varying,
    createjournalscriptid character varying(100) DEFAULT NULL::character varying,
    sessionname character varying(30) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    usecurrentlogin character varying(1) DEFAULT NULL::character varying,
    authjournalscriptid character varying(80) DEFAULT NULL::character varying,
    applicationid character varying(80) DEFAULT NULL::character varying,
    oldstylescripting integer
);


ALTER TABLE accounting.accsubsystem OWNER TO postgres;

--
-- Name: blobregistration; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.blobregistration (
    id integer NOT NULL,
    actualfilename character varying(128) DEFAULT NULL::character varying
);


ALTER TABLE accounting.blobregistration OWNER TO postgres;

--
-- Name: cabang; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.cabang (
    kode_cabang character varying(20) DEFAULT NULL::character varying NOT NULL,
    nama_cabang character varying(30) DEFAULT NULL::character varying,
    tipe_cabang character varying(2) DEFAULT NULL::character varying,
    status_cabang character varying(1) DEFAULT NULL::character varying,
    sandi_bi character varying(7) DEFAULT NULL::character varying,
    zona_waktu character varying(2) DEFAULT NULL::character varying,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input character varying(15) DEFAULT NULL::character varying,
    user_otorisasi character varying(20) DEFAULT NULL::character varying,
    tanggal_otorisasi timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_otorisasi character varying(15) DEFAULT NULL::character varying,
    kode_cabang_induk character varying(20) DEFAULT NULL::character varying,
    status_aktif character varying(1) DEFAULT NULL::character varying,
    status_otorisasi character varying(1) DEFAULT NULL::character varying,
    kode_wilayah character varying(3) DEFAULT NULL::character varying,
    kode_kantor character varying(5) DEFAULT NULL::character varying,
    branchid integer,
    kode_singkat character varying(5),
    kode_lokasi character varying(10),
    status_akses character(1),
    id_sandibi integer,
    id_sandilokasi integer,
    level_cabang integer,
    kode_wilayah_kliring character varying(5),
    kantor_alamat character varying(200),
    kantor_kode_pos character varying(5),
    kantor_nama character varying(100),
    kantor_npwp character varying(30),
    kantor_telepon1 character varying(15),
    kantor_telepon2 character varying(15),
    kantor_telepon3 character varying(15),
    kantor_tipe character varying(2)
);


ALTER TABLE enterprise.cabang OWNER TO postgres;

--
-- Name: branchlocation; Type: VIEW; Schema: accounting; Owner: postgres
--

CREATE VIEW accounting.branchlocation AS
 SELECT kode_cabang AS branch_code,
    nama_cabang AS branchname,
        CASE
            WHEN (((tipe_cabang)::text = 'CU'::text) OR ((tipe_cabang)::text = 'PO'::text)) THEN 'B'::text
            ELSE 'S'::text
        END AS branchstatus,
    user_input AS user_id,
    tanggal_input AS last_update,
    kode_cabang_induk AS masterbranch_code,
    0 AS dataid
   FROM enterprise.cabang;


ALTER VIEW accounting.branchlocation OWNER TO postgres;

--
-- Name: branchlocation_old; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.branchlocation_old (
    branch_code character varying(5) DEFAULT NULL::character varying NOT NULL,
    branchname character varying(50) DEFAULT NULL::character varying,
    branchstatus character varying(1) DEFAULT NULL::character varying,
    user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    masterbranch_code character varying(5) DEFAULT NULL::character varying,
    dataid integer
);


ALTER TABLE accounting.branchlocation_old OWNER TO postgres;

--
-- Name: cashflowgroup; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.cashflowgroup (
    cfgroupid integer NOT NULL,
    cfgroupcode character varying(10),
    cfgroupname character varying(100),
    cfgroupdescription character varying(200),
    cfsequencenumber integer,
    cfparentid integer,
    cfgrouplevel integer,
    isdetail character varying(1),
    cfoperationtype character varying(1)
);


ALTER TABLE accounting.cashflowgroup OWNER TO postgres;

--
-- Name: cashflowmember; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.cashflowmember (
    cfmemberid integer NOT NULL,
    cfgroupid integer,
    account_code character varying(20),
    mutationtype character varying(1),
    trancodeexclude character varying(200),
    trancodeinclude character varying(200),
    journalcodeexclude character varying(200),
    journalcodeinclude character varying(200),
    additionalinfo character varying(300)
);


ALTER TABLE accounting.cashflowmember OWNER TO postgres;

--
-- Name: cpalpamapping; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.cpalpamapping (
    fl_lpa_accountcode character varying(20) DEFAULT NULL::character varying,
    fl_cpa_accountcode character varying(20) DEFAULT NULL::character varying,
    cpalpamapping_id integer NOT NULL
);


ALTER TABLE accounting.cpalpamapping OWNER TO postgres;

--
-- Name: currency; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.currency (
    currency_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    description character varying(64) DEFAULT NULL::character varying,
    currentvalue double precision,
    isdefault character varying(1) DEFAULT NULL::character varying,
    isstandard character varying(1) DEFAULT NULL::character varying,
    centralbank_currency_code character varying(20) DEFAULT NULL::character varying,
    short_name character varying(10) DEFAULT NULL::character varying,
    full_name character varying(50) DEFAULT NULL::character varying,
    country_owner character varying(30) DEFAULT NULL::character varying,
    kurs_buku double precision,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_tengah_bi double precision,
    kurs_beli_kantor_pusat double precision,
    kurs_jual_kantor_pusat double precision,
    tanggal_limit timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_otorisasi character varying(20) DEFAULT NULL::character varying,
    tanggal_otorisasi timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_otorisasi character varying(15) DEFAULT NULL::character varying,
    kurs_neraca double precision,
    deviasi_maksimal double precision,
    kurs_reval double precision,
    kurs_remittance double precision,
    symbol character varying(10),
    symbol_says character varying(50)
);


ALTER TABLE accounting.currency OWNER TO postgres;

--
-- Name: currency_pkpu; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.currency_pkpu (
    currency_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    description character varying(64) DEFAULT NULL::character varying,
    currentvalue double precision,
    isdefault character varying(1) DEFAULT NULL::character varying,
    isstandard character varying(1) DEFAULT NULL::character varying,
    centralbank_currency_code character varying(20) DEFAULT NULL::character varying,
    short_name character varying(10) DEFAULT NULL::character varying,
    full_name character varying(50) DEFAULT NULL::character varying,
    country_owner character varying(30) DEFAULT NULL::character varying,
    kurs_buku double precision,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_tengah_bi double precision,
    kurs_beli_kantor_pusat double precision,
    kurs_jual_kantor_pusat double precision,
    tanggal_limit timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_otorisasi character varying(20) DEFAULT NULL::character varying,
    tanggal_otorisasi timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_otorisasi character varying(15) DEFAULT NULL::character varying,
    kurs_neraca double precision,
    deviasi_maksimal double precision,
    kurs_reval double precision,
    kurs_remittance double precision,
    symbol character varying(10),
    symbol_says character varying(50)
);


ALTER TABLE accounting.currency_pkpu OWNER TO postgres;

--
-- Name: custom_idgen; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.custom_idgen (
    idname character varying(30) DEFAULT NULL::character varying NOT NULL,
    idcode character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE accounting.custom_idgen OWNER TO postgres;

--
-- Name: dailybalance; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.dailybalance (
    dailybalance_id integer NOT NULL,
    balance double precision,
    balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balancecumulative double precision,
    balancecumulative_ekuiv double precision,
    datevalue timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    debit double precision,
    credit double precision,
    debit_ekuiv double precision,
    credit_ekuiv double precision,
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying,
    accountinstance_id integer
);


ALTER TABLE accounting.dailybalance OWNER TO postgres;

--
-- Name: dailyprojectbalance; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.dailyprojectbalance (
    dailyprojectbalance_id integer NOT NULL,
    debit double precision,
    credit double precision,
    balance double precision,
    balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balancecumulative double precision,
    balancecumulative_ekuiv double precision,
    datevalue timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    debit_ekuiv double precision,
    credit_ekuiv double precision,
    project_no character varying(10) DEFAULT NULL::character varying,
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying,
    accountinstance_id integer
);


ALTER TABLE accounting.dailyprojectbalance OWNER TO postgres;

--
-- Name: enum_int; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.enum_int (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value integer NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE accounting.enum_int OWNER TO postgres;

--
-- Name: enum_varchar; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.enum_varchar (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value character varying(2) DEFAULT NULL::character varying NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE accounting.enum_varchar OWNER TO postgres;

--
-- Name: fact_daily_balance; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.fact_daily_balance (
    fact_id integer NOT NULL,
    fact_date timestamp without time zone,
    fact_date_fmt character varying(8),
    accountinstance_id integer,
    account_code character varying(20),
    branch_code character varying(5),
    currency_code character varying(5),
    balance double precision,
    balance_ekiv double precision
);


ALTER TABLE accounting.fact_daily_balance OWNER TO postgres;

--
-- Name: hi_permil; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.hi_permil (
    p_year integer,
    p_month integer,
    currency_code character varying(3) DEFAULT NULL::character varying,
    day_number integer,
    amount double precision,
    process_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    id_hipermil integer NOT NULL,
    ekuiv_rate double precision
);


ALTER TABLE accounting.hi_permil OWNER TO postgres;

--
-- Name: hipermildistribution; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.hipermildistribution (
    distribution_id character varying(2) DEFAULT NULL::character varying NOT NULL,
    hipermil_ratio double precision,
    ekuiv_rate_ratio double precision,
    id_hipermil integer NOT NULL
);


ALTER TABLE accounting.hipermildistribution OWNER TO postgres;

--
-- Name: id_gen; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.id_gen (
    id_code character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE accounting.id_gen OWNER TO postgres;

--
-- Name: intrnewtransaction; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.intrnewtransaction (
    subsysteminteraction_id integer NOT NULL,
    dialogid character varying(80) DEFAULT NULL::character varying,
    processingscriptid character varying(80) DEFAULT NULL::character varying,
    numbertag integer,
    servermethodid character varying(80) DEFAULT NULL::character varying
);


ALTER TABLE accounting.intrnewtransaction OWNER TO postgres;

--
-- Name: intrpicktransaction; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.intrpicktransaction (
    subsysteminteraction_id integer NOT NULL,
    dialogid character varying(80) DEFAULT NULL::character varying,
    numbertag integer
);


ALTER TABLE accounting.intrpicktransaction OWNER TO postgres;

--
-- Name: jenisrak; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.jenisrak (
    koderak character varying(30) DEFAULT NULL::character varying NOT NULL,
    deskripsi character varying(50) DEFAULT NULL::character varying,
    accountcode_rakpusat character varying(20) DEFAULT NULL::character varying,
    jenisrak character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE accounting.jenisrak OWNER TO postgres;

--
-- Name: journal; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.journal (
    journal_no character varying(30) DEFAULT NULL::character varying NOT NULL,
    journal_date_posting timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    description character varying(200) DEFAULT NULL::character varying,
    userid_create character varying(20) DEFAULT NULL::character varying,
    userid_last_modified character varying(20) DEFAULT NULL::character varying,
    journal_date_last_modified timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    userid_posting character varying(20) DEFAULT NULL::character varying,
    is_posted character varying(1) DEFAULT NULL::character varying,
    journal_type character varying(10) DEFAULT NULL::character varying,
    journal_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    lastitemno integer,
    status character varying(1) DEFAULT NULL::character varying,
    docoprstatus character varying(1) DEFAULT NULL::character varying,
    is_partlychecked character varying(1) DEFAULT NULL::character varying,
    branch_code character varying(5) DEFAULT NULL::character varying,
    transaction_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    journal_state character varying(1) DEFAULT NULL::character varying,
    serial_no character varying(23) DEFAULT NULL::character varying,
    event_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    lock_userid character varying(20) DEFAULT NULL::character varying,
    fl_origin_journal character varying(30) DEFAULT NULL::character varying,
    id_journalcreation integer,
    source_app character varying(30) DEFAULT NULL::character varying,
    source_app_class character varying(30) DEFAULT NULL::character varying,
    source_app_ref character varying(30) DEFAULT NULL::character varying,
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying
);


ALTER TABLE accounting.journal OWNER TO postgres;

--
-- Name: journalblock; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.journalblock (
    system_id character varying(10) DEFAULT NULL::character varying,
    class_id character varying(32) DEFAULT NULL::character varying,
    key_id integer,
    id_journalblock integer NOT NULL,
    dataid character varying(50) DEFAULT NULL::character varying,
    id_journalcreation integer,
    journal_no character varying(30) DEFAULT NULL::character varying,
    subsystemcode character varying(20) DEFAULT NULL::character varying,
    transaction_tag character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.journalblock OWNER TO postgres;

--
-- Name: journalcode; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.journalcode (
    description character varying(100) DEFAULT NULL::character varying,
    user_input character varying(20) DEFAULT NULL::character varying,
    terminal_input character varying(15) DEFAULT NULL::character varying,
    user_ubah character varying(20) DEFAULT NULL::character varying,
    terminal_ubah character varying(15) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    tanggal_ubah timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    journalcode_id character varying(10) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE accounting.journalcode OWNER TO postgres;

--
-- Name: journaldeletion; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.journaldeletion (
    journal_no character varying(30) DEFAULT NULL::character varying NOT NULL,
    user_id character varying(20) DEFAULT NULL::character varying,
    user_terminal character varying(23) DEFAULT NULL::character varying,
    process_time timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE accounting.journaldeletion OWNER TO postgres;

--
-- Name: journalitem; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.journalitem (
    fl_journal character varying(30) DEFAULT NULL::character varying NOT NULL,
    journalitem_no integer NOT NULL,
    fl_account character varying(20) DEFAULT NULL::character varying,
    amount_debit double precision,
    amount_credit double precision,
    description character varying(200) DEFAULT NULL::character varying,
    branch_code character varying(20) DEFAULT NULL::character varying,
    valuta_code character varying(20) DEFAULT NULL::character varying,
    rc_code character varying(20) DEFAULT NULL::character varying,
    generic_code character varying(20) DEFAULT NULL::character varying,
    fl_posting_account character varying(20) DEFAULT NULL::character varying,
    fl_project_no character varying(10) DEFAULT NULL::character varying,
    docoprstatus character varying(1) DEFAULT NULL::character varying,
    userid_create character varying(20) DEFAULT NULL::character varying,
    userid_last_modified character varying(20) DEFAULT NULL::character varying,
    journalitemstatus character varying(1) DEFAULT NULL::character varying,
    userid_posting character varying(20) DEFAULT NULL::character varying,
    userid_check character varying(20) DEFAULT NULL::character varying,
    dateposting timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    datelastmod timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    datecreate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    event_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    journalitemtype character varying(1) DEFAULT NULL::character varying,
    kode_kurs character varying(20) DEFAULT NULL::character varying,
    nilai_kurs double precision,
    rpv_main integer,
    subsystemcode character varying(20) DEFAULT NULL::character varying,
    subaccountcode character varying(30) DEFAULT NULL::character varying,
    id_journalcreation integer,
    subaccountname character varying(100) DEFAULT NULL::character varying,
    accountinstance_id integer,
    id_journalblock integer,
    transaksirak_id integer,
    source_class_id character varying(32) DEFAULT NULL::character varying,
    source_key_id integer,
    additionaldescription character varying(200)
);


ALTER TABLE accounting.journalitem OWNER TO postgres;

--
-- Name: journalitem_neraca; Type: VIEW; Schema: accounting; Owner: postgres
--

CREATE VIEW accounting.journalitem_neraca AS
 SELECT j.journal_no,
    i.journalitem_no,
    j.journal_date,
        CASE
            WHEN ((a.account_type)::text = ANY (ARRAY[('A'::character varying)::text, ('L'::character varying)::text, ('E'::character varying)::text])) THEN i.accountinstance_id
            ELSE t.fl_cpa_accountinstance
        END AS a_id,
    i.amount_debit,
    i.amount_credit,
    i.id_journalblock,
    i.nilai_kurs,
        CASE
            WHEN ((a.account_type)::text = ANY (ARRAY[('A'::character varying)::text, ('X'::character varying)::text])) THEN (i.amount_debit - i.amount_credit)
            ELSE (i.amount_credit - i.amount_debit)
        END AS net_amount
   FROM accounting.journal j,
    accounting.journalitem i,
    accounting.accountinstance t,
    accounting.account a
  WHERE (((j.journal_no)::text = (i.fl_journal)::text) AND (i.accountinstance_id = t.accountinstance_id) AND ((t.account_code)::text = (a.account_code)::text) AND ((a.account_type)::text = ANY (ARRAY[('A'::character varying)::text, ('L'::character varying)::text, ('E'::character varying)::text, ('I'::character varying)::text, ('X'::character varying)::text])) AND ((j.is_posted)::text = 'T'::text));


ALTER VIEW accounting.journalitem_neraca OWNER TO postgres;

--
-- Name: journalitem_saldodana; Type: VIEW; Schema: accounting; Owner: postgres
--

CREATE VIEW accounting.journalitem_saldodana AS
 SELECT j.journal_no,
    i.journalitem_no,
    j.journal_date,
    t.fl_cpa_accountinstance AS a_id,
    i.amount_debit,
    i.amount_credit,
    i.id_journalblock,
    i.nilai_kurs,
        CASE
            WHEN ((a.account_type)::text = 'X'::text) THEN (i.amount_debit - i.amount_credit)
            ELSE (i.amount_credit - i.amount_debit)
        END AS net_amount
   FROM accounting.journal j,
    accounting.journalitem i,
    accounting.accountinstance t,
    accounting.account a
  WHERE (((j.journal_no)::text = (i.fl_journal)::text) AND (i.accountinstance_id = t.accountinstance_id) AND ((t.account_code)::text = (a.account_code)::text) AND ((a.account_type)::text = ANY (ARRAY[('I'::character varying)::text, ('X'::character varying)::text])) AND ((j.is_posted)::text = 'T'::text));


ALTER VIEW accounting.journalitem_saldodana OWNER TO postgres;

--
-- Name: kurshistory; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.kurshistory (
    kurshistory_id integer NOT NULL,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_beli_kantorpusat double precision,
    kurs_jual_kantorpusat double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_buku double precision,
    kurs_neraca double precision,
    kurs_tengah_bi double precision,
    history_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_ubah character varying(20) DEFAULT NULL::character varying,
    user_otorisasi character varying(20) DEFAULT NULL::character varying,
    terminal_pengubah character varying(15) DEFAULT NULL::character varying,
    terminal_otorisasi character varying(15) DEFAULT NULL::character varying,
    kurs_reval double precision,
    kurs_remittance double precision,
    currency_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.kurshistory OWNER TO postgres;

--
-- Name: mapaccount; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.mapaccount (
    oldaccount character varying(255),
    newaccount character varying(255)
);


ALTER TABLE accounting.mapaccount OWNER TO postgres;

--
-- Name: masterkurs; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.masterkurs (
    kode_kurs character varying(20) DEFAULT NULL::character varying NOT NULL,
    nama_kurs character varying(30) DEFAULT NULL::character varying,
    deskripsi character varying(50) DEFAULT NULL::character varying,
    nama_field_currency character varying(30) DEFAULT NULL::character varying,
    rpv_name character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.masterkurs OWNER TO postgres;

--
-- Name: parameter; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.parameter (
    parametercode character varying(20) DEFAULT NULL::character varying NOT NULL,
    parametervalue double precision,
    description character varying(100) DEFAULT NULL::character varying,
    parameterstringvalue character varying(100) DEFAULT NULL::character varying,
    parameterdatevalue timestamp(6) without time zone
);


ALTER TABLE accounting.parameter OWNER TO postgres;

--
-- Name: parameterglobaltes; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.parameterglobaltes (
    kode_parameter character varying(10),
    tipe_parameter character varying(1),
    nilai_parameter double precision,
    deskripsi character varying(60),
    is_parameter_system character varying(1),
    nilai_parameter_tanggal timestamp(6) without time zone,
    nilai_parameter_string character varying(30),
    tag character varying(15),
    default_code character varying(30)
);


ALTER TABLE accounting.parameterglobaltes OWNER TO postgres;

--
-- Name: periodebalance; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.periodebalance (
    periodebalance_id integer NOT NULL,
    balance double precision,
    balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balancecumulative double precision,
    balancecumulative_ekuiv double precision,
    debit double precision,
    credit double precision,
    debit_ekuiv double precision,
    credit_ekuiv double precision,
    accountinstance_id integer,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying,
    periode_code integer
);


ALTER TABLE accounting.periodebalance OWNER TO postgres;

--
-- Name: periodeprojectbalance; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.periodeprojectbalance (
    periodeprojectbalance_id integer NOT NULL,
    debit double precision,
    credit double precision,
    balance double precision,
    balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balancecumulative double precision,
    balancecumulative_ekuiv double precision,
    debit_ekuiv double precision,
    credit_ekuiv double precision,
    project_no character varying(10) DEFAULT NULL::character varying,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying,
    periode_code integer,
    accountinstance_id integer
);


ALTER TABLE accounting.periodeprojectbalance OWNER TO postgres;

--
-- Name: project; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.project (
    project_no character varying(10) DEFAULT NULL::character varying NOT NULL,
    name character varying(30) DEFAULT NULL::character varying,
    description character varying(255) DEFAULT NULL::character varying,
    manager character varying(30) DEFAULT NULL::character varying,
    start_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    end_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    dailyprojectbalance_id integer,
    periodeprojectbalance_id integer
);


ALTER TABLE accounting.project OWNER TO postgres;

--
-- Name: rakcabang; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.rakcabang (
    rakcabang_id integer NOT NULL,
    branch_code character varying(5) DEFAULT NULL::character varying,
    koderak character varying(30) DEFAULT NULL::character varying,
    accountinstance_id integer
);


ALTER TABLE accounting.rakcabang OWNER TO postgres;

--
-- Name: rakpusat; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.rakpusat (
    rakpusat_id integer NOT NULL,
    koderak character varying(30) DEFAULT NULL::character varying,
    accountinstance_id integer
);


ALTER TABLE accounting.rakpusat OWNER TO postgres;

--
-- Name: registerkurs; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.registerkurs (
    registerkurs_id integer NOT NULL,
    user_ubah character varying(20) DEFAULT NULL::character varying,
    terminal_ubah character varying(15) DEFAULT NULL::character varying,
    tanggal_ubah timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_tengah_bi double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_buku double precision,
    kurs_beli_kantorpusat double precision,
    kurs_jual_kantorpusat double precision,
    kurs_neraca double precision,
    kode_register character varying(1) DEFAULT NULL::character varying,
    kurs_reval double precision,
    kurs_remittance double precision,
    currency_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.registerkurs OWNER TO postgres;

--
-- Name: revaluationhistory; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.revaluationhistory (
    history_id integer NOT NULL,
    revaluation_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    currency_code character varying(20) DEFAULT NULL::character varying,
    average_exchangerate double precision,
    revaluation_exchangerate double precision,
    branch_code character varying(5) DEFAULT NULL::character varying
);


ALTER TABLE accounting.revaluationhistory OWNER TO postgres;

--
-- Name: rpvaccount; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.rpvaccount (
    rpv_name character varying(20) DEFAULT NULL::character varying NOT NULL,
    rpv_accountcode character varying(20) DEFAULT NULL::character varying,
    profit_accountcode character varying(20) DEFAULT NULL::character varying,
    loss_accountcode character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.rpvaccount OWNER TO postgres;

--
-- Name: rpvaccountdetail; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.rpvaccountdetail (
    accountinstance_valas integer,
    accountinstance_primer integer,
    rpvaccountdetail_accountcode character varying(20) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    rpv_name character varying(20) DEFAULT NULL::character varying NOT NULL,
    branch_code character varying(5) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE accounting.rpvaccountdetail OWNER TO postgres;

--
-- Name: seq_accounthierarchy; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_accounthierarchy
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_accounthierarchy OWNER TO postgres;

--
-- Name: seq_accountinstance; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_accountinstance
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_accountinstance OWNER TO postgres;

--
-- Name: seq_cashflowgroup; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_cashflowgroup
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_cashflowgroup OWNER TO postgres;

--
-- Name: seq_cashflowmember; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_cashflowmember
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_cashflowmember OWNER TO postgres;

--
-- Name: seq_custom_idgen; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_custom_idgen
    START WITH 45
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_custom_idgen OWNER TO postgres;

--
-- Name: seq_dailybalance; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_dailybalance
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_dailybalance OWNER TO postgres;

--
-- Name: seq_fact_daily_balance; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_fact_daily_balance
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_fact_daily_balance OWNER TO postgres;

--
-- Name: seq_journalblock; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_journalblock
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_journalblock OWNER TO postgres;

--
-- Name: seq_journalcreation; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_journalcreation
    START WITH 37
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_journalcreation OWNER TO postgres;

--
-- Name: seq_test; Type: SEQUENCE; Schema: accounting; Owner: postgres
--

CREATE SEQUENCE accounting.seq_test
    START WITH 103
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE accounting.seq_test OWNER TO postgres;

--
-- Name: sim_logrun; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.sim_logrun (
    logrun_id integer NOT NULL,
    sim_userid character varying,
    sim_type character varying(10) DEFAULT NULL::character varying,
    completion_time timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    status integer,
    description character varying(255) DEFAULT NULL::character varying
);


ALTER TABLE accounting.sim_logrun OWNER TO postgres;

--
-- Name: snapshot_accountinstance; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.snapshot_accountinstance (
    accountinstance_id integer,
    balance double precision,
    fl_cpa_accountinstance integer,
    fl_lpa_accountinstance integer,
    balance_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    isbolehinput character varying(1),
    branch_code character varying(5),
    account_code character varying(20),
    currency_code character varying(20),
    dailybalance_id integer,
    periodebalance_id integer,
    dailyprojectbalance_id integer,
    periodeprojectbalance_id integer,
    balancecumulative_ekuiv double precision,
    balancecumulative double precision
);


ALTER TABLE accounting.snapshot_accountinstance OWNER TO postgres;

--
-- Name: subsysteminteraction; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.subsysteminteraction (
    subsysteminteraction_id integer NOT NULL,
    titleinteraction character varying(50) DEFAULT NULL::character varying,
    parentssi_id integer,
    interactiontype character varying(1) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    intrmodel character varying(1) DEFAULT NULL::character varying,
    subsystemcode character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.subsysteminteraction OWNER TO postgres;

--
-- Name: tempcandidatejournal; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.tempcandidatejournal (
    tempcandidatejournal_id integer NOT NULL,
    account_code character varying(20) DEFAULT NULL::character varying,
    branch_code character varying(20) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying,
    description character varying(100) DEFAULT NULL::character varying,
    group_id integer,
    kode_kurs character varying(20) DEFAULT NULL::character varying,
    kode_mutasi character varying(1) DEFAULT NULL::character varying,
    nilai_kurs double precision,
    nilai_mutasi double precision,
    project_no character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE accounting.tempcandidatejournal OWNER TO postgres;

--
-- Name: temptable; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.temptable (
    accountcode character varying(20) NOT NULL,
    accountname character varying(100),
    accounttype character varying(1),
    isdetail character varying(1),
    accountparent character varying(20),
    cpaaccountcode character varying(20),
    is_processed integer
);


ALTER TABLE accounting.temptable OWNER TO postgres;

--
-- Name: temptable_RAK; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting."temptable_RAK" (
    accountcode character varying(20) NOT NULL,
    accountname character varying(100),
    accounttype character varying(1),
    isdetail character varying(1),
    accountparent character varying(20),
    cpaaccountcode character varying(20),
    is_processed integer
);


ALTER TABLE accounting."temptable_RAK" OWNER TO postgres;

--
-- Name: temptable_ori; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.temptable_ori (
    accountcode character varying(20) DEFAULT NULL::character varying NOT NULL,
    accountname character varying(100) DEFAULT NULL::character varying,
    accounttype character varying(1) DEFAULT NULL::character varying,
    isdetail character varying(1) DEFAULT NULL::character varying,
    accountparent character varying(20) DEFAULT NULL::character varying,
    cpaaccountcode character varying(20) DEFAULT NULL::character varying,
    is_processed integer
);


ALTER TABLE accounting.temptable_ori OWNER TO postgres;

--
-- Name: temptable_rpv; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.temptable_rpv (
    accountcode character varying(20) NOT NULL,
    accountname character varying(100),
    accounttype character varying(1),
    isdetail character varying(1),
    accountparent character varying(20),
    cpaaccountcode character varying(20),
    is_processed integer
);


ALTER TABLE accounting.temptable_rpv OWNER TO postgres;

--
-- Name: temptabledata; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.temptabledata (
    accountcode character varying(20),
    accountname character varying(100),
    accounttype character varying(1),
    isdetail character varying(1),
    accountparent character varying(20),
    cpaaccountcode character varying(20),
    is_processed integer
);


ALTER TABLE accounting.temptabledata OWNER TO postgres;

--
-- Name: temptablenew; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.temptablenew (
    accountcode character varying(20) NOT NULL,
    accountname character varying(100),
    accounttype character varying(1),
    isdetail character varying(1),
    accountparent character varying(20),
    cpaaccountcode character varying(20),
    is_processed integer
);


ALTER TABLE accounting.temptablenew OWNER TO postgres;

--
-- Name: transaksirak; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.transaksirak (
    debit double precision,
    credit double precision,
    cabangasal character varying(20) DEFAULT NULL::character varying,
    cabangtujuan character varying(20) DEFAULT NULL::character varying,
    jenistransaksirak character varying(1) DEFAULT NULL::character varying,
    transaksirak_id integer NOT NULL,
    keterangan character varying(50) DEFAULT NULL::character varying,
    statusterprosespusat character varying(1) DEFAULT NULL::character varying,
    transaksirakterkait_id integer,
    currency_code character varying(20) DEFAULT NULL::character varying,
    journal_no character varying(30) DEFAULT NULL::character varying,
    koderak character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE accounting.transaksirak OWNER TO postgres;

--
-- Name: userapp; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.userapp (
    id_user character varying(20) DEFAULT NULL::character varying NOT NULL,
    password character varying(32) DEFAULT NULL::character varying,
    status_profil character varying(1) DEFAULT NULL::character varying,
    level_user integer,
    tanggal_didaftarkan timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    tanggal_kadaluarsa timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    tanggal_password_kadaluarsa timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    tanggal_ubah_password_terakhir timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    tanggal_aktif_terakhir timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    tipe_akses_cabang character varying(1) DEFAULT NULL::character varying,
    tipe_akses_terminal character varying(1) DEFAULT NULL::character varying,
    hari_diperbolehkan_akses character varying(7) DEFAULT NULL::character varying,
    status_restriksi_waktu character varying(1) DEFAULT NULL::character varying,
    waktu_boleh_mulai timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    waktu_harus_selesai timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    maksimum_jumlah_login integer,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input character varying(15) DEFAULT NULL::character varying,
    user_perbarui character varying(20) DEFAULT NULL::character varying,
    tanggal_perbarui timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_perbarui character varying(15) DEFAULT NULL::character varying,
    tipe_user character varying(1) DEFAULT NULL::character varying,
    jumlah_login_gagal integer,
    jumlah_login_aktif integer,
    kunci_akses character varying(1) DEFAULT NULL::character varying,
    nama_user character varying(30) DEFAULT NULL::character varying,
    jumlah_validasi_gagal integer,
    status_password integer,
    maksimum_tidak_aktif integer,
    maksimum_ganti_password integer,
    no_urut_teller character varying(3) DEFAULT NULL::character varying,
    id_terminal character varying(15) DEFAULT NULL::character varying,
    kode_cabang character varying(20) DEFAULT NULL::character varying,
    nomor_karyawan character varying(20) DEFAULT NULL::character varying,
    employeeid integer,
    nolimitlocation character varying(1)
);


ALTER TABLE enterprise.userapp OWNER TO postgres;

--
-- Name: userapp; Type: VIEW; Schema: accounting; Owner: postgres
--

CREATE VIEW accounting.userapp AS
 SELECT id_user AS user_id,
    nama_user AS username,
    nolimitlocation,
    jumlah_login_aktif AS login_count,
    user_perbarui AS mod_user_id,
    tanggal_aktif_terakhir AS last_update,
    kode_cabang AS branch_code,
    id_user AS user_id1
   FROM enterprise.userapp;


ALTER VIEW accounting.userapp OWNER TO postgres;

--
-- Name: userapp_old; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.userapp_old (
    user_id character varying(20) DEFAULT NULL::character varying NOT NULL,
    username character varying(30) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    nolimitlocation character varying(1) DEFAULT NULL::character varying,
    login_count integer,
    mod_user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    branch_code character varying(5) DEFAULT NULL::character varying,
    user_id1 character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE accounting.userapp_old OWNER TO postgres;

--
-- Name: usergroup; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.usergroup (
    group_id character varying(8) DEFAULT NULL::character varying NOT NULL,
    groupname character varying(30) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE accounting.usergroup OWNER TO postgres;

--
-- Name: usergroupapp; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.usergroupapp (
    user_id character varying(20) DEFAULT NULL::character varying NOT NULL,
    group_id character varying(8) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE accounting.usergroupapp OWNER TO postgres;

--
-- Name: vendor; Type: TABLE; Schema: accounting; Owner: postgres
--

CREATE TABLE accounting.vendor (
    name character varying(40) DEFAULT NULL::character varying,
    address character varying(60) DEFAULT NULL::character varying,
    post_code character varying(5) DEFAULT NULL::character varying,
    tlp_no character varying(14) DEFAULT NULL::character varying,
    vendor_no integer NOT NULL
);


ALTER TABLE accounting.vendor OWNER TO postgres;

--
-- Name: auth_group; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE dashboard.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.auth_group_id_seq OWNED BY dashboard.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE dashboard.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.auth_group_permissions_id_seq OWNED BY dashboard.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE dashboard.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.auth_permission_id_seq OWNED BY dashboard.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE dashboard.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE dashboard.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.auth_user_groups_id_seq OWNED BY dashboard.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.auth_user_id_seq OWNED BY dashboard.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE dashboard.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.auth_user_user_permissions_id_seq OWNED BY dashboard.auth_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE dashboard.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.django_admin_log_id_seq OWNED BY dashboard.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE dashboard.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.django_content_type_id_seq OWNED BY dashboard.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: dashboard; Owner: postgres
--

CREATE TABLE dashboard.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE dashboard.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: dashboard; Owner: postgres
--

CREATE SEQUENCE dashboard.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE dashboard.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: dashboard; Owner: postgres
--

ALTER SEQUENCE dashboard.django_migrations_id_seq OWNED BY dashboard.django_migrations.id;


--
-- Name: accounttransactionitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accounttransactionitem (
    accounttitype character varying(1) DEFAULT NULL::character varying,
    accountno character varying(30) DEFAULT NULL::character varying,
    transactionitemid integer NOT NULL,
    amountperunit double precision,
    totalunit integer,
    ashnaf character varying(1) DEFAULT NULL::character varying,
    fundentity integer,
    percentageofamil double precision,
    distributionitemaccount character varying(20) DEFAULT NULL::character varying,
    donorid integer,
    cattype character varying(1),
    returntransactionitemid integer,
    catransactionid integer,
    isupdatebalance character varying(1),
    distributiontransferid integer,
    idpropinsi integer,
    kota character varying(100),
    kecamatan character varying(100),
    mustahiqid integer,
    distributioncategory character varying(1),
    marketerid integer,
    fundaccountno character varying(30)
);


ALTER TABLE transaction.accounttransactionitem OWNER TO postgres;

--
-- Name: branch; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.branch AS
 SELECT kode_cabang AS branchcode,
    nama_cabang AS branchname,
    branchid,
    kode_singkat AS shortcode,
    status_aktif AS isactive,
    kode_cabang_induk AS masterbranchcode
   FROM enterprise.cabang;


ALTER VIEW transaction.branch OWNER TO postgres;

--
-- Name: enum_varchar; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.enum_varchar (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value character varying(3) DEFAULT NULL::character varying NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE transaction.enum_varchar OWNER TO postgres;

--
-- Name: financialaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.financialaccount (
    accountno character varying(30) DEFAULT NULL::character varying NOT NULL,
    accountname character varying(50) DEFAULT NULL::character varying,
    balance numeric(38,2),
    branchcode character varying(5) DEFAULT NULL::character varying,
    currencycode character varying(5) DEFAULT NULL::character varying,
    financialaccounttype character varying(1) DEFAULT NULL::character varying,
    status character varying(1) DEFAULT NULL::character varying,
    openingdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    accountcode character varying(10) DEFAULT NULL::character varying,
    lastdaybalance double precision,
    lastdailybalanceid integer,
    balancedeposit numeric(38,2)
);


ALTER TABLE transaction.financialaccount OWNER TO postgres;

--
-- Name: product; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.product (
    productid integer NOT NULL,
    productname character varying(60) DEFAULT NULL::character varying,
    description character varying(100) DEFAULT NULL::character varying,
    accountofcollection character varying(20) DEFAULT NULL::character varying,
    accountofdistribution character varying(20) DEFAULT NULL::character varying,
    percentageofamilfunds double precision,
    producttype character varying(1) DEFAULT NULL::character varying,
    status character varying(1) DEFAULT NULL::character varying,
    closeddate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    fundcategory character varying(1) DEFAULT NULL::character varying,
    fixedvalue character varying(1) DEFAULT NULL::character varying,
    fixedvalueamount double precision,
    multipackage character varying(1) DEFAULT NULL::character varying,
    nishab double precision,
    haul integer,
    rate double precision,
    parentproductid integer,
    isdetail character varying(1) DEFAULT NULL::character varying,
    level integer,
    productcode character varying(20),
    zakahobjectid integer,
    zakahobject character varying(1),
    programtype character varying(1),
    programcategory character varying(10)
);


ALTER TABLE transaction.product OWNER TO postgres;

--
-- Name: productaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.productaccount (
    accountno character varying(30) DEFAULT NULL::character varying NOT NULL,
    productid integer,
    zakatbalance double precision,
    infaqbalance double precision,
    infaqterikatbalance double precision,
    wakafbalance double precision,
    amilbalance double precision,
    nonhalalbalance double precision,
    producttype character varying(1)
);


ALTER TABLE transaction.productaccount OWNER TO postgres;

--
-- Name: transaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transaction (
    transactionid integer NOT NULL,
    transactiondate timestamp(6) without time zone,
    referenceno character varying(30),
    description character varying(100),
    inputer character varying(20),
    transactioncode character varying(10),
    branchcode character varying(5),
    authuser character varying(20),
    transactiontime timestamp(6) without time zone,
    authdate timestamp(6) without time zone,
    authstatus character varying(1),
    batchid integer,
    isposted character varying(1),
    authaction character varying(1),
    journalblockid integer,
    channelcode character varying,
    sponsorid integer,
    donorid integer,
    volunteerid character varying(10),
    actualdate timestamp(6) without time zone,
    transactionno character varying(30),
    paidto character varying(30),
    donorno character varying(20),
    donorname character varying(150),
    amount numeric(38,2),
    currencycode character varying(5),
    receivedfrom character varying(30),
    marketerid integer,
    channelaccountno character varying(30),
    rate double precision,
    journalno character varying(30),
    hcbatchitemid integer,
    authoperationmode character varying(1),
    updatedate timestamp(6) without time zone,
    journalerrordescription character varying(200),
    flag_omit_journal character varying(1)
);


ALTER TABLE transaction.transaction OWNER TO postgres;

--
-- Name: transactionitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transactionitem (
    transactionitemid integer NOT NULL,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE transaction.transactionitem OWNER TO postgres;

--
-- Name: v_ashnaf_bymonthyear; Type: VIEW; Schema: dashboard; Owner: postgres
--

CREATE VIEW dashboard.v_ashnaf_bymonthyear AS
 SELECT row_number() OVER (ORDER BY (date_part('year'::text, t.actualdate)), (date_part('month'::text, t.actualdate)), a.ashnaf) AS id,
    date_part('month'::text, t.actualdate) AS realization_month,
    date_part('year'::text, t.actualdate) AS realization_year,
    a.ashnaf AS ashnaf_code,
    ea.enum_description AS ashnaf_name,
    count(a.ashnaf) AS count_ashnaf
   FROM ((((((((transaction.accounttransactionitem a
     JOIN transaction.transactionitem i ON ((a.transactionitemid = i.transactionitemid)))
     JOIN transaction.transaction t ON ((i.transactionid = t.transactionid)))
     JOIN transaction.financialaccount f ON (((a.accountno)::text = (f.accountno)::text)))
     JOIN transaction.productaccount p ON (((p.accountno)::text = (f.accountno)::text)))
     JOIN transaction.product pr ON ((p.productid = pr.productid)))
     JOIN transaction.product gpr ON ((pr.parentproductid = gpr.productid)))
     JOIN transaction.branch b ON (((b.branchcode)::text = (i.branchcode)::text)))
     JOIN transaction.enum_varchar ea ON ((((ea.enum_value)::text = (a.ashnaf)::text) AND ((ea.enum_name)::text = 'eAshnaf'::text))))
  WHERE (((a.accounttitype)::text = 'Z'::text) AND ((i.currencycode)::text = 'IDR'::text))
  GROUP BY (date_part('month'::text, t.actualdate)), (date_part('year'::text, t.actualdate)), a.ashnaf, ea.enum_description;


ALTER VIEW dashboard.v_ashnaf_bymonthyear OWNER TO postgres;

--
-- Name: budget; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.budget (
    budgetid integer NOT NULL,
    periodid integer,
    ownerid integer,
    itemcode character varying(30),
    itemname character varying(60),
    currencycode character varying(5),
    amount double precision,
    realization double precision,
    revisionid integer,
    budgetcode character varying(10),
    branchcode character varying(5),
    isdetail character varying(1),
    parentbudgetid integer,
    level integer,
    budgettype character varying(1),
    itemid integer
);


ALTER TABLE transaction.budget OWNER TO postgres;

--
-- Name: budgetowner; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.budgetowner (
    ownerid integer NOT NULL,
    ownername character varying(100),
    parentownerid integer,
    level integer,
    is_detail character varying(1),
    ownercode character varying(10),
    status character varying(1)
);


ALTER TABLE transaction.budgetowner OWNER TO postgres;

--
-- Name: budgetperiod; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.budgetperiod (
    periodid integer NOT NULL,
    parentperiodid integer,
    periodvalue integer NOT NULL,
    isopen character varying(1) NOT NULL,
    periodname character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.budgetperiod OWNER TO postgres;

--
-- Name: budgettransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.budgettransaction (
    transactionid integer,
    budgetid integer,
    transactionitemid integer NOT NULL,
    budgettranstype character varying(1)
);


ALTER TABLE transaction.budgettransaction OWNER TO postgres;

--
-- Name: v_budget_bymonthyear; Type: VIEW; Schema: dashboard; Owner: postgres
--

CREATE VIEW dashboard.v_budget_bymonthyear AS
 SELECT row_number() OVER (ORDER BY q.budget_year, bp.periodvalue, q.ownerid) AS id,
    bp.periodvalue AS budget_month,
    q.budget_year,
    q.ownerid,
    q.ownername,
    q.amount AS budget_amount,
    q2.realization AS budget_realization
   FROM ((( SELECT bp_1.periodvalue AS budget_year,
            bp_1.periodid,
            bo.ownerid,
            bo.ownername,
            sum(bd.amount) AS amount
           FROM ((transaction.budget bd
             JOIN transaction.budgetowner bo ON ((bo.ownerid = bd.ownerid)))
             JOIN transaction.budgetperiod bp_1 ON ((bp_1.periodid = bd.periodid)))
          GROUP BY bp_1.periodvalue, bp_1.periodid, bo.ownerid, bo.ownername) q
     JOIN transaction.budgetperiod bp ON ((bp.parentperiodid = q.periodid)))
     LEFT JOIN ( SELECT date_part('month'::text, t.actualdate) AS budget_month,
            bp_1.periodvalue AS budget_year,
            bp_1.periodid,
            bd.ownerid,
            sum(
                CASE
                    WHEN ((bt.budgettranstype)::text = 'R'::text) THEN (('-1'::integer)::double precision * ti.ekuivalenamount)
                    ELSE ti.ekuivalenamount
                END) AS realization
           FROM ((((transaction.budget bd
             JOIN transaction.budgetperiod bp_1 ON ((bp_1.periodid = bd.periodid)))
             JOIN transaction.budgettransaction bt ON ((bt.budgetid = bd.budgetid)))
             JOIN transaction.transactionitem ti ON ((ti.transactionitemid = bt.transactionitemid)))
             JOIN transaction.transaction t ON ((t.transactionid = ti.transactionid)))
          GROUP BY (date_part('month'::text, t.actualdate)), bp_1.periodvalue, bp_1.periodid, bd.ownerid) q2 ON (((q.ownerid = q2.ownerid) AND (q.periodid = q2.periodid) AND ((bp.periodvalue)::double precision = q2.budget_month))))
  ORDER BY q.budget_year, bp.periodvalue, q.ownername;


ALTER VIEW dashboard.v_budget_bymonthyear OWNER TO postgres;

--
-- Name: cashaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cashaccount (
    bankname character varying(30) DEFAULT NULL::character varying,
    bankaccountno character varying(20) DEFAULT NULL::character varying,
    accountcurrency character varying(5) DEFAULT NULL::character varying,
    cashaccounttype character varying(1) DEFAULT NULL::character varying,
    username character varying(30) DEFAULT NULL::character varying,
    accountno character varying(30) DEFAULT NULL::character varying NOT NULL,
    bankcode character varying(10) DEFAULT NULL::character varying,
    accountinterface character varying(20) DEFAULT NULL::character varying,
    cashcode character varying(10),
    productid integer,
    fundcategory character varying(1),
    isamilaccount character varying(1),
    isreconaccount character varying(1)
);


ALTER TABLE transaction.cashaccount OWNER TO postgres;

--
-- Name: v_dist_monthyear_byproduct; Type: VIEW; Schema: dashboard; Owner: postgres
--

CREATE VIEW dashboard.v_dist_monthyear_byproduct AS
 SELECT row_number() OVER (ORDER BY (date_part('year'::text, t.actualdate)), (date_part('month'::text, t.actualdate)), f.accountno, p2.productname) AS id,
    date_part('month'::text, t.actualdate) AS dist_month,
    date_part('year'::text, t.actualdate) AS dist_year,
    f.accountno,
    f.accountname,
    p2.productname,
    sum(
        CASE
            WHEN ((i.mutationtype)::text = 'D'::text) THEN i.amount
            ELSE (('-1'::integer)::numeric * i.amount)
        END) AS dist_amount
   FROM ((((((((transaction.accounttransactionitem a
     JOIN transaction.transactionitem i ON ((a.transactionitemid = i.transactionitemid)))
     JOIN transaction.financialaccount f ON (((a.accountno)::text = (f.accountno)::text)))
     JOIN transaction.productaccount pa ON (((pa.accountno)::text = (f.accountno)::text)))
     JOIN transaction.product p1 ON ((p1.productid = pa.productid)))
     JOIN transaction.product p2 ON ((p2.productid = p1.parentproductid)))
     JOIN transaction.branch b ON (((b.branchcode)::text = (i.branchcode)::text)))
     JOIN transaction.transaction t ON ((i.transactionid = t.transactionid)))
     LEFT JOIN ( SELECT f2.accountno,
            f2.accountname,
            c.bankaccountno
           FROM transaction.financialaccount f2,
            transaction.cashaccount c
          WHERE ((f2.accountno)::text = (c.accountno)::text)) ch ON (((ch.accountno)::text = (t.channelaccountno)::text)))
  WHERE (((i.currencycode)::text = 'IDR'::text) AND ((a.accounttitype)::text = 'Z'::text))
  GROUP BY (date_part('month'::text, t.actualdate)), (date_part('year'::text, t.actualdate)), f.accountno, f.accountname, p2.productname;


ALTER VIEW dashboard.v_dist_monthyear_byproduct OWNER TO postgres;

--
-- Name: donor; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.donor (
    donorname character varying(200) DEFAULT NULL::character varying,
    addresskelurahan character varying(100) DEFAULT NULL::character varying,
    addresssubdistrict character varying(50) DEFAULT NULL::character varying,
    addresscity character varying(50) DEFAULT NULL::character varying,
    addresspostalcode character varying(10) DEFAULT NULL::character varying,
    phonenumber character varying(20) DEFAULT NULL::character varying,
    fax character varying(20) DEFAULT NULL::character varying,
    referenceby character varying(30) DEFAULT NULL::character varying,
    status character varying(1) DEFAULT NULL::character varying,
    donortype character varying(1) DEFAULT NULL::character varying,
    addressstreet character varying(200) DEFAULT NULL::character varying,
    addressstate character varying(50) DEFAULT NULL::character varying,
    npwp character varying(50) DEFAULT NULL::character varying,
    npwz character varying(30),
    donorno character varying(20),
    donorid integer NOT NULL,
    joindate timestamp(6) without time zone,
    branchcode character varying(5),
    idpropinsi integer,
    marketerid integer,
    addresskecamatan character varying(50) DEFAULT NULL::character varying,
    idnegara integer,
    economicsector character varying(1),
    donorlevelid integer,
    donorgroup character varying(1),
    input_user character varying(20),
    input_date timestamp without time zone,
    nonactivedate timestamp without time zone,
    nonactiveuser character varying(30)
);


ALTER TABLE fund.donor OWNER TO postgres;

--
-- Name: donor; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.donor AS
 SELECT donorname,
    addresskelurahan,
    addresssubdistrict,
    addresscity,
    addresspostalcode,
    phonenumber,
    fax,
    referenceby,
    status,
    donortype,
    addressstreet,
    addressstate,
    npwp,
    npwz,
    donorno,
    donorid,
    joindate,
    branchcode,
    idpropinsi,
    marketerid,
    addresskecamatan,
    idnegara,
    economicsector
   FROM fund.donor;


ALTER VIEW transaction.donor OWNER TO postgres;

--
-- Name: v_fund_monthyear_bycash; Type: VIEW; Schema: dashboard; Owner: postgres
--

CREATE VIEW dashboard.v_fund_monthyear_bycash AS
 SELECT row_number() OVER (ORDER BY (date_part('year'::text, t.actualdate)), (date_part('month'::text, t.actualdate)), ch.accountno) AS id,
    date_part('month'::text, t.actualdate) AS fund_month,
    date_part('year'::text, t.actualdate) AS fund_year,
    ch.accountno,
    ch.accountname,
    sum(
        CASE
            WHEN ((i.mutationtype)::text = 'C'::text) THEN i.amount
            ELSE (('-1'::integer)::numeric * i.amount)
        END) AS fund_amount
   FROM (((((((transaction.accounttransactionitem a
     JOIN transaction.transactionitem i ON ((a.transactionitemid = i.transactionitemid)))
     JOIN transaction.financialaccount f ON (((a.accountno)::text = (f.accountno)::text)))
     JOIN transaction.productaccount p ON (((p.accountno)::text = (f.accountno)::text)))
     JOIN transaction.donor d ON ((a.donorid = d.donorid)))
     JOIN transaction.branch b ON (((b.branchcode)::text = (i.branchcode)::text)))
     JOIN transaction.transaction t ON ((i.transactionid = t.transactionid)))
     LEFT JOIN ( SELECT f2.accountno,
            f2.accountname,
            c.bankaccountno
           FROM transaction.financialaccount f2,
            transaction.cashaccount c
          WHERE ((f2.accountno)::text = (c.accountno)::text)) ch ON (((ch.accountno)::text = (t.channelaccountno)::text)))
  WHERE (((i.currencycode)::text = 'IDR'::text) AND ((a.accounttitype)::text = 'D'::text))
  GROUP BY (date_part('month'::text, t.actualdate)), (date_part('year'::text, t.actualdate)), ch.accountno, ch.accountname;


ALTER VIEW dashboard.v_fund_monthyear_bycash OWNER TO postgres;

--
-- Name: aplikasi; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.aplikasi (
    kode_aplikasi character varying(30) DEFAULT NULL::character varying NOT NULL,
    nama_aplikasi character varying(100) DEFAULT NULL::character varying,
    deskripsi character varying(100) DEFAULT NULL::character varying,
    nama_server character varying(30) DEFAULT NULL::character varying,
    protokol_akses character varying(15) DEFAULT NULL::character varying,
    lokasi_source character varying(100) DEFAULT NULL::character varying,
    lokasi_session character varying(100) DEFAULT NULL::character varying,
    nama_session character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.aplikasi OWNER TO postgres;

--
-- Name: appsubsystem; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.appsubsystem (
    subsystem_code character varying(5) NOT NULL,
    subsystem_name character varying(30),
    is_local character varying(1),
    session_name character varying(20),
    remote_host character varying(23),
    remote_port integer,
    is_ssl character varying(1),
    ssl_profile_name character varying(30),
    remote_appid character varying(50)
);


ALTER TABLE enterprise.appsubsystem OWNER TO postgres;

--
-- Name: areacabang; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.areacabang (
    kode_wilayah character varying(3) DEFAULT NULL::character varying NOT NULL,
    keterangan character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.areacabang OWNER TO postgres;

--
-- Name: backuppass; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.backuppass (
    id_user character varying(20),
    password character varying(32),
    decode character varying(32)
);


ALTER TABLE enterprise.backuppass OWNER TO postgres;

--
-- Name: bpparallelstep; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpparallelstep (
    parallel_step_id integer NOT NULL,
    parameter_name character varying(100) DEFAULT NULL::character varying,
    parameter_order integer,
    parameter_type integer,
    step_id integer
);


ALTER TABLE enterprise.bpparallelstep OWNER TO postgres;

--
-- Name: bpparallelstepdetail; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpparallelstepdetail (
    pstep_detail_id integer NOT NULL,
    svalue character varying(500) DEFAULT NULL::character varying,
    ivalue integer,
    parameter_type integer,
    unrestrict_next_step character varying(1) DEFAULT NULL::character varying,
    parallel_step_id integer,
    disabled character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.bpparallelstepdetail OWNER TO postgres;

--
-- Name: bpparallelstepinstance; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpparallelstepinstance (
    pstepinst_id integer NOT NULL,
    stepinst_id integer,
    pstep_detail_id integer
);


ALTER TABLE enterprise.bpparallelstepinstance OWNER TO postgres;

--
-- Name: bpprocess; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpprocess (
    bpprocess_id integer NOT NULL,
    pid integer,
    status integer,
    main_pid integer,
    phost character varying(24) DEFAULT NULL::character varying,
    error_info character varying(255) DEFAULT NULL::character varying,
    step_id integer,
    ctlcommand integer,
    processed integer
);


ALTER TABLE enterprise.bpprocess OWNER TO postgres;

--
-- Name: bpscenario; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpscenario (
    scenario_code character varying(10) DEFAULT NULL::character varying NOT NULL,
    scenario_name character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.bpscenario OWNER TO postgres;

--
-- Name: bpscenarioinstance; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpscenarioinstance (
    instance_id integer NOT NULL,
    start_time timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    stop_time timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_id character varying(20) DEFAULT NULL::character varying,
    terminal_id character varying(30) DEFAULT NULL::character varying,
    status integer,
    main_pid integer,
    scenario_code character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.bpscenarioinstance OWNER TO postgres;

--
-- Name: bpscript; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpscript (
    script_id integer NOT NULL,
    description character varying(100) DEFAULT NULL::character varying,
    script_path character varying(100) DEFAULT NULL::character varying,
    kode_aplikasi character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.bpscript OWNER TO postgres;

--
-- Name: bpstep; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpstep (
    step_id integer NOT NULL,
    description character varying(100) DEFAULT NULL::character varying,
    step_order integer,
    disabled character varying(1) DEFAULT NULL::character varying,
    scenario_code character varying(10) DEFAULT NULL::character varying,
    script_id integer
);


ALTER TABLE enterprise.bpstep OWNER TO postgres;

--
-- Name: bpstepinstance; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.bpstepinstance (
    stepinst_id integer NOT NULL,
    start_time timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    stop_time timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    status integer,
    step_error_message character varying(255) DEFAULT NULL::character varying,
    main_pid integer,
    pid integer,
    step_id integer,
    instance_id integer
);


ALTER TABLE enterprise.bpstepinstance OWNER TO postgres;

--
-- Name: cabangbmi; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.cabangbmi (
    id_cabang integer NOT NULL,
    kode_cabang character varying(10),
    nama_cabang character varying(50)
);


ALTER TABLE enterprise.cabangbmi OWNER TO postgres;

--
-- Name: custom_idgen; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.custom_idgen (
    idname character varying(30) DEFAULT NULL::character varying NOT NULL,
    idcode character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.custom_idgen OWNER TO postgres;

--
-- Name: daemons; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.daemons (
    "Start" text NOT NULL,
    "Info" text NOT NULL
);


ALTER TABLE enterprise.daemons OWNER TO postgres;

--
-- Name: departemen; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.departemen (
    kode_departemen character varying(10) DEFAULT NULL::character varying NOT NULL,
    nama_departemen character varying(30) DEFAULT NULL::character varying,
    deskripsi character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.departemen OWNER TO postgres;

--
-- Name: employee; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.employee (
    alamat character varying(200),
    agama integer,
    alamatsekarang character varying(100),
    email character varying(100),
    golongandarah character varying(1),
    jeniskelamin character varying(1),
    jumlahtanggungan integer,
    namaemployee character varying(200),
    nomordplk character varying(20),
    nomor_seluler character varying(20),
    nomorindukpegawai integer,
    nomorjamsostek character varying(20),
    nomorktp character varying(30),
    nomorpaspor character varying(30),
    npwp character varying(30),
    npwz character varying(30),
    pendidikanterakhir integer,
    statuspernikahan character varying(1),
    tanggallahir date,
    teleponkantor character varying(20),
    teleponrumah character varying(20),
    tempatlahir character varying(50),
    titel character varying(10),
    employeeid integer NOT NULL,
    inisial character varying(10),
    nomor_karyawan character varying(20),
    employeetype character varying(1),
    kode_pos character varying(10),
    nomor_telepon character varying(20),
    nama_supervisor character varying(200),
    is_supervisor character varying(1),
    is_personalia character varying(1),
    is_lemburberlaku character varying(1),
    nomor_kartu character varying(20),
    kode_departemen character varying(10),
    kode_jabatan character varying(10),
    id_cabangbmi integer,
    kode_cabang character varying(20),
    nama_lengkap character varying(200)
);


ALTER TABLE enterprise.employee OWNER TO postgres;

--
-- Name: enum_int; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.enum_int (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value integer NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.enum_int OWNER TO postgres;

--
-- Name: enum_varchar; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.enum_varchar (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value character varying(2) DEFAULT NULL::character varying NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.enum_varchar OWNER TO postgres;

--
-- Name: executablefungsi; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.executablefungsi (
    is_dual_control character varying(1) DEFAULT NULL::character varying,
    level_dual_control integer,
    level_override integer,
    level_akses integer,
    hari_diperbolehkan_akses character varying(7) DEFAULT NULL::character varying,
    waktu_boleh_diakses timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    waktu_selesai_diakses timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    id_fungsi character varying(10) DEFAULT NULL::character varying NOT NULL,
    restriksi_hari_akses character varying(1) DEFAULT NULL::character varying,
    restriksi_waktu_akses character varying(1) DEFAULT NULL::character varying,
    limit_transaksi_user double precision
);


ALTER TABLE enterprise.executablefungsi OWNER TO postgres;

--
-- Name: fungsi; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.fungsi (
    id_fungsi character varying(10) DEFAULT NULL::character varying NOT NULL,
    nama_fungsi character varying(60) DEFAULT NULL::character varying,
    tipe_fungsi character varying(1) DEFAULT NULL::character varying,
    id_parent_fungsi character varying(10) DEFAULT NULL::character varying,
    kode_aplikasi character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.fungsi OWNER TO postgres;

--
-- Name: gajiemployee; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.gajiemployee (
    nomorindukpegawai integer,
    bonusditerima double precision,
    asuransi double precision,
    aqh double precision,
    dplk double precision,
    gajipokok double precision,
    haricuti integer,
    iuranasuransi double precision,
    iuranjamsostek double precision,
    iurandplk double precision,
    pendapatanlain double precision,
    potonganlain double precision,
    rawatinap double precision,
    rawatjalan double precision,
    tanggal date,
    thr double precision,
    thrditerima double precision,
    tunjangancuti double precision,
    tunjangancutiditerima double precision,
    tunjanganjabatan double precision,
    tunjanganjamsostek double precision,
    tunjangankehadiran double precision,
    tunjangankesehatan double precision,
    tunjangankesehatanditerima double precision,
    tunjangankinerja double precision,
    tunjanganpendidikan double precision,
    tunjanganpulsa double precision,
    employeeid integer
);


ALTER TABLE enterprise.gajiemployee OWNER TO postgres;

--
-- Name: gammu; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.gammu (
    "Version" smallint DEFAULT (0)::smallint NOT NULL
);


ALTER TABLE enterprise.gammu OWNER TO postgres;

--
-- Name: glinterface; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.glinterface (
    kode_interface character varying(20) DEFAULT NULL::character varying,
    tipe_interface character varying(1) DEFAULT NULL::character varying,
    kode_account character varying(20) DEFAULT NULL::character varying,
    kode_rc character varying(20) DEFAULT NULL::character varying,
    deskripsi character varying(50) DEFAULT NULL::character varying,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input character varying(15) DEFAULT NULL::character varying,
    user_perbarui character varying(20) DEFAULT NULL::character varying,
    tanggal_perbarui timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_perbarui character varying(15) DEFAULT NULL::character varying,
    id_interface integer NOT NULL,
    kode_valuta character varying(20) DEFAULT NULL::character varying,
    kode_cabang character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.glinterface OWNER TO postgres;

--
-- Name: historikehadiran; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.historikehadiran (
    tanggal timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    id_histori_kehadiran integer NOT NULL,
    waktu_datang timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    waktu_pulang timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    nama_cabang character varying(30) DEFAULT NULL::character varying,
    nama_departemen character varying(30) DEFAULT NULL::character varying,
    nomor_karyawan character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.historikehadiran OWNER TO postgres;

--
-- Name: id_gen; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.id_gen (
    id_code character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.id_gen OWNER TO postgres;

--
-- Name: inbox; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.inbox (
    "UpdatedInDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "ReceivingDateTime" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "Text" text NOT NULL,
    "SenderNumber" character varying(20) DEFAULT ''::character varying NOT NULL,
    "Coding" character varying(255) DEFAULT 'Default_No_Compression'::character varying NOT NULL,
    "UDH" text NOT NULL,
    "SMSCNumber" character varying(20) DEFAULT ''::character varying NOT NULL,
    "Class" integer DEFAULT '-1'::integer NOT NULL,
    "TextDecoded" text DEFAULT ''::text NOT NULL,
    "ID" integer NOT NULL,
    "RecipientID" text NOT NULL,
    "Processed" boolean DEFAULT false NOT NULL,
    CONSTRAINT "inbox_Coding_check" CHECK ((("Coding")::text = ANY (ARRAY[('Default_No_Compression'::character varying)::text, ('Unicode_No_Compression'::character varying)::text, ('8bit'::character varying)::text, ('Default_Compression'::character varying)::text, ('Unicode_Compression'::character varying)::text])))
);


ALTER TABLE enterprise.inbox OWNER TO postgres;

--
-- Name: inbox_ID_seq; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise."inbox_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise."inbox_ID_seq" OWNER TO postgres;

--
-- Name: inbox_ID_seq; Type: SEQUENCE OWNED BY; Schema: enterprise; Owner: postgres
--

ALTER SEQUENCE enterprise."inbox_ID_seq" OWNED BY enterprise.inbox."ID";


--
-- Name: inboxdeletedsms; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.inboxdeletedsms (
    "UpdatedInDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "ReceivingDateTime" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "Text" text NOT NULL,
    "SenderNumber" character varying(20) DEFAULT ''::character varying NOT NULL,
    "Coding" character varying(255) DEFAULT 'Default_No_Compression'::character varying NOT NULL,
    "UDH" text NOT NULL,
    "SMSCNumber" character varying(20) DEFAULT ''::character varying NOT NULL,
    "Class" integer DEFAULT '-1'::integer NOT NULL,
    "TextDecoded" text DEFAULT ''::text NOT NULL,
    "ID" integer NOT NULL,
    "RecipientID" text NOT NULL,
    "Processed" boolean DEFAULT false NOT NULL,
    "DeletedDateTime" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "UserId" character varying(100),
    CONSTRAINT "inbox_Coding_check" CHECK ((("Coding")::text = ANY (ARRAY[('Default_No_Compression'::character varying)::text, ('Unicode_No_Compression'::character varying)::text, ('8bit'::character varying)::text, ('Default_Compression'::character varying)::text, ('Unicode_Compression'::character varying)::text])))
);


ALTER TABLE enterprise.inboxdeletedsms OWNER TO postgres;

--
-- Name: inboxparameter; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.inboxparameter (
    parameter_code character varying(10) DEFAULT NULL::character varying NOT NULL,
    description character varying(60) DEFAULT NULL::character varying,
    parameter_type character varying(1) DEFAULT NULL::character varying,
    form_script_name character varying(100) DEFAULT NULL::character varying,
    id_fungsi character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.inboxparameter OWNER TO postgres;

--
-- Name: jabatan; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.jabatan (
    kode_jabatan character varying(10) DEFAULT NULL::character varying NOT NULL,
    nama_jabatan character varying(30) DEFAULT NULL::character varying,
    deskripsi character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.jabatan OWNER TO postgres;

--
-- Name: kantor; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.kantor (
    kode_kantor character varying(5) DEFAULT NULL::character varying NOT NULL,
    nama_kantor character varying(100) DEFAULT NULL::character varying,
    tipe_kantor character varying(2) DEFAULT NULL::character varying,
    alamat character varying(200) DEFAULT NULL::character varying,
    nomor_npwp character varying(30) DEFAULT NULL::character varying,
    kode_pos character varying(5) DEFAULT NULL::character varying,
    nomor_telepon1 character varying(15) DEFAULT NULL::character varying,
    nomor_telepon2 character varying(15) DEFAULT NULL::character varying,
    nomor_telepon3 character varying(15) DEFAULT NULL::character varying,
    kode_cabang character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.kantor OWNER TO postgres;

--
-- Name: kemampuanbahasaemployee; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.kemampuanbahasaemployee (
    kemampuanbahasaid integer,
    employeeid integer,
    namabahasa integer,
    keahlianbicara integer,
    keahlianmenulis integer
);


ALTER TABLE enterprise.kemampuanbahasaemployee OWNER TO postgres;

--
-- Name: keterampilanemployee; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.keterampilanemployee (
    keterampilanid integer,
    employeeid integer,
    keahlianketerampilan integer,
    jenisketerampilan character varying(30)
);


ALTER TABLE enterprise.keterampilanemployee OWNER TO postgres;

--
-- Name: limitoperasi; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.limitoperasi (
    id_limit_operasi integer NOT NULL,
    jenis_limit character varying(1) DEFAULT NULL::character varying,
    nilai_limit double precision,
    nilai_limit_akumulasi double precision,
    jumlah_item_limit integer,
    status_otorisasi character varying(1) DEFAULT NULL::character varying,
    kode_cabang character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.limitoperasi OWNER TO postgres;

--
-- Name: limittransaksi; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.limittransaksi (
    id_limit_transaksi integer NOT NULL,
    jenis_limit character varying(1) DEFAULT NULL::character varying,
    nilai_limit double precision,
    nilai_limit_akumulasi double precision,
    jumlah_item_limit integer,
    id_user character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.limittransaksi OWNER TO postgres;

--
-- Name: listaplikasiperan; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.listaplikasiperan (
    kode_aplikasi character varying(30) DEFAULT NULL::character varying NOT NULL,
    id_peran character varying(30) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE enterprise.listaplikasiperan OWNER TO postgres;

--
-- Name: listaplikasiuser; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.listaplikasiuser (
    id_listaplikasiuser integer NOT NULL,
    id_user character varying(20) DEFAULT NULL::character varying,
    kode_aplikasi character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.listaplikasiuser OWNER TO postgres;

--
-- Name: listcabangdiizinkan; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.listcabangdiizinkan (
    id_user character varying(20) DEFAULT NULL::character varying NOT NULL,
    kode_cabang character varying(20) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE enterprise.listcabangdiizinkan OWNER TO postgres;

--
-- Name: listfungsiaplikasiperan; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.listfungsiaplikasiperan (
    kode_aplikasi character varying(30) DEFAULT NULL::character varying NOT NULL,
    id_peran character varying(30) DEFAULT NULL::character varying NOT NULL,
    id_fungsi character varying(10) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE enterprise.listfungsiaplikasiperan OWNER TO postgres;

--
-- Name: listfungsiaplikasiuser; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.listfungsiaplikasiuser (
    id_listfungsiaplikasiuser integer NOT NULL,
    id_fungsi character varying(10) DEFAULT NULL::character varying,
    id_listaplikasiuser integer
);


ALTER TABLE enterprise.listfungsiaplikasiuser OWNER TO postgres;

--
-- Name: listperanuser; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.listperanuser (
    id_peran character varying(30) DEFAULT NULL::character varying NOT NULL,
    id_user character varying(20) DEFAULT NULL::character varying NOT NULL,
    level_peranuser integer
);


ALTER TABLE enterprise.listperanuser OWNER TO postgres;

--
-- Name: listperanuser_bck; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.listperanuser_bck (
    id_peran character varying(30),
    id_user character varying(20),
    level_peranuser integer
);


ALTER TABLE enterprise.listperanuser_bck OWNER TO postgres;

--
-- Name: listterminaldiizinkan; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.listterminaldiizinkan (
    id_user character varying(20) DEFAULT NULL::character varying NOT NULL,
    id_terminal character varying(15) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE enterprise.listterminaldiizinkan OWNER TO postgres;

--
-- Name: loginsession; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.loginsession (
    login_id integer NOT NULL,
    login_time timestamp(6) without time zone,
    app_id character varying(25),
    terminal_ip character varying(25),
    session_id character varying(25),
    last_access_time timestamp(6) without time zone,
    user_id character varying(20),
    branch_code character varying(20)
);


ALTER TABLE enterprise.loginsession OWNER TO postgres;

--
-- Name: lokasi; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.lokasi (
    kode_lokasi character varying(10),
    nama_lokasi character varying(50),
    status_data character(1)
);


ALTER TABLE enterprise.lokasi OWNER TO postgres;

--
-- Name: menu; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.menu (
    menu_id integer NOT NULL,
    menu_name character varying(50),
    caption character varying(50),
    menu_level integer,
    parent_id integer,
    filename_id character varying(100),
    is_popup_menu character varying(1),
    kode_aplikasi character varying(50),
    is_main_menu character varying(1),
    menu_idx character varying(30)
);


ALTER TABLE enterprise.menu OWNER TO postgres;

--
-- Name: menuhierarchy; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.menuhierarchy (
    hierarchy_id integer NOT NULL,
    parent_id integer,
    child_id integer
);


ALTER TABLE enterprise.menuhierarchy OWNER TO postgres;

--
-- Name: otordata; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.otordata (
    id_data integer NOT NULL,
    actualfilename character varying(50),
    is_data_packet character varying(1),
    createddate timestamp(6) without time zone
);


ALTER TABLE enterprise.otordata OWNER TO postgres;

--
-- Name: otorentri; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.otorentri (
    id_otorisasi integer NOT NULL,
    tgl_input timestamp without time zone,
    user_input character varying(20),
    terminal_input character varying(25),
    tipe_target integer,
    keterangan character varying(100),
    info1 character varying(30),
    info2 character varying(30),
    nama_tabel character varying(50),
    tipe_key integer,
    key_int integer,
    key_string character varying(20),
    id_user character varying(20),
    id_peran character varying(30),
    kode_cabang character varying(20),
    kode_entri character varying(10),
    id_data integer,
    id_data1 integer
);


ALTER TABLE enterprise.otorentri OWNER TO postgres;

--
-- Name: otorentrihistori; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.otorentrihistori (
    id_otorisasi integer NOT NULL,
    tgl_input timestamp without time zone,
    user_input character varying(20),
    terminal_input character varying(25),
    tipe_target integer,
    tgl_otorisasi timestamp without time zone,
    user_otorisasi character varying(20),
    terminal_otorisasi character varying(20),
    status_otorisasi character varying(1),
    keterangan character varying(100),
    info1 character varying(30),
    info2 character varying(30),
    nama_entri character varying(50),
    nama_tabel character varying(50),
    tipe_key integer,
    key_int integer,
    key_string character varying(20),
    id_data integer,
    id_user character varying(20),
    id_peran character varying(30),
    kode_cabang character varying(20),
    id_data1 integer,
    kode_entri character varying(10)
);


ALTER TABLE enterprise.otorentrihistori OWNER TO postgres;

--
-- Name: otorparameter; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.otorparameter (
    kode_entri character varying(10) NOT NULL,
    remote_form_id character varying(100),
    method_id_save character varying(50),
    method_id_reject character varying(50),
    nama_entri character varying(50),
    classic_form_call character varying(1),
    subsystem_code character varying(5)
);


ALTER TABLE enterprise.otorparameter OWNER TO postgres;

--
-- Name: otpkey; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.otpkey (
    userid character varying(20) DEFAULT NULL::character varying NOT NULL,
    token_base character varying(16) DEFAULT NULL::character varying,
    t_challenge timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    key1 integer,
    key2 integer,
    key3 integer,
    key4 integer,
    key5 integer
);


ALTER TABLE enterprise.otpkey OWNER TO postgres;

--
-- Name: outbox; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.outbox (
    "UpdatedInDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "InsertIntoDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "SendingDateTime" timestamp without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "SendBefore" time without time zone DEFAULT '23:59:59'::time without time zone NOT NULL,
    "SendAfter" time without time zone DEFAULT '00:00:00'::time without time zone NOT NULL,
    "Text" text,
    "DestinationNumber" character varying(20) DEFAULT ''::character varying NOT NULL,
    "Coding" character varying(255) DEFAULT 'Default_No_Compression'::character varying NOT NULL,
    "UDH" text,
    "Class" integer DEFAULT '-1'::integer,
    "TextDecoded" text DEFAULT ''::text NOT NULL,
    "ID" integer NOT NULL,
    "MultiPart" boolean DEFAULT false NOT NULL,
    "RelativeValidity" integer DEFAULT '-1'::integer,
    "SenderID" character varying(255),
    "SendingTimeOut" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "DeliveryReport" character varying(10) DEFAULT 'default'::character varying,
    "CreatorID" text NOT NULL,
    CONSTRAINT "outbox_Coding_check" CHECK ((("Coding")::text = ANY (ARRAY[('Default_No_Compression'::character varying)::text, ('Unicode_No_Compression'::character varying)::text, ('8bit'::character varying)::text, ('Default_Compression'::character varying)::text, ('Unicode_Compression'::character varying)::text]))),
    CONSTRAINT "outbox_DeliveryReport_check" CHECK ((("DeliveryReport")::text = ANY (ARRAY[('default'::character varying)::text, ('yes'::character varying)::text, ('no'::character varying)::text])))
);


ALTER TABLE enterprise.outbox OWNER TO postgres;

--
-- Name: outbox_ID_seq; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise."outbox_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise."outbox_ID_seq" OWNER TO postgres;

--
-- Name: outbox_ID_seq; Type: SEQUENCE OWNED BY; Schema: enterprise; Owner: postgres
--

ALTER SEQUENCE enterprise."outbox_ID_seq" OWNED BY enterprise.outbox."ID";


--
-- Name: outbox_bak; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.outbox_bak (
    "UpdatedInDB" timestamp(0) without time zone,
    "InsertIntoDB" timestamp(0) without time zone,
    "SendingDateTime" timestamp without time zone,
    "SendBefore" time without time zone,
    "SendAfter" time without time zone,
    "Text" text,
    "DestinationNumber" character varying(20),
    "Coding" character varying(255),
    "UDH" text,
    "Class" integer,
    "TextDecoded" text,
    "ID" integer,
    "MultiPart" boolean,
    "RelativeValidity" integer,
    "SenderID" character varying(255),
    "SendingTimeOut" timestamp(0) without time zone,
    "DeliveryReport" character varying(10),
    "CreatorID" text
);


ALTER TABLE enterprise.outbox_bak OWNER TO postgres;

--
-- Name: outbox_multipart; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.outbox_multipart (
    "Text" text,
    "Coding" character varying(255) DEFAULT 'Default_No_Compression'::character varying NOT NULL,
    "UDH" text,
    "Class" integer DEFAULT '-1'::integer,
    "TextDecoded" text,
    "ID" integer NOT NULL,
    "SequencePosition" integer DEFAULT 1 NOT NULL,
    CONSTRAINT "outbox_multipart_Coding_check" CHECK ((("Coding")::text = ANY (ARRAY[('Default_No_Compression'::character varying)::text, ('Unicode_No_Compression'::character varying)::text, ('8bit'::character varying)::text, ('Default_Compression'::character varying)::text, ('Unicode_Compression'::character varying)::text])))
);


ALTER TABLE enterprise.outbox_multipart OWNER TO postgres;

--
-- Name: outbox_multipart_ID_seq; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise."outbox_multipart_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise."outbox_multipart_ID_seq" OWNER TO postgres;

--
-- Name: outbox_multipart_ID_seq; Type: SEQUENCE OWNED BY; Schema: enterprise; Owner: postgres
--

ALTER SEQUENCE enterprise."outbox_multipart_ID_seq" OWNED BY enterprise.outbox_multipart."ID";


--
-- Name: outboxdeleted; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.outboxdeleted (
    "UpdatedInDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "InsertIntoDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "SendingDateTime" timestamp without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "SendBefore" time without time zone DEFAULT '23:59:59'::time without time zone NOT NULL,
    "SendAfter" time without time zone DEFAULT '00:00:00'::time without time zone NOT NULL,
    "Text" text,
    "DestinationNumber" character varying(20) DEFAULT ''::character varying NOT NULL,
    "Coding" character varying(255) DEFAULT 'Default_No_Compression'::character varying NOT NULL,
    "UDH" text,
    "Class" integer DEFAULT '-1'::integer,
    "TextDecoded" text DEFAULT ''::text NOT NULL,
    "ID" integer DEFAULT nextval('enterprise."outbox_ID_seq"'::regclass) NOT NULL,
    "MultiPart" boolean DEFAULT false NOT NULL,
    "RelativeValidity" integer DEFAULT '-1'::integer,
    "SenderID" character varying(255),
    "SendingTimeOut" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "DeliveryReport" character varying(10) DEFAULT 'default'::character varying,
    "CreatorID" text NOT NULL,
    "DeletedDateTime" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "UserId" character varying(100),
    CONSTRAINT "outboxdeleted_Coding_check" CHECK ((("Coding")::text = ANY (ARRAY[('Default_No_Compression'::character varying)::text, ('Unicode_No_Compression'::character varying)::text, ('8bit'::character varying)::text, ('Default_Compression'::character varying)::text, ('Unicode_Compression'::character varying)::text]))),
    CONSTRAINT "outboxdeleted_DeliveryReport_check" CHECK ((("DeliveryReport")::text = ANY (ARRAY[('default'::character varying)::text, ('yes'::character varying)::text, ('no'::character varying)::text])))
);


ALTER TABLE enterprise.outboxdeleted OWNER TO postgres;

--
-- Name: parameterglobal; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.parameterglobal (
    kode_parameter character varying(10) DEFAULT NULL::character varying NOT NULL,
    tipe_parameter character varying(1) DEFAULT NULL::character varying,
    nilai_parameter double precision,
    deskripsi character varying(60) DEFAULT NULL::character varying,
    is_parameter_system character varying(1) DEFAULT NULL::character varying,
    nilai_parameter_tanggal timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    nilai_parameter_string character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.parameterglobal OWNER TO postgres;

--
-- Name: pbk; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.pbk (
    "ID" integer NOT NULL,
    "GroupID" integer DEFAULT '-1'::integer NOT NULL,
    "Name" text NOT NULL,
    "Number" text NOT NULL
);


ALTER TABLE enterprise.pbk OWNER TO postgres;

--
-- Name: pbk_ID_seq; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise."pbk_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise."pbk_ID_seq" OWNER TO postgres;

--
-- Name: pbk_ID_seq; Type: SEQUENCE OWNED BY; Schema: enterprise; Owner: postgres
--

ALTER SEQUENCE enterprise."pbk_ID_seq" OWNED BY enterprise.pbk."ID";


--
-- Name: pbk_groups; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.pbk_groups (
    "Name" text NOT NULL,
    "ID" integer NOT NULL
);


ALTER TABLE enterprise.pbk_groups OWNER TO postgres;

--
-- Name: pbk_groups_ID_seq; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise."pbk_groups_ID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise."pbk_groups_ID_seq" OWNER TO postgres;

--
-- Name: pbk_groups_ID_seq; Type: SEQUENCE OWNED BY; Schema: enterprise; Owner: postgres
--

ALTER SEQUENCE enterprise."pbk_groups_ID_seq" OWNED BY enterprise.pbk_groups."ID";


--
-- Name: pbk_id_seq; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.pbk_id_seq
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.pbk_id_seq OWNER TO postgres;

--
-- Name: pendidikanemployee; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.pendidikanemployee (
    pendidikanid integer,
    tahun character varying(4),
    pendidikan character varying(60),
    lembaga character varying(60),
    status integer,
    jenispendidikan character varying(1),
    employeeid integer
);


ALTER TABLE enterprise.pendidikanemployee OWNER TO postgres;

--
-- Name: pengalamanemployee; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.pengalamanemployee (
    pengalamanid integer,
    tahun character varying(4),
    lembaga character varying(50),
    jabatan character varying(50),
    deskripsitugas character varying(100),
    employeeid integer,
    tipepengalaman character varying(1)
);


ALTER TABLE enterprise.pengalamanemployee OWNER TO postgres;

--
-- Name: peran; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.peran (
    id_peran character varying(30) DEFAULT NULL::character varying NOT NULL,
    nama_peran character varying(30) DEFAULT NULL::character varying,
    deskripsi character varying(50) DEFAULT NULL::character varying,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input character varying(15) DEFAULT NULL::character varying,
    user_perbarui character varying(20) DEFAULT NULL::character varying,
    tanggal_perbarui timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_perbarui character varying(15) DEFAULT NULL::character varying,
    status_peran character(1)
);


ALTER TABLE enterprise.peran OWNER TO postgres;

--
-- Name: phones; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.phones (
    "ID" text NOT NULL,
    "UpdatedInDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "InsertIntoDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "TimeOut" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "Send" boolean DEFAULT false NOT NULL,
    "Receive" boolean DEFAULT false NOT NULL,
    "IMEI" character varying(35) NOT NULL,
    "Client" text NOT NULL,
    "Battery" integer DEFAULT '-1'::integer NOT NULL,
    "Signal" integer DEFAULT '-1'::integer NOT NULL,
    "Sent" integer DEFAULT 0 NOT NULL,
    "Received" integer DEFAULT 0 NOT NULL
);


ALTER TABLE enterprise.phones OWNER TO postgres;

--
-- Name: publication; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.publication (
    publication_code character varying(5) DEFAULT NULL::character varying NOT NULL,
    description character varying(100) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.publication OWNER TO postgres;

--
-- Name: rekeningemployee; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.rekeningemployee (
    employeeid integer,
    nomorindukpegawai character varying(10),
    namabank character varying(60),
    cabang character varying(50),
    nomorrekening character varying(30),
    namarekening character varying(50)
);


ALTER TABLE enterprise.rekeningemployee OWNER TO postgres;

--
-- Name: rolemenulist; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.rolemenulist (
    list_id integer NOT NULL,
    id_peran character varying(20),
    menu_id integer
);


ALTER TABLE enterprise.rolemenulist OWNER TO postgres;

--
-- Name: sentitems; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.sentitems (
    "UpdatedInDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "InsertIntoDB" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "SendingDateTime" timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    "DeliveryDateTime" timestamp(0) without time zone,
    "Text" text NOT NULL,
    "DestinationNumber" character varying(20) DEFAULT ''::character varying NOT NULL,
    "Coding" character varying(255) DEFAULT 'Default_No_Compression'::character varying NOT NULL,
    "UDH" text NOT NULL,
    "SMSCNumber" character varying(20) DEFAULT ''::character varying NOT NULL,
    "Class" integer DEFAULT '-1'::integer NOT NULL,
    "TextDecoded" text DEFAULT ''::text NOT NULL,
    "ID" integer NOT NULL,
    "SenderID" character varying(255) NOT NULL,
    "SequencePosition" integer DEFAULT 1 NOT NULL,
    "Status" character varying(255) DEFAULT 'SendingOK'::character varying NOT NULL,
    "StatusError" integer DEFAULT '-1'::integer NOT NULL,
    "TPMR" integer DEFAULT '-1'::integer NOT NULL,
    "RelativeValidity" integer DEFAULT '-1'::integer NOT NULL,
    "CreatorID" text NOT NULL,
    CONSTRAINT "sentitems_Coding_check" CHECK ((("Coding")::text = ANY (ARRAY[('Default_No_Compression'::character varying)::text, ('Unicode_No_Compression'::character varying)::text, ('8bit'::character varying)::text, ('Default_Compression'::character varying)::text, ('Unicode_Compression'::character varying)::text]))),
    CONSTRAINT "sentitems_Status_check" CHECK ((("Status")::text = ANY (ARRAY[('SendingOK'::character varying)::text, ('SendingOKNoReport'::character varying)::text, ('SendingError'::character varying)::text, ('DeliveryOK'::character varying)::text, ('DeliveryFailed'::character varying)::text, ('DeliveryPending'::character varying)::text, ('DeliveryUnknown'::character varying)::text, ('Error'::character varying)::text])))
);


ALTER TABLE enterprise.sentitems OWNER TO postgres;

--
-- Name: sentitems_ID_seq; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise."sentitems_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise."sentitems_ID_seq" OWNER TO postgres;

--
-- Name: sentitems_ID_seq; Type: SEQUENCE OWNED BY; Schema: enterprise; Owner: postgres
--

ALTER SEQUENCE enterprise."sentitems_ID_seq" OWNED BY enterprise.sentitems."ID";


--
-- Name: seq_employee; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_employee
    START WITH 727
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_employee OWNER TO postgres;

--
-- Name: seq_gajiemployee; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_gajiemployee
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_gajiemployee OWNER TO postgres;

--
-- Name: seq_kemampuanbahasaemployee; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_kemampuanbahasaemployee
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 999999999
    CACHE 1
    CYCLE;


ALTER SEQUENCE enterprise.seq_kemampuanbahasaemployee OWNER TO postgres;

--
-- Name: seq_keterampilanemployee; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_keterampilanemployee
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 999999999
    CACHE 1
    CYCLE;


ALTER SEQUENCE enterprise.seq_keterampilanemployee OWNER TO postgres;

--
-- Name: seq_limittransaksi; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_limittransaksi
    START WITH 40
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_limittransaksi OWNER TO postgres;

--
-- Name: seq_loginsession; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_loginsession
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_loginsession OWNER TO postgres;

--
-- Name: seq_menu; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_menu
    START WITH 11229
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_menu OWNER TO postgres;

--
-- Name: seq_menuhierarchy; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_menuhierarchy
    START WITH 21447
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_menuhierarchy OWNER TO postgres;

--
-- Name: seq_otordata; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_otordata
    START WITH 29
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_otordata OWNER TO postgres;

--
-- Name: seq_otorentri; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_otorentri
    START WITH 29
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_otorentri OWNER TO postgres;

--
-- Name: seq_outbox; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_outbox
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_outbox OWNER TO postgres;

--
-- Name: seq_pendidikanemployee; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_pendidikanemployee
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999999
    CACHE 1
    CYCLE;


ALTER SEQUENCE enterprise.seq_pendidikanemployee OWNER TO postgres;

--
-- Name: seq_pengalamanemployee; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_pengalamanemployee
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 99999999999
    CACHE 1
    CYCLE;


ALTER SEQUENCE enterprise.seq_pengalamanemployee OWNER TO postgres;

--
-- Name: seq_rolemenulist; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_rolemenulist
    START WITH 8231
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_rolemenulist OWNER TO postgres;

--
-- Name: seq_useraudit; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_useraudit
    START WITH 13951
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_useraudit OWNER TO postgres;

--
-- Name: seq_usermenulist; Type: SEQUENCE; Schema: enterprise; Owner: postgres
--

CREATE SEQUENCE enterprise.seq_usermenulist
    START WITH 17
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE enterprise.seq_usermenulist OWNER TO postgres;

--
-- Name: subscribeitem; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.subscribeitem (
    id_sitem integer NOT NULL,
    script_path character varying(200) DEFAULT NULL::character varying,
    kode_aplikasi character varying(30) DEFAULT NULL::character varying,
    publication_code character varying(5) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.subscribeitem OWNER TO postgres;

--
-- Name: teller; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.teller (
    kode_rekening_teller character varying(7) DEFAULT NULL::character varying,
    id_user character varying(20) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE enterprise.teller OWNER TO postgres;

--
-- Name: terminal; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.terminal (
    id_terminal character varying(15) DEFAULT NULL::character varying NOT NULL,
    nama_terminal character varying(30) DEFAULT NULL::character varying,
    lokasi_terminal character varying(15) DEFAULT NULL::character varying,
    deskripsi character varying(50) DEFAULT NULL::character varying,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input character varying(15) DEFAULT NULL::character varying,
    user_perbarui character varying(20) DEFAULT NULL::character varying,
    tanggal_perbarui timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_perbarui character varying(15) DEFAULT NULL::character varying,
    kode_kantor character varying(5) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.terminal OWNER TO postgres;

--
-- Name: useraudit; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.useraudit (
    audit_id integer NOT NULL,
    user_id character varying(20),
    ip_address character varying(25),
    action_time timestamp(6) without time zone,
    operation_code character varying(32),
    is_objaudit character(1),
    app_id character varying(20)
);


ALTER TABLE enterprise.useraudit OWNER TO postgres;

--
-- Name: usermenulist; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.usermenulist (
    list_id integer NOT NULL,
    id_user character varying(20),
    menu_id integer
);


ALTER TABLE enterprise.usermenulist OWNER TO postgres;

--
-- Name: usertbl; Type: TABLE; Schema: enterprise; Owner: postgres
--

CREATE TABLE enterprise.usertbl (
    userid character varying(20) DEFAULT NULL::character varying NOT NULL,
    enc_password1 character varying(16) DEFAULT NULL::character varying,
    enc_password2 character varying(16) DEFAULT NULL::character varying
);


ALTER TABLE enterprise.usertbl OWNER TO postgres;

--
-- Name: employee; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.employee (
    employeeid character varying(20) NOT NULL,
    supervisorid character varying(20),
    individuid integer,
    performanceappraisalid integer,
    targetachievementid integer,
    workunitid character varying(50),
    positionid character varying(50),
    employeestatus character varying(1),
    employeeentrydate timestamp(6) without time zone,
    rank integer,
    salaryhistoryid integer,
    careerhistoryid integer,
    rankhistoryid integer,
    edpid integer,
    isactive character varying(1),
    nonactivedescription character varying(100),
    nonactivedate timestamp(6) without time zone,
    basicsalary double precision,
    attendanceid character varying(20)
);


ALTER TABLE personalia.employee OWNER TO postgres;

--
-- Name: individu; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.individu (
    individuid integer NOT NULL,
    individuname character varying(50),
    addresscity character varying(50),
    addresskecamatan character varying(50),
    addresskelurahan character varying(50),
    addresspostalcode character varying(10),
    addressstate character varying(50),
    addressstreet character varying(200),
    addresssubdistrict character varying(50),
    branchcode character varying(5),
    individuno character varying(20),
    individutype character varying(2),
    individustatus character varying(1),
    birthdate timestamp(6) without time zone,
    birthplace character varying(50),
    gender character varying(1),
    formaleducation integer,
    marital character varying(2),
    religion integer,
    identitytype character varying(1),
    identitynumber character varying(30),
    phonenumber character varying(20),
    initialname character varying(3),
    mobilenumberpersonal character varying(40),
    mobilenumbercorporate character varying(40),
    emailpersonal character varying(60),
    emailcorporate character varying(60),
    photo1 character varying(200),
    photo2 character varying(200),
    photo3 character varying(200),
    dependent integer,
    accountno character varying(20)
);


ALTER TABLE personalia.individu OWNER TO postgres;

--
-- Name: vemployee; Type: VIEW; Schema: enterprise; Owner: postgres
--

CREATE VIEW enterprise.vemployee AS
 SELECT e.employeeid AS nomor_karyawan,
    i.individuname AS nama_lengkap
   FROM (personalia.employee e
     JOIN personalia.individu i ON ((e.individuid = i.individuid)));


ALTER VIEW enterprise.vemployee OWNER TO postgres;

--
-- Name: bankaccountlist; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.bankaccountlist (
    bankaccountid integer NOT NULL,
    bankaccountname character varying(200),
    bankaccountno character varying(20),
    bankaccountlisttype character varying(1),
    bankcode character varying(10),
    isdefault character varying(1)
);


ALTER TABLE fund.bankaccountlist OWNER TO postgres;

--
-- Name: batchuploadphone; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.batchuploadphone (
    id_batch integer NOT NULL,
    batch_date timestamp without time zone
);


ALTER TABLE fund.batchuploadphone OWNER TO postgres;

--
-- Name: batchuploadphoneitem; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.batchuploadphoneitem (
    id_batch integer NOT NULL,
    workidentitynumber character varying(30) NOT NULL,
    employeename character varying(200),
    mobilephonenew character varying(20),
    mobilephoneold character varying(20)
);


ALTER TABLE fund.batchuploadphoneitem OWNER TO postgres;

--
-- Name: bsz; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.bsz (
    bszid integer NOT NULL,
    bsznumber character varying(30),
    donorid integer,
    bszdate timestamp(6) without time zone,
    bszperiodbegin timestamp without time zone,
    bszperiodend timestamp without time zone
);


ALTER TABLE fund.bsz OWNER TO postgres;

--
-- Name: bszdetail; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.bszdetail (
    bszdetailid integer NOT NULL,
    bszid integer,
    item integer,
    percentage double precision,
    year integer,
    basicvalue double precision,
    zakahvalue double precision
);


ALTER TABLE fund.bszdetail OWNER TO postgres;

--
-- Name: bsztransaction; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.bsztransaction (
    bszid integer,
    transactionitemid integer NOT NULL,
    bsztransactionid integer NOT NULL
);


ALTER TABLE fund.bsztransaction OWNER TO postgres;

--
-- Name: colltarget; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.colltarget (
    targetid integer NOT NULL,
    productid integer,
    periodid integer,
    targetamount numeric(30,2),
    branchcode character varying(5)
);


ALTER TABLE fund.colltarget OWNER TO postgres;

--
-- Name: colltargetperiod; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.colltargetperiod (
    periodid integer NOT NULL,
    periodvalue integer,
    periode_code character varying(4),
    periodamount numeric(30,2)
);


ALTER TABLE fund.colltargetperiod OWNER TO postgres;

--
-- Name: corporatedonor; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.corporatedonor (
    corporation character varying(1) DEFAULT NULL::character varying,
    siupp character varying(20) DEFAULT NULL::character varying,
    tdp character varying(20) DEFAULT NULL::character varying,
    locationtype character varying(30) DEFAULT NULL::character varying,
    ownertype character varying(30) DEFAULT NULL::character varying,
    establisheddate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    establishedplace character varying(50) DEFAULT NULL::character varying,
    contactperson character varying(50) DEFAULT NULL::character varying,
    patronagecompany character varying(1) DEFAULT NULL::character varying,
    donorid integer NOT NULL,
    cpname character varying(150),
    cpemail character varying(200),
    cpphonenumber character varying(30),
    cpmobilenumber character varying(30)
);


ALTER TABLE fund.corporatedonor OWNER TO postgres;

--
-- Name: custom_idgen; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.custom_idgen (
    idname character varying(30) DEFAULT NULL::character varying NOT NULL,
    idcode character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE fund.custom_idgen OWNER TO postgres;

--
-- Name: donorbankaccount; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.donorbankaccount (
    bankaccountid integer NOT NULL,
    donorid integer
);


ALTER TABLE fund.donorbankaccount OWNER TO postgres;

--
-- Name: donorcommitment; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.donorcommitment (
    commitmentid integer NOT NULL,
    commitmentamount numeric(30,2),
    accountno character varying(30),
    donorid integer
);


ALTER TABLE fund.donorcommitment OWNER TO postgres;

--
-- Name: donorcommitmenthistory; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.donorcommitmenthistory (
    historyid integer NOT NULL,
    donorid integer,
    commitmentamount numeric(30,4),
    dateinput timestamp(6) without time zone,
    accountno character varying(30),
    userinput character varying(50)
);


ALTER TABLE fund.donorcommitmenthistory OWNER TO postgres;

--
-- Name: donorfieldhistory; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.donorfieldhistory (
    historyid integer NOT NULL,
    donorid integer,
    fieldname character varying(100),
    fieldvalueint integer,
    fieldvaluechar character varying(200),
    fieldvaluetimestamp timestamp without time zone,
    dateinput timestamp without time zone,
    fielddescription character varying(200),
    fieldvaluedouble numeric(30,4),
    userinput character varying(50)
);


ALTER TABLE fund.donorfieldhistory OWNER TO postgres;

--
-- Name: donorlevel; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.donorlevel (
    donorlevelid integer NOT NULL,
    donorlevelcode character varying(10),
    donorleveldescription character varying(50)
);


ALTER TABLE fund.donorlevel OWNER TO postgres;

--
-- Name: donortotalfund; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.donortotalfund (
    totalfundid integer NOT NULL,
    donorid integer,
    fundentity integer,
    totalamount numeric(38,2)
);


ALTER TABLE fund.donortotalfund OWNER TO postgres;

--
-- Name: emailbody; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.emailbody (
    emailbodyid integer NOT NULL,
    jenisbody character varying(10),
    subject character varying(30),
    body character varying(2000),
    isactive character varying(1),
    userinput character varying(50),
    userubah character varying(50),
    tanggalinput timestamp(6) without time zone,
    tanggalubah timestamp(6) without time zone
);


ALTER TABLE fund.emailbody OWNER TO postgres;

--
-- Name: enum_int; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.enum_int (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value integer NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE fund.enum_int OWNER TO postgres;

--
-- Name: enum_varchar; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.enum_varchar (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value character varying(3) DEFAULT NULL::character varying NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE fund.enum_varchar OWNER TO postgres;

--
-- Name: fieldofwork; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.fieldofwork (
    fworkid integer NOT NULL,
    fworkcode character varying(10) DEFAULT NULL::character varying,
    fworkname character varying(60) DEFAULT NULL::character varying,
    fnpwzcode character varying(3) DEFAULT NULL::character varying
);


ALTER TABLE fund.fieldofwork OWNER TO postgres;

--
-- Name: id_gen; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.id_gen (
    id_code character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE fund.id_gen OWNER TO postgres;

--
-- Name: individualdonor; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.individualdonor (
    gender character varying(1) DEFAULT NULL::character varying,
    birthplace character varying(150) DEFAULT NULL::character varying,
    birthdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    identitytype character varying(1) DEFAULT NULL::character varying,
    religion integer,
    identitynumber character varying(20) DEFAULT NULL::character varying,
    language character varying(1) DEFAULT NULL::character varying,
    lastformaleducation integer,
    incomepermonth double precision,
    expensepermonth double precision,
    maritalstate character varying(1) DEFAULT NULL::character varying,
    officeaddress character varying(200) DEFAULT NULL::character varying,
    officekelurahan character varying(50) DEFAULT NULL::character varying,
    officesubdistrict character varying(50) DEFAULT NULL::character varying,
    officecity character varying(50) DEFAULT NULL::character varying,
    officestate character varying(50) DEFAULT NULL::character varying,
    officepostalcode character varying(50) DEFAULT NULL::character varying,
    officephonenumber character varying(50) DEFAULT NULL::character varying,
    email character varying(200),
    donorid integer NOT NULL,
    mobilephone character varying(20),
    idpropinsioffice integer,
    officekecamatan character varying(50) DEFAULT NULL::character varying,
    corporatename character varying(50) DEFAULT NULL::character varying,
    jobposition character varying(50) DEFAULT NULL::character varying,
    couplename character varying(50) DEFAULT NULL::character varying,
    fworkid integer,
    child integer,
    isinternalemployee character varying(1),
    workareaid integer,
    workunitid integer,
    workidentitynumber character varying(30),
    statusrumah character varying(1),
    workpositionid integer,
    workbusinessareaid integer,
    workbusinessarea character varying(200),
    workunit character varying(200),
    workposition character varying(200),
    workareaidinitial integer
);


ALTER TABLE fund.individualdonor OWNER TO postgres;

--
-- Name: marketer; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.marketer (
    marketername character varying(50) DEFAULT NULL::character varying,
    marketertype character varying(1) DEFAULT NULL::character varying,
    marketercode character varying(20),
    marketerid integer NOT NULL,
    marketeraddress character varying(200),
    marketermobilephone character varying(14),
    branchcode character varying(10),
    cpname character varying(200),
    supervisiorid integer,
    cpphonenumber character varying(20),
    jenismarketer character varying(1),
    joindate timestamp(6) without time zone,
    employeeid character varying(20),
    status character varying(1),
    statusedit character varying(1)
);


ALTER TABLE fund.marketer OWNER TO postgres;

--
-- Name: marketertarget; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.marketertarget (
    targetid integer NOT NULL,
    realizationamount numeric(30,2),
    year integer,
    targetamount numeric(30,2),
    marketerid integer
);


ALTER TABLE fund.marketertarget OWNER TO postgres;

--
-- Name: negara; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.negara (
    idnegara integer NOT NULL,
    nama_negara character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE fund.negara OWNER TO postgres;

--
-- Name: parameter; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.parameter (
    parametercode character varying(20) DEFAULT NULL::character varying NOT NULL,
    parametervalue double precision,
    description character varying(100) DEFAULT NULL::character varying,
    parameterstringvalue character varying(100) DEFAULT NULL::character varying,
    parameterdatevalue timestamp(6) without time zone
);


ALTER TABLE fund.parameter OWNER TO postgres;

--
-- Name: parameterglobal; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.parameterglobal (
    kode_parameter character varying(25) DEFAULT NULL::character varying NOT NULL,
    tipe_parameter character varying(1) DEFAULT NULL::character varying,
    nilai_parameter double precision,
    deskripsi character varying(100) DEFAULT NULL::character varying,
    is_parameter_system character varying(1) DEFAULT NULL::character varying,
    nilai_parameter_tanggal timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    nilai_parameter_string character varying(30) DEFAULT NULL::character varying,
    tag character varying(15),
    default_code character varying(30)
);


ALTER TABLE fund.parameterglobal OWNER TO postgres;

--
-- Name: propinsi; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.propinsi (
    idpropinsi integer NOT NULL,
    idnegara integer,
    propinsi character varying(50) DEFAULT NULL::character varying,
    kodepropinsi character varying(3) DEFAULT NULL::character varying
);


ALTER TABLE fund.propinsi OWNER TO postgres;

--
-- Name: senderemail; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.senderemail (
    idsenderemail integer NOT NULL,
    username character varying(30),
    password character varying(20),
    host character varying(30),
    port integer,
    emailaddress character varying(100),
    userinput character varying(50),
    useredit character varying(50),
    dateinput timestamp(6) without time zone,
    dateedit timestamp(6) without time zone,
    isactive character varying(1)
);


ALTER TABLE fund.senderemail OWNER TO postgres;

--
-- Name: seq_200; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_200
    START WITH 109
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_200 OWNER TO postgres;

--
-- Name: seq_accounthierarchy; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_accounthierarchy
    START WITH 1059
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_accounthierarchy OWNER TO postgres;

--
-- Name: seq_accountinstance; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_accountinstance
    START WITH 43251
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_accountinstance OWNER TO postgres;

--
-- Name: seq_assetcategory; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_assetcategory
    START WITH 13
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_assetcategory OWNER TO postgres;

--
-- Name: seq_bankaccountlist; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_bankaccountlist
    START WITH 5537
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_bankaccountlist OWNER TO postgres;

--
-- Name: seq_batchupload; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_batchupload
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_batchupload OWNER TO postgres;

--
-- Name: seq_bsz; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_bsz
    START WITH 63
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_bsz OWNER TO postgres;

--
-- Name: seq_bszdetail; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_bszdetail
    START WITH 435
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_bszdetail OWNER TO postgres;

--
-- Name: seq_bsztransaction; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_bsztransaction
    START WITH 83
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_bsztransaction OWNER TO postgres;

--
-- Name: seq_budget; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_budget
    START WITH 11747
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_budget OWNER TO postgres;

--
-- Name: seq_budgetitem; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_budgetitem
    START WITH 1251
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_budgetitem OWNER TO postgres;

--
-- Name: seq_budgetitemhierarchy; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_budgetitemhierarchy
    START WITH 2192
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_budgetitemhierarchy OWNER TO postgres;

--
-- Name: seq_budgetowner; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_budgetowner
    START WITH 17
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_budgetowner OWNER TO postgres;

--
-- Name: seq_budgetownerhierarchy; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_budgetownerhierarchy
    START WITH 94
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_budgetownerhierarchy OWNER TO postgres;

--
-- Name: seq_budgetperiod; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_budgetperiod
    START WITH 118
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_budgetperiod OWNER TO postgres;

--
-- Name: seq_budgetrevision; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_budgetrevision
    START WITH 6
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_budgetrevision OWNER TO postgres;

--
-- Name: seq_budgettransaction; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_budgettransaction
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_budgettransaction OWNER TO postgres;

--
-- Name: seq_colltarget; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_colltarget
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_colltarget OWNER TO postgres;

--
-- Name: seq_colltargetperiod; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_colltargetperiod
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_colltargetperiod OWNER TO postgres;

--
-- Name: seq_dailybalance; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_dailybalance
    START WITH 1391
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_dailybalance OWNER TO postgres;

--
-- Name: seq_dinarcertificate; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_dinarcertificate
    START WITH 4
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_dinarcertificate OWNER TO postgres;

--
-- Name: seq_distributiontransferinfo; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_distributiontransferinfo
    START WITH 10
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_distributiontransferinfo OWNER TO postgres;

--
-- Name: seq_donor; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_donor
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_donor OWNER TO postgres;

--
-- Name: seq_donorcommitment; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_donorcommitment
    START WITH 6
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_donorcommitment OWNER TO postgres;

--
-- Name: seq_donorcommitmenthistory; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_donorcommitmenthistory
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_donorcommitmenthistory OWNER TO postgres;

--
-- Name: seq_donorfieldhistory; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_donorfieldhistory
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_donorfieldhistory OWNER TO postgres;

--
-- Name: seq_donorlevel; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_donorlevel
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_donorlevel OWNER TO postgres;

--
-- Name: seq_donortotalfund; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_donortotalfund
    START WITH 4012
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_donortotalfund OWNER TO postgres;

--
-- Name: seq_emailbody; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_emailbody
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_emailbody OWNER TO postgres;

--
-- Name: seq_externaldebtor; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_externaldebtor
    START WITH 40
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_externaldebtor OWNER TO postgres;

--
-- Name: seq_fieldofwork; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_fieldofwork
    START WITH 12
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_fieldofwork OWNER TO postgres;

--
-- Name: seq_glinterface; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_glinterface
    START WITH 5467
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_glinterface OWNER TO postgres;

--
-- Name: seq_glinterfacecontainer; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_glinterfacecontainer
    START WITH 26
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_glinterfacecontainer OWNER TO postgres;

--
-- Name: seq_glinterfacemember; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_glinterfacemember
    START WITH 165
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_glinterfacemember OWNER TO postgres;

--
-- Name: seq_inbox; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_inbox
    START WITH 12362
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_inbox OWNER TO postgres;

--
-- Name: seq_inboxhistory; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_inboxhistory
    START WITH 1887
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_inboxhistory OWNER TO postgres;

--
-- Name: seq_investee; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_investee
    START WITH 14
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_investee OWNER TO postgres;

--
-- Name: seq_investmentcategory; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_investmentcategory
    START WITH 7
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_investmentcategory OWNER TO postgres;

--
-- Name: seq_invoice; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_invoice
    START WITH 22
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_invoice OWNER TO postgres;

--
-- Name: seq_journalblock; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_journalblock
    START WITH 312
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_journalblock OWNER TO postgres;

--
-- Name: seq_kurshistory; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_kurshistory
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_kurshistory OWNER TO postgres;

--
-- Name: seq_mapreconcile; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_mapreconcile
    START WITH 52
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_mapreconcile OWNER TO postgres;

--
-- Name: seq_mapreconcileaccount; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_mapreconcileaccount
    START WITH 107
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_mapreconcileaccount OWNER TO postgres;

--
-- Name: seq_marketer; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_marketer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_marketer OWNER TO postgres;

--
-- Name: seq_marketertarget; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_marketertarget
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_marketertarget OWNER TO postgres;

--
-- Name: seq_mustahiq; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_mustahiq
    START WITH 15
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_mustahiq OWNER TO postgres;

--
-- Name: seq_parameterjournal; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_parameterjournal
    START WITH 65
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_parameterjournal OWNER TO postgres;

--
-- Name: seq_parameterjournalitem; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_parameterjournalitem
    START WITH 205
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_parameterjournalitem OWNER TO postgres;

--
-- Name: seq_product; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_product
    START WITH 139
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_product OWNER TO postgres;

--
-- Name: seq_producthierarchy; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_producthierarchy
    START WITH 116
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_producthierarchy OWNER TO postgres;

--
-- Name: seq_projectsponsor; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_projectsponsor
    START WITH 27
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_projectsponsor OWNER TO postgres;

--
-- Name: seq_projectsponsordisbursement; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_projectsponsordisbursement
    START WITH 11
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_projectsponsordisbursement OWNER TO postgres;

--
-- Name: seq_propinsi; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_propinsi
    START WITH 37
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_propinsi OWNER TO postgres;

--
-- Name: seq_reconcileaccountbalance; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_reconcileaccountbalance
    START WITH 7290
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_reconcileaccountbalance OWNER TO postgres;

--
-- Name: seq_registerkurs; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_registerkurs
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_registerkurs OWNER TO postgres;

--
-- Name: seq_senderemail; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_senderemail
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_senderemail OWNER TO postgres;

--
-- Name: seq_smslog; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_smslog
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_smslog OWNER TO postgres;

--
-- Name: seq_sponsor; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_sponsor
    START WITH 68
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_sponsor OWNER TO postgres;

--
-- Name: seq_transaction; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_transaction
    START WITH 237516
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_transaction OWNER TO postgres;

--
-- Name: seq_transactionbatch; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_transactionbatch
    START WITH 1128
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_transactionbatch OWNER TO postgres;

--
-- Name: seq_transactionitem; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_transactionitem
    START WITH 483734
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_transactionitem OWNER TO postgres;

--
-- Name: seq_transrecongenlog; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_transrecongenlog
    START WITH 218745
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_transrecongenlog OWNER TO postgres;

--
-- Name: seq_wakafcertificate; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_wakafcertificate
    START WITH 51
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_wakafcertificate OWNER TO postgres;

--
-- Name: seq_workarea; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_workarea
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_workarea OWNER TO postgres;

--
-- Name: seq_workbusinessarea; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_workbusinessarea
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_workbusinessarea OWNER TO postgres;

--
-- Name: seq_workposition; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_workposition
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_workposition OWNER TO postgres;

--
-- Name: seq_workunit; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_workunit
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_workunit OWNER TO postgres;

--
-- Name: seq_zakahobject; Type: SEQUENCE; Schema: fund; Owner: postgres
--

CREATE SEQUENCE fund.seq_zakahobject
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE fund.seq_zakahobject OWNER TO postgres;

--
-- Name: smslog; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.smslog (
    log_id integer NOT NULL,
    donorid integer,
    phonenumber character varying(30),
    outbox_id integer,
    message character varying(300),
    messagetype integer,
    iscanceled character varying(1),
    log_date timestamp(6) without time zone,
    log_time timestamp(6) without time zone,
    creatorid character varying(100),
    userid character varying(50),
    reply_inboxid integer,
    extmessageid character varying(30),
    extmsgstatuscode character varying(5),
    extmsgstatusdesc character varying(50)
);


ALTER TABLE fund.smslog OWNER TO postgres;

--
-- Name: smslogdeleted; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.smslogdeleted (
    log_id integer NOT NULL,
    donorid integer,
    phonenumber character varying(30),
    outbox_id integer,
    message character varying(300),
    messagetype integer,
    iscanceled character varying(1),
    log_date timestamp(6) without time zone,
    log_time timestamp(6) without time zone,
    creatorid character varying(100),
    userid character varying(50),
    reply_inboxid integer,
    deleted_datetime timestamp(0) without time zone DEFAULT ('now'::text)::timestamp(0) without time zone NOT NULL,
    deleted_userid character varying(100)
);


ALTER TABLE fund.smslogdeleted OWNER TO postgres;

--
-- Name: tmp_area; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.tmp_area (
    workidentitynumber character varying(20),
    areaname character varying(100),
    workareaid integer
);


ALTER TABLE fund.tmp_area OWNER TO postgres;

--
-- Name: tmp_donor_deleted; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.tmp_donor_deleted (
    donorid integer,
    donorname character varying(200),
    workidentitynumber character varying(30)
);


ALTER TABLE fund.tmp_donor_deleted OWNER TO postgres;

--
-- Name: workarea; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.workarea (
    workareaid integer NOT NULL,
    workareacode character varying(10),
    workareaname character varying(100)
);


ALTER TABLE fund.workarea OWNER TO postgres;

--
-- Name: workbusinessarea; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.workbusinessarea (
    workbusinessareaid integer NOT NULL,
    workbusinessareacode character varying(10),
    workbusinessareaname character varying(200)
);


ALTER TABLE fund.workbusinessarea OWNER TO postgres;

--
-- Name: workposition; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.workposition (
    workpositionid integer NOT NULL,
    workpositioncode character varying(10),
    workpositionname character varying(200)
);


ALTER TABLE fund.workposition OWNER TO postgres;

--
-- Name: workunit; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.workunit (
    workunitid integer NOT NULL,
    workunitcode character varying(10),
    workunitname character varying(100)
);


ALTER TABLE fund.workunit OWNER TO postgres;

--
-- Name: zakahobject; Type: TABLE; Schema: fund; Owner: postgres
--

CREATE TABLE fund.zakahobject (
    zakahobjectid integer NOT NULL,
    zakahobjectcode character varying(5),
    zakahobjectname character varying(100)
);


ALTER TABLE fund.zakahobject OWNER TO postgres;

--
-- Name: bankaccount_convert; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.bankaccount_convert (
    accountno_bank character varying(20) NOT NULL,
    account_code_baru character varying(20),
    saldo_awal numeric(36,10)
);


ALTER TABLE migration.bankaccount_convert OWNER TO postgres;

--
-- Name: cabang_reset_candidate; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.cabang_reset_candidate (
    kode_cabang character varying(10) NOT NULL
);


ALTER TABLE migration.cabang_reset_candidate OWNER TO postgres;

--
-- Name: coaconv_account_laz_old; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_account_laz_old (
    account_code character varying(20),
    account_name character varying(100),
    account_level integer,
    is_detail character varying(1),
    account_type character varying(1),
    is_system character varying(1),
    userid_last_modified character varying(20),
    time_last_modified timestamp(6) without time zone,
    fl_parent_account character varying(20),
    userid_create character varying(20),
    time_create timestamp(6) without time zone,
    balance double precision,
    fl_cpa_accountcode character varying(20),
    fl_lpa_accountcode character varying(20),
    isactivaoffbalancesheet character varying(1),
    isrpvrakreportshow character varying(1),
    isrpvaccount character varying(1)
);


ALTER TABLE migration.coaconv_account_laz_old OWNER TO postgres;

--
-- Name: coaconv_accounthierarchy_laz_old; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_accounthierarchy_laz_old (
    accounthierarchy_id integer,
    fl_parentaccountcode character varying(20),
    fl_childaccountcode character varying(20)
);


ALTER TABLE migration.coaconv_accounthierarchy_laz_old OWNER TO postgres;

--
-- Name: coaconv_accountinstance_laz_old; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_accountinstance_laz_old (
    accountinstance_id integer,
    balance numeric(36,10),
    fl_cpa_accountinstance integer,
    fl_lpa_accountinstance integer,
    balance_ekuiv numeric(36,10),
    balance_ratarata numeric(36,10),
    balance_ratarata_ekuiv numeric(36,10),
    trial_balance numeric(36,10),
    trial_balance_ekuiv numeric(36,10),
    balance_harilalu numeric(36,10),
    balance_harilalu_ekuiv numeric(36,10),
    isbolehinput character varying(1),
    branch_code character varying(5),
    account_code character varying(20),
    currency_code character varying(20),
    dailybalance_id integer,
    periodebalance_id integer,
    dailyprojectbalance_id integer,
    periodeprojectbalance_id integer,
    balance_sign numeric(1,0)
);


ALTER TABLE migration.coaconv_accountinstance_laz_old OWNER TO postgres;

--
-- Name: coaconv_assetwakaf; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_assetwakaf (
    assetregnumber character varying(20) NOT NULL
);


ALTER TABLE migration.coaconv_assetwakaf OWNER TO postgres;

--
-- Name: coaconv_balancesumitemmember_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_balancesumitemmember_bck (
    memberid integer,
    itemid integer,
    account_code character varying(20)
);


ALTER TABLE migration.coaconv_balancesumitemmember_bck OWNER TO postgres;

--
-- Name: coaconv_bankremove; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_bankremove (
    accountno_bank character varying(20) NOT NULL
);


ALTER TABLE migration.coaconv_bankremove OWNER TO postgres;

--
-- Name: coaconv_bankwakaf; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_bankwakaf (
    accountno_bank character varying(20) NOT NULL
);


ALTER TABLE migration.coaconv_bankwakaf OWNER TO postgres;

--
-- Name: coaconv_cashaccount_remove; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_cashaccount_remove (
    accountno character varying(30),
    accountname character varying(50),
    balance numeric(38,2),
    branchcode character varying(5),
    currencycode character varying(5),
    financialaccounttype character varying(1),
    status character varying(1),
    openingdate timestamp(6) without time zone,
    accountcode character varying(10),
    lastdaybalance double precision,
    lastdailybalanceid integer,
    balancedeposit numeric(38,2)
);


ALTER TABLE migration.coaconv_cashaccount_remove OWNER TO postgres;

--
-- Name: coaconv_cashaccount_wakaf; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_cashaccount_wakaf (
    accountno character varying(30),
    accountname character varying(50),
    balance numeric(38,2),
    branchcode character varying(5),
    currencycode character varying(5),
    financialaccounttype character varying(1),
    status character varying(1),
    openingdate timestamp(6) without time zone,
    accountcode character varying(10),
    lastdaybalance double precision,
    lastdailybalanceid integer,
    balancedeposit numeric(38,2)
);


ALTER TABLE migration.coaconv_cashaccount_wakaf OWNER TO postgres;

--
-- Name: coaconv_cashflowmember_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_cashflowmember_bck (
    cfmemberid integer,
    cfgroupid integer,
    account_code character varying(20),
    mutationtype character varying(1),
    trancodeexclude character varying(200),
    trancodeinclude character varying(200),
    journalcodeexclude character varying(200),
    journalcodeinclude character varying(200),
    additionalinfo character varying(300)
);


ALTER TABLE migration.coaconv_cashflowmember_bck OWNER TO postgres;

--
-- Name: coaconv_dailybalance_laz_old; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_dailybalance_laz_old (
    dailybalance_id integer,
    balance numeric(36,10),
    balance_ekuiv numeric(36,10),
    balance_harilalu numeric(36,10),
    balance_harilalu_ekuiv numeric(36,10),
    balance_ratarata numeric(36,10),
    balance_ratarata_ekuiv numeric(36,10),
    trial_balance numeric(36,10),
    trial_balance_ekuiv numeric(36,10),
    balancecumulative numeric(36,10),
    balancecumulative_ekuiv numeric(36,10),
    datevalue timestamp(6) without time zone,
    debit numeric(36,10),
    credit numeric(36,10),
    debit_ekuiv numeric(36,10),
    credit_ekuiv numeric(36,10),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4),
    accountinstance_id integer
);


ALTER TABLE migration.coaconv_dailybalance_laz_old OWNER TO postgres;

--
-- Name: coaconv_depreciableasset_wakaf; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_depreciableasset_wakaf (
    deprassetid integer,
    deprassetregnumber character varying(20),
    registerdate timestamp without time zone,
    inputdate timestamp without time zone,
    inputuser character varying(50),
    deprassettype character varying(1),
    deprassetname character varying(100),
    branchcode character varying(5),
    depreciationsequence integer,
    deprassetstate character varying(1),
    depreciationaccumvalue numeric(30,8)
);


ALTER TABLE migration.coaconv_depreciableasset_wakaf OWNER TO postgres;

--
-- Name: coaconv_financialaccount_remove; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_financialaccount_remove (
    accountno character varying(30),
    accountname character varying(50),
    balance numeric(38,2),
    branchcode character varying(5),
    currencycode character varying(5),
    financialaccounttype character varying(1),
    status character varying(1),
    openingdate timestamp(6) without time zone,
    accountcode character varying(10),
    lastdaybalance double precision,
    lastdailybalanceid integer,
    balancedeposit numeric(38,2)
);


ALTER TABLE migration.coaconv_financialaccount_remove OWNER TO postgres;

--
-- Name: coaconv_financialaccount_wakaf; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_financialaccount_wakaf (
    accountno character varying(30),
    accountname character varying(50),
    balance numeric(38,2),
    branchcode character varying(5),
    currencycode character varying(5),
    financialaccounttype character varying(1),
    status character varying(1),
    openingdate timestamp(6) without time zone,
    accountcode character varying(10),
    lastdaybalance double precision,
    lastdailybalanceid integer,
    balancedeposit numeric(38,2)
);


ALTER TABLE migration.coaconv_financialaccount_wakaf OWNER TO postgres;

--
-- Name: coaconv_fixedasset_wakaf; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_fixedasset_wakaf (
    deprassetid integer,
    isparent character varying(1),
    parentid integer,
    fatypeid integer,
    bookvalue numeric(30,4),
    initvalue numeric(30,4),
    depreciationvalue numeric(30,4),
    model character varying(100),
    description character varying,
    lastdeprdate timestamp without time zone,
    nextdeprdate timestamp without time zone,
    isinsured character varying(1),
    insuranceduedate timestamp(6) without time zone,
    stnkduedate timestamp(6) without time zone,
    fixedassetcategory character varying(1),
    fundentity integer,
    retiredate timestamp without time zone,
    retirereason character varying(1),
    retiredescription character varying(200),
    fixedassetstatus character varying(1)
);


ALTER TABLE migration.coaconv_fixedasset_wakaf OWNER TO postgres;

--
-- Name: coaconv_glinterface_tran_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_glinterface_tran_bck (
    interfaceid integer,
    interfacecode character varying(30),
    description character varying(100),
    accountcode character varying(20),
    accountname character varying(60),
    productid integer
);


ALTER TABLE migration.coaconv_glinterface_tran_bck OWNER TO postgres;

--
-- Name: coaconv_glinterfacemember_perso_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_glinterfacemember_perso_bck (
    glimemberid integer,
    accountcode character varying(20),
    accountname character varying(100),
    glimembercode character varying(20),
    description character varying(100),
    glicontainerid integer
);


ALTER TABLE migration.coaconv_glinterfacemember_perso_bck OWNER TO postgres;

--
-- Name: coaconv_globalglinterface_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_globalglinterface_bck (
    glinterfacecode character varying(20),
    glinterfacename character varying(100),
    accountcode character varying(20)
);


ALTER TABLE migration.coaconv_globalglinterface_bck OWNER TO postgres;

--
-- Name: coaconv_journal_laz_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_journal_laz_bck (
    journal_no character varying(30),
    journal_date_posting timestamp(6) without time zone,
    description character varying(200),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journal_date_last_modified timestamp(6) without time zone,
    userid_posting character varying(20),
    is_posted character varying(1),
    journal_type character varying(10),
    journal_date timestamp(6) without time zone,
    lastitemno integer,
    status character varying(1),
    docoprstatus character varying(1),
    is_partlychecked character varying(1),
    branch_code character varying(5),
    transaction_date timestamp(6) without time zone,
    journal_state character varying(1),
    serial_no character varying(23),
    event_date timestamp(6) without time zone,
    lock_userid character varying(20),
    fl_origin_journal character varying(30),
    id_journalcreation integer,
    source_app character varying(30),
    source_app_class character varying(30),
    source_app_ref character varying(30),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4)
);


ALTER TABLE migration.coaconv_journal_laz_bck OWNER TO postgres;

--
-- Name: coaconv_journal_remove_suspect; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_journal_remove_suspect (
    fl_journal character varying(30)
);


ALTER TABLE migration.coaconv_journal_remove_suspect OWNER TO postgres;

--
-- Name: coaconv_journal_wakaf_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_journal_wakaf_bck (
    journal_no character varying(30),
    journal_date_posting timestamp(6) without time zone,
    description character varying(200),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journal_date_last_modified timestamp(6) without time zone,
    userid_posting character varying(20),
    is_posted character varying(1),
    journal_type character varying(10),
    journal_date timestamp(6) without time zone,
    lastitemno integer,
    status character varying(1),
    docoprstatus character varying(1),
    is_partlychecked character varying(1),
    branch_code character varying(5),
    transaction_date timestamp(6) without time zone,
    journal_state character varying(1),
    serial_no character varying(23),
    event_date timestamp(6) without time zone,
    lock_userid character varying(20),
    fl_origin_journal character varying(30),
    id_journalcreation integer,
    source_app character varying(30),
    source_app_class character varying(30),
    source_app_ref character varying(30),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4)
);


ALTER TABLE migration.coaconv_journal_wakaf_bck OWNER TO postgres;

--
-- Name: coaconv_journal_wakaf_candidate; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_journal_wakaf_candidate (
    fl_journal character varying(30)
);


ALTER TABLE migration.coaconv_journal_wakaf_candidate OWNER TO postgres;

--
-- Name: coaconv_journalitem_laz_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_journalitem_laz_bck (
    fl_journal character varying(30),
    journalitem_no integer,
    fl_account character varying(20),
    amount_debit numeric(36,10),
    amount_credit numeric(36,10),
    description character varying(200),
    branch_code character varying(20),
    valuta_code character varying(20),
    rc_code character varying(20),
    generic_code character varying(20),
    fl_posting_account character varying(20),
    fl_project_no character varying(10),
    docoprstatus character varying(1),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journalitemstatus character varying(1),
    userid_posting character varying(20),
    userid_check character varying(20),
    dateposting timestamp(6) without time zone,
    datelastmod timestamp(6) without time zone,
    datecreate timestamp(6) without time zone,
    event_date timestamp(6) without time zone,
    journalitemtype character varying(1),
    kode_kurs character varying(20),
    nilai_kurs numeric(36,10),
    rpv_main integer,
    subsystemcode character varying(20),
    subaccountcode character varying(30),
    id_journalcreation integer,
    subaccountname character varying(100),
    accountinstance_id integer,
    id_journalblock integer,
    transaksirak_id integer,
    source_class_id character varying(32),
    source_key_id integer,
    additionaldescription character varying(200)
);


ALTER TABLE migration.coaconv_journalitem_laz_bck OWNER TO postgres;

--
-- Name: coaconv_journalitem_laz_old; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_journalitem_laz_old (
    fl_journal character varying(30),
    journalitem_no integer,
    fl_account character varying(20),
    amount_debit numeric(36,10),
    amount_credit numeric(36,10),
    description character varying(200),
    branch_code character varying(20),
    valuta_code character varying(20),
    rc_code character varying(20),
    generic_code character varying(20),
    fl_posting_account character varying(20),
    fl_project_no character varying(10),
    docoprstatus character varying(1),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journalitemstatus character varying(1),
    userid_posting character varying(20),
    userid_check character varying(20),
    dateposting timestamp(6) without time zone,
    datelastmod timestamp(6) without time zone,
    datecreate timestamp(6) without time zone,
    event_date timestamp(6) without time zone,
    journalitemtype character varying(1),
    kode_kurs character varying(20),
    nilai_kurs numeric(36,10),
    rpv_main integer,
    subsystemcode character varying(20),
    subaccountcode character varying(30),
    id_journalcreation integer,
    subaccountname character varying(100),
    accountinstance_id integer,
    id_journalblock integer,
    transaksirak_id integer,
    source_class_id character varying(32),
    source_key_id integer,
    additionaldescription character varying(200)
);


ALTER TABLE migration.coaconv_journalitem_laz_old OWNER TO postgres;

--
-- Name: coaconv_journalitem_wakaf_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_journalitem_wakaf_bck (
    fl_journal character varying(30),
    journalitem_no integer,
    fl_account character varying(20),
    amount_debit numeric(36,10),
    amount_credit numeric(36,10),
    description character varying(200),
    branch_code character varying(20),
    valuta_code character varying(20),
    rc_code character varying(20),
    generic_code character varying(20),
    fl_posting_account character varying(20),
    fl_project_no character varying(10),
    docoprstatus character varying(1),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journalitemstatus character varying(1),
    userid_posting character varying(20),
    userid_check character varying(20),
    dateposting timestamp(6) without time zone,
    datelastmod timestamp(6) without time zone,
    datecreate timestamp(6) without time zone,
    event_date timestamp(6) without time zone,
    journalitemtype character varying(1),
    kode_kurs character varying(20),
    nilai_kurs numeric(36,10),
    rpv_main integer,
    subsystemcode character varying(20),
    subaccountcode character varying(30),
    id_journalcreation integer,
    subaccountname character varying(100),
    accountinstance_id integer,
    id_journalblock integer,
    transaksirak_id integer,
    source_class_id character varying(32),
    source_key_id integer,
    additionaldescription character varying(200)
);


ALTER TABLE migration.coaconv_journalitem_wakaf_bck OWNER TO postgres;

--
-- Name: coaconv_transaction_laz_noitem; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transaction_laz_noitem (
    transactionid integer,
    transactiondate timestamp(6) without time zone,
    referenceno character varying(30),
    description character varying(100),
    inputer character varying(20),
    transactioncode character varying(10),
    branchcode character varying(5),
    authuser character varying(20),
    transactiontime timestamp(6) without time zone,
    authdate timestamp(6) without time zone,
    authstatus character varying(1),
    batchid integer,
    isposted character varying(1),
    authaction character varying(1),
    journalblockid integer,
    channelcode character varying,
    sponsorid integer,
    donorid integer,
    volunteerid character varying(10),
    actualdate timestamp(6) without time zone,
    transactionno character varying(30),
    paidto character varying(30),
    donorno character varying(20),
    donorname character varying(150),
    amount numeric(38,2),
    currencycode character varying(5),
    receivedfrom character varying(30),
    marketerid integer,
    channelaccountno character varying(30),
    rate double precision,
    journalno character varying(30),
    hcbatchitemid integer,
    authoperationmode character varying(1),
    updatedate timestamp(6) without time zone,
    journalerrordescription character varying(200),
    flag_omit_journal character varying(1)
);


ALTER TABLE migration.coaconv_transaction_laz_noitem OWNER TO postgres;

--
-- Name: coaconv_transaction_remove_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transaction_remove_bck (
    transactionid integer,
    transactiondate timestamp(6) without time zone,
    referenceno character varying(30),
    description character varying(100),
    inputer character varying(20),
    transactioncode character varying(10),
    branchcode character varying(5),
    authuser character varying(20),
    transactiontime timestamp(6) without time zone,
    authdate timestamp(6) without time zone,
    authstatus character varying(1),
    batchid integer,
    isposted character varying(1),
    authaction character varying(1),
    journalblockid integer,
    channelcode character varying,
    sponsorid integer,
    donorid integer,
    volunteerid character varying(10),
    actualdate timestamp(6) without time zone,
    transactionno character varying(30),
    paidto character varying(30),
    donorno character varying(20),
    donorname character varying(150),
    amount numeric(38,2),
    currencycode character varying(5),
    receivedfrom character varying(30),
    marketerid integer,
    channelaccountno character varying(30),
    rate double precision,
    journalno character varying(30),
    hcbatchitemid integer,
    authoperationmode character varying(1),
    updatedate timestamp(6) without time zone,
    journalerrordescription character varying(200),
    flag_omit_journal character varying(1)
);


ALTER TABLE migration.coaconv_transaction_remove_bck OWNER TO postgres;

--
-- Name: coaconv_transaction_remove_suspect; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transaction_remove_suspect (
    transactionid integer
);


ALTER TABLE migration.coaconv_transaction_remove_suspect OWNER TO postgres;

--
-- Name: coaconv_transaction_wakaf_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transaction_wakaf_bck (
    transactionid integer,
    transactiondate timestamp(6) without time zone,
    referenceno character varying(30),
    description character varying(100),
    inputer character varying(20),
    transactioncode character varying(10),
    branchcode character varying(5),
    authuser character varying(20),
    transactiontime timestamp(6) without time zone,
    authdate timestamp(6) without time zone,
    authstatus character varying(1),
    batchid integer,
    isposted character varying(1),
    authaction character varying(1),
    journalblockid integer,
    channelcode character varying,
    sponsorid integer,
    donorid integer,
    volunteerid character varying(10),
    actualdate timestamp(6) without time zone,
    transactionno character varying(30),
    paidto character varying(30),
    donorno character varying(20),
    donorname character varying(150),
    amount numeric(38,2),
    currencycode character varying(5),
    receivedfrom character varying(30),
    marketerid integer,
    channelaccountno character varying(30),
    rate double precision,
    journalno character varying(30),
    hcbatchitemid integer,
    authoperationmode character varying(1),
    updatedate timestamp(6) without time zone,
    journalerrordescription character varying(200),
    flag_omit_journal character varying(1)
);


ALTER TABLE migration.coaconv_transaction_wakaf_bck OWNER TO postgres;

--
-- Name: coaconv_transaction_wakaf_candidate; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transaction_wakaf_candidate (
    transactionid integer
);


ALTER TABLE migration.coaconv_transaction_wakaf_candidate OWNER TO postgres;

--
-- Name: coaconv_transactionitem_laz_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transactionitem_laz_bck (
    transactionitemid integer,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE migration.coaconv_transactionitem_laz_bck OWNER TO postgres;

--
-- Name: coaconv_transactionitem_laz_old; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transactionitem_laz_old (
    transactionitemid integer,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE migration.coaconv_transactionitem_laz_old OWNER TO postgres;

--
-- Name: coaconv_transactionitem_remove_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transactionitem_remove_bck (
    transactionitemid integer,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE migration.coaconv_transactionitem_remove_bck OWNER TO postgres;

--
-- Name: coaconv_transactionitem_wakaf_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.coaconv_transactionitem_wakaf_bck (
    transactionitemid integer,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE migration.coaconv_transactionitem_wakaf_bck OWNER TO postgres;

--
-- Name: denomkhasanah; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.denomkhasanah (
    nomor_rekening character varying(20) NOT NULL,
    nama_rekening character varying(200),
    nilai_denominasi numeric(22,2) NOT NULL,
    jenis_denominasi character varying(1) NOT NULL,
    jumlah_denominasi numeric(22,2),
    jumlah_denominasi_tle numeric(22,2)
);


ALTER TABLE migration.denomkhasanah OWNER TO postgres;

--
-- Name: depr_fix_journalitem; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.depr_fix_journalitem (
    fl_journal character varying(30),
    journalitem_no integer,
    fl_account character varying(20),
    fl_account_fix text,
    accountinstance_id integer,
    accountinstance_id_fix integer
);


ALTER TABLE migration.depr_fix_journalitem OWNER TO postgres;

--
-- Name: depr_fix_transactionitem; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.depr_fix_transactionitem (
    transactionitemid integer,
    refaccountno character varying(30),
    glnumber character varying(30),
    journalno character varying(30),
    accountcode character varying(20),
    accountcode_fix text
);


ALTER TABLE migration.depr_fix_transactionitem OWNER TO postgres;

--
-- Name: enum_varchar; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.enum_varchar (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value character varying(3) DEFAULT NULL::character varying NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE migration.enum_varchar OWNER TO postgres;

--
-- Name: errorbatch; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.errorbatch (
    err_id numeric NOT NULL,
    id_batch numeric,
    primarycode character varying(50),
    error_code character varying(4),
    additional_desc character varying(200),
    line_number numeric
);


ALTER TABLE migration.errorbatch OWNER TO postgres;

--
-- Name: errorcode; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.errorcode (
    error_code character varying(4) NOT NULL,
    error_description character varying(200)
);


ALTER TABLE migration.errorcode OWNER TO postgres;

--
-- Name: financialaccount_migbalance; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.financialaccount_migbalance (
    accountno character varying(30) NOT NULL,
    saldo_awal numeric(36,10)
);


ALTER TABLE migration.financialaccount_migbalance OWNER TO postgres;

--
-- Name: glinterface_fidyah; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.glinterface_fidyah (
    interfaceid integer,
    interfacecode character varying(30),
    description character varying(100),
    accountcode character varying(20),
    accountname character varying(60),
    productid integer
);


ALTER TABLE migration.glinterface_fidyah OWNER TO postgres;

--
-- Name: journalitem_repair; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.journalitem_repair (
    journalitem_no integer,
    fl_journal character varying(30),
    fl_account character varying(20),
    account_code_baru character varying(20)
);


ALTER TABLE migration.journalitem_repair OWNER TO postgres;

--
-- Name: kasteller; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.kasteller (
    id_user character varying(20) NOT NULL,
    kode_cabang character varying(10),
    kode_valuta character varying(10),
    status_rekening numeric(22,0),
    saldo numeric(22,2)
);


ALTER TABLE migration.kasteller OWNER TO postgres;

--
-- Name: khasanah; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.khasanah (
    kode_cabang character varying(10) NOT NULL,
    nomor_rekening character varying(20),
    nama_rekening character varying(100),
    kode_valuta character varying(10),
    saldo numeric(22,2)
);


ALTER TABLE migration.khasanah OWNER TO postgres;

--
-- Name: konversi_kode_produk; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.konversi_kode_produk (
    kode_produk character varying(30) NOT NULL,
    kode_cabang character varying(10) NOT NULL,
    kode_produk_baru character varying(30)
);


ALTER TABLE migration.konversi_kode_produk OWNER TO postgres;

--
-- Name: konversi_nomor_rekening; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.konversi_nomor_rekening (
    nomor_rekening character varying(30) NOT NULL,
    kode_cabang character varying(10) NOT NULL,
    nomor_rekening_baru character varying(30)
);


ALTER TABLE migration.konversi_nomor_rekening OWNER TO postgres;

--
-- Name: list_glinterface; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.list_glinterface (
    jenis_produk character varying(10) NOT NULL,
    kode_interface character varying(20) NOT NULL,
    deskripsi character varying(50)
);


ALTER TABLE migration.list_glinterface OWNER TO postgres;

--
-- Name: parameterglobal; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.parameterglobal (
    kode_parameter character varying(20) NOT NULL,
    nilai_parameter_number numeric(36,10),
    deskripsi character varying(100),
    is_parameter_system character varying(1),
    nilai_parameter_tanggal timestamp(6) without time zone,
    nilai_parameter_string character varying(150)
);


ALTER TABLE migration.parameterglobal OWNER TO postgres;

--
-- Name: produkdeposito; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.produkdeposito (
    kode_produk character varying(10) NOT NULL,
    nama_produk character varying(30),
    kode_valuta character varying(5),
    saldo_minimum numeric(38,16),
    masa_perjanjian numeric,
    periode_perjanjian character varying(1),
    status character varying(1),
    is_kena_penalty character varying(1),
    nominal_penalty numeric(38,16),
    is_dapat_bagi_hasil character varying(1),
    nisbah_bonus_dasar numeric(38,16),
    is_override_bagihasilkhusus character varying(1),
    jarak_periode_bagihasil numeric(38,0),
    periode_bagi_hasil character varying(1),
    disposisi_bagi_hasil character varying(1),
    is_override_disposisi_bgh character varying(1),
    is_kena_zakat_bagi_hasil character varying(1),
    presentase_zakat_bagi_hasil numeric(38,16),
    is_override_zakatbagihasil character varying(1),
    is_kena_pajak character varying(1),
    tarif_pajak numeric(38,16),
    is_override_tarifpajak character varying(1),
    gl_saldo character varying(20),
    gl_biaya_bgh character varying(20),
    gl_pendapatan_lay character varying(20),
    gl_pajak character varying(20),
    gl_zakat character varying(20),
    gl_cadangan_bgh character varying(20),
    gl_jttn character varying(20),
    gl_jttr character varying(20),
    gl_hiba character varying(20),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.produkdeposito OWNER TO postgres;

--
-- Name: produkrencana; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.produkrencana (
    kode_produk character varying(10) NOT NULL,
    nama_produk character varying(30),
    kode_valuta character varying(5),
    jenis_akad character varying(1),
    setoran_awal_minimum numeric(36,10),
    status character varying(1),
    minimal_setoran_rutin numeric(38,10),
    jangka_waktu numeric,
    grace_periode_gagal_debet numeric,
    maksimal_gagal_debet numeric,
    biaya_gagal_debet numeric(38,10),
    biaya_penutupan_gagal_debet numeric(38,10),
    is_dapat_bagi_hasil character varying(1),
    nisbah_bonus_dasar numeric(36,10),
    is_override_bagihasilkhusus character varying(1),
    jarak_periode_bagihasil numeric(38,0),
    periode_bagi_hasil character varying(1),
    disposisi_bagi_hasil character varying(1),
    is_override_disposisi_bgh character varying(1),
    is_kena_zakat_bagi_hasil character varying(1),
    presentase_zakat_bagi_hasil numeric(36,10),
    is_override_zakatbagihasil character varying(1),
    is_kena_pajak character varying(1),
    tarif_pajak numeric(36,10),
    is_override_tarifpajak character varying(1),
    is_kena_biayalayananumum character varying(1),
    biaya_adm_bulanan numeric(36,10),
    sumber_biaya_adm numeric,
    is_blokir_debet character varying(1),
    is_blokir_kredit character varying(1),
    biaya_penutupan_rekening numeric(18,2),
    is_override_biaya_penutupan character varying(1),
    is_tidak_dormant character varying(1),
    jumlah_hari_jadi_tidak_aktif numeric(38,0),
    tanggal_acuan_dormant character varying(1),
    is_tutup_otomatis_dormant character varying(1),
    jumlah_hari_tutup_otomatis numeric(38,0),
    is_biaya_rekening_dormant character varying(1),
    biaya_rekening_dormant numeric(20,8),
    gl_saldo character varying(20),
    gl_biaya_bgh character varying(20),
    gl_pendapatan_lay character varying(20),
    gl_pajak character varying(20),
    gl_zakat character varying(20),
    gl_cadangan_bgh character varying(20),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.produkrencana OWNER TO postgres;

--
-- Name: produktabungan; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.produktabungan (
    kode_produk character varying(10) NOT NULL,
    nama_produk character varying(30),
    kode_valuta character varying(5),
    jenis_akad character varying(1),
    setoran_awal_minimum numeric(36,10),
    saldo_minimum numeric(38,16),
    status character varying(1),
    is_dapat_bagi_hasil character varying(1),
    nisbah_bonus_dasar numeric(36,10),
    is_override_bagihasilkhusus character varying(1),
    jarak_periode_bagihasil numeric(38,0),
    periode_bagi_hasil character varying(1),
    disposisi_bagi_hasil character varying(1),
    is_override_disposisi_bgh character varying(1),
    is_kena_zakat_bagi_hasil character varying(1),
    presentase_zakat_bagi_hasil numeric(36,10),
    is_override_zakatbagihasil character varying(1),
    is_kena_pajak character varying(1),
    tarif_pajak numeric(36,10),
    is_override_tarifpajak character varying(1),
    is_kena_biayalayananumum character varying(1),
    biaya_adm_bulanan numeric(36,10),
    sumber_biaya_adm numeric,
    is_blokir_debet character varying(1),
    is_blokir_kredit character varying(1),
    biaya_penutupan_rekening numeric(18,2),
    is_override_biaya_penutupan character varying(1),
    is_biaya_saldo_minimum character varying(1),
    biaya_saldo_minimum numeric(20,8),
    is_tidak_dormant character varying(1),
    jumlah_hari_jadi_tidak_aktif numeric(38,0),
    tanggal_acuan_dormant character varying(1),
    is_tutup_otomatis_dormant character varying(1),
    jumlah_hari_tutup_otomatis numeric(38,0),
    is_biaya_rekening_dormant character varying(1),
    biaya_rekening_dormant numeric(20,8),
    gl_saldo character varying(20),
    gl_biaya_bgh character varying(20),
    gl_pendapatan_lay character varying(20),
    gl_pajak character varying(20),
    gl_zakat character varying(20),
    gl_cadangan_bgh character varying(20),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.produktabungan OWNER TO postgres;

--
-- Name: repair_journalblock_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.repair_journalblock_bck (
    system_id character varying(10),
    class_id character varying(32),
    key_id integer,
    id_journalblock integer,
    dataid character varying(50),
    id_journalcreation integer,
    journal_no character varying(30),
    subsystemcode character varying(20),
    transaction_tag character varying(20)
);


ALTER TABLE migration.repair_journalblock_bck OWNER TO postgres;

--
-- Name: repair_journalitemupload_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.repair_journalitemupload_bck (
    fl_journal character varying(30),
    journalitem_no integer,
    fl_account character varying(20),
    amount_debit numeric(36,10),
    amount_credit numeric(36,10),
    description character varying(200),
    branch_code character varying(20),
    valuta_code character varying(20),
    rc_code character varying(20),
    generic_code character varying(20),
    fl_posting_account character varying(20),
    fl_project_no character varying(10),
    docoprstatus character varying(1),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journalitemstatus character varying(1),
    userid_posting character varying(20),
    userid_check character varying(20),
    dateposting timestamp(6) without time zone,
    datelastmod timestamp(6) without time zone,
    datecreate timestamp(6) without time zone,
    event_date timestamp(6) without time zone,
    journalitemtype character varying(1),
    kode_kurs character varying(20),
    nilai_kurs numeric(36,10),
    rpv_main integer,
    subsystemcode character varying(20),
    subaccountcode character varying(30),
    id_journalcreation integer,
    subaccountname character varying(100),
    accountinstance_id integer,
    id_journalblock integer,
    transaksirak_id integer,
    source_class_id character varying(32),
    source_key_id integer,
    additionaldescription character varying(200)
);


ALTER TABLE migration.repair_journalitemupload_bck OWNER TO postgres;

--
-- Name: repair_journalupload_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.repair_journalupload_bck (
    journal_no character varying(30),
    journal_date_posting timestamp(6) without time zone,
    description character varying(200),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journal_date_last_modified timestamp(6) without time zone,
    userid_posting character varying(20),
    is_posted character varying(1),
    journal_type character varying(10),
    journal_date timestamp(6) without time zone,
    lastitemno integer,
    status character varying(1),
    docoprstatus character varying(1),
    is_partlychecked character varying(1),
    branch_code character varying(5),
    transaction_date timestamp(6) without time zone,
    journal_state character varying(1),
    serial_no character varying(23),
    event_date timestamp(6) without time zone,
    lock_userid character varying(20),
    fl_origin_journal character varying(30),
    id_journalcreation integer,
    source_app character varying(30),
    source_app_class character varying(30),
    source_app_ref character varying(30),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4)
);


ALTER TABLE migration.repair_journalupload_bck OWNER TO postgres;

--
-- Name: repair_transaction_bck; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.repair_transaction_bck (
    transactionid integer,
    transactiondate timestamp(6) without time zone,
    referenceno character varying(30),
    description character varying(100),
    inputer character varying(20),
    transactioncode character varying(10),
    branchcode character varying(5),
    authuser character varying(20),
    transactiontime timestamp(6) without time zone,
    authdate timestamp(6) without time zone,
    authstatus character varying(1),
    batchid integer,
    isposted character varying(1),
    authaction character varying(1),
    journalblockid integer,
    channelcode character varying,
    sponsorid integer,
    donorid integer,
    volunteerid character varying(10),
    actualdate timestamp(6) without time zone,
    transactionno character varying(30),
    paidto character varying(30),
    donorno character varying(20),
    donorname character varying(150),
    amount numeric(38,2),
    currencycode character varying(5),
    receivedfrom character varying(30),
    marketerid integer,
    channelaccountno character varying(30),
    rate double precision,
    journalno character varying(30),
    hcbatchitemid integer,
    authoperationmode character varying(1),
    updatedate timestamp(6) without time zone,
    journalerrordescription character varying(200),
    flag_omit_journal character varying(1)
);


ALTER TABLE migration.repair_transaction_bck OWNER TO postgres;

--
-- Name: script_collection; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.script_collection (
    script_code character varying(15) NOT NULL,
    script_name character varying(100),
    script_description character varying(200),
    script_path character varying(200)
);


ALTER TABLE migration.script_collection OWNER TO postgres;

--
-- Name: seq_errorbatch; Type: SEQUENCE; Schema: migration; Owner: postgres
--

CREATE SEQUENCE migration.seq_errorbatch
    START WITH 852558
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE migration.seq_errorbatch OWNER TO postgres;

--
-- Name: seq_uploadbatch; Type: SEQUENCE; Schema: migration; Owner: postgres
--

CREATE SEQUENCE migration.seq_uploadbatch
    START WITH 4050
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE migration.seq_uploadbatch OWNER TO postgres;

--
-- Name: templatemigration; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.templatemigration (
    tplcode character varying(30) NOT NULL,
    tplname character varying(100),
    tpldesc character varying(200),
    tplfilename character varying(100),
    modulecode character varying(30),
    tpltablename character varying(30),
    tplmigrationscript character varying(200),
    is_nonstandard_template character varying(1),
    is_hidden_standard_upload character varying(1)
);


ALTER TABLE migration.templatemigration OWNER TO postgres;

--
-- Name: tmp_accountofficer; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_accountofficer (
    kode_ao character varying(20) NOT NULL,
    nama_ao character varying(100),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_accountofficer OWNER TO postgres;

--
-- Name: tmp_bankcash; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_bankcash (
    accountno character varying(30) NOT NULL,
    accountname character varying(100),
    branchcode character varying(10),
    currencycode character varying(10),
    balance numeric(36,10),
    accountcode character varying(20),
    cashcode character varying(10),
    isamilaccount character varying(1),
    fundcategory character varying(1),
    productcode character varying(20),
    bankaccountno character varying(30),
    bankcode character varying(10),
    isreconaccount character varying(1),
    status character varying(1),
    baris integer,
    id_batch integer NOT NULL
);


ALTER TABLE migration.tmp_bankcash OWNER TO postgres;

--
-- Name: tmp_coa; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_coa (
    accountcode character varying(20) NOT NULL,
    accountname character varying(100),
    accountparent character varying(20),
    isdetail character varying(1),
    accounttype character varying(1),
    issystem character varying(1),
    cpaaccountcode character varying(20),
    baris numeric,
    id_batch numeric NOT NULL,
    iscpaaccount character varying(1)
);


ALTER TABLE migration.tmp_coa OWNER TO postgres;

--
-- Name: tmp_denominasi_khasanah; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_denominasi_khasanah (
    nomor_rekening character varying(20) NOT NULL,
    nilai_denominasi numeric(36,10) NOT NULL,
    jenis_denominasi character varying(1) NOT NULL,
    jumlah_denominasi numeric,
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_denominasi_khasanah OWNER TO postgres;

--
-- Name: tmp_deposito; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_deposito (
    nomor_rekening character varying(20) NOT NULL,
    nama_rekening character varying(200),
    nomor_bilyet character varying(20),
    kode_cabang character varying(20),
    kode_valuta character varying(20),
    keterangan character varying(50),
    nomor_nasabah character varying(30),
    status_rekening numeric(22,0),
    kode_produk character varying(10),
    saldo numeric(22,8),
    saldo_penempatan numeric(22,8),
    tanggal_buka timestamp(6) without time zone,
    tanggal_tutup timestamp(6) without time zone,
    tanggal_jatuh_tempo_terakhir timestamp(6) without time zone,
    tanggal_jatuh_tempo_berikutnya timestamp(6) without time zone,
    tanggal_aktifitas_terakhir timestamp(6) without time zone,
    kode_ao character varying(20),
    status_confidential character varying(1),
    kode_confidential character varying(10),
    status_kelengkapan character varying(1),
    is_blokir character varying(1),
    keterangan_blokir character varying(200),
    blokir_oleh character varying(32),
    sistem_pemblokir character varying(20),
    is_dapat_bagi_hasil character varying(1),
    is_bagi_hasil_khusus character varying(1),
    nisbah_dasar numeric(22,8),
    spesial_nisbah numeric(22,8),
    aro_nisbah character varying(1),
    disposisi_nominal character varying(1),
    rekening_disposisi_nominal character varying(20),
    bank_transfer_nominal character varying(10),
    penerima_transfer_nominal character varying(32),
    disposisi_bagi_hasil character varying(1),
    rekening_disposisi_baghas character varying(20),
    bank_transfer_baghas character varying(32),
    penerima_transfer_baghas character varying(32),
    is_kena_zakat_bagi_hasil character varying(1),
    persentase_zakat_bagi_hasil numeric(22,8),
    is_kena_pajak character varying(1),
    tarif_pajak numeric(22,8),
    kode_pajak character varying(4),
    tanggal_baghas_terakhir timestamp(6) without time zone,
    tanggal_baghas_berikutnya timestamp(6) without time zone,
    is_kena_biayalayananumum character varying(1),
    is_kena_bea_materai character varying(1),
    jenis_penduduk character varying(1),
    kode_sumber_dana character varying(10),
    kode_tujuan_pembukaan character varying(10),
    alamat_kirim character varying(1),
    user_input character varying(20),
    user_otorisasi character varying(20),
    total_bagihasil numeric(22,8),
    total_pajak numeric(22,8),
    total_zakat numeric(22,8),
    cadangan_baghas_kapitalisir numeric(22,8),
    ekuivalen_rate numeric(22,8),
    is_sudah_cetak_bilyet character varying(1),
    is_sudah_disetor character varying(1),
    masa_perjanjian numeric(22,0),
    saldo_accrual_bagihasil numeric(22,8),
    baris numeric,
    id_batch numeric NOT NULL,
    infotransfer_norekening character varying(30),
    infotransfer_keterangan character varying(100),
    infotransfer_bank character varying(100),
    user_blokir character varying(30)
);


ALTER TABLE migration.tmp_deposito OWNER TO postgres;

--
-- Name: tmp_donorinactivated; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_donorinactivated (
    donorid integer NOT NULL,
    donorname character varying(200),
    lasttrxdate timestamp without time zone,
    id_batch integer NOT NULL
);


ALTER TABLE migration.tmp_donorinactivated OWNER TO postgres;

--
-- Name: tmp_glinterface; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_glinterface (
    baris numeric,
    id_batch numeric,
    kode_tx_class character varying(6),
    acc_type character varying(20),
    description character varying(100),
    kode_produk character varying(20),
    kode_gl character varying(20)
);


ALTER TABLE migration.tmp_glinterface OWNER TO postgres;

--
-- Name: tmp_histtransaksi_candidate; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_histtransaksi_candidate (
    id_transaksi numeric NOT NULL,
    id_detil_transaksi numeric,
    nomor_rekening character varying(30),
    tanggal_transaksi timestamp(6) without time zone,
    tanggal_input timestamp(6) without time zone,
    nilai_mutasi numeric(36,10),
    jenis_mutasi character varying(1),
    keterangan character varying(200),
    kode_transaksi character varying(20),
    nomor_referensi character varying(50),
    user_input character varying(30),
    user_otorisasi character varying(30),
    kode_cabang_transaksi character varying(10),
    jam_input timestamp(6) without time zone,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_histtransaksi_candidate OWNER TO postgres;

--
-- Name: tmp_histtransaksi_tabgir; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_histtransaksi_tabgir (
    nomor_rekening character varying(30) NOT NULL,
    nomor_urut numeric NOT NULL,
    nama_rekening character varying(100),
    tanggal_transaksi timestamp(6) without time zone,
    kode_transaksi character varying(20),
    jenis_mutasi character varying(1),
    nilai_mutasi numeric(36,10),
    keterangan character varying(200),
    baris numeric,
    id_batch numeric NOT NULL,
    kode_cabang character varying(10)
);


ALTER TABLE migration.tmp_histtransaksi_tabgir OWNER TO postgres;

--
-- Name: tmp_histtransaksi_tabgir_bus; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_histtransaksi_tabgir_bus (
    nomor_rekening character varying(30) NOT NULL,
    nomor_urut numeric NOT NULL,
    nama_rekening character varying(100),
    tanggal_transaksi timestamp(6) without time zone,
    kode_transaksi character varying(20),
    nominal_kredit numeric(36,10),
    nominal_debet numeric(36,10),
    keterangan character varying(200),
    baris numeric,
    id_batch numeric NOT NULL,
    kode_cabang character varying(10)
);


ALTER TABLE migration.tmp_histtransaksi_tabgir_bus OWNER TO postgres;

--
-- Name: tmp_journal_candidate; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_journal_candidate (
    journal_date timestamp without time zone,
    journal_no character varying(30) NOT NULL,
    description character varying(400),
    id_batch integer NOT NULL,
    reference_no character varying(50)
);


ALTER TABLE migration.tmp_journal_candidate OWNER TO postgres;

--
-- Name: tmp_journalitem_history; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_journalitem_history (
    journal_date timestamp without time zone,
    journal_no character varying(30),
    account_code character varying(30),
    branch_code character varying(10),
    currency_code character varying(10),
    amount_debet numeric(36,10),
    amount_credit numeric(36,10),
    description character varying(400),
    baris integer NOT NULL,
    id_batch integer NOT NULL,
    reference_no character varying(50)
);


ALTER TABLE migration.tmp_journalitem_history OWNER TO postgres;

--
-- Name: tmp_kasteller; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_kasteller (
    id_user character varying(30) NOT NULL,
    kode_cabang character varying(10),
    kode_valuta character varying(10),
    status_rekening character varying(1),
    saldo numeric(36,10),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_kasteller OWNER TO postgres;

--
-- Name: tmp_khasanah; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_khasanah (
    kode_cabang character varying(10) NOT NULL,
    kode_valuta character varying(10),
    saldo numeric(36,10),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_khasanah OWNER TO postgres;

--
-- Name: tmp_list_rek_disposisi_baghas; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_list_rek_disposisi_baghas (
    nomor_rekening character varying(20) NOT NULL,
    nomor_nasabah character varying(20),
    kode_produk character varying(10),
    saldo numeric(36,10),
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_list_rek_disposisi_baghas OWNER TO postgres;

--
-- Name: tmp_mappingcoa; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_mappingcoa (
    account_code_lama character varying(20) NOT NULL,
    account_code_baru character varying(20),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_mappingcoa OWNER TO postgres;

--
-- Name: tmp_mig_trans; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_mig_trans (
    id_batch numeric NOT NULL,
    nomor_rekening character varying(30),
    id_transaksi numeric NOT NULL
);


ALTER TABLE migration.tmp_mig_trans OWNER TO postgres;

--
-- Name: tmp_nasabahindividu; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_nasabahindividu (
    nomor_nasabah character varying(30) NOT NULL,
    nama_nasabah character varying(100),
    nama_singkat character varying(50),
    nama_lengkap_tanpa_gelar character varying(100),
    nama_ibu_kandung character varying(100),
    nama_gadis_ibu_kandung character varying(100),
    gelar_depan character varying(50),
    gelar_belakang character varying(50),
    tempat_lahir character varying(30),
    tanggal_lahir timestamp(6) without time zone,
    tanggal_buka timestamp(6) without time zone,
    alamat_email character varying(100),
    alamat_rumah_jalan character varying(150),
    alamat_rumah_rt character varying(10),
    alamat_rumah_rw character varying(10),
    alamat_rumah_kelurahan character varying(30),
    alamat_rumah_kecamatan character varying(30),
    alamat_rumah_kota_kabupaten character varying(30),
    alamat_rumah_provinsi character varying(30),
    alamat_rumah_kode_pos character varying(5),
    alamat_surat_jalan character varying(150),
    alamat_surat_rt character varying(10),
    alamat_surat_rw character varying(10),
    alamat_surat_kelurahan character varying(30),
    alamat_surat_kecamatan character varying(30),
    alamat_surat_kode_pos character varying(5),
    alamat_surat_kota_kabupaten character varying(30),
    alamat_surat_provinsi character varying(30),
    telepon_rumah_kode_negara character varying(5),
    telepon_rumah_kode_area character varying(5),
    telepon_rumah_nomor character varying(15),
    telepon_hp_kode_negara character varying(5),
    telepon_hp_nomor character varying(15),
    fax_kode_negara character varying(5),
    fax_kode_area character varying(5),
    fax_nomor character varying(15),
    status_keterkaitan character varying(1),
    jenis_penduduk character varying(1),
    jenis_identitas character varying(1),
    nomor_identitas character varying(30),
    tanggal_terbit_identitas timestamp(6) without time zone,
    tanggal_berakhir_identitas timestamp(6) without time zone,
    nomor_npwp_individu character varying(30),
    nomor_kitas character varying(50),
    tanggal_kadaluarsa_kitas timestamp(6) without time zone,
    is_external character varying(1),
    id_external character varying(20),
    kode_lembaga_external character varying(10),
    nama_grup character varying(20),
    kewarganegaraan character varying(5),
    pekerjaan character varying(5),
    jabatan_pekerjaan character varying(100),
    badan_hukum_pekerjaan character varying(5),
    bidang_usaha_pekerjaan character varying(5),
    sektor_ekonomi character varying(5),
    nama_perusahaan_kerja character varying(32),
    alamat_kerja_jalan character varying(100),
    alamat_kerja_rt character varying(10),
    alamat_kerja_rw character varying(10),
    alamat_kerja_kelurahan character varying(30),
    alamat_kerja_kecamatan character varying(30),
    alamat_kerja_kode_pos character varying(5),
    alamat_kerja_kota_kabupaten character varying(30),
    alamat_kerja_provinsi character varying(30),
    pendidikan character varying(1),
    telepon_kerja_kode_negara character varying(5),
    telepon_kerja_kode_area character varying(5),
    telepon_kerja_nomor character varying(15),
    fax_kerja_kode_negara character varying(5),
    fax_kerja_kode_area character varying(5),
    fax_kerja_nomor character varying(15),
    jenis_kelamin character varying(1),
    agama character varying(1),
    bahasa character varying(4),
    status_perkawinan character varying(1),
    golongan_debitur character varying(6),
    sid_din character varying(20),
    sid_id_debitur character varying(43),
    limit_nom_setor_tunai numeric(22,0),
    limit_nom_setor_nontunai numeric(22,0),
    limit_nom_tarik_tunai numeric(22,0),
    limit_nom_tarik_nontunai numeric(22,0),
    limit_frek_setor_tunai numeric(22,0),
    limit_frek_setor_nontunai numeric(22,0),
    limit_frek_tarik_tunai numeric(22,0),
    limit_frek_tarik_nontunai numeric(22,0),
    status_tempat_tinggal character varying(1),
    tanggal_mulai_menempati timestamp(6) without time zone,
    faktor_resiko character varying(6),
    resiko_identitas_nasabah character varying(1),
    resiko_lokasi_usaha character varying(1),
    resiko_profil_nasabah character varying(1),
    resiko_jumlah_transaksi character varying(1),
    resiko_kegiatan_usaha character varying(1),
    resiko_struktur_kepemilikan character varying(1),
    resiko_info_lainnya character varying(1),
    tujuan_buka_rekening character varying(100),
    tujuan_penggunaan_dana character varying(1),
    sumber_dana character varying(1),
    sumber_dana_lainnya character varying(100),
    penghasilan_utama_per_tahun character varying(2),
    kode_ao character varying(20),
    nama_keluarga_dihubungi character varying(100),
    telepon_keluarga_dihubungi character varying(20),
    dati_ii_domisili character varying(4),
    keterangan character varying(200),
    keterangan_tambahan character varying(200),
    alamat_kantor_i character varying(100),
    alamat_kantor_ii character varying(100),
    cif_lama character varying(10),
    telp_kantor_i character varying(20),
    telp_kantor_ii character varying(20),
    status character varying(1),
    hobi character varying(1),
    kode_cabang character varying(10),
    tahun_menempati_rumah numeric(10,0),
    bulan_menempati_rumah numeric(10,0),
    jumlah_tanggungan_istri numeric(10,0),
    jumlah_tanggungan_anak numeric(10,0),
    jumlah_tanggungan_orangtua numeric(10,0),
    pemberi_referensi character varying(50),
    wilayah_referensi character varying(50),
    user_input character varying(20),
    user_otorisasi character varying(20),
    tanggal_ubah timestamp(6) without time zone,
    jam_ubah timestamp(6) without time zone,
    st_nasabah_induk character varying(1),
    telepon_rumah_kode_area2 character varying(5),
    telepon_rumah_nomor2 character varying(15),
    telepon_kerja_kode_area2 character varying(5),
    telepon_kerja_nomor2 character varying(15),
    telepon_kerja_ext character varying(10),
    telepon_kerja_ext2 character varying(5),
    user_update character varying(20),
    tanggal_update timestamp(6) without time zone,
    baris numeric,
    id_batch numeric NOT NULL,
    negara_asal character varying(5)
);


ALTER TABLE migration.tmp_nasabahindividu OWNER TO postgres;

--
-- Name: tmp_neracasaldo; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_neracasaldo (
    account_code character varying(20) NOT NULL,
    branch_code character varying(10) NOT NULL,
    balance numeric(36,10),
    journal_date timestamp(6) without time zone,
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_neracasaldo OWNER TO postgres;

--
-- Name: tmp_neracasaldo_mapcoa; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_neracasaldo_mapcoa (
    account_code_lama character varying(20) NOT NULL,
    branch_code character varying(10) NOT NULL,
    balance numeric(36,10),
    journal_date timestamp(6) without time zone,
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_neracasaldo_mapcoa OWNER TO postgres;

--
-- Name: tmp_neracasaldo_nonmapping; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_neracasaldo_nonmapping (
    account_code character varying(20) NOT NULL,
    branch_code character varying(10) NOT NULL,
    balance numeric(36,10),
    journal_date timestamp(6) without time zone,
    baris integer,
    id_batch integer NOT NULL
);


ALTER TABLE migration.tmp_neracasaldo_nonmapping OWNER TO postgres;

--
-- Name: tmp_rekeningliabilitas_update; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_rekeningliabilitas_update (
    nomor_rekening character varying(20) NOT NULL,
    kode_marketing_pertama character varying(20),
    kode_marketing_referensi character varying(20),
    kode_marketing_current character varying(20),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_rekeningliabilitas_update OWNER TO postgres;

--
-- Name: tmp_rekeningperantara; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_rekeningperantara (
    nomor_rekening character varying(20) NOT NULL,
    nama_rekening character varying(100),
    kode_cabang character varying(10),
    kode_produk character varying(10),
    kode_valuta character varying(10),
    saldo numeric(36,10),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_rekeningperantara OWNER TO postgres;

--
-- Name: tmp_repair_saldo; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_repair_saldo (
    nomor_rekening character varying(20) NOT NULL,
    kode_cabang character varying(10),
    saldo_seharusnya numeric(36,10),
    saldo_migrasi numeric(36,10)
);


ALTER TABLE migration.tmp_repair_saldo OWNER TO postgres;

--
-- Name: tmp_saldo_awal_rekening; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_saldo_awal_rekening (
    nomor_rekening character varying(30) NOT NULL,
    kode_cabang character varying(10),
    saldo_awal numeric(36,10),
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_saldo_awal_rekening OWNER TO postgres;

--
-- Name: tmp_tabgir; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_tabgir (
    nomor_rekening character varying(20) NOT NULL,
    nama_rekening character varying(200),
    kode_cabang character varying(20),
    kode_valuta character varying(20),
    keterangan character varying(50),
    nomor_nasabah character varying(30),
    jenis_rekening character varying(1),
    join_account character varying(1),
    nomor_nasabah_joinaccount character varying(30),
    status_rekening numeric,
    kode_produk character varying(10),
    saldo numeric(22,8),
    tanggal_buka timestamp(6) without time zone,
    tanggal_aktifitas_terakhir timestamp(6) without time zone,
    kode_ao character varying(20),
    status_confidential character varying(1),
    kode_confidential character varying(10),
    status_kelengkapan character varying(1),
    flag_blokir_debet_internal character varying(1),
    flag_blokir_kredit_internal character varying(1),
    flag_blokir_debet_eksternal character varying(1),
    flag_blokir_kredit_eksternal character varying(1),
    flag_dormant character varying(1),
    flag_biaya_saldo_minimum character varying(1),
    flag_biaya_rekening_tidakaktif character varying(1),
    flag_biaya_atm character varying(1),
    flag_cetak_nota character varying(1),
    flag_cetak_passbook character varying(1),
    is_blokir character varying(1),
    keterangan_blokir character varying(200),
    blokir_oleh character varying(32),
    sistem_pemblokir character varying(20),
    is_dapat_bagi_hasil character varying(1),
    is_bagi_hasil_khusus character varying(1),
    nisbah_bagi_hasil numeric(22,8),
    spesial_nisbah numeric(22,8),
    is_kena_zakat_bagi_hasil character varying(1),
    persentase_zakat_bagi_hasil numeric(22,8),
    is_kena_pajak character varying(1),
    tarif_pajak numeric(22,8),
    is_kena_biayalayananumum character varying(1),
    is_kena_bea_materai character varying(1),
    kode_sumber_dana character varying(10),
    kode_tujuan_pembukaan character varying(10),
    alamat_kirim character varying(1),
    kolektibilitas character varying(1),
    bagi_hasil_terakhir numeric(22,8),
    bagi_hasil_sebelumnya numeric(22,8),
    tanggal_setor_terakhir timestamp(6) without time zone,
    tanggal_tarik_terakhir timestamp(6) without time zone,
    tanggal_tutup timestamp(6) without time zone,
    user_input character varying(20),
    user_otorisasi character varying(20),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_tabgir OWNER TO postgres;

--
-- Name: tmp_tabrencanarutin; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_tabrencanarutin (
    nomor_rekening character varying(20) NOT NULL,
    nama_rekening character varying(200),
    kode_cabang character varying(20),
    kode_valuta character varying(20),
    keterangan character varying(50),
    nomor_nasabah character varying(30),
    jenis_rekening character varying(1),
    join_account character varying(1),
    nomor_nasabah_joinaccount character varying(30),
    status_rekening numeric,
    kode_produk character varying(10),
    saldo numeric(22,8),
    tanggal_buka timestamp(6) without time zone,
    tanggal_aktifitas_terakhir timestamp(6) without time zone,
    kode_ao character varying(20),
    status_confidential character varying(1),
    kode_confidential character varying(10),
    status_kelengkapan character varying(1),
    flag_blokir_debet_internal character varying(1),
    flag_blokir_kredit_internal character varying(1),
    flag_blokir_debet_eksternal character varying(1),
    flag_blokir_kredit_eksternal character varying(1),
    flag_dormant character varying(1),
    flag_biaya_saldo_minimum character varying(1),
    flag_biaya_rekening_tidakaktif character varying(1),
    flag_biaya_atm character varying(1),
    flag_cetak_nota character varying(1),
    flag_cetak_passbook character varying(1),
    is_blokir character varying(1),
    keterangan_blokir character varying(200),
    blokir_oleh character varying(32),
    sistem_pemblokir character varying(20),
    is_dapat_bagi_hasil character varying(1),
    is_bagi_hasil_khusus character varying(1),
    nisbah_bagi_hasil numeric(22,8),
    spesial_nisbah numeric(22,8),
    is_kena_zakat_bagi_hasil character varying(1),
    persentase_zakat_bagi_hasil numeric(22,8),
    is_kena_pajak character varying(1),
    tarif_pajak numeric(22,8),
    is_kena_biayalayananumum character varying(1),
    is_kena_bea_materai character varying(1),
    kode_sumber_dana character varying(10),
    kode_tujuan_pembukaan character varying(10),
    alamat_kirim character varying(1),
    kolektibilitas character varying(1),
    bagi_hasil_terakhir numeric(22,8),
    bagi_hasil_sebelumnya numeric(22,8),
    tanggal_setor_terakhir timestamp(6) without time zone,
    tanggal_tarik_terakhir timestamp(6) without time zone,
    tanggal_tutup timestamp(6) without time zone,
    setoran_rutin numeric(36,10),
    jangka_waktu numeric(22,0),
    tanggal_setoran_rutin numeric(22,0),
    tanggal_jatuh_tempo timestamp(6) without time zone,
    nomor_rekening_induk character varying(20),
    user_input character varying(20),
    user_otorisasi character varying(20),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_tabrencanarutin OWNER TO postgres;

--
-- Name: tmp_tranjournal_candidate; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_tranjournal_candidate (
    id_transaksi numeric NOT NULL,
    id_batch numeric
);


ALTER TABLE migration.tmp_tranjournal_candidate OWNER TO postgres;

--
-- Name: tmp_update_nama_rekening; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_update_nama_rekening (
    nomor_rekening character varying(20) NOT NULL,
    nama character varying(100),
    alamat character varying(200),
    id_individu numeric,
    nomor_nasabah character varying(20)
);


ALTER TABLE migration.tmp_update_nama_rekening OWNER TO postgres;

--
-- Name: tmp_userapp; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_userapp (
    nomor_karyawan character varying(20) NOT NULL,
    nama_lengkap character varying(100),
    id_user character varying(30),
    kode_cabang character varying(10),
    kode_departemen character varying(10),
    role character varying(10),
    baris numeric,
    id_batch numeric NOT NULL
);


ALTER TABLE migration.tmp_userapp OWNER TO postgres;

--
-- Name: tmp_usertraining; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.tmp_usertraining (
    nomor_karyawan character varying(20) NOT NULL,
    nama_lengkap character varying(100),
    kode_cabang character varying(10),
    kode_departemen character varying(10),
    role character varying(10)
);


ALTER TABLE migration.tmp_usertraining OWNER TO postgres;

--
-- Name: uploadbatch; Type: TABLE; Schema: migration; Owner: postgres
--

CREATE TABLE migration.uploadbatch (
    id_batch numeric NOT NULL,
    upload_date timestamp(6) without time zone,
    tplcode character varying(10),
    upload_file_name character varying(100),
    user_input character varying(20),
    user_auth character varying(20),
    upload_state character varying(1),
    verify_date timestamp(6) without time zone,
    push_date timestamp(6) without time zone,
    user_verify character varying(30),
    user_push character varying(30),
    kode_cabang character varying(10)
);


ALTER TABLE migration.uploadbatch OWNER TO postgres;

--
-- Name: achievement; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.achievement (
    employeeid character varying(20) NOT NULL,
    achievementname character varying(100),
    achievementid integer NOT NULL,
    institution character varying(100),
    achievementdate timestamp(6) without time zone
);


ALTER TABLE personalia.achievement OWNER TO postgres;

--
-- Name: assettransaction; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.assettransaction (
    transactionid integer NOT NULL,
    assettranstype character varying(1),
    processid integer
);


ALTER TABLE personalia.assettransaction OWNER TO postgres;

--
-- Name: assettransactionitem; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.assettransactionitem (
    transactionitemid integer NOT NULL,
    deprassetid integer,
    assettransitemtype character varying(1),
    deprcostaccount character varying(20),
    depraccount character varying(20),
    deprperiode timestamp(6) without time zone,
    deprsequence integer
);


ALTER TABLE personalia.assettransactionitem OWNER TO postgres;

--
-- Name: attendance; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.attendance (
    attendanceid integer NOT NULL,
    attendancedate timestamp(6) without time zone,
    attendancestatus character varying(1),
    arrivalstatus character varying(2),
    description character varying(100),
    returntime time(6) without time zone,
    overtime1 double precision,
    overtime2 double precision,
    overtime3 double precision,
    overtime4 double precision,
    totalovertime double precision,
    arrivaluserinput character varying(20),
    arrivalterminalinput character varying(15),
    returnuserinput character varying(20),
    returnterminalinput character varying(15),
    employeeid character varying(20),
    arriveovertime double precision,
    returnovertime double precision,
    arrivetime time(6) without time zone,
    overtime5 double precision,
    attendancesymbol character varying(10),
    statusenum character varying(10),
    arriveovertimeminute integer
);


ALTER TABLE personalia.attendance OWNER TO postgres;

--
-- Name: attendancesymbols; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.attendancesymbols (
    attendancesymbol character varying(10) NOT NULL,
    symboldescription character varying(100),
    attendancestatus character varying(1)
);


ALTER TABLE personalia.attendancesymbols OWNER TO postgres;

--
-- Name: blobregistration; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.blobregistration (
    id integer NOT NULL,
    actualfilename character varying(128),
    istemporary character varying(1)
);


ALTER TABLE personalia.blobregistration OWNER TO postgres;

--
-- Name: branch; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.branch (
    branchcode character varying(3) NOT NULL,
    branchname character varying(30),
    branchid integer,
    shortcode character varying(5),
    isactive character varying(1)
);


ALTER TABLE personalia.branch OWNER TO postgres;

--
-- Name: branchlocation; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.branchlocation (
    branch_code character varying(5) NOT NULL,
    branchname character varying(50),
    branchstatus character varying(1),
    user_id character varying(20),
    last_update timestamp(6) without time zone,
    masterbranch_code character varying(5)
);


ALTER TABLE personalia.branchlocation OWNER TO postgres;

--
-- Name: careerhistory; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.careerhistory (
    careerhistoryid integer NOT NULL,
    employeeid character varying(20),
    workunitid character varying(50),
    positionid character varying(50),
    effectivedate timestamp(6) without time zone
);


ALTER TABLE personalia.careerhistory OWNER TO postgres;

--
-- Name: contracthistory; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.contracthistory (
    employeeid character varying(20),
    contractno character varying(100) NOT NULL,
    initialcontractperiod timestamp(6) without time zone,
    endcontractperiod timestamp(6) without time zone,
    description character varying(100)
);


ALTER TABLE personalia.contracthistory OWNER TO postgres;

--
-- Name: custom_idgen; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.custom_idgen (
    idname character varying(30) NOT NULL,
    idcode character varying(50) NOT NULL,
    last_id integer,
    locked character varying(1)
);


ALTER TABLE personalia.custom_idgen OWNER TO postgres;

--
-- Name: depreciableasset; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.depreciableasset (
    deprassetid integer NOT NULL,
    deprassetregnumber character varying(20),
    registerdate timestamp without time zone,
    inputdate timestamp without time zone,
    inputuser character varying(50),
    deprassettype character varying(1),
    deprassetname character varying(100),
    branchcode character varying(5),
    depreciationsequence integer,
    deprassetstate character varying(1),
    depreciationaccumvalue numeric(30,8)
);


ALTER TABLE personalia.depreciableasset OWNER TO postgres;

--
-- Name: depreciationprocesslog; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.depreciationprocesslog (
    processid integer NOT NULL,
    processdate timestamp without time zone,
    userid character varying(100),
    processtime timestamp without time zone
);


ALTER TABLE personalia.depreciationprocesslog OWNER TO postgres;

--
-- Name: disposisi; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.disposisi (
    disposisiid integer NOT NULL,
    dokumenid integer,
    employeeid character varying(20),
    workunitid character varying(50),
    positionid character varying(50),
    namadisposisi character varying(100),
    keterangandisposisi character varying(200),
    tanggal timestamp without time zone,
    disposisioleh character varying(100)
);


ALTER TABLE personalia.disposisi OWNER TO postgres;

--
-- Name: dokumen; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.dokumen (
    nomor character varying(50),
    perihal character varying(200),
    tanggaldokumen timestamp without time zone,
    tipedokumen character varying(1),
    filedokumen character varying(100),
    keterangan character varying(100),
    dokumenid integer NOT NULL,
    idjenisdokumen integer,
    userinput character varying(50),
    userubah character varying(50),
    tanggalinput timestamp without time zone,
    tanggalubah timestamp without time zone,
    branchcode character varying(10)
);


ALTER TABLE personalia.dokumen OWNER TO postgres;

--
-- Name: dokumenkeluar; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.dokumenkeluar (
    tujuan character varying(50),
    tanggalkirim timestamp without time zone,
    statuskirim character varying(1),
    pic character varying(150),
    jenisdokkeluar integer,
    dokumenid integer NOT NULL,
    konseptor character varying(150),
    workunitid character varying(50)
);


ALTER TABLE personalia.dokumenkeluar OWNER TO postgres;

--
-- Name: dokumenmasuk; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.dokumenmasuk (
    pengirim character varying(50),
    tanggalterima timestamp without time zone,
    diteruskanke integer,
    jenisdokmasuk character varying(1),
    dokumenid integer NOT NULL,
    ditujukanke character varying(100),
    nomoreksternaldokumen character varying(50)
);


ALTER TABLE personalia.dokumenmasuk OWNER TO postgres;

--
-- Name: education; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.education (
    educationid integer NOT NULL,
    individuid integer,
    eduyear character varying(4),
    eduinstitution character varying(100),
    educationtype character varying(1)
);


ALTER TABLE personalia.education OWNER TO postgres;

--
-- Name: employeeactivehistory; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.employeeactivehistory (
    historyid integer NOT NULL,
    employeeid character varying(20),
    activestatus character varying(1),
    description character varying(200),
    changedate timestamp without time zone
);


ALTER TABLE personalia.employeeactivehistory OWNER TO postgres;

--
-- Name: employeedevelopmentprogram; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.employeedevelopmentprogram (
    edpid integer NOT NULL,
    employeeid character varying(20),
    edpfile character varying(200),
    edplegalfile character varying(200),
    evaluatoremployee character varying(20),
    periodyear character varying(4),
    edpdate timestamp(6) without time zone,
    inputdate timestamp(6) without time zone
);


ALTER TABLE personalia.employeedevelopmentprogram OWNER TO postgres;

--
-- Name: employeetraining; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.employeetraining (
    trainingid integer NOT NULL,
    trainingdate timestamp(6) without time zone,
    trainingvalue character varying(20),
    certificate character varying(30),
    traininglocation character varying(100),
    employeeid character varying(20),
    trainingdateend timestamp(6) without time zone
);


ALTER TABLE personalia.employeetraining OWNER TO postgres;

--
-- Name: enum_int; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.enum_int (
    enum_name character varying(32) NOT NULL,
    enum_value integer NOT NULL,
    enum_description character varying(50)
);


ALTER TABLE personalia.enum_int OWNER TO postgres;

--
-- Name: enum_varchar; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.enum_varchar (
    enum_name character varying(32) NOT NULL,
    enum_value character varying(2) NOT NULL,
    enum_description character varying(50)
);


ALTER TABLE personalia.enum_varchar OWNER TO postgres;

--
-- Name: externalcontact; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.externalcontact (
    extcontactid integer NOT NULL,
    individuid integer,
    extcontacttype character varying(1),
    extorgid integer,
    extorgcontacttype character varying(1)
);


ALTER TABLE personalia.externalcontact OWNER TO postgres;

--
-- Name: externalorganization; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.externalorganization (
    extorgid integer NOT NULL,
    extorgcode character varying(20),
    extorgname character varying(150),
    extorgdescription character varying(200),
    extorgaddress character varying(100),
    extorgcity character varying(100),
    extorgtype character varying(1)
);


ALTER TABLE personalia.externalorganization OWNER TO postgres;

--
-- Name: family; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.family (
    familyid integer NOT NULL,
    individuid integer,
    gender character varying(1),
    familyname character varying(100),
    birthdate timestamp(6) without time zone,
    birthplace character varying(60),
    relationships integer,
    education integer,
    worksector character varying(100)
);


ALTER TABLE personalia.family OWNER TO postgres;

--
-- Name: fixedasset; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.fixedasset (
    deprassetid integer NOT NULL,
    isparent character varying(1),
    parentid integer,
    fatypeid integer,
    bookvalue numeric(30,4),
    initvalue numeric(30,4),
    depreciationvalue numeric(30,4),
    model character varying(100),
    description character varying DEFAULT 300,
    lastdeprdate timestamp without time zone,
    nextdeprdate timestamp without time zone,
    isinsured character varying(1),
    insuranceduedate timestamp(6) without time zone,
    stnkduedate timestamp(6) without time zone,
    fixedassetcategory character varying(1),
    fundentity integer,
    retiredate timestamp without time zone,
    retirereason character varying(1),
    retiredescription character varying(200),
    fixedassetstatus character varying(1)
);


ALTER TABLE personalia.fixedasset OWNER TO postgres;

--
-- Name: fixedassettype; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.fixedassettype (
    fatypeid integer NOT NULL,
    fatypecode character varying(10),
    fatypedescription character varying(100),
    fatypename character varying(100),
    parenttypeid integer,
    isdetail character varying(1),
    isdepreciable character varying(1),
    fatypedepreciationtime integer,
    glicontainerid integer
);


ALTER TABLE personalia.fixedassettype OWNER TO postgres;

--
-- Name: formaleducation; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.formaleducation (
    educationid integer NOT NULL,
    educationname integer
);


ALTER TABLE personalia.formaleducation OWNER TO postgres;

--
-- Name: glinterfacecontainer; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.glinterfacecontainer (
    glicontainerid integer NOT NULL,
    glicontainercode character varying(30),
    glicontainername character varying(50)
);


ALTER TABLE personalia.glinterfacecontainer OWNER TO postgres;

--
-- Name: glinterfacemember; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.glinterfacemember (
    glimemberid integer NOT NULL,
    accountcode character varying(20),
    accountname character varying(100),
    glimembercode character varying(20),
    description character varying(100),
    glicontainerid integer
);


ALTER TABLE personalia.glinterfacemember OWNER TO postgres;

--
-- Name: healthplafond; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.healthplafond (
    employeeid character varying(20) NOT NULL,
    empid character varying(20),
    outpatientplafond double precision,
    inpatientplafond double precision,
    totalplafond double precision,
    realization double precision,
    finalbalance double precision,
    currentyear character varying(4)
);


ALTER TABLE personalia.healthplafond OWNER TO postgres;

--
-- Name: healthreimbursement; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.healthreimbursement (
    rank integer NOT NULL,
    reimbursementtype character varying(2) NOT NULL,
    maritalstatus character varying(2) NOT NULL,
    reimbursementvalue double precision,
    description character varying(100)
);


ALTER TABLE personalia.healthreimbursement OWNER TO postgres;

--
-- Name: id_gen; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.id_gen (
    id_code character varying(50) NOT NULL,
    last_id integer,
    locked character varying(1)
);


ALTER TABLE personalia.id_gen OWNER TO postgres;

--
-- Name: innormalinvtransactitem; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.innormalinvtransactitem (
    transactionitemid integer NOT NULL,
    inormalinvtitype character varying(1)
);


ALTER TABLE personalia.innormalinvtransactitem OWNER TO postgres;

--
-- Name: inventory; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.inventory (
    invid integer NOT NULL,
    invcode character varying(10),
    invname character varying(100),
    invtype character varying(1),
    invunitid integer
);


ALTER TABLE personalia.inventory OWNER TO postgres;

--
-- Name: inventorystock; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.inventorystock (
    invstockid integer NOT NULL,
    qty double precision,
    invid integer,
    branchcode character varying(5)
);


ALTER TABLE personalia.inventorystock OWNER TO postgres;

--
-- Name: inventorytransaction; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.inventorytransaction (
    transactionid integer NOT NULL,
    invtranstype character varying(1),
    ponumber character varying(50),
    receiveby character varying(100)
);


ALTER TABLE personalia.inventorytransaction OWNER TO postgres;

--
-- Name: inventorytransactionitem; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.inventorytransactionitem (
    transactionitemid integer NOT NULL,
    qty numeric(10,2),
    invtransitemtype character varying(1),
    invid integer,
    normalinvtitype character varying(1),
    innormalinvtitype character varying(1),
    outnormalinvtitype character varying(1),
    invintransitemtype character varying(1),
    invouttransitemtype character varying(1),
    invstockid integer,
    qtybefore integer
);


ALTER TABLE personalia.inventorytransactionitem OWNER TO postgres;

--
-- Name: inventoryunit; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.inventoryunit (
    invunitid integer NOT NULL,
    invunitcode character varying(10),
    invunitname character varying(30),
    status character varying(1)
);


ALTER TABLE personalia.inventoryunit OWNER TO postgres;

--
-- Name: invreceivetransaction; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.invreceivetransaction (
    transactionid integer NOT NULL,
    ponumber character varying(50),
    receiveby character varying(100)
);


ALTER TABLE personalia.invreceivetransaction OWNER TO postgres;

--
-- Name: islamorganization; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.islamorganization (
    extorgid integer NOT NULL
);


ALTER TABLE personalia.islamorganization OWNER TO postgres;

--
-- Name: islamorgcontactperson; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.islamorgcontactperson (
    extcontactid integer NOT NULL
);


ALTER TABLE personalia.islamorgcontactperson OWNER TO postgres;

--
-- Name: jenisdokumen; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.jenisdokumen (
    idjenisdokumen integer NOT NULL,
    kodejenisdokumen character varying(10),
    namajenisdokumen character varying(50)
);


ALTER TABLE personalia.jenisdokumen OWNER TO postgres;

--
-- Name: journalist; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.journalist (
    extcontactid integer NOT NULL
);


ALTER TABLE personalia.journalist OWNER TO postgres;

--
-- Name: logincorporate; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.logincorporate (
    login character varying(20) NOT NULL,
    employeeid character varying(20)
);


ALTER TABLE personalia.logincorporate OWNER TO postgres;

--
-- Name: newsagency; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.newsagency (
    extorgid integer NOT NULL
);


ALTER TABLE personalia.newsagency OWNER TO postgres;

--
-- Name: nonformaleducation; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.nonformaleducation (
    educationid integer NOT NULL,
    educationname character varying(100)
);


ALTER TABLE personalia.nonformaleducation OWNER TO postgres;

--
-- Name: normalinventory; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.normalinventory (
    invid integer NOT NULL
);


ALTER TABLE personalia.normalinventory OWNER TO postgres;

--
-- Name: normalinvreceive; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.normalinvreceive (
    transactionitemid integer NOT NULL
);


ALTER TABLE personalia.normalinvreceive OWNER TO postgres;

--
-- Name: normalinvretur; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.normalinvretur (
    transactionitemid integer NOT NULL
);


ALTER TABLE personalia.normalinvretur OWNER TO postgres;

--
-- Name: normalinvtransactitem; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.normalinvtransactitem (
    transactionitemid integer NOT NULL,
    normalinvtitype character varying(1),
    innormalinvtitype character varying(1),
    outnormalinvtitype character varying(1)
);


ALTER TABLE personalia.normalinvtransactitem OWNER TO postgres;

--
-- Name: offwork; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.offwork (
    offworkid integer NOT NULL,
    applicationdate timestamp(6) without time zone,
    offworkbegin timestamp(6) without time zone,
    offworkend timestamp(6) without time zone,
    intervalday integer,
    applicationstatus character varying(1),
    offworkstatus character varying(1),
    userinput character varying(20),
    dateinput timestamp(6) without time zone,
    terminalinput character varying(15),
    userapprover character varying(20),
    dateapprover timestamp(6) without time zone,
    terminalapprover character varying(15),
    userproceed character varying(20),
    dateproceed timestamp(6) without time zone,
    terminalproceed character varying(15),
    employeeid character varying(20),
    comebackworkdate timestamp(6) without time zone,
    offworktype character varying(1),
    offworkaddress character varying(200)
);


ALTER TABLE personalia.offwork OWNER TO postgres;

--
-- Name: offworkmaternity; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.offworkmaternity (
    offworkid integer NOT NULL,
    maternitytype character varying(1),
    children integer,
    maternityestimatedate timestamp(6) without time zone
);


ALTER TABLE personalia.offworkmaternity OWNER TO postgres;

--
-- Name: offworkpermit; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.offworkpermit (
    offworkid integer NOT NULL,
    permitdescription integer,
    description character varying(100)
);


ALTER TABLE personalia.offworkpermit OWNER TO postgres;

--
-- Name: offworkplafond; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.offworkplafond (
    employeeid character varying(20) NOT NULL,
    previousyearplafond integer,
    currentyearplafond integer,
    cutibesarbegin timestamp(6) without time zone,
    currentyear character varying(4),
    iscurrentallowancetaken character varying(1),
    ispreviousallowancetaken character varying(1),
    empid character varying(20),
    iscutibesar character varying(1),
    allowance character varying(20),
    currentallowancedate timestamp(6) without time zone,
    previousallowancedate timestamp(6) without time zone
);


ALTER TABLE personalia.offworkplafond OWNER TO postgres;

--
-- Name: offworkregular; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.offworkregular (
    offworkid integer NOT NULL,
    isallowancetaken character varying(1),
    offworkyear character varying(4),
    note character varying(200)
);


ALTER TABLE personalia.offworkregular OWNER TO postgres;

--
-- Name: organizationexperience; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.organizationexperience (
    organizationexperienceid integer NOT NULL,
    individuid integer,
    orgyear character varying(4),
    orginstitution character varying(100),
    orgposition character varying(100),
    orgjobdesk character varying(200)
);


ALTER TABLE personalia.organizationexperience OWNER TO postgres;

--
-- Name: outnormalinvtransactitem; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.outnormalinvtransactitem (
    transactionitemid integer NOT NULL,
    outnormalinvtitype character varying(1)
);


ALTER TABLE personalia.outnormalinvtransactitem OWNER TO postgres;

--
-- Name: parameterglobal; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.parameterglobal (
    kode_parameter character varying(10) NOT NULL,
    tipe_parameter character varying(1),
    nilai_parameter double precision,
    deskripsi character varying(60),
    is_parameter_system character varying(1),
    nilai_parameter_tanggal timestamp(6) without time zone,
    nilai_parameter_string character varying(30),
    tag character varying(15),
    default_code character varying(30)
);


ALTER TABLE personalia.parameterglobal OWNER TO postgres;

--
-- Name: parameterjournal; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.parameterjournal (
    parameterjournalid integer NOT NULL,
    description character varying(100),
    datasource character varying(30),
    journalcode character varying(5)
);


ALTER TABLE personalia.parameterjournal OWNER TO postgres;

--
-- Name: parameterjournalitem; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.parameterjournalitem (
    parameterjournalitemid integer NOT NULL,
    accountcode character varying(20),
    branchbase character varying(1),
    description character varying(50),
    basesign character varying(1),
    currencybase character varying(1),
    amountbase character varying(30),
    ratebase character varying(30),
    accountbase character varying(1),
    parameterjournalid integer
);


ALTER TABLE personalia.parameterjournalitem OWNER TO postgres;

--
-- Name: performanceappraisal; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.performanceappraisal (
    performanceappraisalid integer NOT NULL,
    workunit character varying(50),
    initialperiod timestamp(6) without time zone,
    endingperiod timestamp(6) without time zone,
    "position" character varying(50),
    positioneffectivedate timestamp(6) without time zone,
    rank integer,
    rankeffectivedate timestamp(6) without time zone,
    lastsalary double precision,
    appraisaldate timestamp(6) without time zone,
    totalvalue double precision,
    appraisalannotation character varying(500),
    evaluatoremployee character varying(20),
    inputuser character varying(20),
    inputterminal character varying(15),
    inputdate timestamp(6) without time zone,
    opinionannotation character varying(500),
    generalvaluescale character varying(2),
    employeeopinion character varying(2),
    employeeid character varying(20),
    yearperiod character varying(4),
    filelegalpa character varying(200)
);


ALTER TABLE personalia.performanceappraisal OWNER TO postgres;

--
-- Name: performanceitem; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.performanceitem (
    performanceitemid integer NOT NULL,
    parentid integer,
    value double precision,
    subtotalvalue double precision,
    valueweightpercentage integer,
    performancevaluescale character varying(2),
    parameterid character varying(20),
    performanceappraisalid integer
);


ALTER TABLE personalia.performanceitem OWNER TO postgres;

--
-- Name: performanceparameter; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.performanceparameter (
    parameterid character varying(20) NOT NULL,
    parametername character varying(100),
    description character varying(500),
    parentid character varying(20),
    isactive character varying(1),
    level integer,
    isdetaillevel character varying(1),
    weightpercentage integer
);


ALTER TABLE personalia.performanceparameter OWNER TO postgres;

--
-- Name: performanceworkunitparameter; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.performanceworkunitparameter (
    workunitid character varying(50) NOT NULL,
    parameterid character varying(20) NOT NULL,
    weightpercentage integer
);


ALTER TABLE personalia.performanceworkunitparameter OWNER TO postgres;

--
-- Name: position; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia."position" (
    positionid character varying(50) NOT NULL,
    description character varying(200),
    jobdescription character varying(500),
    status character varying(1),
    nonactivedate timestamp(6) without time zone
);


ALTER TABLE personalia."position" OWNER TO postgres;

--
-- Name: rankhistory; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.rankhistory (
    rankhistoryid integer NOT NULL,
    employeeid character varying(20),
    rank integer,
    rankeffectivedate timestamp(6) without time zone
);


ALTER TABLE personalia.rankhistory OWNER TO postgres;

--
-- Name: regionarea; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.regionarea (
    regionareaid integer NOT NULL,
    regionareacode character varying(10),
    regionareaname character varying(100)
);


ALTER TABLE personalia.regionarea OWNER TO postgres;

--
-- Name: regionrepresentation; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.regionrepresentation (
    regionrepresentionid integer NOT NULL,
    individuid integer,
    regionareaid integer
);


ALTER TABLE personalia.regionrepresentation OWNER TO postgres;

--
-- Name: reimbursementrealization; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.reimbursementrealization (
    reimbursementrealizationid integer NOT NULL,
    reimbursementdate timestamp(6) without time zone,
    realizationvalue double precision,
    nominal double precision,
    finalbalance double precision,
    employeeid character varying(20),
    beginbalance double precision,
    isauthorized character varying(1),
    islast character varying(1)
);


ALTER TABLE personalia.reimbursementrealization OWNER TO postgres;

--
-- Name: salaryhistory; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.salaryhistory (
    salaryhistoryid integer NOT NULL,
    salaryreceiveddate timestamp(6) without time zone,
    workunit character varying(50),
    "position" character varying(50),
    description character varying(200),
    salaryvalue double precision,
    employeeid character varying(20),
    salaryschemeid integer,
    monthperiod integer,
    yearperiod character varying(4)
);


ALTER TABLE personalia.salaryhistory OWNER TO postgres;

--
-- Name: salaryitemhistory; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.salaryitemhistory (
    salaryitemid integer NOT NULL,
    salaryitemvalue double precision,
    salaryhistoryid integer,
    salaryitemschemeid integer,
    description character varying(10)
);


ALTER TABLE personalia.salaryitemhistory OWNER TO postgres;

--
-- Name: salaryitemparameter; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.salaryitemparameter (
    salaryitemparameterid integer NOT NULL,
    parametername character varying(100),
    isactive character varying(1),
    description character varying(200),
    itemvaluedefault double precision,
    formuladefault character varying(100),
    salaryitemperiod character varying(1),
    salaryitemtypedefault character varying(1),
    parametergroupid character varying(20)
);


ALTER TABLE personalia.salaryitemparameter OWNER TO postgres;

--
-- Name: salaryitemparametergroup; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.salaryitemparametergroup (
    parametergroupid character varying(20) NOT NULL,
    description character varying(200)
);


ALTER TABLE personalia.salaryitemparametergroup OWNER TO postgres;

--
-- Name: salaryitemscheme; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.salaryitemscheme (
    salaryitemschemeid integer NOT NULL,
    salaryitemschemename character varying(50),
    description character varying(200),
    isactive character varying(1),
    itemvalue double precision,
    formula character varying(100),
    salaryitemtype character varying(1),
    salaryschemeid integer
);


ALTER TABLE personalia.salaryitemscheme OWNER TO postgres;

--
-- Name: salaryscheme; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.salaryscheme (
    salaryschemeid integer NOT NULL,
    salaryschemename character varying(50),
    isactive character varying(1),
    positionid character varying(50)
);


ALTER TABLE personalia.salaryscheme OWNER TO postgres;

--
-- Name: seq_achievement; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_achievement
    START WITH 11
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_achievement OWNER TO postgres;

--
-- Name: seq_attendance; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_attendance
    START WITH 2163
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_attendance OWNER TO postgres;

--
-- Name: seq_careerhistory; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_careerhistory
    START WITH 86
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_careerhistory OWNER TO postgres;

--
-- Name: seq_depreciableasset; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_depreciableasset
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_depreciableasset OWNER TO postgres;

--
-- Name: seq_depreciationprocesslog; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_depreciationprocesslog
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_depreciationprocesslog OWNER TO postgres;

--
-- Name: seq_disposisi; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_disposisi
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_disposisi OWNER TO postgres;

--
-- Name: seq_dokumen; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_dokumen
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_dokumen OWNER TO postgres;

--
-- Name: seq_education; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_education
    START WITH 183
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_education OWNER TO postgres;

--
-- Name: seq_employeeactivehistory; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_employeeactivehistory
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_employeeactivehistory OWNER TO postgres;

--
-- Name: seq_employeedevelopmentprogram; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_employeedevelopmentprogram
    START WITH 9
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_employeedevelopmentprogram OWNER TO postgres;

--
-- Name: seq_externalcontact; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_externalcontact
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_externalcontact OWNER TO postgres;

--
-- Name: seq_externalorganization; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_externalorganization
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_externalorganization OWNER TO postgres;

--
-- Name: seq_family; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_family
    START WITH 147
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_family OWNER TO postgres;

--
-- Name: seq_fixedassettype; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_fixedassettype
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_fixedassettype OWNER TO postgres;

--
-- Name: seq_glinterfacecontainer; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_glinterfacecontainer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_glinterfacecontainer OWNER TO postgres;

--
-- Name: seq_glinterfacemember; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_glinterfacemember
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_glinterfacemember OWNER TO postgres;

--
-- Name: seq_individu; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_individu
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_individu OWNER TO postgres;

--
-- Name: seq_inventory; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_inventory
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_inventory OWNER TO postgres;

--
-- Name: seq_inventorystock; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_inventorystock
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_inventorystock OWNER TO postgres;

--
-- Name: seq_inventoryunit; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_inventoryunit
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_inventoryunit OWNER TO postgres;

--
-- Name: seq_jenisdokumen; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_jenisdokumen
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_jenisdokumen OWNER TO postgres;

--
-- Name: seq_offwork; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_offwork
    START WITH 18
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_offwork OWNER TO postgres;

--
-- Name: seq_organizationexperience; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_organizationexperience
    START WITH 77
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_organizationexperience OWNER TO postgres;

--
-- Name: seq_performanceappraisal; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_performanceappraisal
    START WITH 4
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_performanceappraisal OWNER TO postgres;

--
-- Name: seq_performanceitem; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_performanceitem
    START WITH 109
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_performanceitem OWNER TO postgres;

--
-- Name: seq_rankhistory; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_rankhistory
    START WITH 69
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_rankhistory OWNER TO postgres;

--
-- Name: seq_regionarea; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_regionarea
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_regionarea OWNER TO postgres;

--
-- Name: seq_regionrepresentation; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_regionrepresentation
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_regionrepresentation OWNER TO postgres;

--
-- Name: seq_reimbursementrealization; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_reimbursementrealization
    START WITH 162
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_reimbursementrealization OWNER TO postgres;

--
-- Name: seq_salaryhistory; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_salaryhistory
    START WITH 11
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_salaryhistory OWNER TO postgres;

--
-- Name: seq_salaryitemhistory; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_salaryitemhistory
    START WITH 107
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_salaryitemhistory OWNER TO postgres;

--
-- Name: seq_salaryitemparameter; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_salaryitemparameter
    START WITH 19
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_salaryitemparameter OWNER TO postgres;

--
-- Name: seq_salaryitemscheme; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_salaryitemscheme
    START WITH 160
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_salaryitemscheme OWNER TO postgres;

--
-- Name: seq_salaryscheme; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_salaryscheme
    START WITH 11
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_salaryscheme OWNER TO postgres;

--
-- Name: seq_targetachievement; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_targetachievement
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_targetachievement OWNER TO postgres;

--
-- Name: seq_training; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_training
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_training OWNER TO postgres;

--
-- Name: seq_transaction; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_transaction
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_transaction OWNER TO postgres;

--
-- Name: seq_transactionitem; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_transactionitem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_transactionitem OWNER TO postgres;

--
-- Name: seq_workexperience; Type: SEQUENCE; Schema: personalia; Owner: postgres
--

CREATE SEQUENCE personalia.seq_workexperience
    START WITH 108
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE personalia.seq_workexperience OWNER TO postgres;

--
-- Name: sessionblob; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.sessionblob (
    id integer NOT NULL,
    sessionid character varying(100),
    sessioncontext integer,
    id1 integer
);


ALTER TABLE personalia.sessionblob OWNER TO postgres;

--
-- Name: targetachievement; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.targetachievement (
    targetachievementid integer NOT NULL,
    evaluatoremployee character varying(20),
    inputdate timestamp(6) without time zone,
    inputterminal character varying(15),
    inputuser character varying(20),
    targetfile character varying(200),
    achievementfile character varying(200),
    targetdate timestamp(6) without time zone,
    lastsalary double precision,
    periodyear character varying(4),
    workunit character varying(50),
    positionid character varying(50),
    positioneffectivedate timestamp(6) without time zone,
    rank integer,
    rankeffectivedate timestamp(6) without time zone,
    employeeid character varying(20),
    achievementlegalfile character varying(200),
    targetlegalfile character varying(200),
    achievementdate timestamp(6) without time zone
);


ALTER TABLE personalia.targetachievement OWNER TO postgres;

--
-- Name: training; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.training (
    trainingid integer NOT NULL,
    individuid integer,
    materi character varying(100),
    institution character varying(100),
    trainingtype character varying(1)
);


ALTER TABLE personalia.training OWNER TO postgres;

--
-- Name: trainingseminar; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.trainingseminar (
    trainingid integer NOT NULL,
    status character varying(100),
    year character varying(4)
);


ALTER TABLE personalia.trainingseminar OWNER TO postgres;

--
-- Name: transaction; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.transaction (
    transactionid integer NOT NULL,
    transactiondate timestamp without time zone,
    inputdate timestamp without time zone,
    editdate timestamp without time zone,
    inputuser character varying(30),
    edituser character varying(30),
    transactiontype character varying(1),
    transactionno character varying(30),
    description character varying(200),
    referencenumber character varying(30),
    branchcode character varying(10),
    core_transactionid integer,
    authuser character varying(50),
    authdate timestamp(6) without time zone
);


ALTER TABLE personalia.transaction OWNER TO postgres;

--
-- Name: transactionitem; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.transactionitem (
    transactionitemid integer NOT NULL,
    transactionitemtype character varying(1),
    branchcode character varying(10),
    description character varying(200),
    transactionid integer,
    amount numeric(30,8)
);


ALTER TABLE personalia.transactionitem OWNER TO postgres;

--
-- Name: workexperience; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.workexperience (
    workexperienceid integer NOT NULL,
    individuid integer,
    workyear character varying(4),
    workinstitution character varying(100),
    workposition character varying(100),
    workjobdesk character varying(200)
);


ALTER TABLE personalia.workexperience OWNER TO postgres;

--
-- Name: workunit; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.workunit (
    workunitid character varying(50) NOT NULL,
    description character varying(200),
    parentid character varying(50),
    status character varying(1),
    nonactivedate timestamp(6) without time zone
);


ALTER TABLE personalia.workunit OWNER TO postgres;

--
-- Name: workunitposition; Type: TABLE; Schema: personalia; Owner: postgres
--

CREATE TABLE personalia.workunitposition (
    workunitid character varying(50) NOT NULL,
    positionid character varying(50) NOT NULL,
    jobdeskfile character varying(100)
);


ALTER TABLE personalia.workunitposition OWNER TO postgres;

--
-- Name: account; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.account (
    account_code character varying(20) NOT NULL,
    account_name character varying(100),
    account_level integer,
    is_detail character varying(1)
);


ALTER TABLE program.account OWNER TO postgres;

--
-- Name: accounttransactionitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.accounttransactionitem (
    accounttitype character varying(1),
    transactionitemid integer NOT NULL,
    fundentity integer,
    isupdatebalance character varying(1),
    accountno character varying(30)
);


ALTER TABLE program.accounttransactionitem OWNER TO postgres;

--
-- Name: activityappraisal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.activityappraisal (
    activityappraisalid integer NOT NULL,
    appraisaldate timestamp(6) without time zone,
    weekperiod integer,
    monthperiod integer,
    anualperiod integer,
    appraisalyear character varying(4),
    approvalstatus character varying(1),
    otherappraisalid integer,
    otherappraisalflag character varying(1),
    mustahiqid integer,
    companionid integer
);


ALTER TABLE program.activityappraisal OWNER TO postgres;

--
-- Name: activityappraisalitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.activityappraisalitem (
    itemid integer NOT NULL,
    integervalue integer,
    floatvalue double precision,
    stringvalue character varying(200),
    boolvalue character varying(1),
    activityappraisalid integer,
    itemtemplateid integer
);


ALTER TABLE program.activityappraisalitem OWNER TO postgres;

--
-- Name: activityappraisalitemtemplate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.activityappraisalitemtemplate (
    itemtemplateid integer NOT NULL,
    sequenceno integer,
    description character varying(200),
    isactive character varying(1),
    productid integer,
    mustahiqid integer,
    integervaluestandard integer,
    floatvaluestandard double precision,
    stringvaluestandard character varying(200),
    boolvaluestandard character varying(1),
    itemname character varying(50),
    groupname character varying(20),
    valuedatatype character varying(1),
    productgroupname character varying(50)
);


ALTER TABLE program.activityappraisalitemtemplate OWNER TO postgres;

--
-- Name: agenda; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.agenda (
    agendaid integer NOT NULL,
    agendatemplateid integer,
    mustahiqid integer,
    productid integer,
    mustahiqproductid integer
);


ALTER TABLE program.agenda OWNER TO postgres;

--
-- Name: agendaitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.agendaitem (
    agendaid integer,
    agendaitemid integer NOT NULL,
    agendaitemtemplateid integer,
    attendance integer
);


ALTER TABLE program.agendaitem OWNER TO postgres;

--
-- Name: agendaitemtemplate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.agendaitemtemplate (
    agendaitemtemplateid integer NOT NULL,
    agendatemplateid integer,
    datevalue integer,
    isevent character varying(1),
    eventplanid integer
);


ALTER TABLE program.agendaitemtemplate OWNER TO postgres;

--
-- Name: agendatemplate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.agendatemplate (
    agendatemplateid integer NOT NULL,
    agendaname character varying(30),
    monthvalue integer,
    quota integer,
    yearvalue integer
);


ALTER TABLE program.agendatemplate OWNER TO postgres;

--
-- Name: appraisal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.appraisal (
    annualperiod integer,
    appraisaldate timestamp(6) without time zone,
    appraisalid integer NOT NULL,
    appraisaltemplateid integer,
    appraisalyear character varying(4),
    approvalstatus character varying(1),
    monthperiod integer,
    weekperiod integer,
    appraisalsubject character varying(1),
    subjectkeycount integer,
    customerid integer,
    subjectkey1 integer,
    subjectkey2 integer
);


ALTER TABLE program.appraisal OWNER TO postgres;

--
-- Name: appraisalitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.appraisalitem (
    appraisalid integer,
    boolvalue character varying(1),
    floatvalue double precision,
    integervalue integer,
    itemid integer NOT NULL,
    itemtemplateid integer,
    stringvalue character varying(200)
);


ALTER TABLE program.appraisalitem OWNER TO postgres;

--
-- Name: appraisalitemgroup; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.appraisalitemgroup (
    groupname character varying(20) NOT NULL,
    description character varying(200)
);


ALTER TABLE program.appraisalitemgroup OWNER TO postgres;

--
-- Name: appraisalitemtemplate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.appraisalitemtemplate (
    appraisaltemplateid integer,
    boolvaluestandard character varying(1),
    description character varying(200),
    floatvaluestandard double precision,
    integervaluestandard integer,
    isactive character varying(1),
    islowlevel character varying(1),
    itemname character varying(50),
    itemtemplateid integer NOT NULL,
    level integer,
    parentid integer,
    sequenceno integer,
    valuedatatype character varying(1),
    stringvaluestandard character varying(200)
);


ALTER TABLE program.appraisalitemtemplate OWNER TO postgres;

--
-- Name: appraisaltemplate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.appraisaltemplate (
    appraisalname character varying(50),
    appraisaltemplateid integer NOT NULL,
    description character varying(200),
    formula character varying(285)
);


ALTER TABLE program.appraisaltemplate OWNER TO postgres;

--
-- Name: aqhpropose; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.aqhpropose (
    aqhproposeid integer NOT NULL,
    mustahiqid integer,
    proposeplafond double precision,
    proposestatus character varying(1),
    proposedate timestamp(6) without time zone,
    paybackperiod integer,
    purposeofuse character varying(100),
    installment double precision,
    accountno character varying(20),
    description character varying(200),
    sidate timestamp(6) without time zone
);


ALTER TABLE program.aqhpropose OWNER TO postgres;

--
-- Name: assetcategory; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.assetcategory (
    assetcategoryid integer NOT NULL,
    parentassetcategoryid integer,
    assetcategorycode character varying(20),
    assetcategoryname character varying(50),
    defaultlifetime integer,
    thresholdvalue double precision,
    inputer character varying(50),
    inputdate timestamp(6) without time zone,
    inputtime double precision,
    glicontainerid integer,
    isdepreciable character varying(1),
    assettype character varying(1)
);


ALTER TABLE program.assetcategory OWNER TO postgres;

--
-- Name: balancepartition; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.balancepartition (
    balancepartitionid character varying(30) NOT NULL,
    balance double precision,
    balancepartitiontype character varying(1),
    accountno character varying(30),
    partitionclassifier character varying(1)
);


ALTER TABLE program.balancepartition OWNER TO postgres;

--
-- Name: bank; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.bank (
    bankcode character varying(10) NOT NULL,
    bankshortname character varying(20),
    bankname character varying(60)
);


ALTER TABLE program.bank OWNER TO postgres;

--
-- Name: bankaccountlist; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.bankaccountlist (
    bankaccountid integer NOT NULL,
    bankaccountno character varying(20),
    bankaccountname character varying(200),
    isdefault character varying(1),
    bankaccountlisttype character varying(1),
    bankcode character varying(10)
);


ALTER TABLE program.bankaccountlist OWNER TO postgres;

--
-- Name: blobregistration; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.blobregistration (
    id integer NOT NULL,
    actualfilename character varying(128),
    istemporary character varying(1)
);


ALTER TABLE program.blobregistration OWNER TO postgres;

--
-- Name: branch; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.branch (
    branchcode character varying(3) NOT NULL,
    branchname character varying(30),
    branchtype character varying(2),
    shortcode character varying(5),
    isactive character varying(1)
);


ALTER TABLE program.branch OWNER TO postgres;

--
-- Name: branchbankpic; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.branchbankpic (
    branchcode character varying(5) NOT NULL,
    branchname character varying(50),
    picname character varying(250),
    activedate timestamp(6) without time zone,
    mobilenumber character varying(60),
    faxnumber character varying(50),
    email character varying(100),
    userlogin character varying(20),
    phonenumber character varying(50),
    picposition character varying(80)
);


ALTER TABLE program.branchbankpic OWNER TO postgres;

--
-- Name: branchlocation; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.branchlocation (
    branch_code character varying(5) NOT NULL,
    branchname character varying(50),
    branchstatus character varying(1),
    user_id character varying(20),
    last_update timestamp(6) without time zone,
    masterbranch_code character varying(5)
);


ALTER TABLE program.branchlocation OWNER TO postgres;

--
-- Name: cashadvancereturninfo; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.cashadvancereturninfo (
    sourcetransactionid integer NOT NULL,
    branchcode character varying(5),
    returntransactionid integer
);


ALTER TABLE program.cashadvancereturninfo OWNER TO postgres;

--
-- Name: claimitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.claimitem (
    claimitemid integer NOT NULL,
    residualclaim double precision,
    claimtotal double precision,
    claimtransactionurbanid integer,
    banktransactionid integer
);


ALTER TABLE program.claimitem OWNER TO postgres;

--
-- Name: claimtransactiondetailqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.claimtransactiondetailqurban (
    claimtransactiondetailqurbanid integer CONSTRAINT claimtransactiondetailqurba_claimtransactiondetailqurb_not_null NOT NULL,
    claimtransactionqurbanid integer,
    nominalklaim double precision,
    productid integer,
    donorid integer,
    transactionitemid integer
);


ALTER TABLE program.claimtransactiondetailqurban OWNER TO postgres;

--
-- Name: claimtransactionqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.claimtransactionqurban (
    claimtransactionqurbanid integer NOT NULL,
    claimtotal double precision
);


ALTER TABLE program.claimtransactionqurban OWNER TO postgres;

--
-- Name: companion; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.companion (
    customerid integer NOT NULL,
    companionid integer NOT NULL,
    parentid integer,
    companionextnumber character varying(60)
);


ALTER TABLE program.companion OWNER TO postgres;

--
-- Name: companioncontract; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.companioncontract (
    contractno character varying(20) NOT NULL,
    companionid integer,
    initialcontractperiod timestamp(6) without time zone,
    endcontractperiod timestamp(6) without time zone,
    description character varying(200),
    documentfile character varying(50),
    inputuser character varying(20),
    inputdate timestamp(6) without time zone,
    inputterminal character varying(15),
    productid integer,
    bmisupervisi character varying(10),
    kabkota character varying(50),
    idpropinsi integer,
    companionexperience character varying(200)
);


ALTER TABLE program.companioncontract OWNER TO postgres;

--
-- Name: companionliabilityaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.companionliabilityaccount (
    accountno character varying(30) NOT NULL,
    companionid integer,
    productid integer
);


ALTER TABLE program.companionliabilityaccount OWNER TO postgres;

--
-- Name: companionpersonalkum3; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.companionpersonalkum3 (
    customerid integer NOT NULL,
    workinghour integer,
    workplace character varying(50),
    workposition character varying(50)
);


ALTER TABLE program.companionpersonalkum3 OWNER TO postgres;

--
-- Name: companionproduct; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.companionproduct (
    productid integer NOT NULL,
    companionid integer NOT NULL,
    contractno character varying(20)
);


ALTER TABLE program.companionproduct OWNER TO postgres;

--
-- Name: companionvisit; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.companionvisit (
    companionvisitid integer NOT NULL,
    visitingdate timestamp(6) without time zone,
    visitingyear character varying(4),
    weekperiod integer,
    monthperiod integer,
    annotation character varying(500),
    approvalstatus character varying(1),
    mustahiqid integer,
    companionid integer
);


ALTER TABLE program.companionvisit OWNER TO postgres;

--
-- Name: companionvisititem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.companionvisititem (
    itemid integer NOT NULL,
    itemtemplateid integer,
    companionvisitid integer,
    integervalue integer,
    floatvalue double precision,
    stringvalue character varying(200),
    boolvalue character varying(1)
);


ALTER TABLE program.companionvisititem OWNER TO postgres;

--
-- Name: companionvisititemtemplate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.companionvisititemtemplate (
    itemtemplateid integer NOT NULL,
    sequenceno integer,
    itemname character varying(50),
    description character varying(200),
    visitgroup character varying(2),
    isactive character varying(1),
    productgroupname character varying(50),
    valuedatatype character varying(1),
    answerchoice character varying(500),
    parentitem integer,
    level integer,
    islowlevel character varying(1)
);


ALTER TABLE program.companionvisititemtemplate OWNER TO postgres;

--
-- Name: corporatedonor; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.corporatedonor (
    corporation character varying(1),
    siupp character varying(20),
    tdp character varying(20),
    locationtype character varying(30),
    ownertype character varying(30),
    establisheddate timestamp(6) without time zone,
    establishedplace character varying(50),
    contactperson character varying(50),
    patronagecompany character varying(1),
    cpname character varying(150),
    cpemail character varying(200),
    cpphonenumber character varying(30),
    cpmobilenumber character varying(30),
    donorid integer NOT NULL
);


ALTER TABLE program.corporatedonor OWNER TO postgres;

--
-- Name: costitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.costitem (
    costitemid integer NOT NULL,
    costitemcode character varying(3),
    costitemdescription character varying(200)
);


ALTER TABLE program.costitem OWNER TO postgres;

--
-- Name: currency; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.currency (
    currency_code character varying(20) NOT NULL,
    short_name character varying(10),
    full_name character varying(50),
    kurs_tengah_bi double precision
);


ALTER TABLE program.currency OWNER TO postgres;

--
-- Name: custom_idgen; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.custom_idgen (
    idname character varying(30) NOT NULL,
    idcode character varying(50) NOT NULL,
    last_id integer,
    locked character varying(1)
);


ALTER TABLE program.custom_idgen OWNER TO postgres;

--
-- Name: customer; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.customer (
    customerid integer NOT NULL,
    customername character varying(50),
    addresscity character varying(50),
    addresskecamatan character varying(50),
    addresskelurahan character varying(50),
    addresspostalcode character varying(10),
    addressstate character varying(50),
    addressstreet character varying(200),
    addresssubdistrict character varying(50),
    branchcode character varying(5),
    customerno character varying(30),
    customerstatus character varying(1),
    phonenumber character varying(60),
    idpropinsi integer,
    idnegara integer,
    customertype character varying(2),
    fax character varying(60),
    email character varying(60)
);


ALTER TABLE program.customer OWNER TO postgres;

--
-- Name: customercorporate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.customercorporate (
    customerid integer NOT NULL,
    cpname character varying(150),
    cpphonenumber character varying(60),
    cpmobilenumber character varying(60),
    corporationnumber character varying(60),
    corporationdate timestamp(6) without time zone,
    cctype character varying(1)
);


ALTER TABLE program.customercorporate OWNER TO postgres;

--
-- Name: customerorphan; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.customerorphan (
    academicachievements character varying(200),
    arthobby character varying(200),
    bloodtype character varying(2),
    currentdisease character varying(200),
    customerid integer NOT NULL,
    dreamof integer,
    fathereducation integer,
    fatherincome integer,
    fathername character varying(200),
    fatheroccupation integer,
    guardianaddress character varying(200),
    guardiancity character varying(100),
    guardiandistrict character varying(100),
    guardianeducation integer,
    guardianname character varying(200),
    guardianoccupation integer,
    guardianrelationship integer,
    guardiansubdistrict character varying(100),
    guardianvillage character varying(100),
    height double precision,
    weight double precision,
    medicalreport character varying(200),
    motheraddress character varying(200),
    mothereducation integer,
    motherincome integer,
    mothername character varying(200),
    motheroccupation integer,
    orphanagestatus character varying(1),
    orphansubtype character varying(1),
    physicaldescription character varying(200),
    psychologicalreport character varying(200),
    schoolname character varying(200),
    schooltype character varying(1),
    scores double precision,
    skills character varying(200),
    sporthobby character varying(200)
);


ALTER TABLE program.customerorphan OWNER TO postgres;

--
-- Name: customerpersonal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.customerpersonal (
    customerid integer NOT NULL,
    birthdate timestamp(6) without time zone,
    birthplace character varying(50),
    identitytype character varying(1),
    identitynumber character varying(30),
    formaleducation character varying(1),
    gender character varying(1),
    marital character varying(1),
    religion integer,
    totalfamily integer,
    worksector character varying(1),
    customerpersonaltype character varying(1),
    workid integer
);


ALTER TABLE program.customerpersonal OWNER TO postgres;

--
-- Name: daerahdistribusi; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.daerahdistribusi (
    picdistribusiid integer,
    alamat character varying(100),
    kontakperson character varying(100),
    namalokasi character varying(100) NOT NULL,
    telepon character varying(100),
    isrequestbaru character varying(1),
    regionid integer
);


ALTER TABLE program.daerahdistribusi OWNER TO postgres;

--
-- Name: transactionitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.transactionitem (
    transactionitemid integer NOT NULL,
    branchcode character varying(5),
    currencycode character varying(20),
    mutationtype character varying(1),
    amount double precision,
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(60),
    accountcode character varying(20),
    parameterjournalid character varying(5),
    transactionid integer,
    paidto character varying(50),
    isinternalpaidto character varying(1)
);


ALTER TABLE program.transactionitem OWNER TO postgres;

--
-- Name: dcamountpartition; Type: VIEW; Schema: program; Owner: postgres
--

CREATE VIEW program.dcamountpartition AS
 SELECT i.transactionitemid,
    d.ekuivalenamount AS debet,
    k.ekuivalenamount AS kredit
   FROM ((( SELECT transactionitem.transactionid,
            transactionitem.transactionitemid,
            transactionitem.ekuivalenamount
           FROM program.transactionitem
          WHERE ((transactionitem.mutationtype)::text = 'D'::text)) d
     FULL JOIN ( SELECT transactionitem.transactionid,
            transactionitem.transactionitemid,
            transactionitem.ekuivalenamount
           FROM program.transactionitem
          WHERE ((transactionitem.mutationtype)::text = 'C'::text)) k ON ((d.transactionitemid = k.transactionitemid)))
     JOIN program.transactionitem i ON (((i.transactionitemid = d.transactionitemid) OR (i.transactionitemid = k.transactionitemid))));


ALTER VIEW program.dcamountpartition OWNER TO postgres;

--
-- Name: detailklaimtransaksiproject; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.detailklaimtransaksiproject (
    detailklaimid integer NOT NULL,
    idtransaksiklaim integer,
    nominalbantuan double precision
);


ALTER TABLE program.detailklaimtransaksiproject OWNER TO postgres;

--
-- Name: disease; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.disease (
    diseasecode character varying(5) NOT NULL,
    diseasename character varying(50)
);


ALTER TABLE program.disease OWNER TO postgres;

--
-- Name: diseasediagnosed; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.diseasediagnosed (
    diseasediagnosedid integer NOT NULL,
    appraisalid integer,
    diseasecode character varying(5),
    ishandled character varying(1)
);


ALTER TABLE program.diseasediagnosed OWNER TO postgres;

--
-- Name: donor; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.donor (
    donorid integer NOT NULL,
    donorname character varying(50),
    addressstreet character varying(200),
    addresskelurahan character varying(50),
    addresssubdistrict character varying(50),
    addresscity character varying(50),
    addresspostalcode character varying(10),
    phonenumber character varying(20),
    fax character varying(20),
    referenceby character varying(30),
    status character varying(1),
    donortype character varying(1),
    addressstate character varying(50),
    npwp character varying(50),
    donorno character varying(20),
    npwz character varying(30),
    joindate timestamp(6) without time zone,
    branchcode character varying(5),
    addresskecamatan character varying(50),
    economicsector character varying(1),
    idpropinsi integer,
    idnegara integer,
    donoremail character varying(100)
);


ALTER TABLE program.donor OWNER TO postgres;

--
-- Name: donorbankaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.donorbankaccount (
    bankaccountid integer NOT NULL,
    donorid integer
);


ALTER TABLE program.donorbankaccount OWNER TO postgres;

--
-- Name: donorliabilityaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.donorliabilityaccount (
    donorid integer,
    customerid integer,
    accountno character varying(30) NOT NULL
);


ALTER TABLE program.donorliabilityaccount OWNER TO postgres;

--
-- Name: donormember; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.donormember (
    donorid integer NOT NULL,
    customerid integer NOT NULL
);


ALTER TABLE program.donormember OWNER TO postgres;

--
-- Name: donorpersonal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.donorpersonal (
    donorid integer NOT NULL
);


ALTER TABLE program.donorpersonal OWNER TO postgres;

--
-- Name: donorproduct; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.donorproduct (
    donorid integer NOT NULL,
    productid integer NOT NULL,
    programtype character varying(1)
);


ALTER TABLE program.donorproduct OWNER TO postgres;

--
-- Name: employee; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.employee (
    employeeid character varying(20) NOT NULL,
    employeename character varying(50),
    homeaddress character varying(200),
    identitytype character varying(1),
    identityid character varying(30),
    birthdate timestamp(6) without time zone,
    birthplace character varying(30),
    phonenumber character varying(30)
);


ALTER TABLE program.employee OWNER TO postgres;

--
-- Name: enum_int; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.enum_int (
    enum_name character varying(32) NOT NULL,
    enum_value integer NOT NULL,
    enum_description character varying(50)
);


ALTER TABLE program.enum_int OWNER TO postgres;

--
-- Name: enum_varchar; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.enum_varchar (
    enum_name character varying(32) NOT NULL,
    enum_value character varying(2) NOT NULL,
    enum_description character varying(50)
);


ALTER TABLE program.enum_varchar OWNER TO postgres;

--
-- Name: event; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.event (
    eventid integer NOT NULL,
    eventdate timestamp(6) without time zone,
    eventplanid integer,
    financingamount double precision,
    reportfile character varying(200),
    totalaudience integer,
    eventtype character varying(1)
);


ALTER TABLE program.event OWNER TO postgres;

--
-- Name: eventattendance; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.eventattendance (
    eventattendanceid integer NOT NULL,
    eventid integer,
    eventplanattendanceid integer,
    description character varying(200)
);


ALTER TABLE program.eventattendance OWNER TO postgres;

--
-- Name: eventksm; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.eventksm (
    eventid integer NOT NULL,
    eventdatefrom timestamp(6) without time zone,
    eventdateto timestamp(6) without time zone
);


ALTER TABLE program.eventksm OWNER TO postgres;

--
-- Name: eventplan; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.eventplan (
    eventplanid integer NOT NULL,
    agendaitemid integer,
    eventplandescription character varying(500),
    eventplanlocation character varying(200),
    eventplanname character varying(200),
    targetaudience integer,
    eventplanbudget double precision,
    eventplandate timestamp(6) without time zone,
    productid integer,
    isreported character varying(1),
    eventplantype character varying(1)
);


ALTER TABLE program.eventplan OWNER TO postgres;

--
-- Name: eventplanattendance; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.eventplanattendance (
    eventplanattendanceid integer NOT NULL,
    eventplanid integer,
    mustahiqid integer
);


ALTER TABLE program.eventplanattendance OWNER TO postgres;

--
-- Name: eventplanksm; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.eventplanksm (
    eventplanid integer NOT NULL,
    datefrom timestamp(6) without time zone,
    dateto timestamp(6) without time zone,
    personel character varying(100),
    successindicator character varying(200),
    target character varying(200),
    eventtype character varying(1),
    isattendancecompleted character varying(1)
);


ALTER TABLE program.eventplanksm OWNER TO postgres;

--
-- Name: externaldebtor; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.externaldebtor (
    debtorid integer NOT NULL,
    debtorcode character varying(5),
    branchcode character varying(3),
    debtorname character varying(100),
    debtorphone character varying(30),
    debtoraddress character varying(200),
    description character varying(200)
);


ALTER TABLE program.externaldebtor OWNER TO postgres;

--
-- Name: financialaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.financialaccount (
    accountno character varying(30) NOT NULL,
    accountname character varying(50),
    balance double precision,
    branchcode character varying(5),
    currencycode character varying(20),
    financialaccounttype character varying(1),
    status character varying(1),
    openingdate timestamp(6) without time zone,
    accountcode character varying(20),
    lastdaybalance double precision,
    lastdailybalanceid integer
);


ALTER TABLE program.financialaccount OWNER TO postgres;

--
-- Name: financingaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.financingaccount (
    periodcount integer,
    periodunit character varying(1),
    baseamount double precision,
    marginamount double precision,
    basebalance double precision,
    marginbalance double precision,
    collectibiltiylevel integer,
    installmentamount double precision,
    installmentbalance double precision,
    productid integer,
    mustahiqid integer,
    accountno character varying(30) NOT NULL,
    debtarrears real,
    cycleperiodcount integer,
    realperiodcount integer,
    graceperiodcount integer,
    mustahiqproductid integer
);


ALTER TABLE program.financingaccount OWNER TO postgres;

--
-- Name: financingtransactionitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.financingtransactionitem (
    transactionitemid integer NOT NULL,
    accountno character varying(30)
);


ALTER TABLE program.financingtransactionitem OWNER TO postgres;

--
-- Name: glinterface; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.glinterface (
    interfaceid integer NOT NULL,
    interfacecode character varying(20),
    description character varying(100),
    accountcode character varying(20),
    accountname character varying(100),
    productid integer
);


ALTER TABLE program.glinterface OWNER TO postgres;

--
-- Name: glinterfacecontainer; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.glinterfacecontainer (
    glicontainerid integer NOT NULL,
    glicontainercode character varying(30),
    glicontainername character varying(50)
);


ALTER TABLE program.glinterfacecontainer OWNER TO postgres;

--
-- Name: glinterfacemember; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.glinterfacemember (
    glimemberid integer NOT NULL,
    accountcode character varying(20),
    accountname character varying(100),
    glimembercode character varying(20),
    description character varying(100),
    glicontainerid integer
);


ALTER TABLE program.glinterfacemember OWNER TO postgres;

--
-- Name: healthliabilitytransactionitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.healthliabilitytransactionitem (
    transactionitemid integer NOT NULL,
    jenissakit character varying(50),
    jenisperawatan character varying(50),
    perkembangan character varying(1),
    keterangan character varying(100),
    kategori character varying(1)
);


ALTER TABLE program.healthliabilitytransactionitem OWNER TO postgres;

--
-- Name: historyofchanges; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.historyofchanges (
    historyid integer NOT NULL,
    changetype character varying(1),
    domainofchange character varying(30),
    processtime timestamp(6) without time zone,
    userid character varying(30),
    datasourcetype character varying(1),
    datasourceref character varying(100),
    datasourceclass character varying(50),
    datasourcerefinteger integer,
    terminalid character varying(20)
);


ALTER TABLE program.historyofchanges OWNER TO postgres;

--
-- Name: id_gen; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.id_gen (
    id_code character varying(50) NOT NULL,
    last_id integer,
    locked character varying(1)
);


ALTER TABLE program.id_gen OWNER TO postgres;

--
-- Name: inbox; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.inbox (
    inboxid integer NOT NULL,
    description character varying(100),
    branchcode character varying(5),
    userid character varying(30),
    filename character varying(200),
    kodeinbox character varying(10),
    inputdate timestamp(6) without time zone,
    inputtime timestamp(6) without time zone,
    inboxtype character varying(1),
    lastinboxhistoryid integer
);


ALTER TABLE program.inbox OWNER TO postgres;

--
-- Name: inboxhistory; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.inboxhistory (
    inboxhistoryid integer NOT NULL,
    inboxid integer,
    filename character varying(200),
    inputdate timestamp(6) without time zone,
    inputtime timestamp(6) without time zone,
    userid character varying(30),
    nextinboxhistoryid integer
);


ALTER TABLE program.inboxhistory OWNER TO postgres;

--
-- Name: inboxtransaction; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.inboxtransaction (
    transactionid integer,
    inboxid integer NOT NULL
);


ALTER TABLE program.inboxtransaction OWNER TO postgres;

--
-- Name: individualdonor; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.individualdonor (
    gender character varying(1),
    birthplace character varying(30),
    birthdate timestamp(6) without time zone,
    identitytype character varying(1),
    religion integer,
    identitynumber character varying(20),
    maritalstate character varying(1),
    language character varying(1),
    lastformaleducation integer,
    incomepermonth double precision,
    expensepermonth double precision,
    officeaddress character varying(200),
    officekelurahan character varying(50),
    officesubdistrict character varying(50),
    officecity character varying(50),
    officestate character varying(50),
    officepostalcode character varying(10),
    officephonenumber character varying(50),
    email character varying(200),
    mobilephone character varying(20),
    donorid integer NOT NULL,
    idpropinsioffice integer,
    officekecamatan character varying(50),
    jobposition character varying(40),
    corporatename character varying(100),
    couplename character varying(40),
    child integer,
    fworkid integer
);


ALTER TABLE program.individualdonor OWNER TO postgres;

--
-- Name: itemuploadedstatement; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.itemuploadedstatement (
    uploadedstatementid integer,
    itemstatementid integer NOT NULL,
    itemrekening character varying(20),
    itemdescription character varying(100),
    itemtype character varying(1),
    itemdate timestamp(6) without time zone,
    productid integer,
    mustahiqid integer,
    reconcilestatus character varying(1),
    itemamount double precision,
    reconcileprocessid integer,
    reconcileuser character varying(20),
    mustahiqproductid integer
);


ALTER TABLE program.itemuploadedstatement OWNER TO postgres;

--
-- Name: kjks; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.kjks (
    customerid integer NOT NULL,
    skmenteri character varying(60),
    chairmanname character varying(50),
    chairmanphonenumber character varying(60),
    secretaryname character varying(50),
    secretaryphonenumber character varying(60),
    treasurername character varying(50),
    treasurerphonenumber character varying(60),
    photo1 character varying(60),
    photo2 character varying(60),
    photo3 character varying(60),
    kjkstype character varying(1),
    spmaccount character varying(20),
    spmdate timestamp(6) without time zone,
    spmnumber character varying(50),
    sp2daccount character varying(20),
    sp2ddate timestamp(6) without time zone,
    sp2dnumber character varying(50)
);


ALTER TABLE program.kjks OWNER TO postgres;

--
-- Name: klaimtransaksiproject; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.klaimtransaksiproject (
    idtransaksiklaim integer NOT NULL,
    idtransaksireferensi integer,
    nomorreferensi character varying(30),
    totalnominal double precision,
    sisaklaim double precision,
    tanggalbantuan timestamp(6) without time zone,
    tanggalklaim timestamp(6) without time zone,
    keterangan character varying(100),
    sumberdana integer,
    productid integer
);


ALTER TABLE program.klaimtransaksiproject OWNER TO postgres;

--
-- Name: konversiperolehanqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.konversiperolehanqurban (
    konversiperolehanqurbanid integer NOT NULL,
    rencanadistribusiid integer,
    jumlahhewankonversi integer,
    productid integer,
    nominalkonversi double precision,
    jenishewan character varying(20)
);


ALTER TABLE program.konversiperolehanqurban OWNER TO postgres;

--
-- Name: liabilityaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.liabilityaccount (
    liabilityaccounttype character varying(1),
    accountno character varying(30) NOT NULL
);


ALTER TABLE program.liabilityaccount OWNER TO postgres;

--
-- Name: liabilitytransactionitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.liabilitytransactionitem (
    transactionitemid integer NOT NULL,
    accountno character varying(30),
    liabilitytransactiontype character varying(1)
);


ALTER TABLE program.liabilitytransactionitem OWNER TO postgres;

--
-- Name: linkedprograms; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.linkedprograms (
    linkedprogramid integer NOT NULL,
    linkedproductid integer,
    productid integer
);


ALTER TABLE program.linkedprograms OWNER TO postgres;

--
-- Name: mapreconcile; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mapreconcile (
    mapid integer NOT NULL,
    mapdescription character varying(200),
    mapproductid integer,
    mapfundentity integer
);


ALTER TABLE program.mapreconcile OWNER TO postgres;

--
-- Name: marginitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.marginitem (
    itemstatementid integer NOT NULL,
    cpp double precision,
    bmi double precision,
    bmm double precision,
    microfin double precision,
    development double precision,
    profitsharing double precision
);


ALTER TABLE program.marginitem OWNER TO postgres;

--
-- Name: marketingqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.marketingqurban (
    customerid integer NOT NULL,
    marketingqurbanid integer NOT NULL,
    bankaccountno character varying(20),
    mqtype character varying(2),
    bankaccountname character varying(50),
    branchcode character varying(3)
);


ALTER TABLE program.marketingqurban OWNER TO postgres;

--
-- Name: masjidkum3; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.masjidkum3 (
    afiliasiorganisasi character varying(200),
    alamat character varying(200),
    bendahara character varying(50),
    contactperson character varying(50),
    cpphone character varying(20),
    foto1 character varying(100),
    foto2 character varying(100),
    idpropinsi integer,
    jumlahukm integer,
    kecamatan character varying(50),
    kegiatanmasjid character varying(200),
    kelurahan character varying(50),
    ketua character varying(50),
    komunitasusahajamaah character varying(100),
    kota character varying(50),
    mustahiqgroupid integer NOT NULL,
    phonenumber character varying(20),
    radiusukm double precision,
    sekertaris character varying(50),
    companionid integer,
    iseligible character varying(1),
    noteligiblereason character varying(100)
);


ALTER TABLE program.masjidkum3 OWNER TO postgres;

--
-- Name: masterjenisdonasiqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.masterjenisdonasiqurban (
    paketqurbanid integer NOT NULL,
    kodepaket character varying(2),
    keteranganwilayah character varying(50),
    nominaldonasi double precision,
    feemarketer double precision,
    jenishewan character varying(30)
);


ALTER TABLE program.masterjenisdonasiqurban OWNER TO postgres;

--
-- Name: mnrtransaction; Type: VIEW; Schema: program; Owner: postgres
--

CREATE VIEW program.mnrtransaction AS
 SELECT t.transactionid,
    t.transactionno,
    t.transactiondate,
    t.amount,
    a.fundentity,
    f.accountno,
    f.accountname
   FROM ((((transaction.transaction t
     JOIN ( SELECT ti.transactionid,
            ti.transactionitemid,
            ti.mutationtype
           FROM transaction.transactionitem ti
          WHERE ((ti.mutationtype)::text = 'D'::text)) i ON ((i.transactionid = t.transactionid)))
     JOIN ( SELECT ati.transactionitemid,
            ati.accounttitype,
            ati.fundentity,
            ati.accountno
           FROM transaction.accounttransactionitem ati
          WHERE ((ati.accounttitype)::text = 'Z'::text)) a ON ((a.transactionitemid = i.transactionitemid)))
     JOIN ( SELECT fa.accountno,
            fa.accountname
           FROM transaction.financialaccount fa) f ON (((f.accountno)::text = (a.accountno)::text)))
     LEFT JOIN ( SELECT klaimtransaksiproject.idtransaksiklaim,
            klaimtransaksiproject.idtransaksireferensi,
            klaimtransaksiproject.nomorreferensi,
            klaimtransaksiproject.totalnominal,
            klaimtransaksiproject.sisaklaim,
            klaimtransaksiproject.tanggalbantuan,
            klaimtransaksiproject.tanggalklaim,
            klaimtransaksiproject.keterangan,
            klaimtransaksiproject.sumberdana
           FROM program.klaimtransaksiproject) k ON ((t.transactionid = k.idtransaksireferensi)))
  WHERE (k.idtransaksiklaim IS NULL);


ALTER VIEW program.mnrtransaction OWNER TO postgres;

--
-- Name: mpz; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mpz (
    assets double precision,
    candidatecount integer,
    customerid integer NOT NULL,
    membercount integer,
    unitsector character varying(1),
    zisfundpreviousmonth double precision,
    zisfundthismonth double precision,
    zisgrowthperyear double precision
);


ALTER TABLE program.mpz OWNER TO postgres;

--
-- Name: mpzzisallocation; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mpzzisallocation (
    customerid integer,
    fundamount double precision,
    fundingperiodename character varying(20),
    sectorname character varying(50),
    zisallocationid integer NOT NULL
);


ALTER TABLE program.mpzzisallocation OWNER TO postgres;

--
-- Name: mustahiq; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiq (
    mustahiqreferenceby character varying(150),
    mustahiqtype character varying(2),
    mustahiqid integer NOT NULL,
    mustahiqgroupid integer,
    customerid integer,
    companionid integer,
    ashnaf character varying(1)
);


ALTER TABLE program.mustahiq OWNER TO postgres;

--
-- Name: mustahiqadditionalinfo; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqadditionalinfo (
    mustahiqinfoid integer NOT NULL,
    mustahiqproductid integer,
    mustahiqid integer,
    mustahiqinfotype character varying(1),
    mustahiqidsupervisor integer,
    schoolname character varying(200),
    sd_kelas character varying(10),
    sd_tahunawal timestamp without time zone,
    sd_tahunakhir timestamp without time zone,
    smp_kelas character varying(10),
    smp_tahunawal timestamp without time zone,
    smp_tahunakhir timestamp without time zone,
    sma_kelas character varying(10),
    sma_tahunawal timestamp without time zone,
    sma_tahunakhir timestamp without time zone,
    achievement character varying(500),
    universitas_kelas character varying(10),
    universitas_tahunawal timestamp without time zone,
    universitas_tahunakhir timestamp without time zone
);


ALTER TABLE program.mustahiqadditionalinfo OWNER TO postgres;

--
-- Name: mustahiqappraisal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqappraisal (
    appraisalid integer NOT NULL,
    mustahiqid integer,
    mustahiqproductid integer
);


ALTER TABLE program.mustahiqappraisal OWNER TO postgres;

--
-- Name: mustahiqaqh; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqaqh (
    mustahiqid integer NOT NULL,
    branchcode character varying(5),
    depositbalance double precision,
    couplename character varying(100),
    couplejob character varying(100),
    employeestatus character varying(1),
    "position" character varying(100)
);


ALTER TABLE program.mustahiqaqh OWNER TO postgres;

--
-- Name: mustahiqbankaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqbankaccount (
    bankaccountid integer NOT NULL,
    mustahiqid integer,
    accountusagetype character varying(2),
    productid integer,
    statusaccount character varying(1),
    activedate timestamp(6) without time zone,
    nonactivedate timestamp(6) without time zone,
    description character varying(100),
    bankstatus character varying(1),
    mustahiqproductid integer
);


ALTER TABLE program.mustahiqbankaccount OWNER TO postgres;

--
-- Name: mustahiqcandidate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqcandidate (
    boys integer,
    customerid integer NOT NULL,
    dependents integer,
    firstchildedu integer,
    girls integer,
    monthlyincome double precision,
    secondchildedu integer,
    thirdchildedu integer,
    candidatestatus character varying(1),
    ethnicgroup character varying(20),
    housingstatus character varying(20),
    spousename character varying(50),
    productid integer,
    verificator character varying(50)
);


ALTER TABLE program.mustahiqcandidate OWNER TO postgres;

--
-- Name: mustahiqcorporate; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqcorporate (
    cpname character varying(150),
    cpphonenumber character varying(30),
    cpmobilenumber character varying(30),
    mustahiqid integer NOT NULL
);


ALTER TABLE program.mustahiqcorporate OWNER TO postgres;

--
-- Name: mustahiqgroup; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqgroup (
    mustahiqgroupid integer NOT NULL,
    groupname character varying(30),
    description character varying(200),
    productid integer,
    parentid integer,
    islowlevel character varying(1),
    detailid integer,
    grouptype character varying(1),
    membercount integer
);


ALTER TABLE program.mustahiqgroup OWNER TO postgres;

--
-- Name: mustahiqgroupdetail; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqgroupdetail (
    description character varying(200),
    detailid integer NOT NULL,
    detailname character varying(50),
    membercount integer,
    mustahiqgroupid integer
);


ALTER TABLE program.mustahiqgroupdetail OWNER TO postgres;

--
-- Name: mustahiqkum3; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqkum3 (
    mustahiqid integer NOT NULL,
    photo1 character varying(200),
    photo2 character varying(200),
    photo3 character varying(200),
    personalid integer
);


ALTER TABLE program.mustahiqkum3 OWNER TO postgres;

--
-- Name: mustahiqliabilityaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqliabilityaccount (
    productid integer,
    mustahiqid integer,
    accountno character varying(30) NOT NULL,
    mlatype character varying(1),
    mustahiqproductid integer
);


ALTER TABLE program.mustahiqliabilityaccount OWNER TO postgres;

--
-- Name: mustahiqpersonal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqpersonal (
    mustahiqgender character varying(1),
    mustahiqbirthplace character varying(150),
    mustahiqbirthdate timestamp(6) without time zone,
    mustahiqidentitynumber character varying(30),
    mustahiqreligion integer,
    mustahiqtotalfamily integer,
    mustahiqformaleducation integer,
    mustahiqmarital character varying(1),
    mustahiqworksector character varying(1),
    mustahiqashnaf character varying(1),
    mustahiqidentitytype character varying(1),
    mustahiqid integer NOT NULL,
    programtype character varying(2),
    mustahiqpersonaltype character varying(2),
    mustahiqtargetcapital double precision,
    workid integer,
    mustahiqincome integer
);


ALTER TABLE program.mustahiqpersonal OWNER TO postgres;

--
-- Name: mustahiqproduct; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqproduct (
    productid integer NOT NULL,
    mustahiqid integer NOT NULL,
    mustahiqextnumber character varying(30),
    iseligible character varying(1),
    noteligiblereason character varying(2),
    mustahiqextfield character varying(50),
    noteligibledate timestamp(6) without time zone,
    companionid integer,
    status character varying(1),
    noteligiblelegal character varying(100),
    lastfundingperiod integer,
    pendingfund double precision,
    mustahiqproducttype character varying(1),
    mustahiqproductid integer NOT NULL,
    startdate timestamp without time zone,
    mustahiqproductname character varying(200),
    dateend timestamp without time zone,
    distributionamount numeric(30,2),
    datestart timestamp without time zone,
    proposalid integer,
    mustahiqproductgroupid integer,
    accountno character varying(30),
    branchcode character varying(10),
    ashnaf character varying(1),
    fundproductid integer,
    totalrecipient integer
);


ALTER TABLE program.mustahiqproduct OWNER TO postgres;

--
-- Name: mustahiqproductgroup; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqproductgroup (
    mustahiqproductgroupid integer NOT NULL,
    productid integer,
    mustahiqproductgrouptype character varying(1),
    mustahiqproductgroupname character varying(100)
);


ALTER TABLE program.mustahiqproductgroup OWNER TO postgres;

--
-- Name: mustahiqproject; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqproject (
    mustahiqid integer NOT NULL,
    productid integer NOT NULL,
    detailklaimid integer,
    mustahiqproductid integer NOT NULL
);


ALTER TABLE program.mustahiqproject OWNER TO postgres;

--
-- Name: mustahiqqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.mustahiqqurban (
    mustahiqid integer NOT NULL,
    mustahiqage integer,
    namalokasi character varying(30),
    description character varying(100)
);


ALTER TABLE program.mustahiqqurban OWNER TO postgres;

--
-- Name: negara; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.negara (
    idnegara integer NOT NULL,
    nama_negara character varying(20)
);


ALTER TABLE program.negara OWNER TO postgres;

--
-- Name: orphanbalancepartition; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.orphanbalancepartition (
    balancepartitionid character varying(30) NOT NULL,
    accountno character varying(30)
);


ALTER TABLE program.orphanbalancepartition OWNER TO postgres;

--
-- Name: orphanbeasiswa; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.orphanbeasiswa (
    age integer,
    aschildnumber integer,
    customerid integer NOT NULL,
    dependent integer,
    fatheraddress character varying(200),
    fatherbirthdate timestamp(6) without time zone,
    fatherbirthplace character varying(100),
    fatherdeathdate timestamp(6) without time zone,
    foundationname character varying(200),
    guardianincome integer,
    guarantor character varying(1),
    housingstatus character varying(1),
    insurance integer,
    insuranceno character varying(30),
    isfatheralive character varying(1),
    ismotheralive character varying(1),
    lifewith integer,
    monthlyelectricitycost double precision,
    monthlycellularcost double precision,
    monthlylandlinecost double precision,
    monthlywatercost double precision,
    motherbirthdate timestamp(6) without time zone,
    motherbirthplace character varying(100),
    nickname character varying(50),
    onfoundation character varying(1),
    onscholarship character varying(1),
    scholarshipprovider character varying(200),
    schooladdress character varying(200),
    schoolclass character varying(5),
    schoolfees double precision,
    schoolingstatus character varying(1),
    totaldebt integer,
    orphanksm character varying(1)
);


ALTER TABLE program.orphanbeasiswa OWNER TO postgres;

--
-- Name: orphandebtlist; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.orphandebtlist (
    customerid integer,
    debtid integer NOT NULL,
    category character varying(50),
    loanvalues double precision
);


ALTER TABLE program.orphandebtlist OWNER TO postgres;

--
-- Name: orphankafala; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.orphankafala (
    causeoforphanage character varying(50),
    cpmobileno character varying(20),
    customerid integer NOT NULL,
    datekafalaended timestamp(6) without time zone,
    datekafalastarted timestamp(6) without time zone,
    donorid integer,
    extracircularactivities character varying(50),
    fathercauseofdeath character varying(50),
    fathercurrenteconomic character varying(50),
    fathermarital character varying(1),
    guardiancurrenteconomic character varying(50),
    guardianphonenumber character varying(20),
    hobbies character varying(50),
    mentorremarks character varying(100),
    mothercauseofdeath character varying(50),
    mothercurrenteconomic character varying(50),
    mothermarital character varying(1),
    numberofbrothers integer,
    numberofsisters integer,
    olduisid character varying(30),
    piachangesstatus character varying(20),
    registrationdate timestamp(6) without time zone
);


ALTER TABLE program.orphankafala OWNER TO postgres;

--
-- Name: orphankafalaliability; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.orphankafalaliability (
    accountno character varying(30) NOT NULL
);


ALTER TABLE program.orphankafalaliability OWNER TO postgres;

--
-- Name: orphanksm; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.orphanksm (
    customerid integer NOT NULL,
    orphanlevel character varying(1),
    fotopeserta character varying(200),
    fotopenyakit character varying(200)
);


ALTER TABLE program.orphanksm OWNER TO postgres;

--
-- Name: orphansiblings; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.orphansiblings (
    siblingsid integer NOT NULL,
    customerid integer,
    siblingsname character varying(100)
);


ALTER TABLE program.orphansiblings OWNER TO postgres;

--
-- Name: orphantertiarylist; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.orphantertiarylist (
    customerid integer,
    tertiaryid integer NOT NULL,
    tertiaryname character varying(50),
    quantity integer
);


ALTER TABLE program.orphantertiarylist OWNER TO postgres;

--
-- Name: parameterglobal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.parameterglobal (
    kode_parameter character varying(10) NOT NULL,
    tipe_parameter character varying(10),
    nilai_parameter double precision,
    deskripsi character varying(60),
    is_parameter_system character varying(1),
    nilai_parameter_tanggal timestamp(6) without time zone,
    nilai_parameter_string character varying(30),
    tag character varying(15),
    default_code character varying(30)
);


ALTER TABLE program.parameterglobal OWNER TO postgres;

--
-- Name: parameterinbox; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.parameterinbox (
    kodeinbox character varying(10) NOT NULL,
    description character varying(50),
    namaform character varying(100),
    taginbox character varying(20)
);


ALTER TABLE program.parameterinbox OWNER TO postgres;

--
-- Name: parameterjournal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.parameterjournal (
    parameterjournalid integer NOT NULL,
    description character varying(100),
    datasource character varying(30),
    journalcode character varying(5)
);


ALTER TABLE program.parameterjournal OWNER TO postgres;

--
-- Name: parameterjournalitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.parameterjournalitem (
    parameterjournalitemid integer NOT NULL,
    accountcode character varying(20),
    branchbase character varying(1),
    description character varying(50),
    basesign character varying(1),
    currencybase character varying(1),
    amountbase character varying(30),
    ratebase character varying(30),
    accountbase character varying(1),
    parameterjournalid integer
);


ALTER TABLE program.parameterjournalitem OWNER TO postgres;

--
-- Name: partner; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.partner (
    partnertype character varying(2),
    partnerid integer NOT NULL,
    customerid integer,
    partnercpname character varying(200),
    partnercpmobilephone character varying(20),
    partnercpaddress character varying(200),
    partnercpemail character varying(150),
    branchcode character varying(10),
    partnername character varying(100)
);


ALTER TABLE program.partner OWNER TO postgres;

--
-- Name: pequrban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.pequrban (
    donorid integer NOT NULL,
    productid integer NOT NULL,
    referensi character varying(20),
    issudahprosesklaim character varying(1),
    marketingqurbanid integer,
    atasnamarekening character varying(30),
    nomorrekening character varying(20),
    requestdistribusiid integer
);


ALTER TABLE program.pequrban OWNER TO postgres;

--
-- Name: perolehanqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.perolehanqurban (
    productid integer NOT NULL,
    perolehanqurbanid integer NOT NULL,
    jenisdonasi character varying(2),
    ekuivalendana double precision,
    claimtransactiondetailqurbanid integer,
    konversiperolehanqurbanid integer,
    paketqurbanid integer,
    fotosebelum character varying(100),
    fotosetelah character varying(100),
    fotosaat character varying(100)
);


ALTER TABLE program.perolehanqurban OWNER TO postgres;

--
-- Name: picdistribusi; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.picdistribusi (
    picdistribusiid integer NOT NULL,
    bankaccountno character varying(20),
    bankaccountname character varying(50),
    customerid integer
);


ALTER TABLE program.picdistribusi OWNER TO postgres;

--
-- Name: product; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.product (
    productid integer NOT NULL,
    productname character varying(100),
    description character varying(200),
    accountofcollection character varying(20),
    accountofdistribution character varying(20),
    percentageofamilfunds double precision,
    producttype character varying(1),
    status character varying(1),
    closeddate timestamp(6) without time zone,
    fundcategory character varying(1),
    fixedvalue character varying(1),
    fixedvalueamount double precision,
    parentproductid integer,
    isdetail character varying(1),
    level integer,
    productcode character varying(20),
    multipackage character varying(1),
    nishab double precision,
    haul integer,
    rate double precision,
    productgroupname character varying(50),
    isquotafull character varying(1),
    mustahiqquota integer,
    currentquotaposition integer,
    productgroupid integer,
    transactionproductid integer
);


ALTER TABLE program.product OWNER TO postgres;

--
-- Name: productaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.productaccount (
    accountno character varying(30) NOT NULL,
    productid integer,
    realbalance double precision
);


ALTER TABLE program.productaccount OWNER TO postgres;

--
-- Name: productdetail; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.productdetail (
    productdetailid integer NOT NULL,
    productid integer,
    detailname character varying(30),
    description character varying(200),
    companionid integer
);


ALTER TABLE program.productdetail OWNER TO postgres;

--
-- Name: productgroup; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.productgroup (
    productgroupid integer NOT NULL,
    productgroupcode character varying(10),
    productgroupname character varying(50),
    description character varying(200),
    statusaktif character varying(1),
    transactionproductid integer
);


ALTER TABLE program.productgroup OWNER TO postgres;

--
-- Name: producthierarchy; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.producthierarchy (
    hierarchyid integer NOT NULL,
    parentproductid integer,
    childproductid integer,
    level integer
);


ALTER TABLE program.producthierarchy OWNER TO postgres;

--
-- Name: producttarget; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.producttarget (
    beginperiod timestamp(6) without time zone,
    description character varying(50),
    endperiod timestamp(6) without time zone,
    productid integer,
    producttargetid integer NOT NULL
);


ALTER TABLE program.producttarget OWNER TO postgres;

--
-- Name: producttargetcomponent; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.producttargetcomponent (
    componentid integer NOT NULL,
    producttargetid integer,
    targetcomponentname character varying(20),
    targetfinalvalue integer,
    targetunit character varying(20),
    targetvalue integer
);


ALTER TABLE program.producttargetcomponent OWNER TO postgres;

--
-- Name: producttargethistory; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.producttargethistory (
    componentid integer,
    currentvalue integer,
    producttargethistoryid integer NOT NULL,
    updatedate timestamp(6) without time zone
);


ALTER TABLE program.producttargethistory OWNER TO postgres;

--
-- Name: producttransactionitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.producttransactionitem (
    transactionitemid integer NOT NULL,
    accountno character varying(30),
    partitioncode character varying(1)
);


ALTER TABLE program.producttransactionitem OWNER TO postgres;

--
-- Name: program; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.program (
    productid integer NOT NULL,
    programtype character varying(1)
);


ALTER TABLE program.program OWNER TO postgres;

--
-- Name: programaqh; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.programaqh (
    productid integer NOT NULL,
    branchcode character varying(5),
    maxplafond double precision,
    maxdropping double precision
);


ALTER TABLE program.programaqh OWNER TO postgres;

--
-- Name: programksm; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.programksm (
    productid integer NOT NULL,
    programterkaitid integer
);


ALTER TABLE program.programksm OWNER TO postgres;

--
-- Name: programqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.programqurban (
    productid integer NOT NULL,
    yearimplementation character varying(4),
    hijriyahyear character varying(4),
    totaldonation double precision
);


ALTER TABLE program.programqurban OWNER TO postgres;

--
-- Name: project; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.project (
    budgetamount double precision,
    startdate timestamp(6) without time zone,
    finsihdate timestamp(6) without time zone,
    productid integer NOT NULL
);


ALTER TABLE program.project OWNER TO postgres;

--
-- Name: projectaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.projectaccount (
    accountno character varying(30) NOT NULL,
    startdate timestamp(6) without time zone,
    finishdate timestamp(6) without time zone,
    budgetamount double precision
);


ALTER TABLE program.projectaccount OWNER TO postgres;

--
-- Name: propinsi; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.propinsi (
    idpropinsi integer NOT NULL,
    idnegara integer,
    propinsi character varying(60),
    kodepropinsi character varying(3)
);


ALTER TABLE program.propinsi OWNER TO postgres;

--
-- Name: proposal; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.proposal (
    proposalid integer NOT NULL,
    mustahiqid integer,
    proposaldate timestamp without time zone,
    proposaldescription character varying(200),
    proposalno character varying(40),
    proposalnominal double precision,
    proposalreceivedby character varying(200),
    proposalreceiveddate timestamp without time zone,
    proposalreferenceby character varying(200),
    proposalstatus character varying(1),
    mustahiqproductid integer,
    productid integer,
    proposalreferenceposition integer,
    productgroupid integer,
    branchcode character varying(10)
);


ALTER TABLE program.proposal OWNER TO postgres;

--
-- Name: realisasidistribusi; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realisasidistribusi (
    realisasidistribusiid integer NOT NULL,
    rencanadistribusiid integer,
    jumlahhewanqurban integer,
    keterangan character varying(100),
    fotolokasi character varying(100),
    bentukdistribusi character varying(2),
    alasanperubahan character varying(100),
    tanggal timestamp(6) without time zone
);


ALTER TABLE program.realisasidistribusi OWNER TO postgres;

--
-- Name: realisasidistribusihewan; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realisasidistribusihewan (
    realisasidistribusihewanid integer NOT NULL,
    rencanadistribusihewanid integer,
    jumlah integer,
    realisasidistribusiid integer,
    jenishewan character varying(20)
);


ALTER TABLE program.realisasidistribusihewan OWNER TO postgres;

--
-- Name: realization; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realization (
    realizationid integer NOT NULL,
    realizationdate timestamp without time zone,
    realmemoid integer,
    realizationtype character varying(1),
    realizationdescription character varying(200),
    realizationinputdate timestamp(6) without time zone,
    realizationinputuser character varying(100),
    realizationlocation character varying(200),
    memoamount numeric(30,8),
    transactionid integer,
    branchcode character varying(5),
    budgetid integer,
    realizationamount numeric(30,8),
    partnerid integer,
    employeeid character varying(20),
    statusreceivables character varying(1),
    statusreclpj character varying(1)
);


ALTER TABLE program.realization OWNER TO postgres;

--
-- Name: realizationbudget; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationbudget (
    realbudgetid integer NOT NULL,
    realizationid integer,
    budgetid integer,
    productid integer
);


ALTER TABLE program.realizationbudget OWNER TO postgres;

--
-- Name: realizationcost; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationcost (
    realizationcostid integer NOT NULL,
    costitemid integer,
    costamount numeric(30,4),
    additionaldescription character varying(200),
    realizationid integer,
    realizationcosttype character varying(1),
    returnid integer
);


ALTER TABLE program.realizationcost OWNER TO postgres;

--
-- Name: realizationdetail; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationdetail (
    realizationdetailid integer NOT NULL,
    realizationamount double precision,
    realizationid integer,
    mustahiqproductid integer,
    memoamount numeric(30,8),
    realizationdescription character varying(200),
    detaildescription character varying(200),
    cashaacountno character varying(30),
    accountno character varying(30),
    branchcode character varying(5),
    transactionid integer,
    ashnaf character varying(1),
    fundproductid integer
);


ALTER TABLE program.realizationdetail OWNER TO postgres;

--
-- Name: realizationmemo; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationmemo (
    realmemoid integer NOT NULL,
    realmemonumber character varying(100),
    realmemosubject character varying(100),
    realmemoamount double precision,
    realmemofrom character varying(100),
    realmemoto character varying(100),
    realizationmemotype character varying(1),
    userinput character varying(30),
    realmemodate timestamp without time zone,
    inputdate timestamp without time zone,
    branchcode character varying(10),
    dokumenid integer
);


ALTER TABLE program.realizationmemo OWNER TO postgres;

--
-- Name: realizationmemodetail; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationmemodetail (
    realmemodetailid integer NOT NULL,
    realmemodetailamount double precision,
    realmemoid integer,
    mustahiqproductid integer,
    productid integer
);


ALTER TABLE program.realizationmemodetail OWNER TO postgres;

--
-- Name: realizationpartner; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationpartner (
    realizationpartnerid integer NOT NULL,
    realizationid integer,
    partnerid integer
);


ALTER TABLE program.realizationpartner OWNER TO postgres;

--
-- Name: realizationphoto; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationphoto (
    photoid integer NOT NULL,
    photofilename character varying(100),
    realizationid integer,
    photodescription character varying(200)
);


ALTER TABLE program.realizationphoto OWNER TO postgres;

--
-- Name: realizationreturn; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationreturn (
    returnid integer NOT NULL,
    returndate timestamp without time zone,
    returndescription character varying(200),
    returnamount numeric(30,8),
    realizationid integer,
    branchcode character varying(5),
    inputuser character varying(50),
    inputdate timestamp without time zone,
    authuser character varying(50),
    authdate timestamp without time zone,
    transactionid integer,
    costamount numeric(30,4)
);


ALTER TABLE program.realizationreturn OWNER TO postgres;

--
-- Name: realizationreturndetail; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationreturndetail (
    returndetailid integer NOT NULL,
    returnamount numeric(30,8),
    detaildescription character varying(200),
    realizationamount numeric(30,8),
    transactionid integer,
    returnid integer,
    realizationdetailid integer,
    accountno character varying(30),
    mustahiqproductid integer
);


ALTER TABLE program.realizationreturndetail OWNER TO postgres;

--
-- Name: realizationtransactionitem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.realizationtransactionitem (
    transactionitemid integer NOT NULL,
    ashnaf character varying(1),
    transactionproductid integer,
    budgetid integer,
    fundproductid integer,
    partnerid integer,
    employeeid character varying(20),
    returnamount numeric(36,10),
    distributionamount numeric(36,10),
    statusrecrepdetailid integer
);


ALTER TABLE program.realizationtransactionitem OWNER TO postgres;

--
-- Name: reconcileprocess; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.reconcileprocess (
    reconcileprocessid integer NOT NULL,
    reconciledate timestamp(6) without time zone,
    reconcileuser character varying(20),
    reconcileterminal character varying(15),
    processstatus character varying(1),
    description character varying(200),
    statementmonth character varying(20),
    statementyear character varying(4),
    isallstatementproceed character varying(1),
    numberofproceed integer,
    reconciletype character varying(2)
);


ALTER TABLE program.reconcileprocess OWNER TO postgres;

--
-- Name: reconciletransaction; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.reconciletransaction (
    banktransactionid integer NOT NULL,
    reconciledate timestamp(6) without time zone,
    userreconcile character varying(80),
    klaim character varying(2),
    saldo character varying(1),
    accountdebet character varying(20)
);


ALTER TABLE program.reconciletransaction OWNER TO postgres;

--
-- Name: reconciletransactionqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.reconciletransactionqurban (
    reconciletransactionqurbanid integer CONSTRAINT reconciletransactionqurban_reconciletransactionqurbani_not_null NOT NULL,
    banktransactionid integer NOT NULL,
    reconciledate timestamp(6) without time zone,
    userreconcile character varying(80),
    accountdebet character varying(20)
);


ALTER TABLE program.reconciletransactionqurban OWNER TO postgres;

--
-- Name: region; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.region (
    regionid integer NOT NULL,
    regionname character varying(20),
    description character varying(100)
);


ALTER TABLE program.region OWNER TO postgres;

--
-- Name: rekeningpenghimpunanqurban; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.rekeningpenghimpunanqurban (
    rekeningpenghimpunanqurbanid integer CONSTRAINT rekeningpenghimpunanqurban_rekeningpenghimpunanqurbani_not_null NOT NULL,
    active character varying(1),
    nomorrekening character varying(30),
    description character varying(50)
);


ALTER TABLE program.rekeningpenghimpunanqurban OWNER TO postgres;

--
-- Name: rencanadistribusi; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.rencanadistribusi (
    rencanadistribusiid integer NOT NULL,
    productid integer,
    tanggal timestamp(6) without time zone,
    namalokasi character varying(100),
    bentukdistribusi character varying(1),
    jumlahhewanqurban integer,
    nominaldana double precision,
    keterangan character varying(500)
);


ALTER TABLE program.rencanadistribusi OWNER TO postgres;

--
-- Name: rencanadistribusihewan; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.rencanadistribusihewan (
    rencanadistribusihewanid integer NOT NULL,
    ekuivalendana double precision,
    rencanajumlah integer,
    jenishewan character varying(20),
    rencanadistribusiid integer
);


ALTER TABLE program.rencanadistribusihewan OWNER TO postgres;

--
-- Name: requestdistribusi; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.requestdistribusi (
    requestdistribusiid integer NOT NULL,
    namalokasi character varying(50),
    productid integer,
    donorid integer
);


ALTER TABLE program.requestdistribusi OWNER TO postgres;

--
-- Name: reversetransaction; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.reversetransaction (
    sourcetransactionid integer NOT NULL,
    revtransactionid integer
);


ALTER TABLE program.reversetransaction OWNER TO postgres;

--
-- Name: seq_activityappraisal; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_activityappraisal
    START WITH 24
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_activityappraisal OWNER TO postgres;

--
-- Name: seq_activityappraisalitem; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_activityappraisalitem
    START WITH 56
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_activityappraisalitem OWNER TO postgres;

--
-- Name: seq_activityappraisalitemtemplate; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_activityappraisalitemtemplate
    START WITH 45
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_activityappraisalitemtemplate OWNER TO postgres;

--
-- Name: seq_agenda; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_agenda
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_agenda OWNER TO postgres;

--
-- Name: seq_agendaitem; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_agendaitem
    START WITH 6
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_agendaitem OWNER TO postgres;

--
-- Name: seq_agendaitemtemplate; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_agendaitemtemplate
    START WITH 14
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_agendaitemtemplate OWNER TO postgres;

--
-- Name: seq_agendatemplate; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_agendatemplate
    START WITH 4
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_agendatemplate OWNER TO postgres;

--
-- Name: seq_appraisal; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_appraisal
    START WITH 36
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_appraisal OWNER TO postgres;

--
-- Name: seq_appraisalitem; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_appraisalitem
    START WITH 377
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_appraisalitem OWNER TO postgres;

--
-- Name: seq_appraisalitemtemplate; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_appraisalitemtemplate
    START WITH 100
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_appraisalitemtemplate OWNER TO postgres;

--
-- Name: seq_aqhpropose; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_aqhpropose
    START WITH 26
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_aqhpropose OWNER TO postgres;

--
-- Name: seq_bankaccountlist; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_bankaccountlist
    START WITH 103
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_bankaccountlist OWNER TO postgres;

--
-- Name: seq_companion; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_companion
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_companion OWNER TO postgres;

--
-- Name: seq_companionvisit; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_companionvisit
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_companionvisit OWNER TO postgres;

--
-- Name: seq_companionvisititem; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_companionvisititem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_companionvisititem OWNER TO postgres;

--
-- Name: seq_companionvisititemtemplate; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_companionvisititemtemplate
    START WITH 10
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_companionvisititemtemplate OWNER TO postgres;

--
-- Name: seq_costitem; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_costitem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_costitem OWNER TO postgres;

--
-- Name: seq_customer; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_customer
    START WITH 379
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_customer OWNER TO postgres;

--
-- Name: seq_detailklaimtransaksiproject; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_detailklaimtransaksiproject
    START WITH 5
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_detailklaimtransaksiproject OWNER TO postgres;

--
-- Name: seq_donor; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_donor
    START WITH 65
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_donor OWNER TO postgres;

--
-- Name: seq_event; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_event
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_event OWNER TO postgres;

--
-- Name: seq_eventplan; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_eventplan
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_eventplan OWNER TO postgres;

--
-- Name: seq_itemuploadedstatement; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_itemuploadedstatement
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_itemuploadedstatement OWNER TO postgres;

--
-- Name: seq_klaimtransaksiproject; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_klaimtransaksiproject
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_klaimtransaksiproject OWNER TO postgres;

--
-- Name: seq_linkedprograms; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_linkedprograms
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_linkedprograms OWNER TO postgres;

--
-- Name: seq_marketingqurban; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_marketingqurban
    START WITH 27
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_marketingqurban OWNER TO postgres;

--
-- Name: seq_masterjenisdonasiqurban; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_masterjenisdonasiqurban
    START WITH 6
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_masterjenisdonasiqurban OWNER TO postgres;

--
-- Name: seq_mpzzisallocation; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_mpzzisallocation
    START WITH 5
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_mpzzisallocation OWNER TO postgres;

--
-- Name: seq_mustahiq; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_mustahiq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_mustahiq OWNER TO postgres;

--
-- Name: seq_mustahiqadditionalinfo; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_mustahiqadditionalinfo
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_mustahiqadditionalinfo OWNER TO postgres;

--
-- Name: seq_mustahiqgroup; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_mustahiqgroup
    START WITH 246
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_mustahiqgroup OWNER TO postgres;

--
-- Name: seq_mustahiqproduct; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_mustahiqproduct
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_mustahiqproduct OWNER TO postgres;

--
-- Name: seq_mustahiqproductgroup; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_mustahiqproductgroup
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_mustahiqproductgroup OWNER TO postgres;

--
-- Name: seq_orphandebtlist; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_orphandebtlist
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_orphandebtlist OWNER TO postgres;

--
-- Name: seq_orphansiblings; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_orphansiblings
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_orphansiblings OWNER TO postgres;

--
-- Name: seq_orphantertiarylist; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_orphantertiarylist
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_orphantertiarylist OWNER TO postgres;

--
-- Name: seq_partner; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_partner
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_partner OWNER TO postgres;

--
-- Name: seq_picdistribusi; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_picdistribusi
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_picdistribusi OWNER TO postgres;

--
-- Name: seq_product; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_product
    START WITH 40
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_product OWNER TO postgres;

--
-- Name: seq_productdetail; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_productdetail
    START WITH 10
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_productdetail OWNER TO postgres;

--
-- Name: seq_productgroup; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_productgroup
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_productgroup OWNER TO postgres;

--
-- Name: seq_proposal; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_proposal
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_proposal OWNER TO postgres;

--
-- Name: seq_realization; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realization
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realization OWNER TO postgres;

--
-- Name: seq_realizationbudget; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationbudget
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationbudget OWNER TO postgres;

--
-- Name: seq_realizationcost; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationcost
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationcost OWNER TO postgres;

--
-- Name: seq_realizationdetail; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationdetail
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationdetail OWNER TO postgres;

--
-- Name: seq_realizationmemo; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationmemo
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationmemo OWNER TO postgres;

--
-- Name: seq_realizationmemodetail; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationmemodetail
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationmemodetail OWNER TO postgres;

--
-- Name: seq_realizationpartner; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationpartner
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationpartner OWNER TO postgres;

--
-- Name: seq_realizationphoto; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationphoto
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationphoto OWNER TO postgres;

--
-- Name: seq_realizationreturn; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationreturn
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationreturn OWNER TO postgres;

--
-- Name: seq_realizationreturndetail; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_realizationreturndetail
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_realizationreturndetail OWNER TO postgres;

--
-- Name: seq_reconcileprocess; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_reconcileprocess
    START WITH 43
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_reconcileprocess OWNER TO postgres;

--
-- Name: seq_region; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_region
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_region OWNER TO postgres;

--
-- Name: seq_rekeningpenghimpunanqurban; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_rekeningpenghimpunanqurban
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_rekeningpenghimpunanqurban OWNER TO postgres;

--
-- Name: seq_requestdistribusi; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_requestdistribusi
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_requestdistribusi OWNER TO postgres;

--
-- Name: seq_statusreceivablereport; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_statusreceivablereport
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_statusreceivablereport OWNER TO postgres;

--
-- Name: seq_statusrecrepdetail; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_statusrecrepdetail
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_statusrecrepdetail OWNER TO postgres;

--
-- Name: seq_transaction; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_transaction
    START WITH 19
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_transaction OWNER TO postgres;

--
-- Name: seq_transactionitem; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_transactionitem
    START WITH 26
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_transactionitem OWNER TO postgres;

--
-- Name: seq_uploadedstatement; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_uploadedstatement
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_uploadedstatement OWNER TO postgres;

--
-- Name: seq_visit; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_visit
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_visit OWNER TO postgres;

--
-- Name: seq_visititem; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_visititem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_visititem OWNER TO postgres;

--
-- Name: seq_visitperson; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_visitperson
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_visitperson OWNER TO postgres;

--
-- Name: seq_worksector; Type: SEQUENCE; Schema: program; Owner: postgres
--

CREATE SEQUENCE program.seq_worksector
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE program.seq_worksector OWNER TO postgres;

--
-- Name: sessionblob; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.sessionblob (
    id integer NOT NULL,
    sessionid character varying(100),
    sessioncontext integer,
    id1 integer
);


ALTER TABLE program.sessionblob OWNER TO postgres;

--
-- Name: statusreceivablereport; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.statusreceivablereport (
    statusreceivableid integer NOT NULL,
    programtype character varying(1),
    realizationid integer,
    realmemoid integer,
    receivablereportamount numeric(36,10),
    receivablereportdate timestamp without time zone,
    receivableinputdate timestamp without time zone,
    receivablereportdesc character varying(200),
    receivablereportstatus character varying(10),
    receivablereportuserauth character varying(30),
    receivablereportuserinput character varying(30),
    branchcode character varying(10),
    lastupdatedate timestamp without time zone,
    lastupdateuser character varying(30)
);


ALTER TABLE program.statusreceivablereport OWNER TO postgres;

--
-- Name: statusrecrepdetail; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.statusrecrepdetail (
    statusrecrepdetailid integer NOT NULL,
    productid integer,
    ashnaf character varying(1),
    mustahiqproductid integer,
    detaildescription character varying(200),
    accountno character varying(30),
    realizationamount numeric(36,10),
    reportamount numeric(36,10),
    statusreceivableid integer NOT NULL,
    transactionid integer,
    realizationdetailid integer,
    reportdetailstatus character varying(1),
    recipientname character varying(100),
    recipientphonenumber character varying(30),
    processdate timestamp without time zone,
    updatedate timestamp without time zone,
    updateuser character varying(30)
);


ALTER TABLE program.statusrecrepdetail OWNER TO postgres;

--
-- Name: tmp_budget; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.tmp_budget (
    realizationid integer,
    budgetid integer,
    productid integer
);


ALTER TABLE program.tmp_budget OWNER TO postgres;

--
-- Name: tmp_migmustahiqproduct; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.tmp_migmustahiqproduct (
    productid integer,
    mustahiqid integer,
    mustahiqextnumber character varying(30),
    iseligible character varying(1),
    noteligiblereason character varying(2),
    mustahiqextfield character varying(50),
    noteligibledate timestamp(6) without time zone,
    companionid integer,
    status character varying(1),
    noteligiblelegal character varying(100),
    lastfundingperiod integer,
    pendingfund double precision,
    mustahiqproducttype character varying(1),
    mustahiqproductid integer,
    startdate timestamp without time zone,
    mustahiqproductname character varying(200),
    dateend timestamp without time zone,
    distributionamount numeric(30,2),
    datestart timestamp without time zone,
    proposalid integer,
    mustahiqproductgroupid integer,
    accountno character varying(30),
    branchcode character varying(10),
    ashnaf character varying(1),
    fundproductid integer
);


ALTER TABLE program.tmp_migmustahiqproduct OWNER TO postgres;

--
-- Name: tmp_migrasikodepos; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.tmp_migrasikodepos (
    baris integer,
    kode_pos character varying(20),
    desa character varying(100),
    is_valid character varying(2),
    is_auth character varying(2),
    kecamatan character varying(100),
    kode_kecamatan character varying(7),
    kota character varying(100),
    kode_kota character varying(7),
    propinsi character varying(100),
    kode_propinsi character varying(7),
    keterangan character varying(100)
);


ALTER TABLE program.tmp_migrasikodepos OWNER TO postgres;

--
-- Name: transaction; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.transaction (
    transactionid integer NOT NULL,
    transactiondate timestamp(6) without time zone,
    referenceno character varying(30),
    description character varying(100),
    inputer character varying(20),
    transactioncode character varying(10),
    branchcode character varying(5),
    authuser character varying(20),
    transactiontime timestamp(6) without time zone,
    authdate timestamp(6) without time zone,
    isposted character varying(1),
    authaction character varying(1),
    transactionblockid integer,
    channelcode character varying,
    inputdate timestamp(6) without time zone,
    transactionno character varying(30),
    paidto character varying(30),
    amount double precision,
    currencycode character varying(5),
    receivedfrom character varying(30),
    channelaccountno character varying(30),
    rate double precision,
    isauthorized character varying(1),
    coretransactionid integer,
    coretransactionno character varying(30),
    transactiontype character varying(1),
    realizationid integer,
    returnid integer,
    statusreceivableid integer,
    coresourcetransactionid integer,
    sourcetransactionid integer
);


ALTER TABLE program.transaction OWNER TO postgres;

--
-- Name: transactionaccount; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.transactionaccount (
    accountno character varying(30) NOT NULL,
    accountname character varying(50),
    linkaccountcode character varying(20),
    accountstatus character varying(1),
    opendate timestamp(6) without time zone,
    balance double precision,
    description character varying(200),
    usercreated character varying(20),
    userotorized character varying(20),
    datecreated timestamp(6) without time zone,
    dateotorized timestamp(6) without time zone,
    terminalcreated character varying(15),
    terminalotorized character varying(15),
    transactionaccounttype character varying(1),
    currency_code character varying(20),
    branchcode character varying(3)
);


ALTER TABLE program.transactionaccount OWNER TO postgres;

--
-- Name: transactiontype; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.transactiontype (
    transactioncode character varying(10) NOT NULL,
    description character varying(50),
    vouchercode character varying(10)
);


ALTER TABLE program.transactiontype OWNER TO postgres;

--
-- Name: uploadedstatement; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.uploadedstatement (
    uploadedstatementid integer NOT NULL,
    reconcileprocessid integer,
    branchcode character varying(5),
    uploaddate timestamp(6) without time zone,
    userfilename character varying(50),
    systemfilename character varying(50),
    isuploadsucceed character varying(1),
    isreconciled character varying(1),
    reconcileuser character varying(20),
    statementyear character varying(4),
    statementmonth character varying(20),
    ispicapprove character varying(1),
    isbasereconciled character varying(1),
    ismarginreconciled character varying(1)
);


ALTER TABLE program.uploadedstatement OWNER TO postgres;

--
-- Name: v_mustahiq; Type: VIEW; Schema: program; Owner: postgres
--

CREATE VIEW program.v_mustahiq AS
 SELECT m.mustahiqid,
    c.customername,
    c.addressstreet,
    c.addresskecamatan,
    c.addresskelurahan
   FROM program.mustahiq m,
    program.customer c
  WHERE (m.customerid = c.customerid);


ALTER VIEW program.v_mustahiq OWNER TO postgres;

--
-- Name: v_mustahiqdata; Type: VIEW; Schema: program; Owner: postgres
--

CREATE VIEW program.v_mustahiqdata AS
 SELECT m.mustahiqid,
    m.mustahiqtype,
    m.ashnaf,
    c.customerid,
    c.customername,
    c.addressstreet,
    c.addresskecamatan,
    c.addresskelurahan,
    c.addresspostalcode,
    c.addressstate,
    c.addresscity
   FROM program.mustahiq m,
    program.customer c
  WHERE (m.customerid = c.customerid);


ALTER VIEW program.v_mustahiqdata OWNER TO postgres;

--
-- Name: reconciletransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.reconciletransaction (
    banktransactionid integer NOT NULL,
    transactiondate timestamp(6) without time zone,
    bankaccountno character varying(20),
    accountdebet character varying(20),
    amount numeric(38,2),
    description character varying(200),
    transactioncode character varying(10),
    fundentity integer,
    productid integer,
    branchcode character varying(5),
    reconstatus character varying(1),
    transactionid integer,
    processstatus character varying(1),
    mutationtype character varying(1),
    referenceno character varying(50),
    processaccountcode character varying(20),
    processaccounttype character varying(1)
);


ALTER TABLE transaction.reconciletransaction OWNER TO postgres;

--
-- Name: v_reconcilequrban; Type: VIEW; Schema: program; Owner: postgres
--

CREATE VIEW program.v_reconcilequrban AS
 SELECT banktransactionid,
    transactiondate,
    bankaccountno,
    accountdebet,
    amount,
    description,
    mutationtype,
    referenceno
   FROM transaction.reconciletransaction;


ALTER VIEW program.v_reconcilequrban OWNER TO postgres;

--
-- Name: v_reconciletransaction; Type: VIEW; Schema: program; Owner: postgres
--

CREATE VIEW program.v_reconciletransaction AS
 SELECT banktransactionid,
    transactiondate,
    bankaccountno,
    accountdebet,
    amount,
    description,
    mutationtype,
    referenceno
   FROM transaction.reconciletransaction
  WHERE ((reconstatus)::text <> 'T'::text);


ALTER VIEW program.v_reconciletransaction OWNER TO postgres;

--
-- Name: vemployee; Type: VIEW; Schema: program; Owner: postgres
--

CREATE VIEW program.vemployee AS
 SELECT e.employeeid,
    i.individuname AS employeename
   FROM (personalia.employee e
     JOIN personalia.individu i ON ((e.individuid = i.individuid)));


ALTER VIEW program.vemployee OWNER TO postgres;

--
-- Name: visit; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.visit (
    visitid integer NOT NULL,
    visitdate timestamp without time zone,
    visitlocation character varying(200),
    visitbegintime timestamp without time zone,
    visitendtime timestamp without time zone,
    visitaddress character varying(200),
    visittype character varying(1),
    mustahiqproductid integer,
    mustahiqid integer
);


ALTER TABLE program.visit OWNER TO postgres;

--
-- Name: visititem; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.visititem (
    visititemid integer NOT NULL,
    visititemtype character varying(1),
    visititemannotation character varying(200),
    visitid integer
);


ALTER TABLE program.visititem OWNER TO postgres;

--
-- Name: visitperson; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.visitperson (
    visitpersonid integer NOT NULL,
    visitid integer,
    visitpersonname character varying(100),
    visitpersonposition character varying(100),
    visitpersontype character varying(1)
);


ALTER TABLE program.visitperson OWNER TO postgres;

--
-- Name: volunteer; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.volunteer (
    volunteerid character varying(10) NOT NULL,
    volunteername character varying(50),
    homeaddress character varying(150),
    homephone character varying(20),
    mobilephone character varying(20),
    email character varying(50),
    totalamount double precision,
    branchcode character varying(5)
);


ALTER TABLE program.volunteer OWNER TO postgres;

--
-- Name: volunteertransaction; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.volunteertransaction (
    transactionitemid integer NOT NULL,
    volunteerid character varying(10)
);


ALTER TABLE program.volunteertransaction OWNER TO postgres;

--
-- Name: vproduct; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.vproduct (
    productcode character varying(30),
    productname character varying(30),
    accountno character varying(30) NOT NULL,
    accountname character varying(50),
    branchcode character varying(5),
    producttype character varying(1),
    status character varying(1),
    currencycode character varying(20),
    fundcategory character varying(1),
    percentageofamilfunds double precision,
    productid integer,
    idx character varying(40)
);


ALTER TABLE program.vproduct OWNER TO postgres;

--
-- Name: worksector; Type: TABLE; Schema: program; Owner: postgres
--

CREATE TABLE program.worksector (
    workid integer NOT NULL,
    workcode character varying(10),
    workname character varying(100),
    statusaktif character varying(1)
);


ALTER TABLE program.worksector OWNER TO postgres;

--
-- Name: accountdetail; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accountdetail (
    fl_account character varying(20) DEFAULT NULL::character varying NOT NULL,
    fl_detail_account character varying(20) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE public.accountdetail OWNER TO postgres;

--
-- Name: accountgroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accountgroup (
    accountgroup_code character varying(5) DEFAULT NULL::character varying,
    accountgroup_name character varying(30) DEFAULT NULL::character varying,
    id integer NOT NULL
);


ALTER TABLE public.accountgroup OWNER TO postgres;

--
-- Name: accountinterface; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accountinterface (
    interface_code character varying(10) DEFAULT NULL::character varying NOT NULL,
    account_code character varying(20) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    interface_type character varying(1) DEFAULT NULL::character varying,
    is_active character varying(1) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE public.accountinterface OWNER TO postgres;

--
-- Name: accountinterfacemember; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accountinterfacemember (
    member_id integer NOT NULL,
    interface_code character varying(10) DEFAULT NULL::character varying,
    account_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE public.accountinterfacemember OWNER TO postgres;

--
-- Name: accountmanager; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accountmanager (
    amcode character varying(10) DEFAULT NULL::character varying NOT NULL,
    rcno character varying(4) DEFAULT NULL::character varying,
    employeeid character varying(20) DEFAULT NULL::character varying,
    employeename character varying(50) DEFAULT NULL::character varying,
    project_no character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE public.accountmanager OWNER TO postgres;

--
-- Name: accsubsystem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accsubsystem (
    subsystemcode character varying(20) DEFAULT NULL::character varying NOT NULL,
    titlesubsystem character varying(50) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    servername character varying(30) DEFAULT NULL::character varying,
    username character varying(20) DEFAULT NULL::character varying,
    password character varying(30) DEFAULT NULL::character varying,
    createjournalscriptid character varying(100) DEFAULT NULL::character varying,
    sessionname character varying(30) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    usecurrentlogin character varying(1) DEFAULT NULL::character varying,
    authjournalscriptid character varying(80) DEFAULT NULL::character varying,
    applicationid character varying(80) DEFAULT NULL::character varying,
    oldstylescripting integer
);


ALTER TABLE public.accsubsystem OWNER TO postgres;

--
-- Name: appsubsystem; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appsubsystem (
    subsystem_code character varying(5) NOT NULL,
    subsystem_name character varying(30),
    is_local character varying(1),
    session_name character varying(20),
    remote_host character varying(23),
    remote_port integer,
    is_ssl character varying(1),
    ssl_profile_name character varying(30),
    remote_appid character varying(50)
);


ALTER TABLE public.appsubsystem OWNER TO postgres;

--
-- Name: blobregistration; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.blobregistration (
    id integer NOT NULL,
    actualfilename character varying(128) DEFAULT NULL::character varying
);


ALTER TABLE public.blobregistration OWNER TO postgres;

--
-- Name: branchlocation; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.branchlocation AS
 SELECT kode_cabang AS branch_code,
    nama_cabang AS branchname,
        CASE
            WHEN (((tipe_cabang)::text = 'CU'::text) OR ((tipe_cabang)::text = 'PO'::text)) THEN 'B'::text
            ELSE 'S'::text
        END AS branchstatus,
    user_input AS user_id,
    tanggal_input AS last_update,
    kode_cabang_induk AS masterbranch_code,
    0 AS dataid
   FROM enterprise.cabang;


ALTER VIEW public.branchlocation OWNER TO postgres;

--
-- Name: branchlocation_old; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.branchlocation_old (
    branch_code character varying(5) DEFAULT NULL::character varying NOT NULL,
    branchname character varying(50) DEFAULT NULL::character varying,
    branchstatus character varying(1) DEFAULT NULL::character varying,
    user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    masterbranch_code character varying(5) DEFAULT NULL::character varying,
    dataid integer
);


ALTER TABLE public.branchlocation_old OWNER TO postgres;

--
-- Name: cpalpamapping; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cpalpamapping (
    fl_lpa_accountcode character varying(20) DEFAULT NULL::character varying,
    fl_cpa_accountcode character varying(20) DEFAULT NULL::character varying,
    cpalpamapping_id integer NOT NULL
);


ALTER TABLE public.cpalpamapping OWNER TO postgres;

--
-- Name: currency_pkpu; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.currency_pkpu (
    currency_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    description character varying(64) DEFAULT NULL::character varying,
    currentvalue double precision,
    isdefault character varying(1) DEFAULT NULL::character varying,
    isstandard character varying(1) DEFAULT NULL::character varying,
    centralbank_currency_code character varying(20) DEFAULT NULL::character varying,
    short_name character varying(10) DEFAULT NULL::character varying,
    full_name character varying(50) DEFAULT NULL::character varying,
    country_owner character varying(30) DEFAULT NULL::character varying,
    kurs_buku double precision,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_tengah_bi double precision,
    kurs_beli_kantor_pusat double precision,
    kurs_jual_kantor_pusat double precision,
    tanggal_limit timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_otorisasi character varying(20) DEFAULT NULL::character varying,
    tanggal_otorisasi timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_otorisasi character varying(15) DEFAULT NULL::character varying,
    kurs_neraca double precision,
    deviasi_maksimal double precision,
    kurs_reval double precision,
    kurs_remittance double precision,
    symbol character varying(10),
    symbol_says character varying(50)
);


ALTER TABLE public.currency_pkpu OWNER TO postgres;

--
-- Name: custom_idgen; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.custom_idgen (
    idname character varying(30) DEFAULT NULL::character varying NOT NULL,
    idcode character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public.custom_idgen OWNER TO postgres;

--
-- Name: daemons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.daemons (
    "Start" text NOT NULL,
    "Info" text NOT NULL
);


ALTER TABLE public.daemons OWNER TO postgres;

--
-- Name: mustahiqadditionalinfo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mustahiqadditionalinfo (
    mustahiqinfoid integer NOT NULL,
    mustahiqproductid integer,
    mustahiqid integer,
    mustahiqinfotype character varying(1),
    mustahiqidsupervisor integer,
    schoolname character varying(200),
    sd_kelas character varying(10),
    sd_tahunawal timestamp without time zone,
    sd_tahunakhir timestamp without time zone,
    smp_kelas character varying(10),
    smp_tahunawal timestamp without time zone,
    smp_tahunakhir timestamp without time zone,
    sma_kelas character varying(10),
    sma_tahunawal timestamp without time zone,
    sma_tahunakhir timestamp without time zone,
    achievement character varying(500),
    universitas_kelas character varying(10),
    universitas_tahunawal timestamp without time zone,
    universitas_tahunakhir timestamp without time zone
);


ALTER TABLE public.mustahiqadditionalinfo OWNER TO postgres;

--
-- Name: seq_menu; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seq_menu
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seq_menu OWNER TO postgres;

--
-- Name: seq_menuhierarchy; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seq_menuhierarchy
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seq_menuhierarchy OWNER TO postgres;

--
-- Name: seq_mustahiqadditionalinfo; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seq_mustahiqadditionalinfo
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seq_mustahiqadditionalinfo OWNER TO postgres;

--
-- Name: seq_rolemenulist; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seq_rolemenulist
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seq_rolemenulist OWNER TO postgres;

--
-- Name: seq_usermenulist; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.seq_usermenulist
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.seq_usermenulist OWNER TO postgres;

--
-- Name: tmp_migrasikodepos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tmp_migrasikodepos (
    baris integer,
    kode_pos character varying(20),
    desa character varying(100),
    is_valid character varying(2),
    is_auth character varying(2),
    kecamatan character varying(100),
    kode_kecamatan character varying(7),
    kota character varying(100),
    kode_kota character varying(7),
    propinsi character varying(100),
    kode_propinsi character varying(7),
    keterangan character varying(100)
);


ALTER TABLE public.tmp_migrasikodepos OWNER TO postgres;

--
-- Name: academicvalue; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.academicvalue (
    academicvalueid integer NOT NULL,
    academicvaluetemplateid integer,
    mustahiqid integer,
    productid integer,
    date timestamp(6) without time zone,
    yearschool character varying(10),
    semester integer
);


ALTER TABLE school.academicvalue OWNER TO postgres;

--
-- Name: academicvalueitem; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.academicvalueitem (
    academicvalueitemid integer NOT NULL,
    academicvalueid integer,
    academicvalueitemtemplateid integer,
    integervalue integer,
    floatvalue double precision,
    stringvalue character varying(200),
    boolvalue character varying(1),
    valuedatatype character varying(1),
    matpel character varying(200),
    kkm integer
);


ALTER TABLE school.academicvalueitem OWNER TO postgres;

--
-- Name: academicvalueitemtemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.academicvalueitemtemplate (
    academicvalueitemtemplateid integer NOT NULL,
    academicvaluetemplateid integer,
    isactive character varying(1),
    subjectid integer,
    integervaluestandard integer,
    floatvaluestandard double precision,
    stringvaluestandard character varying(200),
    boolvaluestandard character varying(1),
    valuedatatype character varying(1),
    matpel character varying(30),
    kkm integer
);


ALTER TABLE school.academicvalueitemtemplate OWNER TO postgres;

--
-- Name: academicvaluetemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.academicvaluetemplate (
    academicvaluetemplateid integer NOT NULL,
    description character varying(200),
    templatename character varying(200),
    semester integer,
    schoolyearcode character varying(5)
);


ALTER TABLE school.academicvaluetemplate OWNER TO postgres;

--
-- Name: achievement; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.achievement (
    employeeid character varying(20) DEFAULT NULL::character varying NOT NULL,
    achievementname character varying(100) DEFAULT NULL::character varying,
    achievementid integer NOT NULL,
    institution character varying(100) DEFAULT NULL::character varying,
    achievementdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school.achievement OWNER TO postgres;

--
-- Name: achievementactivities; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.achievementactivities (
    achievementactivitiesid integer NOT NULL,
    mustahiqid integer NOT NULL,
    productid integer NOT NULL,
    activityschoolid integer NOT NULL,
    achievementname character varying(100) DEFAULT NULL::character varying,
    institution character varying(100) DEFAULT NULL::character varying,
    achievementdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school.achievementactivities OWNER TO postgres;

--
-- Name: activityappraisal; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.activityappraisal (
    activityappraisalid integer NOT NULL,
    appraisaldate timestamp(6) without time zone,
    weekperiod integer,
    monthperiod integer,
    anualperiod integer,
    appraisalyear character varying(4),
    approvalstatus character varying(1),
    otherappraisalid integer,
    otherappraisalflag character varying(1),
    mustahiqid integer,
    companionid integer
);


ALTER TABLE school.activityappraisal OWNER TO postgres;

--
-- Name: activityappraisalitem; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.activityappraisalitem (
    itemid integer NOT NULL,
    integervalue integer,
    floatvalue double precision,
    stringvalue character varying(200),
    boolvalue character varying(1),
    activityappraisalid integer,
    itemtemplateid integer
);


ALTER TABLE school.activityappraisalitem OWNER TO postgres;

--
-- Name: activityappraisalitemtemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.activityappraisalitemtemplate (
    itemtemplateid integer NOT NULL,
    sequenceno integer,
    description character varying(200),
    isactive character varying(1),
    productid integer,
    mustahiqid integer,
    integervaluestandard integer,
    floatvaluestandard double precision,
    stringvaluestandard character varying(200),
    boolvaluestandard character varying(1),
    itemname character varying(50),
    groupname character varying(20),
    valuedatatype character varying(1),
    productgroupname character varying(50)
);


ALTER TABLE school.activityappraisalitemtemplate OWNER TO postgres;

--
-- Name: activityschool; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.activityschool (
    activityschoolid integer NOT NULL,
    activityname character varying(30),
    activitylocation character varying(50),
    activitydate timestamp(6) without time zone,
    activitydescription character varying(200),
    activitylevel character varying(3),
    activitytype character varying(2)
);


ALTER TABLE school.activityschool OWNER TO postgres;

--
-- Name: agenda; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.agenda (
    agendaid integer NOT NULL,
    agendatemplateid integer,
    mustahiqid integer,
    productid integer
);


ALTER TABLE school.agenda OWNER TO postgres;

--
-- Name: agendaitem; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.agendaitem (
    agendaid integer,
    agendaitemid integer NOT NULL,
    agendaitemtemplateid integer,
    attendance integer
);


ALTER TABLE school.agendaitem OWNER TO postgres;

--
-- Name: agendaitemtemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.agendaitemtemplate (
    agendaitemtemplateid integer NOT NULL,
    agendatemplateid integer,
    datevalue integer,
    isevent character varying(1),
    eventplanid integer
);


ALTER TABLE school.agendaitemtemplate OWNER TO postgres;

--
-- Name: agendatemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.agendatemplate (
    agendatemplateid integer NOT NULL,
    agendaname character varying(30),
    monthvalue integer,
    quota integer,
    yearvalue integer
);


ALTER TABLE school.agendatemplate OWNER TO postgres;

--
-- Name: appraisal; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.appraisal (
    annualperiod integer,
    appraisaldate timestamp(6) without time zone,
    appraisalid integer NOT NULL,
    appraisaltemplateid integer,
    appraisalyear character varying(4),
    approvalstatus character varying(1),
    monthperiod integer,
    weekperiod integer,
    appraisalsubject character varying(1),
    subjectkeycount integer,
    customerid integer,
    subjectkey1 integer,
    subjectkey2 integer
);


ALTER TABLE school.appraisal OWNER TO postgres;

--
-- Name: appraisalitem; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.appraisalitem (
    appraisalid integer,
    boolvalue character varying(1),
    floatvalue double precision,
    integervalue integer,
    itemid integer NOT NULL,
    itemtemplateid integer,
    stringvalue character varying(200)
);


ALTER TABLE school.appraisalitem OWNER TO postgres;

--
-- Name: appraisalitemgroup; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.appraisalitemgroup (
    groupname character varying(20) NOT NULL,
    description character varying(200)
);


ALTER TABLE school.appraisalitemgroup OWNER TO postgres;

--
-- Name: appraisalitemtemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.appraisalitemtemplate (
    appraisaltemplateid integer,
    boolvaluestandard character varying(1),
    description character varying(200),
    floatvaluestandard double precision,
    integervaluestandard integer,
    isactive character varying(1),
    islowlevel character varying(1),
    itemname character varying(50),
    itemtemplateid integer NOT NULL,
    level integer,
    parentid integer,
    sequenceno integer,
    valuedatatype character varying(1),
    stringvaluestandard character varying(200)
);


ALTER TABLE school.appraisalitemtemplate OWNER TO postgres;

--
-- Name: appraisaltemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.appraisaltemplate (
    appraisalname character varying(50),
    appraisaltemplateid integer NOT NULL,
    description character varying(200),
    formula character varying(285)
);


ALTER TABLE school.appraisaltemplate OWNER TO postgres;

--
-- Name: attendance; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.attendance (
    attendanceid integer NOT NULL,
    attendancedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    attendancestatus character varying(1) DEFAULT NULL::character varying,
    arrivalstatus character varying(2) DEFAULT NULL::character varying,
    description character varying(100) DEFAULT NULL::character varying,
    returntime time(6) without time zone DEFAULT NULL::time without time zone,
    overtime1 double precision,
    overtime2 double precision,
    overtime3 double precision,
    overtime4 double precision,
    totalovertime double precision,
    arrivaluserinput character varying(20) DEFAULT NULL::character varying,
    arrivalterminalinput character varying(15) DEFAULT NULL::character varying,
    returnuserinput character varying(20) DEFAULT NULL::character varying,
    returnterminalinput character varying(15) DEFAULT NULL::character varying,
    employeeid character varying(20) DEFAULT NULL::character varying,
    arriveovertime double precision,
    returnovertime double precision,
    arrivetime time(6) without time zone DEFAULT NULL::time without time zone,
    overtime5 double precision
);


ALTER TABLE school.attendance OWNER TO postgres;

--
-- Name: careerhistory; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.careerhistory (
    careerhistoryid integer NOT NULL,
    employeeid character varying(20) DEFAULT NULL::character varying,
    workunitid character varying(50) DEFAULT NULL::character varying,
    positionid character varying(50) DEFAULT NULL::character varying,
    effectivedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school.careerhistory OWNER TO postgres;

--
-- Name: classhistory; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.classhistory (
    classhistoryid integer NOT NULL,
    productid integer NOT NULL,
    mustahiqid integer NOT NULL,
    studentclasscode character varying(100),
    schoolyearcode character varying(5),
    description character varying(50),
    semester character varying(50)
);


ALTER TABLE school.classhistory OWNER TO postgres;

--
-- Name: club; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.club (
    clubid integer NOT NULL,
    productid integer,
    clubname character varying(50),
    clubstatus character varying(1),
    progress character varying(500)
);


ALTER TABLE school.club OWNER TO postgres;

--
-- Name: companion; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.companion (
    customerid integer NOT NULL,
    companionid integer NOT NULL,
    parentid integer,
    companionextnumber character varying(60)
);


ALTER TABLE school.companion OWNER TO postgres;

--
-- Name: companioncontract; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.companioncontract (
    contractno character varying(100) NOT NULL,
    companionid integer,
    initialcontractperiod timestamp(6) without time zone,
    endcontractperiod timestamp(6) without time zone,
    description character varying(200),
    documentfile character varying(50),
    inputuser character varying(20),
    inputdate timestamp(6) without time zone,
    inputterminal character varying(15),
    productid integer,
    bmisupervisi character varying(10),
    kabkota character varying(50),
    idpropinsi integer,
    companionexperience character varying(200)
);


ALTER TABLE school.companioncontract OWNER TO postgres;

--
-- Name: companionproduct; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.companionproduct (
    productid integer NOT NULL,
    companionid integer NOT NULL,
    contractno character varying(20)
);


ALTER TABLE school.companionproduct OWNER TO postgres;

--
-- Name: companionvisit; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.companionvisit (
    companionvisitid integer NOT NULL,
    visitingdate timestamp(6) without time zone,
    visitingyear character varying(4),
    weekperiod integer,
    monthperiod integer,
    annotation character varying(500),
    approvalstatus character varying(1),
    mustahiqid integer,
    companionid integer
);


ALTER TABLE school.companionvisit OWNER TO postgres;

--
-- Name: companionvisititem; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.companionvisititem (
    itemid integer NOT NULL,
    itemtemplateid integer,
    companionvisitid integer,
    integervalue integer,
    floatvalue double precision,
    stringvalue character varying(200),
    boolvalue character varying(1)
);


ALTER TABLE school.companionvisititem OWNER TO postgres;

--
-- Name: companionvisititemtemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.companionvisititemtemplate (
    itemtemplateid integer NOT NULL,
    sequenceno integer,
    itemname character varying(50),
    description character varying(200),
    visitgroup character varying(2),
    isactive character varying(1),
    productgroupname character varying(50),
    valuedatatype character varying(1),
    answerchoice character varying(500),
    parentitem integer,
    level integer,
    islowlevel character varying(1)
);


ALTER TABLE school.companionvisititemtemplate OWNER TO postgres;

--
-- Name: contracthistory; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.contracthistory (
    employeeid character varying(20) DEFAULT NULL::character varying,
    contractno character varying(100) DEFAULT NULL::character varying NOT NULL,
    initialcontractperiod timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    endcontractperiod timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    description character varying(100) DEFAULT NULL::character varying
);


ALTER TABLE school.contracthistory OWNER TO postgres;

--
-- Name: custom_idgen; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.custom_idgen (
    idname character varying(30) NOT NULL,
    idcode character varying(50) NOT NULL,
    last_id integer,
    locked character varying(1)
);


ALTER TABLE school.custom_idgen OWNER TO postgres;

--
-- Name: customer; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.customer (
    customerid integer NOT NULL,
    customername character varying(50),
    addresscity character varying(50),
    addresskecamatan character varying(50),
    addresskelurahan character varying(50),
    addresspostalcode character varying(10),
    addressstate character varying(50),
    addressstreet character varying(200),
    addresssubdistrict character varying(50),
    branchcode character varying(5),
    customerno character varying(30),
    customerstatus character varying(1),
    phonenumber character varying(60),
    idpropinsi integer,
    idnegara integer,
    customertype character varying(2),
    fax character varying(60),
    email character varying(60),
    customernickname character varying(30)
);


ALTER TABLE school.customer OWNER TO postgres;

--
-- Name: customercorporate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.customercorporate (
    customerid integer NOT NULL,
    cpname character varying(150),
    cpphonenumber character varying(60),
    cpmobilenumber character varying(60),
    corporationnumber character varying(60),
    corporationdate timestamp(6) without time zone,
    cctype character varying(1)
);


ALTER TABLE school.customercorporate OWNER TO postgres;

--
-- Name: customerpersonal; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.customerpersonal (
    customerid integer NOT NULL,
    birthdate timestamp(6) without time zone,
    birthplace character varying(50),
    identitytype character varying(1),
    identitynumber character varying(30),
    formaleducation character varying(1),
    gender character varying(1),
    marital character varying(1),
    religion integer,
    totalfamily integer,
    worksector character varying(1),
    customerpersonaltype character varying(1),
    fathername character varying(200),
    fatheroccupation integer,
    fatherbirthdate timestamp(6) without time zone,
    fatherbirthplace character varying(50),
    fathereducation integer,
    fatherphonenumber character varying(50),
    mothername character varying(200),
    motheroccupation integer,
    motherbirthdate timestamp(6) without time zone,
    motherbirthplace character varying(50),
    mothereducation integer,
    motherphonenumber character varying(50),
    guardianname character varying(200),
    guardianoccupation integer,
    guardianbirthdate timestamp(6) without time zone,
    guardianbirthplace character varying(50),
    guardianeducation integer,
    guardianphonenumber character varying(50),
    guardianaddress character varying(200),
    educationcertificate character varying(200),
    birthcertificate character varying(200),
    familycard character varying(200),
    photo character varying(200),
    skhu character varying(200),
    schoolorigin character varying(200),
    status character varying(1),
    sourcefoundid integer,
    summemory integer,
    valueskhu integer,
    childerto character varying(20)
);


ALTER TABLE school.customerpersonal OWNER TO postgres;

--
-- Name: education; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.education (
    educationid integer NOT NULL,
    individuid integer,
    eduyear character varying(4) DEFAULT NULL::character varying,
    eduinstitution character varying(100) DEFAULT NULL::character varying,
    educationtype character varying(1) DEFAULT NULL::character varying,
    nilai character varying(10),
    description character varying(50),
    alamat character varying(100)
);


ALTER TABLE school.education OWNER TO postgres;

--
-- Name: employee; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.employee (
    employeeid character varying(20) DEFAULT NULL::character varying NOT NULL,
    supervisorid character varying(20) DEFAULT NULL::character varying,
    individuid integer,
    performanceappraisalid integer,
    targetachievementid integer,
    workunitid character varying(50) DEFAULT NULL::character varying,
    positionid character varying(50) DEFAULT NULL::character varying,
    employeestatus character varying(1) DEFAULT NULL::character varying,
    employeeentrydate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    rank integer,
    salaryhistoryid integer,
    careerhistoryid integer,
    rankhistoryid integer,
    edpid integer,
    isactive character varying(1) DEFAULT NULL::character varying,
    nonactivedescription character varying(100) DEFAULT NULL::character varying,
    nonactivedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    basicsalary double precision,
    productid integer
);


ALTER TABLE school.employee OWNER TO postgres;

--
-- Name: employeedevelopmentprogram; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.employeedevelopmentprogram (
    edpid integer NOT NULL,
    employeeid character varying(20) DEFAULT NULL::character varying,
    edpfile character varying(200) DEFAULT NULL::character varying,
    edplegalfile character varying(200) DEFAULT NULL::character varying,
    evaluatoremployee character varying(20) DEFAULT NULL::character varying,
    periodyear character varying(4) DEFAULT NULL::character varying,
    edpdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    inputdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    schoolyearcode character varying(5)
);


ALTER TABLE school.employeedevelopmentprogram OWNER TO postgres;

--
-- Name: employeetraining; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.employeetraining (
    trainingid integer NOT NULL,
    trainingdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    trainingvalue character varying(20) DEFAULT NULL::character varying,
    certificate character varying(30) DEFAULT NULL::character varying,
    traininglocation character varying(100) DEFAULT NULL::character varying,
    employeeid character varying(20) DEFAULT NULL::character varying,
    trainingdateend timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school.employeetraining OWNER TO postgres;

--
-- Name: enum_int; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.enum_int (
    enum_name character varying(32) NOT NULL,
    enum_value integer NOT NULL,
    enum_description character varying(50)
);


ALTER TABLE school.enum_int OWNER TO postgres;

--
-- Name: enum_varchar; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.enum_varchar (
    enum_name character varying(32) NOT NULL,
    enum_value character varying(2) NOT NULL,
    enum_description character varying(50)
);


ALTER TABLE school.enum_varchar OWNER TO postgres;

--
-- Name: equipment; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.equipment (
    infrastructureid integer,
    equipmentid integer NOT NULL,
    equipmentname character varying(40),
    quantity integer,
    description character varying(100),
    unit character varying(20)
);


ALTER TABLE school.equipment OWNER TO postgres;

--
-- Name: family; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.family (
    familyid integer NOT NULL,
    individuid integer,
    gender character varying(1) DEFAULT NULL::character varying,
    familyname character varying(100) DEFAULT NULL::character varying,
    birthdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    birthplace character varying(60) DEFAULT NULL::character varying,
    relationships integer,
    education integer,
    worksector character varying(100) DEFAULT NULL::character varying
);


ALTER TABLE school.family OWNER TO postgres;

--
-- Name: formaleducation; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.formaleducation (
    educationid integer NOT NULL,
    educationname integer,
    fakultas character varying(100),
    jurusan character varying(100)
);


ALTER TABLE school.formaleducation OWNER TO postgres;

--
-- Name: healthplafond; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.healthplafond (
    employeeid character varying(20) DEFAULT NULL::character varying NOT NULL,
    empid character varying(20) DEFAULT NULL::character varying,
    outpatientplafond double precision,
    inpatientplafond double precision,
    totalplafond double precision,
    realization double precision,
    finalbalance double precision,
    currentyear character varying(4) DEFAULT NULL::character varying
);


ALTER TABLE school.healthplafond OWNER TO postgres;

--
-- Name: healthreimbursement; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.healthreimbursement (
    rank integer NOT NULL,
    reimbursementtype character varying(2) DEFAULT NULL::character varying NOT NULL,
    maritalstatus character varying(2) DEFAULT NULL::character varying NOT NULL,
    reimbursementvalue double precision,
    description character varying(100) DEFAULT NULL::character varying
);


ALTER TABLE school.healthreimbursement OWNER TO postgres;

--
-- Name: id_gen; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.id_gen (
    id_code character varying(50) NOT NULL,
    last_id integer,
    locked character varying(1)
);


ALTER TABLE school.id_gen OWNER TO postgres;

--
-- Name: individu; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.individu (
    individuid integer NOT NULL,
    individuname character varying(50) DEFAULT NULL::character varying,
    addresscity character varying(50) DEFAULT NULL::character varying,
    addresskecamatan character varying(50) DEFAULT NULL::character varying,
    addresskelurahan character varying(50) DEFAULT NULL::character varying,
    addresspostalcode character varying(10) DEFAULT NULL::character varying,
    addressstate character varying(50) DEFAULT NULL::character varying,
    addressstreet character varying(200) DEFAULT NULL::character varying,
    addresssubdistrict character varying(50) DEFAULT NULL::character varying,
    branchcode character varying(5) DEFAULT NULL::character varying,
    individuno character varying(20) DEFAULT NULL::character varying,
    individutype character varying(2) DEFAULT NULL::character varying,
    individustatus character varying(1) DEFAULT NULL::character varying,
    birthdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    birthplace character varying(50) DEFAULT NULL::character varying,
    gender character varying(1) DEFAULT NULL::character varying,
    formaleducation integer,
    marital character varying(2) DEFAULT NULL::character varying,
    religion integer,
    identitytype character varying(1) DEFAULT NULL::character varying,
    identitynumber character varying(30) DEFAULT NULL::character varying,
    phonenumber character varying(20) DEFAULT NULL::character varying,
    initialname character varying(3) DEFAULT NULL::character varying,
    mobilenumberpersonal character varying(40) DEFAULT NULL::character varying,
    mobilenumbercorporate character varying(40) DEFAULT NULL::character varying,
    emailpersonal character varying(60) DEFAULT NULL::character varying,
    emailcorporate character varying(60) DEFAULT NULL::character varying,
    photo1 character varying(200) DEFAULT NULL::character varying,
    photo2 character varying(200) DEFAULT NULL::character varying,
    photo3 character varying(200) DEFAULT NULL::character varying,
    dependent integer,
    accountno character varying(20) DEFAULT NULL::character varying,
    idpropinsi integer,
    alamattinggal character varying(200)
);


ALTER TABLE school.individu OWNER TO postgres;

--
-- Name: infrastructure; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.infrastructure (
    infrastructureid integer NOT NULL,
    infrastructurename character varying(40),
    productid integer,
    parentid integer
);


ALTER TABLE school.infrastructure OWNER TO postgres;

--
-- Name: logincorporate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.logincorporate (
    login character varying(20) DEFAULT NULL::character varying NOT NULL,
    employeeid character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE school.logincorporate OWNER TO postgres;

--
-- Name: mustahiq; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.mustahiq (
    mustahiqtype character varying(2),
    mustahiqid integer NOT NULL,
    customerid integer,
    companionid integer
);


ALTER TABLE school.mustahiq OWNER TO postgres;

--
-- Name: mustahiqpersonal; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.mustahiqpersonal (
    mustahiqid integer NOT NULL
);


ALTER TABLE school.mustahiqpersonal OWNER TO postgres;

--
-- Name: mustahiqproduct; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.mustahiqproduct (
    productid integer NOT NULL,
    mustahiqid integer NOT NULL,
    mustahiqextnumber character varying(30),
    iseligible character varying(1),
    noteligiblereason character varying(2),
    mustahiqextfield character varying(50),
    noteligibledate timestamp(6) without time zone,
    companionid integer,
    status character varying(1),
    noteligiblelegal character varying(100),
    lastfundingperiod integer,
    pendingfund double precision,
    mustahiqtype character varying(1)
);


ALTER TABLE school.mustahiqproduct OWNER TO postgres;

--
-- Name: negara; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.negara (
    idnegara integer NOT NULL,
    nama_negara character varying(20)
);


ALTER TABLE school.negara OWNER TO postgres;

--
-- Name: nonformaleducation; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.nonformaleducation (
    educationid integer NOT NULL,
    educationname character varying(100) DEFAULT NULL::character varying
);


ALTER TABLE school.nonformaleducation OWNER TO postgres;

--
-- Name: officialreport; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.officialreport (
    officialreportid integer NOT NULL,
    officialreporttype character varying(1),
    description character varying(100),
    officialreportdate timestamp without time zone,
    inputdate timestamp without time zone,
    productid integer
);


ALTER TABLE school.officialreport OWNER TO postgres;

--
-- Name: officialreportofdamage; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.officialreportofdamage (
    officialreportid integer NOT NULL,
    damage character varying(40)
);


ALTER TABLE school.officialreportofdamage OWNER TO postgres;

--
-- Name: officialreportofreplacement; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.officialreportofreplacement (
    officialreportid integer NOT NULL,
    replacement character varying(40)
);


ALTER TABLE school.officialreportofreplacement OWNER TO postgres;

--
-- Name: offwork; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.offwork (
    offworkid integer NOT NULL,
    applicationdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    offworkbegin timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    offworkend timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    intervalday integer,
    applicationstatus character varying(1) DEFAULT NULL::character varying,
    offworkstatus character varying(1) DEFAULT NULL::character varying,
    userinput character varying(20) DEFAULT NULL::character varying,
    dateinput timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminalinput character varying(15) DEFAULT NULL::character varying,
    userapprover character varying(20) DEFAULT NULL::character varying,
    dateapprover timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminalapprover character varying(15) DEFAULT NULL::character varying,
    userproceed character varying(20) DEFAULT NULL::character varying,
    dateproceed timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminalproceed character varying(15) DEFAULT NULL::character varying,
    employeeid character varying(20) DEFAULT NULL::character varying,
    comebackworkdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    offworktype character varying(1) DEFAULT NULL::character varying,
    offworkaddress character varying(200) DEFAULT NULL::character varying
);


ALTER TABLE school.offwork OWNER TO postgres;

--
-- Name: offworkmaternity; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.offworkmaternity (
    offworkid integer NOT NULL,
    maternitytype character varying(1) DEFAULT NULL::character varying,
    children integer,
    maternityestimatedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school.offworkmaternity OWNER TO postgres;

--
-- Name: offworkpermit; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.offworkpermit (
    offworkid integer NOT NULL,
    permitdescription integer,
    description character varying(100) DEFAULT NULL::character varying
);


ALTER TABLE school.offworkpermit OWNER TO postgres;

--
-- Name: offworkplafond; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.offworkplafond (
    employeeid character varying(20) DEFAULT NULL::character varying NOT NULL,
    previousyearplafond integer,
    currentyearplafond integer,
    cutibesarbegin timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    currentyear character varying(4) DEFAULT NULL::character varying,
    iscurrentallowancetaken character varying(1) DEFAULT NULL::character varying,
    ispreviousallowancetaken character varying(1) DEFAULT NULL::character varying,
    empid character varying(20) DEFAULT NULL::character varying,
    iscutibesar character varying(1) DEFAULT NULL::character varying,
    allowance character varying(20) DEFAULT NULL::character varying,
    currentallowancedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    previousallowancedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school.offworkplafond OWNER TO postgres;

--
-- Name: offworkregular; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.offworkregular (
    offworkid integer NOT NULL,
    isallowancetaken character varying(1) DEFAULT NULL::character varying,
    offworkyear character varying(4) DEFAULT NULL::character varying,
    note character varying(200) DEFAULT NULL::character varying
);


ALTER TABLE school.offworkregular OWNER TO postgres;

--
-- Name: organizationexperience; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.organizationexperience (
    organizationexperienceid integer NOT NULL,
    individuid integer,
    orgyear character varying(4) DEFAULT NULL::character varying,
    orginstitution character varying(100) DEFAULT NULL::character varying,
    orgposition character varying(100) DEFAULT NULL::character varying,
    orgjobdesk character varying(200) DEFAULT NULL::character varying
);


ALTER TABLE school.organizationexperience OWNER TO postgres;

--
-- Name: paemployee; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.paemployee (
    performanceappraisalid integer NOT NULL,
    workunit character varying(20),
    "position" character varying(20),
    employeeid character varying(20),
    positioneffectivedate timestamp without time zone,
    rankeffectivedate timestamp without time zone,
    rank integer,
    lastsalary double precision,
    evaluatoremployee character varying(20),
    appraisalannotation character varying(500),
    totalvaluepersonal double precision,
    totalvaluesupervisi double precision,
    totalvaluepartner double precision
);


ALTER TABLE school.paemployee OWNER TO postgres;

--
-- Name: parameterglobal; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.parameterglobal (
    kode_parameter character varying(10) NOT NULL,
    tipe_parameter character varying(3),
    nilai_parameter double precision,
    deskripsi character varying(100),
    is_parameter_system character varying(1),
    nilai_parameter_tanggal timestamp(6) without time zone,
    nilai_parameter_string character varying(30),
    tag character varying(15),
    default_code character varying(30)
);


ALTER TABLE school.parameterglobal OWNER TO postgres;

--
-- Name: paschool; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.paschool (
    performanceappraisalid integer NOT NULL,
    productid integer,
    conclusion character varying(500),
    suggestion character varying(500)
);


ALTER TABLE school.paschool OWNER TO postgres;

--
-- Name: performanceappraisal; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.performanceappraisal (
    performanceappraisalid integer NOT NULL,
    appraisaldate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    totalvalue double precision,
    inputuser character varying(20) DEFAULT NULL::character varying,
    inputterminal character varying(15) DEFAULT NULL::character varying,
    inputdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    generalvaluescale character varying(2) DEFAULT NULL::character varying,
    filelegalpa character varying(200) DEFAULT NULL::character varying,
    schoolyearcode character varying(5),
    pptemplateid integer,
    patype character varying(1)
);


ALTER TABLE school.performanceappraisal OWNER TO postgres;

--
-- Name: performanceitem; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.performanceitem (
    performanceitemid integer NOT NULL,
    parentid integer,
    value double precision,
    subtotal double precision,
    performancevaluescale character varying(2) DEFAULT NULL::character varying,
    performanceappraisalid integer,
    parameterid integer,
    itemcode character varying(20),
    valuepersonal double precision,
    valuesupervisi double precision,
    valuepartner double precision,
    subtotalpersonal double precision,
    subtotalsupervisi double precision,
    subtotalpartner double precision
);


ALTER TABLE school.performanceitem OWNER TO postgres;

--
-- Name: performanceparameter; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.performanceparameter (
    parametername character varying(100) DEFAULT NULL::character varying NOT NULL,
    description character varying(500) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    level integer,
    isdetaillevel character varying(1) DEFAULT NULL::character varying,
    parameterid integer NOT NULL,
    parametercode character varying(40) NOT NULL,
    parentid integer,
    pptype character varying(1)
);


ALTER TABLE school.performanceparameter OWNER TO postgres;

--
-- Name: position; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school."position" (
    positionid character varying(50) DEFAULT NULL::character varying NOT NULL,
    description character varying(200) DEFAULT NULL::character varying,
    jobdescription character varying(500) DEFAULT NULL::character varying,
    status character varying(1) DEFAULT NULL::character varying,
    nonactivedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school."position" OWNER TO postgres;

--
-- Name: pptemplate; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.pptemplate (
    pptemplateid integer NOT NULL,
    pptemplatename character varying(100),
    description character varying(200),
    pptemplatecode character varying(20),
    pptype character varying(1)
);


ALTER TABLE school.pptemplate OWNER TO postgres;

--
-- Name: pptemplateitem; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.pptemplateitem (
    pptemplateid integer NOT NULL,
    description character varying(200),
    parameterid integer NOT NULL,
    ppitemcode character varying(20)
);


ALTER TABLE school.pptemplateitem OWNER TO postgres;

--
-- Name: product; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.product (
    productid integer NOT NULL,
    productname character varying(30),
    description character varying(100),
    accountofcollection character varying(20),
    accountofdistribution character varying(20),
    percentageofamilfunds double precision,
    producttype character varying(1),
    status character varying(1),
    closeddate timestamp(6) without time zone,
    fundcategory character varying(1),
    fixedvalue character varying(1),
    fixedvalueamount double precision,
    parentproductid integer,
    isdetail character varying(1),
    level integer,
    productcode character varying(20),
    multipackage character varying(1),
    nishab double precision,
    haul integer,
    rate double precision,
    productgroupname character varying(50),
    isquotafull character varying(1),
    mustahiqquota integer,
    currentquotaposition integer
);


ALTER TABLE school.product OWNER TO postgres;

--
-- Name: productgroup; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.productgroup (
    productgroupname character varying(50) NOT NULL,
    description character varying(200)
);


ALTER TABLE school.productgroup OWNER TO postgres;

--
-- Name: program; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.program (
    productid integer NOT NULL,
    programaddress character varying(100),
    programphonenumber character varying(20)
);


ALTER TABLE school.program OWNER TO postgres;

--
-- Name: propinsi; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.propinsi (
    idpropinsi integer NOT NULL,
    idnegara integer,
    propinsi character varying(60),
    kodepropinsi character varying(3)
);


ALTER TABLE school.propinsi OWNER TO postgres;

--
-- Name: rankhistory; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.rankhistory (
    rankhistoryid integer NOT NULL,
    employeeid character varying(20) DEFAULT NULL::character varying,
    rank integer,
    rankeffectivedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school.rankhistory OWNER TO postgres;

--
-- Name: reimbursementrealization; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.reimbursementrealization (
    reimbursementrealizationid integer NOT NULL,
    reimbursementdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    realizationvalue double precision,
    nominal double precision,
    finalbalance double precision,
    employeeid character varying(20) DEFAULT NULL::character varying,
    beginbalance double precision,
    isauthorized character varying(1),
    islast character varying(1)
);


ALTER TABLE school.reimbursementrealization OWNER TO postgres;

--
-- Name: salaryhistory; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.salaryhistory (
    salaryhistoryid integer NOT NULL,
    salaryreceiveddate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    workunit character varying(50) DEFAULT NULL::character varying,
    "position" character varying(50) DEFAULT NULL::character varying,
    description character varying(200) DEFAULT NULL::character varying,
    salaryvalue double precision,
    employeeid character varying(20) DEFAULT NULL::character varying,
    salaryschemeid integer,
    monthperiod integer,
    yearperiod character varying(4) DEFAULT NULL::character varying
);


ALTER TABLE school.salaryhistory OWNER TO postgres;

--
-- Name: salaryitemhistory; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.salaryitemhistory (
    salaryitemid integer NOT NULL,
    salaryitemvalue double precision,
    salaryhistoryid integer,
    salaryitemschemeid integer,
    description character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE school.salaryitemhistory OWNER TO postgres;

--
-- Name: salaryitemparameter; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.salaryitemparameter (
    salaryitemparameterid integer NOT NULL,
    parametername character varying(100) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    description character varying(200) DEFAULT NULL::character varying,
    itemvaluedefault double precision,
    formuladefault character varying(100) DEFAULT NULL::character varying,
    salaryitemperiod character varying(1) DEFAULT NULL::character varying,
    salaryitemtypedefault character varying(1) DEFAULT NULL::character varying,
    parametergroupid character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE school.salaryitemparameter OWNER TO postgres;

--
-- Name: salaryitemparametergroup; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.salaryitemparametergroup (
    parametergroupid character varying(20) DEFAULT NULL::character varying NOT NULL,
    description character varying(200) DEFAULT NULL::character varying
);


ALTER TABLE school.salaryitemparametergroup OWNER TO postgres;

--
-- Name: salaryitemscheme; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.salaryitemscheme (
    salaryitemschemeid integer NOT NULL,
    salaryitemschemename character varying(50) DEFAULT NULL::character varying,
    description character varying(200) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    itemvalue double precision,
    formula character varying(100) DEFAULT NULL::character varying,
    salaryitemtype character varying(1) DEFAULT NULL::character varying,
    salaryschemeid integer
);


ALTER TABLE school.salaryitemscheme OWNER TO postgres;

--
-- Name: salaryscheme; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.salaryscheme (
    salaryschemeid integer NOT NULL,
    salaryschemename character varying(50) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    positionid character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE school.salaryscheme OWNER TO postgres;

--
-- Name: schoolyear; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.schoolyear (
    schoolyearcode character varying(5) NOT NULL,
    schoolyear character varying(30)
);


ALTER TABLE school.schoolyear OWNER TO postgres;

--
-- Name: seq_transactionnumber; Type: SEQUENCE; Schema: school; Owner: postgres
--

CREATE SEQUENCE school.seq_transactionnumber
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE school.seq_transactionnumber OWNER TO postgres;

--
-- Name: sessionblob; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.sessionblob (
    id integer NOT NULL,
    sessionid character varying(100),
    sessioncontext integer,
    id1 integer
);


ALTER TABLE school.sessionblob OWNER TO postgres;

--
-- Name: sourcefound; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.sourcefound (
    sourcefoundid integer NOT NULL,
    sourcefoundname character varying(50),
    description character varying(200)
);


ALTER TABLE school.sourcefound OWNER TO postgres;

--
-- Name: stockopname; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.stockopname (
    stockopnameid integer NOT NULL,
    stockopnamedate timestamp without time zone,
    description character varying(500),
    inputdate timestamp without time zone,
    productid integer
);


ALTER TABLE school.stockopname OWNER TO postgres;

--
-- Name: stockopnameequipment; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.stockopnameequipment (
    stockopnameid integer NOT NULL,
    equipmentid integer NOT NULL,
    quantity integer,
    unit character varying(50),
    equipmentname character varying(100),
    lokasi character varying(200)
);


ALTER TABLE school.stockopnameequipment OWNER TO postgres;

--
-- Name: stockopnametools; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.stockopnametools (
    stockopnameid integer NOT NULL,
    toolsid integer NOT NULL,
    toolsname character varying(100),
    goodcondition integer,
    brokencondition integer,
    replaced integer,
    unit character varying(50),
    lokasi character varying(200)
);


ALTER TABLE school.stockopnametools OWNER TO postgres;

--
-- Name: student; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.student (
    productid integer NOT NULL,
    mustahiqid integer NOT NULL,
    action character varying(200),
    complaint character varying(150),
    reference character varying(150),
    studentclasscode character varying(100),
    classhistoryid integer,
    nonactivedate timestamp without time zone,
    nonactivedescription character varying(100)
);


ALTER TABLE school.student OWNER TO postgres;

--
-- Name: studentclass; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.studentclass (
    studentclasscode character varying(100) NOT NULL,
    description character varying(100),
    productid integer
);


ALTER TABLE school.studentclass OWNER TO postgres;

--
-- Name: studenthealth; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.studenthealth (
    studenthealthid integer NOT NULL,
    productid integer NOT NULL,
    mustahiqid integer NOT NULL,
    action character varying(100),
    complaint character varying(100),
    reference character varying(100),
    datehealth timestamp without time zone
);


ALTER TABLE school.studenthealth OWNER TO postgres;

--
-- Name: subject; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.subject (
    subjectid integer NOT NULL,
    subjectname character varying(30),
    subjectcode character varying(5)
);


ALTER TABLE school.subject OWNER TO postgres;

--
-- Name: targetachievement; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.targetachievement (
    targetachievementid integer NOT NULL,
    evaluatoremployee character varying(20) DEFAULT NULL::character varying,
    inputdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    inputterminal character varying(15) DEFAULT NULL::character varying,
    inputuser character varying(20) DEFAULT NULL::character varying,
    targetfile character varying(200) DEFAULT NULL::character varying,
    achievementfile character varying(200) DEFAULT NULL::character varying,
    targetdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    lastsalary double precision,
    periodyear character varying(4) DEFAULT NULL::character varying,
    workunit character varying(50) DEFAULT NULL::character varying,
    positionid character varying(50) DEFAULT NULL::character varying,
    positioneffectivedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    rank integer,
    rankeffectivedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    employeeid character varying(20) DEFAULT NULL::character varying,
    achievementlegalfile character varying(200) DEFAULT NULL::character varying,
    targetlegalfile character varying(200) DEFAULT NULL::character varying,
    achievementdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    schoolyearcode character varying(5)
);


ALTER TABLE school.targetachievement OWNER TO postgres;

--
-- Name: toollist; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.toollist (
    toolsid integer,
    toollistid integer NOT NULL,
    description character varying(100),
    officialreportid integer,
    quantity integer
);


ALTER TABLE school.toollist OWNER TO postgres;

--
-- Name: tools; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.tools (
    infrastructureid integer,
    toolsid integer NOT NULL,
    toolsname character varying(40),
    parentid integer,
    quantity integer,
    description character varying(100),
    goodcondition integer,
    brokencondition integer,
    unit character varying(20),
    replacement integer
);


ALTER TABLE school.tools OWNER TO postgres;

--
-- Name: training; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.training (
    trainingid integer NOT NULL,
    individuid integer,
    materi character varying(100) DEFAULT NULL::character varying,
    institution character varying(100) DEFAULT NULL::character varying,
    trainingtype character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE school.training OWNER TO postgres;

--
-- Name: trainingseminar; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.trainingseminar (
    trainingid integer NOT NULL,
    status character varying(100) DEFAULT NULL::character varying,
    year character varying(4) DEFAULT NULL::character varying
);


ALTER TABLE school.trainingseminar OWNER TO postgres;

--
-- Name: workexperience; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.workexperience (
    workexperienceid integer NOT NULL,
    individuid integer,
    workyear character varying(4) DEFAULT NULL::character varying,
    workinstitution character varying(100) DEFAULT NULL::character varying,
    workposition character varying(100) DEFAULT NULL::character varying,
    workjobdesk character varying(200) DEFAULT NULL::character varying
);


ALTER TABLE school.workexperience OWNER TO postgres;

--
-- Name: workunit; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.workunit (
    workunitid character varying(50) DEFAULT NULL::character varying NOT NULL,
    description character varying(200) DEFAULT NULL::character varying,
    parentid character varying(50) DEFAULT NULL::character varying,
    status character varying(1) DEFAULT NULL::character varying,
    nonactivedate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE school.workunit OWNER TO postgres;

--
-- Name: workunitposition; Type: TABLE; Schema: school; Owner: postgres
--

CREATE TABLE school.workunitposition (
    workunitid character varying(50) DEFAULT NULL::character varying NOT NULL,
    positionid character varying(50) DEFAULT NULL::character varying NOT NULL,
    jobdeskfile character varying(100) DEFAULT NULL::character varying
);


ALTER TABLE school.workunitposition OWNER TO postgres;

--
-- Name: account; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.account (
    account_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    account_name character varying(100) DEFAULT NULL::character varying,
    account_level integer,
    is_detail character varying(1) DEFAULT NULL::character varying,
    account_type character varying(1) DEFAULT NULL::character varying,
    is_system character varying(1) DEFAULT NULL::character varying,
    userid_last_modified character varying(20) DEFAULT NULL::character varying,
    time_last_modified timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    fl_parent_account character varying(20) DEFAULT NULL::character varying,
    userid_create character varying(20) DEFAULT NULL::character varying,
    time_create timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    balance double precision,
    fl_cpa_accountcode character varying(20) DEFAULT NULL::character varying,
    fl_lpa_accountcode character varying(20) DEFAULT NULL::character varying,
    isactivaoffbalancesheet character varying(1) DEFAULT NULL::character varying,
    isrpvrakreportshow character varying(1) DEFAULT NULL::character varying,
    isrpvaccount character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE transaction.account OWNER TO postgres;

--
-- Name: account_off_bs; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.account_off_bs AS
 SELECT account_code,
    account_name,
    account_level,
    is_detail,
    account_type,
    is_system,
    userid_last_modified,
    time_last_modified,
    fl_parent_account,
    userid_create,
    time_create,
    balance,
    fl_cpa_accountcode,
    fl_lpa_accountcode,
    isactivaoffbalancesheet,
    isrpvrakreportshow,
    isrpvaccount
   FROM transaction.account
  WHERE ((account_type)::text = 'M'::text);


ALTER VIEW transaction.account_off_bs OWNER TO postgres;

--
-- Name: accountdetail; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountdetail (
    fl_account character varying(20) DEFAULT NULL::character varying NOT NULL,
    fl_detail_account character varying(20) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE transaction.accountdetail OWNER TO postgres;

--
-- Name: accountgroup; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountgroup (
    accountgroup_code character varying(5) DEFAULT NULL::character varying,
    accountgroup_name character varying(30) DEFAULT NULL::character varying,
    id integer NOT NULL
);


ALTER TABLE transaction.accountgroup OWNER TO postgres;

--
-- Name: accounthierarchy; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accounthierarchy (
    accounthierarchy_id integer NOT NULL,
    fl_parentaccountcode character varying(20) DEFAULT NULL::character varying,
    fl_childaccountcode character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.accounthierarchy OWNER TO postgres;

--
-- Name: accountingday; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountingday (
    description character varying(100) DEFAULT NULL::character varying,
    periode_status character varying(1) DEFAULT NULL::character varying,
    islastperiod character varying(1) DEFAULT NULL::character varying,
    periode_code integer NOT NULL,
    fl_accountingperiode integer NOT NULL,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying NOT NULL,
    datevalue timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    isworkday character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE transaction.accountingday OWNER TO postgres;

--
-- Name: accountingperiode; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountingperiode (
    fl_accountingyear character varying(4) DEFAULT NULL::character varying NOT NULL,
    periode_code integer NOT NULL,
    description character varying(100) DEFAULT NULL::character varying,
    periode_status character varying(1) DEFAULT NULL::character varying,
    is_lastyearperiode character varying(1) DEFAULT NULL::character varying,
    pcode_accday_end integer,
    pcode_accday_start integer,
    fl_accountingperiode_start integer,
    fl_accountingyear_start character varying(4) DEFAULT NULL::character varying
);


ALTER TABLE transaction.accountingperiode OWNER TO postgres;

--
-- Name: accountingyear; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountingyear (
    periode_code character varying(4) DEFAULT NULL::character varying NOT NULL,
    description character varying(100) DEFAULT NULL::character varying,
    periode_status character varying(1) DEFAULT NULL::character varying,
    fl_current_periode integer,
    pcode_accper_end integer,
    pcode_accper_start integer,
    fl_accountingyear_start character varying(4) DEFAULT NULL::character varying
);


ALTER TABLE transaction.accountingyear OWNER TO postgres;

--
-- Name: accountinstance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountinstance (
    accountinstance_id integer NOT NULL,
    balance numeric(36,10),
    fl_cpa_accountinstance integer,
    fl_lpa_accountinstance integer,
    balance_ekuiv numeric(36,10),
    balance_ratarata numeric(36,10),
    balance_ratarata_ekuiv numeric(36,10),
    trial_balance numeric(36,10),
    trial_balance_ekuiv numeric(36,10),
    balance_harilalu numeric(36,10),
    balance_harilalu_ekuiv numeric(36,10),
    isbolehinput character varying(1) DEFAULT NULL::character varying,
    branch_code character varying(5) DEFAULT NULL::character varying,
    account_code character varying(20) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying,
    dailybalance_id integer,
    periodebalance_id integer,
    dailyprojectbalance_id integer,
    periodeprojectbalance_id integer,
    balance_sign numeric(1,0)
);


ALTER TABLE transaction.accountinstance OWNER TO postgres;

--
-- Name: accountinstance_neraca; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.accountinstance_neraca AS
 SELECT ai.accountinstance_id,
    ai.account_code,
    ai.branch_code,
    ai.currency_code,
    a.account_name,
    a.account_type,
    a.account_level,
    a.is_detail,
    a.fl_parent_account
   FROM transaction.accountinstance ai,
    transaction.account a
  WHERE (((ai.account_code)::text = (a.account_code)::text) AND ((a.account_type)::text = ANY (ARRAY[('A'::character varying)::text, ('L'::character varying)::text, ('E'::character varying)::text])));


ALTER VIEW transaction.accountinstance_neraca OWNER TO postgres;

--
-- Name: accountinterface; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountinterface (
    interface_code character varying(10) DEFAULT NULL::character varying NOT NULL,
    account_code character varying(20) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    interface_type character varying(1) DEFAULT NULL::character varying,
    is_active character varying(1) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.accountinterface OWNER TO postgres;

--
-- Name: accountinterfacemember; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountinterfacemember (
    member_id integer NOT NULL,
    interface_code character varying(10) DEFAULT NULL::character varying,
    account_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.accountinterfacemember OWNER TO postgres;

--
-- Name: accountmanager; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountmanager (
    amcode character varying(10) DEFAULT NULL::character varying NOT NULL,
    rcno character varying(4) DEFAULT NULL::character varying,
    employeeid character varying(20) DEFAULT NULL::character varying,
    employeename character varying(50) DEFAULT NULL::character varying,
    project_no character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE transaction.accountmanager OWNER TO postgres;

--
-- Name: accountreceivable; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accountreceivable (
    accountno character varying(30) DEFAULT NULL::character varying NOT NULL,
    accountreceivabletype character varying(1) DEFAULT NULL::character varying,
    employeeid character varying(20) DEFAULT NULL::character varying,
    employeeidnumber integer,
    externaldebtorid integer,
    debtorid integer,
    partnerid integer
);


ALTER TABLE transaction.accountreceivable OWNER TO postgres;

--
-- Name: accreceivabletransactitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accreceivabletransactitem (
    transactionitemid integer NOT NULL,
    artransactitemtype character varying(1),
    investmenttitype character varying(1),
    principalamount numeric(38,2),
    shareamount numeric(38,2)
);


ALTER TABLE transaction.accreceivabletransactitem OWNER TO postgres;

--
-- Name: accsubsystem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.accsubsystem (
    subsystemcode character varying(20) DEFAULT NULL::character varying NOT NULL,
    titlesubsystem character varying(50) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    servername character varying(30) DEFAULT NULL::character varying,
    username character varying(20) DEFAULT NULL::character varying,
    password character varying(30) DEFAULT NULL::character varying,
    createjournalscriptid character varying(100) DEFAULT NULL::character varying,
    sessionname character varying(30) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    usecurrentlogin character varying(1) DEFAULT NULL::character varying,
    authjournalscriptid character varying(80) DEFAULT NULL::character varying,
    applicationid character varying(80) DEFAULT NULL::character varying,
    oldstylescripting integer
);


ALTER TABLE transaction.accsubsystem OWNER TO postgres;

--
-- Name: amortizedcost; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.amortizedcost (
    accountno character varying(30) NOT NULL,
    amortizedcosttype character varying(1),
    description character varying(150),
    costaccountno character varying(30)
);


ALTER TABLE transaction.amortizedcost OWNER TO postgres;

--
-- Name: assetcategory; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.assetcategory (
    assetcategoryid integer NOT NULL,
    parentassetcategoryid integer,
    assetcategoryname character varying(50),
    assetcategorycode character varying(20),
    thresholdvalue double precision,
    defaultlifetime integer,
    inputer character varying(50),
    inputdate timestamp(6) without time zone,
    inputtime timestamp(6) without time zone,
    glicontainerid integer,
    isdepreciable character varying(1),
    assettype character varying(1)
);


ALTER TABLE transaction.assetcategory OWNER TO postgres;

--
-- Name: balancesumgroup; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.balancesumgroup (
    groupcode character varying(10) NOT NULL,
    groupname character varying(100),
    groupdescription character varying(200)
);


ALTER TABLE transaction.balancesumgroup OWNER TO postgres;

--
-- Name: balancesumitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.balancesumitem (
    itemid integer NOT NULL,
    itemcode character varying(30),
    itemname character varying(100),
    groupcode character varying(10)
);


ALTER TABLE transaction.balancesumitem OWNER TO postgres;

--
-- Name: balancesumitemmember; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.balancesumitemmember (
    memberid integer NOT NULL,
    itemid integer,
    account_code character varying(20)
);


ALTER TABLE transaction.balancesumitemmember OWNER TO postgres;

--
-- Name: balancesumitemtrancode; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.balancesumitemtrancode (
    memberid integer NOT NULL,
    itemid integer,
    transactioncode character varying(10)
);


ALTER TABLE transaction.balancesumitemtrancode OWNER TO postgres;

--
-- Name: bank; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.bank (
    bankcode character varying(10) DEFAULT NULL::character varying NOT NULL,
    bankshortname character varying(20) DEFAULT NULL::character varying,
    bankname character varying(60) DEFAULT NULL::character varying
);


ALTER TABLE transaction.bank OWNER TO postgres;

--
-- Name: bankaccountlist; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.bankaccountlist (
    bankaccountid integer NOT NULL,
    bankaccountname character varying(200),
    bankaccountno character varying(20),
    bankaccountlisttype character varying(1),
    bankcode character varying(10),
    isdefault character varying(1)
);


ALTER TABLE transaction.bankaccountlist OWNER TO postgres;

--
-- Name: batchupload; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.batchupload (
    batchid integer NOT NULL,
    accountno character varying(30),
    transactionid integer,
    uploaduser character varying(50),
    uploaddate timestamp(6) without time zone,
    totalamount numeric(30,6),
    batchuploadtype character varying(1),
    branchcode character varying(10),
    authorizeduser character varying(50),
    description character varying(200),
    totalrecord integer,
    filename character varying(400)
);


ALTER TABLE transaction.batchupload OWNER TO postgres;

--
-- Name: batchuploaditem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.batchuploaditem (
    batchitemid integer NOT NULL,
    batchid integer,
    transactionid integer,
    transactionno character varying(30),
    amount numeric(30,6),
    transactiondate timestamp(6) without time zone,
    description character varying(200),
    authstatus character varying(1),
    authaction character varying(1),
    validationstatus character varying(1),
    donorid integer,
    productid integer,
    referenceno character varying(30),
    donornamefromdesc character varying(200),
    iscreatenewdonor character varying(1),
    bankaccountno character varying(30),
    accountno character varying(30),
    amountzakatprofesi numeric(30,6),
    amountzakatmaal numeric(30,6),
    amountzakatfitrah numeric(30,6),
    amountinfaq numeric(30,6),
    amountdpu numeric(30,6),
    amountanakyatim numeric(30,6),
    amountanakasuh numeric(30,6),
    amounttitipanwakaf numeric(30,6),
    amountqurban numeric(30,6),
    amountnonhalal numeric(30,6),
    amountfidyah numeric(30,6)
);


ALTER TABLE transaction.batchuploaditem OWNER TO postgres;

--
-- Name: blobregistration; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.blobregistration (
    id integer NOT NULL,
    actualfilename character varying(128) DEFAULT NULL::character varying,
    istemporary character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE transaction.blobregistration OWNER TO postgres;

--
-- Name: bpscenario; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.bpscenario (
    bpscenarioid integer NOT NULL,
    bpscenariocode character varying(10),
    bpscenarioname character varying(50)
);


ALTER TABLE transaction.bpscenario OWNER TO postgres;

--
-- Name: bpscenariostep; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.bpscenariostep (
    bpstepid integer NOT NULL,
    bpstepsequence integer,
    bpscriptid integer,
    bpscenarioid integer,
    isenabled character varying(1)
);


ALTER TABLE transaction.bpscenariostep OWNER TO postgres;

--
-- Name: bpscript; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.bpscript (
    bpscriptid integer NOT NULL,
    bpscriptdescription character varying(250),
    bpscriptname character varying(250),
    bpscriptpath character varying(250)
);


ALTER TABLE transaction.bpscript OWNER TO postgres;

--
-- Name: branchlocation; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.branchlocation AS
 SELECT kode_cabang AS branch_code,
    nama_cabang AS branchname,
    'A'::text AS "?column?",
    ' '::text AS user_id,
    tanggal_input AS last_update,
    kode_cabang_induk AS masterbranch_code
   FROM enterprise.cabang;


ALTER VIEW transaction.branchlocation OWNER TO postgres;

--
-- Name: branchlocation_old; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.branchlocation_old (
    branch_code character varying(5) DEFAULT NULL::character varying NOT NULL,
    branchname character varying(50) DEFAULT NULL::character varying,
    branchstatus character varying(1) DEFAULT NULL::character varying,
    user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    masterbranch_code character varying(5) DEFAULT NULL::character varying,
    dataid integer
);


ALTER TABLE transaction.branchlocation_old OWNER TO postgres;

--
-- Name: branchlocation_oldtran; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.branchlocation_oldtran AS
 SELECT kode_cabang AS branch_code,
    nama_cabang AS branchname,
        CASE
            WHEN (((tipe_cabang)::text = 'CU'::text) OR ((tipe_cabang)::text = 'PO'::text)) THEN 'B'::text
            ELSE 'S'::text
        END AS branchstatus,
    user_input AS user_id,
    tanggal_input AS last_update,
    kode_cabang_induk AS masterbranch_code,
    0 AS dataid
   FROM enterprise.cabang;


ALTER VIEW transaction.branchlocation_oldtran OWNER TO postgres;

--
-- Name: branchparameter; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.branchparameter (
    branchcode character varying(5) NOT NULL,
    inputer character varying(100),
    printertype character varying(1),
    voucherformat character varying(1)
);


ALTER TABLE transaction.branchparameter OWNER TO postgres;

--
-- Name: bsz; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.bsz (
    bszid integer NOT NULL,
    bsznumber character varying(30),
    donorid integer,
    bszdate timestamp(6) without time zone
);


ALTER TABLE transaction.bsz OWNER TO postgres;

--
-- Name: bszdetail; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.bszdetail (
    bszdetailid integer NOT NULL,
    bszid integer,
    item integer,
    percentage double precision,
    year integer,
    basicvalue double precision,
    zakahvalue double precision
);


ALTER TABLE transaction.bszdetail OWNER TO postgres;

--
-- Name: bsztransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.bsztransaction (
    bszid integer,
    transactionitemid integer NOT NULL,
    bsztransactionid integer NOT NULL
);


ALTER TABLE transaction.bsztransaction OWNER TO postgres;

--
-- Name: budgetitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.budgetitem (
    budgetitemcode character varying(20),
    budgetitemdescription character varying(250),
    ownerid integer,
    parentbudgetitemcode character varying(20),
    level integer,
    is_detail character varying(1) DEFAULT NULL::character varying,
    itemid integer NOT NULL,
    budgetitemname character varying(200) NOT NULL,
    parentitemid integer,
    branchcode character varying(5)
);


ALTER TABLE transaction.budgetitem OWNER TO postgres;

--
-- Name: budgetitemhierarchy; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.budgetitemhierarchy (
    hierarchyid integer NOT NULL,
    level integer,
    parentitemid integer,
    childitemid integer
);


ALTER TABLE transaction.budgetitemhierarchy OWNER TO postgres;

--
-- Name: budgetownerhierarchy; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.budgetownerhierarchy (
    hierarchyid integer NOT NULL,
    parentownerid integer,
    childownerid integer,
    level integer
);


ALTER TABLE transaction.budgetownerhierarchy OWNER TO postgres;

--
-- Name: budgetrevision; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.budgetrevision (
    revisionid integer NOT NULL,
    budgetid integer,
    amount double precision,
    userid character varying(20)
);


ALTER TABLE transaction.budgetrevision OWNER TO postgres;

--
-- Name: cashaccountall; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.cashaccountall AS
 SELECT a.accountno,
    a.accountname,
    a.branchcode,
    a.currencycode,
    a.balance,
    b.bankaccountno,
    a.status,
    b.bankcode,
    b.bankname,
    b.cashaccounttype
   FROM transaction.financialaccount a,
    transaction.cashaccount b
  WHERE ((a.accountno)::text = (b.accountno)::text);


ALTER VIEW transaction.cashaccountall OWNER TO postgres;

--
-- Name: cashadvancememoinfo; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cashadvancememoinfo (
    transactionid integer NOT NULL,
    transactionitemid integer,
    realmemoid integer
);


ALTER TABLE transaction.cashadvancememoinfo OWNER TO postgres;

--
-- Name: cashadvanceprograminfo; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cashadvanceprograminfo (
    sourcetransactionid integer NOT NULL,
    reporttransactionid integer NOT NULL,
    branchcode character varying(10)
);


ALTER TABLE transaction.cashadvanceprograminfo OWNER TO postgres;

--
-- Name: cashadvancereturninfo; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cashadvancereturninfo (
    sourcetransactionid integer NOT NULL,
    returntransactionid integer,
    branchcode character varying(5),
    returnamount numeric(20,8),
    reimburseamount numeric(20,8)
);


ALTER TABLE transaction.cashadvancereturninfo OWNER TO postgres;

--
-- Name: cashflowgroup; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cashflowgroup (
    cfgroupid integer NOT NULL,
    cfgroupcode character varying(10),
    cfgroupname character varying(100),
    cfgroupdescription character varying(200),
    cfsequencenumber integer,
    cfparentid integer,
    cfgrouplevel integer,
    isdetail character varying(1),
    cfoperationtype character varying(1)
);


ALTER TABLE transaction.cashflowgroup OWNER TO postgres;

--
-- Name: cashflowmember; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cashflowmember (
    cfmemberid integer NOT NULL,
    cfgroupid integer,
    account_code character varying(20),
    mutationtype character varying(1),
    trancodeexclude character varying(200),
    trancodeinclude character varying(200),
    journalcodeexclude character varying(200),
    journalcodeinclude character varying(200),
    additionalinfo character varying(300)
);


ALTER TABLE transaction.cashflowmember OWNER TO postgres;

--
-- Name: coa_convertion; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.coa_convertion (
    accountcode_old character varying(20) NOT NULL,
    accountcode_new character varying(20)
);


ALTER TABLE transaction.coa_convertion OWNER TO postgres;

--
-- Name: corporatedonor; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.corporatedonor (
    corporation character varying(1) DEFAULT NULL::character varying,
    siupp character varying(20) DEFAULT NULL::character varying,
    tdp character varying(20) DEFAULT NULL::character varying,
    locationtype character varying(30) DEFAULT NULL::character varying,
    ownertype character varying(30) DEFAULT NULL::character varying,
    establisheddate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    establishedplace character varying(50) DEFAULT NULL::character varying,
    contactperson character varying(50) DEFAULT NULL::character varying,
    patronagecompany character varying(1) DEFAULT NULL::character varying,
    donorid integer NOT NULL,
    cpname character varying(150),
    cpemail character varying(200),
    cpphonenumber character varying(30),
    cpmobilenumber character varying(30)
);


ALTER TABLE transaction.corporatedonor OWNER TO postgres;

--
-- Name: costpaidinadvance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.costpaidinadvance (
    accountno character varying(30) NOT NULL,
    hascontract character varying(1),
    contractbegindate timestamp(6) without time zone,
    contractduration integer,
    contractenddate timestamp(6) without time zone,
    contractno character varying(50)
);


ALTER TABLE transaction.costpaidinadvance OWNER TO postgres;

--
-- Name: cpalpamapping; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cpalpamapping (
    fl_lpa_accountcode character varying(20) DEFAULT NULL::character varying,
    fl_cpa_accountcode character varying(20) DEFAULT NULL::character varying,
    cpalpamapping_id integer NOT NULL
);


ALTER TABLE transaction.cpalpamapping OWNER TO postgres;

--
-- Name: currency; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.currency (
    currency_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    description character varying(64) DEFAULT NULL::character varying,
    currentvalue double precision,
    isdefault character varying(1) DEFAULT NULL::character varying,
    isstandard character varying(1) DEFAULT NULL::character varying,
    centralbank_currency_code character varying(20) DEFAULT NULL::character varying,
    short_name character varying(10) DEFAULT NULL::character varying,
    full_name character varying(50) DEFAULT NULL::character varying,
    country_owner character varying(30) DEFAULT NULL::character varying,
    kurs_buku double precision,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_tengah_bi double precision,
    kurs_beli_kantor_pusat double precision,
    kurs_jual_kantor_pusat double precision,
    tanggal_limit timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_otorisasi character varying(20) DEFAULT NULL::character varying,
    tanggal_otorisasi timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_otorisasi character varying(15) DEFAULT NULL::character varying,
    kurs_neraca double precision,
    deviasi_maksimal double precision,
    kurs_reval double precision,
    kurs_remittance double precision,
    symbol character varying(10),
    symbol_says character varying(50)
);


ALTER TABLE transaction.currency OWNER TO postgres;

--
-- Name: currency_pkpu; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.currency_pkpu (
    currency_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    description character varying(64) DEFAULT NULL::character varying,
    currentvalue double precision,
    isdefault character varying(1) DEFAULT NULL::character varying,
    isstandard character varying(1) DEFAULT NULL::character varying,
    centralbank_currency_code character varying(20) DEFAULT NULL::character varying,
    short_name character varying(10) DEFAULT NULL::character varying,
    full_name character varying(50) DEFAULT NULL::character varying,
    country_owner character varying(30) DEFAULT NULL::character varying,
    kurs_buku double precision,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_tengah_bi double precision,
    kurs_beli_kantor_pusat double precision,
    kurs_jual_kantor_pusat double precision,
    tanggal_limit timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_input character varying(20) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_otorisasi character varying(20) DEFAULT NULL::character varying,
    tanggal_otorisasi timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    terminal_otorisasi character varying(15) DEFAULT NULL::character varying,
    kurs_neraca double precision,
    deviasi_maksimal double precision,
    kurs_reval double precision,
    kurs_remittance double precision,
    symbol character varying(10),
    symbol_says character varying(50)
);


ALTER TABLE transaction.currency_pkpu OWNER TO postgres;

--
-- Name: custom_idgen; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.custom_idgen (
    idname character varying(30) DEFAULT NULL::character varying NOT NULL,
    idcode character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE transaction.custom_idgen OWNER TO postgres;

--
-- Name: cutoff_dba_2017; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cutoff_dba_2017 (
    accountinstance_id integer,
    max_period timestamp without time zone
);


ALTER TABLE transaction.cutoff_dba_2017 OWNER TO postgres;

--
-- Name: cutoff_dba_2021; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cutoff_dba_2021 (
    accountinstance_id integer,
    max_period timestamp without time zone
);


ALTER TABLE transaction.cutoff_dba_2021 OWNER TO postgres;

--
-- Name: cutoff_dba_detail_2017; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cutoff_dba_detail_2017 (
    dailybalance_id integer,
    balance numeric(36,10),
    balance_ekuiv numeric(36,10),
    balance_harilalu numeric(36,10),
    balance_harilalu_ekuiv numeric(36,10),
    balance_ratarata numeric(36,10),
    balance_ratarata_ekuiv numeric(36,10),
    trial_balance numeric(36,10),
    trial_balance_ekuiv numeric(36,10),
    balancecumulative numeric(36,10),
    balancecumulative_ekuiv numeric(36,10),
    datevalue date,
    debit numeric(36,10),
    credit numeric(36,10),
    debit_ekuiv numeric(36,10),
    credit_ekuiv numeric(36,10),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear integer,
    accountinstance_id integer
);


ALTER TABLE transaction.cutoff_dba_detail_2017 OWNER TO postgres;

--
-- Name: cutoff_dba_detail_2021; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cutoff_dba_detail_2021 (
    dailybalance_id integer,
    balance numeric(36,10),
    balance_ekuiv numeric(36,10),
    balance_harilalu numeric(36,10),
    balance_harilalu_ekuiv numeric(36,10),
    balance_ratarata numeric(36,10),
    balance_ratarata_ekuiv numeric(36,10),
    trial_balance numeric(36,10),
    trial_balance_ekuiv numeric(36,10),
    balancecumulative numeric(36,10),
    balancecumulative_ekuiv numeric(36,10),
    datevalue date,
    debit numeric(36,10),
    credit numeric(36,10),
    debit_ekuiv numeric(36,10),
    credit_ekuiv numeric(36,10),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear integer,
    accountinstance_id integer
);


ALTER TABLE transaction.cutoff_dba_detail_2021 OWNER TO postgres;

--
-- Name: cutoff_trxitem_sum_2017; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.cutoff_trxitem_sum_2017 (
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    mutationtype character varying(1),
    transactionitemtype character varying(1),
    amount numeric,
    count_amount bigint
);


ALTER TABLE transaction.cutoff_trxitem_sum_2017 OWNER TO postgres;

--
-- Name: daemons; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.daemons (
    "Start" text NOT NULL,
    "Info" text NOT NULL
);


ALTER TABLE transaction.daemons OWNER TO postgres;

--
-- Name: dailybalance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.dailybalance (
    dailybalance_id integer NOT NULL,
    balance numeric(36,10),
    balance_ekuiv numeric(36,10),
    balance_harilalu numeric(36,10),
    balance_harilalu_ekuiv numeric(36,10),
    balance_ratarata numeric(36,10),
    balance_ratarata_ekuiv numeric(36,10),
    trial_balance numeric(36,10),
    trial_balance_ekuiv numeric(36,10),
    balancecumulative numeric(36,10),
    balancecumulative_ekuiv numeric(36,10),
    datevalue timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    debit numeric(36,10),
    credit numeric(36,10),
    debit_ekuiv numeric(36,10),
    credit_ekuiv numeric(36,10),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying,
    accountinstance_id integer
);


ALTER TABLE transaction.dailybalance OWNER TO postgres;

--
-- Name: dailybalancecash; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.dailybalancecash (
    dailybalance_id integer NOT NULL,
    balance numeric(36,10),
    balance_ekuiv numeric(36,10),
    balance_harilalu numeric(36,10),
    balance_harilalu_ekuiv numeric(36,10),
    balance_ratarata numeric(36,10),
    balance_ratarata_ekuiv numeric(36,10),
    trial_balance numeric(36,10),
    trial_balance_ekuiv numeric(36,10),
    balancecumulative numeric(36,10),
    balancecumulative_ekuiv numeric(36,10),
    datevalue timestamp without time zone,
    debit numeric(36,10),
    credit numeric(36,10),
    debit_ekuiv numeric(36,10),
    credit_ekuiv numeric(36,10),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4),
    accountinstance_id integer
);


ALTER TABLE transaction.dailybalancecash OWNER TO postgres;

--
-- Name: dailyprojectbalance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.dailyprojectbalance (
    dailyprojectbalance_id integer NOT NULL,
    debit double precision,
    credit double precision,
    balance double precision,
    balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balancecumulative double precision,
    balancecumulative_ekuiv double precision,
    datevalue timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    debit_ekuiv double precision,
    credit_ekuiv double precision,
    project_no character varying(10) DEFAULT NULL::character varying,
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying,
    accountinstance_id integer
);


ALTER TABLE transaction.dailyprojectbalance OWNER TO postgres;

--
-- Name: externaldebtor; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.externaldebtor (
    debtorid integer NOT NULL,
    debtorname character varying(150),
    debtorcode character varying(15),
    debtoraddress character varying(200),
    branchcode character varying(5),
    description character varying(200),
    debtorphone character varying(30)
);


ALTER TABLE transaction.externaldebtor OWNER TO postgres;

--
-- Name: debtor_all; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.debtor_all AS
 SELECT i.individuid AS debtorid,
    (e.employeeid)::character varying(15) AS debtorcode,
    (i.individuname)::character varying(100) AS debtorname,
    i.branchcode,
    'E'::character varying(1) AS debtortype,
    'Karyawan'::character varying(15) AS debtortypedesc
   FROM personalia.employee e,
    personalia.individu i
  WHERE (e.individuid = i.individuid)
UNION
 SELECT e.debtorid,
    e.debtorcode,
    (e.debtorname)::character varying(100) AS debtorname,
    e.branchcode,
    'X'::character varying(1) AS debtortype,
    'Non Karyawan'::character varying(15) AS debtortypedesc
   FROM transaction.externaldebtor e;


ALTER VIEW transaction.debtor_all OWNER TO postgres;

--
-- Name: depreciableasset; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.depreciableasset (
    accountno character varying(30) NOT NULL,
    accountnoproduct character varying(30),
    depreciableassettype character varying(1),
    lifetime integer,
    nilaiawal double precision,
    nilaisisa double precision,
    penyusutanke integer,
    tanggalakhirpenyusutan timestamp(6) without time zone,
    tanggalperolehan timestamp(6) without time zone,
    tanggalprosesberikut timestamp(6) without time zone,
    tanggalprosesterakhir timestamp(6) without time zone,
    totalpenyusutan double precision,
    nominalpenyusutan double precision,
    deprstate character varying(1),
    fundcategory character varying(1)
);


ALTER TABLE transaction.depreciableasset OWNER TO postgres;

--
-- Name: dinarcertificate; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.dinarcertificate (
    dinarcertificateid integer NOT NULL,
    dinarcertificatenumber character varying(30) DEFAULT NULL::character varying,
    donorid integer,
    transactionitemid integer,
    certificatedate timestamp without time zone
);


ALTER TABLE transaction.dinarcertificate OWNER TO postgres;

--
-- Name: dinarholder; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.dinarholder (
    accountno character varying(30) NOT NULL,
    donorid integer
);


ALTER TABLE transaction.dinarholder OWNER TO postgres;

--
-- Name: distributiontransferinfo; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.distributiontransferinfo (
    distributionid integer NOT NULL,
    transactionid integer NOT NULL,
    reporttransactionid integer,
    accountno character varying(30),
    branchdestination character varying(3),
    branchsource character varying(3),
    reportstatus character varying(1),
    branchreporttransid integer,
    branchreportstatus character varying(1)
);


ALTER TABLE transaction.distributiontransferinfo OWNER TO postgres;

--
-- Name: distributiontransferinfotemp; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.distributiontransferinfotemp (
    distributionid bigint,
    transactionid integer,
    reporttransactionid integer,
    accountno character varying(30),
    branchdestination character varying(3),
    branchsource character varying(3),
    reportstatus character varying(1),
    branchreporttransid integer,
    branchreportstatus character varying(1)
);


ALTER TABLE transaction.distributiontransferinfotemp OWNER TO postgres;

--
-- Name: donorbankaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.donorbankaccount (
    bankaccountid integer NOT NULL,
    donorid integer
);


ALTER TABLE transaction.donorbankaccount OWNER TO postgres;

--
-- Name: donorcommitment; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.donorcommitment (
    commitmentid integer NOT NULL,
    commitmentamount numeric(30,2),
    accountno character varying(30),
    donorid integer
);


ALTER TABLE transaction.donorcommitment OWNER TO postgres;

--
-- Name: donortotalfund; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.donortotalfund (
    totalfundid integer NOT NULL,
    donorid integer,
    fundentity integer,
    totalamount numeric(38,2)
);


ALTER TABLE transaction.donortotalfund OWNER TO postgres;

--
-- Name: employee; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.employee AS
 SELECT e.employeeid,
    i.individuname AS employeename
   FROM personalia.employee e,
    personalia.individu i
  WHERE (e.individuid = i.individuid);


ALTER VIEW transaction.employee OWNER TO postgres;

--
-- Name: enum_int; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.enum_int (
    enum_name character varying(32) DEFAULT NULL::character varying NOT NULL,
    enum_value integer NOT NULL,
    enum_description character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE transaction.enum_int OWNER TO postgres;

--
-- Name: externaltransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.externaltransaction (
    subsystemcode character varying(20),
    transactionid integer,
    exttransactionid integer NOT NULL
);


ALTER TABLE transaction.externaltransaction OWNER TO postgres;

--
-- Name: fact_daily_balance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.fact_daily_balance (
    fact_id integer NOT NULL,
    fact_date timestamp without time zone,
    fact_date_fmt character varying(8),
    accountinstance_id integer,
    account_code character varying(20),
    branch_code character varying(5),
    currency_code character varying(5),
    balance double precision,
    balance_ekiv double precision
);


ALTER TABLE transaction.fact_daily_balance OWNER TO postgres;

--
-- Name: fieldofwork; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.fieldofwork (
    fworkid integer NOT NULL,
    fworkcode character varying(10) DEFAULT NULL::character varying,
    fworkname character varying(60) DEFAULT NULL::character varying,
    fnpwzcode character varying(3) DEFAULT NULL::character varying
);


ALTER TABLE transaction.fieldofwork OWNER TO postgres;

--
-- Name: fixedasset; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.fixedasset (
    accountno character varying(30) NOT NULL,
    totaldibayar double precision,
    qty integer,
    assetcategoryid integer,
    uangmuka double precision,
    hargajual double precision
);


ALTER TABLE transaction.fixedasset OWNER TO postgres;

--
-- Name: fixedassettransactinfo; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.fixedassettransactinfo (
    transactionitemid integer NOT NULL,
    accountno character varying(30),
    cashadvance double precision,
    sellamount double precision
);


ALTER TABLE transaction.fixedassettransactinfo OWNER TO postgres;

--
-- Name: fixedassettransactitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.fixedassettransactitem (
    transactionitemid integer NOT NULL,
    cashadvance double precision,
    sellamount double precision
);


ALTER TABLE transaction.fixedassettransactitem OWNER TO postgres;

--
-- Name: funddailybalance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.funddailybalance (
    dailybalanceid integer NOT NULL,
    balancedate timestamp without time zone,
    lastdaybalance double precision,
    debit double precision,
    credit double precision,
    balance double precision,
    trialbalance double precision,
    isclosed character varying(1),
    accountno character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE transaction.funddailybalance OWNER TO postgres;

--
-- Name: fundproject; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.fundproject (
    budgetamount double precision,
    startdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    finsihdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    productid integer NOT NULL
);


ALTER TABLE transaction.fundproject OWNER TO postgres;

--
-- Name: fundprojectaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.fundprojectaccount (
    accountno character varying(30) NOT NULL,
    startdate timestamp without time zone,
    finishdate timestamp without time zone,
    budgetamount double precision
);


ALTER TABLE transaction.fundprojectaccount OWNER TO postgres;

--
-- Name: fundprojectsponsor; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.fundprojectsponsor (
    projectsponsorid integer NOT NULL,
    productid integer,
    sponsorid integer,
    projectsponsorcode character varying(10),
    agreementdate timestamp without time zone,
    donationamount double precision,
    disbursedamount double precision,
    distributedamount double precision,
    accountno character varying(30)
);


ALTER TABLE transaction.fundprojectsponsor OWNER TO postgres;

--
-- Name: gammu; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.gammu (
    "Version" smallint DEFAULT (0)::smallint NOT NULL
);


ALTER TABLE transaction.gammu OWNER TO postgres;

--
-- Name: generalclass; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.generalclass (
    id integer NOT NULL
);


ALTER TABLE transaction.generalclass OWNER TO postgres;

--
-- Name: generatejournal_candidate; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.generatejournal_candidate (
    transactionid integer NOT NULL
);


ALTER TABLE transaction.generatejournal_candidate OWNER TO postgres;

--
-- Name: glinterface; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.glinterface (
    interfaceid integer NOT NULL,
    interfacecode character varying(30),
    description character varying(100),
    accountcode character varying(20),
    accountname character varying(60),
    productid integer
);


ALTER TABLE transaction.glinterface OWNER TO postgres;

--
-- Name: glinterfacecontainer; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.glinterfacecontainer (
    glicontainerid integer NOT NULL,
    glicontainercode character varying(20),
    glicontainername character varying(50)
);


ALTER TABLE transaction.glinterfacecontainer OWNER TO postgres;

--
-- Name: glinterfaceidentifier; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.glinterfaceidentifier (
    identifier_id integer NOT NULL,
    fundcategory character varying(1),
    ashnaf character varying(1),
    programcategory character varying(10),
    programtype character varying(1),
    interfacecode character varying(30),
    interfacetype character varying(1),
    description character varying(200)
);


ALTER TABLE transaction.glinterfaceidentifier OWNER TO postgres;

--
-- Name: glinterfacemember; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.glinterfacemember (
    glimemberid integer NOT NULL,
    glimembercode character varying(20),
    accountcode character varying(20),
    accountname character varying(100),
    description character varying(100),
    glicontainerid integer
);


ALTER TABLE transaction.glinterfacemember OWNER TO postgres;

--
-- Name: glintftemplate; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.glintftemplate (
    template_code character varying(30) NOT NULL,
    description character varying(200),
    fundcategory character varying(1)
);


ALTER TABLE transaction.glintftemplate OWNER TO postgres;

--
-- Name: glintftemplatedetail; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.glintftemplatedetail (
    templatedetail_id integer NOT NULL,
    template_code character varying(30),
    interfacecode character varying(30),
    description character varying(100),
    accountcode character varying(20)
);


ALTER TABLE transaction.glintftemplatedetail OWNER TO postgres;

--
-- Name: globalglinterface; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.globalglinterface (
    glinterfacecode character varying(20) NOT NULL,
    glinterfacename character varying(100),
    accountcode character varying(20)
);


ALTER TABLE transaction.globalglinterface OWNER TO postgres;

--
-- Name: hi_permil; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.hi_permil (
    p_year integer,
    p_month integer,
    currency_code character varying(3) DEFAULT NULL::character varying,
    day_number integer,
    amount double precision,
    process_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    id_hipermil integer NOT NULL,
    ekuiv_rate double precision
);


ALTER TABLE transaction.hi_permil OWNER TO postgres;

--
-- Name: hipermildistribution; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.hipermildistribution (
    distribution_id character varying(2) DEFAULT NULL::character varying NOT NULL,
    hipermil_ratio double precision,
    ekuiv_rate_ratio double precision,
    id_hipermil integer NOT NULL
);


ALTER TABLE transaction.hipermildistribution OWNER TO postgres;

--
-- Name: historyofchanges; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.historyofchanges (
    historyid integer NOT NULL,
    changetype character varying(1) DEFAULT NULL::character varying,
    domainofchange character varying(30) DEFAULT NULL::character varying,
    processtime timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    userid character varying(30) DEFAULT NULL::character varying,
    datasourcetype character varying(1) DEFAULT NULL::character varying,
    datasourceref character varying(100) DEFAULT NULL::character varying,
    datasourceclass character varying(50) DEFAULT NULL::character varying,
    datasourcerefinteger integer,
    terminalid character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.historyofchanges OWNER TO postgres;

--
-- Name: humancapitalbatch; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.humancapitalbatch (
    batchid integer NOT NULL,
    description character varying(200),
    batchperioddesc character varying(50),
    uploaddate timestamp without time zone,
    uploaduserid character varying(50),
    transactiondate timestamp(6) without time zone
);


ALTER TABLE transaction.humancapitalbatch OWNER TO postgres;

--
-- Name: humancapitalbatchitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.humancapitalbatchitem (
    batchitemid integer NOT NULL,
    description character varying(200),
    batchid integer,
    transactionid integer,
    businessareacode character varying(10),
    businessareadescription character varying(200),
    employeenumber character varying(30),
    name character varying(200),
    birthdate timestamp without time zone,
    birthplace character varying(150),
    gender character varying(10),
    maritalstatus character varying(20),
    "position" character varying(200),
    organizationalunit character varying(200),
    amountzakat numeric(30,2),
    amountinfaq numeric(30,2),
    amountanakyatim numeric(30,2),
    amountanakasuh numeric(30,2),
    iscreateemployeedata character varying(1),
    organizationunit character varying(200),
    donorid integer,
    workareaname character varying(100),
    mobilephone character varying(20),
    amountwakaf numeric(30,2),
    amountqurban numeric(30,2),
    smslog_id integer,
    smslog_time timestamp without time zone
);


ALTER TABLE transaction.humancapitalbatchitem OWNER TO postgres;

--
-- Name: humancapitalpassedreport; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.humancapitalpassedreport (
    reportid integer NOT NULL,
    batchid integer,
    employeenumber character varying(30),
    donorid integer
);


ALTER TABLE transaction.humancapitalpassedreport OWNER TO postgres;

--
-- Name: id_gen; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.id_gen (
    id_code character varying(50) DEFAULT NULL::character varying NOT NULL,
    last_id integer,
    locked character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE transaction.id_gen OWNER TO postgres;

--
-- Name: inbox; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.inbox (
    inboxid integer NOT NULL,
    inputtime timestamp(6) without time zone,
    kodeinbox character varying(10),
    userid character varying(30),
    filename character varying(200),
    description character varying(100),
    branchcode character varying(5),
    lastinboxhistoryid integer,
    inboxtype character varying(1),
    inputdate timestamp(6) without time zone
);


ALTER TABLE transaction.inbox OWNER TO postgres;

--
-- Name: inbox_id_seq; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.inbox_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.inbox_id_seq OWNER TO postgres;

--
-- Name: inboxhistory; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.inboxhistory (
    inboxhistoryid integer NOT NULL,
    inboxid integer NOT NULL,
    inputtime timestamp(6) without time zone,
    userid character varying(30),
    filename character varying(200),
    nextinboxhistoryid integer,
    inputdate timestamp(6) without time zone
);


ALTER TABLE transaction.inboxhistory OWNER TO postgres;

--
-- Name: inboxtransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.inboxtransaction (
    inboxid integer NOT NULL,
    transactionid integer
);


ALTER TABLE transaction.inboxtransaction OWNER TO postgres;

--
-- Name: individualdonor; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.individualdonor (
    gender character varying(1) DEFAULT NULL::character varying,
    birthplace character varying(30) DEFAULT NULL::character varying,
    birthdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    identitytype character varying(1) DEFAULT NULL::character varying,
    religion integer,
    identitynumber character varying(20) DEFAULT NULL::character varying,
    language character varying(1) DEFAULT NULL::character varying,
    lastformaleducation integer,
    incomepermonth double precision,
    expensepermonth double precision,
    maritalstate character varying(1) DEFAULT NULL::character varying,
    officeaddress character varying(200) DEFAULT NULL::character varying,
    officekelurahan character varying(50) DEFAULT NULL::character varying,
    officesubdistrict character varying(50) DEFAULT NULL::character varying,
    officecity character varying(50) DEFAULT NULL::character varying,
    officestate character varying(50) DEFAULT NULL::character varying,
    officepostalcode character varying(50) DEFAULT NULL::character varying,
    officephonenumber character varying(50) DEFAULT NULL::character varying,
    email character varying(200),
    donorid integer NOT NULL,
    mobilephone character varying(20),
    idpropinsioffice integer,
    officekecamatan character varying(50) DEFAULT NULL::character varying,
    corporatename character varying(50) DEFAULT NULL::character varying,
    jobposition character varying(50) DEFAULT NULL::character varying,
    couplename character varying(50) DEFAULT NULL::character varying,
    fworkid integer,
    child integer,
    isinternalemployee character varying(1),
    workareaid integer,
    workunitid integer,
    workidentitynumber character varying(30),
    statusrumah character varying(1)
);


ALTER TABLE transaction.individualdonor OWNER TO postgres;

--
-- Name: intrnewtransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.intrnewtransaction (
    subsysteminteraction_id integer NOT NULL,
    dialogid character varying(80) DEFAULT NULL::character varying,
    processingscriptid character varying(80) DEFAULT NULL::character varying,
    numbertag integer,
    servermethodid character varying(80) DEFAULT NULL::character varying
);


ALTER TABLE transaction.intrnewtransaction OWNER TO postgres;

--
-- Name: intrpicktransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.intrpicktransaction (
    subsysteminteraction_id integer NOT NULL,
    dialogid character varying(80) DEFAULT NULL::character varying,
    numbertag integer
);


ALTER TABLE transaction.intrpicktransaction OWNER TO postgres;

--
-- Name: inventory; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.inventory (
    accountno character varying(30) NOT NULL,
    nilaiawal double precision,
    nilaisisa double precision,
    qtysisa double precision,
    qtytotal double precision,
    inventorycategoryid integer
);


ALTER TABLE transaction.inventory OWNER TO postgres;

--
-- Name: inventorycategory; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.inventorycategory (
    inventorycategoryid integer NOT NULL,
    parentinventorycategoryid integer,
    inventorycategorycode character varying(20),
    inventorycategoryname character varying(100),
    glicontainerid integer
);


ALTER TABLE transaction.inventorycategory OWNER TO postgres;

--
-- Name: investee; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.investee (
    investeeid integer NOT NULL,
    investeename character varying(150),
    investeecode character varying(10),
    branchcode character varying(5),
    description character varying(200),
    investeephone character varying(30),
    investeeaddress character varying(250),
    investeenisbah double precision
);


ALTER TABLE transaction.investee OWNER TO postgres;

--
-- Name: investment; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.investment (
    accountno character varying(30) NOT NULL,
    managerid integer,
    fundentity integer,
    investmentamount double precision,
    investmentcatid integer,
    investmentshare double precision,
    lifetime integer,
    investmenttype character varying(1),
    investeeid integer,
    employeeid integer,
    startdate timestamp(6) without time zone,
    investmentnisbah double precision,
    investmentdescription character varying(200),
    fundcategory character varying(1)
);


ALTER TABLE transaction.investment OWNER TO postgres;

--
-- Name: investmentcategory; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.investmentcategory (
    investmentcatid integer NOT NULL,
    investmentcatname character varying(150),
    investmentcatcode character varying(5),
    investmentcattype character varying(1),
    glicontainerid integer
);


ALTER TABLE transaction.investmentcategory OWNER TO postgres;

--
-- Name: investmentmanager; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.investmentmanager (
    managerid integer NOT NULL,
    managercode character varying(10),
    managername character varying(10),
    branchcode character varying(5)
);


ALTER TABLE transaction.investmentmanager OWNER TO postgres;

--
-- Name: invoice; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.invoice (
    invoiceid integer NOT NULL,
    invoicedate timestamp(6) without time zone,
    invoiceno character varying(30),
    invoicetype character varying(1),
    invoiceamount double precision,
    invoicepaymentstatus character varying(1),
    branchcode character varying(10),
    transactionid integer,
    paymenttransactionid integer,
    description character varying(200)
);


ALTER TABLE transaction.invoice OWNER TO postgres;

--
-- Name: invoicefa; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.invoicefa (
    invoiceid integer NOT NULL,
    accountno character varying(30)
);


ALTER TABLE transaction.invoicefa OWNER TO postgres;

--
-- Name: invoiceproduct; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.invoiceproduct (
    invoiceid integer NOT NULL,
    invoiceaddress character varying(250),
    invoicebankname character varying(100),
    invoicebankaccountname character varying(100),
    invoicebankaccountnumber character varying(30),
    invoiceofficername character varying(100),
    invoiceofficerposition character varying(100),
    invoicetermdate timestamp(6) without time zone,
    sponsorid integer,
    productaccountno character varying(30),
    invoicecontactperson character varying(100),
    invoicecontactphone character varying(20)
);


ALTER TABLE transaction.invoiceproduct OWNER TO postgres;

--
-- Name: invoiceproductdefaultdata; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.invoiceproductdefaultdata (
    branchcode character varying(5) NOT NULL,
    invoicebankname character varying(100),
    invoicebankaccountname character varying(100),
    invoicebankaccountnumber character varying(30),
    invoiceofficername character varying(100),
    invoiceofficerposition character varying(100),
    invoicecontactperson character varying(100),
    invoicecontactphone character varying(20)
);


ALTER TABLE transaction.invoiceproductdefaultdata OWNER TO postgres;

--
-- Name: jenis_dana; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.jenis_dana (
    kode_jenis_dana integer NOT NULL,
    nama_jenis_dana character varying(50)
);


ALTER TABLE transaction.jenis_dana OWNER TO postgres;

--
-- Name: jenisrak; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.jenisrak (
    koderak character varying(30) DEFAULT NULL::character varying NOT NULL,
    deskripsi character varying(50) DEFAULT NULL::character varying,
    accountcode_rakpusat character varying(20) DEFAULT NULL::character varying,
    jenisrak character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE transaction.jenisrak OWNER TO postgres;

--
-- Name: journal; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journal (
    journal_no character varying(30) NOT NULL,
    journal_date_posting timestamp(6) without time zone,
    description character varying(200),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journal_date_last_modified timestamp(6) without time zone,
    userid_posting character varying(20),
    is_posted character varying(1),
    journal_type character varying(10),
    journal_date timestamp(6) without time zone,
    lastitemno integer,
    status character varying(1),
    docoprstatus character varying(1),
    is_partlychecked character varying(1),
    branch_code character varying(5),
    transaction_date timestamp(6) without time zone,
    journal_state character varying(1),
    serial_no character varying(23),
    event_date timestamp(6) without time zone,
    lock_userid character varying(20),
    fl_origin_journal character varying(30),
    id_journalcreation integer,
    source_app character varying(30),
    source_app_class character varying(30),
    source_app_ref character varying(30),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4)
);


ALTER TABLE transaction.journal OWNER TO postgres;

--
-- Name: journal_bck; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journal_bck (
    journal_no character varying(30),
    journal_date_posting timestamp(6) without time zone,
    description character varying(200),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journal_date_last_modified timestamp(6) without time zone,
    userid_posting character varying(20),
    is_posted character varying(1),
    journal_type character varying(10),
    journal_date timestamp(6) without time zone,
    lastitemno integer,
    status character varying(1),
    docoprstatus character varying(1),
    is_partlychecked character varying(1),
    branch_code character varying(5),
    transaction_date timestamp(6) without time zone,
    journal_state character varying(1),
    serial_no character varying(23),
    event_date timestamp(6) without time zone,
    lock_userid character varying(20),
    fl_origin_journal character varying(30),
    id_journalcreation integer,
    source_app character varying(30),
    source_app_class character varying(30),
    source_app_ref character varying(30),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4)
);


ALTER TABLE transaction.journal_bck OWNER TO postgres;

--
-- Name: journal_bck20150821; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journal_bck20150821 (
    journal_no character varying(30),
    journal_date_posting timestamp(6) without time zone,
    description character varying(200),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journal_date_last_modified timestamp(6) without time zone,
    userid_posting character varying(20),
    is_posted character varying(1),
    journal_type character varying(10),
    journal_date timestamp(6) without time zone,
    lastitemno integer,
    status character varying(1),
    docoprstatus character varying(1),
    is_partlychecked character varying(1),
    branch_code character varying(5),
    transaction_date timestamp(6) without time zone,
    journal_state character varying(1),
    serial_no character varying(23),
    event_date timestamp(6) without time zone,
    lock_userid character varying(20),
    fl_origin_journal character varying(30),
    id_journalcreation integer,
    source_app character varying(30),
    source_app_class character varying(30),
    source_app_ref character varying(30),
    periode_code integer,
    fl_accountingperiode integer,
    fl_accountingyear character varying(4)
);


ALTER TABLE transaction.journal_bck20150821 OWNER TO postgres;

--
-- Name: journal_cashflow; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journal_cashflow (
    journal_no character varying(30) NOT NULL,
    cfgroupid integer
);


ALTER TABLE transaction.journal_cashflow OWNER TO postgres;

--
-- Name: journal_cashflow_candidate; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journal_cashflow_candidate (
    journal_no character varying(30) NOT NULL
);


ALTER TABLE transaction.journal_cashflow_candidate OWNER TO postgres;

--
-- Name: journalblock; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journalblock (
    system_id character varying(10) DEFAULT NULL::character varying,
    class_id character varying(32) DEFAULT NULL::character varying,
    key_id integer,
    id_journalblock integer NOT NULL,
    dataid character varying(50) DEFAULT NULL::character varying,
    id_journalcreation integer,
    journal_no character varying(30) DEFAULT NULL::character varying,
    subsystemcode character varying(20) DEFAULT NULL::character varying,
    transaction_tag character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.journalblock OWNER TO postgres;

--
-- Name: journalcode; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journalcode (
    description character varying(100) DEFAULT NULL::character varying,
    user_input character varying(20) DEFAULT NULL::character varying,
    terminal_input character varying(15) DEFAULT NULL::character varying,
    user_ubah character varying(20) DEFAULT NULL::character varying,
    terminal_ubah character varying(15) DEFAULT NULL::character varying,
    tanggal_input timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    tanggal_ubah timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    journalcode_id character varying(10) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE transaction.journalcode OWNER TO postgres;

--
-- Name: journaldeletion; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journaldeletion (
    journal_no character varying(30) DEFAULT NULL::character varying NOT NULL,
    user_id character varying(20) DEFAULT NULL::character varying,
    user_terminal character varying(23) DEFAULT NULL::character varying,
    process_time timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE transaction.journaldeletion OWNER TO postgres;

--
-- Name: journalitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journalitem (
    fl_journal character varying(30) NOT NULL,
    journalitem_no integer NOT NULL,
    fl_account character varying(20),
    amount_debit numeric(36,10),
    amount_credit numeric(36,10),
    description character varying(200),
    branch_code character varying(20),
    valuta_code character varying(20),
    rc_code character varying(20),
    generic_code character varying(20),
    fl_posting_account character varying(20),
    fl_project_no character varying(10),
    docoprstatus character varying(1),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journalitemstatus character varying(1),
    userid_posting character varying(20),
    userid_check character varying(20),
    dateposting timestamp(6) without time zone,
    datelastmod timestamp(6) without time zone,
    datecreate timestamp(6) without time zone,
    event_date timestamp(6) without time zone,
    journalitemtype character varying(1),
    kode_kurs character varying(20),
    nilai_kurs numeric(36,10),
    rpv_main integer,
    subsystemcode character varying(20),
    subaccountcode character varying(30),
    id_journalcreation integer,
    subaccountname character varying(100),
    accountinstance_id integer,
    id_journalblock integer,
    transaksirak_id integer,
    source_class_id character varying(32),
    source_key_id integer,
    additionaldescription character varying(200)
);


ALTER TABLE transaction.journalitem OWNER TO postgres;

--
-- Name: journalitem_cashflow; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.journalitem_cashflow (
    journal_no character varying(30) NOT NULL,
    journalitem_no integer NOT NULL,
    cfgroupid integer
);


ALTER TABLE transaction.journalitem_cashflow OWNER TO postgres;

--
-- Name: kota_kabupaten; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.kota_kabupaten (
    kotaid integer NOT NULL,
    idpropinsi integer,
    idnegara integer,
    kota_kabupaten character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE transaction.kota_kabupaten OWNER TO postgres;

--
-- Name: kurshistory; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.kurshistory (
    kurshistory_id integer NOT NULL,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_beli_kantorpusat double precision,
    kurs_jual_kantorpusat double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_buku double precision,
    kurs_neraca double precision,
    kurs_tengah_bi double precision,
    history_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    user_ubah character varying(20) DEFAULT NULL::character varying,
    user_otorisasi character varying(20) DEFAULT NULL::character varying,
    terminal_pengubah character varying(15) DEFAULT NULL::character varying,
    terminal_otorisasi character varying(15) DEFAULT NULL::character varying,
    kurs_reval double precision,
    kurs_remittance double precision,
    currency_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.kurshistory OWNER TO postgres;

--
-- Name: mapaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mapaccount (
    oldaccount character varying(255),
    newaccount character varying(255)
);


ALTER TABLE transaction.mapaccount OWNER TO postgres;

--
-- Name: mapping_gldetail_2014; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mapping_gldetail_2014 (
    account_code_old character varying(10) NOT NULL,
    account_code_new character varying(10)
);


ALTER TABLE transaction.mapping_gldetail_2014 OWNER TO postgres;

--
-- Name: mapping_glint_asset; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mapping_glint_asset (
    account_code character varying(20) NOT NULL,
    account_code_new character varying(20)
);


ALTER TABLE transaction.mapping_glint_asset OWNER TO postgres;

--
-- Name: mapping_glinttemplate_2014; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mapping_glinttemplate_2014 (
    productcode character varying(20) NOT NULL,
    template_code character varying(30)
);


ALTER TABLE transaction.mapping_glinttemplate_2014 OWNER TO postgres;

--
-- Name: mappingcoa; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mappingcoa (
    account_code_lama character varying(20) NOT NULL,
    account_code_baru character varying(20)
);


ALTER TABLE transaction.mappingcoa OWNER TO postgres;

--
-- Name: mapreconcile; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mapreconcile (
    mapid integer NOT NULL,
    mapdescription character varying(200),
    mapproductid integer,
    mapfundentity integer,
    mapprocesstype character varying(1),
    isapplytoallaccount character varying(1),
    bankaccountno character varying(30),
    mapaccounttype character varying(1),
    mapmutationtype character varying(1),
    mapaccountcode character varying(20)
);


ALTER TABLE transaction.mapreconcile OWNER TO postgres;

--
-- Name: mapreconcileaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mapreconcileaccount (
    mapaccountid integer NOT NULL,
    mapid integer,
    bankcashaccountno character varying(30)
);


ALTER TABLE transaction.mapreconcileaccount OWNER TO postgres;

--
-- Name: marketer; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.marketer AS
 SELECT marketerid,
    marketercode,
    marketername,
    marketeraddress,
    marketermobilephone,
    branchcode
   FROM fund.marketer;


ALTER VIEW transaction.marketer OWNER TO postgres;

--
-- Name: masterkurs; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.masterkurs (
    kode_kurs character varying(20) DEFAULT NULL::character varying NOT NULL,
    nama_kurs character varying(30) DEFAULT NULL::character varying,
    deskripsi character varying(50) DEFAULT NULL::character varying,
    nama_field_currency character varying(30) DEFAULT NULL::character varying,
    rpv_name character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.masterkurs OWNER TO postgres;

--
-- Name: mustahiq; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mustahiq (
    mustahiqaddress character varying(100),
    mustahiqname character varying(50),
    mustahiqphonenumber character varying(30),
    mustahiqreferenceby character varying(150),
    mustahiqstatus character(1),
    mustahiqid integer,
    mustahiqno character varying(20),
    mustahiqtype character varying(2),
    branchcode character varying(5),
    mustahiqaddresskelurahan character varying(30),
    mustahiqaddresskecamatan character varying(30),
    idpropinsi integer,
    mustahiqpostalcode character varying(10)
);


ALTER TABLE transaction.mustahiq OWNER TO postgres;

--
-- Name: mustahiqbankaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mustahiqbankaccount (
    bankaccountid integer NOT NULL,
    mustahiqid integer
);


ALTER TABLE transaction.mustahiqbankaccount OWNER TO postgres;

--
-- Name: mustahiqcorporate; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mustahiqcorporate (
    cpmobilenumber character varying(30),
    cpname character varying(150),
    cpphonenumber character varying(30),
    mustahiqid integer
);


ALTER TABLE transaction.mustahiqcorporate OWNER TO postgres;

--
-- Name: mustahiqpersonal; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.mustahiqpersonal (
    mustahiqashnaf character varying(1),
    mustahiqbirthdate date,
    mustahiqbirthplace character varying(150),
    mustahiqformaleducation integer,
    mustahiqgender character varying(1),
    mustahiqidentitynumber character varying(30),
    mustahiqmarital character varying(1),
    mustahiqreligion integer,
    mustahiqtotalfamily integer,
    mustahiqid integer,
    mustahiqincome double precision,
    mustahiqidentitytype character varying(1),
    mustahiqworksector character varying(1)
);


ALTER TABLE transaction.mustahiqpersonal OWNER TO postgres;

--
-- Name: negara; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.negara (
    idnegara integer NOT NULL,
    nama_negara character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE transaction.negara OWNER TO postgres;

--
-- Name: parameter; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.parameter (
    parametercode character varying(20) DEFAULT NULL::character varying NOT NULL,
    parametervalue double precision,
    description character varying(100) DEFAULT NULL::character varying,
    parameterstringvalue character varying(100) DEFAULT NULL::character varying,
    parameterdatevalue timestamp(6) without time zone
);


ALTER TABLE transaction.parameter OWNER TO postgres;

--
-- Name: parameterglobal; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.parameterglobal (
    kode_parameter character varying(25) DEFAULT NULL::character varying NOT NULL,
    tipe_parameter character varying(1) DEFAULT NULL::character varying,
    nilai_parameter double precision,
    deskripsi character varying(100) DEFAULT NULL::character varying,
    is_parameter_system character varying(1) DEFAULT NULL::character varying,
    nilai_parameter_tanggal timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    nilai_parameter_string character varying(30) DEFAULT NULL::character varying,
    tag character varying(15),
    default_code character varying(30)
);


ALTER TABLE transaction.parameterglobal OWNER TO postgres;

--
-- Name: parameterglobaltes; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.parameterglobaltes (
    kode_parameter character varying(10),
    tipe_parameter character varying(1),
    nilai_parameter double precision,
    deskripsi character varying(60),
    is_parameter_system character varying(1),
    nilai_parameter_tanggal timestamp(6) without time zone,
    nilai_parameter_string character varying(30),
    tag character varying(15),
    default_code character varying(30)
);


ALTER TABLE transaction.parameterglobaltes OWNER TO postgres;

--
-- Name: parameterinbox; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.parameterinbox (
    kodeinbox character varying(10) NOT NULL,
    description character varying(100),
    namaform character varying(100),
    taginbox character varying(20)
);


ALTER TABLE transaction.parameterinbox OWNER TO postgres;

--
-- Name: parameterjournal; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.parameterjournal (
    parameterjournalid integer NOT NULL,
    journalcode character varying(5) DEFAULT NULL::character varying NOT NULL,
    description character varying(100) DEFAULT NULL::character varying,
    datasource character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE transaction.parameterjournal OWNER TO postgres;

--
-- Name: parameterjournalitem; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.parameterjournalitem (
    parameterjournalitemid integer NOT NULL,
    accountcode character varying(20) DEFAULT NULL::character varying,
    branchbase character varying(1) DEFAULT NULL::character varying NOT NULL,
    description character varying(50) DEFAULT NULL::character varying,
    basesign character varying(1) DEFAULT NULL::character varying NOT NULL,
    currencybase character varying(1) DEFAULT NULL::character varying,
    amountbase character varying(30) DEFAULT NULL::character varying,
    ratebase character varying(30) DEFAULT NULL::character varying,
    parameterjournalid integer NOT NULL,
    accountbase character varying(1) DEFAULT NULL::character varying NOT NULL,
    issendjournaldescription character varying(1),
    issendrccode character varying(1)
);


ALTER TABLE transaction.parameterjournalitem OWNER TO postgres;

--
-- Name: periodebalance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.periodebalance (
    periodebalance_id integer NOT NULL,
    balance double precision,
    balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balancecumulative double precision,
    balancecumulative_ekuiv double precision,
    debit double precision,
    credit double precision,
    debit_ekuiv double precision,
    credit_ekuiv double precision,
    accountinstance_id integer,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying,
    periode_code integer
);


ALTER TABLE transaction.periodebalance OWNER TO postgres;

--
-- Name: periodeprojectbalance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.periodeprojectbalance (
    periodeprojectbalance_id integer NOT NULL,
    debit double precision,
    credit double precision,
    balance double precision,
    balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balancecumulative double precision,
    balancecumulative_ekuiv double precision,
    debit_ekuiv double precision,
    credit_ekuiv double precision,
    project_no character varying(10) DEFAULT NULL::character varying,
    fl_accountingyear character varying(4) DEFAULT NULL::character varying,
    periode_code integer,
    accountinstance_id integer
);


ALTER TABLE transaction.periodeprojectbalance OWNER TO postgres;

--
-- Name: producthierarchy; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.producthierarchy (
    hierarchyid integer NOT NULL,
    parentproductid integer,
    childproductid integer,
    level integer
);


ALTER TABLE transaction.producthierarchy OWNER TO postgres;

--
-- Name: project; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.project (
    project_no character varying(10) DEFAULT NULL::character varying NOT NULL,
    name character varying(30) DEFAULT NULL::character varying,
    description character varying(255) DEFAULT NULL::character varying,
    manager character varying(30) DEFAULT NULL::character varying,
    start_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    end_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    dailyprojectbalance_id integer,
    periodeprojectbalance_id integer
);


ALTER TABLE transaction.project OWNER TO postgres;

--
-- Name: projectsponsordisbursement; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.projectsponsordisbursement (
    disbid integer NOT NULL,
    disbnumber integer NOT NULL,
    disbdateplan timestamp without time zone,
    disbamountplan double precision,
    isdisbursed character varying(1),
    transactionitemid integer,
    projectsponsorid integer
);


ALTER TABLE transaction.projectsponsordisbursement OWNER TO postgres;

--
-- Name: propinsi; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.propinsi (
    idpropinsi integer NOT NULL,
    idnegara integer,
    propinsi character varying(50) DEFAULT NULL::character varying,
    kodepropinsi character varying(3) DEFAULT NULL::character varying
);


ALTER TABLE transaction.propinsi OWNER TO postgres;

--
-- Name: prospectivedonor; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.prospectivedonor (
    prospectivedonorid integer NOT NULL,
    phonenumber character varying(20) DEFAULT NULL::character varying,
    donorname character varying(30) DEFAULT NULL::character varying,
    referenceby character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE transaction.prospectivedonor OWNER TO postgres;

--
-- Name: rakcabang; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.rakcabang (
    rakcabang_id integer NOT NULL,
    branch_code character varying(5) DEFAULT NULL::character varying,
    koderak character varying(30) DEFAULT NULL::character varying,
    accountinstance_id integer
);


ALTER TABLE transaction.rakcabang OWNER TO postgres;

--
-- Name: rakpusat; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.rakpusat (
    rakpusat_id integer NOT NULL,
    koderak character varying(30) DEFAULT NULL::character varying,
    accountinstance_id integer
);


ALTER TABLE transaction.rakpusat OWNER TO postgres;

--
-- Name: reconcileaccountbalance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.reconcileaccountbalance (
    accountbalanceid integer NOT NULL,
    bankaccountno character varying(20),
    beginbalance double precision,
    reconciledate timestamp(6) without time zone
);


ALTER TABLE transaction.reconcileaccountbalance OWNER TO postgres;

--
-- Name: reconciletransactionbck; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.reconciletransactionbck (
    banktransactionid integer,
    transactiondate timestamp(6) without time zone,
    accountcredit character varying(20),
    accountdebet character varying(20),
    amount double precision,
    description character varying(200),
    transactioncode character varying(10),
    fundentity integer,
    productid integer,
    branchcode character varying(5),
    reconstatus boolean,
    transactionid integer,
    processstatus character varying(1),
    mutationtype character varying(1)
);


ALTER TABLE transaction.reconciletransactionbck OWNER TO postgres;

--
-- Name: registerkurs; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.registerkurs (
    registerkurs_id integer NOT NULL,
    user_ubah character varying(20) DEFAULT NULL::character varying,
    terminal_ubah character varying(15) DEFAULT NULL::character varying,
    tanggal_ubah timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    kurs_beli_banknote double precision,
    kurs_jual_banknote double precision,
    kurs_tengah_bi double precision,
    kurs_beli_transfer double precision,
    kurs_jual_transfer double precision,
    kurs_buku double precision,
    kurs_beli_kantorpusat double precision,
    kurs_jual_kantorpusat double precision,
    kurs_neraca double precision,
    kode_register character varying(1) DEFAULT NULL::character varying,
    kurs_reval double precision,
    kurs_remittance double precision,
    currency_code character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.registerkurs OWNER TO postgres;

--
-- Name: rekeningbmm; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.rekeningbmm (
    nomorrekening character varying(20) NOT NULL
);


ALTER TABLE transaction.rekeningbmm OWNER TO postgres;

--
-- Name: revaluationhistory; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.revaluationhistory (
    history_id integer NOT NULL,
    revaluation_date timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    currency_code character varying(20) DEFAULT NULL::character varying,
    average_exchangerate double precision,
    revaluation_exchangerate double precision,
    branch_code character varying(5) DEFAULT NULL::character varying
);


ALTER TABLE transaction.revaluationhistory OWNER TO postgres;

--
-- Name: reversetransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.reversetransaction (
    sourcetransactionid integer NOT NULL,
    revtransactionid integer
);


ALTER TABLE transaction.reversetransaction OWNER TO postgres;

--
-- Name: rpvaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.rpvaccount (
    rpv_name character varying(20) DEFAULT NULL::character varying NOT NULL,
    rpv_accountcode character varying(20) DEFAULT NULL::character varying,
    profit_accountcode character varying(20) DEFAULT NULL::character varying,
    loss_accountcode character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.rpvaccount OWNER TO postgres;

--
-- Name: rpvaccountdetail; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.rpvaccountdetail (
    accountinstance_valas integer,
    accountinstance_primer integer,
    rpvaccountdetail_accountcode character varying(20) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying NOT NULL,
    rpv_name character varying(20) DEFAULT NULL::character varying NOT NULL,
    branch_code character varying(5) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE transaction.rpvaccountdetail OWNER TO postgres;

--
-- Name: salestransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.salestransaction (
    transactionid integer NOT NULL,
    salespersonname character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE transaction.salestransaction OWNER TO postgres;

--
-- Name: script_collection; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.script_collection (
    script_code character varying(15) NOT NULL,
    script_name character varying(100),
    script_description character varying(200),
    script_path character varying(200)
);


ALTER TABLE transaction.script_collection OWNER TO postgres;

--
-- Name: seq_200; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_200
    START WITH 109
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_200 OWNER TO postgres;

--
-- Name: seq_accounthierarchy; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_accounthierarchy
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_accounthierarchy OWNER TO postgres;

--
-- Name: seq_accountinstance; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_accountinstance
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_accountinstance OWNER TO postgres;

--
-- Name: seq_assetcategory; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_assetcategory
    START WITH 13
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_assetcategory OWNER TO postgres;

--
-- Name: seq_balancesumitem; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_balancesumitem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_balancesumitem OWNER TO postgres;

--
-- Name: seq_balancesumitemmember; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_balancesumitemmember
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_balancesumitemmember OWNER TO postgres;

--
-- Name: seq_balancesumitemtrancode; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_balancesumitemtrancode
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_balancesumitemtrancode OWNER TO postgres;

--
-- Name: seq_bankaccountlist; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_bankaccountlist
    START WITH 5537
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_bankaccountlist OWNER TO postgres;

--
-- Name: seq_bankcash; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_bankcash
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_bankcash OWNER TO postgres;

--
-- Name: seq_bankcashid; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_bankcashid
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_bankcashid OWNER TO postgres;

--
-- Name: seq_batchupload; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_batchupload
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_batchupload OWNER TO postgres;

--
-- Name: seq_batchuploaditem; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_batchuploaditem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_batchuploaditem OWNER TO postgres;

--
-- Name: seq_bsz; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_bsz
    START WITH 63
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_bsz OWNER TO postgres;

--
-- Name: seq_bszdetail; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_bszdetail
    START WITH 435
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_bszdetail OWNER TO postgres;

--
-- Name: seq_bsznumber; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_bsznumber
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_bsznumber OWNER TO postgres;

--
-- Name: seq_bsztransaction; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_bsztransaction
    START WITH 83
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_bsztransaction OWNER TO postgres;

--
-- Name: seq_budget; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_budget
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_budget OWNER TO postgres;

--
-- Name: seq_budgetitem; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_budgetitem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_budgetitem OWNER TO postgres;

--
-- Name: seq_budgetitemhierarchy; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_budgetitemhierarchy
    START WITH 2192
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_budgetitemhierarchy OWNER TO postgres;

--
-- Name: seq_budgetowner; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_budgetowner
    START WITH 17
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_budgetowner OWNER TO postgres;

--
-- Name: seq_budgetownerhierarchy; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_budgetownerhierarchy
    START WITH 94
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_budgetownerhierarchy OWNER TO postgres;

--
-- Name: seq_budgetperiod; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_budgetperiod
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_budgetperiod OWNER TO postgres;

--
-- Name: seq_budgetrevision; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_budgetrevision
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_budgetrevision OWNER TO postgres;

--
-- Name: seq_budgettransaction; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_budgettransaction
    START WITH 3
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_budgettransaction OWNER TO postgres;

--
-- Name: seq_cashflowgroup; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_cashflowgroup
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_cashflowgroup OWNER TO postgres;

--
-- Name: seq_cashflowmember; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_cashflowmember
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_cashflowmember OWNER TO postgres;

--
-- Name: seq_custom_idgen; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_custom_idgen
    START WITH 45
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_custom_idgen OWNER TO postgres;

--
-- Name: seq_dailybalance; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_dailybalance
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_dailybalance OWNER TO postgres;

--
-- Name: seq_dailybalancecash; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_dailybalancecash
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_dailybalancecash OWNER TO postgres;

--
-- Name: seq_dailyprojectbalance; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_dailyprojectbalance
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_dailyprojectbalance OWNER TO postgres;

--
-- Name: seq_deprassetid; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_deprassetid
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_deprassetid OWNER TO postgres;

--
-- Name: seq_dinarcertificate; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_dinarcertificate
    START WITH 4
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_dinarcertificate OWNER TO postgres;

--
-- Name: seq_distributiontransferinfo; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_distributiontransferinfo
    START WITH 10
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_distributiontransferinfo OWNER TO postgres;

--
-- Name: seq_donor; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_donor
    START WITH 4757
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_donor OWNER TO postgres;

--
-- Name: seq_donorcommitment; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_donorcommitment
    START WITH 6
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_donorcommitment OWNER TO postgres;

--
-- Name: seq_donortotalfund; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_donortotalfund
    START WITH 4012
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_donortotalfund OWNER TO postgres;

--
-- Name: seq_employee; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_employee
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_employee OWNER TO postgres;

--
-- Name: seq_externaldebtor; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_externaldebtor
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_externaldebtor OWNER TO postgres;

--
-- Name: seq_externaltransaction; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_externaltransaction
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_externaltransaction OWNER TO postgres;

--
-- Name: seq_fact_daily_balance; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_fact_daily_balance
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_fact_daily_balance OWNER TO postgres;

--
-- Name: seq_fieldofwork; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_fieldofwork
    START WITH 12
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_fieldofwork OWNER TO postgres;

--
-- Name: seq_glinterface; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_glinterface
    START WITH 5467
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_glinterface OWNER TO postgres;

--
-- Name: seq_glinterfacecontainer; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_glinterfacecontainer
    START WITH 26
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_glinterfacecontainer OWNER TO postgres;

--
-- Name: seq_glinterfaceidentifier; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_glinterfaceidentifier
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_glinterfaceidentifier OWNER TO postgres;

--
-- Name: seq_glinterfacemember; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_glinterfacemember
    START WITH 165
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_glinterfacemember OWNER TO postgres;

--
-- Name: seq_glintftemplatedetail; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_glintftemplatedetail
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_glintftemplatedetail OWNER TO postgres;

--
-- Name: seq_humancapitalbatch; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_humancapitalbatch
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_humancapitalbatch OWNER TO postgres;

--
-- Name: seq_humancapitalbatchitem; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_humancapitalbatchitem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_humancapitalbatchitem OWNER TO postgres;

--
-- Name: seq_humancapitalpassedreport; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_humancapitalpassedreport
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_humancapitalpassedreport OWNER TO postgres;

--
-- Name: seq_inbox; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_inbox
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_inbox OWNER TO postgres;

--
-- Name: seq_inboxhistory; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_inboxhistory
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_inboxhistory OWNER TO postgres;

--
-- Name: seq_investee; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_investee
    START WITH 14
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_investee OWNER TO postgres;

--
-- Name: seq_investmentcategory; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_investmentcategory
    START WITH 7
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_investmentcategory OWNER TO postgres;

--
-- Name: seq_invoice; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_invoice
    START WITH 22
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_invoice OWNER TO postgres;

--
-- Name: seq_journalblock; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_journalblock
    START WITH 312
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_journalblock OWNER TO postgres;

--
-- Name: seq_journalcreation; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_journalcreation
    START WITH 37
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_journalcreation OWNER TO postgres;

--
-- Name: seq_kurshistory; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_kurshistory
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_kurshistory OWNER TO postgres;

--
-- Name: seq_mapreconcile; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_mapreconcile
    START WITH 52
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_mapreconcile OWNER TO postgres;

--
-- Name: seq_mapreconcileaccount; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_mapreconcileaccount
    START WITH 107
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_mapreconcileaccount OWNER TO postgres;

--
-- Name: seq_marketer; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_marketer
    START WITH 43
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_marketer OWNER TO postgres;

--
-- Name: seq_mustahiq; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_mustahiq
    START WITH 15
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_mustahiq OWNER TO postgres;

--
-- Name: seq_parameterjournal; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_parameterjournal
    START WITH 65
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_parameterjournal OWNER TO postgres;

--
-- Name: seq_parameterjournalitem; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_parameterjournalitem
    START WITH 205
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_parameterjournalitem OWNER TO postgres;

--
-- Name: seq_pettycashid; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_pettycashid
    START WITH 5
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_pettycashid OWNER TO postgres;

--
-- Name: seq_product; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_product
    START WITH 139
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_product OWNER TO postgres;

--
-- Name: seq_productaccountid; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_productaccountid
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_productaccountid OWNER TO postgres;

--
-- Name: seq_producthierarchy; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_producthierarchy
    START WITH 116
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_producthierarchy OWNER TO postgres;

--
-- Name: seq_projectsponsor; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_projectsponsor
    START WITH 27
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_projectsponsor OWNER TO postgres;

--
-- Name: seq_projectsponsordisbursement; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_projectsponsordisbursement
    START WITH 11
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_projectsponsordisbursement OWNER TO postgres;

--
-- Name: seq_propinsi; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_propinsi
    START WITH 37
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_propinsi OWNER TO postgres;

--
-- Name: seq_reconcileaccountbalance; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_reconcileaccountbalance
    START WITH 7290
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_reconcileaccountbalance OWNER TO postgres;

--
-- Name: seq_registerkurs; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_registerkurs
    START WITH 2
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_registerkurs OWNER TO postgres;

--
-- Name: seq_sponsor; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_sponsor
    START WITH 68
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_sponsor OWNER TO postgres;

--
-- Name: seq_test; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_test
    START WITH 103
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_test OWNER TO postgres;

--
-- Name: seq_totalfund; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_totalfund
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_totalfund OWNER TO postgres;

--
-- Name: seq_transaction; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_transaction
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_transaction OWNER TO postgres;

--
-- Name: seq_transactionbatch; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_transactionbatch
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_transactionbatch OWNER TO postgres;

--
-- Name: seq_transactionitem; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_transactionitem
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_transactionitem OWNER TO postgres;

--
-- Name: seq_transactionnumber; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_transactionnumber
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_transactionnumber OWNER TO postgres;

--
-- Name: seq_transhistoryofchanges; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_transhistoryofchanges
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_transhistoryofchanges OWNER TO postgres;

--
-- Name: seq_transrecongenlog; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_transrecongenlog
    START WITH 218745
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_transrecongenlog OWNER TO postgres;

--
-- Name: seq_wakafcertificate; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_wakafcertificate
    START WITH 51
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_wakafcertificate OWNER TO postgres;

--
-- Name: seq_workarea; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_workarea
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_workarea OWNER TO postgres;

--
-- Name: seq_workunit; Type: SEQUENCE; Schema: transaction; Owner: postgres
--

CREATE SEQUENCE transaction.seq_workunit
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE transaction.seq_workunit OWNER TO postgres;

--
-- Name: sessionblob; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.sessionblob (
    id integer NOT NULL,
    sessionid character varying(100) DEFAULT NULL::character varying,
    sessioncontext integer,
    id1 integer
);


ALTER TABLE transaction.sessionblob OWNER TO postgres;

--
-- Name: sim_logrun; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.sim_logrun (
    logrun_id integer NOT NULL,
    sim_userid character varying,
    sim_type character varying(10) DEFAULT NULL::character varying,
    completion_time timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    status integer,
    description character varying(255) DEFAULT NULL::character varying
);


ALTER TABLE transaction.sim_logrun OWNER TO postgres;

--
-- Name: snapshot_accountinstance; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.snapshot_accountinstance (
    accountinstance_id integer,
    balance double precision,
    fl_cpa_accountinstance integer,
    fl_lpa_accountinstance integer,
    balance_ekuiv double precision,
    balance_ratarata double precision,
    balance_ratarata_ekuiv double precision,
    trial_balance double precision,
    trial_balance_ekuiv double precision,
    balance_harilalu double precision,
    balance_harilalu_ekuiv double precision,
    isbolehinput character varying(1),
    branch_code character varying(5),
    account_code character varying(20),
    currency_code character varying(20),
    dailybalance_id integer,
    periodebalance_id integer,
    dailyprojectbalance_id integer,
    periodeprojectbalance_id integer,
    balancecumulative_ekuiv double precision,
    balancecumulative double precision
);


ALTER TABLE transaction.snapshot_accountinstance OWNER TO postgres;

--
-- Name: sponsor; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.sponsor (
    sponsorid integer NOT NULL,
    name character varying(50) DEFAULT NULL::character varying,
    description character varying(100) DEFAULT NULL::character varying,
    address character varying(200) DEFAULT NULL::character varying,
    contactpersonname character varying(32),
    contactpersonnumber character varying(32)
);


ALTER TABLE transaction.sponsor OWNER TO postgres;

--
-- Name: sponsortransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.sponsortransaction (
    transactionitemid integer NOT NULL,
    sponsorid integer,
    projectsponsorid integer,
    sttype character varying(1),
    invoicestatus character varying(1),
    invoicedate timestamp(6) without time zone,
    invoiceno character varying(50)
);


ALTER TABLE transaction.sponsortransaction OWNER TO postgres;

--
-- Name: subsysteminteraction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.subsysteminteraction (
    subsysteminteraction_id integer NOT NULL,
    titleinteraction character varying(50) DEFAULT NULL::character varying,
    parentssi_id integer,
    interactiontype character varying(1) DEFAULT NULL::character varying,
    isactive character varying(1) DEFAULT NULL::character varying,
    intrmodel character varying(1) DEFAULT NULL::character varying,
    subsystemcode character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.subsysteminteraction OWNER TO postgres;

--
-- Name: tempcandidatejournal; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tempcandidatejournal (
    tempcandidatejournal_id integer NOT NULL,
    account_code character varying(20) DEFAULT NULL::character varying,
    branch_code character varying(20) DEFAULT NULL::character varying,
    currency_code character varying(20) DEFAULT NULL::character varying,
    description character varying(100) DEFAULT NULL::character varying,
    group_id integer,
    kode_kurs character varying(20) DEFAULT NULL::character varying,
    kode_mutasi character varying(1) DEFAULT NULL::character varying,
    nilai_kurs double precision,
    nilai_mutasi double precision,
    project_no character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE transaction.tempcandidatejournal OWNER TO postgres;

--
-- Name: temptable; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.temptable (
    accountcode character varying(20) NOT NULL,
    accountname character varying(100),
    accounttype character varying(1),
    isdetail character varying(1),
    accountparent character varying(20),
    cpaaccountcode character varying(20),
    is_processed integer
);


ALTER TABLE transaction.temptable OWNER TO postgres;

--
-- Name: temptable_ori; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.temptable_ori (
    accountcode character varying(20) DEFAULT NULL::character varying NOT NULL,
    accountname character varying(100) DEFAULT NULL::character varying,
    accounttype character varying(1) DEFAULT NULL::character varying,
    isdetail character varying(1) DEFAULT NULL::character varying,
    accountparent character varying(20) DEFAULT NULL::character varying,
    cpaaccountcode character varying(20) DEFAULT NULL::character varying,
    is_processed integer
);


ALTER TABLE transaction.temptable_ori OWNER TO postgres;

--
-- Name: temptabledata; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.temptabledata (
    accountcode character varying(20),
    accountname character varying(100),
    accounttype character varying(1),
    isdetail character varying(1),
    accountparent character varying(20),
    cpaaccountcode character varying(20),
    is_processed integer
);


ALTER TABLE transaction.temptabledata OWNER TO postgres;

--
-- Name: temptablenew; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.temptablenew (
    accountcode character varying(20) NOT NULL,
    accountname character varying(100),
    accounttype character varying(1),
    isdetail character varying(1),
    accountparent character varying(20),
    cpaaccountcode character varying(20),
    is_processed integer
);


ALTER TABLE transaction.temptablenew OWNER TO postgres;

--
-- Name: tmp_accounttransactionitem_bck; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_accounttransactionitem_bck (
    accounttitype character varying(1),
    accountno character varying(30),
    transactionitemid integer,
    amountperunit double precision,
    totalunit integer,
    ashnaf character varying(1),
    fundentity integer,
    percentageofamil double precision,
    distributionitemaccount character varying(20),
    donorid integer,
    cattype character varying(1),
    returntransactionitemid integer,
    catransactionid integer,
    isupdatebalance character varying(1),
    distributiontransferid integer,
    idpropinsi integer,
    kota character varying(100),
    kecamatan character varying(100),
    mustahiqid integer,
    distributioncategory character varying(1),
    marketerid integer,
    fundaccountno character varying(30)
);


ALTER TABLE transaction.tmp_accounttransactionitem_bck OWNER TO postgres;

--
-- Name: tmp_acctranitem_repair_zakat2; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_acctranitem_repair_zakat2 (
    accounttitype character varying(1),
    accountno character varying(30),
    transactionitemid integer,
    amountperunit double precision,
    totalunit integer,
    ashnaf character varying(1),
    fundentity integer,
    percentageofamil double precision,
    distributionitemaccount character varying(20),
    donorid integer,
    cattype character varying(1),
    returntransactionitemid integer,
    catransactionid integer,
    isupdatebalance character varying(1),
    distributiontransferid integer,
    idpropinsi integer,
    kota character varying(100),
    kecamatan character varying(100),
    mustahiqid integer,
    distributioncategory character varying(1),
    marketerid integer,
    fundaccountno character varying(30)
);


ALTER TABLE transaction.tmp_acctranitem_repair_zakat2 OWNER TO postgres;

--
-- Name: tmp_deletedaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_deletedaccount (
    account_code character varying(20) NOT NULL
);


ALTER TABLE transaction.tmp_deletedaccount OWNER TO postgres;

--
-- Name: tmp_gen_productaccount; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_gen_productaccount (
    productid integer NOT NULL,
    productname character varying(20),
    branchcode character varying(10) NOT NULL,
    currencycode character varying(10) NOT NULL
);


ALTER TABLE transaction.tmp_gen_productaccount OWNER TO postgres;

--
-- Name: tmp_hctransactiongroup; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_hctransactiongroup (
    donorid integer NOT NULL,
    fundentity integer NOT NULL,
    transactionid integer,
    transactionno character varying(30),
    transactionitemid integer,
    channelaccountno character varying(30) NOT NULL,
    productaccountno character varying(30),
    journalno character varying(30),
    amount numeric(30,2)
);


ALTER TABLE transaction.tmp_hctransactiongroup OWNER TO postgres;

--
-- Name: tmp_journalitem_bck; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_journalitem_bck (
    fl_journal character varying(30),
    journalitem_no integer,
    fl_account character varying(20),
    amount_debit double precision,
    amount_credit double precision,
    description character varying(200),
    branch_code character varying(20),
    valuta_code character varying(20),
    rc_code character varying(20),
    generic_code character varying(20),
    fl_posting_account character varying(20),
    fl_project_no character varying(10),
    docoprstatus character varying(1),
    userid_create character varying(20),
    userid_last_modified character varying(20),
    journalitemstatus character varying(1),
    userid_posting character varying(20),
    userid_check character varying(20),
    dateposting timestamp(6) without time zone,
    datelastmod timestamp(6) without time zone,
    datecreate timestamp(6) without time zone,
    event_date timestamp(6) without time zone,
    journalitemtype character varying(1),
    kode_kurs character varying(20),
    nilai_kurs double precision,
    rpv_main integer,
    subsystemcode character varying(20),
    subaccountcode character varying(30),
    id_journalcreation integer,
    subaccountname character varying(100),
    accountinstance_id integer,
    id_journalblock integer,
    transaksirak_id integer,
    source_class_id character varying(32),
    source_key_id integer,
    additionaldescription character varying(200)
);


ALTER TABLE transaction.tmp_journalitem_bck OWNER TO postgres;

--
-- Name: tmp_mapping_repair_zakat; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_mapping_repair_zakat (
    accountno_old character varying(20) NOT NULL,
    accountno_new character varying(20),
    accountcode_old character varying(10),
    accountcode_new character varying(10),
    accountname_old character varying(100),
    accountname_new character varying(100),
    productid_old integer,
    productid_new integer,
    productname_old character varying(100),
    productname_new character varying(100)
);


ALTER TABLE transaction.tmp_mapping_repair_zakat OWNER TO postgres;

--
-- Name: tmp_mappingproduct1; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_mappingproduct1 (
    oldproductcode character varying(20) NOT NULL,
    oldaccountno character varying(30),
    oldaccountname character varying(50),
    programtype character varying(1),
    programcategory character varying(10),
    programproductid integer,
    fundentity integer NOT NULL,
    fundcategory character varying(1),
    transactionproductid integer,
    newproductcode character varying(20),
    newproductname character varying(50),
    newaccountno character varying(30),
    newtranproductid integer,
    newprogproductid integer
);


ALTER TABLE transaction.tmp_mappingproduct1 OWNER TO postgres;

--
-- Name: tmp_mappingtran_accountcode; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_mappingtran_accountcode (
    transactionitemid integer NOT NULL,
    account_code character varying(20)
);


ALTER TABLE transaction.tmp_mappingtran_accountcode OWNER TO postgres;

--
-- Name: tmp_mappingtran_accountcode2; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_mappingtran_accountcode2 (
    transactionitemid integer NOT NULL,
    account_code character varying(20)
);


ALTER TABLE transaction.tmp_mappingtran_accountcode2 OWNER TO postgres;

--
-- Name: tmp_newprogramname; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_newprogramname (
    productcode character varying(20),
    productname character varying(100),
    newproductname character varying(100)
);


ALTER TABLE transaction.tmp_newprogramname OWNER TO postgres;

--
-- Name: tmp_program; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_program (
    productid integer,
    transactionproductid integer,
    description character varying(200),
    productcode character varying(20),
    tranproductcode character varying(20),
    productname character varying(100),
    tranproductname character varying(60),
    accountno character varying(30),
    accountname character varying(50),
    balance numeric(38,2)
);


ALTER TABLE transaction.tmp_program OWNER TO postgres;

--
-- Name: tmp_repair_journalamil; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_repair_journalamil (
    journal_no character varying(30)
);


ALTER TABLE transaction.tmp_repair_journalamil OWNER TO postgres;

--
-- Name: tmp_repair_phpinfaq; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_repair_phpinfaq (
    actualdate timestamp(6) without time zone,
    transactionitemid integer,
    fundaccountno character varying(30),
    accountcode character varying(20)
);


ALTER TABLE transaction.tmp_repair_phpinfaq OWNER TO postgres;

--
-- Name: tmp_repair_porsiamilinfaq; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_repair_porsiamilinfaq (
    transactionitemid integer,
    fundaccountno character varying(30),
    accountcode character varying(20)
);


ALTER TABLE transaction.tmp_repair_porsiamilinfaq OWNER TO postgres;

--
-- Name: tmp_tranitem_repair_zakat2; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_tranitem_repair_zakat2 (
    transactionitemid integer,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE transaction.tmp_tranitem_repair_zakat2 OWNER TO postgres;

--
-- Name: tmp_tranitem_repair_zakat_bck1; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_tranitem_repair_zakat_bck1 (
    transactionitemid integer,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE transaction.tmp_tranitem_repair_zakat_bck1 OWNER TO postgres;

--
-- Name: tmp_transactiongroup; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_transactiongroup (
    donorid integer,
    fundentity integer,
    transactionid integer,
    transactionno character varying(30),
    transactionitemid integer,
    channelaccountno character varying(30),
    productaccountno character varying(30),
    journalno character varying(30),
    amount numeric(30,2),
    batchid integer
);


ALTER TABLE transaction.tmp_transactiongroup OWNER TO postgres;

--
-- Name: tmp_transactionitem_bck; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.tmp_transactionitem_bck (
    transactionitemid integer,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE transaction.tmp_transactionitem_bck OWNER TO postgres;

--
-- Name: transactionbatch; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transactionbatch (
    batchid integer NOT NULL,
    batchno character varying(30) DEFAULT NULL::character varying,
    batchdate timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    description character varying(100) DEFAULT NULL::character varying,
    branchcode character varying(10) DEFAULT NULL::character varying,
    inputer character varying(20) DEFAULT NULL::character varying,
    isclosed character varying(1) DEFAULT NULL::character varying,
    isposted character varying(1) DEFAULT NULL::character varying,
    batchtag character varying(5)
);


ALTER TABLE transaction.transactionbatch OWNER TO postgres;

--
-- Name: transactionitem_inject; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transactionitem_inject (
    transactionitemid integer,
    branchcode character varying(5),
    currencycode character varying(5),
    mutationtype character varying(1),
    amount numeric(38,2),
    rate double precision,
    ekuivalenamount double precision,
    transactionitemtype character varying(1),
    transactionid integer,
    parameterjournalid character varying(5),
    glnumber character varying(30),
    glname character varying(100),
    description character varying(100),
    refaccountno character varying(30),
    refaccountname character varying(100),
    accountcode character varying(20),
    rc_code character varying(10)
);


ALTER TABLE transaction.transactionitem_inject OWNER TO postgres;

--
-- Name: transactiontype; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transactiontype (
    transactioncode character varying(10) DEFAULT NULL::character varying NOT NULL,
    description character varying(60) DEFAULT NULL::character varying,
    vouchercode character varying(10)
);


ALTER TABLE transaction.transactiontype OWNER TO postgres;

--
-- Name: transaksirak; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transaksirak (
    debit double precision,
    credit double precision,
    cabangasal character varying(20) DEFAULT NULL::character varying,
    cabangtujuan character varying(20) DEFAULT NULL::character varying,
    jenistransaksirak character varying(1) DEFAULT NULL::character varying,
    transaksirak_id integer NOT NULL,
    keterangan character varying(50) DEFAULT NULL::character varying,
    statusterprosespusat character varying(1) DEFAULT NULL::character varying,
    transaksirakterkait_id integer,
    currency_code character varying(20) DEFAULT NULL::character varying,
    journal_no character varying(30) DEFAULT NULL::character varying,
    koderak character varying(30) DEFAULT NULL::character varying
);


ALTER TABLE transaction.transaksirak OWNER TO postgres;

--
-- Name: transhistoryofchanges; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transhistoryofchanges (
    historyid integer NOT NULL,
    transactionid integer,
    transactionno character varying(30),
    newtransactionno character varying(30),
    userid character varying(30),
    processtime timestamp without time zone,
    changetype character varying(1)
);


ALTER TABLE transaction.transhistoryofchanges OWNER TO postgres;

--
-- Name: transitemglinterface; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transitemglinterface (
    glinterfacecode character varying(20) NOT NULL,
    accountcode character varying(20),
    transactionitemid integer NOT NULL,
    description character varying(200)
);


ALTER TABLE transaction.transitemglinterface OWNER TO postgres;

--
-- Name: transrecongenlog; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.transrecongenlog (
    logid integer NOT NULL,
    banktransactionid integer,
    transactionid integer
);


ALTER TABLE transaction.transrecongenlog OWNER TO postgres;

--
-- Name: userapp; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.userapp AS
 SELECT id_user AS user_id,
    nama_user AS username,
    nolimitlocation,
    jumlah_login_aktif AS login_count,
    user_perbarui AS mod_user_id,
    tanggal_aktif_terakhir AS last_update,
    kode_cabang AS branch_code,
    id_user AS user_id1
   FROM enterprise.userapp;


ALTER VIEW transaction.userapp OWNER TO postgres;

--
-- Name: userapp_; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.userapp_ (
    user_id character varying(20) DEFAULT NULL::character varying NOT NULL,
    username character varying(30) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    nolimitlocation character varying(1) DEFAULT NULL::character varying,
    login_count integer,
    mod_user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    branch_code character varying(5) DEFAULT NULL::character varying,
    user_id1 character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.userapp_ OWNER TO postgres;

--
-- Name: userapp_old; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.userapp_old (
    user_id character varying(20) DEFAULT NULL::character varying NOT NULL,
    username character varying(30) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    nolimitlocation character varying(1) DEFAULT NULL::character varying,
    login_count integer,
    mod_user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone,
    branch_code character varying(5) DEFAULT NULL::character varying,
    user_id1 character varying(20) DEFAULT NULL::character varying
);


ALTER TABLE transaction.userapp_old OWNER TO postgres;

--
-- Name: usergroup; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.usergroup (
    group_id character varying(8) DEFAULT NULL::character varying NOT NULL,
    groupname character varying(30) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE transaction.usergroup OWNER TO postgres;

--
-- Name: usergroup_; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.usergroup_ (
    group_id character varying(8) DEFAULT NULL::character varying NOT NULL,
    groupname character varying(30) DEFAULT NULL::character varying,
    description character varying(50) DEFAULT NULL::character varying,
    user_id character varying(20) DEFAULT NULL::character varying,
    last_update timestamp(6) without time zone DEFAULT NULL::timestamp without time zone
);


ALTER TABLE transaction.usergroup_ OWNER TO postgres;

--
-- Name: usergroupapp; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.usergroupapp (
    user_id character varying(20) DEFAULT NULL::character varying NOT NULL,
    group_id character varying(8) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE transaction.usergroupapp OWNER TO postgres;

--
-- Name: usergroupapp_; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.usergroupapp_ (
    user_id character varying(20) DEFAULT NULL::character varying NOT NULL,
    group_id character varying(8) DEFAULT NULL::character varying NOT NULL
);


ALTER TABLE transaction.usergroupapp_ OWNER TO postgres;

--
-- Name: vbatchupload; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.vbatchupload AS
 SELECT b.batchid,
    b.accountno,
    b.transactionid,
    b.uploaduser,
    b.uploaddate,
    b.totalamount,
    b.batchuploadtype,
    b.branchcode,
    b.authorizeduser,
    b.description,
    b.totalrecord,
    f.accountname,
    c.bankaccountno,
    bn.bankname,
    bn.bankshortname
   FROM transaction.batchupload b,
    transaction.financialaccount f,
    (transaction.cashaccount c
     LEFT JOIN transaction.bank bn ON (((bn.bankcode)::text = (c.bankcode)::text)))
  WHERE (((b.accountno)::text = (f.accountno)::text) AND ((f.accountno)::text = (c.accountno)::text));


ALTER VIEW transaction.vbatchupload OWNER TO postgres;

--
-- Name: vdonor; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.vdonor AS
 SELECT donorname,
    addresskelurahan,
    addresssubdistrict,
    addresscity,
    addresspostalcode,
    phonenumber,
    fax,
    referenceby,
    status,
    donortype,
    addressstreet,
    addressstate,
    npwp,
    npwz,
    donorno,
    donorid,
    joindate,
    branchcode,
    idpropinsi,
    marketerid,
    addresskecamatan,
    idnegara,
    economicsector
   FROM fund.donor;


ALTER VIEW transaction.vdonor OWNER TO postgres;

--
-- Name: vemployee; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.vemployee AS
 SELECT employeeid,
    nama_lengkap AS namaemployee,
    alamat AS alamatlengkap,
    nomor_seluler AS nomorhp
   FROM enterprise.employee emp;


ALTER VIEW transaction.vemployee OWNER TO postgres;

--
-- Name: vemployeecashadvance; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.vemployeecashadvance AS
 SELECT employeeid,
    nama_lengkap AS employeename,
    email,
    alamat AS permanent_address,
    nomor_seluler AS current_phone_no,
    kode_cabang AS branchcode
   FROM enterprise.employee a
  WHERE (EXISTS ( SELECT 1
           FROM transaction.accountreceivable b
          WHERE ((a.employeeid = b.employeeidnumber) AND ((b.accountreceivabletype)::text = 'C'::text))));


ALTER VIEW transaction.vemployeecashadvance OWNER TO postgres;

--
-- Name: vendor; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.vendor (
    name character varying(40) DEFAULT NULL::character varying,
    address character varying(60) DEFAULT NULL::character varying,
    post_code character varying(5) DEFAULT NULL::character varying,
    tlp_no character varying(14) DEFAULT NULL::character varying,
    vendor_no integer NOT NULL
);


ALTER TABLE transaction.vendor OWNER TO postgres;

--
-- Name: volunteer; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.volunteer (
    volunteerid character varying(10) DEFAULT NULL::character varying NOT NULL,
    volunteername character varying(50) DEFAULT NULL::character varying,
    totalamount double precision,
    branchcode character varying(5) DEFAULT NULL::character varying,
    homeaddress character varying(150) DEFAULT NULL::character varying,
    homephone character varying(20) DEFAULT NULL::character varying,
    mobilephone character varying(20) DEFAULT NULL::character varying,
    email character varying(50) DEFAULT NULL::character varying
);


ALTER TABLE transaction.volunteer OWNER TO postgres;

--
-- Name: volunteertransaction; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.volunteertransaction (
    transactionitemid integer NOT NULL,
    volunteerid character varying(10) DEFAULT NULL::character varying
);


ALTER TABLE transaction.volunteertransaction OWNER TO postgres;

--
-- Name: vproduct; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.vproduct AS
 SELECT c.accountno,
    a.productid,
    (a.productcode)::character varying(30) AS productcode,
    a.productname,
    c.accountname,
    c.branchcode,
    a.producttype,
    a.status,
    c.currencycode,
    a.fundcategory,
    a.percentageofamilfunds,
    pg.productname AS groupname,
    (('1'::text || (a.productcode)::text))::character varying(40) AS idx
   FROM (((transaction.product a
     JOIN transaction.productaccount b ON ((a.productid = b.productid)))
     JOIN transaction.financialaccount c ON (((b.accountno)::text = (c.accountno)::text)))
     LEFT JOIN transaction.product pg ON ((pg.productid = a.parentproductid)))
  WHERE ((a.producttype)::text = ANY (ARRAY[('Z'::character varying)::text, ('C'::character varying)::text]))
UNION
 SELECT c.accountno,
    a.productid,
    (a.productcode)::character varying(30) AS productcode,
    a.productname,
    c.accountname,
    c.branchcode,
    a.producttype,
    a.status,
    c.currencycode,
    a.fundcategory,
    a.percentageofamilfunds,
    pg.productname AS groupname,
    (('2'::text || (a.productcode)::text))::character varying(40) AS idx
   FROM (((transaction.product a
     JOIN transaction.productaccount b ON ((a.productid = b.productid)))
     JOIN transaction.financialaccount c ON (((b.accountno)::text = (c.accountno)::text)))
     LEFT JOIN transaction.product pg ON ((pg.productid = a.parentproductid)))
  WHERE ((a.producttype)::text = 'G'::text)
UNION
 SELECT c.accountno,
    a.productid,
    c.accountno AS productcode,
    a.productname,
    c.accountname,
    c.branchcode,
    a.producttype,
    a.status,
    c.currencycode,
    a.fundcategory,
    a.percentageofamilfunds,
    pg.productname AS groupname,
    (('3'::text || (c.accountno)::text))::character varying(40) AS idx
   FROM (((transaction.product a
     JOIN transaction.productaccount b ON ((a.productid = b.productid)))
     JOIN transaction.financialaccount c ON (((b.accountno)::text = (c.accountno)::text)))
     LEFT JOIN transaction.product pg ON ((pg.productid = a.parentproductid)))
  WHERE (((a.producttype)::text = 'J'::text) AND ((c.status)::text = 'A'::text));


ALTER VIEW transaction.vproduct OWNER TO postgres;

--
-- Name: vprogrampartner; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.vprogrampartner AS
 SELECT p.partnerid,
    c.customername AS partnername,
    c.addressstreet AS partneraddress,
    c.customerstatus AS partnerstatus,
    p.branchcode
   FROM program.partner p,
    program.customer c
  WHERE (p.customerid = c.customerid);


ALTER VIEW transaction.vprogrampartner OWNER TO postgres;

--
-- Name: wakafcertificate; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.wakafcertificate (
    certificateid integer NOT NULL,
    certificatenumber character varying(30) DEFAULT NULL::character varying,
    donorid integer,
    transactionitemid integer,
    certificatedate timestamp without time zone,
    certificatedescription character varying(150)
);


ALTER TABLE transaction.wakafcertificate OWNER TO postgres;

--
-- Name: workarea; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.workarea (
    workareaid integer NOT NULL,
    workareacode character varying(10),
    workareaname character varying(100)
);


ALTER TABLE transaction.workarea OWNER TO postgres;

--
-- Name: workunit; Type: TABLE; Schema: transaction; Owner: postgres
--

CREATE TABLE transaction.workunit (
    workunitid integer NOT NULL,
    workunitcode character varying(10),
    workunitname character varying(100)
);


ALTER TABLE transaction.workunit OWNER TO postgres;

--
-- Name: zakahobject; Type: VIEW; Schema: transaction; Owner: postgres
--

CREATE VIEW transaction.zakahobject AS
 SELECT zakahobjectid,
    zakahobjectcode,
    zakahobjectname
   FROM fund.zakahobject;


ALTER VIEW transaction.zakahobject OWNER TO postgres;

--
-- Name: auth_group id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_group ALTER COLUMN id SET DEFAULT nextval('dashboard.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('dashboard.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_permission ALTER COLUMN id SET DEFAULT nextval('dashboard.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user ALTER COLUMN id SET DEFAULT nextval('dashboard.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('dashboard.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('dashboard.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.django_admin_log ALTER COLUMN id SET DEFAULT nextval('dashboard.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.django_content_type ALTER COLUMN id SET DEFAULT nextval('dashboard.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.django_migrations ALTER COLUMN id SET DEFAULT nextval('dashboard.django_migrations_id_seq'::regclass);


--
-- Name: inbox ID; Type: DEFAULT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.inbox ALTER COLUMN "ID" SET DEFAULT nextval('enterprise."inbox_ID_seq"'::regclass);


--
-- Name: outbox ID; Type: DEFAULT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.outbox ALTER COLUMN "ID" SET DEFAULT nextval('enterprise."outbox_ID_seq"'::regclass);


--
-- Name: outbox_multipart ID; Type: DEFAULT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.outbox_multipart ALTER COLUMN "ID" SET DEFAULT nextval('enterprise."outbox_multipart_ID_seq"'::regclass);


--
-- Name: pbk ID; Type: DEFAULT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.pbk ALTER COLUMN "ID" SET DEFAULT nextval('enterprise."pbk_ID_seq"'::regclass);


--
-- Name: pbk_groups ID; Type: DEFAULT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.pbk_groups ALTER COLUMN "ID" SET DEFAULT nextval('enterprise."pbk_groups_ID_seq"'::regclass);


--
-- Name: sentitems ID; Type: DEFAULT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.sentitems ALTER COLUMN "ID" SET DEFAULT nextval('enterprise."sentitems_ID_seq"'::regclass);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (account_code);


--
-- Name: accountdetail accountdetail_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountdetail
    ADD CONSTRAINT accountdetail_pkey PRIMARY KEY (fl_account, fl_detail_account);


--
-- Name: accountgroup accountgroup_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountgroup
    ADD CONSTRAINT accountgroup_pkey PRIMARY KEY (id);


--
-- Name: accounthierarchy accounthierarchy_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accounthierarchy
    ADD CONSTRAINT accounthierarchy_pkey PRIMARY KEY (accounthierarchy_id);


--
-- Name: accountingday accountingday_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountingday
    ADD CONSTRAINT accountingday_pkey PRIMARY KEY (periode_code, fl_accountingperiode, fl_accountingyear);


--
-- Name: accountingperiode accountingperiode_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountingperiode
    ADD CONSTRAINT accountingperiode_pkey PRIMARY KEY (fl_accountingyear, periode_code);


--
-- Name: accountingyear accountingyear_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountingyear
    ADD CONSTRAINT accountingyear_pkey PRIMARY KEY (periode_code);


--
-- Name: accountinstance accountinstance_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountinstance
    ADD CONSTRAINT accountinstance_pkey PRIMARY KEY (accountinstance_id);


--
-- Name: accountinterface accountinterface_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountinterface
    ADD CONSTRAINT accountinterface_pkey PRIMARY KEY (interface_code);


--
-- Name: accountinterfacemember accountinterfacemember_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountinterfacemember
    ADD CONSTRAINT accountinterfacemember_pkey PRIMARY KEY (member_id);


--
-- Name: accountmanager accountmanager_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accountmanager
    ADD CONSTRAINT accountmanager_pkey PRIMARY KEY (amcode);


--
-- Name: accsubsystem accsubsystem_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.accsubsystem
    ADD CONSTRAINT accsubsystem_pkey PRIMARY KEY (subsystemcode);


--
-- Name: blobregistration blobregistration_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.blobregistration
    ADD CONSTRAINT blobregistration_pkey PRIMARY KEY (id);


--
-- Name: branchlocation_old branchlocation_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.branchlocation_old
    ADD CONSTRAINT branchlocation_pkey PRIMARY KEY (branch_code);


--
-- Name: cashflowgroup cashflowgroup_key; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.cashflowgroup
    ADD CONSTRAINT cashflowgroup_key PRIMARY KEY (cfgroupid);


--
-- Name: cashflowmember cashflowmember_key; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.cashflowmember
    ADD CONSTRAINT cashflowmember_key PRIMARY KEY (cfmemberid);


--
-- Name: cpalpamapping cpalpamapping_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.cpalpamapping
    ADD CONSTRAINT cpalpamapping_pkey PRIMARY KEY (cpalpamapping_id);


--
-- Name: currency currency_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (currency_code);


--
-- Name: currency_pkpu currencyp_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.currency_pkpu
    ADD CONSTRAINT currencyp_pkey PRIMARY KEY (currency_code);


--
-- Name: custom_idgen custom_idgen_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.custom_idgen
    ADD CONSTRAINT custom_idgen_pkey PRIMARY KEY (idname, idcode);


--
-- Name: dailybalance dailybalance_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.dailybalance
    ADD CONSTRAINT dailybalance_pkey PRIMARY KEY (dailybalance_id);


--
-- Name: dailyprojectbalance dailyprojectbalance_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.dailyprojectbalance
    ADD CONSTRAINT dailyprojectbalance_pkey PRIMARY KEY (dailyprojectbalance_id);


--
-- Name: enum_int enum_int_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.enum_int
    ADD CONSTRAINT enum_int_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: enum_varchar enum_varchar_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.enum_varchar
    ADD CONSTRAINT enum_varchar_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: fact_daily_balance fact_daily_balance_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.fact_daily_balance
    ADD CONSTRAINT fact_daily_balance_pkey PRIMARY KEY (fact_id);


--
-- Name: hi_permil hi_permil_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.hi_permil
    ADD CONSTRAINT hi_permil_pkey PRIMARY KEY (id_hipermil);


--
-- Name: hipermildistribution hipermildistribution_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.hipermildistribution
    ADD CONSTRAINT hipermildistribution_pkey PRIMARY KEY (distribution_id, id_hipermil);


--
-- Name: id_gen id_gen_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.id_gen
    ADD CONSTRAINT id_gen_pkey PRIMARY KEY (id_code);


--
-- Name: intrnewtransaction intrnewtransaction_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.intrnewtransaction
    ADD CONSTRAINT intrnewtransaction_pkey PRIMARY KEY (subsysteminteraction_id);


--
-- Name: intrpicktransaction intrpicktransaction_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.intrpicktransaction
    ADD CONSTRAINT intrpicktransaction_pkey PRIMARY KEY (subsysteminteraction_id);


--
-- Name: jenisrak jenisrak_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.jenisrak
    ADD CONSTRAINT jenisrak_pkey PRIMARY KEY (koderak);


--
-- Name: journal journal_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.journal
    ADD CONSTRAINT journal_pkey PRIMARY KEY (journal_no);


--
-- Name: journalblock journalblock_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.journalblock
    ADD CONSTRAINT journalblock_pkey PRIMARY KEY (id_journalblock);


--
-- Name: journalcode journalcode_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.journalcode
    ADD CONSTRAINT journalcode_pkey PRIMARY KEY (journalcode_id);


--
-- Name: journaldeletion journaldeletion_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.journaldeletion
    ADD CONSTRAINT journaldeletion_pkey PRIMARY KEY (journal_no);


--
-- Name: journalitem journalitem_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.journalitem
    ADD CONSTRAINT journalitem_pkey PRIMARY KEY (fl_journal, journalitem_no);


--
-- Name: kurshistory kurshistory_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.kurshistory
    ADD CONSTRAINT kurshistory_pkey PRIMARY KEY (kurshistory_id);


--
-- Name: masterkurs masterkurs_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.masterkurs
    ADD CONSTRAINT masterkurs_pkey PRIMARY KEY (kode_kurs);


--
-- Name: parameter parameter_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.parameter
    ADD CONSTRAINT parameter_pkey PRIMARY KEY (parametercode);


--
-- Name: periodebalance periodebalance_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.periodebalance
    ADD CONSTRAINT periodebalance_pkey PRIMARY KEY (periodebalance_id);


--
-- Name: periodeprojectbalance periodeprojectbalance_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.periodeprojectbalance
    ADD CONSTRAINT periodeprojectbalance_pkey PRIMARY KEY (periodeprojectbalance_id);


--
-- Name: temptablenew pk_temptablenew; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.temptablenew
    ADD CONSTRAINT pk_temptablenew PRIMARY KEY (accountcode);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (project_no);


--
-- Name: rakcabang rakcabang_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.rakcabang
    ADD CONSTRAINT rakcabang_pkey PRIMARY KEY (rakcabang_id);


--
-- Name: rakpusat rakpusat_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.rakpusat
    ADD CONSTRAINT rakpusat_pkey PRIMARY KEY (rakpusat_id);


--
-- Name: registerkurs registerkurs_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.registerkurs
    ADD CONSTRAINT registerkurs_pkey PRIMARY KEY (registerkurs_id);


--
-- Name: revaluationhistory revaluationhistory_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.revaluationhistory
    ADD CONSTRAINT revaluationhistory_pkey PRIMARY KEY (history_id);


--
-- Name: rpvaccount rpvaccount_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.rpvaccount
    ADD CONSTRAINT rpvaccount_pkey PRIMARY KEY (rpv_name);


--
-- Name: rpvaccountdetail rpvaccountdetail_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.rpvaccountdetail
    ADD CONSTRAINT rpvaccountdetail_pkey PRIMARY KEY (currency_code, rpv_name, branch_code);


--
-- Name: sim_logrun sim_logrun_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.sim_logrun
    ADD CONSTRAINT sim_logrun_pkey PRIMARY KEY (logrun_id);


--
-- Name: subsysteminteraction subsysteminteraction_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.subsysteminteraction
    ADD CONSTRAINT subsysteminteraction_pkey PRIMARY KEY (subsysteminteraction_id);


--
-- Name: tempcandidatejournal tempcandidatejournal_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.tempcandidatejournal
    ADD CONSTRAINT tempcandidatejournal_pkey PRIMARY KEY (tempcandidatejournal_id);


--
-- Name: temptable_ori temptable_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.temptable_ori
    ADD CONSTRAINT temptable_pkey PRIMARY KEY (accountcode);


--
-- Name: transaksirak transaksirak_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.transaksirak
    ADD CONSTRAINT transaksirak_pkey PRIMARY KEY (transaksirak_id);


--
-- Name: userapp_old userapp_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.userapp_old
    ADD CONSTRAINT userapp_pkey PRIMARY KEY (user_id);


--
-- Name: usergroup usergroup_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.usergroup
    ADD CONSTRAINT usergroup_pkey PRIMARY KEY (group_id);


--
-- Name: usergroupapp usergroupapp_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.usergroupapp
    ADD CONSTRAINT usergroupapp_pkey PRIMARY KEY (user_id, group_id);


--
-- Name: vendor vendor_pkey; Type: CONSTRAINT; Schema: accounting; Owner: postgres
--

ALTER TABLE ONLY accounting.vendor
    ADD CONSTRAINT vendor_pkey PRIMARY KEY (vendor_no);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: dashboard; Owner: postgres
--

ALTER TABLE ONLY dashboard.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: aplikasi aplikasi_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.aplikasi
    ADD CONSTRAINT aplikasi_pkey PRIMARY KEY (kode_aplikasi);


--
-- Name: appsubsystem appsubsystem_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.appsubsystem
    ADD CONSTRAINT appsubsystem_pkey PRIMARY KEY (subsystem_code);


--
-- Name: areacabang areacabang_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.areacabang
    ADD CONSTRAINT areacabang_pkey PRIMARY KEY (kode_wilayah);


--
-- Name: bpparallelstep bpparallelstep_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpparallelstep
    ADD CONSTRAINT bpparallelstep_pkey PRIMARY KEY (parallel_step_id);


--
-- Name: bpparallelstepdetail bpparallelstepdetail_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpparallelstepdetail
    ADD CONSTRAINT bpparallelstepdetail_pkey PRIMARY KEY (pstep_detail_id);


--
-- Name: bpparallelstepinstance bpparallelstepinstance_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpparallelstepinstance
    ADD CONSTRAINT bpparallelstepinstance_pkey PRIMARY KEY (pstepinst_id);


--
-- Name: bpprocess bpprocess_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpprocess
    ADD CONSTRAINT bpprocess_pkey PRIMARY KEY (bpprocess_id);


--
-- Name: bpscenario bpscenario_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpscenario
    ADD CONSTRAINT bpscenario_pkey PRIMARY KEY (scenario_code);


--
-- Name: bpscenarioinstance bpscenarioinstance_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpscenarioinstance
    ADD CONSTRAINT bpscenarioinstance_pkey PRIMARY KEY (instance_id);


--
-- Name: bpscript bpscript_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpscript
    ADD CONSTRAINT bpscript_pkey PRIMARY KEY (script_id);


--
-- Name: bpstep bpstep_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpstep
    ADD CONSTRAINT bpstep_pkey PRIMARY KEY (step_id);


--
-- Name: bpstepinstance bpstepinstance_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.bpstepinstance
    ADD CONSTRAINT bpstepinstance_pkey PRIMARY KEY (stepinst_id);


--
-- Name: cabang cabang_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.cabang
    ADD CONSTRAINT cabang_pkey PRIMARY KEY (kode_cabang);


--
-- Name: cabangbmi cabangbmi_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.cabangbmi
    ADD CONSTRAINT cabangbmi_pkey PRIMARY KEY (id_cabang);


--
-- Name: custom_idgen custom_idgen_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.custom_idgen
    ADD CONSTRAINT custom_idgen_pkey PRIMARY KEY (idname, idcode);


--
-- Name: departemen departemen_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.departemen
    ADD CONSTRAINT departemen_pkey PRIMARY KEY (kode_departemen);


--
-- Name: enum_int enum_int_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.enum_int
    ADD CONSTRAINT enum_int_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: enum_varchar enum_varchar_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.enum_varchar
    ADD CONSTRAINT enum_varchar_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: executablefungsi executablefungsi_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.executablefungsi
    ADD CONSTRAINT executablefungsi_pkey PRIMARY KEY (id_fungsi);


--
-- Name: fungsi fungsi_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.fungsi
    ADD CONSTRAINT fungsi_pkey PRIMARY KEY (id_fungsi);


--
-- Name: glinterface glinterface_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.glinterface
    ADD CONSTRAINT glinterface_pkey PRIMARY KEY (id_interface);


--
-- Name: historikehadiran historikehadiran_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.historikehadiran
    ADD CONSTRAINT historikehadiran_pkey PRIMARY KEY (id_histori_kehadiran);


--
-- Name: id_gen id_gen_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.id_gen
    ADD CONSTRAINT id_gen_pkey PRIMARY KEY (id_code);


--
-- Name: inbox inbox_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.inbox
    ADD CONSTRAINT inbox_pkey PRIMARY KEY ("ID");


--
-- Name: inboxdeletedsms inboxdeletedsms_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.inboxdeletedsms
    ADD CONSTRAINT inboxdeletedsms_pkey PRIMARY KEY ("ID");


--
-- Name: inboxparameter inboxparameter_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.inboxparameter
    ADD CONSTRAINT inboxparameter_pkey PRIMARY KEY (parameter_code);


--
-- Name: jabatan jabatan_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.jabatan
    ADD CONSTRAINT jabatan_pkey PRIMARY KEY (kode_jabatan);


--
-- Name: kantor kantor_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.kantor
    ADD CONSTRAINT kantor_pkey PRIMARY KEY (kode_kantor);


--
-- Name: limitoperasi limitoperasi_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.limitoperasi
    ADD CONSTRAINT limitoperasi_pkey PRIMARY KEY (id_limit_operasi);


--
-- Name: limittransaksi limittransaksi_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.limittransaksi
    ADD CONSTRAINT limittransaksi_pkey PRIMARY KEY (id_limit_transaksi);


--
-- Name: listaplikasiperan listaplikasiperan_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.listaplikasiperan
    ADD CONSTRAINT listaplikasiperan_pkey PRIMARY KEY (kode_aplikasi, id_peran);


--
-- Name: listaplikasiuser listaplikasiuser_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.listaplikasiuser
    ADD CONSTRAINT listaplikasiuser_pkey PRIMARY KEY (id_listaplikasiuser);


--
-- Name: listcabangdiizinkan listcabangdiizinkan_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.listcabangdiizinkan
    ADD CONSTRAINT listcabangdiizinkan_pkey PRIMARY KEY (id_user, kode_cabang);


--
-- Name: listfungsiaplikasiperan listfungsiaplikasiperan_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.listfungsiaplikasiperan
    ADD CONSTRAINT listfungsiaplikasiperan_pkey PRIMARY KEY (kode_aplikasi, id_peran, id_fungsi);


--
-- Name: listfungsiaplikasiuser listfungsiaplikasiuser_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.listfungsiaplikasiuser
    ADD CONSTRAINT listfungsiaplikasiuser_pkey PRIMARY KEY (id_listfungsiaplikasiuser);


--
-- Name: listperanuser listperanuser_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.listperanuser
    ADD CONSTRAINT listperanuser_pkey PRIMARY KEY (id_peran, id_user);


--
-- Name: listterminaldiizinkan listterminaldiizinkan_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.listterminaldiizinkan
    ADD CONSTRAINT listterminaldiizinkan_pkey PRIMARY KEY (id_user, id_terminal);


--
-- Name: loginsession loginsession_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.loginsession
    ADD CONSTRAINT loginsession_pkey PRIMARY KEY (login_id);


--
-- Name: menu menu_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.menu
    ADD CONSTRAINT menu_pkey PRIMARY KEY (menu_id);


--
-- Name: menuhierarchy menuhierarchy_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.menuhierarchy
    ADD CONSTRAINT menuhierarchy_pkey PRIMARY KEY (hierarchy_id);


--
-- Name: otordata otordata_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.otordata
    ADD CONSTRAINT otordata_pkey PRIMARY KEY (id_data);


--
-- Name: otorentri otorentri_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.otorentri
    ADD CONSTRAINT otorentri_pkey PRIMARY KEY (id_otorisasi);


--
-- Name: otorentrihistori otorentrihistori_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.otorentrihistori
    ADD CONSTRAINT otorentrihistori_pkey PRIMARY KEY (id_otorisasi);


--
-- Name: otorparameter otorparameter_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.otorparameter
    ADD CONSTRAINT otorparameter_pkey PRIMARY KEY (kode_entri);


--
-- Name: otpkey otpkey_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.otpkey
    ADD CONSTRAINT otpkey_pkey PRIMARY KEY (userid);


--
-- Name: outbox_multipart outbox_multipart_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.outbox_multipart
    ADD CONSTRAINT outbox_multipart_pkey PRIMARY KEY ("ID", "SequencePosition");


--
-- Name: outbox outbox_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.outbox
    ADD CONSTRAINT outbox_pkey PRIMARY KEY ("ID");


--
-- Name: outboxdeleted outboxdeleted_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.outboxdeleted
    ADD CONSTRAINT outboxdeleted_pkey PRIMARY KEY ("ID");


--
-- Name: parameterglobal parameterglobal_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.parameterglobal
    ADD CONSTRAINT parameterglobal_pkey PRIMARY KEY (kode_parameter);


--
-- Name: pbk_groups pbk_groups_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.pbk_groups
    ADD CONSTRAINT pbk_groups_pkey PRIMARY KEY ("ID");


--
-- Name: pbk pbk_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.pbk
    ADD CONSTRAINT pbk_pkey PRIMARY KEY ("ID");


--
-- Name: peran peran_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.peran
    ADD CONSTRAINT peran_pkey PRIMARY KEY (id_peran);


--
-- Name: phones phones_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.phones
    ADD CONSTRAINT phones_pkey PRIMARY KEY ("IMEI");


--
-- Name: employee pk_empoyee; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.employee
    ADD CONSTRAINT pk_empoyee PRIMARY KEY (employeeid);


--
-- Name: publication publication_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.publication
    ADD CONSTRAINT publication_pkey PRIMARY KEY (publication_code);


--
-- Name: rolemenulist rolemenulist_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.rolemenulist
    ADD CONSTRAINT rolemenulist_pkey PRIMARY KEY (list_id);


--
-- Name: sentitems sentitems_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.sentitems
    ADD CONSTRAINT sentitems_pkey PRIMARY KEY ("ID", "SequencePosition");


--
-- Name: subscribeitem subscribeitem_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.subscribeitem
    ADD CONSTRAINT subscribeitem_pkey PRIMARY KEY (id_sitem);


--
-- Name: teller teller_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.teller
    ADD CONSTRAINT teller_pkey PRIMARY KEY (id_user);


--
-- Name: terminal terminal_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.terminal
    ADD CONSTRAINT terminal_pkey PRIMARY KEY (id_terminal);


--
-- Name: userapp userapp_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.userapp
    ADD CONSTRAINT userapp_pkey PRIMARY KEY (id_user);


--
-- Name: useraudit useraudit_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.useraudit
    ADD CONSTRAINT useraudit_pkey PRIMARY KEY (audit_id);


--
-- Name: usermenulist usermenulist_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.usermenulist
    ADD CONSTRAINT usermenulist_pkey PRIMARY KEY (list_id);


--
-- Name: usertbl usertbl_pkey; Type: CONSTRAINT; Schema: enterprise; Owner: postgres
--

ALTER TABLE ONLY enterprise.usertbl
    ADD CONSTRAINT usertbl_pkey PRIMARY KEY (userid);


--
-- Name: bankaccountlist bankaccountlist_pk; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.bankaccountlist
    ADD CONSTRAINT bankaccountlist_pk PRIMARY KEY (bankaccountid);


--
-- Name: batchuploadphone batchuploadphone_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.batchuploadphone
    ADD CONSTRAINT batchuploadphone_pkey PRIMARY KEY (id_batch);


--
-- Name: batchuploadphoneitem batchuploadphoneitem_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.batchuploadphoneitem
    ADD CONSTRAINT batchuploadphoneitem_pkey PRIMARY KEY (id_batch, workidentitynumber);


--
-- Name: bsz bsz_pk; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.bsz
    ADD CONSTRAINT bsz_pk PRIMARY KEY (bszid);


--
-- Name: bszdetail bszdetail_pk; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.bszdetail
    ADD CONSTRAINT bszdetail_pk PRIMARY KEY (bszdetailid);


--
-- Name: bsztransaction bsztransaction_pk; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.bsztransaction
    ADD CONSTRAINT bsztransaction_pk PRIMARY KEY (bsztransactionid);


--
-- Name: colltarget colltarget_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.colltarget
    ADD CONSTRAINT colltarget_pkey PRIMARY KEY (targetid);


--
-- Name: colltargetperiod colltargetperiod_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.colltargetperiod
    ADD CONSTRAINT colltargetperiod_pkey PRIMARY KEY (periodid);


--
-- Name: custom_idgen custom_idgen_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.custom_idgen
    ADD CONSTRAINT custom_idgen_pkey PRIMARY KEY (idname, idcode);


--
-- Name: donorbankaccount donorbankaccount_pk; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.donorbankaccount
    ADD CONSTRAINT donorbankaccount_pk PRIMARY KEY (bankaccountid);


--
-- Name: donorcommitment donorcommitment_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.donorcommitment
    ADD CONSTRAINT donorcommitment_pkey PRIMARY KEY (commitmentid);


--
-- Name: donorcommitmenthistory donorcommitmenthistory_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.donorcommitmenthistory
    ADD CONSTRAINT donorcommitmenthistory_pkey PRIMARY KEY (historyid);


--
-- Name: donorfieldhistory donorfieldhistory_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.donorfieldhistory
    ADD CONSTRAINT donorfieldhistory_pkey PRIMARY KEY (historyid);


--
-- Name: donorlevel donorlevel_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.donorlevel
    ADD CONSTRAINT donorlevel_pkey PRIMARY KEY (donorlevelid);


--
-- Name: donortotalfund donortotalfund_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.donortotalfund
    ADD CONSTRAINT donortotalfund_pkey PRIMARY KEY (totalfundid);


--
-- Name: emailbody emailbody_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.emailbody
    ADD CONSTRAINT emailbody_pkey PRIMARY KEY (emailbodyid);


--
-- Name: enum_int enum_int_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.enum_int
    ADD CONSTRAINT enum_int_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: enum_varchar enum_varchar_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.enum_varchar
    ADD CONSTRAINT enum_varchar_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: fieldofwork fwork_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.fieldofwork
    ADD CONSTRAINT fwork_pkey PRIMARY KEY (fworkid);


--
-- Name: id_gen id_gen_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.id_gen
    ADD CONSTRAINT id_gen_pkey PRIMARY KEY (id_code);


--
-- Name: senderemail key_senderemail; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.senderemail
    ADD CONSTRAINT key_senderemail PRIMARY KEY (idsenderemail);


--
-- Name: propinsi kode_unik; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.propinsi
    ADD CONSTRAINT kode_unik UNIQUE (kodepropinsi);


--
-- Name: marketertarget marketertarget_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.marketertarget
    ADD CONSTRAINT marketertarget_pkey PRIMARY KEY (targetid);


--
-- Name: negara negara_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.negara
    ADD CONSTRAINT negara_pkey PRIMARY KEY (idnegara);


--
-- Name: parameter parameter_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.parameter
    ADD CONSTRAINT parameter_pkey PRIMARY KEY (parametercode);


--
-- Name: parameterglobal parameterglobal_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.parameterglobal
    ADD CONSTRAINT parameterglobal_pkey PRIMARY KEY (kode_parameter);


--
-- Name: corporatedonor pk_corporatedonor; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.corporatedonor
    ADD CONSTRAINT pk_corporatedonor PRIMARY KEY (donorid);


--
-- Name: donor pk_donor; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.donor
    ADD CONSTRAINT pk_donor PRIMARY KEY (donorid);


--
-- Name: individualdonor pk_individualdonor; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.individualdonor
    ADD CONSTRAINT pk_individualdonor PRIMARY KEY (donorid);


--
-- Name: marketer pk_marketer; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.marketer
    ADD CONSTRAINT pk_marketer PRIMARY KEY (marketerid);


--
-- Name: propinsi propinsi_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.propinsi
    ADD CONSTRAINT propinsi_pkey PRIMARY KEY (idpropinsi);


--
-- Name: smslog smslog_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.smslog
    ADD CONSTRAINT smslog_pkey PRIMARY KEY (log_id);


--
-- Name: smslogdeleted smslogdeleted_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.smslogdeleted
    ADD CONSTRAINT smslogdeleted_pkey PRIMARY KEY (log_id);


--
-- Name: workarea workarea_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.workarea
    ADD CONSTRAINT workarea_pkey PRIMARY KEY (workareaid);


--
-- Name: workbusinessarea workbusinessarea_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.workbusinessarea
    ADD CONSTRAINT workbusinessarea_pkey PRIMARY KEY (workbusinessareaid);


--
-- Name: workposition workposition_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.workposition
    ADD CONSTRAINT workposition_pkey PRIMARY KEY (workpositionid);


--
-- Name: workunit workunit_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.workunit
    ADD CONSTRAINT workunit_pkey PRIMARY KEY (workunitid);


--
-- Name: zakahobject zakahobject_pkey; Type: CONSTRAINT; Schema: fund; Owner: postgres
--

ALTER TABLE ONLY fund.zakahobject
    ADD CONSTRAINT zakahobject_pkey PRIMARY KEY (zakahobjectid);


--
-- Name: bankaccount_convert bankaccount_convert_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.bankaccount_convert
    ADD CONSTRAINT bankaccount_convert_pkey PRIMARY KEY (accountno_bank);


--
-- Name: coaconv_assetwakaf coaconv_assetwakaf_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.coaconv_assetwakaf
    ADD CONSTRAINT coaconv_assetwakaf_pkey PRIMARY KEY (assetregnumber);


--
-- Name: coaconv_bankremove coaconv_bankremove_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.coaconv_bankremove
    ADD CONSTRAINT coaconv_bankremove_pkey PRIMARY KEY (accountno_bank);


--
-- Name: coaconv_bankwakaf coaconv_bankwakaf_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.coaconv_bankwakaf
    ADD CONSTRAINT coaconv_bankwakaf_pkey PRIMARY KEY (accountno_bank);


--
-- Name: enum_varchar enum_varchar_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.enum_varchar
    ADD CONSTRAINT enum_varchar_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: financialaccount_migbalance financialaccount_migbalance_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.financialaccount_migbalance
    ADD CONSTRAINT financialaccount_migbalance_pkey PRIMARY KEY (accountno);


--
-- Name: script_collection script_collection_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.script_collection
    ADD CONSTRAINT script_collection_pkey PRIMARY KEY (script_code);


--
-- Name: tmp_bankcash tmp_bankcash_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.tmp_bankcash
    ADD CONSTRAINT tmp_bankcash_pkey PRIMARY KEY (accountno, id_batch);


--
-- Name: tmp_donorinactivated tmp_donorinactivated_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.tmp_donorinactivated
    ADD CONSTRAINT tmp_donorinactivated_pkey PRIMARY KEY (id_batch, donorid);


--
-- Name: tmp_journal_candidate tmp_journal_candidate_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.tmp_journal_candidate
    ADD CONSTRAINT tmp_journal_candidate_pkey PRIMARY KEY (id_batch, journal_no);


--
-- Name: tmp_journalitem_history tmp_journalitem_history_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.tmp_journalitem_history
    ADD CONSTRAINT tmp_journalitem_history_pkey PRIMARY KEY (id_batch, baris);


--
-- Name: tmp_neracasaldo_nonmapping tmp_neracasaldo_nonmapping_pkey; Type: CONSTRAINT; Schema: migration; Owner: postgres
--

ALTER TABLE ONLY migration.tmp_neracasaldo_nonmapping
    ADD CONSTRAINT tmp_neracasaldo_nonmapping_pkey PRIMARY KEY (account_code, branch_code, id_batch);


--
-- Name: inventorytransactionitem Invtransitem_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.inventorytransactionitem
    ADD CONSTRAINT "Invtransitem_pkey" PRIMARY KEY (transactionitemid);


--
-- Name: achievement achievement_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.achievement
    ADD CONSTRAINT achievement_pkey PRIMARY KEY (achievementid);


--
-- Name: assettransaction assettransaction_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.assettransaction
    ADD CONSTRAINT assettransaction_pkey PRIMARY KEY (transactionid);


--
-- Name: assettransactionitem assettransactionitem_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.assettransactionitem
    ADD CONSTRAINT assettransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: attendance attendance_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.attendance
    ADD CONSTRAINT attendance_pkey PRIMARY KEY (attendanceid);


--
-- Name: attendancesymbols attendancesymbols_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.attendancesymbols
    ADD CONSTRAINT attendancesymbols_pkey PRIMARY KEY (attendancesymbol);


--
-- Name: blobregistration blobregistration_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.blobregistration
    ADD CONSTRAINT blobregistration_pkey PRIMARY KEY (id);


--
-- Name: branch branch_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.branch
    ADD CONSTRAINT branch_pkey PRIMARY KEY (branchcode);


--
-- Name: branchlocation branchlocation_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.branchlocation
    ADD CONSTRAINT branchlocation_pkey PRIMARY KEY (branch_code);


--
-- Name: careerhistory careerhistory_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.careerhistory
    ADD CONSTRAINT careerhistory_pkey PRIMARY KEY (careerhistoryid);


--
-- Name: contracthistory contracthistory_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.contracthistory
    ADD CONSTRAINT contracthistory_pkey PRIMARY KEY (contractno);


--
-- Name: custom_idgen custom_idgen_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.custom_idgen
    ADD CONSTRAINT custom_idgen_pkey PRIMARY KEY (idname, idcode);


--
-- Name: depreciationprocesslog depreciationprocesslog_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.depreciationprocesslog
    ADD CONSTRAINT depreciationprocesslog_pkey PRIMARY KEY (processid);


--
-- Name: disposisi disposisi_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.disposisi
    ADD CONSTRAINT disposisi_pkey PRIMARY KEY (disposisiid);


--
-- Name: dokumen dokumen_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.dokumen
    ADD CONSTRAINT dokumen_pkey PRIMARY KEY (dokumenid);


--
-- Name: dokumenkeluar dokumenkeluar_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.dokumenkeluar
    ADD CONSTRAINT dokumenkeluar_pkey PRIMARY KEY (dokumenid);


--
-- Name: dokumenmasuk dokumenmasuk_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.dokumenmasuk
    ADD CONSTRAINT dokumenmasuk_pkey PRIMARY KEY (dokumenid);


--
-- Name: education education_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.education
    ADD CONSTRAINT education_pkey PRIMARY KEY (educationid);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employeeid);


--
-- Name: employeeactivehistory employeeactivehistory_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.employeeactivehistory
    ADD CONSTRAINT employeeactivehistory_pkey PRIMARY KEY (historyid);


--
-- Name: employeedevelopmentprogram employeedevelopmentprogram_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.employeedevelopmentprogram
    ADD CONSTRAINT employeedevelopmentprogram_pkey PRIMARY KEY (edpid);


--
-- Name: employeetraining employeetraining_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.employeetraining
    ADD CONSTRAINT employeetraining_pkey PRIMARY KEY (trainingid);


--
-- Name: enum_int enum_int_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.enum_int
    ADD CONSTRAINT enum_int_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: enum_varchar enum_varchar_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.enum_varchar
    ADD CONSTRAINT enum_varchar_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: externalcontact externalcontact_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.externalcontact
    ADD CONSTRAINT externalcontact_pkey PRIMARY KEY (extcontactid);


--
-- Name: externalorganization externalorganization_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.externalorganization
    ADD CONSTRAINT externalorganization_pkey PRIMARY KEY (extorgid);


--
-- Name: family family_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.family
    ADD CONSTRAINT family_pkey PRIMARY KEY (familyid);


--
-- Name: fixedasset fixedasset_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.fixedasset
    ADD CONSTRAINT fixedasset_pkey PRIMARY KEY (deprassetid);


--
-- Name: fixedassettype fixedassettype_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.fixedassettype
    ADD CONSTRAINT fixedassettype_pkey PRIMARY KEY (fatypeid);


--
-- Name: formaleducation formaleducation_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.formaleducation
    ADD CONSTRAINT formaleducation_pkey PRIMARY KEY (educationid);


--
-- Name: glinterfacecontainer glinterfacecontainer_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.glinterfacecontainer
    ADD CONSTRAINT glinterfacecontainer_pkey PRIMARY KEY (glicontainerid);


--
-- Name: glinterfacemember glinterfacemember_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.glinterfacemember
    ADD CONSTRAINT glinterfacemember_pkey PRIMARY KEY (glimemberid);


--
-- Name: healthplafond healthplafond_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.healthplafond
    ADD CONSTRAINT healthplafond_pkey PRIMARY KEY (employeeid);


--
-- Name: healthreimbursement healthreimbursement_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.healthreimbursement
    ADD CONSTRAINT healthreimbursement_pkey PRIMARY KEY (rank, reimbursementtype, maritalstatus);


--
-- Name: id_gen id_gen_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.id_gen
    ADD CONSTRAINT id_gen_pkey PRIMARY KEY (id_code);


--
-- Name: individu individu_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.individu
    ADD CONSTRAINT individu_pkey PRIMARY KEY (individuid);


--
-- Name: innormalinvtransactitem innormalinvtransactitem_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.innormalinvtransactitem
    ADD CONSTRAINT innormalinvtransactitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: inventory inventory_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.inventory
    ADD CONSTRAINT inventory_pkey PRIMARY KEY (invid);


--
-- Name: inventorystock inventorystock_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.inventorystock
    ADD CONSTRAINT inventorystock_pkey PRIMARY KEY (invstockid);


--
-- Name: inventorytransaction inventorytransaction_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.inventorytransaction
    ADD CONSTRAINT inventorytransaction_pkey PRIMARY KEY (transactionid);


--
-- Name: normalinvtransactitem inventorytransactionitem_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.normalinvtransactitem
    ADD CONSTRAINT inventorytransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: inventoryunit inventoryunit_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.inventoryunit
    ADD CONSTRAINT inventoryunit_pkey PRIMARY KEY (invunitid);


--
-- Name: invreceivetransaction invreceivetransaction_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.invreceivetransaction
    ADD CONSTRAINT invreceivetransaction_pkey PRIMARY KEY (transactionid);


--
-- Name: islamorganization islamorganization_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.islamorganization
    ADD CONSTRAINT islamorganization_pkey PRIMARY KEY (extorgid);


--
-- Name: islamorgcontactperson islamorgcontactperson_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.islamorgcontactperson
    ADD CONSTRAINT islamorgcontactperson_pkey PRIMARY KEY (extcontactid);


--
-- Name: jenisdokumen jenisdokumen_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.jenisdokumen
    ADD CONSTRAINT jenisdokumen_pkey PRIMARY KEY (idjenisdokumen);


--
-- Name: journalist journalist_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.journalist
    ADD CONSTRAINT journalist_pkey PRIMARY KEY (extcontactid);


--
-- Name: regionarea key_regionarea; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.regionarea
    ADD CONSTRAINT key_regionarea PRIMARY KEY (regionareaid);


--
-- Name: logincorporate logincorporate_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.logincorporate
    ADD CONSTRAINT logincorporate_pkey PRIMARY KEY (login);


--
-- Name: newsagency newsagency_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.newsagency
    ADD CONSTRAINT newsagency_pkey PRIMARY KEY (extorgid);


--
-- Name: nonformaleducation nonformaleducation_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.nonformaleducation
    ADD CONSTRAINT nonformaleducation_pkey PRIMARY KEY (educationid);


--
-- Name: normalinventory normalinventory_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.normalinventory
    ADD CONSTRAINT normalinventory_pkey PRIMARY KEY (invid);


--
-- Name: normalinvreceive normalinvreceive_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.normalinvreceive
    ADD CONSTRAINT normalinvreceive_pkey PRIMARY KEY (transactionitemid);


--
-- Name: normalinvretur normalinvretur_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.normalinvretur
    ADD CONSTRAINT normalinvretur_pkey PRIMARY KEY (transactionitemid);


--
-- Name: offwork offwork_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.offwork
    ADD CONSTRAINT offwork_pkey PRIMARY KEY (offworkid);


--
-- Name: offworkmaternity offworkmaternity_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.offworkmaternity
    ADD CONSTRAINT offworkmaternity_pkey PRIMARY KEY (offworkid);


--
-- Name: offworkpermit offworkpermit_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.offworkpermit
    ADD CONSTRAINT offworkpermit_pkey PRIMARY KEY (offworkid);


--
-- Name: offworkplafond offworkplafond_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.offworkplafond
    ADD CONSTRAINT offworkplafond_pkey PRIMARY KEY (employeeid);


--
-- Name: offworkregular offworkregular_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.offworkregular
    ADD CONSTRAINT offworkregular_pkey PRIMARY KEY (offworkid);


--
-- Name: organizationexperience organizationexperience_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.organizationexperience
    ADD CONSTRAINT organizationexperience_pkey PRIMARY KEY (organizationexperienceid);


--
-- Name: outnormalinvtransactitem outnormalinvtransactitem_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.outnormalinvtransactitem
    ADD CONSTRAINT outnormalinvtransactitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: regionrepresentation p_keyregionrepresentation; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.regionrepresentation
    ADD CONSTRAINT p_keyregionrepresentation PRIMARY KEY (regionrepresentionid);


--
-- Name: parameterglobal parameterglobal_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.parameterglobal
    ADD CONSTRAINT parameterglobal_pkey PRIMARY KEY (kode_parameter);


--
-- Name: parameterjournal parameterjournal_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.parameterjournal
    ADD CONSTRAINT parameterjournal_pkey PRIMARY KEY (parameterjournalid);


--
-- Name: parameterjournalitem parameterjournalitem_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.parameterjournalitem
    ADD CONSTRAINT parameterjournalitem_pkey PRIMARY KEY (parameterjournalitemid);


--
-- Name: performanceappraisal performanceappraisal_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.performanceappraisal
    ADD CONSTRAINT performanceappraisal_pkey PRIMARY KEY (performanceappraisalid);


--
-- Name: performanceitem performanceitem_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.performanceitem
    ADD CONSTRAINT performanceitem_pkey PRIMARY KEY (performanceitemid);


--
-- Name: performanceparameter performanceparameter_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.performanceparameter
    ADD CONSTRAINT performanceparameter_pkey PRIMARY KEY (parameterid);


--
-- Name: performanceworkunitparameter performanceworkunitparameter_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.performanceworkunitparameter
    ADD CONSTRAINT performanceworkunitparameter_pkey PRIMARY KEY (workunitid, parameterid);


--
-- Name: position position_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia."position"
    ADD CONSTRAINT position_pkey PRIMARY KEY (positionid);


--
-- Name: rankhistory rankhistory_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.rankhistory
    ADD CONSTRAINT rankhistory_pkey PRIMARY KEY (rankhistoryid);


--
-- Name: reimbursementrealization reimbursementrealization_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.reimbursementrealization
    ADD CONSTRAINT reimbursementrealization_pkey PRIMARY KEY (reimbursementrealizationid);


--
-- Name: salaryhistory salaryhistory_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.salaryhistory
    ADD CONSTRAINT salaryhistory_pkey PRIMARY KEY (salaryhistoryid);


--
-- Name: salaryitemhistory salaryitemhistory_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.salaryitemhistory
    ADD CONSTRAINT salaryitemhistory_pkey PRIMARY KEY (salaryitemid);


--
-- Name: salaryitemparameter salaryitemparameter_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.salaryitemparameter
    ADD CONSTRAINT salaryitemparameter_pkey PRIMARY KEY (salaryitemparameterid);


--
-- Name: salaryitemparametergroup salaryitemparametergroup_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.salaryitemparametergroup
    ADD CONSTRAINT salaryitemparametergroup_pkey PRIMARY KEY (parametergroupid);


--
-- Name: salaryitemscheme salaryitemscheme_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.salaryitemscheme
    ADD CONSTRAINT salaryitemscheme_pkey PRIMARY KEY (salaryitemschemeid);


--
-- Name: salaryscheme salaryscheme_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.salaryscheme
    ADD CONSTRAINT salaryscheme_pkey PRIMARY KEY (salaryschemeid);


--
-- Name: sessionblob sessionblob_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.sessionblob
    ADD CONSTRAINT sessionblob_pkey PRIMARY KEY (id);


--
-- Name: targetachievement targetachievement_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.targetachievement
    ADD CONSTRAINT targetachievement_pkey PRIMARY KEY (targetachievementid);


--
-- Name: training training_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.training
    ADD CONSTRAINT training_pkey PRIMARY KEY (trainingid);


--
-- Name: trainingseminar trainingseminar_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.trainingseminar
    ADD CONSTRAINT trainingseminar_pkey PRIMARY KEY (trainingid);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (transactionid);


--
-- Name: transactionitem transactionitem_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.transactionitem
    ADD CONSTRAINT transactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: workexperience workexperience_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.workexperience
    ADD CONSTRAINT workexperience_pkey PRIMARY KEY (workexperienceid);


--
-- Name: workunit workunit_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.workunit
    ADD CONSTRAINT workunit_pkey PRIMARY KEY (workunitid);


--
-- Name: workunitposition workunitposition_pkey; Type: CONSTRAINT; Schema: personalia; Owner: postgres
--

ALTER TABLE ONLY personalia.workunitposition
    ADD CONSTRAINT workunitposition_pkey PRIMARY KEY (workunitid, positionid);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (account_code);


--
-- Name: accounttransactionitem accounttransactionitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.accounttransactionitem
    ADD CONSTRAINT accounttransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: activityappraisal activityappraisal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.activityappraisal
    ADD CONSTRAINT activityappraisal_pkey PRIMARY KEY (activityappraisalid);


--
-- Name: activityappraisalitem activityappraisalitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.activityappraisalitem
    ADD CONSTRAINT activityappraisalitem_pkey PRIMARY KEY (itemid);


--
-- Name: activityappraisalitemtemplate activityappraisalitemtemplate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.activityappraisalitemtemplate
    ADD CONSTRAINT activityappraisalitemtemplate_pkey PRIMARY KEY (itemtemplateid);


--
-- Name: agenda agenda_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.agenda
    ADD CONSTRAINT agenda_pkey PRIMARY KEY (agendaid);


--
-- Name: agendaitem agendaitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.agendaitem
    ADD CONSTRAINT agendaitem_pkey PRIMARY KEY (agendaitemid);


--
-- Name: agendaitemtemplate agendaitemtemplate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.agendaitemtemplate
    ADD CONSTRAINT agendaitemtemplate_pkey PRIMARY KEY (agendaitemtemplateid);


--
-- Name: agendatemplate agendatemplate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.agendatemplate
    ADD CONSTRAINT agendatemplate_pkey PRIMARY KEY (agendatemplateid);


--
-- Name: appraisal appraisal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.appraisal
    ADD CONSTRAINT appraisal_pkey PRIMARY KEY (appraisalid);


--
-- Name: appraisalitem appraisalitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.appraisalitem
    ADD CONSTRAINT appraisalitem_pkey PRIMARY KEY (itemid);


--
-- Name: appraisalitemgroup appraisalitemgroup_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.appraisalitemgroup
    ADD CONSTRAINT appraisalitemgroup_pkey PRIMARY KEY (groupname);


--
-- Name: appraisalitemtemplate appraisalitemtemplate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.appraisalitemtemplate
    ADD CONSTRAINT appraisalitemtemplate_pkey PRIMARY KEY (itemtemplateid);


--
-- Name: appraisaltemplate appraisaltemplate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.appraisaltemplate
    ADD CONSTRAINT appraisaltemplate_pkey PRIMARY KEY (appraisaltemplateid);


--
-- Name: aqhpropose aqhpropose_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.aqhpropose
    ADD CONSTRAINT aqhpropose_pkey PRIMARY KEY (aqhproposeid);


--
-- Name: assetcategory assetcategory_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.assetcategory
    ADD CONSTRAINT assetcategory_pkey PRIMARY KEY (assetcategoryid);


--
-- Name: balancepartition balancepartition_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.balancepartition
    ADD CONSTRAINT balancepartition_pkey PRIMARY KEY (balancepartitionid);


--
-- Name: bank bank_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.bank
    ADD CONSTRAINT bank_pkey PRIMARY KEY (bankcode);


--
-- Name: bankaccountlist bankaccountlist_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.bankaccountlist
    ADD CONSTRAINT bankaccountlist_pkey PRIMARY KEY (bankaccountid);


--
-- Name: blobregistration blobregistration_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.blobregistration
    ADD CONSTRAINT blobregistration_pkey PRIMARY KEY (id);


--
-- Name: branch branch_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.branch
    ADD CONSTRAINT branch_pkey PRIMARY KEY (branchcode);


--
-- Name: branchbankpic branchbankpic_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.branchbankpic
    ADD CONSTRAINT branchbankpic_pkey PRIMARY KEY (branchcode);


--
-- Name: branchlocation branchlocation_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.branchlocation
    ADD CONSTRAINT branchlocation_pkey PRIMARY KEY (branch_code);


--
-- Name: cashadvancereturninfo cashadvancereturninfo_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.cashadvancereturninfo
    ADD CONSTRAINT cashadvancereturninfo_pkey PRIMARY KEY (sourcetransactionid);


--
-- Name: claimitem claimitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.claimitem
    ADD CONSTRAINT claimitem_pkey PRIMARY KEY (claimitemid);


--
-- Name: claimtransactiondetailqurban claimtransactiondetailqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.claimtransactiondetailqurban
    ADD CONSTRAINT claimtransactiondetailqurban_pkey PRIMARY KEY (claimtransactiondetailqurbanid);


--
-- Name: claimtransactionqurban claimtransactionqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.claimtransactionqurban
    ADD CONSTRAINT claimtransactionqurban_pkey PRIMARY KEY (claimtransactionqurbanid);


--
-- Name: companion companion_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.companion
    ADD CONSTRAINT companion_pkey PRIMARY KEY (companionid);


--
-- Name: companioncontract companioncontract_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.companioncontract
    ADD CONSTRAINT companioncontract_pkey PRIMARY KEY (contractno);


--
-- Name: companionliabilityaccount companionliabilityaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.companionliabilityaccount
    ADD CONSTRAINT companionliabilityaccount_pkey PRIMARY KEY (accountno);


--
-- Name: companionpersonalkum3 companionpersonalkum3_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.companionpersonalkum3
    ADD CONSTRAINT companionpersonalkum3_pkey PRIMARY KEY (customerid);


--
-- Name: companionproduct companionproduct_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.companionproduct
    ADD CONSTRAINT companionproduct_pkey PRIMARY KEY (productid, companionid);


--
-- Name: companionvisit companionvisit_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.companionvisit
    ADD CONSTRAINT companionvisit_pkey PRIMARY KEY (companionvisitid);


--
-- Name: companionvisititem companionvisititem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.companionvisititem
    ADD CONSTRAINT companionvisititem_pkey PRIMARY KEY (itemid);


--
-- Name: companionvisititemtemplate companionvisititemtemplate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.companionvisititemtemplate
    ADD CONSTRAINT companionvisititemtemplate_pkey PRIMARY KEY (itemtemplateid);


--
-- Name: corporatedonor corporatedonor_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.corporatedonor
    ADD CONSTRAINT corporatedonor_pkey PRIMARY KEY (donorid);


--
-- Name: costitem costitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.costitem
    ADD CONSTRAINT costitem_pkey PRIMARY KEY (costitemid);


--
-- Name: currency currency_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (currency_code);


--
-- Name: custom_idgen custom_idgen_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.custom_idgen
    ADD CONSTRAINT custom_idgen_pkey PRIMARY KEY (idname, idcode);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (customerid);


--
-- Name: customercorporate customercorporate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.customercorporate
    ADD CONSTRAINT customercorporate_pkey PRIMARY KEY (customerid);


--
-- Name: customerorphan customerorphan_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.customerorphan
    ADD CONSTRAINT customerorphan_pkey PRIMARY KEY (customerid);


--
-- Name: customerpersonal customerpersonal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.customerpersonal
    ADD CONSTRAINT customerpersonal_pkey PRIMARY KEY (customerid);


--
-- Name: daerahdistribusi daerahdistribusi_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.daerahdistribusi
    ADD CONSTRAINT daerahdistribusi_pkey PRIMARY KEY (namalokasi);


--
-- Name: detailklaimtransaksiproject detailklaimtransaksiproject_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.detailklaimtransaksiproject
    ADD CONSTRAINT detailklaimtransaksiproject_pkey PRIMARY KEY (detailklaimid);


--
-- Name: disease disease_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.disease
    ADD CONSTRAINT disease_pkey PRIMARY KEY (diseasecode);


--
-- Name: diseasediagnosed diseasediagnosed_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.diseasediagnosed
    ADD CONSTRAINT diseasediagnosed_pkey PRIMARY KEY (diseasediagnosedid);


--
-- Name: donor donor_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.donor
    ADD CONSTRAINT donor_pkey PRIMARY KEY (donorid);


--
-- Name: donorbankaccount donorbankaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.donorbankaccount
    ADD CONSTRAINT donorbankaccount_pkey PRIMARY KEY (bankaccountid);


--
-- Name: donorliabilityaccount donorliabilityaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.donorliabilityaccount
    ADD CONSTRAINT donorliabilityaccount_pkey PRIMARY KEY (accountno);


--
-- Name: donormember donormember_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.donormember
    ADD CONSTRAINT donormember_pkey PRIMARY KEY (donorid, customerid);


--
-- Name: donorpersonal donorpersonal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.donorpersonal
    ADD CONSTRAINT donorpersonal_pkey PRIMARY KEY (donorid);


--
-- Name: donorproduct donorproduct_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.donorproduct
    ADD CONSTRAINT donorproduct_pkey PRIMARY KEY (donorid, productid);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employeeid);


--
-- Name: enum_int enum_int_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.enum_int
    ADD CONSTRAINT enum_int_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: enum_varchar enum_varchar_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.enum_varchar
    ADD CONSTRAINT enum_varchar_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: event event_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.event
    ADD CONSTRAINT event_pkey PRIMARY KEY (eventid);


--
-- Name: eventattendance eventattendance_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.eventattendance
    ADD CONSTRAINT eventattendance_pkey PRIMARY KEY (eventattendanceid);


--
-- Name: eventksm eventksm_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.eventksm
    ADD CONSTRAINT eventksm_pkey PRIMARY KEY (eventid);


--
-- Name: eventplan eventplan_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.eventplan
    ADD CONSTRAINT eventplan_pkey PRIMARY KEY (eventplanid);


--
-- Name: eventplanattendance eventplanattendance_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.eventplanattendance
    ADD CONSTRAINT eventplanattendance_pkey PRIMARY KEY (eventplanattendanceid);


--
-- Name: eventplanksm eventplanksm_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.eventplanksm
    ADD CONSTRAINT eventplanksm_pkey PRIMARY KEY (eventplanid);


--
-- Name: externaldebtor externaldebtor_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.externaldebtor
    ADD CONSTRAINT externaldebtor_pkey PRIMARY KEY (debtorid);


--
-- Name: financialaccount financialaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.financialaccount
    ADD CONSTRAINT financialaccount_pkey PRIMARY KEY (accountno);


--
-- Name: financingaccount financingaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.financingaccount
    ADD CONSTRAINT financingaccount_pkey PRIMARY KEY (accountno);


--
-- Name: financingtransactionitem financingtransactionitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.financingtransactionitem
    ADD CONSTRAINT financingtransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: glinterface glinterface_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.glinterface
    ADD CONSTRAINT glinterface_pkey PRIMARY KEY (interfaceid);


--
-- Name: glinterfacecontainer glinterfacecontainer_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.glinterfacecontainer
    ADD CONSTRAINT glinterfacecontainer_pkey PRIMARY KEY (glicontainerid);


--
-- Name: glinterfacemember glinterfacemember_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.glinterfacemember
    ADD CONSTRAINT glinterfacemember_pkey PRIMARY KEY (glimemberid);


--
-- Name: healthliabilitytransactionitem healthliabilitytransactionitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.healthliabilitytransactionitem
    ADD CONSTRAINT healthliabilitytransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: historyofchanges historyofchanges_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.historyofchanges
    ADD CONSTRAINT historyofchanges_pkey PRIMARY KEY (historyid);


--
-- Name: id_gen id_gen_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.id_gen
    ADD CONSTRAINT id_gen_pkey PRIMARY KEY (id_code);


--
-- Name: inbox inbox_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.inbox
    ADD CONSTRAINT inbox_pkey PRIMARY KEY (inboxid);


--
-- Name: inboxhistory inboxhistory_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.inboxhistory
    ADD CONSTRAINT inboxhistory_pkey PRIMARY KEY (inboxhistoryid);


--
-- Name: inboxtransaction inboxtransaction_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.inboxtransaction
    ADD CONSTRAINT inboxtransaction_pkey PRIMARY KEY (inboxid);


--
-- Name: individualdonor individualdonor_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.individualdonor
    ADD CONSTRAINT individualdonor_pkey PRIMARY KEY (donorid);


--
-- Name: itemuploadedstatement itemuploadedstatement_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.itemuploadedstatement
    ADD CONSTRAINT itemuploadedstatement_pkey PRIMARY KEY (itemstatementid);


--
-- Name: kjks kjks_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.kjks
    ADD CONSTRAINT kjks_pkey PRIMARY KEY (customerid);


--
-- Name: klaimtransaksiproject klaimtransaksiproject_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.klaimtransaksiproject
    ADD CONSTRAINT klaimtransaksiproject_pkey PRIMARY KEY (idtransaksiklaim);


--
-- Name: konversiperolehanqurban konversiperolehanqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.konversiperolehanqurban
    ADD CONSTRAINT konversiperolehanqurban_pkey PRIMARY KEY (konversiperolehanqurbanid);


--
-- Name: liabilityaccount liabilityaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.liabilityaccount
    ADD CONSTRAINT liabilityaccount_pkey PRIMARY KEY (accountno);


--
-- Name: liabilitytransactionitem liabilitytransactionitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.liabilitytransactionitem
    ADD CONSTRAINT liabilitytransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: linkedprograms linkedprograms_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.linkedprograms
    ADD CONSTRAINT linkedprograms_pkey PRIMARY KEY (linkedprogramid);


--
-- Name: mapreconcile mapreconcile_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mapreconcile
    ADD CONSTRAINT mapreconcile_pkey PRIMARY KEY (mapid);


--
-- Name: marginitem marginitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.marginitem
    ADD CONSTRAINT marginitem_pkey PRIMARY KEY (itemstatementid);


--
-- Name: marketingqurban marketingqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.marketingqurban
    ADD CONSTRAINT marketingqurban_pkey PRIMARY KEY (marketingqurbanid);


--
-- Name: masjidkum3 masjidkum3_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.masjidkum3
    ADD CONSTRAINT masjidkum3_pkey PRIMARY KEY (mustahiqgroupid);


--
-- Name: masterjenisdonasiqurban masterjenisdonasiqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.masterjenisdonasiqurban
    ADD CONSTRAINT masterjenisdonasiqurban_pkey PRIMARY KEY (paketqurbanid);


--
-- Name: mpz mpz_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mpz
    ADD CONSTRAINT mpz_pkey PRIMARY KEY (customerid);


--
-- Name: mpzzisallocation mpzzisallocation_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mpzzisallocation
    ADD CONSTRAINT mpzzisallocation_pkey PRIMARY KEY (zisallocationid);


--
-- Name: mustahiq mustahiq_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiq
    ADD CONSTRAINT mustahiq_pkey PRIMARY KEY (mustahiqid);


--
-- Name: mustahiqadditionalinfo mustahiqadditionalinfo_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqadditionalinfo
    ADD CONSTRAINT mustahiqadditionalinfo_pkey PRIMARY KEY (mustahiqinfoid);


--
-- Name: mustahiqappraisal mustahiqappraisal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqappraisal
    ADD CONSTRAINT mustahiqappraisal_pkey PRIMARY KEY (appraisalid);


--
-- Name: mustahiqaqh mustahiqaqh_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqaqh
    ADD CONSTRAINT mustahiqaqh_pkey PRIMARY KEY (mustahiqid);


--
-- Name: mustahiqbankaccount mustahiqbankaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqbankaccount
    ADD CONSTRAINT mustahiqbankaccount_pkey PRIMARY KEY (bankaccountid);


--
-- Name: mustahiqcandidate mustahiqcandidate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqcandidate
    ADD CONSTRAINT mustahiqcandidate_pkey PRIMARY KEY (customerid);


--
-- Name: mustahiqcorporate mustahiqcorporate_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqcorporate
    ADD CONSTRAINT mustahiqcorporate_pkey PRIMARY KEY (mustahiqid);


--
-- Name: mustahiqgroup mustahiqgroup_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqgroup
    ADD CONSTRAINT mustahiqgroup_pkey PRIMARY KEY (mustahiqgroupid);


--
-- Name: mustahiqgroupdetail mustahiqgroupdetail_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqgroupdetail
    ADD CONSTRAINT mustahiqgroupdetail_pkey PRIMARY KEY (detailid);


--
-- Name: mustahiqkum3 mustahiqkum3_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqkum3
    ADD CONSTRAINT mustahiqkum3_pkey PRIMARY KEY (mustahiqid);


--
-- Name: mustahiqliabilityaccount mustahiqliabilityaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqliabilityaccount
    ADD CONSTRAINT mustahiqliabilityaccount_pkey PRIMARY KEY (accountno);


--
-- Name: mustahiqpersonal mustahiqpersonal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqpersonal
    ADD CONSTRAINT mustahiqpersonal_pkey PRIMARY KEY (mustahiqid);


--
-- Name: mustahiqproduct mustahiqproduct_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqproduct
    ADD CONSTRAINT mustahiqproduct_pkey PRIMARY KEY (mustahiqproductid);


--
-- Name: mustahiqproductgroup mustahiqproductgroup_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqproductgroup
    ADD CONSTRAINT mustahiqproductgroup_pkey PRIMARY KEY (mustahiqproductgroupid);


--
-- Name: mustahiqproject mustahiqproject_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqproject
    ADD CONSTRAINT mustahiqproject_pkey PRIMARY KEY (mustahiqproductid);


--
-- Name: mustahiqqurban mustahiqqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.mustahiqqurban
    ADD CONSTRAINT mustahiqqurban_pkey PRIMARY KEY (mustahiqid);


--
-- Name: negara negara_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.negara
    ADD CONSTRAINT negara_pkey PRIMARY KEY (idnegara);


--
-- Name: orphanbalancepartition orphanbalancepartition_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.orphanbalancepartition
    ADD CONSTRAINT orphanbalancepartition_pkey PRIMARY KEY (balancepartitionid);


--
-- Name: orphanbeasiswa orphanbeasiswa_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.orphanbeasiswa
    ADD CONSTRAINT orphanbeasiswa_pkey PRIMARY KEY (customerid);


--
-- Name: orphandebtlist orphandebtlist_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.orphandebtlist
    ADD CONSTRAINT orphandebtlist_pkey PRIMARY KEY (debtid);


--
-- Name: orphankafala orphankafala_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.orphankafala
    ADD CONSTRAINT orphankafala_pkey PRIMARY KEY (customerid);


--
-- Name: orphankafalaliability orphankafalaliability_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.orphankafalaliability
    ADD CONSTRAINT orphankafalaliability_pkey PRIMARY KEY (accountno);


--
-- Name: orphanksm orphanksm_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.orphanksm
    ADD CONSTRAINT orphanksm_pkey PRIMARY KEY (customerid);


--
-- Name: orphansiblings orphansiblings_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.orphansiblings
    ADD CONSTRAINT orphansiblings_pkey PRIMARY KEY (siblingsid);


--
-- Name: orphantertiarylist orphantertiarylist_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.orphantertiarylist
    ADD CONSTRAINT orphantertiarylist_pkey PRIMARY KEY (tertiaryid);


--
-- Name: parameterglobal parameterglobal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.parameterglobal
    ADD CONSTRAINT parameterglobal_pkey PRIMARY KEY (kode_parameter);


--
-- Name: parameterinbox parameterinbox_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.parameterinbox
    ADD CONSTRAINT parameterinbox_pkey PRIMARY KEY (kodeinbox);


--
-- Name: parameterjournal parameterjournal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.parameterjournal
    ADD CONSTRAINT parameterjournal_pkey PRIMARY KEY (parameterjournalid);


--
-- Name: parameterjournalitem parameterjournalitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.parameterjournalitem
    ADD CONSTRAINT parameterjournalitem_pkey PRIMARY KEY (parameterjournalitemid);


--
-- Name: partner partner_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.partner
    ADD CONSTRAINT partner_pkey PRIMARY KEY (partnerid);


--
-- Name: pequrban pequrban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.pequrban
    ADD CONSTRAINT pequrban_pkey PRIMARY KEY (donorid, productid);


--
-- Name: perolehanqurban perolehanqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.perolehanqurban
    ADD CONSTRAINT perolehanqurban_pkey PRIMARY KEY (productid, perolehanqurbanid);


--
-- Name: picdistribusi picdistribusi_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.picdistribusi
    ADD CONSTRAINT picdistribusi_pkey PRIMARY KEY (picdistribusiid);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (productid);


--
-- Name: productaccount productaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.productaccount
    ADD CONSTRAINT productaccount_pkey PRIMARY KEY (accountno);


--
-- Name: productdetail productdetail_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.productdetail
    ADD CONSTRAINT productdetail_pkey PRIMARY KEY (productdetailid);


--
-- Name: productgroup productgroup_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.productgroup
    ADD CONSTRAINT productgroup_pkey PRIMARY KEY (productgroupid);


--
-- Name: producthierarchy producthierarchy_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.producthierarchy
    ADD CONSTRAINT producthierarchy_pkey PRIMARY KEY (hierarchyid);


--
-- Name: producttarget producttarget_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.producttarget
    ADD CONSTRAINT producttarget_pkey PRIMARY KEY (producttargetid);


--
-- Name: producttargetcomponent producttargetcomponent_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.producttargetcomponent
    ADD CONSTRAINT producttargetcomponent_pkey PRIMARY KEY (componentid);


--
-- Name: producttargethistory producttargethistory_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.producttargethistory
    ADD CONSTRAINT producttargethistory_pkey PRIMARY KEY (producttargethistoryid);


--
-- Name: producttransactionitem producttransactionitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.producttransactionitem
    ADD CONSTRAINT producttransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: program program_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.program
    ADD CONSTRAINT program_pkey PRIMARY KEY (productid);


--
-- Name: programaqh programaqh_branchcode_key; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.programaqh
    ADD CONSTRAINT programaqh_branchcode_key UNIQUE (branchcode);


--
-- Name: programaqh programaqh_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.programaqh
    ADD CONSTRAINT programaqh_pkey PRIMARY KEY (productid);


--
-- Name: programksm programksm_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.programksm
    ADD CONSTRAINT programksm_pkey PRIMARY KEY (productid);


--
-- Name: programqurban programqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.programqurban
    ADD CONSTRAINT programqurban_pkey PRIMARY KEY (productid);


--
-- Name: project project_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (productid);


--
-- Name: projectaccount projectaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.projectaccount
    ADD CONSTRAINT projectaccount_pkey PRIMARY KEY (accountno);


--
-- Name: propinsi propinsi_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.propinsi
    ADD CONSTRAINT propinsi_pkey PRIMARY KEY (idpropinsi);


--
-- Name: proposal proposal_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.proposal
    ADD CONSTRAINT proposal_pkey PRIMARY KEY (proposalid);


--
-- Name: realisasidistribusi realisasidistribusi_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realisasidistribusi
    ADD CONSTRAINT realisasidistribusi_pkey PRIMARY KEY (realisasidistribusiid);


--
-- Name: realisasidistribusihewan realisasidistribusihewan_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realisasidistribusihewan
    ADD CONSTRAINT realisasidistribusihewan_pkey PRIMARY KEY (realisasidistribusihewanid);


--
-- Name: realization realization_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realization
    ADD CONSTRAINT realization_pkey PRIMARY KEY (realizationid);


--
-- Name: realizationbudget realizationbudget_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationbudget
    ADD CONSTRAINT realizationbudget_pkey PRIMARY KEY (realbudgetid);


--
-- Name: realizationcost realizationcost_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationcost
    ADD CONSTRAINT realizationcost_pkey PRIMARY KEY (realizationcostid);


--
-- Name: realizationdetail realizationdetail_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationdetail
    ADD CONSTRAINT realizationdetail_pkey PRIMARY KEY (realizationdetailid);


--
-- Name: realizationmemo realizationmemo_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationmemo
    ADD CONSTRAINT realizationmemo_pkey PRIMARY KEY (realmemoid);


--
-- Name: realizationmemodetail realizationmemodetail_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationmemodetail
    ADD CONSTRAINT realizationmemodetail_pkey PRIMARY KEY (realmemodetailid);


--
-- Name: realizationpartner realizationpartner_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationpartner
    ADD CONSTRAINT realizationpartner_pkey PRIMARY KEY (realizationpartnerid);


--
-- Name: realizationphoto realizationphoto_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationphoto
    ADD CONSTRAINT realizationphoto_pkey PRIMARY KEY (photoid);


--
-- Name: realizationreturn realizationreturn_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationreturn
    ADD CONSTRAINT realizationreturn_pkey PRIMARY KEY (returnid);


--
-- Name: realizationreturndetail realizationreturndetail_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationreturndetail
    ADD CONSTRAINT realizationreturndetail_pkey PRIMARY KEY (returndetailid);


--
-- Name: realizationtransactionitem realizationtransactionitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.realizationtransactionitem
    ADD CONSTRAINT realizationtransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: reconcileprocess reconcileprocess_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.reconcileprocess
    ADD CONSTRAINT reconcileprocess_pkey PRIMARY KEY (reconcileprocessid);


--
-- Name: reconciletransaction reconciletransaction_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.reconciletransaction
    ADD CONSTRAINT reconciletransaction_pkey PRIMARY KEY (banktransactionid);


--
-- Name: reconciletransactionqurban reconciletransactionqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.reconciletransactionqurban
    ADD CONSTRAINT reconciletransactionqurban_pkey PRIMARY KEY (reconciletransactionqurbanid);


--
-- Name: region region_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.region
    ADD CONSTRAINT region_pkey PRIMARY KEY (regionid);


--
-- Name: rekeningpenghimpunanqurban rekeningpenghimpunanqurban_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.rekeningpenghimpunanqurban
    ADD CONSTRAINT rekeningpenghimpunanqurban_pkey PRIMARY KEY (rekeningpenghimpunanqurbanid);


--
-- Name: rencanadistribusi rencanadistribusi_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.rencanadistribusi
    ADD CONSTRAINT rencanadistribusi_pkey PRIMARY KEY (rencanadistribusiid);


--
-- Name: rencanadistribusihewan rencanadistribusihewan_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.rencanadistribusihewan
    ADD CONSTRAINT rencanadistribusihewan_pkey PRIMARY KEY (rencanadistribusihewanid);


--
-- Name: requestdistribusi requestdistribusi_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.requestdistribusi
    ADD CONSTRAINT requestdistribusi_pkey PRIMARY KEY (requestdistribusiid);


--
-- Name: reversetransaction reversetransaction_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.reversetransaction
    ADD CONSTRAINT reversetransaction_pkey PRIMARY KEY (sourcetransactionid);


--
-- Name: sessionblob sessionblob_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.sessionblob
    ADD CONSTRAINT sessionblob_pkey PRIMARY KEY (id);


--
-- Name: statusreceivablereport statusreceivablereport_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.statusreceivablereport
    ADD CONSTRAINT statusreceivablereport_pkey PRIMARY KEY (statusreceivableid);


--
-- Name: statusrecrepdetail statusrecrepdetail_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.statusrecrepdetail
    ADD CONSTRAINT statusrecrepdetail_pkey PRIMARY KEY (statusrecrepdetailid);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (transactionid);


--
-- Name: transactionaccount transactionaccount_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.transactionaccount
    ADD CONSTRAINT transactionaccount_pkey PRIMARY KEY (accountno);


--
-- Name: transactionitem transactionitem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.transactionitem
    ADD CONSTRAINT transactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: transactiontype transactiontype_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.transactiontype
    ADD CONSTRAINT transactiontype_pkey PRIMARY KEY (transactioncode);


--
-- Name: uploadedstatement uploadedstatement_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.uploadedstatement
    ADD CONSTRAINT uploadedstatement_pkey PRIMARY KEY (uploadedstatementid);


--
-- Name: visit visit_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.visit
    ADD CONSTRAINT visit_pkey PRIMARY KEY (visitid);


--
-- Name: visititem visititem_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.visititem
    ADD CONSTRAINT visititem_pkey PRIMARY KEY (visititemid);


--
-- Name: visitperson visitperson_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.visitperson
    ADD CONSTRAINT visitperson_pkey PRIMARY KEY (visitpersonid);


--
-- Name: volunteer volunteer_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.volunteer
    ADD CONSTRAINT volunteer_pkey PRIMARY KEY (volunteerid);


--
-- Name: volunteertransaction volunteertransaction_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.volunteertransaction
    ADD CONSTRAINT volunteertransaction_pkey PRIMARY KEY (transactionitemid);


--
-- Name: vproduct vproduct_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.vproduct
    ADD CONSTRAINT vproduct_pkey PRIMARY KEY (accountno);


--
-- Name: worksector worksector_pkey; Type: CONSTRAINT; Schema: program; Owner: postgres
--

ALTER TABLE ONLY program.worksector
    ADD CONSTRAINT worksector_pkey PRIMARY KEY (workid);


--
-- Name: appsubsystem appsubsystem_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appsubsystem
    ADD CONSTRAINT appsubsystem_pkey PRIMARY KEY (subsystem_code);


--
-- Name: mustahiqadditionalinfo mustahiqadditionalinfo_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mustahiqadditionalinfo
    ADD CONSTRAINT mustahiqadditionalinfo_pkey PRIMARY KEY (mustahiqinfoid);


--
-- Name: academicvalue academicvalue_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.academicvalue
    ADD CONSTRAINT academicvalue_pkey PRIMARY KEY (academicvalueid);


--
-- Name: academicvalueitem academicvalueitem_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.academicvalueitem
    ADD CONSTRAINT academicvalueitem_pkey PRIMARY KEY (academicvalueitemid);


--
-- Name: academicvalueitemtemplate academicvalueitemtemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.academicvalueitemtemplate
    ADD CONSTRAINT academicvalueitemtemplate_pkey PRIMARY KEY (academicvalueitemtemplateid);


--
-- Name: academicvaluetemplate academicvaluetemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.academicvaluetemplate
    ADD CONSTRAINT academicvaluetemplate_pkey PRIMARY KEY (academicvaluetemplateid);


--
-- Name: achievement achievement_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.achievement
    ADD CONSTRAINT achievement_pkey PRIMARY KEY (achievementid);


--
-- Name: achievementactivities achievementactivities_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.achievementactivities
    ADD CONSTRAINT achievementactivities_pkey PRIMARY KEY (achievementactivitiesid);


--
-- Name: activityappraisal activityappraisal_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.activityappraisal
    ADD CONSTRAINT activityappraisal_pkey PRIMARY KEY (activityappraisalid);


--
-- Name: activityappraisalitem activityappraisalitem_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.activityappraisalitem
    ADD CONSTRAINT activityappraisalitem_pkey PRIMARY KEY (itemid);


--
-- Name: activityappraisalitemtemplate activityappraisalitemtemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.activityappraisalitemtemplate
    ADD CONSTRAINT activityappraisalitemtemplate_pkey PRIMARY KEY (itemtemplateid);


--
-- Name: activityschool activityschool_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.activityschool
    ADD CONSTRAINT activityschool_pkey PRIMARY KEY (activityschoolid);


--
-- Name: agenda agenda_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.agenda
    ADD CONSTRAINT agenda_pkey PRIMARY KEY (agendaid);


--
-- Name: agendaitem agendaitem_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.agendaitem
    ADD CONSTRAINT agendaitem_pkey PRIMARY KEY (agendaitemid);


--
-- Name: agendaitemtemplate agendaitemtemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.agendaitemtemplate
    ADD CONSTRAINT agendaitemtemplate_pkey PRIMARY KEY (agendaitemtemplateid);


--
-- Name: agendatemplate agendatemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.agendatemplate
    ADD CONSTRAINT agendatemplate_pkey PRIMARY KEY (agendatemplateid);


--
-- Name: appraisal appraisal_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.appraisal
    ADD CONSTRAINT appraisal_pkey PRIMARY KEY (appraisalid);


--
-- Name: appraisalitem appraisalitem_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.appraisalitem
    ADD CONSTRAINT appraisalitem_pkey PRIMARY KEY (itemid);


--
-- Name: appraisalitemgroup appraisalitemgroup_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.appraisalitemgroup
    ADD CONSTRAINT appraisalitemgroup_pkey PRIMARY KEY (groupname);


--
-- Name: appraisalitemtemplate appraisalitemtemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.appraisalitemtemplate
    ADD CONSTRAINT appraisalitemtemplate_pkey PRIMARY KEY (itemtemplateid);


--
-- Name: appraisaltemplate appraisaltemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.appraisaltemplate
    ADD CONSTRAINT appraisaltemplate_pkey PRIMARY KEY (appraisaltemplateid);


--
-- Name: attendance attendance_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.attendance
    ADD CONSTRAINT attendance_pkey PRIMARY KEY (attendanceid);


--
-- Name: careerhistory careerhistory_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.careerhistory
    ADD CONSTRAINT careerhistory_pkey PRIMARY KEY (careerhistoryid);


--
-- Name: classhistory classhistory_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.classhistory
    ADD CONSTRAINT classhistory_pkey PRIMARY KEY (classhistoryid);


--
-- Name: club club_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.club
    ADD CONSTRAINT club_pkey PRIMARY KEY (clubid);


--
-- Name: companion companion_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.companion
    ADD CONSTRAINT companion_pkey PRIMARY KEY (companionid);


--
-- Name: companioncontract companioncontract_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.companioncontract
    ADD CONSTRAINT companioncontract_pkey PRIMARY KEY (contractno);


--
-- Name: companionproduct companionproduct_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.companionproduct
    ADD CONSTRAINT companionproduct_pkey PRIMARY KEY (productid, companionid);


--
-- Name: companionvisit companionvisit_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.companionvisit
    ADD CONSTRAINT companionvisit_pkey PRIMARY KEY (companionvisitid);


--
-- Name: companionvisititem companionvisititem_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.companionvisititem
    ADD CONSTRAINT companionvisititem_pkey PRIMARY KEY (itemid);


--
-- Name: companionvisititemtemplate companionvisititemtemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.companionvisititemtemplate
    ADD CONSTRAINT companionvisititemtemplate_pkey PRIMARY KEY (itemtemplateid);


--
-- Name: contracthistory contracthistory_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.contracthistory
    ADD CONSTRAINT contracthistory_pkey PRIMARY KEY (contractno);


--
-- Name: custom_idgen custom_idgen_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.custom_idgen
    ADD CONSTRAINT custom_idgen_pkey PRIMARY KEY (idname, idcode);


--
-- Name: customer customer_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.customer
    ADD CONSTRAINT customer_pkey PRIMARY KEY (customerid);


--
-- Name: customercorporate customercorporate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.customercorporate
    ADD CONSTRAINT customercorporate_pkey PRIMARY KEY (customerid);


--
-- Name: customerpersonal customerpersonal_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.customerpersonal
    ADD CONSTRAINT customerpersonal_pkey PRIMARY KEY (customerid);


--
-- Name: education education_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.education
    ADD CONSTRAINT education_pkey PRIMARY KEY (educationid);


--
-- Name: employee employee_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.employee
    ADD CONSTRAINT employee_pkey PRIMARY KEY (employeeid);


--
-- Name: employeedevelopmentprogram employeedevelopmentprogram_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.employeedevelopmentprogram
    ADD CONSTRAINT employeedevelopmentprogram_pkey PRIMARY KEY (edpid);


--
-- Name: employeetraining employeetraining_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.employeetraining
    ADD CONSTRAINT employeetraining_pkey PRIMARY KEY (trainingid);


--
-- Name: enum_int enum_int_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.enum_int
    ADD CONSTRAINT enum_int_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: enum_varchar enum_varchar_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.enum_varchar
    ADD CONSTRAINT enum_varchar_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: equipment equipment_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (equipmentid);


--
-- Name: family family_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.family
    ADD CONSTRAINT family_pkey PRIMARY KEY (familyid);


--
-- Name: formaleducation formaleducation_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.formaleducation
    ADD CONSTRAINT formaleducation_pkey PRIMARY KEY (educationid);


--
-- Name: healthplafond healthplafond_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.healthplafond
    ADD CONSTRAINT healthplafond_pkey PRIMARY KEY (employeeid);


--
-- Name: healthreimbursement healthreimbursement_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.healthreimbursement
    ADD CONSTRAINT healthreimbursement_pkey PRIMARY KEY (rank, reimbursementtype, maritalstatus);


--
-- Name: id_gen id_gen_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.id_gen
    ADD CONSTRAINT id_gen_pkey PRIMARY KEY (id_code);


--
-- Name: individu individu_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.individu
    ADD CONSTRAINT individu_pkey PRIMARY KEY (individuid);


--
-- Name: infrastructure infrastructure_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.infrastructure
    ADD CONSTRAINT infrastructure_pkey PRIMARY KEY (infrastructureid);


--
-- Name: logincorporate logincorporate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.logincorporate
    ADD CONSTRAINT logincorporate_pkey PRIMARY KEY (login);


--
-- Name: mustahiq mustahiq_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.mustahiq
    ADD CONSTRAINT mustahiq_pkey PRIMARY KEY (mustahiqid);


--
-- Name: mustahiqpersonal mustahiqpersonal_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.mustahiqpersonal
    ADD CONSTRAINT mustahiqpersonal_pkey PRIMARY KEY (mustahiqid);


--
-- Name: mustahiqproduct mustahiqproduct_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.mustahiqproduct
    ADD CONSTRAINT mustahiqproduct_pkey PRIMARY KEY (productid, mustahiqid);


--
-- Name: negara negara_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.negara
    ADD CONSTRAINT negara_pkey PRIMARY KEY (idnegara);


--
-- Name: nonformaleducation nonformaleducation_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.nonformaleducation
    ADD CONSTRAINT nonformaleducation_pkey PRIMARY KEY (educationid);


--
-- Name: officialreport officialreport_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.officialreport
    ADD CONSTRAINT officialreport_pkey PRIMARY KEY (officialreportid);


--
-- Name: officialreportofdamage officialreportofdamage_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.officialreportofdamage
    ADD CONSTRAINT officialreportofdamage_pkey PRIMARY KEY (officialreportid);


--
-- Name: officialreportofreplacement officialreportofreplacement_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.officialreportofreplacement
    ADD CONSTRAINT officialreportofreplacement_pkey PRIMARY KEY (officialreportid);


--
-- Name: offwork offwork_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.offwork
    ADD CONSTRAINT offwork_pkey PRIMARY KEY (offworkid);


--
-- Name: offworkmaternity offworkmaternity_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.offworkmaternity
    ADD CONSTRAINT offworkmaternity_pkey PRIMARY KEY (offworkid);


--
-- Name: offworkpermit offworkpermit_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.offworkpermit
    ADD CONSTRAINT offworkpermit_pkey PRIMARY KEY (offworkid);


--
-- Name: offworkplafond offworkplafond_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.offworkplafond
    ADD CONSTRAINT offworkplafond_pkey PRIMARY KEY (employeeid);


--
-- Name: offworkregular offworkregular_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.offworkregular
    ADD CONSTRAINT offworkregular_pkey PRIMARY KEY (offworkid);


--
-- Name: organizationexperience organizationexperience_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.organizationexperience
    ADD CONSTRAINT organizationexperience_pkey PRIMARY KEY (organizationexperienceid);


--
-- Name: paemployee paemployee_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.paemployee
    ADD CONSTRAINT paemployee_pkey PRIMARY KEY (performanceappraisalid);


--
-- Name: parameterglobal parameterglobal_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.parameterglobal
    ADD CONSTRAINT parameterglobal_pkey PRIMARY KEY (kode_parameter);


--
-- Name: paschool paschool_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.paschool
    ADD CONSTRAINT paschool_pkey PRIMARY KEY (performanceappraisalid);


--
-- Name: performanceappraisal performanceappraisal_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.performanceappraisal
    ADD CONSTRAINT performanceappraisal_pkey PRIMARY KEY (performanceappraisalid);


--
-- Name: performanceitem performanceitem_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.performanceitem
    ADD CONSTRAINT performanceitem_pkey PRIMARY KEY (performanceitemid);


--
-- Name: performanceparameter performanceparameter_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.performanceparameter
    ADD CONSTRAINT performanceparameter_pkey PRIMARY KEY (parameterid);


--
-- Name: position position_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school."position"
    ADD CONSTRAINT position_pkey PRIMARY KEY (positionid);


--
-- Name: pptemplate pptemplate_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.pptemplate
    ADD CONSTRAINT pptemplate_pkey PRIMARY KEY (pptemplateid);


--
-- Name: pptemplate pptemplate_pptemplatecode_key; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.pptemplate
    ADD CONSTRAINT pptemplate_pptemplatecode_key UNIQUE (pptemplatecode);


--
-- Name: pptemplateitem pptemplateitem_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.pptemplateitem
    ADD CONSTRAINT pptemplateitem_pkey PRIMARY KEY (pptemplateid, parameterid);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (productid);


--
-- Name: productgroup productgroup_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.productgroup
    ADD CONSTRAINT productgroup_pkey PRIMARY KEY (productgroupname);


--
-- Name: program program_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.program
    ADD CONSTRAINT program_pkey PRIMARY KEY (productid);


--
-- Name: propinsi propinsi_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.propinsi
    ADD CONSTRAINT propinsi_pkey PRIMARY KEY (idpropinsi);


--
-- Name: rankhistory rankhistory_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.rankhistory
    ADD CONSTRAINT rankhistory_pkey PRIMARY KEY (rankhistoryid);


--
-- Name: reimbursementrealization reimbursementrealization_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.reimbursementrealization
    ADD CONSTRAINT reimbursementrealization_pkey PRIMARY KEY (reimbursementrealizationid);


--
-- Name: salaryhistory salaryhistory_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.salaryhistory
    ADD CONSTRAINT salaryhistory_pkey PRIMARY KEY (salaryhistoryid);


--
-- Name: salaryitemhistory salaryitemhistory_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.salaryitemhistory
    ADD CONSTRAINT salaryitemhistory_pkey PRIMARY KEY (salaryitemid);


--
-- Name: salaryitemparameter salaryitemparameter_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.salaryitemparameter
    ADD CONSTRAINT salaryitemparameter_pkey PRIMARY KEY (salaryitemparameterid);


--
-- Name: salaryitemparametergroup salaryitemparametergroup_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.salaryitemparametergroup
    ADD CONSTRAINT salaryitemparametergroup_pkey PRIMARY KEY (parametergroupid);


--
-- Name: salaryitemscheme salaryitemscheme_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.salaryitemscheme
    ADD CONSTRAINT salaryitemscheme_pkey PRIMARY KEY (salaryitemschemeid);


--
-- Name: salaryscheme salaryscheme_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.salaryscheme
    ADD CONSTRAINT salaryscheme_pkey PRIMARY KEY (salaryschemeid);


--
-- Name: schoolyear schoolyear_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.schoolyear
    ADD CONSTRAINT schoolyear_pkey PRIMARY KEY (schoolyearcode);


--
-- Name: sessionblob sessionblob_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.sessionblob
    ADD CONSTRAINT sessionblob_pkey PRIMARY KEY (id);


--
-- Name: sourcefound sourcefound_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.sourcefound
    ADD CONSTRAINT sourcefound_pkey PRIMARY KEY (sourcefoundid);


--
-- Name: stockopname stockopname_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.stockopname
    ADD CONSTRAINT stockopname_pkey PRIMARY KEY (stockopnameid);


--
-- Name: stockopnameequipment stockopnameequipment_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.stockopnameequipment
    ADD CONSTRAINT stockopnameequipment_pkey PRIMARY KEY (stockopnameid, equipmentid);


--
-- Name: stockopnametools stockopnametools_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.stockopnametools
    ADD CONSTRAINT stockopnametools_pkey PRIMARY KEY (stockopnameid, toolsid);


--
-- Name: student student_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.student
    ADD CONSTRAINT student_pkey PRIMARY KEY (productid, mustahiqid);


--
-- Name: studentclass studentclass_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.studentclass
    ADD CONSTRAINT studentclass_pkey PRIMARY KEY (studentclasscode);


--
-- Name: studenthealth studenthealth_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.studenthealth
    ADD CONSTRAINT studenthealth_pkey PRIMARY KEY (studenthealthid);


--
-- Name: subject subject_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.subject
    ADD CONSTRAINT subject_pkey PRIMARY KEY (subjectid);


--
-- Name: targetachievement targetachievement_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.targetachievement
    ADD CONSTRAINT targetachievement_pkey PRIMARY KEY (targetachievementid);


--
-- Name: toollist toollist_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.toollist
    ADD CONSTRAINT toollist_pkey PRIMARY KEY (toollistid);


--
-- Name: tools tools_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.tools
    ADD CONSTRAINT tools_pkey PRIMARY KEY (toolsid);


--
-- Name: training training_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.training
    ADD CONSTRAINT training_pkey PRIMARY KEY (trainingid);


--
-- Name: trainingseminar trainingseminar_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.trainingseminar
    ADD CONSTRAINT trainingseminar_pkey PRIMARY KEY (trainingid);


--
-- Name: workexperience workexperience_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.workexperience
    ADD CONSTRAINT workexperience_pkey PRIMARY KEY (workexperienceid);


--
-- Name: workunit workunit_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.workunit
    ADD CONSTRAINT workunit_pkey PRIMARY KEY (workunitid);


--
-- Name: workunitposition workunitposition_pkey; Type: CONSTRAINT; Schema: school; Owner: postgres
--

ALTER TABLE ONLY school.workunitposition
    ADD CONSTRAINT workunitposition_pkey PRIMARY KEY (workunitid, positionid);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (account_code);


--
-- Name: accountdetail accountdetail_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountdetail
    ADD CONSTRAINT accountdetail_pkey PRIMARY KEY (fl_account, fl_detail_account);


--
-- Name: accountgroup accountgroup_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountgroup
    ADD CONSTRAINT accountgroup_pkey PRIMARY KEY (id);


--
-- Name: accounthierarchy accounthierarchy_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accounthierarchy
    ADD CONSTRAINT accounthierarchy_pkey PRIMARY KEY (accounthierarchy_id);


--
-- Name: accountingday accountingday_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountingday
    ADD CONSTRAINT accountingday_pkey PRIMARY KEY (periode_code, fl_accountingperiode, fl_accountingyear);


--
-- Name: accountingperiode accountingperiode_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountingperiode
    ADD CONSTRAINT accountingperiode_pkey PRIMARY KEY (fl_accountingyear, periode_code);


--
-- Name: accountingyear accountingyear_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountingyear
    ADD CONSTRAINT accountingyear_pkey PRIMARY KEY (periode_code);


--
-- Name: accountinstance accountinstance_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountinstance
    ADD CONSTRAINT accountinstance_pkey PRIMARY KEY (accountinstance_id);


--
-- Name: accountinterface accountinterface_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountinterface
    ADD CONSTRAINT accountinterface_pkey PRIMARY KEY (interface_code);


--
-- Name: accountinterfacemember accountinterfacemember_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountinterfacemember
    ADD CONSTRAINT accountinterfacemember_pkey PRIMARY KEY (member_id);


--
-- Name: accountmanager accountmanager_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountmanager
    ADD CONSTRAINT accountmanager_pkey PRIMARY KEY (amcode);


--
-- Name: accountreceivable accountreceivable_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accountreceivable
    ADD CONSTRAINT accountreceivable_pkey PRIMARY KEY (accountno);


--
-- Name: accounttransactionitem accounttransactionitem_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accounttransactionitem
    ADD CONSTRAINT accounttransactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: accreceivabletransactitem accreceivabletransactitem_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accreceivabletransactitem
    ADD CONSTRAINT accreceivabletransactitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: accsubsystem accsubsystem_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.accsubsystem
    ADD CONSTRAINT accsubsystem_pkey PRIMARY KEY (subsystemcode);


--
-- Name: balancesumgroup balancesumgroup_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.balancesumgroup
    ADD CONSTRAINT balancesumgroup_pkey PRIMARY KEY (groupcode);


--
-- Name: balancesumitem balancesumitem_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.balancesumitem
    ADD CONSTRAINT balancesumitem_pkey PRIMARY KEY (itemid);


--
-- Name: balancesumitemmember balancesumitemmember_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.balancesumitemmember
    ADD CONSTRAINT balancesumitemmember_pkey PRIMARY KEY (memberid);


--
-- Name: balancesumitemtrancode balancesumitemtrancode_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.balancesumitemtrancode
    ADD CONSTRAINT balancesumitemtrancode_pkey PRIMARY KEY (memberid);


--
-- Name: bank bank_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.bank
    ADD CONSTRAINT bank_pkey PRIMARY KEY (bankcode);


--
-- Name: bankaccountlist bankaccountlist_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.bankaccountlist
    ADD CONSTRAINT bankaccountlist_pk PRIMARY KEY (bankaccountid);


--
-- Name: batchupload batchupload_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.batchupload
    ADD CONSTRAINT batchupload_pkey PRIMARY KEY (batchid);


--
-- Name: batchuploaditem batchuploaditem_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.batchuploaditem
    ADD CONSTRAINT batchuploaditem_pk PRIMARY KEY (batchitemid);


--
-- Name: blobregistration blobregistration_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.blobregistration
    ADD CONSTRAINT blobregistration_pkey PRIMARY KEY (id);


--
-- Name: bpscenario bpscenario_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.bpscenario
    ADD CONSTRAINT bpscenario_pkey PRIMARY KEY (bpscenarioid);


--
-- Name: bpscenariostep bpscenariostep_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.bpscenariostep
    ADD CONSTRAINT bpscenariostep_pkey PRIMARY KEY (bpstepid);


--
-- Name: bpscript bpscript_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.bpscript
    ADD CONSTRAINT bpscript_pkey PRIMARY KEY (bpscriptid);


--
-- Name: bsz bsz_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.bsz
    ADD CONSTRAINT bsz_pk PRIMARY KEY (bszid);


--
-- Name: bszdetail bszdetail_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.bszdetail
    ADD CONSTRAINT bszdetail_pk PRIMARY KEY (bszdetailid);


--
-- Name: bsztransaction bsztransaction_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.bsztransaction
    ADD CONSTRAINT bsztransaction_pk PRIMARY KEY (bsztransactionid);


--
-- Name: cashaccount cashaccount_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.cashaccount
    ADD CONSTRAINT cashaccount_pkey PRIMARY KEY (accountno);


--
-- Name: cashadvancememoinfo cashadvancememoinfo_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.cashadvancememoinfo
    ADD CONSTRAINT cashadvancememoinfo_pkey PRIMARY KEY (transactionid);


--
-- Name: cashadvanceprograminfo cashadvanceprograminfo_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.cashadvanceprograminfo
    ADD CONSTRAINT cashadvanceprograminfo_pkey PRIMARY KEY (sourcetransactionid, reporttransactionid);


--
-- Name: cashflowgroup cashflowgroup_key; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.cashflowgroup
    ADD CONSTRAINT cashflowgroup_key PRIMARY KEY (cfgroupid);


--
-- Name: cashflowmember cashflowmember_key; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.cashflowmember
    ADD CONSTRAINT cashflowmember_key PRIMARY KEY (cfmemberid);


--
-- Name: wakafcertificate cerificated_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.wakafcertificate
    ADD CONSTRAINT cerificated_pkey PRIMARY KEY (certificateid);


--
-- Name: coa_convertion coa_convertion_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.coa_convertion
    ADD CONSTRAINT coa_convertion_pkey PRIMARY KEY (accountcode_old);


--
-- Name: cpalpamapping cpalpamapping_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.cpalpamapping
    ADD CONSTRAINT cpalpamapping_pkey PRIMARY KEY (cpalpamapping_id);


--
-- Name: currency currency_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (currency_code);


--
-- Name: currency_pkpu currencyp_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.currency_pkpu
    ADD CONSTRAINT currencyp_pkey PRIMARY KEY (currency_code);


--
-- Name: custom_idgen custom_idgen_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.custom_idgen
    ADD CONSTRAINT custom_idgen_pkey PRIMARY KEY (idname, idcode);


--
-- Name: dailybalance dailybalance_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.dailybalance
    ADD CONSTRAINT dailybalance_pkey PRIMARY KEY (dailybalance_id);


--
-- Name: dailybalancecash dailybalancecash_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.dailybalancecash
    ADD CONSTRAINT dailybalancecash_pkey PRIMARY KEY (dailybalance_id);


--
-- Name: dailyprojectbalance dailyprojectbalance_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.dailyprojectbalance
    ADD CONSTRAINT dailyprojectbalance_pkey PRIMARY KEY (dailyprojectbalance_id);


--
-- Name: dinarcertificate dinarcertificate_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.dinarcertificate
    ADD CONSTRAINT dinarcertificate_pkey PRIMARY KEY (dinarcertificateid);


--
-- Name: distributiontransferinfo distributiontransferinfo_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.distributiontransferinfo
    ADD CONSTRAINT distributiontransferinfo_pkey PRIMARY KEY (distributionid);


--
-- Name: donorbankaccount donorbankaccount_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.donorbankaccount
    ADD CONSTRAINT donorbankaccount_pk PRIMARY KEY (bankaccountid);


--
-- Name: donorcommitment donorcommitment_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.donorcommitment
    ADD CONSTRAINT donorcommitment_pkey PRIMARY KEY (commitmentid);


--
-- Name: donortotalfund donortotalfund_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.donortotalfund
    ADD CONSTRAINT donortotalfund_pkey PRIMARY KEY (totalfundid);


--
-- Name: enum_int enum_int_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.enum_int
    ADD CONSTRAINT enum_int_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: enum_varchar enum_varchar_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.enum_varchar
    ADD CONSTRAINT enum_varchar_pkey PRIMARY KEY (enum_name, enum_value);


--
-- Name: externaltransaction externaltransaction_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.externaltransaction
    ADD CONSTRAINT externaltransaction_pkey PRIMARY KEY (exttransactionid);


--
-- Name: fact_daily_balance fact_daily_balance_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.fact_daily_balance
    ADD CONSTRAINT fact_daily_balance_pkey PRIMARY KEY (fact_id);


--
-- Name: financialaccount financialaccount_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.financialaccount
    ADD CONSTRAINT financialaccount_pkey PRIMARY KEY (accountno);


--
-- Name: fieldofwork fwork_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.fieldofwork
    ADD CONSTRAINT fwork_pkey PRIMARY KEY (fworkid);


--
-- Name: generalclass generalclass_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.generalclass
    ADD CONSTRAINT generalclass_pkey PRIMARY KEY (id);


--
-- Name: generatejournal_candidate generatejournal_candidate_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.generatejournal_candidate
    ADD CONSTRAINT generatejournal_candidate_pkey PRIMARY KEY (transactionid);


--
-- Name: glinterfaceidentifier glinterfaceidentifier_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.glinterfaceidentifier
    ADD CONSTRAINT glinterfaceidentifier_pkey PRIMARY KEY (identifier_id);


--
-- Name: glintftemplate glintftemplate_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.glintftemplate
    ADD CONSTRAINT glintftemplate_pkey PRIMARY KEY (template_code);


--
-- Name: glintftemplatedetail glintftemplatedetail_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.glintftemplatedetail
    ADD CONSTRAINT glintftemplatedetail_pkey PRIMARY KEY (templatedetail_id);


--
-- Name: globalglinterface globalglinterface_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.globalglinterface
    ADD CONSTRAINT globalglinterface_pkey PRIMARY KEY (glinterfacecode);


--
-- Name: hi_permil hi_permil_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.hi_permil
    ADD CONSTRAINT hi_permil_pkey PRIMARY KEY (id_hipermil);


--
-- Name: hipermildistribution hipermildistribution_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.hipermildistribution
    ADD CONSTRAINT hipermildistribution_pkey PRIMARY KEY (distribution_id, id_hipermil);


--
-- Name: historyofchanges historyofchanges_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.historyofchanges
    ADD CONSTRAINT historyofchanges_pkey PRIMARY KEY (historyid);


--
-- Name: humancapitalbatch humancapitalbatch_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.humancapitalbatch
    ADD CONSTRAINT humancapitalbatch_pkey PRIMARY KEY (batchid);


--
-- Name: humancapitalbatchitem humancapitalbatchitem_pkey2; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.humancapitalbatchitem
    ADD CONSTRAINT humancapitalbatchitem_pkey2 PRIMARY KEY (batchitemid);


--
-- Name: humancapitalpassedreport humancapitalpassedreport_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.humancapitalpassedreport
    ADD CONSTRAINT humancapitalpassedreport_pkey PRIMARY KEY (reportid);


--
-- Name: id_gen id_gen_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.id_gen
    ADD CONSTRAINT id_gen_pkey PRIMARY KEY (id_code);


--
-- Name: inbox inbox_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.inbox
    ADD CONSTRAINT inbox_pkey PRIMARY KEY (inboxid);


--
-- Name: inboxhistory inboxhistory_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.inboxhistory
    ADD CONSTRAINT inboxhistory_pkey PRIMARY KEY (inboxhistoryid);


--
-- Name: inboxtransaction inboxtransaction_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.inboxtransaction
    ADD CONSTRAINT inboxtransaction_pk PRIMARY KEY (inboxid);


--
-- Name: intrnewtransaction intrnewtransaction_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.intrnewtransaction
    ADD CONSTRAINT intrnewtransaction_pkey PRIMARY KEY (subsysteminteraction_id);


--
-- Name: intrpicktransaction intrpicktransaction_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.intrpicktransaction
    ADD CONSTRAINT intrpicktransaction_pkey PRIMARY KEY (subsysteminteraction_id);


--
-- Name: invoiceproduct invoice_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.invoiceproduct
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (invoiceid);


--
-- Name: jenis_dana jenis_dana_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.jenis_dana
    ADD CONSTRAINT jenis_dana_pkey PRIMARY KEY (kode_jenis_dana);


--
-- Name: jenisrak jenisrak_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.jenisrak
    ADD CONSTRAINT jenisrak_pkey PRIMARY KEY (koderak);


--
-- Name: journal_cashflow_candidate journal_cashflow_candidate_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.journal_cashflow_candidate
    ADD CONSTRAINT journal_cashflow_candidate_pkey PRIMARY KEY (journal_no);


--
-- Name: journal_cashflow journal_cashflow_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.journal_cashflow
    ADD CONSTRAINT journal_cashflow_pkey PRIMARY KEY (journal_no);


--
-- Name: journal journal_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.journal
    ADD CONSTRAINT journal_pk PRIMARY KEY (journal_no);


--
-- Name: journalblock journalblock_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.journalblock
    ADD CONSTRAINT journalblock_pkey PRIMARY KEY (id_journalblock);


--
-- Name: journalcode journalcode_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.journalcode
    ADD CONSTRAINT journalcode_pkey PRIMARY KEY (journalcode_id);


--
-- Name: journaldeletion journaldeletion_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.journaldeletion
    ADD CONSTRAINT journaldeletion_pkey PRIMARY KEY (journal_no);


--
-- Name: journalitem_cashflow journalitem_cashflow_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.journalitem_cashflow
    ADD CONSTRAINT journalitem_cashflow_pkey PRIMARY KEY (journal_no, journalitem_no);


--
-- Name: journalitem journalitem_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.journalitem
    ADD CONSTRAINT journalitem_pk PRIMARY KEY (fl_journal, journalitem_no);


--
-- Name: propinsi kode_unik; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.propinsi
    ADD CONSTRAINT kode_unik UNIQUE (kodepropinsi);


--
-- Name: kota_kabupaten kota_kabupaten_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.kota_kabupaten
    ADD CONSTRAINT kota_kabupaten_pkey PRIMARY KEY (kotaid);


--
-- Name: kurshistory kurshistory_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.kurshistory
    ADD CONSTRAINT kurshistory_pkey PRIMARY KEY (kurshistory_id);


--
-- Name: mapping_gldetail_2014 mapping_gldetail_2014_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.mapping_gldetail_2014
    ADD CONSTRAINT mapping_gldetail_2014_pkey PRIMARY KEY (account_code_old);


--
-- Name: mapping_glint_asset mapping_glint_asset_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.mapping_glint_asset
    ADD CONSTRAINT mapping_glint_asset_pkey PRIMARY KEY (account_code);


--
-- Name: mapping_glinttemplate_2014 mapping_glinttemplate_2014_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.mapping_glinttemplate_2014
    ADD CONSTRAINT mapping_glinttemplate_2014_pkey PRIMARY KEY (productcode);


--
-- Name: mappingcoa mappingcoa_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.mappingcoa
    ADD CONSTRAINT mappingcoa_pkey PRIMARY KEY (account_code_lama);


--
-- Name: mapreconcile mapreconcile_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.mapreconcile
    ADD CONSTRAINT mapreconcile_pkey PRIMARY KEY (mapid);


--
-- Name: mapreconcileaccount mapreconcileaccount_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.mapreconcileaccount
    ADD CONSTRAINT mapreconcileaccount_pkey PRIMARY KEY (mapaccountid);


--
-- Name: masterkurs masterkurs_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.masterkurs
    ADD CONSTRAINT masterkurs_pkey PRIMARY KEY (kode_kurs);


--
-- Name: mustahiqbankaccount mustahiqbankaccount_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.mustahiqbankaccount
    ADD CONSTRAINT mustahiqbankaccount_pk PRIMARY KEY (bankaccountid);


--
-- Name: negara negara_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.negara
    ADD CONSTRAINT negara_pkey PRIMARY KEY (idnegara);


--
-- Name: parameter parameter_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.parameter
    ADD CONSTRAINT parameter_pkey PRIMARY KEY (parametercode);


--
-- Name: parameterglobal parameterglobal_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.parameterglobal
    ADD CONSTRAINT parameterglobal_pkey PRIMARY KEY (kode_parameter);


--
-- Name: parameterinbox parameterinbox_key; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.parameterinbox
    ADD CONSTRAINT parameterinbox_key PRIMARY KEY (kodeinbox);


--
-- Name: parameterjournal parameterjournal_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.parameterjournal
    ADD CONSTRAINT parameterjournal_pkey PRIMARY KEY (parameterjournalid);


--
-- Name: parameterjournalitem parameterjournalitem_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.parameterjournalitem
    ADD CONSTRAINT parameterjournalitem_pkey PRIMARY KEY (parameterjournalitemid);


--
-- Name: periodebalance periodebalance_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.periodebalance
    ADD CONSTRAINT periodebalance_pkey PRIMARY KEY (periodebalance_id);


--
-- Name: periodeprojectbalance periodeprojectbalance_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.periodeprojectbalance
    ADD CONSTRAINT periodeprojectbalance_pkey PRIMARY KEY (periodeprojectbalance_id);


--
-- Name: amortizedcost pk_amortizedcost; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.amortizedcost
    ADD CONSTRAINT pk_amortizedcost PRIMARY KEY (accountno);


--
-- Name: assetcategory pk_assetcategory; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.assetcategory
    ADD CONSTRAINT pk_assetcategory PRIMARY KEY (assetcategoryid);


--
-- Name: branchparameter pk_branchparameter; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.branchparameter
    ADD CONSTRAINT pk_branchparameter PRIMARY KEY (branchcode);


--
-- Name: budget pk_budget; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.budget
    ADD CONSTRAINT pk_budget PRIMARY KEY (budgetid);


--
-- Name: budgetitem pk_budgetitem; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.budgetitem
    ADD CONSTRAINT pk_budgetitem PRIMARY KEY (itemid);


--
-- Name: budgetitemhierarchy pk_budgetitemhierarchy; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.budgetitemhierarchy
    ADD CONSTRAINT pk_budgetitemhierarchy PRIMARY KEY (hierarchyid);


--
-- Name: budgetowner pk_budgetowner; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.budgetowner
    ADD CONSTRAINT pk_budgetowner PRIMARY KEY (ownerid);


--
-- Name: budgetownerhierarchy pk_budgetownerhierarchy; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.budgetownerhierarchy
    ADD CONSTRAINT pk_budgetownerhierarchy PRIMARY KEY (hierarchyid);


--
-- Name: budgetperiod pk_budgetperiod; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.budgetperiod
    ADD CONSTRAINT pk_budgetperiod PRIMARY KEY (periodid);


--
-- Name: budgetrevision pk_budgetrevision; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.budgetrevision
    ADD CONSTRAINT pk_budgetrevision PRIMARY KEY (revisionid);


--
-- Name: budgettransaction pk_budgettransaction; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.budgettransaction
    ADD CONSTRAINT pk_budgettransaction PRIMARY KEY (transactionitemid);


--
-- Name: cashadvancereturninfo pk_cashadvancereturninfo; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.cashadvancereturninfo
    ADD CONSTRAINT pk_cashadvancereturninfo PRIMARY KEY (sourcetransactionid);


--
-- Name: corporatedonor pk_corporatedonor; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.corporatedonor
    ADD CONSTRAINT pk_corporatedonor PRIMARY KEY (donorid);


--
-- Name: costpaidinadvance pk_costpaidinadvance; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.costpaidinadvance
    ADD CONSTRAINT pk_costpaidinadvance PRIMARY KEY (accountno);


--
-- Name: funddailybalance pk_dailybalance; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.funddailybalance
    ADD CONSTRAINT pk_dailybalance PRIMARY KEY (dailybalanceid);


--
-- Name: externaldebtor pk_debtor; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.externaldebtor
    ADD CONSTRAINT pk_debtor PRIMARY KEY (debtorid);


--
-- Name: depreciableasset pk_depreciableasset; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.depreciableasset
    ADD CONSTRAINT pk_depreciableasset PRIMARY KEY (accountno);


--
-- Name: dinarholder pk_dinarholder; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.dinarholder
    ADD CONSTRAINT pk_dinarholder PRIMARY KEY (accountno);


--
-- Name: fixedasset pk_fixedasset; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.fixedasset
    ADD CONSTRAINT pk_fixedasset PRIMARY KEY (accountno);


--
-- Name: fixedassettransactinfo pk_fixedassettransactinfo; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.fixedassettransactinfo
    ADD CONSTRAINT pk_fixedassettransactinfo PRIMARY KEY (transactionitemid);


--
-- Name: fixedassettransactitem pk_fixedassettransactitem; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.fixedassettransactitem
    ADD CONSTRAINT pk_fixedassettransactitem PRIMARY KEY (transactionitemid);


--
-- Name: glinterface pk_glinterface; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.glinterface
    ADD CONSTRAINT pk_glinterface PRIMARY KEY (interfaceid);


--
-- Name: glinterfacecontainer pk_glinterfacecontaider; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.glinterfacecontainer
    ADD CONSTRAINT pk_glinterfacecontaider PRIMARY KEY (glicontainerid);


--
-- Name: glinterfacemember pk_glinterfacemember; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.glinterfacemember
    ADD CONSTRAINT pk_glinterfacemember PRIMARY KEY (glimemberid);


--
-- Name: individualdonor pk_individualdonor; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.individualdonor
    ADD CONSTRAINT pk_individualdonor PRIMARY KEY (donorid);


--
-- Name: inventory pk_inventory; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.inventory
    ADD CONSTRAINT pk_inventory PRIMARY KEY (accountno);


--
-- Name: inventorycategory pk_inventorycategory; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.inventorycategory
    ADD CONSTRAINT pk_inventorycategory PRIMARY KEY (inventorycategoryid);


--
-- Name: investee pk_investee; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.investee
    ADD CONSTRAINT pk_investee PRIMARY KEY (investeeid);


--
-- Name: investment pk_investment; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.investment
    ADD CONSTRAINT pk_investment PRIMARY KEY (accountno);


--
-- Name: investmentcategory pk_investmentcategory; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.investmentcategory
    ADD CONSTRAINT pk_investmentcategory PRIMARY KEY (investmentcatid);


--
-- Name: investmentmanager pk_investmentmanager; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.investmentmanager
    ADD CONSTRAINT pk_investmentmanager PRIMARY KEY (managerid);


--
-- Name: invoicefa pk_invoicefa; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.invoicefa
    ADD CONSTRAINT pk_invoicefa PRIMARY KEY (invoiceid);


--
-- Name: invoice pk_invoiceid; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.invoice
    ADD CONSTRAINT pk_invoiceid PRIMARY KEY (invoiceid);


--
-- Name: invoiceproductdefaultdata pk_invoicepdefaultdata; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.invoiceproductdefaultdata
    ADD CONSTRAINT pk_invoicepdefaultdata PRIMARY KEY (branchcode);


--
-- Name: temptablenew pk_temptablenew; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.temptablenew
    ADD CONSTRAINT pk_temptablenew PRIMARY KEY (accountcode);


--
-- Name: transactionbatch pk_transactionbatch; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactionbatch
    ADD CONSTRAINT pk_transactionbatch PRIMARY KEY (batchid);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (productid);


--
-- Name: productaccount productaccount_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.productaccount
    ADD CONSTRAINT productaccount_pkey PRIMARY KEY (accountno);


--
-- Name: producthierarchy producthierarchy_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.producthierarchy
    ADD CONSTRAINT producthierarchy_pkey PRIMARY KEY (hierarchyid);


--
-- Name: fundproject project_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.fundproject
    ADD CONSTRAINT project_pkey PRIMARY KEY (productid);


--
-- Name: fundprojectaccount projectaccount_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.fundprojectaccount
    ADD CONSTRAINT projectaccount_pk PRIMARY KEY (accountno);


--
-- Name: fundprojectsponsor projectsponsor_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.fundprojectsponsor
    ADD CONSTRAINT projectsponsor_pkey PRIMARY KEY (projectsponsorid);


--
-- Name: projectsponsordisbursement projectsponsordisbursement_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.projectsponsordisbursement
    ADD CONSTRAINT projectsponsordisbursement_pkey PRIMARY KEY (disbid);


--
-- Name: propinsi propinsi_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.propinsi
    ADD CONSTRAINT propinsi_pkey PRIMARY KEY (idpropinsi);


--
-- Name: prospectivedonor prospectivedonor_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.prospectivedonor
    ADD CONSTRAINT prospectivedonor_pkey PRIMARY KEY (prospectivedonorid);


--
-- Name: rakcabang rakcabang_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.rakcabang
    ADD CONSTRAINT rakcabang_pkey PRIMARY KEY (rakcabang_id);


--
-- Name: rakpusat rakpusat_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.rakpusat
    ADD CONSTRAINT rakpusat_pkey PRIMARY KEY (rakpusat_id);


--
-- Name: reconciletransaction recon_pk; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.reconciletransaction
    ADD CONSTRAINT recon_pk PRIMARY KEY (banktransactionid);


--
-- Name: reconcileaccountbalance reconcileaccountbalance_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.reconcileaccountbalance
    ADD CONSTRAINT reconcileaccountbalance_pkey PRIMARY KEY (accountbalanceid);


--
-- Name: registerkurs registerkurs_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.registerkurs
    ADD CONSTRAINT registerkurs_pkey PRIMARY KEY (registerkurs_id);


--
-- Name: rekeningbmm rekeningbmm_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.rekeningbmm
    ADD CONSTRAINT rekeningbmm_pkey PRIMARY KEY (nomorrekening);


--
-- Name: revaluationhistory revaluationhistory_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.revaluationhistory
    ADD CONSTRAINT revaluationhistory_pkey PRIMARY KEY (history_id);


--
-- Name: reversetransaction reversetransaction_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.reversetransaction
    ADD CONSTRAINT reversetransaction_pkey PRIMARY KEY (sourcetransactionid);


--
-- Name: rpvaccount rpvaccount_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.rpvaccount
    ADD CONSTRAINT rpvaccount_pkey PRIMARY KEY (rpv_name);


--
-- Name: rpvaccountdetail rpvaccountdetail_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.rpvaccountdetail
    ADD CONSTRAINT rpvaccountdetail_pkey PRIMARY KEY (currency_code, rpv_name, branch_code);


--
-- Name: salestransaction salestransaction_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.salestransaction
    ADD CONSTRAINT salestransaction_pkey PRIMARY KEY (transactionid);


--
-- Name: script_collection script_collection_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.script_collection
    ADD CONSTRAINT script_collection_pkey PRIMARY KEY (script_code);


--
-- Name: sessionblob sessionblob_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.sessionblob
    ADD CONSTRAINT sessionblob_pkey PRIMARY KEY (id);


--
-- Name: sim_logrun sim_logrun_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.sim_logrun
    ADD CONSTRAINT sim_logrun_pkey PRIMARY KEY (logrun_id);


--
-- Name: sponsor sponsor_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.sponsor
    ADD CONSTRAINT sponsor_pkey PRIMARY KEY (sponsorid);


--
-- Name: sponsortransaction sponsortransaction_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.sponsortransaction
    ADD CONSTRAINT sponsortransaction_pkey PRIMARY KEY (transactionitemid);


--
-- Name: subsysteminteraction subsysteminteraction_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.subsysteminteraction
    ADD CONSTRAINT subsysteminteraction_pkey PRIMARY KEY (subsysteminteraction_id);


--
-- Name: tempcandidatejournal tempcandidatejournal_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.tempcandidatejournal
    ADD CONSTRAINT tempcandidatejournal_pkey PRIMARY KEY (tempcandidatejournal_id);


--
-- Name: temptable_ori temptable_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.temptable_ori
    ADD CONSTRAINT temptable_pkey PRIMARY KEY (accountcode);


--
-- Name: tmp_deletedaccount tmp_deletedaccount_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.tmp_deletedaccount
    ADD CONSTRAINT tmp_deletedaccount_pkey PRIMARY KEY (account_code);


--
-- Name: tmp_gen_productaccount tmp_gen_productaccount_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.tmp_gen_productaccount
    ADD CONSTRAINT tmp_gen_productaccount_pkey PRIMARY KEY (productid, branchcode, currencycode);


--
-- Name: tmp_hctransactiongroup tmp_hctransactiongroup_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.tmp_hctransactiongroup
    ADD CONSTRAINT tmp_hctransactiongroup_pkey PRIMARY KEY (donorid, fundentity, channelaccountno);


--
-- Name: tmp_mapping_repair_zakat tmp_mapping_repair_zakat_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.tmp_mapping_repair_zakat
    ADD CONSTRAINT tmp_mapping_repair_zakat_pkey PRIMARY KEY (accountno_old);


--
-- Name: tmp_mappingproduct1 tmp_mappingproduct1_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.tmp_mappingproduct1
    ADD CONSTRAINT tmp_mappingproduct1_pkey PRIMARY KEY (oldproductcode, fundentity);


--
-- Name: tmp_mappingtran_accountcode2 tmp_mappingtran_accountcode2_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.tmp_mappingtran_accountcode2
    ADD CONSTRAINT tmp_mappingtran_accountcode2_pkey PRIMARY KEY (transactionitemid);


--
-- Name: tmp_mappingtran_accountcode tmp_mappingtran_accountcode_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.tmp_mappingtran_accountcode
    ADD CONSTRAINT tmp_mappingtran_accountcode_pkey PRIMARY KEY (transactionitemid);


--
-- Name: transactionitem transactionitem_pkey; Type: CONSTRAINT; Schema: transaction; Owner: postgres
--

ALTER TABLE ONLY transaction.transactionitem
    ADD CONSTRAINT transactionitem_pkey PRIMARY KEY (transactionitemid);


--
-- Name: idx_tmp_transactiongroup1; Type: INDEX; Schema: transaction; Owner: postgres
--

CREATE INDEX idx_tmp_transactiongroup1 ON transaction.tmp_transactiongroup USING btree (donorid, fundentity, channelaccountno);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

\unrestrict V5aqvig4dGypZstXReMn6jJFynAlG1jjSttvgqFcFCyepbweLHeUKnQrjsrchN3

