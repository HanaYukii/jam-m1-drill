# -*- coding: utf-8 -*-
SHEETS = [{
 "ch": "8",
 "title": "Authorization",
 "one": "決定「誰有資格用某個 core」。每個 core 有一個大小 ≤ O 的 authorizer pool α 與長度 Q 的 queue φ；"
        "報告必須帶一個落在該 core pool 裡的 authorizer hash，用掉就從 pool 移除，並從 queue 依序補一個進來。",
 "flow": [
   "α ∈ ⟦⟦H⟧_{:O}⟧_C：每個 core 目前可用的 authorizer hash（至多 O 個）",
   "φ ∈ ⟦⟦H⟧_Q⟧_C：每個 core 的補充佇列，長度固定 Q，被 assigner 特權服務填",
   "報告合法性（eq. 11.32）要求 r_a ∈ α[r_c] —— 用的是本塊的 authorizer pool",
   "用掉的 authorizer 從 α 移除；接著把 φ[c][H_T mod Q] 推進 α 尾端",
   "α 超過 O 就從頭端丟棄，形成一個「先進先出＋隨用隨補」的滑動視窗",
   "authorizer 本身是一段 PVM 程式（is-authorized，Ψ_I），由 guarantor 在 refine 前先跑，決定這個 work-package 能不能用這個 core",
 ],
 "consts": [
   ["O = 8", "authorizer pool 上限（每 core）"],
   ["Q = 80", "authorizer queue 長度（每 core），固定長度、以 H_T mod Q 取用"],
   ["χ_A", "assigners：唯一能改 φ 的特權服務，每個 core 各有一個指派者"],
   ["G_I", "is-authorized 的 gas 上限；跑超過就視為未授權"],
 ],
 "eqs": [
   ["eq. 8.1", "α ∈ ⟦⟦H⟧_{:O}⟧_C、φ ∈ ⟦⟦H⟧_Q⟧_C 的型別（注意 :O 是「至多」，Q 是「剛好」）"],
   ["§8.2", "「The portion of state...」—— φ 只能由對應 core 的 assigner 修改"],
   ["eq. B.1", "Ψ_I : (P, N_C) → (𝔹 ∪ 𝔼, N_G)：吃 work-package 與 core index，回傳 blob 或錯誤，外加耗用 gas"],
   ["eq. 11.32", "報告端的檢查：r_a ∈ α[r_c]"],
 ],
 "asked": [
   ["authorization 到底在防什麼？沒有它會怎樣？",
    "core time 是稀缺資源。沒有 authorization，任何人都能把任意 work-package 丟到任意 core 上，"
    "guarantor 得先跑完 refine 才知道該不該做，等於免費的 DoS。"
    "authorizer 是一段便宜、有 gas 上限的前置程式，先用低成本擋掉沒付費／不合規的請求。"],
   ["為什麼 pool 是「至多 O」而 queue 是「剛好 Q」？",
    "pool 是動態的：用掉就少一個、補進就多一個，所以只能給上限。"
    "queue 是 assigner 預先排好的固定長度環形排程，用 H_T mod Q 取用，"
    "這樣「第 t 個 slot 該補哪個 authorizer」對所有節點都是同一個確定答案，不需要額外共識。"],
   ["is-authorized 為什麼要跑在 PVM 裡，不是一個固定的規則？",
    "不同 service 的付費模型不同——有的賣訂閱、有的按次、有的白名單。"
    "把授權邏輯做成可編程的一小段程式，鏈本身就不用內建任何商業模型，"
    "同時因為它有 gas 上限且無副作用，濫用成本可控。"],
   ["authorizer 用完後如果 queue 還沒補進來會怎樣？",
    "pool 會暫時變小，該 core 的可用授權變少，但不會停擺——下一個 slot 依然照 H_T mod Q 補。"
    "這是刻意的：assigner 沒跟上就自然限流，不需要任何例外處理路徑。"],
 ],
 "delta": [
   "0.8.0 的特權角色分家後，改 φ 的是 assigners χ_A（不是 manager χ_M）—— 兩者別混",
   "GP 0.8.0 的 authorizer queue 符號仍是 φ，沒有改名（ω 是 §12 的 ready queue）",
 ],
 "code": [
   "internal/authorization/ — pool 的移除與補充順序要嚴格照 GP：先移除再補，且補的是 H_T mod Q",
   "測試向量 authorizations/ 對「同一塊用掉兩個同 core authorizer」的情況特別敏感",
 ],
}]
