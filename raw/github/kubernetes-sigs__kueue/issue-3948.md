# Issue #3948: reclaimWithinCohort preemption does not work with hierarchical cohorts

**Summary**: reclaimWithinCohort preemption does not work with hierarchical cohorts

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3948

**Last updated**: 2025-05-16T16:48:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kaschnit](https://github.com/kaschnit)
- **Created**: 2025-01-09T00:33:26Z
- **Updated**: 2025-05-16T16:48:28Z
- **Closed**: 2025-05-16T16:48:20Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

I set up a simple 2-level hierarchical cohort using the Cohorts API. I was unable to get preemptions to happen via `reclaimWithinCohort` to work using the hierarchy.

The following Cohort and ClusterQueue setup:
```
- Cohort(name=root, nominalQuota=0m)
  - ClusterQueue(name=best-effort, nominalQuota=0m)
  - Cohort(name=guaranteed, nominalQuota=100m)
    - ClusterQueue(name=guaranteed, nominalQuota=0m)
```

Note that the "guaranteed" ClusterQueue should effectively have a nominal quota of 100m cpu since it belongs to the guaranteed cohort. Also note that the "guaranteed" ClusterQueue was configured with `spec.preemption.reclaimWithinCohort=Any`.

The following happened
1. Submitted Job(name=best-effort, cpu=100m) to a LocalQueue pointing at ClusterQueue "best-effort"
2. Waited for job "best-effort" to start running
3. Submitted Job(name=guaranteed, cpu=100m) to a LocalQueue pointing at ClusterQueue "guaranteed"
4. Job "guaranteed" is not scheduled until job "best-effort" completes and terminates itself (not terminated via preemption)

No preemption happens even though I think my configuration suggests that it should.

**What you expected to happen**:

The "best-effort" job is borrowing the entire quota from the "guaranteed" cohort, so the "guaranteed" job which belongs to the "guaranteed" cohort should be able to reclaim the quota via preemption.

I expect that the "guaranteed" job should preempt the "best-effort" job.

**How to reproduce it (as minimally and precisely as possible)**:

Kueue config:

```yaml
---
# Empty resource flavor
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
---
# Root Cohort
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Cohort
metadata:
  name: root
spec:
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "0m"
---
# Guaranteed Cohort
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Cohort
metadata:
  name: guaranteed
spec:
  parent: root
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "100m"
---
# Guaranteed ClusterQueue
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "guaranteed"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Any
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: Never
  cohort: guaranteed
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "0m"
---
# Best-effort ClusterQueues
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "best-effort"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Never
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: Never
  cohort: root
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "0m"
---
# LocalQueues
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: guaranteed
spec:
  clusterQueue: guaranteed
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: best-effort
spec:
  clusterQueue: best-effort
```

Best-effort job:

```yaml
---
apiVersion: batch/v1
kind: Job
metadata:
  generateName: best-effort-
  labels:
    kueue.x-k8s.io/queue-name: best-effort
spec:
  parallelism: 1
  completions: 1
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["180s"]
        resources:
          requests:
            cpu: "100m"
      restartPolicy: Never
```

Guaranteed job:

```yaml
---
apiVersion: batch/v1
kind: Job
metadata:
  generateName: guaranteed-
  labels:
    kueue.x-k8s.io/queue-name: guaranteed
spec:
  parallelism: 1
  completions: 1
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["30s"]
        resources:
          requests:
            cpu: "100m"
      restartPolicy: Never
```

To reproduce:
1. Apply the kueue config
2. Create the "best-effort" job
3. Wait for Kueue to admin the "best-effort" job and create its pod.
4. Submit the "guaranteed" job. You will see that no preemptions happen.

**Anything else we need to know?**:

It is worth noting that I saw the "guaranteed" job start to preempt the "best-effort" job when I made the following changes:

1.  Created two `WorkloadPriorityClass`es, low (value=50) and high(value=100)
2. Assigned these priority classes to the "best-effort" and "guaranteed" jobs respectively
3. Set `spec.preemption.borrowWithinCohort.policy=LowerPriority` on the "guaranteed" ClusterQueue

This also seems incorrect, because it would seem to mean that the "guaranteed" Cohort is borrowing quota from the "root" Cohort, which should not be possible because the "root" Cohort has 0 nominal quota. I'm happy to provide the exact configuration and repro steps if needed.

Please let me know if you need any more information from me. Thank you kindly.

**Environment**:
- Kubernetes version (use `kubectl version`): client v1.25.2, server v1.32.0
- Kueue version (use `git describe --tags --dirty --always`): v0.11.0-devel-40-gbf4657ad
- Cloud provider or hardware configuration: kind cluster on my laptop
- OS (e.g: `cat /etc/os-release`): MacOS Catalina
- Kernel (e.g. `uname -a`): Darwin Kernel Version 19.6.0
- Install tools:
- Others: installed kueue with helm on a kind cluster, nothing else installed on the cluster

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-09T10:44:19Z

/cc @gabesaba who works on HierarchicalCohorts and is looking into the similarly sounding issue: https://github.com/kubernetes-sigs/kueue/issues/3779

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-09T15:27:14Z

Thank you for the detailed issue, @kaschnit. I concur that this is a bug, and I agree with the desired behavior, that the guaranteed workload should preempt the best effort workload.

This is due to the way we're naively defining borrowing, which is not taking into account nominal capacity defined at the Cohorts. If a new workload is using more than the CQ's nominal quota, it is considered borrowing
https://github.com/kubernetes-sigs/kueue/blob/bf4657adc4e82b1458a8e0f78e0e21af15486d7b/pkg/scheduler/flavorassigner/flavorassigner.go#L606

Since this guaranteed CQ defines 0 quota, we are classifying the guaranteed job as borrowing, because its CQ does not provide any nominal capacity.

We could update the logic that decides if a workload is borrowing to also include parent Cohorts' nominal quotas (up until root), and to consider the CQ to be borrowing once this limit is exceeded. The question is whether we can keep borrowing as a binary signal, or whether we need a richer representation.

Let me think about this more. Any thoughts @tenzen-y, @mimowo?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-09T15:39:22Z

Updating the logic to include nominal quotas from parent cohorts sounds good to me, following the current approach. 

The approach may not be ideal, and I think even without hierarchical cohorts, there are cases where the classification is not accurate. To make it more accurate we could run oracle simulation, but I would refrain from it for now until really needed.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-10T13:55:56Z

This solution, including parent Cohorts' nominal quotas, wouldn't handle preemptions in the following case well (or any permutation, where capacity comes from another child node, CQ or Cohort, of the `guaranteed` Cohort):

- Cohort(name=root)
  - ClusterQueue(name=best-effort)
  - Cohort(name=guaranteed)
    - Cohort(name=guaranteed-cpu, nominalQuota=100m)
    - Cohort(name=guaranteed-gpu, nominalQuota=1)
    - ClusterQueue(name=guaranteed)

I would expect `guaranteed` ClusterQueue to have a better claim on `guaranteed` cohort's resources (including from child Cohorts) than `best-effort` ClusterQueue, and (I think) should be able to reclaim within Cohort.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-13T09:53:29Z

I see, good point. @gabesaba any ideas how to extend the proposal?

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-15T11:26:27Z

We traverse from the scheduling ClusterQueue towards the root of its Cohort Tree T. We find the first subtree sT (which may be the ClusterQueue itself) which fits our workload's usage + previous [SubtreeUsage](https://github.com/kubernetes-sigs/kueue/blob/d71331bac1c3ba6023f051f579adae1fa67c1962/pkg/cache/resource_node.go#L37-L41) within its [SubtreeQuota](https://github.com/kubernetes-sigs/kueue/blob/d71331bac1c3ba6023f051f579adae1fa67c1962/pkg/cache/resource_node.go#L33-L36). If the first subtree we find is T (the root), then reclaimWithinCohort is not possible. Otherwise, we look for reclaimWithinCohort candidates in the tree defined by removing the found subtree from the CohortTree (T - sT). 

When traversing this new tree starting at its root, we prune subtrees where SubtreeUsage <= SubtreeQuota. This allows a Cohort to be locally out of balance/borrowing from other nodes within its Cohort, without causing it to be preempted by a node outside of its Cohort. Non-pruned nodes are candidates. (note: this is starting to sound similar to [Fair Sharing](https://github.com/kubernetes-sigs/kueue/tree/d71331bac1c3ba6023f051f579adae1fa67c1962/keps/1714-fair-sharing), Scenario 1... maybe this issue is handled well by Fair Sharing, once it works with Hierarchical Cohorts)

I suppose that we would execute this logic during flavor assignment, inside of [IsReclaimPossible](https://github.com/kubernetes-sigs/kueue/blob/d71331bac1c3ba6023f051f579adae1fa67c1962/pkg/scheduler/flavorassigner/flavorassigner.go#L626-L628) - but is this too expensive?

**Next Step**
I'll determine whether this issue is solved by Hierarchical Cohorts + Fair Sharing, before we introduce another complicated algorithm.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-15T11:45:00Z

> I suppose that we would execute this logic during flavor assignment, inside of IsReclaimPossible - but is this too expensive?

What would be the algorithm computational complexity, `O(# of CQs in the cohort)`? If so, it doesn't sound scary as this is probably the same as during scheduling anyway.

> I'll determine whether this issue is solved by Hierarchical Cohorts + Fair Sharing, before we introduce another complicated algorithm.

Thanks! Just note that even if we establish that all use cases are addressed by HC+FS it would still remain a bug as the configuration is allowed. So, in that case we may need to deprecate the configuration and improve the docs to recommend not using it and migrate away.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-30T10:47:18Z

> What would be the algorithm computational complexity, O(# of CQs in the cohort)? If so, it doesn't sound scary as this is probably the same as during scheduling anyway.

Since we do this during flavor assignment, for each scheduling cycle it is something like`O(workload * resource * flavor * (Cohort + CQ + workload))`. The complexity is comparable to the current `IsReclaimPossible` - although I think the constants are more expensive.

> Thanks! Just note that even if we establish that all use cases are addressed by HC+FS it would still remain a bug as the configuration is allowed. So, in that case we may need to deprecate the configuration and improve the docs to recommend not using it and migrate away.

Ack. I think it makes sense to fix this scenario, as I don't think we plan to make Fair Sharing the only option. I'll make this fix while implementing Fair Sharing in Hierarchical Cohorts #3759, as the algorithms are quite similar.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-04T13:51:27Z

@kaschnit We are prioritizing the fix for this issue, and will keep this issue updated with its status.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-03-06T15:27:39Z

We are actively working on this. The fix is quite involved in terms of scheduling, preemption, and flavor assigning logic, as there were many assumptions of flat cohorts there. We completed a design, and are prototyping it now. 

Since there are other big scheduling features going into v0.11 (hierarchical fair sharing, TAS preemptions), We intend to release the fix in v0.12 to avoid major conflicts

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-16T16:45:14Z

Can we fix this already since https://github.com/kubernetes-sigs/kueue/pull/4806 is merged @gabesaba @pajakd ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-16T16:48:15Z

I will assume tentatively the issue is fixed, because the PR says "Fix classical preemption in the case of hierarchical cohorts.", and I remember reviewing that  `reclaimWithinCohort` was considered in the PR. 

Please feel free to re-open it if I missed something, or there are still some gaps.

cc  @kaschnit
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-16T16:48:21Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3948#issuecomment-2887226166):

>I will assume tentatively the issue is fixed, because the PR says "Fix classical preemption in the case of hierarchical cohorts.", and I remember reviewing that  `reclaimWithinCohort` was considered in the PR. 
>
>Please feel free to re-open it if I missed something.
>
>cc  @kaschnit
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
