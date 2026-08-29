# -*- coding: utf-8 -*-
SHEETS = [
{
 "ch": "E",
 "title": "General Merklization / MMR",
 "one": "通用的 Merkle 工具箱：well-balanced 樹 M、常數深度子樹分頁 C、trace 函數 T，"
        "以及只 append 的 Mountain Range（MMR）—— accumulation output 與 BEEFY 用的就是後者。",
 "flow": [
   "M：well-balanced Merkle 樹，最大深度最小、且該深度的葉子數也最小",
   "C：常數化前處理，把每個資料項冠上 $leaf 前綴 hash，再用 zero hash 補到 2 的冪次",
   "T：trace 函數，從根走到某個索引的葉子，沿途回傳每一層的兄弟節點 —— 這就是證明",
   "MMR：只 append；新增一筆合併相鄰同高的峰，舊證明依然有效",
   "super-peak：把 MMR 的所有峰合成單一 hash，放進 β_H item 的 b 欄位供 BEEFY 簽名",
 ],
 "consts": [
   ["N(v) = ⌈|v|/2⌉", "樹的左右切分點 —— 是 ceil，不是 floor"],
   ["$leaf / $node", "常數化前處理用的 domain separator"],
   ["M_R", "hard-wire Keccak 的變體；A 系列則以 hash 函數為參數"],
 ],
 "eqs": [
   ["eq. E.1", "N 的定義（⌈|v|/2⌉）"],
   ["§E.2", "C 的零填充與 $leaf 前綴"],
   ["§E.3", "MMR 的 append 與 super-peak"],
 ],
 "asked": [
   ["為什麼 accumulation output 用 MMR 而不是普通 Merkle 樹？",
    "輸出是持續 append 的，而外部（BEEFY 的消費者）需要長期有效的證明。"
    "MMR 新增一筆只影響 O(log n) 個節點且舊證明不失效；普通樹每次都要重建、舊證明全廢。"],
   ["為什麼要 $leaf 前綴？",
    "沒有 domain separator 的話，一個「葉子的值」有可能剛好等於某個內部節點的 hash，"
    "攻擊者就能把內部節點偽裝成葉子做第二原像攻擊。前綴讓兩者的輸入空間不相交。"],
   ["切分點寫成 ⌊|v|/2⌋ 會怎樣？",
    "奇數長度的那一層會左右顛倒，co-path 的兄弟節點就取錯，證明驗不過。"
    "若上層剛好都先補齊成 2 的冪次可能會意外躲過，但只要有一處對未補齊的序列呼叫就會出錯。"],
 ],
 "delta": ["0.8.0 明確區分以 hash 為參數的 A 系列與 hard-wire Keccak 的 M_R"],
 "code": ["⚠ merkle_tree.T 用 len(v)/2，應為 ⌈|v|/2⌉；ce140.go 對未補齊的 chunk slice 呼叫 T"],
},
{
 "ch": "F",
 "title": "Shuffling",
 "one": "Fisher–Yates 的確定性版本：吃一個 hash 當種子展開成數字流，產生可重現的排列。"
        "validator → core 的指派、auditor 的抽選都靠它。",
 "flow": [
   "由 32-byte 種子用 hash 展開成足夠長的 32-bit 數字序列",
   "以標準 Fisher–Yates 由後往前取模抽換",
   "同樣的種子在任何實作上都必須得到同一個排列",
 ],
 "consts": [
   ["確定性", "沒有任何實作自由度；用系統 RNG 一定會分叉"],
   ["種子來源", "多半是 η′_2 或其衍生值，見 §6 與 §11"],
 ],
 "eqs": [
   ["§F", "洗牌函數的定義與數字流展開"],
   ["eq. 11.22", "core assignment 的實際使用處"],
 ],
 "asked": [
   ["為什麼不能用語言內建的 shuffle？",
    "內建 shuffle 的 RNG 與取模策略因語言與版本而異，兩個實作會得到不同排列，"
    "進而對「誰該 guarantee 哪個 core」有不同看法 —— 直接分叉。"],
   ["洗牌的隨機來源為什麼要用退兩格的熵？",
    "用當前 epoch 還在累積的熵，出塊者可以靠出不出塊來偏移自己的指派；"
    "退兩格（η′_2）讓抽籤依據在兩個 epoch 前就凍結。"],
 ],
 "delta": ["符號與定義在 0.8.0 沒有實質變動"],
 "code": ["自己實作，不要呼叫 rand.Shuffle；並用測試向量比對整個排列而不只是抽樣"],
},
{
 "ch": "G",
 "title": "Bandersnatch VRF",
 "one": "Safrole 的密碼學基礎：ring VRF 讓 validator 證明「我屬於這組人」並產生可驗證的隨機輸出，"
        "但不洩漏自己是誰，直到出塊那一刻才揭露。",
 "flow": [
   "ring root 由 γ_K 這組 bandersnatch 公鑰算出，型別是 𝔹_144",
   "ticket = ring VRF 證明 + 輸出；輸出的 hash 決定 ticket id（排序用）",
   "每個 validator 每 epoch 有 N = 2 個 entry index i_e，可產兩張不同的票",
   "出塊時改用一般（非 ring）簽章：H_S 證明出塊權、H_V 貢獻熵",
 ],
 "consts": [
   ["𝔹_144", "ring root 的型別（144 bytes 的 blob，不是 𝕐）"],
   ["i_e ∈ {0, 1}", "ticket entry index，讓一人最多兩張票"],
   ["X_ 前綴", "各種簽章的 domain separator，混用會讓簽章可跨用途重放"],
 ],
 "eqs": [
   ["§G", "ring VRF 的建構與驗證"],
   ["eq. 6.25–6.27", "ticket 如何變成 slot sealer 序列"],
 ],
 "asked": [
   ["ring VRF 比普通 VRF 多給了什麼？",
    "普通 VRF 的證明綁定單一公鑰，等於公告身分；ring VRF 只證明「簽名者屬於這個 ring」。"
    "在 Safrole 裡這代表：票投進來時沒人知道是誰的，出塊時才揭露 —— 攻擊者無法提前針對特定人下手。"],
   ["為什麼一人只給兩張票？",
    "票數上限決定了單一 validator 在一個 epoch 能占多少出塊機會。"
    "給太多會讓運氣好的人連續出塊、方便短鏈重組；給一張則在票源不足時太容易掉進 fallback。"],
 ],
 "delta": ["0.8.0 明確把 ticket entry index 寫作 i_e；ring root 的型別是 𝔹_144"],
 "code": ["用官方 bandersnatch 綁定；ring root 的重算成本高，要在 γ_K 變動時才重算並快取"],
},
{
 "ch": "H",
 "title": "Erasure Coding",
 "one": "把 bundle 切成 shard 發給全體 validator，使得任何約 1/3 的 validator 就能重建。"
        "基於 16-bit Galois field 的 Reed–Solomon，是可得性系統的底層。",
 "flow": [
   "原始資料補齊後切成 𝒟(v) 個原始 shard，編碼成 v 個 shard（v = validator 數）",
   "任意 𝒟(v) 個 shard 即可還原；𝒟(v) = v/3 + 1 時 rate 最佳",
   "每個 validator 拿一個 shard，assurance 的 bitfield 就是在宣告「我手上有這些 core 的 shard」",
   "segment 大小 4,104 octet，在 1023 validator 下得到 6 路資料平行",
 ],
 "consts": [
   ["GF(2^16)", "編碼所在的有限體"],
   ["𝒟(v) = v/3 + 1", "最佳 rate 的原始 shard 數；v ∈ 𝕍 時成立"],
   ["4,104", "segment 大小（octet）"],
   ["v = 1023", "建議的 validator 數之一；1022 的 rate 會掉到約 1:4.5"],
 ],
 "eqs": [
   ["eq. H.1", "𝒟(v) 的定義與 rate 討論"],
   ["§H", "16-bit GF 的選擇理由與 segment 不需補零的性質"],
 ],
 "asked": [
   ["為什麼是 1/3 就能重建，而不是 1/2？",
    "因為安全假設是「最多不到 1/3 的 validator 作惡或離線」。"
    "門檻設在 1/3 + 1 代表：即使近 2/3 的節點不合作，剩下的誠實節點仍足以還原資料。"
    "這與 assurance 的 > 2/3 表態門檻是同一組假設的兩面。"],
   ["為什麼 validator 數要從特定集合裡選？",
    "rate 只有在 v/3 + 1 剛好整除相關參數時才最佳（6, 9, 15, …, 1023）。"
    "選在這些值上冗餘最小；稍微低於某個值時（如 1022）rate 會明顯變差，白白多存資料。"],
   ["為什麼用 16-bit 而不是 8-bit Galois field？",
    "8-bit 體最多只能有 255 個 shard，撐不起 1023 個 validator。"
    "16-bit 體同時讓 4,104 octet 的 segment 不必補零就能整除，是規模與實作簡潔的折衷。"],
 ],
 "delta": ["0.8.0 的 𝕍 ≡ {3c | c ∈ N_[2,C+1]} 讓較小的 validator set 也合法，別把 1023 寫死"],
 "code": ["解碼函數是 𝓔⁻¹（𝒟 是 shard 數函數，兩個符號別混）；shard 索引與 validator index 的對應要與 assurance 一致"],
},
]
