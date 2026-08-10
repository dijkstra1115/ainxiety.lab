# GitHub 潛力雷達 2026-08-10

> 資料來源：GitHub Trending（日榜 16 個 / 週榜 17 個）+ 近 30 天新秀搜尋
> （created:>2026-07-11, stars:>200）+ 三輪 SaaS 平替定向搜尋
> （topic:self-hosted、"open source alternative"、crm/cms/low-code/booking），
> 共掃描約 60 個候選；與 seen.json 比對後排除 14 天內已介紹的 6 個
> （pdf-inspector、TencentDB-Agent-Memory、airllm、book-to-skill、kaneo、codex-security）。
>
> 本期主軸刻意偏離 trending 首頁——日榜幾乎被 AI agent harness 洗版，
> 但定向搜尋撈出一整批「取代付費 SaaS」的新專案，那才是本帳號的主場。

## 本期精選

### 1. CoreBunch/Instatic ⭐ 7,800（30 天內新專案）
- **這是什麼**：自架的視覺化 CMS，目標明講是取代 Webflow / Framer / WordPress。
  拖拉編輯器 + 內容管理 + 發布，跑在單一個 Bun server 上，輸出的是乾淨的語意 HTML
  靜態頁——不是又一包 React bundle。內建表單、媒體庫、角色權限、審計紀錄、外掛系統，
  還有一個能幫你組頁面的 AI agent
- **為什麼值得關注**：這是本期唯一一個「中小企業官網」可以直接落地的選項。
  Webflow 一個站台 $23–39/月、Framer $20/月起，客戶數一多就是每月固定支出；
  Instatic 自架後這筆歸零，而且客戶要交接時你交的是 HTML，不是綁在別人平台上的專案。
  MIT 授權、沒有商用限制、沒有 open-core 陷阱，這點在 CMS 類專案裡不常見
- **快速上手**：
  ```bash
  git clone https://github.com/corebunch/instatic.git
  cd instatic
  bun install
  bun run dev          # http://localhost:5173
  ```
- **費用與 API**：✅ 完全免費（MIT），無付費雲端版。AI agent 功能是選配，
  要用才需自備 Claude / OpenAI / OpenRouter 金鑰，或接本地 Ollama 完全離線
- 🔗 https://github.com/CoreBunch/Instatic

### 2. coollabsio/shoutrrr ⭐ 282（新，成長中）
- **這是什麼**：自架的社群排程工具，一次寫好、多平台同步發或排定期發。
  支援 X、Bluesky、LinkedIn、Facebook 粉專、Instagram、**Threads**、Discord
- **為什麼值得關注**：星星數是本期最少的，但對位最準——Buffer 團隊方案 $6/頻道/月起、
  Hootsuite $99/月起、Typefully Pro $12.5/月。經營多平台的個人創作者一年省下來
  是四位數台幣起跳。而且它是 Coolify 團隊（coollabs）出品，那群人做自架工具有紀錄可循，
  不是週末專案。原生支援 Threads 這點，在開源排程工具裡目前還相當少見
- **快速上手**：
  ```bash
  docker pull ghcr.io/coollabsio/shoutrrr:latest
  # 產生 APP_KEY 填進 .env.prod（APP_URL=http://localhost:8080）
  docker run --rm --entrypoint php ghcr.io/coollabsio/shoutrrr:latest \
    /var/www/html/artisan key:generate --show
  docker volume create shoutrrr-storage && docker volume create shoutrrr-sqlite
  docker run -d --name shoutrrr --env-file .env.prod -p 8080:8080 \
    -v shoutrrr-storage:/var/www/html/storage \
    -v shoutrrr-sqlite:/var/www/html/database/sqlite \
    ghcr.io/coollabsio/shoutrrr:latest
  ```
- **費用與 API**：✅ 軟體免費（Apache 2.0）、無付費版，但 🔑 **設定門檻不低**——
  X、LinkedIn、Facebook/Instagram、Threads 都要自己去申請開發者 app 並設定 OAuth；
  Bluesky 可用 app password、Discord 只要 webhook。想省訂閱費，代價是一個下午的設定時間
- 🔗 https://github.com/coollabsio/shoutrrr

### 3. trycompai/crm ⭐ 8,100（30 天內新專案）
- **這是什麼**：為 AI agent 設計的開源 CRM。它的差異不在「CRM 加了聊天框」，
  而是 agent 有自己的工作佇列、按自己的排程跑，主動去查資料、依查到的證據回填欄位。
  官方特別強調工具回報的是「觀察到什麼」而不是信心分數——不確定就留白，不猜
- **為什麼值得關注**：CRM 是中小企業數位轉型最常見的第一站，但 HubSpot 一超過免費額度
  就跳到 $20/席/月起、Salesforce 更貴。這個專案的立場很清楚：資料進 CRM 的過程本來
  就該自動化，人只該做決策。MIT 授權、Postgres 自架，資料留在自己機器上這點對
  客戶名單類資料特別重要
- **快速上手**：
  ```bash
  git clone https://github.com/trycompai/crm.git && cd crm
  cp .env.example .env     # 填入登入用的 OAuth 設定
  bun install
  docker compose up -d     # Postgres :5432
  bun run db:deploy && bun run db:seed
  bun run dev              # app :3000 / api :3001
  ```
- **費用與 API**：💰 軟體免費（MIT），未見付費雲端版。🔑 登入必須擇一設定
  Google OAuth 或 Microsoft Entra；進階功能選配 Perplexity（網路查資料）、
  RapidAPI（LinkedIn 資料）、Context（公司品牌資料）——不設定也能跑，只是 agent 變笨
- 🔗 https://github.com/trycompai/crm

### 4. firecrawl/anydoc ⭐ 13,300（30 天內新專案）
- **這是什麼**：把 Word、PowerPoint、Excel、OpenDocument、RTF、EPUB、CSV、PDF
  全部轉成乾淨的 GitHub-Flavored Markdown。純 Rust 寫的，提供 Node、Python、
  瀏覽器 WASM 三種綁定
- **為什麼值得關注**：一個月衝到 13.3k 星，是本期新專案裡最高的。做 RAG、
  做知識庫、做文件搬家的人手上永遠有一堆格式混雜的檔案，過去要拼 pandoc + 各種
  parser；這個是一包搞定，而且**不需要網路、不需要模型**，純本地解析。
  上週介紹過的 pdf-inspector 就是它內建的 PDF 引擎，等於同一組人把整條文件管線補齊了
- **快速上手**：
  ```bash
  npx @firecrawl/anydoc report.docx               # 直接吐 Markdown
  npx @firecrawl/anydoc slides.pptx -o slides.md
  ```
  ```bash
  pip install firecrawl-anydoc
  ```
  ```python
  import anydoc
  markdown = anydoc.to_markdown("report.docx")
  ```
- **費用與 API**：✅ 完全免費、離線可用（MIT），不需 API key 也不需 Firecrawl 帳號。
  Firecrawl 另有付費託管版 Firecrawl Parse，但跟這個函式庫無關
- 🔗 https://github.com/firecrawl/anydoc

### 5. nyblnet/bento ⭐ 3,900
- **這是什麼**：整套簡報軟體塞進**一個 HTML 檔**——編輯器、播放器、簡報者模式全在裡面。
  有轉場變形動畫、內建圖表、講者備忘檢視、PDF 匯出，還支援端對端加密的即時協作。
  不用安裝、不用註冊帳號
- **為什麼值得關注**：這個形式本身就是話題。你交出去的簡報檔就是一個可以雙擊打開、
  可以繼續編輯的 HTML，收件人不需要有 PowerPoint、不需要有 Google 帳號、
  不需要連網。對「不想因為要看一份簡報而註冊 Google Workspace」的場景是乾淨解法
- **快速上手**：
  ```bash
  cd slides
  npm install
  npm run dev            # http://localhost:5173
  npm run build:single   # 產出 dist-single/Bento_Slides.bento.html
  ```
- **費用與 API**：✅ 完全免費、完全離線（MIT），無付費版、無需任何 API key
- 🔗 https://github.com/nyblnet/bento

### 6. pireel/pireel ⭐ 916
- **這是什麼**：瀏覽器裡跑的開源 AI 影片編輯器，鎖定 talking-head（口播）影片。
  分鏡、字幕、主題樣式、時間軸、預覽、匯出全部在瀏覽器端跑完，不用開帳號。
  官方定位直接寫「CapCut、ChatCut 的開源替代」
- **為什麼值得關注**：口播短影音是目前產量最大的內容形式，而 CapCut 的條款與資料
  歸屬一直讓商用者不安。這個專案的另一個特色是可以用 MCP 讓 AI agent 直接驅動剪輯，
  等於「叫 agent 幫你剪片」這件事有了開源實作
- **快速上手**：
  ```bash
  pnpm install
  pnpm dev
  ```
  ```bash
  npx skills add pireel/pireel-agent   # 讓 AI agent 透過 MCP 驅動
  ```
- **費用與 API**：✅ 本地剪輯免費（AGPL-3.0-only，商用改作要注意這個授權比 MIT 嚴格）。
  🔑 AI 生成類功能（旁白、轉錄、生圖生片）要自己接 provider。
  官方另有 pireel.com 託管版，repo 是開源本體
- 🔗 https://github.com/pireel/pireel

### 7. PrimeIntellect-ai/prime-agent ⭐ 12,816（今日 +2,655）
- **這是什麼**：Prime Intellect 出的自主 coding／研究 agent，架構是 RLM
  （Recursive Language Model）。特色是持續存活的 Python 執行環境、可程式化的子代理、
  可自我改寫的 harness 狀態，以及背景 session——設計目標是跑得動「幾小時起跳」的長任務
- **為什麼值得關注**：本期日榜成長王，一天 +2,655 星遠超第二名。它代表的是
  「agent 不只是聊天迴圈，而是一個會改自己工具的長期行程」這條路線。
  故事性夠強，但務實地說——這是給開發者的重型工具，不是小商家能直接用的東西
- **快速上手**：
  ```bash
  curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh
  cd /path/to/project && prime-agent
  # 首次啟動輸入 /login 設定 model provider
  ```
- **費用與 API**：💰 程式碼免費（MIT），但**實際使用要花錢**——必須綁訂閱或
  自備 model API key，沒有免費跑法。列在這裡是因為成長數字太顯眼，不是因為它省錢
- 🔗 https://github.com/PrimeIntellect-ai/prime-agent

## 📱 Threads 貼文草稿

> 搭配圖：`reports/assets/2026-08-10/radar.png`（主文）

這週我沒去追 GitHub 日榜——因為首頁又被 AI agent 洗版了。
反而在 open source alternative 的搜尋結果裡挖到一整排「直接砍掉月費」的東西：

① Instatic：Webflow / Framer / WordPress 的自架替代，拖拉做站、輸出乾淨 HTML。
Webflow 一個站 $23/月起，自架就是 0。MIT 授權沒陷阱。

② shoutrrr：Buffer / Hootsuite 的自架替代，一次寫好同步發到 X、Threads、
IG、LinkedIn。Coolify 那群人做的。免費，但各平台 OAuth 要自己申請。

③ Comp CRM：給 AI agent 用的開源 CRM——agent 有自己的工作佇列，
主動查資料回填欄位，查不到就留白不亂猜。HubSpot 超過免費額度是 $20/席/月。

---（回覆串 2）---

④ anydoc：Word / PPT / Excel / EPUB / PDF 全部轉乾淨 Markdown，
純 Rust、純本地、不用 API key。一個月 13.3k 星，本期新專案最猛。
做 RAG 或知識庫的直接 `npx @firecrawl/anydoc 檔名` 就有。

⑤ Bento：整套簡報軟體塞進一個 HTML 檔。編輯器、播放、講者模式都在裡面，
寄給對方雙擊就能開，不用 PowerPoint、不用 Google 帳號、不用連網。

⑥ pireel：CapCut 的開源替代，口播影片在瀏覽器裡剪完，不用註冊。
還能用 MCP 讓 AI agent 幫你剪。授權是 AGPL，商用改作要看清楚。

這六個我自己會先裝 anydoc 跟 Bento——門檻最低、當天就有用。
shoutrrr 要花一個下午設 OAuth，但省的是每個月的錢。

連結都在留言 👇

#GitHub #開源 #開發者工具 #SaaS平替 #自架

---（回覆串 3・連結）---

Instatic https://github.com/CoreBunch/Instatic
shoutrrr https://github.com/coollabsio/shoutrrr
Comp CRM https://github.com/trycompai/crm
anydoc https://github.com/firecrawl/anydoc
Bento https://github.com/nyblnet/bento
pireel https://github.com/pireel/pireel

## 落選但值得觀察

- **semantica-agi/semantica**（⭐3,937，今日 +967）：graph-native 的 AI context 基礎建設，
  成長很猛但仍偏研究性質，讀者看完不知道能拿來幹嘛——等它有具體 use case 再說
- **huangruiteng/loopx**（⭐3,910，本週 +3,518）：長時間運行 agent 團隊的狀態核心，
  一週衝 3.5k 星，是本期成長比最高的新專案。題目太底層，先觀察
- **vitali87/code-graph-rag**（⭐3,447，今日 +682）：用知識圖譜做 monorepo 的 RAG，
  對大型專案的 code search 很有用，適合之後做「開發者工具」專題時單獨介紹
- **drawdb-io/drawdb**（⭐38,721）：dbdiagram.io 的免費替代，資料庫關聯圖線上編輯器。
  完全符合平替定位，但已經是成熟老專案、成長平穩，不算「潛力」
- **goauthentik/authentik**（⭐24,489）：Okta / Auth0 的自架替代，SSO 與身分管理。
  企業轉型場景很實用，留給「自架企業基礎建設」專題
- **oomol-lab/open-connector**（⭐4,500）：連接 1000+ SaaS 到 AI agent 的開源 auth gateway，
  等於自架版的 Composio。概念好，但 README 資訊不足以判斷成熟度
- **Kritt-ai/open-kritt**（⭐1,700）：自架的 AI 資安漏洞研究工具，多 agent 找並驗證程式碼問題。
  題材好但受眾窄
