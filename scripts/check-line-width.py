"""Fails when a Markdown line is wider than 80 characters.

Usage: python3 -I scripts/check-line-width.py [file ...] (default: every tracked .md file)

Frontmatter, code blocks, tables, headings and HTML lines are exempt, and so is a line
that holds a single word (a long URL or path), since it cannot be broken.
"""
import re
import subprocess
import sys

WIDTH = 80


def long_lines(text):
    lines = text.split("\n")
    front = bool(lines) and lines[0] == "---"
    fence = False
    for n, line in enumerate(lines, 1):
        if front:
            front = not (n > 1 and line == "---")
            continue
        if re.match(r"\s*(```|~~~)", line):
            fence = not fence
            continue
        if fence or len(line) <= WIDTH or re.match(r"\s*(\||#|<)", line):
            continue
        if " " in re.sub(r"^\s*([-*+]|\d+[.)]|>)?\s*", "", line):
            yield n, len(line)


def main(paths):
    if not paths:
        out = subprocess.run(["git", "ls-files", "*.md"], capture_output=True, text=True, check=True)
        paths = out.stdout.splitlines()
    bad = 0
    for path in paths:
        with open(path, encoding="utf-8") as f:
            for n, width in long_lines(f.read()):
                print(f"{path}:{n}: {width} characters (limit {WIDTH})")
                bad = 1
    return bad


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
