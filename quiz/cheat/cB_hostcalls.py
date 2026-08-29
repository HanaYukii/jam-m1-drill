# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "B",
 "title": "Host Calls",
 "one": "PVM 與外界的唯一介面。三組呼叫依 invocation 種類分開：通用（gas / fetch / lookup / read / write / info / log）、"
        "refine 專用（historical_lookup、export、machine / peek / poke / invoke 這組 inner PVM）、"
        "accumulate 專用（bless / assign / designate / new / upgrade / transfer / solicit / forget / yield / provide …）。",
 "flow": [
   "呼叫慣例：引數放 φ_7 起的暫存器，回傳值寫回 φ_7；記憶體位址與長度也走暫存器傳",
   "失敗不是 panic，而是把錯誤常數寫進 φ_7 —— 呼叫端必須自己檢查",
   "讀寫記憶體越界回 OOB，不是直接殺掉程式（真正的 page fault 才是退出理由）",
   "refine 能開 inner PVM：machine 建機器、peek / poke 讀寫它的記憶體、invoke 執行、expunge 銷毀",
   "accumulate 的呼叫多半有副作用且受權限限制，權限不足回 HUH",
   "transfer 產生的是 deferred transfer，不會立刻改餘額（見 §12 的 δ‡）",
 ],
 "consts": [
   ["NONE = 2^64−1", "項目不存在"],
   ["WHAT = 2^64−2", "名稱／host call 編號不明"],
   ["OOB = 2^64−3", "記憶體索引不可存取"],
   ["WHO = 2^64−4", "索引不明（service / validator index）"],
   ["FULL = 2^64−5", "儲存已滿或資源已配置"],
   ["CORE / CASH / LOW / HUH", "2^64−6 / −7 / −8 / −9：core 不明、餘額不足、gas 上限太低、操作不合法"],
   ["OK = 0", "一般成功"],
 ],
 "eqs": [
   ["eq. B.1", "Ψ_I : (P, N_C) → (𝔹 ∪ 𝔼, N_G)"],
   ["§B.x Ψ_R / Ψ_A / Ψ_T", "refine / accumulate / on-transfer 三種 invocation 的簽名與可用呼叫集合"],
   ["eq. B.14", "service info 的欄位布局（read / info 類呼叫回傳的東西）"],
 ],
 "asked": [
   ["為什麼錯誤要用 2^64−k 這種魔術數字，不用負數或旗標？",
    "暫存器是無號 64-bit，沒有負數；用最高的幾個值當哨兵，正常回傳（長度、索引、gas）幾乎不可能撞到。"
    "而且錯誤與成功共用同一個暫存器，呼叫慣例只有一條路徑，JIT 也不必為錯誤處理生額外的分支。"],
   ["為什麼 refine 不能改狀態，只有 accumulate 可以？",
    "refine 跑在 core 上、可以被任何人重跑，本質上是純函數；只有純函數才能被 auditor 重跑並比對結果。"
    "一旦讓 refine 改鏈上狀態，重跑就會有副作用，整個 ELVES 的稽核模型就垮了。"
    "所以 refine 只能讀（historical_lookup）與輸出（export）。"],
   ["inner PVM（machine / invoke）是幹嘛用的？",
    "讓一個 service 在 refine 裡跑「別人的程式」，例如 parachain 的 runtime 或 zk 驗證器。"
    "把它做成受控的巢狀 PVM，gas 與記憶體都由外層配額，"
    "比讓 service 自己寫直譯器安全也便宜得多。"],
   ["transfer 為什麼要 deferred？",
    "同一輪 accumulate 裡多個 service 若能即時互轉，結果就依賴執行順序。"
    "改成先收集、後統一以 eq. 12.18 的排序套用，才能保證所有節點得到同一個 δ′。"],
 ],
 "delta": [
   "0.8.0 把 sbrk 改名為 grow_heap；照舊名答會被聽出來",
   "gas 相關呼叫的語意跟著新的 block-level gas model 調整（見附錄 A）",
 ],
 "code": [
   "host call 的 dispatch 表要用 GP 的編號，不能自己排；未知編號一律回 WHAT 而不是 panic",
   "每個呼叫都要先扣自己的 gas 再執行，OOG 的處理與附錄 A 一致（不扣、直接退出）",
 ],
}]
