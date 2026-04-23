# Issue #2446: Flaky e2e test for MultiKueue

**Summary**: Flaky e2e test for MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2446

**Last updated**: 2024-06-20T18:31:26Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-06-19T12:01:55Z
- **Updated**: 2024-06-20T18:31:26Z
- **Closed**: 2024-06-20T18:31:24Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->
/kind flake

**What happened**:
E2e test for MultiKueue failed

**What you expected to happen**:
No failure

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2408/pull-kueue-test-multikueue-e2e-main/1803390960541896704

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

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-19T12:15:17Z

I'm not sure that it's kueue error.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-06-19T19:52:21Z

Looks like it's limitation to running max count of parallel jobs.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-06-20T09:15:31Z

I'm not very familiar with this part of [test-infra](https://github.com/kubernetes/test-infra), but maybe we can use the occurrences like this as potential motivation to increase the number of nodes in the cluster? cc @alculquicondor

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-20T18:31:20Z

Uhm.... this is about the number of nodes in the test-infra cluster, not our tests' kind clusters.

There isn't much we can do from our side.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-20T18:31:25Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2446#issuecomment-2181296004):

>Uhm.... this is about the number of nodes in the test-infra cluster, not our tests' kind clusters.
>
>There isn't much we can do from our side.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
