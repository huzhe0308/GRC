import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
os.environ['NO_PROXY'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
os.environ['no_proxy'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
import requests

JIRA_URL = 'https://devstack.vgc.com.cn/jira'

session = requests.Session()
session.get(f'{JIRA_URL}/login.jsp', timeout=30)

headers = {
    'Authorization': 'Bearer YOUR_BITBUCKET_TOKEN',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

jql = 'project = CEADU ORDER BY updated DESC'
url = f'{JIRA_URL}/rest/api/2/search?jql={requests.utils.quote(jql)}&maxResults=5&fields=summary,status'
resp = session.get(url, headers=headers, timeout=30, proxies={'http': None, 'https': None})
print(f'Search Status: {resp.status_code}')
if resp.status_code == 200:
    data = resp.json()
    issues = data.get('issues', [])
    print(f'Found {len(issues)} issues')
    for issue in issues[:3]:
        print(f'  {issue.get("key")}: {issue.get("fields", {}).get("summary", "N/A")[:60]}')
else:
    print(resp.text[:500])
