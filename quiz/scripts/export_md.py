#!/usr/bin/env python3
"""Export the bank as a read-through Q&A handout: dist/jam-m1-qa.md"""
import os, sys, datetime, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate import load_items, load_terms, load_sheets, validate_sheets, CHAPTERS, GLOSS_CATS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOTS = {1: "●○○", 2: "●●○", 3: "●●●"}
KIND_ZH = {"concept": "概念", "code": "程式碼", "calc": "計算", "delta": "版本差異", "rationale": "設計理由"}

def chlabel(k):
    n = CHAPTERS[k]
    if k == "ARCH": return "★ Architecture & Rationale"
    if k.isdigit(): return f"§{k} {n}"
    return f"附錄 {k} · {n}"

def main():
    items, _ = load_items()
    terms, _ = load_terms()
    sheets = load_sheets(); validate_sheets(sheets)
    by_ch = collections.OrderedDict((k, []) for k in CHAPTERS)
    for it in items: by_ch[it["ch"]].append(it)

    L = []
    L.append("# JAM M1 Drill — 問答講義\n")
    L.append(f"Gray Paper **0.8.0** · {len(sheets)} 章速記 · {len(items)} 題 · {len(terms)} 條名詞解釋 · New-JAMneration M1 面試準備  ")
    L.append(f"線上互動版：<https://hanayukii.github.io/jam-m1-drill/> · 匯出於 {datetime.date.today().isoformat()}\n")
    L.append("> 讀法：先把題目自己講一遍（口試考的是講得出來，不是認得出來），再看標準答案與詳解。\n")
    L.append("## 目錄\n")
    L.append("- [速記（考前濃縮）](#cheat)")
    for k, lst in by_ch.items():
        if lst: L.append(f"- [{chlabel(k)}](#{('ch-' + k.lower())}) — {len(lst)} 題")
    L.append("- [名詞解釋](#glossary)\n")

    L.append('\n<a id="cheat"></a>\n')
    L.append(f"# 速記　<sub>考前濃縮 · {len(sheets)} 章</sub>\n")
    for sh in sheets:
        L.append(f"## {chlabel(sh['ch'])}\n")
        L.append(sh["one"] + "\n")
        L.append("**流程**\n")
        for i, x in enumerate(sh["flow"], 1): L.append(f"{i}. {x}")
        L.append("\n**常數與門檻**\n")
        for a, b in sh["consts"]: L.append(f"- `{a}` — {b}")
        L.append("\n**核心公式**\n")
        for a, b in sh["eqs"]: L.append(f"- `{a}` — {b}")
        L.append("\n**最常被追問**\n")
        for q, a in sh["asked"]: L.append(f"- **{q}**  \n  {a}")
        L.append("\n**0.7.2 → 0.8.0**\n")
        for x in sh["delta"]: L.append(f"- {x}")
        L.append("\n**對應程式碼**\n")
        for x in sh["code"]: L.append(f"- {x}")
        L.append("\n---\n")
    L.append("\n# 題庫\n")

    for k, lst in by_ch.items():
        if not lst: continue
        L.append(f'\n<a id="ch-{k.lower()}"></a>\n')
        L.append(f"## {chlabel(k)}　<sub>{len(lst)} 題</sub>\n")
        for i, it in enumerate(lst, 1):
            meta = f"{DOTS.get(it['difficulty'],'')} · {KIND_ZH.get(it['kind'], it['kind'])} · {it['gpRef']}"
            if "delta-0.8.0" in it.get("tags", []): meta += " · ⚠ 0.7.2→0.8.0"
            L.append(f"### {k}-{i}　{it['stem']}\n")
            L.append(f"<sub>{it.get('section','')} — {meta}</sub>\n")
            c = it.get("code")
            if c:
                L.append(f"```{c.get('lang','')}\n{c['src'].rstrip()}\n```")
                if c.get("caption"): L.append(f"<sub>{c['caption']}</sub>\n")
            L.append(f"**標準答案**　{it['options'][it['answer']]}\n")
            L.append(it["explanation"] + "\n")
            if it.get("optNotes"):
                L.append("**逐項辨析**\n")
                for j, (o_, note) in enumerate(zip(it["options"], it["optNotes"]), 1):
                    mark = "✅" if j - 1 == it["answer"] else "❌"
                    L.append(f"{j}. {mark} {o_}  \n   {note}")
                L.append("")
            if it.get("trap"): L.append(f"> **陷阱**　{it['trap']}\n")
            L.append(f"<sub>`{it['id']}`</sub>\n")
            L.append("---\n")

    L.append('\n<a id="glossary"></a>\n')
    L.append(f"## 名詞解釋　<sub>{len(terms)} 條</sub>\n")
    seen = []
    for cat, label in GLOSS_CATS.items():
        if label in seen: continue
        seen.append(label)
        rows = [t for t in terms if GLOSS_CATS.get(t["cat"]) == label]
        if not rows: continue
        L.append(f"### {label}\n")
        for t in rows:
            L.append(f"**{t['sym']}**　{t['term']}（{t['zh']}）　<sub>{t['gpRef']}</sub>\n")
            L.append(f"{t['one']}\n")
            L.append(f"{t['body']}\n")
            if t.get("rel"): L.append(f"<sub>相關：{'、'.join(t['rel'])}</sub>\n")
    out = os.path.join(ROOT, "dist", "jam-m1-qa.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote dist/jam-m1-qa.md ({os.path.getsize(out)//1024} KiB, {len(items)} items, {len(terms)} terms)")

if __name__ == "__main__":
    main()
