# 现代 API 契约设计与演进工程标准 (API Design & Evolution Standards)

本文档规范了 `at-api-design` 技能在系统接口契约制定、API-First 研发流程、语义化响应模型、幂等与容错防御方面的核心执行标准。

---

## 目录 (Table of Contents)
- [1. 核心哲学：API-First 与契约即代码](#1-核心哲学api-first-与契约即代码)
- [2. RESTful 资源语义与 HTTP 状态码规范](#2-restful-资源语义与-http-状态码规范)
- [3. RFC 7807 统一错误响应与业务错误码模型](#3-rfc-7807-统一错误响应与业务错误码模型)
- [4. 分页、过滤与大批量数据检索规约](#4-分页过滤与大批量数据检索规约)
- [5. 分布式幂等性与防重提交设计](#5-分布式幂等性与防重提交设计)
- [6. 向后兼容与多版本演进契约](#6-向后兼容与多版本演进契约)

---

## 1. 核心哲学：API-First 与契约即代码

API 是系统间最核心的边界与信任契约。在编码前必须先敲定精确的接口契约（API-First）：
- **契约先于实现**：禁止未出契约先写 Controller，契约是前后端与跨服务联调的唯一法律基准；
- **机器可解析性**：标准契约统一采用 OpenAPI 3.1（YAML/JSON）或强类型 Protocol Buffers / Markdown，便于 Mock 服务自动生成与自动化契约测试；
- **防腐与领域隔离**：API 传输模型（DTO/Request/Response）严禁直接混入内部数据库持久层模型（DO/Entity）。

---

## 2. RESTful 资源语义与 HTTP 状态码规范

### 2.1 资源路径命名准则
- **名词复数为主**：路径使用小写复数名词（如 `/api/v1/orders`、`/api/v1/orders/{orderId}/items`）；
- **层级表达归属**：子资源反映层级关系，最大嵌套深度建议不超过 2 层；
- **Kebab-Case 命名**：多词路径段统一使用短横线隔开（如 `/api/v1/payment-records`），严禁驼峰或下划线混用；
- **动词动作例外 (Controller Actions)**：当操作不符合 CRUD（如支付扣款、激活、退款）时，使用明确动作动词（如 `/api/v1/orders/{orderId}/pay`、`/api/v1/accounts/{accountId}/activate`）。

### 2.2 HTTP 方法与状态码对应矩阵
| 操作意图 | HTTP 方法 | 幂等性 | 成功状态码 | 典型失败状态码 |
| :--- | :--- | :--- | :--- | :--- |
| **获取资源/列表** | `GET` | 是 | `200 OK` | `404 Not Found` |
| **创建新资源** | `POST` | 否 | `201 Created`（带 Location 头） | `400 Bad Request`, `409 Conflict` |
| **全量替换资源** | `PUT` | 是 | `200 OK` 或 `204 No Content` | `400 Bad Request`, `404 Not Found` |
| **局部增量更新** | `PATCH` | 否/视实现 | `200 OK` | `400 Bad Request`, `404 Not Found` |
| **删除指定资源** | `DELETE` | 是 | `204 No Content` 或 `200 OK` | `404 Not Found` |

---

## 3. RFC 7807 统一错误响应与业务错误码模型

为彻底杜绝各接口自由发挥的杂乱报错格式，遵循现代 RFC 7807 Problem Details 规范：

```json
{
  "type": "https://api.example.com/errors/insufficient-balance",
  "title": "账户余额不足",
  "status": 400,
  "detail": "当前账户可用余额为 25.00 元，无法完成金额为 100.00 元的订单支付扣款。",
  "instance": "/api/v1/orders/ord_998822/pay",
  "code": "PAY_INSUFFICIENT_FUNDS",
  "timestamp": "2026-03-20T10:15:30Z",
  "invalidParams": [
    {
      "name": "amount",
      "reason": "扣款金额超出可用授信额度"
    }
  ]
}
```

- **HTTP 状态码优先**：严禁无脑返回 `200 OK` 并在 JSON 内包裹 `{ code: 500, error: "..." }` 的反模式；
- **业务错误码分域**：业务错误码采用 `[DOMAIN]_[ACTION]_[REASON]` 命名（如 `ORDER_CREATE_OUT_OF_STOCK`）。

---

## 4. 分页、过滤与大批量数据检索规约

### 4.1 分页参数与返回模型
- **基于偏移量分页 (Offset-based)**：适用于管理后台（`page=1&pageSize=20`）；
- **基于游标分页 (Cursor-based)**：适用于高并发无限流信息列表（`cursor=eyJuZXh0IjoxMDB9&limit=20`），避免深度分页性能崩塌。

### 4.2 统一响应报文包裹
```json
{
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalCount": 142,
    "totalPages": 8,
    "hasNext": true
  }
}
```

---

## 5. 分布式幂等性与防重提交设计

对于支付、下单、库存扣减等变动资金或核心状态的写接口，必须具备分布式幂等保障：
1. **幂等键头 (Idempotency-Key Header)**：客户端在 POST 请求头中携带 UUID 或业务唯一标识符：
   ```http
   Idempotency-Key: 7b841a54-469b-4e12-8e6d-6725227d8e0f
   ```
2. **幂等处理生命周期**：
   - 服务端通过 Redis 分布式锁缓存该 Key 状态（`PROCESSING`）；
   - 执行业务并落盘持久化，将响应报文快照以该 Key 缓存（有效期通常 24 小时）；
   - 若重复收到相同的 `Idempotency-Key`，直接返回原缓存的响应快照，避免重复扣款或重复下单。

---

## 6. 向后兼容与多版本演进契约

- **版本标注**：统一在 URL 路径体现大版本号（如 `/api/v1/`、`/api/v2/`）；
- **向后兼容原则**：
  - 允许向响应体中新增可选字段；
  - 严禁删除、重命名既有请求参数或修改已有字段的数据类型；
  - 严禁将可选请求参数变更为必填参数；
- **平滑废弃策略**：废弃接口通过 HTTP Header `Deprecation: true` 与 `Sunset: 2026-12-31` 提醒调用方，给予至少 6 个月迁移过渡期。
