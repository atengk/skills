# 增量规格契约实战示例：用户注销 7 天冷静期机制 (Sample Delta Spec)

本文档呈现了一个针对存量系统增加“账户注销 7 天冷静期与撤销注销机制”的真实增量规格契约范例。

---

## 规格元数据头 (Frontmatter)

```yaml
---
spec-id: "DELTA-20261012-USER-ACCOUNT-COOLING-OFF"
title: "存量用户注销流程增加 7 天冷静期与自助撤销契约"
baseline-version: "commit-a8f3d10 (v2.4.0)"
target-modules:
  - "com.example.user.service"
  - "com.example.user.controller"
status: "APPROVED"
author: "Ateng"
created-at: "2026-10-12"
---
```

---

## 1. 变更背景与爆炸半径 (Baseline & Scope)

### 1.1 变更动因
依据合规监管要求与用户体验防误触原则，存量“立即物理标记删除”流程必须改造为“7 天冷静期”。冷静期内账户冻结核心功能但保留数据，用户再次登录可一键撤销注销申请。

### 1.2 影响分析
- **直接受影响类**：`UserServiceImpl`、`UserController`、`UserAccountEntity`；
- **间接受影响组件**：登录认证拦截器 `AuthInterceptor`（需识别冷静期状态）；
- **外部依赖**：无新增依赖。

---

## 2. 增量契约矩阵 (Delta Matrix)

### 2.1 新增契约 (Added)

#### `SPEC-ADD-01`：自助撤销注销申请接口
- **载体**：`POST /api/v1/users/cancel-cancellation`
- **输入**：`CancelCancellationRequest { String cancelReason }`（鉴权 Token 从 Header 获取）
- **行为**：检查当前用户状态是否为 `CANCEL_COOLING_OFF`；若符合，重置用户状态为 `ACTIVE` 并清理冷却截止时间戳。
- **输出**：`UserSummaryVO`，状态码 `200 OK`。
- **断言转化**：
  - `Given`：用户状态为 `CANCEL_COOLING_OFF` 且冷却截止时间在未来；
  - `When`：调用该撤销接口；
  - `Then`：数据库 `status` 变为 `ACTIVE`，`cooling_deadline` 清空，返回成功。

---

### 2.2 变更契约 (Modified)

#### `SPEC-MOD-01`：申请注销接口逻辑变更
- **载体**：`POST /api/v1/users/apply-cancellation`
- **基线行为 (Before)**：直接将数据库 `status` 更新为 `DELETED`，不可逆，立即剔除登录态。
- **增量行为 (After)**：
  - 更新 `status` 为 `CANCEL_COOLING_OFF`；
  - 写入 `cooling_deadline = now() + 7 days`；
  - 踢出当前所有有效 Token，通知登出。
- **兼容性**：接口入参、返回值契约保持向后兼容，仅状态流转目标值与附加时间字段发生变化。

---

### 2.3 移除/废弃契约 (Removed)

#### `SPEC-REM-01`：废弃直接物理硬删除方法
- **废弃载体**：`UserDao.hardDeleteById(Long userId)`
- **替代指引**：全量调用点迁移至 `UserDao.markCoolingOff(Long userId, Instant deadline)`，硬删除仅由 7 天后定时作业执行。

---

## 3. 不变式守恒律 (Invariants)

1. **[INV-01 资产清零先决条件]**：用户账户余额 $> 0$ 或存在未完结借贷订单时，**绝对禁止**进入注销冷静期，必须阻断并抛出 `422 Unprocessable Entity`。
2. **[INV-02 冷静期权限拦截]**：处于 `CANCEL_COOLING_OFF` 状态的用户，除“登录查看冷静期提示”及“撤销注销”两个接口外，**所有业务接口统一拦截并返回 `403 Forbidden`**。
3. **[INV-03 空安全返回规范]**：查询当前注销状态信息接口若无注销记录，返回空对象结构体，严禁返回 `null`。

---

## 4. 故障域与异常响应 (Failure Domains)

| 异常标识 | 触发条件 | 响应状态码 / 异常 | 容错表现 |
| :--- | :--- | :--- | :--- |
| **ERR-COOL-01** | 用户已在冷静期内重复调用申请接口 | `409 Conflict` | 幂等返回已有冷静期的剩余截止时间，不重复重置 7 天计时 |
| **ERR-COOL-02** | 非冷静期状态用户尝试调用撤销接口 | `400 Bad Request` | 拦截并提示“当前账户无需撤销” |
