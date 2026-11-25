CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    is_verified BOOLEAN NOT NULL,
    violations_qty INTEGER NOT NULL DEFAULT 0
        CHECK (violations_qty >= 0)
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    seller_id INTEGER NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category INTEGER NOT NULL,
    images_qty INTEGER NOT NULL
        CHECK (images_qty >= 0)
);

CREATE INDEX items_seller_id_idx ON items(seller_id);