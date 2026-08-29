# G4 (ch11 Reporting & Assurance, ch12 Accumulation) — adversarial verdicts vs GP 0.8.0 LaTeX

ch11-rho-pipeline-worked | OK | 
ch11-guarantee-slot-window-calc | OK | 
ch11-rotation-epoch-boundary-mstar | OK | 
ch11-code-permute-080 | SUSPECT | code snippet is truncated mid-statement (`base := make(...)` then a bare `for i`), so the `⌊C·i/V⌋` base that the marked answer's whole contrast rests on is never shown to the candidate; only the `% CoresCount` rotation is visible. Answer content itself is right (0.8.0 eq. 11.20 rotates mod |c|/3; eq. 11.21 base is [⌊i/3⌋]; ⌊341·i/9⌋ = [0,37,75,113,151,189,227,265,303] verified).
ch11-code-anchor-checks-080 | SUSPECT | code snippet truncated at `// xb = yb` — the lookup-anchor block of the team's function is not shown at all, yet half the marked answer ("lookup anchor: h′_p = H(h) … h′_r = l_s") is a claim about what is missing from code the candidate cannot see. Also the anchor set is β_H† (recent-history component), not β†. Content of option 1 matches eq. 11.36 (x_a=y_h ∧ x_s=y_s ∧ x_b=y_b ∧ x_n=y_t) and eq. 11.38 (h_t=x_t ∧ H(h)=x_l ∧ h′_p=H(h) ∧ h′_r=x_r).
ch11-lookup-anchor-ancestry | SUSPECT | GP half is right and only option 2 is defensible, but the fuzzer half is not checkable against the GP and is at best partial: eq. 11.38 in 0.8.0 also requires h′_r = x_r (the lookup anchor's posterior state root, read off the CHILD header), which a `(slot, header hash)` ancestry list cannot supply — GP says A is "the series of the last L headers", i.e. full headers. "Initialize"/"mandatory M1 feature" are fuzzer-protocol claims outside the GP (the team repo's own message is `SetState{Header, State, Ancestry}`, `AncestryItem{Slot, HeaderHash}`).
ch11-prerequisite-window | OK | 
ch11-code-hash-prediction | OK | 
ch11-assurance-bitfield-packing | OK | 
ch11-inactive-core-set-shrink | SUSPECT | verdict and primary reason are correct (|κ′|/3 = 3 so core 3 is inactive; GP: "Use of an inactive core is not permitted even if a timeslot in the previous rotation is used and the core was active then"), but the option's secondary clause "(w_s)_n must equal |κ′|" names the wrong field: eq. 11.31 is (w_s)_v = |κ′|; in 0.8.0 (w_s)_n is the SEGMENT count.
ch11-rho-state | OK | 
ch11-workreport-fields | SUSPECT | stem's tuple uses 0.7.x letters. GP 0.8.0 eq. 11.2 is W ≡ (s, **c**, c, a, **t**, **l**, **d**, g): the refinement context is bold **c** (not x) and the authorizer trace is bold **t** (not o). Positional mapping still makes option 2 (g = is-authorized gas, not refine gas) the unique correct answer.
ch11-refinement-context | SUSPECT | 8 fields and their meanings are right, but the letters are not GP 0.8.0. Eq. 11.4 is X ≡ (a, n, s, b, l, t, r, **p**): the ANCHOR timeslot is n, the lookup-anchor timeslot is t, the lookup-anchor posterior state root is r. The option's "t / l_t / l_s" are quiz shorthand, not GP symbols.
ch11-avspec | WRONG | GP 0.8.0 eq. 11.5 is s ≡ (p, l, u, v, e, n) — the erasure-shard count is **v** and **n** is the SEGMENT count; there is no k. GP: "the tuple of the work-package's hash p, an auditable work bundle length l …, together with an erasure-root u, the total number of erasure-coded chunks v, a segment-root e and segment-count n" (§11.2.3), and eq. 11.31 reads (w_s)_v = |κ′|. So the stem's "(h, l, u, n, e, k)" and the marked "n = number of erasure shards … k = segment count" both misname fields; correct answer text should read "u = erasure root; v = erasure-shard count, which must equal |κ′|; e = segment root; n = segment count". Substance (roles of the four values) is otherwise correct.
ch11-work-errors | SUSPECT | all six meanings are exactly right per §11.2.4, but the error set is 𝔼 in 0.8.0 (`\workerror = \mathbb{E}`), not J — and 𝕁 is now the SEGMENT set, so calling it J actively mis-teaches.
ch11-report-size-limit | SUSPECT | minor: the limit and value are right (eq. 11.8–11.10, W_R = 48·2^10 = 49,152, errors contribute 0 via L), but the authorizer trace is field **t** in 0.8.0, not o.
ch11-assurance-rules | OK | 
ch11-availability-threshold | OK | 
ch11-guarantor-assignment | OK | 
ch11-guarantee-validity | OK | 
ch11-report-checks-state | OK | 
ch11-contextual-validity | OK | 
ch11-rho-prime | OK | 
ch11-code-availability | OK | 
ch12-history-queue-state | SUSPECT | the question is literally "what are ξ and ϑ", but ϑ is not a GP 0.8.0 symbol: eq. 12.3 defines the ready/accumulation queue as **ω** (`\ready = \omega`), and its element type is the work-report set ℝ (not 𝕎). Types and semantics as stated are correct (ξ ∈ [{ℍ}]_E, ω ∈ [[(ℝ,{ℍ})]]_E).
ch12-W-partition | SUSPECT | mechanism, ordering and pruning are exactly eq. 12.4–12.12, but the formula is written in 0.7.x symbols: the newly-available sequence is **R** (`\justbecameavailable = \mathbf{R}`), so R!, R^Q, R*; and the queue is ω, so q = E(⌢ω[m…] ⌢ ⌢ω[…m] ⌢ R^Q, P(R!)).
ch12-gas-budget | OK | 
ch12-delta-star | OK | 
ch12-delta-one-gas | OK | 
ch12-deferred-transfer | OK | 
ch12-outputs | SUSPECT | δ‡‡ is not a GP symbol. 0.8.0 uses δ† = post-accumulation (eq. 12.26, destructured from e′), δ‡ = δ† with a_a = τ′ for every s ∈ keys(S) (eq. 12.29–12.30), δ′ = post-preimage. So the option's "(δ‡ …) come from e′" should be δ†, and "δ‡‡ marks a_a = τ′" should be δ‡. Everything else (θ′ = the ⟨s,h⟩ pairs of b, S = (N items, T transfers, G gas), ξ′[E−1] = P(R*[…n])) is correct.
ch12-preimage-integration | SUSPECT | same dagger shift: eq. 12.37 is δ′ = I(δ‡, E_P), not I(δ‡‡, E_P). All other clauses check out (eq. 12.34–12.36 ordering/uniqueness, providability Y against the PRIOR δ with δ[s]_l[(H(d),|d|)] = [], and I setting a_l[(H(d),|d|)] = [τ′], a_p[H(d)] = d; GP: "We disregard, without prejudice, any preimages which due to the effects of accumulation are no longer useful").
ch12-code-outer-accumulation | OK | 

## Notes

**Arithmetic re-done independently (all confirmed).**
- `ch11-rho-pipeline-worked`: U = 5 (definitions.tex). Threshold is strict, > 2/3·|κ| = > 4, so neither 4 (slot 42) nor 3 (slot 45) makes the report available — assurance counts are per-block, they do not accumulate across blocks. Timeout in eq. 11.18 is `H_t ≥ p_t + U`, so at H_t = 45, 45 ≥ 40 + 5 fires and ρ‡[0] = ∅; eq. 11.32 then admits g₂ and eq. 11.46 gives ρ′[0] = (g₂, 45). g₁'s report never enters R, so it never accumulates. Only option 0 survives.
- `ch11-guarantee-slot-window-calc`: R·(⌊57/10⌋ − 1) = 10·4 = 40, so t ∈ [40, 57]. ⌊57/10⌋ = 5; t ∈ [50,57] → M (rotation index 5), t ∈ [40,49] → M* (P(|κ′|, η′₂, 47), rotation index ⌊47/10⌋ = 4, same epoch so κ′/η′₂). t = 39 and t = 58 rejected.
- `ch11-rotation-epoch-boundary-mstar`: ⌊603/10⌋ = 60 ≠ ⌊595/10⌋ = 59 → M*. ⌊593/600⌋ = 0 ≠ ⌊603/600⌋ = 1 → (λ′, η′₃). P(|λ′|, η′₃, 593) has rotation index ⌊593/10⌋ = 59. Window 10·59 = 590 ≤ 595 ≤ 603 holds, so the slot itself is legal — the item's point stands.
- `ch11-inactive-core-set-shrink`: |κ′| = 9 ⇒ |κ′|/3 = 3, so cores 0–2 only; core 3 fails eq. 11.28's `c_v = w_c < |κ′|/3` even under M*. |κ| = 12 ≠ |κ′| = 9 clears all of ρ‡ (eq. 11.18). 𝕍 = {3c | c ∈ N_{2…C+1}} (eq. 6.8), so 6/9/12 are all legal set sizes and |κ|/3 is always integral.
- `ch11-assurance-bitfield-packing`: ⌈341/8⌉ = 43 octets; core 340 → octet ⌊340/8⌋ = 42, bit 340 mod 8 = 4; App. C packs "in order of least significant to most" (Σ b[i]·2^i) so that octet is 0x10, and the length prefix applies only "in the case of a variable length sequence" — b_C is fixed-length, so none. Signed message is X_A ⌢ H(E(H_p, f)) = X_A ⌢ H(32 + 43 = 75 octets).
- `ch11-code-availability`: |κ| ∈ 𝕍 is always a multiple of 3, so 2|κ|/3 is an integer and `> 2|κ|/3` ⟺ `≥ ⌊2|κ|/3⌋ + 1` exactly; 6 → 5, 1023 → 683. Option 0's equivalence claim holds.
- `ch12-gas-budget` / `ch12-code-outer-accumulation`: g = max(G_T, G_A·C + Σ values(χ_Z)) with G_T = 3,500,000,000, G_A = 10,000,000, C = 341; eq. 12.17's budget test is Σ d_g + Σ t_g + Σ values(f) ≤ g, n = i + |t| + |f|, g* = g + Σ_{t∈t*} t_g − Σ_{(s,u)∈u*} u, recursing with an empty f. G_R = 5,000,000,000 (\Cpackagerefgas) is a real constant, so option 3 there is a fair distractor.

**Systematic issue: the set is written in GP 0.7.x notation in several places.** The quiz gets the ρ-pipeline daggers (ρ†/ρ‡/ρ′), M/M*, A, ξ, χ_Z, θ, β and the service-account field letters (a_a, a_l, a_p, δ[s]_g, δ[s]_c) right, but consistently uses five symbols that 0.8.0 renamed:
| quiz | GP 0.8.0 | where |
|---|---|---|
| W (newly available reports) | **R** | 205, 212, 213, 218 |
| ϑ (ready queue) | **ω** | 122, 209, 212, 213 |
| 𝕎 (work-report set) | ℝ | 212 |
| J (work-error set) | 𝔼 (𝕁 is now the segment set) | 202 |
| δ‡ / δ‡‡ | δ† / δ‡ | 218, 219 |
plus the per-field letters flagged above (work-report x→**c**, o→**t**; avspec n→v, k→n; refinement context anchor-time→n, lookup-anchor time→t, lookup-anchor state root→r; guarantee w→**r**). None of these flip which option is correct, but a candidate memorising the answers will write down field names that do not exist in 0.8.0. Worth a single pass over the whole bank.

**Genuine GP ambiguities / judgement calls (not errors in the items).**
- eq. 11.28 writes the guarantee signature message as `X_G ⌢ H(r)` with no explicit E, even though H is defined only over 𝔹 (notation §3: "a function H(m ∈ 𝔹) ∈ ℍ"). `ch11-guarantee-validity`'s "X_G ⌢ H(E(w))" is the right reading of that shorthand, and it is consistent with how eq. 11.14 writes the assurance signature (H(E(H_p, f))) explicitly.
- eq. 12.18 evaluates Δ₁ for χ_A[c], χ_V and χ_R even when those services are not in **s**. `ch12-delta-star`'s "each is accumulated exactly once via Δ₁" is about the members of **s** and is fine, but the GP is silent about the extra evaluations.
- Two items lean on non-GP artefacts. `ch11-lookup-anchor-ancestry` depends on the conformance fuzzer protocol (see its line above), and several stems/options quote JAM test-vector error names (`core_engaged`, `dependency_missing`, `bad_code_hash`) that appear nowhere in the Gray Paper. The error names are harmless colour but should not be presented as GP terminology.
- Section/appendix references check out: reporting_assurance = §11, accumulation = §12; appendices run A = PVM, B = PVM invocations (the `transfer` host call Ω_T is there), C = serialization, so `App. C bit-sequence encoding` and `B.transfer` are both correct. All equation numbers cited in gpRef are plausible against the LaTeX row counts (11.16 = the ρ†[c] ≠ ∅ precondition, 11.17 = R, 11.18 = ρ‡, 11.31 = shard count, 11.32 = core unused, 11.33 = gas, 11.36 = anchor, 11.37 = L bound, 11.38 = ancestor set, 11.42 = prerequisites, 11.45 = code hash, 11.46 = ρ′; 12.1–12.3, 12.4–12.12, 12.14, 12.17–12.19, 12.23, 12.24–12.33, 12.34–12.37).
