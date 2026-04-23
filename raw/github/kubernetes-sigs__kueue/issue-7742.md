# Issue #7742: MultiKueue: cleanup code redundant "retry" inside multikueuecluster.go‎

**Summary**: MultiKueue: cleanup code redundant "retry" inside multikueuecluster.go‎

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7742

**Last updated**: 2025-12-16T11:58:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-18T20:00:02Z
- **Updated**: 2025-12-16T11:58:11Z
- **Closed**: 2025-12-16T11:58:11Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The helper functions return the redundant "retry" and "err" values.

See discussion in https://github.com/kubernetes-sigs/kueue/pull/7570#discussion_r2535514225

**Why is this needed**

To make the code easier to reason about.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T20:00:34Z

cc @olekzabl @mszadkow @hdp617

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-18T23:52:56Z

I'm not sure if this `retry` is redundant; see [this comment](https://github.com/kubernetes-sigs/kueue/pull/7570#discussion_r2539980847).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T13:50:18Z

I propose to move the discussion here. Yes in the current form it is not redundant due to non idiomatic handling of failure scenarios, which we could improve imo. For example error on reading a file really could be retried.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-11-21T09:33:43Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-24T12:44:53Z

/reopen 
to address the follow ups mentioned in https://github.com/kubernetes-sigs/kueue/pull/7810#discussion_r2556092255:
1. for secrets we can skip Reconcile, because we already have an event handler
2. for ClusterProfiles we could follow the same pattern and skip Reconcile on NotFound (requires adding event handler)

I think both are nice-to-haves, because the only consequence is that we would often schedule Reconciles rather than wait on user's action to add the resource. OTOH, this is miconfiguration, so it is not a big deal.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-24T12:44:59Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7742#issuecomment-3570619570):

>/reopen 
>to address the follow ups mentioned in https://github.com/kubernetes-sigs/kueue/pull/7810#discussion_r2556092255:
>1. for secrets we can skip Reconcile, because we already have an event handler
>2. for ClusterProfiles we could follow the same pattern and skip Reconcile on NotFound (requires adding event handler)
>
>I think both are nice-to-haves, because the only consequence is that we would often schedule Reconciles rather than wait on user's action to add the resource. OTOH, this is miconfiguration, so it is not a big deal.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
