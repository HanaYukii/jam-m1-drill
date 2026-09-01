# -*- coding: utf-8 -*-
# Chapter 9 — Service Accounts (GP 0.8.0)
ITEMS = [
{
 "id": "ch09-account-fields",
 "ch": "9", "section": "9 Service Accounts", "gpRef": "eq. 9.3",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "state"],
  "stemZh": "在 GP 0.8.0（eq. 9.3）中，下列哪一個不是 service account A 的欄位？",
  "optionsZh": [
   "a_f——gratis storage offset，一筆以餘額計價的押金抵扣額",
   "a_p——parent service index，也就是建立這個 service 的那個 service",
   "a_n——一個 nonce，每次該 service 被 accumulate 時遞增一次",
   "a_m——每筆 deferred transfer 所需的最低 gas（minmemogas）"
  ],
  "stem": "Which of the following is NOT a field of a service account A in GP 0.8.0 (eq. 9.3)?",
 "options": [
  "a_f — the gratis storage offset, a balance-denominated deposit credit",
  "a_p — the parent service index, i.e. the service that created this one",
  "a_n — a nonce, incremented once on every accumulation of the service",
  "a_m — the minimum gas required for each deferred transfer (minmemogas)"
 ],
 "answer": 2,
 "optNotes": [
   "a_f 確實列在 eq. 9.3，就是 a_t = max(0, … − a_f) 裡被扣掉的那筆 deposit credit。",
   "a_p（parent）是 eq. 9.3 的欄位之一，記錄建立這個帳戶的 service index。",
   "service 不由私鑰控制、系統裡也沒有使用者交易，eq. 9.3 因此沒有 nonce 這一欄。",
   "a_m 是 §9.1 的「每筆 deferred transfer 的最低 gas」，確實在 eq. 9.3 的欄位表裡。",
 ],
 "explanation": "eq. 9.3：A ≡ (s storage, p preimages, l requests, f gratis, c codehash, b balance, g minaccgas, m minmemogas, r created, a lastacc, p parent)——十一個欄位，nonce 不在其中。§4.9.2 給了理由：「Since they are not controlled by a secret key, they do not need a nonce.」沒有私鑰控制、也沒有使用者交易，就沒有重放問題要防。兩個 gas 下限要分清：a_g minaccgas 是 per work-item，a_m minmemogas 是 per deferred-transfer。a_f（gratis）與 a_r/a_a/a_p 是 0.6.7～0.7.x 加入的 metadata；manager 才能建立帶 gratis 的 service（`new` 的 f ≠ 0 需要 manager 權限）。",
 "trap": "兩個 gas 下限：a_g 每個 work-item 的 accumulate 最低 gas；a_m 每筆 deferred transfer 的最低 gas。"
},
{
 "id": "ch09-code-metadata",
 "ch": "9", "section": "9.1 Code and Gas", "gpRef": "eq. 9.4",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "code"],
  "stemZh": "一個 service 的程式碼 a_c 與 metadata a_m 是怎麼從它的 code hash 導出的？",
  "optionsZh": [
   "a_c 在該帳戶自己的 lookup a_p 裡的 preimage 必須能解碼成 E(var(m), c)——一段變長的 metadata blob 後面接著程式碼；否則兩者皆為 ∅",
   "程式碼直接放在 storage 字典 a_s 裡、以 a_c 為 key，metadata 則放在 a_c ⌢ [0]；若該項不存在，該 service 會沿用先前的程式碼",
   "preimage 是從 manager service χ_M 的 lookup 取得的，所以所有 service 的程式碼都集中保管；該 blob 開頭的 32 個位元組是 metadata",
   "a_c 是純程式碼本身的 Blake2b，metadata 住在 storage 字典 a_s 裡；即使 preimage 不存在，程式碼仍可從它的雜湊解出來"
  ],
  "stem": "How are a service's code a_c and metadata a_m derived from its code hash?",
 "options": [
  "The preimage of a_c in the account's own lookup a_p must decode as E(var(m), c) — a var-length metadata blob followed by the code; otherwise both are ∅",
  "The code sits directly in the storage dictionary a_s under the key a_c, with the metadata under a_c ⌢ [0]; a missing entry leaves the service on its previous code",
  "The preimage is fetched from the manager service χ_M's lookup, so all service code is held centrally; the leading 32 octets of that blob are the metadata",
  "a_c is the Blake2b of the raw code alone and the metadata lives in the storage dictionary a_s; a missing preimage still leaves the code resolvable from its hash"
 ],
 "answer": 0,
 "optNotes": [
   "eq. 9.4：(a_m, a_c) = (m, c) 當 E(var(m), c) = a_p[a_c]，兩者同來自這一份 preimage。",
   "a_s 是 accumulate 才寫得到、refine 讀不到的 on-chain 存儲；查不到時給 (∅, ∅)，沒有沿用舊 code。",
   "χ_M 的權力限於改 χ 與發 gratis credit，code 一律取自服務自己的 a_p；metadata 也不是固定 32 octets。",
   "a_c 雜湊的是整個 E(var(m), c) 編碼而非裸 code，且 hash 反推不出 preimage。",
 ],
 "explanation": "eq. 9.4：(a_m, a_c) = (m, c) 當 E(var(m), c) = a_p[a_c]，否則 (∅, ∅)。即 code hash 指向的、且必須在服務自己的 preimage lookup a_p 裡的那份 preimage，內容是「var-length metadata ⌢ code」的編碼；metadata 是 opaque（JIP-6 討論標準化）。code 走 preimage 而不走 storage 的理由在 §9.2：只有 preimage 是「available also in-core」的那一種，refine 根本讀不到 a_s。eq. 9.6 的不變式 (h ↦ d) ∈ a_p ⟹ h = H(d) 則固定了雜湊的對象；preimage 不在 state 裡，服務就是不能執行，refine 會回 BAD（eq. 11.7 的 BAD = code unavailable at lookup anchor）。entry points：0 = refine（in-core）、1 = accumulate（on-chain）（0.7.1 起 on_transfer 併入 accumulate）。",
 "trap": "`new` 會在 requests 裡放 (c, l) → []，等待 preimage 被提供。"
},
{
 "id": "ch09-lookup-status",
  "alsoCh": ["14"],
 "ch": "9", "section": "9.2 Preimage Lookups", "gpRef": "§9.2.2 Semantics, eq. 9.7",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "preimages"],
  "stemZh": "一筆 request 條目 a_l[(h, len)] 裝的是最多 3 個時槽的序列。[x, y] 是什麼意思？[x, y, z] 又是什麼意思？",
  "optionsZh": [
   "[x, y]：該 preimage 從 x 起可用、自 y 起不可用；[x, y, z]：從 x 起可用直到 y，並自 z 起再次可用",
   "[x, y]：該 preimage 在 x 被請求、在 y 首次被提供；[x, y, z]：在 y 被提供、然後在 z 被完全從狀態中清除",
   "[x, y]：該 preimage 從 x 起可用、並在 y 被完全從狀態中清除；[x, y, z]：一種不合法的形狀，沒有任何 host call 產生得出來",
   "[x, y]：兩個不同的 service 請求了同一份 preimage，一個在 x、一個在 y；[x, y, z]：三個不同的 service 各自請求了它"
  ],
  "stem": "A request entry a_l[(h, len)] holds a sequence of up to 3 timeslots. What does [x, y] mean, and what does [x, y, z] mean?",
 "options": [
  "[x, y]: the preimage was available from x and is unavailable since y; [x, y, z]: it was available from x until y and is available again since z",
  "[x, y]: the preimage was requested at x and was first supplied at y; [x, y, z]: supplied at y and then expunged from state entirely at z",
  "[x, y]: the preimage was available from x and was expunged from state at y; [x, y, z]: an illegal shape that no host call can ever produce",
  "[x, y]: two distinct services requested the same preimage, one at x and one at y; [x, y, z]: three distinct services each requested it"
 ],
 "answer": 0,
 "optNotes": [
   "兩個形狀都對上 §9.2.2：第二個時刻是轉為 unavailable，第三個是再次可用的起點。",
   "序列裡不記 request 時刻——requested 的狀態就是空序列 []；z 標記的也不是刪除。",
   "[x, y] 只是標成 unavailable，preimage 仍留在 a_p；[x, y, z] 是 §9.2.2 明列的合法形狀。",
   "a_l 掛在單一服務帳戶底下，鍵是 (h, len)、值是這個服務自己的可用性歷史，不記請求者身分。",
 ],
 "explanation": "§9.2.2 用**序列長度**編碼四種狀態，這是刻意的設計：**[]** = 已請求、還沒有人提供；**[x]** = 自 x 起可用；**[x, y]** = 曾於 x 起可用、自 y 起不可用；**[x, y, z]** = x 到 y 可用、自 z 起再次可用。eq. 9.7 的可用性判定 I(l, t) 直接對應：[x] → x ≤ t；[x, y] → x ≤ t < y；[x, y, z] → x ≤ t < y ∨ z ≤ t；[] → 恆為否。**為什麼只往尾端追加、不覆寫**：refine 在 in-core 會用 historical_lookup 查 preimage，而審計時 auditor 必須能對**任意一個 lookup-anchor 時點**重算出「當時到底可不可用」——若狀態被覆寫成單一布林值，這個重算就做不到，稽核也就失效了。所以這不是為了省空間，是為了**可追溯性**。**真正的刪除還要再等**：`forget` 只有在 y < t − D（D = 19,200 時槽 = 32 小時）之後才會真的移除，確保任何還在有效窗口內的稽核都查得到。你們的 `query` host call 把這四種狀態編進 φ_7／φ_8 回傳，讓 service 自己也能讀到。",
 "trap": "再次 solicit 一個 [x,y] 會變 [x,y,t]；forget 一個 [x] 變 [x,t]；forget [x,y]（y 夠舊）才真正刪除。"
},
{
 "id": "ch09-historical-lookup-calc",
 "ch": "9", "section": "9.2 Preimage Lookups", "gpRef": "eq. 9.7 (Λ)",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "preimages", "calc"],
  "stemZh": "某個 service 有一份 preimage p（雜湊 h、長度 40），其 a_l[(h, 40)] = [100, 250, 400]。關於歷史查詢 Λ(a, t, h) 的敘述哪一個正確？",
  "optionsZh": [
   "Λ 在 t = 120 與 t = 450 時回傳 p，但在 t = 300 時回傳 ∅",
   "Λ 只在 t = 300 時回傳 p",
   "只要 t ≥ 100，Λ 都回傳 p",
   "Λ 在 t = 120 時回傳 p，但在 t = 450 時回傳 ∅，因為最後那一項標記的是第二次撤除"
  ],
  "stem": "A service has preimage p (hash h, length 40) with a_l[(h, 40)] = [100, 250, 400]. Which statement about the historical lookup Λ(a, t, h) is correct?",
 "options": [
  "Λ returns p for t = 120 and t = 450, but ∅ for t = 300",
  "Λ returns p for t = 300 only",
  "Λ returns p for any t ≥ 100",
  "Λ returns p for t = 120 but ∅ for t = 450, since the last entry marks a second withdrawal"
 ],
 "answer": 0,
 "optNotes": [
   "三個時點依 x ≤ t < y ∨ z ≤ t 判定為 ✓/✗/✓，與這組答案完全相符。",
   "剛好只認了空窗：250 … 400 才是 unavailable 的區間，t = 300 是唯一查不到的。",
   "把 [x, y, z] 讀成「自 x 起一直可用」，忽略了 y = 250 到 z = 400 的空窗。",
   "第三個時刻是「再次可用」的起點而不是第二次撤回，t = 450 ≥ 400 查得到。",
 ],
 "explanation": "eq. 9.7 的 Λ(a, t, h) 是「在時間點 t 回頭看，這個 preimage 當時算不算可用」。a_l[(h, z)] 這個 request 狀態最多存三個時槽，長度本身就是語意：**[]** = 已請求但還沒提供；**[x]** = 從 x 起可用（還在用）；**[x, y]** = x 起可用、y 時被移除；**[x, y, z]** = 移除後又在 z 被重新提供。所以三元素的可用條件是 x ≤ t < y ∨ z ≤ t——兩段開區間中間夾一段空窗。本題代入 a_l[(h, 40)] = [100, 250, 400]：t = 120 落在 [100, 250) ✓；t = 300 既不在 [100, 250)、也還沒到 400 ✗（這就是那段空窗）；t = 450 ≥ 400 ✓。**兩個容易漏掉的前提**：其一，Λ 還要求 h ∈ keys(a_p)，也就是 preimage 的**內容**現在仍在 state 裡——a_l 記的是「什麼時候可用」，a_p 才是 blob 本身，兩者是分開的。其二，t 的定義域是 (H_T − D) … H_T，D = C_expungeperiod = 19,200 時槽（19,200 × 6 秒 = 32 小時）：超過這個期間、又沒有被引用的 preimage 可以被 expunge，屆時連歷史查詢也查不到。（別和 L = 14,400 時槽 = 24 小時搞混，那是 §11 lookup anchor 的年齡上限，是另一個常數。）",
 "trap": "三個時間點的語意：available / unavailable / available again。"
},
{
 "id": "ch09-footprint-formula",
 "ch": "9", "section": "9.3 Account Footprint and Threshold Balance", "gpRef": "eq. 9.8",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "balance"],
  "stemZh": "footprint 的 a_i（項數）與 a_o（位元組數）以及門檻餘額 a_t 是怎麼定義的？",
  "optionsZh": [
   "a_i = 2·|a_l| + |a_s|；a_o = Σ_{(h,z)∈keys(a_l)} (81 + z) + Σ_{(x,y)∈a_s} (34 + |x| + |y|)；a_t = max(0, B_S + B_I·a_i + B_L·a_o − a_f)",
   "a_i = |a_l| + |a_s|；a_o = Σ_{(h,z)∈keys(a_l)} (81 + z) + Σ_{(x,y)∈a_s} (34 + |x| + |y|)；a_t = max(0, B_S + B_I·a_i + B_L·a_o)",
   "a_i = 2·|a_p| + |a_s|；a_o = Σ_{(h,d)∈a_p} (81 + |d|) + Σ_{(x,y)∈a_s} (34 + |x| + |y|)；a_t = max(0, B_S + B_I·a_i + B_L·a_o − a_f)",
   "a_i = 2·|a_l| + |a_s|；a_o = Σ_{(h,z)∈keys(a_l)} (32 + z) + Σ_{(x,y)∈a_s} (32 + |y|)；a_t = max(0, B_I·a_i + B_L·a_o − a_f)"
  ],
  "stem": "How are the footprint a_i (items) and a_o (octets) and the threshold balance a_t defined?",
 "options": [
  "a_i = 2·|a_l| + |a_s|; a_o = Σ_{(h,z)∈keys(a_l)} (81 + z) + Σ_{(x,y)∈a_s} (34 + |x| + |y|); a_t = max(0, B_S + B_I·a_i + B_L·a_o − a_f)",
  "a_i = |a_l| + |a_s|; a_o = Σ_{(h,z)∈keys(a_l)} (81 + z) + Σ_{(x,y)∈a_s} (34 + |x| + |y|); a_t = max(0, B_S + B_I·a_i + B_L·a_o)",
  "a_i = 2·|a_p| + |a_s|; a_o = Σ_{(h,d)∈a_p} (81 + |d|) + Σ_{(x,y)∈a_s} (34 + |x| + |y|); a_t = max(0, B_S + B_I·a_i + B_L·a_o − a_f)",
  "a_i = 2·|a_l| + |a_s|; a_o = Σ_{(h,z)∈keys(a_l)} (32 + z) + Σ_{(x,y)∈a_s} (32 + |y|); a_t = max(0, B_I·a_i + B_L·a_o − a_f)"
 ],
 "answer": 0,
 "optNotes": [
   "完全對上 eq. 9.8：request 2 items / 81+z octets、storage 1 item / 34+|key|+|value|，門檻再扣 a_f。",
   "request 的係數是 2·|a_l| 不是 1，而且 gratis offset a_f 必須從門檻裡扣掉。",
   "求和應跑 requests dictionary a_l 的鍵 (h, z)、用宣告長度 z，不是跑 a_p 用實際 blob 長度。",
   "固定開銷是 81 與 34 不是 32/32，storage 的 key 長度要計入，base deposit B_S 也不能漏。",
 ],
 "explanation": "eq. 9.8 三條式子，數字都是 GP 直接給定的常數，不需要推導但要記得。**a_i（項數）= 2·|a_l| + |a_s|**——每個 lookup request 算 **2 項**、每個 storage entry 算 1 項。request 算兩項是因為它同時佔用了 requests 字典與（供應後的）preimages 字典兩個位置。**a_o（位元組）= Σ_{(h,z) ∈ keys(a_l)} (81 + z) + Σ_{(x,y) ∈ a_s} (34 + |x| + |y|)**——81 與 34 是固定開銷（涵蓋 key、長度前綴、trie 節點等），z 是**宣告的** preimage 長度。**a_t（門檻餘額）= max(0, B_S + B_I·a_i + B_L·a_o − a_f)**，B_S = 100（基本）、B_I = 10（每項）、B_L = 1（每位元組），a_f 是 gratis 抵扣，扣成負數再由 max(0, ·) 夾回零。**最關鍵的設計點**：計價對象是 **requests 字典**而不是已經供應的 preimages——也就是說 `solicit` 一發出去就開始收押金，還沒有人提供資料也一樣算錢。這是為了防止免費占位：否則任何 service 都能無成本地宣告要一百萬個 preimage。**fuzzer 抓過的坑**：你們曾漏減 a_f，但因為測試 trace 的 DepositOffset 都是 0，錯了很久沒被發現——這類「參數恆為零所以錯得看不出來」的 bug 值得特別留意。",
 "trap": "request 算 2 items；storage 算 1 item。"
},
{
 "id": "ch09-privileges",
 "ch": "9", "section": "9.4 Service Privileges", "gpRef": "eq. 9.9–9.10",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "privileges"],
  "stemZh": "特權狀態 χ ≡ (χ_M, χ_V, χ_R, χ_A, χ_Z)。哪一組「特權 → 權力」的對應是正確的？",
  "optionsZh": [
   "χ_M manager：可更動 χ（bless）並授予 gratis storage；χ_V delegator：可設定 ι（designate）；χ_R registrar：可建立索引小於 S = 2^16 的 service；χ_A assigners（每個 core 一個）：可設定 φ[c]（assign）；χ_Z：每個區塊都會被 accumulate、並帶固定 gas 額度的 service",
   "χ_M manager：可設定 ι（designate）；χ_V delegator：可更動 χ（bless）；χ_R registrar：可設定 φ[c]（assign）；χ_A assigners（每個 core 一個）：可建立索引小於 S = 2^16 的 service；χ_Z：在 accumulate 期間免於 gas 計量的 service",
   "χ_M：替其他所有 service 支付 accumulation gas 的那個 service；χ_V：當前作用中的 validator 集合 κ；χ_R：代其他人登記 preimage 的那個 service；χ_A：每個 tranche 重新抽出的 auditor；χ_Z：獲准持有零餘額的 service",
   "χ_M manager：可更動 χ（bless）並授予 gratis storage；χ_V delegator：可直接設定 κ；χ_R registrar：可在任意索引建立 service；χ_A：一個全域的 assigner，為所有 core 設定 φ；χ_Z：每個 epoch 被 accumulate 一次的 service"
  ],
  "stem": "The privileges state χ ≡ (χ_M, χ_V, χ_R, χ_A, χ_Z). Which mapping of privilege → power is correct?",
 "options": [
  "χ_M manager: may alter χ (bless) and grant gratis storage; χ_V delegator: may set ι (designate); χ_R registrar: may create services with indices below S = 2^16; χ_A assigners (one per core): may set φ[c] (assign); χ_Z: services that accumulate every block with a fixed gas allowance",
  "χ_M manager: may set ι (designate); χ_V delegator: may alter χ (bless); χ_R registrar: may set φ[c] (assign); χ_A assigners (one per core): may create services with indices below S = 2^16; χ_Z: services exempt from gas metering while they accumulate",
  "χ_M: the service that pays the accumulation gas of every other service; χ_V: the current active validator set κ; χ_R: the service that registers preimages on behalf of others; χ_A: the auditors drawn afresh in each tranche; χ_Z: services allowed to hold a zero balance",
  "χ_M manager: may alter χ (bless) and grant gratis storage; χ_V delegator: may set κ directly; χ_R registrar: may create services at any index; χ_A: one global assigner that sets φ for all cores; χ_Z: services that accumulate once per epoch"
 ],
 "answer": 0,
 "optNotes": [
   "完全對上 §9.4：manager 改 χ 兼發 gratis、delegator 設 ι、registrar 開 protected range、assigner 逐 core 改 φ[c]。",
   "四種權力的持有者被互相對調；而 χ_Z 拿到的是每塊一份固定 gas 額度，一樣照 PVM 計量，不是免計 gas。",
   "eq. 9.9 的五個成分全是 service index，既不是 κ 也不是審計者集合；accumulate 的 gas 也沒有誰替別人付。",
   "delegator 設的是 ι 而非 κ（要經 γ_k 才輪到 κ，eq. 6.14）；registrar 只限 index < 2^16，assigner 逐 core，χ_Z 每塊都跑。",
 ],
 "explanation": "§9.4 與 eq. 9.9：χ_M（manager）可改變 χ 並授予 storage deposit credits（gratis）；χ_V（delegator）可設定 ι（下下個 epoch 的 validator keys，透過 `designate`）；χ_R（registrar）可建立 index < S = 2^16 的受保護 service；χ_A ∈ [N_S]_C 每個 core 一個 assigner，可改 φ[c]（`assign`）；χ_Z ∈ D⟨N_S→N_G⟩ always-accumulate 服務與其每塊的基本 gas。GP 的敘述順序本身就是記憶點：「manager … able to effect an alteration of χ … as well as bestow services with storage deposit credits. The next, χ_V, is able to set ι. Then χ_R alone is able to create new service accounts with indices in the protected range. The following, χ_A, are the service indices capable of altering the authorizer queue φ, one for each core.」0.8.0 (#519) 把 `bless` 限制為只有 manager 可呼叫——之前的漏洞：任意 service 可 bless 自己成 manager 再用 `new` 取得 gratis storage。",
 "trap": "registrar 是 0.7.1 加入的（Small service IDs）；0.8.0 bless 只限 manager。"
},
{
 "id": "ch09-preimage-vs-storage",
 "ch": "9", "section": "9.2 Preimage Lookups", "gpRef": "§9.2 intro",
 "difficulty": 1, "kind": "rationale", "tags": ["accounts", "preimages", "rationale"],
  "stemZh": "GP 列出 preimage lookup 與一般 storage 之間的三項差異。下列哪一項不是其中之一？",
  "optionsZh": [
   "preimage 的資料由外部提供（透過 E_P），而 storage 的資料源自該 service 自己的 accumulation",
   "preimage 是從一個雜湊映到它的原像，而 storage 是從任意 key 映到 value",
   "preimage 可以被 service 立即移除，而 storage 條目則會被保留 28 天",
   "preimage 資料一旦被提供，必須先經過一段「不可用」期間才能被移除，好讓它的歷史可用性得以保留"
  ],
  "stem": "The GP lists three differences between preimage lookups and general storage. Which is NOT one of them?",
 "options": [
  "Preimage data is supplied extrinsically (via E_P), whereas storage data originates from the service's own accumulation",
  "Preimages map a hash to its preimage, whereas storage maps arbitrary keys to values",
  "Preimages may be removed instantly by the service, whereas storage entries are retained for 28 days",
  "Preimage data, once supplied, goes through an 'unavailable' period before it may be removed, so that its historical availability is retained"
 ],
 "answer": 2,
 "optNotes": [
   "這是 §9.2 列出的差異之一：preimage 由 E_P 外部提供，storage 由服務自己的 accumulate 寫入。",
   "這是 §9.2 的第一個差異：一邊是 hash 對應其 preimage，一邊是任意 key 對 value。",
   "方向剛好說反：GP 說的是 preimage「may not be removed freely」，被綁住的是 preimage 不是 storage。",
   "這正是 §9.2 的第三個差異：供應後要先標成 unavailable，過一段時間才能移除。",
 ],
 "explanation": "§9.2 列出的三個差異：**① 索引方式**——preimage 是 hash → preimage（key 由內容決定），storage 是任意 key → value。**② 資料來源**——preimage 由**外部**透過 E_P extrinsic 提供，storage 則由 accumulate 自己寫入。**③ 移除方式**——GP 原文：preimage「once supplied, may not be removed freely; instead it goes through a process of being marked as unavailable, and only after a period of time may it be removed」。**第三點是這題的重點，理由也在同一段**：refine 在 in-core 會用 historical_lookup 查 preimage，而 auditor 事後重跑時必須能確定「在那個 lookup-anchor 時點，這份資料到底算不算可用」。若 service 能隨時把 preimage 抹掉，這個判定就沒有依據，一個惡意 service 甚至可以在被稽核前刪掉資料、讓所有 auditor 都無法驗證。所以移除必須走「先標記不可用、等過 D = 19,200 時槽（32 小時）、再由 `forget` 真正刪除」的兩段式流程。**storage 沒有這個限制**：它是 accumulate 的私有狀態，不參與 in-core 的稽核路徑，服務想刪就刪。「28 天」這個數字則是 §14 匯出 segment 的保存期限，跟這裡無關，是常見的混淆來源。",
 "trap": "forget 後要等 D = 19,200 slots 才能真正刪除。"
},
]
