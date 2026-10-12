---
name: at-simplify
description: 当用户面对深层条件嵌套、箭头反模式、过度工程设计、单实现伪抽象、晦涩复合布尔逻辑或需要对既有代码进行可读性极致精简时使用此技能。提供卫语句倒置重构、控制流扁平化、消除冗余间接层与等价性验证编排，交付心智负担最低、清晰度最高的干净代码。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - code-simplification
    - guard-clauses
    - cyclomatic-complexity
    - clean-code
    - occams-razor
  icon: scissors
---

# 代码极致精简与控制流扁平化编排器 (Code Simplification Orchestrator)

践行奥卡姆剃刀原则与“清晰胜过炫技”理念，消除代码中的无谓复杂性。作为轻量化状态机运行，针对深层条件嵌套、箭头反模式、单实现伪接口与晦涩长表达式，以卫语句提早返回、提取具名布尔变量与折叠无用间接层为核心手段，在单元测试全绿灯保护下实施严格等价的极简化重构，显著降低代码库心智负担。

## 渐进式知识地图 (Progressive Disclosure Map)

所有极简规约、复杂度检查单与对比案例均存放于对应目录：
- **极简主义与扁平化规约**：[code-simplification-rules.md](references/protocols/code-simplification-rules.md)（三层嵌套红线、卫语句倒置准则、YAGNI 治理与解释性变量提取）
- **复杂度审查核对单**：[simplicity-review-checklist.md](references/checklists/simplicity-review-checklist.md)（控制流嵌套、过度工程审查、双重否定排查与等价性保障）
- **精简前后实战对比案例**：[sample-before-after-simplification.md](examples/sample-before-after-simplification.md)（电商优惠券核销从 5 层嵌套重构为 1 层扁平卫语句案例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：复杂性异味扫描与测试安全网确认 (Smell Audit & Safety Net)

1. **圈复杂度与嵌套层级摸排**：
   - 扫描目标代码的嵌套深度，标识所有嵌套超过 3 层的分支结构；
   - 排查箭头反模式（多层 `if-else` 向右倾斜）、悬挂 `else` 块与深层循环；
   - 对照 [simplicity-review-checklist.md](references/checklists/simplicity-review-checklist.md) 梳理精简靶心清单；
   - 梳理拟精简代码的公共契约边界，防范向后兼容性破坏。
2. **测试安全网前置确认**：
   - 检查目标代码对应的单元测试用例，确认既有测试全部处于绿灯状态；
   - 若测试覆盖不足，优先补充特征测试锁定既有输入输出行为；
   - 严禁在无自动化测试防护的情况下展开任何控制流重组。

### 阶段 2：卫语句倒置与控制流扁平化重组 (Flattening & Guard Clauses)

1. **倒置条件与提早返回**：
   - 将深层嵌套中的异常检查与边界条件提升至函数顶部，构建自解释卫语句；
   - 不满足前置条件时立即 `return` 或抛出语义化异常，彻底消除外层 `else` 块；
   - 将核心成功路径顶格左对齐展开，确保方法主逻辑一览无余；
   - 消除嵌套三元表达式，拆解多级条件赋值为扁平分支。
2. **循环体过滤扁平化**：
   - 在复杂循环体顶部采用 `if (!isValid) continue;` 提早跳过无关项；
   - 将循环体内部逻辑深度严格收敛至 1 级以内。

### 阶段 3：消除过度工程与布尔降噪 (De-complexification & De-noising)

1. **剔除投机性过度抽象**：
   - 遵循 [code-simplification-rules.md](references/protocols/code-simplification-rules.md)；
   - 折叠系统中仅有单一实现的伪接口与工厂，将紧密内聚的私有小逻辑合并在文件内；
   - 移除毫无信息增量的空心包装透传层，缩短调用链路。
2. **布尔表达式自解释重构**：
   - 将超过 2 个逻辑操作符的复杂判断条件拆解为肯定式语义变量；
   - 消除所有的双重否定命名，杜绝反直觉的心智消耗；
   - 统一参数默认值与空安全防卫策略，消除形式主义防御过当。


### 阶段 4：等价性全量回归与极简交付 (Equivalence Verification & Delivery)

1. **单测全量回归与零破坏保障**：
   - 运行全量单元测试套件，确认 100% 绿灯且所有断言与重构前严格等价；
   - 确认无未预期的返回值突变或异常类型篡改；
   - 比对重构前后的分支覆盖率，确认关键路径无遗漏。
2. **最小 Diff 审查与交付**：
   - 审查 Git Diff，确保仅改动控制流结构，未引入大面积无关代码格式化；
   - 呈现精简前后的圈复杂度对比与代码行数压缩收益；
   - 成果保留在工作区供人类复核，未获显式指令绝不擅自提交；
   - 彻底破除炫技心理，让代码成为团队无障碍阅读的活体资产；
   - 显著降低后续人员维护与排错的心智负担；
   - 守卫系统代码的长期精炼、敏捷与可演进性。

