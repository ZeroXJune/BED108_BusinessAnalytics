"""
Renders the Entity-Relationship Diagram for the Checkpoint 1 report.

The diagram is generated from the schema itself, never hand-drawn, so it
cannot drift from the database. The MySQL DDL is parsed for column names,
types and keys, and the result is cross-checked against the live SQLite build
before anything is drawn - a mismatch fails the run rather than producing a
diagram that quietly lies.

Outputs:
    docs/figures/erd.png   300 dpi, for pasting into the Word report
    docs/figures/erd.svg   vector, for printing or zooming
    docs/figures/erd.dot   the Graphviz source

Run:  python3 scripts/make_erd.py
"""

import os
import re
import shutil
import sqlite3
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "sql", "01_schema_mysql.sql")
DB = os.path.join(ROOT, "data", "sales_trend.db")
FIG = os.path.join(ROOT, "docs", "figures")

# Palette shared with the report figures.
INK = "#1f2933"
ACCENT = "#2f6f9f"
FACT_FILL = "#2f6f9f"
FACT_TEXT = "#ffffff"
DIM_HEAD = "#dce6f1"
BODY = "#ffffff"
LINE = "#8fa3b5"
MUTED = "#5a6672"

# sales holds the additive measures; everything else describes and labels.
FACT_TABLE = "sales"


def parse_schema(path):
    """Pull tables, columns, types, primary keys and foreign keys from DDL."""
    text = open(path, encoding="utf-8").read()
    tables = {}
    for m in re.finditer(r"CREATE TABLE\s+(\w+)\s*\((.*?)\n\)\s*ENGINE",
                         text, re.S):
        name, body = m.group(1), m.group(2)
        cols, pks, fks = [], set(), {}
        for raw in body.split("\n"):
            line = raw.strip().rstrip(",")
            if not line or line.startswith("--"):
                continue
            pk = re.match(r"CONSTRAINT\s+\w+\s+PRIMARY KEY\s*\(([^)]+)\)", line)
            if pk:
                pks.update(c.strip().strip("`") for c in pk.group(1).split(","))
                continue
            fk = re.match(r"CONSTRAINT\s+\w+\s+FOREIGN KEY\s*\(([^)]+)\)", line)
            if fk:
                fks[fk.group(1).strip().strip("`")] = None
                continue
            ref = re.match(r"REFERENCES\s+(\w+)\s*\(([^)]+)\)", line)
            if ref and fks:
                last = list(fks)[-1]
                fks[last] = (ref.group(1), ref.group(2).strip().strip("`"))
                continue
            if line.startswith(("CONSTRAINT", "REFERENCES", ")")):
                continue
            col = re.match(r"`?(\w+)`?\s+([A-Z]+(?:\([^)]*\))?)", line)
            if col:
                cols.append((col.group(1), col.group(2)))
        tables[name] = {"columns": cols, "pk": pks, "fk": fks}
    return tables


def verify(tables):
    """Fail loudly if the parsed DDL disagrees with the built database."""
    if not os.path.exists(DB):
        sys.exit("data/sales_trend.db is missing - run clean_and_load.py first")
    con = sqlite3.connect(DB)
    live = {r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' "
        "AND name NOT LIKE 'sqlite_%'")}
    parsed = set(tables)
    if live != parsed:
        sys.exit(f"table mismatch\n  in DDL only: {parsed - live}\n"
                 f"  in DB only:  {live - parsed}")

    problems = []
    for name, spec in tables.items():
        db_cols = [r[1] for r in con.execute(f"PRAGMA table_info({name})")]
        if db_cols != [c for c, _ in spec["columns"]]:
            problems.append(f"{name}: columns {spec['columns']} vs {db_cols}")
        db_pk = {r[1] for r in con.execute(f"PRAGMA table_info({name})") if r[5]}
        if db_pk != spec["pk"]:
            problems.append(f"{name}: pk {spec['pk']} vs {db_pk}")
        db_fk = {r[3]: (r[2], r[4])
                 for r in con.execute(f"PRAGMA foreign_key_list({name})")}
        if db_fk != spec["fk"]:
            problems.append(f"{name}: fk {spec['fk']} vs {db_fk}")
    con.close()
    if problems:
        sys.exit("schema/DDL mismatch:\n  " + "\n  ".join(problems))
    n_fk = sum(len(t["fk"]) for t in tables.values())
    print(f"verified against the database: {len(tables)} tables, "
          f"{sum(len(t['columns']) for t in tables.values())} columns, "
          f"{n_fk} foreign keys")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def table_node(name, spec):
    """A table drawn as an HTML-like label: header plus one row per column."""
    is_fact = name == FACT_TABLE
    head_bg = FACT_FILL if is_fact else DIM_HEAD
    head_fg = FACT_TEXT if is_fact else INK
    role = "FACT TABLE" if is_fact else "dimension"

    rows = [
        f'<TR><TD BGCOLOR="{head_bg}" COLSPAN="3" ALIGN="CENTER">'
        f'<FONT COLOR="{head_fg}" POINT-SIZE="13"><B>{esc(name)}</B></FONT>'
        f'<BR/><FONT COLOR="{head_fg}" POINT-SIZE="8">{role}</FONT></TD></TR>'
    ]
    for col, typ in spec["columns"]:
        marks = []
        if col in spec["pk"]:
            marks.append("PK")
        if col in spec["fk"]:
            marks.append("FK")
        key = ",".join(marks)
        # Graphviz rejects an empty <B></B>, so only emit markup when there
        # is actually a key to show.
        key_cell = (f'<FONT COLOR="{ACCENT}" POINT-SIZE="8"><B>{key}</B></FONT>'
                    if key else " ")
        name_cell = (f"<B>{esc(col)}</B>" if key else esc(col))
        rows.append(
            f'<TR>'
            f'<TD ALIGN="LEFT" WIDTH="36">{key_cell}</TD>'
            f'<TD ALIGN="LEFT" PORT="{esc(col)}">'
            f'<FONT POINT-SIZE="10">{name_cell}</FONT></TD>'
            f'<TD ALIGN="LEFT"><FONT COLOR="{MUTED}" POINT-SIZE="8">'
            f'{esc(typ)}</FONT></TD>'
            f'</TR>'
        )
    return (f'  {name} [label=<<TABLE BORDER="1" CELLBORDER="0" '
            f'CELLSPACING="0" CELLPADDING="5" BGCOLOR="{BODY}" '
            f'COLOR="{LINE}">' + "".join(rows) + "</TABLE>>];")


def build_dot(tables):
    lines = [
        "digraph erd {",
        '  graph [rankdir=LR, splines=polyline, nodesep=0.55, ranksep=1.5,',
        '         bgcolor="white", fontname="Helvetica", pad=0.35];',
        f'  node  [shape=plaintext, fontname="Helvetica", color="{LINE}"];',
        f'  edge  [color="{LINE}", penwidth=1.3, arrowsize=0.9,',
        f'         fontname="Helvetica", fontsize=9, fontcolor="{MUTED}"];',
        "",
    ]
    for name in sorted(tables):
        lines.append(table_node(name, tables[name]))
    lines.append("")

    # One edge per foreign key, drawn parent -> child in crow's-foot notation:
    # a bar at the "one" end, a crow's foot at the "many" end.
    for child in sorted(tables):
        for col, ref in sorted(tables[child]["fk"].items()):
            parent, pcol = ref
            lines.append(
                f'  {parent}:{pcol}:e -> {child}:{col}:w '
                f'[dir=both, arrowtail=tee, arrowhead=crow];'
            )
    lines += [
        "",
        "  subgraph cluster_legend {",
        '    label=<<FONT POINT-SIZE="10" COLOR="' + MUTED + '">'
        '<B>How to read this diagram</B></FONT>>;',
        f'    color="{LINE}"; style=dashed; fontname="Helvetica";',
        '    legend [label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="2" '
        'CELLPADDING="3">'
        f'<TR><TD ALIGN="LEFT"><FONT COLOR="{ACCENT}" POINT-SIZE="9">'
        '<B>PK</B></FONT></TD><TD ALIGN="LEFT">'
        '<FONT POINT-SIZE="9">primary key &#8212; uniquely identifies a row'
        '</FONT></TD></TR>'
        f'<TR><TD ALIGN="LEFT"><FONT COLOR="{ACCENT}" POINT-SIZE="9">'
        '<B>FK</B></FONT></TD><TD ALIGN="LEFT">'
        '<FONT POINT-SIZE="9">foreign key &#8212; points at another table&#8217;s '
        'primary key</FONT></TD></TR>'
        '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9"><B>&#8213;|</B></FONT></TD>'
        '<TD ALIGN="LEFT"><FONT POINT-SIZE="9">the &#8220;one&#8221; side of a '
        'relationship</FONT></TD></TR>'
        '<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="9"><B>&#8250;&#8212;</B></FONT>'
        '</TD><TD ALIGN="LEFT"><FONT POINT-SIZE="9">crow&#8217;s foot &#8212; '
        'the &#8220;many&#8221; side</FONT></TD></TR>'
        f'<TR><TD ALIGN="LEFT" BGCOLOR="{FACT_FILL}"> </TD>'
        '<TD ALIGN="LEFT"><FONT POINT-SIZE="9">fact table (holds the measures)'
        '</FONT></TD></TR>'
        f'<TR><TD ALIGN="LEFT" BGCOLOR="{DIM_HEAD}"> </TD>'
        '<TD ALIGN="LEFT"><FONT POINT-SIZE="9">dimension (describes and labels)'
        '</FONT></TD></TR>'
        "</TABLE>>];",
        "  }",
    ]
    lines.append("}")
    return "\n".join(lines)


def main():
    if not shutil.which("dot"):
        sys.exit("Graphviz is not installed. Try: apt-get install graphviz")
    os.makedirs(FIG, exist_ok=True)

    tables = parse_schema(SCHEMA)
    verify(tables)

    dot_path = os.path.join(FIG, "erd.dot")
    with open(dot_path, "w", encoding="utf-8") as fh:
        fh.write(build_dot(tables))

    for fmt, extra in (("png", ["-Gdpi=300"]), ("svg", [])):
        out = os.path.join(FIG, f"erd.{fmt}")
        subprocess.run(["dot", f"-T{fmt}", *extra, dot_path, "-o", out],
                       check=True)
        print("wrote", out)


if __name__ == "__main__":
    main()
