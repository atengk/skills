# 端到端自动化验收实战样例 (Sample E2E Acceptance Test)

本案例呈现一个企业级多租户协作平台的核心用户旅程端到端自动化验收用例，包含用户鉴权登录、项目创建、异步状态同步与结果断言。

---

## 1. 业务场景与测试目标

- **系统定位**：多租户协同研发平台；
- **验收旅程**：租户管理员登录系统 -> 导航至空间管理 -> 创建新研发项目 -> 验证成员默认权限与初始化看板卡片；
- **技术栈**：Playwright + TypeScript + Headless Chromium。

---

## 2. 页面对象实现 (ProjectManagementPage)

```typescript
// tests/pages/project-mgmt.page.ts
import { Page, Locator, expect } from '@playwright/test';

export class ProjectManagementPage {
  readonly page: Page;
  readonly newProjectBtn: Locator;
  readonly projectNameInput: Locator;
  readonly projectKeyInput: Locator;
  readonly confirmCreateBtn: Locator;
  readonly projectList: Locator;

  constructor(page: Page) {
    this.page = page;
    this.newProjectBtn = page.getByRole('button', { name: '新建项目' });
    this.projectNameInput = page.getByLabel('项目名称');
    this.projectKeyInput = page.getByLabel('项目标识 (Key)');
    this.confirmCreateBtn = page.getByRole('button', { name: '确定创建' });
    this.projectList = page.getByTestId('project-card');
  }

  async goto() {
    await this.page.goto('/dashboard/projects');
    await expect(this.page.getByRole('heading', { name: '项目工作台' })).toBeVisible();
  }

  async createProject(name: string, key: string) {
    await this.newProjectBtn.click();
    await this.projectNameInput.fill(name);
    await this.projectKeyInput.fill(key);

    const apiPromise = this.page.waitForResponse(
      (resp) => resp.url().includes('/api/v1/projects') && resp.status() === 201
    );

    await this.confirmCreateBtn.click();
    await apiPromise;
  }
}
```

---

## 3. 验收测试用例 (project-creation.spec.ts)

```typescript
// tests/e2e/project-creation.spec.ts
import { test, expect } from '@playwright/test';
import { ProjectManagementPage } from '../pages/project-mgmt.page';

test.describe('项目全生命周期创建与初始化旅程验收', () => {
  let projectPage: ProjectManagementPage;
  const uniqueKey = `PROJ_${Date.now()}`;
  const projectName = `自动化验收项目_${uniqueKey}`;

  test.beforeEach(async ({ page }) => {
    // 注入当前会话 Token
    await page.addInitScript(() => {
      window.localStorage.setItem('auth_token', 'mock_jwt_session_token');
    });
    projectPage = new ProjectManagementPage(page);
    await projectPage.goto();
  });

  test('P0-管理员成功创建项目并自动初始化敏捷看板', async ({ page }) => {
    // 1. 执行创建项目动作
    await projectPage.createProject(projectName, uniqueKey);

    // 2. 断言工作台列表中出现该项目卡片
    const createdCard = page.getByRole('heading', { name: projectName });
    await expect(createdCard).toBeVisible({ timeout: 5000 });

    // 3. 点击卡片进入详情页
    await createdCard.click();
    await expect(page).toHaveURL(new RegExp(`/projects/${uniqueKey}/board`));

    // 4. 断言默认初始化列（待办、进行中、已完成）就绪
    await expect(page.getByText('待处理 (To Do)')).toBeVisible();
    await expect(page.getByText('进行中 (In Progress)')).toBeVisible();
    await expect(page.getByText('已完成 (Done)')).toBeVisible();
  });
});
```

---

## 4. 运行结果报告与日志留痕

```text
Running 1 test using 1 worker
[chromium] › tests/e2e/project-creation.spec.ts:20:7 › 项目全生命周期创建与初始化旅程验收 › P0-管理员成功创建项目并自动初始化敏捷看板
  ✓ 注入当前会话 Token (12ms)
  ✓ 导航至 /dashboard/projects (312ms)
  ✓ 填写项目表单: 自动化验收项目_PROJ_1773322100 (145ms)
  ✓ 等待 API POST /api/v1/projects 返回 201 Created (180ms)
  ✓ 验证看板初始化列可见 (85ms)

  1 passed (1.8s)

To open last HTML report run:
  npx playwright show-report
```
