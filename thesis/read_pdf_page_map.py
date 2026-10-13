"""Read verified PDF locations for cached Word navigation fields.

This utility must operate on a rendered thesis PDF. It does not guess pagination.
The root agent still reviews every page image after the resulting rebuild.
"""
import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader


def normalized(text):
    return re.sub(r'\s+', ' ', text).strip()


def roman(number):
    result = ''
    for value, token in [(1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'), (100, 'c'), (90, 'xc'), (50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'), (5, 'v'), (4, 'iv'), (1, 'i')]:
        while number >= value:
            result += token
            number -= value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf')
    parser.add_argument('--content', default=str(Path(__file__).parent / 'thesis_content.json'))
    parser.add_argument('--output', default=str(Path(__file__).parent / 'page_map.json'))
    args = parser.parse_args()
    content = json.loads(Path(args.content).read_text(encoding='utf-8'))
    document = PdfReader(args.pdf)
    texts = [normalized(page.extract_text() or '') for page in document.pages]
    body_start = next((i for i, text in enumerate(texts) if text.startswith('Chapter 1 ')), None)
    if body_start is None:
        raise ValueError('Cannot locate the rendered first chapter heading.')
    page_map = {}
    physical = {}
    def register(bookmark, index):
        page_map[bookmark] = str(index - body_start + 1) if index >= body_start else roman(index + 1)
        physical[bookmark] = index + 1
    for label, bookmark in [('Abstract', 'front_abstract'), ('List of Figures', 'front_figures'), ('Reader Guide', 'front_reader')]:
        index = next((i for i, text in enumerate(texts[:body_start]) if text.startswith(label)), None)
        if index is not None:
            register(bookmark, index)
    headings = [(f'Chapter {c["number"]} ' + c['title'], 'chapter_' + str(c['number'])) for c in content['chapters']]
    headings += [('References', 'references'), ('Glossary', 'glossary')]
    headings += [('Appendix ' + chr(65 + i) + ' ' + a['title'], 'appendix_' + chr(65 + i)) for i, a in enumerate(content['appendices'])]
    for label, bookmark in headings:
        index = next((i for i, text in enumerate(texts) if i >= body_start and text.startswith(normalized(label))), None)
        if index is None:
            raise ValueError('Cannot locate rendered heading: ' + label)
        register(bookmark, index)
    figures = [sec['figure'] for chapter in content['chapters'] for sec in chapter['sections'] if 'figure' in sec]
    figures += [sec['figure'] for appendix in content['appendices'] for sec in appendix['sections'] if 'figure' in sec]
    for number, spec in enumerate(figures, 1):
        needle = normalized(f'Figure {number}. ' + spec['caption'])
        index = next((i for i, text in enumerate(texts) if i >= body_start and needle in text), None)
        if index is None:
            raise ValueError('Cannot locate rendered caption: ' + needle)
        register('fig_' + spec['id'].replace('-', '_'), index)
    Path(args.output).write_text(json.dumps(page_map, indent=2), encoding='utf-8')
    print(json.dumps({'pdf_pages': len(document.pages), 'body_start_physical': body_start + 1, 'page_map': page_map, 'physical_pages': physical, 'output': args.output}, indent=2))


if __name__ == '__main__':
    main()
