# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "11",
 "title": "Reporting & Assurance",
 "one": "core 上的計算怎麼被「認證」與「保存」：guarantor 跑完 refine 產出 work-report 並連署進 E_G，"
        "占住該 core 的 availability assignment ρ；validator 再用 E_A 表態自己持有 shard，超過 2/3 就算 available，交棒給 §12。",
 "flow": [
   "每 R = 10 個 slot 一次 rotation：依 η′_2 把 validator 洗牌並指派到 C 個 core，每 core 3 個 guarantor",
   "guarantor 取 work-package → 跑 Ψ_I（is-authorized）→ 跑 Ψ_R（refine）→ 得到 work-report（含 avspec、refinement context、results）",
   "同 core 的 ≥2 個 guarantor 連署 → 進 E_G；驗簽時該 validator 的 assignment 必須真的等於 report 的 core",
   "ρ 三段：ρ†（disputes 清過）→ ρ‡（assurance 清過，達標與逾時的都拿掉）→ ρ′（塞入本塊新 guarantee）",
   "E_A：每個 validator 對 parent header hash 簽名，附一個 C-bit 的 bitfield 表示自己手上有哪些 core 的 shard",
   "某 core 的 assurance 數 > 2/3 |V| → 該 report 變 available，離開 ρ，成為 §12 的 R",
   "逾時：報告進 ρ 超過 U = 5 個 slot 還沒 available，直接清掉，該 core 重新可用",
 ],
 "consts": [
   ["C = 341", "core 數；ρ 是長度 C 的序列，每 core 至多一份 pending 報告"],
   ["R = 10", "rotation period（slot）；跨 rotation 邊界驗簽要用 prior assignment"],
   ["U = 5", "assurance timeout：報告在 ρ 上最多待 5 個 slot"],
   ["> 2/3 |V|", "available 門檻；每 core 3 個 guarantor、平均每 report 30 次 audit 是同一套 1/3 假設的另一面"],
   ["W_R / W_B / W_G", "work-report 各部分的大小上限（結果 blob、bundle、總量），超過就不是合法報告"],
 ],
 "eqs": [
   ["eq. 11.1", "ρ ∈ ⟦?(guarantee 𝔾, timeslot)⟧_C —— 0.8.0 存的是完整 guarantee，不只 report"],
   ["eq. 11.22–11.23", "M：本 rotation 的 core assignment；prior assignment 用於跨邊界的簽名驗證"],
   ["eq. 11.28", "連署者 v 的 assignment c[v] 必須等於 report 的 core w_c"],
   ["eq. 11.31", "∀r ∈ I：(r_s)_v = |κ′| —— avspec 的 shard 數要對得上 validator 數"],
   ["eq. 11.32", "∀r ∈ I：ρ‡[r_c] = ∅ ∧ r_a ∈ α[r_c] —— core 必須是空的，且 authorizer 在該 core 的 pool 裡"],
   ["eq. 11.36", "anchor 檢查：refinement context 的 anchor 要對得上 β† 裡某一筆的 h / s / b / t"],
   ["eq. 11.41–11.44", "反重複（β_H ∪ ξ ∪ ω ∪ ρ）、prerequisite 必須可解、segment-root lookup 必須是子字典"],
 ],
 "asked": [
   ["為什麼 guarantee 和 assurance 要拆成兩件事？",
    "guarantee 回答「這個計算結果是對的嗎」，靠的是 guarantor 的質押與後續 auditing；"
    "assurance 回答「這份資料還拿得到嗎」，靠的是 erasure code 的分片持有。"
    "兩者的失敗模式不同：算錯要罰人，資料不見要重建。混成一件事的話，"
    "惡意 guarantor 只要把 bundle 藏起來就能讓沒人能查驗它算得對不對。"],
   ["assurance 為什麼用 bitfield，不是每份 report 各簽一次？",
    "一個 validator 每個 slot 可能同時持有數百個 core 的 shard，逐一簽名的頻寬與驗簽成本都是 C 倍。"
    "bitfield 讓它一次簽 parent header hash + 一整排位元，鏈上只要驗一次簽章就能得到 C 個表態。"],
   ["ρ 為什麼要 †、‡、′ 三段？",
    "同一塊裡三種力量會動 ρ：disputes 要清掉被判壞的、assurance 要清掉已達標與逾時的、guarantees 要塞新的。"
    "定義成有序的三段，是為了讓「這一塊到底能不能報這個 core」有唯一答案——"
    "eq. 11.32 檢查的是 ρ‡（assurance 清完之後），所以同一塊裡剛騰出的 core 可以馬上再被用。"],
   ["為什麼一份報告至少要兩個 guarantor 連署？",
    "單一 guarantor 等於單點作惡，而 auditing 是抽樣的、有延遲。兩個以上的連署把「一起說謊」的成本拉高，"
    "同時每個連署者都獨立質押；三個 guarantor 的配置則是留一個冗餘，避免一個節點離線就報不出來。"],
 ],
 "delta": [
   "ρ 的內容由 (work-report, timeslot) 改成 (完整 guarantee, timeslot)，credentials 也上鏈了",
   "refinement context 欄位擴充（a, n, s, b, l, t, r, p），別照 0.7.2 的六欄背",
   "eq. 11.32 的量詞在 0.8.0 是 ∀r ∈ I（I 於 eq. 11.30 定義），不是舊版的 ∀w ∈ W",
 ],
 "code": [
   "internal/extrinsic/guarantee_controller.go — ValidateWorkReports，反重複與 anchor 檢查都在這",
   "assurance 的 bitfield 與 ValidatorIndex 對應要用 κ′；跨 rotation 邊界請確認用的是 prior assignment",
 ],
}]
