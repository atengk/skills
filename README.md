# Ateng Skills

跨生态通用的 AI Agent 研发效能与技术架构设计技能库 (Universal Agent Skills & Plugins)。

遵循国际开放 **[Agent Skills Specification](https://agent-plugins.org)** 与 **[Agent Plugins Specification](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)** 标准。坚决杜绝任何厂商私有锁定（Zero Vendor Lock-in），原生通用支持 **Claude Code / Desktop、Cursor、Codex、Windsurf、Antigravity、OpenClaw / Vercel Skills** 等全套主流 Agent 生态。

---

## 🌟 核心设计原则 (Design Principles)

- **自包含微内核 (Self-Contained Microkernel)**：每个技能目录均为物理自闭环的原子单元。所有指导协议、模板、手册均内聚于各自私有 `references/` 中，零外部路径隐式依赖。
- **开放中立标准 (Vendor-Neutral by Design)**：代码与文档纯粹采用标准 GitHub Flavored Markdown 与 Mermaid 语法，杜绝专有宿主 API 绑定。
- **双重消费形态 (Dual Consumption Modes)**：既可作为符合 `agent-plugins.org` 规范的完整插件包整体分发，又支持单摘任意单个技能直接拷贝进项目使用。

---

## 📦 项目结构 (Repository Structure)

```text
skills/
├── plugin.json               # 开放插件元数据清单 (遵循 agent-plugins.org 标准)
├── skills/                   # 核心技能集合 (自包含微内核)
│   └── at-tech-doc/          # 工业级技术文档编排生成器
│       ├── SKILL.md          # 技能主指令文件 (YAML Frontmatter + 指南)
│       └── references/       # 渐进式知识地图、执行协议与标准化模板
│           ├── formatting-rules.md
│           ├── protocols/
│           └── templates/
└── README.md
```

---

## 🛠️ 收录技能清单 (Skills Catalog)

| 技能名称 (Slash Command) | 标识符 / 目录 | 核心职责说明 |
| :--- | :--- | :--- |
| `/at-tech-doc` | `skills/at-tech-doc` | 生成工业级技术方案（RFC）、API 接口契约、ADR 架构决策、运维应急手册、技术调研 Spike、数据库设计与字典、割接方案等，内置三层自适应交付模型与真理核验闸门。 |

> **命名空间规范**：本项目所有技能统一遵循 `at-` 轻量前缀命名（取自 Ateng），彻底防止与社区公共技能发生同名冲突与静默覆盖。在支持斜杠命令的客户端中输入 `/at-` 即可快速聚合唤出专属能力。

---

## 🚀 跨生态接入与使用指南 (Universal Usage)

### 1. 单独提取单个技能使用 (推荐，任意项目通用)

无需安装整个插件包，直接将所需技能拷贝至任何工程中：

```bash
# 拷贝至当前项目的通用 Agent 技能目录
mkdir -p .agents/skills
cp -r path/to/skills/at-tech-doc .agents/skills/
```

- **兼容客户端**：Cursor、Claude Code、Windsurf、Codex、OpenClaw。
- **即刻生效**：由于技能是“自包含微内核”，放入 `.agents/skills/` 后，你的 AI 编码助手将自动识别并在需要时激活它。

### 2. 通过开放 Skills CLI 动态安装

```bash
# 使用标准 Agent Skills CLI 从 GitHub 直接安装单个技能
npx skills add atengk/skills/skills/at-tech-doc
```

### 3. 作为完整插件包整体安装 (Antigravity / 支持 Agent Plugins 的环境)

适用于需要一键批量管理全套技能、享受插件级生命周期控制的环境：
- 将本项目放置或克隆到对应环境的插件扫描目录（如 `~/.gemini/config/plugins/ateng-skills`）。
- 运行时将自动加载插件所暴露的全部子技能。

---

## ➕ 如何增量新增技能 (Contributing New Skills)

1. 在 `skills/` 下新建原子子目录，以 `at-<skill-name>` 命名：
   ```text
   skills/at-my-new-skill/
   ├── SKILL.md
   └── references/           # 放置该技能专用的模板或参考文档（可选）
   ```
2. 编写 `SKILL.md`，头部声明开放标准的 YAML Frontmatter：
   ```yaml
   ---
   name: at-my-new-skill
   description: 清晰陈述该技能的核心功能与第三人称触发场景（供 Agent 语义路由或用户通过 /at-my-new-skill 触发）。
   ---

   # 技能说明与操作指导正文
   ```
3. 遵循自包含红线：文档内互链 100% 采用相对路径（`./` 或 `../`），严禁跨技能建立文件引用。

---

## 📄 开源许可证 (License)

本项目基于 [Apache-2.0](LICENSE) 许可证开源。
