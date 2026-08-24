#!/usr/bin/env python3
"""Build the closed Lean proof from any working directory."""

from pathlib import Path
import shutil
import subprocess


def lake_executable(lean_dir: Path) -> str:
    if lake := shutil.which("lake"):
        return lake

    toolchain = (lean_dir / "lean-toolchain").read_text().strip()
    encoded = toolchain.replace("/", "--").replace(":", "---")
    installed = Path.home() / ".elan" / "toolchains" / encoded / "bin" / "lake"
    if installed.is_file():
        return str(installed)
    raise SystemExit("lake is required")


def main() -> None:
    lean_dir = Path(__file__).parent / "lean"
    subprocess.run([lake_executable(lean_dir), "build"], cwd=lean_dir, check=True)
    print("verified: ∀ s, ExactlyOneBlack s → ReachesP104 s")


if __name__ == "__main__":
    main()
