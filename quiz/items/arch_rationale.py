# -*- coding: utf-8 -*-
# Architecture & design rationale (interview portions 3 & 4) + chapter 14 basics + 0.7.2→0.8.0 delta summary
ITEMS = [
{
 "id": "arch-corejam-name",
 "ch": "ARCH", "section": "1.1 Nomenclature / RFC-31", "gpRef": "§1.1 & RFC-31 CoreJam",
 "difficulty": 1, "kind": "rationale", "tags": ["architecture", "history"],
 "stem": "Where does the name 'JAM' come from, and which stages of the original CoreJam model actually execute on-chain?",
 "options": [
  "From CoreJam (Polkadot Fellowship RFC-31), named after its Collect / Refine / Join / Accumulate model; only Join and Accumulate happen on-chain — Collect and Refine are off-chain/in-core — hence 'Join-Accumulate Machine', a complete protocol rather than RFC-31's scope-limited alteration",
  "From CoreJam (Polkadot Fellowship RFC-31), named after its Collect / Refine / Join / Accumulate model; Refine and Accumulate are the on-chain pair — Collect and Join are done off-chain by the package builder — hence 'Join-Accumulate Machine'",
  "From 'Just Another Machine', a nod to the Yellow Paper's naming; the collect / refine / join / accumulate pipeline was bolted on later by RFC-31, and all four stages run on-chain because a single validator set executes everything in consensus",
  "From 'Joint Availability Mechanism', after the erasure-coded D3L at its centre; RFC-31 already proposed this same complete protocol under the name CoreJam, and only Collect runs on-chain, since the chain must order incoming work-packages before the other three stages run in-core"
 ],
 "answer": 0,
 "optNotes": [
   "名字與分工都對上 §1.1：只有 Join 與 Accumulate 上鏈，縮寫才會是 Join-Accumulate Machine。",
   "分工顛倒：Refine 是 in-core 的高吞吐階段，Join 才是把 work-report 帶上鏈的那一步。",
   "四階段全在鏈上就是 §4.9.1 判定「is unfortunately not scalable」的 everybody-does-everything 模型。",
   "§1.1 明寫 RFC-31 是「incomplete, scope-limited alteration」，而 Collect 是 builder 在鏈下收集輸入。",
 ],
 "explanation": "GP §1.1：「An early, unrefined, version of this protocol was first proposed in Polkadot Fellowship RFC 31, known as CoreJam. CoreJam takes its name after the collect/refine/join/accumulate model of computation at the heart of its service proposition. While the CoreJam RFC suggested an incomplete, scope-limited alteration to the Polkadot protocol, JAM refers to a complete and coherent overall blockchain protocol.」四個階段的分界要背熟：Collect（builder 收集輸入）與 Refine（in-core 計算）在鏈下；Join（guarantee/assure 上鏈）與 Accumulate（狀態整合）在鏈上——名字正取自後面那一對。§4.9.1 則說明為何不能四階段全上鏈：「everybody does everything」式的 on-chain consensus model「is unfortunately not scalable」，JAM 引入 in-core 模型正是為了繞開它。",
 "trap": "面試「architecture」開場常問這題；順便提 RFC-31 的三種 service 想像：parachain validation、actor progression（CorePlay）、simple ordering。"
},
{
 "id": "arch-driving-factors",
 "ch": "ARCH", "section": "1.2–1.3 Driving Factors / Size-Coherency Antagonism", "gpRef": "§1.2–1.3",
 "difficulty": 2, "kind": "rationale", "tags": ["architecture", "rationale"],
 "stem": "The GP names five driving factors and a principle called 'size-coherency antagonism'. Which statement is correct?",
 "options": [
  "Factors: Resilience, Generality, Performance, Coherency, Accessibility; performance and coherency are antagonistic because causality is bounded by signal speed, so larger state-spaces become less coherent — JAM answers by pipelining a highly scalable, mostly-coherent element (in-core) into a synchronous, fully-coherent element (on-chain), replacing crude partitioning with 'cache affinity'",
  "Factors: Resilience, Generality, Performance, Coherency, Accessibility; the antagonism is between resilience and accessibility, since every additional validator adds a consensus round-trip and cheap access therefore forces a small set — JAM answers by pinning the validator set at 1,023 and pushing all further growth into off-chain roll-ups that settle asynchronously against the chain",
  "Factors: Resilience, Generality, Performance, Coherency, Accessibility; performance and coherency are antagonistic because signature verification does not parallelize, so throughput must be bought with weaker composability — JAM answers by fragmenting state into 341 causally-independent shards, each small enough to stay coherent, bridged by an asynchronous message queue",
  "Factors: Speed, Cost, Security, Decentralization, Simplicity; the antagonism is between decentralization and performance, because hardware requirements are barriers to entry to the validator set — JAM answers by fixing validator hardware at 16 cores / 64 GB / 8 TB and using SNARKs to compress the work, so coherency survives without any pipeline at all"
 ],
 "answer": 0,
 "optNotes": [
   "五項與對立的那一組（performance／coherency）都對，解法也正是 in-core → on-chain 的 pipeline 與 cache affinity。",
   "被點名對立的是第 3、4 項而非 resilience／accessibility；0.8.0 更已讓 validator 集合大小可變。",
   "把資訊理論論證換成「簽章無法平行化」；341 個因果獨立分片正是 GP 批評的 crude partitioning。",
   "五項名稱全不對；16 核/64 GB/8 TB 只是 §20 的假設硬體，GP 也明確以成本否定 SNARK 路線。",
 ],
 "explanation": "§1.2：(1) Resilience (2) Generality (3) Performance (4) Coherency (5) Accessibility；「items 3 and 4 are antagonistic according to an information theoretic principle… we shall name it size-coherency antagonism」，而前兩項是 Web3 的隱含前提——「we make an implicit assumption of the first two items」。§1.3：state-space 越大越不 coherent（受光速、電子與軟體延遲限制，元件間平均距離與變異都上升，因果解析時間發散）；現有可擴展系統（Polkadot、Cosmos、rollup）靠粗暴分割與非同步溝通，GP 以細菌分裂比喻批評之。JAM「pipelines a highly scalable, mostly coherent element to a synchronous, fully coherent element」，以類似多核心 CPU 共享 RAM 的「cache affinity」取代分割，目標是「avoiding the persistent fragmentation of state-space」——這就是「mostly-coherent trustless supercomputer」副標的由來。GP 也明確以成本為由否定 SNARK 路線（「Unlike with SNARK-based L2-blockchain techniques… this model draws upon crypto-economic mechanisms」）。",
 "trap": "與 SNARK rollup 的對比：§2 指 RISC-Zero 類證明比直接執行慢 6 萬倍以上、且傾向中心化。"
},
{
 "id": "arch-why-safrole",
 "ch": "ARCH", "section": "6 Safrole rationale", "gpRef": "§6 intro & §19",
 "difficulty": 2, "kind": "rationale", "tags": ["architecture", "safrole", "rationale"],
 "stem": "Why does JAM use Safrole (ticket-based, anonymous, ring-VRF) rather than a BABE-like VRF lottery?",
 "options": [
  "Safrole limits each 6-second slot to exactly one predetermined key-holder (near fork-free), keeps the identity of future slot authors anonymous until they seal (DoS resistance), and produces a high-quality unbiasable entropy pool; the best-chain rule additionally prefers chains with more ticket-sealed (vs fallback) ancestors",
  "Safrole's advantage is that several validators may win the same slot so a slot is never empty: the ring VRF lets each of them prove membership of γ_P, the resulting fork is resolved by whichever block reaches Grandpa first, and tickets are drawn afresh each slot from η_0 so that no author is predictable more than one slot ahead",
  "Safrole exists to take signatures off the hot path: the ticket is a plain hash preimage revealed at sealing, so checking a seal costs one hash rather than a VRF verification; anonymity comes from validators rotating their Ed25519 keys every epoch, and the entropy pool η is taken straight from the block hash since a hash is already uniform",
  "Safrole is a finality gadget sitting under Grandpa: it assigns each slot one author, who must then gather 2/3+1 pre-votes before the block may extend the chain, which is why JAM has no forks at all and needs no fork-choice rule; fallback keys are used only in the genesis epoch, before any tickets have accumulated"
 ],
 "answer": 0,
 "optNotes": [
   "三個目的都寫在 §6 intro：每 slot 恰一個作者、未來作者匿名、副產品是高品質 entropy，§19 再加 ticket 優先。",
   "這正是 Safrole 要修掉的 BABE 行為：γ_A 累積整個 epoch，交界一次排成 γ_S，每個 slot 只有一個 sealer。",
   "seal 是 Bandersnatch VRF 簽章、ticket 是 ring-VRF 證明；η′_0 取 Y(H_v) 正是因為 block hash 可被 grinding。",
   "Safrole 只管 block production，finality 歸 Grandpa；fallback F(k, η_2) 任何一次 ticket 不足的交界都會啟用。",
 ],
 "explanation": "§6 intro：「The chief purpose of a block production consensus mechanism is to limit the rate at which new blocks may be authored and, ideally, preclude the possibility of forks… Safrole limits the possible author of any block within any given six-second timeslot to a single key-holder… under normal operation, the identity of the key-holder of any future timeslot will have a very high degree of anonymity. As a side effect… we can generate a high-quality pool of entropy」——三個目的：近似無分叉、DoS 抗性、高品質 entropy。對照 BABE 的 VRF 抽籤會出現多個或零個 slot leader，Safrole 用 ticket 在前一個 epoch 就決定每個 slot 恰好一個作者；注意 GP 的用字是「ideally, preclude the possibility of forks」，並非完全無分叉，所以 §19 仍需 best-chain 規則——偏好「most ancestor blocks whose author used a slot-sealer ticket, rather than a fallback key」。Safrole 是 Sassafras 的簡化版（「To follow in the footsteps of Ethereum yellow paper」——簡單到能被多個獨立實作正確實現）。",
 "trap": "anonymity 來自 ring VRF：證明「我是 γ_P 中某人」而不揭露是誰；seal 時才用普通 VRF 揭露。"
},
{
 "id": "arch-availability-auditing",
  "alsoCh": ["11"],
 "ch": "ARCH", "section": "4.8.1, 11, 16, 17 rationale", "gpRef": "§4.9.1, §16–17, ELVES paper",
 "difficulty": 2, "kind": "rationale", "tags": ["architecture", "rationale", "elves"],
 "stem": "Why does JAM need BOTH availability (assurances + erasure coding) AND auditing/disputes to secure in-core computation?",
 "options": [
  "Guaranteeing attaches economic cost to invalid results; but auditors can only re-execute if the inputs are retrievable, so 2/3+1 of validators must first assure they hold erasure-coded shards (any 1/3 reconstruct); then randomly-selected auditors (ELVES) re-run reports and escalate on negative judgments or no-shows; disputes finalize the verdict on-chain and ban the report/offenders",
  "Auditing comes first: validators re-execute every report the moment it is guaranteed, and only reports that survive audit are then erasure-coded and distributed; a 1/3 assurance threshold suffices because one honest shard-holder can always raise the alarm; disputes exist only to redistribute the guarantors' deposits, so availability is a storage optimization layered onto an already-complete audit",
  "Erasure coding already establishes validity: because every shard is Merklized under the work-report's erasure-root, a validator that reconstructs the bundle can check the result without re-running refine, so assurances alone settle correctness; auditing is an optional latency optimization for nodes wanting to accumulate early, and the disputes extrinsic merely records who assured late",
  "They are two halves of one mechanism: the three guarantors of a core sign the report and then re-execute each other's work — that mutual check is what the GP calls auditing — while assurances only acknowledge receipt of the block; because guarantors are already staked no external auditor is drawn, and a negative judgment slashes the reporter directly with no on-chain verdict needed"
 ],
 "answer": 0,
 "optNotes": [
   "順序與門檻都對：2/3+1 assurance 先讓輸入可取得，隨機抽出的 auditor 才有東西重跑，disputes 收尾。",
   "順序反了；1/3 是重建所需的 chunk 比例而非 assurance 門檻，disputes 產出的是 verdict 與 ban-list。",
   "混淆資料可得性與計算正確性：erasure-root 只承諾輸入，refine 的輸出必須重新執行才知道對不對。",
   "被懷疑的正是 guarantor，自審沒有安全意義；auditor 是用 Bandersnatch VRF 從整個 validator set 抽出的。",
 ],
 "explanation": "§4.9.1：「a crypto-economic game of three stages called guaranteeing, assuring, auditing and, potentially, judging. Respectively, these attach a substantial economic cost to the invalidity of some proposed computation; then a sufficient degree of confidence that the inputs of the computation will be available for some period of time; and finally, a sufficient degree of confidence that the validity of the computation… will be checked by some party who we can expect to be honest.」四階段合起來才讓 §4.9.2 的「code executed in-core has a comparable level of crypto-economic security to that executed on-chain」成立：沒有 availability，惡意 guarantor 可以「藏起」輸入讓人無法審計；沒有 auditing，guarantee 的經濟懲罰無從觸發。report 要先被「a clear 2/3 super-majority of validators」標記，才進入 §17 的 just-became-available 集合被抽中審計；審計每 A = 8 秒一個 tranche、no-show 時 bias factor F = 2 加派審計者，而且是強制的——「one prerequisite of a node finalizing a block is for it to view the block as audited」（§20 給的量：每 validator 每 timeslot 平均 10 次、每份 report 30 次）。ELVES（eprint 2024/961）證明在 ≥ 2/3+1 誠實假設下此遊戲安全。",
 "trap": "面試「design rationale」高頻題：把四階段講清楚，並說明 report 為何要先 available 才 accumulate。"
},
{
 "id": "arch-why-prior-root-and-pipelining",
 "ch": "ARCH", "section": "5 & 20 (pipelining)", "gpRef": "§5, §20 Discussion",
 "difficulty": 2, "kind": "rationale", "tags": ["architecture", "pipelining"],
 "stem": "JAM is designed so that most of a block's work can proceed while the block propagates. Which design features make that possible?",
 "options": [
  "Temporal parallelism (pipelining): the header carries the PRIOR state root, so a block can be published before the new state has been Merklized — that cost lands in the next slot; plus spatial parallelism, both across the largely independent components of σ (whose dependency graph §4.2.1 deliberately keeps shallow) and across cores in-core",
  "Temporal parallelism comes from the header carrying the POSTERIOR state root, which lets a node accept a block without replaying it, so Merklization must finish before publication but is never repeated; spatial parallelism comes from giving each core its own fragment of σ, so two cores never touch the same state component and accumulation runs fully in parallel",
  "Blocks are authored a slot early: the ticket-holder for slot n+1 is handed the state of slot n as soon as it exists, precomputes its block and merely signs it when the slot opens, so the posterior root is already known and can go in the header; the 341 cores then each replay the block, sharing the Merklization cost 341 ways",
  "Both refine and accumulate run off-chain: a core's guarantors execute the whole pipeline and publish only a state diff, leaving the on-chain step a Merkle patch; the header's state-root field is therefore left as the zero hash and corrected only once Grandpa finalizes the block, which is what bounds the pipeline to the 8-block recent-history window"
 ],
 "answer": 0,
 "optNotes": [
   "兩種平行性都對：prior root 讓 Merklization 落到下一個 slot，σ 的淺依賴圖與多 core 則給空間平行。",
   "§5 明說 posterior root 是 Polkadot 與 Yellow Paper 的做法而 JAM 刻意 departs；JAM 也不做持久性狀態切割。",
   "Safrole 只提前決定「誰」出塊，內容取決於當下 extrinsic；core 跑的是 refine 而非重放區塊。",
   "accumulate 明訂在鏈上；先填零再由下一塊補的是 recent history β 的 state-root 欄位，不是 H_r。",
 ],
 "explanation": "§5：prior state root「to facilitate the pipelining of block computation and in particular of Merklization」——這是「a departure from both Polkadot and the Yellow Paper's Ethereum, in both of which a block's header contains the posterior state's Merkle root」，Merklize 新狀態的成本因此落到下一個 slot。§4.2 的 dependency graph 刻意最小化深度，讓 β†、Safrole、disputes、assurances、guarantees 這些輕量步驟可平行，而 accumulation（最重）之後只剩 preimage 整合、α′、π′。§20 Discussion 列了三個 driver：spatial parallelism（341 cores + eq. 4.4 的 17 個大致獨立的 state 元件）、temporal parallelism（pipelining）、PVM 與硬體對齊（RISC-V → 高效 recompile）。參考硬體 16 核/64 GB/8 TB/0.5 Gbps；CPU 預算 10/16 給 auditing、2/16 block execution、1/16 Merklization——Merklization 是每個節點自己的成本，不會被 core 數分攤。",
 "trap": "Grandpa vote 帶 posterior state root（§19）讓下游仍能驗證最新狀態——彌補 header 只有 prior root。"
},
{
 "id": "arch-services-vs-accounts",
 "ch": "ARCH", "section": "4.8.2 services", "gpRef": "§4.9.2, §9",
 "difficulty": 1, "kind": "rationale", "tags": ["architecture", "services"],
 "stem": "How do JAM services differ from Ethereum's account model, and how does external data enter the state?",
 "options": [
  "JAM has only service accounts (code + balance + state, no secret key, no nonce); each has two entry points — refine (in-core, stateless, arbitrary input → small digest) and accumulate (on-chain, stateful); all extrinsic data enters through refine inside work-packages, authorized via coretime/authorizers rather than signed transactions",
  "JAM keeps Ethereum's split but renames it: service accounts hold code, balance and state, while 'authorizer accounts' hold a secret key and a nonce so they can sign work-packages; refine and accumulate are both on-chain entry points, and external data arrives as signed transactions the authorizer account pays for from its balance",
  "JAM has only service accounts (code + balance + state, no secret key, no nonce), but a service exposes a single entry point that guarantors run in-core and the chain then re-runs on-chain to verify; external data enters as extrinsics in the block body, and coretime is charged per byte of that extrinsic much as Ethereum charges gas",
  "JAM services are the direct successors of parachains: each is registered against a fixed core, ships a validation function guarantors execute, and talks to other services over an asynchronous XCM-like queue; data enters via collators' proofs-of-validity, and the accumulate entry point exists only to move balances between services"
 ],
 "answer": 0,
 "optNotes": [
   "兩個 entry point 與「無私鑰、無 nonce」都對上 §4.9.2，外部資料一律走 work-package 裡的 refine。",
   "GP 說「In JAM, all accounts are service accounts」；authorizer 授權的是程式碼而非帳戶，付費靠事先買好的 coretime。",
   "service 有 refine 與 accumulate 兩個 entry-point；鏈上重跑正是 guarantee／assure／audit 賽局要取代的工作。",
   "service 不綁死在某個 core，CoreChains 只是眾多 service 之一，而 accumulate 遠不只搬餘額。",
 ],
 "explanation": "§4.9.2：「In JAM, all accounts are service accounts… Since they are not controlled by a secret key, they do not need a nonce.」「All data extrinsic to JAM is fed into the refinement code of some service… executed in-core… refinement code is executed off-chain and subject to no such constraints, enabling JAM services to scale dramatically both in the size of their inputs and in the complexity of their computation.」同節也明說 service definition「actually includes multiple code entry-points, one concerning refinement and the other concerning accumulation」，而且「there is no such concept of a *transactor*」——授權走的是 coretime 與 authorizer，不是簽章交易。CoreChains（parachains）、CorePlay（actor/continuation smart contracts，靠 PVM 可暫停/續跑）、CoreVM 等都只是 service——JAM 本身沒有 parachain 概念，升級責任下放到 service（Wiki：「Non-upgradable chain; upgradability responsibility shifted to services」）。",
 "trap": "面試官若問「為什麼 JAM 不可升級」：協定固定、可多實作、把演進放在 service 層。"
},
{
 "id": "arch-constants",
 "ch": "ARCH", "section": "Appendix I constants", "gpRef": "Appendix I & §20",
 "difficulty": 2, "kind": "concept", "tags": ["constants"],
 "stem": "Which set of full-configuration constants is correct?",
 "options": [
  "C = 341 cores (|κ| = 3C = 1023 in the full configuration; V itself is no longer a protocol constant), E = 600 slots/epoch, P = 6 s, Y = 500, R = 10, H = 8, L = 14,400, D = 19,200, U = 5, K = 16, O = 8, Q = 80, I = 16, J = 8, T = 128, W_G = 4,104, W_R = 48 KiB, W_B = 13,791,360, W_C = 4,000,000, G_A = 10^7, G_R = 5·10^9, G_T = 3.5·10^9, G_I = 5·10^7, A = 8 s, F = 2",
  "C = 1023 cores with V = 341 validators still fixed by the protocol, E = 3,600 slots/epoch, P = 6 s, Y = 600, R = 60, H = 8, L = 14,400, D = 19,200, U = 5, K = 16, O = 8, Q = 80, I = 16, J = 8, T = 128, W_G = 4,104, W_R = 48 KiB, W_B = 13,791,360, W_C = 4,000,000, G_A = 10^7, G_R = 5·10^9, G_T = 3.5·10^9, G_I = 5·10^7, A = 8 s, F = 2",
  "C = 341 cores with |κ| = 3C = 1023 fixed for every configuration, E = 600 slots/epoch, P = 12 s, Y = 300, R = 10, H = 24, L = 600, D = 19,200, U = 5, K = 16, O = 8, Q = 80, I = 16, J = 8, T = 128, W_G = 4,104, W_R = 48 KiB, W_B = 13,791,360, W_C = 4,000,000, G_A = 10^7, G_R = 5·10^9, G_T = 3.5·10^9, G_I = 5·10^7, A = 6 s, F = 3",
  "C = 341 cores (|κ| = 3C = 1023 in the full configuration), E = 600 slots/epoch, P = 6 s, Y = 500, R = 10, H = 8, L = 14,400, D = 14,400 (identical to L), U = 5, K = 3, O = 80, Q = 8, I = 8, J = 16, T = 16, W_G = 4,096, W_R = 12 MB, W_B = 48 KiB, W_C = 64,000, G_A = 5·10^9, G_R = 10^7, G_T = 3.5·10^9, G_I = 5·10^7, A = 8 s, F = 2"
 ],
 "answer": 0,
 "optNotes": [
   "整組與附錄 I 相符，關鍵在 0.8.0 已把 V 移出常數表、驗證者數改由 𝕍 決定而門檻一律取 |κ|。",
   "core 數與 validator 數對調了；E = 600（正好一小時）、Y 必須小於 E、rotation R = 10。",
   "GP 全文以 six-second timeslot 為前提；H = 8、L = 14,400、A = 8 s、F = 2，且 |κ| 已非固定。",
   "多組常數被對調或寫錯：D = L + 4,800、O = 8 / Q = 80、I = 16 / J = 8、W_G = 4,104、W_C = 4,000,000。",
 ],
 "explanation": "附錄 I 的常數表在 0.8.0 已**沒有 V**（validator 數改由 𝕍 ≡ {3c | c ∈ N_[2,C+1]} 決定、門檻一律取 |κ|）：C_corecount 341、epoch E 600、slot P 6 s、Y（epoch tail start）500、R（rotation）10、H（recent history）8、L（max lookup anchorage）14,400 = 24h、D（expunge）19,200 = L + 4,800、U（assurance timeout）5、K（max block tickets）16、O（auth pool）8、Q（auth queue）80、I（max package items）16、J（max report deps）8、N_V/N_O 16、S = 2^16、T（max package extrinsics）128、W_M/W_X（imports/exports）3,072、W_G segment 4,104、W_F 4,488、W_R 48·2^10、W_B 13,791,360、W_A 64,000、W_C 4,000,000、W_T memo 128、G_A 10^7、G_I 5·10^7、G_R 5·10^9、G_T 3.5·10^9、B_S/B_I/B_L = 100/10/1、A（tranche）8 s、F（audit bias）2、Z_P 2^12、Z_Z 2^16、Z_I 2^24、Z_A 2。full 配置下 |κ| = 1023 = 3·341（每個 active core 3 個 guarantor），但 #514 之後「所有配置都固定 1023」的說法已不成立。",
 "trap": "tiny（test vectors）：V 6、C 2、E 12、Y 10、R 4、D 32、K 3→(0.8.0 由公式)、N ⌈2E/V⌉。"
},
{
 "id": "arch-jam-vs-polkadot-eth",
 "ch": "ARCH", "section": "2 Previous Work", "gpRef": "§2",
 "difficulty": 2, "kind": "rationale", "tags": ["architecture", "rationale"],
 "stem": "According to the GP's 'Previous Work' analysis, what are the main limitations of Polkadot 1.0 and of Ethereum-style rollups that JAM tries to overcome?",
 "options": [
  "Polkadot: parachains are isolated ecosystems with asynchronous, coarse-grained XCMP and access limited to ~50 auction slots; rollups: heterogeneous security/economics, SNARK proving is orders of magnitude too costly (RISC-Zero ~61,000× slower than native) and sequencers centralize — JAM keeps Polkadot's ELVES machinery but makes cores un-opinionated, permissionless and semi-coherent",
  "Polkadot: its weakness is that all parachains share one validator set, so security is capped by a single stake pool and XCMP must stay synchronous to be safe; rollups: proving costs are already within reach of crypto-economic verification and only sequencer uptime is unsolved — JAM therefore drops the ELVES audit game for SNARK-verified cores and gives each service its own validator subset",
  "Polkadot: parachains are isolated and XCMP is asynchronous and coarse-grained; rollups: their fragmentation is benign because Ethereum's validator set gives every roll-up identical communication, security and economic properties, and the one real obstacle is proving the EVM — JAM answers by fixing parachain validation as the single function a core may run, with coretime still auctioned in long-term slots",
  "Polkadot: it cannot safely host more than ~50 parachains because the ELVES audit game is the bottleneck; rollups: proof generation is already cheap enough, but Dank-sharding's erasure coding over a binary field with Merklization is what centralizes them — JAM answers by adopting KZG polynomial-commitment availability and replacing auditing with optimistic fraud proofs"
 ],
 "answer": 0,
 "optNotes": [
   "四點都出自 §2：XCMP 非同步且粗粒度、約 50 個 slot、RISC-Zero 慢 61,000 倍，JAM 則 co-opt ELVES。",
   "GP 拿單一 validator set 對比 Cosmos 的 no homogenous security；XCMP 被明寫為 asynchronous，JAM 也保留 ELVES。",
   "§2 說 rollup 的性質「may differ, potentially quite dramatically」；core 不預設用途，長期拍賣正是要消除的門檻。",
   "兩邊對調：Dank-sharding 用大質數域的 polynomial commitment，binary field 加 Merklization 才是 JAM 採用的方案。",
 ],
 "explanation": "§2：Polkadot「a collection of independent ecosystems with only limited opportunity for collaboration」，XCMP「asynchronous, coarse-grained and practically limited by its reliance on a high-level slowly evolving interaction language」，slot 數約 50——這是 accessibility 的限制，不是安全上限。Ethereum rollup 市場則是「heterogeneous communication… security… and economic properties」；SNARK：RISC-Zero「over 61,000 times as long as simply recompiling and executing」、成本 66,000,000×，即使 50,000× 也「several orders of magnitude greater than would be required to compete on a cost-basis with established crypto-economic techniques」；Solana 式全同步：多次停機、512 GB RAM、依賴中心化資料庫。JAM 的回答是保留（co-opt）ELVES——GP 評它為三種跨網路安全方案中最安全、經濟效率最高者——並把 core 變成 un-opinionated、permissionless、semi-coherent 的通用計算資源。",
 "trap": "Kian 的說法：「What was once called an L2/parachain is now called a service」。"
},
{
 "id": "ch14-work-package",
 "ch": "14", "section": "14.2 Work Packages", "gpRef": "eq. 14.2–14.3 (§14.3)",
 "difficulty": 2, "kind": "concept", "tags": ["work-packages"],
 "stem": "A work-package (eq. 14.2, of the set ℙ) is ⟨j, h, u, f, c, w⟩. Which description is correct?",
 "options": [
  "j authorization token; h auth-service index (the service hosting the authorizer code); u authorizer code hash; f configuration blob (parameterization); c refinement context; w work-items (1..I = 16) each with service, code hash, payload, refine & accumulate gas limits, imports (segment root/hash + index), extrinsic (hash, length) pairs, and export count",
  "j the guarantors' signatures over the package; h the hash of the package itself; u the index of the service whose refine code runs; f the gas limit shared by every item; c the availability specification (erasure-root, segment-root, length); w work-items (1..I = 16) each with service, payload, extrinsic hashes and an authorization token of its own",
  "j authorization token; h the index of the service that will accumulate the results; u the refine code hash of the first work-item; f configuration blob; c the availability context: erasure-root plus the chunk indices; w work-items (1..T = 128) each with service, code hash, payload, one combined gas limit, imported segment hashes, and its exported segments inline",
  "j authorization token (an opaque blob); h the index of the core the package is destined for; u authorizer code hash; f configuration blob (parameterization); c refinement context; w work-items (1..I = 16) each with service, code hash, payload, refine & accumulate gas limits, the imported segments' data inline, extrinsic (hash, length) pairs, and the exported segments' hashes"
 ],
 "answer": 0,
 "optNotes": [
   "六個欄位逐一對上 eq. 14.2，work-item 的 g/a 兩個 gas limit 與只記數量的 e 也對上 eq. 14.3。",
   "把 work-report 的欄位搬進 package：guarantor 簽章在 E_G 裡，availability specification 是 report 的欄位。",
   "item 上限是 I = 16（T = 128 是整個 package 的 extrinsic 總數），而且 export 只記數量、不內嵌。",
   "h 的型別是 N_S（service index），core 由 guarantor 決定並寫在 report 上；import 也是承諾而非內嵌資料。",
 ],
 "explanation": "eq. 14.2：ℙ ≡ (j ∈ B token, h ∈ N_S auth service, u ∈ H auth code hash, f ∈ B config, c ∈ ℂ context, w ∈ [𝕀]_{1:I} items)；eq. 14.3：work-item = (s service, c code hash, y payload, g refine gas limit, a accumulate gas limit, i imports [(H ∪ hash⊞, N)], x extrinsics [(H, N)], e export count)。authorizer a = H(u ⌢ f)（0.8.0 #522）；h 是「hosts the authorization code」的 service，c 是 refinement context（anchor hash/state root/beefy root、lookup anchor hash 與 slot、prerequisites），不要跟 work-report 的 availability specification 混。限制（eq. 14.5–14.9）：總 extrinsics ≤ T = 128、imports/exports ≤ W_M/W_X = 3,072、bundle ≤ W_B = 13,791,360。§14.2 的設計原則是「Rather than having much data inline, they instead reference data through commitments」——import 用 (Merkle root, index) 承諾，export「we do not require any particular commitment to them in the work-package beyond knowing how many」。§14 之後（15 guaranteeing、16 assurance、17 auditing）是 M2 範圍，但 M1 面試仍可能問 refine 的輸入輸出概念。",
 "trap": "auth code 是從 δ[h] 的 preimage 以 lookup-anchor 時間做 historical lookup 取得（eq. 14.4 附近）。"
},
{
 "id": "delta-summary-080",
 "ch": "ARCH", "section": "GP 0.7.2 → 0.8.0 changes", "gpRef": "graypaper releases v0.8.0 (June 3 2026)",
 "difficulty": 2, "kind": "delta", "tags": ["delta-0.8.0"],
 "stem": "Your implementation targets GP 0.7.2 while the current GP is 0.8.0. Which list contains ONLY genuine 0.8.0 changes?",
 "options": [
  "Variable validator-set sizes (multiples of 3, 6…1023, thresholds derived from |κ|); full guarantees kept in ρ; hard caps of 16 verdicts/culprits/faults, with culprits no longer required behind a bad verdict; bless restricted to the manager service; authorizer = H(auth code hash ⌢ config); refinement context gains anchor slot + lookup-anchor posterior root; per-basic-block gas model with grow_heap replacing sbrk; tickets per validator = ⌈2E/|γ′_P|⌉",
  "The 'Macrofication Marathon' moving every variable-length item to the end of its encoding; fixed-length validator-index serialization; W* made to depend on ρ†; accumulate absorbing on_transfer so a service has one on-chain entry point; the core index added to refine's arguments and removed from the guarantee payload; small service IDs; a version byte prefixing account serialization; 'Owned Privileges' for χ",
  "fetch replacing the import host call; memory-access exceptions formalized and a feature freeze declared; assurances checked with the prior validator set; Ed25519 keys in the epoch marker alongside activity statistics; the provide host call, with imports separated from exports; 'super-fetch', gratis storage and account metadata; maximum code sizes with oversize reports handled; stricter opcode and jump validity",
  "64-bit PVM registers and 64-bit addressing throughout; guarantor assignments carrying full validator keys; erasure-coding equation fixes; the info host call gaining registers 9 and 10; explicit per-invocation out-of-gas checks; the transfer gas-charge fix and the work-package size-limit fix; preimage-integration simplification; the posterior state root finalised; a metadata prefix for code blobs"
 ],
 "answer": 0,
 "optNotes": [
   "整份清單都能對回 0.8.0 的 PR：#514、#494、#525、#519、#522、#526、#508、#527。",
   "Macrofication Marathon、變長欄位後移、W* 依賴 ρ† 屬 0.7.0；on_transfer 併入與 small service IDs 屬 0.7.1。",
   "fetch 取代 import 與 feature freeze 屬 0.6.0，其餘散落在 0.6.4、0.6.5、0.6.6、0.6.7。",
   "64-bit registers 屬 0.5.0；info 的 register 9/10、transfer gas fix 等屬 0.7.2，正是你們現在的版本。",
 ],
 "explanation": "0.8.0（2026-06-03）的實際變更清單：#514 support smaller validator sets（𝕍 ≡ {3c}，門檻一律由 |κ| 導出）、#494 keep full guarantees in ρ、#525 dispute extrinsic 硬上限 16 且移除 culprits 必要性、#519 restrict bless to manager service、#522 update authorizer identification（authorizer = H(auth code hash ⌢ config)，對齊 ch. 8 與 ch. 14）、#526 expose lookup anchor posterior root and anchor slot、#508 新 gas cost model（per-basic-block，模擬 ROB/execution units）與 sbrk → grow_heap、#517 host function gas costs、#527 ticket 常數改為 ⌈2E/|γ′_P|⌉、#524 extrinsic hash、#502 processed transfer count、#497 illegal memory access 收費、#520/#521/#528。0.7.2 與 0.8.0 之間沒有任何 release，所以判準就是上面這份 PR 清單：凡不在其中的條目，都屬於更早的 release。你們 issue #1012（Update to v0.8.0）與其子 issue #1013–#1022 就是這張清單的實作追蹤。",
 "trap": "面試官依「最新 GP」出題（T&C 3.5：conformance assessed against the latest release），所以 0.8.0 差異必須熟。"
},
{
 "id": "arch-tiny-config",
 "ch": "ARCH", "section": "Test vectors tiny configuration", "gpRef": "w3f/jamtestvectors README & JIP-4",
 "difficulty": 1, "kind": "concept", "tags": ["tiny", "test-vectors"],
 "stem": "Which values describe the 'tiny' test-vector configuration used by the W3F vectors and the conformance fuzzer?",
 "options": [
  "6 validators, 2 cores, epoch 12 slots, ticket submission ends at slot 10, rotation period 4, preimage expunge period 32, super-majority 5 of 6, verdict thresholds 5/0/2, ring size 6",
  "6 validators, 2 cores, epoch 12 slots, ticket submission ends at slot 12, rotation period 4, preimage expunge period 32, super-majority 4 of 6, verdict thresholds 4/0/2, ring size 6",
  "12 validators, 4 cores, epoch 60 slots, ticket submission ends at slot 50, rotation period 10, preimage expunge period 64, super-majority 9 of 12, verdict thresholds 9/0/4, ring size 12",
  "1023 validators, 341 cores, epoch 600 slots, ticket submission ends at slot 500, rotation period 10, preimage expunge period 19,200, super-majority 683 of 1023, verdict thresholds 683/0/341, ring size 1023"
 ],
 "answer": 0,
 "optNotes": [
   "6/2/12、Y = 10、rotation 4、expunge 32、super-majority 5 of 6，全部對上 jamtestvectors 的 tiny。",
   "Y 必須小於 E，tiny 是 Y = 10 < E = 12；super-majority 是 ⌊2·6/3⌋ + 1 = 5 不是 4，verdict 門檻也跟著錯。",
   "雖然仍滿足 |κ| = 3C，但不是任何一份 W3F 設定的值——tiny 就是 6 個 validator、2 個 core。",
   "這其實是 full 配置的數字；tiny 改動的遠不只 gas limit，連 ring 大小與 assurance bitfield 寬度都不同。",
 ],
 "explanation": "jamtestvectors README（tiny）：num_validators 6、num_cores 2、epoch_duration 12、contest_duration（Y）10、rotation_period 4、preimage_expunge_period 32、tickets_per_validator 3（0.7.x；0.8.0 由 ⌈2E/V⌉ = 4）、max_tickets_per_extrinsic 3、num_ec_pieces_per_segment 1026；其他常數同 GP。門檻一律從 |κ| 現算：super-majority ⌊2·6/3⌋+1 = 5、wonky 門檻 ⌊6/3⌋ = 2；assurance bitfield 1 byte；Bandersnatch ring 大小 6（Zcash SRS）。對照 full 配置則是 1023 validators / 341 cores / epoch 600、expunge 19,200、super-majority 683、wonky 341。JIP-4 chainspec 的 protocol_parameters 就是用 fetch(0) 的編碼傳遞這些參數；你們 chainspec.ApplyProtocolParameters 會驗證編譯期常數必須一致。",
 "trap": "tiny 的 Y = 10 < E = 12，所以每個 epoch 只有 slot 10、11 兩個 tail slot。"
},
]
