# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "6",
 "title": "Safrole",
 "one": "決定「每個 slot 由誰出塊」。用 ring VRF 讓 validator 匿名投票券（ticket）進來，"
        "epoch 結束前抽出 E 張、以 Z 函數重排成 slot-sealer 序列 γ_S；票不夠就 fallback 成公鑰輪流。",
 "flow": [
   "validator 用 bandersnatch ring VRF 產 ticket，證明自己屬於 γ_K 但不洩漏是誰",
   "ticket 進 extrinsic E_T → 累積在 γ_A（accumulator，上限 E 張，依 ticket id 排序保留最小的）",
   "epoch 邊界（e′ ≠ e）：κ′ ← γ_K、γ_K ← ι、λ′ ← κ，四組 validator set 整體輪一格",
   "γ_S 的決定：γ_A 滿 E 張 → Z(γ_A) 外洗牌；否則 fallback F(η′_2, κ′) 用公鑰",
   "出塊時 H_V 要對得上 γ_S[H_T mod E]；H_S 是 seal，H_E 是 entropy source",
   "η 四格輪替：η′_0 由 H_V 累積，η′_1←η_0、η′_2←η_1、η′_3←η_2 只在 epoch 邊界發生",
 ],
 "consts": [
   ["E = 600", "一個 epoch 的 slot 數，也是 ticket 目標張數與 γ_A 容量"],
   ["Y = 500", "ticket 提交截止 slot；之後的 E_T 不再收（保證抽籤前有安定期）"],
   ["N = 2", "每個 validator 每 epoch 最多 2 張 ticket entry index（i_e ∈ {0,1}）"],
   ["K = 16", "單塊 E_T 最多 16 張票"],
 ],
 "eqs": [
   ["eq. 6.8", "𝕍 ≡ {3c | c ∈ N_[2,C+1]} —— validator 數必須是 3 的倍數"],
   ["eq. 6.22", "η ∈ ⟦H⟧_4，四格 entropy 的型別"],
   ["eq. 6.25", "γ′_S 的三分支：epoch 未換就保持 γ_S；換了且票滿用 Z；票不足用 fallback"],
   ["eq. 6.27", "Z(γ_A)：outside-in 重排，讓相鄰 slot 的出塊者在 accumulator 裡距離最遠"],
 ],
 "asked": [
   ["為什麼要 ring VRF，不能用普通 VRF？",
    "普通 VRF 的證明會綁定公鑰，等於提前公告「第 N 個 slot 是我出」，讓攻擊者能針對性 DoS 或賄賂。"
    "ring VRF 只證明「我屬於這個 ring」，直到出塊那一刻才揭露身分。GP 0.8.0 的行文只講 anonymity，DoS/賄賂是 Sassafras 論文的動機。"],
   ["票不足時的 fallback 有什麼安全代價？",
    "fallback 直接用 η′_2 對 κ′ 洗牌，出塊順序在 epoch 一開始就公開可算 —— 匿名性歸零。"
    "這是刻意的可用性優先：寧可退化也不要停鏈。所以 Y = 500 的截止設計就是為了盡量不走到這條路。"],
   ["為什麼用 η′_2 而不是 η′_0 來抽籤？",
    "η′_0 是本 epoch 還在累積的熵，出塊者能用「要不要出這塊」來影響它。"
    "退兩格取 η′_2 表示抽籤所依據的隨機數在兩個 epoch 前就凍結了，操縱成本高到不划算。"],
   ["Z 的 outside-in 重排在防什麼？",
    "γ_A 是依 ticket id 排序的。如果直接照序當出塊順序，同一個人手上的兩張票很可能落在相鄰 slot，"
    "形成連續出塊、方便做短鏈重組。outside-in 把序列首尾交錯，讓 id 相近的票在時間上被拉開。"],
 ],
 "delta": [
   "ticket entry index 在 0.8.0 明確寫成 i_e（0.7.x 文獻常寫成 r），型別 N_N",
   "γ 的四個欄位在 0.8.0 定名為 γ_K / γ_Z / γ_S / γ_A（ring root 落在 𝔹_144，不是 𝕐_144）",
 ],
 "code": [
   "internal/safrole/ — ticket 驗證、γ_A 的排序插入、Z 重排、fallback",
   "測試向量 safrole/ 的 tiny 版本 E 與 validator 數都不同，別把 600 / 1023 寫死",
 ],
}]
