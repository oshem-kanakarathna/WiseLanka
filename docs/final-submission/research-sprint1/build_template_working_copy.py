"""Populate the supplied local UWL template from existing drafts, offline.

Usage: python3 docs/final-submission/research-sprint1/build_template_working_copy.py \
    --template '/path/to/Project Report Template.docx'
No new dissertation prose or participant results are generated. Output is local-only.
"""
import argparse
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import re
from zipfile import ZipFile, ZIP_DEFLATED
from xml.etree import ElementTree as E

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': W}

def element(tag, **attrs):
    return E.Element('{'+W+'}'+tag, {'{'+W+'}'+k: v for k, v in attrs.items()})

def paragraph(text='', style=None):
    p = element('p')
    if style:
        props = element('pPr'); props.append(element('pStyle', val=style)); p.append(props)
    run = element('r'); t = element('t'); t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve'); t.text = text
    run.append(t); p.append(run)
    return p

def field(instruction):
    p = element('p'); f = element('fldSimple', instr=instruction, dirty='true')
    f.append(paragraph('Update this field in Word after captions and pagination are reviewed.')[0]); p.append(f)
    return p

def plain(text):
    text = re.sub(r'!?\[([^\]]*)\]\(([^)]+)\)', r'\1 (\2)', text)
    return text.replace('**', '').replace('`', '')

def table(lines):
    tbl = element('tbl'); props = element('tblPr'); borders = element('tblBorders')
    for side in ['top','left','bottom','right','insideH','insideV']:
        borders.append(element(side, val='single', sz='4', color='B8B8B8'))
    props.append(borders); tbl.append(props)
    for line in lines:
        if re.fullmatch(r'\s*\|?[\s:|\-]+\|?\s*', line): continue
        row = element('tr')
        for cell in line.strip().strip('|').split('|'):
            c = element('tc'); c.append(paragraph(plain(cell.strip()))); row.append(c)
        tbl.append(row)
    return tbl

def markdown(path, appendix=False):
    lines = path.read_text().splitlines(); nodes = []; i = 0; code = False
    for_top = True
    while i < len(lines):
        line = lines[i]; i += 1
        if line.startswith('```'): code = not code; continue
        if not line.strip(): continue
        if line.startswith('|'):
            rows = [line]
            while i < len(lines) and lines[i].startswith('|'): rows.append(lines[i]); i += 1
            nodes.append(table(rows)); continue
        m = re.match(r'^(#{1,6})\s+(.*)',line)
        if m:
            level = len(m[1]); title = m[2]
            if level == 1 and not appendix: continue
            # Source numbering is retained as editorial provenance, not final numbering.
            nodes.append(paragraph(plain(title), 'Heading'+str(min(4, max(2, level if not appendix else level+1)))))
        else:
            nodes.append(paragraph(plain(line), 'ListParagraph' if re.match(r'^(?:[-*]|\d+\.)\s',line) else None))
    return nodes

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--template', type=Path, required=True); args = ap.parse_args()
    template = args.template.resolve()
    expected = json.loads((OUT/'DOCUMENT_REGISTER.json').read_text())['template']['sha256']
    assert hashlib.sha256(template.read_bytes()).hexdigest() == expected, 'Template identity differs; review before use.'
    with ZipFile(template) as source:
        original = source.read('word/document.xml')
        for _, (prefix, uri) in E.iterparse(io.BytesIO(original), events=['start-ns']):
            if not re.fullmatch(r'ns\d+', prefix): E.register_namespace(prefix, uri)
        root = E.fromstring(original); body = root.find('w:body',NS); nodes = []
        replacements = {'Student Name:':'Student Name: Oshem Thirsha Kanakarathna','Student ID:':'Student ID: 34164665',
            'Date: Submission Date':'Date: [CONFIRM ACTUAL SUBMISSION DATE]', 'Supervisor Name:':'Supervisor Name: Dr. Ama Kulathilake',
            'Second Marker:':'Second Marker: [CONFIRM]'}
        baseline = json.loads((ROOT/'alignment/APPROVED_BASELINE.json').read_text())
        for child in body:
            text = ''.join(t.text or '' for t in child.iter('{'+W+'}t'))
            if text == 'Abstract': break
            node = deepcopy(child)
            replacement = replacements.get(text)
            if text.startswith('Project Title:'): replacement = 'Project Title: '+baseline['title']
            if replacement:
                ts = list(node.iter('{'+W+'}t'))
                if ts:
                    ts[0].text = replacement
                    for t in ts[1:]: t.text = ''
            nodes.append(node)
        nodes.append(paragraph('REVISED WORKING DRAFT — research results pending; not final or approved for submission.'))
        nodes.append(paragraph('Module code: originals CP6SL460; supplied guide CP60046E/CP6CS46E. Confirm centre mapping. Published report contingency: 17 December 2026, 5pm; extension and timezone not verified.'))
        nodes.append(paragraph('Editorial note: imported chapter/subsection numbers and internal cross-references still refer to Markdown source drafts. Reconcile after final structure and genuine evaluation. Diagrams/captions and field pagination require manual Word review.'))
        nodes.append(paragraph('Abstract','Title'))
        nodes.append(paragraph('PROVISIONAL — revise last after actual evaluation; the following is the existing bounded technical summary, not final research findings.'))
        front=(ROOT/'chapters/00-front-matter.md').read_text()
        abstract=front.split('### Abstract\n',1)[1].split('### Author review',1)[0].strip()
        nodes.extend(paragraph(plain(p)) for p in abstract.split('\n\n'))
        nodes.append(paragraph('Acknowledgements','Title'))
        nodes.append(paragraph('[AUTHOR TO WRITE: acknowledge genuine assistance only. Confirm permitted AI use and declaration wording. No signature or originality declaration generated.]'))
        nodes.append(paragraph(front.split('### Author review and assistance disclosure\n',1)[1].split('### Reading guide',1)[0].strip()))
        nodes.append(paragraph('Contents','TOCHeading')); nodes.append(field(' TOC \\o "1-3" \\h \\z \\u '))
        nodes.append(paragraph('Figures and Tables','Title'))
        nodes.append(paragraph('List of Figures','Heading2')); nodes.append(field(' TOC \\h \\z \\c "Figure" '))
        nodes.append(paragraph('List of Tables','Heading2')); nodes.append(field(' TOC \\h \\z \\c "Table" '))
        groups=json.loads(json.dumps(list(__import__('csv').DictReader((OUT/'CHAPTER_MAPPING.csv').open()))))
        for group in groups:
            nodes.append(paragraph(group['official_section'],'Heading1'))
            if group['official_section']=='Discussion and Conclusion':nodes.append(paragraph('PROVISIONAL interpretation only. Do not finalise before genuine evaluation and author review.'))
            for name in group['source_chapters'].split('; '):
                nodes.append(paragraph('Imported editable source: chapters/'+name+'. Source references/numbering require final reconciliation.'))
                nodes.extend(markdown(ROOT/'chapters'/name))
        nodes.append(paragraph('References','Heading1')); nodes.extend(markdown(ROOT/'REFERENCES.md'))
        nodes.append(paragraph('Appendices','Heading1'))
        for label in ['Project Progress Form 1','Project Progress Form 2']:
            nodes.append(paragraph(label,'Heading2')); nodes.append(paragraph('[PENDING AUTHENTIC FORM: insert the actual completed/supervisor-signed record. Do not reconstruct signatures, dates or weekly meetings. S2 must also accompany report submission as instructed.]'))
        for path in sorted((ROOT/'appendices').glob('*.md')):nodes.extend(markdown(path,appendix=True))
        for child in body:
            if child.tag=='{'+W+'}sectPr':nodes.append(deepcopy(child))
        content=''.join(E.tostring(n,encoding='unicode') for n in nodes)
        replaced=re.sub(r'(?s)(<w:body\b[^>]*>).*?(</w:body>)',lambda m:m[1]+content+m[2],original.decode('utf-8'),count=1).encode('utf-8')
        assert replaced!=original
        output=OUT/'local-only/WiseLanka_UWL_Template_Working_Draft.docx'; output.parent.mkdir(exist_ok=True)
        assert output.resolve()!=template
        with ZipFile(output,'w',compression=ZIP_DEFLATED) as dest:
            for info in source.infolist():
                data=source.read(info.filename)
                if info.filename=='word/document.xml': data=replaced
                if info.filename=='word/settings.xml':
                    text=data.decode('utf-8')
                    if '<w:updateFields' not in text:text=text.replace('</w:settings>','<w:updateFields w:val="true"/></w:settings>')
                    data=text.encode('utf-8')
                dest.writestr(info,data)
    with ZipFile(output) as z:
        assert z.testzip() is None
        for n in z.namelist():
            if n.endswith('.xml'):E.fromstring(z.read(n))
    with ZipFile(template) as a,ZipFile(output) as b:
        changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
        assert set(changed)<={'word/document.xml','word/settings.xml'}
    print(json.dumps({'output':str(output),'template_sha256':expected,'changed_package_parts':changed,'zip_and_xml_checks':'passed','rendering':'Not performed; Word field/layout/caption review pending','provisional_abstract_and_discussion':True},indent=2))

if __name__=='__main__':main()
