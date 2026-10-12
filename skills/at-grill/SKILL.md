---
name: at-grill
description: 当用户需要对架构方案、业务需求、技术选型或重大决策进行反向压迫式质询与压力测试时使用此技能。提供苏格拉底式发掘、设计树前沿分轮质询、事实自动探查与构建者视角反审（Builder Check），交付收敛完备的共识决策树与权衡清单。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - brainstorming
    - grilling
    - requirements
    - builder-check
  icon: chat-question
---

# 深度质询与构建者反审编排器 (Grilling Orchestrator)

将模糊需求、架构构想或重构草案转化为高度收敛、无隐形假设的工程共识。作为轻量化状态机运行，依托设计树推进前沿，并强制执行构建者视角（Builder Check）防御性质询。

## 渐进式知识地图 (Progressive Disclosure Map)

所有质询协议、反审基准与实战范例均存放于对应目录：
- **设计树前沿质询协议**：[grilling-protocol.md](references/protocols/grilling-protocol.md)（设计树建模、事实探查红线与单轮前沿集中发问规范）
- **构建者视角反审协议**：[builder-check-protocol.md](references/protocols/builder-check-protocol.md)（六大硬核落地考点、权衡矩阵与交付门禁）
- **全流程实战案例**：[grill-session-example.md](examples/grill-session-example.md)（从模糊需求到决策收敛的完整问答全景）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：需求接入、设计树建模与自主事实探查 (Tree Mapping & Fact Probe)

1. **输入意图识别与拓扑建模**：
   - 接收用户的模糊业务需求、架构提案、特性 RFC 或选型思路；
   - 形式化拆解为带前置依赖关系的“设计决策树 (Design Tree)”，将每一个核心分歧点标定为独立决策节点。
2. **事实探查与价值决策严格隔离红线**：
   - **客观事实 (Ground Facts)**：代码库拓扑、现有中间件版本、项目配置等一律由 Agent 依托本地工具链自主扫描查证，**坚决杜绝向用户询问可通过自身探查获知的事实**。
   - **主观决策 (Subjective Decisions)**：业务侧重、技术路线取舍、成本容忍度由用户决断，作为未决分支纳入前沿。
3. **计算首轮决策前沿 (Frontier)**：
   - 识别所有前置依赖已全部清零、当前即可独立判定的决策点，作为当前轮次的发问集合。

### 阶段 2：分轮次前沿集中质询与推荐方案 (Frontier Questioning Rounds)

1. **单轮集中交互契约**：严格遵循 [grilling-protocol.md](references/protocols/grilling-protocol.md) 交互规范，将当前前沿所有问题一次性完整列出：
   - 标注显式编号 `❓ Q{序号}` 与问题标题；
   - 展开问题上下文，并提供 2~3 个具名可选方案及其收益与代价；
   - 必须在题末明确给出基于工程现实的 `➡️ 推荐决策` 及充分技术论据。
2. **交互轮次推进与树状态转移**：
   - **强制停止工具调用**：完成当前前沿发问后立即退出本轮工具调用，等待人类用户答复；
   - 用户反馈后，固化选定分支，剪枝未选分支，解锁下游依赖节点并动态重算下一轮决策前沿；
   - **多选分歧裁决**：若用户提出选项外的新诉求，就地将其转化为新决策节点嫁接至设计树并重新前沿评估。
3. **循环推进直至前沿收敛**：
   - 严禁提前质询下游依赖未就绪的子问题；
   - 持续推进直至所有设计分支均被探索且前沿集合收敛为空（$\emptyset$）。

### 阶段 3：构建者视角反审与落地压力测试 (Builder Check Phase)

设计树前沿收敛后，强制激活 [builder-check-protocol.md](references/protocols/builder-check-protocol.md) 门禁：
1. **身份切换**：以“明日负责写出生产可用代码、上线扛流量并值班的资深研发”视角开展防御性审查。
2. **六大落地考点硬性拷问**：
   - 契约接口数据结构是否完备且强类型？
   - 极端并发、超时、降级与空集合故障域表现？
   - 是否引入破坏性变更及依赖爆炸半径？
   - 生产可观测性（Trace ID、指标、告警阈值）是否清晰？
   - 变更是否具备 5 分钟内平滑回滚与降级能力？
   - 10 倍容量下的 CPU/IO 瓶颈与容量天花板？
3. **权衡决策矩阵固化**：将所有核心取舍整理为结构化的《权衡决策矩阵 (Trade-offs Matrix)》。

### 阶段 4：共识收敛与下游工程移交 (Consensus Convergence & Handoff)

1. **成果物结构化交付**：
   - 输出《架构共识决策备忘录》：包含完整决策树拓扑摘要与权衡矩阵表格；
   - 执行假共识自检：杜绝任何未经用户首肯的隐性假设；
   - 严格核验正文与活动链接零本地绝对路径泄漏。
2. **平滑进入下游生命周期**：
   - 若需拟定详细接口规格或增量契约，推荐唤起 `at-spec` 技能；
   - 若直接开展编码工序微任务拆解，推荐唤起 `at-plan` 技能；
   - 若涉及系统级技术方案撰写，推荐唤起 `at-tech-doc` 技能。


