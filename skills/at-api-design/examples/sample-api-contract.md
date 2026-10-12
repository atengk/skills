# 支付结算中心交易 API 契约范例 (Sample Payment API Contract)

本文档展示了一个高可靠金融级支付结算服务针对“创建支付交易”与“发起申请退款”的标准化 API 契约落地范例。

---

## 目录 (Table of Contents)
- [1. 契约元数据与服务网关](#1-契约元数据与服务网关)
- [2. OpenAPI 3.1 规格片段](#2-openapi-31-规格片段)
- [3. 核心接口规格详情](#3-核心接口规格详情)
- [4. 业务错误码与异常响应样例](#4-业务错误码与异常响应样例)
- [5. 幂等控制与回调通知机制](#5-幂等控制与回调通知机制)

---

## 1. 契约元数据与服务网关

- **服务名称**：支付结算交易中心 (Payment Core Service)
- **契约版本**：v1.1.0
- **网关根路径**：`/api/v1/payments`
- **安全认证**：API Key (Header: `X-Merchant-Key`) + SHA256 HMAC 验签
- **最后更新时间**：2026-03-20

---

## 2. OpenAPI 3.1 规格片段

```yaml
openapi: 3.1.0
info:
  title: "支付结算中心 API"
  version: "1.1.0"
paths:
  /api/v1/payments/charges:
    post:
      summary: "创建支付交易扣款"
      operationId: "createCharge"
      parameters:
        - name: "Idempotency-Key"
          in: "header"
          required: true
          schema:
            type: "string"
            format: "uuid"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateChargeRequest"
      responses:
        "201":
          description: "扣款交易已受理"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ChargeResponse"
        "400":
          $ref: "#/components/responses/ProblemDetails"
        "409":
          description: "交易正在处理或存在重复请求"
```

---

## 3. 核心接口规格详情

### 接口：创建支付交易扣款 (Create Charge)
- **请求方式与路径**：`POST /api/v1/payments/charges`
- **语义说明**：商户系统发起一笔资金扣款请求。接口强制要求分布式幂等键。

#### 请求头 (Headers)
| 请求头键名 | 必填 | 格式与说明 |
| :--- | :--- | :--- |
| `Content-Type` | 是 | `application/json` |
| `Idempotency-Key`| 是 | UUID 格式，唯一标识单次支付意图 |
| `X-Merchant-Key` | 是 | 商户公钥认证标识符 |

#### 请求体参数 (Request Body)
| 参数名 | 类型 | 必填 | 校验规则 | 业务描述 | 示例值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `outTradeNo` | string | 是 | 6~32 字符，字母数字 | 商户端外部订单号 | `"ORD_20260320_001"` |
| `amount` | integer | 是 | 最小值 1（单位：分） | 支付总金额（分） | `9900` |
| `currency` | string | 是 | ISO 4217 格式 | 货币符号 | `"CNY"` |
| `channel` | string | 是 | 枚举 `WECHAT`, `ALIPAY`| 支付渠道 | `"WECHAT"` |
| `subject` | string | 是 | 最长 128 字符 | 订单商品标题描述 | `"企业级云服务年费"` |
| `notifyUrl` | string | 是 | 标准 HTTPS URL | 支付成功异步回调地址 | `"https://merchant.com/pay/notify"` |

#### 响应体 (Response Body - 201 Created)
```json
{
  "chargeId": "chg_9988112233",
  "outTradeNo": "ORD_20260320_001",
  "amount": 9900,
  "currency": "CNY",
  "status": "PENDING",
  "payUrl": "weixin://wxpay/bizpayurl?pr=xyz12345",
  "expiresAt": "2026-03-20T10:30:00Z",
  "createdAt": "2026-03-20T10:00:00Z"
}
```

---

## 4. 业务错误码与异常响应样例

遵循 RFC 7807 规范，当扣款金额超过限额时：

```json
{
  "type": "https://api.pay.com/errors/charge-limit-exceeded",
  "title": "单笔交易金额超限",
  "status": 400,
  "detail": "当前商户单笔微信交易最高限额为 50000 分，当前请求金额 99000 分超出限制。",
  "instance": "/api/v1/payments/charges",
  "code": "PAY_CHANNEL_AMOUNT_LIMIT",
  "timestamp": "2026-03-20T10:00:02Z"
}
```

| HTTP 状态码 | 业务错误代码 (code) | 场景说明 |
| :--- | :--- | :--- |
| `400` | `PAY_AMOUNT_INVALID` | 交易金额必须大于 0 |
| `400` | `PAY_CHANNEL_UNSUPPORTED`| 暂不支持该商户开通指定的结算渠道 |
| `409` | `PAY_ORDER_ALREADY_EXISTS`| 商户外部订单号已被使用且金额不匹配 |
| `422` | `PAY_ACCOUNT_RESTRICTED` | 目标商户账户处于风控冻结状态 |

---

## 5. 幂等控制与回调通知机制

1. **强一致防重入**：
   - 收到相同 `Idempotency-Key` 且参数完全一致的请求时，直接返回先前的响应快照（HTTP 201）；
   - 若参数不同但 `Idempotency-Key` 重复，直接返回 `409 Conflict`；
2. **异步回调验签**：
   - 支付成功后系统发起 15 次指数退避阶梯重试回调；
   - 回调请求附带 `X-Signature` 头部，供商户进行公钥解密验签。
