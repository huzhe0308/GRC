"""User authentication system: register, login, session management."""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import sqlite3
import time
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = APP_ROOT / "runtime" / "users.sqlite"

SESSION_TTL = 86400 * 7


def _get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL DEFAULT '',
            password_hash TEXT NOT NULL,
            salt        TEXT NOT NULL,
            created_at  REAL NOT NULL,
            api_key     TEXT NOT NULL DEFAULT '',
            llm_base_url TEXT NOT NULL DEFAULT '',
            llm_model    TEXT NOT NULL DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token       TEXT PRIMARY KEY,
            user_id     INTEGER NOT NULL,
            username    TEXT NOT NULL,
            created_at  REAL NOT NULL,
            expires_at  REAL NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id     INTEGER PRIMARY KEY,
            settings_json TEXT NOT NULL DEFAULT '{}',
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()


def register_user(username: str, display_name: str, password: str) -> dict:
    username = username.strip().lower()
    if not username or not password:
        return {"ok": False, "error": "Username and password are required"}
    if len(password) < 6:
        return {"ok": False, "error": "Password must be at least 6 characters"}
    init_db()
    conn = _get_db()
    try:
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            return {"ok": False, "error": "Username already exists"}
        salt = secrets.token_hex(16)
        pw_hash = _hash_password(password, salt)
        conn.execute(
            "INSERT INTO users (username, display_name, password_hash, salt, created_at) VALUES (?, ?, ?, ?, ?)",
            (username, display_name or username, pw_hash, salt, time.time()),
        )
        conn.commit()
        user_id = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()["id"]
        token = _create_session(conn, user_id, username)
        conn.close()
        return {"ok": True, "token": token, "user": {"id": user_id, "username": username, "display_name": display_name or username}}
    except Exception as e:
        conn.close()
        return {"ok": False, "error": str(e)}


def login_user(username: str, password: str) -> dict:
    username = username.strip().lower()
    init_db()
    conn = _get_db()
    try:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if not row:
            return {"ok": False, "error": "Invalid username or password"}
        pw_hash = _hash_password(password, row["salt"])
        if pw_hash != row["password_hash"]:
            return {"ok": False, "error": "Invalid username or password"}
        token = _create_session(conn, row["id"], username)
        conn.close()
        return {"ok": True, "token": token, "user": {"id": row["id"], "username": username, "display_name": row["display_name"]}}
    except Exception as e:
        conn.close()
        return {"ok": False, "error": str(e)}


def _create_session(conn: sqlite3.Connection, user_id: int, username: str) -> str:
    now = time.time()
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT OR REPLACE INTO sessions (token, user_id, username, created_at, expires_at) VALUES (?, ?, ?, ?, ?)",
        (token, user_id, username, now, now + SESSION_TTL),
    )
    conn.execute("DELETE FROM sessions WHERE expires_at < ?", (now,))
    conn.commit()
    return token


def verify_token(token: str) -> dict | None:
    if not token:
        return None
    init_db()
    conn = _get_db()
    try:
        row = conn.execute("SELECT * FROM sessions WHERE token = ?", (token,)).fetchone()
        if not row:
            conn.close()
            return None
        if time.time() > row["expires_at"]:
            conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
            conn.commit()
            conn.close()
            return None
        user = conn.execute("SELECT * FROM users WHERE id = ?", (row["user_id"],)).fetchone()
        conn.close()
        if not user:
            return None
        return {"id": user["id"], "username": user["username"], "display_name": user["display_name"], "token": token}
    except Exception:
        conn.close()
        return None


def logout_user(token: str) -> bool:
    init_db()
    conn = _get_db()
    conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return True


def get_user_settings(user_id: int) -> dict:
    init_db()
    conn = _get_db()
    row = conn.execute("SELECT settings_json FROM user_settings WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return json.loads(row["settings_json"])
    return {}


def save_user_settings(user_id: int, settings: dict) -> bool:
    init_db()
    conn = _get_db()
    conn.execute(
        "INSERT OR REPLACE INTO user_settings (user_id, settings_json) VALUES (?, ?)",
        (user_id, json.dumps(settings, ensure_ascii=False)),
    )
    conn.commit()
    conn.close()
    return True


def get_user_api_key(user_id: int) -> str:
    init_db()
    conn = _get_db()
    row = conn.execute("SELECT api_key FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row["api_key"] if row else ""


def set_user_api_key(user_id: int, api_key: str) -> bool:
    init_db()
    conn = _get_db()
    conn.execute("UPDATE users SET api_key = ? WHERE id = ?", (api_key, user_id))
    conn.commit()
    conn.close()
    return True


def get_user_llm_config(user_id: int) -> dict:
    init_db()
    conn = _get_db()
    row = conn.execute("SELECT api_key, llm_base_url, llm_model FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if row:
        return {"api_key": row["api_key"], "base_url": row["llm_base_url"], "model": row["llm_model"]}
    return {"api_key": "", "base_url": "", "model": ""}


def set_user_llm_config(user_id: int, api_key: str, base_url: str, model: str) -> bool:
    init_db()
    conn = _get_db()
    conn.execute("UPDATE users SET api_key = ?, llm_base_url = ?, llm_model = ? WHERE id = ?", (api_key, base_url, model, user_id))
    conn.commit()
    conn.close()
    return True
