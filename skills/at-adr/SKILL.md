---
name: at-adr
description: 当用户需要记录重大架构决策、治理 ADR 生命周期、对比评估多种技术路线方案、权衡正负利弊与 Trade-off 或回溯纳管技术债务时使用此技能。提供 MADR 3.0 标准化流程与全生命周期状态机管理，交付工业级架构决策记录（ADR）。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[new|list|review|deprecate]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - adr
    - architecture-decision
    - madr
    - technical-debt
    - decision-record
  icon: file-badge
---

# 架构决策记录治理编排器 (ADR Governance Orchestrator)

将架构演进中的关键技术选型、重大路线分歧与折衷妥协转化为结构化、机器可检索、长期可追溯的《架构决策记录》（ADR）。作为轻量化状态机运行，贯穿 MADR 3.0 规范，提供从决策背景提炼、多选项正交权衡、正负后果分析到生命周期流转（Proposed/Accepted/Deprecated/Superseded）的系统性治理基石。

## 渐进式知识地图 (Progressive Disclosure Map)

所有 ADR 生命周期规范、交付模板与实战案例均存放于对应目录：
- **ADR 生命周期与治理协议**：[adr-lifecycle-protocol.md](references/protocols/adr-lifecycle-protocol.md)（MADR 3.0 标准、状态流转状态机、选项权衡分析模型、技术债回溯与还款协议）
- **架构决策记录规范模板**：[adr-template.md](references/templates/adr-template.md)（元数据声明、背景上下文、驱动力、决策结论、正负后果与利弊详查模板）
- **嵌入式存储选型实战案例**：[sample-adr.md](examples/sample-adr.md)（高并发会话状态机采用 RocksDB 替代分布式缓存的真实 ADR 范例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：决策诱因识别与工程上下文提炼 (Context & Trigger Ingestion)

1. **架构决策触发场景识别**：
   - 识别导致必须做出决策的技术诉求（如关键技术选型、存储架构迁移、模块解耦与协议重构）；
   - 提取业务瓶颈、系统 SLA 考核指标与核心非功能性要求（延迟、吞吐、成本、维护性）；
   - 探查存量代码库既有的技术栈基准，厘清决策约束与边界条件；
   - 自动扫描工程中已存在的 ADR 目录（`docs/adr/`），解析历史决策脉络并计算下一个递增编号。
2. **决策驱动力 (Decision Drivers) 结构化排序**：
   - 提炼影响本次决策的核心驱动因素（如极端低时延、内存预算受限、学习曲线陡峭度）；
   - 区分核心刚性要求（Hard Constraints）与锦上添花期望（Nice-to-haves）；
   - 严禁空洞陈述，每项驱动力必须绑定具体的业务指标或痛点。

### 阶段 2：候选方案调研与正交利弊权衡 (Multi-Option Trade-off Analysis)

依据 [adr-lifecycle-protocol.md](references/protocols/adr-lifecycle-protocol.md) 展开正交推演：
1. **候选路线矩阵拟定**：必须列出至少 2~3 个具有现实竞争力的备选技术选项（包含主流方案与保持现状方案）；
2. **决策类型与可逆性评估**：区分单向门决策（重大不可逆改动）与双向门决策（轻量可快速试错），实施分级审议；
3. **多维度优缺点客观剖析**：
   - 针对每个选项，客观详述优势（Good, because...）与短板（Bad, because...）；
   - 杜绝预设立场的片面贬低，真实反映各技术路线的客观物理特性；
4. **正负后果与技术债明确定性**：
   - 正面收益（预期达成的具体度量指标与架构红利）；
   - 负面代价（引入的运维复杂度、状态持久化约束或潜在技术债）；
   - 若采纳权宜妥协方案，必须显式标注技术债赎还期限与演进里程碑。

### 阶段 3：人机评审裁决与文档落盘 (Review Verdict & ADR Persistence)

依据 [adr-template.md](references/templates/adr-template.md) 落地最终成果：
1. **ADR 草案呈现与共识达成**：
   - 标定初始状态为 `Proposed`（提议中），在会话中呈现决策结论与对比摘要；
   - **强制停止工具调用**：向用户展示 ADR 决策结论与权衡理由，提供直达链接，等待用户审阅与确认；
   - 根据人类架构师评审意见，将状态更新为 `Accepted`（已采纳）或 `Rejected`（已否决）；
   - 严格遵循盘古之白排版规范，全文档杜绝任何 `file:///` 或本地物理盘符泄漏。
2. **标准化资产落盘与编号规约**：
   - 统一写入 `docs/adr/XXXX-title.md`（按四位数字递增编号）；
   - 自动维护或更新 `docs/adr/README.md` 全局决策索引表。

### 阶段 4：生命周期维护与架构演进闭环 (Lifecycle Maintenance & Handoff)

1. **处理决策演进与继承**：
   - 若本次决策推翻了旧决策，必须在新 ADR 标明替代关系，并将旧 ADR 状态标记为 `Superseded by ADR-XXXX`；
   - 保持架构决策演进树的清晰、可回溯与单向因果链；
   - 定期体检存量 ADR 标定的技术债务，触发还款提醒；
2. **平滑移交下游工程实现**：
   - 决策落地后，引导唤起 `at-spec` 制定承接该架构决策的详细功能与技术规格；
   - 驱动后续 `at-plan` 拆解重构微任务，确保架构决策在代码实现中 100% 兑现；
   - 确保架构演进全量留痕，杜绝口口相传的信息断层与腐化；
   - 赋能团队建立基于实证的架构文化，实现有序演进；
   - 筑牢企业级架构可解释性与长期工程自治防线。
