---
name: at-spec
description: 当用户需要对存量系统或新功能拟定增量规格契约（Delta Specs）、定义接口增量契约、声明系统不变式（Invariants）或防止文档脱节膨胀时使用此技能。提供 OpenSpec 差分规格模型、500 字符原子防膨胀守卫与可测试性契约生成，交付标准化机器可读规格文件。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - specification
    - openspec
    - delta-spec
    - contract
  icon: file-contract
---

# 增量规格契约编排器 (Delta Spec Orchestrator)

将业务共识与需求特性转化为轻量、原子、机器可读且永不漂移的增量规格契约（Delta Specs）。作为轻量化状态机运行，以存量代码库为真理基线，严格约束每项变更在 500 字符防膨胀守卫内，并无缝对接 TDD 测试断言。

## 渐进式知识地图 (Progressive Disclosure Map)

所有规格协议、交付模板与实战案例均存放于对应目录：
- **增量契约设计协议**：[delta-contract-protocol.md](references/protocols/delta-contract-protocol.md)（差分契约模型、500 字符防膨胀守卫与断言转化律）
- **增量规格交付模板**：[delta-spec-template.md](references/templates/delta-spec-template.md)（元数据头、Delta 三元组、不变式与故障域模板）
- **实战参考样例**：[sample-delta-spec.md](examples/sample-delta-spec.md)（用户注销 7 天冷静期增量规格完整示范）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：基线真理探查与影响面标定 (Baseline Probe & Blast Radius)

1. **存量代码基线核查 (Ground Baseline Check)**：
   - 以当前代码库现有实现（Controller、Service、Entity、DB Schema）作为唯一事实基线；
   - 探查涉及模块的方法签名、现有参数校验规则（如 JSR-303 / 显式校验）与返回类型；
   - **真实性硬性门禁**：严禁凭空臆造未核验的方法签名或数据库字段，凡存量方法必须基于探查证据。
2. **爆炸半径 (Blast Radius) 划界与冲突预警**：
   - 明确标注直接受影响的包/类/接口与间接受影响的下游消费者或事件订阅者；
   - 检查外部依赖库版本，提前排查是否存在潜在版本冲突或破坏性变更（Breaking Changes）；
   - 若发现存量接口不兼容，必须在计划中优先设立过渡版本或双轨并存机制。

### 阶段 2：三元差分契约精准提取 (Delta Synthesis: Added / Modified / Removed)

依据 [delta-spec-template.md](references/templates/delta-spec-template.md) 模板拟定增量契约：
1. **Added (新增契约提取)**：
   - 仅描述本次全新引入的接口、实体字段、事件枚举或配置项；
   - 强制声明参数强类型、输入前置条件、状态迁移与输出产物。
2. **Modified (变更契约比对)**：
   - 严格采用“Before vs After”双栏对照呈现具体业务逻辑或接口行为变化；
   - 详细阐述向后兼容过渡措施，明确存量客户端调用时的默认降级路径。
3. **Removed (移除契约废弃)**：
   - 记录废弃的方法、不再使用的字段或历史冗余配置，提供明确的平滑迁移指引；
   - 标注软废弃（Deprecated）标记与计划硬删除（Hard Delete）的生命周期窗口。
4. **防膨胀守卫与原子化拆解**：
   - 执行 [delta-contract-protocol.md](references/protocols/delta-contract-protocol.md) 规则，单项 Delta 描述严格限制在 500 字符内；
   - 若某项业务变更文字说明超过 500 字符，强制原子拆解为多个具名子契约。

### 阶段 3：核心不变式与故障域兜底 (Invariants & Failure Domains)

1. **不可打破的不变式声明 (System Invariants Guard)**：
   - 提炼至少 2 条跨本次变更的核心守恒律（如金额守恒、状态单调递增、空集合安全契约）；
   - 不变式必须作为后续单元测试与集成测试的硬性断言条件，杜绝任何旁路破绽。
2. **故障域与异常映射 (Failure Domains & Exceptions)**：
   - 枚举并发重入、网络超时、下游崩溃、连接池耗尽等极端故障场景；
   - 明确 HTTP 状态码、业务错误码、异常类型与降级容错表现，杜绝未防御的直接崩溃。

### 阶段 4：人机确认闸门与下游流水线移交 (Approval Gate & Pipeline Handoff)

1. **交付物落盘与审阅闸门**：
   - 默认将增量规格持久化至 `spec-delta.md` 或项目规范目录（如 `.specs/<feature-id>-delta.md`）；
   - **强制停止工具调用**：向用户展示增量契约提纲，提供文件链接，等待用户审阅与确认；
   - **就地修订原则**：若用户对任何 Delta 提出异议，必须优先在增量规格中就地修正并重新核对，确认通过后方可冻结。
2. **流水线下一棒移交**：
   - 移交 `at-plan`：将结构化 Delta 契约拆解为 2~5 分钟的微任务流水线清单（`tasks.md`）；
   - 移交 `at-tdd`：将契约中的 Given-When-Then 直接映射为测试驱动红绿灯循环；
   - 若变更涉及系统顶层架构重构，推荐唤起 `at-tech-doc` 编写全景 RFC；
   - 严格遵循盘古之白排版规范，全文档杜绝任何 `file:///` 或本地物理盘符泄漏。



