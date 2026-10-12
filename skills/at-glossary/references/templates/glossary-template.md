# 统一语言术语字典模板 (Glossary Template)

本文档定义了 `at-glossary` 技能在项目根目录生成与维护的 `GLOSSARY.md` 标准文件结构。

---

## 目录 (Table of Contents)
- [1. 术语字典元数据头](#1-术语字典元数据头)
- [2. 核心子域概念 (Core Domain)](#2-核心子域概念-core-domain)
- [3. 通用子域概念 (Generic Domain)](#3-通用子域概念-generic-domain)
- [4. 支撑子域概念 (Supporting Domain)](#4-支撑子域概念-supporting-domain)
- [5. 废弃术语与消歧对照表](#5-废弃术语与消歧对照表)

---

## 1. 术语字典元数据头

```markdown
# 项目领域统一语言字典 (Ubiquitous Language Glossary)

> **项目名称**：{Project Name}
> **上下文边界**：{主系统 / 核心业务线}
> **维护规范**：遵循 DDD 统一语言标准，任何接口契约与代码实体命名以此为唯一基准。
> **最后更新**：{YYYY-MM-DD}
```

---

## 2. 核心子域概念 (Core Domain)

### 2.1 {核心领域实体 A} (`{CanonicalEntityA}`)
- **法定定义 (Definition)**：`{陈述概念核心业务属性}`；
- **核心约束 (Invariants)**：`{不可打破的业务规则，如单调流向、状态前置依赖}`；
- **反例排除 (Not A)**：`{与相似概念的排他边界}`；
- **代码对齐 (Code Mapping)**：`com.example.domain.model.{CanonicalEntityA}`。

---

## 3. 通用子域概念 (Generic Domain)

### 3.1 租户与组织 (`Tenant` & `Organization`)
- **法定定义**：资源物理隔离与计费的最高逻辑容器；
- **代码对齐**：`TenantContext`。

---

## 4. 支撑子域概念 (Supporting Domain)

### 4.1 审计日志与追溯流水 (`AuditLog` & `TraceEvent`)
- **法定定义**：针对敏感资产状态流转的事后不可篡改凭据。

---

## 5. 废弃术语与消歧对照表

| 严禁使用的模糊口语词 | 强制规范术语 (Canonical Term) | 纠偏原因与代码映射 |
| :--- | :--- | :--- |
| 用户 (User) | **买家消费者 (Customer)** / **平台商户 (Merchant)** | 泛化词易导致越权漏洞；分别映射 `CustomerEntity` / `MerchantEntity` |
| 取消 (Cancel) | **撤销 (Revoke)** / **关闭 (Close)** | 撤单与超时关单处理逻辑与退款状态完全不同 |
