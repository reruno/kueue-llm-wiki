# Issue #7280: ElasticJobs & MultiKueue don't work for custom dispatchers

**Summary**: ElasticJobs & MultiKueue don't work for custom dispatchers

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7280

**Last updated**: 2025-12-01T15:20:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-15T16:10:48Z
- **Updated**: 2025-12-01T15:20:12Z
- **Closed**: 2025-12-01T15:20:11Z
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 10

## Description


**What happened**:

The ElasticJobs set the status.clusterName for the replacement slice directly.
This only works because of this hack we want to eliminate for the AllAtOnce dispatcher (default): https://github.com/kubernetes-sigs/kueue/blob/6b1f9388bcf00f44f1332b831224a66073d32fb6/pkg/webhooks/workload_webhook.go#L375-L385

However, it breaks the validation for any other MultiKueue dispachers.

**What you expected to happen**:

MultiKueue works for ElasticJobs for any dispatcher.

**How to reproduce it (as minimally and precisely as possible)**:

Follow the MultiKueue prototype PR which attempted to remove the "hack": https://github.com/kubernetes-sigs/kueue/pull/7278

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T16:11:02Z

cc @mszadkow @ichekrygin

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-10-16T08:13:32Z

/assign

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-16T14:52:53Z

A little confused about "repro", could you please provide more details?

> However, it breaks the validation for any other MultiKueue dispachers.

@mimowo it would be great to have more info on "how" or "when/where" it breaks other MultiKueue dispatchers.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T15:32:41Z

> @mimowo it would be great to have more info on "how" or "when/where" it breaks other MultiKueue dispatchers.

Please check the code under the issue, basically this code with `dispatcherName != configapi.MultiKueueDispatcherModeAllAtOnce` disables the validation for MultiKueueDispatcherModeAllAtOnce specifically.

Now, the validation would prevent scheduler to set status.clusterName for the replacement workload.

I think @mszadkow is also working on an integration test which could illustrate the problem.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-16T15:39:29Z

I see, and:

> Please check the code under the issue, basically this code with dispatcherName != configapi.MultiKueueDispatcherModeAllAtOnce disables the validation for MultiKueueDispatcherModeAllAtOnce specifically.

Is something we are adding now. I.E., not existing (or predating PR with Elastic Workloads + MultiKueue).
Is that correct?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T15:46:45Z

This code existed since 0.13, I think predating the MK+ElasticWorkloads: https://github.com/kubernetes-sigs/kueue/pull/5782

but because of the hack with didn't notice

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-16T15:49:29Z

> but because of the hack with didn't notice

and in addition, or that we didn't have test coverage for cases for `dispatcherName != configapi.MultiKueueDispatcherModeAllAtOnce`, correct?

I.E., trying to figure out how can we do better next time to avoid "misses" like this.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-16T16:04:41Z

`dispatcherName != configapi.MultiKueueDispatcherModeAllAtOnce` adding this was an omission on its own. We introduced that initially when working on "external disaptchers" (introducing NominatedClusterNames), because historically "AllAtOnce" would not set NominatedClusterNames. So, initially we planned to keep backwards compatible API and allows "AllAtOnce" not to use the NominatedClusterNames. However, it was later during review when I proposed to use "NominaedClusterNames" also for "AllAtOnce". However, I forgot to request reverting the hack...

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-01T15:20:06Z

/close
This is probably already addressed by this change: https://github.com/kubernetes-sigs/kueue/pull/7278/files#diff-78176f9cb5321e2dec9c0b0f7ba7bddf13cdcfd1f28011f338c86dc629b62adfL377

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-01T15:20:12Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7280#issuecomment-3597140909):

>/close
>This is probably already addressed by this change: https://github.com/kubernetes-sigs/kueue/pull/7278/files#diff-78176f9cb5321e2dec9c0b0f7ba7bddf13cdcfd1f28011f338c86dc629b62adfL377


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
