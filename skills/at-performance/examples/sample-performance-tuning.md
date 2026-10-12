# 全栈高并发慢接口调优实操案例 (Sample Performance Tuning)

本案例通过一个在促销大促期间 P99 延时超过 3.8 秒、经常发生超时的“用户订单列表与商品明细查询”接口，展示从执行计划分析、消除 N+1、覆盖索引重构到 Redis 缓存集成的全流程调优。

---

## 优化前代码：经典的 N+1 查询与未命中索引

```java
// 优化前的慢接口实现
@GetMapping("/api/orders/my")
public List<OrderVO> getMyOrders(@RequestParam Long userId, @RequestParam int page) {
    int pageSize = 20;
    int offset = (page - 1) * pageSize;

    // 慢点 1: 全表扫描，缺少 (user_id, created_at) 联合索引
    List<OrderDO> orders = orderMapper.selectByUserIdWithPage(userId, offset, pageSize);

    List<OrderVO> result = new ArrayList<>();
    // 慢点 2: 致命的 N+1 循环查询数据库
    for (OrderDO order : orders) {
        List<OrderItemDO> items = itemMapper.selectByOrderId(order.getId()); // 循环查 DB!
        UserProfileDO merchant = userMapper.selectById(order.getMerchantId()); // 循环查 DB!
        result.add(assembleVO(order, items, merchant));
    }
    return result;
}
```

### EXPLAIN 慢查询诊断
```sql
EXPLAIN SELECT * FROM t_orders WHERE user_id = 10086 ORDER BY created_at DESC LIMIT 0, 20;
```
- `type`: `ALL`（全表物理扫描，数据量 500 万行时耗时 1800ms）；
- `Extra`: `Using filesort`（内存与磁盘临时文件排序）。

---

## 优化措施与实施

### 1. 建立覆盖复合索引
针对高频查询维度建立联合索引：
```sql
ALTER TABLE t_orders ADD INDEX idx_user_created (user_id, created_at DESC);
ALTER TABLE t_order_items ADD INDEX idx_order_id (order_id);
```
执行计划直接跃升为 `type: ref`，`Extra: Using index condition`，查询耗时由 1800ms 降至 6ms。

### 2. 批量查询彻底消除 N+1，结合旁路缓存

```java
@GetMapping("/api/orders/my")
public List<OrderVO> getMyOrders(@RequestParam Long userId, @RequestParam int page) {
    int pageSize = 20;
    int offset = (page - 1) * pageSize;

    // 1. 命中 idx_user_created 索引快速分页
    List<OrderDO> orders = orderMapper.selectByUserIdWithPage(userId, offset, pageSize);
    if (orders.isEmpty()) {
        return Collections.emptyList();
    }

    // 2. 批量提取订单 ID 与商家 ID，1 次批量查询取代 40 次单次查询
    List<Long> orderIds = orders.stream().map(OrderDO::getId).toList();
    List<Long> merchantIds = orders.stream().map(OrderDO::getMerchantId).distinct().toList();

    // 批量查询商品明细与商家信息 (IN 查询)
    Map<Long, List<OrderItemDO>> itemsMap = itemMapper.selectByOrderIds(orderIds)
            .stream().collect(Collectors.groupingBy(OrderItemDO::getOrderId));

    // 商家信息走多级缓存 (Redis + 本地 Caffeine)
    Map<Long, UserProfileDO> merchantMap = merchantCacheService.getBatchWithCache(merchantIds);

    // 3. 纯内存极速组装
    return orders.stream()
            .map(o -> assembleVO(o, itemsMap.getOrDefault(o.getId(), List.of()), merchantMap.get(o.getMerchantId())))
            .toList();
}
```

---

## 调优效果量化比对

在并发压测环境（100 并发用户连续请求 1 分钟）下的压测结果对比：

| 指标 | 调优前 | 调优后 | 优化幅度 |
| :--- | :---: | :---: | :---: |
| **P95 响应时间** | 2,450 ms | **38 ms** | ⬇️ **98.4%** |
| **P99 响应时间** | 3,820 ms | **65 ms** | ⬇️ **98.3%** |
| **系统吞吐量 (QPS)** | 42 req/s | **1,850 req/s** | ⬆️ **44 倍** |
| **数据库连接池占用** | 100% 满载排队 | **12% 平稳** | 消除死锁与排队 |
