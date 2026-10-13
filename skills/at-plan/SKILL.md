---
name: at-plan
description: 当用户需要将架构方案、需求规格（Spec）或复杂开发任务拆解为可落地执行的工序与任务清单时使用此技能。提供 2~5 分钟极小颗粒度原子微任务编译、DAG 依赖拓扑图谱解析、示踪线（Tracer Bullet）优先推进与断点续做打卡机制，交付标准化任务拆解文档（.specs 特性工件目录 tasks.md）。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[breakdown|dag|tasks]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - planning
    - tasks
    - workflow
    - tracer-bullet
  icon: list-check
---

# 工序拆解与任务编排器 (Plan & Task Orchestrator)

将高维需求规格（Spec）与架构方案编译为极小颗粒度、零歧义、自包含的原子实施任务清单（`.specs/<feature-slug>/tasks.md`）。作为轻量化状态机运行，依据 DAG 依赖图谱与示踪线（Tracer Bullet）原则组织工序，确保每个微任务在 2~5 分钟内可单次闭环验证。

## 渐进式知识地图 (Progressive Disclosure Map)

所有任务编排协议、工序模板与实战案例均存放于对应目录：
- **依赖图谱与拆解协议**：[dependency-graph-protocol.md](references/protocols/dependency-graph-protocol.md)（2~5 分钟微任务法则、示踪线优先纪律与 DAG 拓扑分析）
- **原子任务清单模板**：[tasks-template.md](references/templates/tasks-template.md)（元数据头、Mermaid 依赖图、微任务卡片与 DoD 门禁模板）
- **完整计划实战案例**：[sample-plan-tasks.md](examples/sample-plan-tasks.md)（注销冷静期从 Spec 编译为 6 个微任务的真实范例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：规格契约接入与上下文校验 (Spec Ingestion & Validation)

1. **输入契约完整性校验**：
   - 读取前序增量规格文件（如 `.specs/<feature-slug>/delta.md`、特性 RFC 或会话上下文）；
   - 校验契约输入是否包含明确的输入参数、输出产物、不变式（Invariants）与异常故障域；
   - 若前置输入存在重大边界含糊，阻断任务拆解并引导用户先唤起 `at-grill` 质询或 `at-spec` 补全。
2. **工程上下文探查与规模评估**：
   - 探查本地测试框架与构建工具，**自动识别单模块 vs 多模块/Monorepo 拓扑（严禁使用 cd 切换目录）**；
   - 确定微任务必须采用的工程验证命令基线（如单测试方法运行命令）；
   - 扫描当前仓库分支与环境依赖，识别是否存在未满足的环境前置条件；
   - 评估拆解规模：若预估微任务总数超过 10 个，强制划分为多个具备阶段交付物的 Phase。

### 阶段 2：示踪线主干划定与 DAG 依赖建模 (Tracer Bullet & DAG Modeling)

1. **确立示踪线优先纪律 (Tracer Bullet Priority)**：
   - 坚决拒绝传统自底向上的全量堆砌模式（如先写完全部表再写完全部业务）；
   - 优先提取核心 Happy Path 形成首条贯穿数据层到控制层的垂直示踪线（通常在前 2~3 个任务闭环）；
   - 示踪线必须贯通“最小测试用例 -> 最小骨架实现”，验证框架注脚与链路畅通。
2. **构建有向无环依赖图 (DAG Topology)**：
   - 依据组件交互关系标定前置依赖边（`Blocked By`）；
   - 识别入度为 0 的并行启动点，并明确关键路径阻塞链；
   - 提取可并行开发的无阻塞子任务组，为后续多 Agent 协同派发奠定拓扑基础；
   - 使用开放 Mermaid 语法生成拓扑图，直观暴露依赖瓶颈与并行加速机会。

### 阶段 3：原子微任务结构化编译 (Atomic Task Compilation)

严格遵循 [tasks-template.md](references/templates/tasks-template.md) 编译微任务清单，每项任务必须满足**四要素完备性门禁**：
1. **显式前置依赖**：清晰标明 `Task XX`，无依赖则标为无，杜绝隐式先行；
2. **精确相对路径**：列出具体的新建或修改文件路径，杜绝模糊通配符；
3. **极简核心动作**：明确改动的函数、新增字段或单测红灯断言，耗时控制在 2~5 分钟微任务规模；
4. **确定性自检命令**：提供单行终端验证指令（单模块如 `mvn test -Dtest=...`，多模块必须携带 `-pl <module> -am`、`--filter` 等裁剪定位参数；若修改公共模块末尾追加下游级联校验任务）；
5. **反模式拦截铁律**：严禁出现跨层大包揽任务（如“实现所有接口”），凡无法在 5 分钟内完成的代码改动一律二次拆解。

### 阶段 4：人机确认闸门与断点续做交接 (Human Approval Gate & Execution Handover)

1. **交付物落盘与审阅闸门**：
   - 统一将任务清单持久化至特性工件目录 `.specs/<feature-slug>/tasks.md`，严禁在工程根目录平铺；
   - **强制停止工具调用**：向用户展示任务拆解摘要，提供文件直达链接，等待用户审阅与确认；
   - 用户提出范围或颗粒度调整时，就地重新校准任务清单并重算 DAG 依赖图；
   - 正文严格遵循盘古之白排版规范，严禁出现任何 `file:///` 或本地物理盘符泄漏。
2. **下游研发执行移交与断点打卡**：
   - 引导调用 `at-tdd` 技能，严格按照任务清单自上而下推进红绿重构循环；
   - 每次任务完成并通过验证后，就地更新清单状态由 `- [ ]` 变为 `- [x]`；
   - 全部任务完成后，引导进入 `at-review` 开展双轴代码审查，或进入 `at-diagnose` 追踪疑难异常；
   - 支持跨会话或子代理断点续做，扫描首个未完成任务即可毫秒级锁定开工锚点；
   - 恪守示踪线优先与任务自包含原则，降低长时运行心智负担；
   - 筑牢原子任务拆解防线，保障代码变更透明可追踪。
