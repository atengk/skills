#!/usr/bin/env python3
"""盘古之白与 Markdown 文本排版自动化格式化工具。

在汉字与西文字符、数字之间智能插入半角空格（盘古之白），消除人工排版心智负担。
安全机制：自动隔离多行代码块、行内反引号、HTML 标签与超链接目标地址，杜绝误伤代码语法与 URL。

底层完全依托 scripts/_common.py 纯标准库基础设施，零外部依赖。

@author Ateng
@since 2026-10-12
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

# 确保无论从任何工作目录调用或作为模块导入，scripts/ 内部私有模块均能被正确解析
_scripts_dir = str(Path(__file__).resolve().parent)
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

# 引入底层私有公共库
from _common import MarkdownScanner, console, get_repo_root, get_skills_dir

# CJK 统一表意文字正则范围（中日韩汉字）
CJK_REGEX = r"[\u4e00-\u9fff]"


def apply_pangu_spacing(text: str) -> str:
    """对纯文本应用盘古之白规范，在汉字与英文字母/数字间插入半角空格

    操作具备幂等性（若已存在空格则不会重复插入）。
    """
    # 1. 汉字紧跟字母或数字：中 -> En / 1 => 中 En / 中 1
    text = re.sub(rf"({CJK_REGEX})([a-zA-Z0-9])", r"\1 \2", text)
    # 2. 字母或数字紧跟汉字：En / 1 -> 中 => En 中 / 1 中
    text = re.sub(rf"([a-zA-Z0-9])({CJK_REGEX})", r"\1 \2", text)
    return text


def format_markdown_content(content: str) -> str:
    """格式化 Markdown 文件内容，在深度保护代码与链接的前提下应用排版规则"""
    # 1. 首先通过 MarkdownScanner 屏蔽围栏代码块、行内代码与 HTML 注释
    masked_content, block_replacements = MarkdownScanner.mask_blocks(content)

    custom_replacements: List[Tuple[str, str]] = []
    counter = 0

    # 2. 屏蔽 HTML 标签 (<...>)
    def mask_html_tag(match: re.Match[str]) -> str:
        nonlocal counter
        token = f"__PANGU_HTML_TAG_{counter}__"
        counter += 1
        custom_replacements.append((token, match.group(0)))
        return token

    text = re.sub(r"<[a-zA-Z/][^>\n]*>", mask_html_tag, masked_content)

    # 3. 保护超链接的 URL 部分 ([显示文本](URL))，但对显示文本执行盘古之白
    def process_markdown_link(match: re.Match[str]) -> str:
        nonlocal counter
        link_text = match.group(1)
        link_url = match.group(2)
        formatted_text = apply_pangu_spacing(link_text)
        token = f"__PANGU_URL_{counter}__"
        counter += 1
        custom_replacements.append((token, link_url))
        return f"[{formatted_text}]({token})"

    text = re.sub(r"\[(.*?)\]\((.*?)\)", process_markdown_link, text)

    # 4. 对正文执行盘古之白空格优化
    text = apply_pangu_spacing(text)

    # 5. 还原自定义占位符（URL 与 HTML 标签）
    for token, original in reversed(custom_replacements):
        text = text.replace(token, original)

    # 6. 还原代码块与行内代码
    text = MarkdownScanner.restore_blocks(text, block_replacements)

    # 7. 清理行尾多余空白字符（保持换行整洁）
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines) + "\n"


def format_file(file_path: Path, repo_root: Path, check_only: bool = False) -> bool:
    """格式化或检查单个 Markdown 文件，返回是否包含排版差异"""
    try:
        original = file_path.read_text(encoding="utf-8")
        formatted = format_markdown_content(original)
        if formatted != original:
            rel_path = file_path.relative_to(repo_root) if file_path.is_relative_to(repo_root) else file_path
            if check_only:
                console.warn(f"排版待优化: {rel_path}")
            else:
                file_path.write_text(formatted, encoding="utf-8")
                console.info(f"已优化排版: {rel_path}")
            return True
        return False
    except Exception as exc:
        console.warn(f"处理文件跳过 {file_path.name}: {exc}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="盘古之白与 Markdown 排版自动化格式化工具")
    parser.add_argument("target", nargs="?", default="skills", help="目标路径（文件或目录，默认扫描 skills/）")
    parser.add_argument("--check", action="store_true", help="只读检查模式：若存在待格式化文件则报错退出（适用于 CI 门禁），不修改文件")
    args = parser.parse_args()

    repo_root = get_repo_root()
    target_path = Path(args.target).resolve()
    if not target_path.exists():
        console.error(f"目标路径不存在: {target_path}")
        sys.exit(1)

    action_label = "排版门禁检查" if args.check else "盘古之白与 Markdown 排版格式化"
    console.rule(action_label)
    changed_count = 0
    total_count = 0

    if target_path.is_file():
        if target_path.suffix.lower() == ".md":
            total_count = 1
            if format_file(target_path, repo_root, check_only=args.check):
                changed_count += 1
    else:
        for md_file in sorted(target_path.rglob("*.md")):
            total_count += 1
            if format_file(md_file, repo_root, check_only=args.check):
                changed_count += 1

    print()
    if args.check:
        if changed_count > 0:
            console.error(f"排版门禁检查未通过！发现 {changed_count} 个文件不符合规范。请执行 'python scripts/format_skills.py' 自动修复。")
            sys.exit(1)
        else:
            console.success(f"排版门禁检查通过！扫描了 {total_count} 个文件，全部符合盘古之白规范。")
            sys.exit(0)
    else:
        if changed_count > 0:
            console.success(f"排版格式化完成！扫描了 {total_count} 个文件，自动优化了 {changed_count} 个文件。")
        else:
            console.success(f"排版格式化完成！扫描了 {total_count} 个文件，全部符合盘古之白规范，无需修改。")


if __name__ == "__main__":
    main()
