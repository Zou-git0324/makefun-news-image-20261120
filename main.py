"""Entry point: copy the pre-rendered image to the output directory.

Standard library only. The image itself (entry.png, in this repository)
was drawn at build time by draw_entry.py; this program just places the
exact bytes at /output/entry.png, so two runs produce byte-identical
output with no network, no clock and no randomness.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
