# Threads API 申請與串接手冊（Phase 3 預備）

> 目的：當內容產線穩定跑 4–6 週後，把「複製貼上」升級為「一鍵發布」。
> Threads API 本身**完全免費**，成本只有申請流程的時間。
> 本文寫於 2026-08，Meta 流程可能變動，動手前先對照官方文件。

## 前置條件（先確認再開工）

1. **Instagram 專業帳號**（商業或創作者類型，個人帳號不行）並已連結你的 Threads 帳號
2. Meta 開發者帳號（developers.facebook.com）
3. **開發者身分驗證**：Meta 要求驗證你是「技術提供者」，獨立於一般註冊，約需 1 週

## 申請流程

1. 在 Meta for Developers 建立 App，加入 **Threads API** 產品
2. 申請兩個權限，各需獨立送審（**每個審核 2–4 週**，需附操作螢幕錄影）：
   - `threads_basic`——所有 Threads API 呼叫的基礎
   - `threads_content_publish`——建立與發布貼文
   - （之後想拉成效數據再加：`threads_manage_insights`）
3. 審核期間可用測試帳號開發，通過後正式帳號才能發文

## 技術要點

發布是**兩段式**（先建容器再發布），端點在 `graph.threads.net`：

```
# 1. 建立媒體容器（純文字例）
POST https://graph.threads.net/v1.0/{threads-user-id}/threads
  ?media_type=TEXT
  &text=貼文內容
  &access_token=...
→ 回傳 creation_id

# 2. 發布
POST https://graph.threads.net/v1.0/{threads-user-id}/threads_publish
  ?creation_id={上一步的 id}
  &access_token=...
```

- 圖片貼文：`media_type=IMAGE&image_url=...`——**圖片必須是公開 URL**，
  所以我們的卡片 PNG 屆時需要一個免費圖床（GitHub raw / Cloudflare R2 免費層皆可）
- 回覆串：發布後用 `reply_to_id` 接續，即可程式化建立「主文 + 連結回覆」結構
- 限制：文字 ≤500 字元、每 24 小時 ≤250 則、影片 ≤5 分鐘、輪播 ≤10 張

## 我們的串接計畫（保留人工把關）

```
skill 產出草稿+配圖 → 你在手機/桌面看一眼、改一兩句 →
對 Claude 說「發布」→ tools/publish_thread.py（屆時新增）：
  1. 上傳卡片 PNG 到圖床
  2. 建容器（主文＋圖）→ 發布
  3. 用 reply_to_id 補上連結回覆串
  4. 把貼文 id 寫入 reports/metrics.json 供之後拉成效
```

**永遠不做全自動盲發**——API 只是把「複製、開 App、貼上、傳圖」壓縮成一次確認。

## 時程建議

| 週次 | 動作 |
|---|---|
| 內容線穩定第 4 週 | 把 IG 帳號轉專業帳號、連結 Threads、送開發者身分驗證 |
| 第 5 週 | 建 App、送 `threads_basic` + `threads_content_publish` 審核 |
| 第 7–9 週 | 審核通過，寫 `tools/publish_thread.py`，跑一週人工對照 |
| 第 10 週起 | 一鍵發布上線，加送 `threads_manage_insights` 讓 metrics.json 自動回填 |

## 參考

- 官方文件：developers.facebook.com/docs/threads
- 流程綜述：[Postproxy 2026 指南](https://postproxy.dev/blog/how-to-post-to-threads-via-api/)、
  [Replia Threads API Guide](https://replia.net/blog/threads-api-guide)
