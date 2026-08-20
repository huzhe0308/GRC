import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
os.environ['NO_PROXY'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
os.environ['no_proxy'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
import requests

JIRA_URL = 'https://devstack.vgc.com.cn/jira'
TOKEN = 'YOUR_BITBUCKET_TOKEN'

session = requests.Session()
session.get(f'{JIRA_URL}/login.jsp', timeout=30)

headers = {'Accept': 'application/json', 'Authorization': f'Bearer {TOKEN}'}

endpoints = [
    '/rest/api/2/serverInfo',
    '/rest/api/2/project',
    '/rest/api/2/issue/CEADU-1',
    '/rest/api/2/search?jql=project=CEADU',
    '/rest/auth/1/session',
]

print('Testing endpoints:')
for ep in endpoints:
    resp = session.get(f'{JIRA_URL}{ep}', headers=headers, timeout=15, proxies={'http': None, 'https': None})
    print(f'  {ep}: {resp.status_code}')
