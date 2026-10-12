---
name: at-glossary
description: 当用户需要为工程项目建立、维护、查询或校验领域统一语言（GLOSSARY.md）、消除跨角色术语歧义、对齐代码实体与业务概念命名或大幅降低多轮沟通 Token 开销时使用此技能。提供 DDD 统一语言提炼、模糊重载词阻断纠偏、代码类与枚举一致性扫描，交付结构化领域字典资产。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - glossary
    - domain-driven-design
    - ubiquitous-language
    - terminology
  icon: book-alphabet
---

# 领域统一语言编排器 (Ubiquitous Language Orchestrator)

在工程根目录建立并动态维护唯一的领域通用字典（`GLOSSARY.md`），消弭“同词不同义”或“同义不同词”的语义污染。作为轻量化状态机运行，主动拦截口语化模糊表达，将业务概念、不变式规则与代码中的 Entity/Enum 强制对齐，显著削减 Agent 沟通冗余与上下文 Token 损耗。

## 渐进式知识地图 (Progressive Disclosure Map)

所有术语协议、字典模板与实战案例均存放于对应目录：
- **统一语言提炼协议**：[ubiquitous-language-protocol.md](references/protocols/ubiquitous-language-protocol.md)（三段式术语卡片、歧义词消歧规则、代码对齐与防膨胀门禁）
- **统一语言字典模板**：[glossary-template.md](references/templates/glossary-template.md)（子域分组、术语定义、约束规则与废弃词消歧表模板）
- **电商领域语言样例**：[sample-glossary.md](examples/sample-glossary.md)（交易订单、预占库存与仓配履约统一语言实战样例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：语境侦测与术语资产索引 (Context Detection & Glossary Indexing)

1. **根目录字典真理探查**：
   - 自动检测根目录是否存在 `GLOSSARY.md`（或模块内 `docs/glossary.md`）；
   - 若根目录存在 `CONTEXT-MAP.md`，依据上下文地图路由至各微服务子域字典；
   - 若已存在字典，立即索引既有术语定义与代码映射，作为本轮会话的唯一真理词汇源；
   - 若不存在，依据 [glossary-template.md](references/templates/glossary-template.md) 懒加载初始化字典骨架。
2. **业务子域划界与限界上下文 (Bounded Context)**：
   - 识别当前需求涉及的核心子域（如支付结算、仓配履约、用户鉴权）；
   - 明确术语的适用边界，防止跨子域概念强行混同；
   - 标定子域间防腐层（ACL）与术语映射关系。


### 阶段 2：模糊概念拦截与术语消歧锐化 (Ambiguity Interception & Sharpening)

依据 [ubiquitous-language-protocol.md](references/protocols/ubiquitous-language-protocol.md) 执行动态消歧拦截：
1. **口语化泛称主动阻断**：
   - 当用户或上游输入模糊词（如“用户”、“取消”、“退款”）时，立即暂停推演并提示消歧；
   - 锐化为精确法定术语（如将“用户”拆分为终端消费者 `Customer` 与平台商户 `Merchant`）；
   - **同义词别名归一化**：将口语别名（Alias）建立重定向索引，统一收口至法定主词条。
2. **规范三段式词条提取**：
   - **法定定义 (Definition)**：客观、精炼陈述核心业务内涵；
   - **边界约束与不变式 (Invariants)**：明确状态前置依赖与排他性业务规则；
   - **反例与澄清 (What it is NOT)**：明确它不是什么，与其他近似概念划清物理界线。

### 阶段 3：代码实体映射与反向冲突核验 (Code Mapping & Conflict Check)

1. **代码命名双向映射**：
   - 为每个领域术语绑定代码库中的核心承载载体（Entity、Value Object、Enum）；
   - 确保接口参数、数据库字段与术语英文标识（Canonical Term）严格对齐；
   - 排查模型穿透坏味道：严禁持久层物理字段反向污染领域语言术语。
2. **反向语义冲突核验**：
   - 扫描当前代码库，核查是否存在“代码命名与字典定义自相矛盾”的历史遗留问题；
   - 发现矛盾时向开发者主动发出预警，并在字典中建立“废弃词与消歧对照表”。

### 阶段 4：增量落盘维护与规范移交 (Inline Update & Pipeline Handoff)

1. **字典增量持久化落盘与审阅闸门**：
   - 新概念一旦达成共识，立即就地增量写入 `GLOSSARY.md`，严禁滞后批量积压；
   - 保持字典纯粹性：严格剔除底层数据库索引、中间件连接等技术实现细节；
   - **人机确认机制**：向用户展示新增或变更词条卡片，等待人类用户审阅确认；
   - 严格遵循盘古之白排版规范，全文档杜绝任何 `file:///` 或本地物理盘符泄漏。
2. **下游研发链路移交**：
   - 移交 `at-spec`：要求增量规格书直接引用 `GLOSSARY.md` 法定术语；
   - 移交 `at-tdd`：测试方法名与断言语义直接遵循统一语言命名规范；
   - 形成高凝聚力领域资产，赋能后续会话免除重复沟通解释；
   - 沉淀高价值无形资产，保障领域架构代际传承；
   - 筑牢业务建模基石，守护软件工程通用语义防腐层。


