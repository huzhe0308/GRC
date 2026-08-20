#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA - 创建新 ticket
"""
import requests
import json
import sys
import io
import os
import argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from config import JIRA_URL, JIRA_TOKEN

def create_ticket(project, summary, description, issue_type='Task', assignee=None):
    """创建 JIRA ticket"""
    if not JIRA_TOKEN:
        print("Error: JIRA_TOKEN not configured")
        return None
    
    session = requests.Session()
    session.get(f"{JIRA_URL}/login.jsp", timeout=30)
    
    headers = {
        'Authorization': f'Bearer {JIRA_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    issue_data = {
        "fields": {
            "project": {"key": project},
            "summary": summary,
            "description": description,
            "issuetype": {"name": issue_type}
        }
    }
    
    if assignee:
        issue_data["fields"]["assignee"] = {"name": assignee}
    
    resp = session.post(
        f"{JIRA_URL}/rest/api/2/issue",
        headers=headers,
        json=issue_data,
        timeout=30
    )
    
    if resp.status_code == 201:
        return resp.json()
    else:
        print(f"Error: {resp.status_code}")
        print(resp.text)
        return None

def main():
    parser = argparse.ArgumentParser(description='Create JIRA ticket')
    parser.add_argument('--project', '-p', default='OBAS', help='Project key')
    parser.add_argument('--summary', '-s', required=True, help='Ticket summary')
    parser.add_argument('--description', '-d', default='', help='Ticket description')
    parser.add_argument('--type', '-t', default='Task', help='Issue type (Task/Story/Bug/Epic)')
    parser.add_argument('--assignee', '-a', default=None, help='Assignee username')
    
    args = parser.parse_args()
    
    result = create_ticket(
        args.project,
        args.summary,
        args.description,
        args.type,
        args.assignee
    )
    
    if result:
        key = result.get('key')
        print(f"\n✓ Ticket created: {key}")
        print(f"  URL: {JIRA_URL}/browse/{key}")

if __name__ == '__main__':
    main()
