# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "4",
 "title": "Overview（狀態與轉移）",
 "one": "把整條協定壓成一行：σ′ = Υ(σ, B)。σ 拆成 17 個大致獨立的元件，"
        "每個元件由哪一章負責、讀誰寫誰，是這一章唯一要記牢的東西 —— 也是面試最愛拿來當開場的地圖題。",
 "flow": [
   "α authorizer pool（§8）、φ authorizer queue（§8）",
   "β recent history（§7）、γ Safrole 狀態（§6）、η entropy 四格（§6）",
   "ι 待入 validator、κ 現任 validator、λ 前任 validator（§6 輪替）",
   "ρ availability assignments（§11）、τ 最近 timeslot（§6）",
   "δ service accounts（§9）、χ 特權服務（§12）",
   "ψ disputes 的四個集合（§10）、π 統計（§13）",
   "ω ready queue、ξ accumulated history、θ accumulation output log（§12）",
 ],
 "consts": [
   ["17", "σ 的元件數"],
   ["σ′ = Υ(σ, B)", "整個協定就是這個函數；每一章負責它的一塊"],
   ["prior / posterior", "無撇＝執行前，撇＝執行後；† ‡ 是章內的中間態（ρ†、ρ‡、δ†、δ‡、β†）"],
 ],
 "eqs": [
   ["eq. 4.1–4.4", "B 的組成、σ 的組成與 Υ 的型別"],
   ["§4.9.1", "guaranteeing / assuring / auditing / judging 四階段的原文定義"],
   ["§4.9.2", "in-core 執行要有與 on-chain 相當的 crypto-economic security"],
 ],
 "asked": [
   ["請用一分鐘描述 JAM 的狀態轉移。",
    "從 header 驗簽與 slot 檢查開始；先處理 disputes（ρ†、ψ′），再處理 assurance（ρ‡、可用的報告）、"
    "接著 guarantees 塞入新報告（ρ′）；然後 Safrole 推進 γ / η / κ / λ；"
    "可用的報告進 accumulation 改 δ / χ / ι / φ 並產出 θ；最後更新 β、π。"
    "順序不是任意的：後面每一步都依賴前面產生的中間態。"],
   ["為什麼 σ 要拆這麼多元件，不用一棵大樹就好？",
    "拆開之後每個元件有自己的 state key（附錄 D），修改一個元件只會動到樹上一條路徑，"
    "而且不同章節能各自證明自己的轉移；合成一大坨會讓「這一章到底改了什麼」無法形式化。"],
   ["哪些元件是「每塊都會動」，哪些是「偶爾才動」？",
    "每塊都動：τ、β、η_0、π、ρ（幾乎必動）。"
    "epoch 才動：κ / λ / γ_K / η_1..3。"
    "只有被使用時才動：α / φ、δ / χ / ι、ψ、ω / ξ / θ。面試常從這裡切入問你懂不懂管線。"],
   ["為什麼 disputes 要排在最前面處理？",
    "因為它會清掉 ρ 上的壞 assignment，也會改變 offender 集合。"
    "如果先處理 guarantees，就可能把新報告塞進一個「這一塊稍後才被判定要清空」的 core，"
    "或讓已被剔除的 validator 的簽章被接受。"],
 ],
 "delta": [
   "0.8.0 把 ϑ 改名為 ω，並新增 θ（accumulation output log）作為獨立元件",
   "χ 由 bless 三元組擴成 manager / assigners / delegator / registrar",
 ],
 "code": [
   "internal/state/ — 元件與 state key 的對應表；C(n) 的編號一錯，整個 state root 就錯",
   "建議面試前把「元件 → 章節 → state key → 誰會寫它」做成一張表背下來",
 ],
}]
