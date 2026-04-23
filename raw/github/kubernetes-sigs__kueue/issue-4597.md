# Issue #4597: High-Priority Workload Fails to Preempt Lower-Priority Workload Using Borrowed Resources

**Summary**: High-Priority Workload Fails to Preempt Lower-Priority Workload Using Borrowed Resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4597

**Last updated**: 2025-11-16T02:08:17Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@dora-zhang](https://github.com/dora-zhang)
- **Created**: 2025-03-13T19:59:57Z
- **Updated**: 2025-11-16T02:08:17Z
- **Closed**: 2025-11-16T02:08:16Z
- **Labels**: `kind/support`, `lifecycle/rotten`
- **Assignees**: [@xiongzubiao](https://github.com/xiongzubiao)
- **Comments**: 16

## Description

**Problem Description**
I found a high-priority workload (`h1`) in ClusterQueue `cq-hi` cannot preempt a lower-priority workload (`m2`) in ClusterQueue `cq-med`, despite both being in the same cohort. The situation is as follows:
ClusterQueue `cq-med`:
   - Has reserved resources from ResourceFlavor `rf1`
   - Can borrow resources from ResourceFlavor `rf2`

ClusterQueue `cq-hi`:
  - Enabled to borrow from both `rf1` and `rf2`

**Steps to Reproduce**
1. Cluster Setup:

a. ResourceFlavors:
- rf1 (1 GPU)
- rf2 (1 GPU)

b. Create two ClusterQueues:
- cq-med
```
spec:
  cohort: common
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  preemption:
    borrowWithinCohort:
      policy: LowerPriority
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
  stopPolicy: None
  resourceGroups:
    - flavors:
        - name: rf1
          resources:
            - name: nvidia.com/gpu
              nominalQuota: 1  # Reserved 1 GPU
        - name: rf2
          resources:
            - name: nvidia.com/gpu
              nominalQuota: 0  # Enable borrow
```
- cq-high
```
spec:
  [omit same setting as cq-med]
  resourceGroups:
    - flavors:
        - name: rf1
          resources:
            - name: nvidia.com/gpu
              nominalQuota: 0  # Enable borrow
        - name: rf2
          resources:
            - name: nvidia.com/gpu
              nominalQuota: 0  # Enable borrow
```
2. Workload Setup:
- `m1`, `m2`: Each requests 1 GPU, medium priority
- `h1`: Requests 1 GPU, high priority

3. Execution Steps:
a. Submit workloads `m1` and `m2` to `cq-med`:
Result: Successfully scheduled
- `m1` occupies the reserved GPU from `rf1`
- `m2` occupies the borrowed GPU from `rf2`

b. Submit workload `h1` to `cq-high`:
Result: `h1` remains pending, unable to preempt lower-priority workloads
Error message:
`Warning  Pending  16m (x7 over 36m)  kueue-admission  couldn't assign flavors to pod set main: insufficient unused quota for nvidia.com/gpu in flavor rf1, 1 more needed, insufficient unused quota for nvidia.com/gpu in flavor rf2, 1 more needed`

**Expected vs Actual Results** 
•	I was expected: High-priority workload h1 should preempt lower-priority workloads `m2` to claim the GPU.
•	Actual: High-priority workload is stuck in Pending state.

**Questions** 
1.	Observation: When assigning a Flavor to workload `h1`, the code selects `rf1` as a candidate but not `rf2`.
a. Why is `rf1` preferred over `rf2` in this scenario?
b. Should the assignment logic prioritize borrowed resources (rf2) over reserved resources (rf1) when looking for preemption candidates?

2. I'm further looking into this function `PotentialAvailable`, I'm not quite clear how the potential available is calculated. How does Kueue handle resource visibility across `ClusterQueues` with shared `ResourceFlavors`?

Additional information for crd configuration
resourceFlavor
```
#  kubectl get rf -o yaml
apiVersion: v1
items:
- apiVersion: kueue.x-k8s.io/v1beta1
  kind: ResourceFlavor
  metadata:
…
    name: ng1
    …
  spec:
    nodeLabels:
…
    tolerations:
    - effect: NoSchedule
      key: node.kubernetes.io/unschedulable
      operator: Exists
- apiVersion: kueue.x-k8s.io/v1beta1
  kind: ResourceFlavor
  metadata:
…
    name: ng2
…
  spec:
    nodeLabels:
      …
    tolerations:
    - effect: NoSchedule
      key: node.kubernetes.io/unschedulable
      operator: Exists
kind: List
metadata:
  resourceVersion: ""
```

ClusterQueue Configuration:
```
# kubectl get cq cq-med -o yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
….
  name: cq-med
  …
spec:
  cohort: memverge.ai
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  namespaceSelector:
    matchLabels:
      project: cq-med
  preemption:
    borrowWithinCohort:
      policy: LowerPriority
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - nvidia.com/gpu
    flavors:
    - name: ng1
      resources:
      - name: cpu
        nominalQuota: "0"
      - name: memory
        nominalQuota: "0"
      - name: nvidia.com/gpu
        nominalQuota: "1"
    - name: ng2
      resources:
      - name: cpu
        nominalQuota: "0"
      - name: memory
        nominalQuota: "0"
      - name: nvidia.com/gpu
        nominalQuota: "0"
  stopPolicy: None
Status:
…
```

```
# kubectl get cq cq-hi -o yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  ..
  name: cq-hi
  ..
spec:
  cohort: memverge.ai
  flavorFungibility:
    whenCanBorrow: Borrow
    whenCanPreempt: TryNextFlavor
  namespaceSelector:
    matchLabels:
      project: cq-hi
  preemption:
    borrowWithinCohort:
      policy: LowerPriority
    reclaimWithinCohort: Any
    withinClusterQueue: LowerPriority
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources:
    - cpu
    - memory
    - nvidia.com/gpu
    flavors:
    - name: ng1
      resources:
      - name: cpu
        nominalQuota: "0"
      - name: memory
        nominalQuota: "0"
      - name: nvidia.com/gpu
        nominalQuota: "0"
    - name: ng2
      resources:
      - name: cpu
        nominalQuota: "0"
      - name: memory
        nominalQuota: "0"
      - name: nvidia.com/gpu
        nominalQuota: "0"
  stopPolicy: None
```

## Discussion

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-03-17T22:20:11Z

This seems a bug that can happen whenever 2+ resourceflavors are used, even there is only 1 queue (no borrowing). 

Considering the following simple ClusterQueue:
```
spec:
  preemption:
    withinClusterQueue: LowerPriority  # <== enable priority-based preemption
  namespaceSelector: {}
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: rf1
      resources:
      - name: cpu
        nominalQuota: 1
    - name: rf2
      resources:
      - name: cpu
        nominalQuota: 1
```

Firstly let's submit two workloads (each requesting 1 cpu) one by one to this queue: 1) `wl-high` with high priority first. It will be assigned to `rf1`. 2) then `wl-low` with low priority will be assigned to `rf2`.

Now let's submit the third workload `wl-medium` with medium priority. It is expected that it can preempt `wl-low` and be assigned to `rf2`. But it doesn't happen, even in version v0.11.0-rc.0.

cc @gabesaba @mimowo

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-03-17T23:01:59Z

I think this is because the tried flavor index is not properly tracked. 

During the first scheduling iteration, although both resourceflavors are evaluated, the first flavor is selected: `"Flavors":{"cpu":{"Name":"rf1","Mode":1,"TriedFlavorIdx":-1}}`. Later when searching the preemption targets, the potential target `wl-low` can't be selected because it is running on the second flavor `rf2`. And because `TriedFlavorIdx` is `-1`, the future scheduling iterations will start searching from flavor `rf1` again, and end up selecting `rf1` again...

I think the `TriedFlavorIdx` should be 0 after the 1st iteration because it was the first flavor that was selected. In this way, the 2nd iteration will skip flavor `rf1` and start from `rf2`. An assignment of `rf2` will be returned, and the preemption candidate `ws-low` will be properly preempted.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-03-17T23:27:18Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T07:44:06Z

@xiongzubiao Thank you for the investigation and the PR. I will check it. In the meanwhile can you also check you face the problem when using `flavorFungibility.whenCanPreempt: Preempt`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T07:57:31Z

> [@xiongzubiao](https://github.com/xiongzubiao) Thank you for the investigation and the PR. I will check it. In the meanwhile can you also check you face the problem when using `flavorFungibility.whenCanPreempt: Preempt`.

If `{"flavorFungibility": {"whenCanPreempt": "Preempt"}}` resolves this situation, this is expected behavior, I guess.
As we can see https://github.com/kubernetes-sigs/kueue/tree/main/keps/582-preempt-based-on-flavor-order,  flavorFungibility aims to resolve such requirements.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-03-18T20:12:22Z

The problem is gone if using `flavorFungibility.whenCanPreempt: Preempt`. But we prefer using `flavorFungibility.whenCanPreempt: TryNextFlavor` to avoid unnecessary preemption in the first flavor when the next flavor has enough resources.

I think this is a valid use case that, when none of the flavors can fit the workload, `flavorFungibility.whenCanPreempt: TryNextFlavor` should allow to preempt the candidates not just in the first flavor.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T09:20:22Z

I see, this makes sense. 

My suggestion was mostly in case you are looking for a workaround.

However I agree I've if TryNextFlavor is used and we exhaust options then we Preempt.

Still I think we should start with extending the test coverage at the scheduler_test level, so that we don't break the other scenario by the refactoring.

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-03-19T16:57:18Z

> Still I think we should start with extending the test coverage at the scheduler_test level, so that we don't break the other scenario by the refactoring.

Agreed! Is there anyone working #4663 ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-19T17:04:07Z

I think no, noone is assigned

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-20T06:26:23Z

> The problem is gone if using `flavorFungibility.whenCanPreempt: Preempt`. But we prefer using `flavorFungibility.whenCanPreempt: TryNextFlavor` to avoid unnecessary preemption in the first flavor when the next flavor has enough resources.
> 
> I think this is a valid use case that, when none of the flavors can fit the workload, `flavorFungibility.whenCanPreempt: TryNextFlavor` should allow to preempt the candidates not just in the first flavor.

I think this is a useful feature, actually that can improve cluster resource usage. However, I would like to take it as a new feature so that we can avoid breaking in the existing environment since there is `TryNextFlavor` since first Preemption support.

We might want to add new fungibility, `PreemptAfterTryNextFlavor` or something. In any case, let's add functional test cases, first.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-18T08:08:23Z

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

### Comment by [@xiongzubiao](https://github.com/xiongzubiao) — 2025-06-18T23:53:09Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-17T00:48:39Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-17T01:35:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-16T02:08:11Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-16T02:08:17Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4597#issuecomment-3537380565):

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
