# Security — Authentication, Authorization, RBAC, and Privilege Escalation

**Summary**: Patterns from Authentication Bypass (34), RBAC Misconfiguration (13), Privilege Escalation (67), and Unauthorized Write Access (37) CVE categories. Covers Kueue's controller ServiceAccount, [[webhooks|webhook]] handlers, [[multikueue]] cross-cluster credentials, and tenant isolation between [[cluster-queue|ClusterQueues]].

**Sources**: `raw/cve/` — representative entries `CVE-2018-18264.md` (Kubernetes Dashboard auth bypass), `CVE-2018-16886.md` (etcd RBAC), `CVE-2019-3779.md` (privilege escalation), `CVE-2019-11247.md` (cross-namespace custom resource access), `CVE-2019-11249.md`, `CVE-2020-8559.md`, `CVE-2022-23524-26.md` (Helm SSRF/auth issues).

**Last updated**: 2026-09-01

---

## Why this matters for Kueue

Kueue runs as a single, privileged controller. Three boundaries must be enforced:

1. **API-server → Kueue webhook.** Validated mutually via TLS; the API server is trusted. Risk: a misconfigured webhook with `failurePolicy: Ignore` that silently passes mutation for security-critical fields.
2. **Kueue controller → tenant resources.** The controller ServiceAccount has broad read on workload kinds. RBAC scope matters because a compromised controller pod inherits its RBAC.
3. **Tenant → tenant inside Kueue's data model.** A namespace can reference any [[local-queue|LocalQueue]] in its own namespace, but [[cluster-queue|ClusterQueue]] is cluster-scoped. RBAC on LocalQueue + the `kueue.x-k8s.io/queue-name` label is the only tenant isolation; cross-tenant data leakage via shared cohort accounting is by design.

## Authentication Bypass (CWE-287, CWE-306, CWE-352)

Patterns from `raw/cve/` Authentication Bypass entries:

- **Webhook handlers that skip token validation on certain HTTP methods.** Kueue's webhooks are called only by the API server (mTLS), so this is low-risk *if* the webhook handler doesn't expose any other HTTP routes on the same listener. Verify the metrics port and webhook port are on separate listeners with separate auth.
- **Missing `SubjectAccessReview` (SAR) calls before privileged operations.** Kueue rarely performs operations on behalf of an end-user identity — most actions run as the controller SA. But the [[visibility-api]] and any future user-facing endpoint *must* SAR the caller before disclosing per-queue data; that surface today escapes traditional RBAC because it's served by Kueue, not the API server.
- **Trusting `X-Forwarded-For` / `X-Remote-User` headers without validation.** Relevant if a Kueue endpoint is fronted by a proxy. Strip and re-set these at the proxy; never trust them in handler code.
- **Admission webhooks with `failurePolicy: Ignore`.** Kueue's validating webhook is `failurePolicy: Fail` (correct). Any new mutating webhook added for an integration must not silently default to `Ignore`.

## RBAC Misconfiguration (CWE-284, CWE-862, CWE-863)

Patterns from `raw/cve/` RBAC entries:

- **ClusterRoles with wildcard verbs (`*`) or resources (`*`).** Kueue's `manager-role` should be enumerable: grep `config/rbac/role.yaml` for `verbs: ['*']` or `resources: ['*']` — neither is acceptable. Each integration adds only the verbs it needs.
- **Roles binding `cluster-admin` to service accounts used by controllers.** Never. Kueue's bundled installation uses a dedicated ClusterRole.
- **Missing namespace scoping** — using `ClusterRoleBinding` where `RoleBinding` suffices. Kueue's controller necessarily needs cluster-wide read on workload kinds (it watches cluster-wide), so most bindings are correctly cluster-scoped. But adapters or extension webhooks that operate per-namespace should prefer `RoleBinding`.
- **ClusterRole aggregation labels.** As of v0.18, each per-resource editor/viewer ClusterRole carries a unique label `rbac.kueue.x-k8s.io/role: <resource>-<access>` (e.g. `clusterqueue-viewer`, `clusterqueue-editor`) — [[pr-11205]]. This lets downstream operators build custom aggregated ClusterRoles by selecting Kueue roles on this label *without* relying on the upstream `rbac.authorization.k8s.io/aggregate-to-view`/`aggregate-to-admin` labels (which Kueue does not stamp on these roles, deliberately, so a "view all CRDs" role isn't forced on every install).
- **Kueue controller ServiceAccount with `get/list/watch` on Secrets cluster-wide.** Audit: Kueue itself should not need cluster-wide Secret access. [[multikueue]] does need read access to specific kubeconfig Secrets (the worker-cluster connection); restrict via resourceNames, not a blanket verb on `secrets`.

## Privilege Escalation (CWE-269, CWE-266, CWE-276)

The 53 PrivEsc CVEs largely target the kubelet/pod security boundary rather than controllers, but the controller-pattern checklist still applies:

- **Functions that mutate ServiceAccount tokens or pod security contexts.** Kueue *does* mutate `.spec.suspend` and inject scheduling gates (for [[integration-statefulset|StatefulSet]] and [[integration-plain-pod|plain Pods]]). It must never mutate `securityContext`, `serviceAccountName`, or `automountServiceAccountToken`. A change that adds such mutation is a security review blocker.
- **Missing `securityContext.runAsNonRoot` / `allowPrivilegeEscalation: false`.** These apply to Kueue's *own* deployment manifest. Verify in `config/manager/manager.yaml`.
- **`HostPID` / `HostNetwork` / `HostIPC` set to `true`.** Kueue's manager pod must have all three `false`.
- **Volumes that mount sensitive host paths** (`/etc/kubernetes`, `/var/run/docker.sock`). Kueue mounts no host paths.

## Unauthorized Write Access (CWE-863, CWE-285)

The 30 Unauthorized Write CVEs map mostly to the API server's authorization layer, but the principle for Kueue is:

- **Webhook mutations must not exceed the scope advertised.** A mutating webhook registered on `Workload` must not mutate fields the user doesn't expect — the spec must be precise.
- **Status updates from one tenant must not influence another tenant's quota.** This is a Kueue-design question, not a Go-code question, but reviewers should think about it whenever changing [[cache-architecture|the cache]] or [[admission|admission accounting]].
- **Cross-namespace reference chains** (LocalQueue → ClusterQueue is OK by design; but a tenant should never be able to *create* a ClusterQueue or LocalQueue in another namespace). RBAC enforces this; verify when bundled manifests change.

## MultiKueue-specific concerns

[[multikueue]] introduces a manager → worker auth boundary that does not exist in single-cluster Kueue:

- The manager holds long-lived kubeconfigs for each worker. These are Secrets in the manager cluster.
- A compromised manager has write access to every worker's Workload CRs and (depending on the kubeconfig) job specs.
- Mitigation: scope each kubeconfig's RBAC on the worker to *only* `kueue.x-k8s.io/workloads` + the gated job types in the configured namespaces. Avoid `cluster-admin` kubeconfigs even though they're operationally simpler.

## Mitigation pattern in CVE corpus

> Ensure every request handler validates the caller's identity via `SubjectAccessReview` or RBAC. Set admission webhooks to `failurePolicy: Fail`. Validate and strip forwarded-identity headers at the ingress layer. Enable audit logging for all API server requests. Apply least-privilege pod security standards: `allowPrivilegeEscalation: false`, `runAsNonRoot: true`, `readOnlyRootFilesystem: true`. Audit all ServiceAccount ClusterRoleBindings.

## Namespace confusion and confused-deputy patterns (2026 corpus additions)

Three shapes recur in the 2026 additions to `raw/cve/` and map directly onto Kueue's multi-tenant surface:

- **Namespace confusion.** `CVE-2026-65601` (Traefik, CWE-863): the Gateway API provider resolved `HTTPRoute...backendRefs[].filters[].extensionRef` in the *backend Service*'s namespace rather than the HTTPRoute's, so a route author holding a cross-namespace ReferenceGrant for the Service could bind a Middleware from that namespace without a grant for it. Kueue's own instance of this class was the [[admission-fair-sharing]] preemption ordering that compared LocalQueues by `spec.queueName` alone, treating `team-a/default` and `team-b/default` as one queue ([[pr-14547]]). **Rule: a namespaced name is only an identity together with its namespace.**
- **Confused deputy via annotation.** `CVE-2026-72640` (Elastic Cloud on Kubernetes, CWE-441): the operator read a list of Secret references from an **annotation** and accepted the namespace in each reference without checking it was authorized for the resource being reconciled, so a namespace-scoped user could make the operator use its cluster-wide Secret permissions to copy any Secret in the cluster into one they could read. Kueue has several annotations that name other objects (`prebuilt-workload-name`, `pod-group-name`, MultiKueue kubeconfig Secret references) and the controller ServiceAccount is cluster-wide — the same shape is available.
- **Tenant-reachable object hijack by name.** `CVE-2026-15228` (Kong KIC, CWE-400/862): CA-certificate Secrets were collected across all watched namespaces by label selector alone, with the primary key derived from a user-supplied field, so duplicate IDs made the gateway reject the entire configuration document and halted all ingress changes cluster-wide. Kueue's pod-group Workload adoption bug ([[pr-13960]]) is the same pattern with quota release as the payload; see [[security#The first confirmed instance in Kueue's own code]].

Two related RBAC-relevant entries: `CVE-2026-65835` (Capsule, CWE-269/863) is an **incomplete fix** — the cluster-scoped-resource rejection guard existed on one code path (`NamespacedItems`) but not on its siblings (`RawItems`, `Generators`) — which is precisely the shape of the pod-group gap that #13014 left and [[pr-13960]] closed. `CVE-2026-18608` and `CVE-2026-18951`/`CVE-2026-18982` are over-broad operator `ClusterRole`s in the Red Hat OpenShift AI training-operator stack; the mitigation is the same per-resource ClusterRole aggregation Kueue already uses (`rbac.kueue.x-k8s.io/role`).

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[webhooks]]
- [[multikueue]]
- [[visibility-api]]
