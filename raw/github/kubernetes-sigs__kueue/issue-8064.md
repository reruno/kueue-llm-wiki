# Issue #8064: Scheduler repeatedly logs preemption attempts and blocks other workloads

**Summary**: Scheduler repeatedly logs preemption attempts and blocks other workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8064

**Last updated**: 2025-12-03T23:48:57Z

---

## Metadata

- **State**: closed (duplicate)
- **Author**: [@sfc-gh-srudenko](https://github.com/sfc-gh-srudenko)
- **Created**: 2025-12-03T20:51:25Z
- **Updated**: 2025-12-03T23:48:57Z
- **Closed**: 2025-12-03T23:48:57Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 0

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The Kueue scheduler is repeatedly printing the same log messages ~40 times per second for a single workload. While this is happening, Kueue does not admit any other workloads - even those in different ClusterQueues that have free nodes and available quota. Those jobs remain stuck in the Suspended state until the spam stops.

Here is the log sequence that loops continuously:

```
{"level":"Level(-2)","ts":"2025-12-03T20:18:40.916603081Z","logger":"scheduler","caller":"scheduler/scheduler.go:254","msg":"Attempting to schedule workload","schedulingCycle":245469,"workload":{"name":"job-xc-b200-a204b","namespace":"mltraining-dev"},"clusterQueue":{"name":"research-modeling"},"parentCohort":{"name":"research"},"rootCohort":{"name":"snowflake"}}
{"level":"Level(-2)","ts":"2025-12-03T20:18:40.916627433Z","logger":"scheduler","caller":"scheduler/scheduler.go:257","msg":"Workload requires preemption, but there are no candidate workloads allowed for preemption","schedulingCycle":245469,"workload":{"name":"job-xc-b200-a204b","namespace":"mltraining-dev"},"clusterQueue":{"name":"research-modeling"},"parentCohort":{"name":"research"},"rootCohort":{"name":"snowflake"},"preemption":{"reclaimWithinCohort":"Any","borrowWithinCohort":{"policy":"Never"},"withinClusterQueue":"Never"}}
{"level":"Level(-2)","ts":"2025-12-03T20:18:40.916670248Z","logger":"scheduler","caller":"scheduler/scheduler.go:763","msg":"Workload re-queued","schedulingCycle":245469,"workload":{"name":"job-xc-b200-a204b","namespace":"mltraining-dev"},"clusterQueue":{"name":"research-modeling"},"queue":{"name":"research-modeling","namespace":"mltraining-dev"},"requeueReason":"","added":true,"status":""}
{"level":"debug","ts":"2025-12-03T20:18:40.916722867Z","logger":"events","caller":"recorder/recorder.go:104","msg":"couldn't assign flavors to pod set main: flavor sky-pool-b200 doesn't match node affinity, flavor sky-pool-b300 doesn't match node affinity, flavor sky-pool-b300-raid0 doesn't match node affinity, flavor sky-pool-h200 doesn't match node affinity, insufficient unused quota for nvidia.com/gpu in flavor sky-pool-b200-raid0, 1 more needed","type":"Warning","object":{"kind":"Workload","namespace":"mltraining-dev","name":"job-xc-b200-a204b","uid":"b8785b54-26a3-407d-840d-01e64d32468a","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"2310887017"},"reason":"Pending"}
```

Additional details:
- Scheduler logs this loop constantly (≈40 lines/sec).
- While this happens, other workloads in unrelated ClusterQueues do not get processed.
- The message “insufficient unused quota for nvidia.com/gpu in flavor sky-pool-b200-raid0” appears incorrect - at that moment a full node with 8 GPUs was completely free.
- Issue is intermittent and happens randomly.

**What you expected to happen**:
Kueue should not get stuck retrying a single workload endlessly, and it should continue scheduling workloads in other ClusterQueues. Quota/flavor calculations should not appear stale.


**How to reproduce it (as minimally and precisely as possible)**:
The issue happens intermittently and is not easy to reproduce deterministically. It appears during normal workload submission. Happy to provide more state dumps if needed.


**Anything else we need to know?**:
It was suggested that this is likely a bug because Kueue should not repeatedly re-attempt scheduling in a tight loop or spam logs like this.

**Environment**:
- Kubernetes version (use `kubectl version`): `Server Version: v1.31.13-eks-3cfe0ce`
- Kueue version (use `git describe --tags --dirty --always`):  `v0.13.10`
- Cloud provider or hardware configuration: AWS EKS
