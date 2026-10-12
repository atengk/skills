---
name: at-handoff
description: 当会话即将超出上下文窗口、切换协作 Agent、从设计阶段转入编码阶段或需要跨会话无损保存当前断点现场与待办任务时使用此技能。提供深度上下文压缩协议与交接棒模板，交付高连续性长时自治协作体验。
disable-model-invocation: false
disable-slash-command: false
argument-hint: "[handoff|compact|context|resume]"
allowed-tools:
  - view_file
  - run_command
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags: [handoff, context-compaction, multi-agent, session-continuity, long-running]
---

# 跨会话上下文压缩与长时交接棒技能 (Context Handoff Engine)

本技能提供面向长对话上下文深度提炼、噪声剥离、断点现场保留与跨 Agent 无损接力的工程交接体系。

```mermaid
flowchart LR
    S1["1. 会话状态扫描与触发条件判定"] --> S2["2. 四象限信息提炼与噪声剥离"]
    S2 --> S3["3. 排他决策归纳与断点现场固化"]
    S3 --> S4["4. 待办拓扑编排与唤醒指令生成"]
    S4 --> S5["5. 交接棒文档持久化与自检交付"]
```

## 执行流程状态机 (Execution State Machine)

### 阶段 1：会话状态扫描与触发条件判定 (Session Scanning)
- 评估当前上下文深度与 Token 消耗，识别是否逼近上下文窗口极限；
- 识别研发阶段跃迁事件（如预研转编码、编码转验收、值班换班）；
- 探查当前工作区 Git 分支、未暂存修改与最近关键提交哈希；
- 触发时机标准参考 [跨会话上下文压缩协议](./references/protocols/context-compaction-protocol.md)。

### 阶段 2：四象限信息提炼与噪声剥离 (Four Quadrants Compaction)
- 严格遵循四象限模型提炼已交付成果、核心决策、当前断点与未完待办；
- 彻底剔除调试日志堆栈、已废弃的技术草稿与对话客套噪声；
- 提炼核心数据结构定义、配置文件路径与确定性接口参数；
- 提炼方法详见 [跨会话上下文压缩协议](./references/protocols/context-compaction-protocol.md)。

### 阶段 3：排他决策归纳与断点现场固化 (Decisions & Context)
- 重点记录已确立的架构决策及否决备选方案的核心技术原因，防止反复；
- 精确定位代码当前修改的文件路径、代码行号与待处理的逻辑边界；
- 固化本地运行所必需的依赖服务、端口配置与安全环境变量；
- 真实案例参考 [设计转编码交接实战样例](./examples/sample-handoff.md)。

### 阶段 4：待办拓扑编排与唤醒指令生成 (Todos & Wake-up Prompt)
- 按 P0/P1/P2 编排结构化任务清单，明确每个任务的预期交付物与推荐技能；
- 生成面向新会话的自解释“一键唤醒指令模板 (Copy & Paste Prompt)”；
- 提示词中显式携带上下文继承约束与工程规范基线，杜绝冷启动漂移；
- 模板骨架参考 [跨 Agent 交接棒文档模板](./references/templates/handoff-document-template.md)。

### 阶段 5：交接棒文档持久化与自检交付 (Persistence & Handoff Delivery)
- 将交接内容持久化写入受管交接文件（如 `HANDOFF.md`）；
- 严格审计交接文档，确保零真实机密泄漏，凭据均采用占位符；
- 校验文档盘古之白排版规范与相对路径引用的工程合规性。

## 质量控制与合规自检 (Quality Checklist)
- [ ] 严格剥离冗余的中间排错日志，提炼信息具备高度信息密度；
- [ ] 决策部分必须说明为何放弃备选方案，避免接棒 Agent 重复探索；
- [ ] 当前断点现场精确到具体文件和行号，并清晰说明当前工作树状态；
- [ ] 文档末尾提供即插即用的一键唤醒指令，支持新 Agent 毫秒级热启动；
- [ ] 全文严格遵循中西文盘古之白空格与零本地绝对路径泄漏红线。

## 知识索引地图 (Knowledge Map)

| 知识模块 | 相对路径 | 核心内容说明 |
| :--- | :--- | :--- |
| 上下文压缩协议 | `./references/protocols/context-compaction-protocol.md` | 四象限提炼模型、噪声剥离、断点恢复与持久化规范 |
| 交接棒模板 | `./references/templates/handoff-document-template.md` | 跨 Agent 结构化交接棒 Markdown 标准模板与唤醒指令 |
| 实战案例样本 | `./examples/sample-handoff.md` | 任务调度系统从设计转入编码阶段的真实交接棒样例 |

## 交付成果规范 (Deliverables Benchmark)
- **交接棒核心文档**：格式标准、信息结构化的 `HANDOFF.md` 文件；
- **排他性决策清单**：包含正反论证、防止重踩弯路的架构共识备忘录；
- **断点现场描述表**：包含活动分支、暂存修改与断点代码锚点的上下文快照；
- **优先级待办矩阵**：按依赖关系拓扑编排的后续行动项与验收标准；
- **一键唤醒提示词**：支持人类直接复制黏贴、新 Agent 即刻开工的指令块。
