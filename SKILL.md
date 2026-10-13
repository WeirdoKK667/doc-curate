---
name: doc-curate
description: |
  把任意来源的资料（外文 PDF、CAJ、扫描件、Word、PPT、EPUB）整理为结构化的多种产物——
  md（模块/标签化，供下游阅读）、Word 成稿、用户指定的其他格式。
  面向严肃学术/档案/技术资料整理场景，含翻译、术语表管理、模块标签化、自动校验、
  多产物导出等能力。

  触发场景（按用户说法匹配）：
  - "翻译这本 PDF"、"把外文文献翻成中文"
  - "整理这份资料"、"把这本报告整理成 Word"
  - "扫描件识别"、"PDF OCR 转 Word"
  - "CAJ 转 PDF"、"知网文献处理"
  - "按章节翻译"、"Chapter X 翻译成中文"
  - "中文资料结构化"、"PPT 整理成 Word"
  - "按标签整理"、"按内容分类导出"
  - PDF/CAJ/Word/PPT/EPUB 文件路径 + "整理/翻译/导出"指令

  不适用：实时翻译（同传/口译）、代码注释、字幕翻译、网页抓取、短消息、
  视频流 OCR、图像编辑、一次性单页快翻（用通用 PDF 工具即可）。
---

# doc-curate · 资料整理

把任意来源的资料，按"探查 → 提取 → 处理 → 校验 → 导出"五阶段，整理为结构化的多种产物。
**翻译只是常用功能之一**，不是全部；中文资料整理、其他格式转换等场景可能不含翻译。

## 一句话定位

> 资料整理 · 多来源 · 多产物 · 可中断可续跑

---

## 适用与不适用

### 适用场景

| 来源 | 典型动作 | 默认产物 |
|---|---|---|
| PDF 文字版 | 抽取 → 翻译/结构化 → 校对 | md + Word |
| PDF 扫描件 | 渲染 → OCR/视觉识别 → 转写 → 校对 | md + Word |
| CAJ | caj2pdf → PDF 工作流 | md + Word |
| Word 文档 | 解析 → 结构化 → 校对 | md + Word |
| PPT | 解析 → 结构化 → 校对 | md + Word |
| EPUB | 解析 → 结构化 → 校对 | md + Word |
| 其他格式 | 用户指定 | 用户指定 |

### 不适用场景

实时翻译（同传/口译）· 代码注释/API 文档 · 字幕翻译 · 网页抓取 ·
短消息/聊天记录 · 实时视频流 OCR · 图像编辑/分类 · 单页快翻。

---

## 工作流五阶段

| 阶段 | 输入 | 输出 | 关键动作 | 硬门 |
|---|---|---|---|---|
| **0 用户提供** | 用户输入（4 种形式） | `1 源/PARAMS.md`（基础字段） | 简单整理，剩余交给阶段 1 | 无 |
| **1 探查** | 阶段 0 PARAMS + 源文件 | `PARAMS.md`（补全）+ 探查报告 | 智能补全 + 信息对照 + 工作流确认 + 术语库确认 + 提问 | 等用户确认决策 |
| **2 提取** | 阶段 1 探查结果 | `3 提取内容/`（按类型分） | 工具开关启用（OCR/表格/图片）+ 格式适配 | 等用户确认 |
| **3 处理** | 阶段 2 素材 | `4 处理内容/` | PIPELINE 动作（翻译/术语/模块化/校对） | 不设硬门（阶段 4 统一校验） |
| **4 校验** | 阶段 3 中间产物 | `5 阶段性工作报告/校验报告.md` | 术语扫描（必）+ 上下文/查证/预测（按需） | 等用户确认 |
| **5 导出** | 阶段 3/4 中间产物 | `6 输出成果/` | 多产物组装（md + Word + 用户声明） | 不设硬门 |

→ 中间产物完整可重跑；阶段 5 脚本可重新组装产物。

---

## 目录结构

```
<动作><原后缀>：<源文件名（去后缀）>/
├── 1 源/
│   ├── <源文件>
│   └── PARAMS.md
├── 2 临时文件/                       # skill/scripts 的运行实例
├── 3 提取内容/
│   ├── 文字/                          # md 原文
│   ├── 表格/                          # md + json
│   ├── 图片/                          # 原始图片
│   └── <其他>/                        # 扩展
├── 4 处理内容/
│   ├── 专用术语表.md / .json
│   └── <PIPELINE 动作的中间产物>
├── 5 阶段性工作报告/                  # 阶段 1-4 报告
│   └── 校验报告.md
└── 6 输出成果/                        # md / Word / 用户指定
```

文件夹命名：`<动作><原后缀>：<源文件名去后缀>`
- 动作：翻译 / 校对 / 整理 / 提取 / 转换（预留扩展）
- 格式：原后缀（PDF/DOCX/PPTX/EPUB/CAJ）
- 例：`翻译PDF：kuznets_1966`、`整理PPTX：slides`

---

## 通用规则分级

### 硬约束（违反必报错）

1. **文件纪律**：所有产物在 `<源文件夹>` 内，不得散落。禁止覆盖、移动、修改源文件。
2. **PDF 原件保护**：只读 `1 源/<源文件>`，禁止读 PDF 原路径。
3. **脚本幂等**：所有 `scripts/` 脚本可重复运行不产生重复文件、覆盖写。
4. **产物组装走脚本**：阶段 5 不允许 agent 硬堆产物，统一调用脚本。
5. **错误三级**：hard_error（停） / soft_error（写 ISSUES 继续） / warning（仅打印）。

### 翻译规则（违反要 `[?]` 标注）

1. **忠实翻译**：不增译、不漏译、不改写、不总结。段落顺序与原文严格一致。
2. **专有名词**：人名/地名/机构/期刊/书名/报纸 → 保留原文（可加引号）；术语 → 中文（原文）。
3. **数字/单位/公式/化学式/代码**：保持原样；单位符号不转中文。
4. **参考文献/索引/ISBN/DOI/URL/引文页码**：保留原文不译。
5. **图片**：不修改图片，译文以"位置 + 内容"列在图下方。

### 建议（可灵活）

字体设置 · 行距 · 首行缩进 · 标题样式等版式细节，按场景调整。

---

## 变体开关总览

| 开关 | 取值 | 默认 | 说明 |
|---|---|---|---|
| `INPUT_FORMAT` | pdf/caj/docx/pptx/epub | pdf | 输入格式 |
| `ACTION` | translate/proofread/organize/extract/convert | translate | 主动作 |
| `PIPELINE` | [translate,glossary,modular,proof,...] | 按场景 | 阶段 3 子动作集 |
| `OUTPUTS` | [md,word,...] | [md,word] | 阶段 5 产物列表 |
| `SCAN` | on/off | off | 是否扫描件 |
| `BILINGUAL` | on/off | off | 是否双语对照 |
| `IMG_DEPTH` | full/caption | full | 图片翻译深度 |
| `TABLE_MODE` | native/image | native | 表格模式 |
| `FOOTNOTE` | docx/inline | docx | 脚注模式 |
| `SPLIT_OUT` | N | 0 | 超过 N 页分卷 |
| `KEEP_MARK` | on/off | on | 保留 PDF 页标记 |
| `ENABLE_OCR` | true/false | true | 启用 OCR |
| `ENABLE_TABLE_EXTRACT` | true/false | true | 启用表格抽取 |
| `ENABLE_IMAGE_EXTRACT` | true/false | true | 启用图片抽取 |
| `IMG_DEPTH_OVERRIDE` | pN_imgNN:caption | — | 逐图覆盖 |
| `TABLE_MODE_OVERRIDE` | pN_tNN:image | — | 逐表覆盖 |
| `GENERAL_GLOSSARY` | path | `~/.translate-glossary/general/` | 通用术语库路径 |
| `CUSTOM_TAGS` | [tag1,tag2,...] | — | 自定义标签 |

### 冲突优先级

- `BILINGUAL=on` ⇒ `IMG_DEPTH=full`
- `SCAN=on` ⇒ `KEEP_MARK=on`、`BATCH=3`
- `FOOTNOTE=docx` + `BILINGUAL=on` ⇒ 改 `FOOTNOTE=inline`

---

## 阶段契约

### 阶段 0：用户提供文件/参数
- 输入：4 种形式（绝对路径 / 目录路径 / 工作区路径 / 口述参数）
- 输出：`1 源/PARAMS.md`（仅含源文件信息：INPUT_FORMAT / SOURCE_FILE / PROJECT_NAME / WORKDIR）
- 动作：解析自然语言 → 关键词识别 → 简单整理；批量 / 口述含异则问
- **不做**：智能补全、信息对照、工作流确认

### 阶段 1：探查
- 5 个目的：完善参数表 + 信息对照 + 工作流确认 + 术语库确认 + 疑问提问
- 智能补全：所有字段有默认值，不一致才问
- 信息对照：清单 + md 呈现
- 工作流确认：主 agent 按探查结果决定（页字数 + 文本可抽取 + INPUT_FORMAT）
- 术语库加载：默认通用库 + 项目专用库
- 提问：汇总后统一问
- **硬门**：确认决策后才进阶段 2
- 详见：`references/workflow-detail.md` §1

### 阶段 2：素材提取
- 输入：阶段 1 探查结果
- 输出：`3 提取内容/` 按类型分（文字/表格/图片/其他）
- 素材格式：文字 md / 表格 md+json / 图片 png 等原图
- 工具开关：ENABLE_OCR / ENABLE_TABLE_EXTRACT / ENABLE_IMAGE_EXTRACT（独立）
- 重试：3 次 / 30 秒（可配置）
- 汇报：失败项写入阶段报告，阶段 2 结束时报给用户
- **硬门**：汇报后等用户确认
- 详见：`references/workflow-detail.md` §2 + `references/format-adapter.md`

### 阶段 3：处理
- 输入：阶段 2 素材
- 输出：`4 处理内容/`
- PIPELINE 子动作（自由搭配）：translate / glossary / modular / proof
- 模块化三种形式：自然结构 / 按页分割 / 按内容标签
- 并行：subagent 同时工作；默认 5 页一批；具体分法由主 agent 决定
- **不设硬门**：输出阶段报告，阶段 4 统一校验
- 详见：`references/workflow-detail.md` §3 + `references/translate-rules.md`

### 阶段 4：自动校验
- 输入：阶段 3 中间产物
- 输出：`5 阶段性工作报告/校验报告.md`
- 4 个子动作（按优先级 + 用户要求判断）：
  - **术语一致性扫描**（必跑）
  - 跨页上下文联系（可选）
  - 未知术语自动查证（可选）
  - 预测不确定项处理方案（可选）
- 预测处理：自动应用，做法写 `references/proofread-rules.md`
- 校验报告章节：总结论 / 各子动作结果 / 发现的不确定项 / 推荐处理方案 / 需要用户裁决项
- **硬门**：汇报后等用户确认
- 详见：`references/workflow-detail.md` §4 + `references/proofread-rules.md` + `references/qa-checks.md`

### 阶段 5：导出成果
- 输入：阶段 3/4 中间产物
- 输出：`6 输出成果/` 按 OUTPUTS 列表生成
- 组装：互不干扰情况下并行，也可串行——主 agent 决定
- 完整性：用户无特殊说明时不额外提及；正常情况 agent 保证使用全部素材
- 优先级：用户声明优先于默认；agent 判断有更好形式（除 md/word）询问用户
- 交付清单：默认不生成；交付物数量多时询问用户
- **不设硬门**
- **产物组装走脚本**：禁止 agent 硬堆
- 详见：`references/workflow-detail.md` §5 + `references/output-formats.md`

---

## 用户输入形式（4 种）

| 形式 | 示例 | agent 动作 |
|---|---|---|
| 绝对路径 | "翻译 `D:/papers/kuznets.pdf`" | 解析路径，写入 PARAMS |
| 目录路径 | "翻译 `D:/papers/` 下的文件" | 列目录，**询问**批量策略 |
| 工作区路径 | "翻译工作区里的 source.pdf" | 相对路径解析 |
| 口述参数 | "从第 5 页到第 20 页" | 关键词识别 + 询问含异 |

---

## 术语表

| 类型 | 范围 | 位置 |
|---|---|---|
| **通用术语表** | 学科级（如地质学），不同文献都可使用 | 用户指定路径，默认 `~/.translate-glossary/general/` |
| **专用术语表** | 项目级/文件级（人名、地名、公司名等） | `<源文件夹>/4 处理内容/专用术语表.md` |

### 术语表格式（双格式）

- **Markdown**（`专用术语表.md`）：人类阅读
- **JSON**（`专用术语表.json`）：脚本读写
- 详见：`assets/glossary-template.md`

### 术语调用脚本

- 查：术语是否已存在
- 增：写入新术语
- 统计：频次 / 不一致检测
- 详见：`references/proofread-rules.md` 术语部分

---

## 中间产物与续跑

### 中间产物完整可重跑
阶段 3/4 产出完整的中间产物；阶段 5 跑脚本可重新组装产物。**修改中间产物不必整段重写**。

### 续跑机制
- PROGRESS.md 记录每阶段进度、批次、用时、ISSUE 数
- 阶段中断 → 下次开工读 PROGRESS.md 自动定位续跑点
- 批次超时 30 分钟 → 拆分重试

---

## references/ 索引（按需读取）

| 细则 | 内容 | 何时读 |
|---|---|---|
| `workflow-detail.md` | 每阶段完整步骤、参数、产物清单 | 进入对应阶段时 |
| `translate-rules.md` | 翻译场景的专名/图片/术语/公式规则 | 阶段 3 含翻译时 |
| `proofread-rules.md` | 阶段 4 子动作细则（含术语调用脚本） | 阶段 4 |
| `format-adapter.md` | PDF/CAJ/Word/PPT/EPUB 各自适配策略 | 阶段 2 启用对应适配时 |
| `output-formats.md` | md / Word / 其他产物版式细则 | 阶段 5 |
| `qa-checks.md` | 硬/软检查判定标准 | 阶段 4 |
| `troubleshooting.md` | 常见报错与处置 | 出错时 |

---

## assets/ 模板（实例化用）

| 资源 | 作用 |
|---|---|
| `params-template.md` | PARAMS.md 初始模板 |
| `glossary-template.md` | 术语表双格式模板 |
| `md-template.md` | md 模块化标签模板 |
| `zh-md-schema.md` | 翻译稿标签格式定义 |
| `manifest-schema.json` | 素材清单 schema |
| `docx-template.docx` | Word 样式模板（含字体/Heading） |

---

## scripts/ 工具集（idempotent）

| 脚本 | 阶段 | 作用 |
|---|---|---|
| `probe.py` | 1 | 探查源文件 |
| `format_adapter.py` | 2 | 输入格式转换（CAJ/Word/PPT/EPUB → PDF） |
| `extract.py` | 2 | 文字/表格/图片抽取 |
| `ocr.py` | 2（按需） | OCR/视觉识别 |
| `process.py` | 3 | 处理调度 |
| `scan_terms.py` | 4 | 术语一致性扫描 |
| `qa.py` | 4 | 自动质检 |
| `build_md.py` | 5 | md 组装 |
| `build_docx.py` | 5 | Word 组装 |
| `build_toc_docx.py` | 5 | 目录 docx |
| `tag_index.py` / `tag_query.py` / `tag_register.py` | 3 | 模块/标签化配套 |
