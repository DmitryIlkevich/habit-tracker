CREATE TABLE IF NOT EXISTS completed_period (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id INTEGER NOT NULL,
    start_date INTEGER NOT NULL,
    end_date INTEGER NOT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT True
);

CREATE TABLE IF NOT EXISTS habit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    period_type INTEGER NOT NULL,
    creation_date TEXT NOT NULL
);