CREATE TYPE post_category AS ENUM ('electronics', 'fashion', 'grocery', 'medicine', 'toys', 'sports', 'books');
CREATE TABLE posts
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ            DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ            DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID          NOT NULL,
    title            VARCHAR       NOT NULL,
    category         post_category NOT NULL,
    images           TEXT[]                 DEFAULT '{}',
    description      TEXT          NOT NULL,
    cost             NUMERIC       NOT NULL,
    brand            VARCHAR       NOT NULL DEFAULT 'unbranded',
    warranty_yrs     INT           NOT NULL DEFAULT 0,
    warranty_months  INT           NOT NULL DEFAULT 0,
    return_days      INT           NOT NULL DEFAULT 0,
    seller_location  TEXT                   DEFAULT NULL,
    in_box           TEXT                   DEFAULT NULL
);