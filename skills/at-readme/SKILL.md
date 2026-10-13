---
name: at-readme
description: 当用户需要为代码仓库编写、重构或持续同步项目核心门户 README.md、提炼项目价值主张、集成状态徽标 (Badges)、梳理架构拓扑图、编写开箱即用快速上手指南或规整目录配置字典时使用此技能。提供代码库特征扫描、模块拓扑抽取、极简快速启动验证与文档死链门禁编排，交付高清晰度、低心智负担且现代美观的工业级项目门户。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[generate|sync|audit]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - readme
    - project-portal
    - technical-writing
    - quickstart
    - architecture-diagram
  icon: book-open
---

# 项目核心门户与全景导航编排器 (Project README Orchestrator)

在代码仓库根目录构筑自解释、易导航且富有现代感的项目第一门面。作为轻量化状态机运行，拒绝大而无当的空洞叙述与滞后文档；针对新用户上手成本高、缺乏架构概览、启动命令不可运行及配置项模糊等痛点，编排从仓库特征深度摸排、一句话价值主张萃取、Mermaid 架构拓扑生成、开箱即用快速开始验证到目录与配置矩阵生成的全生命周期。

## 渐进式知识地图 (Progressive Disclosure Map)

所有门户设计模板、质量规约与开源案例均存放于对应目录：
- **项目门户标准模板**：[readme-standard-template.md](references/templates/readme-standard-template.md)（标头徽标区、特性卡片、架构拓扑、快速启动与配置字典模板）
- **README 质量标准与排版规约**：[readme-quality-protocol.md](references/protocols/readme-quality-protocol.md)（黄金 5 秒法则、Shields.io 徽标规范、一键可复制准则与零死链门禁）
- **工业级项目 README 案例**：[sample-project-readme.md](examples/sample-project-readme.md)（云原生网关完整 README 实战范例与多语言标头参考）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：仓库认知扫描与价值主张提炼 (Repository Scanning & Value Extraction)

1. **代码库技术栈与关键文件探查**：
   - 读取项目工程构建文件（`package.json`、`pom.xml`、`Cargo.toml`、`go.mod` 等），确认主语言与核心依赖；
   - 扫描现有目录拓扑与核心入口源码，定位主要业务领域；
   - 排查开源许可证协议与版权声明，确认合法合规基线；
   - 排查现有 `README.md`，分析存在的信息缺失、过期配置或陈旧链接。
2. **价值主张与核心杀手级特性凝练**：
   - 提炼一句富有穿透力的中英双语项目 Slogan（黄金 5 秒法则）；
   - 归纳 4~6 项最具代表性的核心特性亮点，强调业务与技术效能增量；
   - 配置与仓库真实状态绑定的 Shields.io 矢量风格状态徽标（CI 状态、最新版本、License 等）。

### 阶段 2：架构拓扑绘制与快速开始编排 (Architecture & Quickstart Synthesis)

1. **Mermaid 架构流程拓扑设计**：
   - 提取系统核心分层与数据流向，设计清晰易读的标准 Mermaid 架构图；
   - 节点文本显式双引号包裹，杜绝语法解析异常，保障主流代码托管平台原生渲染。
2. **开箱即用极简启动指令编排**：
   - 整理环境依赖版本基线（Node/Java/Python 等）；
   - 提供从 `git clone`、依赖安装、本地配置复制到启动开发服务器的极简命令；
   - 补充常见单元测试运行与生产制品构建命令说明（Test & Build）；
   - 在本地沙箱环境验证每条命令的准确性，确保一键可复制运行，无隐性踩坑点。

### 阶段 3：目录字典规整与配置矩阵构建 (Directory Layout & Configuration Matrix)

1. **物理目录树提炼与职责标注**：
   - 梳理仓库核心一级与二级物理目录，生成规范的 ASCII 目录树；
   - 清晰标注每一个核心目录的架构职责，指导新开发者快速建立心智模型；
   - 关联并对齐根目录协作生态文档（`CONTRIBUTING.md`、`CHANGELOG.md`、`LICENSE`）。
2. **核心配置项与环境变量矩阵**：
   - 抽取系统运行必需的关键配置项、默认值与含义说明，输出结构化 Markdown 表格；
   - 梳理常见快速排错 FAQ，降低新接触者踩坑几率；
   - 严格落实零机密原则，配置示例中所有敏感凭据统一采用通用占位符（如 `${DATABASE_URL}`）。


### 阶段 4：质量门禁校验与人机共识留置 (Quality Verification & Safe Delivery)

1. **全链路质量与死链自检**：
   - 依据 [readme-quality-protocol.md](references/protocols/readme-quality-protocol.md) 校验所有锚点与文件相对链接物理存在；
   - 校验盘古之白排版规范，确保中西文与数字间空格合规，文档内零物理绝对路径泄漏。
2. **成果呈现与工作区留置**：
   - 将生成的 `README.md` 落盘至仓库根目录；
   - 检查国际化多语言切换锚点（如 `README_EN.md`），保证导流顺畅；
   - 向用户汇报核心章节结构，等待人类审阅与进一步个性化微调；
   - 未获显式指令绝不擅自执行 Git 提交或推送；
   - 消除新贡献者面对陌生产业级代码时的迷茫与心智负担；
   - 塑造专业、高品质且值得信赖的开源与企业级工程门面；
   - 守卫项目核心文档与底层技术架构演进的持久对齐。

