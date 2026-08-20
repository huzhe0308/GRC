import sys
import requests
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

config = {}
with open('.jira_config', 'r') as f:
    for line in f:
        if '=' in line:
            key, val = line.strip().split('=', 1)
            config[key] = val

JIRA_URL = config.get('JIRA_URL', 'https://devstack.vgc.com.cn/jira').rstrip('/')
TOKEN = config.get('JIRA_TOKEN', '')

session = requests.Session()
session.get(f'{JIRA_URL}/login.jsp', timeout=30)

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

tickets = ['CEADU-682', 'CEADU-2739', 'CEADU-3005', 'CEADU-3784', 'CEADU-4494', 'CEADU-5282', 'CEADU-6364', 'CEADU-2711', 'CEADU-6746']

print('Searching for EF-related comments in all FuSa tickets...\n')

for ticket in tickets:
    resp = session.get(f'{JIRA_URL}/rest/api/2/issue/{ticket}/comment', headers=headers, timeout=30)
    if resp.status_code == 200:
        comments = resp.json().get('comments', [])
        for c in comments:
            body = c.get('body', '')
            if 'EF' in body.upper() or 'eF' in body:
                author = c.get('author', {}).get('displayName', 'Unknown')
                created = c.get('created', '')[:10]
                print(f'=== {ticket} [{created}] {author} ===')
                print(body)
                print()
