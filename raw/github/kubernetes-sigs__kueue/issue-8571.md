# Issue #8571: Remove Pod finalizer (`kueue.x-k8s.io/managed`) cleanup processes in v0.20.0

**Summary**: Remove Pod finalizer (`kueue.x-k8s.io/managed`) cleanup processes in v0.20.0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8571

**Last updated**: 2026-04-17T11:44:07Z

---

## Metadata

- **State**: open
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2026-01-13T18:07:31Z
- **Updated**: 2026-04-17T11:44:07Z
- **Closed**: —
- **Labels**: `kind/cleanup`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
We would like to remove Pod finalizer (`kueue.x-k8s.io/managed`) cleanup mechanism in the following parts:

- https://github.com/kubernetes-sigs/kueue/blob/d57032b4987a61b06f1c90eed36de4ed2919a66a/pkg/controller/jobs/leaderworkerset/leaderworkerset_pod_reconciler.go#L86-L100
- https://github.com/kubernetes-sigs/kueue/blob/d57032b4987a61b06f1c90eed36de4ed2919a66a/pkg/controller/jobs/statefulset/statefulset_reconciler.go#L135-L139

**Why is this needed**:
Kueue no longer add finalizer to Pod after https://github.com/kubernetes-sigs/kueue/pull/8530, but we left such mechanism for better migration period.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T18:07:42Z

cc @mbobrovskyi @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T18:16:17Z

For safety we may need not be able to remove the code in 0.18 because serving workloads are expected to be long running. So, some users may expect the old LWS pods to be running for a couple of Kueue upgrades. So, I think for 0.18 we may revisit two options:
1. wait 2x more time until 0.20
2. modify the code to unconditionally remove the finalizers, and drop in 0.20

wdyt?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T18:23:20Z

> modify the code to unconditionally remove the finalizers, and drop in 0.20

I'm fine with this automated approach only if there are no disruptions when kueue removes finalizers from running Pods.

Basically, postponing deletion to v0.20 sounds better to me.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T18:35:01Z

Ok lets update the commentary in the code. I think we can just say to drop the code and refer to the issue number in the TODO, so that we dont need to synchronize the version number.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-13T18:35:02Z

Ok lets update the commentary in the code. I think we can just say to drop the code and refer to the issue number in the TODO, so that we dont need to synchronize the version number.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T13:30:43Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-17T11:03:54Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-04-17T11:44:04Z

/remove-lifecycle stale
