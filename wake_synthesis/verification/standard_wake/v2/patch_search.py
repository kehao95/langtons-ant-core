"""Hash-pinned chain-separation overlay; prerequisite rank overlay is unchanged."""
from pathlib import Path
import hashlib
import importlib.util


def generate(source: Path, destination: Path, rank_overlay: Path) -> str:
    spec = importlib.util.spec_from_file_location('rank_overlay', rank_overlay)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.generate(source, destination)
    text = destination.read_text()
    replacements = {
        'vector<int> chain(n,-1);vector<int64_t> off(n),dist;':
        'vector<int> chain(n,-1),level_at(n),chain_length;vector<int64_t> off(n),dist;',
        'chain[i]=nc;off[i]=pos-level*P;++pos;++seen;':
        'chain[i]=nc;level_at[i]=level;off[i]=pos-level*P;++pos;++seen;',
        '  }++nc;': '  }chain_length.push_back(pos);++nc;',
        '  else edges.push_back({a,b,w});': (
        '  else { int64_t separated=int64_t(chain_length[a])+int64_t(level_at[i]-level_at[i-1])*P; '
        + 'w=max(w,separated); edges.push_back({a,b,w}); }'),
    }
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise ValueError('Ambiguous chain-separation anchor: ' + old)
        text = text.replace(old, new)
    destination.write_text(text)
    return hashlib.sha256(text.encode()).hexdigest()
