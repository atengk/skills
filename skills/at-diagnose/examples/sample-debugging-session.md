# 疑难缺陷系统化排查实战全过程 (Sample Debugging Session)

本文档呈现了一个针对“异步事件消费者偶发读取不到未提交订单”复杂并发缺陷进行系统化根因排查与修复的完整工程案例。

---

## 目录 (Table of Contents)
- [1. 初始故障报告与表象](#1-初始故障报告与表象)
- [2. 阶段 1：构建紧反馈循环与最小重现](#2-阶段-1构建紧反馈循环与最小重现)
- [3. 阶段 2：穷举可证伪假设并排定优先级](#3-阶段-2穷举可证伪假设并排定优先级)
- [4. 阶段 3：插桩验证与锁定根因证据链](#4-阶段-3插桩验证与锁定根因证据链)
- [5. 阶段 4：纵深防御性修复与回归验证](#5-阶段-4纵深防御性修复与回归验证)

---

## 1. 初始故障报告与表象

> **用户报告**：“测试环境压测时，用户支付成功后偶发收不到赠送积分，日志偶尔报错 `OrderNotFoundException: 订单不存在`，但 1 秒后人工去数据库查订单明明已经在那里了！这太奇怪了。”

---

## 2. 阶段 1：构建紧反馈循环与最小重现

Agent 拒绝单纯看代码猜原因，首先在测试代码中构建紧反馈循环：

1. **编写最小复现单测**：`src/test/java/com/example/order/OrderPaymentEventReproTest.java`
   - 模拟支付主线程在 `@Transactional` 中保存订单并触发事件监听；
   - 监听线程立即根据 `orderId` 查询数据库。
2. **运行反馈命令**：
   ```bash
   mvn test -Dtest=OrderPaymentEventReproTest#testConcurrentPaymentEvent
   ```
3. **见证红灯**：循环 50 次并发调用，必有 3~5 次抛出 `OrderNotFoundException`，测试稳定亮起红灯。

---

## 3. 阶段 2：穷举可证伪假设并排定优先级

Agent 提出 3 个具备明确预测的可证伪假设：

1. **假设 H1 (读写分离主从同步延迟)**：
   - *预测*：若将测试环境数据库数据源强制锁定只读主库，该报错将完全消失；
2. **假设 H2 (事务未提交前监听线程已抢先执行反查)**：
   - *预测*：若在事件发布前人工让事件派发延迟 500ms（等待事务完成提交），该报错将不再发生；
3. **假设 H3 (Hibernate/JPA 一级缓存未刷新至底层连接)**：
   - *预测*：若在发布事件前调用 `entityManager.flush()`，该报错将消失。

---

## 4. 阶段 3：插桩验证与锁定根因证据链

1. **验证 H1**：测试环境原本就是单节点 H2/MySQL 内存库，无主从拓扑。**H1 排除**。
2. **验证 H3**：在事件前加入 `flush()`，单测依然 100% 出现红灯报错。**H3 排除**。
3. **插桩验证 H2**：
   - 在主线程与事件监听线程分别插入带前缀探针：
     ```java
     // [DEBUG-7c2a] 打印事务提交与事件监听线程时间戳
     log.info("[DEBUG-7c2a] 主线程事务提交完成时间: {}", System.currentTimeMillis());
     log.info("[DEBUG-7c2a] 监听线程执行查询时间: {}", System.currentTimeMillis());
     ```
   - 运行测试并捕获日志：
     ```text
     [DEBUG-7c2a] 监听线程执行查询时间: 1773342000100 -> 抛出 OrderNotFoundException
     [DEBUG-7c2a] 主线程事务提交完成时间: 1773342000150 -> 事务才真正 Commit！
     ```
   - **确凿证据**：监听线程比主线程事务 Commit 提前了 50ms 执行，查到的是未提交前的数据库视图！

---

## 5. 阶段 4：纵深防御性修复与回归验证

1. **纵深防御修复方案**：
   - 严禁在调用方加 `sleep(100)` 等脆弱补丁；
   - 在事件派发层使用 Spring 事务同步管理器：
     ```java
     if (TransactionSynchronizationManager.isActualTransactionActive()) {
         TransactionSynchronizationManager.registerSynchronization(new TransactionSynchronization() {
             @Override
             public void afterCommit() {
                 eventPublisher.publishEvent(event);
             }
         });
     } else {
         eventPublisher.publishEvent(event);
     }
     ```
2. **验证反馈循环**：
   - 重新执行 `mvn test -Dtest=OrderPaymentEventReproTest`；
   - 50 次高并发循环全部通过，**测试 100% 变绿**！
3. **清理收尾**：
   - 全局搜索并清理 `[DEBUG-7c2a]` 临时探针；
   - 将 `OrderPaymentEventReproTest` 改名为 `OrderPaymentEventRegressionTest` 纳入永久工程回归测试套件。
