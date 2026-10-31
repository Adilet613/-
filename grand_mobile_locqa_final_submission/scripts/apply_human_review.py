#!/usr/bin/env python3
"""Finalize only after actual human review; does not manufacture attestations.

python scripts/apply_human_review.py --manifest human_reviews.json --out-dir reviewed
Use a manifest exported from the included report.html after personal inspection.
"""
import argparse
import json
from pathlib import Path
from datetime import datetime

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--manifest',required=True);p.add_argument('--out-dir',required=True);a=p.parse_args()
    report=json.loads((ROOT/'report.json').read_text())
    fixed=json.loads((ROOT/'intl_kk_fixed.arb').read_text())
    original_manifest=json.loads((ROOT/'audit/human_review_pending.json').read_text())
    m=json.loads(Path(a.manifest).read_text())
    for k in ['version','source_sha256','target_sha256']:
        if m.get(k)!=original_manifest.get(k):raise ValueError('Stale or unrelated manifest: '+k)
    expected={i['key'] for i in report};entries={}
    for e in m.get('entries',[]):
        k=e['key']
        if k in entries:raise ValueError('Duplicate review: '+k)
        if e.get('reviewed_by_human') is not True or (not isinstance(e.get('reviewer'),str) or not e['reviewer'].strip()):raise ValueError('Actual human attestation required: '+k)
        datetime.fromisoformat(e['reviewed_at'].replace('Z','+00:00'))
        entries[k]=e
    if set(entries)!=expected:raise ValueError('Review all 144 changed rows; missing or unrelated rows present')
    for i in report:
        e=entries[i['key']]
        if e.get('source')!=i['source'] or e.get('original')!=i['target']:raise ValueError('Text mismatch '+i['key'])
        if e.get('translation')!=fixed[i['key']]:raise ValueError('Edited translation needs fresh structural/context validation: '+i['key'])
        if i['issue_type'] not in e.get('issue_types',[]):raise ValueError('Issue not reviewed '+i['key'])
        i['reviewed_by_human']=True
    for k,e in entries.items():
        attrs=dict(fixed.get('@'+k,{}));attrs.update(reviewed_by_human=True,reviewer=e['reviewer'],reviewed_at=e['reviewed_at'],review_status='human_confirmed');fixed['@'+k]=attrs
    out=Path(a.out_dir).resolve()
    if out==ROOT:raise ValueError('Use a separate output directory to retain the review-pending original')
    out.mkdir(parents=True,exist_ok=True)
    for name,obj in [('intl_kk_fixed.arb',fixed),('report.json',report)]:
        (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print('Wrote human-attested files to',out)
    print('Attestations are user-provided; native-speaker status is not independently authenticated.')

if __name__=='__main__':main()
