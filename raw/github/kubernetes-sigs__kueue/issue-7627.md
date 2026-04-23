# Issue #7627: Balanced placement cleanup: consider injecting the code inside the stepping down loop

**Summary**: Balanced placement cleanup: consider injecting the code inside the stepping down loop

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7627

**Last updated**: 2025-12-19T10:35:17Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-11-13T08:36:42Z
- **Updated**: 2025-12-19T10:35:17Z
- **Closed**: 2025-12-19T10:35:16Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@pajakd](https://github.com/pajakd)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to try to inject the balanced placement algorithm deeper, preserving the overall structure for all algorithms for stepping down.

https://github.com/kubernetes-sigs/kueue/pull/6851#discussion_r2518884113

**Why is this needed**:

Reuse of the code for the main structure of the TAS algororithms,

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-13T08:37:04Z

/assign @pajakd 
cc @mwysokin 
tentatively

### Comment by [@pajakd](https://github.com/pajakd) — 2025-11-17T13:44:19Z

Left https://github.com/kubernetes-sigs/kueue/pull/7700#discussion_r2533740408 for the next follow up

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:35:11Z

/close
Let's close for now to avoid distraction. We can do the follow up refactor when this becomes needed.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-12-19T10:35:17Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7627#issuecomment-3674538032):

>/close
>Let's close for now to avoid distraction. We can do the follow up refactor when this becomes needed.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
