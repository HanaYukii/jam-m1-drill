# -*- coding: utf-8 -*-
"""GP 0.8.0 §12 Accumulation — batch c3.

Ground truth: /root/work/jam/gp-src/text/accumulation.tex (+ definitions.tex, accounts.tex,
reporting_assurance.tex, pvm_invocations.tex, preamble.tex).  Equation numbers cross-checked
with scripts/eqref.py and /root/work/jam/gp-layout.txt (the typeset PDF).
"""

ITEMS = [

# ─────────────────────────────────────────────────────────── 1 · L1 · delta
{
    "id": "c3-ch12-omega-xi-theta-naming",
    "ch": "12",
    "section": "12.1 History and Queuing",
    "gpRef": "eq. 12.1 & 12.3; eq. 7.4 (θ); §4.2 state σ",
    "difficulty": 1,
    "kind": "delta",
    "tags": ["accumulation", "state", "notation", "delta-0.8.0"],
    "stem": "Among the state items in σ written by accumulation are ω, ξ and θ. A GP 0.7.2-era Go client "
            "still calls its ready-queue field `Vartheta`. Which mapping of symbol → meaning is right for GP 0.8.0?",
    "options": [
        "ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E is the ready (accumulation) queue of deferred reports each paired with its outstanding "
        "dependency set — GP 0.7.2 wrote this as ϑ; ξ ∈ ⟦{H}⟧_E is the epoch-long history of already-accumulated "
        "work-package hashes; θ ∈ ⟦(N_S, H)⟧ is the Accumulation Output Log, this block's (service, commitment) pairs",

        "ω ∈ ⟦(N_S, H)⟧ is the Accumulation Output Log, renamed from θ in 0.8.0; ξ ∈ ⟦⟦(ℝ, {H})⟧⟧_E is the "
        "ready queue of deferred reports each paired with its outstanding dependency set; θ ∈ ⟦(N_S, N_G)⟧ now "
        "holds the per-service gas usage u that the last block's Δ+ returned, which is what the accumulation "
        "statistics read",

        "ω ∈ ⟦{H}⟧_E took over from ξ as the epoch-long history of already-accumulated work-package hashes; the "
        "ready queue is still spelled ϑ ∈ ⟦⟦(ℝ, {H})⟧⟧_E in 0.8.0 and θ ∈ ⟦(N_S, H)⟧ is unchanged, so a 0.7.2 "
        "client only has to retire the symbol ξ and repoint the state key that held it",

        "ω ∈ ⟦(N_S, N_S, N_B, B_128, N_G)⟧ is a new 0.8.0 state item holding the deferred transfers carried "
        "between accumulation rounds so that they survive a block boundary; ϑ ∈ ⟦⟦(ℝ, {H})⟧⟧_E remains the ready "
        "queue and ξ ∈ ⟦{H}⟧_E the epoch-long history of accumulated work-package hashes",
    ],
    "answer": 0,
    "optNotes": [
        "0.8.0 preamble 把 ready 定為 ω、accumulated 定為 ξ、lastaccout 定為 θ，三個型別也全對。",
        "per-service gas usage u 是 eq. 12.17 的回傳分量，餵完 eq. 12.28 的 G(s) 就消失，進不了 σ。",
        "ξ 在 0.8.0 完全沒有改名或改義，「只要把 ξ 退休掉」的遷移會把 accumulated 歷史整個弄丟。",
        "deferred transfers 從不進 σ，只在 Δ+ 遞迴內部傳遞；eq. 12.14 只是 Ψ_A 的輸入型別。",
    ],
    "explanation": "GP 0.8.0 的 preamble 明訂 ready = ω、accumulated = ξ、lastaccout = θ。eq. 12.3 給出 ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E（ℝ 是 0.8.0 的 work-report 集合，0.7.2 記作 W；每個 slot 一串「report + 尚未滿足的 dependency 集合」），eq. 12.1 給出 ξ ∈ ⟦{H}⟧_E（一個 epoch 份量的已 accumulate work-package hash），eq. 7.4 / 12.25 給出 θ ∈ ⟦(N_S, H)⟧ 亦即本區塊的 accumulation output log。0.7.2 的 ready queue 符號是 ϑ（團隊 Go 欄位 `Vartheta`、state key C(14)），0.8.0 改成 ω（GP 與 0.8.0 release notes 都沒有說明改名理由，別在口試時把「為了避開 ϑ/θ 混淆」講成 GP 的說法）；state key 不變：C(14)=ω、C(15)=ξ、C(16)=θ。",
    "trap": "面試常考：0.7.2→0.8.0 ready queue 是 ϑ→ω 的更名，state key C(14) 與型別結構都沒動；同章的 W!/W_Q/W* "
            "也一併改成 R!/R^Q/R*；別把 ω 和 θ（output log）搞混。",
},

# ─────────────────────────────────────────────────────────── 2 · L1 · concept
{
    "id": "c3-ch12-operand-tuple-fields",
    "ch": "12",
    "section": "12.2 Execution",
    "gpRef": "eq. 12.13 (U), 12.14 (X), 12.23 (Δ1)",
    "difficulty": 1,
    "kind": "concept",
    "tags": ["accumulation", "operands", "work-digest"],
    "stem": "Δ1 builds i^U as one operand tuple per work-digest of service s, taken from the round's reports in order. "
            "Two of s's digests sit in different reports r₁ and r₂. Which description of what an operand tuple carries is right for GP 0.8.0?",
    "options": [
        "The set is U (and deferred transfers are X, Ψ_A taking ⟦U ∪ X⟧). Each tuple mixes digest-level fields — "
        "y payload hash, g accumulate gas-limit, l the result, which is a blob or a member of the work-error set E — "
        "with fields lifted from its own report: p = (r_s)_p package hash, e = (r_s)_e segment root, a = r_a authorizer "
        "hash and t = r_t authorizer trace; so the two tuples differ in their report-level fields",

        "The set is U (and deferred transfers are X, Ψ_A taking ⟦U ∪ X⟧). An operand tuple is the work-digest "
        "verbatim, so besides y, g and l it also carries c the code hash, d_u the gas actually used during refine, "
        "and the import / extrinsic / export counts that feed the core statistics; nothing is lifted in from the "
        "enclosing report, so the two tuples differ only in their payload hashes",

        "The set is U (and deferred transfers are X, Ψ_A taking ⟦U ∪ X⟧). One operand tuple is built per report "
        "rather than per digest: its l field holds the concatenation of that report's digest results and its g "
        "field their summed gas-limits, with p, e, a and t lifted from the report as usual, and the service "
        "demultiplexes the results by payload hash — so s receives one tuple here, not two",

        "The set is U (and deferred transfers are X, Ψ_A taking ⟦U ∪ X⟧). Each tuple takes y, g and l from the "
        "digest and, from its report, the core index and the refinement-context anchor in place of the package "
        "hash and segment root, so that accumulate can re-verify availability; digests whose l falls in the "
        "work-error set E are dropped before i^U is assembled, so the two tuples survive only if both refined "
        "successfully",
    ],
    "answer": 0,
    "optNotes": [
        "eq. 12.23 明寫來源：y/g/l 取自 digest，t/e/p/a 取自所屬 report，兩筆的 report-level 欄位因此不同。",
        "code hash c、refine 實際用掉的 gas 與 i/x/z/e 計數只留在 digest，餵 §13 統計與 §11.4 檢查，不進 accumulate。",
        "與 eq. 12.23 的 d ↕ r_d 迭代直接矛盾：該 service 這一輪有幾個 digest 就有幾個 operand。",
        "eq. 12.13 的七個欄位裡沒有 core index 與 refinement context；l 的型別是 B ∪ E，錯誤結果不會被濾掉。",
    ],
    "explanation": "eq. 12.13：U ≡ (p ∈ H, e ∈ H, a ∈ H, y ∈ H, g ∈ N_G, t ∈ B, l ∈ B ∪ E)，eq. 12.14：X ≡ (s, d, a, m, g)，兩者的聯集就是 Ψ_A 的第五個參數（eq. B.9）。eq. 12.23 明白寫出每個 tuple 的來源：l ← d_l、g ← d_g、y ← d_y 來自 work-digest；t ← r_t、e ← (r_s)_e、p ← (r_s)_p、a ← r_a 來自那個 digest 所屬的 report，所以同一個 service 在不同 report 裡的兩個 digest，report-level 欄位不同。l 的型別特地寫成 B ∪ E，就是為了讓 service 自己處理 ∞、☇、BAD、BIG 等錯誤，GP 沒有任何「把 work-error digest 濾掉」的步驟。",
    "trap": "口訣：operand = 「digest 三件（y, g, l）+ report 四件（p, e, a, t）」；refine 用掉多少 gas 不在裡面。",
},

# ─────────────────────────────────────────────────────────── 3 · L2 · rationale
{
    "id": "c3-ch12-E-removes-entries-too",
    "ch": "12",
    "section": "12.1 History and Queuing",
    "gpRef": "eq. 12.7 (E), 12.8 (Q), 12.12, 12.33 (ω′)",
    "difficulty": 2,
    "kind": "rationale",
    "tags": ["accumulation", "dependencies", "queue"],
    "stem": "The queue-editing function E(r, x) does two jobs: it strips dependencies that appear in x, and it also "
            "discards whole entries. A teammate implements only the first job. What actually goes wrong?",
    "options": [
        "Q stops terminating — E(r, P(g)) hands back the same entries with still-empty dependency sets, so the next "
        "recursion picks the identical g forever — and at the block boundary ω′ (both the i = 0 case E(R^Q, ξ′[E−1]) "
        "and the i ≥ τ′ − τ case E(ω↺[m−i], ξ′[E−1])) keeps reports that were just accumulated, so they would be "
        "accumulated again in a later block",

        "Only ω′ is affected — both the i = 0 case E(R^Q, ξ′[E−1]) and the i ≥ τ′ − τ case E(ω↺[m−i], ξ′[E−1]) "
        "would keep reports that were just accumulated, so the ready queue grows without bound until the "
        "epoch-long shift drops the stale entries. Q itself stays safe, because each recursion is fed a strictly "
        "shorter sequence once its dependency sets have been stripped",

        "Nothing breaks. Q still terminates because its recursion is bounded by the epoch length E, and the §11.4 "
        "contextual check rejects any incoming report whose package hash is already in ξ, so an entry sitting in ω "
        "can never be accumulated a second time either; discarding whole entries is a pure optimisation that keeps "
        "ω small",

        "The dependency-stripping job becomes redundant instead: once entries are never removed, a report can only "
        "ever be blocked by another report sitting in the same queue, so every dependency E would have stripped "
        "belongs to an entry E would also have deleted. Q therefore still terminates and ω′ still drains, just "
        "more slowly — one epoch-long shift at a time rather than one accumulation round at a time",
    ],
    "answer": 0,
    "optNotes": [
        "少了 (r_s)_p ∉ x 這一半，eq. 12.8 每一輪都算出同一批 g，遞迴永遠停不下來。",
        "沒有刪除就不會變短：Q 每輪拿到的序列長度不變，遞迴照樣不收斂。",
        "§11.4 管的是 E_G 新進來的 guarantee，管不到早就躺在 ω 裡的項目；Q 也沒有 epoch 長度的界。",
        "被依賴的那份可能走 R! 或早已只留在 ξ，剪依賴與刪項目作用在不同項目上，兩者不互相涵蓋。",
    ],
    "explanation": "eq. 12.7 的 E 同時做兩件事：「(r, x) ↦ [(r, d ∖ x) | (r, d) ↕ r, (r_s)_p ∉ x]」——後半的過濾條件 (r_s)_p ∉ x 才是把「自己已經被 accumulate」的項目整筆刪掉的那一半。少了它，eq. 12.8 的 Q(r) = g ⌢ Q(E(r, P(g))) 會無限遞迴，因為 g 裡的項目依然留在 E(r, P(g)) 中且 dependency 集合仍為空。同樣地 eq. 12.12 的 q = E(… ⌢ R^Q, P(R!)) 會讓同時出現在 R! 與 ready queue 的 report 在同一個區塊被 accumulate 兩次，而 eq. 12.33 三個 case 中的兩個（i = 0 與 i ≥ τ′ − τ）靠 E(·, ξ′[E−1]) 清掉本區塊已完成的項目（中間的 1 ≤ i < τ′ − τ 是直接清成 ⟦⟧，不套用 E）。eq. 12.8 唯一的 base case 是 g = ⟦⟧。",
    "trap": "E 是「刪項目 + 剪依賴」兩件事；只做剪依賴，Q 就不會收斂。",
},

# ─────────────────────────────────────────────────────────── 4 · L2 · concept
{
    "id": "c3-ch12-starved-dependency-fate",
    "ch": "12",
    "section": "12.1 History and Queuing",
    "gpRef": "eq. 12.8 (Q), 12.31–12.33; §12.1",
    "difficulty": 2,
    "kind": "concept",
    "tags": ["accumulation", "dependencies", "ready-queue"],
    "stem": "A report w is sitting in ω with one outstanding dependency p, and package p is never accumulated — the "
            "report carrying p was guaranteed a few blocks ago but timed out on its core and never became available. "
            "Trace w's fate under GP 0.8.0.",
    "options": [
        "Q never emits it, because its dependency set is never emptied; it is then dropped at the very next block, "
        "because E(·, ξ′[E−1]) removes any entry still carrying a dependency that is absent from ξ — which is "
        "exactly how the GP cancels a report with an unsatisfiable dependency",

        "Q never emits it, and the block that made w available is invalid: §12.1 says accumulation is cancelled "
        "entirely in the case of an invalid dependency, and cancellation is signalled by rejecting the block, so a "
        "report that times out on its core retroactively invalidates whichever later block first queued the "
        "report that depended on it",

        "Q holds it back only for a while: after E = 600 slots the dependency is deemed expired, the i ≥ τ′ − τ "
        "case stops re-applying E to that slot, and Q then treats w's dependency set as empty and accumulates it "
        "with whatever operands it has — so the work is delayed by at most one epoch but never silently lost",

        "Q never emits it, because its dependency set is never emptied; each block it is simply carried forward by the "
        "i ≥ τ′ − τ case ω′↺[m−i] = E(ω↺[m−i], ξ′[E−1]), and it vanishes at most one epoch later when the slot index "
        "wraps round and the i = 0 case overwrites that very slot with the new block's R^Q",
    ],
    "answer": 3,
    "optNotes": [
        "把 E 的語意反了：第二個參數是「已完成」的 hash 集合，只刪自己 package hash 落在其中的項目。",
        "§12.1 的 cancelled entirely 指靜默淘汰；guarantor 在 core 上逾時本來就是 §11 允許的正常結果。",
        "「到期就視為依賴滿足、照樣 accumulate」是憑空發明的規則，eq. 12.8 只挑 dependency 集合為空者。",
        "eq. 12.33 的 i ≥ τ′ − τ 逐塊把它搬過去，直到 slot index 繞回、i = 0 那格被新的 R^Q 整個覆寫。",
    ],
    "explanation": "eq. 12.8 的 Q 只挑 dependency 集合為空的項目（g = [r | (r, ∅) ↕ r]），w 永遠不會被挑中。eq. 12.33 的三個 case 決定它的壽命：i = 0 用本區塊的 R^Q 覆寫目前 slot、1 ≤ i < τ′ − τ 把跳過的 slot 清成 []、i ≥ τ′ − τ 則保留舊內容但套用 E(·, ξ′[E−1])。由於索引是 cyclic 的 ω′↺[m − i]，w 所在的 slot 在最多 E = 600 個 slot 後就會輪到 i = 0 被整個覆寫，這正好呼應 §12.1 的敘述「Each of these were made available at most one epoch ago」。GP 說的 cancelled entirely 指的是這種靜默淘汰——§12.1 沒有任何條款把 dependency 問題升級成區塊無效（§12 另有區塊有效性條件：12.18 底下 n/m 的索引衝突、以及 eq. 12.35–12.36 對 E_P 的要求，但與 dependency 無關）。",
    "trap": "ready queue 的淘汰不是超時計時器，而是 cyclic buffer 被同一個 slot index 繞回來覆寫。",
},

# ─────────────────────────────────────────────────────────── 5 · L2 · concept
{
    "id": "c3-ch12-gas-floor-vs-ceiling",
    "ch": "12",
    "section": "12.2 Execution",
    "gpRef": "§11.4 (report gas checks); eq. 12.23 (Δ1 g), 12.24 (block g); §9.1",
    "difficulty": 2,
    "kind": "concept",
    "tags": ["accumulation", "gas", "service-accounts"],
    "stem": "G_A = 10,000,000 and G_T = 3,500,000,000, while every service account carries a_g and a_m. Which statement "
            "correctly places each accumulate-gas limit — the ceilings and the per-service floors?",
    "options": [
        "Per report, §11.4 requires Σ over its digests of d_g ≤ G_A and every digest's d_g ≥ δ[d_s]_g (the destination "
        "service's a_g), both checked at guarantee time against the prior δ; per block, eq. 12.24 sets Δ+'s budget to "
        "g = max(G_T, G_A·C + Σ values(χ_Z)); and the `transfer` host call refuses with LOW unless the transfer's gas "
        "l ≥ δ[d]_m, so a deferred transfer also arrives with enough gas for the recipient's Accumulate",

        "Per report, §11.4 requires Σ over its digests of d_g ≤ G_A; per service, G_A is additionally a per-block "
        "cap enforced inside Δ1, which is why eq. 12.23 clamps that service's g at G_A instead of summing its "
        "sources; and a_g is a refund floor rather than a minimum — whatever a service leaves unspent below a_g is "
        "credited back to its balance at the end of Δ+, with a_m playing the same role for deferred transfers",

        "Both ceilings are enforced inside Δ+ at accumulation time rather than at guarantee time: eq. 12.24's "
        "budget covers the whole block and §11.4's per-report sum is re-checked there against the posterior δ, so "
        "a service whose a_g exceeds G_A can never be accumulated — which is why a_g ≤ G_A is maintained as a "
        "state invariant by the `new` host call, and a_m is bounded against G_T the same way",

        "Per report, §11.4 requires Σ over its digests of d_g ≤ G_T, G_T being the figure that bounds any single "
        "report; per block, eq. 12.24 builds Δ+'s budget out of G_A, the whole-block ceiling, which is why G_T is "
        "the larger constant of the two; and the two service-level floors run the other way round — a_g is the "
        "minimum gas per deferred transfer and a_m the minimum per work-item",
    ],
    "answer": 0,
    "optNotes": [
        "三個層級各歸各位：report 層 G_A 與 a_g（對 prior δ 檢查）、block 層 eq. 12.24、transfer 層 a_m。",
        "eq. 12.23 的 g 是三項相加、沒有任何 clamp；§9.1 的 a_g 是准入下限而不是事後回沖。",
        "§11.4 兩條 gas 條件在 guarantee 時就對 prior δ 檢查過，Δ+ 不會重驗；GP 也沒有這條不變量。",
        "數量級剛好反了：G_T 比 G_A 大 350 倍，當成單一 report 上限會讓一份 report 吃掉整塊預算。",
    ],
    "explanation": "三個層級要分清楚。(1) Report 層：§11.4 的條件是 ∀w ∈ I: Σ_{d ∈ w_d}(d_g) ≤ G_A ∧ ∀d ∈ w_d: d_g ≥ δ[d_s]_g，是在 guarantee 進來時用 prior δ 檢查，跟 §12 無關（真要在 Δ+ 重驗，posterior δ 裡的 a_g 可能已被本塊改過，反而會讓合法區塊被拒）。(2) Block 層：eq. 12.24 的 g = max(G_T, G_A·C + Σ_{x ∈ values(χ_Z)}(x))，definitions.tex 也說 G_T「should be no smaller than G_A·C + Σ」。(3) Service 層的兩個下限來自 §9.1：a_g 是「每個 work-item」執行 Accumulate 所需的最低 gas，a_m 是「每筆 deferred transfer」所需的最低 gas，後者由 `transfer` host call 以 LOW 錯誤把關。",
    "trap": "上限往下走（block g → report G_A），下限往上走（a_g / a_m → 呼叫方必須配足）；別把兩個方向搞反。",
},

# ─────────────────────────────────────────────────────────── 6 · L2 · concept
{
    "id": "c3-ch12-theta-from-yield",
    "ch": "12",
    "section": "12.3 Final State Integration",
    "gpRef": "eq. 12.18 (b), 12.25 (θ′); eq. 7.7 (β′_B)",
    "difficulty": 2,
    "kind": "concept",
    "tags": ["accumulation", "output-log", "beefy"],
    "stem": "In one block: service 5 accumulates and calls `yield` with a 32-octet hash; service 6 accumulates and burns "
            "gas but never calls `yield`; service 9 has no work-digest at all and is reached only by a deferred transfer, "
            "and it calls `yield`. What ends up in θ′, and what consumes it?",
    "options": [
        "θ′ holds one entry for every service in Δ*'s service set s, with the zero hash standing in for services "
        "that did not yield, so θ′ carries pairs for services 5, 6 and 9 alike and |θ′| = |s|, which is what lets "
        "downstream verifiers index it by position. It is a state item of its own, replaced wholesale each block, "
        "and it is what β′_B appends to",

        "b = {(s, y) | s ∈ s, y = Δ(s)_y, y ≠ ∅}, so this block contributes exactly the pairs for services 5 and 9; "
        "but θ′ is the append-only log of every accumulation output since genesis, so those two pairs are merely "
        "its tail, and the belt β_B is a cache of the Merkle root taken over that whole log",

        "b = {(s, y) | s ∈ s, y = Δ(s)_y, y ≠ ∅}, so θ′ carries exactly the pairs for services 5 and 9 — service 6 shows "
        "up in u and in the accumulation statistics S but not here. θ′ is a state item of its own, replaced wholesale each "
        "block, and it is the input to β′_B = A(β_B, M_B(s, H_K), H_K) whose super-peak is stored in the new β_H entry",

        "b = {(s, y) | s ∈ s, y = Δ(s)_y, y ≠ ∅}, but only services holding at least one work-digest in R*[..n] "
        "are members of s, so θ′ carries the pair for service 5 alone — service 9 is excluded even though it "
        "yielded, because a service reached solely by a deferred transfer can never commit an accumulation "
        "output. θ′ is replaced wholesale each block and is what β′_B appends to",
    ],
    "answer": 2,
    "optNotes": [
        "與 eq. 12.18 的 b ≠ ∅ 過濾直接衝突，也讓「零 hash」這個合法的 yield 值無從分辨。",
        "方向顛倒：θ′ 每塊整批換掉（state key C(16)），真正跨區塊累積的是 §7 的 β_B。",
        "b ≠ ∅ 濾掉沒呼叫 yield 的 service 6，而 transfer 收款方本來就在 s 裡，所以 5 與 9 都入列。",
        "eq. 12.18 的 s 是三段聯集，純收款與 always-accumulate 服務同樣會被 Δ1 呼叫、同樣能 yield。",
    ],
    "explanation": "eq. 12.18 定義 b = {(s, b) | s ∈ s, b = Δ(s)_y, b ≠ ∅}，條件 b ≠ ∅ 表示「沒呼叫 yield 就不入列」，所以只燒 gas 的服務只會出現在 u（gas 使用量）與 eq. 12.28 的 S，不會出現在 θ′。Δ* 的 service 集合 s = {d_s | r ∈ r, d ∈ r_d} ∪ K(f) ∪ {t_d | t ∈ t}，transfer 的收款方本來就在裡面。eq. 12.25：θ′ ≡ ⟦(s, h) ∈ b⟧，它是 σ 裡獨立的一項（state key C(16)），每個區塊整批換掉，不是自創世以來的累積；真正累積的是 §7 的 β_B（eq. 7.7 用 Keccak 做 M_B 與 MMB append），其 super-peak 才寫進 β_H。",
    "trap": "沒 yield 就沒 commitment：θ′ 的長度由 yield 次數決定，不由 |s| 決定。",
},

# ─────────────────────────────────────────────────────────── 7 · L2 · concept
{
    "id": "c3-ch12-provide-two-places",
    "ch": "12",
    "section": "12.2 Execution / 12.4 Preimage Integration",
    "gpRef": "eq. 12.18 (d′), 12.20 (I), 12.21 (Y), 12.37",
    "difficulty": 2,
    "kind": "concept",
    "tags": ["accumulation", "preimages", "provide"],
    "stem": "The preimage-integration function I is applied twice during a block's transition. Where are the two "
            "applications, and what does its Y predicate silently discard?",
    "options": [
        "Once inside Δ* as e_d′ = I((e_d ∪ n) ∖ m, ⋃_{s ∈ s} Δ(s)_p) — folding in the blobs offered by the `provide` "
        "host call only after newly created and removed services have been merged — and once at the very end as "
        "δ′ = I(δ‡, E_P). Y(d, s, i) is ⊥ unless s ∈ K(d) and d[s]_l[(H(i), |i|)] = [], so a blob aimed at a service "
        "ejected in the same round, or at a request that is not merely solicited, is dropped without prejudice",

        "Only once, at the very end as δ′ = I(δ‡, E_P): the `provide` host call writes straight into the "
        "service's a_p and a_l during accumulation, so Δ* has nothing left to integrate. Y(d, s, i) is ⊥ unless "
        "s ∈ K(d) and d[s]_l[(H(i), |i|)] = [], so a blob aimed at a service ejected in the same round is dropped "
        "without prejudice — but that can only ever bite the extrinsic, never a `provide`",

        "Twice — once inside Δ* and once at the very end — but both applications take E_P as their second "
        "argument, the blobs offered by `provide` having been merged into E_P before Δ* runs. Y(d, s, i) "
        "additionally requires the blob to be under W_C = 4,000,000 octets and the service to hold the storage "
        "deposit for it, and a failure of either condition makes the block invalid rather than dropping the blob",

        "Once inside Δ1 for each accumulating service — so each service folds in its own provisions before Δ* "
        "merges the account dictionaries — and once at the very end as δ′ = I(δ‡, E_P). Y(d, s, i) accepts a "
        "request slot of the form [] or [x, y], i.e. solicited, or previously available and then forgotten, which "
        "is what lets the same preimage be provided twice over a service's lifetime",
    ],
    "answer": 0,
    "optNotes": [
        "eq. 12.18 的 I 在 n 併入、m 移除之後才收 provisions，eq. 12.37 的 I 再收 E_P，兩處各司其職。",
        "漏掉 Δ* 這一層的合流：eq. 12.18 的 e_d′ 就是用 I 把 ⋃ Δ(s)_p 併進去的。",
        "eq. 12.20–12.21 的 Y 只有兩個條件，沒有 W_C 與押金，且不合格是 disregarded 而非讓區塊無效。",
        "Δ1 只把 provisions 當輸出回傳；[x, y] 代表曾 available 後被 forget，違反 Y 的等號條件。",
    ],
    "explanation": "eq. 12.18 的 e_d′ = I((e_d ∪ n) ∖ m, ⋃_{s ∈ s} Δ(s)_p)：`provide` host call 產生的 provisions Δ(s)_p 是在 Δ* 這一層、而且是在新建服務 n 併入、被刪服務 m 移除「之後」才整合，所以同一輪被 eject 掉的服務收不到 blob（否則 n 與 m 還沒算出來，就無法判斷目標 service 是否還存在）。eq. 12.37 的 δ′ = I(δ‡, E_P) 是第二次，處理 preimage extrinsic。eq. 12.21 的 Y(d, s, i) 只在 s ∈ K(d) 且 d[s]_l[(H(i), |i|)] = ⟦⟧ 時為真，GP 原文也明說「Preimage provisions into services which no longer exist or whose relevant request is dropped are disregarded」——是靜默略過，不是讓區塊無效。",
    "trap": "I 出現兩次：Δ* 裡收 `provide`、區塊尾端收 E_P；兩次的丟棄都是「without prejudice」，不會讓區塊無效。",
},

# ─────────────────────────────────────────────────────────── 8 · L2 · code · delta
{
    "id": "c3-ch12-code-accumulation-statistics",
    "ch": "12",
    "section": "12.3 Final State Integration",
    "gpRef": "eq. 12.27–12.28; eq. 12.17 (Δ+ output)",
    "difficulty": 2,
    "kind": "code",
    "tags": ["accumulation", "statistics", "code", "delta-0.8.0"],
    "stem": "This is the team's GP 0.7.2 accumulation-statistics builder S. Which gap against GP 0.8.0 must be closed?",
    "code": {
        "lang": "go",
        "caption": "internal/accumulation/deferred_transfers.go (calculateAccumulationStatistics), 0.7.2 main",
        "src": """// (12.28–12.29) S ≡ {(s ↦ (G(s), N(s))) | G(s)+N(s) ≠ 0}
func calculateAccumulationStatistics(serviceGasUsedList types.ServiceGasUsedList,
	n types.U64) types.AccumulationStatistics {
	G := map[types.ServiceID]types.Gas{} // G(s)
	for _, serviceGasUsed := range serviceGasUsedList {
		G[serviceGasUsed.ServiceID] += serviceGasUsed.Gas
	}

	S := types.AccumulationStatistics{}
	for s, Gs := range G {
		Ns := types.U64(len(getWorkResultByService(s, n)))

		if types.U64(Gs)+Ns == 0 {
			continue // skip, N(S) = []
		}

		S[s] = types.GasAndNumAccumulatedReports{
			Gas:                   Gs,
			NumAccumulatedReports: Ns,
		}
	}
	return S
}""",
    },
    "options": [
        "N(s) must count whole work-*reports*, not digests: eq. 12.28 iterates r ↕ R*[..n] and counts each report "
        "once for the service that owns it, whereas this code counts one entry per matching digest, so a report "
        "carrying two digests for the same service is double-counted",

        "0.8.0 makes S ∈ ⟨N_S → (N, N, N_G)⟩ a three-tuple S(s) = (N(s), T(s), G(s)); the missing middle element T(s) "
        "counts the processed deferred transfers whose destination is s, which forces Δ+ to return a fifth component — "
        "the processed-transfer sequence t ⌢ t† — and the inclusion filter becomes S(s) ≠ (0, 0, 0) rather than a sum test",

        "G(s) must be the gas *allotted* — Σ d_g over the service's digests, the very figure §11.4 checks against "
        "G_A — rather than the gas actually used, otherwise a service that runs out of gas is under-charged in the "
        "statistics that feed π_S; the two-element shape and the sum-based inclusion filter are both already "
        "right for 0.8.0",

        "S must carry an entry for every service in δ, with the all-zero triple for untouched services, so that "
        "the dictionary's key set is stable from block to block and π_S's serialization keeps a fixed length; the "
        "shape does become a triple in 0.8.0, but the new element is the transfer count sitting *last*, and it is "
        "Δ*, not Δ+, that returns the processed-transfer sequence it is built from",
    ],
    "answer": 1,
    "optNotes": [
        "eq. 12.28 的 N(s) 明確是 d ↕ r_d 逐個 digest 數，不是逐 report 數。",
        "eq. 12.27–12.28 的三元組與 S(s) ≠ (0,0,0) 篩選，逼得 eq. 12.17 的 Δ+ 多回傳 t ⌢ t†。",
        "G(s) ≡ Σ_{(s, u) ∈ u}(u) 就是實際用掉的 gas，不是 §11.4 檢查的宣告上限。",
        "S 只收非零項（δ‡ 才只對 K(S) 蓋 a_a）；T(s) 在三元組中間，且 t ⌢ t† 由 Δ+ 而非 Δ* 回傳。",
    ],
    "explanation": "GP 0.8.0 eq. 12.27 寫的是 S ∈ ⟨N_S → (N, N, N_G)⟩，eq. 12.28 是 S ≡ {(s ↦ S(s)) | S(s) ≠ (0, 0, 0)}，其中 S(s) ≡ (N(s), T(s), G(s))，T(s) ≡ |[t | t ↕ t, t_d = s]| 就是「送到 s 的已處理 deferred transfer 筆數」（GP PR #502 “Add back processed transfer count to service statistics”）。要算得出 T(s)，eq. 12.17 的 Δ+ 必須多回傳一個 processed-transfer 序列（回傳值是 ⟨i + j, e′, b* ∪ b, u* ⌢ u, t ⌢ t†⟩），而這份 0.7.2 程式的 OuterAccumulationOutput 只有四個欄位、型別也只是 (Gas, NumAccumulatedReports) 兩元組，篩選條件寫成 Gs + Ns == 0 也不等價於三元組全零。S 只收非零項，正是為了讓 δ‡ 只對真的被 accumulate 的服務蓋上 a_a = τ′，而 S 又是 π_S 的來源之一（eq. 13.14 的 K(S)）。",
    "trap": "0.8.0 的 accumulation statistics 是三元組 (N, T, G)；漏掉 T 會連帶讓 Δ+ 的回傳值少一個分量。",
},

# ─────────────────────────────────────────────────────────── 9 · L2 · rationale
{
    "id": "c3-ch12-why-R-star-is-a-sequence",
    "ch": "12",
    "section": "12.1 History and Queuing",
    "gpRef": "eq. 11.17 (R), 12.4, 12.11 (R*), 12.17, 12.31",
    "difficulty": 2,
    "kind": "rationale",
    "tags": ["accumulation", "determinism", "availability"],
    "stem": "R, R!, R^Q and R* are all sequences rather than sets, even though only membership decides which reports are "
            "eligible. Why does the ordering matter for consensus, and where is it fixed?",
    "options": [
        "Because Δ+ accumulates only the gas-fitting prefix R*[..i] and then records ξ′[E−1] = P(R*[..n]): a different "
        "ordering yields a different prefix and hence a different posterior state. The order is pinned right back at "
        "eq. 11.17, where R is built by walking cores in ascending core index over ρ† and keeping those with more than "
        "2/3·|κ| assurances; R! preserves that order and Q appends the queued reports in dependency-resolution rounds",

        "It does not matter for the posterior state. Δ* accumulates services in parallel, and any permutation of "
        "R* selects the same gas-fitting prefix anyway, because eq. 12.17 picks the maximal i by a sum and "
        "addition is commutative; that is exactly why b is a set while u is merely a convenient sequence, and why "
        "the GP bothers to fix an order only at eq. 12.11, purely so the prose can talk about R* concretely",

        "Ordering only affects the accumulation statistics S and therefore π_S, because eq. 12.28's N(s) walks "
        "R*[..n] in order; the service state δ† is order-independent, since each service's Δ1 is a pure function "
        "of its own operands and its own prior account, and ξ′[E−1] = P(R*[..n]) is a set, so whatever order its "
        "members were produced in is lost the moment it is written",

        "Because Δ+ accumulates only the gas-fitting prefix R*[..i], so when gas runs short the ordering decides "
        "what gets dropped. The order is pinned at eq. 11.17, where R is built by ranking cores on how many "
        "assurances each collected, most-assured first, so that the best-attested reports are the ones "
        "accumulated and the marginal ones are deferred into ω",
    ],
    "answer": 0,
    "optNotes": [
        "eq. 12.17 只吃 gas 前綴、eq. 12.31 寫 ξ′[E−1] = P(R*[..n])，順序因此是共識的一部分。",
        "把「Δ* 內服務可平行」誤讀成「報告可任意重排」：eq. 12.17 選的是前綴，重排會換掉入選的那個集合。",
        "ξ′[E−1] 雖是集合，決定它內容的仍是前綴長度 n，所以 δ† 與 state root 同樣隨順序而變。",
        "eq. 11.17 走的是 c ↕ N_C；2/3·|κ| 只是布林門檻，跨過就入列，沒有任何名次可言。",
    ],
    "explanation": "eq. 12.17 選的是「最大的前綴 i」使得 Σ_{r ∈ r[..i], d ∈ r_d}(d_g) + Σ_{t ∈ t}(t_g) + Σ_{x ∈ values(f)}(x) ≤ g，而 eq. 12.31 又用 ξ′[E−1] = P(R*[..n]) 把「本區塊做完了哪些 package」寫進 state。這兩處都只看前綴，所以順序一旦不同，被 accumulate 的集合、ξ′、δ† 乃至 state root 全都不同。順序的源頭在 eq. 11.17：R ≡ [(ρ†[c]_g)_w | c ↕ N_C, Σ_{a ∈ E_A} a_f[c] > 2/3·|κ|]，是以 core index 遞增走訪，接著 eq. 12.4 的 R! 沿用該順序、eq. 12.11 的 R* = R! ⌢ Q(q) 再把佇列項目依相依解開的輪次接上。",
    "trap": "「哪些會被 accumulate」由 gas 前綴決定，所以序列順序就是共識的一部分；core index 遞增是唯一的來源。",
},

# ─────────────────────────────────────────────────────────── 10 · L3 · delta
{
    "id": "c3-ch12-accseq-n-with-transfers",
    "ch": "12",
    "section": "12.2 Execution",
    "gpRef": "eq. 12.17 (Δ+), 12.24, 12.28",
    "difficulty": 3,
    "kind": "delta",
    "tags": ["accumulation", "transfers", "gas", "delta-0.8.0"],
    "stem": "Mid-recursion inside Δ+, the remaining report sequence is empty but the previous Δ* round emitted three "
            "deferred transfers t, and the free-accumulation map handed to this call is ∅. Does Δ+ do any more work, and "
            "what does it hand back in GP 0.8.0?",
    "options": [
        "No. The GP's termination test is the prefix length i, and with r = ⟦⟧ the maximal gas-fitting prefix is "
        "i = 0, so the base case ⟨0, e, ∅, ⟦⟧, ⟦⟧⟩ fires and Δ* is never invoked; the three pending transfers are "
        "carried into the next block through ω, which is precisely why ω is typed to hold them alongside the "
        "deferred reports, and their gas is re-charged against that block's budget g rather than this one's",

        "Yes — the test n = i + |t| + |f| = 3 ≠ 0 fires — but the round is a no-op: Δ*'s service set is "
        "s = {d_s | r ∈ r, d ∈ r_d} ∪ K(f) alone, so with r[..i] empty and f = ∅ it is empty too, the three "
        "transfers are discarded, and only the balances already credited by the earlier `transfer` host calls "
        "survive into δ†; u and b therefore come back empty and the three destinations contribute nothing to "
        "eq. 12.28's T(s)",

        "Yes. The GP's termination test is n = i + |t| + |f| = 0 + 3 + 0 = 3 ≠ 0, so Δ* is still invoked; its service set "
        "s = {d_s | r ∈ r, d ∈ r_d} ∪ K(f) ∪ {t_d | t ∈ t} reduces to the three destinations, which are accumulated on the "
        "transfers alone. The result is ⟨i + j, e′, b* ∪ b, u* ⌢ u, t ⌢ t†⟩, whose fifth component — the processed "
        "transfers — is what T(s) in eq. 12.28 counts",

        "Yes — the test n = i + |t| + |f| = 3 ≠ 0 fires and the three destinations are accumulated on the "
        "transfers alone — but Δ+ still returns the four-tuple ⟨n, e′, b, u⟩ exactly as in 0.7.2; the processed "
        "transfers that T(s) needs are recovered afterwards by diffing δ† against δ for balance movements, "
        "eq. 12.28 being defined over that reconstruction rather than over anything Δ+ hands back",
    ],
    "answer": 2,
    "optNotes": [
        "混淆了 i 與 n；ω 型別上只放 report 與 hash 集合，deferred transfer 從不進 σ。",
        "漏掉 eq. 12.18 明列的第三段 {t_d | t ∈ t}，那是純收款服務進入 accumulate 的唯一途徑。",
        "終止條件是 n = i + |t| + |f|；s 縮成三個收款方，回傳五元組的 t ⌢ t† 正是 T(s) 的來源。",
        "餘額變化是淨額：同時有 digest、有轉入又有轉出的 service 根本數不出 transfer 筆數。",
    ],
    "explanation": "eq. 12.17 的終止條件不是「還有沒有 report」，而是 n = i + |t| + |f|：只要還有待處理的 deferred transfer 或還有 free-accumulation 服務，Δ+ 就會再跑一輪 Δ*。eq. 12.18 的服務集合 s 明確包含 {t_d | t ∈ t}，所以純粹被轉帳打到的服務也會被 accumulate（Δ1 的 g = U(f[s], 0) + Σ_{t_d = s}(t_g) + Σ digests，此時只剩轉帳那一項），這正是 0.7.1 之後把 on-transfer 併進 accumulate 的結果。GP 0.8.0 的 Δ+ 回傳五元組，最後一項 t ⌢ t† 是「本次遞迴實際處理掉的 transfer 序列」，eq. 12.28 的 T(s) 就靠它計數（對照 0.7.2 只回傳四元組，這是團隊必須補的差異）。",
    "trap": "Δ+ 的停機條件是 n = i + |t| + |f|；report 用完不代表結束，轉帳與 always-accumulate 也能把遞迴撐著。",
},

# ─────────────────────────────────────────────────────────── 11 · L3 · concept
{
    "id": "c3-ch12-prior-privileged-index-reads",
    "ch": "12",
    "section": "12.2 Execution",
    "gpRef": "eq. 12.18 (Δ*), 12.19 (R)",
    "difficulty": 3,
    "kind": "concept",
    "tags": ["accumulation", "privileges", "prior-posterior"],
    "stem": "Inside Δ*, core c's posterior authorizer queue φ′[c] and the posterior staging keys ι′ are each lifted out "
            "of exactly one service's Δ1 output. Whose output, and selected by which version of χ?",
    "options": [
        "φ′[c] = ((Δ(χ_A[c])_e)_q)[c] and ι′ = (Δ(χ_V)_e)_i — the *prior* per-core assigner and the *prior* delegator. "
        "Even when this same round rewrites χ′_A[c] or χ′_V, the queue and the keys still come from whoever held the "
        "privilege when the round began, and only that service's own copy of the component is read, core index by core index",

        "φ′[c] = ((Δ(χ_M)_e)_q)[c] and ι′ = (Δ(χ_M)_e)_i — both are lifted out of the manager's output "
        "e* = Δ(χ_M)_e, because only the manager may alter any component of χ; the assigner and the delegator "
        "merely stage requests inside their own partial states, which the manager's Accumulate ratifies before "
        "Δ* merges them",

        "φ′[c] = ((Δ(χ′_A[c])_e)_q)[c] and ι′ = (Δ(χ′_V)_e)_i — the *posterior* per-core assigner and the "
        "*posterior* delegator. A service granted the assign privilege during this very block can therefore "
        "immediately install the queue the block will use, and only that service's own copy of the component is "
        "read, core index by core index",

        "φ′[c] = R(φ[c], (e*_q)[c], ((Δ(χ_A[c])_e)_q)[c]) — it is merged across the manager and the prior assigner "
        "with R(o, a, b), exactly as χ′_A[c] is; and ι′ is taken from whichever service in s wrote it last when s "
        "is walked in ascending service index, so a higher-indexed service can overwrite the delegator's copy",
    ],
    "answer": 0,
    "optNotes": [
        "eq. 12.18 的 e_q′[c] 與 e_i′ 括號裡是 Δ* 的輸入 χ_A[c]、χ_V，也就是回合開始時的持有者。",
        "會漏掉 eq. 12.19 註解「This allows privileges to be owned」的整個設計；e* 只供出 e_m′ 與 e_z′。",
        "同一區塊剛拿到 assign 特權的服務要等下一塊才能改 φ′[c]，式子讀的就是 prior。",
        "R 只出現在 e_a′、e_v′、e_r′ 三行；讓任何服務都能覆寫 ι′ 等於誰都能改下一輪的 validator 金鑰。",
    ],
    "explanation": "eq. 12.18 分得很細。**誰擁有特權**用 R 合併：∀c, e_a′[c] = R(e_a[c], (e*_a)[c], ((Δ(e_a[c])_e)_a)[c])，以及 e_v′、e_r′ 同理；而 e_m′ 與 e_z′ 直接取自 manager 的輸出 e* = Δ(m)_e，不經過 R。**特權作用的內容**則另外一條路：e_q′[c] = ((Δ(e_a[c])_e)_q)[c] 與 e_i′ = (Δ(e_v)_e)_i，括號裡的 e_a[c]、e_v 是 Δ* 的輸入、也就是 prior 的 χ_A[c] 與 χ_V。另外 §8 的 α′ 之所以必須在 accumulation 之後才算，authorization.tex 給的理由是「Since α′ is dependent on φ′ … this step must be computed after accumulation, the stage in which φ′ is defined」——那是 α′ 讀 φ′ 造成的順序，與這條 prior/posterior 選擇規則無關。",
    "trap": "χ′ 用 R 合併，但 φ′[c] 與 ι′ 只讀 prior χ_A[c] / χ_V 那一個服務的輸出——同區塊拿到特權，下一區塊才生效。",
},

# ─────────────────────────────────────────────────────────── 12 · L3 · code
{
    "id": "c3-ch12-code-delta-star-map-order",
    "ch": "12",
    "section": "12.2 Execution",
    "gpRef": "eq. 12.18 (u, t′)",
    "difficulty": 3,
    "kind": "code",
    "tags": ["accumulation", "determinism", "transfers", "code"],
    "stem": "In the team's Δ*, the service set s is a Go map and this loop collects u and t′ from the per-service results. "
            "Which GP 0.8.0 requirement does it violate, and what is the observable symptom?",
    "code": {
        "lang": "go",
        "caption": "internal/accumulation/accumulation.go (set_s + ParallelizedAccumulation result loop), condensed",
        "src": """func set_s(r []types.WorkReport, f types.AlwaysAccumulateMap,
	t []types.DeferredTransfer) map[types.ServiceID]bool {
	s := make(map[types.ServiceID]bool, len(r)*2+len(f)+len(t))
	for _, w := range r {
		for _, r := range w.Results {
			s[r.ServiceID] = true // rd
		}
	}
	for serviceID := range f { // K(f)
		s[serviceID] = true
	}
	for _, deferredTransfer := range t {
		s[deferredTransfer.ReceiverID] = true // td
	}
	return s
}

// ... later, in ParallelizedAccumulation:
// Process results from each service accumulation
for service_id := range s {
	singleOutput := cache[service_id]
	// u = [(s, ∆(s)u) S s <− s]
	u = append(u, types.ServiceGasUsed{ServiceID: service_id,
		Gas: singleOutput.GasUsed})
	// t = [∆(s)t S s <− s]
	tPrime = append(tPrime, singleOutput.DeferredTransfers...)
}""",
    },
    "options": [
        "Nothing consensus-relevant: eq. 12.18 writes t′ as a set, and u is only ever consumed by eq. 12.28's "
        "G(s), which sums per service, so both are order-independent. The flattened ⌢⌢t′ does reach the next Δ+ "
        "round in an arbitrary order, but eq. 12.23 re-sorts each destination's i^T by sender before Ψ_A sees it, "
        "so two nodes importing the same block still agree on the state root",

        "Eq. 12.18 writes u = ⟦(s, Δ(s)_u) | s ↕ s⟧ and t′ = ⟦Δ(s)_t | s ↕ s⟧ with the ordered-iteration marker, i.e. "
        "ascending service index, whereas Go randomises map iteration. The flattened ⌢⌢t′ therefore reaches the next Δ+ "
        "round permuted, so each destination's i^T — and hence Ψ_A's operand sequence, the balances it credits and the "
        "resulting state root — can differ between two nodes importing the very same block",

        "Eq. 12.18's ↕ marker does demand a deterministic walk, but over *report* order — the order in which each "
        "service's first digest appears in r[..i] — so sorting by ascending service index would be exactly as "
        "wrong as the map order. The symptom is the same either way: the flattened ⌢⌢t′ reaches the next Δ+ round "
        "permuted and two nodes importing the same block disagree on the state root",

        "The violation is in set_s rather than in the loop: only services carrying a work-digest may contribute to "
        "u and t′, so transfer destinations and always-accumulate services have to be filtered back out of s "
        "before this loop runs. The map iteration itself is harmless, because eq. 12.18 marks u and t′ with ∈ "
        "rather than ↕ and both are consumed order-insensitively",
    ],
    "answer": 1,
    "optNotes": [
        "t′ 是序列不是集合；eq. 12.23 的 i^T = ⟦t | t ↕ t, t_d = s⟧ 沿用傳進來的順序，不會另外重排。",
        "§3.7.1 的 ↕ 是依元素本身遞增，s 的元素是 service index，而 Go map 迭代是刻意隨機化的。",
        "GP 沒有第二套排序規則：↕ 依元素本身遞增，正解就是 ascending service index。",
        "s 的定義本來就含 K(f) 與 {t_d}，濾掉會讓 always-accumulate 與純收款服務完全不被 accumulate。",
    ],
    "explanation": "eq. 12.18 對這兩個輸出都用了有序迭代記號：u = ⟦(s, Δ(s)_u) | s ↕ s⟧、t′ = ⟦Δ(s)_t | s ↕ s⟧，而 §3 的 notation 說明 ↕ 代表依元素本身遞增排序，對 s ∈ N_S 就是 service index 由小到大。Go 的 `for k := range m` 是刻意隨機化的，於是 tPrime 的串接順序在每個節點都不同；由於 eq. 12.17 會把 t* 餵回下一輪，而 eq. 12.23 的 i^T = ⟦t | t ↕ t, t_d = s⟧ 直接沿用該序列，最後 Ψ_A 收到的 operand 序列與 `fetch` 讀出的內容就不同——同一個區塊在不同節點算出不同 state root，典型症狀是 fuzzer / trace 測試偶發性不一致（團隊也用一個 `sort.Slice(iT, ...)` by SenderID 去掩蓋，但 sort.Slice 不穩定，同一 sender 的多筆轉帳仍可能被重排）。",
    "trap": "GP 的 ↕ 不是裝飾：任何從集合展開成序列的地方，Go map 迭代都是共識殺手。",
},

]
