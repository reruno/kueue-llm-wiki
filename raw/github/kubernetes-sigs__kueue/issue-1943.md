# Issue #1943: Flaky integration test for RayJob

**Summary**: Flaky integration test for RayJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1943

**Last updated**: 2024-06-25T20:46:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-04-03T18:36:39Z
- **Updated**: 2024-06-25T20:46:16Z
- **Closed**: 2024-06-25T20:46:14Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

```
RayJob Controller Suite: [It] Job controller with preemption enabled Should preempt lower priority rayJobs when resource insufficient expand_less	20s
{Timed out after 5.001s.
Expected
    <bool>: true
to be false failed [FAILED] Timed out after 5.001s.
Expected
    <bool>: true
to be false
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/controller/jobs/rayjob/rayjob_controller_test.go:735 @ 04/03/24 17:48:18.402
}
```

**What you expected to happen**:

No flakiness

https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/1777/pull-kueue-test-integration-main/1775579633484304384

**How to reproduce it (as minimally and precisely as possible)**:

**Anything else we need to know?**:

It is possible that somehow our new timeout (5s) is too aggressive and we might want to increase it back 10s.

But it's worth investigating if something else could be going on.

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-03T18:37:03Z

/assign @trasc

### Comment by [@trasc](https://github.com/trasc) — 2024-04-08T05:21:28Z

/reopen
In case we see it again. 
https://github.com/kubernetes-sigs/kueue/pull/1951#issuecomment-2040260375

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-04-08T05:23:13Z

@trasc: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1943#issuecomment-2041887606):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:46:11Z

It looks like we haven't seen this again
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T20:46:15Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1943#issuecomment-2189938246):

>It looks like we haven't seen this again
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
