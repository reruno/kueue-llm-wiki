# Issue #6489: Stopgap to prevent a CQ from being blocked by head - Implement timeout

**Summary**: Stopgap to prevent a CQ from being blocked by head - Implement timeout

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6489

**Last updated**: 2025-09-23T21:31:31Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@amy](https://github.com/amy)
- **Created**: 2025-08-06T21:04:16Z
- **Updated**: 2025-09-23T21:31:31Z
- **Closed**: 2025-09-23T21:31:30Z
- **Labels**: `kind/feature`
- **Assignees**: [@amy](https://github.com/amy)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
Because CQ heads are blocking, pending preemption of the preemption target, we have this scenario in production:

- We have a pod stuck in terminating. This blocks its own CQ for hours.
- let's implement a timeout where if the pod has been stuck in terminating beyond a specific duration, we remove it from being considered as a preemption target

**Why is this needed**:
We need a way for a CQ to progress past the CQ head and not hold back the entire queue.

Note: This does NOT solve that CQ admission is incredibly slow if every reclamation needs to involve a preemption.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-08-06T21:49:24Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T11:29:16Z

I think this deserves a KEP, because:
- the new timeout likely requires API configuration
- it is not clear for me atm how to measure it
- maybe instead of a Pod we could consider Workload as the unit of preemption for which we measure the timeout. Then, maybe this is equivalent with waiting for `Eviction=True` until `QuotaReserved=False || Deactivated || Finished`.

### Comment by [@rphillips](https://github.com/rphillips) — 2025-08-12T20:30:54Z

Perhaps consider using the pod's terminatonGracePeriodSeconds timeout + some fudge factor. Kueue might not need an API change.

### Comment by [@amy](https://github.com/amy) — 2025-08-12T20:37:13Z

@rphillips what is fudge factor?

And this is specific to when we do use terminationGracePeriodSeconds timeout + prestop lifecycle hooks on pods + pod workload type. You can see the full context here (context is long so feel free to ask any clarifying questions, ended up splitting 6143 into 6143 + 2 other issues): https://github.com/kubernetes-sigs/kueue/issues/6143

TLDR; this problem would be solved if we used Job workload type. But we can't. Kueue will block on preemption until the workload is preempted. And in this case, if you have zombie pods, the workload never gets preempted blocking the entire cq queue.

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-09-23T14:42:41Z

@amy Has this issue been resolved with https://github.com/kubernetes-sigs/kueue/pull/6872? Or is there more to it?

### Comment by [@amy](https://github.com/amy) — 2025-09-23T21:31:25Z

yup! Its resolved. Closing!

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-09-23T21:31:31Z

@amy: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6489#issuecomment-3325621193):

>yup! Its resolved. Closing!
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
