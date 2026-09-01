# -*- coding: utf-8 -*-
# Batch c3 — Chapter 9 (Service Accounts) + Appendix D (State Merklization), GP 0.8.0
# Sources quoted: gp-src/text/accounts.tex, gp-src/text/merklization.tex (D half),
#                 gp-src/text/pvm_invocations.tex (host calls), gp-src/preamble.tex, gp-src/text/serialization.tex
ITEMS = [

# ---------------------------------------------------------------- ch. 9 ----
{
 "id": "c3-ch09-expunge-delay",
 "ch": "9", "section": "9.2 Preimage Lookups",
 "gpRef": "§9.2 (domain of Λ); App. B Refine Invocation (D ≡ L + 4,800 = 19,200)",
 "difficulty": 1, "kind": "rationale", "tags": ["accounts", "preimages", "constants"],
  "stemZh": "§9.2 把歷史查詢函數 Λ 的時槽引數限制在 (H_t − D … H_t) 這個窗口內，而常數附錄把 D 定為 19,200 個時槽。GP 為這個特定數字給出的理由是什麼？",
  "optionsZh": [
   "19,200 個時槽恰好是 32 個 epoch，也正是 accumulation 歷史 ξ 保留 work-package 雜湊的時間長度，所以在某份 work-package 還可能被重新 accumulate 之前，它用到的 preimage 不得被丟棄；D 因此被定為 32·E",
   "這段期間必須比兩個 epoch 的稽核窗口（1,200 個時槽）長十六倍，好讓 erasure-code 過的 bundle 在爭議期間仍能從 1,023 位 validator 的碎片重建；D 是從那個保存期導出的，與任何 anchor 年齡無關",
   "Ω_H 在任何仍可能發生稽核的時刻都必須回傳相同的答案；而 lookup anchor 本身可能比近期歷史再舊上 L = 14,400 個時槽，所以這段期間就是那個 anchor 年齡再加上 4,800 個時槽（八小時）的安全餘裕",
   "每 octet 的押金 B_L 會在這段期間內線性退還，而 19,200 個時槽在每槽六秒之下正是 32 小時——這是選用性狀態的標準押金退還時程；B_L 會在那些時槽內等額分期退回 a_b"
  ],
  "stem": "§9.2 bounds the timeslot argument of the historical-lookup function Λ to the window (H_t − D … H_t), and the constants appendix fixes D = 19,200 timeslots. What is the GP's stated reason for that particular number?",
 "options": [
  "19,200 timeslots is exactly 32 epochs, which is precisely how long the accumulation history ξ keeps work-package hashes, so a preimage may not be dropped before the work-package that used it can no longer be re-accumulated; D is fixed at 32·E for that reason.",
  "The period must exceed the two-epoch audit window (1,200 timeslots) by a factor of sixteen so that erasure-coded bundles can still be reconstructed from the 1,023 validators' shards during a dispute; D is derived from that retention period, not from any anchor age.",
  "Ω_H must return the same answer at every moment when auditing may still occur; the lookup anchor may itself be up to L = 14,400 timeslots older than recent history, so the period is that anchor age plus a further 4,800 slots (eight hours) of safety margin.",
  "The per-octet deposit B_L is refunded linearly over the period, and 19,200 slots is 32 hours at six seconds per slot — the standard deposit-refund schedule for elective state; B_L is credited back to a_b in equal instalments over those slots."
 ],
 "answer": 2,
 "optNotes": [
   "19,200 / E = 32 只是數值巧合；ξ 只保存一個 epoch 的 package hashes（eq. 12.1），與 D 無關。",
   "推導方向反了：驅動 D 的是 lookup anchor 的年齡，不是 dispute 期間的 erasure 重建。",
   "附錄 B 直接寫出 D ≡ L + 4,800 = 19,200，理由就是 Ω_H 在任何可審計時點都要給同一個答案。",
   "GP 沒有 deposit 攤提退款機制；a_t 是門檻式檢查，餘額只透過 transfer 與 accumulate 改變。",
 ],
 "explanation": "GP 附錄 B（Refine Invocation）原文：「The historical-lookup host-call function, Ω_H, is designed to give the same result regardless of the state of the chain for any time when auditing may occur … The lookup anchor may be up to L timeslots before the recent history and therefore adds to the potential age at the time of audit. We therefore set D to have a safety margin of eight hours: D ≡ L + 4,800 = 19,200。」L = 14,400（max lookup anchor age，24 小時），加 4,800 slot（8 小時）＝ 19,200 slot（32 小時）。§9.2 的 Λ 定義域正是 (H_t − D … H_t)。這題考的是「理由」而不是算術：D 的來源是 lookup anchor 的最大年齡加上安全邊際，凡是把它歸給別的保存期的說法，即使數字湊得上也不是 GP 寫的那條式子。",
 "trap": "D 只是「forget 之後多久才能真的刪」；真正把 preimage 從 state 移除的動作在 `forget`（自家，Ω_F = 25）與 `eject`（別家，Ω_J = 22）兩個 accumulate host call 裡——注意別跟 0.8.0 的 `expunge`（Ω_X = 14）混淆，那是 refine-only 的 inner-PVM 拆除呼叫，與 preimage 無關。preimage 生命週期的狀態機本身在 §9.2.2。"
},
{
 "id": "c3-ch09-service-info-leaf",
 "ch": "9", "section": "9.3 Account Footprint and Threshold Balance",
 "gpRef": "eq. 9.3, eq. 9.8; §D.1 T(σ) row C(255, s); App. B `info` (Ω_I)",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "state", "merklization"],
  "stemZh": "a_i（項數）、a_o（位元組數）與 a_t（門檻餘額）都是衍生值——§9.3 從 a_s 與 a_l 導出 a_i 與 a_o，再從那兩者加上儲存的 gratis 抵扣 a_f 導出 a_t，而三者都不是 eq. 9.3 元組的成員。它們之中哪些真的進入了被 Merklize 的狀態？與 `info` host call 交回的內容相比又如何？",
  "optionsZh": [
   "三者都同時進入兩種編碼，而且兩種編碼逐位元組相同——這正是為什麼實作可以放心地在 trie 葉子與 host call 之間共用同一個 codec，也是為什麼那片葉子可以直接遞給 guest 的緩衝區",
   "service-info 的葉子帶有 a_i 與 a_o 但沒有 a_t，而且它以版本位元組 0 開頭；`info` 沒有版本位元組但有 a_t，其版面為 E(a_c, E_8(a_b, a_t, a_g, a_m, a_o), E_4(a_i), E_8(a_f), E_4(a_r, a_a, a_p))",
   "三者都沒有被序列化到任何地方：trie 只儲存 eq. 9.3 的元組欄位，而 a_i、a_o 與 a_t 是在每次 host call 需要時才從 a_s 與 a_l 重新算出來的",
   "trie 的葉子帶有 a_t 但沒有 a_i 與 a_o（那兩者按需重算），而 `info` 回傳 a_i 與 a_o 但沒有 a_t；兩種編碼都以版本位元組 0 開頭"
  ],
  "stem": "a_i (items), a_o (octets) and a_t (threshold balance) are dependent values — §9.3 derives a_i and a_o from a_s and a_l, and a_t from those two plus the stored gratis offset a_f, and none of them is a member of the eq. 9.3 tuple. Which of them actually reach the Merklized state, and how does that compare with what the `info` host call hands back?",
 "options": [
  "All three reach both encodings, and the two encodings are byte-for-byte identical — which is exactly why an implementation is free to reuse a single codec for the trie leaf and for the host call, and why the leaf can be handed straight to the guest's buffer.",
  "The service-info leaf carries a_i and a_o but not a_t, and it opens with a version octet 0; `info` has no version octet but does include a_t, laid out as E(a_c, E_8(a_b, a_t, a_g, a_m, a_o), E_4(a_i), E_8(a_f), E_4(a_r, a_a, a_p)).",
  "None of the three is serialized anywhere: the trie stores only the eq. 9.3 tuple fields, and a_i, a_o and a_t are recomputed from a_s and a_l each time a host call needs them.",
  "The trie leaf carries a_t but neither a_i nor a_o (those are recomputed on demand), while `info` returns a_i and a_o but not a_t; both encodings begin with the version octet 0."
 ],
 "answer": 1,
 "optNotes": [
   "兩個排列並不相同（version octet、a_t 的有無、a_f 的位置），共用一份 codec 正是最常見的實作坑。",
   "leaf 有 version octet 0、沒有 a_t；`info` 沒有 version octet、有 a_t，兩者 a_f 的位置也不同。",
   "§9.3 明說 a_i、a_o「are expected to be found explicitly within the Merklized state data」，不是臨時重算。",
   "剛好顛倒：leaf 存的是 a_i／a_o 而非 a_t，多寫 a_t 會讓 leaf 多 8 bytes、整棵 trie 的 root 對不上。",
 ],
 "explanation": "§9.3 說得很清楚：a_i、a_o 是 dependent values，「as we will see in the account serialization function … these are expected to be found explicitly within the Merklized state data. Because of this we make explicit their set.」——所以 a_i ∈ N_{2^32}、a_o ∈ N_{2^64} 被寫死進 trie。附錄 D 的 T(σ)：C(255, s) ↦ E(0, a_c, E_8(a_b, a_g, a_m, a_o, a_f), E_4(a_i, a_r, a_a, a_p))，開頭那個 0 就是 0.7.1 起加入的 service-info version octet，而 a_t 不在裡面（它是 max(0, B_S + B_I·a_i + B_L·a_o − a_f)，隨時可重算）。附錄 B 的 Ω_I（`info`）則是另一個排列：E(a_c, E_8(a_b, a_t, a_g, a_m, a_o), E_4(a_i), E_8(a_f), E_4(a_r, a_a, a_p))——有 a_t、沒有 version octet、a_f 的位置也不同。兩份編碼的欄位集合與順序都不一樣，這是 trie 與 host call 之間最容易共用錯 struct 的地方。",
 "trap": "leaf 有 version octet、沒有 a_t；`info` 沒有 version octet、有 a_t。兩個排列不同，別共用 struct。"
},
{
 "id": "c3-ch09-write-threshold-go",
 "ch": "9", "section": "9.3 Account Footprint and Threshold Balance",
 "gpRef": "eq. 9.8 (a_i, a_o, a_t); App. B `write` (Ω_W)",
 "difficulty": 2, "kind": "code", "tags": ["accounts", "balance", "host-calls", "fuzzer-bug"],
  "stemZh": "這是團隊修正「write 在餘額檢查之前就變動 StorageDict」那個 bug 之後的 Ω_W。哪個敘述符合 GP 0.8.0？",
  "optionsZh": [
   "一筆 storage 條目對 a_i 計 1、對 a_o 計 32 + |v|——key 的長度從不計費，因為 JAM 在 trie 裡只存 storage key 的雜湊；而遇到 FULL 時該寫入仍然生效，差額則從餘額中扣除",
   "一筆 storage 條目對 a_i 計 2、對 a_o 計 81 + |v|，與 lookup-meta 條目完全相同，理由是兩者都恰好佔用 state trie 的一片葉子；而 FULL 只有在餘額本身歸零之後才可能產生，所以一個有償付能力的 service 永遠能完成寫入",
   "門檻是在 accumulation 結尾重算一次而不是每次 host call 都算，所以 `write` 根本不可能產生 FULL；過度承諾儲存的 service 會在事後被持有其 code-hash 墓碑的那個 service 修剪掉，押金退還給 parent",
   "一筆 storage 條目對 a_i 計 1、對 a_o 計 34 + |k| + |v|——key 與 value 都計費；當寫入後的門檻超過餘額時該呼叫產生 FULL，而且該帳戶必須被完全原封交回，這正是 map 的寫入要延到比較之後才進行的原因"
  ],
  "stem": "This is the team's Ω_W after the fix for the 'write mutates StorageDict before the balance check' bug. Which statement matches GP 0.8.0?",
 "code": {
  "lang": "go",
  "caption": "PVM/host_call_general.go (write) + internal/service_account/service_account.go:207 (CalcStorageItemfootprint)",
  "src": """// remove the old item's footprint, then add the new one's
newItems := a.ServiceInfo.Items - footprintItems
newOctets := a.ServiceInfo.Bytes - footprintOctets

storageItems, storageOctets := service_account.CalcStorageItemfootprint(
    string(storageRawKey), storageRawData)
newItems += storageItems
newOctets += storageOctets

newMinBalance := service_account.CalcThresholdBalance(
    newItems, newOctets, a.ServiceInfo.DepositOffset) // a_t
if newMinBalance > a.ServiceInfo.Balance {
    input.VM.Registers[7] = FULL
    return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
}

// balance check passed, now apply the storage mutation
a.StorageDict[string(storageRawKey)] = storageRawData
a.ServiceInfo.Items = newItems
a.ServiceInfo.Bytes = newOctets

// ---- service_account.go ----
func CalcStorageItemfootprint(storageRawKey string, storageData types.ByteSequence) (types.U32, types.U64) {
	return 1, 34 + types.U64(len(storageRawKey)) + types.U64(len(storageData))
}"""
 },
 "options": [
  "One storage entry costs 1 against a_i and 32 + |v| against a_o — key length is never charged, because JAM stores only the hash of a storage key in the trie; on FULL the write still lands and the shortfall is taken out of the balance.",
  "One storage entry costs 2 against a_i and 81 + |v| against a_o, exactly like a lookup-meta entry, on the grounds that both occupy precisely one leaf of the state trie; FULL is only ever produced once the balance itself has reached zero, so a solvent service can always complete a write.",
  "The threshold is recomputed once at the end of accumulation rather than on every host call, so `write` can never yield FULL at all; services that over-commit their storage are pruned afterwards by whichever service holds their code-hash tombstone, and their deposit is returned to the parent.",
  "One storage entry costs 1 against a_i and 34 + |k| + |v| against a_o — both the key and the value are charged; when the post-write threshold exceeds the balance the call yields FULL and the account must be returned completely untouched, which is why the map write is deferred until after the comparison."
 ],
 "answer": 3,
 "optNotes": [
   "eq. 9.8 的求和是對 (x, y) 這一對跑，key 長度同樣計費；而且 FULL 分支不得留下任何寫入。",
   "把 lookup request 的 2 items / 81 + z 套到 storage 上；FULL 的條件是 a_t > a_b，不是餘額歸零。",
   "門檻檢查是每次 host call 當場做的，Ω_W 明列 FULL 分支；GP 也沒有 tombstone 剪枝或退款機制。",
   "§9.8 的計價是 34 + |key| + |value|，key 的長度也算，且 FULL 時必須回傳原封不動的 s。",
 ],
 "explanation": "eq. 9.8：a_i ≡ 2·|a_l| + |a_s|；a_o ≡ Σ_{(h,z)∈K(a_l)} (81 + z) + Σ_{(x,y)∈a_s} (34 + |y| + |x|)；a_t ≡ max(0, B_S + B_I·a_i + B_L·a_o − a_f)。求和是對 a_s 的「pair」跑——storage 一筆 = 1 item、34 + |k| + |v| octets；lookup request 一筆 = 2 items、81 + z octets。附錄 B 的 Ω_W：「⟨continue, FULL, s⟩ otherwhen a_t > a_b」——回傳的第三個元素是 **s**（原封不動的帳戶），不是被改過的 a；#979/#980 這個 bug 正是因為 Go map 是 reference，先寫再檢查會讓 FULL 分支殘留寫入，fuzzer seed 3785638964 step 15419 抓到。程式碼把 map 寫入延到比較之後，就是為了滿足這條「失敗即不留下任何狀態變更」的要求。",
 "trap": "FULL 與 CASH 不同：a_t > a_b 用 FULL（write / solicit）；轉帳後自己跌破 a_t 用 CASH（transfer / new）。兩者都不留下任何狀態變更。"
},
{
 "id": "c3-ch09-forget-lifecycle",
 "ch": "9", "section": "9.2.2 Semantics",
 "gpRef": "§9.2.2 (four shapes of a_l); App. B `forget` (Ω_F), expunge period D = 19,200",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "preimages", "host-calls"],
  "stemZh": "某個 service 在時間 t 對自己的某個 request key (h, z) 呼叫 `forget`。逐一考慮 a_l[(h, z)] 的四種形狀，哪一組轉換符合 GP 0.8.0？",
  "optionsZh": [
   "[] → 該 request 條目被丟棄；[x] → [x, t]；[x, y] → 該 request 條目與 a_p[h] 兩者都被清除，但只有在 y < t − D 時；[x, y, w] → [w, t]，同樣只有在 y < t − D 時；其餘每一種情況都回傳 HUH",
   "[] → HUH，沒有東西可忘；[x] → 該 request 條目與 a_p[h] 兩者立即被丟棄；[x, y] → [x, y, t]；[x, y, w] → [w, t] 且不附帶任何年齡條件；其餘每一種情況都回傳 HUH",
   "[] → 該 request 條目被丟棄；[x] → [x, t]；[x, y] → 只要 y < t 就立刻清除該條目與 a_p[h]，不必等 D 個時槽；[x, y, w] → 直接丟棄而不是改寫；其餘每一種情況都回傳 HUH",
   "[] → 丟棄；[x] → 連同 a_p[h] 一起丟棄；[x, y] → 連同 a_p[h] 一起丟棄；[x, y, w] → 連同 a_p[h] 一起丟棄；每一種形狀都立刻塌陷，而那個 D 個時槽的延遲只管 `eject`"
  ],
  "stem": "A service calls `forget` at time t for one of its own request keys (h, z). Taking the four shapes of a_l[(h, z)] in turn, which set of transitions matches GP 0.8.0?",
 "options": [
  "[] → the request entry is dropped; [x] → [x, t]; [x, y] → the request entry and a_p[h] are both expunged, but only once y < t − D; [x, y, w] → [w, t], again only once y < t − D; every other case returns HUH.",
  "[] → HUH, there is nothing to forget; [x] → the request entry and a_p[h] are both dropped at once; [x, y] → [x, y, t]; [x, y, w] → [w, t] with no age condition attached; every other case returns HUH.",
  "[] → the request entry is dropped; [x] → [x, t]; [x, y] → the request entry and a_p[h] are expunged the moment y < t, with no D-slot wait; [x, y, w] → dropped outright rather than rewritten; every other case returns HUH.",
  "[] → dropped; [x] → dropped together with a_p[h]; [x, y] → dropped together with a_p[h]; [x, y, w] → dropped together with a_p[h]; every shape collapses at once and the D-slot delay governs only `eject`."
 ],
 "answer": 0,
 "optNotes": [
   "四支轉移與 Ω_F 逐條相符，且 D 的等待期只綁在 [x, y] 與 [x, y, w] 這兩支上。",
   "[x, y] → [x, y, t] 是 `solicit` 的動作；available 的 preimage 也不能一步刪，[x, y, w] 那支同樣要 y < t − D。",
   "少了 D 個 slot 的等待期會破壞 historical_lookup 的確定性；[x, y, w] 是被改寫成 [w, t] 而非整筆移除。",
   "§9.2 開頭明說「only after a period of time may it be removed from state」，`forget` 自己就帶這道等待期。",
 ],
 "explanation": "附錄 B 的 Ω_F（`forget` = 25）逐條列出 a = self except：(i) 當 a_l[(h,z)] 是 []（無條件），或是 [x, y] 且 y < t − D，同時從 K(a_l) 移除 (h,z)、從 K(a_p) 移除 h；(ii) 當 a_l[(h,z)] = [x]，改寫成 [x, t]；(iii) 當 a_l[(h,z)] = [x,y,w] 且 y < t − D，改寫成 [w, t]；其餘 → error → HUH。這裡要點名一個 GP 的 under-specification：原文只寫了一條 guard「(x_s)_l[h,z] ∈ {[], [x,y]}, y < t − D」，把兩種形狀併在同一個集合裡，但 [] 這一支根本沒有任何東西綁定 y，年齡條件在該支懸空、無從判定；唯一可實作、也就是本題所鍵的讀法，是把 [] 這個 case 直接刪掉、完全不加等待期——[] 代表「已 solicit、從未供應」，若它也要等 D，solicit 之後就永遠取消不掉、[] 會永久卡在 state 裡——所以 D 的等待期實際上只約束 [x, y] 與 [x, y, w] 這兩支。GP 0.8.0 對此並未明文釐清，這是已知的 under-specification。對照 §9.2.2 的四種語意：[] requested、[x] available since x、[x,y] 自 y 起 unavailable、[x,y,z] 自 z 起再度 available。貫穿全題的原則是「available 的東西不能一步刪掉」——它必須先降級成 [x, t]，等 D = 19,200 slot 後才可能被真正 expunge，這正是 §9.2 開頭說的「it goes through a process of being marked as unavailable, and only after a period of time may it be removed from state. This ensures that historical information on its existence is retained.」否則 in-core historical_lookup 就不再確定（auditor 在 lookup anchor 時點重算會拿到不同答案），服務也就能隨時自我抹除歷史。至於 [x,y,w] → [w, t]：舊的 [x,y] 那段歷史被丟掉，因為它已經超過 D、不再需要保存，服務仍然持有那份 preimage 且自 w 起可用。",
 "trap": "`forget` 不看餘額，`solicit` 才有 FULL 檢查；反向的 `solicit` 只接受兩種輸入形狀（不存在 → []、[x,y] → [x,y,t]），其餘一律 HUH。"
},
{
 "id": "c3-ch09-new-service-index",
 "ch": "9", "section": "9 Service Accounts",
 "gpRef": "§9 eq. 9.1 (N_S ≡ N_{2^32}); eq. B.14 (check); S = 2^16",
 "difficulty": 2, "kind": "concept", "tags": ["accounts", "service-id", "accumulation"],
  "stemZh": "某個 service 在 accumulation 期間呼叫 `new`。GP 0.8.0 如何挑選子帳戶的索引？又如何避免與既有 service 相撞？",
  "optionsZh": [
   "索引是新帳戶 code hash 的 Blake2b 對 2^32 取模，好讓相同的程式碼永遠落在同一個位置、使重複部署變得便宜；完全沒有探測，而萬一該索引已被佔用，整個區塊就會被判為無效",
   "索引是 δ 中當前最大的 key 加一，所以索引在整條鏈上是嚴格循序發放的、依構造不可能相撞；registrar 只是在創世時保留了最前面的 2^16 個，並在鏈外發放它們",
   "context 的 next free id 起始於 check((E⁻¹_4(H(E(s, η′_0, H_t))) mod (2^32 − S − 2^8)) + S)，其中 S = 2^16，所以它只會落在公開範圍內；check 以 i ↦ (i − S + 1) mod (2^32 − 2^8 − S) + S 向前線性探測，直到落在 K(δ) 之外的索引；而只有 registrar 可以改為指名任何小於 S 的索引",
   "索引是用 prior 的熵累積器從 H(E(s, η_0, H_t)) 導出的，然後向下探測直到出現空位；保留區塊是索引空間的最上面 2^16 個而不是最下面的，而且任何 service（不只 registrar）都可以認領那些保留位置之一"
  ],
  "stem": "A service calls `new` during accumulation. How does GP 0.8.0 pick the index of the child account, and how is a clash with an existing service avoided?",
 "options": [
  "The index is Blake2b of the new account's code hash reduced mod 2^32, so that identical code always lands on the same slot and duplicate deployments are cheap; there is no probing at all, and should that index already be occupied the whole block is rejected as invalid.",
  "The index is the largest key currently present in δ plus one, so indices are handed out strictly sequentially across the whole chain and a clash is impossible by construction; the registrar merely reserves the first 2^16 of them at genesis and hands them out off-chain.",
  "The context's next free id starts as check((E⁻¹_4(H(E(s, η′_0, H_t))) mod (2^32 − S − 2^8)) + S) with S = 2^16, so it is folded into the public range only; check linearly probes forward, i ↦ (i − S + 1) mod (2^32 − 2^8 − S) + S, until it lands on an index outside K(δ); the registrar alone may instead name any index below S.",
  "The index is derived from H(E(s, η_0, H_t)) using the prior entropy accumulator and then probed downwards until a free slot appears; the reserved block is the top 2^16 of the index space rather than the bottom, and any service — not merely the registrar — may claim one of those reserved slots."
 ],
 "answer": 2,
 "optNotes": [
   "以 code hash 為種子會讓相同 code 的服務互撞，而 GP 給的是線性探測而非直接判區塊無效。",
   "純遞增計數器在 parallel accumulation（Δ*）下無法決定性合併；protected range 也不是鏈下發放。",
   "種子是 H(E(s, η′_0, H_t))，模數扣掉 S 與最高 2^8 折進 public range，check 再往前線性探測。",
   "用 prior η_0 會讓 index 在區塊執行前就可預測；保留區是最低的 2^16，而且只有 registrar 能指定。",
 ],
 "explanation": "附錄 B 的 initializer I：a（next free id）= check((E⁻¹_4(H(E(s, η′_0, H_t))) mod (2^32 − S − 2^8)) + S)，用的是**posterior** entropy accumulator η′_0 與本區塊的 H_t；模數刻意扣掉 S = C_minpublicindex = 2^16（registrar 專屬的 protected range）與最高的 2^8，所以隨機落點一定在 public range。eq. B.14 的 check(i) = i 若 i ∉ K(δ)，否則 check((i − S + 1) mod (2^32 − 2^8 − S) + S)——就是往前線性探測到第一個空位。成功 `new` 之後 context 的下一個 id 再跳 42：i* = check(S + (a − S + 42) mod (2^32 − S − 2^8))。registrar 路徑另走一條：當 caller = χ_R 且要求的 id < S，直接用該 id（已被占用則 FULL）。GP 也補了一句保險：萬一同一個 index 真的被兩個 service 取走，「the block is considered invalid」，但「Since no service can predict the identifier sequence ahead of time, they cannot intentionally disadvantage the block author.」——不可預測性正是這個設計要守住的性質。",
 "trap": "η′_0（posterior）不是 η_0；並且 `new` 只在 accumulate 內可用，refine 沒有 δ。"
},
{
 "id": "c3-ch09-privilege-mutation",
 "ch": "9", "section": "9.4 Service Privileges",
 "gpRef": "eq. 9.9–9.10 (χ); App. B `bless` (Ω_B), `assign` (Ω_A), `new` (Ω_N)",
 "difficulty": 3, "kind": "delta", "tags": ["accounts", "privileges", "gratis", "delta-0.8.0"],
  "stemZh": "你們的 Go 節點停在 GP 0.7.2，那裡的「Owned Privileges」模型讓每個具特權的 service 各自改寫自己在 χ 中的位置。GP 0.8.0 改了什麼？又是誰可以給一個全新帳戶非零的 gratis storage 抵扣 a_f？",
  "optionsZh": [
   "Ω_B 仍然可以被五個具特權 service 中的任何一個呼叫，各自只改寫自己擁有的那一格；manager 的特別之處僅在於它可以授予儲存押金額度，而 `new` 接受來自 manager 或 registrar 的 f ≠ 0",
   "Ω_B 對任何自身索引低於 S = 2^16 的 service 開放，因為佔據保留範圍本身就是特權的來源；χ_A[c] 之後就只有 manager 能移動，而 service 是透過 `upgrade` 提高自己的 a_f",
   "在 0.8.0 中 χ 已經完全不能被 host call 變動；它只能由列在 χ_Z 中的 service 在每個區塊自動獲得的 accumulation 裡改寫，而 a_f 對每個帳戶在創世時就固定、之後任何人（包括 manager）都無法提高",
   "Ω_B 是唯一整批改寫 (χ_M, χ_A, χ_V, χ_R, χ_Z) 的 host call，而它現在除非呼叫者本身就是 χ_M、否則產生 HUH，因此沒有任何 service 能把自己升格為 manager；某個 core 的 assigner 仍可透過 `assign` 交出自己的 χ_A[c]，而 `new` 在 f ≠ 0 且呼叫者不是 manager 時產生 HUH"
  ],
  "stem": "Your Go node is on GP 0.7.2, where the 'Owned Privileges' model let each privileged service rewrite its own slot of χ. What does GP 0.8.0 change, and who may hand a brand-new account a non-zero gratis storage offset a_f?",
 "options": [
  "Ω_B may still be invoked by any of the five privileged services, each rewriting only the slot it owns; the manager is special solely in that it may grant storage deposit credits, and `new` accepts f ≠ 0 from either the manager or the registrar.",
  "Ω_B is open to any service whose own index sits below S = 2^16, since occupying the protected range is what confers privilege in the first place; χ_A[c] may then only be moved by the manager, and a service raises its own a_f through `upgrade`.",
  "χ is no longer mutable by host calls at all in 0.8.0; it may only be rewritten by the services listed in χ_Z as part of the automatic accumulation they receive in every block, and a_f is fixed for every account at genesis and can never be raised afterwards by anyone, manager included.",
  "Ω_B is the one host call that rewrites (χ_M, χ_A, χ_V, χ_R, χ_Z) wholesale, and it now yields HUH unless the caller is χ_M itself, so no service can promote itself to manager; a core's assigner may still hand over its own χ_A[c] through `assign`, and `new` yields HUH whenever f ≠ 0 and the caller is not the manager."
 ],
 "answer": 3,
 "optNotes": [
   "這是 0.7.1 的 Owned Privileges；0.8.0 的 Ω_B 已限定呼叫者必須是 χ_M，gratis 也只認 manager。",
   "低 index 只是 registrar 能指定的保留區、與特權無關；Ω_U 只能改 a_c/a_g/a_m，碰不到 a_f。",
   "χ_Z 只是「每個區塊自動 accumulate 並配基本 gas」的字典，沒有任何寫 χ 的能力。",
   "#519 在 Ω_B 加上 x_s ≠ (x_e)_m → HUH，而 Ω_N 的 gratis 守衛是 f ≠ 0 ∧ x_s ≠ (x_e)_m。",
 ],
 "explanation": "GP 0.8.0（PR #519「Restrict bless to manager service」）在 Ω_B 加了一條守衛：「⟨continue, HUH, …⟩ otherwhen x_s ≠ (x_e)_m」（x_s 是呼叫者的 service index，x_e 是 invocation context 裡的 partial state）——也就是呼叫者不是 χ_M 就整組 HUH。§9.4 原文也改成 χ_M「is the service able to effect an alteration of χ from block to block as well as bestow services with storage deposit credits」。0.7.1 的 Owned Privileges（#475）讓每個特權服務改自己那格，攻擊面是：某服務先 bless 自己成 manager，再用 `new` 配 gratis storage、或把自己設成 registrar 去搶 < S 的低位 index。要留意 0.8.0 並沒有把「自有權」全部收回：Ω_A（`assign`）仍然要求 x_s = (x_e)_a[c] 才能寫 φ[c]，而且它同時寫回 χ_A[c]，所以 assigner 依然能把自己那一核的權限交棒；Ω_D（`designate`）則只要求 x_s = (x_e)_v，能改 ι 但改不了 χ_V。gratis 的守衛則在 Ω_N：「⟨continue, HUH, …⟩ otherwhen f ≠ 0 ∧ x_s ≠ (x_e)_m」。",
 "trap": "0.7.2 → 0.8.0 的一句話：bless 只剩 manager 能叫；但 assign 仍保留 per-core 的自有權。"
},

# ---------------------------------------------------------------- app. D ----
{
 "id": "c3-appD-key-31-octets",
 "ch": "D", "section": "D.2.1 Node Encoding and Trie Identification",
 "gpRef": "§D.1 (C → B_31); §D.2.1 (nodes fixed at 512 bit)",
 "difficulty": 1, "kind": "rationale", "tags": ["merklization", "trie", "state-keys"],
  "stemZh": "state-key 建構子 C 被規定產出 B_31，然而 state trie 中其他每一個量——子節點識別、內嵌值的欄位、H(v)——都是 32 個 octet。是什麼迫使 key 少一個 octet？",
  "optionsZh": [
   "最高位的那個 octet 被保留下來，好讓 branch／leaf 的判別位元能被攜帶在 key 本身之內，這正是讓驗證者不必取得節點就能分辨兩種節點型別的機制",
   "一個節點固定為 512 位元，而一片葉子必須容納一個位元組的「判別子加大小」標頭、那把 key、以及一個完整 32 位元組的欄位（放值本身或它的雜湊）：1 + 31 + 32 = 64",
   "key 是 Blake2b 的輸出，在儲存前把一個位元組的章節索引剝掉了；值的欄位同樣是 31 個 octet，只有在被雜湊時才補到 32",
   "31 個 octet 讓 branch 節點多留一個備用 octet，好在子 trie 超過 2^8 的分支上限時能附加第三個子節點指標"
  ],
  "stem": "The state-key constructor C is specified as producing B_31, yet every other quantity in the state trie — child identities, the embedded value slot, H(v) — is 32 octets. What forces the key to be one octet short?",
 "options": [
  "The top octet is reserved so that the branch/leaf discriminator bit can be carried inside the key itself, which is what lets a verifier tell the two node types apart without fetching the node.",
  "A node is fixed at 512 bit, and a leaf must fit a one-octet discriminator-plus-size header, the key, and a full 32-octet field for either the value or its hash: 1 + 31 + 32 = 64.",
  "Keys are Blake2b outputs with the one-octet chapter index stripped off before storage; the value field is likewise 31 octets, padded to 32 only when hashed.",
  "31 octets leaves one spare octet in a branch node so that a third child pointer can be appended when a sub-trie exceeds the 2^8 fan-out limit."
 ],
 "answer": 1,
 "optNotes": [
   "discriminator 位在 node 的第一個 byte；key 的每個 bit 都要拿去做 trie 導航，不能挪用。",
   "1 + 31 + 32 = 64：header octet 加 key 加整整 32 octet 的 value 或 H(v)，正好填滿 512 bit。",
   "value 欄位是完整 32 octet 並以零填充，不是 31；key 也不是把某個 byte 拿掉之後的結果。",
   "branch 只有左右兩個 child（左邊 255 bits、右邊 256 bits），沒有第三個 child 的概念。",
 ],
 "explanation": "§D.2.1：「Nodes are fixed in size at 512 bit (64 bytes).」leaf 的版面是：第 1 bit 分辨 branch/leaf，第 2 bit 分辨 embedded-value leaf 與 regular leaf，該 byte 剩下的 6 bits 存 embedded value 的長度（regular leaf 則清零）；「The following 31 bytes are dedicated to the state key. The last 32 bytes are defined as the value, filling with zeroes if its length is less than 32 bytes」或是 H(v)。31 就是 64 扣掉 header octet 與整整 32 octet 的 value/hash 欄位之後剩下的空間——這也是 §D.1 一開始就說 state serialization 是「a mapping from 31-octet sequence state-keys to octet sequences of indefinite length」的原因，key 的長度是版面算出來的結果而非任何語意保留。",
 "trap": "JIP-4 chainspec 的 genesis_state 每個 key 是 62 個 hex 字元 = 31 bytes，正好對得上。"
},
{
 "id": "c3-appD-service-subkeys",
 "ch": "D", "section": "D.1 Serialization",
 "gpRef": "§D.1 (state-key constructor C; the final four rows of T(σ))",
 "difficulty": 2, "kind": "concept", "tags": ["merklization", "state-keys", "accounts"],
  "stemZh": "在 T(σ) 中，某個 service 的 storage 條目、它的 preimage、以及它的 lookup-meta 條目全都走同一個 C 的第三種形式。究竟傳進去的是什麼？又是什麼讓這三類在 trie 中彼此分開？",
  "optionsZh": [
   "三者是靠完成後那 31 位元組 key 的第 0 個 octet 區分的：storage 是 0xFD、preimage 是 0xFE、lookup-meta 是 0xFF，其餘 30 個 octet 直接放 H(k) 或雜湊 h，而 service 索引則被摺進值而不是 key 裡",
   "storage 用帶原始 key 的 C(s, k)、preimage 用章節形式 C(254, s)、lookup-meta 用 C(253, s)；根本不需要任何標記，因為三者已經住在不同的章節索引之下，而 lookup 條目的 (h, l) 配對是從葉子的值而不是它的 key 還原的",
   "在雜湊之前會先加上一個四位元組的標記——storage 是 E_4(2^32−1) ⌢ k、preimage 是 E_4(2^32−2) ⌢ h、宣告長度為 l 的 lookup-meta 是 E_4(l) ⌢ h——接著 C(s, ·) 把 n = E_4(s) 的四個 octet 與 a = H(·) 的前四個 octet 交錯，再附上 a_4 … a_26",
   "三者都用 C(s, h)，其中 h 是原始的 storage key 或 preimage 雜湊、完全沒有任何標記；碰撞不可能發生，因為 §9 要求 service 的 storage key 必須恰好 32 個 octet 長，這讓它待在一個與 32 位元組 preimage 雜湊互斥的命名空間裡"
  ],
  "stem": "In T(σ) a service's storage entries, its preimages and its lookup-meta entries all go through the very same third form of C. What exactly is passed in, and what keeps the three kinds apart in the trie?",
 "options": [
  "The three kinds are told apart by octet 0 of the finished 31-octet key, which is 0xFD for storage, 0xFE for a preimage and 0xFF for lookup-meta, with the remaining 30 octets holding H(k) or the hash h directly and the service index folded into the value rather than the key.",
  "Storage uses C(s, k) with the raw key, preimages use the chapter form C(254, s) and lookup-meta uses C(253, s); no marker is needed at all because the three already live under distinct chapter indices, and the (h, l) pair of a lookup entry is recovered from the leaf's value rather than its key.",
  "A four-octet marker is prepended before hashing — E_4(2^32−1) ⌢ k for storage, E_4(2^32−2) ⌢ h for a preimage, and E_4(l) ⌢ h for the lookup-meta of declared length l — and C(s, ·) then interleaves the four octets of n = E_4(s) with the first four octets of a = H(·), appending a_4 … a_26.",
  "All three use C(s, h) with h the raw storage key or preimage hash and no marker whatsoever; collisions cannot arise because a service storage key is required by §9 to be exactly 32 octets long, which keeps it inside a namespace disjoint from the 32-octet preimage hashes."
 ],
 "answer": 2,
 "optNotes": [
   "octet 0 是 n_0，也就是 service id 的最低位 byte——你們的 #779/#780 正是踩到這個誤解。",
   "chapter 形式只用在 C(255, s) 的 service info；三者共用第三形式，靠輸入的 marker 分開。",
   "三列 T(σ) 的 marker 是 E_4(2^32−1)／E_4(2^32−2)／E_4(l)，C(s, ·) 再把 E_4(s) 與 H(·) 交錯成 31 bytes。",
   "GP 明說 storage key 長度完全自由；沒有 marker 就無從保證 C 的輸入互斥。",
 ],
 "explanation": "§D.1 的 T(σ) 最後三列逐字寫著：∀⟨s ↦ a⟩ ∈ δ, ⟨k ↦ v⟩ ∈ a_s：C(s, E_4(2^32−1) ⌢ k) ↦ v；∀⟨h ↦ p⟩ ∈ a_p：C(s, E_4(2^32−2) ⌢ h) ↦ p；∀⟨(h, l) ↦ t⟩ ∈ a_l：C(s, E_4(l) ⌢ h) ↦ E(↕[E_4(x) for x ∈ t])。而第三形式的 C 本身是 (s, h) ↦ [n_0, a_0, n_1, a_1, n_2, a_2, n_3, a_3, a_4, a_5, …, a_26]，其中 n = E_4(s)、a = H(h)——service id 的四個 byte 與雜湊的前四個 byte 交錯，之後接雜湊的第 4…26 byte，共 8 + 23 = 31 bytes。GP 接著保證：「Cryptographic hashing ensures that there will be no duplicate state-keys given that there are no duplicate inputs to C.」——不重複性靠的是 C 的**輸入**互斥，marker 就是把三個命名空間分開的手段；也因此 2^32−1 與 2^32−2 這兩個長度值等於被保留掉：只有當某個 service 同時存在一筆長度剛好是 2^32−1 的 lookup 請求、且其 hash 與某個 32-byte storage key 相同時才會撞上，而 0.8.0（PR #520）已把 preimage 長度收進 N_L ≡ N_{2^32}（注意這個型別**仍然包含** 2^32−1 與 2^32−2 兩個保留值，形式上並未排除碰撞，靠的是實務尺寸），實務上 preimage 遠小於 4 GiB，所以安全。",
 "trap": "GP 明說 storage key「not required to be known by implementations」——只要存得下 Merklisation-ready 的雜湊即可，原始 key 可以不落盤。"
},
{
 "id": "c3-appD-rho-guarantee",
 "ch": "D", "section": "D.1 Serialization",
 "gpRef": "§D.1 T(σ) row C(10); eq. 11.1 (ρ spec)",
 "difficulty": 3, "kind": "delta", "tags": ["merklization", "state-keys", "rho", "delta-0.8.0"],
  "stemZh": "你們 0.7.2 的編碼器把 T(σ) 的 C(10) 條目寫成：每個 core 一個「work-report 與回報時槽」的 optional 配對。GP 0.8.0 改成放什麼？",
  "optionsZh": [
   "與先前完全相同的「每個 core 一個 work-report 與時槽的 optional 配對」；0.8.0 只是把時槽收緊成定長的 E_4 編碼，酬載本身沒有更動",
   "每個 core 一個以 ? 選項判別子寫出的 optional 配對 ⟨a_g, E_4(a_t)⟩，其中 a_g 是整份 guarantee G ≡ (r work-report, t 時槽, a 由 2–3 組 (validator 索引, Ed25519 簽章) 構成的憑證)——因此 guarantor 的簽章現在成為被承諾狀態的一部分",
   "當前區塊的 availability assurances extrinsic，好讓某位 assurer 的 bitfield 不必重放該區塊就能對照 state root 被證明",
   "只放每個 core 待處理 report 的 availability specification（package 雜湊、erasure root、segment root、bundle 長度），而 guarantee 本身由 guarantor 保存在鏈外直到稽核要求為止；這正是 0.8.0 所追求的體積縮減"
  ],
  "stem": "Your 0.7.2 encoder writes the C(10) entry of T(σ) as, per core, an optional pair of work-report and reporting timeslot. What does GP 0.8.0 put there instead?",
 "options": [
  "Per core an optional pair of work-report and timeslot exactly as before; 0.8.0 only tightened the timeslot to a fixed-length E_4 encoding and left the payload alone.",
  "Per core an optional pair ⟨a_g, E_4(a_t)⟩ written with the ? option discriminator, where a_g is the entire guarantee G ≡ (r work-report, t timeslot, a credential of 2–3 (validator index, Ed25519 signature) pairs) — so the guarantors' signatures are now part of committed state.",
  "The availability assurances extrinsic of the current block, so that an assurer's bitfield can be proven against the state root without replaying the block.",
  "Only the availability specification (package hash, erasure root, segment root, bundle length) of each core's pending report, the guarantee itself being retained off-chain by the guarantors until an audit demands it; that is precisely the size reduction 0.8.0 was aiming for."
 ],
 "answer": 1,
 "optNotes": [
   "0.8.0 換掉的是 payload 本身：ρ 現在存整個 guarantee，連 guarantor 的 credential 都在內。",
   "#494 把 eq. 11.1 改成 ρ ∈ ⟦(g ∈ G, t ∈ N_T)?⟧_C，guarantor 簽章因此進入 committed state。",
   "extrinsic 從不進 trie，這是把 extrinsic 與 state 兩件事搞混了。",
   "availability specification 是 work-report 內部的欄位而非 ρ 的內容，0.8.0 也是加大而非縮小這一格。",
 ],
 "explanation": "GP 0.8.0（PR #494「Keep full guarantees in availability assignments state (rho)」）把 eq. 11.1 改成 ρ ∈ ⟦(g ∈ G, t ∈ N_T)?⟧_C，而 G ≡ (r ∈ R, t ∈ N_T, a ∈ ⟦(N, V̄)⟧_{2:3})（eq. 11.24；0.8.0 的 R 是 work-report 集合、W 是 work-item 集合、V̄ 是 Ed25519 簽章集合），也就是 work-report 加上 guarantor 的 credential。附錄 D 的 T(σ) 因此寫成 C(10) ↦ E([ ⟨a_g, E_4(a_t)⟩? for ⟨a_g, a_t⟩ ∈ ρ ])——外層是 optional discriminator（∅ → 0；否則 1 ⌢ …），內層 timeslot 用固定 4 byte。0.7.2 只存 work-report、signature 不進 state；升上 0.8.0 若沒改，C(10) 的 leaf 會短一大截、state root 直接對不上。注意 guarantee 自己帶一個 t（guarantee 的 timeslot），availability assignment 又帶一個 t（reported 的時間，用於 eq. 11.18 的 U 逾時清除），兩者不是同一個欄位。",
 "trap": "0.8.0 之後 ρ[c] 有兩個 timeslot：guarantee 內的 g_t，以及 assignment 的 a_t。序列化時別漏掉前者。"
},
{
 "id": "c3-appD-merklize-bitorder",
 "ch": "D", "section": "D.2 Merklization",
 "gpRef": "§D.2 (M over D⟨b → (B_31, B)⟩); §3 notation (bits(·) is most-significant-first)",
 "difficulty": 3, "kind": "code", "tags": ["merklization", "trie", "state-root", "incremental"],
  "stemZh": "M 是定義在以 bits(k) 為鍵的字典之上，而團隊的 Go 是在每個深度就地切分同一個 slice。有位隊友提議把它換成「把 key-val 升冪排序，然後像 M_B 那樣兩兩摺疊——同樣的葉子、同樣的 root，而且更好向量化」。哪個敘述正確？",
  "optionsZh": [
   "這個提議是可行的：升冪的 key 順序恰好就是 Patricia trie 的前序走訪，所以兩兩摺疊會重建出完全相同的形狀與 root；就地切分只不過是一項配置最佳化，而葉子快取兩種做法都能繼續運作，因為一片葉子的雜湊只取決於它自己的 key 與 value",
   "bits(·) 是最低位在前，好與附錄 C 的位元序列編碼 E(b) 一致，所以深度 d 必須對第 ⌊d/8⌋ 個 octet 的第 d mod 8 位元分支；因此圖中的切分方向是反的，而這種實作之所以還能對上向量，只是因為它的 state-key 建構子也一併反了",
   "插入順序在這裡確實重要：GP 要求葉子必須依升冪 key 順序摺疊，因為產生的 root 是要被 M_R 附加到 accumulation-output belt（一個 append-only 結構）上的；因此跨區塊快取葉子雜湊並不可靠，trie 每個區塊都必須整棵重建",
   "bits(·) 是最高位在前，所以深度 d 對第 ⌊d/8⌋ 個 octet 的第 7 − (d mod 8) 位元分支；樹形只由 key 的位元前綴決定、從不取決於 slice 的順序，這正是讓葉子雜湊可以被快取、而只需重算「從變動葉子到 root」那條路徑的原因——把排序後的葉子兩兩摺疊建出來的是一棵平衡樹，root 也不同"
  ],
  "stem": "M is defined over a dictionary keyed by bits(k), while the team's Go partitions one slice in place at each depth. A teammate proposes replacing it with 'sort the key-vals ascending, then fold them pairwise like M_B — same leaves, same root, and it vectorizes better'. Which statement is correct?",
 "code": {
  "lang": "go",
  "caption": "internal/utilities/merklization/merklization.go (partitionByBit, merklizeWithCache)",
  "src": """func partitionByBit(entries []types.StateKeyVal, depth int) int {
	byteIdx := depth / 8
	bitMask := byte(1 << (7 - depth%8))
	left := 0
	for right := range entries {
		if entries[right].Key[byteIdx]&bitMask == 0 {
			entries[left], entries[right] = entries[right], entries[left]
			left++
		}
	}
	return left
}

func merklizeWithCache(entries []types.StateKeyVal, depth int, cache LeafHashCache) types.OpaqueHash {
	if len(entries) == 0 {
		return types.OpaqueHash{}
	}
	if len(entries) == 1 {
		if cache != nil {
			return cache(entries[0].Key, entries[0].Value)
		}
		node := encodeLeafNode(entries[0].Key, entries[0].Value)
		return hash.Blake2bHash(node[:])
	}
	pivot := partitionByBit(entries, depth)
	leftHash := merklizeWithCache(entries[:pivot], depth+1, cache)
	rightHash := merklizeWithCache(entries[pivot:], depth+1, cache)
	node := encodeBranchNode(leftHash, rightHash)
	return hash.Blake2bHash(node[:])
}"""
 },
 "options": [
  "The proposal is sound: ascending key order is exactly a pre-order walk of the Patricia trie, so pairwise folding rebuilds the identical shape and the identical root; the in-place partition is nothing but an allocation optimization, and leaf caching keeps working either way because a leaf hash depends on nothing beyond its own key and value.",
  "bits(·) runs least-significant-bit first so as to agree with the bit-sequence encoding E(b) of appendix C, so depth d has to branch on bit d mod 8 of octet ⌊d/8⌋; the partition shown is therefore reversed, and the only reason such an implementation ever matches a vector is that its state-key constructor is reversed too.",
  "Insertion order genuinely matters here: the GP requires the leaves to be folded in ascending key order because the resulting root is what gets appended to the accumulation-output belt by M_R, an append-only structure; caching leaf hashes across blocks is consequently unsound and the trie must be rebuilt in full every block.",
  "bits(·) runs most-significant-bit first, so depth d branches on bit 7 − (d mod 8) of octet ⌊d/8⌋; the shape follows from key bit-prefixes alone and never from slice order, which is what lets leaf hashes be cached and only the path from a changed leaf to the root recomputed — folding sorted leaves pairwise builds a balanced tree and a different root."
 ],
 "answer": 3,
 "optNotes": [
   "排序後 pairwise 摺疊得到的是 well-balanced 樹（M_B 的做法），深度與分岔點都不同，root 必然不同。",
   "附錄 C 的 E(b) 確實是 LSB-first 打包，但那是 codec；trie 導航用的 bits(·) 是 MSB-first。",
   "M 的樹形只由 key 的 bit prefix 決定；M_R 的 append-only 屬性屬於 accumulation-output belt，與 state trie 無關。",
   "bits(·) 是 MSB-first，樹形只由 key 的 bit prefix 決定，這正是 leaf hash 能跨區塊快取的前提。",
 ],
 "explanation": "§3（notation）定義得很明確：「We use the function bits(B) ∈ b to denote the sequence of bits, ordered with the most significant first … thus bits([160, 0]) = [1, 0, 1, 0, 0, …]」，所以 depth d 要取 octet ⌊d/8⌋ 的第 7 − (d mod 8) 個 bit——正是程式裡的 `byte(1 << (7 - depth%8))`。§D.2 的 M 收的是 dictionary D⟨b → (B_31, B)⟩，遞迴條件是 ⟨b ↦ p⟩ ∈ d ⇔ ⟨b[1:] ↦ p⟩ ∈ l（當 b_0 = 0）或 r（當 b_0 = 1）：樹形**只**由 key 的 bit prefix 決定，跟輸入順序無關。這正是 incremental／cached 計算的前提：leaf hash 可以用 (key, H(value)) 當快取鍵（你們的 `LeafHashCache` 與 `key_level_cache.go` 就是這樣做），一個 block 只改動幾百個 key 時，只需要重算那幾條從 leaf 到 root 的路徑，而不是整棵 trie——否則每個 block 都要重雜湊整個 state，pipelining（header 帶 prior state root）就完全沒有意義了。順帶把幾種 Merkle 結構分清楚：M_B 用在 accumulation-output log 每區塊的 root（β_B′ ≡ A(β_B, M_B(s, keccak), keccak)）與 work-package 的 erasure root；segment root 用定深的 constant-depth merklization；M_R 是 MMR super-peak；而 0.8.0 的 extrinsic hash 根本不是 Merkle 樹：H_X ≡ H(E(H^#(a)))（PR #524）。",
 "trap": "同一份 GP 裡有兩種 bit 順序：trie 導航 bits(·) 是 MSB-first，codec 的 bitstring 打包是 LSB-first。"
},

]
