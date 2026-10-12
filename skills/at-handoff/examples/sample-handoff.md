# 架构设计转入编码阶段交接棒实战样例 (Sample Handoff: Design to Coding)

本案例记录在完成“分布式任务调度系统”的技术方案设计与架构决策后，无损移交给编码实现 Agent 的真实交接棒内容。

---

## 1. 移交档案基本信息

- **项目名称**：`cron-orchestrator`
- **交接时刻**：`2026-10-12 18:00:00`
- **移交源头**：方案设计与预研 Agent
- **接棒目标**：核心主干编码与 TDD 实现 Agent
- **代码状态**：`origin/feat-job-scheduler` (Commit: `8a2d1f9`)

---

## 2. 第一象限：已完成成果

- [x] 完成架构决策记录：`docs/adr/0004-use-redis-zset-for-delay-queue.md`（MADR 3.0 格式）；
- [x] 完成核心 API 契约设计：`specs/changes/002-job-api/openapi.yaml`；
- [x] 完成丢弃型并发原型验证：`scratch/prototype_zset_throughput.ts`，验证单分片 QPS 可达 12,000；
- [x] 质量门禁状态：所有新增 Markdown 文档盘古之白空格核验 100% 绿灯。

---

## 3. 第二象限：排他性技术决策共识

1. **队列底层选型**：选择 Redis ZSet 按照触发时间戳（Timestamp）作为 Score，**否决了 RabbitMQ 延迟插件**，原因是减少外部中间件依赖并支持精确到毫秒级的动态取消；
2. **锁模型**：采用 Redis Redlock 模式保证多节点争抢任务时的分布式独占，租期设置为 5 秒并集成自动续期（Watchdog）。

---

## 4. 第三象限：当前断点现场

- **活动分支**：`feat-job-scheduler`，当前工作树干净，无未追踪文件；
- **环境基准**：依赖 Node.js v20.x，Docker 本地运行 Redis 7.2 镜像于 6379 端口；
- **待开工入口**：`src/scheduler/task-dispatcher.ts` 尚未创建，准备从单元测试开始推进红绿循环。

---

## 5. 第四象限：待办任务与接棒启动

| 序号 | 任务描述 | 建议采用技能 | 验收准则 |
| :---: | :--- | :--- | :--- |
| **1** | 编写任务分发器核心调度循环的失败测试（红灯） | `at-tdd` | `tests/unit/dispatcher.spec.ts` 覆盖 ZSet 轮询与拉取逻辑 |
| **2** | 编写最小实现代码使单测变绿 | `at-tdd` | 测试 100% 通过且无类型警告 |
| **3** | 对任务调度器进行卫语句与控制流扁平化重构 | `at-simplify` | 消除深层嵌套，圈复杂度 ≤ 5 |

---

## 6. 一键唤醒启动指令

```markdown
请熟悉交接文档：HANDOFF.md

我们上一阶段已经圆满完成任务调度系统的架构设计与选型论证（已落盘 ADR-0004 与 API 契约）。
现在正式进入核心编码实现阶段。请执行以下指令：
1. 检出分支 feat-job-scheduler；
2. 激活 at-tdd 技能，从 tests/unit/dispatcher.spec.ts 开始编写第一个调度循环单测；
3. 严格遵循 Red-Green-Refactor 流程，保证测试驱动的高质量实现。

请确认已接收交接棒并开始输出你的 TDD 开工计划！
```
