# 實測候選清單（watchlist）

> tool-deep-dive 選目標時優先從這裡拿；介紹/實測完移入 seen.json 並從此表刪除。
> 條目格式：名稱、星數（記錄日）、取代誰、查證狀態。

## SaaS 平替線（優先）

- **diwenne/openreply**（754 ⭐，2026-08-02 查）：IG 留言關鍵字自動私訊回覆（comment-to-DM）。
  取代：ManyChat（Pro 約 $15+/月起）。
  ✅ 已驗證走 Instagram 官方 API（README 明言不爬蟲、不要密碼）——可安心介紹。
  自架需求：Docker（Postgres + Redis）+ 自備免費 Meta 開發者 App 憑證 + Resend 帳號。
  MIT。星數不高但題材極符合定位，適合「小而美挖掘」角度。
  ⚠️ 測試邊界：沙盒可測到「安裝→啟動→OAuth 牆」為止；連真實 IG 與觸發回覆
  需帳號主用自己的 Meta App 接力完成（接力流程順便演練 Phase 3 的 Meta 審核）。

## 企業數位轉型線（第一輪蒐集完成 2026-08-02，特輯已發）

實測/專題候選（星數為 2026-08-02 查證值）：
- **koishijs/koishi**（5.6k）：跨平台聊天機器人框架、支援 LINE——「LINE Bot 開發」專題核心
- **krayin/laravel-crm**（23.6k）：SME 定位 CRM，適合與 twenty 做對比篇
- **idurar/idurar-erp-crm**（8.6k）：輕量 ERP+CRM，「ERPNext 太重怎麼辦」角度
- **directus/directus**（37k）：資料庫直接變 headless CMS/後台，開發者向
- **filamentphp/filament**（31.7k）：Laravel 後台框架，「接案者工具箱」專題
- **nocobase/nocobase**：特輯已介紹，實測（真的拖一個內部系統出來）是強內容，優先級高

## 上期雷達待實測

- **virgiliojr94/book-to-skill**（週報預告過，讀者點播優先）
- **usekaneo/kaneo**：取代 Jira/Trello 的自架 PM 工具，SaaS 平替線也適用
