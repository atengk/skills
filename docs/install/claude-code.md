# Claude Code 官方环境插件与配置指南

本文档指导开发者在 Anthropic Claude Code 终端命令行客户端与相关集成环境中接入、配置、验证与升级 `atengk/skills` 全生命周期软件工程技能库。

---

## 1. 生态背景与兼容性说明

Claude Code 是 Anthropic 推出的现代 Agentic 命令行开发工具，具备强大的多轮文件编辑、代码架构分析与终端指令执行能力。本项目技能库严格遵循 Open Agent Skills 国际标准，与 Claude Code 的原生插件及命令扩展机制 100% 兼容：
- **微内核协议规范**：每个技能均提供合法的 YAML Frontmatter 与三级渐进式披露主干，单技能初始路由仅占用极低 Token 开销；
- **自然语言与斜杠命令统一映射**：在 Claude Code 终端中可无缝通过 `/at-workflow`、`/at-plan`、`/at-tdd` 触发技能，亦可通过自然语言陈述意图由 Claude 自主调度；
- **双向规则协同**：原生兼容 `CLAUDE.md` 与本库顶层 `AGENTS.md`，实现工程规约自动化注入。

---

## 2. 插件安装与环境挂载方式

### 2.1 方式一：Claude Code 插件注册表安装 (推荐)

Claude Code 支持通过插件指令从远程仓库直接加载插件包：

```bash
# 从 GitHub 仓库添加技能插件
claude plugin add https://github.com/atengk/skills

# 查看当前加载的插件列表
claude plugin list
```

### 2.2 方式二：本地仓库目录挂载 (贡献者与内网开发者)

若您在本地检出了 `atengk/skills` 代码仓库：

```bash
# 在本地克隆仓库
git clone https://github.com/atengk/skills.git
cd skills

# 挂载本地技能插件目录
claude plugin add .
```

也可以通过设置 Claude Code 配置文件 `~/.claude/config.json`，在 `plugins` 列表中加入技能包路径：

```json
{
  "plugins": [
    {
      "name": "ateng-skills",
      "path": "/path/to/skills"
    }
  ]
}
```

### 2.3 方式三：项目级 CLAUDE.md 规则与技能桥接

若您在已有业务项目中协作，可通过在项目根目录的 `CLAUDE.md` 中引用技能库规则，实现无缝协同：

```markdown
# 项目级工程规约 (CLAUDE.md)

本仓库遵循国际开放 Agent 工程规范与全生命周期技能库：
- 复杂需求与架构质询：请主动调度 `at-grill` 技能收敛边界；
- 编码实现阶段：严格执行 `at-tdd` 测试驱动开发三步循环；
- 架构重构与复杂度压降：遵循 `at-refactor` 与 `at-simplify` 规范；
- 跨会话长任务接力：在切换会话前必须调用 `at-handoff` 沉淀交接备忘录。
```

---

## 3. 技能调度与多模态触发机制

Claude Code 支持两种主要调度方式：

### 3.1 显式斜杠命令调用 (Slash Commands)
在 Claude Code 提示符后直接输入命令及其参数：

```bash
# 启动全局工作流意图向导
> /at-workflow menu

# 针对特定需求进行反向质询压力测试
> /at-grill 用户订单超时未支付自动关单与库存回滚需求

# 启动测试驱动开发
> /at-tdd 编写基于 Redis 分布式锁的库存扣减服务
```

### 3.2 自然语言意图自动唤醒 (Natural Language Invocation)
Claude Code 的语义路由引擎会实时扫描已索引技能的 `description`。当您输入自然语言业务诉求时，模型会自动激活对应技能：

```text
开发者：“我们线上偶发超卖缺陷，不知道怎么复现，请帮我梳理根因排查步骤。”
Claude Code：“检测到线上紧急排错诉求，正在激活 at-diagnose（假设驱动根因排查技能）与 at-workflow 热修流水线...”
```

---

## 4. 首轮连通性验证与操作示范

安装完成后，在终端启动 Claude Code 会话进行三道健康检查：

```bash
# 启动 Claude Code
claude
```

### 4.1 检查一：查看技能帮助与五段式卡片
输入帮助指令验证解析通道：

```text
/at-workflow help at-spec
```

**预期效果**：Claude Code 输出 `at-spec` 技能的定位、触发场景、输入契约、输出规格文件结构与伴随手册超链接。

### 4.2 检查二：执行轻量工作流意图诊断
输入路由向导指令：

```text
/at-workflow menu
```

**预期效果**：输出 5 大核心流水线选择菜单，并在您选择后生成清晰的 Mermaid 执行拓扑图。

### 4.3 检查三：测试驱动开发守护验证
测试让 Claude Code 为一个简单函数编写单测：

```text
/at-tdd 编写一个字符串下划线转驼峰的工具函数
```

**预期效果**：Claude Code 严格服从红灯测试先行原则，首先创建失败的单元测试并执行，确认红灯后再补充业务实现转为绿灯。

---

## 5. 常见排错与注意事项 (FAQ)

### 5.1 提示权限未被授权 (Permission Denied)
Claude Code 默认会对写文件与终端命令执行进行确认提示。在处理大规模重构或自动化门禁时，您可以在启动参数中开启自动批准模式（如在受信任的沙箱环境中运行）：

```bash
# 开启非交互自动执行（请确保环境安全）
claude --dangerously-skip-permissions
```

### 5.2 如何更新技能库版本
```bash
# 更新远程插件至最新 commit
claude plugin update ateng-skills
```

---

## 6. 相关资源与延伸阅读

- [Google Antigravity 原生环境插件与技能配置指南](./antigravity.md)
- [基于 npx skills CLI 的跨端通用分发指南](./open-skills-cli.md)
- [配方 2：线上紧急缺陷排查与热修复流](../workflows/02-hotfix-debugging.md)
