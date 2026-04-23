# Issue #5246: TAS: implement exponential backoff for second pass of scheduler

**Summary**: TAS: implement exponential backoff for second pass of scheduler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5246

**Last updated**: 2025-09-26T13:18:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-14T11:45:48Z
- **Updated**: 2025-09-26T13:18:20Z
- **Closed**: 2025-09-26T13:18:20Z
- **Labels**: `kind/feature`
- **Assignees**: [@mykysha](https://github.com/mykysha), [@mimowo](https://github.com/mimowo)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Implement exponential backoff for the second pass of scheduler for as planed in the TAS KEP. 

This is a follow up to https://github.com/kubernetes-sigs/kueue/pull/5052

**Why is this needed**:

It may take minutes before the provisioned nodes become ready. Assume it takes 3min it means 180 failed attempts to wait for the nodes. 

With exponential delay of in second: 1, 2, 4, 8, 16, 32, 64, 128 this will be around 8 retries only. The logs will be much cleaner, and scheduler offloaded.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-14T11:46:14Z

cc @PBundyra @tenzen-y 
/assign
tentatively

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-12T12:13:47Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-12T12:38:31Z

/remove-lifecycle stale

### Comment by [@mykysha](https://github.com/mykysha) — 2025-08-21T12:14:24Z

/assign
