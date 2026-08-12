# GitHub 潛力雷達 2026-08-12

> 資料來源：GitHub Trending（日榜 17 個 / 週榜 15 個）+ 近 30 天新秀搜尋
> （created:>2026-07-13, stars:>300）+ 兩輪定向搜尋
> （"open source alternative" created:>2026-05-14；self-hosted × booking/helpdesk/
> newsletter/invoice/ecommerce），共掃描約 65 個候選。
>
> 距上期（08-10）只有兩天，日/週榜重疊度高，seen.json 又擋掉 08-01～08-10 已介紹的 22 個，
> 因此本期權重幾乎全押在定向搜尋與新進榜單。結果反而更集中：
> **五個能直接對應到一筆月費的自架工具**，加上兩個成長異常的觀察標的。
>
> 註：技術上這輪的 `fetch_trending.py` 依然三個來源全 403（egress policy 擋 github.com /
> api.github.com 直連），資料全走 WebFetch 備援；成長數字取自 trending 頁面的日/週新增星數，
> 沒有腳本算的 `stars_per_day`。

## 本期精選

### 1. macro-inc/macro ⭐ 1,181（今日 +248）
- **這是什麼**：把 email、聊天、文件、任務、通話、CRM 全部做進同一個工作區，
  彼此雙向連結、共用一份團隊記憶。Rust 寫的，可完整自架
- **為什麼值得關注**：官方對標名單直接寫死——Slack、Linear、Notion、HubSpot、
  Superhuman、Salesforce。一間 10 人公司光這幾套疊起來每月輕鬆破 $300。
  更值得注意的是它**不是週末專案**：團隊 15 人自己內部用了兩年才開源，
  而且有 SOC 2 Type II 與 ISO 27001。AGPL-3.0、明說不是 open-core——
  也就是沒有「功能鎖在企業版」那套。本期我最想動手裝的一個
- **快速上手**：
  ```bash
  git clone https://github.com/macro-inc/macro.git
  cd macro
  nix develop
  just run_local
  ```
  （用 Nix 當開發環境，這在自架工具裡算少見，沒碰過 nix 的人要多花點時間）
- **費用與 API**：💰 軟體免費（AGPL-3.0），但官方有託管版 macro.com/app。
  🔑 自架仍需要串 Gmail / Google Workspace，AI 功能要自備 OpenAI / Google / Anthropic 金鑰
- 🔗 https://github.com/macro-inc/macro

### 2. msrbuilds/voice-studio ⭐ 174
- **這是什麼**：本地跑的 TTS 工作室，一個 Web UI 裡包了七個開源語音模型
  （VibeVoice-1.5B、Kokoro-82M、Kitten TTS Mini、Chatterbox 多語 V3、
  OmniVoice 600+ 語言、VoxCPM2、Qwen3-TTS），另外附 Whisper large-v3-turbo
  做轉錄。支援語音克隆、podcast 剪輯、跨語言配音
- **為什麼值得關注**：對標 ElevenLabs——那邊 Creator 方案 $22/月、Pro $99/月，
  而且字元數用完就得加購。做短影音旁白、有聲內容的人這筆是固定支出。
  這個專案的賣點是 README 寫得很硬：「no cloud, no telemetry, audio never
  leaves your machine」——聲音素材不外流這件事，對商用配音是實質差異
  而不只是隱私口號。星數只有 174，是本期最小的，但七個模型一次打包這件事
  省下的是自己拼環境的兩個晚上
- **快速上手**：
  ```bash
  git clone https://github.com/msrbuilds/voice-studio.git
  cd voice-studio
  python studio.py setup
  python studio.py start          # http://localhost:8880
  ```
- **費用與 API**：✅ 完全免費、完全離線（MIT，各模型另有自己的 MIT / Apache-2.0 授權），
  不需任何 API key。⚠️ 硬體是門檻：VibeVoice fp16 約需 3GB VRAM、VoxCPM2 約 8GB；
  全部模型下載完約 23GB 硬碟。純 CPU 跑得動但很慢
- 🔗 https://github.com/msrbuilds/voice-studio

### 3. hugohe3/ppt-master ⭐ 45,168（今日 +364）
- **這是什麼**：把文件、PDF 或一個主題，轉成**原生可編輯的 PowerPoint**——
  產出的是真的圖形、圖表、表格、轉場、動畫物件，不是把圖片貼滿版面。
  支援套自己的模板，還能從講者備忘稿生成旁白音軌
- **為什麼值得關注**：「AI 做簡報」這題 Gamma（$10–20/月）、Tome 都在做，
  但那些工具的通病是產出鎖在它自己的網頁編輯器裡，你要改就得回去改。
  這個直接吐 .pptx，客戶端用 PowerPoint 打開照樣能動——對要交付簡報給客戶的
  接案者/顧問，這是「能不能用」的分界線。4.5 萬星也說明痛點有多普遍
- **快速上手**：
  ```bash
  git clone https://github.com/hugohe3/ppt-master.git
  cd ppt-master
  pip install -r requirements.txt
  ```
  然後用 AI agent（Claude Code / VS Code 外掛等）開這個資料夾，直接叫它從你的素材生成簡報
- **費用與 API**：💰 程式碼免費（MIT），無付費版，但**實際使用要花模型錢**：
  官方建議用 ~1M context 的模型（Kimi K3 或 Claude）。🔑 選配 `OPENAI_API_KEY`、
  `GEMINI_API_KEY`（生圖）、`PEXELS_API_KEY` / `PIXABAY_API_KEY`（抓素材圖）
- 🔗 https://github.com/hugohe3/ppt-master

### 4. liketrek/TREK ⭐ 12,100
- **這是什麼**：自架的旅遊行程規劃器——地圖、預算分攤、打包清單、訂位管理、
  旅遊日誌、文件保管，加上 WebSocket 即時協作與 PWA。還內建 MCP server，
  可以讓 AI 助理直接讀寫行程
- **為什麼值得關注**：對標 TripIt Pro（$49/年）、Wanderlog Pro。
  這類 app 的難處在於你把護照影本、訂位代號、信用卡末四碼全交給了一家新創；
  自架的價值在這裡比省錢更明顯。內建 MCP 也讓「叫 agent 幫我排行程」
  不用再靠爬蟲外掛
- **快速上手**：
  ```bash
  ENCRYPTION_KEY=$(openssl rand -hex 32) docker run -d -p 3000:3000 \
    -e ENCRYPTION_KEY=$ENCRYPTION_KEY \
    -v ./data:/app/data -v ./uploads:/app/uploads mauriceboe/trek
  ```
- **費用與 API**：✅ 免費、無付費版（AGPL v3——改作後對外提供服務要開源，
  自用/內部用無限制）。🔑 全部選配：地點搜尋可用免費 OpenStreetMap（不用 Google Places）、
  天氣用免費 Open-Meteo 不需 key、Unsplash 選配。核心功能零外部 API 也能跑
- 🔗 https://github.com/liketrek/TREK

### 5. Priyanshu-1622/skiff ⭐ 153
- **這是什麼**：自架的 SSH 連線管理器——加密的憑證保險庫、瀏覽器裡的終端機、
  session 可持久化並事後重播（asciicast 格式錄影）、資料夾分組、團隊共用
- **為什麼值得關注**：對標 Termius（Pro $10/月、團隊版更貴）。
  但真正的賣點是「session 錄影重播」：接案或維運交付時，
  你在客戶機器上做了什麼有完整紀錄可回放，這在 Termius 是團隊版才有的功能。
  README 明說零雲端依賴、零 telemetry——把 SSH 金鑰交給第三方雲這件事本來就該讓人不安
- **快速上手**：
  ```bash
  cp .env.example .env
  mkdir -p data
  docker compose up -d --build     # http://localhost:8080
  ```
- **費用與 API**：✅ 完全免費（AGPL-3.0），無付費版、無需任何 API key、無 telemetry。
  ⚠️ Windows 開發環境要裝 Visual Studio Build Tools 編原生模組，用 Docker 可繞過
- 🔗 https://github.com/Priyanshu-1622/skiff

### 6. cathrynlavery/diagram-design ⭐ 8,339（今日 +1,616）
- **這是什麼**：29 種編輯級品質的圖表模板（架構圖、流程圖、時序圖、組織圖…），
  輸出是自足的 HTML + SVG。能從網站自動抽出品牌配色、能吃 draw.io / Mermaid 檔匯入、
  能匯出 PNG/SVG。以 agent skill 的形式安裝
- **為什麼值得關注**：今日 +1,616 星，是日榜前段少數「不是 agent harness」的東西。
  對做內容、寫技術文、做提案簡報的人，這解決的是「圖畫得醜」這個很實際的問題——
  而且產出是 SVG，可以直接改，不是生一張沒法編輯的圖片
- **快速上手**：
  ```bash
  # Claude Code
  /plugin marketplace add cathrynlavery/diagram-design
  /plugin install diagram-design@diagram-design
  ```
  ```bash
  # Codex
  npx skills add https://github.com/cathrynlavery/diagram-design --skill diagram-design
  ```
  裝完直接叫 agent：「幫我畫一張這個 app 的架構圖」
- **費用與 API**：✅ skill 本身免費（MIT）、不需外部 API。
  💰 但前提是你已經有 Claude Code / Pi / Codex 可用（那是要付費的）。
  匯出 PNG 需另裝 Playwright：`pip install playwright && playwright install chromium`
- 🔗 https://github.com/cathrynlavery/diagram-design

### 7. cloudflare/computer ⭐ 7,716（本週 +6,775）
- **這是什麼**：Cloudflare 官方的「給 agent 一台電腦」——在 Durable Object 裡跑一個
  虛擬檔案系統，配三種可插拔的執行後端：Container（FUSE 掛載 + Linux userland）、
  Isolate shell（Dynamic Worker 裡的 just-bash）、Isolate JavaScript
- **為什麼值得關注**：本週成長王，+6,775 星遠超第二名。大廠親自下場定義
  「agent 的執行沙盒」長什麼樣，這件事本身就是訊號——它預告的是接下來一年
  agent 基礎建設會往 edge 跑
- **快速上手**：README 沒有完整範例，只指向 `@cloudflare/computer` 這個 npm 套件的
  README 去看安裝步驟與 entrypoint 對照表
- **費用與 API**：💰 程式碼 MIT，但 Durable Objects 與 Dynamic Workers 需要
  Cloudflare 帳號；README 未說明免費額度是否夠用，需自行確認。
  ⚠️ **官方標註 PREVIEW ONLY**：「API 不穩定、設計可能變動，適合實驗與原型，
  目前不適合正式環境」——想跟風的請先讀完這句
- 🔗 https://github.com/cloudflare/computer

## 📱 Threads 貼文草稿

> 搭配圖：`reports/assets/2026-08-12/radar.png`（主文）

**主文**

前幾天那串平替有人問「還有沒有」，有。
這次五個，每一個都直接對到一筆你正在繳的月費：

① macro：Slack + Notion + Linear + HubSpot + Superhuman 全包成一個工作區，Rust 寫的，可自架。
不是週末專案——團隊 15 人自己內部用兩年才開源，有 SOC 2 和 ISO 27001。這個我自己會裝。

② voice-studio：ElevenLabs 平替。一個介面裡包七個開源語音模型 + Whisper 轉錄，
支援語音克隆。全離線、聲音不出你的電腦。ElevenLabs Creator 是 $22/月還會算字元數。

③ ppt-master：Gamma 平替，但關鍵差別是它吐**原生可編輯的 .pptx**——
真的圖形和動畫物件，客戶用 PowerPoint 打開照樣能改，不是鎖在網頁編輯器裡的圖片。

---（回覆串 2）---

④ TREK：TripIt Pro（$49/年）平替，自架的旅遊行程規劃。地圖、預算分攤、打包清單、
訂位管理，還內建 MCP 可以叫 AI 幫你排。地點搜尋用免費的 OpenStreetMap 就行，不用 Google key。

⑤ skiff：Termius（$10/月）平替，自架 SSH 連線管理。
真正的賣點是 session 錄影重播——接案在客戶機器上做了什麼有完整紀錄，
這在 Termius 要團隊版才有。零雲端、零 telemetry，SSH 金鑰不交給別人。

誠實說一下代價：
・macro 用 Nix 當開發環境，沒碰過的人要多花時間
・voice-studio 全部模型載完 23GB，還要 3～8GB VRAM
・ppt-master 本身免費，但要餵 1M context 的模型，那是要付錢的

不是「免費」，是「把月費換成一次性的設定成本」。自己算划不划算。

連結在留言 👇

#GitHub #開源 #SaaS平替 #自架 #開發者工具

---（回覆串 3・連結）---

macro https://github.com/macro-inc/macro
voice-studio https://github.com/msrbuilds/voice-studio
ppt-master https://github.com/hugohe3/ppt-master
TREK https://github.com/liketrek/TREK
skiff https://github.com/Priyanshu-1622/skiff

## 落選但值得觀察

- **rmyndharis/OpenWA**（⭐12,700）：自架 WhatsApp API gateway，題材本來完全符合
  「企業客服自動化」線。**但刻意不放進精選**——它走的是逆向工程的
  `whatsapp-web.js` / `baileys`，不是 Meta 官方 Cloud API，README 自己就警告
  「帳號被封的風險永遠非零」「絕對不要接你的主要商業號碼」。
  拿它接正式業務等於把客戶聯絡管道押在隨時可能被砍的號碼上，這種東西我不推薦
- **cactus-compute/needle**（⭐3,879，今日 +248）：14MB 的基礎模型，
  目標是手機與穿戴裝置。體積數字很有話題性，但要看實際能力再說
- **stablyai/orca**（⭐43,390，今日 +1,215）：管理平行 agent 艦隊的 ADE，
  桌面/手機/VPS 都有。成長很猛，但屬於重度開發者工具，受眾偏窄
- **semantica-agi/semantica**（⭐5,405，本週 +2,712）：上期就列在觀察名單，
  兩天內從 3,937 漲到 5,405，成長沒有停。等它有清楚的 use case 就可以寫
- **huangruiteng/loopx**（⭐4,300，本週 +2,687）：同上期觀察，持續高速成長中
- **odysseus-dev/odysseus**（⭐85,200）：自架 AI workspace，星數很高但屬於成熟大專案，
  適合放進「自架企業基礎建設」專題而不是潛力雷達
- **localsend/localsend**（⭐87,505）：AirDrop 的跨平台開源替代。常青平替經典，
  已太廣為人知，留給常青樹特輯
- **NVIDIA-NeMo/Switchyard**（⭐616，今日 +370）：星數基數小但單日成長比極高，
  README 資訊太少無法判斷，下期追蹤
