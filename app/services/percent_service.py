import sqlite3

def calculate_vote_percentages(law_id: str) -> dict:
    conn = sqlite3.connect("acton.db")
    cur = conn.cursor()
    cur.execute("SELECT vote_type FROM votes WHERE law_id = ?", (law_id,))
    votes = cur.fetchall()
    conn.close()

    total = len(votes)
    yes_count = len([v for (v,) in votes if v == "yes"])
    no_count = total - yes_count

    if total == 0:
        return {"yes": 0, "no": 0}
    return {
        "yes": int((yes_count / total) * 100),
        "no": int((no_count / total) * 100)
    }
