#!/usr/bin/env python3
"""Run the narrow verification cone for the clean-room state model."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    command = [
        sys.executable,
        "-m",
        "unittest",
        "discover",
        "-s",
        "tests",
        "-t",
        ".",
    ]
    environment = os.environ.copy()
    engine_path = str(ROOT / "engine")
    existing_path = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        engine_path if not existing_path else os.pathsep.join((engine_path, existing_path))
    )
    completed = subprocess.run(command, cwd=ROOT, env=environment, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
