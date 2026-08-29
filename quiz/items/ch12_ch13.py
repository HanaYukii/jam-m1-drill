# -*- coding: utf-8 -*-
# Chapter 12 — Accumulation; Chapter 13 — Statistics (GP 0.8.0)
ITEMS = [
{
 "id": "ch12-history-queue-state",
 "ch": "12", "section": "12.1 History and Queuing", "gpRef": "eq. 12.1–12.3",
 "difficulty": 2, "kind": "concept", "tags": ["accumulation", "state"],
 "stem": "What are ξ (accumulated) and ω (ready) and how big are they?",
 "options": [
  "ξ ∈ [{H}]_E — one set of accumulated work-package hashes per slot for the last E = 600 slots (an epoch of history); ω ∈ [[(ℝ, {H})]]_E — per slot, the reports made available in that slot that still have unfulfilled dependencies, each paired with its outstanding dependency set",
  "ξ ∈ [{H}]_E — one set of accumulated WORK-REPORT hashes per slot for the last E = 600 slots (an epoch of history); ω ∈ [[(ℝ, {H})]]_E — per slot, every report that became available in that slot, whether or not its dependencies are met, each paired with the full dependency set it originally declared",
  "ξ ∈ {H} — one flat set holding every work-package hash ever accumulated, never pruned; ω ∈ [[(𝕎, {H})]]_E — per slot, the work-ITEMS made available in that slot that still have unfulfilled dependencies, each paired with its outstanding dependency set",
  "ξ ∈ [{H}]_C — one set of accumulated work-package hashes per core, so C = 341 sets; ω ∈ [[(ℝ, {H})]]_C — one queue per core holding that core's reports which still have unfulfilled dependencies, each paired with its outstanding dependency set"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 12.1 與 12.3 都以 slot 索引、長度 E，ω 配的是尚未滿足的 dependency 集合。",
  "P(r) 取的是 avspec 的 work-package hash；eq. 12.4 只把有依賴者放進 R^Q，配的也是修剪後剩下的依賴。",
  "ξ 是長度 E 的序列、歷史只留一個 epoch；ω 裝的是 work-report ℝ，𝕎 是 §14.3 的 work-item。",
  "ξ 與 ω 都以 slot 索引、長度都是 E = 600；App. D 的 C(14) 也是照 slot 逐格序列化。",
 ],
 "explanation": "eq. 12.1：ξ ∈ [{H}]_E（每個 slot 一個集合，共 E 個），ξ_∪ 是聯集；12.3：ω ∈ [[(R, {H})]]_E——ready（已 available 但尚未 accumulate）的 report 與其**未滿足的** dependency（package hash 集合）。兩者都是長度 E 的環狀緩衝：ξ′[E−1] 放本塊剛 accumulate 的 hash 並左移；ω′[m]（m = H_T mod E）放本塊新的 R^Q，跳過的 slot 清空。這就是 test vectors 中 accumulate/ 的 enqueue/unlock/ring-wrap 案例。",
 "trap": "ξ 存的是 package hash 不是 report hash；ready 的依賴在每次 accumulate 後用 E() 修剪。"
},
{
 "id": "ch12-W-partition",
 "ch": "12", "section": "12.1 History and Queuing", "gpRef": "eq. 12.4–12.12 (W!, W^Q, E, Q, W*)",
 "difficulty": 3, "kind": "concept", "tags": ["accumulation", "dependencies"],
 "stem": "How is the sequence of accumulatable reports R* built from the newly available reports R?",
 "options": [
  "R! = reports with no prerequisites and empty segment-root lookup, accumulated immediately; R^Q = the rest, each paired with its dependency set (prerequisites ∪ keys of srlookup) pruned by ξ_∪; R* = R! ⌢ Q(E(ω[m..] ⌢ ω[..m] ⌢ R^Q, P(R!))) where Q repeatedly extracts reports whose dependency set is empty and E removes satisfied dependencies",
  "R! = reports with no prerequisites and empty segment-root lookup, accumulated immediately; R^Q = the rest, each paired with its dependency set (prerequisites ∪ keys of srlookup) pruned by ξ_∪; R* = R! ⌢ Q(E(ω[..m] ⌢ ω[m..] ⌢ R^Q, P(R!))), i.e. the ready queue is read from the current slot m forwards so that the freshest queued reports get their turn first",
  "R! = reports with no prerequisites, whatever their segment-root lookup holds, accumulated immediately; R^Q = the rest, each paired with its prerequisite set alone, pruned by ξ[E−1] (only the packages accumulated in the previous slot); R* = R! ⌢ Q(E(ω[m..] ⌢ ω[..m] ⌢ R^Q, P(R!))) with Q extracting reports whose dependency set is empty",
  "R! = reports with no prerequisites and empty segment-root lookup, accumulated immediately; R^Q = the rest, each paired with its dependency set (prerequisites ∪ keys of srlookup) pruned by ξ_∪; R* = R! ⌢ Q(E(ω[m..] ⌢ ω[..m] ⌢ R^Q, P(R!))), where Q makes a single pass over the queue and any report still holding a dependency afterwards makes the block invalid"
 ],
 "answer": 0,
 "optNotes": [
  "三處都對：R^Q 先用 ξ_∪ 修剪、ready queue 從最舊的 slot m 起繞一圈、Q 遞迴解到解不動為止。",
  "方向反了：m = H_T mod E 正是本塊要覆寫的最舊一格，ω[m..] 起頭才是由舊到新。",
  "eq. 12.4 要求 |x_p| = 0 且 r_l = ∅ 同時成立；D(r) 含 keys(r_l)，修剪用 ξ_∪ 而非只有最後一格。",
  "Q 是遞迴定義（解開一批就再用 E 扣一次依賴）；解不開的 report 只是續留 ω 等過期，區塊仍有效。",
 ],
 "explanation": "eq. 12.4：R! = [r | r ∈ R, |x_p| = 0 ∧ r_l = ∅]；12.5：R^Q = E([D(r) | r ∈ R, 有依賴], ξ_∪)，D(r) = (r, x_p ∪ keys(r_l))；12.7：E(r, x) 移除 package hash ∈ x 的項目並從各項依賴集合扣掉 x；12.8：Q(r) = g ⌢ Q(E(r, P(g)))，g = 依賴集合為空者，直到沒有為止；12.11–12.12：R* = R! ⌢ Q(q)，q = E(ω[m..] ⌢ ω[..m] ⌢ R^Q, P(R!))，m = H_T mod E——ready queue 從**最舊**（slot m 起繞一圈）讀起。有無法解的依賴不會讓區塊無效，只是那個 report 留在 ω 直到過期（一個 epoch 後被覆蓋）。",
 "trap": "E 的參數 x 在第一次是 P(R!)（本塊立即 accumulate 者的 hash），不是整個 ξ（R^Q 已先用 ξ_∪ 修剪過）。"
},
{
 "id": "ch12-gas-budget",
 "ch": "12", "section": "12.3 Final State Integration", "gpRef": "eq. 12.24 (g) & 12.17 (Δ+)",
 "difficulty": 3, "kind": "delta", "tags": ["accumulation", "gas", "delta-0.8.0"],
 "stem": "What total gas budget g is handed to the outer accumulation Δ+ in a block, and how does Δ+ choose how many reports to accumulate in a round?",
 "options": [
  "g = max(G_T, G_A·C + Σ_{x∈values(χ_Z)} x); Δ+ picks the largest prefix i of the reports such that Σ digest gas-limits of those i reports + Σ gas of pending deferred transfers + Σ free-accumulation gas ≤ g, runs Δ* on them, then recurses with g* = g + Σ(new transfers' gas) − Σ gas actually used and an empty free-accumulation map",
  "g = max(G_T, G_A·C + Σ_{x∈values(χ_Z)} x); Δ+ picks the largest prefix i of the reports such that Σ digest gas-limits of those i reports alone ≤ g — transfer gas and free-accumulation gas play no part in the test — runs Δ* on them, then recurses with g* = g − Σ gas actually used, carrying the same free-accumulation map into every round",
  "g = G_A·C = 3.41·10^9 exactly, with the always-accumulate allowances χ_Z drawn out of that same total; Δ+ picks the largest prefix i of the reports such that Σ digest gas-limits + Σ gas of pending deferred transfers ≤ g, runs Δ* on them, then recurses with g* = g − Σ gas actually used and the same free-accumulation map",
  "g = G_R = 5·10^9, the per-package refine allowance reused as the block's accumulation budget; Δ+ accumulates exactly one report per round rather than a prefix, subtracting that report's actual gas use from g each time, and halts as soon as a service's Accumulate panics, discarding the remaining reports and any transfers they produced"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 12.17 的預算測試（#500 之後）含 t_g 與 free allowance，遞迴時 f 傳空、g* 再加回 t* 的 gas。",
  "描述的是 0.7.2 的行為：#500 之後 t_g 與 f 才納入判斷，eq. 12.17 遞迴也明確傳 ∅ 進去。",
  "eq. 12.24 是 max(G_T, G_A·C + Σ χ_Z)，χ_Z 是外加的；何況 3.41·10^9 < G_T，取 max 後就是 G_T。",
  "G_R 是單一 package 的 refine 上限；Δ+ 取的是最大前綴，Ψ_A 內 panic 只讓該 service 的 output 消失。",
 ],
 "explanation": "eq. 12.24：g = max(G_T, G_A·C + Σ χ_Z gas)，G_T = 3.5·10^9、G_A = 10^7、C = 341。eq. 12.17：i = max i：Σ_{r ∈ r[..i], d ∈ r_d} d_g + Σ_{t ∈ t} t_g + Σ_{x ∈ values(f)} x ≤ g（0.8.0 #500「Account for gas reserved by transfer and always acc items」——預算現在把 transfer gas 與 free allowance 也算進去）；n = i + |t| + |f|；(e*, t*, b*, u*) = Δ*(e, t, r[..i], f)；遞迴 Δ+(g*, t*, r[i..], e*, {})，g* = g + Σ t* gas − Σ u* used。為什麼是這種「先估後扣」設計：§12.2 兩個相斥因素——實際 gas 只有執行後才知道（sequential），但同一 service 的 items 想合併成一次 PVM 呼叫以攤銷啟動成本（parallel）。",
 "trap": "遞迴時 f（always-accumulate）傳空——特權 service 只在第一輪免費 accumulate。"
},
{
 "id": "ch12-delta-star",
 "ch": "12", "section": "12.2 Execution", "gpRef": "eq. 12.18–12.19 (Δ*, R)",
 "difficulty": 3, "kind": "concept", "tags": ["accumulation", "privileges"],
 "stem": "In Δ* (parallel accumulation), which services are accumulated and how are the privileged indices (assigners, delegator, registrar) resolved when both the manager and the privileged service itself change them?",
 "options": [
  "s = {services with a digest} ∪ keys(f) ∪ {destinations of deferred transfers}; each is accumulated exactly once via Δ1; the manager's output alone decides χ′_M and χ′_Z; for assigners, delegator and registrar the conflict resolver is R(o, a, b) = b when a = o, else a",
  "s = {services with a digest} only, so a service that merely receives a deferred transfer or enjoys free accumulation is skipped; each is accumulated exactly once via Δ1; the manager's output alone decides χ′_M and χ′_Z, and assigners, delegator and registrar are changeable only by the manager",
  "s = every service in keys(δ); each is accumulated once per work-digest rather than once per round, so a service holding three digests runs Δ1 three times; the manager's output alone decides χ′_M and χ′_Z; a privilege changed by both the manager and its current holder in the same round makes the block invalid",
  "s = {services with a digest} ∪ keys(f) ∪ {destinations of deferred transfers}; each is accumulated exactly once via Δ1; χ′_M and χ′_Z are taken from the registrar's output; the conflict resolver is R(o, a, b) = a when a = o, else b"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 12.18 的三個聯集與 eq. 12.19 的 R 都對：manager 沒動時（a = o）才採用持有者自己的 b。",
  "s 還要聯集 K(f) 與 transfer 收件人 t_d；§12.2 的 R 存在正是要讓特權被 owned、由持有者轉走。",
  "只有 s 之內的 service 會跑；Δ1 把同一 service 的所有 digest 併成一次 Ψ_A 呼叫；衝突交給 R 解。",
  "這兩項直接取 manager 的輸出；顛倒後的 R 在 manager 沒動時回傳 prior 值 o，等於忽略持有者。",
 ],
 "explanation": "eq. 12.18：s = {d_s | r ∈ r, d ∈ r_d} ∪ K(f) ∪ {t_d | t ∈ t}；每個 s 呼叫 Δ1(e, t, r, f, s) 一次。(χ′_M, χ′_Z) 直接取 manager m 的輸出 e*；∀c：χ′_A[c] = R(χ_A[c], e*_A[c], (Δ1(χ_A[c]) 輸出)_A[c])；同理 χ′_V、χ′_R；eq. 12.19：R(o, a, b) = b 若 a = o 否則 a。§12.2：「This allows privileges to be 'owned' and facilitates the removal of the manager service」——assigner 可以自己把 assign 權轉走（owned privileges，0.7.1 #475），但 manager 的變更優先。ι′ 來自 delegator 的輸出，φ′[c] 來自 assigner c 的輸出。新建帳戶 n 與刪除帳戶 m 合併進 δ；若兩個 service 產生同一個新 index（理論上不會）則區塊無效。",
 "trap": "每個 service 一輪只 accumulate 一次，其 inputs = 給它的 transfers ⌢ 它的 operand tuples（eq. 12.23）。"
},
{
 "id": "ch12-delta-one-gas",
 "ch": "12", "section": "12.2 Execution", "gpRef": "eq. 12.23 (Δ1)",
 "difficulty": 2, "kind": "concept", "tags": ["accumulation", "gas"],
 "stem": "For a single service s, Δ1 invokes Ψ_A(e, τ′, s, g, i^T ⌢ i^U). How is the gas g computed and what are the inputs?",
 "options": [
  "g = f[s] (free allowance, or 0) + Σ gas of deferred transfers destined to s + Σ accumulate gas-limits of s's digests across the round's reports; i^T = the transfers to s (in order), i^U = one operand tuple per digest of s (report order)",
  "g = f[s] (free allowance, or 0) + Σ gas of deferred transfers destined to s, the digests' accumulate gas-limits NOT being added because Δ+ already charged them against the block budget; i^T = the transfers to s (in order), i^U = one operand tuple per digest of s (report order)",
  "g = δ[s]_g, the service's own minaccgas, capped at G_A = 10^7; i^T = the transfers to s (in order), i^U = one operand tuple per work-REPORT carrying at least one digest of s, not one per digest",
  "g = f[s] (free allowance, or 0) + Σ gas of deferred transfers destined to s + Σ accumulate gas-limits of s's digests across the round's reports; the argument sequence is i^U ⌢ i^T, this round's operand tuples coming ahead of any transfer carried over from the previous round"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 12.23 的 g 是 f[s]、transfer gas 與 d_g 三項相加、缺一不可，引數順序也明寫 i^T ⌢ i^U。",
  "Δ+ 的預算測試只決定這一輪吃幾個 report；交給 Ψ_A 的額度仍要把該 service 所有 d_g 加總進去。",
  "a_g 是 §11 驗 report 時 d_g 的下限而非 accumulate 的額度；i^U 也是每個 digest 一筆而非每份 report。",
  "順序反了：eq. 12.23 明寫 Ψ_A(…, i^T ⌢ i^U)，0.7.1 併掉 Ψ_T 後就靠位置區分兩類 input。",
 ],
 "explanation": "eq. 12.23：g = f[s]（若無則 0）+ Σ_{t: t_d = s} t_g + Σ_{d: d_s = s} d_g；i^T = [t | t ∈ t, t_d = s]；i^U = [(r_d result, g_d gas limit, y payload hash, o auth trace, e segroot, h package hash, a authorizer) | r ∈ r, d ∈ r_d, d_s = s]，產生式同時走 r ⊰ r 與 d ⊰ r_d，所以同一 report 裡屬於 s 的兩個 digest 會給出兩筆。0.7.1 起 on_transfer 被併入 accumulate：transfer 以 input 形式（在 operand 之前）交給同一次 Ψ_A（你們 deferred_transfers.go 的註解「v0.7.1 has removed deferred transfers & Ψ_T」）。operand tuple 定義在 eq. 12.13：(h, e, a, y, g, o, r)。",
 "trap": "digest 的 g 是 accumulate gas limit（guarantor 從 work-item 帶進來，鏈上檢查 ≥ a_g）。"
},
{
 "id": "ch12-deferred-transfer",
 "ch": "12", "section": "12.2 Execution", "gpRef": "eq. 12.14 & B.transfer",
 "difficulty": 1, "kind": "concept", "tags": ["accumulation", "transfers"],
 "stem": "A deferred transfer T = (s, d, a, m, g). What are the fields, and when is the balance moved?",
 "options": [
  "s source service, d destination, a amount, m memo of W_T = 128 octets, g gas limit for the recipient's handling; the sender's balance is deducted when `transfer` is called, and the amount is credited to the destination when it is accumulated in a later round",
  "s the sender's Ed25519 public key, d the destination service, a the amount, m a 32-octet memo hash, g the gas price the sender is willing to pay; the sender's balance is deducted when `transfer` is called and credited to the destination inside the very same Δ* round",
  "s source service, d the destination CORE index, a amount, m memo of W_T = 128 octets, g gas limit for the recipient's handling; nothing leaves the sender until the destination is actually accumulated, so a transfer aimed at a service deleted during the same round costs the sender nothing",
  "s source service, d destination, a amount, m memo of W_T = 128 octets, g gas limit for the recipient's handling; the sender is debited when `transfer` is called, and the destination is credited later in the same round by a separate on-transfer entry point Ψ_T that Δ* invokes once the digests are done"
 ],
 "answer": 0,
 "optNotes": [
  "五個欄位全對；Ω_T 成功時當場從 sender 扣款，收方要到下一輪 Δ+ 以 input 形式收到才入帳。",
  "eq. 12.14 的 s、d 都是 service index，m 是 128 octet 的 memo 本體，g 是 gas limit 不是價格。",
  "d ∈ N_S 是 service 不是 core；Ω_T 成功時已把 balance 設為 b − a，收方消失錢也回不來。",
  "0.7.1 就把 Ψ_T 併進 accumulate，0.8.0 只有 Ψ_A，而且交付是在下一輪而非同一輪。",
 ],
 "explanation": "eq. 12.14：T ≡ (s ∈ N_S, d ∈ N_S, a ∈ N_B, m ∈ B_{W_T}, g ∈ N_G)，W_T = C_memosize = 128。B 附錄 `transfer`（index 21）：呼叫時檢查 d 存在（否則 WHO）、l ≥ δ[d]_m（否則 LOW）、扣款後餘額 ≥ 自己的 threshold（否則 CASH），成功則立刻從 sender 扣除 a 並把 T 追加到 context 的 transfers 序列。接收方在**下一輪** Δ+ 才以 input 形式收到（Δ+ 的 t* 餵給遞迴呼叫），此時餘額才加上去；轉給不存在（或本輪被刪除）的 service 會被丟棄——但 sender 早就被扣了。",
 "trap": "memo 固定 128 bytes；g 是給接收方處理這筆 transfer 的 gas，會計入下一輪預算。"
},
{
 "id": "ch12-outputs",
 "ch": "12", "section": "12.3 Final State Integration", "gpRef": "eq. 12.24–12.33 (δ† → δ‡ → δ′)",
 "difficulty": 2, "kind": "concept", "tags": ["accumulation", "state"],
 "stem": "After Δ+ returns (n, e′, b, u, t), which statements about the final integration are correct?",
 "options": [
  "θ′ = the (service, hash) pairs in b (services that yielded a 32-byte hash); (δ†, ι′, φ′, χ′) come from e′; the accumulation statistics record per service (N items accumulated, T transfers processed, G gas used); δ‡ marks a_a = τ′ for every service that appears in the statistics; ξ′[E−1] = P(R*[..n])",
  "θ′ = H(E(δ†)), a single commitment to the whole posterior service state; (δ†, ι′, φ′, χ′) come from e′; the accumulation statistics record per service (N items accumulated, T transfers processed, G gas used); δ‡ marks a_a = τ′ for every service that appears in the statistics; ξ′[E−1] = P(R*), the whole accumulatable sequence",
  "θ′ = the (service, hash) pairs in b (services that yielded a 32-byte hash); (δ†, ι′, φ′, χ′) come from e′; the accumulation statistics record per service (N items accumulated, G gas used), the transfer count having been dropped; δ‡ marks a_a = τ′ for every service in keys(δ†); ξ′[E−1] = P(R*[..n])",
  "θ′ = the (service, hash) pairs in b (services that yielded a 32-byte hash); (δ†, ι′, φ′, χ′) come from e′; the accumulation statistics record per service (N items accumulated, T transfers processed, G gas used); δ‡ marks a_a = τ′ for every service that appears in the statistics; ξ′[E−1] = P(R*[..n]) and ω′ is emptied in full, so that no queued report ever survives a block"
 ],
 "answer": 0,
 "optNotes": [
  "θ′ 取 b 的 (s, h) 配對、統計是三元組、a_a 只更新 keys(S)、ξ′[E−1] 只收 R*[..n]，四項全對。",
  "θ′ 是 accumulation output log 不是狀態雜湊；ξ′[E−1] 只收本塊真的做完的 R*[..n]。",
  "0.8.0 的 S(s) 是 (N, T, G) 三元組；a_a = τ′ 只加在 keys(S) 上，沒被 accumulate 的帳戶不動。",
  "ω′ 是環狀更新：只有被跳過的 slot 會清空，其餘 slot 保留並同樣經過 E 修剪。",
 ],
 "explanation": "eq. 12.24：(n, e′, b, u, t) ≡ Δ+(g, [], R*, e, χ_Z)；θ′ ≡ [(s, h) ∈ b]（餵 §7 的 belt）；eq. 12.26：(δ†, ι′, φ′, χ′_M, χ′_A, χ′_V, χ′_R, χ′_Z) ≡ e′。eq. 12.27–12.28：accumulation statistics 記作 **S** ∈ D⟨N_S → (N, N, N_G)⟩，S(s) = (N(s) 前 n 個 report 中屬於 s 的 digest 數, T(s) 處理的 transfers 數（0.8.0 #502 加回）, G(s) gas used)，只記非 (0,0,0) 者。eq. 12.29–12.30：δ‡ = δ† 但 keys(S) 中的 service a_a = τ′。eq. 12.31–12.33：ξ′[E−1] = P(R*[..n])、其餘左移；ω′ 的 ring 更新。",
 "trap": "a_a（last accumulation slot）只對「這塊真的 accumulate 過」的 service 更新。"
},
{
 "id": "ch12-preimage-integration",
 "ch": "12", "section": "12.4 Preimage Integration", "gpRef": "eq. 12.34–12.37",
 "difficulty": 2, "kind": "concept", "tags": ["accumulation", "preimages"],
 "stem": "Which rule governs the preimages extrinsic E_P and its integration into δ′?",
 "options": [
  "E_P ∈ [(s, d)] ordered & unique; each (s, d) must be providable in the PRIOR δ — the service exists and δ[s]_l[(H(d), |d|)] = [] (requested, not yet provided); integration happens after accumulation: δ′ = I(δ‡, E_P), setting a_l[(H(d),|d|)] = [τ′] and a_p[H(d)] = d, silently dropping any preimage that is no longer useful",
  "E_P ∈ [(s, d)] ordered & unique; each (s, d) must be providable in the POSTERIOR δ‡ — the service must still exist there and δ‡[s]_l[(H(d), |d|)] = [] — so a request that accumulation dropped in the same block makes the whole block invalid; integration is then δ′ = I(δ‡, E_P), setting a_l[(H(d),|d|)] = [τ′] and a_p[H(d)] = d",
  "E_P ∈ [(s, d)] ordered & unique; any preimage may be included whether or not the service solicited it, since I stores every pair it is handed; integration happens BEFORE accumulation, δ† = I(δ, E_P), so that a service's Accumulate can read a preimage supplied in the same block, setting a_l[(H(d),|d|)] = [τ′] and a_p[H(d)] = d",
  "E_P ∈ [(s, d)] need only be free of duplicates, the ordering being unconstrained; each (s, d) must be providable in the prior δ and must additionally be signed by the service's manager; integration happens after accumulation: δ′ = I(δ‡, E_P), setting a_l[(H(d),|d|)] = [τ′] and a_p[H(d)] = d, silently dropping any preimage that is no longer useful"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 12.36 的 Y 吃 prior δ 判斷 providable，eq. 12.37 的整合作用在 δ‡，兩個 staging 都擺對了。",
  "eq. 12.36 的 Y 明確吃 prior δ；被 forget 掉的 preimage 是 disregarded, without prejudice。",
  "Y 要求 δ[s]_l[(H(d), |d|)] = []；§12.4 開頭就是 After accumulation, we must integrate…。",
  "eq. 12.35 要求 ordered 且 unique，而 GP 從頭到尾沒有任何簽章條件，只看 request 是否存在。",
 ],
 "explanation": "eq. 12.34–12.36：E_P ∈ [(N_S, B)]，依 (s, d) 排序且唯一，∀(s, d)：Y(δ, s, d)（providable：s ∈ keys(δ) 且 δ[s]_l[(H(d), |d|)] = []）——用 **prior** δ 檢查。eq. 12.37：δ′ = I(δ‡, E_P)——在 accumulation 之後才整合（依 §4 dependency graph 的 merge/join），因此若 accumulate 過程中 service 被刪或 request 被 forget，該 preimage「disregarded, without prejudice」。I 會把 request 設為 [τ′] 並寫入 preimage。你們的錯誤碼：preimages not sorted and unique / preimage not required。",
 "trap": "驗證看 prior δ、整合作用於 δ‡；順序題在 fuzzer 很常出現。"
},
{
 "id": "ch12-code-outer-accumulation",
 "ch": "12", "section": "12.2 Execution", "gpRef": "eq. 12.17 — internal/accumulation/accumulation.go OuterAccumulation",
 "difficulty": 3, "kind": "code", "tags": ["accumulation", "code", "delta-0.8.0"],
 "stem": "This is the team's prefix selection in Δ+. Compared with GP 0.8.0 eq. 12.17, what is missing?",
 "code": {"lang": "go", "caption": "internal/accumulation/accumulation.go (OuterAccumulation, 0.7.2)", "src": """gasSum := types.Gas(0)
i := 0
// Determine the maximal prefix of reports that fits within the gas limit
for idx, report := range r {
    for _, result := range report.Results {
        gasSum += result.AccumulateGas
    }
    if gasSum <= g {
        i = idx + 1
    } else {
        break
    }
}
// n = |t| + i + |f|
n := len(t) + i + len(f)"""},
 "options": [
  "0.8.0 requires the budget test to include Σ gas of the pending deferred transfers t and Σ free-accumulation allowances f (Σ d_g + Σ t_g + Σ f ≤ g), so gasSum must start from those two sums rather than 0",
  "The gas figures are the wrong ones: eq. 12.17 sums each digest's actual gas used d_u over the prefix rather than the declared limits d_g, since Δ* hands the real usage back before the budget is tested",
  "The test must be applied per report rather than cumulatively: eq. 12.17 requires each individual report in r[..i] to satisfy Σ d_g ≤ G_A = 10^7, so the loop must break at the first report exceeding that per-report cap",
  "The bound on i is wrong: eq. 12.17 takes i as a maximum over N_{|r|+1} so that i may reach |r|, whereas `i = idx + 1` inside the loop caps it at |r| − 1 and always leaves the final report for the next round"
 ],
 "answer": 0,
 "optNotes": [
  "PR #500 把 t_g 與 always-accumulate 的 f 納入 eq. 12.17 的預算判斷，0.7.2 的 code 只加 d_g。",
  "§12.2：實際用量只能在 Δ* 跑完後才知道；何況 digest 裡的 u 記的是 refine 用掉的 gas。",
  "eq. 12.17 的測試是對整個前綴累加；單一 package 的 Σ w_a < G_A 是 §14.3 的封包合法性條件。",
  "idx 最大取到 |r| − 1，i = idx + 1 因此可以等於 |r|，與 i ∈ N_{|r|+1} 完全一致。",
 ],
 "explanation": "eq. 12.17（0.8.0）：i = max(N_{|r|+1})：Σ_{r ∈ r[..i], d ∈ r_d} d_g + Σ_{t ∈ t} t_g + Σ_{x ∈ values(f)} x ≤ g。PR #500「Account for gas reserved by transfer and always acc items」把 transfer gas 與 always-accumulate 的 gas 納入預算判斷（否則實際可能超出 g）。0.7.2 的 code 只加 AccumulateGas。n = |t| + i + |f| 在兩版都一樣。§12.2 也講明「Only after a work-item is accumulated can it be known if it uses less gas than the advertised limit」——實際用量只能透過 g* = g + Σ t* gas − Σ u 回饋到下一輪。",
 "trap": "你們 issue digest 提到：eq:accseq budget now includes transfer gas + free allowances。"
},
{
 "id": "ch13-validator-stats",
 "ch": "13", "section": "13.1 Validator Activity", "gpRef": "eq. 13.1–13.6",
 "difficulty": 2, "kind": "delta", "tags": ["statistics", "delta-0.8.0"],
 "stem": "π ≡ (π_V, π_L, π_C, π_S). Which statement about the validator statistics is correct in GP 0.8.0?",
 "options": [
  "Each validator record has six counters (blocks b, tickets t, preimage count p, preimage size d, guarantees g, assurances a); assurances of this block are credited to π_V† BEFORE the epoch-rollover check; on e′ ≠ e, π_L ← π_V† and π_V resets; then b/t/p/d are credited to the author H_I and g to every validator in the reporters set G",
  "Each validator record has five counters (blocks b, tickets t, preimage count p, preimage size d, guarantees g), assurances being tracked per core in π_C instead; on e′ ≠ e both π_V and π_L are zeroed so that the new epoch starts from nothing; then b/t/p/d are credited to the author H_I and g to every validator in the reporters set G",
  "Each validator record has six counters (blocks b, tickets t, preimage count p, preimage size d, guarantees g, assurances a); assurances of this block are credited AFTER the epoch-rollover check, so on e′ ≠ e they land in the fresh π′_V instead of in π′_L; π_L then takes π_V rather than π_V†; b/t/p/d go to the author H_I and g to the reporters set G",
  "Each validator record has six counters (blocks b, tickets t, preimage count p, preimage size d, guarantees g, assurances a); assurances of this block are credited to π_V† BEFORE the epoch-rollover check; on e′ ≠ e, π_L ← π_V† and π_V resets; then b/t/p/d are credited to every validator whose signature appears in the matching extrinsic, and g to the block author H_I"
 ],
 "answer": 0,
 "optNotes": [
  "0.8.0 先做 eq. 13.4（assurance）再做 13.5（rollover），六個 counter 與各自的歸屬也都對。",
  "eq. 13.2 明列六個欄位含 a；π_C 記的是每個 core 被打勾的次數；rollover 是 π_L ← π_V† 的交棒。",
  "描述的是 0.7.2 的順序：0.8.0 邊界那塊的 assurance 會被封進 π′_L，而不是留在新的 π′_V。",
  "兩組規則對調了：b/t/p/d 全部只加在 H_I，g 才看 κ′[v] 是否落在 reporters set 裡。",
 ],
 "explanation": "eq. 13.1：π_V, π_L ∈ [(b, t, p, d, g, a)]，|π_V| = |κ|、|π_L| = |λ|。eq. 13.4：π_V† = π_V 但 ∀v：a += (∃a ∈ E_A: a_v = v)——用 prior κ 的索引，**先**於 rollover；eq. 13.5：e′ = e 時 (π_V‡, π′_L) = (π_V†, π_L)，否則 ([0…], π_V†)；eq. 13.6：π′_V = π_V‡ 但 b += (v = H_I)、t += |E_T|（作者）、p += |E_P|、d += Σ|d|（作者）、g += (κ′[v] ∈ R)。0.8.0 把 assurance 的計入移到 rollover 之前（0.7.2 是一起算），你們 issue digest：「assurances credited before epoch rollover in 0.8.0」。§13 開頭：JAM 不直接發獎勵，只提供資料給 staking 子系統。",
 "trap": "每個 validator 每塊最多 +1 assurance、+1 guarantee（存在性判斷，不是數量）。"
},
{
 "id": "ch13-core-service-stats",
 "ch": "13", "section": "13.2 Cores and Services", "gpRef": "eq. 13.7, 13.9–13.12",
 "difficulty": 3, "kind": "concept", "tags": ["statistics"],
 "stem": "Core statistics π_C and service statistics π_S are per-block (not per-epoch). Which description of the core statistics is correct?",
 "options": [
  "Per core: d (DA load) = Σ over the reports that became AVAILABLE this block (the set R) on that core of bundle length + W_G·⌈65·segment_count/64⌉; p (popularity) = the number of assurances whose bitfield has that core set; i, x, z, e, u and l are summed over the reports GUARANTEED this block (the set I) on that core",
  "Per core: d (DA load) = Σ over the reports GUARANTEED this block (the set I) on that core of bundle length + W_G·⌈65·segment_count/64⌉; p (popularity) = the number of reports guaranteed on that core; i, x, z, e, u and l are summed over I as well, so every field of π′_C comes from one and the same source",
  "Per core: d (DA load) = Σ over the reports that became AVAILABLE this block (the set R) on that core of bundle length + W_G·segment_count, the paged proofs not being counted; p (popularity) = the number of assurances whose bitfield has that core set; i, x, z, e, u and l are summed over R as well, so all eight fields follow availability",
  "Per core: d (DA load) = Σ over the reports that became AVAILABLE this block (the set R) on that core of bundle length + W_G·⌈65·segment_count/64⌉; p (popularity) = the number of guarantor signatures backing that core's reports; i, x, z, e and u are summed over the reports GUARANTEED this block (the set I), but l is the largest bundle length on that core rather than their sum"
 ],
 "answer": 0,
 "optNotes": [
  "d 對 R（本塊剛 available）求和、i/x/z/e/u/l 對 I（本塊 guaranteed）求和，兩個來源分得清楚。",
  "d 的來源是 R 而非 I；p 是對 E_A 的 availability bitfield 求和（Σ_a a_f[c]），與 report 數無關。",
  "65/64 正是把每 64 個 export segment 多出的那一頁 paged proof 算進去；R(c)、L(c) 的範圍是 I。",
  "p 仍然是 assurance 打勾數；L(c) 是該 core 上所有 report 的 bundle length 總和而不是最大值。",
 ],
 "explanation": "eq. 13.9–13.12：π′_C[c] = (d = D(c), p = Σ_a a_f[c], i, x, z, e from R(c), l = L(c), u refine gas)。R(c) 與 L(c) 對 **I**（本塊 E_G 進來的 report，w_c = c）求和；D(c) 對 **R**（本塊剛 available 的 report）求和：bundle length + W_G·⌈k·65/64⌉——65/64 是因為每 64 個 export segment 會多一頁 paged-proof segment（§14）。popularity = 本塊 assurance 中對該 core 打勾的數量。你們 code-map 3.9：「DA load is computed from W while imports/exports/gas/bundle-size come from w」。",
 "trap": "兩個不同來源（guaranteed vs available）——面試容易考。"
},
{
 "id": "ch13-service-stats",
 "ch": "13", "section": "13.2 Cores and Services", "gpRef": "eq. 13.8, 13.13–13.17",
 "difficulty": 2, "kind": "concept", "tags": ["statistics"],
 "stem": "Which services appear in π′_S for a block, and what does the accumulation entry hold?",
 "options": [
  "s = services with a digest in this block's reports ∪ services that received a preimage in E_P ∪ keys of the accumulation statistics; the entry holds provision (count, total size) from E_P, refinement (count, gas), imports/extrinsics/exports, and accumulation = S(s) = (items N, transfers T, gas G) or (0,0,0)",
  "s = every service in keys(δ), so π′_S carries one entry per existing account in every block; the entry holds provision (count, total size) from E_P, refinement (count, gas), imports/extrinsics/exports, and accumulation = S(s) = (items N, transfers T, gas G) or (0,0,0)",
  "s = the keys of the accumulation statistics only, so a service that was merely reported on or that received a preimage this block gets no entry at all; the entry holds provision (count, total size) from E_P, refinement (count, gas), imports/extrinsics/exports, and accumulation = (items N, gas G)",
  "s = every service touched since the start of the epoch, since π_S accumulates across an epoch and is cleared only when e′ ≠ e; the entry holds provision (count, total size) taken from the digests, refinement (count, gas), imports/extrinsics/exports, and accumulation = S(s) = (items N, transfers T, gas G) or (0,0,0)"
 ],
 "answer": 0,
 "optNotes": [
  "s^R ∪ s^P ∪ keys(S) 三個來源都算進去，且 0.8.0 的 accumulation 是 (N, T, G) 三元組。",
  "π_S 是 per-block 的活動紀錄，沒活動的 service 根本不列，不會每個帳戶每塊都有一筆。",
  "本塊被 report 或收到 preimage 但沒 accumulate 者仍要列；(N, G) 是 0.7.2 的形狀。",
  "§13.2 明說 core 與 service 統計 tracked only on a per-block basis；provision 的 (1, |d|) 對 E_P 求和。",
 ],
 "explanation": "eq. 13.13–13.17：s = s^R（reported）∪ s^P（provided）∪ keys(S)；π′_S[s] = (p provision = Σ (1, |d|) over E_P for s, r refinement = (count, gas used) over digests, i, x, z, e, a accumulation = S(s) 或 (0,0,0))。π_S 是 per-block 的，所以沒活動的 service 不會出現；跨 epoch 累積並在 e′ ≠ e 換手的是 π_V／π_L。0.7.1 拿掉 on_transfer 的統計、0.8.0 (#502) 把 processed-transfer count 加回 accumulation 三元組。",
 "trap": "π_S 的 accumulation 是 (N, T, G) 三元組。"
},
]
