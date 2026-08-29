# JAM M1 Drill — 專案說明（給在本機接手的 Claude 用）

面向 **JAM Prize Milestone 1 口頭面試** 的題庫網站，給 New-JAMneration 團隊準備用。
線上版：https://hanayukii.github.io/jam-m1-drill/ ｜ Repo：https://github.com/HanaYukii/jam-m1-drill

## 這個 repo 目前只有編譯後的產物

`index.html`、`questions.json`、`jam-m1-qa.md` 都是 build 出來的。**原始碼在 `jam-m1-drill-src.tar.gz`**，
解開後是 `quiz/`（items / glossary / cheat / scripts / app / review）與 `research/`。
第一件該做的事：把原始碼解開並 commit 進 repo，讓團隊其他人拿得到能改的東西。

## 移植：一次性設定（在本機做一次就好）

解開 `jam-m1-drill-src.tar.gz` 之後，目錄長這樣：

```
jam-m1-drill/          ← git repo
  CLAUDE.md            ← 這個檔
  index.html           ← 編譯後的網站（GitHub Pages 從這裡發佈）
  questions.json  jam-m1-qa.md  README.md  REVIEW.md
  quiz/                ← 原始碼：items / glossary / cheat / scripts / app / review
  research/            ← 團隊 code 對照、issue 摘要、生態系筆記（別重做，很貴）
  gp-src/              ← Gray Paper LaTeX，用下面的指令抓（建議加進 .gitignore）
```

Gray Paper 原始碼是事實依據，用這兩行取得並釘在 0.8.0：

```
git clone https://github.com/gavofyork/graypaper.git gp-src
cd gp-src && git checkout 07f041d   # Release version 0.8.0
```

`quiz/scripts/*` 都用相對路徑，`quiz/` 與 `gp-src/` 是兄弟目錄就能跑。

## 不需要重做的事（這些是最貴的部分，已經做完了）

- **讀完整本 Gray Paper**：不必。要查什麼就 grep `gp-src/text/*.tex`，符號表在 `gp-src/preamble.tex`。
- **推導公式編號**：`quiz/scripts/eqnums.json` 已經從 LaTeX 推好並與 PDF 對過每節總數；用 `scripts/eqref.py` 查。
- **0.7.2 → 0.8.0 的符號對照**：已經全庫統一過（ϑ→ω、W 是 work-item 不是 work-report、𝕐 是 avspec、
  𝒟 是 shard 數函數而非 decoder、ticket entry index 是 i_e、ring root 在 𝔹_144）。
- **團隊 repo 與 issue 的整理**：在 `research/` 裡，共約 390 KB。
- **對抗式審查**：`quiz/review/` 有八組盲審紀錄與判決。

實務上，接手一個小任務（改幾題、補一章）只需要讀 `CLAUDE.md` + `quiz/AUTHORING.md` + 你要動的那個
`quiz/items/*.py` 模組，其餘用 grep 按需查。不要一開始就把整個 `items/` 或整本 GP 讀進脈絡。

## 建置流程

```
cd quiz
python3 scripts/validate.py     # contentGuard：欄位、4 選項、洩題、字母指涉、逐項辨析、選項長度線索
python3 scripts/optlen.py       # 單獨看長度線索（正解不能是最長或最短的那個）
python3 scripts/check_refs.py   # GP 公式編號不得超過該章實際數量
python3 scripts/build.py        # → dist/{questions.json, artifact.html, jam-m1-drill.html, jam-m1-qa.md}
node scripts/smoke.mjs          # Playwright：淺色/深色、作答、模擬考、錯題本、問答、速記、名詞、420px 無橫向溢出
```

部署 = 把 `dist/jam-m1-drill.html` 複製成 `index.html`、`dist/questions.json` 與 `dist/jam-m1-qa.md`
放到 repo 根目錄，commit 後 push。GitHub Pages 從 `main` 的根目錄發佈。

## 內容規則（`quiz/AUTHORING.md` 有完整版）

- 事實以 Gray Paper **0.8.0** 的 LaTeX 原始碼為準（`gp-src/text/*.tex`、符號表在 `preamble.tex`）。
  團隊實作在 0.7.2，**0.7.2 → 0.8.0 的差異是考點**，用 `delta-0.8.0` 標記。
- **口試導向**（第 7 條，最高優先）：問規則與理由，不問位元組偏移、opcode 編號、算到個位數的數字。
  判準是「候選人能不能開口答出來、面試官會不會這樣問」。
- 每題必須有 `optNotes`：四個選項各一句，**照原始碼順序**（build 時與選項一起洗牌）。
  正解那句給關鍵差異，干擾項那句點名具體錯處。
- 詳解用繁體中文、技術名詞保留英文，且**不得用字母指涉選項**（選項會被洗牌，validator 會擋）。
- 正解不能是最長或最短的選項（validator 會擋）——四個選項要「平行結構」：同樣多的子命題、同樣的顆粒度。

## 現況

270 題、92 條名詞解釋、21 章速記（§3–§14、附錄 A–H、架構）。
模式：練習 / 問答 / 速記 / 模擬考 / 錯題本 / 名詞。答完（不論對錯）都有「總說明 + 逐項辨析」。

## 待辦

1. 把原始碼放進 repo（見上）
2. 205 題重寫過干擾選項的盲審——只有選擇題模式會碰到，問答模式不受影響
3. §14（7 題）、附錄 C（5 題）、F（3 題）題數偏薄
4. 兩個團隊 Go code 的疑似 bug，要不要開 issue 由使用者決定：
   - `merkle_tree.T` 用 `len(v)/2`，GP eq. E.1 的 N 是 ⌈|v|/2⌉；`ce140.go:233` 對未補齊的 chunk slice 呼叫 T
   - `Δ*` 用 Go map 迭代順序處理 deferred transfer，eq. 12.18 要求 `s ↕ s` 排序，`sort.Slice` 又不穩定 → state root 可能分歧

## 使用者偏好

- 繁體中文溝通；對 macOS 終端機不熟，優先給 GUI 步驟或直接代為操作
- 不喜歡題目糾結細節（口試不是筆試）
- 在意 token 用量：不要一次開一大批 subagent
