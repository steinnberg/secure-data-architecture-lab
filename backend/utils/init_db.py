import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth import hash_password
import duckdb

db_path = os.path.join(os.path.dirname(__file__), '..', 'mydata.db')
conn = duckdb.connect(db_path)

conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

hashed = hash_password("admin123")
conn.execute("INSERT INTO users VALUES (?, ?)", ("admin", hashed))
conn.commit()
print("✅ Utilisateur admin ajouté à la base.")
