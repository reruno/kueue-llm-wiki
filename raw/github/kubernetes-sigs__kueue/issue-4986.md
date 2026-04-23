# Issue #4986: Flaky Test: Scheduler when Using cohorts for sharing unused resources Should start workloads that are under min quota before borrowing

**Summary**: Flaky Test: Scheduler when Using cohorts for sharing unused resources Should start workloads that are under min quota before borrowing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4986

**Last updated**: 2025-04-16T16:06:51Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-04-15T14:36:17Z
- **Updated**: 2025-04-16T16:06:51Z
- **Closed**: 2025-04-16T16:06:49Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

Failed `Scheduler Suite: [It] Scheduler when Using cohorts for sharing unused resources Should start workloads that are under min quota before borrowing` on unrelated PR: https://github.com/kubernetes-sigs/kueue/pull/4985

```shell
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:333 with:
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:333 with:
Not enough workloads are pending
Expected
    <int>: 1
to equal
    <int>: 2
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/scheduler/scheduler_test.go:1256 @ 04/15/25 14:30:41.047
}
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4985/pull-kueue-test-integration-main/1912148687375568896

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-15T14:36:30Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T14:40:27Z

cc @mbobrovskyi @mszadkow ptal

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-16T11:58:23Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-04-16T16:06:45Z

/close 

Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/5005.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-16T16:06:50Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4986#issuecomment-2810053541):

>/close 
>
>Due to fixed by https://github.com/kubernetes-sigs/kueue/pull/5005.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
