"""Disposable theorem-local replay; old broad suites and large searches are not run."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

here = Path(__file__).resolve().parent
root = here.parents[2]
with tempfile.TemporaryDirectory(prefix='hc-defect-opt-') as tmp:
    isolated = Path(tmp)
    source = root/'experiments/hc_global/defect_resource_spectrum/code'
    target = isolated/'experiments/hc_global/defect_resource_spectrum/code'
    target.mkdir(parents=True)
    for name in ('isl_bridge.py', 'trace_arithmetic.py'):
        shutil.copy2(source/name, target/name)
    module = isolated/'experiments/hc_global/defect_compiler_optimization'
    module.mkdir(parents=True)
    for name in ('fast.py', 'fixtures.py', 'check.py', 'check_results.json'):
        shutil.copy2(here/name, module/name)
    subprocess.run([sys.executable, str(module/'check.py'), '--compare',
                    str(module/'check_results.json')], check=True, cwd=isolated)
print('Disposable scoped replay passed; historical baseline files unchanged.')
