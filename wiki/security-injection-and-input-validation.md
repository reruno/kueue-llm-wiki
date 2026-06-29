# Security — Injection, Input Validation, Path Traversal, and Code Execution

**Summary**: Combined coverage for Injection (13), Path Traversal (10), and Code Execution (161) CVE categories — they share the same root cause (untrusted input crossing a parse/exec boundary) and the same mitigations (validate at boundary, allowlist, type-safe builders).

**Sources**: `raw/cve/` — representative entries `CVE-2018-17450.md` (Jenkins SSRF), `CVE-2019-10165.md` (OpenShift command injection), `CVE-2019-11246.md` (kubectl cp tar extraction path traversal), `CVE-2019-1002101.md` (related path traversal), `CVE-2021-25741.md` (subpath symlink), `CVE-2022-23524-26.md` (Helm SSRF), and CWE-20/22/74/77/78/89/94/502/918/601 entries.

**Last updated**: 2026-06-29

---

## Why this matters for Kueue

Kueue does *not* execute user-supplied code, shell out to commands, or parse files from disk. That removes the highest-impact classes (CWE-78 command injection, CWE-22 path traversal via file open). But four lower-impact attack surfaces remain:

1. **Constructed API requests.** Building label selectors, field paths, or URLs from `workload.Name` or annotation values.
2. **Template rendering.** Anywhere Kueue formats an output by interpolating a user-supplied string — webhook responses, events, log messages, or future Helm-style template fields.
3. **Decoded payloads.** YAML/JSON re-parsing of embedded strings (e.g. an integration's nested `template` field).
4. **The [[dashboard|KueueViz UI]].** A standard web UI surface: XSS (CWE-79), CSRF (CWE-352), open redirect (CWE-601).

## Patterns to flag in review

### Injection (CWE-74, CWE-77, CWE-78, CWE-89, CWE-94, CWE-918)

From the corpus:

- **Building API server URLs from user-controlled namespace/name fields.** Mitigation: use the typed Kubernetes client (`client.Get(ctx, types.NamespacedName{...}, obj)`), never construct REST paths by string concatenation. Kueue already follows this pattern; the rule kicks in only if someone adds direct HTTP code.
- **SSRF via container image URLs or init-container pull specs (CWE-918).** Kueue does not fetch URLs server-side, but [[admission-check]] implementations might. Validate that any new admission check doesn't dereference user-supplied URLs from the controller pod.
- **Using `fmt.Sprintf` to construct YAML/JSON payloads.** Always marshal a typed struct; never string-build YAML.
- **Executing user-supplied strings via `exec.Command` without allowlist (CWE-78).** Kueue contains no `os/exec` calls in `pkg/`; verify on review.
- **Template injection in labels/annotations rendered server-side (CWE-94).** If a feature renders `Sprintf(format, userInput)` where `format` could be tenant-supplied, both the format string and the args are untrusted — use `%q` for safe quoting or fixed format strings only.

### Input validation (CWE-20)

The corpus's CWE-20 entries cluster around two patterns:

1. **Field-format validation missing in the webhook.** Anything the controller parses (durations, IPs, selectors, label keys) must be validated in [[webhooks|the validating webhook]] before the controller sees it. The Flux CVE-2022-39272 pattern is in [[security-denial-of-service]] for a reason — invalid input that survives admission causes DoS.
2. **Missing length / regex bounds.** Label values, annotation keys, and the controller's own annotation namespace (`kueue.x-k8s.io/...`) should have explicit length caps in webhook validation.

### Path traversal (CWE-22, CWE-61, CWE-363)

Limited Kueue surface, but applies if anyone adds:

- File-path construction from CR fields (`filepath.Join(base, userName)` without `filepath.Clean` + prefix check).
- TAR/ZIP extraction (the `kubectl cp` family of CVEs — never extract entries with `..` in their path).
- Symlink-following file reads.

### Code execution and deserialization (CWE-94, CWE-502)

- **`yaml.Unmarshal(data, &interface{})`** with the permissive YAML scheme allows constructor injection in some libraries. Use the typed scheme via `sigs.k8s.io/yaml` or `runtime.Decode`.
- **`encoding/gob`** is not safe on untrusted input. Don't use it on the boundary.
- **`text/template` / `html/template`** rendering a template whose body is user-supplied — pin to safe-only constructs or refuse.

### XSS / CSRF / Open Redirect (CWE-79, CWE-352, CWE-601)

Applies to [[dashboard|KueueViz]]. The CVE corpus has 11 XSS, 6 CSRF, and 1 open-redirect entries — most against Kubernetes Dashboard / ArgoCD / Jenkins UIs. Standard mitigations:

- Render values server-side with proper escaping (`html/template`, not `text/template`).
- CSRF tokens on state-changing requests.
- Validate any `?redirect=` parameter against an allowlist of internal paths.

## Mitigation pattern in CVE corpus

> Validate and sanitize all user-supplied namespace, name, and label values before using them to construct API requests or YAML payloads. Use the Kubernetes API typed clients rather than string-built URLs. Never pass user-supplied data to `exec.Command` or shell evaluation. Use a strict allowlist for any image or binary references.

For Kueue, the simplified rule is: **validate at the webhook boundary, then trust the typed object thereafter.** Re-validation in the reconciler is fine for defense-in-depth but cannot replace webhook validation, because some objects bypass webhooks (existing CRs at upgrade, `--validate=false`).

## Specific checks during PR review

- `git grep -nE 'fmt\.Sprintf.*yaml|fmt\.Sprintf.*json' pkg/` — flag every hit.
- `git grep -n 'os/exec' pkg/` — should be empty.
- `git grep -n 'http\.Get\|http\.Post' pkg/` — flag every hit; verify the URL is not derived from CR content.
- `git grep -n 'filepath\.Join' pkg/` — verify the second arg is not user-supplied.

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[webhooks]]
- [[admission]]
- [[dashboard]]
