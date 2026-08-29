# r1 — §12 Accumulation, adversarial review

Ground truth: `/root/work/jam/gp-src/text/accumulation.tex`, `preamble.tex` (0.8.0 symbol table),
`text/reporting_assurance.tex`, `text/recent_history.tex`, `text/accounts.tex`, `text/pvm_invocations.tex`,
`text/notation.tex`, `text/definitions.tex`. Equation numbers cross-checked with `scripts/eqref.py`.

Symbol table facts established up-front (preamble.tex):
- `\ready` = **ω** (l.789), `\accumulated` = **ξ** (l.786), `\lastaccout` = **θ** (l.790), `\authqueue` = **φ** (`\phi`, l.792),
  `\stagingset` = **ι**, `\privileges` = **χ** with χ_M/χ_A/χ_V/χ_R/χ_Z (l.779–784).
- `\justbecameavailable` = **R** (bold R, l.678)  ← 0.7.2 called this **W**.
- `\workreport` = **ℝ** (l.506); `\workitem` = **𝕎** (l.495)  ← in 0.7.x the work-*report* set was 𝕎.
- `\operandtuple` = **𝕌** (l.537), `\defxfer` = **𝕏** (l.588), `\workerror` = **𝔼** (l.357), `\partialstate` = **𝕊** (l.606).
- `\Creportaccgas` = **G_A** = 10,000,000; `\Cblockaccgas` = **G_T** = 3,500,000,000; `\Cepochlen` = E = 600; C = 341.
- `\sa¬minaccgas` = a_g, `\sa¬minmemogas` = a_m; `\fnmmrappend` = 𝒜, `\fnmerklizewb` = ℳ_B, `\fnmmrsuperpeak` = ℳ_R.

---

## PHASE 1 — blind verdicts

### n=1 — `c3-ch12-omega-xi-theta-naming`
- **Believed correct: index 0** — "ω ∈ ⟦⟦(W, {H})⟧⟧_E is the ready (accumulation) queue … ξ … θ is the Accumulation Output Log".
- **Confidence: HIGH** (on the ω/ξ/θ mapping), but see the notation caveat below.
- Settling lines:
  - `preamble.tex:789` `\newcommand*{\ready}{\omega}`; `:786` `\accumulated}{\xi}`; `:790` `\lastaccout}{\theta}`.
  - eq. 12.1 `accumulation.tex:28` — `ξ ∈ ⟦{H}⟧_E` (`\sequence[\Cepochlen]{\protoset{\hash}}`).
  - eq. 12.3 `accumulation.tex:35` — `ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E` (`\sequence[\Cepochlen]{\sequence{\tuple{\workreport, \protoset{\hash}}}}`).
  - eq. 7.4 `recent_history.tex:18` — `θ ∈ ⟦(N_S, H)⟧` (`\lastaccout \in \sequence{\tup{\serviceid, \hash}}`).
  - ω′ is written by accumulation at eq. 12.33 (`accumulation.tex:426–430`); ξ′ at 12.31–12.32; θ′ at 12.25 (`:370`).
  - 0.7.2→0.8.0 rename ϑ→ω is corroborated by the team repo (`internal/types/state.go:18` `Vartheta ReadyQueue \`json:"theta"\``,
    state-key 14) and `research/code-map.md:76`.
- **CAVEAT (notation):** the option writes the ready-queue element type as `(W, {H})`. In GP 0.8.0 the work-report set is
  **ℝ**, and **𝕎 is the work-*item* set** (`preamble.tex:495,506`). `W` for work-report is a **0.7.x-era symbol**. The
  repo's own glossary already writes it correctly: `glossary/g1_state.py:70` — "ω ∈ [[(ℝ, {H})]]_E". This matters more than
  usual here because the item's whole subject is 0.7.2→0.8.0 symbol renaming.
- Distractors: idx1 (ω = output log, θ = gas usage) — contradicted by 12.3/7.4. idx2 ("ready queue is still spelled ϑ in
  0.8.0") — contradicted by `preamble.tex:789`. idx3 (ω = deferred transfers carried across a block boundary) — transfers
  never survive a block; Δ+ is seeded with `⟦⟧` at eq. 12.24 (`:369`) and `t` only lives inside the Δ+ recursion.

### n=2 — `c3-ch12-operand-tuple-fields`
- **Believed correct: index 0** — "The set is U (and deferred transfers are X, Ψ_A taking ⟦U ∪ X⟧). Each tuple mixes
  digest-level fields — y … g … l … — with fields lifted from its own report: p, e, a, t".
- **Confidence: HIGH**
- Settling lines: eq. 12.13 `accumulation.tex:107–117` gives 𝕌 = (p:H, e:H, a:H, y:H, g:G, t:B, l:B ∪ 𝔼); eq. 12.23
  `accumulation.tex:323–338` builds `i^U` with `l = d_l, g = d_g, y = d_y, t = r_t, e = (r_s)_e, p = (r_s)_p, a = r_a`
  for `r ↕ r, d ↕ r_d, d_s = s`. `accumulation.tex:128`: "the union of the two characterizes inputs to Ψ_A"; eq. 12.23
  `:311` `Ψ_A(e, τ′, s, g, i^T ⌢ i^U)`.
- Distractors: idx1 — 𝕌 has exactly 7 fields; c (code hash), d_u (gas used) and the import/xt/export counts of the
  work-digest (eq. 11.6) are **not** in it. idx2 — `i^U` is one entry per *digest*, not per report. idx3 — no core index or
  refinement context in 𝕌, and `l ∈ B ∪ 𝔼` means work-errors are explicitly *passed through*, not dropped.

### n=3 — `c3-ch12-E-removes-entries-too`
- **Believed correct: index 0** — "Q stops terminating … and at the block boundary ω′ … keeps reports that were just
  accumulated".
- **Confidence: HIGH**
- Settling lines: eq. 12.7 `accumulation.tex:53–60` — E maps `⟨r,d⟩ ↕ r` to `⟨r, d ∖ x⟩` **only when
  `(r_s)_p ∉ x`**; eq. 12.8 `:68–71` — `Q(r) = ⟦⟧ if g = ⟦⟧, else g ⌢ Q(E(r, P(g)))` where `g = ⟦r | ⟨r,∅⟩ ↕ r⟧`.
  Drop the entry-removal half and every element of `g` survives `E(r, P(g))` with `∅ ∖ P(g) = ∅`, so the next `g` is
  identical → non-termination. eq. 12.33 `:426–430` uses E in both the `i = 0` (`E(R^Q, ξ′[E−1])`) and `i ≥ τ′−τ`
  (`E(ω↺[m−i], ξ′[E−1])`) branches, with `ξ′[E−1] = P(R*[..n])` (eq. 12.31) — that is exactly the just-accumulated set.
- Distractors: idx1 — Q's recursion is not fed a shorter sequence by construction; termination *depends* on removal.
  idx2 — the §11.4 duplicate-package check (`reporting_assurance.tex`, eq. 11.30 ff.) filters *incoming* reports in E_G;
  it says nothing about re-accumulating an entry already sitting in ω. idx3 — word salad; dependency sets shrink via
  `d ∖ x` regardless.

### n=4 — `c3-ch12-starved-dependency-fate`
- **Believed correct: index 3** — "Q never emits it … carried forward by the i ≥ τ′ − τ case … vanishes at most one epoch
  later when the slot index wraps round".
- **Confidence: HIGH**
- Settling lines: eq. 12.8 (`:68–71`) — Q only ever emits entries whose dependency set is already `∅`. eq. 12.7 removes an
  entry only if **its own** package hash is in x; an unsatisfiable *dependency* is not a removal trigger. eq. 12.33
  `:426–430`: `ω′↺[m−i] = E(ω↺[m−i], ξ′[E−1])` for `i ≥ τ′−τ`, and the `i = 0` slot is overwritten with
  `E(R^Q, ξ′[E−1])`. Since `m = H_T mod E` (eq. 12.10, `:88`) the slot is reclaimed after at most E slots — matching
  `accumulation.tex:32` "Each of these were made available at most one epoch ago".
- Distractors: idx0 — misstates E (it removes on the *entry's own* package hash, not on a dangling dependency).
  idx1 — `accumulation.tex:25` does say accumulation "is cancelled entirely in the case of an invalid dependency", but
  nothing in the GP turns that into block rejection, and a never-guaranteed prerequisite is not an *invalid* dependency.
  idx2 — no expiry-then-accumulate rule exists anywhere in §12.

### n=5 — `c3-ch12-gas-floor-vs-ceiling`
- **Believed correct: index 0**
- **Confidence: HIGH**
- Settling lines:
  - §11.4 `reporting_assurance.tex:329–334`: "We require that the gas allotted for accumulation of each work-digest …
    respects its service's minimum gas requirements … no greater than the overall gas limit G_A":
    `∀w ∈ I : Σ_{d ∈ w_d}(d_g) ≤ G_A ∧ ∀d ∈ w_d : d_g ≥ δ[d_s]_g` — note **δ**, the prior accounts (`preamble.tex:819`).
  - Block budget: `accumulation.tex:350–352` `g = max(G_T, G_A·C + Σ_{x ∈ values(χ_Z)}(x))`, fed to Δ+ at eq. 12.24.
  - `transfer` host call `pvm_invocations.tex:884`: `⟨LOW, 0⟩ otherwise if l < d[d_d]_m`.
  - `accounts.tex:56`: "a_g is the minimum gas required per work-item, while a_m is the minimum gas required per
    deferred-transfer"; Δ1's gas `g` (eq. 12.23, `:315–317`) sums f[s], the transfers' t_g and the digests' d_g.
- Distractors: idx1 — no gas refund rule exists. idx2 — the `new` host call (`pvm_invocations.tex:806–845`) imposes no
  `a_g ≤ G_A` invariant. idx3 — swaps a_g/a_m *and* swaps G_A/G_T.

### n=6 — `c3-ch12-theta-from-yield`
- **Believed correct: index 2**
- **Confidence: HIGH**
- Settling lines: eq. 12.18 `accumulation.tex:201–207` — `b = {⟨s, b⟩ | s ∈ s, b = Δ1(s)_y, b ≠ ∅}` with
  `s = {d_s | r ∈ r, d ∈ r_d} ∪ K(f) ∪ {t_d | t ∈ t}` (`:190–194`) — so a transfer-only destination **is** in `s` and may
  yield. eq. 12.25 `:370` `θ′ ≡ ⟦⟨s,h⟩ ∈ b⟧`. Gas-burning-without-yield shows up only in `u` (eq. 12.18 `:196–200`) and
  hence in G(s) of eq. 12.28. Consumption: `recent_history.tex:30–32`,
  `s = ⟦E_4(s) ⌢ E(h) | ⟨s,h⟩ ↕ θ′⟧`, `β′_B ≡ 𝒜(β_B, ℳ_B(s, H_K), H_K)` (eq. 7.7), and `recent_history.tex:42`
  stores `b = ℳ_R(β′_B)` in the new β_H item (eq. 7.8).
- Distractors: idx0 — b has no zero-hash padding; the `b ≠ ∅` filter is explicit. idx1 — θ′ is *this block's* sequence and
  is replaced wholesale; β_B is the since-genesis MMB, not a cache of θ′. idx3 — directly contradicted by the `{t_d}` term
  in `s`.

### n=7 — `c3-ch12-provide-two-places`
- **Believed correct: index 0**
- **Confidence: HIGH**
- Settling lines: eq. 12.18 `accumulation.tex:213–216` — `e_d′ = I((e_d ∪ n) ∖ m, ⋃_{s ∈ s} Δ1(s)_p)` (n = new services,
  m = removed, `:246–255`). eq. 12.37 `:452` — `δ′ = I(δ‡, E_P)`. eq. 12.21 `:278–284` —
  `Y(d, s, i) = (d[s]_l[(H(i), |i|)] = ⟦⟧)` when `s ∈ K(d)`, else `⊥`. `accumulation.tex:268`: "Preimage provisions into
  services which no longer exist or whose relevant request is dropped are disregarded"; `:450` "We disregard, without
  prejudice, any preimages which due to the effects of accumulation are no longer useful."
- Distractors: idx1 — `provide` does *not* write a_p/a_l directly; the integration in eq. 12.18 is what does it.
  idx2 — Y has no size test; W_C = 4,000,000 is the max *service code* size (`definitions.tex:286`), and failures are
  disregarded, never block-invalidating. idx3 — I is applied inside Δ*, not Δ1, and Y accepts **only** `⟦⟧`.

### n=8 — `c3-ch12-code-accumulation-statistics`
- **Believed correct: index 1** — the missing T(s) / three-tuple / Δ+ fifth component / `≠ (0,0,0)` filter.
- **Confidence: HIGH**
- Settling lines: eq. 12.27 `accumulation.tex:388` `S ∈ ⟨N_S → (N, N, N_G)⟩`; eq. 12.28 `:390–410`
  `S ≡ {s ↦ S(s) | S(s) ≠ ⟨0,0,0⟩}`, `S(s) ≡ ⟨N(s), T(s), G(s)⟩`,
  `T(s) ≡ |⟦t | t ↕ **t**, t_d = s⟧|`; eq. 12.17 `:155,159` — Δ+ returns
  `⟨N, 𝕊, B, U, ⟦X⟧⟩` / `⟨i+j, e′, b* ∪ b, u* ⌢ u, t ⌢ t†⟩`, five components, the fifth bound to **t** at eq. 12.24
  (`:368`). Corroborated by the 0.8.0 changelog entry #502 "Add back processed transfer count to service statistics"
  (`research/ecosystem-notes.md:~610`).
- Distractors: idx0 — N(s) counts *digests* (`d ↕ r_d`), not reports; the shown code is right about that. idx2 — G(s) is
  `Σ_{⟨s,u⟩ ∈ u}(u)`, actual gas used. idx3 — the `≠ ⟨0,0,0⟩` filter is explicit; the key set is deliberately sparse.

### n=9 — `c3-ch12-why-R-star-is-a-sequence`
- **Believed correct: index 0**
- **Confidence: HIGH**
- Settling lines: eq. 12.17 `:162–163` — `i = max(N_{|r|+1})` s.t. the gas prefix sum fits; eq. 12.31 `:424`
  `ξ′[E−1] = P(R*[..n])`; eq. 11.17 `reporting_assurance.tex:183–188` —
  `R ≡ ⟦(ρ†[c]_g)_w | c ↕ N_C, Σ_{a ∈ E_A} a_f[c] > 2/3·|κ|⟧` (ascending core index over **ρ†**, strict `> 2/3|κ|`);
  eq. 12.4 `:40` R^! preserves `r ↕ R`; eq. 12.11 `:89` `R* ≡ R^! ⌢ Q(q)`.
- Distractors: idx1 — the GP makes no permutation-invariance claim; the prefix cut alone refutes it. idx2 — the prefix cut
  changes δ† too, not just S/π_S. idx3 — R is ordered by core index, not by assurance count.

### n=10 — `c3-ch12-accseq-n-with-transfers`
- **Believed correct: index 2**
- **Confidence: HIGH**
- Settling lines: eq. 12.17 `accumulation.tex:156–167` — base case fires `when n = 0` where
  `n = i + |t| + |f|` (`:164`); with `r = ⟦⟧`, `i = 0`, `|t| = 3`, `|f| = 0` ⇒ `n = 3 ≠ 0` ⇒ o/w branch. Δ* is invoked as
  `Δ*(e, t, r[..i], f)` (`:165`) and its service set (eq. 12.18 `:190–194`) is
  `{d_s | r ∈ r, d ∈ r_d} ∪ K(f) ∪ {t_d | t ∈ t}` = the transfer destinations. Output tuple `:159`
  `⟨i+j, e′, b* ∪ b, u* ⌢ u, t ⌢ t†⟩`, fifth component consumed by T(s) in eq. 12.28 (`:405–408`).
- Distractors: idx0 — misreads the termination test as `i = 0`. idx1 — Δ1 is invoked for every `s ∈ s`, including
  transfer-only destinations; balances are credited by Ψ_A on the `i^T` operands, not by the `transfer` host call in the
  earlier round. idx3 — 0.8.0's Δ+ is a **five**-tuple; balance-diffing is not in the GP.

### n=11 — `c3-ch12-prior-privileged-index-reads`
- **Believed correct: index 0**
- **Confidence: HIGH**
- Settling lines: eq. 12.18 `accumulation.tex:239–245` —
  `e_i′ = (Δ1(e_v)_e)_i` and `∀c ∈ N_C : e_q′[c] = ((Δ1(e_a[c])_e)_q)[c]`, where
  `⟨e_d, e_i, e_q, e_m, e_a, e_v, e_r, e_z⟩ = e` (`:217–219`) is the **prior** partial state. Contrast eq. 12.19 `:260–263`
  `R(o,a,b)`, which is used for χ′_A, χ′_V, χ′_R only.
- Distractors: idx1 — e* = Δ1(m)_e feeds χ′_M/χ′_Z and the `a` argument of R, not φ′/ι′. idx2 — posterior indices are
  never used as the selector. idx3 — φ′[c] is a single read, not an R-merge, and ι′ is not last-writer-wins.

### n=12 — `c3-ch12-code-delta-star-map-order`
- **Believed correct: index 1**
- **Confidence: HIGH**
- Settling lines: eq. 12.18 `accumulation.tex:196–212` — `u = ⟦⟨s, Δ1(s)_u⟩ | s ↕ s⟧` and `t′ = ⟦Δ1(s)_t | s ↕ s⟧` use
  `\orderedin`, whereas `b` (`:201–207`) uses plain `∈`. `notation.tex:123`: "when the ordering of elements matters we use
  ↕ rather than the unordered notation ∈ … This applies to any set which has an unambiguous ordering" — for `s ⊂ N_S`
  that is ascending service index. Δ* returns the flattened `⌢t′` (`:186`), which becomes `t*` and then the next round's
  `t` (eq. 12.17 `:165–166`), and Δ1 slices it order-sensitively into `i^T = ⟦t | t ↕ t, t_d = s⟧` (eq. 12.23 `:318–322`).
- Distractors: idx0 — `t′` is a *sequence* in the GP, and its order is observable through `i^T`. idx2 — report order is not
  what ↕ means over a set of service indices. idx3 — `s` explicitly includes `K(f)` and `{t_d}`.


---

## PHASE 2 — audit against `items/c3_ch12_accum.py`

**Key agreement: 12/12.** Every blind answer matched the key (`0,0,0,3,0,2,0,1,0,2,0,1`). **No MISMATCH.**
Findings below are defects in stems, gpRefs, explanations and traps, plus one cross-cutting item-bank issue.

---

### n=1 · `c3-ch12-omega-xi-theta-naming` — **DELTA-DEFECT + EXPLANATION-DEFECT**

**(a) Stale 0.7.x symbol `W` for the work-report set, in both the keyed option and the explanation.**
GP 0.8.0 `preamble.tex:506` `\newcommand*{\workreport}{\mathbb{R}}` and `:495` `\newcommand*{\workitem}{\mathbb{W}}`.
So eq. 12.3 reads **ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E**, and `W` in 0.8.0 denotes the **work-item** set, not the work-report set.
This is precisely the class of error the item exists to prevent, and the repo's own glossary already has it right
(`glossary/g1_state.py:70`: "ω ∈ [[(ℝ, {H})]]_E"). (`items/ch12_ch13.py` has the same slip in an option while its own
explanation writes `(R, {H})` — outside this batch, but worth the caller's attention.)

- In the option (line 23) replace
  `ω ∈ ⟦⟦(W, {H})⟧⟧_E is the ready`
  with
  `ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E is the ready`
- In the explanation (line 38) replace
  `ω ∈ ⟦⟦(W, {H})⟧⟧_E（每個 slot`
  with
  `ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E（ℝ 是 0.8.0 的 work-report 集合，0.7.2 記作 W；每個 slot`

**(b) The trap asserts the rename was the *only* 0.7.2→0.8.0 change here — it was not.**
`research/code-map.md:24,236,296,2118` shows 0.7.2 spelled the just-became-available sequence and its derivatives
**W!, W_Q, W\***; GP 0.8.0 `preamble.tex:678` makes it `\justbecameavailable = \mathbf{R}` (R!, R^Q, R*). A candidate who
memorises "只是 ϑ→ω 的更名" will mis-name half of §12 in an oral exam.

- Line 45, replace
  `0.7.2→0.8.0 只是 ϑ→ω 的更名，state key 與型別都沒動`
  with
  `0.7.2→0.8.0 ready queue 是 ϑ→ω 的更名，state key C(14) 與型別結構都沒動；同章的 W!/W_Q/W* 也一併改成 R!/R^Q/R*`

**(c) Wrong section reference: `§4.1 state σ`.** σ's composition (eq. 4.4, `\thestate ≡ ⟨α, β, θ, γ, δ, η, ι, κ, λ, ρ, τ,
φ, χ, ψ, π, ω, ξ⟩`) is in **§4.2 "The State"** (`overview.tex:30,34`). **§4.1 is "The Block"** (`overview.tex:12`).

- Line 16, replace `eq. 7.4 (θ); §4.1 state σ` with `eq. 7.4 (θ); §4.2 state σ`
- Line 43, replace `§4.1 的 σ 組成不符` with `§4.2 的 σ 組成不符`

**(d) Unsourced rationale over-claim.** "0.8.0 改成 ω **正是為了**消掉 ϑ/θ … 符號衝突" states a motive. Neither the GP
0.8.0 source nor the 0.8.0 release notes (`research/ecosystem-notes.md:~605–620`, which do not mention the rename at all)
say why. Plausible ≠ sourced.

- Line 41, replace
  `0.8.0 改成 ω 正是為了消掉 ϑ/θ 這組幾乎無法辨識的符號衝突；`
  with
  `0.8.0 改成 ω（GP 與 0.8.0 release notes 都沒有說明改名理由，別在口試時把「為了避開 ϑ/θ 混淆」講成 GP 的說法）；`

**(e) Nit — stem over-counts.** "Three state items in σ are written to by accumulation" is false as read: §12 also
produces δ′ (via δ†/δ‡), χ′, ι′, φ′ and **S** → π (`accumulation.tex:13`, eq. 12.26–12.28). Answerability is unaffected.

- Line 20, replace
  `Three state items in σ are written to by accumulation: ω, ξ and θ.`
  with
  `Among the state items in σ written by accumulation are ω, ξ and θ.`

*(Verified-correct in this item: preamble mapping; ξ/ω/θ types; state keys — `merklization.tex:70,81,84` gives
C(14)→ω, C(15)→ξ, C(16)→θ, and the 0.7.2 client uses the same indices (`team-repo/internal/types/state.go:104`),
so "state key 不變" is right; ϑ→ω really is a 0.7.2→0.8.0 change, since there was no release between them.)*

---

### n=2 · `c3-ch12-operand-tuple-fields` — **EXPLANATION-DEFECT (minor)**

The claim "code hash c、refine 實際用掉的 gas、import/extrinsic/export 計數都留在 digest 裡**供 §13 統計用**" is right for
the five activity fields but **wrong for the code hash**. `statistics.tex:189–193` consumes exactly
`d_u, d_i, d_x, d_z, d_e`; the digest's `c` is never used there. `c` exists for §11.4's eq. 11.45 check
`d_c = δ[d_s]_c` (`reporting_assurance.tex:~438`).

- Line 80, replace
  `export 計數都留在 digest 裡供 §13 統計用，不會進 accumulate。`
  with
  `export 計數都只留在 digest 裡（後四項連同 d_u 餵 §13 的 core statistics，見 statistics.tex 的 d_u/d_i/d_x/d_z/d_e；code hash c 則是給 §11.4 的 d_c = δ[d_s]_c 檢查用），不會進 accumulate。`

*(Everything else verified: eq. 12.13's seven fields; eq. 12.14 X ≡ (s, d, a, m, g); "eq. B.9" for Ψ_A is correct —
`scripts/eqref.py accinvocation` → `B.9 eq:accinvocation`; 𝔼's members at eq. 11.7 include ∞, ☇, BAD, BIG.)*

---

### n=3 · `c3-ch12-E-removes-entries-too` — **EXPLANATION-DEFECT**

"eq. 12.33 的**三個 case 全都**靠 E(·, ξ′[E−1]) 清掉本區塊已完成的項目" is **false**. Only two of the three use E:
`accumulation.tex:426–430` — `i = 0` → `E(R^Q, ξ′[E−1])`; **`1 ≤ i < τ′ − τ` → `⟦⟧`** (no E at all);
`i ≥ τ′ − τ` → `E(ω↺[m−i], ξ′[E−1])`. The keyed option itself correctly names only two, and item n=4's explanation
enumerates the three cases correctly — so this file contradicts itself.

- Line 116, replace
  `而 eq. 12.33 的三個 case 全都靠 E(·, ξ′[E−1]) 清掉`
  with
  `而 eq. 12.33 三個 case 中的兩個（i = 0 與 i ≥ τ′ − τ）靠 E(·, ξ′[E−1]) 清掉`
- Line 117, replace
  `本區塊已完成的項目。說「Q`
  with
  `本區塊已完成的項目（中間的 1 ≤ i < τ′ − τ 是直接清成 ⟦⟧，不套用 E）。說「Q`

*(Verified-correct: eq. 12.7's two jobs; the Q non-termination argument; and the §11.4 duplicate-package check really does
compare against β_H, ξ, ω and ρ — `reporting_assurance.tex:~384–400`, `q` drawn from `⌢ω` and `a` from ρ.)*

---

### n=4 · `c3-ch12-starved-dependency-fate` — **AMBIGUOUS (impossible stem premise) + EXPLANATION-DEFECT**

**(a) The stem posits a state GP §11.4 forbids.** "package p … was never even guaranteed" cannot coexist with w sitting
in ω: contextual validity (`reporting_assurance.tex:~403–412`) requires
`∀w ∈ I, ∀p ∈ (w_c)_p ∪ K(w_l) : p ∈ I_packagehashes ∪ {x | x ∈ K(b_p), b ∈ β_H}` — every prerequisite must already be in
this extrinsic or in the recent-history reported packages, i.e. **already guaranteed**. A sharp examiner will call this
out. The realistic starvation case (and the one the GP's own note at the end of §11.4 addresses — "the reports are simply
ignored") is a prerequisite that *was* guaranteed and then timed out or was disputed. The keyed answer is unaffected.

- Replace lines 131–132
  ```
      "stem": "A report w is sitting in ω with one outstanding dependency p, and package p is never accumulated — it was "
              "never even guaranteed. Trace w's fate under GP 0.8.0.",
  ```
  with
  ```
      "stem": "A report w is sitting in ω with one outstanding dependency p, and package p is never accumulated — the "
              "report carrying p was guaranteed a few blocks ago but timed out on its core and never became available. "
              "Trace w's fate under GP 0.8.0.",
  ```

**(b) "區塊有效性條件在 §11 而不在 §12" is false.** §12 carries at least three block-validity conditions:
`accumulation.tex:287` ("In the unlikely event it does happen, **the block must be considered invalid**", on conflicting
new/removed service indices) and eq. 12.35–12.36 (`accumulation.tex:446–447`, E_P must be ordered/unique and every pair
must satisfy Y against the **prior** δ).

- Line 153, replace
  `區塊有效性條件在 §11 而不在 §12。`
  with
  `§12.1 沒有任何條款把 dependency 問題升級成區塊無效（§12 另有區塊有效性條件——12.18 底下 n/m 的索引衝突、以及 eq. 12.35–12.36 對 E_P 的要求——但與 dependency 無關）。`

*(Verified-correct: Q's `g` filter; the three cases of eq. 12.33; the cyclic-overwrite lifetime and its match to
`accumulation.tex:32`; the rebuttal of the "E removes entries with dangling dependencies" distractor.)*

---

### n=5 · `c3-ch12-gas-floor-vs-ceiling` — **OK**
Checked: §11.4 gas rule verbatim at `reporting_assurance.tex:329–334` (`≤ G_A`, `≥ δ[d_s]_g`, against prior δ);
block budget `accumulation.tex:350–352`; `definitions.tex:268` ("Should be no smaller than G_A·C + Σ");
`transfer` → LOW at `pvm_invocations.tex:884`; a_g/a_m semantics at `accounts.tex:56`, which sits in **§9.1 "Code and
Gas"** (`accounts.tex:38`) — the cited section is right; `new` (`pvm_invocations.tex:806–845`) has no a_g ≤ G_A invariant.

### n=6 · `c3-ch12-theta-from-yield` — **OK**
Checked: b's `b ≠ ∅` filter and s's `{t_d}` term (`accumulation.tex:190–207`); θ′ at 12.25; C(16)→θ
(`merklization.tex:84`); eq. 7.7 `β′_B ≡ 𝒜(β_B, ℳ_B(s, H_K), H_K)` with `\fnmmrappend = 𝒜`, `\fnmerklizewb = ℳ_B`;
super-peak `ℳ_R(β′_B)` written into the new β_H item (`recent_history.tex:42`).

### n=7 · `c3-ch12-provide-two-places` — **OK**
Checked: both applications of I (`accumulation.tex:213–216` inside Δ*, eq. 12.37 at `:452`); Y's exact predicate
(eq. 12.21); the "disregarded / without prejudice" wording at `accumulation.tex:268` and `:450`; W_C = 4,000,000 is the
max **service code** size (`definitions.tex:286`), correctly used only to refute a distractor.

### n=8 · `c3-ch12-code-accumulation-statistics` — **OK**
Checked: eq. 12.27 `S ∈ ⟨N_S → (N, N, N_G)⟩`, eq. 12.28 `S(s) = ⟨N(s), T(s), G(s)⟩` with the `≠ ⟨0,0,0⟩` filter and
`T(s) ≡ |⟦t | t ↕ t, t_d = s⟧|`; Δ+'s five-component return (`accumulation.tex:155,159`) bound at eq. 12.24;
N(s) counts digests; G(s) is gas *used*; the δ‡ / `a_a = τ′` link (eq. 12.29–12.30). PR #502 attribution matches
`research/ecosystem-notes.md`. Independently corroborated by `statistics.tex:169`, which reads
`𝒰(S[s], ⟨0,0,0⟩)` — a three-tuple.

### n=9 · `c3-ch12-why-R-star-is-a-sequence` — **OK**
Checked: eq. 11.17 verbatim (`reporting_assurance.tex:183–188`) — ascending core index over **ρ†**, `> 2/3·|κ|`;
eq. 12.17's prefix `i`; eq. 12.31 `ξ′[E−1] = P(R*[..n])`; eq. 12.4 / 12.11.

### n=10 · `c3-ch12-accseq-n-with-transfers` — **OK**
Checked: `n = i + |t| + |f|` (`accumulation.tex:164`) vs the `when n = 0` base case (`:157`); Δ* invoked on `r[..i]`
(`:165`); s's `{t_d}` term; the five-tuple; f = ∅ in the recursive call (`:166`), consistent with the stem. `𝒰(f[s], 0)`
in the explanation matches GP notation (`\fnsubifnone = 𝒰`, `notation.tex:30`, `accumulation.tex:315`).

### n=11 · `c3-ch12-prior-privileged-index-reads` — **EXPLANATION-DEFECT (minor)**

The keyed answer and the main body of the explanation are exactly right (`accumulation.tex:217–245`: `e_i′ = (Δ1(e_v)_e)_i`,
`e_q′[c] = ((Δ1(e_a[c])_e)_q)[c]` off the **prior** destructured `e`; R only for χ′_A/χ′_V/χ′_R; e_m′/e_z′ straight from
`e* = Δ1(m)_e`). The defect is the tacked-on causal claim:

"…這也是 §8 的 authorization pool 必須在 accumulation 之後才更新的**原因**" — that is not the GP's reason.
`authorization.tex:30` states it plainly: *"Since α′ is dependent on φ′, practically speaking, this step must be computed
after accumulation, the stage in which φ′ is defined."* The ordering follows from α′ **reading** φ′ (eq. 8.2), not from
the prior-vs-posterior assigner selection.

- Line 438, replace
  `這也是 §8 的 authorization pool 必須在 accumulation 之後才更新的原因。`
  with
  `另外 §8 的 α′ 之所以必須在 accumulation 之後才算，authorization.tex 給的理由是「Since α′ is dependent on φ′ … this step must be computed after accumulation, the stage in which φ′ is defined」——那是 α′ 讀 φ′ 造成的順序，與這條 prior/posterior 選擇規則無關。`

Secondary (optional): "（正是 GP PR #519 收緊 bless 想擋的那類攻擊）" over-claims. #519 restricts `bless` to the manager
service; it is a different mechanism, and the GP never states a motive for reading the *prior* χ_A/χ_V.

- Line 440, replace
  `說用 posterior χ′ 會造成同區塊自我授權（正是 GP PR #519 收緊 bless 想擋的那類攻擊）；`
  with
  `說用 posterior χ′ 會造成同區塊自我授權（GP 未載明這條規則的動機；0.8.0 另有 PR #519 把 bless 限縮給 manager，方向類似但機制不同）；`

### n=12 · `c3-ch12-code-delta-star-map-order` — **OK**
Checked: eq. 12.18's `↕` on u and t′ vs plain `∈` on b (`accumulation.tex:196–212`); `notation.tex:123` ("when the
ordering of elements matters we use ↕ … applies to any set which has an unambiguous ordering") → ascending service index
for s ⊂ N_S; the flattened `⌢t′` → next round's t → `i^T = ⟦t | t ↕ t, t_d = s⟧` (eq. 12.23 `:318–322`).
The code claim in the explanation is real and accurately characterised:
`team-repo/internal/accumulation/accumulation.go:784–785` — `sort.Slice(iT, func(i, j int) bool { return
iT[i].SenderID < iT[j].SenderID })`, and `sort.Slice` is documented as not stable.

---

### Cross-cutting — **answer-length leak (not one of the five labels, but it defeats the drill)**

In **12 of 12** items in this file the correct option is the **longest**, at 1.42–1.73× the mean option length.
AUTHORING.md rubric #3 explicitly forbids this ("Don't make the correct option the only long one"). A test-wise
candidate scores 12/12 without reading a line of the GP, which is precisely the failure mode an interview drill must not
train. This is bank-wide, not specific to this batch — **239 / 267 items (90 %)** have the longest option as the key
(`c3_ch12_accum.py` 12/12, `ch12_ch13.py` 12/12, `appA_pvm.py` 8/8, `arch_rationale.py` 11/11, …; the best file is
`ch09_accounts.py` at 62 %). Suggested remedy for the caller: pad the three distractors with equally specific GP detail
(they are currently ~180 chars of assertion vs ~400 chars of reasoning in the key), rather than trimming the key.

---

## Tally

- **MISMATCH: 0** (12/12 keys confirmed)
- **DELTA-DEFECT: 1** — n=1
- **AMBIGUOUS: 1** — n=4(a)
- **EXPLANATION-DEFECT: 5** — n=1 (a/c/d/e), n=2, n=3, n=4(b), n=11
- **OK: 7** — n=5, 6, 7, 8, 9, 10, 12
- Cross-cutting: answer-length leak, 12/12 in this file (90 % bank-wide)
