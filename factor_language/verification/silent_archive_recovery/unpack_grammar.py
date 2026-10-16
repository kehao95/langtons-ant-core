#!/usr/bin/env python3
"""Print the hash-checked, data-only grammar as readable JSON; never overwrite it."""
import json
from check import load
if __name__=='__main__':
    print(json.dumps(load(),indent=2))
