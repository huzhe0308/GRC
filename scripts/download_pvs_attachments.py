#!/usr/bin/env python3
"""下载Jira工单附件到本地目录"""

import os
import sys
import requests
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from demo_app.app import load_config

def download_jira_attachments():
    """下载PSV/PVS附件到raw目录"""
    
    # 目标目录
    raw_dir = Path(r"C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\raw\pvs")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Jira配置
    cfg = load_config()
    jira_url = cfg.get("jira", {}).get("url", "https://devstack.vgc.com.cn/jira")
    jira_token = cfg.get("jira", {}).get("token", "")
    
    headers = {
        "Authorization": f"Bearer {jira_token}",
        "X-Atlassian-Token": "no-check"
    }
    
    # 需要下载附件的Parent工单列表
    parent_tickets = [
        "CEADU-682",   # Korea Cyber Sec
        "CEADU-2631",  # Korea Data Sec
        "CEADU-2739",  # ASEAN RHD
        "CEADU-3005",  # ASEAN LHD
        "CEADU-3784",  # India
        "CEADU-4514",  # Middle East
        "CEADU-4494",  # Kazakhstan
        "CEADU-5282",  # Uzbekistan
        "CEADU-6364",  # Turkey
        "CEADU-2711",  # AUS/NZL
    ]
    
    print(f"目标目录: {raw_dir}")
    print("-" * 50)
    
    downloaded_files = []
    
    for ticket_key in parent_tickets:
        print(f"\n处理工单: {ticket_key}")
        
        # 获取工单信息（含附件）
        try:
            resp = requests.get(
                f"{jira_url}/rest/api/2/issue/{ticket_key}?fields=attachment,summary",
                headers=headers,
                timeout=30
            )
            
            if resp.status_code != 200:
                print(f"  错误: HTTP {resp.status_code}")
                continue
            
            data = resp.json()
            fields = data.get("fields", {})
            summary = fields.get("summary", "")
            attachments = fields.get("attachment", [])
            
            print(f"  主题: {summary}")
            print(f"  附件数量: {len(attachments)}")
            
            # 筛选PVS/PSV文件
            pvs_files = [
                a for a in attachments 
                if a.get("filename", "").lower().endswith(('.xlsx', '.xls'))
                and ('pvs' in a.get("filename", "").lower() or 'psv' in a.get("filename", "").lower())
            ]
            
            if not pvs_files:
                # 下载所有Excel附件
                pvs_files = [
                    a for a in attachments 
                    if a.get("filename", "").lower().endswith(('.xlsx', '.xls'))
                ]
            
            print(f"  PVS/Excel文件: {len(pvs_files)}")
            
            for att in pvs_files:
                filename = att.get("filename", "")
                att_id = att.get("id", "")
                size = att.get("size", 0)
                
                # 下载附件
                try:
                    download_url = f"{jira_url}/rest/api/2/issue/{ticket_key}/attachments/{filename}"
                    resp = requests.get(download_url, headers=headers, timeout=60)
                    
                    if resp.status_code == 200:
                        # 保存文件
                        output_name = f"{ticket_key}_{filename}"
                        output_path = raw_dir / output_name
                        
                        with open(output_path, "wb") as f:
                            f.write(resp.content)
                        
                        size_kb = size / 1024
                        print(f"  ✓ {filename} ({size_kb:.1f} KB) -> {output_name}")
                        downloaded_files.append(str(output_path))
                    else:
                        print(f"  ✗ 下载失败: {filename} (HTTP {resp.status_code})")
                        
                except Exception as e:
                    print(f"  ✗ 错误: {filename} - {e}")
                    
        except Exception as e:
            print(f"  工单获取失败: {e}")
    
    print("\n" + "=" * 50)
    print(f"下载完成! 共 {len(downloaded_files)} 个文件")
    print(f"保存位置: {raw_dir}")
    
    return downloaded_files


if __name__ == "__main__":
    download_jira_attachments()
    input("\n按回车键退出...")
