---
name: ai-news
description: 蒐集過去 24 小時 AI 圈最重要的新聞與話題（Hacker News 高分討論、Hugging Face 熱門論文、重大產品發布），挑出最值得評論的 1 個主題寫成有立場的 Threads 短評草稿，附 2–3 條次要動態。適用於「今天 AI 圈發生什麼」「AI 新聞」「幫我寫今日短評」等請求，或由 Routine 每日/隔日觸發。
---

# 今日 AI 短評

目標：不是新聞搬運，是**挑一件事、給一個立場**。產出物是一則會讓人想留言吵架（好的那種）的
Threads 短評。全流程免費、不需 API key。

寫作規則與模板以 `docs/content-strategy.md` 和 `templates/threads-templates.md`（模板 B）為準。

## 第 1 步：蒐集（三層降級，逐層嘗試）

**層 1 — 腳本**（網路全開的環境最快）：
```bash
python3 .claude/skills/ai-news/scripts/fetch_ai_news.py --out reports/news_raw.json
```
抓 Hacker News 過去 24h 高分 AI 故事 + Hugging Face 今日熱門論文。

**層 2 — WebFetch**（腳本回報 errors 時）：
- WebFetch `https://news.ycombinator.com/`，請它列出 AI/ML 相關的高分故事
- WebFetch `https://huggingface.co/papers`，列出今日熱門論文

**層 3 — WebSearch**（前兩層都不通時，永遠可用）：
- 搜 `AI news today OpenAI Anthropic Google DeepMind` （限最近一天）
- 搜 `LLM model release announcement this week`
- 搜 `AI 新聞 今天`（補中文圈視角）

不論用哪層，目標是拿到 **8–15 個候選事件**，每個含標題、來源連結、熱度訊號（分數/討論數）。

## 第 2 步：選題（一主二副）

從候選中挑：
- **1 個主題**：對台灣/中文圈開發者有實際影響、你能給出非顯而易見立場的事。
  優先序：改變工作流的產品發布 > 定價/授權變動 > 重大模型發布 > 融資八卦（幾乎不選）
- **2–3 個次要動態**：一句話帶過即可，放回覆串
- 檢查 `reports/seen.json`：評論過的主題不重複評，除非有新進展

## 第 3 步：查證主題

對主題事件 WebFetch 原始來源（官方部落格/公告優先於二手報導），確認：
- 事實：發布了什麼、什麼時候可用、哪些地區/方案
- 價格與限制：免費額度、API 定價——讀者最關心
- 查證不到的部分明確標「尚未公布」，不要腦補

## 第 4 步：產出草稿

寫入 `reports/{YYYY-MM-DD}-ai-news.md`：

1. **事件摘要**（給自己看的完整版：事實、來源連結、背景）
2. **Threads 草稿**（模板 B）：
   - hook 是立場不是新聞標題（「X 發布了 Y」是壞 hook；「Y 這功能，我覺得大部分人不需要」是好 hook）
   - 主文 ≤500 字元、無連結、結尾低門檻提問
   - 回覆串放來源連結 + 次要動態
3. **落選事件清單**：一句話記錄為何沒選（下次選題參考）

## 第 4.5 步：產出配圖

quote 卡（主題事件的 hook 金句）→ `reports/assets/{YYYY-MM-DD}/quote-ainews.png`：

```bash
python3 tools/make_card.py --type quote \
  --json '{"date":"{YYYY-MM-DD}","label":"今日 AI 短評","quote":"...","context":"..."}' \
  --out reports/assets/{YYYY-MM-DD}/quote-ainews.png
```

quote 控制在 45 字內（超過會擠版），context 是一句事實背景。產完用 Read 檢視確認再收尾。

## 第 5 步：收尾

1. `reports/seen.json` 加入本次評論的主題（key 用 `news:{slug}`，格式與 repo 條目一致）
2. 刪除 `reports/news_raw.json`
3. commit（`report: ai news YYYY-MM-DD`）並 push
4. 回覆中直接貼出 Threads 草稿全文

## 注意事項

- 立場要具體但別造謠：批評基於已查證的事實與明說的推理，不臆測內部動機
- 「今天沒大事」也是合法產出：改發次要動態合輯（「本日三則小事」），不要硬把小事吹成大事
- 幣別注意：美元價格標 USD；換算台幣時寫「約」
