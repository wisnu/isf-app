CREATE TABLE IF NOT EXISTS otorisasi.submission (
    id              SERIAL PRIMARY KEY,
    entity_type     VARCHAR(50)  NOT NULL,
    module          VARCHAR(50)  NOT NULL,
    branch_code     VARCHAR(10)  NOT NULL,
    payload         JSONB        NOT NULL,
    status          VARCHAR(20)  NOT NULL DEFAULT 'DRAFT'
                    CHECK (status IN ('DRAFT', 'PENDING', 'AUTHORIZED', 'REJECTED')),
    level_current   INTEGER      NOT NULL DEFAULT 0,
    submitted_by    VARCHAR(50)  NOT NULL,
    submitted_at    TIMESTAMPTZ,
    result_entity_id INTEGER,
    created_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_otorisasi_submission_status      ON otorisasi.submission(status);
CREATE INDEX IF NOT EXISTS idx_otorisasi_submission_branch      ON otorisasi.submission(branch_code);
CREATE INDEX IF NOT EXISTS idx_otorisasi_submission_entity_type ON otorisasi.submission(entity_type);
CREATE INDEX IF NOT EXISTS idx_otorisasi_submission_submitted_by ON otorisasi.submission(submitted_by);
CREATE INDEX IF NOT EXISTS idx_otorisasi_submission_status_entity
    ON otorisasi.submission(status, entity_type);
