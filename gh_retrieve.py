#!/usr/bin/env python3
"""
Download GitHub issues and pull requests (with discussions) as Markdown files
for ingestion by the LLM Wiki.

Files are written to `raw/github/<repo-owner>__<repo-name>/` as:
  - issue-<number>.md
  - pr-<number>.md

State is tracked in `raw/github/<repo-owner>__<repo-name>/.sync-state.json`
so repeated runs only re-download items that are new or have been updated
since the last sync.

Incremental sync strategy (minimises GitHub API calls):
  * The state file records a `high_water` timestamp -- the time at which
    the most recent *complete* sync started. Items with `updated_at <=
    high_water` are guaranteed to already be on disk.
  * On each run the script passes `since=<high_water>` to GitHub's
    /issues endpoint, so the server only returns items modified after
    that point. Closing or reopening an issue/PR bumps `updated_at`,
    so state transitions are picked up automatically.
  * The /issues listing is sorted by `updated` desc. As soon as we hit
    an item whose `updated_at` matches what we already have, every later
    page must be unchanged -- so we stop paginating immediately.
  * `high_water` is only advanced when a run finishes without being
    truncated by MAX_ITEMS. A capped run leaves it untouched so the
    next run re-lists the tail it missed.

Steady-state cost: 1 list request per sync when nothing changed,
1 + (changed_items * ~4) requests when items did change.

Configuration:
  * REPO                 -- "owner/name" of the GitHub repository to mirror.
  * OUTPUT_ROOT          -- directory to write markdown into.
  * GITHUB_TOKEN (env)   -- optional, avoids tight anon rate limits.
  * STATE (env) values   -- "open", "closed", "all". Default "all".
                            Use "all" so closed/reopened items are tracked
                            via their bumped `updated_at`.
  * MAX_ITEMS (env)      -- cap items scanned per run (0 = unlimited).
                            A capped run will NOT advance high_water.

Example usage:

  # 1) First run, bounded smoke test against the default repo (Kueue).
  #    20 most-recently-updated issues/PRs; anonymous -> 60 req/hr.
  #    high_water is left empty so the next uncapped run still walks
  #    the full backlog.
  MAX_ITEMS=20 python gh_retrieve.py

  # 2) Authenticated full sync (5000 req/hr) of the default repo.
  #    First call walks the entire history and sets high_water at the end;
  #    every later call is a cheap incremental fetch driven by `since=`.
  export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
  python gh_retrieve.py

  # 3) Point the script at a different repository without editing the file.
  REPO=kubernetes/kubernetes STATE=open MAX_ITEMS=50 python gh_retrieve.py

  # 4) Only open items, writing to raw/github/kubernetes-sigs__kueue/.
  #    Note: `STATE=open` will miss issues that close between runs.
  #    Prefer the default `STATE=all` for incremental syncs.
  STATE=open python gh_retrieve.py

  # 5) Cron-style incremental refresh every 6 hours.
  #    The state file's high_water + GitHub's `since=` keep this nearly
  #    free -- typically 1 API call when the repo has been quiet.
  #    0 */6 * * * cd /path/to/kueue-llm-wiki && \
  #       GITHUB_TOKEN=ghp_xxx /usr/bin/python gh_retrieve.py >> sync.log 2>&1

  # 6) Force a full re-download of everything: delete the state file and re-run.
  #    Removes both the per-item updated_at cache and the high_water mark.
  rm raw/github/kubernetes-sigs__kueue/.sync-state.json
  python gh_retrieve.py

  # 7) Force a full *re-check* without re-downloading unchanged items:
  #    edit the state file and set "high_water" to "" (or delete the key).
  #    The script will re-list everything but only fetch items whose
  #    updated_at is newer than what's recorded per-item.

  # 8) Import and drive it from another Python script:
  #    from gh_retrieve import sync, OUTPUT_ROOT
  #    sync("kubernetes-sigs/kueue", OUTPUT_ROOT, state_filter="all", max_items=0)
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Change this (or set the REPO env var) to point the script at another repo.
REPO: str = os.environ.get("REPO", "kubernetes-sigs/kueue")

# Where markdown files are written. Per CLAUDE.md, raw/ holds immutable
# source documents, so downloaded issues/PRs belong under raw/.
OUTPUT_ROOT: Path = Path(__file__).parent / "raw" / "github"

# "open" | "closed" | "all"
STATE: str = os.environ.get("STATE", "all")

# Per-page size for list endpoints. 100 is the max GitHub allows.
PAGE_SIZE: int = 100

# Cap so a first run does not pull the entire repo history.
# Set to 0 for unlimited.
MAX_ITEMS: int = int(os.environ.get("MAX_ITEMS", "0"))

API = "https://api.github.com"


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _headers() -> dict[str, str]:
    h = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "kueue-llm-wiki-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _request(url: str) -> tuple[Any, dict[str, str]]:
    """Single GET. Returns (parsed_json, response_headers)."""
    req = urllib.request.Request(url, headers=_headers())
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data, dict(resp.headers)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                reset = e.headers.get("X-RateLimit-Reset")
                remaining = e.headers.get("X-RateLimit-Remaining")
                if reset and remaining == "0":
                    wait = max(1, int(reset) - int(time.time())) + 1
                    print(f"  rate limited; sleeping {wait}s", file=sys.stderr)
                    time.sleep(min(wait, 900))
                    continue
                retry_after = e.headers.get("Retry-After")
                if retry_after:
                    time.sleep(int(retry_after) + 1)
                    continue
            if e.code >= 500 and attempt < 4:
                time.sleep(2 ** attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < 4:
                time.sleep(2 ** attempt)
                continue
            raise
    raise RuntimeError(f"exhausted retries for {url}")


def _paginate(url: str, params: dict[str, Any] | None = None) -> Iterator[dict]:
    """Yield each item across all pages of a list endpoint."""
    q = dict(params or {})
    q.setdefault("per_page", PAGE_SIZE)
    full = f"{url}?{urllib.parse.urlencode(q)}"
    while full:
        data, headers = _request(full)
        if isinstance(data, list):
            for item in data:
                yield item
        else:
            yield data
            return
        full = _next_link(headers.get("Link", ""))


_LINK_RE = re.compile(r'<([^>]+)>;\s*rel="([^"]+)"')


def _next_link(link_header: str) -> str | None:
    for url, rel in _LINK_RE.findall(link_header or ""):
        if rel == "next":
            return url
    return None


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

@dataclass
class SyncState:
    path: Path
    items: dict[str, dict[str, Any]]
    # ISO timestamp such that every item with updated_at <= high_water is
    # already represented on disk. Used as the GitHub `since=` query param
    # so subsequent syncs only pull genuinely-changed items.
    high_water: str = ""

    @classmethod
    def load(cls, path: Path) -> "SyncState":
        if path.exists():
            raw = json.loads(path.read_text())
            return cls(
                path=path,
                items=raw.get("items", {}),
                high_water=raw.get("high_water", ""),
            )
        return cls(path=path, items={})

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "items": self.items,
            "high_water": self.high_water,
            "last_run": _now_iso(),
        }
        self.path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    def should_fetch(self, key: str, updated_at: str) -> bool:
        existing = self.items.get(key)
        if not existing:
            return True
        return existing.get("updated_at", "") < updated_at

    def record(
        self, key: str, updated_at: str, filename: str, item_state: str
    ) -> None:
        self.items[key] = {
            "updated_at": updated_at,
            "filename": filename,
            "state": item_state,
        }


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def _fmt_user(user: dict | None) -> str:
    if not user:
        return "_ghost_"
    return f"[@{user.get('login', 'unknown')}]({user.get('html_url', '')})"


def _fmt_labels(labels: list[dict]) -> str:
    if not labels:
        return "_none_"
    return ", ".join(f"`{l['name']}`" for l in labels)


def _fmt_body(body: str | None) -> str:
    if not body:
        return "_(no description)_"
    return body.replace("\r\n", "\n").rstrip()


def _render_comment(c: dict) -> str:
    return (
        f"### Comment by {_fmt_user(c.get('user'))} — {c.get('created_at', '')}\n\n"
        f"{_fmt_body(c.get('body'))}\n"
    )


def _render_review(r: dict, inline_comments: list[dict]) -> str:
    state = r.get("state", "").lower()
    header = (
        f"### Review by {_fmt_user(r.get('user'))} "
        f"({state or 'commented'}) — {r.get('submitted_at', '') or r.get('created_at', '')}\n"
    )
    parts = [header]
    body = _fmt_body(r.get("body")) if r.get("body") else ""
    if body and body != "_(no description)_":
        parts.append(body + "\n")
    for ic in inline_comments:
        path = ic.get("path", "")
        line = ic.get("line") or ic.get("original_line") or ""
        diff_hunk = ic.get("diff_hunk", "")
        hunk_block = f"\n```diff\n{diff_hunk}\n```\n" if diff_hunk else ""
        body_md = _fmt_body(ic.get("body")).replace("\n", "\n  ")
        parts.append(
            f"- **{path}:{line}** by {_fmt_user(ic.get('user'))} — {ic.get('created_at', '')}"
            f"{hunk_block}\n"
            f"  {body_md}\n"
        )
    return "\n".join(parts)


def render_issue(issue: dict, comments: list[dict]) -> str:
    number = issue["number"]
    title = issue.get("title", "").strip()
    lines = [
        f"# Issue #{number}: {title}",
        "",
        f"**Summary**: {title}",
        "",
        f"**Sources**: {issue.get('html_url', '')}",
        "",
        f"**Last updated**: {issue.get('updated_at', '')}",
        "",
        "---",
        "",
        "## Metadata",
        "",
        f"- **State**: {issue.get('state', '')}"
        + (f" ({issue.get('state_reason')})" if issue.get("state_reason") else ""),
        f"- **Author**: {_fmt_user(issue.get('user'))}",
        f"- **Created**: {issue.get('created_at', '')}",
        f"- **Updated**: {issue.get('updated_at', '')}",
        f"- **Closed**: {issue.get('closed_at') or '—'}",
        f"- **Labels**: {_fmt_labels(issue.get('labels', []))}",
        f"- **Assignees**: "
        + (", ".join(_fmt_user(a) for a in issue.get("assignees", [])) or "_none_"),
        f"- **Comments**: {issue.get('comments', 0)}",
        "",
        "## Description",
        "",
        _fmt_body(issue.get("body")),
        "",
    ]
    if comments:
        lines += ["## Discussion", ""]
        for c in comments:
            lines.append(_render_comment(c))
    return "\n".join(lines).rstrip() + "\n"


def render_pr(
    pr: dict,
    comments: list[dict],
    reviews: list[dict],
    review_comments: list[dict],
) -> str:
    number = pr["number"]
    title = pr.get("title", "").strip()
    base = pr.get("base", {}).get("ref", "")
    head = pr.get("head", {}).get("ref", "")
    merged = pr.get("merged_at")

    by_review: dict[int, list[dict]] = {}
    orphan: list[dict] = []
    for rc in review_comments:
        rid = rc.get("pull_request_review_id")
        if rid:
            by_review.setdefault(rid, []).append(rc)
        else:
            orphan.append(rc)

    lines = [
        f"# PR #{number}: {title}",
        "",
        f"**Summary**: {title}",
        "",
        f"**Sources**: {pr.get('html_url', '')}",
        "",
        f"**Last updated**: {pr.get('updated_at', '')}",
        "",
        "---",
        "",
        "## Metadata",
        "",
        f"- **State**: {pr.get('state', '')}" + (" (merged)" if merged else ""),
        f"- **Author**: {_fmt_user(pr.get('user'))}",
        f"- **Branch**: `{head}` → `{base}`",
        f"- **Created**: {pr.get('created_at', '')}",
        f"- **Updated**: {pr.get('updated_at', '')}",
        f"- **Merged**: {merged or '—'}",
        f"- **Closed**: {pr.get('closed_at') or '—'}",
        f"- **Labels**: {_fmt_labels(pr.get('labels', []))}",
        f"- **Assignees**: "
        + (", ".join(_fmt_user(a) for a in pr.get("assignees", [])) or "_none_"),
        f"- **Requested reviewers**: "
        + (", ".join(_fmt_user(a) for a in pr.get("requested_reviewers", [])) or "_none_"),
        f"- **Changed files**: {pr.get('changed_files', '?')}   "
        f"**+{pr.get('additions', '?')} / -{pr.get('deletions', '?')}**",
        "",
        "## Description",
        "",
        _fmt_body(pr.get("body")),
        "",
    ]

    if comments:
        lines += ["## Discussion", ""]
        for c in comments:
            lines.append(_render_comment(c))

    if reviews or orphan:
        lines += ["## Reviews", ""]
        for r in reviews:
            rid = r.get("id")
            lines.append(_render_review(r, by_review.get(rid, [])))
        if orphan:
            lines.append("### Unlinked inline comments\n")
            for ic in orphan:
                path = ic.get("path", "")
                line = ic.get("line") or ic.get("original_line") or ""
                lines.append(
                    f"- **{path}:{line}** by {_fmt_user(ic.get('user'))} "
                    f"— {ic.get('created_at', '')}\n"
                    f"  {_fmt_body(ic.get('body'))}\n"
                )

    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Fetch logic
# ---------------------------------------------------------------------------

def fetch_issue_comments(repo: str, number: int) -> list[dict]:
    return list(_paginate(f"{API}/repos/{repo}/issues/{number}/comments"))


def fetch_pr_detail(repo: str, number: int) -> dict:
    data, _ = _request(f"{API}/repos/{repo}/pulls/{number}")
    return data


def fetch_pr_reviews(repo: str, number: int) -> list[dict]:
    return list(_paginate(f"{API}/repos/{repo}/pulls/{number}/reviews"))


def fetch_pr_review_comments(repo: str, number: int) -> list[dict]:
    return list(_paginate(f"{API}/repos/{repo}/pulls/{number}/comments"))


def sync(repo: str, output_root: Path, state_filter: str, max_items: int) -> None:
    owner, name = repo.split("/", 1)
    out_dir = output_root / f"{owner}__{name}"
    out_dir.mkdir(parents=True, exist_ok=True)
    state = SyncState.load(out_dir / ".sync-state.json")

    # Capture run start *before* any network I/O so we never advance
    # high_water past an item that was updated mid-sync.
    run_started = _now_iso()

    # The /issues endpoint returns both issues and PRs (PRs carry a
    # `pull_request` field). Sort by updated desc so the newest changes
    # are fetched first — plays well with MAX_ITEMS caps and lets us
    # bail out as soon as we hit an item we already have at the same
    # timestamp (everything older must be unchanged too).
    params = {"state": state_filter, "sort": "updated", "direction": "desc"}
    # `since` lets the server filter out anything we've definitely already
    # synced. Combined with `state=all`, this still surfaces items that were
    # closed/reopened since the last run because closing bumps updated_at.
    if state.high_water:
        params["since"] = state.high_water
        print(f"Incremental sync: fetching items updated since {state.high_water}")
    else:
        print("Full sync: no prior high-water mark")
    url = f"{API}/repos/{repo}/issues"

    processed = 0
    skipped = 0
    new_or_updated = 0
    cap_hit = False
    early_stop = False

    try:
        for item in _paginate(url, params):
            if max_items and processed >= max_items:
                cap_hit = True
                break
            processed += 1

            number = item["number"]
            updated_at = item.get("updated_at", "")
            is_pr = "pull_request" in item
            key = f"{'pr' if is_pr else 'issue'}-{number}"

            if not state.should_fetch(key, updated_at):
                skipped += 1
                # Sorted by updated desc: every remaining item is older
                # than this one, and we already have this one. Done.
                early_stop = True
                print(
                    f"Reached known-unchanged {key} (updated={updated_at}); "
                    "stopping early."
                )
                break

            print(f"[{processed}] {key} updated={updated_at} — fetching…")
            try:
                if is_pr:
                    pr = fetch_pr_detail(repo, number)
                    comments = fetch_issue_comments(repo, number)
                    reviews = fetch_pr_reviews(repo, number)
                    review_comments = fetch_pr_review_comments(repo, number)
                    md = render_pr(pr, comments, reviews, review_comments)
                else:
                    comments = fetch_issue_comments(repo, number)
                    md = render_issue(item, comments)
            except urllib.error.HTTPError as e:
                print(f"  skipped {key}: HTTP {e.code}", file=sys.stderr)
                continue

            filename = f"{key}.md"
            (out_dir / filename).write_text(md)
            state.record(key, updated_at, filename, item.get("state", ""))
            new_or_updated += 1

            if new_or_updated % 25 == 0:
                state.save()

        # Only advance high_water when we're certain we've seen every
        # item updated up to `run_started`. If a MAX_ITEMS cap interrupted
        # the listing, leave it untouched so the next run re-lists the
        # tail we missed.
        if not cap_hit:
            state.high_water = run_started
    finally:
        state.save()

    reason = (
        "exhausted listing" if not (cap_hit or early_stop)
        else "MAX_ITEMS cap" if cap_hit
        else "hit known-unchanged item"
    )
    print(
        f"\nDone ({reason}). scanned={processed} "
        f"new_or_updated={new_or_updated} skipped_unchanged={skipped} "
        f"total_tracked={len(state.items)} high_water={state.high_water or '—'}"
    )
    print(f"Output: {out_dir}")


def main() -> int:
    if "/" not in REPO:
        print(f"REPO must be 'owner/name'; got {REPO!r}", file=sys.stderr)
        return 2
    print(f"Syncing {REPO} (state={STATE}) -> {OUTPUT_ROOT}")
    if not (os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")):
        print(
            "No GITHUB_TOKEN set; using unauthenticated rate limit (60/hr).",
            file=sys.stderr,
        )
    sync(REPO, OUTPUT_ROOT, STATE, MAX_ITEMS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
