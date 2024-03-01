CREATE TABLE db1_user_accounts
(
    id               UNIQUEIDENTIFIER PRIMARY KEY,
    created_at       DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    last_modified_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    email            VARCHAR   NOT NULL,
    name             VARCHAR   NOT NULL,
    firebase_user_id VARCHAR   NOT NULL,
    UNIQUE (firebase_user_id),
    UNIQUE (email)
);

CREATE INDEX idx_firebase_user_id ON db1_user_accounts(firebase_user_id);
CREATE INDEX idx_phone_no ON db1_user_accounts(email);