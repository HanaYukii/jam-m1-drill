# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "13",
 "title": "Statistics",
 "one": "鏈上記帳：π = (π_V, π_L, π_C, π_S)，分別是本 epoch 的 validator 計數、上一個 epoch 的快照、"
        "每 core 的用量與每 service 的用量。它不影響共識規則，但是獎勵與監測的唯一事實來源，也是最容易寫錯的一章。",
 "flow": [
   "π_V 是本 epoch 進行中的計數；epoch 邊界時 π_L ← π_V、π_V 歸零",
   "每個 validator 六個計數：b 出塊數、t ticket 數、p preimage 數、d preimage octets、g guarantee 數、a assurance 數",
   "b / t / p / d 記在「author」身上，也就是 H_I 指到的那個人",
   "g 記在 guarantee 的「簽署者」身上（從 credential 裡的 Ed25519 key 反查），不是 author",
   "a 記在 assurance 的簽署者身上（用 assurance 的 ValidatorIndex）",
   "π_C 每 core 記 import / extrinsic / export / bundle / gas 等用量；π_S 每 service 記各自的累計",
 ],
 "consts": [
   ["6", "每個 validator 的計數欄位數 (b, t, p, d, g, a)"],
   ["E = 600", "epoch 長度；π_V → π_L 的搬移點"],
   ["C(13)", "π 在狀態樹裡的 key"],
 ],
 "eqs": [
   ["eq. 13.1–13.2", "π 的組成與 (π_V, π_L) ∈ ⟦(b, t, p, d, g, a)⟧²"],
   ["eq. 13.4", "π_V†[v]_a = π_V[v]_a + (∃a ∈ E_A : a_v = v) —— assurance 是「存在性」判斷，每人每塊最多 +1"],
   ["eq. 13.5", "epoch 邊界的搬移條件（e′ = e 時不動）"],
   ["eq. 13.6", "author 那組計數：b += 1、t += |E_T|、p += |E_P|、d += Σ|d|"],
 ],
 "asked": [
   ["為什麼 assurance 是「每人每塊最多 +1」，不是按 core 數加？",
    "一個 validator 每塊只送一次 assurance，裡面的 bitfield 可能同時表態幾百個 core。"
    "統計要記的是「他有沒有盡到這個 slot 的責任」，不是他持有多少 shard；"
    "若按位元數加，持有較多 shard 的節點會被系統性高估。"],
   ["為什麼 guarantee 記在簽署者、preimage 記在 author？",
    "guarantee 是連署行為，功勞屬於實際簽名的 guarantor（可能有兩三個，都要加）；"
    "preimage 是 author 把它打包進區塊的貢獻，跟誰產生 preimage 無關。"
    "這也是實作最常搞混的地方：把 g 記給 author 會讓統計整組偏掉。"],
   ["ticket 為什麼記給 author，而不是產生 ticket 的人？",
    "ring VRF 的重點就是匿名——鏈上根本不知道 ticket 是誰產的。"
    "eq. 13.6 因此把 |E_T| 記給 H_I，這是「打包進區塊」的貢獻計數，不是「產生」的計數。"],
   ["統計寫錯會怎樣？它不影響共識吧？",
    "π 是狀態的一部分，會進 Merkle 樹。算錯不會讓區塊「邏輯上」失敗，"
    "但 state root 會與其他實作不一致 —— 也就是說，它照樣會讓你分叉。"
    "這是為什麼統計題在 conformance 測試裡權重不低。"],
 ],
 "delta": [
   "0.7.0 修過「每個 validator 只算一次」的 assurance 計數（issue #710）",
   "#869 修 guarantee 計數的歸屬；照舊版寫法會把 g 加到錯的人身上",
 ],
 "code": [
   "statistics.go — UpdateTicketStatistics / UpdatePreimageStatistics / UpdateReportStatistics / UpdateAvailabilityStatistics",
   "UpdateReportStatistics 要用 reporters set（credential 裡的 Ed25519 key 是否在 κ′ 內），不是 author index",
 ],
}]
