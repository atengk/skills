#!/usr/bin/env python3
"""单技能打包与分发导出器。

遵循 Open Agent Skills 国际标准，将指定的微内核技能包导出为标准的 .skill 制品文件（基于 Zip 压缩标准）。
前置强绑定 validate.py 质量门禁：只有 100% 通过死链、Frontmatter 与排版校验的技能才允许打包导出，确保交付物零缺陷。

底层完全依托 scripts/_common.py 纯标准库基础设施，零外部依赖。

@author Ateng
@since 2026-10-12
"""

from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path
from typing import Optional

# 确保无论从任何工作目录调用或作为模块导入，scripts/ 内部私有模块均能被正确解析
_scripts_dir = str(Path(__file__).resolve().parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

# 引入底层私有公共库与门禁验证
from _common import (
    console,
    get_repo_root,
    get_skills_dir,
    parse_yaml_frontmatter,
)
from validate import validate_skill

# 排除不需要打包的临时或系统隐藏文件
EXCLUDE_FILES = {
    ".ds_store",
    "thumbs.db",
    "desktop.ini",
}


def package_single_skill(skill_dir: Path, output_dir: Path) -> Optional[Path]:
    """对单个技能目录进行门禁质检并打包为 .skill 制品"""
    skill_name = skill_dir.name
    console.info(f"正在准备打包技能: {skill_name}")

    # 1. 前置质量门禁核验
    errors = validate_skill(skill_dir)
    if errors:
        console.error(f"技能 [{skill_name}] 质量门禁校验未通过，禁止打包导出:")
        for err in errors:
            print(f"    - {err}")
        return None

    # 2. 解析元数据版本号
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")
    fm, _, _ = parse_yaml_frontmatter(content)
    version = "1.0.0"
    if fm and "metadata" in fm and isinstance(fm["metadata"], dict):
        version = fm["metadata"].get("version", "1.0.0")

    # 3. 准备输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    target_package = output_dir / f"{skill_name}-v{version}.skill"

    # 4. 构建 Zip 制品
    file_count = 0
    with zipfile.ZipFile(target_package, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in sorted(skill_dir.rglob("*")):
            if file_path.is_file():
                if file_path.name.lower() in EXCLUDE_FILES:
                    continue
                # 保持相对路径归档结构 (例如 at-tech-doc/SKILL.md)
                archive_name = file_path.relative_to(skill_dir.parent)
                zipf.write(file_path, archive_name)
                file_count += 1

    size_kb = target_package.stat().st_size / 1024
    console.success(f"打包成功: {target_package.name} ({size_kb:.2f} KB, 包含 {file_count} 个文件)")
    return target_package


def main() -> None:
    parser = argparse.ArgumentParser(description="将 Agent 技能打包导出为标准 .skill 发行制品")
    parser.add_argument("skill", nargs="?", help="技能目录路径或技能名称 (例如: skills/at-tech-doc 或 at-tech-doc)")
    parser.add_argument("--all", action="store_true", help="批量打包全库所有技能")
    parser.add_argument("--out", default="dist", help="制品输出目录 (默认: dist/)")

    args = parser.parse_args()
    root = get_repo_root()
    skills_root = get_skills_dir()
    output_dir = (root / args.out).resolve()

    console.rule("Agent 技能打包与分发")

    if args.all:
        console.info("开始全量批量打包技能库...")
        success_count = 0
        total_count = 0
        table_rows = []

        for item in sorted(skills_root.iterdir()):
            if item.is_dir():
                total_count += 1
                pkg = package_single_skill(item, output_dir)
                if pkg:
                    success_count += 1
                    size_kb = pkg.stat().st_size / 1024
                    table_rows.append([item.name, pkg.name, f"{size_kb:.2f} KB", "SUCCESS"])
                else:
                    table_rows.append([item.name, "-", "-", "FAILED"])

        print()
        if table_rows:
            console.table(["技能名称", "制品文件名", "体积", "打包状态"], table_rows)

        print()
        if success_count == total_count:
            console.success(f"批量打包完毕！全部成功 ({success_count}/{total_count})，制品存放于: {output_dir}")
            sys.exit(0)
        else:
            console.error(f"部分技能打包失败: 成功 {success_count}/{total_count}")
            sys.exit(1)
    else:
        if not args.skill:
            console.error("请指定要打包的技能名称或路径（或使用 --all 参数）")
            sys.exit(1)

        target_skill = Path(args.skill)
        if not target_skill.exists():
            candidate = skills_root / args.skill
            if candidate.exists():
                target_skill = candidate
            else:
                console.error(f"未找到指定的技能目录: {args.skill}")
                sys.exit(1)

        result = package_single_skill(target_skill, output_dir)
        sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
