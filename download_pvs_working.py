#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from pathlib import Path

JIRA_URL = 'https://devstack.vgc.com.cn/jira'
TOKEN = 'YOUR_JIRA_TOKEN'

headers = {'Authorization': 'Bearer ' + TOKEN}

# 获取附件信息
resp = requests.get(
    f'{JIRA_URL}/rest/api/2/issue/CEADU-682?fields=attachment',
    headers=headers,
    timeout=30
)

attachments = resp.json().get('fields', {}).get('attachment', [])
psv_attachments = [a for a in attachments if 'psv' in a.get('filename', '').lower() and a.get('filename', '').endswith('.xlsx')]

print(f'Found {len(psv_attachments)} PSV files')

out_dir = Path(r'C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\raw\pvs')
out_dir.mkdir(parents=True, exist_ok=True)

for att in psv_attachments:
    att_id = att.get('id')
    fname = att.get('filename', '')
    
    print(f'\nDownloading: {fname}')
    print(f'ID: {att_id}')
    
    # 使用正确的endpoint
    url = f'{JIRA_URL}/secure/attachment/{att_id}/{fname}'
    
    r = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
    print(f'Status: {r.status_code}')
    print(f'Size: {len(r.content)/1024:.1f} KB')
    
    if r.status_code == 200 and len(r.content) > 10000:
        out_name = fname.replace(' ', '_')
        out_path = out_dir / out_name
        out_path.write_bytes(r.content)
        print(f'SAVED: {out_path.name}')
    else:
        print('FAILED')

print(f'\nAll files saved to: {out_dir}')
