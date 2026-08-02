# 實測報告：video-use（browser-use/video-use）2026-08-02

> 環境：Linux 沙盒、uv、無 ElevenLabs key。時間盒 30 分鐘。
> 結論先講：它不是「剪片 App」，是讓 Claude Code 變成剪接師的 Skill——理解這點才知道它適合誰。

## 實測筆記

### 它到底是什麼（README 不會直接告訴你的）

video-use 是一個 **Claude Code Skill**：沒有 GUI、沒有時間軸介面。流程是——你把素材丟進資料夾，
對 Claude 說「把這些剪成一支發布影片」，它轉錄音訊 → 讀逐字稿決定剪點 → 用 ffmpeg/PIL 執行
剪輯、調色、上字幕、疊動畫。設計文件品質異常高（12 條「硬規則」全是真剪接坑：字幕必須最後掛、
剪點不能落在字中間、每個剪切邊界要補 30ms 音訊淡入淡出防爆音……看得出真的剪過片）。

### 安裝（真實計時）

```bash
git clone https://github.com/browser-use/video-use   # 0.8 秒，倉庫僅 1.6 MB
cd video-use && uv sync                               # 7.5 秒，.venv 481 MB
# 另需 ffmpeg（見下方踩雷）
```

- 相依極輕（requests/librosa/matplotlib/pillow/numpy），與 OmniRoute 的 3.3 GB 是兩個世界
- ⚠️ **踩雷實錄**：它假設你有完整版 ffmpeg（README 只寫 `brew install ffmpeg`）。
  精簡版 ffmpeg（如 Playwright 附帶的）缺 lavfi/libx264 會直接失敗。
  Linux 免 root 解法：`pip install imageio-ffmpeg` 內附完整靜態編譯版，實測可用

### 功能實測

- ✅ **調色 helper 可獨立跑**：`grade.py --preset warm_cinematic` 對 5 秒測試片調色僅 1.1 秒，
  內建 subtle / neutral_punch / warm_cinematic 等 preset，也吃自訂 filter chain
- 🔑 **轉錄是整條流程的入口，被 ElevenLabs key 擋住**：`transcribe.py` 無 key 時明確報錯。
  它用 ElevenLabs Scribe 做「字級時間戳」轉錄（剪點精度的來源）。ElevenLabs 有免費層，
  但額度撐不撐得起常態剪片需自行確認
- ❗ 未測（被 key 擋）：核心剪輯流程、字幕燒錄、動畫疊層的實際成品品質

## 結論

- 👍 設計文件是我看過的 skill 裡最專業的——12 條硬規則全是實戰血淚，不是行銷文案
- 👍 安裝極輕（8 秒裝完），helper 可單獨當 ffmpeg 快捷工具用
- 👎 「免費剪片」有兩個前提：你要有 Claude Code（訂閱）+ ElevenLabs key（轉錄）；
  README 對後者只有一行帶過
- 💸 平替帳：取代的是 CapCut Pro / Descript（$10–24 USD/月）的「自動剪輯」部分；
  真實成本 = Claude 用量 + ElevenLabs 轉錄額度——輕度使用可能近零，重度剪片要算
- ⚠️ 適合：talking head、教學、訪談這類「以說話內容驅動剪輯」的影片；
  不適合：重視覺特效的 MV 式剪輯、完全不想碰終端機的人
- 🎯 一句話：**用 Claude Code 的內容創作者值得裝**（我們自己階段三的短影片就會用它——
  屆時補上完整實測）；沒有 Claude 訂閱的人，這不是你的免費午餐

## 📱 Threads 貼文草稿

> 配圖：`reports/assets/2026-08-02/verdict-video-use.png`

那個 18k 星的「AI 剪片」repo video-use，我裝起來測了，講三個沒人告訴你的事 👇

1️⃣ 它不是剪片 App——是讓 Claude Code 變成剪接師的 skill。你用「說的」剪片：「把這些素材剪成發布影片」
2️⃣ 安裝 8 秒裝完（跟動輒幾 GB 的剪輯軟體完全兩回事），但「免費」有前提：要 Claude Code + ElevenLabs 的轉錄 key
3️⃣ 它的設計文件是我見過最懂剪接的：剪點不落在字中間、每個剪切邊界補 30ms 淡入淡出防爆音——寫這個的人真的剪過片

結論:有在用 Claude Code 的創作者值得裝，沒有的先觀望

你會讓 AI 動你的影片嗎？

#AI工具

---（回覆串 2）---

補充實測細節：調色功能可以脫離 AI 單獨用，5 秒影片調色 1.1 秒。
踩雷提醒：Linux 上精簡版 ffmpeg 會炸，pip install imageio-ffmpeg 就解了。
核心剪輯品質這次被 API key 擋住沒測到，之後拿真素材補完整實測。

repo: github.com/browser-use/video-use

## 附註

- 測試素材為 ffmpeg 產生的 5 秒測試訊號片，非真實影片；剪輯成品品質未評
- 已從 watchlist 移入 seen.json（deepdive 條目）
