# r5 — Appendices E/F/G/H — independent review (GP 0.8.0)

Ground truth: `/root/work/jam/gp-src` @ `07f041d Release version 0.8.0`, `VERSION` = 0.8.0.

Appendix letters confirmed from `graypaper.tex` `\input` order after `\appendix`:
A `pvm.tex`, B `pvm_invocations.tex`, C `serialization.tex`, D "State Merklization"
(`merklization.tex` §1), **E "General Merklization"** (`merklization.tex` §2),
**F `utilities.tex` (Shuffling)**, **G `bandersnatch.tex`**, **H `erasure_coding.tex`**.

Equation numbering re-derived by counting numbered environments per appendix:
E.1 `N` (`eq:merklenode`), E.2 `T` (trace), E.3 `M_B` (`eq:simplemerkleroot`),
E.4 `M` (`eq:constantdepthmerkleroot`), E.5 `J_x`, E.6 `L_x`, E.7 `C`,
E.8 `A` (`eq:mmrappend`), E.9 `E_M`, E.10 `M_R`.
F.1 `F` (`eq:suffle`), F.2 `Q_l`, F.3 `F` from hash (`eq:sequencefromhash`).
G: five numbered `align` lines but **no `\label`s** → §-style citation is the only safe form.
H.1 `D` (`eq:ecoriginalshards`), H.2 `split`, H.3 `join`, H.4 transpose,
H.5 `C_v^k` (`eq:erasurecoding`), H.6 `R_v^k` (`eq:erasurecodinginv`), H.7+ field/basis.

---

## PHASE 1 — BLIND VERDICTS

### n=1 · `c3-appE-wb-vs-constant-depth`
- **Answer: index 0** — "The segment-root uses M: the preprocessor C rewrites every item as
  H('$leaf' ⌢ s) and pads to 2^⌈log₂ n⌉ zero-hash leaves … The erasure-root uses M_B…"
- **Confidence: HIGH**
- Settled by `work_packages_and_reports.tex` §14.4.4 (Availability Specifier):
  `a_e = M(s)` (`\is{\as¬segroot}{\merklizecd{\mathbf{s}}}`) and
  `a_u = M_B([⌢(x) | x ∈ ᵀ[b♣, s♣]])` (`\as¬erasureroot &= \merklizewb{…}`).
  Confirmed again by `reporting_assurance.tex` §11.1.3: "The *segment-root* is the root of a
  **constant-depth**, left-biased and zero-hash-padded binary Merkle tree".
- Well-balancedness rationale is quoted verbatim in `merklization.tex` E: "This *well-balanced*
  formulation ensures that the maximum depth of any leaf is minimal and that the number of
  leaves at that depth is also minimal", and "it avoids hashing each item in the sequence".
- E.7 `C` matches the option's description exactly: `|v'| = 2^⌈log₂(max(1,|v|))⌉`,
  `v'_i = H($leaf ⌢ v_i)` for `i < |v|`, else `H_0`. Paged proofs use `J_6`/`L_6`
  (`eq:pagedproofs`), i.e. 2⁶ = 64-leaf pages → "64-leaf pages stay size-aligned" ✓.
- Distractor kills: index 2 ("every leaf the same proof length") describes the *constant-depth*
  tree, not `M_B`; index 3 ("padding to a power of two is what makes a tree well-balanced")
  inverts E entirely.
- ⚠ Note on the item's own `gpRef`: it writes "eq. 11.5 (segment-root **a_s**)". In 0.8.0
  `preamble.tex:553` gives `\as¬segroot = e`, so the 0.8.0 symbol is **a_e**. `a_s` is stale.

### n=2 · `c3-appE-code-trace-split`
- **Answer: index 2** — "It rounds the split down while the GP — and this file's own node
  function — round it up … for three items at index 0 the GP yields two nodes and this yields
  one. Page proofs escape it because C has already padded to a power of two, but the direct
  call that builds the CE 140 segment-shard co-path does not."
- **Confidence: HIGH**
- GP eq. E.1 `N` splits at `⌈|v|/2⌉`: `N(v_{…⌈|v|/2⌉}) ‖ N(v_{⌈|v|/2⌉…})`. GP eq. E.2 `T`
  uses the same `⌈|v|/2⌉` in both `P^s` and `P_I`.
- Go (`/root/work/jam/team-repo/internal/utilities/merkle_tree/merkle_tree.go`):
  `N` line 30 `mid := (len(v) + 1) / 2` (= ⌈⌉, correct); `T` line 84 `mid := types.U32(len(v) / 2)`
  (= ⌊⌋, wrong). Confirmed by reading the file, not from the excerpt.
- Worked check, |v| = 3, i = 0. GP: ⌈3/2⌉ = 2 → `[N(v[2:])] ⌢ T(v[0:2], 0)` → inner ⌈2/2⌉ = 1 →
  `[N(v[1:2])] ⌢ T(v[0:1],0)` = `[]` ⇒ **2 nodes**. Go: mid = 1 → sibling `N(v[1:])`,
  traverse `v[:1]` → `len ≤ 1` returns `[]` ⇒ **1 node**. Exactly as index 2 states.
- Ordering claim in index 0 is false: Go appends `sibling` *then* `suffix`, i.e. root→leaf,
  the same order as GP T ("returns each opposite node from top to bottom").
- "Page proofs escape it": `Jx` (line 158) calls `C(v, …)` first; `C` (line 132) pads to a
  power of two, and every recursion level of a power-of-two-length sequence has ⌊n/2⌋ = ⌈n/2⌉.
  ✓ verified.
- "the direct call that builds the CE 140 segment-shard co-path does not":
  `/root/work/jam/team-repo/internal/networking/handler/ce/ce140.go:233`
  `coPath := merkle_tree.T(byteSequences, types.U32(segmentIndex), hash.Blake2bHash)` —
  `byteSequences` comes from `getSegmentShardSequence`, which slices the raw shard into
  32-octet chunks padded only to `(minSegments+1)*32`, never to a power of two.
  ✓ **The unpadded-caller claim is confirmed.** `T` has exactly two live call sites in the
  repo (`Jx` and `ce140.go`), so the blast radius described is right.
- Index 3 is wrong: `T` does not hash anything itself; `N` applies the prefix.
  (Separate, *unrelated* real bug I noticed: the Go prefixes are `"node"`/`"leaf"` whereas
  `\token{\$node}`/`\token{\$leaf}` are literally `$node`/`$leaf` — `\token` is just
  `\text{\small\texttt{#1}}` and `\$` is an escaped dollar. Not what this item asks about.)

### n=3 · `c3-appE-mmb-peaks-superpeak`
- **Answer: index 1** — "The append function A carries like binary addition … the separate
  super-peak M_R (a left-associated Keccak fold over the non-∅ peaks under a '$peak' prefix)
  is the one 32-octet value that enters β_H and is BLS-signed for Beefy."
- **Confidence: HIGH**
- E.8 `A`/`P`: `r ⌢ l` when `n ≥ |r|`; `R(r,n,l)` when `r_n = ∅`; otherwise
  `P(R(r,n,∅), H(r_n ⌢ l), n+1, H)` — textbook binary-counter carry ✓.
- E: "Hashing them removes the possibility of further appending so the range itself is kept on
  the system which needs to generate future proofs." ✓ ("hashing them away would end
  appendability").
- E.10 `M_R`: `Keccak($peak ⌢ M_R(h_{…|h|-1}) ⌢ h_{|h|-1})` over `h = [h ∈ b, h ≠ ∅]` —
  left-associated, Keccak, `$peak` prefix ✓.
- `recent_history.tex` `eq:recenthistorydef`: `β_H` entry field
  `\is{\rh¬accoutlogsuperpeak}{\mmrsuperpeak{\accoutbelt'}}`, and `preamble.tex:655` names that
  field `b` — matching the stem's "one 32-octet value b" ✓.
- `beefy.tex` `eq:accoutsignedcommitment`: BLS over `X_beefy ⌢ last(β_H)_b` ✓.
- Distractor kills: index 0 says Blake2b `M_B` of the peaks (it is Keccak `M_R`);
  index 2 invents an H-entry ring buffer for peaks and names `E_M(β_B)` as the stored value
  (`E_M` is only used in the *state serialization* `C(3)`, not in `β_H`);
  index 3 says Beefy signs the per-block accumulation root (that is the MMR *leaf*
  `M_B(s, Keccak)`, not the stored value).

### n=4 · `c3-appF-shuffle-is-consensus`
- **Answer: index 0** — "Reject the change … its output drives the guarantor-to-core assignment
  P(|κ′|, η′_2, τ′) and the tranche-0 audit selection."
- **Confidence: HIGH**
- `grep -n "fyshuffle" text/*.tex` gives **exactly two** consensus call sites in 0.8.0:
  `reporting_assurance.tex:230` inside `P(v,e,t)`, used as
  `G ≡ ⟨P(|κ'|, η'_2, τ'), Φ(κ')⟩` — the option's `P(|κ′|, η′_2, τ′)` is verbatim; and
  `auditing.tex:67` `L_0 = {w | w ∈ F(local reports, Y(s_0))_{…10}, w ≠ ∅}` (tranche-0).
- F.1 is literally `s_{r_0 mod l}` — the modulo is in the normative definition, so any
  de-biasing is a consensus fork, not an improvement. ✓
- Index 3's premise is false: `γ_a` is never shuffled; `safrole.tex`
  `γ_a' ≡ →[x ordered by x_id | x ∈ n ∪ …]^E` sorts by ticket identifier.
- Index 2 is false: F.2 `Q_l` slices 4-octet windows out of a Blake2b digest, which does
  nothing about `mod l` bias.

### n=5 · `c3-appF-seq-from-hash-vs-fallback`
- **Answer: index 1** — "The shuffle's expansion makes one Blake2b call per eight outputs …
  §6's fallback hashes once per slot … and decodes only the leading 4 octets, using the result
  to index the key sequence cyclically."
- **Confidence: HIGH**
- F.2 `Q_l(h) = [ E⁻¹₄( Blake(h ⌢ E₄(⌊i/8⌋))_{4i mod 32 …+4} ) | i ∈ ℕ_l ]` — the hash input
  changes only every 8 indices, and the window offset cycles 0,4,…,28 → 8 draws per digest ✓;
  `\decode[4]` is the GP's little-endian codec ✓.
- `safrole.tex` `eq:fallbackkeysequence`:
  `F(r, k) = [ ↻(k[E⁻¹₄(Blake(r ⌢ E₄(i))_{…4})])_bs | i ∈ ℕ_E ]` — one hash per slot `i`,
  **leading** 4 octets (`_{…4}`), and `↻` is modulo subscription
  (`notation.tex:120`: `↻(s[i]) ≡ s[i mod |s|]`) → cyclic indexing ✓.
- Index 0 is false — F and the appendix-F shuffle are *different functions*: F never permutes,
  it samples with replacement (the same key can be picked for many slots).

### n=6 · `c3-appG-why-ring-not-plain-vrf`
- **Answer: index 2** — "the proof shows only that its author knows a secret whose public key
  lies in the ring committed by γ′_Z, never which one …"
- **Confidence: HIGH**
- `notation.tex:169`: a ring proof is a "proof of knowledge of a secret within some sequence of
  public keys identified by a root", giving "a unique, valid—and **anonymous**—proof".
  `notation.tex` §3.8.2: "the difference is that the member is identified in the former and is
  **anonymous in the latter**."
- `safrole.tex:14`: "**In order to generate γ_s while keeping the correspondence between
  tickets and validators anonymous**, we use a novel RingVRF" — anonymity is stated as *the*
  reason; and `safrole.tex:8` "the identity of the key-holder of any future timeslot will have
  a very high degree of anonymity."
- Index 0 is the trap: unbiasability is real (`safrole.tex:14` point 2) but it is **not**
  ring-specific — an IETF VRF output is equally deterministic, so it cannot be the reason to
  prefer a *ring* VRF.
- Index 3 is false: `eq:ticketsextrinsic` binds the proof to `γ_Z'` = the ring of the pending
  validator set, so non-validators cannot enter.
- ⚠ The DoS/bribery consequence in index 2 is a reasonable gloss but I could **not** find it
  stated in so many words in 0.8.0 `.tex`; the GP says "anonymity" and stops there. Flagging
  as an inference, not a quotation.

### n=7 · `c3-appG-ring-root-commitment`
- **Answer: index 0** — "ordered Bandersnatch components of the **pending** key set … fixed
  144-octet commitment … Bandersnatch padding point is substituted."
- **Confidence: HIGH**
- `safrole.tex:115–120`: `⟨γ_P', κ', λ', γ_Z'⟩ ≡ (Φ(ι), γ_P, κ, z)` when `e' > e`,
  `where z = O([k_bs | k ∈ γ_P'])` — commits to the **pending** set's Bandersnatch components,
  recomputed only at the epoch boundary ✓.
- `safrole.tex:59`: "γ_z is the epoch's root, a Bandersnatch ring root composed with the one
  Bandersnatch key of each of **the next epoch's validators**, defined in γ_P."
- Size: `definitions.tex:33` "`ringroot` … A subset of `blob[144]`"; `notation.tex:169`
  "roots `ringroot ⊂ blob[144]`" ✓ 144 octets.
- Padding point: `bandersnatch.tex` closing note — "in the case a key `k_bs` has no
  corresponding Bandersnatch point when constructing the ring, then the Bandersnatch *padding
  point* … should be substituted" ✓. `Φ` (`eq:blacklistfilter`) replaces the **whole** key
  tuple with `[0,0,…]`, so its Bandersnatch slot is not a curve point → padding point.
- Index 1 (κ′, shrinking ring) and index 3 (Φ zeroes only the Ed25519 component) are both
  contradicted by `eq:blacklistfilter`; index 2's 32-octet Merkle root contradicts `blob[144]`.

### n=8 · `c3-appG-output-vs-signature`
- **Answer: index 2** — "a VRF output is a high-entropy hash influenced by the context but not
  by the message … the entropy rotation makes those two byte strings equal one epoch later."
- **Confidence: HIGH**
- `notation.tex` §3.8.2, verbatim: "both define a VRF *output*, a high entropy hash
  **influenced by x but not by m**, formally denoted `Y(…)`." Same statement in
  `bandersnatch.tex` where `Y(s) ≡ output(x)_{…32}` for both signature types.
- Ticket: `eq:ticketsextrinsic` — proof ∈ `ringproof_{γ_Z'}⟨X_T ⌢ η'_2 ⌢ i_entryindex⟩^[]`,
  identifier `n_id = Y(i_proof)`.
- Seal: `eq:ticketconditiontrue` — `H_s ∈ signature_{H_bskey}⟨X_T ⌢ η'_3 ⌢ i_entryindex⟩^{E_U(H)}`
  with `i_id = Y(H_s)`. Same `X_T = "$jam_ticket_seal"` (`safrole.tex:163`).
- Rotation: `⟨η'_1, η'_2, η'_3⟩ ≡ ⟨η_0, η_1, η_2⟩` when `e' > e`, so the `η_2` used to build
  the ticket is precisely the `η_3` in force one epoch later ✓ — the context byte string is
  literally identical, and the message differs but does not enter the output ✓.
- Sizes: 784-octet ring proof and 96-octet signature both confirmed in `bandersnatch.tex`.
- Index 0 (identifier = Blake2b of the proof) contradicts `n_id = Y(i_proof)`;
  index 1 (seal republishes a stripped proof) is invention; index 3 (identifier from η alone)
  would destroy unpredictability and contradicts `Y(·)`.

### n=9 · `c3-appH-code-shardcount-080`
- **Answer: index 1** — "the total is that size (which the on-chain rule pins to |κ′|), the
  data-shard count is the largest d with 2d dividing W_G and d no greater than v/3 + 1, and the
  pad width is twice that. On tiny that gives 3 data shards out of 6, a pad width of 6 and 684
  pieces per segment…"
- **Confidence: HIGH** (MED on the phrase "which the on-chain rule pins to |κ′|" — see below)
- H.1: `D(v ∈ 𝕍) ≡ max({ d | d ∈ ℕ_{v/3+2}, W_G mod 2d = 0 })`. `W_G = 4104`
  (`definitions.tex:287`); `2d | 4104 ⇔ d | 2052`; `2052 = 2²·3³·19`.
- `v = 6` → `d ≤ 3` → largest divisor of 2052 that is ≤ 3 is **3** ⇒ `D(6) = 3`, pad width
  `z = 2D = 6`, `k = W_G/z = 684` ✓ exactly index 1's numbers.
  `v = 1023` → `d ≤ 342`, `342 | 2052` ⇒ `D(1023) = 342` ✓ full is unchanged.
- The `𝒟`-derived pad width is normative: `avspec` sets `z = 2·D(a_v)` and pads the bundle
  `P_z(b)`; segments use `k = W_G/z` "Note that the definition of `D` ensures this is always an
  integer, *i.e.* no padding is required."
- Shard total = assuring-set size: `eq:avspec` types `a_v ∈ 𝕍`, and `reporting_assurance.tex`
  §11.1.3: "As one chunk is distributed to each assurer, **the number of chunks must equal the
  size of the assuring validator set**." `computereport` takes the assurer set size as its
  fourth argument (`work_packages_and_reports.tex:191`). ⚠ I did **not** locate an equation that
  literally reads `(w_s)_v = |κ'|` in `reporting_assurance.tex`; the prose ties `a_v` to the
  assuring set, and the report-validity rules would be where an on-chain `= |κ'|` pin lives.
  Treat the parenthetical as MED.
- Index 2 is the trap and is **false**: legal `v` are all multiples of 3
  (`eq:valcount`: `𝕍 ≡ {3c | c ∈ ℕ_{2:C+1}}`, i.e. 6…1023), but the divisibility side
  condition is still binding — e.g. `v = 1020` → `d ≤ 341`, and the largest divisor of 2052
  ≤ 341 is **228**, not 341. The condition is *not* automatically satisfied.
- Index 0 ("`D` is derived from the segment size, and the segment size has not changed") is
  false: `D` takes `v`, not `W_G`. Index 3 ("nothing changes; audit-DA keeps 342:1023") is
  false: `b♣` uses `C_{a_v}` and `z = 2D(a_v)` for the bundle too.
- Code excerpt verified against the repo: `internal/types/const.go:44-45` (tiny
  `ECPiecesPerSegment = 1026`, `ECBasicSize = 4`), `:65-66` (full `6` / `684`), `:188-189`
  (`DataShards = 342`, `TotalShards = 1023`), and `internal/work_package/work_package.go:262-273`
  (`buildBCloud`, `PadToMultiple(bundle, types.ECBasicSize)`) ✓ all quoted accurately.
- Version note: `W_E`/`W_P` no longer exist anywhere in 0.8.0 — the `\mathsf{W}` family is
  `W_A, W_B, W_C, W_F, W_G, W_M, W_R, W_T, W_X` (`preamble.tex:276-284`). Their use in this
  item is legitimate because it is an explicit 0.7.2→0.8.0 delta about the team's own code.

### n=10 · `c3-appH-what-gets-coded`
- **Answer: index 2** — "Two data sets: the auditable bundle, zero-padded … and the exported
  segments together with their paged-proof segments … A validator holds one leaf of the
  erasure-root: its bundle-chunk hash concatenated with the root over its own segment column."
- **Confidence: HIGH**
- `work_packages_and_reports.tex` §14.4.4, verbatim structure:
  `b♣ = Blake#(C_{a_v}^{⌈|b|/z⌉}(P_z(b)))` → pad, code, **hash each chunk** ✓;
  `s♣ = M_B#(ᵀ C_{a_v}^{W_G/z}#(s ⌢ P(s)))` → segments **plus paged proofs**, coded, then
  **transposed** so one chunk of every segment lands on one validator, then `M_B` per column ✓;
  `a_u = M_B([⌢(x) | x ∈ ᵀ[b♣, s♣]])` → leaf `i` = `b♣_i ⌢ s♣_i` ✓ exactly the option's leaf.
- §14.4.2 confirms the two-store framing: "Guarantors are required to erasure-code and
  distribute **two data sets**: one blob, the auditable *bundle* … and a second set of
  exported-segments data together with the *Paged-Proofs* metadata."
- Index 0 (erasure-root over report chunks; bundle stays with guarantors), index 1 (bundle
  replicated whole), index 3 (segments not coded, re-run refine) are each contradicted above.

### n=11 · `c3-appH-rate-and-field-rationale`
- **Answer: index 0** — "reconstruct even should almost two-thirds be malicious … the field is
  16-bit … twice the shard count must divide the 4,104-octet segment size …"
- **Confidence: HIGH**
- §H opening, verbatim: "This rate is derived from the fact we wish to be able to reconstruct
  even should **almost two-thirds** of the `v` validators be malicious or incapacitated, **the
  16-bit Galois field** on which the erasure-code is based and the desire to support, for
  simplicity, **encoding segments of size W_G without padding**." Index 0 reproduces all three,
  in order.
- "the count is the largest such value rather than exactly v/3 + 1" ✓: §H says the rate is
  optimal, i.e. `D(v) = v/3 + 1`, only for `v ∈ {6, 9, 15, 24, 33, 51, 54, 78, 105, 111, 159,
  168, 225, 321, 339, 510, 681, 1023}` — precisely `{3(d-1) | d | 2052, d ≥ 3}`.
- Field-size gloss ("an octet-wide field offers only 256 points and could not address 1,023"):
  §H "Code Word representation" assigns each validator `i` the field element
  `ĩ = Σ i_j v_j ∈ 𝔽̃_{2¹⁶}`, i.e. distinct evaluation points per validator, so 256 points
  cannot address 1,023 validators. Sound inference from the GP's own construction ✓.
- Index 2 is the trap: "exactly ⌊v/3⌋+1 for every legal validator-set size, so no side
  condition is ever active" is **false** — `D(1020) = 228 ≠ 341` (largest divisor of 2052
  ≤ 341). It also inverts causation on the segment size.
- Index 1 (threshold at 2v/3) and index 3 (683 validators; 32 octets = 16 code words) are
  arithmetic/consensus nonsense.
- **Adjudication of the "1:4.5" reading (task item 2).** §H: "when `v = 1022`, the rate is
  approximately 1:4.5." Literal-real reading of `d ∈ ℕ_{v/3+2}`: `1022/3 + 2 = 342.667`,
  so `d ≤ 342`, `342 | 2052`, giving `D = 342` and a rate of `342:1022 ≈ 1:2.99` — **it does
  not reproduce the GP's own number**. Floor-then-bound (`d ≤ ⌊v/3⌋ + 1 = 341`) gives the
  largest divisor of 2052 that is ≤ 341, namely **228**, and `1022/228 = 4.48 ≈ 1:4.5` ✓.
  **So the floor reading is the only one consistent with §H's worked example — claim upheld.**
  Caveat worth recording: `v = 1022 ∉ 𝕍` (`𝕍` is multiples of 3 from 6 to 1023), so the GP's
  example is hypothetical, and for every *legal* `v` the two readings coincide (`v/3 ∈ ℕ`).
  The discriminating legal case is `v = 1020` → `D = 228`, rate ≈ 1:4.47.


---

## PHASE 2 — AUDIT vs `items/c3_appEFGH.py`

**Answer keys: 11/11 agree with my blind verdicts. No `MISMATCH`, and no `DELTA-DEFECT`.**

Both `kind:"code"` excerpts were checked against the files they name and quote them
accurately (`merkle_tree.go` `T`; `const.go:44-45/65-66/188-189` + `work_package.go:262-273`).

Independent adjudication of the four high-risk claims:

1. **Item 2's "claimed Go bug" is REAL.** `N` uses `(len(v)+1)/2` (⌈⌉, matches E.1); `T`
   uses `len(v)/2` (⌊⌋, contradicts E.2). |v| = 3, i = 0 → GP 2 nodes, Go 1 node. `Jx`
   pre-pads via `C` so page proofs are safe; `ce140.go:233` calls `merkle_tree.T` directly on
   an unpadded 32-octet-chunk slice. **Caller claim confirmed.** (Bonus, unrelated to the
   item: `merkle_tree.go` prefixes are `"node"`/`"leaf"`, but `\token{\$node}` is literally
   `$node` — `\token` is `\text{\small\texttt{#1}}` and `\$` is an escaped dollar. Also `Ps`
   at line 60 uses ⌊⌋ while `PI` at line 69 uses ⌈⌉; neither is reachable from `T`.)
2. **Appendix H's floor-then-bound reading is UPHELD.** See n=11 above. Literal
   `d < 1022/3 + 2 = 342.667` gives `D = 342` → 1:2.99, contradicting §H's own 1:4.5;
   `d ≤ ⌊1022/3⌋ + 1 = 341` gives `D = 228` → 1:4.48 ✓. Caveat: `1022 ∉ 𝕍`
   (`𝕍 = {3c | 2 ≤ c ≤ 341}`), so for every *legal* `v` both readings coincide; the
   discriminating legal cases are `v = 1002` (`D = 228`, used correctly in items 9 and 11)
   and `v = 1020` (`D = 228`).
3. **Appendix F call sites CONFIRMED.** `grep fyshuffle text/*.tex` yields exactly two:
   `reporting_assurance.tex:230` (eq. 11.21 `P`) and `auditing.tex:67` (tranche-0). Ticket
   ordering never calls it — `γ'_A` is `sort by x_y`. §6's `F` (eq. 6.27) is a *different*
   function from appendix F's shuffle (it samples with replacement; it never permutes).
   Item 4's and item 5's framing of this is correct. Item 4's jamtestvectors claim also
   checks out: `internal/utilities/shuffle/shuffle_tests.json` has exactly 8 cases with
   input lengths **0, 8, 16, 20, 50, 100, 200, 341**, each pinning the full output sequence.
4. **Appendix G citations are §-style and accurate** (G.1–G.5 are numbered but carry no
   `\label`, so §-style is right). Ring root commits to `γ'_P` (pending), is `⊂ 𝔹_144`, and
   `Y(·)` is "influenced by x but not by m" — all verbatim. But three of the four G-item
   explanations carry wrong 0.8.0 letters; see F8/F10/F11.

Verdict tally: **0 OK · 11 flagged**, all `EXPLANATION-DEFECT`, none touching an answer key.
Nine are wrong-symbol / false-statement defects that a student would memorise as GP fact;
the rest are consistency and over-claim nits.

---

### F1 · `c3-appE-wb-vs-constant-depth` — `EXPLANATION-DEFECT` (HIGH)
**Wrong symbol `a_s` for the segment-root — three places (gpRef, stem, explanation).**
GP 0.8.0 eq. 11.5 is `Y ≡ ⟨p ∈ ℍ, l ∈ ℕ_L, u ∈ ℍ, v ∈ 𝕍, e ∈ ℍ, n ∈ ℕ⟩`
(`preamble.tex:549-554` → `:427,437,443`): the segment-root field is **`e`**. There is no
`s` field. This is not even a 0.7.x survival — the team's own 0.7.2 `WorkPackageSpec`
already annotates `ExportsRoot` as `$e$` (`internal/types/types.go:537`). Worse, `s` is taken
twice over in 0.8.0: `\wr¬avspec = **s**` (a work-report's *whole* avspec — eq. 11.31 reads
`(r_s)_v`) and `\sa¬storage = **s**` (service-account storage, which this same deck uses as
`a_s` in `items/ch09_accounts.py` and `items/c3_ch09_appD.py`). So `a_s` is actively
misleading in both directions.

Fix — three exact replacements:
- `eq. 11.5 (segment-root a_s)` → `eq. 11.5 (segment-root a_e)`
- `the segment-root a_s is built with one of them` → `the segment-root a_e is built with one of them`
- `segment-root a_s 是「a constant-depth` → `segment-root a_e 是「a constant-depth`

### F2 · `c3-appE-wb-vs-constant-depth`, `c3-appE-code-trace-split`, `c3-appH-what-gets-coded` — `EXPLANATION-DEFECT` (LOW)
**`Ⅎ` is not a Gray Paper symbol.** The paged-proofs function of eq. 14.12 is named **`P`**
(`work_packages_and_reports.tex:9` `\newcommand*{\pagedproofs}{P}`; the compiled 14.12 reads
`P : s ↦ [𝒫_l(E(↕J_6(s,i), ↕L_6(s,i))) | i ⊰ ℕ_{⌈|s|/64⌉}]`). `Ⅎ` occurs nowhere in the GP.
The overload the deck is presumably dodging is real — `P` is *also* the guarantor permute
(11.21) and `𝒫_l` is the zero-pad — so name it rather than invent a glyph.

Fix — three replacements:
- `讓 eq. 14.12 的 Ⅎ(s) 能用 J_6/L_6` → `讓 eq. 14.12 的 paged-proofs 函數 P（GP 就叫 P，勿與 eq. 11.21 的 permute P 或 eq. 14.17 的 zero-pad 𝒫_l 混淆）能用 J_6/L_6`
- `所以 work_package.go 走 eq. 14.12 的 Ⅎ(s) 分頁證明沒事` → `所以 work_package.go 走 eq. 14.12 的 paged-proofs P(s) 分頁證明沒事`
- `_{W_G/z}(s ⌢ Ⅎ(s))` → `_{W_G/z}(s ⌢ P(s))`

(Related nit, same family, LOW: item 10 writes the zero-pad as `P_z(b)`; GP has
`\fnzeropad = 𝒫_n`, i.e. `𝒫_z(b)`.)

### F3 · `c3-appE-mmb-peaks-superpeak` — `EXPLANATION-DEFECT` (MED, false statement)
**`E_M` does not take an `H` parameter.** The explanation says
「注意 M_R 是寫死 Keccak，不像 A 與 E_M 吃 H 參數」. Eq. E.9 is
`E_M : ⟦ℍ?⟧ → 𝔹, b ↦ E(↕[¿x | x ⊰ b])` — no hash-function argument, and it does not hash at
all (`\fnmmrencode = \fnencode[M]`, i.e. the codec `𝓔` subscripted `M`). Only `A` (E.8) takes
`H`. Everything else in this explanation is verbatim-correct.

Fix:
- `不像 A 與 E_M 吃 H 參數` → `不像 A（eq. E.8）收 H 參數；E_M（eq. E.9）則根本不雜湊，它只是 codec 𝓔_M`

### F4 · `c3-appF-shuffle-is-consensus` — `EXPLANATION-DEFECT` (HIGH)
**Stale symbol `G` for the guarantor assignments.** 0.8.0 eq. 11.22 is
`M ≡ (P(|κ'|, η'_2, τ'), Φ(κ'))` — `\guarantorassignments = **M**` (`preamble.tex:673`).
`G` in 0.8.0 is the *guarantee* set `𝔾` (`\guarantee = \mathbb{G}`, eq. 11.25
`E_G ∈ ⟦G⟧_{:C}`), so the sentence reads as if de-biasing changed the guarantees extrinsic.

Fix:
- `只要有節點改了 F，它算出的 G 就不同` → `只要有節點改了 F，它算出的 M（eq. 11.22 的 guarantor assignments）就不同`

### F5 · `c3-appF-shuffle-is-consensus` (option 3 + explanation), `c3-appF-seq-from-hash-vs-fallback`, `c3-appG-output-vs-signature` — `EXPLANATION-DEFECT` (LOW–MED)
**Stale symbol `γ_a` for the ticket accumulator; 0.8.0 uses `γ_A`.**
`\ticketaccumulator = \gamma_A` (`preamble.tex:810`); the compiled 0.8.0 text contains
`γA` 16 times and `γa` zero times. This deck already writes `γ_A` everywhere else
(`items/b2_ch06.py` ×12, `items/ch06_safrole.py` ×17) — `c3_appEFGH.py` is the lone outlier,
so this is an internal inconsistency as well as a version-staleness.

Fix — four replacements (`γ_a` → `γ_A` at each):
- option 3 of item 4: `the ticket accumulator γ_a, and since γ_a is re-sorted by identifier`
  → `the ticket accumulator γ_A, and since γ_A is re-sorted by identifier`
- item 4 explanation: `ticket accumulator γ_a 是依 identifier y 排序` → `ticket accumulator γ_A 是依 identifier y 排序`
- item 5 explanation: `γ′_S 在 |γ_a| ≠ E 時` → (see F6 — the whole clause is rewritten)
- item 8 explanation: `γ_a 依 y 排序取最小的 E 個` → `γ_A 依 y 排序取最小的 E 個`
  and `舊 y 進不了新的 γ_a` → `舊 y 進不了新的 γ_A`

### F6 · `c3-appF-seq-from-hash-vs-fallback` — `EXPLANATION-DEFECT` (HIGH)
**Wrong symbol `𝒟_4` for the decoder — and it collides with `𝒟` in this very file.**
`\fndecode = \mathcal{E}^{-1}` (`preamble.tex:180`), so the decoder is `𝓔⁻¹_4`. Meanwhile
`\fnecoriginalshards = \mathcal{D}` — the erasure-coding shard-count function that items 9 and
11 of this same file write as `𝒟`. A student reading both items back to back sees one glyph
meaning two unrelated things. Three occurrences plus one in the "§3 convention" aside.

Fix — four replacements:
- `Q_l(h) = [ 𝒟_4( H(h` → `Q_l(h) = [ 𝓔⁻¹_4( H(h`
- `再以 𝒟_4（little-endian，見 §3 對 E_l/𝒟_l 的約定）` → `再以 𝓔⁻¹_4（little-endian，見 §3 對 E_l/𝓔⁻¹_l 的約定）`
- `F(r,k) = [ k[𝒟_4(H(r ⌢ E_4(i))_{…4})]_b ⟳` → `F(r,k) = [ k[𝓔⁻¹_4(H(r ⌢ E_4(i))_{…4})]_b ⟳`
- `endianness 也不是唯一差異——𝒟_4 兩邊都是 little-endian` → `endianness 也不是唯一差異——𝓔⁻¹_4 兩邊都是 little-endian`

### F7 · `c3-appF-seq-from-hash-vs-fallback` — `EXPLANATION-DEFECT` (MED, over-claim)
**The stated trigger for the fallback is wrong.** Eq. 6.25 has three branches:
`Z(γ_A)` when `e' = e+1 ∧ m ≥ Y ∧ |γ_A| = E`; `γ_S` when `e' = e`; `F(η'_2, κ')` otherwise.
So when `e' = e` the sealer sequence is unchanged *whatever* `|γ_A|` is, and the fallback can
also fire with `|γ_A| = E` (e.g. `m < Y`, or a skipped epoch `e' > e+1`). The claim
「γ′_S 在 |γ_a| ≠ E 時等於 eq. 6.27 的結果」is false as an iff.

Fix:
- `γ′_S 在 |γ_a| ≠ E 時等於 eq. 6.27 的結果` → `γ′_S 只有落到 eq. 6.25 第三支時（跨 epoch 而 Z(γ_A) 的條件不成立，例如 |γ_A| ≠ E 或 m < Y）才等於 eq. 6.27 的結果；同一 epoch 內（e′ = e）γ′_S 一律沿用 γ_S`

### F8 · `c3-appG-why-ring-not-plain-vrf` — `EXPLANATION-DEFECT` (HIGH)
**Stale entry-index letter `r`; 0.8.0 uses `e`.** `\¬entryindex = e` (`preamble.tex:431`);
eq. 6.6 is `T ≡ ⟨y ∈ ℍ, e ∈ ℕ⟩` and eq. 6.30's proof context is `X_T ⌢ η'_2 ⌢ i_e`.

Fix — two replacements:
- `屬於 ⟨γ′_Z, X_T ⌢ η′_2 ⌢ [r], []⟩ 這一族` → `屬於 ⟨γ′_Z, X_T ⌢ η′_2 ⌢ i_e, []⟩ 這一族`
- `每個 entry index r 各自一張 proof` → `每個 entry index e 各自一張 proof`

**Secondary (LOW, over-claim):** both the keyed option and the explanation assert the
DoS/bribery motive ("blunts targeted denial-of-service and bribery" /
「攻擊者無法提前針對某台機器打 DoS 或行賄」). I grepped all of `text/*.tex` for
`sassafras|denial.of.service|bribe|bribery|grinding|adversar`: 0.8.0 states only *anonymity*
(`safrole.tex:8,14`; `notation.tex` §3.8.2) and never gives the attack rationale. It is
standard Sassafras reasoning and no other option is defensible, so the key stands — but the
explanation should attribute it rather than imply the GP says it. Suggested softening:
- `這正是 Safrole 相對 BABE 的賣點：` → `（以下為 Sassafras/Safrole 的公認設計動機，GP 0.8.0 本文只寫到 anonymity，未展開攻擊模型）這正是 Safrole 相對 BABE 的賣點：`

**Nit (LOW):** this item has no `trap` field; every other item in the file except
`c3-appH-what-gets-coded` has one.

### F9 · `c3-appG-ring-root-commitment` — `EXPLANATION-DEFECT` (HIGH)
**Wrong set symbol: `ringroot ⊂ Y_144`.** `\blob = \mathbb{B}` (`preamble.tex:370`), so it is
`ringroot ⊂ 𝔹_144` (`definitions.tex:33`, `notation.tex:169`). `𝕐` is `\avspec` — the
availability-specification set — which items 1, 9 and 10 of this same file discuss.

Fix:
- `都寫明 ringroot ⊂ Y_144` → `都寫明 ringroot ⊂ B_144`

**Secondary (LOW, unverifiable):** 「團隊 #1040/#1041 就是把 verifier 從『以 epoch 為 key』
改成『以 validator-set hash 為 key』」 — no issue/PR data is reachable from this checkout, so I
can neither confirm nor refute it. Same class as item 9's 「PR #1026／#1035…issue #1037」.
Everything GP-sourced in this item is verbatim-correct.

### F10 · `c3-appG-output-vs-signature` — `EXPLANATION-DEFECT` (HIGH)
**Stale entry-index letter `r`, twice.** Eq. 6.32 is `n ≡ [(y ← Y(i_p), e ← i_e) | i ⊰ E_T]`
and eq. 6.16's seal context is `X_T ⌢ η'_3 ⌢ i_e`. (`\st¬id = y` ✓, `\xt¬proof = p` ✓,
`\¬authorbskey = A` ✓ — only the entry index is wrong.)

Fix — two replacements:
- `n = [(y ← Y(i_p), r ← i_r) | i ∈ E_T]` → `n = [(y ← Y(i_p), e ← i_e) | i ∈ E_T]`
- `H_S ∈ ⟨H_A, X_T ⌢ η′_3 ⌢ [i_r], E_U(H)⟩` → `H_S ∈ ⟨H_A, X_T ⌢ η′_3 ⌢ i_e, E_U(H)⟩`

(Plus the `γ_a` → `γ_A` pair listed under F5.)

### F11 · `c3-appH-code-shardcount-080` — `EXPLANATION-DEFECT` (HIGH)
**Eq. 11.31 is misquoted on both letters.** The GP writes
`∀r ∈ I : (r_s)_v = |κ'|`, where `\wrX = **r**` (`preamble.tex:508`) and
`\incomingreports = **I**` (`:677`, "the set of work-reports in the present extrinsic",
eq. 11.30). The deck writes `∀w ∈ W：(w_s)_v = |κ′|`. `W` is not a set in 0.8.0 at all
(work-report set is `ℝ`, work-package set is `ℙ`), and `w` is not a GP bound variable here.
Both the `gpRef` and the explanation body carry it.

Fix — two replacements:
- `eq. 11.31 ((w_s)_v = |κ′|)` → `eq. 11.31 (∀r ∈ I: (r_s)_v = |κ′|)`
- `eq. 11.31 規定 ∀w ∈ W：(w_s)_v = |κ′|` → `eq. 11.31 規定 ∀r ∈ I：(r_s)_v = |κ′|`

**Delta claims in this item are all correct** and I verified them independently: 0.8.0 has
`𝒟(v)` and no `W_E`/`W_P` (the `\mathsf{W}` family is `W_A, W_B, W_C, W_F, W_G, W_M, W_R,
W_T, W_X`, `preamble.tex:276-284`); the avspec really did gain the `v` field, since the
team's 0.7.2 `WorkPackageSpec` has only five (`types.go:533-539`, annotated `p, l, u, e, n`);
`𝒟(6) = 3`, `z = 6`, `k = 684`; and `𝒟(1002) = 228 ≠ 335` is arithmetically right.

### F12 · `c3-appH-what-gets-coded` — `EXPLANATION-DEFECT` (LOW)
Content is fully correct and verbatim-sourced. Two cosmetic issues only: the `Ⅎ(s)` of F2,
and the zero-pad written `P_z` where GP has `𝒫_z`. Also missing a `trap` field.

### F13 · `c3-appH-rate-and-field-rationale` — `EXPLANATION-DEFECT` (LOW, two over-claims)
The three-reason decomposition, the H.1 arithmetic, the `v = 1002` counter-example and the
GF(2¹⁶) evaluation-point argument are all correct. Two soft spots:
- 「這是最根本的理由，速度只是附帶」ranks the GF reasons; §H merely lists "the 16-bit Galois
  field" as one of three considerations and never says which dominates. Suggest
  `這是最根本的理由，速度只是附帶` → `這是最直接的理由（§H 只把 16-bit GF 列為三項考量之一，並未替它們排序）`。
- 「0.8.0 才因為『support smaller validator sets』變成以 v 為參數的函數」puts a phrase in
  quotation marks that does not appear anywhere in `text/*.tex` (grepped). The *substance* is
  right; the quotation marks imply a GP citation that does not exist. Suggest dropping the
  marks: `因為「support smaller validator sets」變成` → `為了支援較小的 validator set 而變成`。

---

### Things I could NOT settle
- **No `DELTA-DEFECT` found, but my coverage of "missed deltas" is incomplete.** There is no
  0.7.2 Gray Paper source in this environment (`gp-src` is a single commit,
  `07f041d Release version 0.8.0`), so I could only corroborate deltas indirectly, via the
  team's 0.7.2 Go tree. Every delta the deck asserts checks out that way; I cannot certify
  that no *other* E/F/G/H change between 0.7.2 and 0.8.0 was missed.
- **Team PR/issue numbers** (`#1026/#1035/#1037` in item 9, `#1040/#1041` in item 7) are not
  verifiable from this checkout.
- **The DoS/bribery rationale** in item 6 is absent from 0.8.0's `.tex`; I am flagging it as
  an unsourced (though conventional) inference rather than an error.

---

### Fix-application note
All 27 `old` substrings proposed above were checked with a `str.count()` pass against
`items/c3_appEFGH.py`: **each occurs exactly once**, so every replacement is unambiguous and
order-independent. No file under `items/` was modified by this review.
