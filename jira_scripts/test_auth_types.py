import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
os.environ['NO_PROXY'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
os.environ['no_proxy'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
import requests
import requests.auth
import base64

JIRA_URL = 'https://devstack.vgc.com.cn/jira'

session = requests.Session()
session.get(f'{JIRA_URL}/login.jsp', timeout=30)

email = 'jingjin.xie@volkswagen-tech.com'
token = 'YOUR_BITBUCKET_TOKEN'
credentials = f'{email}:{token}'
encoded = base64.b64encode(credentials.encode()).decode()

headers_list = [
    {'Authorization': f'Bearer {token}', 'Accept': 'application/json'},
    {'Authorization': f'Basic {encoded}', 'Accept': 'application/json'},
    {'Authorization': f'Basic {token}', 'Accept': 'application/json'},
    {'X-Auth-Token': token, 'Accept': 'application/json'},
    {'X-Api-Key': token, 'Accept': 'application/json'},
]

print('Trying different auth methods:')
for h in headers_list:
    auth_type = list(h.keys())[1] if len(h) > 1 else 'N/A'
    resp = session.get(f'{JIRA_URL}/rest/api/2/myself', headers=h, timeout=15, proxies={'http': None, 'https': None})
    print(f'  {auth_type}: {resp.status_code}')
    if resp.status_code == 200:
        print(f'  User: {resp.json().get("displayName", "N/A")}')
        break
    elif resp.status_code != 401:
        print(f'  {resp.text[:100]}')
