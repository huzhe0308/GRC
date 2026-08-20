#!/usr/bin/env python3
"""解析本地PSV/PVS Excel文件，转换为Wiki格式"""

import os
import sys
import re
from pathlib import Path

try:
    import openpyxl
except ImportError:
    print("需要安装 openpyxl: pip install openpyxl")
    sys.exit(1)

# Layer3关键词
LAYER3_KEYWORDS = {
    "Cyber Security": ["cyber", "cybersecurity", "csms", "un-r 155", "security event", "threat", "penetration", "security"],
    "Data Security": ["data security", "privacy", "gdpr", "pdpa", "personal data", "encryption", "data protection", "privacy"],
    "OTA": ["ota", "over-the-air", "software update", "sums", "un-r 156", "update"],
    "OBD": ["obd", "on-board diagnostic", "emission", "diagnostic", "un-r 83", "un-r 10", "diagnostics"],
    "Functional Safety": ["functional safety", "fusa", "iso 26262", "sotif", "hazard", "asil", "safety"],
}

MARKET_KEYWORDS = {
    "Korea": ["korea", "korean", "r.o.k"],
    "India": ["india", "indian", "ais"],
    "ASEAN": ["asean", "rhd", "lhd", "thailand", "malaysia", "singapore", "vietnam"],
    "Middle East": ["middle east", "uae", "gcc", "gulf"],
    "Kazakhstan": ["kazakhstan", "kz", "tr cu"],
    "Uzbekistan": ["uzbekistan", "uz"],
    "Turkey": ["turkey", "türkiye"],
    "AUS/NZL": ["australia", "aussie", "nz", "new zealand"],
}


def parse_excel_to_markdown(excel_path: Path) -> tuple[str, list]:
    """解析Excel文件，返回Markdown内容和提取的法规"""
    
    filename = excel_path.stem  # 不带扩展名的文件名
    regulations = []
    
    try:
        wb = openpyxl.load_workbook(excel_path, data_only=True)
        
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            
            # 找到表头行
            headers = []
            header_row_idx = None
            
            for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=10, values_only=True), 1):
                if row and any(cell for cell in row):
                    row_text = " ".join(str(c).lower() for c in row if c)
                    if any(kw in row_text for kw in ["regulation", "clause", "requirement", "article", "section"]):
                        headers = [str(c).lower().strip() if c else "" for c in row]
                        header_row_idx = row_idx
                        break
            
            if not headers:
                headers = ["regulation", "clause", "description", "market", "layer3", "status"]
            
            # 解析数据行
            start_row = header_row_idx + 1 if header_row_idx else 2
            
            for row in ws.iter_rows(min_row=start_row, values_only=True):
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
                
                # 匹配市场
                matched_markets = []
                for market, keywords in MARKET_KEYWORDS.items():
                    if any(kw in row_text for kw in keywords):
                        matched_markets.append(market)
                
                # 创建法规条目
                row_data = {}
                for i, cell in enumerate(row):
                    if i < len(headers) and headers[i]:
                        row_data[headers[i]] = str(cell) if cell else ""
                
                regulation = row_data.get("regulation", row[0] if len(row) > 0 else "")
                clause = row_data.get("clause", row[1] if len(row) > 1 else "")
                description = row_data.get("description", row[2] if len(row) > 2 else "")
                status = row_data.get("status", "Required")
                
                if regulation and matched_layer3:
                    regulations.append({
                        "regulation": str(regulation),
                        "clause": str(clause),
                        "description": str(description)[:200],
                        "layer3": matched_layer3,
                        "market": matched_markets[0] if matched_markets else "General",
                        "status": str(status),
                        "source": filename
                    })
        
        wb.close()
        
    except Exception as e:
        print(f"  解析错误: {e}")
    
    return generate_markdown(filename, regulations), regulations


def generate_markdown(title: str, regulations: list) -> str:
    """生成Markdown文档"""
    
    md_lines = [
        f"# {title} - Layer3法规清单",
        "",
        f"**生成时间**: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}",
        f"**法规数量**: {len(regulations)}",
        "",
        "## Layer3 Topics",
        "",
        "- Cyber Security",
        "- Data Security",
        "- OTA (Over-The-Air)",
        "- OBD (On-Board Diagnostics)",
        "- Functional Safety",
        "",
        "---",
        "",
        "## 法规条目",
        "",
    ]
    
    # 按Layer3分组
    by_layer3 = {}
    for reg in regulations:
        for layer3 in reg["layer3"]:
            if layer3 not in by_layer3:
                by_layer3[layer3] = []
            by_layer3[layer3].append(reg)
    
    for layer3, regs in by_layer3.items():
        md_lines.append(f"### {layer3} ({len(regs)} 条)")
        md_lines.append("")
        
        for reg in regs:
            md_lines.append(f"#### {reg['regulation']} - {reg['clause']}")
            md_lines.append("")
            md_lines.append(f"- **市场**: {reg['market']}")
            md_lines.append(f"- **状态**: {reg['status']}")
            md_lines.append(f"- **描述**: {reg['description']}")
            md_lines.append("")
    
    return "\n".join(md_lines)


def main():
    """主函数"""
    # 源目录和目标目录
    source_dir = Path(r"C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki\raw\pvs")
    output_dir = Path(r"C:\Users\T1UKLL7\Desktop\Workstation\employee agent\_archive_llm_wiki")
    
    if not source_dir.exists():
        print(f"源目录不存在: {source_dir}")
        return
    
    # 获取所有Excel文件
    excel_files = list(source_dir.glob("*.xlsx")) + list(source_dir.glob("*.xls"))
    
    if not excel_files:
        print(f"没有找到Excel文件: {source_dir}")
        return
    
    print(f"找到 {len(excel_files)} 个Excel文件")
    print("-" * 50)
    
    all_regulations = []
    
    for excel_file in excel_files:
        print(f"\n处理: {excel_file.name}")
        
        md_content, regulations = parse_excel_to_markdown(excel_file)
        
        if regulations:
            print(f"  提取到 {len(regulations)} 条Layer3法规")
            
            # 保存为Wiki文档
            wiki_name = excel_file.stem.replace(" ", "_")
            wiki_path = output_dir / "queries" / f"pvs_{wiki_name}.md"
            
            with open(wiki_path, "w", encoding="utf-8") as f:
                f.write(md_content)
            
            print(f"  保存: {wiki_path.name}")
            
            all_regulations.extend(regulations)
        else:
            print(f"  未提取到Layer3法规")
    
    # 生成汇总文档
    print("\n" + "=" * 50)
    print(f"完成! 共提取 {len(all_regulations)} 条法规")
    
    # 汇总
    summary_path = output_dir / "queries" / "pvs_layer3_regulations_summary.md"
    summary_lines = [
        "# PVS Layer3 法规汇总",
        "",
        f"**生成时间**: {__import__('time').strftime('%Y-%m-%d %H:%M:%S')}",
        f"**总计**: {len(all_regulations)} 条法规",
        "",
    ]
    
    # 统计
    layer3_count = {}
    market_count = {}
    
    for reg in all_regulations:
        for layer3 in reg["layer3"]:
            layer3_count[layer3] = layer3_count.get(layer3, 0) + 1
        market_count[reg["market"]] = market_count.get(reg["market"], 0) + 1
    
    summary_lines.extend([
        "## 按Layer3分类",
        "",
    ])
    for layer3, count in sorted(layer3_count.items()):
        summary_lines.append(f"- **{layer3}**: {count} 条")
    
    summary_lines.extend([
        "",
        "## 按市场分类",
        "",
    ])
    for market, count in sorted(market_count.items()):
        summary_lines.append(f"- **{market}**: {count} 条")
    
    summary_lines.extend([
        "",
        "---",
        "",
        "## 完整法规列表",
        "",
    ])
    
    for reg in all_regulations:
        summary_lines.append(f"- {reg['regulation']} {reg['clause']} - {reg['layer3']} ({reg['market']})")
    
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))
    
    print(f"\n汇总保存: {summary_path.name}")


if __name__ == "__main__":
    main()
    input("\n按回车键退出...")
