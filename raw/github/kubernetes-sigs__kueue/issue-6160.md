# Issue #6160: Support specifying resource requests via annotation for non-schedulable resources

**Summary**: Support specifying resource requests via annotation for non-schedulable resources

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6160

**Last updated**: 2025-12-22T16:37:12Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@woehrl01](https://github.com/woehrl01)
- **Created**: 2025-07-24T08:36:16Z
- **Updated**: 2025-12-22T16:37:12Z
- **Closed**: 2025-12-22T16:37:11Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 6

## Description



**What would you like to be added**:

Support for specifying resource requests via pod annotations, so that Kueue can manage resources like licenses that are not tied to node-level capacity. For example:

```yaml
metadata:
  annotations:
    kueue.x-k8s.io/requested-resources: |
      licenses.mycompany.com/foo: "1"
```

**Why is this needed:**

Some resources, like commercial licenses, are globally limited and I want to manage by Kueue but not advertise by any node. Using `resources.requests` for such resources results in pods being unschedulable because the scheduler expects the resource to be present in node capacity. Allowing resource requests via annotations would let Kueue enforce global quotas without interfering with the scheduler.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-25T15:13:48Z

Thinking about this, maybe the resourceTransformations feature would be useful for you.

https://github.com/kubernetes-sigs/kueue/tree/main/keps/2937-resource-transformer#story-2

I don't think annotations would be right here as Kueue computes resources based on the requests. 

I do have some questions for you though:

Its also not clear to me if your licenses are at container level or pod level. If I have a pod with 5 containers that call your application, does that require 5 licenses?

Another possiblity could be to limit pods. You could maybe consider a combination of resource flavors with ClusterQueue on quota limiting pods.

### Comment by [@woehrl01](https://github.com/woehrl01) — 2025-07-25T15:28:07Z

@kannon92 thanks, I already stumbled over the transformer, but the docs aren't exactly clear where in the process it sits. Would I add the requests as "license" on the requests and remove it via the transformer?

If I look it from the kep you sent it seems that it's more the other way around, to merge requests, so that you don't have to overcomplicate the flavours.

To your questions, I now see the possible mismatch. But in our case it would map to the pod, not container level

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-23T16:26:29Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-22T16:27:18Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-22T16:37:07Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-22T16:37:12Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6160#issuecomment-3682851943):

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
