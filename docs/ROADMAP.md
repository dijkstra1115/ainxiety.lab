# ainxiety.lab 發展藍圖

> 目標：把這個 repo 經營成一座「AI 自媒體內容工廠」——用 Claude Routines 定期執行各個 Skill，
> 穩定產出高品質的繁中 AI/開發者內容，餵養 Threads 帳號，最終形成「自動蒐集 → 分析 → 草稿 →
> 人工把關 → 發布 → 成效回饋」的完整迴圈。

## 總覽

```
Phase 0 ─ 單一工具        github-trending（已完成 ✅）
Phase 1 ─ 內容矩陣        ai-news + tool-deep-dive + weekly-digest + 貼文模板庫
Phase 2 ─ 成效迴圈        記錄每篇貼文數據 → 回饋選題與 hook 寫法
Phase 3 ─ 半自動發布      Threads API（免費）串接，草稿一鍵發布
Phase 4 ─ 多平台漏斗      長文平台 + 電子報，Threads 當流量入口
```

每個 Phase 都遵守同樣的原則：**只用免費資源、人工把關發布、內容誠實不誇大**。

---

## Phase 0：單一工具（已完成 ✅）

- `github-trending` skill：三個免費來源蒐集竄升 repo → 繁中分析報告 + Threads 草稿
- 雙路徑設計（腳本直連 → WebFetch 備援），已在受限網路環境實測通過
- `reports/seen.json` 去重，避免定期執行重複發文

## Phase 1：內容矩陣（本次新增 🚧）

單一內容形式撐不起一個帳號。Threads 演算法偏好穩定發文（每週至少 3–5 則）與高回覆率內容，
所以需要多條內容線輪替，涵蓋不同互動型態：

| Skill | 內容線 | 形式 | 建議頻率 |
|---|---|---|---|
| `github-trending` | 挖掘型：竄升工具雷達 | 清單式（易轉發收藏） | 每週一 |
| `ai-news`（新）| 時事型：AI 圈今日大事 | 短評式（易引回覆討論） | 每日或每週二四 |
| `tool-deep-dive`（新）| 實測型：一個工具用到底 | 教學式（建立專業信任） | 每週三 |
| `weekly-digest`（新）| 統整型：本週回顧＋下週預告 | 長串式（漲粉主力） | 每週日 |

配套：
- `templates/threads-templates.md`：hook 句庫與貼文格式範本，所有 skill 共用，維持帳號一致的「聲音」
- 各內容線的草稿都遵守：**外部連結一律放「回覆串」而非主文**（外連主文會被降觸及）

### Routines 排程建議（全部設好後）

```
每週一 09:00  執行 github-trending skill
每週二 09:00  執行 ai-news skill
每週三 09:00  執行 tool-deep-dive skill（自動從 seen.json 挑本週最有教學價值的工具實測）
每週四 09:00  執行 ai-news skill
每週日 20:00  執行 weekly-digest skill（回顧本週 + 排下週）
```

先從每週 3 則開始（一、三、日），穩定後再加密度。

## Phase 2：成效迴圈（下一步 📊）

沒有回饋的內容工廠只是在猜。做法：

1. 新增 `reports/metrics.json`：每篇發出去的貼文記錄
   `{date, skill, hook_type, topic, views, likes, replies, reposts, followers_delta}`
2. 初期**手動回填**：發文後 48 小時，把 Threads 提供的洞察數據貼給 Claude，
   由 `weekly-digest` skill 順便寫入
3. `weekly-digest` 每週分析：哪類主題回覆率最高？哪種 hook 開頭表現最好？
   清單式 vs 短評式誰的轉發多？→ 產出「下週選題與寫法調整建議」
4. 累積 8–12 週數據後，讓各 skill 的挑選標準直接引用 metrics 結論
   （例如「agent 類工具歷史互動率最高，同分時優先」）

這一步不需要任何 API——Threads App 內建的洞察數據就夠用。

## Phase 3：半自動發布（條件成熟後 🚀）

Threads 官方 API **完全免費**，可程式化發文，但有前置成本：

- **帳號要求**：Instagram 專業帳號（商業或創作者）並連結 Threads
- **審核**：Meta 開發者身分驗證（約 1 週）+ `threads_basic`、`threads_content_publish`
  兩個權限各需 app review（每個 2–4 週，要錄操作影片）
- **技術**：`graph.threads.net` 兩段式發布（先建 container 再 publish），
  文字上限 500 字元，每天上限 250 則——對我們綽綽有餘
- **維持人工把關**：流程設計成「Claude 產草稿 → 你在手機上按一下確認 → API 發布」，
  而不是全自動盲發。自媒體帳號的信任是資產，發錯一篇的成本遠高於省下的十秒

建議在 Phase 1 穩定跑 4–6 週、確定要長期經營之後再申請（審核期剛好拿來累積內容）。

## Phase 4：多平台漏斗（規模化後 🌊）

Threads 適合引爆但不適合沉澱。當帳號有穩定互動後：

- **長文層**：每月把最好的 deep-dive 擴寫成長文（vocus / Medium，免費），Threads 導流
- **訂閱層**：電子報（Substack / Ghost 免費層），weekly-digest 直接改寫成 newsletter
- **同步層**：X/Twitter 中文圈同步發（內容複用，成本近零）
- repo 內對應新增 `newsletter/` 目錄與 `newsletter-draft` skill

漏斗：Threads 短內容（觸及）→ 長文（信任）→ 電子報（自有受眾，不受演算法綁架）。

---

## 維護與技術債

- [ ] GitHub push 權限：等 repo 授權修復後，所有本地 commit 一次推上
- [ ] `fetch_trending.py` 加上 429（rate limit）退避重試
- [ ] `seen.json` 超過 200 筆後改為按月分檔
- [ ] 各 skill 的 WebFetch 備援已驗證；若使用者環境網路全開，腳本路徑更快更省 token
- [ ] Phase 3 前先寫 `docs/threads-api-setup.md` 申請流程手冊

## 風險與原則

1. **平台依賴**：Threads 演算法隨時會改，Phase 4 的自有受眾（電子報）是保險
2. **內容誠實**：所有工具介紹標明「官方宣稱」vs「實測確認」；費用資訊查證不到就寫查證不到。
   自媒體最大的護城河是「這個帳號說的可以信」
3. **不盲發**：任何階段都保留人工確認那一步
4. **免費優先**：目前整條 pipeline 的現金成本為零（Claude 訂閱除外），保持這個狀態到有變現為止
