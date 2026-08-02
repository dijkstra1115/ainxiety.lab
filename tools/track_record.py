#!/usr/bin/env python3
"""Track-record report: how did our featured repos grow since we featured them?

Reads reports/seen.json (repo entries with stars_at_feature), fetches current
star counts from the GitHub API (free; uses GITHUB_TOKEN/GH_TOKEN if present),
and prints a markdown scoreboard sorted by growth.

This powers the monthly "上月雷達回顧" post — the public, verifiable proof of
the account's eye for winners (and its honesty about misses).

Usage:
    python3 tools/track_record.py                     # all featured repos
    python3 tools/track_record.py --since 2026-08-01  # featured on/after date
    python3 tools/track_record.py --out reports/track-record.md

In network-restricted sandboxes where api.github.com is blocked, run with
--stars-json '{"owner/repo": 12345, ...}' (current counts gathered via
WebFetch) to skip API calls.
"""

import argparse
import json
import os
import ssl
import urllib.request
from datetime import datetime, timezone

SEEN = os.path.join(os.path.dirname(__file__), "..", "reports", "seen.json")


def _ctx():
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if not cafile and os.path.exists("/root/.ccr/ca-bundle.crt"):
        cafile = "/root/.ccr/ca-bundle.crt"
    try:
        return ssl.create_default_context(cafile=cafile)
    except Exception:
        return ssl.create_default_context()


def current_stars(full_name, ctx):
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "track-record/1.0"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(
        f"https://api.github.com/repos/{full_name}", headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return json.load(r).get("stargazers_count")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default="", help="only repos featured on/after YYYY-MM-DD")
    ap.add_argument("--stars-json", default="",
                    help="JSON dict of current stars to use instead of the API")
    ap.add_argument("--out", default="", help="write markdown to file")
    args = ap.parse_args()

    seen = json.load(open(SEEN, encoding="utf-8"))
    provided = json.loads(args.stars_json) if args.stars_json else {}
    ctx = _ctx()

    rows, errors = [], []
    for name, meta in seen.items():
        if ":" in name:          # news:/deepdive: entries aren't radar picks
            continue
        if not isinstance(meta, dict) or "stars_at_feature" not in meta:
            continue
        if args.since and meta.get("featured_on", "") < args.since:
            continue
        base = meta["stars_at_feature"]
        try:
            now = provided.get(name)
            if now is None:
                now = current_stars(name, ctx)
            growth = (now - base) / base * 100 if base else 0
            rows.append((name, meta.get("featured_on", "?"), base, now, growth))
        except Exception as e:
            errors.append(f"{name}: {e}")

    rows.sort(key=lambda r: r[4], reverse=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"# 雷達戰績 {today}", "",
             "| repo | 推薦日 | 推薦時 ⭐ | 現在 ⭐ | 成長 |",
             "|---|---|---|---|---|"]
    for name, day, base, now, growth in rows:
        lines.append(f"| {name} | {day} | {base:,} | {now:,} | {growth:+.1f}% |")
    if errors:
        lines += ["", "查詢失敗（網路受限時改用 --stars-json）：",
                  *[f"- {e}" for e in errors]]
    out = "\n".join(lines) + "\n"

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"wrote {args.out} ({len(rows)} repos, {len(errors)} errors)")
    else:
        print(out)


if __name__ == "__main__":
    main()
