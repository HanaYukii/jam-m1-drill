# -*- coding: utf-8 -*-
# Appendix B — Virtual Machine Invocations & host calls (GP 0.8.0)
ITEMS = [
{
 "id": "appB-result-constants",
 "ch": "B", "section": "B.1 Host-Call Result Constants", "gpRef": "§B.1",
 "difficulty": 1, "kind": "concept", "tags": ["host-calls"],
 "stem": "Which mapping of host-call result constants is correct?",
 "options": [
  "OK = 0; NONE = 2^64−1 (item does not exist); WHAT = 2^64−2 (name unknown); OOB = 2^64−3; WHO = 2^64−4 (index unknown); FULL = 2^64−5; CORE = 2^64−6; CASH = 2^64−7 (insufficient funds); LOW = 2^64−8 (gas limit too low); HUH = 2^64−9 (invalid operation / insufficient privilege)",
  "OK = 0; NONE = 1 (item does not exist); WHAT = 2 (name unknown); OOB = 3; WHO = 4 (index unknown); FULL = 5; CORE = 6; CASH = 7 (insufficient funds); LOW = 8 (gas limit too low); HUH = 9 (invalid operation / insufficient privilege); the inner-PVM results HALT…OOG continue the same run at 10…14",
  "OK = 0; NONE = 2^64−1 (item does not exist); WHAT = 2^64−2 (name unknown); OOB = 2^64−3 (index unknown); WHO = 2^64−4 (inner-PVM memory index not accessible); FULL = 2^64−5 (core index unknown); CORE = 2^64−6 (storage full or resource already allocated); CASH = 2^64−7; LOW = 2^64−8; HUH = 2^64−9",
  "OK = 0; NONE = 2^32−1 (item does not exist); WHAT = 2^32−2 (name unknown); OOB = 2^32−3; WHO = 2^32−4 (index unknown); FULL = 2^32−5; CORE = 2^32−6; LOW = 2^32−7 (gas limit too low); CASH = 2^32−8 (insufficient funds); HUH = 2^32−9 (invalid operation / insufficient privilege)"
 ],
 "answer": 0,
 "optNotes": [
   "十個常數與 §B.1 逐字對上：2^64−k 的數值與 CASH/LOW/FULL/CORE 的語意都正確。",
   "錯誤碼落在 0…9 就無法與 read/new/machine 那些正常的小整數回傳值區分。",
   "數值對但語意平移：OOB 是 inner PVM 記憶體不可存取，WHO 才是 index unknown。",
   "錯誤常數定義在 2^64 附近（2^32−1 是合法長度/索引），且 CASH 排在 LOW 之前。",
 ],
 "explanation": "§B.1 逐字：NONE = 2^64−1、WHAT = 2^64−2、OOB = 2^64−3（inner PVM 記憶體索引不可存取）、WHO = 2^64−4（index unknown）、FULL = 2^64−5（storage full / resource already allocated）、CORE = 2^64−6（core index unknown）、CASH = 2^64−7（insufficient funds）、LOW = 2^64−8（gas limit too low）、HUH = 2^64−9、OK = 0。錯誤碼刻意擺在 2^64 頂端，因為 host call 的正常回傳值本身就是小整數（read/lookup/fetch 回傳長度、new 回傳新 service index、machine 回傳機器編號、query 回傳 1 + 2^32·x），必須能與之區分。inner PVM 的結果碼則是獨立的一組 HALT = 0、PANIC = 1、FAULT = 2、HOST = 3、OOG = 4。另註：「Note return codes for a host-call-request exit are any non-zero value less than 2^64 − 13」。",
 "trap": "常考 WHO vs HUH：WHO = 找不到 service/index；HUH = 操作本身不合法（已 solicit、無法 forget、權限不足）。"
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
 "explanation": "Ω_T（index 21，g = M_T + t，成功時 t = l、失敗時 t = 0，M_T = 575）：t = error（memo 範圍 μ[o..+W_T]、W_T = 128 不可讀）→ panic；d ∉ keys(d) → WHO；l < d[d]_m → LOW；b = balance − a < 自身 a_t → CASH；否則 OK，x′_t = x_t ⌢ t，balance = b。門檻用的是自身 a_t（eq. 9.8）而不是 0——否則帳戶可以把餘額花到低於 deposit 而讓 storage 失去擔保。transfer 屬於 deferred transfer：只是把 ⟨source, dest, amount, memo, gas⟩ 附加到 x_t，由 Δ+ 在**下一輪**把它當成接收方的 accumulate input 送達（接收方屆時不存在就丟棄），這也是 transfer 得先付 l gas 的原因。",
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
 "explanation": "Ω_C（checkpoint, 18）：y′ ≡ x，φ′_7 = ϱ′（扣完 M_C = 103 後的**剩餘** gas）——這是唯一改變 y 的 host call；因為 collapse C 在 ☇/∞ 時使用 y，service 可以「存檔」部分進度。Ω_Taurus（yield, 26）：x_y = 記憶體 o 處的 32 bytes，回 OK 後**繼續執行**；若程式正常 halt 且回傳 32 bytes 也會成為 yield（B.13）。Ω_Aries（provide, 27）：s = φ_7（2^64−1 表示自己），i = μ[φ_8..+φ_9]，s 不存在 → WHO，request 狀態不是 [] 或已提供過 → HUH，否則加入 x_provisions，由 Δ* 的 I() 在該輪後整合（0.6.5 引入 provide）——host call 期間不可能直接改別的 service 的 preimage 表。",
 "trap": "yield 的 hash 進 θ′ → β′_B belt → BEEFY；這是 service 對外（bridge）承諾狀態的管道。"
},
]
