"""GRC Agent Local Client — starts HTTP server + opens browser + system tray."""
import os
import sys
import time
import threading
import socket
import webbrowser
from pathlib import Path


def get_app_root():
    """Determine the application root directory.

    When running as a PyInstaller bundle, frozen data is in _MEIPASS (read-only temp).
    Runtime files (SQLite, reports, chat) go next to the exe (sys.executable's dir).
    """
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


APP_ROOT = get_app_root()

os.environ.setdefault("DEMO_HOST", "127.0.0.1")
os.environ.setdefault("LOCAL_CLIENT", "1")


def load_env_file():
    """Load .env file from exe directory (or script dir when not frozen)."""
    env_path = APP_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val


def setup_frozen_paths():
    """When frozen, patch app module paths so data files are found correctly.
    Database (Turso) is NOT overridden — uses TURSO_URL env var for cloud DB, same as Railway."""
    if not getattr(sys, 'frozen', False):
        return

    frozen_root = Path(sys._MEIPASS).resolve()

    runtime_dir = APP_ROOT / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    import app as app_module
    app_module.APP_ROOT = APP_ROOT
    app_module.CONFIG_PATH = APP_ROOT / "config.yaml"
    app_module.REPORTS_DIR = runtime_dir / "reports"
    app_module.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    app_module.WIKI_DIR = frozen_root / "wiki"
    app_module.STATIC_DIR = frozen_root / "demo_app" / "static"
    app_module.LAYER3_EXCEL_PATH = runtime_dir / "Export_Markets_Layer3_Comparison.xlsx"

    for d in ["scripts", "wiki"]:
        scripts_dir = frozen_root / d
        if scripts_dir.exists():
            sys.path.insert(0, str(scripts_dir))

    contacts = APP_ROOT / "contacts.json"
    if not contacts.exists():
        frozen_contacts = frozen_root / "contacts.json"
        if frozen_contacts.exists():
            import shutil
            shutil.copy2(frozen_contacts, contacts)


def find_free_port(default_port=7860):
    """Find a free port, starting from default_port."""
    for port in range(default_port, default_port + 20):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    return default_port


def ensure_dirs():
    """Create runtime directories."""
    for d in ["runtime", "runtime/reports"]:
        (APP_ROOT / d).mkdir(parents=True, exist_ok=True)
    if not (APP_ROOT / "wiki").exists():
        (APP_ROOT / "wiki").mkdir(parents=True, exist_ok=True)


def open_browser(url, delay=1.5):
    """Open pywebview window after server is ready."""
    def _open():
        time.sleep(delay)
        try:
            import webview
            webview.create_window(
                "GRC Agent",
                url + "?local=1",
                width=1400,
                height=900,
                min_size=(1000, 600),
                text_select=True,
            )
            webview.start()
            os._exit(0)
        except ImportError:
            import webbrowser
            webbrowser.open(url + "?local=1")
    threading.Thread(target=_open, daemon=True).start().start()


def run_tray(port):
    """No-op when using pywebview — the window IS the tray."""
    pass


def main():
    ensure_dirs()

    sys.path.insert(0, str(APP_ROOT / "demo_app"))
    sys.path.insert(0, str(APP_ROOT))

    load_env_file()

    setup_frozen_paths()

    port = find_free_port()
    os.environ["PORT"] = str(port)
    os.environ["LOCAL_CLIENT"] = "1"
    url = f"http://127.0.0.1:{port}"

    if os.environ.get("TURSO_URL"):
        print(f"[GRC Agent] Cloud DB: {os.environ['TURSO_URL'][:30]}...")
    else:
        print("[GRC Agent] WARNING: TURSO_URL not set. Create .env file with Turso credentials.")

    print(f"[GRC Agent] Starting local server on {url}")

    def run_server():
        try:
            from auth import init_db as init_auth_db
            init_auth_db()

            from http.server import ThreadingHTTPServer
            from app import DemoHandler

            server = ThreadingHTTPServer(("127.0.0.1", port), DemoHandler)
            print(f"[GRC Agent] Server running at {url}")
            server.serve_forever()
        except Exception as e:
            print(f"[GRC Agent] Server error: {e}")
            import traceback
            traceback.print_exc()

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()

    time.sleep(2.0)

    try:
        import webview
        print(f"[GRC Agent] Opening window...")
        webview.create_window(
            "GRC Agent",
            url,
            width=1400,
            height=900,
            min_size=(1000, 600),
            text_select=True,
        )
        webview.start()
    except ImportError:
        print("[GRC Agent] pywebview not available, opening browser...")
        import webbrowser
        webbrowser.open(url)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    print("[GRC Agent] Shutting down...")
    os._exit(0)


if __name__ == "__main__":
    main()
