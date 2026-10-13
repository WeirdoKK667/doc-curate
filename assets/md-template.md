# md 模板 · 模块/标签化

> 三种形式：自然结构 / 按页分割 / 按内容标签。

---

## 形式 1：自然结构（普通情况）

```markdown
# 文献标题（中译）

## 章节 1
### 小节 1.1
正文段落...

### 小节 1.2
正文段落...

## 章节 2
### 小节 2.1
正文段落...
```

适用：普通中文资料整理；不需精确标注页码的场景。

---

## 形式 2：按页分割（PDF 等需标注页码）

```markdown
# 文献标题（中译）

<!-- page:323 -->
<!-- 印刷页码：322 -->

## 【PDF 第 323 页】

正文段落...

<!-- IMAGE:p323_img01.png -->
图题译文：图 3-1 ...
图中文字译文：
- 横轴刻度标签：...
<!-- /IMAGE -->

<!-- /page -->

<!-- page:324 -->
<!-- 印刷页码：323 -->

## 【PDF 第 324 页】

正文段落...

<!-- TABLE:p324_t01 -->
表题译文：表 12-1 ...
| 列1 | 列2 |
|---|---|
| 值1 | 值2 |
<!-- /TABLE -->

<!-- /page -->
```

适用：PDF 文献翻译；需精确页码定位的场景。

---

## 形式 3：按内容标签（检索场景）

```markdown
<!-- tag:chapter id="ch1" title="研究背景" -->

## 1. 研究背景

正文段落...

<!-- tag:section id="ch1-1" title="研究问题" -->

正文段落...

<!-- /tag:section -->

<!-- tag:figure id="fig1-1" page="5" -->

图题译文：图 1-1 ...

<!-- /tag:figure -->

<!-- /tag:chapter -->

<!-- tag:chapter id="ch2" title="研究方法" -->

## 2. 研究方法

正文段落...

<!-- /tag:chapter -->
```

适用：检索场景；按主题/类型查找内容。

---

## 内置保留标签

| 标签 | 含义 |
|---|---|
| `<!-- tag:chapter -->` | 章节级 |
| `<!-- tag:section -->` | 小节级 |
| `<!-- tag:figure -->` | 图片相关 |
| `<!-- tag:table -->` | 表格相关 |
| `<!-- tag:footnote -->` | 脚注相关 |
| `<!-- tag:citation -->` | 引文相关 |

## 自定义标签

PARAMS 中声明 `CUSTOM_TAGS: [...]`，如：
```yaml
CUSTOM_TAGS:
  - methodology
  - data
  - conclusion
```

---

## 标签配套脚本

### scripts/tag_index.py
建立标签索引（md 文件 → 标签清单 → 章节定位）

### scripts/tag_query.py
按标签检索指定内容

### scripts/tag_register.py
标签注册（保留字检查、用户自定义校验）
