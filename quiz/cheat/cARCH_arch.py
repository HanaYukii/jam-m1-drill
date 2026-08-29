# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "ARCH",
 "title": "架構與設計理由",
 "one": "JAM = 一條「不做通用計算」的中繼鏈，只負責排序、資料可得性與最終性；"
        "真正的計算被推到 341 個 core 上平行執行，靠 guarantee（質押）＋ availability（分片）＋ auditing（重跑）"
        "三段接力換取安全，最後才把結果 accumulate 進鏈上狀態。",
 "flow": [
   "使用者／builder 組出 work-package（含 authorizer、context、若干 work-item）",
   "core 上的 3 個 guarantor 跑 is-authorized → refine，產出 work-report 並連署上鏈（§11）",
   "bundle 被 erasure code 成 shard 發給全體 validator，> 2/3 表態持有即 available（§11）",
   "ELVES：隨機抽出的 auditor 重建 bundle、重跑 refine，結果不符就升級為爭議（§18 auditing）",
   "available 的 report 進 accumulate，才真正改動鏈上狀態 δ（§12）",
   "爭議走 disputes 上鏈定案，罰沒與剔除（§10）；BEEFY 提供對外的最終性證明（§18）",
   "整條路徑是三段管線：本塊 guarantee、下塊 assure、再下塊 accumulate —— 所以延遲是可預期的常數",
 ],
 "consts": [
   ["6 秒 / slot、600 slot / epoch", "一個 epoch 一小時；validator 輪替與 entropy 輪替都以 epoch 為界"],
   ["C = 341 core、每 core 3 guarantor", "1023 個 validator 剛好三等分；也是 1/3 惡意假設的來源"],
   ["每 report 約 30 次 audit", "平均每 validator 每 slot 10 次 audit 推出來的數字（§21 討論）"],
   ["1/3 門檻家族", "guarantor 3 選 2、assurance > 2/3、verdict ⌊2|k|/3⌋+1 或 ⌊|k|/3⌋ —— 同一套假設的不同投影"],
 ],
 "eqs": [
   ["§4.9.1", "「a crypto-economic game of three stages called guaranteeing, assuring, auditing」——四階段合起來的原句"],
   ["§4.9.2", "in-core 執行要達到與 on-chain 相當的 crypto-economic security"],
   ["§1.2–1.3", "設計目標：resilient、generic、performant，以及不做通用 on-chain 計算的取捨"],
   ["§21", "throughput 的推導：341 work-package / slot 的來源"],
 ],
 "asked": [
   ["JAM 跟 Polkadot、Ethereum 的關鍵差別是什麼？",
    "Polkadot 的 parachain 是「有身分的插槽」，要拍賣、要治理；JAM 的 core 是無身分的計算資源，任何人付 gas 都能用。"
    "Ethereum 把所有計算放在單一 on-chain 環境；JAM 把計算推到 in-core，鏈上只留 accumulate。"
    "結果是 JAM 沒有 parachain 概念、也沒有全域 EVM，而是「service + core time」的模型。"],
   ["為什麼需要 availability 和 auditing 兩層，只有一層不行嗎？",
    "只有 availability：資料在，但沒人檢查算得對不對，guarantor 可以直接報假結果。"
    "只有 auditing：想查也查不到資料——惡意 guarantor 只要不給 bundle，auditor 就無法重跑，也無法證明對方藏資料。"
    "先強制資料可得（分片＋2/3 表態），再讓隨機 auditor 重跑，兩者相乘才讓「說謊且不被抓」的機率降到可忽略。"],
   ["為什麼 header 帶的是 prior state root，不是 posterior？",
    "posterior root 要等本塊執行完才算得出來，出塊者就必須在極短時間內跑完整個 STF 才能簽章。"
    "改成帶 prior root，出塊、驗證、狀態計算就能管線化 —— 代價是驗證某塊的狀態要等下一塊的 header。"],
   ["service 跟 parachain 在心智模型上怎麼對應？",
    "一個 service 大致等於「一段 refine 程式碼 + 一段 accumulate 程式碼 + 一份狀態」。"
    "parachain 可以實作成一個 service，但 service 更小也更自由：它不綁定 core、不需要插槽，"
    "只要有人願意付 core time 並帶對 authorizer，就能被執行。"],
 ],
 "delta": [
   "0.8.0 的特權服務由 bless 三元組擴成 χ_M / χ_A / χ_V / χ_R 四個角色",
   "PVM gas model 改為 block-level 預扣（附錄 A）",
   "ready queue ϑ → ω；ρ 改存完整 guarantee；refinement context 欄位擴充",
 ],
 "code": [
   "面試會問「你們實作到哪、哪裡跟 GP 不一致」——先準備好 0.7.2 → 0.8.0 的差異清單與你們的遷移計畫",
   "已知兩處值得主動提：merkle_tree.T 的 ⌊|v|/2⌋ 應為 ⌈|v|/2⌉；Δ* 的 transfer 需依 eq. 12.18 的 s ↕ s 穩定排序",
 ],
}]
