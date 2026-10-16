#!/usr/bin/env python3
"""Repeat only this module's full exact checks in a disposable directory."""
from pathlib import Path
import shutil,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
FILES=('check.py','supply.py','isl_core.py','dichotomy.py','independent.cpp','witness.json','report.json')
if __name__=='__main__':
    with tempfile.TemporaryDirectory(prefix='ant-schema-supply-') as td:
        root=Path(td)
        for name in FILES:shutil.copy2(HERE/name,root/name)
        subprocess.run([sys.executable,str(root/'check.py'),'--compare',str(root/'report.json')],check=True)
    print('PASS: disposable schema-supply replay.')
