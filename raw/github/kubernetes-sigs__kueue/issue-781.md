# Issue #781: [dep] Use a released version of Ray operator

**Summary**: [dep] Use a released version of Ray operator

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/781

**Last updated**: 2023-07-04T12:32:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-05-19T06:45:28Z
- **Updated**: 2023-07-04T12:32:59Z
- **Closed**: 2023-07-04T12:32:59Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
A released version of `github.com/ray-project/kuberay/ray-operator` should be used instead of `v0.0.0-20230516192117-9bc5d854bd31` once https://github.com/ray-project/kuberay/commit/9bc5d854bd316c46a79920bbd7b2887fb0c6d0af is part of one, probably v0.6.0.



**Why is this needed**:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-19T13:39:36Z

do you know of any time estimates for this? I wonder if we can wait for the release before releasing Kueue 0.4 by the end-of-june

### Comment by [@trasc](https://github.com/trasc) — 2023-05-19T13:47:19Z

It looks like they have ~2 releases per year,  and the last one was April 11, so maybe Q3-Q4, but we could ask.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-29T16:58:16Z

was there a release?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-06-29T17:00:38Z

> was there a release?

Here: https://github.com/ray-project/kuberay/releases/tag/v0.5.2

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-29T17:17:06Z

/assign @trasc
