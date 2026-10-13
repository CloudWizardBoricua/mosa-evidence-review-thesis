"""Prepare a readable presentation copy while preserving the archived source.

Usage: python thesis/format_original_thesis.py --input original.docx --output copy.docx
Export the copy through Word and refresh its four static navigation tables.
The original file is never saved or overwritten.
"""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from docx.text.paragraph import Paragraph
from PIL import ImageFont


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def set_element(parent, name, value=None):
    element = parent.find(qn('w:' + name))
    if element is None:
        element = OxmlElement('w:' + name)
        parent.append(element)
    if value is not None:
        element.set(qn('w:val'), value)
    return element


def normalized(text):
    return re.sub(r'\s+', ' ', text).strip().replace('(A RCI)', '(ARCI)')


def wrap_words(text, width_points, points, bold=False):
    """Use the export font's metrics to place line breaks only between words."""
    font = ImageFont.truetype('C:/Windows/Fonts/timesbd.ttf' if bold else 'C:/Windows/Fonts/times.ttf', round(points * 20))
    limit = max(10, width_points - 8) * 20
    lines, words = [], []
    for word in normalized(text).split():
        candidate = ' '.join(words + [word])
        if words and font.getlength(candidate) > limit:
            lines.append(' '.join(words))
            words = []
        words.append(word)
    if words:
        lines.append(' '.join(words))
    return '\n'.join(lines)


def repair_roadmap(doc, output):
    """Retain Figure 16's five source intervals and move labels outside bars."""
    from reportlab.pdfgen import canvas
    phases = ['Define and baseline', 'Pilot and calibrate', 'Automate and expand', 'Embed in acquisition', 'Federate and scale']
    intervals = []
    for row in doc.tables[38].rows[1:]:
        match = re.search(r'(\d+)\s+to\s+(\d+)\s+months', normalized(row.cells[0].text))
        if match is None:
            raise ValueError('Cannot read a source roadmap interval.')
        intervals.append(tuple(map(int, match.groups())))
    assert intervals == [(0, 6), (6, 12), (12, 18), (18, 24), (24, 36)]
    chart_pdf = output.with_name('original-roadmap-chart.pdf')
    chart = canvas.Canvas(str(chart_pdf), pagesize=(720, 418))
    chart.setFont('Times-Bold', 18)
    chart.drawCentredString(360, 390, 'MOSA conformance harness implementation roadmap')
    left, right, baseline, top = 230, 705, 70, 350
    for tick in range(0, 37, 6):
        x = left + (right-left) * tick / 36
        chart.setStrokeColorRGB(.85, .88, .91)
        chart.setLineWidth(.6)
        chart.line(x, baseline, x, top)
        chart.setFillColorRGB(.12, .16, .20)
        chart.setFont('Times-Roman', 15)
        chart.drawCentredString(x, 49, str(tick))
    for i, (start, end) in enumerate(intervals):
        y = 330 - 56*i
        chart.setFillColorRGB(.12, .16, .20)
        chart.setFont('Times-Roman', 16)
        chart.drawRightString(left-18, y-5, phases[i])
        x = left + (right-left)*start/36
        width = (right-left)*(end-start)/36
        chart.setFillColorRGB(.125, .329, .576)
        chart.rect(x, y-17, width, 34, fill=1, stroke=0)
        chart.setFillColorRGB(1, 1, 1)
        chart.drawCentredString(x+width/2, y-5, f'{start}-{end}')
    chart.setFillColorRGB(.12, .16, .20)
    chart.setFont('Times-Roman', 15)
    chart.drawCentredString((left+right)/2, 23, 'Months from implementation start')
    chart.setStrokeColorRGB(.12, .16, .20)
    chart.line(left, baseline, right, baseline)
    chart.save()
    image = output.with_name('original-roadmap.png')
    renderer = Path(sys.executable).resolve().parent.parent / 'native/poppler/Library/bin/pdftoppm.exe'
    if not renderer.exists():
        raise FileNotFoundError('Use the bundled Python runtime with its Poppler renderer.')
    subprocess.run([str(renderer), '-singlefile', '-r', '220', '-png', str(chart_pdf), str(image.with_suffix(''))], check=True)
    shape = doc.inline_shapes[-1]
    relation = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
    doc.part.related_parts[relation]._blob = image.read_bytes()
    # Keep the existing figure's physical size and caption placement.
    return {'figure': 16, 'intervals_months': intervals, 'labels': phases,
            'change': 'Labels moved outside bars to prevent clipping.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--metadata', default=str(Path(__file__).with_name('thesis_content.json')))
    args = parser.parse_args()
    source, output = Path(args.input).resolve(), Path(args.output).resolve()
    if source == output:
        raise ValueError('The archived original must not be overwritten.')
    original_hash = sha256(source)
    doc = Document(source)
    metadata = json.loads(Path(args.metadata).read_text(encoding='utf-8'))['metadata']
    assert metadata['committee'][:2] == ['Dr. John Hassell, Chair', 'Dr. Christopher Freeze']
    abstract_index = next(i for i, p in enumerate(doc.paragraphs) if p.text == 'Abstract')
    body_before = [p.text for p in doc.paragraphs[abstract_index:]]
    tables_before = [[c.text for row in t.rows for c in row.cells] for t in doc.tables]
    pictures_before = len(doc.inline_shapes)

    # Repair the committee list without changing the research body.
    first = next(p for p in doc.paragraphs if p.text == metadata['committee'][0])
    second = next(p for p in doc.paragraphs if p.text == metadata['committee'][1])
    marker = next(p for p in doc.paragraphs if p.text == 'BY THE COMMITTEE CONSISTING OF')
    marker.text = ''
    marker.paragraph_format.space_after = Pt(18)
    marker.paragraph_format.space_before = Pt(0)
    for p in (first, second, marker):
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_after = Pt(10 if p is not marker else 18)
        for run in p.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.bold = p is marker
    previous = second
    for name in metadata['committee'][2:]:
        element = deepcopy(second._p)
        previous._p.addnext(element)
        paragraph = Paragraph(element, second._parent)
        paragraph.text = name
        for run in paragraph.runs:
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
        previous = paragraph
    label = next(p for p in doc.paragraphs if p.text == 'A THESIS APPROVED FOR THE')
    label.text = 'THESIS COMMITTEE'
    label.alignment = WD_ALIGN_PARAGRAPH.CENTER
    label.paragraph_format.first_line_indent = Inches(0)
    label.paragraph_format.space_after = Pt(16)
    for r in label.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True
    college = next(p for p in doc.paragraphs if p.text == metadata['college'].upper())
    college.text = metadata['college'].upper().replace(' AND THE ', '\nAND THE ')
    college.paragraph_format.space_after = Pt(28)
    college.paragraph_format.first_line_indent = Inches(0)
    college.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in college.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        r.bold = True

    # The body style's half-inch first-line indent must never enter table cells.
    for index, table in enumerate(doc.tables):
        navigation = index < 4
        equation = len(table.rows) == 1 and re.fullmatch(r'\(\d+\)', table.cell(0, 1).text.strip())
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        widths = {
            4: [1.08, 2.17, 1.08, 2.17],
            10: [.9, 1.02, 1.25, 1.18, 1.15, 1.0],
            11: [1.35, 2.1, 2.05, 1.0],
            22: [.8, 3.0, 2.6],
            34: [1.0, 1.25, 2.25, .75, 1.25],
        }.get(index)
        if widths:
            for col, width in zip(table.columns, widths):
                col.width = Inches(width)
            for row in table.rows:
                for cell, width in zip(row.cells, widths):
                    cell.width = Inches(width)
        for row_number, row in enumerate(table.rows):
            trpr = row._tr.get_or_add_trPr()
            for height in list(trpr.findall(qn('w:trHeight'))):
                trpr.remove(height)
            set_element(trpr, 'cantSplit')
            if row_number == 0 and not navigation and not equation:
                set_element(trpr, 'tblHeader')
            for column, cell in enumerate(row.cells):
                cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
                for paragraph in cell.paragraphs:
                    if not equation:
                        was_bold = any(run.bold for run in paragraph.runs)
                        points = 10 if index in (49, 50) else (10.5 if len(table.columns) <= 4 else 9.5)
                        paragraph.text = wrap_words(paragraph.text, cell.width.pt - (0 if navigation else 6.5), points, was_bold)
                        for run in paragraph.runs:
                            run.bold = was_bold
                    pf = paragraph.paragraph_format
                    pf.first_line_indent = Inches(0)
                    pf.left_indent = Inches(0)
                    pf.right_indent = Inches(0)
                    pf.space_before = Pt(0)
                    pf.space_after = Pt(0)
                    pf.line_spacing = 1.0 if navigation or equation else 1.08
                    pf.keep_with_next = False
                    set_element(paragraph._p.get_or_add_pPr(), 'wordWrap', '0')
                    if equation:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT if column else WD_ALIGN_PARAGRAPH.CENTER
                        continue
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    if navigation and column == 1:
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    elif not navigation and (row_number == 0 or re.fullmatch(r'[\d.,%/]+|Pass|Fail|[RACI]', paragraph.text.strip())):
                        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    for run in paragraph.runs:
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(points)
                        run._r.get_or_add_rPr().append(OxmlElement('w:noProof'))
                tcpr = cell._tc.get_or_add_tcPr()
                margins = tcpr.find(qn('w:tcMar'))
                if margins is not None:
                    tcpr.remove(margins)
                margins = OxmlElement('w:tcMar')
                for edge in ('top', 'bottom', 'left', 'right'):
                    item = OxmlElement('w:' + edge)
                    item.set(qn('w:w'), '0' if navigation else (('20' if index == 4 else '30') if edge in ('top', 'bottom') else '65'))
                    item.set(qn('w:type'), 'dxa')
                    margins.append(item)
                tcpr.append(margins)

    for p in doc.paragraphs:
        if p.style.name in ('Heading 1', 'Heading 2', 'Table Caption'):
            p.paragraph_format.keep_with_next = True
        if p._p.findall('.//' + qn('w:drawing')):
            p.paragraph_format.first_line_indent = Inches(0)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.line_spacing = 1.0
    for picture in doc.inline_shapes:
        if picture.width > Inches(6.5):
            ratio = Inches(6.5) / picture.width
            picture.width = Inches(6.5)
            picture.height = round(picture.height * ratio)

    abstract_after = next(i for i, p in enumerate(doc.paragraphs) if p.text == 'Abstract')
    assert body_before == [p.text for p in doc.paragraphs[abstract_after:]], 'Body prose was changed.'
    assert [[normalized(v) for v in row] for row in tables_before] == [[normalized(c.text) for row in t.rows for c in row.cells] for t in doc.tables], 'Table values were changed.'
    assert pictures_before == len(doc.inline_shapes), 'Embedded figures were lost.'
    output.parent.mkdir(parents=True, exist_ok=True)
    roadmap = repair_roadmap(doc, output)
    doc.save(output)
    assert sha256(source) == original_hash
    print(json.dumps({'output': str(output), 'source_sha256': original_hash,
                      'committee': metadata['committee'], 'tables_reformatted': len(doc.tables),
                      'body_prose_unchanged': True, 'table_values_unchanged': True,
                      'embedded_figures_preserved': pictures_before,
                      'roadmap_layout_repair': roadmap}, indent=2))


if __name__ == '__main__':
    main()
