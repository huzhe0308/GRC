#!/usr/bin/env python3
"""
评估分配模块 - 一键执行
使用Jira API直接读取数据，更稳定
"""
import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

# 配置
JIRA_URL = 'https://devstack.vgc.com.cn/jira'
TOKEN = 'YOUR_JIRA_TOKEN'
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

RAW_DIR = Path(r'C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\raw\pvs')
WIKI_DIR = Path(r'C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\queries')
REPORTS_DIR = Path(r'C:\Users\T1UKLL7\Desktop\Workstation\employee agent\runtime\reports')

RAW_DIR.mkdir(parents=True, exist_ok=True)
WIKI_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Layer3关键词
LAYER3_KEYWORDS = {
    "Cyber Security": ["cyber", "csms", "un-r 155", "security", "threat", "penetration"],
    "Data Security": ["data security", "privacy", "gdpr", "pdpa", "personal data", "encryption", "pipa"],
    "OTA": ["ota", "over-the-air", "software update", "sums", "un-r 156", "update"],
    "OBD": ["obd", "emission", "diagnostic", "un-r 83", "un-r 10", "kncap"],
    "Functional Safety": ["functional safety", "fusa", "iso 26262", "sotif", "asil", "hazard"],
}

# 市场映射
MARKET_MAP = {
    "CEADU-682": ("Korea", "South Korea Homologation"),
    "CEADU-2631": ("Korea", "Korea Data Security"),
    "CEADU-2739": ("ASEAN RHD", "ASEAN Right-Hand Drive"),
    "CEADU-3005": ("ASEAN LHD", "ASEAN Left-Hand Drive"),
    "CEADU-3784": ("India", "India Homologation"),
    "CEADU-4514": ("Middle East", "Middle East GCC"),
    "CEADU-4494": ("Kazakhstan", "Kazakhstan EAEU"),
    "CEADU-5282": ("Uzbekistan", "Uzbekistan EAEU"),
    "CEADU-6364": ("Turkey", "Turkey Homologation"),
    "CEADU-2711": ("AUS/NZL", "Australia New Zealand CMP21"),
    "CEADU-6746": ("AUS/NZL", "Australia New Zealand CSP31"),
}


def jira_get(path: str) -> dict:
    """Jira GET请求"""
    resp = requests.get(f"{JIRA_URL}/rest/api/2/{path}", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def list_my_tasks():
    """列出分配给我的Layer3相关任务"""
    print("=" * 60)
    print("1. 获取分配的Layer3评估任务")
    print("=" * 60)
    
    # 查询assignee为当前用户的subtask
    jql = 'project = CEADU AND issuetype = Sub-task AND assignee = currentUser() ORDER BY updated DESC'
    data = jira_get(f"search?jql={requests.utils.quote(jql)}&fields=summary,status,parent,priority&maxResults=20")
    
    tasks = []
    for issue in data.get('issues', []):
        fields = issue.get('fields', {})
        parent_key = fields.get('parent', {}).get('key', '')
        
        # 检查是否与Layer3相关
        summary = fields.get('summary', '').lower()
        if any(kw in summary for kw in ['layer3', 'cyber', 'data', 'ota', 'obd', 'safety', 'assessment']):
            market, _ = MARKET_MAP.get(parent_key, ("Unknown", ""))
            tasks.append({
                'key': issue.get('key'),
                'summary': fields.get('summary'),
                'status': fields.get('status', {}).get('name'),
                'parent': parent_key,
                'market': market,
            })
    
    print(f"找到 {len(tasks)} 个评估任务:\n")
    for i, t in enumerate(tasks, 1):
        print(f"{i}. [{t['key']}] {t['summary']}")
        print(f"   Parent: {t['parent']} | Market: {t['market']} | Status: {t['status']}")
        print()
    
    return tasks


def get_parent_info(parent_key: str):
    """获取Parent工单信息"""
    print("=" * 60)
    print(f"2. 获取Parent工单: {parent_key}")
    print("=" * 60)
    
    try:
        issue = jira_get(f"issue/{parent_key}?fields=summary,attachment,status")
        fields = issue.get('fields', {})
        
        print(f"Summary: {fields.get('summary')}")
        print(f"Status: {fields.get('status', {}).get('name')}")
        
        attachments = fields.get('attachment', [])
        psv_attachments = [a for a in attachments if 'psv' in a.get('filename', '').lower()]
        
        print(f"\nAttachments: {len(attachments)}")
        print(f"PSV Files: {len(psv_attachments)}")
        
        for att in psv_attachments:
            print(f"  - {att.get('filename')} ({att.get('size', 0)/1024:.1f} KB)")
        
        return {
            'key': parent_key,
            'summary': fields.get('summary'),
            'status': fields.get('status', {}).get('name'),
            'attachments': psv_attachments,
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return None


def download_psv(attachment: dict, parent_key: str) -> Path:
    """下载PSV文件"""
    filename = attachment.get('filename')
    content_url = attachment.get('content')
    
    print(f"\nDownloading: {filename}")
    
    # 使用content URL下载
    resp = requests.get(content_url, headers=HEADERS, timeout=120, stream=True)
    resp.raise_for_status()
    
    safe_name = filename.replace(' ', '_')
    out_path = RAW_DIR / f"{parent_key}_{safe_name}"
    out_path.write_bytes(resp.content)
    
    print(f"Saved: {out_path.name} ({len(resp.content)/1024:.1f} KB)")
    return out_path


def parse_psv(excel_path: Path, market: str, parent_key: str):
    """解析PSV文件识别Layer3法规"""
    print(f"\n" + "=" * 60)
    print(f"3. 解析PSV文件: {excel_path.name}")
    print("=" * 60)
    
    import openpyxl
    
    regulations = []
    
    try:
        wb = openpyxl.load_workbook(excel_path, data_only=True)
        
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            
            # 找表头
            headers = []
            header_row = None
            
            for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=10, values_only=True), 1):
                row_text = ' '.join(str(c).lower() for c in row if c)
                if any(kw in row_text for kw in ['regulation', 'clause', 'requirement', 'article', 'section']):
                    headers = [str(c).lower().strip() if c else '' for c in row]
                    header_row = row_idx
                    break
            
            # 解析数据
            start_row = header_row + 1 if header_row else 2
            
            for row in ws.iter_rows(min_row=start_row, values_only=True):
                if not any(row):
                    continue
                
                row_text = ' '.join(str(c).lower() for c in row if c)
                if len(row_text) < 5:
                    continue
                
                # 匹配Layer3
                matched = []
                for topic, keywords in LAYER3_KEYWORDS.items():
                    if any(kw in row_text for kw in keywords):
                        matched.append(topic)
                
                if matched:
                    row_data = dict(zip(headers, row)) if headers else {}
                    
                    regulation = row_data.get('regulation', row[0] if len(row) > 0 else '')
                    clause = row_data.get('clause', row[1] if len(row) > 1 else '')
                    description = ' '.join(str(c) for c in row[2:6] if c)[:200]
                    
                    if regulation:
                        regulations.append({
                            'regulation': str(regulation),
                            'clause': str(clause)[:50],
                            'market': market,
                            'layer3': ', '.join(matched),
                            'matchKeyword': matched[0],
                            'description': description,
                            'status': 'Required',
                            'source': parent_key,
                        })
        
        wb.close()
        
    except Exception as e:
        print(f"Parse error: {e}")
    
    print(f"\n找到 {len(regulations)} 条Layer3法规:\n")
    
    # 按Layer3分组显示
    by_layer3 = {}
    for reg in regulations:
        layer3 = reg['layer3']
        if layer3 not in by_layer3:
            by_layer3[layer3] = []
        by_layer3[layer3].append(reg)
    
    for layer3, regs in sorted(by_layer3.items()):
        print(f"\n### {layer3} ({len(regs)}条)")
        for reg in regs[:5]:  # 每类显示前5条
            print(f"  - {reg['regulation']} {reg['clause'][:30]}")
        if len(regs) > 5:
            print(f"  ... 还有 {len(regs) - 5} 条")
    
    return regulations


def save_to_wiki(regulations: list, market: str, parent_key: str):
    """保存到Wiki"""
    print(f"\n" + "=" * 60)
    print(f"4. 保存到Wiki")
    print("=" * 60)
    
    market_key = market.replace('/', '_').replace(' ', '_').lower()
    
    # 保存市场文件
    lines = [
        f"# {market} - Layer3法规",
        "",
        f"**Parent工单**: {parent_key}",
        f"**法规数量**: {len(regulations)}",
        f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Layer3法规列表",
        "",
    ]
    
    by_layer3 = {}
    for reg in regulations:
        layer3 = reg['layer3']
        if layer3 not in by_layer3:
            by_layer3[layer3] = []
        by_layer3[layer3].append(reg)
    
    for layer3, regs in sorted(by_layer3.items()):
        lines.append(f"### {layer3} ({len(regs)}条)")
        lines.append("")
        for reg in regs:
            lines.append(f"**{reg['regulation']}** - {reg['clause']}")
            lines.append(f"- Layer3: {reg['layer3']}")
            lines.append(f"- 市场: {reg['market']}")
            lines.append(f"- 状态: {reg['status']}")
            lines.append("")
    
    wiki_path = WIKI_DIR / f"pvs_market_{market_key}.md"
    wiki_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"保存: {wiki_path.name}")
    
    # 更新汇总
    update_summary(regulations, parent_key, market)
    
    return wiki_path


def update_summary(new_regs: list, parent_key: str, market: str):
    """更新汇总文件"""
    summary_file = WIKI_DIR / "pvs_layer3_regulations_summary.md"
    
    existing = []
    if summary_file.exists():
        content = summary_file.read_text(encoding='utf-8')
        in_list = False
        for line in content.split('\n'):
            if line.strip() == '## 完整法规列表':
                in_list = True
                continue
            if in_list and line.strip().startswith('- '):
                existing.append(line.strip())
    
    # 添加新法规
    for reg in new_regs:
        reg_str = f"- **{reg['regulation']}** {reg['clause'][:30]} [{market}] ({parent_key})"
        if reg_str not in existing:
            existing.append(reg_str)
    
    lines = [
        "# PVS Layer3 法规汇总",
        "",
        f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**总计**: {len(existing)} 条法规",
        "",
        "## 完整法规列表",
        "",
    ]
    lines.extend(existing)
    
    summary_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"汇总已更新: {len(existing)} 条法规")


def generate_assessment_report(task_key: str, parent_key: str, regulations: list, market: str):
    """生成评估报告"""
    print(f"\n" + "=" * 60)
    print(f"5. 生成评估报告")
    print("=" * 60)
    
    report_lines = [
        f"# Layer3法规评估报告",
        "",
        f"**Sub-task**: {task_key}",
        f"**Parent工单**: {parent_key}",
        f"**市场**: {market}",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        f"## 需要评估的Layer3法规 ({len(regulations)}条)",
        "",
    ]
    
    by_layer3 = {}
    for reg in regulations:
        layer3 = reg['layer3']
        if layer3 not in by_layer3:
            by_layer3[layer3] = []
        by_layer3[layer3].append(reg)
    
    for layer3, regs in sorted(by_layer3.items()):
        report_lines.append(f"### {layer3} ({len(regs)}条)")
        report_lines.append("")
        for reg in regs:
            report_lines.append(f"1. **{reg['regulation']}** - {reg['clause']}")
            report_lines.append(f"   - 匹配关键词: {reg['matchKeyword']}")
            report_lines.append(f"   - 描述: {reg.get('description', '')[:100]}")
            report_lines.append("")
    
    report_lines.extend([
        "---",
        "",
        "## 评估建议",
        "",
        "请在Jira工单中反馈以下内容：",
        "1. 每条法规的合规状态（Compliant/Non-Compliant/Partially Compliant）",
        "2. 需要的适配工作量（MM）",
        "3. 注意事项",
        "",
    ])
    
    report_content = '\n'.join(report_lines)
    report_name = f"assessment_{task_key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path = REPORTS_DIR / report_name
    report_path.write_text(report_content, encoding='utf-8')
    
    print(f"报告已生成: {report_path.name}")
    print(f"路径: {report_path}")
    
    return report_path


def main():
    """Main function - Full workflow"""
    # 设置输出编码
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("\n" + "=" * 60)
    print("Assessment Module - Layer3 Regulation Recognition")
    print("=" * 60)
    
    # 1. List tasks
    tasks = list_my_tasks()
    
    if not tasks:
        print("No tasks found")
        return
    
    # Use first task
    task = tasks[0]
    task_key = task['key']
    parent_key = task['parent']
    market = task['market']
    
    print(f"\nSelected: {task_key}")
    print(f"Parent: {parent_key}")
    print(f"Market: {market}")
    
    # 2. Get Parent info
    parent_info = get_parent_info(parent_key)
    if not parent_info:
        return
    
    # 3. Download PSV
    psv_attachments = parent_info.get('attachments', [])
    if not psv_attachments:
        print("\nNo PSV files found")
        return
    
    att = psv_attachments[0]
    excel_path = download_psv(att, parent_key)
    
    # 4. Parse PSV
    regulations = parse_psv(excel_path, market, parent_key)
    
    if not regulations:
        print("\nNo Layer3 regulations found")
        return
    
    # 5. Save to Wiki
    save_to_wiki(regulations, market, parent_key)
    
    # 6. Generate report
    report_path = generate_assessment_report(task_key, parent_key, regulations, market)
    
    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print(f"Layer3 Regulations: {len(regulations)}")
    print(f"Wiki: {WIKI_DIR}")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
