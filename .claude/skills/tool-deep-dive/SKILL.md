---
name: tool-deep-dive
description: 從近期介紹過的潛力工具（reports/seen.json）挑一個最有教學價值的，在沙盒環境真的安裝、真的跑起來、記錄踩雷點，寫成「實測報告」Threads 草稿。適用於「實測 XX」「深度測試」「這個工具到底好不好用」等請求，或由 Routine 每週觸發。也可以直接指定 repo：「實測 owner/repo」。
---

# 工具實測報告

目標：帳號差異化的核心內容線——**別人翻譯 README，我們真的裝起來跑**。
產出物是一份誠實的實測筆記 + Threads 草稿（模板 C）。

## 第 1 步：選目標

- 使用者指定了 repo → 直接用
- 沒指定 → 讀 `reports/seen.json` 與最近兩期 `reports/*-github-trending.md`，挑選標準：
  1. **可在無 GUI 的 Linux 沙盒裡實測**（CLI 工具、library、Docker 服務優先；
     桌面 App / 手機 App 不行——只能做「安裝流程 + 文件深讀」的降級版並明說）
  2. 讀者上手門檻低（pip/npm/docker 一行裝）
  3. 上期雷達裡互動潛力最高的（agent 類、省錢類優先）
- 已寫過實測的（seen.json 中有 `deepdive:` 前綴）不重測，除非重大改版

## 第 2 步：真的裝、真的跑（時間盒：30 分鐘）

在沙盒環境按 README 實際操作，**過程全程記錄**：

1. 安裝：照官方指令裝。指令失敗、缺相依、版本衝突——這些雷全都是內容素材，記下來
2. 最小範例：跑通 README 的 quick start。需要 API key 的功能，若環境沒有 key
   就測到能測的邊界為止，並記錄「哪些功能被 key 擋住」
3. 進階一步：試一個 README 沒細講但讀者會想做的事（改設定、接自己的資料）
4. 計時與計量：從零到跑通花了幾分鐘？裝了多少 MB？記憶體吃多少？——具體數字是內容的靈魂

沙盒網路受限導致裝不了時：降級為「文件深讀 + issue 區考古」（看使用者實際抱怨什麼），
草稿中必須誠實標明「未能完整實測，以下基於文件與社群回饋」。

## 第 3 步：形成結論

必須回答：
- 👍 兩個真的好的點（具體到功能，不是「很好用」）
- 👎 至少一個雷或限制（沒有雷 = 沒測夠；再挖）
- 💰 費用真相：免費額度撐得起什麼強度的使用？什麼情況下會開始花錢？
- 🎯 一句話結論：「值得裝」「先觀望」「等 X 再說」＋適合誰/不適合誰

## 第 4 步：產出

寫入 `reports/{YYYY-MM-DD}-deepdive-{repo短名}.md`：

1. **完整實測筆記**：環境、每一步指令與輸出摘要、踩雷與解法、計時計量數據
   （這份筆記日後可擴寫成長文，是 Phase 4 的素材庫）
2. **Threads 草稿**（模板 C）：hook 用親測背書型；👍👎💰 各一行；結論明確；
   主文無連結；回覆串放安裝指令 + repo 連結
3. 測試產生的暫存目錄清乾淨，不要 commit 進 repo

## 第 4.5 步：產出配圖

verdict 卡（👍👎💰 三行 + 結論章）→ `reports/assets/{YYYY-MM-DD}/verdict-{repo短名}.png`：

```bash
python3 tools/make_card.py --type verdict \
  --data payload.json --out reports/assets/{YYYY-MM-DD}/verdict-{repo短名}.png
```

payload 的 points 每行控制在 30 字內；verdict_kind 依結論選 good（值得裝）/
warn（先觀望）/ bad（不推薦）。產完用 Read 檢視確認再收尾。

## 第 5 步：收尾

1. `reports/seen.json` 加入 `deepdive:owner/repo` 條目
2. commit（`report: deep dive owner/repo YYYY-MM-DD`）並 push
3. 回覆中貼出 Threads 草稿全文 + 實測筆記路徑

## 誠實守則（這條內容線的生命線）

- 只有親手跑過的才能寫「實測」；跑不了的部分寫「未測」
- 失敗的實測也是好內容：「我裝了 40 分鐘沒裝起來」對讀者一樣有價值，照發
- 不因為上期推薦過就護短——雷達推薦是「看起來有潛力」，實測打臉就誠實打臉，
  這種轉折反而是最高互動的內容
