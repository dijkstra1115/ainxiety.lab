# 特輯：幫中小企業砍掉月費的 6 套開源系統 2026-08-02

> 企業數位轉型線第一輪定向蒐集（topic:crm / topic:cms / 預約排程 / no-code 後台）。
> 星數與專案描述皆已逐一查證（2026-08-02）；「取代誰」欄的 SaaS 定價為公開牌價約略值，
> 發文前可再確認。此特輯與實戰案例線（🏢）互相支援——這些正是「我幫企業架過的那類系統」。

## 本期精選

### 1. twentyhq/twenty ⭐ 54.1k — CRM
- **這是什麼**：明言對標 Salesforce 的開源 CRM，為 AI 時代設計，TypeScript 全棧
- **取代誰**：Salesforce（每人每月 $25 USD 起）、HubSpot 付費版
- **適合**：需要客戶管理但養不起 Salesforce 的中小企業——台灣多數 B2B 公司其實只用得到 CRM 的 20% 功能，這 20% twenty 全有
- 🔗 https://github.com/twentyhq/twenty

### 2. calcom/cal.com（Cal.diy）⭐ 47.2k — 預約排程
- **這是什麼**：社群驅動的完全開源排程平台（Cal.com 移除商業程式碼的社群版），MIT
- **取代誰**：Calendly（每人每月 $10–16 USD）
- **適合**：顧問、診所、教育機構、任何「跟客戶約時間」的生意；注意它純自架、無官方託管版
- 🔗 https://github.com/calcom/cal.com

### 3. nocobase/nocobase ⭐ 23.5k — No-code 內部系統
- **這是什麼**：開源 AI + no-code 平台，拖拉出企業內部系統（審批、資產、報表）
- **取代誰**：Retool（每人每月 $10+ USD）、部分 Airtable 場景
- **適合**：「想要一個客製後台但不想從零開發」的所有情境——接案者的效率倍增器
- 🔗 https://github.com/nocobase/nocobase

### 4. TryGhost/Ghost ⭐ 54.6k — 內容官網＋電子報＋會員
- **這是什麼**：出版級 CMS，官網、電子報、付費訂閱會員一套搞定
- **取代誰**：Ghost Pro 託管（$9+/月）、Substack（抽成 10%）、WordPress 託管方案
- **適合**：內容型品牌與自媒體（對，我們自己的階段三電子報也可以用它）
- 🔗 https://github.com/TryGhost/Ghost

### 5. frappe/erpnext ⭐ 37.5k — ERP 全家桶
- **這是什麼**：完整開源 ERP：進銷存、會計、人資、製造
- **取代誰**：傳統 ERP 導入案（動輒六位數台幣起跳）與各種月費模組
- **適合**：規模到了、Excel 撐不住的公司；導入需要專業服務——這正是實戰案例線的商機所在
- 🔗 https://github.com/frappe/erpnext

### 6. halo-dev/halo ⭐ 39.5k — 建站工具
- **這是什麼**：對華語生態友善的開源建站系統：企業官網、部落格、知識庫、線上商店
- **取代誰**：Wix/Squarespace（$16+/月）、WordPress 託管費
- **適合**：只需要一個「好看、好管、不被月費綁」官網的中小企業
- 🔗 https://github.com/halo-dev/halo

## 📱 Threads 貼文草稿

> 配圖：`reports/assets/2026-08-02/radar-biz.png`

還在幫公司付這些月費嗎？這 6 套開源系統我大部分都幫客戶架過 👇

📇 twenty（54k ⭐）：開源版 Salesforce，中小企業要的 CRM 功能它全有
📅 Cal.diy（47k ⭐）：Calendly 每人每月收 $10，它免費自架
🧩 NocoBase（23k ⭐）：拖拉做出公司內部後台，取代 Retool

---（回覆串 2）---

📰 Ghost（54k ⭐）：官網＋電子報＋付費會員一套搞定，Substack 還要抽你 10%
🏭 ERPNext（37k ⭐）：進銷存會計人資全開源，傳統 ERP 報價看了會心痛的先看它
🌐 Halo（39k ⭐）：華語生態最友善的開源建站，官網不用再繳 Wix 月費

真心話：自架不是零成本——要一台主機和願意動手的人。但「月費 × 人數 × 12 個月」算下來，多數公司半年就回本。

你公司哪筆訂閱費最想砍？留言我幫你看有沒有平替

#開源 #數位轉型

---（回覆串 3：連結）---

twenty: github.com/twentyhq/twenty
cal.diy: github.com/calcom/cal.com
nocobase: github.com/nocobase/nocobase
ghost: github.com/TryGhost/Ghost
erpnext: github.com/frappe/erpnext
halo: github.com/halo-dev/halo

（這類系統的導入我有在幫企業做，需要可以聊聊）

## 落選但入 watchlist

- **koishijs/koishi**（5.6k）：跨平台聊天機器人框架、支援 LINE——LINE Bot 專題的候選核心
- **krayin/laravel-crm**（23.6k）：SME 定位 CRM，與 twenty 擇一介紹避免重複
- **idurar/idurar-erp-crm**（8.6k）：輕量 ERP+CRM，適合「ERPNext 太重」的讀者做對比篇
- **directus/directus**（37k）：資料庫直接變 headless CMS/後台，偏開發者向
- **filamentphp/filament**（31.7k）：Laravel 後台框架，接案者工具箱專題用
