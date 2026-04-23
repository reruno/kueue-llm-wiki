# Issue #3796: Introduce sanity e2e tests for the dashboard

**Summary**: Introduce sanity e2e tests for the dashboard

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3796

**Last updated**: 2025-05-14T11:21:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-12-10T15:15:39Z
- **Updated**: 2025-05-14T11:21:20Z
- **Closed**: 2025-05-14T11:21:20Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 8

## Description

**What would you like to be added**:

e2e sanity tests for the dashboard

**Why is this needed**:

With the recent addition of dependabot [PR](https://github.com/kubernetes-sigs/kueue/pull/3780), and the following upgrades the dashboard is broken apparently after upgrade of react to 19.

It would be great to have some sort of "sanity" validation for the project. We can have a dedicated CI job for that, as we have for tas and multikueue features.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-10T15:16:00Z

cc @mbobrovskyi @akram

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-11T18:29:54Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-17T14:32:09Z

/unassign

Sorry, I don't have capacity to work on it for now.

### Comment by [@akram](https://github.com/akram) — 2025-01-02T14:11:46Z

back from PTO, I will put that on my bucket.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-02T15:49:21Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-03T09:22:59Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-03T09:26:16Z

I believe the work is almost done, with the e2e tests under `cmd/kueueviz/frontend/cypress/e2e`.

Before we close I would yet prefer to move the tests under `test/e2e/kueueviz` for consistency with the placement of other e2e tests for the CI jobs.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-03T09:27:25Z

For reference, the tests were added in https://github.com/kubernetes-sigs/kueue/pull/4596.
