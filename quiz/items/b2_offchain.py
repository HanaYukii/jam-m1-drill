# -*- coding: utf-8 -*-
# Off-chain protocol (ch. 15–19) + interview/conformance context — all filed under ARCH
ITEMS = [
{
 "id": "arch-audit-initial-tranche",
 "ch": "ARCH", "section": "17.3 Selection of Reports", "gpRef": "eq. 17.2–17.4",
 "difficulty": 3, "kind": "concept", "tags": ["auditing", "elves"],
 "stem": "How does a validator pick the work-reports it must audit in the INITIAL tranche (a_0)?",
 "options": [
  "It makes a Bandersnatch VRF signature s_0 over context X_U ⌢ Y(H_V) with an empty message, then Fisher-Yates shuffles the per-core sequence q using Y(s_0) and keeps the non-empty entries among the first ten",
  "It audits every report that became available in the block: q holds one entry per active core, so the initial tranche is simply all of its non-empty entries and no verifiable randomness is involved",
  "It audits the reports on the cores it guaranteed in the previous rotation, reusing the guarantor assignment G* of that rotation rather than drawing any fresh randomness for the tranche",
  "It signs the block hash with its Ed25519 key and audits those cores whose index matches the low bits of that signature, taking as many cores as the audit bias factor F = 2 permits"
 ],
 "answer": 0,
 "optNotes": [
   "eq. 17.3：a_0 = {w | w ∈ F(q, Y(s_0))[..10], w ≠ ∅}，先洗牌取前十、再濾掉 ∅。",
   "全部都審等於退回 everybody-does-everything，也用不上任何可驗證亂數。",
   "guarantor 正是被審的一方，且 G* 公開可算，攻擊者能事先知道誰審什麼。",
   "用的是 Bandersnatch VRF 而非 Ed25519 簽名；F = 2 只用在 n > 0 的後續 tranche 判準。",
 ],
 "explanation": "eq. 17.2：s_0 ∈ F_{κ[v]_b}^{X_U ⌢ Y(H_V)}([])，X_U = $jam_audit——VRF 的 context 綁定本區塊的 entropy VRF 輸出 Y(H_V)，所以選擇是可驗證亂數且逐塊不同。eq. 17.3：a_0 = {w | w ∈ F(q, Y(s_0))[..10], w ≠ ∅}，q 是長度 |κ|/3（active cores）的序列，把「本塊剛 available 的 report」對應到 core（沒有就是 ∅）；先洗牌取前十項、再濾掉 ∅，所以初始 tranche 最多 10 個 core。抽樣而非全審正是 ELVES 的前提：§4.9.1 想要的約 300 倍算力來自 in-core 的少數重算，後續 tranche 的擴張由 no-show 驅動。宣告（announcement）必須先發布並且「should be taken as a contract to complete the audit regardless of any future information」。",
 "trap": "10 個 core 是 shuffle 後取前 10；q 的長度是 active cores = |κ|/3，不是 C = 341。"
},
{
 "id": "arch-audit-outcomes",
 "ch": "ARCH", "section": "17.1 Overview", "gpRef": "§17.1",
 "difficulty": 2, "kind": "concept", "tags": ["auditing", "disputes"],
 "stem": "GP §17.1 describes what happens when a negative judgment appears. Which pair of thresholds and consequences is correct?",
 "options": [
  "If more than 2/3 of validators still issue POSITIVE judgments, those issuing negative judgments may be punished for time-wasting; if more than 1/3 issue NEGATIVE judgments, the block containing the report is ban-listed and it and all its descendants are disregarded",
  "If more than 1/2 of validators issue NEGATIVE judgments, the report is dropped from its availability assignment; if fewer do, nothing happens at all — no validator is ever punished for a false negative and the block containing the report stays buildable",
  "A single NEGATIVE judgment suffices: it invalidates the block that carried the report and slashes all three guarantors of that core; no further validator need judge, no verdict reaches the disputes extrinsic, and the 2/3 positive threshold plays no part",
  "Negative judgments carry no consequence of their own; only the disputes extrinsic matters, a verdict there needs the unanimous signature of the whole active validator set, and the punish-set ψ_O fills only from culprits and never from faults"
 ],
 "answer": 0,
 "optNotes": [
   "兩個門檻都對上 §17.1：2/3 正面罰浪費時間者、1/3 負面 ban-list 該塊與其後代。",
   "門檻是 1/3 不是 1/2；被 ban-list 的區塊「may not be built on」，反對者也確實會被罰。",
   "verdict 需 ⌊2/3·|k|⌋ + 1 票，單獨一票既構不成 verdict，也不會登錄任何 culprit。",
   "eq. 10.12 的票數從來不是 unanimity；ψ_O 除 culprits 外也收 faults 這種 offence。",
 ],
 "explanation": "§17.1：「if greater than 2/3 of the validators still issue positive judgments, then validators issuing negative judgments may receive a punishment for time-wasting. If greater than 1/3 of the validators issue negative judgments, then the block which includes the work-report is ban-listed. It and all its descendants are disregarded and may not be built on.」兩個門檻方向相反：2/3 正面是用來懲罰亂投反對票的人（讓惡意負面判決有代價），1/3 負面則丟掉整條分支。最後由 block author 把足夠的票組成 verdict 放進 disputes extrinsic（§10）——「once there are enough votes, a verdict can be constructed by a block author and placed in a disputes extrinsic」；§10 eq. 10.12 的正面票數只接受 ⌊2/3·|k|⌋ + 1（good）、0（bad）、⌊1/3·|k|⌋（wonky）三個值，而 punish-set ψ_O 同時收 culprits（保證了無效 report 的 guarantor）與 faults（判決與 verdict 相牴觸的簽署者）。另外：一個 report 的所有宣告都被正面判決匹配時即為 audited；一個區塊的所有新 available report 都 audited 時該區塊為 audited——這是 finalize 的前提之一（§19）。",
 "trap": "「1/3 負面 → 整條鏈分支被丟棄」是 best-chain 的 disregard 規則；2/3 正面 → 反對者被罰。"
},
{
 "id": "arch-audit-reconstruction",
 "ch": "ARCH", "section": "17.2 Data Fetching", "gpRef": "§17.2–17.3 & appendix H",
 "difficulty": 2, "kind": "concept", "tags": ["auditing", "erasure-coding"],
 "stem": "How does an auditor obtain the data it needs to re-run a work-report?",
 "options": [
  "It reconstructs the bundle from erasure-coded chunks fetched from about one-third of the validators, verified against the erasure-root; exported segments are recomputed by re-running refine",
  "It downloads the whole bundle from the block author, who is required by the GP to retain it for 28 days; the exported segments arrive with it, so the refine logic never has to be re-run",
  "It reads both the imported and the exported segments straight from on-chain state, where they sit under the reporting service's preimages until the report is accumulated and then expire",
  "It asks the core's other two guarantors to re-sign the report and takes a matching pair of Ed25519 signatures as proof of correctness; no bundle is fetched and refine is never re-run"
 ],
 "answer": 0,
 "optNotes": [
   "chunk 取自約三分之一 validator、以 erasure-root 驗證，exported segments 則靠重跑 refine 產生。",
   "持有 chunk 的是 assurer 不是出塊者；28 天是 exported-segment 的 D³L 期限，不是 audit DA store。",
   "segment 從不進 state，鏈上只有 erasure-root、segment-root 等 hash；preimage 是 §9.2 另一套設施。",
   "guarantor 的簽名正是審計要檢驗的對象，再收一次同一批人的背書是循環論證。",
 ],
 "explanation": "§17.3：「This may be done through requesting erasure-coded chunks from one-third of the validators, verified through the erasure coding's Merkle root, and reconstructing the bundles as per the recovery function」（附錄 H：任意 d(v) ≈ v/3 + 1 個 chunk 即可還原）。§17.2：bundle 內含 work-package、extrinsic data、imported segments 與其 justification；「Exported segments need not be reconstructed in the same way, but rather should be determined… through the execution of the Refine logic」——重跑 refine 正是審計的核心動作，M(w, p) 要求 w = Ξ(p, w_c, w_l, …) 逐欄位相符，光有資料而不重算根本沒有審到。§17.3 確實允許直接向 guarantor 要完整 bundle 當捷徑，但「If this data cannot be decoded or verified however, we must fall back to reconstruction from erasure-coded chunks」，而且拿到之後一樣要重跑 refine，把 work-package specification 的每個欄位重算並比對——「essentially retracing the guarantors steps」。",
 "trap": "審計 = 重跑 computereport 並比對整個 report；解不出 bundle 本身就代表 report 無效。"
},
]
