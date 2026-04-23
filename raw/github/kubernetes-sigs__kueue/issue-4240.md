# Issue #4240: Drop the QueueVisibility feature

**Summary**: Drop the QueueVisibility feature

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4240

**Last updated**: 2025-09-02T14:33:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-02-12T09:36:25Z
- **Updated**: 2025-09-02T14:33:16Z
- **Closed**: 2025-09-02T14:33:16Z
- **Labels**: `kind/feature`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 9

## Description

**What would you like to be added**:

Drop the code related to the deprecated feature.

The feature is deprecated already since 0.9 and I don't know about any users using it.

We don't remove the API fields yet, but we can update the user documentation that the field is no-op (no-longer supported).

**Why is this needed**:

To clean up the code, and related testing.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T09:36:43Z

cc @tenzen-y @mwielgus @mwysokin @dgrove-oss wdyt?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:22:02Z

I think after we reorganize the relationship and corresponding between classic preemption and fairSharing, we can bump API CQ version to v1beta2, then remove the QueueVisibility fields.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-12T13:45:28Z

Any reason to make this dependant on fairSharing? I think this feature is already replaced by `QueueVisibilityOnDemand`.

My idea is to drop the `QueueVisibility` feature even now (all the related code), just keep the fields for backwards compatibility of the API. Then drop the fields in `v1beta2`.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T13:48:01Z

> My idea is to drop the QueueVisibility feature even now (all the related code), just keep the fields for backwards compatibility of the API. Then drop the fields in v1beta2.

If we drop actual logic during v1beta1, could we add validations for KueueConfiguration so that users do not specify it, accidentally.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-13T14:22:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-13T14:23:03Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-08-11T15:03:47Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-11T15:05:36Z

/remove-lifecycle stale

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-08-21T11:34:02Z

/assign
