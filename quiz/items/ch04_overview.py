# -*- coding: utf-8 -*-
# Chapter 4 — Overview (GP 0.8.0)
ITEMS = [
{
 "id": "ch04-stf-extrinsic",
 "ch": "4", "section": "4.1 The Block", "gpRef": "eq. 4.2–4.3 (block / extrinsic)",
 "difficulty": 1, "kind": "concept", "tags": ["block", "extrinsic"],
 "stem": "Per GP 0.8.0, the extrinsic E of a JAM block is a tuple of exactly five components. Which of the following is NOT one of them?",
 "options": [
  "E_T — tickets for the Safrole slot-sealer contest",
  "E_X — user transactions signed by external accounts",
  "E_A — availability assurances by validators",
  "E_D — disputes (verdicts, culprits, faults)"
 ],
 "answer": 1,
 "optNotes": [
  "E_T 是 eq. 4.3 五元組的第一項：Safrole 的 ticket extrinsic。",
  "「使用者簽名的交易」是 Ethereum 模型的概念，eq. 4.3 的五元組裡沒有這一項。",
  "E_A 是 validator 對 availability 的 assurance，確實列在 eq. 4.3 之中。",
  "E_D 是 disputes（verdicts、culprits、faults），eq. 4.3 的第二項。",
 ],
 "explanation": "eq. 4.3：E ≡ (E_T, E_D, E_P, E_A, E_G)——五個成分，各有各的來源與用途：**E_T** tickets，validator 提交的 Safrole 抽籤券；**E_D** disputes，verdicts + culprits + faults；**E_P** preimages，要併進 δ 的原像 blob；**E_A** assurances，validator 宣告自己持有哪些 core 的 shard；**E_G** guarantees，本塊帶進來的 work-report 與其擔保簽章。**沒有第六個，特別是沒有「使用者交易」。** JAM 是 transactionless 的：§4 明說「there is no such concept of a transactor」。五個成分全部由 validator 產生並簽署——ticket 是 validator 抽的、assurance 是 validator 宣告的、guarantee 是 guarantor 簽的、judgment 是 auditor 簽的。**那外部資料怎麼進來？** 兩條路：其一是 work-package——使用者把工作交給 core，經 in-core 的 refine 產出 work-report，再由 guarantor 以 E_G 帶進鏈；其二是 preimage，透過 E_P 把 blob 本身放進狀態。兩條路都要先經過某個 validator 才進得了區塊，這正是 JAM 「in-core 做重活、on-chain 只收結果」架構的直接體現。把 E_X 這種「外部帳戶簽名的交易」列進來，就是把 Ethereum 的模型套到 JAM 上——這是最常見的誤解。",
 "trap": "面試常問：JAM 為什麼沒有 transaction？答：授權（authorization）與 blockspace 購買（coretime）被拆開，外部輸入經 refine 進入。"
},
{
 "id": "ch04-state-components",
 "ch": "4", "section": "4.2 The State", "gpRef": "eq. 4.4 (state composition)",
 "difficulty": 2, "kind": "concept", "tags": ["state"],
 "stem": "GP eq. 4.4 partitions the state σ into 17 components. Which pairing of symbol → meaning is WRONG?",
 "options": [
  "ρ → each core's current availability assignment (a guaranteed but not-yet-available work-report)",
  "ξ → work-packages recently accumulated (one epoch of history)",
  "ω → the authorizer queue from which each core's pool is refilled",
  "θ → the accumulation output log of the most recent block"
 ],
 "answer": 2,
 "optNotes": [
  "ρ 確實是每個 core 的 availability assignment：已 guarantee 但尚未 available 的 work-report。",
  "ξ 確實是最近一個 epoch 內已 accumulate 的 work-package hash，配對無誤。",
  "ω 是 ready queue（已 available 但 dependency 未滿足的 report）；authorizer queue 是 φ。",
  "θ 確實是本區塊的 accumulation output log，配對無誤。",
 ],
 "explanation": "eq. 4.4：σ ≡ (α, β, θ, γ, δ, η, ι, κ, λ, ρ, τ, φ, χ, ψ, π, ω, ξ)，共 17 個分量。**最容易混的是兩組佇列，記法是「誰餵誰」**：α 是 **authorizer pool**——每個 core 目前可用的 authorizer hash（最多 O = 8 個）；φ 是 **authorizer queue**——每個 core 固定 Q = 80 筆的補給來源，每個時槽從 φ 挪一筆進 α。所以「pool 的補給來源」是 φ，不是 ω。ω 是 **ready queue**——已經 available、但依賴還沒滿足、等著被 accumulate 的 report；ξ 是 **accumulation history**——最近一個 epoch 內已被 accumulate 的 work-package hash 集合，用來防重複與判斷依賴是否已滿足；θ 是 **accumulation output log**——本塊各 service 透過 `yield` 產出的 (service, hash) 序列，會被 β 的 belt 吸收。**其餘的分組記憶**：狀態核心 δ（service accounts）、χ（privileges）；Safrole 一組 γ（四元組）、η（entropy）、ι/κ/λ（staging/active/previous 三組金鑰）、τ（時槽）；流程一組 ρ（availability assignments）、β（recent history）、ψ（disputes）、π（statistics）。口試常見的追問是「哪些是每塊都動、哪些只在 epoch 邊界動」——η_0、τ、β、ρ、π 每塊都動，ι/κ/λ 的輪替與 γ_Z 的更新只在 e′ > e 時發生。",
 "trap": "ω (vartheta) vs φ (phi) 容易混：ω = ready/queued reports，φ = auth queue。"
},
{
 "id": "ch04-dependency-graph-alpha",
 "ch": "4", "section": "4.2.1 State Transition Dependency Graph", "gpRef": "eq. 4.5–4.20",
 "difficulty": 2, "kind": "concept", "tags": ["stf", "ordering"],
 "stem": "In the state-transition dependency graph, the posterior authorizer pool α′ is defined as α′ ≺ (H, E_G, φ′, α). What does this imply for the order of computation inside a block import?",
 "options": [
  "α′ can be computed before any extrinsic is validated, since eq. 4.5–4.20 makes it depend only on the header's timeslot H_T and the prior pool α",
  "α′ must be computed after accumulation, because φ′ (the posterior authorizer queue) is only known once accumulate has run (the `assign` host call may change it)",
  "α′ must be computed before the guarantees extrinsic is validated, since eq. 11.32 checks each report's authorizer against the posterior pool α′[w_c]",
  "α′ is independent of the extrinsic and may run in parallel with Safrole, since φ changes only through the `designate` privilege held by the delegator χ_V"
 ],
 "answer": 1,
 "optNotes": [
  "eq. 4.5–4.20 的依賴列是 α′ ≺ (H, E_G, φ′, α)，共四個輸入，不只 header 與 prior pool。",
  "φ′ 只有在 accumulation 跑完後才定義，§8.2 明講這一步必須排在 accumulation 之後。",
  "prior 與 posterior 反了：eq. 11.32 檢查的是 w_a ∈ α[w_c]，用的是 prior pool。",
  "認錯了 host call 與權限：改 φ[c] 的是 core 的 assigner χ_A 用 assign，designate 是 χ_V 設 ι。",
 ],
 "explanation": "GP §8.2 講得很直接：「Since α′ is dependent on φ′, practically speaking, this step must be computed after accumulation, the stage in which φ′ is defined.」**依賴圖不只是描述性的，它規定了計算順序。** α′ ≺ (H, E_G, φ′, α) 的四個輸入各有角色：H 提供 H_T（決定從 queue 的哪一格取）、E_G 決定哪些 authorizer hash 要從 pool 移除、φ′ 決定補進來的是什麼、α 是移除的基礎。**卡住順序的是 φ′**：authorizer queue 只能被具 assigner 權限（χ_A[c]）的 service 在 accumulate 期間透過 `assign` host call 修改，所以要等 accumulation 跑完才知道 φ′ 長什麼樣。**這也解釋了一個容易搞錯的時序**：guarantee 的 authorizer 檢查（eq. 11.32）用的是 **prior 的 α**，而 pool 的更新（eq. 8.2）用的是 **posterior 的 φ′**——一個在前一個在後，所以本塊 assign 進去的新 authorizer 最快要到下一塊才能用。你們的 STF（internal/stf/sft.go）也是在 accumulation 之後才做 α′，順序是對的。**0.8.0 的變動**：這個「pool 更新在 accumulation 之後」是 issue #1020 處理的重點，0.7.2 的順序不同。",
 "trap": "guarantee 驗證看 prior α；pool 更新用 posterior φ′。"
},
{
 "id": "ch04-common-era",
 "ch": "4", "section": "4.4 Time", "gpRef": "§4.4 (JAM Common Era)",
 "difficulty": 1, "kind": "concept", "tags": ["time"],
 "stem": "When does the JAM Common Era begin, and why was that particular time of day chosen?",
 "options": [
  "00:00 UTC on 1 January 2025 — a midnight start makes timeslot 0 the first slot of a calendar day, so every 14,400-slot boundary is a date change worldwide",
  "12:00 UTC on 1 January 2025 — midday ensures every major timezone is on the same calendar date at any exact 24-hour multiple from the epoch start",
  "12:00 UTC on 1 January 2024 — the day the first Gray Paper was published, so the slot index counts from the specification's own birthday",
  "00:00 UTC on 1 January 1970 — the Unix epoch itself, so a JAM timeslot index is simply the current Unix time divided by P = 6 seconds"
 ],
 "answer": 1,
 "optNotes": [
  "從 UTC 午夜起算的 24 小時倍數，UTC−5 還停在前一天、UTC+9 已進隔天，正是 midday 要避免的。",
  "GP 選 midday 的理由就是讓所有主要時區在 24 小時整數倍時落在同一個日期。",
  "年份錯了（是 2025），而且 GP 從未把 common era 綁在自身的出版日上。",
  "若 era 就是 Unix epoch，腳註那個 1,735,732,800 秒的偏移就會是 0。",
 ],
 "explanation": "GP §4.4：「we define the time in terms of seconds passed since the beginning of the JAM Common Era, 1200 UTC on January 1, 2025」，註腳補上這是 Unix 紀元後的 1,735,732,800 秒。**選正午的理由 GP 直接寫出來了**：「Midday UTC is selected to ensure that all major timezones are on the same date at any exact 24-hour multiple from the beginning of the common era.」也就是說，從 Common Era 起算每滿 24 小時的那一刻，從東亞到美洲的所有主要時區都還落在**同一個日曆日**——若選午夜 UTC，那一刻在美洲還是前一天、在東亞已是後一天，任何以「第幾天」做分期的人工對照都會出現跨日歧義。**與時槽的關係**：timeslot index 就是自 Common Era 起算的 6 秒週期數，所以 eq. 5.8 的有效性條件寫成 H_T · P ≤ 𝕋（P = 6 秒、𝕋 是牆鐘秒數）。**順帶算一下壽命**：時槽是 u32（eq. 4.28 的 N_T ≡ N_{2^32}），2^32 × 6 秒 ≈ 816.6 年，所以編號會在 2841 年 8 月中用完。",
 "trap": "數字題：1,735,732,800；slot = 6 秒；epoch = 600 slots = 1 小時。"
},
{
 "id": "ch04-in-core-vs-on-chain",
 "ch": "4", "section": "4.8 The Core Model and Services", "gpRef": "§4.9.1–4.9.2",
 "difficulty": 1, "kind": "concept", "tags": ["architecture", "refine", "accumulate"],
 "stem": "Which statement correctly contrasts JAM's in-core and on-chain consensus models?",
 "options": [
  "In-core computation (refine) is executed by every validator, while on-chain computation (accumulate) is executed only by the block author and replayed by others on a dispute",
  "In-core computation (refine) is executed by a subset of validators and secured by the guarantee/assure/audit/judge game; on-chain computation (accumulate) is executed by all validators",
  "In-core computation (refine) is stateful and may transfer balances between services; on-chain computation (accumulate) is stateless and accepts arbitrarily large inputs",
  "Both are executed by all validators and differ only in pricing: in-core gas is charged per octet of the work-package, while on-chain gas is charged per PVM instruction"
 ],
 "answer": 1,
 "optNotes": [
  "兩邊都顛倒了；accumulate 是 STF 的一部分，每個匯入區塊的節點都必須重算才對得上 H_R。",
  "§4.9.1 的 in-core 只由子集執行、以 guarantee/assure/audit/judge 擔保；on-chain 才是全體都算。",
  "說反了：refine 是 stateless、吃任意大的輸入，accumulate 才 stateful、能 transfer balance。",
  "差異的本質是「誰執行」與可擴展性，不是計價；沒有按 work-package octet 計 gas 這種規則。",
 ],
 "explanation": "GP §4.9.1：in-core model 下「only a subset of the network is responsible for actually executing any given computation」，靠 guaranteeing → assuring → auditing →（可能的）judging 這組 crypto-economic game 確保正確性，可達單機約 300 倍的算力；on-chain（accumulate）則是 GP 稱為「everybody does everything」的模型。§4.9.2 補上兩者的性格：refine 是「a sort of high-performance stateless processor, able to accept arbitrary input data」，accumulate 則「more stateful, providing access to certain on-chain functionality including the possibility of transferring balance」，而 GP 對兩者差異的總結是「the primary difference between them one of scalability versus synchroneity」。",
 "trap": "refine = stateless / in-core / 大輸入；accumulate = stateful / on-chain / 小輸出。"
},
{
 "id": "ch04-balance-timeslot-ranges",
 "ch": "4", "section": "4.6–4.7", "gpRef": "eq. 4.21 (balance), eq. 4.28 (timeslot)",
 "difficulty": 1, "kind": "concept", "tags": ["types"],
 "stem": "Which of the following is TRUE about the numeric domains used by JAM?",
 "options": [
  "Balances are N_2^64 (u64) with a standard denomination of 10^9 tokens; timeslots are N_2^32, giving the protocol a lifespan into the year 2840",
  "Balances are N_2^128 to match Polkadot's 10^10 denomination; timeslots are N_2^64, so the slot index can never wrap and the protocol has no dated end of life",
  "Balances are N_2^64 with Ethereum's 10^18 denomination; timeslots are N_2^32, which caps total issuance at roughly 18 whole tokens once the denomination applies",
  "Balances and timeslots are both N_2^64, with Kusama's 10^12 denomination, putting the protocol's end of life far beyond the year 2840"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 4.21 的 N_B ≡ N_2^64 配 10^9 面額，eq. 4.28 的 N_T ≡ N_2^32 才推得出 2840 年這個壽命。",
  "10^10 是 Polkadot 的面額；balance 是 u64 不是 u128，timeslot 放大成 u64 也就失去 2840 年這個結論。",
  "10^18 是 Ethereum 的值；套上去 18×10^9 tokens 只剩 18 顆，正說明 GP 為何選 10^9。",
  "三處都錯：timeslot 是 u32、面額是 10^9，而 10^12 是 Kusama 的。",
 ],
 "explanation": "兩個數域，兩個都在 §4 明文定義。**餘額** eq. 4.21：N_B ≡ N_{2^64}，也就是 u64。GP 同時說明面額是 10^-9（十億分之一顆為最小單位），因此「there may never be more than around 18×10^9 tokens」——2^64 個最小單位除以 10^9 約等於 184 億顆。選 u64 而不是更寬的型別，是因為餘額要塞進定寬的序列化欄位，也讓 service account 的門檻餘額計算不必動用大數。**時槽** eq. 4.28：N_T ≡ N_{2^32}，即 u32，計數的是自 JAM Common Era 起算的 6 秒時槽。算一下就知道壽命：2^32 × 6 秒 ≈ 257 億秒 ≈ **817 年**；Common Era 起點是 2025-01-01 1200 UTC，所以時槽編號會在 **2841 年 8 月中**用完。（GP 特別註明選正午 UTC，是為了讓所有主要時區在 24 小時的整數倍處都落在同一天。）**干擾項的來源**：GP 在同一段把 Polkadot 的 10^10、Kusama 的 10^12 與 Ethereum 的 10^18 明文列為對照，說 JAM 的 10^9「different to」它們——那三個數字就是被拿來當錯誤面額用的。順帶一提，service index 也是 u32（N_S），與時槽同寬但意義無關，是另一個常被混淆的點。",
 "trap": "u64 balance、u32 timeslot、u32 service index。"
},
{
 "id": "ch04-coretime-vs-gas",
 "ch": "4", "section": "4.8.2 On Services and Accounts", "gpRef": "§4.9.2 last paragraphs",
 "difficulty": 2, "kind": "rationale", "tags": ["coretime", "authorization"],
 "stem": "How does JAM replace Ethereum's gas-purchase model for buying blockspace?",
 "options": [
  "Blockspace is metered in gas and debited from the accumulating service's balance a_b as its work-report accumulates; a service whose balance runs dry has its reports dropped",
  "Coretime is pre-purchased (Agile-Coretime style) and assigned to an authorization agent; procurement is out of scope of the GP and expected to be handled by a system parachain",
  "Validators auction each six-second slot to the highest-bidding work-package builder, and the authorization system of §8 exists to settle that auction and pay out the winning bid",
  "Work-package builders sign a transaction that debits their own account on inclusion, exactly as in Ethereum — the one place where JAM keeps a signature-identified transactor"
 ],
 "answer": 1,
 "optNotes": [
  "gas 在 JAM 只是 PVM 的計量與上限，從頭到尾沒有餘額被扣；a_b 管的是 threshold a_t 與 transfer。",
  "§4.9.2 明講 coretime 是預先購買並指派給 authorization agent，採購本身不在 GP 範圍內。",
  "§8 只維護 authorizer pool α 與 queue φ，沒有出價、沒有拍賣，也不付錢給出塊者。",
  "直接違反「there is no such concept of a 'transactor'」——區塊裡沒有使用者簽名的交易。",
 ],
 "explanation": "GP §4.9.2：「In place of Ethereum's gas model for purchasing and measuring blockspace, JAM has the concept of coretime, which is prepurchased and assigned to an authorization agent… Its procurement is out of scope in the present work and is expected to be managed by a system parachain operating within a parachains service itself blessed with a number of cores」。授權代理（authorizer）讓外部行為者不必像 Ethereum 交易那樣自我識別即可提供輸入；同節斷言「In JAM, these are separated and there is no such concept of a 'transactor'」。這正是 §8 authorization system 的動機：把「買 coretime」與「提交具體工作」解耦。",
 "trap": "面試「design rationale」常問：為什麼要 authorization system？答：同時支援 Ethereum-style 與 Polkadot-style 的互動模式。"
},
{
 "id": "ch04-pvm-summary",
 "ch": "4", "section": "4.5 The Virtual Machine and Gas", "gpRef": "§4.7 The Virtual Machine and Gas, eq. 4.22–4.27",
 "difficulty": 1, "kind": "concept", "tags": ["pvm"],
 "stem": "Which description of the PVM as summarized in the Overview is correct?",
 "options": [
  "A stack machine derived from WebAssembly with 32-bit words, 16 registers and a linear memory that grows in 64 KiB pages with no inaccessible pages",
  "A RISC-V (RV64EM) based register machine with 13 64-bit registers, little-endian, and a pageable 32-bit address space in 4096-octet pages",
  "A RISC-V (RV32IM) based register machine with 16 registers of 32 bits, big-endian, and a flat 64-bit address space that is not paged at all",
  "An EVM-compatible machine that keeps the Yellow Paper's cryptographic precompiles and environment opcodes in its instruction set, with 256-bit words"
 ],
 "answer": 1,
 "optNotes": [
  "GP 明寫 PVM 是 RISC register machine；eq. 4.24 的 access 陣列正是為了讓頁面能是 ∅，page fault 才存在。",
  "RV64EM、13 個 64-bit 暫存器、little-endian、2^32 octet 的 pageable RAM 與 Z_P = 4096 全部對上 §4.5。",
  "四項全反：暫存器是 64-bit、13 個、little-endian，位址空間是 32-bit 且分頁。",
  "與 GP 的簡化理由正好相反：密碼學與環境互動指令一律拿掉，能力改走 host call。",
 ],
 "explanation": "GP §4.7（The Virtual Machine and Gas）：PVM 以 RISC-V 的 **RV64EM** 為基礎，是一台簡單的暫存器機。**13 個 64 位元暫存器**——GP 的註腳解釋了為什麼不是 16：「three fewer than RISC-V's 16, however the amount that program code output by compilers uses is 13 since two are reserved for operating system use and the third is fixed as zero」。**little-endian**，記憶體是 2^32 個 octet 的可分頁 RAM，頁大小 Z_P = 2^12 = 4,096，每頁的權限是 mutable(W)、readable(R) 或 inaccessible(∅) 三選一。**刻意刪減的部分**同節也交代了：「the complex instructions for cryptographic operations are missing as are those which deal with environmental interactions」——密碼學運算不做成指令（改由 host call 提供，才能精準計價），與環境互動的指令也拿掉（PVM 必須是**確定性且無外界依賴**的，否則 auditor 重跑會得到不同結果）。**這條「確定性」要求是整個稽核機制的前提**，也是為什麼 0.8.0 把 sbrk 改成 grow_heap host call：成本取決於運算元的指令會破壞 basic block 的靜態計價。",
 "trap": "13 registers / 64-bit / 4 KiB pages / 32-bit addressing。"
},
{
 "id": "ch04-forks-safrole-grandpa",
 "ch": "4", "section": "4.3 Which History?", "gpRef": "§4.3",
 "difficulty": 1, "kind": "rationale", "tags": ["consensus"],
 "stem": "JAM states three goals about forks: (1) two heads should rarely form, (2) when they do they should be resolved quickly, (3) it should be possible to identify a recent block that will remain in history in perpetuity. Which mechanism delivers which goal?",
 "options": [
  "Safrole delivers (1), Grandpa delivers (3), and both contribute to (2)",
  "Grandpa delivers (1) and (2); Safrole delivers (3)",
  "Safrole delivers all three; Grandpa is only used for BEEFY bridging",
  "ELVES auditing delivers (1); Safrole delivers (2); Grandpa delivers (3)"
 ],
 "answer": 0,
 "optNotes": [
  "正是 §4.3 的分工：出塊的 Safrole 給 (1)、finality 的 Grandpa 給 (3)，(2) 由兩者共同貢獻。",
  "把兩者對調了：Grandpa 管的是 finalization，不是「兩個 head 很少形成」。",
  "Grandpa 在 GP 裡就是 finality gadget 本身，不是只為 BEEFY bridging 服務的附件。",
  "ELVES 是 in-core 計算正確性的 auditing 機制，與這三個 fork 目標無直接關係。",
 ],
 "explanation": "GP §4.3 原話：「Safrole, which governs the (not-necessarily forkless) extension of the blockchain; and Grandpa, which governs the finalization… the former delivers point 1, the latter delivers point 3 and both are important for delivering point 2.」**Safrole → 目標 1（很少長出兩個 head）**：它把每個 6 秒時槽的出塊權限定給**唯一一位**持票人，所以正常情況下同一個 slot 不會有兩個合法區塊。注意 GP 自己用了「not-necessarily forkless」——Safrole 減少分叉但不保證消除，網路延遲或 fallback 模式下仍可能分叉。**Grandpa → 目標 3（某個近期區塊永久留在歷史裡）**：出塊機制本身無法給出「永不回滾」的保證，那是 finality gadget 的工作。**兩者共同 → 目標 2（分叉快速收斂）**：Safrole 讓分叉少發生，Grandpa 讓已發生的分叉有一個明確的收斂點；再加上 §19 的 best-chain 規則偏好 ticket-sealed 祖先較多的分支（T = 1 的那些），三者一起讓分叉不會拖長。**口試常見的追問**：「為什麼不用單一機制解決三件事？」——因為「快速出塊」與「不可回滾」在非同步網路下是互相拉扯的目標，分開處理才能各自最佳化。",
 "trap": ""
},
]
