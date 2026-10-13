# proofread-rules.md · 阶段 4 子动作细则

> 阶段 4 自动校验的 4 个子动作详细做法 + 术语调用脚本接口。

---

## 一、术语一致性扫描（必跑）

### 目标
抽取所有 zh.md 中的英文专名/术语，对比 glossary.md，未收录项标记。

### 调用
```bash
scripts/scan_terms.py \
  --glossary 4 处理内容/专用术语表.md \
  --translations 4 处理内容/ \
  --output ISSUES.md
```

### 规则
1. 抽取 zh.md 中所有英文词组（首字母大写、缩写、专业术语特征）
2. 对比 glossary.md（通用库 + 专用库）
3. 未收录项全部写入 ISSUES.md，标 `term_unregistered`
4. 已收录但译法不一致 → 标 `term_inconsistent`
5. 统计：术语总数、新增数、不一致数

---

## 二、跨页上下文联系（可选）

### 目标
检测段落、术语、引用跨页不一致。

### 检测项
- 段落跨页拼接是否断裂
- 术语前后译法是否一致
- 引用 [1]/[2] 编号是否连续
- 图/表编号是否连续

### 调用
```bash
scripts/context_check.py --project <源文件夹>
```

### 输出
写入校验报告 §各子动作结果。

---

## 三、未知术语自动查证（可选）

### 目标
未在 glossary 的术语，自动查证后建议译法。

### 工作流
1. scan_terms 输出未收录术语清单
2. 调外部知识库（如 Wikipedia、CN 百科）查证
3. 输出建议译法 + 置信度
4. 高置信度 → 自动写入专用术语表
5. 低置信度 → 写入 ISSUES.md 等用户裁决

### 调用
```bash
scripts/lookup_terms.py --terms ISSUES.md#term_unregistered --output 建议译法.md
```

---

## 四、预测不确定项处理方案（可选）

### 目标
对 [?] 存疑项，自动应用预测方案。

### 预测做法

| 不确定类型 | 预测方案 |
|---|---|
| 词义不明 | 上下文联系 + 同领域术语推断 |
| 断句不明 | 按标点 + 段落长度推断 |
| 残损文字 | 标 `残损`，保留原文 |
| 数字缺失 | 标 `[?数字缺失]` |

### 应用规则
- 预测置信度 > 0.8 → **自动应用**
- 0.5-0.8 → 自动应用但写入 ISSUES.md（用户可回退）
- < 0.5 → 不应用，写入 ISSUES.md 等用户裁决

### 调用
```bash
scripts/predict_terms.py --project <源文件夹> --apply
```

---

## 五、术语调用脚本接口

### scripts/scan_terms.py · 查 / 增 / 统计

#### 查
```bash
scripts/scan_terms.py query --term "sustainable development"
# 输出：命中通用库 / 专用库 / 未命中
```

#### 增
```bash
scripts/scan_terms.py add \
  --type term \
  --original "sustainable development" \
  --chinese "可持续发展" \
  --alias "SD"
# 自动写入 4 处理内容/专用术语表.md + .json
```

#### 统计
```bash
scripts/scan_terms.py stats --project <源文件夹>
# 输出：术语总数 / 类型分布 / 频次 TOP20 / 不一致项
```

### 通用库管理

```bash
# 升级到通用库
scripts/scan_terms.py promote --term-id 042 --to general

# 全局统计
scripts/scan_terms.py stats --scope general
```

---

## 六、校验报告输出

`5 阶段性工作报告/校验报告.md`，固定章节：

```markdown
# 校验报告

## 总结论
[通过 / 警告 / 失败]

## 各子动作结果

### 术语一致性扫描
- 扫描术语数：N
- 命中：N / 未命中：N / 不一致：N

### 跨页上下文联系
- 检查项数：N
- 发现：N

### 未知术语自动查证
- 查证数：N
- 自动应用：N / 写入 ISSUES：N

### 预测不确定项处理方案
- 预测项数：N
- 自动应用：N / 写入 ISSUES：N

## 发现的不确定项
- [?] 列表（含定位）

## 推荐处理方案
- 自动应用项清单
- 写入 ISSUES.md 项清单

## 需要用户裁决项
- 待用户决策清单
```
