# 专用术语表 · <项目名>

> 双格式存储：本文档（人类阅读）+ 专用术语表.json（脚本读写）。
> 通用术语表：用户指定路径，默认 `~/.translate-glossary/general/`。

---

## 人名（保留原文）

| 原文 | 中文（音译） | 备注 |
|---|---|---|
| Simon Kuznets | — | 不译，保留原文 |
| John Maynard Keynes | — | 不译 |

---

## 地名（保留原文）

| 原文 | 中文 | 备注 |
|---|---|---|
| Mt Elgon | — | 不译 |
| Lake Victoria | — | 不译 |

---

## 机构名（保留原文）

| 原文 | 中文 | 备注 |
|---|---|---|
| Geological Survey of Finland | — | 不译 |
| Special Paper 55 | — | 不译 |

---

## 期刊名 / 书名 / 报纸名（保留原文）

| 原文 | 备注 |
|---|---|
| Nature | 不译 |
| The Wealth of Nations | 不译 |

---

## 专业术语

| 原文 | 中文（首次/常用） | 备注 |
|---|---|---|
| gross domestic product | 国内生产总值（GDP） | 首次给中+原文，后续只用"国内生产总值" |
| sustainable development | 可持续发展（sustainable development） | 首次给中+原文 |

---

## 概念 / 条约 / 事件

| 原文 | 中文（原文） | 备注 |
|---|---|---|
| Paris Agreement | 《巴黎协定》（Paris Agreement） | 首次给中+原文 |

---

## 缩写

| 原文 | 中文 | 备注 |
|---|---|---|
| GDP | 国内生产总值 | 与 gross domestic product 同义 |
| OPEC | 石油输出国组织 | — |

---

# 对应 JSON（脚本读写）

`专用术语表.json`：

```json
{
  "version": "1.0",
  "project": "<项目名>",
  "updated_at": "2026-10-13T00:00:00Z",
  "entries": [
    {
      "id": "001",
      "type": "person",
      "original": "Simon Kuznets",
      "chinese": "",
      "alias": [],
      "note": "不译，保留原文"
    },
    {
      "id": "002",
      "type": "term",
      "original": "gross domestic product",
      "chinese": "国内生产总值",
      "alias": ["GDP"],
      "note": "首次给中+原文"
    },
    {
      "id": "003",
      "type": "term",
      "original": "sustainable development",
      "chinese": "可持续发展",
      "alias": ["SD"],
      "note": "首次给中+原文"
    },
    {
      "id": "004",
      "type": "institution",
      "original": "Geological Survey of Finland",
      "chinese": "",
      "alias": [],
      "note": "不译"
    }
  ]
}
```

---

## 类型枚举

| type | 含义 | 处理 |
|---|---|---|
| `person` | 人名 | 保留原文，不译 |
| `place` | 地名 | 保留原文，不译 |
| `institution` | 机构名 | 保留原文，不译 |
| `journal` | 期刊名 | 保留原文，不译 |
| `book` | 书名 | 保留原文，不译 |
| `newspaper` | 报纸名 | 保留原文，不译 |
| `term` | 专业术语 | 中文（原文） |
| `concept` | 概念 | 中文（原文） |
| `treaty` | 条约名 | 中文（原文） |
| `event` | 事件名 | 中文（原文） |
| `abbreviation` | 缩写 | 中文（原文） |
