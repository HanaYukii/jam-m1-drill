#!/usr/bin/env python3
"""Build the JAM M1 Drill: items/*.py -> dist/questions.json, dist/artifact.html (fragment), dist/jam-m1-drill.html (standalone)."""
import json, os, sys, random, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import load_items, validate, CHAPTERS, load_terms, validate_terms, GLOSS_CATS, load_sheets, validate_sheets

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
os.makedirs(DIST, exist_ok=True)

BANK_VERSION = "bank v1.0 (" + datetime.date.today().isoformat() + ")"
GROUPS = {
    **{k: "Chapters 3–13" for k in ["3","4","5","6","7","8","9","10","11","12","13"]},
    "14": "Off-chain (14+)",
    **{k: "Appendices" for k in ["A","B","C","D","E","F","G","H"]},
    "ARCH": "Interview extras",
}

def shuffle_options(item):
    """Deterministic per-item shuffle so the exported bank isn't 'answer = A' everywhere."""
    rnd = random.Random("jam-m1:" + item["id"])
    order = [0, 1, 2, 3]
    rnd.shuffle(order)
    new_opts = [item["options"][i] for i in order]
    new_ans = order.index(item["answer"])
    out = dict(item)
    out["options"] = new_opts
    out["answer"] = new_ans
    if item.get("optNotes"):
        out["optNotes"] = [item["optNotes"][i] for i in order]
    return out

def main():
    items, srcs = load_items()
    errors, warnings = validate(items, srcs)
    if errors:
        for e in errors: print("ERROR:", e)
        sys.exit(1)
    terms, tsrcs = load_terms()
    gerr = validate_terms(terms, tsrcs)
    if gerr:
        for e in gerr: print("ERROR:", e)
        sys.exit(1)
    sheets = load_sheets()
    serr = validate_sheets(sheets)
    if serr:
        for e in serr: print("ERROR:", e)
        sys.exit(1)
    items = [shuffle_options(i) for i in items]
    chapters = [{"key": k, "name": v, "group": GROUPS.get(k, "Other")} for k, v in CHAPTERS.items()]
    data = {
        "meta": {
            "bankVersion": BANK_VERSION,
            "gpVersion": "Gray Paper 0.8.0",
            "team": "New-JAMneration M1 interview prep",
            "chapters": chapters,
            "count": len(items),
            "glossaryCats": GLOSS_CATS,
        },
        "items": items,
        "terms": terms,
        "sheets": sheets,
    }
    json_txt = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(DIST, "questions.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    safe = json_txt.replace("</", "<\\/")
    tpl = open(os.path.join(ROOT, "app", "template.html"), encoding="utf-8").read()
    frag = tpl.replace("__DATA__", safe)
    with open(os.path.join(DIST, "artifact.html"), "w", encoding="utf-8") as f:
        f.write(frag)
    # standalone document: split <title> + <meta> + <link> head parts from the fragment
    head_end = frag.index("</style>") + len("</style>")
    head, body = frag[:head_end], frag[head_end:]
    full = "<!doctype html>\n<html lang=\"zh-Hant\">\n<head>\n<meta charset=\"utf-8\">\n" + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    with open(os.path.join(DIST, "jam-m1-drill.html"), "w", encoding="utf-8") as f:
        f.write(full)
    import export_md; export_md.main()
    print(f"built {len(items)} items, {len(terms)} glossary terms, {len(sheets)} cheat sheets -> dist/ (artifact.html {len(frag)//1024} KiB, jam-m1-drill.html {len(full)//1024} KiB)")
    ans = [0,0,0,0]
    for i in items: ans[i["answer"]] += 1
    print("answer positions after shuffle:", ans)
    for w in warnings: print("WARN:", w)

if __name__ == "__main__":
    main()
