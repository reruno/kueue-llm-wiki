# Reviewer: mimowo

**Summary**: Profile of Kueue core maintainer @mimowo — their review philosophy, preferred patterns, recurring concerns, communication style, and what they require before approving a PR. Intended for LLMs performing code review: copy this reasoning to produce feedback that is coherent with Kueue's implicit standards.

**Sources**: `raw/github/kubernetes-sigs__kueue/` — analysis of review comments across PRs where @mimowo left substantive feedback; representative examples drawn from [[pr-4444]], [[pr-8082]], [[pr-8151]], [[pr-8186]], [[pr-8341]], [[pr-8464]], [[pr-8530]], [[pr-8805]], [[pr-9311]], [[pr-9619]].

**Last updated**: 2026-04-30

---

## Identity and role

GitHub handle: [@mimowo](https://github.com/mimowo)

Role: Core Kueue approver and reviewer. Listed in `OWNERS_ALIASES` under both `kueue-approvers` and `kueue-reviewers`. One of only three top-level approvers (alongside `gabesaba` and `tenzen-y`). Also listed in `SECURITY_CONTACTS` and assigned to every new release issue alongside `tenzen-y` (`.github/ISSUE_TEMPLATE/NEW_RELEASE.md`).

**Primary domain expertise** (inferred from CHANGELOG contributions):
- Topology-Aware Scheduling (TAS): architecture, rank-based ordering, node taints/tolerations, node failure handling, node hot-swap
- MultiKueue: dispatch, preemption orchestration, adapter sync logic, `BatchJobWithManagedBy` feature
- Workload eviction: `PrepareForEviction`, `EvictWorkload`, eviction metrics (`evicted_workloads_once_total`), state transitions
- Cache and scheduler internals: queue manager, snapshot, cohort hierarchy
- RayJob integration, ProvisioningRequest controller

---

## Review philosophy

### Correctness over velocity

mimowo places `/hold` rather than /lgtm when something needs clarification. They will block a PR for days or weeks rather than accept a risk and fix it later. When a PR is approved then a blocker is found, they re-apply `/hold` without hesitation.

### Backwards compatibility as a hard constraint

**This is a recurring hard blocker.** Any deletion of code that may still be needed during a cluster upgrade must be kept for two releases. Exact quote from [[pr-8530]]:

> "we cannot remove this code in the PR, because upgrading Kueue will not work — nothing will remove the finalizers from pre-existing workloads. So we need to keep this code for 2 releases."

When temporary/deprecated code is kept, mimowo **requires**:
1. A TODO comment explaining what to remove and when
2. A GitHub issue filed so it is not forgotten
3. Exact version in the TODO (e.g., "drop this in 0.18")

Example from [[pr-8530]]: "please add a comment to drop this code in 0.18, and I would propose to open an issue for that not to forget, and TODO comment."

### Decouple before merging

When a PR conflates multiple concerns (cleanup + bugfix, new feature + refactor), mimowo asks to split them before approval. Typical pattern from [[pr-6297]]:

> "I could try to decouple the bugfix first, wdyt?"

This is especially important when the bugfix is cherry-pick-worthy — a clean single-concern PR is much easier to cherry-pick.

### Squash commits before merge

mimowo requires squashed commits before final approval. Will explicitly say "please squash the commits again" after each push. Rationale: cherry-picks become simpler with a single clean commit. From [[pr-8341]]:

> "This PR has many commits already, it will be much better to squash it indeed. It does not need to be a new PR, you can force push on this branch too."

---

## Code review patterns

### Naming precision (most frequent category)

mimowo uses `nit:` for non-blocking name suggestions but has strong preferences and will explain the semantic ambiguity. Typical concerns:

- **AddFoo vs Foo**: Wrapper builder methods should be `Foo(...)` not `AddFoo(...)`, matching the existing pattern. From [[pr-8082]]: `AddAnnotation` → `Annotation`, citing the existing `Label` convention.
- **Feature gate names must match semantics**: From [[pr-8530]], when a feature gate named `SkipFinalizersForServingWorkloads` was found to check a different condition than the name implied, mimowo proposed renaming to `SkipFinalizersForPodsSuspendedByParent` plus updating the PR title.
- **Variable names must reflect content**: If a set called `noMoreBorrowingCohorts` might actually contain cohorts that are already borrowing, rename to `suspendBorrowingCohorts` or `noFurtherBorrowingCohorts` to clarify the intent.
- **API field symmetry**: When a new field mirrors an existing one, names should be symmetric. Example: if `excludeResourcePrefixes` exists, a complementary field should be `includeResourcePrefixes`, not something asymmetric.

### API design scrutiny

mimowo evaluates API changes against long-term maintainability. Key concerns:

- **Pointer vs value fields**: Is the field optional or required? Should zero values be meaningful?
- **Configuration API validation**: Notes that Configuration API (non-CRD) does not generate CEL validation rules, so developers cannot rely on generated validation.
- **Interaction with feature gates**: New API fields that only make sense when a feature gate is enabled need guard validation. From [[pr-8082]]: "I think we should still make the validation, and allow for `EnableInTreeAutoscaling` only if `ElasticJobsViaWorkloadSlices` are enabled."
- **API naming documentation**: Documentation comments must exactly describe what the field does. Comments claiming behavior that the code doesn't implement are blocked.

### Scope limitation

Prefers the smallest change that fixes the problem. When code touches multiple CRDs generically, mimowo challenges whether the scope should be narrowed:

From [[pr-8082]] on a generic `CopyLabelAndAnnotationFromOwner` applied to all Jobs:
> "I would prefer to narrow the scope to Ray only with: `if IsRaySubmitterJob(ctx, job) && job.Labels[QueueName] == nil { ... }`"

### Unnecessary intermediate variables

Flags redundant local variables inline. Example from [[pr-8082]]:
> "nit, no need for the interim variable here"

(The pattern `x := foo.Bar; if x != nil { ... }` when `foo.Bar` can be used directly.)

### Log verbosity levels

mimowo monitors log level appropriateness:
- Per-reconciliation-cycle logs should be V(4) or higher, not V(2)
- V(2) is reserved for coarse-grained lifecycle events
- From [[pr-8082]]: `log.V(2).Info("Patching pod...")` → "This might be very verbose if V(2), I would say this is V(4)"

### Helper extraction

When the same logic appears across multiple Job CRD adapters (batch/v1 Job, RayJob, JobSet, etc.), mimowo will ask for a shared helper. From [[pr-8151]]:
> "it looks identical for all Job CRDs, so I would propose to introduce a helper like 'ShouldSyncStatus'"

### Dead-code / special-case removal

Extra guard conditions that are logically unnecessary (e.g., checking a label that can never be empty at the call site) are flagged as nits. From [[pr-8082]]:
> "nit, this special case doesn't seem needed"

---

## Test requirements

Testing is a **hard blocker** for mimowo. They will not give final approval without appropriate test coverage.

### Integration tests required for new paths

Any new code path that touches the admission or eviction flow needs an integration test. From [[pr-8186]]:
> "Please add a test, I think the same testing approach should work as in #7913"

For changes that add conditional behavior, they specify the scenario to test: "I would suggest to add more test case: 'when workload is evicted, but suspended, and the startTime is rest, restore node affinity'".

### Flakiness must be proven absent before merge

For tests with timing or ordering sensitivity, mimowo requires loop testing before merge. From [[pr-9619]]:
> "since the test have some exceptions and various subtle points, could you run it in a loop locally to make sure it does not flake? I think 50 repeats should be enough, but if the test runs quickly then we could do more."

### Manual e2e on a live cluster for upgrade paths

For changes that affect in-flight workloads (e.g., changing which object owns a Workload), mimowo asks for manual testing on a live cluster, not just kind: from [[pr-8341]]:
> "I would like to ask you to perform a manual test e2e on a live cluster to check what will happen if there is a pre-existing RayJob at the moment of upgrade."

### Feature gate interaction testing

New code that interacts with a feature gate must be tested with the gate disabled. From [[pr-8151]]:
> "Oh, I think I also need to check with MultiKueueBatchJobWithManagedBy disabled."

---

## Documentation requirements

### Release notes for production bugs

If a bug has been reported by users or is tracked in an issue as a production problem, mimowo asks for a release note. Example from [[pr-8805]]:
> "IIUC this is a production issue as mentioned in the comment [...], so please add a release note. I think we will need to cherrypick this one to 0.16.x."

### Accurate comments

Comments and docstrings must match what the code actually does. mimowo reads comments against the implementation. If a comment says "first batch of Job pods" but the function operates on generic Workloads, it must be updated to be accurate.

### KEP sections

When updating a KEP (design doc), mimowo provides direction on which sections to add vs. which to trim. Example from [[pr-8396]]:
> "TBH, I think this section is too much details. If you want to keep it, then just keep the first paragraph."

---

## Compatibility and upgrade reasoning

### API discovery over version gating

mimowo prefers detecting what API is available over hard-coding Kubernetes version checks. From [[pr-4444]] on ProvisioningRequest v1 adoption:
> "sgtm, I'm ok to use restmapper in this case. If v1 available, then use it, otherwise if v1beta1 available then use it, otherwise fail."

The reasoning: skewed installations (e.g., CA version ≠ K8s version) exist; version checks are fragile; REST mapper discovery is definitive.

### Upgrade scenarios must be investigated

When a change moves where a resource is managed (e.g., Workload ownership from RayCluster to RayJob), mimowo explicitly asks: "what happens to pre-existing objects during upgrade?" This must be answered by testing before approval.

### Cherry-pick decisions

mimowo actively cherry-picks bugfixes to release branches. Patterns:
- Production bugs and regressions: `/cherrypick release-0.16 release-0.15`
- Alpha-feature consistency fixes: cherry-picked if the diff is clean and the feature is alpha (weaker backward-compat obligation)
- Cleanup/refactor: typically not cherry-picked unless it also fixes a bug

---

## Communication style and vocabulary

### Tone

mimowo is collegial, never dismissive. They acknowledge effort before raising concerns: "Thank you for working on this." or "Excellent, thank you!" They frame even hard blockers as questions or observations before stating the problem.

### Shorthand used frequently

| Shorthand | Meaning |
|---|---|
| `nit:` | Non-blocking style/naming suggestion |
| `sgtm` | Sounds good to me (accepts a proposal) |
| `wdyt` | What do you think? (seeking consensus) |
| `IIUC` | If I understand correctly (checking own understanding) |
| `iirc` | If I recall correctly (looser memory claim) |
| `ptal` | Please take a look (inviting review) |
| `LGTM` | Looks good to me (positive signal before /lgtm) |
| `TBH` | To be honest (signals honest disagreement) |

### Questioning style

mimowo rarely issues directives outright. Hard blockers are phrased as questions:
- "Hm, this change does not look right. Do we need it, and why?" (from [[pr-8151]])
- "I'm wondering it would be cleaner to check X also for consistency with the description." (from [[pr-8530]])
- "Do we actually check they are unsuspended? I don't see that in code."

This is a pattern, not hedging — when mimowo says "do we need it?", a good answer requires justification.

### Positive confirmations

mimowo explicitly signals when they are satisfied:
- "I see, nice" — acknowledges a clever approach
- "sounds good" — accepts an explanation
- "ok, sgtm" — closes a naming debate
- "Awesome, thank you 👍" — expresses genuine enthusiasm
- "Excellent, thank you!" — strong approval

---

## Approval workflow

### Standard approval

```
/lgtm
/approve
Thank you 👍
```

### Conditional approval (needs follow-up before merge)

```
/lgtm
LGTM, but we need some integration tests
```

Or: approve then immediately /hold waiting for another reviewer's comment to be resolved.

### Cherry-pick flow

After final approval:
```
/lgtm
/approve
/cherrypick release-0.16
/cherrypick release-0.15
```

### Hold patterns

- `/hold` + reason at the start of review when something needs investigation
- `/unhold` when confirmed resolved (sometimes with "Ok, I checked the PR and it looks reasonable, let's move forward")
- `/hold` can be re-applied after `/lgtm` when a new blocker is found

### Requiring another approver

When mimowo has approved but wants a second opinion:
```
/approve
LGTM, but leaving tagging to @mbobrovskyi
```

Or: `/lgtm` without `/approve` to signal agreement while deferring merge authority.

---

## What triggers a hard block

The following consistently appear as blockers before approval:

1. **No integration test for a new or changed code path** — always asked for; will not approve without it
2. **Deleted code that breaks rolling upgrade** — must be kept for 2 releases; requires TODO + issue
3. **Feature gate interaction not tested** — must verify behavior when feature gate is disabled
4. **Manual upgrade scenario untested for ownership-level changes** — requires explicit confirmation
5. **Wrong log verbosity level** — specifically V(2) for per-reconciliation-cycle logs
6. **API field or feature gate name that doesn't match its semantics** — will block until renamed
7. **Documentation that says something the code doesn't do** — must match exactly

---

## What is a non-blocker (nit)

The following are consistently marked `nit:` and do not block approval:

- Naming suggestions where the original name is acceptable but not ideal
- Intermediate variable removal
- Minor doc wording improvements
- Translation updates to Chinese docs (deferred to separate PR / native speaker review)

---

## Patterns to copy when reviewing Kueue code

An LLM reviewer should apply the following mimowo-derived checks:

**Naming**
- Does every new function and type name accurately describe what it contains? Could a reader mistake it for something broader or narrower?
- For builder/wrapper methods: does it follow the existing convention (`Annotation(k, v)` not `AddAnnotation(k, v)`)?
- Does a new feature gate name match what it actually gates?
- Are API fields symmetric with existing ones where applicable?

**Tests**
- Is there an integration test for each new behavior? Does it cover the "off" state of any feature gate involved?
- If timing-sensitive, was the test run in a loop locally?
- For ownership changes: was a manual upgrade scenario tested on a live cluster?

**Compatibility**
- Does any deleted code leave finalizers, annotations, or other cluster state that would break a rolling upgrade?
- If yes: keep for 2 releases, add TODO with version and a GitHub issue link.

**Logging**
- Is verbose per-iteration log output guarded by V(4) or higher?

**Code placement**
- Does logic shared across multiple Job CRD adapters live in a common helper?
- Does logic conceptually belonging to a function (e.g., cleanup in `DeleteCohort`) live there rather than scattered?

**Documentation**
- Do comments say exactly what the code does — not what a caller hopes it does, not what an older version did?
- Does production-impacting bug fix have a release note?

**Scope**
- Is the PR doing one thing? If it conflates cleanup and bugfix, should they be separated?
- Are generic-looking helpers actually general, or are they specialized to one integration?

---

## Related pages

- [[architecture]]
- [[workload]]
- [[topology-aware-scheduling]]
- [[multikueue]]
- [[testing]]
- [[testing-integration]]
- [[feature-gates]]
