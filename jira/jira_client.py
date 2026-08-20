import os
import re
import time
from typing import Any, Optional
import requests
from requests.auth import HTTPBasicAuth


class JiraClient:
    def __init__(self, config: dict[str, Any]):
        self.url = str(config.get("url", "")).rstrip("/")
        self.timeout = int(config.get("timeout_seconds", 30))
        self.default_project = str(config.get("default_project", "CEADU"))
        self.max_results = int(config.get("max_results", 50))
        self.token = str(config.get("token", ""))
        
        self.session = requests.Session()
        self.session.proxies = {'http': None, 'https': None}
        self.session.get(f"{self.url}/login.jsp", timeout=self.timeout)
        
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        })

    def _get(self, endpoint: str, params: dict = None) -> dict | list | None:
        try:
            url = f"{self.url}/rest/api/3/{endpoint.lstrip('/')}"
            resp = self.session.get(url, params=params, timeout=self.timeout)
            if resp.status_code == 200:
                return resp.json()
            print(f"JIRA API error: {resp.status_code} - {resp.text[:200]}")
        except Exception as e:
            print(f"JIRA request failed: {e}")
        return None

    def get_issue(self, issue_key: str) -> dict | None:
        issue_key = issue_key.upper().strip()
        if not re.match(r"^[A-Z]+-\d+$", issue_key):
            return None
        return self._get(f"issue/{issue_key}")

    def get_issue_comments(self, issue_key: str) -> list[dict]:
        result = self._get(f"issue/{issue_key}/comment", {"maxResults": 100})
        return result.get("comments", []) if result else []

    def search_issues(self, jql: str = None, **kwargs) -> list[dict]:
        params = {
            "maxResults": self.max_results,
            "fields": "summary,status,assignee,reporter,created,updated,description,comment",
            **kwargs
        }
        if jql:
            params["jql"] = jql
        result = self._get("search", params)
        return result.get("issues", []) if result else []

    def get_my_issues(self, status: str = None) -> list[dict]:
        jql_parts = ['assignee = currentUser()']
        if status:
            jql_parts.append(f'status = "{status}"')
        jql = " AND ".join(jql_parts) + " ORDER BY updated DESC"
        return self.search_issues(jql=jql)

    def add_comment(self, issue_key: str, body: str) -> dict | None:
        url = f"{self.url}/rest/api/3/issue/{issue_key}/comment"
        try:
            resp = self.session.post(url, json={"body": body}, timeout=self.timeout)
            if resp.status_code in (200, 201):
                return resp.json()
            print(f"Add comment failed: {resp.status_code}")
        except Exception as e:
            print(f"Add comment error: {e}")
        return None

    def get_project_issues(self, project: str = None, status: str = None) -> list[dict]:
        project = project or self.default_project
        jql_parts = [f'project = "{project}"']
        if status:
            jql_parts.append(f'status = "{status}"')
        jql = " AND ".join(jql_parts) + " ORDER BY updated DESC"
        return self.search_issues(jql=jql)

    def transition_issue(self, issue_key: str, transition_name: str) -> bool:
        transitions = self._get(f"issue/{issue_key}/transitions")
        if not transitions:
            return False
        for t in transitions.get("transitions", []):
            if t["name"].lower() == transition_name.lower():
                url = f"{self.url}/rest/api/3/issue/{issue_key}/transitions"
                try:
                    resp = self.session.post(url, json={"transition": {"id": t["id"]}}, timeout=self.timeout)
                    return resp.status_code in (200, 204)
                except Exception as e:
                    print(f"Transition error: {e}")
                    return False
        return False


def extract_issue_keys(text: str) -> list[str]:
    pattern = r"([A-Z]+-\d+)"
    return list(set(re.findall(pattern, text.upper()())))


def format_issue_summary(issue: dict) -> str:
    if not issue:
        return ""
    fields = issue.get("fields", {})
    key = issue.get("key", "")
    summary = fields.get("summary", "N/A")
    status = fields.get("status", {}).get("name", "N/A")
    assignee = fields.get("assignee", {})
    assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
    created = fields.get("created", "")[:10]
    return f"[{key}] {summary}\n状态: {status} | 负责人: {assignee_name} | 创建: {created}"


def create_jira_client(config: dict[str, Any]) -> Optional[JiraClient]:
    jira_config = config.get("jira", {})
    if not jira_config.get("enabled", False):
        return None
    try:
        return JiraClient(jira_config)
    except Exception as e:
        print(f"Failed to create JIRA client: {e}")
        return None
