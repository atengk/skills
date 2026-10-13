---
name: at-assess
description: 当用户需要对新功能创意、技术改造提案、第三方依赖引入或重大架构变更开展可行性预研与技术 Spike 评估时使用此技能。提供代码基线核验、五维风险量化评估（可行性/复杂度/安全/运维/ROI）与证据驱动的 Go / Clarify / Stop 明确裁决，交付标准化可行性评估报告。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[spike|feasibility|tech-stack]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - assessment
    - feasibility
    - spike
    - architecture-decision
  icon: file-search
---

# 方案可行性评估与预研编排器 (Assess & Feasibility Orchestrator)

将模糊创意、重构设想或第三方组件引入提案转化为证据驱动、五维量化、结论明确的可行性预研报告。作为轻量化状态机运行，基于代码库基线与真实信源进行前置压力测试，输出明确的“Go / Clarify / Stop”裁决，及早阻断低效投入。

## 渐进式知识地图 (Progressive Disclosure Map)

所有评估协议、交付模板与实战案例均存放于对应目录：
- **决策矩阵裁决协议**：[decision-matrix-protocol.md](references/protocols/decision-matrix-protocol.md)（证据驱动原则、五维评估标准、三态裁决准则与 Spike 设计规范）
- **可行性评估报告模板**：[assess-report-template.md](references/templates/assess-report-template.md)（元数据头、五维评分表、确凿证据链与后续路线模板）
- **可行性评估实战案例**：[sample-assessment.md](examples/sample-assessment.md)（引入 GraphQL 替代 REST 网关可行性预研与止损案例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：提案接入与基线真理探查 (Proposal Ingestion & Baseline Probe)

1. **输入意图解析与痛点标定**：
   - 提取用户的核心技术诉求、期望收益与拟采用的技术路线；
   - 标定提案属于全新功能（New Feature）、技术探针（Tech Spike）还是架构改造（Architecture Change）；
   - 划分利益相关方影响面，标定上下游业务系统的依赖矩阵与服务等级协议（SLA）。
2. **存量代码库基线扫描 (Ground Truth Probe)**：
   - 自主探查现有工程的技术栈版本、构建配置、中间件依赖与核心数据模型；
   - 寻找与提案相关的存量接口与实现，核实生态兼容性，**严禁凭空臆测外部兼容情况**；
   - **双源探针核验**：涉及外部新组件引入时，通过官方文档与权威信源核验其 LTS 支持与已知缺陷。

### 阶段 2：五维风险与收益量化推演 (Five-Dimensional Analysis)

依据 [decision-matrix-protocol.md](references/protocols/decision-matrix-protocol.md) 展开正交五维打分（1~5 分）：
1. **技术可行性 (Feasibility)**：分析框架生态适配度，排查底层连接池、序列化模型是否存在冲突；
2. **改动复杂度 (Complexity)**：评估爆炸半径，统计涉及重写的类/接口数量与数据表迁移成本；
3. **数据一致性与事务边界 (Consistency)**：评估是否打破既有本地事务完整性，是否引入分布式事务复杂性；
4. **安全与合规 (Security)**：排查是否引入未受控的权限穿透、外部注入面或数据合规隐患；
5. **维护与运维 (Operability)**：评估 APM 链路监控追踪、日志排障透明度与单点容灾降级能力；
6. **投入产出比 (ROI)**：严密比对研发周期与业务实际收益，排查是否存在 ROI 严重倒挂；
7. **团队技术债反噬评估**：预估新方案对团队整体心智负担与新人上手坡度的长期影响。

### 阶段 3：确凿证据提取与决策三态裁决 (Evidence & Three-State Verdict)

依据五维推演结果，给出唯一明确的工程裁决，严禁模棱两可：
1. **🟢 GO (准予推进)**：五维表现健康，无硬伤且收益明确，给出推荐实施路线；
2. **🟡 CLARIFY (澄清补全)**：存在关键未决技术假设，给出精准限定时间盒（Timebox）的 Spike 实验建议；
3. **🔴 STOP (终止立项)**：触碰架构红线、存在不可调和的缺陷或 ROI 严重倒挂，果断给出终止理由并提供轻量替代方案；
4. **证据准入硬红线**：严禁无证据主观裁决，每个维度的评分必须标注本地代码或官方规范出处。

### 阶段 4：人机确认闸门与下游流程移交 (Approval Gate & Pipeline Handoff)

依据 [assess-report-template.md](references/templates/assess-report-template.md) 落地最终成果：
1. **交付物落盘与审阅闸门**：
   - 统一将评估报告落盘至长期知识资产目录 `docs/spikes/XXXX-title.md`（或呈现于会话），严禁在根目录平铺；
   - **强制停止工具调用**：向用户展示五维打分卡与裁决结论，提供直达链接，等待用户审阅确认；
   - 若用户对评估结论存疑，就地展开单项证据复验或调整五维权重参数；
   - 严格遵循盘古之白排版规范，全文档杜绝任何 `file:///` 或本地物理盘符泄漏。
2. **平滑移交下游工程链路**：
   - 裁决为 GO：若涉及重大决策推荐唤起 `at-adr` 留痕，随后移交 `at-spec` 制定增量契约；
   - 裁决为 CLARIFY：引导唤起 `at-grill` 针对未决分歧开展压迫式反向质询；
   - 裁决为 STOP：方案就地归档，避免团队陷入无效沉没成本；
   - 深度对齐组织业务目标，杜绝为技术而技术的虚构诉求；
   - 恪守证据驱动原则，确保每项决策立足真实基线；
   - 闭环全生命周期前置决策，筑牢架构设计基石。





