"""
Splits the group discussion script into one document per speaker, so each
member gets only the clips they record plus the shared instructions.

Run:  python3 scripts/split_script.py
Then: python3 scripts/build_docx.py docs/parts/<x>.md docs/<X>.docx
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs", "discussion_script.md")
OUTDIR = os.path.join(ROOT, "docs", "parts")

# The leader also edits, so Alber's copy keeps the assembly order and cut list.
SPEAKERS = [
    ("Alber", "A", True),
    ("Julebeth", "B", False),
    ("Mardy", "C", False),
]


def sections(text, level):
    """Split markdown on headings of exactly `level`, keeping the heading."""
    pattern = re.compile(r"^%s (?!#)" % ("#" * level), re.M)
    marks = [m.start() for m in pattern.finditer(text)]
    marks.append(len(text))
    return [text[a:b] for a, b in zip(marks, marks[1:])]


def main():
    text = open(SRC).read()
    parts = {s.split("\n", 1)[0].strip(): s for s in sections(text, 1)}
    shared = sections(text, 2)

    def shared_block(title):
        for s in shared:
            if s.startswith("## " + title):
                return s
        raise KeyError(title)

    preamble = text[:text.index("## Before you record")]
    os.makedirs(OUTDIR, exist_ok=True)

    for name, letter, is_editor in SPEAKERS:
        body = [
            preamble.replace(
                "A recording script for three speakers who record",
                "**%s's part.** A recording script for three speakers who record"
                % name),
            shared_block("Before you record"),
            shared_block("How this works when you record separately"),
        ]
        if is_editor:
            body.append(shared_block("For Alber, as editor"))
        body.append(parts["# Part %s — %s" % (letter, name)])
        body.append(shared_block("Rehearsal checklist"))

        out = os.path.join(OUTDIR, "discussion_script_%s.md" % name.lower())
        with open(out, "w") as fh:
            fh.write("\n".join(b.rstrip() + "\n" for b in body))
        clips = len(re.findall(r"^## Clip", parts["# Part %s — %s"
                                                 % (letter, name)], re.M))
        print("wrote %s (%d clips)" % (out, clips))


if __name__ == "__main__":
    main()
