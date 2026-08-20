import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os
os.environ['NO_PROXY'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
os.environ['no_proxy'] = 'devstack.vgc.com.cn,*.vgc.com.cn'
import requests

JIRA_URL = 'https://devstack.vgc.com.cn/jira'

session = requests.Session()

# Step 1: Get login page and session cookies
login_resp = session.get(f'{JIRA_URL}/login.jsp', timeout=30, proxies={'http': None, 'https': None})
print(f'Login page: {login_resp.status_code}')

# Step 2: Try login form submission
login_data = {
    'os_username': 'jingjin.xie@volkswagen-tech.com',
    'os_password': 'YOUR_BITBUCKET_TOKEN',
    'os_destination': '',
    'user_role': '',
    'atl_token': '',
    'rememberUser': 'on'
}

resp = session.post(
    f'{JIRA_URL}/j_atlantic_security_check',
    data=login_data,
    allow_redirects=True,
    timeout=30,
    proxies={'http': None, 'https': None}
)
print(f'Login submit: {resp.status_code}')
print(f'Cookies after login: {list(session.cookies.keys())}')
print(f'JSESSIONID: {session.cookies.get("JSESSIONID", "N/A")[:20]}...')

# Step 3: Try API with session cookie
headers = {'Accept': 'application/json'}
api_resp = session.get(f'{JIRA_URL}/rest/api/2/myself', headers=headers, timeout=30, proxies={'http': None, 'https': None})
print(f'API Status: {api_resp.status_code}')
if api_resp.status_code == 200:
    print(f'User: {api_resp.json().get("displayName")}')
    print('SUCCESS!')
else:
    print(f'Response: {api_resp.text[:300]}')
