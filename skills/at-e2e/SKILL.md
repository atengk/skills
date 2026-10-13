---
name: at-e2e
description: 当用户需要设计端到端自动化测试、编写 Playwright 或 Cypress 验收脚本、执行核心用户旅程冒烟测试或通过浏览器探针验证 UI 与网络接口联调时使用此技能。提供现代化 E2E 验收协议与套件模板，交付高确定性全链路质量保证。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[journey|playwright|smoke]"
allowed-tools:
  - view_file
  - run_command
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags: [e2e, testing, playwright, browser-automation, user-journey]
---

# 端到端自动化验收与用户旅程验证技能 (E2E Acceptance Engine)

本技能提供面向真实用户行为路径、无头浏览器驱动与网络接口联调的端到端（E2E）全链路自动化验收体系。

```mermaid
flowchart LR
    S1["1. 用户旅程与关键路径梳理"] --> S2["2. 页面对象抽象与环境准备"]
    S2 --> S3["3. 测试套件编写与确定性等待"]
    S3 --> S4["4. 失败诊断与 Trace 轨迹留痕"]
    S4 --> S5["5. CI 流水线集成与门禁交付"]
```

## 执行流程状态机 (Execution State Machine)

### 阶段 1：用户旅程与关键路径梳理 (Journey Mapping)
- 提取系统高价值核心业务路径（Happy Path）与阻断性异常分支；
- 识别涉及的跨页面流转、外部服务调用与异步网络交互节点；
- 明确测试用例的验收标准（Acceptance Criteria）与冒烟优先级；
- 详尽分级标准参考 [端到端测试验收协议](./references/protocols/e2e-testing-protocol.md)。

### 阶段 2：页面对象抽象与环境准备 (POM & Fixtures)
- 基于页面对象模型（POM）封装高内聚的组件选择器与用户业务操作；
- 编排测试运行沙箱与环境上下文，配置无状态的身份凭据与会话注入；
- 确立测试数据隔离机制，杜绝测试用例之间的状态污染与执行序依赖；
- 套件骨架参考 [自动化测试套件模板](./references/templates/e2e-suite-template.md)。

### 阶段 3：测试套件编写与确定性等待 (Suite & Waiting)
- 编写清晰、可维护的自动化测试脚本，优先使用语义化无障碍定位器；
- 坚决杜绝硬编码休眠（Arbitrary Sleep），采用接口响应与 DOM 事件驱动等待；
- 覆盖表单校验、数据流转、异步通知及网络异常降级等关键交互；
- 实战完整用例参考 [全链路验收案例样本](./examples/sample-e2e-test.md)。

### 阶段 4：失败诊断与 Trace 轨迹留痕 (Trace & Triage)
- 配置失败自动现场保留机制，采集视口截图与多媒体操作录像；
- 启用全链路 Trace 轨迹录制，分析网络请求时序、控制台报错与 DOM 快照；
- 区分应用逻辑缺陷与环境偶发抖动，落实指数退避重试与用例防脆弱调优；
- 诊断流程深度规则参考 [端到端测试验收协议](./references/protocols/e2e-testing-protocol.md)。

### 阶段 5：CI 流水线集成与门禁交付 (CI Gate & Reporting)
- 配置无头（Headless）浏览器在 CI 容器中的跨平台执行策略；
- 产出结构化 HTML 测试报告与机器可读的 JUnit/JSON 验收汇总；
- 将核心旅程冒烟测试挂载为主分支合并与发版上线的前置必选卡点；
- 校验交付物中中西文排版空格与相对路径引用的工程合规性。

## 质量控制与合规自检 (Quality Checklist)
- [ ] 严禁在测试代码中写入固定等待休眠，必须全部采用事件驱动显式等待；
- [ ] 页面选择器严格遵循高优先级语义定位，避免使用脆弱的 CSS 深层路径；
- [ ] 测试用例之间保持绝对无状态，支持任意顺序独立执行与并行化并发；
- [ ] 失败用例具备自动截图与全量 Trace 留痕能力，排错信息自闭环；
- [ ] 所有文档与代码满足盘古之白中西文排版与零绝对路径规范。

## 知识索引地图 (Knowledge Map)

| 知识模块 | 相对路径 | 核心内容说明 |
| :--- | :--- | :--- |
| 端到端测试协议 | `./references/protocols/e2e-testing-protocol.md` | 用户旅程分级、定位器优先级与 Trace 留痕体系 |
| 测试套件模板 | `./references/templates/e2e-suite-template.md` | Playwright POM 模式与自动化测试套件代码模板 |
| 实战案例样本 | `./examples/sample-e2e-test.md` | 多租户管理全生命周期自动化验收实战样例 |

## 交付成果规范 (Deliverables Benchmark)
- **页面对象定义**：封装良好、职责清晰的 Page Object 模型代码；
- **验收测试套件**：涵盖 P0 黄金路径与关键异常分支的自动化测试脚本；
- **执行配置文件**：包含重试策略、Trace 收集与并发控制的运行配置；
- **端到端测试报告**：可视化测试通过率、执行耗时与失败追溯证据包；
- **CI 门禁配置脚本**：集成至持续集成流水线的自动化执行步骤定义。
