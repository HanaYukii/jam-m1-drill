# g1_ch03_05_07_08 — adversarial verification against GP 0.8.0 LaTeX source

ch03-sequence-set-subscripts | OK | 
ch03-first-last-n-arrows | OK | 
ch03-bits-msb-first-trie | OK | 
ch03-vrf-signature-notation | SUSPECT | Cosmetic/stale-version misquote in the stem; answer (option 1) is correct and unique. GP 0.8.0 eq. 6.16 reads `H_S ∈ Ṽ_{H_A}^{E_U(H)}⟨X_T ⌢ η′_3 ⧺ i_e⟩` — the ticket entry-index field is `e` (`\st¬entryindex` → `e`, cf. eq. 6.32 `n ≡ [(y ↦ Y(i_p), e ↦ i_e) …]`), not `r` (that was pre-0.7 notation). Change `i_r` → `i_e` in the stem.
ch03-hash-functions-and-codec-subscripts | OK | 
ch03-dictionary-semantics | OK | 
ch04-dagger-intermediate-states | OK | 
ch04-extrinsic-dependency-inputs | OK | 
ch04-in-core-300x-rationale | SUSPECT | gpRef only — content and answer are correct and unique. The "upwards of 300 times" passage is §4.9.1 (In-core Consensus) in 0.8.0, not §4.8.1; §4.8 is "Epochs and Slots". (§4 subsections in 0.8.0: 4.1 The Block, 4.2 The State, 4.3 Which History?, 4.4 Time, 4.5 Best block, 4.6 Economics, 4.7 The Virtual Machine and Gas, 4.8 Epochs and Slots, 4.9 The Core Model and Services.)
ch04-best-block-vs-finalized | SUSPECT | gpRef only — answer (option 2) is correct and unique ("In these cases, we define the best block as the head of the best chain, itself defined in section 19"). But the Best-block discussion is §4.5, not §4.6 (§4.6 is Economics). §4.3 and §19 in the ref are right.
ch05-unsigned-header-serialization | OK | 
ch05-extrinsic-hash-inclusion-proof | OK | 
ch05-future-slot-temporarily-invalid | OK | 
ch05-author-index-bound-set | OK | 
ch07-beta-entry-timeslot-080 | OK | 
ch07-belt-empty-output | OK | 
ch07-belt-five-appends-calc | OK | 
ch08-leftmost-removal-code | OK | 
ch08-pool-two-block-calc | OK | 
ch08-new-authorizer-availability-timing | OK | 
ch04-stf-extrinsic | OK | 
ch04-state-components | SUSPECT | Stale symbol: ϑ does not occur anywhere in GP 0.8.0. The 17 components of eq. 4.4 are `σ ≡ (α, β, θ, γ, δ, η, ι, κ, λ, ρ, τ, φ, χ, ψ, π, ω, ξ)` — the ready/accumulation queue is **ω** (`\ready` → ω) and the authorizer queue is **φ**. The marked answer is still the unique wrong pairing (the other three, ρ / ξ / θ, are all correct), so the item works, but the distractor quizzes 0.6.x notation. Suggested fix: "ω → the authorizer queue from which each core's pool is refilled".
ch04-dependency-graph-alpha | OK | 
ch04-common-era | OK | 
ch04-in-core-vs-on-chain | SUSPECT | gpRef only — answer correct and unique. In-core vs on-chain is §4.9.1–4.9.2 in 0.8.0, not §4.8.1–4.8.2.
ch04-balance-timeslot-ranges | OK | 
ch04-coretime-vs-gas | SUSPECT | gpRef only — answer correct and unique (verbatim: "coretime, which is prepurchased and assigned to an authorization agent … Its procurement is out of scope in the present work and is expected to be managed by a system parachain"). That passage is the last paragraph of §4.9.2, not §4.8.2.
ch04-pvm-summary | SUSPECT | gpRef only — answer correct and unique; the eq. range 4.22–4.27 is right, but "The Virtual Machine and Gas" is §4.7 in 0.8.0, not §4.5 (§4.5 is Best block).
ch04-forks-safrole-grandpa | OK | 
ch05-header-fields | OK | 
ch05-prior-state-root | OK | 
ch05-extrinsic-hash-080 | OK | 
ch05-timeslot-validity | OK | 
ch05-author-index | OK | 
ch05-ancestors-lookup-anchor | OK | 
ch05-markers-types | OK | 
ch07-beta-structure | OK | 
ch07-beta-dagger | OK | 
ch07-belt-keccak | OK | 
ch07-purpose | OK | 
ch08-pool-queue-sizes | OK | 
ch08-pool-update | OK | 
ch08-authorizer-identity | SUSPECT | gpRef only — answer correct and unique; §8.1 alone fully supports it ("Authorizers are identified as the hash of their pvm code hash concatenated with their Configuration blob … not the competence of on-chain logic and happens entirely in-core"). But the second pointer is wrong: the authorizer definition `p_a ≡ H(p_u ⌢ p_p)` is **eq. 14.11** (in §14.3 "Packages and Items"); eq. 14.2 is the work-package tuple and §14.2 is "Segments and the Manifest".
ch08-why-authorization | OK | 

## Notes

Ambiguities / traps in GP 0.8.0 itself that these items touch (none of them change a verdict above):

- **Dictionary subscript.** Eq. 3.7 formally defines `d[k] ≡ ∅` when the key is absent, but the prose immediately after says "when using a subscript, it is an implicit assertion that the key exists … the result is undefined and any block which relies on it must be considered invalid." The two readings are in tension; `ch03-dictionary-semantics` (correctly) uses the prose reading, and its distractor 0 exploits the formal one. Worth knowing that a pedantic candidate can argue both texts exist.
- **"Accumulation Output Log" is overloaded.** §12 calls θ′ "the Accumulation Output Log", and §7 calls β_B "the new Accumulation Output Log" — two different objects with the same name. `ch07-belt-keccak` / `ch07-beta-structure` navigate this correctly (θ′ is the per-block (service, hash) sequence; β_B is the append-only structure over its roots).
- **MMR vs MMB.** Appendix E.3 is titled "Merkle Mountain Ranges and Belts"; it defines the *set* ⟦H?⟧ as an MMR but names eq. E.8 "the MMB append function", and §7 prose calls b "the accumulation-result MMB". Calling β_B "an MMR" (as `ch07-beta-structure` does) is defensible but the GP's own preferred word here is belt/MMB.
- **Empty-belt leaf.** `M_B([], H_K) = ∅` (= ℍ_0) only by falling through to the "otherwise" branch of eq. E.3 into `N([], H) = ℍ_0`; the GP never spells the empty case out. `ch07-belt-empty-output` depends on that implicit reading (which is nonetheless forced by the case structure).
- **§7 prose is out of date w.r.t. eq. 7.2.** "For each recent block, we retain its header hash, its state root, its accumulation-result MMB and the corresponding work-package hashes" omits the timeslot t, which eq. 7.2 does include. Also note eq. 7.2 orders the tuple (h, s, b, t, p) while the state serialization C(3) (§D.1) orders it (h, b, s, E_4(t), var(p)) — `ch07-beta-entry-timeslot-080`'s parenthetical "E_4(t) between s and p" is exactly right for C(3), and its "as a fifth field" should be read as "a fifth member", not "position 5".
- **V is a set, not a scalar, in 0.8.0.** Eq. 6.8: `V ≡ {3c | c ∈ N[2, C+1)}` — validator-set sizes are any multiple of 3 from 6 to 1023, so ⟦·⟧_V means "length in the set V" (relevant to `ch05-author-index-bound-set` and `ch05-markers-types`).
- **Header field subscripts are upper-case in 0.8.0** — H_P, H_R, H_X, H_T, H_E, H_W, H_O, H_I, H_V, H_S, H_A. Several items (mostly the 139–154 batch, plus a few of 82–101) write H_p, H_r, H_t, H_i, H_v, H_s, H_a. This is applied consistently as house style and cannot mislead, so it is not flagged per item, but a one-pass case fix would make the quiz match the paper.
- **`ch07-beta-entry-timeslot-080` version labels.** The stem says "This 0.7.2 code" while the pasted code's own comment says "GP 0.6.7". Harmless (stale comment in the team's code) but the mismatch may read as a typo.
- **`ch07-belt-five-appends-calc` / `ch07-belt-empty-output` prefix.** The GP's super-peak prefix token is `$peak` (with the dollar), rendered as 'peak' in the options; the same in both candidate options, so it does not affect discrimination.
