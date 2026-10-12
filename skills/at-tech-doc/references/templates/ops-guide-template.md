# [系统/组件名称] 运维部署与应急排障手册

| 属性 | 详情 |
| :--- | :--- |
| **文档类型** | 运维部署与故障应急手册 (Runbook) |
| **适用环境** | 测试环境 (Staging) / 生产环境 (Production) |
| **维护团队** | 基础架构 / SRE 运维团队 |
| **作者** | Ateng |
| **最后更新** | YYYY-MM-DD |

---

## 1. 架构拓扑与环境基线

### 1.1 依赖组件清单
| 组件名称 | 推荐版本 | 最小资源规格 | 端口与协议 | 连通性校验命令 |
| :--- | :--- | :--- | :--- | :--- |
| **JDK** | OpenJDK 21+ | 4C 8G | - | `java -version` |
| **MySQL** | 8.0.32+ | 8C 32G (SSD) | 3306 (TCP) | `mysqladmin ping -h <host>` |
| **Redis** | 7.0+ (Cluster) | 16G 内存 | 6379 (TCP) | `redis-cli -h <host> ping` |

---

## 2. 部署与启动流程

### 2.1 容器化启动 (Docker / K8s)
```bash
# 1. 拉取最新生产镜像
docker pull registry.example.com/services/my-service:v1.2.0

# 2. 检查环境变量配置文件
cat /etc/my-service/env.conf

# 3. 容器启动
docker run -d \
  --name my-service \
  --restart always \
  -p 8080:8080 \
  -v /data/logs/my-service:/app/logs \
  --env-file /etc/my-service/env.conf \
  registry.example.com/services/my-service:v1.2.0
```

### 2.2 健康检查验证
```bash
# 检查 Spring Boot Actuator 健康端点
curl -f http://127.0.0.1:8080/actuator/health

# 期望返回:
# {"status":"UP","components":{"db":{"status":"UP"},"redis":{"status":"UP"}}}
```

---

## 3. 关键监控指标与告警阈值

| 监控指标 (Metric) | 告警触发阈值 | 级别 (Severity) | 告警响应动作 |
| :--- | :--- | :--- | :--- |
| **HTTP 5xx 错误率** | > 1% 持续 2 分钟 | P1 (严重) | 触发电话告警，SRE 介入排查 |
| **API P99 响应耗时** | > 1000ms 持续 3 分钟 | P2 (高) | 检查慢 SQL 及下游依赖延迟 |
| **JVM 堆内存使用率** | > 85% 持续 5 分钟 | P2 (高) | 检查内存泄漏，抓取 Dump 文件 |
| **CPU 使用率** | > 80% 持续 10 分钟 | P3 (中) | 评估水平扩容 Pod 副本数 |

---

## 4. 常见故障应急排障操作指南

### 4.1 场景 1: 服务进程假死 / 无响应
- **现象**：健康检查探针超时，外部网关报 502 / 504。
- **排查步骤**：
  1. 执行 `top -Hp <pid>` 确认是否有线程死循环占满 CPU。
  2. 生成线程快照：`jstack <pid> > /tmp/jstack_$(date +%s).dump`。
  3. 查看是否存在死锁（Deadlock）或大量线程阻塞在数据库连接池获取。
- **应急处置**：
  > [!IMPORTANT]
  > 保留现场快照后，立即重启容器或从网关剔除该异常节点以恢复业务。

### 4.2 场景 2: 数据库连接池打满
- **现象**：日志频繁出现 `ConnectionTimeoutException: Request timed out after 30000ms`。
- **排查步骤**：
  1. 登录 MySQL 巡检执行 `SHOW FULL PROCESSLIST;`，定位 `Time` 较长的慢 SQL。
  2. 结合索引分析 `EXPLAIN`，确认是否发生全表扫描。
- **应急处置**：
  - 针对长事务或全表扫描线程执行 `KILL <process_id>;` 临时释放连接。
  - 在配置中心紧急调大连接池上限或针对非核心接口开启限流降级。

---

## 5. 权威参考资料与事实依据

### 5.1 权威信源引用清单
- [[Tier 1]] [Docker / Kubernetes 官方生产运行指南](https://...) - 核验容器存活与就绪探针配置语法及重启策略 (核验日期: YYYY-MM-DD)
- [[Tier 1]] [Spring Boot Actuator 生产监控参考](https://...) - 核验健康检查端点暴露语法与安全权限 (核验日期: YYYY-MM-DD)
- [[Tier 1]] [JVM 调优与诊断工具官方手册](https://...) - 核验 jstack、jmap 参数及 GC 告警阈值工业标准 (核验日期: YYYY-MM-DD)

### 5.2 事实核验矩阵
| 核查对象 (参数/命令/指标) | 官方基准事实 (Ground Truth) | 对应权威依据 (Tier 1 链接) | 核验状态 |
| :--- | :--- | :--- | :--- |
| **容器健康探针配置** | Kubernetes `livenessProbe` 与 `readinessProbe` 字段完全规范 | [K8s Official Docs](https://...) | 已核实官方规范 |
| **Actuator 端点路径** | 默认为 `/actuator/health`，配置 `management.endpoints.web.exposure.include` | [Spring Official Docs](https://...) | 已核验参数真实存在 |
| **诊断命令有效性** | `jstack` / `jmap` 属于 OpenJDK 标准 JDK 附带工具 | [OpenJDK Docs](https://...) | 已核实命令真实可用 |

