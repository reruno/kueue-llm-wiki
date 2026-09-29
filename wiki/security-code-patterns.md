# Security Code Patterns (review checklist)

**Summary**: Master checklist of code patterns reviewers should flag, distilled from the `Security Code Patterns` section of every CVE in `raw/cve/`. Grouped by category and mapped to CWE.

**Sources**: `raw/cve/CVE-*.md` (749 entries). Pattern text is taken verbatim from the CVE files where the same checklist repeats per category.

**Last updated**: 2026-09-29

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
| CWE-200 | Sensitive info exposure | [[security-information-disclosure]] |
| CWE-269 | Improper privilege management | [[security-authn-authz]] |
| CWE-276 | Incorrect default permissions | [[security-authn-authz]] |
| CWE-23 | Relative path traversal (Flux source-controller, Fleet) | [[security-injection-and-input-validation]] |
| CWE-250 | Execution with unnecessary privileges (CRI-O, Strimzi) | [[security-authn-authz]] |
| CWE-284 | Improper access control | [[security-authn-authz]] |
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

## Related pages

- [[security]]
- [[security-best-practices]]
- [[code-quality]]
