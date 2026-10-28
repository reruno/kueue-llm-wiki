# Security — Authentication, Authorization, RBAC, and Privilege Escalation

**Summary**: Patterns from Authentication Bypass (42), RBAC Misconfiguration (15), Privilege Escalation (73), and Unauthorized Write Access (40) CVE categories. Covers Kueue's controller ServiceAccount, [[webhooks|webhook]] handlers, [[multikueue]] cross-cluster credentials, and tenant isolation between [[cluster-queue|ClusterQueues]].

**Sources**: `raw/cve/` — representative entries `CVE-2018-18264.md` (Kubernetes Dashboard auth bypass), `CVE-2018-16886.md` (etcd RBAC), `CVE-2019-3779.md` (privilege escalation), `CVE-2019-11247.md` (cross-namespace custom resource access), `CVE-2019-11249.md`, `CVE-2020-8559.md`, `CVE-2022-23524-26.md` (Helm SSRF/auth issues); 2026-09 additions `CVE-2026-19274.md`, `CVE-2026-55225.md`, `CVE-2026-53718.md`, `CVE-2026-85594.md`, `CVE-2026-61682.md`, `CVE-2026-93991.md`, `CVE-2026-55636.md`, and others cited inline; 2026-10 additions `CVE-2026-92393.md`, `CVE-2026-101919.md`, `CVE-2026-106487.md`, `CVE-2026-103413.md`, `CVE-2026-103546.md`, `CVE-2026-18533.md`, `CVE-2026-18537.md`, `CVE-2026-95837.md`; Kueue code `pkg/controller/jobframework/validation.go`, `pkg/controller/admissionchecks/multikueue/multikueuecluster.go`., raw/kueue/CHANGELOG/CHANGELOG-0.20.md; 2026-10-21 additions `CVE-2026-113727.md`, `CVE-2026-77524.md`, `CVE-2026-105311.md`, `CVE-2026-105312.md`, `CVE-2026-112778.md`, `CVE-2026-53999.md`, `CVE-2026-77459.md`, `CVE-2026-103314.md`, `CVE-2026-94197.md`, `CVE-2026-65162.md`, `CVE-2026-65172.md`; KueueViz fixes pr-17088.md, issue-17073.md, pr-17246.md, issue-17178.md, pr-17249.md, issue-17248.md, pr-17143.md, issue-17142.md; metrics access control pr-16035.md, pr-16535.md, issue-16029.md, `raw/kueue/pkg/config/metrics.go`, `raw/kueue/pkg/config/validation.go`

**Last updated**: 2026-10-28

---

## Why this matters for Kueue

Kueue runs as a single, privileged controller. Three boundaries must be enforced:

1. **API-server → Kueue webhook.** Validated mutually via TLS; the API server is trusted. Risk: a misconfigured webhook with `failurePolicy: Ignore` that silently passes mutation for security-critical fields.
2. **Kueue controller → tenant resources.** The controller ServiceAccount has broad read on workload kinds. RBAC scope matters because a compromised controller pod inherits its RBAC.
3. **Tenant → tenant inside Kueue's data model.** A namespace can reference any [[local-queue|LocalQueue]] in its own namespace, but [[cluster-queue|ClusterQueue]] is cluster-scoped. RBAC on LocalQueue + the `kueue.x-k8s.io/queue-name` label is the only tenant isolation; cross-tenant data leakage via shared cohort accounting is by design.

## Authentication Bypass (CWE-287, CWE-306, CWE-352)

Patterns from `raw/cve/` Authentication Bypass entries:

- **Webhook handlers that skip token validation on certain HTTP methods.** Kueue's webhooks are called only by the API server (mTLS), so this is low-risk *if* the webhook handler doesn't expose any other HTTP routes on the same listener. Verify the metrics port and webhook port are on separate listeners with separate auth.
- **Missing `SubjectAccessReview` (SAR) calls before privileged operations.** Kueue rarely performs operations on behalf of an end-user identity — most actions run as the controller SA. But the [[visibility-api]] and any future user-facing endpoint *must* SAR the caller before disclosing per-queue data; that surface today escapes traditional RBAC because it's served by Kueue, not the API server. **KueueViz does this since v0.20.0 (#13810, ACTION REQUIRED):** with authentication enabled, every API and WebSocket route runs a SubjectAccessReview for the caller (user, groups, UID, extra) via `middleware.RequireAuthorization` (`cmd/kueueviz/backend/middleware/auth.go`), with decisions cached in an LRU with separate allow and deny TTLs (`CacheTTL`/`NegativeCacheTTL`); the backend ServiceAccount needs `create` on `subjectaccessreviews` (source: CHANGELOG-0.20.md). Four follow-up fixes landed in October 2026 (`/ws/namespaces` watch gating, `/ws/cohorts` ClusterQueue names, SAR cache-key collisions, fail-open auth mode); see [[security-authn-authz#KueueViz fixes in this window: in-repo examples]] and [[dashboard]].
- **Trusting `X-Forwarded-For` / `X-Remote-User` headers without validation.** Relevant if a Kueue endpoint is fronted by a proxy. Strip and re-set these at the proxy; never trust them in handler code.
- **Admission webhooks with `failurePolicy: Ignore`.** Kueue's validating webhook is `failurePolicy: Fail` (correct). Any new mutating webhook added for an integration must not silently default to `Ignore`.

## RBAC Misconfiguration (CWE-284, CWE-862, CWE-863)

Patterns from `raw/cve/` RBAC entries:

- **ClusterRoles with wildcard verbs (`*`) or resources (`*`).** Kueue's `manager-role` should be enumerable: grep `config/components/rbac/role.yaml` for `verbs: ['*']` or `resources: ['*']` — neither is acceptable. Each integration adds only the verbs it needs.
- **Roles binding `cluster-admin` to service accounts used by controllers.** Never. Kueue's bundled installation uses a dedicated ClusterRole.
- **Missing namespace scoping** — using `ClusterRoleBinding` where `RoleBinding` suffices. Kueue's controller necessarily needs cluster-wide read on workload kinds (it watches cluster-wide), so most bindings are correctly cluster-scoped. But adapters or extension webhooks that operate per-namespace should prefer `RoleBinding`.
- **ClusterRole aggregation labels.** As of v0.18, each per-resource editor/viewer ClusterRole carries a unique label `rbac.kueue.x-k8s.io/role: <resource>-<access>` (e.g. `clusterqueue-viewer`, `clusterqueue-editor`) — [[pr-11205]]. This lets downstream operators build custom aggregated ClusterRoles by selecting Kueue roles on this label *without* relying on the upstream `rbac.authorization.k8s.io/aggregate-to-view`/`aggregate-to-admin` labels (Kueue also stamps `aggregate-to-view/edit/admin` on most namespaced viewer roles since v0.18, #10482; the per-role label lets operators aggregate more selectively).
- **Kueue controller ServiceAccount with `get/list/watch` on Secrets cluster-wide.** Audit: Kueue itself should not need cluster-wide Secret access. [[multikueue]] does need read access to specific kubeconfig Secrets (the worker-cluster connection); restrict via resourceNames, not a blanket verb on `secrets`.

## Privilege Escalation (CWE-269, CWE-266, CWE-276)

The 73 PrivEsc CVEs largely target the kubelet/pod security boundary rather than controllers, but the controller-pattern checklist still applies:

- **Functions that mutate ServiceAccount tokens or pod security contexts.** Kueue *does* mutate `.spec.suspend` and inject scheduling gates (for [[integration-statefulset|StatefulSet]] and [[integration-plain-pod|plain Pods]]). It must never mutate `securityContext`, `serviceAccountName`, or `automountServiceAccountToken`. A change that adds such mutation is a security review blocker.
- **Missing `securityContext.runAsNonRoot` / `allowPrivilegeEscalation: false`.** These apply to Kueue's *own* deployment manifest. Verify in `config/components/manager/manager.yaml`.
- **`HostPID` / `HostNetwork` / `HostIPC` set to `true`.** Kueue's manager pod must have all three `false`.
- **Volumes that mount sensitive host paths** (`/etc/kubernetes`, `/var/run/docker.sock`). Kueue mounts no host paths.

## Unauthorized Write Access (CWE-863, CWE-285)

The 40 Unauthorized Write CVEs map mostly to the API server's authorization layer, but the principle for Kueue is:

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


## 2026-10 additions: UPDATE-path gaps, kubeconfig trust and identity fallback

None of these is a Kueue CVE or affects a Kueue dependency; see [[security#2026-10 wave: what the 26 new CVEs add]].

### Checks enforced on CREATE but not on UPDATE

**Apache YuniKorn <= 1.9.0, CVE-2026-92393** (CWE-863, no CVSS, fixed 1.10.0): the admission controller enforced label and user-info annotation checks for CREATE of Deployments, ReplicaSets, StatefulSets, DaemonSets, Jobs and CronJobs, but not for UPDATE. One UPDATE could set an arbitrary user-info annotation and change the application ID, placing the workload in a queue the user may not use and side-stepping per-user quota tracking (source: CVE-2026-92393.md).

This is the scheduler-quota version of the "guard missing from a sibling method" rule, and Kueue has had the same shape:

- Kueue's job webhooks validate the `kueue.x-k8s.io/queue-name` label on update in `validateUpdateForQueueName` (`pkg/controller/jobframework/validation.go`): it is immutable while the job is unsuspended, a changed value on a suspended job is re-validated, and removing it is rejected in a namespace that has a default LocalQueue.
- RayJob/RayCluster/SparkApplication webhooks only validated an update when the *new* object was managed, so removing the queue-name label from a managed job skipped validation and left it running unmanaged. #13293 added `ShouldValidateRayOrSparkJobOnUpdate`, which also validates when the *old* object had a queue name, behind `ValidateRayAndSparkJobUpdates` (Beta, on by default since 0.18). See [[integration-rayjob]], [[integration-spark]] and [[webhooks]].
- Kueue derives no quota from a user-identity annotation. The tenant boundary is the namespace: a LocalQueue is namespaced and a ClusterQueue admits only namespaces matching its `namespaceSelector`, so changing the queue-name label can only reach LocalQueues in the job's own namespace.

**Rules:** every `ValidateCreate` check on a routing or identity field (queue name, priority class, prebuilt-workload name, pod-group name) needs a `ValidateUpdate` counterpart. An "is this object managed?" decision on update must look at old **or** new, not only new. Any future per-user quota must take the user from the admission request's `UserInfo`, never from an object label or annotation.

### Kubeconfigs from Secrets run code

**HyperShift operator, CVE-2026-101919** (CWE-20, 8.8): user-supplied kubeconfig Secrets were copied into the privileged control-plane namespace without sanitisation. A kubeconfig with an `exec` credential plugin then ran attacker-chosen commands inside the control plane when a downstream controller loaded it (source: CVE-2026-101919.md).

A kubeconfig is executable configuration, not data: `users[].exec`, `auth-provider`, `tokenFile` and `certificate-authority` paths all make the consuming process run a command or read a local file. Kueue's [[multikueue]] already blocks this class. Since #7439 (2025-10), `validateKubeconfig` and `validateRestConfig` in `multikueuecluster.go` reject, for kubeconfig-sourced `MultiKueueCluster`s:

- `tokenFile`, `bearerTokenFile`, and `certificate-authority` file paths (only `certificate-authority-data` is allowed)
- `insecure-skip-tls-verify`
- basic auth
- exec plugins and auth providers
- a server host that is neither an IP nor a valid DNS-1123 subdomain

A failed check sets the cluster's `Active` condition to false with reason `InsecureKubeConfig`. The one exception is the ClusterProfile path (`MultiKueueClusterProfile` gate), which allows exec providers because the credential plugins are configured by the Kueue operator rather than read from the Secret. Kubeconfigs loaded by `locationType: Path` are confined to `/etc/multikueue/kubeconfigs/` when `MultiKueueKubeConfigPathValidation` is on (Beta, on by default in 0.20). **Rule:** keep this validation for every new credential source, and never relax it to "warn only".

### Falling back to the controller's own identity

**Backstage `@backstage/plugin-kubernetes-backend` < 0.21.10, CVE-2026-106487** (CWE-441, 3.5): when a catalog-supplied cluster entity used an auth mode the backend did not support, the backend used its **local in-cluster identity** against the local API server, exposing resources readable by that ServiceAccount (source: CVE-2026-106487.md). **Rule:** an unsupported or missing credential configuration must be an error, never a fallback to `rest.InClusterConfig()`. Kueue's MultiKueue `loadClientConfig` returns a reason (`BadKubeConfig`, `InsecureKubeConfig`, `BadClusterProfile`, `BadRestConfig`) and has no in-cluster fallback. Keep it that way.

### Operators that apply tenant-authored manifests

- **Apache Camel Karavan 4.0.0 to before 4.22.1, CVE-2026-103413** (CWE-20, 8.8): on deployment, Karavan unmarshalled a project's `kubernetes.yaml` and applied every resource in it with its own ServiceAccount. It did not restrict kinds or pin the namespace, and it did not reject `hostNetwork`, `hostPID`, `hostIPC`, `hostPath`, host ports, privileged containers or added capabilities. Any authenticated user of any role could use it (source: CVE-2026-103413.md).
- **IBM Maximo Location Service for Esri 9.0-9.2, CVE-2026-18533 / CVE-2026-18537** (CWE-94, 6.5 / 8.7): an unsanitised container image reference from configuration was rendered into an operator template (source: CVE-2026-18533.md, CVE-2026-18537.md).
- **MongoDB Controllers for Kubernetes, CVE-2026-103546** (CWE-918, 4.3): Ops Manager backup configuration from the `OpsManager` CR was used for administrative actions without enough validation (source: CVE-2026-103546.md).

Kueue mapping: the [[multikueue]] manager re-creates the user's job object in the worker cluster with the worker kubeconfig's identity. The worker's Pod Security Admission and RBAC still apply. So what limits the kinds and namespaces Kueue can write remotely is the **worker kubeconfig's RBAC** (see "MultiKueue-specific concerns" above), not Kueue code. **Rule:** a controller that writes objects derived from tenant input must fix the namespace to the source object's namespace, allow-list the kinds, and never widen the pod security context.

### Restored state overrides the requested security context

**containerd 2.1.0 to before 2.2.7 / 2.3.4, CVE-2026-95837** (CWE-269, 7.8): CRI checkpoint restore let CRIU restore credentials, capabilities, `no_new_privs` and seccomp from checkpoint data instead of enforcing the destination `ContainerConfig`, while CRI status reported the requested config (source: CVE-2026-95837.md). This is the containerd twin of CRI-O CVE-2026-92574 above and strengthens the "re-apply security context after restore or adoption" rule. Kueue does not use checkpoint restore.

## KueueViz fixes in this window: in-repo examples

Four authorization bugs in the KueueViz backend (`cmd/kueueviz/backend/`) were fixed in October 2026. None is a CVE, and per-user authorization only exists on release-0.20 and main (#13810), so release-0.19 is not affected. Each is a concrete Kueue instance of a rule on this page (source: pr-17088.md, pr-17246.md, pr-17249.md, pr-17143.md; details and release map in [[dashboard#Authorization and startup fixes (2026-10)]]):

| Bug | Rule it illustrates |
|---|---|
| **Fail-open configuration.** Middleware was installed only when `KUEUEVIZ_AUTH_MODE == "TokenReview"`, so any typo (`tokenreview`, `Enabled`) started the backend with **no** authentication. Now an enum with `Disabled`/`TokenReview` and a startup error otherwise (pr-17143, issue-17142) | Security-relevant modes are closed enums. An unknown value is a startup error, never "feature off". Same family as the Backstage fallback above (CVE-2026-106487) |
| **Cache key built by joining with delimiters.** Groups and extra values were joined with `,`/`;`, so `["a,b"]` and `["a","b"]` produced the same SAR cache key and the second identity reused the first one's allow decision. Now SHA-256 over a length-prefixed encoding of username, UID, sorted groups and sorted extra (pr-17249, issue-17248) | A cache key that stands for an identity must be an injective encoding (length-prefixed or structured), then hashed. Sort only where order is semantically irrelevant, and on copies |
| **Secondary data in a response was not authorized.** `/ws/cohorts` returned every ClusterQueue name in each Cohort's `clusterQueues` field, though the sibling `/ws/cohort/:name` already checked `list clusterqueues`. Now omitted when denied **or when the check errors** (pr-17246, issue-17178) | Authorize every resource kind that contributes data to a response, not only the route's primary kind. An authorizer error is a deny |
| **Live stream without watch permission.** `/ws/namespaces` registered a LocalQueue informer for every caller. Now the initial snapshot is still filtered by per-namespace `list`, but the informer (live updates) needs cluster-wide `watch localqueues` (pr-17088, issue-17073) | `list` and `watch` are separate verbs. A long-lived stream needs `watch` on each source it streams |

Still open: the same informer-gating gap on other multi-resource WebSockets (issue-17177).

## Metrics listener: opting out of authentication (main, Alpha)

The metrics endpoint is protected by controller-runtime's `filters.WithAuthenticationAndAuthorization` (TokenReview + SubjectAccessReview on `/metrics`). pr-16035 (KEP-16029, fixes issue-16029, merged 2026-10-21, main only) adds `metrics.accessControlMode` to the v1beta2 Configuration (source: raw/kueue/apis/config/v1beta2/configuration_types.go, raw/kueue/pkg/config/metrics.go, raw/kueue/pkg/config/validation.go):

- `Delegated` (default) keeps TokenReview/SubjectAccessReview. `None` removes the filter, so any process that can reach the listener can scrape.
- Setting the field at all requires the Alpha `MetricsAccessControl` gate (0.21, off). With the gate off, an explicit value is a validation error (`requires the MetricsAccessControl feature gate`). With the gate on, an omitted value means `Delegated`, and any value other than the two is rejected.
- `None` requires `metrics.bindAddress` to be a **literal loopback IP with a port 1-65535** (`netip.ParseAddrPort`, `Addr().Unmap().IsLoopback()`; IPv4, IPv6 and IPv4-mapped accepted). Hostnames, wildcards, non-loopback IPs and port 0 fail validation. `bindAddress: "0"` (metrics off) skips the address check.
- HTTPS stays mandatory (`SecureServing: true`); only authentication and authorization are dropped. At startup the manager logs a `WARNING` that metrics may expose tenant information to other processes sharing the network namespace.

Threat-model note: loopback is not a tenant boundary. Every container in the manager Pod, node processes using `hostNetwork`, and anyone with `pods/exec` or `pods/portforward` on the manager can reach it. Metrics carry tenant data (queue names, namespaces, custom label values). Treat `None` as a decision to trust everything in the manager's network namespace (source: pr-16035.md, pr-16535.md). Client-certificate authentication was proposed as an alternative and is still open (issue-17432, pr-17459).

## 2026-10-21 additions: confused deputies, tenant URLs and authorizing the wrong object

The 20 CVEs added by the 2026-10-21 data-collection are all non-Kueue and none affects a Kueue dependency ([[security#2026-10-21 wave: what the 20 new CVEs add]]). New lessons for this page:

- **Authorize the object you will modify, not the one the client sent.** OpenChoreo 1.0.0 to before 1.0.6 / 1.1.7 / 1.2.5, CVE-2026-113727 (CWE-639, 7.4): the `PUT .../workflowruns/{runName}` route authorized against the project/component labels in the **request body** but loaded the stored object by the **URL path**. A caller allowed on one project named another run in the path, sent labels for a scope they controlled, and rewrote the victim's ownership labels; later checks then trusted those labels (source: CVE-2026-113727.md). Kueue mapping: webhook `ValidateUpdate` must compare old and new, and any check of "who owns this" must read the stored (old) object. Kueue's queue-name update rules already do this (see the CREATE/UPDATE section above).
- **Never send the controller's ServiceAccount token to a tenant-chosen endpoint.** KEDA <= 2.20.2, CVE-2026-77524 (CWE-269/918, 9.9): a namespace admin set `hashiCorpVault.address` to their own server and chose Kubernetes auth without a credential, so KEDA sent the **operator's** projected token as the Vault login; the earlier JWT-shape filter (CVE-2025-68476 fix) accepted it (source: CVE-2026-77524.md). Kueue sends credentials only to MultiKueue worker API servers named by admin-created `MultiKueueCluster` objects, using the kubeconfig's own credentials. Keep it that way: no CR field may make Kueue present its in-cluster token to a URL.
- **Confused deputy copying Secrets across namespaces.** StreamsHub Console operator, CVE-2026-105311 (CWE-441, 7.7): a Console CR field `credentials.kafkaUser.namespace` could name any namespace; the operator, holding cluster-wide Secret RBAC, copied that namespace's KafkaUser Secret into the attacker's namespace. **CVE-2026-105312** (CWE-269, 9.9): the same CR's `containers.api.spec.image` let a tenant run any image under a ServiceAccount with cluster-wide Strimzi rights (source: CVE-2026-105311.md, CVE-2026-105312.md). Rule: a namespaced CR may reference only its own namespace, and a CR field must never choose the image or the identity of a privileged Pod.
- **Cross-namespace references from annotations.** Traefik before 2.11.46 / 3.6.17 / 3.7.0, CVE-2026-112778 (CWE-862): Ingress and Service annotations could reference Middlewares, ServersTransports and TLSOptions in other namespaces, reusing another tenant's injected credentials or client certificates (source: CVE-2026-112778.md). Same rule as the earlier Traefik entry: a tenant-written annotation that names another object must be namespace-confined.
- **Trusting a status annotation the tenant can write.** Radius before 0.58.0, CVE-2026-53999 (CWE-20/441, 7.7): the controller deserialized the user-writable `radapp.io/status` annotation on a Deployment and used its resource ID as a **deletion target** without checking ownership, so a forged annotation plus `radapp.io/enabled: false` deleted another tenant's resource (source: CVE-2026-53999.md). Kueue analogue: Kueue reads its own annotations from tenant objects (`kueue.x-k8s.io/workload`, `pod-group-name`, `prebuilt-workload-name`, `role-hash`). Any such value used to find an object to delete, finish or release must be cross-checked against a Kueue-stamped owner reference or UID (see [[security#The first confirmed instance in Kueue's own code]]).
- **Policy checks applied on the normal path but not on a hook path.** Argo CD 2.10.0 until 3.3.15 / 3.4.10 / 3.5.4, CVE-2026-77459 (CWE-863, 9.9): PostDelete hooks were created without the AppProject destination and resource allow/deny checks used by ordinary sync (source: CVE-2026-77459.md). Another "guard missing from a sibling path" case.
- **Replay of single-use authentication artefacts.** Red Hat ACS, CVE-2026-103314 (CWE-294, 7.4): the SAML endpoint did not remember used assertion IDs, so one signed response minted many tokens (source: CVE-2026-103314.md). Same rule as Omni CVE-2026-45720 above.
- **Forwarded routing headers trusted by an auth subrequest.** F5 NGINX Ingress Controller, CVE-2026-94197 (CWE-290, 7.5): client-supplied `X-Forwarded-Prefix`, `X-Forwarded-URI`, `X-Original-URI` and `X-Forwarded-Method` reached the external-auth subrequest unsanitised (source: CVE-2026-94197.md). Relevant to a KueueViz deployment behind an auth proxy: the proxy must overwrite these headers.
- **Unauthenticated management API and caller-supplied PodSpec security fields.** NVIDIA AIStore: the ETL management API had no authorization (CVE-2026-65172, CWE-862, 8.6), and the legacy ETL PodSpec API accepted host-namespace and security-context settings from a remote caller (CVE-2026-65162, CWE-250, 10.0) (source: CVE-2026-65172.md, CVE-2026-65162.md). Kueue's podSet mutations (TAS node selectors, scheduling gates, tolerations from ResourceFlavors) come from admin-owned objects, never from a request field.

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[webhooks]]
- [[multikueue]]
- [[visibility-api]]
