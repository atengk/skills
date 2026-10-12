#!/usr/bin/env python3
"""
开放 Agent 技能包与插件质量门禁自动化校验脚本。
完全基于 Python 原生标准库（零 pip 依赖），严格执行 .agents/AGENTS.md 规定的四道交付门禁：
1. 技能目录纯粹性与反模式扫描（坚决杜绝多余的 README.md、CHANGELOG.md 等人类文档）
2. SKILL.md Frontmatter 规范自检（顶层属性白名单、命名格式、意图覆盖度、长度与字符安全）
3. 相对路径物理死链核验（检测 SKILL.md 中所有相对超链接是否物理存在）
4. 交付物零绝对路径泄漏检测（防范 file:/// 与物理盘符硬编码）
5. 根目录 plugin.json 开放标准 Schema 契约校验

@author Ateng
@since 2026-10-12
"""

import os
import sys
import re
import json
from pathlib import Path

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

def parse_frontmatter(content: str):
    """
    轻量解析 YAML Frontmatter 头部元数据。
    完全依托正则表达式与字符串切分，无需依赖第三方 pyyaml 库。
    """
    if not content.startswith("---"):
        return None, "文件开头缺少 YAML Frontmatter 分隔符 (---)"

    match = re.match(r"^---\r?\n(.*?)\r?\n---", content, re.DOTALL)
    if not match:
        return None, "YAML Frontmatter 格式不合法或未闭合"

    raw_yaml = match.group(1)
    data = {}
    current_key = None

    for line in raw_yaml.splitlines():
        stripped = line.strip()
        # 跳过空行及以 # 开头的注释行
        if not stripped or stripped.startswith("#"):
            continue

        # 解析顶层键值对（例如：name: at-tech-doc 或 metadata:）
        top_match = re.match(r"^([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
        if top_match and not line.startswith(" ") and not line.startswith("\t"):
            key = top_match.group(1)
            val = top_match.group(2).strip()
            current_key = key
            if val:
                # 剔除首尾的单双引号包裹
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                data[key] = val
            else:
                data[key] = {}
        elif current_key and (line.startswith(" ") or line.startswith("\t")):
            # 处理嵌套属性（例如 metadata 下的子属性）
            if isinstance(data[current_key], dict):
                sub_match = re.match(r"^\s*([a-zA-Z0-9_-]+)\s*:\s*(.*)$", line)
                if sub_match:
                    sub_key = sub_match.group(1)
                    sub_val = sub_match.group(2).strip()
                    if (sub_val.startswith('"') and sub_val.endswith('"')) or (sub_val.startswith("'") and sub_val.endswith("'")):
                        sub_val = sub_val[1:-1]
                    data[current_key][sub_key] = sub_val

    return data, None

def validate_plugin_json(root: Path) -> list:
    """
    校验工程根目录 plugin.json 清单是否符合 agent-plugins.org 规范。
    """
    errors = []
    plugin_path = root / "plugin.json"
    if not plugin_path.exists():
        errors.append("未在仓库根目录下找到 plugin.json 清单文件")
        return errors

    try:
        content = json.loads(plugin_path.read_text(encoding="utf-8"))
        # 核心契约字段完整性校验
        for req in ["$schema", "name", "version", "description", "license"]:
            if req not in content:
                errors.append(f"plugin.json 缺少必需字段: '{req}'")
    except Exception as e:
        errors.append(f"plugin.json 不是合法的 JSON 格式: {e}")

    return errors

def validate_skill(skill_dir: Path) -> list:
    """
    针对单个技能子目录执行完整质量门禁校验。
    """
    errors = []
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
    fm, err = parse_frontmatter(content)
    if err:
        errors.append(f"[{skill_name}] Frontmatter 解析失败: {err}")
        return errors

    # 3. 校验顶层属性白名单
    unexpected = set(fm.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        errors.append(f"[{skill_name}] Frontmatter 包含未授权的非标顶层键: {', '.join(sorted(unexpected))}")

    # 4. 校验 name 字段约束
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

    # 5. 校验 description 字段约束
    if "description" not in fm or not fm["description"]:
        errors.append(f"[{skill_name}] Frontmatter 缺少 'description' 字段")
    else:
        desc = str(fm["description"]).strip()
        if len(desc) > 1024:
            errors.append(f"[{skill_name}] 'description' 超过长度上限 1024 字符 (当前: {len(desc)})")
        if "<" in desc or ">" in desc:
            errors.append(f"[{skill_name}] 'description' 严禁包含尖括号 '<' 或 '>'，防止 Prompt 标签注入与解析异常")

    # 6. 物理死链扫描：校验 SKILL.md 中的所有相对链接是否 100% 存在
    links = re.findall(r"\[.*?\]\((?!https?://)(.*?)\)", content)
    for link in links:
        clean_link = link.split("#")[0].strip()
        if not clean_link:
            continue
        target_path = (skill_dir / clean_link).resolve()
        if not target_path.exists():
            errors.append(f"[{skill_name}] SKILL.md 发现悬空死链: '{link}' -> 物理文件不存在")

    return errors

def validate_zero_absolute_paths(root: Path) -> list:
    """
    扫描所有 Markdown 交付物，确保无任何本地绝对路径或盘符泄漏。
    """
    errors = []
    for md_file in (root / "skills").rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        rel = md_file.relative_to(root)

        # 剥离多行代码块与行内代码，仅对真正渲染的富文本及活动超链接进行严格安全扫描
        clean_text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        clean_text = re.sub(r"`.*?`", "", clean_text)

        # 1. 检查真正的 Markdown 超链接目标地址是否泄漏本地绝对路径
        link_targets = re.findall(r"\[.*?\]\((.*?)\)", clean_text)
        for target in link_targets:
            target_clean = target.strip().split()[0]
            if target_clean.startswith("file:///") or re.match(r"^[a-zA-Z]:[\\/]", target_clean):
                errors.append(f"[{rel}] 检测到绝对路径活动链接: '{target_clean}'")

        # 2. 检查普通正文中是否有裸露的本地盘符或 file:/// URI 泄漏
        leaks = re.findall(r"(?:file:///[^\s\)\>]+|(?<![a-zA-Z0-9_])[a-zA-Z]:[\\/][a-zA-Z0-9_\-\.]+)", clean_text)
        if leaks:
            errors.append(f"[{rel}] 正文检测到未防护的本地绝对路径泄漏: {leaks[:3]}")

    return errors

def main():
    # 自动解析当前脚本所在仓库的物理根目录
    root = Path(__file__).resolve().parent.parent
    print(f"=== 正在执行 Agent 工程质量门禁验证: {root} ===")
    all_errors = []

    # 门禁 1：校验根目录插件清单
    plugin_errs = validate_plugin_json(root)
    all_errors.extend(plugin_errs)

    # 门禁 2 & 3：校验 skills/ 目录下所有子技能
    skills_dir = root / "skills"
    if skills_dir.exists():
        for item in skills_dir.iterdir():
            if item.is_dir():
                skill_errs = validate_skill(item)
                all_errors.extend(skill_errs)
    else:
        all_errors.append("未找到 skills/ 核心技能目录")

    # 门禁 4：扫描零绝对路径与物理盘符泄漏
    path_errs = validate_zero_absolute_paths(root)
    all_errors.extend(path_errs)

    print()
    if all_errors:
        print(f"❌ 质量门禁校验失败，共发现 {len(all_errors)} 处不符合项:")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("✅ 所有 DoD 质量门禁均已通过！全库严格契合国际开放 Agent 工程标准。")
        sys.exit(0)

if __name__ == "__main__":
    main()
