---
name: markdown-notes-organizer
description: 智能扫描、分类和总结指定目录下的 Markdown 笔记。具备自动发现文件、提取关键词、生成分类索引目录（Index）以及创建内容总结报告的能力。适用于个人知识库整理、文档归类和学习笔记管理。
allowed-tools: "Bash(python {baseDir}/scripts/* {baseDir}/* :*), Read, Write"
---

# Markdown 笔记智能整理与 AI 总结 Skill

## 1. 技能概述
本技能旨在帮助用户自动化整理混乱的 Markdown 笔记库。通过一系列 Python 脚本，它可以扫描目录结构、分析笔记内容提取关键词、按主题分类，并最终生成一份结构化的索引文件（INDEX.md）和总结报告。

## 2. 核心能力与工作流

当用户请求整理笔记、生成目录或分析知识库时，请按照以下步骤执行：

### 第一阶段：扫描 (Discovery)
首先，需要了解目标目录中有哪些文件。
*   **动作**：使用 `scan_notes.py` 脚本。
*   **命令格式**：
    ```bash
    python {baseDir}/scripts/scan_notes.py --directory "目标目录路径" --output "scan_result.json"
    ```
*   **目的**：获取所有 .md 文件的路径、大小、修改时间等元数据。

### 第二阶段：分析 (Analysis)
基于扫描结果，分析每个笔记的内容以提取特征。
*   **动作**：使用 `extract_keywords.py` 脚本。
*   **命令格式**：
    ```bash
    python {baseDir}/scripts/extract_keywords.py --input "scan_result.json" --output "keywords.json"
    ```
*   **目的**：读取每个笔记的内容，提取前 5 个关键词，并确定其所属分类（如：编程、日记、会议记录等）。

### 第三阶段：生成 (Generation)
最后，根据分析结果生成用户可视化的成果。
*   **动作**：使用 `generate_index.py` 脚本。
*   **命令格式**：
    ```bash
    python {baseDir}/scripts/generate_index.py --keywords "keywords.json" --template "{baseDir}/templates/index_template.md" --output "INDEX.md"
    ```
*   **目的**：生成一个带有分类导航和统计信息的 Markdown 索引文件。

## 3. 使用场景示例

**场景 A：用户想整理某个文件夹**
> 用户输入：“帮我整理一下 `/Users/alex/Documents/Obsidian` 里的笔记。”
> **Claude 响应策略**：
> 1. 确认目标路径。
> 2. 依次运行 扫描 -> 提取 -> 生成 脚本。
> 3. 告知用户整理完成，并展示 `INDEX.md` 的预览或统计数据。

**场景 B：用户想了解笔记库的主题分布**
> 用户输入：“看看我最近都在写什么内容的笔记？”
> **Claude 响应策略**：
> 1. 运行 扫描 和 提取 脚本。
> 2. 读取 `keywords.json`。
> 3. 基于 JSON 数据直接回答用户的统计问题（例如：“你主要在写 Python 和 React 相关的内容...”），而不需要生成 INDEX 文件。

## 4. 错误处理指南
*   **目录不存在**：如果 `scan_notes.py` 报错提示目录不存在，请立即请求用户核对路径。
*   **权限问题**：如果遇到 Permission denied，尝试建议用户检查文件夹权限。
*   **无 Markdown 文件**：如果扫描结果为空，请礼貌地告知用户该目录下似乎没有笔记文件。

## 5. 参考资源
*   关于推荐的笔记目录结构，请参考：[最佳实践](references/3.1_best_practices.md)
*   关于如何选择最佳关键词，请参考：[关键词指南](references/3.2_keywords_guide.md)