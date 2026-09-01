# -*- coding: utf-8 -*-
# Batch 2 — Appendices C (Serialization Codec), D (State Merklization), E (General Merklization & MMR),
# F (Shuffling), G (Bandersnatch VRF / signing contexts), H (Erasure Coding) — GP 0.8.0
ITEMS = [
{
 "id": "appC-code-avspec-080",
 "ch": "C", "section": "C.2 Block Serialization (availability specification)", "gpRef": "§C.2 E(s ∈ availability spec); eq. 11.5; eq. 11.31",
 "difficulty": 2, "kind": "code", "tags": ["codec", "availability-spec", "delta-0.8.0"],
  "stemZh": "團隊為 availability specification（work-package spec）寫的編碼器還停在 GP 0.7.2。要讓它產出 §C.2 的 GP 0.8.0 線路格式 E(s)，必須改什麼？伴隨這個新欄位的鏈上規則又是什麼？",
  "optionsZh": [
   "在 ErasureRoot 與 ExportsRoot 之間插入一個 U16 的 erasure 碎片數 v，編碼為 E_2(v)；其餘寬度維持原樣（長度用 E_4、exports 計數用 E_2）；鏈上則要求每一份進來的 report 都必須帶 v = |κ′|",
   "把 E_2(v) 附加在 ExportsCount **之後**，因為自 GP 0.7.0 起，結構新增的任何欄位都必須放到尾端以維持解碼器的串流友善性；鏈上則要求 v 必須等於 core 數 C",
   "把定寬的 E_4 Length 換成緊湊的 E(l)，並在其後緊接著加上緊湊自然數 v；v 就是該 guarantor 實際分發出去的碎片數量，所以鏈上不做檢查",
   "線路上什麼都不用改：v 可以從 validator 數 V 推導出來，因此從不被序列化；只有 JSON 測試向量的 schema 為了可讀性多了一個 erasure_shards 欄位"
  ],
  "stem": "The team's encoder for the availability specification (work-package spec) is still on GP 0.7.2. What must change so that it produces the GP 0.8.0 wire form E(s) of §C.2, and which on-chain rule accompanies the new field?",
 "code": {"lang": "go", "caption": "internal/types/encode.go (WorkPackageSpec.Encode) — struct fields: Hash, Length U32, ErasureRoot, ExportsRoot, ExportsCount U16", "src": "func (w *WorkPackageSpec) Encode(e *Encoder) error {\n\tcLog(Cyan, \"Encoding WorkPackageSpec\")\n\n\t// Hash\n\tif err := w.Hash.Encode(e); err != nil {\n\t\treturn err\n\t}\n\n\t// Length\n\tif err := w.Length.Encode(e); err != nil {\n\t\treturn err\n\t}\n\n\t// ErasureRoot\n\tif err := w.ErasureRoot.Encode(e); err != nil {\n\t\treturn err\n\t}\n\n\t// ExportsRoot\n\tif err := w.ExportsRoot.Encode(e); err != nil {\n\t\treturn err\n\t}\n\n\t// ExportsCount\n\tif err := w.ExportsCount.Encode(e); err != nil {\n\t\treturn err\n\t}\n\n\treturn nil\n}"
 },
 "options": [
  "Insert a U16 erasure-shard count v, encoded E_2(v), between ErasureRoot and ExportsRoot; the other widths stay as they are (E_4 length, E_2 exports count); on-chain every incoming report must carry v = |κ′|",
  "Append E_2(v) after ExportsCount, because since GP 0.7.0 any newly added field of a structure must go to its end to keep decoders streaming-friendly; on-chain v must equal the number of cores C",
  "Replace the fixed E_4 Length with a compact E(l) and add v as a compact natural right after it; v is whatever number of chunks the guarantor actually distributed, so it is not checked on-chain",
  "Nothing on the wire: v is derivable from the validator count V and is therefore never serialized; only the JSON test-vector schema gains an erasure_shards field for readability"
 ],
 "answer": 0,
 "optNotes": [
   "§C.2 把 E_2(v) 排在 u 與 e 之間，且 eq. 11.31 要求 (w_s)_v = |κ′|——每個 assurer 恰一個 chunk。",
   "「新欄位排最後」只針對變長（↕）欄位；v 是固定 2 octets、位置由 GP 明定，而且 v 不是 C。",
   "長度 l 仍是 E_4 而非 compact，v 也不是 guarantor 自由決定的——eq. 11.31 在鏈上檢查它。",
   "v 必須進 wire，否則另一個 validator-set 大小的 assurer 無從驗證這份 report。",
 ],
 "explanation": "GP 0.8.0 §C.2：E(s ∈ availability spec) ≡ E(p, E_4(l), u, E_2(v), e, E_2(n))——依序是 package hash p、bundle 長度 l（E_4）、erasure root u、erasure-shard 數 v（E_2）、segment root e、segment 數 n（E_2）。eq. 11.5 把 v ∈ N_V（validator count 型別）放在 u 與 e 之間；eq. 11.31：∀w ∈ 進來的 reports：(w_s)_v = |κ′|，因為「one chunk is distributed to each assurer, the number of chunks must equal the size of the assuring validator set」。0.8.0 的 erasure coding 以 v 為參數（§14.4.1 的 A(p, b, s, v) 用 z = 2·d(v)），所以規格本身要記錄 v；GP 也註明對兩個不同大小的 validator set 派發時要做兩次 erasure coding、產生兩份不同的 work-report。你們的 PR #1026 就是在 ErasureRoot 與 ExportsRoot 之間加 `ErasureShards U16`（producer 設為 TotalShards），這會改變每一個 on-chain WorkReport 的位元組佈局（進而影響 report hash、guarantee 簽名、ρ 內容）。",
 "trap": "0.7.2 五欄位 (p, l, u, e, n) → 0.8.0 六欄位 (p, l, u, v, e, n)；v 是 E_2 且必須等於 |κ′|。"
},
{
 "id": "appC-code-operand-transfer-prefix",
 "ch": "C", "section": "C.2 Block Serialization (operand tuple and deferred transfer)", "gpRef": "§C.2 E(deferred transfer), E(operand tuple); eq. B.9; §B.4 fetch cases 14–15; eq. 12.13–12.14",
 "difficulty": 2, "kind": "code", "tags": ["codec", "accumulation", "deferred-transfer", "fetch"],
  "stemZh": "團隊在每個 accumulate 輸入項目的本體之前加了一個位元組作為前綴。依 GP 0.8.0，關於這兩種前綴、以及究竟是誰在消費這個編碼，哪一種解釋是正確的？",
  "optionsZh": [
   "這兩個前綴就是 GP 放在 E(運算元組)（0）與 E(deferred transfer)（1）之前的判別子；Ψ_A 收下的是單一個混合序列 i ∈ ⟦運算元 ∪ transfer⟧，而 service 透過 fetch（case 14／15）把它讀回來，所以每個項目都必須自我描述",
   "這兩個前綴分隔的是 accumulate 記憶體映像的兩半：Ψ_M 的初始引數 E(t, s, |i|) 之後，先寫入每個運算元（前綴 0）、再寫入每筆 transfer（前綴 1）到 RAM 裡，所以 fetch 只需要服務 work-package 的資料，也沒有任何東西需要自我描述",
   "那個前綴是 GP 0.7.1 引入的帳戶序列化版本位元組（0 = 舊版運算元版面、1 = 帶 128 位元組 memo 的 transfer 版面）；Ψ_A 收下的是兩個各自獨立的序列（一個運算元、一個 transfer），而 0.8.0 因為兩者不再共用序列而拿掉了那個位元組",
   "這些前綴只是團隊為了 JSON 測試向量而定的慣例；線路上 GP 把所有 transfer 排在所有運算元之前，並以固定長度區分兩者（transfer 本體為 152 個 octet）；service 則從 Ψ_M 的初始引數得知這個分界，因為那個引數帶的是兩個計數而不是單一個總數"
  ],
  "stem": "The team prefixes each accumulate input item with a byte before its body. Which explanation of the two prefixes and of what actually consumes this encoding is correct per GP 0.8.0?",
 "code": {"lang": "go", "caption": "internal/types/encode.go (OperandOrDeferredTransfer.Encode)", "src": "func (o *OperandOrDeferredTransfer) Encode(e *Encoder) error {\n\tcLog(Cyan, \"Encoding OperandOrDeferredTransfer\")\n\n\t// if operand is nil, append 0 to the buffer, else append 1\n\tif o.Operand == nil && o.DeferredTransfer == nil {\n\t\treturn errors.New(\"Operand and DeferredTransfer are both nil\")\n\t}\n\t// ...\n\t// Operand\n\tif o.Operand != nil {\n\t\t// prefix\n\t\te.buf.Write([]byte{0})\n\n\t\tif err := o.Operand.Encode(e); err != nil {\n\t\t\treturn err\n\t\t}\n\t}\n\n\t// DeferredTransfer\n\tif o.DeferredTransfer != nil {\n\t\t// prefix\n\t\te.buf.Write([]byte{1})\n\n\t\tif err := o.DeferredTransfer.Encode(e); err != nil {\n\t\t\treturn err\n\t\t}\n\t}\n\n\treturn nil\n}"},
 "options": [
  "The prefixes are the discriminators GP puts in front of E(operand tuple) (0) and E(deferred transfer) (1); Ψ_A takes one mixed sequence i ∈ ⟦operand ∪ transfer⟧ and the service reads it back through fetch (cases 14/15), so each item must be self-describing",
  "The prefixes separate the two halves of the accumulate memory image: Ψ_M's initial argument E(t, s, |i|) is followed by every operand (prefix 0) and then every transfer (prefix 1) written into RAM at start-up, so fetch only ever has to serve work-package data and nothing needs to be self-describing",
  "The prefix is the account-serialization version byte introduced in GP 0.7.1 (0 = legacy operand layout, 1 = transfer layout with the 128-octet memo); Ψ_A takes two separate sequences, one of operands and one of transfers, and 0.8.0 drops the byte because the two never share a sequence",
  "The prefixes are a team convention for the JSON test vectors only; on the wire GP orders all transfers before all operands and tells them apart by fixed length, a transfer body being 152 octets; the service learns the split from Ψ_M's initial argument, which carries both counts rather than one total"
 ],
 "answer": 0,
 "optNotes": [
   "Ψ_M 的初始參數只有 E(t, s, |i|)，項目靠 fetch 14/15 讀回，所以每一項必須自我描述。",
   "初始記憶體只含數量不含 i 的內容；§B.4 的 φ_10 = 14／15 回的正是 E(↕i) 與 E(i[φ_11])。",
   "0.7.1 的 version byte 是 C(255, s) 值的開頭；eq. B.9 收的仍是 operand ∪ transfer 的混合序列。",
   "GP 沒有「transfer 在前、靠固定長度分辨」的規則——operand 的 ↕t 與 O(l) 本來就是變長。",
 ],
 "explanation": "GP §C.2 明確定義 E(x ∈ deferred transfer) ≡ E(1, E_4(s), E_4(d), E_8(a), m, E_8(g))（memo m 固定 128 octets、不加長度前綴）以及 E(x ∈ operand tuple) ≡ E(0, p, e, a, y, g, O(l), ↕t)——開頭的 1/0 就是 discriminator。為什麼需要：eq. B.9 的 Ψ_A 接收的是 i ∈ ⟦operand tuple ∪ deferred transfer⟧ 這種『混合序列』（eq. 12.13–12.14，accumulation.tex：「the union of the two characterizes inputs to the Accumulation invocation function」）；Ψ_M 的初始參數只有 E(t, s, |i|)，項目本身是服務透過 fetch host call 讀回：§B.4 的 fetch 在 φ_10 = 14 時回傳 E(↕i)、15 時回傳 E(i[φ_11])。沒有 discriminator，服務無法分辨讀到的是 operand 還是 transfer。你們的實作正好對應：operand 用 0、transfer 用 1，Operand.Encode 的 GasLimit 走 EncodeInteger（compact，與 GP 的 g 一致），AuthOutput 帶長度前綴。",
 "trap": "1 = transfer、0 = operand；memo 128 octets 無前綴；fetch 14/15 把整段 E(↕i) 或單一 E(i[k]) 交給服務。"
},
{
 "id": "appD-code-service-info-key",
 "ch": "D", "section": "D.1 Serialization (state-key constructor C)", "gpRef": "§D.1 state-key constructor C (unlabelled first equation of appendix D)",
 "difficulty": 3, "kind": "code", "tags": ["merklization", "state-keys", "fuzzer-bug"],
  "stemZh": "在 PR #780 之前，團隊只靠測試 stateKey[0] == 0xFF 來辨認 service-info key C(255, s)，而 fuzzer 的 trace 以「failed to decode expected service info from state key 0xffff0017…: EOF」失敗。為什麼單看第 0 個位元組會有歧義？現在的檢查又為什麼是可靠的？",
  "optionsZh": [
   "C(s, h) 的 key 以 n_0（也就是 E_4(s) 的低位位元組）開頭，所以每一個 s mod 256 = 255 的 service，其 storage／preimage／request key 都會以 0xFF 開頭；新的檢查另外要求所有非 service-id 位置都為零，而一個由 Blake2b 導出的 key 要符合這點的機率可忽略不計",
   "id 大於 2^24 的 service，其 C(255, s) key 會把第四個 id 位元組溢出到位置 9，所以單看第 0 個位元組無法把它們與章節 key C(9)…C(16) 分開；因此修法是跳過位置 1、3、5、7，並且也容忍位置 9",
   "因為 C(s, h) 是把 service id 與 key 一起雜湊，所以這種 key 的每一個位元組（包括第一個）都是均勻隨機的，於是大約 1/256 的 key 會以 0xFF 開頭；修法是把整個 key 重新雜湊一次，讓 0xFF 前綴變得不可能出現",
   "accumulation-output 分量 θ 的章節 key C(255) 與 C(255, s) 共用第一個位元組；修法是要求位置 1、3、5、7 帶非零的 service id、其餘位置全為零，以此區分兩者"
  ],
  "stem": "Before PR #780 the team recognised a service-info key C(255, s) by testing only stateKey[0] == 0xFF, and fuzzer traces failed with 'failed to decode expected service info from state key 0xffff0017…: EOF'. Why was byte 0 alone ambiguous, and why is the current check sound?",
 "code": {"lang": "go", "caption": "internal/utilities/merklization/parse_state_key_vals.go (IsServiceInfoKey) + state_key_constructor.go (ServiceWrapper.StateKeyConstruct)", "src": "func IsServiceInfoKey(stateKey types.StateKey) bool {\n\tif stateKey[0] != 0xFF {\n\t\treturn false\n\t}\n\tfor i := 1; i < len(stateKey); i++ {\n\t\tif i == 1 || i == 3 || i == 5 || i == 7 {\n\t\t\tcontinue\n\t\t}\n\t\tif stateKey[i] != 0 {\n\t\t\treturn false\n\t\t}\n\t}\n\treturn true\n}\n\n// [n_0, h_0, n_1, h_1, n_2, h_2, n_3, h_3, h_4, h_5,...,h_26] where n = encode_4(service_id)\nfunc (w ServiceWrapper) StateKeyConstruct() (output types.StateKey) {\n\tn := encodeServiceID(w.ServiceIndex)\n\ta := hash.Blake2bHashPartial(w.h[:], 27)\n\tfor i := 0; i <= 3; i++ {\n\t\toutput[2*i] = n[i]\n\t\toutput[2*i+1] = a[i]\n\t}\n\tfor i := 4; i <= 26; i++ {\n\t\toutput[i+4] = a[i]\n\t}\n\treturn output\n}"},
 "options": [
  "C(s, h) keys start with n_0, the low octet of E_4(s), so every service with s mod 256 = 255 yields storage/preimage/request keys beginning 0xFF; the new check also requires zeros in all non-service-id positions, which a Blake2b-derived key matches only with negligible probability",
  "C(255, s) keys for service ids above 2^24 spill their fourth id octet into position 9, so byte 0 alone cannot separate them from the chapter keys C(9)…C(16); the fix therefore skips positions 1, 3, 5, 7 and tolerates position 9 as well",
  "Because C(s, h) hashes the service id together with the key, every octet of such a key — the first one included — is uniformly random, so about 1/256 of them start with 0xFF; the fix re-hashes the whole key so the 0xFF prefix becomes unreachable",
  "The chapter key C(255) of the accumulation-output component θ shares its first octet with C(255, s); the fix tells them apart by demanding a non-zero service id in positions 1, 3, 5, 7 and zeros everywhere else"
 ],
 "answer": 0,
 "optNotes": [
   "C(s, h) 的第 0 個 octet 是 n_0（service id 的最低 byte），s ≡ 255 (mod 256) 就會撞上 0xFF。",
   "service id 只佔位置 1、3、5、7 四個 octet，任何 32-bit id 都放得下，不會溢出到位置 9。",
   "C(s, h) 並沒有把 service id 混進 hash，第 0 個 byte 是 n_0 而非隨機，修正也沒有再 hash 一次。",
   "chapter key 只有 C(1)…C(16)（θ 是 C(16)），根本不存在 C(255) 這個單一元件 key。",
 ],
 "explanation": "§D.1：C(i) = [i, 0, 0, …]；C(i, s) = [i, n_0, 0, n_1, 0, n_2, 0, n_3, 0, 0, …]（n = E_4(s)）；C(s, h) = [n_0, a_0, n_1, a_1, n_2, a_2, n_3, a_3, a_4, …, a_26]（a = H(h)）。關鍵在第三種：第 0 個 octet 是 n_0 = service id 的最低 byte，完全不是隨機值——只要 s ≡ 255 (mod 256)（255、511、…、0x????00FF），該 service 的所有 storage（h = E_4(2^32−1) ⌢ k）、preimage（E_4(2^32−2) ⌢ hash）、request（E_4(l) ⌢ hash）key 都以 0xFF 開頭。舊碼把它們當成 C(255, s) 去解 89-octet 的 account info，值太短就 EOF（issue #779，fuzzer trace 0xffff0017…）。修正後的 IsServiceInfoKey 除了 byte 0 = 0xFF，還要求位置 2、4、6 與 8…30 全為 0；C(s, h) 要滿足這點需要 a_0…a_3 與 a_4…a_26 共 27 個 Blake2b 輸出 byte 全為 0，機率 2^−216，可視為不可能。順帶一提，§D.1 末段允許實作不保存原始 storage key，只保存 hash 後的 31-byte key——這正是你們 unmatched key-vals 機制的依據。",
 "trap": "31-byte key 的第 0 個 byte：C(i) 是 chapter 編號、C(255, s) 是 255、C(s, h) 是 service id 的低 byte——三者可能相同。"
},
{
 "id": "appF-code-shuffle",
 "ch": "F", "section": "F Shuffling (Fisher–Yates)", "gpRef": "eq. F.1 (shuffle), F.2 (Q_l), F.3 (hash form); eq. 11.20–11.22 (guarantor assignment R, P, M); eq. 17.3 and the tranche-0 selection that follows it",
 "difficulty": 2, "kind": "code", "tags": ["shuffle", "guarantor-assignment", "calc"],
  "stemZh": "這是團隊對 eq. F.1 洗牌函數 F 的實作。對於 s = [10, 20, 30, 40] 與 r = [3, 6, 4, 5]，它會回傳什麼？那個就地交換忠於 GP 的定義嗎？",
  "optionsZh": [
   "[40, 10, 30, 20]；忠實——GP 是把 s_{l−1} 寫進被挑中的位置並捨去最後一格，而「先交換再切掉尾端」是同一件事（副作用是呼叫者的 slice 被就地修改）",
   "[40, 10, 20, 30]；不忠實——GP 是把被挑中的元素移除並把其餘左移、保持相對順序，所以與 s[l-1] 的交換會靜默地打亂存活者的順序",
   "[20, 30, 10, 40]；不忠實——GP 的結果是所有交換套用完之後原地留下的那個陣列，而不是被依序挑出的元素序列，所以這個函數回傳的是 eq. F.1 所定義者的反序",
   "[40, 30, 10, 20]；不忠實——GP 是對每個 r_i 取**原始長度** l 的模並索引原序列、完全不縮短它，只在最後才丟棄重複"
  ],
  "stem": "This is the team's implementation of the shuffle F of eq. F.1. For s = [10, 20, 30, 40] and r = [3, 6, 4, 5], what does it return, and is the in-place swap faithful to the GP definition?",
 "code": {"lang": "go", "caption": "internal/utilities/shuffle/shuffle.go (FisherYatesShuffle)", "src": "func FisherYatesShuffle(s []types.U32, r []types.U32) []types.U32 {\n\tl := len(s)\n\n\t// If the sequence is empty, return an empty slice\n\tif l == 0 {\n\t\treturn make([]types.U32, 0)\n\t}\n\n\t// Calculate the index\n\tindex := r[0] % types.U32(l)\n\n\t// The selected element\n\tselected := s[index]\n\n\t// Swap elements\n\ts[index], s[l-1] = s[l-1], s[index]\n\n\t// Recursively shuffle the remaining elements\n\tshuffledRest := FisherYatesShuffle(s[:l-1], r[1:])\n\n\t// Return the shuffled sequence\n\treturn append([]types.U32{selected}, shuffledRest...)\n}"},
 "options": [
  "[40, 10, 30, 20]; faithful — GP writes s_{l−1} into the picked slot and drops the last position, and swapping then slicing off the tail is the same thing (the caller's slice is mutated as a side effect)",
  "[40, 10, 20, 30]; not faithful — GP removes the picked element and shifts the remainder left, preserving relative order, so the swap with s[l-1] silently permutes the survivors",
  "[20, 30, 10, 40]; not faithful — GP's result is the array left in place after all swaps have been applied, not the sequence of picked elements, so this function returns the reverse of what eq. F.1 defines",
  "[40, 30, 10, 20]; not faithful — GP takes every r_i modulo the original length l and indexes the original sequence without shrinking it, discarding duplicates only at the end"
 ],
 "answer": 0,
 "optNotes": [
   "洞由 s_{l−1} 填補再縮短長度，所以「對調後切尾」與 eq. F.1 等價，逐步得 40、10、30、20。",
   "這是「移除後左移、保序」的刪法；GP 明寫 s′_{r_0 mod l} = s_{l−1}，並不保留相對順序。",
   "把經典 in-place Fisher–Yates 跑完的陣列當結果；eq. F.1 輸出的是依序挑出的元素序列。",
   "每次都用原長度取模、不縮短序列；GP 的 l 每輪遞減，遞迴吃的是 s′[..l−1]。",
 ],
 "explanation": "eq. F.1：F(s, r) = [s_{r_0 mod l}] ⌢ F(s′[..l−1], r[1..])，其中 s′ = s 但 s′_{r_0 mod l} = s_{l−1}——輸出是「依序挑出的元素」，被挑走的洞由『最後一個』元素填補，再把長度縮 1。逐步：l = 4，3 mod 4 = 3 → 挑 40，s′ = [10, 20, 30]（洞就在最後，等同截掉）；l = 3，6 mod 3 = 0 → 挑 10，s′_0 = s_2 = 30 → [30, 20]；l = 2，4 mod 2 = 0 → 挑 30，s′_0 = 20 → [20]；最後挑 20。結果 [40, 10, 30, 20]。程式碼把 s[index] 與 s[l−1] 對調再取 s[:l−1]：對調後 index 位置放的正是 s_{l−1}，而移到尾端的元素被切掉，與 GP 完全等價；唯一差別是它就地修改呼叫者的 slice（guarantor_assignments.go 與 auditing.go 每次都建新 slice，所以無害）。eq. F.2/F.3：F(s, h) = F(s, Q_l(h))，Q_l(h)_i = decode_4(H(h ⌢ E_4(⌊i/8⌋))[4i mod 32 ..+4])——每個 Blake2b 供 8 個索引，1023 個 validator 需 128 次 hash。用途：eq. 11.21 的 guarantor 指派 P(v, e, t) = R(F([⌊i/3⌋ | i ∈ N_v], η′_2), ⌊(t mod E)/R⌋)（0.8.0 用 |κ′| 與 ⌊i/3⌋，0.7.2 是 ⌊C·i/V⌋），以及 ch. 17 初始 audit tranche F(reports, Y(seed_0))[..10]（eq. 17.3 之後的 tranche-0 式）。官方 shuffle 向量（jamtestvectors/shuffle，長度 0…341）可驗證 Q_l 與 F 的組合。",
 "trap": "GP 的 F 輸出「挑選順序」，洞由最後一個元素補；用 η′_2（不是 η′_1）避免 epoch 末的 fork 放大。"
},
{
 "id": "appG-ietf-vs-ring",
 "ch": "G", "section": "G Bandersnatch VRF (IETF VRF vs Ring VRF)", "gpRef": "§G; §3 cryptography notation; eq. 6.4, 6.14–6.18, 6.30; eq. 17.3 (audit seed)",
 "difficulty": 2, "kind": "concept", "tags": ["bandersnatch", "vrf", "ring-vrf", "safrole"],
  "stemZh": "JAM 使用兩種 Bandersnatch 構造：單一 context 化的 IETF VRF 簽章、以及 ring-VRF 證明。關於兩者各用在哪、大小如何、以及輸出函數 Y，哪個敘述正確？",
  "optionsZh": [
   "只有 E_T 裡的 ticket 證明是 784 位元組的 ring-VRF 證明（匿名，對照 144 位元組的 ring root 驗證）；seal H_S、熵 H_V 與稽核種子都是具名金鑰下 96 位元組的 IETF VRF 簽章；兩者的 Y(·) 都是 VRF 輸出的前 32 個位元組，而且取決於 context 而非訊息",
   "seal H_S 與 ticket 證明**兩者都是** 784 位元組的 ring-VRF 證明、對照 144 位元組的 γ′_Z 驗證——正是這點讓出塊者在該 epoch 結束前保持匿名；熵 H_V 與稽核種子則是 96 位元組的 IETF VRF 簽章；兩者的 Y(·) 都是完整 64 位元組的 VRF 輸出，取決於 context 而非訊息",
   "只有 ticket 證明是 784 位元組的 ring-VRF 證明；seal、熵與稽核種子是 96 位元組的 IETF VRF 簽章；但兩者的 Y(·) 都是**整個簽章的 Blake2b 雜湊**，因此會隨被簽的訊息改變——這正是 ticket 要簽空訊息的原因",
   "只有 ticket 證明是 784 位元組的 ring-VRF 證明，且是對照一個承諾於 **active set κ′**（而非 pending set）的 32 位元組 ring root 驗證；seal、熵與稽核種子是 96 位元組的 IETF VRF 簽章；Y(·) 是 VRF 輸出的前 32 個位元組，而被 Φ 歸零的金鑰會被移出 ring，因此 ring 會隨 offender 數量而縮小"
  ],
  "stem": "JAM uses two Bandersnatch constructions: singly-contextualized IETF VRF signatures and ring-VRF proofs. Which statement about where each is used, its size and the output function Y is correct?",
 "options": [
  "Only ticket proofs in E_T are 784-octet ring-VRF proofs (anonymous, checked against a 144-octet ring root); the seal H_S, entropy H_V and audit seeds are 96-octet IETF VRF signatures under a named key; in both, Y(·) is the first 32 octets of the VRF output and depends on the context, not the message",
  "Both the seal H_S and the ticket proof are 784-octet ring-VRF proofs checked against the 144-octet γ′_Z — that is what keeps the block author anonymous until the epoch ends; the entropy H_V and the audit seeds are 96-octet IETF VRF signatures under a named key; in both, Y(·) is the full 64-octet VRF output and depends on the context, not the message",
  "Only ticket proofs in E_T are 784-octet ring-VRF proofs (anonymous, checked against a 144-octet ring root); the seal H_S, entropy H_V and audit seeds are 96-octet IETF VRF signatures under a named key; in both, Y(·) is the Blake2b hash of the whole signature, so it moves with the signed message — which is why tickets sign the empty message",
  "Only ticket proofs in E_T are 784-octet ring-VRF proofs, checked against a 32-octet ring root committed over the active set κ′ rather than the pending set; the seal H_S, entropy H_V and audit seeds are 96-octet IETF VRF signatures under a named key; Y(·) is the first 32 octets of the VRF output, and a key zeroed by Φ is dropped from the ring so the ring shrinks with the offender count"
 ],
 "answer": 0,
 "optNotes": [
   "ring VRF 只用在 ticket proof；§G 的 Y(s) ≡ output(s)[..32]，受 context 影響而不受 message 影響。",
   "seal 走 eq. 6.16/6.17 的 IETF 形式、作者由 H_I 公開指名；§G 的 Y 也只取前 32 octets。",
   "Y 取的是 VRF output 本身而非簽名的雜湊，§3 註明它受 context 影響、不受 message 影響。",
   "ring root ∈ B̊ ⊂ B_144 且承諾在 γ′_P 上；被 Φ 歸零的 key 以 padding point 代入，ring 大小不變。",
 ],
 "explanation": "§G：V_k⟨c⟩(m) ⊂ B_96 是 IETF VRF（RFC 9381 樣板）——簽名者由公開金鑰 k 指名；V̄_r⟨c⟩(m) ⊂ B_784 是 ring VRF（Pedersen VRF + zk-SNARK），只證明「ring 裡某個成員」簽了，匿名；O(⟦k⟧) ∈ B_144 是 ring root（commit）。用途：eq. 6.30 的 ticket proof p ∈ V̄_{γ′_Z}⟨X_T ⌢ η′_2 ⌢ [e]⟩([])——唯一的 ring VRF；eq. 6.16/6.17 的 seal H_S ∈ V_{H_A}⟨X_T ⌢ η′_3 ⌢ [i_e]⟩(E_U(H)) 或 ⟨X_F ⌢ η′_3⟩，eq. 6.18 的 H_V ∈ V_{H_A}⟨X_E ⌢ Y(H_S)⟩([])，以及 eq. 17.3 的 audit seed ∈ V_{κ[v]_b}⟨X_U ⌢ Y(H_V)⟩([])——都是 IETF、由 H_A = κ′[H_I]_b 指名。Y(x) = output(x)[..32]：VRF 輸出的前 32 octets，§3 特別註明它「influenced by x（context）but not by m（message）」——所以 ticket id = Y(p) 只由 η′_2 與 entry index 決定，seal 的 Y(H_S) 也不受 header 內容影響（這正是 H_V 能用它當 context 的原因）。匿名的是『票』在被使用前不可連結到驗證者，而不是出塊者：seal 的作者由 H_I 公開指名。ring root 是 eq. 6.14 的 z = O([k_b | k ∈ γ′_P])——用『下一個 epoch 的 pending set』而非 κ′，而 offenders 的 key 被 Φ 換成全 0（eq. 6.15），§G 規定「無對應 Bandersnatch point 的 key 以 padding point 代替」，ring 大小不變。你們 #1040 的修正正是基於「ring commitment 是 Bandersnatch keys 的純函數」。",
 "trap": "ring VRF 只用在 ticket；seal/entropy/audit 都是 IETF；γ_Z 來自 γ′_P（pending），壞 key 用 padding point。"
},
{
 "id": "appG-signing-contexts",
 "ch": "G", "section": "Signing contexts X (definitions appendix) and their primitives", "gpRef": "definitions appendix §Signing Contexts; eq. 6.16–6.18, 6.30, 11.14, 11.28, 17.3, 17.7, 17.16, 18.1; ch. 10 culprit/fault signature rules",
 "difficulty": 2, "kind": "concept", "tags": ["signing-contexts", "bandersnatch", "ed25519", "bls"],
  "stemZh": "JAM 的每個簽章都由一個 context 字串 X 做 domain separation。下列（context → 原語 → 用途）的敘述哪一個正確？",
  "optionsZh": [
   "X_T = $jam_ticket_seal 被用了兩次：一次用於 ring-VRF 的 ticket 證明（context 為 X_T ⌢ η′_2 ⌢ [e]、空訊息、root 為 γ′_Z），一次用於一般的 IETF-VRF seal（context 為 X_T ⌢ η′_3 ⌢ [i_e]、訊息為 E_U(H)）",
   "X_E = $jam_entropy 是出塊者對未簽署 header E_U(H) 所做的 **Ed25519** 簽章；而餵給熵累積器 η′_0 的，是該簽章的 Blake2b 雜湊",
   "X_G = $jam_guarantee 是對 H(w) 的 Bandersnatch VRF context，而它的輸出 Y(·) 同時充當與 ρ 中 availability assignment 一起儲存的 guarantee 識別碼",
   "X_U = $jam_audit 是 validator 用來簽署那些出現在 disputes extrinsic E_D 之 verdict 中的 judgment 的 Ed25519 context，每份 report 雜湊一個簽章"
  ],
  "stem": "Each JAM signature is domain-separated by a context string X. Which of the following (context → primitive → use) statements is correct?",
 "options": [
  "X_T = $jam_ticket_seal is used twice: for the ring-VRF ticket proof (context X_T ⌢ η′_2 ⌢ [e], empty message, root γ′_Z) and for the regular IETF-VRF seal (context X_T ⌢ η′_3 ⌢ [i_e], message E_U(H))",
  "X_E = $jam_entropy is an Ed25519 signature by the author over the unsigned header E_U(H); the Blake2b hash of that signature is what feeds the entropy accumulator η′_0 each block",
  "X_G = $jam_guarantee is a Bandersnatch VRF context over H(w), and its output Y(·) doubles as the guarantee identifier stored with the availability assignment in ρ",
  "X_U = $jam_audit is the Ed25519 context under which validators sign the judgments that appear in the verdicts of the disputes extrinsic E_D, one signature per report hash"
 ],
 "answer": 0,
 "optNotes": [
   "同一個字串兩種用法，差別在 η′_2 vs η′_3、ring vs IETF、空訊息 vs E_U(H)。",
   "X_E 是 Bandersnatch IETF VRF：context X_E ⌢ Y(H_S)、訊息為空，既不是 Ed25519 也不簽 header。",
   "X_G 是 Ed25519 而不是 VRF，guarantee 也沒有任何 identifier 會被存進 ρ。",
   "X_U 是 Bandersnatch 的 audit seed context；judgment 與 fault 用的是 X_valid / X_invalid。",
 ],
 "explanation": "definitions 附錄「Signing Contexts」：X_A = $jam_available（Ed25519，assurances；eq. 11.14 簽 X_A ⌢ H(E(H_P, bitfield))）；X_B = $jam_beefy（BLS，eq. 18.1 簽 X_B ⌢ 最新 β_H 的 super-peak）；X_E = $jam_entropy（Bandersnatch IETF，eq. 6.18：context X_E ⌢ Y(H_S)、訊息為空）；X_F = $jam_fallback_seal（Bandersnatch，eq. 6.17）；X_G = $jam_guarantee（Ed25519，eq. 11.28 guarantee 簽 X_G ⌢ H(w)，ch. 10 的 culprit 也用它簽 X_G ⌢ report hash）；X_I = $jam_announce（Ed25519，eq. 17.7 的 audit announcement）；X_T = $jam_ticket_seal（Bandersnatch ring VRF 出票 + IETF 正常 seal）；X_U = $jam_audit（Bandersnatch，audit 選取熵，eq. 17.3 的 seed_0 與 eq. 17.12 的 seed_n）；X_valid/X_invalid = $jam_valid/$jam_invalid（Ed25519，judgments 與 faults，eq. 17.16、ch. 10）。判讀時要連 context 的組成（X ⌢ entropy ⌢ index）與原語一起看，同一個字串完全可以搭配不同的原語與不同的 entropy 版本。你們 const.go 的 JamEntropy/JamFallbackSeal/JamTicketSeal/JamValid/JamInvalid/JamAvailable/JamBeefy/JamGuarantee/JamAnnounce/JamAudit 逐一對應；#940 的 bug（用公鑰簽 judgment）就是 X_valid 這條路徑。",
 "trap": "口訣：Bandersnatch = T/F/E/U（票、備援 seal、熵、audit）；Ed25519 = A/G/I/valid/invalid；BLS = B。"
}
]
