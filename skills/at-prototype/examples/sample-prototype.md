# 抛弃型状态机原型实操样例 (Sample Prototype)

本案例展示了针对一个复杂的“异步支付向导与轮询补偿状态机”，如何构建抛弃型单文件原型并得出架构结论。

---

## 验证背景与核心假设

- **业务场景**：用户扫码支付后，客户端需要发起轮询，同时支持用户主动点击“已完成支付”或“取消支付”，若轮询 30 秒超时则进入人工对账状态；
- **核心待验假设**：当轮询收到“支付中”状态且用户恰好点击“取消”时，竞态条件下的状态机流转与 UI 提示是否顺畅清晰？

---

## 生成的原型代码 (`prototype-payment-flow.html`)

原型精简掉了真实支付网关与后端接口，仅使用 JS 状态机与 Mock 模拟：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>原型: 异步支付状态机探索</title>
  <!-- PROTOTYPE: THROWAWAY EXPERIMENTAL ONLY, DO NOT USE IN PRODUCTION -->
  <style>
    body { font-family: sans-serif; padding: 24px; display: flex; gap: 24px; }
    .box { border: 1px solid #ccc; padding: 16px; border-radius: 8px; flex: 1; }
    .status-badge { font-weight: bold; color: #2563eb; }
    pre { background: #1e1e1e; color: #00ff66; padding: 12px; border-radius: 4px; }
    button { margin: 4px; padding: 8px 12px; cursor: pointer; }
  </style>
</head>
<body>
  <div class="box">
    <h2>支付向导状态机探针</h2>
    <p>当前状态: <span id="current-state" class="status-badge">IDLE</span></p>
    <div style="margin: 16px 0;">
      <button onclick="trigger('USER_CLICK_PAY')">1. 发起支付</button>
      <button onclick="trigger('POLL_SUCCESS')">2. 模拟轮询成功</button>
      <button onclick="trigger('USER_CANCEL')">3. 用户取消</button>
      <button onclick="trigger('TIMEOUT')">4. 模拟超时</button>
      <button onclick="trigger('RESET')">重置</button>
    </div>
    <div id="notice" style="color: #666; font-size: 13px;">请点击按钮模拟状态迁移</div>
  </div>

  <div class="box" style="flex: 0 0 320px;">
    <h3>实时状态探针</h3>
    <pre id="inspector">{}</pre>
  </div>

  <script>
    const machine = {
      state: 'IDLE',
      history: []
    };

    const transitions = {
      IDLE: { USER_CLICK_PAY: 'PENDING_SCAN' },
      PENDING_SCAN: { POLL_SUCCESS: 'PAID', USER_CANCEL: 'CANCELLED', TIMEOUT: 'MANUAL_AUDIT' },
      CANCELLED: { RESET: 'IDLE' },
      PAID: { RESET: 'IDLE' },
      MANUAL_AUDIT: { RESET: 'IDLE' }
    };

    function trigger(event) {
      const next = transitions[machine.state]?.[event];
      if (next) {
        machine.history.push(`${machine.state} -> ${next} (by ${event})`);
        machine.state = next;
      } else {
        alert(`非法状态跃迁: ${machine.state} 不能接收 ${event}`);
      }
      render();
    }

    function render() {
      document.getElementById('current-state').textContent = machine.state;
      document.getElementById('inspector').textContent = JSON.stringify(machine, null, 2);
    }
    render();
  </script>
</body>
</html>
```

---

## 验证结论与架构反哺

通过在浏览器中快速点击交互，团队达成以下共识：
1. **竞态消除方案**：在 `PENDING_SCAN` 状态下，用户点击“取消”前必须先挂起本地轮询请求，向服务端发送撤单请求；
2. **状态机规范确立**：状态集合收敛为 5 个离散值，明确无二义性；
3. **架构反哺**：该结论直接作为正式工单的 `at-spec` 状态迁移契约，原型文件即刻安全回收。
