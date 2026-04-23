# Issue #3197: Release-0.8: Fix PartialAdmission bugs

**Summary**: Release-0.8: Fix PartialAdmission bugs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3197

**Last updated**: 2024-10-09T17:41:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2024-10-08T16:22:51Z
- **Updated**: 2024-10-09T17:41:36Z
- **Closed**: 2024-10-09T17:41:34Z
- **Labels**: `kind/bug`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 6

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:
Recently, we have fixed some PartialAdmission bugs, but those PRs were not cherry picked to release-0.8.
So, after summarizing all PartialAdmission bugs here, we will cherry-pick those to release-0.8 branch.

candidates:
- [x] https://github.com/kubernetes-sigs/kueue/pull/3152
- [x] https://github.com/kubernetes-sigs/kueue/pull/2826
- [x] https://github.com/kubernetes-sigs/kueue/pull/3118
- [x] https://github.com/kubernetes-sigs/kueue/pull/3153

**What you expected to happen**:
Fixed PartialAdmission bugs in the release-0.8 branch as well.

**How to reproduce it (as minimally and precisely as possible)**:

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-09T07:23:38Z

I think we also need:
- https://github.com/kubernetes-sigs/kueue/pull/3118
- https://github.com/kubernetes-sigs/kueue/pull/3153

cc @trasc would you like to prepare the cherry-picks?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-09T11:28:31Z

> I think we also need:
> 
> * [[workload]Fix resource consumption computation for partially admitted workloads #3118](https://github.com/kubernetes-sigs/kueue/pull/3118)
> * [[batch/job] Fix parallelism restoration after partial admission. #3153](https://github.com/kubernetes-sigs/kueue/pull/3153)
> 
> cc @trasc would you like to prepare the cherry-picks?

Thank you for pointing those out. I updated the description.

### Comment by [@trasc](https://github.com/trasc) — 2024-10-09T12:23:49Z

> cc @trasc would you like to prepare the cherry-picks?

Sure
/assign

### Comment by [@trasc](https://github.com/trasc) — 2024-10-09T14:25:57Z

- #3205
- #3206
- #3207
- #3208

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-09T17:41:30Z

@trasc Thanks!
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-10-09T17:41:35Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3197#issuecomment-2402920920):

>@trasc Thanks!
>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
