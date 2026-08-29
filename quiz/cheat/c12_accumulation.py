# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "12",
 "title": "Accumulation",
 "one": "把已 available 的 work-report 依 dependency 解鎖，排成序列後逐 service 呼叫 accumulate，"
        "在 gas 上限內產出新的 δ / χ / ι / φ 與本塊 output log θ。這是 JAM「鏈上」真正改狀態的唯一入口。",
 "flow": [
   "R = 本塊剛變 available 的 reports（來自 ρ‡ 被 assurance 清掉的那些）",
   "R! = 無 prerequisite 且 l = ∅ → 立刻可累積；R^Q = 其餘進佇列",
   "ω（ready queue，長度 E 的環狀緩衝）存「已 available 但依賴未滿足」的 (report, 未滿足依賴集)",
   "ξ（accumulated history，長度 E）存過去每個 slot 累積過的 package hash，用來解鎖與擋重複",
   "R* = Q(ω 由舊到新展開) ⌢ R!　→ 這就是本塊要餵給 Δ 的序列",
   "Δ+ 依 gas 上限決定「這塊能吃幾個」→ Δ* 對單一 service 跑一輪 → Δ1 真正呼叫 PVM 的 accumulate",
   "δ† → δ‡ → δ′：deferred transfer 在 δ‡ 之後才套用；θ′ 收 (service, hash) 的 output log",
 ],
 "consts": [
   ["E = 600", "ω 與 ξ 的長度＝一個 epoch 的 slot 數"],
   ["G_A / G_T / G_I", "單次 accumulate 上限 / 整塊總 gas / is-authorized 上限；Δ+ 用的是總量門檻"],
   ["χ_M / χ_A / χ_V / χ_R", "manager / assigners / delegator / registrar 四個特權 service（0.8.0 的 χ 形狀）"],
   ["χ_Z", "always-accumulate 集合：即使本塊沒有 report 也會被呼叫，帶各自的 gas 配額"],
 ],
 "eqs": [
   ["eq. 12.1–12.3", "ξ ∈ ⟦{H}⟧_E、ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E 的型別與長度"],
   ["eq. 12.4–12.6", "R! / R^Q / R* 三段切法與 Q 函數（依賴解鎖）"],
   ["eq. 12.18", "deferred transfer 要以 s ↕ s 排序後處理 —— 不是 map 迭代順序"],
   ["eq. 12.24", "(n, e′, b, u, t) ≡ Δ+(g, [], R*, e, χ_Z)；θ′ 取 Δ+ 回傳的 output log"],
 ],
 "asked": [
   ["為什麼要 ω / ξ 兩個環狀緩衝，不能只用一個集合？",
    "ξ 是「已累積」的歷史，用來擋重複與解鎖依賴；ω 是「已 available 但還不能累積」的待辦。"
    "兩者都做成長度 E 的環，是為了讓過期自動掉出去、狀態有界，且 O(1) 就能回答「這個 package 最近累積過沒」。"],
   ["Δ+ / Δ* / Δ1 為什麼要分三層？",
    "Δ1 = 對單一 service 呼叫 PVM 的 accumulate（真正執行）；Δ* = 把同一輪裡每個 service 各跑一次並合併狀態；"
    "Δ+ = 在 gas 上限下決定「這一塊到底能吃 R* 的前幾個」，回傳吃掉的個數 n。分層是為了讓 gas 上限的截斷只發生在最外層，內層保持純函數。"],
   ["accumulate 失敗（panic / OOG）會怎樣？",
    "該 service 這一輪的狀態變更整批丟棄，但 report 仍算「已累積」進 ξ，不會無限重試；"
    "gas 照扣（block-level 預扣），output log 記空。這是刻意的：否則一個壞 service 可以卡住整條鏈。"],
   ["為什麼 deferred transfer 要另外一個 δ‡ 階段？",
    "accumulate 期間 service 之間若能直接互改餘額，結果就會依賴執行順序。"
    "先全部收集成 transfer，再以固定排序統一套用，才能讓所有節點得到相同的 δ′。"],
 ],
 "delta": [
   "ready queue 由 0.7.2 的 ϑ 更名為 ω（state key 與型別都沒動），為了不跟 output log θ 撞符號",
   "χ 由單純 bless 三元組擴成 manager / assigners / delegator / registrar 四個角色，且只有 manager 能改 bless",
   "accumulate 的 gas 改成 block-level 預扣（見附錄 A 的 0.8.0 gas model）",
 ],
 "code": [
   "internal/accumulate/ — Δ+/Δ*/Δ1 的對應實作；注意 Vartheta 欄位就是 ω",
   "⚠ 團隊實作用 Go map 迭代順序處理 transfer，eq. 12.18 要求 s ↕ s 排序，且 sort.Slice 不穩定 → state root 可能分歧",
 ],
}]
