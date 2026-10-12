# API 接口契约规范模板 (API Contract Specification Template)

本文档提供符合 OpenAPI 3.1 标准与企业级交付规范的 API 接口契约模板。

---

## 目录 (Table of Contents)
- [1. 契约元数据与服务网关信息](#1-契约元数据与服务网关信息)
- [2. OpenAPI 3.1 规格声明模板](#2-openapi-31-规格声明模板)
- [3. 详细接口交互契约列表](#3-详细接口交互契约列表)
- [4. 统一业务错误码与异常映射](#4-统一业务错误码与异常映射)
- [5. 认证鉴权与安全防护规约](#5-认证鉴权与安全防护规约)

---

## 1. 契约元数据与服务网关信息

```markdown
# [服务/模块名称] API 接口契约规范

- **契约版本**：v1.0.0
- **所属微服务**：[service-name]
- **网关根路径**：`/api/v1/[module-path]`
- **认证方式**：OAuth2 Bearer JWT / API Key
- **维护责任人**：[架构师 / 模块负责人]
- **最后更新时间**：[YYYY-MM-DD]
```

---

## 2. OpenAPI 3.1 规格声明模板

```yaml
openapi: 3.1.0
info:
  title: "[服务名称] 核心 API"
  version: "1.0.0"
  description: "提供标准化业务操作契约"
paths:
  /api/v1/resources:
    post:
      summary: "创建核心资源"
      operationId: "createResource"
      parameters:
        - name: "Idempotency-Key"
          in: "header"
          required: false
          schema:
            type: "string"
            format: "uuid"
          description: "分布式防重幂等键"
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateResourceRequest"
      responses:
        "201":
          description: "创建成功"
          headers:
            Location:
              schema:
                type: "string"
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ResourceResponse"
        "400":
          $ref: "#/components/responses/400BadRequest"
        "409":
          description: "资源冲突或重复提交"

components:
  schemas:
    CreateResourceRequest:
      type: "object"
      required:
        - name
        - category
      properties:
        name:
          type: "string"
          minLength: 2
          maxLength: 64
          example: "高可用计算集群"
        category:
          type: "string"
          enum: ["COMPUTE", "STORAGE", "NETWORK"]
    ResourceResponse:
      type: "object"
      required:
        - id
        - name
        - createdAt
      properties:
        id:
          type: "string"
          example: "res_98234112"
        name:
          type: "string"
        status:
          type: "string"
          example: "ACTIVE"
        createdAt:
          type: "string"
          format: "date-time"
```

---

## 3. 详细接口交互契约列表

### 接口 1：[接口中文名称]
- **请求方法与路径**：`POST /api/v1/resources`
- **功能描述**：用于提交新建资源，自动触发下游事件与配额检查。
- **请求头 (Headers)**：
  - `Content-Type`: `application/json`
  - `Authorization`: `Bearer <token>`
  - `Idempotency-Key`: `[可选/必填 UUID]`

#### 请求参数 (Request Body)
| 字段名 | 类型 | 必填 | 校验规则 | 语义说明 | 示例值 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `name` | string | 是 | 长度 2~64 字符 | 资源显示名称 | `"大数据集群-01"` |
| `category` | string | 是 | 枚举值限定 | 所属分类 | `"COMPUTE"` |
| `tags` | array[string]| 否 | 最多 10 项 | 业务标签 | `["prod", "core"]` |

#### 响应结构 (Response Body - 201 Created)
```json
{
  "id": "res_887711",
  "name": "大数据集群-01",
  "category": "COMPUTE",
  "status": "INITIALIZING",
  "createdAt": "2026-03-20T10:00:00Z"
}
```

---

## 4. 统一业务错误码与异常映射

| HTTP 状态码 | 业务错误代码 (code) | 场景说明与建议处置 |
| :--- | :--- | :--- |
| `400` | `INVALID_ARGUMENT` | 请求参数校验不通过，排查入参必填项或边界 |
| `401` | `UNAUTHENTICATED` | 凭据缺失或 Token 过期，需重新登录换发 |
| `403` | `PERMISSION_DENIED` | 权限不足，当前租户无操作该资源权限 |
| `404` | `RESOURCE_NOT_FOUND` | 指定 ID 的目标资源不存在或已被删除 |
| `409` | `RESOURCE_CONFLICT` | 同名资源已存在或唯一索引冲突 |
| `429` | `RATE_LIMIT_EXCEEDED` | 触发接口限流熔断，请降频重试 |

---

## 5. 认证鉴权与安全防护规约

1. **统一鉴权**：接口由网关校验 JWT 签名并将解析后的 `X-User-Id` 与 `X-Tenant-Id` 注入下游请求头；
2. **防重放攻击**：高敏感写接口必须校验时间戳（请求时效窗口 ±5 分钟）；
3. **敏感信息脱敏**：响应报文中涉及个人隐私（手机号、证件号）必须实施掩码。
