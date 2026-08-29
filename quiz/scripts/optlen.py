#!/usr/bin/env python3
"""Report length tells: a student must not be able to score by picking the longest
(or the shortest) option.
Usage: python3 scripts/optlen.py                  -> bank-wide summary
       python3 scripts/optlen.py <module.py> ...  -> per-item detail for those items/ modules
Flagged when the key is the longest option and len(key)/max(distractor) >= 1.15,
or the key is the shortest and len(key)/min(distractor) <= 0.87.
Target: every item unflagged, i.e. the key sits inside the pack.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import load_items

HI, LO = 1.15, 0.87

def score(it):
    k = len(it["options"][it["answer"]])
    others = [len(o) for i, o in enumerate(it["options"]) if i != it["answer"]]
    hi, lo = k / max(others), k / min(others)
    if k > max(others) and hi >= HI: return ("LONGEST", hi)
    if k < min(others) and lo <= LO: return ("SHORTEST", lo)
    return (None, hi)

items, srcs = load_items()
mods = [m if m.endswith(".py") else m + ".py" for m in sys.argv[1:]]

if not mods:
    b = collections.Counter(); over = collections.Counter()
    for it in items:
        kind, r = score(it)
        b[kind or "ok"] += 1
        if kind: over[srcs.get(it["id"])] += 1
    print(f"{len(items)} items: {dict(b)}")
    for m, n in over.most_common(): print(f"  {m:26} {n} flagged")
    sys.exit(1 if over else 0)

sel = [(it, *score(it)) for it in items if srcs.get(it["id"]) in mods]
sel = [s for s in sel if s[1]]
sel.sort(key=lambda s: -abs(s[2] - 1))
for it, kind, r in sel:
    ls = [len(o) for o in it["options"]]
    print(f"\n=== {it['id']}  ({srcs.get(it['id'])})  key is {kind}, ratio {r:.2f}  lengths {ls}")
    print(f"    stem: {it['stem'][:140]}")
    for i, o in enumerate(it["options"]):
        print(f"    [{i}] {'KEY ' if i == it['answer'] else 'dist'} {len(o):4d}  {o[:160]}")
print(f"\n{len(sel)} item(s) flagged in {', '.join(mods)}")
