# -*- coding: utf-8 -*-
"""Batch c3 — GP 0.8.0 §7 Recent History and §8 Authorization.

Ground truth: /root/work/jam/gp-src/text/recent_history.tex, authorization.tex,
merklization.tex (MMB append E.8 / super-peak E.10, state key C(3)), beefy.tex,
reporting_assurance.tex (eq. 11.32, 11.36, 11.41-11.44), pvm_invocations.tex
(Psi_I = eq. B.1-B.2, assign = Omega_A index 16), preamble.tex (symbols),
definitions.tex (H = 8, O = 8, Q = 80, C = 341, G_I = 50,000,000, W_A = 64,000).
Code excerpts: /root/work/jam/team-repo (GP 0.7.2).
"""

ITEMS = [
    # ------------------------------------------------------------------ §7
    {
        "id": "c3-ch07-reported-map-shape",
        "ch": "7",
        "section": "7 Recent History",
        "gpRef": "eq. 7.2 & 7.8; §7",
        "difficulty": 1,
        "kind": "concept",
        "tags": ["recent-history", "reported-packages"],
  "stemZh": "β_H 的每一項都帶一個欄位 p。在 GP 0.8.0 中，p 裝什麼？它的條目數又受什麼所限？",
  "optionsZh": [
   "一個字典，以該區塊中每個被擔保的 work-package 雜湊為 key、值是該 package 的 segment-root；至多 C = 341 項，因為一個區塊每個 core 至多只能回報一份 work-report",
   "一個集合，裝的是該區塊各祖先的 header 雜湊；至多 H = 8 項、對應近期歷史窗口保留的每一塊，而這正是把 refinement context 的 anchor 限制在八塊深度之內的機制",
   "一個字典，以每個被擔保的 work-package 雜湊為 key、值是該工作所在 core 的索引；至多 O = 8 項，與一個 core 的 authorizer pool 大小相同",
   "一個序列，裝的是該區塊每份 report 中每個 work-item 的 payload 雜湊；至多 I = 16 項，也就是單一 work-package 可攜帶的 work-item 上限，因此這個界限不隨 core 數量成長"
  ],
  "stem": "Every item of β_H carries a field p. In GP 0.8.0, what does p hold, and what bounds the number of entries it can have?",
        "options": [
            "A dictionary keyed by each work-package hash guaranteed in that block, whose value is that package's segment-root; at most C = 341 entries, because a block can report at most one work-report per core",
            "A set holding the header hashes of the block's ancestors; at most H = 8 entries, one for each block kept in the recent-history window, which is what bounds a refinement context's anchor to eight blocks of depth",
            "A dictionary keyed by each guaranteed work-package hash, whose value is the index of the core the work ran on; at most O = 8 entries, matching the size of a core's authorizer pool",
            "A sequence of the payload hashes of every work-item in every report of the block; at most I = 16 entries, the maximum number of work-items one work-package may carry, so the bound does not scale with the number of cores",
        ],
        "answer": 0,
        "optNotes": [
            "§7 原文就寫 no more than the total number of cores, C = 341，且 value 是 segment-root。",
            "header hash 存在同一個 item 的 h 欄位；anchor 深度 8 來自 β_H 本身的 :H 截斷，不是 p 的內容。",
            "core index 從頭到尾沒有進 β（report 自帶 w_c），O = 8 是 authorizer pool 的上限。",
            "I = 16 是單一 work-package 的 work-item 數上限（eq. 14.2），而一個區塊可有多達 C 份 report。",
        ],
        "explanation": "eq. 7.2 宣告 p ∈ D⟨H → H⟩（hash 對 hash 的 dictionary），eq. 7.8 把它建成 {((g_r)_s)_p ↦ ((g_r)_s)_e | g ∈ E_G}，也就是「本區塊 guarantee 的 work-package hash ↦ 該 package 的 segment-root（exports root）」。§7 原文說得很直白：\"the corresponding work-package hashes of each item reported (which is no more than the total number of cores, C = 341)\" —— 上限來自每個 core 每個區塊至多一份 report（eq. 11.32 要求 ρ‡[w_c] = ∅）。團隊 0.7.2 對應的型別是 []ReportedWorkPackage{Hash, ExportsRoot}，其 Validate() 正是拿 CoresCount 當上限。",
        "trap": "p 的 value 不是隨便的雜湊，是 segment-root；eq. 11.44 要靠這個 value 驗 segment-root 與 package hash 配對。",
    },
    {
        "id": "c3-ch07-reported-map-downstream",
  "alsoCh": ["11"],
        "ch": "7",
        "section": "7 Recent History",
        "gpRef": "eq. 7.8 & eq. 11.41–11.44",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["recent-history", "guarantees", "anti-replay"],
  "stemZh": "當某個區塊的 guarantees extrinsic E_G 在 §11 被驗證時，哪些鏈上檢查實際上會讀取存放在 β_H 裡的 reported-package 映射？",
  "optionsZh": [
   "有三項：進來的 package 雜湊不得已經是任何近期區塊之映射的 key（反重複）；每個 prerequisite 以及某份 report 之 segment-root lookup l 的每個 key 都必須是那樣的 key、或來自本塊自己的 guarantee；而且 l 必須是那些映射的子字典，因此每個 segment-root 都要與它的 package 雜湊相符",
   "只有反重複那一項；prerequisite 與 segment-root lookup 改為對照 ξ（accumulation 歷史）與 ready queue ω 解析，而它們的依賴集合才是最終讓一份 report 得以進入 accumulation 的關鍵——所以 β_H 裡的映射在那裡是多餘的，純粹為了重複測試而存在",
   "只有 refinement-context 的 anchor 檢查：anchor 的 header 雜湊、state root、super-peak 與時槽全都是在 β† 的映射中查找的，而重複則留到 accumulation 階段才抓，屆時已經出現在 ξ 裡的 package 雜湊只會被從 ready queue 丟掉而不會讓區塊無效",
   "一項都沒有：那些映射的存在是為了替第三方建立 BEEFY 的納入證明，而 §11 是靠從區塊儲存中解碼最近八塊的 E_G 來重新導出近期的 package 雜湊——這也是為什麼祖先集合 A 必須保留 L = 14,400 個完整含 extrinsic 的區塊而不只是 header"
  ],
  "stem": "When a block's guarantees extrinsic E_G is validated in §11, which of the on-chain checks actually read the reported-package maps stored inside β_H?",
        "options": [
            "Three of them: an incoming package hash must not already be a key of any recent block's map (anti-duplicate); every prerequisite and every key of a report's segment-root lookup l must be such a key or come from this block's own guarantees; and l must be a sub-dictionary of those maps, so each segment-root matches its package hash",
            "Only the anti-duplicate one; prerequisites and the segment-root lookup are instead resolved against ξ (accumulation history) and the ready queue ω, whose dependency sets are what eventually clear a report for accumulation — so the maps in β_H would be redundant there and exist purely for the duplicate test",
            "Only the refinement-context anchor check: the anchor's header hash, state root, super-peak and timeslot are all looked up among the maps of β†, while duplicates are caught later during accumulation, where a package hash already present in ξ is simply dropped from the ready queue instead of invalidating the block",
            "None of them: the maps exist to build BEEFY inclusion proofs for third parties, and §11 re-derives recent package hashes by decoding the E_G of the last eight blocks out of the block store — which is why the ancestor set A must retain L = 14,400 blocks complete with their extrinsics rather than headers alone",
        ],
        "answer": 0,
        "optNotes": [
            "eq. 11.41 反重複、11.42 解 prerequisite 與 l 的 key、11.44 要求 w_l 是子字典，三處都讀 p。",
            "ξ 與 ω 只是 eq. 11.41 聯集裡的額外來源；eq. 11.42 的 prerequisite 檢查照樣讀 β_H 的 p。",
            "anchor 檢查是 eq. 11.36、比對 h/s/b/t 與 p 無關；eq. 11.41 撞到就整塊不合法，不會留到 accumulation。",
            "p 上鏈正是為了不必翻舊 extrinsic；ancestor set A 只留 header，BEEFY 承諾的是 β_B 的 super-peak。",
        ],
        "explanation": "β_H 每筆裡的 p 是一個字典：**work-package hash ↦ segment root（exports root）**。§11 有三處檢查會讀它，各自防的是不同的事。**① 防重複／防過期**（eq. 11.41）：本塊要進來的每個 package hash 都不得出現在任何 β_H 條目的 p 的鍵集合裡（也不得在 ξ、ready queue 或 accumulated 集合裡）。這就是 §7 開宗明義那句「to preclude the possibility of duplicate or out of date work-reports」的落實處。**② 依賴必須有著落**（eq. 11.42）：report 的 prerequisites 與 segment-root lookup l 的每個鍵，必須落在**本塊自己的 E_G**、或某個 β_H 條目的 p 的鍵裡——所以依賴可以指向同一塊裡的兄弟 report，也可以指向最近 8 塊內的舊 report，但不能懸空。**③ 值也要對**（eq. 11.44）：w_l ⊆ 本塊的 package↦segment-root 映射 ∪ ⋃_{b ∈ β_H} b_p——注意這是**字典的包含關係**而不只是鍵的包含，所以 segment root 這個**值**也必須與 p 記錄的一致，不能宣稱某個 package 有別的 exports root。**一句話記憶**：p 同時扮演「這份工作做過了嗎」與「它的 exports root 是什麼」兩個角色，前者防重複、後者讓後續 report 能安全地引用先前的匯出段。",
        "trap": "同一份 map 同時被用來「拒絕重複」與「接受依賴」——方向相反，別記反了。",
    },
    {
        "id": "c3-ch07-superpeak-to-beefy",
        "ch": "7",
        "section": "7 Recent History",
        "gpRef": "eq. 7.7, 7.8; eq. E.8, E.10; §18 Beefy",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["recent-history", "mmr", "beefy", "keccak"],
  "stemZh": "追蹤一個區塊的 accumulation 產出最終如何進入 BEEFY 簽章。哪個描述符合 GP 0.8.0？",
  "optionsZh": [
   "每個區塊把編碼後的 θ′ 以 Keccak Merklize 成一個 root 並把該 root 附加到 belt β_B；新的 β_H 項目只儲存 belt 的 Keccak super-peak；validator 接著對它們所定案的每個區塊，以 BLS 簽署最新項目之 super-peak 的 domain-separated 雜湊",
   "每個區塊把 θ′ 以 Keccak Merklize 成一個 root、附加到 β_B，而 validator 以 BLS 簽署 β_B 的整個編碼後 peak 序列；super-peak 的存在只是為了讓 state key C(3) 有一個定長欄位，這也是為什麼 eq. 18.1 被簽的訊息是 E(mmrencode(β_B)) 而不是單一個雜湊",
   "區塊 header 在一個專屬的 marker 中攜帶 super-peak，而 validator 簽署的是 header 雜湊；β_B 只是 guarantor 端的簿記、從不進入序列化的狀態，所以橋接方永遠只需要 header 鏈、不必讀任何狀態證明",
   "belt 每個區塊都以 Blake2b 從 θ 重建，而 validator 只簽署當前區塊產出的 root，所以一個 BEEFY 簽章恰好佐證一個區塊的 accumulation 結果；想要較舊產出的驗證者則從該區塊自己的 C(16) 條目重新導出它的 root"
  ],
  "stem": "Trace how a block's accumulation outputs end up inside a BEEFY signature. Which description matches GP 0.8.0?",
        "options": [
            "Each block Keccak-Merklizes the encoded θ′ into one root and appends that root to the belt β_B; the new β_H item stores only the belt's Keccak super-peak; validators then BLS-sign the domain-separated hash of the newest item's super-peak for each block they finalize",
            "Each block Keccak-Merklizes θ′ into one root, appends it to β_B, and validators BLS-sign the whole encoded peak sequence of β_B; the super-peak exists only so that state key C(3) has one fixed-length field, which is why eq. 18.1's signed message is E(mmrencode(β_B)) rather than a single hash",
            "The block header carries the super-peak in a dedicated marker and validators sign the header hash; β_B is guarantor-side bookkeeping that never enters the serialized state, so a bridge only ever needs the header chain and never has to read a state proof",
            "The belt is rebuilt from θ with Blake2b every block and validators sign the root of the current block's outputs alone, so one BEEFY signature attests exactly one block's accumulation results and a verifier wanting an older output re-derives its root from that block's own C(16) entry",
        ],
        "answer": 0,
        "optNotes": [
            "eq. 7.7 append 的是 M_B(s, H_K)、eq. 7.8 的 b 存 super-peak、eq. 18.1 簽 X_B ⌢ last(β_H)_b。",
            "完整 peak 序列只以 mmrencode(β_B) 進 C(3)；eq. 18.1 簽的是壓成 32-byte 的 super-peak。",
            "eq. 5.1 只有 epoch／winners／offenders 三個 marker；belt 確實進了 C(3)，bridge 仍得走狀態證明。",
            "MMB 是 append-only 且全程用 Keccak；C(16) 只裝本區塊的 θ，翻不到舊區塊的 root。",
        ],
        "explanation": "eq. 7.6–7.7：s = [E_4(s) ⌢ E(h) | (s, h) ∈ θ′]，β′_B ≡ A(β_B, M_B(s, H_K), H_K)，全程用 Keccak，GP 原文的理由是 \"to maximize compatibility with legacy systems\"。eq. 7.8 新 item 的 b 欄位放 M_R(β′_B)，也就是 belt 的 super-peak（eq. E.10：先濾掉 ∅ peaks，只剩一個就直接回傳，否則以 $peak ⌢ M_R(前 n−1 個) ⌢ 最後一個 由右向左折疊）。beefy.tex eq. 18.1：F_v ≡ S^BLS_{κ′[v]_l}(X_B ⌢ last(β_H)_b)，X_B = $jam_beefy，對每個 finalized block 簽一次。把序列壓成單一 commitment 才能給第三方簡潔證明。GP 0.8.0 的用語是 MMB（Merkle mountain belt）／Accumulation Output Log，團隊 0.7.2 程式碼叫它 beefyBelt / BeefyRoot，是同一個東西。",
        "trap": "θ′ 是本區塊的輸出序列（另一個狀態項），β_B 是跨區塊的 belt；被 append 的是 θ′ 的 M_B root，不是 θ′ 本身。",
    },
    {
        "id": "c3-ch07-dagger-before-append",
        "ch": "7",
        "section": "7 Recent History",
        "gpRef": "eq. 7.5, 7.8 & eq. 11.36",
        "difficulty": 2,
        "kind": "rationale",
        "tags": ["recent-history", "pipelining", "ordering"],
  "stemZh": "某個實作者建構 β′_H 的方式是：先附加本塊的新項目（state root = H_0），然後才把 eq. 7.5 的父狀態根回填套用到「序列的最後一個元素」上。實際上會出什麼錯？",
  "optionsZh": [
   "那次回填會落在本塊自己剛新增的項目上，於是每一筆條目最後帶的都是它父區塊的 posterior root 而不是自己的，而父區塊那一筆則從未收到原本要給它的修正；從此 eq. 11.36 的 state-root 比對會拒絕誠實的 refinement context，而 C(3) 的原像也會與其他每個節點分歧",
   "沒有可觀察的問題：一旦該區塊完成，兩種順序下最後一個元素都是同一個項目，而且 eq. 7.5 的修正是冪等的，所以兩種順序產生相同的 C(3) 原像——這正是為什麼 GP 把 β† 表述成 β_H 的一個例外、而不是去規定運算順序，也是為什麼各家實作在此不同卻不會分歧",
   "只有 β_B 會壞掉：新項目的 super-peak 會取自一個未經修正的 belt，所以 BEEFY 的 root 會漂移，而近期歷史的條目與 state root 仍然正確，因為 eq. 7.7 會把父區塊回填後的 state root 摺進它所附加的葉子裡，而 eq. 11.36 從不看 b",
   "歷史窗口會提早一塊滑動，使 β_H 永久停在 H − 1 = 7 個條目，所以 eq. 11.36 會拒絕恰好八塊之前的任何 anchor，而其餘一切仍然相符，因為 ←(…)^H 的截斷屬於 eq. 7.5 而不屬於 eq. 7.8 的附加——症狀是 guarantee 被拒絕，絕不會是 state-root 不符"
  ],
  "stem": "An implementer builds β′_H by first appending this block's new item (state root = H_0) and only then applying the parent-state-root back-fill of eq. 7.5 to 'the last element of the sequence'. What actually goes wrong?",
        "options": [
            "The back-fill lands on the block's own fresh item, so every entry ends up carrying its parent's posterior root instead of its own, and the parent's entry never receives the correction it was meant for; from then on eq. 11.36's state-root comparison rejects honest refinement contexts and the C(3) preimage diverges from every other node's",
            "Nothing observable: the last element is the same item either way once the block is finished, and eq. 7.5's correction is idempotent, so both orders produce the same C(3) preimage — which is precisely why the GP states β† as an exception on β_H instead of fixing an order of operations, and why implementations differ here without diverging",
            "Only β_B is corrupted: the new item's super-peak would be taken from an uncorrected belt, so BEEFY roots drift apart while the recent-history entries and the state root stay correct, because eq. 7.7 folds the parent's back-filled state root into the leaf it appends and eq. 11.36 never looks at b",
            "The history window slides one block too early, leaving β_H permanently at H − 1 = 7 entries, so eq. 11.36 rejects any anchor exactly eight blocks old while everything else still matches, since the ←(…)^H truncation belongs to eq. 7.5 rather than to the append of eq. 7.8 — the symptom is a rejected guarantee, never a state-root mismatch",
        ],
        "answer": 0,
        "optNotes": [
            "eq. 7.5 的定義域是 append 前的 β_H，順序顛倒會讓修正落在新 item 上，整條系統性 off-by-one。",
            "兩種順序改到的是不同的 item，「idempotent、序列化結果一樣」因此不成立。",
            "β† 完全不碰 β_B（belt 的 leaf 由 θ′ 編碼而來），而 eq. 11.36 確實也比對 x_b = y_b。",
            "←(…)^H 的截斷在 eq. 7.8 的 append 而非 eq. 7.5；先炸的是 state root，不是 guarantee。",
        ],
        "explanation": "eq. 7.5 的 β† ≡ β_H 只改「β_H 最後一個 item」的 s ← H_R，而 H_R 是本區塊 header 攜帶的 *parent* posterior state root（header.tex：JAM 刻意在 header 放 prior state root 以利 pipelining）。正確順序是先 β_H → β†（修好上一個區塊的 s），再 append 新 item 且 s = H_0。順序顛倒後，被修的是剛 append 的新 item，於是它拿到的是「上一個區塊」的 root，而上一個區塊的 item 再也拿不到本該補給它的 root（注意：不會有任何 item 停在 H_0，新 item 一 append 就被錯位的修正立刻蓋掉）。後果有兩層：eq. 11.36 要求 x_s = y_s（context 的 anchor posterior state root 對上 β† item 的 s），guarantor 給的是真值，這台節點比對必失敗；而 C(3) 直接把每個 item 的 s 編進狀態序列化，state root 立刻和別人不同，fuzz trace 會停在 state-root mismatch。GP 自己的註腳講清楚了為什麼 H_0 是安全的：\"β′ is not utilized except to define the next block's β†\"。",
        "trap": "β† 修的是「上一個區塊」的 s，不是自己的；先修再 append，順序寫反不會報錯，只會 state root 不對。",
    },
    {
        "id": "c3-ch07-c3-field-order",
        "ch": "7",
        "section": "7 Recent History",
        "gpRef": "eq. 7.2 & §D.1 state key C(3)",
        "difficulty": 3,
        "kind": "code",
        "tags": ["recent-history", "codec", "delta-0.8.0", "gotcha"],
  "stemZh": "這是團隊在 state key C(3) 之下、為單一筆 β_H 項目所寫的 GP 0.7.2 編碼器。有位審閱者反對，認為 GP 0.8.0 把該項目宣告為 ⟨h, s, b, t, p⟩——state root 排在 accumulation-output-log 的 super-peak 之前——所以這個編碼器一定把兩個欄位對調了。誰說得對？",
  "optionsZh": [
   "編碼器的順序是對的：狀態序列化是由附錄 D 的 C(3) 定死的，它送出的是 header 雜湊、然後 super-peak、然後 state root、然後時槽、最後是 reported 映射；第 7 章的那個元組只是在命名各成分。真正的 0.8.0 落差是 state root 與 reported 映射之間少了那個 4 位元組的時槽",
   "審閱者是對的：一個狀態分量永遠依它的定義式所列欄位順序序列化，所以 C(3) 需要的是 header 雜湊、state root、super-peak、時槽、reported 映射；附錄 D 只是重述第 7 章的元組、兩者不可能牴觸，所以照現況這個編碼器會產生錯誤的 C(3) 原像、因而產生錯誤的 state root",
   "兩者都錯：C(3) 只裝 β_B 編碼後的 peak 序列，而逐區塊的項目是透過 header 裡的一個 marker 承諾、其餘由各節點自行保存在鏈外，所以這個編碼器根本不該餵給狀態序列化，它用哪種順序都動不了 state root",
   "審閱者在順序與形狀上都對：0.8.0 把每個項目的 super-peak 換成了完整的 peak 序列，所以每一項都必須編碼整條 belt，而這段程式碼卻只寫了單一個 32 位元組的雜湊；eq. 11.36 也是拿 anchor 去對照那個序列而不是對照單一個承諾"
  ],
  "stem": "This is the team's GP 0.7.2 encoder for one β_H item under state key C(3). A reviewer objects that GP 0.8.0 declares the item as ⟨h, s, b, t, p⟩ — state root ahead of the accumulation-output-log super-peak — so the encoder must have two fields swapped. Who is right?",
        "code": {
            "lang": "go",
            "caption": "internal/types/encode.go:1950-1980 (BlockInfo.Encode; log line elided)",
            "src": """func (bi *BlockInfo) Encode(e *Encoder) error {
	// HeaderHash
	if err := bi.HeaderHash.Encode(e); err != nil {
		return err
	}
	// BeefyRoot
	if err := bi.BeefyRoot.Encode(e); err != nil {
		return err
	}
	// StateRoot
	if err := bi.StateRoot.Encode(e); err != nil {
		return err
	}
	// Reported
	if err := e.EncodeLength(uint64(len(bi.Reported))); err != nil {
		return err
	}
	for _, reportedWorkPackage := range bi.Reported {
		if err := reportedWorkPackage.Encode(e); err != nil {
			return err
		}
	}
	return nil
}""",
        },
        "options": [
            "The encoder's order is right: state serialization is fixed by C(3) in appendix D, which emits header hash, then super-peak, then state root, then the timeslot, then the reported map; the tuple in chapter 7 merely names the components. The real 0.8.0 gap is the missing 4-byte timeslot between the state root and the reported map",
            "The reviewer is right: a state component is always serialized in the order its defining equation lists the fields, so C(3) needs header hash, state root, super-peak, timeslot, reported map; appendix D merely restates the tuple of chapter 7 and the two can never disagree, so as written the encoder produces the wrong C(3) preimage and therefore the wrong state root",
            "Both are wrong: C(3) holds only the encoded peak sequence of β_B, while the per-block items are committed through a marker in the header and otherwise kept off-chain by each node, so this encoder should not be feeding state serialization at all and whichever order it uses cannot move the state root",
            "The reviewer is right about the order and about the shape: 0.8.0 replaced the per-item super-peak with the full peak sequence, so each item must encode the whole belt where this code writes a single 32-byte hash, and eq. 11.36 compares an anchor against that sequence rather than against one commitment",
        ],
        "answer": 0,
        "optNotes": [
            "D.1 的 C(3) 明寫 ⟨h, b, s, E_4(t), var(p)⟩，b 排在 s 前面；真正缺的是 0.8.0 的 4-byte t。",
            "「附錄 D 只是重述第 7 章的 tuple」正是本題要打掉的直覺：D.1 是獨立定義，就是把 b 排在 s 前面。",
            "header 只有 epoch／winners／offenders 三個 marker；C(3) 同時存整條 belt 與每一筆 item。",
            "eq. 7.2 把 b 的型別寫成 b ∈ H（E.10 算出的單一 super-peak），eq. 11.36 也只比一個 32-byte 值。",
        ],
        "explanation": "兩個地方都是 0.8.0 原文，但講的是不同的事。eq. 7.2 用具名欄位宣告集合：β_H ∈ ⟦⟨h ∈ H, s ∈ H, b ∈ H, t ∈ N_T, p ∈ D⟨H → H⟩⟩⟧_:8。附錄 D 的 C(3) 才是序列化定義，它明寫成 E(var[⟨h, b, s, E_4(t), var(p)⟩ | … ∈ β_H], mmrencode(β_B))——super-peak 在 state root 前面。GP 具名 tuple 的欄位順序不等於 codec 順序，狀態這一塊以 D.1 為準；jam test vectors 的 history JSON（header_hash, mmr, state_root, reported）與團隊的 BlockInfo{HeaderHash, BeefyRoot, StateRoot, Reported} 都跟 D.1 一致，這段 0.7.2 程式碼的順序沒問題。真正要補的是 0.8.0 新增的 t：GP PR #526 把 anchor 的 timeslot 放進 refinement context，eq. 11.36 因此多比一項 x_n = y_t，團隊 PR #1031 就是在 state_root 與 reported 之間插入 4-byte timeslot。",
        "trap": "宣告順序 ≠ 編碼順序。C(3) 是 b 在 s 前面；照 chapter 7 的順序寫 codec，值全對也會 state root 不對。",
    },
    # ------------------------------------------------------------------ §8
    {
        "id": "c3-ch08-queue-writer",
        "ch": "8",
        "section": "8.2 Pool and Queue",
        "gpRef": "§8.2 (note under eq. 8.1); assign host call (index 16)",
        "difficulty": 1,
        "kind": "concept",
        "tags": ["authorization", "privileges", "host-calls"],
  "stemZh": "在 GP 0.8.0 中，誰有權更改某個 core 的 authorizer queue φ[c]？又是透過什麼機制？",
  "optionsZh": [
   "只有當前登記為該 core 之 assigner 的那個 service，而且只能在它的 accumulate 執行期間、藉由呼叫 `assign`——該呼叫會在單一次呼叫中替換那個 core 佇列的全部 Q = 80 個條目，並且也可以把 assigner 的角色轉交給另一個 service",
   "任何 service 都可以呼叫 `assign`，但寫入只在 pool 已經空掉的 core 上生效；manager service 隨時可以用 `bless` 覆寫任何 core，而兩種寫入都落在區塊結尾，因此一個 core 不可能被連續重新指派兩次",
   "由出塊者，藉由在 E_G 之外把一份授權 extrinsic 當成 extrinsic 的第六個成員納入；其他 validator 會拿它去對照 coretime 銷售紀錄再接受該區塊，而 φ′ 就直接是那份 extrinsic 所宣告的內容",
   "鏈上沒有人：φ 是每個節點對已購買 coretime 的本地視圖，由 coretime 鏈在鏈外傳播，只有對它的一個承諾會進入共識——而且就搭載在公布該 epoch 中選 ticket 的同一個 header marker 裡"
  ],
  "stem": "Who is permitted to change a core's authorizer queue φ[c] in GP 0.8.0, and through what mechanism?",
        "options": [
            "Only the service currently registered as that core's assigner, and only from inside its accumulate execution, by calling `assign`, which replaces all Q = 80 entries of that one core's queue in a single call and may also hand the assigner role to another service",
            "Any service may call `assign`, but the write only takes effect on cores whose pool has fallen empty; the manager service can override any core at any time with `bless`, and both writes land at the end of the block so that a core cannot be re-assigned twice in a row",
            "The block author, by including an authorization extrinsic alongside E_G as the sixth member of the extrinsic; the other validators re-check it against the coretime-sales record before accepting the block, and φ′ is then simply whatever that extrinsic declares",
            "Nobody on-chain: φ is each node's local view of purchased coretime, gossiped off-chain by the coretime chain, and only a commitment to it ever reaches consensus — carried in the very same header marker that publishes the epoch's winning tickets",
        ],
        "answer": 0,
        "optNotes": [
            "§8.2 明訂 φ 只能由 privileged service 的 accumulate 呼叫 assign 整批覆寫，並可順手轉手 χ_A[c]。",
            "Ω_A 的呼叫者 ≠ χ_A[c] 就回 HUH；bless 動的是 χ 的 privileges、碰不到 φ，也與 pool 空不空無關。",
            "extrinsic 只有 E_T、E_P、E_G、E_A、E_D 五種，coretime 的成交紀錄也不是鏈上共識條件。",
            "eq. 8.1 的 φ 是不折不扣的狀態元件（序列化在 C(2)）；eq. 5.1 的 marker 只有三個。",
        ],
        "explanation": "§8.2 在 eq. 8.1 底下直接寫死：\"The portion of state φ may be altered only through an exogenous call made from the accumulate logic of an appropriately privileged service.\" 那個 privileged service 就是 χ_A[c]（per-core assigner）。host call Ω_A（`assign` = 16）從 ω_7..ω_9 取 (c, o, a)，自 memory 位址 o 讀 Q = 80 個 32-byte hash：c ≥ C 回 CORE，呼叫者 service id ≠ χ_A[c] 回 HUH，a 不是合法 service id 回 WHO，成功才 φ[c] ← q 並把 χ_A[c] ← a（Owned Privileges，讓 assigner 可以轉手）。所以是整批覆寫單一 core 的 queue，不是逐格插入。`bless` 動的是 χ 的 privileges（0.8.0 PR #519 起只有 manager 能呼叫）。",
        "trap": "「誰能寫 φ」與「誰能寫 χ」不同：assign 由 per-core assigner 呼叫，bless 只屬於 manager。",
    },
    {
        "id": "c3-ch08-rotation-index-cyclic",
        "ch": "8",
        "section": "8.2 Pool and Queue",
        "gpRef": "eq. 8.1–8.2",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["authorization", "rotation"],
  "stemZh": "每個區塊都會把恰好一個佇列條目移進每個 core 的 pool。那個條目是怎麼被挑中的？而那些沒有出塊之時槽所對應的條目又會怎麼樣？",
  "optionsZh": [
   "靠對區塊自身時槽做的循環下標，也就是索引 H_T mod Q，任何地方都沒有儲存游標；沒有產出區塊的時槽，其條目這一輪就是不會被抽到，而那個索引要再過 80 個時槽才會輪回來",
   "靠一個放在 pool 旁邊、每匯入一個區塊就前進一步的逐 core 游標，所以沒有任何佇列條目會被跳過——空時槽只是延後了輪替，而該游標與 α[c] 一起序列化在 state key C(1) 之下",
   "靠索引 H_T mod O，所以只有前八個佇列位置會輪進 pool，其餘 72 個在 `assign` 呼叫把它們往前挪之前都無法觸及，因此停在索引 40 的 authorizer 在 `assign` 輪動佇列之前一直碰不到",
   "靠取出最舊的尚未使用條目（FIFO）並在它進入 pool 時從佇列中刪除，這正是為什麼 assigner 必須至少每 80 個區塊替某個 core 補一次佇列，也是為什麼 φ[c] 在兩次補充之間會短於 Q"
  ],
  "stem": "Each block moves exactly one queue entry into every core's pool. How is that entry picked, and what becomes of the entries belonging to slots in which no block was produced?",
        "options": [
            "By cyclic subscription on the block's own timeslot, i.e. index H_T mod Q, with no stored cursor anywhere; a slot that produces no block simply never has its entry drawn, and that index only comes round again 80 slots later",
            "By a per-core cursor kept beside the pool that advances one step per imported block, so no queue entry is ever skipped — an empty slot merely postpones the rotation, the cursor being serialized next to α[c] under state key C(1)",
            "By index H_T mod O, so only the first eight queue positions ever rotate into the pool and the remaining 72 stay unreachable until an `assign` call shifts them forward, so an authorizer parked at index 40 stays out of reach until `assign` rotates the queue",
            "By taking the oldest not-yet-used entry (FIFO) and deleting it from the queue as it enters the pool, which is why the assigner must refill a core's queue at least every 80 blocks and why φ[c] is shorter than Q between refills",
        ],
        "answer": 0,
        "optNotes": [
            "索引由 H_T mod Q 當場算出、鏈上沒有游標，沒出塊的那一格這輪就跳過，80 個 slot 後才同餘回來。",
            "C(1) 只映射到 E([var(x) | x ∈ α])，附錄 D 沒有地方放游標；一旦出現空 slot 就會與參考實作分歧。",
            "O = 8 只出現在最後的 ←(…)^O 截斷；80 格每一格都會在 80 個 slot 內輪到，沒有碰不到的格子。",
            "刪掉用過的項會讓 φ[c] 短於 Q，直接違反 eq. 8.1 的固定長度型別；queue 也不需要定期補。",
        ],
        "explanation": "eq. 8.2：α′[c] ≡ ←(F(c) ⌢ φ′[c]^⟲[H_T])^O。索引的來源是 **header 自己的 timeslot**，經由 §3.7 的模數下標 s^⟲[i] ≡ s[i mod |s|] 化成 H_T mod Q。**沒有任何游標被存在狀態裡**——這是這題的重點。eq. 8.1 規定 φ ∈ ⟦⟦H⟧_Q⟧_C：每個 core 的 queue 是**恰好** Q = 80 個的定長序列（對照 α ∈ ⟦⟦H⟧_{:O}⟧_C 是**至多** O = 8 個），所以取模永遠落在合法範圍內。**空 slot 的後果**：沒有出塊的時槽，其對應的那一格這一輪就是被跳過，要再等 80 個時槽（8 分鐘）繞回來才有機會。這不是遺漏，而是設計——索引綁在時間上，鏈上任何節點都能獨立算出來，不需要協調。**實作陷阱**：若自己維護一個「下一個要取哪格」的游標，在鏈上出現空 slot（Safrole 沒出票、或單純沒人出塊）時就會與參考實作分歧，而且分歧會一直累積下去，state root 從此對不上。**另一個常見誤解**：queue 不會因為被抽取而縮短或清空——它不是 FIFO，同一格會被反覆讀取。唯一能改動 φ 的是 `assign` host call 的整批覆寫。",
        "trap": "抽 queue 用 mod Q（80），截 pool 用 O（8）——兩個常數各司其職，別互換。",
    },
    {
        "id": "c3-ch08-psi-i-visibility",
        "ch": "8",
        "section": "8.1 Authorizers and Authorizations",
        "gpRef": "eq. B.1–B.2; §8.1",
        "difficulty": 2,
        "kind": "concept",
        "tags": ["authorization", "pvm", "delta-0.8.0"],
  "stemZh": "guarantor 在 refine 任何東西之前會先執行 Is-Authorized 邏輯 Ψ_I。那支程式實際上能觀察到什麼？",
  "optionsZh": [
   "只有它的兩個引數——work-package 與 core 索引（後者以 2 位元組編碼的引數交給 PVM）——加上 `fetch` 能從該 package 裡拉出來的東西、以及協定常數；完全沒有任何鏈上狀態，而且除了 `fetch` 之外，僅有的 host call 就是 gas 計數器與堆成長",
   "work-package 加上 service 帳戶 δ 的唯讀快照，經由 Accumulate 所用的同一批 `read` 與 `lookup` host call 取得，所以 authorizer 可以檢查餘額、或確認 coretime 買家仍持有它正在執行的那個 core；該快照釘在 anchor 區塊上，好讓每位 auditor 看到相同的值",
   "work-package、core 索引，以及一個釘在 lookup-anchor 時槽上的歷史查詢，與 Refine 拿到的完全相同，因為授權程式碼本身就是由同一個查詢解析出來的；因此 authorizer 可以讀取其宿主 service 在該時槽之前所請求過的任何 preimage，例如 coretime 買家發布的白名單",
   "work-package 與該 core 自己的 authorizer pool——後者連同 core 索引一起遞入，因為它至多只有 O × 32 = 256 個 octet——好讓那段程式碼能確認自己的雜湊仍在池中、提早中止，而不是把 guarantor 的 gas 燒在一個 eq. 11.32 反正會拒絕的 package 上"
  ],
  "stem": "A guarantor runs the Is-Authorized logic Ψ_I before refining anything. What is that program actually able to observe?",
        "options": [
            "Its two arguments only — the work-package and the core index, the latter handed to the PVM as a 2-byte encoded argument — plus whatever `fetch` can pull out of that package, and the protocol constants; no chain state at all, and besides `fetch` the only host calls are the gas counter and heap growth",
            "The work-package plus a read-only snapshot of the service accounts δ, reached through the same `read` and `lookup` host calls Accumulate uses, so an authorizer can check a balance or confirm that the coretime buyer still holds the core it is running on; the snapshot is pinned to the anchor block so that every auditor sees identical values",
            "The work-package, the core index and a historical lookup pinned to the lookup-anchor timeslot, exactly as Refine gets it, since the authorization code is itself resolved by that same lookup; an authorizer may therefore read any preimage its host service had solicited by that slot, such as a whitelist published by the coretime buyer",
            "The work-package and the core's own authorizer pool, handed in beside the core index because it is at most O × 32 = 256 octets, so that the code can confirm its own hash is still pooled and abort early rather than burn the guarantor's gas on a package eq. 11.32 will reject anyway",
        ],
        "answer": 0,
        "optNotes": [
            "eq. B.2 的 F 只認 gas、grow_heap、fetch 三個 host call，GP 說 Ψ_I totally stateless。",
            "read／lookup 在 eq. B.2 的 F 裡根本叫不出來，一律扣 M_∅ 並把 ω_7 設成 WHAT。",
            "歷史查詢 Λ 是 Ψ_R 的專利（eq. B.5 的 Ω_H）；auth code 由 lookup anchor 解析是外部餵進來的。",
            "eq. B.1 只有 (P, N_C) 兩個參數、argument blob 就是 E_2(c)；能讀 pool 就不再是 stateless。",
        ],
        "explanation": "eq. B.1：Ψ_I : (P, N_C) → (B ∪ E, N_G)，實際執行 Ψ_M(auth code, 0, G_I, E_2(c), F, ∅)，其中 G_I = 50,000,000、argument blob 就是 E_2(c)；auth code 解不出來（∅）回 BAD、長度 > W_A = 64,000 回 BIG。eq. B.2 的 dispatch F 只認三個 host call：gas、grow_heap、fetch，其他一律扣 M_∅ 並把 ω_7 設成 WHAT。GP 原文：\"totally stateless … we elide the host-call context since, being essentially stateless, it is always ∅\"。fetch（Ω_Y）在這裡除了 work-package 之外的參數全是 ∅，所以 selector 0（protocol constants）與 7–13（package 編碼、config、token、context、work-item metadata、payload）可用，selector 1–6 與 14/15（entropy、authorizer trace、extrinsics、import segments）一律回 NONE。正因為 Ψ_I 完全無狀態，每個 auditor 事後重跑必然得到相同結果。0.8.0 delta：堆積成長的 host call 由 0.7.2 的 `sbrk` 更名為 `grow_heap`（index 1，PR #508 的新 gas model 一起改），Go 端的 dispatch 表要跟著改。",
        "trap": "Ψ_I 無狀態 ⇒ 授權邏輯不能讀鏈上餘額；要收錢只能靠 accumulate 那一端。",
    },
    {
        "id": "c3-ch08-authcode-lookup-anchor",
        "ch": "8",
        "section": "8.1 Authorizers and Authorizations",
        "gpRef": "eq. 14.11; §8.1",
        "difficulty": 2,
        "kind": "rationale",
        "tags": ["authorization", "auditing", "determinism"],
  "stemZh": "pool α[c] 裡除了 32 位元組的 authorizer 雜湊之外什麼都沒有。那麼 guarantor 要從哪裡取得可執行的 is-authorized 程式碼？又是以歷史上的哪一個時點解析的？為什麼是那裡？",
  "optionsZh": [
   "從 work-package 所指名的那個獨立 auth-code 宿主 service 的 preimage 儲存中取得，並以該 package 的 lookup-anchor 時槽做歷史查詢解析，好讓很久之後重跑這項檢查的 auditor 仍能解析出逐位元組相同的程式碼，即使該 service 此後已替換或遺忘了那份 preimage",
   "從第一個 work-item 之 service 的帳戶中取得，讀的是 anchor 區塊的 posterior 狀態，因為 anchor 本來就已經把 refinement context 釘在一個每位 validator 都同意過的近期 state root 上——eq. 11.36 已經把那個 root 與 β† 比對過，所以不需要另外的保存規則來維持程式碼可解析",
   "從 work-package 本身取得：程式碼 blob 就與 token 和設定 blob 一起在 bundle 裡傳送，而那正是 64,000 個 octet 的上限所限制的東西，所以 guarantor 根本不需要做 preimage 查詢，而 α[c] 中所池化的雜湊就只是那段程式碼區段的 Blake2b",
   "從 pool 條目本身取得：α[c] 裡的雜湊就是「程式碼串接其設定」的 preimage 雜湊，所以 guarantor 可以憑雜湊向任何對等節點取得該 blob，並對照當前的最佳頭部執行它——這也是為什麼一個 authorizer 要等到有人發布了它的 preimage 之後才變得可用"
  ],
  "stem": "The pool α[c] stores nothing but 32-byte authorizer hashes. So where does a guarantor obtain the executable is-authorized code, and as of which point in history is it resolved — and why there?",
        "options": [
            "From the preimage store of the separate auth-code host service named by the work-package, resolved by a historical lookup at the package's lookup-anchor timeslot, so that an auditor re-running the check much later resolves byte-identical code even if that service has since replaced or forgotten the preimage",
            "From the account of the first work-item's service, read at the anchor block's posterior state, since the anchor is what already pins the refinement context to a recent state root every validator has agreed on — eq. 11.36 has matched that root against β†, so no separate retention rule is needed to keep the code resolvable",
            "From the work-package itself: the code blob travels in the bundle beside the token and the configuration blob, which is exactly what the 64,000-octet limit bounds, so a guarantor needs no preimage lookup at all and the hash pooled in α[c] is simply the Blake2b of that code section",
            "From the pool entry: the hash in α[c] is the preimage hash of the code concatenated with its configuration, so a guarantor fetches that blob by hash from any peer and runs it against the current best head, which is why an authorizer only becomes usable once someone has published its preimage",
        ],
        "answer": 0,
        "optNotes": [
            "Λ(δ[p_h], (p_c)_t, p_u)：由 package 自己宣告的 auth code host service 於 lookup anchor 時點解析。",
            "anchor 最多只有 8 個區塊深，而 audit 可能兩個 epoch 之後才發生，重跑會拿到不同的 code。",
            "eq. 14.2 的 package 只帶 p_h、p_u、p_f；W_A = 64,000 是解析出來的 code 上限，不是 bundle 欄位。",
            "α[c] 存的是 H(p_u ⌢ p_f)，本身不是任何 blob 的 preimage key；綁 best head 正是 Λ 要避免的漂移。",
        ],
        "explanation": "eq. 14.11：p_a ≡ H(p_u ⌢ p_f)（authorizer = auth code hash 與 config blob 串接後的 Blake2b，0.8.0 PR #522 把 ch.8 與 ch.14 的說法對齊），而 E(var(metadata), auth code) ≡ Λ(δ[p_h], (p_c)_t, p_u)，其中 p_u 是 auth code hash、p_h 是 auth code host service。三個重點：(1) 供應 code 的是 work-package 自己宣告的 auth code host service p_h，那是 eq. 14.2 裡與 work-item 的 service 分開的獨立欄位 —— 這正是「授權」與「工作」分離的具體長相：買 coretime 的人挑 authorizer，真正做事的是別的 service；(2) 時間點是 lookup anchor 的 timeslot (p_c)_t，因為 Λ 的設計目標是「在可能被 audit 的整段期間答案不變」，GP 用 D = L + 4,800 = 19,200 slots 的 expunge period 保證這件事；(3) α[c] 只有 32 bytes 的 hash，既沒有 config 也沒有 code，光靠它取不到程式。W_A = 64,000 是「解析出來的」is-authorized code 的大小上限（eq. B.1 的 BIG 條件）；bundle 自己的上限是 W_B ≈ 13.8 MB。",
        "trap": "anchor 與 lookup anchor 是兩個不同的區塊：anchor 管 state/beefy/timeslot 比對，lookup anchor 管所有 preimage 的解析時點。",
    },
    {
        "id": "c3-ch08-unauthorized-report-outcome",
        "ch": "8",
        "section": "8.2 Pool and Queue",
        "gpRef": "eq. 11.32 & eq. 8.2",
        "difficulty": 3,
        "kind": "code",
        "tags": ["authorization", "guarantees", "prior-posterior"],
  "stemZh": "這段 0.7.2 的程式碼實作的是 eq. 11.32 中 authorizer 的那一半。它有義務讀取哪一個 pool？而當成員測試失敗時，協定層級的後果是什麼？",
  "optionsZh": [
   "prior 的 pool，因為 posterior 那個要等 accumulation 之後才會從 posterior 佇列形成；而失敗只是一個普通的區塊有效性失敗——該 guarantee 不可能成為有效區塊的一部分，所以根本沒有 report 可以拿來懲罰誰，disputes 狀態也不會被寫入任何東西",
   "posterior 的 pool，因為該 report 正被納入這一塊、而 eq. 8.2 的輪替是在處理 guarantee 之前套用的；失敗則使該區塊無效，這也是為什麼依賴圖把 α′ 列在 ρ′ 的輸入之中而不是反過來",
   "哪個 pool 都可以，因為輪替只移除該 report 自己消耗掉的那個 authorizer；失敗會把該 report 的 guarantor 記為 culprit 寫進 disputes 狀態，好讓下個 epoch 的懲罰集合沒收他們，而他們的 Ed25519 金鑰會經由這個 header 自己的 offenders marker 進入 ψ_O",
   "prior 的 pool，但該 report 仍然會以空的 authorizer trace 被收進 availability assignments，並在 accumulation 時被靜默丟棄——這也是為什麼缺席的 authorizer 對 guarantor 毫無代價，而 ρ‡ 會一直持有該條目直到 U = 5 個時槽的 assurance 逾時把它清掉"
  ],
  "stem": "This 0.7.2 code implements the authorizer half of eq. 11.32. Which pool is it obliged to read, and what is the protocol-level consequence when the membership test fails?",
        "code": {
            "lang": "go",
            "caption": "internal/extrinsic/guarantee_controller.go:172-186 (ValidateWorkReports; gas checks elided)",
            "src": """func (g *GuaranteeController) ValidateWorkReports() error {
	workReports := g.WorkReportSet()
	alpha := blockchain.GetInstance().GetPriorStates().GetAlpha()
	delta := blockchain.GetInstance().GetPriorStates().GetDelta()
	rhoDoubleDagger := blockchain.GetInstance().GetIntermediateStates().GetRhoDoubleDagger()
	for _, workReport := range workReports {
		if rhoDoubleDagger[workReport.CoreIndex] != nil {
			err := ReportsErrorCode.CoreEngaged
			return &err
		}
		authPool := alpha[workReport.CoreIndex]
		if !isAuthPoolContains(authPool, workReport.AuthorizerHash) {
			err := ReportsErrorCode.CoreUnauthorized
			return &err
		}
		// … per-service accumulate-gas checks elided …
	}
	return nil
}""",
        },
        "options": [
            "The prior pool, since the posterior one is only formed after accumulation out of the posterior queue; and the failure is an ordinary block-validity failure — the guarantee cannot be part of a valid block, so there is no report to punish anyone over and nothing is written to the disputes state",
            "The posterior pool, because the report is being included in this very block and eq. 8.2's rotation is applied before guarantees are processed; failure then invalidates the block, which is why the dependency graph lists α′ among the inputs of ρ′ rather than the other way round",
            "Either pool will do, because the rotation only removes the authorizer the report itself consumed; failure records the report's guarantors as culprits in the disputes state so that the next epoch's punishment set slashes them, their Ed25519 keys entering ψ_O through the offenders marker of this very header",
            "The prior pool, but the report is still admitted into the availability assignments with an empty authorizer trace and is silently discarded at accumulation time, which is why an absent authorizer costs a guarantor nothing and ρ‡ holds the entry until the U = 5 slot assurance timeout clears it",
        ],
        "answer": 0,
        "optNotes": [
            "eq. 11.32 寫的是 r_a ∈ α[r_c]——α 沒有 prime；不合法就整塊被拒，不會寫進 disputes。",
            "α′ 依賴 φ′、要等 accumulation 之後才存在；§4 的 ρ′ ≺ (E_G, ρ‡, κ, τ′) 根本不含 α′。",
            "每塊每個 core 都會 append 一項 φ′[c]↺[H_T]，兩個 pool 幾乎必然不同；ψ_O 也只能經 E_D 增長。",
            "eq. 11.46 只把通過全部檢查的 guarantee 填進 ρ′；ρ‡ 早在 guarantee 進來前就定案了。",
        ],
        "explanation": "eq. 11.32 寫的是 ∀r ∈ I : ρ‡[r_c] = ∅ ∧ r_a ∈ α[r_c] —— α 沒有 prime。順序上也只能如此：eq. 8.2 的 α′ 依賴 φ′，而 φ′ 是 accumulation 的產出，§8.2 明說 \"practically speaking, this step must be computed after accumulation\"，所以 guarantee 驗證的當下 α′ 根本還不存在。程式碼用 GetPriorStates().GetAlpha() 是對的，也因此本區塊 accumulation 才剛 assign 進 queue 的新 authorizer，最快要下一個區塊才可能被引用。至於後果：§11 的這些條件是「區塊有效性條件」，不滿足就整個區塊不合法，import 時直接拒（團隊實作回 CoreUnauthorized）。這是刻意的分工：culprit／fault 只處理需要離線資料（重跑 refine、拉 audit DA）才能判定的爭議，而 authorizer 在不在 pool 裡是任何節點光看鏈上狀態就能算出來的條件。順帶一提 ρ‡ 是 assurances 之後、guarantees 之前的中間態，這正是 core-engaged 檢查要用它而不是 ρ 的原因。",
        "trap": "「檢查用 prior α、更新用 posterior φ′」同一章兩個方向；面試常問「同一個區塊裡剛 assign 的 authorizer 能不能馬上用」——不能。",
    },
]
