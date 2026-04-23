# Issue #4333: ClusterQueue not reclaiming resources from high-weight ClusterQueue in cohort

**Summary**: ClusterQueue not reclaiming resources from high-weight ClusterQueue in cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4333

**Last updated**: 2025-03-06T15:23:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yuvalaz99](https://github.com/yuvalaz99)
- **Created**: 2025-02-20T08:31:07Z
- **Updated**: 2025-03-06T15:23:51Z
- **Closed**: 2025-03-06T15:23:50Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When a ClusterQueue is configured with nominalQuota and reclaimWithinCohort: any, it cannot reclaim resources from another queue that has nominalQuota: 0 but an extremely high weight.

**setup:**

ClusterQueueA:
- nominalQuota: 4
- reclaimWithinCohort: any

ClusterQueueB:
- nominalQuota: 0
- weight: 9999999


**What you expected to happen**:

Since ClusterQueueB is using more than its nominal quota (which is 0), preemption should occur, allowing ClusterQueueA to reclaim resources. This aligns with the reclaimWithinCohort definition:

"Determines whether a pending Workload can preempt Workloads from other ClusterQueues in the cohort that are using more than their nominal quota."

However, no preemption occurs.

**Observed Behavior:**

- Despite ClusterQueueB exceeding its nominal quota, ClusterQueueA is unable to reclaim resources.
- The weightedShare of ClusterQueueB remains 0, which might be preventing preemption.
- No scheduler logs indicate an attempt to preempt.

Is this expected behavior, or is there a misalignment in how weighted share interacts with reclaimWithinCohort?

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.30
- Kueue version (use `git describe --tags --dirty --always`): 0.10.0
- Cloud provider or hardware configuration: GCP
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-20T11:48:06Z

> The weightedShare of ClusterQueueB remains 0, which might be preventing preemption.

I suspect this to be the root cause - that when weight is high, the weightedShare collapses to zero. This is a known issue, which we are tracking in #4247

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-03-06T15:23:45Z

/close

In favor of #4247. Until that issue is fixed, is it acceptable to scale your weights to be smaller?

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-06T15:23:50Z

@gabesaba: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4333#issuecomment-2704165942):

>/close
>
>In favor of #4247. Until that issue is fixed, is it acceptable to scale your weights to be smaller?


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
