# Security in Kueue

**Summary**: Landing page for code-security guidance applied to Kueue. Synthesizes 795 Kubernetes-ecosystem CVEs (`raw/cve/`) into the vulnerability classes and review patterns that matter for a Kueue contributor or reviewer.

**Sources**: `raw/cve/CVE-*.md` (795 entries spanning 2018–2026, vendors include `kubernetes`, `kubernetes-sigs`, `fluxcd`, `argoproj`, `jenkins`, `redhat`, `fedoraproject`); 2026-10 batch: CVE-2026-101919.md, CVE-2026-103413.md, CVE-2026-103546.md, CVE-2026-105216.md, CVE-2026-105223.md, CVE-2026-105985.md, CVE-2026-106487.md, CVE-2026-106561.md, CVE-2026-106563.md, CVE-2026-107446.md, CVE-2026-108546.md, CVE-2026-108570.md, CVE-2026-109358.md, CVE-2026-18517.md, CVE-2026-18529.md, CVE-2026-18533.md, CVE-2026-18537.md, CVE-2026-26287.md, CVE-2026-55252.md, CVE-2026-55797.md, CVE-2026-71895.md, CVE-2026-7767.md, CVE-2026-86671.md, CVE-2026-92393.md, CVE-2026-95837.md, CVE-2026-95838.md; Kueue code `pkg/controller/admissionchecks/multikueue/multikueuecluster.go`, `pkg/controller/jobframework/validation.go`; 2026-10-21 batch: CVE-2026-103314.md, CVE-2026-105311.md, CVE-2026-105312.md, CVE-2026-110248.md, CVE-2026-112778.md, CVE-2026-113672.md, CVE-2026-113708.md, CVE-2026-113709.md, CVE-2026-113727.md, CVE-2026-47218.md, CVE-2026-53999.md, CVE-2026-65162.md, CVE-2026-65172.md, CVE-2026-77459.md, CVE-2026-77524.md, CVE-2026-77564.md, CVE-2026-77934.md, CVE-2026-87354.md, CVE-2026-92982.md, CVE-2026-94197.md; raw/kueue/go.mod; KueueViz fixes pr-17088.md, pr-17143.md, pr-17246.md, pr-17249.md; pr-16035.md; raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md.

**Last updated**: 2026-10-21

---

## Why this section exists

Kueue is a privileged in-cluster controller. It runs with a ServiceAccount that has read access to most workload kinds and write access to its own CRDs plus `.spec.suspend` of integrated jobs. Its [[webhooks]] sit in the admission path. A bug in Kueue can:

- Crash-loop the cluster's batch-scheduling surface ([[security-denial-of-service|DoS]])
- Leak the contents of jobs across tenants ([[security-information-disclosure|info disclosure]])
- Let a low-privileged tenant escape their [[cluster-queue|ClusterQueue]] or [[cohort]] quota ([[security-authn-authz|authn/authz]])
- Be exploited by a malicious workload spec that the [[admission|admission flow]] doesn't validate ([[security-injection-and-input-validation|injection]])

The CVE corpus in `raw/cve/` is not a list of *Kueue* CVEs — Kueue has not had a published CVE as of 2026-10-21 (none of the 795 entries is a Kueue advisory). The corpus is a curated set of vulnerabilities from the broader Kubernetes ecosystem that teach the *patterns* a reviewer should flag in Kueue code. Every CVE file shares the same structure and ends with a `Security Code Patterns` checklist scoped by `Category`.

## Threat model for Kueue

Three classes of attacker matter:

1. **Authenticated low-privileged tenant** — can submit a [[workload]] and read their own namespace. Largest realistic attack surface because every Kueue user holds this role. Most CVEs in this corpus map here (CWE-863, CWE-20, CWE-400, CWE-770).
2. **Compromised neighbouring controller** — another in-cluster controller (Argo Workflows, Flux, RayOperator, etc.) is malicious or buggy and writes adversarial input into resources Kueue watches. The CVE-2022-39272-class issues (Flux crash on bad `.spec.interval`) live here.
3. **Cluster admin with stolen credentials** — out of scope for Kueue-level mitigation; relevant only via [[security-supply-chain|supply chain]] (image pinning, signing).

External attackers without cluster credentials are *not* a direct Kueue threat: Kueue does not expose a public network endpoint. The webhook port is reachable only from the API server.

## CVE corpus shape

| Category | Count | Primary CWEs |
| --- | --- | --- |
| Code Execution | 218 | CWE-94, CWE-78, CWE-502 |
| Information Disclosure | 148 | CWE-200, CWE-532, CWE-522, CWE-552 |
| Denial of Service | 100 | CWE-400, CWE-770, CWE-476 |
| Privilege Escalation | 70 | CWE-269, CWE-266, CWE-276 |
| Other | 74 | mixed |
| Unauthorized Write Access | 38 | CWE-863, CWE-285 |
| Authentication Bypass | 40 | CWE-287, CWE-306, CWE-352 |
| Injection | 27 | CWE-74, CWE-77, CWE-89, CWE-918 |
| RBAC Misconfiguration | 15 | CWE-284, CWE-862, CWE-863 |
| Path Traversal | 12 | CWE-22, CWE-61, CWE-363 |
| Supply Chain | 7 | CWE-295, CWE-494 |

Recomputed 2026-09-29 from `raw/cve/` (749 files; 67 added by the 2026-09-29 data-collection). Later additions are not folded into the table. The 2026-10 data-collection added 26 more (775 total): 11 Code Execution, 9 Information Disclosure, 2 Other, and one each of Authentication Bypass, Privilege Escalation, Supply Chain and Unauthorized Write Access; 14 High, 7 Medium, 1 Low, 4 Unknown. The 2026-10-21 data-collection added 20 (795 total): 7 Code Execution, 5 Information Disclosure, 2 Other, 2 Privilege Escalation, and one each of Authentication Bypass, Denial of Service, Path Traversal and Unauthorized Write Access; 7 Critical, 8 High, 2 Medium, 1 Low, 2 Unknown. Publication years skew recent (counts as of 2026-09-29): 320 entries published in 2026, 103 in 2025, and 326 across 2018–2024. The `Category` label is assigned by the data collector and is often wrong for the real bug class (for example Traefik authz bypasses and Envoy Gateway DoS bugs are tagged `Code Execution`); read the CWE and description, not the category.

Severity skews Medium (289) and High (271); Critical (109); Low (28); plus 49 Unknown and 3 None. Kueue's direct exposure is concentrated in **DoS**, **info disclosure**, and **unauthorized write access** — categories where the controller-pattern code patterns map almost one-for-one onto Kueue's reconciler, scheduler, and webhook code.

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
- **A second pod-group quota bypass**: a forged `kueue.x-k8s.io/role-hash` let an oversized Pod run under a cheaper role's PodSet. It is fixed at **ungate time**, not in the webhook: before a pod-group Pod is ungated Kueue checks that it fits the PodSet its role maps to, and an oversized Pod stays gated with a `PodExceedsRoleRequests` event (#13382, gate `PodIntegrationVerifyRoleRequests`, Beta/on on main; shipped in **v0.20.2 / v0.19.9** as **Alpha/off** via backports pr-17123/pr-17124, so on those releases you must enable the gate to get the check) (source: CHANGELOG-0.20.md, CHANGELOG-0.19.md). See [[integration-plain-pod]].

## 2026-09 wave: what the 67 new CVEs add

The 2026-09-29 batch is dominated by **Kubernetes operators and gateways that act on tenant-authored CRs with cluster-wide credentials** (Envoy Gateway, Traefik, Capsule, Strimzi, ECK, Instana Agent operator, Nuclio, Fleet, OpenTelemetry Operator, Camel K, Contrast). None is a Kueue CVE and none affects Kueue directly (source: CVE-2026-53713.md, CVE-2026-85594.md, CVE-2026-55225.md). Five generalisable rules came out of it, each recorded on the category page named:

1. **Cluster-scoped objects keyed by bare CR name** (CVE-2026-19274, CVE-2026-85596): the tenant can collide with, overwrite or delete another tenant's object. Extends the "tenant-controlled identifier" rule below. See [[security-authn-authz]].
2. **A CR field that makes the operator mint RBAC or copy Secrets in a namespace the author does not own** (CVE-2026-55225, CVE-2026-19283, CVE-2026-78609, CVE-2026-61549, CVE-2026-79767). See [[security-authn-authz]].
3. **Guard applied on one branch but not its sibling** (CVE-2026-53718, CVE-2026-53714, CVE-2026-93991, CVE-2026-61794/61795, CVE-2026-55636). See [[security-code-patterns]].
4. **Decompression, tar-header and unbounded-`io.ReadAll` size bugs on tenant-supplied URLs** (CVE-2026-53716/53717, CVE-2026-50125, CVE-2026-54247, CVE-2026-53493). See [[security-denial-of-service]].
5. **Tenant-controlled URL or file path read with the controller's own credentials** (CVE-2026-47701, CVE-2026-84721, CVE-2026-92568, CVE-2026-86590, CVE-2026-93537). See [[security-injection-and-input-validation]] and [[security-information-disclosure]].

Kueue's exposure is still the same: it dials only MultiKueue worker endpoints, reads no tenant URLs or files, and the manager has no HTTP endpoint besides metrics, webhooks and the visibility API. The separately deployed [[dashboard|KueueViz]] backend is the other user-facing HTTP surface. The most relevant analogues are [[multikueue]] kubeconfigs, `prebuilt-workload-name`/`pod-group-name` lookups, and the webhook validators.

## 2026-10 wave: what the 26 new CVEs add

> **Direct impact on Kueue: none.** No entry in this batch is a Kueue advisory, and none affects a module Kueue ships. The three containerd entries (CVE-2026-95837, CVE-2026-95838, CVE-2026-107446 for the overlaybd snapshotter) are node-runtime bugs; containerd does not appear in any `go.mod`/`go.sum` under `raw/kueue/` (main module, `cmd/kueueviz/backend`, `hack/tools`, `site`). The two Go TLS entries are in `go-micro` (CVE-2026-105216) and the PHP `maclof/kubernetes-client` (CVE-2026-105223), neither of which Kueue imports. Nothing touches controller-runtime, client-go, the Go standard library, `x/net`, `x/crypto` or gRPC (source: CVE-2026-95837.md, CVE-2026-95838.md, CVE-2026-107446.md, CVE-2026-105216.md, CVE-2026-105223.md).

The batch is again dominated by operators and portals that act on tenant input with their own credentials. Seven rules come out of it, each recorded on the page named:

1. **Validation enforced on CREATE but skipped on UPDATE** (Apache YuniKorn CVE-2026-92393): a tenant changed the queue-routing ID and user annotation on UPDATE to land in a queue they were not allowed to use. Kueue had the same shape in Ray and Spark jobs, closed by #13293 behind `ValidateRayAndSparkJobUpdates`. See [[security-authn-authz]].
2. **A kubeconfig copied from a tenant Secret into a privileged context runs its exec plugin** (HyperShift CVE-2026-101919). Kueue's [[multikueue]] already rejects exec plugins, auth providers, token and CA *file* paths, basic auth and `insecure-skip-tls-verify` in `validateKubeconfig`/`validateRestConfig`. See [[security-authn-authz]].
3. **Falling back to the controller's own identity when the configured auth mode is unsupported** (Backstage CVE-2026-106487). See [[security-authn-authz]].
4. **A security flag cleared by a later initialisation step** (External Secrets Operator CVE-2026-26287). See [[security-code-patterns]].
5. **Credential-bearing clients that follow redirects or accept any URL scheme** (GitLab CVE-2026-7767, Eclipse Che CVE-2026-86671). See [[security-injection-and-input-validation]].
6. **Masking and filtering applied in one endpoint but not in a deprecated or sibling one** (Backstage CVE-2026-106561, CVE-2026-106563), and kubeconfigs readable by non-admins (DolphinScheduler CVE-2026-71895). See [[security-information-disclosure]].
7. **TLS verification off by default, or off when no CA is given** (CVE-2026-105216, CVE-2026-105223), and world-writable files written by a privileged installer (Contrast CVE-2026-109358). See [[security-supply-chain]].

Eight entries are outside Kueue's surface and are recorded only as reinforcing examples: Craft CMS (CVE-2026-105985) and Furion (CVE-2026-108570) template injection, Spotweb (CVE-2026-108546) shell injection, OpenRun open redirect (CVE-2026-55252), the IBM Maximo NetworkPolicy egress gap (CVE-2026-18517; Kueue ships no NetworkPolicy), and the containerd runtime bugs above.

## 2026-10-21 wave: what the 20 new CVEs add

> **Direct impact on Kueue: none.** No entry is a Kueue advisory, and none affects a module Kueue ships. The products are Argo CD (4 entries: CVE-2026-77459, CVE-2026-113672, CVE-2026-113708, CVE-2026-113709), KEDA, Traefik, F5 NGINX Ingress Controller, Radius, OpenChoreo, Talos, runwasi, Red Hat ACS, StreamsHub Console, Ansible Operator Plugins, NVIDIA AIStore (2), Amazon SageMaker Python SDK, Coze Studio and Oracle TimesTen. None of them appears in `raw/kueue/go.mod` (checked for argo, keda, traefik, nginx, radius, talos, wasm, strimzi, ansible, helm). Kueue's Argo Workflows integration does not import Argo CD code (source: raw/kueue/go.mod).

The batch is again about operators acting on tenant input with their own credentials. New rules, each on the page named:

1. **Authorize the stored object, not the submitted one** (OpenChoreo CVE-2026-113727). See [[security-authn-authz]].
2. **Never present the controller's token to a tenant-chosen endpoint** (KEDA CVE-2026-77524), and **namespace-confine every reference a CR or annotation can make** (StreamsHub CVE-2026-105311/105312, Traefik CVE-2026-112778). See [[security-authn-authz]].
3. **A tenant-writable status annotation must not select a deletion target** (Radius CVE-2026-53999). See [[security-authn-authz]] and [[security-denial-of-service]].
4. **Option injection survives argv-slice exec** (Argo CD CVE-2026-113708, missing `--`). See [[security-injection-and-input-validation]].
5. **Search paths, config homes and plugin directories must not come from tenant content** (Argo CD CVE-2026-113672, CVE-2026-113709). See [[security-injection-and-input-validation]] and [[security-supply-chain]].
6. **Error text and support bundles leak credentials** (SageMaker CVE-2026-110248, Talos CVE-2026-77564). See [[security-information-disclosure]].
7. **Bytes from untrusted input must not take the trusted-cache path** (runwasi CVE-2026-47218). See [[security-supply-chain]].

Kueue's own fixes in the same window teach more than the corpus does: four KueueViz authorization bugs (fail-open auth mode, delimiter-joined SAR cache keys, unauthorized secondary fields in `/ws/cohorts`, live updates without `watch` in `/ws/namespaces`) and the new opt-in, loopback-only `metrics.accessControlMode: None` (Alpha, main). See [[security-authn-authz#KueueViz fixes in this window: in-repo examples]] and [[security-code-patterns]].

## Related pages

- [[code-quality]]
- [[architecture]]
- [[webhooks]]
- [[scheduler-internals]]
- [[reviewers]]
