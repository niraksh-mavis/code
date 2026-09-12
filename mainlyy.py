import sqlite3
import hashlib
import os
from config import Config

def get_db():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db_file = os.path.join(os.path.dirname(__file__), Config.DATABASE_PATH)
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        with open(schema_path, "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

# Vulnerability: Weak Hash Function without Salt (Low/Medium)
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()

# Vulnerability: SQL Injection via Raw String Formatting (Critical/High)
def authenticate_user(username: str, password_plain: str):
    conn = get_db()
    cursor = conn.cursor()
    pwd_hash = hash_password(password_plain)

    # Vulnerable to SQL Injection: ' OR '1'='1
    query = f"SELECT id, username, email, role, bio FROM users WHERE username = '{username}' AND password_hash = '{pwd_hash}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

# Vulnerability: SQL Injection in Search Query (High)
def search_users(term: str):
    conn = get_db()
    cursor = conn.cursor()
    # Unsanitized user query formatted directly into SQL statement
    query = f"SELECT id, username, email, role FROM users WHERE username LIKE '%{term}%' OR bio LIKE '%{term}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_comments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, author, content, created_at FROM comments ORDER BY id DESC")
    comments = cursor.fetchall()
    conn.close()
    return comments

def add_comment(user_id: int, author: str, content: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (user_id, author, content) VALUES (?, ?, ?)", (user_id, author, content))
    conn.commit()
    conn.close()

# Vulnerability: IDOR / Broken Access Control in User Retrieval (Medium)
def get_user_by_id(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role, bio FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user
