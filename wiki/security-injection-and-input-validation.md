# Security — Injection, Input Validation, Path Traversal, and Code Execution

**Summary**: Combined coverage for Injection (27), Path Traversal (12), and Code Execution (218) CVE categories — they share the same root cause (untrusted input crossing a parse/exec boundary) and the same mitigations (validate at boundary, allowlist, type-safe builders).

**Sources**: `raw/cve/` — representative entries `CVE-2018-17450.md` (Jenkins SSRF), `CVE-2019-10165.md` (OpenShift command injection), `CVE-2019-11246.md` (kubectl cp tar extraction path traversal), `CVE-2019-1002101.md` (related path traversal), `CVE-2021-25741.md` (subpath symlink), `CVE-2022-23524-26.md` (Helm SSRF), `CVE-2025-15613.md` (Kyverno Service Call SSRF), 2026-09 additions `CVE-2026-80352.md` (Camel K YAML injection), `CVE-2026-77180.md`, `CVE-2026-52831.md`, `CVE-2026-53713.md`, `CVE-2026-84721.md`, `CVE-2026-59341.md`, and CWE-20/22/74/77/78/89/94/502/918/601 entries.

**Last updated**: 2026-09-29

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
- **An endpoint named in a CR, dialled with cluster data in the body (CWE-918).** `CVE-2025-15613` (Kyverno < 1.13.4, CVSS 6.5, `PR:L`): a user who may create `(Cluster)Policies` puts an external URL in a policy's `apiCall`/`service` configuration. The feature is documented for in-cluster Services but resolves external addresses too, and the policy *context* — which can include Secret contents — travels in the request, so a low-privilege author exfiltrates cluster data to a server they control. Two rules for Kueue: an "in-cluster only" endpoint field must be **enforced**, not just documented (resolve and reject non-cluster addresses); and never attach object context to an outbound request whose destination the requester chose.
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

## Connection strings and file paths built from CR fields

Two 2026 entries sharpen the "untrusted input crossing a parse boundary" rule for controllers that act on CR fields:

- `CVE-2026-53572` (KEDA, CWE-74/89): `pkg/scalers/postgresql_scaler.go` builds libpq connection strings from tenant-controlled `host`, `port`, `userName`, `dbName`, `sslmode` and `password`, while `escapePostgreConnectionParameter()` only quotes values containing a **literal space**. Tabs, newlines, carriage returns, form feeds, vertical tabs, quotes and backslashes therefore create additional key-value tokens when `pgx` parses the string, letting an attacker who can write a `TriggerAuthentication` or `ScaledObject` redirect the connection to their own server or turn off TLS. **Escaping that enumerates "the delimiter" is almost always wrong** — use a structured builder (`url.Values`, `pgx.ConnConfig`) instead.
- `CVE-2026-75889` (Grafana Alloy, CWE-552): `ServiceMonitor.bearerTokenFile` lets anyone with ServiceMonitor write access name an **arbitrary local file**, which Alloy reads and sends as a bearer token to an attacker-controlled scrape endpoint — including its own projected ServiceAccount token. Any CR field that names a path on the controller's filesystem is a credential-exfiltration primitive; Kueue should keep file paths confined to the operator Configuration and never accept one from a CR.

## 2026-09 additions: injection into generated config, commands and manifests

The new entries fall into four sub-patterns. None is a Kueue CVE; the reviewer rule is stated for each.

### Text-built configuration, commands and manifests

| CVE | Product / versions | CWE, CVSS | Mechanism |
| --- | --- | --- | --- |
| CVE-2026-80352 | Apache Camel K 2.0.0-2.9.2, 2.10.0-2.10.1 (fixed 2.9.3, 2.10.2, 2.11.0) | CWE-94, 9.8 Critical | YAML injection in CR configuration lets a CR author inject arbitrary Kubernetes objects created with the operator's privileges (source: CVE-2026-80352.md) |
| CVE-2026-77180 | NGINX Ingress Controller | CWE-76, 8.3 | annotation values written unsanitised into generated NGINX config; attacker injects directives, creates or deletes files (source: CVE-2026-77180.md) |
| CVE-2026-52831 | Nuclio < 1.16.4 | CWE-78, 8.0 | controller builds `/bin/sh -c "curl ..."` for a CronJob from `event.headers` keys and `event.body` (source: CVE-2026-52831.md) |
| CVE-2026-79754 | Nuclio 1.6.19-1.17.1 | CWE-77, no CVSS | `spec.build.tempDir` spliced into a shell command in the Kaniko builder; dashboard ServiceAccount has wildcard access (source: CVE-2026-79754.md) |
| CVE-2026-53713 | Envoy Gateway < 1.7.4 / 1.8.1 | CWE-20, 9.1 Critical | Lua validator's path normaliser did not collapse `//`, so a deny-list of critical paths was bypassed by `//etc/...` (source: CVE-2026-53713.md) |
| CVE-2026-100839 | Contrast < 1.18.0 | CWE-94, 8.4 | "BadAML": host-supplied ACPI/AML bytecode executed by the guest kernel (source: CVE-2026-100839.md) |

**Reviewer rules.** (1) Never render a CR or annotation value into a config file, shell string or YAML by `fmt.Sprintf` or `text/template`; build a typed object and marshal it. This restates the existing rule with three fresh 8.0+ examples, and Camel K shows the payload is not only commands but *whole manifests* created under the operator's identity. (2) A **deny-list** of paths or tokens is bypassed by any alternate spelling (`//`, `..`, case, encodings); canonicalise with `filepath.Clean` and prefer an allow-list, and compare only after canonicalisation. (3) Data from the layer below you (host to guest, tenant to operator) is untrusted even when the schema is well formed. Kueue currently has no `os/exec` or template rendering in `pkg/`, so these are guard-rails for future features (for example templated AdmissionCheck parameters).

### SSRF: controller dials a tenant-chosen destination

- **Ansible Automation Platform automation-controller, CVE-2026-84721** (CWE-918, 6.4): SMTP host and port from a notification template are dialled without blocking loopback, link-local or reserved ranges; connection errors are reflected in the notification record, giving an open/closed/filtered port-scan oracle, and a shared template's stored SMTP password can be sent to an attacker host (source: CVE-2026-84721.md).
- **MLRun <= 1.11.0, CVE-2026-92568** (CWE-918, 5.4): a run's `WebhookNotification` sends HTTP requests from the API server to internal addresses or cloud metadata on terminal state (source: CVE-2026-92568.md).
- **Eclipse Che 7.79.0-7.121.0, CVE-2026-86590** (CWE-918, no CVSS): `POST /dashboard/api/data/resolver` GETs any caller-supplied URL, reaching `169.254.169.254` and in-cluster Services; the operator allow-list was not applied (source: CVE-2026-86590.md).
- **Omni < 1.6.6 / 1.7.3, CVE-2026-45723** (CWE-20/22/918, 2.7): `TalosVersion` unvalidated and joined with `url.URL.JoinPath`, whose normalisation turns `..` segments into requests to unintended paths on the image-factory host (source: CVE-2026-45723.md).
- **JetBrains IntelliJ IDEA < 2026.2.2, CVE-2026-86503** (CWE-918, 3.3): opening an untrusted project triggers Kubernetes spec-source URL fetches (source: CVE-2026-86503.md).

These extend the existing `CVE-2025-15613`, `CVE-2026-71208` and `CVE-2026-73263` entries. Two new refinements: **an error message that distinguishes connect outcomes is itself a scanning oracle**, so status conditions for an unreachable MultiKueue worker or AdmissionCheck endpoint should carry a generic reason; and **URL-joining helpers normalise `..`**, so a path segment from a CR must be validated as a version or name before `JoinPath`.

### Path traversal and unsafe archive/file reads

- **Flux source-controller 0.0.17-1.8.4, CVE-2026-47680** (CWE-23, no CVSS): object keys in a `Bucket` write fetched data outside the per-reconciliation working directory (source: CVE-2026-47680.md).
- **Rancher Fleet 0.12-0.16 (fixed 0.16.2, 0.15.7, 0.14.11, 0.13.16, 0.12.20), CVE-2026-93537** (CWE-23, 6.5): bundle content from a Git repository makes Fleet read files from the processing environment, including Helm registry credentials, into the generated `Bundle` (source: CVE-2026-93537.md).
- **kubectl `cp` on Windows, CVE-2026-19444** (CWE-22, 6.5): a malicious `tar` in the container writes to arbitrary local paths (source: CVE-2026-19444.md). Another instance of the `CVE-2019-11246` family; `kueuectl` does not extract archives.
- **Contrast < 1.19.1, CVE-2026-100838** (CWE-59, 8.1): a flawed CopyFile policy allowed arbitrary writes to the guest root filesystem (source: CVE-2026-100838.md).

**Rule:** any name arriving from a remote listing (object key, tar entry, chart file name) must be resolved with `filepath.Join(root, name)` followed by a check that the result has the prefix `root + separator`; symlinks need `os.Root` or `EvalSymlinks`. Prefer Go 1.24's `os.Root` for any future Kueue code that writes files.

### Side channel through templates

**Sealed Secrets, CVE-2026-59341** (CWE-203, 4.2): the unauthenticated `POST /v1/verify` and `/v1/rotate` handlers unsealed a secret and then rendered Go templates from `spec.template.data`, which was **not bound into the AEAD label**. An attacker copies a victim's metadata and ciphertext, swaps in `{{ if eq (substr 0 1 .password) "S" }}ok{{ else }}{{ fail "x" }}{{ end }}` and reads HTTP 200 versus 409 as one bit per request (source: CVE-2026-59341.md). Rules: every field that influences interpretation of ciphertext must be inside the authenticated data; never evaluate tenant templates in a context that contains decrypted data; and do not map internal errors to distinguishable status codes on unauthenticated endpoints.

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[webhooks]]
- [[admission]]
- [[dashboard]]
