#!/usr/bin/env python3
"""Look up Gray Paper 0.8.0 equation numbers by LaTeX label (substring match).
Usage: python3 scripts/eqref.py ticketcondition seal   -> prints matching labels with numbers
       python3 scripts/eqref.py --section 11            -> lists all labelled equations of section 11
Numbers were derived from the LaTeX source and cross-checked against the PDF (per-section totals match).
Unlabelled equations are not listed; count rows in the .tex align environment from the nearest labelled one.
"""
import json, sys, os
d = json.load(open(os.path.join(os.path.dirname(__file__), "eqnums.json")))
args = sys.argv[1:]
if not args:
    print(__doc__); sys.exit(0)
if args[0] == "--section":
    sec = args[1]
    rows = [(v, k) for k, v in d.items() if v.split(".")[0] == sec]
    rows.sort(key=lambda r: (int(r[0].split(".")[1]) if r[0].split(".")[1].isdigit() else 999))
    for v, k in rows: print(v, k)
else:
    for q in args:
        for k, v in d.items():
            if q.lower() in k.lower(): print(v, k)
