---
name: at-frontend
description: 当用户需要设计现代前端 UI 组件架构、拆分展示与容器组件、消除多布尔状态爆炸、实现受控组件模式、落实 Web 无障碍访问 (a11y / WCAG 2.1 AA) 或规整设计 Token 与响应式适配时使用此技能。提供组件分层拓扑切分、状态机驱动建模、焦点捕获与键盘导航加固编排，交付高复用、高可测且包容普适的前端工程成果。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - frontend
    - component-architecture
    - accessibility
    - a11y
    - state-machine
    - design-tokens
  icon: layout
---

# 现代前端 UI 架构与无障碍工程编排器 (Frontend UI Architecture Orchestrator)

在前端用户界面工程中贯彻高内聚低耦合的分层架构与普适包容的无障碍规范。作为轻量化状态机运行，针对组件职责不清、多布尔状态爆炸、Props 深度透传、纯 div 模拟按钮以及视障/纯键盘用户不可访问等典型坏味道，编排从组件拓扑切分、状态机建模、受控事件流梳理、WCAG 2.1 AA 级无障碍焦点管理到设计 Token 绑定的全生命周期。

## 渐进式知识地图 (Progressive Disclosure Map)

所有组件设计规约、无障碍核对单与实操样例均存放于对应目录：
- **组件架构与状态机设计规约**：[component-architecture-protocol.md](references/protocols/component-architecture-protocol.md)（三层拓扑、受控模式、状态机消灭布尔爆炸与设计 Token）
- **Web 无障碍 (a11y) 审查核对单**：[a11y-accessibility-checklist.md](references/checklists/a11y-accessibility-checklist.md)（语义 HTML、全键盘导航、焦点捕获 Focus Trap、颜色对比度）
- **无障碍受控交互组件实操案例**：[sample-ui-engineering.md](examples/sample-ui-engineering.md)（受控模态弹窗、Focus Trap 焦点锁定、Esc 监听与 ARIA 规范实现案例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：组件拓扑切分与状态机建模 (Component Topology & State Machine Modeling)

1. **三层分层与职责边界划定**：
   - 严格区分“基础展示型纯组件 (Presentational)”与“页面编排容器 (Container)”；
   - 确保基础 UI 组件内无任何外部网络请求或硬编码业务逻辑，最大化组件跨场景复用能力；
   - 针对复杂交互单文件，控制在 200 行内，超过则按领域逻辑抽离子组件。
2. **消灭布尔爆炸与显式状态机建模**：
   - 审查代码中的 `isLoading`、`isError` 等重叠布尔变量，重构为互斥枚举状态集合；
   - 绘制状态迁移拓扑图，确保任何时刻组件仅处于单一明确状态，从根本上杜绝非法中间态。

### 阶段 2：受控模式设计与单向数据流梳理 (Controlled Props & Data Flow)

1. **受控组件 (Controlled by Default) 契约**：
   - 组件核心状态由外部 Props（`value` / `isOpen`）完全驱动，禁止在内部随意维护影子状态；
   - 严格遵循单向数据流原则，组件严禁突变 Props 传入的对象，通过具名回调事件向上发射变更；
   - 暴露合理的默认值（`defaultValue`），无缝兼容轻量非受控调用场景。
2. **消除深层 Props 钻取 (Prop Drilling)**：
   - 跨越 3 层以上的状态传递，合理采用 Context、Provide/Inject 或轻量原子状态解耦；
   - 使用 TypeScript 泛型精准定义 Props 与 Emits 签名，杜绝 `any` 侵蚀。

### 阶段 3：无障碍 (a11y) 与键盘导航交互筑牢 (Accessibility & Keyboard Navigation)

对照 [a11y-accessibility-checklist.md](references/checklists/a11y-accessibility-checklist.md) 落地 WCAG 2.1 AA 标准：
1. **语义化标签与 ARIA 属性补齐**：
   - 严禁使用带有 `onclick` 的 `div` 冒充按钮，强制使用原生 `<button>`；
   - 为折叠、下拉与弹窗控件配置 `aria-expanded`、`aria-modal` 与 `aria-labelledby`；
   - 为纯图标按钮添加 `aria-label`，动态变更区域挂载 `aria-live` 实时广播；
   - 审计正文颜色对比度，确保文本与背景对比度不低于 4.5:1。
2. **全键盘导航与焦点捕获 (Focus Trap)**：
   - 保留清晰可见的高对比度聚焦轮廓线（Focus Ring），严禁滥用 `outline: none`；
   - 弹窗浮层内实现 `Tab` / `Shift+Tab` 循环焦点锁定，并支持按 `Esc` 键快捷关闭与原位焦点还原；
   - 适配减弱动效偏好媒体查询（`prefers-reduced-motion`），照顾前庭敏感用户。

### 阶段 4：设计 Token 绑定与交付留置 (Design Tokens & Safe Delivery)

1. **样式 Token 化与响应式触摸防卫**：
   - 颜色、圆角、阴影与字体绑定至全局 CSS 变量（CSS Custom Properties），消灭硬编码像素；
   - 适配移动端视口安全区（Safe Area），保障可点击区域尺寸不小于 44×44px；
   - 组件卸载生命周期内严格执行事件监听与异步副作用的清理，防范内存泄露；
   - 规整组件单元测试与渲染快照，杜绝不必要的非受控闭包重复渲染。
2. **交付物审计与安全留置**：
   - 运行组件单元测试与渲染快照，确保 100% 绿灯通过；
   - 规整组件 Props 与 Slots 契约，防范向后兼容性破坏；
   - 审计组件属性契约完整性，沉淀组件库故事书 (Storybook) 规范；
   - 成果保留在工作区等待人类审查，未获显式指令绝不擅自提交；
   - 破除以凑合跑通为目的的脆弱前端拼接模式；
   - 让界面不仅美观高效，更具备普惠所有群体的人文温度与工业级健壮性；
   - 守卫前端工程的可复用性、类型安全性与长期可演进生命力。
