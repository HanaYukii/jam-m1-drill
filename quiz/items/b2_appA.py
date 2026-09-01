# -*- coding: utf-8 -*-
# Appendix A — Polkadot Virtual Machine (GP 0.8.0), batch 2.
# Angles not covered by items/appA_pvm.py: branch dual-target rule, jump family, signed div/rem,
# 32-bit shifts, ϱ^Δ worked example, gas-charged flag, recompiler gas/fault paths, register write on
# panicking djump, cross-page fault address, v_blob, opcode renumbering / unlikely.
ITEMS = [
{
 "id": "b2-appA-branch-both-targets",
 "ch": "A", "section": "A.5 Single-Step State Transition (branch)", "gpRef": "eq. A.21 (branch), A.5 (ϖ), A.2 (v_blob)",
 "difficulty": 3, "kind": "code", "tags": ["pvm", "branches", "basic-blocks", "delta-0.8.0"],
  "stemZh": "團隊 0.7.2 直譯器裡的每一條條件分支（170–175 的 instBranch 以及 branch_*_imm 處理常式）都經由這個輔助函數解析。依 GP 0.8.0 的 eq. A.21，關於分支規則的哪個敘述正確？",
  "optionsZh": [
   "0.8.0 只要任一個目標不是 basic block 的起點就 panic——不論是被採取的目標 b、還是落空路徑 ı + 1 + skip(ı)——即使條件為假也一樣；而這個輔助函數只驗證 b、而且只在條件 C 成立時才驗，所以一個「未被採取但目標無效」的分支在這裡會繼續執行，在 0.8.0 卻必須 panic",
   "這個輔助函數已經符合 0.8.0：eq. A.21 只在被採取的路徑上驗證 b，因為落空路徑 ı + 1 + skip(ı) 已經由 v_blob 證明過是被 bitmask 標記的合法 opcode、因此顯然是合法的續行點；額外那個 isOpcodeValid 子句只是無害的加強",
   "0.8.0 仍然只驗證被採取的目標，但現在另外要求它像動態跳躍一樣做 2 位元組對齊（b mod Z_A = 0，Z_A = 2）並且要出現在 jump table j 裡，而這兩點該輔助函數都沒檢查；落空路徑在 0.8.0 也一樣不受驗證",
   "0.8.0 完全移除了執行期的 panic：v_blob 現在會在 deblob 階段走訪每一條分支，除非它的兩個目標都落在 ϖ 裡否則拒絕該 blob，所以 deblob 會回傳 error、Ψ 在執行任何一條指令之前就 panic；因此對 b 的檢查與 isOpcodeValid 子句都是死碼"
  ],
  "stem": "Every conditional branch in the team's 0.7.2 interpreter (instBranch for 170–175 and the branch_*_imm handlers) resolves through this helper. Under GP 0.8.0 eq. A.21, which statement about the branch rule is correct?",
 "code": {"lang": "go", "caption": "PVM/branch.go (branch) + call site in PVM/instructions.go (instBranch)", "src": """func branch(pc ProgramCounter, b ProgramCounter, C bool, bitmask Bitmask, instruction ProgramCode) (ExitReason, ProgramCounter) {
	switch {
	case !C:
		return ExitContinue, pc
	case !bitmask.IsStartOfBasicBlock(b) && instruction.isOpcodeValid(b):
		return ExitPanic, pc
	default:
		return ExitContinue, b
	}
}

// instBranch (opcodes 170-175), after computing branchCondition:
	reason, newPC := branch(pc, vX, branchCondition, interp.Program.Bitmasks, interp.Program.InstructionData)
	if reason != ExitContinue {
		pvmLogger.Errorf("instBranch branch error at pc: %d, opcode: %s", pc, zeta[opcode(interp.Program.InstructionData[pc])])
		return ExitReason(reason), pc
	}

	return reason, newPC"""},
 "options": [
  "0.8.0 panics whenever either target is not a basic-block start — the taken target b or the fall-through ı + 1 + skip(ı) — even when the condition is false; this helper validates only b, and only when C holds, so a not-taken branch with an invalid target continues here but must panic in 0.8.0",
  "The helper is already 0.8.0-compliant: eq. A.21 validates b only on the taken path, because the fall-through ı + 1 + skip(ı) has already been proved by v_blob to be a bitmask-flagged, valid opcode and so is trivially a legal continuation; the extra isOpcodeValid clause is a harmless strengthening",
  "0.8.0 still validates only the taken target, but now additionally requires it to be 2-octet aligned like a dynamic jump (b mod Z_A = 0 with Z_A = 2) and to appear somewhere in the jump table j, neither of which this helper checks; the fall-through path remains unvalidated in 0.8.0 too",
  "0.8.0 removed the runtime panic entirely: v_blob now walks every branch at deblob time and rejects the blob unless both of its targets lie in ϖ, so deblob returns error and Ψ panics before a single instruction runs; both the check on b and the isOpcodeValid clause are therefore dead code"
 ],
 "answer": 0,
 "optNotes": [
   "eq. A.21 的第一個 case 不管 C 真假都要求兩個目標都在 ϖ，所以沒跳的無效 fall-through 也得 ☇。",
   "「通過 v_inst 的合法 opcode」與「∈ ϖ」是兩回事——ϖ 只收 0 或某個 terminator 的下一條。",
   "對齊與查 j 只出現在 eq. A.22 的 djump；靜態 branch 的條件只有兩個目標都 ∈ ϖ。",
   "eq. A.2 的 v_blob/v_inst 只驗指令流形狀，一個跳躍目標都不看，runtime 的 ϖ 檢查省不得。",
 ],
 "explanation": "eq. A.21：branch(b, C) ⟹ (ε, ı′) = (☇, ı) when b ∉ ϖ ∨ ı + 1 + skip(ı) ∉ ϖ；(▸, ı + 1 + skip(ı)) otherwhen ¬C；(▸, b) otherwise。GP 原文：「conditional jumps are valid if and only if both branches point to the start of a basic block (regardless of whether a branch is taken), otherwise a panic occurs」。你們的 branch() 先 `case !C: return ExitContinue, pc`——沒跳就完全不檢查，跳了才檢查 b（還加了 isOpcodeValid 條件，把跳到無效 opcode 的情況留給 trap 處理），這是 0.7.2「taken 才驗證」的語意；issues digest 的 #1046（PVM update 0.8.0）把「branch/jump dual-target validation」列為 App. A 的變更之一。實務上只要 blob 通過 v_blob，branch 的 fall-through 位置必然在 ϖ 裡（branch ∈ T，eq. A.5 的 ϖ 定義），唯一例外是 branch 是程式最後一條指令：ı + 1 + skip(ı) = |c| ∉ ϖ，0.8.0 不論條件真假都在 branch 本身 ☇（0.7.2 則是沒跳時掉出程式碼、執行 ζ 的 0 = trap 才 panic，且多扣一次 gas）。",
 "trap": "0.8.0 口訣：branch 的兩個目標（taken 與 fall-through）都必須是 basic block 起點，不管有沒有跳。"
},
{
 "id": "b2-appA-gas-charged-flag",
 "ch": "A", "section": "A.5 Single-Step State Transition (gas charged flag)", "gpRef": "eq. A.8 (ε^ϱ, ϱ*, flag′), A.11 (flag*), A.6 (𝔏), A.39 (Ψ_H starts with ⊥); §B invoke/machine",
 "difficulty": 3, "kind": "concept", "tags": ["pvm", "gas", "host-calls", "delta-0.8.0"],
  "stemZh": "GP 0.8.0 在 Ψ 中貫穿了一個布林的「gas charged」旗標。某個 basic block 的中間有一條 ecalli；該 host call 回傳 ▸，Ψ_H 從 ı″ = ı′ + 1 + skip(ı′) 繼續。關於這個情境下的 gas 計費，哪個敘述正確？",
  "optionsZh": [
   "只有該 block 的後段會被重新計費：每一種非 ▸ 的退出（包含 host call）都會把旗標清成 ⊥，接著 Ψ_1 只對 ı″ 到該 block terminator 之間的指令計價，所以被 n 次 host call 打斷的 block 花費是它的 ϱ^Δ 加上 n 次部分重計",
   "在那次恢復時什麼都不會再被扣：ecalli 不是 terminator，所以 flag* 維持 ⊤ 而 Ψ_1 略過 ϱ^Δ 的扣款；旗標只有在 terminator 執行之後（或在 out-of-gas 退出時）才變成 ⊥；而一個全新的 Ψ_H——它總是以 ⊥ 起始——若從 block 中段的 ı 恢復，會扣掉整個 block 的 ϱ^Δ(𝔏(ı)) 而不是只扣剩餘的後段",
   "每次 host call 恢復時都會把整個 block 的 ϱ^Δ(𝔏(ı″)) 再扣一次，因為 0.8.0 把 ecalli 加進了 terminator 集合 T，使 host call 總是結束一個 basic block；那個旗標的存在只是為了讓全新 Ψ_H 的第一個 block 不被重複計費兩次",
   "那個旗標只在 out-of-gas 的恢復時才有意義：在其他每一種退出上它都會被丟棄，而 Ψ_H 會在繼續之前無條件扣掉含有 ı″ 之 block 的 ϱ^Δ；在 ∞ 退出時它被設為 ⊤，好讓已扣的 gas 在補充 gas 之後不會再被扣一次；而且它只是 Ψ_H* 的參數，從不屬於 Ψ 本身"
  ],
  "stem": "GP 0.8.0 threads a boolean 'gas charged' flag through Ψ. A basic block has an ecalli in its middle; the host call returns ▸ and Ψ_H resumes at ı″ = ı′ + 1 + skip(ı′). Which statement about gas charging in this situation is correct?",
 "options": [
  "Only the suffix of the block is re-charged: every non-▸ exit — a host call included — clears the flag to ⊥, and Ψ_1 then prices just the instructions from ı″ up to the block’s terminator, so a block interrupted by n host calls costs its ϱ^Δ plus n partial re-charges",
  "Nothing is charged again on that resume: ecalli is not a terminator, so flag* stays ⊤ and Ψ_1 skips the ϱ^Δ deduction; the flag becomes ⊥ only after a terminator executes (or on an out-of-gas exit), while a brand-new Ψ_H — which always starts with ⊥ — resuming at a mid-block ı charges the whole block ϱ^Δ(𝔏(ı)), not just the remaining suffix",
  "The whole block ϱ^Δ(𝔏(ı″)) is charged a second time on every host-call resume, because 0.8.0 added ecalli to the terminator set T so that a host call always ends a basic block; the flag exists only so that the first block of a fresh Ψ_H is not charged twice over",
  "The flag matters only for out-of-gas resumption: on every other exit it is discarded and Ψ_H unconditionally charges ϱ^Δ of the block containing ı″ before continuing; on an ∞ exit it is set to ⊤ so that gas already deducted is not deducted again once more gas is supplied, and it is a parameter of Ψ_H* alone, never of Ψ itself"
 ],
 "answer": 1,
 "optNotes": [
   "ϱ^Δ 的引數是 𝔏(ı) 即 block 起點，GP 沒有 suffix 計價；eq. A.11 也只有兩種情況會清 flag。",
   "ecalli 不在 §A.3 的 T 裡所以 flag* 維持 ⊤；而全新的 Ψ_H 從 ⊥ 開始、扣的是整個 𝔏(ı) block。",
   "§A.3 的 T 只有 trap、fallthrough、jump、jump_ind、load_imm_jump(_ind) 與 branch_*，不含 ecalli。",
   "eq. A.8 的 OOG 支是 (∞, ϱ, ⊥)：flag 清成 ⊥ 且 gas 一分未扣；flag 也是 Ψ 本身的參數。",
 ],
 "explanation": "eq. A.8：(ε^ϱ, ϱ*, flag′) = (▸, ϱ, ⊤) when flag = ⊤；(▸, ϱ − ϱ^Δ(c, k, 𝔏(ı)), ⊤) otherwhen ϱ ≥ ϱ^Δ(c, k, 𝔏(ı))；(∞, ϱ, ⊥) otherwise。eq. A.11：flag* = ⊥ when flag′ = ⊥ ∨ (c_ı ∈ T ∧ ε* ∈ {▸} ∪ {h̄} × N_R)，否則 ⊤。T（§A.3）= trap、fallthrough、jump、jump_ind、load_imm_jump(_ind)、所有 branch_*；ecalli（10）不在 T 裡，所以 ecalli 造成 h̄ exit 時 flag* = ⊤，Ψ（eq. A.1）把這個 flag′ 回傳，Ψ_H*（eq. A.38）以同一個 flag′ 續跑 → 不重複收費。flag 何時變 ⊥：執行了 terminator 且 ε* = ▸（下一步進新 block、或「jumps back to the beginning of the current basic block」都重新收費），以及 OOG（此時 ϱ 不變、ı* = ı）。𝔏（eq. A.6）= max(j ∈ ϖ : j ≤ ı) 是「含 ı 的 block 起點」，所以 flag = ⊥ 而 ı 在 block 中間時，扣的是整個 block 的 ϱ^Δ；Ψ_H ≡ Ψ_H*(…, ⊥, …)（eq. A.39）——每次新的 Ψ_H 都從 ⊥ 開始。App. B 也配合：machine 建立內層 PVM 時 flag 初始為 ⊥，invoke 把 Ψ 回傳的 flag′ 存回 m*[n]，內層 host call 後再 invoke 不會重扣；內層 OOG 後補 gas 再 invoke 才會重扣。這正是 #1046 review 的修正：「mid-block resume must charge the full containing block cost L(i) first — not just the suffix」。你們 0.7.2 沒有這個 flag（每指令 1 gas，SingleStepInvokeDecodedBlocks 逐條扣）。",
 "trap": "flag 只被「執行完的 terminator」與「OOG」清成 ⊥；ecalli 不是 terminator，host call 續跑不重扣。"
},
{
 "id": "b2-appA-recompiler-block-gas-stub",
 "ch": "A", "section": "A.5 Single-Step State Transition (gas charging) — x86-64 recompiler", "gpRef": "eq. A.8 (ε^ϱ, ϱ* unchanged on ∞), A.10 (ı* = ı), A.54 (ϱ^Δ)",
 "difficulty": 3, "kind": "code", "tags": ["pvm", "gas", "recompiler", "delta-0.8.0"],
  "stemZh": "重編譯器裡有一段為 GP 0.8.0 準備好但尚未啟用的 block 層級 gas 路徑（與目前 0.7.2 的逐指令 landing pad 一併列出）。對照 eq. A.8，那條準備好的路徑還有什麼問題？",
  "optionsZh": [
   "沒有問題：在 0.8.0 中每條指令仍然花費 1 gas、只是改成逐 block 彙總，所以在 block 進入時減掉指令數就恰好是 ϱ^Δ；而在 out-of-gas 路徑上讓計數器維持負值也是刻意的，因為 Ψ_M 的 R 函數本來就把用量回報為 u = ϱ − max(ϱ′, 0) 並自行夾住",
   "只有退出的 PC 錯了：在 block 進入時的 out-of-gas 退出上，eq. A.10 要求 ı* 指向該 block 的 terminating 指令——也就是那筆扣款本來會付到的最後一條——而不是 block 的起點；扣款金額與「gas 不動」的規則這段程式碼都已經處理正確了",
   "有兩件事：扣掉的金額必須是來自 A.9 管線模擬的該 block 之 ϱ^Δ（max(cycles − 3, 1)），而不是它的指令數；而且在 out-of-gas 路徑上那筆扣款必須被復原，因為 A.8 在 ϱ < ϱ^Δ 時讓 ϱ 維持不變——逐指令的 pad 有復原它的扣款，block 的 pad 卻沒有",
   "方向錯了：0.8.0 是在 block 的 terminator 執行完之後才對它計費，所以 SubMemImm32 應該放在 terminator 之後、而且符號檢查要反過來；在 block 進入時扣款會對一個中途 panic 的 block 收費，而 eq. A.8 正是靠延後扣款來避免這件事"
  ],
  "stem": "The recompiler contains a prepared-but-disabled block-level gas path for GP 0.8.0 (shown together with the current 0.7.2 per-instruction landing pad). Measured against eq. A.8, what is still wrong with the prepared path?",
 "code": {"lang": "go", "caption": "PVM/recompiler/gas.go (emitOutOfGasExit, emitBlockGasCheck, emitBlockOutOfGasExit)", "src": """// emitOutOfGasExit emits the temporary GP v0.7.2 per-instruction OOG landing pad.
func emitOutOfGasExit(a *asm.Assembler, oog asm.Label, instrPC PVM.ProgramCounter) {
	_ = a.BindLabel(oog)
	// Undo the fused charge: on OOG the interpreter leaves gas unchanged.
	a.SubMemImm32(RegGuestBase, -int32(OffsetGas), -1)
	a.MovMemImm32_32(RegGuestBase, -int32(OffsetExitPC), int32(instrPC))
	a.MovImm64ToReg(RegScratch, uint64(PVM.ExitOOG))
	a.MovRegToMem(RegGuestBase, -int32(OffsetExitReason), RegScratch)
	a.Jmp(a.ExitTrampoline())
}

// emitBlockGasCheck is the prepared block-based gas charging path for GP v0.8.0.
func (c *Compiler) emitBlockGasCheck(a *asm.Assembler, blockOOG asm.Label, instrCount int64) {
	a.SubMemImm32(RegGuestBase, -int32(OffsetGas), int32(instrCount))
	a.Jcc(asm.CondS, blockOOG)
}

// emitBlockOutOfGasExit is the prepared block-entry OOG landing pad for GP v0.8.0.
func emitBlockOutOfGasExit(a *asm.Assembler, blockOOG asm.Label, blockStartPC PVM.ProgramCounter) {
	_ = a.BindLabel(blockOOG)
	a.MovMemImm32_32(RegGuestBase, -int32(OffsetExitPC), int32(blockStartPC))
	a.MovImm64ToReg(RegScratch, uint64(PVM.ExitOOG))
	a.MovRegToMem(RegGuestBase, -int32(OffsetExitReason), RegScratch)
	a.Jmp(a.ExitTrampoline())
}"""},
 "options": [
  "Nothing: in 0.8.0 each instruction still costs 1 gas and is merely aggregated per block, so subtracting the instruction count at block entry is exactly ϱ^Δ; and leaving the counter negative on the out-of-gas path is intended, because Ψ_M's R function reports consumption as u = ϱ − max(ϱ′, 0) and clamps it anyway",
  "Only the exit PC: on a block-entry out-of-gas exit eq. A.10 requires ı* to point at the block's terminating instruction — the last one the charge would have paid for — rather than at the block start; the amount deducted and the untouched-gas rule are both already handled correctly by this code",
  "Two things: the amount deducted must be the block's ϱ^Δ from the A.9 pipeline simulation (max(cycles − 3, 1)), not its instruction count; and on the out-of-gas path the deduction must be undone, because A.8 leaves ϱ unchanged when ϱ < ϱ^Δ — the per-instruction pad restores its charge, the block pad does not",
  "The direction: 0.8.0 charges a block only once its terminator has executed, so the SubMemImm32 belongs after the terminator with the sign check reversed; charging at block entry would bill a block that panics half-way through, which eq. A.8 avoids precisely by deferring the deduction"
 ],
 "answer": 2,
 "optNotes": [
   "0.8.0 的 ϱ^Δ 來自 §A.9 管線模擬，與指令數沒有固定比例；u 的 clamp 也救不了寫回外層的負 counter。",
   "eq. A.10 在 ε^ϱ ≠ ▸ 時 ı* = ı（嘗試收費的那條指令）；而金額與不扣款兩點正是真正的缺陷所在。",
   "金額要換成 eq. A.54 的 max(cycles − 3, 1)，且 A.8 的 ϱ* = ϱ 要求 landing pad 把預扣的錢加回去。",
   "事後收費等於讓 panic 的 block 免費，正是 GP 要求「預先扣款」所要防的事。",
 ],
 "explanation": "eq. A.8：ϱ ≥ ϱ^Δ(c, k, 𝔏(ı)) 才扣（ϱ* = ϱ − ϱ^Δ），否則 (∞, ϱ, ⊥)——「the execution is interrupted and the gas counter remains unchanged」；§A.5 也明說「No instruction is allowed to execute within a basic block unless the gas cost for the entire basic block has been charged in advance」。emitBlockGasCheck 用「先 sub 再看 SF」的技巧，判斷方向沒錯（post-charge < 0 ⟺ pre-charge < 金額），但 (1) 金額是 instrCount——那是 0.7.2 的 GasCost = InstrCount（block_info.go），0.8.0 要用 eq. A.54 的 ϱ^Δ = max(cycles − 3, 1)，由 A.9 的 ROB 模擬與 A.10 表算出（#1046 之後 interpreter 與 recompiler 共用 GasCostForBlock）；(2) 走到 emitBlockOutOfGasExit 時記憶體裡的 gas 已經是「負的」，沒有像 emitOutOfGasExit 那樣 `SubMemImm32(…, -1)` 把錢加回去，違反 ϱ* = ϱ；後果可觀察：R（eq. A.48）算 u = ϱ − max(ϱ′, 0) 會變成「全部 gas 用光」，invoke host call 也會把負的 g′_R 寫回記憶體。至於 ExitPC = blockStartPC：eq. A.10 在 ε^ϱ ≠ ▸ 時 ı* = ı，也就是「嘗試收費的那條指令」，正常進入 block 時就是 block 起點，這部分沒錯（唯一例外是 flag = ⊥ 且從 block 中間恢復，此時 ı* 是恢復點，扣的仍是整個 block）。",
 "trap": "OOG 時 ϱ 不變（A.8）——「先扣再判斷」的 JIT 寫法一定要在 landing pad 把錢加回去，而且扣的是 ϱ^Δ 不是指令數。"
},
{
 "id": "b2-appA-load-imm-jump-ind-reg-write",
 "ch": "A", "section": "A.5.1 Instruction Tables (load_imm_jump_ind) & A.1 (Ψ on panic)", "gpRef": "eq. A.34 table (opcode 180), A.22 (djump), A.1 (Ψ returns φ′ on ☇/∎), A.10; §B invoke",
 "difficulty": 3, "kind": "code", "tags": ["pvm", "jumps", "edge-case", "test-vectors"],
  "stemZh": "在這份 load_imm_jump_ind 的實作中，即使動態跳躍 panic，暫存器寫入 φ_A = ν_X 仍然會發生。這是 GP 0.8.0 所規定的嗎？這個差異有可能被觀察到嗎？",
  "optionsZh": [
   "不是：§A.1 那句「the machine state represents the prior state of said instruction」涵蓋 ☇，就如同它涵蓋 ∞、F̄ 與 h̄ 一樣，所以 djump panic 時 φ_A 必須維持不變；這個寫入是一個潛伏的 bug，之所以沒被發現只是因為 Ψ_M 的 R 函數把 ☇ 映到 panic 結果並把整個暫存器檔丟掉",
   "是的，但只有在 halt 哨兵 a = 2^32 − 2^16 的情況下，此時 φ_A = ν_X 是呼叫者會讀回的內容之一；eq. A.22 是先求值 djump 再做暫存器寫入，所以在 panic 分支上該寫入會被跳過，而且無論如何呼叫者都觀察不到，因為 panic 的內層機器不會動到外層記憶體",
   "不是：eq. A.10 會回滾一條 panic 指令的每一項變動——ε* = ☇ 會強制 (ı*, φ*, μ*) = (ı, φ, μ)，與 page fault 的處理完全相同——所以 φ_A 保持舊值；koute 的 PVM 測試向量也印證了這一點，在每一個 *_nok 的 djump 案例中都期望 φ_A 不變，不論是跳到零、超長、還是未對齊的變體",
   "是的：該表格列把 djump((φ_B + ν_Y) mod 2^32) 與 φ′_A = ν_X 定義為互相獨立的變動，而在 ☇ 時 Ψ 回傳的是 posterior 暫存器 φ′、只把 ı 重設為 0；它是可觀察的，因為 invoke host call 即使在內層以 PANIC 退出時也會把內層機器的暫存器寫回記憶體，而在最上層則透過哨兵停機時的 φ_7／φ_8 觀察得到"
  ],
  "stem": "In this implementation of load_imm_jump_ind the register write φ_A = ν_X happens even when the dynamic jump panics. Is that what GP 0.8.0 prescribes, and can the difference ever be observed?",
 "code": {"lang": "go", "caption": "PVM/instructions.go (instLoadImmJumpInd, opcode 180)", "src": """// opcode 180
func instLoadImmJumpInd(interp *Interpreter, pc ProgramCounter, skipLength ProgramCounter) (ExitReason, ProgramCounter) {
	rA, rB, vX, vY, err := decodeTwoRegistersAndTwoImmediates(interp.Program.InstructionData, pc, skipLength)
	if err != nil {
		pvmLogger.Errorf("instLoadImmJumpInd decodeTwoRegistersAndTwoImmediates error: %v", err)
		return ExitPanic, pc
	}
	// per https://github.com/koute/jamtestvectors/blob/master_pvm_initial/pvm/TESTCASES.md#inst_load_imm_and_jump_indirect_invalid_djump_to_zero_different_regs_without_offset_nok
	// the register update should take place even if the jump panics
	dest := uint32(interp.Registers[rB] + vY)
	reason, newPC := djump(pc, dest, interp.Program.JumpTable, interp.Program.Bitmasks)

	interp.Registers[rA] = vX
	switch reason {
	case ExitPanic:
		return reason, pc
	case ExitHalt:
		return reason, pc
	default:
		return reason, newPC
	}
}"""},
 "options": [
  "No: §A.1's 'the machine state represents the prior state of said instruction' covers ☇ just as it covers ∞, F̄ and h̄, so φ_A must stay untouched when the djump panics; the write is a latent bug that goes unnoticed only because Ψ_M's R function maps ☇ to the panic result and throws the register file away",
  "Yes, but only for the halt sentinel a = 2^32 − 2^16, where φ_A = ν_X is part of what the caller reads back; eq. A.22 evaluates djump before the register write, so on the panic branch the write is skipped, and no caller could observe it anyway because a panicking inner machine leaves the outer memory untouched",
  "No: eq. A.10 rolls back every mutation of a panicking instruction — ε* = ☇ forces (ı*, φ*, μ*) = (ı, φ, μ) exactly as it does for a page fault — so φ_A keeps its old value; the koute PVM test vectors bear this out, expecting φ_A unchanged in every *_nok djump case — the jump-to-zero, the over-length and the misaligned variants alike",
  "Yes: the table row defines djump((φ_B + ν_Y) mod 2^32) and φ′_A = ν_X as independent mutations, and on ☇ Ψ returns the posterior registers φ′ with only ı reset to 0; it is observable because the invoke host call writes the inner machine's registers back to memory even when the inner exit is PANIC, and at top level via φ_7/φ_8 when the sentinel halts"
 ],
 "answer": 3,
 "optNotes": [
   "那句 prior state 的主詞是「In all other cases」，☇/∎ 回的是 posterior 狀態、只有 ı 歸零。",
   "eq. A.34 把兩個 mutation 並列、沒有任何條件化；invoke 在 c = ☇ 時照樣把 φ′ 寫回外層 RAM。",
   "回捲只發生在 ε^ϱ ≠ ▸ 與 ε^μ ≠ ▸ 兩支，指令層級的 ☇ 走的是 otherwise 支 (ε, ı′, φ′, μ′)。",
   "表列把 djump 與 φ′_A = ν_X 並列，而 eq. A.1 在 ☇ 回傳 posterior 的 φ′，只有 ı 歸零。",
 ],
 "explanation": "eq. A.34 表列 load_imm_jump_ind：djump((φ_B + ν_Y) mod 2^32)，φ′_A = ν_X——兩個 mutation 並列、互不條件化；eq. A.22 的 djump 只決定 (ε, ı′)。eq. A.10：ε^ϱ、ε^μ 都是 ▸ 時 (ε*, ı*, φ*, μ*) = (ε, ı′, φ′, μ′)，所以 ε = ☇ 時 φ* 仍含這次寫入；eq. A.1 的 Ψ 在 ε ∈ {☇, ∎} 回傳 (ε, 0, ϱ′, flag′, φ′, μ′)——posterior 的暫存器、只有 ı 歸零。§A.1：「In the case of a final halt, either through panic or success, the instruction counter returned is zero」，而那句「the machine state represents the prior state of said instruction」講的是「In all other cases」，即 ∞ / F̄ / h̄ 這三種可續跑的 exit（Ψ 回傳 (ε, ı, ϱ′, flag′, φ, μ)）。可觀察性：App. B 的 invoke 在 c = ☇ 時仍回 (▸, PANIC, φ_8, μ*, m*)，而 μ* 把 E_8(g′_R) ⌢ E_8(φ′) 寫回外層記憶體，外層程式讀得到內層 panic 後的暫存器；頂層 Ψ_M（eq. A.48 的 R）雖對 ☇ 回 panic，但 sentinel halt 時回傳 μ′[φ′_7 …+φ′_8]，若 A ∈ {7, 8} 也直接可見。你們程式碼註解引用的 koute 測試向量 inst_load_imm_and_jump_indirect_invalid_djump_to_zero_different_regs_without_offset_nok 正是要求 panic 後暫存器已更新。load_imm_jump（80）同理：sjump(ν_Y) 與 φ′_A = ν_X 並列。",
 "trap": "☇ 與 ∎ 回傳 posterior 狀態（只有 ı 歸零）；∞ / F̄ / h̄ 才回傳 prior 狀態以便續跑。"
},
{
 "id": "b2-appA-vblob-terminator",
 "ch": "A", "section": "A.1 Basic Definition (deblob validity v_blob / v_inst)", "gpRef": "eq. A.2 (deblob, v_blob, v_inst), A.3 (skip), A.4 (ζ), A.5 (ϖ)",
 "difficulty": 2, "kind": "delta", "tags": ["pvm", "validation", "codec", "delta-0.8.0"],
  "stemZh": "GP 0.8.0 的 deblob(p, ı) 會回傳 error——而 Ψ 隨即在未執行任何指令的情況下 panic——除非 v_blob(c, k, 0) 與 v_inst(c, k, ı) 同時成立。這兩個驗證器實際上強制了哪一組條件？",
  "optionsZh": [
   "只強制 |k| = |c| 以及每個 jump-table 項目都指向某個 basic block 的起點；opcode 的合法性留給執行期處理，屆時未知的 opcode 行為等同 opcode 0 而 trap，而進入點 ı 不論落在哪裡都被接受，因為 Ψ 會從 k 重新推導出最近的 opcode 邊界",
   "強制每個分支與跳躍目標都落在 ϖ 裡、且沒有任何指令長於 16 個 octet，兩者都在對程式碼的單次走訪中確立；最後一條指令可以是任何東西，因為 ζ 會用零填補程式碼，所以跑過尾端就只是執行 opcode 0 而 trap",
   "|k| = |c|；從索引 0 開始以 1 + skip(·) 走訪程式碼，每一個被造訪的 octet 都在 k 中被標記且是合法的 opcode（∈ U）；該次走訪恰好結束在 |k|，且最後一條指令是 terminator（∈ T）；而進入點 ı 本身也必須是一個被標記的合法 opcode",
   "強制程式碼中至少含有一條 ecalli、並以一個跳往 halt 哨兵 2^32 − 2^16 的 jump_ind 結尾，好讓每支程式都有明確定義的返回宿主路徑；bitmask 本身不需要檢查，因為 k 是在 deblob 解碼時由每個 opcode 的長度重新產生的"
  ],
  "stem": "GP 0.8.0's deblob(p, ı) returns error — and Ψ then panics without executing anything — unless v_blob(c, k, 0) and v_inst(c, k, ı) both hold. Which set of conditions do these two validators actually enforce?",
 "options": [
  "Only that |k| = |c| and that every jump-table entry points at a basic-block start; opcode validity is left to execution time, where an unknown opcode behaves like opcode 0 and traps, and the entry point ı is accepted wherever it lands, since Ψ re-derives the nearest opcode boundary from k",
  "That every branch and jump target lies in ϖ and that no instruction is longer than 16 octets, both established during a single walk of the code; the final instruction may be anything, because ζ pads the code with zeros so that running off the end simply executes opcode 0 and traps",
  "|k| = |c|; walking the code from index 0 by 1 + skip(·), every visited octet is flagged in k and is a valid opcode (∈ U); the walk ends exactly at |k| with the last instruction a terminator (∈ T); and the entry point ı is itself a flagged, valid opcode",
  "That the code contains at least one ecalli and ends with a jump_ind to the halt sentinel 2^32 − 2^16, so that every program has a well-defined return path to the host; the bitmask itself needs no check, since k is regenerated from each opcode's length while deblob decodes"
 ],
 "answer": 2,
 "optNotes": [
   "deblob 另外要求 v_inst(c, k, ı)：入口必須 k_ı = 1 且 c_ı ∈ U，Ψ 不會替你重新對齊到最近邊界。",
   "跳躍目標是 eq. A.20/A.21 在 runtime 查 ϖ；真正的關鍵被漏掉了——走訪必須停在 |k| 且尾端 ∈ T。",
   "四項正是 eq. A.2 的 v_blob 與 v_inst：|k| = |c|、沿途皆合法 opcode、剛好停在 |k|、尾端 ∈ T。",
   "GP 沒有這兩條結構要求；k 是 blob 實際傳來的欄位，正因指令長度隱含才需要它，無法反推。",
 ],
 "explanation": "eq. A.2：v_blob(c, k, ı) = ⊤ when ı > 0 ∧ ı = |k|；⊥ otherwhen ı + 1 + skip(ı) = |k| ∧ c_ı ∉ T；v_blob(c, k, ı + 1 + skip(ı)) otherwhen v_inst(c, k, ı)；⊥ otherwise。v_inst(c, k, ı) = |k| = |c| ∧ ı < |k| ∧ k_ı = 1 ∧ c_ı ∈ U。也就是從 0 開始沿 skip 走訪每條指令：每個落點都要是 bitmask 標記的合法 opcode、最後一條必須是 terminator、走訪要剛好停在 |k|（空程式因 ı > 0 條件而無效）；deblob 另外用 v_inst(c, k, ı) 驗證入口 ı。這是 0.8.0 的新規（issues digest #1046：「programs whose final block lacks a terminator are invalid (v_blob rule)」；PR #508 摘要：「blobs pre-validated」），動機是 block-based gas：ϱ^Δ 的模擬（eq. A.58 只有遇到 T 才把 x_ı 設為 ∅）需要每個 basic block 都有終點。0.7.2 沒有 v_blob，無效 opcode 或掉出程式碼末端是靠 ζ = c ⌢ [0, 0, …]（eq. A.4）的 trap 在 runtime 才 panic（會多扣 gas）；0.8.0 裡 ζ 的零填充只剩「最後一條指令缺少的引數 octet」這個用途。你們的 preDecodeBlocks 其實已在 deblob 時對「block 跑出程式末端」與無效 opcode 回 ExitPanic，MakeBitMasks 也驗 bitmask 長度，與 0.8.0 方向一致。",
 "trap": "v_blob 驗的是「指令流的形狀」（合法 opcode + terminator 收尾），不驗跳躍目標；跳錯位置仍是 runtime panic。"
},
]
