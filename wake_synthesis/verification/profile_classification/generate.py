"""Hash-pinned parameterization of the retained ordered-event enumerator.
Only wake bits and diagnostic arguments change the search domain. Geometric
pruning is inherited from the rank and chain-separation overlays.
"""
from pathlib import Path
import hashlib
PIN='567e5464e0be3fe7a748b50661113d5c0ca4466ae3a73488cd0f643830aba39c'

def generate(source: Path, destination: Path, optimized: bool=True) -> str:
    text=source.read_text()
    if hashlib.sha256(text.encode()).hexdigest()!=PIN:
        raise ValueError('Inherited enumerator changed; review the coverage before updating the pin.')
    replacements={
     'using namespace std;':'using namespace std;\n#include "chain_rank.hpp"',
     'vector<int> chain(n,-1);vector<int64_t> off(n),dist;':'vector<int> chain(n,-1),level_at(n),chain_length;vector<int64_t> off(n),dist;',
     'chain[i]=nc;off[i]=pos-level*P;++pos;++seen;':'chain[i]=nc;level_at[i]=level;off[i]=pos-level*P;++pos;++seen;',
     '  }++nc;':'  }chain_length.push_back(pos);++nc;',
     ' if(seen<n){++bad_cycle;return false;}':' if(seen<n){++bad_cycle;return false;}\n if(!consecutive_chain_ranks(ns,cap))return false;',
     '  else edges.push_back({a,b,w});':'  else { int64_t separated=int64_t(chain_length[a])+int64_t(level_at[i]-level_at[i-1])*P; w=max(w,separated); edges.push_back({a,b,w}); }',
     'const bool odd[11][2]={{1,1},{0,1},{0,1},{1,0},{1,0},{1,0},{0,1},{0,0},{1,0},{0,1},{1,1}};':'bool odd[11][2]{}; int mask=-1;',
     ' if(argc<3){':' if(argc<6){',
     ' cap=stoi(argv[1]);if(argc>3)seconds_limit=stod(argv[3]);if(argc>4)work_limit=stoull(argv[4]);':''' cap=stoi(argv[1]);seconds_limit=stod(argv[3]);work_limit=stoull(argv[4]);
 mask=stoi(argv[5]);if(mask<0||mask>255)throw runtime_error("mask outside 0..255");
 odd[0][0]=odd[0][1]=odd[10][0]=odd[10][1]=true;
 const int rows[8]={-9,-8,-7,-6,-5,-4,-2,-1};
 for(int k=0;k<8;k++)odd[rows[k]+10][(mask>>k)&1]=true;''',
     '     <<",\\\"solutions\\\":"<<solutions.size()':'     <<",\\\"mask\\\":"<<mask<<",\\\"rank_checks\\\":"<<rank_checks<<",\\\"rank_rejections\\\":"<<rank_rejections<<",\\\"solutions\\\":"<<solutions.size()'
    }
    if not optimized:
        keep=('const bool odd[11][2]', ' if(argc<3){', ' cap=stoi(argv[1]);',
              '     <<",\\\"solutions\\\":')
        replacements={a:b for a,b in replacements.items() if a.startswith(keep)}
        for a in list(replacements):
            if 'solutions.size()' in a:
                replacements[a]='     <<",\\\"mask\\\":"<<mask<<",\\\"solutions\\\":"<<solutions.size()'
    for old,new in replacements.items():
        if text.count(old)!=1:raise ValueError('Ambiguous source anchor: '+old)
        text=text.replace(old,new)
    destination.write_text(text)
    return hashlib.sha256(text.encode()).hexdigest()
