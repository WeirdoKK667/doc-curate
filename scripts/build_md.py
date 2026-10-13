"""
build_md.py · 阶段 5 md 组装

按 OUTPUTS 含 md 时调用。
组装模块/标签化 md。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def assemble_md(process_dir: Path, output_path: Path, modular_mode: str = "natural") -> None:
    """组装 md（三种形式之一）。"""
    md_files = sorted(process_dir.glob("p*.zh.md"))

    content_parts = ["# 文献标题（中译）\n\n"]

    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        page_match = re.search(r"<!-- page:(\d+) -->", text)
        page_num = int(page_match.group(1)) if page_match else 0

        if modular_mode == "natural":
            content_parts.append(_strip_html_comments(text) + "\n\n")
        elif modular_mode == "per_page":
            content_parts.append(f"## 【PDF 第 {page_num} 页】\n\n")
            content_parts.append(_strip_html_comments(text) + "\n\n")
        elif modular_mode == "per_tag":
            # 按标签归档
            content_parts.append(_extract_tagged(text) + "\n\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(content_parts), encoding="utf-8")
    print(f"已生成: {output_path}")


def _strip_html_comments(text: str) -> str:
    """去掉 HTML 注释，保留正文。"""
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()


def _extract_tagged(text: str) -> str:
    """按标签抽取内容。"""
    tagged = re.findall(r"<!-- tag:(\S+) -->(.*?)<!-- /tag:\1 -->", text, re.DOTALL)
    parts = []
    for tag, content in tagged:
        parts.append(f"<!-- tag:{tag} -->\n{content.strip()}\n<!-- /tag:{tag} -->\n")
    return "\n".join(parts) if parts else _strip_html_comments(text)


def main():
    parser = argparse.ArgumentParser(description="阶段 5 md 组装")
    parser.add_argument("--process-dir", required=True, help="4 处理内容/")
    parser.add_argument("--output", required=True)
    parser.add_argument("--mode", default="natural",
                        choices=["natural", "per_page", "per_tag"])
    args = parser.parse_args()

    assemble_md(Path(args.process_dir), Path(args.output), args.mode)


if __name__ == "__main__":
    main()
