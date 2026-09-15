"""User authentication system: register, login, session management.

Supports both local SQLite and Turso (HTTP API) via environment variables.
Set TURSO_URL and TURSO_TOKEN to use Turso; otherwise falls back to local SQLite.

Turso URL format: libsql://<db-name>-<org>.turso.io
Turso token: from turso platform tokens create
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import sqlite3
import time
from pathlib import Path
from typing import Any

APP_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = APP_ROOT / "runtime" / "users.sqlite"

SESSION_TTL = 86400 * 7

TURSO_URL = os.environ.get("TURSO_URL", "")
TURSO_TOKEN = os.environ.get("TURSO_TOKEN", "")
TURSO_HTTP_URL = os.environ.get("TURSO_HTTP_URL", "")

_db_initialized = False

SCHEMA_SQL = """
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
"""


class _Row(dict):
    """Dict that supports attribute access, mimicking sqlite3.Row."""
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)


class _TursoConn:
    """Turso HTTP API connection wrapper that mimics sqlite3.Connection."""
    def __init__(self):
        import requests
        self._requests = requests
        self._url = TURSO_HTTP_URL or TURSO_URL.replace("libsql://", "https://")
        self._headers = {"Authorization": f"Bearer {TURSO_TOKEN}", "Content-Type": "application/json"}

    def executescript(self, script: str) -> None:
        statements = [s.strip() for s in script.split(";") if s.strip()]
        for stmt in statements:
            self._execute(stmt, [])

    def execute(self, sql: str, params=None) -> Any:
        return self._execute(sql, params or [])

    def commit(self) -> None:
        pass

    def close(self) -> None:
        pass

    @staticmethod
    def _convert_arg(val):
        if val is None:
            return {"type": "null"}
        if isinstance(val, bool):
            return {"type": "integer", "value": 1 if val else 0}
        if isinstance(val, int):
            return {"type": "integer", "value": val}
        if isinstance(val, float):
            return {"type": "float", "value": val}
        return {"type": "text", "value": str(val)}

    @staticmethod
    def _extract_value(val):
        if not isinstance(val, dict):
            return val
        vtype = val.get("type")
        if vtype == "null":
            return None
        return val.get("value")

    def _execute(self, sql: str, params) -> Any:
        typed_args = [self._convert_arg(p) for p in params]
        resp = self._requests.post(
            f"{self._url}/v3/pipeline",
            headers=self._headers,
            json={"requests": [{"type": "execute", "stmt": {"sql": sql, "args": typed_args}}]},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])
        if not results:
            return _TursoCursor([])

        result = results[0]
        if result.get("type") == "error":
            raise Exception(result.get("error", {}).get("message", "Turso error"))

        resp_data = result.get("response", {})
        if resp_data.get("type") == "execute":
            cols = [c["name"] for c in resp_data.get("cols", [])]
            rows_data = resp_data.get("rows", [])
            rows = []
            for row in rows_data:
                values = [self._extract_value(v) for v in row.get("value", [])]
                rows.append(_Row(zip(cols, values)))
            return _TursoCursor(rows)
        return _TursoCursor([])


class _TursoCursor:
    """Cursor that returns rows and supports fetchone/fetchall."""
    def __init__(self, rows):
        self._rows = rows
        self._idx = 0

    def __iter__(self):
        return iter(self._rows)

    def fetchone(self):
        if self._idx < len(self._rows):
            row = self._rows[self._idx]
            self._idx += 1
            return row
        return None

    def fetchall(self):
        return self._rows[self._idx:]


def _get_db():
    if TURSO_URL or TURSO_HTTP_URL:
        return _TursoConn()
    else:
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn


def init_db() -> None:
    global _db_initialized
    if _db_initialized:
        return
    conn = _get_db()
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    _db_initialized = True


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


def _create_session(conn, user_id: int, username: str) -> str:
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
