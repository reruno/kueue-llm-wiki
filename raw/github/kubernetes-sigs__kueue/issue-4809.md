# Issue #4809: StrictFIFO prevents borrowing when CQ has pending workloads

**Summary**: StrictFIFO prevents borrowing when CQ has pending workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4809

**Last updated**: 2025-12-22T17:37:13Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@yuvalaz99](https://github.com/yuvalaz99)
- **Created**: 2025-03-27T15:14:46Z
- **Updated**: 2025-12-22T17:37:13Z
- **Closed**: 2025-12-22T17:37:12Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 9

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

We have a CQ configured with a StrictFIFO queueing strategy.
This queue has a nominal quota that should be borrowed by another CQ when needed.

However, we've recently discovered that StrictFIFO is also affecting whether quota can be borrowed from this queue when there are pending workloads in it.

**Setup:**

Cohort Structure
--- Cohort Root (NM: 0m)
-------- ClusterQueue Guaranteed (NM: 200m)
-------- ClusterQueue BestEffort (NM: 0m)

**Event sequence leading to the Issue:**

1. Guaranteed1 (100m) -> Admitted
2. Guaranteed2 (200m) -> SchedulingGated (100m quota left)
3. BestEffort1 (100m) -> SchedulingGated. Workload have the status:
_"Workload no longer fits after processing another workload"_

**What you expected to happen**:

According to the [docs](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#queueing-strategy)
> The queueing strategy determines how workloads are ordered in the ClusterQueue and how they are re-queued after an unsuccessful admission attempt.

We expected the queueing strategy to impact only the ordering of workloads within the queue.
We did not expect it to affect the ability of workloads from other CQs to borrow quota, which in our use case leads to major system underutilization.

This behavior is not documented anywhere. I'm wondering whether this is the expected behavior from your side?

**How to reproduce it (as minimally and precisely as possible)**:
( We are using in our setup pod integration )
1. Apply core configuration (cohorts, queues, and priority classes):
```
---
# Default Cohort
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Cohort
metadata:
  name: default
---
# Guaranteed ClusterQueue
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "guaranteed"
spec:
  namespaceSelector: {}
  queueingStrategy: StrictFIFO
  preemption:
    reclaimWithinCohort: LowerPriority
    withinClusterQueue: Never
  cohort: default
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "200m"
---
# Best-effort ClusterQueue
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "best-effort"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Never
    withinClusterQueue: Never
  cohort: default
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
---
# Resource Flavor
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
---
```
2. Create guaranteed workloads:
```
# Workloads - Guaranteed
---
apiVersion: apps/v1
kind: Deployment
metadata:
 name: guaranteed-1
 labels: {app: guaranteed-1, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed}
spec:
 replicas: 1
 selector:
   matchLabels: {app: guaranteed-1}
 template:
   metadata:
     labels: {app: guaranteed-1, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed}
   spec:
     terminationGracePeriodSeconds: 1
     containers:
     - name: main
       image: registry.k8s.io/pause:3.9
       resources:
         requests:
           cpu: "100m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
 name: guaranteed-2
 labels: {app: guaranteed-2, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed}
spec:
 replicas: 1
 selector:
   matchLabels: {app: guaranteed-2}
 template:
   metadata:
     labels: {app: guaranteed-2, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed}
   spec:
     terminationGracePeriodSeconds: 1
     containers:
     - name: main
       image: registry.k8s.io/pause:3.9
       resources:
         requests:
           cpu: "200m"
```
3. Create best-effort workload
```
# Workloads - Best Effort
apiVersion: apps/v1
kind: Deployment
metadata:
  name: best-effort-1
  labels: {app: best-effort, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort}
spec:
  replicas: 1
  selector:
    matchLabels: {app: best-effort}
  template:
    metadata:
      labels: {app: best-effort, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort}
    spec:
      terminationGracePeriodSeconds: 1
      containers:
      - name: main
        image: registry.k8s.io/pause:3.9
        resources:
          requests:
            cpu: "100m"
```
4. Expected pods status
```
NAME                                             READY   STATUS             RESTARTS          AGE
best-effort-1-789b74c4f5-2vppj                   0/1     SchedulingGated    0                 20s
guaranteed-1-7c77c5cffc-gcrp2                    1/1     Running            0                 28s
guaranteed-2-78fc659fd8-c6cpg                    0/1     SchedulingGated    0                 28s
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.30
- Kueue version (use `git describe --tags --dirty --always`): 0.10.2
- Cloud provider or hardware configuration: GCP
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-27T15:28:46Z

/assign @gabesaba 
who is already looking into it

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-25T16:18:49Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-07-25T16:28:51Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T16:31:17Z

/remove-lifecycle rotten

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-25T16:39:32Z

https://github.com/kubernetes-sigs/kueue/pull/4813 already addresses the issue when `preemption.reclaimWithinCohort: Any` is used, and it was cherrypicked to [0.11](https://github.com/kubernetes-sigs/kueue/pull/4822) and [0.10](https://github.com/kubernetes-sigs/kueue/pull/4823).

Solving the generic issue when `preemption.reclaimWithinCohort: LowerPriority`  is much trickier because when admitting best effort workloads we cannot be sure we will be able to reclaim back. 

@yuvalaz99 it will be helpful to know if the current status addresses your request, in which case we could close the issue, and defer fixing `preemption.reclaimWithinCohort: LowerPriority`  for later. wdyt?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-23T17:26:30Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-22T17:27:17Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-22T17:37:07Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-22T17:37:13Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4809#issuecomment-3683080831):

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
