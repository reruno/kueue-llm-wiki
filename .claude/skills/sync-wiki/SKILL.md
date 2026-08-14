---
name: sync-wiki
description: Sync this wiki checkout with its upstream remote before reading or writing wiki pages. Use when the user asks to sync, update, pull, or refresh the wiki, when a wiki answer looks like it may be stale, or before an ingest run.
argument-hint: [--status|--force|--remote <name>]
allowed-tools: Bash(${CLAUDE_PROJECT_DIR}/sync_wiki.sh *)
---

Run `${CLAUDE_PROJECT_DIR}/sync_wiki.sh $ARGUMENTS` and tell the user what changed.

- Syncs from the sync branch's tracking remote and prints which one it used. Pass `--remote <name>`
  only when the user names a specific remote.
- Fast-forwards only when that branch is checked out and has no uncommitted tracked changes.
  Otherwise it reports the gap and leaves every file alone.
- Results are cached for 24h. `--force` re-checks the remote, `--status` reports without touching
  files.
- The script exits 0 on every path, so read its output rather than the exit code.

If it reports a skipped sync or a divergence, pass along the command it printed. Don't reach for your
own `git merge`, `git rebase`, or `git checkout` to force the sync through.

When it reports that `wiki/index.md` changed, re-read the index before answering from the wiki — page
names and descriptions may have moved.
