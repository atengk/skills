---
name: at-contributing
description: 当用户需要为开源或企业级项目制定贡献指南 CONTRIBUTING.md、定义分支协同工作流、确立 Conventional Commits 规范化提交约定、拟定代码审查准则或设置 PR 准入质量核对单时使用此技能。提供项目环境基线抽取、提交规范映射、PR 模板构建与贡献者守则编排，交付清晰严密、无歧义且协作阻力最小的工程贡献体系。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[guide|workflow|conventions]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - contributing
    - conventional-commits
    - git-workflow
    - pull-request
    - code-of-conduct
  icon: users
---

# 开源贡献指南与协作规范编排器 (Contributing Guide Orchestrator)

在开源社区与企业团队中建立顺畅、透明且高质量的代码协作纽带。作为轻量化状态机运行，针对新贡献者不知如何搭建环境、提交信息格式混乱、分支管理随意以及 PR 准入缺乏共识等协作壁垒，编排从项目构建命令探测、Conventional Commits 提交约定确立、分支协同策略制定到 PR 自动化门禁清单生成的全生命周期。

## 渐进式知识地图 (Progressive Disclosure Map)

所有贡献指南模板、提交协议与开源协作案例均存放于对应目录：
- **开源贡献指南标准模板**：[contributing-template.md](references/templates/contributing-template.md)（行为准则、开发环境准备、分支流程与 PR 准入检查单）
- **规范化提交与分支协议**：[conventional-commits-protocol.md](references/protocols/conventional-commits-protocol.md)（Conventional Commits 1.0.0 语法、Type/Scope 规范与分支命名）
- **工业级贡献指南实战案例**：[sample-contributing-guide.md](examples/sample-contributing-guide.md)（基础设施库 CONTRIBUTING.md 完整范例与红线标准）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：协作模型摸排与环境基线提取 (Collaboration Model & Environment Probing)

1. **项目构建与质量命令探测**：
   - 审查工程构建描述文件，识别依赖安装（`install`）、单测执行（`test`）与代码检查（`lint`）核心命令；
   - 提炼最低运行时环境要求（如 Node.js、Java、Rust、Go 版本）；
   - 梳理推荐的编辑器插件与本地调试配置建议，降低新环境搭建门槛；
   - 梳理本地开发环境搭建的确定性步骤，杜绝隐性环境假设。
2. **开源行为准则与版权协议确认**：
   - 引入 Contributor Covenant 开源行为守则（Code of Conduct）；
   - 明确所有提交物默认遵循项目根目录的开源许可证协议（LICENSE），保障知识产权清晰。

### 阶段 2：规范化提交与分支策略确立 (Commit Conventions & Branching Strategy)

1. **Conventional Commits 规范落地**：
   - 遵循 [conventional-commits-protocol.md](references/protocols/conventional-commits-protocol.md)；
   - 确立 `feat`、`fix`、`docs`、`refactor`、`perf`、`test`、`ci` 等标准类型使用边界；
   - 强调原子化提交（Atomic Commits）原则，单次提交仅聚焦单一业务或技术动作；
   - 明确 Breaking Change 破坏性变更的感叹号语法与 Footer 声明，防范版本隐性破坏。
2. **分支管理模型与命名规则**：
   - 依据团队规模选定分支模型（主干开发 Trunk-Based 或特性分支模型）；
   - 统一特性分支（`feat/`）与缺陷修复分支（`fix/`）的具名格式，禁止混乱无序分支漫延；
   - 强调精准路径暂存纪律，严禁使用全量通配符暂存无关改动。

### 阶段 3：代码审查与 PR 准入检查单构建 (Code Review & PR Gate Checklist)

1. **单测覆盖率与质量红线设定**：
   - 明确新增业务特性的自动化单元测试覆盖率门槛；
   - 确立代码静态扫描（Lint / Typecheck）0 告警与测试套件 100% 绿灯的前置阻断红线；
   - 规范同行代码评审（Peer Review）流程，要求至少 1 位 Maintainer 核准后方可合入；
   - 强调代码极简原则与奥卡姆剃刀，拒绝炫技与无边界过度工程。
2. **PR 准入检查单 (PR Checklist) 编制**：
   - 制定开箱即用的 PR 检查清单模板（代码已 rebase 主干、测试通过、文档同步）；
   - 强调零敏感机密泄漏与环境变量占位符使用准则。


### 阶段 4：规范文档落地与人机共识留置 (Document Delivery & Safe Retention)

1. **CONTRIBUTING.md 生成与目录对齐**：
   - 基于 [contributing-template.md](references/templates/contributing-template.md) 生成规范文件并落盘至仓库根目录；
   - 在 `README.md` 中建立对 `CONTRIBUTING.md` 的导航直链，形成文档生态自闭环；
   - 执行盘古之白排版与物理相对链接校验，确保 100% 零死链、零绝对路径泄漏。
2. **成果呈现与工作区留置**：
   - 向用户汇报贡献指南核心规约，等待人类审阅；
   - 建立贡献者鸣谢机制（Contributors List），激发开源协作热情；
   - 未获显式指令绝不擅自执行 Git 提交或推送；
   - 消除团队内部与外部贡献者的认知分歧与协作摩擦；
   - 保障代码库历史 Git 提交记录整洁美观且具备机器可解析性；
   - 赋能项目建立专业、包容且高效的现代开源工程协作文化。

