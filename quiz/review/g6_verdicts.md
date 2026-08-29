# G6 (Appendix B — PVM Invocations & host calls) — adversarial verdicts vs GP 0.8.0 LaTeX

appB-result-constants | OK | 
appB-three-invocations | OK | 
appB-host-call-indices | OK | 
appB-accumulate-invocation | NOTATION | context pair written `X` / `Y` → GP 0.8.0 is lowercase bold **x** / **y** (`\imX = \mathbf{x}`, `\imY = \mathbf{y}`, preamble 460–461; §B.4 prose: "one dimension … generally named x and the other … being named y"). Substance of option 0 is exact.
appB-new-service-index | NOTATION | `H_t` → `H_T` (`\¬timeslot = T`, preamble 743; eq. B.10 reads `check((decode_4(H(E(s, η′_0, H_T))) mod (2^32 − S − 2^8)) + S)`). Everything else in option 0 (S = 2^16, +1 probe, +42 bump, registrar/FULL, gratis/HUH, CASH) is verbatim eq. B.10/B.14 and Ω_N.
appB-transfer-rules | OK | 
appB-solicit-forget | OK | 
appB-bless-assign-designate | OK | 
appB-fetch | OK | 
appB-checkpoint-yield | NOTATION | `X` / `Y` → **x** / **y** (same as appB-accumulate-invocation). Ω_C (y′ ≡ x, ω′_7 ≡ ϱ′), Ω_♉ (yield) and Ω_♈ (provide) semantics in option 0 are all correct.
appB-host-gas-costs | OK | 
b2-appB-write-prev-length-full | OK | 
b2-appB-read-cross-service-pure | OK | 
b2-appB-unknown-hostcall-oog | NOTATION | "the checkpointed context `Y`" → **y** (eq. B.13, collapse function C). Arithmetic and the ∞ collapse are right: M_∅ = 1000 (App. I), 300 − 1000 = −700 < 0 → ∞ → C selects the y-dimension.
b2-appB-invoke-gas-refund | OK | 
b2-appB-pages-access-modes | SUSPECT | option 1's closing clause "the WHO-before-HUH ordering matches the GP" is a claim about code the candidate cannot see: the excerpt starts at the `r > 4 || p < 16 || …` HUH test with no leading elision marker and no `n ∈ keys(m)` test, and its second HUH test indexes `IntegratedPVMMap[n]` directly (a Go map lookup that silently yields a zero struct for an absent n). Read literally, the excerpt shows HUH *before* WHO — the opposite of what the option asserts. The two real gaps (r = 0 must zero-fill + set inaccessible; r ∈ {3,4} must preserve contents) are exactly right and only option 1 is defensible.
b2-appB-info-layout-calc | OK | 
b2-appB-query-encoding-calc | OK | 
b2-appB-grow-heap | NOTATION | gpRef writes `Ω_Γ` and `M_Γ,c / M_Γ,p`; the GP macro is `\Gemini` (mathabx zodiac ♊), i.e. Ω_♊ and M_♊,c / M_♊,p (preamble 292–293). Confined to the gpRef metadata — the stem and all four options are clean, and every number checks out.
b2-appB-eject-conditions | OK | 
b2-appB-log-jip1 | OK | 

## Notes

**Everything below was re-derived from the LaTeX before looking at the marked answer.**

### Host-call table re-read end to end (§B.5–B.7)
Indices: `gas` 0, `grow_heap` 1, `fetch` 2, `lookup` 3, `read` 4, `write` 5, `info` 6 (§B.5 General Functions); `historical_lookup` 7, `export` 8, `machine` 9, `peek` 10, `poke` 11, `pages` 12, `invoke` 13, `expunge` 14 (§B.6 Refine Functions); `bless` 15, `assign` 16, `designate` 17, `checkpoint` 18, `new` 19, `upgrade` 20, `transfer` 21, `eject` 22, `query` 23, `solicit` 24, `forget` 25, `yield` 26, `provide` 27 (§B.7 Accumulate Functions). Matches `appB-host-call-indices` option 0 exactly, `grow_heap = 1` included. There is no `compile` host call and no `log` host call anywhere in the GP source (`grep -rn "texttt{log}"` → nothing), so both distractor families are safely false.

Invocation host sets (eq. B.2 / B.6 / B.11) match `appB-three-invocations` option 0 exactly: Ψ_I = {gas, grow_heap, fetch}; Ψ_R = {gas, grow_heap, fetch, historical_lookup, export, machine, peek, poke, pages, invoke, expunge} (11); Ψ_A = {gas, grow_heap, fetch, read, write, lookup, info, bless, assign, designate, checkpoint, new, upgrade, transfer, eject, query, solicit, forget, yield, provide} (20). All three default branches are identical: `ω′_7 = WHAT`, `ϱ′ = ϱ − M_∅`, then `∞ if ϱ′ < 0`.

### Numbers independently recomputed (all confirmed)
- **gas constants** (App. I = `definitions.tex`): M_G = 48, M_C = 103, M_T = 575, M_N = 3855, M_E = 3521, M_{L,c} = 600 / M_{L,ℓ} = 248, M_{W,c} = 2442 / M_{W,k,ℓ} = 3358 / M_{W,v,ℓ} = 216, M_K = 968, M_∅ = 1000, M_♊,c = 275 / M_♊,p = 121, M_{Z,a,c} = 275 / M_{Z,a,p} = 121, M_{Z,f,*} = 212/118, M_{Z,s,*} = 130/29, M_{Z,i} = 80. Every figure quoted in `appB-host-gas-costs` and `b2-appB-grow-heap` is right, and eq. B.17 really is `memgas(L, ℓ) = ⌈L·ℓ/1024⌉`.
- **`grow_heap`**: a = (2·Z_Z + rnq(|o|))/Z_P = (2·2^16 + 0)/2^12 = **32** ✓; h = a + c = 40; g = 275 + (50 − 40)·121 = **1,485** ≤ ϱ = 2,000 → ω′_7 = 50, access[a…50) = W. The ω_7 ≤ h ∨ ω_7 > b branch charges only M_♊,c = 275 and returns h = 40. `sbrk` no longer appears anywhere in the 0.8.0 source, so the stem's framing holds.
- **`info` record** (Ω_I): E(a_c, E_8(a_b, a_t, a_g, a_m, a_o), E_4(a_i), E_8(a_f), E_4(a_r, a_a, a_p)) = 32 + 40 + 4 + 8 + 12 = **96** octets. a_g occupies [48, 56), a_m occupies **[56, 64)** — so ω_9 = 56 / ω_10 = 8 does select a_m, and ω′_7 = |v| = 96, not 8 and not OK. Option 0's "a_g … octets [56,64)" is doubly wrong, which is a clean distractor.
- **`query`**: a = [x, y] → ω′_7 = 2 + 2^32·x = 2 + 429,496,729,600 = **429,496,729,602**, ω′_8 = y = 250. The `[x]` row gives 1 + 2^32·x and the `[x,y,z]` row gives 3 + 2^32·x with ω′_8 = y + 2^32·z, so distractors 1 and 2 are the right kind of near-miss.
- **`eject` footprint**: a_i = 2·|a_l| + |a_s| = 2 for one request and no storage; a_o = 81 + z, so l = max(81, a_o) − 81 = z (eq. 9.8 group). Codehash test is `d_c ≠ E_32(x_s)` (a *serialized service index*, not "the same code"), status must be exactly `[x, y]` with y < t − D, D = 19,200.
- **`transfer` precedence** (Ω_T) is literally panic → WHO → LOW → CASH → OK, with g = M_T + t and t = l only in the OK row; balance test is `b = a_b − amount < a_t`. `appB-transfer-rules` option 0 reproduces this in order.

### gpRef / section numbering audit
Appendix letters: A = PVM, B = VM Invocations, C = Serialization Codec, D = State Merklization, **E = General Merklization** (`merklization.tex` carries two `\section`s), F = Shuffling, G = Bandersnatch VRF, H = Erasure Coding, **I = Index of Notation**. So every "App. I" gas-constant reference in this batch is correct — I checked this specifically because an off-by-one here would have invalidated three items.

Equation numbers were recomputed by counting numbered `align` rows per section: B.1 Ψ_I, B.2 F_isauth, B.3 D ≡ A + 4,800 = 19,200, B.4 innerpvm 4-tuple, B.5 Ψ_R, B.6 F_refine, B.7 𝕃, B.8 x_s, B.9 Ψ_A, B.10 I, B.11 F_acc, B.12 G, B.13 C, B.14 check, B.17 memgas; and A.42 = `eq:conditions` (the Y-initialization conditions). Every gpRef in this batch lands on the right equation, including `eq. B.17 (memgas)`, `eq. B.3 (D)`, `eq. B.4`, `eq. B.11–B.12 (F, G)`, `eq. B.13 (C)` and `eq. A.42`. Subsection refs §B.1 / §B.5 / §B.6 / §B.7 are all correct too.

### Notation checked against `preamble.tex`
Correct as written in the items: a_c/a_b/a_t/a_g/a_m/a_o/a_i/a_f/a_r/a_a/a_p and **a_l** for the request-status dictionary (569–583); χ_M manager, χ_A assigners, χ_V delegator (780–784); φ authorizer queue (792), ι staging set (815); B_I / B_L / B_S deposits (251–253); D = 19,200, S = 2^16, Q = 80, Z_P = 2^12, Z_Z = 2^16, W_C, W_T; ☇ = panic, ∞ = OOG, ħ = host; θ = Accumulation Output Log (790, `recent_history.tex` 28–30 confirms the BEEFY path); **e** for the partial state, so `Ψ_A(e, t, s, g, i)` in the stem is right.

Three slips found, all cosmetic and none flipping an answer:
1. **X / Y for the context pair** — four items (`appB-accumulate-invocation`, `appB-checkpoint-yield`, `b2-appB-unknown-hostcall-oog` in the keyed option; `b2-appB-write-prev-length-full` in distractor 3). GP is **x** / **y** throughout.
2. **H_t → H_T** in `appB-new-service-index`.
3. **Ω_Γ / M_Γ → Ω_♊ / M_♊** in `b2-appB-grow-heap`'s gpRef. This one is close to unavoidable in plain text — ♊ has no ASCII form — so treat it as a transliteration note rather than a defect. If the bank wants consistency, `Ω_Gemini` reads better than `Ω_Γ` (Γ is not otherwise used in the GP and invites confusion).

### Judgement calls, deliberately *not* marked as errors
- `appB-accumulate-invocation` says "entry **5**". Eq. B.9 does write `Ψ_M(a_code, 5, g, …)`, but Ψ_M's second parameter is the initial *instruction counter* (`ı ∈ pvmreg`, App. A Ψ_M), not the entry-point index — and §9.1 numbers the entry points 0 = refine, 1 = accumulate. "entry 5" is therefore GP-literal but collides with the §9.1 numbering; a candidate who memorises it may answer "accumulate is entry point 5". Consider rewording to "initial pc = 5". Ψ_I and Ψ_R both pass 0, which sharpens the collision.
- `appB-fetch` option 0 annotates selector 1 as "η′_0 (in accumulate)". App. I calls case 1 "entropy" and eq. B.11 passes η′_0, so that is right — but eq. B.6 passes **H_0** (the zero hash) for the same selector in refine, so selector 1 is *available* in Ψ_R with a different meaning. The parenthetical covers this adequately; flagging only so it is not "fixed" the wrong way.
- `appB-solicit-forget` attaches "(FULL if the new footprint is unaffordable)" only to the "no entry → []" branch. Ω_S applies the `a_b < a_t` test to both branches (it just cannot bite on the `[x,y] → [x,y,t]` branch, which does not change the footprint). Also neither `solicit` nor `forget` mentions the `z ∉ 𝔹_len → HUH` guard that precedes everything. Both omissions are harmless for answer selection.
- **Claims outside the stated ground truth.** `appB-fetch` ("the same encoding JIP-4 uses for protocol_parameters"), `appB-host-call-indices` ("log 100 (JIP-1)"), `b2-appB-log-jip1` in full, and the fuzzer-bug narratives in `b2-appB-write-prev-length-full` (#979/#980), `b2-appB-read-cross-service-pure` (#938), `b2-appB-unknown-hostcall-oog` (#992) and `b2-appB-host-gas-costs` (PR #517) cannot be verified against the Gray Paper. For `b2-appB-log-jip1` this is structural, not incidental: the GP defines nothing at index 100, so the *only* GP-checkable content is that `ecalli 100` falls through the default branch of F to `ω′_7 = WHAT` + M_∅ with no panic — which is exactly what option 2 asserts, and which makes options 0, 1 and 3 false on GP grounds alone. The item survives, but it is a JIP item wearing an Appendix B label.
- `b2-appB-invoke-gas-refund`: the marked answer bundles two things — `g = M_K + g_R` with the `ϱ′ = ϱ − g + g_R′` refund, and the inner machine's gas-charged flag. Only the flag (and M_K replacing the flat 10) is genuinely *new* in 0.8.0; the up-front-plus-refund shape already existed. The stem asks "which GP 0.8.0 rule is missing from it", and the excerpt touches the outer ϱ nowhere at all, so the whole clause is missing and option 3 stands as the unique answer. Options 0 and 1 are each false twice over (eq. B.6/Ω_K reports HOST × h outward, and sets `m*[n]_pc = i′ + skip(i′) + 1` on a HOST exit — which the code shown actually implements correctly).

### Distractor-defensibility sweep
I tried to defend every distractor in all 21 items. Nothing survived. The near-misses worth recording: `b2-appB-pages-access-modes` option 0 gets the access mapping (0 → none, 1/3 → R, 2/4 → W) exactly right and fails only on "zero-fills for every r" (Ω_Z zero-fills iff r < 3); `b2-appB-query-encoding-calc` option 2 is the correct formula with x and the status code transposed; `b2-appB-info-layout-calc` option 1 is right about the datum and wrong only about ω′_7 (8 vs 96); `appB-accumulate-invocation` option 2 would have been correct in 0.6.x — Ψ_T / `on_transfer` is gone in 0.8.0 (no occurrence in the source), transfers arrive as `𝕏 ∪ 𝕋` operands read through `fetch` selectors 14/15.
