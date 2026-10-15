#!/usr/bin/env python3
"""Generate the downloadable CV from the website's _data/cv.yml.

Install dependencies with: python3 -m pip install reportlab PyYAML
Run from any directory: python3 bin/generate_cv.py --updated 2026-10-15
The bio is intentionally not used by this generator.
"""

import argparse
from datetime import date
from html import escape
from html.parser import HTMLParser
from pathlib import Path

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
ACCENT = colors.HexColor('#8b235a')
INK = colors.HexColor('#202631')
MUTED = colors.HexColor('#59616d')


class InlineHTML(HTMLParser):
    """Preserve the CV's simple inline links and formatting for ReportLab."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a' and attrs.get('href'):
            self.parts.append(f'<a href="{escape(attrs["href"], quote=True)}" color="#8b235a">')
        elif tag in ('b', 'i', 'strong', 'em'):
            self.parts.append('<' + {'strong': 'b', 'em': 'i'}.get(tag, tag) + '>')
        elif tag == 'br':
            self.parts.append('<br/>')

    def handle_endtag(self, tag):
        if tag in ('a', 'b', 'i', 'strong', 'em'):
            self.parts.append('</' + {'strong': 'b', 'em': 'i'}.get(tag, tag) + '>')

    def handle_data(self, data):
        self.parts.append(escape(data))


def inline(value):
    parser = InlineHTML()
    parser.feed(str(value).replace('\u2013', '-').replace('\u2014', '-'))
    return ''.join(parser.parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--updated', type=date.fromisoformat, default=date.today())
    parser.add_argument('--output', type=Path, default=ROOT / 'assets/pdf/alejandro_benito-santos_cv.pdf')
    args = parser.parse_args()
    sections = yaml.safe_load((ROOT / '_data/cv.yml').read_text())
    socials = yaml.safe_load((ROOT / '_data/socials.yml').read_text())
    general = {item['name']: item['value'] for item in sections[0]['contents']}

    body = ParagraphStyle('Body', fontName='Helvetica', fontSize=9.2, leading=12.5,
                          textColor=INK, spaceAfter=3, alignment=TA_LEFT)
    small = ParagraphStyle('Small', parent=body, fontSize=8.4, leading=11, textColor=MUTED)
    title = ParagraphStyle('Name', parent=body, fontName='Helvetica-Bold', fontSize=24,
                           leading=28, spaceAfter=7)
    heading = ParagraphStyle('Heading', parent=body, fontName='Helvetica-Bold', fontSize=12.5,
                             leading=16, textColor=ACCENT, spaceBefore=10, spaceAfter=6,
                             keepWithNext=True)
    entry_title = ParagraphStyle('Entry', parent=body, fontName='Helvetica-Bold', spaceAfter=2)
    bullet = ParagraphStyle('Bullet', parent=body, leftIndent=9, firstLineIndent=-9, spaceAfter=5)
    story = [Paragraph(inline(general['Full Name']), title),
             Paragraph(inline(general['Position']), body),
             Paragraph(f'<a href="mailto:{escape(socials["email"], quote=True)}" color="#8b235a">'
                       f'{escape(socials["email"])}</a> | '
                       '<a href="https://alexbs.me" color="#8b235a">alexbs.me</a> | '
                       f'{inline(general["Location"])}', small), Spacer(1, 7)]

    width = A4[0] - 88
    for section in sections:
        story.append(Paragraph(inline(section['title']), heading))
        kind = section['type']
        if kind == 'map':
            for item in section['contents']:
                if section is sections[0] and item['name'] in ('Full Name', 'Position', 'Location'):
                    continue  # Already displayed in the document header.
                story.append(Paragraph(f'<b>{inline(item["name"])}:</b> {inline(item["value"])}', body))
        elif kind == 'list':
            for item in section['contents']:
                story.append(Paragraph('- ' + inline(item), bullet))
        elif kind == 'time_table':
            for item in section['contents']:
                details = [Paragraph(inline(item['title']), entry_title)]
                if item.get('institution'):
                    details.append(Paragraph(inline(item['institution']), small))
                for description in item.get('description', []):
                    details.append(Paragraph(inline(description), body))
                links = [f'<a href="{escape(link["link"], quote=True)}" color="#8b235a">'
                         f'{escape(link.get("linkname", "Link"))}</a>'
                         for link in item.get('linkitems', [])]
                if links:
                    details.append(Paragraph(' | '.join(links), small))
                table = Table([[Paragraph(inline(item.get('year', '')), small), details]],
                              colWidths=[72, width - 72])
                table.setStyle(TableStyle([
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 0),
                    ('RIGHTPADDING', (0, 0), (0, 0), 10),
                    ('RIGHTPADDING', (1, 0), (1, 0), 0),
                    ('TOPPADDING', (0, 0), (-1, -1), 1),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ]))
                story.append(table)
        else:
            raise ValueError(f'Unsupported CV section type: {kind}')

    story.append(Spacer(1, 9))
    story.append(Paragraph('Full publication list: '
                           '<a href="https://alexbs.me/publications/" color="#8b235a">'
                           'alexbs.me/publications</a>', body))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#dce0e5'))
        canvas.line(44, 34, A4[0] - 44, 34)
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(44, 21, 'Alejandro Benito-Santos | Curriculum vitae')
        stamp = f'Updated {args.updated.day} {args.updated:%B %Y} | {doc.page}'
        canvas.drawRightString(A4[0] - 44, 21, stamp)
        canvas.restoreState()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(args.output), pagesize=A4, leftMargin=44, rightMargin=44,
                                 topMargin=38, bottomMargin=49,
                                 title='Alejandro Benito-Santos - Curriculum Vitae',
                                 author='Alejandro Benito-Santos')
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f'Generated {args.output}')


if __name__ == '__main__':
    main()
