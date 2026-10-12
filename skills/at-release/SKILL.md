---
name: at-release
description: 当用户需要组织生产版本发布、执行上线前起飞检查 (Pre-Flight Checklist)、锁定 SemVer 语义化版本号、合并增量规范至主干规格或归档变更历史时使用此技能。提供现代化安全发版协议与归档模板，交付确定可靠的发布闭环。
disable-model-invocation: false
disable-slash-command: false
argument-hint: "[preflight|semver|archive|tag]"
allowed-tools:
  - view_file
  - run_command
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags: [release, shipping, semver, pre-flight, spec-archiving]
---

# 安全发布与规范归档演进技能 (Safe Release & Archiving Engine)

本技能提供面向生产系统渐进发布、上线起飞核验清单、增量变更规范（Specs）合流与语义化版本锁定的工程发布体系。

```mermaid
flowchart LR
    S1["1. 起飞前六维检查单核验"] --> S2["2. SemVer 版本号判定与元数据锁定"]
    S2 --> S3["3. 增量规范合并与主干规格同步"]
    S3 --> S4["4. 变更目录归档与日志对齐"]
    S4 --> S5["5. Git 打标与渐进放量发布"]
```

## 执行流程状态机 (Execution State Machine)

### 阶段 1：起飞前六维检查单核验 (Pre-Flight Verification)
- 验证代码分支干净且与远端同步，所有关联 PR 审查通过；
- 检查自动化单元测试与端到端冒烟测试门禁处于 100% 绿灯状态；
- 执行依赖安全漏洞扫描，拦截高危 CVE 风险；
- 详尽检查项参考 [上线前起飞检查单协议](./references/checklists/pre-flight-launch-checklist.md)。

### 阶段 2：SemVer 版本号判定与元数据锁定 (SemVer & Metadata)
- 评估本周期交付特性，依据是否存在破坏性变更判定版本号晋升；
- 严格遵循语义化版本规范（MAJOR.MINOR.PATCH）计算目标版本号；
- 批量更新工程清单文件（`package.json`、`pom.xml`、`Cargo.toml` 等）中的版本元数据；
- 规则与基线参考 [增量规范合并与归档协议](./references/protocols/spec-archiving-protocol.md)。

### 阶段 3：增量规范合并与主干规格同步 (Spec Merging)
- 将本周期 `specs/changes/` 下各特性的增量设计汇流至全局主干规范；
- 同步更新系统核心 API 契约、数据模型 ER 图与领域架构拓扑设计；
- 清理或标明已过时的陈旧架构决策，维护全局单一真实信源（SSOT）；
- 完整发布操作参考 [正式版本发布实战样例](./examples/sample-release-workflow.md)。

### 阶段 4：变更目录归档与日志对齐 (Archiving & Changelog)
- 将已交付验收的变更包完整迁移至 `specs/archive/vX.Y.Z/` 留痕目录；
- 对齐 `CHANGELOG.md`，将未发布条目固化为正式版本号与系统真实发布日期；
- 保持活动开发目录整洁，降低后续 Agent 检索上下文噪音；
- 归档目录结构参考 [增量规范合并与归档协议](./references/protocols/spec-archiving-protocol.md)。

### 阶段 5：Git 打标与渐进放量发布 (Tagging & Rollout)
- 生成具备清晰说明与变更摘要的 Git 附注标签（Annotated Tag）；
- 制定金丝雀（Canary）灰度放量比例与核心指标观察时窗；
- 确保部署回滚方案就绪，校验文档中西文排版与相对路径规范。

## 质量控制与合规自检 (Quality Checklist)
- [ ] 起飞检查单所有必选项严格核验通过，无未决 High/Critical 安全漏洞；
- [ ] 数据库变更具备已验证的反向回滚脚本，且遵循双向兼容演进原则；
- [ ] 增量设计文档已全量汇流并归档，活动工作区保持干净整洁；
- [ ] Git 标签使用附注标签（`git tag -a`），包含清晰版本摘要说明；
- [ ] 所有文档排版严格遵循盘古之白中西文空格与零绝对路径规范。

## 知识索引地图 (Knowledge Map)

| 知识模块 | 相对路径 | 核心内容说明 |
| :--- | :--- | :--- |
| 起飞检查协议 | `./references/checklists/pre-flight-launch-checklist.md` | 六维核验矩阵、依赖审计、数据库兼容与回滚策略 |
| 规范归档协议 | `./references/protocols/spec-archiving-protocol.md` | 增量汇流、历史归档目录、SemVer 判定与 Tag 规范 |
| 实战案例样本 | `./examples/sample-release-workflow.md` | v1.2.0 正式发布全流程核验、归档与打标操作样例 |

## 交付成果规范 (Deliverables Benchmark)
- **起飞核验清单**：经逐项核对并全部勾选的上线前安全审计记录；
- **主干规范更新**：汇流了增量特性后的系统全局主规格书（Master Specs）；
- **归档留痕资产**：迁移至 `specs/archive/` 的结构化历史变更包；
- **版本变更日志**：明确标注正式版本号与发布日期的 `CHANGELOG.md`；
- **Git 附注版本标签**：符合 SemVer 规范且语义清晰的 Git Tag 记录。
