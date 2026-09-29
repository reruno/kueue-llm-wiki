# Security — Authentication, Authorization, RBAC, and Privilege Escalation

**Summary**: Patterns from Authentication Bypass (40), RBAC Misconfiguration (15), Privilege Escalation (70), and Unauthorized Write Access (38) CVE categories. Covers Kueue's controller ServiceAccount, [[webhooks|webhook]] handlers, [[multikueue]] cross-cluster credentials, and tenant isolation between [[cluster-queue|ClusterQueues]].

**Sources**: `raw/cve/` — representative entries `CVE-2018-18264.md` (Kubernetes Dashboard auth bypass), `CVE-2018-16886.md` (etcd RBAC), `CVE-2019-3779.md` (privilege escalation), `CVE-2019-11247.md` (cross-namespace custom resource access), `CVE-2019-11249.md`, `CVE-2020-8559.md`, `CVE-2022-23524-26.md` (Helm SSRF/auth issues); 2026-09 additions `CVE-2026-19274.md`, `CVE-2026-55225.md`, `CVE-2026-53718.md`, `CVE-2026-85594.md`, `CVE-2026-61682.md`, `CVE-2026-93991.md`, `CVE-2026-55636.md`, and others cited inline.

**Last updated**: 2026-09-29

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

## 2026-09 additions: operators that trust the CR author

Roughly two dozen operator and gateway CVEs added on 2026-09-29 share one shape: **a namespace-scoped tenant writes a CR, and the operator acts on it with cluster-wide credentials without re-checking that the author owns the target.** None affects Kueue; they are templates for what to check in the Kueue controller, [[multikueue]] and the integrations.

### Cluster-scoped objects named from a namespaced CR

| CVE | Product / versions | CWE, CVSS | Mechanism |
| --- | --- | --- | --- |
| CVE-2026-19274 | IBM Instana Agent Operator 1.0.303-1.0.323 | CWE-284, 9.6 Critical, `PR:L/S:C` | ClusterRoleBinding named only by the CR name; a same-named `InstanaAgent` in another namespace overwrites or deletes the victim's binding (source: CVE-2026-19274.md) |
| CVE-2026-85596 | Traefik 3.7.0-3.7.10, ingress-nginx provider | CWE-287, 9.8 | TLS option named `namespace-name` of the Ingress, so two Ingresses with identical host, CA Secret and mode produce a "conflict" and Traefik falls back to the default option with client auth off (source: CVE-2026-85596.md). A derived name that is too specific broke a security invariant that needed the *same* key |
| CVE-2026-19283 | Instana Agent Operator, same versions | CWE-863, 7.7 | Operator copies etcd mTLS client credentials from `openshift-etcd` into a destination namespace it never validated (source: CVE-2026-19283.md) |
| CVE-2026-78609 | Elastic Cloud on Kubernetes up to 3.5.0 | CWE-863, 5.4 | Namespace-limited actor gets its certificate into a trust bundle managed in another namespace (source: CVE-2026-78609.md) |
| CVE-2026-78600 | ECK up to 3.5.0 | CWE-459, 3.5 | Credentials persist after RBAC denied a cross-namespace association, so read access is retained (incomplete cleanup) (source: CVE-2026-78600.md) |

**Reviewer rules for Kueue:** (1) any cluster-scoped object Kueue creates from a namespaced object must include the namespace (or UID) in its name; (2) a name derived to *group* objects must use exactly the fields that define the security invariant; (3) when an authorization check denies a reference, the reconciler must also **undo** whatever was granted earlier (finalizers, Secrets, bindings) rather than only refuse the next step. Ties to [[security-code-patterns#Tenant-controlled identifiers as lookup keys (2026-09 additions)]].

### CR fields that widen the operator's RBAC or identity

- **Strimzi <= 1.0.0, CVE-2026-55225** (CWE-269/441/250, CVSS 8.0): `Kafka.spec.entityOperator.watchedNamespace` made the Cluster Operator create a Role with full Secret CRUD in the named namespace and bind it to a ServiceAccount in the attacker's namespace; the attacker mints a token and reads Secrets. **CVE-2026-55226** (CWE-269/272, 5.4): deploying only one of Topic/User Operator leaves the shared ServiceAccount with both components' RBAC (source: CVE-2026-55225.md, CVE-2026-55226.md).
- **Woodpecker 1.0.0-3.16.0, CVE-2026-61549** (CWE-269/862): a pipeline step's `serviceAccountName` was copied into the Pod spec without admin authorization, so anyone with repository Push runs under any ServiceAccount in the pipeline namespace (source: CVE-2026-61549.md). This is the same class as a Kueue-integrated Job setting `spec.template.spec.serviceAccountName`; Kueue does not gate it and must not be assumed to.
- **Gardener, CVE-2026-79767** (CWE-863, 5.5, fixed 1.142.6/1.143.3/1.144.2/1.145.0): the `manage-members` admission check compared only `User` subjects, so a project admin added `Group` or `ServiceAccount` subjects including `system:authenticated` (source: CVE-2026-79767.md).
- **Portworx Operator on OpenShift, CVE-2026-15140** (CWE-266, no CVSS): a namespace-scoped user could get broader access during initial provisioning (source: CVE-2026-15140.md).
- **CRI-O 1.34+, CVE-2026-92574** (CWE-250, 8.8): a restored checkpoint kept the checkpoint's credentials, capabilities, `no_new_privs` and seccomp instead of the destination pod's security context (source: CVE-2026-92574.md).

**Rules:** every ownership-sensitive change to a *list of subjects* must diff all subject kinds; least-privilege RBAC must be computed **per deployed component**, not per operator; and a security context must be re-applied after any restore or adoption path (relevant to Kueue's workload adoption and MultiKueue remote-object creation).

### Guards missing from a sibling branch or method

- **Envoy Gateway < 1.7.4 / 1.8.1, CVE-2026-53718** (CWE-862, 6.4): the custom `backendRef` branch in `internal/gatewayapi/route.go` skipped `validateBackendNamespace`, so a route bound a cross-namespace backend without a `ReferenceGrant`. **CVE-2026-53714** (CWE-306, 7.4): in GatewayNamespace mode the xDS gRPC server had a JWT stream interceptor but no unary interceptor, and the stream interceptor only authenticated `DeltaDiscoveryRequest` (source: CVE-2026-53718.md, CVE-2026-53714.md).
- **Traefik <= 3.7.11, CVE-2026-85594** (CWE-639, 9.8): `crossProviderNamespaces` was not enforced for the `service.middlewares` Service annotation. **CVE-2026-88877** (CWE-639, 9.8): an Ingress with an auth annotation plus `from-to-www-redirect` created a sibling router with only a non-terminal redirect middleware pointing at the same protected backend (source: CVE-2026-85594.md, CVE-2026-88877.md).
- **Argo Workflows 4.1.0-4.1.3, CVE-2026-93991** (CWE-639, 7.7): `ListArchivedWorkflows` skipped the cluster-scoped access review when the field selector used `metadata.namespace!=`, so a namespace-scoped lister read every other namespace (source: CVE-2026-93991.md).
- **Capsule 0.13.x, CVE-2026-55636** (CWE-863, 5.7): the webhook rule named `namespace/finalize` instead of the plural `namespaces/finalize`, so it never matched. **CVE-2026-61672** (CWE-697/863, 7.1, fixed 0.13.7): `sort.SearchStrings` used on a case-insensitively sorted list can miss a forbidden key (source: CVE-2026-55636.md, CVE-2026-61672.md).
- **Fleet, CVE-2026-93539** (CWE-306, 5.4, 0.16 before 0.16.2): a webhook receiver with no secret configured accepts requests and rewrites a `GitRepo`'s `pollingInterval` in any namespace (source: CVE-2026-93539.md).

**Rules:** enumerate every path to a protected operation (unary and stream RPCs, every backend kind, every operator such as `In`/`NotIn`/`!=`) and test the negated and sibling forms; webhook rules must use exact **plural resource names and subresources**; a webhook `rules` typo silently disables validation, so add an integration test that proves the webhook fires (see [[webhooks]]); never sort case-insensitively then binary-search with a byte-order comparator; and a receiver with an optional secret must default to closed.

### Identity headers, unauthenticated endpoints, replay

- **kcp < 0.31.4 / 0.32.2, CVE-2026-61682** (CWE-290/302/348, CVSS 9.9 Critical): the front-proxy forwarded inbound `X-Remote-User`, `X-Remote-Group` and `X-Remote-Extra-*` to shards, so any tenant sent `X-Remote-Group: system:masters` (source: CVE-2026-61682.md). Strip trusted identity headers at the edge, then set them from the authenticated identity.
- **Skipper routesrv < 0.27.13, CVE-2026-54246** (CWE-306, 5.7): `/routes` and shard endpoints serve cluster-wide control-plane data without authentication (source: CVE-2026-54246.md).
- **OpenCost < 1.121.0, CVE-2026-44300** (CWE-20/309, no CVSS): unauthenticated `POST /serviceKey` writes an attacker-supplied value into the GCP `key.json` (source: CVE-2026-44300.md).
- **Omni 1.6.x / 1.7.x, CVE-2026-45720** (CWE-294/367, 7.0): SAML assertion `Used` was checked and set in two separate state operations, so concurrent requests replay the same session token. Use compare-and-swap / `resourceVersion` conflict on single-use tokens (source: CVE-2026-45720.md).
- **Warpgate 0.23.0-0.27.3, CVE-2026-91164** (CWE-284/863, 4.3): API-token auth skipped the owning user's `allowed_ip_ranges` (source: CVE-2026-91164.md).
- **Envoy Gateway, CVE-2026-53715** (CWE-362, 5.3): see [[security-denial-of-service]].

Kueue has no header-based identity and no unauthenticated data endpoint beyond metrics; the check is that the [[visibility-api]] aggregated server delegates to the API server's authenticator and never reads `X-Remote-*` itself. Any future Kueue endpoint that mutates state on first-come semantics (single-use token, one-time approval) needs an optimistic-concurrency write.


## Related pages

- [[security]]
- [[security-code-patterns]]
- [[webhooks]]
- [[multikueue]]
- [[visibility-api]]
