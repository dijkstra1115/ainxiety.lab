#!/usr/bin/env python3
"""Fetch AI-related news candidates from free, keyless sources:

1. Hacker News (Algolia API) — high-signal tech community, free, no key.
2. Hugging Face daily papers API — trending AI research, free, no key.

Output: one JSON document (stdout or --out FILE) for Claude to rank and
turn into a Threads-ready commentary draft. If a source is unreachable
(restricted network), it is reported in "errors" and the skill falls back
to WebFetch/WebSearch — see SKILL.md.

Usage:
    python3 fetch_ai_news.py
    python3 fetch_ai_news.py --hours 36 --min-points 80
    python3 fetch_ai_news.py --out reports/news_raw.json
"""

import argparse
import json
import os
import ssl
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

UA = "ai-news-skill/1.0"

AI_KEYWORDS = (
    "ai", "llm", "gpt", "claude", "gemini", "openai", "anthropic", "deepseek",
    "mistral", "llama", "agent", "model", "transformer", "diffusion",
    "machine learning", "neural", "copilot", "rag", "fine-tun", "inference",
)


def _ssl_context():
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if not cafile and os.path.exists("/root/.ccr/ca-bundle.crt"):
        cafile = "/root/.ccr/ca-bundle.crt"
    try:
        return ssl.create_default_context(cafile=cafile)
    except Exception:
        return ssl.create_default_context()


CTX = _ssl_context()


def get_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def looks_ai(text):
    t = (text or "").lower()
    return any(k in t for k in AI_KEYWORDS)


def fetch_hn(hours=24, min_points=80):
    """Front-page-quality stories from the last N hours, AI-filtered."""
    cutoff = int((datetime.now(timezone.utc) - timedelta(hours=hours)).timestamp())
    url = ("https://hn.algolia.com/api/v1/search_by_date?"
           + urllib.parse.urlencode({
                 "tags": "story",
                 "numericFilters": f"points>{min_points},created_at_i>{cutoff}",
                 "hitsPerPage": 100,
             }))
    hits = get_json(url).get("hits", [])
    out = []
    for h in hits:
        title = h.get("title") or ""
        if not looks_ai(title + " " + (h.get("url") or "")):
            continue
        out.append({
            "title": title,
            "url": h.get("url") or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
            "hn_url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
            "points": h.get("points"),
            "num_comments": h.get("num_comments"),
            "created_at": h.get("created_at"),
            "source": "hackernews",
        })
    out.sort(key=lambda x: x.get("points") or 0, reverse=True)
    return out


def fetch_hf_papers(limit=15):
    """Hugging Face daily papers — what AI researchers are upvoting today."""
    papers = get_json("https://huggingface.co/api/daily_papers?limit=%d" % limit)
    out = []
    for p in papers:
        paper = p.get("paper") or {}
        out.append({
            "title": paper.get("title"),
            "url": "https://huggingface.co/papers/" + str(paper.get("id")),
            "upvotes": paper.get("upvotes"),
            "summary_excerpt": (paper.get("summary") or "")[:400],
            "source": "hf_papers",
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=int, default=24, help="HN lookback window")
    ap.add_argument("--min-points", type=int, default=80, help="HN minimum points")
    ap.add_argument("--out", default="", help="write JSON to file instead of stdout")
    args = ap.parse_args()

    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "errors": [],
        "hackernews": [],
        "hf_papers": [],
    }
    for key, fn in [
        ("hackernews", lambda: fetch_hn(args.hours, args.min_points)),
        ("hf_papers", fetch_hf_papers),
    ]:
        try:
            result[key] = fn()
        except Exception as e:
            result["errors"].append(f"{key}: {e}")

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"wrote {args.out}: hn={len(result['hackernews'])} "
              f"hf={len(result['hf_papers'])} errors={result['errors']}")
    else:
        print(out)


if __name__ == "__main__":
    main()
