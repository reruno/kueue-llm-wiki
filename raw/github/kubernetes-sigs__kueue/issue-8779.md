# Issue #8779: [flaky test] Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload becomes inadmissible. next workload admits

**Summary**: [flaky test] Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload becomes inadmissible. next workload admits

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8779

**Last updated**: 2026-01-26T19:22:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-01-26T09:24:36Z
- **Updated**: 2026-01-26T19:22:30Z
- **Closed**: 2026-01-26T19:22:29Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

**Which test is flaking?**:

Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload becomes inadmissible. next workload admits 

**First observed in** (PR or commit, if known):

don't know

**Link to failed CI job or steps to reproduce locally**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-release-0-14/2015458030983843840
**Failure message or logs**:
```
Scheduler Fair Sharing Suite: [It] Scheduler when ClusterQueue head has inadmissible workload sticky workload becomes inadmissible. next workload admits expand_less	16s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:749 with:
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:749 with:
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:927 @ 01/25/26 16:34:08.299
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-26T19:22:24Z

/close
based on https://github.com/kubernetes-sigs/kueue/pull/8776#issuecomment-3798609398

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-26T19:22:29Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8779#issuecomment-3801320308):

>/close
>based on https://github.com/kubernetes-sigs/kueue/pull/8776#issuecomment-3798609398


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
