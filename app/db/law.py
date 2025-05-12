import sqlite3

def create_law_table():
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS laws (
            law_id TEXT PRIMARY KEY,
            title TEXT,
            content TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_law_table()
