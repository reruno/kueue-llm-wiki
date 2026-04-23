# Issue #2393: Flaky test: Kueuectl List when List ClusterQueue when List Workloads Should print workloads list with paging

**Summary**: Flaky test: Kueuectl List when List ClusterQueue when List Workloads Should print workloads list with paging

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2393

**Last updated**: 2024-06-10T15:36:28Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-06-10T15:32:34Z
- **Updated**: 2024-06-10T15:36:28Z
- **Closed**: 2024-06-10T15:36:26Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description


**What happened**:

kueuectl test failed on unreleated branch: https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2392/pull-kueue-test-integration-main/1800186041294917632

**What you expected to happen**:

No failure

**How to reproduce it (as minimally and precisely as possible)**:

Repeat the build

**Anything else we need to know?**:

```
Kueuectl Suite: [It] Kueuectl List when List ClusterQueue when List Workloads Should print workloads list with paging expand_less	1s
{Expected
    <string>: "...     0s
    wl1..."
to equal               |
    <string>: "...     1s
    wl1..." failed [FAILED] Expected
    <string>: "...     0s
    wl1..."
to equal               |
    <string>: "...     1s
    wl1..."
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/kueuectl/list_test.go:227 @ 06/10/24 15:26:45.03
}
```
**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-10T15:32:48Z

/kind flake

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-10T15:32:56Z

cc @mbobrovskyi

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-10T15:36:23Z

/close
as duplicate of https://github.com/kubernetes-sigs/kueue/issues/2353

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-10T15:36:27Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2393#issuecomment-2158679663):

>/close
>as duplicate of https://github.com/kubernetes-sigs/kueue/issues/2353


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
