# Git Worktree 物理环境隔离操作实战案例 (Sample Worktree Workflow)

本案例展示了当主工作区存在未完成代码时，开发者需要紧急开发一个独立特性 `feat-order-export`，Agent 如何安全编排 Worktree 物理隔离并完成闭环。

---

## 场景描述

- **当前仓库路径**：`d:/projects/ecommerce-core`
- **当前状态**：`feature/shopping-cart` 正在开发中，有 5 个未暂存文件；
- **突发诉求**：用户需要紧急切出开发独立的“订单导出”特性，且绝不能污染当前购物车开发进度。

---

## 阶段 1：状态摸排与目录决策

Agent 检查当前工作区，发现脏改动：
```bash
git status --short
# M src/cart/service.ts
# ?? src/cart/temp-helper.ts
```

决策：在同级专用工作树目录 `../ecommerce-core-worktrees/feat-order-export` 下创建物理隔离环境，避免使用 `git stash` 带来的丢弃或恢复冲突风险。

---

## 阶段 2：创建物理隔离工作树并初始化

```bash
# 1. 确保上游最新基线已拉取
git fetch origin main

# 2. 创建同级隔离工作树并切出新分支
git worktree add -b feat-order-export ../ecommerce-core-worktrees/feat-order-export origin/main

# 3. 复制必需的环境配置文件
cp .env.local ../ecommerce-core-worktrees/feat-order-export/.env.local
```

终端切换至隔离工作树并安装锁定依赖：
```bash
cd ../ecommerce-core-worktrees/feat-order-export
pnpm install --frozen-lockfile
```

---

## 阶段 3：核验测试基线 (Green Baseline)

在编写任何新代码前，确认基准测试全部通过：
```bash
pnpm test:unit
# PASS src/order/order.test.ts (24 tests passed)
# Test Suites: 1 passed, 1 total
# Tests:       24 passed, 24 total
```
测试基线确认绿灯，工作树就绪。

---

## 阶段 4：特性开发与验证交付

在隔离工作树中完成订单导出特性开发与新单测编写：
```bash
# 执行测试验证，新增用例全部通过且既有用例无回归
pnpm test:unit
# PASS src/order/order-export.test.ts (6 tests passed)
# PASS src/order/order.test.ts (24 tests passed)
# Tests:       30 passed, 30 total
```

提交代码：
```bash
git add src/order/order-export.ts tests/order/order-export.test.ts
git commit -m "feat(order): 新增订单 Excel 异步导出能力与单元测试"
```

---

## 阶段 5：清理收尾与工作区复位

特性开发完毕且按需推送到远端分支后，执行工作树资源回收：
```bash
# 1. 切回主工作区目录
cd ../../ecommerce-core

# 2. 移除已完成的工作树
git worktree remove ../ecommerce-core-worktrees/feat-order-export

# 3. 修剪已失效的工作树索引
git worktree prune

# 4. 确认主工作区未完成代码完好无损
git status --short
# M src/cart/service.ts
# ?? src/cart/temp-helper.ts
```

至此，新特性在物理零污染环境下高效交付，主工作区上下文平滑保留。
