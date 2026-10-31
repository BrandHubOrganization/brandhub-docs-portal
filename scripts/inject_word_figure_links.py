#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates FIGURE_LINKS_MAPPING.md and optionally injects clickable external hyperlinks
into Figure captions (Figure 1 .. Figure 150) in report3_official.docx.
"""
import argparse
import json
import re
from pathlib import Path
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE

PORTAL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PORTAL_DIR / "src" / "data"
DEFAULT_DOCX = Path(r"d:\ProjectCode\BrandHub\brandhub-final_report\report3\report3_official.docx")
MAPPING_MD_PATH = PORTAL_DIR / "FIGURE_LINKS_MAPPING.md"


def add_external_hyperlink(paragraph, url: str, text: str):
    """Replaces paragraph text with a clickable external hyperlink while preserving italic/center formatting."""
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    # Clear existing runs
    for r in list(paragraph.runs):
        r._r.getparent().remove(r._r)

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")

    # Italic + Blue underline for clickable figure caption
    i_el = OxmlElement("w:i")
    rPr.append(i_el)

    color = OxmlElement("w:color")
    color.set(qn("w:val"), "2563EB")
    rPr.append(color)

    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)

    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def export_markdown_mapping(base_url: str):
    proj = json.loads((DATA_DIR / "project.json").read_text(encoding="utf-8"))
    cloud_name = proj["projectInfo"]["cloudinaryCloudName"]
    figures = []
    for fname in [
        "report1.json",
        "report2.json",
        "report3-overview.json",
        "report3-screens.json",
        "report4-class.json",
        "report4-sequence.json",
    ]:
        figures.extend(json.loads((DATA_DIR / "figures" / fname).read_text(encoding="utf-8")))
    lines = [
        "# BrandHub Documentation Portal — Danh sách Đường Link 312 Figures & Cloudinary HD",
        "",
        f"- **Portal Base URL**: `{base_url}`",
        f"- **Cloudinary Cloud Name**: `{cloud_name}`",
        f"- **Tổng số Figures**: **{len(figures)}** (Report 1: 5, Report 2: 7, Report 3 SRS: 150, Report 4 SDD: 150)",
        "",
        "| Figure ID | Báo cáo | Mục | Số Figure | Caption trong Tài liệu Word | Link Trang Portal (Gắn vào Word) | Link Ảnh Nét Cloudinary CDN |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]
    for fig in figures:
        portal_link = f"{base_url}/figures/{fig['id']}"
        lines.append(
            f"| `{fig['id']}` | {fig['reportId'].upper()} | `{fig['section']}` | **Figure #{fig['figNum']}** | {fig['caption']} | [{portal_link}]({portal_link}) | [Cloudinary HD]({fig['imageUrl']}) |"
        )

    MAPPING_MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Saved Markdown mapping ({len(figures)} figures) -> {MAPPING_MD_PATH}")


def inject_links_into_docx(docx_path: Path, output_path: Path, base_url: str):
    doc = Document(str(docx_path))
    fig_re = re.compile(r"^Figure\s+(\d+)\s*[-–—]\s*(.+)$", re.IGNORECASE)
    count = 0

    for p in doc.paragraphs:
        txt = p.text.strip()
        m = fig_re.match(txt)
        if m:
            fig_num = int(m.group(1))
            if 1 <= fig_num <= 150:
                fig_id = f"r3-fig-{fig_num}"
                url = f"{base_url}/figures/{fig_id}"
                add_external_hyperlink(p, url, txt)
                count += 1

    doc.save(str(output_path))
    print(f"Injected {count} clickable Figure hyperlinks into -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Export Figure Link Mapping and optionally inject links into Word docx.")
    parser.add_argument("--base-url", default="http://localhost:5180", help="Base URL of the deployed React portal")
    parser.add_argument("--inject-docx", action="store_true", help="Also inject hyperlinks into report3_official.docx")
    parser.add_argument("--docx-in", default=str(DEFAULT_DOCX), help="Input docx file path")
    parser.add_argument("--docx-out", default="", help="Output docx file path (defaults to overwriting input)")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    export_markdown_mapping(base_url)

    if args.inject_docx:
        in_path = Path(args.docx_in)
        out_path = Path(args.docx_out) if args.docx_out else in_path
        inject_links_into_docx(in_path, out_path, base_url)


if __name__ == "__main__":
    main()
