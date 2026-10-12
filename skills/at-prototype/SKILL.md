---
name: at-prototype
description: 当用户面对复杂状态机分支、模糊交互流、未决架构方案或需要构建快速抛弃型探针以极低成本验证技术假设时使用此技能。提供极简单文件自闭环原型构建、实时状态监视器集成、假设证明与决策反哺编排，交付用完即弃且零污染的探索性验证成果。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - prototype
    - throwaway-prototype
    - sandbox
    - state-machine
    - exploratory-spike
  icon: flask
---

# 抛弃型原型沙箱探针编排器 (Throwaway Prototype Orchestrator)

在生产代码之外以最小代价构建自闭环的抛弃型实验探针。作为轻量化状态机运行，贯彻抛弃型不变量（Throwaway Invariant），严禁在原型阶段追求生产级健壮性与复杂工程包袱；聚焦核心待验假设，通过单文件无构建的极简交互模型与实时状态探针，帮助开发者快速证明或证伪方案可行性，并将经验沉淀为正式规格。

## 渐进式知识地图 (Progressive Disclosure Map)

所有原型开发规约、单文件模板与交互案例均存放于对应目录：
- **抛弃型原型协议与规约**：[throwaway-prototype-protocol.md](references/protocols/throwaway-prototype-protocol.md)（抛弃型不变量、激进范围裁剪、状态可视化面板与非生产防线）
- **单文件原型自闭环模板**：[prototype-html-template.md](references/templates/prototype-html-template.md)（零构建开箱即用 HTML、双栏交互布局与实时状态探针模板）
- **状态机原型实操演练案例**：[sample-prototype.md](examples/sample-prototype.md)（异步支付轮询状态机探针、竞态条件消除与结论沉淀案例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：假设萃取与范围极端收敛 (Hypothesis & Extreme Scoping)

1. **核心待验假设锚定**：
   - 质询用户或深入待决需求，提炼出 1~2 个最关键的未决问题（如“状态迁移是否自洽”或“API 链式手感是否自然”）；
   - 严禁模糊探索，确保原型具有非真即假的明确验证目标；
   - 梳理待模拟的外部服务交互与竞态场景，锁定验证靶心；
   - 评估探针技术栈形态（Web 交互流选用单 HTML，后端算法选用单文件脚本）。
2. **激进范围裁剪**：
   - 遵循 [throwaway-prototype-protocol.md](references/protocols/throwaway-prototype-protocol.md)；
   - 砍掉所有鉴权、持久化数据库、复杂表单校验与非关键视觉装饰；
   - 采用纯内存模拟或静态 Mock 数据替代外部真实依赖，确保零构建负担；
   - 坚决杜绝在原型阶段过度设计，一切以回答核心问题为唯一指引。

### 阶段 2：单文件原型探针自闭环构建 (Probe Implementation)

1. **单文件技术闭环**：
   - 基于 [prototype-html-template.md](references/templates/prototype-html-template.md) 生成单文件；
   - 将所有样式、骨架与状态流转脚本内联于单一文件中，确保双击即可在浏览器原生运行；
   - 预置常用测试数据集与便捷触发场景，极大降低测试输入成本；
   - 强制在文件头部嵌入不可用于生产的警告标识。
2. **集成实时状态监视器 (State Inspector)**：
   - 页面右侧内嵌实时状态数据面板，每一步交互动作透明回显内部状态对象快照；
   - 暴露关键重置与快进调试按钮，极大提升人工测试验证效率；
   - 确保代码落盘于隔离沙箱或临时目录，严禁写入生产代码树（如 `src/`）。


### 阶段 3：人机交互实测与关键决策提炼 (Interactive Verification & Decision)

1. **引导实机交互与反馈收集**：
   - 向用户呈现生成的原型文件相对路径，提示用户在本地浏览器中双击打开体验；
   - 引导用户重点测试边界条件（如网络超时、并发快速点击、状态冲突）；
   - **强制停止工具调用**：向用户展示原型运行指引并等待用户反馈实测感受与决策倾向。
2. **假设验证与决策形成**：
   - 汇总验证结果，判定既定假设是否成立，记录意外发现的边界陷阱；
   - 形成清晰的架构决策结论（采纳方案 A/B、调整状态流转规则等）；
   - 评估交互心智负担与性能响应平滑度，锁定最终演进方向。


### 阶段 4：成果反哺设计与环境安全回收 (Feedback & Safe Reclamation)

1. **反哺正式规格与架构资产**：
   - 将验证沉淀的正确状态机模型与边界处理结论，反哺至 `at-spec` 规格说明或 `at-adr` 架构决策记录；
   - 指导后续生产代码严格依照测试驱动与深度模块规范重新编写；
2. **沙箱回收与零污染防线**：
   - 提醒用户或自动归档清理临时原型文件，杜绝将原型代码直接合并入主干；
   - 确保代码库零脏文件残留，维护生产资产的严密性与纯粹性；
   - 破除在模糊设计上过度投入重度工程实现的资源浪费沉没成本；
   - 赋予团队在低成本沙箱中敏捷验证天马行空创意的自由度；
   - 构筑从快速直观试错到严谨工程落地的确定性桥梁。
