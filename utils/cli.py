"""Shared command-line handling for the parser scripts.

Every parser used to select its input by having you EDIT THE SOURCE and
uncomment one of five `file_path = ...` lines. That is the single biggest piece
of friction in this repo: you cannot try your own PDF without opening a file
you did not write, and you cannot script a comparison across parsers at all.

This module gives every parser the same tiny interface instead:

    python parser/gemini/gemini.py                       # sample-1.pdf
    python parser/gemini/gemini.py --file input/sample-3.pdf
    python parser/gemini/gemini.py -f /path/to/your.pdf
    python parser/gemini/gemini.py --list

Paths are resolved against the repo root, so the scripts work from any
directory rather than only from the repo root.
"""

from __future__ import annotations

import argparse
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(PROJECT_ROOT, "input")

# The bundled samples, and what makes each one hard. Printed by --list.
SAMPLES = {
    "sample-1.pdf": "standard, machine-readable tables",
    "sample-2.pdf": "image-based simple tables (no text layer)",
    "sample-3.pdf": "image-based complex tables (merged cells, no grid lines)",
    "sample-4.pdf": "mixed content: text, tables and images together",
    "sample-5.pdf": "multi-column text (reading order is the problem)",
}


def list_samples() -> str:
    lines = ["Bundled sample PDFs (in input/):"]
    for name, description in SAMPLES.items():
        lines.append(f"  {name:16s} {description}")
    return "\n".join(lines)


def resolve(path: str) -> str:
    """Turn whatever the user typed into an absolute path that exists.

    Accepts an absolute path, a path relative to the repo root, a path
    relative to the current directory, or a bare sample name.
    """
    candidates = [
        path,
        os.path.join(PROJECT_ROOT, path),
        os.path.join(INPUT_DIR, os.path.basename(path)),
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)

    raise SystemExit(
        f"PDF not found: {path}\n\n"
        f"{list_samples()}\n\n"
        f"Pass one with --file, for example:\n"
        f"  --file input/sample-3.pdf"
    )


def input_pdf(default: str = "sample-1.pdf", description: str = "") -> str:
    """Parse argv and return an absolute path to the PDF to process."""
    parser = argparse.ArgumentParser(
        description=description or "Extract content from a PDF.",
        epilog=list_samples(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f", "--file", default=default,
        help=f"PDF to process. Default: input/{default}",
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List the bundled sample PDFs and exit.",
    )
    args = parser.parse_args()

    if args.list:
        print(list_samples())
        sys.exit(0)

    return resolve(args.file)


def output_path(name: str) -> str:
    """Absolute path for a parser's output, creating output/ if needed."""
    directory = os.path.join(PROJECT_ROOT, "output")
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, name)
