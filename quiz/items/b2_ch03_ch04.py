# -*- coding: utf-8 -*-
# Batch 2 — Chapter 3 (Notational Conventions) and Chapter 4 (Overview), GP 0.8.0
ITEMS = [
# ---------------------------------------------------------------------------------------------
# §3 Notational Conventions
# ---------------------------------------------------------------------------------------------
{
 "id": "ch03-sequence-set-subscripts",
 "ch": "3", "section": "3.7 Sequences", "gpRef": "§3.7 (⟦T⟧, ⟦T⟧_n, ⟦T⟧_{:n}, ⟦T⟧_{n:}, ⟦T⟧_N); applied in eq. 8.1 and eq. 6.22",
 "difficulty": 2, "kind": "concept", "tags": ["notation", "sequences", "types"],
 "stem": "Eq. 8.1 types the authorizer pool and queue as α ∈ ⟦⟦H⟧_{:O}⟧_C and φ ∈ ⟦⟦H⟧_Q⟧_C, and eq. 6.22 types the entropy as η ∈ ⟦H⟧_4. Using the sequence-set notation of GP §3.7, what do these subscripts say?",
 "options": [
  "⟦H⟧_{:O} is the set of hash sequences of length at most O, ⟦H⟧_Q of length exactly Q and ⟦H⟧_4 of length exactly 4; the outer ⟦·⟧_C means exactly one inner sequence per core",
  "⟦H⟧_{:O} is the set of hash sequences of length at least O (a pool must be kept full), while ⟦H⟧_Q and ⟦H⟧_4 are sequences of length at most Q and at most 4 respectively",
  "⟦H⟧_{:O} denotes the first O elements of a hash sequence (a slice), so α is an O-element prefix of each core's queue, and ⟦H⟧_Q denotes the single element at index Q",
  "All three denote sequences of exactly that many hashes; the colon in ⟦H⟧_{:O} only marks that the pool is indexed cyclically (H_T mod O) rather than from zero"
 ],
 "answer": 0,
 "optNotes": [
  "冒號在前是上限、無冒號是恰好：pool 可未滿甚至為空，queue 每 core 恰好 Q = 80。",
  "把 _{:n} 與 _{n:} 的方向弄反了；「至少 n 個」要寫成 ⟦T⟧_{n:}。",
  "把型別標記當成切片語法；取前 n 個元素要寫 s_{…n} 或 →s^n。",
  "cyclic index 是 ⟲ 上標（s[i]^⟲ ≡ s[i mod |s|]）的事，與型別下標無關。",
 ],
 "explanation": "GP §3.7：⟦T⟧ 是元素取自 T、長度任意的序列集合（定義一個 ℕ → T 的 partial mapping）；⟦T⟧_n 是「containing exactly n elements」（complete mapping ℕ_n → T）；「sets of sequences of at most n elements and at least n elements may be denoted ⟦T⟧_{:n} and ⟦T⟧_{n:} respectively」；⟦T⟧_N 則是長度落在集合 N 內。套進題目：α ∈ ⟦⟦H⟧_{:O}⟧_C 是每個 core（C = 341）一條至多 O = 8 個 authorizer hash 的 pool，φ ∈ ⟦⟦H⟧_Q⟧_C 每 core 恰好 Q = 80，eq. 6.22 的 η ∈ ⟦H⟧_4 恰好 4 個 entropy 值。你們的 Go 型別完全對應：`AuthPool.Validate` 只檢查 len ≤ AuthPoolMaxSize(8)，`AuthQueue.Validate` 要求 len == AuthQueueSize(80)，兩者外層都要求 len == CoresCount（internal/types/types.go §8.1 區段）。",
 "trap": "冒號在前（_{:n}）= 上限、冒號在後（_{n:}）= 下限、沒冒號 = 恰好；pool 可空、queue 固定 80。"
},
{
 "id": "ch03-first-last-n-arrows",
 "ch": "3", "section": "3.7.2 Editing", "gpRef": "§3.7.2 (⌢, ⧺, →s^n, ←s^n) and §3.7 (⟲); applied in eq. 7.8, eq. 8.2 and eq. 6.35",
 "difficulty": 2, "kind": "concept", "tags": ["notation", "sequences", "arrows"],
 "stem": "Three state-transition rules use the arrow operators of GP §3.7.2: β_H′ ≡ ←(β_H† ⧺ e)^H (eq. 7.8), α′[c] ≡ ←(F(c) ⧺ φ′[c][H_T]^⟲)^O (eq. 8.2) and γ′_A ≡ →(n ∪ γ_A sorted ascending by ticket id)^E (eq. 6.35). Which reading is correct?",
 "options": [
  "←^n keeps the first n elements and →^n the last n: β_H′ and α′[c] therefore drop the newest entry once they are full, while γ′_A keeps the E largest ticket ids",
  "→^n keeps the first n elements and ←^n the last n: β_H′ and α′[c] retain the H = 8 and O = 8 most recently appended entries, while γ′_A retains the E = 600 smallest ticket ids",
  "Both arrows keep n elements counted from the front; the direction only records whether the sequence was extended with ⧺ (append at the right) or with ⌢ (prepend at the left)",
  "The arrows are cyclic rotations by n positions, the same operation as the ⟲ superscript, so β_H′ and α′[c] behave as ring buffers whose oldest slot is overwritten in place"
 ],
 "answer": 1,
 "optNotes": [
  "箭頭意義對調了：這樣會保留最舊、丟掉最新，且排序後取 →^E 拿到的是最小者不是最大者。",
  "→ 留頭、← 留尾：β_H′ 與 α′[c] 保留最後 8 筆，γ′_A 取排序後最前 600 個最小 ticket id。",
  "忽略了 ← 的定義（「only the final elements」）；⌢ 與 ⧺ 都接在右側，沒有 prepend 語意。",
  "把截斷與 ⟲ 模數索引混為一談；β_H、α 是會伸縮的序列，不是原地覆寫的 ring buffer。",
 ],
 "explanation": "GP §3.7.2：「We denote the sequence made up of the first n elements of sequence s to be →s^n ≡ [s_0, s_1, …, s_{n−1}], and only the final elements as ←s^n」。同節定義 ⌢ 為序列串接、⧺ 為元素接尾（x ⧺ i ≡ x ⌢ [i]）；§3.7 的 s[i]^⟲ ≡ s[i % |s|] 是模數索引，所以 φ′[c][H_T]^⟲ = φ′[c][H_T mod Q]（Q = 80）。三條規則的共同結構都是「先接、再截」：eq. 7.8 與 eq. 8.2 用 ←^n 保留最後 H = 8 / O = 8 筆（丟最舊），eq. 6.35 用 →^E 取排序後最前面 E = 600 個，GP 原文即「the accumulator becomes the lowest items of the sorted union」。你們的 code 三處都對得上：`alpha[c] = alpha[c][len-8:]`（authorization.go）、ticket accumulator 升冪排序後 `[:EpochLength]`（extrinsic_tickets.go）、`AddItem2BetaHPrime` 滿 8 筆時 `copy(historyPrime, historyDagger[1:])` 丟最舊。",
 "trap": "箭頭指向哪邊就留哪邊：→ 留頭、← 留尾。§3.4 另有 % 為 mod、「5 ÷ 3 = 1 R 2」為商餘寫法（§6.1 的 e R m = τ/E 即 e = ⌊τ/E⌋、m = τ mod E）。"
},
{
 "id": "ch03-bits-msb-first-trie",
 "ch": "3", "section": "3.7.3 Boolean values", "gpRef": "§3.7.3 bits(); eq. D.5–D.6 (M_σ, M); App. C.1.4 (bit-sequence encoding); eq. A.15 (PVM ℬ_n)",
 "difficulty": 3, "kind": "code", "tags": ["notation", "bits", "merklization", "codec"],
 "stem": "GP §3.7.3 defines bits(B) for an octet sequence B by the example bits([160, 0]) = [1, 0, 1, 0, 0, …], and M_σ (eq. D.5) keys the state trie by bits(k) of the 31-octet state key. The team's trie splits entries at each depth with the code below. Is it consistent with the GP?",
 "code": {"lang": "go", "caption": "internal/utilities/merklization/merklization.go (partitionByBit)", "src": """func partitionByBit(entries []types.StateKeyVal, depth int) int {
	byteIdx := depth / 8
	bitMask := byte(1 << (7 - depth%8))
	left := 0
	for right := range entries {
		if entries[right].Key[byteIdx]&bitMask == 0 {
			entries[left], entries[right] = entries[right], entries[left]
			left++
		}
	}
	return left
}"""},
 "options": [
  "No: bits() is least-significant-bit first, matching the codec's bit-sequence encoding E(b ∈ 𝕓) which packs b_i into 2^i, so the mask must be 1 << (depth mod 8)",
  "No: bits() is MSB-first, but M_σ keys the trie by bits(H(k)) — the Blake2b hash of the state key — so the partition must be taken over H(k) rather than the raw key",
  "No: bits() is MSB-first, but the first bit of every node is the branch/leaf discriminator, so the key path must skip bit 0 of key[0] and the mask should start at 1 << (6 − depth mod 8)",
  "Yes: 160 = 0b10100000, so bits() emits each octet's most significant bit first; masking key[depth/8] with 1 << (7 − depth mod 8) walks the path in exactly that order"
 ],
 "answer": 3,
 "optNotes": [
  "LSB-first 的是 App. C.1.4 的 E(b ∈ 𝕓) 與 assurance bitfield；§3.7.3 的 bits() 是 MSB-first。",
  "那是 Ethereum MPT 的做法（keccak(key) 當 path）；eq. D.5 直接用 31-octet state key 的 bits(k)。",
  "discriminator 在 node encoding（eq. D.3）裡、不在 key path 裡，key 的每個 bit 都要走。",
  "160 = 0b10100000 對上 [1,0,1,0,0,…]，1 << (7 − depth mod 8) 正是 MSB-first 的走法。",
 ],
 "explanation": "GP §3.7.3：bits(B) 是「the sequence of bits, ordered with the most significant first, which represent the octet sequence B」，160 = 0b10100000 → [1,0,1,0,0,0,0,0]。eq. D.5：M_σ(σ) ≡ M({bits(k) ↦ (k, v) | (k ↦ v) ∈ T(σ)})，eq. D.6 依 key 的第一個 bit 分左右子樹（k_0 = 0 → 左、1 → 右）再遞迴，所以深度 d 對應 key[d/8] 的第 (7 − d mod 8) 位——`partitionByBit` 正確。真正的陷阱是 GP 裡並存三個方向不同的 bit 函數：App. C.1.4 的 E(b ∈ 𝕓)「pack the bits into octets in order of least significant to most」（b_i 放在 2^i），因此 bits() **不是** E(𝕓) 的反函數（E(bits([160])) = [5] ≠ [160]）；PVM 的 ℬ_n（eq. A.15）同樣是 LSB-first 且作用在自然數上。你們的 assurance bitfield 解碼 `(bytes[i/8] >> (i%8)) & 1`（types.go `MakeBitfieldFromByteSlice`）是 LSB-first、對應 codec，與 trie 的 MSB-first 各自都對，混用才錯。",
 "trap": "bits() = MSB-first（trie path）；E(𝕓)、PVM ℬ_n = LSB-first（bitfield、暫存器）。"
},
{
 "id": "ch03-vrf-signature-notation",
 "ch": "3", "section": "3.8.2 Signing Schemes", "gpRef": "§3.8.2; applied in eq. 6.16 (seal), eq. 6.18 (H_V), eq. 6.30 (ticket proof) and eq. 6.32 (ticket id = Y)",
 "difficulty": 3, "kind": "concept", "tags": ["notation", "crypto", "vrf", "safrole"],
 "stem": "GP §3.8.2 writes a Bandersnatch VRF signature as Ṽ_k^m⟨x⟩ ⊂ B_96 with VRF output Y(·) ∈ H, and eq. 6.16 requires H_S ∈ Ṽ_{H_A}^{E_U(H)}⟨X_T ⌢ η′_3 ⧺ i_e⟩. Which statement is correct?",
 "options": [
  "The angle brackets carry the message and the superscript the context, so Y(H_S) depends on the header serialization E_U(H); this is what lets the seal's VRF output commit to the block content",
  "k = H_A is the signer's public key, the superscript E_U(H) is the signed message and the angle-bracketed term is the context; Y(H_S) is determined by the key and the context but not by the message",
  "Ṽ is the anonymous Ring-VRF form: H_A is a ring root over the validator keys and the signer cannot be identified, whereas the identifying form V̊ ⊂ B_784 is the one tickets use",
  "Y(H_S) is a 96-octet value; the 32-octet ticket identifier i_y is obtained as H(Y(H_S)), and Ed25519 signatures V̄_k⟨m⟩ likewise define a VRF output"
 ],
 "answer": 1,
 "optNotes": [
  "⟨⟩ 裝的是 context、上標才是訊息；若反過來，Y 會隨 header 內容改變而失去 bias-resistance。",
  "下標鑰、上標訊息、⟨⟩ context，且 VRF output「influenced by x but not by m」。",
  "具名與匿名說反了：Ṽ 具名、V̊ 才匿名；H_A 是單一公鑰，不是 B̊ 裡的 ring root。",
  "Y(·) ∈ H 本身就是 32 octet，eq. 6.16 直接令 i_y = Y(H_S)；Ed25519 也沒有 VRF output。",
 ],
 "explanation": "GP §3.8.2：Bandersnatch 簽名 Ṽ_k^m⟨x⟩ 的下標 k 是公鑰、上標 m 是訊息、⟨⟩ 內的 x 是 context（LaTeX 巨集 \\bssignature{k}{x}{m} 排版成 Ṽ_k^m⟨x⟩）；「both define a VRF output, a high entropy hash influenced by x but not by m」。具名式與匿名式的差別則是「the member is identified in the former [Ṽ] and is anonymous in the latter [V̊]」——ring proof V̊_r^m⟨x⟩ ⊂ B_784 以 ring root r ∈ B̊ ⊂ B_144（由 O(keys) 算出）為下標。所以 eq. 6.16 的 seal 以未簽名 header E_U(H) 為訊息、X_T ⌢ η′_3 ⧺ i_e 為 context，Y(H_S) 只由金鑰與 context 決定——這正是 i_y = Y(H_S)（ticket id 在上一個 epoch 就能驗）以及 eq. 6.18 H_V ∈ Ṽ_{H_A}^{[]}⟨X_E ⌢ Y(H_S)⟩ 能當 bias-resistant entropy 的原因：作者改動 header 內容不會改變 VRF output。你們的 `createSignatureContext`（extrinsic_tickets.go）組的就是 ⟨⟩ 裡的 context（$jam_ticket_seal ⌢ η′_2 ⧺ attempt），訊息為空。",
 "trap": "Ṽ_k^m⟨x⟩：下標鑰、上標訊息、⟨⟩ context；Y 看 context 不看訊息。Ṽ 具名 96 B、V̊ 匿名 784 B、V̄ Ed25519 64 B。"
},
{
 "id": "ch03-hash-functions-and-codec-subscripts",
 "ch": "3", "section": "3.8.1 Hashing", "gpRef": "§3.8.1 (H, H_K, H_0, E_l and E^{-1}_l assertions); Keccak applied in eq. 7.7",
 "difficulty": 2, "kind": "concept", "tags": ["notation", "hashing", "codec"],
 "stem": "Per GP §3.8.1, which statement about the hash functions and the subscripted codec functions is correct?",
 "options": [
  "H is Keccak-256 as in the Yellow Paper and H_K is Blake2b-256; the subscript on E counts the octets of the input, so E_4 accepts only arguments already in B_4 and E^{-1}_8 only naturals below 2^64",
  "H is Blake2b-256 and H_K is Keccak-256; hashing a tuple is undefined unless it is written explicitly as H(E(…)), and E_4 is the general variable-length natural encoding capped at four octets",
  "H is Blake2b-256 and H_K is Keccak-256, both into H ≡ B_32; a non-blob argument is implicitly passed through E; E_4(x) asserts x ∈ N_2^32 and yields B_4, and E^{-1}_8(y) asserts y ∈ B_8 and yields N_2^64",
  "H is Blake2b-512 truncated to 32 octets and H_K is Keccak-256; H_0 denotes H([]), the hash of the empty blob, which is also how M_σ identifies an empty sub-trie"
 ],
 "answer": 2,
 "optNotes": [
  "H 與 H_K 對調了；下標指的也是 octet 序列那一端的長度，不是輸入端。",
  "GP 明說輸入會隱含通過 E，tuple 可直接放進 H；E_4 是固定長度 little-endian，不是 compact 編碼的上限。",
  "下標永遠釘住 octet 端：E_4(x) 斷言 x ∈ N_2^32 且結果 ∈ B_4，E^{-1}_8 反向亦然。",
  "H 是 Blake2b-256 而非截斷的 512；H_0 是 [0]_32，不是 H([])。",
 ],
 "explanation": "GP §3.8.1：「H denotes the set of 256-bit values equivalent to B_32. All hash functions in the present work output to this type and H_0 is the value equal to [0]_32」；H(m ∈ B) 是 Blake2b 256-bit（RFC 7693）、H_K(m ∈ B) 是 Keccak 256-bit（Ethereum YP 所用）。「The inputs of a hash function should be expected to be passed through our serialization codec E to yield an octet sequence… (Note that an octet sequence conveniently yields an identity transform.)」——所以 H(H)、H(E_4(s) ⌢ E(h)) 這類寫法不需要明寫 E。下標規則同節寫死：「we may subscript the transformation function with the number of octets we expect the octet sequence term to have. Thus, r = E_4(x ∈ N) would assert x ∈ N_2^32 and r ∈ B_4, whereas s = E^{-1}_8(y ∈ B) would assert y ∈ B_8 and s ∈ N_2^64」（App. C.1.7 的固定長度 little-endian）。Keccak 只用於 β_B accumulation-output belt（eq. 7.7，「to maximize compatibility with legacy systems」），header hash、state trie、erasure root 等都是 Blake2b。你們的 `internal/utilities/hash/hash.go`：`Blake2bHash` / `KeccakHash`。",
 "trap": "H = Blake2b、H_K = Keccak、H_0 = 32 個 0；E_l 的 l 指 octet 長度那一端；tuple 進 H 隱含先 E。"
},
{
 "id": "ch03-dictionary-semantics",
 "ch": "3", "section": "3.5 Dictionaries", "gpRef": "eq. 3.7–3.11; 𝒰 in eq. 3.2; ∅ / A? / ∇ in §3.3",
 "difficulty": 2, "kind": "concept", "tags": ["notation", "dictionaries", "calc"],
 "stem": "Let d = {1 ↦ a, 2 ↦ b} and e = {2 ↦ c, 3 ↦ a} be dictionaries in ⟨N → B⟩. Applying GP §3.5 (eq. 3.7–3.11), which statement is correct?",
 "options": [
  "d ∪ e = {1 ↦ a, 2 ↦ b, 3 ↦ a} because the left operand wins on a collision; V(d ∪ e) = [a, b, a] keeps duplicates in insertion order; and d[3] = ∅ is an ordinary, valid lookup result in every context",
  "d ∪ e is undefined because key 2 collides — dictionary union is only defined when K(d) ⫰ K(e), which is why the GP always writes (d ∖ K(e)) ∪ e out explicitly instead of d ∪ e",
  "d ∖ {2} removes the pairs whose value is 2, so d ∖ {2} = d; K(e) = {c, a}; and d ∪ e = {1 ↦ a, 2 ↦ c, 3 ↦ a} because the right operand wins on a collision",
  "d ∪ e = {1 ↦ a, 2 ↦ c, 3 ↦ a} because the right operand wins on a collision; V(d ∪ e) = {a, c}; and writing d[3] in a rule asserts that key 3 exists — a block relying on it without handling ∅ is invalid"
 ],
 "answer": 3,
 "optNotes": [
  "eq. 3.11 是右邊優先，V(·) 回傳的集合也會去重；d[k] 更是隱含斷言 key 存在。",
  "union 正是為了處理衝突而定義的，(d ∖ K(e)) ∪ e 就是它的定義本身，不是替代寫法。",
  "∖ 減的是鍵集合（eq. 3.8）、K(·) 取的也是鍵（eq. 3.9），所以 K(e) = {2, 3} 而非值。",
  "右邊優先、V 去重，且 GP 明說下標是「an implicit assertion that the key exists」。",
 ],
 "explanation": "逐步計算：eq. 3.11 d ∪ e ≡ (d ∖ K(e)) ∪ e，「priorities the right-side operand in the case of a key-collision」：K(e) = {2, 3}（eq. 3.9），d ∖ K(e) = {1 ↦ a}（eq. 3.8，減去的是鍵集合 s ⊆ K），再聯集 e 得 {1 ↦ a, 2 ↦ c, 3 ↦ a}；eq. 3.10 的 V(·) 是**集合**，「should different keys with equal values appear in the dictionary, the set will only contain one such value」，故 V(d ∪ e) = {a, c}。查詢的陷阱藏在 eq. 3.7 之後那句：形式上 d[k] ≡ v 若存在、否則 ∅，但 GP 緊接著說「when using a subscript, it is an implicit assertion that the key exists in the dictionary. Should the key not exist, the result is undefined and any block which relies on it must be considered invalid」——要容許缺鍵就必須明寫處理，GP 自己的模式是 𝒰(d[k], default)（eq. 3.2 substitute-if-nothing）或先用 s ∈ K(d) 守門（accumulation 的 providable 函數 Y）。另外 §3.3：∅ 表示「validly left without a specific value」（|∅| = 0，A? ≡ A ∪ {∅}），∇ 才表示錯誤／無效。",
 "trap": "∪ 右邊贏；∖ 減鍵；K 鍵集、V 值集（去重）；缺鍵要嘛 𝒰(…) 給預設、要嘛 block 無效。"
},
# ---------------------------------------------------------------------------------------------
# §4 Overview
# ---------------------------------------------------------------------------------------------
{
 "id": "ch04-dagger-intermediate-states",
 "ch": "4", "section": "4.2.1 State Transition Dependency Graph", "gpRef": "eq. 4.6, 4.12, 4.13, 4.14, 4.16, 4.17, 4.18",
 "difficulty": 2, "kind": "concept", "tags": ["stf", "intermediate-state", "ordering", "delta-0.8.0"],
 "stem": "GP 0.8.0's dependency graph names four dagger-superscripted intermediate states: β_H†, ρ†, ρ‡ and δ‡. Which description of what each one has just absorbed is correct?",
 "options": [
  "β_H† = β_H after this block's guarantees E_G are appended to the newest entry; ρ† = ρ after the assurances E_A; ρ‡ = ρ† after the guarantees E_G; δ‡ = δ after the preimages E_P are integrated, before accumulation runs",
  "β_H† = β_H with the parent's posterior state root H_R written into its newest entry; ρ† = ρ after the disputes E_D; ρ‡ = ρ† after the assurances E_A; δ‡ = δ after accumulating R*, before E_P is folded in",
  "β_H† = β_H after the accumulation-output log θ′ has been committed to the belt; ρ† = ρ after the guarantees E_G; ρ‡ = ρ† after the disputes E_D; δ‡ = δ after E_P is integrated and before deferred transfers are applied",
  "β_H† = β_H with H_R written in; ρ† = ρ after E_A; ρ‡ = ρ† after E_D; δ‡ = δ after E_P — the order of disputes and assurances is immaterial because both only remove entries from ρ"
 ],
 "answer": 1,
 "optNotes": [
  "eq. 4.6 的 β_H† 只依賴 (H, β_H)、補的是 parent 的 state root；E_P 也在 accumulation 之後才併入。",
  "四個中間態分別出自 eq. 4.6、4.12、4.13 與 4.16，順序與依賴列完全對得上。",
  "belt β_B 由 θ′ 更新、與 dagger 無關；ρ 的兩步也把 E_D 與 E_G 對調了。",
  "E_D 與 E_A 不可交換：assurance 只能對 ρ†[c] ≠ ∅ 的 core 設 bit（eq. 11.15）。",
 ],
 "explanation": "eq. 4.6 β_H† ≺ (H, β_H)：eq. 7.5 把 β_H 最後一筆的 state root（前一塊寫入時是 H_0）改為 H_R，即 parent 的 posterior root，要到本塊 header 才知道；eq. 4.12 ρ† ≺ (E_D, ρ)：disputes 先把 verdict 為 bad/wonky 的 report 從 core 清掉（eq. 10.14）；eq. 4.13 ρ‡ ≺ (E_A, ρ†)：assurances 讓 report 變 available（進入 R，eq. 11.17）或因 timeout 而移除（eq. 11.18）；eq. 4.14 ρ′ ≺ (E_G, ρ‡, κ, τ′)：最後才放入新 guarantee；eq. 4.16 (ω′, ξ′, δ‡, χ′, ι′, φ′, θ′, S) ≺ (R*, ω, ξ, δ, χ, ι, φ, τ, τ′)：accumulation 產出 δ‡（accumulation.tex 另稱 δ† 為 post-accumulation 的第一個中間態、δ‡ 為更新 last-accumulation 時戳 τ′ 後的第二個，overview 的圖只列 δ‡）；eq. 4.18 δ′ ≺ (E_P, δ‡, τ′)：preimage 最後併入。GP：「The latter two [4.17, 4.18] mark a merge and join in the dependency graph… the availability extrinsic may be fully processed and accumulation of work happen before the preimage lookup extrinsic is folded into state」。0.8.0 的符號也要跟上：新 available 的 report 序列寫作 R（R* 為 accumulatable，0.7.2 寫 W/R*），dagger 標在 β_H 上（β = (β_H, β_B)，belt β_B 不受 parent-root 修正影響）；你們 0.7.2 的 code 仍用 W/R*，`intermediateStates` 存 β†, ρ†, ρ‡, δ†, δ‡（chain_state.go）。",
 "trap": "口訣：β_H† 補 root；ρ† 判、ρ‡ 保、ρ′ 收；δ‡ 算完帳、δ′ 才收 preimage。"
},
{
 "id": "ch04-extrinsic-dependency-inputs",
 "ch": "4", "section": "4.2.1 State Transition Dependency Graph", "gpRef": "eq. 4.11–4.20",
 "difficulty": 3, "kind": "concept", "tags": ["stf", "extrinsic", "ordering"],
 "stem": "Reading the 0.8.0 dependency graph (eq. 4.5–4.20) literally, which statement about where the five extrinsic components enter the transition is TRUE?",
 "options": [
  "The preimages extrinsic E_P is an input to the accumulation step (eq. 4.16), so a service's accumulate code can read a preimage that was provided in the same block",
  "The assurances extrinsic E_A is a direct input to ρ′, i.e. ρ′ ≺ (E_G, E_A, ρ†, κ, τ′), because guarantees and assurances are processed together in one pass over the cores",
  "The guarantees extrinsic E_G is an input to ρ′, β_H′, α′ and π′, but not to the accumulation step, whose only extrinsic-derived input is R* (derived from E_A and ρ†)",
  "The disputes extrinsic E_D is a direct input to π′, because the validator statistics record which validators were reported as offenders in the block"
 ],
 "answer": 2,
 "optNotes": [
  "eq. 4.18 是 δ′ ≺ (E_P, δ‡, τ′)：preimage 在 accumulation 之後才併入，accumulate 讀不到同塊的。",
  "E_A 先產生 ρ‡（4.13），再由 E_G 覆蓋成 ρ′（4.14），並不是同一個 pass 的直接輸入。",
  "eq. 4.16 的輸入 (R*, ω, ξ, δ, χ, ι, φ, τ, τ′) 裡沒有任何 extrinsic，只有已 available 的 R*。",
  "π′ ≺ (E_G, E_P, E_A, E_T, τ, κ′, π, H, S) 不含 E_D；offender 記在 ψ′_O 與 header 的 H_O。",
 ],
 "explanation": "逐條讀 eq. 4.5–4.20：E_T → γ′ (4.7)、π′ (4.20)；E_D → ψ′ (4.11)、ρ† (4.12)；E_A → ρ‡ (4.13)、R* (4.15)、π′；E_G → ρ′ (4.14)、β_H′ (4.17)、α′ (4.19)、π′；E_P → δ′ (4.18)、π′。結構上的關鍵是 accumulation（4.16）與 extrinsic 之間隔了一層：report 必須先 **available**（E_A 超過 2/3 assurance，eq. 11.17）才會進入 R*，所以同一塊 E_G 裡的 report 最快也要下一塊才被 accumulate；而 preimage 的併入更排在 accumulation 之後（GP：「accumulation of work happen before the preimage lookup extrinsic is folded into state」）。你們 STF 的順序（code-map §2：ψ′ → ρ† → ρ‡ → accumulation → E_P 併入 → α′ → π′ 最後）與此一致。",
 "trap": "accumulation 的唯一「外部」輸入是 R*；E_P 最後、E_D 不進 π′。"
},
{
 "id": "ch04-in-core-300x-rationale",
 "ch": "4", "section": "4.8.1 In-core Consensus", "gpRef": "§4.9.1",
 "difficulty": 2, "kind": "rationale", "tags": ["architecture", "in-core", "scalability"],
 "stem": "The Overview states that JAM should be able to do 'upwards of 300 times' the computation in-core as a single machine running the VM at full speed. What justifies this figure, and what keeps such unreplicated computation safe?",
 "options": [
  "A given computation is executed by only a subset of validators, so throughput scales with network size rather than one machine; the guarantee/assure/audit (and if needed judge) game secures it, and stateless in-core execution can be reproduced by any node synced to the finalized chain",
  "Every validator still executes every in-core computation, but the PVM's recompiler makes RISC-V code roughly 300 times faster than EVM bytecode; safety therefore follows from full replication, exactly as in the on-chain model, and no auditing stage is required",
  "In-core results are accepted on the guarantors' signatures alone and are never re-executed by anyone else; the economic stake bonded by the guarantors (slashed on a later dispute) is what makes the 300x figure safe without any further verification",
  "The 300x comes from each of the 341 cores using the whole 6-second slot in parallel; in-core code may read arbitrary on-chain state as of the lookup-anchor block, and that anchoring is what makes its results reproducible by other nodes"
 ],
 "answer": 0,
 "optNotes": [
  "GP 給的理由正是「only a subset of the network」執行，算力隨網路規模而非單機擴展。",
  "那是 on-chain（everybody does everything）的描述；300x 也不是 PVM 對 EVM 的速度比。",
  "漏掉 auditing——「確保會有可期待為誠實的一方檢查」正是 ELVES 存在的理由。",
  "違反 stateless 設計：refine 只能透過 historical_lookup 讀 preimage，不能讀任意 on-chain state。",
 ],
 "explanation": "GP §4.9.1：「In this model… only a subset of the network is responsible for actually executing any given computation and assuring the availability of any input data it relies upon… we are able to scale the amount of computation done in consensus commensurate with the size of the network, and not with the computational power of any single machine… upwards of 300 times」。GP 沒有推導 300 這個數字；直觀上它與 core 數同量級——1023 validators / 每 core 3 guarantors = C = 341 cores，扣掉 audit、availability 等額外負擔即「300 多倍」（此為推論，非 GP 原文）。安全性來自「a crypto-economic game of three stages called guaranteeing, assuring, auditing and, potentially, judging」：guarantee 讓無效計算付出經濟代價、assure 確保輸入資料一段期間內可取得、audit 確保會有可期待為誠實的一方檢查正確性（judging 只在有爭議時發生）。並且「All execution done in-core must be reproducible by any node synchronized to the portion of the chain which has been finalized… designed to be as stateless as possible. The requirements… include only the refinement code of the service, the code of the authorizer and any preimage lookups it carried out」，lookup-anchor 必須落在 finalized chain 且夠新。",
 "trap": "三段式（guarantee → assure → audit，必要時 judge）；in-core = stateless、可由 finalized chain 重現；300x ≈ core 數量級。"
},
{
 "id": "ch04-best-block-vs-finalized",
 "ch": "4", "section": "4.6 Best block", "gpRef": "§4.6; §4.3 (head, finalized); §19 (best chain)",
 "difficulty": 2, "kind": "concept", "tags": ["consensus", "grandpa", "best-chain"],
 "stem": "GP §4.6 distinguishes the 'best block' from what the Grandpa finality gadget reports. Which statement matches the GP?",
 "options": [
  "The best block is the latest Grandpa-finalized block; JAM nodes never author on top of an unfinalized block, which is precisely why Grandpa lags only 1–2 blocks behind the most recent head and why no speculative state is ever exposed to applications",
  "The best block is simply the head — the valid block with the most ancestors — with ties between competing heads broken by the smaller header hash; Grandpa merely confirms that head some blocks later and plays no part in choosing a parent for authoring",
  "The best block is the head of the best chain (§19), used when latency matters more than certainty — choosing the parent for a block one is about to author, or reporting the latest state to a downstream application — at the risk that it never becomes canonical",
  "The best block is the most recent block whose timeslot is not in the future; Grandpa is consulted only afterwards, to prune whichever fork lost, so no separate best-chain rule is needed either for authoring or for serving state to applications"
 ],
 "answer": 2,
 "optNotes": [
  "與 GP 相反：那樣每塊都要等 finality，而 Grandpa 本來就落後最新 head 約 1–2 塊。",
  "§19 的 best chain 不是最長鏈，選的是 ticket 封印祖先數最多者，GP 也沒有 header hash tie-break。",
  "GP 明講 best block 就是 §19 best chain 的 head，用於出塊選 parent 與查最新狀態這類低延遲場合。",
  "「timeslot 不在未來」只是 block 暫時有效性的條件（§4.4、§5），不是 best block 的定義。",
 ],
 "explanation": "GP §4.6：「The simplest and least risky means… would be to inspect the Grandpa finality mechanism… However… Grandpa will typically return a block some small period older than the most recently authored block. (Existing deployments suggest around 1-2 blocks in the past…) There are often circumstances when we may wish to have less latency at the risk of the returned block not ultimately forming a part of the future canonical chain. E.g. we may be in a position of being able to author a block, and we need to decide what its parent should be. Alternatively, we may care to speculate about the most recent state… In these cases, we define the best block as the head of the best chain, itself defined in section 19.」§19 的 best block B♭ 必須：以 finalized block 為祖先、未 finalized 的部分沒有 equivocation（同一 timeslot 兩個有效 block）、已 audited；候選中選「使用 slot-sealer ticket（而非 fallback key）封印的祖先數最多」者，Grandpa 投票投的就是它（連同 posterior state root）。§4.3 另把 head 定義為「the block with the most ancestors」——finalized、best、head 是三個不同的概念。",
 "trap": "finalized（Grandpa，落後 1–2 塊、最安全）≠ best（§19 best chain 的 head，出塊/查詢用）≠ head（祖先最多）。"
},
]
