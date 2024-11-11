CREATE TABLE IF NOT EXISTS fib_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    access_time TEXT NOT NULL,
    input_parameter TEXT NOT NULL,
    result TEXT NOT NULL
)