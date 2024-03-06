CREATE TABLE assessments(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ            DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ            DEFAULT now()::TIMESTAMPTZ,
    post_id UUID NOT NULL,
    assessment1 BOOLEAN DEFAULT TRUE,
    assessment2 VARCHAR DEFAULT '{}',
    assessment3 BOOLEAN DEFAULT TRUE,
    assessment4 BOOLEAN DEFAULT TRUE,
    assessment5 BOOLEAN DEFAULT TRUE,
    assessment6 VARCHAR DEFAULT NULL,
    total INT DEFAULT 100,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

CREATE INDEX assessment_post_id ON assessments(post_id);