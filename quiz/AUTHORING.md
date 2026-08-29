# JAM M1 Drill — item authoring guide (for drafting agents)

You are writing multiple-choice items for a JAM (Gray Paper **0.8.0**) interview-prep drill used by the New-JAMneration team
(Go implementation, currently on GP 0.7.2). The interview is an oral exam on GP chapters 3–13 + appendices, with extra
portions on architecture, design rationale and the PVM. Items must be **correct against GP 0.8.0** — the LaTeX source is the
ground truth: `../gp-src/text/*.tex` (chapters: notation, overview, header, safrole, recent_history,
authorization, accounts, judgments, reporting_assurance, accumulation, statistics, work_packages_and_reports; appendices:
pvm, pvm_invocations, serialization, merklization (D + E), utilities (F shuffle), bandersnatch (G), erasure_coding (H),
definitions (constants)). Read the relevant .tex BEFORE writing; quote it in explanations.

Supporting research (read the parts relevant to your chapter):
- `../research/code-map.md` — the team's Go code mapped to GP chapters with verbatim excerpts (use for `code` items;
  you may also open files under `../team-repo/` directly to quote real code).
- `../research/issues-digest.md` — bugs/gotchas the team hit (great sources of tricky items).
- `../research/ecosystem-notes.md` — JAM Prize, JIPs, test vectors tiny/full constants, 0.8.0 changelog, rationale.

## Output format

Write a Python module `items/<name>.py` containing `ITEMS = [ {...}, ... ]`. Each item:

```python
{
 "id": "ch11-guarantee-slot-window",          # unique, kebab-case, prefixed by chapter (ch04.., appA.., appB.., appC.., arch-)
 "ch": "11",                                  # one of: "3".."14", "A","B","C","D","E","F","G","H", "ARCH"
 "section": "11.4 Work Report Guarantees",    # human-readable section title as in the PDF
 "gpRef": "eq. 11.28",                        # equation numbers (verify with scripts/eqref.py) or §-references; never invent numbers
 "difficulty": 2,                             # 1 basic recall, 2 applied, 3 subtle/edge case
 "kind": "concept",                           # concept | code | calc | delta | rationale
 "tags": ["guarantees", "rotation"],          # add "delta-0.8.0" for anything that changed 0.7.2 → 0.8.0
 "stem": "English question text (interview-realistic; may use GP notation like κ′, ρ‡, E_G).",
 "code": {"lang": "go", "caption": "internal/…/file.go (FuncName)", "src": "verbatim code…"},   # only for kind=code (optional otherwise)
 "options": ["A…", "B…", "C…", "D…"],          # exactly 4, mutually exclusive, ONE correct; distractors plausible & wrong
 "answer": 0,                                 # index of the correct option (any position is fine; options get shuffled)
 "explanation": "繁體中文詳解，逐項說明正解為何對、每個干擾為何錯；引用 GP 原文/公式；技術名詞保留英文。",
 "trap": "（optional）一句話點出面試陷阱/記憶口訣。"
}
```

## Quality rubric (jabiko-style; machine-checked parts marked ⚙)

1. **唯一正解** — put every distractor back into the stem and ask "could an examiner accept this?" If yes, fix it. Distractors
   must be wrong for a *substantive* reason (wrong set/prior-vs-posterior, wrong constant, wrong threshold, reversed direction,
   mixing 0.7.2 with 0.8.0…), not by being absurd.
2. **Version discipline** — GP 0.8.0 is the target. When 0.7.2 differs, say so in the explanation and tag `delta-0.8.0`.
3. **No leaks** — ⚙ the correct option's text must not appear verbatim in the stem. Don't make the correct option the only long one.
4. **No letters** — ⚙ never refer to options as A/B/C/D in explanation/trap (options are shuffled). Refer to their content.
5. **Explanation** — ≥ 80 chars (⚙), 繁中, cites the GP (section/equation), explains why each distractor is wrong, and, where
   relevant, links to the team's code (file/function) or a fuzzer bug from the issues digest.
6. **Code items** — quote real code (from code-map.md or the repo); the question should test understanding of the GP rule the
   code implements, or a 0.7.2→0.8.0 gap in it, or an edge case. Keep excerpts ≤ ~25 lines.
7. **Oral-interview test (overrides everything below)** — the M1 examination is a *spoken* exam in front of Gray Paper
   editors and Fellowship members, not a written paper. Before keeping an item, ask: *could a candidate answer this out
   loud, and would an examiner actually ask it?* Good: "why is it done this way", "what breaks if you skip it", "which
   set / prior or posterior", "walk me through what happens when…". Bad: recall a byte offset or a hex discriminant,
   recite an opcode or host-call index table, compute a threshold balance to the octet. Where a numeric rule matters
   (the 34 + |k| + |v| storage charge, the ⌊2|k|/3⌋+1 verdict threshold), ask for the **rule and its reason**, not for
   the arithmetic. `kind: "calc"` is reserved for the rare case where doing the sum *is* the understanding; prefer
   `concept`, `rationale` or `delta`.
8. **Notation** — use the GP's symbols (η′_2, γ′_S, ρ‡, δ‡, E_G, W_G, Ψ_A …). Primes as ′, subscripts as _x, ⌊⌋ ⌈⌉ as unicode.
9. **Per-option notes** — every item carries `optNotes`: four strings, one per option **in source order** (the build
   permutes them with the options). The note for the key gives the discriminating fact; each distractor's note names its
   specific defect. One sentence each, parallel in length, 繁中, never referring to options by letter. Keep the general
   reasoning (rule, GP quote, cross-cutting insight) in `explanation` — it renders first, above the per-option list.
10. **Format** — ⚙ exactly 4 distinct options; fields as above; run `python3 scripts/validate.py` from the `quiz/` directory and
   fix every ERROR before finishing.
11. **Do not duplicate** existing items: read the existing `items/*.py` stems for your chapter first.
