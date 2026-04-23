# Issue #9182: Bump controller runtime for Kueue populator

**Summary**: Bump controller runtime for Kueue populator

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9182

**Last updated**: 2026-02-15T05:14:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-12T17:06:49Z
- **Updated**: 2026-02-15T05:14:35Z
- **Closed**: 2026-02-15T05:14:34Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Unblock controller runtime upgrade by dependabot https://github.com/kubernetes-sigs/kueue/pull/9154 

**Why is this needed**:

To make the future upgrades by dependabot possible

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-02-15T05:14:29Z

Actually, I think we can close this. The issue occurs because the populator is using an old Kueue version, which in turn uses an outdated version of controller-runtime, leading to dependency conflicts. So I think the only way to bump controller-runtime is to bump Kueue as well.

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-02-15T05:14:34Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9182#issuecomment-3903335511):

>Actually, I think we can close this. The issue occurs because the populator is using an old Kueue version, which in turn uses an outdated version of controller-runtime, leading to dependency conflicts. So I think the only way to bump controller-runtime is to bump Kueue as well.
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
