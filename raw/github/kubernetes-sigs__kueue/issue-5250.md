# Issue #5250: Default Kueue deployment should be HA

**Summary**: Default Kueue deployment should be HA

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5250

**Last updated**: 2025-09-28T17:58:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-05-14T17:35:57Z
- **Updated**: 2025-09-28T17:58:14Z
- **Closed**: 2025-09-28T17:58:13Z
- **Labels**: `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 8

## Description

ref: https://github.com/kubernetes-sigs/kueue/issues/5244#issuecomment-2880687077

It seems that the recommendation is to deploy Kueue in HA but our defaults do not do this.

Can we change the default for Kueue to be HA?

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-15T15:56:08Z

I would rather first try to increase user awareness by documentation. Maybe 2 replicas is good for prod usage, but if a user wants to just toy with Kueue then it might be easier to have one pod. 

EDIT: but I'm open to the possibility if there is enough of the interest. 

cc @mwielgus @mwysokin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-15T16:00:24Z

> I would rather first try to increase user awareness by documentation. Maybe 2 replicas is good for prod usage, but if a user wants to just toy with Kueue then it might be easier to have one pod.

I have the same opinion. Practically, productionization is an optional thing. However, I don't have a strong opinion.
Although, kueue-contrller-manager is a memory eater.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-05-15T16:11:17Z

I like elastic's approach where there's basically a log line printed during startup saying that development mode is on and ES runs with a single replica and the recommendation for the prod mode is to enable multiple replicas to reach HA. Maybe we could do something similar?

ES has an explicit Dev mode which needs to be disabled to enable some of the feature. We probably don't need to go as far but still maybe a log line and a doc entry should be enough?

### Comment by [@kannon92](https://github.com/kannon92) — 2025-05-15T16:38:49Z

> I would rather first try to increase user awareness by documentation. Maybe 2 replicas is good for prod usage, but if a user wants to just toy with Kueue then it might be easier to have one pod.

In my experience, people will deploy charts/installation from upstream and assume it is ready for prod usage unless otherwise told. 

In fact, GKE installs from the repo so I would think this is the recommended approach to deploy Kueue for prod.

https://cloud.google.com/kubernetes-engine/docs/tutorials/kueue-intro

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-13T17:24:49Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-12T17:25:36Z

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

### Comment by [@kannon92](https://github.com/kannon92) — 2025-09-28T17:58:08Z

/close

I don't think this is really necessary.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-28T17:58:14Z

@kannon92: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5250#issuecomment-3344008741):

>/close
>
>I don't think this is really necessary.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
