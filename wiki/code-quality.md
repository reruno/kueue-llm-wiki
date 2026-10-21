
# Code Quality in Kueue

**Summary**: The shared technical quality bar that Kueue reviewers enforce, synthesized across [[reviewer-mimowo|mimowo]], [[reviewer-tenzen-y|tenzen-y]], [[reviewer-gabesaba|gabesaba]], [[reviewer-mbobrovskyi|mbobrovskyi]], and [[reviewer-pbundyra|PBundyra]]. Use this page to predict what will block a PR and what will earn quick approval.

**Sources**: `raw/github/kubernetes-sigs__kueue/` PR review comments; `raw/kueue/CONTRIBUTING.md`; `raw/kueue/.golangci*.yaml`; `raw/kueue/Makefile-verify.mk`; `raw/kueue/pkg/features/kube_features.go`; the individual reviewer pages; pr-16725.md (logging policy), pr-10727.md (AI policy), pr-15264.md, pr-16633.md, issue-16866.md; `raw/kueue/site/content/en/community/contribution_guidelines/logging_policy.md`, `logging_reference.md`; `raw/kueue/AGENTS.md`.

**Last updated**: 2026-10-21

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

### AI-assisted contributions

Kueue follows the [Kubernetes AI Tool Usage Policy](https://www.kubernetes.dev/docs/guide/pull-requests/#ai-guidance), linked from `CONTRIBUTING.md` and the contribution-guidelines index since pr-10727.md (merged 2026-04-23). Maintainers chose to link the upstream policy rather than copy it, expecting it to change. The points mimowo highlighted in that PR: large AI-generated PRs and AI-generated commit messages are not allowed; verify AI-generated changes yourself (code review, tests) before asking for review, and be able to explain every change; answer review comments yourself, not through an AI tool. `AGENTS.md` adds Kueue-specific rules (source: `raw/kueue/AGENTS.md`):

- Disclose AI use in the PR description, and when commenting or filing issues. In practice authors add a line such as "AI assisted, but mostly human driven" (source: pr-16725.md, pr-16723.md, pr-16793.md).
- No AI authorship markers: no AI co-author, `assisted-by` or `co-developed` commit trailers.
- No auto-close keywords (`Fixes #123`) or `#` mentions in commit messages. Prow adds `do-not-merge/invalid-commit-message`. Put issue references in the PR description.

A standard `ai-assisted` label or Prow prompt was discussed but left as a follow-up (source: pr-10727.md).

### Respond to every review comment

When updating a PR, reply to each review thread instead of only pushing. Otherwise the reviewer has to reverse-engineer what changed (mimowo on pr-17055.md).

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

## 7. Logging policy and verbosity

Kueue has a written **logging policy** (`site/content/en/community/contribution_guidelines/logging_policy.md`, pr-16725.md, merged 2026-10-08, fixes #9801). It applies to **new or modified** log records. Existing records are being migrated incrementally, starting with the scheduler, `workload_controller` and `cluster_queue_controller`. It builds on the Kubernetes logging conventions and Google's Go logging guidance. At verbosity `n`, records at levels `0..n` are enabled.

| Level | Intended use |
|---|---|
| `Error` | Operational failures that prevent or materially disrupt an operation and may need operator attention |
| `V(0)` | Rare anomalies affecting Kueue as a whole (invariant violations); use `Error` if the operation is disrupted |
| `V(1)` | Infrequent lifecycle and health transitions (startup, configuration, leadership, connection health); rare anomalies confined to one controller or the scheduler |
| `V(2)` | Concise activity summaries: material changes in overall state, start and completion of top-level scheduler cycles |
| `V(3)` | Main per-object diagnostics: `Reconcile` start/end/duration, key informer observations, main scheduling and controller decisions with reasons and outcomes, context for changes saved through the API, relevant cache-vs-API differences |
| `V(4)` | Details that explain a decision: old/new values, aggregated decision context, brief plans for grouped writes, fan-out or enqueue |
| `V(5)` | Implementation traces: individual scheduling calculations, heap/cache mechanics, individual API-write attempts and retries, extra informer/webhook metadata, repeated steps in searches |
| `V(6+)` | Deep tracing and broad internal-state dumps |

Guidelines:

- **Errors:** no `V(n).Error(...)` and no `Enabled()` guard around error logging. Return errors from lower layers and log them **once** at a higher control layer. Preserve each cause when combining failures. `NotFound`/`Conflict` that normal control flow handles may be logged as diagnostics.
- **API writes:** report a persisted transition **after** the write succeeds. Prefer an Event after a successful write; if controller-runtime already logs the Event (it does at `V(1)`), a separate log can be omitted. Logging before a write is optional and `V(4+)`.
- **Performance:** check `Enabled()` on the emitting logger before costly computation, allocation, serialization or locking done only for a log. Small bounded fields (counters, enums) can go at low levels; large already-computed fields at higher levels; fields that need a dedicated state dump at `V(6+)`.
- **Construction:** use the logger from the propagated context. Keys are stable lowerCamelCase: `workload`, `job`, `clusterQueue`, `resourceFlavor`.
- **Security:** never log tokens, secrets or credentials at any level. client-go logs REST bodies at `V(8–10)` (about 1 KiB at V8, 10 KiB at V9, untruncated at V10), and they may contain confidential data.

The companion `logging_reference.md` records dependency behaviour at controller-runtime v0.25.1 / client-go v0.37.1. controller-runtime logs errors returned from `Reconcile` at `Error`; manager Events at `V(1)`; API-server warning headers as plain `Info`; and `Reconcile` start/finish, webhook metadata and 10-second priority-queue snapshots at `V(5)`. client-go logs reflector diagnostics at `V(1–4)`, throttling at `V(3)` (rate-limited `V(2)`/`V(0)` for long waits) and Retry-After at `V(4)`. Kueue's `CustomLogProcessor` (`pkg/util/logging/logging.go`) matches concurrent-modification errors by message text, relabels them from `Error` to `V(3)` and drops the stack trace. The level check runs **before** relabeling, so these records appear whenever `Error` is enabled. The integration framework fails a suite if any Error-level record is a write conflict (see [[testing-integration]]).

**Correction (2026-10-21)**: this section used to say per-reconcile logs belong at `V(4)` and coarse lifecycle at `V(2)`, based on mimowo's review on pr-8082 ("This might be very verbose if V(2), I would say this is V(4)"). The written policy (pr-16725.md) moves the main per-object reconcile diagnostics to **`V(3)`** and reserves `V(2)` for component-level summaries, not per-object transitions. Per-iteration detail inside a reconcile stays at `V(4)`/`V(5)`. Follow the policy for new code.

`golangci.yaml` runs `loggercheck` to enforce structured-logging key/value pairs. The v0.20.0 logger-name alignment (`<kind>-reconciler`, `<subcomponent>-<kind>-reconciler`) is recorded in CHANGELOG-0.20.md.

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

Format: TAS / MultiKueue / Scheduler / etc. — the area prefix is preserved so operators can scan the changelog quickly. Established prefixes include `CLI:` for kueuectl, `KueueViz:`, `Importer:`, `Helm:`, `Observability:`, `FairSharing:`, `AFS:`, `TAS:`, `MultiKueue:` and `Scheduling:` (source: CHANGELOG-0.20.md).

Since pr-15264.md the PR template tells authors to describe the change from the user's point of view, never leave the block blank (use `NONE` when there is no user-facing change), add a feature prefix, and include an `ACTION REQUIRED:` section when upgrade steps are needed. It points to the optional `cmd/experimental/skills/kueue-release-notes/SKILL.md` skill. Maintainers still rewrite notes with `/release-note-edit` or `/set-release-note`, typically into "Fixed a bug where X. Kueue now Y." form (for example pr-15376.md, pr-16850.md).

**Static-analysis false positives.** Snyk reports `crypto/sha1` uses (Workload-name hashing in `jobframework/workload_names.go`, the provisioning controller, WAS virtual Pods) as "password hash with insufficient computational effort". Maintainers closed this as not a bug: the hashes only avoid name collisions and are not security-sensitive. Downstream forks filter them, for example in the OpenShift kueue-operator `.snyk` (source: issue-16866.md).

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
- [ ] Log levels follow the logging policy: main per-object reconcile diagnostics at V(3), decision details at V(4), traces at V(5); errors logged once at the control layer; `Enabled()` guard before costly log-only work.
- [ ] Comments match what the code does, not what it intends to do.
- [ ] Release note for any production-impacting fix, written in scenario/risk/fix form.
- [ ] AI use disclosed in the PR description; no AI trailers or `Fixes #` in commit messages.
- [ ] Tests follow the [[testing#Community test-writing guidelines|writing-tests guide]] (lowest sufficient level, wrappers, one `ginkgo.It` per scenario).
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
