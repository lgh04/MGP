import sqlite3

def create_vote_table():
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            law_id TEXT NOT NULL,
            vote_type TEXT CHECK(vote_type IN ('yes', 'no')) NOT NULL,
            vote_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_vote_table()
