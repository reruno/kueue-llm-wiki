# Security in Kueue

**Summary**: Landing page for code-security guidance applied to Kueue. Synthesizes 569 Kubernetes-ecosystem CVEs (`raw/cve/`) into the vulnerability classes and review patterns that matter for a Kueue contributor or reviewer.

**Sources**: `raw/cve/CVE-*.md` (569 entries spanning 2018–2026, vendors include `kubernetes`, `kubernetes-sigs`, `fluxcd`, `argoproj`, `jenkins`, `redhat`, `fedoraproject`).

**Last updated**: 2026-06-29

---

## Why this section exists

Kueue is a privileged in-cluster controller. It runs with a ServiceAccount that has read access to most workload kinds and write access to its own CRDs plus `.spec.suspend` of integrated jobs. Its [[webhooks]] sit in the admission path. A bug in Kueue can:

- Crash-loop the cluster's batch-scheduling surface ([[security-denial-of-service|DoS]])
- Leak the contents of jobs across tenants ([[security-information-disclosure|info disclosure]])
- Let a low-privileged tenant escape their [[cluster-queue|ClusterQueue]] or [[cohort]] quota ([[security-authn-authz|authn/authz]])
- Be exploited by a malicious workload spec that the [[admission|admission flow]] doesn't validate ([[security-injection-and-input-validation|injection]])

The CVE corpus in `raw/cve/` is not a list of *Kueue* CVEs — Kueue has not had a published CVE as of 2026-05. The corpus is a curated set of vulnerabilities from the broader Kubernetes ecosystem that teach the *patterns* a reviewer should flag in Kueue code. Every CVE file shares the same structure and ends with a `Security Code Patterns` checklist scoped by `Category`.

## Threat model for Kueue

Three classes of attacker matter:

1. **Authenticated low-privileged tenant** — can submit a [[workload]] and read their own namespace. Largest realistic attack surface because every Kueue user holds this role. Most CVEs in this corpus map here (CWE-863, CWE-20, CWE-400, CWE-770).
2. **Compromised neighbouring controller** — another in-cluster controller (Argo Workflows, Flux, RayOperator, etc.) is malicious or buggy and writes adversarial input into resources Kueue watches. The CVE-2022-39272-class issues (Flux crash on bad `.spec.interval`) live here.
3. **Cluster admin with stolen credentials** — out of scope for Kueue-level mitigation; relevant only via [[security-supply-chain|supply chain]] (image pinning, signing).

External attackers without cluster credentials are *not* a direct Kueue threat: Kueue does not expose a public network endpoint. The webhook port is reachable only from the API server.

## CVE corpus shape

| Category | Count | Primary CWEs |
| --- | --- | --- |
| Code Execution | 161 | CWE-94, CWE-78, CWE-502 |
| Information Disclosure | 119 | CWE-200, CWE-532, CWE-522, CWE-552 |
| Denial of Service | 85 | CWE-400, CWE-770, CWE-476 |
| Privilege Escalation | 53 | CWE-269, CWE-266, CWE-276 |
| Other | 53 | mixed |
| Unauthorized Write Access | 30 | CWE-863, CWE-285 |
| Authentication Bypass | 29 | CWE-287, CWE-306, CWE-352 |
| Injection | 13 | CWE-74, CWE-77, CWE-89, CWE-918 |
| Path Traversal | 10 | CWE-22, CWE-61, CWE-363 |
| RBAC Misconfiguration | 9 | CWE-284, CWE-862, CWE-863 |
| Supply Chain | 7 | CWE-295, CWE-494 |

Severity skews Medium (236) and High (216); Critical (73); Low (19); plus 22 Unknown and 3 None. Kueue's direct exposure is concentrated in **DoS**, **info disclosure**, and **unauthorized write access** — categories where the controller-pattern code patterns map almost one-for-one onto Kueue's reconciler, scheduler, and webhook code.

## Where each topic lives

- [[security-code-patterns]] — master checklist of patterns to flag in code review, grouped by category and CWE.
- [[security-denial-of-service]] — DoS patterns: unbounded loops, missing timeouts, large allocations from untrusted input. Highest direct relevance to [[scheduler-internals]], [[webhooks]], and [[admission]].
- [[security-authn-authz]] — Authentication bypass, RBAC misconfiguration, privilege escalation. Relevant to Kueue's controller ServiceAccount, webhook handlers, and [[multikueue]] cross-cluster credentials.
- [[security-information-disclosure]] — Secret leakage in logs, error responses, annotations, cross-tenant visibility. Relevant to [[metrics]], [[visibility-api]], and structured logging.
- [[security-injection-and-input-validation]] — Injection, path traversal, code execution via untrusted strings. Relevant to anywhere Kueue formats user-supplied labels/annotations into commands, URLs, or payloads.
- [[security-supply-chain]] — Image pinning, signature verification, dependency-bump discipline.
- [[security-best-practices]] — Actionable Kueue-specific checklist a reviewer can paste into a PR.

## How this complements [[code-quality]]

[[code-quality]] captures *what reviewers consistently block on* in `kubernetes-sigs/kueue` PRs: upgrade safety, integration tests, naming, API versioning, scope. Security review is a separate axis that the active reviewers do not always call out explicitly — partly because Kueue has had no public CVE, partly because the project has no dedicated security reviewer in `OWNERS`. The pages here are a complement, not a replacement, and should be applied alongside the [[code-quality|code-quality bar]] during review.

## Related pages

- [[code-quality]]
- [[architecture]]
- [[webhooks]]
- [[scheduler-internals]]
- [[reviewers]]
