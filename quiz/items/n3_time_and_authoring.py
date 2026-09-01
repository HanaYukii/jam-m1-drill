# -*- coding: utf-8 -*-
"""基礎套題 N3：時間與出塊。只考主幹。"""

ITEMS = [
 {
  "id": "n3-slots-and-epochs",
  "ch": "N3", "section": "§4.8 Epochs and Slots", "gpRef": "§4",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "time"],
  "stem": "How is time organised in JAM?",
  "stemZh": "JAM 的時間是怎麼組織的？",
  "options": [
   "Into six-second timeslots, grouped into epochs of 600 slots, with at most one block per slot and a single validator entitled to author it",
   "Into blocks of variable duration, where a slot begins when the previous block is seen and ends when the next author has collected enough work to fill one",
   "Into six-second timeslots grouped into epochs, with several blocks allowed per slot so long as they build on different parents and are later merged",
   "Into rounds rather than slots, where a round ends once two thirds of validators have signed the same block, so its length depends on network latency"
  ],
  "optionsZh": [
   "切成 6 秒一個時槽，600 個時槽組成一個 epoch；每個時槽至多一個區塊，而且只有一位 validator 有資格出塊",
   "切成長度不定的區塊：一個時槽從看到前一個區塊開始，到下一位出塊者蒐集到足夠工作填滿一塊為止",
   "切成 6 秒一個時槽並組成 epoch，但每個時槽允許多個區塊，只要它們建在不同的父區塊上、之後再合併",
   "切成回合而非時槽：一個回合在三分之二的 validator 簽署同一個區塊後結束，長度因此取決於網路延遲"
  ],
  "answer": 0,
  "explanation": "**P = 6 秒是一個時槽，E = 600 個時槽是一個 epoch**（所以一個 epoch 是一小時）。時槽是絕對時間的格子，從 JAM Common Era（2025-01-01 1200 UTC）起算——不是「上一塊之後六秒」，而是掛在牆鐘上的固定刻度，所以每個節點都能獨立算出現在是第幾槽。每個時槽至多一個合法區塊，出塊權由 Safrole 事先指派給唯一一位 validator。這也是 JAM「幾乎不分叉」的來源：同一格只有一個人有資格，分叉只會因為網路問題或 fallback 才發生。",
  "optNotes": [
   "6 秒一槽、600 槽一 epoch、每槽一人有資格——三個數字撐起整個出塊模型。",
   "時槽掛在牆鐘上而非相對於前一塊，所以每個節點都算得出現在是第幾槽。",
   "同一個時槽只有一位有出塊資格，不存在「允許多塊之後再合併」這回事。",
   "出塊不等待簽署門檻；那是 finality（Grandpa）的事，與出塊節奏無關。"
  ],
  "trap": "P = 6 秒、E = 600 槽；時槽是絕對刻度，不是相對於前一塊。"
 },
 {
  "id": "n3-what-safrole-does",
  "ch": "N3", "section": "§6 Safrole", "gpRef": "§6",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "safrole"],
  "stem": "What is Safrole for, in one sentence?",
  "stemZh": "一句話說，Safrole 是做什麼用的？",
  "options": [
   "It decides, ahead of time and anonymously, which single validator may author each slot of the coming epoch",
   "It finalizes blocks by collecting supermajority signatures, so that a block past a certain depth can never be reverted",
   "It assigns validators to cores so each core has three guarantors, rotating that assignment every few slots",
   "It spreads each work-package's erasure-coded shards across validators so a report's data stays recoverable"
  ],
  "optionsZh": [
   "它事先且匿名地決定，接下來那個 epoch 的每一個時槽由哪一位 validator 出塊",
   "它藉由蒐集超級多數的簽章來為區塊定案，使超過一定深度的區塊永遠不會被回滾",
   "它把 validator 指派到各個 core，讓每個 core 有三名 guarantor，並每隔幾槽輪換一次以限制串通",
   "它把每份 work-package 的 erasure-coded 碎片分發給 validator，使報告背後的資料保持可重建"
  ],
  "answer": 0,
  "explanation": "Safrole 只做一件事：**產生「這個 epoch 每一槽由誰出塊」的名單**，而且要在事前決定、同時保持匿名。事前決定讓每槽只有一位合法出塊者（因此幾乎不分叉）；匿名則讓別人無法預先知道下一槽是誰，也就無法針對性攻擊他。其他三個選項都是 JAM 的重要機制但屬於別章：finality 是 Grandpa（§19）、guarantor 對 core 的指派在 §11、erasure coding 的分發在 §11 與附錄 H。",
  "optNotes": [
   "事先決定＋匿名，正是 Safrole 的兩個要求，也是它比一般 VRF 抽籤複雜的原因。",
   "finality 是 Grandpa 的工作，Safrole 只管出塊資格。",
   "guarantor 對 core 的指派用的是 entropy 洗牌，不經過 Safrole 的票券機制。",
   "shard 的分發屬於 availability，與出塊資格無關。"
  ],
  "trap": "Safrole = 出塊排班表；finality、core 指派、資料分發都是別的機制。"
 },
 {
  "id": "n3-why-anonymous",
  "ch": "N3", "section": "§6 Safrole", "gpRef": "§6",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "safrole", "security"],
  "stem": "Safrole goes to considerable trouble to keep the identity of a future slot's author secret. What would go wrong if the schedule were public?",
  "stemZh": "Safrole 花了不少力氣讓未來時槽的出塊者身分保密。如果出塊表是公開的，會出什麼問題？",
  "options": [
   "Anyone could see who is about to author and attack or bribe exactly that validator, so a cheap targeted action could stop blocks that a network-wide attack could not",
   "Anyone could compute the same schedule and author in someone else's slot, because knowing who is next is what proves entitlement to seal a block",
   "Validators could see their own future slots and withhold their tickets until the last moment, which would leave the accumulator empty and stall the epoch",
   "The schedule would leak the validator set to observers who have not synchronized the state, which would let them forge the epoch marker in a header"
  ],
  "optionsZh": [
   "任何人都能看出接下來由誰出塊，於是可以精準攻擊或收買那一位；一個廉價的針對性行動就能擋下區塊，而全網規模的攻擊反而做不到",
   "任何人都能算出同一份出塊表，因而能在別人的時槽出塊，因為「知道下一個是誰」正是封印區塊的資格證明",
   "validator 能看見自己未來的時槽，於是會把票拖到最後一刻才提交，導致 accumulator 空著、整個 epoch 停擺",
   "出塊表會把 validator 集合洩漏給尚未同步狀態的觀察者，讓他們能偽造 header 裡的 epoch marker"
  ],
  "answer": 0,
  "explanation": "匿名買到的是**抗針對性攻擊**。如果所有人都知道第 N 槽由某位 validator 出塊，攻擊者只要在那六秒內癱瘓那一台機器（DoS），或事先收買他，就能讓那一槽出不了塊——成本遠低於攻擊整個網路。Safrole 用 ring VRF 讓驗證者只能確認「某位 γ′_P 的成員擁有這張票」而不知道是誰，直到他真的出塊為止。要注意匿名不是靠保密實現的：出塊資格由密碼學證明（持票人才能產生對應的 VRF 輸出），別人算得出票在哪一槽，但算不出票屬於誰。",
  "optNotes": [
   "針對性 DoS 與賄賂的成本遠低於全網攻擊，這正是匿名要擋的東西。",
   "出塊資格由密碼學證明，知道「誰是下一個」並不能讓你冒名出塊。",
   "票券的提交期限由 Y = 500 的 tail 規定，與匿名與否無關。",
   "validator 集合本來就是公開的（epoch marker 就在 header 裡），保密的是「票屬於誰」。"
  ],
  "trap": "匿名擋的是針對性攻擊；公開的是「哪一槽有票」，保密的是「票是誰的」。"
 },
 {
  "id": "n3-fallback-basic",
  "ch": "N3", "section": "§6.5", "gpRef": "§6",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "safrole", "fallback"],
  "stem": "If too few tickets are collected during an epoch, JAM does not stall. What does it do instead, and what is given up?",
  "stemZh": "如果一個 epoch 內收集到的票太少，JAM 不會停擺。它改用什麼做法？又放棄了什麼？",
  "options": [
   "It falls back to picking authors from the entropy and the validator set, which keeps blocks coming but makes the whole epoch's schedule publicly computable",
   "It extends the epoch until enough tickets arrive, which preserves anonymity but leaves the chain producing blocks at an unpredictable rate meanwhile",
   "It lets any validator author any slot on a first-come basis, which keeps blocks coming but allows two validators to seal the same slot and fork the chain",
   "It reuses the previous epoch's schedule, which preserves anonymity but gives the same validators the same slots twice in a row"
  ],
  "optionsZh": [
   "退回用 entropy 與 validator 集合挑選出塊者：區塊照樣產出，但整個 epoch 的出塊表變成任何人都算得出來",
   "延長該 epoch 直到收到足夠的票：匿名性得以保留，但這段期間整條鏈的出塊速率會變得無法預測",
   "讓任何 validator 以先到先得的方式出任何一槽：區塊照樣產出，但可能有兩位 validator 封印同一槽而造成分叉",
   "沿用上一個 epoch 的出塊表：匿名性得以保留，但同一批 validator 會連續兩輪拿到相同的時槽"
  ],
  "answer": 0,
  "explanation": "票不夠時走 **fallback**：直接用 entropy 與 active validator 集合算出每一槽的出塊者。這條路的計算輸入在 epoch 一開始就全部公開，所以**整個 epoch 的出塊表任何人都能算出來**——匿名性在這段期間完全消失，針對性 DoS 與賄賂重新變得可行。GP 仍然這樣設計，是因為**活性優先於匿名性**：寧可退化成公開的輪值表，也不要因為票不夠就停鏈。這也解釋了為什麼票券投票有 Y = 500 的截止線——留 500 個時槽讓票累積，盡量不走到 fallback。",
  "optNotes": [
   "用 entropy 直接算出塊者，代價是整個 epoch 的排班變成公開資訊。",
   "epoch 長度固定為 E = 600，不會為了等票而延長。",
   "每一槽仍然只有一位合法出塊者，fallback 不會退化成先到先得。",
   "沿用舊排班會讓同一批人重複出塊且可預測，GP 沒有採用這個做法。"
  ],
  "trap": "fallback 保住活性、犧牲匿名；它不是停擺也不是先到先得。"
 },
 {
  "id": "n3-safrole-vs-grandpa",
  "ch": "N3", "section": "§4.3; §19", "gpRef": "§4 & §19",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "finality"],
  "alsoCh": ["N1"],
  "stem": "JAM runs two separate consensus mechanisms. What does each one guarantee that the other does not?",
  "stemZh": "JAM 同時跑兩套共識機制。各自保證了什麼對方不保證的事？",
  "options": [
   "Safrole makes it rare for two blocks to compete for the same position; Grandpa makes a block past a certain point permanent, which block production alone can never promise",
   "Safrole orders transactions within a block; Grandpa orders blocks relative to each other, so together they give a single total order over all work",
   "Safrole decides which chain is best when a fork appears; Grandpa decides who may author, so the two run in sequence rather than in parallel",
   "Safrole guarantees that every slot produces a block; Grandpa guarantees that every block is eventually audited, so together they cover liveness and correctness"
  ],
  "optionsZh": [
   "Safrole 讓兩個區塊競爭同一個位置變得罕見；Grandpa 讓超過某個點的區塊成為永久，而這是出塊機制本身永遠無法承諾的",
   "Safrole 決定區塊內部交易的順序，Grandpa 決定區塊彼此之間的順序，兩者合起來給出所有工作的單一全序",
   "Safrole 在分叉出現時決定哪條鏈最好，Grandpa 決定由誰出塊，所以兩者是先後執行而非平行運作",
   "Safrole 保證每個時槽都會產出區塊，Grandpa 保證每個區塊最終都會被稽核，兩者合起來涵蓋活性與正確性"
  ],
  "answer": 0,
  "explanation": "兩者解決的是**不同的問題**。Safrole 管「誰可以出塊」：每槽只有一位有資格，因此很少長出兩個競爭的 head——但它無法保證某個區塊永遠不會被回滾，因為更長的鏈隨時可能出現。Grandpa 管 **finality**：一旦足夠多的 validator 對某個區塊表態，它就永久留在歷史裡。GP §4.3 列了三個目標：很少分叉（Safrole）、分叉快速收斂（兩者共同）、能指出某個近期區塊永久留存（Grandpa）。JAM 沒有交易也就沒有「交易排序」，稽核則是另一套機制（ELVES）。",
  "optNotes": [
   "很少分叉 vs 永不回滾——這正是出塊機制與 finality gadget 的分工。",
   "JAM 沒有交易，也就沒有「區塊內的交易排序」這件事。",
   "角色反了：出塊資格是 Safrole 的事，best-chain 規則另有定義。",
   "Safrole 不保證每槽都出塊（持票人可能離線），稽核也不是 Grandpa 負責。"
  ],
  "trap": "Safrole 管資格、Grandpa 管永久；分叉快速收斂才是兩者共同的貢獻。"
 },
 {
  "id": "n3-two-signatures",
  "ch": "N3", "section": "§5.1; §6.4", "gpRef": "§5 & §6",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "header", "entropy"],
  "stem": "Every header carries two Bandersnatch signatures, not one. What is the second one for?",
  "stemZh": "每個 header 都帶兩個 Bandersnatch 簽章而不是一個。第二個是做什麼用的？",
  "options": [
   "One seals the block and proves the author was entitled to the slot; the other produces the fresh randomness that gets folded into the chain's entropy pool",
   "One is signed by the author and the other by the previous author, so the pair chains the two blocks together in addition to the parent hash",
   "One covers the header and the other covers the extrinsic, so a node can check the header before it has downloaded the block body",
   "One is used during normal operation and the other only during fallback, so a verifier can tell from the header which mode the epoch is in"
  ],
  "optionsZh": [
   "一個封印區塊、證明出塊者對這個時槽有資格；另一個產生新的隨機性，被混進整條鏈的 entropy pool",
   "一個由本塊出塊者簽、另一個由上一塊的出塊者簽，兩者除了父雜湊之外再把兩個區塊串在一起",
   "一個涵蓋 header、另一個涵蓋 extrinsic，讓節點在還沒下載區塊本體之前就能先檢查 header",
   "一個用於正常運作、另一個只在 fallback 時使用，讓驗證者能從 header 看出這個 epoch 處於哪種模式"
  ],
  "answer": 0,
  "explanation": "**H_S（seal）證明資格，H_V（entropy VRF）產生隨機性。** 兩者都是 Bandersnatch VRF 簽章，但用途完全不同：seal 簽的是不含 seal 自己的 header 編碼，用來證明「這一槽本來就該由我出」；entropy 簽章的輸出 Y(H_V) 則被混進 η_0，成為下個 epoch 抽籤與 guarantor 洗牌的隨機性來源。分成兩個而不是共用一個，是為了讓熵不可被操縱——熵簽章的 context 綁在 seal 的輸出上，訊息在產生熵之前就已經固定，出塊者無法試很多份區塊挑一個對自己有利的結果。",
  "optNotes": [
   "一個證明資格、一個產生熵，兩者用途獨立但透過 context 綁在一起。",
   "兩個簽章都由本塊出塊者產生，與上一塊的作者無關。",
   "seal 簽的是 header 編碼；extrinsic 的完整性由 H_X 這個雜湊承諾，不需要另一個簽章。",
   "模式（ticket 或 fallback）由 context 字串區分，但那是同一個 seal 的兩種形式，不是兩個簽章。"
  ],
  "trap": "H_S 證明資格、H_V 產生熵；分開是為了讓熵不可被出塊者挑選。"
 },
 {
  "id": "n3-entropy-basic",
  "ch": "N3", "section": "§6.4 Entropy", "gpRef": "§6",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "entropy"],
  "stem": "The chain needs randomness for the ticket lottery and for assigning validators to cores. Why can it not simply hash the latest block?",
  "stemZh": "這條鏈需要隨機性來做票券抽籤與 validator 對 core 的指派。為什麼不能就直接雜湊最新的區塊？",
  "options": [
   "Because the author chooses the block's contents, so it could try many variations and publish the one whose hash favours it; a VRF output is fixed by the key, not by the contents",
   "Because a block hash is only 32 octets, which is too little entropy to seed a lottery over hundreds of validators across six hundred slots without repeating itself",
   "Because the block hash is not known until the block has propagated to its peers, and the lottery for the coming epoch must be resolved before that broadcast begins",
   "Because hashing is deterministic, and a lottery needs a source that no other participant can reproduce once its result has already been consumed"
  ],
  "optionsZh": [
   "因為區塊內容由出塊者決定，他可以試很多種版本、挑一個雜湊對自己有利的發布出來；VRF 的輸出則由金鑰決定，不由內容決定",
   "因為區塊雜湊只有 32 位元組，用來為橫跨六百個時槽、數百位 validator 的抽籤提供種子，熵量太少",
   "因為區塊雜湊要等區塊傳播之後才知道，而抽籤必須在區塊廣播給任何人之前就完成",
   "因為雜湊是確定性的，而抽籤需要一個一旦被使用就無法被別人重現的來源"
  ],
  "answer": 0,
  "explanation": "問題在**可偏置（bias）**。如果隨機性直接來自區塊雜湊，出塊者可以微調區塊內容（多放一筆、少放一筆、換個順序）試出很多不同的雜湊，再挑一個讓自己下個 epoch 拿到好時槽的版本發布——這叫 grinding attack。JAM 改用 VRF：Y(H_V) 的值由**私鑰與 context 決定**，出塊者換再多內容也只能得到同一個輸出，沒有可挑的餘地。而且 context 綁在 seal 的輸出上，訊息在產生熵之前就固定了。確定性本身不是問題——隨機性必須人人可重算，否則無法達成共識。",
  "optNotes": [
   "出塊者能試很多版本挑對自己有利的雜湊，這正是 VRF 要擋掉的 grinding。",
   "32 位元組是標準的種子長度，熵量從來不是問題。",
   "抽籤本來就發生在區塊產生之後，時序不是理由。",
   "隨機性必須人人可重算才能達成共識，「不可重現」反而是不可接受的。"
  ],
  "trap": "要防的是 grinding：VRF 讓出塊者無法挑選自己的熵。"
 },
 {
  "id": "n3-block-too-new",
  "ch": "N3", "section": "§5.1", "gpRef": "§5",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "validity"],
  "alsoCh": ["N2"],
  "stem": "A node receives a well-formed block whose timeslot is a few seconds in the future. How should it treat it?",
  "stemZh": "一個節點收到一個格式正確、但時槽比現在早了幾秒（屬於未來）的區塊。它應該怎麼處理？",
  "options": [
   "Treat it as not yet valid rather than invalid, because the same block becomes valid as the clock advances and discarding it would punish a peer for a small clock difference",
   "Reject it permanently and treat the sender as misbehaving, because a block claiming a future slot can only come from an author trying to seize a slot it was not given",
   "Accept it immediately, because the timeslot is only used for ordering and the seal already proves the author was entitled to that slot whenever it arrives",
   "Accept it but withhold it from peers until the slot arrives, because forwarding a future block would let it propagate faster than the protocol intends"
  ],
  "optionsZh": [
   "當成「還不到時候」而不是無效，因為同一個區塊會隨著時鐘前進而變得有效；丟棄它等於因為一點時鐘誤差就懲罰對方",
   "永久拒絕並把發送方視為行為不端，因為宣稱未來時槽的區塊只可能來自想搶奪非屬自己時槽的出塊者",
   "立刻接受，因為時槽只用於排序，而 seal 已經證明出塊者對該時槽有資格，不論它何時抵達",
   "接受但先不轉發給其他節點，直到該時槽到來，因為轉發未來區塊會讓它傳播得比協定預期更快"
  ],
  "answer": 0,
  "explanation": "有效性條件是 P(H)_T < H_T ∧ H_T · P ≤ 𝕋，其中後半是**暫時性**的。GP 特別補了一句：「Blocks considered invalid by this rule may become valid as 𝕋 advances」——來自未來的區塊只是還沒到時候，不是攻擊。實作上通常先留著、等時間到再處理。把它當成永久無效並封鎖來源是常見的錯誤，在節點之間時鐘略有偏差時會造成不必要的斷線。相對地，前半（必須嚴格大於父區塊的時槽）是永久性的，違反就是真的無效。",
  "optNotes": [
   "GP 明說這類區塊會隨時間推進而變有效，所以是暫時無效而非永久拒絕。",
   "時鐘小幅偏差就足以產生「未來區塊」，直接視為惡意會造成不必要的斷線。",
   "時槽不只用於排序，它本身就是有效性條件的一部分。",
   "協定沒有規定要延遲轉發；傳播策略不影響有效性判定。"
  ],
  "trap": "「太未來」是暫時無效；「不大於父區塊」才是永久無效。"
 },
]
