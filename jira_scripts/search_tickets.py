#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA - 搜索 tickets
"""
import requests
import json
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from config import JIRA_URL, JIRA_TOKEN

def search_tickets(jql, max_results=30):
    """搜索 JIRA tickets"""
    if not JIRA_TOKEN:
        print("Error: JIRA_TOKEN not configured")
        return None
    
    session = requests.Session()
    session.get(f"{JIRA_URL}/login.jsp", timeout=30)
    
    headers = {
        'Authorization': f'Bearer {JIRA_TOKEN}',
        'Accept': 'application/json'
    }
    
    url = f"{JIRA_URL}/rest/api/2/search?jql={requests.utils.quote(jql)}&maxResults={max_results}"
    url += "&fields=summary,status,priority,project,issuetype,created,updated,assignee"
    
    resp = session.get(url, headers=headers, timeout=30)
    
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"Error: {resp.status_code} - {resp.text[:500]}")
        return None

def main():
    default_jql = "project = OBAS AND status = Open ORDER BY updated DESC"
    
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        jql = query
    else:
        jql = default_jql
    
    print(f"Searching: {jql}\n")
    
    data = search_tickets(jql)
    
    if data:
        issues = data.get('issues', [])
        print(f"=== Found {len(issues)} results ===\n")
        
        for issue in issues:
            key = issue.get('key')
            fields = issue.get('fields', {})
            summary = fields.get('summary', '')[:70]
            status = fields.get('status', {}).get('name', '')
            priority = fields.get('priority', {}).get('name', '')
            issue_type = fields.get('issuetype', {}).get('name', '')
            assignee = fields.get('assignee', {}).get('displayName', 'Unassigned')
            
            print(f"[{key}] {issue_type} - {priority}")
            print(f"  {summary}")
            print(f"  Status: {status} | Assignee: {assignee}\n")
        
        output_path = os.path.join(os.path.dirname(__file__), '..', 'search_results.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved to {output_path}")

if __name__ == '__main__':
    main()
