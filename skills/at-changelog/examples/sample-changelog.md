# 工业级 CHANGELOG.md 多版本演进实战案例 (Sample Changelog)

本案例展示了一个具备主版本演进、破坏性变更、特性新增与安全修复的完整 `CHANGELOG.md`。

---

## 范例文档正文

```markdown
# 变更日志 (Changelog)

本项目的所有显著变更均记录在本文件中。

本日志格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，并且本项目严格遵循 [语义化版本 2.0.0 (SemVer)](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### Added
- 新增对 HTTP/3 (QUIC) 协议的原生代理支持 ([#45](https://github.com/example/gateway/pull/45))

### Fixed
- 修复长连接空闲检测定时器被意外提前销毁的问题 ([#46](https://github.com/example/gateway/pull/46))

---

## [2.0.0] - 2026-10-10

### Changed
- **BREAKING CHANGE**: 重构对外 API 路由配置文件格式，由 XML 迁移为 YAML ([#38](https://github.com/example/gateway/issues/38))
- 插件上下文模型重构为零拷贝只读流，吞吐量提升 40%

### Added
- 新增基于 Redis 的分布式滑动窗口防刷限流中间件 ([#35](https://github.com/example/gateway/pull/35))
- 新增 Prometheus 原生度量指标端点 `/metrics` ([#36](https://github.com/example/gateway/pull/36))

### Removed
- 移除已废弃的旧版基于文件锁的本地限流器实现

### Fixed
- 修复高并发连接关闭时可能发生的 Socket 句柄泄漏缺陷 ([#37](https://github.com/example/gateway/pull/37))

### Security
- 升级底层网络安全依赖组件，修复 CVE-2026-8801 拒绝服务漏洞 ([#39](https://github.com/example/gateway/pull/39))

---

## [1.1.0] - 2026-08-15

### Added
- 新增 JWT 验签中间件与黑名单作废支持 ([#20](https://github.com/example/gateway/pull/20))
- 新增针对后端 upstream 的健康探测重试机制 ([#21](https://github.com/example/gateway/pull/21))

### Fixed
- 修复当 upstream 超时时返回不正确 HTTP 500 状态码的问题，规范为 HTTP 504 ([#22](https://github.com/example/gateway/pull/22))

---

## [1.0.0] - 2026-06-01

### Added
- 核心高性能反向代理网关初始版本正式发布

---

[Unreleased]: https://github.com/example/gateway/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/example/gateway/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/example/gateway/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/example/gateway/releases/tag/v1.0.0
```
