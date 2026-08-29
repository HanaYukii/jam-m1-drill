# g5 — ch14 + Appendix A — adversarial verdicts (GP 0.8.0, source of truth: /root/work/jam/gp-src)

appA-exit-reasons | SUSPECT | answer + distractors fine (ε ∈ {∎,☇,∞} ∪ {F̄,ℏ}×N_R, eq. A.1); gpRef "§4.5" is wrong — §4.5 is "Best block"; the prose list of exit reasons is §4.7 "The Virtual Machine and Gas"
appA-program-blob | OK | 
appA-basic-blocks-gas | OK | 
appA-memory-access | OK | 
appA-standard-init | NOTATION | ω_0/ω_1/ω_7/ω_8 → φ_0/φ_1/φ_7/φ_8 (0.8.0 registers are φ = \registers = \varphi; ω is now the accumulation ready-queue); "Q(|o|)" → "Z(|o|)" (\rnq renders Z(·) for zone-rounding, \rnp = P(·) for page-rounding). Values, layout and eq. A.42–A.47 all check out
appA-djump-alignment | OK | 
appA-host-call-continue | NOTATION | "f(h, ϱ, ω, μ, x)" → f(h, ϱ, φ, μ, x); substance of Ψ_H (eq. A.38–A.40) exactly right, incl. that Ω⟨X⟩'s codomain excludes F̄
appA-registers-immediates | SUSPECT | only defensible option, but over-generalised and the section pointer is empty. (a) "length ℓ = min(4, skip − 1)" is only the one-register/two-register-plus-immediate rule; the one-immediate group (ecalli) uses l_X = min(4, ℓ), and the two-immediate groups take l_X from a 3-bit field of ζ_{ı+1}/ζ_{ı+2}. (b) The item reuses ℓ for the immediate length, but GP 0.8.0 defines ℓ ≡ skip(ı) (eq. A.23) and calls the immediate length l_X/l_Y. (c) "low and high nibbles" is false for three-register instructions: r_D = min(12, ζ_{ı+2}), a whole octet. (d) load_imm_64's immediate is ν_X ≡ E⁻¹_8(ζ_{ı+2…+8}) — not sign-extended. gpRef "§A.5.1" is "Instructions without Arguments", which contains no register/immediate decoding at all
ch14-work-package | NOTATION | "P = (j, h, u, p, x, w)" → in 0.8.0 eq. 14.2 the tuple is ⟨j, h, u, f, c, w⟩: p (configuration blob) → f (\wp¬authconfig = \mathbf{f}); x (refinement context) → c (\wp¬context = \mathbf{c}). Note g5's own ch14-bundle-size-calc already uses the new f. Everything else (h = auth-code host service, u = auth-code hash, I = 16, work-item fields) is correct
b2-appA-branch-both-targets | OK | 
b2-appA-jump-family | NOTATION | ω_reg / ω′_A → φ; operand and target-resolution claims match eq. A.27/A.28/A.30/A.34 + A.20/A.22 exactly
b2-appA-div-rem-signed-calc | NOTATION | ω_A/ω_B/ω′_D → φ_A/φ_B/φ′_D. Arithmetic re-derived independently: a = Z_4(0xFFFFFFF9) = −7, b = 2; div_s_32 = Z⁻¹(rtz(−3.5)) = Z⁻¹(−3) = 2^64−3 ✓; rem_s_32 = Z⁻¹(smod(−7,2)) = Z⁻¹(−1) = 2^64−1 ✓
b2-appA-shift32-code | NOTATION | ω_B/ω′_A → φ_B/φ′_A. Re-derived: 139 → X_4(⌊0xFFFFFFF0 ÷ 2^4⌋) = X_4(0x0FFFFFFF) = 0x0000_0000_0FFF_FFFF ✓; 140 → Z⁻¹_8(⌊−16 ÷ 16⌋) = Z⁻¹(−1) = 0xFFFF_FFFF_FFFF_FFFF ✓
b2-appA-gas-block-calc | NOTATION | ω_1..ω_4 → φ_1..φ_4. I re-ran the eq. A.55–A.61 simulation by hand: all three instructions decode in cycle 0 (slots 1 + 𝔓(1,2)=2 + 1 = 4 ≤ 4); at c=1 the load and the fallthrough start (5 starts, units (4,4,4,1,1)); load's 25 cycles reach 0 at c=26, add_64 starts then and finishes at c=27; in-order retirement empties the ROB at c=29 → ϱ^Δ = max(29 − 3, 1) = 26 ✓. Answer is robust even if 𝔓 resolved to 1
b2-appA-gas-charged-flag | OK | 
b2-appA-recompiler-block-gas-stub | OK | 
b2-appA-load-imm-jump-ind-reg-write | NOTATION | ω_A / ω′ / ω_7/ω_8 → φ. Substance verified: eq. A.1 returns ⟨ε, 0, ϱ′, ϱ̃′, φ′, μ′⟩ on ☇ and ∎ (only ı is zeroed), and Ω_K (invoke, §B) writes E_8(g′_R) ⌢ E_8(φ′) into μ* on the PANIC branch too, so the write is observable
b2-appA-store-cross-page-fault-address | OK | 
b2-appA-sigsegv-handler | OK | 
b2-appA-vblob-terminator | OK | 
b2-appA-opcode-renumbering-unlikely | OK | 
ch14-code-digest-mapping | OK | 
ch14-code-refine-args | OK | 
ch14-compute-report-signature | OK | 
ch14-oversize-cumulative-calc | OK | 
ch14-bundle-size-calc | SUSPECT | answer + arithmetic correct (re-derived 64+32+(10,000+448,800+3,000)+(2,000+224,400) = 688,296; W_F = 4104+32·12 = 4488; W_B = 3072·4488+4096+64+64 = 13,791,360); gpRef "C.6 constants W_G, W_X, W_M" is wrong — Appendix C is the Serialization Codec and has only C.1/C.2; the constants live in Appendix H "Index of Notation", §H.4.4 (and W_F/W_B are also defined in-place at eq. 14.7/14.8)
ch14-paged-proofs | SUSPECT | answer correct; gpRef "eq. E.4–E.6 (M, J_x, L_x)" is wrong — those are eq. D.10, D.11, D.12 in Appendix D "State Merklization" (Appendix E is "Shuffling"). The other refs (eq. 14.12 for P, 14.18 for e = M(s)/s♣, 13.12 for the W_G⌈n·65/64⌉ DA-load) are all correct
ch14-makebundle | OK | 

## Notes

**Method.** Every item was answered from the LaTeX first, then compared with the marked key. Equation numbers were re-derived by counting numbered environments per file; all arithmetic (n=40, 41, 42, 132, 133) was recomputed from scratch. No item's marked answer is substantively wrong: **0 WRONG**. Every item passed the "exactly one defensible option" test — I tried to defend each distractor and none survives (details below for the near-misses).

**Systematic notation error: PVM registers are φ, not ω.** `preamble.tex:845` — `\newcommand*{\registers}{\varphi}`; overview.tex §4.7 says outright "φ ∈ [ℕ_R]_13 is typically used to denote the registers". `\omega` in 0.8.0 is `\ready`, the accumulation ready-queue (preamble.tex:789). Seven appendix-A items and one ch14 item carry the stale ω: appA-standard-init, appA-host-call-continue, b2-appA-jump-family, b2-appA-div-rem-signed-calc, b2-appA-shift32-code, b2-appA-gas-block-calc, b2-appA-load-imm-jump-ind-reg-write. Their explanations use ω throughout as well, so a global s/ω/φ/ pass over group 5 is the right fix. (Some non-option prose, e.g. b2-appA-store-cross-page-fault-address's explanation, also says "ω_8".)

**Other stale symbols found.**
- `Q(x)` → `Z(x)`: 0.8.0 names the zone-rounding function Z(·) (`\rnq` → `Z(#1)`) and the page-rounding function P(·) (`\rnp`). appA-standard-init still writes Q(|o|).
- Work-package field letters changed: configuration blob p → **f**, refinement context x → **c** (preamble.tex:487–488). ch14-work-package still uses the 0.7.x letters; ch14-bundle-size-calc already uses the new f, so the set is internally inconsistent.
- Symbols I checked and found **correct**: Z_A = 2, Z_P = 2^12, Z_Z = 2^16, Z_I = 2^24, ϖ, ζ, 𝔏, U, T, ν, ℓ, 𝔪 = 25, 𝔟, 𝔓, 𝔛, ϱ^Δ, Z_n (𝒵_n signed), X_n (𝒳_n sign-extension), ∇ (error), ⊖ (oversize), ⊛ (badexports), 𝔻/ℝ/ℙ/𝕎/𝕐/𝕁 sets, W_R = 48·2^10, W_G = 4104, W_F = 4488, W_M = W_X = 3072, W_B = 13,791,360, I = 16, G_R = 5·10⁹, M/J_x/L_x, Ξ, B, h⊞, s♣, work-digest fields (s, c, y, g, l, u, i, e, x, z), availability-spec fields (p, l, u, v, e, n).
- Glyph approximations used consistently across the whole quiz and *not* flagged per item: ∎ for `\blacksquare` (■), h̄ for `\host` = `\hbar` (ℏ), F̄ for `\fault` (a 180°-rotated sans F), ▸ for `\continue` = `\blacktriangleright`. The gas-charged flag is written "flag" in prose; its GP symbol is ϱ̃ (`\tilde{\varrho}`, `g̃` inside the inner-PVM tuple P).

**Systematic gpRef imprecision: "§A.5.1".** Seven items cite "§A.5.1" for instruction-table rows that live elsewhere: §A.5 is "Instruction Tables", and A.5.1 is only "Instructions without Arguments". Correct subsections: opcode 40 → A.5.5; 50/62 (store_u64) → A.5.6; 80 → A.5.8; 100–110 → A.5.9; 139/140 → A.5.10; 180 → A.5.12; 190–230 (div/rem) → A.5.13. In every case the equation numbers quoted alongside (A.27, A.28, A.30, A.32, A.34, A.35) are correct and pin the right table, so I only marked it fatal for appA-registers-immediates, where "§A.5.1 & eq. A.19" is the *entire* pointer and neither location contains the register/immediate decoding rules.

**Appendix letters.** With `\appendix` in graypaper.tex the mapping is A = pvm.tex, B = pvm_invocations.tex, C = serialization.tex (Serialization Codec), D = merklization.tex (State Merklization), E = utilities.tex (Shuffling), F = bandersnatch.tex, G = erasure_coding.tex, H = definitions.tex (Index of Notation). The two bad gpRefs above (C.6 → H.4.4; E.4–E.6 → D.10–D.12) both stem from this. Everything else the author cites is right, including the fiddly ones I spot-checked: eq. 11.6 = 𝔻 (work-digest), 11.8 = the W_R report-size limit, 11.31 = "(r_s)_v = |κ′|" (shard count = active validator count), 13.10 = R(c) and 13.17 = R(s) (the digest counters feeding core/service stats), 13.12 = D(c) with the W_G⌈n·65/64⌉ paged-proof term, 14.10 = C, 14.12 = P, 14.13/14.14 = Ξ and the srlookup correspondence, 14.15–14.18 = X/L/S/J, B, s = A(…), A, B.1 = Ψ_I, B.5 = Ψ_R, A.8/A.10/A.11 = gas charge / final state / flag*, A.54/A.62/A.64/A.65 = ϱ^Δ / 𝔓 / 𝔪 / 𝔟.

**Distractors I tried hardest to rescue, and why they still fail.**
- b2-appA-vblob-terminator [1] ("branch and jump targets are validated at deblob time"): v_blob/v_inst (eq. A.2) touch only |k| = |c|, bit-flagging, opcode validity ∈ U, and the terminating instruction ∈ T. Target validity is a *runtime* panic (A.20/A.21/A.22). Same reason b2-appA-branch-both-targets [3] fails.
- b2-appA-recompiler-block-gas-stub [1] ("ı* must be the terminator"): eq. A.10 gives ı* = ı when ε^ϱ ≠ ▸, i.e. the counter as it stood — the block start on a normal entry. The prepared path's ExitPC is the one thing that *is* right.
- ch14-oversize-cumulative-calc [3] ("later items also oversize"): z sums only earlier results with r ∈ Y, so the ⊖ item's 5,000 octets drop out; 1,000+20,000+25,000+3,000 = 49,000 ≤ 49,152, and the fourth item is ok. The numbers are chosen so this is decided by 152 octets — worth keeping.
- appA-registers-immediates [1]/[2]/[3] are all plainly false, which is why the item survives despite the loose key text.

**Unverifiable from the primary source.** Two stems/keys cite upstream PR numbers — appA-basic-blocks-gas ("PR #508" for the gas model) and b2-appA-opcode-renumbering-unlikely (same PR for sbrk → grow_heap). The LaTeX carries no PR metadata, so I could confirm the *content* of both changes (basic-block gas charging exists at A.7/A.8/A.54; sbrk is gone from the two-register table, 101–110 are count_set_bits_64…reverse_bytes, and grow_heap is a host call in F/Ω_Gemini) but not the attribution. If both attributions cannot be sourced, drop the PR number from the stem of appA-basic-blocks-gas — it is decorative there.

**One tension worth a deliberate decision.** b2-appA-sigsegv-handler's key says the handler turns a fault into "F̄ carrying the faulting guest address" — true of the C code, but *not* GP-conformant (eq. A.9 requires Z_P⌊min(x) mod 2^32 ÷ Z_P⌋, the lowest inaccessible *page* address). That exact non-conformance is the answer to b2-appA-store-cross-page-fault-address. The option reads as a description of the handler, not a conformance claim, so I left it OK — but a sharp candidate who has just done the store item may hesitate. Adding "(the same page-alignment gap as the interpreter)" to the option would remove the ambiguity without changing the key.
