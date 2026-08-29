# -*- coding: utf-8 -*-
# Chapter 7 — Recent History; Chapter 8 — Authorization (GP 0.8.0)
ITEMS = [
{
 "id": "ch07-beta-structure",
 "ch": "7", "section": "7 Recent History", "gpRef": "eq. 7.1–7.4",
 "difficulty": 2, "kind": "concept", "tags": ["recent-history", "state"],
 "stem": "In GP 0.8.0 the recent-history state is β ≡ (β_H, β_B). What does each recent block entry in β_H hold, and what is β_B?",
 "options": [
  "Each β_H entry: (header hash h, state root s, accumulation-output-log super-peak b, timeslot t, dictionary p of reported work-package hash → segment root); β_B is the accumulation-output belt, an MMR of per-block accumulation-output roots",
  "Each β_H entry: (header hash, posterior state root, extrinsic hash, timeslot); β_B is the set of BEEFY signatures gathered over the last H = 8 blocks, which is what lets a bridge prove finality without following the header chain",
  "Each β_H entry: (header hash, state root, timeslot, list of the hashes of every work-report guaranteed in the block); β_B is the sequence of the last H = 8 block headers, retained so that a lookup-anchor can be resolved straight out of state",
  "β_H is a single rolling hash committing to the last H = 8 headers, so recent history costs only 32 octets of state; β_B is the four-entry entropy accumulator, rotated at each epoch boundary and re-seeded from every header's VRF output"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 7.2 的五個欄位（含 0.8.0 新增的 timeslot t）與 eq. 7.3 的 Keccak MMR belt 完全吻合。",
  "H_X 只存在 header（eq. 5.1），β 的 item 不含它；β_B 裝的全是 accumulation-output root，一個簽章都沒有。",
  "eq. 7.8 建的 p 是 package hash ↦ segment root 的 dictionary，不是 report hash 清單；狀態裡從無 header 序列。",
  "eq. 7.1–7.2 的 β_H 是最多 8 筆 tuple 的序列；四項的 entropy accumulator 是另一個狀態項 η。",
 ],
 "explanation": "eq. 7.2：β_H ∈ [(h ∈ H, s ∈ H, b ∈ H, t ∈ N_T, p ∈ D⟨H→H⟩)]_{:H}，H = 8。t（timeslot）是 0.8.0 新增欄位（配合 refinement context 的 anchor slot，#526）。p 是本塊 E_G 中每個 work-package hash → 其 segment root（exports root），供之後 report 的 prerequisite / segment-root lookup 驗證用。eq. 7.3：β_B ∈ [H?]（MMR 的 peaks，∅ 表示空 peak），用 Keccak。eq. 7.4：θ ∈ [(N_S, H)] 是本塊的 accumulation output（service, hash）序列。",
 "trap": "0.8.0 β_H 有 5 個欄位（多了 timeslot）；p 的 value 是 segment root 不是 report hash。"
},
{
 "id": "ch07-beta-dagger",
 "ch": "7", "section": "7 Recent History", "gpRef": "eq. 7.5 & 7.8",
 "difficulty": 2, "kind": "concept", "tags": ["recent-history", "pipelining"],
 "stem": "Why does the newest β_H entry get state root s = H_0 (the zero hash) at the end of block N, and how is it corrected?",
 "options": [
  "Because the posterior state root of block N is not yet known when β′ is computed (the header carries the prior root); block N+1 computes β† by overwriting the last entry's s with its own H_R (eq. 7.5) before anything reads β",
  "Because a state root only matters once the block is finalized: the entry keeps H_0 until Grandpa finalizes block N, at which point the finality gadget writes the real root into that entry and eq. 11.36 starts accepting anchors on it",
  "Because β_H entries carry no state root at all: eq. 7.2 declares an item as ⟨h, b, t, p⟩ and the zero hash is only a placeholder that C(3) skips, so eq. 11.36 matches an anchor on its header hash, super-peak and timeslot alone",
  "Because the root goes into β_B instead: each block appends its own posterior state root as the belt's next leaf, so the β_H item can leave s at H_0 permanently and an anchor's state root is checked against b"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 7.5：補正者是下一個區塊，用自己 header 的 H_R 覆寫父塊那筆——§7 說 β′ 只用來定義 β†。",
  "STF 是確定性函數，finality 從不回寫狀態；eq. 7.5 的補正發生在下一塊，與敲定無關。",
  "eq. 7.2 明列 s ∈ H 為第二個具名欄位，C(3) 讓它佔滿 32 bytes，eq. 11.36 也確實比對 x_s = y_s。",
  "eq. 7.6–7.7 append 進 belt 的 leaf 由 θ′ 編碼而來，與 state root 無關；x_s 與 x_b 是兩個獨立比較。",
 ],
 "explanation": "eq. 7.8：新 entry 為 (H(H), H_0, super-peak(β′_B), H_T, p)，§7 說明「The new state-trie root is the zero hash, which is inaccurate but safe since β′ is not utilized except to define the next block's β†」。eq. 7.5：β† ≡ β_H except β†[|β_H|−1]_s = H_R。所以每個 block 一開始（在驗 guarantee 的 anchor 之前）先用自己的 H_R 補正父塊的 state root。這是 header 帶 prior state root（pipelining）的直接後果。你們的 STF 在 τ′ 與 header check 之後、disputes 之前就算 β†。",
 "trap": "guarantee 的 anchor 檢查（eq. 11.36）比對的是 β†（補正後），不是 β。"
},
{
 "id": "ch07-belt-keccak",
 "ch": "7", "section": "7 Recent History", "gpRef": "eq. 7.6–7.7",
 "difficulty": 2, "kind": "rationale", "tags": ["recent-history", "mmr", "beefy"],
 "stem": "The accumulation-output belt β′_B = A(β_B, M_B(s, H_K), H_K) uses Keccak (H_K) rather than Blake2b. What is s and why Keccak?",
 "options": [
  "s = [E_4(service) ⌢ E(hash) for each (service, hash) in θ′]; Keccak is used 'to maximize compatibility with legacy systems'",
  "s = the sequence of every work-report hash guaranteed in this block; Keccak is chosen because it costs less PVM gas than Blake2b",
  "s = the encoded header of the block being appended; Keccak is required because the Bandersnatch ring VRF transcript is defined over it",
  "s = [H(g_w) for each guarantee g ∈ E_G]; Keccak is mandated so that Grandpa's finality votes can be checked by the same bridge contracts"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 7.6 的 s 正是 θ′ 的 (service, hash) 編碼；§7 給的理由就是與 legacy 系統相容。",
  "work-report hash 只出現在 header 的 H_X 與 guarantee 簽章訊息；「省 PVM gas」不是 GP 給的理由。",
  "belt 的 leaf 來源是 θ′ 而非 header；附錄 G 的 ring VRF 有自己的建構，與 belt 雜湊選擇無關。",
  "簽 belt super-peak 的是 BEEFY 的 BLS 簽章（eq. 18.1），Grandpa 完全不碰 belt。",
 ],
 "explanation": "eq. 7.6：s = [E_4(s) ⌢ E(h) | (s,h) ∈ θ′]；eq. 7.7：β′_B ≡ A(β_B, M_B(s, H_K), H_K)——先用 well-balanced binary Merkle（M_B）以 Keccak 算出本塊 accumulation output 的 root，再用 MMR append（附錄 E.2）接到 belt 上。§7：「Throughout, the Keccak hash function is used to maximize compatibility with legacy systems」——EVM 有便宜的 keccak256 precompile，BEEFY（§18）就是對這個 belt 的 super-peak 做 BLS 簽章給外部系統（bridge）用，bridge 合約驗 belt 幾乎不花錢。你們的 recent_history_controller / mmr 都用 Keccak。",
 "trap": "belt 是 MMR（append-only，peaks 序列），super-peak（E.2）才是單一 32-byte commitment。"
},
{
 "id": "ch07-purpose",
 "ch": "7", "section": "7 Recent History", "gpRef": "§7 & eq. 11.36, 11.41–11.44",
 "difficulty": 1, "kind": "concept", "tags": ["recent-history"],
 "stem": "What is the primary purpose of retaining the H = 8 most recent blocks in β_H, according to the GP?",
 "options": [
  "To preclude duplicate or out-of-date work-reports: a guarantee's refinement-context anchor must appear in β† and its work-package hash must not already be a key of any recent block's reported-package map",
  "To let light clients follow the chain without state: β_H is the only place the last H = 8 header hashes are kept, so a client walks them backwards instead of reading H_P out of each header",
  "To seed the fallback slot-sealer sequence: when the ticket contest falls short, F draws E = 600 Bandersnatch keys and the hashes of the last 8 blocks in β_H supply the randomness for that draw",
  "To store the last 8 posterior state roots so that Grandpa voters can compare candidate chains without re-executing them, β_B holding the matching BLS signatures over those roots"
 ],
 "answer": 0,
 "optNotes": [
  "§7 第一句就是 preclude duplicate or out of date work-reports（eq. 11.36、11.41）。",
  "每個 header 自帶 H_P 即可往回走，且 β 是狀態，light client 反而拿不到。",
  "fallback key sequence F 的種子是 η′_2、抽的是 κ′ 的 Bandersnatch key（§6），與 β 無關。",
  "最新一筆的 s 在本塊仍是 H_0、要等下一塊 β† 補正；β_B 是 output belt，不存任何簽章。",
 ],
 "explanation": "§7 第一句：「This is used to preclude the possibility of duplicate or out of date work-reports from being submitted.」具體用途：(1) eq. 11.36：refinement context 的 anchor (hash, state root, belt super-peak, timeslot) 必須匹配 β† 的某一筆——所以 anchor 最多只能是 8 個區塊之前；(2) eq. 11.41：新 report 的 package hash 不得出現在任何 β 條目的 p 裡（防重複）；(3) eq. 11.42 / 11.44：prerequisites 與 segment-root lookup 必須在 extrinsic 或 β 的 p 裡找得到。",
 "trap": "anchor 深度 ≤ 8 blocks；lookup anchor 深度 ≤ 14,400 slots（用 ancestors A）。"
},
{
 "id": "ch08-pool-queue-sizes",
 "ch": "8", "section": "8.2 Pool and Queue", "gpRef": "eq. 8.1",
 "difficulty": 1, "kind": "concept", "tags": ["authorization", "state"],
 "stem": "What are the shapes of the authorizer pool α and authorizer queue φ?",
 "options": [
  "α ∈ [[H]_{:O}]_C with O = 8 (up to 8 authorizer hashes per core); φ ∈ [[H]_Q]_C with Q = 80 (exactly 80 per core)",
  "α ∈ [[H]_{:Q}]_C with Q = 80 (up to 80 pooled per core); φ ∈ [[H]_O]_C with O = 8 (exactly 8 queued per core)",
  "α ∈ [H]_C — one live authorizer per core, replaced every block; φ ∈ [[H]_E]_C with E = 600, one queue entry per epoch slot",
  "α and φ are both dictionaries D⟨H → N_C⟩ from authorizer hash to core index, so no hash ever repeats and no per-core length bound is needed"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 8.1：pool 是最多 O = 8 的變長序列，queue 是固定長度 Q = 80，兩個常數不互換。",
  "O 與 Q 對調了：pool 上限 8、queue 剛好 80，這是最常見的記憶錯亂。",
  "α[c] 是可容多個 hash 的序列（eq. 8.3 才需要移除最左邊一個）；queue 長度是獨立常數 Q，不隨 E 走。",
  "與 eq. 8.1 的型別直接衝突：兩者都是 per-core 序列，同一 hash 在同一 pool 重複完全合法。",
 ],
 "explanation": "eq. 8.1：α ∈ [[H]_{:O}]_C，O = C_authpoolsize = 8（最多 8 個）；φ ∈ [[H]_Q]_C，Q = C_authqueuesize = 80（固定 80 個）。pool 是「現在可以用的 authorizer」，queue 是「未來每個 slot 依序補進 pool 的 authorizer」，rotation 取的是 H_T mod Q。φ 只能由 accumulate 中具 assigner 權限（χ_A[c]）的 service 透過 `assign` host call 修改。編碼上 C(1) 為 [var(x) | x ∈ α]、C(2) 為 E(φ)。",
 "trap": "O = 8、Q = 80；pool 是 :O（可少於 8），queue 是固定長度 Q。"
},
{
 "id": "ch08-pool-update",
 "ch": "8", "section": "8.2 Pool and Queue", "gpRef": "eq. 8.2–8.3",
 "difficulty": 3, "kind": "concept", "tags": ["authorization", "calc"],
 "stem": "Core c has pool α[c] = [a, b, a, d] (left = oldest) and a guarantee in E_G for core c whose report has authorizer a. With φ′[c][H_T mod Q] = x and O = 8, what is α′[c]?",
 "options": [
  "[b, a, d, x] — the leftmost occurrence of a is removed, then x is appended, and the last O entries are kept",
  "[b, d, x] — both copies of a are removed before x is appended, because a pool never holds the same authorizer twice",
  "[a, b, a, d, x] — x is appended and nothing is removed, since F(c) only trims the pool once it already holds O = 8 entries",
  "[x, a, b, a, d] — the queue entry is prepended at the head and the used authorizer is dropped only once the pool would exceed O = 8"
 ],
 "answer": 0,
 "optNotes": [
  "⊖ 是 seqminusl（只砍最左一個）、x 接在尾端、長度 4 未達 O 不截斷，三步全對。",
  "把兩個 a 都刪掉正是 bug #692：⊖ 是 seqminusl，pool 是序列、允許重複。",
  "eq. 8.3 的條件是「E_G 裡存在 core c 的 guarantee」，與長度無關；長度只決定截斷。",
  "方向相反：eq. 8.2 把新項接在右邊，←(…)^O 丟掉的是最左邊（最舊）那個。",
 ],
 "explanation": "eq. 8.2：α′[c] ≡ ←(F(c) ⌢ φ′[c][H_T mod Q])^O；eq. 8.3：F(c) = α[c] ⊖ {w_a}（⊖ 是「移除最左邊一個」的 seqminusl 運算）當 E_G 裡有 core c 的 guarantee，否則 α[c]。所以先移除最左邊那個 a → [b, a, d]，再 append x → [b, a, d, x]，長度 4 ≤ 8 不需截斷。每個區塊每個 core 都會 append 一個（即使沒有 guarantee），滿 8 時以 ←^O 保留**最後** 8 個（丟最舊）。你們的 authorization 模組註解：remove leftmost occurrence, append φ′[c][H_T mod Q], keep last 8。",
 "trap": "H_T mod Q 用的是本塊 timeslot 對 80 取餘；用 posterior φ′。"
},
{
 "id": "ch08-authorizer-identity",
 "ch": "8", "section": "8.1 Authorizers and Authorizations", "gpRef": "§8.1 & eq. 14.11 (§14.3; delta #522)",
 "difficulty": 2, "kind": "delta", "tags": ["authorization", "delta-0.8.0"],
 "stem": "How is an authorizer identified in GP 0.8.0, and where is the authorization decision actually made?",
 "options": [
  "Authorizer = H(PVM code hash ⌢ configuration blob); the is-authorized decision is made entirely in-core by the guarantors (Ψ_I), while on-chain logic only checks that the authorizer is in the core's pool",
  "Authorizer = the is-authorized code hash alone, with the configuration blob passed to Ψ_I separately; the block author runs that code while building the block and other validators trust the trace it publishes",
  "Authorizer = H(token ⌢ trace), so the pool entry commits both to the argument supplied with the package and to the output it produced; every validator therefore re-runs Ψ_I at block import to recompute that hash",
  "Authorizer = the Ed25519 key of the coretime purchaser, so α[c] is a list of up to O = 8 buyer keys and guarantors verify a signature by one of them over the work-package hash rather than executing any PVM code"
 ],
 "answer": 0,
 "optNotes": [
  "§8.1 原文：authorizer 是 PVM code hash ⌢ config blob 的雜湊；鏈上只驗 w_a ∈ α[w_c]。",
  "eq. 14.11 的 p_a ≡ H(p_u ⌢ p_f) 已把 config 包進雜湊，且出塊者不會在鏈上跑 authorizer。",
  "把識別碼與執行結果搞混：authorizer 必須在任何執行之前就能拿去和 α[c] 比對。",
  "eq. 8.1 的 α 裝的是 hash；§8.1 定義 authorizer 是跑在 G_I = 50M gas 下的 PVM 邏輯，不是驗簽。",
 ],
 "explanation": "§8.1：「Authorizers are identified as the hash of their PVM code hash concatenated with their Configuration blob」（0.8.0 #522 統一了第 8 章與第 14 章的定義：work-package 帶 auth code hash h 與 config c，report 的 authorizer a = H(h ⌢ c)）。三個概念要分清：Token（隨 package 附的 opaque 資料）、Trace（成功授權時輸出的 opaque 資料，進 report 的 o 欄位）、Authorizer（在固定 gas G_I = 50M 下判斷是否授權的 PVM 邏輯）。「The process by which work-packages are determined to be authorized… happens entirely in-core」——不是 on-chain logic 的職責，鏈上只驗 w_a ∈ α[w_c]（eq. 11.32）。",
 "trap": "on-chain 不執行 authorizer code；只查 pool。"
},
{
 "id": "ch08-why-authorization",
 "ch": "8", "section": "8 Authorization", "gpRef": "§8 intro",
 "difficulty": 1, "kind": "rationale", "tags": ["authorization", "rationale"],
 "stem": "What motivation does the GP give for the authorization system?",
 "options": [
  "To disentangle the intention of using some coretime from the specification and submission of a particular workload, so that JAM can support both Ethereum-style and Polkadot-style interaction patterns",
  "To give each core its own gas market: guarantors bid for coretime block by block and the clearing price is recorded next to the authorizer hash in α[c], so a congested core costs more to use",
  "To replace Grandpa's finality votes with per-core authorizer votes: a work-report is final once more than two thirds of the authorizers pooled for its core have signed it, which is what the bound O = 8 sizes",
  "To cap how much work one service may submit: the pool's O = 8 entries act as a per-service rate limiter, so a service that already had a package reported this timeslot cannot have a second one guaranteed on any core"
 ],
 "answer": 0,
 "optNotes": [
  "§8 intro 的 disentangling the intention of usage…，買 coretime 與送 package 可分離。",
  "eq. 8.1 的 α 只裝 32-byte hash、沒有價格欄位，G_I / G_R 是協定常數，鏈上沒有競標。",
  "authorizer 是一段 PVM 邏輯而不是簽名者；三分之二門檻屬於 availability assurance，與它無關。",
  "α 是 per-core 而非 per-service，協定並未限制單一 service 能送幾份 package。",
 ],
 "explanation": "§8 intro：Ethereum 的 gas 由交易作者當場購買（購買者 = 作者）；Polkadot 的 parachain slot 由團隊長期租用（購買者通常 ≠ 出塊者）。「On a principle of flexibility, we would wish JAM capable of supporting a range of interaction patterns both Ethereum-style and Polkadot-style… we introduce the authorization system, a means of disentangling the intention of usage for some coretime from the specification and submission of a particular workload」——這就是「買 coretime 的人」與「提交 work-package 的人」可以不同人的來源，連結到 §4.9.2 coretime 與 §14 的 is-authorized。",
 "trap": "設計理念題常見；連結到 §4.9.2 coretime 與 §14 的 is-authorized。"
},
]
