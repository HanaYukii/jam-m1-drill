# -*- coding: utf-8 -*-
# Chapter 12 — Accumulation; Chapter 13 — Statistics (GP 0.8.0)
ITEMS = [
{
 "id": "ch12-history-queue-state",
 "ch": "12", "section": "12.1 History and Queuing", "gpRef": "eq. 12.1–12.3",
 "difficulty": 2, "kind": "concept", "tags": ["accumulation", "state"],
  "stemZh": "ξ（accumulated）與 ω（ready）是什麼？它們各有多大？",
  "optionsZh": [
   "ξ ∈ [{H}]_E——最近 E = 600 個時槽、每槽一個已 accumulate 的 work-package 雜湊集合（一個 epoch 份的歷史）；ω ∈ [[(ℝ, {H})]]_E——每槽一串「該槽變為 available 但依賴仍未滿足」的 report，每筆配上它尚未滿足的依賴集合",
   "ξ ∈ [{H}]_E——最近 E = 600 個時槽、每槽一個已 accumulate 的 work-report 雜湊集合（一個 epoch 份的歷史）；ω ∈ [[(ℝ, {H})]]_E——每槽收錄該槽變為 available 的每一份 report，不論依賴是否已滿足，每筆配上它原本宣告的完整依賴集合",
   "ξ ∈ {H}——一個扁平集合，裝下有史以來每一個被 accumulate 的 work-package 雜湊、永不修剪；ω ∈ [[(𝕎, {H})]]_E——每槽一串該槽變為 available 但依賴仍未滿足的 work-item，每筆配上它尚未滿足的依賴集合",
   "ξ ∈ [{H}]_C——每個 core 一個已 accumulate 的 work-package 雜湊集合，共 C = 341 個；ω ∈ [[(ℝ, {H})]]_C——每個 core 一條佇列，裝該 core 依賴仍未滿足的 report，每筆配上它尚未滿足的依賴集合"
  ],
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
 "explanation": "兩個都是**長度 E = 600 的環狀緩衝**，也就是「一個 epoch 份的歷史」。**ξ（accumulation history，eq. 12.1）**：ξ ∈ ⟦{H}⟧_E——每個 slot 一個集合，裝該 slot 已 accumulate 的 work-package hash；ξ_∪ 是全部的聯集。用途是**防重複**與**判斷依賴是否已滿足**。**ω（ready queue，eq. 12.3）**：ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E——每個 slot 一串「已經 available、但依賴還沒滿足」的 report，每筆配上它**尚未滿足的**依賴集合（會隨時間被扣減，不是原始清單）。**環狀怎麼轉**：ξ′[E−1] 放本塊剛 accumulate 的 hash、其餘左移；ω′[m]（m = H_T mod E）放本塊新產生的 R^Q，而**被跳過的 slot（沒出塊的那些）會被清空**。**為什麼是一個 epoch 的長度**：依賴等太久就沒有意義了——被依賴的 package 若一個 epoch 都沒出現，等下去也不會出現。所以懸而未決的 report 最終會被環狀覆蓋而自然消失，**不需要額外的清理機制**。這也表示「依賴解不開」不會讓區塊無效，只是那份工作靜靜地過期。這正是 test vectors 裡 accumulate 目錄的 enqueue／unlock／ring-wrap 三類案例在測的東西。",
 "trap": "ξ 存的是 package hash 不是 report hash；ready 的依賴在每次 accumulate 後用 E() 修剪。"
},
{
 "id": "ch12-W-partition",
 "ch": "12", "section": "12.1 History and Queuing", "gpRef": "eq. 12.4–12.12 (W!, W^Q, E, Q, W*)",
 "difficulty": 3, "kind": "concept", "tags": ["accumulation", "dependencies"],
  "stemZh": "可被 accumulate 的 report 序列 R* 是怎麼從新變為 available 的 report R 建構出來的？",
  "optionsZh": [
   "R! = 沒有 prerequisites 且 segment-root lookup 為空的 report，立即 accumulate；R^Q = 其餘者，各自配上依賴集合（prerequisites ∪ srlookup 的 key）並先用 ξ_∪ 修剪；R* = R! ⌢ Q(E(ω[m..] ⌢ ω[..m] ⌢ R^Q, P(R!)))，其中 Q 反覆取出依賴集合為空的 report、E 則扣掉已滿足的依賴",
   "R! = 沒有 prerequisites 且 segment-root lookup 為空的 report，立即 accumulate；R^Q = 其餘者，各自配上依賴集合（prerequisites ∪ srlookup 的 key）並先用 ξ_∪ 修剪；R* = R! ⌢ Q(E(ω[..m] ⌢ ω[m..] ⌢ R^Q, P(R!)))，也就是 ready queue 從當前時槽 m 往後讀，好讓最新排入的 report 先輪到",
   "R! = 沒有 prerequisites 的 report（不論其 segment-root lookup 裝了什麼），立即 accumulate；R^Q = 其餘者，各自只配上 prerequisite 集合，並只用 ξ[E−1]（僅前一槽 accumulate 掉的 package）修剪；R* = R! ⌢ Q(E(ω[m..] ⌢ ω[..m] ⌢ R^Q, P(R!)))，Q 取出依賴集合為空的 report",
   "R! = 沒有 prerequisites 且 segment-root lookup 為空的 report，立即 accumulate；R^Q = 其餘者，各自配上依賴集合（prerequisites ∪ srlookup 的 key）並先用 ξ_∪ 修剪；R* = R! ⌢ Q(E(ω[m..] ⌢ ω[..m] ⌢ R^Q, P(R!)))，其中 Q 對佇列只走一遍，事後仍持有依賴的 report 會讓該區塊無效"
  ],
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
 "explanation": "整段是一條流水線，分三步。**① 分流**（eq. 12.4–12.5）：R! = 沒有 prerequisites 且 segment-root lookup 為空的 report——**可以立刻做**；其餘進 R^Q，每筆配上依賴集合 D(r) = prerequisites ∪ keys(r_l)，並先用 ξ_∪ 把「已經做過的」扣掉。**② 兩個工具函數**（eq. 12.7–12.8）：E(r, x) 把 package hash 落在 x 裡的項目移除、並從其餘各項的依賴集合中扣掉 x；Q(r) = g ⌢ Q(E(r, P(g)))，g 是當前依賴集合為空的那些——**反覆「取出可做的、扣掉、再取」直到沒有東西可取**，是一個標準的拓撲排序。**③ 組裝**（eq. 12.11–12.12）：R* = R! ⌢ Q(E(ω[m..] ⌢ ω[..m] ⌢ R^Q, P(R!)))。**注意 ready queue 的讀取順序**：ω[m..] 接 ω[..m]，m = H_T mod E——從**最舊**的 slot 開始繞一圈，等最久的先處理，避免飢餓。**兩個容易誤答的方向**：其一，**依賴解不開不會讓區塊無效**——那份 report 就留在 ω 裡，一個 epoch 後被環狀覆蓋而過期。其二，R! 一定排在最前面，因為它們無依賴、且它們的完成可能正好解開後面那些的依賴（P(R!) 就是傳這個）。",
 "trap": "E 的參數 x 在第一次是 P(R!)（本塊立即 accumulate 者的 hash），不是整個 ξ（R^Q 已先用 ξ_∪ 修剪過）。"
},
{
 "id": "ch12-gas-budget",
 "ch": "12", "section": "12.3 Final State Integration", "gpRef": "eq. 12.24 (g) & 12.17 (Δ+)",
 "difficulty": 3, "kind": "delta", "tags": ["accumulation", "gas", "delta-0.8.0"],
  "stemZh": "一個區塊交給外層 accumulation Δ+ 的總 gas 預算 g 是多少？Δ+ 又是怎麼決定一輪要 accumulate 幾份 report 的？",
  "optionsZh": [
   "g = max(G_T, G_A·C + Σ_{x∈values(χ_Z)} x)；Δ+ 取最大的前綴 i，使得那 i 份 report 的 digest gas 上限總和 + 待處理 deferred transfer 的 gas 總和 + free-accumulation 的 gas 總和 ≤ g，對它們執行 Δ*，然後以 g* = g + Σ(新產生 transfer 的 gas) − Σ 實際用掉的 gas、以及一個空的 free-accumulation 映射遞迴下去",
   "g = max(G_T, G_A·C + Σ_{x∈values(χ_Z)} x)；Δ+ 取最大的前綴 i，使得只有那 i 份 report 的 digest gas 上限總和 ≤ g——transfer 的 gas 與 free-accumulation 的 gas 都不參與這個判斷——對它們執行 Δ*，然後以 g* = g − Σ 實際用掉的 gas 遞迴，並把同一個 free-accumulation 映射帶進每一輪",
   "g 恰好是 G_A·C = 3.41·10^9，而 always-accumulate 的額度 χ_Z 也從這個總額裡支出；Δ+ 取最大的前綴 i，使得 digest gas 上限總和 + 待處理 deferred transfer 的 gas 總和 ≤ g，對它們執行 Δ*，然後以 g* = g − Σ 實際用掉的 gas 與同一個 free-accumulation 映射遞迴",
   "g = G_R = 5·10^9，也就是把每個 package 的 refine 額度直接拿來當區塊的 accumulation 預算；Δ+ 每一輪只 accumulate 一份 report 而不是一個前綴，每次從 g 扣掉那份 report 實際用掉的 gas，並在任何 service 的 Accumulate panic 時立即停止，丟棄其餘 report 與它們產生的 transfer"
  ],
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
  "stemZh": "在 Δ*（平行 accumulation）中，哪些 service 會被 accumulate？當 manager 與某個具特權的 service 同時寫入同一個特權索引——assigners、delegator 或 registrar——時，哪一次寫入會存活？",
  "optionsZh": [
   "s = {有 digest 的 service} ∪ keys(f) ∪ {deferred transfer 的收款方}；每一個都透過 Δ1 恰好被 accumulate 一次；χ′_M 與 χ′_Z 單獨由 manager 的輸出決定；至於 assigners、delegator 與 registrar，衝突解析函數是 R(o, a, b) = b 當 a = o、否則為 a",
   "s = 只有 {有 digest 的 service}，所以僅僅收到 deferred transfer 或享有 free accumulation 的 service 會被略過；每一個都透過 Δ1 恰好被 accumulate 一次；χ′_M 與 χ′_Z 單獨由 manager 的輸出決定，而 assigners、delegator 與 registrar 只有 manager 能更動",
   "s = keys(δ) 裡的每一個 service；每個 service 是每份 digest 被 accumulate 一次而非每輪一次，所以持有三份 digest 的 service 會跑三次 Δ1；χ′_M 與 χ′_Z 單獨由 manager 的輸出決定；同一輪內若某個特權同時被 manager 與它當前的持有者更動，該區塊無效",
   "s = {有 digest 的 service} ∪ keys(f) ∪ {deferred transfer 的收款方}；每一個都透過 Δ1 恰好被 accumulate 一次；χ′_M 與 χ′_Z 取自 registrar 的輸出；衝突解析函數是 R(o, a, b) = a 當 a = o、否則為 b"
  ],
  "stem": "In Δ* (parallel accumulation), which services get accumulated? And when the manager and a privileged service both write to the same privileged index — assigners, delegator or registrar — which write survives?",
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
  "stemZh": "對單一個 service s，Δ1 會呼叫 Ψ_A(e, τ′, s, g, i^T ⌢ i^U)。gas g 是怎麼算出來的？輸入又是什麼？",
  "optionsZh": [
   "g = f[s]（free 額度，若無則為 0）+ 送往 s 的 deferred transfer 的 gas 總和 + 本輪各 report 中屬於 s 的 digest 之 accumulate gas 上限總和；i^T 是送往 s 的 transfer（依序），i^U 是 s 的每份 digest 一個運算元組（依 report 順序）",
   "g = f[s]（free 額度，若無則為 0）+ 送往 s 的 deferred transfer 的 gas 總和，而 digest 的 accumulate gas 上限不加進來，因為 Δ+ 已經把它們計入區塊預算了；i^T 是送往 s 的 transfer（依序），i^U 是 s 的每份 digest 一個運算元組（依 report 順序）",
   "g = δ[s]_g，也就是該 service 自己的 minaccgas，並以 G_A = 10^7 為上限；i^T 是送往 s 的 transfer（依序），i^U 是每份至少含有一個 s 之 digest 的 work-report 一個運算元組，而不是每份 digest 一個",
   "g = f[s]（free 額度，若無則為 0）+ 送往 s 的 deferred transfer 的 gas 總和 + 本輪各 report 中屬於 s 的 digest 之 accumulate gas 上限總和；但引數序列是 i^U ⌢ i^T，本輪的運算元組排在任何從上一輪帶過來的 transfer 之前"
  ],
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
  "stemZh": "一筆 deferred transfer T = (s, d, a, m, g)。這些欄位是什麼？餘額又是在什麼時候移動的？",
  "optionsZh": [
   "s 來源 service、d 目的地、a 金額、m 為 W_T = 128 個 octet 的 memo、g 是給收款方處理用的 gas 上限；發送方的餘額在呼叫 `transfer` 當下就被扣除，而該金額要到之後某一輪目的地被 accumulate 時才入帳",
   "s 是發送方的 Ed25519 公鑰、d 是目的 service、a 是金額、m 是 32 個 octet 的 memo 雜湊、g 是發送方願意支付的 gas 價格；發送方的餘額在呼叫 `transfer` 當下被扣除，並在同一輪 Δ* 之內就入帳給目的地",
   "s 來源 service、d 是目的 core 索引、a 金額、m 為 W_T = 128 個 octet 的 memo、g 是給收款方處理用的 gas 上限；在目的地真正被 accumulate 之前發送方分文未失，所以一筆指向同輪內被刪除之 service 的轉帳，對發送方毫無成本",
   "s 來源 service、d 目的地、a 金額、m 為 W_T = 128 個 octet 的 memo、g 是給收款方處理用的 gas 上限；發送方在呼叫 `transfer` 時被扣款，而目的地在同一輪稍後由 Δ* 在 digest 處理完之後所呼叫的獨立 on-transfer 進入點 Ψ_T 入帳"
  ],
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
 "explanation": "eq. 12.14：T ≡ (s, d, a, m, g)——source service、destination、amount、**memo m ∈ B_{W_T}（W_T = C_memosize = 128 位元組，定長）**、以及給接收方處理用的 gas 上限。**扣款與入帳不同步，這是這題的核心。** 呼叫 `transfer`（host call 21）的當下就會：檢查 d 存在（否則 WHO）、g 不低於 δ[d] 的最低 memo gas（否則 LOW）、扣款後自己的餘額仍不低於門檻 a_t（否則 CASH）；三關都過就**立刻從 sender 扣除 a**，並把 T 追加到本次 accumulate 的 transfers 序列。**接收方要到下一輪 Δ+ 才收到**：那些 T 會被當成 input 餵給遞迴呼叫（Δ+ 的 t*），此時金額才加到收款方帳上，收款方也才有機會用 g 的預算執行自己的處理邏輯。**所以有一個很現實的後果**：轉給「不存在、或在本輪被刪除」的 service，那筆 transfer 會被丟棄，**但 sender 早就被扣了錢**——這不是 bug，是「先扣後送」的必然結果，服務端要自己確認目標存在。**為什麼要延後**：若轉帳在呼叫當下就同步執行接收方的程式碼，accumulate 之間就會產生任意深度的重入（reentrancy），gas 計價與確定性都會失控。",
 "trap": "memo 固定 128 bytes；g 是給接收方處理這筆 transfer 的 gas，會計入下一輪預算。"
},
{
 "id": "ch12-outputs",
 "ch": "12", "section": "12.3 Final State Integration", "gpRef": "eq. 12.24–12.33 (δ† → δ‡ → δ′)",
 "difficulty": 2, "kind": "concept", "tags": ["accumulation", "state"],
  "stemZh": "Δ+ 回傳 (n, e′, b, u, t) 之後，關於最終整合的哪些敘述是正確的？",
  "optionsZh": [
   "θ′ = b 中的 (service, 雜湊) 配對（那些 yield 出 32 位元組雜湊的 service）；(δ†, ι′, φ′, χ′) 來自 e′；accumulation 統計逐 service 記錄（accumulate 掉的項數 N、處理掉的 transfer 數 T、用掉的 gas G）；δ‡ 把出現在統計裡的每個 service 的 a_a 標記為 τ′；ξ′[E−1] = P(R*[..n])",
   "θ′ = H(E(δ†))，一個對整份 posterior service 狀態的單一承諾；(δ†, ι′, φ′, χ′) 來自 e′；accumulation 統計逐 service 記錄（N、T、G）；δ‡ 把出現在統計裡的每個 service 的 a_a 標記為 τ′；ξ′[E−1] = P(R*)，也就是整個可 accumulate 序列",
   "θ′ = b 中的 (service, 雜湊) 配對；(δ†, ι′, φ′, χ′) 來自 e′；accumulation 統計逐 service 記錄（項數 N、用掉的 gas G），transfer 計數已被移除；δ‡ 把 keys(δ†) 中每個 service 的 a_a 標記為 τ′；ξ′[E−1] = P(R*[..n])",
   "θ′ = b 中的 (service, 雜湊) 配對；(δ†, ι′, φ′, χ′) 來自 e′；accumulation 統計逐 service 記錄（N、T、G）；δ‡ 把出現在統計裡的每個 service 的 a_a 標記為 τ′；ξ′[E−1] = P(R*[..n])，而 ω′ 會被完全清空，因此排隊中的 report 永遠無法跨越一個區塊存活"
  ],
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
 "explanation": "Δ+ 回傳 (n, e′, b, u, t) 之後有一連串整合動作，**δ 要經過 δ† → δ‡ → δ′ 三個階段**。**n** = 這輪實際 accumulate 掉的 report 前綴長度；**e′** 裡包含新的 (δ†, ι′, φ′, χ′) —— accumulate 期間透過 host call 改動的東西都在這裡（eq. 12.26）。**b → θ′**（eq. 12.24）：θ′ ≡ [(s, h) ∈ b]，也就是有呼叫 `yield` 且回傳非 ∅ 的 service 及其 hash——這份序列接著餵給 §7 的 accumulation-output belt。**統計 S**（eq. 12.27–12.28）：S ∈ D⟨N_S → (N, T, G)⟩——每個 service 記三個數：前 n 份 report 中屬於它的 digest 數、處理掉的 transfer 數（**0.8.0 PR #502 才加回來的**）、以及實際用掉的 gas。只記非 (0,0,0) 的。**δ‡**（eq. 12.29–12.30）：把 keys(S) 裡每個 service 的 a_a（最後 accumulate 時間）設為 τ′。**為什麼要記這個時間**：`eject` 需要它來判斷一個 service 是否已經長期閒置。**ξ 與 ω 的環狀更新**（eq. 12.31–12.33）：ξ′[E−1] = P(R*[..n])、其餘左移；ω′ 依 m = H_T mod E 更新。**注意 δ′ 還沒完成**——preimage 的整合（eq. 12.37）還在後面，δ‡ 只是中間態。",
 "trap": "a_a（last accumulation slot）只對「這塊真的 accumulate 過」的 service 更新。"
},
{
 "id": "ch12-preimage-integration",
 "ch": "12", "section": "12.4 Preimage Integration", "gpRef": "eq. 12.34–12.37",
 "difficulty": 2, "kind": "concept", "tags": ["accumulation", "preimages"],
  "stemZh": "哪一條規則管轄 preimages extrinsic E_P 以及它併入 δ′ 的方式？",
  "optionsZh": [
   "E_P ∈ [(s, d)] 依序且唯一；每一組 (s, d) 都必須在 prior 的 δ 上為 providable——該 service 存在，且 δ[s]_l[(H(d), |d|)] = []（已請求、尚未提供）；整合發生在 accumulation 之後：δ′ = I(δ‡, E_P)，把 a_l[(H(d),|d|)] 設為 [τ′] 並寫入 a_p[H(d)] = d，任何已不再有用的 preimage 會被靜默丟棄",
   "E_P ∈ [(s, d)] 依序且唯一；每一組 (s, d) 都必須在 posterior 的 δ‡ 上為 providable——該 service 在那裡必須仍然存在且 δ‡[s]_l[(H(d), |d|)] = []——所以同一塊內被 accumulation 撤掉的 request 會讓整個區塊無效；接著整合為 δ′ = I(δ‡, E_P)，設定 a_l 與 a_p",
   "E_P ∈ [(s, d)] 依序且唯一；任何 preimage 都可以被納入，不論該 service 是否請求過，因為 I 會保存交給它的每一組；整合發生在 accumulation 之前，δ† = I(δ, E_P)，好讓 service 的 Accumulate 能讀到同一塊內提供的 preimage，並設定 a_l 與 a_p",
   "E_P ∈ [(s, d)] 只需沒有重複，排序不受限制；每一組 (s, d) 都必須在 prior 的 δ 上為 providable，而且還必須由該 service 的 manager 簽署；整合發生在 accumulation 之後：δ′ = I(δ‡, E_P)，設定 a_l 與 a_p，任何已不再有用的 preimage 會被靜默丟棄"
  ],
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
 "explanation": "兩個階段，**檢查用 prior、整合在 accumulation 之後**。**檢查**（eq. 12.34–12.36）：E_P ∈ ⟦(N_S, B)⟧，依 (service, data) 排序且唯一；每筆必須在 **prior 的 δ** 上「providable」——即 s ∈ keys(δ) 且 δ[s]_l[(H(d), |d|)] = **[]**，也就是**已經被 solicit 但還沒有人提供**。注意空序列 [] 是關鍵：已經提供過的（[x]）或曾被移除的（[x, y]）都不算 providable，這防止同一份 preimage 被重複塞進來。**整合**（eq. 12.37）：δ′ = I(δ‡, E_P)——**在 accumulation 跑完之後**才做，把 request 設為 [τ′]、並把 blob 寫入 a_p。**為什麼順序是這樣，以及它的副作用**：因為檢查用 prior、整合用 posterior，中間隔了一整段 accumulation；若在這段期間該 service 被 `eject` 刪掉、或該 request 被 `forget` 撤銷，這筆 preimage 就會被**「disregarded, without prejudice」——靜靜丟棄，但區塊仍然有效**。這是刻意的：出塊者在打包時無法預知 accumulation 會怎麼改動狀態，若因此讓整塊無效，出塊會變得極難。你們的兩個錯誤碼 preimages not sorted and unique 與 preimage not required 分別對應這兩條檢查。",
 "trap": "驗證看 prior δ、整合作用於 δ‡；順序題在 fuzzer 很常出現。"
},
{
 "id": "ch12-code-outer-accumulation",
 "ch": "12", "section": "12.2 Execution", "gpRef": "eq. 12.17 — internal/accumulation/accumulation.go OuterAccumulation",
 "difficulty": 3, "kind": "code", "tags": ["accumulation", "code", "delta-0.8.0"],
  "stemZh": "這是團隊在 Δ+ 中的前綴選取程式碼。對照 GP 0.8.0 的 eq. 12.17，還缺了什麼？",
  "optionsZh": [
   "0.8.0 要求預算判斷必須把待處理 deferred transfer 的 gas 總和 t 與 free-accumulation 額度總和 f 一併計入（Σ d_g + Σ t_g + Σ f ≤ g），所以 gasSum 必須從那兩個總和起算而不是從 0",
   "用錯了 gas 數字：eq. 12.17 在該前綴上加總的是每份 digest 實際用掉的 gas d_u 而不是宣告的上限 d_g，因為 Δ* 會在預算被檢查之前先把真實用量交回來",
   "判斷應該逐份 report 進行而不是累計：eq. 12.17 要求 r[..i] 中的每一份 report 各自滿足 Σ d_g ≤ G_A = 10^7，所以迴圈必須在第一份超過該單份上限的 report 處中斷",
   "i 的界限錯了：eq. 12.17 是在 N_{|r|+1} 上取最大值，所以 i 可以到達 |r|，而迴圈裡的 `i = idx + 1` 卻把它卡在 |r| − 1，永遠會把最後一份 report 留給下一輪"
  ],
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
 "explanation": "eq. 12.17（0.8.0）：i = max{ i ∈ N_{|r|+1} : Σ_{r ∈ r[..i], d ∈ r_d} d_g + **Σ_{t ∈ t} t_g** + **Σ_{x ∈ values(f)} x** ≤ g }。**加粗的兩項就是 0.7.2 缺的**：待處理 deferred transfer 的 gas，與 always-accumulate 服務的免費額度。PR #500「Account for gas reserved by transfer and always acc items」把它們納入預算判斷——所以 gasSum 必須從這兩個總和起算，而不是從 0。**不加會怎樣**：這一輪選進來的 report 看起來還在預算內，但實際執行時還要付 transfer 的處理費與 always-acc 的額度，**總量就超過 g 了**。換句話說舊版是「事後才發現超支」，新版是「事前就把已承諾的支出算進去」。n = |t| + i + |f| 這條在兩版都一樣，沒有改。**背後的道理 §12.2 講得很清楚**：「Only after a work-item is accumulated can it be known if it uses less gas than the advertised limit」——宣告的 gas 只是上限，實際用量要等做完才知道，所以下一輪的預算得靠 g* = g + Σ t* 的 gas − Σ 實際用量 回饋修正。**這是一個「保守預估 + 事後結算」的模型**，預估這一步漏算任何一項都會讓保守性失效。",
 "trap": "你們 issue digest 提到：eq:accseq budget now includes transfer gas + free allowances。"
},
{
 "id": "ch13-validator-stats",
 "ch": "13", "section": "13.1 Validator Activity", "gpRef": "eq. 13.1–13.6",
 "difficulty": 2, "kind": "delta", "tags": ["statistics", "delta-0.8.0"],
  "stemZh": "π ≡ (π_V, π_L, π_C, π_S)。在 GP 0.8.0 中，關於 validator 統計的哪個敘述正確？",
  "optionsZh": [
   "每位 validator 的紀錄有六個計數器（出塊 b、ticket t、preimage 數 p、preimage 大小 d、guarantee g、assurance a）；本塊的 assurance 在 epoch 換屆判斷之前就記進 π_V†；當 e′ ≠ e 時 π_L ← π_V† 且 π_V 重設；接著 b/t/p/d 記給出塊者 H_I，而 g 記給 reporters 集合 G 裡的每一位",
   "每位 validator 的紀錄有五個計數器（b、t、p、d、g），assurance 改為逐 core 記在 π_C 裡；當 e′ ≠ e 時 π_V 與 π_L 都被歸零，好讓新 epoch 從零開始；接著 b/t/p/d 記給出塊者 H_I，而 g 記給 reporters 集合 G",
   "每位 validator 的紀錄有六個計數器；本塊的 assurance 在 epoch 換屆判斷之後才記，所以當 e′ ≠ e 時它們會落進全新的 π′_V 而不是 π′_L；π_L 取的則是 π_V 而不是 π_V†；b/t/p/d 給出塊者 H_I、g 給 reporters 集合 G",
   "每位 validator 的紀錄有六個計數器；本塊的 assurance 在 epoch 換屆判斷之前就記進 π_V†；當 e′ ≠ e 時 π_L ← π_V† 且 π_V 重設；接著 b/t/p/d 記給每一位其簽章出現在對應 extrinsic 中的 validator，而 g 記給出塊者 H_I"
  ],
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
  "alsoCh": ["11"],
 "ch": "13", "section": "13.2 Cores and Services", "gpRef": "eq. 13.7, 13.9–13.12",
 "difficulty": 3, "kind": "concept", "tags": ["statistics"],
  "stemZh": "core 統計 π_C 與 service 統計 π_S 都是逐區塊（而非逐 epoch）的。關於 core 統計的哪個描述正確？",
  "optionsZh": [
   "逐 core：d（DA 負載）= 對本塊變為 available 的那些 report（集合 R）中屬於該 core 者，加總 bundle 長度 + W_G·⌈65·segment 數/64⌉；p（popularity）= bitfield 設起該 core 的 assurance 數量；i、x、z、e、u、l 則是對本塊被擔保的那些 report（集合 I）中屬於該 core 者加總",
   "逐 core：d（DA 負載）= 對本塊被擔保的那些 report（集合 I）中屬於該 core 者，加總 bundle 長度 + W_G·⌈65·segment 數/64⌉；p（popularity）= 在該 core 上被擔保的 report 數量；i、x、z、e、u、l 也同樣對 I 加總，所以 π′_C 的每個欄位都出自同一個來源",
   "逐 core：d（DA 負載）= 對本塊變為 available 的那些 report（集合 R）中屬於該 core 者，加總 bundle 長度 + W_G·segment 數，不計 paged proof；p（popularity）= bitfield 設起該 core 的 assurance 數量；i、x、z、e、u、l 也同樣對 R 加總，所以八個欄位全都跟隨可得性",
   "逐 core：d（DA 負載）= 對本塊變為 available 的那些 report（集合 R）中屬於該 core 者，加總 bundle 長度 + W_G·⌈65·segment 數/64⌉；p（popularity）= 支持該 core 各 report 的 guarantor 簽章數量；i、x、z、e、u 對本塊被擔保的那些 report（集合 I）加總，但 l 是該 core 上最大的 bundle 長度而不是它們的總和"
  ],
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
 "explanation": "π_C 每個 core 一組，**但不同欄位的求和對象不同，這正是最容易記錯的地方**。**d（DA load，資料可得性負載）對的是 R**——**本塊剛變成 available 的** report，D(c) = Σ (bundle 長度 + W_G · ⌈65 · segment 數 / 64⌉)。那個 65/64 的係數是因為**每 64 個匯出 segment 會多一頁 paged-proof segment**（§14），所以實際要分發的資料比 segment 本身多約 1.6%。**p（popularity）** = 本塊 assurance 中對該 core 打勾的數量，Σ_a a_f[c]。**i、x、z、e、u、l 對的是 I**——**本塊 E_G 帶進來（被 guarantee）的** report。**為什麼要分兩個來源**：guarantee 與 available 是**不同時間點的事件**，同一份 report 通常在某一塊被 guarantee、在之後某一塊才湊滿背書變成 available。「這塊 core 產生了多少工作」要看 I，「這塊 core 造成多少資料分發負擔」要看 R——混用會讓兩種統計都失真。你們 code-map 3.9 的註記正是這件事：「DA load is computed from W while imports/exports/gas/bundle-size come from w」。**另外記住 π_C 與 π_S 都是 per-block**（每塊重算，不累積），跨 epoch 累積的是 π_V／π_L。",
 "trap": "兩個不同來源（guaranteed vs available）——面試容易考。"
},
{
 "id": "ch13-service-stats",
 "ch": "13", "section": "13.2 Cores and Services", "gpRef": "eq. 13.8, 13.13–13.17",
 "difficulty": 2, "kind": "concept", "tags": ["statistics"],
  "stemZh": "一個區塊的 π′_S 裡會出現哪些 service？accumulation 那一項又裝什麼？",
  "optionsZh": [
   "s = 在本塊各 report 中有 digest 的 service ∪ 在 E_P 中收到 preimage 的 service ∪ accumulation 統計的 key；每項裝有來自 E_P 的 provision（筆數、總大小）、refinement（筆數、gas）、imports／extrinsics／exports，以及 accumulation = S(s) = (項數 N, transfer 數 T, gas G) 或 (0,0,0)",
   "s = keys(δ) 裡的每一個 service，所以每個區塊的 π′_S 都為每個現存帳戶帶一項；每項裝有來自 E_P 的 provision（筆數、總大小）、refinement（筆數、gas）、imports／extrinsics／exports，以及 accumulation = S(s) 或 (0,0,0)",
   "s = 只有 accumulation 統計的 key，所以本塊僅僅被回報過、或僅僅收到 preimage 的 service 完全不會有條目；每項裝有來自 E_P 的 provision（筆數、總大小）、refinement（筆數、gas）、imports／extrinsics／exports，以及 accumulation = (項數 N, gas G)",
   "s = 自本 epoch 開始以來被觸及過的每個 service，因為 π_S 是跨 epoch 累積、只在 e′ ≠ e 時才清空；每項裝有取自 digest 的 provision（筆數、總大小）、refinement（筆數、gas）、imports／extrinsics／exports，以及 accumulation = S(s) 或 (0,0,0)"
  ],
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
 "explanation": "**哪些 service 會出現**（eq. 13.13）：三個來源的聯集——s^R（本塊 report 裡有 digest 的）∪ s^P（本塊 E_P 有提供 preimage 的）∪ keys(S)（有 accumulate 活動的）。**π_S 是 per-block 的，所以沒有任何活動的 service 根本不會出現**在這一塊的統計裡，不是記成零。這與 π_V／π_L 不同——後者是跨 epoch 累積、在 e′ ≠ e 時整批換手。**每筆記什麼**（eq. 13.14–13.17）：p（provision）= 對本塊 E_P 中屬於它的每筆累加 (1, |d|)；r（refinement）= digest 的筆數與 refine 用掉的 gas；i、x、z、e = import／extrinsic／export 的計數；a（accumulation）= S(s) = (item 數, transfer 數, gas)，沒有活動則是 (0, 0, 0)。**版本沿革值得記，因為是 delta 考點**：0.7.1 拿掉了 `on_transfer` 的統計；0.8.0（PR #502）又把「處理掉的 transfer 數」加回 accumulation 那個三元組裡。**為什麼要分這麼細**：這些數字是未來計費與獎勵分配的依據——refine 與 accumulate 的成本結構完全不同（一個 in-core、一個 on-chain），混在一起就無法分別定價。",
 "trap": "π_S 的 accumulation 是 (N, T, G) 三元組。"
},
]
