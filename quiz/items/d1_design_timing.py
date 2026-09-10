# -*- coding: utf-8 -*-
# 設計概念與更新時機：每題問「這個東西為什麼存在、什麼時候被更新、從哪個輸入更新」，
# 或「這條 formula 為什麼這樣設計」。深度在基礎套題之上，但不考實作細節。
ITEMS = [
{
 "id": "d1-rho-three-stages-order",
 "alsoCh": ["10"],
 "ch": "11", "section": "4.1 dependency graph; 10.4; 11.3", "gpRef": "eq. 4.x (ρ† ρ‡ ρ′), eq. 10.14, eq. 11.18",
 "difficulty": 2, "kind": "rationale", "tags": ["rho", "ordering", "design"],
  "stemZh": "ρ 在一個 block 裡被更新三次：ρ†（吃完 E_D）、ρ‡（吃完 E_A）、ρ′（吃完 E_G）。為什麼是這個順序？如果把 E_G 排在 E_A 之前處理，會壞在哪？",
  "optionsZh": [
   "disputes 先清掉被判 bad 的 report，它才不會在同一個 block 變 available；assurance 再把 available 或 timeout 的 core 清空；guarantee 只能落在 ρ‡[c] = ∅ 的 core。若 E_G 先於 E_A，剛被釋放的 core 在這個 block 仍是滿的，新 guarantee 得等下一個 block",
   "順序只是 GP 為了公式好寫：三個 extrinsic 各自操作 ρ 的不同欄位，disputes 動 report hash、assurance 動 bitfield 計數、guarantee 動 timeslot，彼此不相依，所以任何順序算出的 ρ′ 都相同，只是中間值的符號 † 與 ‡ 會換位置",
   "guarantee 必須先進來、才有東西給 assurance 背書，所以正確順序其實是 E_G → E_A → E_D，同一個 block 內的 guarantee 就能被同一個 block 的 assurance 背書；GP 把 E_D 放最前面只是因為 verdict 的簽章驗證最貴，要早點拒絕壞 block",
   "assurance 必須先於 disputes，因為 verdict 只能針對已經 available 的 report，未 available 的 report 資料拿不到、auditor 無從判定；把 E_D 放在最前是 0.8.0 的筆誤，實作上兩者可以交換而不影響 state root"
  ],
  "stem": "ρ is updated three times within one block: ρ† (after E_D), ρ‡ (after E_A) and ρ′ (after E_G). Why that order, and what would break if E_G were processed before E_A?",
 "options": [
  "Disputes first, so a report judged bad is cleared before it can become available in the same block; assurances then free every core whose report became available or timed out; a guarantee may only land on a core with ρ‡[c] = ∅. With E_G before E_A, a core freed by this block's assurances would still look occupied, and a new guarantee for it would wait a block",
  "The order is only a presentational choice: the three extrinsics touch different fields of ρ — disputes the report hash, assurances the bitfield count, guarantees the timeslot — and none depends on another, so every ordering yields the same ρ′ and only the † and ‡ labels on the intermediate values would swap places",
  "Guarantees must come first so that there is something for assurances to attest, so the real order is E_G → E_A → E_D and a guarantee can be assured within the very block that carries it; the GP lists E_D first only because verdict signatures are the most expensive to verify and a bad block should be rejected early",
  "Assurances must precede disputes because a verdict can only concern a report that is already available, since auditors cannot fetch the data of an unavailable one; listing E_D first is a 0.8.0 slip, and an implementation may swap the two without changing the state root"
 ],
 "answer": 0,
 "optNotes": [
   "抓到了三個順序的因果：bad 先清、available/timeout 再清、guarantee 只填空位；也說出交換後的具體代價。",
   "三者不是獨立的：11.18 讀 ρ†、guarantee 的 core_engaged 檢查讀 ρ‡，順序改變會改變哪些 guarantee 有效，state root 就不同。",
   "方向反了：assurance 背書的是「上個或更早 block」已經在 ρ 裡的 report，同一個 block 的 guarantee 還沒有 shard 可背書。",
   "verdict 針對的是 report hash，不需要它 available；而且依賴圖是規格的一部分，不是可交換的實作選擇。"
 ],
 "explanation": "§4 的依賴圖把 ρ 的三段寫死：ρ† ≺ (E_D, ρ)、ρ‡ ≺ (E_A, ρ†)、ρ′ ≺ (E_G, ρ‡, κ, τ′)。每一段各做一件事：eq. 10.14 把 report hash 落在 ψ′_B 的 core 清空（bad 的東西不能再往下走）；eq. 11.18 把「超過 2/3 assurance 變 available」「H_T ≥ t + U 逾時」「|κ| ≠ |κ′| 集合大小改變」三種情況的 core 清空；接著 E_G 的 guarantee 只能落在 ρ‡[c] = ∅ 的 core。這個順序讓一個 core 可以在同一個 block 裡「舊 report 變 available → 新 guarantee 進來」，吞吐量才是每 core 每 slot 一份。反過來先處理 E_G，剛被釋放的 core 對這個 block 來說還是滿的，新 guarantee 會被 core_engaged 拒絕，平白浪費一個 slot。口試常見追問：「為什麼 R（剛 available 的 report）是從 ρ† 而不是 ρ 讀？」因為要先排除被 dispute 清掉的。",
 "trap": "記口訣：清壞的 → 清完成的 → 填新的。三段各對應一個 extrinsic。"
},
{
 "id": "d1-lambda-who-reads-it",
 "alsoCh": ["10", "11"],
 "ch": "6", "section": "6.2 validator sets; 10.3; 11.3", "gpRef": "eq. 6.14, eq. 10.4, eq. 11.23",
 "difficulty": 2, "kind": "rationale", "tags": ["validator-sets", "lambda", "design"],
  "stemZh": "state 同時保留三個 validator set：ι（下期）、κ（本期）、λ（上期）。κ 是當然要有的；λ 為什麼要留在 state 裡？哪些檢查會去讀它？",
  "optionsZh": [
   "因為有些簽章是上個 epoch 的人簽的、卻在這個 epoch 才進 block：verdict 的 epoch index 可以是 e−1，判定簽章要對 λ 驗；epoch 邊界附近屬於上個 rotation 的 guarantee，M* 要用 λ′ 重算指派；culprit 與 fault 的 offender key 也允許來自 κ ∪ λ",
   "λ 只是給統計用的：π_L 記錄上個 epoch 每位 validator 的 block、ticket、preimage、guarantee、assurance 計數，需要對應的金鑰序列才能把 index 轉回 key 好發獎勵；除此之外 disputes、guarantee、seal 的驗證都只讀 κ′，沒有任何驗證步驟會讀 λ",
   "λ 是為了讓被踢出的 validator 還能領最後一期的獎勵：offender 的 key 在 Φ 過濾時從 κ′ 移除，但仍留在 λ 一個 epoch，好讓下個 epoch 結算 reward 時找得到他的 Ed25519 key 與 BLS key；等 λ 再往後推一格，他才真正從 state 消失",
   "λ 是 fallback 用的：當 ticket 不足、γ′_S 退回 F(η′_2, ·) 時，slot-sealer 序列從 λ 而不是 κ′ 產生，理由是 λ 在上個 epoch 就已定案、無法再被操縱，攻擊者便不能藉由在本 epoch 改動 ι 來影響下個 epoch 的出塊者"
  ],
  "stem": "The state keeps three validator sets: ι (next), κ (current) and λ (previous). κ is obviously needed. Why is λ kept in state at all, and which checks read it?",
 "options": [
  "Because some signatures are made by last epoch's validators but only reach a block in this epoch: a verdict may carry epoch index e−1, so its judgments verify against λ; a guarantee near an epoch boundary that belongs to the previous rotation is checked with M*, recomputed from λ′; and culprit and fault offender keys may come from κ ∪ λ",
  "λ exists only for statistics: π_L records each validator's block, ticket, preimage, guarantee and assurance counts for the previous epoch and needs the matching key sequence to turn indices back into keys for rewards; disputes, guarantees and seals all verify against κ′ alone, so no validation step reads λ",
  "λ lets an ejected validator collect its final epoch's reward: an offender's key is dropped from κ′ when Φ filters it, but it stays in λ for one epoch so that next epoch's reward settlement can still find its Ed25519 and BLS keys; only when λ shifts once more does the validator truly leave the state",
  "λ serves the fallback: when tickets run short and γ′_S falls back to F(η′_2, ·), the slot-sealer sequence is generated from λ rather than κ′, on the grounds that λ was fixed an epoch ago and can no longer be manipulated, so an attacker cannot influence next epoch's authors by altering ι during this epoch"
 ],
 "answer": 0,
 "optNotes": [
   "三個讀者都對：eq. 10.4 的 K(a) 在 a = e−1 時取 λ；eq. 11.23 的 M* 跨 epoch 時用 λ′；eq. 10.6–10.7 的 offender key 取自 κ ∪ λ。",
   "π_L 只存計數器不存 key，GP 也沒有 reward 結算；而 disputes 與 guarantee 的驗證確實會讀 λ。",
   "GP 沒有 reward 計算；offender 是被 Φ 在輪替時歸零，不是靠 λ 留一期。",
   "fallback 序列 F(η′_2, κ′) 用的是 κ′，不是 λ。"
 ],
 "explanation": "λ 存在的理由是「簽章時間」和「上鏈時間」可以跨 epoch。三個地方會讀它：(1) eq. 10.2–10.4：verdict 帶 epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}，a 是上個 epoch 時 K(a) = λ，判定簽章對 λ 的 Ed25519 key 驗；(2) eq. 11.23：guarantee 的 slot t 落在上一個 rotation、而那個 rotation 又屬於上個 epoch 時，指派 M* 要用 (P(|λ′|, η′_3, …), Φ(λ′)) 重算，否則 epoch 第一個 block 裡的合法 guarantee 全會被拒；(3) eq. 10.6–10.7：culprit 與 fault 的 offender key 只要在 κ ∪ λ 的 Ed25519 key 裡且不在 ψ_O 就合法。這也解釋了為什麼 η 要留到 η_3：M* 重算需要上個 epoch 的 entropy。口試追問：「如果不留 λ，最直接壞掉的是什麼？」答：epoch 換檔那一刻，所有指向上個 epoch 的 verdict 與跨 rotation 的 guarantee 都無法驗證。",
 "trap": "λ 不是紀念品，是三個跨 epoch 驗證的金鑰來源。"
},
{
 "id": "d1-entropy-lag-ticket-and-seal",
 "ch": "6", "section": "6.4 entropy; 6.6 tickets; 6.7 seal", "gpRef": "eq. 6.22–6.24, eq. 6.16, eq. 6.30",
 "difficulty": 3, "kind": "rationale", "tags": ["entropy", "tickets", "seal", "design"],
  "stemZh": "ticket 在 epoch e 提交時，ring-VRF 的 context 用 η′_2；到了 epoch e+1 用這張 ticket 封 block 時，seal 的 context 卻用 η′_3。為什麼兩邊用的下標不同？這個設計在保證什麼？",
  "optionsZh": [
   "下標不同、值相同：epoch 換檔時 η 整個往後推一格，e 時的 η′_2 在 e+1 就變成 η′_3。所以 ticket 與 seal 綁的是同一個 entropy 快照，而且它在 ticket 提交開始前就已經定死，沒有人能在比賽中途改它",
   "兩邊故意用不同的值：ticket 用較舊的 η′_2 讓提交者無法預測，seal 用較新的 η′_3 把最新一個 epoch 的隨機性混進去；eq. 6.16 的 Y(H_S) = i_y 靠的是 Bandersnatch VRF 輸出對 context 的線性性質，把兩個不同 context 下的輸出連起來",
   "η′_2 與 η′_3 在 GP 裡是同一個值的兩種寫法：前者出現在 ticket 章節、後者出現在 seal 章節，只是為了讓公式各自對齊所在章節的記號；實作上存一份就好，UpdateEntropy 不需要為它們各留一格",
   "因為 seal 需要比 ticket 晚一個 epoch 的 entropy 才能防止 grinding：作者若在提交 ticket 時就知道 seal 會用哪個值，就能反覆產生 ticket 挑選讓自己拿到想要 slot 的那張；晚一個 epoch 才揭曉，ticket 提交時便無從挑選"
  ],
  "stem": "A ticket submitted during epoch e is proven with ring-VRF context η′_2, yet when that ticket seals a block in epoch e+1 the seal's context uses η′_3. Why do the subscripts differ, and what does the design guarantee?",
 "options": [
  "Different subscript, same value: at the epoch change η is shifted one place, so what was η′_2 during e is η′_3 during e+1. Ticket and seal are therefore bound to one and the same entropy snapshot, and that snapshot was fixed before ticket submission opened, so nobody can move it mid-contest",
  "They are deliberately different values: the ticket uses the older η′_2 so submitters cannot predict it, while the seal mixes in the freshest epoch's randomness through η′_3; eq. 6.16's Y(H_S) = i_y relies on the Bandersnatch VRF output being linear in the context, which relates the two outputs made under different contexts",
  "η′_2 and η′_3 are two spellings of the same state item: one appears in the tickets section and the other in the seal section, purely so that each equation matches the notation of its own chapter; an implementation stores it once and UpdateEntropy need not keep a separate slot for each",
  "The seal needs entropy one epoch newer than the ticket to prevent grinding: if authors already knew at submission time which value the seal would use, they could generate tickets repeatedly and keep the one that lands them on the slot they want; revealing it an epoch later leaves nothing to select against"
 ],
 "answer": 0,
 "optNotes": [
   "正確：eq. 6.23 的輪替 (η′_1, η′_2, η′_3) = (η_0, η_1, η_2) 讓同一個值換了下標；ticket 與 seal 對同一個 context 產生同一個 VRF 輸出，i_y = Y(H_S) 才成立。",
   "VRF 輸出對不同 context 是完全獨立的，沒有線性性質可用；若 context 不同，i_y = Y(H_S) 不可能成立。",
   "它們是 η 這個四元組的兩個不同欄位，同一時刻的值通常不同，只是跨 epoch 後前者的值移到後者。",
   "反了：seal 用「更新」的值反而會讓 ticket id 與 seal 輸出對不上；防 grinding 靠的是 entropy 在比賽開始前定死。"
 ],
 "explanation": "§6.4：η 是四元組，η_0 是累加器，η_1、η_2、η_3 是「最近三個結束的 epoch」結束時的快照；eq. 6.23 在 e′ > e 時做 (η′_1, η′_2, η′_3) = (η_0, η_1, η_2)。ticket 的 ring-VRF context 是 X_T ⌢ η′_2 ⧺ r（eq. 6.30），seal 的 context 是 X_T ⌢ η′_3 ⧺ i_e（eq. 6.16），而 eq. 6.16 要求 i_y = Y(H_S)：seal 的 VRF 輸出必須等於 ticket id。VRF 輸出由 key 與 context 決定，所以兩者必須用同一個 entropy 值，下標差一正好抵掉一次輪替。GP 對 η_2 的說明是「utilized to help ensure future entropy is unbiased… and seed the fallback」，對 η_3 是「used to regenerate this randomness when verifying the seal」。設計上的保證：比賽用的隨機數在 ticket 提交前就已凍結，提交期間的任何 block 都改不了它；而且 fallback 序列 F(η′_2, κ′) 也用同一個值，ticket 模式與 fallback 模式對「誰能出塊」的隨機來源是一致的。",
 "trap": "看到 η′_2 與 η′_3 同時出現，先想「差一次輪替、同一個值」。"
},
{
 "id": "d1-delta-plus-two-antagonistic-factors",
 "ch": "12", "section": "12.2 Execution", "gpRef": "§12.2 prose; eq. 12.17 (Δ+), eq. 12.18 (Δ*)",
 "difficulty": 2, "kind": "rationale", "tags": ["accumulation", "gas", "design"],
  "stemZh": "GP 把 accumulation 拆成兩層：Δ+ 逐 report 順序遞迴，裡面再呼叫 Δ* 把同一個 service 的東西併成一次 PVM 呼叫。§12.2 說這是為了調和「兩個略微對立的因素」。是哪兩個？為什麼一層順序、一層並行可以同時滿足？",
  "optionsZh": [
   "一是 gas：每個 work-item 只有事前的上限，實際用量要跑完才知道，省下來的 gas 才能給後面的 report，這逼出順序執行；二是 PVM 啟動成本：要攤平就得把同一個 service 的 item 塞進同一次呼叫，這逼出非順序的聚合。Δ+ 按 gas 上限切一段順序跑、段內 Δ* 按 service 聚合，各滿足一邊",
   "一是安全：service 之間不能互相影響，一個 service 的 panic 不能連帶讓別的 service 的改動消失，所以必須逐 report 隔離、順序執行，前一份的結果完全落定才做下一份；二是效能：PVM 本身可以並行，同一個 report 內的多個 item 沒有相依，所以平行跑。Δ+ 負責隔離、Δ* 負責平行",
   "一是確定性：所有 node 必須得到同一個 state root，所以外層必須嚴格按 R* 順序執行、不能靠執行時間決定先後；二是延遲：accumulate 每份 report 只有 10⁷ gas，若全部順序跑會拖過 6 秒的 slot，所以內層並行來縮短牆鐘時間。Δ+ 保證前者、Δ* 保證後者",
   "一是 report 的依賴：有 prerequisite 的 report 必須等前面的 report 先做完、結果可見，所以外層順序；二是 transfer：收款方必須在同一輪就處理，否則帳會不平，所以內層把發款方與收款方併進同一次呼叫一起執行。Δ+ 解依賴、Δ* 解轉帳"
  ],
  "stem": "The GP splits accumulation into two layers: Δ+ recurses over reports in order, and inside it Δ* aggregates everything belonging to one service into a single PVM invocation. §12.2 says this reconciles 'two slightly antagonistic factors'. What are they, and why does one sequential layer plus one parallel layer satisfy both?",
 "options": [
  "Gas: each work-item has only an advertised limit; real usage is known only after it runs, and only then can the unspent part fund later reports — that forces sequential execution. PVM setup cost: amortizing it means packing one service's items into one invocation — that forces aggregation. Δ+ takes a gas-bounded prefix in order and Δ* groups it by service, so each layer serves one factor",
  "Safety: services must not affect one another, a panic in one must not wipe out another's changes, so reports are isolated and run one at a time with each fully settled before the next; performance: the PVM itself can run in parallel and the items inside one report are independent, so they are run concurrently. Δ+ provides the isolation and Δ* the parallelism",
  "Determinism: every node must reach the same state root, so the outer layer must follow R* strictly rather than let timing decide the order; latency: accumulate has only 10⁷ gas per report, and running everything sequentially would overrun the six-second slot, so the inner layer parallelizes to cut wall-clock time. Δ+ secures the former and Δ* the latter",
  "Dependencies: a report with prerequisites must wait until the earlier reports have run and their results are visible, hence the outer order; transfers: the recipient must be handled in the same round or the books would not balance, so the inner layer executes sender and recipient together in one invocation. Δ+ resolves dependencies and Δ* resolves transfers"
 ],
 "answer": 0,
 "optNotes": [
   "正是 §12.2 的兩段：「Only after a work-item is accumulated can it be known if it uses less gas… This implies a sequential execution pattern」與「PVM setup cannot be expected to be zero-cost… aggregating work-items associated with the same service… implies a non-sequential execution pattern」。",
   "Δ* 的並行單位是 service，不是 report 內的 item；而 service 之間的隔離靠的是各自只能改自己的 account，不是靠順序。",
   "確定性由規格固定的順序保證，與 Δ+ 為何遞迴無關；GP 沒有拿牆鐘延遲當設計理由。",
   "依賴在 §12.1 的 Q 就已經解掉、排進 R*；transfer 是刻意「延遲」到下一輪，不是同一輪併處理。"
 ],
 "explanation": "§12.2 原文把問題講得很直白：一個 block 的 accumulate gas 有上限，不一定做得完 R*。第一個因素：「while we have a well-known gas-limit for each work-item to be accumulated, accumulation may still result in a lower amount of gas used. Only after a work-item is accumulated can it be known if it uses less gas than the advertised limit. This implies a sequential execution pattern.」第二個因素：「since PVM setup cannot be expected to be zero-cost, we wish to amortize this cost over as many work-items as possible… aggregating work-items associated with the same service into the same PVM invocation. This implies a non-sequential execution pattern.」解法就是兩層：Δ+（eq. 12.17）用 gas 上限的總和挑出最長前綴 i、順序處理，跑完把 g* = g + 新 transfer 的 gas − 實際用量 傳給下一輪遞迴；Δ*（eq. 12.18）在一段裡面把 report 拆開、按 service 分組，每個 service 只呼叫一次 Ψ_A。順序給了「用剩的 gas 能流到後面」，聚合給了「一個 service 一次啟動」。這也是為什麼 operand tuple 要帶 report-level 的欄位：同一個 service 的 digest 來自不同 report，併進一次呼叫後仍得分得出來源。",
 "trap": "面試官問「為什麼不乾脆一個 report 一次呼叫」時，答 PVM 啟動成本那段。"
},
{
 "id": "d1-deferred-transfer-why-deferred",
 "alsoCh": ["B"],
 "ch": "12", "section": "12.2 Execution; 20 Conclusion", "gpRef": "§12.2 prose, eq. 12.14 (𝕏), eq. 12.17, §20 Further Work",
 "difficulty": 2, "kind": "rationale", "tags": ["transfer", "accumulation", "design"],
  "stemZh": "service A 在 accumulate 裡呼叫 transfer 給 service B，B 不會在同一次執行中收到，而是「延遲」到下一輪。為什麼 JAM 不做成同步呼叫？延遲後 B 是怎麼被喚醒、用誰的 gas 處理這筆轉帳？",
  "optionsZh": [
   "因為 Δ* 讓各 service 獨立執行、看不到彼此這一輪的改動，同步呼叫會打破這個獨立性。transfer 只被記進本輪輸出；Δ+ 的下一輪遞迴把它們當輸入，把 B 加進要 accumulate 的集合，B 拿到的 gas 是 transfer 裡宣告的 gas。GP 把 accumulate 內的同步呼叫列為未來可能的改動",
   "因為同步呼叫會讓 gas 計算不確定：A 在呼叫當下無法知道 B 會用掉多少，Δ+ 的前綴選擇就無法事先用上限估算。所以 transfer 被延遲到下一個 block 才處理：B 在下一個 block 的 R* 裡以一份沒有 digest 的特殊 work-report 出現，處理轉帳的 gas 從 B 自己的餘額 a_b 扣除，扣到門檻以下就丟棄",
   "因為 B 的 accumulate code 可能還不在 δ 裡（code hash 有了、preimage 還沒被提供）；延遲一輪讓本 block 的 preimage integration 有機會先把 B 的 code 補上，這輪結束後 B 才在下一輪以 χ_Z（always-accumulate）的名義被 accumulate，gas 用 χ_Z 表裡登記的固定額度",
   "因為 on-chain 不允許任何跨 service 互動，所有 service 之間的資料流都必須走 in-core：transfer 其實是在 refine 階段以 export segment 的形式寫進 D³L，accumulate 只在 A 這邊做扣款記帳；B 要在自己之後的某個 work-package 裡 import 那個 segment、再於自己的 accumulate 入帳才算收到"
  ],
  "stem": "When service A calls transfer to service B inside accumulate, B does not receive it during the same execution; the transfer is 'deferred' to the next round. Why not make it a synchronous call, and after the deferral how does B get woken up and whose gas pays for handling it?",
 "options": [
  "Because Δ* executes services independently and none sees the others' changes from the same round; a synchronous call would break that independence. The transfer is merely recorded in this round's output; the next Δ+ recursion takes those transfers as input, adds B to the set of services to accumulate, and B receives the gas declared inside the transfer. The GP lists synchronous calls inside accumulate as a possible future change",
  "Because a synchronous call would make gas accounting indeterminate: at call time A cannot know how much B will use, so Δ+'s prefix selection could no longer be estimated from limits up front. The transfer is therefore postponed to the next block, where B appears in R* as a special digest-less work-report and the gas for handling it is deducted from B's own balance a_b, dropping the transfer if that would breach the threshold",
  "Because B's accumulate code may not be present in δ yet (code hash set, preimage not yet provided); deferring by one round gives this block's preimage integration a chance to supply it, after which B is accumulated in the next round under the χ_Z always-accumulate privilege, using the fixed gas allowance registered in the χ_Z table",
  "Because no cross-service interaction is allowed on-chain at all and every data flow between services must go in-core: a transfer is really written during refine as an exported segment into the D³L, accumulate only debits A's side, and B must import that segment in a later work-package of its own and credit it in its own accumulate before it counts as received"
 ],
 "answer": 0,
 "optNotes": [
   "對：§12.2「In all but the first invocation of Δ+, we also integrate the effects of any deferred-transfers implied by the previous round」，Δ* 的 service 集合含 {t_d | t ∈ t}，Δ1 的 g 含 Σ t_g；§20 把 synchronous calls 列為 further work。",
   "不是下一個 block，是同一個 block 內 Δ+ 的下一輪遞迴；gas 來自 transfer 帶的 t_g，不是 B 的餘額。",
   "preimage integration 在整個 accumulation 之後才做，不可能在兩輪 Δ+ 之間插入；χ_Z 是 always-accumulate 名單，與收款無關。",
   "segment 是 refine 之間傳資料的管道，transfer 是 accumulate 的 host call，兩者是不同層。"
 ],
 "explanation": "設計核心是 Δ*（eq. 12.18）的並行模型：每個 service 各自拿一份 state-context 執行，只能改自己的 account，結束後再合併。這個模型下，A 執行到一半「叫 B 現在處理一筆轉帳」是做不到的，因為 B 的執行與 A 平行、甚至可能還沒開始。於是 transfer 只是把 𝕏 = (s, d, a, m, g) 記進輸出（eq. 12.14）。§12.2 明說：「In all but the first invocation of Δ+, we also integrate the effects of any deferred-transfers implied by the previous round of accumulation」。機制上：Δ+ 遞迴時把上一輪的 t* 當輸入，n = i + |t| + |f| 的終止條件讓「report 做完但還有 transfer」時仍會再跑一輪；Δ* 的 service 集合 s 含 {t_d | t ∈ t}，所以 B 被加進來；Δ1 算 B 的 gas 時 g 含 Σ_{t_d = s} t_g，也就是 A 在 transfer 裡預付的 gas（transfer host call 會檢查 l ≥ δ[d]_m，不夠就 LOW）。這正是 0.7.1 之後「on_transfer 併進 accumulate」的樣子：B 跑同一支 accumulate，只是這次 i^T 有東西、i^U 是空的。§20 結論列的第一項 further work 就是「Synchronous calls between services in accumulate」，說明目前的延遲是刻意的取捨，不是永久限制。",
 "trap": "「延遲」是延到下一輪 Δ+，不是下一個 block；gas 是發款方預付的。"
},
{
 "id": "d1-checkpoint-collapse-walkthrough",
 "alsoCh": ["12"],
 "ch": "B", "section": "B.4 Accumulate Invocation", "gpRef": "§B.4 prose (regular vs exceptional dimension), collapse function C, Ω_C",
 "difficulty": 2, "kind": "concept", "tags": ["accumulate", "checkpoint", "context"],
  "stemZh": "Ψ_A 的 context 是一對 (x, y)：x 是一般維度，y 是例外維度。某個 service 在 accumulate 裡依序做了：寫 storage → checkpoint → transfer 給別人 → 再寫 storage → panic。這次呼叫最後回傳什麼？y 存在的意義是什麼？",
  "optionsZh": [
   "回傳的是 y，也就是 checkpoint 當下的快照：第一次 storage 寫入保留，checkpoint 之後的 transfer 與第二次寫入全部消失、不會發出去。y 讓 service 自己決定「做到哪裡算數」：沒有 checkpoint 時 y 就是呼叫前的 state，panic 等於整次回滾",
   "回傳的是 x 在 panic 前一刻的狀態：兩次 storage 寫入與那筆 transfer 都保留，只有 panic 之後尚未執行的指令沒有效果，因為 panic 只是提早終止、不是錯誤。y 只用在 out-of-gas 的情況：gas 耗盡時機器無法保證 x 的一致性，才退回 checkpoint 時的 y",
   "回傳的是呼叫前的 state，所有改動全部丟棄，因為任何 exceptional 終止都代表 service 邏輯有錯：checkpoint 只影響 gas 計費的起算點與 ϱ 的退款，不影響 state；y 是 GP 為了讓 collapse function 在形式上總有東西可以取而引入的副本，實作上可以不存",
   "回傳的是 x 與 y 的合併：storage 寫入取 x（較新，兩次都算）、transfer 取 y（較安全，所以那筆 transfer 不發出）、panic 只把 yield 清成 ∅ 並把 provisions 清空；這樣 service 不會因為一個 bug 損失全部進度，也不會發出它來不及確認的轉帳"
  ],
  "stem": "Ψ_A's context is a pair (x, y): x is the regular dimension, y the exceptional one. A service, during accumulate, does in order: write storage → checkpoint → transfer to another service → write storage again → panic. What does the invocation return, and what is y for?",
 "options": [
  "It returns y, the snapshot taken at checkpoint: the first storage write survives, while the transfer and the second write made after the checkpoint vanish and are never sent. y lets a service decide how much of its progress should count; with no checkpoint, y is the pre-invocation state, so a panic is a full rollback",
  "It returns x as it stood the instant before the panic: both storage writes and the transfer survive, and only the instructions not yet executed after the panic have no effect, since a panic is merely an early stop rather than an error. y is used solely for out-of-gas: when gas runs out the machine cannot vouch for x's consistency, so only then does it fall back to the y taken at checkpoint",
  "It returns the pre-invocation state with every change discarded, because any exceptional termination signals a bug in the service logic: checkpoint only resets where gas accounting starts and how ϱ is refunded, never the state; y is a copy the GP introduces so that the collapse function formally always has something to select, and an implementation need not store it",
  "It returns a merge of x and y: storage writes are taken from x (newer, so both count), transfers from y (safer, so that transfer is not sent), and the panic only clears the yield to ∅ and empties the provisions; that way a service never loses all its progress to one bug and never sends a transfer it did not get to confirm"
 ],
 "answer": 0,
 "optNotes": [
   "對：§B.4 說 collapse function C 依終止是 regular 還是 exceptional（out-of-gas 或 panic）選 x 或 y；y 只被 Ω_C（checkpoint）改寫，初始值等於呼叫前的 context。",
   "panic 是 exceptional 終止，結果取 y 不取 x；y 對 panic 與 out-of-gas 一視同仁。",
   "checkpoint 就是把 x 複製進 y，直接改變回傳的 state；沒有 checkpoint 才會退到呼叫前。",
   "GP 沒有任何合併規則：整個結果 (state, transfers, yield, provisions) 一律從同一個維度取。"
 ],
 "explanation": "§B.4 原文：「our invocation context to be a pair of these contexts… one dimension being the regular dimension and generally named x and the other being the exceptional dimension and being named y. The only function which actually alters this second dimension is checkpoint, Ω_C」，以及「we… collapse the result of the invocation to one or the other depending on whether the termination was regular or exceptional (i.e. out-of-gas or panic)」。所以 Ψ_A 的回傳值（poststate、defxfers、yield、provisions）在 regular halt 時全部取自 x，在 panic 或 ∞ 時全部取自 y。走一遍題目的序列：呼叫開始 y = x = 初始 context；第一次 write 改 x；checkpoint 把 x 複製到 y（此時 y 含第一次 write）；transfer 與第二次 write 只改 x；panic → collapse 取 y → 第一次 write 留下、transfer 沒有發出、第二次 write 消失。設計意義：service 作者可以用 checkpoint 把「已經確認要生效的部分」鎖住，後面再做風險較高的事，失敗時不必從零重來；同時 transfer 也跟著 y 走，不會出現「錢轉出去了但帳沒記」的半套狀態。",
 "trap": "panic 與 out-of-gas 對 y 一視同仁；沒 checkpoint 就是整次作廢。"
},
{
 "id": "d1-accumulate-before-audit",
 "alsoCh": ["10", "ARCH"],
 "ch": "12", "section": "17 Auditing; 19 Best Chain; 10 Disputes", "gpRef": "§17 prose, §19 (audited ∈ best-chain conditions), §10",
 "difficulty": 2, "kind": "rationale", "tags": ["audit", "finality", "design"],
  "stemZh": "report 一變 available 就會被 accumulate，但這時 audit 通常還沒做完。也就是說鏈上 state 已經被一份「還沒被驗證過」的結果改掉了。JAM 靠什麼讓這件事安全？如果之後發現那份 report 是壞的，state 怎麼辦？",
  "optionsZh": [
   "靠「先算、後定案」：節點只把已 audited 的 block 當作可以 finalize 與繼續建塊的 best block；若超過 1/3 的 validator 給出負面判定，含該 report 的 block 被 ban-list、它和所有後代都不再被承認。壞 report 的 state 改動不是被撤銷，而是整條分支被放棄，鏈從它之前重新長",
   "靠 accumulate 的原子性：Ψ_A 在執行前會先查該 report 的 audit 狀態，尚未 audited 的 report 只會被寫進 ω 等待、不進 Δ+，直到 audit 的正面判定累積到門檻才真正 accumulate；所以 state 從頭到尾不會含有未經驗證的結果，也就沒有「事後發現是壞的」這種情況",
   "靠 disputes 的回滾指令：verdict 為 bad 時，E_D 除了 verdict 之外還附帶一份由 auditor 簽署的「反向 diff」，記錄該 report 的 accumulate 改了哪些 storage key 與 balance；下一個 block 的 accumulate 會先套用這份 diff，把改動逐項還原，然後才處理新的 report",
   "靠 guarantor 的押金：壞 report 的三位 guarantor 會被 slash，金額依 report 的 gas 用量計算、足以補償受影響的 service；state 本身不動，因為在 JAM 的模型裡 in-core 的錯誤已經由經濟賠償吸收，撤銷 state 反而會破壞後續 block 的 prior state root"
  ],
  "stem": "A report is accumulated as soon as it becomes available, usually before its audit has completed — so the on-chain state has already been changed by a result nobody has verified yet. What makes that safe, and what happens to the state if the report later turns out to be bad?",
 "options": [
  "'Compute first, finalize later': a node treats only an audited block as a best block it may finalize and build on; if more than 1/3 of validators judge negatively, the block containing the report is ban-listed and it and all its descendants are disregarded. The bad state changes are not undone in place; the whole branch is abandoned and the chain regrows from before it",
  "Atomicity in accumulate: before running, Ψ_A looks up the report's audit status, and an unaudited report is only parked in ω and kept out of Δ+ until enough positive judgments have accrued on-chain; so the state never contains an unverified result, and there is no such thing as discovering afterwards that a report was bad",
  "A rollback instruction in disputes: when the verdict is bad, E_D carries, besides the verdict, an auditor-signed reverse diff listing which storage keys and balances the report's accumulate touched; the next block's accumulate first applies that diff, restoring every change item by item, and only then processes new reports",
  "The guarantors' stake: the three guarantors of a bad report are slashed by an amount scaled to the report's gas usage, enough to compensate the affected services; the state itself is left alone because in JAM's model an in-core error is absorbed economically, and undoing state would break the prior state roots of later blocks"
 ],
 "answer": 0,
 "optNotes": [
   "對：§17「One prerequisite of a node finalizing a block is for it to view the block as audited」與「the block which includes the work-report is ban-listed. It and all its descendants are disregarded and may not be built on」；§19 把 audited 列為 best block 條件。",
   "Ψ_A 與 ω 都不知道 audit 的存在；audit 是 off-chain 的，state transition 只看 availability。",
   "GP 沒有反向 diff；state 是一整棵 Merkle trie，撤銷靠的是換分支。",
   "slash 存在但不是保護 state 的機制；壞結果若留在 canonical chain 上，賠償也救不回被污染的 state。"
 ],
 "explanation": "這題考的是 JAM 分層的本質：state transition（§4–13）只認 availability，不認 audit；audit（§17）與 best-chain 選擇（§19）是 off-chain 的誠實策略。§17 原文：「Once all of any given block's newly available work-reports are audited, then we consider the block to be audited. One prerequisite of a node finalizing a block is for it to view the block as audited.」§19 的 best block 條件之一就是「Is considered audited」。負面判定的後果也在 §17：「If greater than 1/3 of the validators issue negative judgments, then the block which includes the work-report is ban-listed. It and all its descendants are disregarded and may not be built on.」所以「未驗證的結果改了 state」是被允許的，代價由兩件事兜住：GRANDPA 不會 finalize 未 audited 的 block（所以壞結果不會變成不可逆），而一旦判定為壞，整條分支被放棄、由 disputes extrinsic 把 verdict 與 offender 記上鏈。state 從來不做「逐項撤銷」，撤銷的單位是 block。這也是 JAM 敢把 accumulate 放在 audit 之前的原因：audit 需要重跑 refine，太慢，若等它做完才 accumulate，pipeline 的延遲會從幾個 slot 變成幾十個。",
 "trap": "撤銷的單位是 block（換分支），不是 report；finality 才是真正的閘門。"
},
{
 "id": "d1-three-thirty-341",
 "alsoCh": ["11"],
 "ch": "ARCH", "section": "20 Discussion – Technical Characteristics", "gpRef": "§20.1 prose, §11.3 (three validators per core), eq. 6.8",
 "difficulty": 2, "kind": "concept", "tags": ["cores", "audits", "throughput", "design"],
  "stemZh": "GP 的 Discussion 章給了一組數字：1,023 個 validator、每個 core 3 位、每位 validator 每個 timeslot 平均 10 次 audit。這三個數字怎麼推出「341 個 core」與「每份 report 30 次 audit」？當 validator set 縮小時，哪個數字跟著變？",
  "optionsZh": [
   "core 數 = validator 數 ÷ 每 core 人數 = 1023 ÷ 3 = 341；每份 report 的 audit 數 = 每人每 slot 的 audit 數 × validator 數 ÷ report 數 = 10 × 1023 ÷ 341 = 30。set 縮小時啟用的 core 數跟著變成 |κ| ÷ 3，每份 report 的 audit 數維持 30 不變",
   "core 數是協定常數 C = 341，寫死在 §I 裡、與 validator 數無關；30 = 10 × 3 是每份 report 由三位 guarantor 各自去找 10 個人來 audit 的結果。set 縮小時 core 數不變、每個 core 仍有 3 位 guarantor，只是每份 report 的 audit 數等比例降為 10 × |κ| ÷ 1023",
   "341 = 1023 ÷ 3 是因為每份 report 要三個獨立的 audit 判定才算 audited，1023 人一次最多能同時 audit 341 份；30 = 3 × 10 是三位 guarantor 各 10 個 tranche 的總數。set 縮小時每份 report 需要的 tranche 數減少，core 數維持 341 不動",
   "341 與 30 都是從 0.5 GbE 網路頻寬與 16 核 CPU 的硬體假設反推出來的上限，跟 validator 數沒有算術關係。set 縮小時兩者都不變，只是每個 core 的 guarantor 從 3 人降為 1 人，以維持 341 個 core 全部啟用"
  ],
  "stem": "The Discussion chapter gives three numbers: 1,023 validators, three validators per core, and a mean of ten audits per validator per timeslot. How do those yield '341 cores' and '30 audits per work-report', and which figure changes when the validator set shrinks?",
 "options": [
  "Cores = validators ÷ validators per core = 1023 ÷ 3 = 341; audits per report = audits per validator per slot × validators ÷ reports = 10 × 1023 ÷ 341 = 30. When the set shrinks the number of active cores becomes |κ| ÷ 3, while the 30 audits per report stay as they are",
  "The core count is the protocol constant C = 341, fixed in §I independently of the validator count; 30 = 10 × 3 because each of a report's three guarantors recruits ten auditors of its own. When the set shrinks the core count is unchanged and every core keeps three guarantors, only the audits per report scale down to 10 × |κ| ÷ 1023",
  "341 = 1023 ÷ 3 because a report needs three independent audit judgments to count as audited, so 1023 validators can audit at most 341 reports at once; 30 = 3 × 10 is three guarantors times ten tranches each. When the set shrinks the tranches needed per report drop while the core count stays at 341",
  "Both 341 and 30 are hardware ceilings derived from the 0.5 GbE link and the 16-core CPU assumption and bear no arithmetic relation to the validator count. When the set shrinks neither changes; instead the guarantors per core drop from three to one so that all 341 cores remain active"
 ],
 "answer": 0,
 "optNotes": [
   "對：§20.1「with our stated target of 1,023 validators and three validators per core, along with requiring a mean of ten audits per validator per timeslot, and thus 30 audits per work-report, JAM is capable of… 341 work-packages per timeslot」；0.8.0 啟用 core 數 = |κ|/3。",
   "C = 341 是「最大」core 數，啟用數隨 |κ|/3 變；30 是總 audit 量 ÷ report 數，與 guarantor 招人無關。",
   "三位是 guarantor 不是 auditor；audited 的條件是 tranche 內所有應 audit 者都給正面判定，不是固定三次。",
   "0.5 GbE 是硬體假設，不是這兩個數字的來源；每 core 永遠 3 位 guarantor，變的是 core 數。"
 ],
 "explanation": "§20.1 原文一句話把三個數綁在一起：「In total, with our stated target of 1,023 validators and three validators per core, along with requiring a mean of ten audits per validator per timeslot, and thus 30 audits per work-report, JAM is capable of trustlessly processing and integrating 341 work-packages per timeslot.」算法：每個 core 需要 3 位 guarantor，1023 人剛好分成 341 組，所以 C = 341 不是任意常數，是 1023 = 3 × 341 推出來的；audit 是「每人每 slot 平均 10 份」，全網每 slot 共 10 × 1023 次 audit，分攤到每 slot 最多 341 份 report，每份約 30 次。0.8.0 把 validator set 改成可變（eq. 6.8：3 的倍數、6 到 1023）之後，「每 core 3 人」不變，所以啟用的 core 數變成 |κ|/3：tiny config 6 人就是 2 個 core；而 eq. 11.28 也用 |κ′|/3 當 core index 的上界。每份 report 30 次 audit 這個目標值則來自 audit 的抽樣參數（§17 的 tranche 與 F = 2），不隨 set 大小縮放。口試若問「為什麼是 341」，答「1023 除以 3」就夠。",
 "trap": "341 是算出來的，不是選出來的：1023 ÷ 3。"
},
{
 "id": "d1-bounded-asynchrony-concrete",
 "alsoCh": ["11", "12"],
 "ch": "ARCH", "section": "1.3 Scaling under Size-Coherency Antagonism; 11; 12", "gpRef": "§1.3 prose, eq. 11.18 (U), ω ∈ ⟦…⟧_E, eq. 11.38 (L)",
 "difficulty": 3, "kind": "rationale", "tags": ["pipeline", "asynchrony", "design"],
  "stemZh": "§1.3 說 JAM「並不避免非同步，而是把它限制在 pipeline 的長度之內」。這句話落到協定裡是哪幾條具體的界限？一份工作從 in-core 到影響 state，最多能拖多久？",
  "optionsZh": [
   "三道界限：guarantee 進 ρ 後 U = 5 個 slot 內沒變 available 就被清掉；有 dependency 的 report 在 ω 裡最多等一個 epoch，逾期即丟；refine 讀的 lookup-anchor 最多 L = 14,400 個 slot 舊。所以一份 report 要嘛在幾個 slot 內 accumulate、要嘛被丟，沒有「掛著不知何時生效」的中間態",
   "只有一道界限：GRANDPA 的 finality。任何 report 在它所在的 block 被 finalize 前都可以無限期等待，ρ 不會清它、ω 也不會丟它；finalize 之後的第一個 block 才把它 accumulate。所以「pipeline 長度」就是 finality 延遲，正常情況約兩到三個 slot，網路分割時可以無限長",
   "界限是 epoch：所有在 epoch e 保證的 report 必須在 epoch e 結束前 accumulate，否則 epoch 換檔時 ρ 與 ω 一起被清空、整個 epoch 沒做完的 report 作廢重來，builder 必須重新提交。U 與 L 只是 GP 給實作者的建議值，不是 state transition 的規格",
   "沒有硬性界限：非同步由 audit 的 tranche 機制自然收斂，report 會一直留在 ρ 直到它被 audit 完成、拿到足夠的正面判定才 accumulate；「pipeline 長度」指的是 audit 收斂所需的期望輪數，F = 2 的設定下大約三到四個 tranche、也就是 24 到 32 秒"
  ],
  "stem": "§1.3 says JAM does not avoid asynchrony but 'bounds it to the length of the pipeline'. Which concrete limits in the protocol realise that sentence, and how long can one piece of work take from in-core execution to affecting the state?",
 "options": [
  "Three limits: a guarantee sitting in ρ is cleared unless its report becomes available within U = 5 slots; a report with dependencies waits in ω at most one epoch and is then dropped; the lookup-anchor refine reads may be at most L = 14,400 slots old. So a report is either accumulated within a handful of slots or discarded; there is no 'pending indefinitely' state",
  "A single limit: GRANDPA finality. A report may wait indefinitely until the block carrying it is finalized — ρ never clears it and ω never drops it — and the first block after finalization accumulates it. So the pipeline's length is the finality delay: a couple of slots normally, unbounded under a network partition",
  "The limit is the epoch: every report guaranteed in epoch e must be accumulated before epoch e ends, otherwise ρ and ω are both emptied at the epoch change, the epoch's unfinished reports are voided and builders must resubmit them. U and L are only implementation hints the GP offers, not part of the state-transition rules",
  "There is no hard limit: asynchrony converges naturally through the audit tranches, a report stays in ρ until its audit completes and enough positive judgments arrive, and only then is it accumulated; 'pipeline length' refers to the expected number of audit rounds, about three to four tranches or 24 to 32 seconds with F = 2"
 ],
 "answer": 0,
 "optNotes": [
   "對：eq. 11.18 的 H_T ≥ t + U 清 ρ‡；ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E 只有 E 格、逾期出局；eq. 11.38 要求 lookup-anchor 時間 ≥ H_T − L。",
   "accumulate 與 finality 無關；state transition 只看 availability，finality 是 off-chain 決定「哪條分支不可逆」。",
   "沒有「整個 epoch 作廢」的規則；U 與 L 都是 §I 的協定常數，寫在 eq. 11.18 與 11.38 裡。",
   "ρ 的清空條件是 available、timeout、set 大小改變，與 audit 進度無關；audit 是 off-chain。"
 ],
 "explanation": "§1.3 原文：「Asynchrony is not avoided, but we bound it to the length of the pipeline」。這句的具體實現分布在三章：(1) eq. 11.18：ρ‡[c] = ∅ 的條件之一是 H_T ≥ t + U，U = 5，也就是 guarantee 上鏈後 5 個 slot 內若 assurance 沒過 2/3，這個 core 就被清空、report 作廢，必須重新 guarantee；(2) §12.1：ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E 是一個 E 格的環，report 進 ω 之後若依賴一直沒滿足，一個 epoch 後那一格被覆寫，report 消失；(3) eq. 11.38：refinement context 的 lookup-anchor 時間必須 ≥ H_T − L，L = 14,400 slot（24 小時），所以 refine 看到的「舊 state」有年齡上限，audit 重跑時也才找得到同樣的 preimage（D = L + 4,800 就是為此留的安全邊際）。把三者合起來：正常路徑是 guarantee → 幾個 slot 內 available → 同一個 block accumulate；異常路徑是 5 個 slot 內出局或一個 epoch 內出局。這就是「mostly coherent」的量化版本：in-core 與 on-chain 的落差是有上限的、可計算的，不像跨鏈訊息那樣沒有期限。",
 "trap": "答三個常數：U = 5 slot、ω 一個 epoch、L = 24 小時。"
},
{
 "id": "d1-mostly-coherent-lookup-anchor",
 "alsoCh": ["14", "11"],
 "ch": "ARCH", "section": "1.3; 4.9.1; 11.2", "gpRef": "§1.3, §4.9.1 prose, eq. 11.4 (context), eq. 11.38, §B.2 (historical_lookup)",
 "difficulty": 2, "kind": "rationale", "tags": ["coherency", "lookup-anchor", "design"],
  "stemZh": "GP 把 in-core 稱為「mostly coherent」、on-chain 稱為「fully coherent」。落到 refine 身上，「mostly」具體是什麼意思？refine 到底能看到多少 chain state，透過什麼機制？",
  "optionsZh": [
   "refine 看不到當下的 state，只能透過 lookup-anchor 看一個「最近、已 finalize」的 block 當時的 preimage：refinement context 指定 anchor，historical_lookup 對著那個時點查。所以 refine 看到的是一份有年齡上限的舊快照，有連貫性但落後鏈頭一段有界的距離；accumulate 則看得到精確的當下 state",
   "mostly 指的是 refine 只能讀不能寫：它透過 read 與 lookup 兩個 host call 看到跟 accumulate 一樣新的 state，包括其他 service 的 storage 與餘額，只是任何寫入在 report 產生時都會被丟棄、不進 state；fully 指 accumulate 可讀可寫，而且寫入會被 Merklize 進 state root",
   "mostly 指的是機率：refine 的結果只有在超過 2/3 的 validator 背書後才被視為與鏈連貫，在那之前它只是三位 guarantor 的主張，剩下的 1/3 機率代表它可能永遠不會被接受；on-chain 的 accumulate 因為每個 node 都重算一遍，所以連貫性是 100%、沒有機率成分",
   "mostly 指的是 refine 只看得到自己 service 的 state、看不到其他 service：它用 fetch 讀取自己 storage 在 anchor 時點的快照，所以對自己是連貫的、對整條鏈不是；fully 指 accumulate 透過 read 與 info 能讀所有 service 的 state，對整條鏈都連貫"
  ],
  "stem": "The GP calls in-core 'mostly coherent' and on-chain 'fully coherent'. Applied to refine, what does 'mostly' concretely mean — how much chain state can refine see, and through what mechanism?",
 "options": [
  "Refine cannot see the current state; it can only see, through the lookup-anchor, the preimages as they stood at a recent finalized block: the refinement context names the anchor and historical_lookup queries that point in time. So refine sees an age-bounded old snapshot — coherent, but lagging the head by a bounded distance — whereas accumulate sees the exact current state",
  "'Mostly' means refine may read but not write: through the read and lookup host calls it sees state as fresh as accumulate does, including other services' storage and balances, but any write is discarded when the report is produced and never reaches the state; 'fully' means accumulate may both read and write, and its writes are Merklized into the state root",
  "'Mostly' is probabilistic: a refine result counts as coherent with the chain only once more than 2/3 of validators have assured it, before which it is merely three guarantors' claim, and the remaining 1/3 represents the chance it is never accepted; on-chain accumulate is 100% coherent with no probabilistic element because every node re-executes it",
  "'Mostly' means refine sees only its own service's state and not other services': through fetch it reads a snapshot of its own storage as of the anchor, so it is coherent with itself but not with the whole chain; 'fully' means accumulate can read every service's state through read and info and is coherent with the entire chain"
 ],
 "answer": 0,
 "optNotes": [
   "對：§B.2「It has no general access to the state of the JAM chain, with the slight exception being the ability to make a historical lookup」；§4.9.1 說 lookup-anchor「must be in the finalized chain and reasonably recent」。",
   "read 與 lookup 是 Ψ_A 的 host call，Ψ_R 沒有；refine 也沒有「寫了再丟」這回事。",
   "2/3 是 availability 門檻，管的是資料拿不拿得回來，跟 coherency 的定義無關。",
   "refine 連自己 service 的 storage 都看不到；fetch 讀的是 work-package 與常數，不是 state。"
 ],
 "explanation": "§1.3 的措辭：「pipelines a highly scalable, mostly coherent element to a synchronous, fully coherent element」。§4.9.1 給了 in-core 的設計原則：「Execution done in-core is therefore designed to be as stateless as possible. The requirements for doing it include only the refinement code of the service, the code of the authorizer and any preimage lookups it carried out during its execution.」以及「a specific block known as the lookup-anchor is identified. Correct behavior requires that this must be in the finalized chain and reasonably recent」。§B.2 對 Ψ_R 的描述更直接：「It has no general access to the state of the JAM chain, with the slight exception being the ability to make a historical lookup.」所以 refine 唯一的 state 視窗是 Ω_H（historical_lookup），對著 refinement context（eq. 11.4）裡的 lookup-anchor 查 preimage，且 eq. 11.38 要求那個 anchor 不超過 L 個 slot 舊。「mostly coherent」就是：in-core 的運算跟鏈是有因果關係的（它看得到不久前的鏈上事實），但這個關係有時間差、且時間差有上限。accumulate 相反，它在 Δ* 裡拿到的是這個 block 當下的 δ、χ、ι、φ，所以是 fully coherent。這也是為什麼 refine 要 stateless：任何 auditor 在幾個 epoch 後重跑，看到的 lookup-anchor 快照必須一模一樣，否則 audit 無法判定對錯。",
 "trap": "refine 的 state 視窗只有一扇：historical_lookup 對 lookup-anchor。"
},
{
 "id": "d1-block-vs-derived-state",
 "alsoCh": ["12"],
 "ch": "5", "section": "4.1; 5.1 header; 12", "gpRef": "eq. 4.1 (σ′ = Υ(σ, B)), eq. 5.1 (H_R), §12",
 "difficulty": 2, "kind": "concept", "tags": ["state-root", "consensus", "design"],
  "stemZh": "accumulate 的結果（δ‡、θ′ 等）並不會被放進 block。既然 block 裡沒有，全網怎麼對「這份 report accumulate 之後 state 長什麼樣」達成共識？一個 accumulate 算錯的 node 會在哪一步被抓到？",
  "optionsZh": [
   "block 只帶 extrinsic，state 是每個 node 各自從 σ′ = Υ(σ, B) 算出來的。共識來自下一個 block 的 header：H_R 必須等於父 block 的 posterior state root。算錯的 node 算出的 root 跟 H_R 對不上，就會判定下一個 block 無效、接不上鏈，等於自己被分叉掉",
   "block 的 header 帶 posterior state root H_R，所以 block 本身就承諾了自己這一輪 accumulate 的結果；node 匯入時先跑完 Υ 算出 σ′、再把 M_σ(σ′) 跟 H_R 比對，不合就拒絕這個 block。所以算錯的 node 在同一個 block 就會被抓到，不必等下一個 block 出現",
   "accumulate 的結果以 θ′（每個 service 的 yield hash）的形式放進 block 的 E_G 尾端，由出塊者與 2/3 的 validator 對它簽名；共識來自這些簽名，算錯的 node 因為算出不同的 θ′ 而簽出不一致的內容，會被記進 offenders marker H_O 並在下個 epoch 被踢出",
   "共識靠 BEEFY：每個 block 的 accumulation output 被所有 validator 用 BLS 聚合簽名，聚合簽名放在下一個 block 的 H_O marker 裡，任何 node 都能用 γ_Z 驗證；算錯的 node 因為 output 不同、無法參與正確的聚合簽名，它的份額會被排除在 2/3 門檻之外"
  ],
  "stem": "The results of accumulate (δ‡, θ′ and so on) are never placed in the block. Since they are not in the block, how does the whole network reach consensus on what the state looks like after a report is accumulated, and at which step is a node that computed accumulate wrongly caught?",
 "options": [
  "A block carries only the extrinsic; the state is computed by every node itself as σ′ = Υ(σ, B). Consensus comes from the next block's header: its H_R must equal the parent's posterior state root. A node that computed wrongly finds its own root disagreeing with H_R, rejects the next block as invalid and cannot follow the chain — it has effectively forked itself off",
  "The block's header carries the posterior state root H_R, so the block itself commits to the result of its own round of accumulate; on import a node first runs Υ to obtain σ′, then compares M_σ(σ′) with H_R and rejects the block on mismatch. So a wrong node is caught within the same block, without waiting for the next block to appear",
  "The accumulate results are placed in the block as θ′ (each service's yield hash) appended to E_G and signed by the author and 2/3 of validators; consensus comes from those signatures, and a node that computed a different θ′ signs inconsistent content, is recorded in the offenders marker H_O and is ejected at the next epoch",
  "Consensus is via BEEFY: every block's accumulation output is BLS-aggregate-signed by all validators, the aggregate goes into the next block's H_O marker and anyone can verify it against γ_Z; a node whose output differs cannot join the correct aggregate signature and its share is excluded from the 2/3 threshold"
 ],
 "answer": 0,
 "optNotes": [
   "對：eq. 5.1 的 H_R 是 prior state root（父 block 的 posterior）；eq. 4.1 說 state 是由 Υ 導出的；block 本體只有 E。",
   "H_R 是 prior 不是 posterior，這正是 ch05-prior-state-root 那題的重點；同一個 block 抓不到，要等下一個。",
   "θ′ 是 state 項目不是 extrinsic；E_G 裝的是 guarantee；沒有對 θ′ 簽名的機制。",
   "BEEFY 簽的是 β_B 的 super-peak、目的是給 bridge 用，且簽名不進 header；H_O 是 offenders marker。"
 ],
 "explanation": "把三個層次分開：(1) block B = (H, E)，E 只有五個 extrinsic，沒有任何 accumulate 的輸出；(2) state σ 是每個 node 本地持有的，eq. 4.1 σ′ = Υ(σ, B) 說它是「算出來的」，不是「收到的」；(3) 共識的載體是 header 的 H_R。eq. 5.1 定義 H_R 為 prior state root，也就是父 block 執行完之後的 root。所以 block N 的 accumulate 結果，是在 block N+1 的 header 被承諾的：所有 node 匯入 N+1 時檢查 H_R = M_σ(σ_N′)，自己算的 σ_N′ 若不同，這個檢查就失敗，N+1 對它而言是無效 block，它從此接不上主鏈。這就是「算錯的 node 被抓到」的方式：不是被別人指控，而是它自己再也無法驗證後續 block。這個設計（prior root 而非 posterior）讓 block 作者不必等自己的 state Merklize 完就能發 block（§5、§20 的 pipelining 理由），代價是錯誤晚一個 block 才顯現。跟 report 的「上鏈」對照：report 在 guarantee 時就進了 block（E_G），但它的效果要到下一個 header 才被共識承諾。",
 "trap": "block 裡沒有結果，只有輸入；結果的共識靠「下一個」header 的 H_R。"
},
{
 "id": "d1-core-unopinionated-what-binds",
 "alsoCh": ["8"],
 "ch": "ARCH", "section": "2.1 Polkadot; 4.9; 8 Authorization", "gpRef": "§2.1 prose, §8 prose, eq. 8.2, §B (assign)",
 "difficulty": 2, "kind": "rationale", "tags": ["cores", "authorization", "polkadot", "design"],
  "stemZh": "Polkadot 1.0 裡一個 core 綁死一條 parachain：core 永遠只做「驗證那條鏈的 block」。JAM 說 core 是無定見的（un-opinionated）。那在 JAM 裡，「這個 core 現在接受什麼工作」是由哪些東西決定的？拍賣得到的 slot 被什麼取代？",
  "optionsZh": [
   "由每個 core 的 authorizer pool α[c] 決定：只有 authorizer 在 pool 裡的 work-package 才會被這個 core 的 guarantor 接受，package 裡指名的 service 決定實際跑哪支 refine。pool 由 queue φ[c] 補充，φ[c] 只能被該 core 的 assigner 透過 assign 改寫。slot 拍賣被 coretime 取代：買到 coretime 的人透過 assigner 把自己的 authorizer 排進 φ[c]",
   "由 service 的註冊決定：service 用 new 建立時，除了 code hash 與初始餘額之外還要指定它要使用的 core 清單，registrar 會把這些 core 的 ρ 標記為屬於該 service；之後這些 core 的 guarantor 只接受該 service 的 package，其他 service 的 package 一律以 core_unauthorized 拒絕。拍賣被 new 一次性的建立費與押金取代",
   "由 guarantor 自行決定：每個 rotation 開始時，被指派到同一個 core 的三位 guarantor 互相溝通、投票選出這 R = 10 個 slot 要優先服務哪個 service 的 package，票數寫進 guarantee 的 credential 裡讓鏈上知道；拍賣被 validator 之間的市場機制取代，service 直接付費給 guarantor 換取被優先處理",
   "由 refinement context 決定：builder 在組 package 時於 context 裡宣告要用的 core index，guarantor 只處理宣告了自己 core 的 package，on-chain 則只檢查同一個 block 內沒有兩份 report 用同一個 core、以及 core index 小於 |κ′|/3；拍賣被先到先得取代，誰的 package 先送到 guarantor 手上誰就用這個 slot"
  ],
  "stem": "In Polkadot 1.0 a core is bound to one parachain: it only ever validates that chain's blocks. The GP says JAM cores are un-opinionated. So in JAM, what decides 'which work this core accepts right now', and what replaces the auctioned slot?",
 "options": [
  "Each core's authorizer pool α[c]: a work-package is accepted by the core's guarantors only if its authorizer is in the pool, and the service named inside the package decides which refine actually runs. The pool is refilled from the queue φ[c], and φ[c] can be rewritten only by that core's assigner via assign. Auctions are replaced by coretime: whoever buys coretime has the assigner schedule their authorizer into φ[c]",
  "The service's registration: when a service is created with new it supplies, besides its code hash and initial balance, the list of cores it will use, and the registrar marks those cores' ρ entries as belonging to it; from then on those cores' guarantors accept only that service's packages and reject all others with core_unauthorized. The auction is replaced by the one-off creation fee and deposit paid to new",
  "The guarantors themselves: at the start of each rotation the three guarantors assigned to a core confer and vote on which service's packages their R = 10 slots will serve first, recording the vote in the guarantee's credential so the chain can see it; the auction is replaced by a market among validators in which a service pays guarantors directly for priority",
  "The refinement context: the builder declares the intended core index in the package's context, guarantors only process packages that name their core, and on-chain logic merely checks that no two reports in one block use the same core and that the index is below |κ′|/3; the auction is replaced by first-come-first-served — whoever's package reaches the guarantors first gets the slot"
 ],
 "answer": 0,
 "optNotes": [
   "對：§8「the set of authorizers allowable for a particular core c as the authorizer pool α[c]」、「φ may be altered only through an exogenous call made from the accumulate logic of an appropriately privileged service」；§4.9 說 coretime 取代 Ethereum 的 gas 購買與 Polkadot 的 slot。",
   "new 只建立 account，不綁 core；ρ 裝的是 guarantee 不是歸屬標記；service 與 core 之間沒有靜態關係。",
   "guarantor 只檢查 α[c]，沒有投票權；指派是被 entropy 洗牌決定的，credential 裡只有簽章。",
   "core index 是 report 的欄位，但「能不能用這個 core」由 α[c] 決定，不是先到先得。"
 ],
 "explanation": "§2.1 對 Polkadot 的批評是「clients able to utilize its service [are] those who… raise a sufficient deposit to win an auction for a long-term slot」。JAM 把「誰能用 core」拆成兩層。第一層是 §8 的 authorization system：「a means of disentangling the intention of usage for some coretime from the specification and submission of a particular workload」。每個 core 有 pool α[c]（eq. 8.1，最多 O = 8 個 authorizer hash）與 queue φ[c]（Q = 80 格），eq. 8.2 每個 block 從 φ[c][H_T mod Q] 移一個進 pool、並移掉這個 block 用掉的那個。guarantor 只做「authorizer 在 α[c] 裡」的 package，而 authorizer 的 is-authorized 程式在 in-core 執行、決定放不放行（§8：「happens entirely in-core」）。第二層是誰能寫 φ[c]：§8 註明「may be altered only through an exogenous call made from the accumulate logic of an appropriately privileged service」，也就是 χ_A[c] 指定的 assigner service 呼叫 assign。coretime 的買賣本身 GP 留白（§4.9：「Its procurement is out of scope」），預期由一個 system service 處理，買到的人把 authorizer 交給 assigner 排進 φ。所以 core 對「跑什麼」完全沒有意見：它只認 pool 裡的 authorizer，package 裡的 service index 才決定跑哪支 refine。parachain 在這個框架下只是「authorizer 放行 parachain block、service 是 parachains service」的特例。",
 "trap": "兩把鑰匙：α[c] 決定「哪些 package 能上」，package 的 service 決定「跑什麼」。"
}
]
