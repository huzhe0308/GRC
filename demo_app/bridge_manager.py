"""Bridge connection manager - supports HTTP polling (no WebSocket needed).

Bridge agents poll /api/bridge/poll for commands and POST results to /api/bridge/result.
"""
from __future__ import annotations

import json
import queue
import threading
import time
import uuid
from typing import Any

_bridge_connections: dict[str, dict] = {}
_command_queues: dict[str, queue.Queue] = {}
_pending_results: dict[str, threading.Event] = {}
_sync_results: dict[str, dict] = {}


def register_bridge_http(username: str) -> None:
    _bridge_connections[username] = {"last_poll": time.time()}
    if username not in _command_queues:
        _command_queues[username] = queue.Queue()


def unregister_bridge(username: str) -> None:
    _bridge_connections.pop(username, None)
    _command_queues.pop(username, None)


def is_bridge_connected(username: str) -> bool:
    conn = _bridge_connections.get(username)
    if not conn:
        return False
    if time.time() - conn.get("last_poll", 0) > 30:
        return False
    return True


def get_bridge_status(username: str) -> dict:
    if username and is_bridge_connected(username):
        return {"connected": True, "message": "Outlook Bridge is online", "username": username}
    return {"connected": False, "message": "Outlook Bridge is offline. Run the Bridge Agent on your machine to enable email features.", "username": username}


def poll_commands(username: str) -> dict:
    register_bridge_http(username)
    _bridge_connections[username]["last_poll"] = time.time()
    q = _command_queues.get(username)
    if not q:
        return {"commands": []}
    commands = []
    try:
        while True:
            cmd = q.get_nowait()
            commands.append(cmd)
    except queue.Empty:
        pass
    return {"commands": commands}


def submit_result(request_id: str, result: dict) -> None:
    event = _pending_results.get(request_id)
    if event:
        _sync_results[request_id] = result
        event.set()


def send_bridge_command_sync(username: str, command: str, params: dict = None, timeout: float = 30.0) -> dict:
    """Send command to bridge via HTTP polling and wait for result."""
    if not is_bridge_connected(username):
        return {"ok": False, "error": "Bridge not connected"}

    request_id = str(uuid.uuid4())
    q = _command_queues.setdefault(username, queue.Queue())
    q.put({"id": request_id, "command": command, "params": params or {}})

    event = threading.Event()
    _pending_results[request_id] = event
    _sync_results[request_id] = None

    if event.wait(timeout=timeout):
        result = _sync_results.get(request_id, {"ok": False, "error": "No result"})
    else:
        result = {"ok": False, "error": "Bridge command timed out"}

    _pending_results.pop(request_id, None)
    _sync_results.pop(request_id, None)
    return result


# Legacy WS compat (unused but kept for import compatibility)
def register_bridge(username: str, websocket: Any = None) -> None:
    register_bridge_http(username)


def set_event_loop(loop: Any = None) -> None:
    pass


def resolve_bridge_result(request_id: str, result: dict) -> None:
    submit_result(request_id, result)


async def send_bridge_command_async(username: str, command: str, params: dict = None, timeout: float = 30.0) -> dict:
    return send_bridge_command_sync(username, command, params, timeout)
