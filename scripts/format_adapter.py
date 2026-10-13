"""
format_adapter.py · 阶段 2 格式适配器

CAJ / Word / PPT / EPUB → PDF 统一中间格式。
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def convert_caj_to_pdf(caj_path: Path, output_pdf: Path) -> bool:
    """CAJ → PDF（caj2pdf）。"""
    try:
        result = subprocess.run(
            ["caj2pdf", "convert", str(caj_path), "-o", str(output_pdf)],
            capture_output=True, text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("warning: caj2pdf 未安装，CAJ 转换失败", file=sys.stderr)
        return False


def convert_docx_to_pdf(docx_path: Path, output_pdf: Path) -> bool:
    """Word → PDF（python-docx + 简化处理）。"""
    # 实际可使用 LibreOffice 命令行：libreoffice --headless --convert-to pdf
    try:
        result = subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf",
             "--outdir", str(output_pdf.parent), str(docx_path)],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            src = docx_path.with_suffix(".pdf")
            if src.exists():
                shutil.move(str(src), str(output_pdf))
                return True
        return False
    except FileNotFoundError:
        print("warning: LibreOffice 未安装，DOCX 转换失败", file=sys.stderr)
        return False


def convert_pptx_to_pdf(pptx_path: Path, output_pdf: Path) -> bool:
    """PPT → PDF。"""
    try:
        result = subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf",
             "--outdir", str(output_pdf.parent), str(pptx_path)],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            src = pptx_path.with_suffix(".pdf")
            if src.exists():
                shutil.move(str(src), str(output_pdf))
                return True
        return False
    except FileNotFoundError:
        print("warning: LibreOffice 未安装，PPTX 转换失败", file=sys.stderr)
        return False


def convert_epub_to_pdf(epub_path: Path, output_pdf: Path) -> bool:
    """EPUB → PDF（ebooklib + 报告库）。"""
    # 简化处理：提示用户手动转换
    print(f"warning: EPUB 转换需要手动导出，源文件 {epub_path}", file=sys.stderr)
    return False


CONVERTERS = {
    "caj": convert_caj_to_pdf,
    "docx": convert_docx_to_pdf,
    "pptx": convert_pptx_to_pdf,
    "epub": convert_epub_to_pdf,
}


def main():
    parser = argparse.ArgumentParser(description="阶段 2 格式适配")
    parser.add_argument("--format", required=True, choices=CONVERTERS.keys())
    parser.add_argument("--input", required=True, help="输入文件")
    parser.add_argument("--output", required=True, help="输出 PDF")
    args = parser.parse_args()

    converter = CONVERTERS[args.format]
    success = converter(Path(args.input), Path(args.output))
    if success:
        print(f"转换成功: {args.output}")
    else:
        print(f"转换失败: {args.input}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
