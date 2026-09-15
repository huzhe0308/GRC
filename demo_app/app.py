#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
from urllib.request import Request, urlopen
import urllib.error


APP_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = APP_ROOT / "config.yaml"
REPORTS_DIR = APP_ROOT / "runtime" / "reports"
DB_PATH = APP_ROOT / "runtime" / "state.sqlite"
WIKI_DIR = APP_ROOT / "wiki"
STATIC_DIR = Path(__file__).resolve().parent / "static"
LAYER3_EXCEL_PATH = APP_ROOT / "runtime" / "Export_Markets_Layer3_Comparison.xlsx"
MONTHLY_REPORT_DEFAULT_TO = [
    "kai.kunze@volkswagen-tech.com", "yi.yu@volkswagen-tech.com", "dawei.chen@cariad-technology.cn",
    "alvaro.huascar.hekler.merino@volkswagen-tech.com", "shuo.he@volkswagen-tech.com", "yumin.ren@volkswagen-tech.com",
    "hao.sun@volkswagen-tech.com", "wei.zhu@cariad-technology.cn", "zhaolong.wang@volkswagen-tech.com",
    "zhenxing.wang@volkswagen-tech.com",
]
MONTHLY_REPORT_DEFAULT_CC = [
    "xiaochen.sun@volkswagen-tech.com", "wenbo.ma1@volkswagen-tech.com", "xin.cheng@volkswagen-tech.com",
    "li.wang3@cariad-technology.cn", "yiwen.cai@cariad-technology.cn", "extern.chengge.wang@volkswagen-tech.com",
    "zhishuo.zhang@volkswagen-tech.com", "richard.ling@volkswagen-tech.com", "jinfeng.cheng@volkswagen-tech.com",
]
PYTHON = sys.executable or "python"


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8", errors="replace")
    return text[:limit] if limit else text


def load_config() -> dict:
    try:
        import yaml  # type: ignore

        return yaml.safe_load(read_text(CONFIG_PATH)) or {}
    except Exception:
        return {}


def safe_rel_path(base: Path, rel: str) -> Path:
    rel = unquote(rel or "").replace("\\", "/").lstrip("/")
    target = (base / rel).resolve()
    root = base.resolve()
    try:
        target.relative_to(root)
    except ValueError as exc:
        raise ValueError("Path is outside the allowed folder") from exc
    return target


def json_response(handler: BaseHTTPRequestHandler, payload: object, status: int = 200) -> None:
    raw = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def text_response(handler: BaseHTTPRequestHandler, text: str, content_type: str = "text/plain; charset=utf-8", status: int = 200) -> None:
    raw = text.encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Content-Length", str(len(raw)))
    handler.end_headers()
    handler.wfile.write(raw)


def run_agent(args: list[str], timeout: int = 900) -> dict:
    cmd = [PYTHON, "-B", str(APP_ROOT / "scripts" / "run_daily_report.py"), "--config", str(CONFIG_PATH), *args]
    started = time.time()
    proc = subprocess.run(
        cmd,
        cwd=str(APP_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        encoding="utf-8",
        errors="replace",
    )
    output = proc.stdout or ""
    report_match = re.findall(r"\[OK\] Report generated:\s*(.+)", output)
    return {
        "ok": proc.returncode == 0,
        "returncode": proc.returncode,
        "seconds": round(time.time() - started, 1),
        "output": output[-12000:],
        "report_path": report_match[-1].strip() if report_match else "",
    }


def list_reports() -> list[dict]:
    if not REPORTS_DIR.exists():
        return []
    reports = []
    for path in sorted(REPORTS_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
        text = read_text(path, limit=2500)
        title = next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("# ")), path.name)
        status = ""
        source = ""
        run_id = ""
        for line in text.splitlines()[:80]:
            if "Status:" in line:
                status = line.split("Status:", 1)[-1].strip().strip("` ")
            if "Answer source:" in line:
                source = line.split("Answer source:", 1)[-1].strip().strip("` ")
            if "Run ID:" in line:
                run_id = line.split("Run ID:", 1)[-1].strip().strip("` ")
        reports.append(
            {
                "name": path.name,
                "path": str(path),
                "title": title,
                "run_id": run_id,
                "status": status,
                "answer_source": source,
                "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(path.stat().st_mtime)),
                "size": path.stat().st_size,
            }
        )
    return reports


def list_runs(limit: int = 20) -> list[dict]:
    if not DB_PATH.exists():
        return []
    try:
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "select run_id, started_at, finished_at, status, report_path, error from runs order by started_at desc limit ?",
                (limit,),
            ).fetchall()
        return [
            {
                "run_id": row[0],
                "started_at": row[1],
                "finished_at": row[2],
                "status": row[3],
                "report_path": row[4],
                "error": row[5],
            }
            for row in rows
        ]
    except Exception as exc:
        return [{"error": str(exc)}]


def wiki_counts() -> dict:
    counts = {}
    for name in ["concepts", "entities", "comparisons", "queries"]:
        folder = WIKI_DIR / name
        counts[name] = len(list(folder.glob("**/*.md"))) if folder.exists() else 0
    raw_folder = WIKI_DIR / "raw"
    if raw_folder.exists():
        raw_all = list(raw_folder.glob("**/*.md"))
        raw_count = sum(1 for p in raw_all if not (p.name == "text.md" and (p.parent.parent / (p.parent.name + ".md")).exists()))
        counts["raw"] = raw_count
    else:
        counts["raw"] = 0
    return counts


def wiki_files() -> list[dict]:
    files = []
    for layer in ["concepts", "entities", "comparisons", "queries"]:
        folder = WIKI_DIR / layer
        if not folder.exists():
            continue
        for path in sorted(folder.glob("**/*.md")):
            rel = path.relative_to(WIKI_DIR).as_posix()
            filename = path.name
            layer_name = layer
            files.append({"path": rel, "name": filename, "layer": layer_name, "size": path.stat().st_size})

    raw_folder = WIKI_DIR / "raw"
    if raw_folder.exists():
        files = []
        for path in sorted(raw_folder.glob("**/*.md")):
            rel = path.relative_to(WIKI_DIR).as_posix()
            filename = path.name
            if path.name == "text.md":
                sibling = path.parent.parent / (path.parent.name + ".md")
                if sibling.exists():
                    continue
            if path.parent == raw_folder:
                layer_name = "raw"
            else:
                parent_name = path.parent.name
                layer_name = f"raw/{parent_name}"
            files.append({"path": rel, "name": filename, "layer": layer_name, "size": path.stat().st_size})
    return files


def wiki_search(query: str, limit: int = 10, include_raw: bool = True) -> dict:
    if not query.strip():
        return {"hits": []}
    args = [str(APP_ROOT / "tools" / "search_wiki.py"), query, "--limit", str(limit), "--json"]
    if include_raw:
        args.append("--raw")
    proc = subprocess.run(
        [PYTHON, "-B", *args],
        cwd=str(APP_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=60,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        return {"hits": [], "error": proc.stderr or proc.stdout}
    try:
        parsed = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        parsed = []
    return {"hits": parsed}


def wiki_search_semantic(query: str, limit: int = 10, include_raw: bool = True) -> dict:
    if not query.strip():
        return {"hits": [], "mode": "semantic"}
    args = [
        str(APP_ROOT / "tools" / "search_wiki.py"),
        query,
        "--limit", str(limit),
        "--semantic",
        "--json",
    ]
    if include_raw:
        args.append("--raw")
    proc = subprocess.run(
        [PYTHON, "-B", *args],
        cwd=str(APP_ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=90,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        return {"hits": [], "error": proc.stderr or proc.stdout, "mode": "semantic"}
    try:
        parsed = json.loads(proc.stdout or "[]")
    except json.JSONDecodeError:
        parsed = []
    return {"hits": parsed, "mode": "semantic"}


def fetch_emails() -> dict:
    import traceback
    import logging
    sys.path.insert(0, str(APP_ROOT))
    try:
        from scripts.run_daily_report import find_emails, load_config as agent_load_config

        config = agent_load_config(CONFIG_PATH)
        mail_cfg = config.get('mail', {})
        print(f"[DEMO] Config loaded: keywords={mail_cfg.get('subject_contains', [])}")
        emails = []
        for email in find_emails(config):
            emails.append(
                {
                    "entryid": email.get("entryid", ""),
                    "subject": email.get("subject", ""),
                    "sender": email.get("sender", ""),
                    "received": email.get("received", ""),
                    "body_preview": email.get("body_preview", ""),
                    "body": email.get("body", ""),
                    "attachments": email.get("attachments", []),
                }
            )
        print(f"[DEMO] Found {len(emails)} emails")
        return {"emails": emails}
    except Exception as exc:
        print(f"[DEMO] Error: {exc}")
        traceback.print_exc()
        return {"emails": [], "error": str(exc), "trace": traceback.format_exc()}


CONTACTS_FILE = APP_ROOT / "contacts.json"


def load_contacts() -> dict:
    """Load contacts from JSON file"""
    try:
        if CONTACTS_FILE.exists():
            return json.loads(CONTACTS_FILE.read_text(encoding="utf-8"))
        return {"contacts": [], "topic_mapping": {}}
    except Exception:
        return {"contacts": [], "topic_mapping": {}}


def save_contacts(data: dict) -> bool:
    """Save contacts to JSON file"""
    try:
        CONTACTS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False


def get_contacts_by_topic(topic: str) -> list:
    """Get contacts recommended for a specific topic"""
    data = load_contacts()
    contact_ids = data.get("topic_mapping", {}).get(topic, [])
    contacts = data.get("contacts", [])
    return [c for c in contacts if c.get("id") in contact_ids and c.get("active", True)]


def get_all_contacts() -> list:
    """Get all active contacts"""
    data = load_contacts()
    return [c for c in data.get("contacts", []) if c.get("active", True)]


@dataclass
class AutomationState:
    enabled: bool = False
    email_interval: str = "daily"
    email_auto_send: bool = False
    email_force: bool = False
    jira_interval: str = "daily"
    jira_alert_new: bool = True
    jira_force: bool = False
    running: bool = False
    last_status: str = "idle"
    last_output: str = ""
    last_email_run: str = ""
    last_jira_run: str = ""
    next_email_run: str = ""
    next_jira_run: str = ""
    thread: threading.Thread | None = None
    stop_event: threading.Event = field(default_factory=threading.Event)
    lock: threading.Lock = field(default_factory=threading.Lock)


AUTOMATION = AutomationState()


def interval_to_seconds(interval: str) -> int:
    mapping = {"hourly": 3600, "6h": 21600, "daily": 86400}
    return mapping.get(interval, 86400)


def automation_snapshot() -> dict:
    with AUTOMATION.lock:
        return {
            "enabled": AUTOMATION.enabled,
            "email_interval": AUTOMATION.email_interval,
            "email_auto_send": AUTOMATION.email_auto_send,
            "email_force": AUTOMATION.email_force,
            "jira_interval": AUTOMATION.jira_interval,
            "jira_alert_new": AUTOMATION.jira_alert_new,
            "jira_force": AUTOMATION.jira_force,
            "running": AUTOMATION.running,
            "last_status": AUTOMATION.last_status,
            "last_output": AUTOMATION.last_output[-5000:],
            "last_email_run": AUTOMATION.last_email_run,
            "last_jira_run": AUTOMATION.last_jira_run,
            "next_email_run": AUTOMATION.next_email_run,
            "next_jira_run": AUTOMATION.next_jira_run,
        }


def automation_loop() -> None:
    last_email_run_time = 0.0
    last_jira_run_time = 0.0
    seen_email_ids = set()
    running_email = False
    running_jira = False
    
    while True:
        with AUTOMATION.lock:
            if not AUTOMATION.enabled:
                AUTOMATION.running = False
                return
            email_seconds = interval_to_seconds(AUTOMATION.email_interval)
            jira_seconds = interval_to_seconds(AUTOMATION.jira_interval)
            AUTOMATION.next_email_run = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + email_seconds))
            AUTOMATION.next_jira_run = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + jira_seconds))
            min_interval = min(email_seconds, jira_seconds)
            enabled = AUTOMATION.enabled
            email_interval = AUTOMATION.email_interval
            email_auto_send = AUTOMATION.email_auto_send
            email_force = AUTOMATION.email_force
            jira_interval = AUTOMATION.jira_interval
            jira_alert_new = AUTOMATION.jira_alert_new
            jira_force = AUTOMATION.jira_force
        
        if not enabled:
            return
            
        if AUTOMATION.stop_event.wait(min_interval):
            continue
        
        current_time = time.time()
        outputs = []
        
        try:
            should_run_email = email_force or (current_time - last_email_run_time) >= interval_to_seconds(email_interval)
            should_run_jira = jira_force or (current_time - last_jira_run_time) >= interval_to_seconds(jira_interval)
            
            if should_run_email:
                last_email_run_time = current_time
                AUTOMATION.last_email_run = time.strftime("%Y-%m-%d %H:%M:%S")
                
                # Check for new emails before running agent
                try:
                    email_data = fetch_emails()
                    all_emails = email_data.get("emails", [])
                    current_email_ids = set(e.get("entryid", "") for e in all_emails)
                    
                    # Find new emails
                    new_email_ids = current_email_ids - seen_email_ids
                    if new_email_ids and seen_email_ids:  # Only alert if we have previous data
                        new_email_count = len(new_email_ids)
                        new_subjects = [e.get("subject", "无主题")[:40] for e in all_emails if e.get("entryid", "") in new_email_ids][:3]
                        outputs.append(f"[新邮件] 发现 {new_email_count} 封新邮件")
                        for subj in new_subjects:
                            outputs.append(f"  - {subj}")
                    
                    # Update seen emails
                    seen_email_ids.update(current_email_ids)
                except Exception as email_check_err:
                    outputs.append(f"[邮件检查] 警告: {str(email_check_err)}")
                
                args = ["--send-now" if email_auto_send else "--dry-run"]
                if email_force:
                    args.append("--force")
                result = run_agent(args)
                if result.get("ok"):
                    outputs.append(f"[邮件] 报告生成成功")
                else:
                    outputs.append(f"[邮件] {result.get('message', '处理完成')}")
                with AUTOMATION.lock:
                    AUTOMATION.email_force = False
            
            if should_run_jira:
                last_jira_run_time = current_time
                AUTOMATION.last_jira_run = time.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    data = get_export_markets_data()
                    new_tickets = sum(1 for m in data.get("markets", []) 
                                     for t in m.get("tickets", []) 
                                     if t.get("status") in ["Open", "IN EVALUATION"])
                    outputs.append(f"[Jira] 发现 {new_tickets} 个活跃工单")
                    if jira_alert_new and new_tickets > 0:
                        outputs.append(f"[提醒] 有 {new_tickets} 个工单需要关注")
                except Exception as jira_err:
                    outputs.append(f"[Jira] 获取失败: {str(jira_err)}")
                with AUTOMATION.lock:
                    AUTOMATION.jira_force = False
            
            with AUTOMATION.lock:
                AUTOMATION.last_status = "ok"
                AUTOMATION.last_output = "\n".join(outputs) if outputs else "巡检完成，无更新"
        except Exception as e:
            with AUTOMATION.lock:
                AUTOMATION.last_status = "error"
                AUTOMATION.last_output = str(e)
        finally:
            with AUTOMATION.lock:
                AUTOMATION.running = False


import base64 as _b64

AUTH_USERS = {
    "admin": "grc2026",
    "guest": "grc2026",
}

class DemoHandler(BaseHTTPRequestHandler):
    server_version = "GRCAgentDemo/1.0"

    def log_message(self, format: str, *args: object) -> None:
        return

    def _check_auth(self) -> bool:
        hdr = self.headers.get("Authorization", "")
        if hdr.startswith("Basic "):
            try:
                decoded = _b64.b64decode(hdr[6:]).decode()
                user, pwd = decoded.split(":", 1)
                return AUTH_USERS.get(user) == pwd
            except Exception:
                pass
        return False

    def _auth_required(self) -> bool:
        if not self._check_auth():
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="GRC Agent"')
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"Authentication required")
            return True
        return False

    def _send_sse_headers(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

    def _sse_send(self, event: str, data: str) -> None:
        try:
            self.wfile.write(f"event: {event}\ndata: {data}\n\n".encode("utf-8"))
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _stream_analysis(self, action: str) -> None:
        import threading
        cancelled = {"flag": False}

        def emit(status: str, message: str, extra: dict = None) -> None:
            if cancelled["flag"]:
                return
            payload = json.dumps({"status": status, "message": message, **(extra or {})}, ensure_ascii=False)
            self._sse_send("progress", payload)

        def run():
            try:
                action_map = {
                    "deep_jira": ("Deep Jira Analysis", ANALYSIS_SCRIPTS / "deep_jira_analysis.py"),
                    "market_overview": ("Market Overview Analysis", ANALYSIS_SCRIPTS / "comprehensive_analysis.py"),
                    "obd_data": ("OBD Verification", ANALYSIS_SCRIPTS / "verify_obd_data.py"),
                    "cyber_security": ("Cyber Security Verification", ANALYSIS_SCRIPTS / "verify_cyber_security.py"),
                    "layer3_excel": ("Generate Layer3 Excel Report", ANALYSIS_SCRIPTS / "create_excel_final.py"),
                    "fusa_data": ("FuSa Verification", ANALYSIS_SCRIPTS / "verify_fusa.py"),
                    "ota_data": ("OTA and SW Update Verification", ANALYSIS_SCRIPTS / "verify_ota.py"),
                    "immobilizer_data": ("Immobilizer Verification", ANALYSIS_SCRIPTS / "verify_immobilizer.py"),
                }
                info = action_map.get(action)
                if not info:
                    emit("failed", f"Unknown action: {action}")
                    return

                emit("step", f"Preparing to run {info[0]}...", {"step": "prepare"})
                script_path = info[1]

                if not script_path.exists():
                    emit("failed", f"Script not found: {script_path}")
                    return

                emit("step", f"Running analysis script...", {"step": "analyzing"})
                import io
                proc = subprocess.Popen(
                    [PYTHON, str(script_path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=str(ANALYSIS_SCRIPTS),
                    encoding="utf-8",
                    errors="replace"
                )

                output_lines = []
                for line in iter(proc.stdout.readline, ""):
                    if cancelled["flag"]:
                        proc.terminate()
                        emit("cancelled", "Cancelled by user")
                        return
                    stripped = line.rstrip()
                    import re
                    stripped = re.sub(r"\x1b\[[0-9;]*m", "", stripped)
                    if stripped.strip():
                        output_lines.append(stripped)
                        if len(output_lines) <= 3:
                            emit("step", f"Analyzing: {stripped[:80]}", {"step": "analyzing", "snippet": stripped[:80]})

                proc.wait()
                output = "\n".join(output_lines)

                if proc.returncode != 0 and not output.strip():
                    output = f"[完成] {info[0]} 执行完成（exit {proc.returncode}）"

                emit("step", "正在渲染结果...", {"step": "rendering"})
                self._sse_send("done", json.dumps({"output": output, "returncode": proc.returncode, "script": script_path.name}, ensure_ascii=False))
            except Exception as e:
                emit("failed", f"分析失败: {str(e)}")

        t = threading.Thread(target=run, daemon=True)
        t.start()
        try:
            t.join()
        except KeyboardInterrupt:
            cancelled["flag"] = True

    def do_GET(self) -> None:
        if self._auth_required():
            return
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            qs = parse_qs(parsed.query)
            
            # Debug logging
            print(f"[API] GET {path} query={dict(qs)}")
            
            if path == "/":
                return self.serve_static("index.html", "text/html; charset=utf-8")
            if path.startswith("/static/"):
                rel = path.removeprefix("/static/")
                ctype = "application/javascript; charset=utf-8" if rel.endswith(".js") else "text/css; charset=utf-8"
                return self.serve_static(rel, ctype)
            if path == "/api/status":
                cfg = load_config()
                llm = cfg.get("llm", {}) if isinstance(cfg.get("llm", {}), dict) else {}
                send = cfg.get("send", {}) if isinstance(cfg.get("send", {}), dict) else {}
                mail = cfg.get("mail", {}) if isinstance(cfg.get("mail", {}), dict) else {}
                return json_response(
                    self,
                    {
                        "model": llm.get("model", ""),
                        "api_key_set": bool(str(llm.get("api_key", "")).strip()),
                        "send_dry_run": bool(send.get("dry_run", True)),
                        "send_to": send.get("to", []),
                        "mail_backend": mail.get("backend", ""),
                        "mail_keyword": mail.get("subject_contains", []),
                        "reports": len(list_reports()),
                        "wiki_counts": wiki_counts(),
                        "runs": list_runs(8),
                        "automation": automation_snapshot(),
                    },
                )
            if path == "/api/emails":
                return json_response(self, fetch_emails())
            if path == "/api/assessments/sent":
                return json_response(self, get_assessments_sent())
            if path == "/api/reports":
                return json_response(self, {"reports": list_reports()})
            if path == "/api/report":
                report_path = Path(qs.get("path", [""])[0])
                if not report_path.is_absolute():
                    report_path = safe_rel_path(REPORTS_DIR, report_path.as_posix())
                else:
                    report_path = report_path.resolve()
                    report_path.relative_to(REPORTS_DIR.resolve())
                return json_response(self, {"path": str(report_path), "text": read_text(report_path, limit=800000)})
            if path == "/api/wiki/list":
                return json_response(self, {"files": wiki_files(), "counts": wiki_counts()})
            if path == "/api/wiki/file":
                target = safe_rel_path(WIKI_DIR, qs.get("path", [""])[0])
                return json_response(self, {"path": target.relative_to(WIKI_DIR).as_posix(), "text": read_text(target, limit=800000)})
            if path == "/api/wiki/search":
                query = qs.get("q", [""])[0]
                limit = int(qs.get("limit", ["10"])[0])
                return json_response(self, wiki_search(query, limit=limit))
            if path == "/api/wiki/search-semantic":
                query = qs.get("q", [""])[0]
                limit = int(qs.get("limit", ["10"])[0])
                return json_response(self, wiki_search_semantic(query, limit=limit))
            if path == "/api/automation":
                return json_response(self, automation_snapshot())
            if path == "/api/jira/tickets":
                return json_response(self, get_jira_tickets())
            if path == "/api/jira/search":
                jql = qs.get("jql", [""])[0]
                return json_response(self, search_jira_tickets(jql))
            if path == "/api/jira/issue":
                key = qs.get("key", [""])[0]
                return json_response(self, get_jira_issue(key))
            if path == "/api/jira/refresh":
                return json_response(self, refresh_jira_tickets())
            if path == "/api/export-markets/data":
                return json_response(self, get_export_markets_data())
            if path == "/api/export-markets/ticket-detail":
                key = qs.get("key", [""])[0]
                return json_response(self, get_jira_issue(key))
            if path == "/api/export-markets/verify-ticket":
                key = qs.get("key", [""])[0]
                return json_response(self, verify_jira_ticket_status(key))
            if path == "/api/export-markets/generate-report":
                return json_response(self, generate_export_markets_report())
            if path == "/api/monthly-report/generate":
                return json_response(self, generate_monthly_report_html())
            if path == "/api/assessment/parse-pvs":
                parent_key = qs.get("parent", [""])[0]
                filename = qs.get("file", [""])[0]
                return json_response(self, parse_pvs_excel(parent_key, filename))
            if path == "/api/assessment/sync-wiki":
                return json_response(self, sync_pvs_wiki())
            if parsed.path == "/api/gap-tracking/status":
                return json_response(self, gap_tracking_status())
            if parsed.path == "/api/gap-tracking/updates":
                since = qs.get("since", [""])[0]
                return json_response(self, get_gap_updates(since))
            if parsed.path == "/api/gap-tracking/monitor-status":
                with JIRA_MONITOR.lock:
                    return json_response(self, {
                        "running": JIRA_MONITOR.running,
                        "enabled": JIRA_MONITOR.enabled,
                        "interval_sec": JIRA_MONITOR.interval_sec,
                        "last_check": JIRA_MONITOR.last_check,
                        "next_check": JIRA_MONITOR.next_check,
                    })
            if parsed.path == "/api/gap-tracking/inspection":
                return json_response(self, {**get_last_inspection(), "monitor": {
                    "running": JIRA_MONITOR.running,
                    "enabled": JIRA_MONITOR.enabled,
                    "last_check": JIRA_MONITOR.last_check,
                    "next_check": JIRA_MONITOR.next_check,
                }})
            if path == "/api/contacts":
                return json_response(self, {"contacts": get_all_contacts()})
            if path == "/api/contacts/by-topic":
                topic = qs.get("topic", [""])[0]
                return json_response(self, {"contacts": get_contacts_by_topic(topic), "topic": topic})
            if path == "/api/chat/sessions":
                return json_response(self, {"sessions": get_chat_sessions()})
            if path == "/api/chat/messages":
                session_id = qs.get("session", [""])[0]
                limit = int(qs.get("limit", ["50"])[0])
                return json_response(self, {"messages": get_chat_messages(session_id, limit)})
            if path == "/api/chat/search":
                query = qs.get("q", [""])[0]
                return json_response(self, search_knowledge_base(query))
            if path == "/api/outlook/latest":
                sender = qs.get("sender", [""])[0]
                return json_response(self, outlook_latest_email(sender))
            if path == "/api/outlook/search":
                query = qs.get("q", [""])[0]
                max_results = int(qs.get("limit", ["10"])[0])
                return json_response(self, outlook_search_emails(query, max_results))
            if path == "/api/outlook/needs-reply":
                date_filter = qs.get("date", ["today"])[0]
                return json_response(self, outlook_needs_reply(date_filter))
            if path == "/api/outlook/contact":
                name = qs.get("name", [""])[0]
                return json_response(self, outlook_find_contact(name))
            if path == "/api/outlook/detail":
                entry_id = qs.get("entry_id", [""])[0]
                return json_response(self, outlook_email_detail(entry_id))
            if path == "/api/gap-tracking/status":
                return json_response(self, gap_tracking_status())
            if path == "/api/outlook/yesterday":
                return json_response(self, outlook_yesterday_emails())
            return json_response(self, {"error": "Not found"}, status=404)
        except Exception as exc:
            return json_response(self, {"error": str(exc), "trace": traceback.format_exc()}, status=500)

    def do_POST(self) -> None:
        if self._auth_required():
            return
        try:
            parsed = urlparse(self.path)
            body = self.read_json()
            if parsed.path == "/api/run":
                args = ["--send-now" if body.get("send_now") else "--dry-run"]
                if body.get("force"):
                    args.append("--force")
                return json_response(self, run_agent(args))
            if parsed.path == "/api/send-report":
                report_path = str(body.get("path", "")).strip()
                if not report_path:
                    return json_response(self, {"ok": False, "error": "Missing report path"}, status=400)
                return json_response(self, run_agent(["--send-report", report_path, "--send-now"]))
            if parsed.path == "/api/automation":
                action = str(body.get("action", "")).lower()
                with AUTOMATION.lock:
                    if action == "start":
                        AUTOMATION.email_interval = str(body.get("email_interval", "daily"))
                        AUTOMATION.email_auto_send = bool(body.get("email_auto_send", False))
                        AUTOMATION.email_force = bool(body.get("email_force", False))
                        AUTOMATION.jira_interval = str(body.get("jira_interval", "daily"))
                        AUTOMATION.jira_alert_new = bool(body.get("jira_alert_new", True))
                        AUTOMATION.jira_force = bool(body.get("jira_force", False))
                        AUTOMATION.enabled = True
                        AUTOMATION.stop_event.set()
                        AUTOMATION.stop_event = threading.Event()
                        if not AUTOMATION.thread or not AUTOMATION.thread.is_alive():
                            AUTOMATION.thread = threading.Thread(target=automation_loop, daemon=True)
                            AUTOMATION.thread.start()
                        AUTOMATION.last_status = "monitoring"
                    elif action == "stop":
                        AUTOMATION.enabled = False
                        AUTOMATION.stop_event.set()
                        AUTOMATION.last_status = "stopped"
                    else:
                        return json_response(self, {"error": "Unknown automation action"}, status=400)
                return json_response(self, automation_snapshot())
            if parsed.path == "/api/assessment/send":
                return json_response(self, send_assessment_email(body))
            if parsed.path == "/api/contacts":
                action = body.get("action", "")
                data = load_contacts()
                if action == "add":
                    new_contact = {
                        "id": f"c{len(data['contacts']) + 1:03d}",
                        "name": body.get("name", ""),
                        "email": body.get("email", ""),
                        "topics": body.get("topics", []),
                        "role": body.get("role", ""),
                        "active": True
                    }
                    data["contacts"].append(new_contact)
                    save_contacts(data)
                    return json_response(self, {"ok": True, "contact": new_contact})
                elif action == "update":
                    contact_id = body.get("id", "")
                    for c in data["contacts"]:
                        if c["id"] == contact_id:
                            c["name"] = body.get("name", c["name"])
                            c["email"] = body.get("email", c["email"])
                            c["topics"] = body.get("topics", c["topics"])
                            c["role"] = body.get("role", c["role"])
                            c["active"] = body.get("active", c["active"])
                            break
                    save_contacts(data)
                    return json_response(self, {"ok": True})
                elif action == "delete":
                    contact_id = body.get("id", "")
                    data["contacts"] = [c for c in data["contacts"] if c["id"] != contact_id]
                    save_contacts(data)
                    return json_response(self, {"ok": True})
                elif action == "update-mapping":
                    data["topic_mapping"] = body.get("topic_mapping", data["topic_mapping"])
                    save_contacts(data)
                    return json_response(self, {"ok": True})
                return json_response(self, {"error": "Unknown action"}, status=400)
            if parsed.path.startswith("/api/analysis/"):
                action = parsed.path.rsplit("/", 1)[-1]
                if body and body.get("_stream"):
                    self._send_sse_headers()
                    return self._stream_analysis(action)
                return json_response(self, run_analysis_action(action, body))
            if parsed.path == "/api/chat/send":
                session_id = body.get("session_id", "")
                message = body.get("message", "")
                if not session_id:
                    # Create new session
                    session_result = create_chat_session()
                    if not session_result.get("ok"):
                        return json_response(self, session_result, status=500)
                    session_id = session_result["session"]["id"]
                if not message.strip():
                    return json_response(self, {"ok": False, "error": "Message is empty"}, status=400)
                return json_response(self, chat_with_llm(session_id, message))
            if parsed.path == "/api/outlook/assistant":
                message = body.get("message", "")
                intent_result = assistant_intent_router(message)
                return json_response(self, intent_result)
            if parsed.path == "/api/outlook/detail":
                entry_id = body.get("entry_id", "")
                return json_response(self, outlook_email_detail(entry_id))
            if parsed.path == "/api/chat/new-session":
                title = body.get("title")
                return json_response(self, create_chat_session(title))
            if parsed.path == "/api/chat/delete-session":
                session_id = body.get("session_id", "")
                return json_response(self, delete_chat_session(session_id))
            if parsed.path == "/api/monthly-report/generate":
                to = body.get("to") or MONTHLY_REPORT_DEFAULT_TO
                cc = body.get("cc") or MONTHLY_REPORT_DEFAULT_CC
                return json_response(self, generate_monthly_report_html(to, cc))
            if parsed.path == "/api/monthly-report/send-draft":
                to = body.get("to") or MONTHLY_REPORT_DEFAULT_TO
                cc = body.get("cc") or MONTHLY_REPORT_DEFAULT_CC
                return json_response(self, send_monthly_report_draft(to, cc))
            if parsed.path == "/api/gap-tracking/status":
                return json_response(self, gap_tracking_status())
            if parsed.path == "/api/gap-tracking/complete":
                market = str(body.get("market", "")).strip()
                topic = str(body.get("topic", "")).strip()
                if not market or not topic:
                    return json_response(self, {"ok": False, "error": "Missing market or topic"}, status=400)
                return json_response(self, gap_tracking_complete(market, topic))
            if parsed.path == "/api/gap-tracking/reset":
                market = str(body.get("market", "")).strip()
                topic = str(body.get("topic", "")).strip()
                if not market or not topic:
                    return json_response(self, {"ok": False, "error": "Missing market or topic"}, status=400)
                return json_response(self, gap_tracking_reset(market, topic))
            if parsed.path == "/api/gap-tracking/close-layer3":
                market = str(body.get("market", "")).strip()
                if not market:
                    return json_response(self, {"ok": False, "error": "Missing market"}, status=400)
                return json_response(self, close_layer3_ticket(market))
            if parsed.path == "/api/gap-tracking/write-summary":
                market = str(body.get("market", "")).strip()
                if not market:
                    return json_response(self, {"ok": False, "error": "Missing market"}, status=400)
                return json_response(self, write_summary_comment(market))
            if parsed.path == "/api/gap-tracking/set-status":
                market = str(body.get("market", "")).strip()
                topic = str(body.get("topic", "")).strip()
                status = str(body.get("status", "")).strip()
                gap_summary = str(body.get("gap_summary", "")).strip()
                if not market or not topic or not status:
                    return json_response(self, {"ok": False, "error": "Missing market, topic, or status"}, status=400)
                return json_response(self, gap_tracking_set_status(market, topic, status, gap_summary))
            if parsed.path == "/api/gap-tracking/updates":
                since = qs.get("since", [""])[0]
                return json_response(self, get_gap_updates(since))
            if parsed.path == "/api/gap-tracking/trigger-check":
                return json_response(self, trigger_gap_check_now())
            if parsed.path == "/api/gap-tracking/mark-read":
                mark_updates_read()
                return json_response(self, {"ok": True})
            if parsed.path == "/api/gap-tracking/monitor":
                action = str(body.get("action", "")).lower()
                interval = int(body.get("interval", 1800))
                if action == "start":
                    start_jira_gap_monitor(interval)
                    return json_response(self, {"ok": True, "running": True, "interval": interval})
                elif action == "stop":
                    stop_jira_gap_monitor()
                    return json_response(self, {"ok": True, "running": False})
                else:
                    return json_response(self, {"ok": False, "error": "Unknown action"}, status=400)
            if parsed.path == "/api/gap-tracking/monitor-status":
                with JIRA_MONITOR.lock:
                    return json_response(self, {
                        "running": JIRA_MONITOR.running,
                        "enabled": JIRA_MONITOR.enabled,
                        "interval_sec": JIRA_MONITOR.interval_sec,
                        "last_check": JIRA_MONITOR.last_check,
                        "next_check": JIRA_MONITOR.next_check,
                    })
            if parsed.path == "/api/gap-tracking/inspection":
                return json_response(self, {**get_last_inspection(), "monitor": {
                    "running": JIRA_MONITOR.running,
                    "enabled": JIRA_MONITOR.enabled,
                    "last_check": JIRA_MONITOR.last_check,
                    "next_check": JIRA_MONITOR.next_check,
                }})
            return json_response(self, {"error": "Not found"}, status=404)
        except Exception as exc:
            return json_response(self, {"error": str(exc), "trace": traceback.format_exc()}, status=500)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if not length:
            return {}
        raw = self.rfile.read(length).decode("utf-8", errors="replace")
        return json.loads(raw or "{}")

    def serve_static(self, rel: str, content_type: str) -> None:
        target = safe_rel_path(STATIC_DIR, rel)
        if not target.exists() or not target.is_file():
            return json_response(self, {"error": "Static asset not found"}, status=404)
        raw = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


def get_jira_tickets() -> dict:
    try:
        sys.path.insert(0, str(APP_ROOT / "jira_scripts"))
        from jira_integration import create_jira_integration
        cfg = load_config()
        jira = create_jira_integration(cfg)
        
        # Get CEADU Layer3 related tickets
        layer3_tickets = jira.get_cea_layer3_tickets()
        
        # If no filtered results, show all tickets
        if not layer3_tickets:
            tickets = jira.get_my_tickets()
        else:
            tickets = layer3_tickets
        
        return {"tickets": [{
            "key": t.get("key"),
            "summary": t.get("fields", {}).get("summary", ""),
            "status": t.get("fields", {}).get("status", {}).get("name", ""),
            "priority": t.get("fields", {}).get("priority", {}).get("name", ""),
            "project": t.get("fields", {}).get("project", {}).get("key", ""),
            "category": t.get("_category", "other"),
            "display_title": t.get("_display_title", t.get("key", ""))
        } for t in tickets], "source": "cache"}
    except Exception as e:
        return {"tickets": [], "error": str(e)}


def refresh_jira_tickets() -> dict:
    """Trigger opencode skill to fetch fresh Jira tickets"""
    try:
        skill_script = Path(__file__).parent.parent / ".config" / "opencode" / "skills" / "Jira_access_enhanced" / "scripts" / "my_tickets.py"
        if skill_script.exists():
            result = subprocess.run(
                [sys.executable, str(skill_script)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=60,
                cwd=str(skill_script.parent)
            )
            if result.returncode == 0:
                return {"status": "refreshed", "message": "Jira tickets refreshed via skill"}
        return {"status": "failed", "message": "Could not refresh - use opencode command directly"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def search_jira_tickets(jql: str) -> dict:
    try:
        sys.path.insert(0, str(APP_ROOT / "jira_scripts"))
        from jira_integration import create_jira_integration
        cfg = load_config()
        jira = create_jira_integration(cfg)
        result = jira.search_tickets(jql)
        return {"result": result}
    except Exception as e:
        return {"result": str(e), "error": str(e)}


def get_jira_issue(key: str) -> dict:
    try:
        sys.path.insert(0, str(APP_ROOT / "jira_scripts"))
        from jira_integration import create_jira_integration
        cfg = load_config()
        jira = create_jira_integration(cfg)
        issue = jira.get_issue(key, include_attachments=True)
        return {"issue": issue} if issue else {"issue": None, "error": "Not found"}
    except Exception as e:
        return {"issue": None, "error": str(e)}


def verify_jira_ticket_status(key: str) -> dict:
    """Verify and return current Jira ticket status"""
    try:
        sys.path.insert(0, str(APP_ROOT / "jira_scripts"))
        from jira_integration import create_jira_integration
        cfg = load_config()
        jira = create_jira_integration(cfg)
        issue = jira.get_issue(key)
        if issue:
            fields = issue.get("fields", {})
            return {
                "key": key,
                "status": fields.get("status", {}).get("name", "Unknown"),
                "priority": fields.get("priority", {}).get("name", "None"),
                "assignee": fields.get("assignee", {}).get("displayName", "Unassigned"),
                "updated": fields.get("updated", ""),
                "comment_count": len(fields.get("comment", {}).get("comments", [])),
                "labels": fields.get("labels", []),
                "resolution": fields.get("resolution", {}).get("name", "Unresolved"),
            }
        return {"error": f"Ticket {key} not found"}
    except Exception as e:
        return {"error": str(e)}


def get_export_markets_data() -> dict:
    """Get export markets layer 3 comparison data from Jira tickets"""
    try:
        sys.path.insert(0, str(APP_ROOT / "jira_scripts"))
        from jira_integration import create_jira_integration
        cfg = load_config()
        jira = create_jira_integration(cfg)
        
        market_mapping = {
            "Korea": ["CEADU-682", "CEADU-2631"],
            "ASEAN RHD": ["CEADU-2739", "CEADU-5602"],
            "ASEAN LHD": ["CEADU-3005"],
            "India": ["CEADU-3784", "CEADU-3974", "CEADU-3978"],
            "Middle East": ["CEADU-4514", "CEADU-5751", "CEADU-5081", "CEADU-5085"],
            "Kazakhstan": ["CEADU-4494", "CEADU-4870", "CEADU-4864", "CEADU-4868"],
            "Uzbekistan": ["CEADU-5282", "CEADU-6508", "CEADU-6502", "CEADU-6509"],
            "Turkey": ["CEADU-6364", "CEADU-6705", "CEADU-6699", "CEADU-6706"],
            "AUS/NZL CMP21": ["CEADU-2711", "CEADU-5601", "CEADU-3128", "CEADU-3132"],
            "AUS/NZL CSP31": ["CEADU-6746", "CEADU-6757", "CEADU-6749"],
        }
        
        market_status_mapping = {
            "CEADU-682": {"domain": "Cyber Sec", "status": "Baseload"},
            "CEADU-2631": {"domain": "Data Sec", "status": "In Progress"},
            "CEADU-2739": {"domain": "Cyber Sec", "status": "Baseload"},
            "CEADU-5602": {"domain": "Data Sec", "status": "In Progress"},
            "CEADU-3005": {"domain": "Cyber Sec", "status": "N/A"},
            "CEADU-3784": {"domain": "Cyber Sec", "status": "In Progress"},
            "CEADU-4514": {"domain": "Cyber Sec", "status": "N/A"},
            "CEADU-5751": {"domain": "Data Sec", "status": "In Progress"},
            "CEADU-5081": {"domain": "OBD", "status": "Required"},
            "CEADU-4494": {"domain": "Cyber Sec", "status": "N/A"},
            "CEADU-4870": {"domain": "Data Sec", "status": "In Progress"},
            "CEADU-4864": {"domain": "OBD", "status": "Completed"},
            "CEADU-5282": {"domain": "All", "status": "In Progress"},
            "CEADU-6508": {"domain": "Data Sec", "status": "In Progress"},
            "CEADU-6502": {"domain": "OTA", "status": "Completed"},
            "CEADU-6509": {"domain": "Cyber Sec", "status": "In Progress"},
            "CEADU-6364": {"domain": "Cyber Sec", "status": "Completed"},
            "CEADU-6705": {"domain": "Data Sec", "status": "In Progress"},
            "CEADU-6699": {"domain": "OTA", "status": "In Progress"},
            "CEADU-6706": {"domain": "Cyber Sec", "status": "Completed"},
            "CEADU-2711": {"domain": "Cyber Sec", "status": "N/A"},
            "CEADU-5601": {"domain": "Data Sec", "status": "In Progress"},
            "CEADU-3128": {"domain": "OBD", "status": "Completed"},
            "CEADU-3132": {"domain": "User Consent", "status": "In Progress"},
            "CEADU-6746": {"domain": "All", "status": "In Progress"},
            "CEADU-6757": {"domain": "Data Sec", "status": "In Progress"},
            "CEADU-6749": {"domain": "Layer 3", "status": "In Progress"},
        }
        
        markets = []
        for market_name, ticket_keys in market_mapping.items():
            market_tickets = []
            for key in ticket_keys:
                issue = jira.get_issue_with_comments(key)
                if issue:
                    fields = issue.get("fields", {})
                    status_info = market_status_mapping.get(key, {"domain": "Unknown", "status": "Unknown"})
                    comments = issue.get("_comments", [])
                    
                    # Extract key comment summaries
                    recent_comments = []
                    for c in comments[-5:]:  # Last 5 comments
                        body = c.get("body", "")
                        author = c.get("author", {}).get("displayName", "Unknown")
                        created = c.get("created", "")[:10]
                        # Clean and truncate body
                        clean_body = re.sub(r'\[~[^\]]+\]|\[https?://[^\]]+\]|\{[^}]+\}', '', body)
                        clean_body = re.sub(r'\s+', ' ', clean_body).strip()[:200]
                        if clean_body:
                            recent_comments.append({
                                "author": author,
                                "date": created,
                                "summary": clean_body
                            })
                    
                    market_tickets.append({
                        "key": key,
                        "summary": fields.get("summary", ""),
                        "status": fields.get("status", {}).get("name", ""),
                        "domain": status_info.get("domain", ""),
                        "layer3_status": status_info.get("status", ""),
                        "priority": fields.get("priority", {}).get("name", ""),
                        "assignee": fields.get("assignee", {}).get("displayName", ""),
                        "updated": fields.get("updated", "")[:10],
                        "comment_count": len(comments),
                        "recent_comments": recent_comments,
                    })
                else:
                    market_tickets.append({
                        "key": key,
                        "summary": "Ticket not found",
                        "status": "Not Found",
                        "domain": market_status_mapping.get(key, {}).get("domain", ""),
                        "layer3_status": market_status_mapping.get(key, {}).get("status", ""),
                    })
            markets.append({
                "name": market_name,
                "tickets": market_tickets,
                "ticket_count": len(market_tickets),
                "completed_count": sum(1 for t in market_tickets if t["status"] == "Closed"),
                "in_progress_count": sum(1 for t in market_tickets if t["status"] in ["Open", "In Progress", "IN EVALUATION"]),
            })
        
        return {"markets": markets, "total_markets": len(markets)}
    except Exception as e:
        return {"markets": [], "error": str(e)}


def generate_export_markets_report() -> dict:
    """Generate export markets layer 3 comparison report"""
    try:
        data = get_export_markets_data()
        if "error" in data:
            return {"error": data["error"]}
        
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        report_lines = [
            f"# 出口市场 Layer3 法规合规对比报告",
            f"",
            f"**生成时间**: {timestamp}",
            f"**数据来源**: Jira DevStack",
            f"",
            f"## 市场概览",
            f"",
            f"| 市场 | 工单数 | 已完成 | 进行中 |",
            f"|------|--------|--------|--------|",
        ]
        
        for market in data["markets"]:
            report_lines.append(f"| {market['name']} | {market['ticket_count']} | {market['completed_count']} | {market['in_progress_count']} |")
        
        report_lines.extend([
            f"",
            f"## 详细工单状态",
            f"",
        ])
        
        for market in data["markets"]:
            report_lines.append(f"### {market['name']}")
            report_lines.append(f"| Jira工单 | 领域 | Layer3状态 | Jira状态 | 负责人 |")
            report_lines.append(f"|----------|------|-----------|----------|--------|")
            for ticket in market["tickets"]:
                report_lines.append(f"| {ticket['key']} | {ticket['domain']} | {ticket['layer3_status']} | {ticket['status']} | {ticket['assignee']} |")
            report_lines.append("")
        
        report_lines.extend([
            f"",
            f"## 关键结论",
            f"",
            f"1. **Cyber Security**: 大多数市场受益于 Baseload 方案，0 MM 工作量",
            f"2. **Data Security**: 大多数市场需要 UX/Layer 7 适配，技术实现已被中国标准覆盖",
            f"3. **OBD 需求**: 仅 KZ 和 UAE 有 OBD 适配需求 - 共计约 22.5 MM",
            f"4. **India 特殊**: RxSWIN 为可选 - 需决策：实现(+2MM)或提供文档",
            f"5. **时间线**: Uzbekistan 截止 29/07, Turkey 截止 12/08",
        ])
        
        report_content = "\n".join(report_lines)
        report_path = REPORTS_DIR / f"export_markets_layer3_{time.strftime('%Y%m%d_%H%M%S')}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report_content, encoding="utf-8")
        
        return {"success": True, "report_path": str(report_path), "content": report_content}
    except Exception as e:
        return {"error": str(e)}


def _status_badge(status: str) -> str:
    """Generate HTML badge for a compliance status."""
    status_lower = status.lower().replace(" ", "").replace("_", "")
    badges = {
        "baseload": ("#d4edda", "#155724"),
        "inprogress": ("#fff3cd", "#856404"),
        "completed": ("#cce5ff", "#004085"),
        "covered": ("#d1ecf1", "#0c5460"),
        "required": ("#e7a3a3", "#721c24"),
        "partial": ("#ffeaa7", "#6c5400"),
        "na": ("#e2e3e5", "#383d41"),
        "closed": ("#d4edda", "#155724"),
    }
    for key, (bg, fg) in badges.items():
        if key in status_lower:
            return f'<span style="padding:3px 8px;border-radius:4px;font-size:11px;background:{bg};color:{fg};">{status}</span>'
    return f'<span style="padding:3px 8px;border-radius:4px;font-size:11px;background:#eee;color:#333;">{status}</span>'


def _item_badge(category: str) -> str:
    """Generate badge icon for critical/action/closed."""
    icons = {"CRITICAL": ("🚨", "#ffebee", "#c62828"),
             "ACTION": ("📌", "#fff3e0", "#e65100"),
             "RECENTLYCLOSED": ("✅", "#e8f5e9", "#2e7d32")}
    icon, bg, color = icons.get(category.upper(), ("📋", "#f5f5f5", "#333"))
    return f'<span style="background:{bg};color:{color};padding:6px 12px;border-radius:20px;font-size:12px;">{icon} <b>{category.replace("_", " ").title()}</b></span>'


def generate_monthly_report_html(recipients_to: list[str] = None, recipients_cc: list[str] = None) -> dict:
    """Read Excel and generate monthly report HTML email body."""
    try:
        import openpyxl
        wb = openpyxl.load_workbook(str(LAYER3_EXCEL_PATH), read_only=True, data_only=True)

        ws_overview = wb["Layer 3 Comparison"]
        market_rows = []
        for i, row in enumerate(ws_overview.iter_rows(values_only=True), 1):
            if 6 <= i <= 15 and row[0]:
                market_rows.append({
                    "market": str(row[0]),
                    "ticket": str(row[1]) if row[1] else "",
                    "countries": str(row[2]) if row[2] else "",
                    "platform": str(row[3]) if row[3] else "",
                    "vehicle": str(row[4]) if row[4] else "",
                    "sop": str(row[5]) if row[5] else "",
                    "cyber": str(row[6]) if row[6] else "N/A",
                    "data": str(row[7]) if row[7] else "N/A",
                    "ota": str(row[8]) if row[8] else "N/A",
                    "obd": str(row[9]) if row[9] else "N/A",
                    "fusa": str(row[10]) if row[10] else "N/A",
                })

        ws_details = wb["In Progress Details"]
        critical_items = []
        action_items = []
        closed_items = []
        current_section = None
        for i, row in enumerate(ws_details.iter_rows(values_only=True), 1):
            if i <= 5:
                continue
            val = row[0] if row else None
            val_str = str(val).strip() if val else ""
            if val_str.startswith("CRITICAL"):
                current_section = "CRITICAL"
                continue
            if val_str.startswith("ACTION"):
                current_section = "ACTION"
                continue
            if val_str.startswith("RECENTLY CLOSED"):
                current_section = "RECENTLYCLOSED"
                continue
            if val_str and val_str[0].isdigit():
                section_map = {"CRITICAL": critical_items, "ACTION": action_items, "RECENTLYCLOSED": closed_items}
                items = section_map.get(current_section, [])
                items.append({
                    "num": val_str,
                    "market": str(row[1]) if row[1] else "",
                    "ticket": str(row[2]) if row[2] else "",
                    "domain": str(row[4]) if row[4] else "",
                    "status": str(row[5]) if row[5] else "",
                    "deadline": str(row[6]) if row[6] else "TBD",
                    "summary": str(row[8]) if row[8] else "",
                    "owner": str(row[9]) if row[9] else "",
                    "closed": str(row[11]) if len(row) > 11 and row[11] else "",
                })

        critical_count = len(critical_items)
        action_count = len(action_items)
        closed_count = len(closed_items)
        market_count = len(market_rows)

        html = """<html><body style="font-family: 'The Group TEXT'; font-size: 12pt; color: #333;">
<p>Hi team,</p>
<p>Please find the Export Markets Regulatory Compliance Monthly Report, covering Cyber Security, Data Security, OTA, OBD, and FuSa domains across 10 target markets.</p>
<p>Please kindly note the following items that require attention, and kindly close the related JIRA tickets upon In Progress:</p>
<div style="margin: 15px 0;">
  <div style="display: flex; gap: 10px; margin-bottom: 20px;">
    <span style="background: #ffebee; color: #c62828; padding: 6px 12px; border-radius: 20px; font-size: 12px;">🚨 <b>{critical}</b> Critical</span>
    <span style="background: #fff3e0; color: #e65100; padding: 6px 12px; border-radius: 20px; font-size: 12px;">📌 <b>{action}</b> Action</span>
    <span style="background: #e8f5e9; color: #2e7d32; padding: 6px 12px; border-radius: 20px; font-size: 12px;">✅ <b>{closed}</b> Closed</span>
    <span style="background: #e3f2fd; color: #1565c0; padding: 6px 12px; border-radius: 20px; font-size: 12px;">🌍 <b>{markets}</b> Markets</span>
  </div>
</div>""".format(
            critical=critical_count, action=action_count, closed=closed_count, markets=market_count)

        html += """
<div style="margin: 20px 0;">
  <h2 style="font-family: 'The Group TEXT'; font-size: 14pt; color: #1a5276; margin-bottom: 15px;">🌍 Market Overview</h2>
  <table style="width: 100%; border-collapse: collapse; font-size: 12px; font-family: 'The Group TEXT';">
    <tr>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">Market</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">Ticket</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">Target Countries</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">Platform</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">Vehicle Type</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">SOP Target</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">Cyber Sec</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">Data Sec</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">OTA</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">OBD</th>
      <th style="background: #34495e; color: white; padding: 12px 8px; text-align: left;">FuSa</th>
    </tr>"""

        for idx, m in enumerate(market_rows):
            bg = "#f8f9fa" if idx % 2 == 1 else "white"
            html += f"""<tr style="background: {bg};">
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;"><strong>{m['market']}</strong></td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{m['ticket']}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{m['countries']}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{m['platform']}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{m['vehicle']}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{m['sop']}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{_status_badge(m['cyber'])}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{_status_badge(m['data'])}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{_status_badge(m['ota'])}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{_status_badge(m['obd'])}</td>
      <td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{_status_badge(m['fusa'])}</td>
    </tr>"""

        html += """  </table>
  <div style="margin-top: 15px; font-size: 11px; color: #666;">
    <span style="padding: 3px 8px; background: #fff3cd; color: #856404; border-radius: 4px; margin-right: 8px;">In Progress</span>= Work ongoing<br>
    <span style="padding: 3px 8px; background: #d4edda; color: #155724; border-radius: 4px; margin-right: 8px;">Baseload</span>= Compliance achieved | <span style="padding: 3px 8px; background: #cce5ff; color: #004085; border-radius: 4px; margin-right: 8px;">Completed</span>= Assessment done | <span style="padding: 3px 8px; background: #d1ecf1; color: #0c5460; border-radius: 4px; margin-right: 8px;">Covered</span>= Covered | <span style="padding: 3px 8px; background: #e7a3a3; color: #721c24; border-radius: 4px; margin-right: 8px;">Required</span>= Certification needed | <span style="padding: 3px 8px; background: #e2e3e5; color: #383d41; border-radius: 4px; margin-right: 8px;">N/A</span>= Not applicable
  </div>
</div>"""

        if critical_items:
            html += '<h2 style="font-family: \'The Group TEXT\'; font-size: 14pt; color: #1a5276; margin: 25px 0 15px;">🚨 Critical Items</h2>'
            for item in critical_items:
                html += f"""<div style="background: #fff5f5; border-left: 4px solid #dc3545; padding: 12px 15px; margin-bottom: 10px;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
    <strong style="color: #1a5276;">{item['market']}</strong>
    <span style="font-size: 11px; color: #666; background: #eee; padding: 2px 8px; border-radius: 3px;">{item['ticket']}</span>
  </div>
  <div style="font-size: 12px; color: #555; line-height: 1.5;">{item['domain']} - {item['summary']}</div>
  <div style="font-size: 11px; color: #888; margin-top: 5px;">Owner: {item['owner']} | Deadline: <strong style="color: #dc3545;">{item['deadline']}</strong></div>
</div>"""

        if action_items:
            html += '<h2 style="font-family: \'The Group TEXT\'; font-size: 14pt; color: #1a5276; margin: 25px 0 15px;">📌 Action Items</h2>'
            for item in action_items:
                html += f"""<div style="background: white; border: 1px solid #eee; border-left: 4px solid #ddd; padding: 12px 15px; margin-bottom: 10px; border-radius: 4px;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
    <strong style="color: #1a5276;">{item['market']}</strong>
    <span style="font-size: 11px; color: #666; background: #eee; padding: 2px 8px; border-radius: 3px;">{item['ticket']}</span>
  </div>
  <div style="font-size: 12px; color: #555; line-height: 1.5;">{item['domain']} - {item['summary']}</div>
  <div style="font-size: 11px; color: #888; margin-top: 5px;">Owner: {item['owner']} | Deadline: {item['deadline']}</div>
</div>"""

        if closed_items:
            html += '<h2 style="font-family: \'The Group TEXT\'; font-size: 14pt; color: #1a5276; margin: 25px 0 15px;">✅ Recently Closed</h2>'
            for item in closed_items:
                closed_info = f"Closed: {item['closed']}" if item['closed'] else ""
                html += f"""<div style="background: #f0fff4; border-left: 4px solid #27ae60; padding: 12px 15px; margin-bottom: 10px; border-radius: 4px;">
  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
    <strong style="color: #1a5276;">{item['market']}</strong>
    <span style="font-size: 11px; color: #666; background: #eee; padding: 2px 8px; border-radius: 3px;">{item['ticket']}</span>
  </div>
  <div style="font-size: 12px; color: #555; line-height: 1.5;">{item['domain']} - {item['summary']}</div>
  <div style="font-size: 11px; color: #888; margin-top: 5px;">Owner: {item['owner']} {closed_info}</div>
</div>"""

        html += """<hr style="border: none; border-top: 1px solid #ddd; margin: 25px 0;">
<p>Feel free to reach out if you have any questions.</p>
<p>Best,<br>Xie, Jingjing (CEA FuSa)</p>
</body></html>"""

        subject = f"Export Markets Regulatory Compliance Monthly Report - {time.strftime('%B %Y')}"
        return {
            "html": html,
            "subject": subject,
            "stats": {"critical": critical_count, "action": action_count, "closed": closed_count, "markets": market_count},
            "default_to": recipients_to or MONTHLY_REPORT_DEFAULT_TO,
            "default_cc": recipients_cc or MONTHLY_REPORT_DEFAULT_CC,
        }
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}


def send_monthly_report_draft(to: list[str] = None, cc: list[str] = None) -> dict:
    """Generate monthly report and create Outlook draft email."""
    try:
        report = generate_monthly_report_html(to or MONTHLY_REPORT_DEFAULT_TO, cc or MONTHLY_REPORT_DEFAULT_CC)
        if "error" in report:
            return {"ok": False, "error": report["error"]}

        import pythoncom
        import win32com.client

        pythoncom.CoInitialize()
        try:
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            mail.Subject = report["subject"]
            mail.To = "; ".join(report["default_to"])
            mail.CC = "; ".join(report["default_cc"])
            mail.HTMLBody = report["html"]
            mail.Display(False)
            return {"ok": True, "subject": report["subject"], "to": report["default_to"], "cc": report["default_cc"]}
        finally:
            pythoncom.CoUninitialize()
    except Exception as e:
        return {"ok": False, "error": str(e), "trace": traceback.format_exc()}


def download_pvs_from_jira(parent_key: str, filename: str = "") -> list:
    """Download PSV attachments from Jira - returns list of downloaded files"""
    import requests
    
    cfg = load_config()
    jira_url = cfg.get("jira", {}).get("url", "https://devstack.vgc.com.cn/jira")
    jira_token = cfg.get("jira", {}).get("token", "")
    
    headers = {"Authorization": f"Bearer {jira_token}"}
    
    RAW_DIR = APP_ROOT / "wiki" / "raw" / "pvs"
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    downloaded_files = []
    
    try:
        # Get attachment list
        resp = requests.get(
            f"{jira_url}/rest/api/2/issue/{parent_key}?fields=attachment",
            headers=headers,
            timeout=30
        )
        
        if resp.status_code != 200:
            print(f"[PVS] Failed to get issue {parent_key}: {resp.status_code}")
            return []
        
        attachments = resp.json().get('fields', {}).get('attachment', [])
        
        if not attachments:
            print(f"[PVS] No attachments in {parent_key}")
            return []
        
        # Find all PSV attachments
        psv_attachments = []
        for att in attachments:
            att_name = att.get('filename', '').lower()
            if ('psv' in att_name or 'pvs' in att_name) and att_name.endswith('.xlsx'):
                psv_attachments.append(att)
        
        # If specific filename provided, filter to that
        if filename:
            psv_attachments = [att for att in psv_attachments 
                             if filename.lower() in att.get('filename', '').lower()]
        
        if not psv_attachments:
            print(f"[PVS] No PSV attachments found in {parent_key}")
            # List available attachments for debugging
            att_names = [att.get('filename', '') for att in attachments]
            print(f"[PVS] Available attachments: {att_names}")
            return []
        
        print(f"[PVS] Found {len(psv_attachments)} PSV attachment(s) in {parent_key}")
        
        for target_att in psv_attachments:
            att_name = target_att.get('filename', '')
            download_url = target_att.get('content')
            
            if not download_url:
                print(f"[PVS] No content URL for {att_name}")
                continue
            
            print(f"[PVS] Downloading: {att_name}")
            
            dl_resp = requests.get(download_url, headers=headers, timeout=120, stream=True)
            
            if dl_resp.status_code == 200:
                content = dl_resp.content
                if len(content) > 10000:
                    local_file = RAW_DIR / f"{parent_key}_{att_name}"
                    local_file.write_bytes(content)
                    print(f"[PVS] Downloaded: {local_file.name} ({len(content)/1024:.1f} KB)")
                    downloaded_files.append(local_file)
                else:
                    print(f"[PVS] File too small: {len(content)} bytes")
        
        return downloaded_files
        
    except Exception as e:
        print(f"[PVS] Download error: {e}")
        return []


def get_pvs_from_wiki(parent_key: str, market: str) -> list:
    """从Wiki markdown文件读取已解析的Layer3法规"""
    WIKI_DIR = APP_ROOT / "wiki" / "queries"
    
    market_key = market.replace("/", "_").replace(" ", "_").lower()
    wiki_file = WIKI_DIR / f"pvs_market_{market_key}.md"
    
    if not wiki_file.exists():
        return []
    
    try:
        content = wiki_file.read_text(encoding="utf-8")
        results = []
        current_layer3 = ""
        
        for line in content.split("\n"):
            if line.startswith("### "):
                parts = line.split(" (")
                if len(parts) >= 1:
                    current_layer3 = parts[0].replace("### ", "").strip()
            elif line.startswith("**Document-ID:"):
                doc_id = line.replace("**Document-ID:", "").strip().rstrip("**")
            elif line.startswith("**Regulation:"):
                doc_name = line.replace("**Regulation:", "").strip().rstrip("**")
            elif line.startswith("- "):
                if "mandatory" in line.lower():
                    mandatory = line.split(":", 1)[1].strip() if ":" in line else ""
                    results.append({
                        "documentId": doc_id if 'doc_id' in locals() else "",
                        "documentName": doc_name if 'doc_name' in locals() else "",
                        "mandatory": mandatory,
                        "topic": "",
                        "layer3": current_layer3,
                        "matchKeyword": current_layer3.split(",")[0].strip() if current_layer3 else "",
                        "status": "Required"
                    })
        
        return results
    except Exception as e:
        print(f"[Wiki] Read error: {e}")
        return []


def parse_pvs_excel(parent_key: str, filename: str) -> dict:
    """Parse PVS: check wiki first -> download -> save to wiki -> parse"""
    
    print(f"[PVS] Parsing: {parent_key} / {filename}")
    
    # 目录配置
    WIKI_DIR = APP_ROOT / "wiki" / "queries"
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    
    # 市场映射
    market_mapping = {
        "CEADU-682": "Korea",
        "CEADU-2631": "Korea",
        "CEADU-2739": "ASEAN RHD",
        "CEADU-3005": "ASEAN LHD",
        "CEADU-3784": "India",
        "CEADU-4514": "Middle East",
        "CEADU-4494": "Kazakhstan",
        "CEADU-5282": "Uzbekistan",
        "CEADU-6364": "Turkey",
        "CEADU-2711": "AUS/NZL",
        "CEADU-6294": "AUS/NZL",
        "CEADU-6746": "AUS/NZL",
    }
    
    target_market = market_mapping.get(parent_key, "Unknown")
    
    # Step 1: 强制重新解析 - 删除旧Wiki
    WIKI_DIR = APP_ROOT / "wiki" / "queries"
    market_key = target_market.replace("/", "_").replace(" ", "_").lower()
    wiki_file = WIKI_DIR / f"pvs_market_{market_key}.md"
    if wiki_file.exists():
        wiki_file.unlink()
        print(f"[PVS] Deleted old wiki: {wiki_file.name}")
    
    # Step 2: 优先从Jira下载最新的PSV文件
    print(f"[PVS] Checking Jira for PSV attachments...")
    downloaded_files = download_pvs_from_jira(parent_key, filename)
    
    local_file = None
    
    if downloaded_files:
        # 选择最新版本的文件（文件名含 Vx.0 版本号，取最高；否则用最后一个）
        import re
        def version_key(f):
            matches = re.findall(r'V(\d+)\.0', f.name, re.IGNORECASE)
            return int(matches[-1]) if matches else -1
        local_file = max(downloaded_files, key=version_key)
        print(f"[PVS] Using latest file: {local_file.name}")
    else:
        # 如果下载失败，查找本地PSV文件
        print(f"[PVS] No download, looking for local PSV...")
        RAW_DIR = APP_ROOT / "wiki" / "raw" / "pvs"
        import re
        def version_key(f):
            matches = re.findall(r'V(\d+)\.0', f.name, re.IGNORECASE)
            return int(matches[-1]) if matches else -1

        # 优先查找包含parent_key的PSV文件（选最高版本）
        parent_matches = [f for f in RAW_DIR.glob("*PSV*.xlsx") if parent_key in f.name]
        if parent_matches:
            local_file = max(parent_matches, key=version_key)
            print(f"[PVS] Found file with parent_key (latest version): {local_file.name}")

        # 如果没找到，使用包含市场名的文件（选最高版本）
        if not local_file:
            market_key = target_market.replace(" ", "_")
            market_matches = [f for f in RAW_DIR.glob("*PSV*.xlsx") if market_key.lower() in f.name.lower()]
            if market_matches:
                local_file = max(market_matches, key=version_key)
                print(f"[PVS] Found file with market (latest version): {local_file.name}")
    
    if not local_file:
        results = get_pvs_results_for_parent(parent_key)
        return {"results": results, "source": "fallback", "market": target_market}
    
    try:
        import openpyxl
    except ImportError:
        return {"error": "需要安装 openpyxl", "results": []}
    
    # Parse Excel - 提取 Document-ID, Regulation document name, mandatory/if fitted
    results = []
    regulations = []
    
    try:
        wb = openpyxl.load_workbook(local_file, data_only=True)
        
        # 优先处理 "Regulations Focus list" sheet
        focus_sheet = None
        for sheet_name in wb.sheetnames:
            if "regulation" in sheet_name.lower() and "focus" in sheet_name.lower():
                focus_sheet = wb[sheet_name]
                print(f"[PVS] Using sheet: {sheet_name}")
                break
        
        if not focus_sheet:
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                for row_idx, row in enumerate(sheet.iter_rows(min_row=1, max_row=5, values_only=True), 1):
                    row_text = " ".join(str(c).lower() for c in row if c)
                    if "document-id" in row_text or "regulation document name" in row_text:
                        focus_sheet = wb[sheet_name]
                        print(f"[PVS] Using sheet: {sheet_name}")
                        break
                if focus_sheet:
                    break
        
        # 解析所有相关sheet
        sheets_to_parse = []
        for sheet_name in wb.sheetnames:
            name_lower = sheet_name.lower()
            if ("regulation" in name_lower and "focus" in name_lower) or "non homologation" in name_lower:
                sheets_to_parse.append((sheet_name, wb[sheet_name]))
                print(f"[PVS] Will parse sheet: {sheet_name}")
        
        # 检测捷克格式 PSV（如 India CEADU-3784）：无标准 Regulation Focus list sheet
        # 特征: 存在 SZP/CLUSTER_Themengebiet 等 sheet, 表头含 "English theme"
        czech_format = False
        if not sheets_to_parse:
            for sheet_name in wb.sheetnames:
                if "souhrn" in sheet_name.lower() or "szp" in sheet_name.lower():
                    czech_format = True
                    break
            if not czech_format:
                for sheet_name in wb.sheetnames:
                    sheet = wb[sheet_name]
                    try:
                        for row_idx, row in enumerate(sheet.iter_rows(min_row=1, max_row=3, values_only=True), 1):
                            row_text = " ".join(str(c).lower() for c in row if c)
                            if "english theme" in row_text and "themengebiet" in row_text:
                                czech_format = True
                                break
                    except Exception:
                        pass
                    if czech_format:
                        break
        
        if czech_format:
            print(f"[PVS] Detected Czech-format PSV (India style)")
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                try:
                    row_text = " ".join(str(c).lower() for c in next(sheet.iter_rows(min_row=2, max_row=2, values_only=True)) if c)
                except Exception:
                    continue
                if "english theme" in row_text:
                    sheets_to_parse.append((sheet_name, sheet))
                    print(f"[PVS] Will parse Czech sheet: {sheet_name}")
        
        # Layer3关键词 - 仅匹配Topic列
        LAYER3_KEYWORDS = {
            "Cyber Security": ["cyber security", "cybersecurity", "un-r 155", "un-r155"],
            "Data Security": ["data security", "data privacy", "privacy", "personal data", "gdpr", "data protect"],
            "OTA": ["ota", "over-the-air", "software update", "sums", "un-r 156", "un-r156"],
            "OBD": ["obd", "on-board diagnostic", "on board diagnostic"],
            "Functional Safety": ["functional safety", "iso 26262", "asil", "fusa"],
            "Immobilizer-theft": ["immobilizer", "immobiliser", "theft alarm", "vehicle alarm"],
        }
        
        for sheet_name, sheet in sheets_to_parse:
            if czech_format:
                # 捷克格式列: Topic=0(English theme), DocID=2(Regularie), DocName=4(Titel), Mandatory=11(Alle Fahrzeuge date)
                topic_col = 0
                doc_id_col = 2
                doc_name_col = 4
                mandatory_col = 11
                start_row = 3  # R1是标题行, R2才是表头, R3起是数据
            else:
                # 固定列索引: Topic=2, DocName=4, DocID=5, Mandatory=6
                topic_col = 2
                doc_name_col = 4
                doc_id_col = 5
                mandatory_col = 6
                start_row = 2  # Header 在第1行，数据从第2行开始
            
            for row in sheet.iter_rows(min_row=start_row, values_only=True):
                if not any(row):
                    continue
                
                # 仅匹配 Topic 列
                topic_text = str(row[topic_col]).lower() if row[topic_col] else ""
                if len(topic_text) < 3:
                    continue
                
                # 匹配 Layer3 关键词 - 仅在 Topic 列
                matched_layer3 = []
                for layer3, keywords in LAYER3_KEYWORDS.items():
                    if any(kw in topic_text for kw in keywords):
                        matched_layer3.append(layer3)
                
                if matched_layer3:
                    doc_id = str(row[doc_id_col]) if doc_id_col is not None else ""
                    doc_name = str(row[doc_name_col]) if doc_name_col is not None else ""
                    if czech_format:
                        mandatory = "mandatory" if (len(row) > 11 and row[11]) else "if fitted"
                    else:
                        mandatory = str(row[mandatory_col]) if mandatory_col is not None else ""
                    
                    if doc_id or doc_name:
                        reg_info = {
                            "documentId": doc_id[:100],
                            "documentName": doc_name[:200],
                            "mandatory": mandatory[:50],
                            "topic": topic_text[:100],
                            "layer3": ", ".join(matched_layer3),
                            "matchKeyword": matched_layer3[0],
                            "status": "Required"
                        }
                        results.append(reg_info)
                        regulations.append(reg_info)
        
        wb.close()
        print(f"[PVS] Found {len(results)} Layer3 regulations")
        
    except Exception as e:
        print(f"[PVS] Parse error: {e}")
        results = get_pvs_results_for_parent(parent_key)
        return {"results": results, "filename": filename, "parent": parent_key, "source": "fallback"}
    
    # Step 3: Update Wiki
    if regulations:
        update_pvs_wiki(parent_key, target_market, regulations)
    
    return {
        "results": results,
        "filename": filename,
        "parent": parent_key,
        "market": target_market,
        "source": "parsed" if regulations else "fallback",
        "file_path": str(local_file)
    }


def update_pvs_wiki(parent_key: str, market: str, regulations: list):
    """更新本地Wiki文件"""
    WIKI_DIR = APP_ROOT / "wiki" / "queries"
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    
    market_key = market.replace("/", "_").replace(" ", "_").lower()
    
    # 更新市场文件
    market_file = WIKI_DIR / f"pvs_market_{market_key}.md"
    
    lines = [
        f"# {market} - Layer3法规",
        "",
        f"**Parent工单**: {parent_key}",
        f"**法规数量**: {len(regulations)}",
        f"**更新时间**: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Layer3法规列表",
        "",
    ]
    
    # 按Layer3分组
    by_layer3 = {}
    for reg in regulations:
        layer3 = reg.get("layer3", "Other")
        if layer3 not in by_layer3:
            by_layer3[layer3] = []
        by_layer3[layer3].append(reg)
    
    for layer3, regs in by_layer3.items():
        lines.append(f"### {layer3} ({len(regs)}条)")
        lines.append("")
        for reg in regs:
            lines.append(f"**Document-ID:** {reg.get('documentId', '')}")
            lines.append(f"**Regulation:** {reg.get('documentName', '')}")
            lines.append(f"- Mandatory: {reg.get('mandatory', '')}")
            lines.append(f"- Topic: {reg.get('topic', '')}")
            lines.append("")
    
    market_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"[PVS] Wiki updated: {market_file.name}")
    
    # 更新汇总文件
    update_pvs_summary(regulations, parent_key, market)


def update_pvs_summary(new_regulations: list, parent_key: str, market: str):
    """更新汇总Wiki文件"""
    WIKI_DIR = APP_ROOT / "wiki" / "queries"
    summary_file = WIKI_DIR / "pvs_layer3_regulations_summary.md"
    
    existing_regs = []
    
    # 读取现有汇总
    if summary_file.exists():
        content = summary_file.read_text(encoding="utf-8")
        in_list = False
        for line in content.split("\n"):
            if line.strip() == "## 完整法规列表":
                in_list = True
                continue
            if in_list and line.strip().startswith("- "):
                existing_regs.append(line.strip())
    
    # 添加新法规
    for reg in new_regulations:
        layer3 = reg.get("layer3", "Layer3")
        doc_id = reg.get('documentId', reg.get('regulation', ''))
        doc_name = reg.get('documentName', reg.get('clause', ''))
        reg_str = f"- **{doc_id}** {doc_name[:50]} [{market}]"
        if reg_str not in existing_regs:
            existing_regs.append(reg_str)
    
    # 重新生成汇总
    layer3_count = {}
    for reg in new_regulations:
        layer3 = reg.get("layer3", "Other")
        layer3_count[layer3] = layer3_count.get(layer3, 0) + 1
    
    lines = [
        "# PVS Layer3 法规汇总",
        "",
        f"**更新时间**: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}",
        f"**总计**: {len(existing_regs)} 条法规",
        "",
        "## 统计",
        "",
    ]
    
    for layer3, count in sorted(layer3_count.items()):
        lines.append(f"- **{layer3}**: {count} 条")
    
    lines.extend(["", "---", "", "## 完整法规列表", ""])
    for reg_str in existing_regs:
        lines.append(reg_str)
    
    summary_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"[PVS] Summary updated: {len(existing_regs)} regulations")


def sync_pvs_wiki() -> dict:
    """Sync PVS attachments from Jira and update local Wiki"""
    import requests
    from datetime import datetime
    
    print("[WikiSync] Starting PVS Wiki sync...")
    
    # 配置
    JIRA_URL = "https://devstack.vgc.com.cn/jira"
    JIRA_TOKEN = "YOUR_JIRA_TOKEN"
    
    RAW_DIR = APP_ROOT / "wiki" / "raw" / "pvs"
    WIKI_DIR = APP_ROOT / "wiki" / "queries"
    
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    
    headers = {
        "Authorization": f"Bearer {JIRA_TOKEN}",
        "X-Atlassian-Token": "no-check"
    }
    
    # Parent工单
    tickets = ["CEADU-682", "CEADU-2739", "CEADU-3005", "CEADU-3784", "CEADU-4514", "CEADU-4494", "CEADU-5282", "CEADU-6364", "CEADU-2711"]
    
    downloaded = []
    
    for ticket_key in tickets:
        try:
            resp = requests.get(
                f"{JIRA_URL}/rest/api/2/issue/{ticket_key}?fields=attachment",
                headers=headers,
                timeout=30
            )
            if resp.status_code != 200:
                continue
            
            attachments = resp.json().get("fields", {}).get("attachment", [])
            
            for att in attachments:
                filename = att.get("filename", "")
                if filename.lower().endswith(('.xlsx', '.xls')):
                    # 下载
                    dl_resp = requests.get(
                        f"{JIRA_URL}/rest/api/2/issue/{ticket_key}/attachments/{filename}",
                        headers=headers,
                        timeout=60
                    )
                    if dl_resp.status_code == 200:
                        out_name = f"{ticket_key}_{filename}"
                        out_path = RAW_DIR / out_name
                        out_path.write_bytes(dl_resp.content)
                        downloaded.append((out_path, ticket_key))
                        print(f"[WikiSync] Downloaded: {out_name}")
        except Exception as e:
            print(f"[WikiSync] Error {ticket_key}: {e}")
    
    print(f"[WikiSync] Downloaded {len(downloaded)} files")
    
    return {
        "ok": True,
        "downloaded": len(downloaded),
        "raw_dir": str(RAW_DIR),
        "message": f"Downloaded {len(downloaded)} attachments. Run sync_pvs_wiki.py to parse."
    }


def get_pvs_results_for_parent(parent_key: str) -> list:
    """Get PVS results based on parent ticket - fallback data"""
    
    market_regulations = {
        "CEADU-682": [
            {"regulation": "UN-R 155", "clause": "4.2.1", "market": "Korea", "layer3": "Cyber Security", "matchKeyword": "CSMS", "status": "Required"},
            {"regulation": "UN-R 155", "clause": "4.3.2", "market": "Korea", "layer3": "Cyber Security", "matchKeyword": "Threat Analysis", "status": "Required"},
            {"regulation": "UN-R 156", "clause": "5.1.1", "market": "Korea", "layer3": "OTA", "matchKeyword": "SUMS", "status": "Required"},
        ],
        "CEADU-2631": [
            {"regulation": "PIPA", "clause": "23", "market": "Korea", "layer3": "Data Security", "matchKeyword": "Personal Data", "status": "Required"},
        ],
        "CEADU-2739": [
            {"regulation": "PDPA", "clause": "20", "market": "ASEAN RHD", "layer3": "Data Security", "matchKeyword": "Personal Data", "status": "Required"},
            {"regulation": "UN-R 155", "clause": "4.2", "market": "ASEAN RHD", "layer3": "Cyber Security", "matchKeyword": "CSMS", "status": "Required"},
        ],
        "CEADU-3005": [
            {"regulation": "PDPA Thailand", "clause": "22", "market": "ASEAN LHD", "layer3": "Data Security", "matchKeyword": "Personal Data", "status": "Required"},
        ],
        "CEADU-3784": [
            {"regulation": "AIS-189", "clause": "4.1.3", "market": "India", "layer3": "Cyber Security", "matchKeyword": "Type Approval", "status": "Required"},
            {"regulation": "AIS-138", "clause": "6.1", "market": "India", "layer3": "OBD", "matchKeyword": "Emissions", "status": "Required"},
        ],
        "CEADU-4514": [
            {"regulation": "UN-R 156", "clause": "5.1", "market": "Middle East", "layer3": "OTA", "matchKeyword": "SUMS", "status": "Required"},
            {"regulation": "UAE 513", "clause": "3.1", "market": "UAE", "layer3": "Data Security", "matchKeyword": "Privacy", "status": "Required"},
        ],
        "CEADU-4494": [
            {"regulation": "UN-R 83", "clause": "6.1", "market": "Kazakhstan", "layer3": "OBD", "matchKeyword": "Emissions", "status": "Required"},
        ],
        "CEADU-5282": [
            {"regulation": "UN-R 155", "clause": "4.2", "market": "Uzbekistan", "layer3": "Cyber Security", "matchKeyword": "CSMS", "status": "Required"},
            {"regulation": "UN-R 156", "clause": "5.1", "market": "Uzbekistan", "layer3": "OTA", "matchKeyword": "SUMS", "status": "Required"},
        ],
        "CEADU-6364": [
            {"regulation": "UN-R 155", "clause": "4.2", "market": "Turkey", "layer3": "Cyber Security", "matchKeyword": "CSMS", "status": "Completed"},
            {"regulation": "UN-R 156", "clause": "5.1", "market": "Turkey", "layer3": "OTA", "matchKeyword": "SUMS", "status": "In Progress"},
        ],
        "CEADU-2711": [
            {"regulation": "Privacy Act", "clause": "6C", "market": "AUS/NZL", "layer3": "Data Security", "matchKeyword": "Privacy", "status": "Required"},
        ],
    }
    
    if parent_key in market_regulations:
        return market_regulations[parent_key]
    
    return [
        {"regulation": "UN-R 155", "clause": "4.2", "market": "General", "layer3": "Cyber Security", "matchKeyword": "CSMS", "status": "Required"},
        {"regulation": "UN-R 156", "clause": "5.1", "market": "General", "layer3": "OTA", "matchKeyword": "SUMS", "status": "Required"},
    ]


def get_mock_pvs_results() -> list:
    """Return mock PVS results when file cannot be downloaded"""
    return [
        {"regulation": "UN-R 155", "clause": "4.2", "market": "Korea", "layer3": "Cyber Security", "matchKeyword": "CSMS", "status": "Required"},
        {"regulation": "UN-R 156", "clause": "5.1", "market": "Korea", "layer3": "OTA", "matchKeyword": "SUMS", "status": "Required"},
        {"regulation": "AIS-189", "clause": "4.1", "market": "India", "layer3": "Cyber Security", "matchKeyword": "Cyber", "status": "Required"},
        {"regulation": "PDPA", "clause": "20", "market": "ASEAN RHD", "layer3": "Data Security", "matchKeyword": "Personal Data", "status": "Required"},
        {"regulation": "UN-R 83", "clause": "6.1", "market": "Kazakhstan", "layer3": "OBD", "matchKeyword": "Emissions", "status": "Required"},
    ]


def _get_parent_summary(parent_key: str) -> str:
    """Get Jira ticket summary for the parent ticket, containing market and platform info."""
    import requests
    cfg = load_config()
    jira_cfg = cfg.get("jira", {})
    url = jira_cfg.get("url", "https://devstack.vgc.com.cn/jira")
    token = jira_cfg.get("token", "")
    try:
        session = requests.Session()
        session.get(f"{url}/login.jsp", timeout=15, proxies={"http": None, "https": None})
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        resp = session.get(
            f"{url}/rest/api/2/issue/{parent_key}",
            params={"fields": "summary"},
            headers=headers, timeout=30, proxies={"http": None, "https": None}
        )
        if resp.status_code == 200:
            return resp.json().get("fields", {}).get("summary", "")
    except Exception:
        pass
    return ""


def _get_subtask_mapping(parent_key: str) -> dict[str, str]:
    """Fetch sub-task keys from Jira for a given parent ticket.
    Returns a dict mapping topic keyword -> sub-task Jira key.
    Cyber Security and Data Security have separate sub-task tickets."""
    import requests, os
    cfg = load_config()
    jira_cfg = cfg.get("jira", {})
    url = jira_cfg.get("url", "https://devstack.vgc.com.cn/jira")
    token = jira_cfg.get("token", "")
    try:
        session = requests.Session()
        session.get(f"{url}/login.jsp", timeout=15, proxies={"http": None, "https": None})
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        jql = f'parent={parent_key} ORDER BY created ASC'
        resp = session.get(
            f"{url}/rest/api/2/search",
            params={"jql": jql, "fields": "summary,key", "maxResults": 100},
            headers=headers, timeout=30, proxies={"http": None, "https": None}
        )
        if resp.status_code != 200:
            return {}
        mapping = {}
        for item in resp.json().get("issues", []):
            key = item.get("key", "")
            summary = item.get("fields", {}).get("summary", "").lower()
            for topic in ["cyber security", "data security"]:
                if topic in summary:
                    mapping[topic] = key
        return mapping
    except Exception:
        return {}


def send_assessment_email(data: dict) -> dict:
    """Send assessment request email to selected contacts"""
    try:
        task_key = data.get("taskKey", "")
        parent_key = data.get("parentKey", "")
        regulations = data.get("regulations", [])
        recipients = data.get("recipients", [])
        
        if not regulations:
            return {"ok": False, "error": "No regulations selected"}
        
        if not recipients:
            return {"ok": False, "error": "Please select at least one recipient"}
        
        # Load contact details
        contacts_data = load_contacts()
        contact_map = {c["id"]: c for c in contacts_data.get("contacts", [])}
        
        # Generate HTML email content
        JIRA_BASE = "https://devstack.vgc.com.cn/jira/browse"

        def ticket_link(key):
            return f'<a href="{JIRA_BASE}/{key}" style="color:#0066CC;text-decoration:none;font-weight:600;">{key}</a>'

        content_lines = [
            "<html><body style='font-family:Arial,sans-serif;font-size:14px;color:#333;'>",
            "<h2 style='color:#1a5276;border-bottom:2px solid #2980b9;padding-bottom:8px;'>Layer3 Regulation Assessment Request</h2>",
            "",
        ]

        # Resolve sub-task mapping (Cyber Security / Data Security have separate sub-task tickets)
        subtask_map = _get_subtask_mapping(parent_key) if parent_key else {}

        # Build market/platform suffix from parent ticket summary
        parent_suffix = ""
        if parent_key:
            parent_summary = _get_parent_summary(parent_key)
            if parent_summary:
                parts = []
                if "[" in parent_summary:
                    inner = parent_summary[parent_summary.index("[")+1:parent_summary.index("]")]
                    for token in inner.split("@"):
                        token = token.strip()
                        if token.lower() != "cea":
                            parts.append(token)
                import re
                mkt = re.search(r"Regulation for (\w+)", parent_summary)
                if mkt:
                    parts.append(mkt.group(1))
                if parts:
                    parent_suffix = f" ({'/'.join(parts)})"

        def resolve_ticket_key(layer3: str) -> str:
            l3 = layer3.lower()
            if "cyber security" in l3:
                return subtask_map.get("cyber security", task_key)
            if "data security" in l3:
                return subtask_map.get("data security", task_key)
            return task_key

        # Group regulations by Layer3
        by_layer3 = {}
        for reg in regulations:
            layer3 = reg.get("layer3", "Other")
            if layer3 not in by_layer3:
                by_layer3[layer3] = []
            by_layer3[layer3].append(reg)

        group_keys = sorted(by_layer3.keys())
        use_groups = len(group_keys) > 1
        if use_groups:
            content_lines.append("<p><strong>Sub-task:</strong> " +
                f"{ticket_link(task_key)} &nbsp;|&nbsp; <strong>Parent Ticket:</strong> {ticket_link(parent_key)}</p>")
        else:
            only_key = resolve_ticket_key(group_keys[0])
            content_lines.append(
                f"<p><strong>Jira Ticket:</strong> {ticket_link(only_key)}"
                + (f" &nbsp;|&nbsp; <strong>Parent:</strong> {ticket_link(parent_key)}" if parent_key and only_key != task_key else "")
                + "</p>")
        content_lines.append("<hr style='border:none;border-top:1px solid #ddd;'>")
        content_lines.append("<h3 style='color:#2c3e50;'>Regulations to be assessed:</h3>")

        for layer3, regs in sorted(by_layer3.items()):
            link_key = resolve_ticket_key(layer3)
            header = f"【{layer3}】"
            if link_key != task_key:
                header += f" ({ticket_link(link_key)})"
            content_lines.append(f"<h4 style='color:#27ae60;margin-top:16px;margin-bottom:6px;'>{header}</h4>")
            content_lines.append("<table style='border-collapse:collapse;width:100%;'>")
            content_lines.append("<tr style='background:#34495e;color:#fff;'>"
                "<th style='padding:6px 10px;text-align:left;width:80px;'>#</th>"
                "<th style='padding:6px 10px;text-align:left;width:120px;'>DocID</th>"
                "<th style='padding:6px 10px;text-align:left;'>Name</th>"
                "<th style='padding:6px 10px;text-align:center;width:100px;'>Mandatory</th></tr>")
            for i, reg in enumerate(regs, 1):
                doc_id = reg.get("documentId", "-")
                doc_name = reg.get("documentName", "-")
                mandatory = reg.get("mandatory", "-")
                bg = "#f2f2f2" if i % 2 == 0 else "#fff"
                content_lines.append(f"<tr style='background:{bg};'>"
                    f"<td style='padding:6px 10px;'>{i}</td>"
                    f"<td style='padding:6px 10px;'>{doc_id}</td>"
                    f"<td style='padding:6px 10px;'>{doc_name}</td>"
                    f"<td style='padding:6px 10px;text-align:center;'>{mandatory}</td></tr>")
            content_lines.append("</table>")

        content_lines.extend([
            "<hr style='border:none;border-top:1px solid #ddd;'>",
            "<p style='color:#555;font-size:13px;'>Please complete the assessment and update the results in the Jira ticket promptly.</p>",
            f"<p style='color:#888;font-size:12px;'>Sent: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>",
            "</body></html>"
        ])

        content = "\n".join(content_lines)
        
        # Get recipient emails
        recipient_emails = []
        recipient_names = []
        for rid in recipients:
            c = contact_map.get(rid)
            if c:
                recipient_emails.append(c["email"])
                recipient_names.append(c["name"])
        
        # Send via Outlook COM
        sent_count = 0
        errors = []
        
        if recipient_emails:
            try:
                import pythoncom
                import win32com.client
                
                pythoncom.CoInitialize()
                try:
                    outlook = win32com.client.Dispatch("Outlook.Application")
                    for email in recipient_emails:
                        mail = outlook.CreateItem(0)
                        mail.Subject = f"[Assessment Request] {parent_key}{parent_suffix} - Layer3 Regulation Assessment"
                        mail.To = email
                        mail.HTMLBody = content
                        mail.Send()
                        sent_count += 1
                    print(f"[Email] Sent {sent_count} emails to {recipient_emails}")
                finally:
                    pythoncom.CoUninitialize()
            except Exception as e:
                print(f"[Email] Outlook error: {e}, will save to file")
                errors.append(str(e))
        
        # Save to reports
        report_path = REPORTS_DIR / f"assessment_{task_key}_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(content + "\n\n--- RECIPIENTS ---\n" + "\n".join(recipient_names), encoding="utf-8")
        
        # P1-1: 评估分配→追踪打通：发送成功后自动创建gap_tracking条目
        tracking_result = _create_tracking_from_assessment(parent_key, regulations)
        if tracking_result.get("created"):
            print(f"[Assessment] Created {tracking_result['created']} tracking entries for {parent_key}")

        # Record sent ticket for "Processed" badge in Scan Emails
        already_sent = False
        try:
            _ensure_gap_table()
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            recipients_str = ", ".join(recipient_names)
            with sqlite3.connect(DB_PATH) as conn:
                row = conn.execute(
                    "SELECT sent_at FROM assessment_sent WHERE ticket = ?", (task_key,)
                ).fetchone()
                already_sent = row is not None
                conn.execute(
                    """
                    INSERT INTO assessment_sent (ticket, parent_key, sent_at, recipients)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(ticket) DO UPDATE SET
                        parent_key=excluded.parent_key,
                        sent_at=excluded.sent_at,
                        recipients=excluded.recipients
                    """,
                    (task_key, parent_key or "", now, recipients_str),
                )
            print(f"[Assessment] Recorded sent ticket {task_key} (already_sent={already_sent})")
        except Exception as e:
            print(f"[Assessment] Failed to record sent ticket {task_key}: {e}")

        return {
            "ok": True,
            "sent_count": sent_count,
            "recipients": recipient_names,
            "report_path": str(report_path),
            "tracking_created": tracking_result.get("created", 0),
            "tracking_topics": tracking_result.get("topics", []),
            "already_sent": already_sent,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


# P1-1: 评估分配→追踪打通 - 从parent_key到market_name的映射
ASSESSMENT_MARKET_MAPPING = {
    "CEADU-682": "South Korea",
    "CEADU-2631": "South Korea",
    "CEADU-2739": "ASEAN RHD",
    "CEADU-3005": "ASEAN LHD",
    "CEADU-3784": "India",
    "CEADU-4514": "Middle East",
    "CEADU-4494": "Kazakhstan",
    "CEADU-5282": "Uzbekistan",
    "CEADU-6364": "Turkey",
    "CEADU-2711": "AUS/NZL (CMP21)",
    "CEADU-6294": "AUS/NZL (CMP21)",
    "CEADU-6746": "AUS/NZL (CSP31)",
}

# layer3类型到topic_key的映射（这些类型在Layer3票中评估）
LAYER3_TOPIC_TYPES = {"FuSa": "fusa_data", "Functional Safety": "fusa_data"}


def _create_tracking_from_assessment(parent_key: str, regulations: list) -> dict:
    """评估邮件发送后自动创建gap_tracking条目（发送→追踪打通）

    规则：
    1. 根据parent_key确定市场名
    2. 从regulations提取涉及的layer3类型（Topic列匹配到的Layer3）
    3. 对每个涉及的layer3类型创建pending状态条目（如果不存在）
    4. Layer3类型条目对应layer3票，Cyber/Data等子票类型通过其他途径创建
    """
    if not parent_key or not regulations:
        return {"created": 0, "topics": []}

    market_name = ASSESSMENT_MARKET_MAPPING.get(parent_key, "")
    if not market_name:
        return {"created": 0, "topics": []}

    # 从regulations提取涉及的layer3类型
    involved_layer3 = set()
    for reg in regulations:
        layer3 = reg.get("layer3", "")
        if layer3 in LAYER3_TOPIC_TYPES:
            involved_layer3.add(LAYER3_TOPIC_TYPES[layer3])
        elif layer3 in ("Cyber Security", "Data Security"):
            # Cyber/Data通过子票评估，不在此处创建追踪条目
            # 它们的追踪条目由topic_comments API自动回填
            pass
        elif layer3 in ("OTA", "OBD", "Immobilizer-theft"):
            topic_map = {
                "OTA": "ota_data",
                "OBD": "obd_data",
                "Immobilizer-theft": "immobilizer_data",
            }
            topic_key = topic_map.get(layer3)
            if topic_key:
                involved_layer3.add(topic_key)

    if not involved_layer3:
        return {"created": 0, "topics": []}

    created = 0
    created_topics = []
    _ensure_gap_table()

    for topic_key in involved_layer3:
        # 查找市场对应的ticket
        m = next((x for x in MARKETS if x["name"] == market_name), None)
        if not m:
            continue
        ticket = _market_topic_ticket(m, topic_key)
        if not ticket:
            continue

        # 检查是否已存在条目（且状态不是pending）
        with sqlite3.connect(DB_PATH) as conn:
            existing = conn.execute(
                "SELECT status FROM gap_market_tracking WHERE market=? AND topic=?",
                (market_name, topic_key),
            ).fetchone()
            if existing and existing[0] not in ("pending", ""):
                # 已存在非pending状态，跳过
                continue

        # 获取当前评论数用于manual_override保护
        current_comment_count = _get_ticket_comment_count(ticket)

        # 创建或更新为pending状态
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count)
                VALUES (?, ?, ?, 'pending', 0, '', datetime('now','localtime'), 0, ?)
                ON CONFLICT(market, topic) DO UPDATE SET
                    ticket=excluded.ticket,
                    status='pending',
                    comments_total=0,
                    gap_summary='',
                    updated_at=excluded.updated_at,
                    manual_override=0,
                    manual_comment_count=?
            """, (market_name, topic_key, ticket, current_comment_count, current_comment_count))
            created += 1
            created_topics.append(topic_key)

    if created > 0:
        print(f"[Assessment] Created {created} tracking entries for {market_name}: {created_topics}")

    return {"created": created, "topics": created_topics, "market": market_name}


def get_assessments_sent() -> dict:
    """Return tickets for which assessment request emails have already been sent"""
    try:
        _ensure_gap_table()
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT ticket, parent_key, sent_at, recipients FROM assessment_sent ORDER BY sent_at DESC"
            ).fetchall()
        sent = [
            {
                "ticket": row[0],
                "parent_key": row[1],
                "sent_at": row[2],
                "recipients": row[3],
            }
            for row in rows
        ]
        return {"sent": sent, "count": len(sent)}
    except Exception as e:
        print(f"[Assessment] get_assessments_sent error: {e}")
        return {"sent": [], "count": 0, "error": str(e)}


ANALYSIS_DIR = APP_ROOT / "analysis"
ANALYSIS_SCRIPTS = ANALYSIS_DIR / "scripts"

CHAT_MEMORY_FILE = APP_ROOT / "runtime" / "chat_memory.json"
CHAT_SESSIONS_FILE = APP_ROOT / "runtime" / "chat_sessions.json"

OUTLOOK_SCRIPTS_DIR = Path.home() / ".config" / "opencode" / "skills" / "nb-outlook-skill" / "nb-outlook-skill" / "scripts"


def run_outlook_script(script_name: str, args: list[str] = None, timeout: int = 30) -> dict:
    """Run a PowerShell script from the NB Outlook skill and return parsed JSON output"""
    script_path = OUTLOOK_SCRIPTS_DIR / script_name
    if not script_path.exists():
        return {"ok": False, "error": f"Script not found: {script_name}"}
    
    cmd = ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(script_path)]
    if args:
        cmd.extend(args)
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            cwd=str(OUTLOOK_SCRIPTS_DIR)
        )
        
        output = result.stdout.strip() if result.stdout else ""
        
        if result.returncode != 0 and not output:
            return {"ok": False, "error": result.stderr or f"Script error (exit {result.returncode})"}
        
        if not output or output == "True" or output == "False":
            return {"ok": True, "raw": output, "returncode": result.returncode}
        
        try:
            parsed = json.loads(output)
            return {"ok": True, "data": parsed, "raw": output}
        except json.JSONDecodeError:
            return {"ok": True, "raw": output, "text": output}
            
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Script timeout after {timeout}s"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def outlook_latest_email(sender_filter: str = "") -> dict:
    """Get the latest email from inbox"""
    args = []
    if sender_filter:
        args.extend(["-SenderFilter", sender_filter])
    
    result = run_outlook_script("read_latest_email.ps1", args, timeout=15)
    
    if result.get("ok") and result.get("data"):
        data = result["data"]
        return {
            "ok": True,
            "entry_id": data.get("EntryID", ""),
            "subject": data.get("Subject", ""),
            "sender": data.get("SenderName", ""),
            "sender_email": data.get("SenderEmail", ""),
            "received_time": data.get("ReceivedTime", ""),
            "body_preview": data.get("Body", "")[:500] if data.get("Body") else "",
            "body": data.get("Body", ""),
            "has_attachment": data.get("HasAttachment", False),
            "importance": data.get("Importance", 1),
        }
    
    return {"ok": False, "error": result.get("error", "No email found")}


def outlook_search_emails(query: str = "", max_results: int = 10) -> dict:
    """Search emails with natural language query or keywords"""
    if not query.strip():
        return {"ok": False, "error": "Query is required"}
    
    keywords = query.strip()
    
    result = run_outlook_script(
        "search_email.ps1",
        ["-Query", keywords, "-MaxResults", str(max_results), "-AsJson"],
        timeout=30
    )
    
    if result.get("ok") and result.get("data"):
        data = result["data"]
        if isinstance(data, list):
            return {
                "ok": True,
                "count": len(data),
                "emails": [
                    {
                        "entry_id": e.get("EntryID", ""),
                        "subject": e.get("Subject", ""),
                        "sender": e.get("SenderName", ""),
                        "sender_email": e.get("SenderEmail", ""),
                        "received_time": e.get("ReceivedTime", ""),
                        "has_attachment": e.get("HasAttachment", False),
                        "importance": e.get("Importance", 1),
                        "summary": e.get("Summary", {}),
                    }
                    for e in data
                ]
            }
        return {"ok": True, "data": data}
    
    return {"ok": False, "error": result.get("error", "Search failed")}


def outlook_needs_reply(date_filter: str = "today") -> dict:
    """Check emails that need reply"""
    result = run_outlook_script(
        "check_needs_reply.ps1",
        ["-Date", date_filter, "-AsJson"],
        timeout=20
    )
    
    if result.get("ok"):
        raw = result.get("raw", "")
        if "0封" in raw or "no emails need your reply" in raw.lower():
            return {"ok": True, "count": 0, "emails": [], "text": raw}
        
        data = result.get("data", {})
        if isinstance(data, list):
            return {
                "ok": True,
                "count": len(data),
                "emails": data,
                "text": result.get("raw", "")
            }
        
        return {"ok": True, "text": raw, "data": data}
    
    return {"ok": False, "error": result.get("error", "Check failed")}


def outlook_find_contact(search_name: str = "") -> dict:
    """Search contacts by name"""
    if not search_name.strip():
        return {"ok": False, "error": "Search name is required"}
    
    result = run_outlook_script(
        "find_contact.ps1",
        ["-searchName", search_name, "-AsJson"],
        timeout=15
    )
    
    if result.get("ok"):
        data = result.get("data", [])
        if isinstance(data, list):
            return {
                "ok": True,
                "count": len(data),
                "contacts": data[:5],
                "text": result.get("raw", "")
            }
        return {"ok": True, "data": data, "text": result.get("raw", "")}
    
    return {"ok": False, "error": result.get("error", "Search failed")}


def outlook_email_detail(entry_id: str = "") -> dict:
    """Get email thread detail"""
    if not entry_id.strip():
        return {"ok": False, "error": "EntryID is required"}
    
    result = run_outlook_script(
        "read_email_detail.ps1",
        ["-EntryID", entry_id, "-IncludeBody", "-AsJson"],
        timeout=20
    )
    
    if result.get("ok") and result.get("data"):
        return {"ok": True, "data": result["data"]}
    
    return {"ok": False, "error": result.get("error", "Detail fetch failed")}


def outlook_yesterday_emails() -> dict:
    """Get yesterday's email digest"""
    result = run_outlook_script("read_yesterday_emails.ps1", timeout=30)
    
    if result.get("ok"):
        return {"ok": True, "text": result.get("raw", ""), "data": result.get("data")}
    
    return {"ok": False, "error": result.get("error", "Fetch failed")}


EMAIL_INTENT_PATTERNS = [
    (["最新邮件", "最近邮件", "看看邮件", "最新一封"], "latest"),
    (["搜索邮件", "查找邮件", "找邮件", "搜邮件"], "search"),
    (["需要回复", "待回复", "回复我", "回复邮件", "需要答复"], "needs_reply"),
    (["联系人", "找谁", "邮箱", "查联系人", "搜联系人"], "contact"),
    (["昨天邮件", "昨日邮件", "昨天收件", "简报"], "yesterday"),
    (["邮件详情", "邮件内容", "查看邮件"], "detail"),
    (["发邮件", "发送邮件", "写邮件"], "send"),
    (["回复这封", "回复邮件"], "reply"),
]


def detect_email_intent(message: str) -> str | None:
    """Detect if the message is an email-related intent"""
    msg_lower = message.lower()
    for keywords, intent in EMAIL_INTENT_PATTERNS:
        for kw in keywords:
            if kw in msg_lower:
                return intent
    return None


def build_email_tool_result(intent: str, message: str) -> str:
    """Run the appropriate email tool based on detected intent"""
    try:
        if intent == "latest":
            result = outlook_latest_email()
            if result.get("ok"):
                e = result
                return (
                    f"最新邮件:\n"
                    f"主题: {e.get('subject', 'N/A')}\n"
                    f"发件人: {e.get('sender', 'N/A')} <{e.get('sender_email', '')}>\n"
                    f"时间: {e.get('received_time', 'N/A')}\n"
                    f"内容: {e.get('body_preview', '(无正文)')[:300]}..."
                )
            return f"读取失败: {result.get('error', '未知错误')}"
        
        if intent == "search":
            keywords = message
            for kw in ["搜索邮件", "查找邮件", "找邮件", "搜邮件"]:
                keywords = keywords.replace(kw, "").strip()
            if not keywords:
                keywords = "CEADU"
            result = outlook_search_emails(keywords, max_results=5)
            if result.get("ok"):
                emails = result.get("emails", [])
                if not emails:
                    return f"没有找到包含 '{keywords}' 的邮件"
                lines = [f"找到 {result.get('count', 0)} 封邮件:\n"]
                for i, e in enumerate(emails[:5], 1):
                    att = "📎" if e.get("has_attachment") else ""
                    lines.append(
                        f"{i}. [{e.get('received_time', '')[:10]}] {att}{e.get('subject', 'N/A')}\n"
                        f"   发件人: {e.get('sender', 'N/A')}"
                    )
                return "\n".join(lines)
            return f"搜索失败: {result.get('error', '未知错误')}"
        
        if intent == "needs_reply":
            result = outlook_needs_reply("today")
            if result.get("ok"):
                text = result.get("text", "")
                if result.get("count", 0) == 0:
                    return "今天没有需要你回复的邮件，所有邮件已处理完毕！"
                return f"需要回复的邮件 ({result.get('count', '?')}封):\n\n{text[:1500]}"
            return f"检查失败: {result.get('error', '未知错误')}"
        
        if intent == "contact":
            search_name = message
            for kw in ["联系人", "找谁", "邮箱", "查联系人", "搜联系人", "的邮箱"]:
                search_name = search_name.replace(kw, "").strip()
            if not search_name or len(search_name) < 2:
                return "请提供联系人姓名，例如：'查一下Xie Jingjin的邮箱'"
            result = outlook_find_contact(search_name)
            if result.get("ok"):
                contacts = result.get("contacts", [])
                if not contacts:
                    return f"未找到联系人: {search_name}"
                lines = [f"找到联系人:\n"]
                for c in contacts:
                    lines.append(f"- {c.get('name', c.get('displayName', 'N/A'))}: {c.get('email', c.get('smtp', 'N/A'))}")
                return "\n".join(lines)
            return f"联系人搜索失败: {result.get('error', '未知错误')}"
        
        if intent == "yesterday":
            result = outlook_yesterday_emails()
            if result.get("ok"):
                text = result.get("text", "")
                return text[:2000] if text else "昨天没有邮件"
            return f"获取失败: {result.get('error', '未知错误')}"
        
        if intent == "send":
            return (
                "发邮件功能需要更多交互，请通过 'AI Assistant → 发邮件给XXX' 完整描述邮件内容，"
                "我会帮你撰写并确认后发送。"
            )
        
        if intent == "reply":
            return (
                "回复邮件功能需要指定具体邮件。可以通过 '查看最新邮件' 或 '搜索邮件' "
                "找到邮件后再回复。"
            )
        
        return "未识别的邮件指令"
    
    except Exception as e:
        return f"邮件操作出错: {str(e)}"


def assistant_intent_router(message: str) -> dict:
    """Route the message to the appropriate tool and return structured result for LLM"""
    intent = detect_email_intent(message)
    if not intent:
        return {"handled": False, "intent": None}
    
    tool_result = build_email_tool_result(intent, message)
    return {
        "handled": True,
        "intent": intent,
        "tool": "outlook",
        "result": tool_result,
    }


def _load_jira_config() -> tuple[str, str]:
    """Load JIRA URL and token from .jira_config"""
    candidates = [
        APP_ROOT / ".jira_config",
        Path.home() / ".config" / "opencode" / "skills" / "Jira-access" / ".jira_config",
    ]
    jira_url, jira_token = "", ""
    for path in candidates:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("JIRA_URL="):
                jira_url = line.split("=", 1)[1].strip()
            elif line.startswith("JIRA_TOKEN="):
                jira_token = line.split("=", 1)[1].strip()
        if jira_url and jira_token:
            break
    return jira_url, jira_token


def _jira_get(path: str) -> dict | None:
    """GET Jira REST API, return parsed JSON or None"""
    jira_url, jira_token = _load_jira_config()
    if not jira_url or not jira_token:
        return None
    try:
        req = Request(
            jira_url.rstrip("/") + path,
            headers={
                "Authorization": "Bearer " + jira_token,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw.strip() else {}
    except Exception:
        return None


def _jira_post(path: str, payload: dict) -> dict | None:
    """POST Jira REST API.
    Returns None on success (including HTTP 204 empty body),
    returns dict with error info on failure."""
    jira_url, jira_token = _load_jira_config()
    if not jira_url or not jira_token:
        return {"error": "No JIRA config"}
    try:
        req = Request(
            jira_url.rstrip("/") + path,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer " + jira_token,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            if not raw.strip():
                return None
            return json.loads(raw)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err_data = json.loads(body) if body.strip() else {}
        except Exception:
            err_data = {"raw": body[:500]}
        return {"error": f"HTTP {e.code}", "detail": err_data}
    except Exception as e:
        return {"error": str(e)}


MARKETS: list = [
    {"name": "South Korea",    "ticket": "CEADU-682", "layer3": "CEADU-2634", "cyber": "CEADU-2623", "data": "CEADU-2631", "ota": "CEADU-2634", "obd": None,      "fusa": "CEADU-2634"},
    {"name": "ASEAN RHD",      "ticket": "CEADU-2739", "layer3": "CEADU-3137", "cyber": "CEADU-3137", "data": "CEADU-5602", "ota": "CEADU-3137", "obd": None,      "fusa": "CEADU-3137"},
    {"name": "ASEAN LHD",      "ticket": "CEADU-3005", "layer3": "CEADU-3281", "cyber": "CEADU-3281", "data": "CEADU-3281", "ota": "CEADU-3281", "obd": None,      "fusa": "CEADU-3281"},
    {"name": "India",          "ticket": "CEADU-3784", "layer3": "CEADU-3974", "cyber": "CEADU-3971", "data": "CEADU-3974", "ota": "CEADU-3974", "obd": None,      "fusa": "CEADU-3974"},
    {"name": "Middle East",    "ticket": "CEADU-4514", "layer3": "CEADU-5081", "cyber": "CEADU-5081", "data": "CEADU-5751", "ota": "CEADU-5081", "obd": "CEADU-5081", "fusa": "CEADU-5081"},
    {"name": "Kazakhstan",     "ticket": "CEADU-4494", "layer3": "CEADU-4864", "cyber": "CEADU-4864", "data": "CEADU-4870", "ota": "CEADU-4864", "obd": "CEADU-4864", "fusa": "CEADU-4864"},
    {"name": "Uzbekistan",     "ticket": "CEADU-5282", "layer3": "CEADU-6502", "cyber": "CEADU-6509", "data": "CEADU-6508", "ota": "CEADU-6502", "obd": "CEADU-6502", "fusa": "CEADU-6502"},
    {"name": "Turkey",         "ticket": "CEADU-6364", "layer3": "CEADU-6699", "cyber": "CEADU-6706", "data": "CEADU-6705", "ota": "CEADU-6699", "obd": "CEADU-6699", "fusa": "CEADU-6699"},
    {"name": "AUS/NZL (CMP21)","ticket": "CEADU-2711", "layer3": "CEADU-3128", "cyber": "CEADU-3128", "data": "CEADU-5601", "ota": "CEADU-3128", "obd": None,      "fusa": "CEADU-3128"},
    {"name": "AUS/NZL (CSP31)","ticket": "CEADU-6746", "layer3": "CEADU-6749", "cyber": "CEADU-6749", "data": "CEADU-6757", "ota": "CEADU-6749", "obd": "CEADU-6749", "fusa": "CEADU-6749"},
]


def _build_topic_config() -> dict:
    def mk_entries(domain_key: str, layer3_fallback: bool = False):
        entries = []
        for m in MARKETS:
            dom_ticket = m.get(domain_key)
            if not dom_ticket:
                continue
            lt3 = m["layer3"] if layer3_fallback else None
            entries.append((m["name"], m["ticket"], dom_ticket, lt3))
        return entries

    return {
        "cyber_security": {
            "label": "Cyber Security",
            "icon": "\U0001F510",
            "tickets": mk_entries("cyber"),
        },
        "data_security": {
            "label": "Data Security",
            "icon": "\U0001F512",
            "tickets": mk_entries("data"),
        },
        "fusa_data": {
            "label": "Functional Safety",
            "icon": "\U0001F6E1",
            "tickets": mk_entries("layer3"),
        },
        "ota_data": {
            "label": "OTA and SW Update",
            "icon": "\U0001F504",
            "tickets": mk_entries("layer3"),
        },
        "immobilizer_data": {
            "label": "Immobilizer",
            "icon": "\U0001F517",
            "tickets": mk_entries("layer3"),
        },
        "obd_data": {
            "label": "OBD",
            "icon": "\U0001F4FA",
            "tickets": mk_entries("obd"),
        },
    }


TOPIC_CONFIG: dict = _build_topic_config()


GAP_TOPICS: dict = {
    "cyber_security": "cyber",
    "data_security": "data",
    "fusa_data": "layer3",
    "ota_data": "layer3",
    "immobilizer_data": "layer3",
    "obd_data": "obd",
}

GAP_STATUS_FLOW = ["pending", "evaluating", "gap_analysis", "not_applicable", "closed"]

SNAPSHOT_FILE = APP_ROOT / "runtime" / "jira_gap_snapshot.json"
MONITOR_INTERVAL_SEC = 1800
GAP_UPDATES_FILE = APP_ROOT / "runtime" / "jira_gap_updates.json"


@dataclass
class JiraGapMonitor:
    enabled: bool = False
    interval_sec: int = 1800
    running: bool = False
    last_check: str = ""
    next_check: str = ""
    recent_changes: list = field(default_factory=list)
    pending_topics: list = field(default_factory=list)
    thread: threading.Thread | None = None
    stop_event: threading.Event = field(default_factory=threading.Event)
    lock: threading.Lock = field(default_factory=threading.Lock)


JIRA_MONITOR = JiraGapMonitor()


def _load_snapshot() -> dict:
    if not SNAPSHOT_FILE.exists():
        return {}
    try:
        return json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}


def _save_snapshot(snapshot: dict) -> None:
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8")


def _load_updates() -> dict:
    if not GAP_UPDATES_FILE.exists():
        return {"recent": [], "pending": [], "last_update": ""}
    try:
        return json.loads(GAP_UPDATES_FILE.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {"recent": [], "pending": [], "last_update": ""}


def _save_updates(data: dict) -> None:
    GAP_UPDATES_FILE.parent.mkdir(parents=True, exist_ok=True)
    data["last_update"] = time.strftime("%Y-%m-%d %H:%M:%S")
    GAP_UPDATES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _log_inspection(source: str, tickets_checked: int, changed: int, details: str = "") -> None:
    """Record a periodic inspection run (auto monitor or manual check)."""
    try:
        _ensure_gap_table()
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO gap_inspection_log (run_at, source, tickets_checked, changed, details) VALUES (?,?,?,?,?)",
                (time.strftime("%Y-%m-%d %H:%M:%S"), source, tickets_checked, changed, details),
            )
            conn.execute("DELETE FROM gap_inspection_log WHERE id NOT IN (SELECT id FROM gap_inspection_log ORDER BY id DESC LIMIT 100)")
    except Exception as e:
        print(f"[inspection-log] error: {e}")


def get_last_inspection() -> dict:
    """Return the most recent inspection log entry."""
    try:
        _ensure_gap_table()
        with sqlite3.connect(DB_PATH) as conn:
            row = conn.execute(
                "SELECT run_at, source, tickets_checked, changed FROM gap_inspection_log ORDER BY id DESC LIMIT 1"
            ).fetchone()
        if not row:
            return {"last_inspection": None}
        return {"last_inspection": {
            "run_at": row[0], "source": row[1],
            "tickets_checked": row[2], "changed": row[3],
        }}
    except Exception as e:
        return {"last_inspection": None, "error": str(e)}


def _get_tracked_ticket_keys() -> list[tuple]:
    """Get all (ticket_key, topic, market) tuples to monitor."""
    keys = []
    for m in MARKETS:
        for topic, field in GAP_TOPICS.items():
            ticket = m.get(field)
            if ticket:
                keys.append((ticket, topic, m["name"]))
    return keys


def _fetch_ticket_comment_info(ticket_key: str) -> tuple[int, str]:
    """Get comment count and last updated time for a Jira ticket."""
    data = _jira_get(f"/rest/api/2/issue/{ticket_key}?fields=updated,comment")
    if not data:
        return 0, ""
    fields = data.get("fields", {})
    comment_count = len(fields.get("comment", {}).get("comments", []))
    updated = str(fields.get("updated", ""))[:19]
    return comment_count, updated


def _check_all_tickets_snapshot() -> dict[str, dict]:
    """Fetch current state of all tracked tickets. Returns dict: ticket_key -> {comment_count, updated, topic, market}."""
    snapshot = _load_snapshot()
    current = {}
    keys = _get_tracked_ticket_keys()
    seen_tickets = set()

    for ticket_key, topic, market in keys:
        seen_tickets.add(ticket_key)
        old = snapshot.get(ticket_key, {})
        new_count, new_updated = _fetch_ticket_comment_info(ticket_key)
        current[ticket_key] = {
            "comment_count": new_count,
            "updated": new_updated,
            "topic": topic,
            "market": market,
            "changed": False,
        }
        old_count = old.get("comment_count", 0)
        if new_count != old_count and old_count > 0:
            current[ticket_key]["changed"] = True
            current[ticket_key]["delta"] = new_count - old_count
            current[ticket_key]["old_count"] = old_count

    return current, seen_tickets


def _trigger_analysis_for_changed(topics_changed: set, current_state: dict) -> None:
    """Trigger build_topic_comments_report for changed topics, then analyze markets."""
    if not topics_changed:
        return
    topic_list = list(topics_changed)
    print(f"[GapMonitor] Triggering analysis for: {topic_list}")
    try:
        result = build_topic_comments_report(topic_list[0] if len(topic_list) == 1 else "")
        if result.get("ok"):
            topics_data = result.get("topics", {})
            for t, data in topics_data.items():
                changed_markets = [
                    {"market": mk["market"], "ticket": mk.get("domain") or mk.get("layer3") or mk.get("parent")}
                    for mk in data.get("markets", [])
                    if current_state.get(mk.get("domain") or mk.get("layer3") or mk.get("parent"), {}).get("changed")
                ]
                if changed_markets:
                    print(f"[GapMonitor] {t}: updated {len(changed_markets)} markets")
    except Exception as e:
        print(f"[GapMonitor] Analysis error: {e}")


def _add_gap_update(market: str, topic: str, ticket: str, change_type: str, details: str = "") -> None:
    """Add a gap update notification."""
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "id": f"{market}_{topic}_{int(time.time())}",
        "market": market,
        "topic": topic,
        "ticket": ticket,
        "type": change_type,
        "details": details,
        "time": now,
        "read": False,
    }
    updates = _load_updates()
    recent = updates.get("recent", [])
    recent.insert(0, entry)
    recent = recent[:50]
    updates["recent"] = recent
    _save_updates(updates)
    print(f"[GapMonitor] New update: {market}/{topic} {change_type}")


def jira_gap_monitor_loop() -> None:
    """Background thread: periodically checks Jira tickets for comment updates."""
    last_check_time = 0.0
    seen_initial = False

    while True:
        interval = MONITOR_INTERVAL_SEC
        with JIRA_MONITOR.lock:
            if not JIRA_MONITOR.enabled:
                JIRA_MONITOR.running = False
                return
            interval = JIRA_MONITOR.interval_sec
            JIRA_MONITOR.next_check = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + interval))

        if JIRA_MONITOR.stop_event.wait(interval):
            return

        current_time = time.time()
        print(f"[GapMonitor] Running check at {time.strftime('%H:%M:%S')}")
        JIRA_MONITOR.last_check = time.strftime("%Y-%m-%d %H:%M:%S")

        try:
            current_state, seen_tickets = _check_all_tickets_snapshot()
            snapshot = _load_snapshot()

            if not seen_initial:
                for key, val in current_state.items():
                    snapshot[key] = {"comment_count": val["comment_count"], "updated": val["updated"]}
                _save_snapshot(snapshot)
                seen_initial = True
                _log_inspection("auto", len(current_state), 0, "initial snapshot")
                print(f"[GapMonitor] Initial snapshot saved ({len(snapshot)} tickets)")
                continue

            changed_ticket_keys = [k for k, v in current_state.items() if v.get("changed")]
            topics_changed = set()
            market_changes = []

            for tk in changed_ticket_keys:
                info = current_state[tk]
                old_count = snapshot.get(tk, {}).get("comment_count", 0)
                new_count = info["comment_count"]
                delta = new_count - old_count
                topic = info["topic"]
                market = info["market"]

                snapshot[tk] = {"comment_count": new_count, "updated": info["updated"]}
                topics_changed.add(topic)
                market_changes.append({"ticket": tk, "market": market, "topic": topic, "delta": delta})
                _add_gap_update(
                    market, topic, tk,
                    "comment_added" if delta > 0 else "comment_removed",
                    f"+{delta}条" if delta > 0 else f"{delta}条评论"
                )

            _log_inspection("auto", len(current_state), len(changed_ticket_keys),
                            "; ".join(f"{c['ticket']} {c['delta']:+d}" for c in market_changes))

            if changed_ticket_keys:
                _save_snapshot(snapshot)
                _trigger_analysis_for_changed(topics_changed, current_state)
                updates = _load_updates()
                updates["pending"] = market_changes
                _save_updates(updates)
            else:
                for key in list(snapshot.keys()):
                    if key not in seen_tickets:
                        del snapshot[key]
                _save_snapshot(snapshot)

        except Exception as e:
            print(f"[GapMonitor] Error: {e}")

        last_check_time = current_time


def start_jira_gap_monitor(interval_sec: int = 1800) -> None:
    """Start the Jira gap monitoring thread."""
    with JIRA_MONITOR.lock:
        JIRA_MONITOR.enabled = True
        JIRA_MONITOR.interval_sec = interval_sec
        JIRA_MONITOR.stop_event = threading.Event()
        if not JIRA_MONITOR.thread or not JIRA_MONITOR.thread.is_alive():
            JIRA_MONITOR.thread = threading.Thread(target=jira_gap_monitor_loop, daemon=True)
            JIRA_MONITOR.thread.start()
        JIRA_MONITOR.running = True


def stop_jira_gap_monitor() -> None:
    """Stop the Jira gap monitoring thread."""
    with JIRA_MONITOR.lock:
        JIRA_MONITOR.enabled = False
        JIRA_MONITOR.stop_event.set()
        JIRA_MONITOR.running = False


def get_gap_updates(since: str = "") -> dict:
    """Get recent gap updates, optionally filtered by time."""
    updates = _load_updates()
    recent = updates.get("recent", [])
    if since:
        try:
            since_ts = time.mktime(time.strptime(since, "%Y-%m-%d %H:%M:%S"))
            recent = [r for r in recent if time.mktime(time.strptime(r["time"], "%Y-%m-%d %H:%M:%S")) > since_ts]
        except Exception:
            pass
    unread = [r for r in recent if not r.get("read")]
    updates["recent"] = recent
    updates["unread_count"] = len(unread)
    updates["total_count"] = len(recent)
    return updates


def trigger_gap_check_now() -> dict:
    """Trigger an immediate check of all tickets."""
    try:
        current_state, _ = _check_all_tickets_snapshot()
        snapshot = _load_snapshot()
        changed = []
        for tk, info in current_state.items():
            old = snapshot.get(tk, {})
            if info["comment_count"] != old.get("comment_count", 0):
                snapshot[tk] = {"comment_count": info["comment_count"], "updated": info["updated"]}
                changed.append({
                    "ticket": tk, "market": info["market"], "topic": info["topic"],
                    "old_count": old.get("comment_count", 0),
                    "new_count": info["comment_count"],
                    "delta": info["comment_count"] - old.get("comment_count", 0)
                })
                _add_gap_update(info["market"], info["topic"], tk, "comment_change",
                    f"检测到{info['comment_count'] - old.get('comment_count', 0):+d}条评论")
        _save_snapshot(snapshot)
        topics_changed = set(c["topic"] for c in changed)
        if changed:
            _trigger_analysis_for_changed(topics_changed, current_state)
        updates = _load_updates()
        updates["pending"] = changed
        _save_updates(updates)
        _log_inspection("manual", len(current_state), len(changed),
                        "; ".join(f"{c['ticket']}({c['old_count']}->{c['new_count']})" for c in changed))
        return {"ok": True, "checked": len(current_state), "changed": len(changed), "changes": changed}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def mark_updates_read() -> None:
    """Mark all recent updates as read."""
    updates = _load_updates()
    for r in updates.get("recent", []):
        r["read"] = True
    _save_updates(updates)


def _market_topic_ticket(market: dict, topic: str) -> str | None:
    """Get the tracked ticket key for a market+topic combination.
    - Cyber / Data: own sub-tickets (closed by their owners)
    - FuSa / OTA / Immobilizer: Layer3 ticket (closed by user)
    - OBD: own ticket or None (not applicable to some markets)"""
    field = GAP_TOPICS.get(topic, "layer3")
    return market.get(field) or None


def _ensure_gap_table() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gap_market_tracking (
                market TEXT NOT NULL,
                topic TEXT NOT NULL,
                ticket TEXT DEFAULT '',
                status TEXT DEFAULT 'pending',
                comments_total INTEGER DEFAULT 0,
                gap_summary TEXT DEFAULT '',
                updated_at TEXT,
                PRIMARY KEY (market, topic)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gap_layer3_closed (
                market TEXT PRIMARY KEY,
                ticket TEXT NOT NULL,
                closed_at TEXT,
                gap_summary TEXT DEFAULT ''
            )
        """)
        try:
            conn.execute("ALTER TABLE gap_market_tracking ADD COLUMN gap_summary TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
        try:
            conn.execute("ALTER TABLE gap_layer3_closed ADD COLUMN gap_summary TEXT DEFAULT ''")
        except sqlite3.OperationalError:
            pass
        try:
            conn.execute("ALTER TABLE gap_market_tracking ADD COLUMN manual_override INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        try:
            conn.execute("ALTER TABLE gap_market_tracking ADD COLUMN manual_comment_count INTEGER DEFAULT -1")
        except sqlite3.OperationalError:
            pass
        conn.execute("""
            CREATE TABLE IF NOT EXISTS gap_inspection_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_at TEXT NOT NULL,
                source TEXT DEFAULT 'auto',
                tickets_checked INTEGER DEFAULT 0,
                changed INTEGER DEFAULT 0,
                details TEXT DEFAULT ''
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assessment_sent (
                ticket TEXT PRIMARY KEY,
                parent_key TEXT DEFAULT '',
                sent_at TEXT,
                recipients TEXT DEFAULT ''
            )
        """)


def _mark_market_topic_completed(market: str, topic: str, ticket: str = "", comments: int = 0) -> None:
    """Mark one market+topic as completed (called after successful topic_comments run)"""
    _ensure_gap_table()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, updated_at)
            VALUES (?, ?, ?, 'completed', ?, ?)
            ON CONFLICT(market, topic) DO UPDATE SET
                ticket=excluded.ticket,
                status='completed',
                comments_total=excluded.comments_total,
                updated_at=excluded.updated_at
        """, (market, topic, ticket, comments, now))


def _mark_market_topic_gap_analysis(market: str, topic: str, ticket: str = "", comments: int = 0, gap_summary: str = "") -> None:
    """Mark one market+topic as gap_analysis - gap analysis sufficient to give conclusion"""
    _ensure_gap_table()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at)
            VALUES (?, ?, ?, 'gap_analysis', ?, ?, ?)
            ON CONFLICT(market, topic) DO UPDATE SET
                ticket=excluded.ticket,
                status='gap_analysis',
                comments_total=excluded.comments_total,
                gap_summary=excluded.gap_summary,
                updated_at=excluded.updated_at
        """, (market, topic, ticket, comments, gap_summary, now))


def _mark_market_topic_pending(market: str, topic: str, manual_count: int = -1) -> None:
    _ensure_gap_table()
    with sqlite3.connect(DB_PATH) as conn:
        existing = conn.execute(
            "SELECT manual_override, manual_comment_count FROM gap_market_tracking WHERE market=? AND topic=?",
            (market, topic),
        ).fetchone()
        manual_override = 1
        manual_comment_count = manual_count if manual_count >= 0 else (existing[1] if existing else -1)
        conn.execute("""
            INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count)
            VALUES (?, ?, '', 'pending', 0, '', datetime('now','localtime'), ?, ?)
            ON CONFLICT(market, topic) DO UPDATE SET
                status='pending', ticket=excluded.ticket, comments_total=0, gap_summary='',
                updated_at=excluded.updated_at, manual_override=?, manual_comment_count=?
        """, (market, topic, manual_override, manual_comment_count, manual_override, manual_comment_count))


def _auto_detect_na(auto: bool = True) -> None:
    """Auto-detect topics that are 'not applicable' (no evaluation needed).

    Rules:
    - the topic row exists in gap_market_tracking
    - row status is 'pending' (never touched by user/comments)
    - the mapped Jira ticket does NOT exist, OR
    - the ticket has 0 comments AND its Jira status is a terminal state
      (Done / Closed / Cancelled / Rejected) -> no evaluation was needed.

    Such rows are updated to 'not_applicable' in the DB.
    """
    if not auto:
        return
    _ensure_gap_table()
    marked = 0
    try:
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT market, topic, ticket, status, manual_override, manual_comment_count FROM gap_market_tracking WHERE status='pending'"
            ).fetchall()
        if not rows:
            return
        pending = []
        for market_name, topic, ticket, status, manual_override, manual_comment_count in rows:
            if not ticket:
                continue
            info = _fetch_ticket_info(ticket)
            tstatus = (info or {}).get("status", "N/A")
            comment_count = (info or {}).get("comment_count", 0)
            if tstatus in ("ERROR", "N/A"):
                continue
            if manual_override and manual_comment_count >= 0 and comment_count <= manual_comment_count:
                continue
            if comment_count == 0 and tstatus.lower() in ("done", "closed", "cancelled", "canceled", "rejected", "withdrawn", "not applicable", "obsolete", "superseded"):
                pending.append((market_name, topic, ticket))
                print(f"[gap-auto-NA] auto-NA: {market_name}/{topic} (cc={comment_count}, tstatus={tstatus})")
        if not pending:
            return
        with sqlite3.connect(DB_PATH) as conn:
            for market_name, topic, ticket in pending:
                cur = conn.execute(
                    "SELECT 1 FROM gap_market_tracking WHERE market=? AND topic=?",
                    (market_name, topic),
                )
                if not cur.fetchone():
                    conn.execute(
                        "INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count) VALUES (?,?,?,?,0,'',datetime('now','localtime'),0,-1)",
                        (market_name, topic, ticket or ""),
                    )
                conn.execute(
                    "UPDATE gap_market_tracking SET status='not_applicable', updated_at=datetime('now','localtime') WHERE market=? AND topic=? AND (manual_override=0 OR manual_comment_count<0)",
                    (market_name, topic),
                )
            marked = len(pending)
        if marked:
            print(f"[gap-auto-NA] marked {marked} pending topic(s) as not_applicable")
    except Exception as e:
        print(f"[gap-auto-NA] error: {e}")


def _auto_promote_evaluating() -> None:
    """Auto-promote evaluating topics to gap_analysis when conditions are met.

    Condition: Jira ticket has no recent activity (>14 days since last comment)
    OR Jira ticket is in a closed/done terminal state.
    (The ticket is essentially done but user hasn't manually updated status yet.)
    """
    try:
        _ensure_gap_table()
        with sqlite3.connect(DB_PATH) as conn:
            rows = conn.execute(
                "SELECT market, topic, ticket, status, manual_override, manual_comment_count FROM gap_market_tracking WHERE status='evaluating'"
            ).fetchall()
        if not rows:
            return
        promoted = 0
        # Cache ticket info
        cache: dict = {}
        def ticket_info(tkey):
            if tkey not in cache:
                cache[tkey] = _fetch_ticket_info(tkey)
            return cache[tkey]
        now_ts = time.time()
        for market_name, topic, ticket, status, manual_override, manual_comment_count in rows:
            if not ticket:
                continue
            info = ticket_info(ticket)
            tstatus = (info or {}).get("status", "")
            current_comment_count = (info or {}).get("comment_count", 0)
            if manual_override and manual_comment_count >= 0 and current_comment_count <= manual_comment_count:
                continue
            comments = info.get("comments", []) or []
            last_comment_ts = 0
            last_comment_text = ""
            for c in comments:
                created = c.get("created", "")
                if created:
                    ts = 0
                    try:
                        ts = time.mktime(time.strptime(created[:19], "%Y-%m-%dT%H:%M:%S"))
                    except Exception:
                        try:
                            ts = time.mktime(time.strptime(created[:10], "%Y-%m-%d"))
                        except Exception:
                            ts = 0
                    if ts > last_comment_ts:
                        last_comment_ts = ts
                        last_comment_text = c.get("body", "")
            # Check if auto-promotable
            auto_promote = False
            if tstatus.lower() in ("done", "closed", "cancelled", "canceled", "rejected", "withdrawn", "not applicable", "obsolete", "superseded"):
                auto_promote = True
            elif last_comment_ts > 0:
                days_since = (now_ts - last_comment_ts) / 86400
                if days_since > 10:
                    auto_promote = True
            if auto_promote:
                with sqlite3.connect(DB_PATH) as conn:
                    conn.execute(
                        "UPDATE gap_market_tracking SET status='gap_analysis', updated_at=datetime('now','localtime') WHERE market=? AND topic=?",
                        (market_name, topic),
                    )
                promoted += 1
        if promoted:
            print(f"[gap-auto-promote] promoted {promoted} topic(s) to gap_analysis")
    except Exception as e:
        print(f"[gap-auto-promote] error: {e}")


def gap_tracking_status(auto_detect_na: bool = True) -> dict:
    """Market-level gap analysis tracking status.
    Each market shows its 6 topics, their ticket keys, completion status,
    and whether the market's Layer3 ticket is ready to close.

    Status flow: pending -> evaluating -> gap_analysis -> closed
    - pending: Initial state
    - evaluating: Jira ticket is being evaluated
    - gap_analysis: Gap analysis sufficient to give conclusion
    - closed: Layer3 ticket is closed
    - not_applicable: PSV里无命中规则，无需评估

    For can_close: all NEEDED topics must be in gap_analysis or not_applicable.
    'not_applicable' topics are excluded from the can_close denominator."""
    _auto_detect_na(auto=auto_detect_na)
    _auto_promote_evaluating()
    _ensure_gap_table()
    stored: dict = {}
    # Ticket info cache for auto-detection (avoid repeated Jira calls)
    _ticket_info_cache: dict = {}

    def _get_ticket_info_cached(tkey: str) -> dict:
        if tkey not in _ticket_info_cache:
            _ticket_info_cache[tkey] = _fetch_ticket_info(tkey)
        return _ticket_info_cache[tkey]

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count FROM gap_market_tracking"
        ).fetchall()
        closed_rows = conn.execute(
            "SELECT market, ticket, closed_at, gap_summary FROM gap_layer3_closed"
        ).fetchall()
    for row in rows:
        stored[(row[0], row[1])] = {
            "ticket": row[2], "status": row[3],
            "comments_total": row[4], "gap_summary": row[5] if len(row) > 5 else "",
            "updated_at": row[6] if len(row) > 6 else row[5] if len(row) > 5 else "",
            "manual_override": row[7] if len(row) > 7 else 0,
            "manual_comment_count": row[8] if len(row) > 8 else -1,
        }
    layer3_closed = {r[0]: {"ticket": r[1], "closed_at": r[2], "gap_summary": r[3] if len(r) > 3 else ""} for r in closed_rows}

    markets_out = []
    for m in MARKETS:
        market_name = m["name"]
        layer3_ticket = m["layer3"]
        topics = []
        for topic_key, label_cfg in TOPIC_CONFIG.items():
            ticket = _market_topic_ticket(m, topic_key)
            if not ticket:
                continue
            row = stored.get((market_name, topic_key), {})
            row_status = row.get("status", "")

            # For missing DB entries: auto-detect whether evaluation is needed
            # Skip auto-detect if user manually set status (manual_override) and no new Jira comments appeared
            row_manual = row.get("manual_override", 0)
            row_manual_count = row.get("manual_comment_count", -1)
            if not row_status:
                if row_manual and row_manual_count >= 0:
                    row_status = "pending"
                else:
                    info = _get_ticket_info_cached(ticket)
                    tstatus = (info or {}).get("status", "N/A")
                    comment_count = (info or {}).get("comment_count", 0)
                    if tstatus == "N/A" or (comment_count == 0 and tstatus.lower() in (
                        "done", "closed", "cancelled", "canceled", "rejected", "withdrawn",
                        "not applicable", "not_applicable", "obsolete", "superseded"
                    )):
                        row_status = "not_applicable"
                    else:
                        row_status = "pending"

            topics.append({
                "topic": topic_key,
                "label": label_cfg.get("label", topic_key),
                "icon": label_cfg.get("icon", ""),
                "ticket": ticket or row.get("ticket", ""),
                "status": row_status,
                "comments_total": row.get("comments_total", 0),
                "gap_summary": row.get("gap_summary", ""),
                "updated_at": row.get("updated_at", ""),
                "manual_override": row.get("manual_override", 0),
                "is_owner": topic_key in ("fusa_data", "ota_data", "immobilizer_data") or topic_key == "cyber_security" and ticket == layer3_ticket,
            })
        gap_analyzed = sum(1 for t in topics if t["status"] == "gap_analysis")
        evaluating = sum(1 for t in topics if t["status"] == "evaluating")
        completed = sum(1 for t in topics if t["status"] in ("completed", "gap_analysis"))
        na_count = sum(1 for t in topics if t["status"] == "not_applicable")
        needed_topics = [t for t in topics if t["status"] != "not_applicable"]
        total_topics = len(needed_topics)
        # can_close: all needed topics are gap_analysis (NA topics don't need evaluation)
        can_close = total_topics > 0 and gap_analyzed == total_topics
        closed_info = layer3_closed.get(market_name)
        markets_out.append({
            "market": market_name,
            "layer3_ticket": layer3_ticket,
            "layer3_open_url": f"https://devstack.vgc.com.cn/jira/browse/{layer3_ticket}",
            "topics": topics,
            "gap_analyzed": gap_analyzed,
            "evaluating": evaluating,
            "completed": completed,
            "na_count": na_count,
            "total_topics": total_topics,
            "can_close": can_close,
            "layer3_closed": closed_info is not None,
            "layer3_closed_at": (closed_info or {}).get("closed_at", ""),
        })

    ready_markets = [m for m in markets_out if m["can_close"] and not m["layer3_closed"]]
    closed_markets = [m for m in markets_out if m["layer3_closed"]]
    insp = get_last_inspection()

    # P1-2: 到期提醒 - can_close=true 且 Layer3 未关闭的市场
    reminders = []
    for m in ready_markets:
        topics_by_status = {}
        for t in m["topics"]:
            s = t["status"]
            if s not in topics_by_status:
                topics_by_status[s] = []
            topics_by_status[s].append(t["label"])
        reminder_text = ""
        if "gap_analysis" in topics_by_status:
            # 所有领域都已 gap_analysis，提示写 Summary + 关闭 Layer3
            reminder_text = f"All {len(m['topics'])} topics analyzed. Ready to write Summary Comment and close Layer3."
        elif m["gap_analyzed"] > 0:
            reminder_text = f"{m['gap_analyzed']}/{m['total_topics']} topics analyzed. Still need: {', '.join(topics_by_status.get('pending', []) + topics_by_status.get('evaluating', []))}"
        reminders.append({
            "market": m["market"],
            "layer3_ticket": m["layer3_ticket"],
            "layer3_url": m["layer3_open_url"],
            "gap_analyzed": m["gap_analyzed"],
            "total_topics": m["total_topics"],
            "reminder_text": reminder_text,
            "action_needed": m["gap_analyzed"] == m["total_topics"],
        })

    return {
        "ok": True,
        "markets": markets_out,
        "summary": {
            "total_markets": len(markets_out),
            "ready_to_close": len(ready_markets),
            "closed": len(closed_markets),
            "all_done": sum(1 for m in markets_out if m["can_close"]),
        },
        "reminders": reminders,
        "last_inspection": insp.get("last_inspection"),
        "monitor": {
            "running": JIRA_MONITOR.running,
            "last_check": JIRA_MONITOR.last_check,
            "next_check": JIRA_MONITOR.next_check,
        }
    }


def _get_ticket_comment_count(ticket: str) -> int:
    """Get current comment count for a ticket, -1 if error/not found."""
    if not ticket:
        return -1
    try:
        info = _fetch_ticket_info(ticket)
        if not info:
            return -1
        return (info or {}).get("comment_count", 0)
    except Exception as e:
        print(f"[get-comment-count] {ticket}: {e}")
        return -1


def gap_tracking_set_status(market: str, topic: str, status: str, gap_summary: str = "") -> dict:
    """Set a market+topic to a specific status in the flow.
    pending -> evaluating -> gap_analysis -> closed"""
    _ensure_gap_table()
    m = next((x for x in MARKETS if x["name"] == market), None)
    if not m:
        return {"ok": False, "error": f"Unknown market: {market}"}
    if topic not in TOPIC_CONFIG:
        return {"ok": False, "error": f"Unknown topic: {topic}"}
    if status not in GAP_STATUS_FLOW:
        return {"ok": False, "error": f"Unknown status: {status}"}
    ticket = _market_topic_ticket(m, topic) or ""
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    manual_count = _get_ticket_comment_count(ticket)
    if status == "pending":
        _mark_market_topic_pending(market, topic, manual_count=manual_count)
    elif status == "evaluating":
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count)
                VALUES (?, ?, ?, 'evaluating', 0, '', ?, 1, ?)
                ON CONFLICT(market, topic) DO UPDATE SET
                    ticket=excluded.ticket,
                    status='evaluating',
                    updated_at=excluded.updated_at,
                    manual_override=1,
                    manual_comment_count=excluded.manual_comment_count
            """, (market, topic, ticket, now, manual_count))
    elif status == "gap_analysis":
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count)
                VALUES (?, ?, ?, 'gap_analysis', 0, ?, ?, 1, ?)
                ON CONFLICT(market, topic) DO UPDATE SET
                    ticket=excluded.ticket,
                    status='gap_analysis',
                    gap_summary=excluded.gap_summary,
                    updated_at=excluded.updated_at,
                    manual_override=1,
                    manual_comment_count=excluded.manual_comment_count
            """, (market, topic, ticket, gap_summary, now, manual_count))
    elif status == "closed":
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count)
                VALUES (?, ?, ?, 'closed', 0, ?, ?, 1, ?)
                ON CONFLICT(market, topic) DO UPDATE SET
                    ticket=excluded.ticket,
                    status='closed',
                    gap_summary=excluded.gap_summary,
                    updated_at=excluded.updated_at,
                    manual_override=1,
                    manual_comment_count=excluded.manual_comment_count
            """, (market, topic, ticket, gap_summary, now, manual_count))
    return {"ok": True, "market": market, "topic": topic, "ticket": ticket, "status": status}


def gap_tracking_complete(market: str, topic: str) -> dict:
    """Manually mark a market+topic as completed (legacy, keeps working)"""
    _ensure_gap_table()
    m = next((x for x in MARKETS if x["name"] == market), None)
    if not m:
        return {"ok": False, "error": f"Unknown market: {market}"}
    if topic not in TOPIC_CONFIG:
        return {"ok": False, "error": f"Unknown topic: {topic}"}
    ticket = _market_topic_ticket(m, topic) or ""
    _mark_market_topic_completed(market, topic, ticket)
    return {"ok": True, "market": market, "topic": topic, "ticket": ticket, "status": "completed"}


def gap_tracking_reset(market: str, topic: str) -> dict:
    """Reset a market+topic back to pending"""
    _ensure_gap_table()
    m = next((x for x in MARKETS if x["name"] == market), None)
    ticket = _market_topic_ticket(m, topic) if m else ""
    manual_count = _get_ticket_comment_count(ticket)
    _mark_market_topic_pending(market, topic, manual_count=manual_count)
    return {"ok": True, "market": market, "topic": topic, "status": "pending"}


def _build_market_summary_comment(market: str) -> str:
    """Build Summary Comment body from all gap_analysis topics of a market"""
    _ensure_gap_table()
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT topic, status, gap_summary, ticket FROM gap_market_tracking WHERE market=?",
            (market,),
        ).fetchall()

    if not rows:
        return ""

    sections = [
        f"====== Regulatory Compliance Assessment Summary for {market} ======",
        f"Assessment Date: {time.strftime('%Y-%m-%d')}",
        "",
        "## Assessment Results",
        "",
    ]

    topic_labels = {k: v.get("label", k) for k, v in TOPIC_CONFIG.items()}
    status_icons = {
        "gap_analysis": "✅ Gap Analysis Done",
        "evaluating": "🔄 In Evaluation",
        "pending": "⏳ Pending",
        "not_applicable": "⚪ N/A",
        "closed": "📌 Closed",
    }
    na_count = 0
    gap_count = 0
    for topic, status, gap_summary, ticket in rows:
        label = topic_labels.get(topic, topic)
        icon = status_icons.get(status, status)
        if status == "not_applicable":
            na_count += 1
        elif status in ("gap_analysis", "completed"):
            gap_count += 1
        sections.append(f"### {icon} {label}")
        if ticket:
            sections.append(f"Ticket: {ticket}")
        if gap_summary:
            clean_summary = re.sub(r"\[~[^\]]+\]|\[https?://[^\]]+\]|\{[^}]+\}", "", gap_summary).strip()
            if clean_summary:
                sections.append(f"Summary: {clean_summary}")
        sections.append("")

    total = len(rows)
    sections.extend([
        "## Overall Assessment",
        f"- Total domains assessed: {total}",
        f"- Gap analysis completed: {gap_count}",
        f"- Not applicable: {na_count}",
        f"- Assessment status: {'All domains analyzed' if gap_count + na_count == total else 'In progress'}",
        "",
        "====== End of Assessment Summary ======",
    ])

    return "\n".join(sections)


def write_summary_comment(market: str) -> dict:
    """Write Summary Comment to Layer3 Jira ticket for a market"""
    _ensure_gap_table()
    m = next((x for x in MARKETS if x["name"] == market), None)
    if not m:
        return {"ok": False, "error": f"Unknown market: {market}"}
    key = m["layer3"]
    if not key:
        return {"ok": False, "error": "No Layer3 ticket for this market"}

    comment_body = _build_market_summary_comment(market)
    if not comment_body:
        return {"ok": False, "error": "No gap tracking data found for this market"}

    result = _jira_post(
        f"/rest/api/2/issue/{key}/comments",
        {"body": comment_body},
    )
    if result is not None:
        err_msg = result.get("error", "") or str(result)
        err_detail = result.get("detail", {})
        if isinstance(err_detail, dict):
            msgs = err_detail.get("errorMessages", [])
            errs = err_detail.get("errors", {})
            if msgs or errs:
                err_msg = " | ".join(msgs + [f"{k}: {v}" for k, v in errs.items()])
        return {"ok": False, "error": err_msg, "ticket": key}

    now = time.strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        gap_summary = comment_body[:500]
        conn.execute("""
            INSERT OR REPLACE INTO gap_layer3_closed (market, ticket, closed_at, gap_summary)
            VALUES (?, ?, ?, ?)
        """, (market, key, now, gap_summary))

    print(f"[Summary] Written to {key} for {market}")
    return {"ok": True, "ticket": key, "market": market, "comment_length": len(comment_body)}


def close_layer3_ticket(market: str) -> dict:
    """Close ONLY the Layer3 ticket of a market (owned by the user).
    Sub-tickets (Cyber/Data) belong to other teams and are NOT touched.
    P2: Automatically writes Summary Comment to Jira before closing."""
    _ensure_gap_table()
    m = next((x for x in MARKETS if x["name"] == market), None)
    if not m:
        return {"ok": False, "error": f"Unknown market: {market}"}
    key = m["layer3"]
    if not key:
        return {"ok": False, "error": "No Layer3 ticket for this market"}
    issue_data = _jira_get(f"/rest/api/2/issue/{key}")
    if not issue_data:
        return {"ok": False, "error": f"无法获取工单 {key}", "ticket": key}

    # P2: Write Summary Comment before closing
    summary_result = write_summary_comment(market)
    if not summary_result.get("ok"):
        return {"ok": False, "error": "Failed to write Summary Comment: " + summary_result.get("error", ""), "ticket": key}
    summary_written = True

    current_status = (issue_data.get("fields", {}).get("status", {}).get("name", "") or "").lower()
    if "done" in current_status or "closed" in current_status:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO gap_layer3_closed (market, ticket, closed_at) VALUES (?, ?, ?)
            """, (market, key, now))
        return {"ok": True, "ticket": key, "closed": True, "skipped": "已是 Done"}
    transitions_data = _jira_get(f"/rest/api/2/issue/{key}/transitions")
    if not transitions_data:
        return {"ok": False, "error": "Cannot get transitions", "ticket": key}
    done_trans = None
    for t in transitions_data.get("transitions", []):
        t_name = (t.get("name") or "").lower()
        if "done" in t_name or "closed" in t_name or "完成" in t_name:
            done_trans = t
            break
    if not done_trans:
        return {"ok": False, "error": "无 Done 过渡可用", "ticket": key}
    payload = {"transition": {"id": str(done_trans["id"])}}
    fields = done_trans.get("fields") or {}
    if "resolution" in fields:
        payload["fields"] = {"resolution": {"name": "Fixed"}}
    result = _jira_post(f"/rest/api/2/issue/{key}/transitions", payload)
    if result is None:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO gap_layer3_closed (market, ticket, closed_at) VALUES (?, ?, ?)
            """, (market, key, now))
        return {"ok": True, "ticket": key, "closed": True, "transition": done_trans.get("name", "Done")}
    err_msg = result.get("error", "") or str(result)
    err_detail = result.get("detail", {})
    if isinstance(err_detail, dict):
        msgs = err_detail.get("errorMessages", [])
        errs = err_detail.get("errors", {})
        if msgs or errs:
            err_msg += ": " + str(msgs or errs)
    return {"ok": False, "ticket": key, "error": err_msg[:150]}


def _fetch_ticket_info(ticket_key: str) -> dict:
    """Fetch ticket status and recent comments"""
    info = {
        "key": ticket_key,
        "status": "N/A",
        "summary": "",
        "assignee": "",
        "updated": "",
        "comment_count": 0,
        "comments": [],
    }
    data = _jira_get(f"/rest/api/2/issue/{ticket_key}")
    if not data:
        info["status"] = "ERROR"
        return info
    fields = data.get("fields", {})
    assignee = fields.get("assignee") or {}
    info.update({
        "status": (fields.get("status") or {}).get("name", "N/A"),
        "summary": str(fields.get("summary", ""))[:80],
        "assignee": assignee.get("displayName", "Unassigned") if assignee else "Unassigned",
        "updated": str(fields.get("updated", ""))[:10],
    })
    comments_data = _jira_get(f"/rest/api/2/issue/{ticket_key}/comment?maxResults=10&startAt=0")
    if comments_data:
        info["comment_count"] = int(comments_data.get("total", 0))
        raw_comments = comments_data.get("comments", [])
        for c in raw_comments[-10:]:
            body = c.get("body", "")
            clean = re.sub(r"<[^>]+>", "", body)[:600].strip()
            info["comments"].append({
                "author": (c.get("author") or {}).get("displayName", "?"),
                "created": str(c.get("created", ""))[:10],
                "body": clean,
            })
    return info


def _build_comments_for_topic(topic: str, market_entries: list) -> list[dict]:
    """Fetch info for all market entries of a topic, using threading for speed"""
    results = []

    def fetch_one(entry: tuple) -> dict:
        market = entry[0]
        parent_key = entry[1]
        domain_key = entry[2] if len(entry) > 2 else None
        layer3_key = entry[3] if len(entry) > 3 else None
        row = {
            "market": market,
            "parent": parent_key,
            "domain": domain_key or "",
            "layer3": layer3_key or "",
            "status": "N/A",
            "summary": "",
            "assignee": "",
            "updated": "",
            "comment_count": 0,
            "comments": [],
        }
        if domain_key:
            dk_info = _fetch_ticket_info(domain_key)
            if dk_info.get("comment_count", 0) > 0:
                row.update({k: dk_info[k] for k in ("status", "summary", "assignee", "updated", "comment_count", "comments")})
        elif parent_key:
            parent_info = _fetch_ticket_info(parent_key)
            if parent_info.get("comment_count", 0) > 0:
                row.update({k: parent_info[k] for k in ("status", "summary", "assignee", "updated", "comment_count", "comments")})
        return row

    threads = []
    lock = threading.Lock()
    def worker(entry):
        r = fetch_one(entry)
        with lock:
            results.append(r)
    for entry in market_entries:
        t = threading.Thread(target=worker, args=(entry,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join(timeout=30)
    return results


def _llm_topic_summary(label: str, markets: list) -> str:
    """Generate a structured Chinese summary for a topic domain via LLM.
    Falls back to a deterministic summary if LLM is unavailable."""
    try:
        cfg = load_config()
        llm = cfg.get("llm", {}) if isinstance(cfg.get("llm", {}), dict) else {}
        api_key = llm.get("api_key", "") or os.environ.get("LLM_API_KEY", "")
        base_url = llm.get("base_url", "https://llm-gateway.dev.cn-vwa.volkswagen-cea.com/v1")
        model = llm.get("model", "MiniMax")
        if not api_key:
            return _fallback_topic_summary(label, markets)
        import urllib.request
        import urllib.error

        market_lines = []
        for m in markets:
            status = m.get("status", "N/A")
            assignee = m.get("assignee", "Unassigned")
            comments = m.get("comments", [])
            comment_txt = ""
            if comments:
                last = comments[-1]
                comment_txt = f" 最新评论[{last.get('created', '')}] {last.get('author', '')}: {last.get('body', '')[:200]}"
            market_lines.append(f"- {m.get('market', '?')} ({m.get('parent', '')}/{m.get('layer3', '')}): 状态={status} 负责人={assignee}{comment_txt}")

        prompt = (
            f"你是汽车出口市场Layer3合规分析专家。请基于以下各市场【{label}】领域的Jira工单状态与最新评论，"
            f"输出一份简洁的中文分析摘要，格式如下（严格按此格式，不要额外内容）：\n"
            f"【总体判断】1-2句话概括该领域整体进展\n"
            f"【各市场状态】逐市场一句话说明进展/风险\n"
            f"【风险与阻塞】列出仍开放或阻塞的关键事项及原因\n"
            f"【建议行动】列出下阶段应做的具体行动\n"
            f"要求：必须基于给定数据，不要编造；没有数据支撑的请注明\"数据不足\"。\n\n"
            f"数据：\n" + "\n".join(market_lines)
        )

        data = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个严谨的汽车法规合规分析助手，只依据给定数据进行分析，不编造事实。请用中文回答。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 800,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=data,
            headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=25) as resp:
            result = json.loads(resp.read().decode("utf-8", errors="replace"))
        return str(result["choices"][0]["message"]["content"]).strip()
    except Exception as e:
        print(f"[topic_comments] LLM summary failed for {label}: {e}")
        return _fallback_topic_summary(label, markets)


def _fallback_topic_summary(label: str, markets: list) -> str:
    """Deterministic rule-based summary when LLM is unavailable"""
    lines = []
    closed = [m["market"] for m in markets if "closed" in str(m.get("status", "")).lower() or "done" in str(m.get("status", "")).lower()]
    open_mk = [m["market"] for m in markets if str(m.get("status", "")).strip() not in ("", "N/A", "ERROR") and "closed" not in str(m.get("status", "")).lower() and "done" not in str(m.get("status", "")).lower()]
    lines.append(f"【{label}】共{len(markets)}个市场工单")
    if closed:
        lines.append(f"已完成/关闭: {', '.join(closed)}")
    if open_mk:
        lines.append(f"进行中/待处理: {', '.join(open_mk)}")
    if not closed and not open_mk:
        lines.append("暂无有效状态数据")
    return "\n".join(lines)


def _llm_market_gap_verdict(market: str, label: str, comments: list, jira_status: str) -> tuple[str, str]:
    """Use LLM to determine per-market gap analysis status from comments.
    Returns (status, conclusion): 'gap_analysis'/'evaluating'/'pending', with a brief conclusion."""
    try:
        cfg = load_config()
        llm = cfg.get("llm", {}) if isinstance(cfg.get("llm", {}), dict) else {}
        api_key = llm.get("api_key", "") or os.environ.get("LLM_API_KEY", "")
        base_url = llm.get("base_url", "https://llm-gateway.dev.cn-vwa.volkswagen-cea.com/v1")
        model = llm.get("model", "MiniMax")
        if not api_key:
            return _rule_market_status(jira_status, comments)

        if not comments:
            return "pending", "无评论"

        last_n = comments[-5:]
        comment_lines = []
        for c in last_n:
            ts = str(c.get("created", ""))[:10]
            author = str(c.get("author", "?"))
            body = str(c.get("body", ""))[:400].replace("\n", " ").strip()
            comment_lines.append(f"[{ts} {author}] {body}")

        prompt = (
            f"你是汽车出口市场Gap分析审查专家。请分析市场'{market}'的{label}领域Jira评论，判断Gap分析是否已有明确结论。\n"
            f"Jira票状态: {jira_status}\n"
            f"最近评论（按时间倒序）：\n" + "\n".join(comment_lines) + "\n\n"
            f"请严格按以下格式输出（一行，英文分号分隔，中文字）：\n"
            f"结论:是/否; 总结:一句话说明结论内容（30字内）\n"
            f"判断标准：\n"
            f"- 有明确法规差距说明或合规结论 → 结论:是\n"
            f"- 只有进度更新/问题讨论/待确认 → 结论:否\n"
            f"- 无实质评论 → 结论:否\n"
            f"示例输出：结论:是; 总结:无Gap，合规。 | 结论:否; 总结:等待供应商反馈"
        )

        data = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个严谨的法规合规审查助手，只依据评论内容进行判断，不编造。用中文输出。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
            "max_tokens": 120,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=data,
            headers={"Authorization": "Bearer " + api_key, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            result = json.loads(resp.read().decode("utf-8", errors="replace"))
        content = str(result["choices"][0]["message"]["content"]).strip()

        has_conclusion = False
        summary = ""
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("结论:"):
                has_conclusion = "结论:是" in line or "结论: Yes" in line.lower()
            if line.startswith("总结:"):
                summary = line.replace("总结:", "").strip().rstrip(";.,，")
        if has_conclusion:
            return "gap_analysis", summary[:100] if summary else "Gap分析明确"
        return "evaluating", summary[:100] if summary else "评论分析进行中"
    except Exception as e:
        print(f"[market_verdict] LLM failed for {market}/{label}: {e}")
        return _rule_market_status(jira_status, comments)


def _rule_market_status(jira_status: str, comments: list) -> tuple[str, str]:
    """Fallback rule-based status when LLM unavailable"""
    status_lower = jira_status.lower().strip()
    if not comments:
        return "pending", "无评论"
    if "closed" in status_lower or "done" in status_lower:
        return "gap_analysis", f"票已关闭，{len(comments)}条评论"
    comment_text = " ".join(c.get("body", "") for c in comments).lower()
    conclusion_kw = [
        "无gap", "no gap", "无差异", "compliant", "合规", "已评估", "已确认",
        "confirmed", "assessed", "baseload", "已覆盖", "covered",
        "结论", "gap已确认", "已完成评估", "评估完成",
        "no further action", "no action required", "not applicable",
    ]
    progress_kw = ["waiting", "等待", "ongoing", "进行中", "in progress", "pending", "待确认", "待反馈", "待回复"]
    has_conclusion = any(kw in comment_text for kw in conclusion_kw)
    has_progress = any(kw in comment_text for kw in progress_kw)
    count = len(comments)
    if count >= 5 and has_conclusion:
        return "gap_analysis", f"结论明确（{count}条评论）"
    if count >= 3:
        return "evaluating", f"评估中（{count}条评论）"
    if has_progress:
        return "evaluating", f"评估进行中（{count}条评论）"
    if count > 0:
        return "evaluating", f"有评论待分析（{count}条）"
    return "pending", "无评论"


def _analyze_market_gap(row: dict, label: str) -> tuple[str, str]:
        """Analyze single market's comments to determine status and gap summary.
        Returns (status, gap_summary).
        Status rules (checked in order):
        1. Jira ticket Canceled -> 'not_applicable' (不涉及)
        2. Jira ticket Closed/Done -> 'gap_analysis' (已关闭即已有结论)
        3. No comments -> 'pending'
        4. Else: LLM/rule analysis of comments -> 'evaliing' or 'gap_analysis'"""
        jira_status = str(row.get("status", "")).strip().lower()
        if jira_status in ("canceled", "cancelled", "取消", "closed", "done", "完成"):
            if "cancel" in jira_status:
                return "not_applicable", "子票已取消"
            return "gap_analysis", "评论已关闭"
        if not row.get("comments"):
            return "pending", "无评论"
        return _llm_market_gap_verdict(
            market=row.get("market", ""),
            label=label,
            comments=row.get("comments", []),
            jira_status=row.get("status", ""),
        )


def _analyze_markets_concurrent(market_rows: list, label: str) -> dict[str, tuple[str, str]]:
    """Analyze all markets concurrently using LLM.
    Returns dict: market_name -> (status, gap_summary)"""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    results: dict[str, tuple[str, str]] = {}

    def analyze_one(row: dict) -> tuple[str, str, str]:
        status, gap_sum = _analyze_market_gap(row, label)
        return row.get("market", ""), status, gap_sum

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(analyze_one, row): row for row in market_rows}
        for future in as_completed(futures, timeout=180):
            try:
                mkt, status, gap_sum = future.result()
                if mkt:
                    results[mkt] = (status, gap_sum)
            except Exception as e:
                row = futures[future]
                print(f"[analyze_markets] Error: {e}")
                mkt = row.get("market", "")
                if mkt:
                    results[mkt] = ("evaluating", "分析异常")
    for row in market_rows:
        mkt = row.get("market", "")
        if mkt and mkt not in results:
            results[mkt] = ("pending", "")
    return results


def build_topic_comments_report(topic: str = "") -> dict:
    """Build topic comments report for one topic or all topics.
    Per-market status is determined by LLM analysis of actual comments content."""
    topics_to_fetch = list(TOPIC_CONFIG.keys()) if not topic else [topic]
    all_results = {}
    for t in topics_to_fetch:
        cfg = TOPIC_CONFIG.get(t, {})
        entries = cfg.get("tickets", [])
        label = cfg.get("label", t)
        market_rows = _build_comments_for_topic(t, entries)
        total_comments = sum(r["comment_count"] for r in market_rows)
        summary = _llm_topic_summary(label, market_rows)
        all_results[t] = {
            "label": label,
            "icon": cfg.get("icon", ""),
            "total_tickets": len(market_rows),
            "total_comments": total_comments,
            "summary": summary,
            "markets": market_rows,
        }
        verdict_results = _analyze_markets_concurrent(market_rows, label)
        for row in market_rows:
            ticket = row.get("domain") or row.get("layer3") or row.get("parent") or ""
            market_name = row.get("market", "")
            if not market_name:
                continue
            status, gap_sum = verdict_results.get(market_name, ("pending", ""))
            if status in ("gap_analysis", "not_applicable"):
                _ensure_gap_table()
                label_status = "not_applicable" if status == "not_applicable" else "gap_analysis"
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                current_count = row.get("comment_count", 0)
                with sqlite3.connect(DB_PATH) as conn:
                    existing = conn.execute(
                        "SELECT manual_override, manual_comment_count FROM gap_market_tracking WHERE market=? AND topic=?",
                        (market_name, t),
                    ).fetchone()
                    if existing and existing[0] and existing[1] >= 0 and current_count <= existing[1]:
                        continue
                    conn.execute("""
                        INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 0, -1)
                        ON CONFLICT(market, topic) DO UPDATE SET
                            ticket=excluded.ticket, status=excluded.status,
                            comments_total=excluded.comments_total,
                            gap_summary=excluded.gap_summary,
                            updated_at=excluded.updated_at
                    """, (market_name, t, ticket, label_status, current_count, gap_sum, now))
            elif status == "evaluating":
                _ensure_gap_table()
                now = time.strftime("%Y-%m-%d %H:%M:%S")
                current_count = row.get("comment_count", 0)
                with sqlite3.connect(DB_PATH) as conn:
                    existing = conn.execute(
                        "SELECT manual_override, manual_comment_count FROM gap_market_tracking WHERE market=? AND topic=?",
                        (market_name, t),
                    ).fetchone()
                    if existing and existing[0] and existing[1] >= 0 and current_count <= existing[1]:
                        continue
                    conn.execute("""
                        INSERT INTO gap_market_tracking (market, topic, ticket, status, comments_total, gap_summary, updated_at, manual_override, manual_comment_count)
                        VALUES (?, ?, ?, 'evaluating', ?, '', ?, 0, -1)
                        ON CONFLICT(market, topic) DO UPDATE SET
                            ticket=excluded.ticket, status='evaluating',
                            comments_total=excluded.comments_total, updated_at=excluded.updated_at
                    """, (market_name, t, ticket, row.get("comment_count", 0), now))
            else:
                _mark_market_topic_pending(market_name, t)
    return {"ok": True, "topic": topic or "all", "topics": all_results}


def run_analysis_action(action: str, body: dict | None = None) -> dict:
    """Run an analysis script from 00-analysis module"""
    try:
        if action == "topic_comments":
            topic = str((body or {}).get("topic", "")).strip() if body else ""
            return build_topic_comments_report(topic)

        action_map = {
            "deep_jira": "deep_jira_analysis.py",
            "market_overview": "comprehensive_analysis.py",
            "obd_data": "verify_obd_data.py",
            "cyber_security": "verify_cyber_security.py",
            "layer3_excel": "create_excel_final.py",
            "fusa_data": "verify_fusa.py",
            "ota_data": "verify_ota.py",
            "immobilizer_data": "verify_immobilizer.py",
        }
        
        script_name = action_map.get(action)
        if not script_name:
            return {"error": f"Unknown analysis action: {action}", "available": list(action_map.keys())}
        
        script_path = ANALYSIS_SCRIPTS / script_name
        if not script_path.exists():
            return {"error": f"Script not found: {script_path}"}
        
        # Run the script and capture output
        result = subprocess.run(
            [PYTHON, str(script_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
            cwd=str(ANALYSIS_SCRIPTS)
        )
        
        output = result.stdout if result.stdout else result.stderr if result.stderr else ""
        if not output.strip():
            output = f"[完成] {script_name} 执行成功（无输出）"
        
        return {"output": output, "returncode": result.returncode, "script": script_name}
    except subprocess.TimeoutExpired:
        return {"error": "分析超时（120秒）"}
    except Exception as e:
        return {"error": str(e)}


def get_chat_sessions() -> list:
    """Get all chat sessions"""
    try:
        if CHAT_SESSIONS_FILE.exists():
            sessions = json.loads(CHAT_SESSIONS_FILE.read_text(encoding="utf-8"))
            return sorted(sessions, key=lambda x: x.get("updated_at", ""), reverse=True)
        return []
    except Exception:
        return []

def get_chat_messages(session_id: str = None, limit: int = 50) -> list:
    """Get chat messages for a session"""
    try:
        if CHAT_MEMORY_FILE.exists():
            memory = json.loads(CHAT_MEMORY_FILE.read_text(encoding="utf-8"))
            if session_id:
                messages = [m for m in memory.get("messages", []) if m.get("session_id") == session_id]
            else:
                messages = memory.get("messages", [])
            return messages[-limit:]
        return []
    except Exception:
        return []

def save_chat_message(session_id: str, role: str, content: str, metadata: dict = None) -> dict:
    """Save a chat message to memory"""
    try:
        memory = {"messages": [], "sessions": {}}
        if CHAT_MEMORY_FILE.exists():
            memory = json.loads(CHAT_MEMORY_FILE.read_text(encoding="utf-8"))
        
        message = {
            "id": f"msg_{len(memory.get('messages', [])) + 1:05d}",
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "metadata": metadata or {}
        }
        
        memory.setdefault("messages", []).append(message)
        memory.setdefault("sessions", {})
        memory["sessions"][session_id] = memory["sessions"].get(session_id, {})
        memory["sessions"][session_id]["updated_at"] = message["timestamp"]
        memory["sessions"][session_id]["last_message"] = content[:100]
        
        CHAT_MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        CHAT_MEMORY_FILE.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")
        
        return {"ok": True, "message": message}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def create_chat_session(title: str = None) -> dict:
    """Create a new chat session"""
    try:
        sessions = []
        if CHAT_SESSIONS_FILE.exists():
            sessions = json.loads(CHAT_SESSIONS_FILE.read_text(encoding="utf-8"))
        
        session_id = f"session_{time.strftime('%Y%m%d_%H%M%S')}"
        new_session = {
            "id": session_id,
            "title": title or f"对话 {time.strftime('%m-%d %H:%M')}",
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "message_count": 0,
            "tags": []
        }
        
        sessions.insert(0, new_session)
        sessions = sessions[:50]
        
        CHAT_SESSIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        CHAT_SESSIONS_FILE.write_text(json.dumps(sessions, ensure_ascii=False, indent=2), encoding="utf-8")
        
        return {"ok": True, "session": new_session}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def delete_chat_session(session_id: str) -> dict:
    """Delete a chat session and its messages"""
    try:
        sessions = []
        if CHAT_SESSIONS_FILE.exists():
            sessions = json.loads(CHAT_SESSIONS_FILE.read_text(encoding="utf-8"))
        
        sessions = [s for s in sessions if s.get("id") != session_id]
        CHAT_SESSIONS_FILE.write_text(json.dumps(sessions, ensure_ascii=False, indent=2), encoding="utf-8")
        
        memory = {"messages": [], "sessions": {}}
        if CHAT_MEMORY_FILE.exists():
            memory = json.loads(CHAT_MEMORY_FILE.read_text(encoding="utf-8"))
        
        memory["messages"] = [m for m in memory.get("messages", []) if m.get("session_id") != session_id]
        memory["sessions"].pop(session_id, None)
        CHAT_MEMORY_FILE.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")
        
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def chat_with_llm(session_id: str, user_message: str) -> dict:
    """Send user message to LLM and get response. Detects email intents and augments with real data."""
    # Intercept email intents first - run tool, pass result to LLM
    intent_result = assistant_intent_router(user_message)
    
    cfg = load_config()
    llm = cfg.get("llm", {}) if isinstance(cfg.get("llm", {}), dict) else {}

    try:
        api_key = llm.get("api_key", "") or os.environ.get("LLM_API_KEY", "")
        base_url = llm.get("base_url", "https://llm-gateway.dev.cn-vwa.volkswagen-cea.com/v1")
        model = llm.get("model", "MiniMax")

        if not api_key:
            return {"ok": False, "error": "LLM API key not configured"}

        # Get chat history for context
        history = get_chat_messages(session_id, limit=10)

        # Build messages array
        system_prompt = """你是一个专业的汽车法规工程师助手，帮助用户处理：
1. 出口市场Layer3合规问题（Cyber Security, Data Security, OTA, OBD等）
2. Jira工单查询和分析
3. 法规Wiki知识库检索
4. PSV表格解析和评估
5. 邮件处理和报告生成
6. CEADU工单相关问题
7. Outlook邮件操作（查看、搜索、回复）

**邮件助手能力**：
- 当用户说"最新邮件"/"最近邮件"/"看看邮件"时 → 自动查询最新邮件
- 当用户说"搜索邮件"/"查找邮件"时 → 自动搜索邮件
- 当用户说"需要回复"/"待回复"时 → 检查需要回复的邮件
- 当用户说"联系人"/"查邮箱"时 → 搜索联系人邮箱
- 当用户说"昨天邮件"/"简报"时 → 获取昨日邮件简报

**关键出口市场**: Korea, ASEAN RHD/LHD, India, Middle East, Kazakhstan, Uzbekistan, Turkey, AUS/NZL
**关键法规**: UN-R155 (Cyber Sec), UN-R156 (OTA), PDPA (Data Sec), PIPA (Korea Privacy)

请用中文回答。如果邮件助手已提供真实数据，请直接引用并总结给用户。"""

        messages = [{"role": "system", "content": system_prompt}]

        # Inject tool result as system message if intent was handled
        if intent_result.get("handled"):
            tool_context = (
                f"[邮件助手执行结果]\n"
                f"操作类型: {intent_result.get('intent', 'N/A')}\n"
                f"执行结果:\n{intent_result.get('result', 'N/A')}\n\n"
                f"请基于以上真实数据，用中文简洁地回答用户的问题。"
            )
            messages.append({"role": "system", "content": tool_context})

        for msg in history[-6:]:
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })

        messages.append({"role": "user", "content": user_message})

        # Call LLM API
        import urllib.request
        import urllib.error

        data = json.dumps({
            "model": model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

            if "choices" in result and len(result["choices"]) > 0:
                assistant_content = result["choices"][0]["message"]["content"]

                # Save user message (only the original part, not knowledge context)
                original_msg = user_message.split("\n\n参考知识库:")[0] if "\n\n参考知识库:" in user_message else user_message
                save_chat_message(session_id, "user", original_msg)

                # Save assistant message
                save_chat_message(session_id, "assistant", assistant_content)

                # Update session
                sessions = get_chat_sessions()
                for s in sessions:
                    if s["id"] == session_id:
                        s["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        s["message_count"] = s.get("message_count", 0) + 2
                        break
                CHAT_SESSIONS_FILE.write_text(json.dumps(sessions, ensure_ascii=False, indent=2), encoding="utf-8")

                return {
                    "ok": True,
                    "response": assistant_content,
                    "intent_handled": intent_result.get("handled", False),
                    "intent": intent_result.get("intent"),
                    "tool_result": intent_result.get("result") if intent_result.get("handled") else None,
                    "usage": result.get("usage", {})
                }
            else:
                return {"ok": False, "error": "LLM返回格式错误"}

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"ok": False, "error": f"LLM API错误: {e.code} - {error_body[:200]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def search_knowledge_base(query: str) -> list:
    """Search the knowledge base (Wiki) for relevant information"""
    try:
        # Search wiki
        wiki_result = wiki_search(query, limit=5, include_raw=False)
        
        # Search memory
        from memory.memory_service import WorkflowMemory
        memory_db = APP_ROOT / "runtime" / "memory.sqlite"
        if memory_db.exists():
            wf_memory = WorkflowMemory(memory_db)
            similar = wf_memory.find_similar_question(query)
            wf_memory.close()
            
            if similar:
                return {
                    "wiki_hits": wiki_result.get("hits", []),
                    "memory_hint": {
                        "question": similar["question"],
                        "answer": similar["answer"],
                        "similarity": similar["similarity"]
                    }
                }
        
        return {"wiki_hits": wiki_result.get("hits", []), "memory_hint": None}
    except Exception as e:
        return {"wiki_hits": [], "memory_hint": None, "error": str(e)}

def main() -> int:
    host = os.environ.get("DEMO_HOST", "0.0.0.0")
    port = int(os.environ.get("DEMO_PORT", "7860"))
    server = ThreadingHTTPServer((host, port), DemoHandler)
    print(f"G.R.C. Agent running at http://{host}:{port}")
    print(f"API endpoint: http://{host}:{port}/api/export-markets/data")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
