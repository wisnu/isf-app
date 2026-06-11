-- V010: Tabel master pemilik anggaran (Budget Owner)
-- Apply to: mziss_laz, mziss_wakaf

CREATE TABLE IF NOT EXISTS transaction.budgetowner (
    ownerid       SERIAL PRIMARY KEY,
    ownercode     VARCHAR(10)  NOT NULL,
    ownername     VARCHAR(100) NOT NULL,
    level         INTEGER      NOT NULL DEFAULT 1,
    is_detail     VARCHAR(1)   NOT NULL DEFAULT 'T',
    parentownerid INTEGER      REFERENCES transaction.budgetowner(ownerid),
    status        VARCHAR(1)   NOT NULL DEFAULT 'A',
    tglubah       TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    userpengubah  VARCHAR(30),
    terminalubah  VARCHAR(30),
    CONSTRAINT chk_bo_status    CHECK (status    IN ('A', 'N')),
    CONSTRAINT chk_bo_isdetail  CHECK (is_detail IN ('T', 'F')),
    CONSTRAINT chk_bo_parent    CHECK (is_detail = 'F' OR parentownerid IS NOT NULL),
    CONSTRAINT uq_bo_ownercode  UNIQUE (ownercode)
);

COMMENT ON TABLE  transaction.budgetowner IS 'Master pemilik anggaran (Budget Owner)';
COMMENT ON COLUMN transaction.budgetowner.is_detail   IS 'F=node induk/grup, T=node detail/leaf';
COMMENT ON COLUMN transaction.budgetowner.level       IS 'Kedalaman hirarki; root=1';

CREATE TABLE IF NOT EXISTS transaction.budgetownerhierarchy (
    childownerid  INTEGER NOT NULL
        REFERENCES transaction.budgetowner(ownerid) ON DELETE CASCADE,
    parentownerid INTEGER NOT NULL
        REFERENCES transaction.budgetowner(ownerid) ON DELETE CASCADE,
    level         INTEGER NOT NULL,
    PRIMARY KEY (childownerid, parentownerid)
);

COMMENT ON TABLE  transaction.budgetownerhierarchy IS 'Denormalisasi hirarki ancestor-descendant Budget Owner';
COMMENT ON COLUMN transaction.budgetownerhierarchy.level IS '0=self-reference, 1=parent langsung, 2+=ancestor';
