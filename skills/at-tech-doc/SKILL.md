---
name: at-tech-doc
description: 当用户需要编写或生成工业级技术文档、系统架构设计方案、特性 RFC、API 接口契约、数据库设计与数据字典、技术调研 Spike、运维应急手册、割接迁移方案或联调压测方案时使用此技能。支持基于代码库的逆向工程与正向前瞻设计，内置自适应三层交付模型（Tier 1/2/3）与跨轮次交互分批协议。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[rfc|arch|tier1|tier2|tier3]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - architecture
    - rfc
    - api-spec
    - tech-doc
  icon: document-edit
---

# 技术文档编排与生成器 (Tech Doc Orchestrator)

将用户的业务构想或现有代码库转化为具备生产落地深度的交付级技术文档。作为轻量化编排引擎运行，采用渐进式披露、自适应三层交付体系及严格的防技术虚构硬性闸门。

## 渐进式知识地图 (Progressive Disclosure Map)

所有详细执行协议、排版基准与文档模板均存放于 `references/` 目录：
- **执行与分批协议**：[batching.md](references/protocols/batching.md)（Tier 3 跨轮次交互分批纪律与状态看板）
- **真理与事实核验**：[verification.md](references/protocols/verification.md)（双源探针机制、防虚构矩阵与离线降级预警）
- **排版与可视化规范**：[formatting-rules.md](references/formatting-rules.md)（盘古之白、Mermaid 防御语法、零绝对路径红线）
- **标准化文档模板**：
  - 系统/特性设计方案 (RFC)：[rfc-template.md](references/templates/rfc-template.md)
  - API 接口契约规范：[api-spec-template.md](references/templates/api-spec-template.md)
  - 架构决策记录 (ADR)：[adr-template.md](references/templates/adr-template.md)
  - 运维部署与应急手册：[ops-guide-template.md](references/templates/ops-guide-template.md)
  - 技术选型调研与 PoC 报告：[tech-spike-template.md](references/templates/tech-spike-template.md)
  - 数据库设计与数据字典：[db-design-template.md](references/templates/db-design-template.md)
  - 割接迁移与重构方案：[migration-guide-template.md](references/templates/migration-guide-template.md)
  - 联调契约与性能压测方案：[test-plan-template.md](references/templates/test-plan-template.md)

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：需求接入、运行模式判定与层级自适应路由

1. **运行模式识别 (Operating Mode Detection)**：
   - **逆向工程模式 (Reverse Mode)**：基于本地代码库分析（Controller、Entity、DDL、配置文件等）。本地源码为唯一真理之源（Ground Truth），严禁联网搜索臆造私有业务。
   - **前瞻设计模式 (Forward Mode)**：全新架构设计、技术选型或组件引入。凡涉及外部依赖、框架配置、版本生命周期（LTS/EOL）及 GAV 坐标，必须调用搜索探针核实官方依据。
   - *协议引用*：执行前必须查阅 [verification.md](references/protocols/verification.md)。
2. **自适应层级路由 (Adaptive Tier Routing)**：
   - **Tier 1 (轻量速记，$\le 150$ 行)**：适用于简单单点 ADR、单一 API 契约补全，或显式传入 `--tier=1` / `--quick`。
   - **Tier 2 (标准规范，150~500 行)**：适用于标准特性 RFC、技术调研 Spike、单服务数据库设计，或显式传入 `--tier=2` / `--single-pass`。
   - **Tier 3 (史诗套件/多文件模块，$> 500$ 行)**：适用于跨服务复杂架构方案、全景文档套件或大型重构，或显式传入 `--tier=3` / `--batch`。
3. **模板匹配**：从 `references/templates/` 目录加载对应的标准化模板。

### 阶段 2：方案规划与人机确认闸门 (Planning & Human Approval Gate)

1. **落盘路径决策**：默认写入规范的技术文档交付目录（如工程 `docs/` 或会话指定交付区），严禁直接在工作区根目录随意平铺；严格遵守工程目录隔离规范。
2. **分层规划呈现**：
   - **Tier 1**：免除规划握手；直接在单轮对话中生成精炼大纲并完成文档落盘。
   - **Tier 2**：呈现详尽的三级大纲树及单批次交付计划。**必须暂停并等待用户审阅确认**。
   - **Tier 3**：呈现完整的 7 步方案（目标路径、模块化组织形态、层级推荐、带技术要点的三级大纲树、批次进度看板、信源依据、Mermaid 规划拓扑）。**多文档套件（文件数 $> 1$）必须在交付目录根部规划全局导航文件（默认 `README.md`，文档站点使用 `index.md`）并在批次 1 首发交付；同时明确参考文献收敛形式（末篇尾部追加或独立顺延文件），前序各业务文档严禁规划文末参考资料章节**。**必须暂停并等待用户审阅确认**。
3. **大纲优先纠偏**：若用户提出范围或大纲调整，必须优先在计划中就地修正并重新核对，确认通过后方可动笔撰写正文。

### 阶段 3：执行与交付纪律 (Synthesis & Execution Protocols)

方案确认通过后，根据锁定的 Tier 层级推进执行：
- **严格遵循大纲**：绝对严禁擅自删减、合并或漂移已获确认的章节与参数。
- **Tier 1 与 Tier 2 执行**：在单轮次中一次性生成符合 [formatting-rules.md](references/formatting-rules.md) 的完整文档。
- **Tier 3 执行**：严格执行 [batching.md](references/protocols/batching.md) 协议：
  1. **批次 1 首发全局导航门面**：多文档套件批次 1 优先落盘 `README.md` / `index.md`（包含架构全景拓扑、交付模块导航表格、阅读路线、全局离线警示及事实核查导流），为后续细分业务文档确立顶层视图。
  2. 检查方案看板当前激活光标。
  3. 仅写入当前批次对应的文件/章节。
  4. 将看板当前批次标记为 `[▶] 待验收`。
  5. **强制停止工具调用 (MANDATORY TURN-YIELDING)**：立即停止调用任何工具，退出本轮发言，在对话框中提供可直达的文件链接（或相对路径超链接）并引导用户审阅。
  6. 严禁偷跑下一批次，直到用户回复确认且当前批次标记为 `[✓] 已验收`。

### 阶段 4：质量自检与验收标准 (Quality Self-Inspection & Delivery)

1. **排版与元数据**：作者固定为 `@author Ateng`，日期为当天真实日期 `@since YYYY-MM-DD`，严格遵循中英文半角空格（盘古之白）。
2. **Mermaid 语法防御**：含特殊字符（如括号、斜杠、中文标点）的节点标签必须使用双引号包裹；时序图开启 `autonumber` 与生命周期激活。
3. **防虚构核验与参考文献收敛**：严格遵循 [verification.md](references/protocols/verification.md) 与 [formatting-rules.md](references/formatting-rules.md)：
   - **单文档交付 ($= 1$)**：文末附带权威信源核查矩阵。
   - **多文档套件 ($> 1$)**：
     - **全局导航文件**：交付目录根部必须包含 `README.md`（或 `index.md`），承载全景拓扑、模块导航矩阵与阅读路线；网络受限警示 `> [!CAUTION]` 仅在此处顶部声明一次。
     - **参考文献收敛**：前序各业务文档（`01` 至倒数第二篇）严禁出现文末参考文献章节，仅正文使用行内超链接；全套件事实依据核查矩阵统一收口于最后一篇业务文档的末尾章节（默认）或顺延编号的独立参考文档（$\ge 4$ 篇或独立附录规划），并在导航文件表格中明确标注锚点直达。
4. **零绝对路径红线**：严禁在 Markdown 正文中出现 `file:///`、`C:/` 或 `D:/`；文档间互链统一使用标准相对路径（`./`、`../`），外部信源使用标准 HTTPS URL。
