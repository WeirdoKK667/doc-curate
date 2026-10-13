"""
tag_register.py · 标签注册

校验保留字、注册用户自定义标签。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


RESERVED_TAGS = {
    "chapter", "section", "figure", "table", "footnote", "citation",
}


def validate_tag_name(tag: str) -> tuple[bool, str]:
    """校验标签名（保留字 + 命名规范）。"""
    if tag in RESERVED_TAGS:
        return True, f"保留标签: {tag}"

    # 命名规范：小写字母 + 数字 + 下划线/连字符
    if not re.match(r"^[a-z][a-z0-9_-]*$", tag):
        return False, f"标签名格式错: {tag}（应为小写字母开头 + 字母/数字/_/-）"

    if len(tag) > 32:
        return False, f"标签名过长: {tag}（>32 字符）"

    return True, "通过"


def load_registry(registry_path: Path) -> dict:
    """加载标签注册表。"""
    if not registry_path.exists():
        return {"version": "1.0", "reserved": list(RESERVED_TAGS), "custom": []}
    return json.loads(registry_path.read_text(encoding="utf-8"))


def register_tag(registry_path: Path, tag: str, description: str = "") -> None:
    """注册标签。"""
    registry = load_registry(registry_path)

    # 校验
    ok, msg = validate_tag_name(tag)
    if not ok:
        print(f"error: {msg}", file=sys.stderr)
        sys.exit(1)

    # 查重
    if tag in registry["custom"]:
        print(f"warning: 标签 {tag} 已注册", file=sys.stderr)
        return

    registry["custom"].append({
        "tag": tag,
        "description": description,
        "registered_at": "2026-10-13T00:00:00Z",
    })

    registry_path.parent.mkdir(parents=True, exist_ok=True)
    registry_path.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"已注册: {tag}")


def list_tags(registry_path: Path) -> None:
    """列出所有标签。"""
    registry = load_registry(registry_path)
    print(f"保留标签 ({len(registry['reserved'])}):")
    for t in registry["reserved"]:
        print(f"  - {t}")
    print(f"\n自定义标签 ({len(registry['custom'])}):")
    for entry in registry["custom"]:
        print(f"  - {entry['tag']}: {entry.get('description', '')}")


def main():
    parser = argparse.ArgumentParser(description="标签注册")
    parser.add_argument("--registry", required=True, help="注册表 JSON")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    p_register = subparsers.add_parser("register", help="注册标签")
    p_register.add_argument("--tag", required=True)
    p_register.add_argument("--description", default="")
    p_register.set_defaults(func=lambda args: register_tag(Path(args.registry), args.tag, args.description))

    p_list = subparsers.add_parser("list", help="列出标签")
    p_list.set_defaults(func=lambda args: list_tags(Path(args.registry)))

    p_validate = subparsers.add_parser("validate", help="校验标签名")
    p_validate.add_argument("--tag", required=True)
    p_validate.set_defaults(func=lambda args: print(validate_tag_name(args.tag)))

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
