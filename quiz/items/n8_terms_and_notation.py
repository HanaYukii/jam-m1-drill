# -*- coding: utf-8 -*-
"""基礎套題 N8：名詞與符號。考的是「這個字／這個符號指什麼」，加幾題把名詞串成跨章節 flow。"""

ITEMS = [
{
 "id": "n8-prime-dagger-reading",
 "lens": "時機",
 "ch": "N8",
 "section": "§3 notation; §4.1",
 "gpRef": "§3.x, eq. 4.1, §4.1 dependency graph",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "guarantee",
  "prior/posterior"
 ],
 "stem": "You see σ, σ′, ρ† and ρ‡ in one formula. What does each decoration mean?",
 "stemZh": "同一條公式裡出現 σ、σ′、ρ† 和 ρ‡。這些記號各代表什麼？",
 "options": [
  "No mark is the state before this block (prior); a prime ′ is the state after it (posterior); † and ‡ are intermediate values inside the transition, after some but not all of the block has been applied",
  "No mark is the state after this block; a prime ′ is the previous block's state; † and ‡ mark values that were finalized by GRANDPA one and two epochs ago respectively — the older the mark, the older the value",
  "No mark is the on-chain value; a prime ′ is the in-core copy that guarantors work with; † and ‡ are the two erasure-coded halves that assurers hold",
  "No mark is the full state; a prime ′ is its Merkle root; † is the header's commitment to it and ‡ the commitment carried in the next block's header"
 ],
 "optionsZh": [
  "沒記號是這個 block 之前的 state（prior）；撇 ′ 是之後的（posterior）；† 和 ‡ 是轉移過程中的中間值，block 已經套用了一部分、還沒全部套完",
  "沒記號是這個 block 之後的 state；撇 ′ 是上一個 block 的；† 和 ‡ 分別代表被 GRANDPA 在一個和兩個 epoch 前定案的值——記號越多代表越舊",
  "沒記號是鏈上的值；撇 ′ 是 guarantor 在 core 上用的副本；† 和 ‡ 是 assurer 持有的兩半 erasure 分片",
  "沒記號是完整 state；撇 ′ 是它的 Merkle root；† 是 header 對它的承諾、‡ 是下一個 block 的 header 帶的承諾"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 4.1 寫 σ′ = Υ(σ, B)，σ 是輸入、σ′ 是輸出；依賴圖裡 ρ†（吃完 E_D）、ρ‡（吃完 E_A）都是同一個 block 內的中途值。",
  "撇是「之後」不是「之前」；† ‡ 與 finality 無關。",
  "這些記號全是鏈上 state transition 的東西，跟 in-core 副本、erasure 分片無關。",
  "Merkle root 寫成 M_σ(σ)，header 的承諾是 H_R；† ‡ 不是承諾。"
 ],
 "explanation": "GP 全篇的時間記號只有三種。**沒記號**：這個 block 開始前的值，也就是上一個 block 結束時的 state；**撇 ′**：這個 block 結束後的值；**† 和 ‡**：block 內部的中途值——轉移分好幾步，某個分量在第一步之後、第二步之前的樣子。最常見的例子是 ρ：ρ 是開始前，ρ† 是 disputes 處理完、ρ‡ 是 assurance 處理完、ρ′ 是 guarantee 也收完。看到 † 就問「已經做了哪一步、還沒做哪一步」，答案在 §4 的依賴圖裡（例如 ρ† ≺ (E_D, ρ)）。這個約定不在 §3 的記號章，而是在 §4.1 隨著 σ′ ≡ Υ(σ, B) 一起定的，口試常被拿來開場。",
 "trap": "撇是「之後」。看到 † ‡ 先想「做到哪一步了」。"
},
{
 "id": "n8-type-brackets",
 "lens": "機制",
 "ch": "N8",
 "section": "§3.4–3.7 sets, sequences, dictionaries",
 "gpRef": "§3.4, §3.5, §3.7",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "notation"
 ],
 "stem": "How do you read ⟦T⟧, ⟦T⟧_n, ⟦T⟧_{:n}, {T}, ⟨K → V⟩ and T? in a GP type declaration?",
 "stemZh": "GP 的型別宣告裡，⟦T⟧、⟦T⟧_n、⟦T⟧_{:n}、{T}、⟨K → V⟩、T? 各怎麼讀？",
 "options": [
  "⟦T⟧ a sequence of T; ⟦T⟧_n exactly n of them; ⟦T⟧_{:n} at most n; {T} a set (no order, no duplicates); ⟨K → V⟩ a dictionary from K to V; T? either a T or ∅ (absent)",
  "⟦T⟧ a set of T; ⟦T⟧_n the n-th element; ⟦T⟧_{:n} the first n elements; {T} a sequence; ⟨K → V⟩ a function type; T? a T that may be invalid (∇)",
  "⟦T⟧ a Merkle tree of T; ⟦T⟧_n its depth; ⟦T⟧_{:n} its first n leaves; {T} the root; ⟨K → V⟩ a trie keyed by K; T? a T whose hash is stored instead of the value",
  "⟦T⟧ a blob of T octets; ⟦T⟧_n a blob of n octets; ⟦T⟧_{:n} a blob up to n octets; {T} a hash of T; ⟨K → V⟩ a lookup table; T? a T encoded with a leading 0/1 byte only"
 ],
 "optionsZh": [
  "⟦T⟧ 是 T 的序列；⟦T⟧_n 恰好 n 個；⟦T⟧_{:n} 至多 n 個；{T} 是集合（無序、不重複）；⟨K → V⟩ 是 K 到 V 的字典；T? 是「一個 T 或 ∅（缺席）」",
  "⟦T⟧ 是 T 的集合；⟦T⟧_n 是第 n 個元素；⟦T⟧_{:n} 是前 n 個元素；{T} 是序列；⟨K → V⟩ 是函數型別；T? 是「可能無效（∇）的 T」",
  "⟦T⟧ 是 T 的 Merkle 樹；⟦T⟧_n 是深度；⟦T⟧_{:n} 是前 n 片葉子；{T} 是 root；⟨K → V⟩ 是以 K 為 key 的 trie；T? 是「存雜湊不存值」的 T",
  "⟦T⟧ 是 T 個 octet 的 blob；⟦T⟧_n 是 n 個 octet 的 blob；⟦T⟧_{:n} 是至多 n 個 octet 的 blob；{T} 是 T 的雜湊；⟨K → V⟩ 是查表；T? 是「只用一個 0/1 前綴位元組編碼」的 T"
 ],
 "answer": 0,
 "optNotes": [
  "對：§3.7 序列與下標、§3.4 集合、§3.5 字典、§3.3 optional。",
  "⟦⟧ 是序列不是集合、{} 是集合不是序列；T? 是 ∅ 不是 ∇。",
  "跟 Merkle 完全無關；Merklization 的記號是 M、M_B、M_σ。",
  "blob 的記號是 B、B_n；這裡講的是抽象型別，不是編碼。"
 ],
 "explanation": "§3 定的六個容器記號：**⟦T⟧** 序列（有序、可重複），下標 **_n** 表示長度恰好 n（例：⟦H⟧_4 就是四個 hash，η 的型別），**_{:n}** 表示長度至多 n（例：α[c] ∈ ⟦H⟧_{:O} 是最多 8 個 authorizer hash）；**{T}** 集合（無序、不重複，例：ψ_G ∈ {H}）；**⟨K → V⟩** 字典（例：δ ∈ ⟨N_S → A⟩，service index 對到 account）；**T?** optional，值是 T 或 ∅，例如 ρ 的每格是 (𝔾, N_T)?，core 沒有 report 時就是 ∅。與 ∅ 相對的 **∇** 是「無效／出錯」，不是缺席。實作對應：⟦⟧ 是 slice、{} 是 set、⟨→⟩ 是 map、? 是 pointer 或 Option。",
 "trap": "⟦⟧ 序列、{} 集合、⟨→⟩ 字典、? 可缺席。下標 _n 恰好、_{:n} 至多。"
},
{
 "id": "n8-hash-encode-concat",
 "lens": "機制",
 "ch": "N8",
 "section": "§3.7–3.8 operators, hashing, codec",
 "gpRef": "§3.7.2, §3.8.1, App. C",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "serialization",
  "notation"
 ],
 "stem": "What do H(x), H_K(x), E(x), E_4(x), a ⌢ b, a ⧺ b and s[i]^⟲ each do?",
 "stemZh": "H(x)、H_K(x)、E(x)、E_4(x)、a ⌢ b、a ⧺ b、s[i]^⟲ 各是什麼意思？",
 "options": [
  "H is Blake2b-256 and H_K is Keccak-256; E(x) serializes x with the GP codec and E_4(x) is the 4-octet fixed-width form; ⌢ concatenates blobs, ⧺ concatenates sequences; s[i]^⟲ indexes s cyclically (i mod |s|)",
  "H is Keccak-256 and H_K is Blake2b-256; E(x) encrypts x and E_4(x) uses a 4-round variant; ⌢ appends one element, ⧺ merges two sets; s[i]^⟲ reverses s before indexing",
  "H and H_K are the same Blake2b with and without a key; E(x) is the Merkle root of x and E_4(x) the root at depth 4; ⌢ is XOR, ⧺ is addition; s[i]^⟲ takes the i-th element from the end",
  "H is a 64-octet hash and H_K its 32-octet truncation; E(x) is the hex string of x and E_4(x) its first 4 characters; ⌢ and ⧺ are both string concatenation; s[i]^⟲ rotates the whole sequence by i"
 ],
 "optionsZh": [
  "H 是 Blake2b-256、H_K 是 Keccak-256；E(x) 用 GP 的 codec 序列化 x，E_4(x) 是定寬 4 octet 的版本；⌢ 接 blob、⧺ 接序列；s[i]^⟲ 是循環索引（i mod |s|）",
  "H 是 Keccak-256、H_K 是 Blake2b-256；E(x) 是加密 x，E_4(x) 是 4 輪的變體；⌢ 是接一個元素、⧺ 是合併兩個集合；s[i]^⟲ 是先反轉 s 再索引",
  "H 和 H_K 是同一個 Blake2b、差在有沒有 key；E(x) 是 x 的 Merkle root、E_4(x) 是深度 4 的 root；⌢ 是 XOR、⧺ 是加法；s[i]^⟲ 是從尾端數第 i 個",
  "H 是 64 octet 的雜湊、H_K 是截成 32 octet；E(x) 是 x 的十六進位字串、E_4(x) 是前 4 個字元；⌢ 和 ⧺ 都是字串接合；s[i]^⟲ 是把整個序列旋轉 i 格"
 ],
 "answer": 0,
 "optNotes": [
  "對：§3.8.1 定 H = Blake2b、H_K = Keccak；App. C 定 E 與 E_n；§3.7.2 定 ⌢、⧺、⟲。",
  "H 與 H_K 對調了；E 是序列化不是加密。",
  "E 不是 Merkle（Merkle 是 M）；⌢ ⧺ 是接合不是運算。",
  "兩個 hash 都是 32 octet；E 是二進位編碼不是 hex。"
 ],
 "explanation": "這七個記號幾乎每條公式都會碰到。**H(x)** 是 Blake2b-256，GP 預設的雜湊，輸出 32 octet；**H_K(x)** 是 Keccak-256，只用在跟外部系統相容的地方（accumulation 輸出的 MMR、給 BEEFY 簽的東西），因為 Ethereum 生態驗 Keccak 便宜。**E(x)** 是 App. C 的序列化：自然數用變長編碼、序列前綴長度、optional 前綴 0/1；**E_n(x)** 是把自然數固定編成 n 個 octet 的小端序版本（例：H_T 用 E_4，validator index 用 E_2）。**⌢** 接兩段 blob（octet 串），**⧺** 接兩個序列——語意相同，只是型別不同。**s[i]^⟲** 是「i 對序列長度取餘」的索引，例如 φ[c][H_T]^⟲ 就是 queue 的第 H_T mod 80 格。另外常見的 **→^n** 取前 n 個、**←^n** 取後 n 個（例：β 用 ←^H 只留最近 8 筆）。",
 "trap": "H = Blake2b、H_K = Keccak；E 是序列化；⟲ 是取餘索引。"
},
{
 "id": "n8-misleading-words",
 "lens": "機制",
 "ch": "N8",
 "section": "§4.1; §4.9; §10; §12",
 "gpRef": "§4.1 (extrinsic), §4.9 (refine/accumulate), §10 (wonky, culprit, fault), §12",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "extrinsic",
  "refine",
  "accumulate"
 ],
 "stem": "Five GP words whose everyday meaning misleads: extrinsic, refine, accumulate, wonky, culprit. What does each actually mean in JAM?",
 "stemZh": "五個字面意思會誤導的 GP 用詞：extrinsic、refine、accumulate、wonky、culprit。在 JAM 裡各自實際指什麼？",
 "options": [
  "Extrinsic: the block body — the five lists validators submit (tickets, preimages, guarantees, assurances, disputes); there are no user transactions. Refine: the in-core entry point that turns a big input into a small digest. Accumulate: the on-chain entry point that writes a digest's effect into state. Wonky: a verdict with exactly a third positive votes, undecidable. Culprit: a guarantor who signed a report later judged bad",
  "Extrinsic: data the chain stores outside itself in the D³L, referenced by hash only. Refine: the audit step that polishes a report before finality, re-running it until every judgment agrees. Accumulate: the ticket accumulator that collects lottery entries during the epoch. Wonky: a block whose seal failed verification and was dropped by the best-chain rule. Culprit: the auditor who cast the negative judgment that opened a dispute",
  "Extrinsic: a user transaction signed with Ed25519 and paid for from the sender's balance. Refine: the process of shrinking the validator set at an epoch change. Accumulate: appending a block's outputs to the recent-history belt. Wonky: a report that exceeded the 48 KB size limit and was truncated. Culprit: the block author who included an invalid extrinsic and forfeits the block reward",
  "Extrinsic: the header fields visible to light clients. Refine: erasure-coding a bundle into shards. Accumulate: collecting assurances until two thirds are reached. Wonky: a service whose balance is below threshold. Culprit: the builder of an unauthorized package"
 ],
 "optionsZh": [
  "Extrinsic：block body——validator 交上來的五張清單（ticket、preimage、guarantee、assurance、dispute），沒有使用者交易。Refine：in-core 的入口，把大輸入變成小 digest。Accumulate：on-chain 的入口，把 digest 的效果寫進 state。Wonky：正面票恰好三分之一、無法定論的 verdict。Culprit：簽了後來被判 bad 的 report 的 guarantor",
  "Extrinsic：鏈存在自己外面、只以 hash 引用的 D³L 資料。Refine：finality 前把 report 修飾一遍的 audit 步驟，反覆重跑直到所有判定一致。Accumulate：epoch 期間收集抽籤籤的 ticket accumulator。Wonky：seal 驗證失敗、被 best-chain 規則丟掉的 block。Culprit：投下負面票、開啟 dispute 的那位 auditor",
  "Extrinsic：用 Ed25519 簽、從發送者餘額扣費的使用者交易。Refine：epoch 換檔時縮減 validator 集合的過程。Accumulate：把 block 的輸出接上 recent-history 的 belt。Wonky：超過 48 KB 上限而被截斷的 report。Culprit：收了無效 extrinsic、因此失去出塊獎勵的出塊者",
  "Extrinsic：輕節點看得到的 header 欄位。Refine：把 bundle erasure code 成 shard。Accumulate：收集 assurance 直到超過三分之二。Wonky：餘額低於門檻的 service。Culprit：送出未授權 package 的 builder"
 ],
 "answer": 0,
 "optNotes": [
  "對：§4.1 extrinsic 是「external to the system」的輸入；§4.9 兩個入口；§10 的 wonky 與 culprit。",
  "全是望文生義：extrinsic 不是鏈外儲存，accumulate 不是 ticket 累加器。",
  "JAM 沒有使用者交易；refine 跟 validator 集合無關。",
  "extrinsic 是 body 不是 header；accumulate 跟 assurance 計票無關。"
 ],
 "explanation": "這五個字的字面意思都會把人帶偏。**extrinsic**（外來的）：Substrate 造的詞，用來取代 transaction，因為 block 裡的東西不只交易。JAM 沿用，實際指 block body 的五張清單，而且提交者都是 validator，沒有使用者交易——使用者的東西走 work-package，不進 block。**refine**（精煉）：不是「把東西修得更好」，是「把大輸入濃縮成小輸出」——MB 級的 package 進去、48 KB 以內的 report 出來，在 core 上跑、看不到 state。**accumulate**（累積）：不是「堆起來」，是「入帳」——唯一會改 service state 的入口，在鏈上跑。另外 GP 裡還有 ticket accumulator（γ_A）和 entropy accumulator（η_0），跟這個 accumulate 完全無關，只是都在「一直往裡加」。**wonky**（怪怪的）：verdict 的第三種結果，正面票恰好 ⌊|k|/3⌋，既不能判 good 也不能判 bad，report 被擱置。**culprit**（罪魁）：特指「擔保了壞 report 的 guarantor」；投錯票的人另有一個字叫 fault；兩者合稱 offender。口試時遇到這些詞，用你自己的話解釋內容，不要解釋字面。",
 "trap": "extrinsic = body、refine = 縮小、accumulate = 入帳、wonky = 三分之一、culprit = 壞 report 的 guarantor。"
},
{
 "id": "n8-work-nouns-chain",
 "lens": "機制",
 "ch": "N8",
 "section": "§4.9; §11; §14",
 "gpRef": "§4.9, eq. 11.2, eq. 11.6, eq. 14.2",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "work-package",
  "work-item"
 ],
 "stem": "Four nouns share the prefix 'work': work-package, work-item, work-report, work-digest. How do they relate, and which of them go on-chain?",
 "stemZh": "四個以 work 開頭的名詞：work-package、work-item、work-report、work-digest。它們之間是什麼關係？哪些會上鏈？",
 "options": [
  "A work-package contains 1–16 work-items and is what a core receives; refine turns each work-item into a work-digest; the work-report bundles those digests plus context and is the only one that goes on-chain, via a guarantee",
  "A work-item contains several work-packages; each package is refined into a work-report; the work-digest is the hash of a report and is the only thing stored on-chain, in ρ",
  "A work-report is what the builder submits; guarantors split it into work-items, refine each into a work-package, and the work-digest is the erasure-coded form that assurers store; all four go on-chain",
  "A work-package and a work-report are the same object before and after signing; a work-item is one guarantor's signature and a work-digest is the audit result; only the digest goes on-chain"
 ],
 "optionsZh": [
  "work-package 裝 1–16 個 work-item，是 core 收到的東西；refine 把每個 work-item 變成一個 work-digest；work-report 把這些 digest 加上 context 包起來，是四者中唯一上鏈的，透過 guarantee 進去",
  "work-item 裝好幾個 work-package；每個 package 被 refine 成一份 work-report；work-digest 是 report 的雜湊，是唯一存在鏈上（ρ 裡）的東西",
  "work-report 是 builder 提交的；guarantor 把它拆成 work-item，各自 refine 成 work-package，work-digest 是 assurer 存的 erasure 編碼形式；四者都上鏈",
  "work-package 和 work-report 是同一個物件簽名前後的名字；work-item 是一位 guarantor 的簽章、work-digest 是 audit 結果；只有 digest 上鏈"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 14.2 package 含 w ∈ ⟦work-item⟧_{1:I}；eq. 11.6 digest 是每個 item 的結果；eq. 11.2 report 含 d ∈ ⟦digest⟧；上鏈的是 report（E_G）。",
  "包含關係反了；ρ 存的是整份 guarantee（含 report），不是 hash。",
  "builder 提交的是 package；四者只有 report 上鏈。",
  "package 與 report 是不同物件（大 vs 小）；work-item 不是簽章。"
 ],
 "explanation": "把它們排成一條線：**work-package**（§14）是 builder 打包、送到 core 的輸入，可以很大（MB 級），裡面有 1 到 16 個 **work-item**，每個 item 指定 service、payload、gas 上限。guarantor 對每個 item 跑該 service 的 refine，輸出縮成一個 **work-digest**（eq. 11.6：result blob 或錯誤碼、gas 用量、匯出數等）。所有 digest 加上 refinement context、availability spec、authorizer 資訊，合成一份 **work-report**（eq. 11.2），上限 48 KB。只有 report 會上鏈——三位 guarantor 簽名後放進 E_G，進 ρ 等 assurance。package 本身不上鏈，被 erasure code 分給 validator 存著給 audit 用。所以方向是「大 → 小」：package（MB）→ report（KB）→ 每個 digest 只是幾個欄位。口試若問「report 跟 package 差在哪」：一個是輸入、一個是輸出摘要；一個留在 DA、一個上鏈。",
 "trap": "package 進 core、report 上鏈；item 是 package 的一格、digest 是 report 的一格。"
},
{
 "id": "n8-state-letters-work-pipeline",
 "lens": "機制",
 "ch": "N8",
 "section": "§4.2 state components",
 "gpRef": "eq. 4.4, §8, §11, §12",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "authorizer",
  "guarantee"
 ],
 "stem": "Match the Greek letters that a piece of work passes through: α, φ, ρ, ω, ξ, θ, δ. Which is which?",
 "stemZh": "一份工作會經過這些希臘字母：α、φ、ρ、ω、ξ、θ、δ。各是什麼？",
 "options": [
  "α authorizer pool per core, φ the queue that refills it, ρ the report each core currently holds awaiting assurance, ω reports waiting on dependencies, ξ package hashes already accumulated, θ this block's accumulation outputs, δ the service accounts",
  "α the active validators, φ the previous validators, ρ the recent blocks, ω the entropy, ξ the ticket accumulator, θ the timeslot, δ the disputes state",
  "α the service accounts, φ the privileged services, ρ the ready queue of reports waiting on dependencies, ω the authorizer pool per core, ξ this block's accumulation outputs, θ the report each core currently holds, δ the package hashes already accumulated",
  "α the header, φ the extrinsic, ρ the state root, ω the offenders, ξ the statistics, θ the epoch marker, δ the work-package"
 ],
 "optionsZh": [
  "α 每個 core 的 authorizer pool，φ 補充它的 queue，ρ 每個 core 目前持有、等 assurance 的 report，ω 等依賴的 report，ξ 已 accumulate 的 package hash，θ 本 block 的 accumulation 輸出，δ 所有 service account",
  "α 現任 validator，φ 上任 validator，ρ 最近的 block，ω entropy，ξ ticket 累加器，θ timeslot，δ disputes 狀態",
  "α service account，φ 特權 service，ρ 等依賴的 report 的 ready queue，ω 每個 core 的 authorizer pool，ξ 本 block 的 accumulation 輸出，θ 每個 core 目前持有的 report，δ 已 accumulate 的 package hash",
  "α header，φ extrinsic，ρ state root，ω offender，ξ 統計，θ epoch marker，δ work-package"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 4.4 的分量定義，§8（α φ）、§11（ρ）、§12（ω ξ θ）、§9（δ）。",
  "那些是 κ λ β η γ_A τ ψ 的意思，全錯位。",
  "七個全部互相對調，每個字母都指到了別的分量。",
  "header、extrinsic、state root 都不是 σ 的分量。"
 ],
 "explanation": "eq. 4.4 把 σ 拆成 17 個分量，其中七個是「工作管線」上的：**α**（§8）每個 core 目前接受的 authorizer 名單，**φ**（§8）補充 α 的 80 格 queue；**ρ**（§11）每個 core 目前掛著的那份 guarantee，等 assurance 讓它 available；**ω**（§12）ready queue，available 了但還在等 dependency 的 report；**ξ**（§12）最近一個 epoch 已經 accumulate 過的 package hash，防重複；**θ**（§12）這個 block 每個 service 的 accumulation 輸出承諾，之後進 β 的 MMR；**δ**（§9）所有 service account，accumulate 真正改的東西。順著走一遍：package 的 authorizer 要在 **α** → report 進 **ρ** → available 後若有依賴進 **ω** → accumulate 寫 **δ**、記 **ξ**、產 **θ**。剩下十個字母是共識與時間那一組（下一題）。",
 "trap": "α φ 是門票、ρ 是等候區、ω 是排隊區、ξ 是做過的、θ 是收據、δ 是帳本。"
},
{
 "id": "n8-state-letters-consensus",
 "lens": "機制",
 "ch": "N8",
 "section": "§4.2 state components",
 "gpRef": "eq. 4.4, §6, §7, §10, §13",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "validator set",
  "dispute"
 ],
 "stem": "Now the consensus-side letters: β, γ, η, ι, κ, λ, ψ, π, χ, τ. Which is which?",
 "stemZh": "換共識那一組字母：β、γ、η、ι、κ、λ、ψ、π、χ、τ。各是什麼？",
 "options": [
  "β recent blocks, γ Safrole state (tickets, sealer sequence), η entropy, ι next validators, κ current validators, λ previous validators, ψ disputes (good/bad/wonky/offenders), π statistics, χ privileged services, τ the last block's timeslot",
  "β the belt of BEEFY signatures, γ the gas budget, η the epoch index, ι the initial state, κ the Keccak root, λ the lookup-anchor, ψ the PVM state, π the pool, χ the checkpoint, τ the ticket, and none of them is ever rotated at an epoch change",
  "β validators, γ disputes, η recent blocks, ι timeslot, κ Safrole state, λ statistics, ψ entropy, π privileges, χ previous validators, τ next validators",
  "β authorizer queue, γ accounts, η ready queue, ι accumulated hashes, κ accumulation outputs, λ report per core, ψ authorizer pool, π work-package, χ header, τ extrinsic"
 ],
 "optionsZh": [
  "β 最近的 block，γ Safrole 狀態（ticket、sealer 序列），η entropy，ι 下期 validator，κ 現任 validator，λ 上任 validator，ψ disputes（good/bad/wonky/offenders），π 統計，χ 特權 service，τ 上個 block 的 timeslot",
  "β BEEFY 簽名的 belt，γ gas 預算，η epoch 編號，ι 初始 state，κ Keccak root，λ lookup-anchor，ψ PVM 狀態，π pool，χ checkpoint，τ ticket，而且沒有一個會在 epoch 換檔時輪替",
  "β validator，γ disputes，η 最近的 block，ι timeslot，κ Safrole 狀態，λ 統計，ψ entropy，π 特權，χ 上任 validator，τ 下期 validator",
  "β authorizer queue，γ account，η ready queue，ι 已 accumulate 的 hash，κ accumulation 輸出，λ 每 core 的 report，ψ authorizer pool，π work-package，χ header，τ extrinsic"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 4.4 與各章開頭的定義。",
  "全是望文生義的錯（β 不是 BEEFY、κ 不是 Keccak、χ 不是 checkpoint）。",
  "十個全部錯位：validator 是 κ、disputes 是 ψ、entropy 是 η。",
  "那是上一題工作管線的字母，而且也錯位。"
 ],
 "explanation": "另外十個分量：**β**（§7）最近 8 個 block 的摘要加 accumulation 輸出的 MMR；**γ**（§6）Safrole 內部狀態：γ_P 下期 key、γ_Z ring root、γ_S 本期 sealer 序列、γ_A ticket 累加器；**η**（§6）四格 entropy；**ι / κ / λ**（§6）validator 三代：staging（下期）、active（本期）、previous（上期）；**ψ**（§10）disputes 的四個集合；**π**（§13）活動統計；**χ**（§9）五個特權位子：manager、assigners、delegator、registrar、always-accumulate；**τ**（§4）最近一個 block 的 timeslot。記法：ι κ λ 是希臘字母順序，正好對應「下、現、上」——注意 ι 排最前面卻是「下期」。口試最常考的一組是 ι → γ_P → κ → λ 這條輪替線：每個 epoch 邊界往後推一格。",
 "trap": "ι κ λ 是「下、現、上」；γ 是 Safrole 不是 gas；χ 是特權不是 checkpoint。"
},
{
 "id": "n8-extrinsic-five-nouns",
 "lens": "機制",
 "ch": "N8",
 "section": "§4.1 the extrinsic",
 "gpRef": "eq. 4.3, §6, §9, §10, §11",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "extrinsic"
 ],
 "stem": "The extrinsic has five parts: E_T, E_P, E_G, E_A, E_D. Name each and say who puts it there.",
 "stemZh": "extrinsic 有五個部分：E_T、E_P、E_G、E_A、E_D。各叫什麼、由誰放進去？",
 "options": [
  "E_T tickets from validators competing for next epoch's slots; E_P preimages anyone supplies for a service that asked; E_G guarantees signed by a core's guarantors; E_A assurances from validators holding their shard; E_D disputes: verdicts, culprits, faults assembled by the author",
  "E_T transactions from users; E_P proofs of work from miners; E_G gas receipts from services; E_A audit results from auditors; E_D deposits from coretime buyers",
  "E_T timeslots proposed by the author; E_P privileges set by the manager; E_G GRANDPA votes; E_A account updates from accumulate; E_D digests from refine",
  "E_T tickets that only the block author may submit, one per block; E_P preimages supplied by the guarantors of the report that needs them; E_G guarantees signed by the assurers holding shards; E_A assurances produced by the auditors after re-execution; E_D disputes filed by the delegator service on behalf of the validator set"
 ],
 "optionsZh": [
  "E_T 是 validator 為下個 epoch 的 slot 投的 ticket；E_P 是任何人替「要求過的 service」提供的 preimage；E_G 是某 core 的 guarantor 簽的 guarantee；E_A 是持有 shard 的 validator 給的 assurance；E_D 是 disputes：verdict、culprit、fault，由出塊者整理",
  "E_T 使用者的交易；E_P 礦工的工作量證明；E_G service 的 gas 收據；E_A auditor 的稽核結果；E_D coretime 買家的押金",
  "E_T 出塊者提議的 timeslot；E_P manager 設的特權；E_G GRANDPA 投票；E_A accumulate 產生的帳戶更新；E_D refine 產生的 digest",
  "E_T 只有出塊者能投、每 block 一張的 ticket；E_P 由需要它的 report 的 guarantor 提供的 preimage；E_G 由持有 shard 的 assurer 簽的 guarantee；E_A 由 auditor 重跑後產出的 assurance；E_D 由 delegator service 代表 validator 集合提出的 disputes"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 4.3 與 §6、§9、§10、§11 各自的 extrinsic 定義。",
  "JAM 沒有交易、沒有 PoW、gas 不上鏈、audit 結果不直接上鏈。",
  "accumulate 與 refine 的產物都不是 extrinsic。",
  "角色全錯：ticket 是所有 validator、guarantee 是 guarantor、assurance 是 assurer。"
 ],
 "explanation": "eq. 4.3：E ≡ (E_T, E_P, E_G, E_A, E_D)，這是 block body 的全部。**E_T** tickets（§6）：每位 validator 為「下個 epoch」的出塊權投的匿名籤，最多每 block 16 張。**E_P** preimages（§9、§12）：service 透過 solicit 說「我要這個 hash 的原像」，任何人都能把資料放進 E_P 供應上來，常見用途是部署 service 的 code。**E_G** guarantees（§11）：某 core 的 3 位 guarantor 對一份 work-report 的簽名，一個 block 每個 core 至多一份。**E_A** assurances（§11）：每位 validator 一份 bitfield，說「這些 core 的 shard 我拿到了」。**E_D** disputes（§10）：verdict（對某 report 的 2/3 判定）、culprit（擔保壞 report 的人）、fault（投錯票的人），由出塊者從鏈下蒐集來的判定組成。五個裡沒有「交易」——這是 JAM 跟 Ethereum 最明顯的名詞差異；使用者的東西走 work-package，不在 extrinsic 裡。",
 "trap": "T ticket、P preimage、G guarantee、A assurance、D dispute。沒有交易。"
},
{
 "id": "n8-in-core-on-chain-off-chain",
 "lens": "機制",
 "ch": "N8",
 "section": "§4.9; §15–19",
 "gpRef": "§4.9.1, §15–19",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "core",
  "accumulate"
 ],
 "stem": "GP uses three location words: in-core, on-chain, off-chain. Sort these into the right place: refine, accumulate, is-authorized, auditing, GRANDPA voting, assurance signing, the E_A check.",
 "stemZh": "GP 用三個位置詞：in-core、on-chain、off-chain。把這些歸位：refine、accumulate、is-authorized、audit、GRANDPA 投票、簽 assurance、檢查 E_A。",
 "options": [
  "In-core: is-authorized and refine (run by a core's three guarantors). On-chain: accumulate and the E_A check (part of the state transition every node runs). Off-chain: auditing, GRANDPA voting and signing an assurance (things a validator does that are not in Υ)",
  "In-core: refine and accumulate. On-chain: is-authorized and auditing. Off-chain: GRANDPA voting, assurance signing and the E_A check",
  "In-core: everything a guarantor does, including auditing its own report and signing the assurance for it, since it already holds the data. On-chain: accumulate only, because it is the one step that writes state. Off-chain: is-authorized, refine and GRANDPA voting, none of which any other node re-runs",
  "In-core: refine only. On-chain: accumulate, is-authorized, auditing and the E_A check. Off-chain: GRANDPA voting and assurance signing"
 ],
 "optionsZh": [
  "In-core：is-authorized 和 refine（core 的三位 guarantor 跑）。On-chain：accumulate 和檢查 E_A（每個 node 都跑的 state transition 的一部分）。Off-chain：audit、GRANDPA 投票、簽 assurance（validator 做、但不在 Υ 裡的事）",
  "In-core：refine 和 accumulate。On-chain：is-authorized 和 audit。Off-chain：GRANDPA 投票、簽 assurance、檢查 E_A",
  "In-core：guarantor 做的一切，包括 audit 自己的 report、為它簽 assurance，因為它手上就有資料。On-chain：只有 accumulate，因為只有它會寫 state。Off-chain：is-authorized、refine 和 GRANDPA 投票，其他 node 都不會重跑",
  "In-core：只有 refine。On-chain：accumulate、is-authorized、audit、檢查 E_A。Off-chain：GRANDPA 投票和簽 assurance"
 ],
 "answer": 0,
 "optNotes": [
  "對：§4.9.1 定義 in-core（少數人執行）與 on-chain（人人執行）；§15–19 是 off-chain 的誠實策略。",
  "accumulate 是 on-chain；is-authorized 是 in-core；audit 是 off-chain；檢查 E_A 是 on-chain。",
  "audit 不是 guarantor 的工作（是隨機抽的 auditor）；is-authorized 與 refine 是 in-core。",
  "is-authorized 在 in-core；audit 在 off-chain。"
 ],
 "explanation": "三個詞分的是「誰在跑、跑的東西算不算 state transition」。**in-core**：只有被指派到那個 core 的三位 guarantor 跑，內容是 is-authorized（Ψ_I）和 refine（Ψ_R），結果靠 ELVES 賽局保安全。**on-chain**：每個 node 匯入 block 時都要跑的東西，也就是 Υ 裡的每一步——accumulate（Ψ_A）當然是，「檢查 E_A 的簽章和 2/3 門檻」也是（§11 的規則），「檢查 E_G 的 credential」也是。**off-chain**：validator 依 §15–19 的誠實策略做、但不屬於 state transition 的事——挑 report 來 audit（§17）、對 best chain 投 GRANDPA（§19）、簽 BEEFY（§18）、拿到 shard 後「產生」一份 assurance（§16）。注意「簽 assurance」是 off-chain、「檢查 assurance」是 on-chain，同一個名詞兩個位置；audit 也是：做 audit 在 off-chain，結果若變成 verdict 進 E_D 才上鏈。",
 "trap": "產生東西多半 off-chain，檢查東西一定 on-chain，refine 在 in-core。"
},
{
 "id": "n8-header-letters",
 "lens": "機制",
 "ch": "N8",
 "section": "§5 the header",
 "gpRef": "eq. 5.1",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "header",
  "seal"
 ],
 "stem": "The header is H = (H_P, H_R, H_X, H_T, H_E, H_W, H_O, H_I, H_V, H_S). Which letter is which?",
 "stemZh": "header 是 H = (H_P, H_R, H_X, H_T, H_E, H_W, H_O, H_I, H_V, H_S)。每個字母是什麼？",
 "options": [
  "P parent hash, R prior state root, X extrinsic hash, T timeslot, E epoch marker, W winning-tickets marker, O offenders marker, I author index, V entropy VRF signature, S seal",
  "P proof of work, R receipts root, X transactions root, T total difficulty, E epoch number, W weight, O output root, I identity key, V version, S signature",
  "P posterior state root, R random seed, X extra data, T ticket, E extrinsic hash, W work-report hash, O ordering, I index of core, V validator count, S slot",
  "P parent hash, R posterior state root, X extrinsic list, T timeslot, E entropy, W winning validator key, O offenders count, I author public key, V VRF output, S seal"
 ],
 "optionsZh": [
  "P parent hash、R prior state root、X extrinsic hash、T timeslot、E epoch marker、W winning-tickets marker、O offenders marker、I author index、V entropy 的 VRF 簽章、S seal",
  "P 工作量證明、R receipts root、X transactions root、T 總難度、E epoch 編號、W 權重、O 輸出 root、I 身分 key、V 版本、S 簽章",
  "P posterior state root、R 隨機種子、X 額外資料、T ticket、E extrinsic hash、W work-report hash、O 排序、I core index、V validator 數、S slot",
  "P parent hash、R posterior state root、X extrinsic 清單、T timeslot、E entropy、W 贏的 validator key、O offender 數量、I 作者公鑰、V VRF 輸出、S seal"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 5.1 的十個欄位。",
  "那是 Ethereum header 的欄位名，JAM 一個都沒有。",
  "R 是 prior 不是 posterior；X 是 hash 不是額外資料；I 是 validator index。",
  "R 是 prior；X 是 hash 不是清單；E 是 marker 不是 entropy 本身；I 是 index 不是 key；O 是 key 序列不是數量。"
 ],
 "explanation": "十個欄位分三組。**定位**：H_P 父 block 的 hash、H_T 這個 block 的 timeslot。**承諾**：H_R 執行「前」的 state root（不是後，這是 JAM 的特色）、H_X 五個 extrinsic 分量的 hash 再 hash。**共識**：H_I 作者在 κ′ 裡的 index（不是 key）、H_V 作者的 VRF 簽章、輸出餵進 entropy η_0、H_S seal，證明「這個 slot 是我的」。**三個 marker**：H_E epoch marker，只在 epoch 第一個 block 有，帶下期的 entropy 與 validator key；H_W winning-tickets marker，只在 ticket 提交期結束那個 block 有，公布下期的 sealer 序列；H_O offenders marker，列出這個 block 新增的 offender key，通常是空的。E、W 是 optional（沒有就 ∅），O 是序列（沒有就空序列）。記法：P/T 是位置，R/X 是內容，I/V/S 是作者，E/W/O 是公告。",
 "trap": "R 是 prior。I 是 index 不是 key。E/W 可缺席、O 是可空的序列。"
},
{
 "id": "n8-flow-in-symbols",
 "lens": "時機",
 "ch": "N8",
 "section": "§4 dependency graph; §8–12",
 "gpRef": "§4.1, eq. 8.2, eq. 11.17, eq. 11.18, §12",
 "difficulty": 2,
 "kind": "concept",
 "tags": [
  "guarantee",
  "extrinsic"
 ],
 "stem": "Write one work-package's journey using only symbols and the extrinsic it rides in: which check reads α, which extrinsic puts it into ρ, what makes it leave ρ, and which symbols does accumulate write?",
 "stemZh": "只用符號和它搭的 extrinsic 描述一份 work-package 的旅程：哪個檢查讀 α、哪個 extrinsic 把它放進 ρ、什麼讓它離開 ρ、accumulate 寫哪些符號？",
 "options": [
  "Its authorizer must be in α[c]; the guarantee in E_G places it in ρ[c]; enough bits in E_A (> 2/3·|κ|) make it available and clear ρ‡[c], or it times out after U slots; accumulate then writes δ‡, ξ′, θ′ and possibly ω′, χ′, ι′, φ′",
  "Its authorizer must be in φ[c]; the assurance in E_A places it in ρ[c]; the guarantee in E_G, arriving a few blocks later, makes it available and clears ρ[c]; accumulate then writes β′ and π′ only, since the service state δ is changed by refine in-core",
  "Its authorizer must be in χ; the ticket in E_T places it in ρ[c]; a verdict in E_D makes it available; accumulate then writes κ′ and η′",
  "Its authorizer must be in α[c]; the preimage in E_P places it in ρ[c]; GRANDPA finality makes it leave ρ; accumulate then writes the header's H_R"
 ],
 "optionsZh": [
  "它的 authorizer 要在 α[c]；E_G 裡的 guarantee 把它放進 ρ[c]；E_A 裡足夠的 bit（> 2/3·|κ|）讓它 available、清掉 ρ‡[c]，或 U 個 slot 後逾時；accumulate 接著寫 δ‡、ξ′、θ′，可能還有 ω′、χ′、ι′、φ′",
  "它的 authorizer 要在 φ[c]；E_A 裡的 assurance 把它放進 ρ[c]；幾個 block 後 E_G 裡的 guarantee 讓它 available 並清掉 ρ[c]；accumulate 接著只寫 β′ 和 π′，因為 service state δ 是 refine 在 in-core 改的",
  "它的 authorizer 要在 χ；E_T 裡的 ticket 把它放進 ρ[c]；E_D 裡的 verdict 讓它 available；accumulate 接著寫 κ′ 和 η′",
  "它的 authorizer 要在 α[c]；E_P 裡的 preimage 把它放進 ρ[c]；GRANDPA 定案讓它離開 ρ；accumulate 接著寫 header 的 H_R"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 11.32 讀 α；E_G → ρ′；eq. 11.17–11.18 用 E_A 決定 available 與清空；§12 的輸出是 δ‡、ξ′、θ′、ω′ 及特權相關的 χ′、ι′、φ′。",
  "pool 是 α 不是 φ；guarantee 與 assurance 的角色對調了。",
  "χ、E_T、E_D 都跟 work-package 的旅程無關。",
  "E_P 是 preimage 不是 report；GRANDPA 不影響 ρ；H_R 是下個 block 的 header 帶的。"
 ],
 "explanation": "把前面幾題的名詞接起來，用 §4 依賴圖的順序：(1) guarantor 收到 package，先看 **α[c]**（eq. 11.32 在鏈上也會再查一次）有沒有它的 authorizer，然後跑 refine 產出 report。(2) 三人簽名成 guarantee，出塊者放進 **E_G**，state transition 把它寫進 **ρ′[c]** —— 這是它第一次出現在 state 裡。(3) 之後幾個 block，validator 拿到 shard 後在 **E_A** 設 bit；某個 block 的 E_A 累計超過 2/3·|κ| 時（eq. 11.17）它進入 R（available），同時 eq. 11.18 把 **ρ‡[c]** 清空；沒等到就在 U = 5 個 slot 後逾時，也清空。(4) 同一個 block 的 accumulate 吃 R*，寫 **δ‡**（service account）、**ξ′**（記下它的 package hash）、**θ′**（它的輸出承諾）；若它有依賴則先進 **ω′** 排隊；若它的 service 是特權 service，還可能寫 **χ′、ι′、φ′**。(5) 最後 E_P 併進 δ‡ 得 **δ′**，下個 block 的 **H_R** 承諾整個 σ′。一句話：α 放行 → E_G 進 ρ → E_A 出 ρ → Δ+ 寫 δ ξ θ。",
 "trap": "α 讀、E_G 進、E_A 出、accumulate 寫 δ ξ θ。E_P 與 E_D 不在主線上。"
},
{
 "id": "n8-roles-glossary",
 "lens": "機制",
 "ch": "N8",
 "section": "§4.9; §14–17",
 "gpRef": "§4.9.1, §14, §15, §16, §17, §19",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "guarantee",
  "assurance"
 ],
 "stem": "Five role words: builder, author, guarantor, assurer, auditor. Who is a validator, and what does each one produce?",
 "stemZh": "五個角色名詞：builder、author、guarantor、assurer、auditor。哪些是 validator？各自產出什麼？",
 "options": [
  "Builder: not a validator; assembles a work-package. Author: the validator whose ticket owns this slot; produces the block. Guarantor: one of a core's three validators; produces a signed work-report. Assurer: any validator; produces an assurance bit per core it holds a shard for. Auditor: a randomly drawn validator; produces a judgment",
  "Builder: a validator that assembles blocks out of guarantees. Author: the service whose code the work-package targets. Guarantor: the coretime buyer who vouches that the package was paid for. Assurer: the auditor who re-runs the package and confirms the result. Auditor: the manager service that countersigns every dispute before it enters E_D",
  "Builder, author, guarantor, assurer and auditor are five fixed validator ranks; a node is promoted from builder to auditor as it accumulates stake, and each rank produces one extrinsic type",
  "Builder: produces the work-report. Author: produces the guarantee. Guarantor: produces the assurance. Assurer: produces the audit. Auditor: produces the block; only the auditor is a validator"
 ],
 "optionsZh": [
  "Builder：不是 validator，組 work-package。Author：ticket 擁有這個 slot 的 validator，產出 block。Guarantor：core 的三位 validator 之一，產出簽了名的 work-report。Assurer：任何 validator，對持有 shard 的 core 產出一個 assurance bit。Auditor：隨機抽出的 validator，產出 judgment",
  "Builder：把 guarantee 組成 block 的 validator。Author：work-package 指向的那個 service。Guarantor：為 package 已付費背書的 coretime 買家。Assurer：重跑 package、確認結果的 auditor。Auditor：每份 dispute 進 E_D 前都要副署的 manager service",
  "Builder、author、guarantor、assurer、auditor 是五個固定的 validator 階級；node 隨質押累積從 builder 升到 auditor，每個階級產出一種 extrinsic",
  "Builder 產出 work-report。Author 產出 guarantee。Guarantor 產出 assurance。Assurer 產出 audit。Auditor 產出 block；只有 auditor 是 validator"
 ],
 "answer": 0,
 "optNotes": [
  "對：§14 builder 在鏈下、不需是 validator；其餘四個都是同一群 validator 在不同時刻的角色。",
  "builder 不是 validator、author 是 validator 不是 service、guarantor 不是買家。",
  "不是階級，是同一批人輪流做的事。",
  "產出全部錯位一格，而且五個角色裡有四個是 validator。"
 ],
 "explanation": "JAM 只有一種節點身分：validator（full 設定 1023 個）。其餘四個「角色」都是同一批 validator 在不同時刻的帽子：**author** 是這個 slot 的 ticket 持有者，出 block；**guarantor** 是被指派到某 core 的三人，跑 refine、簽 report；**assurer** 是每個拿到 shard 的人，簽 assurance；**auditor** 是被 VRF 抽到的人，重跑 report、給 judgment。同一個 validator 在同一個 slot 可以同時是 author、guarantor、assurer、auditor。**builder** 是唯一不需要是 validator 的：§14 說它在鏈下組 work-package、送給 guarantor，GP 不規範它是誰——可以是使用者、collator、任何服務。口試被問「誰做 X」時，先答「validator」，再說是哪頂帽子。",
 "trap": "四頂帽子一群人；builder 是外人。"
},
{
 "id": "n8-three-key-types",
 "lens": "機制",
 "ch": "N8",
 "section": "§6.2 validator keys; App. G",
 "gpRef": "eq. 6.7, §6, §10, §11, §18, App. G",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "Bandersnatch",
  "Ed25519"
 ],
 "stem": "Each validator key bundles three public keys: Bandersnatch, Ed25519, BLS. Which noun uses which key?",
 "stemZh": "每把 validator key 綁三把公鑰：Bandersnatch、Ed25519、BLS。哪個名詞用哪把？",
 "options": [
  "Bandersnatch: tickets (ring VRF), the seal, the entropy signature H_V, audit selection. Ed25519: guarantees, assurances, judgments, and the identity of offenders. BLS: BEEFY signatures only",
  "Bandersnatch: BEEFY and GRANDPA. Ed25519: tickets and the seal. BLS: guarantees, assurances and judgments",
  "Bandersnatch: everything that ends up on-chain, since every extrinsic must be VRF-signed. Ed25519: everything off-chain, such as networking and audit gossip. BLS: unused in 0.8.0, reserved for a future version's aggregated GRANDPA votes",
  "Bandersnatch: guarantees and assurances. Ed25519: the seal and tickets. BLS: judgments and offender identity"
 ],
 "optionsZh": [
  "Bandersnatch：ticket（ring VRF）、seal、entropy 簽章 H_V、audit 抽籤。Ed25519：guarantee、assurance、judgment、以及 offender 的身分。BLS：只有 BEEFY 簽章",
  "Bandersnatch：BEEFY 和 GRANDPA。Ed25519：ticket 和 seal。BLS：guarantee、assurance、judgment",
  "Bandersnatch：所有會上鏈的東西，因為每個 extrinsic 都要 VRF 簽章。Ed25519：所有鏈下的事，例如網路與 audit 的 gossip。BLS：0.8.0 沒用到，留給未來版本的聚合 GRANDPA 投票",
  "Bandersnatch：guarantee 和 assurance。Ed25519：seal 和 ticket。BLS：judgment 和 offender 身分"
 ],
 "answer": 0,
 "optNotes": [
  "對：§6 的 VRF 都是 Bandersnatch；§10–11 的簽章是 Ed25519；§18 BEEFY 用 BLS。",
  "BEEFY 是 BLS；ticket/seal 是 Bandersnatch；guarantee 等是 Ed25519。",
  "三把 key 的分工是依「需要 VRF 還是普通簽章還是可聚合」，不是鏈上鏈下。",
  "Bandersnatch 與 Ed25519 對調了；BLS 只用在 BEEFY。"
 ],
 "explanation": "三把 key 對應三種需求。**Bandersnatch**（App. G）是一條支援 VRF 的曲線：凡是需要「可驗證的隨機輸出」的地方都用它——ticket 的 ring-VRF 證明（匿名）、seal 與 H_V（普通 VRF，輸出餵 entropy）、audit 抽籤。**Ed25519** 是普通簽章，快、小、人人會驗：guarantee 的 credential、assurance、dispute 的 judgment、culprit、fault 都用它，所以 offender 的「身分」就是 Ed25519 key（ψ_O、H_O 存的都是它）。**BLS** 可以把上千個簽章聚合成一個：只用在 BEEFY（§18），讓橋接系統驗一個簽章就等於驗了 2/3 的 validator。epoch marker H_E 帶的是 Bandersnatch 加 Ed25519 兩把，讓只讀 header 的節點能驗 seal 也能對 offender。",
 "trap": "要隨機用 Bandersnatch，要簽名用 Ed25519，要聚合用 BLS。"
},
{
 "id": "n8-safrole-nouns",
 "lens": "機制",
 "ch": "N8",
 "section": "§6",
 "gpRef": "§6, eq. 6.25, eq. 6.27, eq. 6.28–6.29",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "ticket",
  "Safrole",
  "seal"
 ],
 "stem": "Safrole nouns: ticket, ticket accumulator, sealer sequence, seal, epoch marker, winning-tickets marker, fallback. Put each in one sentence.",
 "stemZh": "Safrole 的名詞：ticket、ticket accumulator、sealer sequence、seal、epoch marker、winning-tickets marker、fallback。各一句話。",
 "options": [
  "Ticket: an anonymous lottery entry for next epoch. Accumulator (γ_A): the best E tickets collected so far. Sealer sequence (γ_S): this epoch's slot-by-slot schedule. Seal: the author's proof it owns this slot. Epoch marker: next epoch's entropy and keys, in the first block. Winning-tickets marker: next epoch's schedule, announced when submission closes. Fallback: a public key sequence used when tickets ran short",
  "Ticket: a signed transaction that pays for the slot. Accumulator: the gas meter for the epoch. Sealer sequence: the list of blocks GRANDPA has finalized. Seal: the block hash signed by the author. Epoch marker: a checkpoint header light clients sync from. Winning-tickets marker: the list of validators slashed this epoch. Fallback: the previous epoch's schedule reused unchanged when the new one is late",
  "Ticket: a coretime purchase receipt. Accumulator: the ready queue. Sealer sequence: the guarantor rotation. Seal: the BEEFY signature. Epoch marker: the offenders list. Winning-tickets marker: the audit assignments. Fallback: GRANDPA's secondary vote",
  "Ticket: the author's public key. Accumulator: the entropy η. Sealer sequence: the validator set κ. Seal: the assurance signature. Epoch marker: the state root. Winning-tickets marker: the extrinsic hash. Fallback: the previous validator set λ"
 ],
 "optionsZh": [
  "Ticket：為下個 epoch 投的匿名籤。Accumulator（γ_A）：目前收到、最好的 E 張 ticket。Sealer sequence（γ_S）：這個 epoch 逐 slot 的排程。Seal：作者證明「這個 slot 是我的」。Epoch marker：epoch 第一個 block 帶的下期 entropy 與 key。Winning-tickets marker：提交期結束時公告的下期排程。Fallback：ticket 不夠時改用的公開 key 序列",
  "Ticket：為 slot 付費的簽名交易。Accumulator：該 epoch 的 gas 計量器。Sealer sequence：GRANDPA 已定案的 block 清單。Seal：作者簽的 block hash。Epoch marker：輕節點用來同步的 checkpoint header。Winning-tickets marker：本 epoch 被罰沒的 validator 清單。Fallback：新排程來不及時，原封不動沿用上個 epoch 的排程",
  "Ticket：coretime 購買收據。Accumulator：ready queue。Sealer sequence：guarantor 輪替表。Seal：BEEFY 簽章。Epoch marker：offender 清單。Winning-tickets marker：audit 指派表。Fallback：GRANDPA 的次要投票",
  "Ticket：作者的公鑰。Accumulator：entropy η。Sealer sequence：validator 集合 κ。Seal：assurance 簽章。Epoch marker：state root。Winning-tickets marker：extrinsic hash。Fallback：上任 validator 集合 λ"
 ],
 "answer": 0,
 "optNotes": [
  "對：§6 各名詞的定義；γ_A、γ_S 在 eq. 6.5；marker 在 eq. 6.28–6.29；fallback 在 eq. 6.25、6.27。",
  "全是別的系統的名詞：JAM 沒有交易、gas 不按 epoch 計、seal 不是 hash。",
  "全部錯位：ticket 不是收據、accumulator 不是 ω、seal 不是 BEEFY。",
  "把 Safrole 名詞對到了 state 的其他分量。"
 ],
 "explanation": "順著一個 epoch 走：epoch e 期間，validator 用 ring-VRF 投 **ticket**（E_T），分數是 VRF 輸出；鏈上把目前最好的 E 張留在 **ticket accumulator** γ_A。提交期在 slot Y = 500 關閉，關閉後第一個 block 的 header 帶 **winning-tickets marker** H_W，公告 γ_A 排成的下期排程。epoch e+1 第一個 block 做輪替，γ_A 變成 **sealer sequence** γ_S（每個 slot 一張 ticket），同時 header 帶 **epoch marker** H_E（下期的 entropy 與 validator key）。之後每個 block 的作者用 ticket 對應的 key 產生 **seal** H_S，證明這個 slot 是自己的。如果 epoch e 結束時 γ_A 沒湊滿 E 張，e+1 整個 epoch 進 **fallback**：γ_S 改成由 entropy 直接算出的公開 key 序列，還是一人一 slot，但誰出塊大家都看得到。",
 "trap": "ticket 投 → accumulator 收 → marker 公告 → sealer sequence 定案 → seal 證明；不夠就 fallback。"
},
{
 "id": "n8-da-nouns",
 "lens": "機制",
 "ch": "N8",
 "section": "§11; §14; §16; App. H",
 "gpRef": "eq. 11.5, §14, §16, App. H",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "segment",
  "erasure coding"
 ],
 "stem": "Data-availability nouns: bundle, shard, erasure-root, segment, segments-root, audit DA, D³L. What is each?",
 "stemZh": "資料可得性的名詞：bundle、shard、erasure-root、segment、segments-root、audit DA、D³L。各是什麼？",
 "options": [
  "Bundle: the package plus its extrinsic data and imported segments, what an auditor needs to re-run. Shard: one validator's erasure-coded piece. Erasure-root: the Merkle root over all shards, in the report. Segment: a 4104-octet block of data one package exports for later ones. Segments-root: the root over a package's exported segments. Audit DA: short-lived storage of bundle shards. D³L: 28-day storage of segment shards",
  "Bundle: a group of consecutive blocks finalized together by one GRANDPA round. Shard: one parachain's slice of the global state. Erasure-root: the state root after expired preimages are pruned. Segment: one slice of an epoch, 60 slots long. Segments-root: the MMR built over those slices. Audit DA: the part of the disputes state that auditors read. D³L: a Merkle trie with exactly three levels, used for the service index",
  "Bundle: the block body. Shard: one core's share of validators. Erasure-root: the hash of deleted preimages. Segment: a basic block of PVM code. Segments-root: the jump table. Audit DA: the auditors' assignment. D³L: the delegator's key list",
  "Bundle: the accumulate input. Shard: a work-item. Erasure-root: the header hash. Segment: a work-digest. Segments-root: the extrinsic hash. Audit DA: the ready queue. D³L: the preimage store"
 ],
 "optionsZh": [
  "Bundle：package 加它的 extrinsic 資料與 import 的 segment，auditor 重跑需要的全部。Shard：一位 validator 拿到的那片 erasure 編碼。Erasure-root：所有 shard 的 Merkle root，寫在 report 裡。Segment：4104 octet 一塊、一份 package 匯出給後面 package 用的資料。Segments-root：一份 package 匯出 segment 的 root。Audit DA：bundle 分片的短期儲存。D³L：segment 分片的 28 天儲存",
  "Bundle：由一輪 GRANDPA 一起定案的連續 block。Shard：一條 parachain 在全域 state 裡的切片。Erasure-root：清掉過期 preimage 之後的 state root。Segment：epoch 的一段，60 個 slot。Segments-root：對那些段建的 MMR。Audit DA：disputes 狀態裡 auditor 讀的那部分。D³L：恰好三層、給 service index 用的 Merkle trie",
  "Bundle：block body。Shard：一個 core 分到的 validator。Erasure-root：被刪 preimage 的 hash。Segment：PVM 的 basic block。Segments-root：jump table。Audit DA：auditor 指派表。D³L：delegator 的 key 清單",
  "Bundle：accumulate 的輸入。Shard：work-item。Erasure-root：header hash。Segment：work-digest。Segments-root：extrinsic hash。Audit DA：ready queue。D³L：preimage 儲存"
 ],
 "answer": 0,
 "optNotes": [
  "對：§14 bundle 與 segment、eq. 11.5 的 erasure-root 與 segments-root、§16 兩種 DA、App. H erasure coding。",
  "全是別的概念：bundle 是 package 的資料包，跟 GRANDPA 無關。",
  "全部錯位：shard 是 validator 拿的分片，segment 是 4104 octet 的資料塊。",
  "全部錯位：bundle 給 audit 用，audit DA 是儲存不是 queue。"
 ],
 "explanation": "兩條線。**Audit 線**：guarantor 把 **bundle**（package + extrinsic 資料 + import 進來的 segment + 證明）erasure code 成 |κ| 個 **shard**，每位 validator 一片，所有 shard 的 Merkle root 就是 report 裡的 **erasure-root**；validator 拿到自己那片才簽 assurance。這些 shard 存在 **audit DA**，只要活到 report 被 audit 完、block 定案就好。**資料線**：refine 可以 export **segment**（固定 4104 octet），這些 segment 也被 erasure code、分片，root 叫 **segments-root**，同樣寫在 report 的 availability spec；後面的 package 可以 import 它們。segment 的 shard 存在 **D³L**（Distributed Data Lake），要留 28 天，因為誰都可能之後 import。所以一份 report 有兩個 root：erasure-root 對 bundle（給 audit），segments-root 對 export（給後人用）。",
 "trap": "bundle 給 audit、segment 給後人；erasure-root 對前者、segments-root 對後者。"
},
{
 "id": "n8-pvm-nouns",
 "lens": "機制",
 "ch": "N8",
 "section": "App. A; App. B",
 "gpRef": "§4.7, App. A, App. B",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "PVM",
  "gas"
 ],
 "stem": "PVM nouns: invocation, host call, gas, basic block, page fault, inner PVM. One line each.",
 "stemZh": "PVM 的名詞：invocation、host call、gas、basic block、page fault、inner PVM。各一句。",
 "options": [
  "Invocation: one of the three ways the protocol runs the PVM (Ψ_I, Ψ_R, Ψ_A), each with its own host-call table. Host call: the only door out of the machine, triggered by ecalli. Gas: the compute budget, charged per basic block on entry. Basic block: a straight run of instructions ending in a jump or trap. Page fault: touching an unmapped page; the host may map it and resume. Inner PVM: a PVM started from inside refine to run, say, a parachain runtime",
  "Invocation: a transaction call that a user signs and submits, one per work-item. Host call: a synchronous call from one service into another service's accumulate, returning its result immediately. Gas: the fee, paid in tokens from the caller's balance at the end of the block. Basic block: a 4 KB memory page, the unit at which the PVM maps and prices memory. Page fault: a panic that ends the invocation and rolls back to the checkpoint. Inner PVM: the accumulate half of a service, which runs nested inside its refine half",
  "Invocation: the seal. Host call: a GRANDPA vote. Gas: the slot length. Basic block: a genesis block. Page fault: a missing preimage. Inner PVM: the auditor's replay",
  "Invocation: an epoch. Host call: an extrinsic. Gas: the erasure-coding rate. Basic block: a work-item. Page fault: a dependency that never arrives. Inner PVM: the recompiler"
 ],
 "optionsZh": [
  "Invocation：協定跑 PVM 的三種方式之一（Ψ_I、Ψ_R、Ψ_A），各有自己的 host call 表。Host call：機器唯一對外的門，由 ecalli 觸發。Gas：計算預算，進入 basic block 時整塊預扣。Basic block：一段直線指令，以跳躍或 trap 結尾。Page fault：碰到未映射的 page，host 可以映射後繼續。Inner PVM：在 refine 裡再開一台 PVM，例如跑 parachain 的 runtime",
  "Invocation：使用者簽名提交的交易呼叫，每個 work-item 一次。Host call：一個 service 對另一個 service 的 accumulate 的同步呼叫，立刻回傳結果。Gas：手續費，block 結束時從呼叫者的餘額以代幣扣除。Basic block：4 KB 的記憶體 page，PVM 映射與計價記憶體的單位。Page fault：結束 invocation 並退回 checkpoint 的 panic。Inner PVM：service 的 accumulate 那一半，巢狀跑在它的 refine 那一半裡面",
  "Invocation：seal。Host call：GRANDPA 投票。Gas：slot 長度。Basic block：創世 block。Page fault：找不到的 preimage。Inner PVM：auditor 的重跑",
  "Invocation：epoch。Host call：extrinsic。Gas：erasure 編碼率。Basic block：work-item。Page fault：永遠不來的依賴。Inner PVM：recompiler"
 ],
 "answer": 0,
 "optNotes": [
  "對：App. B 三種 invocation、App. A 的 host call / gas / basic block / page fault、§B.2 的 inner PVM。",
  "全是別的概念：host call 不是跨 service 同步呼叫，gas 不是代幣費。",
  "全部錯位：invocation 不是 seal，gas 不是 slot 長度。",
  "全部錯位：basic block 是指令段不是 work-item。"
 ],
 "explanation": "**Invocation**（App. B）是「協定在什麼場合、給什麼 host call 表跑 PVM」：Ψ_I 授權、Ψ_R refine、Ψ_A accumulate，機器同一台，門不同。**Host call** 是程式執行 ecalli n 時暫停、把控制權交給 host 跑 Ω_n（讀 storage、轉帳、fetch…）再回來；PVM 沒有 I/O，這是唯一的門。**Gas** 是計算上限，0.8.0 起以 **basic block** 為單位在進入時預扣——basic block 是從入口到下一個跳躍／trap 的直線指令段，成本靜態可算。**Page fault** 是存取未映射的 4 KB page，機器停下並回報位址，host 可以把 page 映射上再繼續（不一定是錯誤）。**Inner PVM** 是 refine 專用：用 machine / peek / poke / invoke 這組 host call 在 PVM 裡再開一台 PVM，parachain 的 runtime 就是這樣在 JAM 上跑的。",
 "trap": "三種 invocation 一台機器；host call 是門；gas 按 block 預扣；page fault 可恢復。"
},
{
 "id": "n8-dispute-nouns-and-constants",
 "lens": "機制",
 "ch": "N8",
 "section": "§10; App. I",
 "gpRef": "§10, App. I",
 "difficulty": 1,
 "kind": "concept",
 "tags": [
  "dispute"
 ],
 "stem": "Two last groups. Disputes: judgment, verdict, good/bad/wonky, culprit, fault, offender. Constants: C, E, P, R, U, L, D, H, Y. What are they?",
 "stemZh": "最後兩組。Disputes：judgment、verdict、good/bad/wonky、culprit、fault、offender。常數：C、E、P、R、U、L、D、H、Y。各是什麼？",
 "options": [
  "Judgment: one auditor's signed vote on a report. Verdict: ⌊2|k|/3⌋+1 judgments collected; good (all positive), bad (none), wonky (exactly a third). Culprit: a guarantor of a bad report. Fault: a judge who voted against the verdict. Offender: either, recorded in ψ_O. Constants: C cores 341, E slots per epoch 600, P seconds per slot 6, R rotation period 10, U availability timeout 5, L lookup-anchor age 14,400, D preimage expunge 19,200, H recent blocks 8, Y ticket close 500",
  "Judgment: the block author's decision to include or drop a report. Verdict: GRANDPA's finality vote on the block. Good/bad/wonky: the three PVM exit codes for halt, panic and out-of-gas. Culprit: a validator that missed its slot. Fault: a page fault inside refine. Offender: a service whose balance fell below threshold. Constants: C the number of chains, E the total epochs since genesis, P the coretime price, R the per-block reward, U the user count, L the loop limit, D the trie depth, H the block height, Y the year of the Common Era",
  "Judgment: a service's yield. Verdict: an accumulate result. Good/bad/wonky: report size classes. Culprit: the builder. Fault: a failed refine. Offender: the delegator. Constants: C cost, E entropy, P pool, R report, U update, L lookup, D dispute, H hash, Y yield",
  "Judgment: an assurance. Verdict: a guarantee. Good/bad/wonky: availability states. Culprit: an assurer. Fault: an auditor. Offender: the author. Constants all equal 1023"
 ],
 "optionsZh": [
  "Judgment：一位 auditor 對某 report 簽名的一票。Verdict：收齊 ⌊2|k|/3⌋+1 票；good（全正面）、bad（全負面）、wonky（恰好三分之一）。Culprit：擔保了 bad report 的 guarantor。Fault：投票與 verdict 相反的人。Offender：兩者皆是，記在 ψ_O。常數：C core 數 341、E 每 epoch slot 數 600、P 每 slot 秒數 6、R 輪替週期 10、U availability 逾時 5、L lookup-anchor 最大年齡 14,400、D preimage 清除期 19,200、H recent block 數 8、Y ticket 截止 500",
  "Judgment：出塊者收或不收某份 report 的決定。Verdict：GRANDPA 對 block 的定案票。Good/bad/wonky：PVM 的三種退出碼 halt、panic、out-of-gas。Culprit：錯過自己 slot 的 validator。Fault：refine 裡的 page fault。Offender：餘額掉到門檻以下的 service。常數：C 鏈的數量、E 創世以來的總 epoch 數、P coretime 價格、R 每 block 獎勵、U 使用者數、L 迴圈上限、D trie 深度、H block 高度、Y Common Era 的年份",
  "Judgment：service 的 yield。Verdict：accumulate 結果。Good/bad/wonky：report 大小分級。Culprit：builder。Fault：失敗的 refine。Offender：delegator。常數：C 成本、E entropy、P pool、R report、U 更新、L lookup、D dispute、H hash、Y yield",
  "Judgment：一份 assurance。Verdict：一份 guarantee。Good/bad/wonky：availability 的狀態。Culprit：assurer。Fault：auditor。Offender：作者。常數全部等於 1023"
 ],
 "answer": 0,
 "optNotes": [
  "對：§10 的名詞定義與 App. I 的常數表。",
  "全是望文生義：judgment 是 auditor 的票，常數是協定參數不是價格獎勵。",
  "全部錯位：verdict 不是 accumulate 結果，culprit 不是 builder。",
  "全部錯位：judgment 不是 assurance，常數各不相同。"
 ],
 "explanation": "**Disputes 名詞**（§10）：auditor 重跑 report 後簽一票 **judgment**（有效／無效）；出塊者收齊 ⌊2|k|/3⌋+1 票組成 **verdict**，正面票數決定 report 是 **good**（全部正面）、**bad**（全部負面）或 **wonky**（恰好 ⌊|k|/3⌋ 正面，資料有問題但無法定論）；bad report 的 guarantor 是 **culprit**，投票方向與最終 verdict 相反的 auditor 是 **fault**，兩者的 Ed25519 key 進 ψ_O 成為 **offender**。**常數**（App. I）：C = 341 core、E = 600 slot/epoch、P = 6 秒/slot（所以 epoch 一小時）、R = 10 slot 換一次 guarantor、U = 5 slot 沒 available 就逾時、L = 14,400 slot（24 小時）是 refine 能看的最舊 state、D = 19,200 slot 後 preimage 才真正清掉、H = 8 個 recent block、Y = 500 之後不收 ticket。這九個字母在公式裡到處出現，看到大寫單字母先想是不是常數。",
 "trap": "judgment 一票、verdict 一票的集合、offender 兩種人；常數 C E P R U L D H Y 各一個數字。"
}
]
