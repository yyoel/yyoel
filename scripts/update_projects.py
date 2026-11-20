#!/usr/bin/env python3
"""Rewrite the "recently updated projects" block of README.md.

Lists the owner's most recently pushed public repositories (no forks,
no archived repos, not the profile repo itself) between the
<!--START_PROJECTS--> and <!--END_PROJECTS--> markers.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

OWNER = os.environ.get("GH_OWNER", "yyoel")
LIMIT = int(os.environ.get("PROJECT_LIMIT", "6"))
README = os.path.join(os.path.dirname(__file__), "..", "README.md")
START, END = "<!--START_PROJECTS-->", "<!--END_PROJECTS-->"
CONTRIB_LIMIT = int(os.environ.get("CONTRIB_LIMIT", "4"))
CONTRIB_DAYS = int(os.environ.get("CONTRIB_DAYS", "365"))


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_repos():
    return get(f"https://api.github.com/users/{OWNER}/repos?type=owner&sort=pushed&direction=desc&per_page=100")


def fetch_external_prs():
    """Open or merged PRs the owner made to other people's repos (e.g. from a fork)."""
    since = (datetime.now(timezone.utc) - timedelta(days=CONTRIB_DAYS)).strftime("%Y-%m-%d")
    q = urllib.parse.quote(f"is:pr author:{OWNER} -user:{OWNER} updated:>={since}")
    items = get(f"https://api.github.com/search/issues?q={q}&sort=updated&order=desc&per_page=50")["items"]
    picked, seen = [], set()
    for pr in items:
        merged = pr.get("pull_request", {}).get("merged_at")
        if pr["state"] != "open" and not merged:
            continue  # closed without merging
        repo = pr["repository_url"].split("/repos/", 1)[1]
        key = (repo, pr["title"])
        if key in seen:
            continue
        seen.add(key)
        status = "🟢 Open" if pr["state"] == "open" else "🟣 Merged"
        picked.append((repo, pr, status))
    return picked[:CONTRIB_LIMIT]


def build_block(repos):
    picked = [
        r for r in repos
        if not r["private"] and not r["fork"] and not r["archived"] and r["name"].lower() != OWNER.lower()
    ][:LIMIT]
    lines = ["| Project | What it is | Stack | Last push |", "| --- | --- | --- | --- |"]
    for r in picked:
        desc = (r.get("description") or "No description yet").replace("|", "\\|")
        lang = r.get("language") or "-"
        lines.append(f"| [**{r['name']}**]({r['html_url']}) | {desc} | {lang} | {r['pushed_at'][:10]} |")
    return "\n".join(lines)


def build_contrib_block(prs):
    if not prs:
        return ""
    lines = ["", "", "**Contributing to other projects**", "", "| Project | Pull request | Status |", "| --- | --- | --- |"]
    for repo, pr, status in prs:
        title = pr["title"].replace("|", "\\|")
        lines.append(f"| [**{repo}**](https://github.com/{repo}) | [{title}]({pr['html_url']}) | {status} |")
    return "\n".join(lines)


def main():
    block = build_block(fetch_repos()) + build_contrib_block(fetch_external_prs())
    with open(README, encoding="utf-8") as f:
        text = f.read()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(text):
        sys.exit("Markers not found in README.md")
    new = pattern.sub(lambda _: f"{START}\n{block}\n{END}", text)
    if new != text:
        with open(README, "w", encoding="utf-8") as f:
            f.write(new)
        print("README updated")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
