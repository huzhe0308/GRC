"""WebSocket server for Bridge Agent connections.

Runs alongside the HTTP server on a separate port (7861 by default).
Bridge agents connect here, authenticate with their session token,
and receive COM commands to execute locally.
"""
from __future__ import annotations

import asyncio
import json
import time
import sys
import traceback

import websockets
from websockets.server import WebSocketServerProtocol

from auth import verify_token
from bridge_manager import register_bridge, unregister_bridge, resolve_bridge_result, is_bridge_connected, set_event_loop


async def handler(websocket: WebSocketServerProtocol) -> None:
    """Handle a bridge agent connection."""
    username = None
    try:
        # Extract token from query string
        path = websocket.request.path if hasattr(websocket, 'request') else websocket.path
        if '?' in path:
            query = path.split('?', 1)[1]
            params = dict(p.split('=', 1) for p in query.split('&') if '=' in p)
            token = params.get('token', '')
        else:
            # Try Authorization header
            headers = websocket.request.headers if hasattr(websocket, 'request') else {}
            auth = headers.get('Authorization', '')
            token = auth.replace('Bearer ', '') if auth.startswith('Bearer ') else ''

        user = verify_token(token)
        if not user:
            await websocket.send(json.dumps({"type": "error", "message": "Authentication failed"}))
            await websocket.close(code=4001, reason="Auth failed")
            return

        username = user['username']
        print(f"[WS] Bridge connected: {username}", flush=True)

        # Register this connection
        register_bridge(username, websocket)

        await websocket.send(json.dumps({
            "type": "welcome",
            "message": f"Bridge connected as {username}",
            "timestamp": time.time(),
        }))

        # Listen for messages (command results)
        async for message in websocket:
            try:
                data = json.loads(message)
                if data.get('type') == 'hello':
                    print(f"[WS] Bridge {username} says hello: {data.get('message', '')}", flush=True)
                    continue
                # Command result
                msg_id = data.get('id', '')
                result = data.get('result', data)
                resolve_bridge_result(msg_id, result)
            except json.JSONDecodeError:
                print(f"[WS] Invalid JSON from {username}: {message[:100]}", flush=True)

    except websockets.exceptions.ConnectionClosed:
        pass
    except Exception as e:
        print(f"[WS] Error: {e}\n{traceback.format_exc()}", flush=True)
    finally:
        if username:
            unregister_bridge(username)
            print(f"[WS] Bridge disconnected: {username}", flush=True)


async def start_ws_server(port: int = 7861) -> None:
    """Start the WebSocket server."""
    set_event_loop(asyncio.get_event_loop())
    print(f"[WS] Starting WebSocket server on port {port}...", flush=True)
    async with websockets.serve(handler, "0.0.0.0", port, ping_interval=30, ping_timeout=10):
        print(f"[WS] WebSocket server listening on ws://0.0.0.0:{port}", flush=True)
        await asyncio.Future()  # Run forever


def run_ws_server(port: int = 7861) -> None:
    """Run WebSocket server in blocking mode (call from a thread)."""
    asyncio.run(start_ws_server(port))
