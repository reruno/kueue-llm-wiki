# Issue #9021: Eliminate the global state from TrainJob reconciler

**Summary**: Eliminate the global state from TrainJob reconciler

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9021

**Last updated**: 2026-05-19T07:01:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-06T08:40:24Z
- **Updated**: 2026-05-19T07:01:07Z
- **Closed**: 2026-05-19T07:01:07Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

I would like to eliminate the global state from the TrainJob reconciler https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobs/trainjob/trainjob_controller.go#L87

**Why is this needed**:

This is causing non-obvious problems in the MultiKueue integration tests, as we encountered in the PR: https://github.com/kubernetes-sigs/kueue/pull/8341/changes#r2766310790

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-06T08:42:29Z

cc @kaisoz @sohankunkerkar @hiboyang

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-02-12T11:19:13Z

This global state was a way to bypass a bug in one of the Trainer helper functions

In order to build the Trainer info object [here](https://github.com/kubernetes-sigs/kueue/blob/20bc130fc47d85ce8eea5e7b4dd943935aad52df/pkg/controller/jobs/trainjob/trainjob_controller.go#L177) We need to get all the available runtimes. The initial idea was to get them on demand, but that's not possible because the [Trainer runtime helper function](https://github.com/kubeflow/trainer/blob/72474fb6d8e29ddb8005efd50e9fd1c955723778/pkg/runtime/core/core.go#L31) that returns the runtimes has a bug:

1. The function first creates a [runtime registry](https://github.com/kubeflow/trainer/blob/72474fb6d8e29ddb8005efd50e9fd1c955723778/pkg/runtime/core/core.go#L32) which contains the available runtimes and its factory methods ([here's the definition](https://github.com/kubeflow/trainer/blob/ca9abf57425f87e2870abbd72c3c0f1bf4711672/pkg/runtime/core/registry.go#L33))
2. Then for each available runtime [calls the corresponding factory method](https://github.com/kubeflow/trainer/blob/72474fb6d8e29ddb8005efd50e9fd1c955723778/pkg/runtime/core/core.go#L39) (the one for the ClusterTrainingRuntime just calls the TrainingRuntime one)
3. Which ends up indexing the field in the indexer ([here](https://github.com/kubeflow/trainer/blob/ca9abf57425f87e2870abbd72c3c0f1bf4711672/pkg/runtime/core/trainingruntime.go#L66))

and you can only register the same index key for the same object type, so the second call would fail. This is the reason why I initialise it once in the reconciler and reuse it. 

I remember having a conversation about this with the maintainers, they said that there was a fix on the way but I can see the code is still there. Let me look for a bug issue and if not I'll create it

### Comment by [@mimowo](https://github.com/mimowo) — 2026-02-12T11:22:36Z

> I remember having a conversation about this with the maintainers, they said that there was a fix on the way but I can see the code is still there. Let me look for a bug issue and if not I'll create it

Thank you for driving that 👍

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-02-16T22:48:45Z

/assign

since I'm on top of this

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-05-17T23:27:59Z

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

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-05-18T14:57:37Z

/remove-lifecycle stale

will have a PR shortly 👍🏻
