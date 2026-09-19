# -*- coding: utf-8 -*-
# Appendix A — Polkadot Virtual Machine (GP 0.8.0)
ITEMS = [
{
 "id": "appA-exit-reasons",
 "lens": "演算法",
 "ch": "A", "section": "A.1 Basic Definition", "gpRef": "eq. A.1 (Ψ) & §4.7",
 "difficulty": 1, "kind": "concept", "tags": ["PVM", "dispute"],
  "stemZh": "PVM 的呼叫 Ψ 會回傳一個退出理由 ε。有哪些可能的退出理由？各自帶什麼資料？",
  "optionsZh": [
   "∎ halt（正常終止）、☇ panic、∞ out-of-gas、F̄ × address（page fault，帶最低的不可存取頁位址）、h̄ × id（host call，帶 host-call 識別碼）",
   "∎ halt（正常終止）、☇ panic、∞ out-of-gas、F̄ × address（page fault，帶被存取的確切 octet 位址）、h̄ × id（host call，帶 host-call 識別碼）",
   "∎ halt（正常終止）、☇ panic、∞ out-of-gas、F̄ × address（page fault，帶最低的不可存取頁位址）、⊘ divide-by-zero（當 div_u_64 收到 φ_B = 0 時引發）",
   "∎ halt（正常終止）、☇ panic、∞ out-of-gas、h̄ × id（host call，帶 host-call 識別碼）、⊗ stack-overflow（當 φ_1 落到堆疊最低頁之下時引發）"
  ],
  "stem": "The PVM invocation Ψ returns an exit reason ε. What are the possible exit reasons, and what does each one carry?",
 "options": [
  "∎ halt (regular termination), ☇ panic, ∞ out-of-gas, F̄ × address (page fault, with the lowest inaccessible page address), h̄ × id (host call, with the host-call identifier)",
  "∎ halt (regular termination), ☇ panic, ∞ out-of-gas, F̄ × address (page fault, carrying the exact octet address that was accessed), h̄ × id (host call, with the host-call identifier)",
  "∎ halt (regular termination), ☇ panic, ∞ out-of-gas, F̄ × address (page fault, with the lowest inaccessible page address), ⊘ divide-by-zero (raised when div_u_64 is given φ_B = 0)",
  "∎ halt (regular termination), ☇ panic, ∞ out-of-gas, h̄ × id (host call, with the host-call identifier), ⊗ stack-overflow (raised when φ_1 falls below the stack’s lowest page)"
 ],
 "answer": 0,
 "optNotes": [
   "與 eq. A.1 的 {∎, ☇, ∞} ∪ ({F̄, h̄} × N_R) 完全一致，fault 帶的正是對齊後的 page 位址。",
   "eq. A.9 回的是 Z_P⌊·/Z_P⌋ 對齊後的最低不可存取 page 位址，不是實際存取的 octet 位址。",
   "§A.5.1 的除法從不 panic（除以 0 得 2^64 − 1），⊘ 不存在，這組還漏掉 host call。",
   "PVM 沒有 stack 概念，越界只是 F̄（低於 2^16 才 ☇），這組還漏掉 page fault。",
 ],
 "explanation": "eq. A.1：ε ∈ {∎, ☇, ∞} ∪ ({F̄, h̄} × N_R)，剛好五種。§A.1：「In the case of a final halt, either through panic or success, the instruction counter returned is zero. In all other cases, the return value of the instruction counter indexes the one which caused the exit to happen and the machine state represents the prior state of said instruction」——所以 host call / page fault / OOG 都是可以「續跑」的：改 RAM、補 gas、或執行 host call 並把 PC 前進 1 + skip。stack 只是標準初始化（eq. A.46）配置的一段 W 記憶體，不是 PVM 的原生概念。",
 "trap": "PVM 內部沒有 stack overflow 概念——stack 只是記憶體區段，越界就是 page fault（或 < 2^16 時 panic）。"
},
{
 "id": "appA-basic-blocks-gas",
 "lens": "演算法",
 "ch": "A", "section": "A.3 Basic Blocks & A.5 Single-Step", "gpRef": "eq. A.5–A.8, A.54",
 "difficulty": 3, "kind": "delta", "tags": ["gas", "basic block", "PVM", "delta-0.8.0"],
  "stemZh": "GP 0.8.0（PR #508）引入了新的 gas 模型。gas 是怎麼扣的？",
  "optionsZh": [
   "以 basic block 為單位、事先扣款：在第一步、以及每當執行進入一個 basic block（或跳回它的起點）時，整個 block 的成本 ϱ^Δ 會被扣掉；若剩餘 gas 不足，機器以 ∞ 退出且計數器維持不變；ϱ^Δ = max(cycles − 3, 1)，來自一個模擬的亂序 CPU 模型",
   "以指令為單位、事後扣款：每條執行過的指令花費 1 gas，計數器在該指令退休時遞減，與 0.7.x 完全相同；當扣款會讓計數器低於零時，機器以 ∞ 退出且該筆扣款仍然成立，所以回報的 gas 是負數",
   "以指令為單位、事先扣款：每條指令執行前，依 §A.10 的表扣掉該 opcode 的固定價格（ecalli 100、div_u_64 60、unlikely 40、move_reg 0）；付不出價格就以 ∞ 退出且計數器不變，而 basic block 在 gas 計算中完全不起作用",
   "以 basic block 為單位、事後扣款：ϱ^Δ 要等該 block 的 terminator 執行完才扣，所以中途 panic 的 block 完全不花錢；ϱ^Δ 是該 block 的指令數，而讓計數器變成負值的扣款會以 ∞ 退出並帶著那個負值"
  ],
  "stem": "GP 0.8.0 (PR #508) introduced a new gas model. How is gas charged?",
 "options": [
  "Per BASIC BLOCK, in advance: on the first step and whenever execution enters a basic block (or jumps back to its start), the whole block's cost ϱ^Δ is deducted; if the remaining gas is insufficient the machine exits with ∞ and the counter is unchanged; ϱ^Δ = max(cycles − 3, 1) from a simulated out-of-order CPU model",
  "Per instruction, in arrears: each executed instruction costs 1 gas and the counter is decremented once it retires, exactly as in 0.7.x; when the deduction would take the counter below zero the machine exits with ∞ and the deduction stands, so the gas reported back is negative",
  "Per instruction, in advance: before each instruction a fixed per-opcode price from the §A.10 table is deducted (ecalli 100, div_u_64 60, unlikely 40, move_reg 0); if the price cannot be paid the machine exits with ∞ and the counter is unchanged, and basic blocks play no part in gas accounting at all",
  "Per basic block, in arrears: ϱ^Δ is deducted once the block’s terminator has executed, so a block that panics half-way through costs nothing; ϱ^Δ is the number of instructions in the block, and a deduction that leaves the counter negative exits with ∞ carrying that negative value"
 ],
 "answer": 0,
 "optNotes": [
   "eq. A.8 在 ϱ < ϱ^Δ 時回 (∞, ϱ, ⊥)，counter 一分不動；ϱ^Δ = max(cycles − 3, 1) 即 eq. A.54。",
   "每指令 1 gas 是 0.7.2 的模型，已被 PR #508 取代；OOG 時 gas 不扣，更不會變負值。",
   "§A.10 那張表給的是餵進管線模擬的 cycles 而非 gas 價格，且 GP 要求整個 block 預先收費。",
   "時機與公式都錯：block 是預扣不是事後扣，ϱ^Δ 也不是指令數，照此 panic 的 block 免費。",
 ],
 "explanation": "§A.5：「On the very first step of execution, and every time the execution enters a new basic block or jumps back to the beginning of the current basic block, the gas counter of the machine is updated according to the gas cost function ϱ^Δ of the target basic block. No instruction is allowed to execute within a basic block unless the gas cost for the entire basic block has been charged in advance. In case there's not enough gas remaining… the execution is interrupted and the gas counter remains unchanged.」新增了「gas charged flag」（Ψ 的 bool 參數）以支援 host call 中斷後續跑不重複收費。eq. A.54：ϱ^Δ = max(cycles_final − 3, 1)，cycles 由 §A.9 的微架構模擬算出——初始狀態 (ı, 0, 4 decode slots, 5 starts, ⟨A 4, L 4, S 4, M 1, D 1⟩, ROB = []）、ROB 上限 32 筆；§A.10 有每條指令的 cycles/decode slots/exec units 表。basic block 的邊界 = terminator 指令（trap、fallthrough、jump、jump_ind、load_imm_jump(_ind)、所有 branch_*）之後。你們 0.7.2 每指令 1 gas（GasCost = InstrCount），0.8.0 需重做（issue #1046）。",
 "trap": "面試「PVM portion」極可能問 0.8.0 gas model；記住：block-level、預先扣、max(c−3,1)、不足則 OOG 且不扣。"
},
{
 "id": "appA-memory-access",
 "lens": "演算法",
 "ch": "A", "section": "A.5 Single-Step State Transition", "gpRef": "eq. A.9–A.10 (ε^μ)",
 "difficulty": 2, "kind": "concept", "tags": ["memory", "PVM", "transfer"],
  "stemZh": "當一條指令存取的 RAM 位址 (a) 低於 2^16、或 (b) 位於 2^16 以上的不可存取頁時，會發生什麼事？",
  "optionsZh": [
   "(a) 不論該頁可否存取，機器立即 panic；(b) 機器狀態維持不變，退出理由是 page fault F̄ × (Z_P·⌊addr/Z_P⌋)，回報最低的不可存取頁位址",
   "(a) 該存取變成 page fault F̄ × 0，好讓宿主能區分空指標錯誤與一般的 fault；(b) 機器 panic，因為在 μ_a 中存取模式為 ∅ 的頁永遠無法再變成可存取，所以退出必須是終局的",
   "(a) 不論該頁可否存取，機器立即 panic；(b) 退出理由是 page fault F̄ × addr、帶被請求的確切 octet 位址，而該次存取中落在可存取頁的那些 octet 會在 fault 被引發之前先被寫入",
   "(a) 低於 2^16 的讀取回傳零、寫入被靜默丟棄；(b) 只有讀取才是 page fault F̄ × (Z_P·⌊addr/Z_P⌋)——對存取模式為 R 而非 W 的頁進行寫入會 panic 而不是 fault"
  ],
  "stem": "What happens when an instruction accesses RAM at an address that is (a) below 2^16, or (b) in an inaccessible page above 2^16?",
 "options": [
  "(a) the machine panics immediately regardless of page accessibility; (b) the machine state is unchanged and the exit is a page fault F̄ × (Z_P·⌊addr/Z_P⌋), reporting the lowest inaccessible page address",
  "(a) the access becomes a page fault F̄ × 0 so that the host can tell null-pointer bugs from ordinary faults; (b) the machine panics, because a page whose access mode in μ_a is ∅ can never be made accessible again and so the exit must be final",
  "(a) the machine panics immediately regardless of page accessibility; (b) the exit is a page fault F̄ × addr carrying the exact octet address requested, and the octets of the access that did fall in accessible pages are written before the fault is raised",
  "(a) reads below 2^16 return zero and writes there are silently dropped; (b) the exit is a page fault F̄ × (Z_P·⌊addr/Z_P⌋) for reads only — a write to a page whose access mode is R rather than W panics instead of faulting"
 ],
 "answer": 0,
 "optNotes": [
   "低位址無條件 ☇、高位址回 eq. A.10 的 F̄ × Z_P⌊·/Z_P⌋，且狀態完全不變因此可續跑。",
   "§A.5 明寫低於 2^16「always panics immediately」；不可存取頁反而是可續跑的 fault 而非終局 panic。",
   "eq. A.10 在 ε^μ ≠ ▸ 時 (ı*, φ*, μ*) = (ı, φ, μ)，記憶體一個 byte 都不能先寫下去。",
   "低於 2^16 一律 ☇ 而非靜默；寫入判定用 V*_μ（μ_a = W），寫 R 頁同樣是 F̄ 不是 ☇。",
 ],
 "explanation": "§A.5：「When an index of RAM below 2^16 is required, the machine always panics immediately… regardless of the apparent (in)accessibility of the value. Otherwise, should the given index of RAM not be accessible then machine state remains unchanged and the exit reason is a fault with the lowest inaccessible page address」。eq. A.10：ε^μ = ☇ 當 min(x) mod 2^32 < 2^16；F̄ × Z_P·⌊min(x) mod 2^32 / Z_P⌋ 否則，x 是所有不可讀/不可寫的存取位址集合。第一個 64 KiB zone 永遠不可存取（標準初始化把 RO data 放在 Z_Z = 2^16 開始）——null-pointer 保護。你們 code-map 3.11：「page fault reports the lowest faulting address; any address in the first 64 KiB zone is a panic not a fault」。",
 "trap": "位址先 mod 2^32（暫存器是 64-bit，記憶體是 32-bit 定址）。"
},
{
 "id": "appA-djump-alignment",
 "lens": "設計",
 "ch": "A", "section": "A.5 (dynamic jumps)", "gpRef": "eq. A.22 (jumptablealignment)",
 "difficulty": 2, "kind": "rationale", "tags": ["PVM", "basic block"],
  "stemZh": "對於跳往位址 a 的動態跳躍，GP 要求 a mod Z_A = 0（Z_A = 2）、a ≠ 0、a ≤ |j|·Z_A，且 j[a/Z_A − 1] ∈ ϖ（一個 basic block 的起點）。為什麼要有對齊這條要求？",
  "optionsZh": [
   "因為 LLVM「在產生程式碼時要求並假設動態計算出的跳躍目標具有某種記憶體對齊」，而 JAM 的工具鏈依賴 LLVM，所以 GP 順從了那個假設",
   "因為每個 jump table 項目恰好佔 Z_A = 2 個 octet：那個 2 純粹是項目寬度，所以乘上 Z_A 就把表中的位置換算成 j 內部的 octet 偏移，項目更寬就需要更大的對齊係數",
   "因為 RISC-V 硬體在未對齊的指令提取時會 trap，而 PVM 必須能在 RISC-V 宿主上直接執行；同一條規則也是為什麼 sjump 在檢查 b ∈ ϖ 之前會先拒絕任何 b mod Z_A ≠ 0 的靜態跳躍目標",
   "因為奇數的動態位址被保留作為哨兵：a = 1 代表 halt，其餘每個奇數值都編碼一個 host-call 識別碼，所以要求 a mod Z_A = 0 可以讓真正的程式碼目標與那些編碼互不相交"
  ],
  "stem": "For a dynamic jump to address a, the GP requires a mod Z_A = 0 with Z_A = 2, a ≠ 0, a ≤ |j|·Z_A and j[a/Z_A − 1] ∈ ϖ (a basic-block start). Why the alignment requirement?",
 "options": [
  "Because LLVM 'requires and assumes in its code generation that dynamically computed jump destinations always have a certain memory alignment', and JAM's tooling depends on LLVM, so the GP acquiesces to that assumption",
  "Because every jump-table entry occupies exactly Z_A = 2 octets: the factor of two is simply the entry width, so scaling by Z_A converts a table position into an octet offset inside j, and wider entries would need a larger alignment factor",
  "Because RISC-V hardware traps on an unaligned instruction fetch and the PVM must stay directly executable on RISC-V hosts; the same rule is why sjump also rejects any static jump target b with b mod Z_A ≠ 0 before checking b ∈ ϖ",
  "Because odd dynamic addresses are reserved as sentinels: a = 1 means halt and every other odd value encodes a host-call identifier, so demanding a mod Z_A = 0 keeps genuine code targets disjoint from those encodings"
 ],
 "answer": 0,
 "optNotes": [
   "eq. A.22 的 footnote 直說是遷就 LLVM 對動態計算跳躍目標的對齊假設，純屬工具鏈妥協。",
   "把 Z_A 與 entry 寬度 z 搞混——z 由 blob 的 E_1(z) 決定，a/Z_A − 1 取的是 j 的元素索引。",
   "PVM 從不由 RISC-V 硬體直接執行，且 eq. A.20 的 sjump 只有 b ∉ ϖ 這一個 panic 條件。",
   "halt sentinel 是偶數的 2^32 − 2^16，host-call id 來自 ecalli 的 ν_X 而非 djump 的位址空間。",
 ],
 "explanation": "eq. A.22 的 footnote：「The popular code generation backend LLVM requires and assumes in its code generation that dynamically computed jump destinations always have a certain memory alignment. Since at present we depend on this for our tooling, we must acquiesce to its assumptions.」djump(a)：a = 2^32 − 2^16 → halt；a = 0 ∨ a > |j|·Z_A ∨ a mod Z_A ≠ 0 ∨ j[a/Z_A − 1] ∉ ϖ → panic；否則 PC = j[a/Z_A − 1]。靜態 jump 與 branch 的目標（含 not-taken 的下一條）也都必須是 basic block 起點，否則 panic（§A.5）。",
 "trap": "jump table index 是 a/Z_A − 1（從 1 開始算），因為 a = 0 保留為無效。"
},
]
