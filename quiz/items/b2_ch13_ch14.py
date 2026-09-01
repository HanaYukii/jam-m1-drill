# -*- coding: utf-8 -*-
# Batch 2 — Chapter 13 (Statistics) and Chapter 14 (Work Packages and Work Reports), GP 0.8.0
# Sources: gp-src/text/statistics.tex, work_packages_and_reports.tex, pvm_invocations.tex (B.1, B.5);
#          team code internal/statistics/statistics.go, internal/work_package/work_package.go, PVM/refine_invocation.go;
#          issues digest #710, #869, #1015, #1021, #1026, #1034.
ITEMS = [
{
 "id": "ch13-counter-deltas-calc",
 "ch": "13", "section": "13.1 Validator Activity", "gpRef": "eq. 13.4–13.6 (π_V†, π_V‡, π′_V); eq. 11.28 (reporters set G)",
 "difficulty": 2, "kind": "concept", "tags": ["statistics", "validator-stats", "calc"],
  "stemZh": "某個 epoch 中段（e′ = e）的區塊，其出塊者索引 H_I = 3。它的 extrinsic 含有：E_T 兩張 ticket、E_P 一份 500 個 octet 的 preimage、E_A 由 validator 1 與 2 簽署的 assurance、E_G 一份 guarantee 且其憑證帶有 validator 0 與 4 的簽章。相對於 π_V，π′_V 會顯示哪些逐 validator 的變動（計數器 b、t、p、d、g、a）？",
  "optionsZh": [
   "validator 3：b+1、t+2、p+1、d+500、g+1、a+2——出塊者納入的每一項 extrinsic 都記在出塊者頭上；其他 validator 都不變",
   "validator 3：b+1、t+2、p+1、**d+1**；validator 1 與 2：各 a+1；validator 0 與 4：各 g+1",
   "validator 3：b+1、t+2、p+1、d+500；validator 1 與 2：各 a+1；validator 0 與 4：各 g+1；其餘紀錄不變",
   "validator 3：b+1、p+1、d+500；產生那兩張 ticket 的兩位 validator：各 t+1；validator 1 與 2：各 a+1；validator 0 與 4：各 g+1"
  ],
  "stem": "A block in the middle of an epoch (e′ = e) has author index H_I = 3. Its extrinsic contains E_T with 2 tickets, E_P with one preimage of 500 octets, E_A with assurances signed by validators 1 and 2, and E_G with one guarantee whose credential carries the signatures of validators 0 and 4. Which per-validator changes does π′_V show relative to π_V (counters b, t, p, d, g, a)?",
 "options": [
  "Validator 3: b+1, t+2, p+1, d+500, g+1, a+2 — every extrinsic the author includes is credited to the author; no other validator changes",
  "Validator 3: b+1, t+2, p+1, d+1; validators 1 and 2: a+1 each; validators 0 and 4: g+1 each",
  "Validator 3: b+1, t+2, p+1, d+500; validators 1 and 2: a+1 each; validators 0 and 4: g+1 each; all other records unchanged",
  "Validator 3: b+1, p+1, d+500; the two validators who generated the tickets: t+1 each; validators 1 and 2: a+1 each; validators 0 and 4: g+1 each"
 ],
 "answer": 2,
 "optNotes": [
  "g 與 a 依簽章歸屬，author 只是把 extrinsic 打包進區塊，不會因此連 g、a 一起拿到。",
  "d 是 preimage 的 octet 總數（500），p 才是筆數，兩者記在不同 counter 不可混。",
  "b/t/p/d 記給 H_I、a 記給 assurance 簽署者、g 記給 eq. 11.28 的 reporters，三種歸屬都對。",
  "ticket 是匿名的 ring-VRF 證明，鏈上不知道誰產生，eq. 13.6 因此把 |E_T| 記給 H_I。",
 ],
 "explanation": "eq. 13.4：π_V†[v]_a = π_V[v]_a + (∃a ∈ E_A : a_v = v)——assurance 記在**簽署者**身上（存在性判斷，每人每塊最多 +1）。eq. 13.5：e′ = e（不在 epoch 邊界）所以 π_V‡ = π_V†、π_L 不變。eq. 13.6：b += (v = H_I)、t += |E_T|、p += |E_P|、d += Σ_{d∈E_P}|d| 都**只給 author**；g += (κ′[v] ∈ G)，G 是 eq. 11.28 的 reporters set——credential 裡有簽名的 validator 的 Ed25519 key。結果：v0: g+1；v1、v2: a+1；v3: b+1, t+2, p+1, d+500；v4: g+1。你們 statistics.go：UpdateTicketStatistics / UpdatePreimageStatistics / UpdatePreimageOctetStatistics 只更新 authorIndex；UpdateReportStatistics 用 reporters set；UpdateAvailabilityStatistics 用 assurance.ValidatorIndex。issue #710（0.7.0）修的就是「每個 validator 只算一次」，#869 修 guarantee 計數。",
 "trap": "b/t/p/d 看 H_I；g/a 看簽章；每塊每人 g、a 最多各 +1（布林值，不是數量）。"
},
{
 "id": "ch13-why-statistics",
 "ch": "13", "section": "13.1 Validator Activity", "gpRef": "§13.1 (intro paragraphs); §14.1 honest behavior; C(13) in App. D",
 "difficulty": 1, "kind": "rationale", "tags": ["statistics", "rationale", "staking"],
  "stemZh": "JAM 這條鏈為什麼要保留 validator 的活動統計？GP 對那些無法在鏈上直接量測的活動又怎麼說？",
  "optionsZh": [
   "JAM 直接支付 validator：每個區塊 STF 都會按 π_V 的比例從某個 treasury service 扣款，就像它處理懲罰那樣；出塊、擔保與背書可在鏈上追蹤，而 GRANDPA、BEEFY 與稽核也可以，因為 validator 簽署的每一則訊息最終都會被納入某個區塊",
   "JAM 自己不發放獎勵，而是把活動資料當成 oracle 提供給質押子系統，就像它處理懲罰資料那樣；出塊、擔保與背書可在鏈上追蹤，而 GRANDPA、BEEFY 與稽核則不行，改由 validator 互相對彼此的努力投票、在 50% 誠實的假設下取中位數",
   "JAM 自己不發放獎勵，而是把 π 餵給 Safrole，由它把計數器低於門檻的 validator 從 ι′ 中剔除；出塊、擔保與背書可在鏈上追蹤，而 GRANDPA 與 BEEFY 的活動直接從 header 的 finality 欄位讀取，稽核則由 validator 互相投票涵蓋",
   "JAM 自己不發放獎勵，而這些統計只是為了遙測（JIP-3）與 RPC 而存在：π 位於共識狀態之外、不被 state root 涵蓋，懲罰紀錄 ψ 也是如此；因此 GRANDPA、BEEFY 與稽核的活動只是被省略，並未被 oracle 給任何外部子系統"
  ],
  "stem": "Why does the JAM chain keep validator activity statistics at all, and what does the GP say about the activities that cannot be measured directly on-chain?",
 "options": [
  "JAM pays validators directly: each block the STF debits a treasury service in proportion to π_V, exactly as it does for punishment; block production, guaranteeing and assurances are trackable on-chain, and so are GRANDPA, BEEFY and auditing, since every message a validator signs is eventually included in some block",
  "JAM issues no rewards itself but oracles activity data to a staking subsystem, as it does with punishment data; block production, guaranteeing and assurances are trackable on-chain, whereas GRANDPA, BEEFY and auditing are not and are instead covered by validators voting on each other's efforts, with a median accepted under a 50%-honest assumption",
  "JAM issues no rewards itself but feeds π into Safrole, which drops from ι′ any validator whose counters fall below a threshold; block production, guaranteeing and assurances are trackable on-chain, whereas GRANDPA and BEEFY activity is read straight from the header's finality field and auditing is covered by validators voting on each other's efforts",
  "JAM issues no rewards itself and the statistics exist only for telemetry (JIP-3) and RPC: π sits outside the consensus state and is not covered by the state root, as is the punishment record ψ; GRANDPA, BEEFY and auditing activity is therefore simply omitted rather than oracled to any external subsystem"
 ],
 "answer": 1,
 "optNotes": [
  "與 §13.1 第一句 does not explicitly issue rewards 正面牴觸；GRANDPA/BEEFY 簽章根本不進區塊。",
  "§13.1 原文：JAM 只 facilitate the arrival of information，untrackable 的部分靠互評取 median。",
  "ι′ 來自 delegator service 的 accumulate 輸出（§12），與 π 無關；§5 的 header 也沒有 finality 欄位。",
  "π 是 App. D 的 C(13)、ψ 是 C(5)，兩者都在 state root 底下；untrackable 的活動也沒有被略過。",
 ],
 "explanation": "§13.1 開頭：「The JAM chain does not explicitly issue rewards—we leave this as a job to be done by the staking subsystem (in Polkadot's case envisioned as a system parachain—hosted without fees…)」，JAM 只負責「facilitate the arrival of information on validator activity in to the staking subsystem」，如同 punishment（ψ_o offenders）資訊一樣是給外部子系統的 oracle。可直接鏈上追蹤的是 block production、guarantor reports、availability assurance（對應 π_V 的 b/t/p/d、g、a）；GRANDPA、BEEFY 與 auditing 則「cannot」，改由 validator 互評——「validators vote on their impression of each other's efforts and a median may be accepted as the truth」，並且「With an assumption of 50% honest validators, this gives an adequate means of oraclizing this information」。§14.1 的 honest behavior 清單最後一項正是「submitting the correct amount of auditing work seen being done by other validators」。編碼上 π 落在 App. D 的 C(13)，0.8.0 起 π_V/π_L 還帶長度前綴（你們 PR #1034）。",
 "trap": "JAM 不發獎勵、不追蹤 GRANDPA/BEEFY/audit；這些靠 validator voting 的 median，假設只需 50% 誠實。"
},
{
 "id": "ch14-code-digest-mapping",
 "ch": "14", "section": "14.3 Packages and Items", "gpRef": "eq. 14.10 (item-to-digest C); eq. 11.6 (D); eq. 13.10/13.17 — internal/work_package/work_package.go C",
 "difficulty": 2, "kind": "code", "tags": ["work-packages", "digest", "code"],
  "stemZh": "這是團隊的 item-to-digest 函數（GP 0.8.0 eq. 14.10，C）。關於它的哪個敘述正確？",
  "optionsZh": [
   "唯一的缺陷是 payload 雜湊：eq. 14.10 要求 y = H(E(w))，也就是**整個編碼後 work-item** 的雜湊而不是只對 payload 取雜湊，所以 PayloadHash 必須改為對 E(item) 取；至於 accumulate gas 上限、import 計數以及三個負載計數器 x = |w_x|、z = extrinsic 長度總和、e = w_e 都指派正確",
   "AccumulateGas 是唯一的缺陷：一個 digest 的 g 必須是 **refine** gas 上限 w_g，因為 accumulation 的 gas 是由鏈上的 Δ+ 決定而不是由該 package 決定；payload 雜湊 H(w_y)、import 計數 |w_i| 以及三個負載計數器都指派正確",
   "這段程式碼是對的：eq. 14.10 只釘死了 payload 雜湊、accumulate gas 上限、import 計數與已用 gas，把三個 manifest 計數器 x、z、e 留給 Ψ_R 實際做了什麼，所以只要 guarantor 對最終的 report 雜湊有共識，任何自洽的指派都可以接受",
   "三個負載計數器被輪換錯位了：eq. 14.10 設定 x = |w_x|（extrinsic 數）、z = extrinsic 長度總和、e = w_e（宣告的匯出數），但程式碼把 w_e 放進 ExtrinsicCount、把 |w_x| 放進 ExtrinsicSize、把長度總和放進 Exports——payload 雜湊、accumulate gas 上限、import 計數與已用 gas 都是對的"
  ],
  "stem": "This is the team's item-to-digest function (GP 0.8.0 eq. 14.10, C). Which statement about it is correct?",
 "code": {"lang": "go", "caption": "internal/work_package/work_package.go (C; the '14.8' in the comment is the 0.7.2 number of eq. 14.10)", "src": """// C (14.8)
func C(item types.WorkItem, result types.WorkExecResult, gas types.Gas) types.WorkResult {
    payloadHash := hash.Blake2bHash(item.Payload)
    importCount := types.U16(len(item.ImportSegments))
    extrinsicSize := types.U32(len(item.Extrinsic))
    var zSum types.U16
    for _, v := range item.Extrinsic {
        zSum += types.U16(v.Len)
    }
    return types.WorkResult{
        ServiceID:     item.Service,
        CodeHash:      item.CodeHash,
        PayloadHash:   payloadHash,
        AccumulateGas: item.AccumulateGasLimit,
        Result:        result,
        RefineLoad: types.RefineLoad{
            GasUsed:        gas,
            Imports:        importCount,
            ExtrinsicCount: item.ExportCount,
            ExtrinsicSize:  extrinsicSize,
            Exports:        zSum,
        },
    }
}"""},
 "options": [
  "The only defect is the payload hash: eq. 14.10 requires y = H(E(w)), the hash of the whole encoded work-item rather than of the payload alone, so PayloadHash must be taken over E(item); the accumulate gas limit, the import count and the three load counters x = |w_x|, z = Σ of the extrinsic lengths and e = w_e are all assigned correctly",
  "AccumulateGas is the only defect: a digest's g must be the refine gas limit w_g, because the accumulation gas is decided on-chain by Δ+ rather than by the package; the payload hash H(w_y), the import count |w_i| and the three load counters x = |w_x|, z = Σ of the extrinsic lengths and e = w_e are all assigned correctly",
  "The code is correct: eq. 14.10 pins down only the payload hash, the accumulate gas limit, the import count and the gas used, leaving the three manifest counters x, z and e to whatever Ψ_R actually did, so any self-consistent assignment is acceptable provided the guarantors agree on the resulting report hash",
  "Three load counters are rotated: eq. 14.10 sets x = |w_x| (number of extrinsics), z = Σ of the extrinsic lengths and e = w_e (declared export count), but the code puts w_e into ExtrinsicCount, |w_x| into ExtrinsicSize and the length sum into Exports — payload hash, accumulate gas limit, import count and gas used are right"
 ],
 "answer": 3,
 "optNotes": [
  "eq. 11.6 說 y 是原樣交給 accumulation 的 payload，digest 取的就是 H(w_y)，不是整個 work-item。",
  "digest 的 g 是 accumulate gas limit w_a；refine 的 w_g 只出現在 eq. 14.9 與 Ψ_R。",
  "eq. 14.10 對 x、z、e 是精確定義，沒有「任意自洽即可」的空間，而 code 的這三欄確實錯位。",
  "ExtrinsicCount 收了 w_e、ExtrinsicSize 收了 |w_x|、Exports 收了 Σz，正是三欄整組輪轉。",
 ],
 "explanation": "eq. 14.10 C：((s, c, y, a, e, i, x), l, u) ↦ (s, c, y ↦ H(y), g ↦ w_a, l, u, i ↦ |w_i|, e, x ↦ |w_x|, z ↦ Σ_{(h,z)∈w_x} z)。對照 code：Imports = len(ImportSegments)、AccumulateGas = w_a、PayloadHash = H(payload)、GasUsed = u 都正確；但 ExtrinsicCount 被塞了 item.ExportCount（應為 len(item.Extrinsic)）、ExtrinsicSize 被塞了 len(item.Extrinsic)（應為 Σ Len，也就是 zSum）、Exports 被塞了 zSum（應為 ExportCount）——三個欄位輪轉錯位。三個干擾項共用同一個破綻：它們都順帶宣稱 x、z、e 指派正確。後果：digest 的 x/z/e 錯 → report hash 與其他實作不同（guarantor 簽章不一致）→ π_C 與 π_S（eq. 13.10、13.17 的 R(c)、R(s)）也錯。STF conformance fuzzer 沒抓到，因為 test vectors 直接提供現成的 work-report（code-map §5 第 16 點：這條路徑不在 STF 向量裡）。另外 e 是 work-item **宣告**的 w_e，實際 export 數不符時 I 函數（eq. 14.13）會給 ⊚ BADEXPORTS。",
 "trap": "digest 五個負載欄位：u gas used、i imports、e exports、x extrinsic count、z extrinsic size——順序與名稱要背熟。"
},
{
 "id": "ch14-code-refine-args",
 "ch": "14", "section": "14.4 Computation of Work-Report", "gpRef": "eq. B.5 (Ψ_R argument a and gas w_g); eq. B.1 (Ψ_I uses E_2(c)); eq. 14.9 (G_R) — PVM/refine_invocation.go RefineInvoke",
 "difficulty": 3, "kind": "code", "tags": ["work-packages", "refine", "pvm-invocation", "code"],
  "stemZh": "以下是團隊的 Ψ_R 建構交給 Ψ_M 之引數 blob a 的方式。依 GP 0.8.0（eq. B.5），哪個敘述正確？",
  "optionsZh": [
   "core 索引必須編碼為 E_2(c)，也就是固定的兩個 octet，與 Ψ_I 的做法完全相同，所以那個緊湊的 EncodeUint 是錯的；至於 service 索引 w_s、緊湊的 i、帶長度前綴的 payload、對編碼後 package 取的 H(p) 以及 gas 上限 w_g 都與 GP 相符",
   "a 的第三個成分必須是以緊湊自然數表示的 service 索引 w_s，但程式碼附加的是 32 位元組的 code hash w_c；緊湊的 c 與 i、帶長度前綴的 payload、H(p) 以及 gas 上限 w_g 都與 GP 相符",
   "最後那個雜湊必須是 H(E(w))，也就是正在被 refine 的那個編碼後 work-item 的雜湊，而不是 H(p)；而且交給 Ψ_M 的 gas 上限必須是 G_R = 5·10⁹（每個 package 的 refine 額度）而不是單一項目的 w_g——緊湊的 c 與 i、service 索引 w_s 與帶長度前綴的 payload 都是對的",
   "payload 必須不帶長度前綴地附加上去，因為 Refine 是改用 fetch host call 取得它的，所以那個 ↕ 是多餘的；緊湊的 c 與 i、service 索引 w_s、H(p) 以及 gas 上限 w_g 都與 eq. B.5 相符"
  ],
  "stem": "Below is how the team's Ψ_R builds the argument blob a handed to Ψ_M. Which statement is correct under GP 0.8.0 (eq. B.5)?",
 "code": {"lang": "go", "caption": "PVM/refine_invocation.go (RefineInvoke, 0.7.2)", "src": """    // otherwise
    var a []byte
    encoder := types.NewEncoder()
    // c
    encoded, _ := encoder.EncodeUint(uint64(input.CoreIndex))
    a = append(a, encoded...)
    // i
    encoded, _ = encoder.EncodeUint(uint64(input.WorkItemIndex))
    a = append(a, encoded...)
    // w_s
    encoded, _ = encoder.Encode(&workItem.CodeHash)
    a = append(a, encoded...)
    // |w_y| . w_y
    encoded, _ = encoder.Encode(&workItem.Payload)
    a = append(a, encoded...)
    // H(p)
    encoded, _ = encoder.Encode(&input.WorkPackage)
    h := hash.Blake2bHash(encoded)
    a = append(a, h[:]...)
    // ... (host-call context `addition` elided)
    result := Psi_M(StandardCodeFormat(code), 0, workItem.RefineGasLimit, a, RefineOmegas, addition)"""},
 "options": [
  "The core index must be encoded as E_2(c), two fixed octets, exactly as Ψ_I does, so the compact EncodeUint is wrong; the service index w_s, the compact i, the length-prefixed payload, H(p) over the encoded package and the gas limit w_g all match the GP",
  "The third component of a must be the service index w_s as a compact natural, but the code appends the 32-octet code hash w_c; the compact c and i, the length-prefixed payload, H(p) over the encoded package and the gas limit w_g all match the GP",
  "The final hash must be H(E(w)), the hash of the encoded work-item being refined, rather than H(p); and the gas limit handed to Ψ_M must be G_R = 5·10⁹, the per-package refine allowance, not one item's w_g — the compact c and i, the service index w_s and the length-prefixed payload are all correct",
  "The payload must be appended without a length prefix because Refine obtains it through the fetch host-call instead, so the ↕ is spurious; the compact c and i, the service index w_s, H(p) over the encoded package and the gas limit w_g all match eq. B.5"
 ],
 "answer": 1,
 "optNotes": [
  "E_2(c) 是 Ψ_I 的參數（eq. B.1：Ψ_M(p_u, 0, G_I, E_2(c), …)），Ψ_R 的 c 用的是 compact E。",
  "註解寫 w_s 的那行編進去的是 workItem.CodeHash，32-byte 的 w_c 頂替了 compact 的 service index。",
  "H(p) 就是整包 package 的 hash；G_R 是 eq. 14.9 的 package 級 Σ w_g 上限，單一 item 傳的是 w_g。",
  "eq. B.5 的 ↕w_y 明確帶長度前綴，fetch selector 13 只是另一個取得管道，不能取消 ↕。",
 ],
 "explanation": "eq. B.5 Ψ_R(c, i, p, r, ī, ς)：a = E(c, i, w_s, ↕w_y, H(p))，code 由 E(↕z, code) = Λ(δ[w_s], (p_c)_t, w_c) 去掉 metadata 前綴取得，然後 (u, o, (m, e)) = Ψ_M(code, 0, w_g, a, F, (∅, []))。c、i、w_s 都是無下標的 E → 一般（compact）自然數編碼；w_y 帶長度前綴（↕）；H(p) 是整個 package 序列化後的 hash。你們的 code：c、i 用 EncodeUint（C.6 compact）正確；Payload 用 ByteSequence.Encode（帶長度）正確；H(p) = Blake2b(E(p)) 正確；gas 傳 workItem.RefineGasLimit（w_g）正確——唯一的錯處是 a 的第三段，任何依 GP 解析 refine args 的 service 會把 code hash 的前幾個 byte 當 service id、後面全部錯位；三個干擾項也都順帶宣稱那一段是對的。0.7.2 與 0.8.0 的公式相同（0.7.1 才加入 c）。",
 "trap": "Ψ_I：E_2(c) + G_I = 50M；Ψ_R：E(c, i, w_s, ↕w_y, H(p)) + w_g（Σ w_g < G_R = 5·10⁹）。"
},
{
 "id": "ch14-compute-report-signature",
 "ch": "14", "section": "14.4 Computation of Work-Report", "gpRef": "eq. 14.13–14.14 (Ξ, E, srlookup correspondence); eq. 14.17 (A with v); eq. 11.31",
 "difficulty": 3, "kind": "delta", "tags": ["work-packages", "compute-report", "delta-0.8.0"],
  "stemZh": "GP 0.8.0 重新定義了 work-report 的計算函數 Ξ。關於它的引數與失敗條件 E，哪個敘述正確？",
  "optionsZh": [
   "Ξ(p, c, l, v) 收下 package、core、一個 segment-root 字典 l（每個被 h⊞ import 引用到的 work-package 雜湊各一項）以及 assurer 集合大小 v；只有在 Is-Authorized 的結果不是至多 W_R 個 octet 的 blob、或 keys(l) 與那組 h⊞ 雜湊不符時才產生 ∇——某個 work-item 的 Refine 以 ∞、☇、BAD 或 BIG 結束並不會讓 Ξ 失敗",
   "Ξ(p, c) 一如 0.7.2 只收下 package 與 core；segment-root 字典是在計算期間從鏈上狀態 ρ 讀出的，而碎片數固定為 V = 1,023；只有在 Is-Authorized 的結果不是至多 W_R 個 octet 的 blob 時才產生 ∇——某個 work-item 的 Refine 失敗並不會讓 Ξ 失敗",
   "Ξ(p, c, l, v) 收下 package、core、segment-root 字典 l 與 assurer 集合大小 v；在 Is-Authorized 的結果不合格、keys(l) 不符、**或任何 work-item 的 Refine 以 ∞、☇、BAD 或 BIG 結束**時都產生 ∇，如此 guarantor 就永遠不會為一份含有失敗項目的 report 簽名",
   "Ξ(p, c, l, v) 收下 package、core、一個以 **work-item 索引**為 key、每個 import 一項的 segment-root 字典 l，以及 v，也就是該 report 上的 guarantor 簽章數（2 或 3）；只有在 Is-Authorized 的結果不合格、或編碼後的 report 超過 W_B = 13,791,360 個 octet 時才產生 ∇"
  ],
  "stem": "GP 0.8.0 redefines the work-report computation function Ξ. Which statement about its arguments and its failure condition E is correct?",
 "options": [
  "Ξ(p, c, l, v) takes the package, the core, a segment-root dictionary l (one entry per work-package hash referenced by an h⊞ import) and the assurer-set size v; it yields ∇ only if the Is-Authorized result is not a blob of at most W_R octets or if keys(l) differ from the set of h⊞ hashes — a work-item whose Refine ends in ∞, ☇, BAD or BIG does not make Ξ fail",
  "Ξ(p, c) as in 0.7.2 takes only the package and the core; the segment-root dictionary is read out of the on-chain state ρ during computation and the shard count is fixed at V = 1,023; it yields ∇ only if the Is-Authorized result is not a blob of at most W_R octets — a work-item whose Refine ends in ∞, ☇, BAD or BIG does not make Ξ fail",
  "Ξ(p, c, l, v) takes the package, the core, a segment-root dictionary l (one entry per work-package hash referenced by an h⊞ import) and the assurer-set size v; it yields ∇ if the Is-Authorized result is not a blob of at most W_R octets, if keys(l) differ from the set of h⊞ hashes, or if any work-item's Refine ends in ∞, ☇, BAD or BIG, so that a guarantor never signs a report holding a failed item",
  "Ξ(p, c, l, v) takes the package, the core, a segment-root dictionary l keyed by work-ITEM index with one entry per import, and v, the number of guarantor signatures on the report (2 or 3); it yields ∇ only if the Is-Authorized result is not a blob of at most W_R octets or if the encoded report exceeds W_B = 13,791,360 octets"
 ],
 "answer": 0,
 "optNotes": [
  "eq. 14.13 的 E 只有兩個 disjunct：Ψ_I 的結果不是 ≤ W_R 的 blob，或 K(l) 與 h⊞ 的 hash 集合不符。",
  "0.8.0 的 Ξ 有四個參數；l 由 guarantor 自組並隨 report 上鏈，ρ 只存各 core pending 的 assignment。",
  "item 失敗由 I 就地換成 error digest 與零 segment，the work-package continues to be valid as a whole。",
  "l 的 key 是 work-package hash；v 是 assurer 集合大小，2–3 是 credential 長度；W_B 是 bundle 上限。",
 ],
 "explanation": "eq. 14.13：Ξ: (P, N_C, ⟨H → H⟩, N_V) → ℝ ∪ {∇}，(p, c, l, v) ↦ ∇ if E，否則 (s, c ↦ p_c, c, a ↦ p_a, t, l, d, g)。其中 (t, g) = Ψ_I(p, c)——Is-Authorized 必須先跑，「to ensure that the work-package warrants the needed core-time」；E = t ∉ B_{:W_R} ∨ K(l) ≠ {h | w ∈ p_w, (h⊞, n) ∈ w_i}。work-item 的 Refine 失敗（∞、☇、BAD、BIG、⊚ bad-exports、⊖ oversize）只會由 I 函數把該 digest 的 result 換成 error、exports 換成零 segment——「the work-package continues to be valid as a whole」。0.7.2 是 Ξ(p, c) 兩個參數，l 只以 keys(l) ≡ {…} 且 |l| ≤ 8 隱含定義；0.8.0（配合 #514 可變 validator 數）把 l 與 assurer 數 v 明確列為參數，v 再傳給 A（eq. 14.17–14.18）決定 erasure coding 的 shard 數，鏈上 eq. 11.31 要求 (w_s)_n = |κ′|。eq. 14.14：guarantor 要自行確認 l 的每一對 (h ↦ e) 真的對應（H(p) = h 且 Ξ(p, …)_s 的 segroot = e），否則「consider the work-package unable to be guaranteed」；auditor 直接沿用 report 裡的 l。你們 issue #1015/#1026：WorkPackageSpec 加 erasure_shards，Producer 設為 TotalShards。",
 "trap": "Ξ 失敗只有兩種：Is-Authorized 失敗、l 的 key 集合不對；item 失敗不會讓 Ξ 失敗。"
},
{
 "id": "ch14-paged-proofs",
 "ch": "14", "section": "14.3.1 Exporting / 14.4.1 Availability Specifier", "gpRef": "eq. 14.12 (P), 14.18 (A: e = M(s), s♣); eq. E.4–E.6 (M, J_x, L_x); eq. 13.12",
 "difficulty": 2, "kind": "concept", "tags": ["work-packages", "segments", "paged-proofs", "merkle"],
  "stemZh": "匯出的 segment 由 availability specification 的 segments-root e 承諾，並透過 paged proof 佐證。哪個敘述正確？",
  "optionsZh": [
   "e = M(s)，是對匯出 segment 所建之定深二元 Merkle 樹的 root，葉子加 '$leaf' 前綴並以零雜湊補到 2 的冪；P(s) 產生 ⌈|s|/64⌉ 個額外的 segment，每個都是「通往某個 64 葉子子樹的 Merkle 路徑 J_6(s, i)、加上該子樹那一頁的 64 個葉子雜湊 L_6(s, i)」的補零編碼；兩者都會被 erasure-code 進長期的 D³L",
   "e = M_B(s)，是對**原始 segment** 取的 well-balanced 二元 Merkle root、不做補齊；P(s) 產生 ⌈|s|/64⌉ 個額外 segment，內容同上；但兩者都存放在可稽核 bundle 之內而不是 D³L 裡",
   "e = M(s)，定深樹的 root；但 P(s) 是每 32 個匯出 segment 產生一個 4,104 octet 的 segment，各帶一頁 32 個葉子雜湊加上它的子樹路徑；而且它們只存在於短期的 Audit DA 裡，因為只有 auditor 會驗證 import",
   "e = M(s)，定深樹的 root；但 P(s) 是每一個匯出 segment 各產生一個額外 segment、各自持有該 segment 自己約 350 位元組的佐證，而且每位 validator 都保存全部，好讓任何節點不必取得碎片就能驗證任何 import"
  ],
  "stem": "Exported segments are committed to by the segments-root e of the availability specification and justified through paged proofs. Which statement is correct?",
 "options": [
  "e = M(s) is the root of a constant-depth binary Merkle tree over the exported segments, its leaves '$leaf'-prefixed and zero-hash-padded to a power of two; P(s) yields ⌈|s|/64⌉ extra segments, each the zero-padded encoding of the Merkle path J_6(s, i) to a 64-leaf subtree plus that subtree's page of 64 leaf hashes L_6(s, i); both are erasure-coded into the long-lived D³L",
  "e = M_B(s), the well-balanced binary Merkle root taken over the raw segments with no padding; P(s) yields ⌈|s|/64⌉ extra segments, each the zero-padded encoding of the Merkle path J_6(s, i) to a 64-leaf subtree plus that subtree's page of 64 leaf hashes L_6(s, i); both are stored inside the auditable bundle rather than in the D³L",
  "e = M(s) is the root of a constant-depth binary Merkle tree over the exported segments, its leaves '$leaf'-prefixed and zero-hash-padded to a power of two; P(s) yields one 4,104-octet segment per 32 exported segments, each carrying a page of 32 leaf hashes plus its subtree path; they live only in the short-term Audit DA, since auditors are the only ones who verify imports",
  "e = M(s) is the root of a constant-depth binary Merkle tree over the exported segments, its leaves '$leaf'-prefixed and zero-hash-padded to a power of two; P(s) yields one extra segment per exported segment, each holding that segment's own ≈350-byte justification, and every validator stores all of them so that any node can verify any import without fetching chunks"
 ],
 "answer": 0,
 "optNotes": [
  "§14.3.1 明指 segment root 用 eq. E.4 的固定深度 M，eq. 14.12 每 64 個 segment 一頁，兩者同進 D³L。",
  "M_B（E.3）是 well-balanced 無填充版，用在 erasure root 與 extrinsic hash；bundle 裝的是本包 import 的 justification。",
  "頁大小是 2^6 = 64（DA load 才會是 65/64）；逐一驗 import justification 的其實是 guarantor。",
  "§14.2.2 正因這種資料 too voluminous to have all validators store all data，才改成 64 個 segment 一頁。",
 ],
 "explanation": "§14.3.1：segments-root「is formed as the root of a constant-depth binary Merkle tree as defined in equation E.4」，即 A 的 e = M(s)（eq. 14.18）；E.4/E.7：M 先把每個 leaf 做 H($leaf ⌢ v) 再零填到 2 的冪——固定深度讓 import 證明的大小固定（eq. 14.7 的 32·⌈log₂ W_X⌉）。eq. 14.12：P(s) = [P_{W_G}(E(↕J_6(s, i), ↕L_6(s, i))) | i < ⌈|s|/64⌉]——每頁一個 segment，內容是 root 到該 64-leaf 子樹的路徑 J_6（E.5）加上這 64 個 leaf hash 的頁 L_6（E.6），零填到 4,104；§14.4.1：「exactly ⌈1/64⌉ paged-proof segments as the number of yielded segments, each composed of a page of 64 hashes of segments, together with a Merkle proof from the root to the subtree-root which includes those 64 segments」。它們與 exported segments 串接後（s ⌢ P(s)）一起被 C_v 切片、轉置後做成 s♣ → erasure root（eq. 14.18），存在長期的 D³L；importer「each justification can be derived through a single paged-proof」，最壞每個 import 多抓一個 segment，連續 import 共用一頁。這也是 eq. 13.12 DA-load 65/64 的由來。你們 work_package.go PagedProofs：Jx(6,…)、Lx(6,…)、PadToMultiple(SegmentSize)；A 用 merkle_tree.M 算 exportsRoot。",
 "trap": "segment root = M（constant depth，$leaf 前綴 + 零填）；paged proof 每 64 個 segment 一頁、存 D³L；65/64。"
},
{
 "id": "ch14-makebundle",
 "ch": "14", "section": "14.4 Computation of Work-Report / 14.2.2 Data Collection and Justification", "gpRef": "eq. 14.15–14.17 (X, L_l, S_l, J_l, B, s = A(H(p), B(p, l), e, v)); §14.3.1 (Audit DA vs D³L lifetimes)",
 "difficulty": 2, "kind": "concept", "tags": ["work-packages", "bundle", "audit-da", "d3l"],
  "stemZh": "guarantor 會把可稽核的 work-bundle B(p, l) 做 erasure coding 放進 Audit DA。這個 bundle 裡究竟有什麼？它與放進 D³L 的東西又有何不同？",
  "optionsZh": [
   "B(p, l) = E(p, X#(p_w), S_l#(p_w), J_l#(p_w)) 並在後面附上完成的 work-report，好讓 auditor 不必碰鏈上資料就能拿自己的結果與 guarantor 的比對；其中每一個序列都帶長度前綴；而 bundle 與「匯出 segment 加其 paged proof」都被保存在同一個儲存區裡 ≥ 28 天（672 個 epoch）",
   "B(p, l) = E(p, X#(p_w), S_l#(p_w), J_l#(p_w))：編碼後的 package、接著每一份 extrinsic blob、再來每一個**匯入**的 segment、最後是那些 import 的 Merkle 佐證——只有佐證路徑帶長度前綴；bundle 屬於短期的 Audit-DA 資料，而匯出 segment 加其 paged proof 則進入長期的 D³L（≥ 28 天 = 672 個 epoch）",
   "B(p, l) 只有 E(p, X#(p_w))：編碼後的 package 與每一份 extrinsic blob，不含匯入的 segment 也不含佐證——auditor 會自己從 D³L 重新取得那些 segment 並檢查它們的 paged proof，就像 guarantor 當初做的那樣；bundle 屬於短期 Audit-DA 資料，匯出 segment 加 paged proof 則進入長期 D³L",
   "B(p, l) = E(p, X#(p_w), S_l#(p_w), J_l#(p_w)) 並附上第五個成分，也就是這個 package 自己的**匯出**：編碼後的 package、每份 extrinsic blob、每個匯入 segment、它們的 Merkle 佐證，最後是這些匯出——只有佐證路徑帶長度前綴；而 bundle 進入長期 D³L（≥ 28 天），只有 paged proof 屬於短期 Audit-DA 資料"
  ],
  "stem": "What exactly goes into the auditable work-bundle B(p, l) that guarantors erasure-code into the Audit DA, and how does that differ from what goes into the D³L?",
 "options": [
  "B(p, l) = E(p, X#(p_w), S_l#(p_w), J_l#(p_w)) with the finished work-report appended, so that auditors can compare their own result against the guarantors' without touching on-chain data; every one of the sequences carries a length prefix; both the bundle and the exported segments with their paged proofs are kept for ≥ 28 days (672 epochs) in the same store",
  "B(p, l) = E(p, X#(p_w), S_l#(p_w), J_l#(p_w)): the encoded package, then every extrinsic blob, then every imported segment and finally the Merkle justifications of those imports — only the justification paths carry length prefixes; the bundle is short-lived Audit-DA data, whereas exported segments plus their paged proofs go to the long-lived D³L (≥ 28 days = 672 epochs)",
  "B(p, l) = E(p, X#(p_w)) only: the encoded package and every extrinsic blob, with no imported segments and no justifications — auditors re-fetch the segments from the D³L and check their paged proofs themselves, exactly as the guarantors did; the bundle is short-lived Audit-DA data, whereas exported segments plus their paged proofs go to the long-lived D³L (≥ 28 days = 672 epochs)",
  "B(p, l) = E(p, X#(p_w), S_l#(p_w), J_l#(p_w)) with the exported segments appended as a fifth component: the encoded package, every extrinsic blob, every imported segment, their Merkle justifications and finally this package's own exports — only the justification paths carry length prefixes; the bundle goes to the long-lived D³L (≥ 28 days = 672 epochs) while the paged proofs alone are short-lived Audit-DA data"
 ],
 "answer": 1,
 "optNotes": [
  "bundle 只有四個元件、不含 report；GP 也明說只有 justification 的 Merkle path 帶長度前綴。",
  "eq. 14.16 的四段順序與「只有 justification path 有長度前綴」都吻合，且 bundle 屬短期 Audit DA。",
  "正好把 §14.2.2 要避免的成本加回去：auditing 每包平均 30 次、guaranteeing 只有 2–3 次。",
  "export 走的是 A 的第三個參數（s ⌢ P(s) 進 D³L）；bundle 只留到 availability 那塊 finalize 為止。",
 ],
 "explanation": "eq. 14.16：B(p, l) = E(p, X#(p_w), S_l#(p_w), J_l#(p_w))；eq. 14.15：X(w) = 依 w_x 順序的 extrinsic 原始 blob（H(d) 與 |d| 必須吻合）；L_l 把 h⊞ 透過 l 換成 segment root；S_l(w) = 每個 (r, n) ∈ w_i 對應的 segment b[n]（M(b) = L_l(r)）；J_l(w) = ↕J_0(b, n)，每個 import 的 Merkle 路徑。「Note the lack of length prefixes: only the Merkle paths for the justifications have a length prefix. All other sequence lengths are determinable through the work package itself」（extrinsic 長度在 w_x、segment 固定 4,104、import 數量在 w_i）。這個 bundle 就是 A 的第二個參數：s = A(H(p), B(p, l), ē, v)，(w_s)_l = |B(p, l)|（eq. 14.17–14.18），被 C_v 切成 v 個 chunk 進**短期** Audit DA——§14.3.1：「assurers are expected to keep them only until finality of the block in which the availability of the work-result's work-package is assured」；exported segments + P(s) 則進**長期** D³L，「kept for a minimum of 28 days (672 complete epochs)」。理由（§14.2.2）：guarantor 已用 justification 驗過 import，但「We do not force auditors to go through the same process」——寧可在 D³L 與 Audit DA 之間重複資料以降低 auditor 成本。你們 work_package.go BuildWorkPackageBundle：WorkPackageBundle{Package, Extrinsics, ImportSegments, ImportProofs}。0.8.0 才把它命名為 B 並明確以 (p, l) 為參數（issue #1015「explicit make-bundle / compute-report semantics」）。",
 "trap": "bundle = package ⌢ extrinsics ⌢ import segments ⌢ justifications（只有 justification path 有長度前綴）；短期 Audit DA vs 長期 D³L（672 epochs）。"
},
]
