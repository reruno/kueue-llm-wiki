# Issue #2257: Flaky integration test: " Pod controller when manageJobsWithoutQueueName is disabled when Using pod group Should keep the running pod group with the queue name if workload is evicted"

**Summary**: Flaky integration test: " Pod controller when manageJobsWithoutQueueName is disabled when Using pod group Should keep the running pod group with the queue name if workload is evicted"

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2257

**Last updated**: 2024-05-22T14:20:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2024-05-22T13:17:57Z
- **Updated**: 2024-05-22T14:20:30Z
- **Closed**: 2024-05-22T14:20:28Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->

/kind flake


**What happened**:
Integration test of the pod controller failed

**What you expected to happen**:

**How to reproduce it (as minimally and precisely as possible)**:
https://prow.k8s.io/view/gs/kubernetes-jenkins/pr-logs/pull/kubernetes-sigs_kueue/2255/pull-kueue-test-integration-main/1793264698469126144

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

### Comment by [@trasc](https://github.com/trasc) — 2024-05-22T14:20:23Z

/close 
duplicate of #2243

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-22T14:20:29Z

@trasc: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2257#issuecomment-2124926475):

>/close 
>duplicate of #2243 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
