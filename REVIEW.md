# Adversarial review — round 1 (2026-08-26)

224 items were re-answered from scratch by eight independent checkers who saw only the stem, the
options and the marked key (never the author's explanation), and who were required to justify every
verdict from the Gray Paper 0.8.0 LaTeX source.

## Result

| group | items | OK | notation | suspect | wrong |
|---|---|---|---|---|---|
| ch3/4/5/7/8 | 44 | 36 | – | 8 | 0 |
| ch6 Safrole | 29 | 26 | – | 3 | 0 |
| ch9/10/13 | 26 | 23 | – | 3 | 0 |
| ch11/12 | 33 | 20 | – | 12 | 1 |
| ch14 + App A | 28 | 16 | 8 | 4 | 0 |
| App B host calls | 21 | 15 | 5 | 1 | 0 |
| App C–H | 20 | 14 | 3 | 3 | 0 |
| architecture | 23 | 20 | 1 | 2 | 0 |
| **total** | **224** | **170** | **17** | **36** | **1** |

**One mis-keyed item** (`ch11-avspec`, availability-spec field letters) — rewritten.
No other item had a wrong key, and no checker found a second defensible option anywhere.

## What was actually wrong, and what changed

1. **Stale 0.7.x symbols** (the dominant defect, ~40 items). GP 0.8.0 renamed enough that an
   interviewee using the old letters would sound out of date. Fixed bank-wide:
   PVM registers **ω → φ** · ready queue **ϑ → ω** · newly-available reports **W → R** ·
   reporters **R → G** · work-error set **J → 𝔼** (𝕁 is now the segment set) ·
   accumulation statistics **I → S** · service-state daggers **δ‡/δ‡‡ → δ†/δ‡** ·
   header subscripts lower → **UPPER** (H_T, H_I, H_P, H_R, H_X, H_E, H_W, H_O, H_V, H_S) ·
   ticket entry index **i_r → i_e** · accumulate context pair **X/Y → x/y** ·
   availability spec **(h,l,u,n,e,k) → (p,l,u,v,e,n)** · work-report **(s,x,c,a,o,l,d,g) → (s,c,c,a,t,l,d,g)** ·
   refinement context **(a,t,s,b,l,l_t,l_s,p) → (a,n,s,b,l,t,r,p)** · work-package config/context **p,x → f,c** ·
   zone rounding **Q(·) → Z(·)** · chunking **C_v^k → 𝒞^v_k** · grow_heap **Ω_Γ → Ω_♊**.
2. **§4 renumbering.** 0.8.0 inserted a "Best block" subsection, so the VM section is §4.7, epochs
   §4.8 and the core model §4.9 — every §4.5/§4.8.x reference was corrected.
3. **Four substantive over-claims** removed or narrowed:
   - the "since 0.7.0 all variable-length fields move to the end of a structure" rule (not in 0.8.0,
     and false for the unsigned header encoding);
   - "validator indices encode as E_4" (appendix C uses **E_2** everywhere);
   - "M_B is the root over hashed leaves" (M_B deliberately does *not* hash each item; only the
     constant-depth M applies the `$leaf` prefix);
   - "V = 1023 is a protocol constant" (0.8.0 dropped V; thresholds are taken over |κ|), plus the
     "~3–3.5 s of effective computation / 5 % / 95 %" pipelining figures, which appear nowhere in 0.8.0.
4. **Internal inconsistencies** fixed in three items (a tiny-vs-full mix-up in the ticket-cap item, the
   "highest-scoring vs lowest ids" wording, an over-broad "this code conforms" claim about the
   fallback key sequence, which reduces modulo |κ′| rather than a compile-time constant).

## Deliberate rebalance

Eleven of the most arcane arithmetic items were dropped (PVM pipeline-cycle simulation, host-call
record byte offsets, paged-proof page counts, bundle-size arithmetic, a duplicate MMR walk-through)
and six "apply the rule" items were re-tagged from calc to concept: an oral examination probes whether
you can explain the mechanism, not whether you can hand-evaluate it. 224 → 213 items, calc 29 → 13.

## Known residue

- `b2-appB-log-jip1`, the JIP/PR-attribution clauses and the fuzz-protocol items cannot be checked
  against the Gray Paper; they rest on JIP-1..5, the conformance repository and the prize rules.
- Genuine ambiguities in the GP itself are listed per group in `g*_verdicts.md` (§6.2 vs eq. 6.35 on
  ticket ordering, the chained biconditional in eq. 10.7, the missing per-service filter in eq. 13.13,
  the two objects both called "Accumulation Output Log").
