# -*- coding: utf-8 -*-
# Batch 2 — Chapter 5 (The Header), Chapter 7 (Recent History), Chapter 8 (Authorization) — GP 0.8.0
# Complements items/ch05_header.py and items/ch07_ch08.py (no overlap with their stems).
ITEMS = [
{
 "id": "ch05-unsigned-header-serialization",
 "ch": "5", "section": "5 The Header (serialization, Appendix C.2)", "gpRef": "eq. 5.1 & §C.2 (E(H), E_U(H))",
 "difficulty": 2, "kind": "code", "tags": ["header", "codec", "seal", "code"],
 "stem": "The team derives the unsigned header serialization by encoding the full header and truncating it. Which statement about GP 0.8.0's E(H) and E_U(H) explains why this is sound and describes E_U's layout correctly?",
 "code": {"lang": "go", "caption": "internal/utilities/block_serialization.go (HeaderUSerialization) + field order of Header.Encode in internal/types/encode.go", "src": """// (C.23)
// This function encodes the header's properties without the seal
// I still use header encoding function, but remove the length of the encoded seal
func HeaderUSerialization(header types.Header) (output types.ByteSequence, err error) {
	encoder := types.GetEncoder()
	defer types.PutEncoder(encoder)

	serializedHeader, err := encoder.Encode(&header)
	if err != nil {
		return nil, err
	}

	lengthOfSeal := len(header.Seal)          // BandersnatchVrfSignature = [96]byte
	validLength := len(serializedHeader) - lengthOfSeal

	output = append(output, serializedHeader[:validLength]...)

	return output, nil
}

// encode.go — Header.Encode writes, in order: Parent, ParentStateRoot, ExtrinsicHash, Slot,
//   EpochMark   (nil -> 0x00, else 0x01 ++ mark),
//   TicketsMark (nil -> 0x00, else 0x01 ++ E tickets),
//   AuthorIndex, EntropySource, OffendersMark (length-prefixed), Seal"""},
 "options": [
  "E_U(H) omits both Bandersnatch signatures — the entropy source H_V as well as the seal H_S — so a conformant implementation must cut 192 octets from E(H), and the seal's message contains no VRF material at all, which is what stops the two signatures depending on one another",
  "E(H) = E(E_U(H), H_S): the 96-octet seal is the last, fixed-size field, so cutting 96 bytes off E(H) yields exactly the seal's message; inside E_U the order is H_P, H_R, H_X, E_4(H_T), H_E (0/1 discriminator), H_W (0/1 discriminator), E_2(H_I), H_V, var(H_O)",
  "E_U(H) is E(H) with the seal replaced by 96 zero octets, keeping the header length constant so that H_P can be computed before sealing; simple truncation therefore yields a message 96 octets too short and an implementation must re-encode with a zeroed seal instead",
  "The serialized field order follows eq. 5.1 literally (…, H_W, var(H_O), E_2(H_I), H_V, H_S), so truncating the last 96 octets is only correct when H_O is empty, because the length-prefixed offenders list shifts every field that follows it, the seal included"
 ],
 "answer": 1,
 "optNotes": [
  "E_U 只排除 seal；連 H_V 也拿掉的話，eq. 6.16/6.17 的 seal 就簽不到本塊的 entropy 來源。",
  "H_S 固定 96 octets 且永遠排在最後，去尾 96 bytes 恰好就是 seal 所簽的 message。",
  "E_U 是直接省略 seal 而不是填零：C.2 寫的是 E(H) = E(E_U(H), H_S)。",
  "H_O 再長也只是把 seal 的起點往後推，「尾端 96 bytes 就是 seal」與 H_O 長度無關。",
 ],
 "explanation": "附錄 C.2：E(H) = E(E_U(H), H_S)，而 E_U(H) = E(H_P, H_R, H_X, E_4(H_T), E_epochmark(H_E), maybe(H_R), E_2(H_I), H_V, var(H_O))。H_V 仍留在 E_U 內（seal 簽到 H_V；H_V 的 VRF context 則含 Y(H_S)，而 VRF output 只由 key 與 context 決定、與 message 無關，所以不循環）。注意序列化順序與 eq. 5.1 的 tuple 順序不同：E_U 裡 E_2(H_I)、H_V 排在 H_O 之前，H_O 以 var（長度前綴）放在 E_U 最後；H_E 用 E(0) 或 E(1, η_0, η_1, var(k))，H_W 用 maybe（0 或 1 ⌢ 固定 E 張 ticket）。你們 Header.Encode 的欄位順序 Parent…AuthorIndex, EntropySource, OffendersMark, Seal 正是這個順序，所以 HeaderUSerialization 的做法正確。0.8.0 的小 delta：epoch marker 的 key 序列改為 var(k)（#1031）。",
 "trap": "序列化順序 p r x t e w i v o | s（H_O 在 H_V 之後、seal 最後），eq. 5.1 的 tuple 順序是 p r x t e w o i v s；E_U = E(H) 去尾 96 bytes。"
},
{
 "id": "ch05-extrinsic-hash-inclusion-proof",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.4–5.7",
 "difficulty": 3, "kind": "concept", "tags": ["header", "extrinsic-hash", "light-client", "delta-0.8.0"],
 "stem": "A light client holds only a verified header H and wants to check that preimage blob d for service s was included in that block's E_P. Given H_X = H(E(H#(a))) with a = [E_T(E_T), p, g, E_A(E_A), E_D(E_D)] (eq. 5.4–5.7), what is the minimal witness it needs and what is the shape of the check?",
 "options": [
  "A log₂|E_P|-length Merkle path from the leaf H(d) up to H_X, because H_X is a binary Merkle root over every extrinsic item of the block, so the witness is O(log n) hashes and grows only logarithmically as the block fills up",
  "The complete E_P (every preimage blob of the block) together with the other four extrinsics in full, because H_X hashes the block's whole extrinsic serialization as one blob and cannot be recomputed from hashes alone",
  "The other four component hashes (h_T, h_g, h_A, h_D) plus the entire p sequence of (E_4(s_i), H(d_i)) pairs: it checks (E_4(s), H(d)) ∈ p and H(h_T ⌢ H(p) ⌢ h_g ⌢ h_A ⌢ h_D) = H_X — no other blob is needed, but p is a flat blob, not a log-size path",
  "Only H(d), the service index s and the block's H_X, because eq. 5.6 commits each (service, preimage-hash) pair directly into H_X, so a single pair can be checked without touching the rest of E_P or any of the other four extrinsic components"
 ],
 "answer": 2,
 "optNotes": [
  "H# 只是逐項 map 後平鋪再取一次 hash，不是二元 Merkle tree，p 內部沒有 log 長度的路徑。",
  "那是 0.7.2 的情況；#524 之後 p 只帶 (service, blake(blob))，不必附上其他人的 blob。",
  "witness = 四個 sibling hash + 整段 p（每項 36 bytes），大小隨區塊裡的 preimage 數線性成長。",
  "p 是先整段編碼再取一次 hash，單憑一組 (s, H(d)) 與 H_X 是重算不出來的。",
 ],
 "explanation": "eq. 5.4：H_X ≡ H(E(H#(a)))，H# 是把 H 逐項套用到序列 a 的每個元素（§3 notation：f^# 表示 map），所以 H_X = H(h_T ⌢ h_p ⌢ h_g ⌢ h_A ⌢ h_D)，其中 h_p = H(p)、p = E(var[(E_4(s), H(d)) | (s, d) ∈ E_P])（eq. 5.6）。這是兩層結構：外層是 5 個 component hash 平鋪後再 hash，內層的 p 是一整個 blob。§5 說明：「taking care to allow for the possibility of reports and preimages to individually have their inclusion proven」——0.8.0 PR #524 把 p 從 E_P(E_P)（含完整 blob）改成 (service, blake(blob)) 的序列，證明時才不必附上其他 preimage 的 blob。你們 CreateExtrinsicHash（0.7.2）對 preimages 仍是 hash 整個 EncodeExtrinsicPreimages，升到 0.8.0 時要改成對 (E_4(s), H(d)) 序列取 hash（#1031）；guarantees 那一段（g，report 用 H(w) 代替）在 0.7.2 已經做對。",
 "trap": "H_X 是「hash of five hashes」，不是 Merkle root；只有 p 與 g 以 hash 代替內容，E_T/E_A/E_D 是整包 encode 後 hash。"
},
{
 "id": "ch05-future-slot-temporarily-invalid",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.8 & §5 text",
 "difficulty": 2, "kind": "concept", "tags": ["header", "time", "validation"],
 "stem": "A node receives a block at wall-clock time T whose header has H_T · P > T, while P(H)_t < H_T holds (its parent is known and older). How does GP §5 classify this block?",
 "options": [
  "It is permanently invalid, and since authoring ahead of the clock is an offence the author's Ed25519 key must reach ψ_O as a culprit in the next block's disputes extrinsic, so the node discards the header rather than keeping it",
  "It is valid as long as the drift stays below one slot period P = 6 s, which the GP grants as an explicit clock-skew tolerance so that honest authors at the very start of a slot are not rejected by peers whose clocks run marginally slow",
  "It is valid: only the ordering rule P(H)_t < H_T belongs to consensus, while the wall-clock comparison is authoring guidance — which is exactly why the STF test vectors carry no notion of T and an importing node must accept the block",
  "It fails eq. 5.8 for now, but the GP notes such a block 'may become valid as T advances' — unlike a block with H_T ≤ P(H)_t, which can never become valid, it is only temporarily invalid and may be re-evaluated later"
 ],
 "answer": 3,
 "optNotes": [
  "ψ_O 只由 E_D 的 culprits/faults 增長，那些爭議全部圍繞 work-report 的正確性，與出塊時間無關。",
  "GP 沒有任何 clock-skew 容忍條款，eq. 5.8 就是 H_T·P ≤ T 這個硬比較。",
  "eq. 5.8 的兩個 conjunct 都是有效性條件；vectors 不含 T 只因離線 trace 表達不了 wall-clock。",
  "T 會前進，所以未來區塊只是暫時無效；而 H_T ≤ P(H)_t 永遠不可能變真。",
 ],
 "explanation": "eq. 5.8：P(H)_t < H_T ∧ H_T·P ≤ T（P = 6 秒，T 為自 JAM Common Era 起的 wall-clock 秒數）。§5：「A block may only be regarded as valid once the time-slot index H_T is in the past」，而且「Blocks considered invalid by this rule may become valid as T advances」——節點可以暫存未來區塊、等 T 追上再 import。對照你們的 code：STF 裡只檢查 τ < τ′（safrole.go 的 BadSlot：「timeslot value must be strictly monotonic」），wall-clock 條件放在 header_controller.ValidateTimeSlot（出塊路徑，用 time.Now() 與 JamCommonEra 2025-01-01 12:00 UTC 相減）；STF test vectors 與 fuzzer trace 都不含 wall-clock，所以這條規則只在 live 節點的 gossip/import 路徑上有意義。",
 "trap": "「暫時無效」只適用於未來 slot；跳過的 slot（H_T > P(H)_t + 1）是合法的，不要跟未來 slot 混淆。"
},
{
 "id": "ch05-author-index-bound-set",
 "ch": "5", "section": "5 The Header", "gpRef": "eq. 5.10 & eq. 6.8 (valcount)",
 "difficulty": 3, "kind": "code", "tags": ["header", "validators", "delta-0.8.0", "fuzzer-bug", "code"],
 "stem": "After fuzzer bug #825 (a header with H_I = 65535 panicked UpdateEtaPrime0 with 'index out of range [65535] with length 6' because the index was used before being validated), the team added this check. Is the bound it uses the one GP 0.8.0 specifies?",
 "code": {"lang": "go", "caption": "internal/stf/validate_header.go (ValidateNonVRFHeader, excerpt)", "src": """	// Validate author_index out of range.
	// NOTE: There is currently no official error code defined for this case.
	// We may need to update this once the spec updates.
	if header.AuthorIndex >= types.ValidatorIndex(len(priorState.Kappa)) {
		errCode := SafroleErrorCode.AuthorIndexOutOfRange
		return &errCode
	}
	return nil
}"""},
 "options": [
  "Yes: eq. 5.10 defines H_I ∈ N_{|κ|} — the author must belong to the prior active set, because the block is built on the prior state and its seal is verified before the epoch's key rotation is applied, so len(priorState.Kappa) is exactly the spec bound and #825 needed nothing beyond moving the test ahead of UpdateEtaPrime0",
  "Not exactly: eq. 5.10 bounds H_I by |κ′| (the posterior active set, whose key also verifies H_S and H_V); the prior κ is equivalent only while |κ| = |κ′|, which holds today because the team never resizes the set, but 0.8.0 lets validator-set sizes differ across an epoch boundary (eq. 6.8)",
  "Yes: the bound is the constant V (1023 full / 6 tiny); κ and κ′ always hold exactly V entries in every configuration, so either length works and the choice of set is purely cosmetic — the only substantive fix for #825 was ordering the range test before the index is dereferenced",
  "No: H_I indexes the pending set γ_P, since the first block of an epoch is sealed by the incoming validators; the bound must therefore be |γ_P| read out of the prior Safrole state, because κ′ is only assigned once the seal has been verified and bounding H_I by it would be circular"
 ],
 "answer": 1,
 "optNotes": [
  "順序講反了：κ′ ≺ (H, τ, κ, γ) 先算出來、seal 驗證在其後，拿 κ′ 當上界沒有循環問題。",
  "eq. 5.10 的上界是 |κ′|；0.8.0 (#514) 起 |κ| 與 |κ′| 可在 epoch 交界不相等。",
  "eq. 6.8 的 𝕍 ≡ {3c | 2 ≤ c ≤ C} 允許長度變動，「V 是常數」是 0.7.2 的寫法。",
  "epoch 首塊時 κ′ 已經等於舊的 γ_P，index 的對象就是 κ′ 本身，不必繞道 γ_P。",
 ],
 "explanation": "eq. 5.10：H_I ∈ N_{|κ′|}，H_A ≡ κ′[H_I]_b——用的是 posterior active set（epoch 的第一個區塊由剛輪替進來的 κ′ = 舊 γ_P 出塊；#784/#791 就是因為用 prior κ/η 驗 seal 與 H_V 而失敗）。0.7.2 這裡的上界是常數 V；0.8.0（PR #514）改為 |κ′|，且 eq. 6.8 允許 validator 序列長度是 6 到 3C 之間任何 3 的倍數、designate 可以改變 ι 的長度。你們目前 |κ| ≡ |κ′| ≡ ValidatorsCount（offender 的 key 就地清零、不移除，issue #1037），所以 len(priorState.Kappa) 暫時等價；一旦支援變動大小，集合變大時會誤拒合法的 H_I ∈ [|κ|, |κ′|)，變小時會放過非法 index，接著在 η′_0 = H(η_0 ⌢ Y(H_V)) 或 seal 驗證取 κ′[H_I] 時再度 panic——正是 #825 的症狀。另一個重點：這個 bound check 必須排在所有使用 κ′[H_I] 的步驟（UpdateEtaPrime0、seal/VRF 驗證）之前——#825 的本質是「先用後驗」。",
 "trap": "H_I 對 κ′ 取 index，bound 也是 |κ′|；0.8.0 之後不要再把 V 當常數用。"
},
{
 "id": "ch07-beta-entry-timeslot-080",
 "ch": "7", "section": "7 Recent History", "gpRef": "eq. 7.2, 7.8 & eq. 11.36; §D.1 C(3)",
 "difficulty": 2, "kind": "delta", "tags": ["recent-history", "delta-0.8.0", "codec", "anchor"],
 "stem": "This 0.7.2 code builds the entry appended to β_H at the end of a block. What must change for GP 0.8.0, and which on-chain check motivates the change?",
 "code": {"lang": "go", "caption": "internal/recent_history/recent_history_controller.go (NewItem) — GP 0.7.2 checkout", "src": """// pack item $n$ (7.8) GP 0.6.7
/*
	item $n$ = (header hash $h$, accumulation-result mmr $b$, state root $s$, WorkReportHash $\\mathbf{p}$)
*/
func NewItem(headerHash types.HeaderHash, workReportHash []types.ReportedWorkPackage, accumulationResultMmr types.OpaqueHash) (item types.BlockInfo) {
	zeroHash := types.StateRoot{}
	item = types.BlockInfo{
		HeaderHash: headerHash,
		BeefyRoot:  accumulationResultMmr,
		StateRoot:  zeroHash,
		Reported:   workReportHash,
	}
	return item
}"""},
 "options": [
  "Add the block's timeslot t = H_T as a fifth field (E_4(t) between s and p under state key C(3)): refinement contexts now carry the anchor's timeslot and eq. 11.36 requires it to equal the t of the matching β† entry (GP PR #526; team PR #1031 threads H_T into NewItem)",
  "Replace the zero state root with the posterior root M_σ(σ′), because 0.8.0 headers now commit to the posterior state rather than the prior one; eq. 7.5's β† correction therefore disappears and eq. 11.36 can compare an anchor's state root against the very block that produced it",
  "Store the whole accumulation-output sequence θ′ in place of the super-peak b, because eq. 11.36 now compares the anchor's accumulation log entry by entry rather than against one commitment, which is also why 0.8.0 moved the belt out of C(3) and into its own state key",
  "Add the lookup-anchor posterior state root of every report guaranteed in the block, because 0.8.0 added that field to the refinement context and β_H is the only on-chain place where the value can be recorded — the ancestor set A holds headers, not the roots that follow them"
 ],
 "answer": 0,
 "optNotes": [
  "#526 讓 refinement context 帶上 anchor slot，鏈上要驗它，β 的每一筆就必須存 t。",
  "0.8.0 的 header 仍只帶 prior state root，state root 照舊填零、由下一塊的 β† 補正（eq. 7.5）。",
  "β 存的是 belt 的 super-peak 而不是整個 θ′；C(3) 至今仍同時裝 item 與 mmrencode(β_B)。",
  "lookup-anchor 的 posterior root 用 ancestor set 裡下一個 header 的 H_R 驗（eq. 11.38），不經過 β。",
 ],
 "explanation": "eq. 7.2（0.8.0）：β_H ∈ [(h, s, b, t ∈ N_T, p)]_{:H}——多了 timeslot；eq. 7.8 的新 entry 是 (H(H), H_0, M_R(β′_B), H_T, p)。動機：0.8.0 PR #526 在 refinement context（eq. 11.4）加入 anchor slot 與 lookup-anchor posterior state root，讓 refine 端能得知 anchor 的時間；鏈上要驗它，eq. 11.36 就變成：∃y ∈ β†：anchor hash = y_h ∧ anchor posterior state = y_s ∧ anchor accumulation log = y_b ∧ anchor time = y_t——其中 accumulation log 只比一個 32-byte super-peak，不是逐筆比對。狀態序列化（§D.1 的 C(3)）順序是 (h, b, s, E_4(t), var(p))——注意 b 在 s 之前，與 eq. 7.2 的 tuple 順序 (h, s, b, t, p) 不同；你們 BlockInfo 的欄位 HeaderHash, BeefyRoot, StateRoot, Reported 正是照序列化順序排，PR #1031 把 4-byte timeslot 插在 state_root 與 reported 之間。",
 "trap": "0.8.0 β_H 一項 = 5 欄；序列化順序 h, b, s, t, p（b 在 s 前）；anchor 的四個欄位全部要對上 β† 的同一筆。"
},
{
 "id": "ch07-belt-empty-output",
 "ch": "7", "section": "7 Recent History", "gpRef": "eq. 7.6–7.7 & eq. E.1, E.3",
 "difficulty": 3, "kind": "concept", "tags": ["recent-history", "mmr", "edge-case"],
 "stem": "Block N accumulates nothing that yields an output, so θ′ = []. What happens to the accumulation-output belt β_B and to the super-peak b written into block N's β_H entry?",
 "options": [
  "Nothing is appended and b repeats the parent's super-peak, so the belt holds one leaf per block that produced at least one accumulation output and BEEFY verifiers simply skip empty blocks",
  "An empty peak ∅ is appended to the peak sequence without any hashing, so the peak count grows by one while b stays unchanged until the next block with a non-empty θ′",
  "One leaf is still appended: M_B([], H_K) = N([], H_K) = H_0, so β′_B = A(β_B, H_0, H_K) and b = M_R(β′_B) changes — the belt always carries exactly one leaf per block since genesis",
  "The block's header hash H(H) is appended in place of the missing output root, so that the belt stays aligned one-to-one with the β_H entries and their header hashes"
 ],
 "answer": 2,
 "optNotes": [
  "eq. 7.7 沒有「θ′ 為空就跳過」的條件，belt 的 leaf 數等於創世以來的區塊數。",
  "∅ 只在 MMR 進位時作為空 peak 出現（eq. E.8 的 R(r, n, ∅)），不會因 θ′ 為空而被 append。",
  "M_B([], H_K) = N([], H_K) = H_0：空塊照樣 append 一片 H_0 的 leaf，super-peak 每塊都變。",
  "header hash 進的是 β_H 的 h 欄位，從來不會被 append 進 belt。",
 ],
 "explanation": "eq. 7.6–7.7：s = [E_4(s) ⌢ E(h) | (s, h) ∈ θ′]，β′_B ≡ A(β_B, M_B(s, H_K), H_K)。θ′ 來自 eq. 12.22/12.24 的 b = {(s, b) | b = yield 結果 ≠ ∅}——只有在 accumulate 裡呼叫 yield 的 service 才會出現，所以大多數區塊的 θ′ 都是空的。此時 s = []，依 eq. E.3：M_B(v, H) 在 |v| = 1 時為 H(v_0)，否則為 N(v, H)；再依 eq. E.1：N([], H) = H_0（零 hash）。你們的 lastAccOutRoot → merkle.Mb：len(v) == 0 時走 N 回傳 zeroHash，再交給 AppendOne（OpaqueHash 長度固定 32，不會被當成空值略過），行為一致。",
 "trap": "belt 是「每塊一片 leaf」的 MMR；空區塊的 leaf 是 H_0 不是 ∅。因此兩個相鄰的空區塊，其 β_H 的 b 也不相同。"
},
{
 "id": "ch08-leftmost-removal-code",
 "ch": "8", "section": "8.2 Pool and Queue", "gpRef": "eq. 8.3 (F) & eq. 11.25, 11.32",
 "difficulty": 2, "kind": "code", "tags": ["authorization", "code", "fuzzer-bug"],
 "stem": "Before PR #694 (bug #692) this removal deleted every occurrence of the used authorizer hash and ignored the report's core. Which statement correctly describes the GP rule the fixed code implements and why the old behaviour was wrong?",
 "code": {"lang": "go", "caption": "internal/authorization/authorization.go (updatePoolFromQueue) & internal/types/types.go (AuthPool.RemoveLeftMostPairedValue)", "src": """func updatePoolFromQueue(coreIndex types.CoreIndex, eg types.ReportGuarantee, alpha types.AuthPools) (types.AuthPools, error) {
	pool := alpha[coreIndex]
	if pool == nil {
		return nil, fmt.Errorf("alpha[%d] is nil", coreIndex)
	}

	// (8.3)   remove (g_r)a from α[c]（leftmost match）
	authHashToRemoved := eg.Report.AuthorizerHash
	pool.RemoveLeftMostPairedValue(authHashToRemoved)

	alpha[coreIndex] = pool
	return alpha, nil
}

func (a *AuthPool) RemoveLeftMostPairedValue(h OpaqueHash) {
	result := (*a)[:0]
	removed := false
	for _, v := range *a {
		if removed || !bytes.Equal(v[:], h[:]) {
			result = append(result, v)
		} else {
			removed = true
		}
	}
	*a = result
}"""},
 "options": [
  "eq. 8.2: the removal only makes room for the queue entry appended this block, so deleting every duplicate is harmless — α[c] is a set in which one authorizer hash can never occur twice, and the ←(…)^O truncation would have discarded any extra copies within eight blocks anyway",
  "eq. 11.32: the removal doubles as the pool-membership check, and a missing match must reject the block — so the old code was wrong only in failing to return an error when nothing matched, which is why the fix belongs in the guarantee validator rather than in the authorization state transition",
  "eq. 8.3, but the pool to edit must be found by looking the guarantors' validator indices up in the current rotation's assignment G, not by the core index stored inside the work-report — so a guarantee signed one rotation earlier edits whichever core those validators are sitting on now",
  "eq. 8.3: F(c) = α[c] ⊖ {w_a} removes one left-most instance from the pool of the report's own core; a pool is a sequence that may hold the same hash several times (e.g. a queue repeating one authorizer), so deleting every copy shrank pools and broke the test vectors"
 ],
 "answer": 3,
 "optNotes": [
  "eq. 8.1 的 α ∈ [[H]_{:O}]_C 是序列不是集合；pool 未滿時根本不截斷，多刪的 hash 永久消失。",
  "F(c) 不做驗證：w_a ∈ α[w_c] 早在 eq. 11.32 就對 prior α 檢查過了。",
  "要編輯哪個 pool 由 (g_w)_c 決定；eq. 11.28 允許 g_t 落在前一個 rotation，反推會挑到別的 pool。",
  "§3 的 s ⊖ {v} 是 excepting the left-most element equal to v，只移除最舊的那一個。",
 ],
 "explanation": "eq. 8.3：F(c) ≡ α[c] ⊖ {(g_w)_a} 當 ∃g ∈ E_G：(g_w)_c = c，否則 F(c) = α[c]。α[c] 是序列而非集合，重複完全合法：queue φ[c] 常常整排都是同一個 authorizer（例如某條 parachain 專用的 core），pool 裡自然會累積多個相同 hash；全部刪掉會讓 pool 憑空縮水，後續的 guarantee 就會因 eq. 11.32 找不到 authorizer 而被拒。而且這裡一定只需要移除一個：eq. 11.25 保證 E_G 每個 core 最多一個 guarantee、依 core 排序且不重複。#692 的修法正是「match the core index from report in guarantees」+「remove only the leftmost instance」。",
 "trap": "⊖（seqminusl）只砍最左邊一個；pool 與 queue 都是「序列」，允許重複。"
},
{
 "id": "ch08-new-authorizer-availability-timing",
 "ch": "8", "section": "8.2 Pool and Queue", "gpRef": "eq. 8.2, eq. 4.19 & eq. 11.32",
 "difficulty": 3, "kind": "concept", "tags": ["authorization", "guarantees", "ordering"],
 "stem": "At the start of block N the pool α[c] does not contain authorizer x. During block N's accumulation the assigner service of core c calls `assign` with a queue whose entry at index H_T mod Q is x, so x will be appended to core c's pool by this block. Block N's E_G also carries a guarantee for core c whose work-report has authorizer x. Is that guarantee valid, and when is x first usable?",
 "options": [
  "Valid: α′ is deliberately computed after accumulation so that guarantees in the same block can already rely on freshly assigned authorizers, which is why §8.2 orders the pool update last",
  "Invalid: eq. 11.32 requires w_a ∈ α[w_c] on the prior pool, and x only enters α′[c] through eq. 8.2 at the end of block N — so the first block whose E_G may carry a report authorized by x is N+1",
  "Valid: the authorizer check accepts any hash present in α[c] or in φ′[c], since the queue is the source of the pool and the assigner has already approved that authorizer for the core",
  "Invalid, but for a different reason: a single block may not both alter a core's queue via `assign` and accept a guarantee on that core, so the guarantee is rejected regardless of x"
 ],
 "answer": 1,
 "optNotes": [
  "α′ 要在 accumulation 之後才算，那是 α′ 的產生順序，不是 guarantee 驗證所看的狀態。",
  "eq. 11.32 比的是 prior α（無 prime、無 dagger），x 要等 block N 結束才進得了 α′[c]。",
  "guarantee 驗證不看 φ：queue 只是 pool 的補給來源，本身不是授權依據。",
  "GP 沒有「同一塊不能同時 assign 與 guarantee 同一個 core」這條規則。",
 ],
 "explanation": "eq. 11.32：∀w ∈ w：ρ‡[w_c] = ∅ ∧ w_a ∈ α[w_c]。依賴圖 eq. 4.19：α′ ≺ (H, E_G, φ′, α)，表示 E_G 是 α′ 的輸入而不是反過來——所以 x 要到 block N 結束時才進入 α′[c]，block N+1 的 prior α 才含 x。實務含意：assigner 想讓新 authorizer 可用，最快也是下一個 slot；而且 pool 每塊都會 append 一個 queue 項目，x 進 pool 後若一直沒被使用、pool 又沒被其他 guarantee 消耗，最多再 8 個區塊就會被 ←^O 擠掉，所以 queue 的安排要與預期的 package 提交時間對齊。你們 STF 的順序（ValidateExtrinsic → UpdateReports → UpdateAccumlate → UpdateAuthorizations）也正是先用 prior α 驗 guarantee、最後才產生 α′。",
 "trap": "guarantee 看 prior α；α′ 用 posterior φ′。新 authorizer 最早在「下一個區塊」才可用。"
},
]
