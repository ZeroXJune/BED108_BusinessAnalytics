"""
Splits the recording script into one document per speaker, so each member gets
only the parts they record plus the shared instructions.

Run:  python3 scripts/split_script.py
Then: python3 scripts/build_docx.py docs/parts/<x>.md docs/Script_<X>.docx
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "discussion_script.md")
OUTDIR = os.path.join(ROOT, "docs", "parts")

# Alber records the opening and the close, and edits, so his copy also keeps
# the assembly notes.
SPEAKERS = [("Alber", True), ("Julebeth", False), ("Mardy", False)]


def sections(text, level):
    """Split markdown on headings of exactly `level`, keeping the heading."""
    marks = [m.start() for m in
             re.finditer(r"^%s (?!#)" % ("#" * level), text, re.M)]
    marks.append(len(text))
    return [text[a:b] for a, b in zip(marks, marks[1:])]


def main():
    text = open(SRC).read()
    parts = sections(text, 1)
    shared = sections(text, 2)
    preamble = text[:text.index("## Before you record")]

    def shared_block(title):
        for s in shared:
            if s.startswith("## " + title):
                return s
        raise KeyError(title)

    os.makedirs(OUTDIR, exist_ok=True)

    for name, is_editor in SPEAKERS:
        mine = [p for p in parts
                if re.match(r"# Part \d+ — %s\b" % name, p)]
        assert mine, name

        body = [
            preamble.replace(
                "Each speaker records their own part",
                "**%s's part.** Each speaker records their own part" % name),
            shared_block("Before you record"),
            shared_block("How to record your part"),
        ]
        if is_editor:
            body.append(shared_block("For Alber, as editor"))
        body.extend(mine)
        body.append(shared_block("Checklist"))

        out = os.path.join(OUTDIR, "discussion_script_%s.md" % name.lower())
        with open(out, "w") as fh:
            fh.write("\n".join(b.rstrip() + "\n" for b in body))
        print("wrote %s (%d part%s)"
              % (out, len(mine), "" if len(mine) == 1 else "s"))


if __name__ == "__main__":
    main()
