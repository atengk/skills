# 系统可观测性与埋点设计规范模板 (Observability Specification Template)

本文档提供面向分布式系统与关键业务链路的可观测性设计规格书模板，涵盖指标定义、PromQL 告警规则、结构化日志与 Kubernetes 健康探针规范。

---

## 1. 服务概况与 SLO 目标

- **服务名称**：`<service-name>`
- **核心业务职责**：`<service-responsibility>`
- **SLO 目标**：
  - **可用性 (Availability)**：月度正常运行率 ≥ 99.95%
  - **延迟 (Latency)**：核心接口 P95 耗时 ≤ 150ms，P99 耗时 ≤ 300ms
  - **错误预算 (Error Budget)**：每自然月允许的 5xx 故障不可用时长上限

---

## 2. 关键业务与系统指标设计 (Metrics Matrix)

### 2.1 RED 吞吐与延迟指标

| 指标名称 | 类型 | 单位 | 维度标签 (Labels) | 业务含义与说明 |
| :--- | :--- | :--- | :--- | :--- |
| `http_server_requests_total` | Counter | 次数 | `method`, `path`, `status` | HTTP 入站请求总数（用于计算 QPS 与错误率） |
| `http_server_request_duration_seconds` | Histogram | 秒 | `method`, `path` | 入站请求耗时分布直方图（分桶: 0.05, 0.1, 0.25, 0.5, 1, 2.5） |
| `biz_transaction_processing_seconds` | Histogram | 秒 | `biz_type`, `result` | 核心业务事务执行耗时 |

---

## 3. Prometheus 告警规则清单 (Prometheus Alerting Rules)

```yaml
groups:
  - name: service_sla_alerts
    rules:
      - alert: HighHttpErrorRate
        expr: |
          sum(rate(http_server_requests_total{status=~"5.."}[2m]))
          /
          sum(rate(http_server_requests_total[2m])) * 100 > 1.0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "服务 HTTP 5xx 错误率突增超过 1%"
          description: "服务当前 5xx 错误率为 {{ $value }}%，持续超过 2 分钟，请立即排查。"

      - alert: ApiLatencyP99Breach
        expr: |
          histogram_quantile(0.99, sum(rate(http_server_request_duration_seconds_bucket[5m])) by (le)) > 0.3
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "API 接口 P99 响应延迟超标"
          description: "核心接口 P99 延迟达到 {{ $value }}s，超过 300ms 阈值。"
```

---

## 4. 结构化日志输出规范 (Structured Logging)

### 4.1 核心字段契约
- `trace_id`：全局分布式跟踪标识；
- `user_id`：脱敏后的调用方唯一标识；
- `action`：当前业务动作代号（如 `CREATE_ORDER`、`PAYMENT_CALLBACK`）；
- `status`：执行结果状态（`SUCCESS`、`FAILED`、`PENDING`）；
- `error_code`：失败时的标准化错误代码。

---

## 5. Kubernetes 健康探针配置 (Health Probes)

```yaml
livenessProbe:
  httpGet:
    path: /actuator/health/liveness
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 10
  timeoutSeconds: 2
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /actuator/health/readiness
    port: 8080
  initialDelaySeconds: 20
  periodSeconds: 5
  timeoutSeconds: 2
  failureThreshold: 2
```
