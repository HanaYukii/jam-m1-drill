# -*- coding: utf-8 -*-
"""基礎套題 N2：區塊與狀態。只考主幹。"""

ITEMS = [
 {
  "id": "n2-block-shape",
  "ch": "N2", "section": "§4.1 The Block", "gpRef": "§4",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "block"],
  "stem": "What are the two parts of a JAM block?",
  "stemZh": "一個 JAM 區塊由哪兩個部分組成？",
  "options": [
   "A header, which is small and fixed in shape, and an extrinsic, which carries the data brought in from outside the state",
   "A header and a state root, with the block's data kept off-chain and referenced by the root so that blocks stay a constant size",
   "A list of transactions and a receipts section, mirroring the layout Ethereum uses so that existing tooling can read JAM blocks",
   "A header and a set of work-reports, since reports are the only thing a block ever carries and every other input reaches the state elsewhere"
  ],
  "optionsZh": [
   "一個 header——體積小、形狀固定，以及一份 extrinsic——承載從狀態之外帶進來的資料",
   "一個 header 與一個 state root，區塊資料存在鏈外並由該 root 指涉，因此區塊大小恆定",
   "一串交易加上一個 receipts 區段，沿用 Ethereum 的版面配置，好讓既有工具能讀 JAM 的區塊",
   "一個 header 與一組 work-report，因為 report 是區塊唯一會攜帶的東西，其他輸入都從別處進入狀態"
  ],
  "answer": 0,
  "explanation": "B ≡ (H, E)：**header 加 extrinsic**。header 是固定的十個欄位，小而可獨立傳播——輕客戶端只跟著 header 鏈走就能追上大部分變化。extrinsic 則是本塊從外界帶進來的東西，共五個成分（tickets、disputes、preimages、assurances、guarantees）。注意 work-report 只是 extrinsic 五個成分中 guarantees 那一項的內容，不是全部；而狀態本身不在區塊裡，區塊只描述「狀態怎麼變」。",
  "optNotes": [
   "header 小而固定、extrinsic 帶外部輸入，這就是 B ≡ (H, E) 的兩半。",
   "區塊資料沒有存在鏈外；extrinsic 本身就在區塊裡，只有 work-package 的內容才走鏈下。",
   "JAM 沒有使用者交易、也沒有 receipt 這一層，這是它與 Ethereum 最根本的差異之一。",
   "work-report 只是 extrinsic 五個成分之一（guarantees）的內容，不是區塊的全部。"
  ],
  "trap": "B = header + extrinsic；狀態不在區塊裡，區塊只說明狀態怎麼變。"
 },
 {
  "id": "n2-no-transactions",
  "ch": "N2", "section": "§4.1; §4.9", "gpRef": "§4",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "extrinsic"],
  "alsoCh": ["N4"],
  "stem": "JAM is described as transactionless. If there are no user transactions, how does anything from outside get into the state?",
  "stemZh": "JAM 被描述為 transactionless。既然沒有使用者交易，外界的東西要怎麼進入狀態？",
  "options": [
   "Through work-packages, which validators execute in-core and bring back as reports, and through preimages, which are blobs a service has already asked for",
   "Through a special system transaction type that only validators may sign, which wraps the user's original request and carries it into the block unchanged",
   "Through direct writes by the block author, who is trusted to apply user requests during its own slot and is punished later if it applies them incorrectly",
   "It cannot: JAM's state is closed and evolves only from its own prior contents, which is what allows the whole transition to be verified without external data"
  ],
  "optionsZh": [
   "透過 work-package——由 validator 在 core 上執行後以 report 帶回，以及透過 preimage——service 事先請求過的資料 blob",
   "透過一種只有 validator 能簽署的特殊系統交易，它把使用者的原始請求包起來、原封不動帶進區塊",
   "由出塊者直接寫入：出塊者在自己的時槽內被信任去套用使用者請求，事後若套用有誤才會被懲罰",
   "進不去：JAM 的狀態是封閉的，只從自身先前的內容演化，這正是整個轉移不需要外部資料就能被驗證的原因"
  ],
  "answer": 0,
  "explanation": "「transactionless」指的是**沒有使用者簽名的交易**——extrinsic 的五個成分全部由 validator 產生並簽署。外部資料有兩條路進來：**work-package**（使用者把工作交給某個 core，guarantor 執行 refine 後以 work-report 經 E_G 進鏈）與 **preimage**（經 E_P 把 blob 本身放進狀態，但前提是某個 service 事先用 `solicit` 請求過）。兩條路都必須先經過某個 validator，這正是「in-core 做重活、on-chain 只收結果」的直接體現。",
  "optNotes": [
   "work-package 與 preimage 是外部資料進入狀態的兩條路，都要先經過 validator。",
   "JAM 沒有任何交易型別；五個 extrinsic 成分全部由 validator 產生。",
   "出塊者不能直接寫狀態，它和其他人一樣受同一套狀態轉移規則約束。",
   "狀態當然接受外部輸入，否則這條鏈就沒有用途了。"
  ],
  "trap": "transactionless ≠ 封閉；只是外部資料必須經由 work-package 或 preimage 進來。"
 },
 {
  "id": "n2-state-components-basic",
  "ch": "N2", "section": "§4.2 The State", "gpRef": "§4",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "state"],
  "stem": "The state σ is split into many named components. What is the point of splitting it that way rather than treating it as one blob?",
  "stemZh": "狀態 σ 被拆成許多具名的分量。這樣拆而不是當成單一個大 blob，用意是什麼？",
  "options": [
   "Each component has its own transition rule and its own dependencies, so splitting them lets independent parts of a block's work be computed in parallel and reasoned about separately",
   "Each component is stored on a different core, so the split is what allows the state to be larger than any single validator could hold on its own machine",
   "Each component is Merklized into its own separate trie with its own root, and the header carries all of those roots so that a proof can target one component",
   "The split exists only for readability in the document; implementations are free to store the state however they like because the Merklization flattens it anyway"
  ],
  "optionsZh": [
   "每個分量有自己的轉移規則與自己的相依關係，拆開之後，一個區塊裡互不相干的工作就能平行計算、也能各自獨立推理",
   "每個分量存放在不同的 core 上，正是這個拆分讓狀態能大於任何單一 validator 機器所能容納的量",
   "每個分量各自 Merklize 成獨立的 trie 與獨立的 root，header 帶著所有這些 root，讓證明可以只針對某一個分量",
   "拆分只是為了文件好讀；實作可以任意選擇儲存方式，因為 Merklization 反正會把它攤平"
  ],
  "answer": 0,
  "explanation": "拆分的用意是**相依關係與平行性**。§4 給出一張狀態轉移的依賴圖，每個分量寫成「α′ ≺ (…)」的形式，明確標出它需要哪些輸入。這讓兩件事成為可能：實作可以把互不相依的部分平行算；讀規格的人可以一次只推理一個分量。狀態沒有依 core 分區（只有一份 σ），也不是每個分量一棵 trie（整個狀態進同一棵 Patricia trie、header 只帶一個 root）。拆分也不只是文件排版——依賴圖規定了計算順序，順序錯了 state root 就會不同。",
  "optNotes": [
   "各分量有自己的轉移規則與依賴，這正是依賴圖與平行計算的基礎。",
   "狀態只有一份、不依 core 分區；那是 JAM 刻意選擇單鏈的結果。",
   "整個狀態進同一棵 trie、header 只帶一個 root，不是每個分量一棵。",
   "依賴圖規定了計算順序，不是純粹的排版選擇——順序錯就算出不同的 root。"
  ],
  "trap": "分量的意義在依賴圖；狀態實體上仍然是一份、一棵 trie、一個 root。"
 },
 {
  "id": "n2-prior-state-root-basic",
  "ch": "N2", "section": "§5.1 The Header", "gpRef": "§5",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "header"],
  "alsoCh": ["N3"],
  "stem": "A JAM header carries the state root from before the block ran, not after. What does that make possible?",
  "stemZh": "JAM 的 header 帶的是區塊執行**之前**的 state root，而不是執行之後的。這讓什麼事情變得可能？",
  "options": [
   "The author can publish the block before finishing the slow Merklization of the new state, because that root is not needed until the next block is authored",
   "A verifier can check the block without holding any state at all, because the prior root is enough to confirm every field the block contains",
   "Two blocks built on the same parent are guaranteed to carry the same root, so a fork can be resolved by comparing timeslots alone without touching state",
   "The state can be Merklized lazily and skipped entirely for blocks that no service wrote to, since an unchanged state needs no new root"
  ],
  "optionsZh": [
   "出塊者可以在還沒把新狀態 Merklize 完之前就發布區塊，因為那個 root 要到下一個區塊出塊時才會被用到",
   "驗證者可以完全不持有狀態就檢查區塊，因為先前的 root 已足以確認區塊裡的每一個欄位",
   "建在同一個父區塊上的兩個區塊必定帶有相同的 root，因此分叉可以只比較時槽而不必碰狀態就解決",
   "狀態可以延遲 Merklize，而且對沒有任何 service 寫入的區塊可以整個略過，因為狀態沒變就不需要新的 root"
  ],
  "answer": 0,
  "explanation": "Merklization（走完整棵狀態 trie 算出 root）是狀態轉移裡最慢的一步。header 帶 prior root 的意思是：**本塊的執行結果要到下一塊才被承諾**，所以出塊者可以先把區塊發出去，讓傳播與 Merklization 重疊而不是排隊。GP 說得很直接——「to facilitate the pipelining of block computation and in particular of Merklization」。代價是 β_H 最新一筆的 state root 當下填不出來，只能先放零、由下一塊補正。",
  "optNotes": [
   "先發布、後 Merklize，讓傳播與計算重疊——這正是 pipelining 的意思。",
   "驗 seal 需要 κ′ 與 γ′_S，都是狀態；光有 prior root 驗不完一個 header。",
   "同一個父區塊的兩個子塊確實帶同樣的 H_R，但那是巧合而非目的，分叉也不是這樣解的。",
   "每塊都要算 root，沒有「狀態沒變就略過」這回事。"
  ],
  "trap": "prior root 換來的是 pipelining；代價是 β_H 要多一個補正步驟。"
 },
 {
  "id": "n2-why-state-root",
  "ch": "N2", "section": "§4.2; App. D", "gpRef": "§4 & App. D",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "merklization"],
  "stem": "Why does the state get reduced to a single 32-octet root at all?",
  "stemZh": "為什麼要把整個狀態壓縮成單一個 32 位元組的 root？",
  "options": [
   "So that two nodes can compare their entire state by comparing one value, and so that anyone can prove a single entry's value with a short path instead of the whole state",
   "So that the state can be stored in the header, which keeps a full copy of every service's data available to light clients without any further requests",
   "So that the state can be compressed for transmission, with the root acting as the checksum that tells a receiving node the compression was applied correctly",
   "So that services cannot read each other's storage, since only the root is visible on-chain and the underlying entries stay private to each service"
  ],
  "optionsZh": [
   "讓兩個節點只要比較一個值就能比對整份狀態，也讓任何人都能用一條短路徑證明某一筆資料的值，而不必出示整個狀態",
   "讓狀態可以被存進 header，使輕客戶端不必再發出任何請求就能取得每個 service 的完整資料副本",
   "讓狀態能被壓縮以便傳輸，root 則充當檢查碼，告訴接收端壓縮有被正確套用",
   "讓 service 無法讀取彼此的 storage，因為鏈上只看得到 root，底層的資料項對各個 service 保持私有"
  ],
  "answer": 0,
  "explanation": "Merkle root 買到兩件事。**其一是比對**：兩個節點只要 root 相同，整份狀態就相同——共識因此不必逐項比對。**其二是證明**：任何人可以用一條從葉子到 root 的路徑（深度乘以節點大小）證明「某個 key 的值是什麼」，而不必持有或傳送整個狀態，這是輕客戶端與跨鏈橋接的基礎。root 不會被存進 header 之外的地方，也跟壓縮、隱私都無關——狀態內容本身是公開的。",
  "optNotes": [
   "一個值就能比對全部、一條短路徑就能證明單筆——這是 Merkle root 的兩個用途。",
   "header 帶的是 root 不是狀態本身；狀態遠大於任何 header 能容納的量。",
   "root 是承諾不是檢查碼，跟壓縮無關。",
   "Merklization 不提供隱私；狀態內容是公開的，service 之間的隔離靠的是 host call 的權限規則。"
  ],
  "trap": "root 的兩個用途：比對整份狀態、證明單一筆資料。"
 },
 {
  "id": "n2-extrinsic-hash-basic",
  "ch": "N2", "section": "§5.1", "gpRef": "§5",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "header"],
  "stem": "The header does not contain the extrinsic itself, only a hash of it. What does that hash have to support, beyond simply detecting tampering?",
  "stemZh": "header 並不包含 extrinsic 本身，只有它的雜湊。除了偵測竄改之外，這個雜湊還必須支援什麼？",
  "options": [
   "Proving that one particular preimage or one particular report was included, without having to hand over the rest of the block's extrinsic data",
   "Reconstructing the extrinsic from the hash alone, so that a node which has lost the block body can recover it from the header it already holds",
   "Ordering the extrinsic components, since the hash is computed over them in sequence and a verifier recovers the intended order from the hash value",
   "Bounding the extrinsic's size, because the hashing scheme only accepts inputs below a fixed length and so caps how much a block may carry"
  ],
  "optionsZh": [
   "證明某一份特定的 preimage 或某一份特定的 report 有被納入，而不必交出區塊其餘的 extrinsic 資料",
   "單憑雜湊重建出 extrinsic，讓遺失了區塊本體的節點能從手上已有的 header 把它復原",
   "決定 extrinsic 各成分的順序，因為雜湊是依序對它們計算的，驗證者能從雜湊值還原出預期的順序",
   "限制 extrinsic 的大小，因為該雜湊方案只接受低於固定長度的輸入，因而限制了一個區塊能攜帶的量"
  ],
  "answer": 0,
  "explanation": "H_X 不是把整份 extrinsic 直接雜湊，而是**五個成分各自先雜湊、再一起雜湊**，而且 preimage 與 guarantee 這兩個成分內部還把每一項換成它自己的雜湊。GP 說明理由是「taking care to allow for the possibility of reports and preimages to individually have their inclusion proven」——要能單獨證明某一筆被納入。這樣做的好處是證明時不必搬運整份資料：一份 work-report 可能接近 48 KiB，preimage 更是任意大小。雜湊當然無法反推原文，也不決定順序或大小上限。",
  "optNotes": [
   "單獨證明某筆被納入而不必交出其餘資料，正是這個兩層結構的目的。",
   "雜湊是單向的，無法從中重建原始資料。",
   "順序由編碼規格決定，不是從雜湊值還原出來的。",
   "大小上限由 W_R 之類的常數規定，跟雜湊函數的輸入長度無關。"
  ],
  "trap": "H_X 是兩層結構，為的是「單獨證明某一筆存在」而不是只防竄改。"
 },
 {
  "id": "n2-what-a-transition-is",
  "ch": "N2", "section": "§4.2", "gpRef": "§4",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "stf"],
  "stem": "What does it mean to say a node 'imports' a block?",
  "stemZh": "說一個節點「import」一個區塊，是什麼意思？",
  "options": [
   "It re-runs the state transition the block describes, from the state it already holds, and checks that every commitment in the header matches what it computed",
   "It downloads the block and stores it, then trusts the header's signatures to attest that the transition was performed correctly by the block's author",
   "It asks the validators who authored the block for a proof of the new state root, and accepts the block once enough of them have signed that proof",
   "It applies the block's changes optimistically and rolls them back later only if an auditor raises a dispute about one of the reports it contained"
  ],
  "optionsZh": [
   "它從自己手上已有的狀態出發，重新執行該區塊所描述的狀態轉移，並檢查 header 裡的每一項承諾都與自己算出來的相符",
   "它下載並保存該區塊，然後信任 header 上的簽章，以此證明轉移已由該區塊的出塊者正確執行",
   "它向出塊的 validator 索取新 state root 的證明，等到足夠多人簽署了該證明就接受這個區塊",
   "它樂觀地套用該區塊的變更，只有當 auditor 對其中某份 report 提出爭議時才回滾"
  ],
  "answer": 0,
  "explanation": "import 就是**自己重跑一遍再對答案**。節點從自己持有的 prior state 出發，照規格執行區塊描述的轉移，然後檢查 header 的每一項承諾——H_R 對得上父塊的 posterior root、H_X 對得上實際的 extrinsic、marker 對得上 Safrole 與 disputes 算出來的值、seal 由該 slot 該出塊的人簽。任何一項對不上，區塊就是無效。這裡沒有「信任出塊者」的空間；簽章證明的是「誰出的塊」，不是「他算對了」。真正沒有全網重跑的只有 in-core 那一段，而那一段靠稽核補上。",
  "optNotes": [
   "重跑轉移、逐項核對承諾——這就是 import，沒有信任的成分。",
   "簽章只證明出自誰之手，不證明計算正確；正確性靠每個人自己重算。",
   "沒有這種索取 root 證明的流程；每個節點自己算得出 root。",
   "on-chain 的部分不是樂觀執行；樂觀加稽核的是 in-core 那一段。"
  ],
  "trap": "on-chain 全體重跑、逐項對承諾；只有 in-core 那段才是樂觀加稽核。"
 },
 {
  "id": "n2-header-vs-state",
  "ch": "N2", "section": "§5.1; §5.3", "gpRef": "§5",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "header", "light-client"],
  "alsoCh": ["N3"],
  "stem": "Someone follows only the chain of headers and never downloads a block body or any state. What can they still keep track of, and what stops them?",
  "stemZh": "有人只跟著 header 鏈走，從不下載區塊本體或任何狀態。他仍然能追蹤什麼？又會卡在哪裡？",
  "options": [
   "They can follow which validators are in charge, because the markers announce key and ticket changes in the header itself; they cannot verify anything that depends on reading the state",
   "They can verify the whole transition, because every commitment the header carries is self-contained; nothing about the block requires them to consult the state at all",
   "They can track balances and service storage, since both are summarized in the state root each header carries; what they cannot see is which validator authored the block",
   "They can track nothing useful, since headers commit to state they cannot read; the protocol expects every participant to hold the full state and offers no header-only mode"
  ],
  "optionsZh": [
   "他能追蹤由誰負責出塊，因為 marker 直接在 header 裡公告金鑰與 ticket 的變化；但凡是需要讀取狀態才能判定的事情，他都驗不了",
   "他能驗證整個轉移，因為 header 帶的每一項承諾都是自足的；這個區塊沒有任何一處需要他去查閱狀態",
   "他能追蹤餘額與 service 的 storage，因為兩者都摘要在每個 header 帶的 state root 裡；他看不到的是這個區塊由哪位 validator 出的",
   "他什麼有用的都追蹤不了，因為 header 承諾的是他讀不到的狀態；協定預期每個參與者都持有完整狀態，並未提供只看 header 的模式"
  ],
  "answer": 0,
  "explanation": "這正是 **marker 存在的理由**。只讀 header 的人沒有狀態，所以像 seal 這種需要知道「這個 slot 該由誰出塊」的檢查他做不了——那來自 γ′_S 與 κ′，都在狀態裡。但 header 帶了三個 marker：epoch marker 公告下個 epoch 的 entropy 與整組 validator 金鑰、winning-tickets marker 公告該 epoch 的出塊表、offenders marker 公告誰被剔除。有了它們，輕客戶端就能自己推出 validator 集合的變化，往後一路驗下去。至於 state root，它只是一個承諾——要讀出裡面某筆資料，還需要對方提供 Merkle 證明。",
  "optNotes": [
   "marker 讓 header-only 的人跟上 validator 變化，而狀態相關的檢查仍然做不到。",
   "seal 的驗證需要 κ′ 與 γ′_S，兩者都在狀態裡，所以 header 並非自足。",
   "state root 是承諾不是內容；要讀某筆資料還需要別人給 Merkle 證明。",
   "協定確實照顧了 header-only 的參與者，marker 就是為他們設計的。"
  ],
  "trap": "header-only 能跟上「誰負責」，跟不上「狀態是什麼」——除非有人給你證明。"
 },
]
