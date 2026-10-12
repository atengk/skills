#!/usr/bin/env python3
"""开放 Agent 技能包与插件质量门禁自动化校验脚本。

严格执行 AGENTS.md 规定的四道交付门禁：
1. 技能目录纯粹性与反模式扫描（坚决杜绝多余的 README.md、CHANGELOG.md 等人类文档）
2. SKILL.md Frontmatter 规范自检（顶层属性白名单、命名格式、意图覆盖度、长度与字符安全）
3. 相对路径物理死链核验（检测 SKILL.md 中所有相对超链接是否物理存在）
4. 交付物零绝对路径泄漏检测（防范 file:/// 与物理盘符硬编码）
5. 根目录 plugin.json 开放标准 Schema 契约校验

底层完全依托 scripts/_common.py 纯标准库基础设施，零外部依赖。

@author Ateng
@since 2026-10-12
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

# 确保无论从任何工作目录调用或作为模块导入，scripts/ 内部私有模块均能被正确解析
_scripts_dir = str(Path(__file__).resolve().parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

# 引入底层私有公共库
from _common import (
    Console,
    MarkdownScanner,
    YamlParseError,
    console,
    get_repo_root,
    get_skills_dir,
    parse_yaml_frontmatter,
)

# 向后兼容别名导出
parse_frontmatter = parse_yaml_frontmatter

# 技能元数据 YAML Frontmatter 允许的顶层属性白名单（依据 Open Agent Skills 国际标准）
ALLOWED_PROPERTIES = {
    "name",                      # [必需] 技能唯一标识
    "description",               # [必需] 触发意图与能力描述契约
    "license",                   # [可选] 开源许可证标识符
    "disable-model-invocation",  # [可选] 是否禁止大模型自主调用（仅限人工斜杠命令）
    "disable-slash-command",     # [可选] 是否禁止在聊天框注册为斜杠命令（模型专用隐式技能）
    "argument-hint",             # [可选] 斜杠命令参数提示符
    "allowed-tools",             # [可选] 最小权限原则工具白名单
    "metadata",                  # [可选] 结构化扩展字典（author、version、tags、icon等）
}

# 技能物理目录下严禁存在的冗余人类辅助文档（反模式名单，避免污染 Agent 语义索引）
PROHIBITED_SKILL_FILES = {
    "readme.md",
    "changelog.md",
    "install.md",
    "installation.md",
    "quick_reference.md",
}


def validate_plugin_json(root: Path) -> List[str]:
    """校验工程根目录 plugin.json 清单是否符合 agent-plugins.org 规范"""
    errors: List[str] = []
    plugin_path = root / "plugin.json"
    if not plugin_path.exists():
        errors.append("未在仓库根目录下找到 plugin.json 清单文件")
        return errors

    try:
        content = json.loads(plugin_path.read_text(encoding="utf-8"))
        for req in ["$schema", "name", "version", "description", "license"]:
            if req not in content:
                errors.append(f"plugin.json 缺少必需字段: '{req}'")
    except Exception as exc:
        errors.append(f"plugin.json 不是合法的 JSON 格式: {exc}")

    return errors


def validate_skill(skill_dir: Path) -> List[str]:
    """针对单个技能子目录执行完整质量门禁校验"""
    errors: List[str] = []
    skill_name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    # 1. 技能目录纯粹性检查：扫描是否存在冗余的反模式文档
    for f in skill_dir.iterdir():
        if f.is_file() and f.name.lower() in PROHIBITED_SKILL_FILES:
            errors.append(f"[{skill_name}] 触发反模式：技能目录下禁止包含人类冗余文档 '{f.name}'，请保持目录纯净")

    # 2. 检查主入口 SKILL.md 是否存在
    if not skill_md.exists():
        errors.append(f"[{skill_name}] 缺少主入口文件 SKILL.md")
        return errors

    content = skill_md.read_text(encoding="utf-8")

    # 3. 使用状态机解析 Frontmatter
    try:
        fm, _, _ = parse_yaml_frontmatter(content)
        if not fm:
            errors.append(f"[{skill_name}] Frontmatter 缺失或未包含有效数据")
            return errors
    except YamlParseError as exc:
        errors.append(f"[{skill_name}] Frontmatter YAML 解析失败: {exc}")
        return errors
    except Exception as exc:
        errors.append(f"[{skill_name}] Frontmatter 解析异常: {exc}")
        return errors

    # 4. 校验顶层属性白名单
    unexpected = set(fm.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        errors.append(f"[{skill_name}] Frontmatter 包含未授权的非标顶层键: {', '.join(sorted(unexpected))}")

    # 5. 校验 name 字段约束
    if "name" not in fm or not fm["name"]:
        errors.append(f"[{skill_name}] Frontmatter 缺少 'name' 字段")
    else:
        name = str(fm["name"]).strip()
        if len(name) > 64:
            errors.append(f"[{skill_name}] 'name' 超过长度上限 64 字符 (当前: {len(name)})")
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            errors.append(f"[{skill_name}] 'name' 必须为合法的 kebab-case 格式 (小写字母、数字与单连字符)")
        if not name.startswith("at-"):
            errors.append(f"[{skill_name}] 'name' 应遵循本项目命名空间规范以 'at-' 开头，避免跨插件全局同名冲突")

    # 6. 校验 description 字段约束
    if "description" not in fm or not fm["description"]:
        errors.append(f"[{skill_name}] Frontmatter 缺少 'description' 字段")
    else:
        desc = str(fm["description"]).strip()
        if len(desc) > 1024:
            errors.append(f"[{skill_name}] 'description' 超过长度上限 1024 字符 (当前: {len(desc)})")
        if "<" in desc or ">" in desc:
            errors.append(f"[{skill_name}] 'description' 严禁包含尖括号 '<' 或 '>'，防止 Prompt 标签注入与解析异常")

    # 7. 校验扩展控制字段类型合法性
    if "disable-model-invocation" in fm and not isinstance(fm["disable-model-invocation"], bool):
        errors.append(f"[{skill_name}] 'disable-model-invocation' 必须为布尔类型 (true/false)")
    if "disable-slash-command" in fm and not isinstance(fm["disable-slash-command"], bool):
        errors.append(f"[{skill_name}] 'disable-slash-command' 必须为布尔类型 (true/false)")
    if "allowed-tools" in fm and not isinstance(fm["allowed-tools"], list):
        errors.append(f"[{skill_name}] 'allowed-tools' 必须为工具名列表")
    if "metadata" in fm and not isinstance(fm["metadata"], dict):
        errors.append(f"[{skill_name}] 'metadata' 必须为嵌套字典对象")

    # 8. 物理死链扫描：精准提取正文所有非网络超链接
    links = MarkdownScanner.extract_links(content)
    for link_info in links:
        raw_url = link_info["url"]
        if raw_url.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_link = raw_url.split("#")[0].strip()
        if not clean_link:
            continue
        target_path = (skill_dir / clean_link).resolve()
        if not target_path.exists():
            errors.append(f"[{skill_name}] SKILL.md 第 {link_info['line']} 行发现悬空死链: '{raw_url}' -> 物理文件不存在")

    return errors


def validate_zero_absolute_paths(root: Path) -> List[str]:
    """扫描所有 Markdown 交付物，确保无任何本地绝对路径或盘符泄漏"""
    errors: List[str] = []
    skills_dir = root / "skills"
    if not skills_dir.exists():
        return errors

    for md_file in skills_dir.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        rel = md_file.relative_to(root)

        # 使用 MarkdownScanner 安全屏蔽代码块，仅检测自然文本与活动链接
        clean_text, _ = MarkdownScanner.mask_blocks(text)

        # 检查活动超链接目标地址
        link_targets = re.findall(r"\[.*?\]\((.*?)\)", clean_text)
        for target in link_targets:
            target_clean = target.strip().split()[0]
            if target_clean.startswith("file:///") or re.match(r"^[a-zA-Z]:[\\/]", target_clean):
                errors.append(f"[{rel}] 检测到绝对路径活动链接: '{target_clean}'")

        # 检查普通正文中的裸露盘符或 file:/// 协议泄漏
        leaks = re.findall(r"(?:file:///[^\s\)\>]+|(?<![a-zA-Z0-9_])[a-zA-Z]:[\\/][a-zA-Z0-9_\-\.]+)", clean_text)
        if leaks:
            errors.append(f"[{rel}] 正文检测到未防护的本地绝对路径泄漏: {leaks[:3]}")

    return errors


def main() -> None:
    root = get_repo_root()
    console.rule("Agent 工程质量门禁自检")
    all_errors: List[str] = []

    # 门禁 1：校验根目录插件清单
    plugin_errs = validate_plugin_json(root)
    all_errors.extend(plugin_errs)
    if plugin_errs:
        console.warn(f"plugin.json 发现 {len(plugin_errs)} 处异常")
    else:
        console.info("plugin.json 清单契约核验通过")

    # 门禁 2 & 3：校验 skills/ 目录下所有子技能
    skills_dir = get_skills_dir()
    if skills_dir.exists():
        skill_count = 0
        for item in sorted(skills_dir.iterdir()):
            if item.is_dir():
                skill_count += 1
                skill_errs = validate_skill(item)
                all_errors.extend(skill_errs)
                if not skill_errs:
                    console.info(f"技能 [{item.name}] 拓扑结构与 Frontmatter 验证通过")
        if skill_count == 0:
            all_errors.append("skills/ 目录下未发现任何有效技能子目录")
    else:
        all_errors.append("未找到 skills/ 核心技能目录")

    # 门禁 4：扫描零绝对路径与物理盘符泄漏
    path_errs = validate_zero_absolute_paths(root)
    all_errors.extend(path_errs)

    print()
    if all_errors:
        console.error(f"质量门禁校验未通过，共发现 {len(all_errors)} 处不符合项:")
        table_rows = []
        for idx, err in enumerate(all_errors, start=1):
            table_rows.append([str(idx), err])
        console.table(["序号", "不符合项详情"], table_rows)
        sys.exit(1)
    else:
        console.success("所有 DoD 质量门禁均已通过！全库严格契合国际开放 Agent 工程标准。")
        sys.exit(0)


if __name__ == "__main__":
    main()
