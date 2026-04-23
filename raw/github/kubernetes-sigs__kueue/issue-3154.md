# Issue #3154: [Flaky test]  RayCluster controller Should reconcile RayClusters

**Summary**: [Flaky test]  RayCluster controller Should reconcile RayClusters

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3154

**Last updated**: 2024-09-27T17:17:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-27T17:16:23Z
- **Updated**: 2024-09-27T17:17:17Z
- **Closed**: 2024-09-27T17:17:15Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 3

## Description

**What happened**:

test flaked on unrelated branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/3132/pull-kueue-test-integration-main/1839710600372948992

**What you expected to happen**:

No random failures

**How to reproduce it (as minimally and precisely as possible)**:

repeat the build on CI

**Anything else we need to know?**:


```
{Timed out after 5.001s.
Expected
    <bool>: false
to be true failed [FAILED] Timed out after 5.001s.
Expected
    <bool>: false
to be true
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/raycluster/raycluster_controller_test.go:192 @ 09/27/24 17:05:36.027
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-27T17:16:36Z

/kind flake
/cc @mbobrovskyi @trasc

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-27T17:17:11Z

Oh, duplicate of https://github.com/kubernetes-sigs/kueue/issues/3144
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-27T17:17:16Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3154#issuecomment-2379732242):

>Oh, duplicate of https://github.com/kubernetes-sigs/kueue/issues/3144
>/close 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
