#!/usr/bin/env python3
"""Bridge Agent - runs on user's machine, connects to GRC server via WebSocket.

Executes Outlook COM commands locally and returns results to the server.

Usage:
    python bridge_agent.py --server ws://10.126.142.71:7860/ws --token <session_token>
    python bridge_agent.py --server ws://localhost:7860/ws --token <session_token>
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
import traceback
import urllib.parse
from datetime import datetime, timedelta

try:
    import websockets
except ImportError:
    print("ERROR: websockets not installed. Run: pip install websockets", file=sys.stderr)
    sys.exit(1)


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


COMMANDS = {
    "ping": cmd_ping,
    "read_latest": cmd_read_latest,
    "search_emails": cmd_search_emails,
    "needs_reply": cmd_needs_reply,
    "yesterday_emails": cmd_yesterday_emails,
    "email_detail": cmd_email_detail,
    "find_contact": cmd_find_contact,
    "send_email": cmd_send_email,
    "reply_email": cmd_reply_email,
}


async def handle_message(message: str) -> str:
    """Parse incoming command and execute."""
    try:
        msg = json.loads(message)
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

        return json.dumps({"id": msg_id, "result": result})
    except json.JSONDecodeError:
        return json.dumps({"id": "", "result": {"ok": False, "error": "Invalid JSON"}})


async def connect_and_serve(server_url: str, token: str, reconnect: bool = True):
    """Connect to server and serve commands."""
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        try:
            url = f"{server_url}?token={token}"
            print(f"[Bridge] Connecting to {server_url} ...", flush=True)

            async with websockets.connect(url, additional_headers=headers, ping_interval=30, ping_timeout=10) as ws:
                print(f"[Bridge] Connected! Listening for commands...", flush=True)

                # Send hello
                await ws.send(json.dumps({
                    "type": "hello",
                    "message": "Bridge agent connected",
                    "timestamp": time.time(),
                }))

                async for message in ws:
                    try:
                        response = await handle_message(message)
                        await ws.send(response)
                    except Exception as e:
                        print(f"[Bridge] Error handling message: {e}", file=sys.stderr, flush=True)

        except websockets.exceptions.ConnectionClosed as e:
            print(f"[Bridge] Connection closed: {e}", flush=True)
        except ConnectionRefusedError:
            print(f"[Bridge] Connection refused. Is the server running on {server_url}?", flush=True)
        except Exception as e:
            print(f"[Bridge] Error: {e}", flush=True)

        if not reconnect:
            break

        print("[Bridge] Reconnecting in 5 seconds...", flush=True)
        await asyncio.sleep(5)


def main():
    parser = argparse.ArgumentParser(description="GRC Bridge Agent - Outlook COM connector")
    parser.add_argument("--server", default=None, help="WebSocket server URL. If not given, auto-discover.")
    parser.add_argument("--api", default=None, help="HTTP API base URL for auto-discovery.")
    parser.add_argument("--token", default=None, help="Session token for authentication")
    parser.add_argument("--no-reconnect", action="store_true", help="Disable auto-reconnect")
    args = parser.parse_args()

    # If no token provided, prompt interactively (for double-click users)
    if not args.token:
        print("=" * 50, flush=True)
        print("  G.R.C. Bridge Agent", flush=True)
        print("=" * 50, flush=True)
        print(flush=True)
        print("You need a token from the G.R.C. Agent web app.", flush=True)
        print("  1. Open the web app in your browser", flush=True)
        print("  2. Click 'Show Token' button", flush=True)
        print("  3. Copy the token and paste it below", flush=True)
        print(flush=True)
        args.token = input("Paste your token here: ").strip()
        if not args.token:
            print("Error: Token is required. Exiting.", flush=True)
            input("Press Enter to exit...")
            return

    if not args.api:
        args.api = os.environ.get("GRC_API_URL", "https://grc-production-e359.up.railway.app")

    print(f"[Bridge] GRC Bridge Agent starting...", flush=True)
    print(f"[Bridge] Token: {args.token[:8]}...", flush=True)

    # Auto-discover WS URL from API if not given
    server_url = args.server
    if not server_url:
        api_url = args.api
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{api_url}/api/bridge/status",
                headers={"Authorization": f"Bearer {args.token}"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read())
                ws_url = data.get("ws_url", "")
                if ws_url:
                    server_url = ws_url
                    print(f"[Bridge] Auto-discovered WS URL: {ws_url}", flush=True)
        except Exception as e:
            print(f"[Bridge] Auto-discovery failed: {e}", flush=True)

    if not server_url:
        # Fallback: derive WS URL from API URL
        api_url = args.api or os.environ.get("GRC_API_URL", "http://localhost:7860")
        parsed = urllib.parse.urlparse(api_url)
        if parsed.scheme == "https":
            server_url = f"wss://{parsed.hostname}/ws"
        elif parsed.scheme == "http":
            ws_port = int(parsed.port or 7860) + 1
            server_url = f"ws://{parsed.hostname or 'localhost'}:{ws_port}/ws"
        else:
            server_url = f"ws://{parsed.hostname or 'localhost'}:7861/ws"
        print(f"[Bridge] Fallback WS URL: {server_url}", flush=True)

    print(f"[Bridge] Server: {server_url}", flush=True)
    print(f"[Bridge] Connecting...", flush=True)
    print(flush=True)

    try:
        asyncio.run(connect_and_serve(server_url, args.token, reconnect=not args.no_reconnect))
    except KeyboardInterrupt:
        print("\n[Bridge] Shutting down...", flush=True)
    except Exception as e:
        print(f"\n[Bridge] Fatal error: {e}", flush=True)
    
    print(flush=True)
    print("Bridge Agent has stopped.", flush=True)
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
