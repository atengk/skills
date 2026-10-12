# 现代前端组件架构与状态机设计规约 (Component Architecture Protocol)

本规约系统规范了现代前端 UI 工程中的组件分层设计、受控模式、状态机驱动与单向数据流标准，旨在打造高可复用、高可测且解耦清晰的工业级前端架构。

---

## 目录 (Table of Contents)

- [1. 组件分层拓扑与职责解耦](#1-组件分层拓扑与职责解耦)
- [2. 受控与非受控组件设计标准](#2-受控与非受控组件设计标准)
- [3. 状态机驱动与消除布尔状态爆炸](#3-状态机驱动与消除布尔状态爆炸)
- [4. Props 下发与事件单向数据流](#4-props-下发与事件单向数据流)
- [5. 样式架构、设计 Token 与组件生命周期](#5-样式架构设计-token-与组件生命周期)

---

## 1. 组件分层拓扑与职责解耦

现代前端应用架构强制遵循三层组件拓扑：

```text
UI Component Hierarchy
├── 1. 基础展示型组件 (Presentational / Primitive Components)
│   └── 纯 UI 渲染、无业务网络请求、由 Props 驱动、极高复用度 (Button, Input, Modal, Badge)
├── 2. 业务领域组件 (Domain / Feature Components)
│   └── 包含特定业务语义的展示与局部交互 (UserAvatarCard, OrderStatusTag, CartItemRow)
└── 3. 页面容器与编排组件 (Container / Page Orchestrators)
    └── 负责路由参数提取、数据获取 (Data Fetching)、全局状态订阅与事件分发 (Pages, Views)
```

### 接入层薄层红线
- **展示组件纯粹性**：基础展示型组件严禁在内部发起网络请求或直接读取路由参数；
- **单一职责**：一个组件只负责一个清晰的交互或视觉单元，单个组件文件行数建议收敛在 200 行以内。

---

## 2. 受控与非受控组件设计标准

- **受控模式优先 (Controlled by Default)**：核心表单与交互组件（Input、Select、Switch、Modal）必须支持由父级通过 `value`/`modelValue` 与 `onChange`/`update:modelValue` 完全受控；
- **状态不自突变红线**：组件严禁直接突变（Mutate）外部传入的 Props 属性；状态变更必须通过事件（Event / Callback）向上发射通知父级处理；
- **无缝回退支持**：支持提供 `defaultValue` 以允许在简单场景下作为非受控组件使用。

---

## 3. 状态机驱动与消除布尔状态爆炸

在管理包含多种互斥状态的异步交互（如加载、错误、成功、空数据、重新提交）时，**坚决杜绝“布尔状态爆炸 (Boolean State Explosion)”**：

### 3.1 消除多布尔标志反模式
- 严禁在组件中平铺定义多个相互重叠的布尔标志：`isLoading`, `isError`, `isEmpty`, `isSuccess`；因为这可能导致出现 `isLoading=true && isError=true` 的非法不一致状态；
- 采用**显式离散状态机 (Finite State Machine)**：
  ```typescript
  type AsyncStatus = 'IDLE' | 'LOADING' | 'SUCCESS' | 'ERROR' | 'EMPTY';
  ```
- 任何时刻状态机处于且仅处于一个合法状态，从根本上消灭非法中间态。

---

## 4. Props 下发与事件单向数据流

- **严格 Props 类型与默认值契约**：使用 TypeScript 显式定义每一个 Prop 的类型与可选性；
- **防透传下钻 (Prop Drilling)**：当某个数据需要穿越 3 层以上无感知的中间组件时，使用轻量 Context / Provide-Inject 或状态管理 Store 进行解耦；
- **具名语义事件**：事件名称必须体现业务或交互意图（如 `onSelectionChange`、`onConfirm`），严禁使用含混的通用事件名。

---

## 5. 样式架构、设计 Token 与组件生命周期

- **设计 Token 驱动**：颜色、字体、间距、圆角与阴影必须绑定至全局 CSS Variables 设计变量，杜绝散落的硬编码像素（如 `padding: 13px; color: #3a2f1b;`）；
- **响应式与触摸安全区**：移动端组件必须考虑视口安全区域（`env(safe-area-inset-bottom)`），触摸目标尺寸（Touch Target）保证不小于 44×44px；
- **副作用清理**：组件销毁（Unmount）时必须清理所有挂载的定时器、`window` 事件监听器与尚未完成的网络请求，杜绝内存泄漏。
