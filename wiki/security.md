# Security in Kueue

**Summary**: Landing page for code-security guidance applied to Kueue. Synthesizes 682 Kubernetes-ecosystem CVEs (`raw/cve/`) into the vulnerability classes and review patterns that matter for a Kueue contributor or reviewer.

**Sources**: `raw/cve/CVE-*.md` (682 entries spanning 2018–2026, vendors include `kubernetes`, `kubernetes-sigs`, `fluxcd`, `argoproj`, `jenkins`, `redhat`, `fedoraproject`).

**Last updated**: 2026-09-01

---

## Why this section exists

Kueue is a privileged in-cluster controller. It runs with a ServiceAccount that has read access to most workload kinds and write access to its own CRDs plus `.spec.suspend` of integrated jobs. Its [[webhooks]] sit in the admission path. A bug in Kueue can:

- Crash-loop the cluster's batch-scheduling surface ([[security-denial-of-service|DoS]])
- Leak the contents of jobs across tenants ([[security-information-disclosure|info disclosure]])
- Let a low-privileged tenant escape their [[cluster-queue|ClusterQueue]] or [[cohort]] quota ([[security-authn-authz|authn/authz]])
- Be exploited by a malicious workload spec that the [[admission|admission flow]] doesn't validate ([[security-injection-and-input-validation|injection]])

The CVE corpus in `raw/cve/` is not a list of *Kueue* CVEs — Kueue has not had a published CVE as of 2026-09. The corpus is a curated set of vulnerabilities from the broader Kubernetes ecosystem that teach the *patterns* a reviewer should flag in Kueue code. Every CVE file shares the same structure and ends with a `Security Code Patterns` checklist scoped by `Category`.

## Threat model for Kueue

Three classes of attacker matter:

1. **Authenticated low-privileged tenant** — can submit a [[workload]] and read their own namespace. Largest realistic attack surface because every Kueue user holds this role. Most CVEs in this corpus map here (CWE-863, CWE-20, CWE-400, CWE-770).
2. **Compromised neighbouring controller** — another in-cluster controller (Argo Workflows, Flux, RayOperator, etc.) is malicious or buggy and writes adversarial input into resources Kueue watches. The CVE-2022-39272-class issues (Flux crash on bad `.spec.interval`) live here.
3. **Cluster admin with stolen credentials** — out of scope for Kueue-level mitigation; relevant only via [[security-supply-chain|supply chain]] (image pinning, signing).

External attackers without cluster credentials are *not* a direct Kueue threat: Kueue does not expose a public network endpoint. The webhook port is reachable only from the API server.

## CVE corpus shape

| Category | Count | Primary CWEs |
| --- | --- | --- |
| Code Execution | 194 | CWE-94, CWE-78, CWE-502 |
| Information Disclosure | 137 | CWE-200, CWE-532, CWE-522, CWE-552 |
| Denial of Service | 94 | CWE-400, CWE-770, CWE-476 |
| Privilege Escalation | 67 | CWE-269, CWE-266, CWE-276 |
| Other | 66 | mixed |
| Unauthorized Write Access | 37 | CWE-863, CWE-285 |
| Authentication Bypass | 34 | CWE-287, CWE-306, CWE-352 |
| Injection | 22 | CWE-74, CWE-77, CWE-89, CWE-918 |
| RBAC Misconfiguration | 13 | CWE-284, CWE-862, CWE-863 |
| Path Traversal | 11 | CWE-22, CWE-61, CWE-363 |
| Supply Chain | 7 | CWE-295, CWE-494 |

Recomputed 2026-09-01 from `raw/cve/` (682 files). Publication years skew recent: 253 entries published in 2026, 103 in 2025, and 214 across 2019–2024.

Severity skews Medium (264) and High (251); Critical (102); Low (24); plus 38 Unknown and 3 None. Kueue's direct exposure is concentrated in **DoS**, **info disclosure**, and **unauthorized write access** — categories where the controller-pattern code patterns map almost one-for-one onto Kueue's reconciler, scheduler, and webhook code.

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

## The first confirmed instance in Kueue's own code

Kueue still has no published CVE, but the 2026-08 pod-group fix ([[pr-13960]]) is a genuine, tenant-reachable **quota bypass** and is the best in-repo example of the classes on these pages. Summary:

- A Pod carrying `kueue.x-k8s.io/pod-group-name: <victim-workload-name>` — a **client-supplied string used as a cross-object primary key** — caused Kueue to mark an unrelated Workload `Finished` with reason `OwnerNotFound` and strip its `resource-in-use` finalizer.
- The victim's quota was released from the cache while its Pods kept running, and the victim's own Job reconciler then dropped the Job finalizer, so the Job ran completely untracked.
- **No privileges beyond creating one Pod** in a namespace where the plain-Pod integration is active, with no queue name, no quota reservation and no admission. Creating and deleting a single throwaway Pod was enough.

Full mechanism, reachability analysis and the two-condition fix predicate: [[integration-plain-pod#PodGroup Workload adoption is guarded by `is-group-workload`]].

Reviewer takeaway, generalised: **any lookup keyed only on a name the tenant controls needs a second, Kueue-stamped condition** (an ownership marker, an owner-reference shape, or a UID). Three more instances of the same shape landed in this window:

- `kueuectl delete workload` deleted an owner **by name**, destroying a same-named replacement object; now uses a **UID delete precondition** ([[pr-14831]]).
- Admission fair-sharing compared LocalQueues by `spec.queueName` alone, so `team-a/default` and `team-b/default` were the same queue; now namespace-qualified ([[pr-14547]]).
- The scheduling-equivalence hash consumed the client-settable `kueue.x-k8s.io/role-hash` annotation via the PodSet name ([[pr-14784]], [[issue-14802]]).

## Related pages

- [[code-quality]]
- [[architecture]]
- [[webhooks]]
- [[scheduler-internals]]
- [[reviewers]]
