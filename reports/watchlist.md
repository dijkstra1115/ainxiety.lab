# 實測候選清單（watchlist）

> tool-deep-dive 選目標時優先從這裡拿；介紹/實測完移入 seen.json 並從此表刪除。
> 條目格式：名稱、星數（記錄日）、取代誰、查證狀態。

## SaaS 平替線（優先）

- **browser-use/video-use**（18.3k ⭐，2026-08-02 查）：用 coding agent 剪影片。
  取代：付費 AI 剪輯訂閱（CapCut Pro / Descript 等，$10–24/月）。
  已驗證存在與星數；安裝方式與硬體需求未查，實測時確認。Python。
- **diwenne/openreply**（754 ⭐，2026-08-02 查）：IG 留言關鍵字自動私訊回覆（comment-to-DM）。
  取代：ManyChat（Pro 約 $15+/月起）。
  ✅ 已驗證走 Instagram 官方 API（README 明言不爬蟲、不要密碼）——可安心介紹。
  自架需求：Docker（Postgres + Redis）+ 自備免費 Meta 開發者 App 憑證 + Resend 帳號。
  MIT。星數不高但題材極符合定位，適合「小而美挖掘」角度。

## 上期雷達待實測

- **virgiliojr94/book-to-skill**（週報預告過，讀者點播優先）
- **usekaneo/kaneo**：取代 Jira/Trello 的自架 PM 工具，SaaS 平替線也適用
