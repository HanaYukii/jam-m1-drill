# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "7",
 "title": "Recent History",
 "one": "鏈上保留最近 H = 8 個區塊的摘要 β_H，加上 accumulation output 的 MMR（β_B）。"
        "它讓 §11 能在不翻歷史區塊的情況下做反重複、prerequisite 與 segment-root lookup，也是 BEEFY 對外證明的來源。",
 "flow": [
   "每個 β_H item = (h header hash, s state root, b accumulation-output MMR 的 super-peak, t timeslot, p reported package map)",
   "出塊時 β† ：把上一筆 item 的 state root 用本塊 header 的 H_R 補上（prior state root 的時間差修正）",
   "接著把本塊的新 item append 進去；超過 H = 8 就從頭端丟棄",
   "p = {package hash ↦ segment root}，來自本塊 E_G 的每份報告",
   "β_B 是 accumulation output 的 MMR，append 後取 super-peak 放進 item 的 b",
   "BEEFY（eq. 18.1）簽的是 X_B ⌢ last(β_H)_b，也就是最新的 super-peak",
 ],
 "consts": [
   ["H = 8", "β_H 保留的區塊數；這也是 anchor 能往回指多遠的硬上限"],
   ["L = 14,400", "lookup anchor 能往回指的 slot 數 —— 比 H 大得多，兩者別混"],
   ["C(3)", "β 在狀態樹裡的 key（附錄 D）"],
 ],
 "eqs": [
   ["eq. 7.2", "β_H item 的型別 ⟨h, s, b, t, p⟩"],
   ["eq. 7.5", "β† ：先補上一筆的 state root，再 append 本塊"],
   ["eq. 7.8", "p ≡ {((g_r)_s)_p ↦ ((g_r)_s)_e | g ∈ E_G}"],
   ["§D.1 C(3)", "序列化順序是 ⟨h, b, s, E_4(t), var(p)⟩ —— 與 eq. 7.2 的欄位順序不一致，實作以 D.1 為準"],
   ["eq. 11.36 / 11.41–11.44", "§11 端的四種使用：anchor、反重複、prerequisite、segment-root lookup"],
 ],
 "asked": [
   ["為什麼只留 8 個區塊？多留一點不是更安全嗎？",
    "β 是鏈上狀態，每一筆都要進 Merkle 樹、每個節點都要存。8 個區塊剛好覆蓋 guarantee → assure → accumulate "
    "這條管線的深度加上一點餘裕，足以做反重複；再往前的資料由 lookup anchor（L = 14,400 slot）以「證明」的方式提供，"
    "不必常駐狀態。這是「常駐成本 vs 證明成本」的取捨。"],
   ["β† 這一步在補什麼？為什麼會有時間差？",
    "header 帶的是 prior state root（為了管線化），所以某塊執行完當下，它自己在 β_H 裡那一筆的 state root 還是未知的。"
    "要等下一塊的 header 帶著 H_R 進來，才能回填給上一筆。β† 就是這個回填動作。"
    "實作上最常見的 bug 是先 append 再回填，導致補到剛加進去的那一筆身上。"],
   ["p（reported package map）為什麼要上鏈？",
    "§11 每塊都要檢查「這個 package 是不是最近報過了」「prerequisite 指到的 package 存不存在」"
    "「segment-root lookup 的值對不對」。如果不上鏈，就得去解碼最近 8 個區塊的 extrinsic 才能回答，"
    "那會讓狀態轉移依賴區塊體而不只是狀態，違反 STF 的封閉性。"],
   ["為什麼 accumulation output 要做成 MMR，不是普通 Merkle 樹？",
    "MMR 只 append 不改寫，新增一筆的成本是 O(log n) 且舊的證明依然有效。"
    "對「持續產出、外部要長期驗證」的 accumulation output 而言，這正好；"
    "普通 Merkle 樹每次加葉子都要重算整棵樹，舊證明全部失效。"],
 ],
 "delta": [
   "0.8.0 的 β_H item 多了 4-byte 的 timeslot 欄位（0.7.2 沒有）",
   "b 欄位存的是 accumulation-output MMR 的 super-peak，BEEFY 直接對它簽名",
 ],
 "code": [
   "internal/types/encode.go 的 BlockInfo.Encode 要照 §D.1 的 ⟨h, b, s, t, p⟩ 順序，不是 §7.2 的文字順序",
   "internal/.../recent_history_controller.go — beefyBelt / BeefyRoot 就是 β_B 與 super-peak",
 ],
}]
