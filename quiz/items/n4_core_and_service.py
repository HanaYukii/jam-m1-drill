# -*- coding: utf-8 -*-
"""基礎套題 N4：Core 與 Service。只考主幹。"""

ITEMS = [
 {
  "id": "n4-what-is-a-service",
  "ch": "N4", "section": "§9 Service Accounts", "gpRef": "§9",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "service"],
  "stem": "What is a service in JAM?",
  "stemZh": "JAM 裡的 service 是什麼？",
  "options": [
   "An account holding code, storage and a balance, whose code defines what happens to it when work is done for it on a core",
   "A long-running process that a validator starts on request and keeps alive between blocks so that it can hold state in memory",
   "A registered chain that rents core time from JAM and keeps its own separate state, much as a parachain rents a slot",
   "A library of functions that other accounts may call, holding no state of its own and existing only while a call is running"
  ],
  "optionsZh": [
   "一個持有程式碼、storage 與餘額的帳戶；當有工作在 core 上為它執行時，它的程式碼決定會發生什麼事",
   "一個長期執行的行程，由 validator 依請求啟動並在區塊之間保持存活，好讓它把狀態留在記憶體裡",
   "一條註冊過的鏈，向 JAM 承租 core time 並保有自己獨立的狀態，就像 parachain 承租一個插槽那樣",
   "一組可供其他帳戶呼叫的函式庫，本身不持有任何狀態，只在呼叫進行期間存在"
  ],
  "answer": 0,
  "explanation": "service 就是 JAM 版的「帳戶」：它有 code、有 storage、有 balance，住在狀態的 δ 分量裡，用一個 u32 的 service index 指涉。它跟 Ethereum 合約帳戶最像，差別在**入口**——service 定義兩個函數：refine（在 core 上執行、無狀態）與 accumulate（在鏈上執行、可寫狀態）。它不是常駐行程（每次執行都從乾淨的 PVM 起跑），也不是獨立的鏈（沒有自己的狀態，全部住在同一個 σ 裡）。",
  "optNotes": [
   "code、storage、balance 加上兩個入口函數，這就是 service 的全部。",
   "每次執行都從乾淨的 PVM 起跑，沒有跨區塊常駐的記憶體。",
   "service 沒有自己的狀態或鏈，全部住在同一份 σ 的 δ 裡。",
   "service 有自己的持久 storage，不是無狀態的函式庫。"
  ],
  "trap": "service ≈ 帳戶；特別的是它有 refine 與 accumulate 兩個入口。"
 },
 {
  "id": "n4-refine-vs-accumulate",
  "ch": "N4", "section": "§4.9; §12; §14", "gpRef": "§4, §12 & §14",
  "difficulty": 1, "kind": "concept", "tags": ["basics", "service"],
  "alsoCh": ["N5"],
  "stem": "A service defines two entry points, refine and accumulate. How do they differ?",
  "stemZh": "一個 service 定義兩個入口：refine 與 accumulate。兩者有什麼不同？",
  "options": [
   "refine runs on a core, sees no chain state and may be given a lot of work; accumulate runs on-chain, may write state, and must therefore stay small",
   "refine runs first to validate the request and accumulate runs second to execute it, so the split is between checking inputs and doing the actual work",
   "refine handles requests from other services and accumulate handles requests from users, so the split follows where the incoming request came from",
   "refine runs when the service is called directly and accumulate runs when it receives a transfer, so the split follows how the service was reached"
  ],
  "optionsZh": [
   "refine 在 core 上執行、看不到鏈上狀態、可以承接大量工作；accumulate 在鏈上執行、可以寫狀態，因此必須維持很小",
   "refine 先執行以驗證請求、accumulate 後執行以實際處理，所以分界是「檢查輸入」與「做事」之間",
   "refine 處理來自其他 service 的請求、accumulate 處理來自使用者的請求，分界跟著請求的來源走",
   "refine 在 service 被直接呼叫時執行、accumulate 在它收到轉帳時執行，分界跟著 service 被觸及的方式走"
  ],
  "answer": 0,
  "explanation": "這是整個 JAM 架構落到 service 層的樣子。**refine**：在 core 上由少數 guarantor 執行，**看不到鏈上狀態**，可以吃大量輸入、跑很久，但只能吐出一個小的結果（work-digest）。**accumulate**：在鏈上執行，**每個節點都會跑**，所以必須便宜；它可以讀寫自己的 storage、轉帳、建立新 service。記法是「refine 做重活但不能碰狀態，accumulate 能碰狀態但必須很輕」——這個限制不是任意的，而是「少數人跑 vs 全體跑」的直接後果。",
  "optNotes": [
   "無狀態的重活 vs 能寫狀態的輕活，正好對應 in-core 與 on-chain。",
   "兩者不是「先檢查後執行」；refine 就是在做真正的計算。",
   "請求來源不影響走哪個入口；work-package 一律先 refine 再 accumulate。",
   "收到轉帳的 service 走的也是 accumulate，沒有獨立的轉帳入口（0.7.1 起併入）。"
  ],
  "trap": "refine 重但不能寫狀態；accumulate 能寫狀態但必須輕。"
 },
 {
  "id": "n4-why-refine-stateless",
  "ch": "N4", "section": "§14; §17", "gpRef": "§14 & §17",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "refine", "audit"],
  "alsoCh": ["N6"],
  "stem": "Why is refine forbidden from reading the chain state?",
  "stemZh": "為什麼 refine 被禁止讀取鏈上狀態？",
  "options": [
   "So that an auditor can re-run it later from the work-package alone and expect the identical result, without having to reconstruct the state as it was at that moment",
   "So that a work-package can be executed by any validator without first synchronizing the chain, which is what allows guarantors to be chosen at random",
   "So that two work-packages on different cores can never conflict, since without state access neither can observe or disturb what the other is doing",
   "So that the refine step stays cheap enough to be metered by a simple instruction count rather than by the full gas model used on-chain"
  ],
  "optionsZh": [
   "好讓 auditor 事後能只憑 work-package 重跑一次並期待得到完全相同的結果，而不必重建當時那一刻的狀態",
   "好讓任何 validator 不必先同步鏈就能執行 work-package，這正是 guarantor 能被隨機選出的原因",
   "好讓不同 core 上的兩份 work-package 永遠不會衝突，因為沒有狀態存取，誰也觀察不到或干擾不了對方",
   "好讓 refine 這一步便宜到可以用單純的指令計數來計量，而不必用鏈上那套完整的 gas 模型"
  ],
  "answer": 0,
  "explanation": "**核心理由是可稽核性。** JAM 的安全論證是「少數人執行、但任何人都能重跑檢查」。如果 refine 能讀狀態，auditor 想重跑就必須先重建「當時那一刻」的完整狀態——那既昂貴又容易有歧義（哪一刻？哪個分叉？）。禁止讀狀態之後，refine 的輸入就完全由 work-package 本身決定：同樣的 package 永遠得到同樣的結果，重跑變成一件確定且便宜的事。這也是為什麼 import segment 必須明確宣告——所有輸入都要寫在 package 裡，不能臨時去撈。",
  "optNotes": [
   "重跑必須只依賴 work-package，這是整個稽核機制成立的前提。",
   "guarantor 仍然是完整節點；隨機選人跟能不能讀狀態無關。",
   "不同 core 之間的隔離來自各自獨立的 package，不是因為禁止讀狀態。",
   "refine 一樣用 gas 計量，而且預算（G_R）比 accumulate 大得多。"
  ],
  "trap": "無狀態是為了讓「重跑」變成確定的事——稽核靠它。"
 },
 {
  "id": "n4-service-code",
  "ch": "N4", "section": "§9.2 Preimage Lookups", "gpRef": "§9",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "service", "preimage"],
  "stem": "A service account stores a code hash, not the code itself. How does the code actually become available to run?",
  "stemZh": "service 帳戶存的是 code hash 而不是程式碼本身。程式碼實際上是怎麼變成可執行的？",
  "options": [
   "Someone supplies the matching blob through the preimages extrinsic, after the service has requested that hash, and it is then stored and looked up by hash",
   "The code is uploaded when the service is created and kept in the account itself, with the hash retained afterwards only as an integrity check",
   "The code is fetched from a peer over the network whenever a core needs it, so it is never part of the state and never needs to be supplied on-chain",
   "The code is reconstructed from the erasure-coded shards held by assurers, which is why enough of them must be online before a service can run"
  ],
  "optionsZh": [
   "在 service 請求過那個 hash 之後，由某人透過 preimages extrinsic 提供對應的 blob；之後它就被保存下來、依 hash 查找",
   "程式碼在 service 建立時就上傳並保存在帳戶本身，hash 只是事後留著當作完整性檢查",
   "每當某個 core 需要時就從對等節點透過網路抓取，所以它從不屬於狀態、也不需要在鏈上被提供",
   "程式碼由 assurer 持有的 erasure-coded 碎片重建，這也是為什麼必須有足夠多的 assurer 在線，service 才能執行"
  ],
  "answer": 0,
  "explanation": "JAM 的資料模型把「請求」與「提供」分開。service 先用 `solicit` 宣告「我要 hash h、長度 z 的那份 blob」，這一刻就開始付押金（footprint 算的是 requests 而不是已提供的 preimage，防止免費占位）。之後任何人都可以透過 **E_P（preimages extrinsic）** 把符合的 blob 送上鏈；系統驗證雜湊相符後存起來，service 就能依 hash 查到它。code 只是這個機制的一個用途——同一套 preimage 機制也用來提供 refine 需要的其他資料。",
  "optNotes": [
   "先 solicit 再由 E_P 提供，這是 JAM 統一的 preimage 機制，code 只是其中一種用途。",
   "帳戶存的是 hash；blob 存在另一個字典裡，兩者分開是為了讓計價與生命週期可控。",
   "程式碼是狀態的一部分、必須上鏈提供，否則不同節點會執行到不同的東西。",
   "erasure coding 用於 work-package 的資料可得性，與 service 的程式碼無關。"
  ],
  "trap": "solicit（請求、開始付押金）→ E_P（提供）→ 依 hash 查找。"
 },
 {
  "id": "n4-threshold-balance",
  "ch": "N4", "section": "§9.3", "gpRef": "§9",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "economics"],
  "stem": "A service's balance must stay above a threshold that grows with how much it stores. What is that rule preventing?",
  "stemZh": "一個 service 的餘額必須高於一個隨其儲存量成長的門檻。這條規則在防什麼？",
  "options": [
   "A service occupying state that every validator must keep forever while holding nothing at stake against that ongoing cost",
   "A service spending its balance faster than it earns, which would leave it unable to pay the gas for its own accumulate step",
   "A service being created by an attacker purely to consume service indices, since each new account permanently uses one up",
   "A service transferring its whole balance away in one block, which would make the resulting account impossible to reason about"
  ],
  "optionsZh": [
   "一個 service 佔用著每位 validator 都必須永久保存的狀態，卻沒有為這份持續成本抵押任何東西",
   "一個 service 花錢比賺錢快，最後付不出自己 accumulate 步驟所需的 gas",
   "攻擊者純粹為了消耗 service index 而大量建立 service，因為每個新帳戶都會永久用掉一個編號",
   "一個 service 在單一區塊內把全部餘額轉走，使得剩下的帳戶變得無法推理"
  ],
  "answer": 0,
  "explanation": "狀態是**每個 validator 都要永久保存**的稀缺資源。如果佔用狀態不需要成本，任何人都能無限寫入、把狀態撐爆到沒人跑得動節點。門檻餘額 a_t 的作法是：依這個帳戶的 footprint（幾筆資料、多少位元組）算出一個最低餘額，帳戶必須一直維持在它之上——等於為佔用的空間押了一筆錢。想少押就得少存。這也是為什麼 `transfer` 在扣款後會檢查自身門檻：不能靠轉帳把錢掏空、留下沒有擔保的狀態。",
  "optNotes": [
   "狀態要每個 validator 永久保存，押金是為這份持續成本提供擔保。",
   "gas 不足只會讓那次 accumulate 失敗，不需要用餘額門檻來防。",
   "service index 是 u32，數量不是稀缺資源；真正稀缺的是狀態空間。",
   "轉帳確實受門檻限制，但那是這條規則的結果而不是它的目的。"
  ],
  "trap": "押金對應的是「佔用狀態」這件事，不是花費或編號。"
 },
 {
  "id": "n4-privileges-basic",
  "ch": "N4", "section": "§9.4 Privileges", "gpRef": "§9",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "privileges"],
  "stem": "A few service indices are recorded in the state as privileged. What does that privilege amount to?",
  "stemZh": "狀態裡記錄了少數幾個具有特權的 service index。這個特權具體是什麼？",
  "options": [
   "The right to change protocol-level settings such as which authorizers a core will accept or who the next validators will be, exercised through host calls during accumulate",
   "The right to bypass the gas model, so a privileged service may run for as long as its work needs without having its accumulate step metered, throttled or cut short",
   "The right to read and write the storage belonging to any other service, which is how system services keep the rest of the state consistent across a protocol upgrade",
   "The right to author blocks out of turn, so that a privileged service can push an urgent change into the chain immediately rather than waiting for a slot of its own"
  ],
  "optionsZh": [
   "有權變更協定層級的設定，例如某個 core 會接受哪些 authorizer、下一批 validator 是誰；透過 accumulate 期間的 host call 行使",
   "有權繞過 gas 模型，因此具特權的 service 想跑多久就跑多久，它的 accumulate 不會被計量、限流或中途截斷",
   "有權讀寫任何其他 service 的 storage，系統 service 就是靠這個在升級後維持其餘狀態的一致",
   "有權不按順序出塊，使具特權的 service 能把緊急變更硬塞進鏈裡，不必等自己的時槽"
  ],
  "answer": 0,
  "explanation": "特權是**改動協定層設定的權力**，而且全部透過 accumulate 期間的 host call 行使。χ 記錄五種：manager（可改特權本身）、每個 core 的 assigner（用 `assign` 改該 core 的 authorizer queue）、delegator（用 `designate` 改下一批 validator）、registrar、以及 always-accumulate 集合。重點是**特權沒有跳出規則之外**：具特權的 service 一樣要跑 accumulate、一樣被計 gas、一樣不能讀別人的 storage。它只是被允許呼叫某些平常會回 HUH 的 host call。",
  "optNotes": [
   "改協定層設定、經由 host call 行使——特權的範圍就這麼大。",
   "特權 service 一樣受 gas 約束，沒有任何豁免。",
   "沒有任何 service 能讀寫別人的 storage，這是 accumulate 隔離性的底線。",
   "出塊資格由 Safrole 決定，與 service 特權完全無關。"
  ],
  "trap": "特權 = 能呼叫某些 host call；不是豁免規則。"
 },
 {
  "id": "n4-core-count-limit",
  "ch": "N4", "section": "§11.3", "gpRef": "§11",
  "difficulty": 2, "kind": "concept", "tags": ["basics", "core"],
  "alsoCh": ["N6"],
  "stem": "The protocol defines many cores, but only some of them can be working at any time. What sets that limit?",
  "stemZh": "協定定義了很多 core，但任一時刻只有其中一部分能運作。是什麼設下這個上限？",
  "options": [
   "Each active core needs three guarantors, so the number of cores that can be busy is the validator count divided by three",
   "Each active core needs a full copy of the state on the machines assigned to it, so the limit is how much state a validator can store",
   "Each active core consumes one entry of the authorizer pool per block, so the limit is the pool size of eight multiplied by the number of blocks",
   "Each active core must be assured by every validator, so the limit is how many assurance signatures will fit inside one block's extrinsic"
  ],
  "optionsZh": [
   "每個運作中的 core 需要三名 guarantor，所以能同時忙碌的 core 數就是 validator 數除以三",
   "每個運作中的 core 需要被指派的機器上有一份完整狀態，所以上限取決於一位 validator 能存多少狀態",
   "每個運作中的 core 每塊消耗一個 authorizer pool 項目，所以上限是 pool 大小 8 乘上區塊數",
   "每個運作中的 core 必須被每一位 validator 背書，所以上限是一個區塊的 extrinsic 能容納多少背書簽章"
  ],
  "answer": 0,
  "explanation": "**上限是 |κ′| / 3**：每個運作中的 core 要指派三名 guarantor（三個人各自執行同一份工作再互相比對，才有意義），validator 只有 |κ′| 位，所以最多 |κ′|/3 個 core 能同時有工作。這也是為什麼 §6 規定 validator 數必須是 3 的倍數（𝕍 = {3c | c ∈ N_{2…C+1}}）。full 設定下 |κ| = 1023 → 341 個 core；tiny 設定 |κ| = 6 → 只有 2 個。所以「core 數」在協定裡是 C = 341 這個常數，但**實際能動的**由當下的 validator 數決定。",
  "optNotes": [
   "三名 guarantor 一個 core，|κ′|/3 就是同時能運作的上限。",
   "guarantor 是完整節點本來就有狀態，狀態容量不是這裡的限制。",
   "authorizer pool 管的是「可接受哪些工作」，與能開幾個 core 無關。",
   "assurance 不需要每位 validator 都給，門檻是超過 2/3。"
  ],
  "trap": "C = 341 是協定常數；真正能動的 core 數是 |κ′|/3。"
 },
 {
  "id": "n4-services-dont-call-directly",
  "ch": "N4", "section": "§12.4 Deferred Transfers", "gpRef": "§12",
  "difficulty": 2, "kind": "rationale", "tags": ["basics", "service"],
  "stem": "One service wants to send value and a message to another. It cannot simply call into that service and wait for a reply. Why not?",
  "stemZh": "一個 service 想送一筆錢和一則訊息給另一個 service。它不能直接呼叫對方並等待回覆。為什麼？",
  "options": [
   "Because a synchronous call would let services re-enter each other to arbitrary depth, which would make gas impossible to budget and results impossible to reproduce",
   "Because the two services may be accumulated on different cores within the same block, and a call reaching across cores would require the two of them to share memory",
   "Because the receiving service may not exist yet at the moment of the call, and the protocol offers no way to check whether an index resolves during accumulate",
   "Because a reply would have to be signed by the receiving service, and a service holds no key material of its own with which it could sign anything at all"
  ],
  "optionsZh": [
   "因為同步呼叫會讓 service 之間以任意深度互相重入，使 gas 無法預先編列、結果也無法重現",
   "因為兩個 service 可能在同一個區塊裡於不同的 core 上被 accumulate，而跨越 core 的呼叫會要求它們兩者共用記憶體",
   "因為接收方在呼叫的當下可能還不存在，而協定在 accumulate 期間無法檢查一個 service 是否存在",
   "因為回覆必須由接收方簽署，而 service 並不持有任何可以拿來簽名的金鑰"
  ],
  "answer": 0,
  "explanation": "JAM 用的是 **deferred transfer**：`transfer` 只是把 (來源, 目的, 金額, memo, gas) 附加到一個序列裡並立刻從發送方扣款，接收方要到**下一輪** accumulate 才收到並執行自己的處理。理由是**確定性與計價**：如果呼叫是同步的，A 呼叫 B、B 又呼叫 A，重入深度沒有上限，那麼「這次 accumulate 要花多少 gas」在執行前就無法估算，而 accumulate 是每個節點都要跑的，預算失控等於整條鏈失控。代價是收款方不存在時那筆轉帳會被丟棄，但錢已經扣了——所以呼叫方要自己確認目標存在。",
  "optNotes": [
   "同步呼叫會帶來無上限的重入，gas 預算與結果重現性都會失控。",
   "accumulate 是在鏈上執行的，不分 core，也不存在跨 core 記憶體的問題。",
   "accumulate 查得到 service 是否存在（不存在會回 WHO），所以這不是理由。",
   "service 之間的呼叫不需要簽章，權限由協定規則而非簽名決定。"
  ],
  "trap": "延後轉帳換來的是「gas 可預估、結果可重現」；代價是要自己確認目標存在。"
 },
]
