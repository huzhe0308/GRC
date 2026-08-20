#!/usr/bin/env python3
"""
一键下载PSV附件 → 解析 → 生成Wiki
"""
import os
import sys
import requests
import re
from pathlib import Path
from datetime import datetime

try:
    import openpyxl
except ImportError:
    print("需要安装 openpyxl: pip install openpyxl")
    sys.exit(1)

# 配置
JIRA_URL = "https://devstack.vgc.com.cn/jira"
JIRA_TOKEN = "YOUR_JIRA_TOKEN"

# 目录
RAW_DIR = Path(r"C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\raw\pvs")
WIKI_DIR = Path(r"C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\queries")
EXCEL_DIR = Path(r"C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\raw\excel")

# Parent工单列表
PARENT_TICKETS = [
    ("CEADU-682", "Korea Cyber Sec"),
    ("CEADU-2631", "Korea Data Sec"),
    ("CEADU-2739", "ASEAN RHD"),
    ("CEADU-3005", "ASEAN LHD"),
    ("CEADU-3784", "India"),
    ("CEADU-4514", "Middle East"),
    ("CEADU-4494", "Kazakhstan"),
    ("CEADU-5282", "Uzbekistan"),
    ("CEADU-6364", "Turkey"),
    ("CEADU-2711", "AUS/NZL CMP21"),
]

# Layer3关键词
LAYER3_KEYWORDS = {
    "Cyber Security": ["cyber", "csms", "un-r 155", "security", "threat", "penetration"],
    "Data Security": ["data security", "privacy", "gdpr", "pdpa", "personal data", "encryption"],
    "OTA": ["ota", "over-the-air", "software update", "sums", "un-r 156"],
    "OBD": ["obd", "emission", "diagnostic", "un-r 83", "un-r 10"],
    "Functional Safety": ["functional safety", "fusa", "iso 26262", "sotif", "hazard", "asil"],
}


def download_attachments():
    """下载所有Parent工单的附件"""
    print("=" * 60)
    print("步骤1: 下载PSV/PVS附件")
    print("=" * 60)
    
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    EXCEL_DIR.mkdir(parents=True, exist_ok=True)
    
    headers = {
        "Authorization": f"Bearer {JIRA_TOKEN}",
        "X-Atlassian-Token": "no-check"
    }
    
    all_downloaded = []
    
    for ticket_key, desc in PARENT_TICKETS:
        print(f"\n[{ticket_key}] {desc}")
        
        try:
            resp = requests.get(
                f"{JIRA_URL}/rest/api/2/issue/{ticket_key}?fields=attachment,summary",
                headers=headers,
                timeout=30
            )
            
            if resp.status_code != 200:
                print(f"  ✗ HTTP {resp.status_code}")
                continue
            
            data = resp.json()
            attachments = data.get("fields", {}).get("attachment", [])
            
            # 筛选Excel文件
            excel_files = [
                a for a in attachments 
                if a.get("filename", "").lower().endswith(('.xlsx', '.xls'))
            ]
            
            print(f"  找到 {len(excel_files)} 个Excel附件")
            
            for att in excel_files:
                filename = att.get("filename", "")
                size = att.get("size", 0)
                
                # 下载
                resp = requests.get(
                    f"{JIRA_URL}/rest/api/2/issue/{ticket_key}/attachments/{filename}",
                    headers=headers,
                    timeout=60
                )
                
                if resp.status_code == 200:
                    # 保存到raw/pvs
                    pvs_name = f"{ticket_key}_{filename}"
                    pvs_path = RAW_DIR / pvs_name
                    pvs_path.write_bytes(resp.content)
                    
                    # 复制到raw/excel
                    excel_path = EXCEL_DIR / pvs_name
                    excel_path.write_bytes(resp.content)
                    
                    size_kb = size / 1024
                    print(f"  ✓ {filename} ({size_kb:.1f} KB)")
                    all_downloaded.append((pvs_path, ticket_key, desc))
                else:
                    print(f"  ✗ 下载失败: {filename}")
                    
        except Exception as e:
            print(f"  ✗ 错误: {e}")
    
    print(f"\n共下载 {len(all_downloaded)} 个文件")
    return all_downloaded


def parse_excel_to_wiki(excel_files):
    """解析Excel文件，生成Wiki文档"""
    print("\n" + "=" * 60)
    print("步骤2: 解析Excel → 生成Wiki")
    print("=" * 60)
    
    all_regulations = []
    
    for excel_path, ticket_key, desc in excel_files:
        print(f"\n解析: {excel_path.name}")
        
        try:
            wb = openpyxl.load_workbook(excel_path, data_only=True)
            
            for sheet_name in wb.sheetnames:
                sheet = wb[sheet_name]
                
                # 找表头行
                headers = []
                header_row = None
                
                for row_idx, row in enumerate(sheet.iter_rows(min_row=1, max_row=10, values_only=True), 1):
                    row_text = " ".join(str(c).lower() for c in row if c)
                    if any(kw in row_text for kw in ["regulation", "clause", "requirement"]):
                        headers = [str(c).lower().strip() if c else "" for c in row]
                        header_row = row_idx
                        break
                
                # 解析数据
                start_row = header_row + 1 if header_row else 2
                
                for row in sheet.iter_rows(min_row=start_row, values_only=True):
                    if not any(row):
                        continue
                    
                    row_text = " ".join(str(c).lower() for c in row if c)
                    if len(row_text) < 5:
                        continue
                    
                    # 匹配Layer3
                    matched_layer3 = []
                    for topic, keywords in LAYER3_KEYWORDS.items():
                        if any(kw in row_text for kw in keywords):
                            matched_layer3.append(topic)
                    
                    if matched_layer3:
                        row_data = {}
                        for i, cell in enumerate(row):
                            if i < len(headers) and headers[i]:
                                row_data[headers[i]] = str(cell) if cell else ""
                        
                        regulation = row_data.get("regulation", row[0] if len(row) > 0 else "")
                        clause = row_data.get("clause", row[1] if len(row) > 1 else "")
                        
                        if regulation:
                            reg_info = {
                                "ticket": ticket_key,
                                "market": desc,
                                "regulation": str(regulation),
                                "clause": str(clause),
                                "layer3": matched_layer3,
                                "raw_data": row_data,
                                "source": excel_path.name
                            }
                            all_regulations.append(reg_info)
            
            wb.close()
            print(f"  ✓ 提取完成")
            
        except Exception as e:
            print(f"  ✗ 错误: {e}")
    
    return all_regulations


def generate_wiki_docs(regulations):
    """生成Wiki文档"""
    print("\n" + "=" * 60)
    print("步骤3: 生成Wiki文档")
    print("=" * 60)
    
    WIKI_DIR.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. 生成汇总文档
    summary_lines = [
        "# PVS Layer3 法规汇总",
        "",
        f"**生成时间**: {timestamp}",
        f"**总计**: {len(regulations)} 条法规",
        f"**更新时间**: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## 统计",
        "",
    ]
    
    # 按Layer3统计
    layer3_count = {}
    market_count = {}
    
    for reg in regulations:
        for l3 in reg["layer3"]:
            layer3_count[l3] = layer3_count.get(l3, 0) + 1
        market_count[reg["market"]] = market_count.get(reg["market"], 0) + 1
    
    summary_lines.extend(["### 按Layer3分类", ""])
    for l3, count in sorted(layer3_count.items()):
        summary_lines.append(f"- **{l3}**: {count} 条")
    
    summary_lines.extend(["", "### 按市场分类", ""])
    for market, count in sorted(market_count.items()):
        summary_lines.append(f"- **{market}**: {count} 条")
    
    summary_lines.extend(["", "---", "", "## 完整列表", ""])
    
    for reg in regulations:
        layer3_str = ", ".join(reg["layer3"])
        summary_lines.append(
            f"- **{reg['regulation']}** {reg['clause']} - {layer3_str} "
            f"[{reg['market']}] ({reg['ticket']})"
        )
    
    # 按Layer3分组
    summary_lines.extend(["", "---", "", "## 按Layer3分组", ""])
    
    for layer3 in ["Cyber Security", "Data Security", "OTA", "OBD", "Functional Safety"]:
        regs = [r for r in regulations if layer3 in r["layer3"]]
        if regs:
            summary_lines.extend([f"### {layer3} ({len(regs)}条)", ""])
            for reg in regs:
                summary_lines.append(f"- {reg['regulation']} {reg['clause']} [{reg['market']}]")
            summary_lines.append("")
    
    summary_path = WIKI_DIR / "pvs_layer3_regulations_summary.md"
    summary_path.write_text("\n".join(summary_lines), encoding="utf-8")
    print(f"✓ 汇总: {summary_path.name}")
    
    # 2. 生成各市场的单独文档
    markets = set(reg["market"] for reg in regulations)
    
    for market in markets:
        market_regs = [r for r in regulations if r["market"] == market]
        
        lines = [
            f"# {market} - Layer3法规",
            "",
            f"**法规数量**: {len(market_regs)}",
            f"**更新时间**: {timestamp}",
            "",
            "## 法规列表",
            "",
        ]
        
        # 按Layer3分组
        for layer3 in ["Cyber Security", "Data Security", "OTA", "OBD", "Functional Safety"]:
            regs = [r for r in market_regs if layer3 in r["layer3"]]
            if regs:
                lines.extend([f"### {layer3}", ""])
                for reg in regs:
                    lines.append(f"#### {reg['regulation']} - {reg['clause']}")
                    lines.append("")
                    lines.append(f"- **Layer3**: {', '.join(reg['layer3'])}")
                    lines.append(f"- **来源**: {reg['source']}")
                    lines.append(f"- **工单**: {reg['ticket']}")
                    if reg["raw_data"]:
                        for k, v in list(reg["raw_data"].items())[:5]:
                            if v and k not in ["regulation", "clause"]:
                                lines.append(f"- **{k}**: {v}")
                    lines.append("")
        
        market_file = market.replace("/", "_").replace(" ", "_").lower()
        market_path = WIKI_DIR / f"pvs_market_{market_file}.md"
        market_path.write_text("\n".join(lines), encoding="utf-8")
        print(f"✓ 市场: {market_path.name}")
    
    # 3. 生成关联文档 - 跨市场对比
    correlation_lines = [
        "# Layer3法规跨市场关联",
        "",
        f"**生成时间**: {timestamp}",
        "",
        "## 法规对照表",
        "",
        "| 法规 | 条款 | Cyber Sec | Data Sec | OTA | OBD | Fusa |",
        "|------|------|-----------|----------|-----|-----|------|"
    ]
    
    # 找到所有唯一的法规
    unique_regs = {}
    for reg in regulations:
        key = f"{reg['regulation']}_{reg['clause']}"
        if key not in unique_regs:
            unique_regs[key] = {
                "regulation": reg["regulation"],
                "clause": reg["clause"],
                "markets": set(),
                "layer3": set()
            }
        unique_regs[key]["markets"].add(reg["market"])
        unique_regs[key]["layer3"].update(reg["layer3"])
    
    for reg_key, info in sorted(unique_regs.items()):
        cs = "✓" if "Cyber Security" in info["layer3"] else "-"
        ds = "✓" if "Data Security" in info["layer3"] else "-"
        ota = "✓" if "OTA" in info["layer3"] else "-"
        obd = "✓" if "OBD" in info["layer3"] else "-"
        fusa = "✓" if "Functional Safety" in info["layer3"] else "-"
        
        markets_str = ", ".join(sorted(info["markets"]))[:30]
        
        correlation_lines.append(
            f"| {info['regulation']} | {info['clause']} | {cs} | {ds} | {ota} | {obd} | {fusa} |"
        )
    
    correlation_path = WIKI_DIR / "pvs_regulation_correlation.md"
    correlation_path.write_text("\n".join(correlation_lines), encoding="utf-8")
    print(f"✓ 关联: {correlation_path.name}")
    
    return len(regulations)


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("PSV/PVS 一键下载 → Wiki生成")
    print("=" * 60)
    
    # 步骤1: 下载
    downloaded = download_attachments()
    
    if not downloaded:
        print("\n没有下载到任何文件!")
        return
    
    # 步骤2: 解析
    regulations = parse_excel_to_wiki(downloaded)
    
    print(f"\n共提取 {len(regulations)} 条Layer3法规")
    
    # 步骤3: 生成Wiki
    if regulations:
        count = generate_wiki_docs(regulations)
        
        print("\n" + "=" * 60)
        print("完成!")
        print("=" * 60)
        print(f"✓ 下载: {len(downloaded)} 个Excel文件")
        print(f"✓ 提取: {count} 条Layer3法规")
        print(f"✓ Wiki: {WIKI_DIR}")
    else:
        print("\n未提取到Layer3法规")


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
