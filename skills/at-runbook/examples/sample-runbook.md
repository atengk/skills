# 生产故障应急手册实战案例 (Sample Runbook)

本案例展示了一个针对“高并发大促期间数据库连接池满载与 HikariCP 线程死锁”的工业级应急 Runbook。

---

## 范例文档正文

```markdown
# 运维应急手册: 订单服务数据库连接池满载与超市响应 (P0)

> **故障分级**：P0 (核心业务受阻)
> **责任服务**：`order-center`
> **责任团队**：订单交易与架构组
> **最后修订**：2026-10-12

---

## 1. 故障表现与告警特征

- **告警标题**：`HikariPool-1 - Connection is not available, request timed out after 30000ms`
- **监控指标**：`hikaricp_connections_pending > 50` 持续 1 分钟，交易成功率暴跌至 60%
- **业务影响**：前端用户在提交订单时无限加载并最终提示“网络超时，请重试”

---

## 2. 5 分钟内止血 SOP (先止血，切勿原地看代码)

### 动作 1：若 20 分钟内有新发版，立即一键回滚
```bash
# 执行 Kubernetes 历史版本回滚
kubectl rollout undo deployment/order-center -n prod
```

### 动作 2：开启非核心旁路功能降级 (削峰保主干)
```bash
# 通过 Nacos/Apollo 动态开关关闭“订单实时积分折算”与“历史发票查询”
curl -X POST "http://config.internal/api/switch" -d "key=degrade.order.bonus=true"
```

### 动作 3：临时隔离并重启连接池僵死 Pod
```bash
# 逐个重启异常 Pod，让连接池重新建立干净握手
kubectl rollout restart deployment/order-center -n prod
```

---

## 3. 标准化深层排查步骤 (止血后进行)

### 步骤 1：排查 MySQL 数据库端长事务与锁等待
```sql
-- 查询阻塞超过 10 秒的长事务与锁信息
SELECT r.trx_id waiting_trx_id, r.trx_mysql_thread_id waiting_thread,
       b.trx_id blocking_trx_id, b.trx_mysql_thread_id blocking_thread,
       TIMESTAMPDIFF(SECOND, r.trx_started, NOW()) wait_secs
FROM performance_schema.data_lock_waits w
JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_engine_transaction_id
JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_engine_transaction_id;
```

### 步骤 2：抓取应用层线程快照定位持锁代码
```bash
# 获取 CPU 占用最高的线程与持锁堆栈
jstack $(pgrep -f order-center) > /tmp/order_jstack_$(date +%s).log
grep -A 20 "runnable" /tmp/order_jstack_*.log | grep -E "OrderMapper|PaymentClient"
```

---

## 4. 彻底恢复验收标准

- [ ] `hikaricp_connections_pending` 数量回落至 0；
- [ ] 订单创建接口 HTTP 200 成功率恢复至 99.99%；
- [ ] P99 响应延迟回落至 80ms 以内。
```
