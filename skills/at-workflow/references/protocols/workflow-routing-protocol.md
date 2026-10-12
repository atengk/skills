# 全局研发工作流总控路由协议 (Global Workflow Routing Protocol)

本文档定义全生命周期 31 个 AI Agent 软件工程技能的场景意图诊断决策树、经典协同配方流水线与调度路由契约。

---

## 目录 (Table of Contents)

- [1. 31 项技能全景拓扑与四层金字塔模型](#1-31-项技能全景拓扑与四层金字塔模型)
- [2. 开发者意图诊断决策树](#2-开发者意图诊断决策树)
- [3. 六大标准化协同流水线配方](#3-六大标准化协同流水线配方)
- [4. 技能链条输入输出契约矩阵](#4-技能链条输入输出契约矩阵)
- [5. 动态降级与自适应调度准则](#5-动态降级与自适应调度准则)

---

## 1. 31 项技能全景拓扑与四层金字塔模型

全库技能按照软件工程职责解耦为四层金字塔拓扑体系：

```mermaid
flowchart TD
    subgraph L4["第四层：资产门户、发版与总控 (Portal & Orchestration)"]
        W1["at-workflow (总控路由)"]
        W2["at-readme"] --- W3["at-contributing"] --- W4["at-changelog"]
        W5["at-runbook"] --- W6["at-rules"] --- W7["at-ci"]
        W8["at-release"] --- W9["at-handoff"]
    end

    subgraph L3["第三层：物理隔离、全栈质效与可观测 (Quality & Isolation)"]
        Q1["at-worktree"] --- Q2["at-prototype"] --- Q3["at-simplify"]
        Q4["at-security"] --- Q5["at-performance"] --- Q6["at-frontend"]
        Q7["at-e2e"] --- Q8["at-observability"] --- Q9["at-retro"]
    end

    subgraph L2["第二层：核心主干闭环 (Core Delivery Loop)"]
        C1["at-grill (反向质询)"] --> C2["at-spec (增量规范)"]
        C2 --> C3["at-plan (任务拆解)"]
        C3 --> C4["at-tdd (测试驱动)"]
        C4 --> C5["at-review (双轴审查)"]
        C5 --> C6["at-diagnose (假设排错)"]
    end

    subgraph L1["第一层：思考、设计与架构基石 (Design Foundations)"]
        F1["at-assess (可行性)"] --- F2["at-glossary (领域防腐)"]
        F3["at-constitution (工程宪章)"] --- F4["at-api-design (接口契约)"]
        F5["at-adr (决策记录)"] --- F6["at-refactor (深度重构)"]
        F7["at-tech-doc (工业级架构)"]
    end

    L1 --> L2 --> L3 --> L4
```

---

## 2. 开发者意图诊断决策树

当开发者向 Agent 提出诉求时，`at-workflow` 按照以下规则树引导意图收敛：

```mermaid
flowchart TD
    Start["开发者发起研发诉求"] --> Q1{"需求类型是什么？"}

    Q1 -->|"新业务功能 / 探索性需求"| PathA{"方案确定性如何？"}
    PathA -->|"不确定 / 需技术预研"| S_Assess["调用 at-assess / at-prototype"]
    PathA -->|"方向明确 / 需澄清细节"| S_Feature["启动【新特性全链路流水线】"]

    Q1 -->|"排查生产缺陷 / 偶发 Bug"| PathB{"是否需要隔离现场？"}
    PathB -->|"需要隔离排查"| S_Worktree["调用 at-worktree 隔离分支"]
    PathB -->|"直接排查"| S_Diagnose["启动【缺陷根因排查流水线】"]

    Q1 -->|"代码异味 / 架构臃肿 / 性能劣化"| S_Refactor["启动【架构演进与重构流水线】"]
    Q1 -->|"开源门户建设 / 规范治理"| S_Gov["启动【规范治理与门面流水线】"]
    Q1 -->|"准备发版 / 跨会话交接"| S_Rel["启动【发版归档与交接流水线】"]
```

---

## 3. 六大标准化协同流水线配方

### 3.1 配方 1：全新特性研发流水线 (Feature Delivery Flow)
`at-assess` -> `at-grill` -> `at-spec` -> `at-api-design` -> `at-plan` -> `at-tdd` -> `at-review` -> `at-e2e` -> `at-release`
- 适用场景：高复杂度新模块上线，要求前置防腐、精确计划、严格单测与端到端验收。

### 3.2 配方 2：缺陷排查与热修流水线 (Hotfix & Diagnostic Flow)
`at-diagnose` -> `at-worktree` -> `at-tdd` -> `at-review` -> `at-release` -> `at-retro`
- 适用场景：生产紧急缺陷，以科学假设驱动快速复现，红灯用例保护，上线后 5 Whys 复盘。

### 3.3 配方 3：架构演进与极简重构流水线 (Refactoring Flow)
`at-adr` -> `at-glossary` -> `at-refactor` -> `at-simplify` -> `at-performance` -> `at-review`
- 适用场景：消除上帝类、深层嵌套与慢查询，在已有单测保护下小步快跑。

### 3.4 配方 4：开源门面与流水线门禁建设 (Governance & Portal Flow)
`at-constitution` -> `at-rules` -> `at-ci` -> `at-readme` -> `at-contributing` -> `at-changelog`
- 适用场景：新项目开荒或存量项目标准化改造，建立全套工程守卫与开发者门面。

### 3.5 配方 5：生产稳态与可观测运维流 (Observability & SRE Flow)
`at-observability` -> `at-runbook` -> `at-retro`
- 适用场景：生产服务上线前监控埋点设计、应急排错预案制定与故障复盘治理。

### 3.6 配方 6：长时自治跨会话接力流 (Autonomous Handoff Flow)
`at-handoff` -> 注入新 Agent -> 断点热启动续跑
- 适用场景：长任务超过上下文窗口阈值时，自动压缩去噪并无缝移交。

---

## 4. 技能链条输入输出契约矩阵

| 阶段 | 上游技能 | 核心产出物 | 下游衔接技能 |
| :--- | :--- | :--- | :--- |
| **需求输入** | `at-grill` | 结构化需求澄清提纲 | `at-spec` (转写契约) |
| **设计规范** | `at-spec` | 原子化增量变更规格书 | `at-plan` (任务依赖图) |
| **任务拆解** | `at-plan` | 拓扑依赖感知微任务清单 | `at-tdd` (逐项单测开发) |
| **编码实现** | `at-tdd` | 100% 绿灯且消除异味的代码 | `at-review` (双轴审查) |
| **质量门禁** | `at-review` | 审查通过报告 / 改进建议 | `at-e2e` / `at-release` |

---

## 5. 动态降级与自适应调度准则

1. **轻量任务快速通道**：对于纯文档修正或微小修复（< 10 行），允许跳过 `at-assess` 与 `at-plan`，直接采用 `at-tdd` -> `at-review`；
2. **阻断级前置卡点**：`at-spec` 未获确认前，严禁越级直接调用 `at-tdd` 编写业务源码；
3. **安全与两级授权**：任何涉及代码提交与远端推送的步骤，工作流总控必须挂起并等待人类显式指令。
