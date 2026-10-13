"""
scan_terms.py · 阶段 4 术语一致性扫描

查询、添加、统计术语；阶段 4 必跑。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def load_glossary(path: Path) -> list:
    """加载专用术语表 JSON。"""
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8")).get("entries", [])


def query_term(glossary: list, term: str) -> dict | None:
    """查询术语是否已存在。"""
    for entry in glossary:
        if entry["original"].lower() == term.lower():
            return entry
    return None


def add_term(glossary_path: Path, type_: str, original: str, chinese: str, alias: list, note: str) -> None:
    """添加术语到专用术语表。"""
    if glossary_path.exists():
        data = json.loads(glossary_path.read_text(encoding="utf-8"))
    else:
        data = {"version": "1.0", "entries": []}

    # 查重
    for entry in data["entries"]:
        if entry["original"].lower() == original.lower():
            print(f"warning: 术语 {original} 已存在", file=sys.stderr)
            return

    new_id = f"{len(data['entries']) + 1:03d}"
    data["entries"].append({
        "id": new_id,
        "type": type_,
        "original": original,
        "chinese": chinese,
        "alias": alias or [],
        "note": note or "",
    })
    glossary_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"已添加: {original} → {chinese}")


def scan_translations(glossary: list, translations_dir: Path) -> dict:
    """扫描 zh.md 中的英文术语，对比 glossary。"""
    pattern = re.compile(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*|\b[A-Z]{2,}\b")
    found = {}
    unregistered = []
    inconsistent = []

    for md_file in translations_dir.rglob("*.zh.md"):
        text = md_file.read_text(encoding="utf-8")
        terms = set(pattern.findall(text))
        for term in terms:
            if len(term) < 3:
                continue
            found[term] = found.get(term, 0) + 1

    for term, count in found.items():
        entry = query_term(glossary, term)
        if not entry:
            unregistered.append({"term": term, "count": count})
        # 检查译法一致性（简化）

    return {
        "total_terms": len(found),
        "registered": len(found) - len(unregistered),
        "unregistered": unregistered,
    }


def cmd_query(args):
    glossary = load_glossary(Path(args.glossary))
    entry = query_term(glossary, args.term)
    if entry:
        print(json.dumps(entry, ensure_ascii=False, indent=2))
    else:
        print(f"未命中: {args.term}")


def cmd_add(args):
    add_term(
        Path(args.glossary),
        args.type, args.original, args.chinese,
        args.alias or [], args.note or "",
    )


def cmd_scan(args):
    glossary = load_glossary(Path(args.general))
    if args.special:
        glossary += load_glossary(Path(args.special))
    result = scan_translations(glossary, Path(args.translations))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.output:
        Path(args.output).write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def cmd_stats(args):
    glossary = load_glossary(Path(args.glossary))
    types = {}
    for entry in glossary:
        t = entry.get("type", "unknown")
        types[t] = types.get(t, 0) + 1
    print(f"术语总数: {len(glossary)}")
    print(f"类型分布: {json.dumps(types, ensure_ascii=False)}")


def main():
    parser = argparse.ArgumentParser(description="术语一致性扫描")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    # query
    p_query = subparsers.add_parser("query", help="查询术语")
    p_query.add_argument("--glossary", required=True)
    p_query.add_argument("--term", required=True)
    p_query.set_defaults(func=cmd_query)

    # add
    p_add = subparsers.add_parser("add", help="添加术语")
    p_add.add_argument("--glossary", required=True)
    p_add.add_argument("--type", required=True)
    p_add.add_argument("--original", required=True)
    p_add.add_argument("--chinese", required=True)
    p_add.add_argument("--alias", nargs="*")
    p_add.add_argument("--note")
    p_add.set_defaults(func=cmd_add)

    # scan
    p_scan = subparsers.add_parser("scan", help="扫描译文术语")
    p_scan.add_argument("--general", help="通用术语表 JSON")
    p_scan.add_argument("--special", help="专用术语表 JSON")
    p_scan.add_argument("--translations", required=True, help="译文目录")
    p_scan.add_argument("--output", help="输出文件")
    p_scan.set_defaults(func=cmd_scan)

    # stats
    p_stats = subparsers.add_parser("stats", help="统计术语")
    p_stats.add_argument("--glossary", required=True)
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
