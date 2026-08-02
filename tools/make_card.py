#!/usr/bin/env python3
"""Generate Threads-ready social cards (1080x1350 PNG) from report data.

Renders an HTML template with the brand's dark theme and screenshots it with
headless Chromium — no paid image API, no external network needed.

Card types and their JSON payloads:

  radar     {"date": "...", "items": [{"rank":1,"name":"owner/repo",
             "delta":"+10,558 ⭐ 本週","desc":"一句話用途"}, ...]}   (max 6)
  spotlight {"date": "...", "label":"本週最猛","name":"owner/repo",
             "desc":"...","hero":"+10,558","hero_label":"本週新增星星",
             "badges":[{"text":"完全免費","kind":"good"},
                       {"text":"Rust","kind":"plain"}]}
  verdict   {"date": "...", "name":"OmniRoute","points":[
             {"icon":"👍","text":"..."},{"icon":"👎","text":"..."},
             {"icon":"💰","text":"..."}],
             "verdict":"值得裝","verdict_kind":"good"}   # good|warn|bad
  quote     {"date": "...", "label":"今日 AI 短評","quote":"...",
             "context":"一句背景說明"}
            # quote 支援 \n 手動斷行——中文請在語意邊界自行斷行，版面最好看
  digest    {"date": "...", "title":"本週 AI 圈回顧","items":["...","...","..."],
             "teaser":"下週實測預告：X"}

Usage:
  python3 tools/make_card.py --type radar --data payload.json --out card.png
  python3 tools/make_card.py --type quote --json '{"quote":"..."}' --out card.png

Fonts: uses Noto Sans TC if the fontsource package is available
(`npm install @fontsource/noto-sans-tc`, pass --fonts-dir or set
NOTO_TC_DIR to its node_modules path); otherwise falls back to system
CJK fonts (PingFang / Microsoft JhengHei / WenQuanYi).

Chromium: auto-detected from PLAYWRIGHT_BROWSERS_PATH, /opt/pw-browsers,
or PATH; override with --chromium.
"""

import argparse
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile

try:
    from PIL import Image  # pip install pillow — needed to crop to exact size
except ImportError:
    Image = None

# Validated dark-surface palette (see docs/content-strategy.md design notes)
CSS_VARS = """
  --surface: #1a1a19;
  --plane: #0d0d0d;
  --ink: #ffffff;
  --ink-2: #c3c2b7;
  --muted: #898781;
  --accent: #3987e5;
  --good: #0ca30c;
  --warn: #fab219;
  --bad: #ec835a;
  --hairline: rgba(255,255,255,0.10);
"""

BASE_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
:root { %(vars)s }
body {
  width:540px; height:675px; background:var(--plane);
  font-family:'Noto Sans TC','PingFang TC','Microsoft JhengHei',
              'WenQuanYi Zen Hei',sans-serif;
  color:var(--ink); -webkit-font-smoothing:antialiased;
}
.card {
  width:100%%; height:100%%; background:var(--surface);
  display:flex; flex-direction:column; padding:34px 36px 26px;
}
.hdr { display:flex; justify-content:space-between; align-items:baseline; }
.brand { font-weight:900; font-size:15px; letter-spacing:1px; }
.brand .dot { color:var(--accent); }
.date { font-size:12px; color:var(--muted); font-variant-numeric:tabular-nums; }
.ftr {
  margin-top:auto; padding-top:14px; border-top:1px solid var(--hairline);
  display:flex; justify-content:space-between; font-size:11px; color:var(--muted);
}
.label {
  display:inline-block; font-size:12px; font-weight:700; color:var(--accent);
  border:1px solid var(--accent); border-radius:999px; padding:3px 12px;
  letter-spacing:2px; margin:20px 0 10px; align-self:flex-start;
}
.chip { border-radius:6px; padding:2px 8px; font-size:11px; font-weight:700; }
.chip.good  { color:var(--good); border:1px solid var(--good); }
.chip.warn  { color:var(--warn); border:1px solid var(--warn); }
.chip.bad   { color:var(--bad);  border:1px solid var(--bad); }
.chip.plain { color:var(--ink-2); border:1px solid var(--hairline); }
""" % {"vars": CSS_VARS}

HEADER = """<div class="hdr"><div class="brand">ainxiety<span class="dot">.</span>lab</div>
<div class="date">{date}</div></div>"""
FOOTER = """<div class="ftr"><span>幫你戒訂閱費的工具偵察兵・親測不吹捧</span><span>{handle}</span></div>"""


def esc(s):
    return html.escape(str(s or ""))


def tpl_radar(d):
    rows = ""
    for it in d.get("items", [])[:6]:
        rows += f"""
        <div style="display:flex;gap:12px;align-items:baseline;padding:8.5px 0;
                    border-bottom:1px solid var(--hairline)">
          <div style="font-size:17px;font-weight:900;color:var(--accent);
                      min-width:22px;font-variant-numeric:tabular-nums">{esc(it.get('rank'))}</div>
          <div style="flex:1;min-width:0">
            <div style="display:flex;justify-content:space-between;gap:8px;align-items:baseline">
              <div style="font-size:16.5px;font-weight:700;white-space:nowrap;overflow:hidden;
                          text-overflow:ellipsis">{esc(it.get('name'))}</div>
              <div style="font-size:13px;font-weight:700;color:var(--good);white-space:nowrap;
                          font-variant-numeric:tabular-nums">{esc(it.get('delta'))}</div>
            </div>
            <div style="font-size:12.5px;color:var(--ink-2);margin-top:2px;white-space:nowrap;
                        overflow:hidden;text-overflow:ellipsis">{esc(it.get('desc'))}</div>
          </div>
        </div>"""
    label = d.get("label") or "GITHUB 潛力雷達"
    title = d.get("title") or f"本週竄升最快的 {len(d.get('items', [])[:6])} 個工具"
    return f"""{HEADER.format(date=esc(d.get('date')))}
      <div class="label">{esc(label)}</div>
      <div style="font-size:29px;font-weight:900;line-height:1.25;margin-bottom:10px">
        {esc(title)}</div>
      <div>{rows}</div>
      <div style="font-size:12px;color:var(--muted);margin-top:10px">完整分析與連結請看留言 👇</div>
      {FOOTER.format(handle=esc(d.get('handle') or ''))}"""


def tpl_spotlight(d):
    badges = "".join(
        f'<span class="chip {esc(b.get("kind") or "plain")}">{esc(b.get("text"))}</span>'
        for b in d.get("badges", []))
    return f"""{HEADER.format(date=esc(d.get('date')))}
      <div class="label">{esc(d.get('label') or '本週焦點')}</div>
      <div style="font-size:34px;font-weight:900;line-height:1.2;word-break:break-all">
        {esc(d.get('name'))}</div>
      <div style="font-size:16px;color:var(--ink-2);line-height:1.6;margin-top:12px">
        {esc(d.get('desc'))}</div>
      <div style="margin-top:auto;margin-bottom:auto;text-align:center">
        <div style="font-size:76px;font-weight:900;color:var(--good);letter-spacing:-2px">
          {esc(d.get('hero'))}</div>
        <div style="font-size:14px;color:var(--muted);margin-top:2px">{esc(d.get('hero_label'))}</div>
      </div>
      <div style="display:flex;gap:8px;margin-bottom:14px">{badges}</div>
      {FOOTER.format(handle=esc(d.get('handle') or ''))}"""


def tpl_verdict(d):
    kind = {"good": "good", "warn": "warn", "bad": "bad"}.get(d.get("verdict_kind"), "warn")
    color = {"good": "var(--good)", "warn": "var(--warn)", "bad": "var(--bad)"}[kind]
    rows = "".join(f"""
      <div style="display:flex;gap:14px;padding:13px 0;border-bottom:1px solid var(--hairline)">
        <div style="font-size:24px">{esc(p.get('icon'))}</div>
        <div style="font-size:15.5px;line-height:1.55;color:var(--ink-2);
                    align-self:center">{esc(p.get('text'))}</div>
      </div>""" for p in d.get("points", [])[:4])
    return f"""{HEADER.format(date=esc(d.get('date')))}
      <div class="label">實測報告</div>
      <div style="font-size:33px;font-weight:900;line-height:1.2">{esc(d.get('name'))}</div>
      <div style="font-size:13px;color:var(--muted);margin-top:4px">真的裝、真的跑、真的踩雷</div>
      <div style="margin-top:12px">{rows}</div>
      <div style="margin-top:auto;margin-bottom:12px;text-align:center">
        <span style="display:inline-block;font-size:30px;font-weight:900;color:{color};
                     border:3px solid {color};border-radius:14px;padding:8px 34px;
                     transform:rotate(-2deg)">{esc(d.get('verdict'))}</span>
      </div>
      {FOOTER.format(handle=esc(d.get('handle') or ''))}"""


def tpl_quote(d):
    # Oversized brackets pinned to the text block's own corners so the quote
    # reads as enclosed — the wrapper shrinks to the text, brackets follow it.
    return f"""{HEADER.format(date=esc(d.get('date')))}
      <div class="label">{esc(d.get('label') or '今日 AI 短評')}</div>
      <div style="flex:1;display:flex;align-items:center;justify-content:center">
        <div style="position:relative;display:inline-block;padding:30px 34px;max-width:440px">
          <div style="position:absolute;top:-14px;left:-10px;font-size:64px;font-weight:900;
                      color:var(--accent);line-height:1">「</div>
          <div style="font-size:27px;font-weight:900;line-height:1.6;white-space:pre-line;
                      text-wrap:balance">{esc(d.get('quote'))}</div>
          <div style="position:absolute;bottom:-14px;right:-10px;font-size:64px;font-weight:900;
                      color:var(--accent);line-height:1">」</div>
        </div>
      </div>
      <div style="font-size:13.5px;color:var(--ink-2);line-height:1.6;margin-bottom:14px">
        {esc(d.get('context'))}</div>
      {FOOTER.format(handle=esc(d.get('handle') or ''))}"""


def tpl_digest(d):
    rows = "".join(f"""
      <div style="display:flex;gap:14px;padding:13px 0;border-bottom:1px solid var(--hairline)">
        <div style="font-size:18px;font-weight:900;color:var(--accent);
                    font-variant-numeric:tabular-nums">{i+1}</div>
        <div style="font-size:16px;line-height:1.55;color:var(--ink-2)">{esc(t)}</div>
      </div>""" for i, t in enumerate(d.get("items", [])[:5]))
    teaser = d.get("teaser")
    teaser_html = (f'<div style="font-size:14px;color:var(--warn);font-weight:700;'
                   f'margin-top:14px">⏭ {esc(teaser)}</div>') if teaser else ""
    return f"""{HEADER.format(date=esc(d.get('date')))}
      <div class="label">本週回顧</div>
      <div style="font-size:30px;font-weight:900;line-height:1.25">
        {esc(d.get('title') or '本週 AI 圈回顧')}</div>
      <div style="margin-top:12px">{rows}</div>
      {teaser_html}
      {FOOTER.format(handle=esc(d.get('handle') or ''))}"""


TEMPLATES = {"radar": tpl_radar, "spotlight": tpl_spotlight, "verdict": tpl_verdict,
             "quote": tpl_quote, "digest": tpl_digest}


def find_chromium(override=""):
    if override:
        return override
    pw = os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")
    for c in (os.path.join(pw, "chromium"),):
        if os.path.exists(c):
            return c
    for name in ("chromium", "chromium-browser", "google-chrome", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("chromium not found; pass --chromium /path/to/chromium")


def font_css(fonts_dir=""):
    """Build @font-face CSS from the fontsource noto-sans-tc package if present."""
    root = fonts_dir or os.environ.get("NOTO_TC_DIR", "")
    if not root:
        for cand in ("node_modules/@fontsource/noto-sans-tc",
                     os.path.join(os.path.dirname(__file__), "..",
                                  "node_modules/@fontsource/noto-sans-tc")):
            if os.path.isdir(cand):
                root = cand
                break
    if not root or not os.path.isdir(root):
        return ""  # fall back to system CJK fonts
    css = []
    for weight in ("400", "700", "900"):
        f = os.path.join(root, f"{weight}.css")
        if os.path.exists(f):
            text = open(f, encoding="utf-8").read()
            text = text.replace("./files/", "file://" + os.path.abspath(
                os.path.join(root, "files")) + "/")
            css.append(text)
    return "\n".join(css)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--type", required=True, choices=sorted(TEMPLATES))
    ap.add_argument("--data", help="path to JSON payload")
    ap.add_argument("--json", help="inline JSON payload")
    ap.add_argument("--out", required=True, help="output PNG path")
    ap.add_argument("--handle", default="", help="account handle for the footer")
    ap.add_argument("--chromium", default="")
    ap.add_argument("--fonts-dir", default="")
    args = ap.parse_args()

    if args.data:
        payload = json.load(open(args.data, encoding="utf-8"))
    elif args.json:
        payload = json.loads(args.json)
    else:
        sys.exit("provide --data FILE or --json '...'")
    if args.handle:
        payload.setdefault("handle", args.handle)

    body = TEMPLATES[args.type](payload)
    doc = f"""<!doctype html><html><head><meta charset="utf-8">
<style>{font_css(args.fonts_dir)}</style><style>{BASE_CSS}</style>
</head><body><div class="card">{body}</div></body></html>"""

    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False,
                                     encoding="utf-8") as f:
        f.write(doc)
        html_path = f.name
    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    # Headless Chromium's viewport comes out ~87 CSS px shorter than
    # --window-size (window chrome is counted even in headless), so render
    # with generous overscan and crop to the exact 1080x1350 with Pillow.
    shot = out + ".raw.png"
    try:
        subprocess.run(
            [find_chromium(args.chromium), "--headless", "--disable-gpu",
             "--no-sandbox", "--hide-scrollbars", "--force-device-scale-factor=2",
             f"--screenshot={shot}", "--window-size=540,900", html_path],
            check=True, capture_output=True, timeout=60)
        if Image is None:
            sys.exit("pillow is required to crop the card: pip install pillow")
        im = Image.open(shot)
        if im.size[0] < 1080 or im.size[1] < 1350:
            sys.exit(f"screenshot too small ({im.size}); expected >= 1080x1350")
        im.crop((0, 0, 1080, 1350)).save(out)
    finally:
        os.unlink(html_path)
        if os.path.exists(shot):
            os.unlink(shot)
    print(f"wrote {out} (1080x1350, {os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
