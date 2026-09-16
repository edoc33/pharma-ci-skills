#!/usr/bin/env python3
"""Build the offline handout, mobile PDF and downloadable ZIP from tracked sources.

Install build-only dependencies with: python3 -m pip install markdown reportlab
Run from any directory: python3 scripts/build_starter_pack.py
"""
import csv
import html
import json
import shutil
import zipfile
from pathlib import Path

import markdown
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'docs/starter-pack'
OUT = ROOT / 'dist'
DOWNLOAD = 'https://github.com/edoc33/pharma-ci-skills/releases/latest/download/'
ONLINE = 'https://github.com/edoc33/pharma-ci-skills/tree/main/docs/starter-pack/'


def main():
    rows = list(csv.DictReader((PACK / 'source-directory.csv').open()))
    counts = f"{len({r['Source ID'] for r in rows})} source entries across {len(rows)} URLs"
    # Keep the skill examples and API-ready shape synchronized with the attendee directory.
    api_rows = [{
        'url':r['URL'], 'title':r['Title'], 'rule':r['Alert me when prompt'],
        'interval':'1440', 'owner':'unassigned', 'backup':'unassigned',
        'recheck_by':r['Recheck-by'], 'decision_served':'Choose before enabling',
        'delivery_policy':'', 'maintenance_owner':'unassigned', 'capture_scope':r['Source role'],
    }for r in rows]
    with (PACK/'api-watchlist.csv').open('w',newline='')as f:
        writer=csv.DictWriter(f,fieldnames=list(api_rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(api_rows)
    examples=ROOT/'plugins/pharma-ci/examples'
    for name in ('import-tab.csv','prompt-guide-tab.csv','source-directory.csv','review-item-template.csv','review-item-schema.json','triage-prompt.txt'):
        shutil.copy2(PACK/name,examples/name)
    shutil.copy2(PACK/'import-tab.csv',examples/'starter-import.csv')
    shutil.copy2(PACK/'api-watchlist.csv',examples/'starter-prompt-guide.csv')
    evidence = json.loads((PACK / 'evidence/catalog.json').read_text())
    events = {e['key']: e for e in evidence['examples']}

    def crop(key, kind='comparison'):
        return PACK / events[key][kind]

    css = '''
    *{box-sizing:border-box}body{margin:0;background:#f7f9fe;color:#0c2235;font:18px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    main{max-width:960px;margin:auto;padding:56px 28px}h1,h2,h3{line-height:1.2}h1{font-size:clamp(38px,7vw,64px);letter-spacing:-.03em;margin:0 0 20px}h2{font-size:30px;margin-top:44px}h3{font-size:23px}p{max-width:760px}a{color:#0b51ae;text-underline-offset:3px}img{max-width:100%;height:auto;display:block;background:white}figure{margin:24px 0}figcaption,.small{font-size:14px;color:#526066}.links{display:flex;flex-wrap:wrap;gap:12px;margin:24px 0}.links a,button{padding:10px 16px;background:white;border:1px solid #aab8bd;border-radius:5px;font:inherit;color:#0b51ae;cursor:pointer}details{border-top:1px solid #cbd2d4;padding:20px 0}summary{font-size:24px;cursor:pointer}.detail-body{padding-top:8px}table{border-collapse:collapse;width:100%;font-size:15px}th,td{padding:10px 8px;border-bottom:1px solid #cbd2d4;text-align:left;vertical-align:top}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:18px;font:14px/1.5 monospace}code{overflow-wrap:anywhere}.policy{background:white;padding:22px;font-size:21px}textarea{display:block;width:100%;min-height:85px;margin:8px 0 22px;padding:12px;font:inherit;border:1px solid #aab8bd;border-radius:4px}label{font-weight:600}a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid #0b51ae;outline-offset:3px}.source{margin-bottom:28px}@media(max-width:560px){main{padding:32px 20px}table{display:block;overflow-x:auto}}@media print{body{background:white;font-size:11pt}main{padding:0}.links,button{display:none}h1{font-size:30pt}h2{font-size:22pt}details{break-inside:avoid}img{max-height:300px;width:auto}}'''
    sections = []
    for name in ['first-run.md','core-rules.md','evidence-exercises.md','m365-workflow.md','demo-dry-run.md','link-verification.md']:
        lines=(PACK/name).read_text().splitlines()
        body=markdown.markdown('\n'.join(lines[1:]),extensions=['tables','fenced_code'])
        sections.append(f'<details><summary>{html.escape(lines[0].removeprefix("# "))}</summary><div class="detail-body">{body}</div></details>')
    directory=''.join(f'<article class="source"><h3><a href="{html.escape(r["URL"],quote=True)}">{html.escape(str(r["Row"]))}. {html.escape(r["Title"])}</a></h3><p>{html.escape(r["Alert me when prompt"])}</p><p class="small">{html.escape(r["Source role"])}. Cadence example: {html.escape(r["Cadence"])}. {html.escape(r["Maintenance"])}</p></article>'for r in rows)
    prompt=html.escape((PACK/'triage-prompt.txt').read_text())
    fda_path=events['fda']['comparison']
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pharma CI starter pack</title><style>{css}</style></head><body><main>
<h1>Make one source useful.</h1><p>Choose the change you need to see. Give it a reviewer. Keep the evidence with the decision.</p><p class="small">Pharma CI USA · September 17, 2026 · 11:15-11:45 EDT<br>Updated September 16. Public source examples selected independently of customer watchlists.</p>
<div class="links"><a href="pharma-ci-starter-guide.pdf">Short PDF</a><a href="source-directory.csv" download>Source directory</a><a href="import-tab.csv" download>Import CSV</a><a href="review-item-template.csv" download>Review template</a><a href="{DOWNLOAD}pharma-ci-starter-pack.zip">Full ZIP</a></div>
<h2>A saved change starts the review.</h2><p>This actual FDA comparison highlights an added Isembyld entry. Open the source detail before drawing an indication or label conclusion. The reviewer and next action are proposed.</p><figure><img src="{fda_path}" alt="Original Visualping highlighted comparison of the FDA approval listing"><figcaption>Saved source evidence. Detection time and classification are recorded separately from source dates in <a href="evidence/README.md">the evidence notes</a>.</figcaption></figure>
<p class="policy">Choose delivery: every captured edit, or IMPORTANT changes only.</p><p>Every change event includes IMPORTANT and an AI Summary. Test small wording and image edits when they matter. A relevance rule can assess only content included in the capture.</p>
{''.join(sections)}
<h2>{counts}.</h2><p>Replace every bracketed scope and example record. Check known records and discovery pages separately. Assign someone to maintain coverage.</p><details><summary>Open the source directory</summary>{directory}</details>
<h2>Draft the review item.</h2><p>Use an approved AI tool with the source evidence. Check its output before routing.</p><button type="button" id="copy">Copy prompt</button><p id="copy-status" class="small" aria-live="polite"></p><pre id="prompt">{prompt}</pre>
<h2>Your first workflow</h2>'''
    for key,label in [('source','Source and watch question'),('reviewer','Reviewer, backup and destination'),('policy','Every-edit or IMPORTANT-only delivery'),('maintenance','Maintenance owner and source-check schedule'),('measure','Success measure and review date')]:
        page+=f'<label for="{key}">{label}</label><textarea id="{key}"></textarea>'
    page+='''<p class="small">Answers stay in this page while it is open. Copy or print them before closing. Nothing is sent or stored online.</p><button type="button" onclick="window.print()">Print your worksheet</button><p class="small">The M365 route remains a configuration recipe. A successful run and recording are unverified. <a href="README.md">File index and limitations</a>.</p></main><script>document.getElementById('copy').addEventListener('click',async()=>{const text=document.getElementById('prompt').textContent;try{await navigator.clipboard.writeText(text);document.getElementById('copy-status').textContent='Prompt copied.'}catch(e){const r=document.createRange();r.selectNodeContents(document.getElementById('prompt'));const s=window.getSelection();s.removeAllRanges();s.addRange(r);document.getElementById('copy-status').textContent='Prompt selected. Use your browser Copy command.'}});</script></body></html>'''
    for name in ('index.html','handout.html'):
        (PACK/name).write_text(page)

    styles={
        'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=27,leading=30,textColor=colors.HexColor('#0c2235'),spaceAfter=15),
        'heading':ParagraphStyle('heading',fontName='Helvetica-Bold',fontSize=15,leading=18,textColor=colors.HexColor('#0b51ae'),spaceBefore=9,spaceAfter=7),
        'body':ParagraphStyle('body',fontName='Helvetica',fontSize=11,leading=15,spaceAfter=9),
        'small':ParagraphStyle('small',fontName='Helvetica',fontSize=9,leading=12,textColor=colors.HexColor('#526066'),spaceAfter=8),
    }
    story=[]
    def p(text,style='body'):story.append(Paragraph(text,styles[style]))
    def title(text):p(text,'title')
    def heading(text):p(text,'heading')
    def picture(path,height=125):
        w,h=ImageReader(str(path)).getSize(); scale=min(308/w,height/h)
        story.append(Image(str(path),width=w*scale,height=h*scale,hAlign='LEFT'));story.append(Spacer(1,8))
    def new():story.append(PageBreak())
    title('Make one source useful.')
    p('Pharma CI starter guide<br/>September 17, 2026 · 11:15-11:45 EDT','small')
    for n,text in enumerate([
        'Choose the source and decision. Known records reveal amendments; listings discover new records. Check pagination and linked documents.',
        'Save the evidence and dates. Keep publication, detection and actual capture times separate. Leave unknown dates unknown.',
        'Write the rule. Include small edits, sites, eligibility or results when the reviewer needs them.',
        'Choose delivery. Review every captured edit, or only IMPORTANT changes. Test the capture before relying on filtering.',
        'Name the reviewer, backup and maintenance owner. Record the action and inspect source failures before expanding.',
    ],1):p(f'{n}. {text}')
    p('Every Visualping change event has a binary IMPORTANT flag and an AI Summary. The saved comparison remains the evidence.','small')
    p(f'<a href="{DOWNLOAD}pharma-ci-starter-pack.zip" color="#0b51ae">Download the full pack</a>: {counts}, prompts, templates and actual saved examples. Unzip and open index.html.','small')
    p(f'<a href="https://github.com/edoc33/pharma-ci-skills" color="#0b51ae">Optional skills for your AI assistant</a>. The manual first run needs no API key or M365 connection.','small')

    new();title('Check the source before routing.')
    p('The FDA example contains a saved comparison and an earlier capture. The added Isembyld entry is the observation.','body')
    picture(crop('fda','before'),95)
    p('Earlier saved view','small')
    picture(crop('fda'),110)
    p('Original highlighted comparison. Observed 11 September 2026. Exact provenance is in the evidence folder.','small')
    heading('Proposed review')
    p('A regulatory-intelligence reviewer opens the approval detail, checks asset and indication scope, and decides whether the briefing needs an update. The owner and action are proposed.')
    p(f'<a href="{ONLINE}evidence/README.md" color="#0b51ae">Read the evidence notes</a>. Saved source evidence does not establish a completed M365 run.','small')

    new();title('Choose the rule for the question.')
    for label,text in [
        ('Trial','Status, dates, enrollment, arms, eligibility, outcomes and results. Add country/site changes explicitly when needed.'),
        ('Pipeline','Programs, indications, phases and published status. Preserve what the source says about the change.'),
        ('Brand or provider','Wording, images, claims, prominence, price or stated availability. Small edits may matter.'),
        ('Congress','New or changed sessions, abstracts and presentations. Open the linked material for its contents.'),
        ('Guideline or access','Version, population, coverage terms and recommendation. Keep draft and final status distinct.'),
        ('Regulatory approval','New approval-list entries. Watch labels and detailed documents as separate sources when needed.'),
    ]:heading(label);p(text)
    p('The trial exercise reports 171 to 169 sites in its saved AI Summary and IMPORTANT=false under a narrower rule. Test whether your project needs a different rule.','small')
    p(f'<a href="{ONLINE}core-rules.md" color="#0b51ae">Full copyable rules</a> and <a href="{ONLINE}evidence-exercises.md" color="#0b51ae">source-check exercises</a>.','small')

    new();title('Watch the commercial message.')
    picture(crop('pfizer'),180)
    p('Actual Pfizer homepage comparison, detected 9 September 2026. Original highlighting shows campaign headline and vaccination wording.','small')
    heading('Give the edit a reviewer')
    p('Proposed owner: brand or commercial CI reviewer. Next action: check the message and decide whether the competitor brief needs updating.')
    p('The pack also includes a CVS availability-announcement example. A services-page announcement prompts a source check; it does not establish current local stock.')
    p('Separate before captures for these two examples were unavailable. Describe the highlighted content and keep prior copy unknown.','small')
    p(f'<a href="{ONLINE}evidence-exercises.md" color="#0b51ae">Open the commercial examples</a>. Choose every-edit delivery when the brief requires small wording or image changes.','small')

    new();title('Give the alert an owner.')
    p('Shared mailbox → Power Automate → SharePoint review queue. Add a Teams notification after the queue item exists.')
    p('Keep the source, saved classification, reviewer, backup and action together. A platform event ID and an email message ID identify different things.')
    p('Before enabling the route, verify tenant permissions, connections, duplicates, missing evidence and failure handling. The included recipe has no verified tenant execution.','small')
    heading('Your first workflow')
    for text in ['Source and watch question','Reviewer, backup and destination','Delivery policy','Maintenance owner and check schedule','Success measure and review date']:
        p(text);story.append(Spacer(1,17))
    p('The maintenance owner checks new/moved pages, pagination, annual URLs and failed monitors. Recheck selected sources before the session.','small')

    def footer(canvas,doc):
        canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#526066'))
        canvas.drawString(26,18,'Pharma CI · Updated 16 September 2026');canvas.drawRightString(334,18,str(doc.page))
    SimpleDocTemplate(str(PACK/'pharma-ci-starter-guide.pdf'),pagesize=(360,600),leftMargin=26,rightMargin=26,topMargin=28,bottomMargin=34,title='Pharma CI starter guide',author='Workshop materials').build(story,onFirstPage=footer,onLaterPages=footer)
    OUT.mkdir(exist_ok=True)
    shutil.copy2(ROOT/'THIRD_PARTY_NOTICES.md',PACK/'THIRD_PARTY_NOTICES.md')
    with zipfile.ZipFile(OUT/'pharma-ci-starter-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in sorted(PACK.rglob('*')):
            if path.is_file() and not path.name.startswith('.'):
                z.write(path,'pharma-ci-starter-pack/'+str(path.relative_to(PACK)))
    print(json.dumps({'source_entries':len({r['Source ID']for r in rows}),'urls':len(rows),'zip':str(OUT/'pharma-ci-starter-pack.zip')}))


if __name__=='__main__':
    main()
