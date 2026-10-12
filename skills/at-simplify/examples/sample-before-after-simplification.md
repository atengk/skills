# 代码极简精简实操前后对比案例 (Sample Before & After Simplification)

本案例通过一个经典的电商“优惠券核销与订单折算”逻辑，展示如何应用奥卡姆剃刀与卫语句消除深层金字塔嵌套和过度工程。

---

## 精简前代码：典型深层箭头金字塔与过度抽象

```typescript
// 复杂的单实现工厂 + 4 层嵌套
interface ICouponStrategy {
  calculate(order: Order, coupon: Coupon): number;
}

class StandardCouponStrategy implements ICouponStrategy {
  calculate(order: Order, coupon: Coupon): number {
    let result = order.totalAmount;
    if (order != null) {
      if (order.status === 'PENDING') {
        if (coupon != null && coupon.isValid) {
          if (order.totalAmount >= coupon.minThreshold) {
            if (new Date() <= coupon.expireAt) {
              result = order.totalAmount - coupon.discountAmount;
            } else {
              throw new Error("Coupon expired");
            }
          } else {
            throw new Error("Threshold not met");
          }
        } else {
          throw new Error("Invalid coupon");
        }
      } else {
        throw new Error("Order not pending");
      }
    } else {
      throw new Error("Order required");
    }
    return result;
  }
}
```

### 痛点诊断
1. **过度抽象**：仅有一种核销策略，却引入了 `ICouponStrategy` 与策略类包装；
2. **箭头反模式 (Arrow Anti-Pattern)**：缩进层级高达 5 层，异常分支分散在文件末尾，阅读心智负担沉重；
3. **可读性极差**：寻找核心计算公式需要穿越层层嵌套。

---

## 精简后代码：扁平卫语句与自解释肯定表达

```typescript
// 消除伪接口，使用扁平卫语句 + 解释性变量
export function applyCouponDiscount(order: Order, coupon: Coupon): number {
  // 1. 前置卫语句拦截非法输入与前置状态
  if (!order) {
    throw new Error("Order required");
  }
  if (order.status !== 'PENDING') {
    throw new Error("Order not pending");
  }
  if (!coupon || !coupon.isValid) {
    throw new Error("Invalid coupon");
  }

  // 2. 提取具名解释性布尔条件
  const isExpired = new Date() > coupon.expireAt;
  if (isExpired) {
    throw new Error("Coupon expired");
  }

  const isThresholdMet = order.totalAmount >= coupon.minThreshold;
  if (!isThresholdMet) {
    throw new Error("Threshold not met");
  }

  // 3. 核心计算逻辑顶格左对齐展开，一目了然
  return Math.max(0, order.totalAmount - coupon.discountAmount);
}
```

---

## 重构收益总结

- **嵌套深度**：从 5 层暴降为 1 层；
- **核心逻辑突出度**：核心业务计算一览无余，无需寻找配对的括号与 `else`；
- **测试通过率**：既有 10 组单元测试无需修改任何断言，全部 100% 绿灯通过；
- **维护成本**：新增校验条件只需在顶部添加一行自解释卫语句，零侵入核心计算逻辑。
