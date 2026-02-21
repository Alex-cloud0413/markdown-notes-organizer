#!/usr/bin/env python3
"""
scripts/extract_keywords.py
功能：读取 scan_notes.py 的输出，分析每个笔记的内容，提取关键词和分类。
"""

import json
import argparse
import sys
import re
from collections import Counter

# 预定义一些简单的关键词映射规则 (可以根据需要扩展)
CATEGORY_RULES = {
    "编程技术": ["python", "java", "javascript", "code", "api", "git", "bash", "linux", "server"],
    "生活记录": ["日记", "感悟", "生活", "旅行", "plan", "shopping"],
    "工作项目": ["meeting", "report", "project", "deadline", "需求", "会议"],
    "阅读笔记": ["book", "reading", "读书", "笔记", "摘要", "quote"]
}

def extract_from_content(content):
    """从文本内容中提取关键词和推断分类"""
    # 1. 简单的分词（以空格和常见标点分隔）
    # 注意：这只是一个简单的实现，对中文支持有限。生产环境建议用 jieba 或 transformers
    words = re.split(r'\s+|[,.，。!！?？:：]', content.lower())
    words = [w for w in words if len(w) > 1] # 过滤掉单字
    
    # 2. 统计词频提取关键词
    word_counts = Counter(words)
    # 过滤掉常见停用词 (这里仅示例几个)
    stop_words = {"the", "and", "is", "in", "to", "of", "a", "for", "with", "的", "了", "是", "在", "和"}
    keywords = [w for w, c in word_counts.most_common(20) if w not in stop_words][:5]
    
    # 3. 基于规则推断分类
    category = "未分类"
    max_score = 0
    
    for cat, rules in CATEGORY_RULES.items():
        score = sum(1 for w in words if w in rules)
        if score > max_score:
            max_score = score
            category = cat
            
    return keywords, category

def analyze_files(scan_data):
    analyzed_files = []
    
    for file_info in scan_data.get("files", []):
        file_path = file_info["path"]
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            keywords, category = extract_from_content(content)
            
            # 更新文件信息，加入分析结果
            file_info["keywords"] = keywords
            file_info["category"] = category
            # 截取前100个字符作为摘要预览
            file_info["summary_preview"] = content[:100].replace('\n', ' ') + "..."
            
            analyzed_files.append(file_info)
            
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}", file=sys.stderr)
            file_info["error"] = str(e)
            analyzed_files.append(file_info)

    return analyzed_files

def main():
    parser = argparse.ArgumentParser(description="Analyze Markdown files for keywords.")
    parser.add_argument("--input", required=True, help="Input JSON file from scan_notes.py")
    parser.add_argument("--output", required=True, help="Output JSON file for analysis results")
    
    args = parser.parse_args()
    
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            scan_data = json.load(f)
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
        
    print("Analyzing file contents...")
    analyzed_files = analyze_files(scan_data)
    
    result = {
        "analysis_timestamp": scan_data.get("scan_timestamp"),
        "total_analyzed": len(analyzed_files),
        "files": analyzed_files
    }
    
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Analysis complete. Results saved to {args.output}")
    except IOError as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
