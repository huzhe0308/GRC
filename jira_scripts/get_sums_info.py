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

# Get CEADU-2440 details (CSMS & SUMS)
print('='*80)
print('CEADU-2440 - CSMS & SUMS (Korea specific)')
print('='*80)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-2440?fields=summary,status,assignee,description,comment', headers=headers, timeout=30)
data = resp.json()
fields = data.get('fields', {})

assignee = fields.get('assignee', {})
assignee_name = assignee.get('displayName', 'N/A') if assignee else 'Unassigned'

print(f"Summary: {fields.get('summary', 'N/A')}")
print(f"Status: {fields.get('status', {}).get('name', 'N/A')}")
print(f"Assignee: {assignee_name}")
print()
print('DESCRIPTION:')
print(fields.get('description', 'No description'))
print()
print('COMMENTS:')
comments = fields.get('comment', {}).get('comments', [])
if comments:
    for c in comments[-5:]:
        author = c.get('author', {}).get('displayName', 'Unknown')
        created = c.get('created', '')[:10]
        body = c.get('body', '')
        body_short = body[:500] if len(body) > 500 else body
        print(f"[{created}] {author}: {body_short}")
else:
    print("No comments")

# Get CEADU-682 description for SUMS context
print()
print('='*80)
print('CEADU-682 - SUMS Related Content from Description')
print('='*80)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-682?fields=description', headers=headers, timeout=30)
data = resp.json()
desc = data.get('fields', {}).get('description', '')

if 'SUMS' in desc:
    # Extract SUMS related part
    lines = desc.split('\n')
    for i, line in enumerate(lines):
        if 'SUMS' in line or 'Software Update' in line:
            start = max(0, i-2)
            end = min(len(lines), i+5)
            print('\n'.join(lines[start:end]))
            print()

# Also search for Korea + OTA specific tickets
print()
print('='*80)
print('KOREAN SPECIFIC OTA/SUMS TICKETS')
print('='*80)

jql = 'project = CEADU AND (summary ~ "Korea" AND summary ~ "OTA") OR (summary ~ "Korea" AND summary ~ "SUMS") ORDER BY updated DESC'
resp = requests.get(f'{JIRA_URL}/rest/api/2/search?jql={requests.utils.quote(jql)}&maxResults=20&fields=summary,status,assignee,parent', headers=headers, timeout=30)
data = resp.json()
print(f"Found {data.get('total', 0)} Korea OTA/SUMS related tickets:")
for issue in data.get('issues', [])[:10]:
    parent = issue.get('fields', {}).get('parent', {})
    parent_key = parent.get('key', '-') if parent else '-'
    status = issue.get('fields', {}).get('status', {}).get('name', 'N/A')
    assignee = issue.get('fields', {}).get('assignee', {})
    assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
    print(f"  [{issue.get('key')}] [{status}] {issue.get('fields', {}).get('summary', 'N/A')}")
    print(f"    Assignee: {assignee_name} | Parent: {parent_key}")
