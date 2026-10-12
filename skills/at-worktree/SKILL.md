---
name: at-worktree
description: 当用户需要利用 Git Worktree 进行物理级独立环境隔离、并发开发新特性、进行破坏性试验或切出紧急热修以防污染当前工作区时使用此技能。提供跨平台工作树创建、环境依赖初始化、测试基线绿灯核验与安全清理闭环编排，交付零污染、物理隔离且自闭环的工程工作空间。
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - git-worktree
    - physical-isolation
    - multi-tasking
    - baseline-testing
    - clean-environment
  icon: git-branch
---

# Git Worktree 物理环境多任务隔离编排器 (Git Worktree Orchestrator)

在物理文件系统层面构建完全独立且自闭环的 Git 工作树开发环境。作为轻量化状态机运行，支持在不干扰当前工作区未暂存修改的前提下，安全切出并行特性分支或热修任务，编排从路径决策、工作树创建、依赖与配置同步、初始测试基线核验到完工合并清理的全生命周期。

## 渐进式知识地图 (Progressive Disclosure Map)

所有工作树隔离规约、就绪检查单与端到端案例均存放于对应目录：
- **工作树隔离与生命周期协议**：[worktree-management-protocol.md](references/protocols/worktree-management-protocol.md)（目录拓扑、分支复用防护、环境初始化契约、清理收尾标准与跨平台避坑）
- **基线核验与就绪检查单**：[baseline-verification-checklist.md](references/checklists/baseline-verification-checklist.md)（物理路径、配置与依赖、测试绿灯基线、清理回收自检表）
- **工作树实战演练案例**：[sample-worktree-workflow.md](examples/sample-worktree-workflow.md)（突发热修环境隔离、基线核验、特性交付与收尾回显实战案例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：工作区状态摸排与隔离拓扑决策 (Probe & Topology Decision)

1. **当前工作区状态探查**：
   - 运行 `git status` 与 `git branch --show-current`，记录当前分支与未提交改动；
   - 评估当前工作区脏改动风险，确认无需使用高风险的 `git stash`，决议采用物理工作树隔离；
   - 探查待开发分支名称与基准提交点（默认以最新主干为基线）；
   - 梳理目标任务所需环境变量、配置文件与端口分配需求。
2. **同级物理路径规划**：
   - 遵循 [worktree-management-protocol.md](references/protocols/worktree-management-protocol.md) 规约；
   - 在主仓库同级目录规划 `<repo-name>-worktrees/<branch-name>` 容器路径，杜绝内部嵌套；
   - 校验物理磁盘空间与操作系统路径限制，防范 Windows 长路径溢出；
   - 核验目标分支是否已在其他工作树被检出，防范 Git 分支并发检出冲突。


### 阶段 2：物理工作树创建与环境对齐 (Creation & Environment Alignment)

1. **工作树原子创建**：
   - 执行 `git worktree add -b <new-branch> <target-path> <base-ref>` 建立独立工作树；
   - 验证物理目录生成完整性与 `.git` 指针文件关联有效性。
2. **本地配置与依赖同步**：
   - 从主工作区安全拷贝必要的本地配置文件（如 `.env.local`），确保敏感凭据占位防护；
   - 切换工作目录至新工作树，执行锁定版本的依赖安装（如 `npm ci` 或 `poetry install`）；
   - 核验本地服务端口配置，确保不与主工作区发生端口冲突。

### 阶段 3：测试基线核验与开发准入 (Baseline Verification & Readiness)

对照 [baseline-verification-checklist.md](references/checklists/baseline-verification-checklist.md) 执行前置准入：
1. **测试基线全量绿灯核验**：
   - 在新工作树中运行全量单元测试与语法检查；
   - 确认基准分支切出状态 100% 绿灯无回归，记录初始用例基线；
   - 若基线测试失败，立即阻断后续特性开发，提示用户优先修复基线或调整基准分支；
2. **交付隔离就绪状态**：
   - 向用户汇报工作树已物理就绪，提供清晰的路径说明与分支基线信息；
   - 保持终端环境定位在隔离工作树中，准备开展原子特性开发。

### 阶段 4：特性交付、收尾清理与工作区复位 (Delivery, Cleanup & Reset)

1. **特性开发验证与原子提交**：
   - 在隔离工作树内实施特性开发，保障新增单测与全量回归 100% 绿灯；
   - 规范提交工作树代码，将成果保留在分支或推送到远端；
2. **资源安全回收与主工作区复位**：
   - 终端工作目录安全切回主仓库根目录；
   - 执行 `git worktree remove` 安全移除隔离工作树，运行 `git worktree prune` 修剪游离元数据；
   - 核验主仓库未暂存改动完好无损，确保整个生命周期零污染、零数据丢失；
   - 成果留置于工作区供人类复核，未获用户显式指令严禁擅自合并或推送主干；
   - 杜绝多任务上下文混杂与未暂存代码被 stash 冲刷的丢失风险；
   - 赋能并行任务研发与破坏性实验的物理零成本快速试错；
   - 筑牢开发环境隔离防线，守卫主干代码库的稳定与纯粹。

