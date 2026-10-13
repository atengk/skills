---
name: at-constitution
description: 当用户需要为工程项目建立顶层技术法典、确立架构刚性红线、拟定不可违背的工程宪章、实施前置熔断守卫或制定技术栈准入白名单时使用此技能。提供多 Agent 协同法律基线，强化全生命周期合规核验，交付可执行的工程宪章与豁免机制。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[init|check|enforce]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - constitution
    - governance
    - guardrails
    - architecture-standards
  icon: shield-check
---

# 项目工程宪章编排器 (Engineering Constitution Orchestrator)

确立代码库最高法律地位的工程宪章（`CONSTITUTION.md`），为人类开发者与多 Agent 协同构筑刚性守卫红线。作为轻量化状态机运行，从技术栈白名单、分层架构拓扑、反模式禁止项到关键不变式契约，提供机器可核验、前置熔断且支持受控豁免的工程基石。

## 渐进式知识地图 (Progressive Disclosure Map)

所有刚性守卫协议、交付模板与实战案例均存放于对应目录：
- **刚性守卫熔断协议**：[guardrail-enforcement-protocol.md](references/protocols/guardrail-enforcement-protocol.md)（法律级约束原则、全阶段前置核验、违规熔断机制与特批豁免流程）
- **工程宪章规范模板**：[constitution-template.md](references/templates/constitution-template.md)（元数据声明、技术白名单、禁止反模式、安全契约与 ADR 追踪模板）
- **工程宪章实战案例**：[sample-constitution.md](examples/sample-constitution.md)（高并发全栈电商微服务项目的真实工程宪章范例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：工程上下文与现状基因探查 (Baseline Ingestion & Probing)

1. **存量工程拓扑与依赖探查**：
   - 自动扫描项目构建配置（`pom.xml`、`package.json`、`build.gradle` 等），提取现有技术栈与中间件基线；
   - 探查代码目录分层结构、持久层接入范式、公共工具库分布及全局异常处理机制；
   - 识别存量代码中既有的隐性架构共识与潜在历史技术债务；
   - 梳理已有 CI 检查脚本、代码风格配置与静态分析工具现状。
2. **治理目标与利益相关方诉求对齐**：
   - 明确本次宪章制定的核心驱动力（如：新工程规范筑基、多团队协作防劣化、Agent 自治长跑安全守卫）；
   - 梳理团队技术栈演进方向与明确禁止引入的淘汰技术；
   - 明确宪章适用边界，区分核心业务域与外围边缘模块的差异化约束。

### 阶段 2：刚性红线与白名单矩阵拟定 (Rule Formulation & Whitelisting)

依据 [guardrail-enforcement-protocol.md](references/protocols/guardrail-enforcement-protocol.md) 确立工程不可违背的不变式：
1. **技术栈白名单与版本底线**：明确运行时、数据库、缓存、消息队列及核心第三方库的准入清单，严禁非标组件偷渡；
2. **架构分层流向与隔离界限**：
   - 严格限定模块调用拓扑，严禁越级穿透（如 Controller 直调持久层）与模块间双向循环依赖；
   - 持久层实体严禁跨域泄露，对外统一通过契约对象解耦；
3. **关键健壮性契约**：
   - 集合查询无匹配统一返回空集合，严禁返回 `null`；
   - 单实体判空必须在前置使用卫语句显式拦截；
   - 单例服务必须保持无状态，严禁使用可变成员变量共享业务状态；
   - 循环体内严禁发起数据库查询或远程 RPC 调用（彻底杜绝 N+1 陷阱）。
4. **安全合规与零凭据红线**：
   - 代码、配置与文档中严禁任何明文密码、API Token 或物理绝对路径泄漏；
   - 所有凭据必须通过系统环境变量或受管 KMS/配置中心注入。

### 阶段 3：人机评审与熔断守卫确认 (Review & Circuit Breaker Setup)

依据 [constitution-template.md](references/templates/constitution-template.md) 组装并落地工程宪章：
1. **草案呈现与逐条对齐**：
   - 默认生成规范草案并在会话中展示核心条款矩阵，或直接落盘至项目根目录 `CONSTITUTION.md`；
   - **强制停止工具调用**：向用户展示宪章核心约束，提供直达链接，等待用户审阅与逐项修正；
   - 针对团队争议条款展开深度权衡，平衡规范严苛度与日常研发敏捷度。
2. **确立特批豁免流程**：
   - 明确宪章不是死板枷锁，极端紧急场景必须通过人类显式双重授权；
   - 任何违背宪章的临时方案必须强制关联 ADR 登记，设定还债时间盒；
   - 建立豁免到期预警机制，防止技术债务无限期拖延。

### 阶段 4：守卫切面激活与下游工具链集成 (Activation & Integration)

1. **切面嵌入全生命周期**：
   - 推动 `at-assess`、`at-spec`、`at-plan`、`at-tdd` 及 `at-review` 将宪章作为最高准则前置加载；
   - 代码审查时任何宪章违例直接标记为 🔴 Blocker 阻断项；
   - 建议联动本地或 CI 自动化工具（如 ArchUnit、SonarQube）固化机器校验。
2. **规范固化与资产移交**：
   - 宪章写入工程版本库，完成项目治理里程碑；
   - 确保正文严格遵循盘古之白排版规范，全文档杜绝任何 `file:///` 或本地物理盘符泄漏；
   - 为后续所有增量需求研发铸就不可撼动的工程防护网。
