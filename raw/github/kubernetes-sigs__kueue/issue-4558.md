# Issue #4558: Enable e2e testing  in a user opt-in namespace

**Summary**: Enable e2e testing  in a user opt-in namespace

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4558

**Last updated**: 2025-06-20T14:10:53Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2025-03-11T14:31:01Z
- **Updated**: 2025-06-20T14:10:53Z
- **Closed**: 2025-06-20T14:10:53Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently, Kueue’s e2e tests are hardcoded to run in the `kueue-system` namespace, limiting flexibility for users/downstream contributors, who may want to test in other namespaces. There should be a mechanism to allow e2e tests to run in any namespace by providing a configuration option to specify a namespace.

**Why is this needed**:

This change would enhance usability and adaptability of the e2e testing in the downstream forks.

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-03-11T14:31:29Z

/assign sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-11T14:37:20Z

+1, you can also consider using the customconfigs suite for that, if the main one is problematic.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-09T14:50:16Z

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

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-06-09T16:14:04Z

/remove-lifecycle stale
