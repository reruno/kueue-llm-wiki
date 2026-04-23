# Issue #82: Add workload priority

**Summary**: Add workload priority

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/82

**Last updated**: 2022-03-28T00:59:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-01T19:36:57Z
- **Updated**: 2022-03-28T00:59:44Z
- **Closed**: 2022-03-28T00:59:43Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@denkensk](https://github.com/denkensk)
- **Comments**: 7

## Description

This is a placeholder to discuss priority semantics.

We can have it at the workload level or queue level.

## Discussion

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-02T16:54:17Z

Agree, queues should re-shuffle to reflect job priority 
maybe "weight" is a better descriptor, as done in HPC (Slurm, HTCondor) 
```
Weight:
from 1 to 100
1 being very important
100 being opportunistic compute run
```
(or we can do 100 important and 1 not, as we like)

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-04T20:43:47Z

Given that we converged on the concept of ClusterQueue being the practical place where queueing is actually happening, then I think it is safe to say that priority should be at the workload level (not a priority of the namedspaced queue for example as it was proposed in the initial proposal).

I think we could rely on k8s priority classes and semantics. If the user doesn't wish for priority to have an impact on kube-scheduler preemption, they can create the class with `preemptionPolicy: Never`.

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-09T01:24:27Z

/unassign
/help

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-09T02:47:21Z

I will take it because Priority is also related to the ClusterQueue QueueingStrategy.
/assign
/remove-help

### Comment by [@denkensk](https://github.com/denkensk) — 2022-03-09T02:47:43Z

/remove-help

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-28T00:59:33Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-28T00:59:44Z

@ahg-g: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/82#issuecomment-1080070426):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
