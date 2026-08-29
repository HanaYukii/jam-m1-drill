# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "D",
 "title": "State Merklization",
 "one": "σ 怎麼變成一個 32-byte 的 state root：先把每個狀態元件序列化並算出它的 state key，"
        "再把 (key, value) 放進一棵固定 64-byte 節點的二元 Patricia trie。key 的建構規則是這一章的重點。",
 "flow": [
   "章節級元件用 C(n)：α = C(1)、β = C(3)、γ = C(4)…（編號錯了 root 就錯）",
   "service 的資料用 C(s, ·) 的交錯規則：service index 與 hash 交錯成 31 bytes 的 key",
   "service 的三類子項用不同標記：storage、preimage、lookup 各有自己的前綴（E_4(2^32−1) / E_4(2^32−2) / E_4(l)）",
   "節點固定 512 bit = 64 bytes：第 1 個 bit 分 branch / leaf，第 2 個 bit 分 embedded-value leaf / regular leaf",
   "embedded-value leaf：首位元組低 6 bits 存值長度（≤ 32），接 31 bytes key，最後 32 bytes 是值（不足補零）",
   "regular leaf：低 6 bits 歸零，接 31 bytes key，最後 32 bytes 存值的 hash",
   "走 trie 時 key 展開成位元流是 MSB-first（與附錄 C 的 LSB-first 打包相反）",
 ],
 "consts": [
   ["64 bytes", "節點固定大小；1 + 31 + 32 的佈局讓 key 恰好 31 bytes"],
   ["32", "embedded value 的長度上限；33 bytes 起改存 hash"],
   ["0xA0 / 0xC0", "32-byte 值的 embedded leaf 首位元組 / regular leaf 首位元組"],
   ["MSB-first", "trie 走訪的位元順序"],
 ],
 "eqs": [
   ["§D.1", "C(n) 與各章節元件的對應表；C(3) 的 β item 是 ⟨h, b, s, E_4(t), var(p)⟩"],
   ["§D.2", "service 子項的 key 建構（交錯規則）"],
   ["§D.2.1", "節點編碼：branch / embedded leaf / regular leaf 三種"],
 ],
 "asked": [
   ["為什麼 key 是 31 bytes 而不是 32？",
    "節點要塞進固定的 64 bytes：1 byte 標頭 + 31 bytes key + 32 bytes 值/雜湊 = 64。"
    "固定大小讓節點可以直接以陣列索引存取、無需長度前綴，也讓證明大小完全可預測。"
    "代價是 key 只有 248 bit —— 對狀態樹的碰撞安全仍綽綽有餘。"],
   ["為什麼要有 embedded-value leaf 這種東西？",
    "大多數狀態值（餘額、索引、小型 metadata）都不到 32 bytes。"
    "直接內嵌可以省掉一次 hash 與一次額外的資料庫查詢，"
    "而超過 32 bytes 就退回存 hash，證明大小仍然有界。"],
   ["state key 為什麼要把 service index 和 hash 交錯，不用簡單串接？",
    "交錯讓同一個 service 的資料在 trie 上不會全部擠在同一條子路徑上，"
    "避免某個熱門 service 讓樹嚴重不平衡、證明變長；同時也讓不同 service 的資料自然分散。"],
   ["state root 為什麼要能增量計算？",
    "每塊只有少數元件改變。若每次都重建整棵樹，出塊時間會被 hash 吃光。"
    "節點編碼與合併順序被定義成與插入順序無關，才能只沿著被改動的路徑往上重算。"
    "實作若把葉子的合併順序搞錯，單獨測試可能過，但跟別人算出來的 root 不一樣。"],
 ],
 "delta": [
   "0.8.0 的 C(10)（ρ）現在存完整的 guarantee（含 credentials）——PR #494",
   "key 建構規則本身在 0.7.2 → 0.8.0 沒有改；別把「欄位變了」誤當成「規則變了」",
 ],
 "code": [
   "state_key_constructor.go — 交錯規則用 Blake2bHashPartial(h, 27)，與 GP 一致",
   "partitionByBit / merklizeWithCache — 位元判斷是 MSB-first，跟附錄 C 的打包方向相反，別共用同一個 helper",
 ],
}]
