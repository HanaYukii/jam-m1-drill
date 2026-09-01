# -*- coding: utf-8 -*-
# Chapter 10 — Disputes, Verdicts and Judgments (GP 0.8.0)
ITEMS = [
{
 "id": "ch10-state",
 "ch": "10", "section": "10.1 The State", "gpRef": "eq. 10.1",
 "difficulty": 1, "kind": "concept", "tags": ["disputes", "state"],
  "stemZh": "disputes 狀態是 ψ ≡ (ψ_G, ψ_B, ψ_W, ψ_O)。這四個分量各裝什麼？",
  "optionsZh": [
   "ψ_G、ψ_B、ψ_W 分別是被判定為正確、錯誤、無法判定的 work-report 雜湊集合；ψ_O 是被認定誤判過某份 report 的 validator 的 Ed25519 金鑰集合",
   "ψ_G、ψ_B、ψ_W 分別是擔保過、稽核過、對某份 report 提出爭議的 validator 索引集合；ψ_O 是已被判定為無效的 report 雜湊集合",
   "ψ_G、ψ_B、ψ_W 分別是被判定為正確、錯誤、無法判定的 work-package 雜湊集合；ψ_O 是被認定誤判過某份 report 的 validator 的 Bandersnatch 金鑰集合",
   "ψ_G 與 ψ_B 是被判定為正確與錯誤的 work-report 雜湊集合；ψ_W 是尚未達到 ⌊2|k|/3⌋+1 門檻的 verdict 佇列；ψ_O 則是從每位 offender 身上沒收的餘額"
  ],
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
 "explanation": "eq. 10.1：ψ ≡ (ψ_G, ψ_B, ψ_W, ψ_O)。**前三個都是 work-report hash 的集合**：good（判定正確）、bad（判定錯誤）、wonky（無法判定，票數卡在 ⌊|k|/3⌋）。**ψ_O 裝的是 Ed25519 金鑰，不是索引**——這一點值得記，理由是 validator 集合每個 epoch 都可能換人，索引在跨 epoch 之後會指向不同的人，只有金鑰是穩定的身分。**ψ_O 有兩個下游**：其一，Φ（eq. 6.15）在 epoch 換屆時把這些金鑰對應的整筆 validator key 歸零；其二，交給上層的 staking 系統處理罰則——**§10 明說 JAM 自己不動餘額**，它只負責「認定誰做錯了」，實際的 slash 由外部機制執行。**為什麼要記錄判定為 good 的那些**：§10 說這樣「ensures that additional disputes cannot be raised in the future of the chain」——判決一次定讞，同一份 report 不能被反覆拿出來爭議，否則攻擊者可以靠不斷提起爭議來拖垮處理管線。§10 也交代 verdict 本身很少發生，但它是「an important security backstop for removing and banning invalid work-reports from the processing pipeline」。",
 "trap": "報告是 report hash H(E(w))；offender 用 Ed25519 key（不是 index，因為 validator 集合每個 epoch 會變）。"
},
{
 "id": "ch10-verdict-structure",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.2–10.4",
 "difficulty": 2, "kind": "delta", "tags": ["disputes", "delta-0.8.0"],
  "stemZh": "依 GP 0.8.0，關於 disputes extrinsic 的 verdicts 成分 E_V，哪一個敘述正確？",
  "optionsZh": [
   "每個 verdict 是 (report 雜湊, epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}, judgments)；judgment 的數量必須恰好是 ⌊2|k|/3⌋+1，其中 a 是當前 epoch 時 k = κ、否則 k = λ；每份 extrinsic 至多 N_V = 16 個 verdict",
   "每個 verdict 是 (report 雜湊, epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}, judgments)；judgment 的數量必須至少是 ⌊2|k|/3⌋+1，且可以從 κ ∪ λ 合併後的集合中取；每份 extrinsic 沒有 verdict 數量上限",
   "每個 verdict 是 (report 雜湊, 該爭議被提起的時槽, judgments)；judgment 的數量必須恰好是 ⌊|k|/3⌋+1，其中 k 永遠是 posterior 的 κ′；每份 extrinsic 至多 N_V = 16 個 verdict",
   "每個 verdict 是 (report 雜湊, epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}, 一個對 report 雜湊的聚合 BLS 簽章)；簽署者必須是 k 當中的 ⌊2|k|/3⌋+1 位成員；每份 extrinsic 至多 N_V = 16 個 verdict"
  ],
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
 "explanation": "eq. 10.2：E_V ∈ ⟦(report hash, epoch index, judgments)⟧_{:N_V}，**N_V = 16**（0.8.0 PR #525 新增的硬上限，E_C 與 E_F 也各有 N_O = 16）。加上限是為了讓單塊的驗簽成本有界。**epoch index 只能是 ⌊τ/E⌋ 或 ⌊τ/E⌋ − 1**——當前或前一個 epoch，不能更舊。eq. 10.3 據此選出對應的 validator 集合：K(a) = κ 當 a 是當前 epoch，否則是 λ。**這就是為什麼 λ（previous set）必須被保留**：跨 epoch 的爭議要用當時那組金鑰驗簽。**每個 verdict 必須恰好包含 ⌊2|k|/3⌋ + 1 個 judgment**（tiny：5；full：683）——注意是「恰好」，多一票少一票都不行，這與 eq. 10.12 三個門檻都是等式是同一個設計思路。每個 judgment 由 k[i]_e 對 **X ⌢ report hash** 簽名，X 是 `$jam_valid` 或 `$jam_invalid` 兩個 domain separator 之一。**為什麼每票要能個別驗證**：因為事後要靠這些簽章構造 fault（投錯邊的人）與 culprit（擔保過 bad report 的人）——若是聚合簽章就指認不出個別責任。你們的 Verdict.Validate 檢查票數等於 ValidatorsSuperMajority，方向正確。",
 "trap": "epoch index 用 prior τ；票數是「恰好」不是「至少」。"
},
{
 "id": "ch10-verdict-thresholds",
 "ch": "10", "section": "10.2 Extrinsic", "gpRef": "eq. 10.12 (V)",
 "difficulty": 2, "kind": "concept", "tags": ["disputes", "calc", "tiny"],
  "stemZh": "一個 verdict 的結果取決於 t，也就是 ⌊2|k|/3⌋+1 個簽章當中正面判定的數量。在 tiny 設定（|k| = 6）下，哪一組（t → 結果）對照表是正確的？其他的 t 又會如何？",
  "optionsZh": [
   "t = 5 → good（⊤）；t = 0 → bad（⊥）；t = 2 → wonky（∅）；其他任何 t 都會讓區塊無效",
   "t ≥ 4 → good（⊤）；t ≤ 1 → bad（⊥）；t ∈ {2, 3} → wonky（∅）；不可能出現其他的 t",
   "t = 5 → good（⊤）；t = 0 → bad（⊥）；t = 3 → wonky（∅）；其他任何 t 都會讓區塊無效",
   "t = 6 → good（⊤）；t = 1 → bad（⊥）；t = 2 → wonky（∅）；其他任何 t 都會被靜默忽略"
  ],
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
  "stemZh": "在 GP 0.8.0 中，關於 culprits（E_C）與 faults（E_F）的敘述哪一個正確？",
  "optionsZh": [
   "culprit 指名一份位於 ψ′_B 的 report 加上該 guarantor 對 X_G ⌢ r 的簽章；fault 指名一份其宣稱的有效性 v 與 verdict 相牴觸的 report（r ∈ ψ′_B ⇔ r ∉ ψ′_G ⇔ v）；offender 的金鑰必須落在 (κ ∪ λ) 的 Ed25519 金鑰扣除 ψ_O 之後的集合裡；一個 good verdict 仍需至少 1 個 fault",
   "culprit 指名一份位於 ψ′_B 的 report 加上該 guarantor 對 X_G ⌢ r 的簽章；fault 指名一份其宣稱的有效性 v 與 verdict 一致的 report（r ∈ ψ′_G ⇔ v）；offender 的金鑰必須落在 (κ ∪ λ) 的 Ed25519 金鑰扣除 ψ_O 之後的集合裡；bad verdict 需至少 2 個 culprit、good verdict 需至少 1 個 fault",
   "culprit 指名一份位於 ψ′_G 的 report 加上該 guarantor 對 X_valid ⌢ r 的判定簽章；fault 指名一份位於 ψ′_W、其宣稱的有效性 v 與 verdict 相牴觸的 report；offender 的金鑰必須只落在 κ′ 的 Ed25519 金鑰裡；一個 good verdict 仍需至少 1 個 fault",
   "culprit 指名一份位於 ψ′_B 的 report 加上該 guarantor 對 X_G ⌢ r 的簽章；fault 指名一份其宣稱的有效性 v 與 verdict 相牴觸的 report（r ∈ ψ′_B ⇔ r ∉ ψ′_G ⇔ v）；已經在 ψ_O 裡的金鑰可以被再次提報以懲罰累犯；每一個 verdict——不論 good、bad 或 wonky——都需要至少 1 個 fault"
  ],
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
  "stemZh": "disputes extrinsic 施加了哪些排序與唯一性的約束？",
  "optionsZh": [
   "verdict 依 report 雜湊排序且唯一；culprits 與 faults 各自依 Ed25519 金鑰排序且唯一；verdict 內部的 judgment 依 validator 索引排序且唯一；任何 verdict 的 report 雜湊都不得已經出現在 ψ_G ∪ ψ_B ∪ ψ_W 裡",
   "verdict 依 report 雜湊排序且唯一；culprits 與 faults 各自依 report 雜湊排序且唯一；verdict 內部的 judgment 依它們的 ⊤/⊥ 投票排序且唯一；已經在 ψ_G ∪ ψ_B ∪ ψ_W 裡的 report 雜湊可以被重新判定以推翻先前的 verdict",
   "verdict 依該 verdict 的 epoch index 排序且唯一；culprits 與 faults 各自依 Ed25519 金鑰排序且唯一；judgment 依 validator 索引排序且唯一；任何 verdict 的 report 雜湊都不得已經出現在 ψ_O 裡",
   "verdict 依每個爭議被提起的時槽排序；culprits 與 faults 依該 offender 在 κ 中的索引排序；judgment 依簽章排序；任何位置的重複都會被靜默丟棄，而不是讓區塊無效"
  ],
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
 "explanation": "四條排序／唯一性規則，**每一條的排序鍵都不同，而且都有理由**：**eq. 10.8**：E_V 依 **report hash** 排序且唯一——一份 report 一塊之內只能被判一次。**eq. 10.9**：E_C 與 E_F 依 **offender 的 Ed25519 金鑰**排序且唯一。**為什麼不用 report hash 排**：同一份 report 可能牽出多個 offender，用 hash 根本排不出唯一序；而用金鑰排就自然保證「同一個人在同一塊裡不會被列兩次」。**eq. 10.10**：verdict 的 report hash 不得已經在 ψ_G ∪ ψ_B ∪ ψ_W 裡——**判決一次定讞**，GP 說這確保「additional disputes cannot be raised in the future of the chain」。**eq. 10.11**：verdict 內部的 judgments 依 **validator index** 排序且唯一——防止同一個人投兩票。**為什麼全部都要求排序而不只是唯一**：排序讓「檢查唯一性」變成 O(n) 的相鄰比較，而且讓編碼**正規化**——同一組內容只有一種合法寫法，state root 才不會因為排列順序不同而分歧。這是 JAM 全篇一致的做法（字典也必須依 key 排序後才編碼）。**實務意義**：test vectors 的 disputes 目錄裡大量 invalid case 就是在測這四條——not sorted、duplicate、already judged，任何一項不合都直接讓區塊無效，不是忽略該筆。",
 "trap": "culprits/faults 排序鍵是 key，不是 report hash。"
},
{
 "id": "ch10-effects",
 "ch": "10", "section": "10.2–10.3", "gpRef": "eq. 10.14–10.19",
 "difficulty": 2, "kind": "concept", "tags": ["disputes", "state"],
  "stemZh": "處理 E_D 會對狀態產生哪些效果？header 的 offenders marker H_O 又必須包含什麼？",
  "optionsZh": [
   "對任何其待處理 report 被判定為 bad 或 wonky 的 core，ρ†[c] = ∅；ψ′_G、ψ′_B、ψ′_W 各自吸收自己 verdict 的 report 雜湊；ψ′_O 吸收全部的 culprit 與 fault 金鑰；H_O = [依序的 culprit 金鑰] ⌢ [依序的 fault 金鑰]",
   "只有其 report 被判定為 bad 的 core 才 ρ†[c] = ∅，wonky 的仍維持待處理；ψ′_G、ψ′_B、ψ′_W 各自吸收自己 verdict 的 report 雜湊；ψ′_O 吸收全部的 culprit 與 fault 金鑰；H_O 列出的是 offender 的 validator 索引",
   "對任何其待處理 report 被判定為 bad 或 wonky 的 core，ρ†[c] = ∅；ψ′_G 在每次 epoch 換屆時被清空，而 ψ′_B 與 ψ′_W 持續成長；ψ′_O 只吸收 culprit 金鑰；H_O = [依序的 fault 金鑰] ⌢ [依序的 culprit 金鑰]",
   "ρ†[c] 完全不動，非正面的 verdict 只是讓之後的 accumulation 停止；ψ′_G、ψ′_B、ψ′_W 各自吸收自己 verdict 的 report 雜湊；ψ′_O 吸收全部的 culprit 與 fault 金鑰；H_O = H(E(E_D))，是對 E_D 的單一個承諾"
  ],
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
  "stemZh": "這是團隊的 verdict 分類程式碼。要符合 GP 0.8.0，必須改什麼？",
  "optionsZh": [
   "門檻必須依 |k| 計算，也就是由該 verdict 的 epoch index 所選出的那個 validator 集合（κ 或 λ）的長度，而不是用全域的 ValidatorsCount 常數",
   "什麼都不必改：|κ| 在每一種設定下都固定為 1023 = 3C，所以 ValidatorsCount 永遠是拿來取三分之二與三分之一的正確長度",
   "wonky 這個情況必須併進 default 的錯誤分支，因為 0.8.0 只記錄 good 與 bad 兩種 verdict，並且已把 ψ_W 從 disputes 狀態中完全移除",
   "default 分支必須把其餘所有票數都歸類為 wonky，因為 0.8.0 把任何既非全體一致也非零的分裂都視為無法判定"
  ],
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
 "explanation": "eq. 10.12 的三個門檻是 ⌊2|k|/3⌋ + 1（good）、0（bad）、⌊|k|/3⌋（wonky），**其中 k = K(a)，由 verdict 自己的 epoch index 決定是 κ 還是 λ**（eq. 10.3）。所以問題有兩層：**第一層**，0.8.0 起 |κ| 可變（eq. 6.8 的 𝕍 允許 6 到 1023 的 3 的倍數），拿全域常數 ValidatorsCount 去算三分之二／三分之一已經不對。**第二層更細**：即使改成動態長度，也不能一律用 |κ|——若 verdict 指的是前一個 epoch，門檻要用 **|λ|** 算。兩個集合的大小在換屆時可能不同，這正是需要依 epoch index 取對應集合的原因。這屬於你們 issue #1037「support variable validator-set size」的範疇。**程式其餘部分是對的**：default 分支回傳 error，讓不合法的票數組合直接使區塊無效，而不是忽略該筆 verdict——這符合「三個門檻都是等式」的語意。**順帶釐清 0.8.0 在 §10 到底改了什麼**：只動了 culprits 的要求與 N_V／N_O 的數量上限，**三個門檻本身沒變**，變的是 |k| 從常數變成變數。",
 "trap": "同樣的 |κ| 依賴也出現在 assurances 的 2/3 門檻與 erasure shards 數。"
},
{
 "id": "ch10-rationale",
 "ch": "10", "section": "10 intro", "gpRef": "§10 intro paragraphs",
 "difficulty": 1, "kind": "rationale", "tags": ["disputes", "rationale"],
  "stemZh": "下列哪一項不是 GP 所陳述的 disputes 系統目的？",
  "optionsZh": [
   "把無效的 work-report 從處理管線中移除並封禁",
   "在對某些金鑰的失能已有共識時，把這些麻煩的金鑰從 validator 集合中移除",
   "協調各節點回滾含有無效 work-report 的鏈延伸，並彙整 offender 交由更高層的系統懲罰（例如在 staking parachain 上沒收質押）",
   "直接在 JAM 的狀態內沒收犯規 validator 的餘額"
  ],
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
