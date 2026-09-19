# -*- coding: utf-8 -*-
# 三個系列：時機（哪個時間點讀哪個 state 版本、為什麼）、對比（Safrole / JAM 與舊 Polkadot）、設計（GP 明說或可推得的理由）。
# 不考實作細節。對 BABE 的描述來自 Polkadot 公開文件，詳解裡標明哪些是 GP 原文、哪些是對照知識。
ITEMS = [
{
 "id": "d2-kappa-vs-kappa-prime-readers",
 "lens": "時機",
 "alsoCh": [
  "11",
  "10"
 ],
 "ch": "6",
 "section": "6.2; 11.2–11.3; 10.2",
 "gpRef": "eq. 6.14, eq. 11.14 (assurance sig), eq. 11.17 (2/3|κ|), eq. 11.20 (M over κ′), eq. 6.16 (seal), §10.2 (K(a))",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["validator set", "prior/posterior"],
 "stemZh": "同一個 block 裡，有些檢查讀 prior 的 κ，有些讀 posterior 的 κ′。哪些讀哪個？為什麼要分？",
 "optionsZh": [
  "讀 κ：assurance 簽章、2/3·|κ| 門檻、當前 epoch 的 verdict 判定。讀 κ′：seal 與 H_I 上界、guarantor 指派 M、|κ′|/3 的 core 上界。assurance 與 verdict 背書的是這個 block 之前發生的事，用當時的集合；seal 與 guarantee 是這個 block 自己的行為，用它裝上的集合",
  "全部讀 κ′：eq. 6.14 的輪替是 state transition 的第一步，之後所有檢查看到的都是新集合；κ 只在 statistics 章節用來把上個 epoch 的計數對回金鑰，state transition 本身從不引用它",
  "全部讀 κ：κ′ 要等整個 block 的轉移完成才存在，所以 block 內的任何檢查都只能讀 prior 集合；seal 也對 κ 驗，這就是為什麼 epoch 第一個 block 的作者必須來自上個 epoch 的集合",
  "剛好相反：assurance 與 2/3 門檻讀 κ′，因為要對「這個 block 之後仍在職」的人計票；seal 與 guarantor 指派讀 κ，因為 ticket 是上個 epoch 就投好的，作者必須來自投票時的集合，shard 數也跟著 κ"
 ],
 "stem": "Within one block some checks read the prior κ and others the posterior κ′. Which reads which, and why the split?",
 "options": [
  "κ: assurance signatures, the 2/3·|κ| threshold and current-epoch verdict judgments. κ′: the seal and H_I bound, the guarantor assignment M and the |κ′|/3 core bound. Assurances and verdicts attest to what happened before this block, so they use that set; sealing and guaranteeing are this block's own acts, so they use the set it installs",
  "Everything reads κ′: the rotation of eq. 6.14 is the first step of the transition, so every later check sees the new set; κ survives only in the statistics chapter, where last epoch's counters are mapped back to keys, and the state transition itself never refers to it",
  "Everything reads κ: κ′ only exists once the whole block's transition has completed, so no check inside the block can read it; the seal too is verified against κ, which is why the author of an epoch's first block must still come from the previous epoch's set",
  "The other way round: assurances and the 2/3 threshold read κ′, because votes should be counted over those still in office after this block; the seal and the guarantor assignment read κ, because tickets were cast in the previous epoch and the author must come from the set that cast them, and the shard count follows κ too"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 11.13 的簽章與 eq. 11.17 的門檻寫的是未加撇的 κ；eq. 11.20 的 M、eq. 11.28 的 |κ′|/3、eq. 11.31 的 shard 數與 eq. 6.16 的 seal 都用 κ′。",
  "κ 不只在統計出現：assurance 與 availability 門檻明確寫 κ；輪替也不是「第一步」，依賴圖只保證 κ′ 在需要它的檢查之前算好。",
  "κ′ 在同一個 block 內就被 seal、guarantee、shard 數讀取；epoch 第一個 block 的作者正是來自 κ′（= 舊的 γ_P）。",
  "方向反了：assurance 的簽章對 κ 驗、門檻用 |κ|，seal 與 M 用 κ′。"
 ],
 "explanation": "把「誰讀哪個 κ」分成兩組。讀 prior κ 的：eq. 11.13 assurance 簽章「∈ E_{κ[a_v]_e}(X_A ⌢ H(E(H_P, a_f)))」、eq. 11.17 available 門檻「> 2/3 |κ|」、eq. 10.4 verdict 的 K(a) 在 a = ⌊τ/E⌋ 時取 κ。讀 posterior κ′ 的：eq. 6.16 seal 的 H_A = κ′[H_I]_b（eq. 5.10 也以 |κ′| 限 H_I）、eq. 11.20 指派 M = (P(|κ′|, η′_2, τ′), Φ(κ′))、eq. 11.28 的 w_c < |κ′|/3、eq. 11.31 的 (w_s)_v = |κ′|。為什麼分：assurance 背書的是「上個 block 已經在 ρ 裡的 report」，它的 shard 是依當時的集合大小切的，verdict 判的是過去的 report，所以都對「當時」的集合驗；seal 是這個 block 的作者身分、guarantee 是這個 block 新收的工作，都應該對「這個 block 裝上去的」集合驗。副作用一：epoch 第一個 block 的 seal 只能對 κ′ 驗，因為它的作者是舊 γ_P 裡的人（本 block 剛升成 κ′）。副作用二：eq. 11.18 在 |κ| ≠ |κ′| 時把 ρ‡ 全清，因為舊 report 的 shard 數對不上新集合。",
 "trap": "口訣：背書與判決看「當時」（κ），出塊與擔保看「現在」（κ′）。"
},
{
 "id": "d2-eta-four-slots-consumers",
 "lens": "時機",
 "ch": "6",
 "section": "6.4 Entropy",
 "gpRef": "eq. 6.22 and the §6.4 entropy update, eq. 6.16, eq. 6.27, eq. 6.30, eq. 11.20",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["entropy", "timeslot"],
 "stemZh": "η 有四格。每一格各是誰在讀？為什麼「正在累積」的 η_0 從來沒有任何抽籤直接拿來用？",
 "optionsZh": [
  "η′_0 每個 block 混入 Y(H_V)，只當累積器；換檔時三格往後推。η′_2 給 ticket context、fallback F、guarantor 洗牌 P；η′_3 給 seal 驗證與跨 epoch 的 M*。η_0 不直接用，因為它每個 block 都在變，比賽用的隨機數必須在比賽開始前凍結",
  "η′_0 每個 block 混入 Y(H_V)，同時直接當 seal 的 context；η′_1 給 ticket、η′_2 給 fallback、η′_3 給 guarantor 洗牌。四格各有一個消費者，是為了讓四種抽籤互不相關；η_0 沒有人不用，seal 用的就是它，只是 GP 寫成 η′_0",
  "四格是四個獨立的 VRF 輸出：η_0 來自 seal、η_1 來自 entropy signature、η_2 來自 ticket、η_3 來自 audit 的 VRF。它們不輪替，各自每個 block 更新；η_0 沒被抽籤用是因為 seal 的輸出已經被 i_y 綁死，不能再拿來當隨機源",
  "只有 η′_0 與 η′_1 有人讀：η′_0 給 seal、η′_1 給 ticket、fallback 與 guarantor 洗牌；η′_2 與 η′_3 只是歷史備份，供 audit 在幾個 epoch 後重跑時對照。η_0 當然有被用，就是 seal 那一路"
 ],
 "stem": "η has four slots. Who reads each one, and why does no lottery ever consume the live accumulator η_0 directly?",
 "options": [
  "η′_0 absorbs Y(H_V) every block and is only the accumulator; the three history slots shift at an epoch change. η′_2 feeds the ticket context, the fallback F and the guarantor shuffle P; η′_3 feeds seal verification and the cross-epoch M*. η_0 is never used directly because it changes every block, and a contest's randomness must be frozen before the contest opens",
  "η′_0 absorbs Y(H_V) every block and is also used directly as the seal's context; η′_1 serves tickets, η′_2 the fallback and η′_3 the guarantor shuffle. One consumer per slot keeps the four lotteries independent; η_0 is certainly used — the seal uses it, the GP merely writes it as η′_0",
  "The four slots are four independent VRF outputs: η_0 from the seal, η_1 from the entropy signature, η_2 from tickets and η_3 from the audit VRF. They do not rotate but are each refreshed every block; η_0 is kept away from lotteries because the seal's output is already pinned by i_y and cannot double as a random source",
  "Only η′_0 and η′_1 have readers: η′_0 for the seal, η′_1 for tickets, the fallback and the guarantor shuffle; η′_2 and η′_3 are historical backups consulted by auditors replaying a block epochs later. η_0 is of course used — that is the seal's path"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 6.22 η′_0 = H(η_0 ⌢ Y(H_V))、eq. 6.23 輪替、eq. 6.30 ticket 用 η′_2、eq. 6.27 fallback 用 η′_2、eq. 11.20 P 用 η′_2、eq. 6.16 seal 用 η′_3、eq. 11.23 M* 用 η′_3。",
  "seal 用 η′_3 不是 η′_0；四格不是四個獨立消費者，而是同一個累積器的四個時間快照。",
  "η 只有一個來源（H_V 的 VRF 輸出），沒有四個；η_1–η_3 不每個 block 更新，只在 epoch 換檔時輪替。",
  "η′_2 與 η′_3 是活躍的讀者，不是備份；η′_1 沒有任何協定規則讀它，它只是「等下個 epoch 變成 η′_2」的中繼。"
 ],
 "explanation": "§6.4 原文：「In addition to the entropy accumulator η_0, we retain three additional historical values of the accumulator at the point of each of the three most recently ended epochs, η_1, η_2 and η_3. The second-oldest of these η_2 is utilized to help ensure future entropy is unbiased… and seed the fallback slot-sealer generation function… The oldest is used to regenerate this randomness when verifying the seal.」逐格：η′_0 = H(η_0 ⌢ Y(H_V))（eq. 6.22）每個 block 變一次；eq. 6.23 在 e′ > e 時 (η′_1, η′_2, η′_3) = (η_0, η_1, η_2)。讀者：η′_2 → ticket context X_T ⌢ η′_2 ⧺ r（eq. 6.30）、fallback F(η′_2, κ′)（eq. 6.27）、guarantor 洗牌 P(|κ′|, η′_2, τ′)（eq. 11.20）；η′_3 → seal context X_T ⌢ η′_3 ⧺ i_e（eq. 6.16）、M* 的 P(|λ′|, η′_3, …)（eq. 11.23）；η′_1 沒有直接讀者，它是「下個 epoch 的 η′_2」。為什麼 η_0 不能直接用：它每個 block 都被當前作者的 VRF 更新，若拿它當 ticket 或 seal 的 context，作者出塊的當下就在改自己要被驗證的隨機數，而且驗證者在不同時間點會看到不同值。所以所有抽籤都用「已經結束的 epoch 末」的快照——固定、公開、人人可重現。",
 "trap": "η_0 是「正在累積」的，永遠不當籤；抽籤只用凍結過的 η_2 / η_3。"
},
{
 "id": "d2-delta-versions-in-one-block",
 "lens": "時機",
 "alsoCh": [
  "11",
  "12"
 ],
 "ch": "9",
 "section": "4.1 dependency graph; 11.4; 12.4",
 "gpRef": "eq. 4.16 (δ‡), eq. 4.18 (δ′), eq. 11.45 (δ[d_s]_c), §11.4 gas floor, §12.4 preimage integration",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["service", "prior/posterior"],
 "stemZh": "service 狀態在一個 block 裡有三個版本：δ、δ‡、δ′。哪條規則讀哪個？為什麼 E_P 的「可提供」判定是對 prior 的 δ 做、而不是對 accumulate 之後的 δ‡？",
 "optionsZh": [
  "E_G 的檢查（gas 下限 δ[d_s]_g、code hash δ[s]_c）讀 prior δ；accumulate 把 prior δ 變成 δ‡；E_P 的可提供判定也對 prior δ，之後才併進 δ‡ 得 δ′，accumulate 途中變無用的 preimage 略過。對 prior 判定，出塊者不必先跑 accumulate 就知道 E_P 合法",
  "E_G 的檢查讀 δ‡，因為 guarantee 的 gas 下限應該反映 accumulate 之後的最新 a_g；E_P 對 δ′ 判定，因為 preimage 是最後才併入的；accumulate 讀的是 δ 但寫回 δ′。三個版本其實只有兩個時間點：block 開始與 block 結束，依賴圖畫的正是這兩點",
  "三個版本讀者相同：所有 §11 的檢查、accumulate 與 E_P 都對 prior δ 判定，δ‡ 與 δ′ 只是中間結果的記號，任何規則都不會去讀它們；區分它們純粹是為了讓依賴圖畫得出來",
  "E_P 對 δ‡ 判定：因為 service 可能在這個 block 的 accumulate 裡才 solicit 這個 preimage，對 prior δ 判會拒絕掉合法的提供；E_G 的檢查也讀 δ‡，好讓同一個 block 裡剛升級的 code hash 立刻生效"
 ],
 "stem": "Service state appears in one block as δ, δ‡ and δ′. Which rule reads which, and why is E_P's 'providable' test made against the prior δ rather than against the post-accumulation δ‡?",
 "options": [
  "The E_G checks (gas floor δ[d_s]_g, code hash δ[s]_c) read the prior δ; accumulate turns the prior δ into δ‡; E_P's providable test is also against the prior δ, and only then is it folded into δ‡ to give δ′, skipping preimages accumulation made useless. Judging against the prior state lets the author know E_P is valid without running accumulate first",
  "The E_G checks read δ‡, because a guarantee's gas floor should reflect the freshest a_g after accumulation; E_P is judged against δ′ since preimages are the last thing folded in; accumulate reads δ but writes δ′. The three versions really amount to two moments only: block start and block end, exactly as the dependency graph draws them",
  "All three have the same readers: every §11 check, accumulate and E_P are judged against the prior δ, while δ‡ and δ′ are mere labels for intermediate results that no rule ever reads; the distinction exists purely so that the dependency graph can be drawn",
  "E_P is judged against δ‡: a service may solicit the preimage only during this block's accumulate, and judging against the prior δ would reject a legitimate supply; the E_G checks also read δ‡ so that a code hash upgraded in this very block takes effect immediately"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 11.45 與 §11.4 的 gas 下限寫的是未加撇的 δ；依賴圖 δ‡ ≺ (…, δ, …)、δ′ ≺ (E_P, δ‡, τ′)；§12.4「must have been solicited by a service but not yet provided in the prior state」。",
  "E_G 的檢查在 accumulate 之前跑，讀不到 δ‡；E_P 對 prior 判定、對 δ‡ 併入，不是對 δ′ 判定。",
  "δ‡ 與 δ′ 確實被讀：δ′ 是 E_P 併入的對象、也是下個 block 的 prior；δ‡ 是 preimage integration 的輸入。",
  "GP 明說 providable 對 prior 判定；同一個 block 內 solicit 的 preimage 下個 block 才能提供。code hash 也對 prior δ 檢查（eq. 11.45），升級要等下個 block。"
 ],
 "explanation": "三個版本的位置由 §4 依賴圖固定：δ‡ 是 accumulation 的輸出（δ‡ ≺ (R*, …, δ, …)），δ′ ≺ (E_P, δ‡, τ′)。讀 prior δ 的規則：§11.4 要求每個 digest 的 d_g ≥ δ[d_s]_g，eq. 11.45 要求 d_c = δ[d_s]_c，兩者都在 E_G 驗證時對 prior 檢查，因為 E_G 驗證先於 accumulate（這也是 ch11-code-hash-prediction 那題的根據：service 在 package 建好後升級 code，guarantee 會被拒）。E_P 的判定，§12.4 原文：「The data must have been solicited by a service but not yet provided in the prior state.」然後「We disregard, without prejudice, any preimages which due to the effects of accumulation are no longer useful」，也就是對 prior 判合法、併入 δ‡ 時再看還有沒有用（例如 service 在這個 block 的 accumulate 裡 forget 了它）。為什麼不對 δ‡ 判：block 的有效性必須在出塊時就能確定，出塊者組 E_P 時 accumulate 還沒跑；若合法性取決於 accumulate 的結果，作者得先執行整個 block 才知道自己的 E_P 會不會讓 block 無效。「對 prior 判定、對 posterior 併入、無用者略過」這個模式在 GP 裡反覆出現。",
 "trap": "口訣：判定看 prior，併入看 ‡，沒用就丟。同一 block 的 solicit 要下一 block 才能 provide。"
},
{
 "id": "d2-beta-dagger-anchor-why",
 "lens": "時機",
 "alsoCh": [
  "11"
 ],
 "ch": "7",
 "section": "7.1; 11.2 (anchor)",
 "gpRef": "eq. 7.5 (β†), eq. 4.6, eq. 11.36, eq. 4.17 (β′ ≺ θ′)",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["lookup-anchor", "recent history"],
 "stemZh": "E_G 的 anchor 檢查（eq. 11.36）拿 refinement context 去對 β†，既不是 β 也不是 β′。為什麼不能是 β？為什麼不能是 β′？",
 "optionsZh": [
  "不能是 β：最新一筆的 state root 還是 H_0，anchor 在父 block 的 report 會對不上，β† 補上 H_R 才對得上。不能是 β′：它要等 accumulate 產出 θ′ 才存在，而且含這個 block 自己，report 不可能 anchor 在收納它的 block 上",
  "不能是 β：β 只有 7 筆，H = 8 的第八筆要在這個 block 追加後才存在，用 β 會少一個可用的 anchor。不能是 β′：β′ 的 state root 欄位全部是 H_0，因為 posterior root 要下個 block 才知道，用它會讓所有 anchor 都對不上",
  "其實三者都可以：anchor 只比對 header hash，state root 欄位在 0.8.0 已改為選填；GP 寫 β† 只是為了讓依賴圖上 β† 這個節點有用途，實作用 β 或 β′ 都會得到相同的 state root",
  "不能是 β：β 是上個 block 的 posterior，可能已經被 fork 掉的 block 覆蓋。不能是 β′：β′ 尚未 Merklize，state root 還沒算出來。β† 是唯一經過 GRANDPA 定案的版本，所以 anchor 必須對它"
 ],
 "stem": "The anchor check for E_G (eq. 11.36) compares the refinement context against β†, neither β nor β′. Why not β, and why not β′?",
 "options": [
  "Not β: its newest entry still holds H_0 as state root, so a report anchored on the parent would fail the state-root match; β† writes H_R in and then it matches. Not β′: it exists only after accumulate has produced θ′, and it would contain this block itself, which a report cannot anchor on",
  "Not β: it holds only seven entries, the eighth of H = 8 appears only after this block appends, so using β would lose one usable anchor. Not β′: its state-root fields are all H_0 because posterior roots are only known a block later, so every anchor would fail against it",
  "In fact any of the three would do: the anchor compares only the header hash, the state-root field became optional in 0.8.0, and the GP writes β† merely so that the β† node in the dependency graph has a purpose; an implementation reading β or β′ gets the same state root",
  "Not β: it is the previous block's posterior and may already have been overwritten by a forked-out block. Not β′: it has not yet been Merklized, so its state root is unknown. β† is the only version finalized by GRANDPA, which is why anchors must be checked against it"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 7.5 β† = β 但最新項目的 s 改成 H_R；eq. 11.36 對 β† 比 (a, n, s, b)；依賴圖 β′ ≺ (H, E_G, β†, θ′) 表示 β′ 要等 accumulate。",
  "β 一直維持 8 筆（→^H 截斷），沒有「少一筆」的問題；β′ 只有最新一筆是 H_0，其他都已補正。",
  "eq. 11.36 明確比對 state root s 與 super-peak b，不只 header hash；state root 沒有改成選填。",
  "β 是 state 的一部分，跟 fork 與 GRANDPA 無關；β† 也不是「定案版本」，只是把父 block 的 root 補上。"
 ],
 "explanation": "三個版本各在依賴圖的不同位置：β† ≺ (H, β)（eq. 7.5：把 header 的 H_R 寫進 β 最新一筆的 state root 欄位，因為 block N 結束時 N 自己的 posterior root 還不知道，先填 H_0）；β′ ≺ (H, E_G, β†, θ′)（要等 accumulate 產出 θ′ 才能算 super-peak、追加新項目）。eq. 11.36 要求 refinement context 的 (a, n, s, b) 等於 β† 某一筆的 (header hash, timeslot, state root, super-peak)。對 β 不行，因為一份 anchor 在父 block 上的 report——這是最常見的情形，builder 總是對最新的 block 建 package——它的 s 是父 block 的真實 posterior root，而 β 裡那格還是 H_0。對 β′ 不行有兩個理由：一是時序，β′ 在 accumulate 之後才存在，而 E_G 驗證在 accumulate 之前；二是語意，β′ 含這個 block 自己的項目，若允許對它 anchor，等於允許一份 report 宣稱自己是對「收納它的那個 block」算的，這在因果上不可能。所以 β† 是唯一「父 block 的 root 已補上、但這個 block 還沒加進去」的版本。這也是 c3-ch07-dagger-before-append 那題的另一面：先 append 再 backfill 會把 H_R 寫錯格。",
 "trap": "β† = 「父 block 補完整、本 block 還沒進」的那一刻，正好是 anchor 該看的時間點。"
},
{
 "id": "d2-tau-vs-tau-prime-rules",
 "lens": "時機",
 "alsoCh": [
  "6",
  "10"
 ],
 "ch": "5",
 "section": "4.1; 6.3; 10.2; 11.3",
 "gpRef": "§4.1 (τ′ ≺ H), §6.3 (e, m, e′, m′), eq. 6.25, eq. 10.2, eq. 11.18, eq. 11.28",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["timeslot", "prior/posterior"],
 "stemZh": "τ 是上個 block 的 timeslot，τ′ = H_T 是這個 block 的。哪些規則刻意用 prior 的 τ、而不是 H_T？背後的原則是什麼？",
 "optionsZh": [
  "用 τ 的：epoch 換檔判定 e = ⌊τ/E⌋ 對 e′ = ⌊H_T/E⌋、ticket 制條件 m = τ mod E ≥ Y、verdict 的 epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}。用 H_T 的：guarantee 的 slot 視窗、逾時、queue 索引。回頭看已發生的事讀 τ，看這個 block 此刻讀 H_T",
  "用 τ 的只有 statistics：π 的 epoch 換檔比較 ⌊τ/E⌋ 與 ⌊τ′/E⌋。其他規則全部用 H_T，包括 Safrole 的 e′ > e 判定也是拿 H_T 與 H_T − 1 比，因為 GP 假設 block 是連續的、τ′ = τ + 1",
  "τ 與 H_T 在所有規則裡可以互換，因為合法 block 的 H_T 一定大於 τ，任何以 τ 寫的條件改寫成 H_T − 1 就等價；GP 混用兩者只是各章作者不同，實作統一用 H_T 即可，每條規則都這樣改也不影響結果",
  "用 H_T 的只有 header 本身的檢查（H_T > τ、H_T 不在未來）；其他規則一律用 τ，因為 state transition 只能依賴 prior state，H_T 是 extrinsic 資料、不可信，要等 block 被 finalize 後才寫進 τ′"
 ],
 "stem": "τ is the previous block's timeslot; τ′ = H_T is this block's. Which rules deliberately use the prior τ rather than H_T, and what is the principle behind the choice?",
 "options": [
  "Using τ: the epoch-change test e = ⌊τ/E⌋ vs e′ = ⌊H_T/E⌋, the ticket-regime condition m = τ mod E ≥ Y, and the verdict epoch index a ∈ {⌊τ/E⌋, ⌊τ/E⌋−1}. Using H_T: the guarantee slot window, the timeout and the queue index. Rules that look back at what has happened read τ; rules about this block's moment read H_T",
  "Only statistics use τ: π's epoch rollover compares ⌊τ/E⌋ with ⌊τ′/E⌋. Every other rule uses H_T, including Safrole's e′ > e test, which compares H_T with H_T − 1 because the GP assumes consecutive blocks with τ′ = τ + 1",
  "τ and H_T are interchangeable in every rule, since a valid block's H_T always exceeds τ and any condition written with τ can be rewritten with H_T − 1; the GP mixes them only because chapters had different authors, and an implementation may use H_T throughout for every rule without changing any result",
  "Only the header's own checks use H_T (H_T > τ, H_T not in the future); every other rule uses τ, because a state transition may depend only on the prior state and H_T is untrusted extrinsic data that is written into τ′ only once the block is finalized"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 6.10–6.11 定義 e, m 由 τ 導出、e′, m′ 由 H_T 導出；eq. 6.25 用 m ≥ Y；eq. 10.2 用 ⌊τ/E⌋；eq. 11.28 與 11.18 用 τ′ / H_T。",
  "Safrole 的 e′ > e 是拿 ⌊H_T/E⌋ 與 ⌊τ/E⌋ 比；block 不連續，可以跳好幾個 slot 甚至跳 epoch（ch06-skip-epochs-transition）。",
  "block 可以跳 slot，τ′ ≠ τ + 1，所以 τ 與 H_T − 1 不等價；m ≥ Y 用 H_T 改寫會改變語意。",
  "H_T 是 header 欄位、是 state transition 的正常輸入（τ′ ≺ H）；用 τ 的規則是少數且各有理由。"
 ],
 "explanation": "§6.3 先定義兩組量：e = ⌊τ/E⌋、m = τ mod E 來自 prior τ；e′ = ⌊H_T/E⌋、m′ = H_T mod E 來自這個 block。用 τ 的規則各有一句理由：(1) e′ > e 是「這個 block 跨過了 epoch 邊界嗎」，必須拿上個 block 的 epoch 當基準；(2) eq. 6.25 的 m ≥ Y 問的是「上個 block 是否已經在尾段」，也就是 ticket 提交期是否在上個 block 就已關閉——ch06-why-m-ge-Y 那題講過，這保證 γ_A 在本 block 之前就已定案；(3) eq. 10.2 verdict 的 epoch index 只能是 ⌊τ/E⌋ 或再前一個，因為 verdict 判的是「已經上鏈的 report」，以上個 block 的 epoch 為現在。用 H_T 的規則：eq. 11.28 guarantee 的 slot 視窗 R·(⌊τ′/R⌋ − 1) ≤ t ≤ τ′、eq. 11.18 的逾時 H_T ≥ t + U、eq. 8.2 的 φ[c][H_T mod Q]，這些都是「這個 block 此刻該收什麼、該清什麼、該抽哪格」。原則就一句：**回頭看的用 τ，看現在的用 H_T**。而 block 可以跳 slot（甚至跳整個 epoch），所以 τ 與 H_T − 1 不能互換。",
 "trap": "看到 e、m 沒加撇就是 prior；e′、m′ 才是這個 block。"
},
{
 "id": "d2-dependency-checks-which-history",
 "lens": "時機",
 "alsoCh": [
  "12",
  "7"
 ],
 "ch": "11",
 "section": "11.5 (prerequisites); 12.1",
 "gpRef": "eq. 11.42, §12.1 (R^Q, ω, ξ), eq. 7.x (β reported map)",
 "difficulty": 3,
 "kind": "rationale",
 "tags": ["dependency", "guarantee", "recent history"],
 "stemZh": "report 的 prerequisite 會被檢查兩次：guarantee 上鏈時、accumulate 時。兩次各讀哪份歷史（E_G、β 的 reported map、ξ、ω）？為什麼 guarantee 時不能只查 ξ？",
 "optionsZh": [
  "guarantee 時（eq. 11.42）prerequisite 必須在同一個 E_G 或 β 最近 8 個 block 的 reported map 裡，證明它報過。accumulate 時（§12.1）R^Q 與 ω 的依賴對 ξ 消去，證明它做完了。guarantee 時只查 ξ 不夠，因為 prerequisite 通常已報但還沒 available，根本不在 ξ 裡",
  "兩次都讀 ξ：guarantee 時 prerequisite 必須已在 ξ（已 accumulate），accumulate 時再用 ξ 把已滿足的依賴消掉；β 的 reported map 只給 audit 用來找 bundle，ω 只是等 gas 的緩衝區。GP 在 §11.5 寫 β 是 0.7.x 的殘留，0.8.0 的編輯只是忘了刪",
  "guarantee 時讀 ω：prerequisite 必須是 ready queue 裡的某個 report；accumulate 時讀 β，看 prerequisite 是否在最近 8 個 block 被 report 過。ξ 只在 epoch 邊界清理 ω 時用到，不參與任何依賴判定",
  "兩次都讀 β：guarantee 時要求 prerequisite 在 β 裡，accumulate 時再對 β 確認一次；ξ 與 ω 不參與依賴判定，它們是防止重複 accumulate 的去重表。只查 ξ 不行是因為 ξ 只存一個 epoch，太短"
 ],
 "stem": "A report's prerequisites are checked twice: when the guarantee lands on-chain and again at accumulation. Which history does each check read (E_G, β's reported maps, ξ, ω), and why would ξ alone not do at guarantee time?",
 "options": [
  "At guarantee time (eq. 11.42) a prerequisite must be in the same E_G or in β's reported maps of the last 8 blocks, proving it was reported. At accumulation (§12.1) the dependencies of R^Q and ω are struck out against ξ, proving it was accumulated. ξ alone will not do at guarantee time because a prerequisite is usually reported but not yet available, so it is not in ξ",
  "Both checks read ξ: at guarantee time the prerequisite must already be in ξ (accumulated), and at accumulation ξ is used again to strike satisfied dependencies; β's reported maps serve auditors locating bundles and ω is just a buffer waiting for gas. The GP's mention of β in §11.5 is a 0.7.x leftover that the 0.8.0 editors simply forgot to remove",
  "Guarantee time reads ω: the prerequisite must be some report in the ready queue; accumulation reads β to see whether the prerequisite was reported within the last 8 blocks. ξ is consulted only when ω is purged at an epoch boundary and plays no part in dependency decisions",
  "Both checks read β: at guarantee time the prerequisite must be in β, and accumulation confirms against β once more; ξ and ω take no part in dependency decisions, being deduplication tables that prevent double accumulation. ξ alone would not do because it covers only one epoch, which is too short"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 11.42 的集合是 E_G 的 package hash ∪ β 各筆的 p（reported map）；§12.1 的 R^Q = E(…, ξ∪) 與 Q 都對「已 accumulate」的集合消依賴；ch11-prerequisite-window 那題就是 ξ 在 guarantee 時不被查的具體案例。",
  "guarantee 時明確不查 ξ；β 的 reported map 是 §11 的 on-chain 檢查在讀（c3-ch07-reported-map-downstream）；ω 也不是「等 gas」而是等依賴。",
  "ω 是 accumulate 階段的東西，guarantee 時不讀；β 在 accumulate 時不讀。整個對調了。",
  "accumulate 時不讀 β；ξ 與 ω 正是依賴判定的核心。ξ 存一個 epoch 對 accumulate 已足夠，因為依賴在 guarantee 時就被限制在最近 8 個 block 內。"
 ],
 "explanation": "兩個階段問的是兩個不同的問題。**guarantee 階段問「它存在嗎」**：eq. 11.42 要求每個 prerequisite（與 segment-root lookup 的 key）出現在本 block E_G 的 package hash 集合、或 β 最近 H = 8 筆的 reported map p 之中——這證明那份 package 已被 guarantee 上鏈，資料在 DA 系統裡找得到。這時 prerequisite 通常還沒 available（它可能就在同一個 block 或前幾個 block 才被 report），所以還不在 ξ。**accumulate 階段問「它做完了嗎」**：§12.1 把有依賴的 report 放進 R^Q，用 E(…, ξ∪) 消掉已 accumulate 的依賴，剩下的進 ω 排隊，Q 每一輪再用剛完成的集合消一次。這裡 ξ（最近一個 epoch 已 accumulate 的 package hash）才是正確的依據，因為只有真的 accumulate 過的結果才可以被依賴。兩份歷史各證明一件事，缺一不可：β 證「有人做過」，ξ 證「做完了」。設計上這也讓兩個檢查的視窗不同：guarantee 用 8 個 block（要快、要小），accumulate 用一個 epoch（要等得起依賴慢慢完成）。",
 "trap": "guarantee 看 β（報過沒），accumulate 看 ξ（做完沒）。ξ 在 guarantee 時完全不被查。"
},
{
 "id": "d2-designate-to-authoring-lag",
 "lens": "時機",
 "alsoCh": [
  "9",
  "B"
 ],
 "ch": "6",
 "section": "6.2; 9.4 (designate)",
 "gpRef": "eq. 6.14 (§6.2 rotation), eq. 6.30 (ring root γ′_Z over γ_P), §B (designate)",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["validator set", "privileges"],
 "stemZh": "delegator service 在 epoch e 的某個 block 呼叫 designate，把 ι 換成一組新 key。這組 key 最早在哪個 epoch 能封 block？中間經過哪幾步？",
 "optionsZh": [
  "epoch e+2。designate 在本 block 寫入 ι′；e+1 的第一個 block 輪替 γ′_P = Φ(ι)、κ′ = 舊 γ_P，新 key 成為 pending；e+1 期間它們用 γ′_Z（γ_P 的 ring root）投 ticket；e+2 的第一個 block 再輪替 κ′ = γ_P，此時才能 seal",
  "epoch e+1。designate 寫入 ι′ 後，epoch e+1 的第一個 block 直接把 ι 升成 κ′，因為 0.8.0 為了讓集合大小可變，把 pending 這一層拿掉了；新 key 在 e 期間就以 fallback 的身分投 ticket，e+1 一開始就能 seal",
  "epoch e 當下。designate 是 accumulate 裡的 host call，ι′ 在同一個 block 生效並立刻取代 κ′，因為 delegator 是特權 service、它的決定不需要等輪替；下一個 slot 的 seal 就對新 key 驗",
  "epoch e+3。ι → γ_P → κ 各要一個 epoch，再加上新 key 必須先在 λ 待一個 epoch 讓 dispute 有時間追溯它們，所以總共三次輪替；這也是為什麼 state 要保留 λ"
 ],
 "stem": "The delegator service calls designate in some block of epoch e, replacing ι with a new set of keys. In which epoch can those keys first seal a block, and through which steps?",
 "options": [
  "Epoch e+2. designate writes ι′ in this block; the first block of e+1 rotates γ′_P = Φ(ι) and κ′ = the old γ_P, so the new keys are pending; during e+1 they submit tickets under γ′_Z, the ring root over γ_P; the first block of e+2 rotates again, κ′ = γ_P, and only then can they seal",
  "Epoch e+1. Once designate has written ι′, the first block of epoch e+1 promotes ι straight to κ′, because 0.8.0 removed the pending layer to make the set size variable; the new keys already submit tickets during e in the fallback role and can seal from the start of e+1",
  "Epoch e itself. designate is a host call inside accumulate, and ι′ takes effect within the same block, replacing κ′ immediately, because the delegator is a privileged service whose decision need not wait for a rotation; the very next slot's seal is verified against the new keys",
  "Epoch e+3. ι → γ_P → κ takes one epoch per step, plus the new keys must first spend an epoch in λ so that disputes have time to reach back to them, making three rotations in all; this is also why the state keeps λ"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 6.14 每次 e′ > e 做一步 (γ′_P, κ′, λ′) = (Φ(ι), γ_P, κ)；ticket 對 γ′_Z（γ_P 的 ring root）證明，所以 pending 那一個 epoch正是投 ticket 的期間。",
  "0.8.0 沒有拿掉 pending 層，eq. 6.14 仍是三段輪替；ι 裡的 key 在 e 期間不能投 ticket（ring root 不含它們）。",
  "designate 只寫 ι′，κ′ 只在 epoch 換檔時由 γ_P 升上來；沒有任何 host call 能直接改 κ。",
  "λ 是「剛卸任」的集合，不是入職前的等待區；ι → γ_P → κ 只有兩次輪替。"
 ],
 "explanation": "把 eq. 6.14 攤開：在 e′ > e 的 block，(γ′_P, κ′, λ′, γ′_Z) = (Φ(ι), γ_P, κ, z)。也就是每個 epoch 邊界，ι 升成 pending、pending 升成 active、active 退成 previous。designate（§B）只寫 ι′。所以時間線：epoch e 的 block N 呼叫 designate → ι′ 是新 key；epoch e+1 的第一個 block → γ′_P = Φ(ι)（新 key 成為 pending，offender 歸零），κ′ = 舊的 γ_P（不是新 key）；epoch e+1 全程新 key 在 pending，此時 γ′_Z 是對 γ_P 算的 ring root，所以它們可以用 ring-VRF 投 ticket、競爭 e+2 的 slot；epoch e+2 的第一個 block → κ′ = γ_P = 新 key，從這個 block 起（含這個 block，因為 seal 對 κ′ 驗）新 key 才能 seal。為什麼要隔兩層：pending 那一個 epoch 是 ticket 提交期，作者必須在成為 active 之前就投完票，這是 Safrole「作者提前一個 epoch 決定」的必然結果。與 d2-kappa-vs-kappa-prime-readers 對照：第 e+2 個 epoch 的第一個 block，seal 對 κ′ 驗，所以新 key 從那一刻就有效，不用再等一個 block。",
 "trap": "ι 今天寫，下個 epoch 投票，再下個 epoch 出塊。兩次輪替，不是一次也不是三次。"
},
{
 "id": "d2-offender-effect-timing",
 "lens": "時機",
 "alsoCh": [
  "6"
 ],
 "ch": "10",
 "section": "10.4; 6.2 (Φ); 5 (H_O)",
 "gpRef": "§10.3 (culprit/fault conditions, k ∉ ψ_O), eq. 10.14, eq. 10.18 (ψ′_O), eq. 6.14 (Φ), §5 (H_O)",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["dispute", "epoch"],
 "stemZh": "某個 validator 的 Ed25519 key 在 block N 因 culprit 或 fault 進了 ψ′_O。立刻發生什麼？下一次 epoch 換檔時發生什麼？什麼事情在 JAM 協定內永遠不會發生？",
 "optionsZh": [
  "立刻：key 進 ψ′_O 與 H_O，之後指名它的 culprit / fault 被拒（k ∉ ψ_O），被判 bad 的 report 從 ρ 清掉。下次換檔 Φ 把它在 γ′_P 的位置換成全零 key，再下個 epoch 它不能投 ticket、seal、guarantee；在那之前它的 κ 位置照舊。永遠不會：state 自己扣它的餘額",
  "立刻：key 從 κ′ 移除、集合縮小一格，它當前 epoch 剩下的 slot 全部變成 fallback；下次換檔：從 λ′ 也移除，dispute 對它的追溯到此為止。永遠不會：它被列進 H_O，因為 H_O 只列 culprit、不列 fault",
  "立刻：什麼都不變，ψ′_O 只是紀錄；下次換檔：它從 ι、γ_P、κ、λ 四個集合同時移除，並由 registrar 扣除押金；永遠不會：它在同一個 epoch 內再被列為 offender，因為 ψ_O 每個 epoch 清空",
  "立刻：它的 Bandersnatch key 失效，seal 對它的驗證全部失敗，但 Ed25519 簽章仍有效所以還能 guarantee；下次換檔：兩把 key 都從集合移除；永遠不會：它重新進入 ι，因為 designate 會拒絕 ψ_O 裡的 key，之後每次呼叫都拒"
 ],
 "stem": "A validator's Ed25519 key enters ψ′_O in block N via a culprit or fault. What happens immediately, what happens at the next epoch change, and what never happens inside the JAM protocol?",
 "options": [
  "Immediately: the key enters ψ′_O and H_O, later culprits or faults naming it are rejected (k ∉ ψ_O), and a report judged bad is cleared from ρ. At the next epoch change Φ replaces its γ′_P slot with an all-zero key, so an epoch later it can neither ticket, seal nor guarantee; until then its κ slot stands. Never: the state debiting its balance",
  "Immediately: the key is removed from κ′ and the set shrinks by one, its remaining slots this epoch all become fallback; at the next epoch change it is removed from λ′ as well, ending any dispute reaching back to it. Never: being listed in H_O, since H_O lists culprits only, never faults",
  "Immediately: nothing changes, ψ′_O is only a record; at the next epoch change it is removed from ι, γ_P, κ and λ at once and the registrar deducts its deposit; never: being named an offender again in the same epoch, because ψ_O is cleared every epoch",
  "Immediately: its Bandersnatch key is invalidated so every seal verification against it fails, while its Ed25519 signatures stay valid so it can still guarantee; at the next epoch change both keys are removed from the sets; never: re-entering ι, because designate rejects keys found in ψ_O on every later call"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 10.6–10.7 要求 offender key ∉ ψ_O；eq. 10.16 ψ′_O = ψ_O ∪ culprit keys ∪ fault keys；H_O 兩者都列；eq. 6.14 的 Φ 只在換檔時作用於 γ′_P；GP 沒有鏈上 slash（ch10-rationale）。",
  "κ 在 epoch 內不會改變，集合大小也只在換檔時變；H_O 列 culprit 與 fault 兩者的 key。",
  "ψ_O 不清空，是累積的；沒有 registrar 扣押金這回事，GP 沒定義押金。",
  "Φ 換掉的是整個 336-octet 的 key 條目（含 Bandersnatch 與 Ed25519），而且只在換檔時；ι 由 delegator 全權決定，GP 沒有「designate 拒絕 ψ_O」的規則。"
 ],
 "explanation": "分三個時間點。**block N 當下**（§10.4）：eq. 10.16 把 culprit 與 fault 的 key 併進 ψ′_O；H_O 必須恰好列出這些新 offender（eq. 5.x「must contain exactly the keys of all new offenders」）；eq. 10.14 把 report hash ∈ ψ′_B 的 core 從 ρ 清掉。從此 eq. 10.6–10.7 的 k ∉ ψ_O 條件讓同一把 key 不能再被列為 offender——這是去重，不是赦免。**下一次換檔**（eq. 6.14）：γ′_P = Φ(ι)，§6.2 原文「incoming keys belonging to the offenders ψ′_O are replaced with a null key containing only zeroes」。注意 Φ 作用在「進入 pending」那一步，所以 offender 在當前 epoch 的 κ 位置不變，還能 seal 自己剩下的 slot、還能 guarantee；到再下個 epoch（它本來會再成為 active 時）位置變成零 key，簽不出任何有效簽章。**永遠不會**：JAM state 不含任何「扣餘額」的規則，ch10-rationale 那題的重點就是 disputes 系統「不自己 slash」，只把 offender 記在 ψ_O 與 H_O，讓 staking 那個 system service 讀取後處理。設計上這是「協定只記事實、經濟後果交給 service」的一貫立場。",
 "trap": "ψ_O 是立刻、Φ 是換檔、slash 是永遠不在 GP 裡。"
},
{
 "id": "d2-M-vs-Mstar-why",
 "lens": "時機",
 "ch": "11",
 "section": "11.3 Guarantor assignments",
 "gpRef": "eq. 11.20–11.23, eq. 11.28 (slot window)",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["guarantee", "entropy"],
 "stemZh": "guarantee 的 credential 可以對 M 或 M* 驗。為什麼需要 M* 這個「上一個 rotation 的指派」？它又為什麼只在上一個 rotation 落在上個 epoch 時才改用 λ′ 與 η′_3？",
 "optionsZh": [
  "因為 guarantee 可以晚到：eq. 11.28 允許 t 落在上一個 rotation，當時的 guarantor 是那個 rotation 的指派，鏈上必須重算才能驗 credential。上一個 rotation 通常在同一個 epoch，重算只是 τ′ − R、集合與 entropy 不變；跨了 epoch 邊界，當時的集合與 entropy 已變成 λ′ 與 η′_3，M* 才改用它們",
  "因為 audit 要重跑上一個 rotation 的 report：auditor 需要知道當時是誰 guarantee 的，M* 就是給 audit 用的指派表；改用 λ′ 與 η′_3 是因為 audit 最多可以晚兩個 epoch，那時 κ′ 與 η′_2 早已不是當時的值",
  "因為 M 與 M* 是同一個 rotation 的兩種計算方式：M 用 κ′、M* 用 λ′，鏈上兩者都算一次，credential 只要符合其中之一就接受，這樣 epoch 換檔那一個 rotation 裡新舊兩組 validator 都能簽；η′_3 只是為了讓兩者的洗牌結果不同；除了那一個 rotation 之外兩張表永遠一致，只查 M",
  "因為 0.8.0 讓集合大小可變：當 |κ| ≠ |κ′| 時 M 的洗牌結果整個改變，M* 用上個集合 λ′ 重算，讓縮減前指派的 guarantor 簽的 credential 仍然有效；不跨 epoch 時 M* 等於 M，只是保險"
 ],
 "stem": "A guarantee's credential may be verified against M or M*. Why is M*, the previous rotation's assignment, needed at all, and why does it switch to λ′ and η′_3 only when that previous rotation lies in the previous epoch?",
 "options": [
  "Because guarantees may arrive late: eq. 11.28 lets t fall in the previous rotation, whose guarantors were that rotation's assignment, so the chain must recompute it to verify the credential. Usually that rotation is in the same epoch and recomputing just means τ′ − R with the same set and entropy; across an epoch boundary the set and entropy of that time have become λ′ and η′_3, so only then does M* use them",
  "Because audits re-run reports from the previous rotation: an auditor needs to know who guaranteed them, and M* is the assignment table kept for auditing; it switches to λ′ and η′_3 because an audit may run up to two epochs late, by which time κ′ and η′_2 no longer hold the values of that time",
  "Because M and M* are two ways of computing the same rotation: M with κ′, M* with λ′, both computed every block, and a credential is accepted if it matches either; that lets both the old and the new validator set sign during the rotation that straddles an epoch change, and η′_3 merely makes the two shuffles differ; outside that one rotation the two tables always agree and only M is consulted",
  "Because 0.8.0 made the set size variable: when |κ| ≠ |κ′| the shuffle of M changes completely, so M* recomputes with the previous set λ′ so that credentials signed by guarantors assigned before the shrink stay valid; when no epoch change occurs M* equals M and is only a safeguard"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 11.23 M* = (P(|κ′|, η′_2, τ′ − R), Φ(κ′)) 當 ⌊(τ′−R)/E⌋ = ⌊τ′/E⌋，否則用 (λ′, η′_3)；eq. 11.28 決定 t 落在哪個 rotation 就對哪個指派驗。",
  "M* 是 §11 的 on-chain 檢查用的，audit 是 off-chain 且自己重建 bundle，不查指派表。",
  "credential 不是「符合任一即可」：t 在當前 rotation 對 M、在上一個 rotation 對 M*，由 t 決定，不能混。",
  "集合大小改變時 eq. 11.18 直接清空 ρ‡、舊 report 作廢，不靠 M* 救；M* 的存在與集合可變無關。"
 ],
 "explanation": "起點是 eq. 11.28 的時間視窗：guarantee 的 slot t 只要滿足 R·(⌊τ′/R⌋ − 1) ≤ t ≤ τ′ 就可以被收，也就是允許「上一個 rotation 簽的、這個 rotation 才進 block」——網路延遲、出塊者剛好沒收到，都會造成這種晚到。但 guarantor 指派每 R = 10 個 slot 洗一次牌（eq. 11.20 M = (P(|κ′|, η′_2, τ′), Φ(κ′))），晚到的 guarantee 是由「當時」被指派的三個人簽的，鏈上要驗 credential 就得重算當時的指派，這就是 M*（eq. 11.23）。重算時要用「當時」的輸入：若上一個 rotation 與現在同一個 epoch，集合與 entropy 都沒變，只要把時間參數改成 τ′ − R；若跨了 epoch 邊界，當時的 active set 現在叫 λ′、當時的 η′_2 現在叫 η′_3（輪替各推了一格），所以 M* 改用 (λ′, η′_3)。這也是 d1-lambda-who-reads-it 列的三個 λ 讀者之一，和 d2-eta-four-slots-consumers 裡 η′_3 的第二個用途。口試追問「為什麼不乾脆拒絕上一個 rotation 的 guarantee」：那會讓每個 rotation 的最後一兩個 slot 產出的 report 幾乎都作廢，吞吐量掉一成。",
 "trap": "M* 不是備用算法，是「把時鐘撥回上一個 rotation」；跨 epoch 才需要連集合與 entropy 一起撥回去。"
},
{
 "id": "d2-seal-uses-posterior-set",
 "lens": "時機",
 "alsoCh": [
  "5"
 ],
 "ch": "6",
 "section": "6.2; 6.7 Seal",
 "gpRef": "eq. 6.14 (§6.2), eq. 6.16, §5 (H_I < |κ′|)",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["seal", "validator set"],
 "stemZh": "epoch 第一個 block 的 seal 是對 κ′ 驗的——也就是這個 block 自己輪替進來的那個集合。為什麼不對 κ 驗？這對實作的 header 驗證流程意味著什麼？",
 "optionsZh": [
  "因為這個 block 的作者是上個 epoch 由當時的 pending 集合 γ_P 投 ticket 選出來的，而 γ_P 在這個 block 的輪替裡正好升成 κ′；對 κ 驗會把每個 epoch 的第一個 block 都拒掉。實作上 seal、H_V 與 epoch marker 只能在算出 posterior Safrole 狀態後才能驗，header 驗證要分兩階段",
  "因為 κ 在這個 block 已經退成 λ′，而 GP 規定任何簽章都不能對 λ 驗；所以 seal 只好對 κ′ 驗。實作上這代表 header 驗證要先把 κ 複製成 κ′ 再驗 seal，順序無所謂",
  "其實 seal 是對 κ 驗的，GP 寫 κ′ 是因為在非換檔的 block 兩者相同、寫哪個都一樣；epoch 第一個 block 的作者仍來自舊集合 κ，這正是 λ 存在的理由。實作上 seal 可以在 state transition 之前驗完，一段就能驗完",
  "因為 seal 的 key H_A 是從 header 的 epoch marker H_E 裡讀的，不是從 state 讀的，所以「κ 還是 κ′」不影響 seal；GP 寫 κ′ 只是為了讓 H_I 的上界有個定義。實作上 seal 在解析 header 時就能驗"
 ],
 "stem": "The seal of an epoch's first block is verified against κ′ — the very set this block rotates in. Why not against κ, and what does that imply for an implementation's header-validation flow?",
 "options": [
  "Because this block's author was chosen by tickets cast in the previous epoch by the then-pending set γ_P, which this block's rotation promotes to κ′; verifying against κ would reject every epoch's first block. For an implementation the seal, H_V and the epoch marker can only be checked after the posterior Safrole state is computed, so header validation runs in two phases",
  "Because κ has already become λ′ in this block and the GP forbids verifying any signature against λ, so the seal has to be verified against κ′. For an implementation it means copying κ into κ′ before checking the seal; the order does not otherwise matter",
  "In truth the seal is verified against κ; the GP writes κ′ because in a non-rotating block the two coincide and either spelling works; the author of an epoch's first block still comes from the old set κ, which is precisely why λ exists. For an implementation the seal can be fully verified before the state transition, in a single pass",
  "Because the seal's key H_A is read from the header's epoch marker H_E rather than from state, so 'κ or κ′' does not affect the seal; the GP writes κ′ only so that the bound on H_I has a definition. For an implementation the seal is verifiable while parsing the header"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 6.16 的 H_A = κ′[H_I]_b、eq. 5.10 的 H_I < |κ′|；ticket 對 γ′_Z（γ_P 的 ring root）證明，而 eq. 6.14 讓 γ_P → κ′。團隊 PR #791 就是把 posterior state 傳給第二階段驗證。",
  "GP 允許對 λ 驗簽章（verdict 就是）；κ′ 不是「複製」來的，是輪替算出來的，順序決定成敗。",
  "seal 明確用 κ′；epoch 第一個 block 的作者來自 γ_P（新升的 κ′），不是舊 κ；λ 的用途是 verdict 與 M*。",
  "H_E 帶的是下個 epoch 的 key（γ′_P），不是這個 block 作者的 key；H_A 由 κ′[H_I] 決定。"
 ],
 "explanation": "把三條公式接起來。eq. 6.30：epoch e 期間投的 ticket，用 ring root γ′_Z 證明，而 γ′_Z 是對 γ_P（pending）算的，也就是投票的人是「下個 epoch 要上任」的那組。eq. 6.14：epoch e+1 的第一個 block 做輪替，κ′ = γ_P——投票的那組現在成為 active。eq. 6.16：seal 由 H_A = κ′[H_I]_b 驗，eq. 5.10 也以 |κ′| 限制 H_I。所以 epoch 第一個 block 的作者，是「這個 block 才升成 κ′」的那組人；對舊的 κ 驗，他的 key 根本不在裡面（或在不同的 index），整個 epoch 的第一個 block 永遠驗不過。這正是團隊 fuzzer bug #784「Header VRF Verification Failure on some cases」的根源（ch06-code-header-checks-posterior 那題）：修法是把 header 驗證拆成兩階段——先驗不依賴 Safrole 的欄位（parent、timeslot、extrinsic hash），跑 UpdateSafrole 得到 κ′、γ′_S、η′_3，再驗 seal、H_V 與 epoch marker。這是「讀 posterior」在實作上最直接的代價：某些 header 檢查不能在 state transition 之前完成。",
 "trap": "seal 看 κ′，因為投票的人和上任的人是同一組；header 驗證因此必須分兩段。"
},
{
 "id": "d2-assurance-prior-set-why",
 "lens": "時機",
 "ch": "11",
 "section": "11.2 Assurances; 11.3",
 "gpRef": "eq. 11.14, eq. 11.17, eq. 11.18, eq. 11.31",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["assurance", "validator set", "guarantee"],
 "stemZh": "assurance 的簽章對 κ[v] 驗、門檻是 2/3·|κ|，都是 prior 的集合；guarantee 卻用 κ′。為什麼不對稱？當 |κ| ≠ |κ′| 時，ρ 裡等待中的 report 會怎樣、為什麼？",
 "optionsZh": [
  "assurance 背書的 report 是更早的 block 進 ρ 的，shard 依當時的集合大小切（eq. 11.31），所以簽的人與門檻都屬於那個集合；guarantee 是這個 block 新收的工作，所以用 κ′。|κ| ≠ |κ′| 時舊 shard 數對不上，eq. 11.18 把 ρ‡ 全清，視為提早逾時",
  "assurance 用 κ 是 0.7.x 的殘留，0.8.0 本意是兩者都用 κ′，但為了相容測試向量沒有改；|κ| ≠ |κ′| 時 ρ 裡的 report 照常等待，只是門檻改成 2/3·|κ′|，shard 數的差異由 guarantor 重新編碼補上",
  "因為 assurance 是由出塊者代簽的，出塊者的 key 在 κ 裡有明確 index，而 guarantor 是 validator 自己簽，要用最新的 κ′；|κ| ≠ |κ′| 時 ρ 的 report 會被搬進 ω 等待下個 epoch 再 assurance 一次",
  "沒有不對稱：兩者都用 κ′，GP 在 eq. 11.13 寫 κ 是因為 assurance 的 anchor 是父 block、所以「父 block 的 κ′」就等於「這個 block 的 κ」；|κ| ≠ |κ′| 時 report 不受影響，因為 erasure coding 的 shard 數是常數 1023，由 full 設定寫死"
 ],
 "stem": "Assurance signatures are verified against κ[v] and the threshold is 2/3·|κ|, both the prior set, while guarantees use κ′. Why the asymmetry, and what happens to the reports waiting in ρ when |κ| ≠ |κ′|, and why?",
 "options": [
  "The report an assurance attests entered ρ in an earlier block and its shards were cut for the set size of that time (eq. 11.31), so signers and threshold belong to that set; a guarantee is work newly accepted in this block, hence κ′. When |κ| ≠ |κ′| the old shard counts no longer fit, so eq. 11.18 clears all of ρ‡ — timed out early",
  "Using κ for assurances is a 0.7.x leftover; 0.8.0 meant both to use κ′ but kept κ for test-vector compatibility; when |κ| ≠ |κ′| the reports in ρ keep waiting, only the threshold becomes 2/3·|κ′|, and the shard-count mismatch is patched by the guarantors re-encoding",
  "Because assurances are signed on validators' behalf by the block author, whose key has a definite index in κ, whereas guarantors sign for themselves and therefore use the freshest κ′; when |κ| ≠ |κ′| the reports in ρ are moved into ω to be assured again in the next epoch",
  "There is no asymmetry: both use κ′, and the GP writes κ in eq. 11.13 because an assurance anchors on the parent block, so 'the parent's κ′' is the same thing as 'this block's κ'; a change of |κ| does not affect reports, since the erasure-coding shard count is the constant 1023 fixed by the full config"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 11.13 簽章對 κ[a_v]_e、eq. 11.17 門檻 > 2/3|κ|、eq. 11.31 shard 數 = |κ′|（收納時）、eq. 11.18 在 |κ| ≠ |κ′| 時清空，§11.2 原文「Items cleared in this way can be viewed as having timed out early」。",
  "不是殘留：0.8.0 明確用 κ；也沒有「重新編碼」這種機制，report 直接作廢。",
  "assurance 是每個 validator 自己簽的（每人一份，最多一份）；ω 是依賴等待區，跟 assurance 無關。",
  "eq. 11.13 就是寫 κ；shard 數不是常數，0.8.0 起等於收納時的 |κ′|（tiny 是 6）。"
 ],
 "explanation": "看數字就懂：report 在 block N 被 guarantee 收進 ρ 時，eq. 11.31 要求它的 availability spec 宣告的 shard 數 (w_s)_v = |κ′|（block N 的 posterior set 大小），guarantor 也是照這個數切 erasure shard、分給那 |κ′| 個 validator。到了 block N+1、N+2 有人來 assurance，這些人就是「拿到 shard 的那批」，也就是 block N 的 κ′ = block N+1 的 κ。所以 eq. 11.13 對 κ[v] 驗簽、eq. 11.17 用 2/3|κ| 當門檻，兩者都在說「對切 shard 時的那個集合計票」。guarantee 相反，它是這個 block 新收的，shard 也是按這個 block 的 κ′ 切，所以用 κ′。當兩者不同——只會發生在 epoch 換檔且集合大小改變的 block——ρ 裡所有等待中的 report 的 shard 數都對不上新集合，沒辦法用新集合的人數算門檻，eq. 11.18 的第三個條件 |κ| ≠ |κ′| 就把 ρ‡ 全清，§11.2 原文：「Note that all items are cleared when the size of the active validator key set κ changes. Items cleared in this way can be viewed as having timed out early.」guarantor 要重新 guarantee、按新集合重切。這是 0.8.0 讓集合可變之後付出的代價，也是 ch11-inactive-core-set-shrink 那題的第三個判定依據。",
 "trap": "assurance 對「切 shard 時的集合」計票；集合大小一變，等待中的 report 全部提早逾時。"
},
{
 "id": "d2-timeout-which-clock",
 "lens": "時機",
 "ch": "11",
 "section": "11.2–11.3",
 "gpRef": "eq. 11.18 (H_T ≥ t + U), §11.4 (ρ′[c] = (g, τ′)), eq. 11.28",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["assurance", "timeslot"],
 "stemZh": "availability 逾時的條件是 H_T ≥ t + U。這個 t 是誰的時間？為什麼不用 guarantee 自己簽的 slot g_t？兩個時間最多差多少？",
 "optionsZh": [
  "t 是 report 進 ρ 那個 block 的 τ′（ρ′[c] = (g, τ′)），不是 guarantee 的 g_t。逾時量的是上鏈後暴露給 assurance 多久，計時從進 ρ 起算；g_t 可以比收納早最多 R = 10 個 slot，若用 g_t，晚到的 guarantee 一進來就可能逾時",
  "t 是 guarantee 自己簽的 slot g_t，因為它才是 guarantor 完成 refine、開始分發 shard 的時間，assurance 的機會從那時就開始；收納 block 的 τ′ 只用來算 statistics。兩者最多差 U = 5 個 slot，往前往後都一樣",
  "t 是 refinement context 裡 anchor 的 timeslot，因為 report 的內容是對那個時間點的 state 算的，逾時應該從資料變舊開始算；與收納時間最多差 H = 8 個 block",
  "t 是 report 第一次收到 assurance 的 block 的 τ′，在那之前不計時，因為沒有人開始背書就談不上逾時；與 guarantee 的 g_t 最多差一個 epoch"
 ],
 "stem": "The availability timeout is H_T ≥ t + U. Whose time is t, why not the guarantee's own signed slot g_t, and how far apart can the two be?",
 "options": [
  "t is the τ′ of the block that placed the report in ρ (ρ′[c] = (g, τ′)), not the guarantee's g_t. The timeout measures on-chain exposure to assurances, so the clock starts when the report enters ρ; g_t may precede inclusion by up to R = 10 slots, and with g_t a late guarantee could be timed out on arrival",
  "t is the guarantee's own signed slot g_t, because that is when the guarantors finished refining and began distributing shards, so the chance to assure starts then; the including block's τ′ is used only for statistics. The two differ by at most U = 5 slots in either direction",
  "t is the anchor timeslot inside the refinement context, because the report's content was computed against the state of that moment and the timeout should run from when the data started ageing; it differs from the inclusion time by at most H = 8 blocks",
  "t is the τ′ of the block in which the report first received an assurance, before which no clock runs, since nothing can time out until someone starts attesting; it differs from the guarantee's g_t by at most one epoch"
 ],
 "answer": 0,
 "optNotes": [
  "對：ρ′[c] 存的是 (g, τ′)，ch11-inactive-core-set-shrink 那題把「蓋 g_t 而非 τ′」列為錯誤選項；eq. 11.28 的視窗寬度是 R。",
  "g_t 只用來決定對 M 還是 M* 驗；逾時看的是 ρ 裡記的收納時間。",
  "anchor timeslot 用於 eq. 11.36 的 anchor 檢查，與逾時無關；差距上限也不是 H。",
  "沒有「第一次 assurance 才開始計時」的規則；ρ 記的就是收納時間，從那一刻起算。"
 ],
 "explanation": "ρ 的每格是 (g, t)：整份 guarantee 加一個 timeslot，而這個 t 在 eq. 11.x 的 ρ′ 定義裡是 τ′——收納它的那個 block 的 timeslot，不是 guarantee 自帶的 g_t。兩者為什麼會不同：eq. 11.28 允許 guarantee 的 g_t 落在上一個 rotation（最多比 τ′ 早 R = 10 個 slot），網路延遲下 guarantor 簽好的東西可能隔幾個 slot 才被某個出塊者收進去。逾時（eq. 11.18 的 H_T ≥ t + U，U = 5）要衡量的是「這份 report 在鏈上讓大家 assurance 的機會有多久」，機會從它出現在 ρ 那一刻才開始，所以 t 必須是收納時間。如果用 g_t：一份晚了 6 個 slot 才上鏈的 guarantee，收進 ρ 的同時就滿足 H_T ≥ g_t + 5，下一個 block 就被清掉，validator 根本沒機會拿到 shard 並背書。所以 g_t 與 t 各有用途：g_t 決定 credential 要對 M 還是 M* 驗（它回答「是誰簽的」），t 決定何時逾時（它回答「等了多久」）。這是 GP 裡「一個東西兩個時間戳」的典型例子，實作時最容易混。",
 "trap": "g_t 答「誰簽的」，ρ 裡的 τ′ 答「等多久」。逾時用後者。"
},
{
 "id": "d2-safrole-vs-babe-when-author-known",
 "lens": "對比",
 "alsoCh": [
  "ARCH"
 ],
 "ch": "6",
 "section": "4.8 Epochs and Slots; 6",
 "gpRef": "§4.8 prose (minimize forks), §6 prose, eq. 6.25",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["Polkadot", "Safrole"],
 "stemZh": "Polkadot 1.0 用 BABE 出塊，JAM 用 Safrole。就「某個 slot 的作者是什麼時候、怎麼決定的」這一點，兩者最根本的差別是什麼？這個差別買到什麼？",
 "optionsZh": [
  "BABE：每個 validator 每個 slot 各自算 VRF、低於門檻就能出塊，作者要等 block 出現才知道，一個 slot 可能零個或多個。Safrole：下個 epoch 每個 slot 的作者在這個 epoch 由匿名 ticket 排名定案，恰好一人一 slot。買到 §4.8 說的嚴格減少 slot 內與跨 slot 的 fork",
  "BABE：作者在 epoch 開始前就由 round-robin 排定，人人可預測；Safrole：作者在 slot 當下由 VRF 抽出，事前無法預測。買到的是抗 DoS，因為攻擊者不知道下一個要打誰；BABE 排程公開才讓空 slot 罕見，Safrole 的保密則是抗 fork 的代價",
  "兩者機制相同，都是 slot VRF 門檻抽籤，差別只在 Safrole 把 VRF 換成 Bandersnatch 曲線、並把門檻改成依 validator 數調整；買到的是簽章更短、驗證更快",
  "BABE：每個 slot 恰好一個作者，由 relay chain 的 runtime 依 stake 權重指定；Safrole：每個 slot 可能多人有資格，靠 GRANDPA 事後選一個。買到的是去中心化，因為不再由 runtime 指定"
 ],
 "stem": "Polkadot 1.0 authors blocks with BABE; JAM uses Safrole. On the single question 'when and how is a slot's author decided', what is the fundamental difference, and what does it buy?",
 "options": [
  "BABE: each validator evaluates its own VRF every slot and may author if under a threshold; the author is known only when a block appears, and a slot may have zero or several. Safrole: every slot of the next epoch has its author fixed during this epoch by ranking anonymous tickets, exactly one per slot. It buys §4.8's strict minimization of forks within and across slots",
  "BABE: authors are laid out round-robin before the epoch starts and anyone can predict them; Safrole: the author is drawn by a VRF at the slot itself and cannot be predicted beforehand. It buys DoS resistance, since an attacker does not know whom to hit next; the schedule being public in BABE is what makes its empty slots rare, whereas Safrole's secrecy is the price of its fork resistance",
  "The mechanisms are the same slot-VRF threshold lottery; Safrole merely swaps the VRF onto the Bandersnatch curve and scales the threshold with the validator count. It buys shorter signatures and faster verification",
  "BABE: exactly one author per slot, appointed by the relay-chain runtime by stake weight; Safrole: several validators may qualify per slot and GRANDPA picks one afterwards. It buys decentralization, since the runtime no longer appoints"
 ],
 "answer": 0,
 "optNotes": [
  "對：BABE 的 slot-VRF 門檻抽籤是 Polkadot 公開文件的描述；Safrole 由 eq. 6.25 在 epoch 換檔時把 γ_A 的 ticket 定案成整個 epoch 的 sealer 序列；§4.8 原文講 fork 最小化。",
  "反了：BABE 才是當下抽、不可預測；Safrole 的排程（哪張 ticket 哪個 slot）是提前公開的，只有「誰持有」是匿名。",
  "BABE 沒有 ticket、沒有提前一個 epoch 排程；Safrole 也不是門檻抽籤，是排名。差別不在曲線。",
  "BABE 沒有「runtime 指定」；Safrole 也不靠 GRANDPA 選作者，GRANDPA 只管 finality。"
 ],
 "explanation": "GP 對 Safrole 目標的原文（§4.8）：「through Safrole we aim to strictly minimize forks arising both due to contention within a slot (where two valid blocks may be produced within the same six-second period) and due to contention over multiple slots (where two valid blocks are produced in different time slots but with the same parent).」這兩種 fork 正是 BABE 的日常：BABE 讓每個 validator 每個 slot 各自用 VRF 對門檻抽籤（Polkadot 文件描述），結果可能沒人中（空 slot → 下一個作者接在同一個 parent 上，跨 slot fork）或多人中（同 slot fork）。Safrole 的做法是把「誰出塊」提前一個 epoch 決定：epoch e 期間大家匿名投 ticket 進 γ_A，eq. 6.25 在 e+1 的第一個 block 把排好的 ticket 定案為 γ′_S，之後每個 slot 恰好對應一張 ticket、一位作者。空 slot 只會因為作者離線而發生，同 slot 兩個作者在協定上不可能（seal 必須對應那張 ticket）。代價是需要 ring-VRF 這種較重的密碼學、需要一整個 epoch 的提前量、以及 ticket 不足時的 fallback。這題是「為什麼要 Safrole」的第一層；匿名性是第二層（d2-safrole-anonymity-vs-babe）。",
 "trap": "BABE 是「當下抽籤、可能零或多人」，Safrole 是「提前一個 epoch 排好、恰好一人」。"
},
{
 "id": "d2-safrole-anonymity-vs-babe",
 "lens": "對比",
 "alsoCh": [
  "ARCH",
  "G"
 ],
 "ch": "6",
 "section": "6 (ring VRF); App. G",
 "gpRef": "§6 prose (anonymous), eq. 6.30, eq. 6.16 (H_I reveals at seal)",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["Safrole", "Polkadot", "ring VRF"],
 "stemZh": "Safrole 把「哪張 ticket 排在哪個 slot」公開、卻把「誰持有那張 ticket」藏到出塊那一刻。BABE 兩者都不公開。Safrole 這樣拆開，比 BABE 多得到什麼、又保住了什麼？",
 "optionsZh": [
  "多得到可預測性：整個 epoch 的排程公開，每個 slot 確定恰好一位作者，網路能據此安排 rotation 與 audit 節奏。保住抗 DoS：ring-VRF 讓 ticket 對不回 validator，攻擊者知道下個 slot 有人出塊卻不知道是誰，直到 H_I 揭曉。BABE 只有後者",
  "多得到的是抗 DoS：BABE 的作者在 slot 前就能被推算，Safrole 把它藏起來；保住的是 BABE 的隨機性，因為 ticket 排名的順序仍由每個 slot 的即時 VRF 決定。兩者的可預測性一樣低",
  "多得到的是效率：公開排程讓 validator 不必每個 slot 都算 VRF；但失去了匿名性，因為 ticket id 是 VRF 輸出、可以由公鑰重算，任何人都能推出持有者。GP 接受這個代價換取確定的出塊",
  "兩者沒有差別：BABE 的作者在 block 出現前同樣無法預測，Safrole 只是把不可預測性從「slot 當下」搬到「epoch 開始」；ring-VRF 的匿名性是為了保護 ticket 分數不被操縱，跟 DoS 無關；兩個系統的抗 DoS 都只是靠 validator 不公開自己的位址"
 ],
 "stem": "Safrole publishes 'which ticket sits in which slot' but hides 'who holds that ticket' until the block is authored. BABE publishes neither. What does Safrole gain over BABE by splitting the two, and what does it keep?",
 "options": [
  "It gains predictability: the epoch's schedule is public and every slot is known to have exactly one author, so the network can plan rotations and audit cadence around it. It keeps DoS resistance: the ring VRF unlinks a ticket from its validator, so an attacker knows someone will author the next slot but not whom until H_I reveals it. BABE has only the latter",
  "It gains DoS resistance: a BABE author can be worked out before the slot, while Safrole hides it; it keeps BABE's randomness, since the order of ranked tickets is still decided by a live VRF in each slot. Both are equally unpredictable",
  "It gains efficiency: a public schedule spares validators from evaluating a VRF every slot; but it loses anonymity, because a ticket id is a VRF output recomputable from the public key, so anyone can infer the holder. The GP accepts that price for deterministic authoring",
  "There is no difference: a BABE author is equally unpredictable before the block appears, and Safrole merely moves the unpredictability from 'at the slot' to 'at epoch start'; the ring VRF's anonymity protects ticket scores from manipulation and has nothing to do with DoS; DoS resistance in both systems comes from validators simply not advertising their addresses"
 ],
 "answer": 0,
 "optNotes": [
  "對：§6 原文「keeping the correspondence between tickets and validators anonymous」；γ′_S 是 state、公開；H_I 在 seal 時才揭曉作者；BABE 沒有提前排程。",
  "BABE 的作者在 slot 前無法被推算（VRF 私鑰）；Safrole 的排序在 epoch 開始時就定案，不是每個 slot 即時抽。",
  "ring-VRF 的意義正是「無法由公鑰重算出是誰」，匿名性沒有失去；GP 也不是「接受失去匿名」。",
  "BABE 的作者事前不可預測，但「這個 slot 有沒有人」也不可預測，這正是差別；ring-VRF 的目的 GP 明說是匿名。"
 ],
 "explanation": "§6 開頭的原文：「In order to generate γ_S while keeping the correspondence between tickets and validators anonymous, we use a novel Ring VRF cryptographic scheme… This scheme allows validators to provide a proof which simultaneously: (1) guarantees the author controlled a key within the validator key sequence, and (2) produces an unbiasable deterministic hash output.」ring VRF 證明「我是集合裡的某一個」而不說是哪一個，所以 ticket id 對外只是個隨機數。排程本身（γ′_S 這個 sequence）是 state，人人可讀：第 k 個 slot 就是第 k 張 ticket。這給了兩樣東西。可預測性：每個 slot 確定有一位作者（不像 BABE 可能零或多位），整個網路——guarantor rotation、audit tranche 的 8 秒節奏、assurance 的 5 slot 逾時——都能建立在「slot 一定會有 block」的假設上。匿名性：攻擊者看得到「slot 37 有人」，看不到是哪台機器，直到那個 block 帶著 H_I 出現，這時攻擊已經來不及。BABE 的作者在 slot 前同樣不可推算（VRF 需要私鑰），所以 BABE 有匿名性；但 BABE 沒有「一定有人、恰好一人」的保證。所以 Safrole 不是「比 BABE 更匿名」，而是「同樣匿名，外加可預測」。這也是為什麼 fallback 模式（d2-fallback-vs-secondary-slots）被視為降級：它保住可預測性、放棄匿名性。",
 "trap": "Safrole：排程公開、持有者匿名。BABE：兩者都不知道，連「有沒有人」都不知道。"
},
{
 "id": "d2-fallback-vs-secondary-slots",
 "lens": "對比",
 "alsoCh": [
  "ARCH"
 ],
 "ch": "6",
 "section": "6.5 Slot key sequence (fallback)",
 "gpRef": "eq. 6.25, eq. 6.27, eq. 6.16 (fallback seal case)",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["fallback", "Safrole", "Polkadot"],
 "stemZh": "BABE 用 secondary slot 補空：某個 slot 沒人中籤時，由一個公開、可預測的次要作者補上。Safrole 的 fallback 跟它在「粒度」和「觸發條件」上有什麼不同？兩種設計各在保什麼？",
 "optionsZh": [
  "BABE 的 secondary 逐 slot：每個 slot 有一位公開的備援，primary 沒出現就補，所以匿名與公開作者在同一 epoch 交錯。Safrole 的 fallback 逐 epoch：只在邊界判斷上個 epoch 的 ticket 有沒有湊滿 E 張，沒有就整個下個 epoch 用 F(η′_2, κ′)。BABE 保每個 slot 有 block；Safrole 保一個 epoch 只有一種作者選法",
  "兩者相同：Safrole 的 fallback 也是逐 slot 的，某張 ticket 的持有者沒出塊時，eq. 6.27 用 η′_2 立刻算出該 slot 的替補 key；差別只在 BABE 的替補是 round-robin、Safrole 的替補是 hash 抽出。兩者都保每個 slot 有 block，而且只要 ticket 持有者沒出現，兩者都允許匿名與公開作者在同一個 epoch 內交錯",
  "BABE 的 secondary 是整個 epoch 的：epoch 開始時若 VRF 中籤人數不足就全 epoch 改 round-robin；Safrole 的 fallback 是逐 slot 的，ticket 沒人認領的 slot 才用 F 補。Safrole 保的是匿名性能撐到最後一刻",
  "Safrole 沒有 fallback：ticket 不夠時下個 epoch 直接沿用上個 epoch 的 γ_S；BABE 也沒有 secondary slot，空 slot 就是空著。兩者都靠 GRANDPA 在空 slot 之後重新同步"
 ],
 "stem": "BABE fills gaps with secondary slots: when no one wins a slot, a public, predictable secondary author steps in. How does Safrole's fallback differ in granularity and trigger, and what does each design protect?",
 "options": [
  "BABE's secondary is per slot: every slot has a public standby who fills in if the primary fails, so anonymous and public authors interleave within an epoch. Safrole's fallback is per epoch: only at the boundary does the chain ask whether last epoch's tickets filled all E places, and if not the whole next epoch uses F(η′_2, κ′). BABE protects 'every slot gets a block'; Safrole protects one author rule per epoch",
  "They are the same: Safrole's fallback is also per slot, and when a ticket's holder fails to author, eq. 6.27 uses η′_2 to compute that slot's replacement key on the spot; the only difference is that BABE's standby is round-robin and Safrole's is drawn by hash. Both protect 'every slot gets a block', and both let anonymous and public authors interleave freely within a single epoch whenever a ticket holder goes quiet",
  "BABE's secondary is per epoch: if too few validators win VRFs at the start, the whole epoch switches to round-robin; Safrole's fallback is per slot, using F only for slots whose ticket goes unclaimed. Safrole protects anonymity for as long as possible",
  "Safrole has no fallback: when tickets run short the next epoch simply reuses the previous γ_S; BABE has no secondary slots either, an empty slot stays empty. Both rely on GRANDPA to resynchronize after gaps"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 6.25 的三個 case 只在 e′ = e + 1 時決定整個 epoch 的 γ′_S，條件是 m ≥ Y ∧ |γ_A| = E；不滿足就 F(η′_2, κ′)，整個 epoch 都是 key 序列。BABE secondary 的描述來自 Polkadot 文件。",
  "Safrole 沒有逐 slot 替補：ticket 持有者沒出塊那個 slot 就是空的（下一個作者接同一個 parent）。",
  "反了：BABE 逐 slot、Safrole 逐 epoch。",
  "eq. 6.25 明確定義 fallback 為 F(η′_2, κ′)；BABE 有 secondary slot；GRANDPA 不處理出塊。"
 ],
 "explanation": "eq. 6.25 是全部：γ′_S 在 e′ = e + 1 時，若 m ≥ Y 且 |γ_A| = E，取 Z(γ_A)（ticket 模式）；否則取 F(η′_2, κ′)（fallback）；非換檔 block 則不變。決定只在 epoch 邊界做一次，決定的是整個 epoch。eq. 6.27 的 F 用 η′_2 對每個 slot 算一個 hash、對 |κ′| 取模，得到一串公開的 Bandersnatch key——這是「排程公開、持有者也公開」的模式，匿名性沒了，但「恰好一人一 slot」還在，seal 改用 X_F context 驗（eq. 6.16 第二種情形）。BABE 的 secondary slot（Polkadot 文件）是另一種思路：primary 抽籤照常，每個 slot 另外用 round-robin 指定一位公開的備援，primary 沒出現他就補，所以 epoch 內兩種作者交錯出現。兩種設計保的東西不同：BABE 在意「盡量不要有空 slot」，Safrole 在意「同一個 epoch 內作者的選法只有一種、事前就定」——這讓 ch06-fallback-purpose 那題問的「fallback 期間放棄什麼」有明確答案：放棄匿名，不放棄確定性。順帶：Safrole 的 ticket 模式下，持有者離線那個 slot就是空的，沒有替補，這是它接受的代價。",
 "trap": "BABE secondary 是每個 slot 的備胎；Safrole fallback 是整個 epoch 換模式，中途不切。"
},
{
 "id": "d2-grandpa-unchanged-why",
 "lens": "對比",
 "alsoCh": [
  "6"
 ],
 "ch": "ARCH",
 "section": "4.6 Best block; 19 Grandpa and the Best Chain",
 "gpRef": "§4.6, §19 (best-chain conditions), §18",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["GRANDPA", "Polkadot"],
 "stemZh": "JAM 把出塊機制從 BABE 換成 Safrole，卻把 GRANDPA 原樣留下。為什麼 finality 不需要跟著重新設計？JAM 對 GRANDPA 唯一改動的地方在哪？",
 "optionsZh": [
  "因為 GRANDPA 對 block 怎麼產生是中立的：它只對哪條鏈投票，不管作者。Safrole 解決的是出塊層的 fork 問題，finality 不用動。唯一改的是餵給它的東西：best-chain 規則加了「已 audited」「無 equivocation」「ticket 封緘祖先優先」，投票帶 header 與 posterior state root",
  "因為 GRANDPA 在 JAM 裡已經被 BEEFY 取代：BEEFY 的 BLS 聚合簽名就是 finality，GRANDPA 只留下名字給文件相容。JAM 改動的地方是把投票從 header 改成 accumulation output 的 super-peak，所以投票不再需要帶 state root，audited 條件也就不需要了",
  "因為 GRANDPA 被併進 Safrole 了：ticket 的排名同時決定作者與 finality 順序，seal 的簽章就是 finality 投票。JAM 改的是把 GRANDPA 的 2/3 門檻改成 ticket 的 Y 尾段條件",
  "因為 GRANDPA 改成逐 work-report 投票：每份 report available 之後由 validator 投票定案，block 的 finality 是所有 report 定案的結果。JAM 改的是投票單位，從 block 變成 report"
 ],
 "stem": "JAM replaces BABE with Safrole for block production yet keeps GRANDPA as is. Why does finality not need redesigning, and what is the one place JAM does change around GRANDPA?",
 "options": [
  "Because GRANDPA is agnostic about how blocks are produced: it votes on which chain, not on who authored it. Safrole fixes a production-layer problem (too many forks), so finality is untouched. The one change is its input: the best-chain rule adds 'audited', 'no equivocation' and 'prefer ticket-sealed ancestors', and the vote carries the header with its posterior state root",
  "Because GRANDPA has been replaced by BEEFY in JAM: BEEFY's aggregated BLS signatures are the finality, and GRANDPA survives in name only for documentation compatibility. The change is that votes are cast over the accumulation-output super-peak rather than the header, which is why the vote no longer needs to carry a state root and why the audited condition became unnecessary",
  "Because GRANDPA has been folded into Safrole: the ticket ranking decides both the author and the finality order, and the seal signature doubles as the finality vote. The change is that GRANDPA's 2/3 threshold becomes the ticket tail condition Y",
  "Because GRANDPA now votes per work-report: once a report is available, validators vote to finalize it, and a block's finality is the sum of its reports' finalizations. The change is the unit of voting, from block to report"
 ],
 "answer": 0,
 "optNotes": [
  "對：§19 列 best block 的條件（descend from finalized、audited、無 equivocation、ticket 封緘祖先最多），投票帶 header 與 posterior state root（arch-best-chain-selection）；GRANDPA 本身沒改。",
  "BEEFY 是給 bridge 用的額外簽名（§18），不取代 GRANDPA；它在 block finalize 之後才簽。",
  "Safrole 只管出塊，seal 不是 finality 投票；Y 是 ticket 提交期的尾段界線。",
  "GRANDPA 投的是鏈（block），不是 report；report 的「定案」靠的是 audit 與它所在 block 的 finality。"
 ],
 "explanation": "GRANDPA 的輸入是「每個 validator 認為最好的鏈頭」，輸出是「所有誠實節點都同意不可逆的前綴」。它對鏈頭怎麼來的沒有任何假設，所以出塊層從 BABE 換成 Safrole 對它是透明的。JAM 需要改的是「什麼算最好的鏈頭」，§19 給了條件：從最新 finalized block 往下、被視為 audited、未定案部分沒有 equivocation、在這些裡選 ticket 封緘（非 fallback）祖先最多的（§6 說 ticket 封緘「is of greater security」，所以優先）。「必須 audited」是關鍵的新條件：JAM 的 block 在 accumulate 時還沒被驗證（d1-accumulate-before-audit），若 GRANDPA 對未 audited 的 block 投票，壞 report 就可能被定案。§17 原文：「One prerequisite of a node finalizing a block is for it to view the block as audited.」投票內容則是 header 加 posterior state root（arch-best-chain-selection）。BEEFY（§18）是另一層：在 GRANDPA 定案之後，validator 對 accumulation output 的 super-peak 做 BLS 簽名，給 bridge 用，不參與 finality 判定。所以三個機制分工：Safrole 決定誰出塊、GRANDPA 決定哪條鏈不可逆、BEEFY 讓外部系統便宜地驗證定案結果。",
 "trap": "GRANDPA 沒改，改的是餵給它的 best-chain 規則：audited 才能投。"
},
{
 "id": "d2-elves-mapping-whats-new",
 "lens": "對比",
 "alsoCh": [
  "11"
 ],
 "ch": "ARCH",
 "section": "2.1 Polkadot; 4.9.1",
 "gpRef": "§2.1 (co-opts ELVES), §4.9.1 (four stages), §14, §16",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["ELVES", "Polkadot", "host call"],
 "stemZh": "GP 說 JAM「co-opts much of the same game-theoretic and cryptographic machinery as Polkadot known as ELVES」。把 Polkadot 1.0 的四個階段對到 JAM 的名字，然後說：在同一套 ELVES 之上，JAM 真正新增的是什麼？",
 "optionsZh": [
  "backing → guaranteeing、availability → assuring、approval → auditing、disputes → judging。新增的：core 只輸出小 digest，效果由 service 的 accumulate 在鏈上決定；DA 分成短期 audit DA 與長期 D³L，package 之間能 import / export segment；core 對跑什麼沒有意見",
  "backing → assuring、availability → guaranteeing、approval → judging、disputes → auditing。新增的是 SNARK 證明：每份 report 附一個 refine 的零知識證明，讓 audit 可以只驗證明不必重跑，這也是 JAM 不需要可得性系統的原因",
  "四個階段一一對應、名字也沒改，GP 直接沿用 backing / availability / approval / disputes；JAM 新增的是 BEEFY 與 ring-VRF，這兩個是 Polkadot 沒有的",
  "JAM 沒有沿用 ELVES：guaranteeing 與 assuring 是新設計，Polkadot 的 backing 與 availability 被拿掉；只有 disputes 保留。新增的是把 audit 從鏈下搬到鏈上，讓每個 validator 都重跑 refine"
 ],
 "stem": "The GP says JAM 'co-opts much of the same game-theoretic and cryptographic machinery as Polkadot known as ELVES'. Map Polkadot 1.0's four stages onto JAM's names, and then say what JAM genuinely adds on top of that same machinery.",
 "options": [
  "backing → guaranteeing, availability → assuring, approval → auditing, disputes → judging. New on top: a core emits a small digest whose effect the service's accumulate decides on-chain; availability splits into a short audit DA and a long-lived D³L with segment import/export; cores hold no opinion on what they run",
  "backing → assuring, availability → guaranteeing, approval → judging, disputes → auditing. What is new is SNARK proving: every report carries a zero-knowledge proof of refine so that auditing verifies the proof instead of re-executing, which is also why JAM needs no availability system",
  "The four stages map one to one and even keep their names — the GP simply reuses backing / availability / approval / disputes; what JAM adds are BEEFY and the ring VRF, neither of which Polkadot had",
  "JAM does not reuse ELVES: guaranteeing and assuring are new designs, Polkadot's backing and availability were dropped, and only disputes survive. What is new is moving auditing on-chain so that every validator re-runs refine"
 ],
 "answer": 0,
 "optNotes": [
  "對：§4.9.1「guaranteeing, assuring, auditing and, potentially, judging」對應 ELVES 的四階段；§4.9 講 refine/accumulate 拆分；§14、§16 講兩種 DA 與 segment；§2.1 講 core 無定見。",
  "對應順序錯了兩對；JAM 不用 SNARK（§1.3 明說走 crypto-economic 路線）。",
  "名字改了；BEEFY 是 Polkadot 就有的（給 bridge 用），ring-VRF 是 Sassafras 的，都不是 JAM 「在 ELVES 之上新增」的東西。",
  "§2.1 明說 co-opts ELVES；audit 在 JAM 仍是 off-chain（§17），沒有人人重跑。"
 ],
 "explanation": "§2.1 原文：「In order to deliver its service, JAM co-opts much of the same game-theoretic and cryptographic machinery as Polkadot known as ELVES… However, major differences exist in the actual service offered.」四階段的對應來自 §4.9.1：「a crypto-economic game of three stages called guaranteeing, assuring, auditing and, potentially, judging」，分別對 Polkadot 的 backing（少數人執行並簽名）、availability（erasure code 分發、bitfield 背書）、approval checking（隨機抽人重跑）、disputes（投票定罪）。機制一樣，服務不一樣，差別在三處。一、**輸出的意義**：Polkadot 的 core 跑 PVF，輸出是 parachain 的新 head/state root，relay chain 只記錄；JAM 的 core 跑 refine，輸出是 ≤ 48 KB 的 digest，然後鏈上跑 service 的 accumulate 決定它怎麼影響 state（§4.9），所以 service 之間能組合。二、**DA 的用途擴大**：Polkadot 的 availability 只為 approval 服務，資料活到 audit 完就好；JAM 多了 D³L（§14、§16），export 的 segment 活 28 天，讓後面的 package import——資料可以在 core 之間流動而不必回到鏈上。三、**core 無定見**（§2.1）：Polkadot 的 core 只會驗 parachain block，JAM 的 core 跑任何 authorizer 放行的 package。所以口試若問「JAM 跟 Polkadot 差在哪」，答「安全賽局同一套，改的是 core 上跑什麼、輸出怎麼用、資料能不能留」。",
 "trap": "四個名字換了、賽局沒換；新的是 refine/accumulate 拆分、D³L、core 無定見。"
},
{
 "id": "d2-jam-header-vs-relay-header",
 "lens": "對比",
 "alsoCh": [
  "ARCH"
 ],
 "ch": "5",
 "section": "5 The Header",
 "gpRef": "eq. 5.1, eq. 5.4–5.7 (H_X), eq. 5.10–5.11",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["Polkadot", "work-digest"],
 "stemZh": "Polkadot relay chain 的 header 是 (parent hash, number, post-state root, extrinsics root, digest logs)，BABE 的 slot / VRF 與 seal 都塞在 digest 裡。對照 JAM 的十元組 header，最重要的三個結構差異是什麼？各自的理由？",
 "optionsZh": [
  "一、承諾 prior state root 而非 post，作者不必等 Merklize 就能發 block。二、seal、entropy VRF、author index 與三個 marker 是型別化欄位，不是不透明的 digest log，只讀 header 的節點就能驗作者。三、用 timeslot 取代 block number，因為 block 可以跳 slot；H_X 是五個分量雜湊再雜湊，光憑 header 就能證明某個分量",
  "一、JAM 的 header 沒有 parent hash，改用 timeslot 定位父 block，因為 slot 唯一決定 parent。二、JAM 把 state root 完全拿掉，state 的承諾交給 BEEFY。三、JAM 的 seal 放在 block body 的 E_T 裡，header 只留 author index，好讓只讀 header 的節點仍能按 index 數 block",
  "兩者結構相同：JAM 只是把 digest logs 攤平成命名欄位，方便 formula 引用；post-state root 仍在（H_R），extrinsics root 仍在（H_X），block number 仍在（H_T 就是 number）。差別純粹是表示法",
  "一、JAM 的 header 多了 post-state root 與 prior state root 兩個，Polkadot 只有一個。二、JAM 的 seal 是 Ed25519 而 Polkadot 是 sr25519，所以要單獨一欄。三、JAM 的 digest 改名叫 marker，但內容一樣是不透明 log"
 ],
 "stem": "A Polkadot relay-chain header is (parent hash, number, post-state root, extrinsics root, digest logs), with BABE's slot/VRF and the seal tucked inside the digest. Against JAM's ten-tuple header, what are the three most important structural differences, and the reason for each?",
 "options": [
  "One: the prior state root, not the post one, so the author can publish before Merklizing. Two: seal, entropy VRF, author index and three markers are typed fields, not opaque digest logs, so a header-only node can verify the author. Three: a timeslot instead of a block number, since blocks may skip slots; and H_X is a hash of five per-component hashes, so a header can prove one component",
  "One: JAM's header has no parent hash and locates its parent by timeslot, since a slot uniquely determines the parent. Two: JAM drops the state root entirely and delegates state commitment to BEEFY. Three: JAM's seal lives in the block body inside E_T, with only the author index left in the header so that a header-only node can still count blocks by index",
  "The structures are the same: JAM merely flattens the digest logs into named fields for easier reference in formulas; the post-state root is still there (H_R), the extrinsics root is still there (H_X), and the block number is still there (H_T is the number). The difference is purely notational",
  "One: JAM's header carries both a post-state root and a prior state root where Polkadot has one. Two: JAM's seal is Ed25519 where Polkadot's is sr25519, hence its own field. Three: JAM's digest is renamed 'marker' but remains an opaque log"
 ],
 "answer": 0,
 "optNotes": [
  "對：eq. 5.1 的十個欄位；H_R 是 prior（§5 原文與 ch05-prior-state-root）；H_E/H_W/H_O 型別在 eq. 5.11；H_X 的結構在 eq. 5.4–5.7；沒有 number，只有 H_T。Polkadot header 結構來自 Substrate 的 Header 型別。",
  "H_P 是 parent hash，存在；H_R 是 state root，存在；seal H_S 在 header 裡，E_T 是 ticket。",
  "H_R 是 prior 不是 post；H_T 是 timeslot 不是連續的高度，block 可以跳；marker 是型別化的，不是 log。",
  "只有一個 state root（prior）；seal 是 Bandersnatch 不是 Ed25519；marker 有明確型別（eq. 5.11）。"
 ],
 "explanation": "eq. 5.1：H = (H_P, H_R, H_X, H_T, H_E, H_W, H_O, H_I, H_V, H_S)。逐項對照 Substrate 的 Header（parent_hash, number, state_root, extrinsics_root, digest）。**state root 的時間點**：Polkadot 的 state_root 是執行後的，JAM 的 H_R 是執行前的（§5：「the prior state root」），ch05-prior-state-root 講過理由——作者不用等 Merklize，錯誤晚一個 block 才顯現。**共識資料的地位**：Polkadot 把 BABE 的 pre-runtime digest（slot、VRF 輸出）、seal、epoch 變更的 consensus log 全放在 digest 這個不透明的 log 序列裡，runtime 與 client 各自解析；JAM 把它們升為 header 的正式欄位並給型別（eq. 5.11：H_E ∈ (H, H, ⟦(bs, ed)⟧)?、H_W ∈ ⟦ticket⟧_E?、H_O ∈ ⟦ed key⟧），所以只讀 header 的節點能做 ch05-what-header-alone-proves 那題列的檢查。**高度與時間**：Polkadot 有連續的 number，JAM 只有 H_T，因為 Safrole 下 block 可以跳 slot（甚至跳 epoch），「第幾個 block」不是有意義的量。**extrinsics root 的結構**：Polkadot 是 extrinsic 的 trie root；JAM 的 H_X = H(E(H#(a)))，a 是五個分量各自的雜湊（其中 preimage 與 guarantee 兩個分量內部再逐項雜湊），ch05-why-five-component-hash 講過這讓輕節點能用一份小 witness 證明某個分量。",
 "trap": "三個差：prior root、型別化的共識欄位、timeslot 取代 number。"
},
{
 "id": "d2-why-transactionless",
 "lens": "設計",
 "alsoCh": [
  "ARCH",
  "8"
 ],
 "ch": "4",
 "section": "4.9 The Core Model and Services",
 "gpRef": "§4.9 prose (no transactor), §8 prose",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["authorizer", "core"],
 "stemZh": "JAM 沒有 transaction。§4.9 說 JAM 裡「沒有 transactor 這個概念」。為什麼要把 Ethereum 那種「簽名的交易」整個拿掉？拿掉之後，「使用者提交東西」這件事去了哪裡？",
 "optionsZh": [
  "因為 Ethereum 的簽名同時做兩件事：證明誰授權、誰付費，綁在同一個帳戶。JAM 拆開：付費走 coretime，授權走在 in-core 跑的 is-authorized 程式，資料全經 refine 進入。使用者的提交變成帶 token 的 work-package 給 authorizer 看；想要交易式體驗，寫一支驗簽名的 authorizer 就有",
  "因為簽名驗證太貴：Ed25519 每秒只能驗幾萬次，鏈上做不到 JAM 要的吞吐量。JAM 把驗簽搬到 accumulate 裡由 service 自己做，鏈上只看 hash。使用者的提交變成 E_P：把要送的資料當 preimage 提供給 service，service 在 accumulate 時讀出來處理",
  "因為 JAM 沒有使用者帳戶：所有帳戶都是 service，沒有私鑰、沒有 nonce，所以無法簽交易。使用者的提交變成 ticket：透過 E_T 把請求送給下個 epoch 的出塊者，由出塊者代為執行",
  "因為 transaction 需要 mempool，而 Safrole 的匿名出塊者無法維護共用的 mempool。使用者的提交改由 guarantor 收集，guarantor 把交易打包成 work-report 的 authorizer trace 帶上鏈"
 ],
 "stem": "JAM has no transactions; §4.9 says there is 'no such concept of a transactor'. Why remove Ethereum-style signed transactions altogether, and where does 'a user submitting something' go instead?",
 "options": [
  "Because an Ethereum signature does two jobs, proving who authorizes and who pays, tied to one account. JAM separates them: payment goes through coretime, authorization through the is-authorized program run in-core, and all data enters through refine. A user's submission becomes a work-package carrying a token for the authorizer; a transaction-like flow is one signature-checking authorizer away",
  "Because signature verification is too expensive: Ed25519 verifies only tens of thousands of signatures per second, short of JAM's throughput target. JAM moves signature checking into accumulate for each service to do itself, while the chain looks only at hashes. A user's submission becomes E_P: the data to send is supplied as a preimage, which the service reads out and handles during accumulate",
  "Because JAM has no user accounts: every account is a service with no private key and no nonce, so nothing could sign a transaction. A user's submission becomes a ticket: the request is sent through E_T to the next epoch's authors, who execute it on the user's behalf",
  "Because transactions need a mempool, and Safrole's anonymous authors cannot maintain a shared one. Submissions are instead collected by guarantors, who bundle them into the work-report's authorizer trace and carry them on-chain"
 ],
 "answer": 0,
 "optNotes": [
  "對：§4.9「the mechanism of account authorization is somewhat combined with the mechanism of purchasing blockspace, both relying on a cryptographic signature… In JAM, these are separated and there is no such concept of a transactor」；§8 講 authorizer 與 token；資料經 refine（§4.9「All data extrinsic to JAM is fed into the refinement code」）。",
  "GP 沒有拿驗簽成本當理由；E_P 是 service 主動 solicit 的原像供應，不是使用者的通用提交管道。",
  "「沒有使用者帳戶」是結果不是原因；E_T 是 Safrole 的 ticket，與使用者提交無關。",
  "mempool 不在 GP 的討論裡；authorizer trace 是 is-authorized 的輸出，不裝交易。"
 ],
 "explanation": "§4.9 原文把理由講完了：「Within the Ethereum transactive model, the mechanism of account authorization is somewhat combined with the mechanism of purchasing blockspace, both relying on a cryptographic signature to identify a single 'transactor' account. In JAM, these are separated and there is no such concept of a 'transactor'.」也就是說，問題不在簽名本身，而在簽名把「誰授權這件事」和「誰為這件事付費」焊死在一起，於是每個使用者都得有帳戶、有餘額、有 nonce，鏈上得為每筆交易驗簽、扣費。JAM 把三件事分到三個地方：**付費**是 coretime，事先買、由 authorizer 代表這段時間的使用意圖（§8：「disentangling the intention of usage for some coretime from the specification and submission of a particular workload」）；**授權**是 is-authorized 程式，在 in-core 跑，鏈上只查 pool（ch08-authorizer-identity）；**資料**一律走 refine（§4.9：「All data extrinsic to JAM is fed into the refinement code of some service」），鏈上永遠不解析使用者輸入。使用者「提交」的東西是 work-package，裡面的 token 就是給 authorizer 看的憑證——可以是簽名、可以是付款證明、可以什麼都不是。這讓 JAM 同時容納 Ethereum 式（authorizer 驗使用者簽名）和 Polkadot 式（authorizer 驗 parachain block）兩種模式，§8 原文：「supporting a range of interaction patterns both Ethereum-style and Polkadot-style」。副產品：沒有 nonce、沒有使用者帳戶、沒有 mempool 這種鏈上概念（arch-services-vs-accounts）。",
 "trap": "不是「不能簽名」，是「簽名不再是入口」。授權、付費、資料三件事各走各的路。"
},
{
 "id": "d2-elves-vs-snark-tradeoff",
 "lens": "設計",
 "ch": "ARCH",
 "section": "1.3; 2.2 SNARK roll-ups",
 "gpRef": "§1.3 last paragraph, §2.2 (SNARK roll-ups), §4.9.1",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["Ethereum", "ELVES"],
 "stemZh": "JAM 用 ELVES（擔保 + 可得性 + 稽核 + 爭議）而不是 SNARK 來保證 in-core 運算正確。GP 給的理由是什麼？這個選擇在「正確性的性質」上付出了什麼代價？",
 "optionsZh": [
  "理由（§1.3）：crypto-economic 機制「inherits their low-cost and high-performance profiles and averts a bias toward centralization」；SNARK 證明成本高好幾個數量級、證明者集中。代價：正確性從「數學上確定」變成「機率上被誠實的人抓到」，所以需要 assurance、隨機 auditor 與整條分支作廢的 dispute",
  "理由：SNARK 的驗證太慢，1023 個 validator 每個 block 驗 341 個證明來不及。代價：JAM 的 in-core 結果只有三位 guarantor 看過，其他人完全信任他們，所以 guarantor 的押金必須大到足以賠償整個 service 的損失，直接從它鏈上的餘額扣",
  "理由：SNARK 只能證明固定電路，而 refine 是任意 PVM 程式。代價：JAM 必須讓每個 validator 都重跑一遍 refine 才能確定正確，這就是 audit 的意思，也是 in-core 只有單機 300 倍的原因",
  "理由：SNARK 需要可信設定（trusted setup），與 Web3 的 resilience 相衝。代價：JAM 放棄了 in-core 運算的正確性保證，只保證資料可得，正確性由 service 自己在 accumulate 裡驗證"
 ],
 "stem": "JAM secures in-core computation with ELVES (guarantee + availability + audit + dispute) rather than SNARKs. What reason does the GP give, and what does the choice cost in the nature of correctness?",
 "options": [
  "Reason (§1.3): crypto-economic mechanisms 'inherit their low-cost and high-performance profiles and avert a bias toward centralization'; SNARK proving costs orders of magnitude more and concentrates provers. Cost: correctness is 'probably caught by an honest party', not 'mathematically certain', hence assurance, random auditors and branch-abandoning disputes",
  "Reason: SNARK verification is too slow, 1023 validators could not verify 341 proofs per block in time. Cost: an in-core result is seen only by its three guarantors and everyone else trusts them completely, so a guarantor's stake must be large enough to compensate the whole service's loss from its own balance, on-chain",
  "Reason: a SNARK can prove only a fixed circuit, whereas refine is an arbitrary PVM program. Cost: JAM must have every validator re-run refine to be sure it is right, which is what auditing means and why in-core is only 300 times a single machine",
  "Reason: SNARKs need a trusted setup, which conflicts with Web3 resilience. Cost: JAM gives up any correctness guarantee for in-core work and guarantees only availability, leaving correctness for each service to verify itself inside accumulate"
 ],
 "answer": 0,
 "optNotes": [
  "對：§1.3 末段原文；§2.2 對 SNARK roll-up 成本與中心化的分析；§4.9.1 說明四階段各附加什麼保證。",
  "GP 的理由是證明成本與中心化，不是驗證速度；in-core 結果不是「完全信任 guarantor」，有 audit。",
  "PVM 通用性不是 GP 給的理由；audit 是隨機抽樣（每 report 約 30 次），不是人人重跑。",
  "GP 沒提 trusted setup；in-core 的正確性正是由 audit + dispute 保證的，不是交給 service。"
 ],
 "explanation": "§1.3 結尾原文：「Unlike with SNARK-based L2-blockchain techniques for scaling, this model draws upon crypto-economic mechanisms and inherits their low-cost and high-performance profiles and averts a bias toward centralization.」§2.2 的 SNARK roll-up 小節展開了兩個問題：證明的計算成本比原生執行高好幾個數量級（GP 引用的估計是數萬倍），以及證明者因此集中到少數有大機器的人手上——這與 resilience 相衝。ELVES 的路線（§4.9.1）：guaranteeing「attach a substantial economic cost to the invalidity」、assuring「a sufficient degree of confidence that the inputs… will be available」、auditing「a sufficient degree of confidence that the validity… will be checked by some party who we can expect to be honest」。三句話說完了代價：每一層都是「足夠的信心」而不是「證明」。所以 JAM 的正確性模型是：三個人算、大家存一片、隨機約 30 個人重跑、有人發現不對就 dispute、整條含壞 report 的分支被放棄（d1-accumulate-before-audit）。它依賴「隨機抽到的人裡至少有一個誠實且會說話」，這是機率性的，也是 §17 說「there may not be consensus at the time that the block gets finalized」的原因。換來的是 in-core 運算幾乎零額外成本、任何機器都能當 validator。",
 "trap": "SNARK 賣「不可能錯」但貴且集中；ELVES 賣「錯了會被抓」但便宜且分散。"
},
{
 "id": "d2-tickets-per-validator-scaling",
 "lens": "設計",
 "ch": "6",
 "section": "6.6 Tickets extrinsic",
 "gpRef": "eq. 6.30 (n = ⌈2E/|γ′_P|⌉), §6.6 prose, eq. 6.25",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["ticket", "validator set"],
 "stemZh": "0.8.0 把每位 validator 能投的 ticket 數改成 n = ⌈2E/|γ′_P|⌉，validator 越少每人能投越多。GP 給的理由是什麼？為什麼分子是 2E 而不是 E？",
 "optionsZh": [
  "理由（§6.6）：「To ensure the accumulator can be saturated, when there are fewer validators, each validator is permitted more tickets」；eq. 6.25 只在 |γ_A| = E 時用 ticket 模式。2E 讓容量是 slot 數的兩倍，部分 validator 離線仍能填滿；full 設定 n = 2，六人 n = 4",
  "理由：讓每位 validator 的中籤機率相等。分子 2E 是因為 ticket 有兩個 entry index（0 和 1），每張 ticket 算兩次；validator 少的時候每人多投是為了補償他們在 ring 裡的匿名集合變小，讓每個 validator 一樣難被辨識",
  "理由：防止女巫攻擊。validator 越少，每個人越容易被辨識，所以讓每人投更多 ticket 來稀釋可辨識性；2E 是因為 GP 要求 accumulator 保留 2E 張再取前 E 張",
  "理由：與 core 數對齊。每個 core 需要兩張 ticket（一張 primary 一張 backup），2E 就是 2 × 每 epoch 的 slot 數；validator 少時每人多投是為了讓每個 core 都有備援"
 ],
 "stem": "0.8.0 makes the tickets each validator may submit n = ⌈2E/|γ′_P|⌉, so fewer validators means more tickets each. What reason does the GP give, and why is the numerator 2E rather than E?",
 "options": [
  "Reason (§6.6): 'To ensure the accumulator can be saturated, when there are fewer validators, each validator is permitted more tickets'; eq. 6.25 uses tickets only when |γ_A| = E. 2E makes capacity twice the slot count, so the accumulator fills even if some validators are offline; full config n = 2, six validators n = 4",
  "Reason: to equalize each validator's chance of winning. The numerator is 2E because a ticket has two entry indices (0 and 1) and each ticket counts twice; with fewer validators each submits more to compensate for the smaller anonymity set in the ring, keeping every validator equally hard to identify",
  "Reason: to resist Sybil attacks. With fewer validators each is easier to identify, so each submits more tickets to dilute identifiability; 2E is because the GP requires the accumulator to keep 2E tickets and then take the best E",
  "Reason: to line up with cores. Every core needs two tickets, a primary and a backup, so 2E is twice the slots per epoch; with fewer validators each submits more so that every core keeps a backup"
 ],
 "answer": 0,
 "optNotes": [
  "對：§6.6 原文與 eq. 6.30；eq. 6.25 的 |γ_A| = E 條件說明為何「湊滿」是硬需求；2× 的過額是可從公式推得的設計裕度。",
  "entry index 的範圍是 N_n（0 到 n−1），不是固定兩個；ticket 不「算兩次」。",
  "accumulator 只保留 E 張（eq. 6.35 的 →^E），不是 2E；Sybil 不是 GP 給的理由。",
  "ticket 對應的是 slot 不是 core，也沒有 backup ticket 的概念。"
 ],
 "explanation": "§6.6 原文：「To ensure the accumulator can be saturated, when there are fewer validators, each validator is permitted more tickets.」關鍵字是 saturated。eq. 6.25 把 ticket 模式的條件寫死：只有當 |γ_A| = E（accumulator 剛好裝滿 E 張）且 m ≥ Y 時，下個 epoch 才用 Z(γ_A)；少一張都整個 epoch 退回 fallback F(η′_2, κ′)，匿名性沒了。所以「每個 epoch 至少要收到 E 張有效 ticket」是硬需求，而 ticket 只能由 validator 投，每人 n 張、|γ′_P| 個人，總容量 n·|γ′_P|。0.7.x 把 n 寫死為常數 N（full 設定 2），validator 數固定 1023 時 2 × 1023 = 2046 ≥ 600 沒問題；0.8.0 允許集合小到 6 人，若 n 仍是 2 就只有 12 張，永遠填不滿 E = 12 以外的任何設定——tiny 的 E 正好是 12，剛好夠但零裕度。改成 n = ⌈2E/|γ′_P|⌉ 之後，總容量 ≥ 2E，是需求的兩倍：容許約一半的 validator 離線、或 ticket 分數不佳被擠掉，accumulator 仍能填滿。2 這個係數 GP 沒有另外解釋，但從「容量 = 2 × 需求」讀出來就是安全裕度。full 設定 n = ⌈1200/1023⌉ = 2 與舊常數相同，所以對既有實作零改動；tiny 6 人 n = 4，這也是 ecosystem-notes 提醒的舊向量 tickets_per_validator: 3 已失效的原因。",
 "trap": "湊不滿就整個 epoch 沒匿名，所以容量抓兩倍。"
},
{
 "id": "d2-six-second-slot-one-hour-epoch",
 "lens": "設計",
 "alsoCh": [
  "6"
 ],
 "ch": "4",
 "section": "4.8 Epochs and Slots",
 "gpRef": "§4.8 prose, §I (P = 6, E = 600)",
 "difficulty": 1,
 "kind": "rationale",
 "tags": ["Safrole", "timeslot"],
 "stemZh": "slot 固定 6 秒、epoch 固定 600 個 slot（一小時）。GP 對「6 秒」這個數字的定位是什麼？Safrole 在這個時間結構上要「嚴格減少」的兩種東西是什麼？",
 "optionsZh": [
  "6 秒是「JAM block 之間的最小間隔」，不是保證每 6 秒一定有 block。Safrole 要嚴格減少的兩種 fork：slot 內的競爭與跨 slot 的競爭（不同 slot 的兩個有效 block 有同一個 parent）。epoch 是輪替、ticket 與 entropy 的單位；timeslot 用 32 位元",
  "6 秒是網路傳播延遲的實測值：1023 個 validator 之間 gossip 一個 block 平均要 6 秒。Safrole 要減少的是空 slot 與 orphan block。epoch 一小時是為了讓 GRANDPA 每小時定案一次",
  "6 秒是 accumulate 的 gas 預算換算成時間的結果：3.5·10⁹ gas 約需 6 秒。Safrole 要減少的是 ticket 不足與 fallback 次數。epoch 長度隨 validator 數調整，1023 人時是 600 個 slot，六人時是 60 個 slot，維持約一小時",
  "6 秒與 600 沒有特別理由，是從 Polkadot 的 6 秒 slot 與 1 小時 session 直接沿用；Safrole 要減少的是 validator 離線與 equivocation。timeslot 用 64 位元"
 ],
 "stem": "Slots are fixed at 6 seconds and epochs at 600 slots (one hour). How does the GP position the number 6 seconds, and what two things does Safrole set out to 'strictly minimize' on this time structure?",
 "options": [
  "6 seconds is 'the minimum time between JAM blocks', not a promise of one every 6 seconds. Safrole strictly minimizes forks from contention within a slot and across slots (two valid blocks in different slots sharing a parent). The epoch is the unit of rotation, tickets and entropy; timeslots are 32-bit",
  "6 seconds is the measured network propagation delay: gossiping a block among 1023 validators takes about 6 seconds on average. Safrole minimizes empty slots and orphan blocks. The one-hour epoch lets GRANDPA finalize once an hour",
  "6 seconds is the accumulate gas budget converted to time: 3.5·10⁹ gas takes about 6 seconds. Safrole minimizes ticket shortages and fallback occurrences. The epoch length scales with the validator count, 600 slots at 1023 validators and 60 slots with six, keeping epochs about an hour",
  "6 seconds and 600 have no particular reason; they are carried over from Polkadot's 6-second slot and one-hour session. Safrole minimizes validator downtime and equivocation. Timeslots are 64-bit"
 ],
 "answer": 0,
 "optNotes": [
  "對：§4.8 原文「This six-second slot period represents the minimum time between JAM blocks, and through Safrole we aim to strictly minimize forks arising both due to contention within a slot… and due to contention over multiple slots」；timeslot ∈ N_{2^32}，壽命到 2840 年。",
  "GP 沒有給傳播延遲數據；GRANDPA 不是每小時定案，它持續運作。",
  "gas 與 slot 長度沒有換算關係；E = 600 是常數，不隨 validator 數變。",
  "GP 明確給了 fork 最小化的理由；timeslot 是 32 位元（eq. 4.x 的 N_{2^32}）。"
 ],
 "explanation": "§4.8 原文三句話：「The Safrole mechanism subdivides time following genesis into fixed length epochs with each epoch divided into E = 600 timeslots each of uniform length P = 6 seconds, given an epoch period of… one hour.」「This six-second slot period represents the minimum time between JAM blocks, and through Safrole we aim to strictly minimize forks arising both due to contention within a slot (where two valid blocks may be produced within the same six-second period) and due to contention over multiple slots (where two valid blocks are produced in different time slots but with the same parent).」「the lifespan of the proposed protocol takes us to mid-August of the year 2840.」三個重點：(1) 6 秒是下限不是節拍——作者離線的 slot 就是空的，下一個 block 可以隔 12 秒、18 秒；(2) 兩種 fork 正對應 BABE 的兩個常見狀況（同 slot 多人中籤、空 slot 後接同一 parent），這就是 Safrole「提前一個 epoch 排好、恰好一人一 slot」的動機（d2-safrole-vs-babe-when-author-known）；(3) epoch 是所有週期性事務的單位：validator 輪替（eq. 6.14）、ticket 比賽（提交到 Y = 500 為止）、entropy 快照（eq. 6.23）、統計歸檔（§13）、ξ 與 ω 的環長。這題難度低，但「6 秒是最小間隔」這個定位口試常被追問：「那 block 之間可以多久？」答：任意長，只要 H_T 遞增且不在未來（ch05-timeslot-validity）。",
 "trap": "6 秒是「最快」不是「一定」；Safrole 要殺的是兩種 fork。"
},
{
 "id": "d2-offender-zeroed-not-removed",
 "lens": "設計",
 "alsoCh": [
  "10",
  "11"
 ],
 "ch": "6",
 "section": "6.2 (Φ)",
 "gpRef": "eq. 6.14 (Φ, §6.2), §6.2 prose, eq. 6.8 (|V| multiple of 3), eq. 11.20",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["dispute", "validator set", "authorizer"],
 "stemZh": "offender 的 key 在下次輪替時被 Φ 換成全零 key，而不是從集合裡移除。GP 只寫了做法。從其他規則可以推出什麼理由？全零 key 在協定裡會產生什麼效果？",
 "optionsZh": [
  "推論：協定用 index 指涉 validator（H_I、assurer index、credential 與判定的 index），移除一個會讓後面的人全部位移；且 eq. 6.8 要求大小是 3 的倍數、core 數 = |κ|/3。效果：全零 key 簽不出任何簽章，它的 slot 會空、它的 core 只剩兩位可用的 guarantor，其他人的 index 完全不動",
  "理由：GP 要保留 offender 的位置好在下個 epoch 恢復他，全零只是暫時停權；效果是那個位置的 slot 由 fallback 序列補上，core 的三位 guarantor 由 M* 從 λ 補一位",
  "理由：移除需要重新計算 ring root γ_Z，成本太高；全零 key 讓 ring root 不用重算。效果是 offender 仍能投 ticket（ring 裡還有他），只是 seal 會失敗",
  "理由：與 Polkadot 相容，Polkadot 的 validator set 也是用零 key 標記被踢出的人；效果是統計 π 對那個 index 停止計數，其餘規則把零 key 當成不存在、集合實質縮小，之後每次輪替都如此，所以每多一個 offender core 數就少一個，直到 delegator 重新填 ι"
 ],
 "stem": "An offender's key is replaced by an all-zero key by Φ at the next rotation rather than removed from the set. The GP states only the mechanism. What reason can be inferred from the other rules, and what effect does an all-zero key have inside the protocol?",
 "options": [
  "Inferred: the protocol names validators by index (H_I, assurer index, credential and judgment indices), so removing one shifts everyone after it, and eq. 6.8 needs the size to stay a multiple of 3 with cores = |κ|/3. Effect: a zero key cannot sign, so its slots go empty and its core keeps two usable guarantors, while all other indices stay put",
  "Reason: the GP keeps the offender's slot so it can be reinstated next epoch, the zero key being a temporary suspension; the effect is that its slots are filled by the fallback sequence and its core gets a third guarantor from λ via M*",
  "Reason: removal would require recomputing the ring root γ_Z, which is too expensive, so a zero key avoids the recomputation. The effect is that the offender can still submit tickets, since it remains in the ring, but its seals fail",
  "Reason: compatibility with Polkadot, whose validator set also marks ejected members with zero keys; the effect is that the statistics π stop counting that index while every other rule treats the zero key as absent and the set effectively shrinks for every later rotation, so the core count drops by one for each offender until the delegator refills ι"
 ],
 "answer": 0,
 "optNotes": [
  "對：§6.2 只說「replaced with a null key containing only zeroes」；index 指涉散見 eq. 5.10、11.13、11.28、10.4；eq. 6.8 的 3 的倍數與 eq. 11.20 的 |κ′|/3 分組是「不能移除」的硬約束。詳解標明這是推論。",
  "GP 沒有恢復機制，ψ_O 是累積的；fallback 與 M* 都不做「補位」。",
  "γ′_Z 每個 epoch 本來就重算（eq. 6.14 的 z）；零 key 不在 ring 裡有效，投不了 ticket。",
  "Polkadot 沒有這種零 key 標記；GP 也沒有「當成不存在」的規則，集合大小不變。"
 ],
 "explanation": "GP 的原文只有一句（§6.2）：「Note that on epoch changes the posterior queued validator key sequence γ′_P is defined such that incoming keys belonging to the offenders ψ′_O are replaced with a null key containing only zeroes.」沒有解釋為什麼不直接移除。以下是從其他規則推出的理由，口試時要標明是推論。第一，**index 是身分**：eq. 5.10 的 H_I、eq. 11.13 的 assurer index、eq. 11.28 credential 裡的 (index, sig)、eq. 10.4 verdict 判定的 index，全部是「第幾個」而不是「哪把 key」。移除第 k 個，第 k+1 個之後全部位移，跨 epoch 的 verdict（對 λ 驗）和跨 rotation 的 guarantee（M*）就會對錯人。第二，**大小是結構**：eq. 6.8 要求 |V| 是 3 的倍數，eq. 11.20 的指派把 validator 每 3 個一組對到 core，啟用 core 數 = |κ|/3；移掉一個人，整個 epoch 的 core 數、分組、洗牌全部改變，而 eq. 11.18 在 |κ| ≠ |κ′| 時還會把 ρ‡ 全清。所以「留位子、換成廢 key」是最小擾動的做法。效果：全零的 Bandersnatch key 與 Ed25519 key 都不是合法公鑰，任何簽章都驗不過——它排到的 slot 沒人能 seal（空 slot），它被指派到的 core 只有另外兩位 guarantor 能簽（eq. 11.28 允許 2 個簽章，所以 core 還能運作），ticket 也投不出來（ring 裡對應的是零點）。這正是 ch06-ring-root-nulled-keys 那題的機制面。",
 "trap": "index 不能動、大小不能動，所以只能把 key 廢掉留位子。"
},
{
 "id": "d2-gas-per-basic-block-why",
 "lens": "設計",
 "alsoCh": [
  "B"
 ],
 "ch": "A",
 "section": "A.9 Gas Cost Model",
 "gpRef": "§A.9 prose, eq. A.54 (gas cost for block), eq. A.22 (jump-table alignment), §A.3 (basic blocks)",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["gas", "PVM", "basic block"],
 "stemZh": "0.8.0 把 gas 改成「進入 basic block 時預扣整塊」。為什麼以 block 而不是以指令為單位計價？這個決定跟「間接跳躍必須落在 block 起點」有什麼關係？",
 "optionsZh": [
  "因為 §A.9 的模型是對每個 basic block 模擬 CPU 微架構——decode slot、執行單元、reorder buffer；指令會重疊，只有整塊的成本有意義，而且它是靜態的，recompiler 只要在入口扣一次。既然在入口扣，控制流就只能從 block 起點進入，這就是 eq. A.21 要求目標在 ϖ 裡的原因",
  "因為指令太多，逐條查表太慢；以 block 為單位可以把查表次數減到約十分之一。跟間接跳躍的關係是：跳到 block 中間會讓計數器重複扣同一塊，所以禁止",
  "因為 gas 要跟 wall-clock 對齊，而 CPU 是一次執行一整個 cache line；basic block 大約等於一個 cache line。間接跳躍限制在起點是為了 cache 對齊，跟計價無關",
  "因為 host call 的成本是動態的，只有把 host call 排除在 block 之外、其餘指令整塊計價才能讓成本可預測。間接跳躍必須落在起點是因為 jump table 只存 block 起點的位址，這是編碼格式的限制，繼承自 RISC-V"
 ],
 "stem": "0.8.0 charges gas for a whole basic block up front on entry. Why price by block rather than by instruction, and how does that decision relate to 'indirect jumps must land on a block start'?",
 "options": [
  "Because §A.9's model simulates a CPU microarchitecture — decode slots, execution units, reorder buffer — per basic block; instructions overlap, so only a whole block's cost is meaningful, and it is static, so a recompiler deducts once per entry. Since the charge is on entry, control may enter only at block starts, hence eq. A.21's ϖ requirement",
  "Because there are too many instructions for a per-instruction table lookup to be fast; pricing by block cuts lookups to roughly a tenth. The link to indirect jumps is that jumping into the middle of a block would charge the same block twice, so it is forbidden",
  "Because gas must track wall-clock time and a CPU executes a whole cache line at once; a basic block is roughly one cache line. Restricting indirect jumps to block starts is about cache alignment and unrelated to pricing",
  "Because host-call costs are dynamic, and only by excluding host calls from blocks and pricing the remaining instructions as a unit can costs be predictable. Indirect jumps must land on starts because the jump table stores only block-start addresses, a constraint of the encoding format inherited from RISC-V"
 ],
 "answer": 0,
 "optNotes": [
  "對：§A.9 原文；eq. A.8 在進入 block 時扣 ϱ^Δ；eq. A.21 要求目標 ∈ ϖ；appA-jump-semantics 那題從另一面講同一件事。",
  "查表速度不是 GP 的理由；跳到中間的問題是「少扣」不是「重複扣」。",
  "GP 的模型是 decode / 執行單元 / reorder buffer 的管線模擬，不是 cache line；跳躍限制正是為了計價。",
  "host call 有自己的計費（M_∅ 與各自基本成本），沒有被「排除」；jump table 存的是位址，限制來自語意不是格式。"
 ],
 "explanation": "§A.9 開頭原文：「The gas cost model for the PVM is a simplified model of a modern CPU microarchitecture, heavily inspired by what's used by production-grade compilers to predict how much time a given piece of code will take. For each basic block in the program the model simulates its execution flow and computes the required number of virtual CPU cycles that would be needed to execute it.」模擬的東西包括 decode slots、每週期能啟動的指令數、執行單元（ALU / LOAD / STORE / MUL / DIV）、reorder buffer 與指令間的依賴。在這種模型裡，兩條相鄰指令的成本取決於它們能不能重疊、有沒有依賴，所以「指令 A 的成本」不是一個獨立的數字，只有「這一整段直線程式碼的週期數」是。這自然把計價單位推到 basic block（從入口到 terminator 的直線段）。第二個好處是靜態：block 的內容在 deblob 時就固定，成本可以一次算好，eq. A.8 在進入 block 時扣 ϱ^Δ(𝔏(ı))，recompiler 把它編成入口的一條減法。第三個後果才是這題的重點：既然扣款只在入口，就必須保證執行只能從入口進來。靜態跳躍編譯期就能檢查；間接跳躍（jump_ind、load_imm_jump_ind）的目標是暫存器算出來的，只能在執行期驗證，eq. A.21 因此要求目標 ∈ ϖ（block 起點集合），否則 panic。不然一支程式可以反覆跳進某個 block 的中段，白跑後半段指令，計價模型整個崩潰。appB-grow-heap-semantics 那題講的「指令成本不能依賴運算元」也是同一個原則的另一面。",
 "trap": "指令會重疊所以只能整塊算；整塊預扣所以只能從頭進。"
},
{
 "id": "d2-staking-out-of-scope-why",
 "lens": "設計",
 "alsoCh": [
  "ARCH",
  "9"
 ],
 "ch": "4",
 "section": "4.8; 4.9; 21 Conclusion",
 "gpRef": "§4.8 prose (proof-of-authority, staking out of scope), §4.9 (coretime out of scope), §B (designate, assign), §21",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["coretime", "privileges"],
 "stemZh": "GP 把 staking、token 經濟、coretime 銷售全部標為 out of scope，卻又說 JAM 是 proof-of-authority。那 validator 到底由誰決定？這種「協定只留 API、經濟交給 service」的切法在保什麼？",
 "optionsZh": [
  "§4.8：validator「decided by a staking mechanism residing within some system hosted by JAM. The staking system is out of scope… instead there is an API」——就是 delegator 的 designate 寫 ι；coretime 同理由 assigner 的 assign 寫 φ。協定只定「誰能寫、寫到哪」，不定內容怎麼決定，經濟邏輯可以當 service 演進",
  "validator 由 genesis 固定，之後只能透過 GP 版本升級更換；staking 標為 out of scope 是因為 JAM 目前是許可制的測試網，之後的版本才會加入。切法保的是規格穩定，先凍結核心再談經濟；designate 這個 host call 只是讓治理公投能在版本之間輪換許可制的集合",
  "validator 由 GRANDPA 投票決定：每個 epoch 結束時 validator 互相投票選出下一期的集合，這是 proof-of-authority 的意思。staking out of scope 是因為 Polkadot 的 staking pallet 會直接搬過來當 relay 用，不需要在 GP 定義",
  "validator 由 manager service 用 bless 直接寫進 κ；coretime 由 registrar 用 new 分配。切法保的是效率，把經濟邏輯放在鏈上會拖慢 accumulate"
 ],
 "stem": "The GP marks staking, token economics and coretime sales all out of scope, yet calls JAM proof-of-authority. So who decides the validators, and what does this 'protocol keeps only the API, economics go to services' cut protect?",
 "options": [
  "§4.8: validators are 'decided by a staking mechanism residing within some system hosted by JAM. The staking system is out of scope… instead there is an API which may be utilized to update these keys' — the delegator's designate writing ι; coretime likewise goes through the assigner's assign writing φ. The protocol fixes who may write into which state, not how it is decided, so economics can evolve as services",
  "Validators are fixed at genesis and can only be changed through a GP version upgrade; staking is out of scope because JAM is currently a permissioned testnet, with staking to be added in a later version. The cut protects specification stability: freeze the core first, discuss economics later; the designate host call exists only so that a governance referendum can rotate the permissioned set between versions",
  "Validators are chosen by GRANDPA voting: at the end of each epoch validators vote among themselves on the next set, which is what proof-of-authority means. Staking is out of scope because Polkadot's staking pallet will be ported over as a relay and needs no definition in the GP",
  "Validators are written straight into κ by the manager via bless; coretime is allocated by the registrar via new. The cut protects efficiency, since putting economic logic on-chain would slow accumulate"
 ],
 "answer": 0,
 "optNotes": [
  "對：§4.8 原文；§4.9「Its procurement is out of scope… expected to be managed by a system parachain operating within a parachains service」；§B 的 designate 寫 ι、assign 寫 φ；§21 列出 token/coretime/staking 為刻意留白。",
  "validator 集合可由 designate 隨時更新，不是 genesis 固定；GP 沒說測試網或之後才加。",
  "GRANDPA 只管 finality，不選 validator；GP 沒有「搬 pallet」的說法。",
  "bless 改的是 χ（誰是 manager/delegator/assigner），不直接寫 κ；new 建 service 不分配 coretime。"
 ],
 "explanation": "§4.8 原文：「JAM defines a proof-of-authority consensus mechanism, with the authorized validators presumed to be identified by a set of public keys and decided by a staking mechanism residing within some system hosted by JAM. The staking system is out of scope for the present work; instead there is an API which may be utilized to update these keys, and we presume that whatever logic is needed for the staking system will…」proof-of-authority 在這裡的意思是「協定只認一組公鑰」，至於這組公鑰怎麼來的（質押、選舉、指派）協定不管。那個 API 是 §B 的 designate：只有 χ_V 指定的 delegator service 能呼叫，寫入 ι′，經兩次輪替成為 κ（d2-designate-to-authoring-lag）。coretime 完全平行：§4.9「Its procurement is out of scope in the present work and is expected to be managed by a system parachain operating within a parachains service」，API 是 assign，只有 χ_A[c] 指定的 assigner 能呼叫，寫入 φ[c]。而誰是 delegator、assigner、registrar，由 χ_M（manager）用 bless 決定。所以協定提供的是一組「權限 + 寫入口」的骨架：manager → 指定各角色 → 各角色各寫一個 state 分量 → 協定機械地消費那些分量。經濟邏輯（怎麼質押、怎麼拍賣、怎麼發幣）全在 service 的 accumulate 裡，§21 也把 token/coretime/staking 列為刻意留白。保的東西：這些邏輯可以像任何 service 一樣升級（upgrade host call 換 code）、替換（bless 換 delegator）、甚至並存，而 GP 本身不動。這跟「core 無定見」（d1-core-unopinionated-what-binds）是同一個哲學：協定定義機制，不定義政策。",
 "trap": "GP 只給「誰能寫、寫到哪」：designate → ι、assign → φ、bless → χ。怎麼決定寫什麼，是 service 的事。"
},
{
 "id": "d2-why-digest-not-state-diff",
 "lens": "設計",
 "alsoCh": [
  "ARCH",
  "4"
 ],
 "ch": "12",
 "section": "4.9 On Services and Accounts; 12",
 "gpRef": "§4.9 prose (refinement vs accumulation), §12 prose, §2.1",
 "difficulty": 2,
 "kind": "rationale",
 "tags": ["Polkadot", "accumulate", "work-digest"],
 "stemZh": "Polkadot 的 core 跑完 PVF，輸出就是 parachain 的新狀態（head data / state root），relay chain 只負責記錄。JAM 的 core 跑完 refine，輸出只是一小段 digest，然後還要在鏈上跑 service 的 accumulate 才決定狀態怎麼變。多這一步在買什麼？",
 "optionsZh": [
  "買的是結果進入同一個狀態機：§4.9 說 accumulate 提供「transferring balance and invoking the execution of code in other services」。core 若直接輸出狀態差異，只能改自己的 service，又回到 parachain 的隔離。讓鏈上 code 決定 digest 怎麼入帳，service 才能互動；代價是人人重跑 accumulate，所以 gas 小、輸入限 48 KB",
  "買的是安全：core 上的三位 guarantor 可能作弊，直接接受他們輸出的狀態太危險，所以鏈上要用 accumulate 重新驗證一遍 refine 的結果。這也是為什麼 accumulate 的 gas 比 refine 小很多：它只驗證不計算；accumulate 與 refine 結果不一致的 report 就是無效 report 的定義，會觸發 dispute",
  "買的是壓縮：parachain 的新狀態太大，塞不進 block；digest 只有 48 KB，鏈上再用 accumulate 把它展開回完整狀態。這一步純粹是為了頻寬，功能上與 Polkadot 相同",
  "買的是延遲容忍：refine 的結果要等 audit 完才安全，accumulate 這一步就是在等 audit；等到了才把 digest 套用到狀態。所以 accumulate 總是比 refine 晚一個 epoch"
 ],
 "stem": "Polkadot's core runs the PVF and its output is the parachain's new state (head data / state root), which the relay chain merely records. JAM's core runs refine and outputs only a small digest, after which the service's accumulate still has to run on-chain to decide how the state changes. What does the extra step buy?",
 "options": [
  "It buys results landing in one state machine: §4.9 says accumulate allows 'transferring balance and invoking the execution of code in other services'. A core emitting a state diff could only edit its own service — parachain isolation again. Letting on-chain code book the digest is what lets services interact, at the price that everyone re-runs accumulate, hence small gas and the 48 KB cap",
  "It buys safety: the three guarantors on the core may cheat, so accepting their output state directly is too dangerous, and accumulate re-verifies refine's result on-chain. That is also why accumulate's gas is much smaller than refine's: it only verifies, it does not compute; a report whose accumulate disagrees with its refine is the definition of an invalid report and triggers a dispute",
  "It buys compression: a parachain's new state is too large for a block; the digest is at most 48 KB and accumulate expands it back into the full state on-chain. The step is purely about bandwidth and functionally identical to Polkadot",
  "It buys latency tolerance: refine's result is only safe once audited, and the accumulate step is where the chain waits for the audit, applying the digest to state only then. Accumulate therefore always trails refine by one epoch"
 ],
 "answer": 0,
 "optNotes": [
  "對：§4.9 對 accumulation 的描述；§2.1 對 parachain 隔離的批評；§1.2 的 coherency；accumulate 的 gas 與 48 KB 上限（W_R）是這個設計的直接後果。",
  "accumulate 不重跑 refine，也驗證不了它（看不到 package）；正確性靠 audit 與 dispute。",
  "digest 不是壓縮後的狀態，是 refine 的任意輸出；accumulate 是執行 service 的邏輯，不是解壓。",
  "accumulate 在 available 時就跑，通常在 audit 之前（d1-accumulate-before-audit）；不等 audit、也不隔一個 epoch。"
 ],
 "explanation": "§4.9 對兩個入口的描述：refine「acts as a sort of high-performance stateless processor, able to accept arbitrary input data and distill it into some much smaller amount of output data… known as a digest」；accumulate「is more stateful, providing access to certain on-chain functionality including the possibility of transferring balance and invoking the execution of code in other services. Being stateful this might be said to more closely correspond to the code of an Ethereum contract account.」Polkadot 的模式是 core 輸出「新狀態的承諾」，relay chain 記下 head data，parachain 之間要互動只能走 XCMP——§2.1 批評的正是這個：「a collection of independent ecosystems… very similar in ergonomics to bridged blockchains」。JAM 把「結果如何影響狀態」這個決定從 core 搬到鏈上、交給 service 自己的 code，於是同一個 σ 裡的 service 可以在 accumulate 中互相轉帳（transfer）、讀對方的 storage（read）、被對方的 transfer 喚醒（下一輪 Δ+）。這就是 §1.2 的 coherency：「the causal relationship possible between different elements of state and thus how well individual applications may be composed」。代價很直接：accumulate 是 on-chain、人人重跑，所以只能給很少的 gas（每 report 10⁷，全 block 3.5·10⁹）、輸入只能是 ≤ W_R = 48 KB 的 digest（n5-why-report-is-small），重的運算必須留在 refine。這也解釋了 refine 為什麼 stateless：所有需要 state 的邏輯都被推到 accumulate 這一步，refine 只負責把大輸入變小。",
 "trap": "多一步 accumulate 是為了讓 service 能互動；代價是這一步必須小、必須人人跑。"
}
]
