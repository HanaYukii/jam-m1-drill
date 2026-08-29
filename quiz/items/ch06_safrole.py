# -*- coding: utf-8 -*-
# Chapter 6 — Block Production and Chain Growth (Safrole), GP 0.8.0
ITEMS = [
{
 "id": "ch06-gamma-components",
 "ch": "6", "section": "6.2 Safrole Basic State", "gpRef": "eq. 6.3–6.6",
 "difficulty": 1, "kind": "concept", "tags": ["safrole", "state"],
 "stem": "The Safrole state γ ≡ (γ_P, γ_Z, γ_S, γ_A). Which description is correct?",
 "options": [
  "γ_P pending validator keys for the next epoch; γ_Z the Bandersnatch ring root over γ_P; γ_S the current epoch's slot-sealer sequence (E tickets or E keys); γ_A the ticket accumulator (≤ E tickets) for the next epoch",
  "γ_P the previous epoch's validator keys (the λ set); γ_Z the Bandersnatch ring root over the active set κ; γ_S the current epoch's slot-sealer sequence (E tickets or E keys); γ_A the ticket accumulator (≤ E tickets) for the next epoch",
  "γ_P pending validator keys for the next epoch; γ_Z an Ed25519 ring root over γ_P; γ_S the ticket accumulator (≤ E tickets) for the next epoch; γ_A the current epoch's slot-sealer sequence (E tickets or E keys)",
  "γ_P the ticket accumulator (≤ E tickets) for the next epoch; γ_Z the Bandersnatch ring root over γ_P; γ_S the current epoch's slot-sealer sequence (E tickets or E keys); γ_A the pending validator keys, reset to ι at the start of each epoch"
 ],
 "answer": 0,
 "optNotes": [
  "四項全對上 eq. 6.3–6.5：pending set、對 γ_P 取的 ring root、本 epoch sealer、下個 epoch 的票池。",
  "γ_P 指向未來不是過去（λ 是 γ 之外的獨立狀態），且 eq. 6.14 的 ring root 是對 γ′_P 取的。",
  "ring root 只由 Bandersnatch key k_b 構成；γ_S 與 γ_A 兩者也被對調了。",
  "違反 6.5/6.6 的型別：accumulator 是 ticket 序列（≤ E 筆），pending set 是 validator key 序列。",
 ],
 "explanation": "GP eq. 6.3–6.5：γ_P（pending set，每個 epoch 開頭從 ι 重置，決定下一個 epoch 的 ring root）、γ_Z ∈ ring root（由 γ_P 的 Bandersnatch key k_b 組成，eq. 6.14 的 z = O([k_b | k ∈ γ′_P])）、γ_S ∈ [C]_E ∪ [H_B]_E（本 epoch 的 slot-sealer 序列：600 張 ticket 或 fallback 的 600 把 Bandersnatch key）、γ_A ∈ [C]_{:E}（下一個 epoch 用的 ticket accumulator，最多 E 筆）。Safrole 只透過 ι、κ、τ、η 與協定其他部分互動。最容易混的是 γ_S 與 γ_A 的時間方向：γ_S 是**本** epoch 已定案、每個 slot 對應一筆的 sealer 序列，γ_A 則是本 epoch 期間持續累積、供**下**個 epoch 用的 ticket 池。",
 "trap": "γ_S 有兩種型態（tickets 或 keys），serialization 時用 0/1 discriminator（見 D.1 C(4)）。"
},
{
 "id": "ch06-key-rotation",
 "ch": "6", "section": "6.3 Key Rotation", "gpRef": "eq. 6.14–6.15",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "validators", "epoch"],
 "stem": "On an epoch change (e′ > e), how are the validator key sets rotated per eq. 6.14?",
 "options": [
  "(γ′_P, κ′, λ′, γ′_Z) = (Φ(ι), γ_P, κ, z) where z is the ring root over the Bandersnatch keys of γ′_P and Φ nulls the entire key tuple of any validator whose Ed25519 key is in ψ′_O",
  "(γ′_P, κ′, λ′, γ′_Z) = (ι, γ_P, κ, z) where z is the ring root over γ′_P's Bandersnatch keys and no offender filtering is applied — offenders are skipped later by the guarantor assignment",
  "(γ′_P, κ′, λ′, γ′_Z) = (Φ(ι), ι, κ, z) where z is the ring root over the Bandersnatch keys of κ′ and Φ nulls the keys of offenders in the prior ψ_O rather than the posterior set",
  "(γ′_P, κ′, λ′, γ′_Z) = (Φ(γ_P), κ, λ, γ_Z) where the ring root is only recomputed when ι changes and Φ nulls the keys of offenders in ψ′_O — the sequences advance one step every block"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.14 與 6.15 完全對上：來源是 staging set ι，ring root 對 γ′_P 取，Φ 用 posterior ψ′_O。",
  "eq. 6.15 的 Φ 在輪換當下就把 offender 整把 key 歸零；§11 的 P(|κ′|, η′_2, τ′) 沒有排除機制。",
  "錯兩處：ring root 必須對 γ′_P（下個 epoch 的提票 ring）取，且 disputes 先跑，用 posterior ψ′_O。",
  "輪換只在 e′ > e 發生，且新 pending set 的來源是 ι 而非 γ_P 自身，否則 ι 永遠進不了 κ。",
 ],
 "explanation": "eq. 6.14：e′ > e 時 (γ′_P, κ′, λ′, γ′_Z) = (Φ(ι), γ_P, κ, z)，其中 z = O([k_b | k ∈ γ′_P])（ring root），否則四者不變。eq. 6.15：Φ(k) 把 k_e ∈ ψ′_O（posterior offenders，因為 disputes 已先處理）的 validator 整組換成全零 key。所以 staging set ι 要等**兩個** epoch 邊界才會成為 active（ι → γ_P → κ）。你們的 KeyRotate() 對應此式；ReplaceOffenderKeys 用的是 posterior ψ_O。",
 "trap": "常考：ι 什麼時候變成 κ？答：下下個 epoch（先進 γ_P，再進 κ）。"
},
{
 "id": "ch06-valcount",
 "ch": "6", "section": "6.3 Key Rotation", "gpRef": "eq. 6.7–6.8 (valcount)",
 "difficulty": 2, "kind": "delta", "tags": ["safrole", "validators", "delta-0.8.0"],
 "stem": "GP 0.8.0 (PR #514) generalized the validator-set size. Which sizes are permitted for ι, γ_P, κ and λ?",
 "options": [
  "Exactly 1023 validators always — the size is the fixed constant 3·C with C = 341 cores",
  "Any size between 6 and 1023 inclusive, with no divisibility rule (N_V ≡ N_{6..3·C+1})",
  "Any multiple of 3 between 6 and 3·C = 1023 inclusive (N_V ≡ {3c | c ∈ N_{2..C+1}})",
  "Any multiple of 3 between 3 and 3·C − 3 = 1020 inclusive (N_V ≡ {3c | c ∈ N_{1..C}})"
 ],
 "answer": 2,
 "optNotes": [
  "那是 0.7.2 的世界觀；0.8.0 之後 ι、γ_P、κ、λ 各自的長度都可以是 N_V 裡的任一值。",
  "「3 的倍數」是硬條件：每個 active core 固定配 3 個 guarantor，非 3 倍數會讓 |κ′|/3 不整除。",
  "eq. 6.8 的 N_V ≡ {3c | c ∈ N_{2…C+1}}，即 6, 9, 12, …, 1023。",
  "兩端各差一格：c 從 2 起算所以下界是 6，c 上限到 C+1 才使 3c 達到 3·C = 1023。",
 ],
 "explanation": "eq. 6.8：N_V ≡ {3c | c ∈ N_{2…C+1}}，即 6, 9, 12, …, 1023；§6.3：「The length of each sequence is always a multiple of 3 between 6 and 3C.」每個 active core 需要 3 個 guarantor，所以只有前 |κ′|/3 個 core 是 active（§11.3）。這是 0.7.2→0.8.0 的重大變化：很多常數改成依 |κ| 計算（例如 super-majority ⌊2|κ|/3⌋+1、tickets per validator n = ⌈2E/|γ′_P|⌉、erasure shards = |κ′|），designate host call 也只要求 z ∈ N_V。你們 repo 的 issue #1037 就是在追這個變動。",
 "trap": "tiny 模式 V=6、C=2；full V=1023、C=341（1023 = 3·341）。"
},
{
 "id": "ch06-validator-key-layout",
 "ch": "6", "section": "6.3 Key Rotation", "gpRef": "eq. 6.9–6.13",
 "difficulty": 1, "kind": "concept", "tags": ["safrole", "validators", "codec"],
 "stem": "A validator key K is a 336-octet sequence. What is the layout?",
 "options": [
  "Bandersnatch 32 | Ed25519 32 | BLS 144 | metadata 128",
  "Ed25519 32 | Bandersnatch 32 | BLS 96 | metadata 176",
  "Bandersnatch 32 | BLS 144 | Ed25519 32 | metadata 128",
  "Bandersnatch 33 | Ed25519 32 | BLS 143 | metadata 128"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.9–6.13 的順序與長度：32 + 32 + 144 + 128 = 336。",
  "前兩把的順序對調了，且 BLS 是 144 octets 不是 96（metadata 固定 128）。",
  "Ed25519 必須緊接 Bandersnatch 落在 offset 32，BLS 要到 offset 64 才開始。",
  "Bandersnatch 公鑰是 32 octets、BLS 是 144；總長雖仍為 336，每個切點卻都偏了一格。",
 ],
 "explanation": "eq. 6.9–6.13：k_b = k[0..32)（Bandersnatch）、k_e = k[32..64)（Ed25519）、k_l = k[64..208)（BLS，144 octets）、k_m = k[208..336)（metadata，128 octets，opaque，用來放例如網路位址等實務識別資訊）。32+32+144+128 = 336。",
 "trap": "BLS 144 octets（BLS12-381 上的 key 組合）。metadata 不參與任何密碼學運算。"
},
{
 "id": "ch06-entropy-update",
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "eq. 6.22–6.24",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "entropy"],
 "stem": "How is the entropy accumulator η updated in each block, and on an epoch change?",
 "options": [
  "η′_0 = H(η_0 ⌢ Y(H_V)) every block, folding in the entropy VRF's output; on e′ > e additionally (η′_1, η′_2, η′_3) = (η_0, η_1, η_2), otherwise (η_1, η_2, η_3) unchanged",
  "η′_0 = H(η_0 ⌢ H_V) every block, hashing the whole VRF signature rather than its 32-byte output; on e′ > e additionally (η′_1, η′_2, η′_3) = (η_0, η_1, η_2), otherwise unchanged",
  "η′_0 = H(η_0 ⌢ Y(H_S)) every block, folding in the seal's VRF output; on e′ > e additionally (η′_1, η′_2, η′_3) = (η′_0, η_1, η_2), pushing the posterior accumulator into the history",
  "η′_0 = H(η_0 ⌢ Y(H_V)) every block; the history rotates every block as well, so (η′_1, η′_2, η′_3) = (η_0, η_1, η_2) holds unconditionally and η_3 is always three blocks old"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.23 取的是 Y(H_V) 這個 VRF 輸出，eq. 6.24 的 rotate 只在 e′ > e 且推入 prior η_0。",
  "6.23 餵進 hash 的是 VRF **輸出** Y(H_V)；簽章 bytes 本身不是那個 unbiasable 隨機值。",
  "累積進 η_0 的是 H_V 的輸出；rotate 推入 posterior η′_0 更會把本塊 entropy 混進 η′_1。",
  "違反 6.24 的 case 條件：每塊都推的話，η_2 就不再是上上個 epoch 結束時的累積值。",
 ],
 "explanation": "eq. 6.23：η′_0 ≡ H(η_0 ⌢ Y(H_V))——用 **prior** η_0 與 H_V 的 VRF **輸出** Y(·)（App. G 定義為 output 的前 32 bytes）做 Blake2b。eq. 6.24：e′ > e 時 (η′_1, η′_2, η′_3) = (η_0, η_1, η_2)，注意推入的是 prior η_0，否則三者不變。H_V 的簽章 context 是 X_E ⌢ Y(H_S)（eq. 6.18），也就是 seal 的 VRF 輸出，因此 entropy 是「先固定訊息、再產生」的 bias-resistant 來源；Y(H_S) 本身只拿來當 H_V 的 context 並與 ticket id 比對，不會直接進 η。你們 UpdateEtaPrime0() / UpdateEntropy() 分別對應 6.23 / 6.24。",
 "trap": "H_V 的輸出餵 η′_0；H_S 的輸出（Y(H_S)）只作為 H_V 的訊息與 ticket id 比對。"
},
{
 "id": "ch06-which-eta-where",
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "eq. 6.16–6.18, 6.25, 6.30, 11.22",
 "difficulty": 3, "kind": "concept", "tags": ["safrole", "entropy"],
 "stem": "Each of η′_2 and η′_3 has specific uses in GP 0.8.0. Which assignment is correct?",
 "options": [
  "η′_2: ticket ring-proof context (X_T ⌢ η′_2 ++ r), fallback key sequence F(η′_2, κ′), guarantor assignment shuffle; η′_3: verifying the seal signature context (X_T ⌢ η′_3 ++ i_e or X_F ⌢ η′_3)",
  "η′_2: verifying the seal signature context (X_T ⌢ η′_2 ++ i_e or X_F ⌢ η′_2); η′_3: ticket ring-proof context (X_T ⌢ η′_3 ++ r), fallback key sequence F(η′_3, κ′), guarantor assignment shuffle",
  "η′_1: ticket ring-proof context (X_T ⌢ η′_1 ++ r) and fallback key sequence F(η′_1, κ′); η′_2: verifying the seal signature context (X_T ⌢ η′_2 ++ i_e); η′_3: the guarantor assignment shuffle P(|κ′|, η′_3, τ′)",
  "η′_0: ticket ring-proof context (X_T ⌢ η′_0 ++ r) and the guarantor assignment shuffle; η′_1: fallback key sequence F(η′_1, κ′) and seal verification; η′_2 and η′_3 are kept solely to populate the epoch marker H_E"
 ],
 "answer": 0,
 "optNotes": [
  "提票、fallback 與 guarantor 分配都用 η′_2，驗 seal 用晚一個 epoch 的 η′_3，正是 §6.4 的說法。",
  "方向剛好相反：提票在前用較新的那格，驗 seal 在後才用已 rotate 的最舊那格。",
  "三個用途整組往前挪一格；eq. 11.22 明寫 G ≡ (P(|κ′|, η′_2, τ′), Φ(κ′))，用的是 η′_2。",
  "η′_0 每塊都被 6.23 改寫，拿它當 ring proof context 會使同 epoch 內每塊 context 都不同。",
 ],
 "explanation": "tickets 在 epoch N 提交時用 η′_2（eq. 6.30 的 ring proof context X_T ⌢ η′_2 ++ r）；到 epoch N+1 驗 seal 時，那個值已經被 rotate 成 η′_3（eq. 6.16：X_T ⌢ η′_3 ++ i_e；6.17：X_F ⌢ η′_3），這就是 §6.4 說的「The oldest is used to regenerate this randomness when verifying the seal」。fallback F(η′_2, κ′)（6.25）與 guarantor 分配 P(|κ′|, η′_2, τ′)（11.22）也都用 η′_2；§11.3 解釋不用 η_1 是為了避免 epoch 末尾狀態不確定造成 fork magnification。epoch marker H_E 帶的則是 prior (η_0, η_1)，rotate 後即 η′_1、η′_2。",
 "trap": "口訣：提 ticket 用 η2，驗 seal 用 η3（同一個值晚一個 epoch）。"
},
{
 "id": "ch06-seal-ticket-condition",
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "eq. 6.16 (ticket seal)",
 "difficulty": 3, "kind": "concept", "tags": ["safrole", "seal"],
 "stem": "When γ′_S is a sequence of tickets, the seal H_S must satisfy three conditions (eq. 6.16), with i = γ′_S[H_T mod E]. Which set is exactly right?",
 "options": [
  "i_y = Y(H_S); H_S is a Bandersnatch signature by H_A over context X_T ⌢ η′_3 ++ i_e with message E_U(H) (the unsigned header); and the block is marked T = 1 (ticketed)",
  "i_y = H(H_S), the Blake2b hash of the seal bytes; H_S is a ring-VRF proof against γ′_Z over context X_T ⌢ η′_3 ++ i_e with message E(H) (the full header); and the block is marked T = 1 (ticketed)",
  "i_y = Y(H_S); H_S is a Bandersnatch signature by H_A over context X_T ⌢ η′_2 ++ i_e with message E_U(H) (the unsigned header); and the block is marked T = 1 (ticketed)",
  "i = H_A (the sealer entry is the author's own Bandersnatch key); H_S is a Bandersnatch signature by H_A over context X_F ⌢ η′_3 with message E_U(H) (the unsigned header); and the block is marked T = 0"
 ],
 "answer": 0,
 "optNotes": [
  "三個條件與 eq. 6.16 一字不差：Y(H_S) 對上該 slot 的 ticket id、η′_3 context、T = 1。",
  "6.32 的 ticket id 是 VRF 輸出而非簽章 hash；訊息取完整 E(H) 更是循環定義（header 含 H_S）。",
  "η′_2 是提交 ticket 時的 context；驗 seal 一律用已 rotate 的 η′_3。",
  "那是 eq. 6.17 的 fallback 情況：i = H_A、X_F context、T = 0。",
 ],
 "explanation": "eq. 6.16：γ′_S ∈ [C] ⇒ { i_y = Y(H_S)（seal 的 VRF 輸出必須等於該 slot ticket 的 id，證明出塊者就是持票人）, H_S ∈ F^{X_T ⌢ η′_3 ++ i_e}_{H_A}(E_U(H)), T = 1 }。seal 是一般（IETF）Bandersnatch VRF 簽章，不是 ring VRF——ring 只在提交 ticket 時用；訊息則是省略 seal 欄位的 E_U(H)，否則簽章會簽進自己。你們的 sealing.go ValidateByBandersnatchs 就是檢查 Y(H_S) == ticket id。",
 "trap": "E_U(H) = 不含 H_S 的 header 序列化；H_V 則是 context X_E ⌢ Y(H_S)、訊息為空 []。"
},
{
 "id": "ch06-slot-sealer-cases",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.25",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "fallback"],
 "stem": "The posterior slot-sealer sequence γ′_S has three cases. A block arrives with e′ = e + 1, the previous block was at slot phase m = 480 (< Y = 500) and γ_A holds 600 tickets. What is γ′_S?",
 "options": [
  "Z(γ_A) — the outside-in ordering of the accumulator, because e′ = e + 1 and |γ_A| = E both hold and the m ≥ Y clause constrains m′, the new block's phase, not the prior block's",
  "γ_S — unchanged, because the second case of eq. 6.25 covers any block whose prior still sat inside the same epoch's ticket-submission window, and only m ≥ Y forces a fresh sequence",
  "F(η′_2, κ′) — fallback keys, because eq. 6.25's first case also needs m ≥ Y and the prior block's phase is still inside the ticket-submission window, so the contest never closed",
  "F(η_2, κ) — fallback keys, because m = 480 < Y does select the third case, but F is seeded with the prior η_2 and the prior active set κ that were in force while the previous block was authored"
 ],
 "answer": 2,
 "optNotes": [
  "6.25 的 m 出自 τ（前一塊的 slot phase）；讀成 m′ 會讓本塊自己跨過 Y 就提前開票。",
  "「γ_S 不變」的條件是 e′ = e（同一 epoch），本題 e′ = e + 1 已不適用。",
  "三條件缺一不可：m = 480 < Y = 500，比賽尚未封閉，即使 accumulator 已滿也得走 fallback。",
  "F 的參數必須是 posterior：κ′（= 舊 γ_P）才是本 epoch 的 active set，η′_2 也已 rotate 過。",
 ],
 "explanation": "eq. 6.25：γ′_S ≡ Z(γ_A) 當 e′ = e+1 ∧ m ≥ Y ∧ |γ_A| = E；γ_S 當 e′ = e；否則 F(η′_2, κ′)。三個條件缺一不可，而 m 是 **prior** block 的 slot phase（來自 τ），這個門檻是要確認「比賽在上一塊時就已結束」。同理若跳過整個 epoch（e′ ≥ e+2）也走 fallback。fallback 一律以 posterior 的 η′_2 與 κ′ 為種子。你們 UpdateSlotKeySequence() 的三段 if 完全對應。",
 "trap": "面試愛問邊界：(1) 跳過整個 epoch；(2) accumulator 未滿；(3) 前一塊 m < Y。全部都是 fallback。"
},
{
 "id": "ch06-outside-in-Z",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.26 (Z)",
 "difficulty": 1, "kind": "concept", "tags": ["safrole", "tickets"],
 "stem": "With a tiny epoch of E = 6 and a sorted accumulator γ_A = [a, b, c, d, e, f] (ascending ticket ids), what is Z(γ_A)?",
 "options": [
  "[a, f, b, e, c, d]",
  "[a, b, c, d, e, f]",
  "[f, a, e, b, d, c]",
  "[a, c, e, f, d, b]"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.26 的 [s_0, s_{n−1}, s_1, s_{n−2}, …] 逐項對上。",
  "那是原始的升冪序列，完全沒有做 outside-in 交錯。",
  "頭尾起點反了：Z 從最小 id 起頭，不是從最大的那一張開始。",
  "那是「隔一個取一個」再折返，不是 6.26 的頭尾交錯。",
 ],
 "explanation": "eq. 6.26：Z(s) = [s_0, s_{n−1}, s_1, s_{n−2}, …]，「outside-in」交錯取頭尾。所以 [a,b,c,d,e,f] → [a,f,b,e,c,d]。目的：最佳（最小 id）的 ticket 與最差的 ticket 交錯散佈到整個 epoch，避免某段時間集中由同一批 validator 出塊。你們的 OutsideInSequencer() 用 left/right 兩個指標實作。",
 "trap": "第一個 slot 是最小 id（s_0），第二個是最大 id。"
},
{
 "id": "ch06-epoch-marker",
 "ch": "6", "section": "6.6 The Markers", "gpRef": "eq. 6.28",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "markers"],
 "stem": "What exactly does the epoch marker H_E contain in the first block of a new epoch (e′ > e)?",
 "options": [
  "(η_0, η_1, [(k_b, k_e) | k ∈ γ′_P]) — the prior η_0 and η_1 plus the Bandersnatch and Ed25519 keys of the pending validators γ′_P who take over in the next epoch",
  "(η′_0, η′_1, [(k_b, k_e) | k ∈ κ′]) — the posterior η′_0 and η′_1 plus the Bandersnatch and Ed25519 keys of the validators that have just become active in this epoch",
  "(η_2, η_3, [(k_b, k_e) | k ∈ ι]) — the two oldest historical entropies plus the Bandersnatch and Ed25519 keys of the staging set exactly as the designate host call left it",
  "(η_0, η_1, Z(γ_A)) — the prior η_0 and η_1 plus the outside-in ordered ticket identifiers, one per timeslot, that will seal each slot of the coming epoch"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.28 一字不差：prior (η_0, η_1) 加上已 Φ 過濾的 γ′_P 的 Bandersnatch + Ed25519 key。",
  "η′_0 已摻進本塊的 VRF 輸出；key 來源也錯，marker 預告的是下個 epoch 的 γ′_P 而非 κ′。",
  "(η_2, η_3) 又更舊兩格；未經 Φ 過濾的 ι 會讓 light client 收到尚未歸零的 offender key。",
  "Z(γ_A) 是 winning-tickets marker H_W（6.29）的內容，與 H_E 是 header 裡互斥的兩個欄位。",
 ],
 "explanation": "eq. 6.28：H_E ≡ (η_0, η_1, [(k_b, k_e) | k ∈ γ′_P]) 當 e′ > e，否則 ∅。η_0 與 η_1 是 **prior** 值（rotate 後就是 η′_1、η′_2，也就是下個 epoch 提 ticket 與 fallback 會用到的 entropy），加上 γ′_P（下一個 epoch 的 pending set，已經 Φ 過濾）的 Bandersnatch + Ed25519 key。目的（§6.6）：讓不同步完整 state 的節點（light client）只靠 header 鏈就能追蹤 validator 變化。你們 ValidateHeaderEpochMark（InvalidEpochMark = code 9）檢查此式。",
 "trap": "H_E 放 γ′_P 不是 κ′；entropy 是 prior η_0/η_1。"
},
{
 "id": "ch06-winning-tickets-marker",
 "ch": "6", "section": "6.6 The Markers", "gpRef": "eq. 6.29",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "markers"],
 "stem": "Under which exact condition is the winning-tickets marker H_W non-empty?",
 "options": [
  "e′ = e ∧ m < Y ≤ m′ ∧ |γ_A| = E — the first block of the same epoch whose slot phase crosses the tail start Y, with a saturated accumulator; then H_W = Z(γ_A)",
  "e′ > e ∧ m ≥ Y ∧ |γ_A| = E — the first block of a new epoch, once the previous epoch's tail has been reached and the accumulator is saturated; then H_W = Z(γ_A)",
  "e′ = e ∧ Y ≤ m < m′ ∧ |γ_A| = E — every block of the epoch's tail after ticket submission has already closed, provided the accumulator is saturated; then H_W = Z(γ_A)",
  "e′ = e ∧ m < Y ≤ m′ ∧ |γ_A| ≥ 1 — the first block of the same epoch whose slot phase crosses the tail start Y, with any non-empty accumulator; then H_W = Z(γ_A)"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.29 的三個合取項完全對上：同一 epoch 內跨越 Y 的那一塊，且 accumulator 已飽和。",
  "那組條件描述的其實是 slot-sealer 序列的第一個 case；進入新 epoch 才公告已經太遲。",
  "少了 m < Y 這個下界，整段 tail 每一塊都會重複公告同一份序列。",
  "Z 的定義域是長度 E 的序列；accumulator 未滿時下個 epoch 直接走 fallback。",
 ],
 "explanation": "eq. 6.29：H_W ≡ Z(γ_A) 當 e′ = e ∧ m < Y ≤ m′ ∧ |γ_A| = E，否則 ∅。即「同一 epoch 內，前一塊 phase 在 Y 之前、本塊 phase 在 Y 之後（含）」的那唯一一個區塊，且 accumulator 已飽和，就把下個 epoch 的最終 ticket 序列公告在 header；6.25 則在下個 epoch 的第一塊把同一份序列定案為 γ′_S。注意若 epoch 尾端沒有任何區塊跨越 Y（例如 m = 480 直接跳到下個 epoch），H_W 永遠不會出現。",
 "trap": "H_W 與 H_E 互斥：H_W 要 e′ = e，H_E 要 e′ > e。"
},
{
 "id": "ch06-ticket-extrinsic-limits",
 "ch": "6", "section": "6.7 The Extrinsic and Tickets", "gpRef": "eq. 6.30–6.32",
 "difficulty": 2, "kind": "delta", "tags": ["safrole", "tickets", "delta-0.8.0"],
 "stem": "Per GP 0.8.0, what bounds apply to the tickets extrinsic E_T?",
 "options": [
  "|E_T| ≤ K = 16 when m′ < Y, otherwise |E_T| = 0; each entry index e < n where n = ⌈2E / |γ′_P|⌉ — so 2 in the full configuration (E = 600, |γ′_P| = 1023)",
  "|E_T| ≤ K = 16 in every block including those in the tail; each entry index e < N = 2, a fixed constant that does not depend on the validator-set size (E = 600, |κ| = 1023)",
  "|E_T| ≤ E = 600 summed across the whole epoch rather than per block; each entry index e < n where n = ⌈2E / |γ′_P|⌉ — so 2 in the full configuration (E = 600, |γ′_P| = 1023)",
  "|E_T| ≤ K = 16 when m′ ≤ Y, otherwise |E_T| = 0; each entry index e < n where n = ⌈|γ′_P| / 2E⌉ — so 1 in the full configuration (E = 600, |γ′_P| = 1023)"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.31 的 m′ < Y 與 eq. 6.30 的 n = ⌈2E/|γ′_P|⌉ 都對上，full 配置算出來是 2。",
  "tail 期間必須是空 extrinsic；把上限寫成固定常數 N = 2 也是 0.7.2 的舊寫法。",
  "K 限制的是**單一區塊**的 extrinsic 大小；GP 對整個 epoch 的提交總量沒有直接上限。",
  "m′ = Y 那一塊已在 tail 內；比例倒過來更會變成 validator 越多、每人配額越少。",
 ],
 "explanation": "eq. 6.30：E_T ∈ [(r ∈ N_n, p ∈ ring proof over γ′_Z with context X_T ⌢ η′_2 ++ r)]，n = ⌈2E/|γ′_P|⌉——0.8.0 (#527) 把原本的常數 N 改成公式，「To ensure the accumulator can be saturated, when there are fewer validators, each validator is permitted more tickets」。full：⌈2·600/1023⌉ = 2；test-vector 的 tiny 配置（E = 12、|γ′_P| = 6）：⌈24/6⌉ = 4（0.7.x 的 tiny 常數是 3，這是遷移時要改的點）。eq. 6.31：|E_T| ≤ K = 16 當 m′ < Y，否則必須為 0（tail 期間不能再提 ticket）。",
 "trap": "條件是 m′ < Y（本塊的 phase），K = 16 是每個區塊的上限，不是每個 epoch。"
},
{
 "id": "ch06-ticket-accumulator-rules",
 "ch": "6", "section": "6.7 The Extrinsic and Tickets", "gpRef": "eq. 6.33–6.36",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "tickets"],
 "stem": "Which statement about the new tickets n and the posterior accumulator γ′_A is FALSE?",
 "options": [
  "n must be sorted ascending by ticket id and contain no duplicates, and no id in n may already be in γ_A",
  "γ′_A is the lowest E entries of the sorted union of n and (γ_A, or ∅ if e′ > e)",
  "Every submitted ticket must appear in γ′_A — a ticket that would be evicted by the accumulator's cap is useless and makes the extrinsic invalid",
  "Tickets with higher ids are preferred, so γ′_A keeps the highest E entries"
 ],
 "answer": 3,
 "optNotes": [
  "eq. 6.33 要求依 id 排序且唯一、6.34 要求與 γ_A 不相交——這句是真的。",
  "eq. 6.35 就是這麼寫的：排序後的聯集取最低 E 筆，跨 epoch 時起點換成空序列。",
  "eq. 6.36 的 n ⊆ γ′_A：「It is invalid to include useless tickets in the extrinsic」——真的。",
  "eq. 6.35 留下的是排序後**最低**的 E 個 ticket id，數值小者勝。",
 ],
 "explanation": "eq. 6.33：n 依 id 排序且唯一；6.34：n 的 id 與 γ_A 不相交；6.35：γ′_A = →(sort_by_id(n ∪ (∅ if e′ > e else γ_A)))^E，取的是排序後**最前面**（即最低）的 E 筆，§6.7 原文「the accumulator becomes the lowest items of the sorted union」；6.36：n ⊆ γ′_A，「It is invalid to include useless tickets in the extrinsic」。注意 §6.2 的行文說 γ_A 是「highest-scoring ticket identifiers」——GP 兩處措辭方向相反，實作一律以 6.35 的公式為準。你們 CreateNewTicketAccumulator() 排序後取 [:E]，GetPreviousTicketsAccumulator 在 e′ > e 時回傳空 accumulator。",
 "trap": "「score」= ticket id（VRF 輸出），數值小者勝。"
},
{
 "id": "ch06-ticket-proof-context",
 "ch": "6", "section": "6.7 The Extrinsic and Tickets", "gpRef": "eq. 6.30, 6.32",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "tickets", "vrf"],
 "stem": "A ticket proof p in E_T is a Bandersnatch ring-VRF proof. Against which ring root, with what context, and what is the ticket identifier?",
 "options": [
  "Against γ′_Z (the posterior ring root), context X_T ⌢ η′_2 ++ r, empty message []; the ticket id is the VRF output Y(p)",
  "Against γ_Z (the prior ring root), context X_T ⌢ η′_3 ++ r, message E_U(H) (the unsigned header); the ticket id is the Blake2b hash H(p)",
  "Against the Ed25519 keys of κ′ (the active set), context X_T ⌢ η_0 ++ r, empty message []; the ticket id is the proof p itself",
  "Against γ′_Z (the posterior ring root), context X_E ⌢ Y(H_S), message E_U(H) (the unsigned header); the ticket id is the VRF output Y(p)"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.30 與 6.32 全對上：root 取 γ′_Z、context X_T ⌢ η′_2 ++ r、訊息為空、id = Y(p)。",
  "prior γ_Z 會在 epoch 第一塊整批誤判；綁上 E_U(H) 更失去「先提交、後開票」的性質。",
  "ring 由 γ′_P 的 Bandersnatch key 組成，曲線與集合都不對；proof 可重新隨機化，不能當 id。",
  "X_E ⌢ Y(H_S) 是 H_V 的 context（6.18）；提票的當下根本還沒有 H_S 存在。",
 ],
 "explanation": "eq. 6.30：p ∈ F̄^{X_T ⌢ η′_2 ++ r}_{γ′_Z}([])，ring proof 的驗證 root 是 γ′_Z（若本塊是 epoch 第一塊，γ′_Z 已換成新 pending set 的 root，因此 ticket 會針對**新** ring 驗證）；訊息為空序列；eq. 6.32：ticket id y = Y(p)（VRF 輸出），r 是 entry index。ring proof 讓驗證者知道「某個 γ′_P 成員」擁有此 ticket，但不知道是誰——這正是匿名性的來源。你們 createSignatureContext 就是 \"jam_ticket_seal\" + η′_2(32B) + attempt(1B)。",
 "trap": "ring VRF 用在 ticket；一般 VRF 用在 seal 與 H_V。"
},
{
 "id": "ch06-seal-fallback",
 "ch": "6", "section": "6.4 Sealing", "gpRef": "eq. 6.17–6.18",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "seal", "fallback"],
 "stem": "In fallback mode (γ′_S is a sequence of Bandersnatch keys), which checks apply to the header?",
 "options": [
  "γ′_S[H_T mod E] must equal H_A; H_S is a Bandersnatch signature by H_A with context X_F ⌢ η′_3 over E_U(H); T = 0; and H_V is still required with context X_E ⌢ Y(H_S) over []",
  "γ′_S[H_T mod E] must equal H_A; H_S is a Bandersnatch signature by H_A with context X_F ⌢ η′_2 over E_U(H); T = 0; and H_V is still required with context X_E ⌢ Y(H_S) over E_U(H)",
  "γ′_S[H_T mod E] must equal the author's Ed25519 key; H_S is a ring-VRF proof against γ′_Z with context X_F ⌢ η′_3 over E_U(H); T = 1; and H_V is still required with context X_E ⌢ Y(H_S) over []",
  "γ′_S[H_T mod E] must equal H_A; no seal is required in fallback mode, there being no ticket identifier to bind it to; T = 0; and H_V alone is checked, with context X_E ⌢ η′_3 over []"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 6.17 的三個條件加上 6.18 的 H_V ∈ F^{X_E ⌢ Y(H_S)}_{H_A}([]) 全部對上。",
  "驗 seal 一律用已 rotate 的 η′_3；6.18 的 H_V 訊息是空序列 []，不是 E_U(H)。",
  "三處都錯：γ′_S ∈ [H_B]_E 是 Bandersnatch key 序列，ring proof 只用於提票，fallback 的 T 必為 0。",
  "6.17 仍要求 H_S，否則無從證明作者持有該 slot 指定的 key；H_V 的 context 也是 X_E ⌢ Y(H_S)。",
 ],
 "explanation": "eq. 6.17：γ′_S ∈ [H_B] ⇒ { i = H_A, H_S ∈ F^{X_F ⌢ η′_3}_{H_A}(E_U(H)), T = 0 }。eq. 6.18 對 ticket 與 fallback 兩種模式都適用：H_V ∈ F^{X_E ⌢ Y(H_S)}_{H_A}([])，也就是 entropy 在 fallback 下仍然每塊更新。三個 context 字串：X_F = $jam_fallback_seal、X_T = $jam_ticket_seal、X_E = $jam_entropy。T = 0 表示此塊「安全性較低」，§19 best-chain 規則會偏好 ticket-sealed 祖先較多的鏈。",
 "trap": "fallback 的 entropy 仍然每塊更新（H_V 必填）。"
},
{
 "id": "ch06-code-slot-key-sequence",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.25 — internal/safrole/sealing.go UpdateSlotKeySequence",
 "difficulty": 2, "kind": "code", "tags": ["safrole", "code"],
 "stem": "This is the team's implementation of γ′_S. Which claim about it is correct?",
 "code": {"lang": "go", "caption": "internal/safrole/sealing.go (UpdateSlotKeySequence)", "src": """if ePrime == e+1 && len(gammaA) == types.EpochLength && int(slotIndex) >= types.SlotSubmissionEnd {
    // Z(γa) if e′ = e + 1 ∧ m ≥ Y ∧ |γa| = E
    newGammaS.Tickets = OutsideInSequencer(&gammaA)
} else if ePrime == e { // γs if e′ = e
    newGammaS = cs.GetPriorStates().GetGammaS()
} else { // F(η′2, κ′) otherwise
    newGammaS.Keys = FallbackKeySequence(etaPrime[2], posteriorState.GetKappa())
}
posteriorState.SetGammaS(newGammaS)"""},
 "options": [
  "`slotIndex` is m — the slot phase of the PRIOR block (τ mod E) — and `gammaA` is the prior accumulator; `etaPrime[2]` and `posteriorState.GetKappa()` are posterior values, matching F(η′_2, κ′)",
  "`slotIndex` should be m′ — the phase of the block being imported, H_T mod E — because eq. 6.25 asks whether the contest has closed by the current block; reading the prior block's τ mod E is an off-by-one",
  "The fallback branch should pass the prior κ together with the prior η_2, since the incoming validators only gain authoring rights from the second block of the epoch onwards",
  "The first branch should also fire when ePrime ≥ e + 2 provided |γ_A| = E and m ≥ Y, since accumulated tickets stay valid until they are consumed; restricting it to e + 1 forces fallback needlessly"
 ],
 "answer": 0,
 "optNotes": [
  "6.25 的 m 出自 τ、F 的參數是 posterior，這段程式三處判斷都與公式一致。",
  "換成 m′ 會讓「跨過 Y 的那一塊」立刻開票、少等一整段 tail——6.25 明寫的是 m。",
  "epoch 第一塊完成 6.14 輪換之後，κ′（= 舊 γ_P）才是本 epoch 真正的 active set。",
  "跳過整個 epoch 後 ring root 與 η 都已再度 rotate，那些 ticket 是為 e+1 準備的。",
 ],
 "explanation": "eq. 6.25 的條件是 m ≥ Y，m 是 **prior** block 的 phase（τ 除以 E 的餘數），不是 m′——因為要確認「比賽已在前一塊之前結束」，這正是 fuzzer 愛打的邊界。F 的參數則是 η′_2 與 κ′（posterior）。e′ ≥ e+2（跳過整個 epoch）必須走 fallback，因為 accumulator 裡的 ticket 是為「e+1」那個 epoch 準備的，其 ring proof 針對的是當時的 γ′_Z。",
 "trap": "你們的 OuterUsedSafrole 先做 UpdateEntropy、KeyRotate，再做 UpdateSlotKeySequence——順序正是為了讓 η′_2、κ′ 就位。"
},
{
 "id": "ch06-code-fallback-hash",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.27 — internal/safrole/slot_key_sequence.go",
 "difficulty": 2, "kind": "code", "tags": ["safrole", "code", "fallback"],
 "stem": "Read the team's FallbackKeySequence. Which statement is accurate about its conformance to eq. 6.27?",
 "code": {"lang": "go", "caption": "internal/safrole/slot_key_sequence.go", "src": """for i = 0; i < epochLength; i++ {
    serial := utils.SerializeFixedLength(i, 4)          // E_4(i)
    concatenation := append(entropy[:], serial...)      // r ⌢ E_4(i)
    // H4 : Keccak256(serializedBytes) -> See section 3.8 , take only the first 4 octets of the hash,
    hash := hash.Blake2bHashPartial(concatenation, 4)
    validatorIndex, _ := utils.DeserializeFixedLength(types.ByteSequence(hash), types.U32(4))
    validatorIndex %= (types.U32(types.ValidatorsCount))
    keys[i] = validators[validatorIndex].Bandersnatch
}"""},
 "options": [
  "The hash is right — Blake2b is the GP's H and the first 4 octets are decoded little-endian — but eq. 6.27's cyclic subscript reduces modulo the length of the key sequence passed in, i.e. |κ′|, whereas the code reduces modulo the compile-time constant ValidatorsCount",
  "The hash is wrong — §3.8 reserves H for Blake2b-256 but eq. 6.27 calls for H_K, Keccak-256, exactly as the surviving comment says — while the modulus is right, since the cyclic subscript reduces over the fixed validator count that ValidatorsCount holds",
  "The slice is wrong — eq. 6.27's subscript takes the LAST four octets of H(r ⌢ E_4(i)) and decodes them big-endian, so Blake2bHashPartial(·, 4) reads the wrong end — while the modulus over ValidatorsCount matches the equation's cyclic subscript exactly",
  "The reduction is spurious — decode_4 of four Blake2b octets already lands inside N_E and eq. 6.27 carries no modulus at all, so `%= ValidatorsCount` is an invented step that can map two distinct slots onto the same validator and break one-slot-one-author"
 ],
 "answer": 0,
 "optNotes": [
  "Blake2b 與「前 4 octets、小端」都對；問題在 `%= ValidatorsCount` 用編譯期常數而非 len(κ′)。",
  "被 stale 註解帶偏：§3.8 的 H 就是 Blake2b-256，而對固定 validator 數取模在 0.8.0 也不成立。",
  "兩處都錯：s_{…4} 取的是**前** 4 個元素，且 decode 與 E_n 一律小端。",
  "忽略了 6.27 外層的 ⟲：decode_4 的值域是 0…2³²−1，不取模必然越界。",
 ],
 "explanation": "eq. 6.27：k[decode_4(H(r ⌢ E_4(i))_{…4})]_b，外面套 ⟲（cyclic 索引）——也就是對**傳入的 key 序列長度** |k| = |κ′| 取模。H 是 Blake2b（§3.8：H ≡ Blake2b-256；H_K 才是 Keccak，只用在 accumulation-output belt 與 BEEFY）。這段 code 有兩個要點：(1) 註解寫 Keccak256 是 stale，實際呼叫的是 Blake2bHashPartial，行為正確；(2) `%= types.ValidatorsCount` 用的是編譯期常數，在 0.7.2（|κ| 恆等於 V）沒問題，但 0.8.0 允許 |κ| 變動後就必須改成 len(κ′)——這正是 issue #1037 要處理的一類問題。順帶一提，取模讓不同 slot 撞到同一個 validator 是 fallback 的正常行為而非缺陷——F 本來就是可重複抽樣。",
 "trap": "面試官可能直接問：你們 fallback 用哪個 hash？答 Blake2b，並指出註解錯誤。"
},
{
 "id": "ch06-code-entropy-order",
 "ch": "6", "section": "6.4 Sealing and Entropy", "gpRef": "eq. 6.23–6.24 — internal/safrole/sealing.go UpdateEntropy",
 "difficulty": 2, "kind": "code", "tags": ["safrole", "code", "entropy"],
 "stem": "In the team's UpdateEntropy, why is `eta[0]` overwritten with the posterior η′_0 AFTER the rotation loop, and what would go wrong if the loop ran after UpdateEtaPrime0 wrote into the same array?",
 "code": {"lang": "go", "caption": "internal/safrole/sealing.go", "src": """eta := cs.GetPriorStates().GetEta()
if ePrime > e {
    for i := 2; i >= 0; i-- {
        eta[i+1] = eta[i]          // (η′1, η′2, η′3) = (η0, η1, η2)
    }
}
// This make sure we won't overwrite eta0
eta[0] = cs.GetPosteriorStates().GetEta0()
cs.GetPosteriorStates().SetEta(eta)"""},
 "options": [
  "Because eq. 6.24 rotates the PRIOR η_0 into η′_1; if η′_0 (already hashed with this block's VRF output) were rotated instead, η′_1 would wrongly include the current block's entropy",
  "Because eq. 6.24 re-seeds the accumulator on an epoch change: η′_0 has to be reset after the rotation so the new epoch starts from a clean value, which is exactly what writing eta[0] last achieves",
  "Because the descending loop is what stops η_0 from being copied into all three history slots; the write to eta[0] is independent of eq. 6.24 and could equally well run before the rotation",
  "Because eq. 6.24 is stated over posterior values, (η′_1, η′_2, η′_3) = (η′_0, η′_1, η′_2), so η′_0 must be settled first and the assignment after the loop is a compensating fix-up for the wrong order"
 ],
 "answer": 0,
 "optNotes": [
  "6.24 右側全是 prior 值；先寫 η′_0 會讓 η′_1 變成 H(η_0 ⌢ Y(H_V))，混進本塊的 entropy。",
  "GP 沒有這個依據：6.23 每一塊都照 H(η_0 ⌢ Y(H_V)) 更新，epoch 邊界也不例外。",
  "正好說反：倒序確實避免了覆蓋，但**寫入時機**才是這段程式的核心。",
  "6.24 右邊是 (η_0, η_1, η_2) 三個 prior 值；照 posterior 遞推會讓三格歷史被同一值填滿。",
 ],
 "explanation": "eq. 6.24：(η′_1, η′_2, η′_3) ≡ (η_0, η_1, η_2)——右側全是 **prior** 值。η′_0 = H(η_0 ⌢ Y(H_V))（6.23）則已經包含本塊的 VRF 輸出。若先把 η′_0 寫進 eta[0] 再 rotate，η′_1 會變成 H(η_0 ⌢ Y(H_V))，導致下個 epoch 的 ticket context（用 η′_2）與 fallback 都算錯，state root 立刻 mismatch。這種「prior vs posterior」的細節正是 fuzzer 最常抓到的 bug 類型。",
 "trap": "所有 Safrole 式子都要先問：右邊是 prior 還是 posterior？"
},
]
