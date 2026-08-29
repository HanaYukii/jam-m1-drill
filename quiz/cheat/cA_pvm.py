# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "A",
 "title": "PVM (Polka Virtual Machine)",
 "one": "JAM 的確定性執行引擎：RISC-V RV64EM 子集、13 個暫存器、分頁式 RAM，"
        "以 basic block 為單位「預先」扣 gas。所有 service 的 refine / accumulate / on-transfer 都跑在它上面。",
 "flow": [
   "程式 blob 解出三段：唯讀資料、可寫資料（含 heap）、程式碼＋jump table；標準初始化把它們鋪進 2^16 對齊的區段",
   "執行狀態 = (ı 指令指標, φ 13 個暫存器, μ 記憶體, ϱ gas counter, 以及 0.8.0 新增的 gas-charged flag)",
   "每個 basic block 進入時（第一步、跳進新 block、跳回本 block 開頭）先扣整塊的 ϱ^Δ；不夠就 ∞ 退出且 gas 不動",
   "單步 Ψ_1 回傳 continue / halt / panic / OOG，或 (page-fault, 位址) / (host-call, 編號)",
   "host call 中斷後可續跑，gas-charged flag 保證同一個 block 不會被重複收費",
   "四種對外呼叫：Ψ_I is-authorized、Ψ_R refine、Ψ_A accumulate、Ψ_T on-transfer，各有自己的 gas 上限與可用 host call 集合",
 ],
 "consts": [
   ["13", "暫存器數量 φ ∈ ⟦N_R⟧_13（RV64E 的 16 個扣掉三個）"],
   ["Z_P = 2^12", "記憶體分頁大小；page fault 回報的是對齊到分頁的位址"],
   ["Z_I = 2^16", "標準程式初始化的區段對齊單位"],
   ["ϱ^Δ = max(cycles − 3, 1)", "basic block 的 gas 價格，cycles 由 §A.9 的亂序 CPU 模擬算出"],
   ["ROB = 32", "微架構模擬的 reorder buffer 上限；4 decode slots、5 issue starts"],
 ],
 "eqs": [
   ["eq. A.5–A.8", "單步語意與 gas 不足時的 (∞, ϱ, ⊥)：OOG 時 gas counter 原封不動"],
   ["eq. A.54", "ϱ^Δ = max(cycles_final − 3, 1)"],
   ["§A.3", "basic block 邊界＝terminator（trap / fallthrough / jump / jump_ind / load_imm_jump(_ind) / 所有 branch_*）之後"],
   ["§A.10", "每條指令的 cycles / decode slots / execution units 表 —— 那是餵給模擬器的，不是 gas"],
 ],
 "asked": [
   ["為什麼是 block-level 預扣，而不是每條指令扣？",
    "每條指令扣的話，直譯器每一步都要動 gas counter，也擋不掉 JIT——編譯後的原生碼沒有「一條指令」的概念。"
    "整個 basic block 一次扣清，JIT 只要在 block 入口插一次檢查就完全等價，效能差好幾倍，"
    "而且 block 的成本是靜態可算的，不同實作能得到位元一致的結果。"],
   ["為什麼 OOG 時 gas counter 不扣？",
    "因為這塊根本沒執行。若扣了，餘額會變負或需要飽和處理，兩者都會讓不同實作在邊界上分歧；"
    "保持不動則「退出時的 ϱ」有唯一定義，也讓上層能精確知道還剩多少。"],
   ["為什麼用 RISC-V 而不是 WASM 或 EVM？",
    "RISC-V 的指令集小、暫存器機、沒有隱藏控制流，容易做確定性的 gas 計價與 JIT；"
    "WASM 的結構化控制流與 host 綁定太肥、實作間差異大；EVM 的 256-bit 字長與 stack 機在現代 CPU 上代價高。"
    "PVM 再往下砍：no floating point、no dynamic linking，換來跨實作可重現。"],
   ["page fault 為什麼要當成一種「退出理由」，而不是直接 panic？",
    "refine 需要按需載入 import segment，accumulate 需要按需取 storage。"
    "把 fault 做成可回復的退出，host 就能把資料填進那一頁再續跑，"
    "避免一開始就把所有可能用到的資料塞進記憶體（那會讓 work-package 大到不可行）。"],
 ],
 "delta": [
   "gas model 是 0.8.0 最大的改動（PR #508）：0.7.2 是每指令 1 gas，0.8.0 改成 block-level 預扣 max(c−3,1)",
   "新增 gas-charged flag 作為 Ψ 的 bool 參數，處理 host call 中斷後續跑不重複收費",
   "記憶體存取模式維持 ∅ / R / W 三種；別把它跟 0.7.x 的舊命名混用",
 ],
 "code": [
   "internal/pvm/ — 團隊實作目前是 GasCost = InstrCount（0.7.2 語意），對應 issue #1046，需整段重寫",
   "重寫時注意：ϱ^Δ 要能靜態算出來並快取在 block 表上，否則每次進 block 都跑一次模擬會很慢",
 ],
}]
