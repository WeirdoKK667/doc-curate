# format-adapter.md · 输入格式适配

> 每种输入格式的读取库、关键参数、异常处置。

---

## 一、PDF 文字版（默认）

### 读取库
- **pdfplumber**：文字、表格、字体信息
- **PyMuPDF (fitz)**：图片、渲染、元数据

### 关键能力
- 文字抽取（按页）
- 表格抽取（`extract_tables`）
- 图片抽取（`get_images(full=True)`）
- 元数据（作者、年份、加密、字体清单）

### 异常处置
- 加密 PDF → `hard_error`，提示用户解密
- 总页数 < 起止页 → `hard_error`
- 单页可提取文字 < 80 字符 → 标 `need_ocr=true`

---

## 二、PDF 扫描件（SCAN=on）

### 读取库
- **PyMuPDF (fitz)**：渲染为图（300dpi）
- **subagent 视觉识别**（默认 OCR_BACKEND）：读图转写

### 工作流
1. 阶段 2 跳过 pdfplumber 文本抽取
2. 全部页渲染 300dpi 图：`p{N}_fullpage.png`
3. 逐页视觉识别转写（而非 OCR 引擎）
4. 输出 `p{N}.md`，同时在 manifest 标 `ocr_confidence: high/mid/low`

### OCR 置信度
| 置信度 | 处置 |
|---|---|
| high | 直接进阶段 3 |
| mid | 标记但继续 |
| low | **自动转人工复读**（强制走 subagent 视觉识别重做） |

### 特殊场景
- 手写体、褪色页、竖排日文 → 直接标 `[?]`
- BATCH 建议降到 3

---

## 三、CAJ

### 读取库
- **caj2pdf**（开源 GitHub）：`.caj` → `.pdf`

### 工作流
```
.caj 文件 → [caj2pdf 适配层] → .pdf → 原 PDF 工作流
```

### 成功率
- 旧版 caj：~95%
- 新版 caj（含 2020 年后部分加密版）：~70%

### 异常处置
- 转换失败 → 写 `ISSUES.md`，提示用户改用 CAJViewer 手动导出 PDF
- caj 文件其实是 PDF 封装 → 重命名 `.caj` → `.pdf`，走原 PDF 工作流

---

## 四、Word（DOCX）

### 读取库
- **python-docx**：段落、表格、图片、样式

### 关键能力
- 段落（含样式：标题/正文/列表）
- 表格（`doc.tables`）
- 图片（`inline_shapes`）
- 页眉页脚

### 异常处置
- 文件损坏 → `hard_error`
- 受保护文档 → `hard_error`，提示用户解除保护

---

## 五、PPT（PPTX）

### 读取库
- **python-pptx**：幻灯片、文字、图片、备注

### 关键能力
- 幻灯片（`slides`）
- 占位符文字
- 图片（`shapes`）
- 备注（`notes_slide`）
- 版式信息

### 工作流
- 按幻灯片序号抽取
- 每张幻灯片输出独立 md 块
- 图片单独存放 `3 提取内容/图片/`

---

## 六、EPUB

### 读取库
- **ebooklib**：章节、HTML 内容、元数据

### 关键能力
- 章节结构（`spine`、`toc`）
- HTML 内容（`items`）
- 元数据（作者、书名、语言）

### 工作流
1. 按章节抽取 HTML 内容
2. 转为 markdown
3. 图片单独存放
4. 章节标题自动识别 → Heading

---

## 七、读文件脚本接口

每个适配器提供统一接口：

```python
def extract(input_path: str, output_dir: str, params: dict) -> dict:
    """
    返回 manifest：
    {
      "format": "pdf/caj/docx/pptx/epub",
      "pages": [...],
      "text_files": [...],
      "tables": [...],
      "images": [...],
      "anomalies": [...],
      "extraction_confidence": "high/mid/low"
    }
    """
```

### 适配器清单

| 格式 | 适配器 | 调用 |
|---|---|---|
| PDF 文字版 | `extract_pdf_text.py` | 默认 |
| PDF 扫描件 | `extract_pdf_scan.py` | SCAN=on |
| CAJ | `convert_caj.py` | INPUT_FORMAT=caj |
| Word | `extract_docx.py` | INPUT_FORMAT=docx |
| PPT | `extract_pptx.py` | INPUT_FORMAT=pptx |
| EPUB | `extract_epub.py` | INPUT_FORMAT=epub |

---

## 八、统一中间格式

### 设计选择
**所有输入最终统一为 PDF + 文本/md 混合**——阶段 3 不区分原始格式。

### 理由
- 简化阶段 3 处理逻辑
- 复用 PDF 工作流的脚本
- 章节定位、页码标注统一

### 例外
- Word/PPT/EPUB 直接产出的 md 含原格式信息（标题级别、列表样式）
- 阶段 5 组装时按 INPUT_FORMAT 选对应版式
