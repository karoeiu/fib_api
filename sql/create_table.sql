CREATE TABLE IF NOT EXISTS fib_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    access_time TEXT NOT NULL,
    input_parameter TEXT NOT NULL,
    status_code INTEGER NOT NULL
)