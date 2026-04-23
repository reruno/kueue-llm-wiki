# Issue #169: Knobs to configure which jobs kueue manages

**Summary**: Knobs to configure which jobs kueue manages

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/169

**Last updated**: 2022-05-04T02:47:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-03-31T18:01:49Z
- **Updated**: 2022-05-04T02:47:45Z
- **Closed**: 2022-05-04T02:47:44Z
- **Labels**: `kind/feature`, `priority/important-soon`, `kind/productionization`
- **Assignees**: [@ahg-g](https://github.com/ahg-g)
- **Comments**: 6

## Description

**What would you like to be added**:

Currently, kueue takes over and suspends any Job in the system that is not admitted in a ClusterQueue.

**Why is this needed**:

There might be users in a cluster that are using the Job API for supporting services (like backups), instead of batch workloads. They would likely run in dedicated nodes that should not be subject to quotas.

Also, a custom workload might use a Job underneath, perhaps more than one. Once this custom workload is accepted as a whole, we don't want the Job to be queued as well.

**Open questions**:

- Should we just do it per namespaces?
- Can we use the namespace selectors from the ClusterQueues to decide? If the controller is re-starting, we might miss some.
- Is an annotation in the job enough? This would cover both use cases, but it could be used by a malicious user to bypass Kueue.

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-01T13:56:46Z

I think we want a `ConfigMap` that includes a namespace selector to configure the job controller with which namespaces to work on. Should be none by default.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-01T13:57:39Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-04-13T02:05:29Z

https://github.com/kubernetes-sigs/kueue/pull/207 adds component config with a flag to control if kueue will manage jobs without queue name set; defaults to not managing them.

We should still add a namespace selector to component config to allow limiting kueue to managing jobs in a select subset of namespaces.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-01T01:52:00Z

I feel that we do not yet need a namespace selector in component config, basing it on whether the queue-name is set is sufficient for now.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-05-04T02:47:33Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-05-04T02:47:45Z

@ahg-g: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/169#issuecomment-1116878718):

>/close 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
