### Domain: Security

Security findings cover code patterns that could be exploited by an authenticated low-privileged tenant, a compromised neighbouring controller, or a malicious workload spec. Kueue is a privileged in-cluster controller that runs with broad watch permissions and sits in the admission path via webhooks — a single insecure pattern can crash-loop the cluster's batch-scheduling surface, leak tenant data, allow quota escape, or open arbitrary code execution. Diff Code MUST promote a secure architecture and MUST NOT introduce, re-enable, or weaken any of the rules below.

Rules:

1. **Input validation at trust boundaries** — every new user-settable field on a CR, webhook payload, label, or annotation MUST have explicit validation (length, regex, enum, parse) before it is used. Diff Code MUST NOT trust strings coming from `obj.Spec`, `obj.Annotations`, `obj.Labels`, or webhook request bodies. Reconciler code MUST still nil-check optional fields the webhook has already validated. Re-parsing untrusted input with permissive deserializers (`yaml.Unmarshal(..., interface{})`, `gob`, generic JSON into `map[string]interface{}`) is a hard violation (CWE-20, CWE-502).

2. **No injection from user-supplied strings** — Diff Code MUST NOT construct executable surfaces from untrusted data:
   - No `os/exec` / `exec.Command` with user-controlled arguments (CWE-78, CWE-94).
   - No `http.Get` / `http.NewRequest` to URLs built from CR fields (CWE-918 SSRF). Container image refs, init-container pull specs, and webhook target URLs count as untrusted.
   - No `fmt.Sprintf` building YAML, JSON, label selectors, field paths, or API server URLs from user input. Use typed marshalling and `labels.SelectorFromSet` / typed client builders.
   - No template rendering of annotation/label values server-side (CWE-94).
   - No SQL-like or query-language string concatenation (relevant if any external store is added).

3. **Path traversal** — file paths built from user-supplied names MUST go through `filepath.Clean` plus a prefix check against an allowlisted root. Diff Code MUST NOT follow symlinks in tenant-controlled directories, and MUST NOT extract archives without validating each entry stays within the destination root (zip-slip, CWE-22).

4. **Resource bounds / DoS resistance** — Diff Code MUST NOT enable uncontrolled resource consumption (CWE-400, CWE-770):
   - Every loop over a user-supplied slice (`PodSets`, `ResourceGroups`, `Flavors`, cohort children, admission checks) MUST have a documented webhook-enforced cap or an explicit length check.
   - `make([]T, n)` / `make(map[K]V, n)` where `n` comes from user data MUST have a sanity cap.
   - Every outbound API call or external HTTP call MUST have a `context.WithTimeout` (or inherit a bounded reconcile context).
   - Invalid `.spec.interval`-style fields MUST NOT be able to wedge the reconciler for the entire kind (CVE-2022-39272 pattern). Reconcile errors caused by invalid CR content MUST terminate without infinite re-enqueue; the failure goes to status, not a crash-loop.
   - New metrics MUST have bounded label cardinality — no `workload_name`, `pod_name`, namespace+name composites, or annotation values as label values (DoS via cardinality explosion).

5. **Nil-safety and crash resistance** — every deref of an optional pointer field reachable from a malformed CR (`Workload.Status.Admission`, `ClusterQueue.Spec.Cohort`, optional sub-structs, slice elements) MUST be guarded (CWE-476). A panic in scheduler cache construction or webhook handling wedges the entire scheduling loop and is treated as a high-severity finding. Goroutines launched outside the controller-runtime workqueue MUST have a deferred `recover()` or a documented panic policy.

6. **AuthN / AuthZ discipline** — Diff Code MUST NOT relax authentication or authorization:
   - No webhook handler that skips token validation or trusts `X-Forwarded-For` / `X-Remote-User` (CWE-287, CWE-306).
   - New admission webhooks MUST register with `failurePolicy: Fail` unless an explicit, documented reason is given for `Ignore` (CWE-352-class bypass).
   - Privileged operations (cross-namespace reads, secret reads, impersonation) MUST be preceded by a `SubjectAccessReview` when acting on behalf of a tenant.
   - No new ClusterRole with wildcard verbs (`*`) or resources (`*`); new RBAC MUST use the minimum verbs needed and prefer `RoleBinding` over `ClusterRoleBinding` when namespace scope suffices (CWE-269, CWE-862, CWE-863).
   - Reads of `Secret` MUST be scoped via `resourceNames`, never a blanket verb on `secrets` cluster-wide.
   - Diff Code MUST NOT set `HostPID`, `HostNetwork`, `HostIPC`, `privileged: true`, `allowPrivilegeEscalation: true`, or mount sensitive host paths (`/etc/kubernetes`, `/var/run/docker.sock`). `runAsNonRoot: true` MUST be preserved.

7. **Information disclosure** — Diff Code MUST NOT leak secrets, internal state, or cross-tenant data (CWE-200, CWE-522, CWE-532, CWE-552):
   - No logging of full Kubernetes objects (`%+v`, `%#v` of a CR). Use `klog.KObj(obj)` for identifiers and structured key/value pairs for the rest.
   - No webhook response, event, or status field that echoes a request body, stack trace, or credential-bearing field.
   - No persistence of credentials or tokens in annotations, labels, env vars, or status — credentials live in mounted Secrets.
   - [[multikueue]] kubeconfigs MUST NEVER be logged, echoed in status, or written with `insecure-skip-tls-verify: true`.
   - Visibility-API and metrics endpoints MUST scope results by tenant; a new query MUST NOT widen visibility past the caller's namespace/queue.
   - Status updates are at-least-once: audit before writing anything to `.status`. A secret-bearing status field leaks on every retry.

8. **Supply chain hygiene** — Diff Code MUST NOT weaken supply-chain controls (CWE-295, CWE-494):
   - No image references without a digest pin (`image: foo:latest` is a violation; pin to `@sha256:...`).
   - No `InsecureSkipVerify: true`, no TLS verification bypass, no `--insecure` flags.
   - No `replace` directive in `go.mod` without a tracked issue and a target removal version.
   - No `curl | sh`, no `wget | bash`, no fetching scripts from a URL inside a Dockerfile or Makefile.
   - New GitHub Actions and other CI workflow steps MUST pin third-party actions to a commit SHA, not a moving tag.
   - New direct dependencies require a one-line justification.

9. **Annotation/label namespace discipline** — the `kueue.x-k8s.io/` annotation/label namespace is reserved. Diff Code MUST be specific about which keys it reads or writes. Generic loops over `obj.Annotations` that copy, forward, or echo values are a footgun (allows tenant injection of reserved keys, leakage of operator-set values across boundaries). Forwarding annotations from one CR to another MUST go through an explicit allowlist.

10. **Feature-gate security posture** — when Diff Code adds behavior behind a [[feature-gates|feature gate]], the security-relevant assumptions of the gated path MUST hold both when the gate is on and when it is off. Diff Code MUST NOT use a feature gate to ship a path that would be insecure if accidentally enabled. New alpha gates with new attack surface SHOULD note the assumption in a code comment near the gate check.

11. **Integration adapter trust boundary** — each adapter in `pkg/controller/jobs/<framework>/` imports third-party CRD types. Diff Code that newly reads credential-like fields from an external CRD (`RayCluster` head-node secret refs, `SparkApplication` driver env, JobSet pod template env) MUST treat those fields as untrusted: validate before forwarding, never log, never copy into Kueue-owned status.

12. **Webhook safety** — Diff Code that adds or modifies validating/mutating webhooks MUST NOT loosen `failurePolicy` to `Ignore`, MUST NOT shorten `timeoutSeconds` below the existing default without justification, and MUST NOT add a webhook path that bypasses TLS verification. Mutating webhooks MUST be idempotent — non-idempotent mutators are both a correctness and a security risk (admission retry storms).