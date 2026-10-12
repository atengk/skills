# 工业级开源贡献指南实战案例 (Sample Contributing Guide)

本案例展示了一个名为 `infra-toolkit` 的工业级基础库项目的完整 `CONTRIBUTING.md`。

---

## 范例文档正文

```markdown
# 贡献指南 (CONTRIBUTING.md)

感谢你对 Infra-Toolkit 项目的关注与支持！为了维护高质量的代码资产与顺畅的开源协作体验，请在提交代码前仔细阅读本贡献指引。

---

## 1. 行为准则 (Code of Conduct)

本项目遵循 Contributor Covenant 2.1 行为准则。我们期望所有贡献者与维护者保持友好、包容与建设性的技术沟通。

---

## 2. 本地开发与测试环境

- **运行环境**：Node.js >= 20.0.0, pnpm >= 8.10.0
- **初始化工程**：
  ```bash
  git clone https://github.com/example/infra-toolkit.git
  cd infra-toolkit
  pnpm install
  ```
- **门禁自检命令**：
  ```bash
  pnpm lint       # 静态代码规范校验
  pnpm test:unit  # 运行全量单元测试
  pnpm build      # 生产环境编译构建
  ```

---

## 3. Git 分支与提交流程

### 3.1 分支命名
- 特性分支：`feat/issue-102-distributed-lock`
- 修复分支：`fix/issue-204-redis-reconnect`

### 3.2 规范化提交示例
```text
feat(lock): 实现基于 Redis 的 Redlock 分布式锁算法

- 支持自适应重试间隔与可配置锁漂移因子
- 补充 12 组高并发竞争单测，用例 100% 绿灯
- 完善使用示例与参数文档
```

---

## 4. Pull Request 准入红线

- [ ] 本地全量测试通过率 100%；
- [ ] 核心业务方法与对外接口单测行覆盖率不低于 85%；
- [ ] 零硬编码机密，配置文件使用环境变量占位符；
- [ ] Git 提交历史整洁，无 `fix bug`、`update` 等无意义提交。
```
