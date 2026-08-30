# -*- coding: utf-8 -*-
# Appendix B — Virtual Machine Invocations & host calls (GP 0.8.0)
ITEMS = [
{
 "id": "appB-result-constants",
 "ch": "B", "section": "B.1 Result Constants; Omega_A (assign)", "gpRef": "§B.1; Ω_A",
 "difficulty": 2, "kind": "concept", "tags": ["host-calls", "privileges"],
 "stem": "A service calls `assign` to give core c a fresh authorizer queue and name a new assigner. Ω_A can refuse that call for four different reasons, tested in a fixed order. Which ladder is right, and what separates one constant from the next?",
 "options": [
  "A queue that cannot be read out of memory panics; a core index at or beyond C gives CORE; a caller that is not that core's current assigner gives HUH; a nominated assigner outside the service-id set gives WHO. Each constant names what kind of thing is wrong: the out-of-range index, the absent privilege, the unresolvable identity.",
  "A queue that cannot be read out of memory panics; a core index at or beyond C gives CORE; a nominated assigner outside the service-id set gives WHO; a caller that is not that core's current assigner gives HUH. Privilege comes last so that a structurally broken call is never turned away merely for who happened to submit it.",
  "A queue that cannot be read out of memory panics; a caller that is not that core's current assigner gives WHO; a core index at or beyond C gives CORE; a nominated assigner outside the service-id set gives WHAT. WHO names the party that made the call, and WHAT names an argument the host could not resolve to anything.",
  "A queue that cannot be read out of memory gives OOB; a core index at or beyond C gives CORE; a caller that is not that core's current assigner gives HUH; a nominated assigner outside the service-id set gives WHO. A memory fault is reported rather than fatal here, so accumulation carries on and the caller may retry."
 ],
 "answer": 0,
 "explanation": "Ω_A（`assign` = 16）把四種失敗排成一道有序的階梯：q = error（要寫進佇列的那段記憶體不可讀）→ panic；c ≥ C → CORE；呼叫者 ≠ χ_A[c]（該 core 目前的 assigner）→ HUH；新的 assigner a ∉ 𝕊（不是合法 service id）→ WHO；其餘 OK。分工的原則是「常數描述的是哪一種東西壞了」：越界的索引用它專屬的常數（§B.1 逐字：CORE = core index unknown），權限不足一律是 HUH（§B.1：the operation is invalid… or the service is insufficiently privileged），解析不出來的身分是 WHO（index unknown）。順序本身也有意義：先確定 core 存不存在，再確定你有沒有權動它，最後才看你要塞進去的值合不合法。兩個常被混用的：WHAT 不是給參數用的，它是 Ω 派送表的 otherwise 分支——host call 編號本身不認得（Name unknown），且只扣 C_gasunknown；OOB 則專指 inner PVM 的記憶體索引不可存取，跟 accumulate 自己的記憶體無關——後者讀不到就直接 panic。",
 "optNotes": [
  "四段依序 panic → CORE → HUH → WHO，與 Ω_A 的 cases 逐項對上；範圍、權限、身分各有專屬常數。",
  "順序反了：GP 先檢查呼叫者是不是該 core 的 assigner，才輪到新 assigner 的 service id 合不合法。",
  "WHO 指的是解析不出來的索引或身分，不是呼叫者；WHAT 是用在整個 host call 編號不認得的時候。",
  "記憶體讀不到在 Ω_A 是直接 panic，不是回 OOB；OOB 專指 inner PVM 的記憶體索引不可存取。"
 ],
 "trap": "權限不足 → HUH；索引解析不出來 → WHO；host call 編號不認得 → WHAT。三者最常被混用。"
},
{
 "id": "appB-three-invocations",
 "ch": "B", "section": "B.2–B.4 Invocations", "gpRef": "eq. B.1–B.2, B.5–B.6, B.9–B.11",
 "difficulty": 2, "kind": "concept", "tags": ["host-calls", "pvm"],
 "stem": "The PVM has three invocation types. Which statement about their host-call sets is correct in GP 0.8.0?",
 "options": [
  "Ψ_I (is-authorized, stateless): gas, grow_heap, fetch only; Ψ_R (refine): gas, grow_heap, fetch, historical_lookup, export, machine, peek, poke, pages, invoke, expunge; Ψ_A (accumulate): gas, grow_heap, fetch, lookup, read, write, info, bless, assign, designate, checkpoint, new, upgrade, transfer, eject, query, solicit, forget, yield, provide; any other id costs M_∅ = 1000 gas and returns WHAT",
  "Ψ_I (is-authorized, stateless): gas, grow_heap, fetch only; Ψ_R (refine): gas, grow_heap, fetch, lookup, read, write, info, export, machine, peek, poke, pages, invoke, expunge; Ψ_A (accumulate): gas, grow_heap, fetch, historical_lookup, bless, assign, designate, checkpoint, new, upgrade, transfer, eject, query, solicit, forget, yield, provide; any other id costs M_∅ = 1000 gas and returns WHAT",
  "Ψ_I (is-authorized): gas, grow_heap, fetch, historical_lookup; Ψ_R (refine): gas, grow_heap, fetch, historical_lookup, lookup, read, invoke, expunge; Ψ_A (accumulate): gas, grow_heap, fetch, write, info, export, machine, peek, poke, pages, bless, assign, designate, checkpoint, new, upgrade, transfer, eject, query, solicit, forget, yield, provide; any other id costs M_∅ = 1000 gas and returns WHAT",
  "Ψ_I (is-authorized, stateless): gas, fetch only; Ψ_R (refine): gas, grow_heap, fetch, historical_lookup, export, machine, peek, poke, pages, invoke, expunge; Ψ_A (accumulate): gas, fetch, lookup, read, write, info, bless, assign, designate, checkpoint, new, upgrade, transfer, eject, query, solicit, forget, yield, provide; grow_heap is refine-only since only in-core execution may resize RAM, and any other id panics (☇) with no gas charged"
 ],
 "answer": 0,
 "optNotes": [
   "三張表分別對上 eq. B.2/B.6/B.11，未知 id 走 F 的 default：扣 M_∅ 後填 WHAT 續跑。",
   "正好顛倒——in-core 沒有共識狀態，refine 只能做依 lookup-anchor 時間的 historical_lookup。",
   "inner PVM 與 D3L export 只在 eq. B.6；eq. B.2 的 is-authorized 是 stateless，連 accounts 都拿不到。",
   "grow_heap 三張表都有（0.8.0 用它取代 sbrk 指令），且未知 id 絕不是 ☇。",
 ],
 "explanation": "eq. B.2（is-authorized mutator F）：gas、grow_heap、fetch；eq. B.6（refine）：+ historical_lookup、export、machine、peek、poke、pages、invoke、expunge（inner PVM 與 D3L export）；eq. B.11（accumulate）：+ lookup/read/write/info（透過 G 包裝，讓對自身帳戶的變更同步進 context）、bless、assign、designate、checkpoint、new、upgrade、transfer、eject、query、solicit、forget、yield、provide。分界的原理：in-core 的 refine 沒有共識狀態，只能做依 lookup-anchor 時間的 historical_lookup；accumulate 在鏈上，讀寫的是當下 partial state；is-authorized 則是 stateless，context 恆為 ∅。0.8.0（GP PR #508）把 sbrk 指令換成 grow_heap host call（index 1）並列進三張表。未知 id 走 F 的 default——扣 M_∅ = 1000 後 φ′_7 = WHAT 繼續執行，只有扣到 ϱ′ < 0 才 ∞。",
 "trap": "read/write/lookup/info 在 accumulate 才有；refine 用 historical_lookup（依 lookup-anchor 時間）。"
},
{
 "id": "appB-accumulate-invocation",
 "ch": "B", "section": "B.4 Accumulate Invocation", "gpRef": "eq. B.7–B.14",
 "difficulty": 3, "kind": "concept", "tags": ["host-calls", "accumulate"],
 "stem": "Which statement about the accumulate invocation Ψ_A(e, t, s, g, i) is correct?",
 "options": [
  "If the service's code is unavailable or > W_C it returns the state with incoming transfer amounts already credited and no other effect; otherwise it runs Ψ_M(code, entry 5, g, E(t, s, |i|), F, I(s, s)^2) with a regular context x and an exceptional context y (only `checkpoint` copies x into y); on ☇ or ∞ the result collapses to y; a 32-octet return blob becomes the yield hash; inputs are read via `fetch`",
  "If the service's code is unavailable or > W_C it returns the state with incoming transfer amounts already credited and no other effect; otherwise it runs Ψ_M(code, entry 1, g, E(t, s, |i|) ⌢ E(i), F, I(s, s)^2) with a regular context x and an exceptional context y (only `checkpoint` copies x into y); on ☇ or ∞ the result collapses to x, so everything done before the fault is kept; a 32-octet return blob becomes the yield hash",
  "If the service's code is unavailable or > W_C it returns the state with incoming transfer amounts already credited and no other effect; otherwise it runs Ψ_M(code, entry 0, g, E(t, s, |i|), F, I(s, s)^2) with a regular context x and an exceptional context y (only `checkpoint` copies x into y); on ☇ or ∞ the result collapses to y; the deferred transfers among i are instead delivered by a separate Ψ_T on-transfer invocation",
  "If the service's code is unavailable or > W_C it halts with the work error BAD or BIG exactly as Ψ_I and Ψ_R do; otherwise the guarantors run it in-core as Ψ_M(code, entry 5, g, E(c, i, s, payload, H(p)), F, I(s, s)^2) and the block author merely records the resulting hash; a regular context x and an exceptional context y are kept (only `checkpoint` copies x into y) and on ☇ or ∞ the result collapses to y"
 ],
 "answer": 0,
 "optNotes": [
   "entry point 是 5、參數只有 12 octets 的 E(t, s, |i|)，例外時 collapse 取 checkpoint 過的 y。",
   "GP 明寫 entry point 5 且參數不接 E(i)；例外時若取 x，checkpoint 就完全沒有意義。",
   "entry point 應為 5，且 0.8.0 只有三種 invocation，deferred transfer 直接混在 i 裡當 input。",
   "BAD/BIG 是 Ψ_I/Ψ_R 的 workerror，E(c, i, s, payload, H(p)) 也是 refine 的參數。",
 ],
 "explanation": "eq. B.9：Ψ_A(e, t, s, g, i)：若 code = ∅ 或 |code| > W_C → (s（餘額已加上 Σ transfer 金額）, [], ∅, 0, [])；否則 C(Ψ_M(code, 5, g, E(t, s, |i|), F, I(s, s)^2))——entry point 是 **5**（refine 與 is-authorized 是 0），參數只有 (timeslot, service id, input 數) 共 12 octets，正是為了「avoid introducing unbounded data as part of the basic invocation arguments」（否則 RAM 配置無界、gas 會被灌水），實際 inputs 用 fetch(14/15) 讀。eq. B.7：context **x** = (s id, u state, i nextfreeid, t transfers, y yield, p provisions)；例外維度是 **y**；eq. B.10：I(s, s) 初始化 nextfreeid = check(decode_4(H(E(s, η′_0, H_T))) mod (2^32 − S − 2^8) + S)。collapse C（B.13）：o ∈ {∞, ☇} → 用 **y**（checkpoint 過的狀態）；o ∈ H（32 bytes）→ yield = o；其他 → X 原樣。你們 code-map 3.8.7：「accumulate entry point is PC 5；on PANIC/OOG the checkpointed context y is committed；a 32-byte return blob becomes the accumulation output hash」。",
 "trap": "transfer 的金額在執行**前**就加到餘額（s = e except balance += Σ x_a）。"
},
{
 "id": "appB-new-service-index",
 "ch": "B", "section": "B.4 Accumulate Invocation", "gpRef": "eq. B.10, B.14 & `new` (§B.7)",
 "difficulty": 3, "kind": "concept", "tags": ["host-calls", "accounts"],
 "stem": "How are new service indices chosen by the `new` host call in GP 0.8.0?",
 "options": [
  "The context's next-free id starts at check(decode_4(H(E(s, η′_0, H_T))) mod (2^32 − S − 2^8) + S) with S = 2^16; check() linearly probes (+1 wrapping inside [S, 2^32 − 2^8)) until an index not in keys(δ); after each `new` the next candidate is check(S + (i − S + 42) mod (2^32 − S − 2^8)); only the registrar may instead request a specific index < S, which returns FULL if that index already exists",
  "The context's next-free id starts at check(decode_4(H(E(s, η′_0, H_T))) mod (2^32 − S − 2^8) + S) with S = 2^16; check() linearly probes (+1 wrapping inside [S, 2^32 − 2^8)) until an index not in keys(δ); after each `new` the next candidate is simply check(i + 1); only the registrar may instead request a specific index < S, which returns WHO if that index already exists",
  "The context's next-free id starts at check(decode_4(H(E(s, η_0, H_T))) mod (2^32 − S − 2^8) + S) with S = 2^8; check() linearly probes (+1 wrapping inside [S, 2^32 − 2^8)) until an index not in keys(δ); after each `new` the next candidate is check(S + (i − S + 42) mod (2^32 − S − 2^8)); only the registrar may instead request a specific index < S, which returns FULL if that index already exists",
  "The context's next-free id starts at S itself with S = 2^16, so the sequence is fixed by the block author rather than by entropy; check() linearly probes (+1 wrapping inside [S, 2^32 − 2^8)) until an index not in keys(δ); after each `new` the next candidate is check(i + 1); only the registrar may instead request a specific index < S, which returns FULL if that index already exists"
 ],
 "answer": 0,
 "optNotes": [
   "種子綁 posterior η′_0、每次配置跳 42 讓序列不可預測，撞號回 FULL（resource already allocated）。",
   "跳 42 是刻意讓連續配置不相鄰；撞號的語意是 FULL，WHO 指的是 index unknown。",
   "GP 用的是本區塊的 posterior η′_0，且 S = 2^16；2^8 是保留在 2^32 頂端的另外 256 個索引。",
   "序列若從 S 固定推進就可預測，service 便能預先卡位，正是 §B.4 要防的事。",
 ],
 "explanation": "eq. B.10：i_nextfree = check((decode_4(H(E(s, η′_0, H_T))) mod (2^32 − S − 2^8)) + S)；eq. B.14：check(i) = i 若 i ∉ keys(δ)，否則 check((i − S + 1) mod (2^32 − 2^8 − S) + S)。`new`（index 19）：registrar 且 desired id < S → 直接用該 id（若已存在 → FULL）；否則用 nextfreeid 並把 nextfreeid 更新為 check(S + (i − S + 42) mod (2^32 − S − 2^8))。§B.4 的設計目的：「no service can predict the identifier sequence ahead of time, they cannot intentionally disadvantage the block author」——正因為種子綁 η′_0，service 無法預先卡位。另外（本題選項未涵蓋，但同屬 Ω_N）：f ≠ 0 且非 manager → HUH；扣掉新帳戶的 a_t 後餘額低於自身 threshold → CASH。新帳戶：storage 空、requests = {(c, l) → []}、balance = 其 threshold、created = t、lastacc = 0、parent = 建立者。",
 "trap": "S = 2^16 = 65536 是 public index 下限；2^32 − 2^8 上限保留最後 256 個。"
},
{
 "id": "appB-transfer-rules",
 "ch": "B", "section": "B.7 Accumulate Functions — transfer", "gpRef": "`transfer` = 21",
 "difficulty": 2, "kind": "concept", "tags": ["host-calls", "transfers"],
 "stem": "The `transfer` host call (φ_7 = d, φ_8 = a, φ_9 = l gas, φ_10 = o memo ptr) can fail in several ways. Which order/meaning is correct?",
 "options": [
  "Memo unreadable → panic; d ∉ keys(δ) → WHO; l < δ[d]_m (recipient's minmemogas) → LOW; balance − a < own threshold a_t → CASH; otherwise OK: the transfer is appended to the context's transfer list, the sender's balance is reduced by a, and gas g = M_T + l is charged",
  "Memo unreadable → panic; d ∉ keys(δ) → WHO; l < δ[d]_m (recipient's minmemogas) → CASH; balance − a < own threshold a_t → LOW; otherwise OK: the transfer is appended to the context's transfer list, the sender's balance is reduced by a, and gas g = M_T + l is charged",
  "Memo unreadable → HUH; d ∉ keys(δ) → WHO; l < the sender's own minmemogas a_m → LOW; balance − a < 0 → CASH; otherwise OK: the transfer is appended to the context's transfer list, the sender's balance is reduced by a, and gas g = M_T alone is charged",
  "Memo unreadable → panic; d ∉ keys(δ) → WHO; l < δ[d]_m (recipient's minmemogas) → LOW; balance − a < own threshold a_t → CASH; otherwise OK: a is moved into δ[d]'s balance inside this host call and the recipient is entered at once with the 128-octet memo, gas g = M_T + l being charged"
 ],
 "answer": 0,
 "optNotes": [
   "四個檢查依序是 panic/WHO/LOW/CASH，且 g = M_T + l 把預付給接收方的 gas 一起收。",
   "語義反了：LOW 對應的是 l 不足（gas limit too low），CASH 對應餘額跌破 threshold。",
   "記憶體不可讀在 Ω_T 一律是 ☇；比的是接收方的 d[d]_m，門檻是自身 a_t 而不是 0。",
   "transfer 是 deferred 的：只附加到 x_t，接收方下一輪才被當成 accumulate input 叫起來。",
 ],
 "explanation": "Ω_T（index 21）的失敗階梯是**有序**的，而且順序有意義：memo 範圍 μ[o..+W_T]（W_T = 128）不可讀 → **panic**（記憶體錯誤一律是致命的，不是回錯誤碼）；d ∉ keys(δ) → **WHO**（身分解析不出來）；l < δ[d]_m（低於收款方自訂的最低處理 gas）→ **LOW**；扣款後餘額低於**自身**的門檻 a_t → **CASH**；否則 OK。gas 計價是 g = M_T + l（M_T = 575），**失敗時只收 M_T**。**門檻用 a_t 而不是 0 是關鍵**：a_t（eq. 9.8）是該帳戶依 footprint 算出的最低擔保餘額，若允許花到低於它，storage 就失去押金支撐——等於免費占用狀態空間。**這是 deferred transfer**：成功只是把 (source, dest, amount, memo, gas) 附加到 context 的 transfer 序列、並**立刻從 sender 扣款**；收款方要到 Δ+ 的**下一輪**才以 accumulate input 的形式收到。**所以會有一個現實後果**：收款方若在那之前被刪除，這筆轉帳直接丟棄，**但錢已經扣了**。這也解釋了為什麼要先付 l 的 gas——那是預留給收款方處理這筆轉帳的預算，必須在當下就從發送方的預算裡切出來，否則下一輪沒有經費來源。",
 "trap": "LOW 對照的是**接收方**的 a_m，不是發送方。"
},
{
 "id": "appB-solicit-forget",
 "ch": "B", "section": "B.7 — solicit / forget / eject", "gpRef": "`solicit` = 24, `forget` = 25, `eject` = 22",
 "difficulty": 3, "kind": "concept", "tags": ["host-calls", "preimages"],
 "stem": "Given request status l = a_l[(h, z)] and current slot t, which transitions do `solicit` and `forget` perform?",
 "options": [
  "solicit: no entry → [] (FULL if the new footprint is unaffordable); [x, y] → [x, y, t]; anything else → HUH. forget: [] or [x, y] with y < t − D → delete request and preimage; [x] → [x, t]; [x, y, w] with y < t − D → [w, t]; anything else → HUH",
  "solicit: no entry → [] (CASH if the new footprint is unaffordable); [x, y] → [x, y, t]; anything else → HUH. forget: [] or [x, y] with y < t − D → delete request and preimage; [x] → [] (unavailable at once); [x, y, w] with y < t − D → [w, t]; anything else → HUH",
  "solicit: no entry → [t]; [x, y] → [x, y, t]; anything else → HUH. forget: [] or [x, y] with y < t − D → delete request and preimage; [x] → [x, t]; [x, y, w] with w < t − D → [w, t]; anything else → HUH. Either call returns FULL when the account cannot afford its new threshold",
  "solicit and forget are refine host calls managing D3L segments: solicit reserves the next export index (FULL once W_X is spent), forget releases one, both HUH on a bad index; the request lattice [] → [x] → [x, y] → [x, y, w] is driven purely by the preimages extrinsic E_P"
 ],
 "answer": 0,
 "optNotes": [
   "兩者正是 preimage lattice 的兩個方向：過期判定看的是 y，付不起新 footprint 回 FULL。",
   "付不起 footprint 在 GP 裡是 FULL 而非 CASH；[x] → [x, t] 保留了 historical lookup 所需的可用區間。",
   "新 request 一定是空序列 []；三元素的過期判定看中間的 y，而且 forget 從不回 FULL。",
   "eq. B.6 的 refine 表裡沒有 solicit/forget，D3L segment 是 export（index 8）在管。",
 ],
 "explanation": "Ω_S（solicit, 24）：(h,z) 不存在 → 新增 [] 並付 footprint（a_balance < a_minbalance → FULL）；[x,y] → append t（重新請求）；其他 → HUH。Ω_F（forget, 25）：[] 或 [x,y] 且 y < t − D → 刪 request 與 preimage；[x] → [x, t]（標記 unavailable，preimage 仍留著）；[x,y,w] 且 y < t − D → [w, t]；其他 → HUH。三元素 [x,y,w] 的過期判定看的是**中間**的 y（上一次停止可用的時刻），w 是最近一次重新請求的時刻，必然比較新。preimage 的請求狀態機由 solicit/forget 在 accumulate 中驅動，E_P extrinsic 只負責把 [] 推進到 [x]。D = C_expungeperiod = 19,200（= L + 4,800，§B.3 說明：審計最晚可在 accumulate 後兩個 epoch 發生，lookup anchor 最多 L 舊，再留 8 小時安全邊際）。`eject`（22）讓一個 codehash = E_32(caller id) 且只剩單一 request（items = 2）的 service 被銷毀並把餘額轉給呼叫者，條件同樣是 [x,y] 且 y < t − D。",
 "trap": "刪除必須等 D 個 slot（32h）——確保 refine 的 historical lookup 仍可判定。"
},
{
 "id": "appB-bless-assign-designate",
 "ch": "B", "section": "B.7 — bless / assign / designate", "gpRef": "`bless` = 15, `assign` = 16, `designate` = 17",
 "difficulty": 2, "kind": "delta", "tags": ["host-calls", "privileges", "delta-0.8.0"],
 "stem": "Which privilege checks do bless, assign and designate perform in GP 0.8.0?",
 "options": [
  "bless: caller must be the current manager χ_M (else HUH), sets (m, a[C], v, r, z); assign(c, o, a): c ≥ C → CORE, caller must be χ_A[c] (else HUH), writes the 80-entry queue φ[c] and a new assigner a; designate(o, z): z must be a valid validator count and caller must be χ_V (else HUH), sets ι to z 336-octet keys",
  "bless: caller must be the current registrar χ_R (else HUH), sets (m, a[C], v, r, z); assign(c, o, a): c ≥ C → CORE, caller must be χ_A[c] (else HUH), writes the 80-entry queue φ[c] and a new assigner a; designate(o, z): z must be a valid validator count and caller must be χ_M (else HUH), sets ι to z 336-octet keys",
  "bless: caller must be the current manager χ_M (else HUH), sets (m, a[C], v, r, z); assign(c, o, a): c ≥ C → HUH, caller must be χ_A[c] (else CORE), writes the 32-entry queue φ[c] and a new assigner a; designate(o, z): z must be a valid validator count and caller must be χ_V (else HUH), sets ι to z 32-octet Ed25519 keys",
  "All three are gated on the manager alone: each returns HUH unless the caller is χ_M. bless additionally returns WHO when m, v or r is not a service index, assign additionally returns CORE for c ≥ C and writes the 80-entry queue φ[c], and designate additionally requires z ∈ N_V; χ_A[c] and χ_V are read-only and only bless can change them"
 ],
 "answer": 0,
 "optNotes": [
   "三者分屬 χ_M、χ_A[c]、χ_V 三把獨立權限，且 assign 成功時會把 χ_A[c] 改寫成參數 a。",
   "張冠李戴：χ_R 只在 new 裡決定誰能指定 < S 的低位索引，designate 由 delegator χ_V 專屬。",
   "CORE = core index unknown 專對應 c ≥ C，權限不符一律 HUH；Q = 80、每把 key 336 octets。",
   "漏掉 owned privilege：assign 會寫入新的 χ_A[c]，core 指派權可以轉手而不必回頭找 manager。",
 ],
 "explanation": "Ω_B（bless, 15）：讀 m, a（4C 個 u32 assigners）, v, r, o/n（z 的 (u32, u64) pairs）；x_s ≠ χ_M → HUH（0.8.0 #519 新增：只有 manager 能 bless）；m/v/r 不是有效 service id → WHO。Ω_A（assign, 16）：c ≥ C → CORE；x_s ≠ χ_A[c] → HUH；a 無效 → WHO；否則 φ[c] = Q = 80 個 32-octet hash，χ_A[c] = a（owned privilege：assigner 可把權限轉給別人）。Ω_D（designate, 17）：z ∉ N_V（不是 6..1023 的 3 倍數）或 x_s ≠ χ_V → HUH；否則 ι = 讀入的 z 個 336-octet key（32 Bandersnatch + 32 Ed25519 + 144 BLS + 128 metadata）。三把權限刻意分開：manager 管全域、每個 core 各有自己的 assigner、validator key 由 delegator 專管。這三者的變更經 Δ* 的 R() 合併規則整合。",
 "trap": "0.8.0 designate 也要驗 z 是合法 validator 數（#514）。"
},
{
 "id": "appB-checkpoint-yield",
 "ch": "B", "section": "B.7 — checkpoint / yield / provide", "gpRef": "`checkpoint` = 18, `yield` = 26, `provide` = 27",
 "difficulty": 2, "kind": "concept", "tags": ["host-calls", "accumulate"],
 "stem": "What do `checkpoint`, `yield` and `provide` do inside accumulate?",
 "options": [
  "checkpoint: copies the regular context x into the exceptional context y (so a later panic/OOG commits the checkpointed state) and returns remaining gas in φ_7; yield(o): records the 32-octet hash at o as the service's accumulation output (θ entry / BEEFY-visible commitment); provide(s, o, z): supplies preimage bytes for a request [] of service s (or the caller if φ_7 = 2^64−1), returning WHO/HUH on errors, integrated after the round",
  "checkpoint: copies the exceptional context y into the regular context x (so a later panic/OOG rewinds to the start of the accumulation) and returns the gas already used in φ_7; yield(o): records the 32-octet hash at o as the service's accumulation output (θ entry / BEEFY-visible commitment); provide(s, o, z): supplies preimage bytes for a request [] of service s (or the caller if φ_7 = 2^64−1), returning WHO/HUH on errors, integrated after the round",
  "checkpoint: copies the regular context x into the exceptional context y (so a later panic/OOG commits the checkpointed state) and returns remaining gas in φ_7; yield(o): halts the invocation there and then, committing x and forfeiting the unspent gas, with the 32 octets at o as the output; provide(s, o, z): writes the preimage straight into δ[s]_p and moves a_l[(H(i), z)] to [t] inside this same host call",
  "All three belong to the refine invocation: checkpoint snapshots the inner-PVM map m so that a later panic can restore it and returns remaining gas in φ_7; yield(o) appends the 32 octets at o to the export sequence e; provide(s, o, z) hands preimage bytes to the guarantor's local cache, returning WHO/HUH on errors; accumulate reaches the same effects through write, export and transfer instead"
 ],
 "answer": 0,
 "optNotes": [
   "checkpoint 是唯一會改 y 的 host call，因此 ☇/∞ 時 collapse 才能 commit 到存檔點。",
   "方向相反：存檔是把當下的 x 複製進 y，反過來會把先前的進度倒回去，回傳的也是剩餘 gas。",
   "Ω_Taurus 只設 x_y 一個欄位（停機得靠 halt 指令），provide 也只加進 x_provisions 等 Δ* 整合。",
   "eq. B.11 才有這三個；refine 的 export 附加的是 4,104 octet segment，不是 32-octet hash。",
 ],
 "explanation": "三個都是 accumulate 專屬，但作用的層面完全不同。**`checkpoint`（18，Ω_C）**：y′ ≡ x——把當前的 regular context 整份複製到 exceptional context，並在 φ_7 回傳**扣掉 M_C = 103 之後的剩餘 gas**。**它是唯一會改動 y 的 host call**。意義在於：collapse 函數 C 在 ☇（panic）或 ∞（OOG）時採用的是 y，所以 service 可以「存檔」——即使後面爆掉，存檔當下的進度仍會被提交。沒有 checkpoint 的話，一次 panic 就會讓整個 accumulate 的改動全部作廢。**`yield`（26，Ω_♉）**：把記憶體 o 處的 32 個位元組記成本次 accumulate 的產出，**回 OK 後繼續執行**（不是結束）。這個值最終進 θ′、再進 β_B、最後被 BEEFY 簽名給外部看。順帶一提，若程式正常 halt 且回傳恰好 32 位元組，那也會被當成 yield（B.13）。**`provide`（27，Ω_♈）**：替某個 service（φ_7 = 2^64−1 表示自己）補上一份 preimage，s 不存在 → WHO，request 狀態不是 [] 或已提供過 → HUH。**注意它不會當場改動別人的狀態**——只是加進 x_provisions，由 Δ* 在該輪結束後用 I() 統一整合。host call 期間不能直接寫別的 service 的表，這是 accumulate 隔離性的一部分。",
 "trap": "yield 的 hash 進 θ′ → β′_B belt → BEEFY；這是 service 對外（bridge）承諾狀態的管道。"
},
]
