"""Export the bilingual macro interview rounds to a group-ready TXT and a PDF."""
import argparse
import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "quiz" / "pages"))
from macro_interview import PAGE


def round_text(section, index):
    questions = section["blocks"]
    heading = (f"【{PAGE['title']}｜第 {index:02d} 輪】{section['title']}\n"
               f"{section['scope']} · {section['en']} · Q{questions[0]['number']:03d}-Q{questions[-1]['number']:03d}")
    return heading + "\n\n" + "\n\n".join(
        f"Q{q['number']:03d}  {q['questionZh']}\n{q['questionEn']}" for q in questions)


def export_pdf(filename, font_regular, font_medium):
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.lib.colors import HexColor

    for name, path in (("InterviewTC", font_regular), ("InterviewTCMedium", font_medium)):
        if not path.is_file():
            raise SystemExit(f"Supply an embeddable Traditional Chinese TrueType font for {name}: {path}")
        font = TTFont(name, str(path), subfontIndex=0)
        pdfmetrics.registerFont(font)
        text = "".join(s["title"] + "".join(q["questionZh"] + q["answerZh"] for q in s["blocks"])
                       for s in PAGE["sections"])
        missing = sorted({c for c in text if not c.isspace() and not font.face.charToGlyph.get(ord(c))})
        if missing:
            raise ValueError(f"{name} lacks glyphs: {''.join(missing)}")

    width, margin = 452, 26
    body_width = width - 2 * margin
    ink, muted, teal, rule = "#182C37", "#415866", "#12666A", "#C2D4D3"
    sections = PAGE["sections"]
    blocks = [
        ("questionZh", "InterviewTCMedium", 13.6, 17.3, 0, 0, ink),
        ("questionEn", "Helvetica-Oblique", 10.5, 13.5, 0, 2, muted),
        ("answerZh", "InterviewTC", 12.0, 15.8, 10, 6, ink),
        ("answerEn", "Helvetica", 10.6, 13.5, 10, 2, muted),
    ]
    tokens = re.compile(r"[A-Za-z0-9³]+(?:['./-][A-Za-z0-9³]+)*|\s+|.", re.S)
    close = "，。！？、）】」』,.?!)]"

    def wrap(text, font, size, room):
        lines, current = [], []
        for token in tokens.findall(text):
            if not current and token.isspace():
                continue
            if current and pdfmetrics.stringWidth("".join(current) + token, font, size) > room:
                while current and current[-1].isspace():
                    current.pop()
                carry = []
                if len(current) > 1 and (token in close or current[-1] in "（【「『(["):
                    carry = [current.pop()]
                if current:
                    lines.append("".join(current).strip())
                current = carry
            if current or not token.isspace():
                current.append(token)
        if current:
            lines.append("".join(current).strip())
        if any(pdfmetrics.stringWidth(line, font, size) > room + 0.1 for line in lines):
            raise ValueError(f"Line too wide: {text}")
        return lines

    prepared = {}
    for section in sections:
        for q in section["blocks"]:
            rows, height = [], 17
            for field, font, size, leading, indent, gap, color in blocks:
                lines = wrap(q[field], font, size, body_width - indent)
                rows.append((lines, font, size, leading, indent, gap, color))
                height += gap + len(lines) * leading
            prepared[q["number"]] = (height, rows)
    fullest = max(sum(prepared[q["number"]][0] for q in s["blocks"]) for s in sections)
    page_h = max(790, math.ceil((fullest + 97 + 40 + 4 * 13) / 10) * 10)
    pdf = Canvas(str(filename), pagesize=(width, page_h), pageCompression=1, invariant=1)
    pdf.setTitle(PAGE["title"] + " | Bilingual interview notes")
    pdf.setAuthor("JAM M1 Drill")
    pdf.setSubject("Gray Paper v0.8.0 | 20 rounds | 100 bilingual questions and short answers")

    def label(x, y, value, font="Helvetica", size=10, color=ink, right=False):
        pdf.setFont(font, size)
        pdf.setFillColor(HexColor(color))
        if right:
            pdf.drawRightString(x, y, value)
        else:
            pdf.drawString(x, y, value)

    def line(x1, y1, x2, y2):
        pdf.setStrokeColor(HexColor(rule))
        pdf.setLineWidth(.6)
        pdf.line(x1, y1, x2, y2)

    def top(right_text):
        label(margin, page_h-28, "JAM  /  PROTOCOL STUDIES", "Helvetica-Bold", 9, teal)
        label(width-margin, page_h-28, right_text, "Helvetica", 9, muted, right=True)

    def footer(page):
        line(margin, 29, width-margin, 29)
        label(margin, 15, "Gray Paper v0.8.0", size=8.5, color=muted)
        pdf.linkURL(PAGE["sourceIndex"], (margin, 11, margin+86, 25), relative=0)
        if page > 1:
            label(width/2-22, 15, "回到目錄", "InterviewTC", 9, teal)
            pdf.linkRect("", "index", (width/2-25, 10, width/2+23, 26), relative=0, thickness=0)
        label(width-margin, 15, f"{page:02d} / {len(sections)+1:02d}", size=9, color=muted, right=True)

    pdf.bookmarkPage("index")
    pdf.addOutlineEntry("目錄 / Contents", "index")
    top("INTERVIEW QUESTIONS   /   ZH + EN")
    label(margin, page_h-77, PAGE["title"], "InterviewTCMedium", 25)
    label(margin, page_h-101, "100 questions on the JAM protocol", "Helvetica", 15, muted)
    label(margin, page_h-131, "中英文口述題與短答，每輪五題。", "InterviewTC", 12)
    label(margin, page_h-151, "點輪次可跳頁。每題上方的章號連到 v0.8.0 原文。", "InterviewTC", 10.5, muted)
    index_top = page_h-174
    spacing = (index_top-40)/len(sections)
    for i, section in enumerate(sections, 1):
        y = index_top-(i-1)*spacing
        line(margin, y+2, width-margin, y+2)
        label(margin, y-14, f"{i:02d}", "Helvetica-Bold", 10, teal)
        label(margin+28, y-13, section["title"], "InterviewTCMedium", 11.5)
        label(margin+28, y-25, section["scope"] + "   /   " + section["en"], size=9.4, color=muted)
        label(width-margin, y-14, f"{(i-1)*5+1:03d}-{i*5:03d}", size=9.3, color=teal, right=True)
        pdf.linkRect("", section["id"], (margin, y-spacing+2, width-margin, y+2), relative=0, thickness=0)
    footer(1)
    pdf.showPage()

    for index, section in enumerate(sections, 1):
        pdf.bookmarkPage(section["id"])
        pdf.addOutlineEntry(f"{index:02d}  {section['title']}", section["id"])
        top(f"{section['scope']}     /     ROUND   {index:02d} / {len(sections):02d}")
        label(margin, page_h-58, section["title"], "InterviewTCMedium", 20)
        label(margin, page_h-77, section["en"], size=12, color=muted)
        line(margin, page_h-86, width-margin, page_h-86)
        qs = section["blocks"]
        y = page_h-97
        gap = (y-40-sum(prepared[q["number"]][0] for q in qs))/(len(qs)-1)
        for j, q in enumerate(qs):
            height, rows = prepared[q["number"]]
            card_top = y
            label(margin, y-8, f"Q{q['number']:03d}", "Helvetica-Bold", 9.2, teal)
            x = margin+35
            for ref in q["refs"]:
                source = PAGE["sources"][ref]
                tag = source.get("label") or ("§"+ref if ref.isdigit() else "App. "+ref)
                label(x, y-8, tag, size=8.8, color=muted)
                end = x+pdfmetrics.stringWidth(tag, "Helvetica", 8.8)
                url = source["url"]
                if ref in q["passages"]:
                    url = url.split("#")[0] + f"#L{q['passages'][ref]}"
                pdf.linkURL(url, (x-2,y-12,end+2,y+3), relative=0)
                x = end+10
            y -= 17
            for lines, font, size, leading, indent, before, color in rows:
                y -= before
                if indent and font == "InterviewTC":
                    answer_top = y
                for row in lines:
                    label(margin+indent, y-size, row, font, size, color)
                    y -= leading
            line(margin+2, answer_top-2, margin+2, y+2)
            assert abs(card_top-y-height) < .01 and y >= 39.9
            if j+1 < len(qs):
                line(margin, y-gap/2, width-margin, y-gap/2)
                y -= gap
        footer(index+1)
        pdf.showPage()
    pdf.save()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "macro")
    parser.add_argument("--font-regular", type=Path, default=Path("/System/Library/Fonts/STHeiti Light.ttc"))
    parser.add_argument("--font-medium", type=Path, default=Path("/System/Library/Fonts/STHeiti Medium.ttc"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    title = PAGE["title"] + "（群組題目版）\nGray Paper v0.8.0 · 20 輪，每輪 5 題\n" + PAGE["sourceIndex"]
    rounds = [round_text(section, i) for i, section in enumerate(PAGE["sections"], 1)]
    (args.out / "jam-100-questions.txt").write_text(title + "\n\n\n" + "\n\n\n".join(rounds) + "\n", encoding="utf-8")
    export_pdf(args.out / "jam-100-answers.pdf", args.font_regular, args.font_medium)


if __name__ == "__main__":
    main()
