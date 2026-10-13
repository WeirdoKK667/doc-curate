"""
build_docx.py · 阶段 5 Word 组装

解析 p*.zh.md 标签，按物理页升序自动组装。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def parse_zh_md(md_path: Path) -> dict:
    """解析单页 zh.md，按标签分组。"""
    text = md_path.read_text(encoding="utf-8")

    # 提取标签内容
    page_match = re.search(r"<!-- page:(\d+) -->", text)
    print_match = re.search(r"<!-- 印刷页码：(\S+) -->", text)

    # 提取 IMAGE 块
    images = re.findall(
        r"<!-- IMAGE:(p\d+_img\d+\.\w+) -->(.*?)<!-- /IMAGE -->",
        text, re.DOTALL,
    )
    # 提取 TABLE 块
    tables = re.findall(
        r"<!-- TABLE:(p\d+_t\d+) -->(.*?)<!-- /TABLE -->",
        text, re.DOTALL,
    )
    # 提取脚注
    footnotes = re.findall(
        r"<!-- footnote:(\d+) -->(.*?)<!-- /footnote -->",
        text, re.DOTALL,
    )

    return {
        "page": int(page_match.group(1)) if page_match else 0,
        "print_page": print_match.group(1) if print_match else None,
        "images": images,
        "tables": tables,
        "footnotes": footnotes,
        "body": re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip(),
    }


def set_chinese_font(run, size: int = 11, bold: bool = False, color: RGBColor | None = None):
    """设置中文字体（必须同时设 eastAsia）。"""
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = "Times New Roman"  # 西文
    run.font.element.rPr.rFonts.eastAsia = "宋体"  # 中文（硬约束）
    if color:
        run.font.color.rgb = color


def build_docx(translations_dir: Path, output_path: Path, keep_mark: bool = True):
    """组装 Word。"""
    doc = Document()
    # 默认样式
    style = doc.styles["Normal"]
    style.font.name = "Times New Roman"
    style.font.element.rPr.rFonts.eastAsia = "宋体"
    style.font.size = Pt(11)

    # 卷首
    title = doc.add_heading("", level=0)
    run = title.add_run("文献标题（中译 + 原文）")
    set_chinese_font(run, size=18, bold=True)

    p = doc.add_paragraph()
    run = p.add_run("原文页码范围：PDF 第 X-X 页")
    set_chinese_font(run, size=10)
    p = doc.add_paragraph()
    run = p.add_run("翻译说明：专有名词规则、图片文字处理方式、存疑项数量")
    set_chinese_font(run, size=10)

    # 按物理页升序遍历
    md_files = sorted(translations_dir.glob("p*.zh.md"))
    for md_file in md_files:
        page_data = parse_zh_md(md_file)

        if keep_mark:
            # 页标记：Normal 段 + 加粗 + 浅灰底（不污染导航窗格）
            p = doc.add_paragraph()
            run = p.add_run(f"【PDF 第 {page_data['page']} 页】")
            set_chinese_font(run, size=10, bold=True, color=RGBColor(0x80, 0x80, 0x80))

        # 正文
        for para_text in page_data["body"].split("\n\n"):
            if not para_text.strip():
                continue
            p = doc.add_paragraph()
            p.paragraph_format.first_line_indent = Cm(0.74)  # 2 字符
            p.paragraph_format.line_spacing = 1.5
            run = p.add_run(para_text)
            set_chinese_font(run, size=11)

        # 图片（居中，超宽等比缩放到 15cm）
        for img_id, img_text in page_data["images"]:
            img_path = translations_dir.parent / "3 提取内容" / "图片" / f"{img_id}.png"
            if img_path.exists():
                p = doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p.add_run()
                run.add_picture(str(img_path), width=Cm(15))

        # 表格
        for tbl_id, tbl_text in page_data["tables"]:
            # 简化处理：实际可解析 markdown 表格
            lines = [l for l in tbl_text.split("\n") if l.strip() and "|" in l]
            if len(lines) >= 2:
                header = [c.strip() for c in lines[0].split("|")[1:-1]]
                rows = [[c.strip() for c in l.split("|")[1:-1]] for l in lines[2:]]
                table = doc.add_table(rows=1 + len(rows), cols=len(header))
                table.style = "Table Grid"
                for i, h in enumerate(header):
                    table.rows[0].cells[i].text = h
                for r, row in enumerate(rows, start=1):
                    for c, val in enumerate(row):
                        table.rows[r].cells[c].text = val

        # 脚注（FOOTNOTE=docx）
        for fn_id, fn_text in page_data["footnotes"]:
            # python-docx 的脚注 API 较复杂，此处简化
            p = doc.add_paragraph()
            run = p.add_run(f"[{fn_id}] {fn_text}")
            set_chinese_font(run, size=9)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    print(f"已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="阶段 5 Word 组装")
    parser.add_argument("--translations", required=True, help="译文目录（4 处理内容/）")
    parser.add_argument("--output", required=True, help="输出 docx 路径")
    parser.add_argument("--keep-mark", default="on", help="on / off")
    args = parser.parse_args()

    keep_mark = args.keep_mark == "on"
    build_docx(Path(args.translations), Path(args.output), keep_mark)


if __name__ == "__main__":
    main()
