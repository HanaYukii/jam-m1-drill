# JAM M1 Drill

Interview-prep drill for the **JAM Prize Milestone 1 examination interview**, built for the
[New-JAMneration](https://github.com/New-JAMneration/JAM-Protocol) team.

- **267 multiple-choice questions** over Gray Paper **0.8.0** — chapters 3–13, appendices A–H,
  plus architecture / design-rationale / off-chain-protocol items.
- **92-entry glossary** of GP 0.8.0 symbols and terms (state components, data structures, PVM,
  cryptography, constants, ecosystem), searchable and cross-linked.
- Explanations in Traditional Chinese with English protocol terms, each citing the section or
  equation it comes from; 52 items are tagged **0.7.2 → 0.8.0** for the version delta.
- Study modes: **practice** (instant feedback), **Q&A** (read straight through — question, then tap
  for the model answer and explanation, no options to pick), **cheat sheet** (one condensed page per
  chapter: flow, constants, key equations, the questions examiners keep asking, 0.7.2→0.8.0 deltas),
  **mock exam** (interview weighting: two random chapters + architecture + appendices), and a
  Leitner-style wrong-answer box.

Also shipped as a printable handout: **[`jam-m1-qa.md`](jam-m1-qa.md)** — every question with its
model answer, explanation and GP reference, plus the full glossary, in one read-through file. The
Q&A mode's **列印 / 存 PDF** button prints the same thing (answers expanded, chrome hidden) straight
from the browser.

Everything is one self-contained `index.html` — no build step, no backend. Progress lives in the
visitor's own browser (`localStorage`).

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
scripts/validate.py   # content gate: schema, 4 distinct options, no answer leaks,
                      #   no letter references (options are shuffled at build and at render)
scripts/check_refs.py # every "eq. X.Y" must exist in that chapter of the Gray Paper
scripts/build.py      # -> dist/questions.json, dist/jam-m1-drill.html
scripts/smoke.mjs     # headless Chromium pass over both themes and both layouts
```

`REVIEW.md` records the adversarial review: every item was re-answered from the Gray Paper LaTeX
source by an independent checker that never saw the author's explanation.

## Accuracy

Content is checked against the Gray Paper 0.8.0 source, not recalled from memory. Where the paper
itself is ambiguous, the explanation says so. If you find a mistake, please open an issue — a drill
that teaches a wrong rule is worse than no drill.
