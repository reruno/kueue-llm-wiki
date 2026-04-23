# Issue #658: Restrict scaling out MPIJob

**Summary**: Restrict scaling out MPIJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/658

**Last updated**: 2024-05-01T11:31:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2023-03-22T16:15:59Z
- **Updated**: 2024-05-01T11:31:08Z
- **Closed**: 2024-05-01T11:31:06Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
I would like to restrict scaling out MPIJob in admission webhooks when clusterQueue lacks resources.

**Why is this needed**:
MPIJob supports scaling out workers by updating replicas.
Currently, if we scale out MPIJob that uses under-resourced clusterQueue, kueue sets suspend=true to MPIJob, and then the mpi-operator kills all MPIJob replicas.

However, I don't think that users want to kill all MPI replicas in that case.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-22T16:16:33Z

/cc @mimowo @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-22T17:23:49Z

We discussed this before in the context of Job #467

I think it makes sense to just restrict this via webhooks while we don't have the support.

@mwielgus do you think this is still not worth since we will eventually remove this piece of code?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-22T18:31:12Z

> We discussed this before in the context of Job #467
> 
> I think it makes sense to just restrict this via webhooks while we don't have the support.
> 
> @mwielgus do you think this is still not worth since we will eventually remove this piece of code?

It's reasonable. For the first step, we can introduce webhooks for both batch/job and mpijob.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-06-20T19:01:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-20T19:03:19Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-23T01:40:04Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-23T05:29:42Z

I think this still could be possible although we can close this once https://github.com/kubernetes-sigs/kueue/issues/77 is realized.


/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-22T06:22:56Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-01T11:31:02Z

This would be resolved by https://github.com/kubernetes-sigs/kueue/issues/77.
Considering the current effort for #77, we can close this issue for now.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-01T11:31:07Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/658#issuecomment-2088318657):

>This would be resolved by https://github.com/kubernetes-sigs/kueue/issues/77.
>Considering the current effort for #77, we can close this issue for now.
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
