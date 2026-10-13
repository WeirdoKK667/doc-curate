"""
probe.py · 阶段 1 探查脚本

探查源文件：物理信息、排版、字体、加密、字符数；补全 PARAMS.md。
幂等：重复运行不产生重复文件，覆盖写。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import fitz  # PyMuPDF


def probe_pdf(source: str) -> dict:
    """探查 PDF：物理信息、排版、字体、加密。"""
    doc = fitz.open(source)
    info = {
        "format": "pdf",
        "total_pages": doc.page_count,
        "is_encrypted": doc.is_encrypted,
        "metadata": doc.metadata,
        "fonts": set(),
        "has_math_fonts": False,
        "page_samples": [],
        "print_offset_estimate": None,
    }

    math_font_prefixes = ("CM", "Math", "MT", "Symbol", "MS")

    # 抽样首/中/尾 3 页
    sample_indices = sorted(set([0, doc.page_count // 2, doc.page_count - 1]))
    for idx in sample_indices:
        page = doc[idx]
        blocks = page.get_text("dict")["blocks"]
        text = page.get_text()

        # 字体统计
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    font = span.get("font", "")
                    info["fonts"].add(font)
                    if any(font.startswith(p) for p in math_font_prefixes):
                        info["has_math_fonts"] = True

        # 双栏判断：x 坐标聚类
        x_coords = []
        for block in blocks:
            if block["type"] != 0:
                continue
            x_coords.append(block["bbox"][0])
        x_unique = sorted(set(round(x) for x in x_coords))
        cols = 2 if len(x_unique) >= 2 and (x_unique[1] - x_unique[0]) > 50 else 1

        info["page_samples"].append({
            "page": idx + 1,
            "char_count": len(text),
            "cols": cols,
            "image_count": len(page.get_images(full=True)),
        })

    # 推断印刷页偏移（启发式）
    info["print_offset_estimate"] = _estimate_offset(doc)

    info["fonts"] = sorted(info["fonts"])
    doc.close()
    return info


def _estimate_offset(doc: fitz.Document) -> int:
    """启发式推断印刷页 vs 物理页 offset。"""
    if doc.page_count < 2:
        return 0
    # 检查首页是否有印刷页号（位于页面底部居中）
    page0_text = doc[0].get_text()
    # 简单启发：印刷页号常为纯数字
    # 此处仅返回 0，实际可由用户填或更复杂算法推断
    return 0


def write_params(base_params: dict, probe_info: dict, output: Path) -> None:
    """覆盖写 PARAMS.md（探查补全后）。"""
    merged = {**base_params, **{
        "PAGE_START": 1,
        "PAGE_END": probe_info["total_pages"],
        "PRINT_OFFSET": probe_info["print_offset_estimate"],
        "BATCH": 3 if probe_info["has_math_fonts"] else 5,
        "SCAN": "off",
    }}
    # 用户填写区与探查补全区用 --- 分隔
    content = "# PARAMS.md · 探查补全后\n\n"
    content += "## 探查结果\n```json\n" + json.dumps(probe_info, ensure_ascii=False, indent=2) + "\n```\n\n"
    content += "---\n\n"
    content += "## 完整参数\n```yaml\n"
    for k, v in merged.items():
        content += f"{k}: {v}\n"
    content += "```\n"
    output.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="阶段 1 探查")
    parser.add_argument("--source", required=True, help="源文件绝对路径")
    parser.add_argument("--workdir", required=True, help="工作目录")
    parser.add_argument("--params", help="基础 PARAMS.md（可选）")
    args = parser.parse_args()

    if not Path(args.source).exists():
        print(f"hard_error: 源文件不存在 {args.source}", file=sys.stderr)
        sys.exit(1)

    print(f"探查 {args.source} ...")
    if args.source.lower().endswith(".pdf"):
        info = probe_pdf(args.source)
    else:
        print(f"hard_error: 暂未支持 {args.source}（仅 PDF）", file=sys.stderr)
        sys.exit(1)

    # 输出探查报告
    workdir = Path(args.workdir)
    report_dir = workdir / "5 阶段性工作报告"
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "探查报告.json").write_text(
        json.dumps(info, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 输出补全的 PARAMS.md
    base = {}
    if args.params and Path(args.params).exists():
        # 简化解析（实际可更复杂）
        base = {}
    write_params(base, info, workdir / "1 源" / "PARAMS.md")

    print(f"探查完成：{info['total_pages']} 页，"
          f"{'含数学字体' if info['has_math_fonts'] else '无数学字体'}")


if __name__ == "__main__":
    main()
