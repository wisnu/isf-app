--
-- PostgreSQL database dump
--

\restrict otcnKTeSdEBUTeFR2734pRFr4KLCY8n1trvpFh5UpoH5SvHLCS9dczAxeqi7NkE

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
-- Name: isf_auth; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA isf_auth;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: audit_log; Type: TABLE; Schema: isf_auth; Owner: -
--

CREATE TABLE isf_auth.audit_log (
    id bigint NOT NULL,
    ts timestamp with time zone DEFAULT now() NOT NULL,
    event character varying(80) NOT NULL,
    user_id character varying(20),
    tenant_id character varying(40),
    ip character varying(64),
    ua text,
    payload jsonb
);


--
-- Name: audit_log_id_seq; Type: SEQUENCE; Schema: isf_auth; Owner: -
--

CREATE SEQUENCE isf_auth.audit_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: isf_auth; Owner: -
--

ALTER SEQUENCE isf_auth.audit_log_id_seq OWNED BY isf_auth.audit_log.id;


--
-- Name: menu; Type: TABLE; Schema: isf_auth; Owner: -
--

CREATE TABLE isf_auth.menu (
    menu_key character varying(64) NOT NULL,
    label character varying(120) NOT NULL,
    group_label character varying(60) NOT NULL,
    route_path character varying(200),
    sort_order integer DEFAULT 0 NOT NULL,
    status character(1) DEFAULT 'A'::bpchar NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


--
-- Name: role_menu; Type: TABLE; Schema: isf_auth; Owner: -
--

CREATE TABLE isf_auth.role_menu (
    id_peran character varying(30) NOT NULL,
    menu_key character varying(64) NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    created_by character varying(20)
);


--
-- Name: tenant_memberships; Type: TABLE; Schema: isf_auth; Owner: -
--

CREATE TABLE isf_auth.tenant_memberships (
    user_id character varying(20) NOT NULL,
    tenant_id character varying(40) NOT NULL,
    is_default boolean DEFAULT false NOT NULL
);


--
-- Name: tenants; Type: TABLE; Schema: isf_auth; Owner: -
--

CREATE TABLE isf_auth.tenants (
    id character varying(40) NOT NULL,
    name character varying(120) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: user_credentials; Type: TABLE; Schema: isf_auth; Owner: -
--

CREATE TABLE isf_auth.user_credentials (
    user_id character varying(20) NOT NULL,
    password_hash text NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: user_provider_links; Type: TABLE; Schema: isf_auth; Owner: -
--

CREATE TABLE isf_auth.user_provider_links (
    user_id character varying(20) NOT NULL,
    provider character varying(40) NOT NULL,
    external_id text NOT NULL,
    email character varying(255),
    linked_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: isf_auth; Owner: -
--

CREATE TABLE isf_auth.users (
    id character varying(20) NOT NULL,
    username character varying(120) NOT NULL,
    display_name character varying(200) NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: audit_log id; Type: DEFAULT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.audit_log ALTER COLUMN id SET DEFAULT nextval('isf_auth.audit_log_id_seq'::regclass);


--
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (id);


--
-- Name: menu menu_pkey; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.menu
    ADD CONSTRAINT menu_pkey PRIMARY KEY (menu_key);


--
-- Name: role_menu role_menu_pkey; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.role_menu
    ADD CONSTRAINT role_menu_pkey PRIMARY KEY (id_peran, menu_key);


--
-- Name: tenant_memberships tenant_memberships_pkey; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.tenant_memberships
    ADD CONSTRAINT tenant_memberships_pkey PRIMARY KEY (user_id, tenant_id);


--
-- Name: tenants tenants_pkey; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.tenants
    ADD CONSTRAINT tenants_pkey PRIMARY KEY (id);


--
-- Name: user_credentials user_credentials_pkey; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.user_credentials
    ADD CONSTRAINT user_credentials_pkey PRIMARY KEY (user_id);


--
-- Name: user_provider_links user_provider_links_pkey; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.user_provider_links
    ADD CONSTRAINT user_provider_links_pkey PRIMARY KEY (user_id, provider);


--
-- Name: user_provider_links user_provider_links_provider_external_id_key; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.user_provider_links
    ADD CONSTRAINT user_provider_links_provider_external_id_key UNIQUE (provider, external_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: idx_audit_event_ts; Type: INDEX; Schema: isf_auth; Owner: -
--

CREATE INDEX idx_audit_event_ts ON isf_auth.audit_log USING btree (event, ts);


--
-- Name: idx_audit_user_ts; Type: INDEX; Schema: isf_auth; Owner: -
--

CREATE INDEX idx_audit_user_ts ON isf_auth.audit_log USING btree (user_id, ts);


--
-- Name: idx_role_menu_peran; Type: INDEX; Schema: isf_auth; Owner: -
--

CREATE INDEX idx_role_menu_peran ON isf_auth.role_menu USING btree (id_peran);


--
-- Name: role_menu role_menu_menu_key_fkey; Type: FK CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.role_menu
    ADD CONSTRAINT role_menu_menu_key_fkey FOREIGN KEY (menu_key) REFERENCES isf_auth.menu(menu_key) ON DELETE CASCADE;


--
-- Name: tenant_memberships tenant_memberships_tenant_id_fkey; Type: FK CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.tenant_memberships
    ADD CONSTRAINT tenant_memberships_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES isf_auth.tenants(id) ON DELETE CASCADE;


--
-- Name: tenant_memberships tenant_memberships_user_id_fkey; Type: FK CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.tenant_memberships
    ADD CONSTRAINT tenant_memberships_user_id_fkey FOREIGN KEY (user_id) REFERENCES isf_auth.users(id) ON DELETE CASCADE;


--
-- Name: user_credentials user_credentials_user_id_fkey; Type: FK CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.user_credentials
    ADD CONSTRAINT user_credentials_user_id_fkey FOREIGN KEY (user_id) REFERENCES isf_auth.users(id) ON DELETE CASCADE;


--
-- Name: user_provider_links user_provider_links_user_id_fkey; Type: FK CONSTRAINT; Schema: isf_auth; Owner: -
--

ALTER TABLE ONLY isf_auth.user_provider_links
    ADD CONSTRAINT user_provider_links_user_id_fkey FOREIGN KEY (user_id) REFERENCES isf_auth.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict otcnKTeSdEBUTeFR2734pRFr4KLCY8n1trvpFh5UpoH5SvHLCS9dczAxeqi7NkE

