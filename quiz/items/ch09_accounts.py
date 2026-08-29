# -*- coding: utf-8 -*-
# Chapter 9 — Service Accounts (GP 0.8.0)
ITEMS = [
{
 "id": "ch09-account-fields",
 "ch": "9", "section": "9 Service Accounts", "gpRef": "eq. 9.3",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "state"],
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
 "ch": "9", "section": "9.2 Preimage Lookups", "gpRef": "§9.2.2 Semantics, eq. 9.7",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "preimages"],
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
 "explanation": "§9.2.2：h = []：requested 未提供；[x]：自 x 起 available；[x, y]：曾於 x 可用、自 y 起 unavailable；[x, y, z]：x～y 可用、z 起再次可用。eq. 9.7 的 I(l, t)：[x] → x ≤ t；[x,y] → x ≤ t < y；[x,y,z] → x ≤ t < y ∨ z ≤ t；[] → ⊥。真正要移除還得靠 `forget`，而且要等 y < t − D。這個「歷史可用性」是為了 in-core refine 的 historical_lookup 能在任何 lookup-anchor 時點被確定性地重算（審計需要），所以狀態只往序列尾端追加。你們 `query` host call 把這四種狀態編成 φ_7/φ_8。",
 "trap": "再次 solicit 一個 [x,y] 會變 [x,y,t]；forget 一個 [x] 變 [x,t]；forget [x,y]（y 夠舊）才真正刪除。"
},
{
 "id": "ch09-historical-lookup-calc",
 "ch": "9", "section": "9.2 Preimage Lookups", "gpRef": "eq. 9.7 (Λ)",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "preimages", "calc"],
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
 "explanation": "eq. 9.7：[x,y,z] 的條件是 x ≤ t < y ∨ z ≤ t。逐一代入：t=120：100 ≤ 120 < 250 ✓；t=300：不在 [100,250) 且 300 < 400 ✗；t=450：450 ≥ 400 ✓。Λ 還要求 h ∈ keys(a_p)（preimage 還在 state 裡），而 t 的定義域是 (H_T − D) … H_T，D = 19,200 slots（32 小時）——超過這個期間的 preimage 可能已被 expunge。",
 "trap": "三個時間點的語意：available / unavailable / available again。"
},
{
 "id": "ch09-footprint-formula",
 "ch": "9", "section": "9.3 Account Footprint and Threshold Balance", "gpRef": "eq. 9.8",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "balance"],
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
 "explanation": "eq. 9.8：每個 lookup request 算 2 個 item 與 81+z octets（z 是宣告的 preimage 長度；81 是 GP 給定的固定開銷常數），每個 storage entry 算 1 個 item 與 34+|k|+|v| octets（34 同為固定開銷）。這些數字直接寫在 eq. 9.8 裡，面試時不需要推導、但要記得。a_t = max(0, B_S + B_I·a_i + B_L·a_o − a_f)，B_S = 100、B_I = 10、B_L = 1（appendix I），a_f 是 gratis 抵扣，扣到負數再由 max(0, ·) 夾回零。計價對象是 requests dictionary 而非已供應的 preimages，等於 solicit 一發出就開始收押金，防止免費占位。fuzzer 曾抓到你們少減 a_f（issue digest：因為 traces 的 DepositOffset 都是 0 所以一直沒發現）。",
 "trap": "request 算 2 items；storage 算 1 item。"
},
{
 "id": "ch09-privileges",
 "ch": "9", "section": "9.4 Service Privileges", "gpRef": "eq. 9.9–9.10",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "privileges"],
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
 "explanation": "§9.2：三個差異——(1) hash→preimage vs 任意 key→value；(2) preimage 由 extrinsic 外部提供，storage 由 accumulate 產生；(3) preimage「once supplied, may not be removed freely; instead it goes through a process of being marked as unavailable, and only after a period of time may it be removed」。理由：refine 在 in-core 用 historical_lookup 查 preimage，審計時必須能確定「當時是否可用」，所以移除只能走這種可追溯的兩段式流程。",
 "trap": "forget 後要等 D = 19,200 slots 才能真正刪除。"
},
]
