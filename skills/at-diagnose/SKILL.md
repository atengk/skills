---
name: at-diagnose
description: 当用户遇到疑难 Bug、偶发并发缺陷、报错异常堆栈、性能劣化或需要系统化排查定位根因时使用此技能。提供紧反馈循环构建（Tight Loop）、最小化复现（Minimization）、可证伪假设验证、带标探针隔离与纵深防御修复，交付根因诊断报告与永久回归测试。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - debugging
    - troubleshooting
    - root-cause
    - systematic-debugging
  icon: bug-scanner
---

# 系统化根因排错编排器 (Systematic Debugging Orchestrator)

将模糊报错、疑难 Bug 与生产诡异故障转化为确定性复现、确凿证据链与纵深防御修复。作为轻量化状态机运行，强制执行“无紧反馈循环不推测根因”铁律，杜绝盲目看代码瞎猜与表面打补丁，输出具备永久回归保障的稳健工程产物。

## 渐进式知识地图 (Progressive Disclosure Map)

所有排错协议、诊断模板与实战案例均存放于对应目录：
- **系统化排错执行协议**：[systematic-debugging-protocol.md](references/protocols/systematic-debugging-protocol.md)（紧反馈循环法则、可证伪假设推演、探针打标与深度防御准则）
- **诊断报告交付模板**：[diagnostic-report-template.md](references/templates/diagnostic-report-template.md)（故障元数据、复现命令、假设树、根因剖析与防范建议模板）
- **疑难排查实战案例**：[sample-debugging-session.md](examples/sample-debugging-session.md)（事务与并发监听脏读缺陷的四步法排错完整全景）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：构建紧反馈循环与最小化复现 (Feedback Loop & Minimization)

依据 [systematic-debugging-protocol.md](references/protocols/systematic-debugging-protocol.md) 构建测试闭环：
1. **构造单行紧反馈命令 (Tight Feedback Loop)**：
   - 优先编写失败单测（单元/集成/端到端），其次为轻量脚本（curl/CLI/测试桩）；
   - **红灯可复现性门禁**：该命令必须在数秒内稳定跑出用户描述的精确故障表现；
   - 坚决杜绝在没有可运行复现命令前空想推测代码；
   - **安全停机协议**：若受限于外部网络或凭据完全无法建立自动化循环，必须停下并请求用户提供脱敏环境日志，严禁盲目猜测。
2. **场景最小化削减 (Minimise)**：
   - 逐项砍掉非承重的入参、外部依赖服务与多余配置；
   - 锁定导致故障发生的最小必要条件集。
3. **偶发/并发缺陷加压提率**：
   - 针对非确定性 Bug，通过增加并发压力或循环执行 50~100 次，将复现率提高到可观测阈值。

### 阶段 2：穷举可证伪假设与探针证据链 (Falsifiable Hypotheses & Evidence)

1. **穷举 3~5 个按概率排序的假设**：
   - 严禁陷入单一假设的“先入为主”误区；
   - 每一个假设必须具备**明确的可证伪预测**（“若因为 X，则调整 Y 时故障必定表现为 Z”）。
2. **注入受控探针并单变量验证**：
   - 遵循零污染协议：所有临时日志统一添加随机前缀（如 `[DEBUG-xxxx]`）；
   - 一次只改变一个变量，观察紧反馈循环命令输出是否符合预测；
   - 记录确凿数据链（时间戳、调用栈、状态值），锁定物理根因。

### 阶段 3：纵深防御修复与反打补丁铁律 (Deep Defensive Fix)

1. **溯源物理根因 (Root Cause Analysis)**：
   - 运用 5 Whys 因果链溯源数据错误的初始产生源头，而非在末端症状处打补丁；
   - **反打补丁铁律**：严禁无脑包 `try-catch` 或静默兜底吞没真实异常。
2. **多层防御式编码与最小爆炸半径**：
   - 在契约入口增加前置断言与卫语句拦截；
   - 在状态机或数据持久层增加不可打破的不变式守卫；
   - 严格遵循最小变更半径原则，严禁借修复 Bug 之名进行大面积无关重构。

### 阶段 4：回归锁定、探针清理与复盘移交 (Regression Lock & Post-Mortem)

依据 [diagnostic-report-template.md](references/templates/diagnostic-report-template.md) 汇编报告与归档：
1. **见证测试全绿 (Pass)**：重新执行阶段 1 的紧反馈命令，验证测试彻底变绿。
2. **固化为永久回归测试**：将最小复现测试改名为 `*RegressionTest` 沉淀为资产。
3. **彻底清理临时探针**：全局搜索并物理删除所有 `[DEBUG-...]` 临时代码。
4. **输出复盘备忘录与下游移交**：
   - 向用户输出《缺陷根因诊断报告》；
   - 修复完成后，引导唤起 `at-review` 开展双轴代码审查，核验修复是否引入新坏味道；
   - 总结导致缺陷的深层架构因素，必要时引导调用 `at-tech-doc` 编写重构方案；
   - 确保因果链闭环自洽，不留任何悬空疑点；
   - 形成持续改进闭环，防止同类问题再次滋生；
   - 严格遵循盘古之白排版规范，全文档杜绝任何本地绝对路径泄漏。



