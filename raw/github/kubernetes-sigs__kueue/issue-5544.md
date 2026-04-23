# Issue #5544: Configure ResourceTransformations via Singleton CRD

**Summary**: Configure ResourceTransformations via Singleton CRD

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5544

**Last updated**: 2025-09-08T16:38:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2025-06-06T15:49:55Z
- **Updated**: 2025-09-08T16:38:25Z
- **Closed**: 2025-09-08T16:38:24Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 7

## Description

We didn't think of the "singleton" CRD, when designing the ResourceTransformation API, but looking at this back, it would also be a good fit there, as we now require Kueue restart. cc @dgrove-oss

_Originally posted by @mimowo in https://github.com/kubernetes-sigs/kueue/pull/5149#discussion_r2132389836_

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-06T15:51:00Z

cc @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-06T19:52:11Z

I want to know the use cases and situations where we want to change the parameters dynamically.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-06T19:52:19Z

/kind feature

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-10T16:01:08Z

> I want to know the use cases and situations where we want to change the parameters dynamically.

For example you didn't have ResourceTransformations set, and you would like to set it. 

Currently we require restart of Kueue, which many admins don't like as it brings risk. If all goes smoothly, then it is just seconds, but an admin makes a mistake in the configuration, then the downtime can be longer during debugging.

I also got similar request regarding the WaitForPodsReady, where admins don't like to need to restart Kueue to configure it.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-08T16:30:52Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-08T16:38:18Z

/close
There is no point to refactor just for this feature I think. 

Let's track the discussion here about the possibility of refactoring: https://github.com/kubernetes-sigs/kueue/issues/5646

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-08T16:38:24Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5544#issuecomment-3267105674):

>/close
>There is no point to refactor just for this feature I think. 
>
>Let's track the discussion here about the possibility of refactoring: https://github.com/kubernetes-sigs/kueue/issues/5646


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
