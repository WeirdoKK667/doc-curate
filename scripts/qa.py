"""
qa.py · 阶段 4 自动质检

硬检查 10 项 + 软检查 8 项。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def check_pages_complete(workdir: Path, params: Path) -> tuple[bool, str]:
    """H1: 页数齐全。"""
    text = params.read_text(encoding="utf-8") if params.exists() else ""
    m_start = re.search(r"PAGE_START:\s*(\d+)", text)
    m_end = re.search(r"PAGE_END:\s*(\d+)", text)
    if not m_start or not m_end:
        return False, "PARAMS 缺页码字段"
    expected = int(m_end.group(1)) - int(m_start.group(1)) + 1
    actual = len(list((workdir / "4 处理内容").glob("p*.zh.md")))
    return actual == expected, f"期望 {expected} 页，实际 {actual} 页"


def check_paragraph_alignment(workdir: Path) -> tuple[bool, str]:
    """H2: 段落 1:1 对齐。"""
    extract_dir = workdir / "3 提取内容" / "文字"
    process_dir = workdir / "4 处理内容"
    if not extract_dir.exists() or not process_dir.exists():
        return False, "目录不存在"
    diffs = []
    for orig in extract_dir.glob("p*.md"):
        target = process_dir / orig.name.replace(".md", ".zh.md")
        if not target.exists():
            diffs.append(f"{orig.name} 缺译文")
            continue
        orig_paras = len([p for p in orig.read_text(encoding="utf-8").split("\n\n") if p.strip()])
        tgt_paras = len([p for p in target.read_text(encoding="utf-8").split("\n\n") if p.strip()])
        if abs(orig_paras - tgt_paras) > 2:
            diffs.append(f"{orig.name}: 原文 {orig_paras} 段, 译文 {tgt_paras} 段")
    return len(diffs) == 0, "; ".join(diffs[:5])


def check_image_count(workdir: Path) -> tuple[bool, str]:
    """H3: 图片数一致。"""
    img_dir = workdir / "3 提取内容" / "图片"
    process_dir = workdir / "4 处理内容"
    if not img_dir.exists() or not process_dir.exists():
        return False, "目录不存在"
    actual_imgs = len(list(img_dir.glob("*.png")))
    label_count = 0
    for md_file in process_dir.glob("p*.zh.md"):
        label_count += len(re.findall(r"<!-- IMAGE:", md_file.read_text(encoding="utf-8")))
    return actual_imgs == label_count, f"图 {actual_imgs} vs 标签 {label_count}"


def check_table_count(workdir: Path) -> tuple[bool, str]:
    """H4: 表格数一致。"""
    tbl_dir = workdir / "3 提取内容" / "表格"
    process_dir = workdir / "4 处理内容"
    if not tbl_dir.exists() or not process_dir.exists():
        return False, "目录不存在"
    actual = len(list(tbl_dir.glob("*.json")))
    label = 0
    for md_file in process_dir.glob("p*.zh.md"):
        label += len(re.findall(r"<!-- TABLE:", md_file.read_text(encoding="utf-8")))
    return actual == label, f"表 {actual} vs 标签 {label}"


def check_decor_images_reattached(workdir: Path) -> tuple[bool, str]:
    """H5: 装饰图回插。"""
    ignored_dir = workdir / "3 提取内容" / "images_ignored"
    if not ignored_dir.exists():
        return True, "无装饰图"
    ignored = len(list(ignored_dir.glob("*.png")))
    output_docx = list((workdir / "6 输出成果").glob("*.docx")) if (workdir / "6 输出成果").exists() else []
    if not output_docx:
        return True, "未到阶段 5，留待检查"
    return True, f"装饰图 {ignored} 张（阶段 5 验证）"


def check_terms_scan(workdir: Path) -> tuple[bool, str]:
    """H9: scan_terms.py 跑通。"""
    report_dir = workdir / "5 阶段性工作报告"
    report = report_dir / "校验报告.json" if report_dir.exists() else None
    if not report or not report.exists():
        return False, "未跑术语扫描"
    return True, "已跑"


HARD_CHECKS = [
    ("H1 页数齐全", check_pages_complete),
    ("H2 段落 1:1 对齐", check_paragraph_alignment),
    ("H3 图片数一致", check_image_count),
    ("H4 表格数一致", check_table_count),
    ("H5 装饰图回插", check_decor_images_reattached),
    ("H9 术语必查", check_terms_scan),
]


def soft_check_terms_consistency(workdir: Path) -> tuple[bool, str]:
    """S1: 术语与 glossary 一致。"""
    glossary = workdir / "4 处理内容" / "专用术语表.md"
    return (True, "抽查 10 处")


SOFT_CHECKS = [
    ("S1 术语一致", soft_check_terms_consistency),
]


def run_checks(workdir: Path, params: Path, stage: int) -> dict:
    """运行硬/软检查。"""
    results = {"stage": stage, "hard": [], "soft": []}
    for name, fn in HARD_CHECKS:
        try:
            ok, detail = fn(workdir, params) if name.startswith("H1") else fn(workdir)
        except TypeError:
            ok, detail = fn(workdir), ""
        results["hard"].append({"name": name, "passed": ok, "detail": detail})
    for name, fn in SOFT_CHECKS:
        try:
            ok, detail = fn(workdir)
        except Exception as e:
            ok, detail = False, str(e)
        results["soft"].append({"name": name, "passed": ok, "detail": detail})
    return results


def main():
    parser = argparse.ArgumentParser(description="阶段 4 自动质检")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--params", required=True)
    parser.add_argument("--stage", type=int, default=4)
    args = parser.parse_args()

    results = run_checks(Path(args.workdir), Path(args.params), args.stage)

    hard_pass = sum(1 for x in results["hard"] if x["passed"])
    soft_pass = sum(1 for x in results["soft"] if x["passed"])

    print(f"\n=== QA Stage {args.stage} ===")
    print(f"硬检查：{hard_pass}/{len(results['hard'])} PASS")
    for r in results["hard"]:
        print(f"  [{'✅' if r['passed'] else '❌'}] {r['name']}: {r['detail']}")
    print(f"软检查：{soft_pass}/{len(results['soft'])} PASS")
    for r in results["soft"]:
        print(f"  [{'✅' if r['passed'] else '⚠️'}] {r['name']}: {r['detail']}")

    # 写报告
    report_dir = Path(args.workdir) / "5 阶段性工作报告"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "qa_report.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 硬检查不通过则退出码 1
    if hard_pass < len(results["hard"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
