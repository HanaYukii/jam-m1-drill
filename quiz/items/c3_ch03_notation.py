# -*- coding: utf-8 -*-
"""GP 0.8.0 §3 Notational Conventions — batch c3.

Ground truth: /root/work/jam/gp-src/text/notation.tex, cross-checked against preamble.tex
(\\Nmax{n} = N_n, \\bloblength = N_L, \\blob = B, \\dictionary, \\optional{A} = A?, \\none = ∅,
\\error = ∇, \\fnsubifnone = 𝒰, \\cyclic{s[i]} = s[i]^⟲, \\interval{a}{b} = _{a…b},
\\subrange{a}{b} = _{a…+b}, \\is = tricolon, \\isa = ∈).
§3 has 11 numbered equations: 3.1 precedes · 3.2 substitute-if-nothing · 3.3–3.4 dictionary
constraint · 3.5–3.6 key/value pairs · 3.7 d[k] · 3.8 d ∖ s · 3.9 K(d) · 3.10 V(d) · 3.11 d ∪ e.
"""

ITEMS = [
    {
        "id": "c3-ch03-bounded-numeric-blob-types",
        "ch": "3",
        "section": "3.4 Numbers / 3.7.4 Octets and Blobs",
        "gpRef": "§3.4; §3.7.4; §3.8.1",
        "difficulty": 1,
        "kind": "concept",
        "tags": ["notation", "types", "blobs", "numbers"],
  "stemZh": "Gray Paper 裡幾乎每個型別都建立在 §3.4 與 §3.7.4 固定下來的詞彙上：N、N_n、Z、N_L、B、B_x 與 B_$。哪一個敘述把它們全部照 GP 的定義讀對了？",
  "optionsZh": [
   "帶下標的自然數集是嚴格小於下標的自然數，所以 N_n 有 n 個元素；N_L 是 octet 序列長度的集合、等同 N_{2^32}；B_x 是長度恰為 x 的 blob 集合，但 B_$ 是其中首個位元組為哨兵標記的子集；而 octet 就是小於 256 的自然數，兩者序列化方式相同",
   "帶下標的自然數集包含下標本身，所以 N_n 有 n + 1 個元素；N_L 等同 N_{2^64}，因為 octet 序列的長度是以 64 位元值攜帶的；B_x 是長度恰為 x 的 blob 集合、B_$ 是其中屬於 ASCII 編碼字串的子集；而 octet 雖與小於 256 的自然數一一對應，在序列化上並非同一種實體",
   "帶下標的自然數集是嚴格小於下標的自然數，所以 N_n 有 n 個元素；N_L 是 GP 用來指稱 octet 序列**長度**集合的簡寫、等同 N_{2^32}；B_x 是長度恰為 x 的 blob 集合、B_$ 是其中屬於 ASCII 編碼字串的子集；而 octet 雖與小於 256 的自然數一一對應，就序列化而言並非同一種實體",
   "帶下標的自然數集是嚴格小於下標的自然數，所以 N_n 有 n 個元素；N_L 是長度小於 2^32 的 octet 序列集合，而不是它們長度的集合；B_x 是至多 x 個 octet 的 blob 集合、B_$ 是其中屬於 ASCII 編碼字串的子集；而 octet 的序列化方式與一般自然數編碼完全相同"
  ],
  "stem": (
            "Almost every type in the Gray Paper is built from the vocabulary fixed in §3.4 and §3.7.4: N, "
            "N_n, Z, N_L, B, B_x and B_$. Which statement reads all of them the way the GP defines them?"
        ),
        "options": [
            "The subscripted natural set is the naturals strictly below the subscript, so N_n has n members; "
            "N_L is the set of lengths of octet sequences and is equivalent to N_{2^32}; B_x is the set of "
            "blobs of length exactly x but B_$ is the subset whose leading octet is a sentinel marker; and an "
            "octet just is a natural under 256, so the two serialize identically.",
            "The subscripted natural set includes the subscript itself, so N_n has n + 1 members; N_L is "
            "equivalent to N_{2^64} because octet-sequence lengths are carried as 64-bit values; B_x is the "
            "set of blobs of length exactly x and B_$ the subset which are ASCII-encoded strings; and an "
            "octet, though bijective with a natural under 256, is not the same entity under serialization.",
            "The subscripted natural set is the naturals strictly below the subscript, so N_n has n members; "
            "N_L is the GP's shorthand for the set of *lengths* of octet sequences and is equivalent to "
            "N_{2^32}; B_x is the set of blobs of length exactly x and B_$ the subset which are ASCII-encoded "
            "strings; and an octet, though bijective with a natural under 256, is not the same entity for "
            "serialization.",
            "The subscripted natural set is the naturals strictly below the subscript, so N_n has n members; "
            "N_L is the set of octet sequences shorter than 2^32 rather than the set of their lengths; B_x is "
            "the set of blobs of at most x octets and B_$ the subset which are ASCII-encoded strings; and an "
            "octet serializes exactly as the general natural-number encoding does.",
        ],
        "answer": 2,
        "optNotes": [
            "B_$ 是 ASCII 字串子集、與 sentinel 標記無關；octet 與自然數在序列化上明確不等價。",
            "N_n 是嚴格小於（恰 n 個元素），且 N_L 等價於 N_{2^32} 而不是 N_{2^64}。",
            "四項全對上 §3.4 與 §3.7.4：嚴格小於、長度集合、恰好 x 個 octet、octet 與自然數序列化不同。",
            "N_L 是**長度**的集合而非 blob 集合；B_x 是恰好 x，且 octet 一律序列化為自身。",
        ],
        "explanation": "§3.4：「N denotes the set of naturals including zero whereas N_n implies a restriction on that set to values less than n. Formally, N = {0, 1, …} and N_n = {x | x ∈ N, x < n}」——嚴格小於，所以 N_n 有 n 個元素。同節：「we denote N_L as the set of lengths of octet sequences and is equivalent to N_{2^32}」——N_L 是**長度的集合**（一個自然數集），不是 blob 的集合。§3.7.4：「B denotes the set of octet strings (“blobs”) of arbitrary length… B_x denotes the set of such sequences of length x. B_$ denotes the subset of B which are ascii-encoded strings」。同節最後那句是面試最愛考的：「while an octet has an implicit and obvious bijective relationship with natural numbers less than 256…we do not treat them as exactly equivalent entities. In particular for the purpose of serialization, an octet is always serialized to itself, whereas a natural number may be serialized as a sequence of potentially several octets, depending on its magnitude and the encoding variant」——這是 App. C 裡 blob 直接落地、而自然數走 E 或 compact 變體的根據。另外 §3.8.1 定義 hash 集合 H ≡ B_32。",
        "trap": "N_L 是「長度」的集合（= N_{2^32}），不是 blob 的集合；B_x 是「恰好 x」不是「至多 x」。",
    },
    {
        "id": "c3-ch03-optional-none-error",
        "ch": "3",
        "section": "3.3 Sets / 3.2 Functions and Operators",
        "gpRef": "§3.3; eq. 3.2 (substitute-if-nothing); applied at eq. 13.13",
        "difficulty": 1,
        "kind": "concept",
        "tags": ["notation", "optional", "none", "error"],
  "stemZh": "§3.3 引入 ∅、∇ 與 optional 建構子 A?，eq. 3.2 定義了「若為空則替代」的函數 𝒰。§13.2 接著把一個 service 的 accumulation 條目寫成 𝒰(S[s], (0, 0, 0))，其中 S 是從 service index 到三元組的字典。哪一種讀法是對的？",
  "optionsZh": [
   "∅ 標記一個「合法地沒有具體值」的項，並被定義為基數為零；optional 建構子給出 A? ≡ A ∪ {∅}；∇ 標記非預期的失敗或無效值，GP 偏好用它而不用 ⊥ 以免與布林假值混淆；而 𝒰 取出它第一個不是 ∅ 的參數——所以字典裡有該 service 時取它自己的三元組，否則取全零三元組",
   "∅ 就是空集合本身，它的基數為零只是因為裡面剛好沒有成員；optional 建構子 A? 是一個編碼指示，意思是該成分可以從編碼中省略，而不是集合運算；∇ 是 GP 對布林假值選用的寫法，這也是為什麼避開較常見的 ⊥；而 𝒰 取出它**最後**一個不是 ∅ 的參數——所以只要字典裡有任何東西，該條目就是全零三元組",
   "∅ 標記一個「合法地沒有具體值」的項，optional 建構子給出 A? ≡ A ∪ {∅}；∇ 是 ∅ 的同義詞，保留給「這個缺席是預期中的」情況，所以兩者是 A? 裡可互換的成員；而 𝒰 取出它第一個**確實是** ∅ 的參數，若都不是則退回最後一個參數——所以每個被 accumulate 過的 service 條目都是 ∅，只有沒被碰過的才是全零三元組",
   "∅ 的基數為一，它是 A? 加進 A 的一個獨立成員；∇ 標記非預期的失敗或無效值，GP 偏好用它而不用 ⊥ 以免與布林假值混淆；𝒰 恰好定義在兩個參數上，一個候選值與一個預設值；而對缺少的 key 做字典下標會得到 ∇ 而不是 ∅——這正是 eq. 13.13 需要那個 fallback 的原因"
  ],
  "stem": (
            "§3.3 introduces ∅, ∇ and the optional constructor A?, and eq. 3.2 defines the substitute-if-nothing "
            "function 𝒰. §13.2 then writes a service's accumulation entry as 𝒰(S[s], (0, 0, 0)), where S is a "
            "dictionary from service index to a triple. Which reading is correct?"
        ),
        "options": [
            "∅ marks a term validly left without a specific value and is defined to have cardinality zero; the "
            "optional constructor gives A? ≡ A ∪ {∅}; ∇ marks an unexpected failure or an invalid value, and "
            "the GP prefers it to ⊥ so it is not confused with Boolean false; and 𝒰 yields its first argument "
            "that is not ∅ — so the entry is the service's own triple when the dictionary holds one and the "
            "all-zero triple otherwise.",
            "∅ is the empty set itself, so it has cardinality zero only because it happens to hold no "
            "members; the optional constructor A? is a codec directive meaning the component may be omitted "
            "from the encoding rather than a set operation; ∇ is the GP's chosen spelling of Boolean false, "
            "which is why the more conventional ⊥ is avoided; and 𝒰 yields the last of its arguments that is "
            "not ∅ — so the entry is the all-zero triple whenever the dictionary holds anything at all.",
            "∅ marks a term validly left without a specific value and the optional constructor gives "
            "A? ≡ A ∪ {∅}; ∇ is a synonym for ∅ reserved for the case where the absence was anticipated, so "
            "the two are interchangeable inhabitants of A?; and 𝒰 yields the first of its arguments that *is* "
            "∅, falling back to its last argument when none of them is — so the entry is ∅ for every service "
            "that was accumulated and the all-zero triple only for the untouched ones.",
            "∅ has cardinality one, being a distinct inhabitant that A? adds to A; ∇ marks an unexpected "
            "failure or an invalid value and the GP prefers it to ⊥ so it is not confused with Boolean false; "
            "𝒰 is defined for exactly two arguments, a candidate and a default; and a dictionary subscript on "
            "a missing key yields ∇ rather than ∅ — which is precisely why eq. 13.13 needs its fallback.",
        ],
        "answer": 0,
        "optNotes": [
            "§3.3 與 eq. 3.2 逐句對上：∅ 的 cardinality 為零、A? ≡ A ∪ {∅}、∇ 表錯誤、𝒰 取第一個非 ∅。",
            "A? 是集合運算不是 codec 指示；GP 不用 ⊥ 正是怕與 Boolean false 混淆，∇ 不是 false。",
            "∇ 與 ∅ 語意相反：前者是「出錯了」，後者才是「合法地沒有值」；𝒰 取的也是非 ∅ 的那個。",
            "∅ 的 cardinality 依 §3.3 定義為零；eq. 3.7 的 dictionary miss 給 ∅，且 𝒰 不限兩個引數。",
        ],
        "explanation": "§3.3：「We commonly use ∅ to indicate that some term is validly left without a specific value. Its cardinality is defined as zero. We define the operation A? such that A? ≡ A ∪ {∅}」；「The term ∇ is utilized to indicate the unexpected failure of an operation or that a value is invalid or unexpected. (We try to avoid the use of the more conventional ⊥ here to avoid confusion with Boolean false…)」——∅ 與 ∇ 語意完全不同：前者是「合法地沒有值」，後者是「錯了」。eq. 3.2：𝒰(a_0, … a_n) ≡ a_x : (a_x ≠ ∅ ∨ x = n), ⋀_{i=0}^{x−1} a_i = ∅，GP 自己給的例子是 𝒰(∅, 1, ∅, 2) = 1 與 𝒰(∅, ∅) = ∅——取**第一個非 ∅** 的引數，且可以有兩個以上引數。至於 dictionary 查不到 key 時的結果：eq. 3.7 明寫 d[k] ≡ v if ∃k : (k ↦ v) ∈ d，otherwise ∅（不是 ∇）；這正是 𝒰(S[s], (0, 0, 0)) 能運作的原因——沒被 accumulate 的 service 查出 ∅，於是落到後備的全零三元組；若 dictionary miss 真的給 ∇，eq. 13.13 這個包裝就救不回來，因為 ∇ 代表的是「出錯了」而不是「合法地沒有值」。",
        "trap": "∅ = 合法的「沒有值」；∇ = 錯誤。dictionary miss 給 ∅，不是 ∇；𝒰 取第一個非 ∅。",
    },
    {
        "id": "c3-ch03-ellipsis-ranges",
        "ch": "3",
        "section": "3.4 Numbers / 3.7 Sequences",
        "gpRef": "§3.4 (Z_{a…b}, Z_{a…+b}); §3.7 (slicing, s[i]^⟲, last)",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["notation", "sequences", "slicing", "ranges"],
  "stemZh": "令 s = [10, 20, 30, 40, 50]。套用 GP §3.4 對整數集合、以及 §3.7 對序列切片的省略號慣例，哪一行從頭到尾都正確？",
  "optionsZh": [
   "s_{…3} = [10, 20]、s_{1…+3} = [20, 30, 40, 50]、Z_{1…3} = {1, 2, 3}、Z_{1…+3} = {1, 2, 3, 4}、last(s) = 50、s[7]^⟲ = 20",
   "s_{…3} = [10, 20, 30]、s_{1…+3} = [20, 30, 40]、Z_{1…3} = {1, 2}、Z_{1…+3} = {1, 2, 3}、last(s) = 50、s[7]^⟲ = 30",
   "s_{…3} = [30, 40, 50]、s_{1…+3} = [10, 20, 30]、Z_{1…3} = {1, 2}、Z_{1…+3} = {1, 2, 3}、last(s) = 10、s[7]^⟲ = 40",
   "s_{…3} = [10, 20, 30]、s_{1…+3} = [20, 30]、Z_{1…3} = {1, 2, 3}、Z_{1…+3} = {2, 3, 4}、last(s) = 50、s[7]^⟲ = 30"
  ],
  "stem": (
            "Let s = [10, 20, 30, 40, 50]. Applying the ellipsis conventions of GP §3.4 for integer sets and "
            "§3.7 for sequence slicing, which line is correct throughout?"
        ),
        "options": [
            "s_{…3} = [10, 20], s_{1…+3} = [20, 30, 40, 50], Z_{1…3} = {1, 2, 3}, Z_{1…+3} = {1, 2, 3, 4}, "
            "last(s) = 50, s[7]^⟲ = 20",
            "s_{…3} = [10, 20, 30], s_{1…+3} = [20, 30, 40], Z_{1…3} = {1, 2}, Z_{1…+3} = {1, 2, 3}, "
            "last(s) = 50, s[7]^⟲ = 30",
            "s_{…3} = [30, 40, 50], s_{1…+3} = [10, 20, 30], Z_{1…3} = {1, 2}, Z_{1…+3} = {1, 2, 3}, "
            "last(s) = 10, s[7]^⟲ = 40",
            "s_{…3} = [10, 20, 30], s_{1…+3} = [20, 30], Z_{1…3} = {1, 2, 3}, Z_{1…+3} = {2, 3, 4}, "
            "last(s) = 50, s[7]^⟲ = 30",
        ],
        "answer": 1,
        "optNotes": [
            "把整數區間讀成閉區間、切片又少取一格；7 mod 5 = 2 應得 s[2] = 30 而非 s[1]。",
            "半開區間與 offset/length 逐項對上，前綴切片與 7 mod 5 = 2 也都算對。",
            "把前綴切片讀成後綴、把 …+ 當成從頭取，last(s) 取的更是第一個元素而非最後。",
            "Z_{1…3} 是半開的 {1, 2}；…+3 是從 index 1 起算三個，Z_{1…+3} 也不從 2 起跳。",
        ],
        "explanation": "§3.4：「Z_{a…b} = {x | x ∈ Z, a ≤ x < b}. E.g. Z_{2…5} = {2, 3, 4}」——**半開**區間；「We denote the offset/length form of this set as Z_{a…+b}, a short form of Z_{a…a+b}」。§3.7 對序列用同一套省略號：「A range may be denoted using an ellipsis for example: [0, 1, 2, 3]_{…2} = [0, 1] and [0, 1, 2, 3]_{1…+2} = [1, 2]」——下標只有結尾時是「取前 n 個」（等價於 index < n），有 …+ 時是 offset/length。同節另有兩個記號：「We denote modulo subscription as s[i]^⟲ ≡ s[i mod |s|]」與「We denote the final element x of a sequence s = [..., x] through the function last(s) ≡ x」。GP 全篇沒有任何「a 到 b 皆含」的閉區間記法——從 PDF 抄公式時最常見的錯誤就是把它讀成閉區間。另外會在正文遇到 §3 從未定義的 N_{a…b}（preamble 的 \\Nclamp，例如 eq. 6.8 的 𝕍 ≡ {3c | c ∈ N_{2…C+1}}）：它沿用同一套半開讀法，C = 341 時 c 的上界是 341（c < 342），𝕍 的最大值才會剛好是 3 · 341 = 1023。",
        "trap": "GP 只有兩種形式：半開的 a…b，與 offset/length 的 a…+b；序列切片沿用同一套，沒有閉區間。",
    },
    {
        "id": "c3-ch03-prime-dagger-record",
        "ch": "3",
        "section": "3.6 Tuples / 3.7 Sequences",
        "gpRef": "§3.6 (named tuple components); eq. 4.1 (σ′ ≡ Υ(σ, B)); §4 state-transition dependency graph; eq. 13.1–13.3",
        "difficulty": 3,
        "kind": "concept",
        "tags": ["notation", "tuples", "prior-vs-posterior", "state"],
  "stemZh": "eq. 13.1–13.2 宣告 π ≡ (π_V, π_L, π_C, π_S)，其中 (π_V, π_L) ∈ ⟦(b ∈ N, t ∈ N, p ∈ N, d ∈ N, g ∈ N, a ∈ N)⟧²，而 §13.1 接著處理 π_V†、π_V‡ 與 π′_V。面試官請你把這段記號唸出來。哪一種讀法是對的？",
  "optionsZh": [
   "型別宣告與具體值都用 ∈ 書寫，三重冒號保留給字典的 key/value 配對，所以那六個計數器只有位置意義、必須以索引而非名稱存取；把序列集合平方表示那兩筆紀錄各自都是序列，每位 validator 一筆六欄位項目；prime 代表某個狀態分量經 Grandpa 定案後的值，所以 π′ 要等 finality 追上鏈之後才有定義；而 dagger 與 double-dagger 標記的是同一個分量在某條後來被丟棄的分叉上的樣子",
   "型別宣告用 ∈ 引入每個成分，具體值則用三重冒號綁定欄位，兩種寫法都可以用名稱下標把欄位讀回來；把序列集合平方表示這一對總共剛好兩筆紀錄、每個 epoch 一筆，所以每筆帶的是單一位 validator 的六個計數器；prime 標記下一個 epoch 開始時將會生效的值；而 dagger 與 double-dagger 是 σ 的另外兩個分量，各自有自己的 state-trie key",
   "∈ 與三重冒號是同一種綁定的兩種可互換寫法，所以欄位既可用名稱也可用位置讀回；把序列集合平方表示那兩筆紀錄各自都是序列，每位 validator 一筆六欄位項目；§3 把 prime 定義為「extrinsic 套用之後的值」；而 dagger 標記已經歷過 epoch 換屆的值、double-dagger 標記尚未歷經的",
   "型別宣告用 ∈ 引入每個成分，具體值則用三重冒號綁定欄位，兩種寫法都可以用名稱下標把欄位讀回來；把序列集合平方表示那兩筆紀錄各自都是序列，每位 validator 一筆六欄位項目；未加裝飾的符號是 prior 狀態、加了 prime 的是 posterior——這個慣例 GP 不是在 §3 訂下的，而是在 σ′ ≡ Υ(σ, B) 旁邊訂的——而 dagger 與 double-dagger 標記的是單一次轉移內部的中間值，它們既不在 σ 也不在 σ′ 裡"
  ],
  "stem": (
            "Eq. 13.1–13.2 declare π ≡ (π_V, π_L, π_C, π_S) with (π_V, π_L) ∈ ⟦(b ∈ N, t ∈ N, p ∈ N, d ∈ N, "
            "g ∈ N, a ∈ N)⟧², and §13.1 then works through π_V†, π_V‡ and π′_V. An interviewer asks you to read "
            "that notation aloud. Which reading is right?"
        ),
        "options": [
            "A type declaration and a concrete value are both written with ∈, the tricolon being reserved "
            "for the key/value pairs of a dictionary, so the six counters are positional only and must be "
            "addressed by index rather than by name; squaring the sequence-set says each of the two records "
            "is itself a sequence, one six-field entry per validator; the prime denotes the Grandpa-finalized "
            "value of a state component, so π′ is only well defined once finality has caught up with the "
            "chain; and dagger and double-dagger mark the same component as it stood on a fork that was "
            "later discarded.",
            "A type declaration introduces each component with ∈ while a concrete value binds its fields "
            "with the tricolon, and either way a field is read back by subscripting its name; squaring the "
            "sequence-set means the pair holds exactly two records in total, one per epoch, so each record "
            "carries a single validator's six counters; the prime marks the value that will be current at "
            "the start of the next epoch; and dagger and double-dagger are two further components of σ, each "
            "with its own state-trie key.",
            "∈ and the tricolon are interchangeable spellings of the same binding, so a field may equally be "
            "read back by name or by position; squaring the sequence-set says each of the two records is "
            "itself a sequence, one six-field entry per validator; §3 defines the prime as 'the value after "
            "the extrinsic has been applied'; and the dagger marks a value that has already been through the "
            "epoch rollover while the double-dagger marks one that has not.",
            "A type declaration introduces each component with ∈ while a concrete value binds its fields "
            "with the tricolon, and either way a field is read back by subscripting its name; squaring the "
            "sequence-set says each of the two records is itself a sequence, one six-field entry per "
            "validator; the undecorated symbol is the prior state and the primed one the posterior — a "
            "convention the GP fixes not in §3 but alongside σ′ ≡ Υ(σ, B) — and dagger and double-dagger "
            "mark intermediate values inside a single transition that appear in neither σ nor σ′.",
        ],
        "answer": 3,
        "optNotes": [
            "型別宣告用 ∈、具體值用 tricolon，欄位一律以名字下標；prime 也與 finality 無關。",
            "上標 2 是把整個序列集合取平方：π_V 與 π_L 各自是序列、每個 validator 一筆；dagger 也沒有 trie key。",
            "∈ 與 tricolon 不可互換、沒有位置索引；prime 不在 §3 定義，dagger 與 double-dagger 的先後也說反了。",
            "prime 由 eq. 4.1 旁的文字定下、dagger 出自 §4 的 dependency graph，兩者都不在 §3。",
        ],
        "explanation": "§3.6 Tuples：「we may denote a tuple with two named natural components a and b as T = (a ∈ N, b ∈ N). We would denote an item t ∈ T through subscripting its name, thus for some t = (a ⦂ 3, b ⦂ 5), t_a = 3 and t_b = 5」——型別宣告用 ∈、具體值用 tricolon（⦂），欄位一律用**名字**下標讀取。tricolon 的位置也要記牢：§3.5 的 dictionary 用的是 ↦（k ↦ v），tricolon 只出現在 §3.6 具體 tuple 值的欄位綁定。eq. 13.2 的上標 2 則是把整個「序列集合」取平方：π_V 與 π_L **各自**都是一個序列，eq. 13.3 再釘死長度 |π_V| = |κ|、|π_L| = |λ|（0.8.0 改用 |κ|/|λ| 取代常數 V，根源是 eq. 6.8 的 𝕍 ≡ {3c | c ∈ N_{2…C+1}} 與 κ, λ ∈ ⟦𝕂⟧_𝕍——validator-set 大小在 0.8.0 是**可變**的）。最刁鑽的一點：prime 的意義**不是**在 §3 定義的——§3 只談 typography、sets、numbers、dictionaries、tuples、sequences、cryptography，通篇沒有 prime 字樣。它是在 §4 的 eq. 4.1 旁以文字定下的：「Where σ is the prior state, σ′ is the posterior state, B is some valid block and Υ is our block-level state-transition function」。dagger 同樣出自 §4 的 dependency graph 段落：「The only synchronous entanglements are visible through the intermediate components superscripted with a dagger」——π_V† / π_V‡ 是單次 transition 內部的中間值，既不在 eq. 4.4 的 σ 分量清單裡，也沒有自己的 state-trie key（π 整體只佔 C(13) 一把）。兩者先後見 eq. 13.4 的 π_V†（rollover **之前**：assurance 已加、尚未換代）與 eq. 13.5 產出的 π_V‡（rollover **之後**的起點）——把先後說反，正好會把 epoch 邊界那一塊的 counter 放錯 record。",
        "trap": "「prime 在 GP 哪一節定義？」——不在 §3，而是 §4 eq. 4.1；dagger/double-dagger 也是 §4 交代的中間值。",
    },
]
