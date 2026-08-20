#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import imaplib
import os
import re
import shutil
import sqlite3
import subprocess
import smtplib
import ssl
import sys
import traceback
import urllib.error
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from email import policy
from email.header import decode_header
from email.message import Message, EmailMessage
from email.parser import BytesParser
from email.utils import getaddresses, parsedate_to_datetime


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


AGENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AGENT_ROOT))
from memory.memory_service import WorkflowMemory, init_memory_db

DEFAULT_CONFIG = AGENT_ROOT / "config.yaml"
CODEX_ROOT = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
OUTLOOK_SKILL = CODEX_ROOT / "skills" / "outlook-access"
WIKI_SKILL = Path(
    os.environ.get(
        "AUTOMOTIVE_WIKI_ROOT",
        str(CODEX_ROOT / "skills" / "automotive-llm-wiki"),
    )
)
SKILL_ROOT = AGENT_ROOT

SUPPORTED_CONVERT_EXTS = {".pdf", ".png", ".jpg", ".jpeg", ".jp2", ".webp", ".gif", ".bmp", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
DIRECT_MARKDOWN_EXTS = {".md", ".markdown", ".txt"}


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def stamp() -> str:
    return now_local().strftime("%Y%m%d-%H%M%S")


def today() -> str:
    return now_local().strftime("%Y-%m-%d")


def safe_name(value: str, limit: int = 120) -> str:
    value = str(value or "").strip()
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", value)
    value = re.sub(r"\s+", " ", value).strip(" ._")
    return (value[:limit].strip(" ._") or "untitled")


def slugify(value: str, limit: int = 90) -> str:
    value = safe_name(value, limit=limit).lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-._")
    return value or "untitled"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    return text[:limit] if limit else text


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        match = re.match(r"^---\r?\n.*?\r?\n---\r?\n?", text, re.S)
        if match:
            return text[match.end() :]
    return text


def write_text(path: Path, text: str) -> None:
    ensure_dir(path.parent)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        example = SKILL_ROOT / "config.example.yaml"
        ensure_dir(path.parent)
        shutil.copy2(example, path)
        print(f"[INIT] Created config from example: {path}")
    raw = read_text(path)
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(raw) or {}
        if not isinstance(data, dict):
            raise ValueError("config root must be a mapping")
        return data
    except ImportError:
        return parse_simple_yaml(raw)


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    current: dict[str, Any] | None = None
    pending_list_key: str | None = None
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not line.startswith(" ") and stripped.endswith(":"):
            key = stripped[:-1]
            root[key] = {}
            current = root[key]
            pending_list_key = None
            continue
        if current is None:
            continue
        if stripped.startswith("- ") and pending_list_key:
            current.setdefault(pending_list_key, []).append(parse_scalar(stripped[2:].strip()))
            continue
        if ":" in stripped:
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                current[key] = []
                pending_list_key = key
            else:
                current[key] = parse_scalar(value)
                pending_list_key = None
    return root


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none"}:
        return None
    try:
        return int(value)
    except ValueError:
        return value


def cfg(config: dict[str, Any], section: str, key: str, default: Any = None) -> Any:
    value = config.get(section, {})
    if isinstance(value, dict):
        return value.get(key, default)
    return default


def cfg_section(config: dict[str, Any], section: str) -> dict[str, Any]:
    value = config.get(section, {})
    return value if isinstance(value, dict) else {}


def resolve_agent_path(value: str | Path, default: str | Path) -> Path:
    raw = str(value or default).strip()
    path = Path(raw)
    return path if path.is_absolute() else AGENT_ROOT / path


def init_db(db_path: Path) -> sqlite3.Connection:
    ensure_dir(db_path.parent)
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        create table if not exists processed_emails (
            entryid text primary key,
            subject text,
            received text,
            processed_at text,
            status text,
            report_path text,
            error text
        )
        """
    )
    conn.execute(
        """
        create table if not exists attachments (
            sha256 text primary key,
            filename text,
            saved_path text,
            markdown_path text,
            imported_path text,
            processed_at text
        )
        """
    )
    conn.execute(
        """
        create table if not exists runs (
            run_id text primary key,
            started_at text,
            finished_at text,
            status text,
            report_path text,
            error text
        )
        """
    )
    conn.commit()
    return conn


def already_processed(conn: sqlite3.Connection, entryid: str) -> bool:
    row = conn.execute("select status from processed_emails where entryid = ?", (entryid,)).fetchone()
    return bool(row and row[0] == "success")


def mark_email(conn: sqlite3.Connection, email: dict[str, Any], status: str, report_path: str = "", error: str = "") -> None:
    conn.execute(
        """
        insert into processed_emails(entryid, subject, received, processed_at, status, report_path, error)
        values (?, ?, ?, ?, ?, ?, ?)
        on conflict(entryid) do update set
            subject=excluded.subject,
            received=excluded.received,
            processed_at=excluded.processed_at,
            status=excluded.status,
            report_path=excluded.report_path,
            error=excluded.error
        """,
        (
            email.get("entryid", ""),
            email.get("subject", ""),
            email.get("received", ""),
            now_local().isoformat(timespec="seconds"),
            status,
            report_path,
            error,
        ),
    )
    conn.commit()


def record_attachment(conn: sqlite3.Connection, item: dict[str, str]) -> None:
    conn.execute(
        """
        insert into attachments(sha256, filename, saved_path, markdown_path, imported_path, processed_at)
        values (?, ?, ?, ?, ?, ?)
        on conflict(sha256) do update set
            filename=excluded.filename,
            saved_path=excluded.saved_path,
            markdown_path=excluded.markdown_path,
            imported_path=excluded.imported_path,
            processed_at=excluded.processed_at
        """,
        (
            item.get("sha256", ""),
            item.get("filename", ""),
            item.get("saved_path", ""),
            item.get("markdown_path", ""),
            item.get("imported_path", ""),
            now_local().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()


def initialize_outlook_com() -> Any:
    try:
        import pythoncom  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pywin32 is required for Outlook COM access. Install with: pip install pywin32") from exc
    pythoncom.CoInitialize()
    return pythoncom


@contextmanager
def outlook_session() -> Any:
    pythoncom = initialize_outlook_com()
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pywin32 is required for Outlook COM access. Install with: pip install pywin32") from exc
    try:
        ol = create_outlook_application(win32com.client)
        yield ol, ol.GetNamespace("MAPI")
    finally:
        pythoncom.CoUninitialize()


def create_outlook_application(win32_client: Any) -> Any:
    candidates = [
        "Outlook.Application",
        "Outlook.Application.16",
        "Outlook.Application.15",
    ]
    last_exc: Exception | None = None
    for progid in candidates:
        for creator in (
            lambda: win32_client.GetActiveObject(progid),
            lambda: win32_client.Dispatch(progid),
        ):
            try:
                return creator()
            except Exception as exc:
                last_exc = exc
                continue
    raise RuntimeError(
        f"Outlook COM is not registered on this machine. Diagnostics: {diagnose_outlook_com()}. "
        "This usually means classic Outlook desktop is not installed, or the installed Office edition does not include Outlook."
    ) from last_exc


def get_outlook() -> tuple[Any, Any]:
    initialize_outlook_com()
    try:
        import win32com.client  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pywin32 is required for Outlook COM access. Install with: pip install pywin32") from exc
    ol = create_outlook_application(win32com.client)
    return ol, ol.GetNamespace("MAPI")


def get_outlook_folder(folder: str | None, mapi: Any | None = None) -> Any:
    if mapi is None:
        _, mapi = get_outlook()
    folder_map = {
        "inbox": 6,
        "sent": 5,
        "drafts": 16,
        "outbox": 4,
        "deleted": 3,
    }
    if not folder:
        return mapi.GetDefaultFolder(6)
    folder_key = str(folder).casefold()
    if folder_key in folder_map:
        return mapi.GetDefaultFolder(folder_map[folder_key])
    return mapi.Folders.Item(folder)


def iter_com_collection(collection: Any) -> list[Any]:
    if collection is None:
        return []
    try:
        count = int(getattr(collection, "Count", 0) or 0)
        return [collection.Item(i) for i in range(1, count + 1)]
    except Exception:
        try:
            return list(collection)
        except Exception:
            return []


def diagnose_outlook_com() -> dict[str, Any]:
    diag: dict[str, Any] = {
        "registered_progids": [],
        "outlook_exe_in_path": [],
        "outlook_process_running": False,
        "click_to_run": {},
        "office_products": [],
    }
    try:
        import winreg  # type: ignore
    except Exception:
        winreg = None  # type: ignore

    if winreg is not None:
        for progid in ("Outlook.Application", "Outlook.Application.16", "Outlook.Application.15"):
            try:
                with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, progid):
                    diag["registered_progids"].append(progid)
            except Exception:
                pass

        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Office\ClickToRun\Configuration") as key:
                for name in ("ProductReleaseIds", "Platform", "ClientVersionToReport", "InstallationPath"):
                    try:
                        diag["click_to_run"][name] = winreg.QueryValueEx(key, name)[0]
                    except Exception:
                        pass
        except Exception:
            pass

        for root_key in (
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        ):
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, root_key) as root:
                    index = 0
                    while True:
                        try:
                            subkey = winreg.EnumKey(root, index)
                        except OSError:
                            break
                        index += 1
                        try:
                            with winreg.OpenKey(root, subkey) as key:
                                display_name = str(winreg.QueryValueEx(key, "DisplayName")[0])
                                if any(term in display_name for term in ("Office", "Outlook", "Microsoft 365")):
                                    diag["office_products"].append(display_name)
                        except Exception:
                            continue
            except Exception:
                continue

    try:
        proc = subprocess.run(
            ["where.exe", "outlook"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )
        diag["outlook_exe_in_path"] = [line.strip() for line in (proc.stdout or "").splitlines() if line.strip()]
    except Exception:
        pass

    try:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "Get-Process OUTLOOK -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10,
            encoding="utf-8",
            errors="replace",
        )
        diag["outlook_process_running"] = bool((proc.stdout or "").strip())
    except Exception:
        pass

    return diag


def safe_outlook_str(value: Any, max_len: int | None = None) -> str:
    if value is None:
        return ""
    try:
        text = str(value)
    except Exception:
        return ""
    return text[:max_len] if max_len else text


def get_email_text(item: Any, max_body: int = 5000) -> str:
    body = safe_outlook_str(getattr(item, "Body", ""), max_body)
    if body:
        return clean_email_body(body)
    html = safe_outlook_str(getattr(item, "HTMLBody", ""), max_body * 2)
    cleaned = re.sub("<[^>]+>", "", html)
    return clean_email_body(cleaned)[:max_body]


def clean_email_body(text: str) -> str:
    if not text:
        return ""
    url_pattern = r"https?://[^\s<>\"'\)]+"
    text = re.sub(url_pattern, "", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"^\s*[\r\n]+", "", text, flags=re.MULTILINE)
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and len(stripped) > 2:
            lines.append(stripped)
    return "\n".join(lines).strip()


def backend_name(config: dict[str, Any], section: str, default: str = "auto") -> str:
    return str(cfg(config, section, "backend", default) or default).casefold()


def resolve_secret(section: dict[str, Any]) -> str:
    if not isinstance(section, dict):
        return ""
    env_name = str(section.get("api_key_env", "") or section.get("password_env", "") or "").strip()
    if env_name:
        value = os.environ.get(env_name, "")
        if value:
            return value
    file_path = str(section.get("password_file", "") or "").strip()
    if file_path:
        path = Path(file_path).expanduser()
        if path.exists():
            return read_text(path).strip()
    value = str(section.get("api_key", "") or section.get("password", "") or "")
    return value.strip()


def normalize_responses_endpoint(base_url: str) -> str:
    base_url = base_url.strip().rstrip("/")
    if not base_url:
        return "https://dashscope.aliyuncs.com/compatible-mode/v1/responses"
    if base_url.endswith("/responses"):
        return base_url
    return f"{base_url}/responses"


def decode_mime_header(value: str | None) -> str:
    if not value:
        return ""
    parts: list[str] = []
    for chunk, charset in decode_header(value):
        if isinstance(chunk, bytes):
            parts.append(chunk.decode(charset or "utf-8", errors="replace"))
        else:
            parts.append(chunk)
    return "".join(parts)


def normalize_imap_folder(folder: str | None) -> str:
    if not folder:
        return "INBOX"
    value = str(folder).strip()
    if not value:
        return "INBOX"
    aliases = {
        "inbox": "INBOX",
        "sent": "Sent",
        "drafts": "Drafts",
        "trash": "Trash",
        "deleted": "Trash",
        "spam": "Junk",
        "junk": "Junk",
    }
    key = value.casefold()
    return aliases.get(key, value)


def parse_email_datetime(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except Exception:
        return None
    if parsed is None:
        return None
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone().replace(tzinfo=None)
    return parsed


def extract_message_text(message: Message, max_body: int) -> str:
    pieces: list[str] = []

    def decode_part(part: Message) -> str:
        payload = part.get_payload(decode=True)
        if payload is None:
            return ""
        charset = part.get_content_charset() or "utf-8"
        try:
            return payload.decode(charset, errors="replace")
        except Exception:
            return payload.decode("utf-8", errors="replace")

    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                continue
            disposition = part.get_content_disposition()
            content_type = part.get_content_type()
            if disposition == "attachment":
                continue
            if content_type in {"text/plain", "text/html"}:
                text = decode_part(part)
                if content_type == "text/html":
                    text = re.sub("<[^>]+>", "", text)
                if text.strip():
                    pieces.append(text.strip())
    else:
        content_type = message.get_content_type()
        text = decode_part(message)
        if content_type == "text/html":
            text = re.sub("<[^>]+>", "", text)
        if text.strip():
            pieces.append(text.strip())

    return "\n".join(pieces)[:max_body]


def extract_message_attachments(message: Message) -> list[tuple[str, bytes]]:
    attachments: list[tuple[str, bytes]] = []
    for part in message.walk():
        if part.is_multipart():
            continue
        filename = part.get_filename()
        disposition = part.get_content_disposition()
        if not filename and disposition != "attachment":
            continue
        data = part.get_payload(decode=True)
        if not data:
            continue
        attachments.append((decode_mime_header(filename) if filename else "attachment", data))
    return attachments


def has_imap_settings(config: dict[str, Any]) -> bool:
    imap_cfg = cfg(config, "mail", "imap", {})
    return isinstance(imap_cfg, dict) and bool(str(imap_cfg.get("host", "") or "").strip())


def has_smtp_settings(config: dict[str, Any]) -> bool:
    smtp_cfg = cfg(config, "send", "smtp", {})
    return isinstance(smtp_cfg, dict) and bool(str(smtp_cfg.get("host", "") or "").strip())


def find_emails_outlook(config: dict[str, Any]) -> list[dict[str, Any]]:
    subject_config = cfg(config, "mail", "subject_contains", [])
    if isinstance(subject_config, str):
        keywords = [subject_config.strip()] if subject_config.strip() else []
    elif isinstance(subject_config, list):
        keywords = [k.strip() for k in subject_config if k.strip()]
    else:
        keywords = []
    if not keywords:
        raise ValueError("mail.subject_contains is required (string or list)")

    sender_filter = str(cfg(config, "mail", "sender_contains", "") or "").casefold()
    days_back = int(cfg(config, "mail", "lookback_days", 3))
    limit = int(cfg(config, "mail", "max_emails", 10))
    cutoff = (dt.datetime.now() - dt.timedelta(days=days_back)).replace(tzinfo=None) if days_back else None
    keywords_folded = [k.casefold() for k in keywords]

    _, mapi = get_outlook()
    folder = get_outlook_folder(cfg(config, "mail", "folder", "inbox"), mapi)
    items = folder.Items
    items.Sort("[ReceivedTime]", True)

    print(f"[MAIL] Searching Outlook folder '{folder.Name}' for keywords: {keywords}")
    results: list[dict[str, Any]] = []
    for item in items:
        try:
            if len(results) >= limit:
                break
            subject = safe_outlook_str(getattr(item, "Subject", ""))
            body = get_email_text(item, int(cfg(config, "mail", "include_body_chars", 4000)))
            sender_name = safe_outlook_str(getattr(item, "SenderName", ""))
            sender_email = safe_outlook_str(getattr(item, "SenderEmailAddress", ""))
            received = getattr(item, "ReceivedTime", None)
            if received:
                received = received.replace(tzinfo=None) if received.tzinfo else received

            if received and cutoff and received < cutoff:
                continue
            if sender_filter and sender_filter not in sender_name.casefold() and sender_filter not in sender_email.casefold():
                continue
            subject_lower = subject.casefold()
            body_lower = body.casefold()
            if not all(kw in subject_lower or kw in body_lower for kw in keywords_folded):
                continue

            attachments = []
            try:
                attachments = [safe_outlook_str(getattr(att, "Filename", "")) for att in iter_com_collection(getattr(item, "Attachments", None))]
            except Exception:
                pass
            results.append(
                {
                    "subject": subject,
                    "sender": f"{sender_name} <{sender_email}>" if sender_email else sender_name,
                    "received": str(received)[:19] if received else "",
                    "body": body,
                    "body_preview": body[:300],
                    "attachments": attachments,
                    "entryid": safe_outlook_str(getattr(item, "EntryID", "")),
                    "item": item,
                }
            )
        except Exception:
            print(f"[MAIL] Skipped an Outlook item: {traceback.format_exc(limit=1).strip()}")
            continue
    print(f"[MAIL] Found {len(results)} matching email(s).")
    return results


def find_emails_imap(config: dict[str, Any]) -> list[dict[str, Any]]:
    subject_config = cfg(config, "mail", "subject_contains", [])
    if isinstance(subject_config, str):
        keywords = [subject_config.strip()] if subject_config.strip() else []
    elif isinstance(subject_config, list):
        keywords = [k.strip() for k in subject_config if k.strip()]
    else:
        keywords = []
    if not keywords:
        raise ValueError("mail.subject_contains is required (string or list)")

    imap_cfg = cfg(config, "mail", "imap", {}) if isinstance(cfg(config, "mail", "imap", {}), dict) else {}
    if not isinstance(imap_cfg, dict) or not str(imap_cfg.get("host", "") or "").strip():
        raise ValueError("mail.imap.host is required for IMAP backend")

    host = str(imap_cfg.get("host", "")).strip()
    port = int(imap_cfg.get("port", 993) or 993)
    username = str(imap_cfg.get("username", "") or "").strip()
    password = resolve_secret(imap_cfg)
    folder = normalize_imap_folder(str(cfg(config, "mail", "folder", imap_cfg.get("folder", "INBOX")) or "INBOX"))
    sender_filter = str(cfg(config, "mail", "sender_contains", "") or "").casefold()
    days_back = int(cfg(config, "mail", "lookback_days", 3))
    limit = int(cfg(config, "mail", "max_emails", 10))
    max_body = int(cfg(config, "mail", "include_body_chars", 4000))
    cutoff = (dt.datetime.now() - dt.timedelta(days=days_back)).replace(tzinfo=None) if days_back else None
    keywords_folded = [k.casefold() for k in keywords]

    print(f"[MAIL] Searching IMAP folder '{folder}' at {host} for keywords: {keywords}")
    if imap_cfg.get("use_ssl", True):
        conn = imaplib.IMAP4_SSL(host, port)
    else:
        conn = imaplib.IMAP4(host, port)
        if bool(imap_cfg.get("starttls", False)):
            conn.starttls(ssl.create_default_context())
    login_status, login_data = conn.login(username, password)
    print(f"[MAIL] IMAP login status: {login_status}")
    try:
        imaplib.Commands["ID"] = ("AUTH", "SELECTED")
        id_status, id_data = conn._simple_command(
            "ID",
            '("name" "daily-mail-wiki-report" "version" "1.0" "vendor" "openai-codex")',
        )
        print(f"[MAIL] IMAP ID status: {id_status} {id_data}")
    except Exception as exc:
        print(f"[MAIL] IMAP ID command skipped: {exc}")
    try:
        list_status, mailbox_data = conn.list()
        mailboxes: list[str] = []
        if mailbox_data:
            for raw in mailbox_data:
                if not raw:
                    continue
                if isinstance(raw, bytes):
                    mailboxes.append(raw.decode("utf-8", errors="replace"))
                else:
                    mailboxes.append(str(raw))
        print(f"[MAIL] IMAP folders: {mailboxes if mailboxes else 'unavailable'}")

        select_candidates = []
        for candidate in [folder, "INBOX", "Inbox", "inbox"]:
            if candidate and candidate not in select_candidates:
                select_candidates.append(candidate)

        status = "NO"
        selected_folder = folder
        select_trace: list[str] = []
        for candidate in select_candidates:
            status, data = conn.select(candidate)
            select_trace.append(f"{candidate}: {status} {data}")
            if status == "OK":
                selected_folder = candidate
                break
        if status != "OK":
            raise RuntimeError(
                f"Unable to select IMAP folder: {folder}. list_status={list_status}. select_trace={select_trace}. Available folders: {mailboxes}"
            )
        print(f"[MAIL] IMAP selected folder: {selected_folder}")

        criteria = ["ALL"]
        if cutoff:
            criteria = ["SINCE", cutoff.strftime("%d-%b-%Y")]
        status, data = conn.search(None, *criteria)
        if status != "OK":
            raise RuntimeError("IMAP search failed")

        uids = data[0].split()
        results: list[dict[str, Any]] = []
        for uid in reversed(uids):
            if len(results) >= limit:
                break
            status, msg_data = conn.fetch(uid, "(RFC822)")
            if status != "OK" or not msg_data:
                continue
            raw_bytes = msg_data[0][1] if isinstance(msg_data[0], tuple) else None
            if not raw_bytes:
                continue
            message = BytesParser(policy=policy.default).parsebytes(raw_bytes)
            subject = decode_mime_header(message.get("Subject"))
            from_name, from_addr = ("", "")
            from_values = getaddresses([message.get("From", "")])
            if from_values:
                from_name, from_addr = from_values[0]
            date_value = parse_email_datetime(message.get("Date"))
            if date_value:
                date_value = date_value.replace(tzinfo=None) if date_value.tzinfo else date_value
            if date_value and cutoff and date_value < cutoff:
                continue
            if sender_filter and sender_filter not in from_name.casefold() and sender_filter not in from_addr.casefold():
                continue
            body = extract_message_text(message, max_body)
            subject_lower = subject.casefold()
            body_lower = body.casefold()
            if not all(kw in subject_lower or kw in body_lower for kw in keywords_folded):
                continue
            attachments = [name for name, _ in extract_message_attachments(message)]
            results.append(
                {
                    "subject": subject,
                    "sender": f"{from_name} <{from_addr}>" if from_addr else from_name,
                    "received": date_value.isoformat(timespec="seconds") if date_value else "",
                    "body": body,
                    "body_preview": body[:300],
                    "attachments": attachments,
                    "entryid": f"imap-{uid.decode(errors='ignore')}",
                    "item": message,
                }
            )
        print(f"[MAIL] Found {len(results)} matching email(s).")
        return results
    finally:
        try:
            conn.logout()
        except Exception:
            pass


def find_emails(config: dict[str, Any]) -> list[dict[str, Any]]:
    backend = backend_name(config, "mail", "auto")
    if backend == "outlook_com":
        return find_emails_outlook(config)
    if backend == "imap":
        return find_emails_imap(config)
    if backend == "auto":
        try:
            return find_emails_outlook(config)
        except Exception as exc:
            raise RuntimeError(
                "Outlook COM is unavailable. Make sure Outlook desktop is installed, signed in, and pywin32 is installed."
            ) from exc
    raise ValueError("mail.backend must be auto, outlook_com, or imap")


def download_attachments(email: dict[str, Any], out_dir: Path, allowed_exts: set[str]) -> list[dict[str, Any]]:
    item = email["item"]
    saved: list[dict[str, Any]] = []
    subject_slug = slugify(email.get("subject", "email"), limit=60)
    email_dir = ensure_dir(out_dir / f"{safe_name(email.get('received', '')[:10])}_{subject_slug}")

    if hasattr(item, "Attachments"):
        attachments = getattr(item, "Attachments", None)
        if not attachments or int(getattr(attachments, "Count", 0) or 0) == 0:
            return saved
        for attachment in iter_com_collection(attachments):
            filename = safe_name(getattr(attachment, "Filename", "attachment"))
            ext = Path(filename).suffix.lower()
            if allowed_exts and ext not in allowed_exts:
                print(f"[SKIP] Attachment extension not allowed: {filename}")
                continue
            dest = unique_path(email_dir / filename)
            attachment.SaveAsFile(str(dest))
            saved.append(
                {
                    "filename": filename,
                    "saved_path": str(dest),
                    "extension": ext,
                    "sha256": sha256_file(dest),
                    "email_subject": str(email.get("subject", "")),
                    "email_received": str(email.get("received", "")),
                }
            )
            print(f"[ATTACH] Saved: {dest}")
        return saved

    if isinstance(item, Message):
        for filename, data in extract_message_attachments(item):
            filename = safe_name(filename)
            ext = Path(filename).suffix.lower()
            if allowed_exts and ext not in allowed_exts:
                print(f"[SKIP] Attachment extension not allowed: {filename}")
                continue
            dest = unique_path(email_dir / filename)
            with dest.open("wb") as fh:
                fh.write(data)
            saved.append(
                {
                    "filename": filename,
                    "saved_path": str(dest),
                    "extension": ext,
                    "sha256": sha256_file(dest),
                    "email_subject": str(email.get("subject", "")),
                    "email_received": str(email.get("received", "")),
                }
            )
            print(f"[ATTACH] Saved: {dest}")
        return saved

    return saved


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for index in range(2, 1000):
        candidate = path.with_name(f"{stem}_{index}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"cannot create unique path for {path}")


def convert_attachment(att: dict[str, Any], config: dict[str, Any], run_dir: Path, markdown_dir: Path) -> str:
    source = Path(att["saved_path"])
    ext = source.suffix.lower()
    ensure_dir(markdown_dir)

    if ext in DIRECT_MARKDOWN_EXTS:
        target = unique_path(markdown_dir / f"{source.stem}.md")
        if ext == ".txt":
            body = read_text(source)
            write_text(target, f"# {source.stem}\n\n{body}")
        else:
            shutil.copy2(source, target)
        return str(target)

    if ext not in SUPPORTED_CONVERT_EXTS:
        return ""

    if not bool(cfg(config, "convert", "enabled", True)):
        print(f"[CONVERT] Disabled, keeping original only: {source}")
        return ""

    wiki_root = resolve_agent_path(cfg(config, "wiki", "root_dir", str(WIKI_SKILL)), WIKI_SKILL)
    mineru_script = wiki_root / "work" / "mineru_api_convert.py"
    if not mineru_script.exists():
        raise FileNotFoundError(f"MinerU converter not found: {mineru_script}")

    before = {p.resolve() for p in markdown_dir.glob("*.md")}
    output_dir = ensure_dir(run_dir / "mineru" / source.stem)
    mode = str(cfg(config, "convert", "mineru_mode", "precise"))
    if mode != "precise":
        raise ValueError("convert.mineru_mode currently supports only 'precise' in the first version")
    cmd = [
        sys.executable,
        str(mineru_script),
        mode,
        "--input",
        str(source),
        "--output",
        str(output_dir),
        "--markdown-dir",
        str(markdown_dir),
        "--language",
        str(cfg(config, "convert", "language", "ch")),
        "--timeout",
        str(int(cfg(config, "convert", "timeout_seconds", 7200))),
        "--interval",
        str(int(cfg(config, "convert", "interval_seconds", 15))),
    ]
    cmd.extend(["--model-version", str(cfg(config, "convert", "model_version", "vlm")), "--ocr"])

    print(f"[CONVERT] Running MinerU for: {source.name}")
    subprocess.run(cmd, check=True, cwd=str(wiki_root / "work"))
    after = sorted((p for p in markdown_dir.glob("*.md") if p.resolve() not in before), key=lambda p: p.stat().st_mtime, reverse=True)
    if not after:
        raise RuntimeError(f"MinerU did not produce Markdown for {source}")
    return str(after[0])


def import_markdown_to_wiki(markdown_path: str, att: dict[str, Any], run_id: str, config: dict[str, Any]) -> str:
    if not markdown_path or not bool(cfg(config, "wiki", "import_markdown", True)):
        return ""

    wiki_root = resolve_agent_path(cfg(config, "wiki", "root_dir", str(WIKI_SKILL)), WIKI_SKILL)
    raw_dir = ensure_dir(wiki_root / "raw" / "documents")
    source = Path(markdown_path)
    body = read_text(source)
    if body.startswith("---"):
        match = re.match(r"^---\r?\n.*?\r?\n---\r?\n?", body, re.S)
        if match:
            body = body[match.end() :]

    imported_name = unique_path(raw_dir / f"incoming-{today()}-{slugify(Path(att['filename']).stem)}.md")
    digest = hashlib.sha256(body.encode("utf-8", errors="replace")).hexdigest()
    frontmatter = [
        "---",
        "source_type: mail-attachment",
        f"ingested: {today()}",
        f"sha256: {digest}",
        f"run_id: {run_id}",
        f"mail_subject: {json.dumps(att.get('email_subject', ''), ensure_ascii=False)}",
        f"mail_received: {json.dumps(att.get('email_received', ''), ensure_ascii=False)}",
        f"original_file: {json.dumps(att.get('filename', ''), ensure_ascii=False)}",
        "---",
        "",
    ]
    write_text(imported_name, "\n".join(frontmatter) + body.strip() + "\n")
    return str(imported_name)


def create_query_page(
    imported_paths: list[str],
    emails: list[dict[str, Any]],
    question: str,
    search_query: str,
    report_title: str,
    run_id: str,
    config: dict[str, Any],
) -> str:
    wiki_root = resolve_agent_path(cfg(config, "wiki", "root_dir", str(WIKI_SKILL)), WIKI_SKILL)
    wiki_dir = wiki_root
    queries_dir = ensure_dir(wiki_dir / "queries")
    page_slug = f"daily-mail-report-{today()}-{run_id}"
    page_path = queries_dir / f"{page_slug}.md"
    source_refs = [Path(path).relative_to(wiki_dir).as_posix() for path in imported_paths if path]
    subject_lines = "\n".join(f"- {email.get('received', '')} | {email.get('subject', '')} | {email.get('sender', '')}" for email in emails)
    source_lines = "\n".join(f"- ^[{src}]" for src in source_refs) or "- No imported source."
    content = f"""---
title: {report_title} {today()}
created: {today()}
updated: {today()}
type: query
tags: [compliance, regulation]
sources: {json.dumps(source_refs, ensure_ascii=False)}
aliases: []
related: []
confidence: medium
---

# {report_title} {today()}

## Question

{question or "- No extracted question."}

## Search Query

{search_query or "- No search query."}

## Matched Emails

{subject_lines or "- No matched email."}

## Imported Sources

{source_lines}

## Notes

This page was generated by the daily mail wiki report workflow. Use the generated report file for the full analysis.
"""
    write_text(page_path, content)
    update_wiki_index(wiki_dir, page_slug, report_title)
    append_wiki_log(wiki_dir, f"## [{today()}] ingest | daily mail report {run_id}\n\n- Imported {len(source_refs)} mail attachment source(s).\n- Created query page `queries/{page_path.name}`.\n")
    return str(page_path)


def extract_question(emails: list[dict[str, Any]], config: dict[str, Any]) -> str:
    max_chars = int(cfg(config, "mail", "question_max_chars", 5000))
    question_parts: list[str] = []
    for email in emails:
        subject = str(email.get("subject", "")).strip()
        body = str(email.get("body", "") or email.get("body_preview", "")).strip()
        if not subject and not body:
            continue
        # The subject is primarily a routing keyword ("票"); the body is the
        # user's question. Include the subject only when the body is empty.
        if body:
            body_lines: list[str] = []
            seen_lines: set[str] = set()
            for line in body.splitlines():
                clean_line = line.strip()
                if clean_line and clean_line not in seen_lines:
                    body_lines.append(clean_line)
                    seen_lines.add(clean_line)
            question_parts.append("\n".join(body_lines))
        else:
            question_parts.append(subject)
    question = "\n\n".join(question_parts).strip()
    question = re.sub(r"\n{3,}", "\n\n", question)
    return question[:max_chars]


def build_query(config: dict[str, Any], emails: list[dict[str, Any]], attachments: list[dict[str, Any]], markdown_paths: list[str], question: str) -> str:
    configured = cfg(config, "wiki", "query_terms", []) or []
    parts: list[str] = []
    if question.strip():
        parts.append(question)
    else:
        parts.extend(str(x) for x in configured if str(x).strip())
        parts.extend(str(email.get("body", "")) for email in emails)
        parts.extend(str(email.get("subject", "")) for email in emails)
    parts.extend(str(att.get("filename", "")) for att in attachments)
    for path in markdown_paths[:3]:
        if path:
            parts.append(read_text(Path(path), limit=1000))
    value = " ".join(parts)
    value = re.sub(r"\s+", " ", value).strip()
    return value[:3000]


def extract_response_text(data: dict[str, Any]) -> str:
    text = str(data.get("output_text") or "").strip()
    if text:
        return text
    chunks: list[str] = []
    for output in data.get("output") or []:
        if not isinstance(output, dict):
            continue
        for content in output.get("content") or []:
            if not isinstance(content, dict):
                continue
            if content.get("type") in {"output_text", "text"} and content.get("text"):
                chunks.append(str(content.get("text", "")).strip())
            elif content.get("text"):
                chunks.append(str(content.get("text", "")).strip())
    return "\n".join(chunk for chunk in chunks if chunk).strip()


def collapse_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def trim_text(text: str, limit: int) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def excerpt_from_hit(hit: dict[str, Any], page_text: str, max_chars: int) -> str:
    clean_text = strip_frontmatter(page_text)
    lines = clean_text.splitlines()
    snippets: list[str] = []
    for match in (hit.get("matches") or [])[:3]:
        line_no = match.get("line")
        try:
            line_index = int(line_no) - 1
        except Exception:
            line_index = -1
        if line_index < 0 or not lines:
            continue
        start = max(0, line_index - 2)
        end = min(len(lines), line_index + 3)
        snippet = "\n".join(lines[start:end]).strip()
        if snippet:
            snippets.append(snippet)
    if snippets:
        return trim_text("\n...\n".join(snippets), max_chars)
    return trim_text(clean_text, max_chars)


def collect_wiki_context(hits: list[dict[str, Any]], config: dict[str, Any]) -> str:
    wiki_root = resolve_agent_path(cfg(config, "wiki", "root_dir", str(WIKI_SKILL)), WIKI_SKILL)
    wiki_dir = wiki_root
    max_pages = int(cfg(config, "llm", "max_pages", 5))
    max_page_chars = int(cfg(config, "llm", "max_page_chars", 2500))
    max_context_chars = int(cfg(config, "llm", "max_context_chars", 18000))
    blocks: list[str] = []
    for index, hit in enumerate(hits[:max_pages], 1):
        rel_path = str(hit.get("path", "")).strip()
        page_path = wiki_dir / rel_path if rel_path else None
        page_text = ""
        if page_path and page_path.exists():
            page_text = read_text(page_path, limit=max_page_chars * 2)
        excerpt = excerpt_from_hit(hit, page_text, max_page_chars) if page_text else ""
        sources = hit.get("sources") or []
        match_lines = []
        for match in (hit.get("matches") or [])[:3]:
            line = match.get("line")
            text = str(match.get("text", "")).strip()
            if text:
                match_lines.append(f"  - line {line}: {text}")
        block = [
            f"[{index}] path: {rel_path or 'unknown'}",
            f"    title: {hit.get('title', '')}",
            f"    score: {hit.get('score', '')}",
            f"    layer: {hit.get('layer', '')}",
        ]
        if sources:
            block.append(f"    sources: {', '.join(str(s) for s in sources)}")
        if match_lines:
            block.append("    matches:")
            block.extend(match_lines)
        if excerpt:
            block.append("    excerpt:")
            block.append("\n".join(f"      {line}" for line in excerpt.splitlines()))
        blocks.append("\n".join(block))
    context = "\n\n".join(blocks).strip()
    return trim_text(context, max_context_chars)


def call_openai_responses(prompt: str, config: dict[str, Any]) -> tuple[str, str]:
    llm_cfg = cfg_section(config, "llm")
    if not isinstance(llm_cfg, dict):
        return "", ""
    api_key = resolve_secret(llm_cfg)
    if not api_key:
        raise RuntimeError("LLM enabled but no API key was found. Set llm.api_key in config.yaml.")
    model = str(llm_cfg.get("model", "gpt-4o-mini") or "gpt-4o-mini").strip()
    base_url = str(llm_cfg.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1") or "https://dashscope.aliyuncs.com/compatible-mode/v1").strip().rstrip("/")
    timeout = int(llm_cfg.get("timeout_seconds", 120) or 120)
    provider = str(llm_cfg.get("provider", "aliyun_bailian") or "aliyun_bailian").lower()
    
    if "openai" in provider or "minimax" in model.lower() or "glm" in model.lower():
        endpoint = f"{base_url}/chat/completions"
        instructions = str(llm_cfg.get("instructions", "") or "").strip()
        messages = [{"role": "user", "content": (instructions + "\n\n" if instructions else "") + prompt}]
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
        }
    else:
        endpoint = f"{base_url}/responses"
        payload = {
            "model": model,
            "input": prompt,
        }
        instructions = str(llm_cfg.get("instructions", "") or "").strip()
        if instructions:
            payload["instructions"] = instructions

    temperature = llm_cfg.get("temperature")
    if temperature is not None and str(temperature).strip() != "":
        payload["temperature"] = float(temperature)

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    data = json.loads(raw or "{}")
    
    if "chat/completions" in endpoint:
        choices = data.get("choices", [])
        if choices and len(choices) > 0:
            text = choices[0].get("message", {}).get("content", "")
            return text.strip(), model
    
    text = extract_response_text(data)
    return text.strip(), model


def fallback_answer(question: str, wiki_context: str, hits: list[dict[str, Any]]) -> str:
    top_paths = [str(hit.get("path", "")).strip() for hit in hits[:3] if str(hit.get("path", "")).strip()]
    path_text = ", ".join(f"`{path}`" for path in top_paths) if top_paths else "no wiki pages"
    question_line = trim_text(question, 600) or "No question could be extracted."
    context_line = trim_text(collapse_whitespace(wiki_context), 900) or "No wiki context available."
    return "\n".join(
        [
            "### Answer",
            "LLM output is unavailable in this run, so this is a fallback extractive answer.",
            "",
            f"Question: {question_line}",
            f"Likely relevant wiki pages: {path_text}",
            "",
            "### Evidence Notes",
            context_line,
            "",
            "### Next Step",
            "Enable llm.enabled and set llm.api_key in config.yaml to switch this section to a model-generated answer.",
        ]
    )


def generate_grounded_answer(question: str, wiki_context: str, hits: list[dict[str, Any]], config: dict[str, Any], memory: WorkflowMemory = None) -> tuple[str, str]:
    llm_cfg = cfg_section(config, "llm")
    if not isinstance(llm_cfg, dict) or not bool(llm_cfg.get("enabled", True)):
        return fallback_answer(question, wiki_context, hits), "fallback-disabled"

    max_context_chars = int(llm_cfg.get("max_context_chars", 18000) or 18000)
    
    memory_context = ""
    similar_answer = None
    if memory:
        similar = memory.find_similar_question(question)
        if similar:
            memory_context = f"\n\n## Similar Past Answer (Similarity: {similar['similarity']:.0%})\nQ: {similar['question']}\nA: {similar['answer']}"
            similar_answer = similar['answer']
    
    prompt = "\n\n".join(
        [
            "You are answering a user email question using only the provided wiki context.",
            "Do not use outside knowledge.",
            "If the evidence is insufficient, say so explicitly.",
            "Cite wiki page paths or raw provenance paths inline when possible.",
            "Return concise Markdown with these sections:",
            "1. Answer",
            "2. Evidence",
            "3. Caveats",
            "4. Suggested Reply",
            "",
            "# Email Question",
            trim_text(question, max_context_chars // 3 or max_context_chars),
            memory_context,
            "",
            "# Wiki Context",
            trim_text(wiki_context, max_context_chars),
        ]
    )

    try:
        answer, model = call_openai_responses(prompt, config)
        if answer:
            return answer, model
    except Exception as exc:
        print(f"[LLM] Model call failed, falling back to extractive answer: {exc}")
        if bool(llm_cfg.get("required", False)):
            raise
    return fallback_answer(question, wiki_context, hits), "fallback"


def update_wiki_index(wiki_dir: Path, page_slug: str, title: str) -> None:
    index_path = wiki_dir / "index.md"
    if not index_path.exists():
        return
    text = read_text(index_path)
    bullet = f"- [[{page_slug}|{title} {today()}]] - Daily Outlook mail wiki report.\n"
    if bullet.strip() in text:
        return
    if "## Queries" not in text:
        text = text.rstrip() + "\n\n## Queries\n\n" + bullet
    else:
        text = text.replace("## Queries\n\n_None yet._", "## Queries\n\n" + bullet)
        if bullet not in text:
            text = text.rstrip() + "\n" + bullet
    write_text(index_path, text)


def append_wiki_log(wiki_dir: Path, entry: str) -> None:
    log_path = wiki_dir / "log.md"
    old = read_text(log_path) if log_path.exists() else "# Wiki Log\n"
    write_text(log_path, old.rstrip() + "\n\n" + entry.strip() + "\n")


def search_wiki(query: str, config: dict[str, Any]) -> list[dict[str, Any]]:
    wiki_root = resolve_agent_path(cfg(config, "wiki", "root_dir", str(WIKI_SKILL)), WIKI_SKILL)
    script = wiki_root / "tools" / "search_wiki.py"
    if not script.exists():
        return []
    normalized_query = re.sub(
        r"是什么|什么意思|有哪些|有什么|如何|怎么|为什么|请问|请介绍|请说明|请分析",
        " ",
        query,
    )
    normalized_query = re.sub(r"[,;，；、/]+", " ", normalized_query)
    normalized_query = re.sub(r"\s+", " ", normalized_query).strip()
    limit = int(cfg(config, "wiki", "search_limit", 8))

    def run_search(include_raw: bool) -> list[dict[str, Any]]:
        cmd = [
            sys.executable,
            str(script),
            normalized_query,
            "--limit",
            str(max(limit * 2, limit)),
            "--no-raw-fallback",
            "--json",
        ]
        if include_raw:
            cmd.append("--raw")
        result = subprocess.run(
            cmd,
            cwd=str(wiki_root),
            text=True,
            encoding="utf-8",
            errors="replace",
            capture_output=True,
            check=True,
        )
        return json.loads(result.stdout or "[]")

    # Query pages are workflow traces, not evidence. Exclude them so today's
    # generated page cannot become tomorrow's strongest search result.
    hits = [hit for hit in run_search(False) if hit.get("layer") != "queries"]
    if bool(cfg(config, "wiki", "search_raw", True)) and len(hits) < limit:
        existing = {str(hit.get("path", "")) for hit in hits}
        for hit in run_search(True):
            if hit.get("layer") == "queries" or str(hit.get("path", "")) in existing:
                continue
            hits.append(hit)
            existing.add(str(hit.get("path", "")))
            if len(hits) >= limit:
                break
    layer_priority = {
        "concepts": 0,
        "comparisons": 1,
        "entities": 2,
        "raw": 3,
    }
    hits.sort(
        key=lambda hit: (
            layer_priority.get(str(hit.get("layer", "")), 4),
            -int(hit.get("score", 0) or 0),
            str(hit.get("path", "")).casefold(),
        )
    )
    return hits[:limit]


def workflow_mode(config: dict[str, Any]) -> str:
    return str(cfg_section(config, "workflow").get("mode", "api") or "api").strip().casefold()


def summarize_email_for_model(email: dict[str, Any]) -> dict[str, Any]:
    return {
        "entryid": str(email.get("entryid", "")),
        "received": str(email.get("received", "")),
        "sender": str(email.get("sender", "")),
        "subject": str(email.get("subject", "")),
        "body": str(email.get("body", "") or email.get("body_preview", "")),
        "attachments": list(email.get("attachments") or []),
    }


def summarize_attachment_for_model(att: dict[str, Any]) -> dict[str, Any]:
    return {
        "filename": str(att.get("filename", "")),
        "saved_path": str(att.get("saved_path", "")),
        "markdown_path": str(att.get("markdown_path", "")),
        "imported_path": str(att.get("imported_path", "")),
        "sha256": str(att.get("sha256", "")),
    }


def build_model_input_bundle(context: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    llm_cfg = cfg_section(config, "llm")
    return {
        "run_id": str(context.get("run_id", "")),
        "generated_at": now_local().isoformat(timespec="seconds"),
        "workflow_mode": workflow_mode(config),
        "mail_keyword": str(cfg(config, "mail", "subject_contains", "")),
        "question": str(context.get("question", "")),
        "search_query": str(context.get("query", "")),
        "query_page": str(context.get("query_page", "")),
        "report_title": str(cfg(config, "report", "title", "Daily Mail Wiki Report")),
        "report_focus": str(cfg(config, "report", "focus", "")),
        "emails": [summarize_email_for_model(email) for email in context.get("emails", [])],
        "attachments": [summarize_attachment_for_model(att) for att in context.get("attachments", [])],
        "wiki_hits": context.get("wiki_hits", []),
        "wiki_context": str(context.get("wiki_context", "")),
        "instructions": str(llm_cfg.get("instructions", "")),
        "report_template": read_text(SKILL_ROOT / "assets" / "report_template.md"),
    }


def format_model_input_markdown(bundle: dict[str, Any]) -> str:
    email_lines = []
    for email in bundle.get("emails") or []:
        email_lines.append(
            f"- `{email.get('received', '')}` {email.get('sender', '')}: {email.get('subject', '')}"
        )
        body = str(email.get("body", "")).strip()
        if body:
            email_lines.append(f"  - Body: {trim_text(body, 1200)}")
    attachment_lines = []
    for att in bundle.get("attachments") or []:
        attachment_lines.append(
            f"- `{att.get('filename', '')}` | markdown: `{att.get('markdown_path', '')}` | wiki: `{att.get('imported_path', '')}`"
        )
    hit_lines = format_wiki_hits(bundle.get("wiki_hits") or [], True)
    wiki_context = str(bundle.get("wiki_context", "")).strip() or "- No wiki context."
    report_template = str(bundle.get("report_template", "")).strip()
    return "\n".join(
        [
            "# Model Input",
            "",
            f"- Run ID: `{bundle.get('run_id', '')}`",
            f"- Generated: `{bundle.get('generated_at', '')}`",
            f"- Mode: `{bundle.get('workflow_mode', '')}`",
            f"- Mail keyword: `{bundle.get('mail_keyword', '')}`",
            f"- Query page: `{bundle.get('query_page', '')}`",
            "",
            "## Question",
            "",
            str(bundle.get("question", "")).strip() or "- No question extracted.",
            "",
            "## Search Query",
            "",
            str(bundle.get("search_query", "")).strip() or "- No search query.",
            "",
            "## Matched Emails",
            "",
            "\n".join(email_lines) or "- No matched emails.",
            "",
            "## Attachments",
            "",
            "\n".join(attachment_lines) or "- No attachments.",
            "",
            "## Wiki Hits",
            "",
            hit_lines or "- No wiki hits.",
            "",
            "## Wiki Context",
            "",
            "```text",
            wiki_context,
            "```",
            "",
            "## Instructions",
            "",
            str(bundle.get("instructions", "")).strip() or "- No instructions configured.",
            "",
            "## Report Template",
            "",
            "```md",
            trim_text(report_template, 12000),
            "```",
            "",
        ]
    )


def write_model_input_bundle(bundle: dict[str, Any], run_dir: Path) -> tuple[Path, Path]:
    json_path = run_dir / "model_input.json"
    md_path = run_dir / "model_input.md"
    write_text(json_path, json.dumps(bundle, ensure_ascii=False, indent=2))
    write_text(md_path, format_model_input_markdown(bundle))
    return json_path, md_path


def risk_level(text: str, hits: list[dict[str, Any]]) -> str:
    high_terms = ["强制", "mandatory", "shall", "必须", "型式认证", "type approval", "召回", "违法", "不符合", "effective date", "生效"]
    medium_terms = ["requirement", "要求", "测试", "验证", "合规", "compliance", "风险", "risk", "安全"]
    hay = (text + " " + json.dumps(hits, ensure_ascii=False)).lower()
    if any(term.lower() in hay for term in high_terms):
        return "High"
    if any(term.lower() in hay for term in medium_terms):
        return "Medium"
    return "Low"


def generate_report(context: dict[str, Any], config: dict[str, Any], report_path: Path) -> str:
    template_path = SKILL_ROOT / "assets" / "report_template.md"
    template = read_text(template_path)
    hits = context["wiki_hits"]
    emails = context["emails"]
    attachments = context["attachments"]
    risk = risk_level(context["query"], hits)
    question = str(context.get("question", "") or "").strip() or "No question could be extracted from the matched email body."
    answer = str(context.get("answer", "") or "").strip() or "No answer was generated."
    answer_source = str(context.get("answer_source", "") or "").strip() or "unknown"

    email_lines = "\n".join(
        f"- `{email.get('received', '')}` {email.get('sender', '')}: {email.get('subject', '')}"
        for email in emails
    ) or "- No matched emails."
    attachment_lines = "\n".join(
        f"- `{att.get('filename', '')}` | saved: `{att.get('saved_path', '')}` | markdown: `{att.get('markdown_path', '')}` | wiki: `{att.get('imported_path', '')}`"
        for att in attachments
    ) or "- No processed attachments."
    evidence_lines = format_wiki_hits(hits, bool(cfg(config, "report", "include_wiki_snippets", True)))
    summary = f"Matched {len(emails)} email(s), extracted an email-body question, processed {len(attachments)} attachment(s), imported {len([a for a in attachments if a.get('imported_path')])} wiki source(s), found {len(hits)} wiki evidence hit(s), and generated a wiki-grounded answer via {answer_source}. Preliminary risk level: {risk}."
    analysis = build_analysis(risk, hits, config)
    actions = build_actions(risk, hits)
    trace = "\n".join(
        [
            f"- Query page: `{context.get('query_page', '')}`",
            f"- Search query: `{context['query'][:500]}`",
            f"- Answer source: `{answer_source}`",
            "- Analysis mode: email question -> wiki retrieval -> bounded wiki context -> model or explicit fallback answer.",
        ]
    )
    rendered = template.format(
        title=str(cfg(config, "report", "title", "Daily Mail Wiki Report")),
        run_id=context["run_id"],
        generated_at=now_local().isoformat(timespec="seconds"),
        mail_keyword=str(cfg(config, "mail", "subject_contains", "")),
        status="dry-run" if bool(cfg(config, "send", "dry_run", True)) else "send-enabled",
        summary=summary,
        question=question,
        answer=answer,
        emails=email_lines,
        attachments=attachment_lines,
        wiki_evidence=evidence_lines,
        analysis=analysis,
        actions=actions,
        trace=trace,
    )
    write_text(report_path, rendered)
    return rendered


def format_wiki_hits(hits: list[dict[str, Any]], include_snippets: bool) -> str:
    if not hits:
        return "- No wiki hits found."
    lines: list[str] = []
    for index, hit in enumerate(hits, 1):
        lines.append(f"{index}. `{hit.get('path', '')}` - {hit.get('title', '')} (score: {hit.get('score', '')})")
        sources = hit.get("sources") or []
        if sources:
            lines.append(f"   Sources: {', '.join(str(s) for s in sources)}")
        if include_snippets:
            for match in (hit.get("matches") or [])[:2]:
                lines.append(f"   Line {match.get('line')}: {match.get('text')}")
    return "\n".join(lines)


def build_analysis(risk: str, hits: list[dict[str, Any]], config: dict[str, Any]) -> str:
    focus = str(cfg(config, "report", "focus", "regulatory impact and compliance actions"))
    layers = sorted({str(hit.get("layer", "")) for hit in hits if hit.get("layer")})
    tags = sorted({str(tag) for hit in hits for tag in (hit.get("tags") or [])})
    return "\n".join(
        [
            f"- Focus: {focus}",
            f"- Preliminary risk: {risk}",
            f"- Evidence layers: {', '.join(layers) if layers else 'none'}",
            f"- Related tags: {', '.join(tags[:20]) if tags else 'none'}",
            "- Interpretation: Review the matched wiki pages and raw provenance before making compliance commitments.",
        ]
    )


def build_actions(risk: str, hits: list[dict[str, Any]]) -> str:
    actions = [
        "Review the imported source Markdown and the generated query page.",
        "Check the top wiki matches for jurisdiction, effective date, vehicle scope, and test evidence impact.",
    ]
    if risk == "High":
        actions.append("Open a follow-up action with the responsible compliance or system owner before external distribution.")
    if any("cybersecurity" in (hit.get("tags") or []) for hit in hits):
        actions.append("Route cybersecurity-related changes to the CSMS or security engineering owner.")
    if any("functional-safety" in (hit.get("tags") or []) or "sotif" in (hit.get("tags") or []) for hit in hits):
        actions.append("Route safety-related changes to the FuSa/SOTIF owner for impact assessment.")
    return "\n".join(f"- {action}" for action in actions)


def send_report_outlook(report_path: Path, report_text: str, config: dict[str, Any]) -> None:
    recipients = cfg(config, "send", "to", []) or []
    cc = cfg(config, "send", "cc", []) or []
    if isinstance(recipients, str):
        recipients = [recipients]
    if isinstance(cc, str):
        cc = [cc]
    recipients = [str(x).strip() for x in recipients if str(x).strip()]
    cc = [str(x).strip() for x in cc if str(x).strip()]
    if not recipients:
        raise ValueError("send.to must contain at least one recipient")

    subject = f"{cfg(config, 'send', 'subject_prefix', '[Daily Mail Wiki Report]')} {today()}"
    body = str(cfg(config, "send", "body", "Please find the attached report."))
    body = body + f"\n\nReport: {report_path}\n\n" + report_text[:1500]
    if bool(cfg(config, "send", "dry_run", True)):
        print("[DRY-RUN] Would send Outlook email:")
        print(f"  To: {', '.join(recipients)}")
        if cc:
            print(f"  CC: {', '.join(cc)}")
        print(f"  Subject: {subject}")
        print(f"  Attachment: {report_path}")
        return

    with outlook_session() as (ol, _):
        mail = ol.CreateItem(0)
        mail.To = ";".join(recipients)
        if cc:
            mail.CC = ";".join(cc)
        mail.Subject = subject
        mail.Body = body
        mail.Attachments.Add(str(report_path))
        mail.Send()
    print(f"[MAIL] Report sent to: {', '.join(recipients)}")


def send_report_smtp(report_path: Path, report_text: str, config: dict[str, Any]) -> None:
    recipients = cfg(config, "send", "to", []) or []
    cc = cfg(config, "send", "cc", []) or []
    if isinstance(recipients, str):
        recipients = [recipients]
    if isinstance(cc, str):
        cc = [cc]
    recipients = [str(x).strip() for x in recipients if str(x).strip()]
    cc = [str(x).strip() for x in cc if str(x).strip()]
    if not recipients:
        raise ValueError("send.to must contain at least one recipient")

    smtp_cfg = cfg(config, "send", "smtp", {}) if isinstance(cfg(config, "send", "smtp", {}), dict) else {}
    if not isinstance(smtp_cfg, dict) or not str(smtp_cfg.get("host", "") or "").strip():
        raise ValueError("send.smtp.host is required for SMTP backend")

    host = str(smtp_cfg.get("host", "")).strip()
    port = int(smtp_cfg.get("port", 465) or 465)
    username = str(smtp_cfg.get("username", "") or "").strip()
    password = resolve_secret(smtp_cfg)
    use_ssl = bool(smtp_cfg.get("use_ssl", True))
    starttls = bool(smtp_cfg.get("starttls", False))
    from_addr = str(smtp_cfg.get("from_address", "") or username).strip() or username
    subject = f"{cfg(config, 'send', 'subject_prefix', '[Daily Mail Wiki Report]')} {today()}"
    body = str(cfg(config, "send", "body", "Please find the attached report."))
    body = body + f"\n\nReport: {report_path}\n\n" + report_text[:1500]

    if bool(cfg(config, "send", "dry_run", True)):
        print("[DRY-RUN] Would send SMTP email:")
        print(f"  To: {', '.join(recipients)}")
        if cc:
            print(f"  CC: {', '.join(cc)}")
        print(f"  From: {from_addr}")
        print(f"  Subject: {subject}")
        print(f"  Attachment: {report_path}")
        return

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(recipients)
    if cc:
        msg["Cc"] = ", ".join(cc)
    msg.set_content(body)
    report_bytes = report_path.read_bytes()
    msg.add_attachment(report_bytes, maintype="text", subtype="markdown", filename=report_path.name)

    if use_ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            if username or password:
                server.login(username, password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(host, port) as server:
            if starttls:
                server.starttls(context=ssl.create_default_context())
            if username or password:
                server.login(username, password)
            server.send_message(msg)
    print(f"[MAIL] SMTP report sent to: {', '.join(recipients)}")


def send_report(report_path: Path, report_text: str, config: dict[str, Any]) -> None:
    backend = backend_name(config, "send", "auto")
    if backend == "outlook_com":
        return send_report_outlook(report_path, report_text, config)
    if backend == "smtp":
        return send_report_smtp(report_path, report_text, config)
    if backend == "auto":
        try:
            return send_report_outlook(report_path, report_text, config)
        except Exception as exc:
            raise RuntimeError(
                "Outlook COM send is unavailable. Make sure Outlook desktop is installed, signed in, and pywin32 is installed."
            ) from exc
    raise ValueError("send.backend must be auto, outlook_com, or smtp")


def send_existing_report(config_path: Path, report_path: Path, send_dry_run_override: bool | None = None) -> int:
    config = load_config(config_path)
    if send_dry_run_override is not None:
        config.setdefault("send", {})["dry_run"] = send_dry_run_override
    if not report_path.exists():
        raise FileNotFoundError(f"Report file does not exist: {report_path}")
    report_text = read_text(report_path)
    send_report(report_path, report_text, config)
    print(f"[OK] Existing report handled by mail backend: {report_path}")
    return 0


def run(config_path: Path, force: bool = False, mode_override: str | None = None, send_dry_run_override: bool | None = None) -> int:
    config = load_config(config_path)
    if send_dry_run_override is not None:
        config.setdefault("send", {})["dry_run"] = send_dry_run_override
    run_mode = str(mode_override or workflow_mode(config) or "api").strip().casefold()
    if run_mode not in {"api", "codex_assisted"}:
        raise ValueError("workflow.mode must be api or codex_assisted")
    root_dir = resolve_agent_path(cfg(config, "workflow", "root_dir", str(DEFAULT_CONFIG.parent)), DEFAULT_CONFIG.parent)
    run_id = stamp()
    run_dir = ensure_dir(root_dir / "runs" / run_id)
    logs_dir = ensure_dir(root_dir / "logs")
    downloads_dir = ensure_dir(root_dir / "downloads" / run_id)
    markdown_dir = ensure_dir(root_dir / "markdown" / run_id)
    reports_dir = ensure_dir(root_dir / "reports")
    db = init_db(root_dir / "state.sqlite")
    report_path = reports_dir / f"daily-mail-wiki-report-{run_id}.md"
    
    memory_enabled = bool(cfg(config, "memory", "enabled", False))
    memory = None
    if memory_enabled:
        memory_db_path = resolve_agent_path(cfg(config, "memory", "db_path", "runtime/memory.sqlite"), root_dir)
        try:
            memory = WorkflowMemory(memory_db_path)
            print(f"[MEMORY] Enabled, database: {memory_db_path}")
        except Exception as exc:
            print(f"[MEMORY] Failed to initialize: {exc}")
            memory = None

    db.execute("insert or replace into runs(run_id, started_at, status) values (?, ?, ?)", (run_id, now_local().isoformat(timespec="seconds"), "running"))
    db.commit()
    try:
        emails = find_emails(config)
        target_emails = [email for email in emails if force or not already_processed(db, email.get("entryid", ""))]
        if not target_emails:
            print("[OK] No new target emails.")
            db.execute("update runs set finished_at=?, status=?, report_path=? where run_id=?", (now_local().isoformat(timespec="seconds"), "no-new-mail", "", run_id))
            db.commit()
            return 0

        question = extract_question(target_emails, config)
        allowed_exts = {str(x).lower() for x in (cfg(config, "attachments", "allowed_extensions", []) or [])}
        processed_attachments: list[dict[str, Any]] = []
        for email in target_emails:
            try:
                downloaded = download_attachments(email, downloads_dir, allowed_exts)
                if bool(cfg(config, "attachments", "require_attachment", True)) and not downloaded:
                    mark_email(db, email, "skipped-no-attachment")
                    continue
                for att in downloaded:
                    markdown_path = convert_attachment(att, config, run_dir, markdown_dir)
                    att["markdown_path"] = markdown_path
                    att["imported_path"] = import_markdown_to_wiki(markdown_path, att, run_id, config) if markdown_path else ""
                    record_attachment(db, {k: str(v) for k, v in att.items()})
                    processed_attachments.append(att)
                mark_email(db, email, "processed")
            except Exception as exc:
                mark_email(db, email, "error", error=str(exc))
                raise

        imported_paths = [att.get("imported_path", "") for att in processed_attachments if att.get("imported_path")]
        markdown_paths = [att.get("markdown_path", "") for att in processed_attachments if att.get("markdown_path")]
        query = build_query(config, target_emails, processed_attachments, markdown_paths, question)
        wiki_hits = search_wiki(query or str(cfg(config, "mail", "subject_contains", "")), config)
        wiki_context = collect_wiki_context(wiki_hits, config)
        query_page = create_query_page(
            imported_paths,
            target_emails,
            question,
            query,
            str(cfg(config, "report", "title", "Daily Mail Wiki Report")),
            run_id,
            config,
        )
        base_context = {
            "run_id": run_id,
            "emails": target_emails,
            "attachments": processed_attachments,
            "query_page": query_page,
            "query": query,
            "wiki_hits": wiki_hits,
            "wiki_context": wiki_context,
            "question": question,
        }
        if run_mode == "codex_assisted":
            bundle = build_model_input_bundle(base_context, config)
            json_path, md_path = write_model_input_bundle(bundle, run_dir)
            for email in target_emails:
                mark_email(db, email, "codex-input-ready")
            db.execute(
                "update runs set finished_at=?, status=?, report_path=? where run_id=?",
                (now_local().isoformat(timespec="seconds"), "codex-input-ready", str(md_path), run_id),
            )
            db.commit()
            print(f"[OK] Codex-assisted model input generated: {md_path}")
            print(f"[OK] Model input JSON: {json_path}")
            return 0

        answer, answer_source = generate_grounded_answer(question, wiki_context, wiki_hits, config, memory)
        
        if memory and bool(cfg(config, "memory", "auto_learn", True)):
            wiki_pages = [hit.get("path", "") for hit in wiki_hits if hit.get("path")]
            memory.store_question_answer(run_id, question, answer, wiki_pages)
            print(f"[MEMORY] Stored Q&A pair")
        
        report_text = generate_report(
            {
                **base_context,
                "answer": answer,
                "answer_source": answer_source,
            },
            config,
            report_path,
        )
        send_report(report_path, report_text, config)
        for email in target_emails:
            mark_email(db, email, "success", report_path=str(report_path))
        db.execute("update runs set finished_at=?, status=?, report_path=? where run_id=?", (now_local().isoformat(timespec="seconds"), "success", str(report_path), run_id))
        db.commit()
        print(f"[OK] Report generated: {report_path}")
        return 0
    except Exception as exc:
        error_text = traceback.format_exc()
        log_path = logs_dir / f"error-{run_id}.log"
        write_text(log_path, error_text)
        db.execute("update runs set finished_at=?, status=?, report_path=?, error=? where run_id=?", (now_local().isoformat(timespec="seconds"), "error", str(report_path), str(exc), run_id))
        db.commit()
        print(f"[ERROR] {exc}")
        print(f"[ERROR] Details: {log_path}")
        return 1
    finally:
        if memory:
            memory.close()
        db.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the daily Outlook mail to automotive wiki report workflow.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Path to config.yaml.")
    parser.add_argument("--force", action="store_true", help="Reprocess emails already marked as successful.")
    parser.add_argument("--mode", choices=["api", "codex_assisted"], help="Override workflow.mode for this run.")
    parser.add_argument("--send-report", dest="send_report_path", default="", help="Send an existing report file and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Override config and keep SMTP/Outlook sending disabled for this run.")
    parser.add_argument("--send-now", action="store_true", help="Override config and send through the configured backend.")
    args = parser.parse_args()
    if args.dry_run and args.send_now:
        raise ValueError("--dry-run and --send-now cannot be used together")
    send_override = True if args.dry_run else False if args.send_now else None
    if args.send_report_path:
        return send_existing_report(Path(args.config), Path(args.send_report_path), send_dry_run_override=send_override)
    return run(Path(args.config), force=args.force, mode_override=args.mode, send_dry_run_override=send_override)


if __name__ == "__main__":
    raise SystemExit(main())
