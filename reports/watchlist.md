# 實測候選清單（watchlist）

## 專題素材包 A：Claude Code 生態爆發（2026-08-04 高星掃蕩，星數當日值）

> 2026 年的 breakout 榜幾乎被 Claude Code 生態霸榜——這本身就是一篇趨勢文的題目。
> 也是 build-in-public 線（#6 回覆串預告的「拆解我的產線」）的完美銜接素材。

- **affaan-m/ECC**（238k）：agent harness 效能優化系統——2026 星數第一的 breakout
- **mattpocock/skills**（204k）：Matt Pocock 的實戰 skills 合集
- **multica-ai/andrej-karpathy-skills**（200k）：Karpathy 洞察做成的 CLAUDE.md
- **ultraworkers/claw-code**（195k）：agent 自主管理的 Rust 專案，概念展示型
- **garrytan/gstack**（126k）：Garry Tan 的 23 工具 Claude Code 配置
- **Graphify-Labs/graphify**（103k）：codebase 變可查詢知識圖譜
- **DietrichGebert/ponytail**（96.3k）：讓 agent「像最懶的資深工程師一樣思考」
- **JuliusBrussee/caveman**（96k）：「講穴居人話」省 65% token——趣味+實用，單篇好題
- **karpathy/autoresearch**（93.2k）：單 GPU 自動跑研究的 agent

## 專題素材包 B：SaaS 平替常青樹（高星自架經典，適合平替特輯第二彈）

> 不是新聞，但每一個都有明確的「取代誰、省多少/月」，正是帳號定位的主場。

- **n8n-io/n8n**（199k）：取代 Zapier/Make（$20+/月起）
- **open-webui/open-webui**（148k）：自架 AI 對話介面，配本地模型可完全離線
- **immich-app/immich**（110k）：取代 Google Photos（100GB $2.99+/月）
- **louislam/uptime-kuma**（89.8k）：取代 Pingdom/UptimeRobot 付費版
- **Stirling-Tools/Stirling-PDF**（88.9k）：取代 Adobe Acrobat 訂閱（$19.99/月）
- **usememos/memos**（62k）：取代 flomo/Notion 的輕量筆記
- **coollabsio/coolify**（60.1k）：取代 Vercel/Heroku/Netlify 付費層
- **go-gitea/gitea**（57.2k）：取代 GitHub 私有方案/GitLab 雲端版
- **unslothai/unsloth**（69.6k）：本地微調訓練，配「小硬體跑大模型」專題


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
