# 疑难缺陷根因诊断与排错报告模板 (Diagnostic Report Template)

本文档定义了 `at-diagnose` 技能在完成缺陷排查后输出的诊断报告（默认呈现于会话或落盘为 `diagnostic-report.md`）标准结构。

---

## 目录 (Table of Contents)
- [1. 故障元数据与初始表象](#1-故障元数据与初始表象)
- [2. 紧反馈复现循环命令](#2-紧反馈复现循环命令)
- [3. 假设推演与证据链记录](#3-假设推演与证据链记录)
- [4. 物理根因深度分析](#4-物理根因深度分析)
- [5. 纵深防御修复与永久回归测试](#5-纵深防御修复与永久回归测试)
- [6. 清理确认与架构防范建议](#6-清理确认与架构防范建议)

---

## 1. 故障元数据与初始表象

```markdown
# 缺陷根因诊断报告：{缺陷简明标题} (Diagnostic Report)

> **故障标识**：`BUG-{YYYYMMDD}-{MODULE}`
> **涉及环境**：{开发环境 / CI / 准生产}
> **严重程度**：`BLOCKER | MAJOR | MINOR`
> **排查时间**：{YYYY-MM-DD}
> **状态**：`VERIFIED_AND_FIXED`
```

### 1.1 初始故障表象
- **错误堆栈 / 异常提示**：
  ```text
  {粘贴关键报错信息，已自动脱敏机密与本地绝对路径}
  ```
- **预期行为**：`{描述系统按设计应表现的行为}`
- **实际行为**：`{描述实际发生的异常行为}`

---

## 2. 紧反馈复现循环命令

- **单行自动化复现命令**：
  ```bash
  {单行测试指令或脚本，如 mvn test -Dtest=OrderReproTest#testConcurrentCancel}
  ```
- **复现特征**：耗时 `{X}` 秒，复现稳定性 `100% (确定性) | N% (压力循环稳定)`。

---

## 3. 假设推演与证据链记录

| 假设编号 | 假设描述 (Hypothesis) | 可证伪预测 (Falsifiable Prediction) | 验证手段与插桩 | 最终结论 |
| :---: | :--- | :--- | :--- | :---: |
| **H1** | 缓存数据未序列化过期时间 | 若显式传入固定 TTL，Key 依然永不失效 | `[DEBUG-a1b2]` 日志探针 | ❌ 证伪 (排除) |
| **H2** | 事务内部异步发布事件引发脏读 | 将事件发布移至事务提交后，脏读消失 | 单变量代码调整 | ✔️ 证实 (确认根因) |

---

## 4. 物理根因深度分析

<!-- 运用 5 Whys 或因果链条深入剖析，直击物理根本原因 -->
1. **直接原因**：事件监听者在主事务尚未 Commit 时便收到消息并发起数据库反查；
2. **中间诱因**：`@TransactionalEventListener` 缺少显式 `phase = TransactionPhase.AFTER_COMMIT` 注解；
3. **根本根因**：团队历史工具类默认封装将事件总线直接作为进程内即时同步派发，未对事务边界实施契约防御。

---

## 5. 纵深防御修复与永久回归测试

### 5.1 纵深防御性修复代码
- **修改文件**：`src/main/java/com/example/event/EventPublisher.java`
- **防御加固**：
  - 增加事务处于活动态（`TransactionSynchronizationManager.isActualTransactionActive()`）时的延迟发布安全网；
  - 拒绝裸打补丁，从源头切断未提交脏读可能性。

### 5.2 永久回归测试用例
- **测试文件**：`src/test/java/com/example/event/EventPublisherRegressionTest.java`
- **执行命令**：`mvn test -Dtest=EventPublisherRegressionTest`（运行通过，结果 100% 绿灯）。

---

## 6. 清理确认与架构防范建议

- [x] 所有 `[DEBUG-...]` 临时探针与打印已 100% 物理移除；
- [x] 原始紧反馈循环已完全由红变绿；
- **防范建议**：建议将事务感知事件发布抽象为核心脚手架，并在 Checkstyle/Linter 中增加对裸事件派发的静态告警规则。
