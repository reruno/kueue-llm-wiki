# Integration: LeaderWorkerSet (LWS)

**Summary**: LeaderWorkerSet is a SIG-Apps API for running groups of Pods where each group has a designated leader and a number of followers. It targets inference serving (disaggregated prefill/decode) and training with tightly-coupled worker groups. Kueue integrates per-group, treating a leader+workers as one gang.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

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

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — leader + workers PodSet shape.
- [[topology-aware-scheduling]] — co-scheduling leaders and workers.
