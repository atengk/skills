# Keep a Changelog 标准版本日志模板 (Changelog Template)

本模板遵循国际通用的 Keep a Changelog 1.1.0 与 SemVer 2.0.0 规范，提供标准的根目录 `CHANGELOG.md` 骨架。

---

## 模板正文

```markdown
# 变更日志 (Changelog)

本项目的所有显著变更均记录在本文件中。

本日志格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，并且本项目严格遵循 [语义化版本 2.0.0 (SemVer)](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### Added
- 新增待发布功能的简要描述 ([#00](https://github.com/<!-- REPO -->/issues/00))

### Fixed
- 修复待发布缺陷的简要描述 ([#00](https://github.com/<!-- REPO -->/issues/00))

---

## [<!-- VERSION -->] - <!-- RELEASE_DATE -->

### Added
- **<!-- MODULE_NAME -->**：新增特性的用户价值说明 ([#<!-- ISSUE -->](https://github.com/<!-- REPO -->/issues/<!-- ISSUE -->))
- 新增 API 契约或命令行参数说明

### Changed
- 重构模块内部实现，降低 P99 延迟与内存占用
- **破坏性变更**：调整接口入参类型（若有）

### Deprecated
- 声明废弃某个旧方法，推荐使用新 API 代替

### Removed
- 移除上个版本标记废弃的遗留无用代码

### Fixed
- 修复特定边界条件下的崩溃或状态机竞态缺陷 ([#<!-- ISSUE -->](https://github.com/<!-- REPO -->/issues/<!-- ISSUE -->))

### Security
- 升级依赖库并修复 CVE 漏洞

---

[Unreleased]: https://github.com/<!-- REPO -->/compare/v<!-- VERSION -->...HEAD
[<!-- VERSION -->]: https://github.com/<!-- REPO -->/releases/tag/v<!-- VERSION -->
```
