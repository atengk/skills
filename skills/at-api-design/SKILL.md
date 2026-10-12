---
name: at-api-design
description: 当用户需要设计现代 RESTful 接口、拟定 OpenAPI 3.1 接口契约、制定 API-First 规范、定义 RFC 7807 错误码模型、规划接口分页与防重幂等机制或演进版本策略时使用此技能。提供机器可解析的契约骨架与工程设计指南，交付工业级 API 接口契约规范。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - api-design
    - openapi
    - restful
    - contract-first
    - interface-spec
  icon: network-wired
---

# 现代 API 契约设计与演进编排器 (API Design Orchestrator)

将业务需求与领域模型转化为符合工业级标准、严密健壮的 API 接口契约。作为轻量化状态机运行，贯穿 API-First 设计哲学，从 RESTful 资源拓扑、OpenAPI 3.1 规格声明、RFC 7807 结构化错误模型到分布式幂等与平滑演进机制，提供机器可解析、前后端可独立并行研发的契约基石。

## 渐进式知识地图 (Progressive Disclosure Map)

所有 API 设计规范、交付模板与实战案例均存放于对应目录：
- **API 设计与演进标准**：[api-design-standards.md](references/protocols/api-design-standards.md)（RESTful 语义规范、RFC 7807 错误码模型、分页游标机制、分布式幂等与兼容性演进）
- **接口契约规格模板**：[api-contract-template.md](references/templates/api-contract-template.md)（元数据头、OpenAPI 3.1 结构骨架、字段校验规则与错误码映射模板）
- **支付交易契约实战案例**：[sample-api-contract.md](examples/sample-api-contract.md)（金融级支付结算中心交易与退款接口设计真实范例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：业务场景接入与领域资源建模 (Domain & Resource Modeling)

1. **业务意图解析与实体边界标定**：
   - 提取接口核心服务对象、交互上下游系统及关键业务流转状态机；
   - 将业务实体映射为标准化 RESTful 资源拓扑（小写复数名词、层级嵌套关系）；
   - 划分只读查询与有状态变更动作，落实读写分离（CQRS）视角；
   - 区分公共开放接口与内部微服务 RPC 接口，划定租户隔离与权限边界。
2. **存量接口与网关基线探查**：
   - 扫描现有代码库的路由前缀、公共返回体封装格式及全局异常拦截器；
   - 探查存量 Controller 的注解风格、DTO 命名约定与路径前缀规则；
   - 识别系统已有的认证凭据传递机制（如 Bearer Token、网关透传头），确保契约风格全局一致；
   - 严格遵循深模块原则，对外暴露极简且内聚的公共交互契约。

### 阶段 2：契约参数规约与容错防御推演 (Contract Specification & Guardrails)

依据 [api-design-standards.md](references/protocols/api-design-standards.md) 展开正交契约设计：
1. **HTTP 动词与状态码矩阵映射**：严格绑定语义化动词（GET/POST/PUT/PATCH/DELETE）与匹配状态码，严禁无脑返回 200；
2. **入参校验与返回体模型定义**：
   - 显式声明字段类型、最大最小边界、正则表达式校验规则及枚举集合；
   - 区分必填项与可选项，返回列表统一提供分页与数量元数据；
   - 针对大文件上传或导出场景，规范分片传输与预签名下载机制；
3. **RFC 7807 统一错误响应建模**：定义分域业务错误码（`code`）、人类可读原因（`title`/`detail`）与字段级校验失败明细；
4. **分布式幂等与并发控制**：对关键资金或状态变更接口引入 `Idempotency-Key` 机制与乐观锁版本控制；
5. **安全脱敏与隐私保护**：对响应报文中的手机号、身份证、密钥等敏感信息统一制定掩码规则；
6. **版本策略与向后兼容考量**：URL 显式标注主版本号（如 `/api/v1/`），严禁破坏性变更现有字段语义。

### 阶段 3：人机评审闸门与契约文档落盘 (Review Gate & Contract Persistence)

依据 [api-contract-template.md](references/templates/api-contract-template.md) 生成标准化契约：
1. **契约草案呈现与确认**：
   - 在会话中展示核心接口清单、参数明细与 OpenAPI 3.1 YAML 片段；
   - **强制停止工具调用**：向用户展示 API 核心契约与样例，提供直达链接，等待用户审阅与参数微调；
   - 开展兼容性静态比对，确认未破坏存量既有调用方的字段依赖；
   - 若用户指出字段缺失或命名分歧，就地修订并重申领域一致性；
   - 确保正文严格遵循盘古之白排版规范，全文档杜绝任何 `file:///` 或本地物理盘符泄漏。
2. **标准化资产落盘**：默认落盘为 `api-contract.md`（或 `openapi.yaml`）。

### 阶段 4：研发工具链打通与下游移交 (Toolchain Integration & Handoff)

1. **打通前后端并行研发**：
   - 产出的 OpenAPI 3.1 契约可直接输入 Mock 服务引擎（如 Prism / Apipost），先于后端实现启动前端对接；
   - 支持一键导出并驱动 Swagger UI / ReDoc 交互式文档预览；
   - 自动生成契约变更日志（Changelog），同步至组织 API 注册中心；
   - 为后续自动化契约测试提供确定性输入基准；
2. **平滑移交下游工程链路**：
   - 引导唤起 `at-spec` 将接口契约固化为全栈规格与验收标准（Given-When-Then）；
   - 驱动后续 `at-tdd` 编写针对 Controller 层的端到端或集成测试用例；
   - 杜绝随意破坏向后兼容性，守护长期演进生命线；
   - 闭环 API-First 软件工程生命周期，筑牢分布式协同基石。
