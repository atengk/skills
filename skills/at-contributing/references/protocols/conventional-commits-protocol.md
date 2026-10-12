# 规范化提交与 Git 分支策略工程指南 (Conventional Commits Protocol)

本指南系统规范了现代软件工程中的 Git 提交历史规范化标准与团队分支协同策略，遵循 Conventional Commits 1.0.0 国际规范，保障变更历史清晰、机器可读与自动化发布版本追踪。

---

## 目录 (Table of Contents)

- [1. Conventional Commits 结构规范与语义语法](#1-conventional-commits-结构规范与语义语法)
- [2. 常用提交类型 (Type) 定义与使用边界](#2-常用提交类型-type-定义与使用边界)
- [3. 范围 (Scope) 与破坏性变更 (Breaking Change) 规范](#3-范围-scope-与破坏性变更-breaking-change-规范)
- [4. Git 分支模型与命名规范](#4-git-分支模型与命名规范)
- [5. 精准暂存与两级显式授权安全红线](#5-精准暂存与两级显式授权安全红线)

---

## 1. Conventional Commits 结构规范与语义语法

每一个 Git Commit Message 必须遵循以下三段式结构：

```text
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### 核心约束
- **首行摘要 (Header)**：必须简明扼要，建议控制在 50~72 字符内，首字符小写或中文肯定句；
- **空行隔离**：Header 与正文 Body 之间、Body 与页脚 Footer 之间必须留有 1 行空行；
- **正文多项罗列**：单次提交包含多个微改动时，在 Body 中逐项使用列表符清晰罗列说明。

---

## 2. 常用提交类型 (Type) 定义与使用边界

| 提交类型 (Type) | 语义含义 | 典型适用场景 | 是否触发版本递增 |
| :--- | :--- | :--- | :---: |
| **`feat`** | 新增特性 | 新增业务功能、开放全新 API、新增交互界面 | Minor (次版本) |
| **`fix`** | 缺陷修复 | 修复线上或测试环境 Bug、修复空指针等异常 | Patch (补丁版本) |
| **`docs`** | 文档变更 | 仅修改 README、API 文档、技术方案或代码注释 | 无/Patch |
| **`style`** | 代码格式 | 空格、分号、中西文排版优化，不影响代码逻辑 | 无/Patch |
| **`refactor`** | 代码重构 | 既不修复缺陷也不添加特性的代码重组、深模块演进 | Patch |
| **`perf`** | 性能调优 | 提升运行效率、降低延时、减少内存开销的代码改动 | Patch |
| **`test`** | 测试相关 | 补充单元测试、集成测试用例，重构测试夹具 | 无/Patch |
| **`build`** | 构建系统 | 修改构建脚本、依赖版本升级 (npm, Maven, Cargo) | Patch |
| **`ci`** | 自动化门禁 | 修改 GitHub Actions、GitLab CI 流水线配置文件 | 无/Patch |
| **`chore`** | 日常杂务 | 不属于上述分类的辅助性工程改动、清理废弃资产 | 无/Patch |

---

## 3. 范围 (Scope) 与破坏性变更 (Breaking Change) 规范

### 3.1 范围 (Scope) 约束
- 范围用小括号包裹在 Type 之后，用于指示发生变更的代码模块（如 `feat(order): 新增批量导出`、`fix(auth): 修复 Token 续期失效`）；
- Scope 统一使用 kebab-case，保持简短（如 `user`、`payment`、`api-gateway`）。

### 3.2 破坏性变更 (Breaking Change) 显式声明
- **语法标识**：在 Type/Scope 之后紧跟叹号 `!`（如 `feat(api)!: 变更用户分页响应契约`），或者在 Footer 中以 `BREAKING CHANGE: <详细破坏性说明>` 开头；
- **语义化版本触发**：破坏性变更强制触发 Major (主版本号) 递增。

---

## 4. Git 分支模型与命名规范

团队推荐基于主干演进（Trunk-based）或轻量特性分支模型：

- **特性开发**：`feat/<issue-id>-<short-name>`（例如 `feat/42-order-export`）；
- **缺陷热修**：`fix/<issue-id>-<short-name>`（例如 `fix/88-token-leak`）；
- **架构重构**：`refactor/<module-name>`（例如 `refactor/payment-gateway`）；
- **长期主干**：`main`（受保护主干，严禁直接 Force Push）。

---

## 5. 精准暂存与两级显式授权安全红线

- **精准路径暂存**：暂存必须显式指定具体修改文件（`git add <file-path>`），严禁使用 `.` 或 `-A` 全量通配；
- **两级显式授权**：AI Agent 实施修改后默认停留在工作区；未收到用户显式指令（“提交”或“推送”）前，严禁自主执行 `git commit` 或 `git push`；
- **机密扫描**：提交前自动审计暂存区 Diff，严禁泄漏任何真实 Token、密码或私钥。
