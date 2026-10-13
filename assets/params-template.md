# PARAMS.md · 模板

> 阶段 0 由用户填 / agent 整理；阶段 1 由探查补全。

---

```yaml
# ============================================
# 必填字段（阶段 0 必须）
# ============================================
INPUT_FORMAT: pdf              # pdf / caj / docx / pptx / epub / other
SOURCE_FILE: <absolute path>   # 源文件绝对路径
PROJECT_NAME: <string>         # 项目名
WORKDIR: <absolute path>       # <动作><格式>：<源文件名去后缀>/

# ============================================
# 推荐字段（用户口述 / agent 推断）
# ============================================
ACTION: translate              # translate / proofread / organize / extract / convert
PIPELINE: [translate, glossary, modular, proof]   # 阶段 3 子动作集

# ============================================
# 探查补全字段（阶段 1 写入）
# ============================================
PAGE_START: <int>              # 起页（PDF 物理页）
PAGE_END: <int>                # 止页
PRINT_OFFSET: 0                # 印刷页偏移（阶段 1 实测）
BATCH: 5                       # 每批页数（SCAN=on 时默认 3）
OUTPUTS: [md, word]            # 产物列表

ENABLE_OCR: true
ENABLE_TABLE_EXTRACT: true
ENABLE_IMAGE_EXTRACT: true

# ============================================
# 可选字段（默认 + 用户覆盖）
# ============================================
SCAN: off                      # off / on
BILINGUAL: off                 # off / on
IMG_DEPTH: full                # full / caption
TABLE_MODE: native             # native / image
FOOTNOTE: docx                 # docx / inline
SPLIT_OUT: 0                   # 超过 N 页分卷
KEEP_MARK: on                  # on / off

# ============================================
# 路径字段
# ============================================
GENERAL_GLOSSARY: ~/.translate-glossary/general/   # 通用术语库
# CUSTOM_GLOSSARY: <path>      # 用户预提供专用术语表（可选）

# ============================================
# OCR 后端
# ============================================
OCR_BACKEND: subagent_visual   # subagent_visual / tesseract / paddleocr

# ============================================
# 覆盖字段（可选）
# ============================================
# IMG_DEPTH_OVERRIDE:
#   p345_img03: caption
# TABLE_MODE_OVERRIDE:
#   p343_t02: image

# ============================================
# 自定义标签
# ============================================
# CUSTOM_TAGS:
#   - methodology
#   - data
#   - conclusion

# ============================================
# 用户预提供内容（可选）
# ============================================
# PREDEFINED_GLOSSARY: <path>   # 预提供的术语表
# PREDEFINED_ISSUES: <path>     # 预提供的存疑表
# TRANSLATE_PREFERENCE: <text>   # 翻译偏好（如"专业术语用日译"）
```

---

## 字段说明

### 必填字段（阶段 0）
- `INPUT_FORMAT`：输入格式，决定适配路径
- `SOURCE_FILE`：源文件绝对路径
- `PROJECT_NAME`：项目名
- `WORKDIR`：工作目录（即 `<动作><格式>：<源文件名去后缀>/`）

### 推荐字段
- `ACTION`：主动作（决定文件夹名前缀）
- `PIPELINE`：阶段 3 子动作集

### 探查补全字段（阶段 1）
阶段 0 不要求，阶段 1 探查后自动补全。

### 可选字段
所有字段都有默认值；用户口述才覆盖。

### 覆盖字段
用于逐图 / 逐表覆盖默认开关。
