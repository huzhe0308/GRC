#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JIRA Client - 查询和更新 ticket 状态

用法:
    python update_status.py <issue-key>              # 查询状态
    python update_status.py <issue-key> --transitions  # 查看可用转换
    python update_status.py <issue-key> --transition <id>  # 更新状态
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class JiraConfig:
    url: str
    token: str


def load_config():
    import os
    config_file = os.path.join(os.path.dirname(__file__), '.jira_config')
    config = {}
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    env_url = os.environ.get('JIRA_URL', '')
    env_token = os.environ.get('JIRA_TOKEN', '')
    return env_url or config.get('JIRA_URL', ''), env_token or config.get('JIRA_TOKEN', '')


JIRA_URL, JIRA_TOKEN = load_config()


class JiraClient:
    def __init__(self, url: str, token: str):
        self.url = url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        self.session.get(f"{self.url}/login.jsp", timeout=30)
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_issue(self, key: str) -> dict:
        resp = self.session.get(
            f"{self.url}/rest/api/2/issue/{key}",
            headers=self.headers,
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def get_transitions(self, key: str) -> list:
        resp = self.session.get(
            f"{self.url}/rest/api/2/issue/{key}/transitions",
            headers=self.headers,
            timeout=30
        )
        resp.raise_for_status()
        return resp.json().get('transitions', [])

    def transition(self, key: str, transition_id: str) -> bool:
        resp = self.session.post(
            f"{self.url}/rest/api/2/issue/{key}/transitions",
            headers=self.headers,
            json={"transition": {"id": transition_id}},
            timeout=30
        )
        if resp.status_code == 204:
            return True
        print(f"Error: {resp.status_code} - {resp.text}")
        return False

    def print_issue(self, key: str) -> None:
        data = self.get_issue(key)
        fields = data.get('fields', {})
        print(f"Key: {data.get('key')}")
        print(f"Summary: {fields.get('summary')}")
        print(f"Status: {fields.get('status', {}).get('name')}")
        print(f"Issue Type: {fields.get('issuetype', {}).get('name')}")
        print(f"Priority: {fields.get('priority', {}).get('name')}")
        print(f"Assignee: {fields.get('assignee', {}).get('displayName')}")
        print(f"URL: {self.url}/browse/{key}")

    def print_transitions(self, key: str) -> None:
        transitions = self.get_transitions(key)
        print(f"可用状态转换 [{key}]:")
        for t in transitions:
            print(f"  ID: {t['id']:>3}  {t['name']}")
        if not transitions:
            print("  (无可用转换)")


def main():
    if not JIRA_URL or not JIRA_TOKEN:
        print("Error: JIRA not configured")
        print("设置环境变量或创建 scripts/.jira_config 文件")
        sys.exit(1)

    parser = argparse.ArgumentParser(description='JIRA Client')
    parser.add_argument('key', nargs='?', help='Issue key (e.g., ISSUE-123)')
    parser.add_argument('--transitions', '-t', action='store_true', help='Show available transitions')
    parser.add_argument('--transition', metavar='ID', help='Transition ID to execute')

    args = parser.parse_args()

    if not args.key:
        parser.print_help()
        sys.exit(1)

    client = JiraClient(JIRA_URL, JIRA_TOKEN)

    if args.transitions:
        client.print_transitions(args.key)
    elif args.transition:
        if client.transition(args.key, args.transition):
            print(f"✓ 状态已更新: {args.key}")
            client.print_issue(args.key)
        else:
            print("✗ 更新失败")
    else:
        client.print_issue(args.key)


if __name__ == '__main__':
    main()
