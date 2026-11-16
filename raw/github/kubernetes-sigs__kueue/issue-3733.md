# Issue #3733: TAS: cache information is not updated when RF spec (nodeTaints or tolerations) is changed

**Summary**: TAS: cache information is not updated when RF spec (nodeTaints or tolerations) is changed

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3733

**Last updated**: 2026-11-04T10:14:47Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-04T10:40:14Z
- **Updated**: 2026-11-04T10:14:47Z
- **Closed**: —
- **Labels**: `kind/bug`, `lifecycle/stale`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 38

## Description


**What happened**:

When TAS RF is updated (e.g. nodeTaints or tolerations), then the cache information is not updated.

**What you expected to happen**:

Update the cache or fail the update. I think updating cache would be ideal, but it might be hard to deliever before 0.10, 
so we may just block updates for now (when topologyName is specified).

**How to reproduce it (as minimally and precisely as possible)**:

Create a TAS setup, and add the .spec.tolerations.
issue: the tolerations are not added to the newly admitted workloads.

**Anything else we need to know?**:

We had a similar decision about update to the levels and decided to block updates for now: https://github.com/kubernetes-sigs/kueue/issues/3614

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-04T10:40:29Z

/assign @PBundyra 
tentatievly
cc @mbobrovskyi

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-04T10:41:15Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-04T21:31:52Z

/remove-lifecycle stale

### Comment by [@qti-haeyoon](https://github.com/qti-haeyoon) — 2025-04-15T05:14:23Z

Hi @mimowo , do we have plan to make resource flavor spec mutable again? Moreover, it is currently not possible to remove `topologyName` from `ResourceFlavor` in case we want to not use TAS anymore. Is this intended behavior?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T05:19:49Z

Hi, we want to support mutating TAS RF spec long term, we just didn't have the capacity to do it right in the early phases. 

So disabling mutations was a conservative move to avoid bugs. There is no timeline to support mutations on our side but we can consider contributions. 

cc@mwielgus @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T05:34:55Z

cc @mwielgus

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-07-03T17:52:34Z

Any new plan to support mutation when topologyName is specified, by any chance?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-03T18:06:57Z

It is not prioritized at the moment, but I would welcome contributions.

I think mutating RF's .spec.tolerations should be relatively easy as it does not impact cached TAS usage (we can start here).

However, mutating spec.nodeLabels impacts cached TAS usage, so we need to choose:
1. drop the usage completely and start rebuilding from scratch
2. keep cache usage as if nothing happened
3. update cache usage by dropping usage for workloads which no longer match the new spec.nodeLabels

I think (1.) is problematic, because it will lead to overadmission of workloads. Probably (3.) is most accurate.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-01T19:03:20Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-31T19:57:04Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-30T20:26:25Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-30T20:26:30Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3733#issuecomment-3593300399):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T07:30:46Z

/remove-lifecycle rotten
/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T07:30:52Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3733#issuecomment-3595018985):

>/remove-lifecycle rotten
>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-01T07:46:40Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-01T08:34:11Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-30T09:25:45Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-29T09:43:48Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-07-29T06:45:39Z

Hi @mimowo and @PBundyra,

Following the discussion on #13606, I investigated the current TAS ResourceFlavor immutability constraints and cache update paths. I would like to take a narrowly scoped first step toward ResourceFlavor mutability: supporting in-place updates to `spec.tolerations` for TAS ResourceFlavors.

My proposed behavior is:

- Update the tolerations stored in the existing TAS flavor cache without rebuilding the cache or dropping `usage`/`wlUsage`.
- Preserve the accounting and status of already admitted workloads; running workloads would not be evicted or rewritten.
- Use the updated tolerations for subsequent TAS scheduling decisions and the existing ResourceFlavor-to-Pod injection path.
- Requeue affected inadmissible workloads so that adding a toleration can make them schedulable without requiring another unrelated cluster event.
- Add integration coverage for adding and removing tolerations, requeuing a pending workload, and preserving admitted workload usage across the update.

This first change would intentionally exclude `nodeLabels`, `topologyName`, and Topology `levels`, since those fields change node membership or the meaning of cached topology usage and require separate semantics.

Does this scope and behavior sound reasonable? Since #3733 still has an existing assignee, would it be okay for me to take this scoped part of the issue?

AI disclosure: I used an AI assistant to help investigate the current code paths and draft this proposal. I reviewed the findings and proposed scope.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-29T07:34:32Z

Yeah, I think starting with mutability for tolerations is the safest start possible, because it does not change the set of matching workloads.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-07-29T07:40:01Z

Thank you, that makes sense. I will proceed with the narrowly scoped `spec.tolerations` mutability work. I will preserve the existing TAS `usage`/`wlUsage`, cover adding and removing tolerations plus pending-workload requeue behavior with integration tests, and then open a PR for review.

/remove-lifecycle rotten

AI disclosure: I used an AI assistant to help investigate the implementation paths and draft this response. I reviewed the proposed scope and will verify the implementation and test results.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-07-30T03:48:28Z

Following up on the tolerations phase (#13622, merged — thanks for the reviews!): I looked into `spec.nodeTaints` next, since it is already mutable (#9427). The API update works, but updating nodeTaints does not requeue inadmissible workloads — a workload rejected for an untolerated flavor taint stays Pending indefinitely after the taint is removed, until an unrelated event happens to trigger a requeue. With `SchedulingEquivalenceHashing` (default since 0.18), even newly submitted workloads of the same shape are parked without a scheduling attempt, so resubmitting does not help either.

I opened #13647 with a narrow fix mirroring the tolerations approach: extend the TAS ResourceFlavor controller's update predicate to detect `nodeTaints` changes and reuse the existing sync-cache-then-requeue path. No TAS cache changes are needed since nodeTaints are not stored there, and admitted usage is unaffected.

One open question: the core ResourceFlavor controller only requeues inadmissible workloads when a ClusterQueue flips from pending to active, so a similar gap likely exists for non-TAS flavors as well. Happy to investigate that separately if you think it is worth addressing at the core controller level.

AI disclosure: I used an AI coding tool to help with the investigation and reproduction; I reviewed the analysis and code myself.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-07-30T08:54:45Z

Following up on the mutability work (#13622 tolerations, #13647 nodeTaints requeue + CPs): I'd like to propose tackling `spec.nodeLabels` next, and I want to align on semantics before writing any code.

**Proposed semantics** (following your option 3 from the earlier discussion — drop only the usage that no longer matches):

1. **ClusterQueue quota usage is untouched.** Admitted workloads keep their quota reservation until they finish, regardless of the nodeLabels change. This prevents the over-admission problem of option 1.
2. **TAS usage follows the topology tree.** The flavor cache updates `NodeLabels` in place (same pattern as `updateTolerations` in #13622), preserving `usage`/`wlUsage`. The per-cycle snapshot then rebuilds the tree from nodes matching the *new* labels, and usage rows whose domains are no longer in the tree are skipped — **this skip-path already exists and is exercised today** for deleted/not-Ready nodes (`tas_flavor_snapshot.go`, `addTASUsage`: *"this can happen if there is an admitted workload for which the backing node was deleted or is no longer Ready"*). So option-3 semantics at the TAS level largely reuse battle-tested behavior rather than introducing new state migration.
3. **Admitted workloads are not evicted and not re-routed.** Their `TopologyAssignment` remains authoritative; pods created after the update (e.g. remaining pods of a partially-started workload) still follow the original assignment, so pod sets are never split across old/new node sets. The new labels only affect new admissions.
4. **Pending workloads are requeued.** Extend the TAS ResourceFlavor controller's update predicate to detect `nodeLabels` changes (same sync-cache-then-requeue path as #13622/#13647, which also clears the equivalence-hash bulk-move state).

**Consistency notes:**
- Restart converges to the same state: caches rebuild from Workload objects, and stale-domain usage is skipped by the same snapshot path — online and post-restart behavior match.
- Existing validation (at least one entry in `nodeLabels`) stays; only immutability is lifted.
- Quota, borrowing, and preemption are unaffected (no quota-level change).

**To verify during implementation** (will be covered by integration tests):
- Nodes that left the flavor's set may now be matched by *another* flavor while still running pods admitted under the old set; their usage must be correctly visible to the other flavor's accounting (`TASHandleOverlappingFlavors` interaction).
- Ordering: cache must observe the new labels before inadmissible workloads are retried.

**Known operational trade-off** to document: during the transition, a flavor's admitted workloads may be running on nodes outside its current `nodeLabels` until they finish naturally. This is the price of not evicting running workloads; admins who need a hard cutover can still drain the old nodes.

**Scope**: `spec.nodeLabels` only. `topologyName` and Topology `levels` remain immutable and out of scope here.

Does this direction look right to you? If so I'll start with integration tests pinning the four semantics above, then the implementation.

AI disclosure: I used an AI coding tool to help analyze the cache/snapshot code paths and prepare this proposal; I reviewed the analysis myself.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-07-30T16:18:54Z

Following up on the non-TAS `nodeTaints` open question I raised earlier: I reproduced it, and it is confirmed.

Removing `nodeTaints` from a **non-TAS** ResourceFlavor does not retry workloads left inadmissible by the taint — same signature as the TAS case (#13647), but non-TAS flavors have no TAS ResourceFlavor controller to sidestep the empty-set path in the core controller's requeue. Two integration specs reproduce it (both red without the fix):

- A pending workload is never retried after the taint is removed, while a differently-shaped workload created after the update **is** admitted — proving the scheduler cache saw the change and only the requeue was missing.
- An identically-shaped workload submitted after the removal is also frozen by scheduling-equivalence hashing, so resubmitting the same job does not help.

I opened #13670 with a narrow fix (core ResourceFlavor controller retries inadmissible workloads in the ClusterQueues using the flavor when its `nodeTaints` change). There is a narrow-vs-wide choice — I described the wider alternative (changing `updateClusterQueues` itself) in the PR and would appreciate your call on scope.

AI disclosure: I used an AI assistant to help investigate the code paths, build the reproduction, and draft the fix.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-07-31T01:33:14Z

@mimowo  (cc @PBundyra ) — gently resurfacing this in case the earlier comment was missed: I proposed a set of semantics for `spec.nodeLabels` mutability above (following your option 3 — drop only the usage that no longer matches) and would value your steer on the direction before I write any code. Happy to adjust if you'd prefer different semantics — no rush.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-07-31T02:08:33Z

@tomsen02 thank you for moving this forward. I read your comment https://github.com/kubernetes-sigs/kueue/issues/3733#issuecomment-5128677910 and looks reasonable, especially 3 and 4 points sound good already - we certainly don't want to evict workloads on node labels change.

Now 1 and 2 might be correct but I'm not sure I understand. Let me add one high level comment and the ask for clarifications.

The comment is that the driving principle should be to follow the same patter as for quota, ie. Already when RF nodeLabels are modified (relaxed or narrowed) the new flavors match or are removed. Based on that CQ usage may change. With TAS domain usage we should try to follow the same pattern, unless there are some good reasons not to.

So let me summarize what happens in regular quota when we relax or narrow the RF nodeLabels. 

Then let's clarify how we can achieve the same semantics for TAS, or if we need to diverge the semantics, then why.

This is consistent with 3 and 4 already as we don't evict workloads when quota is changed or RF nodeLabels.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-07-31T02:50:13Z

Thanks @mimowo. I dug into the regular-quota path to ground points 1 and 2.

**What regular (non-TAS) quota does when nodeLabels change**

For already-admitted workloads, the CQ's reserved/admitted quota is not recomputed from node matching. Usage is recorded at admission from the workload's assigned flavor + requests (`updateWorkloadUsage` → `wi.ResourceUsage().Assigned`, backed by `totalRequestsFromAdmission`), and it is only added/removed on workload add/finish. The flavor-change path (`updateClusterQueues` → `UpdateWithFlavors`) recomputes flavor metadata and CQ active/pending status, but never reads nodeLabels and never touches usage. I confirmed this with a small characterization test: admit a workload, flip the flavor's nodeLabels, and the reserved quota stays put and the workload stays admitted.

So what a nodeLabels edit actually affects is matching for *new* admissions (a narrowed flavor matches fewer nodes; new pods get the new nodeSelector) — already-admitted workloads keep their reservation. That's what point 1 was trying to capture: if by "CQ usage may change" you meant the new-admission side, we're aligned; if you meant admitted usage, the code says it stays. Happy to be corrected if I'm missing a path.

**How TAS mirrors this (point 2)**

TAS can follow the same semantics with machinery that already exists. The domain usage (`usage`/`wlUsage`) is preserved in the flavor cache; each cycle the snapshot rebuilds the tree from the nodes matching the *current* nodeLabels (`nodesCache.find(flavor.NodeLabels, …)` → `addNode` → leaves) and applies the preserved usage via `addTASUsage`, which skips any domain not in the rebuilt tree:

> // this can happen if there is an admitted workload for which the backing node was deleted or is no longer Ready

A nodeLabels change makes a domain "disappear" from the tree the same way a node deletion does, so it hits this existing, battle-tested skip path — not a new state migration. Combined with points 3 and 4 (which you already endorsed — no eviction, requeue pending), the net effect matches regular quota: admitted workloads keep their reservation, and only new admissions see the new node set.

The one new piece is wiring the cache's `flavor.NodeLabels` to update in place on a change (the same pattern as `updateTolerations` from #13622); the skip behavior it relies on is already there.

Does this match what you had in mind, or would you prefer different handling for the admitted-usage side?

AI disclosure: I used an AI assistant to help investigate the code paths and draft this comment.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-08-03T07:11:14Z

Following up on the open note in #13670 ("The same requeue gap likely applies to `nodeLabels` for non-TAS flavors"): I confirmed it, and it also applies to `tolerations`.

The core ResourceFlavor controller retries inadmissible workloads only when a non-TAS flavor's `nodeTaints` change, but the flavor assigner consults `nodeTaints`, `tolerations`, and `nodeLabels` together when matching workloads to the flavor. Editing either of the other two fields (e.g. adding a toleration so the flavor accepts its own taint, or correcting a `nodeLabels` value so it matches workloads' nodeSelector) leaves previously rejected workloads `Pending` indefinitely — and with `SchedulingEquivalenceHashing` (default since 0.18), resubmitting an identical workload does not help either.

Integration specs reproduce both cases (red without the fix): a differently-shaped workload created after the update is admitted, proving the scheduler cache saw the new spec and only the retry is missing.

Note this is distinct from the TAS `nodeLabels` mutability semantics discussed above: non-TAS flavors keep no topology usage, so there is no state-migration question — it is the same one-condition gap as the `nodeTaints` case.

Opened PR #13734 with the fix (same shape as #13670: compare all three scheduling-relevant fields, retry `ClusterQueuesUsingFlavor`).

AI disclosure: I used an AI assistant to help investigate and draft this. I reviewed the analysis and verified the reproduction and fix with integration tests.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-08-03T07:43:16Z

> Does this match what you had in mind, or would you prefer different handling for the admitted-usage side?

Yes, the description sounds great. Actually, I think with TAS it should work even better now- when there is a TAS workload admitted to one flavor, say A, then after extending the Flavor B definition to also cover Flavor A we should not double-count the workload originally submitted to flavor A twice

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-08-03T08:14:55Z

Thanks @mimowo! Opened PR #13738 implementing the agreed semantics.

Your overlapping-flavors point is pinned as an integration test: a TAS workload admitted on flavor A is counted exactly once after flavor B's `nodeLabels` are extended to also cover A's nodes — the spec asserts both directions (the capacity left by A's workload is admissible through B, and A's usage still counts against the shared node).

Full test list (all red without the implementation, green with it):

1. admitted workloads keep their ClusterQueue quota reservation across a `nodeLabels` change;
2. out-of-scope capacity becomes inadmissible (preserved usage rows are skipped via the existing deleted/NotReady-node path — no state migration);
3. admitted workloads keep their `TopologyAssignment` (no eviction);
4. pending workloads are requeued against the new node set (including the scheduling-equivalence freeze);
5. no double-counting across overlapping flavors.

Plus a unit test asserting the flavor cache object is preserved in place with `usage`/`wlUsage` intact, and the full TAS integration suite passing.

AI disclosure: I used an AI assistant to help write the tests and implementation. I reviewed the changes and verified the behavior with the tests above.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-08-04T07:27:42Z

@mimowo Following up on your comment in #13738 — here is a proposal for the last frozen ResourceFlavor field, `spec.topologyName`, with a note on `Topology.spec.levels` at the end (same mechanism family). *(AI tooling was used to assist the research; all code paths cited were verified manually against current `main`.)*

**Why this one is fundamentally harder than `nodeLabels`.** Changing `nodeLabels` changes *membership* — which nodes belong to the flavor — while the addressing scheme for TAS usage stays intact: when a node leaves, its capacity and its usage rows leave together. Changing `topologyName` changes the *addressing scheme itself*: domain IDs are the joined level values (`pkg/util/tas/tas.go`), so every admitted workload's `TopologyAssignment` keeps addresses expressed in the **old** topology's levels.

**The dangerous case is the one that looks healthy.** If nodes don't carry the new topology's level labels, capacity and usage vanish together — no over-admission, but the flavor is effectively dead; note this "safe" state is one `kubectl label` away from the dangerous one below. If nodes **do** carry them, capacity is counted into the new tree while the old usage rows hit the `leaves[domainID] == nil` skip in `addTASUsage` (`tas_flavor_snapshot.go`) and are silently dropped → the same seats get sold twice.

**The lost usage cannot be recovered from anywhere** (all three fallbacks verified dead): the pod-based usage path deliberately excludes TAS pods (`belongsToNonTASCache` in `pkg/controller/tas/pod_usage_controller.go`) to avoid double counting; rebuilding from `TopologyAssignment` (`ensureTASIsSynced` → `ComputeUsagePerDomain`) reproduces the old-scheme addresses; and cross-flavor aggregation only participates when the lowest level is hostname.

**Option A — keep it immutable.** Precedent: StorageClass keeps fields that reference another object's structure immutable. The operation is rare enough that "delete and recreate the flavor" may be an acceptable admin cost. Zero new mechanism.

**Option B — reuse the node-replacement model.** On `topologyName` change: try to *re-express* each admitted workload's `TopologyAssignment` in the new topology's levels (same nodes, new addressing) and persist it — writing back through the API means no in-memory-only translation that a restart would lose. If re-expression is impossible, evict and requeue — the fallback KEP-2724 already accepts for failed node replacement, riding the same machinery as `findReplacementAssignment`. Hard boundary: re-expression only works when the old topology's lowest level is `kubernetes.io/hostname` (the assignment's last value is the node name; `TASAssignedNodeNames` already exists). With a coarser lowest level (e.g. rack-lowest), we only know the rack, not the nodes → evict. One ordering constraint we'd carry over from the previous fields: the repair pass must complete before pending workloads are requeued, so new admissions never see the freed capacity mid-transition.

External data point: Slurm applies `topology.conf` changes to new allocations only and never touches running jobs — but it is immune to this problem *because its accounting is per-node, not per-domain-address*; that difference is exactly why kueue needs A or B rather than "just allow it".

**On `Topology.spec.levels`:** same family, bigger blast radius — one edit changes the addressing scheme for *every* flavor referencing that Topology. Whichever direction we pick for `topologyName` should apply: under A, keep `levels` immutable too; under B, the same repair-or-evict pass runs per referencing flavor.

My lean is B if mutability is worth having here, but A is defensible given how rare the operation is. WDYT? Happy to start with integration tests pinning the chosen semantics (red → green), as with the previous fields.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-08-06T06:07:10Z

@mimowo One more consideration for the A/B choice above — I think it simplifies the `Topology.spec.levels` half: **if B (mutable `topologyName`) is chosen, `levels` can arguably stay immutable forever.** An admin who wants a different level structure can create a *new* Topology with the desired levels and flip each flavor's `topologyName` to it one at a time — every flip going through B's controlled repair-or-evict path, with a per-flavor blast radius — instead of editing `levels` in place, which re-addresses every referencing flavor at once. A mutable pointer to immutable structures, effectively.

That reduces the realistic outcomes to two: "A + A — freeze both, document the recreate path", or "B for `topologyName` + permanent immutability for `levels`, with the flip-over as the documented migration story". It also means B is worth more than field convenience — it *is* the safe migration path for topology changes.

(AI-assisted analysis, as before.)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-08-06T06:18:34Z

 Good point, we don't need to provide mutability to the topology levels if we allow mutability to Topology name on RF. 

Otoh I have a hunch mutability of Topology.spec.levels can be easy assuming the lowest level

The main use of Topology is to have the hostname specified as the lowest level. I think if we restrict mutations to only such topologies then it should be relatively simple, because cache will store the usage for the lowest domain in both cases. Let me know if you see complications.

So for the next step I think we have two relaistc options, I don't have an opinion where to start:
1. Support mutating RF topology name, but not clearing or setting
2. Mutating topology levels in Topology, but only assuming the hostname is the lowest level before and after.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-08-06T08:55:41Z

@mimowo Verified your hunch against the code — it holds, with three anchors:

1. When `kubernetes.io/hostname` is the lowest level, the persisted `TopologyAssignment` records *only* the hostname level — higher levels are omitted (`buildAssignment`: `if s.isLowestLevelNode { levelIdx = len(s.levelKeys)-1 }` in `tas_flavor_snapshot.go`; also documented on `topologyAssignment` in `workload_types.go`).
2. Usage reconstruction keys domains by the stored values verbatim (`workload.go` builds `TopologyDomainRequests` straight from `psa.TopologyAssignment`), so with hostname-lowest the ledger key is just the hostname — middle-level renames/insertions/removals don't re-address any admitted workload.
3. The snapshot maps nodes to leaf domains by hostname on every rebuild, so the attribution also survives a controller restart.

Complications I see (none blocking, but worth agreeing upfront):

a. **Validation locality is the real difference between the two options.** Both rely on the same invariant — "hostname is the lowest level before and after". Option 2 can enforce it single-object: the Topology webhook compares `old.spec.levels` vs `new.spec.levels` in one request. Option 1 needs the RF webhook to dereference *two other objects* (old and new Topology), and either can be deleted/recreated between validation and persistence — a TOCTOU gap we can't fully close. So I'd **start with option 2**, and treat option 1 as a follow-up that reuses the same invariant machinery — it still earns its keep long-term (per-flavor staged migration, natural rollback by pointing back).

b. **Requeue gap**: pending workloads that became inadmissible under the old levels must be requeued on a levels change — same family as the RF `tolerations`/`nodeTaints`/`nodeLabels` fixes, so the fix shape and its integration tests are well understood.

c. **Mid-cycle change**: a levels update landing between snapshot and admission (including the second pass) should result in a plain requeue rather than a mixed-levels comparison — I'd pin that with a test.

d. **Semantics to state explicitly**: a gang admitted under a "same rack" constraint stays admitted if the rack level is later removed — admission-time constraints aren't retroactively re-validated. I believe that's the right call, but it should be written down in the docs.

If this sounds right I'm happy to take option 2 — test-first as usual (integration specs pinning the webhook invariant, the requeue, and the carried-over usage), then the implementation.

(AI-assisted analysis, as before.)

### Comment by [@mimowo](https://github.com/mimowo) — 2026-08-06T09:00:20Z

> Option 1 needs the RF webhook to dereference two other objects (old and new Topology), and either can be deleted/recreated between validation and persistence — a TOCTOU gap we can't fully close

Yes, this is the main reason mutating spec.topologyName on RF may be signifficantly more complex, because it opens up the possibility of changing topology drastically. With mutating just the levels we may enforce the lowest level is hostname reliably.

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-08-06T09:05:12Z

@mimowo Agreed — I'll take option 2 then. Starting with integration specs pinning the three behaviors (the webhook invariant "hostname stays the lowest level before and after", the requeue of pending workloads on a levels change, and the carried-over usage of admitted workloads), then the implementation behind them; will link the PR here.

(AI-assisted, as before.)

### Comment by [@tomsen02](https://github.com/tomsen02) — 2026-08-06T09:53:08Z

As promised — option 2 is up: #13910 (CEL relaxation on both API versions, in-place TAS cache update preserving accumulated usage, and requeue of inadmissible workloads on a levels change; three integration specs pinning the invariant, the requeue, and the carried-over usage — the requeue spec verified load-bearing against the unfixed tree).

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-11-04T10:14:44Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/
