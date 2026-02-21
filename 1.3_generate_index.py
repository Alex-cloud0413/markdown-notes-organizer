#!/usr/bin/env python3
"""
scripts/generate_index.py
功能：基于分析结果，使用模板生成最终的 INDEX.md 索引文件。
"""

import json
import argparse
import sys
from datetime import datetime
from collections import defaultdict

def load_template(template_path):
    """读取模板文件，如果不存在则使用默认简单模板"""
    if template_path and os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # 内置默认模板，防止模板文件丢失导致报错
        return "# 笔记索引\n\n自动生成于: {date}\n\n{content}"

import os # 补上 import

def generate_markdown(data, template_template):
    # 1. 按分类聚合文件
    files_by_category = defaultdict(list)
    for file in data.get("files", []):
        cat = file.get("category", "未分类")
        files_by_category[cat].append(file)
    
    # 2. 构建核心内容块
    content_parts = []
    
    # 统计概览
    total_files = data.get("total_analyzed", 0)
    categories_count = len(files_by_category)
    content_parts.append(f"## 📊 概览\n")
    content_parts.append(f"- **总笔记数**: {total_files}")
    content_parts.append(f"- **涵盖主题**: {categories_count} 个分类\n")
    
    # 分类列表
    for category, files in sorted(files_by_category.items()):
        content_parts.append(f"### 📂 {category} ({len(files)})\n")
        
        # 制作表格
        content_parts.append("| 文件名 | 关键词 | 摘要 |")
        content_parts.append("| :--- | :--- | :--- |")
        
        for f in files:
            name = f.get("filename", "Unknown")
            path = f.get("relative_path", "")
            # 创建文件链接 [Name](Path)
            link = f"[{name}]({path})"
            keywords = ", ".join(f.get("keywords", []))
            summary = f.get("summary_preview", "").replace("|", "\|") # 转义表格符
            
            content_parts.append(f"| {link} | {keywords} | {summary} |")
        
        content_parts.append("\n")
        
    content_body = "\n".join(content_parts)
    
    # 3. 填充模板
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    final_output = template_template.replace("{{date}}", current_date)
    final_output = final_output.replace("{{content}}", content_body)
    
    return final_output

def main():
    parser = argparse.ArgumentParser(description="Generate INDEX.md from analysis results.")
    parser.add_argument("--keywords", required=True, help="Input JSON file (keywords.json)")
    parser.add_argument("--template", help="Path to Markdown template file")
    parser.add_argument("--output", required=True, help="Path to output INDEX.md file")
    
    args = parser.parse_args()
    
    try:
        with open(args.keywords, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
        
    # 加载模板
    template_content = load_template(args.template)
    
    print("Generating index...")
    markdown_output = generate_markdown(data, template_content)
    
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        print(f"Index generated successfully at: {args.output}")
    except IOError as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
