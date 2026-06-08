CREATE TABLE otorisasi.submission (
    id              SERIAL PRIMARY KEY,
    entity_type     VARCHAR(50)  NOT NULL,
    module          VARCHAR(50)  NOT NULL,
    branch_code     VARCHAR(10)  NOT NULL,
    payload         JSONB        NOT NULL,
    status          VARCHAR(20)  NOT NULL DEFAULT 'DRAFT',
    level_current   INTEGER      NOT NULL DEFAULT 0,
    submitted_by    VARCHAR(50)  NOT NULL,
    submitted_at    TIMESTAMP,
    result_entity_id INTEGER,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_otorisasi_submission_status      ON otorisasi.submission(status);
CREATE INDEX idx_otorisasi_submission_branch      ON otorisasi.submission(branch_code);
CREATE INDEX idx_otorisasi_submission_entity_type ON otorisasi.submission(entity_type);
CREATE INDEX idx_otorisasi_submission_submitted_by ON otorisasi.submission(submitted_by);
