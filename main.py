#!/usr/bin/env python3
"""Copy the pre-rendered front page to /output/entry.png.

Stdlib only. Verifies the copy (JPEG magic, byte size) and exits
non-zero on any failure. Cleans only the contents of /output, never
the folder itself (the grader mounts it).
"""
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT_DIR = "/output"
OUT = os.path.join(OUT_DIR, "entry.png")
MAX_BYTES = 1048576


def fail(msg):
    print("main.py: " + msg, file=sys.stderr)
    return 1


def main():
    if not os.path.isfile(SRC):
        return fail("entry.png missing from repo")
    with open(SRC, "rb") as f:
        data = f.read()
    if len(data) < 3 or data[:3] != b"\xff\xd8\xff":
        return fail("entry.png is not a JPEG")
    if len(data) > MAX_BYTES:
        return fail("entry.png over 1 MiB: %d bytes" % len(data))
    os.makedirs(OUT_DIR, exist_ok=True)
    for name in os.listdir(OUT_DIR):
        path = os.path.join(OUT_DIR, name)
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
    shutil.copyfile(SRC, OUT)
    with open(OUT, "rb") as f:
        copied = f.read()
    if copied != data:
        return fail("verify-after-copy mismatch")
    print("wrote /output/entry.png (%d bytes)" % len(copied))
    return 0


if __name__ == "__main__":
    sys.exit(main())
