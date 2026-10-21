#!/usr/bin/env python3
"""Verify an exact candidate ZIP in isolation, replay its checks, and rebuild its PDF."""
import argparse, hashlib, json, os, subprocess, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True,choices=('wake_synthesis','factor_language','memory_feedback','four_cell_port','defect_synthesis','four_row_escape'))
    parser.add_argument('--quick',action='store_true',help='wake only: omit the large thin-wake exclusion replay')
    parser.add_argument('--extensions-only',action='store_true',help='wake/factor: replay new modules and hash-match inherited fully replayed mathematical sources')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not __debug__: parser.error('Run without -O')
    if args.extensions_only and (args.project not in {'wake_synthesis','factor_language'} or args.quick): parser.error('--extensions-only is a separate wake/factor mode')
    if args.quick and args.project!='wake_synthesis': parser.error('--quick applies only to wake')
    home=ROOT/args.project;manifest=json.loads((home/'release/candidate-manifest.json').read_text())
    archive=home/'release/candidate'/f"{args.project}-{manifest['version']}-source.zip"
    inherited=None
    if args.extensions_only:
        previous=home/'release'/('v'+manifest['version'])/'revisions/2026-10-15'
        old=json.loads((previous/'prepared-source-manifest.json').read_text())
        replay=json.loads((previous/'standalone-check.json').read_text())
        assert replay['status']=='passed' and replay['mode']=='full'
        assert replay['source_snapshot_sha256']==old['snapshot_sha256']
        inherited_sources={name:digest for name,digest in old['source_sha256'].items()
                           if '/verification/' in name or '/proof/' in name
                           or ('/evidence/' in name and not name.endswith('/README.md'))}
        assert inherited_sources
        for name,digest in inherited_sources.items():
            assert manifest['source_sha256'].get(name)==digest,('inherited mathematical source changed',name)
        inherited={'source_snapshot_sha256':old['snapshot_sha256'],
                   'prior_full_archive_sha256':replay['archive_sha256'],
                   'prior_completed_utc':replay['completed_utc'],
                   'unchanged_mathematical_files':len(inherited_sources),
                   'source_sha256':inherited_sources,
                   'scope':'Prior full base replay retained; these unchanged sources are hash-matched, not re-executed.'}
    env=dict(os.environ);env.pop('PYTHONPATH',None);env['PYTHONNOUSERSITE']='1'
    with tempfile.TemporaryDirectory(prefix='preprint-standalone-') as directory:
        work=Path(directory)
        with zipfile.ZipFile(archive) as z:
            for name in z.namelist():
                path=Path(name)
                if path.is_absolute() or '..' in path.parts: raise ValueError('Unsafe ZIP member')
            z.extractall(work)
        bundled=json.loads((work/'artifact-manifest.json').read_text())
        assert bundled==manifest
        for name,digest in manifest['source_sha256'].items():
            assert sha((work/name).read_bytes())==digest,name
        command=['python3',f'{args.project}/reproduce.py','--output-report',str(work/'fresh-report.json')]
        if args.quick: command.append('--quick')
        if args.extensions_only: command.append('--extensions-only')
        print('Isolated replay:',args.project,flush=True)
        subprocess.run(command,cwd=work,env=env,check=True)
        subprocess.run(['make','-C',f'{args.project}/paper'],cwd=work,env=env,check=True,
                       stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        pdf=work/args.project/'paper/build/paper.pdf'
        current=home/'paper/build/paper.pdf'
        assert sha(current.read_bytes())==manifest['pdf']['sha256'],'Delivered PDF changed since packaging'
        assert sha((work/'metadata.json').read_bytes())==manifest['metadata_sha256']
        a=subprocess.check_output(['pdftotext',str(pdf),'-'])
        b=subprocess.check_output(['pdftotext',str(current),'-'])
        assert a==b,'Rebuilt PDF text differs'
        report={'status':'passed','project':args.project,'version':manifest['version'],
                'mode':'extensions-only' if args.extensions_only else ('quick' if args.quick else 'full'),
                'inherited_full_replay':inherited,'archive_sha256':sha(archive.read_bytes()),
                'source_snapshot_sha256':manifest['snapshot_sha256'],
                'source_files_verified':len(manifest['source_sha256']),
                'no_research_checkout_dependency':True,'pdf_text_matches':True,
                'pdf_text_sha256':sha(a),'replay':json.loads((work/'fresh-report.json').read_text()),
                'completed_utc':datetime.now(timezone.utc).isoformat()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(args.project+': isolated archive replay and PDF rebuild PASS',flush=True)
if __name__=='__main__':main()
