import sqlite3
import os

DB_PATH = "../data/webui.db"


def delete_user_by_email(email):
    """
    Delete a user from the Users table based on their email.
    Returns True if a user was deleted, False otherwise.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM auth WHERE email = ?", (email,))
        conn.commit()
        deleted = cursor.rowcount > 0
    finally:
        cursor.close()
        conn.close()
    return deleted

def clear_db():
    """
    Delete all data from all tables in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Get all table names except for sqlite_sequence (used for autoincrement)
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = [row[0] for row in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"DELETE FROM {table};")
        conn.commit()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    delete_user_by_email("sohanrahman182@gmail.com")