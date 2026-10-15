"""Hash-pinned mechanical parameterization of the inherited exact searches.

Only the wake bits become input data. The proved search and rank pruning are
unchanged. The optional top-down shard partitions a complete-layer frontier
into disjoint ordinal classes. It does not remove any candidate from the union.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
ODD='const bool odd[11][2]={{1,1},{0,1},{0,1},{1,0},{1,0},{1,0},{0,1},{0,0},{1,0},{0,1},{1,1}};'


def replace_once(text,old,new):
    if text.count(old)!=1:raise ValueError('An inherited source anchor changed')
    return text.replace(old,new)


def generate(side: str, sharded=False) -> str:
    if side not in('top','bottom') or (sharded and side!='top'):
        raise ValueError('Invalid engine')
    inputs=ROOT/'inputs';manifest=json.loads((inputs/'MANIFEST.json').read_text())
    name=f'glue_{side}.cpp';raw=(inputs/name).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=manifest[name]:raise ValueError('Inherited search hash mismatch')
    s=raw.decode()
    s=replace_once(s,'#include <vector>','#include <vector>\n#include "chain_rank.hpp"')
    anchor=' if(seen<n){++bad_cycle;return false;}'
    s=replace_once(s,anchor,anchor+'\n if(!consecutive_chain_ranks(ns,cap))return false;')
    anchor='<<",\\"solutions\\":"<<solutions.size()'
    s=replace_once(s,anchor,'<<",\\"rank_checks\\":"<<rank_checks<<",\\"rank_rejections\\":"<<rank_rejections'+anchor)
    s=replace_once(s,ODD,'bool odd[11][2]{};')
    s=replace_once(s,' cap=stoi(argv[1]);',''' if(argc<7)throw runtime_error("expected mask and hole arguments");
 int mask=stoi(argv[5]),hole=stoi(argv[6]);
 if(mask<0||mask>=256||hole < -9||hole > -1)throw runtime_error("wake parameter range");
 odd[0][0]=odd[0][1]=odd[10][0]=odd[10][1]=true;
 int j=0;
 for(int t=-9;t<0;++t)if(t!=hole){odd[t+10][(mask>>j)&1]=true;++j;}
 if(j!=8)throw runtime_error("thin profile size");
 cap=stoi(argv[1]);''')
    if sharded:
        s=replace_once(s,'int cap=104;','int shard_id=0,shard_count=1;\nuint64_t cuts=0,selected_cuts=0,cut_hash=1469598103934665603ULL;\nint cap=104;')
        s=replace_once(s,' cap=stoi(argv[1]);',''' if(argc>7){shard_id=stoi(argv[7]);}
 if(argc>8){shard_count=stoi(argv[8]);}
 if(shard_count<1||shard_id<0||shard_id>=shard_count)throw runtime_error("shard parameters");
 cap=stoi(argv[1]);''')
        s=replace_once(s,'void rec(int t,const Row &old){','''void rec(int t,const Row &old){
 if(t==-5){
  uint64_t ordinal=cuts++;
  for(const auto& nd:ns){
   for(int x:{nd.t,nd.r,nd.k,nd.a,nd.down,nd.h,nd.next,nd.prev,nd.v}){
    cut_hash^=uint64_t(int64_t(x));cut_hash*=1099511628211ULL;
   }
  }
  if(ordinal%shard_count!=uint64_t(shard_id))return;
  ++selected_cuts;
 }''')
        anchor='<<",\\"solutions\\":"<<solutions.size()'
        s=replace_once(s,anchor,'<<",\\"shard\\":"<<shard_id<<",\\"shards\\":"<<shard_count<<",\\"cuts\\":"<<cuts<<",\\"selected_cuts\\":"<<selected_cuts<<",\\"cut_hash\\":"<<cut_hash'+anchor)
    return s


def compile_all(directory: Path):
    if shutil.which('g++') is None:raise RuntimeError('g++ is required')
    directory.mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'inputs/chain_rank.hpp',directory/'chain_rank.hpp')
    result={}
    for name,side,shard in [('top','top',False),('bottom','bottom',False),('sharded','top',True)]:
        source=directory/f'{name}.cpp';source.write_text(generate(side,shard))
        binary=directory/name
        subprocess.run(['g++','-std=c++17','-O3','-Wall','-Wextra','-pedantic',str(source),'-o',str(binary)],check=True)
        result[name]=binary
    return result
