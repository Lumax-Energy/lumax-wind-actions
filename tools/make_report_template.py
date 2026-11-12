"""Build report-template.js from a Word report in the Lumax house style.

The app writes the body of its Word report itself. The letterhead (first-page header art, footers),
styles, theme and fonts come from an existing Lumax report, so the export matches the house style.
This script lifts those parts out of that report and stores them as text in report-template.js,
which index.html loads when a report is downloaded.

Run:  python tools/make_report_template.py "path/to/a Lumax report.docx"
"""
import base64
import json
import re
import sys
import zipfile
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent.parent / 'report-template.js'

TEXT_PARTS = [
    'word/header1.xml', 'word/footer1.xml', 'word/footer2.xml',
    'word/_rels/header1.xml.rels', 'word/_rels/footer1.xml.rels', 'word/_rels/footer2.xml.rels',
    'word/styles.xml', 'word/theme/theme1.xml', 'word/fontTable.xml', 'word/settings.xml',
    'word/footnotes.xml', 'word/endnotes.xml',
]

z = zipfile.ZipFile(SRC)
names = set(z.namelist())
text = {}
for n in TEXT_PARTS:
    assert n in names, f'{n} is missing from {SRC.name}'
    text[n] = z.read(n).decode('utf-8')

# images the header and footers point at
b64 = {}
for rels in ('word/_rels/header1.xml.rels', 'word/_rels/footer1.xml.rels', 'word/_rels/footer2.xml.rels'):
    for target in re.findall(r'Type="[^"]*/image" Target="([^"]+)"', text[rels]):
        part = 'word/' + target
        b64[part] = base64.b64encode(z.read(part)).decode('ascii')

# the model's footer links to "lumaxenergy.coma": a typo behind the visible www.lumaxenergy.com
for rels in ('word/_rels/footer1.xml.rels', 'word/_rels/footer2.xml.rels'):
    text[rels] = text[rels].replace('http://www.lumaxenergy.coma"', 'http://www.lumaxenergy.com"')
    assert '.coma"' not in text[rels]

# the opening <w:document ...> tag carries every namespace the header, footer and body use
doc = z.read('word/document.xml').decode('utf-8')
doc_open = doc[:doc.index('<w:body>')]

# the section must be the house layout: A4, first-page header, default and first-page footers
sect = doc[doc.rindex('<w:sectPr'):]
assert '<w:titlePg/>' in sect and 'w:type="first"' in sect, 'unexpected section layout'
pg = re.search(r'<w:pgSz[^>]*/><w:pgMar[^>]*/>', sect).group(0)

js = ('/* Letterhead, styles, theme and fonts of the Lumax report template, lifted from a house-style Word report\n'
      '   by tools/make_report_template.py. index.html loads this when a Word report is downloaded. */\n'
      'window.LX_TPL = ' + json.dumps({'docOpen': doc_open, 'page': pg, 'text': text, 'b64': b64},
                                      ensure_ascii=False, separators=(',', ':')) + ';\n'
      'if (typeof window.lxTemplateReady === "function") window.lxTemplateReady();\n')
OUT.write_text(js, encoding='utf-8', newline='\n')
print(f'{OUT.name}: {len(js) / 1024:.0f} KB; text parts {len(text)}, images {list(b64)}; page {pg}')
