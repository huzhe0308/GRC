import sys
import requests
import io

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

tickets = ['CEADU-2631', 'CEADU-2623', 'CEADU-2634']

for tk in tickets:
    print('='*80)
    print(f'TICKET: {tk}')
    print('='*80)
    
    resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/{tk}?fields=summary,status,issuetype,assignee,reporter,description,created,updated,labels,priority,parent,subtasks,comment', headers=headers, timeout=30)
    data = resp.json()
    fields = data.get('fields', {})
    
    print(f"Summary: {fields.get('summary', 'N/A')}")
    print(f"Status: {fields.get('status', {}).get('name', 'N/A')}")
    print(f"Type: {fields.get('issuetype', {}).get('name', 'N/A')}")
    print(f"Priority: {fields.get('priority', {}).get('name', 'N/A')}")
    print(f"Assignee: {fields.get('assignee', {}).get('displayName', 'N/A')}")
    print(f"Reporter: {fields.get('reporter', {}).get('displayName', 'N/A')}")
    
    created = fields.get('created', 'N/A')
    print(f"Created: {created[:10] if created else 'N/A'}")
    
    updated = fields.get('updated', 'N/A')
    print(f"Updated: {updated[:10] if updated else 'N/A'}")
    
    parent = fields.get('parent', {})
    if parent:
        print(f"Parent: {parent.get('key', 'N/A')}")
    
    labels = fields.get('labels', [])
    if labels:
        print(f"Labels: {', '.join(labels)}")
    
    print()
    print('DESCRIPTION:')
    print('-'*80)
    desc = fields.get('description', 'No description')
    print(desc if desc else 'No description')
    print()
    
    # Get comments
    comments = fields.get('comment', {}).get('comments', [])
    if comments:
        print('RECENT COMMENTS:')
        print('-'*80)
        for c in comments[-10:]:
            author = c.get('author', {}).get('displayName', 'Unknown')
            created = c.get('created', '')[:10]
            body = c.get('body', '')
            print(f"[{created}] {author}:")
            print(body[:800] if len(body) > 800 else body)
            print()
    
    print()
