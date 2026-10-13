# 全生命周期多技能协同串联实战样例 (Sample Workflow Orchestration)

本案例记录开发者输入 `/at-workflow #42` 时，`at-workflow` 作为总控中枢如何自动解析 GitHub Issue #42、锚定特性命名空间、在会话内通过内联接力（Inline Chaining）串联 6 个核心技能推进完整研发闭环，并最终生成 Issue 回填评论的全过程。

---

## 1. 意图诊断与远程 Issue 锚定

**开发者**：“`/at-workflow #42`”

**`at-workflow` 响应**：
> 🔗 **远程 Issue 关联成功**：
> - **来源**：GitHub Issue #42 (订单 30 分钟超时未支付自动取消与库存释放)
> - **特性目录**：`.specs/issue-42-order-timeout/`
> - **推荐路线**：配方 1（全新特性研发流：`at-grill` -> `at-spec` -> `at-plan` -> `at-tdd` -> `at-review`）
>
> 正在启动第一阶段需求质询...

---

## 2. 阶段推演与会话内内联接力 (Inline Chaining)

### 阶段 1：激活 `at-grill` 需求压力测试
- Agent 针对订单状态机逆向流转、并发支付与超时取消临界竞争、库存释放幂等性提出 3 个反向质询；
- 产出确认备忘录，明确“Redis 延迟队列分发，状态机采用乐观锁 CAS 校验，库存回滚强制幂等”。
- **人机闸门**：开发者回复“质询结论确认，进入下一阶段”。

### 阶段 2：会话内接力激活 `at-spec` 拟定增量契约
- Agent **无需开发者退出重输命令**，自动在当前会话内加载 `at-spec` 协议；
- 生成增量契约文件：`.specs/issue-42-order-timeout/delta.md`；
- 核心定义：
  - Added：`OrderTimeoutScheduler` 与 `StockRollbackEvent`；
  - Modified：`OrderService.cancelOrder()` 增加状态版本校验；
  - Invariants：订单一旦进入 CANCELLED 状态，禁止任何后续扣款，锁定库存必须 100% 释放。
- **人机闸门**：输出规格审阅卡片，开发者审阅后回复“契约无误”。

### 阶段 3：会话内接力激活 `at-plan` 拓扑微任务拆解
- 依据 `delta.md` 编译 2~5 分钟微任务清单，生成 `.specs/issue-42-order-timeout/tasks.md`；
- 示踪线（Tracer Bullet）优先排序：
  - Task 1: 延迟队列监听器核心骨架与单测红灯；
  - Task 2: 订单状态机 CAS 取消与幂等性单测；
  - Task 3: 库存回滚事件广播与补偿逻辑集成。
- **人机闸门**：开发者回复“微任务拆解合理，开工”。

### 阶段 4：会话内接力激活 `at-tdd` 测试驱动开发
- 严格遵循红-绿-重构纪律：
  - 针对 Task 1 编写 `OrderTimeoutSchedulerTest`（红灯 Failure 退出码非 0）；
  - 编写最小监听实现（绿灯 Pass 退出码 0）；
  - 执行思维突变检验（反转超时时间判断，确认测试敏锐杀死突变体）；
  - 在 `tasks.md` 中打卡 `[x] Task 1`；
- 依次推进 Task 2 与 Task 3，所有微任务 100% 打卡完成。

### 阶段 5：会话内接力激活 `at-review` 双轴代码审查
- Standards 轴：100% 遵循工程宪章（`CONSTITUTION.md`），无绝对路径泄漏，无裸明文凭据；
- Spec 轴：严格对齐 `delta.md` 不变式，未发生契约漂移；
- 产出双轴审查报告：`.specs/issue-42-order-timeout/review.md`（综合评分 98/100，0 Blocker）。

---

## 3. 闭环审计与远程 Issue 结项回填

工作流进入阶段 5，Agent 汇总全生命周期工件并输出 Issue 回填草案：

```markdown
## ✅ 需求实现与交付验收报告 (Delivery Summary)

### 1. 变更范围与核心工件
- **规格契约**：`.specs/issue-42-order-timeout/delta.md`
- **任务清单**：`.specs/issue-42-order-timeout/tasks.md` (3/3 原子微任务全部闭环)
- **审查报告**：`.specs/issue-42-order-timeout/review.md` (0 Blocker, 双轴合规)

### 2. 代码实现与自测验证
- 修复超时未支付订单库存死锁问题，引入 Redis 延迟死信与 CAS 状态乐观锁；
- 单元测试套件全部绿灯通过，覆盖高并发竞态边界。
```

开发者在终端运行 `gh issue comment 42 --body "..."` 完成远程闭环。

---

## 4. 全局调度复盘与效能收益

通过 `at-workflow` 升级后的总控编排能力：
1. **零交互中断**：在关闭模型自主唤醒的情况下，依靠会话内授权内联接力，开发者无需重复键入斜杠命令；
2. **工件物理收敛**：所有临时规范与任务清单统一聚合于 `.specs/issue-42-order-timeout/`，根目录零污染；
3. **闭环双向追溯**：从 GitHub Issue #42 出发，最终以结构化验收评论回填结束，研发上下文完整透明。
