# -*- coding: utf-8 -*-
# Off-chain protocol (ch. 15–19) + interview/conformance context — all filed under ARCH
ITEMS = [
{
 "id": "arch-audit-initial-tranche",
 "lens": "演算法",
 "ch": "ARCH", "section": "17.3 Selection of Reports", "gpRef": "eq. 17.2–17.4",
 "difficulty": 3, "kind": "concept", "tags": ["audit", "work-report"],
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
 "lens": "演算法",
 "ch": "ARCH", "section": "17.1 Overview", "gpRef": "§17.1",
 "difficulty": 2, "kind": "concept", "tags": ["audit", "dispute"],
  "stemZh": "GP §17.1 描述了出現負面判定時會發生什麼事。兩個門檻是什麼？各自導致什麼後果？",
  "optionsZh": [
   "若仍有超過 2/3 的 validator 發出正面判定，發出負面判定的人可能因浪費時間而受罰；若有超過 1/3 發出負面判定，含有該 report 的區塊會被列入禁用名單，它與其所有後代都會被忽略",
   "若有超過 1/2 的 validator 發出負面判定，該 report 會從它的 availability assignment 中被移除；若不足此數則什麼也不會發生——沒有任何 validator 會因為誤報而受罰，含有該 report 的區塊仍可繼續被建構",
   "單一個負面判定就足夠：它使承載該 report 的區塊無效，並沒收該 core 三位 guarantor 的質押；不需要其他 validator 再判定，也不會有 verdict 進入 disputes extrinsic，2/3 的正面門檻完全不起作用",
   "負面判定本身沒有任何後果；只有 disputes extrinsic 才算數，那裡的 verdict 需要全體作用中 validator 的一致簽署，而懲罰集合 ψ_O 只會從 culprits 填入、永遠不會從 faults 填入"
  ],
  "stem": "GP §17.1 describes what happens when a negative judgment appears. What are the two thresholds, and what follows from each?",
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
]
