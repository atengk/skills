---
name: at-ci
description: 当用户需要配置持续集成流水线、编写 GitHub Actions 工作流、集成代码质量门禁或设计自动化构建与发布流水线时使用此技能。提供现代化 CI/CD 流水线模板与门禁校验，交付稳定可靠的集成体系。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[workflow|lint|gate]"
allowed-tools:
  - view_file
  - run_command
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags: [ci-cd, github-actions, devops, quality-gate]
---

# 持续集成流水线与自动化门禁技能 (CI/CD Pipeline Engine)

本技能提供面向代码质量保障、自动化测试执行与多环境发布的现代化 CI/CD 流水线编排与门禁体系。

```mermaid
flowchart LR
    S1["1. 环境与技术栈识别"] --> S2["2. 门禁基线与阶段规划"]
    S2 --> S3["3. 工作流编写与缓存编排"]
    S3 --> S4["4. 矩阵测试与跨平台覆盖"]
    S4 --> S5["5. 流水线演练与质量审计"]
```

## 执行流程状态机 (Execution State Machine)

### 阶段 1：环境与技术栈识别 (Stack Identification)
- 识别项目语言基线（Node.js、Python、Java、Go 等）与构建打包工具；
- 探查当前测试套件框架（Jest、Pytest、JUnit 等）与覆盖率采集方案；
- 梳理目标托管平台特性与 Runner 运行环境限制；
- 检查是否存在历史 CI 配置文件并评估迁移适配成本。

### 阶段 2：门禁基线与阶段规划 (Gate Design)
- 制定轻量快速失败的四级漏斗门禁（格式化、静态检查、单测、制品构建）；
- 确立分支保护策略与 PR 合并前置必选检查项（Required Checks）；
- 设定测试覆盖率最低熔断阈值与代码异味阻断红线；
- 详细门禁标准与安全规则参考 [质量门禁协议](./references/protocols/ci-gate-protocol.md)。

### 阶段 3：工作流编写与缓存编排 (Workflow Authoring)
- 编写标准化声明式工作流配置（如 `.github/workflows/ci.yml`）；
- 配置精确的依赖缓存 Key，加速重复构建任务；
- 遵循最小特权原则收敛工作流 `GITHUB_TOKEN` 的读写权限；
- 标准流水线配置参考 [GitHub Actions 模板](./references/templates/github-actions-ci-template.md)。

### 阶段 4：矩阵测试与跨平台覆盖 (Matrix Testing)
- 按需配置操作系统（Ubuntu、Windows、macOS）与运行时版本组合矩阵；
- 确保测试环境之间完全独立无状态，杜绝并发执行冲突；
- 配置并发作业取消策略，当新提交到达时自动终止旧作业；
- 矩阵实战编排参考 [多平台门禁案例样本](./examples/sample-ci-workflow.md)。

### 阶段 5：流水线演练与质量审计 (Pipeline Audit)
- 校验工作流 YAML 语法完整性与阶段间依赖拓扑合理性；
- 审计流水线脚本是否严格使用环境变量或 Secret，杜绝凭据泄漏；
- 验证错误处理机制与失败通知告警闭环能力；
- 确保相关文档满足盘古之白排版与标准相对路径引用。

## 质量控制与合规自检 (Quality Checklist)
- [ ] 流水线中严禁硬编码任何真实账号密码、Token 或私有网络地址；
- [ ] 关键测试作业前置配置了依赖缓存，平均构建耗时保持在可控范围；
- [ ] 门禁阶段严格遵循由快到慢的拓扑依赖（Fail-Fast 策略）；
- [ ] 权限配置符合最小特权原则，默认禁止无意义的高危写权限；
- [ ] 所有中西文排版与相对路径互链符合全局工程规范。

## 知识索引地图 (Knowledge Map)

| 知识模块 | 相对路径 | 核心内容说明 |
| :--- | :--- | :--- |
| 质量门禁协议 | `./references/protocols/ci-gate-protocol.md` | 四级门禁模型、覆盖率熔断与安全基线 |
| CI 工作流模板 | `./references/templates/github-actions-ci-template.md` | 现代化 GitHub Actions 声明式工作流模板 |
| 实战案例样本 | `./examples/sample-ci-workflow.md` | 跨平台矩阵测试与发布门禁实战样本 |

## 交付成果规范 (Deliverables Benchmark)
- **CI 工作流定义**：格式严谨、开箱即用的工作流 YAML 文件；
- **门禁度量规则**：覆盖率与代码异味明确量化的门禁规则文件；
- **本地校验脚本**：与 CI 环境执行等价的本地预检脚本与指令；
- **配置与迁移手册**：包含环境变量与 Secret 配置说明的运维手册；
- **演练验证报告**：记录流水线阶段耗时与拦截效果的自检清单。
