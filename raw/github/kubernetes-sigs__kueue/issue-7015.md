# Issue #7015: Workloads unable to use cohort guarantees (hierarchical cohorts, fair sharing, multiple flavors.)

**Summary**: Workloads unable to use cohort guarantees (hierarchical cohorts, fair sharing, multiple flavors.)

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7015

**Last updated**: 2025-09-30T14:01:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@varunsyal](https://github.com/varunsyal)
- **Created**: 2025-09-25T17:57:57Z
- **Updated**: 2025-09-30T14:01:08Z
- **Closed**: 2025-09-30T14:01:08Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Kueue version = 0.13.4
Featuregate: FlavorFungibilityImplicitPreferenceDefault=True

When hierarchical cohorts are used with multiple flavors, a workload is unable to schedule in a flavor where its parent cohort has guarantees (i.e. another clusterqueue in the same subtree has unused nominal quota), when capacity in the flavor is fully occupied through borrowing by another cohort.


**What you expected to happen**:

If there are unused guarantees under the parent cohort, a workload should always be able to schedule, no matter what flavor it is.

**How to reproduce it (as minimally and precisely as possible)**:

Example:
Total Size of Cluster:
- Flavor-1 = 10
- Flavor-2 = 10

<img width="1493" height="1150" alt="Image" src="https://github.com/user-attachments/assets/c439d9be-9c76-4c7e-9091-85822b65ba68" />

If we submit 18 workloads (each using resources = 1) to clusterqueue "cq-p1", we observe that it schedules 10 workloads in Flavor-1 and 8 workloads in Flavor-2. (This result is not ideal too: https://github.com/kubernetes-sigs/kueue/issues/7016)
Next, if we submit 2 workloads (each using 1 resource) to clusterqueue ~~"cq-p4"~~ **"cq-p5"** which is part of cohort-B, it does not schedule at all. This is bad since, it is not able to borrow within the cohort, even when there is unused capacity on the cluster. This violates the guarantees at the parent cohort level.

All clusterqueues use the following:
```
Flavor Fungibility:
    When Can Borrow:   TryNextFlavor
    When Can Preempt:  TryNextFlavor
  Namespace Selector:
  Preemption:
    Borrow Within Cohort:
      Max Priority Threshold:  80000
      Policy:                  LowerPriority
    Reclaim Within Cohort:     Any
    Within Cluster Queue:      LowerPriority
  Queueing Strategy:           BestEffortFIFO
```

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): v1.32.7
- Kueue version (use `git describe --tags --dirty --always`): 0.13.4
- Feature Flag enabled: **FlavorFungibilityImplicitPreferenceDefault=True**

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-09-25T18:37:19Z

/cc

### Comment by [@varunsyal](https://github.com/varunsyal) — 2025-09-25T23:32:24Z

I encounter this issue when hierarchical cohorts are involved and fairsharing enabled. Also do note that I use the feature gate: `"FlavorFungibilityImplicitPreferenceDefault"`. I've not seen this in a flat cohort system.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-09-26T05:13:43Z

I think I understand what do you mean.

My understanding of the current behavior:

When we attempt to schedule a workload against a **CQ** and it doesn’t fit, `flavorFungibility` decides whether to borrow or to try the next flavor. However, once we enter the borrowing path for a given flavor, we keep borrowing from that same flavor until it’s exhausted across all CQs in the cohort, and then further up the hierarchy. I.E, something like:

<img width="1384" height="390" alt="Image" src="https://github.com/user-attachments/assets/ef2a0176-22bd-4717-8fa4-6dd30b97785c" />

---

It appears your expectation is that we should continue respecting the fungibility order even while borrowing , i.e., try the next flavor before escalating borrowing on the current one. I.E., something like:

<img width="1388" height="403" alt="Image" src="https://github.com/user-attachments/assets/60a2448d-0e28-4029-8f5d-1cbd9f1a5eef" />

If this is a correct understanding,, I don’t think this is strictly about hierarchical cohorts. You can observe it within a single cohort. For example, after running 12 workloads you might see:
```
  flavorsReservation:
    - name: f1
      resources:
        - borrowed: "600" <-- borrowed across all CQ's within immediate cohort for `f1`
          name: cpu
          total: "900"
    - name: f2
      resources:
        - borrowed: "0" <-- never borrowed
          name: cpu
          total: "300"
```
* `f1` consumed nominal (300)
* `f2` consumed nominal (300)
* `f1` borrows against all CQ'a within immediate cohort parent and doesn't touch `f2`

The same behavior carries over for hierarchy.

I think the current behavior is aligned with my understanding of how it should work, but I completely see your concern.

### Comment by [@varunsyal](https://github.com/varunsyal) — 2025-09-26T07:11:14Z

I'm not very sure if that is the solution (it could be). But this is more concerning if we look at the cohort. Since, with Fair Sharing, a cohort has guaranteed access to the sum of all the nominal quota in its subtree through reclamation preemption (introduced first in the [Fair Sharing KEP](https://github.com/kubernetes-sigs/kueue/tree/main/keps/1714-fair-sharing)), it is sub-optimal if the cohort starts borrowing from other cohorts before exhausting its own subtree's nominal quota, as that makes it prone to preemption. This however points to the other issue I have opened - https://github.com/kubernetes-sigs/kueue/issues/7016

In the example in description, the cohort-B is not even able to reclaim its subtree's nominal quota. This means that the cohort is not able to preempt to reclaim its own guarantee, which is a bigger concern.

A related PR is https://github.com/kubernetes-sigs/kueue/pull/6132 where the new feature flag was introduced. (However, I have not yet tested with the same example without the feature flag so not really sure if its related)
cc @pajakd @gabesaba who may have more context regarding this.

### Comment by [@pajakd](https://github.com/pajakd) — 2025-09-26T13:02:20Z

@varunsyal I cannot reproduce the issue based on the description. I'm seeing preemptions happen as expected and the workloads getting admitted to `cq-p4`. There has to be something different in my setup. Could you please share some logs of the `kueue-system` pods?

We have some idea how to fix #7016 but this one looks like something that should never happen.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-09-26T13:50:51Z

@varunsyal I wrote a base test scenario. Can you see if you can repro using this base, and share the (failing) test?
https://github.com/gabesaba/kueue/commit/bf69be3b7087576cc63c438f57312df6bfef527e

### Comment by [@varunsyal](https://github.com/varunsyal) — 2025-09-26T17:38:58Z

So sorry, I think I messed up the clusterqueue name in the issue description. The submission of 2 workloads need to be for "cq-p5" instead, which does not have any nominal quota for the clusterqueue itself, but should still get access to the nominal quota in parentCohort's subtree, over any other cohort's workloads. Updated the description now.
