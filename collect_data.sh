#!/usr/bin/env bash
# Data collection pipeline for kueue-llm-wiki.
# 1. Runs collect_gh.py to sync GitHub issues/PRs into raw/github/
# 2. Updates the raw/kueue submodule to latest main
# 3. Runs collect_cve.py to fetch ecosystem CVEs into raw/cve/
# 4. Commits all changes with prefix [data-collection]
#
# Usage:
#   ./collect_data.sh --token <github-token>
#   ./collect_data.sh --token <github-token> --max-items 50
#   GITHUB_TOKEN=ghp_xxx ./collect_data.sh
#   NVD_API_KEY=xxx ./collect_data.sh          (higher NVD rate limit)
#   SKIP_CVE=true ./collect_data.sh            (skip CVE collection)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ---------------------------------------------------------------------------
# Load .env (shell-level, so env vars are available to the script itself)
# Python scripts do their own _load_dotenv(); this covers bash-level vars
# like GITHUB_TOKEN that the script checks before invoking Python.
# ---------------------------------------------------------------------------

if [[ -f "$REPO_ROOT/.env" ]]; then
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip blanks and comments
        [[ -z "$line" || "$line" == \#* ]] && continue
        [[ "$line" != *"="* ]] && continue
        key="${line%%=*}"
        value="${line#*=}"
        # Strip surrounding quotes
        value="${value%\"}"
        value="${value#\"}"
        value="${value%\'}"
        value="${value#\'}"
        # Only set if not already in environment
        if [[ -z "${!key+x}" ]]; then
            export "$key"="$value"
        fi
    done < "$REPO_ROOT/.env"
fi

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

GH_TOKEN="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
MAX_ITEMS="${MAX_ITEMS:-0}"
REPO="${REPO:-kubernetes-sigs/kueue}"
STATE="${STATE:-all}"
SKIP_SUBMODULE="${SKIP_SUBMODULE:-false}"
SKIP_CVE="${SKIP_CVE:-false}"
NVD_API_KEY="${NVD_API_KEY:-}"
CVE_SINCE="${CVE_SINCE:-2019-01-01}"
CVE_MAX_PAGES="${CVE_MAX_PAGES:-0}"

usage() {
    echo "Usage: $0 --token <github-token> [options]"
    echo ""
    echo "Options:"
    echo "  --token <token>        GitHub personal access token (or set GITHUB_TOKEN env var)"
    echo "  --max-items <n>        Cap items per run (default: 0 = unlimited)"
    echo "  --repo <owner/name>    GitHub repo to sync (default: kubernetes-sigs/kueue)"
    echo "  --state <all|open|closed>  Issue/PR state filter (default: all)"
    echo "  --skip-submodule       Skip updating the raw/kueue submodule"
    echo "  --skip-cve             Skip CVE collection step"
    echo "  --nvd-key <key>        NVD API key (or set NVD_API_KEY env var)"
    echo "  --cve-since <date>     Only fetch CVEs published after this date (default: 2019-01-01)"
    echo "  --cve-max-pages <n>    Cap CVE pages per keyword (0 = unlimited)"
    echo "  --help                 Show this message"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --token)
            GH_TOKEN="$2"
            shift 2
            ;;
        --max-items)
            MAX_ITEMS="$2"
            shift 2
            ;;
        --repo)
            REPO="$2"
            shift 2
            ;;
        --state)
            STATE="$2"
            shift 2
            ;;
        --skip-submodule)
            SKIP_SUBMODULE=true
            shift
            ;;
        --skip-cve)
            SKIP_CVE=true
            shift
            ;;
        --nvd-key)
            NVD_API_KEY="$2"
            shift 2
            ;;
        --cve-since)
            CVE_SINCE="$2"
            shift 2
            ;;
        --cve-max-pages)
            CVE_MAX_PAGES="$2"
            shift 2
            ;;
        --help|-h)
            usage
            ;;
        *)
            echo "Unknown argument: $1" >&2
            usage
            ;;
    esac
done

if [[ -z "$GH_TOKEN" ]]; then
    echo "Warning: no GitHub token provided; unauthenticated rate limit applies (60 req/hr)." >&2
    echo "Pass --token <token> or set GITHUB_TOKEN in the environment." >&2
fi

cd "$REPO_ROOT"

# ---------------------------------------------------------------------------
# Step 1: Sync GitHub issues and PRs
# ---------------------------------------------------------------------------

echo "==> Syncing GitHub issues/PRs for ${REPO}..."

GITHUB_TOKEN="$GH_TOKEN" \
REPO="$REPO" \
STATE="$STATE" \
MAX_ITEMS="$MAX_ITEMS" \
python3 collect_gh.py

echo "==> GitHub sync complete."

# ---------------------------------------------------------------------------
# Step 2: Update raw/kueue submodule to latest main
# ---------------------------------------------------------------------------

if [[ "$SKIP_SUBMODULE" == "false" ]]; then
    echo "==> Updating raw/kueue submodule..."

    if [[ ! -f "raw/kueue/.git" ]] && [[ ! -d "raw/kueue/.git" ]]; then
        echo "    Initializing submodule for the first time..."
        git submodule update --init --recursive raw/kueue
    fi

    git -C raw/kueue fetch origin main
    git -C raw/kueue checkout main
    git -C raw/kueue pull --ff-only origin main

    echo "==> Submodule updated to: $(git -C raw/kueue rev-parse --short HEAD)"
else
    echo "==> Skipping submodule update (--skip-submodule)."
fi

# ---------------------------------------------------------------------------
# Step 3: Fetch ecosystem CVEs from NVD into raw/cve/
# ---------------------------------------------------------------------------

if [[ "$SKIP_CVE" == "false" ]]; then
    echo "==> Fetching CVEs from NVD (since ${CVE_SINCE})..."

    NVD_API_KEY="$NVD_API_KEY" \
    CVE_OUTPUT="raw/cve" \
    CVE_SINCE="$CVE_SINCE" \
    CVE_MAX_PAGES="$CVE_MAX_PAGES" \
    python3 collect_cve.py

    echo "==> CVE collection complete."
else
    echo "==> Skipping CVE collection (--skip-cve)."
fi

# ---------------------------------------------------------------------------
# Step 4: Commit all changes
# ---------------------------------------------------------------------------

echo "==> Checking for changes to commit..."

git add raw/

if git diff --cached --quiet; then
    echo "==> No changes to commit."
    exit 0
fi

# Build a commit message summarising what changed
CHANGED_FILES="$(git diff --cached --name-only)"
NEW_FILES="$(git diff --cached --name-only --diff-filter=A | grep -v '\.sync-state\.json' || true)"
UPDATED_FILES="$(git diff --cached --name-only --diff-filter=M | grep -v '\.sync-state\.json' || true)"

NEW_COUNT="$(echo "$NEW_FILES" | grep -c '\S' || true)"
UPDATED_COUNT="$(echo "$UPDATED_FILES" | grep -c '\S' || true)"

SUMMARY_PARTS=()
[[ "$NEW_COUNT" -gt 0 ]]     && SUMMARY_PARTS+=("${NEW_COUNT} new")
[[ "$UPDATED_COUNT" -gt 0 ]] && SUMMARY_PARTS+=("${UPDATED_COUNT} updated")

if [[ "${#SUMMARY_PARTS[@]}" -gt 0 ]]; then
    ITEM_SUMMARY="$(IFS=", "; echo "${SUMMARY_PARTS[*]}") items from ${REPO}"
else
    ITEM_SUMMARY="sync-state and submodule pointer"
fi

SUBMODULE_NOTE=""
if [[ "$SKIP_SUBMODULE" == "false" ]] && echo "$CHANGED_FILES" | grep -q "raw/kueue"; then
    SUBMODULE_SHA="$(git -C raw/kueue rev-parse --short HEAD)"
    SUBMODULE_NOTE=", kueue@${SUBMODULE_SHA}"
fi

COMMIT_MSG="[data-collection] ${ITEM_SUMMARY}${SUBMODULE_NOTE}"

echo "==> Committing: ${COMMIT_MSG}"

git commit -m "$(cat <<EOF
${COMMIT_MSG}
EOF
)"

echo "==> Done. Committed data collection run."
