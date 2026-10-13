"""
ocr.py · 阶段 2 OCR（按需）

SCAN=on 时调用。
默认走 subagent 视觉识别（输出渲染图，由 subagent 转写）；
可选 tesseract / paddleocr。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import fitz


def render_page_as_image(source: str, page_num: int, output_path: Path, dpi: int = 300) -> None:
    """渲染 PDF 单页为 300dpi 图。"""
    doc = fitz.open(source)
    page = doc[page_num - 1]
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    pix.save(str(output_path))
    doc.close()


def ocr_with_tesseract(image_path: Path) -> str:
    """OCR（tesseract 引擎）。"""
    try:
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        return pytesseract.image_to_string(img, lang="chi_sim+eng")
    except ImportError:
        print("warning: pytesseract 未安装", file=sys.stderr)
        return ""


def ocr_with_paddleocr(image_path: Path) -> str:
    """OCR（PaddleOCR 引擎）。"""
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(use_angle_cls=True, lang="ch")
        result = ocr.ocr(str(image_path), cls=True)
        lines = [line[1][0] for line in result[0]] if result[0] else []
        return "\n".join(lines)
    except ImportError:
        print("warning: paddleocr 未安装", file=sys.stderr)
        return ""


def main():
    parser = argparse.ArgumentParser(description="阶段 2 OCR")
    parser.add_argument("--source", required=True, help="PDF 源文件")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--output-dir", required=True, help="输出目录（存渲染图 + 转写 md）")
    parser.add_argument("--backend", default="subagent_visual",
                        choices=["subagent_visual", "tesseract", "paddleocr"])
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"OCR ({args.backend}): {args.source} 第 {args.start}-{args.end} 页 ...")

    for page_num in range(args.start, args.end + 1):
        img_path = out_dir / f"p{page_num:03d}_fullpage.png"
        render_page_as_image(args.source, page_num, img_path)

        if args.backend == "tesseract":
            text = ocr_with_tesseract(img_path)
        elif args.backend == "paddleocr":
            text = ocr_with_paddleocr(img_path)
        else:
            # subagent_visual: 输出图，由 subagent 视觉识别
            print(f"已渲染: {img_path}（待 subagent 视觉识别）")
            continue

        # 写转写 md
        md_path = out_dir / f"p{page_num:03d}.md"
        md_path.write_text(
            f"<!-- page:{page_num} -->\n\n{text}\n\n<!-- /page -->\n",
            encoding="utf-8",
        )

    print(f"OCR 完成: {out_dir}")


if __name__ == "__main__":
    main()
