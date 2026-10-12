---
name: at-security
description: 当用户需要排查代码安全漏洞、审查 OWASP Top 10 威胁、防御 SQL/NoSQL 注入与 XSS、拦截越权访问 (IDOR)、治理硬编码明文机密或实施防御式编程加固时使用此技能。提供威胁建模扫描、参数化防注入改造、权限租户隔离与依赖供应链合规编排，交付零明文、高韧性且纵深防御的安全代码。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - security
    - owasp-top-10
    - defensive-programming
    - zero-secret
    - vulnerability-scan
  icon: shield-alert
---

# 全栈安全审查与威胁加固编排器 (Security & Hardening Orchestrator)

在全栈软件开发与代码审查中贯彻纵深防御（Defense-in-Depth）理念。作为轻量化状态机运行，针对 OWASP Top 10 经典漏洞威胁、SQL 注入、跨站脚本（XSS）、失效的访问控制（水平/垂直越权 IDOR）与明文密钥泄漏风险，提供全方位的输入净化、参数化查询改造、零信任鉴权加固与密钥环境变量收口编排，构筑坚不可摧的工业级应用安全防线。

## 渐进式知识地图 (Progressive Disclosure Map)

所有安全核对单、防御式协议与加固实操案例均存放于对应目录：
- **OWASP 全栈安全检查核对单**：[owasp-security-checklist.md](references/checklists/owasp-security-checklist.md)（注入防御、越权拦截、密码慢哈希、安全标头与供应链扫描）
- **防御式编程与零机密协议**：[defensive-programming-protocol.md](references/protocols/defensive-programming-protocol.md)（输入白名单净化、零明文不变量、最小特权与异常信息安全）
- **安全加固实操前后比对案例**：[sample-security-hardening.md](examples/sample-security-hardening.md)（参数化防注入、UUID 模式校验、租户强隔离与错误码抽象案例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：威胁建模与漏洞异味扫描 (Threat Modeling & Vulnerability Scan)

1. **攻击面探查与数据流追踪**：
   - 绘制数据从外部接入层（HTTP/RPC/MQ）流向持久层的完整拓扑；
   - 对照 [owasp-security-checklist.md](references/checklists/owasp-security-checklist.md) 审查代码中的高危敏感调用点；
   - 排查拼接 SQL、命令执行函数、未净化的富文本渲染及未鉴权接口；
   - 梳理服务对外暴露的网络边界、CORS 配置与跨域安全范围；
   - 扫描源码、配置文件与单测桩中是否存在疑似明文硬编码密钥。
2. **供应链与依赖漏洞审计**：
   - 执行依赖合规检查（如 `npm audit` 或 `pip-audit`），识别已知 CVE 漏洞；
   - 评估漏洞利用难度与真实危害半径，确定加固修复靶心优先级。

### 阶段 2：注入与越权防御深度加固 (Injection & IDOR Hardening)

1. **参数化预编译与白名单映射**：
   - 将所有动态拼接的 SQL/NoSQL 语句重构为预编译参数化占位符；
   - 对动态排序列或表名强制实施白名单映射枚举校验，拒绝透传用户入参；
   - 前端动态渲染区域引入 DOMPurify 白名单净化，阻断反射型/存储型 XSS；
   - 补齐安全响应头配置（CSP、X-Frame-Options、HSTS），筑牢接入层防线。
2. **租户归属与访问控制强绑定**：
   - 审查所有按标识符查询与变更资源的端点，识别水平越权（IDOR）风险；
   - 在持久层查询条件中强制硬绑定当前上下文中的 `tenant_id` 或 `user_id`；
   - 管理端路由补齐严格的角色权限（RBAC）拦截卫语句。

### 阶段 3：零明文机密与最小特权规约落地 (Zero-Secret & Principle of Least Privilege)

1. **机密收敛与环境变量外置**：
   - 遵循 [defensive-programming-protocol.md](references/protocols/defensive-programming-protocol.md)；
   - 彻底剥离源码与配置中的明文口令与私钥，转为标准环境变量或 KMS 动态注入；
   - 配置文件模板采用大写语义占位符（如 `YOUR_API_TOKEN`）；
   - 检查数据库连接账号权限，确保收敛至业务库读写最小特权。
2. **异常安全与敏感日志脱敏**：
   - 生产环境统一屏蔽底层数据库报错细节与物理调用栈，对外暴露标准业务错误码；
   - 在日志切片层配置脱敏过滤器，强制遮罩手机号、身份证与令牌凭据；
   - 落实安全失败默认准则（Fail-Safe Defaults），鉴权异常一律默认拒绝访问。


### 阶段 4：安全基线回归与交付留置 (Security Regression & Safe Delivery)

1. **安全自动化测试用例构建**：
   - 编写针对加固点的对抗性单测（注入探测入参、越权跨租户访问断言拦截）；
   - 确认全量单元测试与集成测试 100% 绿灯无回退；
2. **最小 Diff 审计与安全就绪交付**：
   - 审计 Git Diff，确保防御加固改动最小化，无多余格式化扰动；
   - 向用户呈现加固前后安全对比报告与剩余风险排查建议；
   - 所有改动保留在工作区等待人类审查，未获显式指令绝不擅自提交；
   - 阻断恶意渗透与数据泄露的致命合规与声誉风险；
   - 筑牢从应用接入层到底层存储的纵深纵向防御链条；
   - 让安全与合规内建于每一次日常研发与代码审查流中。
