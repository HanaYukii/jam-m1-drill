# -*- coding: utf-8 -*-
# Chapter 6 — Block Production and Chain Growth (Safrole), GP 0.8.0
ITEMS = [
{
 "id": "ch06-gamma-components",
 "ch": "6", "section": "6.2 Safrole Basic State", "gpRef": "eq. 6.3–6.6",
 "difficulty": 1, "kind": "concept", "tags": ["safrole", "state"],
  "stemZh": "Safrole 狀態 γ ≡ (γ_P, γ_Z, γ_S, γ_A)。哪一個描述是正確的？",
  "optionsZh": [
   "γ_P 是下個 epoch 的 pending validator 金鑰；γ_Z 是對 γ_P 取的 Bandersnatch ring root；γ_S 是本 epoch 的 slot-sealer 序列（E 張 ticket 或 E 把金鑰）；γ_A 是供下個 epoch 用的 ticket accumulator（至多 E 張）",
   "γ_P 是上個 epoch 的 validator 金鑰（也就是 λ 集合）；γ_Z 是對 active set κ 取的 Bandersnatch ring root；γ_S 是本 epoch 的 slot-sealer 序列（E 張 ticket 或 E 把金鑰）；γ_A 是供下個 epoch 用的 ticket accumulator（至多 E 張）",
   "γ_P 是下個 epoch 的 pending validator 金鑰；γ_Z 是對 γ_P 取的 **Ed25519** ring root；γ_S 是供下個 epoch 用的 ticket accumulator（至多 E 張）；γ_A 是本 epoch 的 slot-sealer 序列（E 張 ticket 或 E 把金鑰）",
   "γ_P 是供下個 epoch 用的 ticket accumulator（至多 E 張）；γ_Z 是對 γ_P 取的 Bandersnatch ring root；γ_S 是本 epoch 的 slot-sealer 序列（E 張 ticket 或 E 把金鑰）；γ_A 是 pending validator 金鑰，並在每個 epoch 開始時重設為 ι"
  ],
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
  "stemZh": "在 epoch 換屆（e′ > e）時，依 eq. 6.14，validator 的金鑰集合是怎麼輪替的？",
  "optionsZh": [
   "(γ′_P, κ′, λ′, γ′_Z) = (Φ(ι), γ_P, κ, z)，其中 z 是對 γ′_P 的 Bandersnatch 金鑰取的 ring root，而 Φ 會把任何 Ed25519 金鑰落在 ψ′_O 裡的 validator 整組金鑰歸零",
   "(γ′_P, κ′, λ′, γ′_Z) = (ι, γ_P, κ, z)，其中 z 是對 γ′_P 的 Bandersnatch 金鑰取的 ring root，且不做任何 offender 過濾——offender 是之後在 guarantor 指派時才被跳過的",
   "(γ′_P, κ′, λ′, γ′_Z) = (Φ(ι), ι, κ, z)，其中 z 是對 **κ′** 的 Bandersnatch 金鑰取的 ring root，而 Φ 歸零的是 **prior** 的 ψ_O 而非 posterior 集合裡的 offender",
   "(γ′_P, κ′, λ′, γ′_Z) = (Φ(γ_P), κ, λ, γ_Z)，ring root 只在 ι 改變時才重算，而 Φ 歸零的是 ψ′_O 裡的 offender——這些序列每個區塊都前進一步"
  ],
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
 "explanation": "eq. 6.14：e′ > e 時 (γ′_P, κ′, λ′, γ′_Z) = (Φ(ι), γ_P, κ, z)，其 where 子句定義 z = ringroot([k_b | k ∈ γ′_P])；非 epoch 邊界則四者原封不動。**四組金鑰是一條輸送帶**：ι staging（服務透過 `designate` 寫入）→ γ_P pending（下個 epoch 生效，決定 ring root）→ κ active（現在出塊、擔保、背書的就是這組）→ λ previous（上一個 epoch，仍需保留以驗證跨界的舊簽章）。**所以 ι 要等兩個 epoch 邊界才會真正上場**（ι → γ_P → κ），這個延遲是刻意的：ring root 必須在整個 epoch 之前就固定下來，ticket 才有東西可以證明自己屬於某個 ring。**Φ 的角色**（eq. 6.15）：把 k_e ∈ ψ′_O 的 validator **整筆 336 位元組換成全零**，而不是從序列中移除。用 posterior 的 ψ′_O 是因為 disputes 在同一塊裡已經先處理完。**歸零而非移除很重要**：|κ| ≡ |λ| ≡ V 因此恆成立，索引不會位移——H_I 才能一直當索引用，π_V 的統計陣列也不必重排。你們的 KeyRotate() 對應此式，ReplaceOffenderKeys 取的是 posterior ψ_O。",
 "trap": "常考：ι 什麼時候變成 κ？答：下下個 epoch（先進 γ_P，再進 κ）。"
},
{
 "id": "ch06-valcount",
 "ch": "6", "section": "6.3 Key Rotation", "gpRef": "eq. 6.7–6.8 (valcount)",
 "difficulty": 2, "kind": "delta", "tags": ["safrole", "validators", "delta-0.8.0"],
  "stemZh": "GP 0.8.0（PR #514）把 validator 集合的大小一般化了。ι、γ_P、κ 與 λ 允許哪些大小？",
  "optionsZh": [
   "永遠恰好 1023 位 validator——這個大小是固定常數 3·C，其中 C = 341 個 core",
   "6 到 1023 之間的任何大小（含端點），沒有整除規則（N_V ≡ N_{6..3·C+1}）",
   "6 到 3·C = 1023 之間任何 3 的倍數（含端點）（N_V ≡ {3c | c ∈ N_{2..C+1}}）",
   "3 到 3·C − 3 = 1020 之間任何 3 的倍數（含端點）（N_V ≡ {3c | c ∈ N_{1..C}}）"
  ],
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
 "explanation": "eq. 6.8：𝕍 ≡ {3c | c ∈ N_{2…C+1}}——**3 的倍數，從 6 到 3C = 1023**（C = 341 是 core 數）。§6.3 原文：「The length of each sequence is always a multiple of 3 between 6 and 3C.」**為什麼一定是 3 的倍數**：每個 active core 需要 3 名 guarantor，所以 validator 數與 core 數是 3:1 的關係，只有前 |κ′| / 3 個 core 會被指派工作（§11.3）。tiny 設定 |κ| = 6 就只有 2 個 core 在動。**這是 0.7.2 → 0.8.0 的重大變化（PR #514）**：原本 V 是一個常數，現在集合大小可變，於是一整批原本寫死的數字都得改成依 |κ| 計算——super-majority 門檻 ⌊2|κ|/3⌋+1、每位 validator 的 ticket 配額 n = ⌈2E/|γ′_P|⌉、erasure coding 的 shard 數 = |κ′|、verdict 的三個門檻（⌊2|k|/3⌋+1、0、⌊|k|/3⌋）。`designate` host call 也只檢查 z ∈ 𝕍，不再比對某個常數。**遷移時最容易漏的**就是散在各處的 `ValidatorsCount` 編譯期常數（你們的 issue #1037 在追這件事）——它們在 0.7.2 都成立，因為那時 |κ| 恆等於 V；0.8.0 之後必須換成 len(κ′)。注意 Φ 把 offender 歸零而非移除，所以 |κ| 在 epoch 內不會變動，只在換屆時才可能改變。",
 "trap": "tiny 模式 V=6、C=2；full V=1023、C=341（1023 = 3·341）。"
},
{
 "id": "ch06-validator-key-layout",
 "ch": "6", "section": "6.3 Key Rotation", "gpRef": "eq. 6.9–6.13",
 "difficulty": 1, "kind": "concept", "tags": ["safrole", "validators", "codec"],
  "stemZh": "一把 validator 金鑰 K 是 336 位元組的序列。它的版面配置是什麼？",
  "optionsZh": [
   "Bandersnatch 32 | Ed25519 32 | BLS 144 | metadata 128",
   "Ed25519 32 | Bandersnatch 32 | BLS 96 | metadata 176",
   "Bandersnatch 32 | BLS 144 | Ed25519 32 | metadata 128",
   "Bandersnatch 33 | Ed25519 32 | BLS 143 | metadata 128"
  ],
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
 "explanation": "§6.3：驗證者金鑰集合 𝕂 ≡ B_336，也就是一段 336 位元組的 blob；GP 為了好指涉才把它切成四塊（eq. 6.9–6.13）：k_b = k[0…32) Bandersnatch、k_e = k[32…+32) Ed25519、k_l = k[64…+144) BLS、k_m = k[208…+128) metadata。32 + 32 + 144 + 128 = 336。**四把鑰匙各司其職**：Bandersnatch 用在出塊——seal H_S 與 ticket 的 ring-VRF proof 都是它；Ed25519 用在「表態」類簽章——guarantee、assurance、judgment 都是；BLS 用在 Beefy，是對外橋接時要驗的那把；metadata 則完全不參與密碼學，GP 說它是「an opaque octet sequence, but utilized to specify practical identifiers for the validator, not least a hardware address」，也就是放網路位址這類實務資訊。**為什麼要記得切點**：其一，epoch 的 ring root 只取每筆的前 32 位元組——eq. 6.14 的 where 子句定義 z = ringroot([k_b | k ∈ γ′_P])（z 本身沒有獨立編號），拿錯 offset 整個 root 就對不上。其二，offender 的處置是「就地歸零」而不是移除：eq. 6.15 的 Φ 把整筆 336 位元組換成全 0，所以 |κ| ≡ |λ| ≡ V 永遠成立，索引不會位移（H_I 才能一直當索引用）。相關名詞：ι staging（待命）、γ_P pending（下個 epoch 生效、決定 ring root）、κ active（現行）、λ previous（上一個 epoch）。",
 "trap": "BLS 144 octets（BLS12-381 上的 key 組合）。metadata 不參與任何密碼學運算。"
},
{
 "id": "ch06-entropy-update",
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "eq. 6.22–6.24",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "entropy"],
  "stemZh": "熵累積器 η 在每個區塊、以及在 epoch 換屆時是怎麼更新的？",
  "optionsZh": [
   "每個區塊 η′_0 = H(η_0 ⌢ Y(H_V))，把熵 VRF 的**輸出**混進去；在 e′ > e 時另外做 (η′_1, η′_2, η′_3) = (η_0, η_1, η_2)，否則 (η_1, η_2, η_3) 不變",
   "每個區塊 η′_0 = H(η_0 ⌢ H_V)，雜湊的是整個 VRF **簽章**而不是它的 32 位元組輸出；在 e′ > e 時另外做 (η′_1, η′_2, η′_3) = (η_0, η_1, η_2)，否則不變",
   "每個區塊 η′_0 = H(η_0 ⌢ Y(H_S))，把 **seal** 的 VRF 輸出混進去；在 e′ > e 時另外做 (η′_1, η′_2, η′_3) = (η′_0, η_1, η_2)，把 posterior 的累積器推進歷史",
   "每個區塊 η′_0 = H(η_0 ⌢ Y(H_V))；而歷史也**每個區塊**都輪替，所以 (η′_1, η′_2, η′_3) = (η_0, η_1, η_2) 無條件成立，η_3 永遠是三個區塊以前的值"
  ],
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
 "explanation": "兩條式子分工明確。**eq. 6.23（每塊都做）**：η′_0 ≡ H(η_0 ⌢ Y(H_V))——把 **prior** 的 η_0 接上本塊 entropy VRF 簽章的輸出 Y(H_V) 再 Blake2b。Y(·) 是附錄 G 定義的 VRF output（簽章的前 32 個位元組），不是簽章本身。**eq. 6.24（只在 e′ > e 做）**：(η′_1, η′_2, η′_3) = (η_0, η_1, η_2)——整體右移一格，**推進去的是 prior 的 η_0**，不是剛算好的 η′_0。這個 prior/posterior 的區分是實作最常翻車的地方。**為什麼這樣就不可偏置（bias-resistant）**：H_V 的簽章 context 是 X_E ⌢ Y(H_S)（eq. 6.18），也就是綁在 seal 的 VRF 輸出上——而 seal 又必須簽 E_U(H)，訊息在產生熵之前就已經固定。出塊者無法試很多份 header 挑一個對自己有利的熵，因為換內容就換 seal、換 seal 就整組重來，且輸出是確定性的。**Y(H_S) 本身不直接進 η**，它只當 H_V 的 context、並在票券模式下與 ticket id 比對。四個 η 的用途分工：η_0 每塊更新的活水；η′_2 供本 epoch 抽籤（ticket context、fallback、guarantor 洗牌）；η′_3 供驗證 seal。你們的 UpdateEtaPrime0() 與 UpdateEntropy() 分別對應 6.23 與 6.24。",
 "trap": "H_V 的輸出餵 η′_0；H_S 的輸出（Y(H_S)）只作為 H_V 的訊息與 ticket id 比對。"
},
{
 "id": "ch06-which-eta-where",
  "alsoCh": ["11"],
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "eq. 6.16–6.18, 6.25, 6.30, 11.22",
 "difficulty": 3, "kind": "concept", "tags": ["safrole", "entropy"],
  "stemZh": "在 GP 0.8.0 中，η′_2 與 η′_3 各有特定的用途。哪一組對應是正確的？",
  "optionsZh": [
   "η′_2：ticket 的 ring-proof context（X_T ⌢ η′_2 ++ r）、fallback 金鑰序列 F(η′_2, κ′)、guarantor 指派的洗牌；η′_3：驗證 seal 簽章的 context（X_T ⌢ η′_3 ++ i_e 或 X_F ⌢ η′_3）",
   "η′_2：驗證 seal 簽章的 context（X_T ⌢ η′_2 ++ i_e 或 X_F ⌢ η′_2）；η′_3：ticket 的 ring-proof context（X_T ⌢ η′_3 ++ r）、fallback 金鑰序列 F(η′_3, κ′)、guarantor 指派的洗牌",
   "η′_1：ticket 的 ring-proof context（X_T ⌢ η′_1 ++ r）與 fallback 金鑰序列 F(η′_1, κ′)；η′_2：驗證 seal 簽章的 context（X_T ⌢ η′_2 ++ i_e）；η′_3：guarantor 指派的洗牌 P(|κ′|, η′_3, τ′)",
   "η′_0：ticket 的 ring-proof context（X_T ⌢ η′_0 ++ r）與 guarantor 指派的洗牌；η′_1：fallback 金鑰序列 F(η′_1, κ′) 與 seal 的驗證；η′_2 與 η′_3 只用來填 epoch marker H_E"
  ],
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
 "explanation": "記法是**「同一份隨機性在不同時間點有不同名字」**：η 每個 epoch 邊界右移一格，所以今天的 η′_2 就是明天的 η′_3。**η′_2 用於「本 epoch 要抽的籤」**：ticket 的 ring-proof context X_T ⌢ η′_2 ++ r（eq. 6.30）、fallback 金鑰序列 F(η′_2, κ′)（eq. 6.25／6.27）、以及 guarantor 對 core 的分配洗牌 P(|κ′|, η′_2, τ′)（eq. 11.22）。**η′_3 用於「驗證上一輪抽籤的結果」**：seal 的 context——票券模式 X_T ⌢ η′_3 ++ i_e（eq. 6.16）、fallback 模式 X_F ⌢ η′_3（eq. 6.17）。**兩者為什麼必須是同一個值的不同時期**：ticket 在 epoch N 提交時用 η′_2 當 context，到 epoch N+1 出塊驗 seal 時，那個值已經 rotate 成 η′_3——§6.4 說得很直接：「The oldest is used to regenerate this randomness when verifying the seal」。用錯就會驗不過，而且只在 epoch 交界才爆，單機測試常常看不出來。**為什麼不用更新的 η_1**：§11.3 解釋是為了避免 fork magnification——η_1 在 epoch 末尾仍可能因為分叉而不確定，拿它當分配依據會讓分叉自我放大。**epoch marker 帶的是 prior 的 (η_0, η_1)**，rotate 之後正好成為 η′_1 與 η′_2，供輕客戶端接續使用。",
 "trap": "口訣：提 ticket 用 η2，驗 seal 用 η3（同一個值晚一個 epoch）。"
},
{
 "id": "ch06-seal-ticket-condition",
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "eq. 6.16 (ticket seal)",
 "difficulty": 3, "kind": "concept", "tags": ["safrole", "seal"],
  "stemZh": "當 γ′_S 是一串 ticket 時，seal H_S 必須滿足三個條件（eq. 6.16），其中 i = γ′_S[H_T mod E]。哪一組完全正確？",
  "optionsZh": [
   "i_y = Y(H_S)；H_S 是由 H_A 對 context X_T ⌢ η′_3 ++ i_e、訊息為 E_U(H)（未含 seal 的 header）所做的 Bandersnatch 簽章；而且該區塊被標記為 T = 1（ticketed）",
   "i_y = H(H_S)，也就是 seal 位元組的 Blake2b 雜湊；H_S 是對 γ′_Z 的 ring-VRF 證明，context 為 X_T ⌢ η′_3 ++ i_e、訊息為 E(H)（完整 header）；而且該區塊被標記為 T = 1（ticketed）",
   "i_y = Y(H_S)；H_S 是由 H_A 對 context X_T ⌢ **η′_2** ++ i_e、訊息為 E_U(H)（未含 seal 的 header）所做的 Bandersnatch 簽章；而且該區塊被標記為 T = 1（ticketed）",
   "i = H_A（該 sealer 項目就是出塊者自己的 Bandersnatch 金鑰）；H_S 是由 H_A 對 context X_F ⌢ η′_3、訊息為 E_U(H) 所做的 Bandersnatch 簽章；而且該區塊被標記為 T = 0"
  ],
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
 "explanation": "eq. 6.16（票券模式，i = γ′_S[H_T mod E]）三個條件：**i_y = Y(H_S)**——seal 的 VRF 輸出必須等於該 slot 那張 ticket 的 id；**H_S ∈ F^{X_T ⌢ η′_3 ++ i_e}_{H_A}(E_U(H))**——用 H_A 簽的 Bandersnatch 簽章；**T = 1**（標記為 ticketed）。**第一個條件是整個 Safrole 的樞紐**：ticket id 當初是持票人用 ring-VRF 產生的 VRF 輸出，只有握有那把私鑰的人能在出塊時再產生同樣的輸出。所以 i_y = Y(H_S) 這一行同時證明了「你就是當初買下這個 slot 的人」，而**不必揭露你是誰**——匿名性正是在這裡兌現的。**兩個常見誤解**：其一，**seal 是一般的 IETF Bandersnatch VRF 簽章，不是 ring VRF**——ring 只在提交 ticket（eq. 6.30）時用；出塊當下驗證者已經能從 κ′[H_I] 拿到公鑰，不需要匿名集合。其二，簽的訊息是 **E_U(H)**（省略 H_S 欄位的 header 編碼），否則簽章會簽進自己、無解。context 裡的 η′_3 是專供 seal 驗證的那份 entropy，i_e 是 ticket 的 entry index。",
 "trap": "E_U(H) = 不含 H_S 的 header 序列化；H_V 則是 context X_E ⌢ Y(H_S)、訊息為空 []。"
},
{
 "id": "ch06-slot-sealer-cases",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.25",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "fallback"],
  "stemZh": "posterior 的 slot-sealer 序列 γ′_S 有三種情形。現在來了一個區塊，e′ = e + 1、前一塊的 slot phase m = 480（< Y = 500）、而 γ_A 持有 600 張 ticket。γ′_S 是什麼？",
  "optionsZh": [
   "Z(γ_A)——accumulator 的 outside-in 排序，因為 e′ = e + 1 與 |γ_A| = E 都成立，而 m ≥ Y 那個子句約束的是新區塊的 phase m′、不是前一塊的",
   "γ_S——維持不變，因為 eq. 6.25 的第二種情形涵蓋任何其前一塊仍位於同一個 epoch 之投票期內的區塊，只有 m ≥ Y 才會逼出一份新序列",
   "F(η′_2, κ′)——fallback 金鑰，因為 eq. 6.25 的第一種情形還需要 m ≥ Y，而前一塊的 phase 仍在 ticket 投票期之內，所以那場競賽從未收尾",
   "F(η_2, κ)——fallback 金鑰，因為 m = 480 < Y 確實選中第三種情形，但 F 的種子是前一塊出塊當時生效的 prior η_2 與 prior active set κ"
  ],
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
 "explanation": "eq. 6.25 三個分支：γ′_S ≡ Z(γ_A) 當 **e′ = e + 1 ∧ m ≥ Y ∧ |γ_A| = E**；γ_S（原封不動）當 e′ = e；其餘走 F(η′_2, κ′)。本題給的是 e′ = e + 1 ✓、|γ_A| = 600 = E ✓，但 m = 480 < Y = 500 ✗——**三個條件缺一不可**，所以落到 fallback。**m 是誰的 phase 是這題的核心**：m 來自 τ（**prior** block 的時槽），m′ 才是本塊的。用 prior 的 phase 當門檻，是要確認「投票在上一塊的時候就已經結束」；本題的情境正是 epoch 在票還沒截止時就結束了——比賽從未收尾，自然不能拿 accumulator 當結果。**同理 e′ ≥ e + 2（整個 epoch 被跳過）也走 fallback**：那批 ticket 是為 e + 1 準備的，其 ring proof 對應的是當時的 γ_Z，中間隔一個 epoch 之後 ring root 與 entropy 都已再度輪替。**fallback 的種子一律是 posterior**：F(η′_2, κ′)——因為 epoch 第一塊會先完成 eq. 6.14 的金鑰輪換與 entropy rotate。相關名詞：Y = 500 是投票截止的 phase（epoch tail start）、E = 600 是 epoch 長度、Z 是 outside-in sequencer（eq. 6.26）、F 是 fallback key sequence（eq. 6.27）。",
 "trap": "面試愛問邊界：(1) 跳過整個 epoch；(2) accumulator 未滿；(3) 前一塊 m < Y。全部都是 fallback。"
},
{
 "id": "ch06-outside-in-Z",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.26 (Z)",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "tickets"],
  "stemZh": "ticket accumulator γ_A 保留 id 最小的 E 張 ticket 並依升冪排序，而 eq. 6.25 讓下個 epoch 的 slot-sealer 序列成為 Z(γ_A)。一張存活下來的 ticket，其排名如何對應到它可以封印的時槽？",
  "optionsZh": [
   "最小的 id 封印第一個時槽、最大的封印第二個、第二小的封印第三個，依此類推：Z 同時從排序好的序列兩端往內取，所以排名的兩個極端會並排坐在 epoch 的開頭",
   "排名順序與時槽順序一致，因為 accumulator 在插入時就已排序；Z 只對 fallback 序列有意義，而後者由熵導出、抵達時本來就毫無順序可言",
   "最大的 id 封印第一個時槽、最小的封印第二個，所以 Z 一樣是從兩端往內取，只是從排名的另一端開始而不是從頭開始",
   "排名被交替發配到 epoch 的兩半，所以最小的 id 封印第一個時槽、次小的封印中間那個時槽、第三小的封印第二個，如此橫跨兩半交錯下去"
  ],
  "stem": "The ticket accumulator γ_A retains the E lowest ticket identifiers in ascending order, and eq. 6.25 makes the next epoch's slot-sealer sequence Z(γ_A). How does a surviving ticket's rank in that ordering map to the slot it gets to seal?",
 "options": [
  "The lowest identifier seals the first slot, the highest the second, the second-lowest the third, and so on: Z consumes the sorted sequence from both ends inward at once, so the two extremes of the ranking sit side by side at the head of the epoch.",
  "Rank order and slot order coincide, because the accumulator is already sorted on insertion; Z matters only for the fallback sequence, which is derived from entropy and therefore arrives in no particular order at all.",
  "The highest identifier seals the first slot and the lowest the second, so Z still consumes the sorted sequence from both ends inward but begins at the far end of the ranking rather than at its start.",
  "Ranks are dealt alternately into the epoch's two halves, so the lowest identifier seals the first slot, the next lowest the middle slot, the third lowest the second slot, and so on across both halves."
 ],
 "answer": 0,
 "explanation": "eq. 6.26：Z(s) = [s_0, s_{|s|−1}, s_1, s_{|s|−2}, …]——從排序好的序列頭尾交替往內取。「rank」的來源是 §6：accumulator「becomes the lowest items of the sorted union of tickets from prior accumulator and the submitted tickets」，即依 ticket id 升冪、只留最小的 E 張。所以 rank 0 → slot 0、rank E−1 → slot 1、rank 1 → slot 2……分數順序決定的是**誰入選**，slot 位置則是那個順序的頭尾交錯，兩者不是同一回事。同一個 Z 在本章出現兩次：eq. 6.25 用它產生 γ′_S（e′ = e+1 ∧ m ≥ Y ∧ |γ_A| = E）；winning-tickets marker H_W 則在 e′ = e ∧ m < Y ≤ m′ ∧ |γ_A| = E 時帶同一個 Z(γ_A)——marker 先把下個 epoch 要用的序列公告出來，兩處必須逐項一致，方向算反就會踩到 InvalidTicketsMark（團隊 issue #770）。需要說明的是：**GP 只定義 Z，並沒有交代為什麼要 outside-in**，safrole.tex 只寫「we use Z as the outside-in sequencer function」，所以口試時講定義與用途即可，不必編一個抗攻擊的理由。",
 "optNotes": [
  "eq. 6.26 從頭尾交替往內取，所以最小與最大的 id 相鄰坐在 epoch 開頭的兩個 slot。",
  "γ_A 已排序不代表 Z 是恆等函數；eq. 6.25 對滿的 accumulator 一樣要套 Z，fallback 走的是 F 不是 Z。",
  "方向反了：eq. 6.26 的第一項是 s_0（最小 id），最大的那張排第二。",
  "那是把序列切兩半交錯，不是頭尾往內收；Z 的第二項取的是整個序列的最後一個。"
 ],
 "trap": "Z 決定的是 slot 位置，不是誰入選；入選由 id 最小的 E 張決定。GP 未解釋為何要 outside-in。"
},
{
 "id": "ch06-epoch-marker",
 "ch": "6", "section": "6.6 The Markers", "gpRef": "eq. 6.28",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "markers"],
  "stemZh": "在一個新 epoch 的第一塊（e′ > e）中，epoch marker H_E 究竟包含什麼？",
  "optionsZh": [
   "(η_0, η_1, [(k_b, k_e) | k ∈ γ′_P])——prior 的 η_0 與 η_1，加上將在下個 epoch 接手的 pending validator γ′_P 的 Bandersnatch 與 Ed25519 金鑰",
   "(η′_0, η′_1, [(k_b, k_e) | k ∈ κ′])——posterior 的 η′_0 與 η′_1，加上剛在本 epoch 變為 active 的那批 validator 的 Bandersnatch 與 Ed25519 金鑰",
   "(η_2, η_3, [(k_b, k_e) | k ∈ ι])——兩個最舊的歷史熵，加上 staging 集合的 Bandersnatch 與 Ed25519 金鑰，內容就是 designate host call 留下的樣子",
   "(η_0, η_1, Z(γ_A))——prior 的 η_0 與 η_1，加上以 outside-in 排序的 ticket 識別碼，每個時槽一張，用來封印接下來那個 epoch 的每一槽"
  ],
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
 "explanation": "eq. 6.28：H_E ≡ (η_0, η_1, [(k_b, k_e) | k ∈ γ′_P]) 當 e′ > e，否則 ∅。**兩個 entropy 是 prior 值**——注意是 η_0 與 η_1 不是 η′。rotate 之後它們就變成 η′_1 與 η′_2，而 η′_2 正是下個 epoch 提交 ticket 的 context 種子（eq. 6.30）與 fallback F 的種子（eq. 6.27）。換句話說，marker 提前把「下個 epoch 抽籤要用的隨機性」公告出來。**金鑰是 γ′_P（pending set）的**，也就是**再下一個** epoch 才會 active 的那組（ι → γ_P → κ 的中段），而且已經被 Φ 過濾（offender 的位置是全零）。每筆帶 Bandersnatch 與 Ed25519 兩把（Ed25519 是 0.6.4 起加入的）。**用途**（§6.6）：讓不同步完整狀態的節點只靠 header 鏈就能追蹤 validator 集合的變化——它需要 Bandersnatch 來驗未來的 seal、需要 Ed25519 來驗 guarantee 與 judgment 簽章，所以兩把都給。**為什麼不給 BLS**：BLS 只用於 Beefy 的鏈下分發，跟「跟著 header 走」無關，給了是浪費頻寬。你們的 ValidateHeaderEpochMark（InvalidEpochMark = code 9）檢查此式。",
 "trap": "H_E 放 γ′_P 不是 κ′；entropy 是 prior η_0/η_1。"
},
{
 "id": "ch06-winning-tickets-marker",
 "ch": "6", "section": "6.6 The Markers", "gpRef": "eq. 6.29",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "markers"],
  "stemZh": "winning-tickets marker H_W 在什麼樣的確切條件下才非空？",
  "optionsZh": [
   "e′ = e ∧ m < Y ≤ m′ ∧ |γ_A| = E——同一個 epoch 內、其 slot phase 首次跨越 tail 起點 Y 的那一塊，且 accumulator 已飽和；此時 H_W = Z(γ_A)",
   "e′ > e ∧ m ≥ Y ∧ |γ_A| = E——新 epoch 的第一塊，只要上個 epoch 的 tail 已經到達且 accumulator 已飽和；此時 H_W = Z(γ_A)",
   "e′ = e ∧ Y ≤ m < m′ ∧ |γ_A| = E——ticket 投票已經關閉之後、該 epoch tail 期間的**每一塊**，只要 accumulator 已飽和；此時 H_W = Z(γ_A)",
   "e′ = e ∧ m < Y ≤ m′ ∧ |γ_A| ≥ 1——同一個 epoch 內、其 slot phase 首次跨越 tail 起點 Y 的那一塊，且 accumulator 只要非空即可；此時 H_W = Z(γ_A)"
  ],
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
 "explanation": "eq. 6.29：H_W ≡ Z(γ_A) 當 **e′ = e ∧ m < Y ≤ m′ ∧ |γ_A| = E**，否則 ∅。逐條拆開：e′ = e 表示**還在同一個 epoch 內**（不是換屆那一塊）；m < Y ≤ m′ 表示前一塊的 phase 還在投票期內、本塊的 phase 已經到達或越過截止點 Y = 500——這個「跨越」的性質保證了**整個 epoch 至多只有一塊**滿足它；|γ_A| = E 則要求 accumulator 已收滿 600 張。**它和 γ′_S 是同一份資料在兩個時間點**：H_W 在票剛截止那一塊就把結果公告在 header 裡，eq. 6.25 則要等到下個 epoch 的第一塊才把同一份 Z(γ_A) 定案為 γ′_S。兩處必須逐項一致，算錯方向就會踩到 InvalidTicketsMark。這樣安排的用意是讓只讀 header 的人**提早一整段 tail** 就知道下個 epoch 誰在哪個 slot 出塊，不必等到換屆。**注意反面情形**：若 epoch 尾端根本沒有區塊跨越 Y（例如 m = 480 之後就直接進入下個 epoch），H_W 永遠不會出現，而那個 epoch 也就只能走 fallback——這與 eq. 6.25 的 m ≥ Y 條件是同一件事的兩面。",
 "trap": "H_W 與 H_E 互斥：H_W 要 e′ = e，H_E 要 e′ > e。"
},
{
 "id": "ch06-ticket-extrinsic-limits",
 "ch": "6", "section": "6.7 The Extrinsic and Tickets", "gpRef": "eq. 6.30–6.32",
 "difficulty": 2, "kind": "delta", "tags": ["safrole", "tickets", "delta-0.8.0"],
  "stemZh": "依 GP 0.8.0，tickets extrinsic E_T 受哪些界限約束？",
  "optionsZh": [
   "m′ < Y 時 |E_T| ≤ K = 16，否則 |E_T| = 0；每個 entry index e < n，其中 n = ⌈2E / |γ′_P|⌉——所以 full 設定下是 2（E = 600、|γ′_P| = 1023）",
   "每一塊都是 |E_T| ≤ K = 16，包含 tail 期間的區塊；每個 entry index e < N = 2，這是一個不依賴 validator 集合大小的固定常數（E = 600、|κ| = 1023）",
   "|E_T| ≤ E = 600，而且是整個 epoch 加總而非每塊計算；每個 entry index e < n，其中 n = ⌈2E / |γ′_P|⌉——所以 full 設定下是 2（E = 600、|γ′_P| = 1023）",
   "m′ ≤ Y 時 |E_T| ≤ K = 16，否則 |E_T| = 0；每個 entry index e < n，其中 n = ⌈|γ′_P| / 2E⌉——所以 full 設定下是 1（E = 600、|γ′_P| = 1023）"
  ],
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
 "explanation": "三個限制，來源不同。**每位 validator 的配額**（eq. 6.30）：entry index r ∈ N_n，n = ⌈2E / |γ′_P|⌉。0.8.0（PR #527）把原本的常數 N 換成這條公式，理由 GP 明寫：「To ensure the accumulator can be saturated, when there are fewer validators, each validator is permitted more tickets」——accumulator 要收滿 E = 600 張才能啟用票券模式，validator 少的時候若每人配額不變就永遠收不滿。full 設定：⌈2·600/1023⌉ = **2**；test-vector 的 tiny 設定（E = 12、|γ′_P| = 6）：⌈24/6⌉ = **4**（0.7.x 的 tiny 常數是 3，這是遷移時必須改的點）。**每塊的數量上限與時間窗**（eq. 6.31）：|E_T| ≤ K = 16 當 m′ < Y = 500；**m′ ≥ Y 時 |E_T| 必須為 0**——tail 期間完全不能再提票，不是「提了也不算」而是「提了區塊就無效」。**為什麼要有 tail**：投票必須在 epoch 結束前收攤，Z(γ_A) 才能在 eq. 6.29 的那一塊被公告成 H_W、並在下個 epoch 第一塊定案為 γ′_S。沒有這段緩衝，換屆時序列還在變動。注意 K = 16 是**每塊**上限而非每人，用意是限制單塊的驗簽成本（ring proof 驗證不便宜）。",
 "trap": "條件是 m′ < Y（本塊的 phase），K = 16 是每個區塊的上限，不是每個 epoch。"
},
{
 "id": "ch06-ticket-accumulator-rules",
 "ch": "6", "section": "6.7 The Extrinsic and Tickets", "gpRef": "eq. 6.33–6.36",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "tickets"],
  "stemZh": "關於新進的 ticket n 與 posterior 的 accumulator γ′_A，哪一個敘述是**錯的**？",
  "optionsZh": [
   "n 必須依 ticket id 升冪排序且不得重複，而且 n 裡的任何 id 都不得已經在 γ_A 裡",
   "γ′_A 是 n 與（γ_A，若 e′ > e 則為 ∅）的排序聯集當中最小的 E 筆",
   "每一張被提交的 ticket 都必須出現在 γ′_A 裡——會被 accumulator 上限擠掉的 ticket 是無用的，會讓該 extrinsic 無效",
   "id 較大的 ticket 較受青睞，所以 γ′_A 保留的是最大的 E 筆"
  ],
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
  "stemZh": "E_T 裡的一份 ticket 證明 p 是 Bandersnatch ring-VRF 證明。它是對哪個 ring root、用什麼 context 驗證的？ticket 的識別碼又是什麼？",
  "optionsZh": [
   "對 γ′_Z（posterior 的 ring root）驗證，context 為 X_T ⌢ η′_2 ++ r，訊息為空序列 []；ticket id 是 VRF 輸出 Y(p)",
   "對 γ_Z（prior 的 ring root）驗證，context 為 X_T ⌢ η′_3 ++ r，訊息為 E_U(H)（未含 seal 的 header）；ticket id 是 Blake2b 雜湊 H(p)",
   "對 κ′（active set）的 Ed25519 金鑰驗證，context 為 X_T ⌢ η_0 ++ r，訊息為空序列 []；ticket id 就是那份證明 p 本身",
   "對 γ′_Z（posterior 的 ring root）驗證，context 為 X_E ⌢ Y(H_S)，訊息為 E_U(H)（未含 seal 的 header）；ticket id 是 VRF 輸出 Y(p)"
  ],
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
 "explanation": "eq. 6.30：p ∈ F̄^{X_T ⌢ η′_2 ++ r}_{γ′_Z}([])——四個要素缺一不可。**驗證 root 是 γ′_Z**（posterior 的 epoch ring root）：若本塊是 epoch 第一塊，γ′_Z 已經換成新 pending set 的 root，所以 ticket 是針對**新的** ring 驗證的。**context 是 X_T ⌢ η′_2 ++ r**：X_T = `$jam_ticket_seal` 是 domain separator、η′_2 是本 epoch 的抽籤隨機性、r 是 entry index（同一位 validator 可以用不同的 r 提交多張）。**訊息是空序列 []**——ticket 不需要對任何內容表態，它只是「我有資格」這件事本身。**ticket id 是 VRF 輸出 y = Y(p)**（eq. 6.32），這個值後來會在出塊時被 eq. 6.16 拿來比對。**匿名性是怎麼來的**：ring proof 讓驗證者確信「**某個** γ′_P 的成員」擁有這張票，卻不知道是哪一位——這是 ring VRF 相對於一般 VRF 的全部價值。而因為 VRF 輸出是確定性且不可偏置的，持票人也無法挑選自己想要的 slot，只能接受抽到什麼算什麼。你們的 createSignatureContext 組出來的正是 `jam_ticket_seal` + η′_2（32 B）+ attempt（1 B）。",
 "trap": "ring VRF 用在 ticket；一般 VRF 用在 seal 與 H_V。"
},
{
 "id": "ch06-seal-fallback",
 "ch": "6", "section": "6.4 Sealing", "gpRef": "eq. 6.17–6.18",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "seal", "fallback"],
  "stemZh": "在 fallback 模式下（γ′_S 是一串 Bandersnatch 金鑰），header 要通過哪些檢查？",
  "optionsZh": [
   "γ′_S[H_T mod E] 必須等於 H_A；H_S 是由 H_A 以 context X_F ⌢ η′_3 對 E_U(H) 所做的 Bandersnatch 簽章；T = 0；而 H_V 仍然必要，其 context 為 X_E ⌢ Y(H_S)、訊息為 []",
   "γ′_S[H_T mod E] 必須等於 H_A；H_S 是由 H_A 以 context X_F ⌢ η′_2 對 E_U(H) 所做的 Bandersnatch 簽章；T = 0；而 H_V 仍然必要，其 context 為 X_E ⌢ Y(H_S)、訊息為 E_U(H)",
   "γ′_S[H_T mod E] 必須等於出塊者的 Ed25519 金鑰；H_S 是對 γ′_Z 的 ring-VRF 證明，context 為 X_F ⌢ η′_3、訊息為 E_U(H)；T = 1；而 H_V 仍然必要，其 context 為 X_E ⌢ Y(H_S)、訊息為 []",
   "γ′_S[H_T mod E] 必須等於 H_A；fallback 模式下不需要 seal，因為沒有 ticket 識別碼可供綁定；T = 0；只檢查 H_V，其 context 為 X_E ⌢ η′_3、訊息為 []"
  ],
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
 "explanation": "eq. 6.17（fallback 模式，γ′_S 每格直接是一把 Bandersnatch 公鑰）：**i = H_A**——該 slot 指定的那把公鑰必須就是本塊作者的；**H_S ∈ F^{X_F ⌢ η′_3}_{H_A}(E_U(H))**；**T = 0**。和票券模式對照著記：票券模式比對的是 **VRF 輸出等於 ticket id**（i_y = Y(H_S)），fallback 比對的是**公鑰本身相等**（i = H_A）——後者根本沒有匿名性可言，因為出塊表是公開可算的。context 也換了：X_F = `$jam_fallback_seal` 取代 X_T，而且**沒有 ++ i_e**（fallback 沒有 entry index 這回事）。**eq. 6.18 兩種模式都適用**：H_V ∈ F^{X_E ⌢ Y(H_S)}_{H_A}([])，X_E = `$jam_entropy`。也就是說**熵在 fallback 之下仍然每塊更新**——Safrole 可以退化，但鏈的隨機性來源不能斷，否則下個 epoch 連 fallback 都沒有種子可用。注意它的 context 吃的是 Y(H_S)，所以 seal 必須先算出來。**T 這個旗標有下游用途**：§19 的 best-chain 規則偏好「ticket-sealed 祖先較多」的分支，因為 fallback 區塊的出塊者是公開可預測的，安全性較低——T = 0 就是這個偏好的依據。",
 "trap": "fallback 的 entropy 仍然每塊更新（H_V 必填）。"
},
{
 "id": "ch06-code-slot-key-sequence",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.25 — internal/safrole/sealing.go UpdateSlotKeySequence",
 "difficulty": 2, "kind": "code", "tags": ["safrole", "code"],
  "stemZh": "這是團隊對 γ′_S 的實作。關於它的哪一個說法是正確的？",
  "optionsZh": [
   "`slotIndex` 是 m——**前一塊**的 slot phase（τ mod E）——而 `gammaA` 是 prior 的 accumulator；`etaPrime[2]` 與 `posteriorState.GetKappa()` 都是 posterior 值，與 F(η′_2, κ′) 相符",
   "`slotIndex` 應該是 m′——正在匯入這一塊的 phase，也就是 H_T mod E——因為 eq. 6.25 問的是「到當前這一塊為止競賽是否已結束」；讀前一塊的 τ mod E 是差一錯誤",
   "fallback 分支應該把 prior 的 κ 與 prior 的 η_2 一起傳入，因為新進的 validator 要從該 epoch 的第二塊起才取得出塊權",
   "只要 |γ_A| = E 且 m ≥ Y，第一個分支在 ePrime ≥ e + 2 時也應該觸發，因為累積的 ticket 在被消耗之前一直有效；把它限制在 e + 1 是不必要地強迫走 fallback"
  ],
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
 "explanation": "eq. 6.25 給 γ′_S 三種情形，這段程式要同時對上三處才算正確。**第一處是 m 還是 m′。** m 是 **prior** block 的 phase（τ mod E），m′ 是本塊的（τ′ mod E）。6.25 用票券的條件是 e′ = e + 1 ∧ **m ≥ Y** ∧ |γ_A| = E——用 prior 的 phase，是為了確認「投票在前一塊之前就已經結束」。寫成 m′ 會讓「剛好跨過 Y 的那一塊」立刻開票，等於少等一整段 tail，這正是 fuzzer 最愛打的邊界。**第二處是 prior 還是 posterior。** fallback 函數 F 的兩個參數必須是 η′_2 與 κ′，都是 posterior。原因是 epoch 第一塊會先完成 eq. 6.14 的輪換（γ_P → κ、κ → λ）與 entropy rotate，之後 κ′ 才是本 epoch 真正的 active set。你們的 OuterUsedSafrole 先做 UpdateEntropy、KeyRotate，最後才 UpdateSlotKeySequence，順序正是為了讓這兩個值就位。**第三處是跳過整個 epoch。** e′ ≥ e + 2 必須走 fallback，不能沿用 accumulator：那批 ticket 是為「e + 1」那個 epoch 準備的，它們的 ring proof 針對的是當時的 γ_Z（epoch ring root），中間隔了一個 epoch 之後 ring root 與 η 都已再度輪替，證明不再對應。相關名詞：Y = 500 是 ticket 投票截止的 phase（epoch tail start）、E = 600 是 epoch 長度、γ_A 是 ticket accumulator、γ_Z 是 epoch 的 Bandersnatch ring root。",
 "trap": "你們的 OuterUsedSafrole 先做 UpdateEntropy、KeyRotate，再做 UpdateSlotKeySequence——順序正是為了讓 η′_2、κ′ 就位。"
},
{
 "id": "ch06-code-fallback-hash",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.27 — internal/safrole/slot_key_sequence.go",
 "difficulty": 2, "kind": "code", "tags": ["safrole", "code", "fallback"],
  "stemZh": "讀團隊的 FallbackKeySequence。關於它是否符合 eq. 6.27，哪個敘述正確？",
  "optionsZh": [
   "雜湊是對的——Blake2b 就是 GP 的 H，而且前 4 個 octet 是以 little-endian 解碼——但 eq. 6.27 的 cyclic 下標是對**傳入的金鑰序列長度**（也就是 |κ′|）取模，程式碼卻是對編譯期常數 ValidatorsCount 取模",
   "雜湊是錯的——§3.8 把 H 保留給 Blake2b-256，但 eq. 6.27 要的是 H_K、也就是 Keccak-256，正如那段殘留的註解所說——而模數是對的，因為 cyclic 下標就是對 ValidatorsCount 所持的固定 validator 數取模",
   "取的片段是錯的——eq. 6.27 的下標取的是 H(r ⌢ E_4(i)) 的**最後**四個 octet 並以 big-endian 解碼，所以 Blake2bHashPartial(·, 4) 讀錯了一端——而對 ValidatorsCount 取模則與該式的 cyclic 下標完全相符",
   "那個取模是多餘的——四個 Blake2b octet 的 decode_4 本來就落在 N_E 之內，而 eq. 6.27 根本沒有任何模數，所以 `%= ValidatorsCount` 是憑空多出來的一步，可能把兩個不同的時槽映到同一位 validator、破壞「一槽一人」"
  ],
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
 "explanation": "eq. 6.27：F(r, k) = [ k[decode_4(H(r ⌢ E_4(i))_{…4})]^⟲ _b | i ∈ N_E ]。逐項對照程式碼：**H 是 Blake2b**——§3.8 定義 H ≡ Blake2b-256；H_K 才是 Keccak，只用在 accumulation-output belt 與 BEEFY。**取前 4 個位元組、little-endian 解碼**（decode_4）。這兩點程式都對，雖然註解寫 Keccak256 已經 stale，實際呼叫的是 Blake2bHashPartial。**真正的落差在 ⟲ 這個記號**：它是 §3.7 的模數下標 s[i]^⟲ ≡ s[i mod |s|]，對的是**傳入的金鑰序列長度** |k| = |κ′|；程式卻寫 `%= types.ValidatorsCount`，用的是編譯期常數。在 0.7.2 這沒問題（|κ| 恆等於 V），但 0.8.0 讓 |κ| 可變（eq. 6.8 的 𝕍）之後就必須換成 len(κ′)，否則在非滿編的設定下會索引越界或選錯人。這正是 issue #1037 那一類問題。**一個容易誤判為 bug 的行為**：取模會讓不同 slot 抽到同一位 validator——這是 F 的正常語意（可重複抽樣），不是缺陷；fallback 本來就沒有「每人一個 slot」的保證。",
 "trap": "面試官可能直接問：你們 fallback 用哪個 hash？答 Blake2b，並指出註解錯誤。"
},
{
 "id": "ch06-code-entropy-order",
 "ch": "6", "section": "6.4 Sealing and Entropy", "gpRef": "eq. 6.23–6.24 — internal/safrole/sealing.go UpdateEntropy",
 "difficulty": 2, "kind": "code", "tags": ["safrole", "code", "entropy"],
  "stemZh": "在團隊的 UpdateEntropy 中，為什麼 `eta[0]` 是在輪替迴圈**之後**才被 posterior 的 η′_0 覆寫？如果讓迴圈在 UpdateEtaPrime0 寫入同一個陣列之後才跑，會出什麼問題？",
  "optionsZh": [
   "因為 eq. 6.24 輪替進 η′_1 的是 **prior** 的 η_0；若被輪替的是 η′_0（它已經混入本塊的 VRF 輸出），η′_1 就會錯誤地包含當前這一塊的熵",
   "因為 eq. 6.24 會在 epoch 換屆時為累積器重新播種：η′_0 必須在輪替之後重設，好讓新的 epoch 從一個乾淨的值開始，而最後才寫 eta[0] 正是達成這件事",
   "因為那個遞減的迴圈正是防止 η_0 被複製進全部三個歷史欄位的關鍵；對 eta[0] 的寫入與 eq. 6.24 無關，放在輪替之前執行也一樣可以",
   "因為 eq. 6.24 是以 posterior 值陳述的，(η′_1, η′_2, η′_3) = (η′_0, η′_1, η′_2)，所以 η′_0 必須先定案，而迴圈之後的那個賦值是對錯誤順序所做的補償性修正"
  ],
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
 "explanation": "兩條式子必須分清楚。eq. 6.23：η′_0 = H(η_0 ⌢ Y(H_V))——把 **prior** 的 η_0 接上本塊 entropy VRF 簽章的輸出再 hash，所以 η′_0 **已經含有本塊的隨機性**。eq. 6.24：(η′_1, η′_2, η′_3) ≡ (η_0, η_1, η_2)——右側**全部是 prior 值**，是一次單純的整體右移。**所以順序不能顛倒**：正確做法是先用 prior 的 η_0 完成 rotation（η_0 → η′_1），最後才把 η′_0 寫回 eta[0]。若先寫 η′_0 再 rotate，η′_1 會變成 H(η_0 ⌢ Y(H_V))，也就是**把本塊的熵提前混進了「上一個 epoch 的結尾值」**。**後果會擴散**：η′_2 是 ticket 的 ring-VRF context 種子、也是 fallback F 的種子，η′_3 則用於驗證 seal；三者一路錯下去，state root 立刻與其他節點 mismatch。**這是 fuzzer 最常抓到的 bug 類型**——「prior 還是 posterior」的錯誤在單機測試中完全看不出來，因為兩種寫法都能自洽地跑完，只有跟別人比對 state root 時才會爆。相關名詞：η 是 entropy pool，四個 32 位元組的值；η_0 每塊更新，η_1、η_2、η_3 分別是前三個 epoch 結束時的快照。",
 "trap": "所有 Safrole 式子都要先問：右邊是 prior 還是 posterior？"
},
]
