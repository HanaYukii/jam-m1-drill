# -*- coding: utf-8 -*-
# Appendix C — Serialization Codec; D — State Merklization; E — General Merklization; H — Erasure Coding (GP 0.8.0)
ITEMS = [
{
 "id": "appC-discriminators",
 "ch": "C", "section": "C.1 Discriminator / Sequence / Dictionary encoding", "gpRef": "§C.1.3–C.1.5",
 "difficulty": 2, "kind": "concept", "tags": ["codec"],
 "stem": "Appendix C fixes how a value whose length its type does not imply gets encoded, how an absent value is distinguished from a present one, how a dictionary is laid out, and in which direction a bit sequence is packed. Which account of those four conventions is right?",
 "options": [
  "Fixed-length items (hashes, fixed sequences) encode as-is; variable-length items ↕x are prefixed by E(|x|); an optional value x? encodes as [0] if ∅ else [1] ⌢ E(x); dictionaries encode as their (key, value) pairs ordered by key; and bit sequences pack bits into octets least-significant-first",
  "Fixed-length items (hashes, fixed sequences) are prefixed by E(|x|) too, so a decoder never needs type information; variable-length items ↕x are prefixed the same way; an optional value x? encodes as [0] if ∅ else [1] ⌢ E(x); dictionaries encode as their (key, value) pairs ordered by key; and bit sequences pack bits into octets least-significant-first",
  "Fixed-length items (hashes, fixed sequences) encode as-is; variable-length items ↕x are prefixed by E(|x|); an optional value x? encodes as [0xFF] if ∅ else the value alone; dictionaries encode as their (key, value) pairs in insertion order; and bit sequences pack bits into octets least-significant-first",
  "Fixed-length items (hashes, fixed sequences) encode as-is; variable-length items ↕x are prefixed by E_4(|x|) so every length prefix is the same width; an optional value x? encodes as [0] if ∅ else [1] ⌢ E(x); dictionaries encode as their (key, value) pairs ordered by key; and bit sequences pack bits into octets most-significant-first"
 ],
 "answer": 0,
 "optNotes": [
   "四點都對上 §C.1：固定長度免前綴、x? = 0 或 (1, x)、dictionary 依 key 排序、bit 打包 LSB-first。",
   "§C.1.3 的但書：長度 discriminator「is omitted in the case of fixed-length terms such as hashes」。",
   "x? 的定義是 0 或 (1, x)；dictionary 明訂依 key 排序，否則同一 state 會有多種合法編碼。",
   "長度 discriminator 用的是可變長的 compact E，且 §C.1.4 明寫 bit 打包由最低位到最高位。",
 ],
 "explanation": "附錄 C 的幾條通則：**E(∅) = []**（空的什麼都不寫）；blob 編碼為自身；tuple 是各元素直接串接（沒有分隔符）；**↕x ≡ (|x|, x)**——變長的東西前面掛長度前綴；**x? = 0 當 x = ∅，否則 (1, x)**——optional 用一個判別位元組；dictionary **依 key 排序後**編碼成 (key, value) 對；§C.1.4 的 bit sequence 每 8 位打包成一個位元組，而且是「**in order of least significant to most**」（assurance 的 bitfield 就是這樣）。**最後這一條特別容易踩**：它與 §3.7.3 的 bits()（**MSB first**，用於 state trie 的 key path）方向相反。同一份實作裡兩種方向並存，混用只會在特定資料上出錯，很難查。**一個常見的錯誤通則**：以為「變長欄位一律排到最後」。附錄 C **沒有**這條規則——它是對每個結構逐一給出編碼的。反例就在眼前：E_U(H) 把變長的 epoch marker 與 winning-tickets marker 排在**固定長度**的 H_I、H_V 之前。**為什麼可以這樣**：因為每個變長欄位自己帶長度前綴，解碼器讀完就知道下一個欄位從哪開始，不需要靠位置推算。順帶記：0.7.1 為 account serialization 加了 version byte（C(255, s) 開頭的 0）。",
 "trap": "bits(x) 函數（§3）是 MSB-first 用於 trie key；codec 的 bit sequence 是 LSB-first——兩者方向不同。"
},
{
 "id": "appC-fixed-vs-compact",
 "ch": "C", "section": "C.2–C.3 Block/state serialization", "gpRef": "§C.2 & appendix D note",
 "difficulty": 2, "kind": "concept", "tags": ["codec"],
 "stem": "Where does the GP use fixed-width integer encodings E_l versus the general compact encoding E?",
 "options": [
  "State serialization (appendix D) uses fixed-length for all non-discriminator numerics (e.g. E_4(τ), E_8(balance)); block/extrinsic encodings use E_4 for timeslots and E_2 for validator indices, while lengths/discriminators always use the compact E; the GP defines each structure's encoding explicitly in appendix C",
  "State serialization (appendix D) uses fixed-length for all non-discriminator numerics (e.g. E_4(τ), E_8(balance)); block/extrinsic encodings use E_8 for timeslots and E_4 for validator indices, while lengths/discriminators always use the compact E; appendix C leaves each structure's field layout to the implementation",
  "State serialization (appendix D) uses the compact E for every numeric, τ and account balances included; block/extrinsic encodings use E_4 for timeslots and E_2 for validator indices, while lengths/discriminators are always fixed 4-octet values; the GP defines each structure's encoding explicitly in appendix C",
  "State serialization (appendix D) uses fixed-length for all non-discriminator numerics, but big-endian rather than little-endian; block/extrinsic encodings use E_4 for timeslots and E_2 for validator indices, while lengths/discriminators always use the compact E; a service index is E_2 throughout, matching the validator index width"
 ],
 "answer": 0,
 "optNotes": [
   "state 數值一律 fixed-length、H_T 為 E_4、validator index 一律 E_2、長度前綴才走 compact E。",
   "H_T 是 E_4、validator index 是 E_2；附錄 C 也逐一給出各結構的明確編碼而非交給實作自訂。",
   "把附錄 D 的註與 §C.1.3 兩邊倒過來：state 非 discriminator 數值才 fixed，discriminator 走 compact。",
   "§C.1.6 明寫「Values are encoded in a regular little-endian fashion」，且 service index 全程是 E_4。",
 ],
 "explanation": "附錄 D 的註：「all non-discriminator numeric serialization in state is done in fixed-length according to the size of the term」（例如 C(11) ↦ E_4(τ)，account info 用 E_8/E_4）；§C.1.3 則說 discriminator「are encoded as a natural」，也就是變長的 compact E。附錄 C 對 header、extrinsic、work report 等逐一定義：H_T 用 E_4，**所有 validator index 都是 E_2**（assurer、judge、author、guarantor），service index E_4、gas E_8、長度前綴用 compact E；§C.1.6：「Values are encoded in a regular little-endian fashion」。你們 code-map 3.13.2 指出：work report 內的 core index 與 auth gas used 用 compact（C.6 風格），WorkResult.AccumulateGas 也是 compact，而 π_V/π_L 的統計用 E_4。這些細節是 codec test vectors 的核心。",
 "trap": "面試若問「為什麼 state 用 fixed-length」：可預測大小、Merklization 友善、避免同值多種編碼。"
},
{
 "id": "appD-state-key",
 "ch": "D", "section": "D.1 Serialization (state-key constructor C)", "gpRef": "§D.1 eq. C",
 "difficulty": 3, "kind": "concept", "tags": ["merklization", "state-keys"],
 "stem": "The state-key constructor C maps to 31-octet keys. Which forms are correct?",
 "options": [
  "C(i) = [i, 0, 0, …]; C(i, s) = [i, n_0, 0, n_1, 0, n_2, 0, n_3, 0, …] with n = E_4(s); C(s, h) = [n_0, a_0, n_1, a_1, n_2, a_2, n_3, a_3, a_4, …, a_26] with n = E_4(s) and a = H(h) — service-id bytes interleaved with the first 4 hash bytes, then hash bytes 4..26",
  "C(i) = [i, 0, 0, …]; C(i, s) = [i, n_0, n_1, n_2, n_3, 0, 0, …] with n = E_4(s); C(s, h) = [n_0, a_0, n_1, a_1, n_2, a_2, n_3, a_3, a_4, …, a_26] with n = E_4(s) and a = H(h) — the service id sits in one contiguous run and only the hash bytes are interleaved",
  "C(i) = [i, 0, 0, …]; C(i, s) = [i, n_0, 0, n_1, 0, n_2, 0, n_3, 0, …] with n = E_4(s); C(s, h) = [n_0, a_0, n_1, a_1, n_2, a_2, n_3, a_3, a_4, …, a_27] with n = E_4(s) and a = h itself — the raw 32-octet key is interleaved and the result runs to 32 octets",
  "C(i) = [0, …, 0, i] with the chapter index in the final octet; C(i, s) = [i, n_0, 0, n_1, 0, n_2, 0, n_3, 0, …] with n = E_4(s); C(s, h) = [n_0, a_0, n_1, a_1, n_2, a_2, n_3, a_3, a_4, …, a_26] with n = E_4(s), a = H(h) and h the raw storage key for a storage item"
 ],
 "answer": 0,
 "optNotes": [
   "C(i, s) 的 service-id byte 與 0 交錯、C(s, h) 取 a = H(h)，且值域固定為 B_31。",
   "service-id 四個 byte 若連成一段，相鄰 service 的 key 在 trie 中就不會散開。",
   "a 是 H(h)（Blake2b）而不是原始 h，且 C 的值域是 B_31，31 octets 才對。",
   "C(i) 是 [i, 0, 0, …]（index 在最前），storage 走的也是 C(s, E_4(2^32−1) ⌢ k) 而非原始 key。",
 ],
 "explanation": "§D.1：C: N_2^8 ∪ (N_2^8, N_S) ∪ (N_S, B) → B_31。C(i) = [i, 0, …]（chapter i 的單一元件：1 α、2 φ、3 β、4 γ、5 ψ、6 η、7 ι、8 κ、9 λ、10 ρ、11 τ、12 χ、13 π、14 ω、15 ξ、16 θ）；C(255, s) 是 service s 的 account info（[255, n_0, 0, n_1, 0, n_2, 0, n_3, 0, …]）；C(s, h) 用於 storage / preimage / request：n 與 a = H(h) 的前 4 bytes 交錯（交錯是為了讓相鄰 service 的 key 在 trie 中散開），再接 a_4…a_26。storage key h = E_4(2^32−1) ⌢ k、preimage h = E_4(2^32−2) ⌢ hash、request h = E_4(l) ⌢ hash（l 是長度，因為 preimage < 2^32 所以不會與前兩者碰撞）。§D.1 末：「JAM does not allow service storage keys to be directly inspected or enumerated」——實作可以只存 hash 後的 key。",
 "trap": "31 bytes（不是 32）：讓 leaf node 的 1 byte header + 31 key + 32 value 剛好 64 bytes。"
},
{
 "id": "appD-trie-nodes",
 "ch": "D", "section": "D.2 Merklization (node encoding)", "gpRef": "§D.2.1 B and L functions, M",
 "difficulty": 2, "kind": "concept", "tags": ["merklization", "trie"],
 "stem": "How are nodes of the state Patricia Merkle trie encoded?",
 "options": [
  "Every node is 512 bits. Branch: bit 0 = 0, then the last 255 bits of the left child's hash, then the full 256 bits of the right child's hash. Leaf with value ≤ 32 octets: bits 10 + 6-bit value length, the 31-octet key, then the value zero-padded to 32 octets. Leaf with larger value: bits 11000000, the 31-octet key, then H(value). Empty (sub)trie = zero hash; node identity = Blake2b of the 64 octets",
  "Every node is 512 bits. Branch: bit 0 = 0, then the full 256 bits of the left child's hash, then the last 255 bits of the right child's hash. Leaf with value ≤ 32 octets: bits 10 + 6-bit value length, the 31-octet key, then the value zero-padded to 32 octets. Leaf with larger value: bits 11000000, the 31-octet key, then H(value). Empty (sub)trie = H([]); node identity = Blake2b of the 64 octets",
  "Every node is 512 bits. Branch: bit 0 = 0, then the last 255 bits of the left child's hash, then the full 256 bits of the right child's hash. Leaf with value ≤ 32 octets: bits 10 + 6-bit value length, the 31-octet key, then H(value). Leaf with larger value: bits 11000000, the 31-octet key, then the value's first 32 octets. Empty (sub)trie = zero hash; node identity = Keccak of the 64 octets",
  "Every node is 512 bits. Branch: bit 0 = 1, then the last 255 bits of the left child's hash, then the full 256 bits of the right child's hash. Leaf with value ≤ 32 octets: bits 00 + 6-bit value length, the 31-octet key, then the value zero-padded to 32 octets. Leaf with larger value: bits 01000000, the 31-octet key, then H(value). Empty (sub)trie = zero hash; node identity = Blake2b of the 64 octets"
 ],
 "answer": 0,
 "optNotes": [
   "左子截成後 255 bits 以騰出 discriminator bit、右子取滿 256；空子樹識別為 zero hash。",
   "§D.2.1 是左子取後 255 bits、右子取滿 256 bits；空子樹識別為 H_0 而不是 H([])。",
   "L 的定義正好相反（內嵌存 value 補零、大值存 H(v)），且 state trie 全程用 Blake2b。",
   "GP 是第一個 bit 為 0 才是 branch、為 1 是 leaf，第二個 bit 再分內嵌與一般 leaf。",
 ],
 "explanation": "§D.2.1：「Nodes are fixed in size at 512 bit (64 bytes). Each node is either a branch or a leaf. The first bit discriminate between these two types.」B(l, r) = [0] ⌢ bits(l)[1..] ⌢ bits(r)——「the last 255 bits of the 0-bit (left) sub-trie identity and the full 256 bits of the 1-bit (right) sub-trie identity」；L(k, v) = [1, 0] ⌢ bits(E_1(|v|))[2..] ⌢ bits(k) ⌢ bits(v) ⌢ 0-padding 當 |v| ≤ 32，否則 [1,1,0,0,0,0,0,0] ⌢ bits(k) ⌢ bits(H(v))。M(d)：空 → H_0（zero hash）；單一 → H(L(k, v))；否則 H(B(M(l), M(r)))，依 key 的下一個 bit 分左右（MSB-first）。設計理由：「a format optimized for modern compute hardware, primarily by optimizing sizes to fit succinctly into typical memory layouts and reducing the need for unpredictable branching」。Keccak 只出現在 accumulation output belt，state trie 全程 Blake2b。",
 "trap": "左子 hash 丟掉最高位（255 bits）以騰出 discriminator bit；值 ≤ 32 bytes 內嵌可省一次 hash。"
},
{
 "id": "appE-merkle-functions",
 "ch": "E", "section": "E.1 Binary Merkle Trees & E.2 MMR", "gpRef": "eq. E.1–E.8",
 "difficulty": 2, "kind": "concept", "tags": ["merklization", "mmr"],
 "stem": "Which description of the general Merklization functions is correct?",
 "options": [
  "N (node): splits the sequence at ⌈n/2⌉ and hashes '$node' ⌢ left ⌢ right (well-balanced); M_B is the well-balanced root taken over the RAW blobs (it deliberately avoids hashing each item); M (constant-depth) first hashes each leaf as '$leaf' ⌢ v and pads to a power of two with zero hashes — used for segment roots and paged proofs; the MMR append A adds a peak with binary-addition-style carrying and the super-peak folds the peaks with a '$peak' prefix",
  "N (node): splits the sequence at ⌊n/2⌋ so the right half is the larger one, and hashes '$node' ⌢ left ⌢ right; M_B is the well-balanced root taken over the RAW blobs; M (constant-depth) first hashes each leaf as '$leaf' ⌢ v and pads to a power of two by repeating the final leaf rather than with zero hashes; the MMR append A gives every leaf its own new peak without any carrying, and the super-peak folds the peaks with a '$peak' prefix",
  "N (node): splits the sequence at ⌈n/2⌉ and hashes left ⌢ right with no domain-separation prefix, the prefixes being reserved for leaves; M_B is the constant-depth root that pads to a power of two while M is the well-balanced root over the raw blobs — the two are named for their leaf treatment, not their shape; the MMR append A carries like binary addition and the super-peak folds the peaks with a '$node' prefix under Blake2b",
  "N (node): splits the sequence at ⌈n/2⌉ and hashes '$node' ⌢ left ⌢ right (well-balanced); M_B hashes every item as '$leaf' ⌢ v before building the tree, which is what costs it one extra hash per item; M (constant-depth) takes the RAW blobs and pads to a power of two with zero hashes; the MMR append A carries like binary addition and the super-peak folds the peaks with a '$peak' prefix, but is defined only when the number of peaks is a power of two"
 ],
 "answer": 0,
 "optNotes": [
   "M_B 直接把原始 blob 當 leaf（GP 明說 avoids hashing each item），M 才先 $leaf 雜湊再零填。",
   "三處都相反：GP 是 ⌈n/2⌉ 切、補 zero hash H_0、A 遇到已占用的 slot 就折疊進位。",
   "N 的定義本身就含 $node 前綴，M_B 與 M 的角色被對調，super-peak 用 $peak 且是 Keccak。",
   "加 $leaf 的是 constancy preprocessor C，且 super-peak 對任意個非 ∅ peak 都遞迴定義。",
 ],
 "explanation": "eq. E.1：N(v, H) = H_0 若空；v_0 若單一；否則 H($node ⌢ N(v[..⌈n/2⌉]) ⌢ N(v[⌈n/2⌉..]))——「well-balanced」使最大深度最小。前綴 $node/$leaf 防止 preimage collision。E.3：M_B(v, H) = H(v_0) 當 |v| = 1，否則 N(v, H)——直接把原始 blob 當 leaf、不加 $leaf 前綴（GP 明說它「avoids hashing each item in the sequence」）；用於 extrinsic hash 與 accumulation output belt 的每塊 root（Keccak）。E.4：M（constant depth）先 $leaf 雜湊、零填到 2 的冪——segment root 與 paged proofs（J_x/L_x, x = 6 即每 64 個 leaf 一頁）用它，因為固定深度讓 import 證明大小固定。E.8：MMR append A（peaks 序列，像二進位加法進位），super-peak 用 $peak 前綴從左到右摺疊。β_B 就是這種 MMR（Keccak）。",
 "trap": "M_B 取 root 的分割點是 ⌈n/2⌉（左邊較多）；M 是零填到 2^k。"
},
{
 "id": "appH-chunking",
 "ch": "H", "section": "H Erasure Coding", "gpRef": "eq. H.5–H.6",
 "difficulty": 2, "kind": "concept", "tags": ["erasure-coding"],
 "stem": "How does the chunking function 𝒞^v_k turn a data blob into v chunks, and what makes the code 'systematic'?",
 "options": [
  "The blob (padded to a multiple of 2·d(v) octets) is split into k pieces of d(v) octet-pairs; each piece is erasure-coded into v octet-pairs; the results are transposed so that chunk i holds the i-th pair of every piece (k pairs per chunk); systematic means the first d(v) chunks are the original data, so if they are all present reconstruction is mere concatenation",
  "The blob (padded to a multiple of 2·v octets) is split into v pieces of one octet-pair each; each piece is erasure-coded into d(v) octet-pairs; the results are concatenated rather than transposed, so chunk i is a contiguous slice of the coded stream; systematic means the parity pairs sit after the data, so any v − d(v) chunks reconstruct",
  "The blob (padded to a multiple of 2·d(v) octets) is split into k pieces of d(v) octet-pairs; each piece is erasure-coded into v octet-pairs; the pieces are then hashed and it is those hashes, not the coded pairs, that are handed out as chunks; systematic means every chunk carries a Merkle proof of its own index, so one chunk can be checked without reconstructing anything",
  "The blob (padded to a multiple of 2·d(v) octets) is split into k pieces of d(v) octet-pairs; each piece is erasure-coded into v octet-pairs over GF(2^8) in the standard polynomial basis; the results are transposed so that chunk i holds the i-th pair of every piece; systematic means the encoder is its own inverse, so coding a blob twice returns the blob"
 ],
 "answer": 0,
 "optNotes": [
   "systematic 的意義是前 𝒟(v) 個 chunk 就是原始資料，全在手時還原只是串接。",
   "方向整個顛倒：eq. H.5 是切成 k 段、每段 𝒟(v) 個 pair 編成 v 個 pair 再轉置。",
   "chunk 就是轉置後的 coded octet-pair 本身，雜湊只發生在組 erasure-root 的 b^♣ 那一步。",
   "§H 明訂 GF(2^16)（x^16 + x^5 + x^3 + x^2 + 1）並改用 Cantor basis，systematic 也與自反性無關。",
 ],
 "explanation": "eq. H.5：𝒞^v_k(d) = join(T[C_v(p) | p ∈ T(split_2(split_2k(d)))])——拆開來看是四步：**① 分段**——資料補齊到 2·𝒟(v) 的倍數後切成 k 段，每段 𝒟(v) 個 octet-pair；**② 編碼**——每一段各自做 Reed–Solomon，從 𝒟(v) 個 pair 擴成 v 個 pair；**③ 轉置**——把結果轉置，讓第 i 個 chunk 收集**每一段的第 i 個 pair**；**④ 串接**——於是共 v 個 chunk，每個含 k 個 pair。**轉置是關鍵**：它讓每個 chunk 都均勻地含有全部 k 段的一小片，所以任何 𝒟(v) 個 chunk（附索引）就能還原全部（eq. H.6）——而不是「某幾段的 chunk 湊齊才救得回那幾段」。**systematic 的意思**：前 𝒟(v) 個 chunk **就是原始資料本身**，沒有經過變換。GP 明說「If the original d items are known then reconstruction is just their concatenation」——也就是說在正常情況（持有前 342 個 chunk）下，重建的成本是**零**，只要接起來；只有在缺片時才需要跑代價高的 RS 解碼。**兩個使用情境**：Audit DA 處理 work-package bundle（變長），Import DA 處理固定 4,104 位元組的 segment。實作用 Cantor basis 的 GF(2^16)。",
 "trap": "shard/chunk 數 = |κ′|（每個 validator 一個）；erasure root 是對這些 chunk 的 Merkle root。"
},
]
