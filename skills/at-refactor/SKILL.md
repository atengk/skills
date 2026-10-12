---
name: at-refactor
description: 当用户需要治理系统架构坏味道、剥离历史上帝类、设计深度模块接口、消除依恋情结与散弹式修改、防范代码过度碎片化或实施受控微重构时使用此技能。提供深度模块设计哲学与双安全网微步进工序编排，交付高内聚、低耦合且最小爆炸半径的重构落地成果。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - refactoring
    - deep-module-design
    - architecture-smell
    - clean-code
    - modularization
  icon: refresh-cw
---

# 深度模块架构演进与微重构编排器 (Refactor & Deep Module Orchestrator)

将复杂臃肿的历史代码与系统坏味道演进为高内聚、低心智负担的工业级深度模块。作为轻量化状态机运行，贯彻 John Ousterhout 深度模块设计哲学（浅接口深实现、高信息隐藏、杜绝过度碎片化），提供从异味诊断、新模块缝隙设计、双安全网测试构建到原子微重构步进的端到端受控演进基石。

## 渐进式知识地图 (Progressive Disclosure Map)

所有重构设计准则、交付模板与异味清单均存放于对应目录：
- **深度模块演进协议**：[deep-module-design-protocol.md](references/protocols/deep-module-design-protocol.md)（深模块哲学、浅接口深实现、信息隐藏、防过度碎片化与双安全网微步进原则）
- **架构重构方案模板**：[refactor-plan-template.md](references/templates/refactor-plan-template.md)（元数据头、异味诊断、目标深度模块接口设计、微步骤执行清单与验收标准）
- **架构异味自检清单**：[architecture-smell-checklist.md](references/checklists/architecture-smell-checklist.md)（上帝类、浅模块、过度碎片化、依恋情结、散弹式修改自检与治理对照表）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：坏味道诊断与存量基线摸排 (Smell Diagnosis & Baseline Probe)

1. **架构异味定位与爆炸半径评估**：
   - 对照 [architecture-smell-checklist.md](references/checklists/architecture-smell-checklist.md) 识别存量核心瓶颈；
   - 排查上帝类膨胀、接口过于浅显、形式主义微文件泛滥或散弹式修改等典型异味；
   - 探查存量代码的圈复杂度（Cyclomatic Complexity）与模块耦合度指标；
   - 梳理目标模块的依赖拓扑与调用方分布，评估改动爆炸半径，圈定受影响边界。
2. **第一安全网（存量基线回归网）核验**：
   - 探查存量代码的自动化测试覆盖率，确认既有测试全部处于绿灯状态；
   - 若存量测试薄弱或缺失，优先补充端到端行为特征测试（Characterization Tests），锁定既有正确行为；
   - 严禁在无安全网防护的前提下展开任何破坏性代码重组。

### 阶段 2：深度模块接口与隐藏信息设计 (Deep Module Seam Design)

依据 [deep-module-design-protocol.md](references/protocols/deep-module-design-protocol.md) 确立目标设计：
1. **浅接口设计 (Simple Interface)**：提炼富有概括力的高层语义接口，大幅减少对外暴露的方法数与参数数量；
2. **厚实现封装 (Deep Implementation)**：
   - 将复杂的内部细节（并发锁、持久化缓存、多步骤事务、重试降级）完整隐藏在模块实现内部；
   - 杜绝向调用方泄露底层实现异常或专有内部数据结构；
   - 确保外部公共 API 签名的向后兼容性，防止下游调用方联动改动；
3. **警惕过度碎片化防御**：
   - 坚守高内聚原则，严禁形式主义微文件拆分；
   - 仅供模块内部使用的轻量私有逻辑统一在文件内部内聚闭环，坚决杜绝把简单代码拆成迷宫。

### 阶段 3：方案人机评审与双安全网筑牢 (Review Gate & Second Safety Net)

依据 [refactor-plan-template.md](references/templates/refactor-plan-template.md) 落地重构方案：
1. **重构方案呈现与共识达成**：
   - 展示目标深度接口草案、预期隐藏信息点与分批微步骤拆解；
   - **强制停止工具调用**：向用户呈现重构方案明细，提供直达链接，等待用户审阅与确认；
   - 确保正文严格遵循盘古之白排版规范，全文档杜绝任何 `file:///` 或本地物理盘符泄漏。
2. **第二安全网（新契约单测网）先置**：
   - 在新深度模块编码前，依据新接口预先编写高覆盖测试用例（契约测试）；
   - 确立测试驱动的验证靶心，保障重构后的深度模块自闭环。

### 阶段 4：原子微步进重构与最小 Diff 交付 (Atomic Refactoring & Delivery)

1. **增量绞杀与微步快跑 (Strangler Micro-steps)**：
   - 遵循最小变更原则，每一次微步动作保持原子化（新建模块 -> 补齐实现 -> 增量委托 -> 移除死代码）；
   - 每一个微步完成后立即运行测试验证，严禁累积大面积未验证改动；
   - 面对存量大文件，采用外拆委托模式，严禁全量推倒重写引发 Git 冲突风暴；
2. **全量回归核验与安全留置**：
   - 运行工程全量测试套件，确认 100% 绿灯无回退；
   - 比对重构前后的圈复杂度与文件结构清晰度，量化重构收益；
   - 审计 Git Diff，确保无无关格式化或无关文件污染；
   - 所有成果留置于工作区供人类复核，未获用户显式指令严禁自主提交或推送；
   - 消除架构腐化与暗坑，显著降低新功能迭代的心智负担；
   - 促进团队形成高内聚、深模块的优秀工程文化；
   - 筑牢代码库可维护性与演进生命力，守卫架构长青。
