#!/usr/bin/env python3
"""新技能脚手架自动化生成器。

依据 Open Agent Skills 国际标准与本项目微内核架构规范，一键初始化合规的原子技能骨架。
自动注入规范的 Frontmatter 模板、三级状态机生命周期与 references/ 知识层骨架，生成即合规。

底层完全依托 scripts/_common.py 纯标准库基础设施，零外部依赖。

@author Ateng
@since 2026-10-12
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional, Tuple

# 引入底层私有公共库
from _common import console, get_skills_dir


def validate_skill_name(name: str) -> Tuple[bool, Optional[str]]:
    """校验技能名称是否符合 kebab-case 与命名空间规范"""
    if len(name) > 64:
        return False, f"技能名称长度不能超过 64 字符 (当前: {len(name)})"
    if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
        return False, f"技能名称 '{name}' 必须全小写，仅包含数字、字母与单连字符 (kebab-case)"
    if not name.startswith("at-"):
        return False, f"技能名称 '{name}' 必须遵循项目命名空间规范以 'at-' 开头 (例如: at-{name})"
    return True, None


def generate_skill_scaffold(skill_name: str, display_name: Optional[str] = None, description: Optional[str] = None) -> bool:
    """生成合规的技能物理拓扑与初始骨架文件"""
    skills_dir = get_skills_dir()
    target_dir = skills_dir / skill_name

    if target_dir.exists():
        console.error(f"目标技能目录已存在: {target_dir}")
        return False

    title = display_name if display_name else skill_name[3:].replace("-", " ").title()
    desc = description if description else f"当用户需要编写或处理关于 {title} 的高频业务场景时使用此技能。提供专业编排引擎与方法论，交付生产就绪的标准产物。"

    # 1. 创建微内核物理目录拓扑
    target_dir.mkdir(parents=True, exist_ok=True)
    ref_dir = target_dir / "references"
    protocols_dir = ref_dir / "protocols"
    templates_dir = ref_dir / "templates"
    protocols_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    # 2. 生成主入口 SKILL.md
    skill_md_content = f"""---
name: {skill_name}
description: {desc}
license: Apache-2.0
metadata:
  author: Ateng
  version: 1.0.0
  tags:
    - engineering
    - agent-skill
  icon: puzzle
---

# {title} 编排器 ({title} Orchestrator)

提供专业、生产落地的 {title} 编排与交付能力。作为轻量化状态机运行，采用三级渐进式披露生命周期。

## 渐进式知识地图 (Progressive Disclosure Map)

详细执行协议与标准化模板均存放于 `references/` 目录：
- **执行协议**：[protocol.md](references/protocols/protocol.md)
- **交付模板**：[template.md](references/templates/template.md)

---

## 编排生命周期 (Synthesis Lifecycle)

### 阶段 1：需求分析与模式识别
1. **模式判定**：分析用户诉求，匹配最佳处理路径。
2. **上下文检索**：按需 JIT 阅读 [protocol.md](references/protocols/protocol.md)。

### 阶段 2：方案规划与人机确认闸门
1. **大纲呈现**：在动笔前呈现清晰的三级大纲树与交付范围。
2. **用户审批**：明确等待用户确认通过后，方可推进正文撰写。

### 阶段 3：执行与交付纪律
1. **模板应用**：依据 [template.md](references/templates/template.md) 进行结构化生产。
2. **渐进交付**：长篇产物遵循分批交付纪律，严禁跨轮次偷跑。

### 阶段 4：质量自检与闭环
1. **排版质检**：严格遵循盘古之白与 Markdown 规范。
2. **路径安全**：严禁泄漏本地绝对路径（`file:///`、物理盘符）。
"""

    (target_dir / "SKILL.md").write_text(skill_md_content, encoding="utf-8")

    # 3. 创建合规的示例参考文件（防止初始死链）
    protocol_content = f"""# {title} 核心执行协议 (Execution Protocol)

本文档定义了 `{skill_name}` 在执行过程中的交互与推演约束。

---

## 1. 执行准则
1. 优先使用标准库及环境已有依赖；
2. 遵循防御性编程原则与向后兼容契约；
3. 单一职责，保持模块深而窄。
"""
    (protocols_dir / "protocol.md").write_text(protocol_content, encoding="utf-8")

    template_content = f"""# {title} 标准交付模板 (Template)

本文档提供了 `{skill_name}` 的标准交付产物结构。

---

## 1. 核心概述
<!-- 阐述核心业务背景与技术目标 -->

## 2. 详细设计
<!-- 展开具体架构或代码设计 -->
"""
    (templates_dir / "template.md").write_text(template_content, encoding="utf-8")

    console.success(f"成功创建新技能脚手架: {skill_name}")
    console.info(f"物理路径: {target_dir}")
    print()
    console.table(
        ["文件与模块", "职责类型", "相对路径"],
        [
            ["SKILL.md", "主入口与 Frontmatter", f"skills/{skill_name}/SKILL.md"],
            ["protocol.md", "L3 深度执行协议", f"skills/{skill_name}/references/protocols/protocol.md"],
            ["template.md", "L3 交付模板", f"skills/{skill_name}/references/templates/template.md"],
        ],
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="一键初始化合规的原子 Agent 技能脚手架")
    parser.add_argument("name", help="技能名称 (必须以 at- 开头且符合 kebab-case，例如 at-code-review)")
    parser.add_argument("--title", help="技能展示标题 (可选，例如 'Code Review')")
    parser.add_argument("--desc", help="技能描述与触发意图 (可选，符合第三人称触发工程标准)")

    args = parser.parse_args()

    # 校验名称合规性
    valid, err = validate_skill_name(args.name)
    if not valid:
        console.error(f"参数错误: {err}")
        sys.exit(1)

    console.rule("初始化新 Agent 技能脚手架")
    success = generate_skill_scaffold(args.name, args.title, args.desc)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
