"""
tag_query.py · 按标签检索

按标签检索指定内容。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def query_by_tag(index_path: Path, tag: str) -> list:
    """按标签查询。"""
    if not index_path.exists():
        print(f"error: 索引文件不存在 {index_path}", file=sys.stderr)
        sys.exit(1)

    index = json.loads(index_path.read_text(encoding="utf-8"))
    return index.get("tags", {}).get(tag, [])


def query_by_chapter(index_path: Path, chapter: str) -> dict:
    """按章节查询。"""
    index = json.loads(index_path.read_text(encoding="utf-8"))
    return index.get("chapters", {}).get(chapter, {})


def main():
    parser = argparse.ArgumentParser(description="按标签/章节检索")
    parser.add_argument("--index", required=True, help="标签索引 JSON")
    parser.add_argument("--tag", help="按标签查询")
    parser.add_argument("--chapter", help="按章节查询")
    args = parser.parse_args()

    if args.tag:
        results = query_by_tag(Path(args.index), args.tag)
        print(f"标签 '{args.tag}': {len(results)} 处")
        for r in results:
            print(f"  - {r['file']} (PDF 第 {r['page']} 页)")
    elif args.chapter:
        result = query_by_chapter(Path(args.index), args.chapter)
        if result:
            print(f"章节 '{args.chapter}': {result}")
        else:
            print(f"未找到章节 '{args.chapter}'")
    else:
        print("error: 必须指定 --tag 或 --chapter", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
