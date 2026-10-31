#!/usr/bin/env python3
"""Prepare standard Flutter ARBs without silently losing legacy metadata.

Moves legacy `message@description` properties to @message.description and
normalizes uppercase-initial message IDs. The resulting alias map is an
integration contract: game callers must migrate if they reference those IDs.
"""
import argparse
import json
import re
from pathlib import Path


import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'cli'))
from locqa.flutter_arb import canonicalize


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True);p.add_argument('--target',required=True)
    p.add_argument('--out-dir',required=True);p.add_argument('--manifest',required=True)
    a=p.parse_args();out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    log={}
    for locale,path in [('ru',a.source),('kk',a.target)]:
        original=json.loads(Path(path).read_text(encoding='utf-8-sig'))
        result,migrations=canonicalize(original)
        result['@@locale']=locale
        (out/f'intl_{locale}.arb').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        log[locale]=migrations
    Path(a.manifest).write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
