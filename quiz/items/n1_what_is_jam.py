# -*- coding: utf-8 -*-
"""基礎套題 N1：JAM 是什麼。只考主幹——讀過 GP 但不深入的人要答得出來。"""

ITEMS = [
 {
  "id": "n1-what-problem",
  "ch": "N1", "section": "§1 Introduction", "gpRef": "§1",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "overview"],
  "stemZh": "一句話說，JAM 想成為什麼？",
  "optionsZh": [
   "一條能為許多獨立 service 執行大量運算的鏈：多數工作由少數 validator 在主鏈之外平行完成，鏈上只對結果達成共識",
   "一個更快的支付網路，用平行執行把每秒轉帳筆數推高到超過單一機器能簽署的量",
   "一個通用的 rollup host，只負責保存其他鏈的資料並定期公布它們的 state root，本身不對那些資料做任何運算",
   "一條隱私鏈，每筆運算都要先產生零知識證明才會被接受，因此 validator 從不需要看見自己正在確認的工作的輸入"
  ],
  "stem": "In one sentence, what does JAM set out to be?",
  "options": [
   "A single chain that runs a large amount of computation for many independent services, by having most work done by a few validators in parallel off the main chain and only the results agreed on-chain",
   "A faster payment network that settles transfers between accounts, using parallel execution to raise the number of transfers each second above what a single machine could sign",
   "A general-purpose rollup host that stores the data of other chains and periodically posts their state roots, without running any computation of its own on that data",
   "A privacy-preserving chain where every computation is proved in zero knowledge before it is accepted, so validators never see the inputs to the work they are agreeing on",
  ],
  "answer": 0,
  "explanation": "JAM 的核心主張是「把重活搬到鏈外做、只把結果放上鏈」。§1 描述它是一個能承載大量獨立服務的單一鏈，作法是讓少數被指派的 validator 在**core** 上平行執行工作（in-core），主鏈只負責對結果達成共識（on-chain）。這個分工是理解後面所有章節的地基：work-package 在 core 上被 refine、產出的 work-report 才上鏈、再由 accumulate 寫進狀態。JAM 不是支付網路（它沒有內建的轉帳語意，service 才決定自己在做什麼），也不是只存資料的 rollup host（它真的執行計算），更不是 zk 鏈（它靠重跑與稽核而不是證明來確保正確）。",
  "optNotes": [
   "in-core 平行執行、on-chain 只收結果——這正是 JAM 全篇的架構主軸。",
   "JAM 沒有內建轉帳語意；要不要做支付是各個 service 自己的事。",
   "rollup host 只存資料不算，JAM 的 core 是真的在跑 service 的程式碼。",
   "JAM 用「重跑 + 稽核」確保正確性（ELVES），不是用零知識證明。",
  ],
  "trap": "一句話版本：少數人平行做、全體只對結果達成共識。",
 },
 {
  "id": "n1-in-core-vs-on-chain-basic",
  "ch": "N1", "section": "§1; §4 Overview", "gpRef": "§1 & §4",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "in-core"],
  "stemZh": "「in-core」執行的工作與「on-chain」執行的工作，差別在哪裡？",
  "optionsZh": [
   "in-core 的工作只由被指派的少數 validator 執行、其他人不重跑；on-chain 的工作屬於狀態轉移的一部分，每個節點都會執行",
   "in-core 的工作跑在 PVM 裡，on-chain 的工作直接跑在 validator 自己的硬體上，所以前者必須計量而後者不必",
   "in-core 是任何碰到 service 自有 storage 的工作，on-chain 是任何碰到餘額的工作，界線跟著寫入哪一塊狀態走",
   "in-core 發生在區塊被封印之前、on-chain 發生在它被 finalize 之後，兩者的差別是時間先後而不是由誰執行"
  ],
  "stem": "What is the difference between work done 'in-core' and work done 'on-chain'?",
  "options": [
   "In-core work is executed by a small assigned subset of validators and is not re-run by everyone; on-chain work is part of the state transition and every node executes it",
   "In-core work runs inside the PVM while on-chain work runs natively on the validator's own hardware, which is why in-core work must be metered but on-chain work need not be",
   "In-core work is anything touching a service's own storage, while on-chain work is anything touching balances, so the split follows which part of the state is written",
   "In-core work happens before a block is sealed and on-chain work happens after it is finalized, so the two differ by when in the block's life they run rather than by who runs them",
  ],
  "answer": 0,
  "explanation": "分界線是**誰執行**，不是執行在哪種硬體上、也不是碰哪塊狀態。in-core：一份 work-package 被指派到某個 core，只有該 core 的少數 guarantor 真的跑它（refine），其他人不重跑——這正是 JAM 能承載大量計算的原因，因為總算力不再被「每個人都要跑一遍」綁住。on-chain：accumulate 屬於狀態轉移的一部分，**每個節點都會執行**，所以它必須便宜且結果小。少數人執行帶來的風險，由稽核機制補上：auditor 會隨機抽樣重跑 in-core 的結果，錯了就進 disputes。兩者都在 PVM 裡跑，所以「native vs VM」的說法不成立。",
  "optNotes": [
   "分界是「少數人跑 vs 全體跑」，而稽核正是為了補上前者的信任缺口。",
   "refine 與 accumulate 都在 PVM 裡執行，不存在誰跑原生碼的差別。",
   "碰哪塊狀態不是判準；refine 根本不能寫狀態，accumulate 才能。",
   "時間先後不是判準，兩者都發生在同一個區塊的處理過程中。",
  ],
  "trap": "in-core = 少數人跑、要靠稽核擔保；on-chain = 全體跑、所以必須小。",
 },
 {
  "id": "n1-vs-ethereum-model",
  "ch": "N1", "section": "§2 Previous Work; §4.9", "gpRef": "§2 & §4",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "comparison"],
  "alsoCh": ["N4"],
  "stemZh": "與 Ethereum 相比，JAM 把使用者請求所執行的程式碼放在哪裡？這個選擇帶來什麼後果？",
  "optionsZh": [
   "Ethereum 的每次合約呼叫都由每個節點重跑，吞吐因此被單一機器綁住；JAM 讓 service 最重的那一步只在一個 core 上執行，所以增加 core 就能增加容量",
   "Ethereum 在依 shard 選出的節點子集上執行合約，JAM 則到處都跑，用吞吐換取一個不需要稽核層的簡單安全論證",
   "兩者都是全網重跑，差別只在 JAM 的虛擬機是暫存器式而非堆疊式，這才是它每條指令更快的原因",
   "Ethereum 把合約程式碼存在鏈上，JAM 則完全存在鏈外，所以 JAM 的容量來自於狀態裡從不需要支付程式碼的儲存成本"
  ],
  "stem": "Compared with Ethereum, where does JAM put the code that a user's request runs, and what follows from that choice?",
  "options": [
   "Ethereum re-executes every contract call on every node, so throughput is bounded by one machine; JAM runs a service's heavy step on one core only, so adding cores adds capacity",
   "Ethereum runs contracts on a subset of nodes chosen per shard while JAM runs them everywhere, trading throughput for a simpler security argument that needs no auditing layer",
   "Both re-execute everywhere, and the difference is only that JAM's virtual machine is register-based rather than stack-based, which is what makes it faster per instruction",
   "Ethereum stores contract code on-chain while JAM stores it off-chain entirely, so JAM's capacity comes from never having to pay for code storage in the state",
  ],
  "answer": 0,
  "explanation": "這題問的是**擴展性從哪裡來**。Ethereum 的每一次合約呼叫都由全網每個節點重跑，因此整條鏈的處理能力大約等於一台機器的能力——加節點只會增加安全性，不會增加吞吐。JAM 把最重的那一步（refine）放在 core 上，一份 work-package 只由被指派到該 core 的少數 guarantor 執行；core 數量增加，總能力就跟著增加。代價是「只有少數人跑過」這件事本身不可信，所以必須另外付出稽核成本（erasure coding 讓資料可重建、auditor 隨機重跑、disputes 處理歧見）。register-based VM 與 code 存哪裡都是次要差異，不是擴展性的來源。",
  "optNotes": [
   "全網重跑 vs 單一 core 執行，正是「加 core 就加容量」的來源。",
   "方向反了，而且 JAM 需要稽核層恰恰因為它不是全網重跑。",
   "PVM 是 register-based 沒錯，但那影響的是單指令效率，不是擴展性。",
   "service 的 code 一樣存在狀態裡（透過 preimage），不是存在鏈外。",
  ],
  "trap": "擴展性來自「不是每個人都跑」，代價是必須額外買一套稽核機制。",
 },
 {
  "id": "n1-name-corejam",
  "ch": "N1", "section": "§1", "gpRef": "§1",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "naming"],
  "stemZh": "JAM 這個名字由兩個字組成。是哪兩個字，它們又指什麼？",
  "optionsZh": [
   "Join 與 Accumulate——把 in-core 的結果帶回鏈上的兩個階段，也是每個 service 都必須定義的操作",
   "Just Another Machine——一個刻意平凡的名字，用來表明這條鏈提供的是通用虛擬機而非任何特定應用的功能集",
   "Justified Availability Merkleization——一份 work-report 的輸出要能寫進狀態之前必須滿足的三個性質",
   "Jump And Map——PVM 在 RISC-V 之上額外加入的兩個原語，讓 service 能定址被匯入自己 core 的 segment"
  ],
  "stem": "The name JAM comes from two words. Which pair, and what do they refer to?",
  "options": [
   "Join and Accumulate — the two stages that bring in-core results back on-chain, which are the operations every service must define",
   "Just Another Machine — a deliberately plain name signalling that the chain offers a general virtual machine rather than any application-specific feature set",
   "Justified Availability Merkleization — the three properties a work-report must satisfy before its outputs may be written into the state",
   "Jump And Map — the two primitives the PVM adds on top of RISC-V so that a service can address the segments imported into its core",
  ],
  "answer": 0,
  "explanation": "JAM = **Join-Accumulate Machine**。這兩個字對應把 in-core 的結果帶回鏈上的兩個階段，源頭是更早的 CoreJam 模型（RFC-31）裡的 Collect-Refine-Join-Accumulate 四段。實際落到 Gray Paper 裡，真正在鏈上執行的只有 accumulate 這一段（join 的角色被吸收進 accumulate 的批次處理），refine 則在 core 上執行，collect 屬於鏈下的收集行為。記住這個名字的來源有實際好處：它直接提醒你「一份工作有 in-core 與 on-chain 兩段」，而這正是整份規格的骨架。",
  "optNotes": [
   "Join-Accumulate 出自 CoreJam 的四段模型，正是把結果帶回鏈上的那兩段。",
   "名字不是這樣來的；JAM 確實提供通用 VM，但那不是命名的由來。",
   "這三個詞都是 JAM 的概念，但湊起來不是名字的來源。",
   "PVM 沒有這兩個特殊 primitive，它是 RV64EM 的精簡子集。",
  ],
  "trap": "Join-Accumulate Machine，源自 CoreJam 的 Collect-Refine-Join-Accumulate。",
 },
{
  "id": "n1-why-one-chain",
  "ch": "N1", "section": "§1; §2 Previous Work", "gpRef": "§1 & §2",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "architecture"],
  "stem": "Polkadot gets its capacity from many parallel chains. JAM keeps a single chain and gets capacity from cores instead. What does that buy?",
  "stemZh": "Polkadot 的處理能力來自許多條平行的鏈，JAM 卻只保留單一條鏈、改用 core 來取得能力。這樣做買到了什麼？",
  "options": [
   "One shared state and one set of rules, so services can call and pay each other synchronously instead of passing asynchronous messages between separate chains",
   "A smaller validator set, because a single chain needs fewer validators than many parallel chains and can therefore reach agreement in fewer rounds",
   "Freedom from erasure coding, since with one chain every validator already holds the whole state and no data needs to be reconstructed from shards",
   "Cheaper finality, because a single chain can finalize on every block whereas parallel chains must wait for a shared relay chain to finalize them together"
  ],
  "optionsZh": [
   "單一份共享狀態與單一套規則，因此 service 之間可以同步互相呼叫與付費，不必在不同鏈之間傳遞非同步訊息",
   "較小的 validator 集合，因為單一條鏈需要的 validator 比許多平行鏈少，達成共識的輪數也因此較少",
   "不需要 erasure coding，因為只有一條鏈時每個 validator 本來就持有完整狀態，沒有資料需要從碎片重建",
   "更便宜的 finality，因為單一條鏈可以每塊都 finalize，而平行鏈必須等共用的 relay chain 一起把它們 finalize"
  ],
  "answer": 0,
  "explanation": "差別在**狀態是不是同一份**。Polkadot 的每條 parachain 有自己的狀態，跨鏈只能靠非同步訊息（XCMP），這讓「A 呼叫 B 並拿回結果」這種再普通不過的事變得困難。JAM 只有一條鏈、一份狀態 σ，所有 service 都住在同一個 δ 裡，因此可以同步互動、互相轉帳。能力則由 core 提供：core 不是獨立的鏈，而是同一條鏈上平行執行的運算單位，它們的結果最後都回到同一份狀態。至於 erasure coding，正因為 in-core 的資料沒有全網保存，**才更需要**它；validator 集合大小與 finality 都不是這個選擇的產物。",
  "optNotes": [
   "一份共享狀態才能讓 service 同步互相呼叫，這是單鏈換來的核心好處。",
   "validator 數量與鏈的數目無關，JAM 的 core 數還是綁在 |κ|/3 上。",
   "方向反了：正因為只有少數人持有 in-core 資料，才需要 erasure coding。",
   "finality 由 Grandpa 負責，跟「一條鏈或多條鏈」不是同一個維度。"
  ],
  "trap": "單鏈買到的是「同一份狀態」；能力來自 core，而 core 不是另一條鏈。"
 },
 {
  "id": "n1-what-is-a-core",
  "ch": "N1", "section": "§4.9 The Core Model", "gpRef": "§4",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "core"],
  "alsoCh": ["N4", "N5"],
  "stem": "What is a 'core' in JAM?",
  "stemZh": "JAM 裡的 core 是什麼？",
  "options": [
   "A slot of parallel computation on the one chain: a few validators are assigned to it, they run the work sent there, and only their agreed result comes back on-chain",
   "A separate blockchain with its own state and its own validators, connected to the main chain by the same kind of bridge Polkadot uses for its parachains",
   "A physical CPU core on each validator's machine, so the core count is set by the hardware requirement the protocol places on validators",
   "A storage partition of the state, so that a service's data lives on one core and requests touching two services must be split across two cores"
  ],
  "optionsZh": [
   "同一條鏈上的一個平行運算位置：少數 validator 被指派到它、執行送進來的工作，只有他們一致同意的結果會回到鏈上",
   "一條擁有自己的狀態與自己 validator 的獨立區塊鏈，用 Polkadot 連接 parachain 的那種橋接方式接到主鏈",
   "每台 validator 機器上的一個實體 CPU 核心，因此 core 的數量由協定對 validator 的硬體要求決定",
   "狀態的一個儲存分區，所以一個 service 的資料住在某個 core 上，跨兩個 service 的請求必須拆成兩個 core 處理"
  ],
  "answer": 0,
  "explanation": "core 是**同一條鏈上的一個平行運算位置**，不是另一條鏈、不是硬體、也不是儲存分區。每個 core 在每個 rotation 被指派 3 名 guarantor，他們執行送到該 core 的 work-package（refine），產出的 work-report 才進入區塊。所以「加 core 就加運算能力」，而狀態始終只有一份——core 之間不需要橋接，因為它們的產出最後都寫進同一個 σ。名稱容易誤導：它借用 CPU 的比喻表達「平行的執行單位」，但一個 core 在任一時刻只掛一份工作（ρ[c] 至多一筆），而且能同時運作的 core 數受限於 |κ′|/3，因為每個 core 要 3 名 guarantor。",
  "optNotes": [
   "少數 validator 被指派、執行後只回傳結果——這正是 core 作為平行運算位置的定義。",
   "core 沒有自己的狀態、也不需要橋接，所有產出都回到同一份 σ。",
   "core 是協定層的抽象，與 validator 機器上有幾顆實體 CPU 無關。",
   "狀態沒有依 core 分區；service 全部住在同一個 δ 裡，這正是單鏈的好處。"
  ],
  "trap": "core = 平行的執行位置，不是平行的鏈；狀態永遠只有一份。"
 },
 {
  "id": "n1-validator-roles",
  "ch": "N1", "section": "§1; §11; §17", "gpRef": "§1, §11 & §17",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "roles"],
  "alsoCh": ["N6"],
  "stem": "The same validators take on several different jobs around one piece of work. Which description of guarantor, assurer and auditor is right?",
  "stemZh": "同一批 validator 會圍繞同一份工作扮演幾種不同的角色。關於 guarantor、assurer、auditor 的描述，哪一個是對的？",
  "options": [
   "A guarantor runs the work and signs for its result; an assurer states that it holds a piece of the data needed to re-run it; an auditor re-runs the work and publicly judges whether the result was right",
   "A guarantor proposes the work, an assurer executes it and signs the result, and an auditor stores the data long enough for anyone else to repeat the execution later if they wish",
   "A guarantor and an assurer are two names for the same role at different stages, while an auditor is a separate permissionless participant who need not be a validator at all",
   "A guarantor executes the work, an assurer finalizes the block containing it, and an auditor settles disputes by voting on which of two competing chains should survive"
  ],
  "optionsZh": [
   "guarantor 執行工作並為結果簽名；assurer 宣告自己持有重跑該工作所需的一份資料；auditor 重新執行該工作並公開判定結果是否正確",
   "guarantor 提出工作，assurer 執行它並為結果簽名，auditor 則把資料保存夠久，讓其他人日後想重跑時有東西可用",
   "guarantor 與 assurer 是同一個角色在不同階段的兩個名稱，而 auditor 是獨立的無許可參與者、不必是 validator",
   "guarantor 執行工作，assurer 為含有它的區塊定案，auditor 則透過投票決定兩條競爭的鏈哪一條該存活來解決爭議"
  ],
  "answer": 0,
  "explanation": "三個角色對應一份工作的三個階段，而且**都是 validator 在做**。guarantor：被指派到某個 core，實際執行 refine 並在 work-report 上簽名——他是那份結果的擔保人。assurer：宣告自己持有該 work-package 的一份 erasure-coded shard；當超過 2/3 的 assurer 都這麼說，報告才算 available，意思是「這份資料救得回來」。auditor：隨機被抽中去重跑那份工作，公開判定結果對不對；判定不一致就進 disputes。三者環環相扣：沒有 assurer 的保證，auditor 拿不到重跑所需的資料；沒有 auditor，guarantor 的簽名就沒有制衡。finality 是 Grandpa 的事，不屬於這三個角色。",
  "optNotes": [
   "執行、持有資料、重跑判定——三個階段各對應一個角色，正是稽核鏈的骨架。",
   "順序反了：執行的是 guarantor，assurer 只宣告自己持有資料、不執行。",
   "三者是不同角色，而且 auditor 必須是 validator（由 VRF 隨機抽出）。",
   "區塊定案是 Grandpa 的工作，爭議也不是靠投票選鏈而是判定 report 對錯。"
  ],
  "trap": "guarantor 做、assurer 存、auditor 查；三者都是 validator。"
 },
 {
  "id": "n1-gp-structure",
  "ch": "N1", "section": "Gray Paper 全書結構", "gpRef": "§3–§14 & App. A–H",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "reading-guide"],
  "stem": "You open the Gray Paper for the first time. Which description of how it is laid out will help you find things?",
  "stemZh": "你第一次打開 Gray Paper。關於它的編排方式，哪一個描述能幫你找到東西？",
  "options": [
   "Chapters 3 to 13 walk the state transition component by component, chapter 14 onward covers what happens off-chain, and the appendices hold the machinery the chapters lean on",
   "The chapters are ordered by how a block is processed from start to finish, so reading them in order traces one block through the node exactly once, with the appendices covering the same ground in more detail",
   "Each chapter is self-contained and defines the notation it needs at the point of use, so any chapter can be read on its own without reference to the rest of the document",
   "The appendices are informative background only, so an implementation that follows chapters 3 to 14 is already complete and conformant without reading any of them"
  ],
  "optionsZh": [
   "第 3 到 13 章逐一走過狀態轉移的各個分量，第 14 章之後談鏈下發生的事，附錄則收放各章所倚賴的機制",
   "章節是按照一個區塊從頭到尾的處理順序排列的，所以照順序讀完就等於完整追蹤一個區塊走過節點一次，附錄則是同樣內容的細節版",
   "每一章都自成一體、在用到的地方各自定義所需記號，因此任何一章都可以不參照文件其他部分獨立閱讀",
   "附錄只是補充背景，所以一份實作只要照著第 3 到 14 章做就已經完整且合規，完全不必讀附錄"
  ],
  "answer": 0,
  "explanation": "把結構記住能省下大量翻找時間。**§3** 先把記號定義完（序列、字典、雜湊、簽章），後面所有章節都靠它；**§4** 給出全貌與狀態 σ 的分量清單；**§5–§13** 則逐一定義各分量怎麼轉移——header、Safrole、recent history、authorization、service accounts、disputes、reporting & assurance、accumulation、statistics；**§14 起**進入鏈下：work-package 的形狀、guaranteeing、availability、auditing。**附錄 A–H 是必要機制而非補充**：PVM（A）、host call（B）、codec（C）、state Merklization（D）、一般 Merklization（E）、shuffle（F）、Bandersnatch（G）、erasure coding（H）——沒有它們，正文的公式無法實作。章節順序**不等於**區塊處理順序（例如 disputes 在 §10、但處理時排在很前面）。",
  "optNotes": [
   "§3 記號、§4 全貌、§5–13 逐分量、§14+ 鏈下、附錄放機制——這是最實用的地圖。",
   "章節順序不是處理順序；例如 disputes 在 §10，但區塊處理時它排在 reporting 之前。",
   "記號集中在 §3，其他章大量沿用；沒有哪一章是可以完全獨立閱讀的。",
   "附錄是實作必需（PVM、codec、Merklization…），不是可略過的背景。"
  ],
  "trap": "附錄不是補充讀物，是正文公式的實作依據。"
 },
]
