# Issue #6238: MK Dispatcher: provide example implementation of a dispatcher under cmd/experimental

**Summary**: MK Dispatcher: provide example implementation of a dispatcher under cmd/experimental

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6238

**Last updated**: 2025-12-26T15:18:15Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-29T12:16:07Z
- **Updated**: 2025-12-26T15:18:15Z
- **Closed**: 2025-12-26T15:18:14Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 9

## Description

**What would you like to be added**:

Provide an example implementation of a MK dispatcher which could be easily copied and adapted by users. 

**Why is this needed**:

To demonstrate to users how to write such an external dispatcher. It should be accompanied by documentation describing how to write such a dispatcher.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T12:28:23Z

If we accommodate the dispatcher as a separate example, why do we not have a separate one for AdmissionCheck and JobFramework?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T12:40:46Z

I think the only reason is the work needed, I would love to have examples for JobFramework and AdmissionCheck. 

For JobFramework the role of the example played for a while AppWrapper, but not it is integrated in.

Also, I think MK dispatcher is signifficantly harder to write than a Job controller so this is additional argument to have an example.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T12:45:46Z

> I think the only reason is the work needed, I would love to have examples for JobFramework and AdmissionCheck.
> 
> For JobFramework the role of the example played for a while AppWrapper, but not it is integrated in.
> 
> Also, I think MK dispatcher is signifficantly harder to write than a Job controller so this is additional argument to have an example.

In that case, I would like to combine all examples into one manager, which means a single example manager has a custom JobFramework controller, AdmissionCheck controller, and Dispatcher. A single manager would be maintainable more.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T13:06:59Z

sgtm as a long term goal, but we could start gradually just with one, then extending the example.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-07-29T13:09:54Z

> sgtm as a long term goal, but we could start gradually just with one, then extending the example.

SGTM, we could focus on Dispathcer for this issue.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-27T13:59:34Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-11-26T14:59:21Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-26T15:18:10Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-26T15:18:15Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6238#issuecomment-3693003867):

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
