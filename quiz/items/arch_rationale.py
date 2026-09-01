# -*- coding: utf-8 -*-
# Architecture & design rationale (interview portions 3 & 4) + chapter 14 basics + 0.7.2→0.8.0 delta summary
ITEMS = [
{
 "id": "arch-corejam-name",
 "ch": "ARCH", "section": "1.1 Nomenclature / RFC-31", "gpRef": "§1.1 & RFC-31 CoreJam",
 "difficulty": 1, "kind": "rationale", "tags": ["architecture", "history"],
  "stemZh": "JAM 這個名字從何而來？原始 CoreJam 模型的哪些階段真的在鏈上執行？",
  "optionsZh": [
   "來自 CoreJam（Polkadot Fellowship RFC-31），以其 Collect / Refine / Join / Accumulate 模型命名；只有 Join 與 Accumulate 發生在鏈上——Collect 與 Refine 是鏈下／in-core 的——因此稱為 Join-Accumulate Machine，而它是一套完整的協定而非 RFC-31 那種範圍受限的改動",
   "來自 CoreJam（RFC-31），以其四段模型命名；Refine 與 Accumulate 才是鏈上那一對——Collect 與 Join 由 package 建構者在鏈下完成——因此稱為 Join-Accumulate Machine",
   "來自「Just Another Machine」，向 Yellow Paper 的命名致意；collect / refine / join / accumulate 這條管線是 RFC-31 後來才加上的，而四個階段全都在鏈上執行，因為所有東西都由單一個 validator 集合在共識中執行",
   "來自「Joint Availability Mechanism」，以位於其核心的 erasure-coded D3L 命名；RFC-31 早已用 CoreJam 這個名字提出過同一套完整協定，而只有 Collect 在鏈上執行，因為鏈必須先對進來的 work-package 排序，其餘三個階段才能在 core 上執行"
  ],
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
  "stemZh": "GP 點名了五個驅動因素、以及一條稱為「size-coherency antagonism」的原則。哪個敘述正確？",
  "optionsZh": [
   "因素為：Resilience、Generality、Performance、Coherency、Accessibility；performance 與 coherency 互相對立，因為因果關係受訊號速度所限，所以狀態空間越大就越不連貫——JAM 的回應是把一個高度可擴展、大致連貫的元件（in-core）管線化進一個同步、完全連貫的元件（on-chain），以「cache affinity」取代粗暴的分割",
   "因素同上；但對立發生在 resilience 與 accessibility 之間，因為每多一位 validator 就多一次共識往返、而便宜的取用因此迫使集合變小——JAM 的回應是把 validator 集合釘在 1,023 並把後續成長全推給非同步結算的鏈下 roll-up",
   "因素同上；performance 與 coherency 互相對立，因為簽章驗證無法平行化，所以吞吐必須用較弱的可組合性換來——JAM 的回應是把狀態切成 341 個因果獨立的分片、每片小到足以保持連貫，再以非同步訊息佇列橋接",
   "因素為：Speed、Cost、Security、Decentralization、Simplicity；對立發生在 decentralization 與 performance 之間，因為硬體需求是進入 validator 集合的門檻——JAM 的回應是把 validator 硬體固定在 16 核／64 GB／8 TB，並用 SNARK 壓縮工作量，使連貫性完全不需要任何管線就能維持"
  ],
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
  "stemZh": "JAM 為什麼採用 Safrole（票券式、匿名、ring-VRF）而不是類似 BABE 的 VRF 抽籤？",
  "optionsZh": [
   "Safrole 把每個 6 秒時槽限定給恰好一位事先決定的金鑰持有者（近乎無分叉）、讓未來時槽出塊者的身分在封印之前保持匿名（抗 DoS），並產生高品質且不可偏置的熵池；而 best-chain 規則另外偏好 ticket 封印（相對於 fallback）祖先較多的鏈",
   "Safrole 的優點是可以有多位 validator 同時贏得同一槽、使時槽永不落空：ring VRF 讓他們各自證明自己是 γ_P 的成員，產生的分叉由哪個區塊先抵達 Grandpa 決勝，而 ticket 每一槽都從 η_0 重新抽取，所以沒有出塊者能被預測超過一槽以上",
   "Safrole 的存在是為了把簽章移出熱路徑：ticket 是一個在封印時揭露的單純雜湊原像，所以檢查一個 seal 只要一次雜湊而不是一次 VRF 驗證；匿名來自 validator 每個 epoch 輪換 Ed25519 金鑰，而熵池 η 直接取自區塊雜湊，因為雜湊本來就是均勻的",
   "Safrole 是坐在 Grandpa 之下的 finality gadget：它指派每一槽一位出塊者，而該出塊者必須先蒐集 2/3+1 的預投票，該區塊才能延伸這條鏈，這正是 JAM 完全沒有分叉、也不需要 fork-choice 規則的原因；fallback 金鑰只用在創世 epoch、也就是還沒有任何 ticket 累積之前"
  ],
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
  "stemZh": "JAM 為什麼同時需要可得性（assurance + erasure coding）與稽核／爭議，才能保障 in-core 的運算？",
  "optionsZh": [
   "擔保為無效結果附上經濟成本；但 auditor 只有在輸入可取回時才能重新執行，所以必須先有 2/3+1 的 validator 背書自己持有 erasure-coded 的碎片（任意 1/3 即可重建）；接著隨機抽選的 auditor（ELVES）重跑那些 report，並在出現負面判定或缺席時升級處理；最後由 disputes 在鏈上為判決定案、封禁該 report 與 offender",
   "稽核在前：validator 在某份 report 一被擔保時就立刻重新執行它，只有通過稽核的 report 才會被 erasure-code 並分發；1/3 的背書門檻就夠了，因為一位誠實的碎片持有者永遠能發出警報；而 disputes 的存在只是為了重新分配 guarantor 的押金，所以可得性只是疊加在一套已然完整之稽核之上的儲存最佳化",
   "erasure coding 本身就確立了有效性：因為每個碎片都被 Merklize 在該 work-report 的 erasure-root 之下，所以重建出 bundle 的 validator 不必重跑 refine 就能檢查結果，因此光靠 assurance 就能定奪正確性；稽核只是給想提早 accumulate 的節點用的延遲最佳化，而 disputes extrinsic 只是記錄誰太晚背書",
   "兩者是同一個機制的兩半：一個 core 的三位 guarantor 簽署該 report、然後互相重跑彼此的工作——這種相互檢查就是 GP 所謂的稽核——而 assurance 只是確認收到了該區塊；既然 guarantor 已經質押，就不會抽出外部 auditor，而負面判定會直接沒收回報者，不需要任何鏈上判決"
  ],
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
  "stemZh": "JAM 的設計讓一個區塊的大部分工作能在該區塊傳播的同時進行。是哪些設計特徵讓這件事成為可能？",
  "optionsZh": [
   "時間上的平行（管線化）：header 帶的是先前的 state root，所以一個區塊可以在新狀態尚未 Merklize 完成之前就發布——那份成本落在下一個時槽；再加上空間上的平行，既跨越 σ 中大致獨立的各分量（§4.2.1 刻意讓其依賴圖保持淺），也跨越各個 core",
   "時間上的平行來自 header 帶著執行後的 state root，這讓節點不必重放就能接受一個區塊，所以 Merklization 必須在發布前完成、但永遠不必重做；空間上的平行則來自給每個 core 自己的 σ 片段，所以兩個 core 永遠不會碰到同一個狀態分量、accumulation 完全平行",
   "區塊是提早一槽出的：時槽 n+1 的持票人在時槽 n 的狀態一存在時就拿到它、預先算好自己的區塊，等時槽開啟時只需簽名，所以執行後的 root 早已知道、可以放進 header；接著那 341 個 core 各自重放該區塊，把 Merklization 的成本分攤 341 份",
   "refine 與 accumulate 兩者都在鏈下執行：某個 core 的 guarantor 執行整條管線、只發布一份狀態差異，讓鏈上那一步只剩一次 Merkle 修補；因此 header 的 state-root 欄位被留成零雜湊、只在 Grandpa 定案該區塊之後才修正，這正是把管線限制在 8 塊近期歷史窗口內的原因"
  ],
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
  "stemZh": "JAM 的 service 與 Ethereum 的帳戶模型有何不同？外部資料又是怎麼進入狀態的？",
  "optionsZh": [
   "JAM 只有 service 帳戶（程式碼 + 餘額 + 狀態，沒有私鑰、沒有 nonce）；每個都有兩個入口——refine（in-core、無狀態、任意輸入 → 小的 digest）與 accumulate（鏈上、有狀態）；所有外部資料都透過 refine、在 work-package 內進入，並以 coretime／authorizer 而不是簽署過的交易來授權",
   "JAM 保留了 Ethereum 的二分法只是改了名字：service 帳戶持有程式碼、餘額與狀態，而「authorizer 帳戶」持有私鑰與 nonce 好簽署 work-package；refine 與 accumulate 都是鏈上入口，而外部資料以簽署交易的形式抵達、由 authorizer 帳戶從自己的餘額支付",
   "JAM 只有 service 帳戶（沒有私鑰、沒有 nonce），但一個 service 只暴露單一個入口，由 guarantor 在 core 上執行、鏈上再重跑一次以驗證；外部資料以 extrinsic 的形式進入區塊本體，而 coretime 是按該 extrinsic 的位元組計費，很像 Ethereum 收 gas",
   "JAM 的 service 是 parachain 的直接後繼：每一個都對應註冊到一個固定的 core、提供一支由 guarantor 執行的驗證函數，並透過類似 XCM 的非同步佇列與其他 service 溝通；資料經由 collator 的有效性證明進入，而 accumulate 這個入口只是為了在 service 之間移動餘額"
  ],
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
  "stemZh": "哪一組 full 設定的常數是正確的？",
  "optionsZh": [
   "C = 341 個 core（full 設定下 |κ| = 3C = 1023；V 本身不再是協定常數）、E = 600 槽／epoch、P = 6 秒、Y = 500、R = 10、H = 8、L = 14,400、D = 19,200、U = 5、K = 16、O = 8、Q = 80、I = 16、J = 8、T = 128、W_G = 4,104、W_R = 48 KiB、W_B = 13,791,360、W_C = 4,000,000、G_A = 10^7、G_R = 5·10^9、G_T = 3.5·10^9、G_I = 5·10^7、A = 8 秒、F = 2",
   "C = 1023 個 core 而 V = 341 位 validator 仍由協定固定、E = 3,600 槽／epoch、P = 6 秒、Y = 600、R = 60，其餘同上",
   "C = 341 個 core 而 |κ| = 3C = 1023 在每一種設定下都固定、E = 600 槽／epoch、P = 12 秒、Y = 300、R = 10、H = 24、L = 600、D = 19,200、U = 5…、A = 6 秒、F = 3",
   "C = 341 個 core（full 下 |κ| = 1023）、E = 600、P = 6 秒、Y = 500、R = 10、H = 8、L = 14,400、D = 14,400（與 L 相同）、U = 5、K = 3、O = 80、Q = 8、I = 8、J = 16、T = 16、W_G = 4,096、W_R = 12 MB、W_B = 48 KiB、W_C = 64,000、G_A = 5·10^9、G_R = 10^7、G_T = 3.5·10^9、G_I = 5·10^7、A = 8 秒、F = 2"
  ],
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
  "stemZh": "依 GP 的「Previous Work」分析，Polkadot 1.0 與 Ethereum 式 rollup 的主要侷限是什麼？JAM 想克服的又是什麼？",
  "optionsZh": [
   "Polkadot：parachain 是彼此隔離的生態系，XCMP 非同步且顆粒粗，而取用受限於約 50 個拍賣插槽；rollup：安全性與經濟性異質、SNARK 的證明成本高出好幾個數量級（RISC-Zero 約比原生慢 61,000 倍）、而 sequencer 走向中心化——JAM 保留 Polkadot 的 ELVES 機制，但讓 core 變得無定見、無許可且半連貫",
   "Polkadot：它的弱點在於所有 parachain 共用同一個 validator 集合，所以安全性被單一質押池封頂，而 XCMP 必須維持同步才安全；rollup：證明成本已經進入密碼經濟驗證的可及範圍、只剩 sequencer 的可用性未解——因此 JAM 捨棄了 ELVES 稽核賽局改用 SNARK 驗證的 core，並給每個 service 自己的 validator 子集",
   "Polkadot：parachain 隔離、XCMP 非同步且粗糙；rollup：它們的碎片化是良性的，因為 Ethereum 的 validator 集合給了每個 roll-up 完全相同的通訊、安全與經濟性質，唯一真正的障礙是證明 EVM——JAM 的回應是把 parachain 驗證固定為 core 唯一能執行的函數，而 coretime 仍以長期插槽拍賣",
   "Polkadot：它無法安全地承載超過約 50 條 parachain，因為 ELVES 稽核賽局是瓶頸；rollup：證明產生已經夠便宜，但 Dank-sharding 在二元體上的 erasure coding 加 Merklization 才是使它們中心化的原因——JAM 的回應是採用 KZG 多項式承諾的可得性，並以樂觀詐欺證明取代稽核"
  ],
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
  "stemZh": "一份 work-package（eq. 14.2，屬於集合 ℙ）是 ⟨j, h, u, f, c, w⟩。哪個描述正確？",
  "optionsZh": [
   "j 授權 token；h auth-service 索引（承載 authorizer 程式碼的那個 service）；u authorizer code hash；f 設定 blob（參數化）；c refinement context；w 是 1 到 I = 16 個 work-item，每個帶 service、code hash、payload、refine 與 accumulate 的 gas 上限、imports（segment root／雜湊 + 索引）、extrinsic 的 (雜湊, 長度) 配對、以及匯出計數",
   "j 是 guarantor 對該 package 的簽章；h 是該 package 自身的雜湊；u 是其 refine 程式碼將被執行的那個 service 的索引；f 是所有項目共用的 gas 上限；c 是 availability specification；w 是 1 到 I = 16 個 work-item，每個帶自己的授權 token",
   "j 授權 token；h 將 accumulate 這些結果的 service 索引；u 第一個 work-item 的 refine code hash；f 設定 blob；c availability context（erasure-root 加碎片索引）；w 是 1 到 T = 128 個 work-item，每個帶單一個合併的 gas 上限、匯入 segment 的雜湊、以及內嵌的匯出 segment",
   "j 授權 token（一個不透明的 blob）；h 該 package 所指向的 core 索引；u authorizer code hash；f 設定 blob；c refinement context；w 是 1 到 I = 16 個 work-item，每個帶 service、code hash、payload、兩個 gas 上限、內嵌的匯入 segment 資料、extrinsic 配對、以及匯出 segment 的雜湊"
  ],
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
  "stemZh": "你們的實作以 GP 0.7.2 為目標，而當前的 GP 是 0.8.0。哪一份清單只包含真正屬於 0.8.0 的變動？",
  "optionsZh": [
   "可變的 validator 集合大小（3 的倍數、6…1023，門檻由 |κ| 導出）；ρ 中保留完整的 guarantee；verdict／culprit／fault 各 16 的硬上限，且 bad verdict 不再要求必須有 culprit；bless 限縮給 manager service；authorizer = H(auth code hash ⌢ config)；refinement context 新增 anchor slot 與 lookup-anchor 的 posterior root；以 basic block 為單位的 gas 模型、並以 grow_heap 取代 sbrk；每位 validator 的 ticket 數 = ⌈2E/|γ′_P|⌉",
   "把每個變長項目移到其編碼末端的「Macrofication Marathon」；定長的 validator 索引序列化；讓 W* 依賴 ρ†；accumulate 吸收 on_transfer 使 service 只剩一個鏈上入口；把 core 索引加入 refine 的引數並從 guarantee 的酬載移除；小型 service ID；帳戶序列化前綴版本位元組；χ 的「Owned Privileges」",
   "以 fetch 取代 import host call；記憶體存取例外的形式化與功能凍結宣告；以 prior validator 集合檢查 assurance；epoch marker 中加入 Ed25519 金鑰並附上活動統計；provide host call、以及 import 與 export 的分離；「super-fetch」、gratis storage 與帳戶 metadata；最大程式碼大小與過大 report 的處理；更嚴格的 opcode 與跳躍有效性",
   "全面的 64 位元 PVM 暫存器與 64 位元定址；guarantor 指派攜帶完整的 validator 金鑰；erasure-coding 公式修正；info host call 新增暫存器 9 與 10；明確的逐 invocation out-of-gas 檢查；transfer 的 gas 計費修正與 work-package 大小上限修正；preimage 整合的簡化；posterior state root 定案；程式碼 blob 的 metadata 前綴"
  ],
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
  "stemZh": "哪一組數值描述的是 W3F 向量與 conformance fuzzer 所使用的「tiny」測試向量設定？",
  "optionsZh": [
   "6 位 validator、2 個 core、epoch 12 槽、ticket 提交止於第 10 槽、rotation 週期 4、preimage expunge 期 32、超級多數 6 取 5、verdict 門檻 5/0/2、ring 大小 6",
   "6 位 validator、2 個 core、epoch 12 槽、ticket 提交止於第 12 槽、rotation 週期 4、preimage expunge 期 32、超級多數 6 取 4、verdict 門檻 4/0/2、ring 大小 6",
   "12 位 validator、4 個 core、epoch 60 槽、ticket 提交止於第 50 槽、rotation 週期 10、preimage expunge 期 64、超級多數 12 取 9、verdict 門檻 9/0/4、ring 大小 12",
   "1023 位 validator、341 個 core、epoch 600 槽、ticket 提交止於第 500 槽、rotation 週期 10、preimage expunge 期 19,200、超級多數 1023 取 683、verdict 門檻 683/0/341、ring 大小 1023"
  ],
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
