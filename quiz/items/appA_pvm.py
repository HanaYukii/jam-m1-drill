# -*- coding: utf-8 -*-
# Appendix A — Polkadot Virtual Machine (GP 0.8.0)
ITEMS = [
{
 "id": "appA-exit-reasons",
 "ch": "A", "section": "A.1 Basic Definition", "gpRef": "eq. A.1 (Ψ) & §4.7",
 "difficulty": 1, "kind": "concept", "tags": ["pvm"],
  "stemZh": "PVM 的呼叫 Ψ 會回傳一個退出理由 ε。哪一個是可能的退出理由的完整集合？",
  "optionsZh": [
   "∎ halt（正常終止）、☇ panic、∞ out-of-gas、F̄ × address（page fault，帶最低的不可存取頁位址）、h̄ × id（host call，帶 host-call 識別碼）",
   "∎ halt（正常終止）、☇ panic、∞ out-of-gas、F̄ × address（page fault，帶被存取的確切 octet 位址）、h̄ × id（host call，帶 host-call 識別碼）",
   "∎ halt（正常終止）、☇ panic、∞ out-of-gas、F̄ × address（page fault，帶最低的不可存取頁位址）、⊘ divide-by-zero（當 div_u_64 收到 φ_B = 0 時引發）",
   "∎ halt（正常終止）、☇ panic、∞ out-of-gas、h̄ × id（host call，帶 host-call 識別碼）、⊗ stack-overflow（當 φ_1 落到堆疊最低頁之下時引發）"
  ],
  "stem": "The PVM invocation Ψ returns an exit reason ε. Which is the complete set of possible exit reasons?",
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
 "id": "appA-program-blob",
 "ch": "A", "section": "A.1 Basic Definition (deblob)", "gpRef": "eq. A.2 (deblob), A.3 (skip)",
 "difficulty": 2, "kind": "concept", "tags": ["pvm", "codec"],
  "stemZh": "PVM 程式 blob p 的版面配置是什麼？opcode bitmask k 的作用又是什麼？",
  "optionsZh": [
   "p = E(|j|) ⌢ E_1(z) ⌢ E(|c|) ⌢ E_z(j) ⌢ c ⌢ k：jump table 長度、jump table 每項的寬度 z、code 長度、jump table 本身（每項 z 個 octet）、指令資料 c，最後是 bitmask k（每個 code octet 一位，1 表示這個 octet 是 opcode）；|k| 必須等於 |c|",
   "p = E(|c|) ⌢ c ⌢ E(|k|) ⌢ k ⌢ E(|j|) ⌢ j：指令資料與它的 bitmask 排在最前，好讓 deblob 在還沒讀到表之前就能解碼指令，而每個 jump table 項目固定 4 個 octet 寬；k 是每個 code octet 一位，1 表示這個 octet 是 opcode",
   "p = magic ⌢ version ⌢ E_4(|c|) ⌢ c ⌢ relocations：一份精簡過的 RISC-V ELF 映像，由 header 給出 code 長度，完全沒有 bitmask——指令邊界由每個 opcode 固定 4 octet 的長度推得，動態跳躍目標則由 relocation 表補上",
   "欄位順序同樣是 p = E(|j|) ⌢ E_1(z) ⌢ E(|c|) ⌢ E_z(j) ⌢ c ⌢ k，但 k 標記的是每條指令之後的那個 octet 而不是它的 opcode octet，所以 |k| = |c| + 1（多出來的那一位用來終止最後一條指令），而 skip(i) 是往回數到前一個被設起的位元"
  ],
  "stem": "What is the layout of a PVM program blob p, and what does the opcode bitmask k do?",
 "options": [
  "p = E(|j|) ⌢ E_1(z) ⌢ E(|c|) ⌢ E_z(j) ⌢ c ⌢ k: jump-table length, jump-table entry width z, code length, the jump table (entries of z octets each), the instruction data c, then the bitmask k (one bit per code octet, 1 = this octet is an opcode); |k| must equal |c|",
  "p = E(|c|) ⌢ c ⌢ E(|k|) ⌢ k ⌢ E(|j|) ⌢ j: the instruction data and its bitmask come first so that deblob can decode instructions before it has read the table, and every jump-table entry is a fixed 4 octets wide; k is one bit per code octet, 1 = this octet is an opcode",
  "p = magic ⌢ version ⌢ E_4(|c|) ⌢ c ⌢ relocations: a stripped RISC-V ELF image whose headers give the code length, with no bitmask at all — instruction boundaries follow from each opcode’s fixed 4-octet length, and dynamic jump targets are patched in by the relocation table",
  "p = E(|j|) ⌢ E_1(z) ⌢ E(|c|) ⌢ E_z(j) ⌢ c ⌢ k in that field order, but k flags the octet *after* each instruction rather than its opcode octet, so |k| = |c| + 1 (the extra bit terminates the last instruction) and skip(i) counts backwards to the previous set bit"
 ],
 "answer": 0,
 "optNotes": [
   "欄位順序與 v_inst 的 |k| = |c| ∧ k_ı = 1 都對上 eq. A.2：k 標的正是每條指令的 opcode octet。",
   "違反 eq. A.2 的欄位順序，且 entry 寬度是 blob 裡的 E_1(z) 變數，不是固定 4 octets。",
   "§A.2 的指令長度隱含且最多 16 octets，動態跳躍是 runtime 查 j（eq. A.22）而非載入期重定位。",
   "v_inst 要求 |k| = |c| 且標記的就是 opcode 那個 octet，eq. A.3 的 skip 也是往前找下一個 set bit。",
 ],
 "explanation": "eq. A.2 的 deblob 要求 p = E(|j|) ⌢ E_1(z) ⌢ E(|c|) ⌢ E_z(j) ⌢ E(c) ⌢ E(k)——jump table 長度、**每個 table 項目的寬度 z**（單一位元組）、code 長度、jump table 本身、指令資料 c，最後是 bitmask k。**k 是這題的核心**：PVM 以 **octet 為單位**計算指令位置，而指令長度是隱含的（最多 16 octet），所以需要一張表告訴解碼器「哪些 octet 是 opcode 的起點」——k 就是每個 code octet 一位，1 表示這裡是 opcode。|k| 必須等於 |c|。**指令長度怎麼算出來**：eq. A.3 的 skip(i) = min(24, 到下一個 set bit 的距離 − 1)，也就是「離下一條指令還有幾個位元組」。k 的後面補無限多個 1，讓**最後一條指令也有定義**，不必特別處理邊界。**兩個驗證條件**：v_blob(c, k, 0) 與 v_inst(c, k, ı) 都必須成立——沿著 skip 走訪的每個落點都得是 bitmask 標記的合法 opcode，且最後一條是 terminator。不成立就直接 panic，**一條指令都不執行**（0.8.0 的行為）。**還有一個安全網**：eq. A.4 定義指令資料 ζ = c ⌢ [0, 0, …]，所以 PC 若跑出程式碼範圍，讀到的是 opcode 0 = trap，而不是未定義行為。",
 "trap": "deblob 失敗（格式錯）→ 整個 Ψ 直接 panic。"
},
{
 "id": "appA-basic-blocks-gas",
 "ch": "A", "section": "A.3 Basic Blocks & A.5 Single-Step", "gpRef": "eq. A.5–A.8, A.54",
 "difficulty": 3, "kind": "delta", "tags": ["pvm", "gas", "delta-0.8.0"],
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
 "ch": "A", "section": "A.5 Single-Step State Transition", "gpRef": "eq. A.9–A.10 (ε^μ)",
 "difficulty": 2, "kind": "concept", "tags": ["pvm", "memory"],
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
 "id": "appA-standard-init",
 "ch": "A", "section": "A.7 Standard Program Initialization", "gpRef": "eq. A.42–A.47",
 "difficulty": 3, "kind": "concept", "tags": ["pvm", "memory"],
  "stemZh": "在標準程式初始化 Y(p, a) 之下，哪一組暫存器／記憶體配置是正確的？",
  "optionsZh": [
   "φ_0 = 2^32 − 2^16（返回位址，跳到那裡即 halt）、φ_1 = 2^32 − 2·Z_Z − Z_I（堆疊指標）、φ_7 = 2^32 − Z_Z − Z_I（引數指標）、φ_8 = |a|；唯讀資料放在 Z_Z = 2^16、可讀寫資料（heap）放在 2·Z_Z + Z(|o|)、堆疊止於 2^32 − 2·Z_Z − Z_I、引數放在 2^32 − Z_Z − Z_I；Z_I = 2^24",
   "φ_0 = 0、φ_1 = 2^32 − 1（堆疊指標位於 RAM 最頂端）、φ_7 = 2^32 − Z_Z − Z_I（引數指標）、φ_8 = |a|；唯讀資料放在位址 0、可讀寫資料（heap）緊接其後不留間隙、堆疊自 2^32 − 1 向下成長、引數放在 2^32 − Z_Z − Z_I；Z_I = 2^24",
   "φ_0 = 2^32 − 2^16（返回位址，跳到那裡即 halt）、φ_1 = 2^32 − 2·Z_Z − Z_I（堆疊指標）、φ_7 = |a|、φ_8 = 2^32 − Z_Z − Z_I（引數指標）；唯讀資料放在 Z_Z = 2^16、可讀寫資料（heap）放在 2·Z_Z + Z(|o|)、堆疊止於 2^32 − 2·Z_Z − Z_I、引數放在 2^32 − Z_Z − Z_I；Z_I = 2^24",
   "φ_0 = 2^32 − 2^16（返回位址，跳到那裡即 halt）、φ_1 = 2^32 − 2·Z_Z − Z_I（堆疊指標）、φ_7 = 2^32 − Z_Z − Z_I（引數指標）、φ_8 = |a|；唯讀資料放在 Z_Z = 2^16 但映射為 W 所以程式可以就地修改它、可讀寫資料（heap）放在 2·Z_Z + Z(|o|)、堆疊止於 2^32 − 2·Z_Z − Z_I、引數放在 2^32 − Z_Z − Z_I；Z_I = 2^16"
  ],
  "stem": "Under standard program initialization Y(p, a), which register/memory layout is correct?",
 "options": [
  "φ_0 = 2^32 − 2^16 (return address; jumping there halts), φ_1 = 2^32 − 2·Z_Z − Z_I (stack pointer), φ_7 = 2^32 − Z_Z − Z_I (argument pointer), φ_8 = |a|; RO data at Z_Z = 2^16, RW data (heap) at 2·Z_Z + Z(|o|), stack ends at 2^32 − 2·Z_Z − Z_I, args at 2^32 − Z_Z − Z_I; Z_I = 2^24",
  "φ_0 = 0, φ_1 = 2^32 − 1 (stack pointer at the very top of RAM), φ_7 = 2^32 − Z_Z − Z_I (argument pointer), φ_8 = |a|; RO data at address 0, RW data (heap) immediately after it with no gap, stack growing down from 2^32 − 1, args at 2^32 − Z_Z − Z_I; Z_I = 2^24",
  "φ_0 = 2^32 − 2^16 (return address; jumping there halts), φ_1 = 2^32 − 2·Z_Z − Z_I (stack pointer), φ_7 = |a|, φ_8 = 2^32 − Z_Z − Z_I (argument pointer); RO data at Z_Z = 2^16, RW data (heap) at 2·Z_Z + Z(|o|), stack ends at 2^32 − 2·Z_Z − Z_I, args at 2^32 − Z_Z − Z_I; Z_I = 2^24",
  "φ_0 = 2^32 − 2^16 (return address; jumping there halts), φ_1 = 2^32 − 2·Z_Z − Z_I (stack pointer), φ_7 = 2^32 − Z_Z − Z_I (argument pointer), φ_8 = |a|; RO data at Z_Z = 2^16 but mapped W so the program may patch it, RW data (heap) at 2·Z_Z + Z(|o|), stack ends at 2^32 − 2·Z_Z − Z_I, args at 2^32 − Z_Z − Z_I; Z_I = 2^16"
 ],
 "answer": 0,
 "optNotes": [
   "eq. A.46/A.47 全部對上：段間各留一個 Z_Z 空洞、φ_0 為 halt sentinel、Z_I = 2^24。",
   "第一個 Z_Z zone 永遠不配置（null-pointer 保護），且 φ_0 不是 halt sentinel 就回不了 entry function。",
   "eq. A.47 是 φ_7 存參數指標、φ_8 存長度，對調會一併弄壞 Ψ_M 的回傳值 μ′[φ′_7 … +φ′_8]。",
   "eq. A.46 的 o 段與參數段存取模式皆為 R，只有 w/heap 與 stack 是 W；Z_I = 2^24，2^16 是 Z_Z。",
 ],
 "explanation": "eq. A.42：JAM program blob 格式 E_3(|o|) ⌢ E_3(|w|) ⌢ E_2(z) ⌢ E_3(s) ⌢ o ⌢ w ⌢ E_4(|p|) ⌢ p（o = RO data、w = RW data、z = 額外 heap 頁數、s = stack 大小）。eq. A.46：記憶體區段——[Z_Z, Z_Z+|o|) RO、[2Z_Z + Z(|o|), …) RR（w 之後 + z 頁）、stack 在 [2^32 − 2Z_Z − Z_I − P(s), 2^32 − 2Z_Z − Z_I) 可寫、args 在 [2^32 − Z_Z − Z_I, …) 唯讀；每段之間刻意留一個 Z_Z = 64 KiB 的未配置 zone，「one major zone is always left unallocated between sections in order to reduce accidental overrun」。eq. A.47：φ_0 = 2^32 − 2^16、φ_1 = 2^32 − 2Z_Z − Z_I、φ_7 = 2^32 − Z_Z − Z_I、φ_8 = |a|，其餘 0；Z_I = 2^24 是最大參數大小。",
 "trap": "φ_0 是 RA：djump 到 2^32 − 2^16 = 0xFFFF0000 即 halt（eq. A.22 附近的 djump 定義）。"
},
{
 "id": "appA-djump-alignment",
 "ch": "A", "section": "A.5 (dynamic jumps)", "gpRef": "eq. A.22 (jumptablealignment)",
 "difficulty": 2, "kind": "rationale", "tags": ["pvm", "rationale"],
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
{
 "id": "appA-host-call-continue",
 "ch": "A", "section": "A.6 Host Call Definition", "gpRef": "§A.6 (Ψ_H)",
 "difficulty": 2, "kind": "concept", "tags": ["pvm", "host-calls"],
  "stemZh": "在 Ψ_H 中，當內層的 Ψ 以 h̄ × h（經由 `ecalli` 的 host call）退出時，接下來會發生什麼？",
  "optionsZh": [
   "context mutator f(h, ϱ, φ, μ, x) 會執行；若它回傳 ▸（continue），Ψ_H 會以推進到 ı′ + 1 + skip(ı′) 的指令計數器、以及新的 gas／暫存器／記憶體／context 繼續執行；若它回傳 ☇／∎／∞，那就成為最終的退出理由；page fault 不可能從 host call 本身冒出來",
   "context mutator f(h, ϱ, φ, μ, x) 會執行；若它回傳 ▸（continue），Ψ_H 會在不變的計數器 ı′ 處繼續，好讓那條 ecalli 重新執行、使 host call 具冪等性；若它回傳 ☇／∎／∞，那就成為最終的退出理由；f 也可以回傳 F̄ 把 page fault 交回去",
   "Ψ_H 會停下內層機器，把 h̄ × h 連同暫存器檔一起上交給自己的呼叫者；由該呼叫者執行 host call、重建機器，再以全新的 gas 從 ı′ + 1 + skip(ı′) 重新進入 Ψ——這正是 h̄ 仍留在 Ψ_H 退出理由集合中的原因",
   "context mutator f(h, ϱ, φ, μ, x) 會執行；回傳 ▸ 時 Ψ_H 從 ı′ + 1 + skip(ı′) 繼續，但會先把 gas-charged 旗標重設為 ⊥，因此含有那條 ecalli 的 block 會被再扣一次 ϱ^Δ；f 回傳的 ☇／∎／∞ 則成為最終退出理由"
  ],
  "stem": "In Ψ_H, when the inner Ψ exits with h̄ × h (a host call via `ecalli`), what happens next?",
 "options": [
  "The context mutator f(h, ϱ, φ, μ, x) runs; if it returns ▸ (continue), Ψ_H resumes with the instruction counter advanced to ı′ + 1 + skip(ı′), the new gas/registers/memory/context; if it returns ☇/∎/∞ that becomes the final exit; a page fault cannot come out of a host call itself",
  "The context mutator f(h, ϱ, φ, μ, x) runs; if it returns ▸ (continue), Ψ_H resumes at the unchanged counter ı′ so that the ecalli re-executes and the host call is idempotent; if it returns ☇/∎/∞ that becomes the final exit; f may also return F̄ and hand a page fault back",
  "Ψ_H halts the inner machine and passes h̄ × h up to its own caller together with the register file; that caller performs the host call, rebuilds the machine and re-enters Ψ at ı′ + 1 + skip(ı′) with fresh gas — which is why h̄ stays in Ψ_H’s exit-reason set",
  "The context mutator f(h, ϱ, φ, μ, x) runs; on ▸ Ψ_H resumes at ı′ + 1 + skip(ı′), but the gas-charged flag is first reset to ⊥, so the block holding the ecalli is charged ϱ^Δ a second time; a ☇/∎/∞ returned by f becomes the final exit"
 ],
 "answer": 0,
 "optNotes": [
   "§A.6 要求明確給出 ı″ = ı′ + 1 + skip(ı′)，且 f 的型別 Ω_X 裡沒有 fault。",
   "PC 停在原地會讓 ecalli 無限重跑；f 的 codomain {▸, ∎, ☇, ∞} 也不含 F̄。",
   "違反 Ψ_H 的 codomain {☇, ∞, ∎} ∪ {F̄} × N_R——host call 是在內部用 state-mutator 處理掉的。",
   "eq. A.11 的 flag 只在 terminator 執行完或 OOG 時變 ⊥，ecalli 不在 T 裡，不會重扣整個 block。",
 ],
 "explanation": "§A.6：Ψ_H* 先跑 Ψ；若 ε′ ∈ {∎, ☇, ∞} ∪ F̄ 直接回傳；若 ε′ = h̄ × h 則呼叫 f（Ω 函數，依 invocation 類型決定），得到 (▸, ϱ″, φ″, μ″, x″) 就以 ı″ = ı′ + 1 + skip(ı′) 續跑；得到 ☇/∎/∞ 則結束。「we must provide the new instruction counter value ı″ explicitly」——因為 Ψ 回傳的 PC 指向造成 exit 的那條指令（ecalli 本身）。GP 也明說「host-calls are in effect handled internally with the state-mutator function provided as an argument, preventing the possibility of the result being a host-call fault」。gas charged flag 保留（續跑同一 basic block 不重複收費）。未知 host call id：扣 M_∅ = 1000 gas 並在 φ_7 放 WHAT（eq. B.2/B.6/B.10 的 otherwise 分支）。",
 "trap": "你們 interpreter 的 hostCallException 就是「charge gas → φ_7 = WHAT」。"
},
{
 "id": "appA-registers-immediates",
 "ch": "A", "section": "A.5.1 Instruction Tables", "gpRef": "§A.5.1 & eq. A.19 (sign extension)",
 "difficulty": 2, "kind": "concept", "tags": ["pvm", "decoding"],
  "stemZh": "暫存器運算元與 immediate 是怎麼從一條指令的 octet 解碼出來的？",
  "optionsZh": [
   "在兩暫存器的指令形式中，兩個暫存器索引來自 opcode 之後那個 octet 的低位與高位 nibble，各自以 min(12, …) 夾住；immediate 是 little-endian，而在編碼允許變寬 immediate 的地方，其寬度由該指令的 skip 距離導出，值則被 sign-extend 成 64 位元",
   "在兩暫存器的指令形式中，兩個暫存器索引來自 opcode 之後那個 octet 的低位與高位 nibble，各自以 min(12, …) 夾住；immediate 是 big-endian，凡是帶 immediate 的形式其寬度一律固定為 4 個 octet，且被 zero-extend 成 64 位元，所以負常數需要另一條 negate 指令",
   "暫存器索引各佔一整個 octet——第一個是 ζ_{ı+1}、第二個是 ζ_{ı+2}，各自以 min(12, …) 夾住，所以每條兩暫存器指令至少 3 個 octet 長；immediate 是 little-endian 並被 sign-extend 成 64 位元，但凡是帶 immediate 的形式其寬度一律固定為 8 個 octet",
   "暫存器索引是打包進 opcode octet 本身的 3 位元欄位，因此每個格式類別只剩 32 個 opcode；immediate 是 little-endian、寬度取自 skip 距離並被 sign-extend 成 64 位元，但因為只塞得下 8 種編碼，φ_8 … φ_12 只能透過 move_reg 存取"
  ],
  "stem": "How are register operands and immediates decoded from an instruction's octets?",
 "options": [
  "For the two-register instruction forms the register indices come from the low and high nibbles of the octet after the opcode, each clamped with min(12, …); immediates are little-endian and, where the encoding allows a variable-width immediate, its width is derived from the instruction's skip distance and the value is sign-extended to 64 bits",
  "For the two-register instruction forms the register indices come from the low and high nibbles of the octet after the opcode, each clamped with min(12, …); immediates are big-endian, their width is fixed at 4 octets in every form that takes one, and they are zero-extended to 64 bits, so a negative constant needs a separate negate instruction",
  "The register indices are whole octets — ζ_{ı+1} for the first and ζ_{ı+2} for the second, each clamped with min(12, …), so every two-register instruction is at least 3 octets long; immediates are little-endian and sign-extended to 64 bits, but their width is fixed at 8 octets in every form that takes one",
  "Register indices are 3-bit fields packed into the opcode octet itself, leaving 32 opcodes per format class; immediates are little-endian, take their width from the skip distance and are sign-extended to 64 bits, but because only 8 encodings fit, φ_8 … φ_12 are reachable only through move_reg"
 ],
 "answer": 0,
 "optNotes": [
   "兩暫存器類的兩個索引擠在 ζ_{ı+1} 的高低 nibble，ℓ_X 由 skip 導出並依 eq. A.19 sign-extend。",
   "§A.5 明說 immediate 是 little-endian、MSB 為符號位，省略高位補 0 或 255，補零會把 −1 變成 0xFF。",
   "只有三暫存器類才用 ζ_{ı+2} 放 r_D；固定 8-octet immediate 也只有 load_imm_64 一條。",
   "3 bits 只能表示 8 個暫存器，但 §4.7 有 13 個；opcode octet 從頭到尾都是 opcode，沒有分租。",
 ],
 "explanation": "指令表（§A.5.5 起）逐類給出解碼規則。以「Two Registers & One Immediate」為例：r_A = min(12, ζ_{ı+1} mod 16)、r_B = min(12, ⌊ζ_{ı+1}/16⌋)、ℓ_X = min(4, max(0, skip(ı) − 1))、ν_X 由 eq. A.19 的 sign extension 得出。clamp 到 12 是因為只有 13 個暫存器（0..12）。§A.5：「Immediate arguments are encoded in little-endian format with the most-significant bit being the sign bit… Elided octets are assumed to be zero if the MSB of the value is zero, and 255 otherwise」——省略高位正是為了壓縮負值。要小心：**不是每一類都這樣**——三暫存器形式的 r_D 佔一整個 octet（min(12, ζ_{ı+2})），單一 immediate 形式沒有暫存器 nibble，load_imm_64 帶固定 8-byte immediate 且不做 sign extension。你們 code-map 3.11 對應同一套解碼。",
 "trap": "immediate 長度由 skip 決定——編碼器可省略高位零/全 1 位元組。"
},
]
