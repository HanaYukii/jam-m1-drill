# -*- coding: utf-8 -*-
SHEETS = [{'ch': '12',
  'title': 'Accumulation',
  'one': '把已 available 的 work-report 排成候選序列，在 gas 預算內執行各 service 的 accumulate，將工作結果套入鏈上 service 狀態，並產出 χ′ / '
         'ι′ / φ′ 與 output log θ′。',
  'flow': ['R = 本塊經 assurance 剛變 available 的 reports，不是本塊 E_G 新加入的所有 reports',
           'R! = 無 prerequisite 且 segment-root lookup 為空；R^Q = 其餘配上依賴並用 ξ 的聯集修剪',
           'ω 保存已 available、尚未累積且現在或曾經有依賴的 (report, 剩餘依賴集)',
           'ξ 是長度 E 的已累積 package hash 集合序列；每次 block transition 左移，末格加入本塊結果',
           'R* = R! ⌢ Q(q)；q = E(flatten(ω[m..]) ⌢ flatten(ω[..m]) ⌢ R^Q, P(R!))，m = H_T mod E',
           'Δ+ 挑可負擔的 report 前綴並遞迴；Δ* 本輪按 service 執行並合併；Δ1 組參數交給 Ψ_A',
           'deferred transfers 在同 block 後續 Δ+ 輪次整合；δ† 是整個 Δ+ 的帳戶結果，δ‡ 更新 last-accumulation record，δ′ 再整合 '
           'E_P'],
  'consts': [['E = 600', 'ξ 與 ω 長度相同，但 ξ 按 transition 左移，ω 按 slot 循環索引並清理跳過的 slots'],
             ['G_A / G_T', '每 report 的 digest accumulation gas 總上限 / block gas 基準；初始 g 依 eq. 12.24 取 max'],
             ['χ_M / χ_A / χ_V / χ_R',
              'manager / 每 core 的 assigner / delegator / registrar 索引，角色不必由不同 service 擔任'],
             ['χ_Z', 'service id → 基本 gas 配額的字典；第一輪帶入，即使沒有 report 或 transfer 也可觸發執行']],
  'eqs': [['eq. 12.1–12.3', 'ξ ∈ ⟦{H}⟧_E、ω ∈ ⟦⟦(ℝ, {H})⟧⟧_E 的型別與長度'],
          ['eq. 12.4–12.12', 'D 取依賴、E 刪項目並剪依賴、P 取 package hashes、Q 依序解鎖；R! 排在 Q(q) 前'],
          ['eq. 12.18', '依 service index 的確定順序串接 transfers，保留每個 service 輸出序列內的順序'],
          ['eq. 12.24–12.26', 'Δ+ 回傳 (n, e′, b, u, t)；e′ 給出 δ† 等狀態，b 形成 θ′']],
  'asked': [['為什麼需要 ω 和 ξ？',
             'ξ 記已累積的 package hashes，ω 記尚未處理的 reports 及剩餘依賴。兩者有界但更新方式不同；GP 的集合定義本身不保證實作查詢為 O(1)。'],
            ['Δ+ / Δ* / Δ1 為什麼分三層？',
             'Δ+ 以 gas limits 選前綴，再依 actual usage 決定後續輪次；Δ* 聚合同一 service 的工作以攤銷 PVM 啟動成本並合併結果；Δ1 組出單一 '
             'service 的 gas 與 operands，呼叫 Ψ_A。'],
            ['panic 或 OOG 會怎樣？',
             '附錄 B.4 的 collapse 採 exceptional context y；checkpoint 保存的變更、transfers、output 與 provisions '
             '可以留下。初始 context 已含 incoming transfer 入帳，actual gas used 仍回報；不能說全部回滾或 output 必空。已處理的 report '
             '前綴仍記入 ξ。'],
            ['deferred transfer 延到何時？',
             'sender 在局部 context 扣款並記錄 transfer，最終採用的 context 決定是否送出。合併後交給下一輪 Δ+ 的 receiver，通常仍在同一 block。δ‡ '
             '本身只更新最後累積時間，並非 transfer 執行階段。']],
  'delta': ['v0.8.0 ready queue 使用 ω；對照舊實作 Vartheta 時須區分 output log θ',
            'v0.8.0 的 χ 有 manager、assigners、delegator、registrar、always-accumulate 五類欄位；bless 檢查 manager 權限',
            'eq. 12.17 選前綴也要計入 transfer gas 與 free allowance；這與附錄 A 的 basic-block instruction gas 計費是不同層次'],
  'code': ['歷史 code-map：internal/accumulation/ 的 OuterAccumulation / ParallelizedAccumulation / '
           'SingleServiceAccumulation；PVM/accumulate_invocation.go 的 Psi_A',
           'Review 線索：unordered map 收集 transfer 或不穩定排序可能改變 operand 順序；是否仍存在須核對目前 checkout']}]
