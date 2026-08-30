#!/usr/bin/env python3
"""Build the JAM M1 Drill: items/*.py -> dist/questions.json, dist/artifact.html (fragment), dist/jam-m1-drill.html (standalone)."""
import json, os, sys, random, datetime, re
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

GREEK_SYM = "αβγδεζηθικλμνξοπρστυφχψωϱϖΓΔΘΛΞΠΣΦΨΩ"
BB_SYM    = "𝔹𝕊𝕍𝕐𝔻𝔼ℙℝℂℍℕℤ𝕁𝔾𝕏𝕌"
_SYM_TOKEN = re.compile(
    "^(?:[" + GREEK_SYM + "][\u2032\u2021\u2020]?(?:_[A-Za-z0-9]+)?"
    "|[" + BB_SYM + "]"
    "|[A-Z]_[A-Za-z0-9]+)$")

# Symbols the stems use that have no standalone glossary entry. Kept out of
# glossary/*.py on purpose: the 92-term list is a reader-facing feature with
# its own shape, and these are one-line hover glosses, not entries.
SYM_ALIASES = {
    "E_T": "tickets extrinsic：本塊提交的 Safrole ticket（每塊至多 K = 16 張）。",
    "E_D": "disputes extrinsic：verdicts、culprits、faults 三部分。",
    "E_P": "preimages extrinsic：本塊要併入 δ 的 preimage blob。",
    "E_A": "assurances extrinsic：validator 宣告持有哪些 core 的 shard。",
    "E_G": "guarantees extrinsic：本塊帶進來的 work-report 與其擔保簽章。",
    "E_C": "culprits：disputes 中被證明擔保了 bad report 的 validator。",
    "E_F": "faults：disputes 中被證明投了與最終判決相反票的 validator。",
    "E_U": "E_U(H)：不含 H_S 的 header 編碼，也就是 seal 實際簽的訊息。",
    "H_T": "timeslot index：本塊的時槽編號；τ′ = H_T。",
    "H_t": "timeslot index：本塊的時槽編號；τ′ = H_T。",
    "H_I": "author index：出塊者在 posterior active set κ′ 裡的索引。",
    "H_A": "author 的 Bandersnatch key：H_A ≡ κ′[H_I]_b，只是等價式，不被序列化。",
    "H_P": "parent hash：父 header 編碼的 Blake2b。",
    "H_0": "zero hash：32 個 0 位元組，β_H 新項的 state root 佔位用。",
    "Delta_PLACEHOLDER": "",
    "\u0394": "accumulation 函數族：Δ+ 外層、Δ* 平行、Δ1 單一 service。",
    "\u03a9": "host call 函數族：Ω_R read、Ω_W write、Ω_A assign、Ω_K invoke…",
    "\u03a6": "blacklist filter：epoch 換屆時把 offender 的金鑰整筆歸零（不是移除）。",
    "\u039b": "historical lookup：在 (H_t − D … H_t) 視窗內查某 service 的 preimage。",
    "M_B": "well-balanced Merkle root：Appendix E 的 M_B，與定深的 M 不同。",
    "X_T": "ticket 的簽章 context 字串，與 seal / entropy 的 context 分開。",
    "Z_A": "dynamic jump alignment：Z_A = 2，動態跳躍目標必須對齊且落在 basic block 起點。",
    "\u2119": "work-package 集合 ℙ：⟨j, h, u, f, c, w⟩。",
    "N_L": "octet 序列長度的集合（§3.4），等同 N_{2^32}——是長度的集合，不是 blob 的集合。",
    "N_S": "service index 集合：u32，與時槽同寬但意義無關。",
    "N_n": "小於 n 的自然數（§3.4，嚴格小於，所以有 n 個元素）。",
    "B_x": "長度恰為 x 的 octet 序列（§3.7.4）；B 本身是任意長度。",
    "B_31": "31 octet 的 blob——state key 構造函數 C 的值域。",
    "B_96": "96 octet 的 blob——Bandersnatch 簽章的長度。",
    "\u03bd_X": "指令解碼出的 immediate 值（附錄 A，寬度由 skip 決定並做 sign extension）。",
    "E_V": "verdicts：disputes extrinsic 中的判決，每筆帶 ⌊2|k|/3⌋+1 個簽章。",
    "\u039e": "work-report 計算函數 Ξ：把 work-package 算成 work-report。",
}
SYM_ALIASES.pop("Delta_PLACEHOLDER", None)

def symbol_map(terms):
    """symbol -> one-line gloss, for the reader-facing tooltips.

    Only unambiguous symbols: Greek (with optional prime/dagger/subscript),
    blackboard bold, and subscripted Latin. A bare 'B' or 'E' is ordinary
    English and would match everywhere, so those glossary entries are skipped.
    """
    out = {}
    for t in terms:
        raw = (t.get("sym") or "").strip()
        if not raw:
            continue
        gloss = t["term"] + "（" + t["zh"] + "）：" + t["one"]
        for tok in re.split(r"\s*/\s*|\s+", raw):
            tok = tok.strip()
            if _SYM_TOKEN.match(tok):
                out.setdefault(tok, gloss)
    for k, v in SYM_ALIASES.items():
        out.setdefault(k, v)
    return out

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
        "symbols": symbol_map(terms),
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
