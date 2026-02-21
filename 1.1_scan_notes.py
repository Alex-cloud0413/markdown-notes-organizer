#!/usr/bin/env python3
"""
scripts/scan_notes.py
功能：递归扫描指定目录，发现所有 .md 文件并收集基本元数据。
"""

import os
import sys
import json
import argparse
from datetime import datetime

def scan_directory(directory):
    """递归扫描目录，返回文件列表元数据"""
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
        sys.exit(1)

    markdown_files = []
    
    # 递归遍历目录
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    stats = os.stat(file_path)
                    markdown_files.append({
                        "path": file_path,
                        "filename": file,
                        "relative_path": os.path.relpath(file_path, directory),
                        "size": stats.st_size,
                        "last_modified": datetime.fromtimestamp(stats.st_mtime).isoformat()
                    })
                except OSError as e:
                    print(f"Warning: Could not access {file_path}: {e}", file=sys.stderr)

    return markdown_files

def main():
    parser = argparse.ArgumentParser(description="Scan directory for Markdown files.")
    parser.add_argument("--directory", required=True, help="Path to the directory to scan")
    parser.add_argument("--output", required=True, help="Path to output JSON file")
    
    args = parser.parse_args()
    
    print(f"Scanning directory: {args.directory}...")
    files = scan_directory(args.directory)
    
    result = {
        "scan_timestamp": datetime.now().isoformat(),
        "root_directory": os.path.abspath(args.directory),
        "total_files": len(files),
        "files": files
    }
    
    # 写入结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Successfully scanned {len(files)} files. Results saved to {args.output}")
    except IOError as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
