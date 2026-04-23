# Issue #5416: Flaky Integration Test: Topology Aware Scheduling when Single TAS Resource Flavor when Preemption is enabled within ClusterQueue should preempt the low and mid priority workloads to fit the high-priority workload

**Summary**: Flaky Integration Test: Topology Aware Scheduling when Single TAS Resource Flavor when Preemption is enabled within ClusterQueue should preempt the low and mid priority workloads to fit the high-priority workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5416

**Last updated**: 2025-05-30T06:01:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-05-30T05:59:57Z
- **Updated**: 2025-05-30T06:01:11Z
- **Closed**: 2025-05-30T06:01:10Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Periodic Integration Test failed on `TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Single TAS Resource Flavor when Preemption is enabled within ClusterQueue should preempt the low and mid priority workloads to fit the high-priority workload`

```shell
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:365 with:
Not enough workloads are admitted
Expected
    <int>: 1
to equal
    <int>: 2 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:365 with:
Not enough workloads are admitted
Expected
    <int>: 1
to equal
    <int>: 2
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/tas/tas_test.go:1374 @ 05/29/25 18:41:09.282
}
```

**What you expected to happen**:
No errors

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1928155106998489088

<img width="985" alt="Image" src="https://github.com/user-attachments/assets/6f7fe10e-5d96-4912-88bd-873c83e61546" />

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T06:00:06Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T06:01:05Z

Duplicated with https://github.com/kubernetes-sigs/kueue/issues/5395

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-30T06:01:11Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5416#issuecomment-2921317240):

>Duplicated with https://github.com/kubernetes-sigs/kueue/issues/5395
>
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
