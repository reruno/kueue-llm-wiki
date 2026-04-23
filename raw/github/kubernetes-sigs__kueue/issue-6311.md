# Issue #6311: Refactor ProvRequest tests to use active LocalQueues and ClusterQueues

**Summary**: Refactor ProvRequest tests to use active LocalQueues and ClusterQueues

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6311

**Last updated**: 2025-08-06T15:09:27Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-31T07:09:14Z
- **Updated**: 2025-08-06T15:09:27Z
- **Closed**: 2025-08-06T15:09:27Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently most of the tests in [ProvReq suite](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go) is using inactive LocalQueues and ClusterQueues. 

This is probably because a small subset of tests requires the AC to be pending. I expect such tests should be extracted to a separate dedicated and small "When(AC is inactive)". 

**Why is this needed**:

It makes debugging the tests confusing, because workloads in inactive LQ and CQ should not be have quota reserved. We reserve quota for them bypassing scheduler. Even if this works it is confusing when reading logs.

On top of that the "ReadyAC" variable is used for the pending AC which actually is blocking the admission (in most tests): https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go#L850-L853

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-31T07:09:34Z

cc @PBundyra @mbobrovskyi @mszadkow @vladikkuzn

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T14:24:27Z

/assign
