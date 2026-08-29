# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "5",
 "title": "The Header",
 "one": "區塊的「可獨立驗證」摘要：只看 header 就能驗簽、定位時間、確認 extrinsic 內容，"
        "並在 epoch 邊界宣告新的 validator set 與抽籤結果。header 帶的是 prior state root，這是整條管線化設計的關鍵。",
 "flow": [
   "H_P parent hash、H_R prior state root、H_X extrinsic hash 三者釘住鏈的結構",
   "H_T timeslot 決定 epoch/slot 與該由誰出塊；H_I author index 指向 κ′ 裡的位置",
   "H_V 是 VRF 輸出（entropy source），累積進 η′_0；H_S 是對 header 的 seal 簽章",
   "H_E epoch marker：epoch 邊界時宣告下一組 validator 的 bandersnatch key 與 entropy",
   "H_W winning tickets：抽籤成功時宣告本 epoch 的 ticket 序列（票不足則不出現）",
   "H_O offenders：本塊新增的 offender key（來自 §10 的 culprits/faults）",
   "驗證順序：先確認 H_T 對應的 slot sealer 是 H_I、再用該 key 驗 H_S 與 H_V，最後才談內容",
 ],
 "consts": [
   ["H_S / H_V", "seal 與 entropy source 都是 bandersnatch 簽章，但用途不同：一個證明出塊權、一個貢獻隨機"],
   ["H_R", "prior state root：本塊執行「之前」的狀態根"],
   ["H_E / H_W", "只在 epoch 邊界／抽籤成功時出現，平時是 ∅（optional 欄位）"],
 ],
 "eqs": [
   ["eq. 5.1", "H 的十個欄位與型別"],
   ["§5.x seal", "H_S 對「除了 seal 以外的 header」簽名；H_V 的輸入含 X_ 前綴 domain separator"],
   ["§D.1", "header 不進狀態樹，但 H_R 是狀態樹的根 —— 別把兩者搞混"],
 ],
 "asked": [
   ["為什麼是 prior state root 而不是 posterior？",
    "posterior root 必須等本塊全部執行完才算得出，出塊者就得在 slot 內跑完 STF 才能簽章封塊。"
    "改帶 prior root，出塊、傳播、狀態計算就能重疊成管線；代價是要驗證第 n 塊的狀態，得等第 n+1 塊的 header。"
    "這是 JAM 為了 6 秒 slot 做的核心取捨。"],
   ["H_S 和 H_V 為什麼要兩個簽章？",
    "H_S 證明「這個 slot 的確輪到我」，輸入綁 slot sealer；H_V 是熵的來源，輸入綁 entropy domain。"
    "如果共用一個，出塊者就能靠「要不要出這塊」同時操縱出塊權證明與隨機數；"
    "分開之後，H_V 的值在 H_S 決定的那一刻就已經被鎖住。"],
   ["epoch marker 為什麼要放在 header，而不是等狀態自己算出來？",
    "輕客戶端只同步 header。沒有 H_E，它就無法在不重放狀態的情況下知道 validator set 換人了，"
    "後續的簽章也就無從驗起。H_W 同理：它讓輕客戶端能自行推出誰該出塊。"],
   ["H_O（offenders）為什麼要上 header？",
    "剔除 validator 會直接影響後續所有簽章的驗證。放進 header 讓這件事對只看 header 的人也是明確的，"
    "同時它也是 H_X 之外少數會影響 κ 的欄位。"],
 ],
 "delta": [
   "0.8.0 統一把 header 欄位下標寫成大寫（H_T / H_I / H_P / H_R / H_X / H_E / H_W / H_O / H_V / H_S）",
 ],
 "code": [
   "internal/types/header.go — seal 驗證要先把 H_S 欄位清空再編碼，順序錯了簽章一定過不了",
   "epoch marker 與 winning tickets 是 optional，編碼時是 0/1 前綴，不是固定長度",
 ],
}]
