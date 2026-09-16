#!/usr/bin/env python3
"""Bridge Agent - runs on user's machine, connects to GRC server via HTTP polling.

Executes Outlook COM commands locally and returns results to the server.
No WebSocket needed - uses simple HTTP polling.

Token is saved on first use, subsequent runs are silent (no console needed).

Usage:
    python bridge_agent.py                        # auto: saved token or prompt
    python bridge_agent.py --token <token>        # explicit token
    python bridge_agent.py --silent               # silent mode (no console)
    python bridge_agent.py --forget               # clear saved token
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path


# ── Token persistence ──────────────────────────────────────────────
CONFIG_DIR = Path(os.environ.get("APPDATA", str(Path.home()))) / "GRCBridge"
TOKEN_FILE = CONFIG_DIR / "token.txt"
API_FILE = CONFIG_DIR / "api_url.txt"
LOG_FILE = CONFIG_DIR / "bridge.log"

DEFAULT_API = "https://grc-production-efc4.up.railway.app"


def save_config(token: str, api_url: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token, encoding="utf-8")
    API_FILE.write_text(api_url, encoding="utf-8")
    # Also write token without BOM for urllib header compatibility
    with open(TOKEN_FILE, "w", encoding="ascii") as f:
        f.write(token)
    with open(API_FILE, "w", encoding="ascii") as f:
        f.write(api_url)


def load_token() -> str | None:
    if TOKEN_FILE.exists():
        t = TOKEN_FILE.read_text(encoding="utf-8-sig").strip()
        return t if t else None
    return None


def load_api_url() -> str:
    if API_FILE.exists():
        return API_FILE.read_text(encoding="utf-8").strip().rstrip("/")
    return DEFAULT_API


def clear_config() -> None:
    TOKEN_FILE.unlink(missing_ok=True)


def log(msg: str, silent: bool = False) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    if not silent:
        print(line, flush=True)
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def validate_token(api_url: str, token: str) -> bool:
    """Quick check if token is still valid."""
    try:
        req = urllib.request.Request(
            f"{api_url}/api/bridge/poll",
            headers={"Authorization": f"Bearer {token}"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            resp.read()
        return True
    except urllib.error.HTTPError as e:
        return e.code != 401
    except Exception:
        return True  # assume valid on network error


def relaunch_silent(api_url: str, token: str) -> None:
    """Relaunch self in background (detached, no console window)."""
    CREATE_NO_WINDOW = 0x08000000
    DETACHED_PROCESS = 0x00000008
    subprocess.Popen(
        [sys.executable, "--silent", "--api", api_url, "--token", token],
        creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS,
        close_fds=True,
    )


def is_already_running() -> bool:
    """Check if another bridge instance is already running."""
    try:
        import ctypes
        import ctypes.wintypes as w
        # Try to create a named mutex; if it exists, another instance is running
        mutex_name = "GRCBridgeAgent_SingleInstance_Mutex"
        CreateMutex = ctypes.windll.kernel32.CreateMutexW
        CreateMutex.restype = w.HANDLE
        CreateMutex.argtypes = [w.LPCVOID, w.BOOL, w.LPCWSTR]
        GetLastError = ctypes.windll.kernel32.GetLastError
        GetLastError.restype = w.DWORD
        GetLastError.argtypes = []
        ERROR_ALREADY_EXISTS = 183
        handle = CreateMutex(None, False, mutex_name)
        if GetLastError() == ERROR_ALREADY_EXISTS:
            return True
        # Keep handle alive on this process
        _MUTEX_HANDLE = handle
    except Exception:
        pass
    return False


def setup_autostart() -> None:
    """Create a Windows startup shortcut so bridge auto-launches on boot."""
    try:
        startup_dir = Path(os.environ.get("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut_path = startup_dir / "GRCBridgeAgent.lnk"
        exe_path = str(Path(sys.executable).resolve())

        # Use PowerShell to create .lnk shortcut (no extra dependency)
        ps_script = (
            f'$s=(New-Object -COM WScript.Shell).CreateShortcut("{shortcut_path}");'
            f'$s.TargetPath="{exe_path}";'
            f'$s.Arguments="--silent";'
            f'$s.WindowStyle=7;'
            f'$s.Description="GRC Bridge Agent";'
            f'$s.Save()'
        )
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            capture_output=True, timeout=10,
        )
    except Exception:
        pass


def self_install() -> str | None:
    """If running from a temp/download dir, copy exe to a stable location and restart.
    Returns the new exe path if it relocated, or None if already in a stable location."""
    if not getattr(sys, "frozen", False):
        return None  # running as .py script, not exe

    current_exe = Path(sys.executable).resolve()
    stable_dir = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "GRCBridge"
    stable_exe = stable_dir / "GRCBridgeAgent.exe"

    # Check if we're in a temp/download directory
    temp_indicators = [
        os.environ.get("TEMP", ""),
        os.environ.get("TMP", ""),
        str(Path.home() / "Downloads"),
        "MicrosoftEdgeDownloads",
        "Temp",
        "Temporary Internet Files",
    ]

    current_str = str(current_exe)
    is_temp = any(ind and ind.lower() in current_str.lower() for ind in temp_indicators if ind)

    if not is_temp and stable_exe.exists():
        return None  # already stable

    if current_exe == stable_exe:
        return None  # already at stable location

    # Copy to stable location
    try:
        stable_dir.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copy2(str(current_exe), str(stable_exe))
        print(f"[Bridge] Installed to: {stable_exe}", flush=True)
        return str(stable_exe)
    except Exception as e:
        print(f"[Bridge] Could not self-install: {e}", flush=True)
        return None


def remove_autostart() -> None:
    """Remove the startup shortcut."""
    try:
        startup_dir = Path(os.environ.get("APPDATA")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
        shortcut_path = startup_dir / "GRCBridgeAgent.lnk"
        shortcut_path.unlink(missing_ok=True)
    except Exception:
        pass


def get_outlook():
    """Get Outlook COM application object."""
    import win32com.client
    return win32com.client.Dispatch("Outlook.Application")


def get_namespace():
    """Get MAPI namespace."""
    outlook = get_outlook()
    ns = outlook.GetNamespace("MAPI")
    return outlook, ns


def get_inbox():
    """Get default inbox folder."""
    _, ns = get_namespace()
    inbox = ns.GetDefaultFolder(6)  # olFolderInbox = 6
    return inbox


def _format_time(com_time) -> str:
    """Convert COM time to ISO string."""
    try:
        if hasattr(com_time, 'year'):
            return f"{com_time.year:04d}-{com_time.month:02d}-{com_time.day:02d}T{com_time.hour:02d}:{com_time.minute:02d}:{com_time.second:02d}"
    except Exception:
        pass
    return str(com_time)


def _extract_email(mail) -> dict:
    """Extract email fields from COM MailItem."""
    try:
        sender_email = ""
        try:
            sender_email = mail.SenderEmailAddress
        except Exception:
            pass
        return {
            "entry_id": mail.EntryID,
            "subject": mail.Subject or "",
            "sender": mail.SenderName or "",
            "sender_email": sender_email,
            "received_time": _format_time(mail.ReceivedTime),
            "body_preview": (mail.Body or "")[:500],
            "body": mail.Body or "",
            "html_body": mail.HTMLBody or "",
            "has_attachment": mail.Attachments.Count > 0,
            "attachment_count": mail.Attachments.Count,
            "importance": mail.Importance,
            "unread": mail.UnRead,
        }
    except Exception as e:
        return {"error": f"Failed to extract email: {e}"}


def cmd_read_latest(params: dict) -> dict:
    """Read the latest email, optionally filtered by sender."""
    inbox = get_inbox()
    items = inbox.Items
    items.Sort("[ReceivedTime]", True)

    sender_filter = params.get("sender", "")
    if sender_filter:
        for item in items:
            try:
                if sender_filter.lower() in (item.SenderEmailAddress or "").lower() or \
                   sender_filter.lower() in (item.SenderName or "").lower():
                    return {"ok": True, "data": _extract_email(item)}
            except Exception:
                continue
        return {"ok": False, "error": f"No email from {sender_filter}"}

    item = items.GetFirst()
    if item:
        return {"ok": True, "data": _extract_email(item)}
    return {"ok": False, "error": "No emails found"}


def cmd_search_emails(params: dict) -> dict:
    """Search emails by keyword."""
    query = params.get("query", "")
    max_results = int(params.get("max_results", 10))

    inbox = get_inbox()
    items = inbox.Items
    items.Sort("[ReceivedTime]", True)

    results = []
    count = 0
    for item in items:
        if count >= max_results:
            break
        try:
            subject = item.Subject or ""
            body = item.Body or ""
            sender = item.SenderName or ""
            sender_email = item.SenderEmailAddress or ""
            if query.lower() in subject.lower() or query.lower() in body.lower() or \
               query.lower() in sender.lower() or query.lower() in sender_email.lower():
                results.append(_extract_email(item))
                count += 1
        except Exception:
            continue

    return {"ok": True, "count": len(results), "emails": results}


def cmd_needs_reply(params: dict) -> dict:
    """Check emails that need reply (unread, received today/yesterday)."""
    date_filter = params.get("date", "today")

    inbox = get_inbox()
    items = inbox.Items
    items.Sort("[ReceivedTime]", True)

    now = datetime.now()
    if date_filter == "yesterday":
        cutoff = now - timedelta(days=1)
        cutoff = cutoff.replace(hour=0, minute=0, second=0)
    else:
        cutoff = now.replace(hour=0, minute=0, second=0)

    results = []
    for item in items:
        try:
            rt = item.ReceivedTime
            email_time = datetime(rt.year, rt.month, rt.day, rt.hour, rt.minute, rt.second)
            if email_time < cutoff:
                break
            if item.UnRead:
                results.append(_extract_email(item))
        except Exception:
            continue

    return {"ok": True, "count": len(results), "emails": results}


def cmd_yesterday_emails(params: dict) -> dict:
    """Get yesterday's email digest."""
    inbox = get_inbox()
    items = inbox.Items
    items.Sort("[ReceivedTime]", True)

    now = datetime.now()
    yesterday_start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0)
    yesterday_end = now.replace(hour=0, minute=0, second=0)

    results = []
    for item in items:
        try:
            rt = item.ReceivedTime
            email_time = datetime(rt.year, rt.month, rt.day, rt.hour, rt.minute, rt.second)
            if email_time < yesterday_start:
                break
            if email_time >= yesterday_end:
                continue
            results.append(_extract_email(item))
        except Exception:
            continue

    return {"ok": True, "count": len(results), "emails": results}


def cmd_email_detail(params: dict) -> dict:
    """Get email detail by EntryID."""
    entry_id = params.get("entry_id", "")
    if not entry_id:
        return {"ok": False, "error": "entry_id is required"}

    _, ns = get_namespace()
    try:
        item = ns.GetItemFromID(entry_id)
        return {"ok": True, "data": _extract_email(item)}
    except Exception as e:
        return {"ok": False, "error": f"Email not found: {e}"}


def cmd_find_contact(params: dict) -> dict:
    """Search Outlook contacts by name."""
    search_name = params.get("search_name", "")
    if not search_name:
        return {"ok": False, "error": "search_name is required"}

    _, ns = get_namespace()
    contacts = ns.GetDefaultFolder(10)  # olFolderContacts = 10

    results = []
    try:
        items = contacts.Items
        for item in items:
            try:
                full_name = item.FullName or ""
                email = ""
                try:
                    email = item.Email1Address or ""
                except Exception:
                    pass
                if search_name.lower() in full_name.lower() or \
                   (email and search_name.lower() in email.lower()):
                    results.append({
                        "name": full_name,
                        "email": email,
                        "company": getattr(item, "CompanyName", "") or "",
                        "job_title": getattr(item, "JobTitle", "") or "",
                    })
                    if len(results) >= 5:
                        break
            except Exception:
                continue
    except Exception as e:
        return {"ok": False, "error": str(e)}

    return {"ok": True, "count": len(results), "contacts": results}


def cmd_send_email(params: dict) -> dict:
    """Send email via Outlook COM."""
    to = params.get("to", "")
    cc = params.get("cc", "")
    subject = params.get("subject", "")
    body = params.get("body", "")
    html_body = params.get("html_body", "")
    draft_only = params.get("draft_only", False)

    if not to or not subject:
        return {"ok": False, "error": "to and subject are required"}

    try:
        outlook = get_outlook()
        mail = outlook.CreateItem(0)  # olMailItem = 0
        mail.To = to
        if cc:
            mail.Cc = cc
        mail.Subject = subject
        if html_body:
            mail.HTMLBody = html_body
        else:
            mail.Body = body

        if draft_only:
            mail.Save()
            return {"ok": True, "message": "Draft saved"}
        else:
            mail.Send()
            return {"ok": True, "message": "Email sent"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def cmd_reply_email(params: dict) -> dict:
    """Reply to an email by EntryID."""
    entry_id = params.get("entry_id", "")
    body = params.get("body", "")
    reply_all = params.get("reply_all", False)

    if not entry_id:
        return {"ok": False, "error": "entry_id is required"}

    _, ns = get_namespace()
    try:
        item = ns.GetItemFromID(entry_id)
        if reply_all:
            reply = item.ReplyAll()
        else:
            reply = item.Reply()
        reply.Body = body + "\n\n" + (reply.Body or "")
        reply.Send()
        return {"ok": True, "message": "Reply sent"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def cmd_ping(params: dict) -> dict:
    """Health check."""
    return {"ok": True, "timestamp": time.time(), "message": "Bridge is alive"}


def cmd_llm_proxy(params: dict) -> dict:
    """Proxy LLM request to internal API gateway (accessible from local machine)."""
    try:
        import urllib.request as ur
        api_key = params.get("api_key", "")
        base_url = params.get("base_url", "https://llm-gateway.dev.cn-vwa.volkswagen-cea.com/v1")
        model = params.get("model", "MiniMax")
        messages = params.get("messages", [])
        temperature = params.get("temperature", 0.7)
        max_tokens = params.get("max_tokens", 2000)

        body = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode("utf-8")

        req = ur.Request(
            f"{base_url}/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with ur.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        return {"ok": True, "data": result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def cmd_scan_emails(params: dict) -> dict:
    """Scan inbox for emails matching keywords (like find_emails in run_daily_report).
    params: keywords (list[str]), sender_filter (str), days_back (int), limit (int)
    """
    keywords = params.get("keywords", [])
    if isinstance(keywords, str):
        keywords = [keywords]
    keywords_folded = [k.lower() for k in keywords if k]
    sender_filter = str(params.get("sender_filter", "")).lower()
    days_back = int(params.get("days_back", 3))
    limit = int(params.get("limit", 10))

    inbox = get_inbox()
    items = inbox.Items
    items.Sort("[ReceivedTime]", True)

    from datetime import datetime, timedelta
    cutoff = (datetime.now() - timedelta(days=days_back)).replace(hour=0, minute=0, second=0) if days_back else None

    results = []
    for item in items:
        if len(results) >= limit:
            break
        try:
            subject = item.Subject or ""
            body = item.Body or ""
            sender_name = item.SenderName or ""
            sender_email = item.SenderEmailAddress or ""
            rt = item.ReceivedTime
            received = datetime(rt.year, rt.month, rt.day, rt.hour, rt.minute, rt.second) if hasattr(rt, 'year') else None

            if received and cutoff and received < cutoff:
                continue
            if sender_filter and sender_filter not in sender_name.lower() and sender_filter not in sender_email.lower():
                continue
            subject_lower = subject.lower()
            body_lower = body.lower()
            if keywords_folded and not all(kw in subject_lower or kw in body_lower for kw in keywords_folded):
                continue

            attachments = []
            try:
                atts = item.Attachments
                for i in range(1, atts.Count + 1):
                    attachments.append(atts.Item(i).Filename)
            except Exception:
                pass

            results.append({
                "entryid": item.EntryID or "",
                "subject": subject,
                "sender": f"{sender_name} <{sender_email}>" if sender_email else sender_name,
                "received": str(received)[:19] if received else "",
                "body": body[:4000],
                "body_preview": body[:300],
                "attachments": attachments,
            })
        except Exception:
            continue

    return {"ok": True, "count": len(results), "emails": results}


COMMANDS = {
    "ping": cmd_ping,
    "llm_proxy": cmd_llm_proxy,
    "scan_emails": cmd_scan_emails,
    "read_latest": cmd_read_latest,
    "search_emails": cmd_search_emails,
    "needs_reply": cmd_needs_reply,
    "yesterday_emails": cmd_yesterday_emails,
    "email_detail": cmd_email_detail,
    "find_contact": cmd_find_contact,
    "send_email": cmd_send_email,
    "reply_email": cmd_reply_email,
}


def handle_command(msg: dict) -> dict:
    """Execute a command and return result."""
    msg_id = msg.get("id", "")
    command = msg.get("command", "")
    params = msg.get("params", {})

    handler = COMMANDS.get(command)
    if not handler:
        result = {"ok": False, "error": f"Unknown command: {command}"}
    else:
        try:
            result = handler(params)
        except Exception as e:
            result = {"ok": False, "error": str(e), "trace": traceback.format_exc()}

    return {"id": msg_id, "result": result}


def poll_loop(api_url: str, token: str, poll_interval: float = 2.0, silent: bool = False):
    """Main polling loop - polls server for commands, executes them, posts results back."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    poll_url = f"{api_url}/api/bridge/poll"
    result_url = f"{api_url}/api/bridge/result"

    log(f"Polling {poll_url} every {poll_interval}s", silent=silent)
    log(f"Connected! Waiting for commands...", silent=silent)

    consecutive_errors = 0
    while True:
        try:
            # Poll for commands
            req = urllib.request.Request(poll_url, headers=headers, method="GET")
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())

            consecutive_errors = 0

            commands = data.get("commands", [])
            for cmd in commands:
                log(f"Executing: {cmd.get('command', '?')}", silent=silent)
                result = handle_command(cmd)
                # Post result back
                try:
                    body = json.dumps(result).encode("utf-8")
                    r = urllib.request.Request(result_url, data=body, headers=headers, method="POST")
                    with urllib.request.urlopen(r, timeout=30) as resp2:
                        pass
                except Exception as e:
                    log(f"Failed to post result: {e}", silent=silent)

            time.sleep(poll_interval)

        except KeyboardInterrupt:
            log("Shutting down...", silent=silent)
            break
        except urllib.error.HTTPError as e:
            if e.code == 401:
                log("Token expired (401). Please get a new token from the web app.", silent=silent)
                clear_config()
                if not silent:
                    print("\nYour token has expired. Please get a new token from the web app.", flush=True)
                    input("Press Enter to exit...")
                break
            elif e.code in (502, 503, 504):
                # Railway deployment/restart — wait and retry, don't count as error
                log(f"Server temporarily unavailable ({e.code}). Retrying...", silent=silent)
                time.sleep(10)
            else:
                log(f"HTTP error: {e.code}", silent=silent)
                consecutive_errors += 1
                time.sleep(5)
        except Exception as e:
            # Timeouts are normal, just retry quietly
            if "timed out" in str(e).lower():
                consecutive_errors = 0
                continue
            log(f"Polling error: {e}", silent=silent)
            consecutive_errors += 1
            if consecutive_errors >= 10:
                log("Too many errors. Waiting 30s...", silent=silent)
                time.sleep(30)
                consecutive_errors = 0
            else:
                time.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="GRC Bridge Agent - Outlook COM connector (HTTP polling)")
    parser.add_argument("--api", default=None, help="Server API base URL")
    parser.add_argument("--token", default=None, help="Session token for authentication")
    parser.add_argument("--interval", type=float, default=2.0, help="Poll interval in seconds (default: 2)")
    parser.add_argument("--silent", action="store_true", help="Silent mode (no console, for background use)")
    parser.add_argument("--forget", action="store_true", help="Clear saved token and exit")
    parser.add_argument("--stop", action="store_true", help="Stop running bridge and disable autostart")
    args = parser.parse_args()

    # --forget: clear saved token, remove autostart, and exit
    if args.forget:
        clear_config()
        remove_autostart()
        print("Saved token cleared. Autostart removed.", flush=True)
        input("Press Enter to exit...")
        return

    # --stop: disable autostart and exit
    if args.stop:
        remove_autostart()
        print("Autostart disabled. You can now close this window.", flush=True)
        input("Press Enter to exit...")
        return

    # Silent mode: read token from file, no interaction
    if args.silent:
        token = args.token or load_token()
        api_url = (args.api or load_api_url()).rstrip("/")
        if not token:
            log("No saved token. Run without --silent to configure.", silent=True)
            return
        # Watchdog loop: if poll_loop crashes, restart automatically
        while True:
            try:
                poll_loop(api_url, token, poll_interval=args.interval, silent=True)
            except SystemExit:
                raise
            except Exception as e:
                log(f"Fatal error: {e}. Restarting in 10s...", silent=True)
                time.sleep(10)
        return

    # Interactive mode
    api_url = (args.api or load_api_url()).rstrip("/")

    # If running from temp/download dir, self-install to stable location and restart
    new_exe = self_install()
    if new_exe:
        # Re-launch from stable location with same args
        restart_args = [new_exe]
        if args.api: restart_args += ["--api", args.api]
        if args.token: restart_args += ["--token", args.token]
        subprocess.Popen(restart_args)
        return

    # If already running in background, don't launch another
    if is_already_running():
        print("Bridge Agent is already running in the background.", flush=True)
        print(f"Logs: {LOG_FILE}", flush=True)
        print("To stop it: run GRCBridgeAgent.exe --stop", flush=True)
        time.sleep(3)
        return

    # Try saved token first
    token = args.token or load_token()
    if token:
        if validate_token(api_url, token):
            log("Token is valid. Starting in background...")
            save_config(token, api_url)
            relaunch_silent(api_url, token)
            print("Bridge Agent is now running in the background.", flush=True)
            print("It will auto-start on Windows boot. You never need to open this again.", flush=True)
            print(f"\nLogs: {LOG_FILE}", flush=True)
            print("To change token: run GRCBridgeAgent.exe --forget", flush=True)
            time.sleep(3)
            return
        else:
            log("Saved token is expired. Please enter a new one.")
            clear_config()
            token = None

    # No valid token - prompt user (first time)
    if not token:
        print("=" * 50, flush=True)
        print("  G.R.C. Bridge Agent - First Time Setup", flush=True)
        print("=" * 50, flush=True)
        print(flush=True)
        print("You need a token from the G.R.C. Agent web app.", flush=True)
        print("  1. Open the web app in your browser", flush=True)
        print("  2. Click 'Show Token' button", flush=True)
        print("  3. Copy the token and paste it below", flush=True)
        print(flush=True)
        print("NOTE: You only need to do this once.", flush=True)
        print("      The bridge will auto-start on Windows boot afterwards.", flush=True)
        print(flush=True)
        args.token = input("Paste your token here: ").strip()
        if not args.token:
            print("Error: Token is required. Exiting.", flush=True)
            input("Press Enter to exit...")
            return
        token = args.token

    # Save token, setup autostart, and relaunch in background
    save_config(token, api_url)
    setup_autostart()
    print(flush=True)
    print(f"[Bridge] Token saved. Auto-start configured.", flush=True)
    print(f"[Bridge] Starting in background...", flush=True)
    relaunch_silent(api_url, token)
    print(flush=True)
    print("Done! Bridge Agent is running in the background.", flush=True)
    print("It will auto-start on Windows boot. You never need to open this again.", flush=True)
    print(f"\nLogs: {LOG_FILE}", flush=True)
    print("To change token: run GRCBridgeAgent.exe --forget", flush=True)
    print("To disable autostart: run GRCBridgeAgent.exe --stop", flush=True)
    time.sleep(3)


if __name__ == "__main__":
    main()
