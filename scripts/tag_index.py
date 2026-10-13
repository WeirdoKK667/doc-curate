"""
tag_index.py · 标签索引

建立 md 文件 → 标签清单 → 章节定位 的索引。
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def build_index(md_dir: Path) -> dict:
    """建立标签索引。"""
    index = {"files": {}, "tags": {}, "chapters": {}}

    for md_file in sorted(md_dir.glob("*.md")):
        text = md_file.read_text(encoding="utf-8")

        # 提取页码
        page_match = re.search(r"<!-- page:(\d+) -->", text)
        page_num = int(page_match.group(1)) if page_match else 0

        # 提取标签
        tags = re.findall(r"<!-- tag:(\S+) -->", text)

        # 提取章节标题
        headings = []
        for match in re.finditer(r"^(#{1,3})\s+(.+)$", text, re.MULTILINE):
            level = len(match.group(1))
            headings.append({"level": level, "title": match.group(2).strip()})

        index["files"][md_file.name] = {
            "page": page_num,
            "tags": tags,
            "headings": headings,
        }

        for tag in tags:
            index["tags"].setdefault(tag, []).append({
                "file": md_file.name,
                "page": page_num,
            })

        for h in headings:
            if h["level"] == 1:
                index["chapters"][h["title"]] = {
                    "page": page_num,
                    "file": md_file.name,
                }

    return index


def main():
    parser = argparse.ArgumentParser(description="建立标签索引")
    parser.add_argument("--md-dir", required=True)
    parser.add_argument("--output", required=True, help="索引输出 JSON")
    args = parser.parse_args()

    index = build_index(Path(args.md_dir))
    Path(args.output).write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"索引已建立: {args.output}")
    print(f"  文件数: {len(index['files'])}")
    print(f"  标签数: {len(index['tags'])}")
    print(f"  章节数: {len(index['chapters'])}")


if __name__ == "__main__":
    main()
