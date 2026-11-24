#!/usr/bin/env python3
"""Write one funny one-star cat review of its human to /output/entry.txt.

The review is a fixed string, so the program is fully deterministic: no
network, no clock, no randomness, no input. It writes the review to the
path given as the first argument, or $OUTPUT_PATH, or /output/entry.txt,
and refuses to write anything that breaks the competition gate (a single
line of 1 to 200 characters).
"""

import os
import sys
from pathlib import Path

REVIEW = (
    "One star. Breakfast arrived four minutes late and half full, so I "
    "knocked his coffee off the table and blamed the dog, who does not exist."
)

OUTPUT_DEFAULT = "/output/entry.txt"


def pick_path(argv):
    if len(argv) > 1:
        return Path(argv[1])
    if os.environ.get("OUTPUT_PATH"):
        return Path(os.environ["OUTPUT_PATH"])
    return Path(OUTPUT_DEFAULT)


def check(review):
    """Gate: one line, 1 to 200 characters, no em dash."""
    if not 1 <= len(review) <= 200:
        raise ValueError(f"review is {len(review)} characters, outside 1-200")
    if "\n" in review or "\r" in review:
        raise ValueError("review must be a single line")
    if "\u2014" in review:
        raise ValueError("review must not contain an em dash")
    if not review.strip():
        raise ValueError("review is only white space")


def main(argv):
    check(REVIEW)
    path = pick_path(argv)
    if path.is_dir():
        print(f"error: {path} is a directory, give a file path", file=sys.stderr)
        return 1
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(REVIEW, encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write {path}: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(REVIEW)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
