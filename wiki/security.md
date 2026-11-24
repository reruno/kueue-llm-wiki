# Security in Kueue

**Summary**: Landing page for code-security guidance applied to Kueue. Synthesizes 855 Kubernetes-ecosystem CVEs (`raw/cve/`) into the vulnerability classes and review patterns that matter for a Kueue contributor or reviewer.

**Sources**: `raw/cve/CVE-*.md` (875 entries spanning 2018–2026, vendors include `kubernetes`, `kubernetes-sigs`, `fluxcd`, `argoproj`, `jenkins`, `redhat`, `fedoraproject`); 2026-10 batch: CVE-2026-101919.md, CVE-2026-103413.md, CVE-2026-103546.md, CVE-2026-105216.md, CVE-2026-105223.md, CVE-2026-105985.md, CVE-2026-106487.md, CVE-2026-106561.md, CVE-2026-106563.md, CVE-2026-107446.md, CVE-2026-108546.md, CVE-2026-108570.md, CVE-2026-109358.md, CVE-2026-18517.md, CVE-2026-18529.md, CVE-2026-18533.md, CVE-2026-18537.md, CVE-2026-26287.md, CVE-2026-55252.md, CVE-2026-55797.md, CVE-2026-71895.md, CVE-2026-7767.md, CVE-2026-86671.md, CVE-2026-92393.md, CVE-2026-95837.md, CVE-2026-95838.md; Kueue code `pkg/controller/admissionchecks/multikueue/multikueuecluster.go`, `pkg/controller/jobframework/validation.go`; 2026-10-21 batch: CVE-2026-103314.md, CVE-2026-105311.md, CVE-2026-105312.md, CVE-2026-110248.md, CVE-2026-112778.md, CVE-2026-113672.md, CVE-2026-113708.md, CVE-2026-113709.md, CVE-2026-113727.md, CVE-2026-47218.md, CVE-2026-53999.md, CVE-2026-65162.md, CVE-2026-65172.md, CVE-2026-77459.md, CVE-2026-77524.md, CVE-2026-77564.md, CVE-2026-77934.md, CVE-2026-87354.md, CVE-2026-92982.md, CVE-2026-94197.md; raw/kueue/go.mod; KueueViz fixes pr-17088.md, pr-17143.md, pr-17246.md, pr-17249.md; pr-16035.md; raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md; 2026-10-28 batch: CVE-2025-30050.md, CVE-2026-102649.md, CVE-2026-113788.md, CVE-2026-114636.md, CVE-2026-114638.md, CVE-2026-114640.md, CVE-2026-115356.md, CVE-2026-83938.md; pr-14142.md, pr-17207.md, pr-17736.md, pr-17729.md, issue-17728.md; `raw/kueue/cmd/kueueviz/backend/handlers/websocket_handler.go`, `raw/kueue/config/components/networkpolicy/`. 2026-11-24 additions: CVE-2026-102339.md, CVE-2026-102340.md, CVE-2026-103002.md, CVE-2026-103506.md, CVE-2026-109797.md, CVE-2026-116472.md, CVE-2026-118760.md, CVE-2026-119115.md, CVE-2026-119572.md, CVE-2026-119573.md, CVE-2026-120091.md, CVE-2026-120306.md, CVE-2026-120307.md, CVE-2026-121374.md, CVE-2026-122310.md, CVE-2026-122986.md, CVE-2026-123047.md, CVE-2026-123059.md, CVE-2026-123810.md, CVE-2026-126643.md, CVE-2026-126802.md, CVE-2026-127073.md, CVE-2026-127077.md, CVE-2026-127080.md, CVE-2026-59185.md, CVE-2026-62284.md, CVE-2026-63121.md, CVE-2026-88982.md, CVE-2026-88984.md, CVE-2026-91163.md, CVE-2026-91168.md, CVE-2026-97373.md; 2026-11-24 second batch: CVE-2026-100975.md, CVE-2026-100976.md, CVE-2026-102884.md, CVE-2026-112788.md, CVE-2026-129235.md, CVE-2026-129236.md, CVE-2026-130007.md, CVE-2026-130622.md, CVE-2026-130623.md, CVE-2026-132239.md, CVE-2026-132896.md, CVE-2026-132947.md, CVE-2026-133173.md, CVE-2026-134360.md, CVE-2026-18491.md, CVE-2026-61581.md, CVE-2026-68903.md, CVE-2026-95839.md, CVE-2026-96298.md, CVE-2026-97187.md.

**Last updated**: 2026-11-24

---

## Why this section exists

Kueue is a privileged in-cluster controller. It runs with a ServiceAccount that has read access to most workload kinds and write access to its own CRDs plus `.spec.suspend` of integrated jobs. Its [[webhooks]] sit in the admission path. A bug in Kueue can:

- Crash-loop the cluster's batch-scheduling surface ([[security-denial-of-service|DoS]])
- Leak the contents of jobs across tenants ([[security-information-disclosure|info disclosure]])
- Let a low-privileged tenant escape their [[cluster-queue|ClusterQueue]] or [[cohort]] quota ([[security-authn-authz|authn/authz]])
- Be exploited by a malicious workload spec that the [[admission|admission flow]] doesn't validate ([[security-injection-and-input-validation|injection]])

The CVE corpus in `raw/cve/` is not a list of *Kueue* CVEs — Kueue has not had a published CVE as of 2026-11-24 (none of the 875 entries is a Kueue advisory). The corpus is a curated set of vulnerabilities from the broader Kubernetes ecosystem that teach the *patterns* a reviewer should flag in Kueue code. Every CVE file shares the same structure and ends with a `Security Code Patterns` checklist scoped by `Category`.

## Threat model for Kueue

Three classes of attacker matter:

1. **Authenticated low-privileged tenant** — can submit a [[workload]] and read their own namespace. Largest realistic attack surface because every Kueue user holds this role. Most CVEs in this corpus map here (CWE-863, CWE-20, CWE-400, CWE-770).
2. **Compromised neighbouring controller** — another in-cluster controller (Argo Workflows, Flux, RayOperator, etc.) is malicious or buggy and writes adversarial input into resources Kueue watches. The CVE-2022-39272-class issues (Flux crash on bad `.spec.interval`) live here.
3. **Cluster admin with stolen credentials** — out of scope for Kueue-level mitigation; relevant only via [[security-supply-chain|supply chain]] (image pinning, signing).

External attackers without cluster credentials are *not* a direct Kueue threat: Kueue does not expose a public network endpoint. The webhook port is reachable only from the API server.

## CVE corpus shape

| Category | Count | Primary CWEs |
| --- | --- | --- |
| Code Execution | 236 | CWE-94, CWE-78, CWE-502 |
| Information Disclosure | 163 | CWE-200, CWE-532, CWE-522, CWE-552 |
| Denial of Service | 101 | CWE-400, CWE-770, CWE-476 |
| Other | 79 | mixed |
| Privilege Escalation | 75 | CWE-269, CWE-266, CWE-276 |
| Authentication Bypass | 44 | CWE-287, CWE-306, CWE-352 |
| Unauthorized Write Access | 41 | CWE-863, CWE-285 |
| Injection | 28 | CWE-74, CWE-77, CWE-89, CWE-918 |
| RBAC Misconfiguration | 15 | CWE-284, CWE-862, CWE-863 |
| Path Traversal | 13 | CWE-22, CWE-61, CWE-363 |
| Supply Chain | 8 | CWE-295, CWE-494 |

Recomputed 2026-11-24 for severity (see the 2026-11-24 wave below for category counts of the 32 newest entries); category counts here were last computed 2026-10-28 on 803 files. The 2026-10-28 data-collection added 8 files: 2 Authentication Bypass, 2 Privilege Escalation, and one each of Information Disclosure, Injection, Other and Unauthorized Write Access. By severity they are 2 Critical, 3 High, 1 Medium and 2 Unknown. The previous recount (2026-09-29) covered 749 files, 67 of them added by the 2026-09-29 data-collection. The 2026-10 data-collection added 26 more (775 total): 11 Code Execution, 9 Information Disclosure, 2 Other, and one each of Authentication Bypass, Privilege Escalation, Supply Chain and Unauthorized Write Access; 14 High, 7 Medium, 1 Low, 4 Unknown. The 2026-10-21 data-collection added 20 (795 total): 7 Code Execution, 5 Information Disclosure, 2 Other, 2 Privilege Escalation, and one each of Authentication Bypass, Denial of Service, Path Traversal and Unauthorized Write Access; 7 Critical, 8 High, 2 Medium, 1 Low, 2 Unknown. Publication years skew recent (counts as of 2026-09-29): 320 entries published in 2026, 103 in 2025, and 326 across 2018–2024. The `Category` label is assigned by the data collector and is often wrong for the real bug class (for example Traefik authz bypasses and Envoy Gateway DoS bugs are tagged `Code Execution`); read the CWE and description, not the category.

Severity skews High (327) and Medium (321); Critical (124); Low (32); plus 68 Unknown and 3 None (875 files, recounted 2026-11-24 after the second batch; the 855-file count was High 318, Medium 314, Critical 124, Low 32, Unknown 64, None 3; the 803-file count was Medium 298, High 297, Critical 119, Low 30, Unknown 56, None 3, recounted 2026-10-28; the 795-file count was Medium 297, High 293, Critical 117, Low 30, Unknown 55, None 3. The same collection rescored the earlier Traefik entry CVE-2026-112778 from Unknown to High 8.8, which is why High rose by 4 and Unknown by only 1; the 749-file baseline before the two October waves was Medium 288, High 271, Critical 110, Low 28, Unknown 49, None 3). Kueue's direct exposure is concentrated in **DoS**, **info disclosure**, and **unauthorized write access** — categories where the controller-pattern code patterns map almost one-for-one onto Kueue's reconciler, scheduler, and webhook code.

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

Eight entries are outside Kueue's surface and are recorded only as reinforcing examples: Craft CMS (CVE-2026-105985) and Furion (CVE-2026-108570) template injection, Spotweb (CVE-2026-108546) shell injection, OpenRun open redirect (CVE-2026-55252), the IBM Maximo NetworkPolicy egress gap (CVE-2026-18517; Kueue shipped no NetworkPolicy then, and since pr-14142 ships **opt-in, ingress-only** policies, see below), and the containerd runtime bugs above.

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

## 2026-10-28 wave: what the 8 new CVEs add

> **Direct impact on Kueue: none.** No entry is a Kueue advisory. The products are Traefik's Kubernetes Ingress-NGINX provider (3 entries), Burrito (a Terraform operator), OpenBao, Lagoon, Azure Kubernetes Configuration Service and CGM CLININET. None of them appears in `raw/kueue/go.mod`, `cmd/kueueviz/backend/go.mod` or `hack/tools/go.mod` (checked for traefik, openbao, vault, burrito, `go-playground/webhooks` and lagoon; the only Azure module is the unrelated `Azure/go-ansiterm`) (source: raw/kueue/go.mod).

The new rules and reinforcements, each recorded on the page named:

1. **An empty or optional secret must not turn verification off** (Burrito CVE-2026-102649, Critical 9.9). With `webhookSecret` unset, the webhook library skipped signature checks, so anyone who could reach the endpoint could forge events. Forged fields were also never cross-checked against the object they named: the payload's branch was not compared with the real pull request. Kueue's in-repo analogue is the fail-closed `KUEUEVIZ_AUTH_MODE` validation (pr-17143). See [[security-authn-authz]].
2. **Keys derived by lossy normalization collide like delimiter-joined keys** (Traefik CVE-2026-114638). Two `auth-tls-secret` names that were equal after dot-to-dash normalization merged their client CAs. This is the same class as the KueueViz SubjectAccessReview cache-key collision (pr-17249). See [[security-code-patterns]].
3. **A generated sibling path that skips the access-control annotations** (Traefik CVE-2026-114636: the HTTP router built for ssl-passthrough Ingresses ignored `auth-*` and `whitelist-source-range`), and **client-supplied identity headers trusted on a plaintext path** (CVE-2026-114640: `Ssl-Client-Verify: SUCCESS`). Both reinforce existing rules. KueueViz's matching surface is the secondary-informer gap closed by pr-17207, and Gin's `SetTrustedProxies(nil)` in `SetupGinEngine`, which keeps forwarded headers untrusted. See [[security-authn-authz]].
4. **Renewing a session without re-checking the credential it came from** (OpenBao CVE-2026-115356). KueueViz long-lived WebSockets re-run a live TokenReview every 30 s (`tokenRevalidationInterval`). On an invalid token **or an error** they close with `ClosePolicyViolation`. See [[security-authn-authz#Long-lived sessions must re-check the original credential]].
5. Outside Kueue's surface, recorded only as reinforcing examples: a module name imported from a query parameter (CVE-2025-30050), shell argument injection in Lagoon's `ssh` service (CVE-2026-113788; see the option-injection rule in [[security-injection-and-input-validation]]) and a missing-authentication cloud endpoint (CVE-2026-83938).

**Kueue's own changes in this window teach more than the corpus**:

- **Opt-in ingress NetworkPolicies** for the controller-manager and KueueViz (pr-14142, main). They are off by default because NetworkPolicies are additive, and turning them on by default would widen a stricter policy a user already has. See [[security-authn-authz#Opt-in NetworkPolicies (pr-14142)]].
- **KueueViz secondary informers gated on cluster-wide `watch`** (pr-17207). See [[dashboard#Secondary informers need cluster-wide `watch` (pr-17207)]].
- **The Dependabot sync workflow moved from `pull_request_target` to `pull_request`** (pr-17736). See [[security-supply-chain]].

## 2026-11-24 wave: what the 32 new CVEs add

> **Direct impact on Kueue: none.** No entry is a Kueue advisory, and none of the affected products is a Kueue dependency. The corpus is now 855 files (803 plus the 2026-11-24 data-collection, which also added files outside this analysis). Of the 32 entries analysed here: 5 Critical, 12 High, 8 Medium, 2 Low, 5 Unknown. By collector category: 7 Code Execution, 6 Information Disclosure, 5 Authentication Bypass, 4 Other, 3 Injection, 2 each of Denial of Service, Privilege Escalation and RBAC Misconfiguration, 1 Path Traversal. Corpus-wide severity (855 files, recounted 2026-11-24): Critical 124, High 318, Medium 314, Low 32, Unknown 64, None 3.

CVEs, grouped:

- **Telepresence** CVE-2026-102339, CVE-2026-102340 (session hijack, unauthenticated namespace claim); **GPUStack** CVE-2026-103002 (proxy without per-resource authz); **Grafana** CVE-2026-103506 (feature-toggled API missing authz); **SAP astonish** CVE-2026-109797; **Warpgate** CVE-2026-91163 (verbose errors), CVE-2026-91168 (correlator keyed by username); **identrail** CVE-2026-59185. See [[security-authn-authz]].
- **Kubeflow Pipelines** CVE-2026-88982 (cache key lacks namespace), CVE-2026-88984 (empty namespace skips authz), CVE-2026-118760 (artifact routes). See [[security-code-patterns]].
- **Traefik Ingress-NGINX provider** CVE-2026-119572, CVE-2026-119573; **aws-privateca-issuer** CVE-2026-119115; **ingress-nginx** CVE-2026-116472 (`mirror-target` reaches local config API); **Kubewarden** CVE-2026-63121 (case-sensitive registry match). 
- **BuildPiper** CVE-2026-127073, CVE-2026-127077, CVE-2026-127080 (cluster-admin via manifests, cross-project cluster, hostPath `/`); **Beta9** CVE-2026-120306, CVE-2026-120307 (build and file-API escapes, 9.9 each); **Kyverno** CVE-2026-122310 (`apiCall` path fragment bypass, 9.9); **Temporal** CVE-2026-120091 (command execution via request client config); **OSAC operator** CVE-2026-62284 (kubeconfig exec/SSRF). See [[security-injection-and-input-validation]] and [[security-supply-chain]].
- **Credentials in the wrong place**: BaSyx charts CVE-2026-123047, CVE-2026-123059; AAP Gateway Operator CVE-2026-126643; NextScan CVE-2026-126802 (hardcoded). See [[security-information-disclosure]].
- **Other injection**: Checkmk CVE-2026-121374 (argument injection), Dynatrace MCP CVE-2026-123810 (DQL injection), draw.io CVE-2026-97373 (SSRF block-list gap). Azure Kubernetes Service CVE-2026-122986 has no technical detail.

Rules worth carrying into Kueue review (full checklist in [[security-best-practices]]):

1. A namespace, cluster or ID taken from the request is re-authorised; the empty form fails closed.
2. Authorization caches key on UID and are evicted on close.
3. Validate the string that is executed, not a cleaned copy.
4. Any client or kubeconfig struct from a CR is executable configuration; [[multikueue]] already validates `exec` and file paths, and the same review should cover `server`.
5. Never copy Secret values into ConfigMaps, CRs or status.

## 2026-11-24 second batch: what 20 more CVEs add

> **Direct impact on Kueue: none.** None is a Kueue advisory or a Kueue dependency. Corpus 855 → 875. By severity: 9 High, 7 Medium, 4 Unknown (no Critical or Low); by collector category: 5 Code Execution, 5 Other, 4 Information Disclosure, 3 Denial of Service, 2 Supply Chain, 1 Injection. Categories are collector labels and often wrong (the NVIDIA OpenShell secret-in-environment CVE is tagged DoS; the Connaisseur and Kubeshark entries are tagged Supply Chain).

- **Cross-namespace credential use (the pattern closest to Kueue):** aws-privateca-issuer before 1.12.0, CVE-2026-130622 and CVE-2026-130623 (CWE-441/639/863): a user who can create a *namespace-scoped* issuer got certificates signed with another namespace's stored AWS credentials, or with the controller's own identity. GitLab agent workspaces CVE-2026-97187 (read Secrets of other namespaces) and CVE-2026-18491 (granular PAT scope escaped through Kubernetes API proxy). TeamCity CVE-2026-132239 (project viewers used stored Kubernetes credentials). Review rule: a namespaced object must never resolve a credential, Secret or identity outside its own namespace unless the cluster-scoped owner opted in; compare with how [[multikueue]] resolves kubeconfig Secrets (needs verification against the current code before citing a namespace rule).
- **Unauthenticated management surfaces:** k8s-mcp-server CVE-2026-130007 (SSE listener on `0.0.0.0:8080`, session ID is only a correlation value), Apache Texera CVE-2026-112788 / CVE-2026-96298 (endpoints and websocket authorised only by a gateway that some deployments lack). See [[security-authn-authz]].
- **Tenant-scoped lookup without the tenant filter:** WatchAlert CVE-2026-133173 (`dataSourceGet` omits `tenant_id`, CWE-639). Same family as the Kubeflow Pipelines cache-key entries in the previous wave.
- **Caller-controlled path or URI:** LLMKube CVE-2026-68903 (`Model.spec.source` accepts absolute paths and `file://`), Heym CVE-2026-134360 (Playwright `file://` navigation reads the ServiceAccount token), Kubeshark CVE-2026-129235 (`download_file` destination unconfined). A CR field that names a file or URL is a read primitive in the operator's identity; allow-list schemes and roots. See [[security-injection-and-input-validation]].
- **Argument injection:** Kubeshark CVE-2026-129236 (`pod_regex` appended to `kubeshark tap` without `--`, so `--set` becomes a Helm override); TeamCity CVE-2026-132896 (code execution via Kubernetes Executor settings), CVE-2026-132947 (reflected XSS in namespace/deployment choosers).
- **Secrets in process environment / identity confusion:** NVIDIA OpenShell CVE-2026-100975 (shared SSH handshake secret in a plaintext env var) and CVE-2026-100976 (proxy attributes traffic by TCP source port). Datadog `datadog-apm-inject` CVE-2026-61581 (predictable host directory, CWE-379).
- **Validation that counts the wrong thing:** Connaisseur before 3.11.1 CVE-2026-102884 counts valid signature layers instead of distinct trust roots (CWE-697). containerd CVE-2026-95839: a malformed digest in an `io.containerd.manifest.subject` annotation panics unrecovered during image pull (CWE-248), the reminder to bound and recover parsing of externally supplied descriptors.

No new Kueue-specific rule beyond the 2026-11-24 list above; the Namespace/credential rule is the one to check when reviewing any new `secretRef`-style API field.

## Related pages

- [[code-quality]]
- [[architecture]]
- [[webhooks]]
- [[scheduler-internals]]
- [[reviewers]]
