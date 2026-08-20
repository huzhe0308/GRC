import json
import os
import sys
import io
import subprocess
import re
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

if hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

SCRIPT_DIR = Path(__file__).parent
OPENCODE_CONFIG = Path.home() / ".config" / "opencode"
SKILL_DIR = OPENCODE_CONFIG / "skills" / "Jira_access_enhanced" / "scripts"
SKILL_CACHE = OPENCODE_CONFIG / "skills" / "Jira_access_enhanced" / "my_tickets.json"
OPENCODE_CMD = "opencode"  # or full path to opencode executable

class JiraIntegration:
    def __init__(self, config: dict[str, Any]):
        self.config = config
        self.jira_config = config.get("jira", {})
        self.url = self.jira_config.get("url", "https://devstack.vgc.com.cn/jira")
        self.token = self.jira_config.get("token", "")
        self.project = self.jira_config.get("default_project", "CEADU")
        self._ensure_config()
    
    def _ensure_config(self):
        config_file = SCRIPT_DIR / ".jira_config"
        if not config_file.exists():
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(f"JIRA_URL={self.url}\n")
                f.write(f"JIRA_TOKEN={self.token}\n")
    
    def _run_skill_script(self, script_name: str, args: list[str] = None) -> dict | None:
        script_path = SKILL_DIR / script_name
        if not script_path.exists():
            script_path = SCRIPT_DIR / script_name
        if not script_path.exists():
            print(f"Script not found: {script_name}")
            return None
        
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=60)
            return {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode}
        except subprocess.TimeoutExpired:
            return {"error": "Timeout", "stdout": "", "stderr": "Script timed out", "returncode": -1}
        except Exception as e:
            return {"error": str(e), "stdout": "", "stderr": "", "returncode": -1}
    
    def get_my_tickets(self, force_refresh: bool = False) -> list[dict]:
        cache_file = Path("runtime/jira_cache.json")
        
        if SKILL_CACHE.exists():
            with open(SKILL_CACHE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("issues", [])
        
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("issues", [])
        
        return []
    
    def get_cea_layer3_tickets(self) -> list[dict]:
        """获取CEADU Layer3相关工单：直接分配的Layer3票 + 上级大票的Data Security/Cyber Security subtask"""
        all_issues = []
        
        if SKILL_CACHE.exists():
            with open(SKILL_CACHE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_issues = data.get("issues", [])
        
        if not all_issues:
            cache_file = Path("runtime/jira_cache.json")
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    all_issues = data.get("issues", [])
        
        # Layer3 Topics
        layer3_topics = ["Functional Safety", "Data Security", "Cyber Security", "OBD", "OTA", "Software Update", "Diagnostics", "Network", "Net Work"]
        
        result = []
        layer3_parent_keys = set()
        
        for issue in all_issues:
            fields = issue.get("fields", {})
            project_key = fields.get("project", {}).get("key", "")
            summary = fields.get("summary", "")
            parent_id = fields.get("parent", {}).get("key", "")
            
            # 1. CEADU Layer3 直接工单
            if project_key == "CEADU" and ("Layer3" in summary or any(topic in summary for topic in layer3_topics)):
                result.append({
                    **issue,
                    "_category": "layer3_direct",
                    "_display_title": f"[Layer3] {issue.get('key')}"
                })
                if parent_id:
                    layer3_parent_keys.add(parent_id)
                elif not parent_id:
                    layer3_parent_keys.add(issue.get("key"))
            
            # 2. Data Security / Cyber Security subtask（来自Layer3父工单）
            elif parent_id in layer3_parent_keys and ("Data Security" in summary or "Cyber Security" in summary):
                result.append({
                    **issue,
                    "_category": "security_subtask",
                    "_display_title": f"[安全] {issue.get('key')}"
                })
        
        return result
    
    def get_cea_layer3_jql(self) -> str:
        """生成Layer3相关工单的JQL查询"""
        return '''project = CEADU AND (
  summary ~ "Layer3" AND assignee = currentUser()
) OR (
  parent IN (
    SELECT parent FROM issue 
    WHERE project = CEADU AND summary ~ "Layer3" AND assignee = currentUser()
  ) AND (
    summary ~ "Data Security" OR summary ~ "Cyber Security"
  )
)
ORDER BY updated DESC'''
    
    def _fetch_via_opencode_skill(self) -> list[dict]:
        """Fetch tickets via opencode subagent with JIRA skill - requires user to run opencode first"""
        skill_cache = Path(SKILL_DIR.parent / "my_tickets.json")
        if skill_cache.exists():
            mod_time = datetime.fromtimestamp(skill_cache.stat().st_mtime)
            age_minutes = (datetime.now() - mod_time).total_seconds() / 60
            if age_minutes < 60:
                with open(skill_cache, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get("issues", [])
        return []
    
    def search_tickets(self, jql: str, fields: str = None) -> list[dict]:
        cache_file = Path("runtime/jira_cache.json")
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                issues = data.get("issues", [])
                if not fields:
                    return issues
        
        result = self._run_skill_script("search_tickets.py", [jql])
        if result and result.get("returncode") == 0:
            return result.get("stdout", "")
        return result.get("stderr", "")
    
    def get_issue(self, issue_key: str, include_attachments: bool = False) -> dict | None:
        import requests
        session = requests.Session()
        try:
            session.get(f'{self.url}/login.jsp', timeout=30)
        except:
            pass
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
        }
        
        # Build fields parameter
        fields_param = "summary,status,parent,priority,assignee,attachment"
        if not include_attachments:
            fields_param = "summary,status,parent,priority,assignee"
        
        try:
            resp = session.get(f'{self.url}/rest/api/2/issue/{issue_key}?fields={fields_param}', headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()
        except:
            pass
        result = self._run_skill_script("get_ticket.py", [issue_key])
        if result and result.get("returncode") == 0:
            try:
                stdout = result.get("stdout", "")
                import re
                json_match = re.search(r'\{.*?"key".*?\}', stdout, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
            except:
                pass
        return None
    
    def get_issue_comments(self, issue_key: str) -> list[dict]:
        """Get comments for a Jira issue"""
        import requests
        session = requests.Session()
        try:
            session.get(f'{self.url}/login.jsp', timeout=30)
        except:
            pass
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
        }
        try:
            resp = session.get(f'{self.url}/rest/api/2/issue/{issue_key}/comment', headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data.get('comments', [])
        except:
            pass
        return []
    
    def get_issue_with_comments(self, issue_key: str) -> dict | None:
        """Get issue with comments included"""
        issue = self.get_issue(issue_key)
        if issue:
            issue['_comments'] = self.get_issue_comments(issue_key)
        return issue
    
    def update_status(self, issue_key: str, transition_id: str) -> bool:
        result = self._run_skill_script("update_status.py", [issue_key, "--transition", transition_id])
        return result and result.get("returncode") == 0
    
    def get_transitions(self, issue_key: str) -> list[dict]:
        result = self._run_skill_script("update_status.py", [issue_key, "--transitions"])
        if result and result.get("returncode") == 0:
            return result.get("stdout", "")
        return []
    
    def add_comment(self, issue_key: str, comment: str) -> bool:
        script = f'''
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
os.environ['NO_PROXY'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
os.environ['no_proxy'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
import requests

JIRA_URL = 'https://devstack.vgc.com.cn/jira'
JIRA_TOKEN = '{self.token}'

session = requests.Session()
session.get(f'{{JIRA_URL}}/login.jsp', timeout=30, proxies={{'http': None, 'https': None}})

headers = {{
    'Authorization': f'Bearer {{JIRA_TOKEN}}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}}

data = {{"body": "{comment}"}}
resp = session.post(f'{{JIRA_URL}}/rest/api/2/issue/{{issue_key}}/comment', json=data, headers=headers, timeout=30, proxies={{'http': None, 'https': None}})
print(resp.status_code)
'''
        result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True, encoding='utf-8', timeout=30)
        return "201" in result.stdout or "204" in result.stdout
    
    def format_ticket_summary(self, issue: dict) -> str:
        key = issue.get("key", "N/A")
        fields = issue.get("fields", {})
        summary = fields.get("summary", "N/A")
        status = fields.get("status", {}).get("name", "N/A")
        priority = fields.get("priority", {}).get("name", "N/A")
        assignee = fields.get("assignee", {})
        assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
        return f"[{key}] {summary}\nStatus: {status} | Priority: {priority} | Assignee: {assignee_name}"


def create_jira_integration(config: dict[str, Any]) -> JiraIntegration:
    return JiraIntegration(config)
