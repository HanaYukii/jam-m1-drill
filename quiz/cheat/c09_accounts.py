# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "9",
 "title": "Service Accounts",
 "one": "δ 裡的每個 service 就是一個帳戶：一份 code、一份 storage、一組 preimage、餘額與兩個 gas 上限。"
        "重點在「什麼東西是存起來的、什麼是推導出來的」，以及 preimage 的四階段生命週期。",
 "flow": [
   "帳戶欄位：storage s、preimages p、lookup meta l、code hash c、balance b、accumulate gas g、on-transfer gas m",
   "另有計數類欄位（item 數、octet 數、threshold）——它們是可推導的，序列化時放在 C(255, s) 的 info 裡",
   "threshold balance：帳戶餘額必須 ≥ 由 storage 與 preimage 用量算出的押金，否則不能再寫入",
   "storage 每一項的計價是 34 + |key| + |value| octets（eq. 9.8）",
   "preimage 生命週期看 l[(h, z)] 的形狀：[] = 已請求未提供、[x] = 自 x 起可用、[x, y] = 於 y 被遺忘、[x, y, z] = 遺忘後又被請求",
   "forget 之後要等 D 個 slot 才真正 expunge（D ≡ L + 4,800 = 19,200），期間資料仍可被 lookup",
   "service index 由 check() 推導並避開既有索引；registrar χ_R 負責新服務的註冊範圍",
 ],
 "consts": [
   ["34 + |k| + |v|", "單筆 storage 的押金計價（含 key 長度，別只算 value）"],
   ["D = 19,200", "preimage 從 forget 到 expunge 的延遲（= L + 4,800 slot）"],
   ["L = 14,400", "lookup anchor 的回溯上限；D 比它大是刻意的"],
   ["C(255, s)", "service info 在狀態樹裡的 key 形狀"],
 ],
 "eqs": [
   ["eq. 9.3", "帳戶的欄位與型別"],
   ["eq. 9.8", "storage 用量與 threshold balance 的計算"],
   ["eq. 9.9–9.10", "Ω_W（write）與 Ω_F（forget）的狀態轉移；餘額不足時 s′ = s 且回傳 FULL"],
   ["§D.2", "service 的 storage / preimage / lookup 各自的 state key 建構"],
 ],
 "asked": [
   ["為什麼 forget 不是立即刪除，要等 D 個 slot？",
    "因為 refine 可以用 lookup anchor 回看 L = 14,400 slot 之內的 preimage。"
    "如果 forget 立刻生效，一份還在有效 anchor 範圍內的 work-package 就會突然變成無法重現，"
    "auditor 也就無法重跑驗證。D > L 保證「只要 anchor 還有效，資料就一定還在」。"],
   ["threshold balance 的意義是什麼？餘額掉到門檻以下會怎樣？",
    "它是狀態租金的押金化：你占用多少鏈上空間，就得押多少錢。"
    "掉到門檻以下不會被自動清除，而是「不能再增加占用」——寫入直接失敗回 FULL。"
    "這讓失敗是可預期的、局部的，不需要任何全域的垃圾回收流程。"],
   ["哪些欄位是存的、哪些是算的？為什麼要區分？",
    "storage、preimages、lookup meta、code hash、balance、兩個 gas 上限是真正存的；"
    "item 數、octet 數、threshold 是從前者推導的。區分的理由是狀態樹只該存最小充分集合，"
    "推導值若也存起來就可能與本體不一致；但序列化時為了讓讀取端不必掃全部 storage，會把它們一起寫進 info。"],
   ["誰能改一個 service 的什麼？",
    "service 只能改自己的 storage 與 preimage（透過自己的 accumulate）；"
    "code hash、gas 上限這類設定要由自己或有權限的特權服務改；"
    "0.8.0 之後只有 manager χ_M 能改 bless 設定，assigners χ_A 改 authorizer queue，registrar χ_R 管新服務。"],
 ],
 "delta": [
   "0.8.0 把 bless 的修改權收斂到 manager，且 new service 可帶 gratis 額度",
   "帳戶欄位在 0.8.0 有調整，別直接照 0.7.2 的欄位表背；info 的序列化內容也跟著變",
 ],
 "code": [
   "CalcStorageItemFootprint / CalcOctets — 註解寫成只算 value，實際程式碼算 34+key+value（程式碼才對）",
   "issue #979 / #980 就是這一塊的計價與 FULL 回傳",
 ],
}]
