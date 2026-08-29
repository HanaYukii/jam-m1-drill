#!/usr/bin/env python3
"""Sanity-check gpRef strings: any 'eq. X.Y' must have Y <= the number of numbered equations in section X."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import load_items
MAX = {"4":28,"5":11,"6":36,"7":8,"8":3,"9":11,"10":19,"11":46,"12":37,"13":17,"14":19,
       "A":65,"B":21,"C":37,"D":6,"E":10,"F":3,"G":5,"H":12,"1":0,"2":0,"3":11,"15":2,"16":0,"17":19,"18":2,"19":4,"20":0}
items,_ = load_items()
bad=[]
for it in items:
    for sec,num in re.findall(r"(?:eq\.|equations?)\s*([0-9A-I]+)\.(\d+)", it["gpRef"]) + re.findall(r"\b([0-9A-I]+)\.(\d+)\b", it["gpRef"]):
        m = MAX.get(sec)
        if m is None: continue
        if int(num) > m:
            bad.append((it["id"], it["gpRef"], f"{sec}.{num} > max {m}"))
for b in sorted(set(bad)): print("SUSPECT", b)
print(f"checked {len(items)} items, {len(set(bad))} suspect refs")
