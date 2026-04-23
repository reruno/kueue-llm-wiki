# Issue #6490: Emit metric for workloads stuck in termination

**Summary**: Emit metric for workloads stuck in termination

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6490

**Last updated**: 2025-08-07T21:45:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-08-06T21:07:02Z
- **Updated**: 2025-08-07T21:45:49Z
- **Closed**: 2025-08-07T21:45:48Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Related Issue: https://github.com/kubernetes-sigs/kueue/issues/6489
When workloads are stuck in termination, we'd like a metric that notifies us of the issue. Its because it could potentially hold up an entire Queue from admission if every reclamation involves a preemption. 

**Why is this needed**:
Hard to gain visibility into the problem.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-08-06T21:46:10Z

Potentially related to this: https://github.com/kubernetes-sigs/kueue/issues/6122

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-07T20:05:39Z

This is a pretty common problem but I'm not sure if Kueue is the right place for this.

Workloads aren't really "stuck" in termination. They are being terminated and they would obey termination grace periods set by the pods. This would be WAI so I'm not sure we would emit a metric.

It may be worth expanding on why workloads "are stuck" in termination. 

Its also a pretty common problem that once a workload is being deleted we should relinquish the resources but the resources are still being used. In some cases, the volumes are being removed from Kubelet or a device may still be held by Kubelet. So I'm not sure what to do here without more information.

I am reminded of https://github.com/kubernetes/kubernetes/issues/120756.

### Comment by [@amy](https://github.com/amy) — 2025-08-07T21:44:56Z

Yeah... overall agree from discussion on other threads. I think we can just use this: https://github.com/kubernetes-sigs/kueue/issues/6122 `Metric that measures time between eviction and actual preemption` and alert when it passes some time threshold. Working on a PR for this. 

I'll close this issue.

### Comment by [@amy](https://github.com/amy) — 2025-08-07T21:45:44Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-08-07T21:45:49Z

@amy: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6490#issuecomment-3165876535):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
