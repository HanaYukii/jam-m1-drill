# -*- coding: utf-8 -*-
# Chapter 11 — Reporting and Assurance (GP 0.8.0)
ITEMS = [
{
 "id": "ch11-rho-state",
 "ch": "11", "section": "11.1 State", "gpRef": "eq. 11.1 (ρ)",
 "difficulty": 2, "kind": "delta", "tags": ["reports", "state", "delta-0.8.0"],
 "stem": "What does each entry of ρ (the availability assignments) hold in GP 0.8.0, and why did PR #494 change it?",
 "options": [
  "ρ ∈ [(g ∈ 𝔾 guarantee, t ∈ N_T timeslot)?]_C — the whole guarantee, i.e. the work-report together with its 2–3 guarantor signatures, plus the slot at which it was reported",
  "ρ ∈ [(w ∈ ℝ work-report, t ∈ N_T timeslot)?]_C — the report and its slot but no signatures, as in 0.7.2; guarantor identities are recovered from the guarantees recorded in β instead",
  "ρ ∈ [(h ∈ ℍ report hash, t ∈ N_T timeslot)?]_C — only a 32-octet commitment per core, the guarantee itself being held off-chain by the guarantors until the report accumulates",
  "ρ ∈ [(g ∈ 𝔾 guarantee, t ∈ N_T timeslot, f ∈ bits[|κ|])?]_C — the guarantee, the slot, and a bitfield of assurances accumulated across blocks until the super-majority is reached"
 ],
 "answer": 0,
 "optNotes": [
  "0.8.0 (#494) 改存整個 guarantee，正是為了留住 guarantor 的身分與簽章。",
  "(w, t) 是 0.7.2 的型別；β 每筆只有 header hash、state root、super-peak、slot 與字典，無簽章可翻。",
  "eq. 11.17 要把 (ρ†[c]_g)_w 這份完整 report 交給 accumulation，光有 hash 拼不回 digest。",
  "可用性是單一區塊內的統計：eq. 11.17 只對本塊 E_A 求和，state 裡沒有跨塊累加的 bitfield。",
 ],
 "explanation": "eq. 11.1：ρ ∈ [(g ∈ G, t ∈ N_T)?]_C。0.7.2 存的是 (w report, t)；0.8.0 (#494) 改存整個 guarantee（含 2–3 個 guarantor 簽章），理由：「To determine the guarantors to try directly fetching the bundle from」以及「In the case of a dispute, the guarantor signatures are needed to construct a disputes extrinsic（culprits）」。t 是 report 被 guarantee 進鏈的 slot（τ′），用來算 timeout U = 5。這也改變了 C(10) 的 state serialization：↕(g, E_4(t))。",
 "trap": "遷移點：ρ 的型別與序列化都變了（issue #1012 樹）。"
},
{
 "id": "ch11-workreport-fields",
 "ch": "11", "section": "11.1.1 Work Report", "gpRef": "eq. 11.2–11.3",
 "difficulty": 2, "kind": "concept", "tags": ["reports"],
 "stem": "A work-report (eq. 11.2, of the set ℝ) is a tuple (s, c, c, a, t, l, d, g) — bold c is the refinement context, plain c the core index. Which field description is WRONG?",
 "options": [
  "s — the availability specification (package hash, bundle length, erasure root, shard count, segment root, segment count)",
  "l — the segment-root lookup dictionary (work-package hash → segment root), which together with the context's prerequisites is limited to J = 8 entries",
  "g — the total gas used by all refine invocations in the package",
  "d — the work-digests, between 1 and I = 16 of them"
 ],
 "answer": 2,
 "optNotes": [
  "eq. 11.2 的第一欄 s 就是 avspec，六個子欄位 (p, l, u, v, e, n) 也列對了。",
  "eq. 11.3 就是 |l| + |c_p| ≤ J = 8，這個共用預算的描述無誤。",
  "g 記的是 Is-Authorized 消耗的 gas；refine 的用量在每個 digest 自己的 u 欄位。",
  "eq. 11.2 的 d ∈ [𝔻]_{1:I}，I = 16，digest 數的上下界都對。",
 ],
 "explanation": "eq. 11.2：ℝ ≡ (s, **c**, c, a, **t**, **l**, **d**, g)，八個欄位——**s** avspec（availability specification 𝕐，描述 bundle 怎麼被 erasure-code 出去）、**c**（粗體）refinement context ℂ（anchor 四件組 + lookup anchor + prerequisites）、c（細體）core index、**a** authorizer hash、**t** authorizer trace（Ψ_I 的輸出）、**l** segment-root lookup（把 package hash 對應到 segment root）、**d** ∈ ⟦𝔻⟧_{1:I} 各個 work-item 的 digest、**g** authgasused。**g 是這題的陷阱**：report 層級的 g 記的是**授權階段**（Ψ_I）用掉的 gas，而每個 item 各自 refine 用掉多少，記在它自己的 digest 裡（𝔻 的 gas 欄位）。兩層各有一個 gas 欄位、命名相近但語意完全不同，是這章最容易記混的地方——問「這份 report 總共花了多少 gas」時，正確答案是 g 加上所有 digest 的 gas，不是 g 本身。**另外記住 eq. 11.3 的預算**：|l| + |(c_p) prerequisites| ≤ J = 8——segment-root lookup 的筆數與 refinement context 裡的前置依賴**共用同一個 8 的額度**，不是各自 8。這個上限存在是為了讓依賴圖的深度與寬度都有界，accumulate 的排程才不會爆掉。",
 "trap": "report 層級的 g = auth gas；digest 層級的 u = refine gas；digest 的 g = accumulate gas limit。"
},
{
 "id": "ch11-refinement-context",
 "ch": "11", "section": "11.1.2 Refinement Context", "gpRef": "eq. 11.4",
 "difficulty": 2, "kind": "delta", "tags": ["reports", "delta-0.8.0"],
 "stem": "Which fields does the refinement context (eq. 11.4, of the set ℂ) contain in GP 0.8.0 (PR #526)?",
 "options": [
  "Anchor: header hash a, timeslot n, posterior state root s, accumulation-output-log super-peak b; lookup-anchor: header hash l, timeslot t, posterior state root r; prerequisites p (a set of package hashes) — 8 fields",
  "Anchor: header hash a, posterior state root s, accumulation-output-log super-peak b; lookup-anchor: header hash l, timeslot t; prerequisites p (a set of package hashes) — 6 fields, unchanged from 0.7.2",
  "Anchor: header hash a, timeslot n, posterior state root s, BEEFY root b; lookup-anchor: header hash l, timeslot t, posterior state root r; core index c and prerequisites p (a set of package hashes) — 9 fields",
  "Anchor: header hash a, timeslot n, prior state root s, accumulation-output-log super-peak b; lookup-anchor: header hash l, timeslot t, prior state root r; prerequisites p (a set of package hashes) — 8 fields"
 ],
 "answer": 0,
 "optNotes": [
  "0.8.0 #526 補上的正是 anchor 的 timeslot n 與 lookup anchor 的 posterior state root r，共八欄。",
  "(a, s, b, l, t, p) 六欄是 0.7.2 的型別；少了 n，eq. 11.36 就沒有 x_n = y_t 這一項可比。",
  "b 是 accumulation-output super-peak（BEEFY root 是舊名），而 core index 是 w_c、不在 ℂ 裡。",
  "兩個 root 都是 posterior：eq. 11.36 比 β† 那筆的 state root，eq. 11.38 比子塊 header 的 H_R。",
 ],
 "explanation": "eq. 11.4（0.8.0）：ℂ ≡ (a anchor hash, n anchor slot, s anchor posterior state root, b anchor accumulation-output super-peak, l lookup-anchor hash, t lookup-anchor slot, r lookup-anchor posterior state root, p prerequisites)。#526「Expose lookup anchor posterior root and anchor slot in refinement context」新增了 anchor 的 timeslot n 與 lookup anchor 的 posterior state root r。驗證：anchor 四元組要匹配 β† 的某筆（eq. 11.36：hash、state root、super-peak b、timeslot）；lookup anchor 的三元組要在 ancestors A 裡找到（eq. 11.38：h_T = t、H(h) = l、且其子塊 h′ 的 H_R = r）。你們 issue #1022 提到「8-field RefineContext」。",
 "trap": "b 是 β 的 accumulation-output super-peak（Keccak MMR），不是 BEEFY root 這個舊名。"
},
{
 "id": "ch11-avspec",
 "ch": "11", "section": "11.1.3 Availability", "gpRef": "eq. 11.5, 11.31",
 "difficulty": 2, "kind": "concept", "tags": ["reports", "availability"],
 "stem": "The availability specification (eq. 11.5) is s ≡ (p, l, u, v, e, n). What do u, v and e denote, and what constraint does eq. 11.31 place on v?",
 "options": [
  "u = erasure root, the Merkle root over the v chunks that erasure-code the bundle plus exported segments; v = the erasure-chunk count, which eq. 11.31 forces to equal |κ′|; e = segment root, a constant-depth tree over the exported segment hashes; n = the segment count",
  "u = segment root over the exported segment hashes; v = the number of work-items in the package, which eq. 11.31 forces to be at most I = 16; e = erasure root over the coded chunks; n = the number of validators assuring the core",
  "u = erasure root, the Merkle root over the v chunks that erasure-code the bundle plus exported segments; v = the erasure-chunk count, which eq. 11.31 fixes at 1023 in every configuration; e = segment root, a constant-depth tree over the exported segment hashes; n = the segment count",
  "u = the hash of the auditable work bundle; v = the number of guarantors credentialing the report, which eq. 11.31 forces to be 2 or 3; e = the erasure root of the bundle's extrinsics; n = the index of the core the package was built for"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 11.31 要求 (w_s)_v = |κ′|：一個 chunk 發給一個 assurer，數量必須等於 assurer 集合大小。",
  "u 與 e 對調了；v 也不是 work-item 數（那是 eq. 11.2 的 d ∈ [𝔻]_{1:I}），n 更不是 validator 數。",
  "eq. 11.31 比的是 |κ′|，而 validator 數是 6 到 1023 之間 3 的倍數，寫死 1023 正是移植 bug。",
  "p 才是 package hash、l 是 bundle 長度；2–3 是 credential 長度（eq. 11.24），core index 是 w_c。",
 ],
 "explanation": "eq. 11.5：s ≡ (p package hash, l bundle length, u erasure root, v ∈ 𝕍 erasure shards, e segment root, n segment count)。eq. 11.31：∀w ∈ I：(w_s)_v = |κ′|——GP 的理由是「As one chunk is distributed to each assurer, the number of chunks must equal the size of the assuring validator set」（0.8.0 因 validator 數可變而必須明確檢查）。兩個 root 分工不同：erasure root 承諾了審計所需的全部資料（bundle shard + segment shards），segment root 則讓後續 package 的 import 可驗證重建出來的 segment。",
 "trap": "erasure shard 數 v = |κ′|（posterior）：tiny 6、full 1023。別把 v（shards）跟 n（segment count）記反。"
},
{
 "id": "ch11-work-errors",
 "ch": "11", "section": "11.1.4 Work Digest", "gpRef": "eq. 11.6–11.7",
 "difficulty": 2, "kind": "concept", "tags": ["reports", "errors"],
 "stem": "A work-digest's result is either a blob or a member of the error set 𝔼 = {∞, ☇, BADEXPORTS, OVERSIZE, BAD, BIG} (eq. 11.7). Which meaning is correct?",
 "options": [
  "∞ out-of-gas; ☇ panic; BADEXPORTS the number of exports was misreported; OVERSIZE the refine output would exceed the size limit; BAD service code unavailable at the lookup-anchor; BIG code exceeds W_C = 4,000,000",
  "∞ an infinite loop was detected by the guarantor; ☇ a host-call fault; BADEXPORTS the number of exports was misreported; OVERSIZE the refine output would exceed the size limit; BAD service code unavailable at the lookup-anchor; BIG the bundle exceeds W_B",
  "∞ out-of-gas; ☇ a PVM page fault; BADEXPORTS the number of imported segments was misreported; OVERSIZE the bundle would exceed W_B; BAD the authorizer rejected the package; BIG more than I = 16 work-items",
  "∞ out-of-gas; ☇ panic; BADEXPORTS the number of exports was misreported; OVERSIZE the refine output would exceed the size limit; BAD the code was available but exceeds W_C = 4,000,000; BIG the code was unavailable at the lookup-anchor"
 ],
 "answer": 0,
 "optNotes": [
  "六個值與 §11.1.4 逐字對應，關鍵在 BAD 是 code 不可得、BIG 是 code 存在但超過 W_C。",
  "PVM 不做迴圈偵測（停機問題），∞ 就是 gas 耗盡；W_B 是 §14 對 bundle 的檢查，不是 digest 結果。",
  "page fault 只是 panic 的成因之一；BADEXPORTS 針對 export 數，OVERSIZE 針對 refine 的輸出。",
  "BAD 與 BIG 對調了：GP 是 the third… code was not available、the fourth… beyond W_C。",
 ],
 "explanation": "eq. 11.7（錯誤集合是 𝔼，注意 𝕁 在 0.8.0 是 segment 的集合）與 §11.1.4：「The first two are special values concerning execution of the virtual machine, ∞ denoting an out-of-gas error and ☇ denoting an unexpected program termination（panic）. Of the remaining four, the first indicates that the number of exports made was invalidly reported, the second that the size of the digest（refinement output）would cross the acceptable limit, the third（BAD）indicates that the service's code was not available for lookup in state at the posterior state of the lookup-anchor block. The fourth（BIG）indicates that the code was available but was beyond the maximum size allowed W_C」。另外 authorizer 不接受的 package 根本進不了鏈（eq. 11.32 要求 w_a ∈ α[w_c]），不會以 error 的形式留在 digest 裡。你們 encode.go 的 WorkExecResult：0 ok、1 oog、2 panic、3 bad-exports、4 output-oversize、5 bad-code、6 code-oversize。",
 "trap": "錯誤結果仍會被 accumulate（operand 的 r 是 error），只是沒有 output blob。"
},
{
 "id": "ch11-report-size-limit",
 "ch": "11", "section": "11.1.4 Work Digest", "gpRef": "eq. 11.8",
 "difficulty": 1, "kind": "concept", "tags": ["reports", "limits"],
 "stem": "What is the on-chain limit on the variable-size content of a single work-report?",
 "options": [
  "|authorizer trace t| + Σ over digests of |result blob| (errors count as 0) ≤ W_R = 48·2^10 = 49,152 octets",
  "|authorizer trace t| + Σ over digests of |result blob| (errors count as their encoded length) ≤ W_B = 13,791,360 octets",
  "Σ over digests of |result blob| alone, the authorizer trace being unbounded, ≤ W_R = 48·2^10 = 49,152 octets",
  "|authorizer trace t| ≤ 32 octets and each digest's result blob ≤ W_G = 4,104 octets, giving at most I = 16 blobs"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 11.8 的 L 對 r ∈ 𝔼 回 0，失敗的 digest 不佔 report 空間，out-of-gas 反而「便宜」。",
  "error 不按編碼長度計；而 W_B 套的是 §14 的 work-package bundle，不是 report 的 W_R。",
  "|w_t| 是加總的第一項，否則 is-authorized 的 trace 可以無限撐大區塊。",
  "eq. 11.8 是單一總量上限、沒有逐項上限；W_G = 4,104 是 segment 大小，與 report 無關。",
 ],
 "explanation": "eq. 11.8：∀w ∈ R：|w_o| + Σ_{i} L(w_d[i]_r) ≤ W_R，L(r) = |r| 若 r ∈ B（成功輸出），否則 0；W_R = 48·2^10 = 49,152。GP 給的理由：「In order to ensure fair use of a block's extrinsic space」。對照 W_B（13,791,360）是 work-package **bundle**（extrinsics + imports 等）的上限（§14）——兩者管的是不同層級的東西。你們 guarantor 端的 BIG/OVERSIZE 判斷是累積前面 item 的輸出一起算。",
 "trap": "48 KiB 是 report 級總量，且 auth trace 也算在內。"
},
{
 "id": "ch11-assurance-rules",
 "ch": "11", "section": "11.2 Package Availability Assurances", "gpRef": "eq. 11.11–11.16",
 "difficulty": 2, "kind": "concept", "tags": ["assurances"],
 "stem": "Which set of rules applies to the assurances extrinsic E_A?",
 "options": [
  "Each assurance = (anchor a, bitfield f ∈ bits[C], validator index v, Ed25519 sig); a must equal H_P; assurances strictly ordered by v (so at most one per validator); the signature by κ[v]_e is over X_A ⌢ H(E(H_P, f)); a bit may be set only if ρ†[c] ≠ ∅",
  "Each assurance = (anchor a, bitfield f ∈ bits[C], validator index v, Ed25519 sig); a must equal the hash of the block being built; assurances strictly ordered by v; the signature by κ′[v]_e is over X_A ⌢ H(E(H_P, f)); a bit may be set only if ρ†[c] ≠ ∅",
  "Each assurance = (anchor a, bitfield f ∈ bits[|κ|], validator index v, Bandersnatch sig); a must equal H_P; a validator may send several assurances so long as they stay sorted by v; the signature is over X_A ⌢ H(E(H_P, f)); a bit may be set only if ρ†[c] ≠ ∅",
  "Each assurance = (anchor a, bitfield f ∈ bits[C], validator index v, Ed25519 sig); a must equal H_P; assurances strictly ordered by core index; the signature by κ[v]_e is over X_A ⌢ the erasure root of each assured report; a bit may be set only if ρ‡[c] ≠ ∅"
 ],
 "answer": 0,
 "optNotes": [
  "五個條件全中，關鍵是 anchor 綁 parent hash H_P、簽名用的是 prior 的 κ[v]_e。",
  "簽名當下本塊 hash 還不存在，eq. 11.12 因此綁 H_P；eq. 11.14 用的也是 prior 的 κ。",
  "f ∈ bits[C] 是每個 core 一 bit、簽章是 Ed25519，而 eq. 11.13 的嚴格遞增讓每人至多一筆。",
  "排序鍵是 assurer 的 index v；一筆 assurance 只簽整個 bitfield 一次；前提是 ρ† 而非 ρ‡。",
 ],
 "explanation": "eq. 11.11：E_A ∈ [(a ∈ H, f ∈ B_C, v ∈ N_{|κ|}, s ∈ E)]；11.12：a = H_P（anchor 是 parent hash，這也讓 assurance 無法被搬到另一條分叉）；11.13：依 v 嚴格遞增；11.14：s ∈ Ed25519 由 κ[v]_e 對 X_A ⌢ H(E(H_P, f)) 簽署，X_A = $jam_available；11.16：f[c] ⇒ ρ†[c] ≠ ∅。注意 signer 用的是 **prior** κ（0.6.4 起「Assurances are checked with the prior validator set」），而 11.16 的前提是 ρ†（disputes 之後、assurances 之前）——ρ‡ 要處理完這些 assurance 才算得出來，拿它當前提會變成循環定義。bit = 1 的意義是「我保證我正在為它的 availability 出力」（軟性宣告，§11.2.1 footnote）。你們的錯誤碼：BadAttestationParent、NotSortedOrUniqueAssurers、CoreNotEngaged。",
 "trap": "bitfield 長度 = C（cores），full 是 43 bytes（341 bits），tiny 1 byte；LSB-first。"
},
{
 "id": "ch11-availability-threshold",
 "ch": "11", "section": "11.2.2 Available Reports", "gpRef": "eq. 11.17–11.18",
 "difficulty": 2, "kind": "delta", "tags": ["assurances", "delta-0.8.0", "tiny"],
 "stem": "When does a report become available (R), and when is a pending assignment cleared from ρ‡ in GP 0.8.0?",
 "options": [
  "Available iff the number of assurances with bit c set is > 2/3·|κ| (tiny: ≥ 5 of 6; full: ≥ 683); ρ‡[c] = ∅ if the report became available, or H_T ≥ t + U (U = 5 slots), or |κ| ≠ |κ′| (the validator-set size changed)",
  "Available iff the number of assurances with bit c set is ≥ 2/3·|κ| (tiny: ≥ 4 of 6; full: ≥ 682); ρ‡[c] = ∅ if the report became available, or H_T ≥ t + U (U = 5 slots), or |κ| ≠ |κ′| (the validator-set size changed)",
  "Available iff the number of assurances with bit c set is > 2/3·|κ| (tiny: ≥ 5 of 6; full: ≥ 683); ρ‡[c] = ∅ if the report became available, or H_T ≥ t + U with U = 10 slots, or the epoch index has changed",
  "Available iff the number of assurances with bit c set is > 1/2·|κ| (tiny: ≥ 4 of 6; full: ≥ 512); ρ‡[c] = ∅ only once the report has been accumulated, so an assignment never times out and never reacts to a change in |κ|"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 11.17 是嚴格大於 2/3，而 eq. 11.18 的第三個清除條件正是 0.8.0 新增的 |κ| ≠ |κ′|。",
  "剛好 2/3 不夠：tiny 要 5 票、full 要 683 票，這裡各少了一票。",
  "U = 5 不是 10；清除條件是 |κ| ≠ |κ′| 而非 epoch 邊界，人數沒變的換屆不清任何 pending。",
  "門檻是 2/3 super-majority；等 accumulate 才清會讓湊不到票的 report 把 core 永久卡死。",
 ],
 "explanation": "eq. 11.17：R ≡ [ρ†[c]_g_w | Σ_a f[c] > 2/3·|κ|]——嚴格大於 2/3（tiny 6 → >4 → ≥5；full 1023 → >682 → ≥683，即 ⌊2V/3⌋+1；ELVES 的安全假設要求 2/3+1 誠實且 live）。eq. 11.18：ρ‡[c] = ∅ 當 p = ∅ ∨ report ∈ R ∨ H_T ≥ p_t + U ∨ |κ| ≠ |κ′|，否則 p。U = C_assurancetimeoutperiod = 5。「|κ| ≠ |κ′|」是 0.8.0 新增：validator 數改變時所有 pending 都視為提早 timeout（因為 erasure shard 數與 assurer 集合都對不上了）。你們 0.7.2 的 FilterAvailableReports 只有 timeout，沒有 size-change 條件。",
 "trap": "timeout 比較的是 H_T（本塊 slot）與 assignment 的 t（guarantee 進鏈的 slot）。"
},
{
 "id": "ch11-guarantor-assignment",
 "ch": "11", "section": "11.3 Guarantor Assignments", "gpRef": "eq. 11.19–11.23",
 "difficulty": 3, "kind": "concept", "tags": ["guarantees", "shuffle"],
 "stem": "How are validators assigned to cores for guaranteeing in GP 0.8.0?",
 "options": [
  "P(v, e, t) = R(F([⌊i/3⌋ | i ∈ N_v], e), ⌊(t mod E)/R⌋): the sequence [0,0,0,1,1,1,…] is Fisher-Yates shuffled with entropy e = η′_2, then rotated by the rotation index (R = 10 slots); M = (P(|κ′|, η′_2, τ′), Φ(κ′)) — only cores < |κ′|/3 are active",
  "P(v, e, t) = R(F([⌊C·i/v⌋ | i ∈ N_v], e), ⌊(t mod E)/R⌋): the base sequence spreads the v validators over all C cores before the Fisher-Yates shuffle with entropy e = η′_2; M = (P(|κ′|, η′_2, τ′), Φ(κ′)) — all C = 341 cores are active",
  "P(v, e, t) = R(F([⌊i/3⌋ | i ∈ N_v], e), ⌊(t mod E)/R⌋), the shuffle taking entropy e = η′_1 and the rotation period being R = 600, i.e. one rotation per epoch; M = (P(|κ′|, η′_1, τ′), Φ(κ′)) — only cores < |κ′|/3 are active",
  "P(v, e, t) = R(F([⌊i/3⌋ | i ∈ N_v], e), t mod R): the shuffled sequence is rotated once per slot, so each validator's core advances by one every block, with entropy e = η′_2; M = (P(|κ′|, η′_2, τ′), Φ(κ′)) — only cores < |κ′|/3 are active"
 ],
 "answer": 0,
 "optNotes": [
  "base sequence ⌊i/3⌋、entropy η′_2、rotation index ⌊(t mod E)/R⌋ 三處都合 eq. 11.21。",
  "⌊C·i/v⌋ 是 0.7.2 的寫法：|κ′| < 3C 時它會把 validator 撒到不存在的 active core 上。",
  "§11.3 明說用 η′_2 而非 η′_1；R = 10 而非 600，一個 epoch 有 E/R = 60 次 rotation。",
  "index 是 ⌊(t mod E)/R⌋：同一 rotation 的 10 個 slot 內分配不變，eq. 11.28 才容許回溯。",
 ],
 "explanation": "§11.3：C = 341 個 core 固定，但只有前 |κ′|/3 個是 active（每個 core 3 個 guarantor）。eq. 11.20：R(c, n) = [(x + n) mod (|c|/3) | x ∈ c]（rotation）；11.21：P(v, e, t) = R(F([⌊i/3⌋ | i ∈ N_v], e), ⌊(t mod E)/R⌋)，F 是附錄 F 的 Fisher-Yates shuffle；11.22：M ≡ (P(|κ′|, η′_2, τ′), Φ(κ′))——key 經 Φ 過濾，offender 會被拒（你們 BannedValidator = code 23）。用 η′_2 是為了避免 fork magnification：§11.3「to avoid the possibility of fork-magnification where uncertainty about chain state at the end of an epoch could give rise to two established forks」。11.23：M* 是上一個 rotation 的分配：若 τ′ − R 仍在同一 epoch 用 (κ′, η′_2)，否則用 (λ′, η′_3)。版本差異：0.7.2 的 base assignment 是 ⌊C·i/V⌋，0.8.0 改成 ⌊i/3⌋（因為 active cores = V/3）。",
 "trap": "rotation period R = 10 slots；每個 epoch 600/10 = 60 次 rotation。"
},
{
 "id": "ch11-guarantee-validity",
 "ch": "11", "section": "11.4 Work Report Guarantees", "gpRef": "eq. 11.24–11.29",
 "difficulty": 3, "kind": "concept", "tags": ["guarantees"],
 "stem": "Which statement about a guarantee g = (w, t, a) in E_G is correct?",
 "options": [
  "a has 2 or 3 (validator index, Ed25519 sig) pairs ordered by index; every signer must be assigned to core w_c under M when t is in the current rotation and under M* otherwise; R·(⌊τ′/R⌋ − 1) ≤ t ≤ τ′; each signature is over X_G ⌢ H(E(w)); w_c < |κ′|/3",
  "a has exactly 3 (validator index, Ed25519 sig) pairs ordered by index; every signer must be assigned to core w_c under M when t is in the current rotation and under M* otherwise; t must equal τ′; each signature is over the encoded report E(w) itself; w_c < |κ′|/3",
  "a has 2 or 3 (validator index, Ed25519 sig) pairs ordered by index; signers may be any members of κ′ ∪ λ′ whatever core they are assigned to; R·(⌊τ′/R⌋ − 1) ≤ t ≤ τ′; each signature is over X_G ⌢ H(E(w)); any core index below C = 341 may be used",
  "a has 2 or 3 (validator index, Ed25519 sig) pairs ordered by index; every signer must be assigned to core w_c under M* when t is in the current rotation and under M otherwise; R·(⌊τ′/R⌋ − 1) ≤ t ≤ τ′; each signature is over X_G ⌢ H(E(w)); w_c < C/3"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 11.28 的五個條件全中：c[v] = w_c、w_c < |κ′|/3、簽 X_G ⌢ H(E(w))、t 可回溯一個 rotation。",
  "credential 型別是 [(index, sig)]_{2:3}，2 個就成立；t 可早於 τ′；訊息要先 hash 再冠 context。",
  "eq. 11.28 要求 c[v] = w_c，簽署者必須正好被指派到這個 core；active core 上限是 |κ′|/3。",
  "M 與 M* 對調了：t 落在當前 rotation 用 M；且 C/3 ≈ 113 不是任何 config 的 active core 數。",
 ],
 "explanation": "eq. 11.24：G ≡ (w ∈ R, t ∈ N_T, a ∈ [(N, E)]_{2:3})；11.25–11.26：E_G ∈ [G]_{:C}，依 core 排序且唯一；11.27：credential 依 validator index 排序；11.28：∀(v, s) ∈ a：v < |k| ∧ c[v] = w_c < |κ′|/3、s ∈ Ed25519_{k[v]_e}(X_G ⌢ H(w))、R(⌊τ′/R⌋ − 1) ≤ t ≤ τ′；(c, k) = M 當 ⌊τ′/R⌋ = ⌊t/R⌋，否則 M*。GP：「Use of an inactive core is not permitted even if a timeslot in the previous rotation is used」。訊息先 Blake2b 再冠上 context string X_G，是為了避免同一段位元組在別的協定情境下被重放。簽署者的 Ed25519 key 會進入 reporters 集合 R（給 π 統計）。",
 "trap": "t 是 guarantee 的 slot，可比 τ′ 早最多一個 rotation；ρ′ 的 timestamp 卻是 τ′（eq. 11.46）。"
},
{
 "id": "ch11-report-checks-state",
 "ch": "11", "section": "11.4 Work Report Guarantees", "gpRef": "eq. 11.31–11.33",
 "difficulty": 2, "kind": "concept", "tags": ["guarantees", "gas"],
 "stem": "Which on-chain checks apply to each incoming report w before it is placed in ρ′?",
 "options": [
  "ρ‡[w_c] = ∅ (core free after disputes and assurances); w_a ∈ α[w_c] (authorizer in the PRIOR pool); Σ digest accumulate-gas ≤ G_A = 10,000,000 and each digest's gas ≥ δ[d_s]_g; the erasure-chunk count equals |κ′|",
  "ρ[w_c] = ∅ (core free in the prior state); w_a ∈ α′[w_c] (authorizer in the POSTERIOR pool); Σ digest accumulate-gas ≤ G_T = 3,500,000,000 and each digest's gas ≥ δ[d_s]_g; the erasure-chunk count equals |κ′|",
  "ρ‡[w_c] = ∅ and the core must additionally have stayed free for U = 5 slots; w_a ∈ α[w_c]; Σ digest accumulate-gas ≤ G_A = 10,000,000 with no per-service floor; the erasure-chunk count equals |κ′|",
  "ρ‡[w_c] = ∅ (core free after disputes and assurances); w_a ∈ α[w_c]; Σ digest refine-gas used ≤ G_R = 5,000,000,000 and each digest's gas ≥ δ[d_s]_g; the erasure-chunk count equals |κ| in the prior state"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 11.32 檢查的是 ρ‡，所以同一塊裡剛騰出的 core 可以馬上再被用。",
  "用 prior ρ 會擋掉本塊剛騰出的 core；α′ 要 accumulation 之後才存在；G_T 是整塊的總預算。",
  "eq. 11.32 只要求 ρ‡[r_c] = ∅、沒有「空滿 U 個 slot」；eq. 11.33 也明確有 d_g ≥ δ[d_s]_g。",
  "eq. 11.33 管的是 accumulate gas 而不是 refine 的 G_R；eq. 11.31 比的也是 posterior 的 |κ′|。",
 ],
 "explanation": "eq. 11.31：∀r ∈ I：(r_s)_v = |κ′|（erasure chunk 數 = posterior 的 validator 數，因為 chunk 是發給下一組 assurer 的）；11.32：∀r ∈ I：ρ‡[r_c] = ∅ ∧ r_a ∈ α[r_c]——core 空不空要等 disputes 清完（ρ†）、assurances 與 timeout 收完（ρ‡）才知道，而 authorizer 只能比 **prior** 的 α；11.33：Σ_{d ∈ r_d} d_g ≤ G_A（10M，每個 report 的 accumulate gas 上限）∧ ∀d：d_g ≥ δ[d_s]_g。對照另外兩個容易混的預算：G_T = 3.5·10^9 是**整塊** accumulation 的總預算，G_R = 5·10^9 是單一 work-package refine 的預算（§14，鏈下判定）。",
 "trap": "α（prior）用於檢查，α′ 在 accumulate 之後才算。"
},
{
 "id": "ch11-contextual-validity",
 "ch": "11", "section": "11.4.1 Contextual Validity of Reports", "gpRef": "eq. 11.35–11.45",
 "difficulty": 3, "kind": "concept", "tags": ["guarantees", "context"],
 "stem": "Which of the following is NOT one of the contextual validity requirements for reports in E_G?",
 "options": [
  "No two reports in the extrinsic share a work-package hash, and no package hash may appear in β's reported sets, in ξ (accumulated), in the ready queue ω or in a pending assignment of ρ",
  "The anchor's (a, n, s, b) must match an entry of β†; the lookup-anchor time must be ≥ H_T − L, and the lookup-anchor header must be found in the ancestor set A",
  "Every prerequisite and every segment-root-lookup key must appear in this extrinsic or in β's reported sets, and the looked-up segment roots must match those records",
  "Every digest's service must have been accumulated at least once within the last epoch E, and a service left idle for longer must be re-registered before it may be reported again"
 ],
 "answer": 3,
 "optNotes": [
  "eq. 11.35 加 11.39–11.41 就是這一項：不重複，且不在 β、ξ、ω、ρ 任何一段 pipeline 裡。",
  "eq. 11.36（anchor 四元組對 β†）、11.37（l_t ≥ H_T − L）、11.38（header 在 A 裡）確有此三條。",
  "eq. 11.42 與 11.43–11.44 正是這一項：prereq/srlookup 的 key 與 segment root 都要對得上。",
  "GP 沒有「service 閒置過久失效」這條規則，唯一相關的是 eq. 11.45 的 d_c = δ[d_s]_c。",
 ],
 "explanation": "這題考的是 §11.4.1 的完整清單：eq. 11.35（同一塊不得有兩份同 package 的 report）、11.36–11.38（anchor 四元組對 β†、lookup anchor 的時間下限與祖先集合 A）、11.39–11.41（package hash 不得出現在 β 的 reported 集合、ξ、ready queue ω 或任何 pending 的 ρ）、11.42–11.44（prerequisites 與 srlookup 的 key 與 segment root）、11.45（d_c = δ[d_s]_c）。service 只會因 eject 而消失（§9），report 是否合法完全不看該 service 上次 accumulate 的時間。§11.4.1 附註：這些檢查刻意允許表面上的 dependency loop，因為 accumulation 端的 Q 函數永遠不會 accumulate 它們。",
 "trap": "面試官可能要求你列舉「所有」contextual checks——建議背下 anchor / lookup-anchor / no-dup / prereq / srlookup / code-hash 六類。"
},
{
 "id": "ch11-rho-prime",
 "ch": "11", "section": "11.5 Transitioning for Reports", "gpRef": "eq. 11.46",
 "difficulty": 1, "kind": "concept", "tags": ["guarantees", "state"],
 "stem": "After processing E_G, what does ρ′[c] hold for a core that received a new guarantee g?",
 "options": [
  "(g, τ′) — the whole guarantee paired with the current block's timeslot τ′ as its assignment time",
  "(g, g_t) — the whole guarantee paired with the guarantee's own slot t, which may lie a rotation earlier",
  "(w, τ′) — only the work-report, the guarantor credential being discarded once it has been verified",
  "(H(E(w)), τ′) — the report hash paired with the current block's timeslot, the guarantee moving into β"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 11.46 存的時間戳是 τ′（本塊 slot），timeout 因此從進鏈那一刻起算。",
  "g_t 可比 τ′ 早一整個 rotation（R = 10），一進鏈就超過 U = 5，下一塊立刻被清掉。",
  "0.8.0 (#494) 的 ρ 型別就是 (g, t)：簽章要留著抓 bundle、以及在 dispute 時構造 culprits。",
  "β 每筆從不存 guarantee（eq. 7.2）；而 eq. 11.17 之後要交出整份 report，只有 hash 不夠。",
 ],
 "explanation": "eq. 11.46：ρ′[c] ≡ (g, t: τ′) 當 ∃g ∈ E_G 使得該 guarantee 的 report 指向 core c，否則沿用 ρ‡[c]。也就是**整份 guarantee**（work-report 加上 2–3 個 guarantor 簽章）配上一個時間戳一起掛在該 core 上。**時間戳是這題的坑**：存的是 **τ′（本塊的時槽）**，不是 guarantee 自己帶的 slot g_t。兩者可以差到一整個 rotation（R = 10 個時槽）——report 可以在被擔保之後隔幾塊才進鏈。這個差別直接決定 eq. 11.18 的逾時從哪一刻起算：報告若在 U = 5 個時槽內沒有湊到 availability 的超級多數，就會被清掉；用 g_t 當起點會讓可用時間平白縮水。你們 code-map 3.7.6 特別標了這一點。**另一個常被忽略的細節**：對 c ≥ |κ′| / 3 的 core，ρ′[c] 恆為 ∅。因為每個 core 需要 3 名 guarantor，active validator 只有 |κ′| 個，能同時運作的 core 數自然被 |κ′| / 3 卡住；這保證待審計的 report 數不會超過現有驗證者能負擔的量（tiny 設定下 |κ| = 6 就只有 2 個 core 在動）。相關名詞：ρ 是 availability assignments、ρ† 是清掉 disputes 判定為壞的那些之後的中間值、ρ‡ 是再處理完 assurances 之後的中間值。",
 "trap": ""
},
{
 "id": "ch11-code-availability",
 "ch": "11", "section": "11.2.2 Available Reports", "gpRef": "eq. 11.17 — internal/extrinsic/assurance_controller.go",
 "difficulty": 2, "kind": "code", "tags": ["assurances", "code", "delta-0.8.0"],
 "stem": "The team's availability check uses `totalAvailable[i] >= types.ValidatorsSuperMajority`. Which statement is accurate?",
 "code": {"lang": "go", "caption": "internal/extrinsic/assurance_controller.go (UpdateNewlyAvailableWorkReports)", "src": """for i := 0; i < types.CoresCount; i++ {
    // If the votes for this core are greater than the available number, add the work report
    if totalAvailable[i] >= types.ValidatorsSuperMajority {
        if rhoDagger[i] == nil {
            continue
        }
        availableWorkReports = append(availableWorkReports, rhoDagger[i].Report)
    }
}"""},
 "options": [
  "It matches the GP's strict '> 2/3·|κ|' exactly when ValidatorsSuperMajority = ⌊2|κ|/3⌋ + 1 is derived from the live size of κ — 5 of 6 in tiny, 683 of 1023 in full — rather than from a compile-time constant",
  "It is wrong: eq. 11.17 asks only for ≥ 2/3·|κ|, so 4 of 6 assurances suffice in tiny and 682 of 1023 in full; the comparison should be against ⌈2|κ|/3⌉ instead of a super-majority constant",
  "It is wrong: eq. 11.17 counts, per core, the assurers that set that core's bit, whereas the loop must first count the distinct validators appearing anywhere in E_A and compare that with the super-majority",
  "It is wrong: a core whose rhoDagger entry is nil must still contribute its report, because eq. 11.18 only empties ρ‡ after the availability count for the block has already been taken"
 ],
 "answer": 0,
 "optNotes": [
  "> 2V/3 對整數等價於 ≥ ⌊2V/3⌋+1，所以只要該常數隨 |κ| 變動，這個比較就是對的。",
  "eq. 11.17 寫的是嚴格大於，⌈2·6/3⌉ = 4 會少算一票，平手局面不該讓 report 變成可用。",
  "eq. 11.17 的 Σ 是逐 core 對 a_f[c] 求和；混著數會把只 assure 了別的 core 的人算進來。",
  "那個 core 根本沒有 report 可送；ρ‡ 是 eq. 11.18 的輸出，不是計票當下的狀態。",
 ],
 "explanation": "eq. 11.17：Σ_a a_f[c] > (2/3)|κ|。對整數而言 > 2V/3 ⇔ ≥ ⌊2V/3⌋ + 1：V = 6 → > 4 → ≥ 5；V = 1023 → > 682 → ≥ 683。所以 `>= ValidatorsSuperMajority` 這個寫法本身是對的，真正的風險在該常數必須等於 ⌊2|κ|/3⌋+1 且隨 |κ| 變動（0.8.0 起 validator 數可變），不能是編譯期寫死的數字。另外 `rhoDagger[i] == nil` 的情況其實已被 eq. 11.16（bit 只能在有 pending report 的 core 上設）擋掉，這裡是防禦性檢查。",
 "trap": "tiny 5/6、full 683/1023；同一個 super-majority 常數也用在 verdict 的 good 門檻。"
},
]
