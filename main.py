"""News image entry: copy the front page to the grader output.

The image (entry.png, 1024x1024, drawn by draw_frontpage.py from
20 November 2026 reporting) sits beside this file. No network is
used and the copy is byte-for-byte identical on every run.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    src = HERE / "entry.png"
    dst = OUT / "entry.png"
    shutil.copyfile(src, dst)
    # Fail loudly instead of submitting a truncated copy.
    assert dst.stat().st_size == src.stat().st_size
    assert dst.stat().st_size <= 1048576


if __name__ == "__main__":
    main()
