# 端到端自动化测试套件模板 (E2E Test Suite Template)

本文档提供基于现代化 Playwright 框架的端到端自动化测试套件代码结构模板，涵盖页面对象模型（POM）、数据夹具（Fixtures）与高确定性断言。

---

## 1. 页面对象抽象模板 (Page Object Model)

```typescript
// tests/pages/checkout.page.ts
import { Page, Locator, expect } from '@playwright/test';

export class CheckoutPage {
  readonly page: Page;
  readonly cartItems: Locator;
  readonly couponInput: Locator;
  readonly applyCouponButton: Locator;
  readonly submitOrderButton: Locator;
  readonly orderStatusBanner: Locator;

  constructor(page: Page) {
    this.page = page;
    this.cartItems = page.getByTestId('cart-item');
    this.couponInput = page.getByPlaceholder('请输入优惠券码');
    this.applyCouponButton = page.getByRole('button', { name: '兑换优惠券' });
    this.submitOrderButton = page.getByRole('button', { name: '提交订单' });
    this.orderStatusBanner = page.getByTestId('order-status-banner');
  }

  async goto() {
    await this.page.goto('/checkout');
    await expect(this.page).toHaveTitle(/结算中心/);
  }

  async applyCoupon(code: string) {
    await this.couponInput.fill(code);
    await this.applyCouponButton.click();
    // 显式等待接口返回
    await this.page.waitForResponse(
      (resp) => resp.url().includes('/api/coupons/apply') && resp.status() === 200
    );
  }

  async submitOrder(): Promise<string> {
    const responsePromise = this.page.waitForResponse(
      (resp) => resp.url().includes('/api/orders') && resp.status() === 201
    );
    await this.submitOrderButton.click();
    const response = await responsePromise;
    const data = await response.json();
    return data.orderId;
  }
}
```

---

## 2. 核心用户旅程测试用例模板 (Test Suite)

```typescript
// tests/e2e/order-flow.spec.ts
import { test, expect } from '@playwright/test';
import { CheckoutPage } from '../pages/checkout.page';

test.describe('订单提交流程全链路验收 (Order Checkout Flow)', () => {
  let checkoutPage: CheckoutPage;

  test.beforeEach(async ({ page }) => {
    // 注入鉴权状态或模拟用户会话
    checkoutPage = new CheckoutPage(page);
    await checkoutPage.goto();
  });

  test('P0-黄金旅程：用户使用有效优惠券成功创建订单', async ({ page }) => {
    // 1. 验证结算清单默认加载完成
    await expect(checkoutPage.cartItems).toHaveCount(2);

    // 2. 兑换优惠券并断言金额更新
    await checkoutPage.applyCoupon('DISCOUNT_2026');
    await expect(page.getByText('已抵扣 ¥50.00')).toBeVisible();

    // 3. 提交订单并捕获返回的订单 ID
    const orderId = await checkoutPage.submitOrder();
    expect(orderId).toBeTruthy();

    // 4. 断言页面自动跳转至支付成功页
    await expect(page).toHaveURL(new RegExp(`/pay/${orderId}`));
    await expect(checkoutPage.orderStatusBanner).toContainText('订单创建成功，请尽快支付');
  });

  test('P1-异常分支：输入过期优惠券时提示语义化错误并阻断提单', async ({ page }) => {
    await checkoutPage.applyCoupon('EXPIRED_CODE');

    // 断言错误提示可见
    const errorToast = page.getByRole('alert');
    await expect(errorToast).toBeVisible();
    await expect(errorToast).toContainText('优惠券已失效或不存在');

    // 断言按钮依然保持可用状态，允许用户重新输入
    await expect(checkoutPage.submitOrderButton).toBeEnabled();
  });
});
```

---

## 3. 全局配置文件模板 (playwright.config.ts)

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30 * 1000,
  expect: {
    timeout: 5000,
  },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html', { open: 'never' }],
    ['list']
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
  ],
});
```
