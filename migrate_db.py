import sqlite3
import os

for path in ['instance/database.db', 'database.db']:
    if os.path.exists(path):
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(users)")
        cols = [r[1] for r in cur.fetchall()]
        if 'age_group' not in cols:
            cur.execute("ALTER TABLE users ADD COLUMN age_group VARCHAR(20) DEFAULT '18-23'")
            conn.commit()
            print(f"Added age_group column to {path}")
        else:
            print(f"{path} already has age_group")
        conn.close()
