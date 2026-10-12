# 全栈安全加固与防注入实战改造案例 (Sample Security Hardening)

本案例通过一个存在严重 SQL 注入、水平越权与明文机密漏洞的查询接口，展示如何实施工业级安全加固改造。

---

## 加固前代码：漏洞百出的原始实现

```typescript
// 存在严重安全漏洞的订单查询接口
import express from 'express';
import mysql from 'mysql2/promise';

const app = express();
const dbPassword = "SuperSecretPassword123!"; // 漏洞 1: 硬编码明文机密

app.get('/api/orders', async (req, res) => {
  const orderId = req.query.id;
  const sortBy = req.query.sort || 'created_at';

  // 漏洞 2: SQL 注入 (字符串拼接)
  // 漏洞 3: 水平越权 (IDOR，未校验当前用户租户归属)
  const query = `SELECT * FROM orders WHERE id = '${orderId}' ORDER BY ${sortBy} DESC`;

  try {
    const conn = await mysql.createConnection({ host: 'localhost', user: 'root', password: dbPassword });
    const [rows] = await conn.execute(query);
    res.json(rows);
  } catch (err) {
    // 漏洞 4: 暴露数据库详细异常与物理堆栈
    res.status(500).json({ error: err.message, stack: err.stack });
  }
});
```

---

## 加固后代码：参数化绑定、租户隔离与凭据脱敏

```typescript
import express, { Request, Response } from 'express';
import { z } from 'zod';
import { getDbPool } from './db';
import { authenticateUser, UserContext } from './auth';

// 1. 输入参数模式验证与排序字段白名单
const QuerySchema = z.object({
  id: z.string().uuid("无效的订单标识格式"),
  sort: z.enum(['created_at', 'amount', 'status']).default('created_at'),
});

export async function getOrderHandler(req: Request & { user?: UserContext }, res: Response) {
  // 2. 身份认证与上下文卫语句拦截
  const currentUser = req.user;
  if (!currentUser) {
    return res.status(401).json({ code: 'UNAUTHORIZED', message: '请先登录' });
  }

  // 3. 严格模式白名单校验输入
  const parseResult = QuerySchema.safeParse(req.query);
  if (!parseResult.success) {
    return res.status(400).json({
      code: 'INVALID_ARGUMENT',
      message: '参数格式不合法',
      errors: parseResult.error.flatten()
    });
  }

  const { id, sort } = parseResult.data;

  try {
    const pool = getDbPool(); // 连接凭据统一从 process.env.DB_PASSWORD 环境变量读取

    // 4. 防御 SQL 注入 (预编译参数化占位符) + 防御水平越权 (强绑定当前用户租户 ID)
    const sql = `
      SELECT id, amount, status, created_at
      FROM orders
      WHERE id = ? AND tenant_id = ?
      ORDER BY ${sort} DESC
    `;
    const [rows] = await pool.execute(sql, [id, currentUser.tenantId]);

    if (!Array.isArray(rows) || rows.length === 0) {
      return res.status(404).json({ code: 'NOT_FOUND', message: '订单不存在或无权访问' });
    }

    return res.json({ data: rows[0] });
  } catch (err) {
    // 5. 异常安全：内部记录错误日志，对外屏蔽堆栈，返回统一抽象语义码
    console.error(`[SecuritySafeLog] 查询订单失败, orderId=${id}`, err);
    return res.status(500).json({ code: 'INTERNAL_ERROR', message: '系统繁忙，请稍后再试' });
  }
}
```

---

## 安全防御成效比对

| 审查维度 | 加固前状况 | 加固后防御成果 |
| :--- | :--- | :--- |
| **凭据安全** | 源代码硬编码数据库明文密码 | 环境变量安全注入，代码 0 明文泄漏 |
| **SQL 注入** | 拼接字符串，可被 `' OR '1'='1` 拖库 | 参数化预编译占位符，排序列严格白名单枚举映射 |
| **访问控制** | 任意用户改 id 即可查看他人订单 (IDOR) | 强力注入 `tenant_id` 过滤条件，根除越权风险 |
| **异常暴露** | 客户端直接返回数据库报错与调用栈 | 抽象错误码统一响应，底层细节被严格屏蔽 |
