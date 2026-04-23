# Issue #4665: TAS KubeRay: Strengthen the assert on the number of scheduled Pods

**Summary**: TAS KubeRay: Strengthen the assert on the number of scheduled Pods

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4665

**Last updated**: 2025-03-21T09:10:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-18T08:06:16Z
- **Updated**: 2025-03-21T09:10:41Z
- **Closed**: 2025-03-21T09:10:41Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Strengthen the assert on the number of scheduled Pods after moving to KubeRay 1.3.1.

https://github.com/kubernetes-sigs/kueue/pull/4620/files#diff-7396e17677ba9505b4f650f9b7aada9d3833aa188e6e4a0869dc81164190fbd9R202

See also discussion in https://github.com/kubernetes-sigs/kueue/issues/4508#issuecomment-2724257298
to see why we relaxed the check.

**Why is this needed**:

To make sure all KubeRay pods are getting scheduled.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T08:06:36Z

cc @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-20T09:55:17Z

/assign
