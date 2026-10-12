# OWASP Top 10 全栈安全审查核对单与防御指南 (OWASP Security Checklist)

本核对单结合 OWASP Top 10 漏洞模型与工业级安全基准，提供在开发、审查与上线前全栈代码安全自检清单及标准化防御对策。

---

## 目录 (Table of Contents)

- [1. 注入攻击防御 (Injection)](#1-注入攻击防御-injection)
- [2. 失效的身份认证与会话管理 (Broken Authentication)](#2-失效的身份认证与会话管理-broken-authentication)
- [3. 敏感数据暴露与凭据卫生 (Cryptographic Failures)](#3-敏感数据暴露与凭据卫生-cryptographic-failures)
- [4. 失效的访问控制与越权漏洞 (Broken Access Control)](#4-失效的访问控制与越权漏洞-broken-access-control)
- [5. 安全配置错误与外部注入 (Security Misconfiguration & SSRF)](#5-安全配置错误与外部注入-security-misconfiguration--ssrf)
- [6. 跨站脚本与脆弱依赖组件 (XSS & Vulnerable Components)](#6-跨站脚本与脆弱依赖组件-xss--vulnerable-components)

---

## 1. 注入攻击防御 (Injection)

- [ ] **SQL/NoSQL 参数化查询**：严禁采用字符串拼接方式拼装 SQL/NoSQL 语句；强制使用预编译参数化占位符（如 MyBatis `#{}`、JPA 参数化绑定、ORM 参数绑定）；
- [ ] **ORM 动态排序防御**：对于 `ORDER BY` 等无法使用参数化的动态字段，强制实施白名单映射校验，拒绝直接透传客户端入参；
- [ ] **命令注入防范**：杜绝向 `exec`、`eval`、`Runtime.getRuntime().exec` 传递未经验证的外部参数；参数必须作为独立数组/列表传递，杜绝 Shell 解释器执行；
- [ ] **XML/JSON 实体注入 (XXE)**：解析外部 XML 时显式禁用外部实体（`DOCTYPE` 与外部 DTD）。

---

## 2. 失效的身份认证与会话管理 (Broken Authentication)

- [ ] **强密码策略与哈希存储**：用户凭据必须使用经过加盐慢哈希算法（如 Argon2id、BCrypt，Work Factor ≥ 12）存储，严禁使用 MD5 或 SHA-256 明文哈希；
- [ ] **安全会话与 Token 机制**：Session ID 或 JWT 具备合理的生存期与刷新机制；退出登录时服务端支持黑名单作废；
- [ ] **接口防爆破与频控**：登录、短信验证码、找回密码等关键鉴权接口，配置基于 IP 与账号维度的分布式滑动窗口限流防爆破；
- [ ] **Cookie 安全标记**：鉴权 Cookie 必须开启 `HttpOnly`、`Secure` 并配置 `SameSite=Lax` 或 `Strict`。

---

## 3. 敏感数据暴露与凭据卫生 (Cryptographic Failures)

- [ ] **零明文机密不变量**：源码、配置文件、测试代码与 Git 提交中杜绝任何真实 API Key、Token 或数据库密码；
- [ ] **日志脱敏防范**：日志打印切片拦截器必须对用户手机号、身份证号、银行卡号及密钥自动打码（如 `138****0000`）；
- [ ] **强加密传输**：所有外部与内部通信强制启用 TLS 1.3/1.2；禁用过期的废弃密码套件；
- [ ] **安全随机数生成**：涉及 Token、盐值、验证码生成时，强制使用加密学安全随机数（如 `crypto.randomBytes`、`SecureRandom`）。

---

## 4. 失效的访问控制与越权漏洞 (Broken Access Control)

- [ ] **水平越权拦截 (IDOR 防御)**：查询或变更资源时（如 `/api/orders/{id}`），必须强制校验当前用户或租户与该资源的物理归属权（`WHERE id = ? AND tenant_id = ?`）；
- [ ] **垂直越权防御**：管理端接口（如 `/api/admin/*`）必须具备严格的基于角色的访问控制（RBAC），接入层卫语句拦截未授权访问；
- [ ] **默认拒绝原则 (Deny by Default)**：所有受保护路由默认拒绝访问，仅对经过白名单鉴权的用户开放；
- [ ] **CORS 跨域安全配置**：严禁在携带凭据（`credentials: true`）的响应中配置通配符 `Access-Control-Allow-Origin: *`。

---

## 5. 安全配置错误与外部注入 (Security Misconfiguration & SSRF)

- [ ] **生产环境屏蔽详细堆栈**：生产环境全局异常处理器严禁向客户端抛出数据库报错细节、系统绝对路径或异常调用栈；
- [ ] **服务端请求伪造防范 (SSRF)**：后端代理请求外部 URL 时，必须校验目标协议（仅限 http/https），严禁请求内网私有网段（`127.0.0.1`、`10.0.0.0/8`、`192.168.0.0/16`、云厂商元数据地址 `169.254.169.254`）；
- [ ] **安全响应头配置**：生产响应头配置 `X-Content-Type-Options: nosniff`、`X-Frame-Options: DENY` 以及内容安全策略（CSP）。

---

## 6. 跨站脚本与脆弱依赖组件 (XSS & Vulnerable Components)

- [ ] **存储型/反射型 XSS 净化**：在前端渲染不可信用户输入时，避免使用 `dangerouslySetInnerHTML` 或 `v-html`；若必须富文本渲染，强制使用 DOMPurify 白名单净化；
- [ ] **第三方依赖供应链漏洞扫描**：定期运行 `npm audit`、`mvn dependency-check` 或 `pip-audit`，清除已知 CVE 高危漏洞组件；
- [ ] **严格依赖版本锁定**：使用 `package-lock.json`、`pnpm-lock.yaml` 或 `poetry.lock` 锁定依赖版本，防止依赖包恶意投毒。
