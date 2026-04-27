#!/usr/bin/env bash
# Wiki update pipeline for kueue-llm-wiki.
#
# Finds every [data-collection] commit that has not yet been analysed, then
# for each one calls Claude to read the new raw/ files and update wiki/ pages,
# and commits the result with prefix [wiki-update] commit=<hash>.
#
# "Not yet analysed" means: [data-collection] commits that appear in git log
# AFTER the most recent [wiki-update] commit (or all of them if no
# [wiki-update] commit exists yet).
#
# Usage:
#   ./gen_wiki.sh
#   ./gen_wiki.sh --model opus
#   ./gen_wiki.sh --dry-run
#   ./gen_wiki.sh --max-budget 2.00
#   ./gen_wiki.sh --effort high

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

MODEL="${MODEL:-sonnet}"
DRY_RUN=false
MAX_BUDGET="${MAX_BUDGET:-}"
EFFORT="${EFFORT:-}"

usage() {
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --model <model>          Claude model alias or ID (default: sonnet)"
    echo "  --max-budget <usd>       Maximum USD to spend per Claude call (e.g. 2.00)"
    echo "  --effort <level>         Thinking effort: low, medium, high, max (default: off)"
    echo "  --dry-run                Print what would be done without calling Claude"
    echo "  --help                   Show this message"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --model)       MODEL="$2";      shift 2 ;;
        --max-budget)  MAX_BUDGET="$2"; shift 2 ;;
        --effort)      EFFORT="$2";     shift 2 ;;
        --dry-run)     DRY_RUN=true;    shift   ;;
        --help|-h)     usage ;;
        *)             echo "Unknown argument: $1" >&2; usage ;;
    esac
done

cd "$REPO_ROOT"

# ---------------------------------------------------------------------------
# Resolve unprocessed [data-collection] commits
# ---------------------------------------------------------------------------

# Find the most recent [wiki-update] commit (if any).
LAST_WIKI_COMMIT="$(git log --format='%H' --grep='^\[wiki-update\]' -1 2>/dev/null || true)"

if [[ -z "$LAST_WIKI_COMMIT" ]]; then
    echo "No prior [wiki-update] commit found — will process all [data-collection] commits."
    # All data-collection commits, oldest first.
    mapfile -t DATA_COMMITS < <(git log --format='%H' --reverse --grep='^\[data-collection\]')
else
    echo "Last [wiki-update] commit: ${LAST_WIKI_COMMIT}"
    # Only commits that came after the last wiki-update, oldest first.
    mapfile -t DATA_COMMITS < <(git log --format='%H' --reverse --grep='^\[data-collection\]' "${LAST_WIKI_COMMIT}..HEAD")
fi

if [[ ${#DATA_COMMITS[@]} -eq 0 ]]; then
    echo "No new [data-collection] commits to analyse. Wiki is up to date."
    exit 0
fi

echo "Found ${#DATA_COMMITS[@]} unprocessed [data-collection] commit(s)."

# ---------------------------------------------------------------------------
# Process each commit
# ---------------------------------------------------------------------------

for DC_HASH in "${DATA_COMMITS[@]}"; do
    DC_MSG="$(git log -1 --format='%s' "$DC_HASH")"
    echo ""
    echo "==> Processing: ${DC_HASH} — ${DC_MSG}"

    # Collect new files added to raw/ in this commit (ignore state files).
    mapfile -t NEW_FILES < <(
        git diff-tree --no-commit-id -r --name-only --diff-filter=A "$DC_HASH" -- raw/ \
        | grep -v '\.sync-state\.json' \
        || true
    )

    if [[ ${#NEW_FILES[@]} -eq 0 ]]; then
        echo "    No new raw files in this commit — skipping."
        continue
    fi

    echo "    New raw files (${#NEW_FILES[@]}):"
    printf '      %s\n' "${NEW_FILES[@]}"

    # Build the file list for the prompt (newline-separated, repo-relative).
    FILE_LIST="$(printf '%s\n' "${NEW_FILES[@]}")"

    PROMPT="$(cat <<PROMPT
Wiki update task — data-collection commit ${DC_HASH}

The following files were just added to raw/ by a data-collection run:

${FILE_LIST}

Please carry out the wiki ingest workflow defined in CLAUDE.md.

## Goal

Build a wiki that is maximally useful for two purposes:
  (a) A developer actively contributing to or extending Kueue
  (b) An LLM assistant helping with Kueue development — the wiki is its primary context

Write with that reader in mind: precise, unambiguous, implementation-oriented.
Prefer concrete details (field names, controller names, reconcile logic, edge cases, error conditions)
over high-level summaries that could be inferred from a README.

## What to include

- Merged, shipped behaviour only. No proposals, KEPs, open issues, or planned work.
- Bug fixes that reveal non-obvious invariants or constraints (even if the fix itself is trivial).
- API fields with their semantics, defaults, and interaction effects.
- Controller/reconciler responsibilities and the sequence of operations they perform.
- Preemption, borrowing, and admission logic — the rules and their priority order.
- Known gotchas, subtle behaviours, and conditions that are easy to get wrong.
- Integration details: how Kueue interacts with each supported workload type (Job, JobSet, RayJob, etc.).

## What to exclude

- Proposals, KEPs, design docs, draft PRs, open issues, "we plan to", "will be added".
- Alpha/experimental features not yet in a stable release.
- Purely administrative content (CI fixes, test infra, release bookkeeping).
- Content that duplicates what is already in the wiki without adding new detail.

## Steps

1. Read each file listed above.
2. Identify what is genuinely new or clarifying relative to existing wiki pages.
3. Create or update wiki/ pages following the page format in CLAUDE.md.
   Favour depth on existing pages over creating many thin new pages.
4. Update wiki/index.md with any new pages.
5. Append ONE entry to wiki/log.md with:
   - date: $(date -u +%Y-%m-%d)
   - data-collection commit: ${DC_HASH}
   - source files analysed (list the files above)
   - wiki pages created or updated and a one-line summary of each change

Only write to wiki/ (never raw/). Do not create unnecessary pages for trivial changes.
PROMPT
)"

    if [[ "$DRY_RUN" == "true" ]]; then
        echo "    [dry-run] Would call Claude with the prompt above."
        echo "    [dry-run] Skipping commit step."
        continue
    fi

    # Build claude flags
    CLAUDE_ARGS=(
        --print
        --model "$MODEL"
        --allowedTools "Read,Edit(wiki/*),Write(wiki/*)"
        --permission-mode bypassPermissions
    )
    [[ -n "$MAX_BUDGET" ]] && CLAUDE_ARGS+=(--max-budget-usd "$MAX_BUDGET")
    [[ -n "$EFFORT" ]]     && CLAUDE_ARGS+=(--effort "$EFFORT")

    echo "    Calling Claude (model=${MODEL}, effort=${EFFORT:-off})..."
    claude "${CLAUDE_ARGS[@]}" --output-format stream-json --verbose "$PROMPT" \
        | jq -r '
            if .type == "assistant" then
                .message.content[]? |
                if .type == "thinking" and (.thinking | length) > 0 then "    [thinking] \(.thinking)"
                elif .type == "tool_use" then "    [tool] \(.name): \(.input | to_entries | map("\(.key)=\(.value|tostring)") | join(", "))"
                elif .type == "text" and (.text | length) > 0 then "    \(.text)"
                else empty end
            elif .type == "result" then "    [done] cost=\(.total_cost_usd // "?")"
            else empty end
        '

    # Stage wiki/ changes
    git add wiki/

    if git diff --cached --quiet; then
        echo "    Claude made no wiki changes for ${DC_HASH}."
        continue
    fi

    mapfile -t CHANGED_FILES < <(git diff --cached --name-only)
    echo "    Changed: ${CHANGED_FILES[*]}"

    PAGES_LIST="$(printf '  - %s\n' "${CHANGED_FILES[@]}")"
    COMMIT_MSG="[wiki-update] commit=${DC_HASH}"
    echo "    Committing: ${COMMIT_MSG}"

    git commit -m "$(cat <<EOF
${COMMIT_MSG}

Pages updated:
${PAGES_LIST}
EOF
)"

    echo "    Done."
done

echo ""
echo "==> Wiki update pipeline complete."
