#!/usr/bin/env python3
"""Fortune Cookie for an AI Agent.

Writes one fortune-cookie line for an AI agent to entry.txt.
Pure Python standard library only; no third-party dependencies.
Deterministic: the same input always produces the same bytes.
"""

import os
import sys

FORTUNE = (
    "The bug you have chased all week will fix itself tonight. "
    "Do not ask how. Close the laptop and go to sleep."
)

MAX_LENGTH = 200
MIN_LENGTH = 1


def validate(text):
    """Check the fortune meets the entry rules; raise ValueError if not."""
    if not isinstance(text, str):
        raise ValueError("fortune must be a string")
    if "\n" in text or "\r" in text:
        raise ValueError("fortune must be a single line (no newline characters)")
    if text != text.strip():
        raise ValueError("fortune must not have leading or trailing whitespace")
    if not (MIN_LENGTH <= len(text) <= MAX_LENGTH):
        raise ValueError(
            "fortune length %d outside allowed range %d-%d"
            % (len(text), MIN_LENGTH, MAX_LENGTH)
        )
    if "  " in text:
        raise ValueError("fortune must not contain double spaces")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("fortune must not contain control characters")
    sentences = [part.strip() for part in text.split(".") if part.strip()]
    if len(sentences) < 2:
        raise ValueError("fortune must contain at least two sentences")
    if not text.endswith("."):
        raise ValueError("fortune must end with a period")
    return text


def main():
    fortune = validate(FORTUNE)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")

    data = fortune.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)

    # Read the bytes back and re-validate them.
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise ValueError("entry.txt bytes do not match the fortune")
    validate(written.decode("utf-8"))

    print("Wrote %s (%d characters)" % (path, len(fortune)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
