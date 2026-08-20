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

# Check /rest/auth/1/session endpoint
resp = session.get(f'{JIRA_URL}/rest/auth/1/session', timeout=15, proxies={'http': None, 'https': None})
print(f'/rest/auth/1/session: {resp.status_code}')
print(resp.text[:300] if resp.status_code != 401 else '401 Unauthorized')

# Check /rest/auth/1/session with POST
resp2 = session.post(f'{JIRA_URL}/rest/auth/1/session', json={'username': 'jingjin.xie@volkswagen-tech.com', 'password': 'YOUR_BITBUCKET_TOKEN'}, timeout=15, proxies={'http': None, 'https': None})
print(f'POST /rest/auth/1/session: {resp2.status_code}')
print(resp2.text[:300])
