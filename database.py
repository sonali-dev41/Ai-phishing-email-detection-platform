import sqlite3

conn = sqlite3.connect("emails.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scan_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    prediction TEXT,
    confidence REAL,
    scan_time TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")