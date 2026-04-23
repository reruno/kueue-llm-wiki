# Issue #8287: TrainJob integration: eliminate the post-processing code for Trainer helpers to handle numNodes correctly

**Summary**: TrainJob integration: eliminate the post-processing code for Trainer helpers to handle numNodes correctly

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8287

**Last updated**: 2026-04-07T21:12:07Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-17T08:03:11Z
- **Updated**: 2026-04-07T21:12:07Z
- **Closed**: —
- **Labels**: `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@NarayanaSabari](https://github.com/NarayanaSabari)
- **Comments**: 7

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to eliminate the special handling of numNodes inside Kueue code: https://github.com/kubernetes-sigs/kueue/pull/8135/changes#diff-eb30173c6ca84a779cd005d1c147a311b18a077bd35205dc64942fd824ffb3e4R181-R187

**Why is this needed**:

I think the correct numbers of Pods (and PodSets)  should already be returned by Kubeflow helpers. Other projects using the helpers will need to do the same

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T08:04:44Z

cc @kaisoz @NarayanaSabari ptal. Feel free to collab on this. It also will require an issue in Kubeflow I think, opened: https://github.com/kubeflow/trainer/issues/3042

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T08:11:39Z

cc @tenzen-y @andreyvelich

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-17T13:48:39Z

> cc [@kaisoz](https://github.com/kaisoz) [@NarayanaSabari](https://github.com/NarayanaSabari) ptal. Feel free to collab on this. It also will require an issue in Kubeflow I think, opened: [kubeflow/trainer#3042](https://github.com/kubeflow/trainer/issues/3042)

Sorry for not following this up earlier as I said I would. I'll chime in in the Trainer issue

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T09:28:16Z

/priority important-soon

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2025-12-24T10:36:38Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-24T10:57:22Z

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

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-04-07T21:12:03Z

/remove-lifecycle stale
