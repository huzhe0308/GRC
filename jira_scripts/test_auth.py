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

# First get the login page to get session cookies
login_resp = session.get(f'{JIRA_URL}/login.jsp', timeout=30)
print(f'Login page status: {login_resp.status_code}')
print(f'Cookies: {dict(session.cookies)}')

# Try different auth methods
headers_list = [
    {'Authorization': f'Bearer {TOKEN}', 'Accept': 'application/json'},
    {'Authorization': f'Basic {TOKEN}', 'Accept': 'application/json'},
    {'X-Atlassian-Token': 'no-check', 'Accept': 'application/json'},
]

for i, headers in enumerate(headers_list):
    print(f'\nTrying auth method {i+1}:')
    print(f'Headers: {headers}')
    resp = session.get(f'{JIRA_URL}/rest/api/2/myself', headers=headers, timeout=30)
    print(f'  Status: {resp.status_code}')
    if resp.status_code == 200:
        print(f'  Success! User: {resp.json().get("displayName", "N/A")}')
        break
    else:
        print(f'  Failed: {resp.text[:200]}')
