# -*- coding: utf-8 -*-
# Batch 2 — Chapter 10 (Disputes) and Chapter 11 (Reporting and Assurance), GP 0.8.0.
# New angles only; see items/ch10_disputes.py and items/ch11_reporting.py for the first batch.
ITEMS = [
{
 "id": "ch10-verdict-keyset-epoch-boundary",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.2–10.4",
 "difficulty": 3, "kind": "concept", "tags": ["disputes", "calc", "tiny", "epoch-boundary"],
 "stem": "Tiny config (E = 12). A block with H_T = 24 — the first block of epoch 2 — is imported on top of a parent whose τ = 23, and its E_D contains verdicts. Per eq. 10.2–10.4, which epoch indices a may those verdicts carry, and which validator set K(a) verifies each of them?",
 "options": [
  "a ∈ {1, 0}: a = 1 selects the prior κ (the set active during epoch 1) and a = 0 the prior λ; a = 2 is rejected even though the block itself belongs to epoch 2",
  "a ∈ {2, 1}: a = 2 selects κ′ (the set this block rotates in) and a = 1 selects κ, because the index is derived from the block's own timeslot H_T; a = 0 is rejected since λ is two epochs stale by now",
  "a ∈ {2, 1}: a = 2 selects the prior κ and a = 1 the prior λ, since ⌊H_T/E⌋ = 2 is the epoch index a verdict must name; a = 0 is rejected as too old",
  "a ∈ {2, 1, 0}: in an epoch-boundary block judgments from κ′, κ and λ are all admissible, each verdict still needing ⌊2|k|/3⌋+1 = 5 signatures"
 ],
 "answer": 0,
 "optNotes": [
  "τ = 23 → ⌊23/12⌋ = 1，所以 a ∈ {1, 0}；K(a) 取的正是 prior 的 κ 與 λ。",
  "epoch index 綁的是父塊的 τ 而不是本塊 H_T；κ′ 這批新 validator 本塊還不能簽 verdict。",
  "同樣拿 H_T 推 a：⌊H_T/E⌋ = 2 不是 verdict 該帶的 index，型別綁的是 ⌊τ/E⌋。",
  "K 只有兩個 case，a = 2 既 ≠ ⌊τ/E⌋ 也 ≠ ⌊τ/E⌋ − 1 → 區塊直接無效。",
 ],
 "explanation": "eq. 10.2 的 verdict 第二項型別是 ⌊τ/E⌋ − N_2，即 {⌊τ/E⌋, ⌊τ/E⌋ − 1}，而 τ 是 **prior state 的 timeslot**（GP 原文：「must be either the epoch index of the prior state or one less」）。eq. 10.3：K(a) = κ 當 a = ⌊τ/E⌋，否則 λ——這裡的 κ、λ 都是 prior state 的集合。計算：τ = 23 → ⌊23/12⌋ = 1。本塊雖然 H_T = 24 屬於 epoch 2、且會做 key rotation（κ′ = γ_P、λ′ = κ，eq. 6.14），但 disputes 用的是 prior 集合，γ_P 這批新 validator 在本塊還不能簽 verdict；要到下一塊（τ = 24：a = 2 → κ = 新集合，a = 1 → λ = 舊 κ）才行。eq. 10.4 另要求每個 verdict 恰好 ⌊2|k|/3⌋+1 = 5（tiny）個 judgment。你們 VerifySignature：`a := U32(state.GetTau()) / U32(EpochLength)`，state 取自 `GetPriorStates()`，與 GP 一致。",
 "trap": "口訣：verdict 的 a 看「父塊的 τ」，K(a) 取「prior κ/λ」；換 epoch 那一塊，新集合還簽不了 verdict。"
},
{
 "id": "ch10-code-genesis-age-underflow",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.2–10.3 — internal/extrinsic/verdict_controller.go VerifySignature",
 "difficulty": 3, "kind": "code", "tags": ["disputes", "code", "fuzzer", "edge-case"],
 "stem": "The chain is still in its genesis epoch (prior τ < E, so ⌊τ/E⌋ = 0). Which verdict `Age` does this code accept although GP 0.8.0 (eq. 10.2–10.3) makes the block invalid — and against which key set would it then verify the judgments?",
 "code": {"lang": "go", "caption": "internal/extrinsic/verdict_controller.go (VerdictWrapper.VerifySignature)", "src": """func (v *VerdictWrapper) VerifySignature() error {

    state := blockchain.GetInstance().GetPriorStates()

    a := types.U32(state.GetTau()) / types.U32(types.EpochLength)
    if v.Verdict.Age != a && v.Verdict.Age != a-1 {
        return errors.New("bad_judgement_age")
    }

    k := make(types.ValidatorsData, types.ValidatorsCount)
    if v.Verdict.Age == a {
        k = state.GetKappa()
    } else {
        k = state.GetLambda()
    }"""},
 "options": [
  "Age = 1: because the check compares Age against both a and a−1 symmetrically, the next epoch's index also passes and the judgments are verified against κ as if the epoch had already rolled over",
  "Age = 0 with judgments signed by λ keys: since a−1 cannot be matched at genesis, the code falls through to the λ branch and accepts λ signatures for the current epoch",
  "Age = 2^32 − 1: `a-1` wraps around in U32, so the age check passes and the judgments are verified against λ, whereas ⌊τ/E⌋ − N_2 has no previous epoch at epoch 0",
  "None: the wrapped value of `a-1` can never equal a decoded 32-bit Age, so at genesis only Age = 0 passes and the code is exactly the GP rule"
 ],
 "answer": 2,
 "optNotes": [
  "Age = 1 既不等於 a = 0 也不等於 wrap 後的 0xFFFFFFFF，這個輸入照樣會被擋下。",
  "Age = 0 走的是 `Age == a` 分支 → 用 κ 驗簽，不會落到 λ。",
  "a 宣告成 U32，a = 0 時 a-1 wrap 成 4294967295，而 Age 以 E_4 編碼，fuzzer 做得出這個值。",
  "U32 之間的比較就是會相等，wrap 後的值完全可能命中解碼出來的 Age。",
 ],
 "explanation": "eq. 10.2：a ∈ ⌊τ/E⌋ − N_2 = {⌊τ/E⌋, ⌊τ/E⌋ − 1}；eq. 10.3：K(a) = κ 當 a = ⌊τ/E⌋，否則 λ。在 genesis epoch，⌊τ/E⌋ = 0，「前一個 epoch」的 index 是 −1，不是自然數，所以唯一合法的 a 是 0；序列化上 a 是 E_4（附錄 C 的 E_D 編碼：(r, E_4(a), var[j])）。後果：這樣的區塊會通過 age 檢查並改用 λ 驗簽，若簽章確實由 λ 的 key 產生（genesis 時 λ 通常等於 κ），你們會接受一個 reference implementation 會拒絕的區塊 → state root 分歧。這正是 #1042 整合 PR 補的「genesis-epoch guard」。",
 "trap": "用 unsigned 減 1 之前先想 a = 0；GP 的 ⌊τ/E⌋ − N_2 沒有負數，也沒有 2^32 − 1。"
},
{
 "id": "ch10-code-fault-equivalence-wonky",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.7 — internal/extrinsic/fault_controller.go VerifyReportHashValidty",
 "difficulty": 3, "kind": "code", "tags": ["disputes", "code", "faults", "edge-case"],
 "stem": "In this block a verdict classifies report r as wonky (exactly ⌊|k|/3⌋ positive judgments), so r ∈ ψ′_W and r ∉ ψ′_G ∪ ψ′_B. E_F also carries a fault (r, ⊥, k, s) with a correct signature from a κ ∪ λ key that is not in ψ_O. Per GP 0.8.0 eq. 10.7, is the block valid — and what does this code do with it?",
 "code": {"lang": "go", "caption": "internal/extrinsic/fault_controller.go (FaultController.VerifyReportHashValidty)", "src": """func (f *FaultController) VerifyReportHashValidty() error {
    posteriorStates := blockchain.GetInstance().GetPosteriorStates()
    psiBad := posteriorStates.GetPsiB()
    psiGood := posteriorStates.GetPsiG()
    // ... badMap / goodMap are filled from psiBad / psiGood ...
    length := len(f.Faults)
    for i := 0; i < length; i++ {
        vote := f.Faults[i].Vote
        // if vote not contradict verdict, should not be in faults
        inGood := goodMap[f.Faults[i].Target] && !badMap[f.Faults[i].Target]
        inBad := !goodMap[f.Faults[i].Target] && badMap[f.Faults[i].Target]
        if (vote && inGood) || (!vote && inBad) {
            return errors.New("fault_verdict_wrong")
        }
    }
    return nil
}"""},
 "options": [
  "Valid: v = ⊥ does not contradict a non-good verdict, so the fault stands, k enters ψ′_O and H_O; the code agrees, since neither inGood nor inBad is set for a wonky target",
  "Invalid: the equivalence forces r into exactly one of ψ′_B, ψ′_G, so a wonky report admits no fault for either v; the code nevertheless accepts it, since it only rejects (v ∧ good) or (¬v ∧ bad)",
  "Invalid, and the code rejects it too: with inGood = inBad = false both clauses collapse to the vote itself, so fault_verdict_wrong is returned for v = ⊥",
  "Valid only if v = ⊤ — a 'valid' vote on a report that is not in ψ′_G is the offense a fault documents — and the code rejects exactly that combination via inGood"
 ],
 "answer": 1,
 "optNotes": [
  "wonky 時等價式的前兩項就已經不相等，無論 v 為何都不成立，fault 不可能合法。",
  "eq. 10.7 要求 r 必落在 ψ′_B 或 ψ′_G 之一；wonky 時程式兩個子句皆假 → 直接放行。",
  "inGood = inBad = false 時，(vote ∧ false) 與 (¬vote ∧ false) 都是 false，不會回錯誤。",
  "v = ⊤ 只有對 bad report 才是 offense；good report 對應的 fault 投的是 ⊥。",
 ],
 "explanation": "eq. 10.7 是三向等價：r ∈ ψ′_B ⇔ r ∉ ψ′_G ⇔ v。真值表：r 是 bad → (⊤ ⇔ ⊤ ⇔ v) → v 必須是 ⊤（offender 對壞 report 投 valid）；r 是 good → (⊥ ⇔ ⊥ ⇔ v) → v 必須是 ⊥（對好 report 投 invalid）；r 是 wonky 或根本沒被判過 → r ∈ ψ′_B 為 ⊥、r ∉ ψ′_G 為 ⊤，前兩項就不等價 → 區塊無效。直覺：wonky 表示「無法判定」，沒有人能被證明投錯票，所以 wonky verdict 只會清 ρ†（eq. 10.14），不會產生 offender。這段 Go 放行之後，k 還會被 UpdatePsiO 寫進 ψ′_O 並出現在 H_O——與 reference 分歧；#1042 的「fault equivalence enforcement」就是補這個洞。另外 k 的來源也有限制：k ∈ {κ ∪ λ 的 Ed25519 key} \\ ψ_O（prior），已在 punish-set 裡的 key 不能再報（你們回 offender_already_reported）。",
 "trap": "fault 只能指向 good 或 bad 的 report；wonky 沒有 offender，只有 ρ† 清除。"
},
{
 "id": "ch10-report-hash-identity",
 "ch": "10", "section": "10.1 The State", "gpRef": "eq. 10.1, 10.6, 10.14; cf. eq. 11.28",
 "difficulty": 2, "kind": "rationale", "tags": ["disputes", "rationale", "hashing"],
 "stem": "ψ_G, ψ_B, ψ_W, every judgment message, every culprit proof and the ρ† clearing rule (eq. 10.14) all identify the disputed item by one 32-byte hash. Which hash is it, and why is that the right identity for a dispute?",
 "options": [
  "The work-package hash (w_s)_h: the package is the unit of work, so judging it bans every report ever made of that package, and eq. 10.14 compares the package hash held in ρ[c] against the verdict",
  "H(E(g)) — the hash of the whole guarantee including its credential and slot, so that the guarantors who signed are bound into the judged object and culprits can be derived from the verdict alone",
  "H(E(w)) — the hash of the encoded work-report: it is exactly what guarantors signed (X_G ⌢ H(w)), so a culprit proof is the original guarantee signature, and eq. 10.14 matches cores via H((ρ[c]_g)_w)",
  "The erasure root (w_s)_u, because a dispute is ultimately about whether the erasure-coded bundle behind the report reconstructs to valid data, which is what auditors re-execute"
 ],
 "answer": 2,
 "optNotes": [
  "package hash 只承諾輸入：同一個 package 可能產出一對一錯的兩份 report，分不開。",
  "若 hash 含 credential，同一份 report 換一組簽章就成了另一個物件，judgment 也無法獨立計算。",
  "H(E(w)) 與 guarantor 簽的 X_G ⌢ H(w) 是同一個訊息，culprit proof 就是原本那把簽章。",
  "erasure root 只承諾資料可用性、不承諾計算結果，而 dispute 爭的正是結果。",
 ],
 "explanation": "§10.1：ψ_G/ψ_B/ψ_W 是「the hashes of all work-reports」；eq. 10.14 用 H((ρ[c]_g)_w)——取 assignment 裡的 guarantee、再取其中的 work-report 來 hash——去比對 verdict。dispute 爭的是「這份宣稱的結果」是否正確，所以識別碼必須綁在 report 這一層。eq. 10.6 的 culprit 簽章是 Ed25519_k(X_G ⌢ r)，而 eq. 11.28 的 guarantee 簽章是 Ed25519(X_G ⌢ H(w))——訊息完全相同（這也是 0.8.0 #494 把整個 guarantee 存進 ρ 的理由之一：「the guarantor signatures are needed to construct a disputes extrinsic」）。你們 ClearWorkReports 正是 `encoder.Encode(&priorStatesRho[i].Report)` 再 Blake2b——hash 的是 report，不是整個 assignment (g, t)。",
 "trap": "三處同一個 hash：judgment 訊息 X_valid/X_invalid ⌢ H(w)、culprit 訊息 X_G ⌢ H(w)、ρ† 清除 H((ρ[c]_g)_w)。"
},
{
 "id": "ch11-rho-pipeline-worked",
 "ch": "11", "section": "11.2 Package Availability Assurances / 11.5 Transitioning for Reports", "gpRef": "eq. 11.16–11.18, 11.32, 11.46",
 "difficulty": 3, "kind": "concept", "tags": ["assurances", "guarantees", "calc", "tiny", "timeout"],
 "stem": "Tiny config (|κ| = 6, U = 5), one core c = 0, no disputes. Block at slot 40: E_G carries guarantee g₁ for core 0. Block at slot 42: E_A has 4 assurances with bit 0 set. Block at slot 45: E_A has 3 assurances with bit 0 set and E_G carries an otherwise-valid guarantee g₂ for core 0. After the slot-45 block, what are ρ‡[0] and ρ′[0], and is g₁'s report ever accumulated?",
 "options": [
  "ρ‡[0] = ∅ because 45 ≥ 40 + U; g₁'s report never enters R and is dropped without accumulation; g₂ is accepted, so ρ′[0] = (g₂, 45)",
  "ρ‡[0] = (g₁, 40): the 4 + 3 = 7 assurances gathered so far exceed the threshold of 5, so the report is in R and accumulates, while g₂ is rejected as core_engaged",
  "ρ‡[0] = ∅ because the cumulative 7 assurances made the report available; it accumulates in this block and ρ′[0] = (g₂, 45)",
  "ρ‡[0] = (g₁, 40): the timeout only fires once H_T > t + U, i.e. from slot 46, so g₂ is rejected as core_engaged"
 ],
 "answer": 0,
 "optNotes": [
  "45 ≥ 40 + 5 觸發 timeout，g₁ 從未進入 R，同一塊的 core 就能換上 g₂。",
  "assurance 不跨塊累加：ρ 只存 (g, t)，state 裡沒有任何計數器。",
  "同樣把 4 + 3 當成 7 票；eq. 11.17 只數本塊 E_A 裡的 assurance。",
  "eq. 11.18 的比較子是 ≥ 而不是 >，slot 45 就已經逾時。",
 ],
 "explanation": "逐塊推演。slot 40：eq. 11.46 → ρ′[0] = (g₁, 40)（timestamp 是 τ′，不是 g₁ 裡的 t）。slot 42：eq. 11.17 的 R 只數**本塊** E_A：Σ_{a ∈ E_A} a_f[0] = 4，門檻是 > 2/3·6 = 4，需 ≥ 5 → 不可用；eq. 11.18 的 timeout 檢查 42 ≥ 40 + 5 為假 → ρ‡[0] = ρ′[0] = (g₁, 40)。slot 45：本塊只有 3 個 assurance → 仍不可用（assurer 必須每塊重送，直到某一塊單獨過門檻）；但 45 ≥ 40 + 5 成立 → ρ‡[0] = ∅；g₁ 的 report 從未進入 R，就這樣消失、不 accumulate（§11 開頭：「timed-out, implying it may be replaced by another report without accumulation」）。接著 eq. 11.32 用 ρ‡ 檢查 core：ρ‡[0] = ∅ → g₂ 合法 → ρ′[0] = (g₂, 45)。附註：slot 45 的三個 assurance 仍合法，因為 eq. 11.16 只要求 ρ†[0] ≠ ∅（timeout 在 ρ‡ 才生效）。你們 FilterAvailableReports：`headerTimeSlot >= AssignedSlot + WorkReportTimeout`，UpdateNewlyAvailableWorkReports 只統計當塊 extrinsic——與 GP 一致。",
 "trap": "assurance 不累積；timeout 用 ≥；timeout 的 report 不 accumulate，但 core 同一塊就可再用——這正是 ρ‡ 存在的理由。"
},
{
 "id": "ch11-guarantee-slot-window-calc",
 "ch": "11", "section": "11.4 Work Report Guarantees", "gpRef": "eq. 11.28",
 "difficulty": 2, "kind": "concept", "tags": ["guarantees", "rotation", "calc"],
 "stem": "Full config (R = 10). The block being imported has τ′ = 57. For a guarantee g = (w, t, a) in E_G, which values of t are acceptable under eq. 11.28, and which assignment (M or M*) verifies the credential for each?",
 "options": [
  "t ∈ [47, 57] — a sliding window of R slots ending at τ′; t ∈ [47, 49] is verified against M* and t ∈ [50, 57] against M; t = 46 is rejected as too old",
  "t ∈ [40, 57]: t ∈ [40, 49] is verified against M* (rotation index 4) and t ∈ [50, 57] against M (rotation index 5); t = 39 and t = 58 are both rejected",
  "t ∈ [50, 57] only — the current rotation, all verified against M — because M* is consulted solely when the previous rotation lies in the previous epoch",
  "t ∈ [40, 59] — the whole previous and current rotation — with t > τ′ allowed since guarantees may be produced before the block that includes them"
 ],
 "answer": 1,
 "optNotes": [
  "下界是 rotation 對齊的 R·(⌊τ′/R⌋ − 1) = 40，不是滑動的 τ′ − R = 47。",
  "⌊57/10⌋ = 5 → 下界 10·4 = 40，共 18 個 slot；rotation index 相同才用 M。",
  "M* 在每個 rotation 邊界都會用到，並不是只有跨 epoch 時才查。",
  "eq. 11.28 明寫 t ≤ τ′，未來 slot 的 guarantee 一律不收。",
 ],
 "explanation": "eq. 11.28 第三行：R·(⌊τ′/R⌋ − 1) ≤ t ≤ τ′。⌊57/10⌋ = 5 → 10·(5 − 1) = 40，所以 40 ≤ t ≤ 57，共 18 個 slot（前一整個 rotation + 本 rotation 到目前為止）。選集合的規則：(c, k) = M 當 ⌊τ′/R⌋ = ⌊t/R⌋，否則 M*。t ∈ [50, 57] → ⌊t/10⌋ = 5 = ⌊57/10⌋ → M = (P(|κ′|, η′_2, 57), Φ(κ′))；t ∈ [40, 49] → ⌊t/10⌋ = 4 → M* = (P(|k|, e, τ′ − R = 47), Φ(k))，而 ⌊47/600⌋ = ⌊57/600⌋，所以 (k, e) = (κ′, η′_2)，rotation index ⌊47/10⌋ = 4。你們 ValidateSignatures：`(int(tau)/RotationPeriod-1)*RotationPeriod <= slot` 否則 ReportEpochBeforeLast、`slot <= tau` 否則 FutureReportSlot、`tau/R == slot/R` 決定 GFunc 或 GStarFunc——完全對應。",
 "trap": "下界是 rotation 對齊的 R(⌊τ′/R⌋−1)，不是 τ′−R；τ′ = 57 時可回溯 17 個 slot，τ′ = 50 時也是只回到 40。"
},
{
 "id": "ch11-rotation-epoch-boundary-mstar",
 "ch": "11", "section": "11.3 Guarantor Assignments", "gpRef": "eq. 11.23, 11.28",
 "difficulty": 3, "kind": "concept", "tags": ["guarantees", "rotation", "calc", "epoch-boundary"],
 "stem": "Full config (E = 600, R = 10). A block at τ′ = 603 includes a guarantee with t = 595. Which assignment must its credential be checked against?",
 "options": [
  "M* = (P(|κ′|, η′_2, 593), Φ(κ′)): the previous rotation always uses the current epoch's entropy and set, only the rotation index differs",
  "M = (P(|κ′|, η′_2, 603), Φ(κ′)) at rotation index 0, because t is within R slots of τ′",
  "The guarantee is invalid: a guarantee may not straddle an epoch boundary because the validator set may have changed",
  "M* = (P(|λ′|, η′_3, 593), Φ(λ′)): the previous rotation (index 59) belonged to the previous epoch, so it is recomputed from λ′ and η′_3"
 ],
 "answer": 3,
 "optNotes": [
  "τ′ − R = 593 落在上一個 epoch，eq. 11.23 因此改用 (λ′, η′_3) 而不是當期的 (κ′, η′_2)。",
  "判準是兩個 rotation index 是否相同（60 ≠ 59），而不是 t 與 τ′ 的距離。",
  "GP 明講可以用前一個 rotation 的 t，M* 正是為此而存在。",
  "⌊593/600⌋ = 0 ≠ ⌊603/600⌋ = 1 → 取 (λ′, η′_3)，P 內的 rotation index 是 59。",
 ],
 "explanation": "先看視窗：R(⌊603/10⌋ − 1) = 590 ≤ 595 ≤ 603 ✓。再看 rotation：⌊603/10⌋ = 60 ≠ ⌊595/10⌋ = 59 → 用 M*（eq. 11.28 的 otherwise）。eq. 11.23：(k, e) = (κ′, η′_2) 當 ⌊(τ′ − R)/E⌋ = ⌊τ′/E⌋，否則 (λ′, η′_3)。為什麼這樣才對：epoch 換屆時 λ′ = κ（eq. 6.14）、η′_3 = η_2（eq. 6.24），正好是上個 epoch 期間算 M 所用的 (κ′, η′_2)，所以 M* 精確重現 rotation 59 的分配；換屆後 η′_2 已是新 epoch 的 entropy，拿它配 λ′ 或 κ′ 都算不出當時的分配。注意 0.8.0 額外要求：即使用 M*，w_c 仍須 < |κ′|/3（posterior set）——「Use of an inactive core is not permitted even if a timeslot in the previous rotation is used and the core was active then」；且 Φ 用的是 ψ′_O，本塊新抓到的 offender 在 λ′ 裡也會被 null 掉。你們 GStarFunc：`(tau − R)/E == tau/E` 選 (η′_2, κ′) 否則 (η′_3, λ′)，再以 tau − R 呼叫 NewGuranatorAssignments——一致。",
 "trap": "M* 的 entropy/set 由 τ′ − R 落在哪個 epoch 決定；(λ′, η′_3) 這組合只在 epoch 開頭的第一個 rotation 出現。"
},
{
 "id": "ch11-code-permute-080",
 "ch": "11", "section": "11.3 Guarantor Assignments", "gpRef": "eq. 11.20–11.22 — internal/extrinsic/guarantor_assignments.go permute",
 "difficulty": 2, "kind": "code", "tags": ["guarantees", "shuffle", "code", "delta-0.8.0"],
 "stem": "This is the team's P (GP 0.7.2). Under GP 0.8.0 (eq. 11.20–11.21), what changes when the validator sequence has |κ′| = 9 in a chain with C = 341 cores?",
 "code": {"lang": "go", "caption": "internal/extrinsic/guarantor_assignments.go (rotateCores, permute)", "src": """// (11.19) R(c, n) = [(x + n) mod C | x ∈ c]
func rotateCores(in []types.U32, n types.U32) []types.U32 {
    out := make([]types.U32, len(in))
    for i, x := range in {
        out[i] = (x + n) % types.U32(types.CoresCount)
    }
    return out
}

// (11.20)
func permute(e types.Entropy, currentSlot types.TimeSlot) []types.CoreIndex {
    base := make([]types.U32, types.ValidatorsCount)
    for i := 0; i < types.ValidatorsCount; i++ {
        c := (types.CoresCount * i) / types.ValidatorsCount
        base[i] = types.U32(c)
    }

    shuffled := shuffle.Shuffle(base, types.OpaqueHash(e))

    subEpoch := (int(currentSlot) % types.EpochLength) / types.RotationPeriod

    // R(...) call
    rotatedU32 := rotateCores(shuffled, types.U32(subEpoch))
    ..."""},
 "options": [
  "0.8.0 builds the base [⌊i/3⌋ | i ∈ N_9] = [0,0,0,1,1,1,2,2,2] and rotates modulo |κ′|/3 = 3; this code builds ⌊341·i/9⌋ = [0, 37, 75, …, 303] and rotates modulo 341, scattering guarantors over inactive cores",
  "Nothing observable: ⌊C·i/V⌋ and ⌊i/3⌋ coincide for every validator count permitted by eq. 6.8, and mod C equals mod V/3 for the same reason, so only the constant names differ between the versions",
  "0.8.0 keeps ⌊C·i/V⌋ = [0, 37, 75, …, 303] as the base but changes the rotation modulus from C to E/R = 60, the number of rotations per epoch, so the shuffle output cycles once per epoch",
  "0.8.0 replaces the Fisher–Yates shuffle by a plain rotation of the identity assignment [0, 1, 2, …, 8] modulo |κ′|/3, removing the dependence on η′_2 so that assignments are known a whole epoch ahead"
 ],
 "answer": 0,
 "optNotes": [
  "0.8.0 的 base 是 ⌊i/3⌋、modulus 是 |κ′|/3；⌊C·i/9⌋ 會把 guarantor 撒到 inactive core。",
  "只有 V = 3C 時兩式才重合；eq. 6.8 允許的其他 |κ| 一出現就分歧。",
  "E/R = 60 是每個 epoch 的 rotation 次數，跟 rotation 的 modulus（core 數）是兩回事。",
  "F 與 η′_2 都還在：用 η′_2 而非 η′_1 正是為了避免 fork magnification。",
 ],
 "explanation": "eq. 11.21：P(v, e, t) = R(F([⌊i/3⌋ | i ∈ N_v], e), ⌊(t mod E)/R⌋)；eq. 11.20：R(c, n) = [(x + n) mod (|c|/3) | x ∈ c]。0.8.0 的邏輯是「每個 core 3 個 guarantor，所以只有前 |κ′|/3 個 core 是 active」（§11.3）；|κ′| = 9 → base = [0,0,0,1,1,1,2,2,2]，用 η′_2 做 Fisher–Yates 後 rotation 取 mod 3。你們 permute 是 0.7.2 的 ⌊C·i/V⌋ 加 `% CoresCount`：i = 0..8 → ⌊341·i/9⌋ = [0, 37, 75, 113, 151, 189, 227, 265, 303]，再 mod 341——把 guarantor 分到 inactive core，且每個 core 只有 1 人，永遠湊不到 2 個簽章。為什麼現在 test vectors 都過？因為 tiny (6, 2) 與 full (1023, 341) 都滿足 V = 3C：⌊2i/6⌋ = ⌊341i/1023⌋ = ⌊i/3⌋，且 mod C = mod V/3，兩式完全重合；一旦 0.8.0 eq. 6.8 允許的其他 |κ| ∈ {3c} 出現就分歧（issue #1037「support variable validator-set size」）。",
 "trap": "0.8.0 的 base 與 modulus 都只看 |κ′|（⌊i/3⌋、mod |κ′|/3），C 只在 ρ 的長度出現。"
},
{
 "id": "ch11-code-anchor-checks-080",
 "ch": "11", "section": "11.4.1 Contextual Validity of Reports", "gpRef": "eq. 11.36, 11.38 — internal/extrinsic/guarantee_controller.go ValidateContexts",
 "difficulty": 2, "kind": "code", "tags": ["guarantees", "context", "code", "delta-0.8.0"],
 "stem": "This is the team's refinement-context validation (GP 0.7.2). Which conditions required by GP 0.8.0 eq. 11.36 (anchor) and eq. 11.38 (lookup anchor) are missing from it?",
 "code": {"lang": "go", "caption": "internal/extrinsic/guarantee_controller.go (GuaranteeController.ValidateContexts)", "src": """for _, context := range contexts {
    recentAnchorMatch := false
    stateRootMatch := false
    beefyRootMatch := false
    for _, blockInfo := range betaDagger {
        // xa = yh
        if context.Anchor == blockInfo.HeaderHash {
            recentAnchorMatch = true
            // xs = ys
            stateRootMatch = (context.StateRoot == blockInfo.StateRoot)
            // xb = yb
            beefyRootMatch = context.BeefyRoot == types.BeefyRoot(blockInfo.BeefyRoot)
            break
        }
    }
    ...
}
// 11.35   ancestors currently not maintained
ancestry := blockchain.GetInstance().GetAncestry()
if len(ancestry) > 0 {
    for _, context := range contexts {
        anchorHashCondition := false
        for _, item := range ancestry {
            cond1 := item.Slot == context.LookupAnchorSlot
            cond2 := item.HeaderHash == context.LookupAnchor
            if cond1 && cond2 {
                anchorHashCondition = true
                break
            }
        }
        ..."""},
 "options": [
  "Anchor: compare against β instead of β†, since 0.8.0 no longer patches the parent's state root into recent history; lookup anchor: unchanged, since the ancestor set already stores (slot, hash) pairs",
  "Anchor: the context's anchor timeslot must also equal the β† entry's timeslot (x_t = y_t); lookup anchor: the child header h′ (h′_p = H(h)) must carry h′_r = l_s, verifying the lookup anchor's posterior state root",
  "Anchor: drop the state-root comparison because 0.8.0 anchors carry a timeslot instead of a state root; lookup anchor: check only l_t ≥ H_T − L, since the ancestor-set requirement was removed in 0.8.0",
  "Nothing beyond renaming BeefyRoot to the accumulation-output super-peak b, with the new BlockInfo timeslot being informational only; both anchor tuples are otherwise identical to 0.7.2"
 ],
 "answer": 1,
 "optNotes": [
  "β† 仍然必要：它把父塊 entry 的 state root 換成本塊的 H_R（eq. 7.5），否則沒有正確的 root 可比。",
  "缺的正是 eq. 11.36 的第四個等式 x_t = y_t，以及 eq. 11.38 的 h′_r = l_s。",
  "state root 的比對並沒有被拿掉，祖先集合的要求也還在，eq. 11.38 仍是硬性條件。",
  "「只是改名」忽略了 0.8.0 新增的兩個欄位：anchor slot 與 lookup-anchor posterior root。",
 ],
 "explanation": "eq. 11.36（0.8.0）：∀x ∈ x：∃y ∈ β†：x_a = y_h ∧ x_s = y_s ∧ x_b = y_b ∧ x_t = y_t——四個等式，第四個 timeslot 是 #526 新增（β 的每筆 entry 在 0.8.0 也多了 timeslot，eq. 7.2/7.8；你們 #1031 加了 BlockInfo.timeslot）。eq. 11.38（0.8.0）：∃h, h′ ∈ A：h_t = l_t ∧ H(h) = l ∧ h′_p = H(h) ∧ h′_r = l_s——lookup anchor 的 posterior state root l_s 沒辦法從 h 自己讀到（header 只帶 prior state root H_R），所以透過它的子塊 h′ 的 H_R 來驗。這段 Go 只比對 Anchor/StateRoot/BeefyRoot（三項）以及 ancestry 的 (slot, hash)（兩項）；#1027 加了 anchor_slot 與 lookup_anchor_state_root 兩個欄位，驗證邏輯也要跟上。",
 "trap": "0.8.0 的 anchor 比四項（hash、state root、super-peak、slot）；lookup anchor 比三項，其中 l_s 要靠子塊的 H_R。"
},
{
 "id": "ch11-lookup-anchor-ancestry",
 "ch": "11", "section": "11.4.1 Contextual Validity of Reports", "gpRef": "eq. 11.37–11.38",
 "difficulty": 2, "kind": "concept", "tags": ["guarantees", "context", "fuzzer"],
 "stem": "Why can the lookup-anchor requirement (eq. 11.38) not be checked from the on-chain state σ alone, and how does the conformance fuzzer make it checkable for an M1 target?",
 "options": [
  "It only needs β, the last H = 8 blocks, whose entries carry a header hash, a state root and a timeslot, so the check is purely on-chain; the fuzzer merely replays enough blocks to fill β before it submits any guarantees",
  "It needs the full posterior state of the lookup-anchor block in order to recompute its state root r, which the fuzzer supplies on demand through GetState messages while the block is being imported",
  "It needs the headers of the last L slots (the ancestor set, not part of σ), deterministic from the header chain; the fuzzer's Initialize message therefore carries an ancestry list of (slot, header hash), a mandatory M1 feature",
  "The fuzzer skips it: 0.8.0 made the lookup anchor optional in the refinement context, so only the age bound l_t ≥ H_T − L is exercised by the vectors and no ancestry list is transmitted at Initialize"
 ],
 "answer": 2,
 "optNotes": [
  "β 只有 H = 8 筆，而 lookup anchor 可回溯 L = 14,400 slot，覆蓋範圍差了三個數量級。",
  "eq. 11.38 只比對 header 欄位、不必重算 state root；GetState 是匯入完成後的稽核介面。",
  "祖先集合不在 σ 裡，但由 header chain 決定，所以仍是 deterministic and calculable。",
  "eq. 11.4 的 ℂ 一定帶 l、t、r 三個 lookup-anchor 欄位，0.8.0 反而多要求了 posterior root r。",
 ],
 "explanation": "§11.4.1 原文：「this is one of the few conditions which cannot be checked purely with on-chain state and must be checked by virtue of retaining the series of the last L headers as the ancestor set. Since it is determined through the header chain, it is still deterministic and calculable.」eq. 11.37 只用 H_T 與 l_t 比（l_t ≥ H_T − L，L = 14,400 slots = 24 小時）；eq. 11.38 則要在祖先集合裡找到 h（h_t = l_t、H(h) = l）及其子塊 h′（h′_p = H(h)、h′ 的 prior-state-root = r）——後者是 β 完全沒有的資訊。Conformance fuzzer 因此把 Ancestry 列為 M1 必備 feature（「lookup anchors in guarantees are within last L imported headers」），Initialize（SetState）訊息附帶 ancestry 陣列，之後每次成功 import 再 append——這就是 #853/#854「add ancestry to store and fix guarantee slot validation」與 #892 的來源。你們 ValidateContexts 只在 `len(ancestry) > 0` 時比對 (slot, hash)，否則跳過（錯誤碼 LookupAnchorNotRecent）。",
 "trap": "anchor 靠 β†（state 內），lookup anchor 靠祖先 header（state 外）；兩者的年齡上限不同：H = 8 塊 vs L = 14,400 slots。"
},
{
 "id": "ch11-prerequisite-window",
 "ch": "11", "section": "11.4.1 Contextual Validity of Reports", "gpRef": "eq. 11.42",
 "difficulty": 3, "kind": "concept", "tags": ["guarantees", "dependencies", "edge-case"],
 "stem": "A work-report in E_G lists prerequisite p. Package p was guaranteed 10 blocks ago and accumulated 8 blocks ago, so p ∈ ξ but p no longer appears in any entry of β (H = 8). Is the guarantee valid?",
 "options": [
  "Valid: p ∈ ξ proves the package was accumulated, and eq. 11.42 accepts ξ alongside the extrinsic and β, so the dependency holds and the report accumulates as soon as it is available",
  "Invalid (dependency_missing): eq. 11.42 admits a prerequisite only if it is in this block's E_G or among the reported-package sets of β; ξ is not consulted at guarantee time",
  "Valid at guarantee time, but the report is parked in the ready queue ω until p is reported again inside the recent-history window, because eq. 11.42 is re-evaluated during accumulation",
  "Invalid (dependency_missing): eq. 11.42 requires every prerequisite to be guaranteed in the very same block, so only mutual and self dependencies are admissible and β is never consulted"
 ],
 "answer": 1,
 "optNotes": [
  "把 §12 的規則搬到了 §11：ξ 只在 accumulation 端用來判斷 prerequisite 是否已滿足。",
  "eq. 11.42 的來源集合只有本塊的 p 與 β 各 entry 的 reported 字典，ξ 不在其中。",
  "ω 只收已經通過 guarantee 檢查的 report，不存在「暫存等補件」這種狀態。",
  "eq. 11.42 明列 β 各 entry 的 reported 字典，vectors 的「from history」測的正是這條路徑。",
 ],
 "explanation": "eq. 11.42：∀w ∈ I, ∀p ∈ (w_x)_p ∪ keys(w_l)：p ∈ p ∪ {x | x ∈ keys(b_p), b ∈ β}——prerequisite（以及 segment-root lookup 的 key）只能來自本塊 E_G 的 package hash 集合 p，或 β 各 entry 的 reported-package 字典（最近 H = 8 塊）。ξ（accumulated，保存 E 個 slot 的 accumulated package hash）完全沒有出現在這條式子裡；它是 §12 accumulation 端用來判斷 prerequisite 是否已滿足、決定 report 進 R* 還是留在 ω 的依據。所以「10 塊前 report、8 塊前 accumulate」的 p 已經掉出 β：新 report 在 guarantee 階段就被拒（你們回 DependencyMissing；test vectors 的 dependencies 案例分 mutual/self/from history 三種）。設計意圖：pipeline 中相依的 package 應緊接著提交；β 同時提供 segment root（eq. 11.43–11.44）供 lookup 驗證，ξ 沒有 segment root。你們 CheckExtrinsicOrRecentHistory 的 checkPackageSet 正是 p ∪ β.History[].Reported。",
 "trap": "guarantee 時看 β（8 塊），accumulate 時看 ξ（E 個 slot）；兩個視窗、兩個問題。"
},
{
 "id": "ch11-code-hash-prediction",
 "ch": "11", "section": "11.4.1 Contextual Validity of Reports", "gpRef": "eq. 11.45",
 "difficulty": 3, "kind": "concept", "tags": ["guarantees", "digest", "edge-case"],
 "stem": "Service s upgraded its code after a work-package was built: the work-item's code hash c was correct at build time and refine ran the code available at the lookup anchor, but the including block's prior state has δ[s]_c ≠ c. What happens to the guarantee at inclusion?",
 "options": [
  "Accepted: c only records which code refine actually executed, resolved against the lookup anchor's posterior state, and accumulation then simply runs whatever δ′[s]_c holds at that time",
  "Accepted, but the digest's result is overwritten on-chain with the BAD error, since the recorded code hash no longer resolves to a preimage the service still holds in its lookup dictionary",
  "Accepted provided the lookup anchor is at most L = 14,400 slots old, because code availability is judged only at the lookup anchor and eq. 11.45 constrains the payload hash, not the code hash",
  "Rejected (bad_code_hash): eq. 11.45 demands d_c = δ[d_s]_c in the prior state of the including block, so a report refined against superseded code is discarded rather than accumulated"
 ],
 "answer": 3,
 "optNotes": [
  "eq. 11.45 是硬性等式，比對基準是包含區塊的 prior δ，既不是 lookup anchor 也不是 δ′。",
  "鏈上規則從不改寫 digest：改寫會讓 report hash 對不上 guarantor 的簽章。",
  "11.45 管的是 d_c（code hash），payload hash 鏈上不檢查；年齡上限是另一條 eq. 11.37。",
  "eq. 11.45 要求 d_c = δ[d_s]_c，service 一升級這個預測就落空，report 只能重做。",
 ],
 "explanation": "§11.1.4：「We include the hash of the code of the service at the time of being reported c, which must be accurately predicted within the work-report according to equation 11.45」；eq. 11.45：∀w ∈ I, ∀d ∈ w_d：d_c = δ[d_s]_c，δ 是 prior state。§14 的 work-item 也說 c 是「the code hash of the service at the time of reporting (whose preimage must be available from the perspective of the lookup anchor block)」——refine 執行的是這個 hash 在 lookup-anchor 視角下 historical lookup 到的 preimage，而鏈上檢查的是包含區塊當下的 δ[s]_c（reports vectors 有 bad_code_hash 案例）。理由：accumulate 稍後會用當下的 code 執行，若 report 是用已被淘汰的 code 算出來的，不該進入 accumulation，而是讓 guarantor 重做。附帶一提，BAD 是 refine 階段在 lookup-anchor 視角查不到 code preimage 時就寫進 digest 的值（eq. 11.7），與這條鏈上檢查是兩回事。你們 CheckWorkResult：`w.CodeHash != delta[w.ServiceID].ServiceInfo.CodeHash` → BadCodeHash，δ 取自 prior state。",
 "trap": "digest 的 c 是「預測」：refine 用 lookup-anchor 的 code，鏈上卻比對 prior δ 的 code hash。"
},
{
 "id": "ch11-inactive-core-set-shrink",
 "ch": "11", "section": "11.4 Work Report Guarantees", "gpRef": "eq. 11.18, 11.23, 11.28, 11.31",
 "difficulty": 3, "kind": "delta", "tags": ["guarantees", "assurances", "delta-0.8.0", "variable-validators"],
 "stem": "GP 0.8.0, C = 341, E = 600, R = 10. During epoch e the active set had |κ| = 12 (cores 0–3 active); at the epoch change the set shrinks to |κ′| = 9. The first block of the new epoch (τ′ = 600) carries a guarantee for core 3 with t = 595, signed by the three validators that M* assigns to core 3. Which statement is correct?",
 "options": [
  "Valid: M* reproduces the previous rotation's assignment, under which core 3 was active and 12 chunks were the right shard count; eq. 11.28's core bound is read against whichever set M* selects, and ρ‡ survives an epoch change untouched",
  "Valid, but ρ′[3] is stamped with the guarantee's own slot t = 595 instead of τ′ = 600, so eq. 11.18's H_T ≥ t + U already holds at slot 600 and the assignment is dropped in the very block that created it",
  "Invalid: eq. 11.28 bounds w_c by |κ′|/3 = 3 even under M*, so core 3 is now inactive; eq. 11.31 wants (w_s)_v = |κ′| = 9, not the 12 chunks the report carries; and eq. 11.18 has already emptied ρ‡ because |κ| ≠ |κ′|",
  "Invalid only because the signers come from λ′: eq. 11.23 lets M* fall back to the previous epoch's keys for assurances alone, so a guarantee in an epoch's first block needs κ′ signatures and w_c may be any core below C/3"
 ],
 "answer": 2,
 "optNotes": [
  "M/M* 只決定誰有資格簽；w_c 的上限永遠用 posterior κ′，ρ‡ 也會被 |κ| ≠ |κ′| 清空。",
  "eq. 11.46 的 timestamp 永遠是 τ′ = 600，600 ≥ 605 不成立，不會當場被清掉。",
  "三條 0.8.0 新規則同時命中：core 上限 |κ′|/3 = 3、shard 數要 9、且 ρ‡ 已因換屆清空。",
  "eq. 11.23 的 M* 本來就是 guarantor 的上一輪分配，λ′ 成員簽名合法；上限也不是 C/3。",
 ],
 "explanation": "這題把 0.8.0 因「validator 數可變」（eq. 6.8：|κ| ∈ {3c}）而新增的三條規則放在一起。(1) eq. 11.28：c[v] = w_c < |κ′|/3——用 **posterior** κ′ 的大小，且 GP 明說「Use of an inactive core is not permitted even if a timeslot in the previous rotation is used and the core was active then」，所以 core 3（|κ′|/3 = 3 → active 只有 0–2）即使透過 M* = (P(|λ′|, η′_3, 590), Φ(λ′)) 找得到合法簽署者也不行。(2) eq. 11.31：(w_s)_v = |κ′| = 9——每個 assurer 拿一個 chunk，chunk 數必須等於新的 assurer 數；為 12 個 validator 編的 report 對不上。(3) eq. 11.18：|κ| ≠ |κ′| 時 ρ‡ 全部清空（「Items cleared in this way can be viewed as having timed out early」）——舊集合留下的 pending report 也無法再被新集合 assure。0.7.2 沒有這些問題（V = 1023 = 3C 固定），你們 0.7.2 的 FilterAvailableReports 也沒有 size-change 條件（#1027 review 才補上），|κ′|/3 的 core 上限與 (w_s)_v = |κ′| 亦是 #1016/#1037 的範圍。",
 "trap": "0.8.0 三個「跟著 |κ′| 走」的地方：active core 數 |κ′|/3、erasure shard 數 |κ′|、|κ| ≠ |κ′| 就清 ρ‡。"
},
]
