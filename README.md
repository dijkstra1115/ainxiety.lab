# ainxiety.lab

自媒體內容工廠——用 Claude Skills + Routines 自動蒐集、分析、產出繁中工具類內容
（定位：**幫你戒掉訂閱費的工具偵察兵**——挖掘能取代付費 SaaS 的免費/開源工具，
親測後告訴你值不值得換），餵養 Threads 帳號。全 pipeline 只用免費資源，發布前保留人工把關。

📖 發展藍圖：[docs/ROADMAP.md](docs/ROADMAP.md)
📖 經營策略與寫作規則：[docs/content-strategy.md](docs/content-strategy.md)
📖 貼文模板庫：[templates/threads-templates.md](templates/threads-templates.md)

## 內容 Skill 矩陣

| Skill | 內容線 | 建議排程 | 產出 |
|---|---|---|---|
| [`github-trending`](.claude/skills/github-trending/SKILL.md) | 🔭 竄升工具雷達 | 每週一 | 5–8 個潛力 repo 分析 + Threads 清單文 |
| [`ai-news`](.claude/skills/ai-news/SKILL.md) | 📰 今日 AI 短評 | 每週二、四 | 一主二副事件 + 有立場的短評文 |
| [`tool-deep-dive`](.claude/skills/tool-deep-dive/SKILL.md) | 🔧 實測報告 | 每週三 | 沙盒真裝真跑的實測筆記 + 實測文 |
| [`weekly-digest`](.claude/skills/weekly-digest/SKILL.md) | 📅 週報＋下週計畫 | 每週日 | 回顧文 + 內部選題計畫與成效分析 |

每個 skill 的產出都包含**可直接複製發布的 Threads 草稿**（含分串、連結放回覆串、
結尾提問——規則見經營策略文件）。

## 共同設計原則

1. **免費**：GitHub Trending/Search API、HN Algolia、HF papers 全部免費、不需 API key
   （有 `GITHUB_TOKEN` 時自動使用以放寬限流，也免費）
2. **三層降級**：腳本直連 → WebFetch → WebSearch，任何網路環境都能跑完
3. **去重**：`reports/seen.json` 記錄介紹過的工具與評過的事件，定期執行不重複
4. **誠實**：實測才寫實測、查不到就寫查不到、敢寫負評

## 配圖產線（零成本，不需繪圖 API）

每條內容線的草稿都會自動配一張 **1080×1350 品牌卡片**（Threads 動態最大版面），
由 `tools/make_card.py` 用 HTML 模板 + 無頭 Chromium 截圖產生：

| 卡片 | 用途 | 對應 skill |
|---|---|---|
| `radar` | 竄升工具排行清單 | github-trending |
| `spotlight` | 單一工具 + 巨大成長數字 | github-trending（成長王） |
| `quote` | 短評金句卡 | ai-news |
| `verdict` | 👍👎💰 實測結論 + 結論章 | tool-deep-dive |
| `digest` | 週回顧 3 條 + 下週預告 | weekly-digest |

一次性安裝（產圖相依）：

```bash
pip install pillow                        # 裁切到精確尺寸
npm install @fontsource/noto-sans-tc      # 中文字型（可選，無則退回系統字型）
```

設計採用經驗證的深色面板色票（對比全部通過 3:1），成品存 `reports/assets/{日期}/`。

## 快速開始

對 Claude 說：

```
/github-trending          # 或「幫我找這週爆紅的 repo」
/ai-news                  # 或「今天 AI 圈發生什麼」
/tool-deep-dive           # 或「實測 owner/repo」
/weekly-digest            # 或「本週回顧」
```

### Routines 排程（建議起手式：每週 3 則）

| Routine prompt | Cron（台北時間） |
|---|---|
| 執行 github-trending skill，產出報告與草稿，commit 並 push | 週一 09:00 |
| 執行 tool-deep-dive skill，實測本週雷達最值得測的工具 | 週三 09:00 |
| 執行 weekly-digest skill，回顧本週並規劃下週 | 週日 20:00 |

穩定後加入週二、四的 `ai-news` 升到每週 5 則。

## 目錄結構

```
.claude/skills/           # 四個內容 skill（各含 SKILL.md，部分含抓取腳本）
docs/                     # ROADMAP、經營策略
templates/                # Threads 貼文模板與 hook 句庫
reports/                  # 每期報告（含 Threads 草稿）
├── seen.json             # 去重紀錄
└── metrics.json          # 貼文成效（Phase 2 啟用）
```
