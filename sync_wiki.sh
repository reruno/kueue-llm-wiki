#!/usr/bin/env bash
# Bring this wiki checkout up to date with its upstream remote.
# 1. Skips the whole check if it already ran within the TTL (default 24h)
# 2. Asks the remote for its branch tip with ls-remote (no object transfer)
# 3. Fast-forwards only when the sync branch is checked out and clean
# 4. Reports which wiki pages moved
#
# Called three ways: by hand, by the SessionStart hook in .claude/settings.json,
# and by the /sync-wiki skill. No remote name is hardcoded -- see "Resolve the
# remote" below -- so this works the same in any clone.
#
# Usage:
#   ./sync_wiki.sh                    sync if the remote has moved
#   ./sync_wiki.sh --status           report only, never touch the worktree
#   ./sync_wiki.sh --quiet            print nothing unless something changed
#   ./sync_wiki.sh --force            ignore the TTL and re-check the remote
#   ./sync_wiki.sh --remote epam      sync from a specific remote
#   WIKI_SYNC_REMOTE=epam ./sync_wiki.sh

# No `set -e`: the callers surface a non-zero exit as a failure, and the
# SessionStart hook sends stderr to a debug log the user never reads. A wiki
# that could not be synced should say why on stdout, not fail a session start,
# so every path reports what happened and returns 0. The trap covers
# unexpected failures too.
set -uo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REMOTE="${WIKI_SYNC_REMOTE:-}"
TTL="${WIKI_SYNC_TTL:-86400}"
QUIET=false
STATUS_ONLY=false
FORCE=false
JSON=false

# ---------------------------------------------------------------------------
# Output
#
# Buffered and emitted once, by the EXIT trap, because --json has to wrap the
# whole report in a single JSON object. The trap is installed before argument
# parsing so that even a bad argument leaves through the same door.
#
# report: always collected -- changes, warnings, anything actionable.
# note: informational, dropped by --quiet so a session start stays silent when
#   there is nothing to say.
# warn: one line addressed to the person, not to Claude. Under --json it
#   becomes systemMessage, which Claude Code shows to the user directly
#   instead of relying on Claude to pass it on.
# ---------------------------------------------------------------------------

OUT=()
WARN=""

report() { OUT+=("$*"); }
note() { [[ "$QUIET" == "true" ]] || OUT+=("$*"); }
warn() { WARN="$*"; }

flush() {
    local text=""
    if (( ${#OUT[@]} )); then
        text="$(printf '%s\n' "${OUT[@]}")"
    fi

    if [[ "$JSON" == "true" ]] && command -v python3 >/dev/null 2>&1; then
        [[ -z "$text" && -z "$WARN" ]] && exit 0
        python3 - "$text" "$WARN" <<'PY'
import json
import sys

context, warning = sys.argv[1], sys.argv[2]
payload = {}
if context:
    payload["hookSpecificOutput"] = {
        "hookEventName": "SessionStart",
        "additionalContext": context,
    }
if warning:
    payload["systemMessage"] = warning
print(json.dumps(payload))
PY
        exit 0
    fi

    # Plain text: by hand, from the /sync-wiki skill, or with no python3 to
    # build the JSON with. The warning is already part of the report.
    [[ -n "$text" ]] && printf '%s\n' "$text"
    exit 0
}
trap flush EXIT

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --status               Report the state only; never fetch or modify files"
    echo "  --quiet                Print nothing when the checkout is already current"
    echo "  --force                Ignore the TTL stamp and re-check the remote"
    echo "  --remote <name>        Remote to sync from (or set WIKI_SYNC_REMOTE)"
    echo "  --ttl <seconds>        Re-check window, default 86400 (or set WIKI_SYNC_TTL)"
    echo "  --json                 Emit SessionStart hook JSON instead of plain text"
    echo "  --help                 Show this message"
    # Exits 0 like every other path here, so a mistyped argument can never
    # break the caller.
    exit 0
}

# A bad argument under --json must not print the help text, or a misconfigured
# hook command would feed its own usage message into Claude's context. Tell the
# person instead, which is who can fix it.
bad_argument() {
    if [[ "$JSON" == "true" ]]; then
        warn "sync_wiki: $1. The wiki was not synced."
        exit 0
    fi
    echo "sync_wiki: $1" >&2
    usage
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --status)
            STATUS_ONLY=true
            shift
            ;;
        --quiet)
            QUIET=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        # `shift 2` on a lone flag fails without shifting, which spins the loop
        # forever, so check for the value before consuming it.
        --remote)
            [[ $# -ge 2 ]] || bad_argument "--remote needs a value"
            REMOTE="$2"
            shift 2
            ;;
        --ttl)
            [[ $# -ge 2 ]] || bad_argument "--ttl needs a value"
            TTL="$2"
            shift 2
            ;;
        --json)
            JSON=true
            shift
            ;;
        --help|-h)
            usage
            ;;
        *)
            bad_argument "unknown argument: $1"
            ;;
    esac
done

if ! GIT_DIR="$(git -C "$REPO_ROOT" rev-parse --git-dir 2>/dev/null)"; then
    report "sync_wiki: $REPO_ROOT is not a git checkout; skipping sync."
    exit 0
fi
case "$GIT_DIR" in
    /*) ;;
    *) GIT_DIR="$REPO_ROOT/$GIT_DIR" ;;
esac

git_r() { git -C "$REPO_ROOT" "$@"; }

# ---------------------------------------------------------------------------
# Resolve the branch and remote to sync from
#
# Nothing is hardcoded: this script is shared across clones that use different
# remote names (a fork, an upstream, an internal mirror). The branch is
# resolved first so the remote can be read from that branch's own tracking
# config, which is what makes the zero-configuration case correct.
# ---------------------------------------------------------------------------

CURRENT_BRANCH="$(git_r symbolic-ref --short -q HEAD)"

BRANCH="$(git_r config --get wiki.syncBranch)"
if [[ -z "$BRANCH" ]]; then
    for candidate in main master; do
        if git_r show-ref --verify --quiet "refs/heads/$candidate"; then
            BRANCH="$candidate"
            break
        fi
    done
fi
BRANCH="${BRANCH:-$CURRENT_BRANCH}"

if [[ -z "$BRANCH" ]]; then
    report "sync_wiki: cannot tell which branch to sync (detached HEAD, no main/master); skipping."
    exit 0
fi

if [[ -z "$REMOTE" ]]; then
    REMOTE="$(git_r config --get wiki.syncRemote)"
fi
if [[ -z "$REMOTE" ]]; then
    REMOTE="$(git_r config --get "branch.$BRANCH.remote")"
fi
REMOTE="${REMOTE:-origin}"

if ! git_r config --get "remote.$REMOTE.url" >/dev/null; then
    report "sync_wiki: no remote named '$REMOTE' in this checkout; skipping sync."
    report "  Set one with: git config wiki.syncRemote <name>"
    warn "Wiki not synced: no remote named '$REMOTE'. Set one with: git config wiki.syncRemote <name>"
    exit 0
fi

# ---------------------------------------------------------------------------
# TTL gate
#
# The wiki changes about once a fortnight, so one check a day is plenty. The
# stamp lives in .git/ to stay per-clone and out of the working tree, which
# means there is nothing to add to .gitignore.
# ---------------------------------------------------------------------------

STAMP="$GIT_DIR/wiki-sync-stamp"

file_mtime() {
    # BSD stat (macOS) first, then GNU stat (Linux).
    stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null
}

if [[ "$FORCE" != "true" && "$STATUS_ONLY" != "true" && -f "$STAMP" ]]; then
    stamped="$(file_mtime "$STAMP")"
    if [[ -n "$stamped" ]] && (( $(date +%s) - stamped < TTL )); then
        exit 0
    fi
fi

# ---------------------------------------------------------------------------
# Ask the remote where its branch is
#
# ls-remote is one round trip that transfers no objects, so it is safe to run
# on every session start. A real fetch only happens once it reports a tip we
# do not have.
# ---------------------------------------------------------------------------

if ! ls_remote_out="$(git_r ls-remote --heads "$REMOTE" "$BRANCH" 2>&1)"; then
    report "sync_wiki: cannot reach remote '$REMOTE'; keeping the current checkout."
    report "  ${ls_remote_out}"
    warn "Wiki not synced: remote '$REMOTE' is unreachable. Wiki pages may be stale."
    exit 0
fi

REMOTE_SHA="$(printf '%s\n' "$ls_remote_out" | awk 'NR==1 {print $1}')"
if [[ -z "$REMOTE_SHA" ]]; then
    report "sync_wiki: remote '$REMOTE' has no branch '$BRANCH'; skipping sync."
    exit 0
fi

LOCAL_SHA="$(git_r rev-parse -q --verify "refs/heads/$BRANCH")"

# We have the remote commit already if a previous fetch brought it in, in which
# case the relationship can be described without touching the network again.
have_remote_commit() { git_r cat-file -e "${REMOTE_SHA}^{commit}" 2>/dev/null; }

describe_gap() {
    if have_remote_commit; then
        local counts
        counts="$(git_r rev-list --left-right --count "$LOCAL_SHA...$REMOTE_SHA" 2>/dev/null)"
        report "$REMOTE/$BRANCH is at $(git_r rev-parse --short "$REMOTE_SHA"), local $BRANCH at $(git_r rev-parse --short "$LOCAL_SHA") (ahead/behind: ${counts//$'\t'//})."
    else
        report "$REMOTE/$BRANCH is at ${REMOTE_SHA:0:9}, local $BRANCH at $(git_r rev-parse --short "$LOCAL_SHA")."
    fi
}

# Checked before the up-to-date shortcut and before --status: if you're not on
# the sync branch, the files on disk are not what LOCAL_SHA describes, so
# comparing LOCAL_SHA to REMOTE_SHA below would be a claim about a ref nobody
# is looking at. Applies to --status too, so it doesn't report "up to date" or
# "run to fast-forward" for a branch that isn't even checked out.
if [[ "$CURRENT_BRANCH" != "$BRANCH" ]]; then
    describe_gap
    report "Not syncing: on branch '${CURRENT_BRANCH:-detached HEAD}', not '$BRANCH'. Wiki pages may be stale."
    report "  To sync: git switch $BRANCH && ./sync_wiki.sh"
    warn "Wiki not synced: on branch '${CURRENT_BRANCH:-detached HEAD}', not '$BRANCH'. Wiki pages may be stale. To sync: git switch $BRANCH && ./sync_wiki.sh"
    exit 0
fi

# The stamp is only set once the checkout is actually current. Stamping a
# skipped sync -- a dirty tree, a divergence -- would silence the warning for
# the next 24h and leave the wiki quietly stale, which is the failure this
# script exists to prevent. One extra ls-remote per session is the cheaper
# trade. --status must not stamp either: it promises never to modify files.
if [[ "$LOCAL_SHA" == "$REMOTE_SHA" ]]; then
    [[ "$STATUS_ONLY" == "true" ]] || touch "$STAMP" 2>/dev/null
    note "Wiki is up to date with $REMOTE/$BRANCH ($(git_r rev-parse --short "$LOCAL_SHA"))."
    exit 0
fi

if [[ "$STATUS_ONLY" == "true" ]]; then
    describe_gap
    report "Run ./sync_wiki.sh to fast-forward."
    exit 0
fi

# ---------------------------------------------------------------------------
# Guards -- never touch the working tree unless the fast-forward is trivial
#
# Only tracked changes matter: untracked files cannot block a fast-forward,
# and this repo commonly has untracked editor state lying around.
# ---------------------------------------------------------------------------

if ! git_r diff --quiet HEAD -- 2>/dev/null; then
    describe_gap
    report "Not syncing: you have uncommitted changes to tracked files. Wiki pages may be stale."
    report "  To sync: commit or stash them, then ./sync_wiki.sh"
    warn "Wiki not synced: uncommitted changes to tracked files. Wiki pages may be stale. Commit or stash, then ./sync_wiki.sh"
    exit 0
fi

# ---------------------------------------------------------------------------
# Fetch and fast-forward
#
# --no-tags and --no-recurse-submodules keep this to the one branch we asked
# about; raw/kueue is a submodule that is often not checked out at all, and
# updating it would be a large surprise download.
# ---------------------------------------------------------------------------

if ! fetch_out="$(git_r fetch --no-tags --no-recurse-submodules "$REMOTE" "$BRANCH" 2>&1)"; then
    report "sync_wiki: fetch from $REMOTE failed; keeping the current checkout."
    report "  ${fetch_out}"
    warn "Wiki not synced: fetch from '$REMOTE' failed. Wiki pages may be stale."
    exit 0
fi

OLD_SHA="$LOCAL_SHA"

if git_r merge-base --is-ancestor "$REMOTE_SHA" HEAD; then
    describe_gap
    # Deliberately no "git push" suggestion: where these commits should go
    # depends on the clone's remote layout, and the sync remote may well be
    # one nobody pushes to directly.
    report "Local $BRANCH is ahead of $REMOTE/$BRANCH; nothing to sync."
    exit 0
fi

if ! git_r merge-base --is-ancestor HEAD "$REMOTE_SHA"; then
    describe_gap
    report "Not syncing: local $BRANCH and $REMOTE/$BRANCH have diverged."
    report "  To reconcile: git rebase $REMOTE/$BRANCH"
    warn "Wiki not synced: $BRANCH and $REMOTE/$BRANCH have diverged. To reconcile: git rebase $REMOTE/$BRANCH"
    exit 0
fi

if ! merge_out="$(git_r merge --ff-only "$REMOTE_SHA" 2>&1)"; then
    report "sync_wiki: fast-forward to $REMOTE/$BRANCH failed; the checkout is unchanged."
    report "  ${merge_out}"
    warn "Wiki not synced: fast-forward to $REMOTE/$BRANCH failed. Wiki pages may be stale."
    exit 0
fi

# ---------------------------------------------------------------------------
# Report what moved
# ---------------------------------------------------------------------------

touch "$STAMP" 2>/dev/null

report "Synced $BRANCH from $REMOTE: $(git_r rev-parse --short "$OLD_SHA") -> $(git_r rev-parse --short HEAD)"

wiki_changed="$(git_r diff --name-only "$OLD_SHA..HEAD" -- wiki/)"
raw_count="$(git_r diff --name-only "$OLD_SHA..HEAD" -- raw/ | grep -c . || true)"

if [[ -n "$wiki_changed" ]]; then
    wiki_count="$(printf '%s\n' "$wiki_changed" | grep -c .)"
    report "  ${wiki_count} wiki page(s) changed:"
    while IFS= read -r page; do
        [[ -n "$page" ]] && report "    $page"
    done < <(printf '%s\n' "$wiki_changed" | head -n 15)
    if (( wiki_count > 15 )); then
        report "    ... and $(( wiki_count - 15 )) more"
    fi
    if printf '%s\n' "$wiki_changed" | grep -qx 'wiki/index.md'; then
        report "  wiki/index.md changed -- re-read it before answering from the wiki."
    fi
    warn "Wiki synced from $REMOTE: ${wiki_count} page(s) updated."
else
    report "  No wiki pages changed."
    warn "Wiki synced from $REMOTE: no page changes."
fi

if (( raw_count > 0 )); then
    report "  ${raw_count} file(s) changed under raw/."
fi

if [[ -n "$(git_r diff --name-only "$OLD_SHA..HEAD" -- raw/kueue)" ]]; then
    report "  The raw/kueue submodule pointer moved. To follow it:"
    report "    git submodule update --init --recursive raw/kueue"
fi

exit 0
