# Issue #7230: [flaky test] Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Summary**: [flaky test] Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7230

**Last updated**: 2025-10-22T06:25:15Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-13T08:11:20Z
- **Updated**: 2025-10-22T06:25:15Z
- **Closed**: 2025-10-22T06:25:14Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 5

## Description


**What happened**:

failure on periodic build https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1977627531985031168

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload deleted, next workload can admit expand_less	14s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:695 with:
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:695 with:
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:946 @ 10/13/25 07:07:18.088
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T07:25:15Z

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1978352315156926464

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-15T07:26:07Z

Seems like currently this is the most common flake

### Comment by [@pajakd](https://github.com/pajakd) — 2025-10-22T06:23:32Z

@mimowo this looks like a duplicate of #7250

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-22T06:25:08Z

/close
indeed

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-22T06:25:15Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7230#issuecomment-3430670987):

>/close
>indeed


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
