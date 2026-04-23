# Issue #2324: Support ClusterQueues defining DWS flavors

**Summary**: Support ClusterQueues defining DWS flavors

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2324

**Last updated**: 2024-05-29T19:24:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@colinjc](https://github.com/colinjc)
- **Created**: 2024-05-29T18:29:23Z
- **Updated**: 2024-05-29T19:24:35Z
- **Closed**: 2024-05-29T19:19:14Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

We want to be able to define a ClusterQueue that has a default flavor pointing at some fixed resources, and if that's full bursts out using the DWS API. This would be similar to having a fixed cluster that bursts to spot nodes.

**Why is this needed**:

Currently users must either submit to a fixed queue OR a DWS queue, and need to change code to do so. If we could target a single queue, it would be simpler to ensure the fixed cluster is always saturated and DWS is only used when required.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-29T19:19:11Z

This is already supported in the upcoming release of Kueue v0.7.

Please give us one or two days to release. We are just finishing up some documentation #2305

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-05-29T19:19:15Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2324#issuecomment-2138102081):

>This is already supported in the upcoming release of Kueue v0.7.
>
>Please give us one or two days to release. We are just finishing up some documentation #2305
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-05-29T19:24:34Z

BTW, this was the original issue #1432
