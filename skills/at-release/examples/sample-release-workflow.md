# 正式版本发布全流程实战样例 (Sample Release Workflow)

本案例记录系统从开发完成到正式生产发布 `v1.2.0` 的标准操作流程，涵盖起飞检查单核验、增量规范归档、变更日志对齐与 Git Tag 打标全过程。

---

## 1. 发布任务基本信息

- **目标版本**：`v1.2.0` (SemVer: MINOR，新增向后兼容特性)
- **主要特性**：多租户空间隔离、在线支付网关集成与性能优化；
- **发布负责人**：Ateng

---

## 2. 阶段 1：起飞前检查单核验 (Pre-Flight Verification)

```text
[✔ 成功] 分支基线检查：main 分支与远端保持同步，working tree clean
[✔ 成功] 自动化门禁：CI 流水线运行完毕，单元测试 214/214 通过，E2E 冒烟测试全绿
[✔ 成功] 依赖安全性：npm audit 扫描完成，0 vulnerabilities (0 high, 0 critical)
[✔ 成功] 数据库演练：V1.2.0__add_tenant_tables.sql 预发执行成功，Down 脚本演练通过
[✔ 成功] 凭据审计：无明文密钥，已配置生产 Kubernetes Secret: db-credentials
[✔ 成功] 监控就绪：核心交易 RED 仪表盘已打开，告警通知群组正常在线
```

---

## 3. 阶段 2：增量规范合并与归档操作

### 3.1 合并增量规范至主干规格
- 将 `specs/changes/003-tenant-isolation/api-spec.yaml` 中的多租户端点合并至 `specs/master/api-spec.yaml`；
- 更新 `specs/master/data-model.md` 中的租户架构 ER 图。

### 3.2 归档变更目录
```bash
# 创建版本归档目录并迁移增量包
mkdir -p specs/archive/v1.2.0
git mv specs/changes/003-tenant-isolation specs/archive/v1.2.0/
git mv specs/changes/004-payment-gateway specs/archive/v1.2.0/
```

---

## 4. 阶段 3：CHANGELOG.md 对齐与版本锁定

更新 `CHANGELOG.md` 顶部条目：

```markdown
## [1.2.0] - 2026-10-12

### Added
- 多租户组织架构与资源数据物理隔离能力；
- 微信与支付宝在线收银台支付通道集成；
- 端到端核心旅程 Playwright 自动化验收门禁。

### Changed
- 优化订单查询分页 SQL，P99 延迟降低 45%。
```

---

## 5. 阶段 4：Git 打标与正式发布生效

```bash
# 1. 提交发布准备元数据变更
git add specs/ CHANGELOG.md package.json
git commit -m "chore(release): prepare release v1.2.0"

# 2. 创建附注版本标签
git tag -a v1.2.0 -m "release: 正式发布 v1.2.0 - 包含多租户隔离与支付网关能力"

# 3. 推送主分支与标签至远端仓库 (需人工显式授权)
# git push origin main --tags
```
