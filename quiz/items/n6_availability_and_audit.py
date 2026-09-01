# -*- coding: utf-8 -*-
"""基礎套題 N6：資料可得性與稽核。"""

ITEMS = [
 {
  "id": "n6-why-erasure-coding",
  "ch": "N6", "section": "§11.2; App. H", "gpRef": "§11 & App. H",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "availability"],
  "stem": "Why does JAM erasure-code a work-package instead of simply asking every validator to keep a full copy?",
  "stemZh": "JAM 為什麼要把 work-package 做 erasure coding，而不是直接要求每位 validator 各留一份完整副本？",
  "options": [
   "A full copy per validator would multiply the storage cost by the validator count; coding lets each hold a small piece while the whole stays recoverable from a fraction of them",
   "A full copy per validator would be unsafe, because any single validator could then publish the package and expose data the submitter intended to keep private from others",
   "A full copy per validator would be impossible, because the package never leaves the core it was sent to and no validator outside that core ever receives any of it",
   "A full copy per validator would be slower, because coding lets the pieces be transmitted in parallel whereas a full copy has to be sent to each validator in turn"
  ],
  "optionsZh": [
   "每位 validator 各存一份完整副本會讓儲存成本乘上 validator 數量；編碼後每人只持有一小片，而整份資料仍能從其中一部分重建",
   "每位 validator 各存一份完整副本並不安全，因為任何單一 validator 都能把該 package 公開，洩漏提交者原本想對其他人保密的資料",
   "每位 validator 各存一份完整副本並不可能，因為 package 從未離開它被送往的那個 core，該 core 以外的 validator 從來收不到任何部分",
   "每位 validator 各存一份完整副本會比較慢，因為編碼後各片可以平行傳輸，而完整副本必須逐一送給每位 validator"
  ],
  "answer": 0,
  "explanation": "問題是**成本**。work-package bundle 可以到十幾 MB，如果 1023 位 validator 每人存一份，一份工作就要佔掉數十 GB 的總儲存與頻寬——這會直接抵消掉 JAM 「少數人執行」省下來的成本。Reed–Solomon 讓每人只拿一小片，而**任何 1/3 的片就能重建全部**，所以即使將近 2/3 的節點離線或作惡，資料仍然救得回來。資料本身是公開的（沒有隱私考量），而且它確實會離開 core——分發給所有 validator 正是重點。",
  "optNotes": [
   "成本乘上 validator 數是不可接受的，編碼讓每人只付一小片的代價。",
   "work-package 的內容是公開的，erasure coding 不提供任何隱私。",
   "資料必須離開 core 才有意義——分發給所有 validator 正是可得性的定義。",
   "傳輸速度不是設計動機；重點在總儲存量與容錯門檻。"
  ],
  "trap": "編碼買到的是「省成本」加「容錯」：1/3 的碎片就能重建。"
 },
 {
  "id": "n6-what-auditing-does",
  "ch": "N6", "section": "§17 Auditing", "gpRef": "§17",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "audit"],
  "alsoCh": ["N1"],
  "stem": "Only three guarantors actually ran a piece of work. What stops them from simply lying about the result?",
  "stemZh": "一份工作實際上只有三位 guarantor 跑過。是什麼阻止他們乾脆對結果說謊？",
  "options": [
   "Randomly chosen validators re-run the work afterwards and publish their own judgment, so a false result is expected to be caught and its guarantors punished",
   "The three guarantors must produce identical results before the report is accepted, so a lie would require all three of them to collude perfectly on the same wrong value",
   "The result is checked against a zero-knowledge proof that the guarantors must attach, so an incorrect result cannot be signed in the first place",
   "The result is only provisional until the service itself confirms it during accumulation, at which point a service may reject a result it does not recognise"
  ],
  "optionsZh": [
   "隨機選出的 validator 事後會重跑這份工作並公開自己的判定，因此虛假的結果預期會被抓到、其擔保人會受罰",
   "三位 guarantor 必須產生完全相同的結果，report 才會被接受，所以說謊需要三人在同一個錯誤值上完美串通",
   "結果會與 guarantor 必須附上的零知識證明比對，因此不正確的結果根本無法被簽署",
   "結果在 accumulation 階段由 service 自己確認之前都只是暫定的，屆時 service 可以拒絕它不認得的結果"
  ],
  "answer": 0,
  "explanation": "答案是**事後隨機重跑**（ELVES）。guarantor 的簽名不代表結果正確，它代表「我為這個結果負責」。之後會有隨機抽中的 auditor 拿回原始輸入（靠可得性重建）重跑一次，公開發表判定；若判定不一致就進 disputes，錯的一方被列為 offender、金鑰被歸零。三人簽名相同確實是必要條件，但**三人可以串通**——所以那不是安全來源。JAM 也沒有用零知識證明，而且 service 在 accumulate 時無從得知結果對不對（它沒有重跑的能力）。",
  "optNotes": [
   "隨機抽樣重跑加上事後懲罰，這才是 in-core 結果可信的根源。",
   "三人可以串通，所以「三人一致」本身不構成安全保證。",
   "JAM 不使用零知識證明，它靠的是重跑與經濟懲罰。",
   "service 在 accumulate 時沒有重跑能力，也就無法判斷結果對錯。"
  ],
  "trap": "簽名 = 負責，不 = 正確；正確性靠事後抽樣重跑。"
 },
 {
  "id": "n6-why-random-auditors",
  "ch": "N6", "section": "§17", "gpRef": "§17",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "audit"],
  "stem": "Auditors are picked by a verifiable random function rather than volunteering or being appointed. Why does that matter?",
  "stemZh": "auditor 是由可驗證隨機函數選出的，而不是自願或被指派。為什麼這件事重要？",
  "options": [
   "Nobody can know in advance who will check a given report, so a dishonest guarantor cannot bribe or target the checkers, and everyone can verify the selection was fair",
   "Nobody has to volunteer, so the protocol avoids the free-rider problem in which every validator would rather let someone else pay the cost of re-running the work",
   "Nobody is appointed, so the protocol needs no privileged service to maintain the auditor list, which keeps the whole auditing mechanism outside the state entirely",
   "Nobody audits twice, so the random selection guarantees each validator checks a different report and the workload is spread evenly across the validator set"
  ],
  "optionsZh": [
   "沒有人能事先知道某份 report 會由誰查核，所以不誠實的 guarantor 無法賄賂或針對查核者，而且任何人都能驗證這個抽選是公正的",
   "沒有人需要自願，協定因此避開了搭便車問題——否則每位 validator 都寧可讓別人去付重跑的成本",
   "沒有人被指派，協定因此不需要一個具特權的 service 來維護 auditor 名單，讓整個稽核機制完全留在狀態之外",
   "沒有人會稽核兩次，隨機抽選保證每位 validator 查核不同的 report，工作量因此平均分散在整個 validator 集合"
  ],
  "answer": 0,
  "explanation": "隨機性擋的是**針對性攻擊**。如果 auditor 事先可知，一個打算說謊的 guarantor 只要收買或癱瘓那幾位就能矇混過關——稽核就形同虛設。VRF 選人讓兩件事同時成立：**事前不可預測**（連被選中的人自己也要到那一刻才知道），以及**事後可驗證**（他可以出示證明說「我確實被選中」，沒被選中的人無法偽裝）。搭便車問題是靠協定義務與獎懲處理的，不是靠隨機；而隨機抽樣也不保證不重複。",
  "optNotes": [
   "事前不可預測、事後可驗證，這兩點才是 VRF 抽選的價值。",
   "搭便車靠的是義務與獎懲，隨機抽選本身解決不了誰願意付成本。",
   "auditor 的抽選用的是狀態裡的 entropy，並沒有離開狀態。",
   "隨機抽樣不保證不重複，也不以平均分攤工作量為目標。"
  ],
  "trap": "隨機的價值在「不可預測 + 可驗證」，不是公平分攤。"
 },
 {
  "id": "n6-disputes-three-outcomes",
  "ch": "N6", "section": "§10 Disputes", "gpRef": "§10",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "disputes"],
  "stem": "A dispute over one report ends in one of three verdicts. What are they, and what is the third one for?",
  "stemZh": "對一份 report 的爭議會以三種判決之一收場。是哪三種？第三種又是為了什麼？",
  "options": [
   "Good, bad, and wonky — the last covering the case where the validators split roughly evenly, so no conclusion can be drawn and nobody is punished for it",
   "Good, bad, and pending — the last covering a dispute that has not yet gathered enough judgments, which is revisited once more validators have weighed in",
   "Good, bad, and appealed — the last covering a verdict that a guarantor has formally challenged, which then escalates to the full validator set for a second round",
   "Good, bad, and expired — the last covering a dispute raised too late to matter, since the report it concerns has already been accumulated into the state"
  ],
  "optionsZh": [
   "good、bad、wonky——最後一種涵蓋 validator 意見大致對半分裂、無法得出結論的情況，這種情形不罰任何人",
   "good、bad、pending——最後一種涵蓋尚未蒐集到足夠判定的爭議，等更多 validator 表態之後會再處理一次",
   "good、bad、appealed——最後一種涵蓋 guarantor 正式提出異議的判決，會升級到全體 validator 進行第二輪",
   "good、bad、expired——最後一種涵蓋提得太晚而無關緊要的爭議，因為它所針對的 report 早已被 accumulate 進狀態"
  ],
  "answer": 0,
  "explanation": "三種判決是 **good（⊤）、bad（⊥）、wonky（∅）**。前兩種好理解：一致認為結果正確、或一致認為錯誤。**wonky 是給「連 validator 自己都無法達成一致」的情況**——票數恰好卡在三分之一那個門檻。這種時候協定不假裝知道答案：該 report 作廢，但**不懲罰任何人**，因為無法認定誰說謊。這個設計反映一個務實的判斷：分不出對錯時，最安全的做法是丟掉這份工作而不是隨便罰人。三個門檻都是**等式**而非區間，落在其外的票數分布會讓整個區塊無效。",
  "optNotes": [
   "wonky 對應無法認定的分裂情況，作廢該 report 但不罰任何人。",
   "沒有 pending 這種狀態；一份 verdict 必須帶足額的判定才合法。",
   "沒有申訴或第二輪機制，判決一次定讞。",
   "沒有過期概念；爭議的 epoch 範圍另有規定，但那不是第三種判決。"
  ],
  "trap": "第三種是 wonky（分不出對錯）：報告作廢、但不罰人。"
 },
 {
  "id": "n6-offender-consequence",
  "ch": "N6", "section": "§10; §6.3", "gpRef": "§10 & §6",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "disputes"],
  "alsoCh": ["N3"],
  "stem": "A validator is found to have guaranteed a report that turned out to be bad. What does JAM itself do to them?",
  "stemZh": "某位 validator 被認定擔保了一份後來被判定為錯誤的 report。JAM 本身會對他做什麼？",
  "options": [
   "It records their key in an offenders set and zeroes their entry at the next epoch change, so they can no longer author or sign; the actual slashing is left to the staking layer above",
   "It deducts a fixed penalty from their balance immediately and removes them from the validator set within the same block, so the punishment lands before the next block is authored",
   "It marks them for a probation period during which their signatures still count but carry less weight, and removes them only if they offend a second time within the epoch",
   "It reassigns all of their pending work to other cores and bars them from guaranteeing again, while leaving their ability to assure and audit completely untouched"
  ],
  "optionsZh": [
   "把他的金鑰記進 offenders 集合，並在下一次 epoch 換屆時把他的項目歸零，使他不能再出塊或簽署；實際的沒收則交給上層的 staking 機制處理",
   "立刻從他的餘額扣除一筆固定罰金，並在同一個區塊內把他移出 validator 集合，讓懲罰在下一個區塊出塊之前就落地",
   "把他標記為觀察期，期間他的簽章仍然算數但權重較低，只有在同一個 epoch 內再犯才會被移除",
   "把他所有待處理的工作重新指派到其他 core，並禁止他再擔保，但完全不影響他背書與稽核的能力"
  ],
  "answer": 0,
  "explanation": "JAM 的分工很清楚：**它負責「認定」，不負責「沒收」**。被認定的 validator 其 Ed25519 金鑰進入 ψ_O（offenders 集合），到下一個 epoch 換屆時，Φ 會把他那整筆 validator key 換成全零——從此不能出塊、不能擔保、不能背書。§10 明說 JAM 自己不動餘額，實際的 slash 由上層的 staking 系統依這份紀錄執行。這個分層是刻意的：JAM 是一台通用機器，質押與代幣經濟屬於建在它上面的 service。另外要注意歸零是**就地**進行而不是移除，所以 validator 集合的長度與索引不會位移。",
  "optNotes": [
   "認定與紀錄由 JAM 做、實際沒收由上層做——這個分層是刻意的。",
   "JAM 不會直接扣餘額，§10 明說它不處理罰金。",
   "沒有觀察期或權重折減這種機制，認定即失效。",
   "金鑰歸零之後所有角色都做不了，不是只擋擔保。"
  ],
  "trap": "JAM 只認定並歸零金鑰；扣錢是上層 staking 的事。"
 },
 {
  "id": "n6-why-two-thirds",
  "ch": "N6", "section": "§11.2; §17", "gpRef": "§11 & §17",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "thresholds"],
  "stem": "The availability threshold is set above two thirds of validators. Why not a simple majority?",
  "stemZh": "可得性門檻訂在超過三分之二的 validator。為什麼不是簡單多數就好？",
  "options": [
   "Because the security model assumes up to a third may be dishonest, so only a two-thirds threshold guarantees that at least some honest validators are among those attesting",
   "Because a simple majority would be reached too quickly, and the protocol needs the extra delay so that auditors have time to fetch the data before accumulation begins",
   "Because the erasure coding needs exactly two thirds of the shards to reconstruct, so the threshold is a direct consequence of the coding rate that was chosen",
   "Because a simple majority could be split evenly on an even-sized validator set, and two thirds is the smallest fraction that avoids the possibility of a tie"
  ],
  "optionsZh": [
   "因為安全模型假設最多可能有三分之一不誠實，只有三分之二的門檻才能保證表態者當中至少有一部分是誠實的",
   "因為簡單多數會太快達成，協定需要這段額外延遲，好讓 auditor 在 accumulation 開始前有時間取得資料",
   "因為 erasure coding 恰好需要三分之二的碎片才能重建，所以這個門檻是所選編碼率的直接結果",
   "因為在偶數大小的 validator 集合上簡單多數可能剛好對半，而三分之二是能避免平手的最小比例"
  ],
  "answer": 0,
  "explanation": "門檻來自**拜占庭容錯的標準假設**：最多有 1/3 的參與者可能作惡。若只要求簡單多數，一群串通的不誠實 validator 有可能自己湊出過半、宣稱資料可得，但實際上誰也沒有留著它——結果是 auditor 事後拿不到輸入，稽核失效。要求超過 2/3 就保證了表態的人裡面必定有誠實的一群，而誠實的人不會謊稱自己持有碎片。順帶注意 erasure coding 的重建門檻是 **1/3** 不是 2/3——兩個數字都出現在同一段機制裡，但意義不同，很容易記混。",
  "optNotes": [
   "1/3 作惡的假設決定了 2/3 的門檻，這是拜占庭容錯的標準推論。",
   "門檻不是為了製造延遲；稽核時間由別的機制安排。",
   "重建只需要 1/3 的碎片，這與表態門檻是兩個不同的數字。",
   "避免平手不是理由；三態判決另有自己的門檻設計。"
  ],
  "trap": "背書門檻 2/3（因為 1/3 可能作惡）；重建門檻 1/3（因為編碼率）。兩者別搞混。"
 },
 {
  "id": "n6-chain-of-guarantees",
  "ch": "N6", "section": "§11; §17; §10", "gpRef": "§11, §17 & §10",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "security"],
  "alsoCh": ["N5"],
  "stem": "Availability, auditing and disputes are three separate mechanisms. What breaks if you remove availability and keep the other two?",
  "stemZh": "可得性、稽核、爭議是三套獨立的機制。如果拿掉可得性、只留另外兩套，會壞在哪裡？",
  "options": [
   "Auditing loses its input: an auditor asked to re-run a report may find the data gone, so a dishonest guarantor could simply withhold it and never be contradicted",
   "Disputes lose their evidence: a verdict could still be reached but nobody could prove which guarantors signed the report, so no offender could ever be identified",
   "Auditing loses its randomness: without assurances there is nothing for the selection function to draw on, so auditors could no longer be chosen unpredictably",
   "Disputes lose their bound: without availability there is no timeout, so a report could stay pending forever and its dispute window would never actually close"
  ],
  "optionsZh": [
   "稽核失去輸入：被要求重跑某份 report 的 auditor 可能發現資料已經不見，於是不誠實的 guarantor 只要把資料藏起來就永遠不會被反駁",
   "爭議失去證據：判決仍然做得出來，但沒有人能證明是哪些 guarantor 簽署了該 report，因此永遠無法認定任何 offender",
   "稽核失去隨機性：沒有 assurance 就沒有東西可供抽選函數取用，auditor 也就無法再被不可預測地選出",
   "爭議失去邊界：沒有可得性就沒有逾時機制，一份 report 可能永遠處於待處理狀態，它的爭議窗口也就永遠不會關閉"
  ],
  "answer": 0,
  "explanation": "三者是一條**依序相扣的鏈**：可得性保證資料救得回來 → 稽核靠那份資料重跑 → 爭議處理重跑後的歧見。抽掉第一環，第二環就懸空：auditor 被抽中去查某份 report，卻拿不到原始輸入，於是「查不出錯」與「沒有錯」變得無法區分。更糟的是這給了作惡者一個乾淨的策略——**簽一個假結果，然後把資料丟掉**。這正是為什麼 accumulate 必須等到 available 之後才發生：先確保查得了，再讓它生效。guarantor 的簽章一直都在 report 裡（0.8.0 起連簽章一起存進 ρ），所以證據不是問題。",
  "optNotes": [
   "沒有資料就無法重跑，「藏起資料」會變成一個乾淨的作弊策略。",
   "guarantor 的簽章存在 report 與 ρ 裡，證據不會因為缺少可得性而消失。",
   "auditor 的抽選用的是狀態裡的 entropy，與 assurance 無關。",
   "逾時是 ρ 自己的規則（U = 5 個時槽），不依賴可得性機制存在。"
  ],
  "trap": "可得性 → 稽核 → 爭議是一條鏈；斷第一環，作惡者只要丟掉資料就贏了。"
 },
 {
  "id": "n6-two-da-basic",
  "ch": "N6", "section": "§11.2; §14", "gpRef": "§11 & §14",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "availability"],
  "stem": "JAM keeps two different kinds of data available, with different lifetimes. What are they for?",
  "stemZh": "JAM 讓兩種不同的資料保持可得，而且保存期限不同。它們各自的用途是什麼？",
  "options": [
   "One holds the package bundle so auditors can re-run the work; the other holds the exported segments so later packages can import them, and needs to last much longer",
   "One holds the package bundle for auditors; the other holds a copy of the chain state so that a node which falls behind can rebuild it without replaying every block",
   "One holds the data for the current epoch and the other holds an archive of previous epochs, so the split is by age rather than by what the data is used for",
   "One holds data for cores that are currently busy and the other for cores that are idle, so that a core can be brought back into service without refetching anything"
  ],
  "optionsZh": [
   "一種保存 package bundle，好讓 auditor 能重跑那份工作；另一種保存匯出的 segment，好讓後續的 package 能匯入它們，而且必須保存久得多",
   "一種為 auditor 保存 package bundle；另一種保存鏈上狀態的副本，好讓落後的節點不必重放每個區塊就能重建狀態",
   "一種保存當前 epoch 的資料、另一種保存先前 epoch 的封存，所以區分依據是資料的新舊而非用途",
   "一種保存目前忙碌中的 core 的資料、另一種保存閒置 core 的，好讓一個 core 重新投入服務時不必重新抓取任何東西"
  ],
  "answer": 0,
  "explanation": "兩種可得性對應**兩種不同的需求**。**Audit DA**：保存 work-package bundle，供 auditor 事後重跑用；它只需要撐過稽核窗口，時間相對短。**Import/Segment DA**：保存匯出的 segment，供**後續的 work-package** 匯入使用；因為接力可能隔很久才發生，它必須保存得久得多（規格上是 28 天）。分開設計的理由很直接：兩者的讀取者不同（auditor vs 後續的 package）、保存期限差很多，混在一起就得一律用長的那個期限，成本會浪費在不需要長存的 bundle 上。",
  "optNotes": [
   "稽核用的 bundle 與接力用的 segment，讀者與期限都不同，所以分開處理。",
   "JAM 的可得性層不保存狀態副本；狀態同步是另一回事。",
   "區分依據是用途而不是新舊；兩種資料在同一時間都可能存在。",
   "core 沒有閒置與否的資料區分；可得性是針對 package 而非 core。"
  ],
  "trap": "Audit DA（給 auditor、短）vs Segment DA（給後續 package、28 天）。"
 },
]
