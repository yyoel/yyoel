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
import urllib.request

OWNER = os.environ.get("GH_OWNER", "yyoel")
LIMIT = int(os.environ.get("PROJECT_LIMIT", "6"))
README = os.path.join(os.path.dirname(__file__), "..", "README.md")
START, END = "<!--START_PROJECTS-->", "<!--END_PROJECTS-->"


def fetch_repos():
    url = f"https://api.github.com/users/{OWNER}/repos?type=owner&sort=pushed&direction=desc&per_page=100"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


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


def main():
    block = build_block(fetch_repos())
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
