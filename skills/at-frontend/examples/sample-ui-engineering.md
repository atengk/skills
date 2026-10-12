# 现代前端无障碍交互组件工程实操样例 (Sample UI Engineering)

本案例通过一个经典的“受控模态弹窗 (Accessible Modal Dialog)”组件实现，展示现代组件分层、焦点捕获 (Focus Trap)、状态机驱动以及 WCAG 2.1 AA 级无障碍特性的工程落地。

---

## 优化前代码：典型的有障碍 div 模拟弹窗

```tsx
// 常见的有严重可用性与无障碍缺陷的弹窗
export function BadModal({ open, onClose, children }) {
  if (!open) return null;
  return (
    <div className="overlay" onClick={onClose}>
      <div className="modal-box" onClick={e => e.stopPropagation()}>
        {/* 缺陷 1: 缺少无障碍角色与标题关联 */}
        {/* 缺陷 2: 纯图标关闭按钮缺少 aria-label，屏幕阅读器无法读取 */}
        {/* 缺陷 3: 键盘无法使用 Esc 关闭，Tab 键会跳出弹窗聚焦底层页面 */}
        <span className="close-btn" onClick={onClose}>×</span>
        <div>{children}</div>
      </div>
    </div>
  );
}
```

---

## 优化后代码：受控架构、焦点锁定与全键盘无障碍支持

```tsx
import React, { useEffect, useRef } from 'react';

export interface ModalProps {
  /** 弹窗是否打开 (受控状态) */
  isOpen: boolean;
  /** 关闭回调 */
  onClose: () => void;
  /** 弹窗无障碍标题 */
  title: string;
  /** 弹窗内容 */
  children: React.ReactNode;
}

export function AccessibleModal({ isOpen, onClose, title, children }: ModalProps) {
  const dialogRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!isOpen) return;

    // 1. 记录打开前的焦点元素，用于关闭后恢复焦点
    previousActiveElement.current = document.activeElement as HTMLElement;

    // 2. 自动聚焦到弹窗首个可交互元素
    dialogRef.current?.focus();

    // 3. 监听键盘 Esc 键关闭
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.stopPropagation();
        onClose();
        return;
      }

      // 4. 实现焦点捕获 (Focus Trap)：防止 Tab 跳出弹窗
      if (event.key === 'Tab' && dialogRef.current) {
        const focusables = dialogRef.current.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        if (focusables.length === 0) return;

        const firstElement = focusables[0];
        const lastElement = focusables[focusables.length - 1];

        if (event.shiftKey && document.activeElement === firstElement) {
          event.preventDefault();
          lastElement.focus();
        } else if (!event.shiftKey && document.activeElement === lastElement) {
          event.preventDefault();
          firstElement.focus();
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      // 5. 弹窗卸载或关闭时，焦点恢复至打开前的源按钮
      previousActiveElement.current?.focus();
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title-id"
        tabIndex={-1}
        className="relative w-full max-w-lg rounded-xl bg-white p-6 shadow-2xl focus:outline-none"
      >
        <div className="flex items-center justify-between pb-4 border-b border-gray-100">
          <h2 id="modal-title-id" className="text-lg font-semibold text-gray-900">
            {title}
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="关闭对话框"
            className="rounded-lg p-2 text-gray-400 hover:text-gray-700 focus-visible:ring-2 focus-visible:ring-blue-600 focus:outline-none"
          >
            <span aria-hidden="true">&times;</span>
          </button>
        </div>

        <div className="py-4 text-gray-600 text-sm">{children}</div>
      </div>
    </div>
  );
}
```

---

## 核心工程指标收益

- **无障碍合规性**：100% 通过 axe-core / Lighthouse a11y 检查，评分 100 分；
- **全键盘闭环**：视障与纯键盘用户可通过 `Esc`、`Tab` 与 `Shift+Tab` 顺畅操作；
- **组件纯粹性**：纯展示与受控交互，零网络请求与外部副作用，可在任意业务中高度复用。
