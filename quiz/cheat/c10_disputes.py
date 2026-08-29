# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "10",
 "title": "Disputes",
 "one": "把鏈下 auditing 的爭議搬上鏈做最終裁決：verdict 決定某份 work-report 是好是壞，"
        "culprits / faults 指認簽錯的人，結果沉澱進 ψ（good/bad/wonky/offenders），並清掉 ρ 上還掛著的壞 assignment。",
 "flow": [
   "E_D = (v, c, f)：verdicts、culprits、faults 三段各自獨立，但打包在同一個 extrinsic 裡",
   "每個 verdict = (report hash, epoch index, judgments)，judgments 剛好 ⌊2|k|/3⌋+1 筆，k = 該 epoch 的 validator set（κ′ 或 λ′）",
   "V 函數看正票數 t：t = ⌊2|k|/3⌋+1 → ⊤ good；t = 0 → ⊥ bad；t = ⌊|k|/3⌋ → ∅ wonky（三者以外的票數直接不合法）",
   "⊤ 的 verdict 必須在 faults 裡至少有一筆同 report hash 的紀錄（有人簽了「無效」卻被推翻）",
   "culprit = guarantee 了一份被判無效的 report；fault = 簽了與最終判決相反的 judgment，兩者都算 offence",
   "ρ† ：verdict 為 ⊥ 或 ∅ 的 core，availability assignment 直接清成 ∅（⊤ 不清，因為報告是好的）",
   "ψ′_G / ψ′_B / ψ′_W 收 report hash，ψ′_O 收所有 offender 的 Ed25519 key，之後輪替時被排除",
 ],
 "consts": [
   ["⌊2|k|/3⌋+1", "一份 verdict 要帶的 judgment 筆數，也是判 good 的正票數（|k| = 1023 時 = 683）"],
   ["⌊|k|/3⌋", "判 wonky 的正票數（|k| = 1023 時 = 341）—— 注意是「剛好等於」，不是「小於」"],
   ["0", "判 bad 的正票數：一票贊成都沒有"],
   ["排序規則", "verdicts 依 report hash；culprits / faults 各依 validator 的 Ed25519 key，且不得重複"],
 ],
 "eqs": [
   ["eq. 10.3", "E_D ≡ (v, c, f) 的型別與各段長度上限"],
   ["eq. 10.10–10.11", "verdicts 依 hash、offender 依 key 排序且去重；report hash 不得與過去judged 過的重複"],
   ["eq. 10.12", "V(epoch index, judgments) 的三分支（⊤ / ⊥ / ∅）"],
   ["eq. 10.14", "⊤ ⇒ faults 中存在同 hash 的項"],
   ["eq. 10.15", "ρ† ：⊥ 或 ∅ 的 core 清空"],
 ],
 "asked": [
   ["為什麼判 bad 需要「零票贊成」這麼極端的門檻？",
    "因為 ELVES 的設計是「只要有一個誠實的 auditor 就會發現問題」。一份真的無效的 report，"
    "沒有任何誠實 validator 會投贊成；反過來說只要有一票贊成，就代表要嘛報告其實有效、要嘛投票者說謊——"
    "後者屬於 fault，該走 fault 流程指認個人，而不是把整份報告打成 bad。"],
   ["wonky（∅）存在的意義是什麼？",
    "它代表「validator 之間對這份 report 的看法分裂到剛好 ⌊|k|/3⌋」，通常是網路分割或資料不可得，而不是有人作惡。"
    "wonky 一樣會清掉 core assignment（報告不能用），但不會產生 offender —— 不確定不等於有罪。"],
   ["culprit 和 fault 差在哪？",
    "culprit 是「當初 guarantee 了這份壞報告」的 guarantor，罪在生產端；"
    "fault 是「judgment 投得跟最終判決相反」的裁決者，罪在裁決端。兩者都進 ψ_O，但證據形態不同："
    "culprit 附的是 guarantee 簽名，fault 附的是 judgment 簽名。"],
   ["為什麼 judgment 要帶 epoch index？",
    "judgment 可能來自本 epoch 的 κ′ 或上一個 epoch 的 λ′（爭議往往跨 epoch 才被發現）。"
    "epoch index 決定用哪一組 key 驗簽、以及 |k| 是多少，少了它連門檻都算不出來。"],
 ],
 "delta": [
   "0.8.0 只保留「⊤ ⇒ 至少一筆 fault」，沒有「⊥ ⇒ 至少兩筆 culprit」這條——別照舊版寫法答",
   "ρ 現在存的是完整的 guarantee 𝔾（含 credentials），所以 ρ† 判斷時要從 guarantee 裡取 work-report 再 hash",
 ],
 "code": [
   "internal/disputes/ — verdict 計票、offender 累積、ρ† 清除",
   "驗簽時 κ′ / λ′ 要依 judgment 的 epoch index 選，寫死成 κ′ 是常見 bug",
 ],
}]
