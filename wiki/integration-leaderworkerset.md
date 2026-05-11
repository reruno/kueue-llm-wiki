# Integration: LeaderWorkerSet (LWS)

**Summary**: LeaderWorkerSet is a SIG-Apps API for running groups of Pods where each group has a designated leader and a number of followers. It targets inference serving (disaggregated prefill/decode) and training with tightly-coupled worker groups. Kueue integrates per-group, treating a leader+workers as one gang.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-05-08

---

## Shape

An LWS defines `spec.leaderWorkerTemplate` (leader + workers) and `spec.replicas` groups. Total Pods = `replicas × (1 + workers.size)`.

Kueue's integration represents this as two PodSets per group or a combined PodSet, depending on the shape — the MVP support ([[issue-3232]] — MVP support for serving workloads running as LeaderWorkerSet) landed with leader-and-workers counted together. Rank-based placement of leaders and followers across topology domains became a TAS-specific feature ([[issue-4531]] — TAS: support co-scheduling (and rank-based ordering) of leaders and workers for LWS groups).

## Startup policies and scaling

LWS supports `startupPolicy: LeaderCreated` or `LeaderReady`. Kueue's integration must handle both: in LeaderReady mode, the workers are created after the leader is Ready, which affects PodsReady accounting. Flaky tests around scaling cover this ([[issue-4374]], [[issue-4626]], [[issue-4674]] — scaling up/down LeaderReady/LeaderCreated).

## Name length

"Kueue fails for run LWS with long name" ([[issue-10032]]) — a naming-collision/derivation edge case specific to the integration.

## NodeSelector mutation

Admission-check-applied node selectors or flavor-injected selectors need to reach the LWS Pod templates. "Allow to mutate nodeSelector for LWS" ([[issue-10178]]) was the tracking issue.

## PodTemplate metadata propagation

"Propagate LeaderWorkerSet PodTemplate metadata to PodSet" ([[issue-10326]]) — labels/annotations on the LWS template must flow into the Workload's PodSet and back to Pods.

## WorkloadPriorityClass on LWS

LWS with WorkloadPriorityClass had specific flakes around PodTemplate updates ([[issue-4744]] — Should allow to update the PodTemplate in LeaderWorkerSet).

## Naming consistency

"[LWS] Use consistent naming for prebuilt workload across the codebase" ([[issue-4324]]) — an internal hygiene issue.

## v0.18.0 behaviour changes

### Relaxed PodSpec validation — `nodeSelector` is mutable on running LWS

The LWS validation webhook previously rejected `PodTemplate.Spec` mutation while a Workload was admitted, which blocked operators from rolling node-selector updates onto an already-running LWS (typical when migrating between accelerator pools). v0.18.0 (#10275, with cherry-pick [[pr-10944]] and [[pr-10930]]) relaxes the validation so `nodeSelector` can be changed; other PodSpec fields remain restricted.

### Mutating `queue-name` while idle

When `status.readyReplicas == 0` (no live group), `kueue.x-k8s.io/queue-name` may now be re-labeled on the LWS itself — useful for moving an LWS to a different LocalQueue without recreating it. Released as #4932 in v0.18.0.

### `WorkloadKeyForLeaderWorkerSet` helper

The integration's lookup key (used to map LWS objects back to their owning Workload) was unified into `WorkloadKeyForLeaderWorkerSet()` in #8843. The helper reduces several duplicated key-derivation paths to a single function. Cherry-picked to release-0.16 in [[pr-10945]].

### PodTemplate metadata propagation (#10330)

Labels/annotations on the LWS PodTemplate now propagate into the Workload's PodSets so they are also visible to admission-check controllers (e.g. ProvisioningRequest). Closes the long-standing [[issue-10326]].

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — leader + workers PodSet shape.
- [[topology-aware-scheduling]] — co-scheduling leaders and workers.
