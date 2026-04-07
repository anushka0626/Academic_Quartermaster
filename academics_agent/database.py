import sqlite3
import os
from pathlib import Path

# This ensures the DB is found whether running locally or on Cloud Run
DB_PATH = Path(__file__).parent.resolve() / "quartermaster.db"
def init_db():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    # Table for study notes and research snippets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS archives (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT, -- e.g., 'Veritas Ledger', 'OS Class', 'GenAI'
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_snippet(category, content):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    cursor.execute("INSERT INTO archives (category, content) VALUES (?, ?)", (category, content))
    conn.commit()
    conn.close()

def search_notes(query):
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    # Using OR and LOWER to catch more results across categories and content
    cursor.execute("""
        SELECT category, content FROM archives 
        WHERE LOWER(content) LIKE LOWER(?) 
        OR LOWER(category) LIKE LOWER(?)
    """, (f'%{query}%', f'%{query}%'))
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_db()
    print("Database initialized!")