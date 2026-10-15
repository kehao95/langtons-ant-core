#!/usr/bin/env python3
"""Verify an exact candidate ZIP in isolation, replay its checks, and rebuild its PDF."""
import argparse, hashlib, json, os, subprocess, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(data): return hashlib.sha256(data).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project',required=True,choices=('wake_synthesis','factor_language','memory_feedback','four_cell_port'))
    parser.add_argument('--quick',action='store_true',help='wake only: omit the large thin-wake exclusion replay')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if not __debug__: parser.error('Run without -O')
    if args.quick and args.project!='wake_synthesis': parser.error('--quick applies only to wake')
    home=ROOT/args.project;manifest=json.loads((home/'release/candidate-manifest.json').read_text())
    archive=home/'release/candidate'/f"{args.project}-{manifest['version']}-source.zip"
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
        print('Isolated replay:',args.project,flush=True)
        subprocess.run(command,cwd=work,env=env,check=True)
        subprocess.run(['make','-C',f'{args.project}/paper'],cwd=work,env=env,check=True,
                       stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        pdf=work/args.project/'paper/build/paper.pdf'
        current=home/'paper/build/paper.pdf'
        a=subprocess.check_output(['pdftotext',str(pdf),'-'])
        b=subprocess.check_output(['pdftotext',str(current),'-'])
        assert a==b,'Rebuilt PDF text differs'
        report={'status':'passed','project':args.project,'version':manifest['version'],
                'mode':'quick' if args.quick else 'full','archive_sha256':sha(archive.read_bytes()),
                'source_snapshot_sha256':manifest['snapshot_sha256'],
                'source_files_verified':len(manifest['source_sha256']),
                'no_research_checkout_dependency':True,'pdf_text_matches':True,
                'pdf_text_sha256':sha(a),'replay':json.loads((work/'fresh-report.json').read_text()),
                'completed_utc':datetime.now(timezone.utc).isoformat()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(args.project+': isolated archive replay and PDF rebuild PASS',flush=True)
if __name__=='__main__':main()
