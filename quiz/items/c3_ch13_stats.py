# -*- coding: utf-8 -*-
"""GP 0.8.0 §13 Statistics — batch c3.

Ground truth: /root/work/jam/gp-src/text/statistics.tex (§13), preamble.tex symbol table
(π = \\activity, π_V = \\valstatsaccumulator, π_L = \\valstatsprevious, π_C = \\corestats,
π_S = \\servicestats, I = \\incomingreports, R = \\justbecameavailable, G = \\reporters,
S = \\accumulationstatistics, W_G = C_segmentsize = 4104).
Equation numbering for §13 (17 numbered equations, only eq:activityspec is labelled):
13.1 π ≡ (π_V, π_L, π_C, π_S) · 13.2 record type · 13.3 |π_V| = |κ|, |π_L| = |λ|
13.4 π_V† (assurances) · 13.5 (π_V‡, π′_L) epoch rollover · 13.6 π′_V (b,t,p,d,g)
13.7 π_C type · 13.8 π_S type · 13.9 π′_C · 13.10 R(c) · 13.11 L(c) · 13.12 D(c)
13.13 π′_S · 13.14 s = s^R ∪ s^P ∪ K(S) · 13.15 s^R · 13.16 s^P · 13.17 R(s)
"""

ITEMS = [
    {
        "id": "c3-ch13-epoch-boundary-split",
        "ch": "13",
        "section": "13.1 Validator Activity",
        "gpRef": "eq. 13.4–13.6",
        "difficulty": 3,
        "kind": "concept",
        "tags": ["statistics", "epoch", "rollover", "prior-vs-posterior", "delta-0.8.0"],
        "stem": (
            "GP 0.8.0 §13.1 derives the validator activity records in three ordered steps — π_V†, then "
            "(π_V‡, π′_L), then π′_V — with e = ⌊τ/E⌋ and e′ = ⌊τ′/E⌋. Take the first block of a new epoch "
            "(so e′ ≠ e): its author is validator 7, its assurance extrinsic E_A carries assurances signed by "
            "validators 4 and 9, and its guarantee extrinsic E_G credits validator 22. Where do this block's "
            "own increments end up?"
        ),
        "options": [
            "Everything this block contributes lands in the freshly zeroed accumulator, because eq. 13.4 "
            "applies the assurance pass to π_V‡ rather than to π_V; validator 7's block/ticket/preimage "
            "counters and validator 22's guarantee credit therefore sit in the current-epoch record "
            "alongside validators 4 and 9's assurance steps, and the archive keeps the previous epoch's "
            "totals untouched.",
            "The two assurance increments land in the last-epoch archive, because they are added to the prior "
            "record first and it is that already-incremented record which is moved across at the rollover; "
            "validator 7's block/ticket/preimage counters and validator 22's guarantee credit start from the "
            "freshly zeroed accumulator and so land in the current-epoch record. One block is deliberately "
            "split across the two records.",
            "Everything this block contributes lands in the last-epoch archive, because eq. 13.6 applies its "
            "five remaining counters to π_V† as well and it is the result of that whole pass which is moved "
            "across at the rollover; validator 7's block/ticket/preimage counters, validator 22's guarantee "
            "credit and validators 4 and 9's assurance steps therefore travel together into π′_L. The "
            "current-epoch record stays an all-zero sequence until the second block of the new epoch.",
            "The rollover is triggered by the header's epoch marker H_E rather than by comparing ⌊τ/E⌋ with "
            "⌊τ′/E⌋, and when H_E ≠ ∅ both records are zeroed rather than one being overwritten by the "
            "other; validator 7's block/ticket/preimage counters, validator 22's guarantee credit and "
            "validators 4 and 9's assurance steps are therefore all first entries of the current-epoch "
            "record, and the archive contributes nothing to this block at all.",
        ],
        "answer": 1,
        "optNotes": [
            "eq. 13.4 白紙黑字是 π_V† ≡ π_V except …，起點是 prior 的 π_V；π_V‡ 要到 eq. 13.5 才存在。",
            "eq. 13.4 先加在 π_V 上，eq. 13.5 的 otherwise 分支再把整包 π_V† 搬進 π′_L，一塊被劈成兩半。",
            "eq. 13.6 明寫 π′_V ≡ π_V‡ except …，五個 counter 的起點是 rollover 之後的 π_V‡。",
            "π_L 從來不會被歸零：eq. 13.5 的 otherwise 分支是把 π_V† 整包搬過去覆寫它。",
        ],
        "explanation": "eq. 13.4 先做 π_V† ≡ π_V except ∀v ∈ N_{|κ|}：π_V†[v]_a = π_V[v]_a + (∃a ∈ E_A : a_v = v)——assurance 是加在 **prior** 的 π_V 上。eq. 13.5 之後才做 epoch rollover：(π_V‡, π′_L) = (π_V†, π_L) when e′ = e，otherwise ([(0, …), …], π_V†)，其中 e = ⌊τ/E⌋（prior τ）、e′ = ⌊τ′/E⌋（posterior τ′ = H_T）。eq. 13.6 才從已歸零的 π_V‡ 出發：b += (v = H_I)、t += |E_T|、p += |E_P|、d += Σ_{d ∈ E_P}|d|（都只給 author）、g += (κ′[v] ∈ G)，這些落在 π′_V。因此同一塊的六個 counter 被刻意拆到兩個 record：a 記在舊 epoch、其餘五個記在新 epoch。「整塊都進新累加器」正是 0.7.2 的作法（也是 statistics.go 目前的行為，PR #1034 才修）。順帶一提，eq. 6.28 的 H_E 恰好在 e′ > e 時非 ∅，觸發時機與 eq. 13.5 的 e′ ≠ e 重合，但 §13 從不讀它——H_E 只帶 (η_0, η_1) 與 γ′_P 的金鑰序列。",
        "trap": "口訣：assurance 在 rollover 之前，b/t/p/d/g 在 rollover 之後；epoch 邊界那一塊會被劈成兩半。",
    },
    {
        "id": "c3-ch13-guarantee-credit-set",
        "ch": "13",
        "section": "13.1 Validator Activity",
        "gpRef": "eq. 13.6 (g counter); eq. 11.28 (reporters set G)",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["statistics", "guarantees", "reporters", "prior-vs-posterior"],
        "stem": (
            "GP 0.8.0 updates the guarantee counter as π′_V[v]_g = π_V‡[v]_g + (κ′[v] ∈ G), where G is the "
            "reporters set of eq. 11.28. Suppose one block's E_G holds two guarantees: validator 12 signed a "
            "credential in both of them (one report under this rotation's assignment, one under the previous "
            "rotation's), validator 30 signed a credential in only one, and the block's author is validator 5. "
            "How does the g counter move?"
        ),
        "options": [
            "Validator 12 moves by 1, validator 30 by 1, the author not at all — the added term is a Boolean "
            "membership test of the validator's Ed25519 key against a set of keys, so two credentials in the "
            "same block still yield a single step, and the index v is resolved through the posterior active set.",
            "Validator 12 moves by 2, validator 30 by 1, the author not at all — the added term counts "
            "credential signatures rather than testing membership, so a validator that signs in two "
            "guarantees of the same block takes two steps, and the index v is resolved through the "
            "posterior active set.",
            "Validator 12 moves by 1, validator 30 by 1, and the author additionally by 2 — the added term "
            "is a Boolean membership test, so each guarantor takes a single step, the author is separately "
            "credited one step per report the block carries, and the index v is resolved through the prior "
            "active set κ.",
            "Only the author moves, and by 2 — g records the reports the author brought on-chain, one step "
            "per report; the guarantors are credited through the assurance counter a instead, and because "
            "that counter is incremented against the prior record, their steps land in the archive whenever "
            "the block sits on an epoch boundary.",
        ],
        "answer": 0,
        "optNotes": [
            "(κ′[v] ∈ G) 是集合成員的 Boolean，同一塊簽兩份也只 +1，且索引跑的是 N_{|κ′|}。",
            "來源是 §13.1 的 prose 與 0.7.0 的 per-report 舊讀法，與 eq. 13.6 的成員測試方向相反。",
            "eq. 13.6 只有 b/t/p/d 帶 v = H_I 的條件，g 的式子裡沒有 author 的位置；索引也是 posterior κ′。",
            "a 的增量條件是 ∃a ∈ E_A : a_v = v，資料來源是 assurance extrinsic 而不是 E_G。",
        ],
        "explanation": "eq. 11.28 定義 reporters set：k ∈ G ⟺ ∃(r, t, a) ∈ E_G, ∃(v, s) ∈ a : k = (k_v)_e——G 是 **Ed25519 公鑰的集合**（k 取自本 rotation 或前一 rotation 的 guarantor assignment）。eq. 13.6 的增量 (κ′[v] ∈ G) 是一個 Boolean，依 §3.7.3「⊤ = 1、⊥ = 0」的隱含轉換，同一塊裡簽兩份 report 也只能 +1（實作上就是先把 G 建成 reportersSet，再對每個 validator 最多 +1）。這裡有一個 GP 自身的矛盾必須知道：§13.1 的欄位說明寫「g: The number of reports guaranteed by the validator」，但依 eq. 13.6 的集合成員測試，g 每塊最多 +1，實際語意是「該 validator 在這一塊有沒有 guarantee 過 report」而不是 report 的筆數。考試以 eq. 13.6 為準，但要認得那句 prose——團隊在 0.7.0 時期（#710/#711）採用的正是這種 per-report 舊讀法。索引用的是 **posterior** 的 κ′（eq. 13.6 的 ∀v ∈ N_{|κ′|}），不是 prior 的 κ——注意 eq. 13.4 的 assurance 迴圈才是跑 N_{|κ|}，兩者刻意不同。",
        "trap": "GP 字面寫 κ′[v] ∈ G，但 κ′[v] ∈ K 是四欄位金鑰 tuple 而 G ⊂ H；實作一律讀成 (κ′[v])_e ∈ G。",
    },
    {
        "id": "c3-ch13-core-record-fields",
        "ch": "13",
        "section": "13.2 Cores and Services",
        "gpRef": "eq. 13.7–13.9; §13.2",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["statistics", "core-stats", "types", "gas"],
        "stem": (
            "GP 0.8.0 types the core statistics as π_C ∈ ⟦(d, p, i, x, z, e, l, u)⟧_C while the service "
            "statistics are π_S ∈ ⟨N_S → (…)⟩. A teammate is laying out the Go struct for one core record and "
            "asks which of the eight components are gas, which are counts and which are octet quantities — and "
            "whether the container needs zeroing at the epoch boundary. What do you tell them?"
        ),
        "options": [
            "All eight are plain naturals — the gas type N_G appears only in the service record's refinement "
            "pair; the DA load and the total extrinsic size are octet quantities but the total bundle length "
            "counts the segments in the bundle; the popularity figure counts the guarantors assigned to that "
            "core in this rotation, and the import, extrinsic and export components are plain counts. The "
            "container is a fixed-length sequence with one entry per core, rebuilt from scratch every block.",
            "The DA load and the refine gas are both gas-typed, because DA occupancy is charged against the "
            "refine budget; the total extrinsic size is an octet quantity while the total bundle length "
            "counts work-items rather than octets; the popularity figure and the import and export "
            "components are plain counts. The container is a dictionary that lists only the cores which saw "
            "activity in the block.",
            "Only the last component is gas-typed (N_G, the refine gas summed over the digests); the DA load, "
            "the total extrinsic size and the total bundle length are octet quantities; the popularity figure "
            "and the import, extrinsic and export components are plain counts. The container is a fixed-length "
            "sequence with one entry per core, rebuilt from scratch on every block, so no epoch-boundary "
            "zeroing exists for it.",
            "Only the last component is gas-typed (N_G, the refine gas summed over the digests); the DA "
            "load, the total extrinsic size and the total bundle length are octet quantities; the popularity "
            "figure and the import, extrinsic and export components are plain counts. But the sequence "
            "accumulates over the epoch just like the validator records and is zeroed at the same rollover, "
            "which is why the first component is called a load rather than a size.",
        ],
        "answer": 2,
        "optNotes": [
            "eq. 13.7 的 u ∈ N_G 確實是 gas；l = Σ (w_s)_l 是 octet 長度，p 是 assurance 打勾的張數。",
            "eq. 13.7 裡只有 u ∈ N_G，DA 佔用從不從 refine 預算扣；π_C 是定長序列，dictionary 的是 π_S。",
            "只有 u ∈ N_G、d/z/l 是 octet、其餘為計數，且 π_C 定長每塊重算——三件事都符合 eq. 13.7 與 §13.2。",
            "§13.2 第一句就否定跨塊累加；d 叫 load 是因為它衡量 DA 佔用量（含 65/64 放大），與累加無關。",
        ],
        "explanation": "eq. 13.7：π_C ∈ ⟦(d ∈ N, p ∈ N, i ∈ N, x ∈ N, z ∈ N, e ∈ N, l ∈ N, u ∈ N_G)⟧_C——八個欄位裡**只有 u 是 N_G**（gas），其餘都是 N；語意上 d（DA load）、z（extrinsic size）、l（bundle length）是 octet 數量，p、i、x、e 是計數。eq. 13.9：p = Σ_{a ∈ E_A} a_f[c]，是本塊 assurance 裡把該 core 打勾的**張數**；l = L(c) = Σ_{w ∈ I, w_c = c} (w_s)_l 明確是 avspec 的 bundle **長度**（segment 數是 avspec 的 n，只在 eq. 13.12 的 D(c) 裡以 W_G⌈65n/64⌉ 換算成 octet）。§13.2 開宗明義：「These are tracked only on a per-block basis unlike the validator statistics which are tracked over the whole epoch.」——所以 π_C 每塊整個重算。容器型別也別搞混：π_C 是 ⟦…⟧_C 的**定長序列**（341 個 core 全都有一筆，即使全零），eq. 13.8 的 π_S 才是 dictionary，只放有活動的 service。",
        "trap": "π_C 定長、每塊重算；π_S 是 dictionary、每塊重算；只有 π_V/π_L 才有 epoch rollover。",
    },
    {
        "id": "c3-ch13-rollover-code",
        "ch": "13",
        "section": "13.1 Validator Activity",
        "gpRef": "eq. 13.4–13.6",
        "difficulty": 2,
        "kind": "code",
        "tags": ["statistics", "rollover", "delta-0.8.0", "go"],
        "code": {
            "lang": "go",
            "caption": "internal/statistics/statistics.go:109-133, 460-504 (UpdateValidatorActivityStatistics / UpdateCurrentStatistics, GP 0.7.2, condensed)",
            "src": """// (13.3)  π ≡ (πV , πL, πC , πS);  (πV, πL) => (current, last)
func UpdateValidatorActivityStatistics() {
	cs := blockchain.GetInstance()
	preEpochIndex := GetEpochIndex(cs.GetPriorStates().GetTau())
	postEpochIndex := GetEpochIndex(cs.GetPosteriorStates().GetTau())
	preStatistics := cs.GetPriorStates().GetPi()
	if preEpochIndex == postEpochIndex {
		cs.GetPosteriorStates().SetPiCurrent(preStatistics.ValsCurr)
		cs.GetPosteriorStates().SetPiLast(preStatistics.ValsLast)
	} else { // reset
		valsCurrent := make(types.ValidatorsStatistics, types.ValidatorsCount)
		cs.GetPosteriorStates().SetPiCurrent(valsCurrent)
		cs.GetPosteriorStates().SetPiLast(preStatistics.ValsCurr)
	}
	UpdateCurrentStatistics(cs.GetLatestBlock().Extrinsic) // ... plus core & service stats
}

func UpdateCurrentStatistics(extrinsic types.Extrinsic) {
	statistics := cs.GetPosteriorStates().GetPi()
	UpdateBlockStatistics(&statistics, authorIndex)
	UpdateTicketStatistics(&statistics, authorIndex, extrinsic.Tickets)
	UpdatePreimageStatistics(&statistics, authorIndex, extrinsic.Preimages)
	UpdateReportStatistics(&statistics, extrinsic.Guarantees, tau, kappa)
	UpdateAvailabilityStatistics(&statistics, authorIndex, extrinsic.Assurances)
	cs.GetPosteriorStates().SetPiCurrent(statistics.ValsCurr)
}""",
        },
        "stem": (
            "This is the team's GP 0.7.2 statistics code, condensed. Measured against GP 0.8.0 eq. 13.4–13.6, "
            "on which blocks does it place a validator's assurance increment in the wrong record, and what is "
            "the minimal fix?"
        ),
        "options": [
            "Only on blocks where ⌊τ/E⌋ ≠ ⌊τ′/E⌋. eq. 13.4 applies the assurance pass to the prior record, and "
            "eq. 13.5 then moves that already-incremented record into the archive, so on an epoch-boundary "
            "block each assurer's step belongs in the archive rather than in the newly allocated slice this "
            "code writes it into. The fix is to run the assurance pass on the prior record before the branch "
            "and to hand the incremented record to the else-branch's archive assignment.",
            "On every block. eq. 13.4 attributes each assurance to the block author rather than to the "
            "assurer who signed it, so the availability pass credits the wrong validator on every block and "
            "not merely at the boundary; which of the two records receives that credit is a separate "
            "question this code already answers correctly. The fix is to index the increment by authorIndex "
            "exactly as the ticket and preimage passes already do.",
            "Only on epoch-boundary blocks, but in the opposite direction. eq. 13.6 applies all six counters "
            "to π_V† before eq. 13.5 performs the rollover, so on a boundary block the author's block, "
            "ticket and preimage steps belong in the archive too, and the newly allocated slice must stay "
            "an all-zero sequence until the second block of the new epoch. The fix is to hoist the whole of "
            "UpdateCurrentStatistics above the epoch branch, so that every counter is credited before the "
            "reset rather than only the assurance pass.",
            "On no block at all: the placement of the assurance increment already matches 0.8.0, because "
            "eq. 13.4 is itself applied to π_V‡ and this code likewise runs its availability pass on the "
            "posterior record. The only genuine 0.8.0 gap visible here is eq. 13.3, which sizes the two "
            "records from |κ| and |λ| rather than from the constant ValidatorsCount. The fix is to allocate "
            "the reset slice with len(kappa) instead.",
        ],
        "answer": 0,
        "optNotes": [
            "非邊界塊 π_V‡ = π_V†，兩種寫法同值；只有 ⌊τ/E⌋ ≠ ⌊τ′/E⌋ 的那一塊才會顯現差異。",
            "與 UpdateAvailabilityStatistics 目前用 assurance.ValidatorIndex 的作法相反，也違反 §13.1 對 a 的定義。",
            "eq. 13.6 的 b/t/p/d/g 全部以 π_V‡ 為起點，提前做等於讓新 epoch 的第一塊完全不計分。",
            "|κ|/|λ| 確實是另一個缺口，但這說法把 eq. 13.4 的起點誤讀成 π_V‡，與式子本身矛盾。",
        ],
        "explanation": "0.7.2 → 0.8.0 的差異就在 assurance 的時機。0.8.0 eq. 13.4：π_V† ≡ π_V except ∀v ∈ N_{|κ|}：π_V†[v]_a = π_V[v]_a + (∃a ∈ E_A : a_v = v)——作用在 **prior** π_V 上；eq. 13.5 才 rollover：e′ ≠ e 時 (π_V‡, π′_L) = ([(0, …), …], π_V†)。上面這段 Go 先分支歸零、把 π_V 搬進 ValsLast，然後 UpdateCurrentStatistics 從 **posterior** 取 π 再跑 UpdateAvailabilityStatistics，等於把 assurance 記進了新 epoch 的累加器。這正是 team issue #1021 / PR #1034「assurances credited before epoch rollover」要修的東西。另外 eq. 13.3 以 |κ|/|λ| 決定兩份 record 的長度（程式碼仍用常數 ValidatorsCount）也還沒補，是 team issue #1037，但那是獨立的一件事，不影響 assurance 落在哪一份 record。",
        "trap": "非 epoch 邊界的 fuzz trace 全綠不代表對——這個 bug 只在 600 塊裡的那 1 塊現形。",
    },
    {
        "id": "c3-ch13-accum-triple-code",
        "ch": "13",
        "section": "13.2 Cores and Services",
        "gpRef": "eq. 13.8, 13.13–13.14; eq. 12.27–12.28",
        "difficulty": 2,
        "kind": "code",
        "tags": ["statistics", "service-stats", "accumulation", "delta-0.8.0", "go"],
        "code": {
            "lang": "go",
            "caption": "internal/statistics/statistics.go:386-450 (CalculateAccumulationStatistics + record assembly, GP 0.7.2)",
            "src": """// v0.7.1
// (13.12) a
// AccumulateCount, AccumulateGasUsed
func CalculateAccumulationStatistics(serviceID types.ServiceID,
	accumulationStatistics types.AccumulationStatistics,
) (accumulateCount types.U32, accumulateGasUsed types.Gas) {
	value, ok := accumulationStatistics[serviceID]
	if ok {
		accumulateCount = types.U32(value.NumAccumulatedReports)
		accumulateGasUsed = value.Gas
	}
	// else, the service id is not found, count and gas are 0
	return accumulateCount, accumulateGasUsed
}

// ... inside UpdateServiceActivityStatistics, for each serviceID in s:
servicesStatistics[serviceID] = types.ServiceActivityRecord{
	ProvidedCount:     ps.count,
	ProvidedSize:      ps.size,
	RefinementCount:   R.n,
	RefinementGasUsed: R.GasUsed,
	AccumulateCount:   accumulateCount,
	AccumulateGasUsed: accumulateGasUsed,
}""",
        },
        "stem": (
            "The team's GP 0.7.2 code builds each service record's accumulation entry as the pair shown. GP "
            "0.8.0 reshapes that entry. What exactly changes, and what observable consequence does it have for "
            "which services appear in π′_S?"
        ),
        "options": [
            "The entry becomes a three-element value — work-digests accumulated for the service, deferred "
            "transfers delivered to it, and accumulation gas — obtained as the substitute-if-nothing of the "
            "service's entry in S against an all-zero triple. Since S now keeps every service whose triple is "
            "not all-zero, a service touched only by incoming transfers has a non-zero middle element, becomes "
            "a key of S, and therefore joins the union that forms π′_S's domain.",
            "The entry keeps its two elements — work-digests accumulated for the service and accumulation "
            "gas — but the gas element is re-typed from N_G to a plain natural, and it is now read out with "
            "a bare dictionary subscript rather than through the substitute-if-nothing wrapper. The domain "
            "of π′_S is unchanged, still the union of reported services, preimage-provided services and the "
            "keys of the accumulation statistics, so a service touched only by a transfer never appears.",
            "0.8.0 restores the separate on-transfer PVM invocation Ψ_T, so the accumulation entry keeps "
            "its two elements and the record regains a transfer count and a transfer gas figure as two "
            "further top-level fields beside it, drawn from a second dictionary of on-transfer statistics. "
            "Every service that received a transfer therefore appears in π′_S carrying its own on-transfer "
            "gas figure, beside the reported and preimage-provided services.",
            "The entry becomes a three-element value — work-digests accumulated for the service, preimages "
            "provided to it, and accumulation gas — obtained as the substitute-if-nothing of the service's "
            "entry in S against an all-zero triple. Since that middle element already counts provisions the "
            "separate provision pair becomes redundant, and the domain of π′_S narrows to exactly the "
            "services which appear as keys of the accumulation statistics.",
        ],
        "answer": 0,
        "optNotes": [
            "eq. 13.13 的 a = 𝒰(S[s], (0,0,0))；T(s) > 0 讓純收款的 service 經 K(S) 進入 domain。",
            "eq. 13.8 的 a 第三個元素仍是 N_G，且用的是 𝒰 包裝——裸下標查不到會得 ∅，型別不合。",
            "accumulation.tex 全篇沒有 Ψ_T；#502 只放回 transfer 筆數，沒有第二本 on-transfer 統計字典。",
            "eq. 12.28 的 T(s) 數的是 transfer 筆數而非 preimage；eq. 13.14 的三方聯集也沒動過。",
        ],
        "explanation": "eq. 13.8：π_S ∈ ⟨N_S → (p ∈ (N, N), r ∈ (N, N_G), i ∈ N, x ∈ N, z ∈ N, e ∈ N, a ∈ (N, N, N_G))⟩——a 在 0.8.0 是**三元組**。eq. 13.13：a = 𝒰(S[s], (0, 0, 0))，𝒰 是 §3.2 / eq. 3.2 的 substitute-if-nothing。S 的定義在 eq. 12.27–12.28：S ∈ ⟨N_S → (N, N, N_G)⟩、S ≡ {s ↦ S(s) | S(s) ≠ (0, 0, 0)}，其中 S(s) = (N(s), T(s), G(s))：N(s) 是本塊被 accumulate 的 work-digest 數、T(s) ≡ |[t | t ↕ t, t_d = s]| 是 destination 為 s 的 processed deferred transfer 數、G(s) 是 accumulation 用掉的 gas。eq. 13.14：s = s^R ∪ s^P ∪ K(S)。歷史脈絡：0.7.1（team #656）因為 Ψ_T 被移除而把 OnTransfersCount / OnTransfersGasUsed 從 ServiceActivityRecord 刪掉，0.8.0（GP #502「Add back processed transfer count to service statistics」）只把 transfer **筆數**放回三元組中間，並沒有復活 on-transfer 的 gas 欄位，也沒有復活 Ψ_T——轉帳的 gas 是在 eq. 12.23 的 g 裡與 work-digest 的 gas 加總後一次進 Ψ_A。另一個要留意的編輯瑕疵：eq. 13.13 的 p = Σ_{(s, d) ∈ E_P}(1, |d|)，comprehension 綁定的 s 字面上**遮蔽**了外層的 ∀s ∈ s，照字面讀會退化成與 service 無關的全域總和；實際意思（也是所有實作的作法）是「E_P 中 service index 等於該 s 的那些 preimage 的 (筆數, 總 octet 數)」，同樣的遮蔽寫法也見於 eq. 12.28 的 G(s)。",
        "trap": "0.8.0 加回來的是 transfer 的「筆數」，不是 on-transfer 的 gas；Ψ_T 沒有回來。",
    },
    {
        "id": "c3-ch13-consensus-state-rationale",
        "ch": "13",
        "section": "13.1 Validator Activity",
        "gpRef": "§13.1; eq. 4.4 (state composition); eq. 13.1–13.3; App. D key C(13)",
        "difficulty": 2,
        "kind": "rationale",
        "tags": ["statistics", "rationale", "state", "epoch", "staking"],
        "stem": (
            "An interviewer pushes back: 'Validator counters look like telemetry to me. Why are they a "
            "component of σ and Merklized into the state trie at all, and why keep two validator records "
            "rather than one running counter?' What is the GP-grounded answer?"
        ),
        "options": [
            "It is essentially a serialization convenience: the JIP-2 RPC's statistics endpoint and the "
            "conformance vectors want a fixed-shape record, so π rides along in σ purely to give those "
            "consumers a stable layout, and because it is excluded from the state-trie construction of "
            "appendix D a node that skipped the update entirely would still agree on the state root. The "
            "pairing exists only so that a test vector can compare a whole epoch's totals in one shot.",
            "Because Grandpa weights finality votes by validator performance, so the figures have to sit in "
            "σ where the finality gadget can read them and a stale accumulator would let a validator vote "
            "with the previous epoch's weight; that is also why §13.1 has validators vote on each other's "
            "auditing efforts, since audits carry the same weight in that ballot. The pairing exists so "
            "that a validator removed from the active set mid-epoch can still be slashed against its own "
            "history rather than against whoever replaced it, and the core records are paired for exactly "
            "the same reason.",
            "Because the author's reward is paid out of the block's accumulation gas budget in the same "
            "block, so the counters have to be readable from inside the state transition rather than from "
            "an off-chain index. The pairing is a rollback buffer: when a fork is reverted the archive is "
            "copied back over the accumulator, which is exactly why both halves have to be Merklized.",
            "Because the figures must be bit-identical on every node and provable to a consumer outside the "
            "chain: JAM pays no rewards itself but has to deliver activity data to a staking subsystem, so "
            "the record is a state component with its own trie key and a node computing it differently "
            "produces a different state root. The pairing exists because settlement is per-epoch — the "
            "archive holds the just-completed epoch's totals unchanged for the whole of the next epoch, "
            "giving a stable snapshot to read while the accumulator fills.",
        ],
        "answer": 3,
        "optNotes": [
            "與 App. D 直接衝突：C(13) 就是 π 的 state key，π′ 一定會被併進 M_σ(σ′)。",
            "GRANDPA、BEEFY 與 auditing 恰恰是 §13.1 說無法直接鏈上追蹤、要靠互評取中位數的部分。",
            "§13.1 第一句就是 does not explicitly issue rewards；分叉靠整個 σ 版本切換，沒有回拷 π 的動作。",
            "§13.1 原文：JAM 不發獎勵、只把活動資料送進 staking subsystem，配對是為了 per-epoch 結算的穩定快照。",
        ],
        "explanation": "§13.1 開頭：「The JAM chain does not explicitly issue rewards—we leave this as a job to be done by the staking subsystem…However…it is important for the JAM chain to facilitate the arrival of information on validator activity in to the staking subsystem so that it may be acted upon.」要讓鏈外（甚至跨鏈）的 staking 系統能**信任**這些數字，它就必須是共識狀態：eq. 4.4 把 π 列為 σ 的十七個分量之一，App. D 以 C(13) 當 state key 併入 state trie，因此 π′ 併入 M_σ(σ′) 並可被 light client 證明——但要記住 JAM 的 header 帶的是 **prior** state root（§5：H_R ≡ M_σ(σ)，GP 明說這是與 Ethereum／Polkadot 相反的設計，為了 pipelining），所以含 π′ 的 σ′ 之根**不在本塊的 H_R 裡**，要等**下一塊**的 header 才會出現，剛好落後一塊；任何節點算錯 π 就會算出不同的 state root，直接是 invalid block。雙份 record 的理由在 §13.1：「The validator statistics are made on a per-epoch basis and we retain one record of completed statistics (π_L) together with one record which serves as an accumulator for the present epoch (π_V)」——結算以 epoch 為單位，π_L 在整個下一個 epoch 都不再變動，消費者才有穩定快照可讀。§13.2 明講 π_C/π_S「are tracked only on a per-block basis」，所以不需要這種配對；而懲罰在 §10 的 judgements，依據是 ψ 不是 π。",
        "trap": "「為什麼在鏈上」的標準答法：因為要能被證明且必須共識一致，π 進 state root；不是為了 RPC 好看。",
    },
]
