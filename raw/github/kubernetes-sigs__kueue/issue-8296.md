# Issue #8296: TrainJob integration: Job should be unsuspended and updated in a single API request

**Summary**: TrainJob integration: Job should be unsuspended and updated in a single API request

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8296

**Last updated**: 2026-04-22T09:26:10Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-17T10:05:10Z
- **Updated**: 2026-04-22T09:26:10Z
- **Closed**: —
- **Labels**: `kind/bug`, `priority/important-soon`, `kind/cleanup`
- **Assignees**: [@NarayanaSabari](https://github.com/NarayanaSabari)
- **Comments**: 8

## Description

/kind bug
I think this is also a small performance bug.

**What would you like to be cleaned**:

Currently when we are starting a TrainJob instance we need to send two API requests to start it:
1. to set unsupend=false
2. to inject the NodeSelectors

**Why is this needed**:

1. To avoid race conditions as the one found here: https://github.com/kubernetes-sigs/kueue/pull/8255#discussion_r2626391001
2. To optimize the number of API request sent to the API server

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T10:05:40Z

cc @kaisoz @j-skiba @NarayanaSabari

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-17T13:45:41Z

The Trainjob admission webhook [requires the Trainjob to be suspended to modify the podTemplateOverrides](https://github.com/kubeflow/trainer/blob/eaa3d859d313824374badbf4c327802639b9fc40/pkg/runtime/framework/plugins/jobset/jobset.go#L167). This is why we first call the API server to update the podTemplateOverrides and then unsuspend the job.

I don't think doing just one API call is possible without Trainer modifications... I remember asking the maintainers about the reason.. let me open an issue in there

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T13:51:13Z

Thank you for the context. It seems reasonable to me to discuss this more under Kubeflow issue.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-17T14:22:24Z

Issue in Trainer: https://github.com/kubeflow/trainer/issues/3043

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:31:57Z

/priority important-soon

### Comment by [@NarayanaSabari](https://github.com/NarayanaSabari) — 2026-01-22T08:47:12Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-22T09:16:37Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-22T09:26:08Z

/remove-lifecycle stale
cc @kaisoz any progress here?
