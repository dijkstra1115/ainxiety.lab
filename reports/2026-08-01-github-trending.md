# GitHub 潛力雷達 2026-08-01

> 資料來源：GitHub Trending（日榜/週榜）+ 近 30 天新秀搜尋（created:>2026-07-01, stars:>200，共 517 個結果），本期掃描約 30 個候選。

## 本期精選

### 1. xai-org/grok-build ⭐ 23,800（建立不到一個月）
- **這是什麼**：xAI 推出的終端機 AI coding agent，全螢幕 TUI 介面、支援滑鼠操作，能理解整個 codebase、改檔案、跑指令、查網路，也有 headless 模式可嵌進自動化流程。
- **為什麼值得關注**：上線不到一個月就衝到 2.3 萬星，是本月新秀榜第一名。終端機 coding agent 這條賽道（Claude Code、Codex CLI）競爭白熱化，xAI 親自下場本身就是話題。
- **快速上手**：
  ```bash
  curl -fsSL https://x.ai/cli/install.sh | bash
  grok --version
  ```
- **費用與 API**：🔑 首次啟動會開瀏覽器登入 x.ai 帳號；README 未明說免費額度，需自行到 docs.x.ai/build 確認。程式碼本身 Apache 2.0。
- 🔗 https://github.com/xai-org/grok-build

### 2. block/buzz ⭐ 20,233（本週 +10,558，週榜成長王）
- **這是什麼**：Block（Square 母公司）開源的「人類 + AI agent 共用工作空間」——聊天室、code review、git 操作全部進同一條可搜尋的事件紀錄，agent 有自己的金鑰和權限，是正式的團隊成員而不是外掛 bot。底層是 Nostr relay。
- **為什麼值得關注**：單週破萬星是本週全站最猛的成長曲線。「多 agent 協作要有共用空間」是今年很熱的架構問題，大廠開源的完整答案不多。
- **快速上手**：
  ```bash
  git clone https://github.com/block/buzz.git && cd buzz
  . ./bin/activate-hermit
  just setup && just build
  just dev   # 啟動 relay（ws://localhost:3000）+ 桌面 app
  ```
  也有 macOS / Linux / Windows 預編譯版可直接下載。
- **費用與 API**：✅ 自架完全免費、不需 API key（接 AI agent 時才需要各家模型的 key）。Apache 2.0。
- 🔗 https://github.com/block/buzz

### 3. diegosouzapw/OmniRoute ⭐ 36,902（本週 +7,701）
- **這是什麼**：自架 AI gateway：一個本地端點聚合 290+ 模型供應商（其中 90+ 有免費額度），額度用完自動切換下一家，還會做 token 壓縮。可直接接 Claude Code、Cursor、Cline 等 33+ 工具。
- **為什麼值得關注**：直接命中「AI coding 工具太燒錢」的普遍痛點，官方宣稱免費供應商池合計每月約 15 億 token。對想省訂閱費的開發者非常實用，Threads 上這種「白嫖攻略」型工具最容易擴散。
- **快速上手**：
  ```bash
  npm install -g omniroute
  omniroute
  # 開 http://localhost:20128 儀表板
  # 把你的 coding 工具 API base 指到 http://localhost:20128/v1，model 填 auto
  ```
- **費用與 API**：✅ 工具本身免費（MIT、零遙測）、裝完即用，內建免費供應商不用註冊；想擴充可自行綁其他免費額度或付費 API。免費模型的品質與穩定性需自行評估。
- 🔗 https://github.com/diegosouzapw/OmniRoute

### 4. andrewyng/openworker ⭐ 11,600（建立不到一個月）
- **這是什麼**：吳恩達（Andrew Ng）開源的桌面 AI 同事，主打「交付完成的工作，不是聊天」——接了 Slack、GitHub、Jira、Notion、Outlook 等 25+ 工具，重要動作（寄信、跑指令）前會先要求人類批准。
- **為什麼值得關注**：一個月 1.1 萬星，掛著 Andrew Ng 的名字自帶流量；「open-source AI coworker」正面對打各家付費 agent 產品，是這波 agent 桌面化趨勢的指標專案。
- **快速上手**：到 openworker.com 下載 macOS（Apple Silicon）或 Windows 版，開啟後填一組模型 API key（或指向本地 Ollama），直接用自然語言描述你要的成果。
- **費用與 API**：🔑 軟體本身免費（MIT），但要自備模型 key（OpenAI / Anthropic / Gemini / DeepSeek…）；想完全免費可接本地 Ollama 跑開源模型。
- 🔗 https://github.com/andrewyng/openworker

### 5. usekaneo/kaneo ⭐ 5,579（今日 +778，日榜黑馬）
- **這是什麼**：極簡開源專案管理平台——看板、issue 追蹤、團隊協作，主張「你需要的都有，不需要的都沒有」，走 Jira 反面路線。
- **為什麼值得關注**：今天單日 +778 星、總星數才 5 千多，是典型的「小專案起飛中」曲線。輕量自架 PM 工具長期有穩定需求（Trello 漲價、Jira 太重都是催化劑）。
- **快速上手**：
  ```bash
  # Docker Compose：設好 POSTGRES_PASSWORD 和 AUTH_SECRET 後
  docker compose up -d
  # 開 http://localhost:5173
  ```
- **費用與 API**：💰 自架免費、無需 API key（MIT）；官方另有付費雲端版 cloud.kaneo.app，不想自己架可以付費。
- 🔗 https://github.com/usekaneo/kaneo

### 6. virgiliojr94/book-to-skill ⭐ 14,744（本週 +4,603）
- **這是什麼**：把任何技術書（PDF/EPUB）轉成 Claude Code / Copilot CLI 的「skill」——抽出書中的框架、模式、關鍵概念，整理成按需載入的章節檔，官方宣稱比直接把整本書塞進 context 省 24～51 倍 token。
- **為什麼值得關注**：獨立開發者作品單週 +4,600 星。「讓 AI 讀完一本書再幫你工作」這個概念直覺又好講，非常適合社群傳播；也反映 Claude Code skill 生態正在起飛。
- **快速上手**：
  ```bash
  git clone https://github.com/virgiliojr94/book-to-skill.git ~/.claude/skills/book-to-skill
  # 在 Claude Code 裡：
  /book-to-skill ~/path/to/your-book.pdf
  ```
- **費用與 API**：✅ 工具免費（MIT）、不需額外 API key，轉換在本地跑；但轉一本書會消耗你既有的 Claude 用量（實測 371 頁約 $1 美元等值 token）。
- 🔗 https://github.com/virgiliojr94/book-to-skill

## 📱 Threads 貼文草稿

> 配圖：主文附 `reports/assets/2026-08-01/radar.png`（六工具排行卡）；
> 成長王 buzz 可隔日用 `spotlight-buzz.png` 單獨加熱一篇。

這週 GitHub 上竄最快的 6 個工具，第 3 個直接幫你省訂閱費 👇

🥇 block/buzz：Block 開源的「人+AI 共用工作間」，agent 是正式隊友不是 bot。單週 +1 萬星，免費自架
🤖 grok-build：xAI 的終端機 coding agent，上線一個月 2.3 萬星（要 x.ai 帳號）
💸 OmniRoute：一個本地端點聚合 290+ 家模型、額度用完自動換下一家，免費模型池每月約 15 億 token。MIT 完全免費

---（回覆串 2）---

👔 openworker：吳恩達開源的桌面 AI 同事，接好 Slack/GitHub/Jira，交付成果不是聊天（要自備模型 key，或接 Ollama 全免費）
📋 kaneo：極簡開源版 Jira，docker compose up 就能用，今天單日 +778 星
📚 book-to-skill：把任何技術書 PDF 變成 Claude Code skill，讓 AI「讀完書」再幫你寫 code，省 24 倍 token

全部連結放留言。你最想試哪個？

#GitHub #開源 #開發者工具

---（回覆串 3：連結）---

buzz: github.com/block/buzz
grok-build: github.com/xai-org/grok-build
OmniRoute: github.com/diegosouzapw/OmniRoute
openworker: github.com/andrewyng/openworker
kaneo: github.com/usekaneo/kaneo
book-to-skill: github.com/virgiliojr94/book-to-skill

## 落選但值得觀察

- **citrolabs/ego-lite**（7.3k，週 +4.7k）：主打「給 AI agent 用的最快瀏覽器」，賽道熱但同類太多，等它做出差異化再介紹
- **ayghri/i-have-adhd**（15.1k，週 +5.1k）：防止 coding agent 把重點埋在長篇回覆裡的 skill，有趣但單一功能，適合湊「skill 專題」再寫
- **CoreBunch/Instatic**（7.1k，週 +2.9k）：開源版 Webflow/Framer，受眾偏設計側，留給下一期
- **moeru-ai/airi**（46.4k）與 **permissionlesstech/bitchat**（33.9k）：仍在漲但已廣為人知，不符合「挖掘」定位
- **MoonshotAI/Kimi-K3**（7.8k，新）：模型發布型 repo，適合寫模型評測文而非工具介紹
