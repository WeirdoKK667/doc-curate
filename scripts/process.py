"""
process.py · 阶段 3 处理调度

根据 PIPELINE 调度子动作：translate / glossary / modular / proof / format_convert。
幂等：覆盖写。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_pipeline(params_path: Path) -> list:
    """解析 PARAMS.md 中的 PIPELINE 列表。"""
    if not params_path.exists():
        return []
    text = params_path.read_text(encoding="utf-8")
    # 简化解析：找 PIPELINE: [translate, glossary, ...]
    import re
    match = re.search(r"PIPELINE:\s*\[([^\]]+)\]", text)
    if not match:
        return []
    items = [x.strip() for x in match.group(1).split(",")]
    return items


def action_translate(params: dict, workdir: Path) -> None:
    """翻译子动作（占位，实际由 subagent 派发）。"""
    print("action: translate - 派发 subagent")


def action_glossary(params: dict, workdir: Path) -> None:
    """术语汇总子动作。"""
    print("action: glossary - 维护专用术语表")


def action_format_convert(params: dict, workdir: Path) -> None:
    """格式转换子动作。"""
    print("action: format_convert - 调用 format_adapter")


def action_modular(params: dict, workdir: Path) -> None:
    """模块化子动作。"""
    print("action: modular - 应用三种形式之一")


def action_proof(params: dict, workdir: Path) -> None:
    """校对子动作。"""
    print("action: proof - 对照原文译文检查")


ACTIONS = {
    "translate": action_translate,
    "glossary": action_glossary,
    "format_convert": action_format_convert,
    "modular": action_modular,
    "proof": action_proof,
}


def main():
    parser = argparse.ArgumentParser(description="阶段 3 处理调度")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--params", required=True)
    args = parser.parse_args()

    workdir = Path(args.workdir)
    pipeline = parse_pipeline(Path(args.params))
    print(f"PIPELINE: {pipeline}")

    if not pipeline:
        print("warning: PIPELINE 为空，跳过阶段 3", file=sys.stderr)
        return

    for action_name in pipeline:
        if action_name not in ACTIONS:
            print(f"warning: 未知动作 {action_name}", file=sys.stderr)
            continue
        ACTIONS[action_name]({}, workdir)

    # 写阶段报告
    report_dir = workdir / "5 阶段性工作报告"
    report_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "stage": 3,
        "pipeline": pipeline,
        "completed": pipeline,
    }
    (report_dir / "处理报告.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("阶段 3 完成")


if __name__ == "__main__":
    main()
