# Issue #4135: Preemption during flavor assignment ambiguous

**Summary**: Preemption during flavor assignment ambiguous

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4135

**Last updated**: 2025-06-23T12:56:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gabesaba](https://github.com/gabesaba)
- **Created**: 2025-02-03T14:20:08Z
- **Updated**: 2025-06-23T12:56:40Z
- **Closed**: 2025-06-23T12:56:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@gabesaba](https://github.com/gabesaba)
- **Comments**: 7

## Description

**What would you like to be cleaned**:
It is possible that we assign mode `Preempt`, even when preemption is never possible. E.g. imagine the case that the CQ never allows preemption, and yet the workload's requests are below nominal quota.

https://github.com/kubernetes-sigs/kueue/blob/14e2ca76af24ac576bb21808dd2538971de6ced3/pkg/scheduler/flavorassigner/flavorassigner.go#L622-L631

However, the fact that we chose `Preempt` and not `NoFit` is later used to reserve resources that belong to the CQ - see https://github.com/kubernetes-sigs/kueue/issues/4105.

Nevertheless, this is confusing. Something _like_ the following categories may make more sense:

```
NeverFit - current NoFit, where workload is too big even if cluster is empty
NoFit - workload can fit if no workloads are running, but it has to wait, as preemption is not an option
Preemption
Fit
```

/cc @mimowo

## Discussion

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-03T14:21:05Z

/assign @gabesaba

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-03T14:26:14Z

The fact that NeverFit workloads are handled as NoFit might be even considered a bug currently, because such a workload blocks indefinitely other "valid" workloads without a clear response saying "why".

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-04T15:06:51Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-07T22:09:19Z

/remove-lifecycle stale

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-06-11T12:06:30Z

Will be solved by #5428

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-23T12:56:34Z

> Will be solved by https://github.com/kubernetes-sigs/kueue/issues/5428

Closing as the issue is closed. Also, the 4-level result discussed in the issue is already introduced in https://github.com/kubernetes-sigs/kueue/pull/5698.


/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-23T12:56:40Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4135#issuecomment-2996394367):

>> Will be solved by https://github.com/kubernetes-sigs/kueue/issues/5428
>
>Closing as the issue is closed. Also, the 4-level result discussed in the issue is already introduced in https://github.com/kubernetes-sigs/kueue/pull/5698.
>
>
>/close
>
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
