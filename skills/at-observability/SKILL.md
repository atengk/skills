---
name: at-observability
description: 当用户需要设计生产级系统可观测性方案、制定 Prometheus 指标与 RED/USE 监控模型、统一结构化日志规范、集成分布式链路追踪或配置容器健康探针时使用此技能。提供现代化可观测性设计协议与埋点模板，交付透明可靠的监控运维体系。
disable-model-invocation: false
disable-slash-command: false
argument-hint: "[metrics|tracing|logging|health]"
allowed-tools:
  - view_file
  - run_command
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags: [observability, prometheus, opentelemetry, logging, metrics]
---

# 生产级系统可观测性与埋点设计技能 (Observability Design Engine)

本技能提供面向分布式系统度量指标（Metrics）、结构化日志（Logging）、全链路追踪（Tracing）与健康探针的生产级可观测性建设体系。

```mermaid
flowchart LR
    S1["1. 业务目标与 SLO 契约梳理"] --> S2["2. RED/USE 指标建模与埋点设计"]
    S2 --> S3["3. 结构化日志与链路上下文穿透"]
    S3 --> S4["4. 健康检查探针与告警规则编排"]
    S4 --> S5["5. 看板集成与演练压测验证"]
```

## 执行流程状态机 (Execution State Machine)

### 阶段 1：业务目标与 SLO 契约梳理 (SLO & Critical Path)
- 梳理服务核心业务流与关键交易路径，明确核心可用性与延迟预算；
- 制定服务的服务等级目标（SLO）与错误预算（Error Budget）阈值；
- 明确基础设施、外部依赖 RPC 与持久化数据库的监控边界与重点关注项；
- 核心指标分类标准参考 [指标日志可观测性协议](./references/protocols/metrics-logging-standards.md)。

### 阶段 2：RED/USE 指标建模与埋点设计 (Metrics & Cardinality)
- 面向应用层建立吞吐量、错误率与耗时分布（RED 范式）的核心指标集；
- 面向系统资源层梳理利用率、饱和度与错误数（USE 范式）度量方案；
- 实施严格的标签基数防御，严禁将用户 ID 或未脱敏动态参数作为 Label 维度；
- 设计标准格式参考 [系统可观测性设计模板](./references/templates/observability-spec-template.md)。

### 阶段 3：结构化日志与链路上下文穿透 (Logging & Tracing)
- 统一 JSON 格式结构化日志输出，确保时间戳、日志级别与业务字段对齐；
- 集成 W3C Trace Context，实现全局 Trace ID 与 Span ID 跨网络线程透明透传；
- 制定自动脱敏策略，阻断鉴权凭证、个人隐私与机密信息明文打印；
- 完整支付埋点与日志样本参考 [支付链路埋点实战样例](./examples/sample-observability-design.md)。

### 阶段 4：健康检查探针与告警规则编排 (Probes & Alerting)
- 设计解耦的存活（Liveness）与就绪（Readiness）探针，杜绝因外部故障引发雪崩；
- 编写多级 Prometheus 告警规则（Warning、Critical、Disaster），配置告警收敛；
- 明确告警触发后的首要处置动作与应急响应预案（SOP）关联关系；
- 探针与告警规范参考 [指标日志可观测性协议](./references/protocols/metrics-logging-standards.md)。

### 阶段 5：看板集成与演练压测验证 (Dashboard & Verification)
- 规划 Grafana 业务与系统监控看板视图布局，呈现 P95/P99 延迟走势；
- 结合压力测试与故障注入演练，验证告警触发准确性与指标上报实时性；
- 确保相关设计文档满足盘古之白排版与相对路径引用规范。

## 质量控制与合规自检 (Quality Checklist)
- [ ] 严格杜绝在 Prometheus 指标标签中引入高基数动态变量（如 UUID/用户 ID）；
- [ ] 存活探针（Liveness）绝不强依赖下游数据库或远程第三方连通性；
- [ ] 结构化日志必须包含统一的 Trace ID 关联字段，方便快速端到端检索；
- [ ] 告警规则配置明确的持续时间（`for` 窗口），避免偶发毛刺引发告警风暴；
- [ ] 所有文档排版中西文及数字间距符合盘古之白规范，无绝对路径泄漏。

## 知识索引地图 (Knowledge Map)

| 知识模块 | 相对路径 | 核心内容说明 |
| :--- | :--- | :--- |
| 可观测性协议 | `./references/protocols/metrics-logging-standards.md` | RED/USE 模型、Prometheus 规范、日志脱敏与健康探针 |
| 埋点设计模板 | `./references/templates/observability-spec-template.md` | 服务级 SLO、指标矩阵、PromQL 告警与 K8s 探针配置模板 |
| 实战案例样本 | `./examples/sample-observability-design.md` | 在线支付链路指标埋点、链路透传与结构化日志样例 |

## 交付成果规范 (Deliverables Benchmark)
- **可观测性设计书**：包含 SLO 定义、指标矩阵与告警阈值的技术方案；
- **埋点实现代码**：遵循统一命名规范与低基数原则的指标收集与日志代码；
- **告警规则配置文件**：标准化 Prometheus Alertmanager 告警规则 YAML 文件；
- **Grafana 看板配置**：结构化的看板仪表盘 JSON 模型导出文件；
- **探针健康检查端点**：符合容器调度规范的轻量存活与就绪 HTTP 路由。
