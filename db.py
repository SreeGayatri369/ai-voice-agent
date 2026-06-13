import sqlite3

conn = sqlite3.connect("support.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tickets (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    issue TEXT,
    status TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    role TEXT,
    message TEXT
)
""")

conn.commit()

def save_message(session_id, role, message):
    cursor.execute(
        "INSERT INTO conversations (session_id, role, message) VALUES (?, ?, ?)",
        (session_id, role, message)
    )
    conn.commit()

def get_conversation(session_id):
    cursor.execute(
        "SELECT role, message FROM conversations WHERE session_id=?",
        (session_id,)
    )
    return cursor.fetchall()

def create_ticket(ticket_id, session_id, issue):
    cursor.execute(
        "INSERT INTO tickets VALUES (?, ?, ?, ?)",
        (ticket_id, session_id, issue, "ACTIVE")
    )
    conn.commit()

def get_all_tickets():
    cursor.execute("SELECT * FROM tickets")
    return cursor.fetchall()

def update_ticket(ticket_id, status):
    cursor.execute(
        "UPDATE tickets SET status=? WHERE id=?",
        (status, ticket_id)
    )
    conn.commit()