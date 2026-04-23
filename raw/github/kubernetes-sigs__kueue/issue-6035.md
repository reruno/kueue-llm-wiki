# Issue #6035: QuotaReservation does not get released when AdmissionCheck state is Rejected or Retry

**Summary**: QuotaReservation does not get released when AdmissionCheck state is Rejected or Retry

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6035

**Last updated**: 2026-02-10T08:26:08Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@jenny-yang-ai](https://github.com/jenny-yang-ai)
- **Created**: 2025-07-18T22:56:47Z
- **Updated**: 2026-02-10T08:26:08Z
- **Closed**: 2026-02-10T08:26:07Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
After an AdmissionCheck rejects or retries a workload, the workload still holds onto its quota reservation. I see this when describing a workload after the AdmissionCheck sets state Rejected:
```
  status:
    admission:
      clusterQueue: ml-infra
      podSetAssignments:
      - count: 1
        flavors:
          cpu: head
          memory: head
        name: head
        resourceUsage:
          cpu: 400m
          memory: 9262144k
      - count: 900
        flavors:
          cpu: vm-gpu-a10-2
          memory: vm-gpu-a10-2
          nvidia.com/gpu: vm-gpu-a10-2
        name: ray-worker-a10-2
        resourceUsage:
          cpu: "26190"
          memory: 197984306250Ki
          nvidia.com/gpu: "900"
      - count: 1
        name: submitter
    admissionChecks:
    - lastTransitionTime: "2025-07-16T18:41:13Z"
      message: 'Reset to Pending after eviction. Previously: Rejected'
      name: lilypad-gpu-capacity-check
      state: Pending
    conditions:
    - lastTransitionTime: "2025-07-16T18:39:58Z"
      message: Quota reserved in ClusterQueue ml-infra
      observedGeneration: 1
      reason: QuotaReserved
      status: "True"
      type: QuotaReserved
    - lastTransitionTime: "2025-07-16T18:39:58Z"
      message: Not all pods are ready or succeeded
      observedGeneration: 1
      reason: PodsReady
      status: "False"
      type: PodsReady
    - lastTransitionTime: "2025-07-16T18:41:13Z"
      message: 'The workload is deactivated due to Admission check(s): [lilypad-gpu-capacity-check],
        were rejected'
      observedGeneration: 2
      reason: DeactivatedDueToAdmissionCheck
      status: "True"
      type: Evicted
```
When describing the ClusterQueue, it counts this workload in the `reservingWorkloads` field.

**What you expected to happen**:
According to the [docs](https://github.com/kubernetes-sigs/kueue/issues), if the workload's AdmissionCheck is in Rejected or Retry state, the workload's quota reservation will be released. I would expect that describing the workload shows that the QuotaReserved is False (or the condition doesn't exist) and the ClusterQueue isn't tracking it as a reservingWorkload.

**How to reproduce it (as minimally and precisely as possible)**:
1. Create a ClusterQueue with quota of 1 resource with an AdmissionCheck
2. Create a workload requesting 1 resource and submit it to the ClusterQueue
3. Have the AdmissionCheck reject it (state = rejected)
4. The workload still has condition QuotaReserved = True and status.Admission not nil
5. If we create another workload requesting 1 resource, it doesn't get the quota reservation.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-07-19T01:17:13Z

cc/ @mimowo @gabesaba 

Can you check if this reproduction in integration testing is correct in my PR here: https://github.com/kubernetes-sigs/kueue/pull/6037

One aspect I'd like you to confirm is this (see comments in code blocks):
```
ginkgo.By("simulating workload admission for quota reservation only", func() {
			admission := testing.MakeAdmission("cq").Obj()
			gomega.Expect(k8sClient.Get(ctx, wlKey, &createdWl)).To(gomega.Succeed())
			gomega.Expect(util.SetQuotaReservation(ctx, k8sClient, &createdWl, admission)).Should(gomega.Succeed())
			util.SyncAdmittedConditionForWorkloads(ctx, k8sClient, &createdWl)
		})
// Please confirm that testing.MakeAdmission specifically means only admission from a quota reservation perspective
```
```
g.Expect(workload.IsAdmitted(&createdWl)).To(gomega.BeTrue())
// Please confirm workload.IsAdmitted means admission for both quota reservation and admissionChecks
```

### Comment by [@amy](https://github.com/amy) — 2025-07-19T01:19:16Z

/assign

(tentatively, if my reproduction is actually real. Also if the bug is indeed not expected behavior)

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-21T06:51:17Z

@amy thank you for the issue. 

The process of Eviction is 2-phase. In the first phase add the Evicted condition, and only in the follow up request (second phase) we set `QuotaReservation=False`. We do this so that we can release quota only once all Pods are stopped.  However, in the case of Deactivated workloads I think `QuotaReservation` may indeed never be cleaned. 

So, the fact that the quota reservation is not cleaned immediately is ok, but it should be cleaned once all Pods are stopped. The workload condition not cleaned is misleading, but probably not that much of a deal if the quota is freed at the CQ level, and the  `reservingWorkloads` is reduced.

Since the steps depend on termination of Pods you may also want to check the behavior beyond integration tests - on a running cluster. There very likely might be lurking a bug, but hard to say based on the integration test only.

### Comment by [@amy](https://github.com/amy) — 2025-07-21T13:42:17Z

@mimowo Ah I see. Thanks for the explanation! Specifically about how 2 phase eviction works. 

 Will see if I can find anything from e2e testing.

### Comment by [@amy](https://github.com/amy) — 2025-09-12T17:39:56Z

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-11T18:35:34Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-12T06:47:17Z

Jennty, do you still observe the issue? The has been recently a number of bugfixes to Admission checks lifecycle so I would suppose this is already fixed.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-11T07:36:20Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-10T08:26:02Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-10T08:26:08Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6035#issuecomment-3876101297):

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
