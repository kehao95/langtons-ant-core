#!/usr/bin/env python3
"""Validate exact sources and replay the article's certificates in isolation."""
from pathlib import Path
import argparse,gzip,hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
MODULES={'four': 'four_row_boundary', 'five': 'persistent_boundary_memory', 'basin': 'counter_highway_basin', 'access': 'counter_basin_random_access'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--component',choices=list(MODULES),help='check only this theorem component')
    parser.add_argument('--output-report',type=Path)
    args=parser.parse_args()
    if not __debug__:parser.error('Run without Python -O')
    sources=json.loads((ROOT/'sources.json').read_text())['sha256']
    for name,digest in sources.items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Source mismatch: '+name)
    chosen=[args.component] if args.component else list(MODULES)
    with tempfile.TemporaryDirectory(prefix=ROOT.name+'-') as td:
        work=Path(td)/'verification'
        shutil.copytree(ROOT/'verification',work,ignore=shutil.ignore_patterns('__pycache__'))
        for compressed in work.rglob('*.json.gz'):
            compressed.with_suffix('').write_bytes(gzip.decompress(compressed.read_bytes()))
        for key in chosen:
            module=work/MODULES[key]
            subprocess.run([sys.executable,str(module/'check.py')],cwd=module,check=True)
    if args.output_report:
        args.output_report.parent.mkdir(parents=True,exist_ok=True)
        args.output_report.write_text(json.dumps({'status':'passed','components':chosen,'source_sha256':sources},indent=2)+'\n')
if __name__=='__main__':main()
