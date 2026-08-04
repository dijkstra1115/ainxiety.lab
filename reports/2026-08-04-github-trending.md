# GitHub 潛力雷達 2026-08-04

> 資料來源：GitHub Trending（日/週榜）+ 近 30 天新秀搜尋（created:>2026-07-05, stars:>300），
> 共掃描約 40 個候選；與 seen.json 比對後排除 14 天內已介紹的 12 個。

## 本期精選

### 1. lyogavin/airllm ⭐ 27,764（今日 +1,085）
- **這是什麼**：讓 4GB GPU 跑得動 70B 大模型的推理庫——原理是一次只把一層放上 GPU，
  不靠量化。官方數據：70B 約 4GB VRAM、DeepSeek-V3 671B 約 12GB
- **為什麼值得關注**：日榜 +1,085 星。「本地跑大模型」加速民主化的代表作，
  對不想付雲端 API 費的開發者是直接的省錢選項（代價是推理速度，逐層載入不快）
- **快速上手**：
  ```bash
  pip install airllm
  ```
  ```python
  from airllm import AutoModel
  model = AutoModel.from_pretrained("Qwen/Qwen3-32B")
  ```
- **費用與 API**：✅ 免費（Apache 2.0）；下載 Meta Llama 這類 gated 模型才需要免費的
  HuggingFace token
- 🔗 https://github.com/lyogavin/airllm

### 2. drumih/turbo-fieldfare ⭐ 4,700（新，30 天內）
- **這是什麼**：讓 8GB RAM 的 Apple Silicon MacBook 跑 Gemma 4 26B——14.3GB 的模型
  不整個載入，核心 ~2GB 常駐記憶體，專家權重從 SSD 串流
- **為什麼值得關注**：與 airllm 同一個趨勢的 Mac 端答案，一人專案一個月 4.7k 星。
  適合想在筆電上離線跑正經模型的人
- **快速上手**：
  ```bash
  git clone https://github.com/drumih/turbo-fieldfare.git
  cd turbo-fieldfare && swift build -c release
  .build/release/TurboFieldfareMac   # 首次啟動下載 15GB 權重
  ```
- **費用與 API**：✅ 完全免費（Apache 2.0）；需 macOS 26 + Apple Silicon ≥8GB RAM、15GB 硬碟
- 🔗 https://github.com/drumih/turbo-fieldfare

### 3. firecrawl/pdf-inspector ⭐ 9,018（今日 +1,699）
- **這是什麼**：Firecrawl 開源的 Rust PDF 庫：自動分類 PDF 是文字檔還是掃描檔、
  帶座標抽取文字、輸出乾淨 Markdown——文字型 PDF 不經 OCR，速度是賣點
- **為什麼值得關注**：日榜成長王之一。做 RAG／文件處理的人天天在跟爛 PDF 搏鬥，
  這是基礎建設級的工具；Python/Node/Rust 三種綁定都有
- **快速上手**：
  ```bash
  npm install @firecrawl/pdf-inspector
  ```
  ```javascript
  import { processPdf } from '@firecrawl/pdf-inspector';
  const r = processPdf(readFileSync('doc.pdf'));  // r.pdfType, r.markdown
  ```
- **費用與 API**：✅ 完全免費本地執行（MIT），不需 Firecrawl 帳號
- 🔗 https://github.com/firecrawl/pdf-inspector

### 4. TencentCloud/TencentDB-Agent-Memory ⭐ 12,572（今日 +1,090）
- **這是什麼**：騰訊開源的「團隊級 agent 記憶中樞」——把對話、文件、程式碼變成
  四種可治理、可共用的記憶資產（Chat Memory / Skills / Wiki / CodeGraph），
  讓團隊的 agent 不用每次從零開始
- **為什麼值得關注**：「agent 記憶」是今年下半年的熱門基建題，大廠開源完整方案不多；
  MIT 授權且不綁騰訊雲
- **快速上手**：
  ```bash
  git clone https://github.com/Tencent/TencentDB-Agent-Memory.git
  cd TencentDB-Agent-Memory/deploy/global-images
  cp .env.example .env && $EDITOR .env   # 填兩組 LLM 參數
  ./start-all.sh                          # http://localhost:8125
  ```
- **費用與 API**：🔑 工具免費（MIT），需自備 LLM API key（兩組：記憶用＋代理用）
- 🔗 https://github.com/TencentCloud/TencentDB-Agent-Memory

### 5. openai/codex-security ⭐ 8,500（新，30 天內）
- **這是什麼**：OpenAI 開源的防禦性安全工具鏈——掃描 codebase 找漏洞、驗證是否真實、
  協助修復，CLI 一行掃描
- **為什麼值得關注**：大廠開源＋「AI 找漏洞」正處在風口（上週 OpenAI 模型攻擊 HF 事件
  之後，防禦側工具的關注度明顯上升）
- **快速上手**：
  ```bash
  npm install @openai/codex-security
  npx @openai/codex-security login
  npx @openai/codex-security scan .
  ```
- **費用與 API**：🔑 需 ChatGPT 帳號登入或 API key（也支援 OpenRouter/Fireworks 的 key）
- 🔗 https://github.com/openai/codex-security

### 6. oso95/scroll-world ⭐ 7,300（新，30 天內）
- **這是什麼**：把品牌素材變成 Apple 產品頁風格的「3D 捲動穿越」落地頁——
  訪客捲動時鏡頭無剪接飛越多個 AI 生成場景。以 Claude Code plugin 形式安裝
- **為什麼值得關注**：效果確實驚豔、對做品牌官網的人有吸引力；**但要特別注意費用**——
  README 深處才寫：預設影片後端按片計費，6 場景 1080p 一條約 $27 美元，
  另外場景渲染還要 Higgsfield credits。「開源」不等於「免費產出」
- **快速上手**：
  ```
  /plugin marketplace add oso95/scroll-world
  /plugin install scroll-world@scroll-world
  ```
- **費用與 API**：💰 程式碼 MIT 免費，但實際產一頁約 $27 USD 起的生成費＋多個服務 credits
- 🔗 https://github.com/oso95/scroll-world

## 📱 Threads 貼文草稿

> 配圖：主文附 `reports/assets/2026-08-04/radar.png`

這週翻雷達看到一個明顯的趨勢：大模型正在被塞進越來越小的硬體 👇

🖥 airllm：單張 4GB GPU 跑 70B 模型，做法是一次只把一層放上 GPU。pip install airllm 就能試，今天一天 +1,085 星
💻 turbo-fieldfare：8GB RAM 的 MacBook 跑 Gemma 4 26B——14GB 模型不全載入，2GB 核心常駐、其他從 SSD 串流
📄 pdf-inspector：Firecrawl 開源的 Rust PDF 庫，自動判斷文字檔還是掃描檔、直接轉乾淨 Markdown。做 RAG 的人會懂這有多重要

---（回覆串 2）---

🧠 TencentDB-Agent-Memory：騰訊開源的團隊級 agent 記憶中樞，對話、文件、code 變成可共用的記憶資產（要自備 LLM key）
🛡 codex-security：OpenAI 開源的漏洞掃描 CLI，npx 三行就能掃自己的專案（要 ChatGPT 帳號或 API key）
🌍 scroll-world：把品牌變成 Apple 風格的 3D 捲動落地頁，效果很驚豔——但我翻 README 才發現產一頁約 $27 美元生成費。開源不等於免費產出，裝之前先知道

前三個完全免費、離線可用；後三個要 key 或會花錢。

這期你會先裝哪個？

#GitHub #開源

---（回覆串 3：連結）---

airllm: github.com/lyogavin/airllm
turbo-fieldfare: github.com/drumih/turbo-fieldfare
pdf-inspector: github.com/firecrawl/pdf-inspector
agent-memory: github.com/TencentCloud/TencentDB-Agent-Memory
codex-security: github.com/openai/codex-security
scroll-world: github.com/oso95/scroll-world

## 落選但值得觀察

- **alibaba/open-code-review**（18.6k，週 +3,881）：LLM code review，開發者向專題再寫
- **esengine/DeepSeek-Reasonix**（30.4k）：又一個終端 coding agent，同類介紹太密，觀察差異化
- **yc-software/qm**（10.5k 新）與 **unicity-aos/aos-ce**（8.6k 新）：agent 基建題材，
  等「agent 記憶/OS」專題一起寫
- **img2threejs**（9.5k 新）：圖片轉 Three.js 模型，趣味向，適合創作者專題
- **Panniantong/Agent-Reach**（66k）：量級已廣為人知，不符挖掘定位
- **Alishahryar1/free-claude-code**（44k）：「免費用 Claude Code」的授權合規性存疑，不推薦
- **zhaoxuya520/reverse-skill**（16.7k，日 +2,446）：滲透測試工具、來源與治理不明，
  不適合一般受眾推薦
