---
name: at-runbook
description: 当用户需要为生产服务编写或更新运维应急手册 Runbook、制定突发故障响应预案、梳理核心黄金指标告警排查路径、沉淀高并发止血 SOP (回滚/降级/限流/扩容) 或规整运维故障自愈步骤时使用此技能。提供故障等级评估、先止血后排障决策树构建、线程日志现场抓取与恢复验收编排，交付标准化、步骤可复制且 10 分钟止血的工业级应急手册。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[incident|sop|recovery]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - runbook
    - sre
    - incident-response
    - troubleshooting
    - rollback
  icon: alert-triangle
---

# 运维应急手册与故障响应编排器 (Incident Runbook Orchestrator)

在生产系统面对突发严重故障与告警风暴时构筑确定性的生命救援防线。作为轻量化状态机运行，贯彻 SRE 站点可靠性工程“先止血后排障”与“1-5-10”黄金响应原则，针对线上事故发生时值班人员慌乱无序、缺乏可执行 SOP、原地分析代码耽误止血等致命痛点，编排从故障影响面分级、第一时间回滚/降级/隔离止血指令生成、系统现场快照抓取到恢复验收指标固化的全生命周期。

## 渐进式知识地图 (Progressive Disclosure Map)

所有应急手册模板、SRE 响应规约与工业级案例均存放于对应目录：
- **故障应急排错手册标准模板**：[runbook-template.md](references/templates/runbook-template.md)（故障分级、止血预案、标准化诊断流程与事后复盘模板）
- **SRE 故障应急与操作安全守则**：[sre-incident-protocol.md](references/protocols/sre-incident-protocol.md)（1-5-10 指标、黄金四信号、双人复核红线与不可逆操作规避）
- **数据库连接池故障应急实战案例**：[sample-runbook.md](examples/sample-runbook.md)（HikariCP 满载死锁排查、降级限流与快速止血实操范例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：故障特征萃取与影响面定级 (Incident Profile & Triage)

1. **告警表现与核心异常模式识别**：
   - 关联分析监控告警项（如连接池耗尽、CPU 飙高 100%、5xx 错误率骤增、P99 延时毛刺）；
   - 梳理故障涉及的核心服务、上游调用方与下游强依赖（数据库/缓存/第三方网关）；
   - 梳理受影响的业务 SLA 协议与用户侧可见报错形态；
   - 明确故障第一责任人（Incident Commander）与跨团队协同渠道；
   - 依据 [sre-incident-protocol.md](references/protocols/sre-incident-protocol.md) 评定故障影响面等级（P0/P1/P2）。
2. **高危边界与不可逆操作警示**：
   - 标识该故障场景下严禁执行的危险动作（如高峰期全表删改、未加条件的 kill、重启集群中心）；
   - 确立生产环境操作双人复核前置条件，规范对外通报与客服同步口径。

### 阶段 2：黄金止血 SOP 与回滚预案制定 (Emergency Mitigation & Rollback SOP)

1. **第一响应止血指令 (先止血)**：
   - 检查近 30 分钟内是否有版本变更，将“一键回滚指令”作为步骤 A 置顶；
   - 梳理非核心旁路功能的动态配置降级开关（Feature Toggle），削峰保核心链路；
   - 编排临时实例水平扩容（Scale Out）或有损限流阻断命令；
   - 设定单步止血操作超时阈值（超 3 分钟无效立即切换备选方案），防范二次雪崩。
2. **命令确定性与零假设核验**：
   - 手册中的每一条 shell 或 SQL 指令必须可直接复制，携带参数说明；
   - 检查止血脚本在测试环境的演练验证记录，确保零语法错误；
   - 所有敏感凭据采用标准占位符，严禁泄露真实生产密钥。

### 阶段 3：诊断路径编排与快照现场抓取 (Diagnostic Workflow & Telemetry Capture)

1. **系统现场环境快照保存**：
   - 编写现场保护脚本：导出 JVM 线程快照（`jstack`）、内存直方图、活跃连接数快照；
   - 提取最近 200 条核心错误日志堆栈并过滤高频异常关键字；
   - 锁定故障期间的现场数据，规避实例自动重启导致证据丢失。
2. **标准化排障决策树构建**：
   - 绘制标准 Mermaid 故障排查状态机流程图；
   - 梳理跨可用区网络抖动与第三方接口超时的穿透式诊断排查指南；
   - 给出按层推进的排查路径（服务健康探针 -> 数据库锁等待 -> 慢 SQL 执行计划 -> 缓存击穿）。

### 阶段 4：恢复验收指标固化与手册交付 (Recovery Gate & Safe Delivery)

1. **黄金指标恢复核验单**：
   - 明确故障消除的客观度量门槛（如 5xx 错误率 < 0.05%、P99 延时恢复基线、连接池空闲）；
   - 罗列事故后 24 小时内的 5 Whys 复盘与长效防范改进要求；
   - 将排错经验转化为常态化混沌工程巡检探针与定期桌面推演（Tabletop Exercise）。
2. **手册落盘与工作区留置**：
   - 基于 [runbook-template.md](references/templates/runbook-template.md) 生成文档落盘至 `docs/runbook/<incident-type>.md`；
   - 执行盘古之白排版规范核验，全文档 100% 杜绝本地绝对路径；
   - 成果保留在工作区等待人类审查，未获显式指令绝不擅自提交；
   - 破除面对黑天鹅事件时的慌乱摸索，将经验转化为肌肉记忆；
   - 守卫线上系统的高可用 SLA 与用户资产安全底线。


