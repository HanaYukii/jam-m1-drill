# -*- coding: utf-8 -*-
# Chapter 7 — Recent History; Chapter 8 — Authorization (GP 0.8.0)
ITEMS = [
{
 "id": "ch07-beta-structure",
 "ch": "7", "section": "7 Recent History", "gpRef": "eq. 7.1–7.4",
 "difficulty": 2, "kind": "concept", "tags": ["recent-history", "state"],
  "stemZh": "在 GP 0.8.0 中，recent-history 狀態是 β ≡ (β_H, β_B)。β_H 的每一筆近期區塊條目裝什麼？β_B 又是什麼？",
  "optionsZh": [
   "每筆 β_H 條目為：(header 雜湊 h, state root s, accumulation-output log 的 super-peak b, 時槽 t, 從被回報的 work-package 雜湊映到 segment root 的字典 p)；β_B 是 accumulation-output belt，一個由每塊 accumulation-output root 構成的 MMR",
   "每筆 β_H 條目為：(header 雜湊, posterior state root, extrinsic 雜湊, 時槽)；β_B 是最近 H = 8 個區塊上蒐集到的 BEEFY 簽章集合，這正是橋接方不必跟隨 header 鏈也能證明 finality 的憑藉",
   "每筆 β_H 條目為：(header 雜湊, state root, 時槽, 該區塊中每份被擔保 work-report 的雜湊清單)；β_B 是最近 H = 8 個區塊 header 的序列，保留它是為了讓 lookup-anchor 能直接從狀態解出",
   "β_H 是一個承諾最近 H = 8 個 header 的滾動雜湊，所以近期歷史只佔 32 個位元組的狀態；β_B 是四項的熵累積器，在每個 epoch 邊界輪替並由每個 header 的 VRF 輸出重新播種"
  ],
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
 "explanation": "β ≡ (β_H, β_B) 是兩個目的不同的東西被放在同一個狀態分量裡。**β_H（recent history）**（eq. 7.2）：β_H ∈ ⟦(h, s, b, t, p)⟧_{:H}，最多 H = 8 筆，每筆是h = header hash、s = state root、b = accumulation-output log 的 super-peak、t = timeslot（**0.8.0 新增**，配合 refinement context 的 anchor slot，PR #526）、p = 一個字典，把本塊 E_G 裡每個 work-package hash 映到它的 segment root（exports root）。**p 是最容易被忽略但用途最多的欄位**：後續 report 的重複檢查、prerequisite 檢查、segment-root lookup 全都要查它（§11）。**β_B（accumulation-output belt）**（eq. 7.3）：β_B ∈ ⟦?H⟧，是一個 MMR 的 peak 序列（∅ 代表該高度沒有 peak），用 Keccak 而不是 Blake2b。**兩者的時間尺度完全不同**：β_H 是滑動窗口，只留 8 筆、舊的直接丟；β_B 是 append-only、永不遺忘，因為它要支撐鏈外幾個月後回來驗的 BEEFY 證明。**θ 不在 β 裡**（eq. 7.4）：θ ∈ ⟦(N_S, H)⟧ 是**本塊**各 service 透過 `yield` 產出的 (service, hash) 序列，它是 β_B 這一輪的輸入，本身是獨立的狀態分量。",
 "trap": "0.8.0 β_H 有 5 個欄位（多了 timeslot）；p 的 value 是 segment root 不是 report hash。"
},
{
 "id": "ch07-beta-dagger",
 "ch": "7", "section": "7 Recent History", "gpRef": "eq. 7.5 & 7.8",
 "difficulty": 2, "kind": "concept", "tags": ["recent-history", "pipelining"],
  "stemZh": "為什麼區塊 N 結束時，β_H 最新的那筆條目其 state root s = H_0（零雜湊）？它又是怎麼被補正的？",
  "optionsZh": [
   "因為算 β′ 的當下還不知道區塊 N 執行後的 state root（header 帶的是先前的 root）；區塊 N+1 會在任何人讀取 β 之前，用自己的 H_R 覆寫最後一筆的 s 來算出 β†（eq. 7.5）",
   "因為 state root 要到區塊被定案後才有意義：該條目會保持 H_0 直到 Grandpa 定案區塊 N，屆時 finality gadget 會把真正的 root 寫進該條目，eq. 11.36 也才開始接受以它為 anchor",
   "因為 β_H 的條目根本不帶 state root：eq. 7.2 宣告一個項目為 ⟨h, b, t, p⟩，零雜湊只是 C(3) 會略過的佔位符，所以 eq. 11.36 只憑 header 雜湊、super-peak 與時槽來比對 anchor",
   "因為 root 是放進 β_B 而不是這裡：每個區塊把自己執行後的 state root 當成 belt 的下一片葉子附加上去，所以 β_H 的項目可以永遠把 s 留在 H_0，而 anchor 的 state root 是拿去對照 b"
  ],
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
 "explanation": "**根因是 header 帶的是 prior state root**（H_R = 父塊的 posterior root），為的是 pipelining——出塊者不必先算完 Merklization 才能發布。代價就是：算 β′ 的當下，本塊自己的 posterior root 還不存在。**GP 的處理是先填零再補正**。eq. 7.8 定義新 entry 為 (H(H), H_0, super-peak(β′_B), H_T, p)，其中 state root 那格是 H_0（零雜湊）；§7 說明「The new state-trie root is the zero hash, which is inaccurate but safe since β′ is not utilized except to define the next block's β†」——**安全的原因是它在被補正之前不會被任何人讀到**。eq. 7.5：β† ≡ β_H 但 β†[|β_H| − 1]_s = H_R——下一個區塊一開始就用自己的 H_R 把父塊那格補上。**時序很重要**：β† 必須在**驗證 guarantee 的 anchor 之前**算好，因為 eq. 11.36 要拿 anchor 的 state root 去比對 β† 的內容——比對的對象若還是零，所有 anchor 都會失敗。你們的 STF 在 τ′ 與 header 檢查之後、disputes 之前就算 β†，順序是對的。**口試常見追問**：「為什麼不乾脆讓 header 帶 posterior root？」——那就等於要求出塊者序列化地跑完 Merklization，pipelining 的好處整個消失，這個零雜湊是換來並行的代價。",
 "trap": "guarantee 的 anchor 檢查（eq. 11.36）比對的是 β†（補正後），不是 β。"
},
{
 "id": "ch07-belt-keccak",
  "alsoCh": ["E"],
 "ch": "7", "section": "7 Recent History", "gpRef": "eq. 7.6–7.7",
 "difficulty": 2, "kind": "rationale", "tags": ["recent-history", "mmr", "beefy"],
  "stemZh": "accumulation-output belt β′_B = A(β_B, M_B(s, H_K), H_K) 用的是 Keccak（H_K）而不是 Blake2b。s 是什麼？為什麼用 Keccak？",
  "optionsZh": [
   "s = [對 θ′ 中每個 (service, hash) 取 E_4(service) ⌢ E(hash)]；使用 Keccak 是「為了最大化與既有系統的相容性」",
   "s = 本區塊中每份被擔保 work-report 的雜湊序列；選用 Keccak 是因為它比 Blake2b 花費更少的 PVM gas",
   "s = 正被附加的那個區塊的編碼後 header；必須用 Keccak，因為 Bandersnatch ring VRF 的 transcript 是定義在它之上的",
   "s = [對每個 guarantee g ∈ E_G 取 H(g_w)]；規定用 Keccak 是為了讓 Grandpa 的 finality 投票能被同一批橋接合約檢查"
  ],
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
 "explanation": "eq. 7.6：s = [E_4(service) ⌢ E(hash) | (service, hash) ∈ θ′]——把本塊的 accumulation output 逐筆編碼成 blob。eq. 7.7：β′_B ≡ A(β_B, M_B(s, H_K), H_K)——**兩層結構**：先用 well-balanced binary Merkle（M_B，附錄 E）把本塊的 s 壓成一個 root，再用 MMR 的 append 函數 A（附錄 E.2）接到 belt 上。所以 belt 每塊只長一個 peak，而塊內有幾個 service 產出則由 M_B 那層吸收。**為什麼是 Keccak 不是 Blake2b**：§7 直接寫明「Throughout, the Keccak hash function is used to maximize compatibility with legacy systems」。具體是誰在用：BEEFY（§18）對這條 belt 的 super-peak 做 BLS 簽章，交給**外部系統**（主要是 EVM 橋接合約）驗證；而 EVM 有便宜的 keccak256 precompile，Blake2b 則沒有——換句話說這個選擇不是為了 JAM 自己，是為了讓別人驗得起。**注意 H_K 只在這一條路徑上出現**：狀態 trie、header、extrinsic 雜湊全都用 Blake2b（§3.8 的 H）。把兩者搞混會讓 belt 的 root 對不上，而且只有在跟外部橋接對接時才會爆——很難查。",
 "trap": "belt 是 MMR（append-only，peaks 序列），super-peak（E.2）才是單一 32-byte commitment。"
},
{
 "id": "ch07-purpose",
  "alsoCh": ["11"],
 "ch": "7", "section": "7 Recent History", "gpRef": "§7 & eq. 11.36, 11.41–11.44",
 "difficulty": 1, "kind": "concept", "tags": ["recent-history"],
  "stemZh": "依 GP，在 β_H 中保留最近 H = 8 個區塊的主要目的是什麼？",
  "optionsZh": [
   "防止重複或過期的 work-report：一份 guarantee 的 refinement-context anchor 必須出現在 β† 裡，而它的 work-package 雜湊不得已經是任何近期區塊之 reported-package 映射的 key",
   "讓輕客戶端不必持有狀態就能跟隨這條鏈：β_H 是唯一保存最近 H = 8 個 header 雜湊的地方，客戶端因此可以往回走訪它們，而不必從每個 header 讀出 H_P",
   "為 fallback 的 slot-sealer 序列提供種子：當 ticket 競賽不足額時，F 會抽出 E = 600 把 Bandersnatch 金鑰，而 β_H 裡最近 8 個區塊的雜湊就是那次抽取的隨機性來源",
   "保存最近 8 個執行後的 state root，好讓 Grandpa 的投票者不必重新執行就能比較候選鏈，而 β_B 則持有對那些 root 的對應 BLS 簽章"
  ],
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
 "explanation": "§7 第一句就給了答案：「This is used to preclude the possibility of duplicate or out of date work-reports from being submitted.」**防重複、防過期，兩件事。****防過期**（eq. 11.36）：refinement context 的 anchor——(header hash, state root, belt super-peak, timeslot)——必須能在 β† 裡找到完全相符的一筆。因為 β_H 只留 H = 8 筆，這等於規定 **anchor 最多只能是 8 個區塊之前**，report 不能拿很舊的鏈狀態當前提。**防重複**（eq. 11.41）：新 report 的 work-package hash 不得出現在任何 β 條目的 p 字典裡——同一份工作不能被重複計酬或重複 accumulate。**還有兩個附帶用途**（eq. 11.42、11.44）：prerequisite 與 segment-root lookup 所指的 package，必須在本塊的 extrinsic 裡、或在 β 的 p 裡找得到，否則依賴關係就懸空了。**為什麼是 8 而不是更多**：窗口越長，節點要保存與掃描的資料越多；8 塊約 48 秒，足夠涵蓋 guarantee 從產生到進鏈的正常延遲（一個 rotation R = 10 個時槽），又不會讓檢查成本失控。**注意這與 L = 14,400 的 ancestor 窗口是兩回事**：後者存的是 header 序列、供 lookup anchor 用。",
 "trap": "anchor 深度 ≤ 8 blocks；lookup anchor 深度 ≤ 14,400 slots（用 ancestors A）。"
},
{
 "id": "ch08-pool-queue-sizes",
 "ch": "8", "section": "8.2 Pool and Queue", "gpRef": "eq. 8.1",
 "difficulty": 1, "kind": "concept", "tags": ["authorization", "state"],
  "stemZh": "authorizer pool α 與 authorizer queue φ 的形狀各是什麼？",
  "optionsZh": [
   "α ∈ [[H]_{:O}]_C，O = 8（每個 core 至多 8 個 authorizer 雜湊）；φ ∈ [[H]_Q]_C，Q = 80（每個 core 恰好 80 個）",
   "α ∈ [[H]_{:Q}]_C，Q = 80（每個 core 至多 80 個在池中）；φ ∈ [[H]_O]_C，O = 8（每個 core 恰好 8 個在佇列中）",
   "α ∈ [H]_C——每個 core 一個現行 authorizer、每塊替換；φ ∈ [[H]_E]_C，E = 600，每個 epoch 時槽一筆佇列項目",
   "α 與 φ 都是從 authorizer 雜湊映到 core 索引的字典 D⟨H → N_C⟩，所以同一個雜湊永遠不會重複、也不需要每個 core 的長度上限"
  ],
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
 "explanation": "eq. 8.1：**α ∈ ⟦⟦H⟧_{:O}⟧_C**，O = C_authpoolsize = 8——每個 core **最多** 8 個（注意是 `:O`，上界不是定值）；**φ ∈ ⟦⟦H⟧_Q⟧_C**，Q = C_authqueuesize = 80——每個 core **恰好** 80 個（定長）。兩者都是每個 core 一份，所以外層是 ⟦…⟧_C。**分工**：α 是「現在這個 core 可以用哪些 authorizer」，是 guarantor 檢查 report 時實際比對的清單；φ 是「未來要依序補進 α 的排程」，每個時槽從 φ[c][H_T mod Q] 取一筆補進去。取模讓 φ 變成一個循環排程——**80 個時槽（8 分鐘）繞一圈**，所以一份 φ 可以持續供給而不必頻繁改寫。**誰能改**：φ 只能由 accumulate 期間具 assigner 權限的 service 透過 `assign` host call 修改，而 assigner 是**每個 core 各自指定**的（χ_A[c]），不是全域單一權限——這讓不同 core 可以由不同的 service 掌管授權策略。α 則沒有人能直接寫，它完全由 eq. 8.2 的規則推導。**編碼**：狀態 trie 裡 C(1) 存 [var(x) | x ∈ α]、C(2) 存 E(φ)。",
 "trap": "O = 8、Q = 80；pool 是 :O（可少於 8），queue 是固定長度 Q。"
},
{
 "id": "ch08-pool-update",
 "ch": "8", "section": "8.2 Pool and Queue", "gpRef": "eq. 8.2–8.3",
 "difficulty": 3, "kind": "concept", "tags": ["authorization", "calc"],
  "stemZh": "core c 的 pool 為 α[c] = [a, b, a, d]（左邊最舊），而 E_G 中有一份指向 core c 的 guarantee，其 report 的 authorizer 是 a。已知 φ′[c][H_T mod Q] = x 且 O = 8，α′[c] 是什麼？",
  "optionsZh": [
   "[b, a, d, x]——最左邊那個 a 被移除，接著附加 x，最後保留最後 O 筆",
   "[b, d, x]——兩個 a 都在附加 x 之前被移除，因為一個 pool 絕不會同時持有兩個相同的 authorizer",
   "[a, b, a, d, x]——附加 x 而不移除任何東西，因為 F(c) 只有在 pool 已經持有 O = 8 筆時才會修剪",
   "[x, a, b, a, d]——佇列項目被插在最前面，而被使用掉的 authorizer 只有在 pool 將超過 O = 8 時才會被丟棄"
  ],
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
 "explanation": "eq. 8.2：α′[c] ≡ ←(F(c) ⌢ φ′[c][H_T mod Q])^O；eq. 8.3：F(c) = α[c] ⊖ {w_a} 當 E_G 裡有 core c 的 guarantee，否則就是 α[c] 原封不動。三步驟依序做：**① 移除**——⊖ 是「只移除**最左邊那一個**符合的元素」（sequence-minus-leftmost），不是移除全部。[a, b, a, d] 移掉最左的 a 得 [b, a, d]，**第二個 a 留著**。**② 補一個**——把 φ′[c][H_T mod Q] 接到尾端，得 [b, a, d, x]。注意這一步**每塊每個 core 都做，即使該 core 這塊沒有 guarantee**——所以 pool 會自然汰換。**③ 截斷**——←(…)^O 保留**最後** O = 8 個（丟最舊的）。本題長度只有 4，不需截斷。**為什麼是「移除最左邊一個」而不是全部**：同一個 authorizer 可以合法地在 pool 裡出現多次（φ 排程裡重複排入即可），代表它有多個可用額度；一次用掉一個才符合語意。你們的 issue #692/#694 就是這個 bug——原本刪掉了所有出現，等於一次消耗掉全部額度。**另一個 0.8.0 的變動**：pool 更新在 accumulation **之後**才做，用的是 posterior 的 φ′（issue #1020），因為 accumulate 期間的 `assign` 可能剛改過佇列。",
 "trap": "H_T mod Q 用的是本塊 timeslot 對 80 取餘；用 posterior φ′。"
},
{
 "id": "ch08-authorizer-identity",
 "ch": "8", "section": "8.1 Authorizers and Authorizations", "gpRef": "§8.1 & eq. 14.11 (§14.3; delta #522)",
 "difficulty": 2, "kind": "delta", "tags": ["authorization", "delta-0.8.0"],
  "stemZh": "在 GP 0.8.0 中，一個 authorizer 是怎麼被識別的？授權的判定實際上在哪裡進行？",
  "optionsZh": [
   "authorizer = H(PVM code hash ⌢ 設定 blob)；is-authorized 的判定完全由 guarantor 在 core 內進行（Ψ_I），鏈上邏輯只檢查該 authorizer 是否在該 core 的 pool 裡",
   "authorizer = 單獨的 is-authorized code hash，設定 blob 另外傳給 Ψ_I；出塊者在建構區塊時執行那段程式碼，其他 validator 則信任它公布的 trace",
   "authorizer = H(token ⌢ trace)，所以 pool 項目同時承諾了隨 package 提供的引數與它產生的輸出；因此每位 validator 在區塊匯入時都要重跑 Ψ_I 以重算該雜湊",
   "authorizer = coretime 購買者的 Ed25519 金鑰，所以 α[c] 是一份至多 O = 8 個買家金鑰的清單；guarantor 驗證的是其中之一對 work-package 雜湊的簽章，而不執行任何 PVM 程式碼"
  ],
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
  "stemZh": "GP 為授權系統給出的動機是什麼？",
  "optionsZh": [
   "把「打算使用某段 coretime」這個意圖，與「指定並提交某個特定工作負載」這件事解耦，好讓 JAM 能同時支援 Ethereum 式與 Polkadot 式的互動模式",
   "給每個 core 自己的 gas 市場：guarantor 逐塊競標 coretime，成交價記錄在 α[c] 中 authorizer 雜湊的旁邊，因此壅塞的 core 使用起來更貴",
   "用每個 core 的 authorizer 投票取代 Grandpa 的 finality 投票：當某份 work-report 獲得該 core 池中超過三分之二 authorizer 的簽署即為最終，而 O = 8 這個上限正是為此而設",
   "限制單一 service 可提交多少工作：pool 的 O = 8 個項目扮演每個 service 的速率限制器，所以本時槽已經有 package 被回報的 service，不能在任何 core 上再讓第二份被擔保"
  ],
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
