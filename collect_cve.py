#!/usr/bin/env python3
"""
Download CVEs from the NVD API v2.0 for Kueue's ecosystem and related
batch/job-queue projects, writing one Markdown file per CVE into raw/cve/.

Each file is structured to be maximally useful for training a security
evaluation domain (security.md) inside the code-eval skill.  The fields
captured go beyond the raw NVD data: attack category, root-cause class,
Go/Kubernetes-specific code patterns, and mitigation guidance are derived
from the CVE description and CVSS vector.

NVD API docs: https://nvd.nist.gov/developers/vulnerabilities
Rate limits  : 5 requests/30 s unauthenticated · 50 requests/30 s with key

Configuration (env vars):
  NVD_API_KEY   -- optional, raises rate limit
  CVE_OUTPUT    -- output directory (default: raw/cve)
  CVE_MAX_PAGES -- max pages per keyword (0 = unlimited, default: 0)
  CVE_SINCE     -- only fetch CVEs published after this date (YYYY-MM-DD),
                   default: 2019-01-01 (covers modern Kubernetes era)

Usage:
  python3 collect_cve.py
  NVD_API_KEY=xxxx CVE_SINCE=2022-01-01 python3 collect_cve.py
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def _load_dotenv() -> None:
    """Load KEY=VALUE pairs from .env in the script's directory into os.environ.

    Existing env vars are never overwritten — shell/CLI values always win.
    Supports inline comments (#), quoted values, and blank lines.
    """
    env_path = Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, raw = line.partition("=")
        key = key.strip()
        value = raw.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_dotenv()

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

NVD_API_KEY: str = os.environ.get("NVD_API_KEY", "")
OUTPUT_DIR: Path = Path(os.environ.get("CVE_OUTPUT", "raw/cve"))
MAX_PAGES: int = int(os.environ.get("CVE_MAX_PAGES", "0"))
CVE_SINCE: str = os.environ.get("CVE_SINCE", "2019-01-01")

NVD_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"
RESULTS_PER_PAGE = 100
REQUEST_DELAY = 7.0   # seconds between requests (unauthenticated: 5 req/30s)
AUTH_DELAY = 0.7      # seconds when authenticated

# ---------------------------------------------------------------------------
# Keyword groups: each entry is (label, keywords_to_try).
# We search each keyword independently to maximise recall.
# ---------------------------------------------------------------------------

SEARCH_TARGETS: list[tuple[str, list[str]]] = [
    # Kueue itself (no CVEs yet; kept for future tracking)
    ("kueue",               ["kueue"]),
    # Core Kubernetes — broad keyword covers scheduler, apiserver, kubelet, etc.
    ("kubernetes",          ["kubernetes"]),
    # Infrastructure components used by Kueue clusters
    ("etcd",                ["etcd"]),
    ("containerd",          ["containerd"]),
    ("runc",                ["runc"]),
    # Related batch / job-queue orchestration in the same ecosystem
    ("argo-workflows",      ["argo workflows"]),
    # Specific vulnerability classes common in Kubernetes controllers/operators
    ("kubernetes-privilege", ["kubernetes privilege escalation"]),
    ("kubernetes-dos",       ["kubernetes denial of service"]),
    ("kubernetes-rbac",      ["kubernetes RBAC"]),
]

# ---------------------------------------------------------------------------
# Severity helpers
# ---------------------------------------------------------------------------

CVSS_SEVERITY_MAP = {
    "CRITICAL": "Critical",
    "HIGH":     "High",
    "MEDIUM":   "Medium",
    "LOW":      "Low",
    "NONE":     "None",
}

# Map CVSS attack vector codes → human-readable labels
AV_LABELS = {"N": "Network", "A": "Adjacent", "L": "Local", "P": "Physical"}
AC_LABELS = {"L": "Low", "H": "High"}
PR_LABELS = {"N": "None", "L": "Low", "H": "High"}
UI_LABELS = {"N": "None", "R": "Required"}
S_LABELS  = {"U": "Unchanged", "C": "Changed"}
C_LABELS  = {"N": "None", "L": "Low", "H": "High"}


def parse_cvss_vector(vector: str) -> dict[str, str]:
    """Return a human-readable breakdown of a CVSS v3 vector string."""
    parts: dict[str, str] = {}
    for segment in vector.split("/"):
        if ":" not in segment:
            continue
        k, v = segment.split(":", 1)
        parts[k] = v
    return parts


def cvss_to_human(vector: str) -> str:
    """One-line English summary of a CVSS v3 vector."""
    p = parse_cvss_vector(vector)
    av = AV_LABELS.get(p.get("AV", ""), p.get("AV", "?"))
    ac = AC_LABELS.get(p.get("AC", ""), p.get("AC", "?"))
    pr = PR_LABELS.get(p.get("PR", ""), p.get("PR", "?"))
    ui = UI_LABELS.get(p.get("UI", ""), p.get("UI", "?"))
    ci = C_LABELS.get(p.get("C", ""),  p.get("C", "?"))
    ii = C_LABELS.get(p.get("I", ""),  p.get("I", "?"))
    ai = C_LABELS.get(p.get("A", ""),  p.get("A", "?"))
    return (
        f"Attack vector: {av}, complexity: {ac}, privileges required: {pr}, "
        f"user interaction: {ui} | Impact — C:{ci} I:{ii} A:{ai}"
    )


# ---------------------------------------------------------------------------
# Category inference from description + vector
# ---------------------------------------------------------------------------

_CATEGORY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Privilege Escalation",   re.compile(r"privilege.escal|elevat.*(privilege|permiss)|escalat.*access", re.I)),
    ("Authentication Bypass",  re.compile(r"bypass.*(auth|verif|check)|auth.*bypass|unauthenticated access", re.I)),
    ("Denial of Service",      re.compile(r"denial.of.service|resource.exhaustion|infinite loop|crash|OOM|memory.leak|cpu.exhaust", re.I)),
    ("Information Disclosure", re.compile(r"information.disclos|secret.*expos|sensitive.*data|credential.*leak|token.*leak", re.I)),
    ("Code Execution",         re.compile(r"remote.code.exec|arbitrary.command|RCE|command.inject", re.I)),
    ("Injection",              re.compile(r"inject|SSRF|server.side.request", re.I)),
    ("Path Traversal",         re.compile(r"path.traversal|directory.traversal|\.\.\/", re.I)),
    ("RBAC Misconfiguration",  re.compile(r"RBAC|role.binding|cluster.?role|over.permiss|excess.*permiss", re.I)),
    ("Supply Chain",           re.compile(r"supply.chain|image.pull|registry|checksum|signature", re.I)),
]


def infer_category(description: str, vector: str) -> str:
    for label, pat in _CATEGORY_PATTERNS:
        if pat.search(description):
            return label
    # Fall back to CVSS impact fields
    p = parse_cvss_vector(vector)
    if p.get("I") == "H" and p.get("PR") == "N":
        return "Unauthorized Write Access"
    if p.get("C") == "H":
        return "Information Disclosure"
    if p.get("A") == "H":
        return "Denial of Service"
    return "Other"


# ---------------------------------------------------------------------------
# Root-cause inference
# ---------------------------------------------------------------------------

_ROOT_CAUSE_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Missing input validation",       re.compile(r"insuffici.*validat|fail.*validat|lack.*sanitiz|not.*sanit", re.I)),
    ("Improper access control",        re.compile(r"improper.access|missing.authoriz|lack.*access.control|no.*permission.check", re.I)),
    ("Missing resource limits",        re.compile(r"no.limit|unbounded|resource.quota|rate.limit|throttl", re.I)),
    ("Race condition",                 re.compile(r"race.condition|TOCTOU|time.of.check|concurrent", re.I)),
    ("Insecure default configuration", re.compile(r"default.*insecure|misconfigur|default.*allow|world.readable", re.I)),
    ("Credential exposure",            re.compile(r"hardcoded|plaintext.*credential|secret.*log|token.*log|password.*log", re.I)),
    ("Unsafe deserialization",         re.compile(r"deserializ|unmarshal.*untrusted|yaml.*exec|json.*inject", re.I)),
    ("Insufficient privilege separation", re.compile(r"privilege.*sep|least.privil|over.permiss|cluster.admin", re.I)),
    ("Missing TLS/mTLS",               re.compile(r"plaintext|unencrypted|missing.TLS|no.TLS|insecure.*transport", re.I)),
    ("Path traversal / symlink",       re.compile(r"path.traversal|symlink|\.\.\/", re.I)),
]


def infer_root_cause(description: str) -> str:
    for label, pat in _ROOT_CAUSE_PATTERNS:
        if pat.search(description):
            return label
    return "See description"


# ---------------------------------------------------------------------------
# Code pattern hints for the security.md domain
# ---------------------------------------------------------------------------

_CODE_PATTERN_HINTS: dict[str, list[str]] = {
    "Privilege Escalation": [
        "Functions that mutate ServiceAccount tokens or pod security contexts",
        "Missing `securityContext.runAsNonRoot` or `allowPrivilegeEscalation: false`",
        "HostPID / HostNetwork / HostIPC set to `true`",
        "Volumes that mount sensitive host paths (e.g. `/etc/kubernetes`, `/var/run/docker.sock`)",
    ],
    "Authentication Bypass": [
        "Webhook handlers that skip token validation on certain HTTP methods",
        "Missing `SubjectAccessReview` calls before privileged operations",
        "Trusting `X-Forwarded-For` or `X-Remote-User` headers without validation",
        "Admission webhooks with `failurePolicy: Ignore`",
    ],
    "Denial of Service": [
        "Unbounded loops iterating over user-supplied input",
        "Missing context timeouts (`context.WithTimeout`) on API calls",
        "Large allocations proportional to untrusted user input",
        "Missing `LimitRanger` or `ResourceQuota` enforcement before admit",
        "Workloads admitted without CPU/memory limits set",
    ],
    "Information Disclosure": [
        "Logging objects that may contain secrets (tokens, passwords, keys)",
        "Error responses that include internal stack traces",
        "Listing secrets across namespaces with a ClusterRole",
        "Storing sensitive values in annotations or labels (readable by all tenants)",
    ],
    "Code Execution": [
        "Executing user-supplied strings via `exec.Command` without allowlist",
        "Template injection in labels/annotations rendered server-side",
    ],
    "Injection": [
        "Building API server URLs from user-controlled namespace/name fields",
        "SSRF via container image URLs or init-container pull specs",
        "Using `fmt.Sprintf` to construct YAML/JSON payloads",
    ],
    "RBAC Misconfiguration": [
        "ClusterRoles with wildcard verbs (`*`) or resources (`*`)",
        "Roles binding `cluster-admin` to service accounts used by controllers",
        "Missing namespace scoping — using ClusterRoleBinding where RoleBinding suffices",
        "Kueue controller ServiceAccount with `get/list/watch` on Secrets cluster-wide",
    ],
    "Missing resource limits": [
        "Admission paths that allow workloads with no resource requests/limits",
        "Missing rate limiting on webhook endpoints",
        "Queues or controllers processing items without back-pressure",
    ],
    "Race condition": [
        "Non-atomic read-modify-write on shared Kubernetes objects (use optimistic locking / resourceVersion)",
        "Cache reads without re-validation before admission",
        "Workload status transitions not guarded by status conditions",
    ],
    "Supply Chain": [
        "Image references without digest pinning (`image: foo:latest`)",
        "Missing image signature verification before admission",
    ],
}


def code_pattern_hints(category: str) -> list[str]:
    return _CODE_PATTERN_HINTS.get(category, [
        "Review related code paths for the vulnerability class described above.",
    ])


# ---------------------------------------------------------------------------
# Fix patch extraction
# ---------------------------------------------------------------------------

# Regex to detect GitHub commit URLs in CVE references
_GH_COMMIT_RE = re.compile(
    r"https?://github\.com/([^/]+/[^/]+)/commit/([0-9a-f]{7,40})",
    re.I,
)
MAX_PATCH_BYTES = 8_000  # keep diffs compact; trim if larger


def fetch_fix_patch(refs: list[dict[str, Any]]) -> str | None:
    """Fetch the fix diff from references, prioritising Patch-tagged ones.

    Tries GitHub commit URLs (.diff endpoint). Patch-tagged refs are tried
    first; all others are tried as fallback. Returns a diff string (possibly
    truncated), or None if nothing usable is found.
    """
    patch_refs = [r for r in refs if "Patch" in r.get("tags", [])]
    other_refs = [r for r in refs if "Patch" not in r.get("tags", [])]

    for ref in patch_refs + other_refs:
        url = ref.get("url", "")
        m = _GH_COMMIT_RE.search(url)
        if not m:
            continue
        diff_url = f"https://github.com/{m.group(1)}/commit/{m.group(2)}.diff"
        try:
            req = Request(
                diff_url,
                headers={"User-Agent": "kueue-llm-wiki-cve-collect", "Accept": "text/plain"},
            )
            with urlopen(req, timeout=20) as resp:
                raw = resp.read(MAX_PATCH_BYTES + 1).decode("utf-8", errors="replace")
            truncated = len(raw) > MAX_PATCH_BYTES
            patch = raw[:MAX_PATCH_BYTES]
            if truncated:
                patch += "\n… (diff truncated)"
            return patch
        except Exception:
            continue
    return None


# ---------------------------------------------------------------------------
# NVD API helpers
# ---------------------------------------------------------------------------

def _request_delay() -> float:
    return AUTH_DELAY if NVD_API_KEY else REQUEST_DELAY


def nvd_get(params: dict[str, str]) -> dict[str, Any]:
    """Execute one NVD API request, honouring rate limits and retrying 403s."""
    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{NVD_BASE}?{query}"
    headers: dict[str, str] = {"Accept": "application/json"}
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY

    for attempt in range(3):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except HTTPError as exc:
            if exc.code == 403:
                wait = 35 * (attempt + 1)
                print(f"    [rate-limit] 403 received, waiting {wait}s …", flush=True)
                time.sleep(wait)
            elif exc.code == 404:
                return {}
            else:
                raise
    raise RuntimeError(f"NVD API request failed after retries: {url}")


def fetch_cves(keyword: str, since: str) -> list[dict[str, Any]]:
    """Fetch CVEs matching keyword, filtering client-side to those published after 'since'.

    The NVD v2 API does not support server-side date range filtering via
    pubStartDate/pubEndDate when combined with keywordSearch (returns 404).
    We paginate without date params and skip CVEs whose `published` field
    predates `since`.
    """
    since_dt = since[:10]  # YYYY-MM-DD for prefix comparison

    results: list[dict[str, Any]] = []
    start_index = 0
    page = 0
    total_results = None

    while True:
        page += 1
        if MAX_PAGES > 0 and page > MAX_PAGES:
            print(f"    [capped] reached MAX_PAGES={MAX_PAGES} for '{keyword}'")
            break

        # Encode spaces; NVD v2 does not accept + encoding
        encoded_kw = keyword.replace(" ", "%20")
        params = {
            "keywordSearch":  encoded_kw,
            "resultsPerPage": str(RESULTS_PER_PAGE),
            "startIndex":     str(start_index),
        }

        print(f"    page {page} (offset {start_index}) …", end=" ", flush=True)
        data = nvd_get(params)

        if not data:
            print("empty response")
            break

        if total_results is None:
            total_results = data.get("totalResults", 0)
            print(f"total={total_results}", flush=True)
        else:
            print(flush=True)

        vulns = data.get("vulnerabilities", [])
        for vuln in vulns:
            published = vuln.get("cve", {}).get("published", "")[:10]
            if published >= since_dt:
                results.append(vuln)

        start_index += len(vulns)
        if start_index >= (total_results or 0) or not vulns:
            break

        time.sleep(_request_delay())

    return results


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def extract_cvss(cve_item: dict[str, Any]) -> dict[str, Any]:
    """Return a dict of all available CVSS fields, preferring v3.1 > v3.0 > v2."""
    metrics = cve_item.get("metrics", {})
    for key in ("cvssMetricV31", "cvssMetricV30"):
        entries = metrics.get(key, [])
        if entries:
            e = entries[0]
            m = e["cvssData"]
            return {
                "version":             key[-3:].replace("V", "").replace("31", "3.1").replace("30", "3.0"),
                "severity":            CVSS_SEVERITY_MAP.get(m.get("baseSeverity", ""), "Unknown"),
                "score":               m.get("baseScore", 0.0),
                "vector":              m.get("vectorString", ""),
                "exploitability":      e.get("exploitabilityScore"),
                "impact":              e.get("impactScore"),
                "scope":               m.get("scope", ""),
            }
    entries = metrics.get("cvssMetricV2", [])
    if entries:
        e = entries[0]
        m = e["cvssData"]
        score = m.get("baseScore", 0.0)
        return {
            "version":         "2.0",
            "severity":        "High" if score >= 7 else "Medium" if score >= 4 else "Low",
            "score":           score,
            "vector":          m.get("vectorString", ""),
            "exploitability":  e.get("exploitabilityScore"),
            "impact":          e.get("impactScore"),
            "obtain_all":      e.get("obtainAllPrivilege"),
            "obtain_user":     e.get("obtainUserPrivilege"),
            "user_interaction": e.get("userInteractionRequired"),
            "scope":           "",
        }
    return {"severity": "Unknown", "score": 0.0, "vector": "", "version": ""}


def cve_to_markdown(vuln: dict[str, Any]) -> str:
    cve = vuln.get("cve", {})
    cve_id: str = cve.get("id", "CVE-UNKNOWN")

    # Description (prefer English)
    descriptions = cve.get("descriptions", [])
    description = next(
        (d["value"] for d in descriptions if d.get("lang") == "en"),
        descriptions[0]["value"] if descriptions else "No description available.",
    )

    # Dates and status
    published   = cve.get("published", "")[:10]
    modified    = cve.get("lastModified", "")[:10]
    vuln_status = cve.get("vulnStatus", "")
    source_id   = cve.get("sourceIdentifier", "")

    # CVSS (all available fields)
    cvss = extract_cvss(cve)
    vector   = cvss.get("vector", "")
    severity = cvss.get("severity", "Unknown")
    score    = cvss.get("score", 0.0)
    human_vector = cvss_to_human(vector) if vector else "N/A"

    # Inferred fields
    category   = infer_category(description, vector)
    root_cause = infer_root_cause(description)
    patterns   = code_pattern_hints(category)

    # Affected products (CPE): cpe:2.3:a:vendor:product:version:...
    affected: list[str] = []
    vendors: list[str] = []
    for config in cve.get("configurations", []):
        for node in config.get("nodes", []):
            for cpe_match in node.get("cpeMatch", []):
                if cpe_match.get("vulnerable"):
                    uri = cpe_match.get("criteria", "")
                    parts = uri.split(":")
                    if len(parts) >= 6:
                        vendor = parts[3]
                        product = f"{vendor}/{parts[4]}"
                        ver = parts[5] if parts[5] != "*" else "all"
                        ver_end = cpe_match.get("versionEndIncluding") or cpe_match.get("versionEndExcluding")
                        entry = f"{product} {ver}" + (f" (up to {ver_end})" if ver_end else "")
                        if entry not in affected:
                            affected.append(entry)
                        if vendor not in vendors:
                            vendors.append(vendor)

    # References — deduplicate, then group by tag
    all_refs: list[dict[str, Any]] = cve.get("references", [])
    seen: set[str] = set()
    unique_refs: list[dict[str, Any]] = []
    for r in all_refs:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique_refs.append(r)
    all_refs = unique_refs

    # Group by first tag for display
    ref_groups: dict[str, list[str]] = {}
    for r in all_refs:
        tags = r.get("tags", [])
        label = tags[0] if tags else "Other"
        ref_groups.setdefault(label, []).append(r["url"])

    # Weaknesses (CWE)
    cwes: list[str] = []
    for w in cve.get("weaknesses", []):
        for desc in w.get("description", []):
            if desc.get("lang") == "en" and desc.get("value", "").startswith("CWE-"):
                if desc["value"] not in cwes:
                    cwes.append(desc["value"])

    # Fix patch (best-effort; prioritises Patch-tagged GitHub commit refs)
    fix_patch: str | None = fetch_fix_patch(all_refs)

    # ---- Render ----
    lines: list[str] = []

    lines.append(f"# {cve_id}")
    lines.append("")

    # --- Metadata block ---
    lines.append(f"**CVE ID**: {cve_id}  ")
    lines.append(f"**Published**: {published}  ")
    lines.append(f"**Last Modified**: {modified}  ")
    if vuln_status:
        lines.append(f"**Status**: {vuln_status}  ")
    if source_id:
        lines.append(f"**Reporter**: {source_id}  ")
    if vendors:
        lines.append(f"**Vendor**: {', '.join(vendors)}  ")
    lines.append(f"**Severity**: {severity} ({score})  ")
    if vector:
        lines.append(f"**CVSS Version**: {cvss.get('version', '')}  ")
        lines.append(f"**CVSS Vector**: `{vector}`  ")
    lines.append(f"**Attack Summary**: {human_vector}  ")
    if cvss.get("exploitability") is not None:
        lines.append(f"**Exploitability Score**: {cvss['exploitability']}  ")
    if cvss.get("impact") is not None:
        lines.append(f"**Impact Score**: {cvss['impact']}  ")
    lines.append(f"**Category**: {category}  ")
    lines.append(f"**Root Cause Class**: {root_cause}  ")
    if cwes:
        lines.append(f"**CWE**: {', '.join(cwes)}  ")
    lines.append("")

    # --- Description ---
    lines.append("## Description")
    lines.append("")
    lines.append(description)
    lines.append("")

    # --- Affected Products ---
    if affected:
        lines.append("## Affected Products")
        lines.append("")
        for a in affected[:20]:
            lines.append(f"- {a}")
        lines.append("")

    # --- Root Cause Analysis ---
    lines.append("## Root Cause Analysis")
    lines.append("")
    if vector:
        p = parse_cvss_vector(vector)
        lines.append(
            f"This vulnerability is classified as **{root_cause}**. "
            f"The CVSS vector indicates the attack can be launched from the "
            f"**{AV_LABELS.get(p.get('AV', ''), 'unknown')}** attack surface "
            f"with **{AC_LABELS.get(p.get('AC', ''), 'unknown').lower()}** complexity "
            f"and **{PR_LABELS.get(p.get('PR', ''), 'unknown').lower()}** privileges required. "
            f"User interaction: **{UI_LABELS.get(p.get('UI', ''), 'unknown').lower()}**."
        )
    else:
        lines.append(f"This vulnerability is classified as **{root_cause}**. See description for details.")
    lines.append("")

    # --- Security Code Patterns ---
    lines.append("## Security Code Patterns")
    lines.append("")
    lines.append(
        f"Patterns in Go/Kubernetes controller code associated with **{category}** "
        "that reviewers should flag during code evaluation:"
    )
    lines.append("")
    for p in patterns:
        lines.append(f"- {p}")
    lines.append("")

    # --- Mitigation ---
    lines.append("## Mitigation")
    lines.append("")
    lines.append(_mitigation_text(category))
    lines.append("")

    # --- Fix Patch ---
    if fix_patch:
        lines.append("## Fix Patch")
        lines.append("")
        lines.append("Diff extracted from a referenced commit showing the upstream fix:")
        lines.append("")
        lines.append("```diff")
        lines.append(fix_patch.rstrip())
        lines.append("```")
        lines.append("")

    # --- References grouped by tag ---
    if ref_groups:
        lines.append("## References")
        lines.append("")
        for label in sorted(ref_groups):
            lines.append(f"**{label}**")
            lines.append("")
            for url in ref_groups[label][:5]:
                lines.append(f"- {url}")
            lines.append("")

    return "\n".join(lines)


def _mitigation_text(category: str) -> str:
    mitigations: dict[str, str] = {
        "Privilege Escalation": (
            "Apply least-privilege pod security standards: set "
            "`allowPrivilegeEscalation: false`, `runAsNonRoot: true`, and "
            "`readOnlyRootFilesystem: true` in all container security contexts. "
            "Use Kubernetes Pod Security Admission or OPA/Gatekeeper to enforce "
            "these at the cluster level. Audit all ServiceAccount ClusterRoleBindings."
        ),
        "Authentication Bypass": (
            "Ensure every request handler validates the caller's identity via "
            "`SubjectAccessReview` or RBAC. Set admission webhooks to "
            "`failurePolicy: Fail`. Validate and strip forwarded-identity headers "
            "at the ingress layer. Enable audit logging for all API server requests."
        ),
        "Denial of Service": (
            "Enforce `ResourceQuota` and `LimitRange` objects in every tenant namespace. "
            "Add `context.WithTimeout` to all controller-to-API-server calls. "
            "Use Kueue's own admission and borrowing limits to cap resource consumption "
            "per ClusterQueue. Implement rate limiting on webhook endpoints."
        ),
        "Information Disclosure": (
            "Never log full Kubernetes objects that may contain secret data. "
            "Use structured logging with explicit field selection. "
            "Scope RBAC roles to the minimum namespaces and resource types. "
            "Store secrets in an external vault rather than Kubernetes Secrets when possible."
        ),
        "Code Execution": (
            "Never pass user-supplied data to `exec.Command` or shell evaluation. "
            "Use a strict allowlist for any image or binary references. "
            "Apply seccomp profiles to limit syscall surface."
        ),
        "Injection": (
            "Validate and sanitize all user-supplied namespace, name, and label values "
            "before using them to construct API requests or YAML payloads. "
            "Use the Kubernetes API typed clients rather than string-built URLs."
        ),
        "RBAC Misconfiguration": (
            "Audit all ClusterRoles for wildcard verbs/resources. "
            "Prefer `RoleBinding` over `ClusterRoleBinding` where namespace scope is sufficient. "
            "Run `kubectl auth can-i --list --as=system:serviceaccount:<ns>:<sa>` periodically "
            "to verify minimal permissions."
        ),
        "Missing resource limits": (
            "Configure `LimitRange` defaults and `ResourceQuota` maximums. "
            "Reject workloads without explicit resource requests/limits in the admission webhook. "
            "Add back-pressure mechanisms (e.g. work queue depth limits) to controllers."
        ),
        "Race condition": (
            "Use optimistic concurrency via `resourceVersion` when updating Kubernetes objects. "
            "Re-fetch objects from the API server (not the cache) immediately before making "
            "admission decisions. Use `status.conditions` for workload state transitions."
        ),
        "Supply Chain": (
            "Pin all container images to their digest (`:tag@sha256:...`). "
            "Enable image signature verification via Cosign/Sigstore. "
            "Use admission webhooks to reject unsigned or unpinned images."
        ),
    }
    base = mitigations.get(
        category,
        "Review the affected component for the vulnerability class described. "
        "Apply the principle of least privilege, validate all inputs, and "
        "enforce resource limits at the Kubernetes admission layer.",
    )
    return base


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    state_file = OUTPUT_DIR / ".cve-sync-state.json"

    # Load existing state
    state: dict[str, Any] = {}
    if state_file.exists():
        with state_file.open() as f:
            state = json.load(f)

    written = 0
    skipped = 0
    total_fetched = 0

    for label, keywords in SEARCH_TARGETS:
        for keyword in keywords:
            print(f"\n==> Fetching CVEs for keyword: '{keyword}' (group: {label})")
            time.sleep(_request_delay())

            vulns = fetch_cves(keyword, CVE_SINCE)
            total_fetched += len(vulns)
            print(f"    {len(vulns)} CVE records returned")

            for vuln in vulns:
                cve_id: str = vuln.get("cve", {}).get("id", "")
                if not cve_id:
                    continue

                modified = vuln.get("cve", {}).get("lastModified", "")
                prev_modified = state.get(cve_id, {}).get("lastModified", "")

                out_path = OUTPUT_DIR / f"{cve_id}.md"

                if out_path.exists() and modified == prev_modified:
                    skipped += 1
                    continue

                md = cve_to_markdown(vuln)
                out_path.write_text(md, encoding="utf-8")
                state[cve_id] = {"lastModified": modified, "label": label}
                written += 1

            time.sleep(_request_delay())

    # Persist state
    with state_file.open("w") as f:
        json.dump(state, f, indent=2)

    print(f"\n==> CVE collection complete.")
    print(f"    Total CVE records fetched : {total_fetched}")
    print(f"    Files written (new/updated): {written}")
    print(f"    Files skipped (unchanged)  : {skipped}")
    print(f"    Output directory           : {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
