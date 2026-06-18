"""
update_dataplant_tools.py
=========================
Fetches contributor data for all DataPLANT repositories from GitHub
and prints a summary that can be used to update the HTML overview files.

Usage:
    pip install requests
    python update_dataplant_tools.py

Optional: set a GitHub token to avoid rate limiting (60 req/h → 5000 req/h):
    set GITHUB_TOKEN=your_token_here        # Windows
    export GITHUB_TOKEN=your_token_here     # Mac/Linux
"""

import os
import requests
from datetime import datetime

ORG = "nfdi4plants"

# Repos to track (add or remove as needed)
REPOS = [
    "ARCitect",
    "ARCtrl",
    "Swate",
    "swate-template-registry",
    "nfdi4plants_ontology",
    "ARCCommander",
    "ARCmanager",
    "DataHUB",
    "arc-export",
    "ARCSummary",
    "arcfs-fsspec",
    "archigator-frontend",
    "ARC-specification",
    "elab2ARC",
    "dataplan",
    "metadataquiz",
    "nfdi4plants.knowledgebase",
    "training-material",
    "Delight",
    "arc-vs-code",
]

# ── Auth ──────────────────────────────────────────────────────────────────────
TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
if not TOKEN:
    print("⚠  No GITHUB_TOKEN set — using unauthenticated requests (60 req/h limit).")
    print("   Set the env var GITHUB_TOKEN to increase limit to 5000 req/h.\n")

# ── Helpers ───────────────────────────────────────────────────────────────────
def get(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code == 403:
        print(f"  ⚠  Rate limited on {url} — consider setting GITHUB_TOKEN")
        return []
    if r.status_code == 404:
        return []
    r.raise_for_status()
    return r.json()

def get_contributors(repo, top=3):
    data = get(f"https://api.github.com/repos/{ORG}/{repo}/contributors?per_page=10")
    if not isinstance(data, list):
        return []
    # filter out bots
    humans = [c for c in data if "[bot]" not in c.get("login", "")]
    return humans[:top]

def get_real_name(login):
    data = get(f"https://api.github.com/users/{login}")
    if isinstance(data, dict):
        return data.get("name") or login
    return login

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"DataPLANT Tool Contributor Report")
    print(f"Organisation : {ORG}")
    print(f"Generated    : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    # Cache real names to avoid duplicate API calls
    name_cache = {}

    results = {}
    for repo in REPOS:
        print(f"\n📦 {repo}")
        contributors = get_contributors(repo, top=3)
        if not contributors:
            print("   (no data or repo not found)")
            results[repo] = []
            continue

        repo_result = []
        for c in contributors:
            login = c["login"]
            commits = c["contributions"]
            if login not in name_cache:
                name_cache[login] = get_real_name(login)
            real_name = name_cache[login]
            print(f"   {real_name:30s} @{login:25s} {commits:5d} commits")
            repo_result.append({
                "name": real_name,
                "login": login,
                "commits": commits,
            })
        results[repo] = repo_result

    # ── Summary table ─────────────────────────────────────────────────────────
    print("\n\n" + "=" * 60)
    print("COPY-PASTE SUMMARY (for updating the HTML files)")
    print("=" * 60)
    for repo, contributors in results.items():
        if not contributors:
            continue
        people = " · ".join(
            f"{c['name']} ({c['commits']} commits)" for c in contributors
        )
        print(f"\n{repo}")
        print(f"  → {people}")

    # ── Changed repos (simple heuristic: flag repos with very recent commits) ─
    print("\n\n" + "=" * 60)
    print("CHECKING LAST PUSH DATE (to spot recently updated repos)")
    print("=" * 60)
    for repo in REPOS:
        data = get(f"https://api.github.com/repos/{ORG}/{repo}")
        if isinstance(data, dict):
            pushed = data.get("pushed_at", "unknown")
            updated = data.get("updated_at", "unknown")
            print(f"  {repo:40s}  last push: {pushed[:10]}")

if __name__ == "__main__":
    main()
