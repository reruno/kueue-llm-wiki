# Issue #1526: Limited scope user can have a way to get overview of quota

**Summary**: Limited scope user can have a way to get overview of quota

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1526

**Last updated**: 2024-06-08T02:45:38Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@panpan0000](https://github.com/panpan0000)
- **Created**: 2023-12-28T09:53:24Z
- **Updated**: 2024-06-08T02:45:38Z
- **Closed**: 2024-06-08T02:45:36Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

For people only having **namespaced** privilege, localqueue only shows the usage and reserved resources.
but people may want to know the total usable quota , so that to plan their usage.
but the total quota only exist  in ClusterQueue CR , but it's cluster-scoped CRD, privilege stop people to get the total values:
```
Error from server (Forbidden): clusterqueues.kueue.x-k8s.io is forbidden: User "xxx" cannot list resource "clusterqueues" in API group "kueue.x-k8s.io" at the cluster scope
```



**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-01-02T03:01:32Z

Since it's namespaced, doesn't this already as you expected, since clusterQueue is cluster-wide. Or a namespaced user will see all the clusterQueues out of his bounds.

### Comment by [@panpan0000](https://github.com/panpan0000) — 2024-01-10T01:04:05Z

thanks for reply, @kerthcet  . 
But please notice that in my scenario, as a limited user, I want to get the queue QUOTA, instead of the whole ClusterQueue CR.
I think it's very reasonable that for a namespaced limited user to understand how much quota still left that he/she can use.

my suggestion is to reflect the quota TOTAL in the LocalQueue CR. currently, only flavourUsage available in LocalQueue CR.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-09T02:06:02Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-09T02:06:29Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-08T02:45:33Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-08T02:45:36Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1526#issuecomment-2155774987):

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
