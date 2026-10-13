# qa-checks.md · 硬/软检查判定标准

> 阶段 4 + 阶段 5 的质检清单。

---

## 一、硬检查（不通过不交付）

| # | 检查项 | 判定标准 |
|---|---|---|
| H1 | 页数齐全 | 输出页数 = PARAMS `PAGE_END - PAGE_START + 1` |
| H2 | 段落 1:1 对齐 | 译文段落数 = 原文段落数 |
| H3 | 图片数一致 | zh.md IMAGE 标签数 = manifest images[] 数 |
| H4 | 表格数一致 | zh.md TABLE 标签数 = manifest tables[] 数 |
| H5 | 装饰图回插 | 装饰图回插数 = images_ignored 数 |
| H6 | 兜底补入 | 兜底补入数 = reused_in_pages 数 |
| H7 | Heading 标题数 | docx Heading 数 = 原文标题数 |
| H8 | [?] 子段数 | 拆分子段数 = zh.md 中 [?] 总数 |
| H9 | 术语必查 | scan_terms.py 跑通 |
| H10 | 完整性断言 | scripts/qa.py 全部通过 |

---

## 二、软检查（不通过仅警告）

| # | 检查项 | 判定标准 |
|---|---|---|
| S1 | 术语与 glossary 一致 | 抽查 10 处不一致率 |
| S2 | 人名/地名未被音译 | 抽查 10 处无音译 |
| S3 | 公式符号未乱码 | 公式页字符数正常 |
| S4 | ISSUES.md 已处理 | 存疑项已逐条处理或标注 |
| S5 | 工作目录干净 | 无散落文件 |
| S6 | 目录生成 | build_toc_docx.py 输出与 Heading 一致 |
| S7 | 字体设置 | eastAsia + 西文字体同时生效 |
| S8 | 页标记 KEEP_MARK | 校对稿有 / 正式稿无 |

---

## 三、检查脚本

### scripts/qa.py

```bash
scripts/qa.py \
  --project <源文件夹> \
  --stage 4  # 检查阶段 4 输出
  --stage 5  # 检查阶段 5 输出
```

输出：
```
硬检查：10/10 PASS
软检查：8/8 PASS
警告：0
错误：0
```

---

## 四、自动质检时机

| 时机 | 检查范围 |
|---|---|
| 阶段 4 完成 | H1-H4, H9（数据完整性 + 术语必查） |
| 阶段 5 完成 | H5-H10（产物完整性 + 版式） |
| 用户要求时 | S1-S8（软检查） |

---

## 五、交付清单（默认不生成）

仅在交付物数量较多（>5 个）时询问用户是否生成 `delivery_report.md`。
