# G2 / Chapter 6 (Safrole) — adversarial verdicts vs GP 0.8.0

Ground truth: `gp-src/text/safrole.tex` (+ `header.tex`, `definitions.tex`, `bandersnatch.tex`,
`notation.tex`), cross-checked against the rendered `graypaper-0.8.0.pdf`.
Equation numbering for §6 was rebuilt by counting numbered rows (labelled ones match `eqref.py`):
6.9–6.13 = validator-key layout, 6.14 = key rotation, 6.19–6.21 = X_E/X_F/X_T, 6.23 = η′_0,
6.24 = η history, 6.26 = Z, 6.32 = n, 6.33 = order/unique, 6.34 = disjoint, 6.35 = γ′_A, 6.36 = n ⊆ γ′_A.
All of these were confirmed verbatim in the PDF.

ch06-code-useless-ticket-gap | OK | 
ch06-code-attempt-cap-v080 | OK | 
ch06-code-header-checks-posterior | OK | 
ch06-code-author-index-bound | OK | 
ch06-skip-epochs-transition | OK | 
ch06-variable-set-boundary | OK | 
ch06-ring-root-nulled-keys | OK | 
ch06-vrf-output-message-independence | OK | 
ch06-why-m-ge-Y | OK | 
ch06-three-keys-epoch-marker | OK | 
ch06-gamma-components | OK | 
ch06-key-rotation | OK | 
ch06-valcount | OK | 
ch06-validator-key-layout | OK | 
ch06-entropy-update | OK | 
ch06-which-eta-where | OK | 
ch06-seal-ticket-condition | OK | 
ch06-slot-sealer-cases | OK | 
ch06-outside-in-Z | OK | 
ch06-fallback-F | OK | 
ch06-epoch-marker | OK | 
ch06-winning-tickets-marker | OK | 
ch06-ticket-extrinsic-limits | SUSPECT | marked option 0 is internally inconsistent: it fixes E via "m′ < Y = 500" (so E = 600) and then says n = ⌈2E/|γ′_P|⌉ is "4 for a tiny set of 6". With the GP's E = 600 and |γ′_P| = 6 the value is ⌈1200/6⌉ = 200; the 4 only follows from the non-GP tiny config (E = 12). Fix: say "4 in the tiny config (E = 12, V = 6)" or drop the parenthetical. Everything else in option 0 is exact (6.30, 6.31) and no distractor is defensible, so the keyed answer is still the only right one.
ch06-ticket-accumulator-rules | SUSPECT | the FALSE-statement key (option 3, "keeps the highest E entries") is unambiguously false and correct as the answer, but option 2's parenthetical "a useless (too-high-scoring) ticket" inverts the GP's own score convention — §6 intro: "The tickets with the best scores are then selected", §6.2: "γ_A is the ticket accumulator, a sequence of highest-scoring ticket identifiers", while 6.35/§6.7 keep "the lowest items of the sorted union". A dropped ticket therefore has a LOW score (high id). A careful reader can argue option 2 is also false. Reword to "too-high-id" / "lowest-scoring".
ch06-ticket-proof-context | OK | 
ch06-seal-fallback | OK | 
ch06-code-slot-key-sequence | OK | 
ch06-code-fallback-hash | SUSPECT | option 0's blanket "It conforms" is over-broad for 0.8.0. Eq. 6.27 reduces the index modulo the length of the passed key sequence (`⌞k[D_4(H(r ⌢ E_4(i))_…4)]⌟↺` — cyclic subscription is defined in §3.7 as `s[i mod |s|]`), i.e. mod |κ′|. The team's `FallbackKeySequence` does `validatorIndex %= types.U32(types.ValidatorsCount)` — a global constant, not `len(validators)`. That is exactly the prior-vs-posterior/constant-vs-actual defect that ch06-code-author-index-bound marks as NON-conformant, so the two items grade the same pattern differently. It is still the only defensible option (1, 2, 3 are all refuted by the GP text itself), and the modulo line is not visible in the 400-char code excerpt.
ch06-code-entropy-order | OK | 

## Notes

**1. Entry-index subscript is `e` in 0.8.0, not `r`.** GP 0.8.0 eq. 6.6 reads `T ≡ {y ∈ H, e ∈ N}` and
eq. 6.16 reads `H_S ∈ V_{H_A}^{E_U(H)}⟨X_T ⌢ η′_3 ⌢ i_e⟩`; eq. 6.30/6.32 likewise use `e` for the
extrinsic entry index (`\¬entryindex` is defined as `e` in `preamble.tex:431`). The quiz consistently
uses the 0.7.x letter `r` (`i_r`, `++ r`) in ch06-vrf-output-message-independence, ch06-which-eta-where,
ch06-seal-ticket-condition, ch06-ticket-extrinsic-limits and ch06-ticket-proof-context. The referent is
never ambiguous (every option spells out "entry index"), and the GP's own choice of `e` collides with the
epoch index `e` used throughout §6 — which is presumably why the author kept `r` — so this changes no
answer. Flagging only because the set advertises 0.8.0 fidelity.

**2. Header timeslot is `H_T` in 0.8.0.** The quiz writes `H_t` throughout (`γ′_S[H_t mod E]`). Cosmetic.
Note also that eq. 6.16/6.17 use cyclic subscription `γ′_S[H_T]↺`, i.e. `mod |γ′_S|`; "mod E" is right
only because |γ′_S| = E by eq. 6.5 — which it always is.

**3. The `code` field is hard-truncated at exactly 400 characters** in this review export, cutting five
excerpts mid-token: ch06-code-useless-ticket-gap (cut before the `[:E]` truncation that option 1 names),
ch06-code-attempt-cap-v080 (cut at `n := (2*types.EpochL`, i.e. before the ceiling expression AND before
the `>=` comparison that options 0 and 3 argue about), ch06-code-header-checks-posterior,
ch06-code-slot-key-sequence, ch06-code-fallback-hash (cut before the `%=` line that options 0 and 3
argue about). In every case the GP alone still refutes the three distractors, so no answer changes — but
if this truncation is present in the quiz as delivered, the two worst (useless-ticket-gap, attempt-cap,
fallback-hash) ask about code the candidate cannot see. Verify against the source JSON.

**4. "Tiny" parameters are not GP constants.** E = 12 / V = 6 (used by ch06-variable-set-boundary,
ch06-code-attempt-cap-v080, ch06-ticket-extrinsic-limits) come from the JAM test-vector chainspec, not
the Gray Paper, whose only values are E = 600, Y = 500, K = 16, C = 341 (⇒ 3C = 1023),
P = 6 (`definitions.tex:261-294`). Fine for an implementation-flavoured quiz, but tiny values must always
be introduced explicitly in the stem, as ch06-variable-set-boundary correctly does and
ch06-ticket-extrinsic-limits does not.

**5. Genuine GP looseness — what γ′_P/H_E "define".** §6.6 says the epoch marker holds keys "defining the
validator keys beginning in the next epoch", and §6.3 says γ_P "will be active in the next epoch". Read
from a block that has just started epoch e+1, γ′_P actually becomes κ at the start of epoch **e+2**.
ch06-gamma-components and ch06-epoch-marker both use the GP's own loose phrasing ("pending validators for
the next epoch"), so they are consistent with the source; a pedantic candidate could object to either.
No change recommended — the options match the GP verbatim.

**6. ch06-why-m-ge-Y answer requires one unstated step.** Option 2's claim ("m ≥ Y is exactly the
condition under which H_W = Z(γ_A) was published in that epoch") is true, but only in conjunction with the
other two conjuncts of 6.25: γ_A resets on every epoch change and can only grow while m′ < Y (6.31, 6.35),
so |γ_A| = E at the boundary forces a pre-tail block in epoch e, hence a first tail-crossing block with
m < Y ≤ m′ and a then-frozen saturated accumulator, hence H_W by 6.29. The GP never states this
implication; it is a (correct) derivation. Acceptable for a hard item, worth knowing when defending it.

**7. Repo metadata is unverifiable from the GP.** "PR #514" (ch06-valcount), "since GP 0.6.4"
(ch06-three-keys-epoch-marker), "#784/#791" (ch06-code-header-checks-posterior), "#825/#1037"
(ch06-code-author-index-bound), "PR #1025 / branch 1012-update-to-v080" (ch06-code-attempt-cap-v080),
"identical on main and on the 0.8.0 branch" (ch06-code-useless-ticket-gap). None affect correctness and
all are consistent with `research/code-map.md §3.2`, but none were checkable against the primary source.

**8. Everything else verified positively**, including the cross-chapter references: 5.10
(`H_I ∈ N_{|κ′|}, H_A ≡ κ′[H_I]_b`), 5.11 (marker types), 11.14/11.28 (Ed25519 assurance/guarantee sigs),
11.22 (`M ≡ (P(|κ′|, η′_2, τ′), Φ(κ′))` — the η′_2 shuffle), 17.3 (Bandersnatch audit-selection VRF),
17.7 (Ed25519 audit announcement), 18.1 (BLS BEEFY — the only BLS use in the whole paper),
G.2/G.5 (`Y(·)` for signature and ring proof), G.3 (`O(⟦H̄⟧) ≡ commit(·)`) and the App. G padding-point
note. §3.8.2 confirms the VRF output is "influenced by x but not by m", which is what
ch06-vrf-output-message-independence turns on. Appendix letters: A pvm, B pvm-invocations,
C serialization, D state-merklization, E general-merklization, F shuffling, **G bandersnatch**,
H erasure coding — so the "App. G" references are right (merklization.tex carries two `\section`s).
