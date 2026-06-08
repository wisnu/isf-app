CREATE TABLE IF NOT EXISTS otorisasi.approval_log (
    id            SERIAL PRIMARY KEY,
    submission_id INTEGER      NOT NULL REFERENCES otorisasi.submission(id) ON DELETE CASCADE,
    level         INTEGER      NOT NULL,
    authorizer_id VARCHAR(50)  NOT NULL,
    status        VARCHAR(20)  NOT NULL
                  CHECK (status IN ('APPROVED', 'REJECTED')),
    notes         TEXT,
    logged_at     TIMESTAMPTZ     NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_otorisasi_approval_log_submission ON otorisasi.approval_log(submission_id);
