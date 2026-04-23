# Issue #4028: Preemption doesn't happened for guaranteed resource

**Summary**: Preemption doesn't happened for guaranteed resource

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4028

**Last updated**: 2025-06-25T04:05:55Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@and-1](https://github.com/and-1)
- **Created**: 2025-01-21T08:52:11Z
- **Updated**: 2025-06-25T04:05:55Z
- **Closed**: 2025-06-25T04:05:54Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

**What happened**: There are two CQ for teams without cpu/ram guaranteed resources and one CQ for capacity management. CQ1 configured with nominalQuota=1 for resource nvidia.com/gpu. I apply job2 to CQ2 (without any guaranteed resources) and after job1 to CQ1 and preemption doesn't happened for job1. Message from WL status
```
message: 'couldn''t assign flavors to pod set main: insufficient unused quota
      for cpu in flavor a100, 2 more needed, insufficient unused quota for memory
      in flavor a100, 2Gi more needed'
```

**What you expected to happen**:
job1 will preempt job2.

**How to reproduce it (as minimally and precisely as possible)**:

CQ1

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "team1"
spec:
  cohort: default
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: TryNextFlavor
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
    flavors:
    - name: "a100"
      resources:
      - name: "cpu"
        nominalQuota: 0
      - name: "memory"
        nominalQuota: 0
      - name: "nvidia.com/gpu"
        nominalQuota: 1
```

CQ2

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "team2"
spec:
  cohort: default
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
  flavorFungibility:
    whenCanBorrow: TryNextFlavor
    whenCanPreempt: TryNextFlavor
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
    flavors:
    - name: "a100"
      resources:
      - name: "cpu"
        nominalQuota: 0
      - name: "memory"
        nominalQuota: 0
      - name: "nvidia.com/gpu"
        nominalQuota: 0
```

CQ3

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "unallocated-resources"
spec:
  cohort: default
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu", "memory", "nvidia.com/gpu"]
    flavors:
    - name: "a100"
      resources:
      - name: "cpu"
        nominalQuota: 2
      - name: "memory"
        nominalQuota: 2Gi
      - name: "nvidia.com/gpu"
        nominalQuota: 1
```
```
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "a100"
spec:
  nodeLabels:
    flavor.kueue.x-k8s.io/a100: "true"
  tolerations:
  - effect: NoSchedule
    key: flavor.kueue.x-k8s.io/a100
    operator: "Exists"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: "team1-lq"
spec:
  clusterQueue: "team1"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: "team2-lq"
spec:
  clusterQueue: "team2"
```

job1

```
apiVersion: batch/v1
kind: Job
metadata:
  name: job1
  labels:
    kueue.x-k8s.io/queue-name: team1-lq
spec:
  parallelism: 1
  completions: 1
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["10m"]
        resources:
          limits:
            cpu: 2
            memory: "2Gi"
            nvidia.com/gpu: 1
      restartPolicy: Never
```

job2

```
apiVersion: batch/v1
kind: Job
metadata:
  name: job2
  labels:
    kueue.x-k8s.io/queue-name: team2-lq
spec:
  parallelism: 1
  completions: 1
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["10m"]
        resources:
          limits:
            cpu: 2
            memory: "2Gi"
            nvidia.com/gpu: 1
      restartPolicy: Never
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):  v1.29.0
- Kueue version (use `git describe --tags --dirty --always`): 0.10.0
- OS (e.g: `cat /etc/os-release`): Debian 11
- Kernel (e.g. `uname -a`): 6.1.0-0.deb11.17-amd64

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-21T09:32:39Z

I haven't run the experiment, but my first thought is that job1 needs to also borrow (cpu, because it requests 2 cpu, but it is not provided by nominal quota of CQ1), and preemption while borrowing is not enabled (preemption.borrowWithinCohort), so seem WAI.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-21T09:33:01Z

cc @gabesaba as related to scheduling

### Comment by [@and-1](https://github.com/and-1) — 2025-01-21T10:10:44Z

It's a little bit confuse, job without any guaranteed resources cann't be preempted by job with guaranteed resource. It's expected, for example, in case when CQ2 has cpu guarantee, CQ1 - nvidia.com/gpu and scheduler could not decide which one win without any resource priority algorithm.
Also i thought that my case managed by preemption.reclaimWithinCohort parameter

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-22T13:21:56Z

> guaranteed resources cann't be preempted by job with guaranteed resource.

What do you mean "job with guaranteed resource"? job1 requires "cpu" which is not provided by nominal quota of CQ1.

> Also i thought that my case managed by preemption.reclaimWithinCohort parameter

Due to the need to borrow "cpu" the `job1` needs to borrow, and as such it cannot preempt, even reclaim, unless the `preemption.borrowWIthinCohort` is enabled.

### Comment by [@and-1](https://github.com/and-1) — 2025-01-25T10:53:21Z

> What do you mean "job with guaranteed resource"? job1 requires "cpu" which is not provided by nominal quota of CQ1.

Gpu provided by CQ1, cpu/ram - not, I expect that kueue provides gpu for job1 in best effort mode. I'll try to explain what i mean: we submit job2, usage of CQ2 (for all resources) will above nominal quota. After submitting job1, gpu resource will be equal nominal quota CQ1 and should be provided by kueue (if possible). Kueue should scan all CQ in cohort and if finds CQ (in our case CQ2) with borrowed resources and after preempting usage of CQ still equal or above nominal quotas, so it should preempt that workload (in our case job2). Another words - job1 requested resources more guaranteed then job2 resources

> Due to the need to borrow "cpu" the job1 needs to borrow, and as such it cannot preempt, even reclaim, unless the preemption.borrowWIthinCohort is enabled.

if it should be handled by borrowWIthinCohort parameter - ok, but now supported only borrow based on workload priority, not based on quota conditions

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-25T11:44:14Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-25T11:45:54Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-25T04:05:49Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-25T04:05:55Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4028#issuecomment-3002997098):

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
