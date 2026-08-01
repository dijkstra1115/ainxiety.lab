---
name: github-trending
description: 蒐集 GitHub 上星星數成長最快、最有爆火潛力的 repo，分析每個工具的用途、使用方式、是否需要額外 API key 或付費，並產出繁體中文報告與 Threads 貼文草稿。適用於「github trending」「爆紅 repo」「潛力專案」「今天有什麼新工具」等請求，或由 Routine 定期觸發。
---

# GitHub Trending 潛力 Repo 蒐集與分析

目標：找出「正在快速竄升」的 GitHub repo，產出一份可以直接拿去發 Threads 的繁體中文報告。整個流程只用免費資源（GitHub Trending 頁面 + GitHub 公開 API），不需要任何付費服務。

## 第 1 步：蒐集候選 repo

先嘗試跑腳本（結構化資料最完整）：

```bash
python3 .claude/skills/github-trending/scripts/fetch_trending.py \
  --readme-top 8 --out reports/latest_raw.json
```

腳本會抓三個來源並輸出 JSON：
- `trending_daily` / `trending_weekly`：GitHub Trending 頁面，含「今日/本週新增星星數」
- `rising_newcomers`：透過 Search API 找出近 30 天內建立、但已累積大量星星的年輕 repo，並算出 `stars_per_day`（星星成長速度）

**如果腳本回報 errors 或某個來源是空的（常見於網路受限的環境），改用 WebFetch 備援，不要放棄：**
- WebFetch `https://github.com/trending?since=daily`，請它列出所有 repo 的 full name、描述、總星數、今日新增星數
- WebFetch `https://github.com/trending?since=weekly`（同上，本週新增）
- 新秀 repo 備援：WebFetch `https://github.com/search?q=created%3A%3E{30天前日期}+stars%3A%3E200&type=repositories&s=stars&o=desc`；若也失敗，用 WebSearch 搜「site:github.com 最近爆紅的新工具」相關關鍵字補足

## 第 2 步：去重與挑選（編輯判斷是關鍵）

1. 讀取 `reports/seen.json`（不存在就當空的）。**14 天內已介紹過的 repo 直接跳過**，除非它有重大新動態（例如星星數翻倍、發布 1.0）。
2. 從所有來源合併去重後，挑出 **5～8 個**最值得介紹的。挑選標準（重要性排序）：
   - **成長速度**：daily 新增星數高、或 `stars_per_day` 高的年輕 repo，優先於總星數高的老牌專案
   - **對一般開發者/創作者實用**：讀者看完能直接上手用的工具 > 純研究性質的論文程式碼
   - **故事性**：新概念、解決普遍痛點、大廠開源、獨立開發者爆紅——這些在 Threads 上有話題性
   - **排除**：awesome-list 清單類、純教學課程類（如 xxx-for-beginners）除非成長異常驚人；已經人盡皆知的巨型專案（如 100k+ 星的老專案只是日常波動）

## 第 3 步：逐一深入分析

對每個選中的 repo，如果 JSON 裡已有 `readme_excerpt` 就先用它；不足或沒有時 WebFetch 該 repo 的 GitHub 頁面。每個 repo 必須回答以下問題（這是報告的核心，不能省略）：

1. **這是什麼**：一到兩句話講清楚它解決什麼問題，避免直譯官方口號
2. **為什麼有潛力／為什麼爆火**：成長數據 + 你的判斷（趨勢、話題、缺口）
3. **怎麼用**：具體的安裝與最小上手指令（例如 `pip install x` → 三行範例程式；或 Docker 一行跑起來）。從 README 裡找真實指令，不要編造
4. **需要額外 API key 或付費嗎**：明確分類——
   - ✅ 完全免費、離線可用
   - 🔑 需要第三方 API key（哪家？免費額度多少？）
   - 💰 核心免費但有付費雲端版 / open-core
   - 若 README 沒寫清楚，標註「README 未明說，需自行確認」，不要猜

## 第 4 步：產出報告

寫入 `reports/{YYYY-MM-DD}-github-trending.md`（日期用今天），結構：

```markdown
# GitHub 潛力雷達 {YYYY-MM-DD}

> 資料來源：GitHub Trending（日/週榜）+ 近 30 天新秀搜尋，共掃描 N 個候選

## 本期精選

### 1. owner/repo ⭐ 總星數（+今日新增 / 或 每日成長速度）
- **這是什麼**：…
- **為什麼值得關注**：…
- **快速上手**：
  ```bash
  （真實指令）
  ```
- **費用與 API**：✅/🔑/💰 …
- 🔗 https://github.com/owner/repo

（重複 5～8 個）

## 📱 Threads 貼文草稿

（見下方規格）

## 落選但值得觀察

- owner/repo：一句話說明為何暫不介紹但值得追蹤
```

**Threads 草稿規格**（放在報告內，讓使用者複製即發）：
- 繁體中文、口語、第一人稱，像分享給朋友，不要像新聞稿
- 第一行要是 hook（例如「這週 GitHub 上最猛的 5 個工具，第 3 個我已經在用了」）
- 每個 repo 一段：名字 + 一句話用途 + 是否免費 + 連結
- Threads 單則上限 500 字元，若超過就拆成主文 + 回覆串（在草稿中用 `---（回覆串 2）---` 分隔）
- 結尾附 2–3 個 hashtag（如 #GitHub #開源 #開發者工具）

## 第 4.5 步：產出配圖

用卡片產生器做 Threads 配圖（1080×1350 PNG，設定與相依見 `tools/make_card.py` 開頭註解）：

1. **radar 卡**（必做）：本期精選清單 → `reports/assets/{YYYY-MM-DD}/radar.png`
   ```bash
   python3 tools/make_card.py --type radar --data payload.json \
     --out reports/assets/{YYYY-MM-DD}/radar.png
   ```
   payload 的 `items[].delta` 用最有力的成長數字（如 `+10,558 ⭐ 週`），`desc` 控制在 20 字內避免截斷
2. **spotlight 卡**（選做）：本期成長王單獨一張，適合當第二張圖或隔日加熱貼文
3. 產完務必用 Read 檢視 PNG 確認無跑版、無截字，再寫進報告
4. 在報告的 Threads 草稿區塊註明每則貼文搭配哪張圖

## 第 5 步：更新狀態並提交

1. 更新 `reports/seen.json`：對每個本期介紹的 repo 記錄 `{"full_name": {"featured_on": "YYYY-MM-DD", "stars_at_feature": N}}`，保留歷史紀錄
2. 刪除 `reports/latest_raw.json`（中間產物不入版控）
3. `git add reports/ && git commit`（訊息格式：`report: github trending YYYY-MM-DD`）並 push 到當前分支
4. 在最後回覆中直接貼出 Threads 草稿全文，並附上報告檔案路徑，讓使用者不用點開檔案就能看到成果

## 注意事項

- GitHub Search API 未帶 token 時限流 10 次/分鐘；環境有 `GITHUB_TOKEN` 或 `GH_TOKEN` 時腳本會自動使用（30 次/分鐘）。都不需要付費。
- 星星數是輔助訊號不是全部：一個 3 天 800 星的小工具，比一個 10 年 8 萬星的老專案更符合本 skill 的目的。
- 描述工具用途時保持誠實：沒驗證過的功能寫「官方宣稱」，不要背書。
