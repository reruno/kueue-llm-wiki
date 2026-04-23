# Issue #5937: Incorrect admission due to wrong borrowable resource when a cluster queue in cohort is deleted

**Summary**: Incorrect admission due to wrong borrowable resource when a cluster queue in cohort is deleted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5937

**Last updated**: 2025-07-18T15:34:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@qti-haeyoon](https://github.com/qti-haeyoon)
- **Created**: 2025-07-11T05:18:57Z
- **Updated**: 2025-07-18T15:34:28Z
- **Closed**: 2025-07-18T15:34:28Z
- **Labels**: `kind/bug`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
ClusterQueue can admit a workload incorrectly through borrowing even when a ClusterQueue in the same cohort is deleted and no borrowable resource is present.

**What you expected to happen**:
When ClusterQueue is deleted, borrowable resources of ClusterQueues in the same cohort should be updated automatically to keep the borrowable resources up-to-date.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create two ClusterQueues in the same cohort and LocalQueues for respective CQs:
  ```yaml
  apiVersion: kueue.x-k8s.io/v1beta1
  kind: ResourceFlavor
  metadata:
    name: default-flavor
  spec: {}
  ---
  # Create two cluster queues in the same cohort
  # 8 CPU nominal quota and 0 CPU nominal quota respectively.
  # cluster queue with 0 CPU nominal quota will have to borrow from the other to admit workloads.
  apiVersion: kueue.x-k8s.io/v1beta1
  kind: ClusterQueue
  metadata:
    name: cluster-queue-1
  spec:
    cohort: bug-test
    namespaceSelector: {}
    resourceGroups:
    - coveredResources: ["cpu"]
      flavors:
      - name: "default-flavor"
        resources:
          - name: cpu
            nominalQuota: "8"
  ---
  apiVersion: kueue.x-k8s.io/v1beta1
  kind: ClusterQueue
  metadata:
    name: cluster-queue-2
  spec:
    cohort: bug-test
    namespaceSelector: {}
    resourceGroups:
    - coveredResources: ["cpu"]
      flavors:
      - name: "default-flavor"
        resources:
          - name: cpu
            nominalQuota: "0"
  ---
  # Create local queues for the corresponding cluster queues.
  apiVersion: kueue.x-k8s.io/v1beta1
  kind: LocalQueue
  metadata:
    name: local-queue-1
    namespace: test
  spec:
    clusterQueue: cluster-queue-1
  ---
  apiVersion: kueue.x-k8s.io/v1beta1
  kind: LocalQueue
  metadata:
    name: local-queue-2
    namespace: test
  spec:
    clusterQueue: cluster-queue-2
  
  ```
2. Delete **cluster-queue-1** which has 8 CPU nominal quota. This will result in 0 borrowable CPU and 0 nominal CPU quota for **cluster-queue-2**
3. Create a pod which requests 8 CPU to **cluster-queue-2**. This is supposed to be scheduling gated but you'll see it pending, passing the admission.
```yaml
# A pod requesting 8 CPUs
apiVersion: v1
kind: Pod
metadata:
  name: pod-8-cpu
  namespace: test
  labels:
    kueue.x-k8s.io/queue-name: local-queue-2
spec:
  containers:
  - name: sleep
    command: ["sleep", "infinity"]
    image: busybox:stable
    resources:
      requests:
        cpu: "8"
```

**Anything else we need to know?**:

We can remediate this situation by:
* Restarting the Kueue controller manager.
* Submitting another workload in cluster-queue-2 (which seems to trigger sync).

However since there could be an incorrect admission until we take this remediation, it'd be best if controller could remediate by itself.

**Environment**:
- Kubernetes version (use `kubectl version`): v1.29.4
- Kueue version (use `git describe --tags --dirty --always`): v0.12.4 (latest) and v0.11.6

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-11T05:40:50Z

cc @gabesaba

### Comment by [@amy](https://github.com/amy) — 2025-07-13T23:40:35Z

I am able to replicate this issue locally. I'm going to...
1. Take a look at whether a ClusterQueue deletion triggers an event for LocalQueue
2. Take a look at when the cache representation of the tree gets synced after a ClusterQueue deletion
3. If the cache does get synced after a ClusterQueue deletion, what it looks like

### Comment by [@amy](https://github.com/amy) — 2025-07-15T04:08:11Z

Adding findings here so folks can follow along / correct me as I debug:

For this line: `cqName, cqOk := r.queues.ClusterQueueForWorkload(&wl)`
I added a log here to print the values for cqName and cqOk, I get:
`clusterQueue:  cluster-queue-2, cq exists:  true`

https://github.pie.apple.com/kubernetes-sigs/kueue/blob/main/pkg/controller/core/workload_controller.go#L298

### Comment by [@amy](https://github.com/amy) — 2025-07-15T05:32:11Z

I think I found a fix! The issue is within `cache.DeleteClusterQueue` function. We need to add ` updateCohortTreeResources(parent)` after clusterqueue deletion. 

I see the pod with `SchedulingGated` locally. Will send up a PR in the upcoming days! (need a second to get approvals with my employer)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-15T07:19:04Z

Awesome, this sounds quite reasonable! I think ideally the fix is accompanied by an integration test.

### Comment by [@amy](https://github.com/amy) — 2025-07-15T16:40:17Z

For curiosity purposes, is this an issue? https://github.com/kubernetes-sigs/kueue/issues/5937#issuecomment-3071819429

Want to make sure my solution isn't roundabout. Specifically, this means that `queues *queue.Manager` in `WorkloadReconciler` still sees this workload attached to the deleted cq. My solution separately triggers the `cache` to reconcile the resources to prevent pod admission. But the `queue` representation sees the deleted cq even after cq deletion. Which means the deletion event isn't reconciling the queue. 

Prior to my local fix, when I print its:
--delete cq 1--

1. logs from cq controller - triggers cq delete event

--submit workload--

2. logs from workload controller -  workload has reservation
3. logs from workload controller - workload queue.Manager returns deleted CQ as workload's CQ

I would expect my fix (that updates `cache` resource tree) to resolve 2. But also, 3 is weird because I would have expected the workload controller `queue` representation to have been updated. The workload should be orphaned.

@mimowo ^

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T08:50:30Z

Maybe @gabesaba can answer in more detail, but AFAIK deleting the CQ from `queues` sounds like a proper fix, here are more details:

> logs from workload controller - workload has reservation

This sounds expected. Even though the quota for cohort is reduced, the Workload still has the `QuotaReserved` condition. Kueue does not have a mechanism to preempt due to reduced quota (either by lowering the numbers or deleting a CQ contributing to the cohort's quota). So, as a result CQs and cohorts may run over-committed for a while. 

We may consider supporting triggering preemptions in this case, but I would call it out-of-scope, and limit the scope of the issue to only prevent "new" admissions.

> logs from workload controller - workload queue.Manager returns deleted CQ as workload's CQ

Is the workload targeting the deleted CQ, or the other one in the cohort?
- if the other CQ (local-queue-2, as in the Issue description), then it is perfectly ok. 
- if the workload is targeting local-queue-1, then indeed the internal functions may get confused, because the `local-queue-1` is remembered at the [QueueName status field](https://github.com/kubernetes-sigs/kueue/blob/f4a78e032c0d116860d7dff15d445952a65e6904/apis/kueue/v1beta1/workload_types.go#L42). So, if `local-queue-1` exists, while `cluster-queue-1` is deleted, then it might be confusing, but we generally prevent it with finalizers. Let me know if you want to explore these scenarios more.

### Comment by [@amy](https://github.com/amy) — 2025-07-16T16:06:23Z

ah ok nevermind. Yeah the workload is targeting `cluster-queue-2`, so not the deleted one. Alrighty! I'll go ahead with my original suggestion: updating `cache.DeleteClusterQueue` function.

This is interesting. I didn't realize when borrowing, that a workload borrows from a specific clusterQueue. I falsely assumed that the cohort aggregates unallocated guarantees. And that when a clusterQueue needs to borrow, that it borrows from an aggregated pool. (😂 assumption made from not reading the code)

@mimowo Re: running overcommitted, yeah... I think eventual consistency may actually be preferable here (ie not preempting in the scenario you described). So for instance, if we're running migrations with cohorts (moving quota around), it'd be nice for already running workloads to have a somewhat graceful end & finish using their granted reservation, then just block on admission.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-16T17:09:54Z

> This is interesting. I didn't realize when borrowing, that a workload borrows from a specific clusterQueue. I falsely assumed that the cohort aggregates unallocated guarantees. And that when a clusterQueue needs to borrow, that it borrows from an aggregated pool. (😂 assumption made from not reading the code)

Actually, we are borrowing from the aggregated pool rather than a specific CQ. In this specific case of 2 CQs it is actually the same, so sometimes we shortcut saying 'borrowing from another CQ. More generically the aggregated pool description is better. 

More precisely tbis is an aggregated pool of lendable resources. If lendingLimit is used then it might be less than nominalQuota.

### Comment by [@amy](https://github.com/amy) — 2025-07-16T22:04:13Z

/assign
