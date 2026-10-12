"""通用基础支持库 (内部私有模块)

为工程工具链脚本提供跨平台终端美化、健壮的 YAML Frontmatter 解析器与结构化 Markdown 流式扫描能力。
严格限定使用 Python 3 原生标准库，保持 100% 零外部依赖。

@author Ateng
@since 2026-10-12
"""

from __future__ import annotations

import ctypes
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ==============================================================================
# 1. 终端视觉渲染引擎 (Console Engine)
# ==============================================================================

class Console:
    """跨平台终端彩色与格式化排版控制台

    支持 TTY 检测、NO_COLOR 环境变量兼容、Windows 原生虚拟终端激活以及表格/徽标渲染。
    """

    # ANSI 转义样式常量
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # 前景色
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # 背景色
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"

    def __init__(self, force_color: Optional[bool] = None) -> None:
        """初始化控制台实例

        Args:
            force_color: 是否强制启用彩色。None 表示自适应环境检测。
        """
        if force_color is not None:
            self.color_enabled = force_color
        else:
            self.color_enabled = self._detect_color_support()

        if self.color_enabled and sys.platform == "win32":
            self._enable_windows_vt_mode()

    @staticmethod
    def _detect_color_support() -> bool:
        """探测当前运行环境是否支持颜色"""
        # 若设置了 NO_COLOR 环境变量，则遵循规范禁用颜色
        if "NO_COLOR" in os.environ:
            return False
        # 若未连接到真实终端且未设置 FORCE_COLOR，则禁用颜色
        if not sys.stdout.isatty() and "FORCE_COLOR" not in os.environ:
            return False
        # Windows 或 POSIX 默认支持
        return True

    @staticmethod
    def _enable_windows_vt_mode() -> bool:
        """为 Windows 10+ 控制台激活虚拟终端 ANSI 序列支持"""
        try:
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            if handle in (0, -1):
                return False
            mode = ctypes.c_ulong()
            if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                return False
            # 开启 ENABLE_VIRTUAL_TERMINAL_PROCESSING (0x0004)
            mode.value |= 0x0004
            return bool(kernel32.SetConsoleMode(handle, mode))
        except Exception:
            return False

    def style(self, text: str, *styles: str) -> str:
        """为文本包裹 ANSI 样式，若未开启颜色则原样返回"""
        if not self.color_enabled or not styles:
            return text
        prefix = "".join(styles)
        return f"{prefix}{text}{self.RESET}"

    # 快捷业务打印方法
    def success(self, message: str) -> None:
        """打印成功提示"""
        badge = self.style(" ✔ 成功 ", self.BOLD, self.WHITE, self.BG_GREEN) if self.color_enabled else "[✔ 成功]"
        print(f"{badge} {message}")

    def error(self, message: str) -> None:
        """打印错误提示"""
        badge = self.style(" ✖ 失败 ", self.BOLD, self.WHITE, self.BG_RED) if self.color_enabled else "[✖ 失败]"
        print(f"{badge} {message}")

    def warn(self, message: str) -> None:
        """打印警告提示"""
        badge = self.style(" ⚠ 警告 ", self.BOLD, self.BLACK, self.BG_YELLOW) if self.color_enabled else "[⚠ 警告]"
        print(f"{badge} {message}")

    def info(self, message: str) -> None:
        """打印信息提示"""
        badge = self.style(" ℹ 信息 ", self.BOLD, self.WHITE, self.BG_BLUE) if self.color_enabled else "[ℹ 信息]"
        print(f"{badge} {message}")

    def rule(self, title: str = "", char: str = "─", width: int = 70) -> None:
        """打印水平分割线"""
        if not title:
            line = char * width
            print(self.style(line, self.DIM))
            return

        formatted_title = f" {title} "
        title_len = len(title.encode("gbk", errors="ignore"))  # 估算 CJK 字符宽度
        left_len = max(2, (width - title_len) // 2)
        right_len = max(2, width - title_len - left_len)
        line = f"{char * left_len}{formatted_title}{char * right_len}"
        print(self.style(line, self.BOLD, self.CYAN))

    def table(self, headers: List[str], rows: List[List[str]]) -> None:
        """打印自适应对齐的终端文本表格

        Args:
            headers: 表头列表
            rows: 数据行列表
        """
        if not headers:
            return

        all_rows = [headers] + rows

        def display_width(text: str) -> int:
            """估算包含东亚全角字符的字符串在终端中占用的物理列数"""
            total = 0
            for char in str(text):
                # 简单判定 CJK 范围
                if ord(char) > 127:
                    total += 2
                else:
                    total += 1
            return total

        # 计算每列的最大物理宽度
        col_widths = [0] * len(headers)
        for row in all_rows:
            for idx, cell in enumerate(row):
                if idx < len(col_widths):
                    col_widths[idx] = max(col_widths[idx], display_width(str(cell)))

        # 生成边框辅助函数
        def pad_cell(text: str, target_width: int) -> str:
            pad_size = max(0, target_width - display_width(text))
            return str(text) + (" " * pad_size)

        sep_line = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
        header_sep = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
        bottom_line = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"

        print(self.style(sep_line, self.DIM))

        # 表头
        header_cells = [f" {pad_cell(h, col_widths[i])} " for i, h in enumerate(headers)]
        print("│" + "│".join(self.style(cell, self.BOLD) for cell in header_cells) + "│")
        print(self.style(header_sep, self.DIM))

        # 内容行
        for row in rows:
            row_cells = []
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    row_cells.append(f" {pad_cell(cell, col_widths[i])} ")
            print("│" + "│".join(row_cells) + "│")

        print(self.style(bottom_line, self.DIM))


# 模块全局默认单例控制台
console = Console()


# ==============================================================================
# 2. 健壮 YAML Frontmatter 状态机 (YAML-lite FSM)
# ==============================================================================

class YamlParseError(ValueError):
    """YAML 解析语法异常"""
    def __init__(self, message: str, line_no: int, raw_line: str = "") -> None:
        super().__init__(f"第 {line_no} 行解析错误: {message} -> '{raw_line}'")
        self.line_no = line_no
        self.raw_line = raw_line


def _parse_scalar(value_str: str) -> Any:
    """将 YAML 标量字符串自动识别为 Python 原生类型"""
    val = value_str.strip()
    if not val:
        return ""

    # 布尔值
    if val.lower() in ("true", "yes", "on"):
        return True
    if val.lower() in ("false", "no", "off"):
        return False
    if val.lower() in ("null", "~"):
        return None

    # 整型与浮点型
    if re.fullmatch(r"-?\d+", val):
        return int(val)
    if re.fullmatch(r"-?\d+\.\d+", val):
        return float(val)

    # 引号包裹字符串
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        inner = val[1:-1]
        return inner.replace('\\"', '"').replace("\\'", "'")

    # 行内列表: [item1, item2]
    if val.startswith("[") and val.endswith("]"):
        inner = val[1:-1].strip()
        if not inner:
            return []
        items = [s.strip() for s in inner.split(",")]
        return [_parse_scalar(item) for item in items if item]

    return val


class _YamlRecursiveParser:
    """内部 YAML Frontmatter 递归下降解析器"""

    def __init__(self, lines: List[Tuple[int, str]]) -> None:
        self.lines = lines
        self.pos = 0

    def parse(self) -> Dict[str, Any]:
        """执行顶层解析"""
        result, _ = self.parse_dict(expected_indent=0)
        return result

    def parse_dict(self, expected_indent: int) -> Tuple[Dict[str, Any], int]:
        """解析指定缩进深度的字典"""
        d: Dict[str, Any] = {}
        while self.pos < len(self.lines):
            line_no, raw_line = self.lines[self.pos]
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                self.pos += 1
                continue

            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if indent < expected_indent:
                break
            if ":" not in stripped:
                break

            key_part, val_part = stripped.split(":", 1)
            key = key_part.strip()
            val_raw = val_part.strip()
            if " #" in val_raw:
                val_raw = re.sub(r"\s+#.*$", "", val_raw).strip()

            self.pos += 1
            if val_raw:
                d[key] = _parse_scalar(val_raw)
            else:
                d[key] = self.parse_child_block(indent)

        return d, self.pos

    def parse_child_block(self, parent_indent: int) -> Any:
        """根据下一有效行的特征分发为嵌套字典或列表"""
        peek_pos = self.pos
        while peek_pos < len(self.lines):
            _, raw_l = self.lines[peek_pos]
            s = raw_l.strip()
            if s and not s.startswith("#"):
                break
            peek_pos += 1

        if peek_pos >= len(self.lines):
            return {}

        child_indent = len(self.lines[peek_pos][1]) - len(self.lines[peek_pos][1].lstrip(" "))
        if child_indent <= parent_indent:
            return {}

        first_line = self.lines[peek_pos][1].strip()
        if first_line.startswith("- "):
            return self.parse_list(child_indent)
        else:
            sub_dict, _ = self.parse_dict(child_indent)
            return sub_dict

    def parse_list(self, expected_indent: int) -> List[Any]:
        """解析缩进列表项"""
        items: List[Any] = []
        while self.pos < len(self.lines):
            line_no, raw_line = self.lines[self.pos]
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                self.pos += 1
                continue

            indent = len(raw_line) - len(raw_line.lstrip(" "))
            if indent < expected_indent:
                break
            if not stripped.startswith("- "):
                break

            item_raw = stripped[2:].strip()
            if " #" in item_raw:
                item_raw = re.sub(r"\s+#.*$", "", item_raw).strip()
            items.append(_parse_scalar(item_raw))
            self.pos += 1

        return items


def parse_yaml_frontmatter(content: str) -> Tuple[Dict[str, Any], str, int]:
    """使用轻量递归下降状态机解析 Markdown 顶层 YAML Frontmatter

    完整支持：缩进层级、`key: value`、行内列表、缩进列表 (`- item`)、嵌套字典与基础标量转换。

    Args:
        content: Markdown 完整文本

    Returns:
        Tuple[Dict[str, Any], str, int]: (元数据字典, 剩余正文文本, Frontmatter 结束行号)

    Raises:
        YamlParseError: 语法错误时抛出详细行号
    """
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, content, 0

    frontmatter_lines: List[Tuple[int, str]] = []
    end_idx = -1

    for idx in range(1, len(lines)):
        line_str = lines[idx]
        if line_str.strip() == "---":
            end_idx = idx
            break
        frontmatter_lines.append((idx + 1, line_str))

    if end_idx == -1:
        raise YamlParseError("YAML Frontmatter 未正确闭合，缺少结尾的 '---'", 1)

    parser = _YamlRecursiveParser(frontmatter_lines)
    root_dict = parser.parse()
    body_text = "".join(lines[end_idx + 1:])
    return root_dict, body_text, end_idx + 1


# ==============================================================================
# 3. 结构化 Markdown 流式扫描器 (Markdown Scanner)
# ==============================================================================

class MarkdownScanner:
    """结构化 Markdown 文档流式扫描器

    提供代码块屏蔽、超链接精准提取、标题提取等确定性解析能力。
    """

    # 链接匹配正则 (支持 [text](url))，需排除图片 ![]
    LINK_PATTERN = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
    IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    @classmethod
    def mask_blocks(cls, content: str) -> Tuple[str, List[Tuple[str, str]]]:
        """屏蔽 Markdown 代码块、行内代码与 HTML 注释，防止后续文本替换/排版时发生污染

        Args:
            content: 原 Markdown 文本

        Returns:
            Tuple[str, List[Tuple[str, str]]]: (带占位符的脱敏文本, [(占位符Token, 原始文本), ...])
        """
        replacements: List[Tuple[str, str]] = []
        token_counter = 0

        def replace_with_token(match: re.Match[str]) -> str:
            nonlocal token_counter
            token = f"__MD_BLOCK_TOKEN_{token_counter}__"
            token_counter += 1
            replacements.append((token, match.group(0)))
            return token

        text = content

        # 1. 屏蔽连续 3 或 4 个反引号的多行代码块
        text = re.sub(r"(```|~~~)(?:[\s\S]*?)\1", replace_with_token, text)

        # 2. 屏蔽 HTML 注释 <!-- ... -->
        text = re.sub(r"<!--[\s\S]*?-->", replace_with_token, text)

        # 3. 屏蔽行内代码 `...`
        text = re.sub(r"`[^`\n]+`", replace_with_token, text)

        return text, replacements

    @classmethod
    def restore_blocks(cls, text: str, replacements: List[Tuple[str, str]]) -> str:
        """还原被屏蔽的代码块与占位符"""
        result = text
        for token, original in reversed(replacements):
            result = result.replace(token, original)
        return result

    @classmethod
    def extract_links(cls, content: str) -> List[Dict[str, Any]]:
        """从 Markdown 正文中精准提取所有超链接（排除代码块与图片链接）

        Returns:
            List[Dict]: 每个元素包含 {"text": 锚文本, "url": 链接地址, "line": 行号}
        """
        results: List[Dict[str, Any]] = []
        in_code_block = False

        for line_no, line in enumerate(content.splitlines(), start=1):
            stripped = line.strip()
            # 代码块围栏判定
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # 屏蔽行内代码
            line_no_code = re.sub(r"`[^`]+`", "", line)

            # 匹配常规链接
            for match in cls.LINK_PATTERN.finditer(line_no_code):
                anchor = match.group(1).strip()
                url = match.group(2).strip()
                results.append({
                    "text": anchor,
                    "url": url,
                    "line": line_no,
                })

        return results

    @classmethod
    def extract_headings(cls, content: str) -> List[Dict[str, Any]]:
        """提取所有标题层级（排除代码块中的 # 字符）"""
        headings: List[Dict[str, Any]] = []
        in_code_block = False

        for line_no, line in enumerate(content.splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            if stripped.startswith("#"):
                match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
                if match:
                    level = len(match.group(1))
                    title = match.group(2).strip()
                    headings.append({
                        "level": level,
                        "title": title,
                        "line": line_no,
                    })

        return headings


# ==============================================================================
# 4. 项目公共路径与文件工具
# ==============================================================================

def get_repo_root() -> Path:
    """获取技能代码仓库根目录绝对路径"""
    return Path(__file__).resolve().parent.parent


def get_skills_dir() -> Path:
    """获取 skills/ 核心目录路径"""
    return get_repo_root() / "skills"
