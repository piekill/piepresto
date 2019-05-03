import sqlite3
import os

home = os.path.join(os.path.expanduser('~'), ".pypresto")
os.makedirs(home, exist_ok=True)
lite_db = os.path.join(home, "history.db")

history_table = """
    CREATE TABLE IF NOT EXISTS history(
        sql TEXT PRIMARY KEY,
        update_time datetime default current_timestamp
    )
"""
get_history = """
    SELECT sql FROM history ORDER BY update_time DESC LIMIT 50
"""
upsert_history = """
    INSERT INTO history(sql) VALUES (?) ON CONFLICT(sql) DO UPDATE SET update_time = current_timestamp
"""


class DBLite():
    def __init__(self):
        self.connection = sqlite3.connect(lite_db)
        self.connection.execute(history_table)

    def history(self):
        cursor = self.connection.execute(get_history)
        return [row[0] for row in cursor]

    def upsert(self, stmt):
        self.connection.execute(upsert_history, (stmt,))
        self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()

    def __del__(self):
        self.close()
