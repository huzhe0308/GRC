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

# Get all fields of CEADU-2634
resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-2634?fields=-1', headers=headers, timeout=30)
data = resp.json()
fields = data.get('fields', {})

print('='*80)
print('CEADU-2634 - ALL FIELDS')
print('='*80)
print()

# Standard fields
standard_fields = [
    ('summary', 'Summary'),
    ('status', 'Status'),
    ('priority', 'Priority'),
    ('issuetype', 'Issue Type'),
    ('assignee', 'Assignee'),
    ('reporter', 'Reporter'),
    ('creator', 'Creator'),
    ('created', 'Created'),
    ('updated', 'Updated'),
    ('description', 'Description'),
    ('labels', 'Labels'),
    ('components', 'Components'),
    ('parent', 'Parent'),
    ('project', 'Project'),
    ('resolution', 'Resolution'),
    ('resolutiondate', 'Resolution Date'),
    ('duedate', 'Due Date'),
]

for field_id, field_name in standard_fields:
    val = fields.get(field_id)
    if val is None or val == '' or val == []:
        continue
    if isinstance(val, dict):
        display = val.get('name') or val.get('value') or val.get('displayName') or json.dumps(val)
    elif isinstance(val, list):
        if val and isinstance(val[0], dict):
            display = ', '.join([v.get('name', '') or v.get('displayName', '') for v in val if v])
        else:
            display = ', '.join(str(v) for v in val)
    else:
        display = str(val)[:100] if len(str(val)) > 100 else str(val)
    print(f'{field_name}: {display}')

# Custom fields
print()
print('='*80)
print('CUSTOM FIELDS')
print('='*80)

for key, val in fields.items():
    if key.startswith('customfield_'):
        if val is None or val == '' or val == []:
            continue
        if isinstance(val, dict):
            display = val.get('name') or val.get('value') or val.get('displayName') or str(val)[:100]
        elif isinstance(val, list):
            if val and isinstance(val[0], dict):
                display = ', '.join([v.get('name', '') or v.get('displayName', '') for v in val[:5] if v])
            else:
                display = ', '.join(str(v) for v in val[:5])
        else:
            display = str(val)[:100] if len(str(val)) > 100 else str(val)
        print(f'{key}: {display}')

# Print all attachments
print()
print('='*80)
print('ATTACHMENTS')
print('='*80)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-2634?fields=attachment', headers=headers, timeout=30)
attachments = resp.json().get('fields', {}).get('attachment', [])
if attachments:
    for att in attachments:
        filename = att.get('filename', 'N/A')
        size = att.get('size', 0)
        author = att.get('author', {}).get('displayName', 'N/A')
        created = att.get('created', '')[:10]
        print(f'  - {filename} ({size} bytes)')
        print(f'    Author: {author}')
        print(f'    Created: {created}')
else:
    print('No attachments')

# Print all comments
print()
print('='*80)
print('ALL COMMENTS')
print('='*80)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-2634/comment', headers=headers, timeout=30)
comments = resp.json().get('comments', [])
if comments:
    for c in comments:
        author = c.get('author', {}).get('displayName', 'Unknown')
        created = c.get('created', '')[:19]
        body = c.get('body', '')
        print(f'[{created}] {author}:')
        print(body)
        print('-'*40)
else:
    print('No comments')

# Print subtasks if any
print()
print('='*80)
print('SUBTASKS')
print('='*80)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-2634?fields=subtasks', headers=headers, timeout=30)
subtasks = resp.json().get('fields', {}).get('subtasks', [])
if subtasks:
    for st in subtasks:
        print(f'  - [{st.get("key")}] {st.get("fields", {}).get("summary", "N/A")}')
        print(f'    Status: {st.get("fields", {}).get("status", {}).get("name", "N/A")}')
else:
    print('No subtasks')

# Print links if any
print()
print('='*80)
print('ISSUE LINKS')
print('='*80)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-2634?fields=issuelinks', headers=headers, timeout=30)
links = resp.json().get('fields', {}).get('issuelinks', [])
if links:
    for link in links:
        if link.get('inwardIssue'):
            issue = link['inwardIssue']
            print(f'  [{link.get("type", {}).get("name", "N/A")}] {issue.get("key")}: {issue.get("fields", {}).get("summary", "N/A")}')
        if link.get('outwardIssue'):
            issue = link['outwardIssue']
            print(f'  [{link.get("type", {}).get("name", "N/A")}] {issue.get("key")}: {issue.get("fields", {}).get("summary", "N/A")}')
else:
    print('No issue links')
