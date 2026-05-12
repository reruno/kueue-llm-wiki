
# Code Quality in Kueue

**Summary**: The shared technical quality bar that Kueue reviewers enforce, synthesized across [[reviewer-mimowo|mimowo]], [[reviewer-tenzen-y|tenzen-y]], [[reviewer-gabesaba|gabesaba]], [[reviewer-mbobrovskyi|mbobrovskyi]], and [[reviewer-pbundyra|PBundyra]]. Use this page to predict what will block a PR and what will earn quick approval.

**Sources**: `raw/github/kubernetes-sigs__kueue/` PR review comments; `raw/kueue/CONTRIBUTING.md`; `raw/kueue/.golangci*.yaml`; `raw/kueue/Makefile-verify.mk`; `raw/kueue/pkg/features/kube_features.go`; the individual reviewer pages.

**Last updated**: 2026-05-12

---

## What matters most

Across hundreds of review comments, six concerns dominate:

1. **Upgrade safety** — code that affects in-flight workloads or finalizers stays for 2 releases
2. **Integration tests** — every new code path needs one; feature-gate off-state must be covered
3. **Semantic naming** — feature gates, API fields, and variables must match what they actually mean
4. **API versioning rules** — beta fields don't disappear in-place; deprecate and remove on promotion
5. **One concern per PR** — cleanup + bugfix gets split; squashed commits before merge
6. **Release notes that describe the user-visible scenario** — for any production-relevant fix

These are blockers, not preferences. The remaining sections expand each one with quoted reviewer guidance.

---

## 1. Upgrade safety and backwards compatibility

**Rule**: code that any pre-existing cluster object depends on must stay for two release cycles.

From [[reviewer-mimowo|mimowo]] on pr-8530:

> "we cannot remove this code in the PR, because upgrading Kueue will not work — nothing will remove the finalizers from pre-existing workloads. So we need to keep this code for 2 releases."

When the deprecated path is kept, the PR must include:

1. A `// TODO(#issue): drop this in v0.18` comment with the exact target version
2. A GitHub issue filed so it's not forgotten
3. The migration scenario explicitly tested (manual e2e on a live cluster, not just kind, for ownership-level changes — see pr-8341)

**Prefer API discovery over version gating.** From pr-4444 on ProvisioningRequest:

> "If v1 available, then use it, otherwise if v1beta1 available, then use it, otherwise fail."

REST mapper discovery is definitive; hard-coded Kubernetes version checks are fragile because of skewed installations (e.g., CA version ≠ K8s version).

---

## 2. Test coverage

### Integration tests are a hard requirement for new paths

From mimowo on pr-8186:

> "Please add a test, I think the same testing approach should work as in #7913."

And when the scenario is conditional, the reviewer will name the exact case to cover:

> "I would suggest to add more test case: 'when workload is evicted, but suspended, and the startTime is reset, restore node affinity'."

### Feature-gate off-state must be tested

From mimowo on pr-8151:

> "Oh, I think I also need to check with MultiKueueBatchJobWithManagedBy disabled."

### Flakiness must be proven absent

For timing-sensitive tests, mimowo asks for a local loop run before merge. From pr-9619:

> "could you run it in a loop locally to make sure it does not flake? I think 50 repeats should be enough."

### Manual e2e for ownership-level changes

When a change moves where a resource is managed (e.g., Workload ownership from RayCluster to RayJob), kind is not enough. From pr-8341:

> "I would like to ask you to perform a manual test e2e on a live cluster to check what will happen if there is a pre-existing RayJob at the moment of upgrade."

See also [[testing]], [[testing-integration]], [[testing-e2e]].

---

## 3. Naming conventions

### Feature gate names must match what they actually gate

From mimowo on pr-8530: a feature gate named `SkipFinalizersForServingWorkloads` was renamed to `SkipFinalizersForPodsSuspendedByParent` once it was discovered the check inside didn't match the original name. The PR title was updated too.

### API field symmetry

If `excludeResourcePrefixes` exists, a new complementary field should be `includeResourcePrefixes`, not something asymmetric.

### Builder/wrapper method conventions

`AddAnnotation(k, v)` was renamed to `Annotation(k, v)` to match the existing `Label` convention (pr-8082). Builder methods don't take an `Add` prefix.

### Variable names must reflect content

A set called `noMoreBorrowingCohorts` that might actually contain cohorts currently borrowing was renamed to `suspendBorrowingCohorts` to disambiguate intent.

### Required vs optional in API markers

From [[reviewer-pbundyra|PBundyra]] on pr-10244:

```suggestion
Mode AdmissionMode `json:"mode"`
```

A `+required` field must drop `omitempty`. Linter-clean is non-negotiable on CRDs.

---

## 4. API design and versioning

### API field removal requires version promotion

From PBundyra on pr-10244:

> "We should never remove API fields without a new API promotion. This goes against Kubernetes API practices for beta fields."

The lifecycle is: deprecate (mark in comments + add replacement field) → wait for the next API version → remove in the new version. **Never in-place.**

### Configuration API has no CEL

From mimowo on pr-8082:

> "Configuration API (non-CRD) does not generate CEL validation rules, so developers cannot rely on generated validation."

For Configuration API, write the validation in Go in the webhook.

### Feature-gated API fields need guard validation

From mimowo on pr-8082:

> "I think we should still make the validation, and allow for `EnableInTreeAutoscaling` only if `ElasticJobsViaWorkloadSlices` are enabled."

A field that only makes sense under a feature gate must be rejected at validation when the gate is off.

### Comments must match behavior

From mimowo on pr-10013:

> "Do we actually check they are unsuspended? I don't see that in code, maybe better to say 'The number of admitted Workloads that are active (i.e., not finished)'."

Aspirational comments are blocked. Update either the comment or the code.

---

## 5. PR scope and hygiene

### One concern per PR

From mimowo on pr-6297:

> "I could try to decouple the bugfix first, wdyt?"

Why it matters: clean single-concern PRs are cherry-pickable. From mimowo on pr-10013:

> "We could yes, but in a dedicated PR so that we can cherrypick easily, I would not mix the changes to pre-existing metrics in this PR."

[[reviewer-mbobrovskyi|mbobrovskyi]] applies the same rule on pr-10595:

> "Can we move these changes into a separate PR to avoid mixing concerns?"

### Squash before final approval

From mimowo on pr-8341:

> "This PR has many commits already, it will be much better to squash it indeed. It does not need to be a new PR, you can force push on this branch too."

Single clean commit → simpler cherry-picks.

---

## 6. Scheduler/cache performance and correctness

### Map changes to invariants

From [[reviewer-gabesaba|gabesaba]] on pr-10082:

> "I'm concerned that this will invalidate the original sticky workload fix, as it was an inadmissible, high-priority workload at the front of the queue..."

For any change in `pkg/scheduler/` or `pkg/cache/`, list the invariants the system depends on (sticky workloads, preemption-loop avoidance, requeue batching, cache coherency under churn) and check the diff against each.

### Event-volume scaling

For event handlers, the question is: does this scale to clusters with thousands of pods reconciling per second? From gabesaba on pr-8709:

> "probably only requeue for ClusterQueues which are affected by the change."

Workqueue patterns with time-based batching (1 minute prod, 5 seconds tests) beat raw event-per-event reconciliation.

### MultiKueue disconnect scenarios

For admission-check changes that span clusters, the manager-worker disconnect path must be reasoned through explicitly. From gabesaba's pr-9359 release note:

> "When this happened on a manager that had temporarily lost connection to a worker, the remote workload would keep running on the reconnected worker — invisible to the manager — risking double resource reservation."

See [[scheduler-internals]], [[preemption]], [[cache-architecture]], [[multikueue]].

---

## 7. Logging verbosity

From mimowo on pr-8082:

> "This might be very verbose if V(2), I would say this is V(4)."

| Level | Purpose |
|---|---|
| V(0) – V(1) | Errors and very rare lifecycle events |
| V(2) | Coarse lifecycle events (one per workload state transition, not per reconcile) |
| V(3) | Significant events at moderate frequency |
| V(4) | Per-reconciliation-cycle detail |
| V(5)+ | Deep debug (per-pod, per-condition, per-iteration loops) |

Per-reconcile logs at V(2) is the most common verbosity bug; fix the level before merge.

`golangci.yaml` runs `loggercheck` to enforce structured-logging patterns.

---

## 8. Helper extraction across integrations

When the same logic appears in multiple [[integrations|Job adapter implementations]] (batch/v1 Job, RayJob, JobSet, Kubeflow, AppWrapper, …), a shared helper is required. From mimowo on pr-8151:

> "it looks identical for all Job CRDs, so I would propose to introduce a helper like 'ShouldSyncStatus'."

[[reviewer-mbobrovskyi|mbobrovskyi]] applies the same pattern within a single file. From pr-10323:

> "I think this function does too much. It would be helpful to add a `workload.WorkloadClusterQueue(oldWl)` helper and use it outside this function."

See [[job-framework-interface]].

---

## 9. Release notes

Production bugs require a release note that describes the **scenario, risk, and fix** — not just the fix.

From mimowo on pr-8805:

> "IIUC this is a production issue as mentioned in the comment, so please add a release note. I think we will need to cherrypick this one to 0.16.x."

From [[reviewer-tenzen-y|tenzen-y]] on pr-10282, rewriting a vague note:

> "TAS: fix a bug that Pods which only contain the `kueue.x-k8s.io/podset-slice-required-topology` or `kueue.x-k8s.io/podset-slice-required-topology-constraints` are not ungated."

Format: TAS / MultiKueue / Scheduler / etc. — the area prefix is preserved so operators can scan the changelog quickly.

---

## 10. Feature gate lifecycle

`pkg/features/kube_features.go` is the source of truth. After editing it:

```shell
make generate-featuregates
```

This rebuilds `test/compatibility_lifecycle/reference/versioned_feature_list.yaml` and copies it to `site/data/featuregates/`. CI enforces YAML/doc sync.

Lifecycle stages: Alpha → Beta → GA. From real PRs:

- **Alpha**: cherry-picks allowed if the fix is mechanical; weaker backwards-compat obligation
- **Beta**: stricter; on-by-default features that fail in production may be temporarily disabled (e.g., `SchedulingEquivalenceHashing` in pr-10001)
- **GA**: cannot be disabled; behavior is contract

New code under a feature gate must:
- Validate API fields conditional on the gate (block usage when gate is off)
- Have integration tests covering both gate states
- Update `versioned_feature_list.yaml` via `make generate-featuregates`

See [[feature-gates]].

---

## 11. Tooling that enforces the bar

### `make verify`

The local equivalent of CI. Regenerates checked-in artifacts (codegen, mocks, docs, Helm outputs) and runs read-only checks (linters, formatting, shellcheck, TOC verification, Helm unit tests).

Subsets:
- `make verify-tree-prereqs` — just regenerate
- `make verify-checks` — just check
- `make ci-lint`, `make fmt-verify`, `make helm-verify`, `make shell-lint` — individual targets

### `.golangci.yaml`

Enabled linters relevant to review feedback above:

| Linter | What it catches |
|---|---|
| `loggercheck` | Structured-logging key/value mismatches |
| `nilerr`, `nilnesserr` | Nil-error handling bugs |
| `durationcheck` | Multiplying durations incorrectly |
| `perfsprint` (`errorf: true`) | Bad `fmt.Errorf` formatting |
| `forbidigo` | Banned APIs (e.g., `sort.Slice` family — use `slices` instead) |
| `makezero` | `make([]T, n)` followed by `append` (length bug) |
| `fatcontext` | Context captured by hot-loop variable |
| `copyloopvar` | Loop-variable capture in goroutines |

Several of the "review nits" you'd otherwise get from a human are caught by these linters first.

---

## 12. The implicit checklist before opening a PR

A condensed pre-flight version of everything above:

- [ ] One concern. Cleanup and bugfix are separate PRs.
- [ ] Squashed commits.
- [ ] Integration test for the new path. Both feature-gate states if applicable.
- [ ] Manual e2e on a live cluster for any ownership-level change.
- [ ] Names match semantics (feature gates, API fields, variables).
- [ ] API markers are linter-clean (`+required` ⇒ no `omitempty`).
- [ ] No in-place removal of beta API fields. Deprecate now, remove on promotion.
- [ ] Code kept for upgrade compatibility has a TODO with the target version and a tracking issue.
- [ ] Per-reconcile logs at V(4)+; coarse lifecycle at V(2).
- [ ] Comments match what the code does, not what it intends to do.
- [ ] Release note for any production-impacting fix, written in scenario/risk/fix form.
- [ ] `make verify` passes locally.

---

## Related pages

- [[reviewers]]
- [[reviewer-mimowo]]
- [[reviewer-tenzen-y]]
- [[reviewer-gabesaba]]
- [[reviewer-mbobrovskyi]]
- [[reviewer-pbundyra]]
- [[testing]]
- [[testing-integration]]
- [[testing-e2e]]
- [[feature-gates]]
- [[release-process]]
- [[job-framework-interface]]
