# -*- coding: utf-8 -*-
"""基礎套題 N7：PVM 與 gas。"""

ITEMS = [
 {
  "id": "n7-what-is-pvm",
  "ch": "N7", "section": "§4.7; App. A", "gpRef": "§4 & App. A",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "pvm"],
  "stem": "What is the PVM, and why does JAM define one instead of reusing an existing virtual machine?",
  "stemZh": "PVM 是什麼？JAM 為什麼要自己定義一個，而不沿用既有的虛擬機？",
  "options": [
   "A small deterministic register machine based on RISC-V, defined precisely so that every node and every auditor executing the same program gets exactly the same result and gas cost",
   "A sandbox that isolates service code from the host, defined by JAM because existing virtual machines cannot prevent a program from reading memory belonging to another service",
   "A just-in-time compiler specification, defined by JAM so that service code can be translated to native instructions and run at speeds an interpreter could never reach",
   "A bytecode format designed for small program size, defined by JAM because service code must fit inside a work-package and existing formats are far too verbose for that"
  ],
  "optionsZh": [
   "一台以 RISC-V 為基礎的小型確定性暫存器機，被精確定義，好讓每個節點與每位 auditor 執行同一支程式時都得到完全相同的結果與 gas 花費",
   "一個把 service 程式碼與宿主隔離的沙箱，由 JAM 自行定義，因為既有的虛擬機無法阻止程式讀取屬於另一個 service 的記憶體",
   "一份即時編譯器規格，由 JAM 定義，好讓 service 程式碼能被翻譯成原生指令、跑出直譯器永遠達不到的速度",
   "一種為縮小程式體積而設計的位元碼格式，由 JAM 定義，因為 service 程式碼必須塞進 work-package，而既有格式對此太過冗長"
  ],
  "answer": 0,
  "explanation": "PVM 存在的理由是**確定性**，不是速度或體積。JAM 的安全模型建立在「同一份輸入重跑會得到同一份輸出」上——auditor 才有辦法反駁 guarantor。這要求執行語意與 gas 計費都被規格逐條釘死，不能有「依實作而異」的空間。既有的 VM 要嘛語意有未定義的角落、要嘛計費模型不適合，所以 GP 自己定義了一台以 RISC-V 的 RV64EM 為基礎的暫存器機。隔離、JIT、體積都是次要考量（JIT 甚至是允許的實作手法，只要結果一致）。",
  "optNotes": [
   "確定性是核心：重跑必須得到相同結果與相同 gas，稽核才成立。",
   "隔離是任何 VM 都能做到的，不足以構成自訂一台的理由。",
   "JIT 是實作選擇；規格關心的是結果一致而非執行速度。",
   "程式碼透過 preimage 進入狀態，體積不是設計 PVM 的動機。"
  ],
  "trap": "自訂 VM 是為了「重跑結果必須一致」，不是為了快或小。"
 },
 {
  "id": "n7-why-riscv",
  "ch": "N7", "section": "§4.7; App. A", "gpRef": "§4 & App. A",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "pvm"],
  "stem": "The PVM is based on RISC-V rather than on a bespoke instruction set. What does that buy?",
  "stemZh": "PVM 以 RISC-V 為基礎而不是自創一套指令集。這樣做買到了什麼？",
  "options": [
   "Existing compilers already target it, so services can be written in ordinary languages, and its register machine maps onto real hardware more directly than a stack machine",
   "Existing hardware can execute it directly without any translation layer, so a validator with a RISC-V processor runs service code at full native speed with no interpreter",
   "Existing RISC-V programs run unmodified, so software written for general-purpose operating systems can be deployed as a JAM service without being recompiled at all",
   "Existing formal proofs of the RISC-V specification carry over, so the PVM's determinism is inherited from that work rather than needing to be established separately"
  ],
  "optionsZh": [
   "既有的編譯器已經支援它，所以 service 可以用一般語言撰寫；而且暫存器機比堆疊機更直接對應到真實硬體",
   "既有硬體可以直接執行它、不需要任何翻譯層，所以配備 RISC-V 處理器的 validator 能以完整原生速度執行 service 程式碼、不必直譯",
   "既有的 RISC-V 程式可以原封不動執行，所以為一般作業系統寫的軟體不必重新編譯就能部署成 JAM service",
   "既有對 RISC-V 規格的形式化證明可以直接沿用，所以 PVM 的確定性繼承自那些成果，不需要另外建立"
  ],
  "answer": 0,
  "explanation": "兩個實際好處。**工具鏈**：LLVM 等既有編譯器已經能產生 RISC-V 程式碼，所以 service 可以用 Rust、C 這類一般語言寫，不必為了一套自創指令集重建整條工具鏈。**執行效率**：暫存器機的指令與真實 CPU 的暫存器一一對應，實作要做 JIT 或 AOT 翻譯時比堆疊機（例如 EVM）容易得多。但 PVM **不是** RISC-V：它是 RV64EM 的精簡子集，拿掉了密碼學與環境互動的指令，另外加上自己的計價與記憶體模型，所以既有的 RISC-V 程式不能直接跑。",
  "optNotes": [
   "既有工具鏈可用、暫存器機好翻譯，這是選 RISC-V 的兩個實際理由。",
   "PVM 是精簡子集加上自己的計價與記憶體模型，硬體無法直接執行。",
   "一般 RISC-V 程式依賴系統呼叫與完整指令集，不能原封不動部署。",
   "確定性來自 GP 自己的逐條定義，不是繼承自 RISC-V 的既有成果。"
  ],
  "trap": "PVM 是 RV64EM 的子集，不是 RISC-V 本身；好處在工具鏈與翻譯難度。"
 },
 {
  "id": "n7-what-gas-is-for",
  "ch": "N7", "section": "§4.7", "gpRef": "§4",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "gas"],
  "stem": "What is gas actually protecting in JAM?",
  "stemZh": "JAM 的 gas 實際上在保護什麼？",
  "options": [
   "The bound on how long execution may run, so that one service cannot consume a validator's time indefinitely and stall everyone else's work along with it",
   "The fairness of pricing between services, so that two services doing similar amounts of work end up paying similar amounts for the core time they consumed",
   "The integrity of the state, so that a service which runs out of resources cannot leave its storage half-written and inconsistent for the next block to read",
   "The privacy of a service's execution, so that observers cannot infer what a program did by measuring how long its accumulate step happened to take"
  ],
  "optionsZh": [
   "執行時間的上界，讓單一 service 無法無止盡地佔用 validator 的時間、連帶拖住其他所有人的工作",
   "service 之間定價的公平性，讓兩個做了差不多工作量的 service，最終為所消耗的 core time 付出差不多的代價",
   "狀態的完整性，讓資源耗盡的 service 不會留下寫到一半、不一致的 storage 給下一個區塊讀到",
   "service 執行過程的隱私，讓觀察者無法藉由測量 accumulate 步驟花了多久來推斷程式做了什麼"
  ],
  "answer": 0,
  "explanation": "gas 是**停機問題的實用解法**。沒有它，一支寫了無窮迴圈的 service 程式會讓執行它的節點永遠卡住——in-core 會拖垮那個 core，on-chain 更會讓整條鏈停擺，因為 accumulate 是每個節點都要跑的。gas 給每次執行一個上界，用完就中止（OOG）。定價公平性是次要的（實際計價還牽涉 core time 的分配）；狀態一致性靠的是 accumulate 的 checkpoint 與 collapse 機制而不是 gas；隱私則完全不在 JAM 的目標裡。",
  "optNotes": [
   "gas 給執行設上界，這是防止無窮迴圈拖垮節點的唯一手段。",
   "定價公平是附帶效果，gas 的首要任務是保證會停下來。",
   "半寫入的狀態由 checkpoint 與 collapse 處理，不是 gas 的職責。",
   "JAM 不提供執行隱私，狀態與程式碼都是公開的。"
  ],
  "trap": "gas 保護的是「一定會停下來」；一致性與定價是別的機制。"
 },
 {
  "id": "n7-determinism-requirement",
  "ch": "N7", "section": "App. A; §17", "gpRef": "App. A & §17",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "pvm", "audit"],
  "alsoCh": ["N6"],
  "stem": "The PVM has no instruction for reading a clock, generating randomness or opening a socket. What would go wrong if it did?",
  "stemZh": "PVM 沒有任何讀取時鐘、產生隨機數或開啟網路連線的指令。如果有的話會出什麼問題？",
  "options": [
   "Two honest nodes running the same program could reach different results, so an auditor's re-run would prove nothing and every disagreement would become unresolvable",
   "A service could reach outside the chain to fetch data, so the state would depend on external systems that the protocol has no way to hold accountable for their answers",
   "The gas cost of an instruction would depend on how long the outside world took to respond, so a basic block's price could no longer be computed before it runs",
   "A malicious service could exhaust the validator's file handles or sockets, so one program could degrade the machine for every other service scheduled after it"
  ],
  "optionsZh": [
   "兩個誠實節點跑同一支程式可能得到不同結果，於是 auditor 的重跑什麼也證明不了，任何歧見都變得無法裁決",
   "service 可以伸手到鏈外抓資料，於是狀態會依賴外部系統，而協定無從對那些系統給出的答案追究責任",
   "一條指令的 gas 成本會取決於外界回應的快慢，於是一個 basic block 的價格在執行之前就再也算不出來",
   "惡意的 service 可能耗盡 validator 的檔案描述子或連線，於是一支程式就能拖累排在它之後的其他所有 service"
  ],
  "answer": 0,
  "explanation": "根本問題是**確定性**。JAM 的整個正確性論證是「少數人執行、任何人可重跑檢查」；重跑要有意義，前提是同樣的輸入必然得到同樣的輸出。如果程式能讀時鐘或產生真隨機數，兩個誠實節點跑同一支程式就會得到不同結果——這時 auditor 說「我算出來不一樣」完全無法證明 guarantor 說謊，爭議機制也就失去判準。其他三個選項描述的後果都真實存在，但它們是**衍生的問題**；沒有確定性，稽核這一層直接崩塌。",
  "optNotes": [
   "誠實節點得到不同結果，稽核與爭議就失去判準——這是最根本的後果。",
   "外部依賴確實是問題，但它之所以致命是因為破壞確定性。",
   "計價可預測是重要的，但那是確定性在 gas 這個面向的表現。",
   "資源耗盡屬於沙箱層面的顧慮，不是禁止這些指令的主要理由。"
  ],
  "trap": "禁止這些指令是為了保住「重跑必然一致」——稽核的地基。"
 },
 {
  "id": "n7-host-calls-basic",
  "ch": "N7", "section": "App. B", "gpRef": "App. B",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "host-calls"],
  "stem": "If the PVM cannot touch the outside world, how does a service read its own storage or send value to another service?",
  "stemZh": "既然 PVM 碰不到外界，一個 service 要怎麼讀取自己的 storage 或轉帳給另一個 service？",
  "options": [
   "Through host calls: a special instruction hands control to the protocol, which performs the operation under its own rules and returns a result the program can read",
   "Through reserved memory regions: the protocol maps the service's storage into the address space, so reading it is an ordinary load and writing it an ordinary store",
   "Through the work-package: everything a service may read or write must be declared in the package up front, and the protocol applies the declared changes afterwards",
   "Through privileged instructions: the PVM has a second instruction set that only becomes available during accumulate and is otherwise treated as invalid opcodes"
  ],
  "optionsZh": [
   "透過 host call：一條特殊指令把控制權交給協定，由協定依自己的規則執行該操作，再回傳一個程式讀得到的結果",
   "透過保留的記憶體區段：協定把該 service 的 storage 映射進位址空間，因此讀取只是普通的 load、寫入只是普通的 store",
   "透過 work-package：一個 service 可以讀寫的東西必須事先全部宣告在 package 裡，協定事後再套用那些被宣告的變更",
   "透過特權指令：PVM 有第二套指令集，只在 accumulate 期間才可用，其餘時候一律視為非法的 opcode"
  ],
  "answer": 0,
  "explanation": "答案是 **host call**：程式執行 `ecalli` 這條指令，控制權交回協定，協定依規則完成操作（讀 storage、轉帳、建立 service…）再把結果放回暫存器，程式繼續跑。這個設計讓兩件事成立：**所有對外的效果都經過協定的規則**（權限、計價、驗證都在這一層執行），以及**動態成本被隔離在 host call 裡**——指令層因此可以維持靜態可計價。記憶體映射的作法會讓 storage 的存取繞過權限檢查；work-package 事先宣告則不可能，因為 accumulate 要寫什麼取決於執行結果。",
  "optNotes": [
   "把控制權交回協定執行、再回傳結果，這正是 host call 的形狀。",
   "記憶體映射會讓 storage 存取繞過權限與計價，協定無從介入。",
   "accumulate 要寫什麼取決於執行結果，不可能事先宣告。",
   "PVM 只有一套指令集；能不能用某個 host call 由 invocation 種類決定。"
  ],
  "trap": "host call 是「唯一的對外出口」，也是動態成本的統一入口。"
 },
 {
  "id": "n7-no-crypto-instructions",
  "ch": "N7", "section": "§4.7; App. B", "gpRef": "§4 & App. B",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "pvm"],
  "stem": "The PVM deliberately omits instructions for cryptographic operations. Does that mean a service cannot hash anything?",
  "stemZh": "PVM 刻意省略了密碼學運算的指令。這是否表示 service 沒辦法做雜湊？",
  "options": [
   "No — such operations are offered as host calls instead, which lets the protocol price them realistically rather than as some number of ordinary instructions",
   "No — a service can implement them in ordinary instructions, and the omission simply reflects that the protocol has no opinion on which primitives a service should use",
   "Yes — services are not expected to hash anything themselves, because every commitment a service needs is computed for it by the protocol during accumulation",
   "Yes — hashing inside a service would be non-deterministic across implementations, so the protocol forbids it and computes all digests outside the virtual machine"
  ],
  "optionsZh": [
   "不會——這類運算改以 host call 提供，讓協定能對它們做出貼近實際的定價，而不是折算成某個數量的普通指令",
   "不會——service 可以用普通指令自己實作，這個省略只是反映協定對 service 該用哪些原語沒有意見",
   "會——service 本來就不需要自己做雜湊，因為它需要的每一個承諾都由協定在 accumulation 期間代為計算",
   "會——在 service 內部做雜湊在不同實作之間會產生不確定性，所以協定禁止它，並在虛擬機外計算所有摘要"
  ],
  "answer": 0,
  "explanation": "省略指令不等於不能用——這些運算改由 **host call** 提供。理由是**計價**：一次 Blake2b 的實際成本遠高於一條普通指令，如果硬用普通指令實作，計價就得靠「大約等於幾百條指令」這種粗糙的折算，而且不同實作的效率差異會讓那個折算失準。做成 host call 之後，協定可以直接對它訂一個貼近實際成本的價格。當然 service 理論上仍可用普通指令自己寫一份雜湊實作，只是慢又貴——這正是設計要引導的方向。雜湊本身完全是確定性的，不存在不確定性的問題。",
  "optNotes": [
   "改以 host call 提供是為了能對真實成本定價，而不是為了禁止。",
   "自己用普通指令實作在技術上可行，只是慢又貴，設計刻意不鼓勵。",
   "service 當然會需要自己做雜湊，協定不會代勞。",
   "雜湊是完全確定性的運算，不確定性不是這裡的問題。"
  ],
  "trap": "拿掉指令是為了「能正確定價」，功能改由 host call 提供。"
 },
 {
  "id": "n7-memory-basic",
  "ch": "N7", "section": "§4.7; App. A", "gpRef": "§4 & App. A",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "pvm", "memory"],
  "stem": "The PVM's memory is paged, and touching an unmapped page raises a fault rather than killing the program outright. What does that make possible?",
  "stemZh": "PVM 的記憶體是分頁的，碰到未映射的頁會引發 fault 而不是直接殺掉程式。這讓什麼變得可能？",
  "options": [
   "Loading input on demand: a program can be started without every segment it might read already in memory, and the host maps a page only when it is actually touched",
   "Sharing memory between services: a faulting page can be resolved to a region another service owns, which is how two services exchange large values without copying",
   "Growing the stack without limit: a fault on the page below the stack is what tells the host to extend it, so a program need never declare how deep its recursion goes",
   "Recovering from bugs: a program that reads uninitialised memory gets a chance to handle the fault and continue, instead of being terminated for a simple mistake"
  ],
  "optionsZh": [
   "按需載入輸入：程式啟動時不必把所有可能讀到的 segment 都先放進記憶體，宿主只在某一頁真的被碰到時才映射它",
   "在 service 之間共享記憶體：出錯的那一頁可以被解析到另一個 service 擁有的區段，兩個 service 就是靠這個交換大型資料而不必複製",
   "無限制地擴張堆疊：堆疊下方那一頁的 fault 正是通知宿主延展它的信號，因此程式永遠不必宣告自己的遞迴有多深",
   "從 bug 中復原：讀到未初始化記憶體的程式有機會處理該 fault 並繼續執行，而不是因為一個簡單的錯誤就被終止"
  ],
  "answer": 0,
  "explanation": "**按需分頁讓「宣告很多、實際只碰一小部分」變成可行。** refine 可能宣告匯入上千個 segment，但實際執行往往只讀其中幾個；如果啟動前就得把全部塞進記憶體，work-package 會大到不切實際。page fault 是**可回復的退出理由**：宿主把那一頁映射進來，程式從中斷處繼續。這也是為什麼 fault 回報的是**頁對齊的位址**——那正好是宿主需要映射的單位。至於跨 service 共享記憶體，JAM 沒有這種機制（隔離是硬性的）；堆疊擴張走的是 `grow_heap` 這類 host call。",
  "optNotes": [
   "按需載入讓「宣告多、實際碰少」可行，這是 fault 可回復的主要價值。",
   "service 之間完全隔離，沒有共享記憶體的機制。",
   "堆疊與堆的擴張走 host call（0.8.0 的 grow_heap），不是靠 fault 觸發。",
   "fault 不是給程式自己處理的例外；它把控制權交給宿主。"
  ],
  "trap": "page fault 是可回復的，為的是按需載入輸入——不是錯誤處理機制。"
 },
 {
  "id": "n7-two-gas-budgets",
  "ch": "N7", "section": "§11.3; §12; §14", "gpRef": "§11, §12 & §14",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "gas"],
  "alsoCh": ["N5"],
  "stem": "refine and accumulate are given very different gas budgets. Why should the on-chain step get so much less?",
  "stemZh": "refine 與 accumulate 拿到的 gas 預算差距很大。為什麼鏈上那一步應該少那麼多？",
  "options": [
   "Because refine runs once on one core while accumulate runs on every node in the network, so the same amount of gas costs the system hundreds of times more on-chain",
   "Because refine is audited afterwards and accumulate is not, so accumulate must be kept small enough that any error it makes is cheap to detect and correct later",
   "Because refine works on data that is already available while accumulate must fetch what it needs from storage, and storage access is what the budget is really limiting",
   "Because refine is paid for by the submitter of the work-package while accumulate is paid for by the service itself, and services are expected to hold smaller balances"
  ],
  "optionsZh": [
   "因為 refine 只在一個 core 上執行一次，而 accumulate 在網路上的每個節點都要執行，所以同樣的 gas 量在鏈上讓整個系統付出數百倍的代價",
   "因為 refine 事後會被稽核而 accumulate 不會，所以 accumulate 必須小到即使出錯，事後偵測與修正的代價也很低",
   "因為 refine 處理的是已經備妥的資料，而 accumulate 必須從 storage 取用所需內容，而預算真正在限制的正是 storage 存取",
   "因為 refine 由 work-package 的提交者付費、accumulate 由 service 自己付費，而 service 通常被預期持有較小的餘額"
  ],
  "answer": 0,
  "explanation": "差別來自**誰在執行**。refine 只在一個 core 上由 3 名 guarantor 跑一次；accumulate 屬於狀態轉移，**網路上每個節點都要跑一遍**。所以同樣一單位的 gas，花在 accumulate 上對整個系統的真實成本是花在 refine 上的數百倍（大約等於節點數量的倍數）。這就是為什麼 refine 的預算（G_R）是數十億，而單份 report 的 accumulate 預算（G_A）只有一千萬——差了約三個數量級。這個比例不是任意的，它直接反映 JAM「in-core 做重活、on-chain 只收結果」的架構。",
  "optNotes": [
   "一個 core 跑一次 vs 全網每個節點都跑，成本差距約等於節點數量。",
   "accumulate 沒有被稽核，但那正是它必須簡單的原因之一，不是預算大小的來源。",
   "兩者都會存取資料；storage 存取本身不是預算差距的解釋。",
   "付費方不同確實存在，但預算的比例反映的是系統成本而非帳戶餘額。"
  ],
  "trap": "預算差三個數量級，因為 accumulate 的成本要乘上節點數。"
 },
]
