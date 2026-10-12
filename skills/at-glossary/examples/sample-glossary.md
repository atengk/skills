# 电商交易与履约领域统一语言字典样例 (Sample Glossary)

本文档呈现了一个针对电商订单与仓储履约系统的真实 `GLOSSARY.md` 示范文件。

---

# 电商交易与履约统一语言字典 (Ubiquitous Language)

> **上下文边界**：订单中心、仓配履约与库存中台
> **最后维护**：2026-10-12

---

## 1. 核心交易概念 (Trading Domain)

### 1.1 交易订单 (`TradeOrder`)
- **定义**：买家在前端购物车结算生成的全局法律级商业交易凭据；
- **核心约束**：全局唯一，总金额在生成后绝对不可篡改；
- **反例排除**：**不是**仓库拣货打包的物理单据（那是履约单 `FulfillmentOrder`）；
- **代码映射**：`com.example.trade.entity.TradeOrder`。

### 1.2 预占库存 (`ReservedStock`)
- **定义**：用户进入收银台待支付期间，为防止超卖而临时在 Redis 中预扣除的逻辑库存；
- **核心约束**：具备 15 分钟 TTL 倒计时，超时未付自动归还；
- **反例排除**：**不是**仓库已实物下架扣减的实物库存（那是扣减库存 `DeductedStock`）；
- **代码映射**：`com.example.inventory.service.StockReservationService`。

---

## 2. 履约仓配概念 (Fulfillment Domain)

### 2.1 履约单 (`FulfillmentOrder`)
- **定义**：交易订单支付成功后，根据商家分仓规则拆单后派发给物理仓库作业的指令单据；
- **核心约束**：一个 `TradeOrder` 可拆分为 1~N 个 `FulfillmentOrder`；
- **代码映射**：`com.example.fulfillment.entity.FulfillmentOrder`。

---

## 3. 术语纠偏与消歧对照表

| 模糊歧义口语 | 规范领域术语 (Canonical) | 纠偏说明与代码映射 |
| :--- | :--- | :--- |
| 取消订单 | **超时关单 (`AutoExpire`)** | 超时自动释放预占库存，无需发起退款流程 |
| 取消订单 | **买家主动撤单 (`BuyerRevoke`)** | 未支付状态下买家手动取消，立即释放库存 |
| 取消订单 | **售后退款 (`RefundAfterPay`)** | 已支付状态走逆向退款工作流，不可直接改订单状态 |
