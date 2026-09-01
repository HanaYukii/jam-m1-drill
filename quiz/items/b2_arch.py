# -*- coding: utf-8 -*-
# Batch 2 — architecture / design rationale / off-chain protocol (GP chapters 15–21) + ecosystem (JIPs, fuzzer, Prize).
# Equation numbers below were checked against the 0.8.0 PDF layout (gp-layout.txt); note that scripts/eqref.py is
# off by one in §17 from 17.12 onward (an empty numbered align row at 17.11), so PDF numbers are used here.
ITEMS = [
{
 "id": "arch-beefy-commitment",
 "ch": "ARCH", "section": "18 Beefy Distribution (ch. 18)", "gpRef": "eq. 18.1–18.2; eq. 7.7–7.8; §19–20",
 "difficulty": 2, "kind": "concept", "tags": ["beefy", "grandpa", "bridging", "off-chain"],
  "stemZh": "依 Beefy Distribution 這一章，validator 用哪把金鑰、在什麼時候、簽什麼？這個簽章又是拿來做什麼的？",
  "optionsZh": [
   "在匯入每個已定案的區塊之後：以 κ′[v] 的 BLS 金鑰對 $jam_beefy ⌢ b 做一個 BLS12-381 簽章，其中 b 是最新 β_H 條目所持有、accumulation 輸出腰帶的 Keccak MMR super-peak；這些簽章可自由發布，以便聚合成精簡的定案證明供橋接等第三方系統使用",
   "在匯入每個區塊之後（不論是否已定案）：以該 validator 的 BLS 金鑰對 posterior state root M_σ(σ′) 做 BLS12-381 簽章，好讓輕節點能驗證最新狀態；Grandpa 接著把這些簽章聚合成它的定案證明，而不再跑自己的投票回合",
   "每個 epoch 一次：對該 epoch 最後一個 header 的 Keccak 雜湊做 Ed25519 簽章，與 epoch marker H_E 一同發布，好讓經由 CoreChains service 橋接的 parachain 能證明整個 epoch 都已定案、而不必追蹤個別區塊",
   "對它所出的每個區塊：以 Bandersnatch VRF 簽章（context $jam_beefy）簽該區塊的 accumulation 輸出 root M_B(s, H_K)，放進 header 的 H_O marker，而那正是 Grandpa 投票者在定案該區塊時所簽的資料"
  ],
  "stem": "Per the Beefy Distribution chapter, what does a validator sign, with which key, and when — and what is the signature for?",
 "options": [
  "After importing each finalized block: a BLS12-381 signature under κ′[v]'s BLS key over $jam_beefy ⌢ b, where b is the Keccak MMR super-peak of the accumulation-output belt held in the newest β_H entry; the signatures are published freely so they can be aggregated into concise finality proofs for third-party systems such as bridges",
  "After importing every block, finalized or not: a BLS12-381 signature under the validator's BLS key over the posterior state root M_σ(σ′), so that light clients can verify the newest state; Grandpa then aggregates these signatures into its finality justification instead of running its own vote round",
  "Once per epoch: an Ed25519 signature over the Keccak hash of the epoch's last header, published alongside the epoch marker H_E so that parachains bridged through the CoreChains service can prove that the whole epoch was finalized without tracking individual blocks",
  "For each block it authors: a Bandersnatch VRF signature (context $jam_beefy) over the accumulation-output root M_B(s, H_K) of that block, which is placed in the header's H_O marker and is the datum that Grandpa voters sign when they finalize the block"
 ],
 "answer": 0,
 "optNotes": [
   "eq. 18.1–18.2：對每個已 finalized 且已 import 的 block，用 BLS 簽 X_B ⌢ last(β_H)_b。",
   "posterior state root 是 Grandpa vote 的內容，Grandpa 也不靠 BLS 聚合，時機更不是每個 block。",
   "金鑰型別與頻率都錯：Beefy 用的是 BLS12-381，而且是每個 finalized block 各簽一次。",
   "H_O 是 offenders marker；Bandersnatch 只用於 seal／ticket／entropy／audit VRF。",
 ],
 "explanation": "§18：「For each finalized block B which a validator imports, said validator shall make a BLS signature on the BLS12-381 curve… affirming the Keccak hash of the block's most recent Beefy MMR. This should be published and distributed freely… These signatures may be aggregated in order to provide concise proofs of finality to third-party systems.」eq. 18.1：Ξ_v ≡ S^BLS_{κ′[v]_bls}⟨X_B ⌢ last(β_H)_b⟩，eq. 18.2：X_B = $jam_beefy。b 是 β_H 最新一筆的 accumulation-output super-peak：eq. 7.7 先把 θ′ 的 (service, hash) 序列用 M_B(s, H_K) 取根、append 進 belt β′_B，eq. 7.8 再以 App. E 的 super-peak 函數 M_R（H_K($peak ⌢ …)）算出 b——全程 Keccak，§7 明說是「to maximize compatibility with legacy systems」（EVM 系橋用 Keccak precompile 便宜驗證）。分工要分清：Grandpa（§19）負責 JAM 內部 finality，投票資料是 best header＋posterior state root；Beefy 則是給鏈外系統看的可聚合 BLS 承諾（聚合機制見 eprint 2022/1611）。validator key K 的 BLS 公鑰佔 144 bytes（offset 64）。團隊程式：internal/recent_history 的 AppendAndCommitMmr 以 hash.KeccakHash 建 MMR 並回傳 SuperPeak（即 b）；Beefy 簽章本身屬 M2 node 範圍，main 尚未實作。§20 預算：Grandpa＋Beefy 合佔 1/16 CPU、每 slot 各 4 MB 上下行。",
 "trap": "三種金鑰三種用途：Bandersnatch = seal/ticket/entropy/audit VRF；Ed25519 = guarantee/assurance/judgment/announcement；BLS = 只有 Beefy（GP 未指定 Grandpa 投票的金鑰型別）。"
},
{
 "id": "arch-best-chain-selection",
 "ch": "ARCH", "section": "19 Grandpa and the Best Chain (ch. 19)", "gpRef": "eq. 19.1–19.4; §17 (ban-listing)",
 "difficulty": 2, "kind": "concept", "tags": ["best-chain", "grandpa", "auditing", "off-chain"],
  "stemZh": "一個節點如何選出它據以建塊、並投 Grandpa 票的最佳區塊 B♭？這張票又攜帶什麼資料？",
  "optionsZh": [
   "在已定案區塊的後代之中採最長鏈規則；同一個 timeslot 的兩個有效區塊都會保留，因為 Safrole 容忍 equivocation；是否已稽核只影響 accumulation、不影響投票；票中攜帶 header 雜湊連同取自 header 的先前狀態 root H_R",
   "候選者必須是最新已定案區塊的後代、必須被視為已稽核、且不得含有「位於節點已見過 equivocation 之 timeslot」的未定案祖先；在這些之中，帶有最多 ticket 封緘（非 fallback）祖先的那條鏈勝出；票中攜帶最佳 header 連同它的 posterior state root",
   "候選者必須是已定案區塊的後代且帶有最多 guarantee；累計 timeslot 最大的那條鏈勝出，好懲罰停滯的 core；票中只攜帶 header，因為 Grandpa 與狀態無關、state root 由 Beefy 提供",
   "候選者是所有父區塊已知的區塊；帶有最多 fallback 封緘祖先的那條鏈勝出，因為 fallback 金鑰屬於誠實多數；票中攜帶 header 加上 accumulation 輸出的 super-peak，好讓橋接能重用 Grandpa 的定案證明"
  ],
  "stem": "How does a node choose the best block B♭ on which it builds and casts Grandpa votes, and what data does the vote carry?",
 "options": [
  "Longest-chain rule among descendants of the finalized block; two valid blocks at the same timeslot are both kept because Safrole tolerates equivocation; audited status only gates accumulation, not voting; the vote carries the header hash together with the prior state root H_R taken from the header",
  "Candidates must descend from the latest finalized block, be considered audited, and contain no unfinalized ancestor at a timeslot where the node has seen an equivocation; among them the chain with the most ticket-sealed (non-fallback) ancestors wins; the vote carries the best header together with its posterior state root",
  "Candidates must descend from the finalized block and carry the most guarantees; the chain with the greatest cumulative timeslot wins so that stalled cores are penalised; the vote carries the header only, since Grandpa is independent of state and the state root is supplied by Beefy",
  "Candidates are all blocks whose parent is known; the chain with the most fallback-sealed ancestors wins because fallback keys belong to the honest majority; the vote carries the header plus the accumulation-output super-peak so that bridges can reuse Grandpa justifications"
 ],
 "answer": 1,
 "optNotes": [
   "longest chain 不是 JAM 的規則；§17 要求投 Grandpa 票前先視該 block 為 audited，投票也帶 posterior root。",
   "三個可接受條件（eq. 19.1–19.3）加上最大化 ticket-sealed 祖先數（eq. 19.4），投票內容也對。",
   "guarantee 數與 timeslot 總和都不是準則；投票必須附上 M_σ(σ′)，下游才驗得了最新狀態。",
   "方向相反——偏好的是 ticket-sealed 而非 fallback；super-peak 是 Beefy 的承諾，不進 Grandpa 投票。",
 ],
 "explanation": "§19 可接受集合（eq. 19.1–19.3）：A(H♭) ∋ H♮（以最新 finalized block 為祖先）；U♭ ≡ ⊤（已審計：§17 eq. 17.19，該 block 剛 available 的 R 中每個 report 都滿足 U(w)）；∄ H^A ≠ H^B 使 H^A_T = H^B_T、H^A ∈ A(H♭) 且 H^A ∉ A(H♮)（未 finalized 的 equivocation）。eq. 19.4：在可接受集合裡最大化 m = Σ_{H^A ∈ A♭} isticketed^A，即用 ticket 而非 fallback key seal 的祖先數——§17 也說 best block 是「the chain with the most regular Safrole blocks which does not contain any such disregarded block」，而被至少 1/3 驗證者判無效的 report 一旦被 accumulate，整條鏈不可再建塊（「may require reversion to an earlier head or alternative fork」）。投票資料：「the block header of the best block together with its posterior state root M_σ(σ′)」——header 只帶 prior root（§5 為了 pipelining），所以下游要能驗證最新狀態就得靠投票補上；後果是投票前必須先算完 posterior state，且「votes for the same block hash but with different associated posterior state roots are considered votes for different blocks」（只在節點失誤或文件歧義時發生）。團隊：fuzz target 以 RestoreBlockAndState(parent) 處理 fork（internal/fuzz/service.go）；#892 處理重複 slot／未知 parent；#783 曾把 prior/posterior root 搞反。",
 "trap": "GP 明說：block 是否 audited 在 finalize 當下可能沒有共識，但「This does not affect the crypto-economic guarantees」——最終會有共識。"
},
{
 "id": "arch-audit-tranches",
 "ch": "ARCH", "section": "17 Auditing and Judging (ch. 17)", "gpRef": "eq. 17.1–17.19 (PDF numbering); §20 (10 audits/validator/slot)",
 "difficulty": 3, "kind": "concept", "tags": ["auditing", "elves", "tranches", "off-chain"],
  "stemZh": "在稽核協定中，一位 validator 如何決定它必須稽核哪些剛變為可得的 work-report？這個集合又是如何隨時間成長的？",
  "optionsZh": [
   "Tranche 0：每個 core 的三位 guarantor 重跑自己的 report，好讓被指控方承擔成本；每 6 秒（一個 slot）依序輪替加入其餘 validator，直到超過 2/3 做出判決，此時該 report 即算已稽核，而任何做出負面判決的 validator 會被罰沒；不需要任何公告，因為輪替順序可由區塊雜湊導出",
   "Tranche 0：以 η′_2 為種子對 κ 做 Fisher–Yates 洗牌，為每份 report 指派恰好 30 位 auditor，對應 §20 每份 report 30 次稽核；一旦這 30 個正面判決到齊該 report 即算已稽核，而 tranche 0 之後不涉及 VRF，因為指派整個 epoch 都固定；後續 tranche 只有在出現負面判決時才會發生",
   "Tranche 0：以一個 Bandersnatch VRF 輸出（context $jam_audit ⌢ Y(H_V)）洗牌每個 core 上剛變可得的 report 清單，取前 10 個非空條目；每 A = 8 秒開始一個新 tranche，加入一份 report 的方式或是無條件（曾看到負面判決）、或是靠一個逐 report 的 VRF，其接受機率隨前一個 tranche 的缺席數成長，調校成每個缺席期望有 F = 2 位 validator 補上",
   "Tranche 0：每位 validator 稽核它在當前 rotation 所 guarantee 的那些 core 的 report，因為它本來就持有 bundle；每 8 秒再以 η′_3 洗牌選出 F = 3 份 report 加入；一份 report 一旦其三位 guarantor 重新背書即算已稽核，而負面判決在 validator 之間流言傳播、但從不放上鏈"
  ],
  "stem": "In the auditing protocol, how does a validator decide which newly-available work-reports it must audit, and how does that set grow over time?",
 "options": [
  "Tranche 0: the three guarantors of each core re-execute their own report so that the accused party bears the cost; every 6 s (one slot) the remaining validators are added round-robin until more than 2/3 have judged, at which point the report counts as audited and any validator that judged negatively is slashed; no announcements are needed because the round-robin order follows from the block hash",
  "Tranche 0: a Fisher–Yates shuffle of κ seeded with η′_2 assigns exactly 30 auditors to every report, matching the 30 audits per report of §20; a report is audited once those 30 positive judgments are in, and no VRF is involved after tranche 0 because the assignment is fixed for the whole epoch; later tranches only ever occur if a negative judgment appears",
  "Tranche 0: shuffle the per-core list of just-available reports with a Bandersnatch VRF output (context $jam_audit ⌢ Y(H_V)) and take the first 10 non-empty entries; a new tranche starts every A = 8 s, adding a report either unconditionally (a negative judgment was seen) or by a per-report VRF whose acceptance chance grows with the previous tranche's no-shows, tuned so that F = 2 validators are expected per no-show",
  "Tranche 0: each validator audits the reports of the cores it guarantees in the current rotation, since it already holds the bundle; every 8 s it adds F = 3 further reports chosen by shuffling with η′_3; a report counts as audited as soon as its three guarantors have re-attested, and negative judgments are gossiped between validators but never placed on-chain"
 ],
 "answer": 2,
 "optNotes": [
   "被懷疑的正是 guarantor，自審沒有安全意義；週期是 A = 8 秒，而且每個 tranche 都要先發 announcement。",
   "η′_2 是 fallback key sequence 的種子；30 是 §20 的期望值而非固定指派，tranche 0 之後仍有 per-report VRF。",
   "eq. 17.3／17.5 的 VRF 洗牌取前 10，加上 eq. 17.13–17.15 的 no-show VRF，F = 2 正是每個 no-show 期望補上的人數。",
   "F = 2 而非 3，context 是 X_U ⌢ Y(H_V) ⌢ H(w) ++ n；票數夠時 block author 會把 verdict 放進 E_D 上鏈。",
 ],
 "explanation": "eq. 17.1–17.2：q 是長度 |κ|/3（active cores 數）的序列，core c 的位置放 ρ[c] 的 report（若 ∈ R，即本 block 剛 available）否則 ∅。eq. 17.3：s_0 ∈ S^bs_{κ[v]_bs}⟨X_U ⌢ Y(H_V)⟩[]（Bandersnatch VRF，context $jam_audit 接本 block entropy VRF 輸出、空訊息）；eq. 17.5：a_0 = {w | w ∈ F(q, Y(s_0))[..10], w ≠ ∅}——Fisher–Yates 洗牌後取前 10 個非空。eq. 17.6：n = ⌊(T − P·H_T)/A⌋，A = 8 秒。新 tranche 的兩種來源：看到 negative judgment（一律必審）；或前一 tranche 的 judgment 數 < announcement 數（no-show）——後者用 eq. 17.13–17.15：s_n(w) 以 X_U ⌢ Y(H_V) ⌢ H(w) ++ n 為 context，條件 (|κ|/(256·F))·Y(s_n(w))_0 < |A_{n−1}(w) ∖ J_⊤(w)|，F = 2 是「the expected number of validators which will be required to issue a judgment for a work-report given a single no-show in the tranche before」（ELVES 論文模型顯示最佳）。每個 tranche 都先發 announcement（eq. 17.7：Ed25519 簽 X_I ++ n ⌢ x_n ⌢ H(H)，附 VRF 證據與前一 tranche 未配對的 announcement），且「Publication of an announcement should be taken as a contract to complete the audit regardless of any future information」。審計本體：向 1/3 驗證者索取 chunk 以 R_{|κ|} 重建 bundle（full 需 342 片），重算 Ξ(p, w_c, w_l, (w_a)_n) 必須與 w 相等（解碼失敗即無效，eq. 17.16），再以 Ed25519 發 judgment（eq. 17.17，context $jam_valid／$jam_invalid ⌢ H(w)）。eq. 17.18：U(w) ⟺ (J_⊥(w) = ∅ ∧ ∃n: A_n(w) ⊆ J_⊤(w)) ∨ |J_⊤(w)| > 2/3·|κ|；eq. 17.19：block audited ⟺ ∀w ∈ R: U(w)。後果：>2/3 仍判 positive → 判 negative 者可能因 time-wasting 受罰；>1/3 判 negative → 含該 report 的 block 被 ban-list、子孫全部不可建塊；block author 可組 verdict 放入 E_D（放在該 report 尚未 accumulate 的鏈上，會清掉 ρ 對應項）。§20 的「每驗證者每 slot 平均 10 次審計 → 每 report 約 30 次」是期望值，不是固定指派。ELVES 對照：backing/approval/inclusion = guaranteeing/auditing/accumulation。團隊：internal/auditing（#935 ComputeInitialAuditAssignment 漏 ValidatorID 導致只能靠超多數規則過關；#956 ComputeAnForValidator 門檻 s_n(w)[0]·V/(256·F) < m_n；#940 BuildJudgements 誤用公鑰簽名）；網路 CE144 announcement／CE145 judgment。",
 "trap": "F = 2 的直覺：每個 no-show 期望「再多 2 個人」來審；一個 negative judgment 則是「所有人都要審」。"
},
{
 "id": "arch-guaranteeing-procedure",
 "ch": "ARCH", "section": "15 Guaranteeing (ch. 15)", "gpRef": "§15; eq. 14.13 (Ξ); eq. 11.24, 11.28",
 "difficulty": 2, "kind": "concept", "tags": ["guaranteeing", "off-chain", "work-reports"],
  "stemZh": "關於 Guaranteeing 一章所描述的誠實 guarantor 策略，哪個敘述正確？",
  "optionsZh": [
   "在跑任何 refine 邏輯之前，先拿最新鏈狀態的 authorizer pool 檢查該 package 的授權（連同其他鏈上收納條件）；算出 r = Ξ(p, c, l, v) 之後，以 Ed25519 簽 $jam_guarantee ⌢ H(E(r))；兩個簽章就足以把 report 送給下一位出塊者；一份無法被收納的 report 只是損失獎勵，而謊報 Ξ 結果則會受重罰；平均每個 timeslot 至多簽兩份 report",
   "先跑完每個 work-item 的 refine、之後才檢查授權，因為 pool 反正會在鏈上重新驗證、而 refine 才是成本大宗；必須集齊全部三位 guarantor 的簽章才能把 report 送給出塊者；出塊者拒絕收納的任何 report 都算違規、會像無效 report 一樣被罰沒；一位 guarantor 每個 rotation 至多簽一份 report",
   "pool 檢查要用該 report 的 lookup-anchor 當時的鏈狀態、而不是當前鏈頭，好讓該 core 的所有 guarantor 對同一份視圖取得共識；單一個簽章就足以散播，因為出塊者會自行收集其餘 credential；因此 credential 清單可以未排序地抵達，而 GP 對一位 guarantor 每個 slot 能簽幾份 report 沒有給出指引",
   "以 Bandersnatch 金鑰在 $jam_guarantee context 下簽署該 report，好讓 ring 證明隱藏是該 core 的哪位 guarantor 簽的，所以鏈上 credential 不帶 validator 索引；兩個簽章足以散播；guarantor 每個 epoch 絕不該簽超過一份 report，否則出塊者的反垃圾過濾器會在該 epoch 剩下的時間裡無視他們"
  ],
  "stem": "Which statement about the honest guarantor strategy described in the Guaranteeing chapter is correct?",
 "options": [
  "Check the package's authorization against the authorizer pool of the most recent chain state (plus the other on-chain inclusion conditions) before running any refine logic; after r = Ξ(p, c, l, v), Ed25519-sign $jam_guarantee ⌢ H(E(r)); two signatures suffice to send the report to the next block author; an unincludable report only forfeits reward, a misrepresented Ξ result is punished severely; sign on average at most two reports per timeslot",
  "Run every work-item's refine first and check authorization only afterwards, since the pool is re-verified on-chain anyway and refine dominates the cost; all three guarantors' signatures must be collected before the report may be sent to the block author; any report the block author declines to include counts as an offence and is slashed exactly like an invalid report; a guarantor may sign at most one report per rotation",
  "Use the chain state at the report's lookup-anchor rather than the current head for the pool check so that all guarantors of the core agree on the same view; a single signature suffices for distribution because the block author collects the remaining credentials itself; the credential list may therefore arrive unsorted, and the GP gives no guidance on how many reports a guarantor may sign per slot",
  "Sign the report with the Bandersnatch key under the $jam_guarantee context so that the ring proof hides which of the core's guarantors signed, so the on-chain credential carries no validator index; two signatures suffice for distribution; guarantors should never sign more than one report per epoch, otherwise the block author's anti-spam filter disregards them for the rest of the epoch"
 ],
 "answer": 0,
 "optNotes": [
   "四點都對上 §15：先驗 authorization、兩個簽名即可分發、只有謊報 Ξ 結果才重罰、每 slot 平均不超過兩份。",
   "§15 要求所有檢查在評估 Ψ_R 之前完成，而被 block author 拒收只損失獎勵、不構成 offence。",
   "GP 明說「the chain state of the most recent block should always be utilized」；分發門檻也是兩個簽名。",
   "guarantee 用 Ed25519 且身分公開（credential 帶 validator index）；建議值是每 slot 平均兩份而非每 epoch 一份。",
 ],
 "explanation": "§15 流程：(1) 評估 work-package 的 authorization 並對照「the authorization pool in the most recent JAM chain state」；(2) 逐 work-item 執行 refine；(3) 依 erasure codec 切 bundle 與 exported data；(4) 組裝並發布 work-report；(5) 把 chunk 分發到驗證者集合；(6) 應要求提供 bundle／exported data。r = Ξ(p, c, l, v)（eq. 14.13）：guarantor 自行選 c（通常是自己被指派的 core）、l（segment-root dictionary，由先前 guaranteed 的 report 推得）、v（assuring validator set 大小，通常是 active set；遇 epoch 交界可對新舊兩個集合各編碼一次、產生兩份 report，但鏈上只能收一份，§14）。簽章：payload (s, i)，s 是 Ed25519 對 X_G ⌢ H(E(r)) 的簽名（鏈上 eq. 11.28 同式；credential 2–3 個、依 validator index 排序且唯一，簽名者須為本或前一 rotation 指派到該 core，eq. 11.24）。「With two guarantor signatures, the work-report may be distributed to the forthcoming JAM chain block author」。這題的重點是激勵不對稱：「validators will be punished severely if they malfunction and commit to a report which does not faithfully represent the result of Ξ」，而 contextual validity／pool 檢查沒做好「does not result in punishment, but will prevent the block author from including the report and so reduces rewards」。效率建議：所有檢查應在「prior to evaluating the Ψ_R function」之前做完，並把 package 轉給同 core 其他 guarantor 以形成共識；為免被 block author 的 anti-spam 忽略，「guarantors should sign an average of no more than two work-reports per timeslot」。團隊：CE133（builder→guarantor 提交）、CE134（guarantor 間分享）、CE135（report 分發）；#863/#860「not sorted or unique guarantors」錯誤碼、#864 guarantor 唯一性。",
 "trap": "先驗 authorization 再跑 refine：白跑 Ψ_R 不會被罰，但浪費的是自己的 CPU 與獎勵。"
},
{
 "id": "arch-two-da-classes",
 "ch": "ARCH", "section": "16 Availability Assurance (ch. 16) & 14 Exporting / Availability Specifier", "gpRef": "§16; §14 (Exporting, eq. 14.18); eq. 11.5, 11.11–11.18",
 "difficulty": 2, "kind": "concept", "tags": ["availability", "erasure-coding", "d3l", "off-chain"],
  "stemZh": "在一位 validator 於它的 assurance 中把某個 core 的位元設起之前，它必須持有哪些 erasure 編碼的資料？這些資料如何驗證？又必須保存多久？",
  "optionsZh": [
   "只需要它那一份 work-package bundle 的分片；segment 分片由後續的匯入者直接向匯出 package 的 guarantor 惰性取得；bundle 分片保存 L = 14,400 個 slot（24 小時）好讓 lookup-anchor 維持可稽核，而且不需要證明，因為 assurance 簽章會在鏈上對該 report 的 erasure-root 檢查",
   "完整的 work-package bundle 加上每一個匯出 segment 的明文（不是分片），驗證方式是在背書前於本地重算該 work-report，並保存 D = 19,200 個 slot，好讓該 package 所引用的任何原像能在爭議視窗期間重新驗證",
   "兩者都要：它那份可稽核 bundle 的分片（只保存到該 report 被視為已稽核／其區塊定案為止，在那之前依請求提供），以及該 report 的 segments-root 之下每一個匯出 segment 的分片加上分頁證明資料（長期的 D³L，保存 ≥ 28 天 = 672 個 epoch）；在宣稱持有之前，各自都要以 Merkle 證明對該 report 的 erasure-root 驗證",
   "它的 bundle 分片與 segment 分片，驗證是對 segments-root 而非 erasure-root，因為 erasure-root 只承諾了 bundle；bundle 分片保存 28 天，而 segment 分片在該 report 被 accumulate 後即可丟棄，因為 accumulation 會把匯出的 segment 複製進鏈上 service 儲存"
  ],
  "stem": "Before a validator sets a core's bit in its assurance, which erasure-coded data must it hold, how is that data verified, and for how long must it be kept?",
 "options": [
  "Only its shard of the work-package bundle; segment shards are fetched lazily by later importers directly from the guarantors of the exporting package; the bundle shard is retained for L = 14,400 slots (24 h) so that lookup-anchors stay auditable, and no proof is needed because the assurance signature is checked on-chain against the report's erasure-root",
  "The full work-package bundle plus every exported segment in clear (not shards), verified by recomputing the work-report locally before assuring, and kept for D = 19,200 slots so that any preimage referenced by the package can be re-verified during the dispute window",
  "Both its shard of the auditable bundle (kept only until the report is considered audited / its block finalized, served on request until then) and its shards of every exported segment under the report's segments-root plus paged-proof data (the long-term D³L, kept ≥ 28 days = 672 epochs), each verified by a Merkle proof against the report's erasure-root before possession is claimed",
  "Its bundle shard and segment shards, verified against the segments-root rather than the erasure-root since the erasure-root only commits to the bundle; the bundle shard is kept for 28 days while segment shards may be dropped once the report is accumulated, because accumulation copies the exported segments into on-chain service storage"
 ],
 "answer": 2,
 "optNotes": [
   "§16 要求兩類 shard 都持有；保留期也不是 L = 14,400，而且 assurance 前必須自己驗過 Merkle 證明。",
   "assurer 持有的是 erasure-coded shard 而非明文 bundle 與 segment；D = 19,200 是 preimage expunge 期限。",
   "兩類 shard 分得清楚：bundle shard 留到 audited／finality，segment shard 留 28 天，都以 erasure-root 驗證。",
   "erasure-root u = M_B(transpose[b♣, s♣]) 同時承諾兩者；accumulation 也不會把 segment 複製進鏈上 storage。",
 ],
 "explanation": "§16：「There are two classes of shard a validator must have for an availability assignment before claiming possession in an assurance」——(1) bundle 的 erasure-coded shard：「needed to verify the work-report's validity and completeness and need not be retained after the work-report is considered audited. Until then, it should be provided on request」；(2) segments-root 所指每個 exported segment 的 shard：「These should be retained for 28 days and provided to any validator on request」。驗證：「trivially proven through the work-report's work-package erasure-root and a Merkle-proof of inclusion in the correct location」，且「a validator should not claim possession of shards in an assurance unless it has, and has verified, the corresponding proofs」——鏈上對 assurance（eq. 11.11–11.14）只驗 Ed25519 簽章（X_A ⌢ H(E(H_P, f))）與 bitfield、不驗 shard 內容，所以證明必須自己在鏈下驗完。§14 Exporting 把兩者稱為短期 Audit DA store（assurer 保留到「finality of the block in which the availability of the work-result's work-package is assured」）與長期 D³L（Distributed, Decentralized, Data Lake，≥ 28 天 = 672 個完整 epoch，還含 paged-proofs：每 64 個 segment 一頁 hash＋子樹證明）。Availability specifier（eq. 14.18／eq. 11.5）：erasure-root u = M_B(transpose[b♣, s♣])——同時承諾 bundle 與 segments（含 paged proofs）的 chunk，chunk 數 n = assuring validator set 大小；segments-root e 只承諾 exported segments 本身（constant-depth Merkle）。鏈上規則對照：report 在 > 2/3·|κ| 的 assurance 後才 available（eq. 11.17），逾 U = 5 slot 未 available 則清出 ρ（eq. 11.18）。§20：全網 DA 容量約 2 PB、每節點最多 6 TB；assuring 每 slot 上行 144 MB。團隊：internal/store/work_package_bundle_store.go、CE137/138（shard 分發／audit shard 請求）、CE139/140（segment shard 請求）；#1035：erasure 參數依驗證者數（tiny 6 → 3 片可重建，full 1023 → 342 片）。",
 "trap": "兩個 DA：短期 audit DA（bundle shard）vs 長期 import DA / D³L（segment shard＋paged proofs，28 天）——兩者都在同一個 erasure-root 之下。"
},
{
 "id": "arch-core-virtual-hardware",
 "ch": "ARCH", "section": "20.1 Technical Characteristics & 20.2 Illustrating Performance (ch. 20)", "gpRef": "§20 Discussion",
 "difficulty": 2, "kind": "concept", "tags": ["performance", "hardware", "throughput", "rationale"],
  "stemZh": "Discussion 一章如何刻劃一份 work-package 在 JAM core 上所取得的「虛擬硬體」？它的結果之後又會怎樣？",
  "optionsZh": [
   "一整台 validator 機器（16 核、64 GB RAM、8 TB）獨佔一個 6 秒的 slot、鏈狀態 I/O 無上限；結果最大可達 12 MB，接著以相同的 I/O 預算 accumulate 至多一秒，這也是效能模型裡把 2/16 的 validator CPU 時間分給區塊執行的原因，而原像查詢也計入同一份 12 MB 預算",
   "大約一顆一般 CPU 核心、以原生速度的 25–50% 執行整個 6 秒 slot，約 2 MB/s 的通用 I/O（其中包含對近期 JAM 狀態的免信任讀取）與至多 2 GB RAM，外加對半靜態原像庫的無上限讀取；結果至多 48 KB，接著在同一台機器上取得約 10 ms、沒有外部 I/O 但對鏈狀態有完整且即時的存取",
   "一顆 CPU 核心以原生速度跑一秒，外加每 6 秒 slot 5 MB 的 I/O——原封不動沿用 Polkadot 的 parachain 預算，好讓 CoreChains 不必重新調校——結果至多 90 KB，並在下一個 slot 以完整狀態存取加上另外 6 秒的執行時間 accumulate；半靜態原像庫在 core 上完全無法觸及",
   "一顆以 25–50% 速度執行、配 2 GB RAM 的 CPU 核心，但完全無法存取鏈狀態，因為 refine 在構造上就是無狀態的；I/O 無上限，因為沒有任何東西會離開 core；那份 48 KB 的結果接著在稽核預算（10/16 的 CPU 時間）之內 accumulate，這也是每份 report 上限 10^7 gas、每個區塊 3.5·10^9 的原因"
  ],
  "stem": "How does the Discussion chapter characterise the 'virtual hardware' that a work-package gets on a JAM core, and what happens to its result afterwards?",
 "options": [
  "A full validator machine (16 cores, 64 GB RAM, 8 TB) for one 6-second slot with unlimited chain-state I/O; the result may be up to 12 MB and is then accumulated for up to one second with the same I/O budget, which is why block execution is allotted 2/16 of validator CPU time in the performance model, and preimage lookups are metered against that same 12 MB budget",
  "Roughly one regular CPU core at 25–50% of native speed for the whole 6-second slot, about 2 MB/s of general-purpose I/O (which includes trustless reads of recent JAM state) and up to 2 GB of RAM, plus unlimited reads from a semi-static preimage store; the result is at most 48 KB and then gets ~10 ms on the same machine with no external I/O but full, immediate access to chain state",
  "One CPU core at native speed for one second plus 5 MB of I/O per 6-second slot — the Polkadot parachain budget carried over unchanged so that CoreChains needs no re-tuning — with results up to 90 KB that are accumulated during the following slot with full state access and a further 6 s of execution; the semi-static preimage store is not reachable in-core at all",
  "A CPU core at 25–50% speed with 2 GB RAM but no access to chain state whatsoever, since refine is stateless by construction, and with unbounded I/O because nothing ever leaves the core; the 48 KB result is then accumulated inside the audit budget (10/16 of CPU time), which is why accumulation is capped at 10^7 gas per report and 3.5·10^9 per block"
 ],
 "answer": 1,
 "optNotes": [
   "16 核／64 GB／8 TB 是參考「節點」的規格；12 MB 是 bundle 量級 W_B，work-result 上限是 W_R = 48 KiB。",
   "整段對上 §20.1 原文：25–50% 速度、2 MB/s I/O、2 GB RAM、48 KB 結果，再 10 ms 且可直接讀狀態。",
   "1 秒原生算力加 5 MB I/O 是 Polkadot parachain 的預算；90 KB 沒有出處，preimage store 在 in-core 讀得到。",
   "GP 明說 I/O「includes any trustless reads from the JAM chain state」且設有 2 MB/s 預算，並非無上限。",
 ],
 "explanation": "§20.1：「What might be called the 'virtual hardware' of a JAM core is essentially a regular CPU core executing at somewhere between 25% and 50% of regular speed for the whole six-second portion and which may draw and provide 2MB/s average in general-purpose I/O and utilize up to 2GB in RAM. The I/O includes any trustless reads from the JAM chain state, albeit in the recent past. This virtual hardware also provides unlimited reads from a semi-static preimage-lookup database.」「Each work-package may occupy this hardware… to create some result of at most 48KB. This work-result is then entitled to 10ms on the same machine, this time with no 'external' I/O, but instead with full and immediate access to the JAM chain state.」對應常數：W_R = 48·2^10、G_R = 5·10^9（refine）、G_A = 10^7（每 report accumulate）、G_T = 3.5·10^9（每 block）、W_B = 13,791,360 ≈ 2 MB/s × 6 s。整台參考節點才是 16 核／64 GB／8 TB／0.5 GbE；CPU 分配 audits 10/16、block execution 2/16、Merklization、Grandpa+Beefy、erasure coding、networking 各 1/16；RAM：auditing 20 GB（10 個 PVM instance × 2 GB）、block execution 2 GB、state cache 40 GB（≈ 20,000 條 parachain 的 2 MB footprint）、misc 2 GB；頻寬每 slot 上行 304 MB／下行 281 MB（guaranteeing 106/48、assuring 144/13、auditing 0/133、authoring 53/87、Grandpa+Beefy 4/4），表中換算為 387/357 Mb/s（megabit），故建議 500 Mb/s 且要有 burst 餘裕；全網 DA 2 PB、每節點 ≤ 6 TB。吞吐估計（GP 自稱「a provisional and crude estimation only」）：JAM ≈ 85× single native CPU core 與 682 MB/s DA；simple-transfer 模型：12 MB package ÷ 128 B ≈ 96k tx，但 48 KB result ÷ 8 B（4 B index＋4 B balance）≈ 6k 筆更新 → 每 package ≈ 3k tx → 3k × 341 cores ÷ 6 s ≈ 171k TPS；若瓶頸改為 Merklization（500k–1M 次讀寫/秒）則 250k–350k TPS；把餘額更新也搬進 core 的分割模型可達 1.4M TPS 以上；EVM 對照：每 core ≈ 1,500 gas/µs（區間 500–5,000）vs Eth L1 1.25。三大來源：spatial parallelism、temporal parallelism（pipelining）、與硬體貼合的 VM/gas model。",
 "trap": "「85×」是相對於單一 native CPU core（Polkadot 為 13×，即約 6.5 倍 Polkadot），不是「85 倍 Polkadot」；且全是模型估計。"
},
{
 "id": "arch-sweet-spot-further-work",
 "ch": "ARCH", "section": "21 Conclusion / 21.1 Further Work (ch. 21)", "gpRef": "§21",
 "difficulty": 2, "kind": "rationale", "tags": ["rationale", "future-work", "architecture"],
  "stemZh": "結論一章稱 JAM 為一個「甜蜜點」，接著列出這份論文刻意留白的部分。哪個摘要正確？",
  "optionsZh": [
   "甜蜜點＝在接受 Solana 級硬體需求的前提下，達到與完全同步鏈相當的連貫性；未決事項：一旦證明成本降到原生的 50,000 倍以下就以 SNARK 證明取代 ELVES 稽核、把 D³L 保存期從 28 天縮短為 24 小時、把 refine 的匯入 segment 移進區塊本體、以及把 coretime 銷售與質押寫進後續章節而非委由系統 service；網路協定已在附錄中定案",
   "甜蜜點＝341 個 core 恰好塞滿一條 0.5 GbE 連線的那個點；考慮中：refine 期間 service 之間的同步呼叫、完全移除 `transfer` host call、解除每區塊的 accumulate gas 上限 G_T、以及在 state trie 中引入 Merklization 好讓授權無需完整下載即可判定；網路協定已在附錄完整規範，而 validator 獎勵已在鏈上追蹤",
   "甜蜜點＝像 Cosmos 那樣完全碎片化但共用同一個 validator 集合的設計；考慮中：捨棄 Beefy 改採純 Grandpa 證明、讓鏈上治理能原地升級 service、加入原生的簽署交易（因為 transfer 模型顯示只靠 refine 的轉帳受限於 I/O）、以及提高 48 kB 的 work-result 上限好讓 accumulate 看到更多資料；coretime 銷售與質押已在附錄規範",
   "甜蜜點＝在安全、有韌性的共識之下進行大量運算（不同於完全同步的模型），同時對一台單體狀態機提供嚴格的時序與整合保證（不同於持續碎片化的模型）；考慮中：accumulate 中的同步 service 呼叫、為了平行 accumulation 而限制 `transfer`、在特定條件下保留額外的 accumulate 運算、以及把 work-package 格式 Merkle 化好讓授權無需完整下載；網路層與代幣／coretime／質押層則留白"
  ],
  "stem": "The Conclusion calls JAM a 'sweet spot' and then lists what the paper deliberately leaves open. Which summary is accurate?",
 "options": [
  "Sweet spot = as coherent as a fully synchronous chain while accepting Solana-class hardware requirements; open items: replacing ELVES auditing with SNARK proofs once proving cost falls under 50,000× native, shortening D³L retention from 28 days to 24 hours, moving refine's imported segments into the block body, and writing coretime sales and staking into a later chapter rather than delegating them to system services; the networking protocol is already fixed in an appendix",
  "Sweet spot = the point where 341 cores exactly saturate a 0.5 GbE link; under consideration: synchronous calls between services during refine, removing the `transfer` host call entirely, lifting the per-block accumulate gas limit G_T, and introducing Merklization into the state trie so authorization can be judged without a full download; the networking protocol is fully specified in an appendix and validator rewards are already tracked on-chain",
  "Sweet spot = a fully fragmented design like Cosmos but sharing one validator set; under consideration: dropping Beefy in favour of Grandpa-only proofs, letting on-chain governance upgrade services in place, adding native signed transactions because the transfer model showed refine-only transfers are I/O-bound, and raising the 48 kB work-result limit so accumulate sees more data; coretime sales and staking are specified in the appendix",
  "Sweet spot = massive computation under secure, resilient consensus (unlike fully-synchronous models) with strict timing and integration guarantees into a singleton state machine (unlike persistently fragmented models); under consideration: synchronous service calls in accumulate, restricting `transfer` for parallel accumulation, reserving extra accumulate compute under certain conditions, and Merklizing the work-package format so authorization needs no full download; networking and token/coretime/staking layers are left out"
 ],
 "answer": 3,
 "optNotes": [
   "JAM 標榜的是 mostly-coherent 與一般規格硬體；用 SNARK 取代 ELVES 也與 §2 的成本論證相反。",
   "§20 算出的是每 slot 387／357 Mb/s 並刻意留 headroom；要 Merklize 的是 work-package 格式，state trie 早已 Merklize。",
   "「unlike persistently fragmented models」正好相反；§4.9.2 也明說沒有 transactor 這種概念。",
   "sweet spot 的兩個對照組與 §21.1 的四項待辦（同步呼叫、限制 transfer、保留額外算力、Merklize package）全部吻合。",
 ],
 "explanation": "§21：「We argue that the model of JAM provides a novel 'sweet spot', allowing for massive amounts of computation to be done in secure, resilient consensus compared to fully-synchronous models, and yet still have strict guarantees about both timing and integration of the computation into some singleton state machine unlike persistently fragmented models.」——兩個對照組分別是 fully-synchronous（Solana）與 persistently fragmented（Polkadot 1.0／Cosmos／rollups）。Further Work 明列四項可能修改：(1)「Synchronous calls between services in accumulate」；(2)「Restrictions on the transfer function in order to allow for substantial parallelism over accumulation」；(3)「The possibility of reserving substantial additional computation capacity during accumulate under certain conditions」；(4)「Introducing Merklization into the Work Package format in order to obviate the need to have the whole package downloaded in order to evaluate its authorization」。另外：「The networking protocol is also left intentionally undefined at this stage」（JAMNP-S 只在 docs.jamcha.in，且「will most likely not be formalized in the Graypaper」）；「we have also intentionally omitted details of higher-level protocol elements including cryptocurrency, coretime sales, staking and regular smart-contract functionality」；還需要更多實證效能研究、成本比較，以及 PVM 計量下 parachain-validation service 的吞吐原型。注意：§21 最後還寫「Validator performance is not presently tracked on-chain. We do expect this to be tracked on-chain in the final revision」——這段與 §13 的 π（0.6.4 起的 activity statistics）看起來不一致，疑似未更新的舊句，面試被問到時可指出。與 ch. 12 的呼應：Δ_seq／Δ_par 的張力正是「限制 transfer 以換取平行化」的動機。",
 "trap": "「sweet spot」對比的兩端：fully-synchronous（Solana）與 persistently fragmented（Polkadot 1.0 / Cosmos / rollups）。"
},
{
 "id": "arch-jip4-protocol-parameters-080",
 "ch": "ARCH", "section": "JIP-4 chainspec `protocol_parameters` = fetch(0) encoding (App. B), 0.7.2 → 0.8.0", "gpRef": "App. B fetch selector 0 (0.8.0 vs 0.7.2); JIP-4; JIP-5",
 "difficulty": 3, "kind": "delta", "tags": ["jip", "chainspec", "fetch", "delta-0.8.0", "code-gap"],
  "stemZh": "JIP-4 把 chainspec 的 `protocol_parameters` 定義為以 `fetch` 選擇子 0 的編碼所序列化的參數 blob。比較 GP 0.7.2 與 0.8.0，哪個敘述正確？",
  "optionsZh": [
   "這個 blob 在 0.7.2 與 0.8.0 之間沒有變（33 個定寬小端欄位、134 位元組）；0.8.0 反而把 V 與 N 移進創世 header 的 epoch marker H_E，所以 chainspec 必須在那裡重複 validator 數量，而節點從它匯入的第一個 epoch marker 讀取 ticket 數；因此既有解碼器除了也要解析 H_E 之外不需改動",
   "0.8.0 拿掉四個欄位——N（每位 validator 的 ticket 數，現為 ⌈2E/|γ′_P|⌉）、V（validator 數量，現由創世狀態中的 validator 集合隱含）、W_E 與 W_P（erasure 編碼大小，現由 validator 數量導出）——使該 blob 從 33 欄／134 位元組縮為 29 欄／122 位元組；解析器、以及任何仍從中覆寫「每 validator ticket 數／validator 數量／EC 大小」的『套用參數』程式碼都必須修改",
   "0.8.0 為新的 gas 模型常數（C_gasunknown 與各 host call 的基本成本）以及稽核常數 F 與 A 新增欄位，好讓 service 能透過 fetch(0) 讀取；V 留在 blob 裡，因為 validator 集合現在可變，而 service 必須知道集合大小才能為它的匯出計算 erasure 編碼參數，所以該 blob 從 33 欄／134 位元組成長為 41 欄／168 位元組",
   "0.8.0 保留全部 33 個欄位，但把它們從定寬小端整數改為通用的緊湊編碼 E(x)，所以 blob 長度現在取決於數值（例如 1,023 與 6 位 validator 的差別）；JIP-4 同時把 `genesis_state` 的 key 從 31 位元組加寬為 32 位元組，好讓 state trie 無需重新雜湊即可載入，而一份 tiny chainspec 現在編碼後遠小於 122 位元組"
  ],
  "stem": "JIP-4 defines a chainspec's `protocol_parameters` as the JAM-serialized parameter blob in the encoding of `fetch` selector 0. Comparing GP 0.7.2 with 0.8.0, which statement is correct?",
 "options": [
  "The blob is unchanged between 0.7.2 and 0.8.0 (33 fixed-width little-endian fields, 134 bytes); 0.8.0 instead moved V and N into the genesis header's epoch marker H_E, so a chainspec must repeat the validator count there and a node reads the ticket count from the first epoch marker it imports; existing decoders therefore need no change beyond also parsing H_E",
  "0.8.0 drops four fields — N (tickets per validator, now ⌈2E/|γ′_P|⌉), V (validator count, now implied by the validator sets in the genesis state), W_E and W_P (erasure-coding sizes, now derived from the validator count) — shrinking the blob from 33 fields / 134 bytes to 29 fields / 122 bytes; parsers and any 'apply parameters' code that still overwrites tickets-per-validator, validator count or EC sizes from it must change",
  "0.8.0 adds fields for the new gas-model constants (C_gasunknown and the host-call base costs) and for the audit constants F and A so that services can read them via fetch(0); V stays in the blob because validator sets may now vary and a service must know the set size to compute erasure-coding parameters for its exports, so the blob grows from 33 fields / 134 bytes to 41 fields / 168 bytes",
  "0.8.0 keeps all 33 fields but switches them from fixed-width little-endian integers to the general compact encoding E(x), so the blob length now depends on the values (e.g. 1,023 versus 6 validators); JIP-4 widened the `genesis_state` keys from 31 to 32 bytes at the same time so that the state trie can be loaded without re-hashing, and a tiny chainspec now encodes to well under 122 bytes"
 ],
 "answer": 1,
 "optNotes": [
   "epoch marker H_E 只帶 entropy 與下一 epoch 的金鑰，不放 V／N；blob 本身確實從 33 欄縮成 29 欄。",
   "N、V、W_E、W_P 四欄消失，122 bytes = 7×8 + 11×2 + 11×4；照舊覆寫這四項的程式都得改。",
   "審計常數與 gas／PVM 常數本來就不在 Ω_Y 裡，0.8.0 也沒有把驗證者數留在 blob 內。",
   "編碼仍是固定寬度 little-endian，所以 tiny 與 full 一樣都是 122 bytes；JIP-4 的 state key 也仍是 31 bytes。",
 ],
 "explanation": "JIP-4：chainspec JSON 有 id、bootnodes（`<name>@<ip>:<port>`，name 是 53 字元 DNS 名：'e' ＋ base-32 Ed25519 公鑰）、genesis_header（JAM-serialized header 的 hex）、genesis_state（「Each key is a 62-character hex string defining the 31-byte state key」，值為任意長度 hex）、protocol_parameters（「A hex string containing JAM-serialized protocol parameters. Encoding matches protocol parameters returned by the fetch host call」）。0.7.2 的 fetch(0)（App. B Ω_Y，φ_10 = 0）依序為 E_8(B_I, B_L, B_S)、E_2(C)、E_4(D, E)、E_8(G_A, G_I, G_R, G_T)、E_2(H, I, J, K)、E_4(L)、E_2(N)、E_2(O, P, Q, R, T, U)、E_2(V)、E_4(R_A, W_B, W_C)、E_4(R_E)、E_4(R_M)、E_4(R_P)、E_4(R_R, W_T, W_X, Y)——33 欄、134 bytes。0.8.0 的 Ω_Y 只剩 29 欄：B_I, B_L, B_S, C, D, E, G_A, G_I, G_R, G_T, H, I, J, K, L, O, P, Q, R, T, U, W_A, W_B, W_C, W_M, W_R, W_T, W_X, Y，共 7×8 + 11×2 + 11×4 = 122 bytes。原因：#527 把每人票數 N 改為公式 ⌈2E/|γ′_P|⌉（tiny 4、full 2）；#514 允許可變驗證者集合（|κ| ∈ {3c | c ∈ [2, C+1]}，來自 genesis state 的 ι/κ/λ，不再是常數）；App. H 的 erasure coding 改以 d(v) = max{d ∈ N_{v/3+2} | W_G mod 2d = 0} 由 v 推導，所以 W_E／W_P 消失（W_G = 4104 仍是常數但本來就不在 blob 裡）。仍不在 blob 內的還有審計常數、C_gasunknown 等 gas 常數與 Z_*（PVM）；編碼也仍是固定寬度 little-endian，31-byte state key 未變。團隊程式：types.ProtocolParameters（types.go:1683）仍是 0.7.2 的 33 欄（含 N、V、WE、WP）；ApplyProtocolParameters（protocol_parameters.go）先斷言不可變常數（B_I, B_L, B_S, P, H, O, Q, I, J, U, G_A, G_I, W_A, W_B, W_C, W_R, W_T, W_M, W_X, T）再覆寫 C, D, E, G_R, G_T, K, L, N, R, V, W_E, W_P, Y——升到 0.8.0 時解碼順序要拿掉 N/V/W_E/W_P，V 改由 genesis state 取得，N 改用公式；#1035/#1022 已示範過 erasure 參數與驗證者數不一致會悄悄改變 erasure root。同一份 blob 也是 service 透過 fetch(0) 看到的（appB-fetch）。JIP-5 補充：dev 驗證者金鑰由 blake2b('jam_val_key_ed25519' ++ seed)／blake2b('jam_val_key_bandersnatch' ++ seed) 推導，trivial_seed(i) = 8 × E_4(i)，不含 BLS（internal/keystore/jip5_key_derivation.go）。",
 "trap": "0.8.0 的 chainspec 不再告訴你 V——驗證者數量要數 genesis state 裡的 κ/ι；tiny 的 N 也不再是 3 而是 ⌈2·12/6⌉ = 4。"
},
{
 "id": "arch-fuzz-protocol-m1",
 "ch": "ARCH", "section": "jam-conformance fuzz protocol & the M1 evaluation pipeline", "gpRef": "davxy/jam-conformance fuzz-proto README; w3f/jam-milestone-delivery PRs",
 "difficulty": 2, "kind": "concept", "tags": ["conformance", "fuzzer", "history", "m1"],
  "stemZh": "關於 W3F 用於 M1 稽核的 jam-conformance fuzz 協定，哪個描述正確？",
  "optionsZh": [
   "一個架在 WebSocket（連接埠 19800）之上的 JSON-RPC 2.0 會話，由 fuzzer 監聽、目標端撥接；區塊以十六進位字串傳輸，每次 importBlock 呼叫回覆的是 header 雜湊而不是 state root；區塊被拒會關閉連線，ancestry 由 fuzzer 從 finalizedBlock 訂閱重建而非由外部提供，而且從不產生分叉，因為 Safrole 排除了 equivocation",
   "一條 TCP 串流，由目標端撥接 fuzzer 並送出第一個握手訊息；區塊以 SCALE 編碼、前綴一個 u16 大端長度；fuzzer 在每個區塊後比對完整狀態傾印而非 root，無效區塊是靠乾脆不回應來表示，而 ancestry 功能對 M1 是選用的，因為 lookup-anchor 檢查約束的是出塊者而不是匯入者",
   "一個基於檔案的協定：fuzzer 把編號的區塊 .bin 檔寫進共享目錄，目標端在旁邊寫出 post-state JSON；握手是一個版本檔而不是 PeerInfo 交換，所以沒有功能協商、ancestry 與分叉一律開啟；第一次 state root 不符就中止該次執行、不產生報告，且該 GP 版本的送審視為失敗",
   "一個架在「由目標端監聽的 Unix domain socket」之上的同步請求／回應協定；訊息以 JAM codec 編碼、前綴一個 u32 小端長度；在 PeerInfo 握手（features = 雙方的位元 AND）之後，fuzzer 送出 Initialize（header、狀態鍵值、祖先清單），接著送 ImportBlock 請求，每個都以 posterior state root 或 Error（狀態不變）回覆；root 不符會觸發 GetState；ancestry 與分叉對 M1 是必備的"
  ],
  "stem": "Which description of the jam-conformance fuzz protocol that the W3F used for the M1 audit is correct?",
 "options": [
  "A JSON-RPC 2.0 session over WebSockets (port 19800) that the fuzzer binds and the target dials; blocks travel as hex strings and each importBlock call is answered with the header hash rather than a state root; a rejected block closes the connection, ancestry is reconstructed by the fuzzer from a finalizedBlock subscription instead of being supplied, and forks are never generated because Safrole precludes equivocation",
  "A TCP stream on which the target dials the fuzzer and sends the first handshake message; blocks are SCALE-encoded behind a u16 big-endian length prefix; the fuzzer diffs a full state dump after every block rather than a root, an invalid block is signalled by simply omitting the response, and the ancestry feature is optional for M1 because lookup-anchor checks bind block authors rather than importers",
  "A file-based protocol: the fuzzer writes numbered block .bin files into a shared directory and the target writes post-state JSON beside them; the handshake is a version file rather than a PeerInfo exchange, so there is no feature negotiation and ancestry and forks are always on; on the first state-root mismatch the run stops, no report is produced, and the submission is failed for that GP version",
  "A synchronous request/response protocol over a Unix domain socket the target binds; messages are JAM-codec encoded with a u32 little-endian length prefix; after a PeerInfo handshake (features = bitwise AND of both sides) the fuzzer sends Initialize (header, state key-vals, ancestor list) then ImportBlock requests, each answered by the posterior state root or an Error (state unchanged); a root mismatch triggers GetState; ancestry and forks are mandatory for M1"
 ],
 "answer": 3,
 "optNotes": [
   "JSON-RPC／WebSocket 19800 是 JIP-2 的節點 RPC；被拒的 block 回 Error 後連線繼續，forks 對 M1 更是必備。",
   "實際是 Unix socket、JAM codec、u32 little-endian，fuzzer 先送 PeerInfo，而且每塊比對的是 state root。",
   "沒有目錄／檔案協定；feature 由雙方 PeerInfo 的 bitwise-and 協商，mismatch 之後還要產出完整 fuzz report。",
   "Unix socket、JAM codec、u32 little-endian 長度前綴、PeerInfo 交集協商，全部對上 fuzz-proto README。",
 ],
 "explanation": "davxy/jam-conformance fuzz-proto README：「a synchronous request-response protocol over Unix domain sockets」，target 綁定具名 SOCK_STREAM socket（例 /tmp/jam_target.sock），只有 fuzzer 發起請求、target 回覆後才有下一個；「All messages are encoded according to the JAM codec format. Prior to transmission, each encoded message is prefixed with its length, represented as a 32-bit little-endian integer」。訊息：PeerInfo（discriminant 0x00，含 fuzz_version、fuzz_features、jam_version、app_version、app_name；fuzzer 先送、target 再回）；Initialize（header＋state key-vals＋開啟 ancestry 時的 ancestor list）→ StateRoot（0x02）；ImportBlock → StateRoot 或 Error（0xff；「the target must return an Error message and then wait for the next block」，狀態不變）；GetState → State（整個 key-val 儲存）。「Session features are determined by the intersection (bitwise-and) of the features listed in the PeerInfo message」；M1 必備：feature-ancestry（Initialize 帶祖先清單以做 GP 規定的 lookup-anchor 檢查，tiny 最多 24 筆）與 feature-forks（fuzzer 以突變 block 製造 fork，主鏈只從原始 block 延伸）——Safrole 只保證每個 slot 單一 sealer，並不使 equivocation 不可能，否則就不需要 disputes 與 best-chain 規則了。判定：每次 import 後比對 state root，「When a state root mismatch is detected the fuzzer attempts to fetch the whole state from the target to produce a comprehensive fuzz report」。M1 流程：W3F 以 GP 0.7.2 target 跑「1 million steps」（結果推到 fuzz-reports/0.7.2）→ Parity 審核 → Fellowship 錄音面試（rule 12）→ Fellows track referendum 以 remark「approves in full」批准（#595–#598）。團隊：internal/fuzz/messages.go 的型別（PeerInfo=0、SetState=1〔即 Initialize 的舊名〕、StateRoot=2、ImportBlock=3、GetState=4、State=5、Error=255）；#785 拒絕 block 時回 Error 並保持 pre-state root；#828 trace 中全零 post-state root 代表「必須拒絕」；#991/#983 fuzz 模式依 MaxLookupAge（tiny 24）修剪狀態；config.DefaultConfig().Info 就是送出的 PeerInfo（FuzzVersion 1）。",
 "trap": "Error 回應 = block 被拒但連線繼續、狀態不變；runtime panic 才是真正的 bug——你們的 STF 以 *types.ErrorCode 區分 protocol error 與 runtime error。"
},
{
 "id": "arch-prize-interview-rule12",
 "ch": "ARCH", "section": "JAM Prize rules (rule 12) & milestone-delivery T&Cs", "gpRef": "jam.web3.foundation/rules #12; T&C 3.5 / 6.1 / 8.4; delivery template",
 "difficulty": 1, "kind": "concept", "tags": ["prize", "history", "interview"],
  "stemZh": "依 JAM Prize 規則與里程碑交付條款，送審後的口試其目的與地位是什麼？",
  "optionsZh": [
   "它是對效能測試（gas、trie／DB、簽章驗證、可得性）的強制口頭答辯，由基金會在標準硬體上執行；主持者是 W3F 員工而非 Fellowship，且不錄影，第 12 條只涵蓋 benchmark harness 的著作權，生成式 AI 的使用另依 clean-room 規則處理，而且設計上其結果無法改變所頒發的獎項",
   "它是與 Parity 稽核者針對 conformance fuzzer 發現所做的選擇性問答；通過它就不必再通過公開與私有的一致性測試，結果由基金會在鏈下記錄而非由 Fellowship 在鏈上批准，而既然是選擇性的，婉拒的團隊只需等下一個審查視窗、對其獎項毫無影響",
   "它可在送審後被要求，用以查驗團隊成員是否為正當作者（排除生成式 AI）、並對 Gray Paper 與自家程式碼庫兩者都具備確切的專業；交付範本使團隊承諾接受一場由 Polkadot Technical Fellowship 進行、且錄影的口試，並以鏈上的 Fellowship remark 批准，而未能證明專業可能導致獎金減少或團隊被取消資格",
   "它是僅限於 PVM 與 host call 實作的程式碼審查會；使用過生成式 AI 的團隊只要在交付文件中事先申報仍可通過，主持者取自該團隊自己的客戶端實作同儕，而表現不佳唯一可能的後果是付款延後到協定 1.0 版獲批准為止"
  ],
  "stem": "According to the JAM Prize rules and the milestone-delivery terms, what is the purpose and standing of the post-submission interview?",
 "options": [
  "It is a mandatory oral defence of the performance tests (gas, trie/DB, signature verification, availability) that the Foundation runs on standard hardware; it is conducted by W3F staff rather than the Fellowship and is not recorded, rule 12 covering only authorship of the benchmark harness, generative-AI use being handled separately under the clean-room rule, and by design the outcome cannot change the prize awarded",
  "It is an optional Q&A with Parity's auditors about findings from the conformance fuzzer; passing it replaces the need to pass the public and private conformance tests, the outcome is recorded off-chain by the Foundation rather than ratified by the Fellowship on-chain, and because it is optional a team that declines simply waits for the next review window with no effect on its prize",
  "It may be requested after submission to verify that team members are the legitimate authors (precluding generative AI) with definitive expertise on both the Gray Paper and their own codebase; the delivery template commits the team to a recorded interview by the Polkadot Technical Fellowship, ratified by an on-chain Fellowship remark, and failing to prove expertise may reduce the prize or disqualify the team",
  "It is a code-review session limited to the PVM and host-call implementation; teams that used generative AI may still pass provided they declared it up-front in the delivery document, the interviewers are drawn from the team's own client-implementation peers, and the only possible consequence of a poor showing is that payment is deferred until version 1.0 of the protocol is ratified"
 ],
 "answer": 2,
 "optNotes": [
   "效能測試是 rule 5 的獨立要求；rule 12 的面試由 Fellowship 主持、範本明文是 recorded，且確實會影響獎金。",
   "rule 20 要求通過所有相關公開與私有測試，面試取代不了；核准也是 Fellows track 的 on-chain remark。",
   "rule 12 的三個要素齊備：authorship 與 expertise 的驗證、錄音面試加 on-chain remark、減額或取消的後果。",
   "考的範圍是 GP 全文加自家程式；rule 9 是「must not be used in any substantive way」而非事先申報即可。",
 ],
 "explanation": "jam.web3.foundation/rules 第 12 條原文：「An interview may be requested after submission to ensure team members are the legitimate authors of the code. This precludes the use of generative AI. The interview will seek to ensure the individual has definitive expertise on both the Graypaper and their own codebase. INABILITY TO PROVE THIS EXPERTISE MAY RESULT IN A REDUCED PRIZE OR FULL DISQUALIFICATION.」milestone-delivery 範本的聲明：「we agree to a recorded interview by the Polkadot Technical Fellowship on any matter arising from this milestone submission」與「this milestone submission will need to be ratified with an on-chain remark by the Polkadot Technical Fellowship before it can be merged」。周邊條款：T&C 6.1 允許 Foundation 在提交後要求面試以釐清；T&C 3.5 規定 conformance 以評估當時最新 GP release 為準（所以 0.8.0 差異必考）；T&C 8.4：M1 可在 GP 1.0 批准前付款（2026 年 2 月的 early acceptance 修訂），其餘里程碑不行；rule 5 另有獨立的效能測試（gas、trie/DB、簽章驗證、availability，由 W3F 在標準硬體上跑）；rule 20 要求通過所有相關公開與私有 conformance／performance 測試；rule 9 禁止實質使用生成式 AI；rule 6 clean-room。評審是 Polkadot Fellowship（排除涉入該實作的成員，Gav 的 HackMD）。實際流程（2026）：W3F fuzz（1M steps，GP 0.7.2）→ Parity audit → Fellowship 面試 → Fellows referendum（#595–#598 的 remark「approves in full」，暗示部分核准也可能）。",
 "trap": "面試考兩件事：你「寫了」這份程式（authorship），以及你「懂」GP 與自己的程式（expertise）——回答時把 GP 條文與自家 code 路徑一起講。"
},
]
