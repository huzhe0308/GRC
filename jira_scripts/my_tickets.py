#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA - 获取当前用户未解决的 tickets
"""
import requests
import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from config import JIRA_URL, JIRA_TOKEN

def get_my_tickets():
    """获取当前用户未解决的 tickets"""
    if not JIRA_TOKEN:
        print("Error: JIRA_TOKEN not configured")
        return None
    
    session = requests.Session()
    session.get(f"{JIRA_URL}/login.jsp", timeout=30)
    
    headers = {
        'Authorization': f'Bearer {JIRA_TOKEN}',
        'Accept': 'application/json'
    }
    
    resp = session.get(f"{JIRA_URL}/rest/api/2/myself", headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"Error: {resp.status_code} - {resp.text[:200]}")
        return None
    
    user = resp.json()
    print(f"=== User: {user.get('displayName')} ===\n")
    
    jql = "assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC, updated DESC"
    url = f"{JIRA_URL}/rest/api/2/search?jql={requests.utils.quote(jql)}&maxResults=50"
    url += "&fields=summary,status,priority,project,issuetype,created,updated"
    
    resp = session.get(url, headers=headers, timeout=30)
    if resp.status_code != 200:
        print(f"Search Error: {resp.status_code}")
        return None
    
    data = resp.json()
    issues = data.get('issues', [])
    
    print(f"=== Found {len(issues)} open tickets ===\n")
    
    for issue in issues:
        key = issue.get('key')
        fields = issue.get('fields', {})
        summary = fields.get('summary', '')[:60]
        status = fields.get('status', {}).get('name', '')
        priority = fields.get('priority', {}).get('name', '')
        issue_type = fields.get('issuetype', {}).get('name', '')
        print(f"[{key}] {issue_type} - {priority}")
        print(f"  {summary}")
        print(f"  Status: {status}\n")
    
    return data

def main():
    data = get_my_tickets()
    
    if data:
        skill_output = os.path.join(os.path.dirname(__file__), '..', 'my_tickets.json')
        with open(skill_output, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nSaved to {skill_output}")

        try:
            desktop_output = os.path.join(os.path.expandvars(r'%USERPROFILE%\Desktop\connect'), 'jira_tickets_memory.json')
            desktop_dir = os.path.dirname(desktop_output)
            if os.path.exists(desktop_dir):
                with open(desktop_output, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"Also saved to {desktop_output}")
        except Exception:
            pass

if __name__ == '__main__':
    main()
