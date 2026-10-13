#!/usr/bin/env python3
"""Create the delivery PDF at 300 dpi while preserving the full source assets.
Run: uv run --with pymupdf==1.28.2 python preprint/optimize_pdf.py INPUT OUTPUT
"""
import sys
from pathlib import Path
import pymupdf

source,target=map(Path,sys.argv[1:])
with pymupdf.open(source) as doc:
    texts=[page.get_text() for page in doc]
    doc.rewrite_images(dpi_threshold=350,dpi_target=300,quality=95)
    doc.save(target,garbage=4,deflate=True,use_objstms=1)
with pymupdf.open(target) as doc:
    assert [page.get_text() for page in doc]==texts
print(f'Preserved all text and {len(texts)} pages; {source.stat().st_size} -> {target.stat().st_size} bytes')
