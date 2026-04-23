# Issue #9419: KubeRay e2e tests cleanup

**Summary**: KubeRay e2e tests cleanup

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9419

**Last updated**: 2026-02-24T07:01:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-23T11:38:45Z
- **Updated**: 2026-02-24T07:01:37Z
- **Closed**: 2026-02-24T07:01:37Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Couple of cleanups:
- use the new helpers for the pre-existing tests in `test/e2e/singlecluster/kuberay_test.go` as they were added here:  https://github.com/kubernetes-sigs/kueue/pull/9102/changes#diff-8e3047d39693f7182e27b043adafb5a76db1d44c8923c03f7c561d8a3ea194a6R478-R483
- align the requests and limits for the Pods, 1500m seems too much. Maybe we could standardize at 500m or so

**Why is this needed**:

To keep the test code clean and easy to maintain.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-23T11:38:51Z

cc @hiboyang
