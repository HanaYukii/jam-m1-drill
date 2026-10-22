# JAM M1 Drill

Interview-prep drill for the **JAM Prize Milestone 1 examination interview**, built for the
[New-JAMneration](https://github.com/New-JAMneration/JAM-Protocol) team.

- **383 multiple-choice questions** over Gray Paper **0.8.0** — chapters 3–14, appendices A–H,
  plus architecture / design-rationale / off-chain-protocol items.
- **92-entry glossary** of GP 0.8.0 symbols and terms (state components, data structures, PVM,
  cryptography, constants, ecosystem), searchable and cross-linked.
- Explanations in Traditional Chinese with English protocol terms, each citing the section or
  equation it comes from. Questions stick to GP 0.8.0 as written — version-to-version differences are kept
  out of the question bank and live only in the cheat sheets. Every answered question shows
  the same breakdown whether you got it right or wrong: the general reasoning first, then a
  per-option verdict saying why each of the four options is right or wrong.
- Questions are written for an **oral** examination: they ask for rules, reasons and consequences rather
  than byte offsets, opcode tables or arithmetic to the octet.
- Study modes: **practice** (instant feedback), **Q&A** (read straight through — question, then tap
  for the model answer and explanation, no options to pick), **cheat sheet** (21 condensed pages — one per
  chapter and appendix: flow, constants, key equations, the questions examiners keep asking, and the
  0.7.2→0.8.0 deltas),
  **mock exam** (interview weighting: two random chapters + architecture + appendices), a
  Leitner-style wrong-answer box, and a **reference page** (新舊對照: Polkadot 1.0 → 2.0 → JAM design
  comparison, every row tagged with its source; open it directly with `#evo`).

Also shipped as a printable handout: **[`jam-m1-qa.md`](jam-m1-qa.md)** — all 21 cheat sheets, then every
question with its model answer, explanation and GP reference, then the full glossary, in one
read-through file. The
Q&A mode's **列印 / 存 PDF** button prints the same thing (answers expanded, chrome hidden) straight
from the browser.

Everything is one self-contained `index.html` — no build step, no backend. Progress lives in the
visitor's own browser (`localStorage`).

For focused chapter 12 practice, select **12 Accumulation** and search **第12章專練** (or
`ch12-study`). These 24 short, bilingual questions cover notation, report dependencies, gas rounds,
partial-state timing, deferred transfers and privilege merging. Use practice mode for instant
per-option feedback, or Q&A mode to rehearse an answer before revealing it.

For chapter-by-chapter notation and function practice, search **符號函式專練** (or
`notation-functions`) and select a chapter. This adds two bilingual questions to each of the other
19 chapters/appendices (§3–11, §13–14 and A–H), with six relevant questions from the chapter 12 set
included in the same filter. The focus is each symbol's role, function inputs/outputs, and state timing.

## Deploy

Live at **https://hanayukii.github.io/jam-m1-drill/** — GitHub Pages serves `main` at `/ (root)`,
so any commit to `main` republishes it (**Settings → Pages → Deploy from a branch → main / (root)**).

Any static host works just as well:

```bash
npx wrangler pages deploy . --project-name jam-m1-drill   # Cloudflare Pages
python3 -m http.server 8080                               # local
```

## Content pipeline

The page is generated from typed question data:

```
items/*.py            # questions, one module per chapter group
glossary/*.py         # glossary terms
pages/*.py            # long-form reference pages (the 新舊對照 tab); schema-checked at build
scripts/validate.py   # content gate: schema, 4 distinct options, no answer leaks,
                      #   no letter references (options are shuffled at build and at render)
scripts/check_refs.py # every "eq. X.Y" must exist in that chapter of the Gray Paper
scripts/build.py      # -> dist/questions.json, dist/jam-m1-drill.html
scripts/smoke.mjs     # headless Chromium pass over both themes and both layouts
```

`REVIEW.md` records the earlier adversarial review. Newly added drills are checked against the
pinned Gray Paper source and the content gates; they are not covered by that historical blind review.

## Accuracy

Content is checked against the Gray Paper 0.8.0 source, not recalled from memory. Where the paper
itself is ambiguous, the explanation says so. If you find a mistake, please open an issue — a drill
that teaches a wrong rule is worse than no drill.
