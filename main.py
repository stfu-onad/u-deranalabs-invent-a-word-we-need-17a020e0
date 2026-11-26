#!/usr/bin/env python3
"""Invent a Word We Need: coin one new English word, define it in one line.

The coinage
----------
``Inboxiety`` — the quiet dread of opening an inbox that only ever grows.

Etymology: ``inbox`` + ``anxiety``, clipped at the shared ``x`` sound so the
blend stays pronounceable in one breath: in-BOX-ie-ty. The word names a
feeling almost everyone with an email account or a messaging app already
knows, but which has no name of its own yet: not the panic of one urgent
message, and not the boredom of an empty inbox, but the low, specific dread
that builds while unread counts climb and opening the app feels like opening
a door you know leads to more work than you have hours for.

Why this word, and why now: inboxes never empty. They refill overnight, over
a weekend, over a holiday, and the number beside the icon only ever points
one way. ``Inboxiety`` gives that creeping reluctance a handle short enough
to say out loud — "sorry, inboxiety got me again" — which is exactly what a
new word has to do to earn its keep: compress a shared experience into a
single sayable unit.

The program below does one small, deterministic job. It assembles the entry
from its parts (the coined word, an em dash, and the one-line definition),
checks the result against every gate the competition states — one word, one
line, between 1 and 140 characters, real text and not only whitespace — and
writes it to ``/output/entry.txt`` as UTF-8. It then reads the file back and
refuses to report success unless the bytes on disk match the entry exactly.

Standard library only. No network, no input, no randomness, no arguments.
The same command always writes the same file.
"""

import os
import sys

# --- The entry itself -------------------------------------------------------

# The coined word. One token, letters only, capitalised the way a dictionary
# headword is capitalised.
WORD = "Inboxiety"

# The definition, kept as a list of clauses so each one can be read, counted
# and, if ever needed, revised on its own line without touching the rest.
DEFINITION_CLAUSES = [
    "the quiet dread of opening an inbox",
    "that only ever grows.",
]

# The separator between the word and its definition: an em dash, the usual
# dictionary convention for "is defined as".
SEPARATOR = "\u2014"

# Competition gates for the finished line, taken from the bounty rules.
MIN_CHARS = 1
MAX_CHARS = 140


def assemble_entry():
    """Join the coined word, the separator and the definition into one line.

    The clauses are joined with single spaces first, so the definition reads
    as one flowing sentence, and the word is joined to it with the separator
    spaced on both sides: ``Word — definition.``
    """
    definition = " ".join(DEFINITION_CLAUSES)
    return f"{WORD} {SEPARATOR} {definition}"


def check_single_word(word):
    """The headword must be exactly one word: letters, no spaces, no digits."""
    if not word:
        raise ValueError("coined word must not be empty")
    if not word.isalpha():
        raise ValueError(f"coined word must be letters only, got {word!r}")
    if " " in word or "-" in word:
        raise ValueError(f"coined word must be a single token, got {word!r}")
    return word


def check_entry(text):
    """Check the assembled line against every gate the competition states.

    Raises ValueError with a plain message on the first gate that fails, so
    a bad entry is never written out and mistaken for a good one.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, "
            f"got {len(text)}"
        )
    if not text.startswith(WORD + " "):
        raise ValueError("entry must start with the coined word")
    # A definition that repeats the word it defines is circular: it explains
    # nothing. The definition must stand on ordinary words alone, so the
    # coined word may appear exactly once — as the headword, never again.
    if text.count(WORD) != 1:
        raise ValueError("definition must not repeat the coined word")
    return text


def resolve_output_dir():
    """Where entry.txt goes.

    The harness mounts ``/output``; the environment variable only lets a
    local run point the file elsewhere for a dry run. It is read as a plain
    path, never executed, and the default is used whenever it is unset.
    """
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def write_entry(text, out_dir):
    """Write the entry, then read it back and prove the disk matches."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text + "\n":
        raise ValueError("re-read mismatch: file content differs from entry")
    return path


def main():
    """Assemble the entry, check it, write it, and report what was done."""
    check_single_word(WORD)
    text = check_entry(assemble_entry())
    path = write_entry(text, resolve_output_dir())
    print(f"wrote {len(text)} characters to {path}")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
