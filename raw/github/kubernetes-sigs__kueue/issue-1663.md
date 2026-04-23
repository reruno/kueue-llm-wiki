# Issue #1663: Fleky multikueue E2E tests

**Summary**: Fleky multikueue E2E tests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1663

**Last updated**: 2024-02-05T10:24:32Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-01-29T10:41:43Z
- **Updated**: 2024-02-05T10:24:32Z
- **Closed**: 2024-02-05T10:24:30Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 4

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

The below error happened:

```shell
{Timed out after 30.000s.
Expected
    <nil>: nil
to be a NotFound error failed [FAILED] Timed out after 30.000s.
Expected
    <nil>: nil
to be a NotFound error
In [BeforeSuite] at: /home/prow/go/src/sigs.k8s.io/kueue/test/util/e2e.go:74 @ 01/29/24 10:28:36.861
}
```

**What you expected to happen**:

No errors happened.

**How to reproduce it (as minimally and precisely as possible)**:

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1662/pull-kueue-test-e2e-main-1-29/1751913992147701760

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-29T10:41:49Z

/kind flake

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-29T10:42:55Z

cc: @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-02-05T10:24:25Z

/close

This happened because out of the two replicas of kueue-controller-manager the one that is not the leader finished seting up the certificates and is able to perform the webhook actions (including adding RF finalizers), but the leader is still waiting for the certificate generation hence is unable to remove the RF finalizers.

However the way we wait for kueue to be ready has changed in #1674

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-02-05T10:24:30Z

@trasc: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1663#issuecomment-1926657581):

>/close
>
>This happened because out of the two replicas of kueue-controller-manager the one that is not the leader finished seting up the certificates and is able to perform the webhook actions (including adding RF finalizers), but the leader is still waiting for the certificate generation hence is unable to remove the RF finalizers.
>
>However the way we wait for kueue to be ready has changed in #1674


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
