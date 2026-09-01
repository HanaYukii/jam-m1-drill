#!/usr/bin/env python3
"""contentGuard for the JAM M1 quiz bank (jabiko-style machine gate).
Usage: python3 validate.py            -> validates items/*.py, prints report, exit 1 on failure
"""
import importlib.util, glob, os, sys, re, collections, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITEMS_DIR = os.path.join(ROOT, "items")
CHAPTERS = {
    # 基礎套題：主題式，只考主幹（不是 GP 章節的鏡像）
    "N1": "JAM 是什麼", "N2": "區塊與狀態", "N3": "時間與出塊", "N4": "Core 與 Service",
    "N5": "一份工作的一生", "N6": "資料可得性與稽核", "N7": "PVM 與 gas",
    # M1 套題：對應 Gray Paper 章節
    "3": "Notation", "4": "Overview", "5": "The Header", "6": "Safrole", "7": "Recent History",
    "8": "Authorization", "9": "Service Accounts", "10": "Disputes", "11": "Reporting & Assurance",
    "12": "Accumulation", "13": "Statistics", "14": "Work Packages & Reports",
    "A": "PVM", "B": "Host Calls", "C": "Codec", "D": "State Merklization", "E": "General Merklization / MMR",
    "F": "Shuffling", "G": "Bandersnatch VRF", "H": "Erasure Coding", "ARCH": "Architecture & Rationale",
}
KINDS = {"concept", "code", "calc", "delta", "rationale"}
REQUIRED = ["id", "ch", "section", "gpRef", "difficulty", "kind", "tags", "stem", "options", "answer", "explanation"]
OPTIONAL = ["code", "trap", "optNotes", "alsoCh", "stemZh", "optionsZh"]


GLOSS_DIR = os.path.join(ROOT, "glossary")
GLOSS_CATS = {"state":"狀態與區塊", "block":"狀態與區塊", "flow":"流程與角色", "data":"資料結構",
              "pvm":"PVM 與 host call", "crypto":"密碼學", "codec":"編碼與 Merklization",
              "const":"常數", "offchain":"鏈下協定", "eco":"生態系與規則"}
GLOSS_REQ = ["sym","term","zh","cat","gpRef","one","body","rel"]

SHEET_DIR = os.path.join(ROOT, "cheat")
SHEET_REQ = ["ch", "title", "one", "flow", "consts", "eqs", "asked", "delta", "code"]

def load_sheets():
    sheets = []
    for path in sorted(glob.glob(os.path.join(SHEET_DIR, "*.py"))):
        spec = importlib.util.spec_from_file_location("sh_" + os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        sheets.extend(mod.SHEETS)
    return sheets

def validate_sheets(sheets):
    errors, seen = [], set()
    order = list(CHAPTERS)
    for sh in sheets:
        w = "sheet " + str(sh.get("ch"))
        for k in SHEET_REQ:
            if not sh.get(k): errors.append(f"{w}: missing {k}")
        if sh.get("ch") not in CHAPTERS: errors.append(f"{w}: unknown chapter")
        if sh.get("ch") in seen: errors.append(f"{w}: duplicate chapter")
        seen.add(sh.get("ch"))
        for k in ("consts", "eqs", "asked"):
            for row in sh.get(k, []):
                if not (isinstance(row, (list, tuple)) and len(row) == 2):
                    errors.append(f"{w}: {k} rows must be [label, text]")
    sheets.sort(key=lambda x: order.index(x["ch"]) if x["ch"] in order else 99)
    return errors

def load_terms():
    terms, srcs = [], {}
    for path in sorted(glob.glob(os.path.join(GLOSS_DIR, "*.py"))):
        spec = importlib.util.spec_from_file_location("gl_" + os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for t in mod.TERMS:
            terms.append(t); srcs[t.get("term")] = os.path.basename(path)
    return terms, srcs

def validate_terms(terms, srcs):
    errors = []
    seen = set()
    for t in terms:
        w = f"{srcs.get(t.get('term'))}:{t.get('term')}"
        for k in GLOSS_REQ:
            if k not in t: errors.append(f"{w}: missing {k}")
        if set(t.keys()) - set(GLOSS_REQ): errors.append(f"{w}: unknown fields {sorted(set(t.keys())-set(GLOSS_REQ))}")
        if t.get("cat") not in GLOSS_CATS: errors.append(f"{w}: bad cat {t.get('cat')}")
        if len(t.get("body","")) < 60: errors.append(f"{w}: body too short")
        if not re.search(r"[一-鿿]", t.get("body","")): errors.append(f"{w}: body has no Chinese")
        key = (t.get("term"), t.get("sym"))
        if key in seen: errors.append(f"{w}: duplicate term")
        seen.add(key)
    return errors

def load_items():
    items, srcs = [], {}
    for path in sorted(glob.glob(os.path.join(ITEMS_DIR, "*.py"))):
        spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for it in mod.ITEMS:
            items.append(it)
            srcs[it.get("id")] = os.path.basename(path)
    return items, srcs

def validate(items, srcs):
    errors, warnings = [], []
    ids = collections.Counter(i.get("id") for i in items)
    for i, n in ids.items():
        if n > 1:
            errors.append(f"duplicate id: {i}")
    for it in items:
        iid = it.get("id", "<no id>")
        where = f"{srcs.get(iid)}:{iid}"
        for k in REQUIRED:
            if k not in it:
                errors.append(f"{where}: missing field {k}")
        extra = set(it.keys()) - set(REQUIRED) - set(OPTIONAL)
        if extra:
            errors.append(f"{where}: unknown fields {sorted(extra)}")
        if it.get("ch") not in CHAPTERS:
            errors.append(f"{where}: bad chapter {it.get('ch')}")
        # optional Chinese rendering of the question itself (the interview is in English,
        # so this is a reading aid, not a replacement)
        if "optionsZh" in it:
            z = it["optionsZh"]
            if not (isinstance(z, (list, tuple)) and len(z) == 4):
                errors.append(f"{where}: optionsZh must be a list of exactly 4 strings")
            elif any(not isinstance(t, str) or len(t.strip()) < 10 for t in z):
                errors.append(f"{where}: optionsZh entry too short")
            elif len(set(z)) != 4:
                errors.append(f"{where}: optionsZh entries must be distinct")
            if "stemZh" not in it:
                errors.append(f"{where}: optionsZh without stemZh (translate both or neither)")
        if "stemZh" in it and "optionsZh" not in it:
            errors.append(f"{where}: stemZh without optionsZh (translate both or neither)")
        # cross-chapter items: keep one primary ch, list the others in alsoCh
        also = it.get("alsoCh")
        if also is not None:
            if not isinstance(also, (list, tuple)) or not also:
                errors.append(f"{where}: alsoCh must be a non-empty list of chapter keys")
            else:
                for c in also:
                    if c not in CHAPTERS:
                        errors.append(f"{where}: alsoCh has unknown chapter {c!r}")
                    if c == it.get("ch"):
                        errors.append(f"{where}: alsoCh repeats the primary chapter {c!r}")
                if len(set(also)) != len(also):
                    errors.append(f"{where}: alsoCh has duplicates")
        if it.get("kind") not in KINDS:
            errors.append(f"{where}: bad kind {it.get('kind')}")
        if it.get("difficulty") not in (1, 2, 3):
            errors.append(f"{where}: bad difficulty {it.get('difficulty')}")
        opts = it.get("options", [])
        if len(opts) != 4:
            errors.append(f"{where}: need exactly 4 options, got {len(opts)}")
        if len(set(o.strip() for o in opts)) != len(opts):
            errors.append(f"{where}: options not mutually distinct")
        ans = it.get("answer")
        if not isinstance(ans, int) or not (0 <= ans < len(opts)):
            errors.append(f"{where}: answer index out of range: {ans}")
        if not it.get("stem", "").strip():
            errors.append(f"{where}: empty stem")
        if len(it.get("explanation", "")) < 80:
            errors.append(f"{where}: explanation too short (<80 chars)")
        if not re.search(r"[一-鿿]", it.get("explanation", "")):
            warnings.append(f"{where}: explanation contains no Chinese (policy: 繁中詳解)")
        if it.get("kind") == "code" and not it.get("code"):
            errors.append(f"{where}: kind=code but no code block")
        if it.get("code"):
            c = it["code"]
            for k in ("lang", "src", "caption"):
                if k not in c:
                    errors.append(f"{where}: code block missing {k}")
        # leak check: full correct option text quoted verbatim in stem
        if opts and isinstance(ans, int) and 0 <= ans < len(opts):
            if opts[ans].strip().lower() in it.get("stem", "").lower():
                errors.append(f"{where}: correct option text appears verbatim in stem (leak)")
        # explanations must not refer to options by letter (options are shuffled at build and at render)
        if re.search(r"選項 ?[A-D]\b|[^A-Za-z_\d][A-D] (說|是|錯|分別|把)", it.get("explanation", "") + " " + it.get("trap", "")):
            errors.append(f"{where}: explanation refers to an option by letter (options are shuffled)")
        # per-option notes: 4 entries aligned with the pre-shuffle option order
        if "optNotes" in it:
            n = it["optNotes"]
            if not (isinstance(n, (list, tuple)) and len(n) == 4):
                errors.append(f"{where}: optNotes must be a list of exactly 4 strings")
            else:
                for j, t in enumerate(n):
                    if not isinstance(t, str) or len(t.strip()) < 10:
                        errors.append(f"{where}: optNotes[{j}] too short")
                    if re.search(r"選項 ?[A-D]\b", t or ""):
                        errors.append(f"{where}: optNotes[{j}] refers to an option by letter")
        # length tell: a student must not be able to score by picking the longest (or shortest) option
        if opts and isinstance(ans, int) and 0 <= ans < len(opts) and len(opts) == 4:
            k = len(opts[ans]); rest = [len(o) for i, o in enumerate(opts) if i != ans]
            if k > max(rest) and k / max(rest) >= 1.15:
                errors.append(f"{where}: correct option is conspicuously the longest ({k} vs {max(rest)}) — thicken the distractors")
            if k < min(rest) and k / min(rest) <= 0.87:
                errors.append(f"{where}: correct option is conspicuously the shortest ({k} vs {min(rest)}) — level the options")
        # "all of the above"-style options are discouraged
        for o in opts:
            if re.search(r"all of the above|none of the above", o, re.I):
                warnings.append(f"{where}: avoid 'all/none of the above' options")
        if not it.get("tags"):
            warnings.append(f"{where}: no tags")
        if not it.get("gpRef"):
            warnings.append(f"{where}: no gpRef")
    missing = [i["id"] for i in items if "optNotes" not in i]
    if missing:
        warnings.append(f"{len(missing)} item(s) without optNotes (first: {missing[0]})")
    return errors, warnings

def report(items):
    by_ch = collections.Counter(i["ch"] for i in items)
    by_kind = collections.Counter(i["kind"] for i in items)
    by_diff = collections.Counter(i["difficulty"] for i in items)
    by_ans = collections.Counter(i["answer"] for i in items)
    delta = sum(1 for i in items if "delta-0.8.0" in i.get("tags", []))
    print(f"items: {len(items)}")
    print("by chapter:", ", ".join(f"{k}={by_ch[k]}" for k in CHAPTERS if by_ch[k]))
    print("by kind:", dict(by_kind))
    print("by difficulty:", dict(by_diff))
    print("answer position (pre-shuffle):", dict(by_ans))
    print("delta-0.8.0 tagged:", delta)

if __name__ == "__main__":
    items, srcs = load_items()
    terms, tsrcs = load_terms()
    errors_g = validate_terms(terms, tsrcs)
    errors, warnings = validate(items, srcs)
    report(items)
    print("glossary terms:", len(terms), dict(collections.Counter(t["cat"] for t in terms)))
    errors += errors_g
    for w in warnings:
        print("WARN:", w)
    for e in errors:
        print("ERROR:", e)
    if errors:
        print(f"\n{len(errors)} error(s)")
        sys.exit(1)
    print("\ncontentGuard: OK")
