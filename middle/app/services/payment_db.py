import sqlite3
import json
from datetime import datetime

DB_PATH = "middle/payment.db"



def get_db():
    return sqlite3.connect(DB_PATH)

# --- USERS ---
def add_user(email, stripe_customer_id=None):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO users (email, stripe_customer_id) VALUES (?, ?)",
            (email, stripe_customer_id)
        )
        conn.commit()
        return cur.lastrowid

def get_user_by_email(email):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cur.fetchone()

# --- PAYMENTS ---
def add_payment(user_id, stripe_subscription_id, amount, currency, status, plan):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO payments
            (user_id, stripe_subscription_id, amount, currency, status, plan)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, stripe_subscription_id, amount, currency, status, plan)
        )
        conn.commit()
        return cur.lastrowid

def get_payments_for_user(user_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM payments WHERE user_id = ?", (user_id,))
        return cur.fetchall()

# --- VIRTUAL KEYS ---
def add_virtual_key(user_id, key, models, max_budget, duration, metadata, expires_at=None):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO virtual_keys
            (user_id, key, models, max_budget, duration, metadata, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (user_id, key, json.dumps(models), max_budget, duration, json.dumps(metadata), expires_at)
        )
        conn.commit()
        return cur.lastrowid

def get_virtual_keys_for_user(user_id):
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM virtual_keys WHERE user_id = ?", (user_id,))
        return cur.fetchall()

def get_active_virtual_key(user_id):
    now = datetime.utcnow().isoformat()
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute(
            """SELECT * FROM virtual_keys
            WHERE user_id = ? AND (expires_at IS NULL OR expires_at > ?)
            ORDER BY created_at DESC LIMIT 1""",
            (user_id, now)
        )
        return cur.fetchone()

# --- EXAMPLE USAGE ---
if __name__ == "__main__":
    # Add a user
    user_id = add_user("testuser@example.com", "cus_12345")
    print("User ID:", user_id)

    # Add a payment
    payment_id = add_payment(user_id, "sub_67890", 10.0, "USD", "active", "pro")
    print("Payment ID:", payment_id)

    # Add a virtual key
    key_id = add_virtual_key(
        user_id,
        "sk-virtual-123",
        ["gpt-4o", "claude-3-haiku"],
        10.0,
        "30d",
        {"saas_user_id": "user-12345", "subscription_tier": "Pro"},
        None
    )
    print("Virtual Key ID:", key_id)

    # Get user info
    print(get_user_by_email("testuser@example.com"))

    # Get payments
    print(get_payments_for_user(user_id))

    # Get virtual keys
    print(get_virtual_keys_for_user(user_id))

    # Get active virtual key
    print(get_active_virtual_key(user_id)) 