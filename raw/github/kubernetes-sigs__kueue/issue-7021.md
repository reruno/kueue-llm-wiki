# Issue #7021: Create a test util function for asserting `admissionCheckState`

**Summary**: Create a test util function for asserting `admissionCheckState`

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7021

**Last updated**: 2026-03-16T16:53:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@PBundyra](https://github.com/PBundyra)
- **Created**: 2025-09-26T10:03:31Z
- **Updated**: 2026-03-16T16:53:41Z
- **Closed**: 2026-03-16T16:53:41Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@reruno](https://github.com/reruno)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Create a test util function that with a header along the lines:
```
func ExpectAdmissionCheckState(wl kueue.Workload, acName string, expectedState kueue.CheckState, expectedMessage string)
```
that asserts if a Workload has admission check with desired fields

The function should be used across the codebase, especially in `test/integration/singlecluster/controller/admissionchecks/provisioning/provisioning_test.go`

**Why is this needed**:
Context: https://github.com/kubernetes-sigs/kueue/pull/6408/files#r2251649819
To make test more readable and robust

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-26T11:19:17Z

cc @olekzabl

### Comment by [@aatia-commits](https://github.com/aatia-commits) — 2025-10-07T14:16:11Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-05T14:24:11Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@PBundyra](https://github.com/PBundyra) — 2026-01-08T10:30:37Z

/remove-lifecycle stale

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2026-03-05T12:08:52Z

/unassign @aatia-commits

### Comment by [@reruno](https://github.com/reruno) — 2026-03-05T12:09:24Z

/assign @reruno
