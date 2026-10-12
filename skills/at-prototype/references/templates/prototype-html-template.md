# 单文件交互原型自闭环模板 (Prototype HTML Template)

本模板提供了一个零依赖、零构建、内置实时状态监视面板的单文件交互原型结构。用于快速验证复杂状态机、UI 交互流或多步骤表单。

---

## 模板源码规范

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>实验原型: <!-- PROTOTYPE_TITLE --></title>
  <!-- PROTOTYPE: THROWAWAY EXPERIMENTAL ONLY, DO NOT USE IN PRODUCTION -->
  <style>
    :root {
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --border: #e2e8f0;
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --radius: 8px;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }
    .prototype-canvas {
      flex: 1;
      padding: 32px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 24px;
      max-width: 640px;
      width: 100%;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .badge {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 600;
      background: #eff6ff;
      color: #1e40af;
      margin-bottom: 12px;
    }
    button {
      background: var(--primary);
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 14px;
      cursor: pointer;
      margin-right: 8px;
    }
    button:hover { background: var(--primary-hover); }
    /* 实时状态监视器面板 (State Inspector) */
    .inspector {
      width: 360px;
      background: #0f172a;
      color: #f8fafc;
      border-left: 1px solid #334155;
      padding: 20px;
      display: flex;
      flex-direction: column;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 13px;
    }
    .inspector h3 {
      font-size: 14px;
      color: #94a3b8;
      margin-bottom: 12px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .inspector pre {
      flex: 1;
      overflow-y: auto;
      background: #020617;
      padding: 12px;
      border-radius: 6px;
      border: 1px solid #1e293b;
      color: #38bdf8;
    }
  </style>
</head>
<body>
  <main class="prototype-canvas">
    <div class="card">
      <span class="badge">抛弃型验证原型</span>
      <h2><!-- PROTOTYPE_TITLE --></h2>
      <p style="color: #64748b; margin: 8px 0 20px 0;"><!-- HYPOTHESIS_DESCRIPTION --></p>

      <!-- 核心交互区域 -->
      <div id="interactive-app">
        <!-- 动态渲染组件 -->
      </div>
    </div>
  </main>

  <aside class="inspector">
    <h3>实时状态探针 (State Inspector)</h3>
    <pre id="state-dump">{}</pre>
  </aside>

  <script>
    // 1. 核心状态机模型定义 (State Machine)
    const state = {
      step: 'INIT',
      data: {},
      history: []
    };

    function renderInspector() {
      document.getElementById('state-dump').textContent = JSON.stringify(state, null, 2);
    }

    function dispatch(action, payload) {
      console.log('[Action]', action, payload);
      state.history.push({ action, payload, time: new Date().toISOString() });
      // 状态迁移逻辑
      // ...
      renderApp();
      renderInspector();
    }

    function renderApp() {
      const container = document.getElementById('interactive-app');
      // 渲染核心交互 DOM
    }

    // 初始启动
    renderApp();
    renderInspector();
  </script>
</body>
</html>
```
