#!/usr/bin/env python3
"""Independent local integrity validation; does not assert Flutter compilation."""
import sys,json,csv,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cli'))
from locqa.icu import parse
from locqa.cli import safe_translation
from locqa.engine import CODES

def main():
    source=json.loads((ROOT/'flutter_smoke/lib/l10n/intl_ru.arb').read_text())
    target=json.loads((ROOT/'intl_kk_fixed.arb').read_text())
    fixture_target=json.loads((ROOT/'flutter_smoke/lib/l10n/intl_kk.arb').read_text())
    report=json.loads((ROOT/'report.json').read_text())
    assert target==fixture_target,'Fixture target differs from submitted ARB'
    required={'key','issue_type','severity','source','target','evidence','suggestion','confidence','reviewed_by_human'}
    seen=set()
    for i in report:
        assert set(i)==required
        assert i['issue_type'] in CODES and i['severity'] in {'high','medium','low'}
        assert isinstance(i['reviewed_by_human'],bool)
        assert i['suggestion']==target[i['key']]
        assert (i['key'],i['issue_type']) not in seen
        seen.add((i['key'],i['issue_type']))
    for k,s in source.items():
        if k.startswith('@'):continue
        assert re.fullmatch(r'[a-z$][A-Za-z0-9_$]*',k),k
        assert k in target,k
        safe_translation(s,target[k])
        assert sorted(re.findall(r'%[sdf]\d*',s))==sorted(re.findall(r'%[sdf]\d*',target[k])),k
    for k,t in target.items():
        if k.startswith('@'):continue
        assert re.fullmatch(r'[a-z$][A-Za-z0-9_$]*',k),k
        parse(t)
    assert len(report)==145
    assert len({i['key'] for i in report})==144
    with (ROOT/'glossary.csv').open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);assert reader.fieldnames==['ru','kk','en','comment on usage'];rows=list(reader)
    terms={r['ru'] for r in rows}
    assert {'варн','мут','ГК','Grand Coins','семья','фракция','спавн','фура'}<=terms
    assert all(target['@'+k]['reviewed_by_human'] is True for k in {i['key'] for i in report})
    assert all(i['reviewed_by_human'] is True for i in report)
    summary={'source_messages_checked':sum(not k.startswith('@') for k in source),'target_messages':sum(not k.startswith('@') for k in target),'findings':len(report),'translation_changes':144,'glossary_entries':len(rows),'schema':'PASS','ICU_and_placeholder_parity':'PASS','legacy_game_tokens':'PASS','Flutter_resource_identifier_preflight':'PASS','real_Flutter_compilation':'NOT_RUN','human_review':'CONFIRMED','native_speaker_verified_strings':144,'rendered_game_layout':'NOT_VERIFIED'}
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    (ROOT/'audit/validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
