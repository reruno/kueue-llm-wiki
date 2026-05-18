# Security — Best Practices Checklist for Kueue

**Summary**: Actionable checklist a Kueue contributor or reviewer can apply to a PR. Distilled from the `Mitigation` sections of `raw/cve/` and adapted to Kueue's code shape (controller-runtime, webhooks, scheduler cache).

**Sources**: `raw/cve/CVE-*.md` mitigation blocks (which repeat per category); the category pages [[security-denial-of-service]], [[security-authn-authz]], [[security-information-disclosure]], [[security-injection-and-input-validation]], [[security-supply-chain]]; [[code-quality]] for the project's existing review bar.

**Last updated**: 2026-05-18

---

## Pre-flight checklist (paste into PR review)

### Input handling

- [ ] Every field a user can set on a Kueue CR has webhook validation (length, regex, parse). New optional fields default safely.
- [ ] Reconciler code does *not* re-parse fields that the webhook already validated — but does guard nil-checked optional fields.
- [ ] No `fmt.Sprintf` building YAML/JSON. Marshal a typed struct.
- [ ] No string concatenation building label selectors, field paths, or URLs from user data. Use the typed client and `labels.SelectorFromSet`.
- [ ] No `os/exec`, no `http.Get` to user-supplied URLs, no file path from user-supplied names.

### Resource bounds

- [ ] Every outbound API call has a `context.WithTimeout` deadline (or inherits one from the reconcile context bounded by the manager).
- [ ] Every loop over a user-supplied slice (`PodSets`, `ResourceGroups`, `Flavors`, cohort children) has a cap or a documented invariant from the webhook.
- [ ] No `make([]T, n)` where `n` comes from user data without a sanity cap.
- [ ] New metrics have bounded label cardinality — no `workload_name`, no `pod_name`, no annotation values.

### Errors and logs

- [ ] `klog.InfoS` / `klog.ErrorS` with `klog.KObj(obj)` for identifiers, never `%+v` of a Kubernetes object.
- [ ] Log level discipline per [[code-quality]]: v=2 default; v=4 for verbose but bounded; v=6 for per-cycle debug only.
- [ ] No webhook response includes a full request body. Error messages are user-actionable but field-scoped.
- [ ] No event includes a secret-bearing field.

### Authentication and RBAC

- [ ] If a new CR or sub-resource is added, the bundled `config/rbac/role.yaml` change uses the minimum verbs needed. No wildcard verbs or resources.
- [ ] New webhooks register with `failurePolicy: Fail` unless there's a documented reason for `Ignore`.
- [ ] Any read of a `Secret` is via `resourceNames`, not a blanket verb on `secrets`.
- [ ] [[multikueue]] kubeconfigs: never logged, never echoed in status, never with `insecure-skip-tls-verify: true`.

### Nil-safety and crash resistance

- [ ] Every deref of an optional pointer field (`workload.Status.Admission`, `cq.Spec.Cohort`, optional sub-structs) is guarded.
- [ ] Reconcile errors that come from invalid CR content terminate the reconcile *without* re-enqueue. Status records the error; the controller does not crash-loop on bad input.
- [ ] Goroutines launched outside the controller-runtime workqueue have a deferred recover or a documented panic-policy.

### Supply chain

- [ ] No new direct dependency without a one-line justification in the PR body.
- [ ] No `replace` directive in `go.mod` without a tracked issue and target removal version.
- [ ] No `curl | sh` in any added script or Dockerfile.
- [ ] CI workflow additions pin actions to a SHA.

## Kueue-specific guardrails

These are not in the CVE corpus mitigation text but follow from Kueue's design:

1. **Status updates are at-least-once.** A bug that publishes secret-bearing data into status leaks every retry. Audit *before* you write to `.status`.
2. **The scheduler cache is per-cycle.** A panic in cache construction wedges the entire scheduling loop. The [[scheduler-internals|6-phase cycle]] should fail closed on a single bad object, not abort the whole snapshot. This is also a [[reviewer-gabesaba|gabesaba]] concern in [[code-quality]].
3. **Feature gates open new attack surface.** A feature gated to alpha should have its security-relevant assumptions documented. The [[feature-gates|feature-gate lifecycle]] doesn't currently require this; treat it as best practice.
4. **Integrations import third-party SDKs.** Each adapter in `pkg/controller/jobs/<framework>/` brings the framework's CRD types. Audit when those types contain credential-like fields (`RayCluster` head-node secret refs, `SparkApplication` driver env).
5. **The `kueue.x-k8s.io/` annotation namespace is reserved.** Anything reading or writing annotations should be specific about which keys it touches. Generic loops over `obj.Annotations` are a footgun.

## Suggested review commands

Run from a Kueue checkout against a PR branch:

```bash
# Logging hygiene
git grep -nE '%\+v|%#v' pkg/

# Forbidden surfaces
git grep -n 'os/exec\|InsecureSkipVerify' pkg/

# Bounded label-selector construction
git grep -nE 'fmt\.Sprintf.*kueue\.x-k8s\.io' pkg/

# Wildcard RBAC
grep -nE "verbs:\s*\['\*'\]|resources:\s*\['\*'\]" config/rbac/role.yaml

# Webhook failure policy
grep -n 'failurePolicy' config/webhook/manifests.yaml
```

These complement the [[testing|test pyramid]] — they don't replace integration tests but catch the patterns no test will exercise.

## When in doubt

The CVE corpus has no Kueue-specific entries as of 2026-05. Use the most-similar Kubernetes CVE as a template. Two starting points:

- For DoS-class concerns: `raw/cve/CVE-2019-11253.md` (API server YAML/JSON), `raw/cve/CVE-2022-39272.md` (Flux invalid `.spec.interval`).
- For RBAC concerns: `raw/cve/CVE-2018-16886.md` (etcd RBAC), `raw/cve/CVE-2019-11247.md` (cross-namespace CR access).

## Related pages

- [[security]]
- [[security-code-patterns]]
- [[security-denial-of-service]]
- [[security-authn-authz]]
- [[security-information-disclosure]]
- [[security-injection-and-input-validation]]
- [[security-supply-chain]]
- [[code-quality]]
