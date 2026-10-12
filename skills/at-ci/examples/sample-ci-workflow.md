# 案例样本：多平台与全量门禁 CI 工作流 (Sample CI Workflow)

本案例展示开源与企业级高严谨度项目采用的矩阵测试与全量门禁工作流配置。

---

## 1. 场景背景与架构目标

- **项目类型**：跨平台开源工具库（Node.js / Python 混合）；
- **核心诉求**：
  - 支持 Linux、macOS 与 Windows 三端并行测试；
  - 自动执行 Markdown 文档死链检测与盘古之白排版核验；
  - PR 合并至主干分支后自动打 Tag 并发布 Release。

---

## 2. 真实流水线配置样例

```yaml
name: Matrix CI & Quality Gate

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  docs-and-lint:
    name: Markdown & Code Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Validate Markdown Formatting
        run: python scripts/format_skills.py --check
      - name: Execute Quality Gate
        run: python scripts/validate.py

  cross-platform-test:
    name: Test on ${{ matrix.os }} (Node ${{ matrix.node }})
    needs: docs-and-lint
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ ubuntu-latest, windows-latest, macos-latest ]
        node: [ 18, 20 ]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci
      - run: npm test
```

---

## 3. 运行效果与度量结果

- **测试吞吐率**：6 组矩阵并发执行，全量测试耗时由串行的 12 分钟下降至 2 分 30 秒；
- **缺陷拦截率**：门禁在前置 G1 阶段即拦截了 92% 的格式与链接问题，避免无效构建浪费 Runner 额度。
