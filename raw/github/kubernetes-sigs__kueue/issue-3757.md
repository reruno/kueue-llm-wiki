# Issue #3757: MultiKueue: Support sequential attempts to try worker clusters

**Summary**: MultiKueue: Support sequential attempts to try worker clusters

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3757

**Last updated**: 2025-07-28T11:35:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-06T15:28:34Z
- **Updated**: 2025-07-28T11:35:12Z
- **Closed**: 2025-07-28T11:35:10Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 6

## Description

**What would you like to be added**:

We would like to try sequentially the worker clusters, not all of them at the same time. The attempts could be time-based.

This will require at least API for controlling the time between the attempts. Also, the question -should the timeout be global, per manager, or per worker. Needs to be designed.

**Why is this needed**:

* To avoid the risk of admitting the same workload on two clusters at the same time, and thus possibly doing preemptions on both clusters
* To prioritize the use of some clusters over others. For example a user may have one cluster with reservations, and one auto-scaled. The user prefers to first try the reservation cluster, and only as a fallback try autoscaling. 
* To avoid autoscaling on multiple worker clusters at the same time.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-06T15:28:57Z

cc @mwielgus @mwysokin @tenzen-y

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-06T16:01:56Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-06T16:09:26Z

/remove-lifecycle stale

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-29T06:35:07Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-28T11:35:06Z

/close 
It is addressed by https://github.com/kubernetes-sigs/kueue/pull/5782

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-28T11:35:11Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3757#issuecomment-3126813193):

>/close 
>It is addressed by https://github.com/kubernetes-sigs/kueue/pull/5782


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
