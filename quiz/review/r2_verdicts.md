# r2 — blind verdicts + audit (§13 Statistics, §3 Notation), GP 0.8.0

Ground truth: `/root/work/jam/gp-src/text/{statistics,notation,reporting_assurance,accumulation,overview,merklization}.tex`,
`/root/work/jam/gp-src/preamble.tex`. Equation numbers cross-checked against the rendered
`/root/work/jam/graypaper-0.8.0.pdf` text dump (`/root/work/jam/gp-layout.txt`).

Symbol table facts fixed up-front (preamble.tex):
- `\activity`=π (832), `\valstatsaccumulator`=π_V (833), `\valstatsprevious`=π_L (834), `\corestats`=π_C (835), `\servicestats`=π_S (836)
- validator record fields (641–646): b, t, p, d, g, a
- core record fields (621–628): d, p, i, x, z, e, l, u
- service record fields (631–638): p, r, a, (t = `\ss¬xferral`, **declared but unused in 0.8.0 §13**), i, x, z, e
- `\accumulationstatistics`=**S** (675), `\reporters`=**G** (676), `\incomingreports`=**I** (677), `\justbecameavailable`=**R** (678)
- `\Csegmentsize`=W_G (280), `\bloblength`=N_L (408), `\gas`=N_G (409), `\ready`=**ω** (789) — 0.8.0 ready queue is ω, not ϑ
- `\activeset`=κ (816), `\previousset`=λ (817)

Real equation numbers (from gp-layout.txt): 13.1 π-tuple; 13.2 (π_V,π_L) type; 13.3 |π_V|=|κ|,|π_L|=|λ|;
13.4 π_V†; 13.5 (π_V‡,π′_L); 13.6 π′_V; 13.7 π_C type; 13.8 π_S type; 13.9 π′_C[c]; 13.10 R(c); 13.11 L(c);
13.12 D(c); 13.13 π′_S[s]; 13.14 s = s^R ∪ s^P ∪ K(S); 13.15 s^R; 13.16 s^P; 13.17 R(s).
11.17 **R** (available reports); 11.28 guarantor-sig block incl. `k ∈ G ⟺ …`; 11.30 `let I = {g_r | g ∈ E_G}`.
12.27 `S ∈ ⟨N_S → (N,N,N_G)⟩`; 12.28 `S ≡ {(s ↦ S(s)) | S(s) ≠ (0,0,0)}`.
4.1 `σ′ ≡ Υ(σ,B)`; 4.4 `σ ≡ (α,β,θ,γ,δ,η,ι,κ,λ,ρ,τ,ϕ,χ,ψ,π,ω,ξ)`. App. D key C(13) → π (merklization.tex:64–68).

---

## PHASE 1 — BLIND

### n=1 — `c3-ch03-bounded-numeric-blob-types`
- **My answer: index 2** — "…N_L is the GP's shorthand for the set of octet-sequence lengths and is equivalent to N_{2^32}; B_$ is the subset of blobs which are ASCII-encoded strings; …an octet always serializes to itself…"
- **Confidence: HIGH**
- Settled by: notation.tex:53 "`\N` denotes the set of naturals including zero whereas `\Nmax{n}` implies a restriction on that set to values **less than** n"; notation.tex:57 "we denote `\bloblength` as the set of lengths of octet sequences and is **equivalent to** `\Nbits{32}`"; notation.tex:149 "`\blob[\$]` denotes the subset of `\blob` which are ascii-encoded strings… we do not treat them as exactly equivalent entities. In particular for the purpose of serialization, an octet is always serialized to itself, whereas a natural number may be serialized as a sequence of potentially several octets, depending on its magnitude and the encoding variant."
- Distractors die on: idx0 (B_$ ≠ sentinel; B is *arbitrary-length* blobs, not single-octet), idx1 (N_n excludes n; N_L = N_{2^32}; octet ≠ natural for serialization), idx3 (N_L is lengths not sequences; B_x is *exactly* x octets, not "at most").

### n=2 — `c3-ch03-optional-none-error`
- **My answer: index 0** — "∅ marks a term validly left without a specific value and is defined to have cardinality zero; …A? ≡ A ∪ {∅}; ∇ marks an unexpected failure…; and 𝒰 yields its first argument that is not ∅"
- **Confidence: HIGH**
- Settled by: notation.tex:47 "We commonly use `\none` to indicate that some term is validly left without a specific value. Its cardinality is defined as zero. We define the operation `\optional{}` such that `\optional{A} ≡ A ∪ \set{\none}`"; notation.tex:49 "`\error` is utilized to indicate the unexpected failure of an operation or that a value is invalid or unexpected. (We try to avoid the use of the more conventional ⊥ here to avoid confusion with Boolean false…)"; eq. 3.2 notation.tex:30 "The substitute-if-nothing function `\fnsubifnone` is **equivalent to the first argument which is not** `\none`". Applied at statistics.tex:169 `\subifnone{\accumulationstatistics\subb{s}, \tup{0,0,0}}`.
- idx3's "dictionary subscript on a missing key yields ∇" is false — notation.tex:83–86 gives **∅** for a missing key.

### n=3 — `c3-ch03-ellipsis-ranges`
- **My answer: index 1** — "s_{…3} = [10, 20, 30], s_{1…+3} = [20, 30, 40], Z_{1…3} = {1, 2}, Z_{1…+3} = {1, 2, 3}, last(s) = 50, s[7]^⟲ = 30"
- **Confidence: HIGH**
- Settled by: notation.tex:118 "`\sq{0,1,2,3}\sub{\dots2} = \sq{0,1}`" (prefix of length n) and "`\sq{0,1,2,3}\sub{1\dots+2} = \sq{1,2}`" (offset 1, length 2) → s_{…3}=[10,20,30], s_{1…+3}=[20,30,40]; notation.tex:55 "`\Z\interval{a}{b}` … integers within the interval [a,b) … `\Z\interval{2}{5} = \set{2,3,4}`" and "offset/length form `\Z\subrange{a}{b}`, a short form of `\Z\interval{a}{a+b}`" → Z_{1…3}={1,2}, Z_{1…+3}=Z_{1…4}={1,2,3}; notation.tex:120 "modulo subscription `\cyclic{s[i]} ≡ s[i mod |s|]`" → s[7 mod 5]=s[2]=30; "last(s) ≡ x" of s = […, x] → 50.

### n=4 — `c3-ch03-prime-dagger-record`
- **My answer: index 3** — "A type declaration introduces each component with ∈ … while a concrete value binds fields with the tricolon … squaring the sequence-set says each of the two records is itself a sequence … the undecorated symbol is the prior state and the primed one the posterior — a convention the GP fixes not in §3 but alongside σ′ ≡ Υ(σ, B) — and dagger and double-dagger mark intermediate values…"
- **Confidence: HIGH**
- Settled by: §3.6 notation.tex:112 "we may denote a tuple with two named natural components a and b as T = ⟨a ∈ N, b ∈ N⟩. We would denote an item t ∈ T through subscripting its name, thus for some t = (a: 3, b: 5), t_a = 3 and t_b = 5"; statistics.tex:12–22 `⟦(…)⟧²` together with eq. 13.3 `|π_V| = |κ|, |π_L| = |λ|` → each of the two is a per-validator sequence; overview.tex:3–8 (eq. 4.1) "The latter defines the **posterior** state given a pairing of some **prior** state and a block… Where σ is the prior state, σ′ is the posterior state" — §3 (notation.tex) never mentions prime or dagger at all (grepped: zero hits); overview.tex:67 "The only synchronous entanglements are visible through the **intermediate** components superscripted with a dagger".
- idx1's "one record per epoch, each record carries a single validator's six counters" contradicts eq. 13.3. idx2's "§3 defines the prime" is false.

### n=5 — `c3-ch13-epoch-boundary-split`
- **My answer: index 1** — "The two assurance increments land in the last-epoch archive… One block is deliberately split across the two records."
- **Confidence: HIGH**
- Settled by ordering of eq. 13.4 → 13.5 → 13.6. statistics.tex:41–45 (eq. 13.4) applies the assurance step to **π_V** (prior) giving π_V†; statistics.tex:47–51 (eq. 13.5) `(π_V‡, π′_L) ≡ (π_V†, π_L) when e′ = e; ([(0,…),…], π_V†) otherwise` — so on a boundary block the archive receives **π_V†**, i.e. the already-assurance-incremented record; statistics.tex:54–74 (eq. 13.6) then adds b/t/p/d/g on top of the *zeroed* π_V‡. So assurers 4 and 9 → π′_L; author 7's b/t/p/d and guarantor 22's g → π′_V.
- idx3 is false: the trigger is `e = ⌊τ/E⌋` vs `e′ = ⌊τ′/E⌋` (statistics.tex:51), not H_E.

### n=6 — `c3-ch13-guarantee-credit-set`
- **My answer: index 0** — "Validator 12 moves by 1, validator 30 by 1, the author not at all — the added term is a Boolean membership test… two credentials in the same block still yield a single step, and the index v is resolved through the posterior active set."
- **Confidence: HIGH** on the arithmetic; see AMBIGUOUS note in Phase 2 re: the GP's own prose gloss of `g`.
- Settled by: statistics.tex:72–73 `π_V'[v]_g = π_V‡[v]_g + (κ′[v] ∈ G)` — κ′ is the **posterior** active set (preamble:816 `\activeset`=κ); reporting_assurance.tex:299 (eq. 11.28) `k ∈ G ⟺ ∃(w,t,a) ∈ E_G, ∃(v,s) ∈ a: k = (k[v])_e` — **G is a set of Ed25519 keys**, so the added term is a set-membership Boolean ∈ {0,1}; reporting_assurance.tex:308 "the Ed25519 key of each validator whose signature is in a credential is placed in the reporters set G". Two credentials by the same validator contribute the *same* key to the set, hence one step. Cross-rotation is immaterial here: eq. 11.28's `where (c,k) = M when ⌊τ′/R⌋=⌊t/R⌋, M* otherwise`, and eq. 11.23 gives M* the key sequence Φ(κ′) unless the previous rotation lies in the previous *epoch* — so both of validator 12's credentials yield the identical key.
- The author is nothing: eq. 13.6 has no author term on `g`. idx3 ("guarantors compensated through `a`") is flatly contradicted by eq. 13.4, where `a` counts assurances.

### n=7 — `c3-ch13-core-record-fields`
- **My answer: index 2** — "Only the last component is gas-typed (N_G, the refine gas summed over the digests); the DA load, the total extrinsic size and the total bundle length are octet quantities; …The container is a fixed-length sequence with one entry per core, rebuilt from scratch on every block, so no epoch-boundary zeroing exists for it."
- **Confidence: HIGH**
- Settled by: eq. 13.7 statistics.tex:86–97 — seven `\N` fields and `\isa{&\cs¬gasused&}{\gas}` as the only `\gas` (=N_G, preamble:409); the container is `\sequence[\Ccorecount]{…}`, a fixed C-length sequence, not a dictionary. statistics.tex:84 "These are tracked only on a per-block basis unlike the validator statistics which are tracked over the whole epoch." eq. 13.9 defines `∀c ∈ N_C: π′_C[c] ≡ (…)` outright — full rebuild, no `except`, so no zeroing step exists. Octet-ness: eq. 13.12 `D(c) ≡ Σ (r_s)_l + W_G⌈(r_s)_n·65/64⌉` is octets; `l` = `(r_s)_l` bundle length in octets; `z` = `\¬xtsize` (preamble:449) is a size.
- idx1's "DA load and refine gas both gas-typed" and "dictionary listing only active cores" are both false against eq. 13.7.

### n=8 — `c3-ch13-da-load-calc`
- **My answer: index 2 — "807,976"**
- **Confidence: HIGH**
- Settled by eq. 13.12 (statistics.tex:141–146): `D(c) ≡ Σ_{r ∈ R, r_c = c} (r_s)_l + W_G⌈(r_s)_n·65/64⌉` — the sum ranges over **R** = `\justbecameavailable` (preamble:678; eq. 11.17), i.e. *newly available* reports only, **not** over **I** = `\incomingreports` (eq. 11.30). The freshly-guaranteed report (a) is in I, not R (eq. 11.32 requires ρ‡[r_c] = ∅ for incoming reports, and R is built from ρ†-assigned reports crossing the ⅔ threshold, eq. 11.17), so it contributes only to `l` via eq. 13.11 `L(c)`, never to `d`.
  D(5) = 262,144 + 4104·⌈130·65/64⌉ = 262,144 + 4104·⌈132.03125⌉ = 262,144 + 4104·133 = 262,144 + 545,832 = **807,976**.
- Distractor forensics: 803,872 = floor instead of ceil (4104·132); 795,664 = 65/64 factor dropped (4104·130); 937,216 = the *incoming* report used instead of the available one (100,000 + 4104·⌈200·65/64⌉ = 100,000 + 4104·204).

### n=9 — `c3-ch13-rollover-code`
- **My answer: index 0** — "Only on blocks where ⌊τ/E⌋ ≠ ⌊τ′/E⌋… The fix is to run the assurance pass on the prior record before the branch and to hand the incremented record to the else-branch's archive assignment."
- **Confidence: HIGH**
- The code's `else` branch sets `PiLast = preStatistics.ValsCurr` — the **un**-daggered π_V — and then `UpdateCurrentStatistics` runs `UpdateAvailabilityStatistics` against the posterior (zeroed) current record. eq. 13.4 + 13.5 require π′_L = π_V†, i.e. assurances applied *before* the rollover. On same-epoch blocks the two orderings coincide, so the defect fires only on boundary blocks.
- idx1 false (eq. 13.4 indexes by `a_v`, the assurer, not H_I). idx2 false (13.6 credits the *new* record on boundary blocks). idx3: eq. 13.3 does say |π_V|=|κ|, |π_L|=|λ|, but |κ|=|λ|=V is constant, and idx3's second clause ("placement of the assurance increment is already identical") is false, which sinks it.

### n=10 — `c3-ch13-accum-triple-code`
- **My answer: index 0** — "…three-element value — work-digests accumulated for the service, deferred transfers delivered to it, and accumulation gas — obtained as the substitute-if-nothing of the service's entry in S against an all-zero triple. Since S now keeps every service whose triple is not all-zero, a service touched only by incoming transfers … joins the union that forms π′_S's domain."
- **Confidence: HIGH**
- Settled by: eq. 13.8 statistics.tex:106 `\isa{\ss¬accumulation}{\tup{\N, \N, \gas}}` — a **3-tuple**; eq. 13.13 statistics.tex:167–169 `a: 𝒰(S[s], (0,0,0))`; eq. 12.27/12.28 accumulation.tex:388–392 `S ∈ ⟨N_S → (N,N,N_G)⟩`, `S ≡ {(s ↦ S(s)) | S(s) ≠ (0,0,0)}` with accumulation.tex:394–408 `S(s) ≡ (N(s), T(s), G(s))`, `N(s) ≡ |[d | r ∈ R*_{…n}, d ∈ r_d, d_s = s]|` (accumulated work-digests), `T(s) ≡ |[t | t ∈ t, t_d = s]|` (**deferred transfers whose destination is s**), `G(s) ≡ Σ_{(s,u) ∈ u} u` (gas). Domain: eq. 13.14 `s = s^R ∪ s^P ∪ K(S)`, so a transfer-only service with T(s) > 0 has S(s) ≠ (0,0,0), is a key of S, and enters the domain. Confirms the 2-tuple → 3-tuple reshape and the observable consequence.
- idx2 is false: 0.8.0 has no separate top-level transfer pair in the service record (`\ss¬xferral` is declared at preamble:634 but appears nowhere in statistics.tex — a dead macro).

### n=11 — `c3-ch13-consensus-state-rationale`
- **My answer: index 3** — "…the figures must be bit-identical on every node and provable to a consumer outside the chain: JAM pays no rewards itself but has to deliver activity data to a staking subsystem… The pairing exists because settlement is per-epoch… Core and service records need no pairing because they are rebuilt every block."
- **Confidence: HIGH**
- Settled by: statistics.tex:5 "The Jam chain does not explicitly issue rewards—we leave this as a job to be done by the staking subsystem… it is important for the Jam chain to facilitate the arrival of information on validator activity in to the staking subsystem so that it may be acted upon"; statistics.tex:9 "we retain one record of completed statistics (π_L) together with one record which serves as an accumulator for the present epoch (π_V)"; statistics.tex:84 core/service stats "are tracked only on a per-block basis"; eq. 4.4 places π in σ; merklization.tex:64–68 `C(13) ↦ E(var[…π_V], var[…π_L], π_C, π_S)` gives it its own trie key.
- idx0 is false (a node skipping the update *would* diverge on the state root — C(13)). idx1 is false (Grandpa does not weight by these counters anywhere in the GP). idx2 is false (the GP explicitly does *not* pay rewards).

**Blind summary:** 1→2, 2→0, 3→1, 4→3, 5→1, 6→0, 7→2, 8→2, 9→0, 10→0, 11→3.

---

## PHASE 2 — AUDIT

**Key agreement: 11/11.** Every `answer` in `items/c3_ch13_stats.py` and `items/c3_ch03_notation.py`
matches my blind verdict. **No MISMATCH.** All DELTA claims were checked against
`/root/work/jam/research/issues-digest.md`, `/root/work/jam/team-repo` (VERSION_GP `0.7.2`,
HEAD `c7fb743`, 2026-07-24) and the .tex, and all survive — see the DELTA ledger at the end.
Four items carry explanation-level defects.

### FINDING 1 — `c3-ch13-consensus-state-rationale` — **EXPLANATION-DEFECT** (severity: MED-HIGH)
File: `items/c3_ch13_stats.py`

The explanation says π is committed into **H_R**, calling H_R "state root":

> 「App. D 以 C(13) 當 state key 併入 state trie，因此 π 進入 **H_R（state root）**、可被 light client 證明」

`H_R` is `\¬priorstateroot` (preamble.tex:742) — the **prior** state root. header.tex:56–58:

> "The parent state root $\H_\¬priorstateroot$ is the root of a Merkle trie composed by the mapping of the
> **prior** state's Merkle root… **This is a departure from both Polkadot and the Yellow Paper's Ethereum, in
> both of which a block's header contains the posterior state's Merkle root.** We do this to facilitate the
> pipelining of block computation and in particular of Merklization."
> `\H_\¬priorstateroot \equiv \merklizestate{\thestate}`  (σ, not σ′)

So π′ is *not* in this block's H_R; it is in M_σ(σ′), whose root first appears in the **child** block's H_R.
This is the single most-probed header fact in JAM orals, and the item currently teaches its inverse.
(The rest of the answer — C(13), eq. 4.4, the 17 σ components, per-epoch pairing, §13.2's per-block core/service
records, Grandpa not reading π — all check out.)

**Fix** — replace this exact source text (spans two adjacent string literals, lines 362–363):
```python
            "十七個分量之一，App. D 以 C(13) 當 state key 併入 state trie，因此 π 進入 H_R（state root）、"
            "可被 light client 證明；任何節點算錯 π 就會算出不同的 state root，直接是 invalid block——"
```
with:
```python
            "十七個分量之一，App. D 以 C(13) 當 state key 併入 state trie，因此 π′ 併入 M_σ(σ′) 並可被 light "
            "client 證明——但要記住 JAM 的 header 帶的是 **prior** state root（§5：H_R ≡ M_σ(σ)，GP 明說這是"
            "與 Ethereum／Polkadot 相反的設計，為了 pipelining），所以含 π′ 的 σ′ 之根要到**下一塊**的 H_R 才出現；"
            "任何節點算錯 π 就會算出不同的 state root，直接是 invalid block——"
```

### FINDING 2 — `c3-ch13-guarantee-credit-set` — **EXPLANATION-DEFECT + AMBIGUOUS** (severity: MED)
File: `items/c3_ch13_stats.py`

**Adjudication of the author's flagged question 1 — the item is RIGHT.** `κ′[v] ∈ G` is a set-membership
Boolean: eq. 11.28 (reporting_assurance.tex:299) defines `k ∈ G ⟺ … k = (k[v])_e`, so **G ⊂ H is a set of
Ed25519 keys**; §3.7.3 (notation.tex:143) supplies ⊤=1/⊥=0. Two credentials in one block contribute the *same*
key to the set ⇒ **+1, not +2**. Cross-rotation is a red herring: eq. 11.23 gives M* the key sequence Φ(κ′)
unless the previous rotation lies in the previous *epoch*. The item's `trap` line (κ′[v] ∈ 𝕂 is a 4-field tuple
while G ⊂ H, so implementations read `(κ′[v])_e ∈ G`) is exactly right — 𝕂's fields are b/e/l/m, preamble:596–599.

Two defects remain in the *explanation*:

**(2a) Mis-citation.** The explanation credits the +1 reading to team issue #710/#711:
> 「同一塊裡簽兩份 report 也只能 +1，這正是 issue #710/#711 的「only counting once for each validator」修法」

`issues-digest.md:267` records that fix's *resolution* as the opposite:
> "guarantees count = number of reports in E_G whose credentials include the validator's key
> (**each report counted once per validator**)"

i.e. under #710/#711 a validator signing two reports gets **+2**. Citing it as authority for +1 teaches a false
provenance and hands an interviewer a contradiction. The GP argument stands on its own; drop the attribution.

**(2b) Unflagged GP internal contradiction.** statistics.tex:31 glosses the counter as
> "$g$ — **The number of reports guaranteed by the validator.**"

Under eq. 13.6 that is false: `g` increments by at most 1 per block, so it counts *blocks in which the validator
guaranteed at least one report*. Distractor idx1's justification clause ("which is what makes it a count of
reports guaranteed") **is verbatim the GP's own prose** — so idx1 is defensible from statistics.tex:31 alone.
The stem's explicit quoting of eq. 13.6 saves the key, but a bank meant for memorisation must surface this or
the team will be blindsided. This is why I mark the item AMBIGUOUS as well as defective.

**Fix** — replace this exact source text (lines 90–92):
```python
            "依 §3.7.3「⊤ = 1、⊥ = 0」的隱含轉換，同一塊裡簽兩份 report 也只能 +1，這正是 issue #710/#711 的 "
            "「only counting once for each validator」修法，也是 UpdateReportStatistics 先建 reportersSet map、"
            "再對每個 validator 最多 +1 的原因。"
```
with:
```python
            "依 §3.7.3「⊤ = 1、⊥ = 0」的隱含轉換，同一塊裡簽兩份 report 也只能 +1（實作上就是先把 G 建成 "
            "reportersSet，再對每個 validator 最多 +1）。這裡有個 GP 自身的矛盾必須知道：§13.1 的欄位說明寫 "
            "「g: The number of reports guaranteed by the validator」，但依 eq. 13.6 的集合成員測試，g 每塊最多 +1，"
            "實際語意是「該 validator 在這一塊有沒有 guarantee 過 report」而不是 report 筆數。考試以 eq. 13.6 為準，"
            "但要認得那句 prose——以及團隊 0.7.0 時期 per-report 的舊讀法（#710/#711）——正是選項 B 的來源。"
```
Additionally (trivial, same explanation, line 88): the GP's guarantee-tuple field letters are **(r, t, a)**
(`\g¬workreport` = **r**, preamble:447+520; cf. eq. 11.30 `let I = {g_r | g ∈ E_G}`), not `(w, t, a)`.
Replace `∃(w, t, a) ∈ E_G` with `∃(r, t, a) ∈ E_G`.

### FINDING 3 — `c3-ch13-accum-triple-code` — **AMBIGUOUS / EXPLANATION-DEFECT** (severity: MED-LOW)
File: `items/c3_ch13_stats.py`

**Adjudication of the author's flagged question 2 — the item's "implicit per-service filter" is NOT something
the GP states.** eq. 13.13 (statistics.tex:163–166) writes the provision term as

```
p:  Σ_{(s, d) ∈ E_P} (1, |d|)
```

where `\xp¬serviceindex` = **s** (preamble:708 → 444) — the *same letter* as the outer `∀s ∈ s`
(statistics.tex:156). Read literally, the comprehension's pattern binding **shadows** the outer `s`, and the sum
ranges over *every* preimage in E_P, giving every service in the domain the identical total. §3 defines
set-builder and ordered-comprehension syntax (notation.tex:123, 131) but **never** states a
"repeated bound name unifies with the enclosing binding" rule — so there is no stated basis for a filter.

The intended reading is obviously the per-service filter, and the GP uses the same shadowing idiom elsewhere —
`G(s) ≡ Σ_{(s, u) ∈ u}(u)` at accumulation.tex:410 (eq. 12.28), and accumulation.tex:167. But note that where the
GP is being careful it picks *fresh* names for pattern components (judgments.tex:108; work_packages_and_reports.tex
:113 `Σ_{(h, l) ∈ …}`, :149 `Σ_{(h, z) ∈ …}`), which is what makes the `s` collision look like editorial
sloppiness rather than a convention. Verdict: **read it as a per-service filter, but do not present it as
something the GP says.**

The item's *answer key is unaffected* — option 0 turns entirely on the accumulation triple, not on `p`. The defect
is the explanation's unqualified assertion.

**Fix** — replace this exact source text (line 320):
```python
            "也沒有復活 Ψ_T。provision pair p 仍然獨立存在，記的是 E_P 裡給該 service 的 (筆數, 總 octet 數)。"
```
with:
```python
            "也沒有復活 Ψ_T。provision pair p 仍然獨立存在：eq. 13.13 寫作 p = Σ_{(s, d) ∈ E_P}(1, |d|)，"
            "注意 comprehension 綁定的 s 字面上**遮蔽**了外層的 ∀s ∈ s，而 §3 從未定義「重複綁定即過濾」的規則——"
            "照字面讀會退化成與 service 無關的全域總和。實際意思（也是所有實作的作法）是「E_P 中 service index "
            "等於該 s 的那些 preimage 的 (筆數, 總 octet 數)」；同樣的遮蔽寫法也見於 eq. 12.28 的 "
            "G(s) ≡ Σ_{(s, u) ∈ u}(u)，屬於 GP 的編輯瑕疵而非明文慣例。"
```

### FINDING 4 — `c3-ch03-prime-dagger-record` — **EXPLANATION-DEFECT** (severity: LOW)
File: `items/c3_ch03_notation.py`

> 「eq. 13.3 再釘死長度 |π_V| = |κ|、|π_L| = |λ|（0.8.0 改用 |κ|/|λ| 取代常數 V，**正是 team issue #1037 的來源**）」

The delta itself is sound (issues-digest.md:333, #1021: "statistics vectors sized to |κ| and |λ|"), and #1037 is
real and open (issues-digest.md:186, "feat: support variable validator-set size (|κ| ≠ V) across validation and
codecs"). But naming eq. 13.3 as its **source** over-narrows: #1037 is a *cross-phase* follow-up
(issues-digest.md:315) whose actual GP origin is **eq. 6.8** — `𝕍 ≡ {3c | c ∈ N_{2…C+1}}` (safrole.tex:100–101)
with `κ, λ ∈ ⟦𝕂⟧_𝕍` (safrole.tex:98–99) — i.e. 𝕍 is a *set of admissible validator-set sizes*, which is what makes
|κ| variable at all. eq. 13.3 merely consumes that. Secondary nit: an unverifiable team-issue number is
out of place in a §3 notation item that is otherwise pure GP.

**Fix** — replace this exact source text (line 178):
```python
            "eq. 13.3 再釘死長度 |π_V| = |κ|、|π_L| = |λ|（0.8.0 改用 |κ|/|λ| 取代常數 V，正是 team issue #1037 的來源），"
```
with:
```python
            "eq. 13.3 再釘死長度 |π_V| = |κ|、|π_L| = |λ|（0.8.0 改用 |κ|/|λ| 取代常數 V，根源是 eq. 6.8 的 "
            "𝕍 ≡ {3c | c ∈ N_{2…C+1}} 與 κ, λ ∈ ⟦𝕂⟧_𝕍——validator-set 大小在 0.8.0 是**可變**的），"
```

### OPTIONAL POLISH — `c3-ch03-ellipsis-ranges` (not a defect)
The explanation's universal claim 「GP 全篇沒有任何「a 到 b 皆含」的閉區間記法」 **holds** — I checked every
interval-like form. But readers will meet `\Nclamp` = `N_{a…b}` (safrole.tex:101, pvm_invocations.tex:329,
work_packages_and_reports.tex:322), which §3 never defines. It inherits the half-open `Z_{a…b}` reading, and this
is checkable: eq. 6.8's `𝕍 ≡ {3c | c ∈ N_{2…C+1}}` with C = 341 yields max 3·341 = 1023 = V **only** if
`c < 342`. Worth one clause so the team is not stranded when they hit it.

### ITEMS MARKED `OK` (7)
`c3-ch03-bounded-numeric-blob-types`, `c3-ch03-optional-none-error`, `c3-ch03-ellipsis-ranges`,
`c3-ch13-epoch-boundary-split`, `c3-ch13-core-record-fields`, `c3-ch13-da-load-calc`, `c3-ch13-rollover-code`.

Spot-checks that could have been defects but are correct:
- n=1: App. C **is** serialization (graypaper.tex appendix order: A pvm · B pvm_invocations · **C serialization** ·
  **D merklization** · E utilities · F bandersnatch · G erasure_coding), so both "App. C" here and "App. D key C(13)"
  in n=11's gpRef are right. `H ≡ B_32` ✓ notation.tex:159.
- n=2: "eq. 3.7 明寫 d[k] ≡ v … otherwise ∅" — eq. **3.7** is indeed `∀K,V,d ∈ ⟨K→V⟩: d[k] ≡ …`
  (gp-layout.txt:392) ✓. (notation.tex:93 adds "the result is undefined and any block which relies on it must be
  considered invalid" — an internal GP tension, but eq. 3.7 is explicit and the item cites it correctly.)
- n=5: `a_v = v` matches the GP literally (`\xa¬assurer` = **v**, preamble:705); τ′ = H_T ✓ safrole.tex:28
  (`\¬timeslot` = T, preamble:743); 「π_L 從來不會被歸零」✓ eq. 13.5.
- n=7: 「341 個 core」✓ definitions.tex:261 `C = 341`; `p = Σ_{a ∈ E_A} a_f[c]` ✓ statistics.tex:122
  (`\xa¬availabilities` = f, preamble:704); π_C is `\sequence[\Ccorecount]{…}`, a fixed-length sequence ✓.
- n=8: W_G = 4104 ✓ definitions.tex:287; the 65/64 rationale ✓ work_packages_and_reports.tex:316 ("each composed
  of a page of **64** hashes of segments") in **§14** ✓ (work_packages follows statistics in graypaper.tex);
  n + ⌈n/64⌉ = ⌈65n/64⌉ ✓. eq. 11.17 = **R**, eq. 11.30 = **I** ✓ (gp-layout.txt:1840, 1913) — gpRef correct.
- n=9: 「statistics.go 目前的行為」 ✓ verified against the working tree — `internal/statistics/statistics.go:479–485`
  still does `valsLast := preStatistics.ValsCurr` (un-daggered) and `UpdateAvailabilityStatistics` (line 103–107)
  writes into `statistics.ValsCurr` taken from the *posterior* state; #1034 is absent from this checkout's git log.
  The #1037 remark here is correctly scoped ("程式碼仍用常數 ValidatorsCount" ✓).

### DELTA LEDGER (all verified — no DELTA-DEFECT)
| claim | verdict | evidence |
|---|---|---|
| assurances credited **before** the epoch rollover is 0.8.0 behaviour; 0.7.2 put them in the fresh accumulator | **TRUE** | eq. 13.4→13.5 ordering; issues-digest.md:353 (#1034 "…rather than the fresh accumulator"); working tree still pre-fix |
| accumulation entry **2-tuple → 3-tuple** (the item's specific claim) | **TRUE, field-by-field** | 0.7.2 `ServiceActivityRecord` = `AccumulateCount U32` + `AccumulateGasUsed Gas` only (team-repo `internal/types/types.go:731–742`, no transfers field); 0.8.0 eq. 13.8 `a ∈ (N, N, N_G)` with eq. 12.28 `S(s) = (N(s), T(s), G(s))` = digests / transfers-to-s / gas (accumulation.tex:394–408) |
| transfer **count** only, no on-transfer gas, Ψ_T not restored | **TRUE** | eq. 12.27 is `(N, N, N_G)` — one gas slot; `\ss¬xferral` (preamble:634) is declared but appears **nowhere** in statistics.tex, i.e. a dead macro from the removed field; GP #502 "Add back processed transfer count to service statistics" ✓ ecosystem-notes.md:612; #656 removed `OnTransfersCount`/`OnTransfersGasUsed` in 0.7.1 ✓ issues-digest.md:424 |
| transfer-only services newly appear in π′_S | **TRUE** | eq. 12.28 keeps any s with `S(s) ≠ (0,0,0)`; eq. 13.14 unions `K(S)` into the domain |
| π_V/π_L sized by |κ|/|λ| is a 0.8.0 change | **TRUE**, but see Finding 4 for the attribution | eq. 13.3; root cause eq. 6.8 `𝕍 ≡ {3c | c ∈ N_{2…C+1}}` |
| core/service stats have no epoch rollover | **TRUE** | statistics.tex:84; eq. 13.9/13.13 rebuild unconditionally |

**Stale-symbol sweep: clean.** No `ϑ` anywhere in either module (0.8.0's ready queue is **ω**, preamble:789 /
definitions.tex:236). Validator fields `b,t,p,d,g,a`, core fields `d,p,i,x,z,e,l,u` and service fields
`p,r,i,x,z,e,a` all match the 0.8.0 preamble exactly. No pre-0.8.0 statistics field names used.
