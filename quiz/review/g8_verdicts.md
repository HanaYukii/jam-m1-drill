# g8_arch.json — adversarial verdicts (checked against GP 0.8.0 LaTeX + PDF, and research/ecosystem-notes.md)

arch-corejam-name | OK | 
arch-driving-factors | OK | 
arch-why-safrole | OK | 
arch-availability-auditing | OK | 
arch-why-prior-root-and-pipelining | SUSPECT | Stem's "roughly 3–3.5 seconds of effective block computation per 6-second slot" appears nowhere in GP 0.8.0 (grep of text/ and the rendered PDF finds no such figure), and the keyed option's "~5% pre-accumulation / ~95% accumulation" split is likewise absent — GP only says the prior state root exists "to facilitate the pipelining of block computation and in particular of Merklization" (§5) and lists "temporal parallelism … pipelines much of the computation between blocks" (§20). Also "~16 independent state components": eq. 4.4 gives σ ≡ (α, β, θ, γ, δ, η, ι, κ, λ, ρ, τ, ϕ, χ, ψ, π, ω, ξ) = 17. Answer index 0 is still the only defensible option, but it rests on invented precision.
arch-services-vs-accounts | OK | 
arch-constants | SUSPECT | Every value in the keyed option is right EXCEPT "V = 1023 validators". In 0.8.0 V is no longer a protocol constant: the Index of Notation constants list (App. I.4.4) contains A, B_I, B_L, B_S, C, D, E, F, G_A, G_I, G_R, G_T, H, I, J, K, L, M, N_V, N_O, O, P, Q, R, S, T, U, W_A, W_B, W_C, W_G, W_F, W_M, W_R, W_T, W_X, X, Y, Z_A, Z_I, Z_P, Z_Z — no V and no N. Validator-set size is variable: eq. 6.x defines 𝕍 ≡ {3c : c ∈ N_[2,C+1]} (multiples of 3, 6…1023) and thresholds are taken over |κ|. The item also contradicts arch-jip4-protocol-parameters-080 in the same file, which correctly states V was dropped. Fix: drop V (or say "target/full chainspec V = 1023, not a GP constant").
arch-jam-vs-polkadot-eth | OK | 
delta-summary-080 | OK | 
arch-tiny-config | OK | 
arch-beefy-commitment | OK | 
arch-best-chain-selection | OK | 
arch-audit-tranches | NOTATION | keyed option (index 2): "$jam_audit ⌢ Y(H_v)" → Y(H_V). In 0.8.0 header subscripts are uppercase (preamble.tex 741-750: P, R, T, X, E, W, O, I, V, S); eq. 17.3 reads s_0 ∈ V_{κ[v]}⟨X_U ⌢ Y(H_V)⟩. Everything else in the option is correct (A = 8 s tranche period, F = 2 bias factor, per-report VRF over no-shows).
arch-guaranteeing-procedure | OK | 
arch-two-da-classes | OK | 
arch-core-virtual-hardware | OK | 
arch-sweet-spot-further-work | OK | 
arch-jip4-protocol-parameters-080 | OK | 
arch-fuzz-protocol-m1 | OK | 
arch-prize-interview-rule12 | OK | 
arch-audit-initial-tranche | OK | 
arch-audit-outcomes | OK | 
arch-audit-reconstruction | OK | 

## Notes

**Method.** Read text/{intro,previous_work,overview,header,recent_history,safrole,accounts,authorization,judgments,reporting_assurance,work_packages_and_reports,guaranteeing,assurance,auditing,beefy,best_chain,discussion,conclusion,definitions,erasure_coding,pvm_invocations}.tex plus preamble.tex, and cross-checked section/equation/appendix numbering against the rendered gp-raw.txt / gp-layout.txt of the 0.8.0 PDF. Non-GP items checked against research/ecosystem-notes.md verbatim quotes, and — where the notes were silent — against the 0.7.2-targeting client in /root/work/jam/team-repo.

**Numbering baselines established (useful for the whole quiz).**
- Sections: 1 Intro, 2 Previous Work, 3 Notation, 4 Overview, 5 Header, 6 Block Production, 7 Recent History, 8 Authorization, 9 Accounts, 10 Disputes, 11 Reporting & Assurance, 12 Accumulation, 13 Statistics, 14 Work Packages/Reports, 15 Guaranteeing, 16 Assurance, 17 Auditing, 18 Beefy, 19 Grandpa/Best Chain, 20 Discussion, 21 Conclusion.
- Appendices: A PVM, B VM Invocations, C Serialization, D State Merklization, E General Merklization, F Shuffling, G Bandersnatch VRF, **H Erasure Coding**, **I Index of Notation**. (So `arch-audit-reconstruction`'s "appendix H" and `arch-constants`' "Appendix I" are both correct — the `\input` list in graypaper.tex is misleading because merklization.tex and utilities.tex each contain two appendix sections.)
- §17 runs to eq. 17.19, so `arch-audit-tranches`' "eq. 17.1–17.19 (PDF numbering)" is exact.

**gpRef nits (content and keying unaffected; worth fixing).**
- `arch-availability-auditing`: "§4.8.1" → **§4.9.1** (In-core Consensus). §4.8 is Epochs and Slots and has no subsections.
- `arch-services-vs-accounts`: "§4.8.2" → **§4.9.2** (On Services and Accounts).
- `arch-audit-initial-tranche`: "eq. 17.2–17.4" → **17.3–17.5**. PDF numbering: 17.1/17.2 = q, 17.3 = s_0, 17.4 = X_U, **17.5 = a_0** — the shuffle-and-take-ten equation the question is actually about is outside the cited range.
- `arch-beefy-commitment`: "eq. 7.7–7.8" is exact (7.7 = β_B′ MMR append, 7.8 = β_H′ with b = MMR super-peak); "§19–20" is a loose add-on — the bridge/aggregation rationale is in §18 itself.
- `arch-jip4-protocol-parameters-080`: JIP-5 (validator key derivation) is irrelevant to `protocol_parameters`; JIP-4 + App. B are the real refs.
- `arch-prize-interview-rule12`: T&C 3.5 (conformance to latest GP) and 8.4 (payment timing) are not about the interview; 6.1 and the delivery template are. Harmless.

**Phrasing imprecision, both audit-selection items** (`arch-audit-tranches`, `arch-audit-initial-tranche`): "takes the first ten **non-empty** entries" is not what eq. 17.5 says — `a_0 = {r | r ∈ F(q, Y(s_0))_{···+10}, r ≠ ∅}` takes the first **ten** entries of the shuffled sequence and *then* discards ∅, so |a_0| ≤ 10. Defensible only because the GP's own prose says "the non-empty items to audit through a verifiably random selection of ten cores". Consider rewording to "the first ten entries, keeping the non-empty ones".

**Verifications worth recording (all confirmed correct, no action needed).**
- `delta-summary-080`: all twelve listed changes check out against 0.8.0 source and the release notes — 𝕍 = {3c}, full guarantees in ρ, N_V = N_O = 16, bless→manager, "Authorizers are identified as the hash of their PVM code hash concatenated with their Configuration blob" (§8), refine context anchor slot + lookup-anchor posterior root, `grow_heap = 1` host call + per-basic-block gas model, M_* host-call gas costs, `n = ⌈2E/|γ′_P|⌉` (safrole.tex:297), extrinsic hash `p = E(var([⟨E_4(s), H(d)⟩ …]))` (§5), processed-transfer count in service stats, and β_H gaining `t` — the last one verified by diff against the 0.7.2 client, whose `BlockInfo` is ⟨h, b, s, p⟩ with no timeslot. All three distractors are genuine 0.6.0 / 0.7.1 / 0.5.0+0.6.4 changes, so the item discriminates well.
- `arch-jip4-protocol-parameters-080`: counted directly. 0.8.0 fetch selector 0 = 29 fields (B_I,B_L,B_S,C,D,E,G_A,G_I,G_R,G_T,H,I,J,K,L,O,P,Q,R,T,U,W_A,W_B,W_C,W_M,W_R,W_T,W_X,Y) = 7×8 + 11×2 + 11×4 = **122 bytes**. The 0.7.2 struct (team-repo internal/types/types.go:1683) has 33 fields = 7×U64 + 13×U16 + 13×U32 = **134 bytes**; the extras are N (U16), V (U16), W_E (U32), W_P (U32) = exactly 12 bytes. The option's numbers are right to the byte.
- `arch-fuzz-protocol-m1`: Unix `SOCK_STREAM` bound by the target, JAM codec + u32-LE length prefix, PeerInfo feature intersection, GetState on mismatch, mandatory Ancestry+Forking — all verbatim in the notes; the two details the notes don't quote were confirmed in team-repo: `Initialize{Header, State, Ancestry}` (cmd/fuzz/step_folder.go:247-270) and Error returning the *prior* state root, i.e. state unchanged (internal/fuzz/client.go:84-85, discriminant 255 = 0xff).
- `arch-tiny-config`: 6/2/12/Y=10/R=4/D=32/ring 6 verbatim from the vectors README; the two derived numbers are right — supermajority is >2/3·6 → ≥5, and verdict thresholds are ⌊2/3|k|⌋+1 / 0 / ⌊1/3|k|⌋ = **5/0/2** for |k| = 6 (judgments.tex:104-106).
- `arch-two-da-classes`: "kept ≥ 28 days = 672 epochs" is verbatim GP — work_packages_and_reports.tex:168 "a minimum of 28 days (672 complete epochs) … referred to as the *Distributed, Decentralized, Data Lake* or D³L". Paged-proofs are genuinely part of the long-term store (same paragraph), so the option is not over-reaching.
- `arch-core-virtual-hardware`: every figure (25–50%, 2 MB/s, 2 GB RAM, unlimited semi-static preimage reads, 48 KB result, 10 ms with full state access) is verbatim §20.1.
- `arch-sweet-spot-further-work`: the four "under consideration" items and the three omissions match §21 one-for-one; distractor 1 inverts each of them (refine vs accumulate, removing vs restricting `transfer`, lifting vs reserving, state trie vs work-package format), which is a well-built distractor.

**Distractor-side notation slips (not scored, but they'd read as sloppy to a GP-literate candidate).** `arch-best-chain-selection` option 0 writes "H_r" (should be H_R); `arch-beefy-commitment` option 3 writes "H_o marker" (should be H_O) and the invented "M_B(s, H_K)".

**Staleness watch on `arch-tiny-config`.** The quoted tiny/full table comes from the jamtestvectors README titled "Test Vectors for the JAM Protocol (0.7.1)"; no 0.8.0 branch existed at note-fetch time. Two of its rows are already dead under 0.8.0: `tickets_per_validator: 3` (0.8.0 derives N = ⌈2E/|γ′_P|⌉ = ⌈24/6⌉ = **4** for tiny) and `num_ec_pieces_per_segment: 1026` (W_P was removed; shard counts now come from `original_shards(v)`, i.e. 3:6 for tiny). Neither appears in the keyed option, so the item is safe as written — but do not extend it to tickets or EC parameters without re-sourcing.

**Wording drift, `arch-jam-vs-polkadot-eth`.** "semi-coherent" is the quiz's word; the GP's is "mostly coherent" (title, §1.3). Substantively fine.

**Symbol baseline used for the notation pass** (preamble.tex): header subscripts uppercase — H_P, H_R, H_X, H_T, H_E, H_W, H_O, H_I, H_V, H_S; R = newly-available reports (`\justbecameavailable`, 678); G = reporters (`\reporters`, 676); ω = ready queue (eq. 4.4); κ = active set, γ_P = pending set; contexts X_A/X_B/X_E/X_F/X_G/X_I/X_T/X_U/X_⊤/X_⊥; A = audit tranche period, F = audit bias factor. Only one item in the file misuses any of these (`arch-audit-tranches`).
