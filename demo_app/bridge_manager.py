"""Bridge connection manager - tracks WebSocket connections from user bridge agents.

Supports both async (from ws_server) and sync (from HTTP handler) command dispatch.
"""
from __future__ import annotations

import asyncio
import json
import threading
import time
import uuid
from typing import Any

_connections: dict[str, Any] = {}
_pending_results: dict[str, asyncio.Future | threading.Event] = {}
_sync_results: dict[str, dict] = {}
_ws_loop: asyncio.AbstractEventLoop | None = None


def set_event_loop(loop: asyncio.AbstractEventLoop) -> None:
    global _ws_loop
    _ws_loop = loop


def get_event_loop() -> asyncio.AbstractEventLoop | None:
    return _ws_loop


def register_bridge(username: str, websocket: Any) -> None:
    _connections[username] = websocket


def unregister_bridge(username: str) -> None:
    _connections.pop(username, None)


def is_bridge_connected(username: str) -> bool:
    return username in _connections


def get_bridge_status(username: str) -> dict:
    if username and username in _connections:
        return {"connected": True, "message": "Outlook Bridge is online", "username": username}
    return {"connected": False, "message": "Outlook Bridge is offline. Email features require the bridge agent running locally.", "username": username}


async def send_bridge_command_async(username: str, command: str, params: dict = None, timeout: float = 30.0) -> dict:
    """Send command to bridge via WebSocket (async version)."""
    if username not in _connections:
        return {"ok": False, "error": "Bridge not connected"}

    request_id = str(uuid.uuid4())
    ws = _connections[username]
    message = json.dumps({"id": request_id, "command": command, "params": params or {}})

    future: asyncio.Future = asyncio.get_event_loop().create_future()
    _pending_results[request_id] = future

    try:
        await ws.send(message)
        result = await asyncio.wait_for(future, timeout=timeout)
        return result
    except asyncio.TimeoutError:
        return {"ok": False, "error": "Bridge command timed out"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        _pending_results.pop(request_id, None)


def send_bridge_command_sync(username: str, command: str, params: dict = None, timeout: float = 30.0) -> dict:
    """Send command to bridge synchronously (from HTTP handler thread).

    Uses threading.Event to wait for the async result.
    """
    if username not in _connections:
        return {"ok": False, "error": "Bridge not connected"}
    if _ws_loop is None:
        return {"ok": False, "error": "WebSocket event loop not available"}

    request_id = str(uuid.uuid4())
    ws = _connections[username]
    message = json.dumps({"id": request_id, "command": command, "params": params or {}})

    event = threading.Event()
    _pending_results[request_id] = event
    _sync_results[request_id] = None

    # Schedule the send on the WS event loop
    async def _send():
        await ws.send(message)

    asyncio.run_coroutine_threadsafe(_send(), _ws_loop)

    # Wait for result
    if event.wait(timeout=timeout):
        result = _sync_results.get(request_id, {"ok": False, "error": "No result"})
    else:
        result = {"ok": False, "error": "Bridge command timed out"}

    _pending_results.pop(request_id, None)
    _sync_results.pop(request_id, None)
    return result


def resolve_bridge_result(request_id: str, result: dict) -> None:
    """Resolve a pending bridge command result."""
    pending = _pending_results.get(request_id)
    if pending is None:
        return

    if isinstance(pending, asyncio.Future):
        if not pending.done():
            pending.set_result(result)
    elif isinstance(pending, threading.Event):
        _sync_results[request_id] = result
        pending.set()
