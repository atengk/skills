---
name: at-rules
description: 当用户需要制定 AI 编程助手规范、初始化 AGENTS.md 行为准则、设计多智能体系统提示词或统一上下文治理规约时使用此技能。提供跨模型规约脚手架与自动化校验支持，交付高清晰度工程规则系统。
disable-model-invocation: false
disable-slash-command: false
argument-hint: "[init|check|export]"
allowed-tools:
  - view_file
  - run_command
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags: [agents, prompt-engineering, governance, ai-coding]
---

# 智能体工程规约与行为治理技能 (Agent Rules Engine)

本技能提供跨模型、跨 IDE 生态的 AI Agent 工程行为规约初始化、审计诊断与标准化治理编排。

```mermaid
flowchart LR
    S1["1. 环境与技术栈探查"] --> S2["2. 上下文预算与红线剪裁"]
    S2 --> S3["3. 规约生成与分层配置"]
    S3 --> S4["4. 多生态格式同步转译"]
    S4 --> S5["5. 规则健康度与冲突审计"]
```

## 执行流程状态机 (Execution State Machine)

### 阶段 1：环境与技术栈探查 (Environment Inspection)
- 探查当前工作区核心配置文件（如 `pom.xml`、`package.json`、`go.mod`、`pyproject.toml` 等）；
- 识别项目架构风格、测试框架、代码格式化工具及团队既有协作规范；
- 确认现有是否存在 `.cursorrules`、`CLAUDE.md`、`AGENTS.md` 等历史遗留规约；
- 分析既有代码提交历史中的常用提交前缀与协作者角色边界。

### 阶段 2：上下文预算与红线剪裁 (Context Pruning)
- 评估目标 Agent 模型窗口与注意力预算，遵循三层金字塔架构收敛规约体积；
- 严格确立“凭证零明文泄漏”、“Git 两级显式授权”与“最小破坏半径”三大安全红线；
- 结合多智能体协作网络定义各子 Agent 的职责分工与调用权限范围；
- 详细治理法则与防防御性约束参考 [提示词治理协议](./references/protocols/prompt-governance-protocol.md)。

### 阶段 3：规约生成与分层配置 (Rule Generation)
- 基于标准化骨架生成项目根目录 `AGENTS.md` 交付物；
- 针对项目专属领域技术栈（如空安全契约、异常处理、并发安全）注入定向约束；
- 为高频易错场景（如空集合返回、浮点数金额运算）设定确定性编码禁令；
- 标准规约结构与章节模板参考 [AGENTS.md 规范模板](./references/templates/agents-md-template.md)。

### 阶段 4：多生态格式同步转译 (Ecosystem Translation)
- 保持 `AGENTS.md` 作为项目主数据源（Single Source of Truth）；
- 按需生成或同步其他主流 AI 编码助手适配文件（如 `CLAUDE.md` 或 `.cursor/rules`）；
- 建立跨生态规约同源机制，避免多份规则文件出现逻辑脱节与漂移；
- 真实项目落地规约参考 [电商中台 Agent 规约样例](./examples/sample-agents-spec.md)。

### 阶段 5：规则健康度与冲突审计 (Health & Conflict Audit)
- 检查规约中是否包含本地物理路径或未转义反斜杠，保证跨平台通用性；
- 核验指令语义是否存在互斥冲突或过度冗余；
- 执行空安全契约与异常处理策略的形式化推演，消除歧义表达；
- 确认排版遵循盘古之白规范，中西文与数字保留半角空格。

## 质量控制与合规自检 (Quality Checklist)
- [ ] 规约中严禁包含任何环境专属物理绝对路径与私有绝对链接；
- [ ] 核心安全红线（Git 授权与凭据脱敏）具备明确的操作边界与判定准则；
- [ ] 针对核心技术栈声明了地道代码风格与模块化拆分边界准则；
- [ ] 规约文档严格控制在 Token 预算上限内，杜绝注意力涣散；
- [ ] 排版 100% 满足盘古之白规范与标准相对路径引用。

## 知识索引地图 (Knowledge Map)

| 知识模块 | 相对路径 | 核心内容说明 |
| :--- | :--- | :--- |
| 提示词治理协议 | `./references/protocols/prompt-governance-protocol.md` | 分层上下文预算、防御性约束与审计机制 |
| AGENTS 模板 | `./references/templates/agents-md-template.md` | 标准化项目工程规范与行为红线模板 |
| 实战案例样本 | `./examples/sample-agents-spec.md` | 电商交易微服务实战落地规约样本 |

## 交付成果规范 (Deliverables Benchmark)
- **主规约文件**：根目录下结构完整、防御清晰的 `AGENTS.md`；
- **生态衍生配置**：符合特定 IDE 工具链语法的映射文件；
- **测试夹具规范**：针对单测桩与 Mock 数据的使用边界声明；
- **自检核验单**：涵盖路径安全与指令冲突的核验报告；
- **沉浸式落地文档**：配套维护与演进指南说明。
