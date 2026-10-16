#!/usr/bin/env python3
"""Run only this theorem's complete checker in a fresh disposable directory."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
HERE=Path(__file__).resolve().parent
FILES=('engine.py','check.py','independent.cpp','grammar.json.zlib',
       'grammar-manifest.json','checked_report.json')
if __name__=='__main__':
    with tempfile.TemporaryDirectory(prefix='ant-silent-recovery-') as td:
        dest=Path(td)
        for name in FILES:
            shutil.copy2(HERE/name,dest/name)
        subprocess.run([sys.executable,str(dest/'check.py'),'--compare',str(dest/'checked_report.json')],check=True)
    print('PASS: complete theorem-local replay matches the frozen report.')
