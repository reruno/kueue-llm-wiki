# Issue #7715: [flaky test] Interacting with scheduler when the cluster queue has admission check and workload priority class Should readmit preempted Job with priorityClass in alternative flavor with admission check

**Summary**: [flaky test] Interacting with scheduler when the cluster queue has admission check and workload priority class Should readmit preempted Job with priorityClass in alternative flavor with admission check

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7715

**Last updated**: 2025-11-17T16:52:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-17T16:51:44Z
- **Updated**: 2025-11-17T16:52:15Z
- **Closed**: 2025-11-17T16:52:14Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

**What happened**:

flake https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/7711/pull-kueue-test-integration-baseline-main/1990446599133728768

**What you expected to happen**:
no failure 
**How to reproduce it (as minimally and precisely as possible)**:
ci

```

Job Controller Suite: [It] Interacting with scheduler when the cluster queue has admission check and workload priority class Should readmit preempted Job with priorityClass in alternative flavor with admission check expand_less	15s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:615 with:
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:615 with:
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/controller/jobs/job/job_controller_test.go:2454 @ 11/17/25 15:58:38.058
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-17T16:52:09Z

/close 
duplicate of https://github.com/kubernetes-sigs/kueue/issues/7714

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-11-17T16:52:15Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7715#issuecomment-3542899540):

>/close 
>duplicate of https://github.com/kubernetes-sigs/kueue/issues/7714


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
