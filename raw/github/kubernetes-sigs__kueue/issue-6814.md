# Issue #6814: Fail to preempt an older low-priority job when borrowing within cohort

**Summary**: Fail to preempt an older low-priority job when borrowing within cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6814

**Last updated**: 2025-12-17T10:12:04Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@xiongzubiao](https://github.com/xiongzubiao)
- **Created**: 2025-09-12T18:18:18Z
- **Updated**: 2025-12-17T10:12:04Z
- **Closed**: 2025-12-17T10:10:34Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I have 3 ClusterQueues within a cohort: the first one is a placeholder that holds the nominal quota, the other two are borrowing from the placeholder and taking workloads.

It can happen that a newer job with higher priority fails to preempt an older job with lower priority. I submitted 3 Jobs in the following order (Note that order matters):
1. The 1st Job is submitted to the 2nd CQ with high priority. It requests more than the cohort's total quota, so that it won't be admitted.
2. The 2nd Job is submitted to the 3rd CQ with low priority. It requests exactly the cohorts' total quota, so that it will be borrowing from the 1st CQ and admitted.
3. The 3rd Job is submitted to the 2nd CQ with high priority. It also requests exactly the cohort's total quota. Supposedly, it will preempt the 2nd Job, but it doesn't from my experiment.

See the yaml files in `How to reproduce it` section.

There are following errors in Kueue's log:

> {"level":"error","ts":"2025-09-12T17:54:06.963558903Z","logger":"scheduler","caller":"scheduler/scheduler.go:307","msg":"Failed to preempt workloads","schedulingCycle":14,"workload":{"name":"job-high-priority-preempting-579a3","namespace":"default"},"clusterQueue":{"name":"cq-high"},"parentCohort":{"name":"default"},"rootCohort":{"name":"default"},"error":"Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"job-low-priority-preemptible-67e5e\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule\n\t/workspace/pkg/scheduler/scheduler.go:307\nsigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1\n\t/workspace/pkg/util/wait/backoff.go:43\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255\nk8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233\nsigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff\n\t/workspace/pkg/util/wait/backoff.go:42\nsigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff\n\t/workspace/pkg/util/wait/backoff.go:34"}

It seems that Kueue tried to preempt the older low-priority job, but failed because of unable to update the workload status.

**What you expected to happen**:

A high-priority job should be able to preempt a low-priority job.

**How to reproduce it (as minimally and precisely as possible)**:

<details>
<summary>ResourceFlavor, ClusterQueues, LocalQueues, and WorkloadPriorityClasses:</summary>

```yaml
kind: ResourceFlavor
apiVersion: kueue.x-k8s.io/v1beta1
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cq-placeholder"
spec:
  namespaceSelector: {} # match all.
  cohort: default
  resourceGroups:
  - coveredResources: [ "cpu" ]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 6
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  preemption:
    borrowWithinCohort:
      policy: LowerPriority
    reclaimWithinCohort: LowerPriority
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cq-high"
spec:
  namespaceSelector: {} # match all.
  cohort: default
  resourceGroups:
  - coveredResources: [ "cpu" ]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 0
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  preemption:
    borrowWithinCohort:
      policy: LowerPriority
    reclaimWithinCohort: LowerPriority
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cq-low"
spec:
  namespaceSelector: {} # match all.
  cohort: default
  resourceGroups:
  - coveredResources: [ "cpu" ]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 0
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  preemption:
    borrowWithinCohort:
      policy: LowerPriority
    reclaimWithinCohort: LowerPriority
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "lq-high"
spec:
  clusterQueue: "cq-high"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "lq-low"
spec:
  clusterQueue: "cq-low"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: priority-high
value: 10000
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: WorkloadPriorityClass
metadata:
  name: priority-low
value: -10000
```

</details>

<details>
<summary>Jobs:</summary>

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: high-priority-over-quota
  labels:
    kueue.x-k8s.io/queue-name: lq-high
    kueue.x-k8s.io/priority-class: priority-high
spec:
  template:
    spec:
      containers:
      - name: dummy-job
        image: registry.k8s.io/e2e-test-images/agnhost:2.53
        args: [ "pause" ]
        resources:
          requests:
            cpu: "12"
      restartPolicy: Never
---
apiVersion: batch/v1
kind: Job
metadata:
  name: low-priority-preemptible
  labels:
    kueue.x-k8s.io/queue-name: lq-low
    kueue.x-k8s.io/priority-class: priority-low
spec:
  template:
    spec:
      containers:
      - name: dummy-job
        image: registry.k8s.io/e2e-test-images/agnhost:2.53
        args: [ "pause" ]
        resources:
          requests:
            cpu: "6"
      restartPolicy: Never
---
apiVersion: batch/v1
kind: Job
metadata:
  name: high-priority-preempting
  labels:
    kueue.x-k8s.io/queue-name: lq-high
    kueue.x-k8s.io/priority-class: priority-high
spec:
  template:
    spec:
      containers:
      - name: dummy-job
        image: registry.k8s.io/e2e-test-images/agnhost:2.53
        args: [ "pause" ]
        resources:
          requests:
            cpu: "6"
      restartPolicy: Never
```
Note that the order matters. The jobs must be submitted in the order that they are showing in the yaml, to reproduce the issue.

</details>

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.33.4+k3s1
- Kueue version (use `git describe --tags --dirty --always`): v0.13.3
- Cloud provider or hardware configuration: I think it doesn't matter
- OS (e.g: `cat /etc/os-release`): Ubuntu 22.04.5 LTS
- Kernel (e.g. `uname -a`): 5.15.0-142-generic
- Install tools: kubectl with manifest yamls
- Others:

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-25T02:31:06Z

I think you may actually be encountering head of CQ blocking. See if this problem is similar: https://github.com/kubernetes-sigs/kueue/issues/6929

Specifically, you're submitting 2 workloads to cq-high. The first inadmissible one is blocking the admission of the second admissible one. And this is a bug.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-09-25T17:34:22Z

It looks it is. The issue is gone if the first inadmissible workload doesn't exist or it is submitted later than others.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-11-06T17:12:19Z

@xiongzubiao I believe the issues should be solved with #7157. Can you verify with one of more recent releases that it solved your issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T10:10:29Z

Actually, it doesn't look to me like https://github.com/kubernetes-sigs/kueue/pull/7157. From the logs we see the preemption was attempted, but it failed due to conflict. I suppose it was not retried. For this bug we fixed another issue: https://github.com/kubernetes-sigs/kueue/pull/7665

This could also explain the flaky nature of the problem as it didn't re-occur later per: https://github.com/kubernetes-sigs/kueue/issues/6814#issuecomment-3335200546

/close
As it looks like solved already. @xiongzubiao if you still observe the issue (on 0.15.1+ or 0.14.5+ which contain https://github.com/kubernetes-sigs/kueue/pull/7665) feel free to re-open or open another issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-17T10:10:35Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6814#issuecomment-3664629524):

>Actually, it doesn't look to me like https://github.com/kubernetes-sigs/kueue/pull/7157. From the logs we see the preemption was attempted, but it failed due to conflict. I suppose it was not retried. For this bug we fixed another issue: https://github.com/kubernetes-sigs/kueue/pull/7665
>
>This could also explain the flaky nature of the problem as it didn't re-occur later per: https://github.com/kubernetes-sigs/kueue/issues/6814#issuecomment-3335200546
>
>/close
>As it looks like solved already. @xiongzubiao if you still observe the issue feel free to re-open or open another issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
