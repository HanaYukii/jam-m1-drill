# -*- coding: utf-8 -*-
# Batch 2 — Appendices C (Serialization Codec), D (State Merklization), E (General Merklization & MMR),
# F (Shuffling), G (Bandersnatch VRF / signing contexts), H (Erasure Coding) — GP 0.8.0
ITEMS = [
{
 "id": "appD-code-service-info-key",
 "lens": "演算法",
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
 "id": "appG-ietf-vs-ring",
 "lens": "對比",
 "ch": "G", "section": "G Bandersnatch VRF (IETF VRF vs Ring VRF)", "gpRef": "§G; §3 cryptography notation; eq. 6.4, 6.14–6.18, 6.30; eq. 17.3 (audit seed)",
 "difficulty": 2, "kind": "concept", "tags": ["bandersnatch", "vrf", "ring-vrf", "safrole"],
  "stemZh": "JAM 使用兩種 Bandersnatch 構造：單一 context 化的 IETF VRF 簽章、以及 ring-VRF 證明。兩者各用在哪？各多大？輸出函數 Y 又取決於什麼？",
  "optionsZh": [
   "只有 E_T 裡的 ticket 證明是 784 位元組的 ring-VRF 證明（匿名，對照 144 位元組的 ring root 驗證）；seal H_S、熵 H_V 與稽核種子都是具名金鑰下 96 位元組的 IETF VRF 簽章；兩者的 Y(·) 都是 VRF 輸出的前 32 個位元組，而且取決於 context 而非訊息",
   "seal H_S 與 ticket 證明兩者都是 784 位元組的 ring-VRF 證明、對照 144 位元組的 γ′_Z 驗證——正是這點讓出塊者在該 epoch 結束前保持匿名；熵 H_V 與稽核種子則是 96 位元組的 IETF VRF 簽章；兩者的 Y(·) 都是完整 64 位元組的 VRF 輸出，取決於 context 而非訊息",
   "只有 ticket 證明是 784 位元組的 ring-VRF 證明；seal、熵與稽核種子是 96 位元組的 IETF VRF 簽章；但兩者的 Y(·) 都是整個簽章的 Blake2b 雜湊，因此會隨被簽的訊息改變——這正是 ticket 要簽空訊息的原因",
   "只有 ticket 證明是 784 位元組的 ring-VRF 證明，且是對照一個承諾於 active set κ′（而非 pending set）的 32 位元組 ring root 驗證；seal、熵與稽核種子是 96 位元組的 IETF VRF 簽章；Y(·) 是 VRF 輸出的前 32 個位元組，而被 Φ 歸零的金鑰會被移出 ring，因此 ring 會隨 offender 數量而縮小"
  ],
  "stem": "JAM uses two Bandersnatch constructions: singly-contextualized IETF VRF signatures and ring-VRF proofs. Where is each used, how big is each, and what does the output function Y depend on?",
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
 "lens": "機制",
 "ch": "G", "section": "Signing contexts X (definitions appendix) and their primitives", "gpRef": "definitions appendix §Signing Contexts; eq. 6.16–6.18, 6.30, 11.14, 11.28, 17.3, 17.7, 17.16, 18.1; ch. 10 culprit/fault signature rules",
 "difficulty": 2, "kind": "concept", "tags": ["signing-contexts", "bandersnatch", "ed25519", "bls"],
  "stemZh": "JAM 的每個簽章都由一個 context 字串 X 做 domain separation。列出這些 context 與各自搭配的原語——並指出唯一一個被用了兩次、搭配兩種不同原語的 context。",
  "optionsZh": [
   "X_T = $jam_ticket_seal 被用了兩次：一次用於 ring-VRF 的 ticket 證明（context 為 X_T ⌢ η′_2 ⌢ [e]、空訊息、root 為 γ′_Z），一次用於一般的 IETF-VRF seal（context 為 X_T ⌢ η′_3 ⌢ [i_e]、訊息為 E_U(H)）",
   "X_E = $jam_entropy 是出塊者對未簽署 header E_U(H) 所做的 Ed25519 簽章；而餵給熵累積器 η′_0 的，是該簽章的 Blake2b 雜湊",
   "X_G = $jam_guarantee 是對 H(w) 的 Bandersnatch VRF context，而它的輸出 Y(·) 同時充當與 ρ 中 availability assignment 一起儲存的 guarantee 識別碼",
   "X_U = $jam_audit 是 validator 用來簽署那些出現在 disputes extrinsic E_D 之 verdict 中的 judgment 的 Ed25519 context，每份 report 雜湊一個簽章"
  ],
  "stem": "Each JAM signature is domain-separated by a context string X. Name the contexts and the primitive each goes with — and point out the one context that is used twice, with two different primitives.",
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
