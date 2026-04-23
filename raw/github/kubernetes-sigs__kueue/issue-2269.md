# Issue #2269: Kueue might lose fields when admitting jobs

**Summary**: Kueue might lose fields when admitting jobs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2269

**Last updated**: 2024-07-11T20:30:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-05-23T15:41:14Z
- **Updated**: 2024-07-11T20:30:37Z
- **Closed**: 2024-07-11T20:30:37Z
- **Labels**: `kind/bug`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 10

## Description

**What happened**:

Whenever Kueue APIs are a version behind the latest version for a particular job type, there is the risk of dropping fields, because of the use of `Update`.

We should be using `Patch` instead.

**What you expected to happen**:

Kueue to be resilient to upgrades of Job CRDs.

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-23T15:41:22Z

/assign @PBundyra

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-23T17:13:08Z

As a hotfix for jobset integration, we need to bump the version of jobset in the release-0.6 branch.

We might have to do it manually https://github.com/kubernetes-sigs/kueue/pull/1984

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T18:25:48Z

intersting. Which job types did you observe this issue?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T18:42:00Z

jobset

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T18:47:43Z

I see. It's only JobSet. Thanks.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-24T18:50:42Z

It could be anything, but jobset is the only API that is changing quite fast.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-05-24T18:54:41Z

> It could be anything, but jobset is the only API that is changing quite fast.

That makes sense.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T14:17:52Z

/assign @mbobrovskyi 
/unassign @PBundyra

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-09T15:08:57Z

/reopen
Let's keep it open to keep track of the outstanding work in https://github.com/kubernetes-sigs/kueue/pull/2553 which is not just cleanup but also semantic change from non-strict to strict patches.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-07-09T15:09:02Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2269#issuecomment-2217979517):

>/reopen
>Let's keep it open to keep track of the outstanding work in https://github.com/kubernetes-sigs/kueue/pull/2553 which is not just cleanup but also semantic change from non-strict to strict patches.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
