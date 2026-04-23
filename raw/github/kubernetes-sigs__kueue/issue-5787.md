# Issue #5787: Update queueing strategy API comments for the 2-phase Admission

**Summary**: Update queueing strategy API comments for the 2-phase Admission

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5787

**Last updated**: 2026-03-06T08:29:47Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-06-27T14:30:28Z
- **Updated**: 2026-03-06T08:29:47Z
- **Closed**: 2026-03-06T08:29:46Z
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: [@tenzen-y](https://github.com/tenzen-y)
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
The SecondPass scheduling mechanism takes head workloads from ClusterQueue heads and the second pass queue in https://github.com/kubernetes-sigs/kueue/blob/5665ed27860264ee482c7270fa8627b8e2719a73/pkg/queue/manager.go#L650-L651.

For the BestEffort FIFIO strategy, this sounds reasonable since the strategy allows Kueue to admit following workloads when the head workload is inadmissible.

However, in the StrictFIFO strategy, if there are any workloads in the second pass queue, queueManager should not take the following workloads from the clusterQueue to guarantee the order strictly.

**What you expected to happen**:
In the strict FIFO strategy mode, Kueue must always admit the head workload first.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-27T14:44:28Z

I'm not understanding why this is a bug.

I think BestEffortFIFO and StrictFIFO are meant to control quota reservation. In case of the second pass of scheduling the workloads already have quota reserved. Note that, even before introduction of the second pass of scheduling the admission of workload was gated by the AdmissionChecks, and workload would be admitted independently of BestEffort / StrictFIFO as soon as all checks were green. I think this is similar case here.

For example, even without the second scheduling pass, you can have a Provisioning flavor in the StrictFIFO queue, and two workloads in the queue: wl1 (queued first), wl2 (queued second).

1. wl1 is queud, then wl2
2. wl1 has quota reserved and starts to wait for AC
3. wl2 has quota reserved and starts to wait for AC
4. wl2 is admitted before wl1 because the AC provisioned first, before AC for wl1 (this is likely to happen, for example it requested fewer nodes)
5. wl1 is admitted now once its AC provisioned

So, the order of getting quota was FIFO, but not admission.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-27T16:40:54Z

> So, the order of getting quota was FIFO, but not admission.

Yes, that's right for AC case.
Especially, in the step 5, wl1 will be admitted by workload-controller instead of scheduler since the quota reserved workload is not considered as an inadmissible workload.

I assumed that SecondPass scheduling admission (not quota reservation) still depends on FIFO. However, if we can define the queueing strategy is respected only for quota reservation, not admission, we should update the API comment and documentations: 

- https://github.com/kubernetes-sigs/kueue/blob/adee4646e2d3a4dc92597388cfa527b72e13647a/apis/kueue/v1beta1/clusterqueue_types.go#L81-L94
- https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#queueing-strategy

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-27T16:49:22Z

/remove-kind bug
/kind cleanup

/retitle Update queueing strategy API comments for the 2-phase Admission

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-30T15:26:18Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-28T15:37:57Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T08:16:28Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-05T08:23:11Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-04T08:26:39Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-06T08:29:40Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-06T08:29:47Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5787#issuecomment-4010314898):

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
