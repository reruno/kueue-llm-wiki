# Integration: LeaderWorkerSet (LWS)

**Summary**: LeaderWorkerSet is a SIG-Apps API for running groups of Pods where each group has a designated leader and a number of followers. It targets inference serving (disaggregated prefill/decode) and training with tightly-coupled worker groups. Kueue integrates per-group, treating a leader+workers as one gang.

**Sources**: `raw/github/kubernetes-sigs__kueue/`.

**Last updated**: 2026-04-23

---

## Shape

An LWS defines `spec.leaderWorkerTemplate` (leader + workers) and `spec.replicas` groups. Total Pods = `replicas × (1 + workers.size)`.

Kueue's integration represents this as two PodSets per group or a combined PodSet, depending on the shape — the MVP support (source: issue-3232.md — MVP support for serving workloads running as LeaderWorkerSet) landed with leader-and-workers counted together. Rank-based placement of leaders and followers across topology domains became a TAS-specific feature (source: issue-4531.md — TAS: support co-scheduling (and rank-based ordering) of leaders and workers for LWS groups).

## Startup policies and scaling

LWS supports `startupPolicy: LeaderCreated` or `LeaderReady`. Kueue's integration must handle both: in LeaderReady mode, the workers are created after the leader is Ready, which affects PodsReady accounting. Flaky tests around scaling cover this (source: issue-4374.md, source: issue-4626.md, source: issue-4674.md — scaling up/down LeaderReady/LeaderCreated).

## Name length

"Kueue fails for run LWS with long name" (source: issue-10032.md) — a naming-collision/derivation edge case specific to the integration.

## NodeSelector mutation

Admission-check-applied node selectors or flavor-injected selectors need to reach the LWS Pod templates. "Allow to mutate nodeSelector for LWS" (source: issue-10178.md) was the tracking issue.

## PodTemplate metadata propagation

"Propagate LeaderWorkerSet PodTemplate metadata to PodSet" (source: issue-10326.md) — labels/annotations on the LWS template must flow into the Workload's PodSet and back to Pods.

## WorkloadPriorityClass on LWS

LWS with WorkloadPriorityClass had specific flakes around PodTemplate updates (source: issue-4744.md — Should allow to update the PodTemplate in LeaderWorkerSet).

## Naming consistency

"[LWS] Use consistent naming for prebuilt workload across the codebase" (source: issue-4324.md) — an internal hygiene issue.

## Related pages

- [[integrations]] — integration mechanics.
- [[workload]] — leader + workers PodSet shape.
- [[topology-aware-scheduling]] — co-scheduling leaders and workers.
