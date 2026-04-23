# Issue #62: Replace borrowing ceiling with weight

**Summary**: Replace borrowing ceiling with weight

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/62

**Last updated**: 2024-02-09T18:16:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-24T16:34:19Z
- **Updated**: 2024-02-09T18:16:40Z
- **Closed**: 2024-02-09T18:16:38Z
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/frozen`, `kind/grand-feature`
- **Assignees**: _none_
- **Comments**: 8

## Description

bit.ly/kueue-apis defined a weight to dynamically set a borrowing ceiling for each Capacity, based on the total resources in the Cohort and the capacities that have pending workloads.

We need to implement such behavior and remove the ceiling.
The weights and unused resources should lead to a dynamic ceiling that is calculated in every scheduling cycle. The exact semantics of this calculation are not fully understood.
In a given scheduling cycle, which capacities are considered for splitting the unused resources? Only the ones with pending jobs? What about the ones that are already borrowing but have no more pending jobs? What is considered unused resources once some resources have already being borrowed?

There are probably a few interpretations to these questions that lead to slightly different results. We need to explore them and pick one that sounds more reasonable or is based on existing systems.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T16:34:35Z

/kind feature
/size L
/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-14T14:46:53Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-14T16:07:08Z

/lifecycle frozen

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-06T20:09:33Z

Alternatively, the weights could be added to the namespace, so that fairness can be evaluated for the cluster by tenant, rather than per ClusterQueue.

This calls for a proper design doc.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-06T20:12:35Z

> Alternatively, the weights could be added to the namespace, so that fairness can be evaluated for the cluster by tenant, rather than per ClusterQueue.

Where would those weights be stored? I think setting a weight per namespace is probably going to be difficult to maintain, there will be way more namespaces than CQs

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-11-17T20:13:11Z

From @denkensk in https://github.com/kubernetes-sigs/kueue/pull/410/files#r998066062:

> I think we can probably add some algorithms in the future to ensure that there is fairness between the cluster queues？ Even we don't violate the min，but maybe can not preempt the workloads which are all coming from the same CQ？Maybe you know, we always do not want to hurt some single user too much, even though he borrowed someone else's resources.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-02-09T18:16:35Z

/close
in favor of #1714

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-09T18:16:39Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/62#issuecomment-1936396411):

>/close
>in favor of #1714


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
