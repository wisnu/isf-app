-- Migration: V012__create_humancapital_tables.sql
-- Portal: zakat
-- Dibuat: 2026-06-15
-- Deskripsi: Membuat tabel untuk fitur Upload Data Penerimaan ZIS Rutin (HC Batch)

-- ============================================================================
-- Table 1: transaction.humancapitalbatch
-- Menyimpan header batch upload HC/payroll per periode
-- ============================================================================

CREATE TABLE IF NOT EXISTS transaction.humancapitalbatch (
    batchid                 SERIAL PRIMARY KEY,
    batchperioddesc         VARCHAR(50)  NOT NULL UNIQUE,  -- Dari cell B2 file XLS, identifikasi periode
    description             VARCHAR(200),                   -- Deskripsi batch (optional)
    uploaddate              TIMESTAMP    NOT NULL DEFAULT NOW(),
    uploaduserid            VARCHAR(50)  NOT NULL,          -- User yang melakukan upload
    transactiondate         DATE         NOT NULL,          -- Tanggal efektif transaksi
    branchcode              VARCHAR(20),
    totalzakat              NUMERIC(20, 4) DEFAULT 0,
    totalinfaq              NUMERIC(20, 4) DEFAULT 0,
    totalanakasuh           NUMERIC(20, 4) DEFAULT 0,
    totalanakyatim          NUMERIC(20, 4) DEFAULT 0,
    totalwakaf              NUMERIC(20, 4) DEFAULT 0,
    totaltaqurma            NUMERIC(20, 4) DEFAULT 0,
    grandtotal              NUMERIC(20, 4) DEFAULT 0,
    totalrecord             INTEGER      DEFAULT 0,
    submissionid            INTEGER,    -- FK ke otorisasi.submission (nullable, set setelah submit)
    created_at              TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_humancapitalbatch_batchperioddesc
    ON transaction.humancapitalbatch(batchperioddesc);

CREATE INDEX IF NOT EXISTS idx_humancapitalbatch_transactiondate
    ON transaction.humancapitalbatch(transactiondate);

CREATE INDEX IF NOT EXISTS idx_humancapitalbatch_uploaduserid
    ON transaction.humancapitalbatch(uploaduserid);

-- ============================================================================
-- Table 2: transaction.humancapitalbatchitem
-- Menyimpan baris-baris detail dari file XLS (per karyawan per jenis dana)
-- ============================================================================

CREATE TABLE IF NOT EXISTS transaction.humancapitalbatchitem (
    batchitemid             SERIAL PRIMARY KEY,
    batchid                 INTEGER      NOT NULL REFERENCES transaction.humancapitalbatch(batchid) ON DELETE CASCADE,
    datano                  INTEGER,
    businessareacode        VARCHAR(20),
    businessareadescription VARCHAR(200),
    employeenumber          VARCHAR(30),                     -- NIP karyawan
    name                    VARCHAR(200),                    -- Nama karyawan
    birthplace              VARCHAR(150),
    workareaname            VARCHAR(100),
    mobilephone             VARCHAR(20),
    birthdate               DATE,
    gender                  VARCHAR(1),                      -- 'L' = MALE, 'P' = FEMALE
    maritalstatus           VARCHAR(1),                      -- 'K' = MARRIED, 'B' = SINGLE, 'S' = DIVORCED/WIDOW
    position                VARCHAR(200),
    organizationalunit      VARCHAR(200),
    amountzakat             NUMERIC(20, 4) DEFAULT 0,
    amountinfaq             NUMERIC(20, 4) DEFAULT 0,
    amountanakasuh          NUMERIC(20, 4) DEFAULT 0,
    amountanakyatim         NUMERIC(20, 4) DEFAULT 0,
    amountwakaf             NUMERIC(20, 4) DEFAULT 0,       -- NOT diproses ke transaksi (disabled)
    amountqurban            NUMERIC(20, 4) DEFAULT 0,
    totalamount             NUMERIC(20, 4) DEFAULT 0,
    description             VARCHAR(200),
    validationdesc          VARCHAR(120),
    transactionid           INTEGER,                         -- Link ke transaction.transaction setelah authorize
    donorid                 INTEGER,                         -- FK ke fund.donor.donorid
    iscreateemployeedata    VARCHAR(1)   DEFAULT 'N',       -- 'T' = donor baru, 'F' = existing
    isprocessed             VARCHAR(1)   DEFAULT 'N',       -- 'Y' = sudah diproses ke transaksi
    smslogid                INTEGER,
    smslogtime              TIMESTAMP,
    created_at              TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_humancapitalbatchitem_batchid
    ON transaction.humancapitalbatchitem(batchid);

CREATE INDEX IF NOT EXISTS idx_humancapitalbatchitem_donorid
    ON transaction.humancapitalbatchitem(donorid);

CREATE INDEX IF NOT EXISTS idx_humancapitalbatchitem_employeenumber
    ON transaction.humancapitalbatchitem(employeenumber);

CREATE INDEX IF NOT EXISTS idx_humancapitalbatchitem_transactionid
    ON transaction.humancapitalbatchitem(transactionid);

-- ============================================================================
-- Table 3: transaction.humancapitalpassedreport
-- Menyimpan donatur internal yang TIDAK ada di file batch (absen)
-- ============================================================================

CREATE TABLE IF NOT EXISTS transaction.humancapitalpassedreport (
    passedreportid          SERIAL PRIMARY KEY,
    batchid                 INTEGER      NOT NULL REFERENCES transaction.humancapitalbatch(batchid) ON DELETE CASCADE,
    employeenumber          VARCHAR(30),
    donorid                 INTEGER,                         -- FK ke fund.donor.donorid
    branchcode              VARCHAR(20),
    tglreport               TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_humancapitalpassedreport_batchid
    ON transaction.humancapitalpassedreport(batchid);

CREATE INDEX IF NOT EXISTS idx_humancapitalpassedreport_donorid
    ON transaction.humancapitalpassedreport(donorid);
