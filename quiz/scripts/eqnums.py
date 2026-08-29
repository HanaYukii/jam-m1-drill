#!/usr/bin/env python3
"""Approximate LaTeX equation numbering for the Gray Paper source: label -> (section, number).
Walks graypaper.tex input order, counts numbered equation rows per \\section.
Handles equation/align/gather/alignat/multline environments, \\nonumber, \\notag, \\label.
Appendix sections lettered A.. after \\appendix.
"""
import re, sys, os, json
SRC = "../gp-src"
main = open(os.path.join(SRC, "graypaper.tex")).read()
files = re.findall(r"\\input\{(text/[^}]+)\}", main)
appendix_at = main.find("\\appendix")
# figure out which inputs are after \appendix
inputs_with_pos = [(m.start(), m.group(1)) for m in re.finditer(r"\\input\{(text/[^}]+)\}", main)]

sec_num = 0
app_idx = -1
labels = {}
env_re = re.compile(r"\\begin\{(equation\*?|align\*?|gather\*?|alignat\*?|multline\*?|flalign\*?|eqnarray\*?)\}(.*?)\\end\{\1\}", re.S)

def process_env(kind, body, secname, counter):
    """Return updated counter, record labels."""
    starred = kind.endswith("*")
    if kind.startswith("equation") or kind.startswith("multline"):
        rows = [body]
    else:
        # split rows on \\ not inside braces (approximate)
        rows, depth, cur = [], 0, ""
        i = 0
        while i < len(body):
            if body.startswith("\\begin{", i):
                depth += 1
            elif body.startswith("\\end{", i):
                depth -= 1
            elif body[i] == "{" and not body.startswith("\\{", i-1):
                depth += 1
            elif body[i] == "}" and not body.startswith("\\}", i-1):
                depth -= 1
            if body.startswith("\\\\", i) and depth == 0:
                rows.append(cur); cur = ""; i += 2; continue
            cur += body[i]; i += 1
        rows.append(cur)
    for row in rows:
        if row.strip() == "":
            continue
        # nested environments like cases/aligned don't get numbers
        numbered = (not starred) and ("\\nonumber" not in row) and ("\\notag" not in row)
        labs = re.findall(r"\\label\{([^}]+)\}", row)
        if numbered:
            counter += 1
            for l in labs:
                labels[l] = f"{secname}.{counter}"
        else:
            for l in labs:
                labels[l] = f"{secname}.(unnumbered)"
    return counter

for pos, f in inputs_with_pos:
    is_app = pos > appendix_at
    txt = open(os.path.join(SRC, f)).read()
    # remove comments
    txt = re.sub(r"(?<!\\)%.*", "", txt)
    # iterate through sections and envs in order
    tokens = []
    for m in re.finditer(r"\\section\{", txt):
        tokens.append((m.start(), "sec"))
    for m in env_re.finditer(txt):
        tokens.append((m.start(), ("env", m.group(1), m.group(2))))
    tokens.sort(key=lambda t: t[0])
    for pos2, t in tokens:
        if t == "sec":
            if is_app:
                app_idx += 1
            else:
                sec_num += 1
            counter = 0
            globals()["counter"] = 0
        else:
            _, kind, body = t
            secname = chr(ord("A") + app_idx) if is_app else str(sec_num)
            globals()["counter"] = process_env(kind, body, secname, globals().get("counter", 0))

json.dump(labels, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "eqnums.json"), "w"), indent=1)
for k in sys.argv[1:]:
    print(k, labels.get(k))
