# Security — Information Disclosure

**Summary**: Patterns from the 110 Information Disclosure CVEs in `raw/cve/`. Covers logging hygiene, error-response content, [[metrics]] label cardinality (as a covert channel), [[visibility-api]] cross-tenant exposure, and credential handling.

**Sources**: `raw/cve/` — representative entries `CVE-2019-1002101.md` (kubectl cp path traversal also exposes file contents), `CVE-2020-8554.md` (man-in-the-middle via ExternalIP), `CVE-2020-8563.md` (sensitive info in logs), `CVE-2021-25741.md` (subpath symlink), CWE-200/CWE-532/CWE-522/CWE-552 entries broadly.

**Last updated**: 2026-05-18

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
- The [[dashboard|KueueViz UI]] aggregates state across queues — its RBAC must mirror the visibility-api's.

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

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[metrics]]
- [[visibility-api]]
- [[dashboard]]
- [[multikueue]]
