# -*- coding: utf-8 -*-
# Batch 2 — Chapter 5 (The Header), Chapter 7 (Recent History), Chapter 8 (Authorization) — GP 0.8.0
# Complements items/ch05_header.py and items/ch07_ch08.py (no overlap with their stems).
ITEMS = [
{
 "id": "ch05-unsigned-header-serialization",
 "ch": "5", "section": "5 The Header (serialization, Appendix C.2)", "gpRef": "eq. 5.1 & §C.2 (E(H), E_U(H))",
 "difficulty": 2, "kind": "code", "tags": ["header", "codec", "seal", "code"],
  "stemZh": "團隊是靠「把完整 header 編碼後截斷」來導出未簽署的 header 序列化。關於 GP 0.8.0 的 E(H) 與 E_U(H)，哪個敘述既說明了這樣做為何成立、又正確描述了 E_U 的版面？",
  "optionsZh": [
   "E_U(H) 省略了**兩個** Bandersnatch 簽章——熵來源 H_V 與 seal H_S——所以合規的實作必須從 E(H) 切掉 192 個 octet，而 seal 的訊息裡完全不含 VRF 材料，這正是阻止兩個簽章互相依賴的原因",
   "E(H) = E(E_U(H), H_S)：96 位元組的 seal 是最後一個定長欄位，所以從 E(H) 切掉 96 位元組恰好得到 seal 的訊息；E_U 內部的順序是 H_P、H_R、H_X、E_4(H_T)、H_E（0/1 判別子）、H_W（0/1 判別子）、E_2(H_I)、H_V、var(H_O)",
   "E_U(H) 是把 E(H) 的 seal 換成 96 個零位元組、保持 header 長度不變，好讓 H_P 能在封印之前算出來；因此單純截斷得到的訊息會短了 96 個 octet，實作必須改為以歸零的 seal 重新編碼",
   "序列化的欄位順序完全照 eq. 5.1（…、H_W、var(H_O)、E_2(H_I)、H_V、H_S），所以只有在 H_O 為空時截掉最後 96 個 octet 才正確，因為帶長度前綴的 offender 清單會位移它之後的每一個欄位，包括 seal"
  ],
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
  "stemZh": "某個輕客戶端只持有一個已驗證的 header H，想確認 service s 的 preimage blob d 有被納入該區塊的 E_P。已知 H_X = H(E(H#(a)))、a = [E_T(E_T), p, g, E_A(E_A), E_D(E_D)]（eq. 5.4–5.7），它需要的最小見證是什麼？檢查的形狀又是什麼？",
  "optionsZh": [
   "一條長度為 log₂|E_P| 的 Merkle 路徑，從葉子 H(d) 一路到 H_X，因為 H_X 是對該區塊每一個 extrinsic 項目所取的二元 Merkle root，所以見證是 O(log n) 個雜湊、只隨區塊變滿而對數成長",
   "完整的 E_P（該區塊的每一份 preimage blob）連同其餘四個 extrinsic 的完整內容，因為 H_X 是把該區塊整份 extrinsic 序列化當成一個 blob 來雜湊、無法只從雜湊重算出來",
   "其餘四個成分的雜湊（h_T、h_g、h_A、h_D）加上完整的 p 序列（(E_4(s_i), H(d_i)) 配對）：它檢查 (E_4(s), H(d)) ∈ p 且 H(h_T ⌢ H(p) ⌢ h_g ⌢ h_A ⌢ h_D) = H_X——不需要其他任何 blob，但 p 是一個扁平的 blob 而不是對數大小的路徑",
   "只需要 H(d)、service 索引 s 與該區塊的 H_X，因為 eq. 5.6 把每一組 (service, preimage 雜湊) 直接承諾進 H_X，所以單一組配對不必碰 E_P 的其餘部分、也不必碰其他四個 extrinsic 成分就能檢查"
  ],
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
  "stemZh": "某個節點在牆鐘時間 T 收到一個區塊，其 header 滿足 H_T · P > T，同時 P(H)_t < H_T 也成立（父區塊已知且較舊）。GP §5 如何歸類這個區塊？",
  "optionsZh": [
   "它是永久無效的；而且因為提前於時鐘出塊是一種違規，該出塊者的 Ed25519 金鑰必須在下一塊的 disputes extrinsic 中以 culprit 身分進入 ψ_O，所以節點應該丟棄該 header 而不是留著",
   "只要偏移小於一個時槽週期 P = 6 秒它就是有效的，GP 明確給了這個時鐘偏移容忍度，好讓在時槽最開頭出塊的誠實出塊者不會被時鐘略慢的對等節點拒絕",
   "它是有效的：只有排序規則 P(H)_t < H_T 屬於共識，而牆鐘的比較只是出塊時的指引——這正是為什麼 STF 測試向量裡完全沒有 T 這個概念，而匯入節點必須接受該區塊",
   "它目前不滿足 eq. 5.8，但 GP 註明這類區塊「may become valid as T advances」——與 H_T ≤ P(H)_t 那種永遠不可能變有效的區塊不同，它只是**暫時**無效，日後可以重新評估"
  ],
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
  "stemZh": "在 fuzzer bug #825（一個 H_I = 65535 的 header 讓 UpdateEtaPrime0 以「index out of range [65535] with length 6」panic，因為該索引在被驗證之前就被使用）之後，團隊加了這個檢查。它用的界限是 GP 0.8.0 所規定的那一個嗎？",
  "optionsZh": [
   "是：eq. 5.10 定義 H_I ∈ N_{|κ|}——出塊者必須屬於 **prior** 的 active set，因為該區塊建立在 prior 狀態上、而它的 seal 是在該 epoch 的金鑰輪換套用之前就被驗證的，所以 len(priorState.Kappa) 正是規格的界限，#825 需要的只是把這個測試移到 UpdateEtaPrime0 之前",
   "不完全是：eq. 5.10 是以 |κ′|（posterior 的 active set，其金鑰同時也用來驗證 H_S 與 H_V）為 H_I 的界限；prior 的 κ 只有在 |κ| = |κ′| 時才等價，而這在今天成立只是因為團隊從不調整集合大小，但 0.8.0 允許 validator 集合大小跨 epoch 邊界改變（eq. 6.8）",
   "是：那個界限就是常數 V（full 1023／tiny 6）；κ 與 κ′ 在每一種設定下都恰好持有 V 項，所以用哪個長度都行、選哪個集合純粹是形式問題——#825 唯一實質的修正就是把範圍測試排到索引被解參考之前",
   "不對：H_I 索引的是 pending set γ_P，因為一個 epoch 的第一塊是由**新進**的 validator 封印的；因此界限必須是從 prior 的 Safrole 狀態讀出的 |γ_P|，因為 κ′ 要等 seal 驗證完才被指派，用它來界定 H_I 會構成循環"
  ],
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
  "stemZh": "這段 0.7.2 的程式碼建構的是在區塊結尾附加到 β_H 的那一筆條目。為了 GP 0.8.0 必須改什麼？又是哪一項鏈上檢查促成了這個改動？",
  "optionsZh": [
   "加上該區塊的時槽 t = H_T 作為第五個欄位（在 state key C(3) 之下、s 與 p 之間放 E_4(t)）：refinement context 現在會攜帶 anchor 的時槽，而 eq. 11.36 要求它必須等於相符的那筆 β† 條目的 t（GP PR #526；團隊 PR #1031 把 H_T 串進 NewItem）",
   "把那個零 state root 換成執行後的 root M_σ(σ′)，因為 0.8.0 的 header 現在承諾的是 posterior 而非 prior 狀態；因此 eq. 7.5 的 β† 修正就消失了，而 eq. 11.36 可以把 anchor 的 state root 拿去和產生它的那個區塊直接比對",
   "用完整的 accumulation-output 序列 θ′ 取代 super-peak b，因為 eq. 11.36 現在是逐項比對 anchor 的 accumulation log 而不是比對單一個承諾，這也是 0.8.0 把 belt 從 C(3) 移到它自己的 state key 的原因",
   "加上該區塊中每份被擔保 report 的 lookup-anchor posterior state root，因為 0.8.0 把那個欄位加進了 refinement context，而 β_H 是鏈上唯一能記錄該值的地方——祖先集合 A 存的是 header，不是它們之後的 root"
  ],
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
  "stemZh": "區塊 N 沒有 accumulate 出任何產出，所以 θ′ = []。accumulation-output belt β_B 以及寫進區塊 N 之 β_H 條目的 super-peak b 會怎麼樣？",
  "optionsZh": [
   "什麼都不會被附加，而 b 沿用父區塊的 super-peak，所以 belt 只對「至少產出一個 accumulation output」的區塊各持有一片葉子，BEEFY 的驗證者則單純跳過空區塊",
   "一個空的 peak ∅ 會被附加到 peak 序列上、完全不做雜湊，所以 peak 數增加一個、而 b 維持不變直到下一個 θ′ 非空的區塊",
   "仍然會附加一片葉子：M_B([], H_K) = N([], H_K) = H_0，所以 β′_B = A(β_B, H_0, H_K) 而 b = M_R(β′_B) 也會改變——belt 自創世以來永遠是每個區塊恰好一片葉子",
   "該區塊的 header 雜湊 H(H) 會取代缺席的 output root 被附加上去，好讓 belt 與 β_H 的條目及其 header 雜湊保持一對一對齊"
  ],
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
 "explanation": "關鍵是 **belt 每塊必定長一片葉子，即使本塊什麼都沒產出**。θ′ 來自 eq. 12.22／12.24：只有在 accumulate 裡呼叫 `yield` 且回傳非 ∅ 的 service 才會出現在裡面，所以**多數區塊的 θ′ 都是空的**——這不是特例而是常態。此時 s = []（eq. 7.6 的映射對空序列就是空序列），接著看附錄 E：eq. E.3 定義 M_B(v, H) 在 |v| = 1 時為 H(v_0)、否則走 N(v, H)；eq. E.1 定義 N([], H) = H_0（零雜湊）。所以 M_B([], H_K) = H_0，β′_B = A(β_B, H_0, H_K) 照樣 append 一片，b = M_R(β′_B) 也照樣改變。**為什麼要這樣設計**：belt 是 MMR，第 i 個 peak 代表 2^i 個項——若空區塊不 append，「第 n 片葉子」就不再對應「第 n 個區塊」，外部拿著區塊高度來索引證明的系統（BEEFY 橋接）就得額外維護一張對照表。每塊一片、從 genesis 起算，索引才能直接等於高度。**實作陷阱**：H_0 是 32 個零位元組，是一個**合法的雜湊值**而不是「空值」。你們的 lastAccOutRoot → merkle.Mb 在 len(v) == 0 時回傳 zeroHash 再交給 AppendOne，因為 OpaqueHash 長度固定 32，不會被誤判成 nil 而略過——這正是要小心的地方。",
 "trap": "belt 是「每塊一片 leaf」的 MMR；空區塊的 leaf 是 H_0 不是 ∅。因此兩個相鄰的空區塊，其 β_H 的 b 也不相同。"
},
{
 "id": "ch08-leftmost-removal-code",
 "ch": "8", "section": "8.2 Pool and Queue", "gpRef": "eq. 8.3 (F) & eq. 11.25, 11.32",
 "difficulty": 2, "kind": "code", "tags": ["authorization", "code", "fuzzer-bug"],
  "stemZh": "在 PR #694（bug #692）之前，這段移除邏輯會刪掉被使用之 authorizer 雜湊的**每一個**出現、而且忽略該 report 的 core。哪個敘述正確描述了修正後程式碼所實作的 GP 規則、以及舊行為為何是錯的？",
  "optionsZh": [
   "eq. 8.2：這次移除只是為了給本塊附加的佇列項目騰出位置，所以刪掉每一個重複是無害的——α[c] 是一個集合、同一個 authorizer 雜湊不可能出現兩次，而且 ←(…)^O 的截斷反正會在八個區塊內丟掉任何多餘的副本",
   "eq. 11.32：這次移除同時兼作 pool 成員檢查，而找不到相符者就必須拒絕該區塊——所以舊程式碼唯一的錯是沒在無匹配時回傳錯誤，這也是為什麼修正應該放在 guarantee 驗證器而不是授權的狀態轉移裡",
   "eq. 8.3，但要編輯哪個 pool 必須靠把 guarantor 的 validator 索引拿到**當前 rotation** 的指派 G 裡查出來，而不是靠 work-report 內部記錄的 core 索引——所以一份在前一個 rotation 簽署的 guarantee 會去編輯那些 validator 現在所在的 core",
   "eq. 8.3：F(c) = α[c] ⊖ {w_a} 是從**該 report 自己那個 core** 的 pool 中移除最左邊的一個實例；pool 是序列、可以持有同一個雜湊數次（例如某個佇列反覆排入同一個 authorizer），所以刪掉每一個副本會讓 pool 憑空縮水、並使測試向量對不上"
  ],
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
 "explanation": "eq. 8.3：F(c) ≡ α[c] ⊖ {(g_w)_a} 當 ∃g ∈ E_G 且該 guarantee 的 report 指向 core c，否則 F(c) = α[c]。⊖ 是 sequence-minus-leftmost：**只移除最左邊那一個符合的元素**。**為什麼「刪掉全部」是錯的**：α[c] 是**序列不是集合**，同一個 authorizer hash 重複出現完全合法——queue φ[c] 很可能整排都排同一個 authorizer（例如某條專用 core），每個時槽補一筆進 pool，pool 裡自然會累積多個相同的 hash。這些重複代表的是**可用額度**：有幾個就能用幾次。一次全刪等於把剩餘額度一併沒收，pool 憑空縮水，後續 guarantee 就會在 eq. 11.32（w_a ∈ α[w_c]）找不到 authorizer 而被拒——測試向量因此對不上。**為什麼只需要移除一個就夠**：eq. 11.25 保證 E_G 裡每個 core 至多一個 guarantee、且依 core index 排序不重複，所以一塊之內同一個 core 不會消耗兩次。**還有第二個錯**：舊實作忽略了 report 的 core index，等於在錯的 core 的 pool 上做移除。#692 的修法正是兩件事一起補——比對 report 的 core、且只移除最左邊一個。",
 "trap": "⊖（seqminusl）只砍最左邊一個；pool 與 queue 都是「序列」，允許重複。"
},
{
 "id": "ch08-new-authorizer-availability-timing",
 "ch": "8", "section": "8.2 Pool and Queue", "gpRef": "eq. 8.2, eq. 4.19 & eq. 11.32",
 "difficulty": 3, "kind": "concept", "tags": ["authorization", "guarantees", "ordering"],
  "stemZh": "在區塊 N 開始時，pool α[c] 並不含 authorizer x。在區塊 N 的 accumulation 期間，core c 的 assigner service 呼叫 `assign`，其佇列在索引 H_T mod Q 處的項目是 x，所以 x 會在這一塊被附加進 core c 的 pool。而區塊 N 的 E_G 也帶了一份指向 core c 的 guarantee，其 work-report 的 authorizer 正是 x。這份 guarantee 有效嗎？x 最快什麼時候可用？",
  "optionsZh": [
   "有效：α′ 之所以刻意排在 accumulation 之後計算，正是為了讓同一塊裡的 guarantee 已經能倚賴剛被指派的 authorizer，這也是 §8.2 把 pool 更新排在最後的原因",
   "無效：eq. 11.32 要求 w_a ∈ α[w_c]，用的是 **prior** 的 pool，而 x 要到區塊 N 結束時才經由 eq. 8.2 進入 α′[c]——所以第一個可以帶著由 x 授權之 report 的區塊是 N+1",
   "有效：authorizer 的檢查接受任何出現在 α[c] **或** φ′[c] 中的雜湊，因為佇列就是 pool 的來源，而 assigner 已經為該 core 核准了那個 authorizer",
   "無效，但理由不同：同一個區塊不得既透過 `assign` 改動某個 core 的佇列、又接受該 core 上的 guarantee，所以不論 x 是什麼，這份 guarantee 都會被拒絕"
  ],
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
 "explanation": "答案落在**依賴圖的方向**上。eq. 4.19：α′ ≺ (H, E_G, φ′, α)——讀作「α′ 由 header、本塊的 E_G、posterior 的 φ′ 與 prior 的 α 共同決定」，也就是 **E_G 是 α′ 的輸入，不是反過來**。而 eq. 11.32 檢查 guarantee 時要求 w_a ∈ α[w_c]——用的是 **prior 的 α**。所以 assigner 在本塊 accumulate 期間呼叫 `assign` 寫進 φ′，x 要等到本塊結束、經由 eq. 8.2 才進入 α′[c]；**最快能使用 x 的是下一個區塊 N+1**（那時它才是 prior α 的一部分）。本題的 guarantee 因此無效。**實務上要注意的第二件事**：pool 每塊都會 append 一筆（即使沒有 guarantee 消耗），而 ←(…)^O 只保留最後 O = 8 個。所以 x 進了 pool 之後若一直沒被用到，**最多再過 8 個區塊就會被擠掉**——assigner 安排 queue 的時機必須與預期的 work-package 提交時間對齊，太早排入等於白排。你們 STF 的順序（ValidateExtrinsic → UpdateReports → UpdateAccumlate → UpdateAuthorizations）正好體現這個方向：先用 prior α 驗 guarantee，最後才產生 α′。",
 "trap": "guarantee 看 prior α；α′ 用 posterior φ′。新 authorizer 最早在「下一個區塊」才可用。"
},
]
