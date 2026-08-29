# R3 blind review — §7 Recent History / §8 Authorization (GP 0.8.0)

Reviewer: adversarial pass. Ground truth: `/root/work/jam/gp-src/text/*.tex`, `preamble.tex`,
cross-checked against the rendered `graypaper-0.8.0.pdf` text dump (`/root/work/jam/gp-layout.txt`)
for every equation number cited below.

Appendix letters confirmed from `graypaper.tex` `\appendix` ordering + `\section` count:
A = Polkadot Virtual Machine, B = Virtual Machine Invocations, C = Serialization Codec,
**D = State Merklization** (D.1 = "Serialization", holds `C(3)`), **E = General Merklization**
(E.2 = "Merkle Mountain Ranges and Belts"), F = Shuffling, G = Bandersnatch, H = Erasure Coding.

Symbols resolved from `preamble.tex`: `\rh¬headerhash`=h (654), `\rh¬accoutlogsuperpeak`=b (655),
`\rh¬stateroot`=s (656), `\rh¬timeslot`=t (657), `\rh¬reportedpackagehashes`=**p** (658);
`\Ccorecount`=C=341, `\Crecenthistorylen`=H=8, `\Cauthpoolsize`=O=8, `\Cauthqueuesize`=Q=80
(values from `text/definitions.tex:261,269,277,279`).

Section-7 equation map (verified against PDF p.16): 7.1 `β ≡ (β_H, β_B)`; **7.2** `β_H ∈ ⟦{h∈H, s∈H,
b∈H, t∈N_T, p∈⟨H→H⟩}⟧:H`; 7.3 `β_B ∈ ⟦H?⟧`; 7.4 `θ`; **7.5** `β†_H`; 7.6 `let s = …`; **7.7** `β_B′`;
**7.8** `β_H′`.

---

## PHASE 1 — BLIND VERDICTS

### n=1 · `c3-ch07-reported-map-shape`
- **My answer: index 0** — "A dictionary keyed by each work-package hash guaranteed in that block,
  whose value is that package's segment-root; at most C = 341 entries…"
- **Confidence: HIGH**
- Settled by: eq. 7.2 types `p` as `\dictionary{\hash}{\hash}` (`recent_history.tex:13`), and the
  `where` clause of eq. 7.8 builds it as
  `p = { ((g_r)_s)_p ↦ ((g_r)_s)_e | g ∈ E_G }` (`recent_history.tex:46-54`), i.e. key =
  availability-spec **package hash** (`\as¬packagehash`), value = **segment root** (`\as¬segroot`,
  preamble:553). The bound is stated verbatim in `recent_history.tex:21`: "the corresponding
  work-package hashes of each item reported (which is no more than the total number of cores,
  C = 341)". One-report-per-core comes from eq. 11.32 `ρ‡[r_c] = ∅`
  (`reporting_assurance.tex:326`).
- Distractors: header-hash set (there is no such field; H=8 is the *window* length, not a field
  bound); core index as value (value is the seg-root, and O=8 is the pool size); payload-hash
  sequence (p is a dictionary, not a sequence; I=`C_maxpackageitems`=16 is a package limit).

### n=2 · `c3-ch07-reported-map-downstream`
- **My answer: index 0** — "Three of them: an incoming package hash must not already be a key of any
  recent block's map (anti-duplicate); every prerequisite and every key of a report's segment-root
  lookup l …; and l must be a sub-dictionary of those maps…"
- **Confidence: HIGH**
- Settled by three separate §11 conditions, all reading `β_H`'s `p`:
  - **11.41** `∀p ∈ p, p ∉ ⋃_{x∈β_H} K(x_p) ∪ ⋃_{x∈ξ} x ∪ q ∪ a` (`reporting_assurance.tex:394`) —
    anti-duplicate, reads the **keys**.
  - **11.42** prerequisites ∪ `K(r_l)` ⊆ this block's package hashes ∪ `{x | x ∈ K(b_p), b ∈ β_H}`
    (`reporting_assurance.tex:404-409`).
  - **11.44** `∀r ∈ I : r_l ⊆ p ∪ ⋃_{b∈β_H} b_p` (`reporting_assurance.tex:423`) — sub-dictionary
    containment, so the *values* (segment roots) must match too.
- Note 11.41's union also contains ξ (`\accumulated`) and the ready/assignment sets — but the
  β_H-keyed term is genuinely there, so "three of them" is right.
- Distractors: "only the anti-duplicate one" contradicts 11.42/11.44; "only the anchor check" —
  eq. 11.36 (`reporting_assurance.tex:362`) reads `y_h, y_s, y_b, y_t` and **never** `y_p`;
  "none of them / BEEFY proofs" is flatly contradicted by 11.41/11.42/11.44.

### n=3 · `c3-ch07-superpeak-to-beefy`
- **My answer: index 0** — "Each block Keccak-Merklizes the encoded θ′ into one root and appends
  that root to the belt β_B; the new β_H item stores only the belt's Keccak super-peak; validators
  then BLS-sign the domain-separated hash of the newest item's super-peak…"
- **Confidence: HIGH**
- Settled by: eq. 7.6 `s = [E_4(s) ⌢ E(h) | (s,h) ⟨− θ′]`; eq. 7.7
  `β_B′ ≡ A(β_B, M_B(s, H_K), H_K)` (`recent_history.tex:30-32`) — one `M_B` root per block,
  appended with the MMB append function **A** (eq. **E.8**, `merklization.tex:296-317`), Keccak
  throughout ("Throughout, the Keccak hash function is used", `recent_history.tex:28`). eq. 7.8
  stores `b ↦ M_R(β_B′)` — the super-peak (eq. **E.10**, `merklization.tex:328-340`, itself Keccak:
  `keccak($peak ⌢ …)`). §18 eq. 18.1 (`beefy.tex:8`):
  `S_v ≡ BLS-sign_{κ′[v]_bls}( X_B ⌢ last(β_H)_b )`, `X_B = $jam_beefy`, "For each finalized block
  B which a validator imports".
- Distractors: signing the whole peak sequence (18.1 signs `last(β_H)_b`, and C(3) *does* store
  `E_M(β_B)` so the "fixed-length field" rationale is false); header marker (no super-peak marker
  exists in §5, and β_B is in C(3)); Blake2b rebuild (Keccak, and A appends rather than rebuilds).

### n=4 · `c3-ch07-dagger-before-append`
- **My answer: index 0** — "The back-fill lands on the block's own fresh item, so every entry ends up
  carrying its parent's posterior root instead of its own … eq. 11.36's state-root comparison
  rejects honest refinement contexts and the C(3) preimage diverges…"
- **Confidence: MED** (index is certain; one *clause* of this option is wrong — see Phase 2)
- Settled by: eq. 7.5 `β†_H ≡ β_H  except  β†_H[|β_H| − 1]_s = H_R` (`recent_history.tex:24-26`)
  operates on the **prior** β_H, i.e. corrects the *parent's* item. eq. 7.8 appends the new item
  with `s ↦ H_0` and `recent_history.tex:58` states the zero hash is "safe since β′ is not utilized
  except to define the next block's β†". Appending first makes `last()` the fresh item, so the
  off-by-one shifts every stored state root by one block. Downstream break: eq. **11.36**
  (`reporting_assurance.tex:362`) requires `x_anchorpoststate = y_s`; and `s` is in the C(3)
  preimage (`merklization.tex:28`), so the state root diverges.
- Distractors: "idempotent / nothing observable" (the correction targets a *different element*,
  so it is not idempotent); "only β_B corrupted" (β_B is computed from θ′, untouched by 7.5);
  "window stuck at 7" (the `←…→^H` truncation in 7.8 is orthogonal to 7.5).
- ⚠ Reservation recorded before seeing the key: the sub-clause "**and the block before it keeps the
  zero hash forever**" is false under the described bug — at every block the fresh item is appended
  with H_0 and then *immediately* overwritten by the mis-targeted back-fill, so no entry retains H_0.

### n=5 · `c3-ch07-c3-field-order`  (kind: code)
- **My answer: index 0** — "The encoder's order is right: state serialization is fixed by C(3) in
  appendix D … The real 0.8.0 gap is the missing 4-byte timeslot between the state root and the
  reported map"
- **Confidence: HIGH**
- Settled by: **the discrepancy is real, and D.1 governs serialization.** Character-by-character:
  - `recent_history.tex:8-14` (eq. 7.2): `h`, `s`, `b`, `t`, `p` — **state root before super-peak**.
  - `merklization.tex:26-31` (D.1, `C(3)`):
    `E( ↕[ (h, b, s, E_4(t), ↕p) | (h, b, s, t, p) ⟨− β_H ] , E_M(β_B) )`
    — **super-peak before state root**, timeslot as a fixed 4-octet field, `p` length-prefixed.
  - PDF confirmation (`gp-layout.txt:7728`, Appendix D):
    `C(3) ↦ E(↕[(h, b, s, E4 (t), ↕p) ∣ (h, b, s, t, p) <− βH ], EM (βB ))`.
  So the reviewer's premise (7.2 order ⇒ encoder must swap) is wrong: C(3) *explicitly names* the
  emitted fields and puts `b` second. The genuine defect in the 0.7.2 code is the absent
  `E_4(t)` between StateRoot and Reported — the 0.8.0 addition (β_H item gained `t`; see also
  `issues-digest.md:347`, "BlockInfo gets a 4-byte timeslot between state_root and reported").
- Distractors: "reviewer is right about order" (contradicted by D.1); "C(3) holds only the peak
  sequence" (it holds both the item sequence *and* `E_M(β_B)`, and there is no header marker);
  "per-item super-peak replaced by full peak sequence" (7.2 still types `b ∈ H`, a single hash).

### n=6 · `c3-ch08-queue-writer`
- **My answer: index 0** — "Only the service currently registered as that core's assigner, and only
  from inside its accumulate execution, by calling `assign`, which replaces all Q = 80 entries of
  that one core's queue in a single call and may also hand the assigner role to another service"
- **Confidence: HIGH**
- Settled by: `authorization.tex:22` — "The portion of state φ may be altered **only** through an
  exogenous call made from the accumulate logic of an appropriately privileged service." The call is
  `Ω_A`, `assign = 16` (`pvm_invocations.tex:762-763`, dispatched at :197). Its body
  (`pvm_invocations.tex:766-777`):
  - `q = [μ[o+32i ⋯ 32] | i ⟨− N_Q]` — reads exactly **Q = 80** hashes;
  - `→ HUH` when `x_s ≠ (x_state)_χ_A[c]` — **only the core's registered assigner**;
  - `→ CORE` when `c ≥ C`; `→ WHO` when `a ∉ N_S`;
  - otherwise `(OK, q, a)` — sets `φ[c] ← q` **and** `χ_A[c] ← a`, i.e. it can transfer the
    assigner role.
- Distractors: "any service may call assign / bless overrides" (bless is `Ω_B`, manager-only, and
  touches χ, not φ); "authorization extrinsic" (E has only E_T, E_P, E_G, E_A, E_D — no such
  extrinsic); "off-chain / header commitment" (φ is state, `C(2) ↦ E(φ)`, `merklization.tex:24`).

### n=7 · `c3-ch08-rotation-index-cyclic`
- **My answer: index 0** — "By cyclic subscription on the block's own timeslot, i.e. index H_T mod Q,
  with no stored cursor anywhere; a slot that produces no block simply never has its entry drawn…"
- **Confidence: HIGH**
- Settled by: eq. 8.2 (`authorization.tex:26`)
  `∀c ∈ N_C : α′[c] ≡ ←(F(c) ⌢ φ′[c][H_T]^↺)→^O`, and `notation.tex:120` defines
  `s[i]^↺ ≡ s[i mod |s|]`. Since `φ[c] ∈ ⟦H⟧_Q` with Q = 80 (eq. 8.1), the drawn index is
  `H_T mod 80`, keyed on the header's timeslot alone — there is no cursor in the state
  (eq. 8.1 lists only α and φ). Empty slots are therefore simply skipped.
- Distractors: per-core cursor (no such state item); `mod O` (O = 8 is the *pool* cap in the
  `←…→^O` truncation, not the queue index); FIFO-with-deletion (φ is a fixed-length `⟦H⟧_Q`
  sequence — entries are read, never removed).

### n=8 · `c3-ch08-psi-i-visibility`
- **My answer: index 0** — "Its two arguments only — the work-package and the core index, the latter
  handed to the PVM as a 2-byte encoded argument — plus what `fetch` can pull out of that package …
  no chain state at all, and besides `fetch` the only host calls are the gas counter and heap growth"
- **Confidence: HIGH**
- Settled by: eq. **B.1** (`pvm_invocations.tex:35-44`)
  `Ψ_I : (ℙ, N_C) → (𝔹 ∪ 𝔼, N_G)`, `(p, c) ↦ …` where
  [transcription of this signature corrected while resolving macros in Phase 2; verdict unchanged]
  `(u, r, ∅) = Ψ_M(p_u, 0, G_A, E_2(c), F, ∅)` — the core index enters as **`E_2(c)`**, a 2-octet
  argument blob. Prose at :33: "totally stateless. It provides only host-call functions for
  inspecting its environment and parameters."
  eq. **B.2** (`pvm_invocations.tex:45-55`) is the whole dispatch table: `gas → Ω_G`,
  `grow_heap → Ω_Ǥ`, `fetch → Ω_Y(ϱ, ω, μ, p, ∅, ∅, ∅, ∅, ∅, ∅, ∅)`, everything else `WHAT`.
  Because every argument of `Ω_Y` except `p` is ∅, the reachable `fetch` selectors are exactly
  0 (protocol constants), 7 (`E(p)`), 8 (`p_f` config), 9 (`p_j` token), 10 (`E(p_x)` context),
  11/12 (work-item metadata `S(w)`), 13 (work-item payload) — see `pvm_invocations.tex:349-402`.
- Distractors: read-only δ (no `read`/`lookup`/`info` in B.2); historical lookup like Refine
  (`Ω_H` appears only in Ψ_R's table, :97 region); the core's authorizer pool (α is chain state and
  is not passed to Ψ_I at all).

### n=9 · `c3-ch08-authcode-lookup-anchor`
- **My answer: index 0** — "From the preimage store of the separate auth-code host service named by
  the work-package, resolved by a historical lookup at the package's lookup-anchor timeslot…"
- **Confidence: HIGH**
- Settled by: eq. **14.11** (`work_packages_and_reports.tex:155-161`, PDF `gp-layout.txt:2843`):
  `p_a ≡ H(p_u ⌢ p_f)` and
  `E(↕p_m, p_u) ≡ Λ( δ[p_h], (p_x)_t , p_u )`
  with prose at :154: "We define the authorization code as `p_u` and require that it be available at
  the time of the **lookup anchor block** from the historical lookup of service `p_h`." `p_h` is the
  work-package's `authcodehost` service index (eq. 14.1, `work_packages_and_reports.tex:83-93`).
  The "why" is the historical-lookup design note in `pvm_invocations.tex:63`: Λ "is designed to give
  the same result regardless of the state of the chain for any time when auditing may occur".
- Distractors: first work-item's service at anchor posterior state (14.11 names `p_h` and the
  *lookup* anchor, not the anchor); code travelling in the bundle (only token + config are counted
  in eq. 14.6's bundle sum; `C_maxauthcodesize` bounds the *resolved* code, cf. B.1's `BIG` case);
  pool entry as code preimage hash (α holds `p_a = H(p_u ⌢ p_f)`, a hash of a hash ⌢ blob, which is
  not itself a retrievable preimage).

### n=10 · `c3-ch08-unauthorized-report-outcome`  (kind: code)
- **My answer: index 0** — "The prior pool, since the posterior one is only formed after accumulation
  out of the posterior queue; and the failure is an ordinary block-validity failure…"
- **Confidence: HIGH**
- Settled by: eq. **11.32** (`reporting_assurance.tex:324-327`, PDF `gp-layout.txt:1927`):
  `∀w ∈ I : ρ‡[w_c] = ∅ ∧ w_a ∈ **α**[w_c]` — unprimed α, the **prior** pool. Why it must be prior:
  `authorization.tex:30` — "Since α′ is dependent on φ′, practically speaking, this step must be
  computed after accumulation, the stage in which φ′ is defined." Failure is simply a violated
  block-validity predicate; §10 culprits/faults arise only from the disputes extrinsic E_D, never
  from a rejected guarantee.
- Distractors: posterior pool (α′ is not available at guarantee-validation time — 8.2/8.3 also
  *consume* the used authorizer via `F(c)`, so α′ may no longer contain it); culprits/slashing
  (nothing in §10 is written by a failed 11.32); "silently discarded at accumulation" (11.32 is a
  hard block-validity condition, not a filter).

**Blind summary: I answer index 0 for all ten items.** (Recorded as-is; noted as suspicious and
re-examined in Phase 2 rather than adjusted to look less uniform.)

---

## PHASE 2 — AUDIT vs `items/c3_ch07_ch08.py`

**Answer keys: all ten are `answer: 0`, identical to my ten blind verdicts. No MISMATCH, no
AMBIGUOUS, no DELTA-DEFECT.** Every defect below is in explanation/trap/caption text (one of them
also in the keyed-correct option's own wording) and none of them changes which option is right.

Extra macro resolutions used throughout this section (all from `preamble.tex`):
`\incomingreports`=**I** (677), `\wrX`=**r** (508), `\g¬workreport`=**r** (520→447),
`\as¬packagehash`=**p** (549→437), `\as¬segroot`=**e** (553→443), `\wr¬core`=**c**,
`\wp¬context`=**c** (488→429), `\wc¬anchortime`=**n** (561), `\blob`=**𝔹** (370),
`\avspec`=**𝕐** (547 — 𝕐 is the *availability spec* set in 0.8.0, not blobs), `\workerror`=**𝔼** (357),
`\gas`=**N_G** (409), `\accoutcommitment{v}`=**F**_v (681), `\vk¬bls`=**l** (602),
`\assigners`=**χ_A** (783), `\Xbeefy`=**X_B** (342), `\Cpackageauthgas`=G_I, `\Cmaxauthcodesize`=W_A,
`\Cgasunknown`=M_∅, `\Cmaxpackageitems`=I.

---

### n=1 · `c3-ch07-reported-map-shape` — **EXPLANATION-DEFECT** (severity MED)

Key = 0 = my answer. Bound, key/value semantics, distractor analysis and the team-code claim all
check out — I verified `internal/types/types.go:637-640` (`ReportedWorkPackage{Hash, ExportsRoot}`)
and `types.go:650-652` (`func (b *BlockInfo) Validate()` → `if len(b.Reported) > CoresCount`).
`I = 16` at eq. 14.2 is right too (14.2 *is* the work-package definition, whose `w ∈ ⟦W⟧_{1:I}`
carries the bound; `definitions.tex:270`).

**Defect — stale 0.7.x symbols inside a quoted 0.8.0 equation.** The explanation renders eq. 7.8's
`where` clause as `{((g_w)_s)_h ↦ ((g_w)_s)_e | g ∈ E_G}`. GP 0.8.0 reads
`{((g_r)_s)_p ↦ ((g_r)_s)_e | g ∈ E_G}` (`recent_history.tex:46-54`; PDF p.16). Both wrong glyphs
matter: `\g¬workreport` is **r** (not `w`), and the availability-spec package-hash field is **p**
(not `h`). Worse, in 0.8.0 `_h` is not a field of the availability spec at all, and the `w`/`W`
report symbols were replaced by `r`/`I` — a candidate who memorises this will quote a
non-existent equation at the oral.

**Fix** — in `items/c3_ch07_ch08.py`, replace the exact substring
```
{((g_w)_s)_h ↦ ((g_w)_s)_e | g ∈ E_G}
```
with
```
{((g_r)_s)_p ↦ ((g_r)_s)_e | g ∈ E_G}
```

---

### n=2 · `c3-ch07-reported-map-downstream` — **OK**

Key = 0 = my answer. All three cited conditions verified: 11.41 (`reporting_assurance.tex:394`),
11.42 (:404-409), 11.44 (:423); and the rebuttal of the anchor distractor via 11.36 (:362, which
compares `h, s, b, t` and never `p`) is exactly right.

Nit only (no fix required): "ξ 與 ω 確實出現在 eq. 11.41 的聯集裡" — ξ appears *literally* in
11.41's union, but ω does not; it enters through the derived set **q** of eq. 11.39
(`q = {(r_s)_p | (r, d) ∈ ⋃ω}`). The sentence's substantive point (they are additional sources, not
the basis of the prerequisite check) is correct.

---

### n=3 · `c3-ch07-superpeak-to-beefy` — **EXPLANATION-DEFECT** (severity MED)

Key = 0 = my answer. 7.6/7.7/7.8, E.8, E.10 and the Keccak claim all verified; the team-code aside
is true as well (`internal/recent_history/recent_history_controller.go:77-85` uses a `beefyBelt`
parameter and `types.go:645` names the field `BeefyRoot`).

**Defect — the BEEFY commitment is quoted with symbols GP 0.8.0 does not use.** The explanation
writes `beefy.tex：C(v) ≡ S_BLS(k_b, X_beefy ⌢ last(β_H)_b)`. GP 0.8.0 eq. **18.1**
(`beefy.tex:7-9`, PDF §18) is

`F_v ≡ S^BLS_{κ′[v]_l}( X_B ⌢ last(β_H)_b )`  with  `X_B = $jam_beefy`.

The commitment symbol is **F**_v (`\accoutcommitment`, preamble:681), not `C(v)`; the signing key
is `κ′[v]_**l**` (`\vk¬bls`, preamble:602), not `k_b`; and the domain separator is `X_B`
(`\Xbeefy`, preamble:342). `C` is badly overloaded in 0.8.0 — the state-key constructor `C(i)`
(this item's own §D.1!), the constancy preprocessor `C` (E.7) and the item-to-digest function `C`
(14.10) — so `C(v)` is actively misleading here.

Minor nits, no fix needed: eq. E.10's `|h| = 0 → H_0` case is omitted from the paraphrase, and
`(s, h) ∈ θ′` should be the ordered-in binder `(s, h) ⟨− θ′`.

**Fix** — replace the exact substring
```
beefy.tex：C(v) ≡ S_BLS(k_b, X_beefy ⌢ last(β_H)_b)，X_beefy = $jam_beefy
```
with
```
beefy.tex eq. 18.1：F_v ≡ S^BLS_{κ′[v]_l}(X_B ⌢ last(β_H)_b)，X_B = $jam_beefy
```

---

### n=4 · `c3-ch07-dagger-before-append` — **EXPLANATION-DEFECT** (severity **HIGH** — the false
claim is inside the keyed-correct option itself, then repeated in the explanation)

Key = 0 = my answer, and the option is still the only defensible one. Everything else in it is
right: the off-by-one, the 11.36 rejection and the C(3) divergence all follow from eq. 7.5
(`recent_history.tex:24-26`) + eq. 7.8, and the pipelining rationale cited in the explanation is
verbatim GP (`header.tex:56`: "We do this to facilitate the pipelining of block computation").

**Defect — "and the block before it keeps the zero hash forever" is false**, and the explanation
restates it as "而上一個區塊的 item 永遠停在 H_0". Simulate the described bug from genesis:

| block | step | resulting last entries |
|---|---|---|
| 1 | append `item₁(s=H_0)`, then correct **last** | `[item₁(s=root₀)]` |
| 2 | append `item₂(s=H_0)`, then correct **last** | `[item₁(root₀), item₂(root₁)]` |
| 3 | append `item₃(s=H_0)`, then correct **last** | `[item₁(root₀), item₂(root₁), item₃(root₂)]` |

Every freshly appended item is written with `H_0` and then **immediately** overwritten by the
mis-targeted back-fill in the *same* block, so after block 1 **no entry ever retains the zero hash**.
(It is the *correct* pipeline that leaves `H_0` in the last slot — `recent_history.tex:58` — until
the next block's β† fixes it.) What is actually lost is different and worth stating precisely: each
block's *own* posterior state root is never written anywhere, because the correction meant for the
parent's entry lands one slot too far right.

**Fix (two substrings).** In the option text, replace
```
and the block before it keeps the zero hash forever
```
with
```
and the parent's entry never receives the correction it was meant for
```
and in the explanation, replace
```
而上一個區塊的 item 永遠停在 H_0——整條 β_H 系統性 off-by-one
```
with
```
而上一個區塊的 item 再也拿不到本該補給它的 root——整條 β_H 系統性 off-by-one（注意：不會有任何 item 停在 H_0，新 item 一 append 就被錯位的修正立刻蓋掉）
```

---

### n=5 · `c3-ch07-c3-field-order` — **EXPLANATION-DEFECT** (severity LOW — wrong source line range
only). The substantive claim, including the GP-internal inconsistency, is **correct**.

Key = 0 = my answer. I verified the claimed inconsistency character by character in both files and
in the rendered PDF, as instructed:

- `text/recent_history.tex:8-14` (eq. 7.2) — field order `h`, `s`, `b`, `t`, `p`
  (`\rh¬headerhash`, `\rh¬stateroot`, `\rh¬accoutlogsuperpeak`, `\rh¬timeslot`,
  `\rh¬reportedpackagehashes`): **state root before super-peak**.
- `text/merklization.tex:26-31` (§D.1, `C(3)`) — emits
  `(\rh¬headerhash, \rh¬accoutlogsuperpeak, \rh¬stateroot, \encode[4]{\rh¬timeslot}, \var{\rh¬reportedpackagehashes})`,
  and even its comprehension binder destructures as `(h, b, s, t, p)`: **super-peak before state root**.
- Rendered PDF, `gp-layout.txt:7728`:
  `C(3) ↦ E(↕[(h, b, s, E4 (t), ↕p) ∣ (h, b, s, t, p) <− βH ], EM (βB ))`.

**The discrepancy is real**, and the item does exactly what it should: it treats D.1 as
authoritative for serialization and says so explicitly ("附錄 D 的 C(3) 才是序列化定義 … 狀態這一塊
以 D.1 為準"), while naming chapter 7's declaration as the thing that disagrees. So this is **not**
a MISMATCH. The 0.8.0 delta claim is also right — `t` is the 0.8.0 addition
(`issues-digest.md:347`: "`BlockInfo` gets a 4-byte `timeslot` between `state_root` and `reported`";
GP PR #526 puts `x_n` into the refinement context and 11.36 compares `x_n = y_t`, which I confirmed
at `reporting_assurance.tex:362` where `\wc¬anchortime` = **n**). The supporting evidence about the
vectors is accurate too: `internal/recent_history/data/progress_blocks_history-*.json` really do
order each item `header_hash`, `mmr`, `state_root`, `reported`
(and `internal/input/jam_types/jam_types.go:450-455` mirrors that), while `internal/types/types.go:643-648`
orders `HeaderHash, BeefyRoot, StateRoot, Reported` — both consistent with D.1's ordering.

**Code excerpt: faithful.** It matches `internal/types/encode.go` verbatim, with only the declared
`cLog(Cyan, "Encoding BlockInfo")` line elided (and blank lines closed up).

**Defect — the caption's line range is wrong at both ends.** `BlockInfo.Encode` runs
**1950–1980** (`func` at 1950, closing `}` at 1980; 1949 is the `// BlockInfo` comment and 1978 is a
blank line). The caption says `1949-1978`.

**Fix** — replace
```
internal/types/encode.go:1949-1978 (BlockInfo.Encode; log line elided)
```
with
```
internal/types/encode.go:1950-1980 (BlockInfo.Encode; log line elided)
```

---

### n=6 · `c3-ch08-queue-writer` — **EXPLANATION-DEFECT** (severity LOW — one wrong subscript case)

Key = 0 = my answer. Everything substantive verified against `pvm_invocations.tex:762-777`
(`assign = 16`; `[c, o, a] = ω_{7..9}`; `q` = Q = 80 hashes; `CORE` / `HUH` / `WHO` / `OK` branches;
`φ[c] ← q` **and** `χ_A[c] ← a`), plus `authorization.tex:22` for the "only through an exogenous
call … of an appropriately privileged service" note, `accumulation.tex:243-245`
(`∀c : χ_φ′[c] = ((acc(χ_A[c])_poststate)_φ)[c]` — only that core's assigner's write survives),
`pvm_invocations.tex:755` for the manager-only `bless`, and `overview.tex:17` (eq. 4.3) for the
five-extrinsic claim.

**Defect** — the explanation writes the assigner privilege as `χ_a[c]` (3 occurrences). GP 0.8.0's
symbol is **χ_A** (`\assigners` = `\privileges_A`, preamble:783; `definitions.tex:230` "The indices
of the services able to assign each core's authorizer queue"). Lowercase `a` is the *accumulation
partial-state* field name (`\ps¬assigners` = bold **a**), a different object; conflating the two is
exactly the kind of slip an examiner will pick up.

**Fix** — replace all 3 occurrences of
```
χ_a[c]
```
with
```
χ_A[c]
```
(all three are inside this item's explanation; no other item uses the string).

---

### n=7 · `c3-ch08-rotation-index-cyclic` — **OK**

Key = 0 = my answer. eq. 8.2 (`authorization.tex:26`), the modulo-subscription definition
(`notation.tex:120`), the `⟦H⟧_Q` vs `⟦H⟧_{:O}` contrast (eq. 8.1), the "keep the final n elements"
reading of `←(…)→^n` (`notation.tex:136`) and the "only `assign` can change φ" claim are all correct.
Rendering `φ′[c]↺[H_T]` rather than `(φ′[c][H_T])^↺` is cosmetic; the meaning is preserved.

---

### n=8 · `c3-ch08-psi-i-visibility` — **EXPLANATION-DEFECT** (severity MED)

Key = 0 = my answer. Everything else verified: eq. B.1 (`pvm_invocations.tex:35-44`) with
`Ψ_M(p_u, 0, G_I, E_2(c), F, ∅)`, `G_I = 50,000,000` (`definitions.tex:266`), `BAD` when `p_u = ∅`,
`BIG` when `|p_u| > W_A = 64,000` (`definitions.tex:284`); eq. B.2's three-call dispatch with
`M_∅` and `ω_7 ← WHAT`; the reachable `fetch` selectors {0, 7–13} and unreachable {1–6, 14, 15}
(`pvm_invocations.tex:349-402`); `Ψ_R` really is eq. **B.5** (PDF `gp-layout.txt:5707`);
`grow_heap` really is index 1 (`pvm_invocations.tex:311`) and the `sbrk` → `grow_heap` rename is a
genuine 0.8.0 change (`ecosystem-notes.md:466,717`) — the `delta-0.8.0` tag is earned.

**Defect — the signature of Ψ_I is quoted with a non-0.8.0 set symbol.** The explanation writes
`Ψ_I : (P, N_C) → (Y ∪ E, G)`. GP 0.8.0's eq. B.1 codomain is `𝔹 ∪ 𝔼` paired with `N_G`:
`\blob` = **𝔹** (preamble:370) and `\gas` = **N_G** (preamble:409). `𝕐` is not the blob set in
0.8.0 at all — it is `\avspec`, the *availability specification* set (preamble:547), so "Y ∪ E"
both uses a stale symbol and collides with a live one. `G` alone denotes gas *constants*
(G_A, G_I, G_R), not the gas set.

**Fix** — replace
```
Ψ_I : (P, N_C) → (Y ∪ E, G)
```
with
```
Ψ_I : (P, N_C) → (B ∪ E, N_G)
```

---

### n=9 · `c3-ch08-authcode-lookup-anchor` — **EXPLANATION-DEFECT** (severity MED)

Key = 0 = my answer. Verified: eq. **14.11** (`work_packages_and_reports.tex:155-161`, PDF
`gp-layout.txt:2843`) `p_a ≡ H(p_u ⌢ p_f)` and `E(↕p_m, p_u) ≡ Λ(δ[p_h], (p_c)_t, p_u)`; the
work-package's `h` (auth-code host) is indeed a field of eq. **14.2** separate from a work-item's
`s`; `D ≡ L + 4,800 = 19,200` is eq. **B.3** (PDF :5645) with L = 14,400 (`definitions.tex:273`);
`W_A = 64,000` and `W_B = 13,791,360` (eq. 14.8) are both right; and the anchor-vs-lookup-anchor
trap is sound.

**Defect** — the explanation writes the historical lookup as `Λ(δ[p_h], (p_x)_t, p_u)` (twice).
The work-package's refinement-context field is **c** in 0.8.0 (`\wp¬context` → `\¬context` =
bold **c**, preamble:488→429), so the GP text is `(p_c)_t`. `x` is a *different* object in this
neighbourhood — the §11 local set of incoming contexts defined at eq. 11.34 — so writing `p_x`
invites precisely the confusion the item's own trap warns about.

**Fix** — replace both occurrences of
```
(p_x)_t
```
with
```
(p_c)_t
```
(both are inside this item's explanation.)

---

### n=10 · `c3-ch08-unauthorized-report-outcome` — **EXPLANATION-DEFECT** (severity MED)

Key = 0 = my answer. Everything substantive verified: eq. 11.32's α is unprimed
(`reporting_assurance.tex:324-327`); the ordering argument quotes `authorization.tex:30` correctly;
ρ‡ really is the post-assurances intermediate (`overview.tex:57`, `eq:rhoddagger`); eq. **11.46**
really is the ρ′ definition (PDF `gp-layout.txt:1963`); and "an authorizer assigned in this block is
usable no earlier than the next block" follows correctly from α′ ← φ′ vs. 11.32 ← α.

**Code excerpt: faithful.** Verbatim match to `internal/extrinsic/guarantee_controller.go:172-186`
with the declared elision of the per-service accumulate-gas checks; caption line range is accurate.

**Defect — eq. 11.32 is quoted with the 0.7.x report symbols.** The explanation says
"eq. 11.32 寫的是 `∀w ∈ W : ρ‡[w_c] = ∅ ∧ w_a ∈ α[w_c]`". GP 0.8.0 reads
`∀r ∈ **I** : ρ‡[r_c] = ∅ ∧ r_a ∈ α[r_c]`, where **I** is defined at eq. 11.30
(`I = {g_r | g ∈ E_G}`; `\incomingreports` = **I**, preamble:677; `\wrX` = **r**, preamble:508).
`W`/`w` are not 0.8.0 symbols for this set, and this item is *not* flagged as a version-delta
discussion, so the stale notation stands unqualified.

**Fix** — replace
```
∀w ∈ W : ρ‡[w_c] = ∅ ∧ w_a ∈ α[w_c]
```
with
```
∀r ∈ I : ρ‡[r_c] = ∅ ∧ r_a ∈ α[r_c]
```

---

## PHASE 2 — TALLY

| id | verdict | severity |
|---|---|---|
| `c3-ch07-dagger-before-append` | EXPLANATION-DEFECT (false clause in the keyed option *and* the explanation) | HIGH |
| `c3-ch07-reported-map-shape` | EXPLANATION-DEFECT (stale `g_w` / `_h` in a quoted equation) | MED |
| `c3-ch07-superpeak-to-beefy` | EXPLANATION-DEFECT (`C(v)`/`k_b` for eq. 18.1's `F_v`/`κ′[v]_l`) | MED |
| `c3-ch08-psi-i-visibility` | EXPLANATION-DEFECT (`Y ∪ E, G` for B.1's `𝔹 ∪ 𝔼, N_G`) | MED |
| `c3-ch08-authcode-lookup-anchor` | EXPLANATION-DEFECT (`(p_x)_t` for `(p_c)_t`) | MED |
| `c3-ch08-unauthorized-report-outcome` | EXPLANATION-DEFECT (`∀w ∈ W` for `∀r ∈ I`) | MED |
| `c3-ch07-c3-field-order` | EXPLANATION-DEFECT (caption line range `1949-1978` → `1950-1980`) | LOW |
| `c3-ch08-queue-writer` | EXPLANATION-DEFECT (`χ_a[c]` → `χ_A[c]`, ×3) | LOW |
| `c3-ch07-reported-map-downstream` | **OK** (one nit noted, no fix) | — |
| `c3-ch08-rotation-index-cyclic` | **OK** | — |

- MISMATCH: **0**
- DELTA-DEFECT: **0** (both `delta-0.8.0` tags — the β_H timeslot and `sbrk` → `grow_heap` — are
  real 0.8.0 changes; I found no unflagged change that the set misses)
- AMBIGUOUS: **0**
- EXPLANATION-DEFECT: **8**
- OK: **2**

Nothing I could not settle from the .tex: every claim above is anchored to a file:line or to the
rendered PDF text.

---

## APPENDIX — mechanical field-order diff (n=5, the claimed GP-internal inconsistency)

Macro-name extraction from the two `.tex` sources (no eyeballing):

```
eq 7.2  (recent_history.tex:8-14)  declared : [headerhash, stateroot, accoutlogsuperpeak, timeslot, reportedpackagehashes]
D.1 C(3)(merklization.tex:26-31)   emitted  : [headerhash, accoutlogsuperpeak, stateroot, timeslot, reportedpackagehashes]
D.1 C(3)(merklization.tex:26-31)   binder   : [headerhash, accoutlogsuperpeak, stateroot, timeslot, reportedpackagehashes]

  pos 0: 7.2=headerhash              C(3)=headerhash              SAME
  pos 1: 7.2=stateroot               C(3)=accoutlogsuperpeak      <<< DIFFERS
  pos 2: 7.2=accoutlogsuperpeak      C(3)=stateroot               <<< DIFFERS
  pos 3: 7.2=timeslot                C(3)=timeslot                SAME
  pos 4: 7.2=reportedpackagehashes   C(3)=reportedpackagehashes   SAME
```

Two independent points follow. (a) The inconsistency is **real** — positions 1 and 2 are
transposed. (b) D.1 is **internally self-consistent**: its comprehension binder and its emitted
tuple use the same `h, b, s, t, p` order, so the serialization intent is unambiguous even though it
contradicts chapter 7's declaration. Item `c3-ch07-c3-field-order` is therefore correctly keyed and
correctly framed (D.1 authoritative, chapter 7 named as disagreeing) — not a MISMATCH.

Cross-check on the corpus-wide `answer: 0` pattern that made me suspicious in Phase 1:
`scripts/validate.py` reports pre-shuffle answer positions across all 267 items as
`{0: 156, 1: 46, 2: 42, 3: 23}`, i.e. index 0 is the house habit for the whole bank (options are
shuffled at render time). The uniformity in this batch is an authoring artefact, not evidence that
I anchored on the first option.
