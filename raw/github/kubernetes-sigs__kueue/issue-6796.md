# Issue #6796: JobSet integration: Support DependsOn for PodsReady

**Summary**: JobSet integration: Support DependsOn for PodsReady

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6796

**Last updated**: 2026-04-20T05:47:54Z

---

## Metadata

- **State**: open (reopened)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-11T14:20:39Z
- **Updated**: 2026-04-20T05:47:54Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Correct support for PodsReady when JobSet dependsOn is used.

So, with dependsOn feature, a JobSet may say "start Job B after Job A completes". 

This means that we should not expect all pods to be ready, because the Pods of Job B will only start after Job A completes. 

So we should first wait for number of Pods in A, then number of Pods in A+B.

**Why is this needed**:

To properly support WaitForPodsReady for JobSets with dependsOn feature used.

## Discussion

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-09-18T15:03:18Z

@mimowo hello, I would like to try helping with this task. Would that be ok?
Let me know if anything else would be needed in order to start checking it out.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-18T15:04:29Z

Sure, you are welcome!

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-09-18T15:05:40Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T12:25:42Z

cc @MichalZylinski

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T05:51:57Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-17T05:52:02Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6796#issuecomment-3663770772):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T12:59:07Z

We have attempted to fix this, but the fix turned out to have some issues, I summarized them here: https://github.com/kubernetes-sigs/kueue/pull/7889#issuecomment-3663785196

We need some design and KEP update first to discuss how we are going to fix this. At this moment I'm not sure.

I **think** the way it should work is that whenever Job referenced by dependsOn=Ready gets Ready, or depends=Complete gets complete, then we start counting waitForPodsReady.timeout from that moment. 

However, we only set PodsReady=true at the end of the process, when **all** Pods are ready, to be consistent with the [definition](https://github.com/kubernetes-sigs/kueue/blob/9477dda80722d6694bdf83508e53bb82f9f4dde5/apis/kueue/v1beta1/workload_types.go#L640-L642).

And only then we start counting waitForPodsReady.recoveryTimeout.

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-12-17T22:23:13Z

@mimowo I'm trying understand the issue that we are trying to solve.
Are we trying to solve a possible premature eviction?
For example, WaitForPodsReady.Timeout=1 and  JobB dependsOn completion of JobA, jobA takes the hole 1 min to complete, then the workload is evicted and re-queued, given the Timeout was reached, but the jobB didn't even have a chance to start, so it shouldn't be re-queued because it wasn't failing or didn't have any problems, it was just waiting for it's dependency to be finished. Is that the considered issue?

Some additional questions:

- If we move the Timeout to only start counting when JobB starts, couldn't we be in a situation that if JobA takes the hole timeout, the workload wouldn't be evicted? or there is something else that controls eviction besides `WaitForPodsReady.Timeout`?
- For JobSet with DependsOn maybe we could consider start the Timeout when jobA starts, then re-start the Timeout when JobB starts? But then it would move away from the Timeout description given we only want to set PodsReady=true when all the Pods are ready.

```
	// Timeout defines the time for an admitted workload to reach the
	// PodsReady=true condition. When the timeout is exceeded, the workload
	// evicted and requeued in the same cluster queue.
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T08:39:32Z

> it was just waiting for it's dependency to be finished. Is that the considered issue?

Yes, the main motivation for the issue is that with the dependsOn feature the JobSet may take arbitrarily long to have all Pods running. It can even take hours. So, it requires the system administrators to increase the waitForPodsReady.timeout to very high numbers.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-18T08:43:17Z

> If we move the Timeout to only start counting when JobB starts, couldn't we be in a situation that if JobA takes the hole timeout, the workload wouldn't be evicted?

Exactly, this is the problem with the initial implementation.

> or there is something else that controls eviction besides WaitForPodsReady.Timeout?

We also have waitForPodsReady.recoveryTimeout which could mitigate the problem if we use it to wait for "Job2" and potentially evict "job2". However this timeout is only meant to be relevant for already fully running jobs, when a single pod requires fixing. So `waitForPodsReady.recoveryTimeout` is meant to be small like 3min or so.

> For JobSet with DependsOn maybe we could consider start the Timeout when jobA starts, then re-start the Timeout when JobB starts? But then it would move away from the Timeout description given we only want to set PodsReady=true when all the Pods are ready.

Yes, with this proposed approach (of updating PodsReady=False with new message and LastTransitionTime) we would need to adjust this code to count from Admitted=True, or PodsReady=False .LastTransitionTime. I think it will be virtually the same for all other Jobs than JobSet, so I think adjusting the definition is fine.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:59:44Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T10:46:22Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T11:15:54Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-04-20T05:47:52Z

/remove-lifecycle rotten
