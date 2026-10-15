"""Reject deliberately damaged immutable certificates without repairing them."""
from __future__ import annotations
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def hashes(folder):return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.iterdir() if p.is_file()}
def main(exe):
    results=[]
    for case in ('deleted_edge','spurious_edge','bad_quotient'):
        with tempfile.TemporaryDirectory(prefix='ant-negative-') as td:
            cert=Path(td)/'certificates';shutil.copytree(ROOT/'certificates',cert)
            if case in ('deleted_edge','spurious_edge'):
                path=cert/'windows10.txt';words=path.read_text().splitlines()
                if case=='deleted_edge':words.pop(len(words)//2)
                else:words=sorted(words+['R'*150])
                path.write_text('\n'.join(words)+'\n')
            else:
                path=cert/'quotient.tsv';rows=path.read_text().splitlines()
                rows[0]=rows[0].split('\t')[0]+'\t102';path.write_text('\n'.join(rows)+'\n')
            before=hashes(cert)
            for name,cmd in [('python',[sys.executable,str(ROOT/'check.py'),'--cert-dir',str(cert)]),('cpp',[str(exe),str(cert)])]:
                proc=subprocess.run(cmd,capture_output=True,text=True)
                if proc.returncode==0:raise AssertionError(f'{name} accepted {case}')
                assert hashes(cert)==before,'damaged witness was changed'
                results.append({'case':case,'implementation':name,'rejected':True,'certificate_unchanged':True})
    return {'status':'passed','controls':results}
if __name__=='__main__':print(json.dumps(main(Path(sys.argv[1]).resolve()),indent=2))
