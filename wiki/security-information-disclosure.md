# Security — Information Disclosure

**Summary**: Patterns from the 148 Information Disclosure CVEs in `raw/cve/`. Covers logging hygiene, error-response content, [[metrics]] label cardinality (as a covert channel), [[visibility-api]] cross-tenant exposure, and credential handling.

**Sources**: `raw/cve/` — representative entries `CVE-2019-1002101.md` (kubectl cp path traversal also exposes file contents), `CVE-2020-8554.md` (man-in-the-middle via ExternalIP), `CVE-2020-8563.md` (sensitive info in logs), `CVE-2021-25741.md` (subpath symlink), CWE-200/CWE-532/CWE-522/CWE-552 entries broadly; 2026-09 additions `CVE-2025-71425.md`, `CVE-2025-71423.md`, `CVE-2026-47701.md`, `CVE-2026-86332.md`, `CVE-2026-94611.md`, `CVE-2026-45726.md`; 2026-10 additions `CVE-2026-106561.md`, `CVE-2026-106563.md`, `CVE-2026-71895.md`, `CVE-2026-18517.md`; 2026-10-21 additions `CVE-2026-110248.md`, `CVE-2026-77564.md`, `CVE-2026-113672.md`, `CVE-2026-113709.md`, `CVE-2026-65172.md`, `CVE-2026-77934.md`, `CVE-2026-87354.md`; Kueue sources pr-17246.md, pr-17088.md, pr-16035.md, `raw/kueue/pkg/config/metrics.go`.

**Last updated**: 2026-10-21

---

## Why this matters for Kueue

Kueue's multi-tenant story is built on namespace + LocalQueue isolation, but the controller itself sees *every* workload across the cluster. Anywhere Kueue serializes or persists data, two leakage modes are possible:

1. **Logs** (`klog`) — Kueue runs at log level 2 by default, with verbose modes up to v=6 in dev. Logging full objects is the single most common information-disclosure bug in the corpus.
2. **Metrics labels** — Prometheus label values are world-readable to anyone with metrics scrape access. Putting a Workload name, image, or annotation value into a label is a covert channel.

## Patterns to flag in review

From the shared `Security Code Patterns` block in every Info-Disclosure CVE file:

- **Logging objects that may contain secrets** (tokens, passwords, keys).
- **Error responses that include internal stack traces.**
- **Listing secrets across namespaces with a ClusterRole.**
- **Storing sensitive values in annotations or labels** (readable by all tenants).

## Specific anti-patterns by CWE

### CWE-532 — Sensitive information in log files (18 CVEs)

The most common pattern in the corpus. Concrete Kueue triggers:

- `klog.Errorf("failed to reconcile: %+v", workload)` — `%+v` on a Workload prints `.spec.podSets[*].template`, which may contain env vars with secrets injected from `secretKeyRef` (in some clusters these get resolved before reaching Kueue; in others not).
- `klog.V(2).Infof("admission check: %s", check)` where `check` is the AdmissionCheck object — third-party admission-check implementations may stash credentials in `parameters`.
- Logging webhook request bodies on validation failure — this is the most direct leak path because the body is *exactly* the user's submission.

**Rule**: log identifiers (`namespace/name`, UID, owner ref), never bodies. Use structured logging with explicit field selection. Already part of [[code-quality|the project's log-level discipline]] for noise reasons — same rule serves security.

### CWE-200 — Sensitive information exposure (17 CVEs)

Catch-all for fields that should not cross tenant boundaries. In Kueue:

- The [[visibility-api]] reveals pending-Workload position in queue. If exposed to tenants in other namespaces, this discloses other tenants' workload names. Verify per-namespace RBAC.
- [[metrics]] label cardinality: never use `workload_name` or `pod_name` as a label. Always use `cluster_queue` (cluster-scoped, intentionally public among queue users) or `namespace` (visible only to namespace members).
- The [[dashboard|KueueViz UI]] aggregates state across queues — its RBAC must mirror the visibility-api's. Two aggregate-field leaks were fixed in October 2026 (see "KueueViz: names leaked through aggregate fields" below).

### CWE-522 — Insufficiently protected credentials (7 CVEs)

For Kueue, this is about [[multikueue]] kubeconfig Secrets:

- Never log a kubeconfig field's contents, even at high verbosity.
- Never emit a kubeconfig in a Workload's status or events.
- When the manager controller fails to connect to a worker, the error must not include the bearer token from the kubeconfig.

### CWE-552 — Files / directories accessible to outside parties (4 CVEs)

Less directly applicable (Kueue writes few files), but relevant for:

- Diagnostic dumps written to `/tmp` or container ephemeral storage that survive into log-collection pipelines.
- The webhook certificate directory — verify mode 0400 and dedicated SA.

## Mitigation pattern in CVE corpus

> Never log full Kubernetes objects that may contain secret data. Use structured logging with explicit field selection. Scope RBAC roles to the minimum namespaces and resource types. Store secrets in an external vault rather than Kubernetes Secrets when possible.

The first sentence is the load-bearing rule for Kueue — `klog.InfoS("admitted", "workload", klog.KObj(wl))` rather than `klog.Infof("admitted %+v", wl)`. See [[code-quality]] for [[reviewer-mimowo|mimowo]]'s adjacent rule on log levels.

## Specific checks during PR review

- `git grep -nE '%\+v|%#v' pkg/` — flag every hit where the argument is a Kubernetes object.
- `git grep -n 'klog.*Secret\b' pkg/` — secret-typed logging.
- `git grep -nE 'WithValues.*token|WithValues.*password' pkg/`.
- For any new metric, verify the label set in `pkg/metrics/`: namespace and cluster-queue are OK; workload/pod name are not.

## 2026-09 additions

### Secrets and credentials read through an over-trusted operator

| CVE | Product / versions | CWE, CVSS | Mechanism and Kueue rule |
| --- | --- | --- | --- |
| CVE-2026-47701 | OpenTelemetry Operator < 0.152.0 (TargetAllocator) | CWE-200, 7.7 | `ServiceMonitor.bearerTokenFile` preserved as `CredentialsFile`; a tenant points it at the Collector's own ServiceAccount token file (source: CVE-2026-47701.md). Same class as `CVE-2026-75889`; never accept a filesystem path from a CR |
| CVE-2026-86332 | odh-dashboard (Red Hat OpenShift AI) | CWE-862, 6.5 | backend route reads Secrets with the dashboard ServiceAccount and returns the whole object, including NGC API key and image pull secret, to any authenticated user while create and delete were admin-gated (source: CVE-2026-86332.md). A UI backend that reads with its own identity must repeat the user's authorization (`SubjectAccessReview`); relevant to [[dashboard]] |
| CVE-2026-94611 | authentik < 2026.2.7 / 2026.5.7 / 2026.8.2 | CWE-200/522, 8.1 | API serializers return stored credentials to accounts that only have *view* permission (source: CVE-2026-94611.md). Separate read-config from read-secret fields and mark secret fields write-only |
| CVE-2026-45726 | Omni 1.3.0-1.6.5, 1.7.0-1.7.2 | CWE-200/522/732, 7.6 | `ImportedClusterSecrets` holds the whole CA bundle and the Reader role may fetch it (source: CVE-2026-45726.md) |
| CVE-2026-93537 | Rancher Fleet | CWE-23, 6.5 | file contents of the processing environment, including Helm registry credentials, land in a readable `Bundle` (source: CVE-2026-93537.md) |
| CVE-2026-59341 | Sealed Secrets | CWE-203, 4.2 | decryption oracle via template errors; see [[security-injection-and-input-validation]] |
| CVE-2026-19283 | Instana Agent Operator | CWE-863, 7.7 | etcd mTLS client credentials copied across namespaces; see [[security-authn-authz]] |
| CVE-2026-93991 | Argo Workflows 4.1.0-4.1.3 | CWE-639, 7.7 | `metadata.namespace!=` selector bypasses the access review, leaking archived workflow arguments and parameters; see [[security-authn-authz]] |
| CVE-2026-54246 | Skipper routesrv < 0.27.13 | CWE-306, 5.7 | unauthenticated cluster-wide route data (source: CVE-2026-54246.md) |
| CVE-2026-86464 | Eclipse aeriOS (development version) | CWE-200/306/798/1188/1392 | Helm chart exposed Keycloak and PostgreSQL via NodePort with fixed default credentials (source: CVE-2026-86464.md) |

**Rules for Kueue:** the visibility API and [[dashboard]] must impose the caller's permissions, not the server's; list and watch endpoints must apply the *same* namespace filter for every selector form; Helm values must not ship default credentials or NodePort services (the Kueue chart exposes only metrics and webhook ClusterIP Services, verify on review); any resource that bundles secrets with non-secret config should be split so `get` on the config does not reveal the secret.

### Secrets in logs and confidential-computing failures (Contrast)

The Contrast (Edgeless Systems) runtime supplies four log or key-handling lessons:

- **CVE-2025-71425** (< 1.8.1, CWE-532, 7.3): the initializer logged the workload secret at the **default** `info` level to pod logs. **CVE-2025-71423** (1.9.0-1.12.1, CWE-532, 7.3): a regression of the same bug, where the full `NewMeshCert` response was logged (source: CVE-2025-71425.md, CVE-2025-71423.md). Rule: a fixed log-leak needs a test that greps captured logs for the secret, otherwise refactors reintroduce it; log defaults are the exposure, not the debug level.
- **CVE-2025-71422** (< 1.12.1, CWE-347, 5.7): `cryptsetup open` succeeding was taken as proof of an encrypted volume even though a LUKS2 header may specify `cipher_null-ecb` (source: CVE-2025-71422.md). Rule: "the operation succeeded" is not evidence of the property you wanted; verify the property.
- **CVE-2026-100833** (1.14.0-1.23.0, CWE-20, 8.2): a bad rebase added an `allow_storage` rule that accepted `image_guest_pull` entries without checking the image digest (source: CVE-2026-100833.md). Rule: security policy files need their own tests that prove the negative case, especially after vendored-code rebases.
- **CVE-2025-71426** (< 1.4.1, CWE-285, 7.1) and **CVE-2025-71424** (<= 1.9.0, CWE-693, 3.5): a recovering Coordinator that does not verify the seed, and a Dockerfile `VOLUME` mount requiring the runtime to push data to the Kata agent (source: CVE-2025-71426.md, CVE-2025-71424.md).

### Other low-signal entries

| CVE | Product | CWE, CVSS | Note |
| --- | --- | --- | --- |
| CVE-2026-78600 | ECK up to 3.5.0 | CWE-459, 3.5 | credentials persist after RBAC denied an association |
| CVE-2026-91164 | Warpgate 0.23.0-0.27.3 | CWE-284/863, 4.3 | API token ignores `allowed_ip_ranges` |
| CVE-2026-50166, CVE-2026-52724 | Kuma < 2.7.26 / 2.9.16 / 2.11.14 / 2.12.11 / 2.13.7 | CWE-295 | TLS peer verification silently disabled when no CA file is given; see [[security-supply-chain]] |

## 2026-10 additions

None is a Kueue CVE ([[security#2026-10 wave: what the 26 new CVEs add]]).

| CVE | Product / versions | CWE, CVSS | Mechanism and Kueue rule |
| --- | --- | --- | --- |
| CVE-2026-106561 | Backstage `@backstage/plugin-kubernetes-backend` < 0.21.9 | CWE-200/863, 5.0 | a user with the standard Kubernetes resource read permission could get values the plugin is designed to **mask**. Exposure was limited to what the Backstage ServiceAccount can read in the entity's namespace and label selector (source: CVE-2026-106561.md). Redaction must happen on every serialisation path, including raw and aggregated views, and have a test per path |
| CVE-2026-106563 | same plugin < 0.21.8 | CWE-20/862, 5.3 | a **deprecated** services endpoint accepted crafted entity data and returned workload metadata across all configured clusters (source: CVE-2026-106563.md). Deprecated endpoints keep the current endpoint's authorization until they are removed. For Kueue, the [[visibility-api]] serves only `visibility.kueue.x-k8s.io/v1beta2` at this snapshot (`apis/visibility/` has no other version), so there is no legacy version to drift |
| CVE-2026-71895 | Apache DolphinScheduler 3.2.0 to before 3.4.3 | CWE-862, 7.1 | non-admin users could fetch the kubeconfig held for admin-managed cluster configuration and use it directly against the API server (source: CVE-2026-71895.md). For Kueue, [[multikueue]] worker kubeconfigs are Secrets in the Kueue config namespace. Neither `kueuectl` nor [[dashboard]] may read or return them, and the dashboard backend must not list Secrets |
| CVE-2026-18517 | IBM Maximo Location Service for Esri 9.0-9.2 | CWE-284, 7.7 | misconfigured NetworkPolicy allowed unintended egress (source: CVE-2026-18517.md). Kueue's manifests ship no NetworkPolicy, so egress restriction for the controller is the installer's choice |

**Rule added:** a UI or API that reads cluster data with its own ServiceAccount must apply redaction and namespace filtering on **every** handler and served version. This restates the 2026-09 `CVE-2026-86332` rule for [[dashboard]] with two more examples.

## KueueViz: names leaked through aggregate fields (fixed 2026-10)

The rule above was violated in Kueue's own dashboard and fixed in this window (release-0.20 and main only; release-0.19 KueueViz has no per-user authorization):

- `/ws/cohorts` put every ClusterQueue name into each Cohort's `clusterQueues` field for any user allowed to view Cohorts. It now checks `list clusterqueues` for the caller and omits the field on deny or on authorizer error (pr-17246, issue-17178; release-0.20 after v0.20.2).
- `/ws/namespaces` streamed LocalQueue-driven updates, which reveal queue existence and update timing per namespace, to callers without `watch localqueues`. The initial snapshot stays filtered by `list`; live updates now need cluster-wide `watch` (pr-17088, issue-17073; v0.20.2).

Generalised: a response is only as private as its **least-checked field**. When a handler embeds data of a second kind (names, counts, child lists), it needs a check for that kind too (source: pr-17246.md, pr-17088.md). See [[security-authn-authz#KueueViz fixes in this window: in-repo examples]].

## Metrics without authentication (main, Alpha)

`metrics.accessControlMode: None` (gate `MetricsAccessControl`, Alpha, off, main only; pr-16035) serves `/metrics` without TokenReview/SubjectAccessReview on a loopback-only address. Kueue metrics carry tenant information: ClusterQueue and LocalQueue names, namespaces, and configured custom label values from queues and Workloads (`CustomMetricLabels`). With `None`, anything in the manager Pod's network namespace can read them, and the manager logs a startup warning saying so (source: raw/kueue/pkg/config/metrics.go, pr-16035.md). Rule for reviewers: a new metric label sourced from a tenant object is data that sidecar scrapers will see.

## 2026-10-21 additions

None is a Kueue CVE ([[security#2026-10-21 wave: what the 20 new CVEs add]]).

| CVE | Product / versions | CWE, CVSS | Mechanism and Kueue rule |
| --- | --- | --- | --- |
| CVE-2026-110248 | Amazon SageMaker Python SDK v3 < 3.10.0, v2 < 2.257.3 | CWE-532, 5.3 | a failed `git clone` logged the subprocess error output **including the credential-bearing URL** to CloudWatch (source: CVE-2026-110248.md). Kueue rule: errors from client calls that may embed a URL with userinfo or a token (MultiKueue kubeconfig servers, ClusterProfile endpoints) must not be logged verbatim |
| CVE-2026-77564 | Talos Linux < 1.12.9 / 1.13.3 | CWE-312, 3.3 | `talosctl support` bundles included registry `auth` fields and sensitive file specs without redaction (source: CVE-2026-77564.md). Kueue analogue: debugging dumps (`pkg/debugger`, which dumps the cache and queues on SIGUSR2) must not include Secret contents or kubeconfigs |
| CVE-2026-113672 | Argo CD 0.9.0 until 3.3.15 / 3.4.10 / 3.5.4 | CWE-22, 9.9 | jsonnet `import`/`importstr`/`importbin` were not confined to the repo root, so a manifest could read `/proc/self/environ`, projected SA tokens and mounted keys and return them in a ConfigMap; `importstr /dev/zero` exhausted memory (source: CVE-2026-113672.md). See [[security-injection-and-input-validation]] |
| CVE-2026-113709 | Argo CD 2.1.0 until 3.3.15 / 3.4.10 / 3.5.4 | CWE-829, 9.9 | with `--enable-helm`, a repository-controlled `helmGlobals.configHome` made Helm load a downloader plugin from the repo and run it in the repo-server, with access to repository credentials (source: CVE-2026-113709.md) |
| CVE-2026-65172 | NVIDIA AIStore | CWE-862, 8.6 | unauthenticated ETL management API (source: CVE-2026-65172.md); see [[security-authn-authz]] |
| CVE-2026-77934 | Coze Studio < 0.5.0 | CWE-1188, 8.8 | workflow code nodes ran in an unsandboxed `python3` subprocess; a regex import filter was bypassed with `__import__('subprocess')`, exposing environment variables and model API keys (source: CVE-2026-77934.md). Denylist filters on code are not a sandbox |
| CVE-2026-87354 | Oracle TimesTen In-Memory Database Kubernetes Operator 22.1-22.1.40.0, 26.1-26.1.1.2.0 | no CWE, 4.3 | low-privileged network read of a subset of data; no mechanism published (source: CVE-2026-87354.md). Low signal |

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[metrics]]
- [[visibility-api]]
- [[dashboard]]
- [[multikueue]]
