CREATE TABLE otorisasi.approval_log (
    id            SERIAL PRIMARY KEY,
    submission_id INTEGER      NOT NULL REFERENCES otorisasi.submission(id) ON DELETE CASCADE,
    level         INTEGER      NOT NULL,
    authorizer_id VARCHAR(50)  NOT NULL,
    status        VARCHAR(20)  NOT NULL,
    notes         TEXT,
    logged_at     TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_otorisasi_approval_log_submission ON otorisasi.approval_log(submission_id);
