# Ateng Skills

[![CI](https://github.com/atengk/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/atengk/skills/actions)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Open Agent Skills](https://img.shields.io/badge/Standard-Open_Agent_Skills-success.svg)](https://agent-plugins.org)

专注研发效能与架构设计的实用 AI Agent 技能与插件库。

开箱即用，让你的 AI 编程助手（Cursor、Claude Code、Antigravity、Codex、Windsurf 等）具备工业级架构设计、API 契约编写、数据库建模与技术方案交付能力。

---

## 🛠️ 技能清单 (Skills Catalog)

### 📌 `at-tech-doc`：工业级技术文档与架构设计生成器

将业务构想或现有代码库转化为具备生产落地深度的交付级技术文档。支持逆向工程与前瞻设计，内置自适应三层交付模型与真实性核验闸门。

- **斜杠命令**：`/at-tech-doc`
- **支持场景与模板**：
  - 📐 **系统/特性设计方案 (RFC)**：背景边界、选型对比、架构拓扑、详细设计、发布与回滚
  - 🔌 **API 接口契约规范 (API Spec)**：RESTful 规范、请求响应报文、错误码、幂等与安全防护
  - 🗄️ **数据库设计与数据字典 (DB Design)**：容量预估、ER 关系、物理数据字典、索引规划
  - 🔬 **技术选型调研报告 (Tech Spike)**：评估准入、候选方案对比、原型压测实测、加权决策矩阵
  - 📋 **架构决策记录 (ADR)**：决策上下文、方案权衡、产生后果与影响
  - 🚨 **运维部署与应急手册 (Ops Guide)**：服务依赖、部署排错、高频告警处置 SOP、服务降级
  - 🔄 **割接迁移方案 (Migration Guide)**：割接演练、双写平滑过渡、数据对齐核对、灰度切流
  - 🧪 **联调契约与压测方案 (Test Plan)**：环境依赖、边界测试用例、全链路压测指标、性能瓶颈排查

#### 💬 典型使用示例

只需在你的 AI 客户端输入自然语言即可触发：

> - *“帮我设计一个订单分布式幂等防重的 API 接口契约”*
> - *“为用户中心微服务重构编写一份特性设计方案 (RFC)”*
> - *“对比 Redis 与本地缓存构建二级缓存体系，写一份技术选型 Spike 报告”*
> - *“分析现有订单模块代码，逆向生成数据库设计与数据字典”*

---

## 🚀 快速上手与集成指南 (Getting Started)

本仓库的技能均为自闭环结构，你可以根据使用习惯自由选择以下任意方式：

### 方式 1：单独在任意项目中引入单个技能（推荐）

直接将所需技能拷贝至目标项目的 Agent 技能目录即可生效：

```bash
# 拷贝至当前项目的通用 Agent 技能目录
mkdir -p .agents/skills
cp -r path/to/skills/at-tech-doc .agents/skills/
```

- **适用客户端**：Cursor、Claude Code、Codex、Windsurf 等；
- **即刻生效**：放置后，AI 助手在处理相关任务时会自动识别并按需激活。

### 方式 2：通过 Agent Skills CLI 一键添加

```bash
# 从 GitHub 仓库直接安装单个技能
npx skills add atengk/skills/skills/at-tech-doc
```

### 方式 3：作为完整插件集成 (Antigravity)

将本项目克隆至 Antigravity 插件目录，享受插件级生命周期管理：

```bash
git clone https://github.com/atengk/skills.git ~/.gemini/config/plugins/ateng-skills
```

---

## 📦 项目结构 (Repository Layout)

```text
skills/
├── .github/                  # GitHub Actions CI 自动化流水线
├── AGENTS.md                 # 国际开放 Agent 研发工程规范与跨生态准则
├── plugin.json               # 插件元数据描述清单
├── scripts/                  # 自动化工程工具链 (零外部依赖)
│   ├── _common.py            # 底层终端引擎、YAML 状态机与 Markdown 扫描器
│   ├── init_skill.py         # 新技能脚手架生成器
│   ├── format_skills.py      # 盘古之白与排版自动修复器 (支持 --check)
│   ├── validate.py           # DoD 质量门禁校验器
│   └── package_skill.py      # 单技能打包导出器 (.skill 制品)
├── skills/                   # 核心技能集合
│   └── at-tech-doc/          # 技术文档与架构设计生成器
│       ├── SKILL.md          # 核心编排指令入口
│       └── references/       # 深度协议与标准化模板库
└── README.md
```

---

## ➕ 技能开发与维护工具链 (Developer Toolchain)

本仓库内置全套基于 Python 标准库的零依赖工程工具：

1. **一键生成新技能脚手架**：
   ```bash
   python scripts/init_skill.py at-<skill-name>
   ```
   自动生成微内核物理拓扑、合规 Frontmatter 模板与 `references/` 骨架文件。
2. **编写核心指令与参考资料**：在 `SKILL.md` 编写核心状态机编排，在 `references/` 下组织协议与模板。
3. **一键格式化与排版修复 (盘古之白)**：
   ```bash
   python scripts/format_skills.py
   # 仅检查不修改（适用于 CI 门禁）：python scripts/format_skills.py --check
   ```
   自动为中英文、数字边界补齐半角空格并优化 Markdown 排版。
4. **运行质量门禁全量自检**：
   ```bash
   python scripts/validate.py
   ```
   严格核验 Frontmatter 格式、相对路径死链、目录纯粹性与绝对路径安全。
5. **打包导出独立 `.skill` 制品 (可选)**：
   ```bash
   python scripts/package_skill.py skills/at-<skill-name>
   # 或批量打包全库：python scripts/package_skill.py --all
   ```

---

## 📄 开源许可证 (License)

本项目基于 [Apache-2.0](LICENSE) 许可证开源。
