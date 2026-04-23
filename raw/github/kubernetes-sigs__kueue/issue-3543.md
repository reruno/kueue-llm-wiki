# Issue #3543: Workload can get stuck indefinitely when using external AdmissionCheck

**Summary**: Workload can get stuck indefinitely when using external AdmissionCheck

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3543

**Last updated**: 2026-03-26T10:14:32Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-11-15T10:21:34Z
- **Updated**: 2026-03-26T10:14:32Z
- **Closed**: 2026-03-26T10:14:31Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 18

## Description

**What happened**:

A workload can get stuck forever with Evicted=True if the external controller sets state of the admission check to Retry while Evicted=True.

The scenario does not seem to happen consistently, but this is the root cause of the issue here: https://github.com/kubernetes-sigs/kueue/discussions/3365#discussioncomment-11259602. As a consequence the workload could not get re-admitted.

The issue has a workaround at the level of external admission check, to guard setting the Retry for the AC state whilst Evicted=True, as [here](https://github.com/kubernetes-sigs/kueue/blob/c6556458c39d103d260ca8c0bbeac15d9bea5352/pkg/controller/admissionchecks/provisioning/controller.go#L122-L124). 

Then Kueue flips the Retry to Pending, but it is stuck with Evicted=True forever. This is the final status:

```
Status:
  Admission Checks:
    Last Transition Time:  2024-11-14T18:09:17Z
    Message:               The workload is pending on Prefetch Admission Check
    Name:                  custom-ac
    State:                 Pending
  Conditions:
    Last Transition Time:  2024-11-14T18:08:57Z
    Message:               The workload has failed admission checks
    Observed Generation:   1
    Reason:                Pending
    Status:                False
    Type:                  QuotaReserved
    Last Transition Time:  2024-11-14T18:08:57Z
    Message:               At least one admission check is false
    Observed Generation:   1
    Reason:                AdmissionCheck
    Status:                True
    Type:                  Evicted
    Last Transition Time:  2024-11-14T18:08:57Z
    Message:               The workload backoff was finished
    Observed Generation:   1
    Reason:                BackoffFinished
    Status:                True
    Type:                  Requeued
Events:
  Type     Reason                      Age   From                       Message
  ----     ------                      ----  ----                       -------
  Normal   QuotaReserved               13m   kueue-admission            Quota reserved in ClusterQue
ue cluster-queue, wait time since queued was 0s
  Normal   EvictedDueToAdmissionCheck  13m   kueue-workload-controller  At least one admission check
 is false
  Warning  Pending                     13m   kueue-admission            The workload has failed admi
ssion checks
```

Some observations: the workload get re-admitted when we manually set `Evicted=False` - I expect Kueue should do it on its own.

**What you expected to happen**:

 I think Kueue should be able to recover from the situation on its own, and finalize eviction of the workload, allowing it to get re-admitted.

**How to reproduce it (as minimally and precisely as possible)**:

More details in the issue or @leipanhz can share, but basically the external AC was setting Retry while Kueue was evicting the workload. I think we should be able to reproduce this with integration tests.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-15T10:21:45Z

cc @mbobrovskyi @PBundyra

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-11-15T13:12:22Z

/assign

### Comment by [@leipanhz](https://github.com/leipanhz) — 2024-11-15T23:04:27Z

@mimowo Thanks for creating a ticket tracking this. 

I observed some unexcepted behaviors after applying for the workaround, commenting here:
In the custom controller, the requeue interval after setting to "Retry" is 5 seconds, however from the log, I see 28 times in 2 seconds the reconciler tries to set the AC status from Pending to Retry.  Seems like although Kueue evicts workload after AC is in retry status, it un-evicts it and reserves quota right away, so the status is back to Pending, Then Reconciler sets it back to Retry... It's like a race condition.

### Comment by [@hy00nc](https://github.com/hy00nc) — 2025-02-10T05:15:13Z

Hi @mszadkow @mimowo , is there update on this issue? I'm trying to deploy my own admission check controller but this is blocking it from functioning correctly. Just as @leipanhz pointed out, when the admission check state is `Retry`, Kueue releases reserved quota but as soon as it does, it changes admission check state back to `Pending` and quota is reserved almost right away (I'm using v0.8.4).

I was assuming there should be some gap in between the quota release and re-reservation, so that other workloads that are waiting in queue for quota can sneak in and get admitted when other workload releases quota by admission check. Please let me know if I'm missing something. Thanks!

edit: Probably this is related to this issue? https://github.com/kubernetes-sigs/kueue/issues/3258

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-10T10:52:36Z

@hy00nc please check this comment: https://github.com/kubernetes-sigs/kueue/discussions/3365#discussioncomment-11259602. Maybe the same "workaround" would work for you?

### Comment by [@hy00nc](https://github.com/hy00nc) — 2025-02-10T10:58:15Z

> [@hy00nc](https://github.com/hy00nc) please check this comment: [#3365 (comment)](https://github.com/kubernetes-sigs/kueue/discussions/3365#discussioncomment-11259602). Maybe the same "workaround" would work for you?

Thanks for the reply @mimowo , yes I tried this workaround and this workaround is what's causing this issue. Quota reservation is done by Kueue again as soon as it is released via `Retry`, making other workloads not able use the supposed-to-be-released quota. It looks like a race condition.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-10T11:12:08Z

I see, what may work in that case (but not sure this is available on 0.8) is to delay requeing as we do in the provisioning controller. PTAL: https://github.com/kubernetes-sigs/kueue/blob/3755065cfde22ef480b882e7558aa8cd1bee58de/pkg/controller/admissionchecks/provisioning/controller.go#L579

> edit: Probably this is related to this issue? https://github.com/kubernetes-sigs/kueue/issues/3258

I guess so, this would be a more generic solution which would support external admission checks OOTB.

cc @PBundyra

### Comment by [@hy00nc](https://github.com/hy00nc) — 2025-02-12T04:35:30Z

> I see, what may work in that case (but not sure this is available on 0.8) is to delay requeing as we do in the provisioning controller. PTAL:
> 
> [kueue/pkg/controller/admissionchecks/provisioning/controller.go](https://github.com/kubernetes-sigs/kueue/blob/3755065cfde22ef480b882e7558aa8cd1bee58de/pkg/controller/admissionchecks/provisioning/controller.go#L579)
> 
> Line 579 in [3755065](/kubernetes-sigs/kueue/commit/3755065cfde22ef480b882e7558aa8cd1bee58de)
> 
>  workload.UpdateRequeueState(wlPatch, backoffBaseSeconds, backoffMaxSeconds, c.clock) 
> > edit: Probably this is related to this issue? [#3258](https://github.com/kubernetes-sigs/kueue/issues/3258)
> 
> I guess so, this would be a more generic solution which would support external admission checks OOTB.
> 
> cc [@PBundyra](https://github.com/PBundyra)

Thanks @mimowo ! I think `UpdateRequeueState` can do the job temporarily until [#3258](https://github.com/kubernetes-sigs/kueue/issues/3258) is  addressed 👍

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-13T05:14:23Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-13T12:16:59Z

@PBundyra @mimowo Do you want to keep working on AdmissionCheck retry mechanism in this issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-13T12:28:58Z

/remove-lifecycle stale
It is not high priority, but I would welcome contributions to support it.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-11T13:03:47Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T13:08:34Z

/remove-lifecycle stale

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-27T09:02:46Z

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-25T09:28:39Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-24T09:38:17Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-26T10:14:24Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-26T10:14:32Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3543#issuecomment-4133334585):

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
