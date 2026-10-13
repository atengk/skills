---
name: at-review
description: 当用户需要对代码变更（Git Diff、PR、分支或特性提交）进行全面质量审查、检查规范违规与代码坏味道、核验需求规格（Spec）契约完成度或评估五轴健康度时使用此技能。提供 Standards 与 Spec 双轴并行隔离审查、Fowler 坏味道基线体检与五轴健康雷达评估，交付结构化双轴审查报告。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[dual-axis|spec|standards]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - code-review
    - standards
    - spec-verification
    - quality-gate
  icon: git-pull-request
---

# 代码双轴与五轴健康审查编排器 (Code Review Orchestrator)

对 Git 变更集开展正交双轴（Standards 规范轴 + Spec 契约轴）并行隔离审查，并辅以五轴全景健康度雷达体检。作为轻量化状态机运行，通过独立的子代理并行评估，杜绝规范与需求相互掩盖，输出严密分级的审查报告并收敛至特性工件目录。

## 渐进式知识地图 (Progressive Disclosure Map)

所有审查协议、报告模板与坏味道核查基线均存放于对应目录：
- **双轴审查执行协议**：[dual-axis-review-protocol.md](references/protocols/dual-axis-review-protocol.md)（双轴正交隔离、并行派发机制、五轴健康模型与阻断分级标准）
- **审查报告交付模板**：[review-report-template.md](references/templates/review-report-template.md)（元数据头、双轴结论并置、健康雷达与阻断项清单模板）
- **坏味道核查基线清单**：[code-smell-checklist.md](references/checklists/code-smell-checklist.md)（Fowler 十二大经典坏味道与现代工程安全规范）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：锚点标定与 Diff 范围锁定 (Fixed Point & Diff Scoping)

1. **确定比对锚点 (Fixed Point)**：
   - 提取用户指定的 Commit SHA、分支名（如 `main`、`develop`）或 Tag；
   - 若未提供，自动探查当前分支与主干的合并基线：`git merge-base origin/main HEAD`；
   - 校验锚点有效性：执行 `git rev-parse <fixed-point>` 确认引用存在，防止无效 Ref 导致空跑。
2. **提取物理差异与熔断防御**：
   - 执行三点 Diff：`git diff <fixed-point>...HEAD`，提取变更文件列表与提交日志；
   - **空 Diff 熔断**：若无任何代码改动，直接退出并提示用户无需审查。

### 阶段 2：双信源探查与准备 (Standards & Spec Sources Probe)

依据 [dual-axis-review-protocol.md](references/protocols/dual-axis-review-protocol.md) 准备两个轴的真理信源：
1. **Standards 轴信源准备**：
   - 索引仓库编码规约（`AGENTS.md`、`CODING_STANDARDS.md`）；
   - 装载 [code-smell-checklist.md](references/checklists/code-smell-checklist.md) 中的 Fowler 经典坏味道与空安全契约；
   - 优先服从仓库显式明文规约，仓库规约优于基线坏味道。
2. **Spec 轴信源准备**：
   - 检索关联特性规格（提交信息引用的 Issue `#ID`、`.specs/<feature-slug>/delta.md` 或 RFC 方案）；
   - 若无显式 Spec，在 Spec 轴显式标记为“未提供规格，仅审查自解释意图”。

### 阶段 3：双轴并行隔离审查派发 (Parallel Two-Axis Dispatch)

严禁在单一上下文中混淆两个轴的注意力，采用隔离子代理或隔离阶段推演：
1. **Standards 轴独立推演**：
   - 审查代码是否违背仓库编码规范；
   - 逐处扫描神秘命名、重复代码、依恋情结、循环内 SQL 查询与未防护绝对路径；
   - **多模块依赖拓扑防腐**：核验模块依赖有向无环图，严禁底层契约模块反向依赖业务实现模块，违者标记为 🔴 Blocker；
   - 区分“硬性规约违背”与“启发式坏味道建议”，严禁越界评判需求是否合理。
2. **Spec 轴独立推演**：
   - 严格对照需求契约，审查是否有“遗漏未实现的要求”；
   - 审查是否存在“未被要求的范围蔓延 (Scope Creep)”；
   - 审查已有实现是否与规格意图存在逻辑偏差，严禁纠缠命名排版细节。

### 阶段 4：双轴并置汇编与五轴健康雷达 (Report Aggregation & Five-Axis Radar)

依据 [review-report-template.md](references/templates/review-report-template.md) 汇编最终报告：
1. **双轴并置呈现与落盘**：
   - 严禁加权平均或相互抵消，保持 Standards 与 Spec 双栏独立展示；
   - 默认将审查报告落盘至特性工件目录 `.specs/<feature-slug>/review.md`（或会话指定交付区），严禁在根目录平铺。
2. **五轴健康雷达度量**：对契约正确性、可维护性、安全性、性能效率、测试健壮度进行分级打分。
3. **问题分级与移交裁决**：
   - 明确标注 🔴 Blocker、🟠 Major、🟡 Minor、⚪ Nit；
   - 包含 Blocker 时判定为 `REQUEST_CHANGES` 并引导调用 `at-tdd` 补充修复；
   - 若发现难以解释的隐蔽缺陷，引导调用 `at-diagnose` 逆向排查；
   - **交互确认闸门**：向用户呈现双轴审查核心摘要，等待人类用户最终决断；
   - 全项合规时判定为 `APPROVED`，推荐准备合流或提交代码；
   - 正文严格遵循盘古之白排版规范，全文档杜绝任何本地绝对路径泄漏。
