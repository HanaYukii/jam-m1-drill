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
 "explanation": "eq. 5.1：H ≡ (H_P parent hash, H_R prior state root, H_X extrinsic hash, H_T timeslot, H_E epoch marker, H_W winning-tickets marker, H_O offenders marker, H_I author index, H_V VRF signature, H_S seal)，共十個欄位——一個 parent hash、兩個 root/hash、時間、三個 marker、作者索引，以及兩個 Bandersnatch 簽章。BEEFY / accumulation-output root 屬於 β 的 accumulation-output belt（β_B，見 §7）與 §18 Beefy Distribution 的鏈下流程，從來不是 header 的一部分。",
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
 "explanation": "GP §5：「This is a departure from both Polkadot and the Yellow Paper's Ethereum… We do this to facilitate the pipelining of block computation and in particular of Merklization.」實務上 block author 可以先發布區塊，把耗時的 state Merklization 延後到下一個 slot 才需要（下一個區塊的 H_R 才會用到）。後果：β 裡最新一筆的 state root 先填零，由下一個區塊的 β† 用 H_R 補正（eq. 7.5）。",
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
 "explanation": "GP eq. 5.6–5.7：p = E(var[(E_4(s), H(d)) for (s,d) in E_P])，g = E(var[(H(w), E_4(t), var(a)) for (w,t,a) in E_G])。GP 為此給的理由（§5）：「taking care to allow for the possibility of reports and preimages to individually have their inclusion proven」——只放 hash，就能用 Merkle proof 證明某個 preimage/report 在區塊裡，而不必附上整個 blob。你們的 code（block_serialization / header hash）在 0.7.2 對 guarantees 已是用 report hash，0.8.0 再把 preimages 改為 (service, blake(data))。",
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
 "explanation": "GP eq. 5.8：P(H)_t < H_T ∧ H_T·P ≤ T，其中 P = 6 秒、T 為 wall-clock 秒數（自 Common Era 起算）。§5 原文：「A block may only be regarded as valid once the time-slot index H_T is in the past. It is always strictly greater than that of its parent.」且「Blocks considered invalid by this rule may become valid as T advances」——太新的區塊只是暫時無效，不是永久拒絕。你們 STF 裡 `BadSlot` 對應的是 τ ≥ τ′ 的情況。",
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
 "explanation": "GP eq. 5.10：H_I ∈ N_{|κ′|}，H_A ≡ κ′[H_I]_b，「this is merely an equivalence, and is not serialized as part of the header」——驗證者是自己用 κ′ 算出作者的 Bandersnatch key。用 posterior κ′ 是因為 epoch 交界的第一個區塊已由新的 active set 出塊（key rotation 在該區塊內完成）。你們的 sealing.go 驗 seal/VRF 時傳入的也是 posterior state（code-map 3.2.6 註：參數名叫 priorState 但 STF 傳的是 posterior）。",
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
 "explanation": "GP eq. 11.38：∀x ∈ contexts: ∃h, h′ ∈ A: h_t = x_l（lookup-anchor time）∧ H(h) = x_l（lookup-anchor hash）∧ h′_p = H(h) ∧ h′_r = x_{l,s}（posterior state root of lookup anchor，0.8.0 新增）。§11.4：「this is one of the few conditions which cannot be checked purely with on-chain state and must be checked by virtue of retaining the series of the last L headers」。這也是 fuzzer 的「Ancestry」feature：M1 必須支援。",
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
 "explanation": "GP eq. 5.11：H_E ∈ (H, H, [(bandersnatch, ed25519)]_V)?（兩個 entropy hash + 下一 epoch 每個 validator 的 Bandersnatch 與 Ed25519 key，0.6.4 起加入 Ed25519），H_W ∈ ([ticket]_E)?（E = 600 張 tickets），H_O ∈ [ed25519 key]。時機也不同：H_E 只在 e′ > e 時非空，H_W 只在同一 epoch 內首次跨越 Y 且 accumulator 飽和時非空，而 H_O 與 epoch 邊界無關，由 §10 disputes 帶進來的 culprits/faults 決定。fallback slot-sealer 序列 F(η′_2, κ′) 則是鏈上重算（eq. 6.27），不佔任何 header 欄位。",
 "trap": "H_E 放的是 key 的子集合（bs + ed），不是完整 336-octet key；H_O 放 key 不是 index。"
},
]
