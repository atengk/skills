---
name: at-changelog
description: 当用户需要从 Git 提交历史自动提取变更日志、维护根目录 CHANGELOG.md、遵循 Keep a Changelog 规范分类 (Added/Changed/Fixed/Security 等)、解析 Conventional Commits 或评估 SemVer 语义化版本号升级时使用此技能。提供 Git 提交增量差分检索、工程杂音过滤、版本递增判定与发布对比超链接生成编排，交付清晰严谨、面向用户的版本演进日志。
disable-model-invocation: true
disable-slash-command: false
argument-hint: "[generate|unreleased|preview]"
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - changelog
    - keep-a-changelog
    - semver
    - git-history
    - release-notes
  icon: list
---

# 变更日志自动化提取与维护编排器 (Changelog Orchestrator)

在软件版本演进与发布生命周期中提供严谨、机器可解析且面向用户的变更说明。作为轻量化状态机运行，拒绝手工拼凑日志带来的遗漏与格式混乱；针对 Git 提交历史杂音多、破坏性变更未标明、版本号随意递增等痛点，编排从 Git Tag 增量日志差分提取、杂音过滤清洗、Conventional Commits 映射、SemVer 语义版本决策到 CHANGELOG.md 增量追加落盘的全生命周期。

## 渐进式知识地图 (Progressive Disclosure Map)

所有日志模板、提取协议与多版本实战案例均存放于对应目录：
- **Keep a Changelog 标准模板**：[changelog-template.md](references/templates/changelog-template.md)（Keep a Changelog 1.1.0 标准结构、Unreleased 节与比对链接模板）
- **Git 提交解析与分类协议**：[changelog-extraction-protocol.md](references/protocols/changelog-extraction-protocol.md)（Added/Changed/Fixed 映射矩阵、杂音过滤红线与 SemVer 决策）
- **多版本演进变更日志案例**：[sample-changelog.md](examples/sample-changelog.md)（含大版本演进、破坏性变更声明与安全修复的完整 CHANGELOG 案例）

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：Git 历史检索与 Tag 增量扫描 (Git History Retrieval & Tag Delta)

1. **基准 Tag 定位与差分区间锁定**：
   - 运行 `git describe --tags --abbrev=0` 获取最新的正式发布 Tag；
   - 提取从该 Tag 到当前 `HEAD` 的全部增量提交列表（`git log <tag>..HEAD --oneline`）；
   - 若仓库尚无任何 Tag，则扫描全部提交历史作为 `1.0.0` 初始版本或 `Unreleased` 基础；
   - 检查本地工作树状态，确保无未处理的冲突标记。
2. **多分支与 PR 关联信息提取**：
   - 提取每个提交对应的 Issue 编号与 PR 编号；
   - 收集作者信息，为开源社区贡献者鸣谢提供数据支撑。

### 阶段 2：提交分流清洗与版本建议判定 (Commit Filtering & SemVer Bump Decision)

1. **杂音提交物理过滤**：
   - 依据 [changelog-extraction-protocol.md](references/protocols/changelog-extraction-protocol.md)；
   - 物理剔除 `style`、纯内部 `chore`、CI 配置微调与 `Merge branch` 等无用户感知价值的杂音；
   - 针对非规范历史提交执行上下文意图推断与二次语义对齐；
   - 将内部实现技术术语润色转译为面向使用者的高质量业务语言。
2. **SemVer 语义化版本号智能判定**：
   - 检查提交中是否存在 `BREAKING CHANGE` 或感叹号 `!` 语法，若存在则建议递增 Major 主版本；
   - 检查是否存在 `feat` 特性提交，若存在则建议递增 Minor 次版本；
   - 若仅有 `fix` 缺陷修复或 `perf` 优化，则建议递增 Patch 补丁版本。

### 阶段 3：Keep a Changelog 格式化归类渲染 (Changelog Classification & Formatting)

1. **标准 6 大分节精准归流**：
   - 将特性提交分类至 `### Added`；
   - 将行为微调、重构与破坏性变更分类至 `### Changed`（破坏性变更置顶标注）；
   - 将 Bug 修复分类至 `### Fixed`，安全加固分类至 `### Security`；
   - 将废弃与移除代码分别分类至 `### Deprecated` 与 `### Removed`。
2. **生成版本差分比较链接**：
   - 在日志末尾自动生成 GitHub/GitLab 两次版本间的 Compare 超链接；
   - 检查引用的 PR 与 Issue 超链接完整性，杜绝悬空死链；
   - 维护顶部 `[Unreleased]` 节的指向链接。

### 阶段 4：增量追加落盘与人机核对留置 (Delta Append & Safe Delivery)

1. **根目录 CHANGELOG.md 原子更新**：
   - 若文件已存在，保留既有历史版本内容，仅在 `[Unreleased]` 下方插入新版本块；
   - 若文件不存在，基于 [changelog-template.md](references/templates/changelog-template.md) 完整初始化；
   - 执行盘古之白排版规范核验，杜绝正文中出现任何物理绝对路径泄露。
2. **成果呈现与安全工作区留置**：
   - 向用户汇报提取出的变更摘要与建议的 SemVer 版本号，等待人类审阅确认；
   - 提示发布完成后按需执行带签名的 Git Tag 打标（`git tag -a`）；
   - 未获显式指令绝不擅自执行 Git 提交或打 Tag 操作；
   - 消除版本发布说明人工撰写的高昂时间成本与疏漏风险；
   - 为下游调用方提供透明、详尽且高度可信赖的版本升级指引；
   - 筑牢从原子提交到版本发布的自动化全链路追溯闭环。

