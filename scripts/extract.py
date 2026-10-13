"""
extract.py · 阶段 2 素材提取

抽取文字、表格、图片到 3 提取内容/。
幂等：重复运行不产生重复文件，覆盖写。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import fitz
import pdfplumber


def extract_text_and_tables(source: str, page_range: tuple, out_dir: Path) -> dict:
    """按页抽取文字 + 表格。"""
    manifest = {"pages": []}
    text_dir = out_dir / "文字"
    text_dir.mkdir(parents=True, exist_ok=True)

    with pdfplumber.open(source) as pdf:
        for page_num in range(page_range[0], page_range[1] + 1):
            page = pdf.pages[page_num - 1]
            text = page.extract_text() or ""
            tables = page.extract_tables() or []

            # 双栏处理（简化）
            x_coords = [w["x0"] for w in page.extract_words()]
            cols = 2 if len(set(round(x) for x in x_coords)) > 5 else 1

            # 写文字 md
            text_file = text_dir / f"p{page_num:03d}.md"
            md_content = f"<!-- page:{page_num} -->\n\n{text}\n\n<!-- /page -->\n"
            text_file.write_text(md_content, encoding="utf-8")

            # 异常检测
            anomalies = []
            if len(text) < 80:
                anomalies.append("short_page")
            if "\ufffd" in text:
                anomalies.append("replacement_char")
            if not text.strip():
                anomalies.append("empty_text")

            page_info = {
                "page": page_num,
                "text_file": f"3 提取内容/文字/p{page_num:03d}.md",
                "tables": [],
                "image_count": 0,
                "need_ocr": len(text) < 80,
                "char_count": len(text),
                "anomalies": anomalies,
                "column_skip_suspect": False,
                "extraction_confidence": "high" if not anomalies else "mid",
            }
            manifest["pages"].append(page_info)

    return manifest


def extract_images(source: str, page_range: tuple, out_dir: Path) -> dict:
    """按页抽取图片（PyMuPDF + md5 去重）。"""
    images_dir = out_dir / "图片"
    ignored_dir = out_dir / "images_ignored"
    images_dir.mkdir(parents=True, exist_ok=True)
    ignored_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(source)
    seen_md5 = {}  # md5 -> 已使用页
    img_count = 0

    for page_num in range(page_range[0], page_range[1] + 1):
        page = doc[page_num - 1]
        images = page.get_images(full=True)
        # 按 y0 排序
        page_imgs = []
        for img in images:
            xref = img[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                y0 = pix.y if hasattr(pix, "y") else 0
                page_imgs.append((y0, xref, pix))
            except Exception:
                continue
        page_imgs.sort(key=lambda x: x[0])

        for idx, (y0, xref, pix) in enumerate(page_imgs, start=1):
            try:
                if pix.n - pix.alpha >= 4:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                data = pix.tobytes("png")
                md5 = hashlib.md5(data).hexdigest()

                if pix.width < 80 or pix.height < 80:
                    ignored_dir / f"p{page_num:03d}_img{idx:02d}.png"
                    (ignored_dir / f"p{page_num:03d}_img{idx:02d}.png").write_bytes(data)
                    continue

                if md5 in seen_md5:
                    continue  # 跨页重复图跳过

                seen_md5[md5] = page_num
                img_count += 1
                (images_dir / f"p{page_num:03d}_img{idx:02d}.png").write_bytes(data)
            except Exception as e:
                print(f"warning: 抽取图 p{page_num}_img{idx} 失败: {e}", file=sys.stderr)

    doc.close()
    return {"total_images": img_count}


def write_manifest(manifest: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description="阶段 2 素材提取")
    parser.add_argument("--source", required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--workdir", required=True)
    args = parser.parse_args()

    workdir = Path(args.workdir)
    extract_dir = workdir / "3 提取内容"
    extract_dir.mkdir(parents=True, exist_ok=True)

    print(f"抽取 {args.source} 第 {args.start}-{args.end} 页 ...")
    text_manifest = extract_text_and_tables(
        args.source, (args.start, args.end), extract_dir
    )
    img_info = extract_images(args.source, (args.start, args.end), extract_dir)

    manifest = {
        **text_manifest,
        "summary": {
            "total_pages": len(text_manifest["pages"]),
            "images_kept": img_info["total_images"],
        },
    }
    write_manifest(manifest, extract_dir / "manifest.json")

    print(f"抽取完成：{len(text_manifest['pages'])} 页，{img_info['total_images']} 图")


if __name__ == "__main__":
    main()
