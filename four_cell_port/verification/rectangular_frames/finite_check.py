"""Rebuild all finite cover cases, cross-check full traces and endpoint fields.

Native output contains every endpoint coordinate. Python compares the complete
sets before reducing the persistent report to a hash. Default never rewrites
frozen evidence; --write explicitly creates a report.
"""
import argparse,hashlib,json,subprocess,tempfile,threading
from pathlib import Path
from literal import rectangle,vector_replay,chronological_permanent,STANDARD
HERE=Path(__file__).resolve().parent

def inputs():
    for n in range(1,200):
        for m in range(1,200):
            if min(n,m)<=9:yield n,m,0,0,0,'corner'
    for r in range(43):
        if (r%2==0 and r>=32) or (r%2==1 and r>=43):continue
        yield 2*r+1,2*r+1,r,r,0,'center'

def replay():
    cases=list(inputs());rows=[];steps=0
    with tempfile.TemporaryDirectory() as temp:
        exe=Path(temp)/'verify'
        subprocess.run(['g++','-O2','-std=c++17',str(HERE/'independent.cpp'),'-o',str(exe)],check=True)
        proc=subprocess.Popen([str(exe)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
        def feed():
            try:
                for n,m,x,y,h,kind in cases:proc.stdin.write(f'{n} {m} {x} {y} {h} 2000000\n')
                proc.stdin.close()
            except BrokenPipeError:pass
        feeder=threading.Thread(target=feed);feeder.start()
        for index,case in enumerate(cases):
            line=proc.stdout.readline()
            if not line:raise AssertionError('Native output incomplete')
            z=json.loads(line);n,m,x,y,h,kind=case
            if (z['n'],z['m'],*z['head'])!=(n,m,x,y,h):raise AssertionError('Native input mismatch')
            word,B,pose,foot=vector_replay(rectangle(n,m),(x,y,h),z['boundary'])
            if word!=z['word'] or B!={tuple(p) for p in z['field']} or pose!=tuple(z['pose']):raise AssertionError('Full literal mismatch')
            if not chronological_permanent(B,pose,z['tail']):raise AssertionError('Independent infinite checker rejected')
            tau=len(word)
            while tau>0 and word[tau-1]==z['tail'][(tau-1-len(word))%104]:tau-=1
            if tau!=z['first']:raise AssertionError('Wrong first entrance')
            if z['tail'] not in STANDARD*2:raise AssertionError('Nonstandard reference')
            steps+=len(word)
            rows.append({'kind':kind,'n':n,'m':m,'head':[x,y,h],'first':tau,'boundary':len(word),'pose':list(pose),'tail':z['tail'],
                         'endpoint_count':len(B),'endpoint_sha256':hashlib.sha256(json.dumps(sorted(B),separators=(',',':')).encode()).hexdigest(),
                         'word_sha256':hashlib.sha256(word.encode()).hexdigest()})
            if (index+1)%100==0:print(json.dumps({'completed':index+1,'total':len(cases)}),flush=True)
        feeder.join();extra=proc.stdout.read();code=proc.wait()
        if code!=0 or extra.strip():raise AssertionError('Native failure/extra output')
    return {'schema':'recovered-finite-cover-v1','cases':len(rows),'complete_field_comparisons':len(rows),'literal_updates_per_implementation':steps,'rows':rows}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',type=Path);a=p.parse_args();r=replay()
    if a.write:a.write.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    else:
        expected=json.loads((HERE/'finite_report.json').read_text())
        if r!=expected:raise AssertionError('Frozen finite report mismatch')
    print(json.dumps({k:v for k,v in r.items() if k!='rows'}),flush=True)
