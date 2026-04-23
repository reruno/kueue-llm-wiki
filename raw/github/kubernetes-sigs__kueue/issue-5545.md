# Issue #5545: Add a customconfig e2e test of Kueue without alpha-level APIs

**Summary**: Add a customconfig e2e test of Kueue without alpha-level APIs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5545

**Last updated**: 2026-02-04T14:31:42Z

---

## Metadata

- **State**: open
- **Author**: [@dgrove-oss](https://github.com/dgrove-oss)
- **Created**: 2025-06-06T15:59:08Z
- **Updated**: 2026-02-04T14:31:42Z
- **Closed**: —
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a customconfig e2e test where we install Kueue without any alpha-level APIs and run a few representative workloads to verify the system is working as expected.

**Why is this needed**:

To ensure that all uses of alpha-level APIs in the Kueue codebase are properly guarded by feature gates.  It simulates downstream production use cases where alpha-level APIs are not installed.

**Completion requirements**:

Changes are made as needed to enable automated installation of Kueue without alpha-level APIs and an e2e test is defined.

## Discussion

### Comment by [@dgrove-oss](https://github.com/dgrove-oss) — 2025-06-09T13:05:34Z

/cc @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-06-09T13:18:29Z

TBH I don't feel that strong that this should be a e2e test. It seems like overkill as from what I found the bugs related to this were subtle.

For example, I only discovered HierarchicalCohorts issue when I looked at the logs of Kueue.


cc @tenzen-y @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-09T13:21:28Z

I don't have a strong view here, but I'm ok with the sanity check if @dgrove-oss finds it useful.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-07T13:24:50Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-10-07T13:59:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T14:00:17Z

/remove-lifecycle rotten

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-04T14:28:41Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-04T14:31:39Z

/remove-lifecycle rotten
