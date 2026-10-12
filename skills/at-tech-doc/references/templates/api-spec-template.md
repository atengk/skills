# [服务/业务域名称] API 接口契约规范

| 属性 | 详情 |
| :--- | :--- |
| **文档类型** | API 接口契约规范 (API Specification) |
| **基础网关地址** | `https://api.example.com/v1` |
| **协议标准** | HTTP/1.1 & HTTP/2, RESTful, JSON |
| **鉴权方式** | `Authorization: Bearer <JWT_TOKEN>` |
| **维护人** | Ateng |
| **创建日期** | YYYY-MM-DD |

---

## 目录 (Table of Contents)

- [1. 全局约定与通用规范](#1-全局约定与通用规范)
- [2. 核心接口明细清单](#2-核心接口明细清单)
- [3. 安全防护与频控规范](#3-安全防护与频控规范)
- [4. 权威参考资料与事实依据](#4-权威参考资料与事实依据)

---

## 1. 全局约定与通用规范

### 1.1 通用响应报文封装
```json
{
  "code": 200,
  "success": true,
  "message": "Operation successful",
  "data": {},
  "timestamp": 1726910000000,
  "traceId": "c0a80101-6f4a-4b92-9e6b-123456789abc"
}
```

### 1.2 全局业务错误码表
| 错误码 | HTTP 状态码 | 业务含义 | 排查处理建议 |
| :--- | :--- | :--- | :--- |
| `200` | 200 | 请求成功 | 正常处理 |
| `40001` | 400 | 请求参数格式错误/缺失 | 校验请求 Body 是否符合 schema |
| `40101` | 401 | 凭据失效或未登录 | 引导用户重新换取 Token |
| `40301` | 403 | 无此操作权限 | 检查用户角色权限 RBAC 配置 |
| `42901` | 429 | 请求频次触发限流 | 采用指数退避重试 |
| `50001` | 500 | 系统服务内部异常 | 根据 `traceId` 检索告警日志 |

---

## 2. 核心接口明细清单

### 2.1 [接口名称，例如：分页查询资源列表]
- **请求方法**：`GET`
- **接口路径**：`/resources`
- **接口描述**：查询并过滤资源列表，支持按创建时间倒序分页。

#### 查询请求参数
| 参数名 | 类型 | 必填 | 默认值 | 约束与说明 |
| :--- | :--- | :--- | :--- | :--- |
| `pageNum` | integer | 否 | `1` | 当前页码，必须 >= 1 |
| `pageSize` | integer | 否 | `20` | 每页大小，最大不超过 100 |
| `status` | string | 否 | `ALL` | 状态过滤：`PENDING`, `ACTIVE`, `DISABLED` |

#### 正常响应报文 (200 OK)
```json
{
  "code": 200,
  "success": true,
  "message": "OK",
  "data": {
    "list": [
      {
        "id": "1001",
        "name": "示例资源",
        "status": "ACTIVE",
        "createdAt": "2026-09-21T17:00:00Z"
      }
    ],
    "total": 1,
    "pageNum": 1,
    "pageSize": 20
  },
  "timestamp": 1726910000000,
  "traceId": "trace-uuid-demo"
}
```

---

### 2.2 [接口名称，例如：创建新资源]
- **请求方法**：`POST`
- **接口路径**：`/resources`
- **幂等要求**：请求头必须携带 `X-Idempotency-Key` 防重 Token。

#### 请求头参数
| Header Key | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `Authorization` | string | 是 | Bearer 鉴权 Token |
| `X-Idempotency-Key` | string | 是 | 唯一防重 UUID |

#### 请求体数据 (JSON)
```json
{
  "name": "新增资源示例",
  "type": "STANDARD",
  "config": {
    "retryLimit": 3,
    "timeoutMs": 5000
  }
}
```

| 字段路径 | 类型 | 必填 | 格式/取值限制 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `name` | string | 是 | 长度 2~50 字符 | 资源唯一可读名称 |
| `type` | string | 是 | 枚举值: `STANDARD`, `PREMIUM` | 规格类型 |
| `config.retryLimit` | integer | 否 | 1~5，默认 3 | 失败重试上限 |
| `config.timeoutMs` | integer | 否 | 100~30000 | 超时毫秒数 |

---

## 3. 安全防护与频控规范
- **防重与幂等机制**：网关层针对 POST/PUT 自动提取 `X-Idempotency-Key`，在 Redis 维持 30 秒分布式锁，重复请求直接返回上一次处理结果。
- **频控限流策略**：单 IP/单用户限制 `60 次/分钟`，超出返回 `429 Too Many Requests`。

---

## 4. 权威参考资料与事实依据

### 4.1 权威信源引用清单
- [[Tier 1]] [IETF RFC 9110 - HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110) - 规范 HTTP 状态码（200, 400, 401, 403, 404, 409, 429, 500）语义 (核验日期: YYYY-MM-DD)
- [[Tier 1]] [OpenAPI Specification 3.0.3 / 3.1.0](https://spec.openapis.org/oas/v3.1.0) - 核验接口契约字段类型与元数据格式 (核验日期: YYYY-MM-DD)
- [[Tier 1]] [第三方开放平台官方文档 (若涉及三方回调/对接)](https://...) - 核验外部系统签名算法、请求参数与回调报文规范 (核验日期: YYYY-MM-DD)

### 4.2 事实核验矩阵
| 核查对象 (协议/状态码/外部 API) | 官方基准事实 (Ground Truth) | 对应权威依据 (Tier 1 链接) | 核验状态 |
| :--- | :--- | :--- | :--- |
| **HTTP 429 限流状态码** | RFC 6585 标准状态码：Too Many Requests | [RFC 6585](https://...) | 已核实官方标准 |
| **幂等键标准 Header** | 遵循 IETF 草案 `Idempotency-Key` 规范语义 | [IETF Draft](https://...) | 已核实行业规范 |
| **三方对接接口定义** | 本地代码与官方最新对外开放 API 版本一致 | [官方开放平台](https://...) | 已核验契约一致 |

