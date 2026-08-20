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

# 1. Get Sub-tasks of CEADU-682
print('='*70)
print('SUB-TASKS OF CEADU-682')
print('='*70)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-682?fields=subtasks,summary,status,issuetype,assignee', headers=headers, timeout=30)
data = resp.json()
subtasks = data.get('fields', {}).get('subtasks', [])

if subtasks:
    for st in subtasks:
        print(f"\n[Sub-task] {st.get('key')}")
        print(f"  Summary: {st.get('fields', {}).get('summary', 'N/A')}")
        print(f"  Status: {st.get('fields', {}).get('status', {}).get('name', 'N/A')}")
        print(f"  Assignee: {st.get('fields', {}).get('assignee', {}).get('displayName', 'N/A')}")
else:
    print('No sub-tasks found')

# 2. Get linked issues
print('\n' + '='*70)
print('LINKED ISSUES')
print('='*70)

resp = requests.get(f'{JIRA_URL}/rest/api/2/issue/CEADU-682?fields=issuelinks,summary,status,issuetype,assignee', headers=headers, timeout=30)
data = resp.json()
links = data.get('fields', {}).get('issuelinks', [])

link_count = 0
for link in links:
    if link.get('inwardIssue'):
        issue = link['inwardIssue']
        print(f"\n[{link.get('type', {}).get('name', 'N/A')}] {issue.get('key')}")
        print(f"  Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
        print(f"  Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
        print(f"  Type: {issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
        link_count += 1
    if link.get('outwardIssue'):
        issue = link['outwardIssue']
        print(f"\n[{link.get('type', {}).get('name', 'N/A')}] {issue.get('key')}")
        print(f"  Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
        print(f"  Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
        print(f"  Type: {issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
        link_count += 1

if link_count == 0:
    print('No linked issues found')

# 3. Get Child Issues (if CEADU-682 is Epic)
print('\n' + '='*70)
print('CHILD ISSUES OF CEADU-682')
print('='*70)

jql = 'parent = CEADU-682 ORDER BY created ASC'
resp = requests.get(f'{JIRA_URL}/rest/api/2/search?jql={requests.utils.quote(jql)}&maxResults=50&fields=summary,status,issuetype,assignee', headers=headers, timeout=30)
search_data = resp.json()

child_count = search_data.get('total', 0)
print(f"\nFound {child_count} child issues:")
for issue in search_data.get('issues', []):
    print(f"\n[{issue.get('key')}] {issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
    print(f"  Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
    print(f"  Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
    print(f"  Assignee: {issue.get('fields', {}).get('assignee', {}).get('displayName', 'N/A')}")

# 4. Search for issues linked to CEADU-682 by text
print('\n' + '='*70)
print('RELATED ISSUES (same project, Korea context)')
print('='*70)

jql = 'project = CEADU AND summary ~ \"Korea\" AND status != Closed ORDER BY created DESC'
resp = requests.get(f'{JIRA_URL}/rest/api/2/search?jql={requests.utils.quote(jql)}&maxResults=30&fields=summary,status,issuetype,assignee,parent', headers=headers, timeout=30)
search_data = resp.json()

print(f"\nFound {search_data.get('total', 0)} issues with 'Korea' in summary:")
for issue in search_data.get('issues', []):
    parent_key = issue.get('fields', {}).get('parent', {}).get('key', '-')
    if parent_key and parent_key != '-':
        print(f"\n[{issue.get('key')}] {issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}")
        print(f"  Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
        print(f"  Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
        print(f"  Assignee: {issue.get('fields', {}).get('assignee', {}).get('displayName', 'N/A')}")
        print(f"  Parent: {parent_key}")

print('\n' + '='*70)
print('ALL ISSUES IN CEADU PROJECT (Korea related, last 50)')
print('='*70)

jql = 'project = CEADU AND (summary ~ \"Korea\" OR summary ~ \"South Korea\" OR labels ~ \"Korea\") ORDER BY updated DESC'
resp = requests.get(f'{JIRA_URL}/rest/api/2/search?jql={requests.utils.quote(jql)}&maxResults=50&fields=summary,status,issuetype,assignee,parent', headers=headers, timeout=30)
search_data = resp.json()

print(f"\nTotal Korea-related issues: {search_data.get('total', 0)}")
for issue in search_data.get('issues', []):
    parent_key = issue.get('fields', {}).get('parent', {}).get('key', '-')
    print(f"\n[{issue.get('key')}] [{issue.get('fields', {}).get('issuetype', {}).get('name', 'N/A')}]")
    print(f"  Summary: {issue.get('fields', {}).get('summary', 'N/A')}")
    print(f"  Status: {issue.get('fields', {}).get('status', {}).get('name', 'N/A')}")
    print(f"  Assignee: {issue.get('fields', {}).get('assignee', {}).get('displayName', 'N/A')}")
    if parent_key and parent_key != '-':
        print(f"  Parent: {parent_key}")
