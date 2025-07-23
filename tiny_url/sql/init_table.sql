CREATE TABLE url_mapping (
    id SERIAL PRIMARY KEY,
    source_url TEXT NOT NULL,
    slug_url TEXT NOT NULL UNIQUE,
    end_validity_date TIMESTAMPTZ,
    clic_count INTEGER DEFAULT 0 NOT NULL
);
CREATE INDEX idx_slug_url ON url_mapping(slug_url);
