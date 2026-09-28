#!/usr/bin/env python3
"""
手动下载PSV文件 - 生成下载链接
"""
import webbrowser
from pathlib import Path

JIRA_URL = 'https://devstack.vgc.com.cn/jira'

PARENT_TICKETS = {
    'CEADU-682': 'Korea',
    'CEADU-2631': 'Korea Data Sec',
    'CEADU-2739': 'ASEAN RHD',
    'CEADU-3005': 'ASEAN LHD',
    'CEADU-3784': 'India',
    'CEADU-4514': 'Middle East',
    'CEADU-4494': 'Kazakhstan',
    'CEADU-5282': 'Uzbekistan',
    'CEADU-6364': 'Turkey',
    'CEADU-2711': 'AUS/NZL',
}

print('=' * 60)
print('请从Jira手动下载PSV文件')
print('=' * 60)

for ticket, desc in PARENT_TICKETS.items():
    url = f'{JIRA_URL}/browse/{ticket}'
    print(f'\n{desc} ({ticket}):')
    print(f'  {url}')
    print(f'  请下载PSV/PSV Excel文件，重命名为: {ticket}_PSV.xlsx')

_APP_ROOT = Path(__file__).resolve().parent.parent
_target = _APP_ROOT / "wiki" / "raw" / "pvs"

print('\n' + '=' * 60)
print('下载后保存到:')
print(str(_target))
print('=' * 60)

# 创建目录
target_dir = _target
target_dir.mkdir(parents=True, exist_ok=True)

print(f'\n目录已创建: {target_dir}')
