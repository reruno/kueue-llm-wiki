# Issue #642: [Question] why we only consider workload's request when judging whether Flavor.Min is satisfied

**Summary**: [Question] why we only consider workload's request when judging whether Flavor.Min is satisfied

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/642

**Last updated**: 2023-03-17T13:07:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@KunWuLuan](https://github.com/KunWuLuan)
- **Created**: 2023-03-17T02:57:31Z
- **Updated**: 2023-03-17T13:07:51Z
- **Closed**: 2023-03-17T13:07:50Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

we consider val instead of used+val when judging whether Flavor.Min is satisfied

https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L435
```
	if val <= flavor.Min {
		// The request can be satisfied by the min quota, assuming quota is
		// reclaimed from the cohort or assuming all active workloads in the
		// ClusterQueue are preempted.
		mode = Preempt
	}
```

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-17T13:07:46Z

This doesn't mean that the workload fits right away. It just means that it might fit if we preempt (remove) all the workloads that are currently running. That's why `used` doesn't matter.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-03-17T13:07:50Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/642#issuecomment-1473817349):

>This doesn't mean that the workload fits right away. It just means that it might fit if we preempt (remove) all the workloads that are currently running. That's why `used` doesn't matter.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
