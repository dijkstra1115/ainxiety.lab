# ainxiety.lab

自動化工具實驗室。目前包含：

## 🔭 github-trending Skill

自動蒐集 GitHub 上星星數成長最快、最有爆火潛力的 repo，分析每個工具的：

- **用途**：它解決什麼問題
- **使用方式**：具體安裝與最小上手指令
- **費用**：完全免費 ✅ / 需要第三方 API key 🔑 / open-core 有付費版 💰

並產出繁體中文報告 + 可直接發布的 **Threads 貼文草稿**，存到 `reports/` 目錄。

### 資料來源（全部免費，不需付費服務）

| 來源 | 提供什麼 | 需要 API key？ |
|---|---|---|
| GitHub Trending 頁面（日榜/週榜） | 今日/本週新增星星數 | 不需要 |
| GitHub Search API | 近 30 天新建但已高星的「新秀」repo，計算每日星星成長速度 | 不需要（有 `GITHUB_TOKEN` 時自動使用，限流較寬） |
| WebFetch 備援 | 上述來源在受限網路環境失敗時的替代路徑 | 不需要 |

### 怎麼觸發

在 Claude Code / Claude 對話中說：

```
/github-trending
```

或自然語言：「幫我找這週 GitHub 上爆紅的 repo」。

### 搭配 Routines 定期執行

在 Claude 建立 Routine，排程（例如每週一早上）執行 prompt：

```
執行 github-trending skill，蒐集本週 GitHub 潛力 repo，
產出報告與 Threads 草稿，commit 並 push。
```

每次執行會：

1. 抓取三個來源的候選 repo
2. 比對 `reports/seen.json`，跳過 14 天內已介紹過的（不會重複發文）
3. 挑 5～8 個最有潛力的深入分析
4. 產出 `reports/YYYY-MM-DD-github-trending.md`（含 Threads 草稿）
5. commit + push，並在回覆中直接貼出草稿全文

### 手動跑抓取腳本（可選）

```bash
python3 .claude/skills/github-trending/scripts/fetch_trending.py --help
python3 .claude/skills/github-trending/scripts/fetch_trending.py --lang python --readme-top 5
```

只用 Python 標準函式庫，無任何第三方相依。

### 目錄結構

```
.claude/skills/github-trending/
├── SKILL.md                  # Skill 指令（Claude 讀這個）
└── scripts/fetch_trending.py # 抓取腳本（stdlib only）
reports/
├── YYYY-MM-DD-github-trending.md  # 每期報告
└── seen.json                      # 已介紹過的 repo（避免重複）
```
