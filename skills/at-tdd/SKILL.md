---
name: at-tdd
description: 当用户需要通过测试驱动开发（TDD）实现新功能、修复缺陷、实施红-绿-重构循环、拦截假通过测试或执行突变检验时使用此技能。提供未测先写立即删代码铁律、测试先行红灯验证、最小实现绿灯与突变敏感度反思，交付生产级健壮源码与自验证测试套件。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[red|green|refactor|mutation]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - tdd
    - testing
    - refactoring
    - mutation-testing
  icon: test-tube
---

# 测试驱动开发编排器 (Test-Driven Development Orchestrator)

将原子任务与业务契约转化为严格遵循“红 -> 绿 -> 重构”纪律的高质量源码与测试资产。作为轻量化状态机运行，强制执行“未测先写立即删代码”铁律，并在绿灯后嵌入突变检验（Mutation Testing）反思，根除假通过测试与虚假覆盖率。

## 渐进式知识地图 (Progressive Disclosure Map)

所有测试执行协议、突变反思机制与反模式清单均存放于对应目录：
- **红绿重构执行协议**：[tdd-red-green-protocol.md](references/protocols/tdd-red-green-protocol.md)（删代码铁律、公开接缝定位、垂直切片与最小实现准则）
- **突变检验反思协议**：[mutation-testing-protocol.md](references/protocols/mutation-testing-protocol.md)（突变杀死率、四大经典突变算子与思维实验突变法）
- **单测反模式拦截清单**：[testing-anti-patterns.md](references/anti-patterns/testing-anti-patterns.md)（重言式测试、假通过盲目绿灯与脆弱时序拦截）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：公开接缝锁定与红灯测试先行 (Red Phase & Seam Locking)

1. **公开接缝 (Public Seam) 严格限定**：
   - 识别当前切片的公开接缝（API 端点、Service 接口公共方法）；
   - **接缝保护红线**：严禁直接测试私有方法（Private Methods），严禁通过反射穿透私有字段；
   - 检查任务是否涉及存量代码，若未测先写了业务代码，**立即强制物理删除**！
2. **编写红灯用例 (RED)**：
   - 依据前序契约或原子微任务编写单个公开接口测试用例；
   - 遵循 Given-When-Then 结构，期望值必须来自独立的权威真理，杜绝重言式自我计算；
   - 参照 [testing-anti-patterns.md](references/anti-patterns/testing-anti-patterns.md) 拦截盲目通过与无断言坏味道；
   - 确保测试夹具环境完全隔离，严禁污染共享静态变量或既有数据库数据。
3. **真实运行测试命令**：
   - 在终端实际运行单测指令；**多模块中必须使用模块裁剪参数执行（如 `-pl` / `--filter`），严禁 `cd` 切换目录或裸跑全工程**；
   - 必须在控制台真实见证红灯（Failure），并确认失败原因确实是“能力缺失”，而非语法导入或编译错误。

### 阶段 2：克制编码与最小实现绿灯 (Green Phase & Minimal Implementation)

依据 [tdd-red-green-protocol.md](references/protocols/tdd-red-green-protocol.md) 推进绿灯：
1. **编写最小实现代码**：
   - 只编写刚好足以让该红灯单测通过的生产代码；
   - 坚决杜绝过度设计、猜测性扩展参数或提前编写未来分支；
   - 保持克制，优先返回直接满足断言的紧凑实现。
2. **重新运行验证命令**：
   - 执行单测指令，亲眼见证测试状态由红变绿（Pass/Green）；
   - 退出码必须为 0，且无任何警告或异常残留。

### 阶段 3：突变敏感度反思与假通过防御 (Mutation Reflection)

绿灯达成后，强制激活 [mutation-testing-protocol.md](references/protocols/mutation-testing-protocol.md) 门禁：
1. **思维突变反思**：
   - 自省：“如果我把刚才写的核心判断条件反转（`>` 改为 `<=`），当前测试用例会立即报错吗？”
   - 检查断言是否仅校验了非空（NotNull），而漏掉了具体的关键字段值。
2. **探针验证与突变体清除**：
   - 若存在疑虑，就地注入边界突变体；
   - 确认测试能够敏锐捕捉并杀死突变体后，立即恢复代码为正确绿灯版本。

### 阶段 4：局部安全重构与状态打卡 (Refactor Phase & Task Checkout)

1. **受控重构 (REFACTOR)**：
   - 在所有测试持续绿灯的安全网庇护下，消除硬编码魔法值、提炼自解释私有函数、优化变量命名；
   - 遵循单一职责与最小改动范围原则，保持 Git Diff 干净最小；
   - 重构完毕后再次运行全量测试套件，确保无破坏性回归。
2. **状态打卡与下游移交**：
   - 回写 `tasks.md`，将当前微任务状态由 `- [ ]` 标记为 `- [x]`；
   - 全部任务完成后，引导进入 `at-review` 开展双轴代码质量体检；
   - 若排查到意外顽固缺陷，推荐唤起 `at-diagnose` 开展系统化排错；
   - 恪守红绿铁律，打造高韧性自验证代码资产；
   - 正文严格遵循盘古之白排版规范，全流程杜绝本地绝对路径泄漏。


