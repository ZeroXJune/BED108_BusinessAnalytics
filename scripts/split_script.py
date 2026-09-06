"""
Splits the recording script into one document per speaker: the shared preamble
plus only the parts that speaker records.

Run:  python3 scripts/split_script.py
Then: python3 scripts/build_docx.py docs/parts/<x>.md docs/Script_<X>.docx
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "discussion_script.md")
OUTDIR = os.path.join(ROOT, "docs", "parts")
SPEAKERS = ["Alber", "Julebeth", "Mardy"]


def main():
    text = open(SRC).read()
    marks = [m.start() for m in re.finditer(r"^# Part ", text, re.M)]
    assert marks, "no parts found"
    bounds = marks + [len(text)]
    preamble = text[:marks[0]]
    parts = [text[a:b] for a, b in zip(bounds, bounds[1:])]

    os.makedirs(OUTDIR, exist_ok=True)
    for name in SPEAKERS:
        mine = [p for p in parts if re.match(r"# Part \d+ — %s\b" % name, p)]
        assert mine, name
        out = os.path.join(OUTDIR, "discussion_script_%s.md" % name.lower())
        with open(out, "w") as fh:
            fh.write(preamble.replace(
                "| Part | Speaker | Covers | Approx |",
                "**%s reads the parts below.** The full running order:\n\n"
                "| Part | Speaker | Covers | Approx |" % name))
            fh.write("".join(mine))
        print("wrote %s (%d part%s)"
              % (out, len(mine), "" if len(mine) == 1 else "s"))


if __name__ == "__main__":
    main()
