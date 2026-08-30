# -*- coding: utf-8 -*-
# Chapter 5 — The Header (GP 0.8.0)
ITEMS = [
{
 "id": "ch05-header-fields",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.1",
 "difficulty": 1, "kind": "concept", "tags": ["header"],
 "stem": "GP eq. 5.1 defines the header H as a 10-tuple. Which field is NOT part of the header?",
 "options": [
  "H_R — the prior state root, which is the parent block's posterior state root",
  "H_W — the winning-tickets marker, carrying the next epoch's E = 600 tickets",
  "H_B — the BEEFY root committing to this block's own accumulation outputs",
  "H_V — the entropy-yielding VRF signature that feeds the accumulator η_0"
 ],
 "answer": 2,
 "optNotes": [
  "H_R 是 eq. 5.1 的第二個欄位，§5 定義它就是 parent 的 posterior state root。",
  "H_W 型別為 ([ticket]_E)?（eq. 5.11），E = 600，裝的正是下一 epoch 的 slot-sealer tickets。",
  "accumulation output 走 β 的 accumulation-output belt，簽的是 last(β)_b 的 super-peak，header 無此欄。",
  "H_V 的輸出 Y(H_V) 正是 entropy accumulator 的輸入：η′_0 ≡ H(η_0 ⌢ Y(H_V))。",
 ],
 "explanation": "eq. 5.1：H ≡ (H_P, H_R, H_X, H_T, H_E, H_W, H_O, H_I, H_V, H_S)，十個欄位，可以分成四組來記：**指向過去**——H_P parent hash（父 header 完整編碼的 Blake2b）、H_R prior state root（**父區塊的** posterior root）；**指向本塊內容**——H_X extrinsic hash、H_T timeslot；**給輕客戶端的三個 marker**——H_E epoch、H_W winning-tickets、H_O offenders；**出塊者身分與證明**——H_I author index、H_V entropy VRF 簽章、H_S seal。**為什麼 BEEFY root 不在裡面**：accumulation output 的承諾走的是狀態那條路——θ（本塊的 output log）被吸進 β_B（accumulation-output belt，一個 MMR，§7），BEEFY（§18）再對它取 super-peak 簽名，那是**鏈下的分發流程**，不是 header 欄位。把它放進 header 反而會破壞 pipelining：H_R 之所以是 prior root，就是為了讓出塊者不必先算完本塊的 Merklization；若 header 還要承諾本塊自己的 accumulation output，那個好處就沒了。順帶記：H_A（作者的 Bandersnatch 公鑰）也**不是**欄位，它只是 κ′[H_I]_b 的等價式，不被序列化。",
 "trap": "記憶法：p r x t | e w o | i v s。"
},
{
 "id": "ch05-prior-state-root",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.9 (H_r)",
 "difficulty": 1, "kind": "rationale", "tags": ["header", "pipelining"],
 "stem": "Unlike Ethereum and Polkadot, a JAM header commits to the PRIOR state root (H_R = M_σ(σ)) rather than the posterior one. What is the stated reason?",
 "options": [
  "To reduce header size: the extrinsic hash H_X already commits to every input that can change state, so committing a second 32-octet root would be redundant",
  "To facilitate pipelining of block computation, in particular of Merklization: the author need not finish Merklizing the new state before publishing the block",
  "Because Grandpa votes carry the block header alone, which makes the header's prior state root the only place a finalized state root is ever committed",
  "Because the posterior state root is undefined until the block's work-reports have been audited, and auditing only completes several tranches later"
 ],
 "answer": 1,
 "optNotes": [
  "prior 與 posterior root 都是 32 octet，換一個並不省空間；H_X 承諾的是輸入而不是結果狀態。",
  "GP 給的理由就是 pipelining：作者不必先算完新狀態的 Merklization 才發布區塊。",
  "§19 明寫 Grandpa 投的是 best block header「together with its posterior state root」。",
  "σ′ 由 (σ, B) 完全決定、區塊內就算得出；auditing 是鏈下流程，只影響 finalization 與選鏈。",
 ],
 "explanation": "GP §5 原文：「This is a departure from both Polkadot and the Yellow Paper's Ethereum… We do this to facilitate the pipelining of block computation and in particular of Merklization.」**H_R = M_σ(σ) 是 prior state 的 root，也就是父區塊的 posterior root**，不是本塊執行完的結果。**實務上買到什麼**：Merklization 是整個轉移裡最慢的一段（要走完整棵 Patricia trie）。把它移出關鍵路徑之後，出塊者可以先把區塊發出去，本塊的 posterior root 到**下一個 slot** 才真正需要——因為那是下一個區塊的 H_R。傳播與 Merklization 因此可以重疊，而不是排隊。**代價與補償**：β_H 裡最新那一筆的 state root 在當下還算不出來，只能先填 H_0（零雜湊）；下一個區塊再用 eq. 7.5 的 β†（beta dagger）把它用自己的 H_R 補正。所以「β_H 最後一筆的 root 是零」不是 bug 而是設計，這也是為什麼 §7 要多一個 dagger 中間態。**口試會追問的對照**：Ethereum 的 header 帶 post-state root，代表出塊者必須算完才能發布——JAM 用一個 slot 的延遲換取整段 Merklization 的並行空間。",
 "trap": "設計理念題。延伸：Grandpa vote 會帶 posterior state root（§19）以彌補 header 只有 prior root。"
},
{
 "id": "ch05-extrinsic-hash-080",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.4–5.7 (H_x)",
 "difficulty": 3, "kind": "delta", "tags": ["header", "delta-0.8.0", "codec"],
 "stem": "GP 0.8.0 (PR #524) redefined the extrinsic hash H_X = H(E(H#(a))) with a = [E_T(E_T), p, g, E_A(E_A), E_D(E_D)]. How are the preimages (p) and guarantees (g) components formed?",
 "options": [
  "p and g are the full codec encodings of E_P and E_G exactly as the block body carries them, so a commits to every preimage blob and every complete work-report",
  "p encodes the sequence of (E_4(service), H(data)) pairs and g encodes the sequence of (H(work-report), E_4(slot), var(credential)) tuples, each sequence var-length prefixed",
  "p is the Blake2b hash of the concatenated preimage blobs and g is the Keccak hash of the concatenated work-reports, so a carries exactly one 32-octet leaf for each",
  "p and g are dropped from a, which is then the three-element sequence [E_T(E_T), E_A(E_A), E_D(E_D)]; preimages and guarantees are committed only via the prior state root"
 ],
 "answer": 1,
 "optNotes": [
  "那樣 a 會扛著整包 blob 與整份 report，恰好毀掉「逐項證明 inclusion」的設計目的。",
  "eq. 5.6–5.7 兩者都是 E(var[…]) 的形狀：序列每個元素先換成 hash 再編碼。",
  "H# 是 blake-many（對序列每個元素各取一次 hash），且 Keccak 在 JAM 只用於 §18 的 BEEFY MMR。",
  "eq. 5.5 的 a 是五個元素；preimages 與 guarantees 正是靠 H_X 而非 state root 進入 header。",
 ],
 "explanation": "eq. 5.4–5.7：H_X = H(E(H#(a)))，其中 a 是五個成分各自的承諾，**每個成分先被壓成自己的雜湊、再一起雜湊**。0.8.0（PR #524）重新定義了其中兩個：p = E(var[(E_4(s), H(d)) | (s, d) ∈ E_P])——preimage 存的是 (service index, blob 的雜湊)；g = E(var[(H(w), E_4(t), var(a)) | (w, t, a) ∈ E_G])——guarantee 存的是 (work-report 的雜湊, slot, 擔保簽章)。**GP 給的理由寫在 §5**：「taking care to allow for the possibility of reports and preimages to individually have their inclusion proven」——因為只放雜湊，第三方就能用一份 Merkle proof 證明「某個 preimage 或某份 report 確實在這個區塊裡」，而**不必附上整個 blob 或整份報告**。work-report 可以接近 48 KiB（W_R），preimage 更可能是任意大小，差別是實質的。**為什麼是兩層雜湊**：先各自 hash 再合併，讓每個成分成為獨立的承諾——證明某個 preimage 存在時，不需要揭露 tickets、assurances 或 disputes 的內容。這是「承諾結構跟隨證明需求」的典型設計，與 §7 的 β_B 用 MMR 是同一種思路。",
 "trap": "0.7.2→0.8.0 差異；H# 是 blake-many（對序列每個元素各取 hash 再 encode）。"
},
{
 "id": "ch05-timeslot-validity",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.8",
 "difficulty": 1, "kind": "concept", "tags": ["header", "time"],
 "stem": "Which condition must a block's timeslot H_T satisfy for the block to be considered valid right now?",
 "options": [
  "P(H)_t < H_T ∧ H_T · P ≤ T — strictly greater than the parent's slot, and no later than the current wall-clock time T",
  "P(H)_t ≤ H_T ∧ H_T · P ≤ T — greater than or equal to the parent's slot, and no later than the current wall-clock time T",
  "P(H)_t < H_T ∧ H_T · P ≥ T — strictly greater than the parent's slot, and at or beyond the current wall-clock time T",
  "H_T = P(H)_t + 1 ∧ H_T · P ≤ T — exactly one slot after the parent, and no later than the current wall-clock time T"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 5.8 正是這兩條：對 parent 嚴格大於，且 H_T·P ≤ T（P = 6 秒的 wall-clock）。",
  "放寬成「大於或等於 parent」會允許父子同 slot，GP 明寫 strictly greater。",
  "wall-clock 條件方向反了：H_T·P ≥ T 等於只接受當下或未來的區塊。",
  "要求恰好 parent + 1 就禁止跳 slot，但沒人出塊時 slot 本來就會被跳過。",
 ],
 "explanation": "eq. 5.8：**P(H)_T < H_T ∧ H_T · P ≤ 𝕋**。兩個條件的性質完全不同，這是這題的重點。**前半是永久性的**：本塊的時槽必須嚴格大於父的（GP：「It is always strictly greater than that of its parent」）。違反就是永遠無效——你們 STF 裡的 `BadSlot` 對應的正是這種 τ ≥ τ′ 的情況。**後半是暫時性的**：H_T 乘上 P = 6 秒（每個時槽的長度）不得超過目前的牆鐘秒數 𝕋（自 JAM Common Era 起算）。GP 特別補一句「Blocks considered invalid by this rule may become valid as 𝕋 advances」——**一個「來自未來」的區塊只是還沒到時候，不該被永久丟棄或當成攻擊**，實作上通常先留著、等時間到再處理。把這兩者混為一談是常見的實作 bug：對未來區塊直接 ban 掉來源節點，會在時鐘些微不同步時互相斷線。**注意這條規則不需要任何狀態**：前半只要父 header、後半只要一個時鐘，所以它是「只拿到 header 能驗什麼」那題裡的第二層——真正卡住的是需要 κ′ 與 γ′_S 的 seal。",
 "trap": "跳 slot 是合法的（例如沒人出塊），這也是為什麼 Safrole 要處理 e′ > e+1（整個 epoch 被跳過）的情況。"
},
{
 "id": "ch05-author-index",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.10 (H_i, H_a)",
 "difficulty": 2, "kind": "concept", "tags": ["header", "validators"],
 "stem": "The block author index H_I is an index into which validator set, and how is the author's Bandersnatch key H_A obtained?",
 "options": [
  "Into the prior active set κ; H_A = κ[H_I]_b, and H_A is serialized as an eleventh header field beside H_I",
  "Into the posterior active set κ′; H_A ≡ κ′[H_I]_b, and H_A is NOT serialized — it is merely an equivalence",
  "Into the pending set γ_k; H_A = γ_k[H_I]_b, which is why H_I may exceed |κ′| in an epoch's first block",
  "Into the staging set ι; H_A = ι[H_I]_b, since ι holds the keys the delegator designates for the very next epoch"
 ],
 "answer": 1,
 "optNotes": [
  "prior/posterior 反了，而且 eq. 5.1 的 header 只有十個欄位，H_A 從不上鏈。",
  "eq. 5.10 就是 H_I ∈ N_{|κ′|}、H_A ≡ κ′[H_I]_b，並明說它不被序列化。",
  "違反 eq. 5.10 的型別 H_I ∈ N_{|κ′|}——索引域永遠是 κ′，不可能超出。",
  "ι 慢一輪：eq. 6.14 要先 ι → γ_k，再過一個 epoch 才成為 κ，對應的是下下個 epoch。",
 ],
 "explanation": "eq. 5.10：H_I ∈ N_{|κ′|}，H_A ≡ κ′[H_I]_b。兩個要點。**其一，header 裡放的是索引不是公鑰。** GP 明說 H_A「is merely an equivalence, and is not serialized as part of the header」——驗證者拿到 H_I 之後，自己去 κ′ 裡查出作者的 Bandersnatch 公鑰。省下的是每塊 32 個位元組，但真正的代價是**驗簽從此需要狀態**（這正是輕客戶端只拿 header 驗不了 seal 的原因）。**其二，用的是 posterior 的 κ′ 不是 prior 的 κ。** epoch 交界的第一個區塊已經由**新的** active set 出塊，而金鑰輪換（eq. 6.14：γ_P → κ、κ → λ）是在該區塊的轉移中完成的——所以要驗那一塊的作者，必須先跑完輪換、拿到 κ′ 才行。你們的 sealing.go 驗 seal 與 VRF 時傳的也是 posterior state（code-map 3.2.6 註明參數雖叫 priorState、但 STF 實際傳入 posterior），這個命名落差值得記一下，容易看走眼。相關名詞：κ active（現行）、λ previous、ι staging、γ_P pending。",
 "trap": "epoch 第一個區塊：作者屬於 κ′ = 舊的 γ_k。"
},
{
 "id": "ch05-ancestors-lookup-anchor",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.3 (ancestors A) & §11.4 lookup anchor",
 "difficulty": 2, "kind": "concept", "tags": ["header", "ancestry"],
 "stem": "The GP only requires implementations to store headers of ancestors authored within the previous L = 14,400 timeslots (24 hours). Which on-chain check is the reason this ancestor set A is needed?",
 "options": [
  "Verifying that a guarantee's lookup-anchor block (hash, timeslot and posterior state root) really occurs in the chain, which state σ on its own cannot attest",
  "Verifying that each new block's parent hash H_P is the Blake2b of the parent header, which needs every header back to the last finalized block",
  "Verifying that each availability assurance's anchor matches the parent hash H_P, which needs a search of the retained headers to locate that anchor",
  "Recomputing the fallback slot-sealer sequence F(η′_2, κ′) after a skipped epoch, which needs the entropy VRF H_V of every header in the skipped epoch"
 ],
 "answer": 0,
 "optNotes": [
  "lookup anchor 最舊可到 L = 14,400 slot 之前，而 recent history β 只留 H = 8 塊，非靠 A 不可。",
  "eq. 5.2（H_P ≡ H(E(P(H)))）只用到直接的 parent header 一份，不必往回保留任何東西。",
  "eq. 11.12 的 a_a = H_P 是一次等值比對，不需要在保留的 header 序列裡搜尋。",
  "F(η′_2, κ′)（eq. 6.27）的輸入只有 posterior entropy 與 κ′ 兩個 state 分量，不讀歷史 header。",
 ],
 "explanation": "eq. 5.3 定義祖先集合 A（h ∈ A ⇔ h = H ∨ ∃i ∈ A : h = P(i)），而 GP 只要求實作保存「過去 L = 14,400 個時槽（24 小時）內出塊的祖先 header」。**需要它的是 §11.4 的 lookup-anchor 檢查。**eq. 11.38 要求：對每個 refinement context，存在 h, h′ ∈ A 使得 h 的時槽等於 context 的 lookup-anchor time、H(h) 等於 lookup-anchor hash、且 h′ 的 parent 是 H(h)、h′ 的 H_R 等於 context 記的 posterior state root（最後這項是 0.8.0 新增的）。**為什麼狀態本身辦不到**：σ 只描述「現在長什麼樣」，不保留「哪些區塊曾經在鏈上」。β_H 只留最近 H = 8 塊，遠遠不夠涵蓋 24 小時。GP 自己點明：「this is one of the few conditions which cannot be checked purely with on-chain state and must be checked by virtue of retaining the series of the last L headers」——**全書少數必須靠鏈外保存資料才能驗的條件之一**。**對 M1 的意義**：fuzzer 的 Ancestry feature 就是在測這個，實作必須真的維護那份 header 序列。別把 L = 14,400（24 小時，lookup anchor）與 D = 19,200（32 小時，preimage expunge）搞混，兩者常被互換。",
 "trap": "L = 14,400 slots = 24h；recent history H = 8 blocks 是給 anchor 用的，lookup anchor 用 A。"
},
{
 "id": "ch05-markers-types",
 "ch": "5", "section": "5.1 The Markers", "gpRef": "eq. 5.11 (markers)",
 "difficulty": 2, "kind": "concept", "tags": ["header", "markers"],
 "stem": "Which statement about the three header markers (H_E, H_W, H_O) is correct per eq. 5.11?",
 "options": [
  "H_E ∈ (H, H, [(bandersnatch, ed25519)]_V)? ; H_W ∈ ([ticket]_E)? ; H_O ∈ [ed25519 key] — the offenders marker is a plain sequence that may be empty but is never None",
  "H_E ∈ (H, H, [(bandersnatch, ed25519)]_V)? ; H_W ∈ ([ticket]_E)? ; H_O ∈ [ed25519 key]? — all three are optional and all three are None outside an epoch's first block",
  "H_E ∈ ([336-octet validator key]_V)? ; H_W ∈ ([bandersnatch key]_E)? ; H_O ∈ [ed25519 key] — the epoch marker carries whole keys and the winners marker the fallback sealers",
  "H_E ∈ (H, H, [(bandersnatch, ed25519)]_V)? ; H_W ∈ ([ticket]_E)? ; H_O ∈ [N_V]? — the offenders marker is optional and holds validator indices rather than keys"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 5.11 的 H_O 沒有 ? 包裝：它可以是空序列，但永遠不是 None。",
  "型別上 H_O 不帶 ?；語意上只要該塊帶了 culprits 或 faults，epoch 中間任何一塊都可能非空。",
  "H_E 只放 (bandersnatch, ed25519) 這對子集合；fallback key 由鏈上重算，從不進 H_W。",
  "H_O 裝的是 Ed25519 公鑰而不是 validator index，而且它並非 optional。",
 ],
 "explanation": "eq. 5.11 的三個型別：**H_E ∈ ?(H, H, ⟦(bandersnatch, ed25519)⟧_V)**——兩個 entropy 雜湊加上下個 epoch 每位 validator 的 Bandersnatch 與 Ed25519 金鑰（Ed25519 是 0.6.4 起加入的）；**H_W ∈ ?(⟦ticket⟧_E)**——整個 epoch 的 E = 600 張 ticket；**H_O ∈ ⟦ed25519 key⟧**——注意這個**沒有問號**，是普通序列，可以為空但永遠不是 ∅。前兩個是 optional、第三個不是，這個型別差異本身就是常考點。**出現時機也各不相同**：H_E 只在 e′ > e（新 epoch 第一塊）非空；H_W 只在同一 epoch 內首次跨越 Y = 500 且 accumulator 飽和的那一塊非空（eq. 6.29）；H_O 與 epoch 邊界完全無關，由本塊 disputes extrinsic 帶進來的 culprits 與 faults 決定，多數區塊為空。**一個容易誤答的方向**：fallback 的 slot-sealer 序列 F(η′_2, κ′) 並不佔任何 header 欄位——它是鏈上用 eq. 6.27 重算出來的，因為輸入（η′_2 與 κ′）本來就在狀態裡，不需要出塊者告知。換句話說，marker 只承載「算不出來、必須被告知」的東西。",
 "trap": "H_E 放的是 key 的子集合（bs + ed），不是完整 336-octet key；H_O 放 key 不是 index。"
},
]
