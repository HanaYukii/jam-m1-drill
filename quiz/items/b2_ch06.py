# -*- coding: utf-8 -*-
# Chapter 6 — Block Production and Chain Growth (Safrole), GP 0.8.0 — batch 2 (new angles)
# Sources: gp-src/text/safrole.tex, header.tex (§5), notation.tex (§3.8.2), bandersnatch.tex (App. G);
#          team-repo internal/safrole/*.go (main = 0.7.2, HEAD c7fb743) and branch 1012-update-to-v080 (PR #1025);
#          research/issues-digest.md (#284, #770, #784/#791, #825, #1013/#1025, #1037, #1040/#1041);
#          w3f/jamtestvectors stf/safrole README (tiny cases).
ITEMS = [
{
 "id": "ch06-code-useless-ticket-gap",
 "ch": "6", "section": "6.7 The Extrinsic and Tickets", "gpRef": "eq. 6.35–6.36 — internal/safrole/extrinsic_tickets.go CreateNewTicketAccumulator",
 "difficulty": 3, "kind": "code", "tags": ["safrole", "tickets", "code", "fuzzer"],
 "stem": "This is the tail of the team's CreateNewTicketAccumulator (identical on main and on the 0.8.0 branch), reached after the new tickets passed the tail/attempt/proof/order/duplicate checks. A block at m′ = 300 carries 3 valid tickets whose ids are all HIGHER than every id in a saturated γ_A (|γ_A| = E). What does the GP require, and what does this code do?",
 "code": {"lang": "go", "caption": "internal/safrole/extrinsic_tickets.go (CreateNewTicketAccumulator, tail)", "src": """// (6.34) Get previous ticket accumulator
previousTicketsAccumulator := GetPreviousTicketsAccumulator()

// (6.34) Concatenate the new tickets and the previous ticket accumulator
newTicketsAccumulator := append(newTickets, previousTicketsAccumulator...)

// (6.34) sort the tickets by ticket id
sort.Slice(newTicketsAccumulator, func(i, j int) bool {
    return bytes.Compare(newTicketsAccumulator[i].ID[:], newTicketsAccumulator[j].ID[:]) < 0
})

// (6.33) Verify the new tickets accmuulator
err = VerifyTicketsDuplicate(newTicketsAccumulator)
if err != nil {
    // Found a ticket duplicate (Someone submitted the same ticket)
    return err
}

// (6.34) select E tickets from the sorted tickets for the new ticket accumulator
maxTicketsAccumulatorSize := types.EpochLength
if len(newTicketsAccumulator) > maxTicketsAccumulatorSize {
    newTicketsAccumulator = newTicketsAccumulator[:maxTicketsAccumulatorSize]
}

// (6.34) set the new ticket accumulator to the posterior state
cs.GetPosteriorStates().SetGammaA(newTicketsAccumulator)

return nil"""},
 "options": [
  "The block is valid per eq. 6.35: γ′_A simply keeps the lowest E ids, so the 3 tickets are not retained and nothing further is required of the block; this code is fully conformant and needs no extra check",
  "Eq. 6.36 (n ⊆ γ′_A) makes the block INVALID, but this code silently drops the 3 tickets in the [:E] truncation and accepts it — a block that the reference implementation rejects",
  "The block is invalid per eq. 6.34 because the new ids collide with γ_A, and VerifyTicketsDuplicate on the merged, sorted sequence is exactly the check that catches this case, so the code is conformant",
  "The block is invalid per eq. 6.31 because tickets are only accepted while |γ_A| < E; the code should compare len(previousTicketsAccumulator) with E before merging and return UnexpectedTicket"
 ],
 "answer": 1,
 "optNotes": [
  "漏掉 6.36：γ′_A 的確等於 γ_A，但「沒擠進前 E 名的 ticket」讓整個區塊必須被拒絕。",
  "6.36 要求 n ⊆ γ′_A，而這裡 `[:maxTicketsAccumulatorSize]` 截掉後就 SetGammaA、return nil。",
  "6.34 講的是 id **相同**；VerifyTicketsDuplicate 只比排序後相鄰是否相等，抓不到較大的合法 id。",
  "6.31 限的是 |E_T| ≤ K，與 |γ_A| 無關——accumulator 已滿仍可接受分數更好的 ticket。",
 ],
 "explanation": "eq. 6.35：γ′_A ≡ 取 sort_by_id(n ∪ (∅ if e′ > e else γ_A)) 的最低 E 筆；eq. 6.36 緊接著要求 n ⊆ γ′_A：「It is invalid to include useless tickets in the extrinsic, so all submitted tickets must exist in their posterior ticket accumulator」。這段程式（main 與 1012-update-to-v080 分支相同）沒有任何「截斷後確認 newTickets 仍在 accumulator 內」的步驟，SafroleErrorCode 也沒有對應的 code；w3f 的 safrole vectors 沒有 useless-ticket 失敗案例（fail cases 只有 bad attempt / already recorded / bad order / bad proof / lottery over），所以一直沒被抓到，但 fuzzer 若產生這種區塊，reference 會拒絕、你們會接受，state 立刻分岔。對照 vector publish_tickets_with_mark-3：「Publish some tickets with a full accumulator. Some old ticket are removed to make space for new ones」——滿載的 accumulator 本來就還能收更好的票。修法：截斷後確認 newTickets 的最大 id ≤ γ′_A 的最後一筆（或逐一 Contains），失敗就回傳錯誤。",
 "trap": "口訣：進不了前 E 名的 ticket 不是被丟掉，而是讓整個區塊作廢（6.36）。"
},
{
 "id": "ch06-code-attempt-cap-v080",
 "ch": "6", "section": "6.7 The Extrinsic and Tickets", "gpRef": "eq. 6.30 (n = ⌈2E/|γ′_P|⌉) — internal/safrole/extrinsic_tickets.go VerifyTicketsAttempt (branch 1012-update-to-v080, PR #1025)",
 "difficulty": 2, "kind": "code", "tags": ["safrole", "tickets", "code", "delta-0.8.0"],
 "stem": "This is VerifyTicketsAttempt on the team's 0.8.0 branch (PR #1025); on main (0.7.2) it compared Attempt against the constant TicketsPerValidator. Which statement about it is correct?",
 "code": {"lang": "go", "caption": "internal/safrole/extrinsic_tickets.go (VerifyTicketsAttempt, branch 1012-update-to-v080)", "src": """func VerifyTicketsAttempt(tickets types.TicketsExtrinsic) *types.ErrorCode {
    numV := len(blockchain.GetInstance().GetPosteriorStates().GetGammaK())
    if numV == 0 {
        ...
        if len(tickets) > 0 {
            err := SafroleErrorCode.BadTicketAttempt
            return &err
        }
        return nil
    }
    // n = ceil(2E / numV) via integer arithmetic.
    n := (2*types.EpochLength + numV - 1) / numV

    for _, ticket := range tickets {
        // ticket.Attempt is an entry index (0-based); reject Attempt >= n.
        if ticket.Attempt >= types.TicketAttempt(n) {
            err := SafroleErrorCode.BadTicketAttempt
            return &err
        }
    }

    return nil
}"""},
 "options": [
  "It has an off-by-one: eq. 6.30 puts the entry index in N_n, which by §3.4 includes n itself, so Attempt == n must be accepted and the comparison should be > n rather than >= n; in tiny mode (E = 12, |γ′_P| = 6) this wrongly rejects entry index 4",
  "It uses the wrong set: n must be derived from |κ′|, the active set, because tickets are submitted by the validators authoring blocks right now; taking GetGammaK makes the bound change one epoch too early on any chain whose set size varies",
  "It is only a refactor: because offenders are zeroed in place rather than removed, |γ′_P| always equals V, so 0.7.2's constant TicketsPerValidator (3 tiny / 2 full) already produced exactly the same bound and no test vector changes behaviour",
  "It implements n = ⌈2E/|γ′_P|⌉ with the posterior pending set (the team's GammaK), i.e. the ring the tickets are proven against; (2E + |γ′_P| − 1) / |γ′_P| is the integer ceiling and the bound is exclusive because N_n = {0, …, n−1}"
 ],
 "answer": 3,
 "optNotes": [
  "誤讀 §3.4：N_n = {x | x < n} 是嚴格小於，tiny 下合法的 entry index 是 0…3 而非 0…4。",
  "分母必須與 ticket 所證明的 ring 是同一個集合——ring 由 γ′_P 的 Bandersnatch key 建成。",
  "與 PR #1025 的事實相反：tiny 的 bound 從 3 變成 4，舊 vector 才被標成 IsV080IncompatibleVector。",
  "分母取 posterior 的 γ′_P，(2E + |γ′_P| − 1) / |γ′_P| 是整數 ceiling，上界 exclusive 也正確。",
 ],
 "explanation": "eq. 6.30：E_T ∈ [(r ∈ N_n, p ∈ F̄^{X_T ⌢ η′_2 ++ r}_{γ′_Z}([]))]，n = ⌈2E/|γ′_P|⌉——分母是 **posterior pending set** γ′_P（你們命名為 GammaK），因為 ticket 是對 γ′_Z（由 γ′_P 的 Bandersnatch key 建 ring）做 ring proof，是「下個 epoch 的 validator」在投票，與本 epoch 出塊的 κ′ 無關。§3.4：N_n = {x ∈ N, x < n}。算例：tiny E = 12、|γ′_P| = 6 → (24+5)/6 = 4；full E = 600、1023 → (1200+1022)/1023 = 2。0.7.2 main 用常數 TicketsPerValidator（tiny 3 / full 2），tiny 下 entry index 3 在 0.8.0 變成合法（PR #1025 因此把舊 vector publish-tickets-no-mark-1「bad ticket attempt number」標成 IsV080IncompatibleVector 跳過）；同一個 PR 也把 VerifyEpochTail 的上限從 ValidatorsCount 改成 MaxTicketsPerBlock（K，eq. 6.31）。GP 的理由：「To ensure the accumulator can be saturated, when there are fewer validators, each validator is permitted more tickets」（每個 slot 期望約 2 張 ticket）。",
 "trap": "n 的分母是 |γ′_P| 不是 |κ′|；上界是 exclusive（r < n）；tiny 的 n 從 3 變 4。"
},
{
 "id": "ch06-code-header-checks-posterior",
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "eq. 6.16–6.18, 6.28; §5 eq. 5.10 — internal/stf/sft.go RunSTF, validate_header.go ValidateHeaderVrf",
 "difficulty": 3, "kind": "code", "tags": ["safrole", "seal", "markers", "code", "fuzzer", "epoch"],
 "stem": "The team's RunSTF validates the header in two phases around UpdateSafrole; passing the POSTERIOR state to the second phase was the fix for fuzzer bug #784 'Header VRF Verification Failure on some cases' (PR #791). For the first block of a new epoch, why can the seal H_S, the entropy source H_V and the epoch marker H_E only be checked in the second phase?",
 "code": {"lang": "go", "caption": "internal/stf/sft.go (RunSTF) + validate_header.go (ValidateHeaderVrf)", "src": """// Validate Non-VRF Header(H_E, H_W, H_O, H_I)
// For non-genesis blocks, validate the header
if header.Parent != (types.HeaderHash{}) {
    err = ValidateNonVRFHeader(header, &priorState, extrinsic)
    ...
}
...
// Update Safrole
err = UpdateSafrole()
...
postState := cs.GetPosteriorStates().GetState()

// After keyRotate
err = ValidateHeaderVrf(header, &priorState, &postState)
...
func ValidateHeaderVrf(header types.Header, priorState *types.State, posteriorState *types.State) error {
    if err := safrole.ValidateHeaderEpochMark(header, priorState, posteriorState); err != nil {
        return err
    }
    if err := safrole.ValidateHeaderSeal(header, posteriorState); err != nil {
        return err
    }
    if err := safrole.ValidateHeaderEntropy(header, posteriorState); err != nil {
        return err
    }
    return nil
}"""},
 "options": [
  "Because the seal signs E_U(H), which embeds H_E and H_W, so those markers must be finalized first; the validator set itself is irrelevant, since κ′ = κ whenever the block is valid and the seal context η′_3 equals η_3 in every block",
  "Because all three depend on this block's own rotation: H_S is checked against γ′_S[H_T mod E] with H_A = κ′[H_I]_b and context η′_3, H_V against the same H_A, and H_E against γ′_P = Φ(ι); the prior κ/η/γ_S pass mid-epoch but fail at epoch boundaries",
  "Only for performance: ring-VRF verification is slow, so it is deferred until the cheap checks have passed; verifying against the prior state would give identical results in every block because κ, η and γ_S are stable within a block",
  "Because H_E must be compared with the posterior entropy η′_0, η′_1, which only exist after UpdateEtaPrime0; the seal itself could safely be verified against the prior state, since H_A = κ[H_I]_b by definition"
 ],
 "answer": 1,
 "optNotes": [
  "「κ′ = κ whenever valid」在 e′ > e 就不成立，η′_3 也只有 epoch 中段才等於 η_3。",
  "三者的比對對象 γ′_S、κ′、η′_3、γ′_P 全是本塊自己的 rotation 產物，只能在 UpdateSafrole 之後驗。",
  "效能不是理由，而且 seal 是 IETF VRF、不是昂貴的 ring VRF。",
  "H_E 比對的是 **prior** η_0、η_1；且 §5 eq. 5.10 明寫 H_A ≡ κ′[H_I]_b，用的是 posterior。",
 ],
 "explanation": "eq. 6.16/6.17：i = γ′_S[H_T mod E]（posterior 序列），H_S 由 H_A 簽、context 用 η′_3；§5 eq. 5.10：H_A ≡ κ′[H_I]_b（posterior active set）；eq. 6.18：H_V 同樣由 H_A 驗；eq. 6.28：H_E 的 key 列表是 γ′_P = Φ(ι)，但其兩個 entropy 欄位比對的是 prior η_0、η_1（ValidateHeaderEpochMark 用 priorState.Eta[0]/[1]）。這些 posterior 值在 epoch 第一塊全由該塊自己的 KeyRotate（κ′ = γ_P）、UpdateEntropy（η′_3 = η_2）、UpdateSlotKeySequence 產生，所以 seal/entropy/epoch-mark 只能在 UpdateSafrole 之後驗；epoch 中段 κ′ = κ、η′_3 = η_3、γ′_S = γ_S，用 prior state 也會過——這正是 #784「on some cases」只在 epoch 邊界失敗的原因（trace 1758621879/00000348 被誤判為 error 7 VrfSealInvalid），PR #791 改成傳 posterior Kappa & Eta。H_W、H_O、H_X、H_R、H_I 只依賴 prior state 與 extrinsic，所以留在 ValidateNonVRFHeader（reviewer yu2C 堅持不要整個搬到 safrole 之後），其中 H_I 的 range check 必須最早做（#825）。順帶一提 sft.go 的註解「(H_E, H_W, H_O, H_I)」已過時——H_E 實際在 ValidateHeaderVrf 裡驗。",
 "trap": "口訣：seal、H_V 看 posterior（γ′_S、κ′、η′_3）；H_E 看 prior η_0/η_1 + posterior γ′_P；H_W/H_O/H_I 只看 prior + extrinsic。"
},
{
 "id": "ch06-code-author-index-bound",
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "§5 eq. 5.10 (H_I ∈ N_{|κ′|}), eq. 6.7–6.8, 6.14 — internal/stf/validate_header.go ValidateNonVRFHeader",
 "difficulty": 3, "kind": "code", "tags": ["safrole", "validators", "code", "fuzzer", "delta-0.8.0"],
 "stem": "After fuzzer bug #825 (panic 'index out of range [65535] with length 6' while computing η′_0), the team added this check to ValidateNonVRFHeader, which runs BEFORE UpdateSafrole. Which assessment is right under GP 0.8.0?",
 "code": {"lang": "go", "caption": "internal/stf/validate_header.go (ValidateNonVRFHeader)", "src": """// Validate author_index out of range.
// NOTE: There is currently no official error code defined for this case.
// We may need to update this once the spec updates.
if header.AuthorIndex >= types.ValidatorIndex(len(priorState.Kappa)) {
    errCode := SafroleErrorCode.AuthorIndexOutOfRange
    return &errCode
}"""},
 "options": [
  "The check is exactly what the GP specifies: eq. 5.10 bounds H_I by |κ|, the prior active set, which is precisely why it can be verified before key rotation without loss of generality, and it therefore covers the fuzzer's 65535 case at any validator-set size",
  "The check is unnecessary: an out-of-range H_I already fails the seal signature check and is reported as VrfSealInvalid, so the fuzzer's expected rejection is produced anyway; the real fix for #825 belonged inside UpdateEtaPrime0, where the panic was raised",
  "The GP bound is |κ′| (posterior), not |κ|; the check is equivalent today only because every key sequence here has exactly V entries (offenders are zeroed in place, #1037) — once a 0.8.0 set-size change makes |γ_P| ≠ |κ|, a bound taken from the prior κ is wrong at the boundary",
  "The bound should be |ι|, since at an epoch boundary the block author is drawn from the staging set that eq. 6.14 has just promoted into κ′; bounding by either the prior or the posterior κ would reject every author from the incoming set on the first block"
 ],
 "answer": 2,
 "optNotes": [
  "eq. 5.10 寫的是 H_I ∈ N_{|κ′|}——邊界取的是 posterior κ′ 的長度，不是 prior κ。",
  "根本走不到簽章驗證：索引 κ′[H_I] 時就先 panic，修法塞進 UpdateEtaPrime0 也治標不治本。",
  "今天 |κ| = |κ′| 只因序列永遠是 V 筆；0.8.0 允許長度變動後，κ′ = γ_P 在邊界就會不同長。",
  "eq. 6.14 在邊界把 ι 推進的是 γ′_P，κ′ 取的是舊 γ_P——ι 還要再過一個邊界才成為 κ。",
 ],
 "explanation": "§5 eq. 5.10：H_I ∈ N_{|κ′|}、H_A ≡ κ′[H_I]_b——邊界是 **posterior** κ′ 的長度。#825 的 panic（index out of range [65535] with length 6）就是 H_I 在 range check 之前被拿去索引 validator 陣列；Go 直接 panic 而不是回傳錯誤，fuzzer 視為 target crash。這段檢查放在 ValidateNonVRFHeader（UpdateSafrole 之前），手上只有 prior state，於是用 len(priorState.Kappa)；今天這是等價的，因為 codebase 裡 ι/γ_P/κ/λ 永遠都是 V 筆（offender 只被 Φ 歸零、不移除，#1037），|κ| = |κ′|。但 GP 0.8.0 eq. 6.7/6.8（PR #514）允許每個序列長度各自 ∈ N_V = {6, 9, …, 1023}，designate host call 也只要求 z ∈ N_V；當 |γ_P| ≠ |κ| 時，epoch 第一塊的 κ′ = γ_P（eq. 6.14）長度會變（eq. 11.18 也因此在 |κ| ≠ |κ′| 時清空 ρ‡），正確做法是先算出 κ′ 的長度（e′ > e 時取 |γ_P|，否則 |κ|）再檢查。錯誤碼方面 GP 與官方 enum 沒有對應值，你們暫用 AuthorIndexOutOfRange (13)。",
 "trap": "面試官可能追問：H_I 越界時你們回什麼？答：沒有官方 code，自訂 13；重點是必須在任何 κ′[H_I] 之前檢查，否則 panic。"
},
{
 "id": "ch06-skip-epochs-transition",
 "ch": "6", "section": "6.3–6.7 (epoch transition across skipped epochs)", "gpRef": "eq. 6.2, 6.14, 6.24, 6.25, 6.28–6.29, 6.35",
 "difficulty": 3, "kind": "concept", "tags": ["safrole", "epoch", "entropy", "fallback", "markers", "calc"],
 "stem": "Full parameters (E = 600, Y = 500). The prior block has τ = 1195 and a saturated accumulator (|γ_A| = E); the next block has H_T = 1810 (nothing was authored in between). Expressing posterior values in terms of PRIOR ones, which description of this transition is correct?",
 "options": [
  "Rotation is applied once per elapsed epoch, i.e. twice here: κ′ = Φ(ι), λ′ = γ_P, (η′_1, η′_2, η′_3) = (η′_0, η_0, η_1); γ′_S = F(η_0, Φ(ι)); H_E is present and H_W absent",
  "Rotation happens exactly once: κ′ = γ_P, λ′ = κ, γ′_P = Φ(ι), (η′_1, η′_2, η′_3) = (η_0, η_1, η_2); γ′_S = F(η_1, γ_P) despite m = 595 ≥ Y and a full γ_A; H_E is present, H_W absent; γ′_A is rebuilt from this block's E_T alone",
  "γ′_S = Z(γ_A) because the prior block sat in the tail (m = 595 ≥ Y) with a saturated accumulator; keys and entropy rotate once; H_W = Z(γ_A) is emitted as well since this block closes the contest",
  "The block is rejected with BadSlot: eq. 6.25 has no case for e′ = e + 2, so a chain may skip individual slots but never an entire epoch; the next valid H_T is therefore some slot of epoch 2, and only from there can epoch 3 be reached"
 ],
 "answer": 1,
 "optNotes": [
  "6.14 與 6.24 的條件是布林的 e′ > e，與 e′ − e 差幾格無關，state 只記得最後一塊。",
  "一次 rotation 加 fallback：e′ = e + 2 讓 6.25 第一種情況失效，H_W 需要 e′ = e 也不會出現。",
  "6.25 的第一種情況要求 e′ = e + 1（精確相等）；本題 e′ = e + 2，累積的 ticket 一律作廢。",
  "BadSlot 只在 τ′ ≤ τ 時觸發；跳過任意多個 slot 甚至整個 epoch 都是合法的。",
 ],
 "explanation": "計算：e ⌢ m = 1195/600 → e = 1、m = 595；e′ ⌢ m′ = 1810/600 → e′ = 3、m′ = 10（eq. 6.2）。eq. 6.14 與 6.24 的條件都是布林的 e′ > e，與 e′ − e 無關，所以 key 與 entropy **只 rotate 一次**：κ′ = γ_P、λ′ = κ、γ′_P = Φ(ι)、(η′_1, η′_2, η′_3) = (η_0, η_1, η_2)——state 只記得最後一塊，沒有「中間 epoch」可言。eq. 6.25 第一種情況要求 e′ = e + 1，這裡不成立，即使 m = 595 ≥ Y 且 |γ_A| = E 也走 F(η′_2, κ′) = F(η_1, γ_P)（vector skip_epochs-1：「Progress skipping epochs with a full tickets accumulator. Tickets mark is not generated. Accumulated tickets discarded. Fallback method enacted」）。eq. 6.28：e′ > e → H_E = (η_0, η_1, γ′_P 的 (k_b, k_e))；eq. 6.29：H_W 需要 e′ = e → ∅。eq. 6.35：e′ > e → γ′_A 只由本塊的 n 組成（m′ = 10 < Y，可帶最多 K 張、對新的 γ′_Z 與 context X_T ⌢ η_1 驗）。本塊 seal 走 fallback：H_A = γ′_S[10]、context X_F ⌢ η′_3 = X_F ⌢ η_2、T = 0。你們的程式：UpdateEntropy/KeyRotate 用 `ePrime > e`，UpdateSlotKeySequence 用 `ePrime == e+1`，正好對應。",
 "trap": "跳 N 個 epoch ≠ rotate N 次；6.25 要的是 e′ = e + 1（精確），6.14/6.24 要的是 e′ > e（任意）。"
},
{
 "id": "ch06-variable-set-boundary",
 "ch": "6", "section": "6.3 Key Rotation / 6.7 The Extrinsic and Tickets", "gpRef": "eq. 6.7–6.8, 6.14, 6.28, 6.30; §5 eq. 5.10",
 "difficulty": 3, "kind": "delta", "tags": ["safrole", "validators", "tickets", "delta-0.8.0", "calc"],
 "stem": "Tiny parameters (E = 12). During epoch e the delegator service set the staging set ι to 9 validators while γ_P and κ still hold 6 — a legal 0.8.0 configuration (eq. 6.8). Consider the first block of epoch e + 1. Which statement is correct?",
 "options": [
  "n = ⌈24/6⌉ = 4, because n is computed from the active set κ′ that seals this epoch; γ′_Z stays a 6-key ring and H_E lists 6 pairs until the 9 validators actually become active in epoch e + 2",
  "n = ⌊24/9⌋ = 2, and the seal must now come from one of the 9 incoming validators (H_I < 9), because γ′_Z commits to their keys from this block on and H_E lists their 9 pairs",
  "Tickets submitted during epoch e + 1 need entry index < n = ⌈24/9⌉ = 3 and ring proofs against a 9-key γ′_Z; H_E lists 9 (k_b, k_e) pairs; but the block's H_I must be < 6 and its seal comes from κ′ = the old 6-member γ_P",
  "The block is invalid: eq. 6.8 requires |ι| = |κ| at all times, so the validator count can only be changed by restarting from genesis with a new chainspec; designate would have returned HUH for z = 9"
 ],
 "answer": 2,
 "optNotes": [
  "分母是 γ′_P 不是 κ′；γ′_Z 與 H_E 在這一塊就已換成 9 人（eq. 6.14 的 z 對 γ′_P 取）。",
  "n 用的是 ceiling 不是 floor（⌈24/9⌉ = 3）；而且本 epoch 出塊的仍是 κ′ 這 6 個人。",
  "ticket 規則跟著 γ′_P（9 人）走，seal 與 H_I 跟著 κ′（舊的 6 人 γ_P）走，兩者在這塊分家。",
  "eq. 6.7/6.8 沒有要求四個序列彼此等長；designate 只檢查 z ∈ N_V，11.18 更明文處理 |κ| ≠ |κ′|。",
 ],
 "explanation": "eq. 6.14：e′ > e 時 γ′_P = Φ(ι)（9 筆）、κ′ = γ_P（6 筆）、λ′ = κ、z = O([k_b | k ∈ γ′_P])——ring 有 9 個成員。eq. 6.30：n = ⌈2E/|γ′_P|⌉ = ⌈24/9⌉ = ⌈2.67⌉ = 3，entry index ∈ N_3 = {0, 1, 2}。eq. 6.28：H_E 列出 γ′_P 的 9 組 (k_b, k_e)。但本 epoch 出塊的是 κ′（舊的 6 人 γ_P）：§5 eq. 5.10 H_I ∈ N_{|κ′|} = N_6，seal 由 κ′[H_I]_b 簽（6.16/6.17），fallback F(η′_2, κ′) 的索引 mod 6；9 位新 validator 要到 epoch e + 2 才成為 κ。eq. 6.7/6.8（0.8.0 PR #514「Support smaller validator sets」）：ι、γ_P、κ、λ 各自 ∈ [K]_{N_V}、N_V = {3c | c ∈ N_{2..C+1}}。連帶影響：active core 數 = |κ′|/3，本 epoch 2 個、下個 epoch 3 個。你們的 code 目前撐不住這種鏈：GetVerifier 要求 len(gammaK) == ValidatorsCount，ValidateHeaderEpochMark 要求 len(em.Validators) == ValidatorsCount，兩者都會拒絕合法區塊——這就是 open issue #1037。",
 "trap": "一句話：ticket 規則跟著 γ′_P（下個 epoch 的人），seal/author 規則跟著 κ′（這個 epoch 的人）。"
},
{
 "id": "ch06-ring-root-nulled-keys",
 "ch": "6", "section": "6.3 Key Rotation / Appendix G", "gpRef": "eq. 6.14–6.15, G.3 (ring root), App. G padding-point note",
 "difficulty": 3, "kind": "concept", "tags": ["safrole", "ring-vrf", "offenders", "validators"],
 "stem": "On an epoch change, one validator in ι has its Ed25519 key in ψ′_O, so Φ replaces its entire 336-octet entry with zeros. How does this affect γ′_Z and ticket verification in the new epoch?",
 "options": [
  "The offender's slot is removed from the ring, so γ′_Z commits to |γ′_P| − 1 keys and everyone's ring position shifts by one; this is why the accumulator has to be re-sorted at the epoch boundary and why H_E lists the surviving keys only",
  "The ring keeps |γ′_P| members: a zero key decodes to no Bandersnatch point, so the padding point is substituted at that position in z = O([k_b | k ∈ γ′_P]); the offender cannot produce a valid ring proof, everyone else's tickets verify against this γ′_Z all epoch",
  "The all-zero key is a valid Bandersnatch point (the identity), so γ′_Z is computed normally and the offender can keep submitting tickets until the following epoch removes it; only its Ed25519-signed artefacts are refused meanwhile",
  "O(…) fails on an undecodable key, so a block that would place a nulled key into γ′_P is invalid; offenders therefore have to be removed from ι by the delegator service (designate) before the boundary, shrinking the set by 3 each time"
 ],
 "answer": 1,
 "optNotes": [
  "ring 的大小與每個人的位置都不變：eq. 6.14 的 z 仍對全部 |γ′_P| 個位置取 commitment。",
  "App. G 明文：無對應 Bandersnatch point 時該位置改用 padding point，ring 大小維持不變。",
  "全零 32 bytes 不是合法點：Twisted Edwards 的 identity 是 (0, 1)，壓縮編碼不是全零。",
  "vector enact-epoch-change-with-padding-1 正是把兩把無效 key 換成 padding point，而非拒絕區塊。",
 ],
 "explanation": "eq. 6.15：Φ 把 k_e ∈ ψ′_O 的整組 key 換成 [0, 0, …]；eq. 6.14：z = O([k_b | k ∈ γ′_P]) 仍對 **全部** |γ′_P| 個位置取 commitment。App. G 明文：「in the case a key has no corresponding Bandersnatch point when constructing the ring, then the Bandersnatch padding point … should be substituted」。w3f vector enact-epoch-change-with-padding-1 就是測這個：一把 key 因在 posterior offenders 而歸零、另一把本來就 undecodable，「Both the invalid keys are replaced with the padding point during ring commitment computation」。offender 沒有 padding point 的私鑰，做不出合法 ring proof，整個 epoch 都無法投 ticket。注意 Φ 只作用在進入 γ′_P 的 ι——已在 κ′ 裡的 offender 本 epoch 的 seal 仍照常驗（§11 eq. 11.22 的 guarantor 分配才另外套 Φ(κ′)）；而歸零的 entry 下個 epoch 進到 κ 後，fallback F 若抽到它，那個 slot 就沒人能出塊。工程面：γ′_Z ∈ B_144（G.3）是 key 序列的純函數，只在 e′ > e 時重算（KeyRotate 否則直接沿用 prior γ_Z）；你們的 GetVerifier 以 Blake2b(所有 Bandersnatch key 串接) 當快取鍵（#1041），取代原本按 epoch 快取、fork-restore 就得重建的做法（#1040）。",
 "trap": "零 key ≠ 移除：ring 成員數不變、位置不變，只是那格換成 padding point。"
},
{
 "id": "ch06-vrf-output-message-independence",
 "ch": "6", "section": "6.4 Sealing and Entropy Accumulation", "gpRef": "eq. 6.16, 6.24, 6.30, 6.32; §3.8.2 Signing Schemes; App. G eq. G.2/G.5",
 "difficulty": 3, "kind": "rationale", "tags": ["safrole", "vrf", "seal", "tickets", "rationale"],
 "stem": "A ticket proof is a ring-VRF proof with context X_T ⌢ η′_2 ++ r over the EMPTY message, while the seal H_S is a plain Bandersnatch signature with context X_T ⌢ η′_3 ++ i_e over E_U(H), the whole unsigned header. Why can eq. 6.16 nevertheless demand i_y = Y(H_S), i.e. that the seal's VRF output equal the ticket id?",
 "options": [
  "Because a VRF output depends only on the secret key and the context ('influenced by x but not by m'), and by seal time the submission entropy has rotated from η′_2 into η′_3 so the contexts coincide: the same key reproduces the ticket id under any message — anonymous in the ring proof, attributable in the seal",
  "Because the ticket id is defined as the Blake2b hash of the proof bytes, and eq. 6.16 requires the seal to embed a copy of the original 784-byte ring proof so that every verifier can recompute that hash from the header alone; the E_U(H) message merely binds the embedded copy to this particular block",
  "Because both the ticket proof and the seal are in fact signed over the empty message — E_U(H) is only ever the message of H_V, whose output feeds η′_0 — so the two VRF outputs agree trivially; the identity check i_y = Y(H_S) is accordingly made against H_V rather than against the seal",
  "Because η′_2 = η′_3 whenever the tickets were submitted in the same epoch as the block being sealed, so the author simply re-signs an identical context; the message is ignored by the verifier for seals though not for ring proofs, which is why tickets carry [] and seals carry E_U(H)"
 ],
 "answer": 0,
 "optNotes": [
  "VRF output 只看 (key, context)；6.24 的 rotate 讓提票時的 η′_2 到封章時正好變成 η′_3。",
  "6.32 取的是 VRF **輸出**而非 proof bytes 的 hash；seal 是 96-byte 簽章，不含 784-byte ring proof。",
  "seal 的訊息就是 E_U(H)（這才把它綁到 header）；i_y 比對的對象是 H_S 而不是 H_V。",
  "η′_2 與 η′_3 差一個 epoch；訊息也仍然參與簽章驗證，只是不影響 VRF output。",
 ],
 "explanation": "§3.8.2：Bandersnatch signature 與 RingVRF proof「both define a VRF output, a high entropy hash influenced by x but not by m」，且「the member is identified in the former and is anonymous in the latter」；App. G（G.2/G.5）：Y(·) 取 output 的前 32 bytes。eq. 6.32：ticket id y = Y(p)；eq. 6.30 的 context 是 X_T ⌢ η′_2 ++ r（提交當時的 η′_2）；eq. 6.24 在下個 epoch 邊界把它 rotate 成 η′_3，所以 eq. 6.16 seal 的 context X_T ⌢ η′_3 ++ i_e 與當初提票的 context 逐 byte 相同。同一把 secret key 加上相同 context ⇒ 相同 VRF output，無論訊息是 [] 還是 E_U(H)，因此驗證者比對 i_y = Y(H_S) 就能確定「出塊者就是持票人」——提票時 ring proof 只證明「γ′_P 某成員」，出塊時 IETF 簽章（H_A 已知）揭露身分；這就是 Safrole「事前匿名、事後可歸屬」的核心。§6.7 也說 ticket id「is used both as a score in the contest and as input for the block's entropy source VRF signature」（即 H_V 的 context X_E ⌢ Y(H_S)）。你們 ValidateByTickets 先比 vrf.VRFIetfOutput(header.Seal) == ticket.ID，再 IETFVerify(context, E_U(H))。",
 "trap": "VRF output 只看 (key, context)，不看 message——這是 ticket 能匿名提交、之後又能對上 seal 的原因。"
},
{
 "id": "ch06-why-m-ge-Y",
 "ch": "6", "section": "6.5 The Slot-Sealer Sequence", "gpRef": "eq. 6.25, 6.29, 6.31, 6.35; §6.6–6.7 prose",
 "difficulty": 3, "kind": "rationale", "tags": ["safrole", "fallback", "markers", "rationale"],
 "stem": "Eq. 6.25 uses the accumulator as the next slot-sealer sequence only when e′ = e + 1 ∧ m ≥ Y ∧ |γ_A| = E. What does the conjunct m ≥ Y — a property of the PRIOR block — actually guarantee, and why does the GP tie the ticket regime to it?",
 "options": [
  "That at least Y tickets were submitted during the epoch, so the contest was competitive enough for the accumulator to be trusted over the fallback keys; with fewer than Y entries the outside-in ordering Z would leave slots unassigned",
  "That no ticket submitted inside the tail is counted: tickets arriving at m ≥ Y would otherwise have been proven against the wrong ring root and entropy, since γ′_Z and η′_2 already refer to the epoch after next by then",
  "That some block of the ending epoch was authored in the tail, which — γ_A being frozen once m′ ≥ Y — is exactly the condition under which H_W = Z(γ_A) was published in that epoch, so a header-only node is never asked to verify ticket seals for a sequence it never saw",
  "That the prior block's author held a ticket (T = 1), since a fallback-sealed block is not allowed to close a contest on behalf of the ticket holders; this is also what the best-chain rule of §19 counts when it prefers ticketed ancestors"
 ],
 "answer": 2,
 "optNotes": [
  "Y = 500 是 slot phase，與「提交了幾張 ticket」無關；飽和由 |γ_A| = E 這個 conjunct 負責。",
  "tail 內本來就不可能有 ticket（6.31 要求 |E_T| = 0），沒有「算錯 ring root」的餘地。",
  "m ≥ Y 等價於「本 epoch 已有某塊發佈過 H_W」，header-only 節點才不會驗到沒見過的序列。",
  "T 旗標不是 6.25 的輸入，它只用在 §19 best-chain 對 ticket-sealed 祖先的偏好上。",
 ],
 "explanation": "eq. 6.31：m′ ≥ Y 時 |E_T| = 0，§6.7 末尾更指出此時 γ′_A = γ_A——進入 tail 後 accumulator 凍結。eq. 6.29：同一 epoch 內第一個跨過 Y 的區塊（m < Y ≤ m′）若 |γ_A| = E 就發佈 H_W = Z(γ_A)。把兩者合起來：「前一塊在 tail（m ≥ Y）且 |γ_A| = E」⟺「本 epoch 已有某塊發佈了 H_W，且內容恰是 Z(γ_A)」（tail 內任何一塊都是或晚於那個第一塊，而 γ_A 從那之後不再變動）。§6.6 說 marker 的目的就是讓「nodes which do not synchronize the entire state」能「using only the chain of headers」追蹤 sealer/validator 的變化，§6.7 也說 Y 之後「the following epoch's slot-sealer sequence becomes fixed」。若沒有任何區塊落在 tail（前一塊 m < Y 直接跳到下個 epoch），H_W 從未出現，header-only 節點無從得知 ticket 序列，所以 GP 寧可走 fallback（vector skip_epoch_tail-1：「Tickets mark has no chance to be generated. Accumulated tickets discarded. Fallback method enacted」）。你們的 #284 就是最初只判 ePrime == e+1，會在沒有 H_W 的情況下啟用 ticket（也會在跳過 epoch 時用錯 accumulator）。",
 "trap": "m ≥ Y 不是「比賽夠久」，而是「H_W 一定已經在 header 鏈上」——三個 conjunct 各管一件事：e′ = e+1（是下一個 epoch）、m ≥ Y（H_W 已發佈）、|γ_A| = E（飽和）。"
},
{
 "id": "ch06-three-keys-epoch-marker",
 "ch": "6", "section": "6.3 Key Rotation / 6.6 The Markers", "gpRef": "eq. 6.10–6.13, 6.15, 6.28; §5 eq. 5.11; eq. 11.14, 11.28, 17.7, 18.1",
 "difficulty": 2, "kind": "concept", "tags": ["safrole", "validators", "markers", "keys"],
 "stem": "Each validator key K bundles a Bandersnatch, an Ed25519 and a BLS public key. Which mapping of key → protocol use is correct, and why has the epoch marker H_E carried the Ed25519 keys alongside the Bandersnatch keys since GP 0.6.4?",
 "options": [
  "Bandersnatch: seals, H_V and BEEFY; Ed25519: ticket ring proofs, guarantees, assurances and audit announcements; BLS: judgments, culprits, faults and offender identity (ψ_O, H_O, Φ). H_E carries Ed25519 keys because the ring root γ′_Z is a commitment to the Ed25519 keys of γ′_P, which header-only nodes must be able to rebuild for themselves",
  "Bandersnatch: ticket ring proofs, H_S, H_V, audit-selection VRFs; Ed25519: guarantees, assurances, judgments/culprits/faults, audit announcements, offender identity (ψ_O, H_O, Φ); BLS: BEEFY only. H_E carries Ed25519 keys so a header-only node can attribute every Ed25519-signed artefact and every H_O entry to a validator",
  "Bandersnatch: ticket ring proofs, seals and H_V; Ed25519: everything else, including BEEFY signatures and audit announcements; BLS is reserved metadata with no protocol use yet, exactly like k_m. H_E carries Ed25519 keys so that GRANDPA voters can be weighted by stake using nothing but the header chain",
  "Bandersnatch: ticket ring proofs, seals, H_V and audit-selection VRFs; Ed25519: guarantees and assurances only; BLS: judgments, culprits, faults and BEEFY. H_E carries Ed25519 keys because Φ needs them to null the offenders inside κ′ at the epoch boundary, and κ′ is not otherwise reconstructible from headers"
 ],
 "answer": 1,
 "optNotes": [
  "ticket 是 Bandersnatch ring proof、BEEFY 用 BLS；ψ_O 是 Ed25519 key 集合，γ′_Z 也是對 k_b 取的。",
  "三把 key 的分工與 H_E 的動機都對：header-only 節點要能把 Ed25519 簽章與 H_O 對應到 validator。",
  "BEEFY（18.1）用 κ′[v]_bls，BLS 並非未用的保留欄位；GP 也沒有「以 stake 加權 GRANDPA」。",
  "judgments/culprits/faults 都直接帶 Ed25519 key 與簽章；Φ 作用在 ι → γ′_P、讀的是 state 而非 header。",
 ],
 "explanation": "eq. 6.10–6.13：k_b Bandersnatch、k_e Ed25519、k_l BLS（144 bytes）、k_m metadata（opaque，不參與任何密碼學）。Bandersnatch：ticket ring proof（6.30，對 γ′_Z）、seal H_S（6.16/6.17）、entropy VRF H_V（6.18）、§17 auditing 的 VRF seed（s_0、s_n 用 κ[v]_b）。Ed25519：guarantee credentials（11.28）、assurances（11.14，κ[a]_e）、verdict 中的 judgments（§10 用 k[i]_e，k 取自 κ 或 λ）、culprits/faults（10.2 的 tuple 直接帶 Ed25519 key 與簽章）、audit announcements（17.7）、以及 offender 身分——ψ_O 是 Ed25519 key 的集合，H_O ∈ [H_E]（5.11），Φ 用 k_e ∈ ψ′_O 判斷（6.15）。BLS：只有 BEEFY（18.1，κ′[v]_bls 對 accumulation-output MMR 的 Keccak 簽章）。eq. 6.28：H_E = (η_0, η_1, [(k_b, k_e) | k ∈ γ′_P])；§6.6：marker 是給「do not synchronize the entire state」的節點用 header 鏈追蹤 validator 變化——只有 Bandersnatch 的話，這種節點能驗 seal，卻無法把 guarantee/assurance/judgment/announcement 或 H_O 裡的 Ed25519 key 對應到 validator，因此 0.6.4 把 Ed25519 key 加進 H_E（changelog：「Ed25519 keys in epoch marker」）；BLS 與 metadata 不在 H_E 內。你們的 EpochMarkValidatorKeys 就是 {Bandersnatch, Ed25519} 兩欄，ValidateHeaderEpochMark 兩者都比。",
 "trap": "口訣：Bandersnatch = Safrole（票、seal、entropy、audit 抽籤）；Ed25519 = 其他所有簽章與 offender 身分；BLS = 只有 BEEFY。"
},
]
