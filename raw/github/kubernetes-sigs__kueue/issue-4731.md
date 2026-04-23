# Issue #4731: release-0.10 branch: failed to detect containerd snapshotter in CI

**Summary**: release-0.10 branch: failed to detect containerd snapshotter in CI

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4731

**Last updated**: 2025-03-21T07:08:34Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-03-21T05:45:45Z
- **Updated**: 2025-03-21T07:08:34Z
- **Closed**: 2025-03-21T07:08:32Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Our release-0.10 CI was broken by upgrading Kind cluster version in https://github.com/kubernetes/test-infra/pull/34564

- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-10-1-29/1902898218627239936
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-10-1-30/1902898470214176768
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-e2e-release-0-10-1-31/1902898470319034368

```shell
Digest: sha256:67a12fef1c7ad21df600874e4194ff0c78e46430d0bb56b689f6a5894d87d973
Status: Downloaded newer image for registry.k8s.io/jobset/jobset:v0.7.1
registry.k8s.io/jobset/jobset:v0.7.1
Image: "registry.k8s.io/e2e-test-images/agnhost:2.52" with ID "sha256:a0a1ebb2fc2d2a7c926ec4cf72b9308f06400d9254a5f873c17e66cb76cd3e11" not yet present on node "kind-control-plane", loading...
Image: "registry.k8s.io/e2e-test-images/agnhost:2.52" with ID "sha256:a0a1ebb2fc2d2a7c926ec4cf72b9308f06400d9254a5f873c17e66cb76cd3e11" not yet present on node "kind-worker2", loading...
Image: "registry.k8s.io/e2e-test-images/agnhost:2.52" with ID "sha256:a0a1ebb2fc2d2a7c926ec4cf72b9308f06400d9254a5f873c17e66cb76cd3e11" not yet present on node "kind-worker", loading...
ERROR: failed to detect containerd snapshotter
```

**What you expected to happen**:

No errors.

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

The error reason could be considered https://github.com/kubernetes-sigs/kind/issues/3853

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-21T05:46:42Z

cc: @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-21T07:08:27Z

/close
As addressed in https://github.com/kubernetes-sigs/kueue/pull/4732

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-21T07:08:33Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4731#issuecomment-2742533319):

>/close
>As addressed in https://github.com/kubernetes-sigs/kueue/pull/4732


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
