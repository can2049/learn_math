---
name: pdf-to-markdown
description: >-
  将 PDF 论文转换为 Markdown 文件，保留数学公式可读性和学术论文排版结构。
  支持本地 PDF 文件和网页 PDF 链接。使用项目中已配置的 uv + markitdown 工具链。
  触发词：pdf转markdown、PDF转换、下载论文、准备论文、convert pdf、pdf to md、
  论文预处理、准备阅读材料、pdf2md。
  本 skill 是 paper-reading skill 的前置步骤，用于准备输入材料。
---

# PDF to Markdown — 论文 PDF 转 Markdown

## 适用场景

为 paper-reading skill 准备输入材料。将学术论文 PDF 转为 Markdown，
使公式保持可读、章节结构清晰，便于后续深度阅读分析。

## 前置条件

项目根目录已通过 uv 管理 Python 虚拟环境，并安装了：
- `markitdown`：PDF → Markdown 转换
- `pdfplumber`：PDF 文本提取（备用方案）

## 输入形式

1. **本地 PDF 文件路径** — 直接使用
2. **网页 PDF 链接**（arXiv、会议官网等）— 先下载到 `temp/` 再转换

## 工作流程

```
Task Progress:
- [ ] Step 1: 确定输入来源（本地路径 or URL）
- [ ] Step 2: 如果是 URL，下载 PDF 到 temp/ 目录
- [ ] Step 3: 执行转换
- [ ] Step 4: 检查输出质量并做后处理
- [ ] Step 5: 输出最终 Markdown 文件路径
```

### Step 1: 确定输入来源

- 用户提供本地路径 → 用 `file` 命令确认是 PDF
- 用户提供 URL → 进入 Step 2 下载

### Step 2: 下载 PDF（仅 URL 场景）

```bash
cd <project_root>
mkdir -p temp

# 对 arXiv 链接：将 abs 页面转为 pdf 链接
# https://arxiv.org/abs/2301.00001 → https://arxiv.org/pdf/2301.00001

curl -L -o "temp/<paper_id>.pdf" "<pdf_url>"
file "temp/<paper_id>.pdf"   # 确认是 PDF
```

若 URL 无明显 paper ID，用论文标题或日期命名。

### Step 3: 执行转换

运行项目内的转换脚本：

```bash
cd <project_root>
uv run python .cursor/skills/pdf-to-markdown/scripts/pdf2md.py \
  "temp/<paper_id>.pdf" \
  -o "temp/<paper_id>.md"
```

脚本会：
1. 先尝试 `markitdown` 转换
2. 检查输出质量（字符碎片率、空白率等）
3. 如果质量不佳，回退到 `pdfplumber` 提取
4. 对提取结果做后处理：修复缺失空格、清理乱码行、标准化公式格式

### Step 4: 检查输出质量

读取生成的 Markdown 文件，人工检查：
- 标题和章节结构是否完整
- 公式是否可读（非乱码）
- 正文段落是否连贯

如有明显问题，可手动编辑修正或重新运行脚本调整参数。

### Step 5: 输出结果

告知用户 Markdown 文件路径，供 paper-reading skill 使用。

## 与 paper-reading skill 的协作

当 paper-reading skill 收到 PDF 文件或 PDF 链接时：
1. 先调用本 skill 将 PDF 转为 Markdown
2. 再用 `Read` 工具读取 Markdown 内容
3. 按 paper-reading 流程进行深度阅读分析

## 注意事项

- arXiv URL 格式转换：`/abs/` → `/pdf/`
- 下载的 PDF 和输出的 Markdown 统一放在 `temp/` 目录
- 文件名保持一致，仅后缀不同：`xxx.pdf` → `xxx.md`
- 如果 PDF 是扫描件（图片型），当前工具链效果有限，需提醒用户
