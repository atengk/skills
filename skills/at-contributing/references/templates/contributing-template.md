# 工业级开源贡献指南标准模板 (Contributing Standard Template)

本模板提供了一个符合国际开源规范的项目根目录 `CONTRIBUTING.md` 标准骨架。

---

## 模板正文

```markdown
# 贡献指南 (Contributing Guide)

感谢您对 <!-- PROJECT_NAME --> 的关注！我们热烈欢迎来自社区的每一位贡献者。为了保证协作顺畅与代码库质量，请在提交代码前仔细阅读本指南。

---

## 📜 行为准则 (Code of Conduct)

我们致力于营造一个包容、开放且互相尊重的协作环境。所有参与本项目的贡献者必须遵守公认的开源行为准则，尊重不同背景与视角的协作者。

---

## 🛠️ 本地开发环境准备 (Development Setup)

1. **环境依赖要求**：
   - <!-- RUNTIME_REQUIREMENTS --> (例如 Node.js >= 18.0.0 / Java >= 17)
   - Git 2.30+
2. **克隆与环境初始化**：
   ```bash
   git clone https://github.com/<!-- REPO -->.git
   cd <!-- REPO_DIR -->
   <!-- INSTALL_COMMAND --> # npm install 或 mvn clean install
   ```
3. **本地测试与代码质量验证**：
   ```bash
   <!-- TEST_COMMAND -->  # 运行全量单元测试
   <!-- LINT_COMMAND -->  # 运行代码规范校验
   ```

---

## 🌿 分支与协作工作流 (Branching Workflow)

1. **创建特性分支**：
   基于最新的 `main` 主干切出新分支，命名格式遵循：
   - 特性功能：`feat/<issue-id>-<description>`
   - 缺陷修复：`fix/<issue-id>-<description>`
2. **本地原子化开发**：
   - 单次提交保持职责单一与最小爆炸半径；
   - 编写或修改代码的同时，必须同步补充对应的单元测试。

---

## 📝 提交信息规范 (Commit Guidelines)

本项目严格执行 **Conventional Commits 1.0.0** 规范。提交信息格式为：

```text
<type>(<scope>): <清晰中文描述>

[可选详细说明正文]
```

### 常用类型 (Types)
- `feat`: 新增特性或功能
- `fix`: 缺陷修复
- `docs`: 文档变更
- `style`: 代码格式优化（空格、分号等，不影响运行逻辑）
- `refactor`: 既不修复缺陷也不新增特性的代码重构
- `perf`: 性能调优
- `test`: 单元测试与集成测试补充
- `ci`: 流水线配置变更

---

## 🚀 Pull Request (PR) 准入检查清单

在发起 Pull Request 之前，请确认以下各项均已自检通过：

- [ ] **分支基于最新 main**：已通过 `git rebase main` 完成最新基线对齐；
- [ ] **测试全量通过**：运行本地测试套件，确认 100% 绿灯无回归；
- [ ] **代码规范合规**：代码通过了本地 Lint 与格式化校验；
- [ ] **文档同步更新**：若涉及 API 变更或配置调整，已同步更新相关文档；
- [ ] **无敏感凭据**：检查 Diff，确认无任何数据库密码或真实 Token 泄漏。

---

## 📄 许可证确认 (License Agreement)

向本项目提交的所有代码与文档，默认均在项目既有的开源许可证（<!-- LICENSE_NAME -->）下发布。
```
