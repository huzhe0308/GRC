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

parent_tickets = ['CEADU-682', 'CEADU-2739', 'CEADU-3005', 'CEADU-3784', 'CEADU-4494', 'CEADU-5282', 'CEADU-6364', 'CEADU-2711', 'CEADU-6746']

for parent in parent_tickets:
    resp = session.get(f'{JIRA_URL}/rest/api/2/issue/{parent}', headers=headers, timeout=30)
    if resp.status_code == 200:
        data = resp.json()
        subtasks = data.get('fields', {}).get('subtasks', [])
        if subtasks:
            print(f'\n=== {parent} Subtasks ({len(subtasks)}) ===')
            for st in subtasks:
                st_key = st.get('key', '')
                st_summary = st.get('fields', {}).get('summary', '')
                st_status = st.get('fields', {}).get('status', {}).get('name', '')
                st_type = st.get('fields', {}).get('issuetype', {}).get('name', '')
                print(f'  [{st_status}] {st_key}: {st_summary}')

                # Get comments for this subtask
                st_resp = session.get(f'{JIRA_URL}/rest/api/2/issue/{st_key}/comment', headers=headers, timeout=30)
                if st_resp.status_code == 200:
                    comments = st_resp.json().get('comments', [])
                    for c in comments:
                        body = c.get('body', '')
                        if 'EF' in body.upper() or 'EF' in body:
                            author = c.get('author', {}).get('displayName', 'Unknown')
                            created = c.get('created', '')[:10]
                            print(f'    EF comment [{created}] {author}:')
                            print(f'    {body[:500]}')
