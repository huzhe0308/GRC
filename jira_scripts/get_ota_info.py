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

# Search for OTA/SUMS related tickets
print('='*80)
print('SEARCHING OTA/SUMS RELATED TICKETS')
print('='*80)

jqls = [
    'project = CEADU AND summary ~ "OTA" ORDER BY updated DESC',
    'project = CEADU AND summary ~ "SUMS" ORDER BY updated DESC',
    'project = CEADU AND summary ~ "Software Update" ORDER BY updated DESC'
]

for jql in jqls:
    resp = requests.get(f'{JIRA_URL}/rest/api/2/search?jql={requests.utils.quote(jql)}&maxResults=20&fields=summary,status,issuetype,assignee,parent', headers=headers, timeout=30)
    data = resp.json()
    total = data.get('total', 0)
    if total > 0:
        print(f'\nFound {total} issues:')
        for issue in data.get('issues', [])[:10]:
            parent_key = issue.get('fields', {}).get('parent', {}).get('key', '-')
            status = issue.get('fields', {}).get('status', {}).get('name', 'N/A')
            summary = issue.get('fields', {}).get('summary', 'N/A')
            assignee_field = issue.get('fields', {}).get('assignee')
            assignee = assignee_field.get('displayName', 'Unassigned') if assignee_field else 'Unassigned'
            print(f"  [{issue.get('key')}] [{status}] {summary}")
            print(f"    Assignee: {assignee} | Parent: {parent_key}")

# Get CEADU-2634 full comments for OTA details
print()
print('='*80)
print('CEADU-2634 - FULL OTA/SUMS EVALUATION DETAILS')
print('='*80)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-2634?fields=comment', headers=headers, timeout=30)
data = resp.json()
comments = data.get('fields', {}).get('comment', {}).get('comments', [])

for c in comments:
    author = c.get('author', {}).get('displayName', 'Unknown')
    created = c.get('created', '')[:10]
    body = c.get('body', '')
    if 'OTA' in body or 'SUMS' in body or 'ota' in body.lower() or 'ota' in body:
        print(f'\n[{created}] {author}:')
        print(body)

# Also get CEADU-682 attachment list for OTA related docs
print()
print('='*80)
print('CEADU-682 ATTACHMENTS (OTA/SUMS related)')
print('='*80)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-682?fields=attachment', headers=headers, timeout=30)
data = resp.json()
attachments = data.get('fields', {}).get('attachment', [])

ota_related = [a for a in attachments if 'ota' in a.get('filename', '').lower() or 'sums' in a.get('filename', '').lower() or 'update' in a.get('filename', '').lower() or 'SUMS' in a.get('filename', '').upper()]

print(f"Found {len(ota_related)} OTA/SUMS related attachments:")
for att in ota_related:
    print(f"  - {att.get('filename')} ({att.get('size', 0)} bytes)")
