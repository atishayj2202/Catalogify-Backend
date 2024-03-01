CREATE TABLE db1_feedbacks
(
    id               UNIQUEIDENTIFIER PRIMARY KEY,
    created_at       DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    last_modified_at DATETIMEOFFSET DEFAULT SYSDATETIMEOFFSET(),
    rating           INT  NOT NULL CHECK (rating > 0),
    feedback         NVARCHAR(MAX) DEFAULT NULL,
    from_user_id     UNIQUEIDENTIFIER NOT NULL,
    FOREIGN KEY (from_user_id) REFERENCES db1_user_accounts (id)
);

CREATE INDEX feedbacks_from_user_id_idx ON db1_feedbacks (from_user_id);
