# Issue #620: Performance degradation in scheduler with additional metrics for tracking go-routines

**Summary**: Performance degradation in scheduler with additional metrics for tracking go-routines

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/620

**Last updated**: 2023-03-09T17:10:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-03-09T17:00:51Z
- **Updated**: 2023-03-09T17:10:29Z
- **Closed**: 2023-03-09T17:10:27Z
- **Labels**: `kind/bug`, `sig/scheduling`
- **Assignees**: _none_
- **Comments**: 5

## Description

**What happened**:

We observed degradation in scheduling throughput, putting it under 100 pods/s

pprof points to https://github.com/kubernetes/kubernetes/pull/112003/files#diff-bdc8ab11c11340bf2786fe2a0a3900856fa6d098c0c217ba6b25de33ca22a506R58-R59

![image](https://user-images.githubusercontent.com/1299064/224100503-708cb729-6a4c-48fe-b634-66421dd8e180.png)


**What you expected to happen**:

100 pods/s

**How to reproduce it (as minimally and precisely as possible)**:

N/A

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`): 1.26
- Kueue version (use `git describe --tags --dirty --always`):
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-09T17:01:38Z

/sig scheduling
/assign @mborsz

cc @sanposhiho

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-03-09T17:01:40Z

@alculquicondor: GitHub didn't allow me to assign the following users: mborsz.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people) with read permissions, repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/620#issuecomment-1462423991):

>/sig scheduling
>/assign @mborsz
>
>cc @sanposhiho 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-09T17:06:40Z

@alculquicondor Here is the kueue repo. it looks like this issue mentions the kube-scheduler, not the kueue-scheduler.
Should we create this issue in k/k?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-09T17:10:23Z

lol, sorry
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-03-09T17:10:28Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/620#issuecomment-1462437508):

>lol, sorry
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
