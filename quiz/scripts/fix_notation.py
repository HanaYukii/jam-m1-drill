#!/usr/bin/env python3
"""One-off: bring item text in line with GP 0.8.0 symbol names (verified against gp-src/preamble.tex)."""
import re, glob, sys

FIELDS = ("stem","explanation","trap")
def apply(text):
    # 1. PVM registers: ω_n -> φ_n  (0.8.0: \registers = varphi; omega is the ready queue)
    text = re.sub(r"ω(['′]?)_(\{?)([0-9A-Za-z])", r"φ\1_\2\3", text)
    text = text.replace("ω_reg", "φ_reg")
    # 2. ready queue ϑ -> ω
    text = text.replace("ϑ", "ω")
    # 3. ticket entry index i_r -> i_e
    text = text.replace("i_r", "i_e")
    # 4. header subscripts are uppercase in 0.8.0
    for lo, up in [("t","T"),("i","I"),("p","P"),("r","R"),("x","X"),("e","E"),
                   ("w","W"),("o","O"),("v","V"),("s","S"),("a","A")]:
        text = re.sub(r"\bH_" + lo + r"\b", "H_" + up, text)
        text = re.sub(r"\bH['′]_" + lo + r"\b", "H′_" + up, text)
    # 5. reporters set R -> G   (do BEFORE W -> R)
    text = text.replace("reporters set R", "reporters set G").replace("reporters 集合 R", "reporters 集合 G")
    text = text.replace("the reporters set R", "the reporters set G")
    # 6. newly-available reports W -> R  (never touch W_x constants)
    text = text.replace("W!", "R!").replace("W^Q", "R^Q").replace("W*", "R*")
    text = re.sub(r"\bW\b(?!_)(?!\s*=)", "R", text)
    return text

changed = 0
for path in glob.glob("items/*.py"):
    src = open(path, encoding="utf-8").read()
    out = []
    # operate only inside the three text fields to avoid touching ids/tags/code
    def repl(m):
        global changed
        key, val = m.group(1), m.group(2)
        new = apply(val)
        if new != val:
            changed += 1
        return f'"{key}": "{new}"'
    new_src = re.sub(r'"(stem|explanation|trap)": "((?:[^"\\]|\\.)*)"', repl, src)
    # options are a list of strings; handle them separately
    def repl_opts(m):
        global changed
        body = m.group(1)
        def r2(mm):
            global changed
            v = mm.group(1)
            n = apply(v)
            if n != v: changed += 1
            return '"' + n + '"'
        return '"options": [' + re.sub(r'"((?:[^"\\]|\\.)*)"', r2, body) + ']'
    new_src = re.sub(r'"options": \[((?:[^\[\]]|\[[^\]]*\])*)\]', repl_opts, new_src, flags=re.S)
    if new_src != src:
        open(path, "w", encoding="utf-8").write(new_src)
        print("patched", path)
print("field edits:", changed)
