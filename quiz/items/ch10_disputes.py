# -*- coding: utf-8 -*-
# Chapter 10 — Disputes, Verdicts and Judgments (GP 0.8.0)
ITEMS = [
{
 "id": "ch10-state",
 "ch": "10", "section": "10.1 The State", "gpRef": "eq. 10.1",
 "difficulty": 1, "kind": "concept", "tags": ["disputes", "state"],
 "stem": "The disputes state is ψ ≡ (ψ_G, ψ_B, ψ_W, ψ_O). What do the four components hold?",
 "options": [
  "ψ_G, ψ_B and ψ_W are sets of work-report hashes judged respectively correct, incorrect and impossible to judge; ψ_O is a set of the Ed25519 keys of validators found to have misjudged a report",
  "ψ_G, ψ_B and ψ_W are sets of the validator indices which respectively guaranteed, audited and disputed a report; ψ_O is a set of the report hashes that have been judged invalid",
  "ψ_G, ψ_B and ψ_W are sets of work-package hashes judged respectively correct, incorrect and impossible to judge; ψ_O is a set of the Bandersnatch keys of validators found to have misjudged a report",
  "ψ_G and ψ_B are sets of work-report hashes judged correct and incorrect; ψ_W is the queue of verdicts still short of the ⌊2|k|/3⌋+1 threshold; ψ_O is the balance slashed from each offender"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 10.1 的前三者都是 work-report hash 集合，ψ_O 則是 Ed25519 key 的 punish-set。",
  "三個集合裝的是 report hash 本身而不是誰投過票，且把 ψ_O 說成 report hash 正好相反。",
  "judgment 針對的是 work-report（hash 為 H(E(w))），而 punish-set 用的是 Ed25519 key。",
  "eq. 10.4 要求 verdict 進鏈時票數恰好，鏈上沒有待補佇列；JAM 也不在 ψ_O 記罰沒餘額。",
 ],
 "explanation": "eq. 10.1：ψ ≡ (ψ_G, ψ_B, ψ_W, ψ_O)。前三者都是 **work-report hash** 的集合：good（判定正確）、bad（判定錯誤）、wonky（無法判定）；ψ_O 是 punish-set，裝的是 **Ed25519 key**（不是 index，因為 validator 集合每個 epoch 會變），供 Φ 在換屆時把 offender 的 key 清零，也供上層 staking 系統 slash——§10 明說 JAM 自己不動餘額。§10 說明 verdict 很少發生，但是「an important security backstop for removing and banning invalid work-reports from the processing pipeline」。",
 "trap": "報告是 report hash H(E(w))；offender 用 Ed25519 key（不是 index，因為 validator 集合每個 epoch 會變）。"
},
{
 "id": "ch10-verdict-structure",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.2–10.4",
 "difficulty": 2, "kind": "delta", "tags": ["disputes", "delta-0.8.0"],
 "stem": "Per GP 0.8.0, which statement about the verdicts component E_V of the disputes extrinsic is correct?",
 "options": [
  "Each verdict is (report hash, epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}, judgments); judgments must number exactly ⌊2|k|/3⌋+1 where k = κ if a is the current epoch else λ; at most N_V = 16 verdicts per extrinsic",
  "Each verdict is (report hash, epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}, judgments); judgments must number at least ⌊2|k|/3⌋+1 and may be drawn from κ ∪ λ combined; there is no per-extrinsic cap on verdicts",
  "Each verdict is (report hash, the timeslot at which the dispute was raised, judgments); judgments must number exactly ⌊|k|/3⌋+1 where k is always the posterior set κ′; at most N_V = 16 verdicts per extrinsic",
  "Each verdict is (report hash, epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}, one aggregated BLS signature over the report hash); the signers must be ⌊2|k|/3⌋+1 members of k; at most N_V = 16 verdicts per extrinsic"
 ],
 "answer": 0,
 "optNotes": [
  "epoch index、恰好 ⌊2|k|/3⌋+1 票、K(a) 二選一、N_V = 16 四點全中 eq. 10.2–10.4。",
  "eq. 10.4 是「恰好」不是「至少」；K(a) 只取 κ 或 λ 之一；0.8.0 #525 正是新增 N_V = 16。",
  "第二欄是 epoch index 而非 timeslot；⌊|k|/3⌋ 是 wonky 門檻；K(a) 取 prior 的 κ/λ 不是 κ′。",
  "judgment 是 [(⊤/⊥, N, Ed25519 sig)] 序列、每票須可個別驗證；BLS 只用於 Beefy commitment。",
 ],
 "explanation": "eq. 10.2：E_V ∈ [(H, ⌊τ/E⌋ − N_2, [(⊤/⊥, N, Ed25519 sig)])]_{:N_V}，N_V = 16（0.8.0 #525 新增硬上限）；E_C、E_F 各最多 N_O = 16。eq. 10.3：K(a) = κ 當 a = ⌊τ/E⌋（prior τ 的 epoch），否則 λ；每個 verdict 必須恰好包含 ⌊2|k|/3⌋+1 個 judgment（tiny：5；full：683），每個 judgment 由 k[i]_e 對 X_valid/X_invalid ⌢ report hash 簽名（X = $jam_valid / $jam_invalid）。每票依 index 排序、可個別驗證，事後才能被引用來構造 fault。你們 Verdict.Validate 檢查 ValidatorsSuperMajority 個票。",
 "trap": "epoch index 用 prior τ；票數是「恰好」不是「至少」。"
},
{
 "id": "ch10-verdict-thresholds",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.12 (V)",
 "difficulty": 2, "kind": "concept", "tags": ["disputes", "calc", "tiny"],
 "stem": "A verdict's outcome depends on t, the number of positive judgments among the ⌊2|k|/3⌋+1 signatures. In the tiny config (|k| = 6), which (t → outcome) table is correct, and what happens for any other t?",
 "options": [
  "t = 5 → good (⊤); t = 0 → bad (⊥); t = 2 → wonky (∅); any other t makes the block invalid",
  "t ≥ 4 → good (⊤); t ≤ 1 → bad (⊥); t ∈ {2, 3} → wonky (∅); no other t can occur",
  "t = 5 → good (⊤); t = 0 → bad (⊥); t = 3 → wonky (∅); any other t makes the block invalid",
  "t = 6 → good (⊤); t = 1 → bad (⊥); t = 2 → wonky (∅); any other t is silently ignored"
 ],
 "answer": 0,
 "optNotes": [
  "tiny |k| = 6 代入 eq. 10.12 的三個等式：⌊4⌋+1 = 5、0、⌊2⌋ = 2，其餘 t 皆無定義。",
  "三個門檻都是等式不是區間，而且分裂票（t = 4、t = 1）正是 dispute 最可能的結果。",
  "wonky 門檻是 ⌊|k|/3⌋ = ⌊6/3⌋ = 2 而不是 3；good 與 bad 這兩個值倒是對的。",
  "good 是 ⌊2|k|/3⌋+1 = 5 不是全票 6，bad 是 0 不是 1，落空的 t 也不會被忽略。",
 ],
 "explanation": "eq. 10.12 定義 V(a, j)：**⊤（good）當 t = ⌊2|k|/3⌋ + 1；⊥（bad）當 t = 0；∅（wonky）當 t = ⌊|k|/3⌋**，其中 t 是這份 verdict 的 ⌊2|k|/3⌋+1 個簽章中投正面票的數量。tiny 設定 |k| = 6：⌊4⌋ + 1 = **5**、**0**、⌊2⌋ = **2**；full 設定 |k| = 1023：**683**、**0**、**341**。**最關鍵的一點：三個門檻都是「等式」而不是區間。** t 若落在這三個值之外（tiny 下例如 t = 3），V 根本無定義——結果不是「忽略這份 verdict」，而是**整個區塊無效**（團隊的實作回 `bad_vote_split`）。這常被誤讀成「多數決」，但 JAM 這裡要的是**明確的三態結論**：全體一致認為好、全體一致認為壞、或恰好卡在三分之一的分裂。任何其他分布都代表這份 verdict 本身是被構造出來的，不該被接受。**三個門檻對應三種後續動作**：⊤ 進 ψ_G（good set），提交 verdict 的人若曾投反對票會被列為 fault；⊥ 進 ψ_B（bad set），擔保過這份 report 的 guarantor 成為 culprit；∅ 進 ψ_W（wonky set），不罰任何人但該 report 作廢。安全假設是超過 2/3 的 validator 為誠實且在線（ELVES），三個門檻正是建立在這個假設上。",
 "trap": "wonky 是「剛好 1/3 正票」，不是「介於中間」。"
},
{
 "id": "ch10-culprits-faults",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.6–10.7, 10.13",
 "difficulty": 3, "kind": "delta", "tags": ["disputes", "delta-0.8.0"],
 "stem": "Which statement about culprits (E_C) and faults (E_F) is correct in GP 0.8.0?",
 "options": [
  "A culprit names a report in ψ′_B plus that guarantor's signature over X_G ⌢ r; a fault names a report whose claimed validity v contradicts the verdict (r ∈ ψ′_B ⇔ r ∉ ψ′_G ⇔ v); offender keys must lie in (κ ∪ λ)'s Ed25519 keys minus ψ_O; a good verdict still needs ≥ 1 fault",
  "A culprit names a report in ψ′_B plus that guarantor's signature over X_G ⌢ r; a fault names a report whose claimed validity v agrees with the verdict (r ∈ ψ′_G ⇔ v); offender keys must lie in (κ ∪ λ)'s Ed25519 keys minus ψ_O; a bad verdict needs ≥ 2 culprits and a good one ≥ 1 fault",
  "A culprit names a report in ψ′_G plus that guarantor's judgment signature over X_valid ⌢ r; a fault names a report in ψ′_W whose claimed validity v contradicts the verdict; offender keys must lie in κ′'s Ed25519 keys alone; a good verdict still needs ≥ 1 fault",
  "A culprit names a report in ψ′_B plus that guarantor's signature over X_G ⌢ r; a fault names a report whose claimed validity v contradicts the verdict (r ∈ ψ′_B ⇔ r ∉ ψ′_G ⇔ v); keys already in ψ_O may be re-reported to punish a repeat offender; every verdict, good, bad or wonky, needs ≥ 1 fault"
 ],
 "answer": 0,
 "optNotes": [
  "四個條件全中；關鍵是 fault 宣稱的 v 必須與 verdict 相反，good verdict 仍要 ≥ 1 個 fault。",
  "「bad verdict 要 ≥ 2 culprits」是 0.7.2 的規則（0.8.0 #525 移除），且 fault 的 v 條件反了。",
  "culprit 是 bad report 的 guarantor（r ∈ ψ′_B、簽 X_G），fault 不落在 ψ′_W，k 也要含 λ。",
  "k 的定義最後就寫著扣掉 ψ_O，重複上報使區塊無效；eq. 10.13 只對 (r, ⊤) 要求 fault。",
 ],
 "explanation": "eq. 10.6：∀(r, k, s) ∈ E_C：r ∈ ψ′_B ∧ k ∈ k ∧ s 是 k 對 X_G ⌢ r 的簽章（culprit = 曾 guarantee 一個壞 report 的人，用的正是他的 guarantee 簽章；X_G = $jam_guarantee，正是 eq. 11.28 那把簽章，所以 ρ 在 0.8.0 要存整個 guarantee 才 construct 得出來）。eq. 10.7：∀(r, v, k, s) ∈ E_F：r ∈ ψ′_B ⇔ r ∉ ψ′_G ⇔ v（fault 宣稱的 validity 必須與 verdict 相反：對 bad report 投 valid，或對 good report 投 invalid）。k = {κ ∪ λ 的 Ed25519 key} \\ ψ_O。eq. 10.13：∀(r, ⊤) ∈ v：∃(r, …) ∈ E_F——good verdict 至少要有一個 fault，因為 2/3+1 全投正票的 verdict 必然是有人先投了反票才會啟動 dispute。0.8.0 #525「remove culprits requirement」則拿掉了 bad verdict ≥ 2 culprits 的舊要求。",
 "trap": "你們 0.7.2 code 仍檢查 bad verdict ≥ 2 culprits（code-map 3.6.4）——0.8.0 要拿掉。"
},
{
 "id": "ch10-ordering",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.8–10.11",
 "difficulty": 2, "kind": "concept", "tags": ["disputes", "ordering"],
 "stem": "Which ordering/uniqueness constraints does the disputes extrinsic impose?",
 "options": [
  "Verdicts ordered & unique by report hash; culprits and faults each ordered & unique by Ed25519 key; judgments within a verdict ordered & unique by validator index; no verdict report hash may already be in ψ_G ∪ ψ_B ∪ ψ_W",
  "Verdicts ordered & unique by report hash; culprits and faults each ordered & unique by report hash; judgments within a verdict ordered & unique by their ⊤/⊥ vote; a report hash already in ψ_G ∪ ψ_B ∪ ψ_W may be re-judged to overturn the earlier verdict",
  "Verdicts ordered & unique by the verdict's epoch index; culprits and faults each ordered & unique by Ed25519 key; judgments ordered & unique by validator index; no verdict report hash may already be in ψ_O",
  "Verdicts ordered by the timeslot at which each dispute was raised; culprits and faults ordered by the offender's index within κ; judgments ordered by signature; duplicates anywhere are silently dropped rather than invalidating the block"
 ],
 "answer": 0,
 "optNotes": [
  "三個排序鍵都對：verdict 用 report hash、offender 用 Ed25519 key、judgment 用 validator index。",
  "offender 序列的排序鍵是 Ed25519 key、judgment 用 index，而 eq. 10.10 不許翻案重判。",
  "epoch index 只有兩個可能值排不出唯一序；要比對的也是 ψ_G ∪ ψ_B ∪ ψ_W 而非裝 key 的 ψ_O。",
  "verdict 結構裡根本沒有 timeslot 欄位，offender 用 key 不用 index，違規也不會被靜默忽略。",
 ],
 "explanation": "eq. 10.8：E_V 依 report hash 排序且唯一；10.9：E_C、E_F 依 offender 的 Ed25519 key 排序且唯一（同一個 report 可能有多個 offender，用 hash 排不出唯一序）；10.10：verdict 的 report hash 與 ψ_G ∪ ψ_B ∪ ψ_W 不相交，判決一次定讞——GP 說 recording reports found to be valid「ensures that additional disputes cannot be raised in the future of the chain」；10.11：每個 verdict 的 judgments 依 validator index 排序且唯一。這些是 test vectors（disputes/）大量 invalid case 的來源：not sorted、duplicate、already judged，任何一項不合都直接使區塊無效。",
 "trap": "culprits/faults 排序鍵是 key，不是 report hash。"
},
{
 "id": "ch10-effects",
 "ch": "10", "section": "10.2–10.3", "gpRef": "eq. 10.14–10.19",
 "difficulty": 2, "kind": "concept", "tags": ["disputes", "state"],
 "stem": "What are the state effects of processing E_D, and what must the header's offenders marker H_O contain?",
 "options": [
  "ρ†[c] = ∅ for any core whose pending report was judged bad or wonky; ψ′_G, ψ′_B and ψ′_W each absorb their verdict's report hashes; ψ′_O absorbs all culprit and fault keys; H_O = [culprit keys in order] ⌢ [fault keys in order]",
  "ρ†[c] = ∅ only for cores whose report was judged bad, wonky ones staying pending; ψ′_G, ψ′_B and ψ′_W each absorb their verdict's report hashes; ψ′_O absorbs all culprit and fault keys; H_O lists the offenders' validator indices",
  "ρ†[c] = ∅ for any core whose pending report was judged bad or wonky; ψ′_G is emptied at each epoch change while ψ′_B and ψ′_W grow; ψ′_O absorbs the culprit keys only; H_O = [fault keys in order] ⌢ [culprit keys in order]",
  "ρ†[c] is left untouched, a non-positive verdict only stopping accumulation later; ψ′_G, ψ′_B and ψ′_W each absorb their verdict's report hashes; ψ′_O absorbs all culprit and fault keys; H_O = H(E(E_D)), one commitment to E_D"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 10.14 的條件是 v ∈ {⊥, ∅}，bad 與 wonky 一起清；H_O 是 culprits 在前、faults 在後。",
  "wonky 代表無法判定，eq. 10.14 一樣要清掉；eq. 10.19 的 H_O 裝 Ed25519 key 不是 index。",
  "eq. 10.15–10.17 三個集合只做 ∪、永不清空；ψ′_O 兩邊 key 都吸收；H_O 串接順序也反了。",
  "清 ρ† 正是 disputes 階段的效果；H_O 要列出所有新 offender 的 key，不是 E_D 的單一 hash。",
 ],
 "explanation": "eq. 10.14：∀c：ρ†[c] = ∅ 當 (H(ρ[c]_w), v) ∈ v 且 v ∈ {⊥, ∅}——GP：「Authoring a block with a non-positive verdict has the effect of cancelling its imminent accumulation」。eq. 10.15–10.18：ψ′_G/ψ′_B/ψ′_W 各自 ∪ 對應的 report hash（三者單調成長、永不清空，這正是「同一個 report 不能被重複 dispute」的基礎）；ψ′_O = ψ_O ∪ {culprit keys} ∪ {fault keys}。eq. 10.19：H_O ≡ [k | (…, k, …) ∈ E_C] ⌢ [k | ∈ E_F]，內容必須是「exactly the keys of all new offenders」，好讓輕客戶端從 header 直接讀出誰被罰。你們 ClearWorkReports 對 PositiveJudgmentsSum < 2V/3 的 verdict 清 ρ。",
 "trap": "ρ† 是 disputes 之後、assurances 之前的中間狀態；順序：ρ → ρ† (disputes) → ρ‡ (assurances) → ρ′ (guarantees)。"
},
{
 "id": "ch10-code-thresholds",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.12 — internal/extrinsic/dispute_controller.go CompareVerdictsWithPsi",
 "difficulty": 2, "kind": "code", "tags": ["disputes", "code", "delta-0.8.0"],
 "stem": "This is the team's verdict classification. What must change for GP 0.8.0 conformance?",
 "code": {"lang": "go", "caption": "internal/extrinsic/dispute_controller.go", "src": """for _, verdict := range verdictSumSequence {
    switch verdict.PositiveJudgmentsSum {
    case types.ValidatorsCount*2/3 + 1:
        updates.Good = append(updates.Good, types.WorkReportHash(verdict.ReportHash))
    case 0:
        updates.Bad = append(updates.Bad, types.WorkReportHash(verdict.ReportHash))
    case types.ValidatorsCount * 1 / 3:
        updates.Wonky = append(updates.Wonky, types.WorkReportHash(verdict.ReportHash))
    default:
        return types.DisputesRecords{}, errors.New("bad_vote_split")
    }
}"""},
 "options": [
  "The thresholds must be computed from |k|, the length of the validator set that the verdict's epoch index selects (κ or λ), rather than from the global ValidatorsCount constant",
  "Nothing needs to change: |κ| is fixed at 1023 = 3C in every configuration, so ValidatorsCount is always the right length to take two-thirds and one-third of",
  "The wonky case must be folded into the default error branch, because 0.8.0 records only good and bad verdicts and dropped ψ_W from the disputes state entirely",
  "The default branch must classify every remaining vote count as wonky, because 0.8.0 treats any split that is neither unanimous nor zero as impossible to judge"
 ],
 "answer": 0,
 "optNotes": [
  "0.8.0 允許 |κ| ≠ |λ|（#514），門檻必須跟著 K(a) 選到的那個集合的長度走。",
  "§6.4 明說 validator 序列長度是 6 到 3C 之間的 3 的倍數，tiny 就是 6，並非固定 1023。",
  "ψ_W 仍是 eq. 10.1 的第三個成員，⌊|k|/3⌋ 的 wonky case 也還在，0.8.0 沒有拿掉。",
  "V 是部分函數；把 4 票、3 票也判成 wonky 會讓惡意 verdict 清掉別人的 pending report。",
 ],
 "explanation": "eq. 10.12 的門檻是 ⌊2|k|/3⌋+1、0、⌊|k|/3⌋，其中 k = K(a) ∈ {κ, λ}，所以拿全域常數 ValidatorsCount 去取三分之二／三分之一不再正確——必須依 verdict 的 epoch index 取對應集合的長度（你們 issue #1037「support variable validator-set size (|κ| ≠ V)」就是在處理這件事；§6.4 的 𝕍 見 eq. 6.8：「The length of each sequence is always a multiple of 3 between 6 and 3C」）。程式其餘部分是對的：default → error，讓不合法的票數組合直接使區塊無效。0.8.0 在 §10 只動了 culprits 要求與 N_V/N_O 上限，三個門檻本身沒變。",
 "trap": "同樣的 |κ| 依賴也出現在 assurances 的 2/3 門檻與 erasure shards 數。"
},
{
 "id": "ch10-rationale",
 "ch": "10", "section": "10 intro", "gpRef": "§10 intro paragraphs",
 "difficulty": 1, "kind": "rationale", "tags": ["disputes", "rationale"],
 "stem": "Which of the following is NOT a purpose of the disputes system as stated in the GP?",
 "options": [
  "Removing and banning invalid work-reports from the processing pipeline",
  "Removing troublesome keys from the validator set where there is consensus over their malfunction",
  "Coordinating nodes to revert chain-extensions containing invalid work-reports and aggregating offenders for punishment in a higher-level system (e.g. slashing on a staking parachain)",
  "Directly slashing the offending validator's balance inside the JAM state"
 ],
 "answer": 3,
 "optNotes": [
  "§10 intro 原話：removing and banning invalid work-reports from the processing pipeline。",
  "§10 intro 原話：removing troublesome keys from the validator set，確實是列出的目的之一。",
  "§10 intro 同樣明列 revert chain-extensions 與 aggregating offenders for punishment。",
  "JAM 只記 ψ_O 並在下次 key rotation 把 key 清零；扣質押是上層 staking parachain 的事。",
 ],
 "explanation": "§10 intro：disputes 是「an important security backstop for removing and banning invalid work-reports… as well as removing troublesome keys from the validator set… It also helps coordinate nodes to revert chain-extensions… and provides a convenient means of aggregating all offending validators for punishment in a higher-level system」。JAM 本身不做 slashing：「Should JAM be used for a public network such as Polkadot, this would imply the slashing of the offending validator's stake on the staking parachain.」JAM 只記錄 ψ_O 並在下次 key rotation 把 key 清零。",
 "trap": "與 §13 statistics 同理：rewards/slashing 都交給 staking 子系統。"
},
]
