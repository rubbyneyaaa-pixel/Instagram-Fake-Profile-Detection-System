import sqlite3

conn = sqlite3.connect("users.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    insta_id TEXT,
    result TEXT
)
""")

conn.commit()
conn.close()

print("History Table Created Successfully")