# Issue #5429: Support KubeRay RayService as a Kueue workload

**Summary**: Support KubeRay RayService as a Kueue workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5429

**Last updated**: 2025-07-07T18:02:40Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@andrewsykim](https://github.com/andrewsykim)
- **Created**: 2025-05-30T20:39:50Z
- **Updated**: 2025-07-07T18:02:40Z
- **Closed**: 2025-07-07T18:02:40Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 7

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Today Kueue supports `RayJob` and `RayCluster` as a supported workload but does not support RayService. I've heard feedback from some KubeRay users asking for RayService support. Similar to RayCluster support, we should support RayService as a kueue-able workload but without autoscaling support.  

**Why is this needed**:

RayService is the only KubeRay resource not supported by Kueue. We should support it for full feature parity with KubeRay.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [X] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kimminw00](https://github.com/kimminw00) — 2025-06-04T02:05:02Z

+1
Advanced scheduling features like `Topology Aware Scheduling` (TAS) and `All-or-Nothing with Ready Pods` is essential in production-grade inference workloads.

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-06-10T16:48:25Z

@weizhaowz do you have cycles to implement this?

### Comment by [@weizhaowz](https://github.com/weizhaowz) — 2025-06-10T17:30:42Z

> [@weizhaowz](https://github.com/weizhaowz) do you have cycles to implement this?

Yes, I can do it.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-26T09:05:43Z

Thank you folks for driving that!

### Comment by [@weizhaowz](https://github.com/weizhaowz) — 2025-07-07T17:53:05Z

Initially I tried add RayService controller, webhook and multikueue-adapter in [pr](https://github.com/kubernetes-sigs/kueue/pull/5664), but in testing, I found the the RayCluster created for the RayService cannot be updated as the RayCluster is managed by its own controller, so KubeRay cannot provision the RayCluster. Therefore, we decide to let Kueue manage RayService through RayCluster, and this [pr](https://github.com/kubernetes-sigs/kueue/pull/5822) contains details

### Comment by [@andrewsykim](https://github.com/andrewsykim) — 2025-07-07T18:02:35Z

Thanks @weizhaowz 

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-07-07T18:02:40Z

@andrewsykim: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5429#issuecomment-3046089429):

>Thanks @weizhaowz 
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
