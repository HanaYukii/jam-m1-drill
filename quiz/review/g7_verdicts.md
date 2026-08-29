# g7 (appendices C, D, E, F, G, H) — independent verification against GP 0.8.0 LaTeX

appC-compact-int | OK | 
appC-discriminators | SUSPECT | Marked option's final clause ("since 0.7.0 all variable-length fields of a structure are moved to its end") has no support anywhere in the 0.8.0 source and is false for E_U(H): serialization.tex:181-191 orders E_E(H_E) [variable] and ¿H_W [variable] *before* the fixed E_2(H_I) and H_V. Also E(g ∈ guarantee) puts the variable work-report first. Two lesser nits: GP writes the optional as ¿x (prefix), not "x?"; and dictionaries are additionally wrapped in a length discriminator (E(↕[...]) in C.1.5), which the option omits. Rest of the option is verbatim-correct and the other three options are plainly false, so the key (0) still stands — the clause should be deleted. gpRef §C.1.3–C.1.5 also misses C.1.2, the source of the "fixed-length items encode as-is" clause.
appC-fixed-vs-compact | SUSPECT | Marked option says block/extrinsic encodings "use E_4 for timeslots and validator indices". Timeslots yes (E_4(H_T), E_4(g_t), E_4(x_a), E_4(x_l)), but *every* validator index in appendix C is E_2, never E_4: E_2(a_v) assurer (serialization.tex:155), E_2(j_i) judge (:164), E_2(H_I) author (:188), E_2(v) guarantor credential (:246). The other two clauses are exact — merklization.tex:117 "all non-discriminator numeric serialization in state is done in fixed-length according to the size of the term", and E_2 for a core index does occur (auditing.tex:83, E_2(w_c)). Option 0 is still the only defensible choice; fix "validator indices" (probably meant "service indices", which are E_4).
appD-state-key | OK | 
appD-trie-nodes | OK | 
appE-merkle-functions | SUSPECT | Marked option asserts "M_B is the root over hashed leaves". M_B does the opposite: merklization.tex eq. E.3 is M_B(v,H) = H(v_0) when |v|=1, else N(v,H) — raw blobs as leaves — and the GP says verbatim: "This is suitable for creating proofs on data which is not much greater than 32 octets in length since it avoids hashing each item in the sequence." Hashing leaves ($leaf prefix, via C) is the constant-depth M only, which the same option correctly describes. Everything else in the option (N split at ⌈n/2⌉ with $node, C padding to a power of two with zero hashes, MMR carry-append, $peak super-peak) is exact, and options 1-3 are plainly false, so key 0 still stands. gpRef "eq. E.1–E.8" does not reach the super-peak (E.10) or the MMR encoding (E.9) that the option describes.
appH-erasure-rate | OK | 
appH-chunking | NOTATION | Content fully verified (matches erasure_coding.tex:22-24 and eq. H.5 exactly, including the systematic-concatenation property). Symbol only: the chunking function is 𝒞^v_k (preamble.tex:177 \fnerasurecode -> \mathcal{C}^{#1}_{#2}, v superscript, k subscript); stem writes C_v^k with sub/superscript swapped.
appC-decode-compact-bytes | OK | 
appC-code-avspec-080 | OK | 
appC-work-digest-encoding | OK | 
appC-code-operand-transfer-prefix | OK | 
appD-leaf-first-octet | OK | 
appD-code-service-info-key | OK | 
appE-mmr-append-worked | OK | 
appE-paged-proof-sizes | OK | 
appF-code-shuffle | NOTATION | Answer and worked shuffle verified correct. gpRef calls eq. 11.20–11.22 "guarantor assignment R, P, G": the guarantor-assignment symbol is bold M (preamble.tex:673 \guarantorassignments -> \mathbf{M}; eq. 11.22 "M ≡ (P(|κ′|, η′_2, τ′), Φ(κ′))"). G → M. (G is the reporters set, ch. 11.)
appG-ietf-vs-ring | OK | 
appG-signing-contexts | OK | 
appH-segment-chunk-size | NOTATION | Arithmetic verified (D(1023)=342, k=6, 12-octet chunk, chunk j = d[12j,12j+12) for j<342). Symbol only: same sub/superscript swap — GP writes 𝒞^v_k, stem writes C_v^k.

## Notes

**Method.** Every item was answered from the LaTeX before looking at the marked index. Recomputed independently: E(128)=[0x80,0x80] and E(2^56)=[0xFF]⌢E_8 (9 octets); decode [0xA7,0x10] → l=1, 167−128=39, x=39·256+16=10000; leaf first octets 0xA0 / 0xC0 (bits() is MSB-first per notation.tex:143, bits([160,0])=[1,0,1,0,0,…], so [1,0]⌢bits(E_1(32))[2..]=0b10100000); 5-leaf MMR peaks [l_4, ∅, H(H(l_0⌢l_1)⌢H(l_2⌢l_3))] with super-peak H_K($peak ⌢ l_4 ⌢ H(H(l_0⌢l_1)⌢H(l_2⌢l_3))) — note M_R folds M_R(h_{…|h|−1}) *before* h_{|h|−1}, which is what separates options 0 and 1; F([10,20,30,40],[3,6,4,5]) = [40,10,30,20] by hand; P(200 segments) → ⌈200/64⌉ = 4 segments and |J_6| = max(0,⌈log₂200 − 6⌉) = 2; D(1023)=342 and D(6)=3 from 2d dividing 4104 = 2³·3³·19 with d < v/3+2.

**Distractor defensibility.** Attempted to defend every distractor. Two are strong and correctly wrong: appD-leaf-first-octet option 2 (0xA0/0xA1) is internally consistent — a 6-bit field does hold 33 — and fails only on L's `|v| ≤ 32` guard; appE-mmr-append-worked option 1 has the right peaks and fails only on super-peak argument order. No item had a second defensible key.

**Cross-item inconsistency (worth resolving).** appC-discriminators marks the "since 0.7.0, variable-length fields go last" claim as part of the *correct* answer, while appC-code-avspec-080 uses the near-identical "since GP 0.7.0 any newly added field of a structure must go to its end" as a *wrong* distractor. Since the 0.8.0 source states no such rule, deleting the clause from appC-discriminators removes the contradiction.

**gpRef audit** (verified against the numbering of the rendered 0.8.0, cross-checked to the source): C.5 really is the 5th equation of appendix C (appC-decode-compact-bytes is precise); D.1 = C, D.3/D.4 = B/L; E.1=N, E.2=T, E.3=M_B, E.4=M, E.5=J_x, E.6=L_x, E.7=C, E.8=A, E.9=E_M, E.10=M_R; F.1=shuffle, F.2=Q_l, F.3=hash form; H.1=D(v), H.5=chunking, H.6=recovery; 11.5=Y (avspec), 11.6=D (work digest), 11.7=E (errors), 11.20–11.22=R/P/M, 11.31="∀r ∈ I : (r_s)_v = |κ′|", 12.13=U, 12.14=X, 14.12=P (paged proofs), §14.4.1="Availability Specifier", B.9=Ψ_A, 17.3=s_0 audit seed, 18.1=BLS beefy. All plausible.

One soft gpRef point, not flagged: appC-code-operand-transfer-prefix cites "§B.4 fetch cases 14–15". Ω_Y and its cases 14/15 live in §B.5 (General Functions); §B.4 (Accumulate Invocation) is only where **i** is wired into fetch. Cases 14/15 are reachable *only* from B.4, so the citation is defensible as written, but §B.5 is where a reader will actually find them.

**Transliteration, accepted as-is.** The quiz is plain text, so script/calligraphic symbols are flattened consistently: 𝒟(v) → "d(v)" (items 25/26/71), 𝕌 ∪ 𝕏 → "operand ∪ transfer", ⊚/⊖ → "BADEXPORTS"/"OVERSIZE" (these two are *symbols* in eq. 11.7, unlike the genuine tokens BAD and BIG — the naming mirrors the macro names \badexports/\oversize and is unambiguous in context), ⧺[e] → "⌢ [e]". None of these creates ambiguity, so they are not flagged per-item; only the 𝒞^v_k sub/superscript swap is, because it inverts a real sub/superscript relation rather than changing a typeface.

**Naming.** appC-code-avspec-080 calls the availability-spec fields "ExportsRoot"/"ExportsCount"; GP calls them segment-root e and segment-count n (reporting_assurance.tex:73). This matches the team's Go identifiers shown in the item's code, so it reads correctly in context.

**Minor wording.** appH-erasure-rate's key says a 4,104-octet segment "splits into 4104/(2·342) = 6 pieces per validator". k = 6 is the piece count for the whole segment (GP: "data-parallelism of order 6 with 1023 validators"); each validator's chunk happens also to be 6 octet-pairs, so both readings land on 6 and nothing is falsified — but "per validator" is loose. Left as OK.
