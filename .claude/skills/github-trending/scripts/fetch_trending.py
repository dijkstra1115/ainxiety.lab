#!/usr/bin/env python3
"""Fetch fast-growing GitHub repos from two free sources:

1. GitHub Trending page (https://github.com/trending) — gives "stars gained
   today / this week", no API key needed.
2. GitHub Search API — finds young repos (created recently) that already
   collected many stars, i.e. high star velocity. Works unauthenticated;
   uses GITHUB_TOKEN / GH_TOKEN automatically if present for higher rate
   limits.

Output: a single JSON document on stdout (or --out FILE) that Claude can
read and turn into a report. No paid services involved.

Usage:
    python3 fetch_trending.py                      # daily + weekly trending + rising newcomers
    python3 fetch_trending.py --lang python        # filter trending by language
    python3 fetch_trending.py --days 14 --min-stars 300
    python3 fetch_trending.py --readme-top 8       # also fetch README excerpts for top repos
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html import unescape

UA = "github-trending-skill/1.0 (+https://github.com)"


def _ssl_context():
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if not cafile:
        for candidate in ("/root/.ccr/ca-bundle.crt",):
            if os.path.exists(candidate):
                cafile = candidate
                break
    try:
        return ssl.create_default_context(cafile=cafile)
    except Exception:
        return ssl.create_default_context()


CTX = _ssl_context()


def http_get(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
        return resp.read().decode("utf-8", errors="replace")


def gh_token():
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""


def api_get(path_or_url):
    url = path_or_url if path_or_url.startswith("http") else "https://api.github.com" + path_or_url
    headers = {"Accept": "application/vnd.github+json"}
    token = gh_token()
    if token:
        headers["Authorization"] = "Bearer " + token
    return json.loads(http_get(url, headers=headers))


# ---------------------------------------------------------------------------
# Source 1: github.com/trending (HTML, no auth)
# ---------------------------------------------------------------------------

ARTICLE_RE = re.compile(r"<article class=\"Box-row\">(.*?)</article>", re.S)
REPO_RE = re.compile(r'href="/([^/"]+/[^/"]+)"')
DESC_RE = re.compile(r"<p class=\"col-9[^\"]*\">\s*(.*?)\s*</p>", re.S)
LANG_RE = re.compile(r'itemprop="programmingLanguage">([^<]+)</span>')
STARS_TOTAL_RE = re.compile(r'href="/[^"]+/stargazers"[^>]*>\s*<svg[^>]*>.*?</svg>\s*([\d,]+)', re.S)
STARS_PERIOD_RE = re.compile(r"([\d,]+)\s+stars\s+(?:today|this week|this month)")
TAG_RE = re.compile(r"<[^>]+>")


def parse_int(s):
    try:
        return int(s.replace(",", ""))
    except Exception:
        return None


def fetch_trending_page(since="daily", language=""):
    qs = urllib.parse.urlencode({"since": since})
    lang_path = "/" + urllib.parse.quote(language) if language else ""
    url = f"https://github.com/trending{lang_path}?{qs}"
    html = http_get(url)
    repos = []
    for block in ARTICLE_RE.findall(html):
        m = REPO_RE.search(block)
        if not m:
            continue
        full_name = m.group(1)
        desc_m = DESC_RE.search(block)
        desc = unescape(TAG_RE.sub("", desc_m.group(1)).strip()) if desc_m else ""
        lang_m = LANG_RE.search(block)
        stars_m = STARS_TOTAL_RE.search(block)
        period_m = STARS_PERIOD_RE.search(block)
        repos.append({
            "full_name": full_name,
            "url": f"https://github.com/{full_name}",
            "description": desc,
            "language": lang_m.group(1) if lang_m else None,
            "stars_total": parse_int(stars_m.group(1)) if stars_m else None,
            "stars_gained": parse_int(period_m.group(1)) if period_m else None,
            "period": since,
            "source": f"trending_{since}",
        })
    return repos


# ---------------------------------------------------------------------------
# Source 2: Search API — young repos with lots of stars (high velocity)
# ---------------------------------------------------------------------------

def fetch_rising_newcomers(days=30, min_stars=200, per_page=25, query=""):
    created_after = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    q = query or f"created:>{created_after} stars:>{min_stars}"
    data = api_get(
        "/search/repositories?"
        + urllib.parse.urlencode({"q": q, "sort": "stars", "order": "desc", "per_page": per_page})
    )
    repos = []
    for item in data.get("items", []):
        age_days = max(
            1,
            (datetime.now(timezone.utc)
             - datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))).days,
        )
        repos.append({
            "full_name": item["full_name"],
            "url": item["html_url"],
            "description": item.get("description") or "",
            "language": item.get("language"),
            "stars_total": item["stargazers_count"],
            "created_at": item["created_at"],
            "age_days": age_days,
            "stars_per_day": round(item["stargazers_count"] / age_days, 1),
            "topics": item.get("topics", [])[:8],
            "source": "search_newcomers",
        })
    repos.sort(key=lambda r: r["stars_per_day"], reverse=True)
    return repos


# ---------------------------------------------------------------------------
# Optional: README excerpts so the analysis step needs fewer web fetches
# ---------------------------------------------------------------------------

def fetch_readme_excerpt(full_name, max_chars=4000):
    try:
        data = api_get(f"/repos/{full_name}/readme")
        import base64
        text = base64.b64decode(data.get("content", "")).decode("utf-8", errors="replace")
        return text[:max_chars]
    except Exception as e:
        return f"(failed to fetch README: {e})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="", help="language filter for trending pages, e.g. python")
    ap.add_argument("--days", type=int, default=30, help="newcomer window in days")
    ap.add_argument("--min-stars", type=int, default=200, help="newcomer min stars")
    ap.add_argument("--readme-top", type=int, default=0,
                    help="fetch README excerpts for top N repos across all sources")
    ap.add_argument("--query", default="",
                    help="override the newcomer search query entirely, e.g. "
                         "'created:>2026-05-01 stars:>300 topic:self-hosted'")
    ap.add_argument("--out", default="", help="write JSON to this file instead of stdout")
    args = ap.parse_args()

    result = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "token_used": bool(gh_token()),
        "errors": [],
        "trending_daily": [],
        "trending_weekly": [],
        "rising_newcomers": [],
    }

    for key, fn in [
        ("trending_daily", lambda: fetch_trending_page("daily", args.lang)),
        ("trending_weekly", lambda: fetch_trending_page("weekly", args.lang)),
        ("rising_newcomers", lambda: fetch_rising_newcomers(args.days, args.min_stars,
                                                            query=args.query)),
    ]:
        try:
            result[key] = fn()
        except Exception as e:
            result["errors"].append(f"{key}: {e}")

    if args.readme_top > 0:
        seen, picked = set(), []
        for repo in (result["trending_daily"] + result["rising_newcomers"]
                     + result["trending_weekly"]):
            if repo["full_name"] not in seen:
                seen.add(repo["full_name"])
                picked.append(repo)
            if len(picked) >= args.readme_top:
                break
        for repo in picked:
            repo["readme_excerpt"] = fetch_readme_excerpt(repo["full_name"])

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        counts = {k: len(v) for k, v in result.items() if isinstance(v, list) and k != "errors"}
        print(f"wrote {args.out}: {counts}; errors={result['errors']}")
    else:
        print(out)


if __name__ == "__main__":
    main()
