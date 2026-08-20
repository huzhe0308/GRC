import sys
import requests
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load config
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

# Get CEADU-682
issue_key = 'CEADU-682'
resp = session.get(f'{JIRA_URL}/rest/api/2/issue/{issue_key}', headers=headers, timeout=30)
print(f"Status Code: {resp.status_code}")
print(f"Response Text: {resp.text[:500]}")
data = resp.json()

print('='*60)
print(f"Ticket: {data.get('key')}")
print(f"Summary: {data.get('fields', {}).get('summary', 'N/A')}")
print(f"Type: {data.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
print(f"Status: {data.get('fields', {}).get('status', {}).get('name', 'N/A')}")
print(f"Priority: {data.get('fields', {}).get('priority', {}).get('name', 'N/A')}")
print(f"Assignee: {data.get('fields', {}).get('assignee', {}).get('displayName', 'N/A')}")
print(f"Reporter: {data.get('fields', {}).get('reporter', {}).get('displayName', 'N/A')}")
print(f"Created: {data.get('fields', {}).get('created', 'N/A')}")
print(f"Updated: {data.get('fields', {}).get('updated', 'N/A')}")
print('='*60)

# Get labels
labels = data.get('fields', {}).get('labels', [])
if labels:
    print(f"\nLabels: {', '.join(labels)}")

# Get components
components = data.get('fields', {}).get('components', [])
if components:
    print(f"Components: {', '.join([c.get('name', '') for c in components])}")

# Get sprint info
print()
print('Description:')
print('-'*60)
desc = data.get('fields', {}).get('description', 'No description')
print(desc if desc else 'No description')
print('='*60)

# Get attachments
attachments = data.get('fields', {}).get('attachment', [])
if attachments:
    print('\nAttachments:')
    for att in attachments:
        print(f"  - {att.get('filename')} ({att.get('size', 0)} bytes)")

# Get comments
print()
print('Comments:')
print('-'*60)
resp_comments = session.get(f'{JIRA_URL}/rest/api/2/issue/{issue_key}/comment', headers=headers, timeout=30)
comments_data = resp_comments.json()
if comments_data.get('comments'):
    for comment in comments_data['comments']:
        author = comment.get('author', {}).get('displayName', 'Unknown')
        created = comment.get('created', '')[:10]
        body = comment.get('body', '')
        print(f"[{created}] {author}:")
        print(body)
        print()
else:
    print("No comments")
print('='*60)
