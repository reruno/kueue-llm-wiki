# Issue #8523: [Release-0.14 Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created with WorkloadPriorityClass should allow to update the workload priority in LeaderWorkerSet

**Summary**: [Release-0.14 Flaky E2E] LeaderWorkerSet integration when LeaderWorkerSet created with WorkloadPriorityClass should allow to update the workload priority in LeaderWorkerSet

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8523

**Last updated**: 2026-01-12T19:35:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2026-01-10T15:41:06Z
- **Updated**: 2026-01-12T19:35:44Z
- **Closed**: 2026-01-12T19:35:43Z
- **Labels**: `kind/bug`, `kind/failing-test`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 5

## Description

/kind flake

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

End To End Suite: kindest/node:v1.35.0: [It] LeaderWorkerSet integration when LeaderWorkerSet created with WorkloadPriorityClass should allow to update the workload priority in LeaderWorkerSet

```
{Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:885 with:
Expected
    <string>: low-priority
to equal
    <string>: high-priority failed [FAILED] Timed out after 45.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:885 with:
Expected
    <string>: low-priority
to equal
    <string>: high-priority
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/leaderworkerset_test.go:886 @ 01/10/26 07:13:02.779
}
```

**What you expected to happen**:
No issue.

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/8520/pull-kueue-test-e2e-release-0-14-1-35/2009881132048322560

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-11T09:24:02Z

We are tracking and investigating the root casue in https://github.com/kubernetes-sigs/kueue/pull/8516

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-11T09:24:18Z

/assign @sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T12:45:34Z

/remove-kind flake
/kind failing-test
As it fails consistently

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-01-12T19:35:38Z

/close
as this is fixed in https://github.com/kubernetes-sigs/kueue/pull/8541

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-01-12T19:35:44Z

@sohankunkerkar: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/8523#issuecomment-3740179987):

>/close
>as this is fixed in https://github.com/kubernetes-sigs/kueue/pull/8541


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
