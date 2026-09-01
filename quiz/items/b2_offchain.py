# -*- coding: utf-8 -*-
# Off-chain protocol (ch. 15–19) + interview/conformance context — all filed under ARCH
ITEMS = [
{
 "id": "arch-audit-initial-tranche",
 "ch": "ARCH", "section": "17.3 Selection of Reports", "gpRef": "eq. 17.2–17.4",
 "difficulty": 3, "kind": "concept", "tags": ["auditing", "elves"],
  "stemZh": "validator 如何挑出自己在初始 tranche（a_0）必須稽核的 work-report？",
  "optionsZh": [
   "它以 context X_U ⌢ Y(H_V) 對空訊息做一個 Bandersnatch VRF 簽章 s_0，再用 Y(s_0) 對每個 core 的序列 q 做 Fisher-Yates 洗牌，取前十個當中非空的那些",
   "它稽核本區塊中所有變成 available 的 report：q 每個作用中的 core 一筆，所以初始 tranche 就是它全部的非空項目，過程不涉及任何可驗證隨機性",
   "它稽核自己在上一個 rotation 擔保過的那些 core 上的 report，沿用該 rotation 的 guarantor 指派 G*，不為這個 tranche 另外抽取新的隨機性",
   "它用自己的 Ed25519 金鑰簽署區塊雜湊，稽核那些索引與該簽章低位元相符的 core，取用的 core 數以稽核放大係數 F = 2 所允許的為上限"
  ],
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
  "stemZh": "GP §17.1 描述了出現負面判定時會發生什麼事。哪一組門檻與後果是正確的？",
  "optionsZh": [
   "若仍有超過 2/3 的 validator 發出正面判定，發出負面判定的人可能因浪費時間而受罰；若有超過 1/3 發出負面判定，含有該 report 的區塊會被列入禁用名單，它與其所有後代都會被忽略",
   "若有超過 1/2 的 validator 發出負面判定，該 report 會從它的 availability assignment 中被移除；若不足此數則什麼也不會發生——沒有任何 validator 會因為誤報而受罰，含有該 report 的區塊仍可繼續被建構",
   "單一個負面判定就足夠：它使承載該 report 的區塊無效，並沒收該 core 三位 guarantor 的質押；不需要其他 validator 再判定，也不會有 verdict 進入 disputes extrinsic，2/3 的正面門檻完全不起作用",
   "負面判定本身沒有任何後果；只有 disputes extrinsic 才算數，那裡的 verdict 需要全體作用中 validator 的一致簽署，而懲罰集合 ψ_O 只會從 culprits 填入、永遠不會從 faults 填入"
  ],
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
  "stemZh": "auditor 要怎麼取得重跑一份 work-report 所需的資料？",
  "optionsZh": [
   "它從大約三分之一的 validator 取得 erasure-coded 的碎片來重建 bundle，並對照 erasure-root 驗證；匯出的 segment 則靠重跑 refine 重新算出來",
   "它向出塊者下載整份 bundle——GP 要求出塊者保存它 28 天；匯出的 segment 會一併送達，所以完全不需要重跑 refine 的邏輯",
   "它直接從鏈上狀態讀取匯入與匯出的 segment：兩者都放在該 reporting service 的 preimage 底下，直到該 report 被 accumulate 之後才過期",
   "它請該 core 另外兩位 guarantor 重新簽署這份 report，並以一對相符的 Ed25519 簽章作為結果正確的證明；不會取得任何 bundle，也從不重跑 refine"
  ],
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
