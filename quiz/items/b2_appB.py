# -*- coding: utf-8 -*-
# Appendix B (batch 2) — host-call register conventions, inner PVM, 0.8.0 deltas, fuzzer-found bugs (GP 0.8.0)
ITEMS = [
{
 "id": "b2-appB-write-prev-length-full",
 "ch": "B", "section": "B.5 General Functions — write", "gpRef": "§B.5 `write` = 5 (Ω_W); eq. B.12 (G); eq. 9.8 (a_t)",
 "difficulty": 2, "kind": "code", "tags": ["host-calls", "write", "storage", "fuzz-bug"],
 "stem": "The excerpt is the team's Ω_W (`write`) after fix #980. A service overwrites a key that currently holds a 100-octet value with a 5,000-octet value (φ_7…φ_10 = k_O, k_Z, v_O, v_Z). Which statement matches GP 0.8.0?",
 "code": {"lang": "go", "caption": "PVM/host_call_general.go (write, after PR #980)", "src": """	value, storageRawKeyExists := a.StorageDict[string(storageRawKey)]
	// ...
	if storageRawKeyExists {
		footprintItems, footprintOctets = service_account.CalcStorageItemfootprint(string(storageRawKey), value)
		l = uint64(len(value))
	} else { // ... (elided: key only present in the not-yet-decoded state key-vals)
		l = NONE
	}
	// ...
	if vz == 0 { // remove storage
		delete(a.StorageDict, string(storageRawKey))
	} else if input.VM.Mem.IsReadable(vo, vz) { // storage append/update
		storageRawData := input.VM.Mem.Read(vo, vz)
		// ...
		newMinBalance := service_account.CalcThresholdBalance(newItems, newOctets, a.ServiceInfo.DepositOffset) // a_t
		if newMinBalance > a.ServiceInfo.Balance {
			input.VM.Registers[7] = FULL
			return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
		}
		// balance check passed, now apply the storage mutation
		a.StorageDict[string(storageRawKey)] = storageRawData
		// ...
	} else {
		return OmegaOutput{ExitReason: ExitPanic, Addition: input.Addition}
	}
	// ...
	input.VM.Registers[7] = l"""},
 "options": [
  "On success φ′_7 = 5000, the length of the value just written; if a_t > a_b the value is still stored, φ′_7 = FULL and the shortfall is debited from the balance at the service's next accumulation — so all the fix had to change was the register value, not the order of the map mutation",
  "If the post-write a_t ≤ a_b the value is stored and φ′_7 = 100, the length of the value being replaced; if a_t > a_b, φ′_7 = FULL and the account is handed back unchanged (s′ = s) — the pre-fix code had already mutated the shared Go map, so the FULL write leaked (#979)",
  "On success φ′_7 = OK (0); a_t > a_b cannot occur for an overwrite because the storage deposit (B_I per item, B_L per octet) is charged only when a key is first created, never when its value changes size, so Ω_W needs no threshold check on this path",
  "If a_t > a_b the host call exits ☇ (panic) so that the whole accumulation collapses to the checkpointed context y; otherwise φ′_7 = 100, the length of the value being replaced, and the value is stored — the collapse is exactly what made the pre-fix map mutation harmless"
 ],
 "answer": 1,
 "optNotes": [
   "回傳的是被取代的舊值長度而不是新長度；GP 的 FULL 分支回的是原封不動的 s，沒有欠款概念。",
   "成功回舊值長度 100（key 原本不存在才回 NONE），FULL 時 s′ = s——所以必須先算門檻再改 map。",
   "a_t 隨 a_o 變動（每筆 storage 計 34 + |k| + |v|），改變 value 大小就會拉高門檻。",
   "☇ 只保留給記憶體錯誤；餘額不足是可續行的 FULL，context 不會被丟棄，污染會一路寫進 δ′。",
 ],
 "explanation": "Ω_W（write = 5）定義：[k_O, k_Z, v_O, v_Z] = φ_7…φ_10；k = μ[k_O..+k_Z]（不可讀 → error）；a = s 但 a_storage[k] = μ[v_O..+v_Z]（v_Z = 0 時改為刪除 k；value 範圍不可讀 → error）；l = |s_storage[k]| 若 k ∈ keys(s_storage)，否則 NONE；(ε′, φ′_7, s′) = (☇, φ_7, s) 當 k = error ∨ a = error；(▸, FULL, s) 當 a_minbalance > a_balance；(▸, l, a) 否則。所以成功時回傳的是「被取代的舊值長度」，FULL 時 s′ = s 一字不改。a_t（eq. 9.8）= max(0, B_S + B_I·a_i + B_L·a_o − a_f)，而 a_o 含每筆 storage 的 34 + |k| + |v|，所以把 100 octets 換成 5,000 octets 會拉高 a_t。你們的 bug #979（fuzz seed 3785638964 step 15419）：write 先改了 StorageDict 再檢查門檻，Go map 淺複製共用底層 map，FULL 的寫入仍被持久化 → state root mismatch；PR #980 改成先算 newMinBalance 再改 map（即上面的順序）。另外 accumulate 中 write 經 G（eq. B.12）包裝：x*_self = 回傳的 s′，所以同一次 accumulate 之後的 read/info 看得到新值。",
 "trap": "write 回傳「舊長度或 NONE」，不回傳 OK；v_Z = 0 是刪除；FULL 時必須零副作用。"
},
{
 "id": "b2-appB-read-cross-service-pure",
 "ch": "B", "section": "B.5 General Functions — read", "gpRef": "§B.5 `read` = 4 (Ω_R); eq. B.11–B.12 (F, G)",
 "difficulty": 3, "kind": "code", "tags": ["host-calls", "read", "storage", "fuzz-bug", "accumulation"],
 "stem": "Excerpt from the team's Ω_R (`read`) after fix #938, which added the `callerServiceID == serviceID` guard (s* = φ_7, or the caller when φ_7 = 2^64−1). Accumulating service A reads a storage key of service B, which is not accumulating in this block. Which statement is correct?",
 "code": {"lang": "go", "caption": "PVM/host_call_general.go (read, after PR #938)", "src": """	var a types.ServiceAccount
	callerServiceID := serviceID
	if sStar == uint64(serviceID) {
		a = delta[serviceID]
	} else if value, exists := delta[types.ServiceID(sStar)]; exists {
		a = value
		serviceID = types.ServiceID(sStar)
	} else {
		input.VM.Registers[7] = NONE
		return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
	}
	storageRawKey := input.VM.Mem.Read(ko, kz)
	v, exists := a.StorageDict[string(storageRawKey)]
	storageValueFromKeyVal := getStorageFromKeyVal(input.Addition.GeneralArgs.StorageKeyVal, serviceID, storageRawKey)
	if !exists {
		if storageValueFromKeyVal == nil { // check storage state key-val
			input.VM.Registers[7] = NONE
			return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
		} else {
			v = *storageValueFromKeyVal
			// ...
			if callerServiceID == serviceID {
				a.StorageDict[string(storageRawKey)] = v
				input.Addition.AccumulateArgs.ResultContextX.PartialState.ServiceAccounts[serviceID] = a
				removeStorageFromKeyVal(input.Addition.GeneralArgs.StorageKeyVal, serviceID, storageRawKey)
			}
		}
	}"""},
 "options": [
  "Ω_R(ϱ, ω, μ, s, s, d) may look up any account in d but hands back only the caller's account s (mirrored into x by G); a read of B is a pure lookup that must leave B untouched — before the guard, B's key-val was evicted from the unmatched pool, B's entry vanished from the merged δ′ and the state root diverged",
  "Reading another service's storage is not permitted by Ω_R: for s* ≠ s the call must return WHO without touching memory or the key-val pool, so in a compliant implementation the branch that reaches B's account is unreachable and the guard is merely defensive — cross-service inspection is what `info` and `historical_lookup` are for",
  "The read must observe the posterior state being built in this block — including writes by services accumulated earlier in the same round — so the cached value has to be refreshed from the accumulation context on every read rather than removed from the pool, and the guard is itself a bug because it suppresses that refresh for every s* ≠ s",
  "The read must be served from the lookup-anchor snapshot exactly as `historical_lookup` does, so mutating the current-state cache is only a performance concern and can never change δ′; the guard merely avoids decoding B's key-vals twice, and the state-root divergence came from the merge rule alone"
 ],
 "answer": 0,
 "optNotes": [
   "跨 service 讀取在 GP 裡是純函數：G 只把呼叫者自己的帳戶寫回 x_self，B 不可能被改動。",
   "d（partial state 的 accounts）正是為了讓 s* ≠ s 能查而傳進來的，而且查不到時回的是 NONE。",
   "d 是 Ψ_A 拿到的 partial state 快照，同一輪其他 service 的寫入本來就看不到，refresh 也救不了。",
   "historical_lookup 只存在於 refine；且因果顛倒——交集式 merge 是既定設計，缺陷在純函數留下副作用。",
 ],
 "explanation": "Ω_R（read = 4）：s* = s 若 φ_7 = 2^64−1，否則 φ_7；a = s（呼叫者自己，含本次已 write 的內容）若 s* = s；d[s*] 若 s* ∈ keys(d)；否則 none。[k_O, k_Z, o] = φ_8…φ_10、v_Z = φ_12、f = min(φ_11, |v|)、l = min(v_Z, |v| − f)；v = error（key 範圍不可讀）→ ☇；a = none 或 k ∉ keys(a_storage) → NONE（不是 WHO——WHO 是 transfer/eject/provide 等找不到 service 時用的）；否則寫 v[f..f+l] 到 μ[o..+l] 並回傳 |v|。read 的 mutation 只有 (ε′, φ′_7, μ′)，s′ = s；在 accumulate 的 F（eq. B.11）中 read 被 G 包起來，G 只把「呼叫者自己的帳戶」寫回 x_self（eq. B.12），所以跨 service 的讀取在 GP 裡是純函數，不可能改動 B。d 是 (x_u)_d，即 Ψ_A 拿到的 partial state 快照（Δ1 對同一輪的每個 service 傳同一份 e，§12 平行累加），因此同一輪其他 service 的寫入本來就看不到。你們的 #938（bug id 1776702160_6218）：A 讀 B 的 key 時，把 B 的 entry 從 UnmatchedKeyVals cache 移除當成最佳化，但 B 這個 block 沒有 accumulate，其本地帳戶副本從未寫回 d′，而 #880 的 merge 採交集語意（任何輸出缺少的 key 視為被刪除）→ B 的 storage 全局消失、state root mismatch；修法就是只在 callerServiceID == serviceID 時才快取並移除。",
 "trap": "read/lookup/info 找不到回 NONE（2^64−1）；跨 service 讀取是唯讀快照，只有自己的帳戶會經 G 寫回 x。"
},
{
 "id": "b2-appB-unknown-hostcall-oog",
 "ch": "B", "section": "B.2/B.3/B.4 — context mutator F, default case", "gpRef": "eq. B.2, B.6, B.11 (default case); eq. B.13 (C); M_∅ in App. I",
 "difficulty": 2, "kind": "code", "tags": ["host-calls", "gas", "fuzz-bug", "delta-0.8.0"],
 "stem": "During accumulation a service executes `ecalli 9` (`machine`, a refine-only call) with ϱ = 300 gas remaining. The team's dispatcher routes ids that are not in the invocation's table to hostCallException (below, after PR #992). What does GP 0.8.0 prescribe for this situation?",
 "code": {"lang": "go", "caption": "PVM/host_call_general.go (hostCallException / chargeGasAndCheck, after PR #992)", "src": """func hostCallException(input OmegaInput) (output OmegaOutput) {
	if result := chargeGasAndCheck(&input); result != nil {
		return *result
	}
	input.VM.Registers[7] = WHAT
	return OmegaOutput{
		ExitReason: ExitContinue,
		Addition:   input.Addition,
	}
}

func chargeGasAndCheck(input *OmegaInput) *OmegaOutput {
	*input.VM.Gas -= 10
	if *input.VM.Gas < 0 {
		return &OmegaOutput{
			ExitReason: ExitOOG,
			Addition:   input.Addition,
		}
	}
	return nil
}"""},
 "options": [
  "φ′_7 = WHAT and execution continues at the next instruction regardless of the remaining gas — nothing was executed, so an unknown or unavailable host call can never by itself trigger out-of-gas (the pre-#992 behaviour)",
  "The machine panics (☇) with no gas charged: a host-call id outside the invocation's table is treated like an invalid instruction, and the accumulation collapses to the checkpointed context y",
  "The default branch of F charges M_∅ = 1000 first: ϱ′ = 300 − 1000 < 0, so the invocation exits ∞ and Ψ_A collapses to the checkpointed context y; under the 0.7.2 flat charge of 10 the same call would have continued with φ′_7 = WHAT",
  "The `ecalli` surfaces to the caller of Ψ_A as the exit h̄ × 9: the accumulation is aborted, treated as a host-call fault, and the service's result for this block is recorded as BAD"
 ],
 "answer": 2,
 "optNotes": [
   "F 的 default 是「先扣 M_∅ 再回 WHAT」，扣費本身就可能把 ϱ′ 壓到負值而 ∞。",
   "ecalli 對任何立即數都是合法指令，未知 id 只是走 default 分支，不是無效指令。",
   "0.8.0 的 M_∅ = 1000 > 300，ϱ′ < 0 使 invocation ∞，collapse 因而取 checkpoint 過的 y。",
   "§A.6 的 Ψ_H 把每個 host id 都交給 F 處理，最上層永遠看不到 h̄；BAD 也不在 Ψ_A 的值域裡。",
 ],
 "explanation": "三個 invocation 的 mutator F（eq. B.2、B.6、B.11）最後兩行完全相同：ω′ = ω 但 φ′_7 = WHAT，ϱ′ = ϱ − M_∅；若 ϱ′ < 0 → (∞, ϱ′, ω′, μ)，否則 (▸, ϱ′, ω′, μ)。M_∅（Gas cost charged for an unknown host-call）在 0.8.0 是 1000（0.7.2 是 10，你們 chargeGasAndCheck 裡的 10 就是 0.7.2 值）。所以 ϱ = 300 時：300 − 1000 = −700 < 0 → ∞；Ψ_M 的 u = ϱ − max(ϱ′, 0) = 300（全部耗盡）；collapse C（eq. B.13）在 o ∈ {∞, ☇} 時採用 exceptional context Y（最後一次 checkpoint 的狀態，沒 checkpoint 就是初始 I(s, s)）。只有 refine 用 invoke 驅動的 inner machine 才會把 ecalli 以 (HOST, h) 回報給外層。你們的 #993：hostCallException 扣 10 gas 後沒檢查 gas 是否為負（fuzzer session 8f50823b… step 175662，service 0x6707fa2e 在 accumulate 呼叫了無效 host function）；參考實作 polkajam 停機（∞）、你們繼續執行 → θ（LastAccOut）、β（BEEFY root）與 state root 分歧；PR #992 補上 chargeGasAndCheck 的 OOG 檢查（GP 0.7.2 gavofyork/graypaper#482「explicit OOG check for each invocation mutator default case」）。升 0.8.0 時要把 10 換成 M_∅ = 1000（連同其他 host call 的 base + per-KiB 費用，見 App. I）。",
 "trap": "未知 host call「先扣費再回 WHAT」，扣費本身就能觸發 ∞；0.8.0 的 M_∅ = 1000 不是 10。"
},
{
 "id": "b2-appB-invoke-gas-refund",
 "ch": "B", "section": "B.6 Refine Functions — invoke", "gpRef": "§B.6 `invoke` = 13 (Ω_K); eq. B.4 (inner PVM tuple); §B.1 inner result codes",
 "difficulty": 3, "kind": "code", "tags": ["host-calls", "refine", "inner-pvm", "gas", "delta-0.8.0"],
 "stem": "The excerpt is the team's 0.7.2 `invoke` (Ω_K): it reads a 112-octet block at φ_8, runs inner machine n = φ_7 and writes the block back. Apart from the id shift (12 → 13), which GP 0.8.0 rule is missing from it?",
 "code": {"lang": "go", "caption": "PVM/host_call_refine.go (invoke, 0.7.2 numbering)", "src": """	n, o := input.VM.Registers[7], input.VM.Registers[8]

	offset := uint64(112)
	// g = panic
	if !input.VM.Mem.IsWriteable(o, offset) {
		input.VM.Registers[7] = OOB
		return OmegaOutput{ExitReason: ExitPanic, Addition: input.Addition}
	}
	// ... (WHO if n is not a known machine; decode g and w[0..13] from the 112 octets)
	// wrap m[n]_p (program), w (registers), m[n]_u (memory), g (gas)
	tempInterp := NewInterpreter(&tmpProgram, w, &tempMemory, Gas(g))
	// ...
	c, pcPrime = tempInterp.SingleStepInvoke(input.Addition.IntegratedPVMMap[n].PC)
	// ... (re-encode gas' and registers')
	// write data into memory (mu)
	input.VM.Mem.Write(o, data)

	// m* = m
	tmp := input.Addition.IntegratedPVMMap[n]
	tmp.Memory = *tempInterp.Memory
	if c.GetReasonType() == HOST_CALL {
		tmp.PC = pcPrime + 1 + ProgramCounter(skip(int(pcPrime), input.Addition.Program.Bitmasks))
	} else {
		tmp.PC = pcPrime
	}
	input.Addition.IntegratedPVMMap[n] = tmp"""},
 "options": [
  "Nested host calls: an `ecalli` executed by the inner machine must be dispatched through the refine mutator F (historical_lookup, export, …) instead of stopping the inner run, so Ω_K has to invoke Ψ_H rather than Ψ and the outer service should never see the HOST result code at all",
  "Resumption: on a HOST exit the saved instruction counter must stay on the `ecalli` itself, so that the outer service can re-execute that instruction after servicing the call, exactly as Ψ does for a page fault; advancing it by i′ + skip(i′) + 1 drops an instruction",
  "Memory: the 112-octet block need only be readable, because in 0.8.0 the inner gas and the 13 registers are handed back through φ′_7…φ′_12 rather than written back into the block, so a readable-but-unwritable window is fine and the excerpt's OOB-and-panic path should be a plain WHO instead",
  "Gas: the outer machine pays g = M_K + g_R up front (∞ if ϱ < g; g_R is the inner gas read from the block) and afterwards gets the inner's unspent g_R′ back, ϱ′ = ϱ − g + g_R′; the inner machine also carries a gas-charged flag for its current basic block"
 ],
 "answer": 3,
 "optNotes": [
   "inner PVM 刻意沒有 host call 能力，Ω_K 明寫呼叫 Ψ，ecalli 一律以 (HOST, h) 停機交外層處理。",
   "m*[n]_i = i′ + skip(i′) + 1 正是要跳過那條 ecalli；停在原地會讓 resume 後無限重複同一個 ecalli。",
   "GP 要求 N_{o..+112} ⊆ writable(μ)，因為 g_R′ 與 w′ 要原地寫回同一塊，不可寫就 ⟨0, error⟩ → ☇。",
   "0.7.2 只扣 10 且 inner gas 完全獨立；0.8.0 要外層預付 M_K + g_R 並退還未用完的 g_R′。",
 ],
 "explanation": "Ω_K（invoke = 13）：[n, o] = φ_7,8；⟨g_R, w⟩ 滿足 E_8(g_R) ⌢ E_8(w) = μ[o..+112]（8 octets gas + 13 個 8-octet 暫存器），且 N_{o..+112} 必須 ⊆ writable(μ)，否則 ⟨0, error⟩ → ☇（因為結果要寫回同一塊）；(c, i′, g_R′, f′, w′, u′) = Ψ(m[n]_p, m[n]_i, g_R, m[n]_f, w, m[n]_u)——是 Ψ 不是 Ψ_H，inner 沒有 host call，遇到 ecalli 就以 c = h̄ × h 停下；μ* 寫回 E_8(g_R′) ⌢ E_8(w′)；m*[n]_i = i′ + skip(i′) + 1 當 c ∈ {h̄} × N_R（跳過那條 ecalli，讓外層 service 代為服務後 resume），否則 i′；m*[n]_f = f′（eq. B.4 的 inner PVM tuple ⟨p, u, i, f⟩，f 是「本 basic block 的 gas 已扣」旗標，因為 0.8.0 gas 以 basic block 為單位預扣，mid-block resume 時不能再扣一次——#1046 review 也提到 A.4 的 L(i)）。gas：g = M_K + g_R（M_K = 968）；ϱ′ = ϱ − g 當 w = error ∨ n ∉ keys(m) ∨ ϱ < g，否則 ϱ − g + g_R′——也就是外層先付全部 inner gas，剩下的退回；ϱ < g 依 B.18/B.19 直接 ∞。回傳：(HOST, h)、(FAULT, x 位址)、OOG、PANIC、HALT 進 φ′_7/φ′_8（非 HOST/FAULT 時 φ′_8 不變）；n 不存在 → WHO。你們的 0.7.2 版本只扣 10 gas，inner 的 g 完全獨立、也不退還——這正是 #1046 的「invoke gas refund」項目；同一 PR 也加了 machine 的 63 台上限（GP PR #521，|m| ≥ 63 → FULL，且排在 ☇ 之前）。另外值得複查：excerpt 的 skip 用的是 input.Addition.Program.Bitmasks（外層程式的 bitmask），GP 的 skip(i′) 應以 inner 程式 m[n]_p 的 bitmask 計算。",
 "trap": "invoke 的 112 octets 必須「可寫」；inner 無 host call（ecalli → HOST）；0.8.0 外層預付 g_R 並退還 g_R′。"
},
{
 "id": "b2-appB-pages-access-modes",
 "ch": "B", "section": "B.6 Refine Functions — pages", "gpRef": "§B.6 `pages` = 12 (Ω_Z); App. I M_Z,* gas constants",
 "difficulty": 3, "kind": "code", "tags": ["host-calls", "refine", "inner-pvm", "memory"],
 "stem": "The excerpt is the team's `pages` (Ω_Z) acting on inner machine n over page range [p, p+c) with mode r (φ_7…φ_10 = n, p, c, r). Compared with GP 0.8.0, which statement is correct?",
 "code": {"lang": "go", "caption": "PVM/host_call_refine.go (pages, 0.7.2 numbering)", "src": """	if r > 4 || p < 16 || p+c >= (1<<32)/ZP {
		input.VM.Registers[7] = HUH
		return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
	}
	if r > 2 && !isReadable(p, c, input.Addition.IntegratedPVMMap[n].Memory) {
		input.VM.Registers[7] = HUH
		return OmegaOutput{ExitReason: ExitContinue, Addition: input.Addition}
	}
	// otherwise : ok
	// u_v
	if r >= 3 {
		for i := uint32(p); i < uint32(p+c); i++ {
			input.Addition.IntegratedPVMMap[n].Memory.Pages[i] = &Page{
				Value:  make([]byte, ZP),
				Access: MemoryInaccessible,
			}
		}
	}
	// u_a
	if r == 1 || r == 3 {
		for i := uint32(p); i < uint32(p+c); i++ {
			input.Addition.IntegratedPVMMap[n].Memory.Pages[i] = &Page{
				Value:  make([]byte, ZP),
				Access: MemoryReadOnly,
			}
		}
	}
	// ... (r == 2 || r == 4: same loop with Access: MemoryReadWrite)
	input.VM.Registers[7] = OK"""},
 "options": [
  "The code is correct: Ω_Z zero-fills the range for every r ∈ 0…4 and only the resulting access differs (0 → inaccessible, 1/3 → R, 2/4 → W); the GP never distinguishes an allocation from a mode change, which is why App. I prices every r with one base cost and one per-page rate",
  "Two semantic gaps: for r = 0 the GP zero-fills the range and makes it inaccessible (the code leaves it untouched), and for r ∈ {3, 4} the GP keeps the page contents and only changes the access mode to R or W (the code re-allocates zeroed pages instead)",
  "The only gap is the error code: when r > 2 and a page of the range is inaccessible the GP returns OOB (inner-PVM memory index not accessible) exactly as `peek` and `poke` do, rather than HUH; the page mutations themselves are right, and r = 0 rightly leaves the octets alone",
  "The GP validates r ∈ 0…4, p ≥ 16 and p + c < 2^32/Z_P before looking up n, so an invalid request aimed at a non-existent machine must yield HUH where the code yields WHO; the page mutations themselves are right, and an invalid r is free, no gas constant being defined for it"
 ],
 "answer": 1,
 "optNotes": [
   "u′_value 只在 r < 3 時被清成 0；附錄 I 也給了 free/alloc/setmode 三組不同費率而非一組。",
   "r = 0 是「歸零 + 設為不可存取」，r ∈ {3, 4} 保留內容只改權限——實作恰好兩邊都做反了。",
   "Ω_Z 的結果只有 WHO/HUH/OK，OOB 專屬於 peek/poke 對 inner memory 的位元組範圍存取。",
   "u = error（n ∉ keys(m)）是第一個 case 且回 WHO；無效 r 也不免費，M_Z,i = 80。",
 ],
 "explanation": "Ω_Z（pages = 12）：[n, p, c, r] = φ_7…φ_10；u = m[n]_u（n ∉ keys(m) → error）；u′ = u 但 value[p·Z_P..+c·Z_P] = [0, 0, …] 當 r < 3、否則保留原值；access[p..+c] = [∅…] 當 r = 0、[R…] 當 r ∈ {1, 3}、[W…] 當 r ∈ {2, 4}；(φ′_7, m′) = (WHO, m) 當 u = error；(HUH, m) 當 r > 4 ∨ p < 16 ∨ p + c ≥ 2^32/Z_P（= 2^20 頁；p < 16 保護最低的 64 KiB）；(HUH, m) 當 r > 2 ∧ access[p..+c] ∋ ∅（改權限只能對已配置的頁）；(OK, m′) 否則。語意上 r = 0 是「釋放」（歸零 + 不可存取）、1/2 是「配置」（歸零 + R/W）、3/4 是「改權限」（內容保留）；把內容留著等於把舊資料留在一個之後可能被重新配置的頁裡。0.8.0 的 gas 也依此分類：free M_Z,f,c + c·M_Z,f,p = 212 + 118/頁、alloc 275 + 121/頁、setmode 130 + 29/頁、無效 r 固定 M_Z,i = 80——三組常數正是因為三種操作成本不同。對照你們的程式：r = 0 什麼都沒做（GP 要歸零並設為不可存取）；r ≥ 3 先配置歸零頁再設 R/W（GP 要保留內容）——code-map 3.12.9 也標出這個分歧；而 WHO 先於 HUH 的順序與 GP 一致。額外注意：r > 2 的檢查把「頁索引 p、頁數 c」丟給 isReadable(start, offset, m)，而該函式（argument_invocation.go）以位元組位址計算 startPage = start / Z_P，所以檢查的是錯的頁——這條路徑沒有 conformance vectors 覆蓋，遷移 0.8.0 時值得補測。",
 "trap": "pages 的 r：0 釋放、1/2 配置（歸零）、3/4 只改權限（保留內容）；錯誤碼是 WHO/HUH，沒有 OOB、沒有 panic。"
},
{
 "id": "b2-appB-eject-conditions",
 "ch": "B", "section": "B.7 Accumulate Functions — eject", "gpRef": "§B.7 `eject` = 22 (Ω_J); eq. 9.8 (a_i, a_o); eq. B.3 (D)",
 "difficulty": 3, "kind": "concept", "tags": ["host-calls", "eject", "preimages", "accounts"],
 "stem": "Service 7 (accumulating) calls `eject` (index 22) with φ_7 = 9 and φ_8 = o, where μ[o..+32] = h. Under GP 0.8.0, when does the call return OK, and what happens then?",
 "options": [
  "Service 9 exists, is not the caller, and its code hash equals the code hash of service 7 with its parent field a_p = 7; its footprint is exactly a_i = 2 with l = max(81, a_o) − 81 (one request (h, l), no storage); a_l[(h, l)] = [x, y] with y < t − D; then 9 is deleted and its balance is burned",
  "Service 9 exists, is not the caller, and its code hash equals E_32(7); its footprint is exactly a_i = 2 with l = max(81, a_o) − 81 (one request (h, l), no storage); a_l[(h, l)] = [x, y] with y < t − D; then 9 is deleted and its entire balance is added to service 7",
  "Service 9 exists, is not the caller, and its code hash equals E_32(7); its footprint is exactly a_i = 2 with l = max(81, a_o) − 81 (one request (h, l), no storage); a_l[(h, l)] = [], still unprovided; then 9 is deleted and its entire balance is credited to the registrar χ_R",
  "Service 9 exists, is not the caller, and its code hash equals E_32(7); its footprint is exactly a_i = 2 with l = max(81, a_o) − 81 (one request (h, l), no storage); a_l[(h, l)] = [x, y, w] with w < t − D; then 9 is deleted and its entire balance is added to service 7"
 ],
 "answer": 1,
 "optNotes": [
   "Ω_J 比對的是 d_c = E_32(呼叫者索引)；兩個 service 共用同一份 code 是正常狀態，a_p 也從未被讀。",
   "code hash = E_32(呼叫者) 是自我停用標記，狀態須為 [x, y] 且 y < t − D，餘額歸呼叫者。",
   "[] 表示「已請求、從未提供」，不保證沒有 refine 還需要它；χ_R 也與 eject 的資金流向無關。",
   "三元素狀態只有 forget 會處理，Ω_J 的 OK 分支只匹配長度為 2 的 [x, y]，且過期看的是中間的 y。",
 ],
 "explanation": "Ω_J（eject = 22，g = M_J = 458）：[d, o] = φ_7,8；h = μ[o..+32]（不可讀 → ☇）；d = accounts[d] 只在 d ≠ x_id ∧ d ∈ keys(accounts) 時成立，否則 error → WHO；d_c ≠ E_32(x_id) → WHO；l = max(81, d_o) − 81；d_i ≠ 2 ∨ (h, l) ∉ keys(d_l) → HUH；d_l[(h, l)] = [x, y] ∧ y < t − D → OK：accounts \\ {d} ∪ {x_id ↦ s′}，s′_b = x_self_b + d_b；其他情況（[]、[x]、[x, y, w]、或 y 尚未過期）→ HUH。81 從哪來：eq. 9.8 定義 a_i = 2·|a_l| + |a_s|、a_o = Σ_{(h,z)∈a_l}(81 + z) + Σ_{a_s}(34 + |k| + |v|)；「恰一個 request、沒有 storage」等價於 a_i = 2 且 a_o = 81 + z，因此 l = a_o − 81 就把那個唯一 request 的長度 z 還原出來（通常是被 eject 的 service 自己舊 code 的 preimage）。設計意圖：一個 service 把自己的 code hash 設成 E_32(某個 service 索引)（不可能是合法 code 的值，等於自我停用）就等於指名「由那個 service 回收我」；等最後一個 preimage 已 forget 且過了 D = L + 4,800 = 19,200 slots（eq. B.3，確保 refine 的 historical lookup 不再需要它），parent 才能回收餘額並刪帳戶。你們的 eject()（host_call_accumulate.go）：SerializeFixedLength(callerID, 32)、max(81, Bytes) − 81、Items != 2、lookupDataLength == 2 && lookupData[1] < timeslot − D，與 GP 相符。",
 "trap": "eject 的三把鎖：code hash = E_32(呼叫者)、a_i = 2（唯一 request）、該 request 狀態 [x, y] 且 y < t − D；餘額歸呼叫者。"
},
{
 "id": "b2-appB-log-jip1",
 "ch": "B", "section": "B.2–B.4 mutator default case & JIP-1 `log`", "gpRef": "eq. B.2, B.6, B.11 (default branch); JIP-1 (host call 100)",
 "difficulty": 2, "kind": "concept", "tags": ["host-calls", "jip", "log", "fuzz-bug"],
 "stem": "A service executes `ecalli 100` (`log`). Which statement is correct?",
 "options": [
  "`log` is host call 100 of GP App. B, available in all three invocations: it returns OK, costs M_∅ = 1000 and, like every other host call that reads memory, panics (☇) when the message range is not readable — omitting that check merely turns a specified panic into a crash",
  "`log` is consensus-critical: the formatted message is hashed into the service's accumulation output θ and hence into the BEEFY root β_B, so every node must implement byte-identical level/target/message formatting, and an unreadable range must panic (☇)",
  "`log` is specified by JIP-1, not by the Gray Paper: its observable effects match an unimplemented index — φ′_7 = WHAT and the gas of a bad-index call — and an unreadable message/target range must have no side-effects (no panic); the node merely prints the message",
  "`log` exists only in Ψ_R as a guarantor diagnostic, where it returns OK and charges M_∅; during accumulate and is-authorized `ecalli 100` instead falls through to the mutator's WHAT default, so the same program sees OK in one invocation and WHAT in another"
 ],
 "answer": 2,
 "optNotes": [
   "JIP-1 明寫「No side-effects if memory access is invalid」，☇ 會讓實作與未實作的節點分岔。",
   "yield（26）才是唯一把 32-octet hash 送進 x_y → θ′ → BEEFY 的管道，log 不改任何 context 欄位。",
   "JIP-1 刻意讓 log 對共識透明：回傳值與 gas 都與「未實作的壞 index」完全一致。",
   "三張表都註冊了 [100]；JIP-1 的重點正是不論實作與否、不論哪個 invocation 都看到同樣結果。",
 ],
 "explanation": "GP 附錄 B 沒有 index 100；純 GP 節點對 ecalli 100 走 F 的 default（eq. B.2/B.6/B.11）：扣 M_∅、φ′_7 = WHAT、繼續（gas 不足則 ∞）。JIP-1「Debug message host call」原文：Index 100、Name log、Gas usage 10「(same as host-call with bad index)」；輸入 φ_7 = level（0 fatal … 4 pedantic）、target = ∅ 若 φ_8 = 0 ∧ φ_9 = 0 否則 μ[φ_8..+φ_9]、message = μ[φ_10..+φ_11]；輸出 φ′_7 = WHAT——「WHAT is always returned so that authorizer/service behaviour is the same whether or not this JIP is implemented」；「No side-effects if memory access is invalid」。換言之 log 對共識刻意「透明」：不進 θ/β、不改狀態、不 panic，回傳值與 gas 都與未實作時一致（注意 JIP 的「10」是 0.7.x 時代的 bad-index 費用；0.8.0 的 M_∅ = 1000，實作時要跟目前 GP 版本對齊，否則 gas 統計會分歧）。它不是 refine 專屬：你們 host_call_invocation.go 的三張表都註冊了 [100] = logHostCall。你們的 #975（fuzz seed 309584898、tiny spec）：logHostCall 讀 (r10, r11)/(r8, r9) 前沒做 isReadable，直接解參考未配置的頁 → target 程序崩潰（「IO error: early eof」）；PR #976 改成不可讀就 continue、無副作用。另外值得核對：現行 logHostCall 沒有設 φ′_7 = WHAT（註解寫「none modified per spec」），與現在的 JIP-1 文字不符——若 service 在 log 後讀 φ_7，會與依 JIP-1 或純 GP 的節點不一致。",
 "trap": "log 不在 GP 裡；合規做法 = 印訊息、φ′_7 = WHAT、bad-index 費用、記憶體無效時零副作用（不能 panic、更不能 crash）。"
},
]
