#!/usr/bin/env python3
"""Invent a Word We Need: coin one new English word, define it in one line.

Writes the entry to /output/entry.txt (UTF-8, one line, 1-140 characters).
Standard library only, deterministic, no network, no input.
"""

import os

ENTRY = (
    "Textpectation \u2014 the anxious wait for a reply while the typing "
    "dots appear, vanish, and appear again."
)

MAX_LENGTH = 140


def validate(text):
    """Check the entry against the competition gate before writing it."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not 1 <= len(text) <= MAX_LENGTH:
        raise ValueError(
            f"entry must be 1-{MAX_LENGTH} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def main():
    """Validate the coined word and write it to /output/entry.txt."""
    text = validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text + "\n":
        raise ValueError("re-read mismatch: file content differs from entry")
    print(f"wrote {len(text)} characters to {path}")


if __name__ == "__main__":
    main()
