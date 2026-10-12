# 前端 Core Web Vitals 与渲染管线性能优化法则 (Web Vitals Optimization Protocol)

本协议系统规范了现代前端 Web 性能工程的指标体系、度量标准与关键渲染路径（Critical Rendering Path）优化法则，聚焦 Google Core Web Vitals 核心指标。

---

## 目录 (Table of Contents)

- [1. Core Web Vitals 核心指标与健康基准](#1-core-web-vitals-核心指标与健康基准)
- [2. 最大内容绘制 (LCP) 极致加速指南](#2-最大内容绘制-lcp-极致加速指南)
- [3. 交互到下次绘制 (INP) 与主线程解绑](#3-交互到下次绘制-inp-与主线程解绑)
- [4. 累积布局偏移 (CLS) 稳定性保障](#4-累积布局偏移-cls-稳定性保障)
- [5. 资源加载优先级与代码分割策略](#5-资源加载优先级与代码分割策略)

---

## 1. Core Web Vitals 核心指标与健康基准

现代前端体验聚焦三大核心真实用户指标（RUM）：

| 指标 | 全称 | 体验维度 | 良好标准 (Good) | 需改进 (Needs Improvement) | 较差 (Poor) |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **LCP** | Largest Contentful Paint | 加载感知速度 | **≤ 2.5 秒** | 2.5 ~ 4.0 秒 | > 4.0 秒 |
| **INP** | Interaction to Next Paint | 交互响应灵敏度 | **≤ 200 毫秒** | 200 ~ 500 毫秒 | > 500 毫秒 |
| **CLS** | Cumulative Layout Shift | 视觉稳定性 | **≤ 0.1** | 0.1 ~ 0.25 | > 0.25 |

---

## 2. 最大内容绘制 (LCP) 极致加速指南

LCP 元素通常是页面首屏可见区域中最大的图片、文本块或视频海报：

### 2.1 消除渲染阻塞资源 (Eliminate Render-Blocking Resources)
- **CSS 优化**：首屏关键 CSS 优先内联（Critical CSS）；非关键 CSS 异步延迟加载或使用媒体查询分离；
- **JS 脚本加载**：非关键 JavaScript 脚本强制添加 `defer` 或 `async`，杜绝在 `<head>` 中出现阻塞解析的裸 `<script>`。

### 2.2 关键图片资源优先级提示 (Priority Hints)
- 对首屏最大 Banner 图片显式添加 `fetchpriority="high"` 与 `loading="eager"`；
- 严禁对首屏 LCP 候选图片使用 `loading="lazy"`；
- 采用现代格式图片（WebP、AVIF），并使用 `<picture>` 或 `srcset` 按设备分辨率自适应分发。

---

## 3. 交互到下次绘制 (INP) 与主线程解绑

INP 取代 FID 成为度量用户在整个页面生命周期中所有点击、轻按与键盘输入的整体响应灵敏度：

### 3.1 拆解长任务 (Break Up Long Tasks)
- 任何在主线程执行超过 50ms 的 JavaScript 任务均为长任务（Long Task）；
- 使用 `scheduler.yield()`、`setTimeout` 或 `requestIdleCallback` 将长计算切片为微任务块，及时让出主线程给渲染管线；
- 复杂数据计算、格式化、密集加解密转移至 Web Worker 独立线程执行。

### 3.2 避免高频 DOM 读写交替引发强制同步布局
- 严禁在循环体中交替执行“读取几何属性（如 `offsetHeight`）”与“写入样式（如 `style.width`）”操作（Layout Thrashing）；
- 批量读取后再批量修改，或通过 `requestAnimationFrame` 统一调度 DOM 突变。

---

## 4. 累积布局偏移 (CLS) 稳定性保障

布局偏移会导致用户误触按钮，严重损害体验：

### 4.1 预留占位空间与尺寸宽高比
- 所有 `<img>`、`<video>` 与 `<iframe>` 标签**必须显式标注 `width` 与 `height` 属性**，或在 CSS 中配置 `aspect-ratio`，以便浏览器在资源下载前预留布局空间；
- 骨架屏（Skeleton Screen）与占位容器必须保持与最终内容完全一致的尺寸高度。

### 4.2 字体加载偏移 (FOUT / FOIT) 防护
- Web 字体加载配置 `font-display: swap` 或 `optional`；
- 使用 `@font-face` 中的 `size-adjust`、`ascent-override` 与本地后备字体尺寸对齐，消除字体替换瞬间的跳变。

---

## 5. 资源加载优先级与代码分割策略

- **路由级与组件级动态加载**：基于动态 `import()` 拆分打包产物（Chunk），非首页路由组件与低频弹窗组件实施按需懒加载；
- **Tree-Shaking 与依赖瘦身**：移除过重的全量引入（如 `lodash` 换为原生方法或具名按需导入，`moment.js` 换为 `dayjs`）；
- **预加载关键依赖**：使用 `<link rel="preload">` 预先拉取首屏关键字体与首屏 API 数据。
