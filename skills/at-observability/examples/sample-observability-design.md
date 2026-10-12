# 支付链路可观测性设计实战样例 (Sample Observability Design: Payment Flow)

本案例呈现高并发在线支付网关服务在生产环境下的完整可观测性设计方案，涵盖 Prometheus 指标埋点、OpenTelemetry 链路透传、结构化支付审计日志与告警规则。

---

## 1. 业务场景与指标矩阵

在支付交易系统中，核心关注点为订单扣款成功率、外部银行通道耗时分布与资金对账闭环。

### 1.1 RED 核心指标定义

| 指标全名 | 类型 | 标签列表 | 说明 |
| :--- | :--- | :--- | :--- |
| `payment_transactions_total` | Counter | `channel`, `status`, `currency` | 支付交易请求计数器 |
| `payment_gateway_duration_seconds` | Histogram | `channel`, `operation` | 第三方支付网关外部 RPC 耗时分布 |
| `payment_amount_cents_total` | Counter | `channel`, `status` | 成功交易流水金额计数器（分） |

---

## 2. 核心埋点代码实现 (TypeScript / Node.js)

```typescript
// src/metrics/payment.metrics.ts
import { Counter, Histogram } from 'prom-client';

export const paymentTransactionsCounter = new Counter({
  name: 'payment_transactions_total',
  help: 'Total number of payment transactions processed',
  labelNames: ['channel', 'status', 'currency'],
});

export const paymentGatewayLatencyHistogram = new Histogram({
  name: 'payment_gateway_duration_seconds',
  help: 'Duration of external payment gateway calls in seconds',
  labelNames: ['channel', 'operation'],
  buckets: [0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
});
```

```typescript
// src/services/payment.service.ts
import { paymentTransactionsCounter, paymentGatewayLatencyHistogram } from '../metrics/payment.metrics';
import { logger } from '../utils/logger';

export class PaymentService {
  async processPayment(orderId: string, amountCents: number, channel: string, traceId: string) {
    const timer = paymentGatewayLatencyHistogram.startTimer({ channel, operation: 'charge' });

    try {
      // 1. 调用外部网关并计时
      const result = await this.invokeThirdPartyGateway(orderId, amountCents, channel);
      timer();

      // 2. 上报成功指标
      paymentTransactionsCounter.inc({ channel, status: 'SUCCESS', currency: 'CNY' });

      // 3. 输出结构化审计日志
      logger.info({
        message: '支付交易处理成功',
        trace_id: traceId,
        order_id: orderId,
        amount_cents: amountCents,
        channel,
        status: 'SUCCESS',
      });

      return result;
    } catch (error: any) {
      timer();
      paymentTransactionsCounter.inc({ channel, status: 'FAILED', currency: 'CNY' });

      logger.error({
        message: '支付交易处理失败',
        trace_id: traceId,
        order_id: orderId,
        channel,
        error_code: error.code || 'UNKNOWN_ERROR',
        error_message: error.message,
      });

      throw error;
    }
  }

  private async invokeThirdPartyGateway(orderId: string, amount: number, channel: string) {
    // 模拟网络请求
    return { transactionId: `TX_${Date.now()}` };
  }
}
```

---

## 3. Prometheus 告警规则配置 (Alerting Rule)

```yaml
groups:
  - name: payment_gateway_alerts
    rules:
      - alert: PaymentFailureRateHigh
        expr: |
          sum(rate(payment_transactions_total{status="FAILED"}[3m]))
          /
          sum(rate(payment_transactions_total[3m])) * 100 > 2.0
        for: 1m
        labels:
          severity: disaster
        annotations:
          summary: "支付失败率超过 2% 熔断红线"
          description: "当前支付通道失败率已达 {{ $value }}%，请立即检查支付网关连通性。"
```

---

## 4. 结构化日志输出样例

```json
{
  "timestamp": "2026-10-12T21:11:00.412+08:00",
  "level": "INFO",
  "service": "payment-gateway",
  "trace_id": "8f3b790d98414ad7a35cb998811e5443",
  "order_id": "ORD_20261012_8912",
  "amount_cents": 29900,
  "channel": "WXPAY",
  "status": "SUCCESS",
  "message": "支付交易处理成功"
}
```
