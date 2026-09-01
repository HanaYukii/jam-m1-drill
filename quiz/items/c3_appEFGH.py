# JAM M1 drill — appendices E (general Merklization / MMR), F (shuffle), G (Bandersnatch), H (erasure coding).
# Ground truth: GP 0.8.0 LaTeX — text/merklization.tex (§E), text/utilities.tex (§F),
# text/bandersnatch.tex (§G), text/erasure_coding.tex (§H), plus preamble.tex symbol table.

ITEMS = [

    # ---------------------------------------------------------------- appendix E
    {
        "id": "c3-appE-wb-vs-constant-depth",
        "ch": "E",
        "section": "E.1 Binary Merkle Trees & E.2 MMR",
        "gpRef": "eq. E.1 (N), E.3 (M_B), E.4 (M), E.7 (C); eq. 11.5 (segment-root a_e); §14 availability specifier (erasure-root a_u)",
        "difficulty": 3,
        "kind": "rationale",
        "tags": ["merklization", "segment-root", "erasure-root", "rationale"],
  "stemZh": "附錄 E 給了兩個通用 Merkle root 函數：well-balanced 的 M_B 與定深的 M。在 availability specification 中，segment-root a_e 用其中一個、erasure-root a_u 用另一個。是哪個配哪個？well-balanced 的形狀相對於「一律補到 2 的冪」又買到了什麼？",
  "optionsZh": [
   "segment-root 用 **M**：前處理器 C 把每一項改寫成 H('$leaf' ⌢ s) 並以零雜湊補到 2^⌈log₂ n⌉ 片葉子，讓所有葉子位於同一深度、使 64 葉子的頁面對 J_6／L_6 保持大小對齊。erasure-root 用 **M_B**，因為它的葉子本來就是 64 位元組的雜湊對、預先雜湊是浪費，而在 ⌈|v|/2⌉ 處切分能讓最深層——以及那一層的葉子數——維持最小",
   "剛好相反：segment-root 用 M_B，因為一個 segment 有 4,104 個 octet 而 M_B 避免了對每一項做雜湊；erasure-root 用 M，因為碎片數固定為 validator 集合大小、定深樹建起來比較便宜。M_B 在自己的基底情形套用 '$leaf' 前綴，所以不需要另外的前處理器，而 well-balanced 只有在項數很少、log₂ 取整會浪費一層時才有意義",
   "兩個 root 都用 M_B；定深函數只為附錄 D 的 state trie 而存在，因為它 31 位元組的 key 本來就固定了深度，而前處理器 C 就是那棵 trie 的 key 補齊步驟。偏好 well-balanced 是因為它讓每片葉子有相同的證明長度，而一旦項數本身不是 2 的冪，補到 2 的冪的樹就做不到這點，所以 J_6／L_6 是在那棵 trie 上分頁而不是在一般 Merkle 樹上",
   "兩個 root 都用 M；M_B 只是一層薄包裝，它處理單一項目的雜湊、其餘一律委派給節點函數 N。補到 2 的冪正是讓一棵樹變成 well-balanced 的做法，'$leaf' 與 '$node' 前綴是兩個 root 函數之間唯一實質的差別，而 erasure-root 的葉子是單一個 32 位元組的碎片雜湊而不是 64 位元組的對"
  ],
  "stem": "Appendix E gives two general Merkle root functions: the well-balanced M_B and the constant-depth M. In an availability specification the segment-root a_e is built with one of them and the erasure-root a_u with the other. Which way round is it, and what does the well-balanced shape buy over simply padding every tree up to a power of two?",
        "options": [
            "The segment-root uses M: the preprocessor C rewrites every item as H('$leaf' ⌢ s) and pads to 2^⌈log₂ n⌉ zero-hash leaves, so all leaves sit at one depth and 64-leaf pages stay size-aligned for J_6/L_6. The erasure-root uses M_B, whose leaves are already 64-octet hash pairs, so pre-hashing would be wasted and splitting at ⌈|v|/2⌉ keeps the deepest level — and the count of leaves on it — minimal.",
            "The other way round: the segment-root uses M_B because a segment is 4,104 octets and M_B avoids hashing each item, while the erasure-root uses M because the chunk count is fixed at the validator-set size, so a constant-depth tree is cheaper to build. M_B applies the '$leaf' prefix in its own base case, so no separate preprocessor is needed, and well-balancedness only matters for very short sequences where log₂ rounding wastes one level.",
            "Both roots use M_B; the constant-depth function exists only for the state trie of appendix D, whose 31-octet keys already fix the depth, and the preprocessor C is that trie's key-padding step. The well-balanced shape is preferred because it gives every leaf the same proof length, which a power-of-two-padded tree cannot do once the item count is not itself a power of two, so J_6/L_6 page over the trie rather than over a general Merkle tree.",
            "Both roots use M; M_B is only a thin wrapper that hashes a lone item and otherwise defers to the node function N. Padding up to a power of two is exactly what makes a tree well-balanced, the '$leaf' versus '$node' prefixes are the only substantive difference between the two root functions, and the erasure-root's leaves are single 32-octet chunk hashes rather than 64-octet pairs.",
        ],
        "answer": 0,
        "optNotes": [
          "eq. 11.5 明寫 segment-root 是 constant-depth、zero-hash-padded，而 erasure-root 的 leaf 本來就是 hash。",
          "與 eq. 11.5 原文相反，而且 M_B 的 base case 是 H(v_0)，並沒有 '$leaf' 前綴。",
          "附錄 D 的是 binary Patricia Merkle Trie、31-octet key 不經過 C；證明長度齊一的反而是定深樹。",
          "M_B 完全不 padding；well-balanced 指的是最深深度與該層 leaf 數皆最小，不是補到 2 的冪次。",
        ],
        "explanation": "GP 0.8.0 eq. 11.5 的說明文字寫得很白：segment-root a_e 是「a constant-depth, left-biased and zero-hash-padded binary Merkle tree committing to the hashes of each of the exported segments」，也就是 M（eq. E.4）＝ N(C(v,H),H)；C（eq. E.7）先把每個 item 換成 H('$leaf' ⌢ v_i)，再用 zero hash H_0 補到 2^⌈log₂ max(1,|v|)⌉。這兩件事缺一不可：先雜湊 leaf 才不會讓 justification 夾帶一整個 4,104-octet segment；補到 2 的冪次才會有 size-aligned 的 2^6 page，讓 eq. 14.12 的 paged-proofs 函數 P（GP 就叫 P，勿與 eq. 11.21 的 permute P 或 eq. 14.19 的 zero-pad 𝒫_n 混淆）能用 J_6/L_6 一次證明 64 個 segment。erasure-root a_u 走的是另一條路：§14 的 availability specifier 定義 a_u = M_B([⌢x | x ∈ ᵀ[b♣, s♣]])，每片 leaf 已經是「bundle chunk 的 Blake2b ⌢ 該 validator segment 欄的 M_B root」共 64 octets，再 pre-hash 一次純屬多做。GP 對 well-balanced 的定義是「ensures that the maximum depth of any leaf is minimal and that the number of leaves at that depth is also minimal」——注意這不等於「每片 leaf 的證明一樣長」：N 在 ⌈|v|/2⌉ 切，|v| = 5 時 index 0 的 trace 長 3、index 3 的長 2；長度齊一的是 constant-depth 那一種。",
        "trap": "口訣：segment-root 走「先 $leaf 再補 0」的定深樹（要分頁證明），erasure-root 走「不補不預雜湊」的均衡樹（leaf 本來就是 hash）。",
    },

    {
        "id": "c3-appE-code-trace-split",
        "ch": "E",
        "section": "E.1 Binary Merkle Trees & E.2 MMR",
        "gpRef": "eq. E.1 (N), E.2 (trace T), E.5–E.6 (J_x, L_x), E.7 (C); eq. 14.12 (paged proofs)",
        "difficulty": 3,
        "kind": "code",
        "tags": ["merklization", "justification", "proof-path", "bug"],
  "stemZh": "以下是團隊的 trace 函數，它產生的是納入佐證的兄弟節點。同一個檔案裡的節點函數 N 是用 `mid := (len(v) + 1) / 2` 切分輸入的。把兩者合起來看，缺陷是什麼？它又實際在哪裡咬人？",
  "optionsZh": [
   "照現況是沒問題的：對一棵 well-balanced 的樹而言，兩種取整慣例描述的是同一棵樹，因為 N 遞迴的正是這個函數所走訪的那些半邊。與 GP 唯一真正的分歧是順序——它回傳的序列是由葉子往上，而 GP 送出的是由 root 往下的另一組節點，所以在 CE 140 的呼叫點把 slice 反轉就是全部的修法",
   "遞迴下降的是**兄弟**那一半而不是含有目標索引的那一半，所以回傳的 co-path 是正確者的鏡像。長度總是與 GP 相符，這正是為什麼針對證明長度的單元測試會通過、而對照 root 的驗證卻失敗。分頁證明逃過一劫是因為 2 的冪的樹是對稱的，所以只有 CE 140 的 co-path 受影響",
   "它把切分**向下**取整，而 GP——以及這個檔案自己的節點函數——是**向上**取整，所以在任何長度為奇數的遞迴層上，兄弟節點乃至路徑長度都是錯的：三個項目、索引 0 時，GP 給出兩個節點而它只給一個。分頁證明逃過一劫是因為 C 已經先補到 2 的冪，但直接建構 CE 140 segment-shard co-path 的那次呼叫沒有",
   "它在把兄弟節點摺進路徑時漏掉了 '$node' 的 domain-separation 前綴，所以它回傳的雜湊無法被重新組合成 root；修法是在這個函數內部加上該前綴，而不是依賴節點函數去做。奇數長度的層不受影響，因為兩個函數的切分取整方式相同，而分頁證明失敗的頻率與直接呼叫完全一樣"
  ],
  "stem": "Below is the team's trace function, the one that produces the sibling nodes of an inclusion justification. In the same file the node function N splits its input with `mid := (len(v) + 1) / 2`. Reading the two together, what is the defect and where does it actually bite?",
        "code": {
            "lang": "go",
            "caption": "internal/utilities/merkle_tree/merkle_tree.go (T) — compare with N in the same file",
            "src": """func T(v []types.ByteSequence, i types.U32, hashFunc func(types.ByteSequence) types.OpaqueHash) (output []types.ByteSequence) {
	if len(v) <= 1 {
		return output
	}
	mid := types.U32(len(v) / 2)
	var siblingHalf []types.ByteSequence
	var traverseHalf []types.ByteSequence
	var newIndex types.U32

	if i < mid {
		siblingHalf = v[mid:]  // right is sibling
		traverseHalf = v[:mid] // go left
		newIndex = i
	} else {
		siblingHalf = v[:mid]  // left is sibling
		traverseHalf = v[mid:] // go right
		newIndex = i - mid
	}
	sibling := N(siblingHalf, hashFunc)
	suffix := T(traverseHalf, newIndex, hashFunc)
	result := make([]types.ByteSequence, 0, 1+len(suffix))
	result = append(result, sibling)
	result = append(result, suffix...)
	return result
}""",
        },
        "options": [
            "It is fine as written: for a well-balanced tree the two rounding conventions describe the same tree, because N recurses on the very halves this function walks. The only genuine divergence from the GP is ordering — the returned sequence runs from the leaf upwards, whereas the GP emits the opposite nodes from the root downwards, so reversing the slice at the CE 140 call site is the whole of the fix.",
            "The recursion descends into the sibling half rather than the half that contains the target index, so the returned co-path is the mirror image of the correct one. Lengths always match the GP's, which is why unit tests on proof length pass while verification against a root fails. Page proofs escape it because a power-of-two tree is symmetric, so only the CE 140 co-path is affected.",
            "It rounds the split down while the GP — and this file's own node function — round it up, so at any recursion level of odd length the siblings and even the path length are wrong: for three items at index 0 the GP yields two nodes and this yields one. Page proofs escape it because C has already padded to a power of two, but the direct call that builds the CE 140 segment-shard co-path does not.",
            "It omits the '$node' domain-separation prefix when folding a sibling into the path, so the hashes it returns cannot be recombined into the root; the fix is to prepend the prefix inside this function rather than relying on the node function to do it. Odd-length levels are unaffected, since both functions round the split the same way, and page proofs fail exactly as often as direct calls do.",
        ],
        "answer": 2,
        "optNotes": [
          "同檔的 N 用 ceil、T 用 floor，兩者根本不描述同一棵樹；順序則本來就由 root 往下，與 eq. E.2 一致。",
          "程式遞迴的是 traverseHalf 而不是兄弟半，而且長度就是會少一層，不是「長度永遠相符」。",
          "N 是 `(len(v)+1)/2`、T 是 `len(v)/2`；v = [a,b,c]、i = 0 時正解兩層、這份程式只回一層。",
          "'$node' 前綴由 N 自己加，T 只是收集 N 的輸出；兩個函式的取整方式也並不相同。",
        ],
        "explanation": "GP eq. E.1 的 N 在 ⌈|v|/2⌉ 切：N(v,H) = H('$node' ⌢ N(v_{…⌈|v|/2⌉},H) ⌢ N(v_{⌈|v|/2⌉…},H))；eq. E.2 的 trace T 用同一個 ⌈|v|/2⌉ 決定 P^⊤（含 i 的那半）與 P^⊥（兄弟那半）以及 P_I 的位移。程式裡 N 寫成 `(len(v)+1)/2` 是對的（ceil），但 T 寫成 `len(v)/2` 是 floor，兩者在長度為奇數時分岔。以 v = [a,b,c]、i = 0 為例：GP 的樹是 ((a,b),c)，正解 co-path 為 [N([c]), N([b])] 共兩層；這份程式取 mid = 1，兄弟半變成 [b,c]、只遞迴 [a]，回傳長度 1 的 [N([b,c])]，內容與長度全錯，proof 永遠對不回 root。為什麼平常沒炸：J_x（eq. E.5）先呼叫 C（eq. E.7）把序列補到 2 的冪次才丟給 T，之後每一層都是偶數，floor 與 ceil 相同，所以 work_package.go 走 eq. 14.12 的 paged-proofs P(s) 分頁證明沒事；真正踩雷的是 networking/handler/ce/ce140.go 的 constructMerkleCoPath，它把未補齊的 segment-shard 序列直接餵給 T。",
        "trap": "看到 Merkle 程式先問一句：ceil 還是 floor？GP 全篇一律 ⌈|v|/2⌉，只要 root 與 proof 用不同取整，偶數長度測資會全綠、奇數長度全紅。",
    },

    {
        "id": "c3-appE-mmb-peaks-superpeak",
        "ch": "E",
        "section": "E.1 Binary Merkle Trees & E.2 MMR",
        "gpRef": "eq. E.8 (A), E.9 (E_M), E.10 (M_R); eq. 7.3, 7.7–7.8; §18 Beefy Distribution",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["mmr", "mmb", "accumulation-log", "beefy"],
  "stemZh": "Accumulation Output Log β_B 是一個 optional 雜湊的序列而不是單一個 root，然而每筆近期歷史條目只儲存一個由它導出的 32 位元組值 b。為什麼狀態要保留整個 peak 序列？那個單一值又是拿來做什麼的？",
  "optionsZh": [
   "append 函數 A 像二進位加法一樣進位——被佔用的槽 n 會與進來的葉子摺疊並進位到槽 n+1，空槽 ∅ 則直接填入——但 peak 序列本身只是一個快取，因為節點需要證明時隨時可以從最近 H 筆近期歷史條目重建它；那個單一值是對各 peak 取的 Blake2b well-balanced root M_B，放在 β_H 裡純粹是讓輕客戶端不必重放 accumulation 就能檢查該 log，而 Beefy 簽的是 state root 而不是那個值",
   "append 函數 A 像二進位加法一樣進位——被佔用的槽會與進來的葉子摺疊並進位，空槽則直接填入——所以那些 peak 正是「繼續附加」以及「提供 O(log N) 納入證明」所需的全部狀態；把它們雜湊掉就等於終結可附加性，這正是為什麼另有一個 super-peak M_R（在 '$peak' 前綴之下對非 ∅ 的 peak 做左結合的 Keccak 摺疊）才是那個進入 β_H、並被 BLS 簽署供 Beefy 使用的 32 位元組值",
   "append 函數 A 每個區塊恰好推入一個新 peak，並在序列超過 H 項時丟掉最舊的，就像近期歷史的環狀緩衝區一樣，所以那些 peak 是一個有界窗口而不是持續成長的承諾，舊的產出就這樣自然失去可證明性；而儲存的那個單一值是編碼後 peak 序列 E_M(β_B) 的 Keccak 雜湊，它進入 β_H、被第三方當成橋接承諾並被 BLS 簽署",
   "append 函數 A 像二進位加法一樣進位，而保留那些 peak 是為了讓該 log 能在分叉時回捲，因為移除最後一片葉子永遠只需要丟掉一個 peak；那個單一值是對**那一個區塊**的 accumulation 產出所取的 well-balanced Keccak root，它進入 β_H 並被 BLS 簽署供 Beefy 使用，所以 peak 序列本身從不離開節點"
  ],
  "stem": "The Accumulation Output Log β_B is a sequence of optional hashes rather than a single root, yet every recent-history entry stores only one 32-octet value b derived from it. Why does state keep the whole peak sequence, and what is that single value used for?",
        "options": [
            "The append function A carries like binary addition — an occupied slot n is folded with the incoming leaf and carried into slot n+1, an empty slot ∅ is simply filled — but the peak sequence itself is only a cache, since a node can rebuild it from the last H recent-history entries whenever it needs a proof; the single value is the Blake2b well-balanced root M_B taken over the peaks, kept in β_H purely so light clients can check the log without replaying accumulation, and Beefy signs the state root rather than that value.",
            "The append function A carries like binary addition — an occupied slot n is folded with the incoming leaf and carried into slot n+1, an empty slot ∅ is simply filled — so the peaks are exactly the state needed to keep appending and to serve O(log N) inclusion proofs; hashing them away would end appendability, which is why the separate super-peak M_R (a left-associated Keccak fold over the non-∅ peaks under a '$peak' prefix) is the one 32-octet value that enters β_H and is BLS-signed for Beefy.",
            "The append function A pushes exactly one new peak per block and drops the oldest once the sequence exceeds H entries, exactly like the recent-history ring buffer, so the peaks are a bounded window rather than a growing commitment and old outputs simply age out of provability; the single stored value is the Keccak hash of the encoded peak sequence E_M(β_B), which enters β_H and is what third parties treat as the bridging commitment and BLS-sign for Beefy.",
            "The append function A carries like binary addition — an occupied slot n is folded with the incoming leaf and carried into slot n+1, an empty slot ∅ is simply filled — and the peaks are kept so that the log can be rewound on a fork, since removing the last leaf only ever requires dropping one peak; the single value is the well-balanced Keccak root over the accumulation outputs of that one block, which is what enters β_H and is BLS-signed for Beefy, so the peak sequence itself never leaves the node.",
        ],
        "answer": 1,
        "optNotes": [
          "β_H 每筆只留 super-peak 而且只有 H 筆，重建不出整條 belt；進 β_H 的也是 Keccak 的 M_R 而非 M_B。",
          "GP 明寫雜湊掉 peaks 就不能再 append，所以 state 留 peaks、對外只公布 super-peak M_R。",
          "A 的動作是進位而非推入，peak 數只隨 log₂N 成長且從不淘汰；E_M 是 C(3) 的 codec、根本不雜湊。",
          "一次 append 可能連鎖進位好幾格；那顆 root 是被 append 進去的 leaf，不是 eq. 7.8 存下的 M_R(β′_B)。",
        ],
        "explanation": "GP 附錄 E 的 MMR/MMB 段落：「a sequence of peaks, each peak the root of a Merkle tree containing 2^i items where i is the index in the sequence」，且「some peaks may be empty, ∅ rather than a Merkle root」。eq. E.8 的 A(r,l,H) = P(r,l,0,H) 就是二進位加法的進位：n ≥ |r| 時把 l 接在尾端；r_n = ∅ 時直接填入；否則把 r_n 清成 ∅、把 H(r_n ⌢ l) 當新的 leaf 進位到 n+1。GP 也明講「Hashing them removes the possibility of further appending so the range itself is kept on the system which needs to generate future proofs」——這就是 state 存 peaks 而不是存單一 root 的理由，也是 MMR 與一般 Merkle root 的根本差別。eq. 7.7：β′_B ≡ A(β_B, M_B(s, keccak), keccak)，每個 block 只 append 一片 leaf（該 block accumulation output 的 well-balanced root，且明講「Throughout, the Keccak hash function is used to maximize compatibility with legacy systems」）。eq. 7.8 存進 β_H 的欄位是 b = M_R(β′_B)，而 eq. E.10 的 M_R 先濾掉 ∅、空則 H_0、單一則直接回傳，否則 keccak('$peak' ⌢ M_R(h_{…|h|−1}) ⌢ h_{|h|−1})——注意 M_R 是寫死 Keccak，不像 A（eq. E.8）收 H 參數；E_M（eq. E.9）則根本不雜湊，它只是給 state serialization C(3) 用的 codec 𝓔_M。§18 Beefy 就是對 X_B ⌢ last(β_H)_b 做 BLS 簽章，所以 super-peak 才是對外橋接的那顆 commitment。",
        "trap": "MMR 與單一 Merkle root 的差別＝「還能不能再 append」。peaks 留著才能 append 與出證明；對外公布的是 super-peak（Keccak、'$peak'）。",
    },

    # ---------------------------------------------------------------- appendix F
    {
        "id": "c3-appF-shuffle-is-consensus",
        "ch": "F",
        "section": "F Shuffling (Fisher–Yates)",
        "gpRef": "eq. F.1 (F); eq. 11.21 (guarantor permute P); §17 tranche-0 audit selection",
        "difficulty": 2,
        "kind": "rationale",
        "tags": ["shuffle", "determinism", "guarantor-assignment", "rationale"],
  "stemZh": "團隊裡有位審閱者想把洗牌函數 F 中的 `r_0 mod l` 索引選取換成拒絕取樣，理由是只要 l 不整除 2³²，對 32 位元抽樣取模就有偏差。團隊該怎麼回應？",
  "optionsZh": [
   "拒絕這個更動。F 是一條**共識規則**而不是統計工具：每個節點都必須從相同的熵導出完全相同的排列，而它的輸出驅動 guarantor 對 core 的指派 P(|κ′|, η′_2, τ′) 以及 tranche-0 的稽核抽選。一個去偏的節點會把 validator 指派到不同的 core，接著拒絕完全有效的 guarantor 簽章並使鏈分裂；32 位元抽樣的殘餘偏差是被刻意接受的",
   "接受這個更動。Gray Paper 只固定了**分布**——任何能對輸入產生均勻隨機排列的洗牌都是合規的——而 jamtestvectors 的 shuffle 套件也只檢查結果是輸入的一個排列、不檢查是哪一個排列。反正 F 餵給的東西鏈上都不檢查：guarantor 對 core 的指派是由每份 work-report 自己攜帶的 core 索引固定的，而 tranche-0 的稽核純粹是本地選擇",
   "這個更動是多餘而非錯誤：numeric-sequence-from-hash 函數已經藉由從 Blake2b 摘要中切出互不重疊的 4 octet 窗口去除了偏差，所以那個值對剩餘長度取模恰好是均勻的、拒絕取樣會迴圈零次。因此兩種形式逐位元相符，切換過去的節點仍然導出與其他人相同的指派",
   "接受，但只用在 ticket 的處理上。附錄 F 的洗牌是用來排序 ticket accumulator γ_A、以及 §6 用來建構 fallback 金鑰序列的，而既然 γ_A 在使用前會依識別碼重新排序，那個排列從不進入狀態；guarantor 那條路徑與 tranche-0 的稽核抽選則必須維持 Gray Paper 有偏差的形式，因為那兩者確實進入狀態"
  ],
  "stem": "A reviewer on the team wants to replace the `r_0 mod l` index selection in the shuffle F with rejection sampling, on the grounds that a modulo of a 32-bit draw is biased whenever l does not divide 2³². How should the team answer?",
        "options": [
            "Reject the change. F is a consensus rule, not a statistics utility: every node must derive the identical permutation from the same entropy, and its output drives the guarantor-to-core assignment P(|κ′|, η′_2, τ′) and the tranche-0 audit selection. A node that de-biases assigns validators to different cores, then rejects perfectly valid guarantor signatures and splits the chain; the residual bias across 32-bit draws is deliberately accepted.",
            "Accept the change. The Gray Paper fixes only the distribution — any shuffle that yields a uniformly random permutation of the input is conformant — and the jamtestvectors shuffle suite checks only that the result is a permutation of the input, not which permutation. F feeds nothing that is checked on chain anyway: the guarantor-to-core assignment is fixed by the core index each work-report carries, and tranche-0 auditing is a purely local choice.",
            "The change is unnecessary rather than wrong: the numeric-sequence-from-hash function already removes the bias by slicing non-overlapping 4-octet windows out of a Blake2b digest, so the value taken modulo the remaining length is exactly uniform and rejection sampling would loop zero times. The two forms therefore agree bit for bit, and a node that switches still derives the same assignment P(|κ′|, η′_2, τ′) as everyone else.",
            "Accept it, but only for ticket handling. The appendix-F shuffle is what orders the ticket accumulator γ_A and what §6 calls on to build the fallback key sequence, and since γ_A is re-sorted by identifier before use the permutation never reaches state; the guarantor path and the tranche-0 audit selection must keep the Gray Paper's biased form, because those two do reach state.",
        ],
        "answer": 0,
        "optNotes": [
          "F 是共識規則而非統計工具：它的輸出決定 eq. 11.21 的 P 與 §17 的 tranche-0，改了就分叉。",
          "GP 給的是逐步可重現的函數定義，jamtestvectors 的 shuffle 向量是逐一比對輸出序列本身。",
          "Q_l（eq. F.2）只是把 hash 展開成 32-bit 數列，取模時的偏差原封不動保留下來。",
          "γ_A 依 identifier y 排序取最小的 E 個，從未呼叫 F；§6 那個 fallback 是另一個同名函數。",
        ],
        "explanation": "eq. F.1 定義 F(s,r)：每一步取 index = r_0 mod l，輸出 s_{r_0 mod l}，再把 s_{l−1} 搬進那個位置、序列縮短一格遞迴。這裡的 mod 確實有 modulo bias（r_i ∈ N_{2³²}，l 通常不整除 2³²），GP 明知而不改，因為它要的不是統計上的完美均勻，而是「所有節點算出同一個排列」。用到的地方是硬性共識：eq. 11.21 的 P(v,e,t) = R(F([⌊i/3⌋ | i ∈ N_v], e), ⌊(t mod E)/R⌋) 決定每個 validator 這一輪被指派到哪個 core，η′_2 當種子（GP 特別說用 η_2 而非 η_1 是為了避開 fork-magnification）；另一處是 §17 的 tranche-0：F(reports, Y(s_0))[..10]。只要有節點改了 F，它算出的 M（eq. 11.22 的 guarantor assignments）就不同，於是把別人合法的 guarantor 簽章判成 bad validator index／unsorted guarantors，直接分叉。規範函數的價值在 bit-exact 可重現，不在統計品質，這是面試常考的判斷題。",
        "trap": "面試常問「這個 shuffle 有 bias 你要不要修？」——答案永遠是不修：規範函數的價值在於 bit-exact 可重現，不在於統計品質。",
    },

    {
        "id": "c3-appF-seq-from-hash-vs-fallback",
        "ch": "F",
        "section": "F Shuffling (Fisher–Yates)",
        "gpRef": "eq. F.2 (Q_l), F.3 (F from a hash); eq. 6.27 (fallback key sequence)",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["shuffle", "entropy", "safrole", "fallback"],
  "stemZh": "Gray Paper 有兩處把一個 32 位元組的雜湊展開成一串索引：餵給洗牌的 numeric-sequence-from-hash 函數，以及 §6 在 ticket accumulator 未滿時挑選一整個 epoch 份 Bandersnatch 金鑰的 fallback 金鑰序列函數。這兩種展開實際上差在哪裡？",
  "optionsZh": [
   "它們是同一個構造被用了兩次：§6 的 fallback 序列字面上就是把附錄 F 的洗牌套用在 active 金鑰集合 κ′ 上、以 η′_2 為種子、再截斷到 E 項，所以兩者都是每八個輸出做一次 Blake2b（對種子串接 ⌊i/8⌋ 的 4 位元組編碼）、都解碼位於偏移 4i mod 32 的 little-endian 窗口、也都以循環方式索引金鑰序列——這正是為什麼實作只需要一套雜湊展開常式",
   "洗牌的展開是每**八個**輸出做一次 Blake2b——雜湊的是種子串接 ⌊i/8⌋ 的 4 位元組編碼——並解碼位於偏移 4i mod 32 的 little-endian 4 位元組窗口，所以一個 32 位元組摘要供應八個連續的 32 位元數字。而 §6 的 fallback 是**每個時槽**雜湊一次，對象是種子串接該時槽索引的編碼，並且只解碼開頭的 4 個 octet，再用結果以循環方式索引金鑰序列",
   "剛好相反：洗牌的展開是每個輸出雜湊一次（對種子串接 i 的 4 位元組編碼）並取每個摘要的前四個 octet；而 §6 的 fallback 是每八個時槽做一次 Blake2b（雜湊種子與 ⌊i/8⌋ 的編碼）並解碼偏移 4i mod 32 的 little-endian 窗口，這正是讓整個 epoch 的 fallback 金鑰能一次算得很便宜的原因",
   "兩者都是每個輸出雜湊一次（對種子串接該索引的 4 位元組編碼）、也都只取每個摘要的前四個 octet；差別在洗牌接著以 big-endian 解碼並直接使用其自然範圍內的值，而 §6 的 fallback 以 little-endian 解碼並對金鑰序列長度取模，所以位元組序是唯一真正的差異，也是 fallback seal 不符的經典來源"
  ],
  "stem": "Two places in the Gray Paper expand a 32-octet hash into a sequence of indices: the numeric-sequence-from-hash function that feeds the shuffle, and the fallback key-sequence function of §6 that picks an epoch's worth of Bandersnatch keys when the ticket accumulator is not full. How do the two expansions actually differ?",
        "options": [
            "They are the same construction used twice: §6's fallback sequence is literally the appendix-F shuffle applied to the active key set κ′ with η′_2 as the seed and then truncated to E entries, so both make one Blake2b call per eight outputs over the seed concatenated with the 4-octet encoding of ⌊i/8⌋, both decode the little-endian window at offset 4i mod 32, and both index the key sequence cyclically — which is why an implementation only needs one hash-expansion routine.",
            "The shuffle's expansion makes one Blake2b call per eight outputs — hashing the seed concatenated with the 4-octet encoding of ⌊i/8⌋ — and decodes the little-endian 4-octet window at offset 4i mod 32, so one 32-octet digest supplies eight consecutive 32-bit numbers. §6's fallback hashes once per slot, over the seed concatenated with the encoding of the slot index, and decodes only the leading 4 octets, using the result to index the key sequence cyclically.",
            "It is the other way round: the shuffle's expansion hashes once per output, over the seed concatenated with the 4-octet encoding of i, and takes the leading four octets of each digest; §6's fallback makes one Blake2b call per eight slots — hashing the seed with the encoding of ⌊i/8⌋ — and decodes the little-endian window at offset 4i mod 32, which is what keeps a whole epoch of fallback keys cheap to compute at once.",
            "Both hash once per output, over the seed concatenated with the 4-octet encoding of the index, and both take only the leading four octets of each digest; the shuffle then decodes big-endian and uses the value in its natural range while §6's fallback decodes little-endian and reduces modulo the key-sequence length, so endianness is the only real difference and is the classic source of fallback-seal mismatches.",
        ],
        "answer": 1,
        "optNotes": [
          "eq. 6.27 寫的是 H(r ⌢ E_4(i)) 逐 slot 一次、只取 _{…4}，規格與 Q_l 並不相同。",
          "Q_l 的 counter 是 ⌊i/8⌋、window 取 4i mod 32；eq. 6.27 逐 slot 一次 hash、取前 4 octets 再做 cyclic index。",
          "把兩邊的批次方式對調了：八個一批的是 Q_l，逐 slot 一次的才是 fallback key sequence。",
          "𝓔⁻¹_4 兩邊都是 little-endian，GP 從未定義 big-endian 解碼；Q_l 取的也不是固定前四個 octet。",
        ],
        "explanation": "eq. F.2：Q_l(h) = [ 𝓔⁻¹_4( H(h ⌢ E_4(⌊i/8⌋))_{4i mod 32 …+4} ) | i ∈ N_l ]。注意兩個細節：counter 是 ⌊i/8⌋，所以每八個輸出才換一次 Blake2b；取的是 offset 4i mod 32 起算的 4 octets，剛好把 32-octet digest 切成八個互不重疊的 window，再以 𝓔⁻¹_4（little-endian，見 §3 對 E_l/𝓔⁻¹_l 的約定；別和 eq. H.1 的 shard 數函數 𝒟 混用同一個字母）解成 32-bit 數。eq. F.3 則把它接到 shuffle 上：F(s,h) ≡ F(s, Q_{|s|}(h))，數列長度恰好等於序列長度。§6 的 fallback key sequence（eq. 6.27）長得像但不是同一個：F(r,k) = [ k[𝓔⁻¹_4(H(r ⌢ E_4(i))_{…4})]_b ⟳ | i ∈ N_E ]——每個 slot 各做一次 hash，只取前 4 octets，而且是對 k 取 cyclic index（⟳），輸出是 Bandersnatch 公鑰而不是數字。把兩者當成同一個函數，是實作 safrole fallback 時最典型的錯法：γ′_S 只有落到 eq. 6.25 第三支時（跨 epoch 而 Z(γ_A) 的條件不成立，例如 |γ_A| ≠ E 或 m < Y）才等於 eq. 6.27 的結果（那是逐 slot 抽 k 的 fallback，不是把 κ′ 拿去 shuffle）；同一 epoch 內（e′ = e）γ′_S 一律沿用 γ_S。",
        "trap": "§6 的 fallback 叫 F、附錄 F 的 shuffle 也叫 𝓕——同名不同物。fallback 一個 slot 一次 hash、取前 4 bytes；Q_l 一次 hash 供八個、取 4i mod 32 的 window。",
    },

    # ---------------------------------------------------------------- appendix G
    {
        "id": "c3-appG-why-ring-not-plain-vrf",
        "ch": "G",
        "section": "G Bandersnatch VRF (IETF VRF vs Ring VRF)",
        "gpRef": "§G; §3 signing schemes; eq. 6.30 (tickets extrinsic), eq. 6.16 (ticket seal)",
        "difficulty": 1,
        "kind": "rationale",
        "tags": ["bandersnatch", "ring-vrf", "safrole", "anonymity", "rationale"],
  "stemZh": "Safrole 本來可以用一般的 IETF VRF 簽章加上提交者已公開的 Bandersnatch 金鑰來證明 ticket 有效。為什麼 Gray Paper 堅持改用 ring VRF 證明？",
  "optionsZh": [
   "因為 ring VRF 的輸出不可偏置，而一般 VRF 的輸出可被簽署者靠重複提交來輾磨，所以只有 ring 形式才能讓下個 epoch 的 slot-sealer 序列安全公開；匿名只是樂見的副作用而非理由，而抗輾磨也正是 ticket 的訊息為空、其 context 不帶 entry index 的原因",
   "因為一份 ring 證明可以一次涵蓋某位 validator 的所有 ticket 項目——entry index 搭在訊息裡、而 context 只固定 η′_2——所以 784 個 octet 的成本每位 validator 每個 epoch 只付一次，而不論每人被允許幾個項目，tickets extrinsic 都能待在每塊 16 個的上限之內",
   "因為那份證明只顯示它的作者知道某個私鑰、其公鑰落在 γ′_Z 所承諾的 ring 之中，卻從不顯示是哪一個，所以下個 epoch 的 slot-sealer 序列可以放在公開狀態裡而不洩漏誰將在哪一槽出塊；作者只有在 seal 出現時才被識別，這正是鈍化針對性阻斷服務與賄賂的機制",
   "因為它讓任何持有金鑰的人（不論是不是 validator）都能參加 ticket 競賽——證明是對照 144 位元組的 γ′_Z 檢查的，但並不要求 ring 成員資格、只要求知道某個 Bandersnatch 私鑰——這正是在部分 validator 離線時仍能讓 accumulator 保持飽和的機制，也是競賽在該 epoch 第 500 槽關閉的原因"
  ],
  "stem": "Safrole could have proved ticket validity with an ordinary IETF VRF signature plus the submitting validator's published Bandersnatch key. Why does the Gray Paper insist on a ring VRF proof instead?",
        "options": [
            "Because a ring VRF output is unbiasable whereas a plain VRF output can be ground by its signer through resubmission, so only the ring form makes next epoch's slot-sealer sequence safe to publish; anonymity is a welcome side effect but not the reason, and grinding resistance is also why the ticket's message is empty and its context carries no entry index.",
            "Because one ring proof can carry all of a validator's ticket entries at once — the entry indices ride in the message while the context fixes only η′_2 — so the 784-octet cost is paid once per validator per epoch and the tickets extrinsic stays inside its 16-per-block cap however many entries each validator is allowed.",
            "Because the proof shows only that its author knows a secret whose public key lies in the ring committed by γ′_Z, never which one, so next epoch's slot-sealer sequence can sit in public state without revealing who will author which slot; the author is identified only when the seal appears, which is what blunts targeted denial-of-service and bribery.",
            "Because it lets any key holder, validator or not, enter the ticket contest — the proof is checked against the 144-octet γ′_Z but ring membership is not required, only knowledge of some Bandersnatch secret — which is what keeps the accumulator saturated when part of the validator set is offline, and is why the contest closes at slot 500 of the epoch.",
        ],
        "answer": 2,
        "optNotes": [
          "兩種簽章都是 VRF，output 的不可操縱性來自 input 綁死 η′_2；eq. 6.30 的 context 也確實帶著 i_e。",
          "每個 entry index 各自一張 784-octet proof；16 限的是每個 block 的 ticket 筆數而非每人一張。",
          "§3 說得最白：兩者的差別就在「member is identified in the former and is anonymous in the latter」。",
          "ring proof 恰恰只有 ring 成員產得出來；Y = 500 收單是 C_epochtailstart 的規定，與參賽資格無關。",
        ],
        "explanation": "§3 的簽章章節把差別講得最清楚：「Both the Bandersnatch signature and RingVRF proof strictly imply that a member utilized their secret key in combination with both the context x and the message m; the difference is that the member is identified in the former and is anonymous in the latter.」而 ring root 那段又說「A root implies a specific sequence of Bandersnatch key pairs, knowledge of one of the secrets would imply being capable of making a unique, valid—and anonymous—proof of knowledge of a unique secret within the sequence.」eq. 6.30 的 ticket proof 屬於 ⟨γ′_Z, X_T ⌢ η′_2 ⌢ i_e, []⟩ 這一族 784-octet ring proof，驗證只看 144-octet 的 ring root，因此鏈上永遠不知道某張 ticket 是誰投的；到了下一個 epoch 該 slot 的作者才用 eq. 6.16 的 96-octet IETF 簽章現身。（以下為 Sassafras/Safrole 的公認設計動機，GP 0.8.0 本文只寫到 anonymity，未展開攻擊模型）這正是 Safrole 相對 BABE 的賣點：未來的出塊者名單公開、身分不公開，攻擊者無法提前針對某台機器打 DoS 或行賄。",
        "trap": "GP 0.8.0 只把 anonymity 寫成理由：ring proof 證明的是「簽章者在 γ′_Z 這個 ring 之中」而不指名是誰；unbiasability 兩種 VRF 都有，拿它當選 ring VRF 的理由必錯。",
    },

    {
        "id": "c3-appG-ring-root-commitment",
        "ch": "G",
        "section": "G Bandersnatch VRF (IETF VRF vs Ring VRF)",
        "gpRef": "§G (ring root O, padding point); eq. 6.14–6.15 (key rotation and Φ); eq. 6.4 (γ_Z)",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["bandersnatch", "ring-vrf", "ring-root", "offenders"],
  "stemZh": "epoch root γ′_Z 究竟承諾了什麼？而某位 validator 因其 Ed25519 金鑰落在 offenders 集合中、金鑰元組被 Φ 歸零之後，會怎麼樣？",
  "optionsZh": [
   "它承諾的是 **pending** 金鑰集合（也就是接下來那個 epoch 的 validator）依序排列的 Bandersnatch 成分，是一個在 epoch 邊界重算的定長 144 位元組承諾。一個全零的項目不是合法的曲線點，所以會用 Bandersnatch 的 padding 點代入它：ring 維持原本大小、其他每個成員保住自己的索引，而那個位置永遠產不出任何證明",
   "它承諾的是 **active** 金鑰集合 κ′（也就是當前 epoch 的 validator）依序排列的 Bandersnatch 成分，是一個在 offenders 集合改變時就重算的定長 144 位元組承諾。被歸零的項目會被丟棄、倖存金鑰重新編號，所以 ring 會依 offender 數量縮小，而 root 與證明也相應變便宜",
   "它是對 pending 金鑰集合依序排列之 32 位元組 Bandersnatch 成分所取的 well-balanced Merkle root M_B，因此它本身就是 32 個 octet，在 epoch 邊界重算。被歸零的項目就成為一片沒有人知道其開啟方式的葉子：ring 維持大小、其他成員保住索引，而這正是把 offender 排除在競賽之外的機制",
   "它承諾的是 pending 集合**完整 336 位元組**的 validator 金鑰元組——Bandersnatch、Ed25519、BLS 與 metadata 一併——是一個在 epoch 邊界重算的定長 144 位元組承諾。既然 Φ 只歸零 Ed25519 那個成分，Bandersnatch 那一半仍然存活並保住索引，所以 offender 在下一次輪替把它移除之前仍能提交 ticket"
  ],
  "stem": "What exactly does the epoch root γ′_Z commit to, and what becomes of a validator whose key tuple has been zeroed by Φ because its Ed25519 key is in the offenders set?",
        "options": [
            "It commits to the ordered Bandersnatch components of the pending key set — the validators of the coming epoch — as a fixed 144-octet commitment recomputed at the epoch boundary. An all-zero entry is not a valid curve point, so the Bandersnatch padding point is substituted for it: the ring keeps its size, every other member keeps its index, and no proof can ever be produced for that position.",
            "It commits to the ordered Bandersnatch components of the active key set κ′ — the validators of the current epoch — as a fixed 144-octet commitment recomputed whenever the offenders set changes. Zeroed entries are dropped and the surviving keys re-indexed, so the ring shrinks by the number of offenders and both the root and the proofs get correspondingly cheaper.",
            "It is the well-balanced Merkle root M_B over the ordered 32-octet Bandersnatch components of the pending key set and is therefore itself 32 octets, recomputed at the epoch boundary. A zeroed entry simply becomes a leaf whose opening nobody knows: the ring keeps its size, every other member keeps its index, and that is what excludes the offender from the contest.",
            "It commits to the full 336-octet validator key tuples of the pending set — Bandersnatch, Ed25519, BLS and metadata alike — as a fixed 144-octet commitment recomputed at the epoch boundary. Since Φ zeroes only the Ed25519 component the Bandersnatch half survives and keeps its index, so an offender can still submit tickets until the next rotation removes it.",
        ],
        "answer": 0,
        "optNotes": [
          "eq. 6.14 的 z = O([k_b | k ∈ γ′_P]) 承諾的是 pending set，而全零鍵以 padding point 補位、索引不變。",
          "承諾的是 pending set 且只在 epoch 邊界重算；proof 恆 784 octets、root 恆 144，不會因 ring 變小而變便宜。",
          "O(s) ≡ commit(s) 是多項式承諾而非 Merkle root，definitions 也寫明 ringroot ⊂ B_144。",
          "z 只取 32-octet 的 Bandersnatch 分量，而 eq. 6.15 的 Φ 是把整條 tuple 換成 [0, 0, …]。",
        ],
        "explanation": "eq. 6.14 的 key rotation 在 e′ > e 時把 (γ′_P, κ′, λ′, γ′_Z) 設成 (Φ(ι), γ_P, κ, z)，其中 z = O([k_b | k ∈ γ′_P])——所以 ring root 承諾的是 pending set γ′_P（下一個 epoch 才上線的那組）的 Bandersnatch 分量。§G 的 O(s) ≡ commit(s)，而 §3 與 definitions 都寫明 ringroot ⊂ B_144（B_144 是 blob 集合 𝔹 的 144-octet 子集；別寫成 𝕐_144，𝕐 是 eq. 11.5 的 avspec 集合），是固定 144 octets、與 ring 大小無關的 commitment。eq. 6.15 的 Φ(k) 在 k_e ∈ ψ′_O 時把「整個」key tuple 換成 [0,0,…]，不是只清 Ed25519 那 32 octets。§G 結尾那句就是為這種情況準備的：「Note that in the case a key k̃ has no corresponding Bandersnatch point when constructing the ring, then the Bandersnatch padding point as stated by Hosseini–Galassi should be substituted.」——用 padding point 補位而不是把它刪掉，ring 長度與每個成員的索引都不變，只是那個位置沒有人握有對應私鑰，因此永遠生不出合法 proof。若真的把零鍵刪掉再重新編號，所有人的 ring 成員位置都會位移，跨實作的 root 也就對不起來，這是 ring verifier 快取常見的災難（團隊 #1040/#1041 就是把 verifier 從「以 epoch 為 key」改成「以 validator-set hash 為 key」）。",
        "trap": "三個字要記牢：pending（不是 active）、144 octets（不是 32）、padding point（不是刪除）。",
    },

    {
        "id": "c3-appG-output-vs-signature",
        "ch": "G",
        "section": "G Bandersnatch VRF (IETF VRF vs Ring VRF)",
        "gpRef": "§G (Y as output(·)‥32); §3 signing schemes; eq. 6.6 (ticket), 6.16 (ticket seal), 6.30 (tickets extrinsic)",
        "difficulty": 3,
        "kind": "concept",
        "tags": ["bandersnatch", "vrf-output", "ticket-identifier", "safrole"],
  "stemZh": "ticket accumulator 只保留「32 位元組識別碼 + entry index」的元組；extrinsic 中那份 784 位元組的 ring 證明一經驗證就被丟棄。一個 epoch 之後，某一槽的封印者必須出示一個 96 位元組的簽章，其輸出要等於當初儲存的那個識別碼——即使它現在簽的是序列化後的未簽署 header 而不是空訊息。是什麼讓這件事成為可能？",
  "optionsZh": [
   "因為儲存的識別碼是那份 ring 證明的 Blake2b 雜湊，而 Bandersnatch 的 ring 證明是確定性的，所以同一把金鑰與 context 會重現完全相同的證明位元組、因而重現相同的雜湊；訊息在那個雜湊裡完全不起作用。ticket 的 context 是 ticket-seal 字串加 η′_2 與 entry index，seal 的則是同一個字串加 η′_3，而熵的輪替讓那兩串位元組在一個 epoch 之後相等",
   "因為 seal 把儲存的 ring 證明重新發布在 seal 欄位裡——96 位元組的形式就是那同一份證明剝掉零知識部分後的樣子，這正是兩種大小不同的原因——所以不論簽的是什麼，它的輸出理所當然不變。context 確實會在 epoch 邊界從 η′_2 移到 η′_3，但被剝除過的證明會把它原本的輸出一併帶著走，所以儲存的識別碼仍然吻合",
   "因為 VRF 的輸出是一個受 context 影響、但**不受訊息影響**的高熵雜湊，只由私鑰與輸入決定。ticket 的 context 是 ticket-seal 字串加 η′_2 與 entry index；seal 的則是同一個字串加 η′_3 與該 ticket 的 entry index，而熵的輪替讓那兩串位元組在一個 epoch 之後相等，所以同一把金鑰在兩種簽章型別之下都產出相同的 32 個 octet",
   "因為識別碼只由 η′_2 連同 entry index 導出，所以每位 validator 不必看過證明就能重算每一個 ticket 識別碼；簽章只提供「有權使用它」的證明，這也是為什麼證明本身不必保留。一個 epoch 之後 seal 在 η′_3 之下簽署，但既然識別碼從不依賴任何私鑰，封印者只需要出示相同的 entry index"
  ],
  "stem": "The ticket accumulator keeps only tuples of a 32-octet identifier and an entry index; the 784-octet ring proof from the extrinsic is thrown away once verified. An epoch later the sealer of a slot must present a 96-octet signature whose output equals that stored identifier, even though it now signs the serialized unsigned header rather than an empty message. What makes that possible?",
        "options": [
            "Because the stored identifier is the Blake2b hash of the ring proof, and a Bandersnatch ring proof is deterministic, so the same key and context regenerate the identical proof bytes and hence the identical hash; the message plays no part in that hash. The ticket's context is the ticket-seal string with η′_2 and the entry index, the seal's is the same string with η′_3, and the entropy rotation makes those two byte strings equal one epoch later.",
            "Because the seal republishes the stored ring proof inside the seal field — the 96-octet form is that same proof with the zero-knowledge portion stripped, which is exactly why the two sizes differ — so its output is trivially unchanged no matter what is signed. The context does move from η′_2 to η′_3 across the epoch boundary, but a stripped proof carries its original output along with it, so the stored identifier still matches.",
            "Because a VRF output is a high-entropy hash influenced by the context but not by the message, fixed by the secret key and the input alone. The ticket's context is the ticket-seal string with η′_2 and the entry index; the seal's is the same string with η′_3 and the ticket's entry index, and the entropy rotation makes those two byte strings equal one epoch later, so the same key yields the same 32 octets under either signature type.",
            "Because the identifier is derived from η′_2 together with the entry index alone, so every validator can recompute every ticket identifier without ever seeing the proof; the signature contributes only the proof of the right to use it, which is why the proof itself need not be retained. One epoch later the seal signs under η′_3, but since the identifier never depended on a secret key, the sealer need only exhibit the same entry index.",
        ],
        "answer": 2,
        "optNotes": [
          "96-octet IETF 簽章與 784-octet ring proof 是兩種位元串，雜湊不可能相同；Y(s) 取的是 VRF output 本身。",
          "eq. 6.16 的 H_S 是重新產生的 96-octet IETF 簽章，不是舊 ring proof 剝掉某部分之後的片段。",
          "§3 明說 VRF output「influenced by x but not by m」，而 entropy 輪轉讓投票時的 η′_2 正是一個 epoch 後的 η′_3。",
          "那樣 ticket 就毫無私鑰綁定、人人可奪 slot；eq. 6.16 要求 i_y = Y(H_S)，H_S 必須由 H_A 這把私鑰簽出。",
        ],
        "explanation": "§3 的關鍵句：「both define a VRF output, a high entropy hash influenced by x but not by m」，§G 則寫 Y(s) ≡ output(x | x ∈ ⟨…⟩)‥32，也就是取 VRF output 的前 32 octets。§6 定義新 ticket 為 n = [(y ← Y(i_p), e ← i_e) | i ∈ E_T]，γ_A 依 y 排序取最小的 E 個，全程沒有保留 784-octet 的 proof。到了下一個 epoch，eq. 6.16 要求 i_y = Y(H_S) 且 H_S ∈ ⟨H_A, X_T ⌢ η′_3 ⌢ i_e, E_U(H)⟩。兩邊 context 之所以逐 byte 相同，是因為 entropy 每個 epoch 輪轉 (η′_1, η′_2, η′_3) ← (η_0, η_1, η_2)：投票當下的 η′_2，正是一個 epoch 後的 η′_3；entry index 也一路帶著。message 一邊是空序列、一邊是 E_U(H)，但 message 不影響 output，所以同一把私鑰照樣算出同一個 y。這也解釋了為什麼「ticket 不能被搬到別的 epoch」：換 epoch 就換 η，context 一變 y 就變，舊 y 進不了新的 γ_A；順帶一提 ticket 跟 core 完全無關，validator→core 是 eq. 11.21 的 shuffle 在管，別把兩者混談。",
        "trap": "先分清楚兩個東西：signature／proof 是「可丟的憑證」，Y(·) 的 VRF output 才是「進 state 的身分」。output 綁 key＋context，不綁 message。",
    },

    # ---------------------------------------------------------------- appendix H
    {
        "id": "c3-appH-code-shardcount-080",
        "ch": "H",
        "section": "H Erasure Coding",
        "gpRef": "eq. H.1 (𝒟); eq. 6.8 (𝕍); eq. 11.5 (a_v), eq. 11.31 (∀r ∈ I: (r_s)_v = |κ′|); §14 availability specifier",
        "difficulty": 2,
        "kind": "code",
        "tags": ["erasure-coding", "delta-0.8.0", "constants", "tiny-vs-full"],
  "stemZh": "團隊的 Go 樹停在 GP 0.7.2、把 erasure-coding 的比率寫死如圖。GP 0.8.0 把固定比率換成函數 𝒟(v)。最小的正確遷移是什麼？它對 6 位 validator 的 tiny 設定又有什麼影響？",
  "optionsZh": [
   "只有總數需要跟隨 report 自己攜帶的 assuring-set 大小；資料碎片數僅由 segment 大小決定，因為 𝒟 是使 2d 整除 W_G 的最大 d，而填補寬度就是它的兩倍。因此 tiny 維持它的 4 與每 segment 1026 片，只有總數變成可變的，而 buildBCloud 除了讀取 report 的碎片數欄位之外不需要任何更動",
   "這些數字**每一個**都變成 report 自己攜帶之 assuring-set 大小的函數：總數就是那個大小（鏈上規則把它釘在 |κ′|）、資料碎片數是使 2d 整除 W_G 且 d 不大於 v/3 + 1 的最大 d、而填補寬度是它的兩倍。在 tiny 上這給出 6 取 3 個資料碎片、填補寬度 6、每 segment 684 片，所以舊的 4 / 1026 那一組必須拿掉",
   "把資料碎片數無條件設為 v/3 + 1、總數設為 report 攜帶的 assuring-set 大小、填補寬度設為碎片數的兩倍。因為合法的 validator 集合大小只含 3 的倍數，「碎片數的兩倍要整除 segment 大小」這個附帶條件自動滿足、可以拿掉；tiny 變成 6 取 3、每 segment 684 片，而 full 維持 1023 取 342",
   "這個檔案裡除了 segment 常數之外什麼都不用改。𝒟(v) 只管 Import-DA 的 segment 路徑，所以 audit-DA 的 bundle 維持它的 342:1023 比率與 684 位元組填補寬度，只有 segment 路徑改用 report 自己的碎片數；那個不對稱正是 availability spec 新增碎片數欄位的原因，也是 tiny 那一組維持 4 / 1026 而非 3 / 684 的原因"
  ],
  "stem": "The team's Go tree is on GP 0.7.2 and pins the erasure-coding rate as shown. GP 0.8.0 replaces the fixed rate with the function 𝒟(v). What is the minimal correct migration, and what does it do to the 6-validator tiny configuration?",
        "code": {
            "lang": "go",
            "caption": "internal/types/const.go (mode setters + package constants) and internal/work_package/work_package.go (buildBCloud)",
            "src": """// SetTinyMode()                     // SetFullMode()
	ECPiecesPerSegment = 1026         //   ECPiecesPerSegment = 6      // W_P
	ECBasicSize        = 4            //   ECBasicSize        = 684    // W_E

// erasure coding constants
// 342:1023 (Appendix H)
const (
	DataShards  = 342
	TotalShards = 1023
)

// buildBCloud
	padded := PadToMultiple(bundle, types.ECBasicSize)

	shards, err := erasurecoding.EncodeDataShards(padded, types.DataShards, types.TotalShards-types.DataShards)
	if err != nil {
		return nil, err
	}
	hashedShards := make([]types.OpaqueHash, len(shards))
	for i, shard := range shards {
		hashedShards[i] = hash.Blake2bHash(types.ByteSequence(shard))
	}""",
        },
        "options": [
            "Only the total needs to follow the assuring-set size that the report itself carries; the data-shard count is fixed by the segment size alone, since 𝒟 is the largest d with 2d dividing W_G, and the pad width is twice that. Tiny therefore keeps its 4 and its 1026 pieces per segment while only the total becomes variable, and buildBCloud needs no change beyond reading the report's shard-count field.",
            "Every one of these numbers becomes a function of the assuring-set size that the report itself carries: the total is that size (which the on-chain rule pins to |κ′|), the data-shard count is the largest d with 2d dividing W_G and d no greater than v/3 + 1, and the pad width is twice that. On tiny that gives 3 data shards out of 6, a pad width of 6 and 684 pieces per segment, so the old 4 / 1026 pair must go.",
            "Set the data-shard count to v/3 + 1 unconditionally, the total to the assuring-set size the report carries, and the pad width to twice the count. Because the set of legal validator-set sizes contains only multiples of three, the side condition that twice the count divide the segment size is automatically satisfied and can be dropped; tiny becomes 3 out of 6 with 684 pieces per segment and full stays 342 out of 1023.",
            "Nothing in this file changes beyond the segment constants. 𝒟(v) governs only the Import-DA segment path, so the audit-DA bundle keeps its 342:1023 rate and its 684-octet pad width, while the segment path alone switches to the report's own shard count; that asymmetry is exactly why the availability spec gained a shard-count field, and why the tiny pair stays 4 / 1026 rather than 3 / 684.",
        ],
        "answer": 1,
        "optNotes": [
          "丟掉了 eq. H.1 的候選集合 N_{v/3+2}：沒有 v/3+1 這個上界，最大的 d 會變成 2,052。",
          "三個數都成為 a_v 的函數：total = a_v、d = 𝒟(a_v)、pad 寬 2d，tiny 因此是 3/6 與 684 pieces。",
          "數值恰好對，錯在理由與通用性：v = 1002 時 335 不整除 2,052，真正的 𝒟(1002) = 228。",
          "§14 的 b♣ = H#(C^{a_v}_{⌈|b|/z⌉}(𝒫_z(b)))，bundle 路徑一樣吃 a_v 與 z = 2·𝒟(a_v)。",
        ],
        "explanation": "GP 0.8.0 的 eq. H.1：𝒟(v ∈ 𝕍) ≡ max({d | d ∈ N_{v/3+2}, W_G mod 2d = 0})，也就是「不超過 v/3+1 且 2d 能整除 W_G = 4,104 的最大 d」；配合 eq. 6.8 的 𝕍 ≡ {3c | c ∈ N_{2…C+1}}（§6 原文：「always a multiple of 3 between 6 and 3C」），rate 不再是常數而是每份 report 自帶的參數。eq. 11.5 讓 availability spec 多了 a_v ∈ 𝕍，緊接著 eq. 11.31 規定 ∀r ∈ I：(r_s)_v = |κ′|，§14 的 availability specifier 又把 z = 2·𝒟(a_v) 當成 bundle 補零與每段切片的寬度。代進 tiny：v = 6 → v/3+1 = 3，2·3 = 6 整除 4,104，所以 𝒟(6) = 3、z = 6、W_G/z = 684 pieces per segment；程式裡 tiny 的 4 / 1026 是 0.7.x 時代的值（等於 𝒟 = 2），必須換掉，否則 padded 長度與 encoder 期望的 2·DataShards 根本不一致。整除側條件不是裝飾：v = 1002 ∈ 𝕍 時 v/3+1 = 335，但 2d | 4104 要求 d 整除 2,052，335 不合，真正的 𝒟(1002) = 228，GP 也特別提醒「the rate is least efficient when v is slightly below one of these values」。團隊的 PR #1026／#1035（original_shards(v)）與 issue #1037（|κ| ≠ V）就是這條遷移。",
        "trap": "0.8.0 的 shard 數不是常數而是 report 欄位：先讀 a_v，再算 𝒟(a_v)，最後才 pad。tiny 從 2:6 變 3:6，每段 pieces 從 1026 變 684。",
    },

    {
        "id": "c3-appH-what-gets-coded",
        "ch": "H",
        "section": "H Erasure Coding",
        "gpRef": "§14 availability specifier (b♣, s♣, a_u); eq. 14.12 (paged proofs); eq. 11.5; eq. H.5–H.6",
        "difficulty": 1,
        "kind": "concept",
        "tags": ["erasure-coding", "availability", "audit-da", "d3l"],
  "stemZh": "對於一份 work-report，guarantor 會把哪些資料做 erasure coding 並發出去？單一位 validator 最後又持有什麼？",
  "optionsZh": [
   "一份資料集：work-report 本身，補零到資料碎片數兩倍的倍數後編碼成每位 validator 一個碎片，每個產生的碎片再被雜湊；erasure-root 就是對那些碎片雜湊所取的 well-balanced Merkle root。work-package bundle 與匯出 segment 留在 guarantor 手上、稽核時依請求提供，所以一位 validator 持有一個 32 位元組的碎片雜湊、別無其他",
   "一份資料集：只有匯出 segment 連同它們的 paged-proof segment 會被編碼、再經轉置讓每個 segment 的一個碎片落在同一位 validator 身上，因為只有它們必須在長期資料湖中存活。可稽核的 bundle 則是整份複製給每位 validator，這正是為什麼它可以在區塊定案後不久就被丟棄，而一位 validator 的 erasure-root 葉子就只是它自己那一欄 segment 的 root",
   "**兩份**資料集：可稽核的 bundle——補零到資料碎片數兩倍的倍數後編碼，每個產生的碎片再被雜湊；以及匯出 segment 連同它們的 paged-proof segment——各自編碼後再轉置，使每個 segment 的一個碎片落在同一位 validator 身上。一位 validator 持有 erasure-root 的一片葉子：它的 bundle 碎片雜湊串接它自己那一欄 segment 的 root",
   "一份資料集：只有 work-package bundle，補零到資料碎片數兩倍的倍數後編碼成與 assurer 數量相同的碎片，每個碎片被雜湊成 erasure-root 的一片葉子。匯出 segment 改由 segment-root 承諾、並在需要時靠重跑 refine 重建，這正是 segment-root 與 erasure-root 分屬不同欄位的原因，所以一位 validator 持有單一個 32 位元組的 bundle 碎片雜湊"
  ],
  "stem": "For one work-report, which data does a guarantor erasure-code and hand out, and what does an individual validator end up holding?",
        "options": [
            "One data set: the work-report itself, zero-padded up to a multiple of twice the data-shard count and then coded into one chunk per validator, with each resulting chunk hashed; the erasure-root is the well-balanced Merkle root over those chunk hashes. The work-package bundle and the exported segments stay with the guarantors, who serve them on request during an audit, so a validator holds one 32-octet chunk hash and nothing more.",
            "One data set: only the exported segments, together with their paged-proof segments, are coded and then transposed so that one chunk of every segment lands on the same validator, because only they must survive in the long-term data lake. The auditable bundle is replicated whole to every validator, which is precisely why it may be discarded soon after the block is finalized, and a validator's erasure-root leaf is just the root over its own segment column.",
            "Two data sets: the auditable bundle, zero-padded up to a multiple of twice the data-shard count and then coded, with each resulting chunk hashed; and the exported segments together with their paged-proof segments, each coded and then transposed so that one chunk of every segment lands on the same validator. A validator holds one leaf of the erasure-root: its bundle-chunk hash concatenated with the root over its own segment column.",
            "One data set: only the work-package bundle, zero-padded up to a multiple of twice the data-shard count and then coded into as many chunks as there are assurers, with each chunk hashed into a leaf of the erasure-root. The exported segments are committed to by the segment-root instead and are reconstructed on demand by re-running refine, which is why the segment-root and the erasure-root are separate fields, so a validator holds a single 32-octet bundle-chunk hash.",
        ],
        "answer": 2,
        "optNotes": [
          "work-report 只有幾 KB 而且本來就上鏈；a_u 的每片 leaf 也是 64 octets 而非單一 chunk hash。",
          "把 bundle 全量複製 1023 份正是 audit DA 要避免的事；它短命是因為只需撐到該區塊 final。",
          "§14 明寫 guarantor 要編碼並分發「two data sets」，validator 的 leaf 是 bundle chunk hash 接自己那欄的 M_B root。",
          "refine 的輸入（imported segments）本身就得先能取回，這正是長期 D³L 存在的理由。",
        ],
        "explanation": "§14 講得很直接：「Guarantors are required to erasure-code and distribute two data sets: one blob, the auditable bundle containing the encoded work-package, extrinsic data and self-justifying imported segments which is placed in the short-term Audit DA store; and a second set of exported-segments data together with the Paged-Proofs metadata.」availability specifier 的定義式把兩條路寫成 b♣ = H#(C^{a_v}_{⌈|b|/z⌉}(𝒫_z(b)))（先用 𝒫_z 補零到 z = 2·𝒟(a_v) 的倍數，再切片編碼，每片 chunk 各做一次 Blake2b）與 s♣ = M_B#(ᵀ C^{a_v}#_{W_G/z}(s ⌢ P(s)))（每個 segment 各自編碼、轉置後每個 validator 拿到自己那一欄，再對該欄取 M_B root）；最後 a_u = M_B([⌢x | x ∈ ᵀ[b♣, s♣]])，所以每個 validator 對應到 erasure-root 的一片 leaf＝「它的 bundle chunk hash ⌢ 它的 segment 欄 root」，共 64 octets。eq. 11.5 的說明也印證：「the root of a binary Merkle tree whose leaves are the a_v chunks produced by erasure-coding the work-package bundle and exported segments. As one chunk is distributed to each assurer, the number of chunks must equal the size of the assuring validator set.」segment-root 與 erasure-root 之所以是兩個欄位，是因為前者承諾 segment 內容、後者承諾分片配置。",
        "trap": "兩條線分開記：bundle 先 𝒫_z 補零→編碼→每片各做一次 Blake2b；segments 是 s ⌢ P(s) 一起編碼→轉置→每欄取 M_B root。erasure-root 的一片 leaf ＝同一個 validator 在這兩條線上的結果接起來。",
    },

    {
        "id": "c3-appH-rate-and-field-rationale",
        "ch": "H",
        "section": "H Erasure Coding",
        "gpRef": "eq. H.1 (𝒟) and the §H opening paragraph; eq. 6.8 (𝕍); eq. 11.17 (availability super-majority)",
        "difficulty": 2,
        "kind": "rationale",
        "tags": ["erasure-coding", "rationale", "gf65536", "threshold", "delta-0.8.0"],
  "stemZh": "附錄 H 說編碼比率是「derived from」三項各自獨立的考量。哪一種說法是對的？而這個編碼為什麼建立在 GF(2¹⁶) 而不是單一 octet 之上？",
  "optionsZh": [
   "重建必須能在將近三分之二的 validator 惡意或失能時仍然存活，這把資料碎片數壓在 v/3 + 1 附近、並與 2/3+1 的 assurance 超級多數彼此契合；欄位是 16 位元的，所以一個碼字就是一對 octet、而其取值點可以索引到多達 v 個相異的 validator；再者碎片數的兩倍必須整除 4,104 個 octet 的 segment 大小，好讓一個 segment 編碼時完全不需要填補——這正是碎片數取「最大的那個合格值」而不是恰好 v/3 + 1 的原因",
   "比率的選擇讓三分之二的 assurance 超級多數本身就是重建門檻，這把資料碎片數壓在 2v/3 附近；欄位是 16 位元純粹因為一個 segment 是 4,104 = 2 × 2,052 個 octet、碼字必須整齊地鋪滿它；而那個整除的附帶條件只是為了避免最後一個碎片需要長度前綴。在 1,023 位 validator 上這會給出 682 個資料碎片、每位 validator 每 segment 3 片",
   "資料碎片數對每一種合法的 validator 集合大小都恰好是 ⌊v/3⌋ + 1，所以那個整除的附帶條件從不生效、可以拿掉；選 GF(2¹⁶) 只是因為在現代硬體上 16 位元的乘加比逐位元組運算快；而 4,104 個 octet 的 segment 大小是**由欄位推導出來**而非反過來，4,104 只是碼字寬度最方便的最小倍數。在 1,002 位 validator 上這給出 335 個資料碎片且無需填補",
   "比率的設定讓恰好構成完整超級多數的那 683 位 validator 才能重建，這把可得性綁在 finality 上、並把碎片數固定在 2v/3 + 1 而不是最大的合格值；選 GF(2¹⁶) 是因為 Blake2b 送出 32 個 octet、也就是恰好 16 個碼字，所以碎片雜湊與碎片共用一種表示法；而碎片數的兩倍仍然整除 4,104 個 octet 的 segment 大小，因為 1,366 整除 4,104"
  ],
  "stem": "Appendix H says the coding rate 'is derived from' three separate considerations. Which account of them is right, and why is the code built over GF(2¹⁶) rather than over single octets?",
        "options": [
            "Reconstruction must survive almost two-thirds of the validators being malicious or incapacitated, which puts the data-shard count near v/3 + 1 and dovetails with the 2/3+1 assurance super-majority; the field is 16-bit, so one code word is an octet pair and the evaluation points can index up to v distinct validators; and twice the shard count must divide the 4,104-octet segment size so that a segment codes with no padding at all, which is why the count is the largest such value rather than exactly v/3 + 1.",
            "The rate is chosen so that a two-thirds super-majority of assurances is itself the reconstruction threshold, which puts the data-shard count near 2v/3; the field is 16-bit purely because a segment is 4,104 = 2 × 2,052 octets and the code words must tile it evenly; and the divisibility side condition exists only to keep the last chunk from needing a length prefix, which is why the count is the largest admissible value rather than exactly 2v/3. On 1,023 validators that gives 682 data shards and 3 pieces per validator per segment.",
            "The data-shard count is exactly ⌊v/3⌋ + 1 for every legal validator-set size, so the divisibility side condition is never active and could be dropped; GF(2¹⁶) is chosen only because 16-bit multiply-accumulate is faster than byte-wise arithmetic on modern hardware; and the 4,104-octet segment size follows from the field rather than the other way round, 4,104 being simply the smallest convenient multiple of the code-word width. On 1,002 validators that gives 335 data shards with no padding.",
            "The rate is set so that exactly the 683 validators of a full super-majority are needed to rebuild, which is what ties availability to finality and fixes the count at 2v/3 + 1 rather than at the largest admissible value; GF(2¹⁶) is chosen because Blake2b emits 32 octets, i.e. exactly 16 code words, so a chunk hash and a chunk share a representation; and twice the shard count still divides the 4,104-octet segment size, since 1,366 divides 4,104.",
        ],
        "answer": 0,
        "optNotes": [
          "三個理由與 §H 開頭的並列完全對應：近 2/3 容錯給出上界、16-bit field、segment 免 padding 的整除條件。",
          "682 早已超出 N_{v/3+2} 的上界 342，而且 2·682 = 1,364 不整除 4,104，切不出整數 pieces。",
          "v = 1002 時 335 不整除 2,052（𝒟 = 228）；GF(2⁸) 只有 256 個點，連 1,023 個 validator 都編不完。",
          "算術就錯了：1,366 × 3 = 4,098 尚餘 6；Blake2b 輸出 32 octets 與選 GF(2¹⁶) 也毫無因果關係。",
        ],
        "explanation": "§H 開頭原文把三個理由並列：「This rate is derived from the fact we wish to be able to reconstruct even should almost two-thirds of the v validators be malicious or incapacitated, the 16-bit Galois field on which the erasure-code is based and the desire to support, for simplicity, encoding segments of size W_G without padding.」對應到 eq. H.1 的 𝒟(v) ≡ max({d | d ∈ N_{v/3+2}, W_G mod 2d = 0})：上界 v/3+1 來自第一點（只要有 𝒟(v) 片就能重建，等於容忍將近 2/3 的節點消失，與 eq. 11.17 的 2/3+1 assurance 門檻互相搭配，而不是要求 2/3 的 chunk）；「2d 整除 4,104」來自第三點，所以 segment 用 k = W_G/(2𝒟(v)) 永遠是整數、完全不必 padding；而取 max 而非直接等於 v/3+1，正是因為整除條件會把它往下拉——GP 自己舉例「when v = 1022, the rate is approximately 1:4.5」——但要注意 1022 ∉ 𝕍（𝕍 只收 6 到 1023 之間 3 的倍數），這是個假想值：也只有在 v 不是 3 的倍數時，H.1 的上界該讀成 ⌊v/3⌋+1 還是 v/3+1 才會有差（取 ⌊1022/3⌋+1 = 341 才得到 𝒟 = 228、rate ≈ 1:4.48，與 GP 自己寫的 1:4.5 相符；讀成 342 則是 1:2.99）。對每個合法的 v 兩種讀法一致（v/3 ∈ ℕ），真正能驗證整除側條件確實會生效的合法案例是 v = 1002：v/3+1 = 335 不整除 2,052，𝒟(1002) = 228。至於為什麼是 GF(2¹⁶)：code word 就是一個 octet pair，validator i 被映成 field element ĩ = Σ i_j v_j（Cantor basis），evaluation point 必須每個 validator 各一個且互異，GF(2⁸) 只有 256 個點，連 1,023 個 validator 都編不完，這是 16-bit 最直接的必要性（§H 只把 16-bit GF 列為三項考量之一，並未替它們排序）。0.7.2 時這一切是寫死的 342:1023，0.8.0 才為了支援較小的 validator set 而變成以 v 為參數的函數。",
        "trap": "「三分之一容錯」講的是 chunk 門檻 𝒟(v) ≈ v/3+1（任 1/3 即可重建），「三分之二」講的是 assurance 的 super-majority——兩個門檻方向相反，別對調。",
    },
]
