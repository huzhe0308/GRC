import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
os.environ['NO_PROXY'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
os.environ['no_proxy'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
import requests

JIRA_URL = 'https://devstack.vgc.com.cn/jira'

session = requests.Session()
login_resp = session.get(f'{JIRA_URL}/login.jsp', timeout=30, proxies={'http': None, 'https': None})
print(f'Login status: {login_resp.status_code}')
cookie = session.cookies.get('JSESSIONID', 'N/A')
print(f'Cookie JSESSIONID: {cookie[:20]}...')

headers = {'Accept': 'application/json'}
resp = session.get(f'{JIRA_URL}/rest/api/2/myself', headers=headers, timeout=30, proxies={'http': None, 'https': None})
print(f'API Status (no auth): {resp.status_code}')
if resp.status_code == 200:
    print(f'User: {resp.json().get("displayName")}')
else:
    print(f'Response: {resp.text[:200]}')
