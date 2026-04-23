# Issue #809: support match expressions in resource flavor

**Summary**: support match expressions in resource flavor

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/809

**Last updated**: 2024-03-21T07:11:33Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Created**: 2023-05-25T04:08:33Z
- **Updated**: 2024-03-21T07:11:33Z
- **Closed**: 2024-03-21T07:11:31Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Comments**: 12

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
support match expressions in resource flavor

**Why is this needed**:
maybe some high priority job don't want to run on spot nodes, now we have to add all 
nodes except for spot nodes to the one or multiple resource flavors, which is difficult 
if we have a large cluster

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-05-25T04:10:00Z

/assign 
This will involve API changes, scheduling logic changes, and test case changes. If necessary, I will submit a KEP for discussion.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-25T04:22:56Z

> support match expressions in resource flavor

Do you assume to add a new member to the following?

https://github.com/kubernetes-sigs/kueue/blob/64434d0ca4c9ecca24494e779d4dc63523ff1496/apis/kueue/v1beta1/resourceflavor_types.go#L36C40-L37

### Comment by [@KunWuLuan](https://github.com/KunWuLuan) — 2023-05-25T06:05:05Z

@tenzen-y yes, we can either add a property of v1.matchexpression type in ResourceFlavorSpec or change map[string]string to v1.labelSelector type

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-25T06:35:26Z

> change map[string]string to v1.labelSelector type

I think we can not add changes without backward compatibility to API since our API version is beta.

So, as you say, I think we can `add a property of v1.matchexpression type in ResourceFlavorSpec` .

However, I'm not sure the reason why we should support v1.matchExpressions in resourceFlavor since I think we should add Toleration to Node and create resourceFlavor with Taints in your case.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-25T06:40:45Z

Also, users can directly add nodeAffinity to batch/job and other integrated framework jobs. So the workload will be scheduled to Node matched both nodeSelector injected by kueue and nodeAffinity specified by users.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-05-25T06:42:29Z

cc: @kerthcet

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-05-25T11:28:01Z

I think `MatchExpressions` is more descriptive than `MatchLabels`, so it seems like an enhancement not a necessary one. Do we have so many resource flavors?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-25T15:05:56Z

Are `nodeTaints` in the ResourceFlavor not enough to express this semantics?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-21T06:22:00Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-02-20T06:22:15Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-21T07:11:27Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-03-21T07:11:32Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/809#issuecomment-2011353428):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
