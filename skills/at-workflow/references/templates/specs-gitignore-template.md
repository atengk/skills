# 特性工件目录忽略规约模板 (Specs Gitignore Template)

本文档定义了目标工程 `.specs/.gitignore` 的标准忽略规则，用于隔离瞬态交接文档与临时文件，防止污染 Git 主干代码库。

---

## 目录 (Table of Contents)

- [1. 标准忽略规则清单](#1-标准忽略规则清单)
- [2. 忽略规则核心设计考量](#2-忽略规则核心设计考量)

---

## 1. 标准忽略规则清单

在目标工程的 `.specs/.gitignore` 文件中配置以下规则：

```gitignore
# 特性工件目录瞬态资产忽略规则 (Transient Artifacts)
**/HANDOFF.md
**/*.tmp.md
**/scratch/
```

---

## 2. 忽略规则核心设计考量

- **`**/HANDOFF.md`**：跨会话交接棒是易失性瞬态桥梁，接棒 Agent 读取后即失去价值，严禁入库污染主干 Commit 历史；
- **`**/*.tmp.md`**：过程推演中的临时草稿与探针记录，受保护无需提交；
- **`**/scratch/`**：临时脚本、排查日志与临时探针目录，严格受保护隔离。
