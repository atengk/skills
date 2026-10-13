---
name: at-workflow
description: 当用户面对复杂工程任务不确定如何推进、需要全生命周期研发向导、诊断当前场景最佳技能路线或需要智能调度串联多技能时使用此技能。提供全局工作流路由协议与交互菜单模板，交付无缝衔接的端到端研发编排体验。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[init|#<issue-id>|recipe <id>|help [skill]|menu]"
allowed-tools:
  - view_file
  - run_command
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.1.0
  tags: [workflow, orchestrator, router, full-lifecycle, dev-assistant]
---

# 全生命周期研发工作流总控路由技能 (Master Workflow Orchestrator)

本技能作为全库 31 个 AI Agent 软件工程技能的总控调度中枢，提供工程一键初始化脚手架、远程 Issue 自动联动、标准化流水线配方推荐与会话内内联接力推进。

```mermaid
flowchart LR
    S1["1. 诉求诊断与 Issue 锚定"] --> S2["2. 标准流水线配方推荐"]
    S2 --> S3["3. 人机对齐与路线确认"]
    S3 --> S4["4. 会话内内联接力推进"]
    S4 --> S5["5. 闭环审计与 Issue 回填"]
```

## 执行流程状态机 (Execution State Machine)

### 阶段 1：研发诉求探查与 Issue 锚定 (Diagnosis & Issue Binding)
- 响应 `init` 子命令：探查技术栈并调用脚手架生成目标项目工程治理基座；
- 响应 `help` / `help <skill>` 子命令，直接渲染标准五段式技能卡片；
- 识别远程 Issue 编号（`#<id>`）或 URL，调用 CLI（`gh`/`glab`）提取标题正文；
- 探查代码仓库状态、单/多模块拓扑、既有规范文件（`CONSTITUTION.md`、`docs/glossary.md`）与 Git 上下文；
- 诊断决策树规则参考 [全局工作流总控路由协议](./references/protocols/workflow-routing-protocol.md)。

### 阶段 2：标准场景流水线配方推荐 (Recipe Recommendation)
- 匹配经典流水线配方（特性流、热修流、重构流、门面流、运维流、交接流）；
- 统一锚定特性工件目录为 `.specs/issue-<id>-<slug>/`（如 `.specs/issue-42-order-timeout/`）；
- 提取任务所必需的最小特权原子技能子集，规划拓扑调用顺序与阶段产出契约；
- 输出向导菜单与配方卡片，展示规范参考 [研发工作流交互向导模板](./references/templates/workflow-menu-template.md)。

### 阶段 3：人机交互对齐与执行路线确认 (Interactive Alignment)
- 向开发者展示建议的技能调用链路、工件落盘目录与关键阶段产出物预期；
- 针对模糊需求引导前置质询（`at-grill`），针对技术不确定项推荐可行性探针；
- 获取开发者显式确认指令后锁定本轮工作流执行蓝图；
- 经典交互编排参考 [全生命周期多技能协同实战样例](./examples/sample-workflow-orchestration.md)。

### 阶段 4：会话内内联接力推进 (Inline Chaining Orchestration)
- 依据拓扑顺序渐进式推进工作流，管理阶段工件在 `.specs/<slug>/` 内自闭环流转；
- **会话内授权内联接力**：每个阶段工件生成后设置人机确认闸门，经人类指令确认后，Agent 自动在当前会话内加载下一阶段技能协议继续推演，无需开发者反复退出重敲命令；
- 实时渲染推进状态看板与待办清单；遇到意外阻塞或上下文逼近极限时调用 `at-handoff` 保护现场；
- 技能依赖矩阵参考 [全局工作流总控路由协议](./references/protocols/workflow-routing-protocol.md)。

### 阶段 5：全生命周期闭环审计与 Issue 回填 (Audit & Backfill)
- 核对全链路工件契约（规格、微任务、单测、实现、审查报告 100% 齐备）；
- 执行代码质量与排版门禁自检，阻断违规变更；严格遵循 Git 两级授权原则；
- 输出格式化 Issue 结项回填摘要，支持一键通过 CLI 回贴或手动复制回贴；
- 总结本次研发效能与工程质量收益，生成交付复盘报告。

## 质量控制与合规自检 (Quality Checklist)
- [ ] 意图诊断准确，推荐的配方与技能子集严格遵循最小特权原则；
- [ ] 流水线推进过程透明，每个阶段向开发者提供清晰的状态看板与交付物说明；
- [ ] 阻断越级操作：未确认契约前严禁跳步编写业务代码；
- [ ] 严格遵守 Git 两级授权原则，代码提交与远端推送绝不越权自主执行；
- [ ] 所有文档输出严格服从盘古之白中西文排版与相对路径规范。

## 知识索引地图 (Knowledge Map)

| 知识模块 | 相对路径 | 核心内容说明 |
| :--- | :--- | :--- |
| 总控路由协议 | `./references/protocols/workflow-routing-protocol.md` | 四层金字塔模型、Issue 联动契约、内联推进协议与配方矩阵 |
| 交互向导模板 | `./references/templates/workflow-menu-template.md` | 场景菜单、阶段确认闸门、状态看板与 Issue 回填摘要模板 |
| 特性忽略模板 | `./references/templates/specs-gitignore-template.md` | .specs/.gitignore 瞬态工件忽略规则与防污染规范 |
| 实战案例样本 | `./examples/sample-workflow-orchestration.md` | 基于 Issue #42 的全生命周期 6 大技能会话内内联协同实战全流程 |

## 交付成果规范 (Deliverables Benchmark)
- **特性闭环工件包**：落盘于 `.specs/issue-<id>-<slug>/` 下的完整规格、微任务与审查报告；
- **工作流推进看板**：清晰展示当前步骤、完成项与待办项的 Markdown 进度看板；
- **Issue 完工回填摘要**：包含变更概述、自测验证结果与审查结论的标准化评论草案；
- **全生命周期产物包**：包含规范、代码、单测、审查报告与发版标签的完整成果；
- **跨会话接力索引**：需要切会话时同步输出的开箱即用 `HANDOFF.md`。
