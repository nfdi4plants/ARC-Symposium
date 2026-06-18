# DataPLANT Tool Overview

Interactive HTML reference pages for the [DataPLANT](https://www.nfdi4plants.org) tool ecosystem, aimed at **new data stewards and collaborators** who want to understand which tools exist, what they do, and who to contact.

## Contributors

- Sabrina Zander ([@SabrinaZander](https://github.com/SabrinaZander))

## Motivation / Problem

DataPLANT provides a growing number of tools around the **ARC**.  For newcomers — especially new data stewards — it is hard to get an overview of:

- which tools exist and what each one does
- which tool to use at which point in the research workflow
- who is responsible for each tool and who to contact with questions

No single, up-to-date, visual reference existed that answers all three questions in one place.

## Proposed Solution

Two standalone HTML pages that can be opened in any browser without installation, shared via link, and updated semi-automatically via a Python script:

| File | Description |
|---|---|
| `DataPLANT_Tool_Overview.html` | Workflow-based onboarding overview organised into 5 steps (Create ARCs → Annotate → Collaborate → Publish → Learn). Filterable by category, searchable, with "When do I use this?" guidance per tool. |
| `DataPLANT_Interactive_Map.html` | Draggable node map showing all tools and their dependencies. Nodes can be rearranged freely; arrows update live. Click any node for details and contact persons. |

Both files are **fully self-contained** — they work offline and require no server or framework.

**Constraints:**
- Responsible persons are approximated by **commit count** via the GitHub API, which is a proxy for ownership but may not always reflect the true maintainer.
- The HTML files must be updated manually when tool information changes — they are not yet auto-generated from the script output.
- GitHub API rate limits apply when running the update script without authentication (60 req/h unauthenticated vs. 5,000 req/h with a token).

## Technical Details

### Data sources

Tool and contributor data was retrieved from the [nfdi4plants GitHub organisation](https://github.com/nfdi4plants) using the GitHub REST API:

- `GET /repos/{org}/{repo}/contributors` — top contributors per repo
- `GET /users/{login}` — resolve GitHub handle to real name

### Update script

`update_dataplant_tools.py` re-fetches contributor data for all tracked repos and prints a structured summary with last-push dates so you can spot which tools have changed.

```bash
pip install requests

# Optional but recommended — avoids rate limiting
set GITHUB_TOKEN=your_token_here   # Windows
export GITHUB_TOKEN=your_token_here # Mac/Linux

python update_dataplant_tools.py
```


## As of

June 2025 — based on public GitHub data from [github.com/nfdi4plants](https://github.com/nfdi4plants)
