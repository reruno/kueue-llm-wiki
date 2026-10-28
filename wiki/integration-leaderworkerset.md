# Integration: LeaderWorkerSet (LWS)

**Summary**: LeaderWorkerSet is a SIG-Apps API for running groups of Pods where each group has a designated leader and a number of followers. It targets inference serving (disaggregated prefill/decode) and training with tightly-coupled worker groups. Kueue integrates per-group, treating a leader+workers as one gang.

**Sources**: `raw/github/kubernetes-sigs__kueue/`., pr-14405.md, pr-16402.md, pr-16423.md, pr-13316.md, pr-16401.md, pr-13775.md, pr-17255.md, pr-17307.md, pr-17310.md, issue-17251.md, pr-16474.md, pr-17309.md, pr-17313.md, issue-16333.md, pr-17504.md, pr-15142.md, pr-15412.md, raw/kueue/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler.go, raw/kueue/pkg/controller/jobs/leaderworkerset/leaderworkerset_webhook.go, raw/kueue/pkg/controller/jobframework/validation.go, raw/kueue/CHANGELOG/CHANGELOG-0.20.md

**Last updated**: 2026-10-28

---

## Shape

An LWS defines `spec.leaderWorkerTemplate` (leader + workers) and `spec.replicas` groups. Total Pods = `replicas × leaderWorkerTemplate.size` (`size` includes the leader; Kueue builds a leader PodSet of 1 and a worker PodSet of `size − 1`).

Kueue's integration represents this as two PodSets per group or a combined PodSet, depending on the shape — the MVP support ([[issue-3232]] — MVP support for serving workloads running as LeaderWorkerSet) landed with leader-and-workers counted together. Rank-based placement of leaders and followers across topology domains became a TAS-specific feature ([[issue-4531]] — TAS: support co-scheduling (and rank-based ordering) of leaders and workers for LWS groups).

## Startup policies and scaling

LWS supports `startupPolicy: LeaderCreated` or `LeaderReady`. Kueue's integration must handle both: in LeaderReady mode, the workers are created after the leader is Ready, which affects PodsReady accounting. Flaky tests around scaling cover this ([[issue-4374]], [[issue-4626]], [[issue-4674]] — scaling up/down LeaderReady/LeaderCreated).

## Name length

"Kueue fails for run LWS with long name" ([[issue-10032]]) — a naming-collision/derivation edge case specific to the integration. The concrete failure: an LWS whose name exceeded **39 characters** failed to create Pods with `metadata.labels: Invalid value`, because the integration set the PodGroup identifiers `kueue.x-k8s.io/pod-group-name` and `kueue.x-k8s.io/prebuilt-workload-name` as **labels**, whose values are capped at 63 characters. The fix ([[pr-11409]], cherry-pick of #10311) introduces the **`WorkloadIdentifierAnnotations`** feature gate (default-enabled — see [[feature-gates]]) that lets those identifiers be carried as annotations instead of labels; LWS now uses the annotation counterparts, raising the supported name length to **52 characters**. Labels remain a valid way to manually define a PodGroup (see [[integration-plain-pod]]).

## NodeSelector mutation

Admission-check-applied node selectors or flavor-injected selectors need to reach the LWS Pod templates. "Allow to mutate nodeSelector for LWS" ([[issue-10178]]) was the tracking issue.

## PodTemplate metadata propagation

"Propagate LeaderWorkerSet PodTemplate metadata to PodSet" ([[issue-10326]]) — labels/annotations on the LWS template must flow into the Workload's PodSet and back to Pods.

## WorkloadPriorityClass on LWS

LWS with WorkloadPriorityClass had specific flakes around PodTemplate updates ([[issue-4744]] — Should allow to update the PodTemplate in LeaderWorkerSet).

## Naming consistency

"[LWS] Use consistent naming for prebuilt workload across the codebase" ([[issue-4324]]) — an internal hygiene issue.

## v0.18.0 behaviour changes

### Relaxed PodSpec validation was reverted — strict equality restored

An earlier change (#10275, with cherry-picks [[pr-10944]]/[[pr-10930]]) had relaxed the LWS PodSpec validation by adding `ignoreTolerations` / `ignoreNodeSelector` flags to `ComparePodSetsOptions` (`pkg/util/equality/podset.go`), so `nodeSelector`/toleration mutations on a running LWS were tolerated. This was found to be a **regression** and was **reverted** by [[pr-11214]] (net `-161` lines; cherry-picked to 0.16/0.17). Kueue again enforces **strict PodSpec equality**: the running PodSpec's tolerations and nodeSelector must match what Kueue expects, and a mutation is rejected rather than silently ignored. (The small struct cleanup of the ignore-flag fields may be re-applied later, but the behavioural relaxation is gone.) Do not rely on mutating `nodeSelector` on an admitted LWS.

### Manual `queue-name` edits no longer reverted (race fix)

A race in the jobframework reconciler could revert a **manual `queue-name` label change** on an LWS (or StatefulSet) at the Workload-object level. [[pr-11191]] fixes it by introducing the `JobWithCustomQueueNameChange` integration interface (see [[job-framework-interface]]); the Pod controller (which backs LWS and StatefulSet) implements it and owns queue-name-change handling for these serving workloads instead of the generic path.

### Mutating `queue-name` while idle

When `status.readyReplicas == 0` (no live group), `kueue.x-k8s.io/queue-name` may now be re-labeled on the LWS itself — useful for moving an LWS to a different LocalQueue without recreating it. Released as #4932 in v0.18.0.

**Not while a group Workload holds quota.** `readyReplicas == 0` does not mean "no reservation". A group's Workload can already hold quota while its Pods pull images. The Workload's `spec.queueName` is immutable while quota is reserved, so the webhook accepted the new label and the reconciler then failed on every retry with `queueName is immutable while workload quota reserved`. The Workload stayed in the old queue ([[issue-17251]]). [[pr-17255]] makes the webhook reject the change if **any** Workload of the LWS holds a quota reservation. LWS has one Workload per group, so `hasWorkloadWithQuotaReservation` lists them all through the `OwnerReferenceUID` index. The lookup runs only when the queue name changes to a non-empty value on an LWS with no Ready replicas. The check is the shared `jobframework.ValidateQueueNameUpdate`, also used by StatefulSet (see [[integration-statefulset#Queue changes are rejected while the Workload holds quota]]). The webhook reads from the informer cache, so a reservation made just before the update can still slip through (source: pr-17255.md, raw/kueue/pkg/controller/jobs/leaderworkerset/leaderworkerset_webhook.go).

Releases: `main` (merged 2026-10-16), release-0.20 ([[pr-17307]]) and release-0.19 ([[pr-17310]]). All merged after v0.20.2 / v0.19.9, so the next patch releases are the first to include it. The 0.19 backport keeps the StatefulSet lookup on `findWorkloadName` + `client.Get` and has unit tests only, because that branch has no LWS controller integration suite (source: pr-17310.md).

### `WorkloadKeyForLeaderWorkerSet` helper

The integration's lookup key (used to map LWS objects back to their owning Workload) was unified into `WorkloadKeyForLeaderWorkerSet()` in #8843. The helper reduces several duplicated key-derivation paths to a single function. Cherry-picked to release-0.16 in [[pr-10945]].

### PodTemplate metadata propagation (#10330)

Labels/annotations on the LWS PodTemplate now propagate into the Workload's PodSets so they are also visible to admission-check controllers (e.g. ProvisioningRequest). Closes the long-standing [[issue-10326]].

## `queue-name` is backfilled onto adopted Pods

When the `queue-name` write moved from the LWS **pod reconciler** into the LWS **webhook** (#4932), the webhook began stamping the leader and worker pod *templates* instead of the Pods. Webhooks only run on create/update, so a LeaderWorkerSet admitted **before** that change keeps templates without the label and nothing backfills it.

The failure mode is silent and self-reinforcing (#13968, fixed by [[pr-14138]]; follow-ups [[pr-14602]], [[pr-14603]]):

1. a Pod recreated from such a template starts with no queue name;
2. the Pod integration skips it (`"queue-name label is not set, ignoring the job"`), so no workload annotation is written and the Pod is missing from the `WorkloadSliceNameKey` index;
3. the topology ungater finds no candidates, so the scheduling gates are never removed;
4. `waitForPodsReady` eventually evicts the Workload, the Pods are recreated from the same template, and the loop repeats until `requeueState.count` hits `backoffLimitCount` and the Workload is **deactivated**.

Throughout all of this the Workload reports `Admitted=True` with a valid TAS assignment, so quota looks perfectly healthy — the only symptom is permanently `SchedulingGated` Pods.

`setDefault` now reads the queue name from the LeaderWorkerSet and sets it when **adopting** a Pod, and reconciles it on already-adopted gated Pods — mirroring what the StatefulSet pod reconciler already did. Guarded by `queueName != ""`, so the webhook stays authoritative and `manageJobsWithoutQueueName` behaviour is unchanged.

## Operator-precedence bug in the revision guard

`lwsStsHandler.enqueue` mixed `||` and `&&` without parentheses:

```go
if sts.Status.CurrentRevision == "" || sts.Status.UpdateRevision == "" &&
    sts.Status.CurrentRevision == sts.Status.UpdateRevision {
    return
}
```

Go binds `&&` tighter, so this is `A || (B && C)`; `(B && C)` requires `UpdateRevision == "" && CurrentRevision == UpdateRevision`, which already implies `CurrentRevision == ""`. The whole guard therefore collapsed to `if CurrentRevision == "" { return }`, and **every** StatefulSet status update with a non-empty `CurrentRevision` enqueued a LeaderWorkerSet reconcile — including the steady state with no rollout in progress. Later guards dropped most of them, so it was over-enqueue rather than a correctness failure.

[[pr-14447]] (cherry-picks [[pr-14892]], [[pr-14893]]) extracts a named `revisionChanged` helper that is true only when both revisions are set and differ. The narrowing is safe because this controller watches Pods directly, so the reconcile that removes their scheduling gates does not depend on the StatefulSet event; `Create`, `Delete` and `Generic` on the handler are already no-ops.

**Update (2026-10-21)**: on `main` (v0.20.0) the whole LWS StatefulSet watch, including `lwsStsHandler` and `revisionChanged`, is gone. #16329 removed it together with the rollout-ungating rule it served (see the rollout section below; source: raw/kueue/pkg/controller/jobs/leaderworkerset/). The release-0.19 backport keeps the watch (source: pr-16401.md).

## `WorkloadAnnotation` on LWS Pods

`wasSimulator.TrackPod` needs `kueue.x-k8s.io/workload` on every Pod to map it to its Workload. LWS Pods get it from the shared write site, `getPodSetsInfoFromStatus`, when the Pod integration ungates them. Since [[pr-15412]] (`main` only, merged 2026-10-19) that write is unconditional; before, it required `TopologyAwareScheduling`, `SchedulerLibraryIntegration` or `WaitForPodsReadyUnscheduledTimeout` (source: raw/kueue/pkg/controller/jobframework/reconciler.go, pr-15412.md). See [[job-framework-interface#`kueue.x-k8s.io/workload` is always set on the PodTemplate]].

**Correction (2026-10-21)**: this section said [[pr-15142]] writes the annotation in LWS `setDefault` in two places. That is what the PR description proposed, but the merged commit (98e61efd7, +341/-0) only adds integration and e2e tests that assert the annotation. `leaderworkerset_reconciler.go` does not reference `WorkloadAnnotation` at the snapshot (source: pr-15142.md, raw/kueue/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler.go).

## Empty PodGroups and quota

An evicted LWS Workload with no Pods (e.g. scaled to zero) used to keep its quota reserved; fixed together with StatefulSet, see [[integration-plain-pod#Empty PodGroups of StatefulSet / LeaderWorkerSet]] (source: pr-14578.md). Open issues that reveal current limits: the LWS webhook can be blind to an object created before it is ready ([[issue-15835]]); pod-template shape immutability for non-quota fields ([[issue-15570]]); TAS support for LWS affinity/anti-affinity ([[issue-15057]]).

## Rolling update with a percentage `maxSurge`

`isRollingUpdateWithSurge` used to read `rolloutStrategy.rollingUpdateConfiguration.maxSurge` with `IntOrString.IntValue()`, which discards the `strconv.Atoi` error, so **every percentage read as 0**, `100%` included. `filterWorkloads` is meant to keep Workloads "for all groups including surge replicas" by raising `replicas` to `status.replicas` while a surge rollout is in progress. With the surge read as 0, that never happened, and the Workloads of surge groups that were still running went into `toDelete`. Example: spec 2 replicas, status 3. `maxSurge: 1` gives `toDelete=[]`, but `maxSurge: 50%` gave `toDelete=[group-2]` (source: pr-14405.md).

The reconciler now uses `intstr.GetScaledValueFromIntOrPercent(maxSurge, replicas, true)`, which rounds up as the LWS API documents, and **returns** a parse error instead of folding it to 0. A string that is not a percentage, such as `"3"`, is an error; the LWS webhook rejects such values with the same helper (source: raw/kueue/pkg/controller/jobs/leaderworkerset/leaderworkerset_reconciler.go). Shipped in **v0.20.0, v0.19.7 ([[pr-16402]]) and v0.18.11 ([[pr-16423]])** (source: raw/kueue/CHANGELOG/CHANGELOG-0.20.md, CHANGELOG-0.19.md, CHANGELOG-0.18.md).

## Rollouts: current-revision Pods stay gated until admission

Shared with StatefulSet. During a rolling update, current-revision Pods were ungated before the Workload was admitted. Now they are ungated only after admission. On `main` the LWS StatefulSet watch is removed, and on release-0.19 current-revision LWS Pods also get their default labels, so a Pod recreated mid-rollout joins its pod group. Shipped in v0.20.0, v0.19.7 and v0.18.11. Details: [[integration-statefulset#Rollouts: current-revision Pods stay gated until admission]] (source: pr-16401.md).

## Legacy finalizer cleanup removed (v0.20)

The migration code that removed the legacy `kueue.x-k8s.io/managed` finalizer from parent-suspended Pods is gone from the LWS reconciler, together with the `SkipFinalizersForPodsSuspendedByParent` gate. See [[integration-statefulset#Legacy parent-suspended Pod finalizer cleanup removed (v0.20)]] ([[pr-13316]]).

## Default WorkloadPriorityClass is not added on update to a running LWS

The LWS mutating webhook also runs on update. With `WorkloadPriorityClassDefaulting` it used to add `kueue.x-k8s.io/priority-class: default` to an LWS created before the `default` class existed, and the validating webhook then rejected every update to a Ready LWS, even one Kueue does not manage. `Default` now reads the old object and applies the default class only if `CanSetWorkloadPriorityClassName(old.status.readyReplicas == 0, old)` is true ([[pr-16474]]). See [[workload-priority#Default WorkloadPriorityClass is skipped on updates to running serving workloads]] (source: raw/kueue/pkg/controller/jobs/leaderworkerset/leaderworkerset_webhook.go).

## LWS v1.0.0 (main)

`main` vendors `sigs.k8s.io/lws` **v1.0.0**, the first stable LWS release (was v0.11.1). The e2e operator install and the integration-test CRDs follow the `go.mod` version. Kueue code did not change: the new API is additive and opt-in. It adds `spec.podTerminationPolicy` (`Sequential` default, or `Parallel`), `leaderWorkerTemplate.maxGroupRestarts` and `restartBackoff`, a `Degraded` condition, and annotations plus a Pod finalizer used only when `maxGroupRestarts` is set. The CRD now defaults `spec.rolloutStrategy` to `{type: RollingUpdate}`. Kueue does not read any of the new fields (source: pr-17504.md).

## Missing WorkloadPriorityClass

LWS resolves `kueue.x-k8s.io/priority-class` **once per component** (`PrepareWorkloadPriority` per group Workload). A label naming a missing class therefore emits one `WorkloadPriorityClassNotFound` Warning per component. The events are identical on the same object, so they fold into one event with a count. #13820 tracks resolving the class once per reconcile (source: pr-13775.md). See [[workload-priority#Missing WorkloadPriorityClass: Warning event]].

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — leader + workers PodSet shape.
- [[topology-aware-scheduling]] — co-scheduling leaders and workers.
- [[integration-statefulset]]
- [[integration-plain-pod]]
- [[workload-priority]]
