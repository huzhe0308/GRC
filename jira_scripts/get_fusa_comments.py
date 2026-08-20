import sys
import requests
import io
import json

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

for ticket in tickets:
    resp = session.get(f'{JIRA_URL}/rest/api/2/issue/{ticket}', headers=headers, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        print(f'\n=== {ticket} ===')
        print(f'Summary: {data.get("fields", {}).get("summary", "N/A")}')
        print(f'Status: {data.get("fields", {}).get("status", {}).get("name", "N/A")}')
        comments_resp = session.get(f'{JIRA_URL}/rest/api/2/issue/{ticket}/comment', headers=headers, timeout=30)
        if comments_resp.status_code == 200:
            comments = comments_resp.json().get('comments', [])
            print(f'Comments ({len(comments)}):')
            for c in comments[:10]:
                body = c.get('body', '')
                author = c.get('author', {}).get('displayName', 'Unknown')
                created = c.get('created', '')[:10]
                print(f'  [{created}] {author}: {body[:500]}')
                if len(body) > 500:
                    print(f'    ...(truncated)')
        else:
            print(f'Failed to get comments: {comments_resp.status_code} - {comments_resp.text[:200]}')
    else:
        print(f'\n{ticket}: Error {resp.status_code}')
        print(f'  Response: {resp.text[:300]}')
