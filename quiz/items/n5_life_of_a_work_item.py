# -*- coding: utf-8 -*-
"""基礎套題 N5：一份工作的一生。主幹資料流。"""

ITEMS = [
 {
  "id": "n5-pipeline-order",
  "ch": "N5", "section": "§11; §12; §14", "gpRef": "§11, §12 & §14",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "pipeline"],
  "alsoCh": ["N4", "N6"],
  "stem": "Put the life of one piece of work in order, from a user handing it over to its effect landing in the state.",
  "stemZh": "把一份工作從使用者交出、到它的效果落進狀態為止的過程排出順序。",
  "options": [
   "A work-package is sent to a core; guarantors refine it into a work-report; the report enters a block; validators assure they hold its data; once enough do, it is accumulated",
   "A work-package enters a block; validators vote on whether to run it; the winning core refines it into a report; the report is accumulated and the data is discarded afterwards",
   "A work-package is refined by every validator; the results are compared and the majority result becomes a report; the report is accumulated once the block is finalized",
   "A work-package is accumulated first to reserve its gas; guarantors then refine it on a core; the report is written back and validators assure the result was correct"
  ],
  "optionsZh": [
   "work-package 被送到某個 core；guarantor 把它 refine 成 work-report；report 進入區塊；validator 宣告自己持有它的資料；當足夠多人宣告後，它才被 accumulate",
   "work-package 先進入區塊；validator 投票決定要不要執行它；勝出的 core 把它 refine 成 report；report 被 accumulate 之後資料就丟棄",
   "work-package 由每一位 validator 各自 refine；比對結果後以多數決產生 report；等區塊被 finalize 之後該 report 才被 accumulate",
   "work-package 先被 accumulate 以預留 gas；接著 guarantor 在 core 上 refine 它；report 寫回鏈上後由 validator 宣告結果正確"
  ],
  "answer": 0,
  "explanation": "五個階段，順序不能亂：**① 送到 core**——使用者把 work-package 交給某個 core（要通過該 core 的 authorizer 檢查）。**② refine**——被指派的 3 名 guarantor 在 core 上執行，產出小的 work-report。**③ 進區塊**——report 經 E_G 上鏈（此時還不生效）。**④ available**——validator 用 assurance 宣告自己持有 erasure-coded 的碎片，超過 2/3 才算數。**⑤ accumulate**——這時才真的執行 service 的鏈上邏輯、寫進狀態。第四步常被跳過理解，但它是整個安全模型的關鍵：**沒有可得性就無法稽核**。",
  "optNotes": [
   "送到 core → refine → 進區塊 → 湊到可得性 → accumulate，五步缺一不可。",
   "沒有「投票決定要不要跑」這一步；能不能跑由 authorizer 決定。",
   "只有被指派的 3 名 guarantor 執行 refine，不是全網重跑再多數決。",
   "accumulate 是最後一步；gas 的預留發生在 accumulate 當下，不是事前。"
  ],
  "trap": "「available」是獨立的一步，而且是稽核的前提，不是可有可無的細節。"
 },
 {
  "id": "n5-what-is-a-work-package",
  "ch": "N5", "section": "§14 Work Packages", "gpRef": "§14",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "work-package"],
  "stem": "What does a work-package contain?",
  "stemZh": "一份 work-package 裡面有什麼？",
  "options": [
   "An authorization token and the code that checks it, plus one or more work-items, each naming the service to run, the code to run and the payload to run it on",
   "A signed request from the user, the fee they are paying and the address of the service, with the service then deciding for itself what code to execute",
   "A compiled program and its full input data, with no reference to any service, since a package is executed on its own and its result is credited to the submitter",
   "A list of state keys the work will read and write, along with the code, so that conflicting packages can be detected before either of them is executed"
  ],
  "optionsZh": [
   "一個授權 token 與檢查它的程式碼，加上一或多個 work-item，每個 item 指明要執行的 service、要跑的程式碼、以及要處理的 payload",
   "一份使用者簽署的請求、他支付的費用、以及該 service 的位址；至於要執行什麼程式碼，則由該 service 自行決定",
   "一支編譯好的程式與它完整的輸入資料，不指涉任何 service，因為 package 是獨立執行的、結果歸屬於提交者",
   "一份這項工作會讀寫的 state key 清單以及程式碼，好讓互相衝突的 package 在任一方執行之前就被偵測出來"
  ],
  "answer": 0,
  "explanation": "work-package 的核心是 **authorization + 一串 work-item**。authorization 那部分回答「這個 core 憑什麼接受這份工作」——它帶一個 token 與一個 is-authorized 的程式（Ψ_I），由 core 先跑一次決定收不收。work-item 則是實際的工作單位，每個指明 service、code hash 與 payload，以及要匯入／匯出哪些 segment。注意它**沒有使用者簽名**（JAM 是 transactionless 的），付費模型也不是隨包附錢——core time 本身才是被爭奪的資源。也沒有預先宣告的讀寫集合，因為 refine 根本不能讀狀態。",
  "optNotes": [
   "授權加上一串 work-item，這就是 work-package 的兩個部分。",
   "package 不帶使用者簽名，JAM 沒有交易；能不能執行由 authorizer 決定。",
   "每個 work-item 都明確指名 service 與 code hash，不是獨立執行的程式。",
   "沒有讀寫集合宣告——refine 不能讀狀態，也就無從衝突。"
  ],
  "trap": "package = 授權 + work-item；沒有簽名、沒有讀寫集合。"
 },
 {
  "id": "n5-why-report-is-small",
  "ch": "N5", "section": "§11.1; §14", "gpRef": "§11 & §14",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "work-report"],
  "stem": "A work-package can be many megabytes, but the work-report that reaches the chain is capped at tens of kilobytes. Why the difference?",
  "stemZh": "一份 work-package 可以有好幾 MB，但真正上鏈的 work-report 卻被限制在幾十 KB。為什麼差這麼多？",
  "options": [
   "The package is the input that only the core needs to see; the report is the summary every node must store forever, so the two live under completely different budgets",
   "The package is compressed before it is hashed into the report, so the size difference is the compression ratio and the full data is still recoverable from the report",
   "The package includes debugging information that is stripped once refine has finished, leaving only the parts of the input the service actually read during execution",
   "The report holds only the parts of the package that changed the state, with unchanged inputs omitted because replaying them would produce no observable effect"
  ],
  "optionsZh": [
   "package 是只有 core 需要看到的輸入；report 則是每個節點都必須永久保存的摘要，兩者受完全不同的預算約束",
   "package 在被雜湊進 report 之前會先壓縮，所以大小差距就是壓縮比，完整資料仍可從 report 還原",
   "package 含有除錯資訊，refine 結束後會被剝除，只留下 service 執行期間真正讀取過的那些輸入",
   "report 只保留 package 中改變了狀態的部分，未改變的輸入被省略，因為重放它們不會產生可觀察的效果"
  ],
  "answer": 0,
  "explanation": "這是 JAM 整個架構的縮影：**輸入留在鏈外、結果才上鏈**。work-package bundle 的上限 W_B 約 13 MB——它只需要被該 core 的 guarantor 看到，以及被 erasure-code 分散給 validator 以備稽核。work-report 的上限 W_R = 48 KiB——它會進入區塊，每個節點都要處理與保存。這兩個數字差了近 300 倍，正好對應「少數人看大資料、全體只看小摘要」。report 也**不是**壓縮或裁剪過的 package：它是 refine 的**輸出**（各 work-item 的 digest），與輸入是不同的東西。",
  "optNotes": [
   "只有 core 看的輸入 vs 全體保存的摘要，W_B 與 W_R 差近 300 倍正是這個分工。",
   "report 是 refine 的輸出而不是壓縮過的輸入，無法從中還原 package。",
   "沒有「剝除除錯資訊」這種步驟；輸入與輸出是兩種不同的東西。",
   "report 不是 package 的子集；它是執行後產生的新資料。"
  ],
  "trap": "package 是輸入（W_B ≈ 13 MB）、report 是輸出（W_R = 48 KiB），不是同一份東西的兩種大小。"
 },
 {
  "id": "n5-what-available-means",
  "ch": "N5", "section": "§11.2 Assurance", "gpRef": "§11",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "availability"],
  "alsoCh": ["N6"],
  "stem": "A report sits in a block but cannot be accumulated until it becomes 'available'. What does available actually mean here?",
  "stemZh": "一份 report 已經在區塊裡，但要等到「available」之後才能被 accumulate。這裡的 available 究竟是什麼意思？",
  "options": [
   "That enough validators have said they hold a piece of the underlying data, so anyone who later wants to re-run the work can reconstruct its input from those pieces",
   "That the report has been checked by enough validators for correctness, so a supermajority has independently confirmed the result before it touches the state",
   "That the data has been published somewhere any node can download it on demand, so availability is a statement about a public endpoint rather than about validators",
   "That the block containing the report has been finalized by Grandpa, so the report can no longer disappear through a reorganization of the chain"
  ],
  "optionsZh": [
   "已經有足夠多的 validator 宣告自己持有底層資料的一份碎片，因此日後任何想重跑這份工作的人，都能從那些碎片重建出它的輸入",
   "這份 report 已被足夠多的 validator 檢查過正確性，也就是超級多數在它碰到狀態之前已獨立確認過結果",
   "資料已經發布在某個任何節點都能隨時下載的地方，所以可得性談的是一個公開端點而不是 validator",
   "含有該 report 的區塊已被 Grandpa 定案，因此這份 report 不會再因為鏈的重組而消失"
  ],
  "answer": 0,
  "explanation": "available 談的是**資料救不救得回來**，不是結果對不對。work-package 被 erasure-code 成碎片分給每位 validator，assurance 就是「我持有我那一份」的宣告；超過 2/3 的人這麼說，就代表即使部分節點離線或作惡，剩下的碎片仍足以重建原始輸入。**為什麼這是 accumulate 的前提**：JAM 的正確性靠 auditor 事後重跑，而重跑需要輸入；如果輸入救不回來，這份 report 就永遠無法被查核，等於沒有擔保。所以順序是「先確保查得了，再讓它生效」。",
  "optNotes": [
   "assurance 保證的是資料可重建，這正是事後稽核的前提。",
   "正確性由 auditor 事後重跑判定，assurance 完全不檢查結果對不對。",
   "資料是分散在 validator 手上的碎片，沒有任何公開端點的概念。",
   "finality 是 Grandpa 的事，與 available 是兩個獨立的條件。"
  ],
  "trap": "available = 資料救得回來（能被稽核），不是結果被驗證過。"
 },
 {
  "id": "n5-what-accumulate-does",
  "ch": "N5", "section": "§12 Accumulation", "gpRef": "§12",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "accumulate"],
  "stem": "When a report finally gets accumulated, what happens?",
  "stemZh": "當一份 report 終於被 accumulate 時，發生了什麼事？",
  "options": [
   "Each service named in the report runs its own on-chain code, seeing the refine results as input, and may write its storage, move balances or create services",
   "The report's outputs are copied verbatim into the service's storage by the protocol, without running any service code, which is why accumulation is cheap",
   "The report is re-executed on-chain by every node to confirm the guarantors' result, and only a matching result is written into the state",
   "The report is handed to the next block's author, who decides which of its outputs are worth applying and writes those into the state on the service's behalf"
  ],
  "optionsZh": [
   "report 裡指名的每個 service 執行自己的鏈上程式碼，把 refine 的結果當成輸入，並可以寫自己的 storage、轉移餘額或建立新的 service",
   "協定把 report 的輸出原封不動複製進該 service 的 storage，完全不執行任何 service 程式碼，這正是 accumulation 便宜的原因",
   "report 由每個節點在鏈上重新執行一次以確認 guarantor 的結果，只有結果相符時才寫進狀態",
   "report 被交給下一個區塊的出塊者，由他決定哪些輸出值得套用，並代表該 service 把那些寫進狀態"
  ],
  "answer": 0,
  "explanation": "accumulate 是 service **自己的鏈上程式碼**在跑，不是協定代勞。輸入是 refine 產出的 work-digest（包含結果 blob 或錯誤值），service 據此決定要做什麼——寫 storage、轉帳、建立新 service、呼叫 `yield` 產出一個對外的承諾。這一步每個節點都會執行，所以受 gas 嚴格約束（單份 report 上限 G_A、整塊上限 G_T）。也因此 accumulate **不會重跑 refine**：重跑是 auditor 的工作，而且只在 core 上抽樣進行，不是全網每塊都做。",
  "optNotes": [
   "service 自己的鏈上程式碼執行、可寫狀態——這就是 accumulate。",
   "協定不會代為複製輸出；要做什麼完全由 service 的程式碼決定。",
   "全網重跑 refine 正是 JAM 要避免的事；重跑是 auditor 抽樣做的。",
   "出塊者沒有選擇權，accumulate 依規則進行、每個節點結果一致。"
  ],
  "trap": "accumulate = service 的鏈上邏輯在跑；它不重跑 refine。"
 },
 {
  "id": "n5-why-authorizer",
  "ch": "N5", "section": "§8 Authorization", "gpRef": "§8",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "authorization"],
  "stem": "Before a core will work on a package, the package must satisfy that core's authorizer. What problem does that solve?",
  "stemZh": "在 core 願意處理一份 package 之前，該 package 必須通過該 core 的 authorizer。這解決了什麼問題？",
  "options": [
   "Core time is scarce and unpriced at submission, so without a gate anyone could flood a core with work; the authorizer is where the right to use a core is decided",
   "Packages may contain arbitrary code, so without a gate a malicious package could escape the virtual machine; the authorizer is where the code is checked for safety",
   "Cores are assigned to validators at random, so without a gate a validator could refuse work; the authorizer is what forces a core to accept the packages sent to it",
   "Reports must be small, so without a gate an oversized package could produce an oversized report; the authorizer is where the size limits are actually enforced"
  ],
  "optionsZh": [
   "core time 稀缺、而且在提交當下並未被定價，所以沒有一道關卡的話任何人都能用工作淹沒一個 core；authorizer 正是決定「誰有權使用這個 core」的地方",
   "package 可能含有任意程式碼，所以沒有一道關卡的話惡意 package 可能逃出虛擬機；authorizer 正是檢查程式碼安全性的地方",
   "core 是隨機指派給 validator 的，所以沒有一道關卡的話 validator 可以拒絕工作；authorizer 正是強制 core 接受送來的 package 的機制",
   "report 必須夠小，所以沒有一道關卡的話過大的 package 會產生過大的 report；authorizer 正是實際執行大小限制的地方"
  ],
  "answer": 0,
  "explanation": "authorizer 是 **core time 的門禁**。JAM 沒有「提交時附上手續費」這種機制——core time 是被排程的稀缺資源，誰能用必須事先決定。作法是：每個 core 有一個 authorizer pool（最多 8 個 authorizer hash），package 必須帶一個能通過其中某個 authorizer 的 token，該 core 才會處理它。而 pool 的內容由具 assigner 特權的 service 透過 `assign` 管理——換句話說，**「誰能用這個 core」這個問題被外包給一個 service 去定義策略**，協定本身不規定商業模式。VM 的隔離、大小限制都是別的機制在管。",
  "optNotes": [
   "core time 稀缺且提交時未定價，authorizer 就是那道門禁。",
   "VM 的隔離由 PVM 本身保證，不需要事前檢查程式碼。",
   "authorizer 不強制 core 接受任何東西，它是在篩選而不是在強迫。",
   "大小限制由 W_R 等常數在 refine 期間執行，與授權無關。"
  ],
  "trap": "authorizer 管的是「誰有權用這個 core」，策略由 service 定義而非協定。"
 },
 {
  "id": "n5-segments-basic",
  "ch": "N5", "section": "§14", "gpRef": "§14",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "segments"],
  "stem": "Work-packages can import segments exported by earlier packages. Why is that needed at all, given refine cannot read the chain state?",
  "stemZh": "work-package 可以匯入先前 package 匯出的 segment。既然 refine 讀不到鏈上狀態，為什麼還需要這個機制？",
  "options": [
   "It is the only way one piece of in-core work can build on another's output, since results large enough to matter never reach the state for a later package to read",
   "It is how a package reads the current state indirectly, because segments are snapshots of state entries exported by the protocol at the end of each block",
   "It is a caching mechanism only, letting a package skip recomputing something, and any package could always recompute the imported data from its own inputs instead",
   "It is how a package receives its authorization token, which the previous package on the same core exports so that core time can be handed along a chain of work"
  ],
  "optionsZh": [
   "這是一份 in-core 工作能建立在另一份工作產出之上的唯一途徑，因為夠大而有意義的結果從來不會進入狀態、讓後續的 package 去讀",
   "這是 package 間接讀取當前狀態的方式，因為 segment 是協定在每個區塊結束時匯出的狀態條目快照",
   "這純粹是一種快取機制，讓 package 省下重算的功夫；任何 package 其實都能改用自己的輸入重新算出被匯入的資料",
   "這是 package 取得授權 token 的方式，由同一個 core 上前一份 package 匯出，好讓 core time 能沿著一連串工作傳遞下去"
  ],
  "answer": 0,
  "explanation": "關鍵在於**大的結果從來不上鏈**。refine 的輸出只有一小份 digest 進 work-report，真正龐大的產物（例如一段被處理過的資料）是以 **export segment** 的形式留在 core 的資料可得性層裡。如果後續的工作想接著處理它，唯一的辦法就是 import 那些 segment——因為它們既不在狀態裡（太大），refine 也讀不到狀態。這讓「一連串 in-core 工作接力」成為可能，而每一步都仍然是無狀態且可重跑的：import 的內容由 package 明確宣告，並靠 segment root 驗證。",
  "optNotes": [
   "大的結果不上鏈，所以接力只能靠 segment，這是 in-core 工作串接的唯一途徑。",
   "segment 不是狀態的快照，協定沒有這種匯出機制。",
   "被匯入的資料通常是別人算出來的，重算未必可能、也違背接力的目的。",
   "授權 token 由提交者提供，不是從前一份 package 傳遞下來的。"
  ],
  "trap": "segment 是 in-core 工作之間的接力棒；狀態太小裝不下這些結果。"
 },
 {
  "id": "n5-refine-failure",
  "ch": "N5", "section": "§11.1; §14", "gpRef": "§11 & §14",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "errors"],
  "stem": "One work-item inside a package runs out of gas during refine. What happens to that item and to the rest of the package?",
  "stemZh": "package 裡的某一個 work-item 在 refine 期間耗盡 gas。這個 item 與 package 的其餘部分會怎麼樣？",
  "options": [
   "That item's result becomes an error value that travels on-chain like any other result; the other items still run and the report is still perfectly valid",
   "The whole package is discarded and never becomes a report, because a package is treated as one unit of work that either completes or does not",
   "That item is retried on another core with a larger allowance, and only if it fails there too does the package as a whole get abandoned",
   "The report is produced but marked invalid, so it enters the block and is then rejected during accumulation before it can affect any service's state"
  ],
  "optionsZh": [
   "該 item 的結果變成一個錯誤值，像其他結果一樣被帶上鏈；其餘的 item 照樣執行，這份 report 仍然完全有效",
   "整份 package 被丟棄、永遠不會變成 report，因為 package 被當成一個工作單位，要嘛完成要嘛不完成",
   "該 item 會在另一個 core 上以更大的額度重試，只有在那裡也失敗，整份 package 才會被放棄",
   "report 仍然會產生但被標記為無效，於是它進入區塊、然後在 accumulation 階段被拒絕，不會影響任何 service 的狀態"
  ],
  "answer": 0,
  "explanation": "**失敗是一個「值」，不是一個「例外」。** work-digest 的 result 欄位可以是成功的 blob，也可以是錯誤集合 𝔼 裡的一員（out-of-gas、panic、輸出過大等）。它會照常隨 report 上鏈、被 accumulate 讀到，由 service 自己決定要重試、退款還是只記一筆帳。這樣設計有三個好處：service 知道失敗的原因；**同包裡其他 item 不受牽連**（否則一個服務失控就能吃掉同包所有人的工作）；而且失敗本身也可被稽核——auditor 重跑時比對的是「同樣的輸入是否同樣地失敗」。",
  "optNotes": [
   "失敗是可被 accumulate 讀到的值，其他 item 照跑、report 依然有效。",
   "package 不是全有全無；每個 item 各自有自己的結果。",
   "沒有跨 core 重試的機制；重試與否由 service 自己決定。",
   "report 不會因為含有失敗的 item 而無效，錯誤值是合法內容。"
  ],
  "trap": "refine 的失敗是資料不是例外；同包其他 item 不受影響。"
 },
]
