"""A small, hash-pinned overlay on the retained exact enumeration.

The baseline remains an independent fallback. The generated source only adds
a necessary rank-contiguity check after premature cycles have been excluded.
"""
from pathlib import Path
import hashlib
PIN='567e5464e0be3fe7a748b50661113d5c0ca4466ae3a73488cd0f643830aba39c'
def generate(source: Path, destination: Path) -> str:
    raw=source.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PIN:
        raise ValueError('The prerequisite enumerator changed; review before patching.')
    text=raw.decode()
    anchor=' if(seen<n){++bad_cycle;return false;}'
    if text.count(anchor)!=1: raise ValueError('Ambiguous insertion point')
    text=text.replace('#include <vector>', '#include <vector>\n#include "chain_rank.hpp"')
    text=text.replace(anchor, anchor+'\n if(!consecutive_chain_ranks(ns,cap))return false;')
    anchor='<<",\\"solutions\\":"<<solutions.size()'
    if text.count(anchor)!=1: raise ValueError('Ambiguous counter insertion')
    text=text.replace(anchor,
        '<<",\\"rank_checks\\":"<<rank_checks<<",\\"rank_rejections\\":"<<rank_rejections'+anchor)
    destination.write_text(text)
    return hashlib.sha256(text.encode()).hexdigest()
