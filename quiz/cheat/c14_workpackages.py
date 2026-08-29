# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "14",
 "title": "Work Packages & Reports",
 "one": "鏈下的資料格式與 refine 的輸入輸出：work-package 帶著 authorizer 與若干 work-item 進 core，"
        "refine 後產出 work-report；中間的 import / export segment 與 paged proof 是可得性系統的實際負載。",
 "flow": [
   "work-package ⟨j auth token, h host service, u auth code hash, f auth config, c refinement context, w items⟩",
   "每個 work-item 指定 service、payload、gas 上限，以及它要 import 的 segment 與會 export 幾個 segment",
   "guarantor 先跑 Ψ_I（用 u / f / j 決定授權），再對每個 item 跑 Ψ_R（refine）",
   "refine 的輸出組成 work-report 的 results；avspec (p, l, u, v, e, n) 描述 bundle 與 segment 的可得性參數",
   "bundle = work-package + 所有 extrinsic + 所有 import segment 的證明，這才是被 erasure code 的東西",
   "export segment 被組成 segment tree，其 root（e）進 avspec，供下游 package 以 lookup 取用",
   "paged proof：把 segment 以固定頁大小分組做證明，讓 importer 只需拉一頁而不是整棵樹",
 ],
 "consts": [
   ["4,104", "segment 大小（octet）；erasure coding 的 6 路資料平行度由它與 1023 推出"],
   ["W_R / W_B / W_G", "report 結果、bundle、總量的大小上限"],
   ["avspec = (p, l, u, v, e, n)", "package hash、bundle 長度、erasure root、shard 數、segment root、segment 數"],
   ["refinement context (a, n, s, b, l, t, r, p)", "anchor 與 lookup anchor 相關的八個欄位"],
 ],
 "eqs": [
   ["eq. 14.2", "work-package 的六個欄位"],
   ["eq. 14.11", "authorizer code 由 Λ(δ[p_h], (p_c)_t, p_u) 取得 —— 用的是 context 的 lookup anchor timeslot"],
   ["eq. 14.12", "paged proofs 函數 P（注意 GP 用的符號與 §D 的 P 不同義）"],
   ["eq. 14.19", "零填充 𝒫_n：把資料補到頁邊界"],
 ],
 "asked": [
   ["為什麼要區分 import segment 和 extrinsic？",
    "extrinsic 是 package 自帶的資料，作者說了算；import segment 是「別人先前 export 出來的」資料，"
    "必須用 segment root 證明它確實來自某個已被報告的 package。"
    "兩者的信任模型不同：前者只要跟著 bundle 一起可得，後者還要能被追溯到鏈上的 segment root。"],
   ["paged proof 解決什麼問題？",
    "一個 package 可能 export 上千個 segment。若下游只要一個 segment 卻得拉整棵樹的證明，頻寬會爆。"
    "分頁之後 importer 拉「該 segment 所在的那一頁 + 一條到 root 的路徑」就夠了，"
    "代價是頁內的 segment 綁在一起 —— 這是常見的空間 / 頻寬取捨題。"],
   ["為什麼 bundle（而不是 work-report）才是被 erasure code 的東西？",
    "auditor 要重跑 refine，就必須拿到 refine 的完整輸入：package、extrinsic、import segment 及其證明。"
    "work-report 只是輸出摘要，拿到它無法重現計算。所以可得性保的是輸入，不是輸出。"],
   ["refinement context 的 anchor 和 lookup anchor 差在哪？",
    "anchor 指的是「這個 package 基於哪個近期區塊的狀態」，受 §7 的 H = 8 限制，由 eq. 11.36 對著 β† 驗證；"
    "lookup anchor 決定「preimage 要用哪個時間點的可見性」，可回溯 L = 14,400 slot。"
    "把兩者混為一談是很典型的失分點。"],
 ],
 "delta": [
   "refinement context 在 0.8.0 是八欄（a, n, s, b, l, t, r, p），別照 0.7.2 的六欄背",
   "avspec 的 segment root 欄位是 e（s 是整個 avspec，也是 service storage 的符號，容易撞）",
 ],
 "code": [
   "makeBundle / paged proof 的實作要注意零填充與頁邊界，差一個 byte 整個 erasure root 就不同",
   "⚠ merkle_tree.T 用 len(v)/2 切，GP eq. E.1 的 N 是 ⌈|v|/2⌉；ce140.go 對未補齊的 chunk slice 呼叫 T 會產生錯的 co-path",
 ],
}]
