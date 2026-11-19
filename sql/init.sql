
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    amount NUMERIC(12, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS checkpoints (
    source_name TEXT PRIMARY KEY,
    next_cursor INTEGER,
    completed BOOLEAN NOT NULL DEFAULT FALSE
);
