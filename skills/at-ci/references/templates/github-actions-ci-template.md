# GitHub Actions CI 工作流标准模板 (GitHub Actions Template)

本模板提供现代多阶段持续集成流水线定义，支持代码检查、单元测试、安全扫描与质量门禁。

---

## 目录 (Table of Contents)

- [1. 工作流 YAML 模板](#1-工作流-yaml-模板)
- [2. 关键阶段与环境变量说明](#2-关键阶段与环境变量说明)
- [3. 适用技术栈适配指导](#3-适用技术栈适配指导)

---

## 1. 工作流 YAML 模板

将以下内容保存至项目 `.github/workflows/ci.yml`：

```yaml
name: Continuous Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint-and-validate:
    name: Code Quality & Lint
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Runtime Environment
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Run Format Check
        run: npm run format:check

      - name: Run Static Linter
        run: npm run lint

  test-and-coverage:
    name: Automated Tests
    runs-on: ubuntu-latest
    needs: lint-and-validate
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Runtime Environment
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Run Unit Tests with Coverage
        run: npm run test:coverage

      - name: Verify Coverage Threshold
        run: npm run test:threshold

  build-and-package:
    name: Build Artifact
    runs-on: ubuntu-latest
    needs: test-and-coverage
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Runtime Environment
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Compile and Build
        run: npm run build
```

---

## 2. 关键阶段与环境变量说明

1. **并发控制 (`concurrency`)**：
   - 当开发者向同一 PR 推送新提交时，自动取消旧构建，节约计算资源。
2. **快速失败依赖链 (`needs`)**：
   - 必须通过格式化与代码风格检测后，方才启动耗时较长的单元测试与构建流程。
3. **确定性锁版本 (`npm ci` / `pip sync`)**：
   - 依赖严格锁文件安装，杜绝偶发性小版本升级带来的不确定破坏。

---

## 3. 适用技术栈适配指导

- **Java / Spring Boot**：将运行时替换为 `actions/setup-java@v4`，命令替换为 `./mvnw clean verify`；
- **Python**：使用 `actions/setup-python@v5`，集成 `ruff check`、`pytest` 与 `pip-audit`；
- **Go**：使用 `actions/setup-go@v5`，配置 `golangci-lint` 与 `go test -race ./...`。
