"""Unified async server - handles both HTTP and WebSocket on a single port.

This replaces the ThreadingHTTPServer + separate WS server architecture,
enabling deployment on platforms like Railway that only expose one port.

Uses aiohttp to serve:
  - HTTP routes -> proxied to DemoHandler logic
  - WebSocket /ws -> bridge agent connections
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
import traceback
import threading
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from io import BytesIO

# Ensure demo_app is on path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from aiohttp import web, WSMsgType

from auth import init_db as init_auth_db, verify_token, register_user, login_user, logout_user, get_user_settings, save_user_settings, get_user_llm_config, set_user_llm_config
from bridge_manager import register_bridge, unregister_bridge, resolve_bridge_result, send_bridge_command_sync, is_bridge_connected, get_bridge_status, set_event_loop

# Import the original handler to reuse all its route logic
from app import DemoHandler, APP_ROOT, STATIC_DIR, _thread_local, _current_username, _try_bridge

# Reuse app.py's thread-local (bridge routing reads app._thread_local)
_thread_local = _thread_local


def _run_handler_method(method: str, path: str, query_string: str, headers: dict, body: bytes, current_user: dict | None) -> tuple[int, dict, bytes]:
    """Simulate a request through DemoHandler and capture the response."""
    
    class FakeRequest:
        def __init__(self):
            self.makefile = lambda *a, **kw: BytesIO(body) if a and a[0] == 'rb' else BytesIO()
    
    # We can't easily reuse DemoHandler's methods without a real socket.
    # Instead, we'll route directly to the underlying functions.
    pass


async def http_handler(request: web.Request) -> web.Response:
    """Handle HTTP requests by routing to the app's functions."""
    path = request.path
    method = request.method
    
    # Skip WebSocket path - handled by websocket_handler
    if path == "/ws":
        return web.json_response({"error": "WebSocket endpoint - use ws:// protocol"}, status=426)
    
    qs = {k: [v] for k, v in request.query.items()}
    
    # Auth
    auth_header = request.headers.get("Authorization", "")
    current_user = None
    if auth_header.startswith("Bearer "):
        current_user = verify_token(auth_header[7:])
    
    _thread_local.current_user = current_user
    
    public_paths = {"/", "/login", "/api/auth/login", "/api/auth/register"}
    is_static = path.startswith("/static/") or path.endswith((".css", ".js", ".png", ".svg", ".ico", ".woff", ".woff2"))
    needs_auth = path not in public_paths and not is_static
    
    if needs_auth and not current_user:
        # Also check Basic auth for backward compat
        import base64
        if auth_header.startswith("Basic "):
            try:
                decoded = base64.b64decode(auth_header[6:]).decode()
                user_name, pwd = decoded.split(":", 1)
                from app import AUTH_USERS
                if AUTH_USERS.get(user_name) == pwd:
                    current_user = {"id": 0, "username": user_name, "display_name": user_name}
                    _thread_local.current_user = current_user
            except Exception:
                pass

    if needs_auth and not current_user:
        return web.json_response({"error": "Authentication required", "redirect": "/login"}, status=401)
    
    # Serve static files
    if path == "/" or path == "/login":
        filename = "index.html" if path == "/" else "login.html"
        target = STATIC_DIR / filename
        if target.exists():
            return web.Response(body=target.read_bytes(), content_type="text/html", charset="utf-8")
        return web.json_response({"error": "Not found"}, status=404)

    # Bridge Agent download
    if path == "/download/bridge" or path == "/static/downloads/GRCBridgeAgent.exe":
        exe_path = STATIC_DIR / "downloads" / "GRCBridgeAgent.exe"
        if not exe_path.exists():
            exe_path = APP_ROOT / "dist" / "GRCBridgeAgent.exe"
        if exe_path.exists():
            return web.FileResponse(str(exe_path), headers={
                "Content-Disposition": "attachment; filename=GRCBridgeAgent.exe",
                "Content-Type": "application/octet-stream",
            })
        return web.json_response({"error": "Bridge Agent exe not available"}, status=404)
    
    if path.startswith("/static/") or path.endswith((".css", ".js", ".png", ".svg", ".ico")):
        rel = path.lstrip("/")
        if path.startswith("/static/"):
            rel = path[8:]
        target = STATIC_DIR / rel
        if target.exists() and target.is_file():
            ct = "text/html"
            if rel.endswith(".css"): ct = "text/css"
            elif rel.endswith(".js"): ct = "application/javascript"
            elif rel.endswith(".png"): ct = "image/png"
            elif rel.endswith(".svg"): ct = "image/svg+xml"
            elif rel.endswith(".ico"): ct = "image/x-icon"
            return web.Response(body=target.read_bytes(), content_type=ct)
        return web.json_response({"error": "Not found"}, status=404)
    
    # API routes
    try:
        from app import (
            get_all_contacts, get_contacts_by_topic, 
            gap_tracking_status, wiki_search, wiki_search_semantic,
            outlook_latest_email, outlook_search_emails, outlook_needs_reply,
            outlook_find_contact, outlook_email_detail, outlook_yesterday_emails,
            get_chat_sessions, get_chat_messages, search_knowledge_base,
            get_export_markets_data, get_assessments_sent,
            wiki_files, wiki_counts, read_text, safe_rel_path, WIKI_DIR,
        )
        
        # GET routes
        if method == "GET":
            if path == "/api/status":
                from app import automation_snapshot, list_reports, wiki_counts, list_runs
                return web.json_response({
                    "automation": automation_snapshot(),
                    "reports": list_reports(),
                    "wiki_counts": wiki_counts(),
                    "runs": list_runs(),
                })
            if path == "/api/contacts":
                topic = qs.get("topic", [""])[0]
                if topic:
                    return web.json_response({"contacts": get_contacts_by_topic(topic), "topic": topic})
                return web.json_response({"contacts": get_all_contacts()})
            if path == "/api/gap-tracking/status":
                return web.json_response(gap_tracking_status())
            if path == "/api/chat/sessions":
                return web.json_response({"sessions": get_chat_sessions()})
            if path == "/api/chat/messages":
                session_id = qs.get("session", [""])[0]
                limit = int(qs.get("limit", ["50"])[0])
                return web.json_response({"messages": get_chat_messages(session_id, limit)})
            if path == "/api/chat/search":
                q = qs.get("q", [""])[0]
                return web.json_response(search_knowledge_base(q))
            if path == "/api/outlook/latest":
                return web.json_response(outlook_latest_email(qs.get("sender", [""])[0]))
            if path == "/api/outlook/search":
                return web.json_response(outlook_search_emails(qs.get("q", [""])[0], int(qs.get("limit", ["10"])[0])))
            if path == "/api/outlook/needs-reply":
                return web.json_response(outlook_needs_reply(qs.get("date", ["today"])[0]))
            if path == "/api/outlook/yesterday":
                return web.json_response(outlook_yesterday_emails())
            if path == "/api/wiki/search":
                return web.json_response(wiki_search(qs.get("q", [""])[0], int(qs.get("limit", ["10"])[0])))
            if path == "/api/wiki/search-semantic":
                return web.json_response(wiki_search_semantic(qs.get("q", [""])[0], int(qs.get("limit", ["10"])[0])))
            if path == "/api/wiki/list":
                return web.json_response({"files": wiki_files(), "counts": wiki_counts()})
            if path == "/api/wiki/file":
                target = safe_rel_path(WIKI_DIR, qs.get("path", [""])[0])
                return web.json_response({"path": target.relative_to(WIKI_DIR).as_posix(), "text": read_text(target, limit=800000)})
            if path == "/api/settings":
                if current_user and current_user.get("id"):
                    settings = get_user_settings(current_user["id"])
                    llm = get_user_llm_config(current_user["id"])
                    return web.json_response({"settings": settings, "llm": llm, "user": current_user})
                return web.json_response({"settings": {}, "llm": {}, "user": None})
            if path == "/api/bridge/status":
                status = get_bridge_status(current_user["username"] if current_user else "")
                return web.json_response(status)
            if path == "/api/bridge/poll":
                if not current_user:
                    return web.json_response({"error": "Auth required"}, status=401)
                from bridge_manager import poll_commands
                cmds = poll_commands(current_user["username"])
                return web.json_response(cmds)
            if path == "/api/auth/me":
                if current_user:
                    return web.json_response({"ok": True, "user": current_user})
                return web.json_response({"ok": False}, status=401)
            if path == "/api/export-markets/data":
                return web.json_response(get_export_markets_data())
            if path == "/api/assessments/sent":
                return web.json_response({"sent": get_assessments_sent()})
            
            return web.json_response({"error": "Not found"}, status=404)
        
        # POST routes
        if method == "POST":
            body = await request.json()
            
            if path == "/api/auth/register":
                result = register_user(body.get("username", ""), body.get("display_name", ""), body.get("password", ""))
                return web.json_response(result, status=200 if result.get("ok") else 400)
            
            if path == "/api/auth/login":
                result = login_user(body.get("username", ""), body.get("password", ""))
                return web.json_response(result, status=200 if result.get("ok") else 401)
            
            if path == "/api/auth/logout":
                logout_user(auth_header.replace("Bearer ", ""))
                return web.json_response({"ok": True})
            
            if path == "/api/settings":
                if current_user and current_user.get("id"):
                    settings = get_user_settings(current_user["id"])
                    for k, v in body.items():
                        settings[k] = v
                    save_user_settings(current_user["id"], settings)
                    return web.json_response({"ok": True, "settings": settings})
                return web.json_response({"ok": False, "error": "Not authenticated"}, status=401)
            
            if path == "/api/settings/llm":
                if current_user and current_user.get("id"):
                    set_user_llm_config(current_user["id"], body.get("api_key", ""), body.get("base_url", ""), body.get("model", ""))
                    return web.json_response({"ok": True})
                return web.json_response({"ok": False, "error": "Not authenticated"}, status=401)
            
            if path == "/api/bridge/result":
                if not current_user:
                    return web.json_response({"error": "Auth required"}, status=401)
                from bridge_manager import submit_result
                submit_result(body.get("id", ""), body.get("result", body))
                return web.json_response({"ok": True})
            
            # Delegate remaining POST routes to app.py functions
            # Import here to avoid circular imports
            from app import (
                run_agent, send_assessment_email,
                parse_pvs_excel, gap_tracking_set_status, gap_tracking_reset,
                write_summary_comment, close_layer3_ticket,
                chat_with_llm, generate_monthly_report_html, send_monthly_report_draft,
                run_analysis_action, build_topic_comments_report,
                create_chat_session, delete_chat_session, save_chat_message,
                sync_pvs_wiki, download_pvs_from_jira,
            )
            
            if path == "/api/run":
                args = ["--send-now" if body.get("send_now") else "--dry-run"]
                if body.get("force"): args.append("--force")
                return web.json_response(run_agent(args))
            if path == "/api/send-report":
                return web.json_response(generate_monthly_report_html(body.get("to", []), body.get("cc", [])))
            if path == "/api/assessments/send":
                return web.json_response(send_assessment_email(body))
            if path == "/api/parse-pvs":
                return web.json_response(parse_pvs_excel(body.get("parent_key", ""), body.get("file_path", "")))
            if path == "/api/gap-tracking/set-status":
                return web.json_response(gap_tracking_set_status(body.get("market", ""), body.get("topic", ""), body.get("status", "")))
            if path == "/api/gap-tracking/reset-status":
                return web.json_response(gap_tracking_reset(body.get("market", ""), body.get("topic", "")))
            if path == "/api/gap-tracking/write-summary":
                return web.json_response(write_summary_comment(body.get("market", "")))
            if path == "/api/gap-tracking/close-jira":
                return web.json_response(close_layer3_ticket(body.get("market", "")))
            if path == "/api/chat":
                return web.json_response(chat_with_llm(body.get("session_id", ""), body.get("message", "")))
            if path == "/api/chat/session":
                return web.json_response(create_chat_session(body.get("title", "")))
            if path == "/api/chat/delete":
                return web.json_response(delete_chat_session(body.get("session_id", "")))
            if path == "/api/monthly-report/generate":
                return web.json_response(generate_monthly_report_html())
            if path == "/api/monthly-report/send-draft":
                return web.json_response(send_monthly_report_draft(body.get("to", []), body.get("cc", [])))
            if path.startswith("/api/analysis/"):
                action = path.split("/api/analysis/")[1]
                return web.json_response(run_analysis_action(action, body))
            if path == "/api/analysis/topic_comments":
                return web.json_response(build_topic_comments_report(body.get("topic", "")))
            if path == "/api/pvs/sync":
                return web.json_response(sync_pvs_wiki())
            if path == "/api/pvs/download":
                return web.json_response({"files": download_pvs_from_jira(body.get("parent_key", ""))})
            
            return web.json_response({"error": "Not found"}, status=404)
    
    except Exception as exc:
        return web.json_response({"error": str(exc), "trace": traceback.format_exc()}, status=500)


async def websocket_handler(request: web.Request) -> web.WebSocketResponse:
    """Handle WebSocket connections from bridge agents."""
    ws = web.WebSocketResponse(ping_interval=30, ping_timeout=10)
    try:
        await ws.prepare(request)
    except Exception as e:
        print(f"[WS] Failed to prepare: {e}", flush=True)
        return ws

    username = None

    try:
        # Extract token from query string
        token = request.query.get("token", "")
        if not token:
            auth = request.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                token = auth[7:]

        user = verify_token(token)
        if not user:
            await ws.send_json({"type": "error", "message": "Authentication failed"})
            await ws.close(code=4001)
            return ws

        username = user["username"]
        print(f"[WS] Bridge connected: {username}", flush=True)

        register_bridge(username, ws)

        await ws.send_json({
            "type": "welcome",
            "message": f"Bridge connected as {username}",
            "timestamp": time.time(),
        })

        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    if data.get("type") == "hello":
                        print(f"[WS] Bridge {username} says hello", flush=True)
                        continue
                    msg_id = data.get("id", "")
                    result = data.get("result", data)
                    resolve_bridge_result(msg_id, result)
                except json.JSONDecodeError:
                    print(f"[WS] Invalid JSON from {username}", flush=True)
            elif msg.type == WSMsgType.ERROR:
                print(f"[WS] Error from {username}: {ws.exception()}", flush=True)
    except Exception as e:
        print(f"[WS] Handler error: {e}\n{traceback.format_exc()}", flush=True)
    finally:
        if username:
            unregister_bridge(username)
            print(f"[WS] Bridge disconnected: {username}", flush=True)
    
    return ws


def create_app() -> web.Application:
    """Create the aiohttp application."""
    app = web.Application()
    
    # WebSocket route
    app.router.add_get("/ws", websocket_handler)
    
    # All other routes - use catch-all
    app.router.add_route("*", "/{tail:.*}", http_handler)
    
    return app


def main() -> int:
    init_auth_db()
    set_event_loop(asyncio.get_event_loop())
    
    host = os.environ.get("DEMO_HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", os.environ.get("DEMO_PORT", "7860")))
    
    print(f"G.R.C. Agent (unified) starting on {host}:{port}", flush=True)
    print(f"HTTP + WebSocket on same port", flush=True)
    
    app = create_app()
    web.run_app(app, host=host, port=port, print=None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
