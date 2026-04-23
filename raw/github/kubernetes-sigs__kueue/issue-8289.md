# Issue #8289: WaitForPodsReady documetation Adjust the first snippet to use `blockAdmission: false`

**Summary**: WaitForPodsReady documetation Adjust the first snippet to use `blockAdmission: false`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8289

**Last updated**: 2025-12-18T09:35:22Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-17T08:35:38Z
- **Updated**: 2025-12-18T09:35:22Z
- **Closed**: 2025-12-18T09:35:22Z
- **Labels**: `kind/documentation`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 1

## Description

<!-- Please use this template for documentation-related issues -->

**What would you like to be documented or improved**:

I would like to use `blockAdmission: false` in the main snippet on this page, because users will often copy-paste that snippet.

We should just mention in the example https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/#example that it is using "blockAdmission: true". And note that the example is not using TopologyAwareScheduling, which could also solve the mentioned problem.

**Location** (URL, file path, or section if applicable):

https://kueue.sigs.k8s.io/docs/tasks/manage/setup_wait_for_pods_ready/#enabling-waitforpodsready

## Discussion

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-12-18T08:08:58Z

/assign
