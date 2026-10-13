# doc-curate · 资料整理

> 把任意来源的资料（外文 PDF、CAJ、扫描件、Word、PPT、EPUB）整理为结构化的多种产物
> —— md（模块/标签化）、Word 成稿、用户指定的其他格式。

**翻译只是常用功能之一，不是全部。**

---

## 特性

- **多来源支持**：PDF 文字版、PDF 扫描件、CAJ、Word、PPT、EPUB
- **多产物输出**：md（模块/标签化）+ Word 成稿 + 用户指定的其他
- **动作随场景变**：翻译场景含翻译，校对场景不含；中文资料整理不含翻译
- **五阶段工作流**：用户提供 → 探查 → 提取 → 处理 → 校验 → 导出
- **可中断可续跑**：每阶段回写 PROGRESS.md，下次开工自动定位
- **三级错误处置**：hard_error / soft_error / warning
- **三级规则分级**：硬约束 / 翻译规则 / 建议
- **通用/专用术语库**：自动查/增/统计
- **模块/标签化**：自然结构 / 按页分割 / 按内容标签
- **多产物组装走脚本**：禁止 agent 硬堆产物

---

## 工作流五阶段

```
0 用户提供 → 1 探查 → 2 提取 → 3 处理 → 4 校验 → 5 导出
```

| 阶段 | 关键动作 | 硬门 |
|---|---|---|
| **0 用户提供** | 4 种输入形式 + 简单整理 PARAMS | 无 |
| **1 探查** | 智能补全 + 信息对照 + 工作流确认 + 术语库确认 + 提问 | 等用户确认决策 |
| **2 提取** | 按类型分文件夹抽取 + 工具开关启用 | 等用户确认 |
| **3 处理** | PIPELINE 子动作（翻译/术语/模块化/校对） | 不设（阶段 4 统一校验） |
| **4 校验** | 术语扫描（必）+ 上下文/查证/预测（按需） | 等用户确认 |
| **5 导出** | 多产物组装（md + Word + 用户声明） | 不设 |

---

## 目录结构

```
<动作><原后缀>：<源文件名（去后缀）>/
├── 1 源/                    # 源文件 + PARAMS.md
├── 2 临时文件/                # skill 脚本的运行实例
├── 3 提取内容/
│   ├── 文字/                  # md 原文
│   ├── 表格/                  # md + json
│   ├── 图片/                  # 原始图片
│   └── <其他>/                # 扩展
├── 4 处理内容/
│   ├── 专用术语表.md / .json
│   └── PIPELINE 中间产物
├── 5 阶段性工作报告/           # 阶段 1-4 报告
└── 6 输出成果/                # md / Word / 用户指定
```

文件夹命名：`<动作><原后缀>：<源文件名去后缀>`
- 动作：翻译 / 校对 / 整理 / 提取 / 转换（预留扩展）
- 格式：原后缀（PDF / DOCX / PPTX / EPUB / CAJ）

---

## 安装

将 `SKILL.md` 注册到你的 agent 平台的 skill 加载目录（如 `~/.agents/skills/`）。

```bash
# 克隆
git clone https://github.com/WeirdoKK667/doc-curate.git ~/.agents/skills/doc-curate
```

依赖（按需）：
- `pdfplumber`（PDF 文字/表格）
- `PyMuPDF` / `fitz`（PDF 图片/渲染）
- `python-docx`（Word）
- `python-pptx`（PPT）
- `ebooklib`（EPUB）
- `caj2pdf`（CAJ 转换）
- `pytesseract` / `paddleocr`（OCR，可选）

---

## 使用示例

### 触发 skill

用自然语言表达需求，skill 自动识别：

```
翻译 D:/papers/kuznets_1966.pdf 第 5-30 页
整理工作区里的 source.pdf，按内容打标签
扫描件 source.pdf 转 Word 并校对
CAJ 文献 cnki_001.caj 翻译并导出 md + Word
```

### skill 响应流程

1. **阶段 0**：解析输入，整理 `1 源/PARAMS.md`
2. **阶段 1**：探查源文件，补全 PARAMS，输出对照表，等用户确认
3. **阶段 2**：按类型抽取到 `3 提取内容/`，等用户确认
4. **阶段 3**：按 PIPELINE 处理（翻译/术语/模块化/校对）
5. **阶段 4**：术语扫描 + 上下文联系 + 校验报告，等用户确认
6. **阶段 5**：组装 md + Word 到 `6 输出成果/`

---

## 适用与不适用

### 适用

| 来源 | 典型场景 | 默认产物 |
|---|---|---|
| PDF 文字版 | 外文文献翻译、中文资料整理 | md + Word |
| PDF 扫描件 | 扫描件转写 | md + Word |
| CAJ | 知网文献 | md + Word |
| Word | 中文资料整理、文档转换 | md + Word |
| PPT | 课件整理、报告整理 | md + Word |
| EPUB | 电子书整理 | md + Word |

### 不适用

- 实时翻译（同传/口译）
- 代码注释/API 文档
- 字幕翻译
- 网页内容抓取
- 短消息/聊天记录
- 实时视频流 OCR
- 图像编辑/分类
- 单页快翻

---

## 文件清单

```
doc-curate/
├── SKILL.md                              # 主文档
├── README.md                             # 项目说明（本文件）
├── LICENSE                               # MIT 许可证
├── .gitignore                            # 忽略规则
├── references/                           # 7 个细则
│   ├── workflow-detail.md                # 5 阶段完整细则
│   ├── translate-rules.md                # 翻译场景规则
│   ├── format-adapter.md                 # 7 种格式适配
│   ├── output-formats.md                 # md + Word 版式
│   ├── proofread-rules.md                # 阶段 4 子动作
│   ├── qa-checks.md                      # 硬/软检查标准
│   └── troubleshooting.md                # 常见报错
├── assets/                               # 5 个模板
│   ├── params-template.md                # PARAMS 完整模板
│   ├── glossary-template.md              # 术语表双格式模板
│   ├── md-template.md                    # md 模块化模板
│   ├── zh-md-schema.md                   # 翻译稿标签格式
│   └── manifest-schema.json              # 素材清单 schema
└── scripts/                              # 13 个脚本
    ├── probe.py                          # 阶段 1
    ├── format_adapter.py                 # 阶段 2（CAJ/Word/PPT/EPUB）
    ├── extract.py                        # 阶段 2
    ├── ocr.py                            # 阶段 2（按需）
    ├── process.py                        # 阶段 3
    ├── scan_terms.py                     # 阶段 4
    ├── qa.py                             # 阶段 4
    ├── build_md.py                       # 阶段 5
    ├── build_docx.py                     # 阶段 5
    ├── build_toc_docx.py                 # 阶段 5
    ├── tag_index.py                      # 标签索引
    ├── tag_query.py                      # 标签查询
    └── tag_register.py                   # 标签注册
```

---

## 贡献

欢迎贡献！主要方向：
- 新格式适配器（如 .md / .html / .rtf）
- 翻译规则细化（按学科）
- 校验算法增强
- 模板与版式扩展

提交前请阅读 `references/` 下的相关细则。

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。

---

## 相关项目

- 参考文档：`参考/外文资料翻译.md`（基于真实项目 `work_stage1/` 提炼）
- 测试工作区：`C:\Users\91094\Desktop\澳洲三矿\测试`（端到端测试）
