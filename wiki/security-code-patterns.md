# Security Code Patterns (review checklist)

**Summary**: Master checklist of code patterns reviewers should flag, distilled from the `Security Code Patterns` section of every CVE in `raw/cve/`. Grouped by category and mapped to CWE.

**Sources**: `raw/cve/CVE-*.md` (855 entries); 2026-10-28 additions `CVE-2026-102649.md`, `CVE-2026-114636.md`, `CVE-2026-114638.md`, `CVE-2026-114640.md`, `CVE-2026-115356.md`, pr-17207.md, pr-14142.md; 2026-10 additions `CVE-2026-26287.md`, `CVE-2026-92393.md`, `CVE-2026-101919.md`, `CVE-2026-106487.md`, `CVE-2026-106563.md`, `CVE-2026-7767.md`, `CVE-2026-86671.md`, `CVE-2026-105216.md`, `CVE-2026-105223.md`, `CVE-2026-109358.md`, `CVE-2026-107446.md`; 2026-10-21 additions `CVE-2026-113727.md`, `CVE-2026-113708.md`, `CVE-2026-77524.md`, `CVE-2026-53999.md`, `CVE-2026-110248.md`, `CVE-2026-47218.md`; Kueue fixes pr-17143.md, pr-17249.md, pr-17246.md, pr-17088.md, pr-16035.md; Kueue `pr-16379.md`. Pattern text is taken verbatim from the CVE files where the same checklist repeats per category. 2026-11-24 additions: CVE-2026-122310.md, CVE-2026-62284.md, CVE-2026-120091.md, CVE-2026-121374.md, CVE-2026-63121.md, CVE-2026-88982.md, CVE-2026-123810.md, CVE-2026-97373.md, CVE-2026-120307.md, CVE-2026-126643.md.

**Last updated**: 2026-11-24

---

This page is the single-pane reference. The category pages ([[security-denial-of-service]], [[security-authn-authz]], etc.) expand each pattern with Kueue context, examples, and concrete file references where applicable.

## Denial of Service (CWE-400, CWE-770, CWE-476, CWE-789, CWE-1284)

- Unbounded loops iterating over user-supplied input.
- Missing context timeouts (`context.WithTimeout`) on API calls.
- Large allocations proportional to untrusted user input.
- Missing `LimitRanger` or `ResourceQuota` enforcement before admit.
- Workloads admitted without CPU/memory limits set.
- Nil-pointer paths reachable from a malformed CR (CWE-476): always pre-validate referenced objects exist before deref.
- Invalid `.spec.interval` / `.spec.timeout` values that halt the reconciler for the entire kind (the Flux CVE-2022-39272 class).

→ See [[security-denial-of-service]].

## Authentication Bypass (CWE-287, CWE-306, CWE-352)

- Webhook handlers that skip token validation on certain HTTP methods.
- Missing `SubjectAccessReview` calls before privileged operations.
- Trusting `X-Forwarded-For` or `X-Remote-User` headers without validation.
- Admission webhooks with `failurePolicy: Ignore` for security-critical checks.

→ See [[security-authn-authz]].

## RBAC Misconfiguration & Privilege Escalation (CWE-269, CWE-266, CWE-276, CWE-284, CWE-285, CWE-862, CWE-863)

- ClusterRoles with wildcard verbs (`*`) or resources (`*`).
- Roles binding `cluster-admin` to service accounts used by controllers.
- Missing namespace scoping — using ClusterRoleBinding where RoleBinding suffices.
- Kueue controller ServiceAccount with `get/list/watch` on Secrets cluster-wide.
- Functions that mutate ServiceAccount tokens or pod security contexts.
- Missing `securityContext.runAsNonRoot` or `allowPrivilegeEscalation: false`.
- `HostPID` / `HostNetwork` / `HostIPC` set to `true`.
- Volumes that mount sensitive host paths (`/etc/kubernetes`, `/var/run/docker.sock`).

→ See [[security-authn-authz]].

## Information Disclosure (CWE-200, CWE-532, CWE-522, CWE-552)

- Logging objects that may contain secrets (tokens, passwords, keys).
- Error responses that include internal stack traces.
- Listing secrets across namespaces with a ClusterRole.
- Storing sensitive values in annotations or labels (readable by all tenants).
- Persisting credentials in env vars instead of mounted Secrets.
- Including request body / object contents in `klog.Errorf` or webhook responses.

→ See [[security-information-disclosure]].

## Injection & Input Validation (CWE-20, CWE-74, CWE-77, CWE-78, CWE-89, CWE-94, CWE-502, CWE-918)

- Building API server URLs from user-controlled namespace/name fields.
- SSRF via container image URLs or init-container pull specs (CWE-918).
- Using `fmt.Sprintf` to construct YAML/JSON payloads from untrusted input.
- Executing user-supplied strings via `exec.Command` without allowlist (CWE-78).
- Template injection in labels/annotations rendered server-side (CWE-94).
- Unsafe deserialization of untrusted data with `gob`, `yaml.Unmarshal(..., interface{})`, etc. (CWE-502).
- SQL-like queries built by string concatenation (relevant if any external store is added).

→ See [[security-injection-and-input-validation]].

## Path Traversal (CWE-22, CWE-61, CWE-363)

- File paths constructed from user-supplied names without `filepath.Clean` + prefix check.
- Symlink-following file reads in a tenant-controlled directory.
- ZIP/TAR extraction without validating that entry paths stay inside the destination root (the "zip-slip" pattern, CWE-22).

→ See [[security-injection-and-input-validation]] (path traversal lives there since the mitigation pattern is identical to input validation).

## Code Execution (CWE-78, CWE-94, CWE-502)

- Executing user-supplied strings via `exec.Command` without allowlist.
- Template injection in labels/annotations rendered server-side.
- Loading user-controlled Go plugins, WASM, or scripts at runtime.
- Deserializing untrusted YAML into `interface{}` with a permissive scheme.

→ See [[security-injection-and-input-validation]].

## Supply Chain (CWE-295, CWE-494)

- Image references without digest pinning (`image: foo:latest`).
- Missing image signature verification before admission.
- `go.mod`/`go.sum` changes that don't go through review.
- Pulling build-time scripts from a URL in `Dockerfile` or Makefile.

→ See [[security-supply-chain]].

## CWE quick index

| CWE | Class | Page |
| --- | --- | --- |
| CWE-20 | Improper input validation | [[security-injection-and-input-validation]] |
| CWE-22 | Path traversal | [[security-injection-and-input-validation]] |
| CWE-78 | OS command injection | [[security-injection-and-input-validation]] |
| CWE-79 | XSS (relevant to [[dashboard]]) | [[security-injection-and-input-validation]] |
| CWE-94 | Code injection | [[security-injection-and-input-validation]] |
| CWE-190 | Integer overflow in a length field (containerd overlaybd) | [[security-denial-of-service]] |
| CWE-200 | Sensitive info exposure | [[security-information-disclosure]] |
| CWE-269 | Improper privilege management | [[security-authn-authz]] |
| CWE-276 | Incorrect default permissions | [[security-authn-authz]] |
| CWE-23 | Relative path traversal (Flux source-controller, Fleet) | [[security-injection-and-input-validation]] |
| CWE-250 | Execution with unnecessary privileges (CRI-O, Strimzi) | [[security-authn-authz]] |
| CWE-284 | Improper access control | [[security-authn-authz]] |
| CWE-441 | Confused deputy (ECK annotation refs, Backstage in-cluster identity fallback) | [[security-authn-authz]] |
| CWE-285 | Improper authorization | [[security-authn-authz]] |
| CWE-287 | Improper authentication | [[security-authn-authz]] |
| CWE-295 | Improper cert validation | [[security-supply-chain]] |
| CWE-306 | Missing authn for critical function | [[security-authn-authz]] |
| CWE-352 | CSRF | [[security-authn-authz]] |
| CWE-362 | Race condition (Envoy Gateway map, Omni SAML replay) | [[security-denial-of-service]] |
| CWE-400 | Uncontrolled resource consumption | [[security-denial-of-service]] |
| CWE-476 | Nil-pointer dereference | [[security-denial-of-service]] |
| CWE-502 | Deserialization of untrusted data | [[security-injection-and-input-validation]] |
| CWE-522 | Insufficiently protected credentials | [[security-information-disclosure]] |
| CWE-532 | Sensitive info in log files | [[security-information-disclosure]] |
| CWE-552 | Files/dirs accessible to outside parties | [[security-information-disclosure]] |
| CWE-601 | Open redirect | [[security-injection-and-input-validation]] |
| CWE-696 | Incorrect behaviour order (External Secrets flag cleared by later init) | [[security-code-patterns]] |
| CWE-732 | Incorrect permission on a critical file (Contrast world-writable containerd config) | [[security-supply-chain]] |
| CWE-639 | IDOR / user-controlled key (Traefik, Argo Workflows) | [[security-authn-authz]] |
| CWE-770 | Allocation without limits | [[security-denial-of-service]] |
| CWE-789 | Memory allocation with excessive size (Envoy Gateway) | [[security-denial-of-service]] |
| CWE-776 | XML entity expansion (billion laughs) | [[security-denial-of-service]] |
| CWE-862 | Missing authorization | [[security-authn-authz]] |
| CWE-863 | Incorrect authorization | [[security-authn-authz]] |
| CWE-918 | SSRF | [[security-injection-and-input-validation]] |

## Tenant-controlled identifiers as lookup keys (2026-09 additions)

A cluster of ecosystem CVEs in this corpus, and a matching set of Kueue fixes, share one shape: **a controller resolves an object using a string the tenant can write, without a second condition that the tenant cannot forge.**

| Pattern | Ecosystem CVE | Kueue counterpart |
|---|---|---|
| User-supplied field used as a cross-namespace primary key; a duplicate ID wedges or hijacks another tenant's object | `CVE-2026-15228` (Kong KIC — CA-certificate Secrets collected cluster-wide by label selector alone, primary key derived from a user-supplied field; duplicate IDs make Kong reject the whole config, halting ingress cluster-wide) | pod-group name adoption ([[pr-13960]]) |
| Namespace confusion — a namespaced name resolved in the wrong namespace, or compared without its namespace | `CVE-2026-65601` (Traefik — `extensionRef` resolved in the *backend Service*'s namespace instead of the HTTPRoute's, letting a route author bind a Middleware without a ReferenceGrant) | AFS LocalQueue identity ([[pr-14547]]) |
| Annotation-driven cross-namespace read performed with the controller's cluster-wide credentials (confused deputy) | `CVE-2026-72640` (ECK operator — a secret-reference list read from an annotation, namespace accepted unvalidated, so a namespace-scoped user copies any Secret in the cluster) | any Kueue annotation that names another object: `prebuilt-workload-name`, `pod-group-name`, MultiKueue kubeconfig Secret refs |
| Name-only delete without a UID precondition, hitting a recreated object | — | `kueuectl delete workload` ([[pr-14831]]) |
| CR-supplied endpoint dialled by the controller with no allow/deny list (SSRF to loopback / RFC1918 / `169.254.169.254`) | `CVE-2026-71208` (KubeSphere `addCluster` — `url.Parse` only, then `Discovery.ServerVersion` against the CRD-specified endpoint), `CVE-2026-73263` (Prowler — kubeconfig accepted from the connection test) | [[multikueue]] `MultiKueueCluster` kubeconfig Secrets |
| CR-supplied endpoint dialled with cluster object contents **in the request body** (SSRF becomes exfiltration) | `CVE-2025-15613` (Kyverno < 1.13.4 — a `(Cluster)Policy` author sets an external URL in `apiCall`/`service`; Service Call is documented as in-cluster but resolves external addresses too, and the policy context data sent along includes Secret contents) | any [[admission-check]] or webhook that POSTs Workload/PodSpec context to an endpoint named in a CR |
| CR field spliced into a connection string / command with inadequate quoting | `CVE-2026-53572` (KEDA `postgresql_scaler` — `escapePostgreConnectionParameter` quotes only literal spaces, so tabs/newlines/quotes forge extra key-value tokens and redirect the connection or disable TLS) | anywhere Kueue formats tenant labels/annotations into a URL or command |
| CR field naming a **local file** that the controller reads with its own identity | `CVE-2026-75889` (Grafana Alloy — `ServiceMonitor.bearerTokenFile` reads the projected ServiceAccount token and ships it to an attacker-controlled scrape endpoint) | validate any config path that comes from a CR, not just from the Configuration file |
| Unvalidated regex from an admin-writable config compiled with `MustCompile`, panicking the webhook | `CVE-2026-65834` (Capsule — `ForbiddenLabels.Regex` crashes the node admission webhook on every Node create/update) | Kueue's own `managedJobsNamespaceSelector` / label-selector parsing; see [[security-denial-of-service]] |
| A guard applied on one code path but not its sibling (incomplete fix) | `CVE-2026-65835` (Capsule — `NamespacedItems` had the cluster-scoped rejection guard; `RawItems`/`Generators` did not) | #13014 guarded `FindMatchingWorkloads` but not the earlier `finalize` path — exactly the gap [[pr-13960]] closed |

**Review rule that falls out of the table:** when a reconciler looks an object up, ask *who can write the key*. If the answer includes an unprivileged tenant, require a second condition that only Kueue stamps — an ownership marker such as `kueue.x-k8s.io/is-group-workload`, an owner-reference *shape* (controller vs non-controller), a UID, or a namespace qualification — and check that **every** path that reaches the lookup applies it, not just the obvious one.

## Guard-coverage and derived-identity patterns (2026-09-29 additions)

The 2026-09-29 data-collection added 67 CVEs (all non-Kueue operators, gateways and runtimes). They reinforce the lookup-key table above and add six patterns that are checkable by reading a diff:

| Pattern | Ecosystem CVE | What to check in Kueue code |
|---|---|---|
| Cluster-scoped object named by a bare namespaced name; a same-named CR elsewhere overwrites or deletes it | `CVE-2026-19274` (Instana Agent Operator, CWE-284, 9.6, versions 1.0.303-1.0.323) | any ClusterRole/Binding, webhook config or cluster-scoped CR created from a namespaced object needs namespace or UID in its name |
| Derived name that is **too specific**, splitting objects that must share a security decision | `CVE-2026-85596` (Traefik 3.7.0-3.7.10, TLS option named per Ingress, conflict falls back to no client auth, CWE-287, 9.8) | on a conflict, fail closed; do not fall back to a weaker default |
| Guard on one branch but not the sibling branch, RPC kind or operator | `CVE-2026-53718` (Envoy Gateway custom `backendRef` skipped `validateBackendNamespace`), `CVE-2026-53714` (unary RPC lacked the stream JWT interceptor), `CVE-2026-93991` (Argo `metadata.namespace!=` skipped access review), `CVE-2026-88877` (Traefik sibling redirect router) | enumerate every entry into a protected function, including negated selectors and each integration adapter |
| Validation that reads the wrong variable (`old` for `new`, labels for annotations) | `CVE-2026-61795`, `CVE-2026-61794` (Capsule 0.13.x, fixed 0.13.7) | validators need a table test for each field with valid-old/invalid-new |
| Webhook or policy rule that silently never matches (singular vs plural, wrong subresource) | `CVE-2026-55636` (Capsule `namespace/finalize` vs `namespaces/finalize`, 0.13.0-0.13.5) | integration test that proves each webhook rule fires; compare `+kubebuilder:webhook` markers with real resource names |
| Data structure invariant broken between sort and search | `CVE-2026-61672` (Capsule, `sort.SearchStrings` on a case-insensitively sorted list) | `slices.BinarySearchFunc` must use the same comparator as the sort; prefer a `sets.Set` |
| Operator writes RBAC from a CR field | `CVE-2026-55225` (Strimzi `watchedNamespace`, CWE-269, 8.0) | see [[security-authn-authz]] |
| Untrusted size fields used to allocate or iterate | `CVE-2026-53717` (tar `h.Size`), `CVE-2026-53716` (gzip), `CVE-2026-44778` (ELF `DescSize`) | see [[security-denial-of-service]] |
| Optional secret defaults to open | `CVE-2026-93539` (Fleet webhook receiver without a configured secret) | new receivers or endpoints default closed |
| Compound identifier verified on one half only | `CVE-2026-85781` (EFS CSI `volumeHandle` pairs an access point with a different filesystem, CWE-283, 8.7) | verify ownership of every component of a key before a destructive action |

**Extension of the review rule:** after finding *who can write the key*, ask *what does every sibling path do with the same key*. Four of the 2026-09 CVEs (Envoy Gateway x2, Argo, Traefik) are one guard missing from one branch. The Kueue-side instance remains #13014 versus [[pr-13960]].

## Ordering, update-path and fallback patterns (2026-10 additions)

The 26 CVEs added by the 2026-10 data-collection are all non-Kueue and none affects a Kueue dependency ([[security#2026-10 wave: what the 26 new CVEs add]]). They add these diff-checkable patterns:

| Pattern | Ecosystem CVE | What to check in Kueue code |
|---|---|---|
| A security flag is set, then **reset by a later initialisation or defaulting step**, so the check silently never runs | `CVE-2026-26287` (External Secrets Operator 0.10.0 to before 1.3.2, CWE-696, 7.1: `webhook` generator init order cleared `EnforceLabels` after it was set, skipping the `external-secrets.io/type=webhook` label check) | Configuration defaulting (`SetDefaults_*`) must not overwrite a value the admin set. Feature-gate and integration setup that runs in several phases needs a test that asserts the final state, not the state after the first phase |
| Check enforced on CREATE, missing on UPDATE | `CVE-2026-92393` (YuniKorn: queue and user annotation re-written on UPDATE) | every `ValidateCreate` rule on a routing field has a `ValidateUpdate` twin; "managed?" decided from old **or** new (Kueue #13293, see [[security-authn-authz]]) |
| A configuration format that can execute code is copied from a tenant into a privileged context | `CVE-2026-101919` (HyperShift kubeconfig `exec` plugin) | kubeconfigs, Helm values or templates read from Secrets go through an allow-list validator; MultiKueue's `validateKubeconfig` is the model |
| An unsupported auth mode falls back to the controller's own identity | `CVE-2026-106487` (Backstage Kubernetes backend) | unsupported credential source is an error; no `rest.InClusterConfig()` fallback |
| A deprecated or alternate endpoint skips validation that the current one applies | `CVE-2026-106563` (Backstage deprecated services endpoint), `CVE-2026-106561` (masking bypass) | every served API version and every handler for the same data applies the same authz and redaction (relevant to [[visibility-api]] and [[dashboard]]) |
| A credential-bearing HTTP client follows a redirect, or accepts any URL scheme | `CVE-2026-7767` (GitLab Kubernetes proxy), `CVE-2026-86671` (Eclipse Che `file://`) | custom HTTP clients set `CheckRedirect` to stop or same-host-only; URLs from config or CRs are limited to `https` and validated hosts |
| Secure transport is **off by default**, or off when the CA is missing | `CVE-2026-105216` (go-micro TLS helper `InsecureSkipVerify: true` by default), `CVE-2026-105223` (maclof kubernetes-client skipped verification when `certificate-authority-data` was absent) | keep the `InsecureSkipVerify` grep in [[security-supply-chain]]; missing CA means system roots or refuse |
| Privileged component writes files world-writable | `CVE-2026-109358` (Contrast node installer wrote the containerd config `0666`) | any `os.WriteFile`/`MkdirAll` uses `0600`/`0700` (or `0644` for non-secret), never `0666`/`0777` |
| A failed parse is represented by the **same value as "no restriction"** (`nil` selector, empty list), so an invalid rule silently widens scope | Kueue's own, no CVE: before v0.20.0, `NewLocalQueueMetricsConfig` discarded the parse error from `metrics.localQueueMetrics.localQueueSelector` and returned `nil`, which downstream treated as "no LocalQueue filtering". With `LocalQueueMetrics` on, an invalid selector (for example `operator: InvalidOp`) emitted LocalQueue metrics for **all** queues: wider monitoring scope and higher cardinality, with no error reported. Fixed in v0.20.0 by returning the error to callers, so the controller fails startup (ACTION REQUIRED: correct invalid selectors before upgrading) (source: pr-16379.md) | a parse or validation error is returned, never mapped to the zero value. Where `nil`/empty means "match everything", test that an invalid input is rejected rather than matching everything. Same fail-closed rule as the Traefik conflict fallback row above. See [[metrics]] |
| Length field from an untrusted binary format overflows | `CVE-2026-107446` (overlaybd `index_bytes`, CWE-190) | see [[security-denial-of-service]] |

## Identity, option and ownership patterns (2026-10-21 additions)

The 20 CVEs added by the 2026-10-21 data-collection are non-Kueue and none affects a Kueue dependency ([[security#2026-10-21 wave: what the 20 new CVEs add]]). Four of the rows below come from Kueue's own KueueViz fixes in the same window.

| Pattern | Example | What to check in Kueue code |
|---|---|---|
| A security mode compared with `==` against one "on" value, so any other string means "off" | Kueue KueueViz `KUEUEVIZ_AUTH_MODE` (pr-17143, issue-17142): `tokenreview` disabled authentication | security-relevant modes are validated enums; unknown values fail startup. `switch` with an explicit `default:` error, not `if mode == X` |
| A cache key built by joining strings with a delimiter that can occur in the strings | Kueue KueueViz SAR cache (pr-17249, issue-17248): `["a,b"]` and `["a","b"]` shared a decision | keys for identities or authz decisions use a structured or length-prefixed encoding (then hash); never `strings.Join` of tenant-controlled values. Sort copies, not the caller's slice |
| A response embeds data of a second kind that was never authorized | Kueue KueueViz `/ws/cohorts` ClusterQueue names (pr-17246); `/ws/namespaces` live updates without `watch` (pr-17088) | each kind contributing to a response has its own check; authorizer errors deny; streams need `watch`, snapshots need `list` |
| The authorized object differs from the modified object | `CVE-2026-113727` (OpenChoreo: labels in the body authorized, object loaded by URL path) | webhooks and handlers decide ownership from the **stored** object; `ValidateUpdate` compares old to new |
| An argv value from input is parsed as an option | `CVE-2026-113708` (Argo CD `git fetch` without `--`, `--upload-pack`) | `exec.Command` callers (only `kueuectl` passthrough today) and `hack/` scripts put `--` before positional input or reject a leading `-` |
| The controller's own token is sent to a tenant-chosen URL | `CVE-2026-77524` (KEDA Vault auth with the operator's SA token) | no CR field selects an endpoint that receives Kueue's in-cluster credentials |
| A tenant-writable status/marker annotation chooses a deletion target | `CVE-2026-53999` (Radius `radapp.io/status`) | Kueue-owned annotations read from tenant objects are cross-checked with an owner reference or UID before a destructive action |
| Credentials in subprocess or client error text are logged verbatim | `CVE-2026-110248` (SageMaker git clone error) | errors that may contain URLs with userinfo or tokens are wrapped or redacted before logging |
| Untrusted input read through the component's trusted-cache path | `CVE-2026-47218` (runwasi precompiled Wasm from an image layer) | annotations Kueue normally writes are validated on read, since tenants can set them too |
| An authentication opt-out is not confined to a safe listener | Kueue `metrics.accessControlMode: None` (pr-16035) is the positive model: Alpha gate, literal loopback IP and port required, HTTPS kept, startup warning | any new "auth off" switch is gated, validated against the bind address, and logged |

## Normalization, renewal and output-channel patterns (2026-10-28 additions)

The 8 CVEs added on 2026-10-28 are non-Kueue ([[security#2026-10-28 wave: what the 8 new CVEs add]]). Two rows below come from Kueue's own changes in the same window.

| Pattern | Example | What to check in Kueue code |
|---|---|---|
| Distinct names collapse to one key after **lossy normalization** (dot-to-dash, case-folding, truncation, hashing to a short suffix), and the merged key carries security config | `CVE-2026-114638` (Traefik merged client CAs of two `auth-tls-secret` names equal after dot-to-dash) | treat any derived name or key like a delimiter-joined key (pr-17249 above). When two inputs can map to one output, the consumer must not merge their permissions or quota. Typical places: generated Workload names, label-value sanitisation, metric label values |
| An optional secret or config value whose **empty value skips verification** | `CVE-2026-102649` (Burrito accepted unsigned webhooks when `webhookSecret` was empty) | an empty security setting is a validation error or means "deny". Compare with `KUEUEVIZ_AUTH_MODE` (pr-17143) and `metrics.accessControlMode` (pr-16035) |
| A renewal or refresh path that never re-checks the original credential | `CVE-2026-115356` (OpenBao renewed Kubernetes-auth tokens after the ServiceAccount was deleted) | long-lived KueueViz WebSockets re-run TokenReview every 30 s and close on error; new streaming endpoints must do the same. Authorization decided at connect time is not re-evaluated ([[security-authn-authz#Long-lived sessions must re-check the original credential]]) |
| An **informer or watch registered on behalf of a caller** without checking `watch` on that resource | Kueue KueueViz secondary informers (pr-17207, issue-17177) | every informer whose events reach a caller is authorized separately from the route's primary resource; an authorizer error drops the socket |
| A deploy-time control that is **additive** turned on by default | Kueue NetworkPolicies kept opt-in (pr-14142): default-on would widen users' stricter policies | additive controls (NetworkPolicy rules, aggregated RBAC, extra webhook rules) ship opt-in or are proven not to widen existing policy. Port-scoped rules are documented as defence in depth, not isolation |
| Client-supplied identity headers forwarded on an unauthenticated path | `CVE-2026-114640` (Traefik `Ssl-Client-Verify: SUCCESS` on the HTTP router) | KueueViz identity comes only from the bearer token's TokenReview; Gin `SetTrustedProxies(nil)` keeps `X-Forwarded-*` untrusted |

## Path, kubeconfig, normalization and cache-key patterns (2026-11-24 additions)

| Pattern | Example | Kueue check |
| --- | --- | --- |
| Validate a cleaned value, execute the raw one | `CVE-2026-122310` (Kyverno 1.19.1, CWE-436, 9.9, fixed 1.19.2): `context.apiCall.urlPath` was cleaned for validation, but the raw path went to the client, which drops `#fragment` and `?query`. `../` hidden behind `#` or `?` reached cluster-scoped endpoints with Kyverno's ServiceAccount (source: CVE-2026-122310.md) | Validate and use the same normalized value, or build requests with typed clients and `url.URL` fields instead of concatenated strings. Applies to any path built from CR fields, including MultiKueue remote object names |
| Parsed kubeconfig used without sanitising `rest.Config` | `CVE-2026-62284` (OSAC operator console-proxy): `clientcmd.RESTConfigFromKubeConfig` on a labelled Secret let `users[].user.exec` spawn a process when `rest.TransportFor` built the transport, and `clusters[].server` gave SSRF. The patch closed the exec path but not the SSRF path (source: CVE-2026-62284.md) | Already handled for MultiKueue by `validateKubeconfig`/`validateRestConfig` ([[security-authn-authz#Kubeconfigs from Secrets run code]]). The lesson is to also validate `server` against an allow-list and not to treat a partial fix as complete |
| Case-sensitive comparison of case-insensitive identifiers | `CVE-2026-63121` (Kubewarden `trusted-repos-policy`, CWE-178, fixed 2.1.2): registry hostnames compared case-sensitively against a reject list, so `Docker.IO` evaded a rule for `docker.io`. Allow-lists failed closed (source: CVE-2026-63121.md) | Lower-case DNS names (and compare with `strings.EqualFold`) before matching hostnames, label values that are DNS names, and image registries. Prefer allow-lists over reject-lists |
| Cache or dedup key omits the tenant | `CVE-2026-88982` (Kubeflow Pipelines cache, CWE-345/639, fixed 2.18.0): the key hashed template fields without the namespace, and a mutable annotation was trusted when publishing outputs (source: CVE-2026-88982.md) | Any cache, hash or dedup key in Kueue (workload equivalence hashes, admission-check state) must include namespace and not trust tenant-writable annotations. Related: role-hash fixes in [[security]] |
| Argument injection into a generated command line | `CVE-2026-121374` (Checkmk Kubernetes agent, CWE-88): node roles from a rule written to arbitrary files via option injection (source: CVE-2026-121374.md) | Values from a Kubernetes object (node role, label) are untrusted when put in argv; use `--` and validate against a label-value regex |
| Query language built by string interpolation | `CVE-2026-123810` (Dynatrace MCP server, CWE-89): entity names, `timeframe`, `clusterId` interpolated into DQL broke the "read-only" tool contract (source: CVE-2026-123810.md) | Never build selectors or queries by `fmt.Sprintf`; use `labels.Selector`/`fields.OneTermEqualSelector` and typed field selectors |
| Incomplete SSRF block-list | `CVE-2026-97373` (draw.io `/proxy`, CWE-918): the RFC 6598 range `100.64.0.0/10` was missed (source: CVE-2026-97373.md) | If Kueue ever fetches a user-supplied URL, resolve then check the IP (loopback, link-local, private, `100.64.0.0/10`, metadata) and pin the connection to the checked IP |
| `filepath.Join` after the prefix check | `CVE-2026-120307` (Beta9 worker, CWE-22/23/59, 9.9): `..` segments were cleaned after the mount prefix check, and absolute symlinks were followed against the host root. Fixed with `os.OpenRoot` (source: CVE-2026-120307.md) | Use `os.OpenRoot` (Go 1.24+) or `securejoin` for any path derived from tenant data, e.g. the MultiKueue kubeconfig directory check |
| Secret value copied into a derived object | `CVE-2026-126643` (AAP Gateway Operator, CWE-312): a Secret's value was written into a CR `spec`, readable without Secret permission (source: CVE-2026-126643.md) | Copy Secret *references*, never values, into CRs, annotations or status |

## Related pages

- [[security]]
- [[security-best-practices]]
- [[code-quality]]
