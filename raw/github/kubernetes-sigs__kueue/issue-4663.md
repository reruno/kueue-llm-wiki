# Issue #4663: Add a "functional" test case for the scenario in scheduler_test for issue #2391

**Summary**: Add a "functional" test case for the scenario in scheduler_test for issue #2391

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4663

**Last updated**: 2026-04-21T14:05:40Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-18T07:56:00Z
- **Updated**: 2026-04-21T14:05:40Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `lifecycle/rotten`
- **Assignees**: [@Horiodino](https://github.com/Horiodino)
- **Comments**: 16

## Description

**What would you like to be cleaned**:

I would like to have a functional test in scheduler_test.go which demonstrates the fix implemented in https://github.com/kubernetes-sigs/kueue/pull/2407 works. 

**Why is this needed**:

Currently, we have tests which only assert the internal state of TriedFlavorIdx added as part of https://github.com/kubernetes-sigs/kueue/pull/2407.

However, we should test for user-observable behavior to allow refactoring of the current solution.

One refactoring is proposed in https://github.com/kubernetes-sigs/kueue/pull/4662, but we may get future requests too. Without the functional test we will be uncertain about the refactorings.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T07:56:50Z

cc @xiongzubiao @PBundyra @gabesaba

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T07:59:28Z

Did you see any other lack of functional scheduler tests?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-18T08:19:31Z

There are probably some gaps, but I don't have any on the top of my head. 

I would prefer to focus the issue on this specific one, as motivated by the proposed fix and refactoring.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-18T08:25:41Z

> I would prefer to focus the issue on this specific one, as motivated by the proposed fix and refactoring.

SGTM

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-03-18T09:56:01Z

/retitle Add a "functional" test case for the scenario in scheduler_test for issue #2391

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-03-20T06:23:39Z

@xiongzubiao If you want to take this one, you can comment with `/assign`.

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-03-22T16:45:38Z

/assign

### Comment by [@Horiodino](https://github.com/Horiodino) — 2025-03-22T16:46:37Z

`/assign` if no one is working on this. Writing test cases is a great way to understand the internals of the code.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-24T20:07:55Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-25T05:54:58Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-23T06:36:53Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-23T06:48:31Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-22T07:43:07Z

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

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-12-22T12:33:46Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-22T13:28:21Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-21T14:05:37Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/
