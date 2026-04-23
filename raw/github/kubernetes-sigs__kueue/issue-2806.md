# Issue #2806: [kueuectl] Support filter by custom job type on the list pods command.

**Summary**: [kueuectl] Support filter by custom job type on the list pods command.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2806

**Last updated**: 2025-03-07T17:33:03Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2024-08-09T08:29:26Z
- **Updated**: 2025-03-07T17:33:03Z
- **Closed**: 2025-03-07T17:33:01Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@rainfd](https://github.com/rainfd)
- **Comments**: 13

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

**Why is this needed**:
We need to allow to support filtering pods by custom job type on the list pods command as discussed on https://github.com/kubernetes-sigs/kueue/pull/2280#discussion_r1654280733.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@rainfd](https://github.com/rainfd) — 2024-08-15T08:34:17Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-08-28T14:38:12Z

@rainfd Do you want to take it?

### Comment by [@rainfd](https://github.com/rainfd) — 2024-09-03T06:33:24Z

@mbobrovskyi The user case is that user have crd job type and use kueue to summit it, and you want to support to list their pod?
I'm a little confused. Because the code metioned in the discussed  https://github.com/kubernetes-sigs/kueue/pull/2280#discussion_r1654280733 don't block the case.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-09-03T13:27:43Z

There is already support for arbitrary label selectors, but you can do the same using `kubectl get`. So, we wouldn't be adding much value.

Maybe something we can do is to do a client-side filtering using the owner references? But not all custom jobs own the pods directly, so it's not generally useful.

Thoughts?

### Comment by [@rainfd](https://github.com/rainfd) — 2024-09-03T16:17:38Z

> There is already support for arbitrary label selectors, but you can do the same using `kubectl get`. So, we wouldn't be adding much value.
> 
> Maybe something we can do is to do a client-side filtering using the owner references? But not all custom jobs own the pods directly, so it's not generally useful.
> 
> Thoughts?

User's CRD -> Operator ->  Workload supported by kueue.

To support kueue, the custom operator should create a workload which is supported in kueue, like pod/job/jobset/...

If the workload is pod, we can filter using the owner references, but the user should provide the full crd name like `batch.kubernetes.io/job-name=xx` because we don't the relationship between `job/xx` and `batch.kubernetes.io/job-name=xx`. 

Another simpler way to find the pod is using the label selectors directly, because the pod must have a queue name in order to be managed by kueue.

If the workload is not a pod, we should look through all the workload supported by kueue to find the original reference workload , and then find the pods through that workload. But is there such a user case?

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-27T13:07:47Z

For built-in integration, users can build the `kueuectl` binary and use it. It should work if `JobWithPodLabelSelector` interface is implemented. However, for external integration, I’m honestly not sure.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-27T13:22:17Z

I can see only one way to add some flag like `--selector` and use it instead of `JobWithPodLabelSelector` interface.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-09-27T13:54:42Z

Looks like, we already have `--selector` flag for `kueuectl list pod` command.

https://github.com/kubernetes-sigs/kueue/blob/425ece197331d6b0c9b6d2bf4cc82326420c9f0a/cmd/kueuectl/app/list/list_pods.go#L72

Currently, the `--for` flag is required, and we can’t use the command without it. It might make sense to relax the validation and allow filtering Pods with the `--selector` flag, enabling users to filter custom jobs.

@alculquicondor WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-10-08T16:29:06Z

but then it's just the same as `kubectl get pods`. Not very useful IMO.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-06T16:35:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-02-05T17:07:03Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-07T17:32:57Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-07T17:33:02Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2806#issuecomment-2707023434):

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
