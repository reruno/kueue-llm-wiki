# Issue #7000: TrainJob integration: determine the mechanism for identifying the PodSetOverride

**Summary**: TrainJob integration: determine the mechanism for identifying the PodSetOverride

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7000

**Last updated**: 2026-04-07T21:11:45Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-09-25T08:36:04Z
- **Updated**: 2026-04-07T21:11:45Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 6

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Currently the integration relies on the  "kueue.x-k8s.io/override-idx" annotation

Alternatives to consider:
1. A dedicated "manager" field in the PodSpecOverrides, issue opened in https://github.com/kubeflow/trainer/issues/2856
2. Introspect the manager recorded by Kubertenes in the "ManagedFields" structure


**Why is this needed**:

Relying on the annotation is not ideal, because the API is hard to reason about.

A clear API field "manager" would nicely indicate. OTOH, it might be duplicating the responsibility of the ManagedFields structure, so we should also consider this as an option.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-25T08:36:46Z

cc @tenzen-y @andreyvelich @kaisoz

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-09-30T08:22:36Z

/assign

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-10-08T13:13:19Z

I checked if we can use the `ManagedFields` structure and unfortunately we can't. `ManagedFields` only shows that Kueue modified the `podSpecOverrides`, it doesn't specify what values it added:

```
- apiVersion: trainer.kubeflow.org/v1alpha1
    fieldsType: FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          f:kueue.x-k8s.io/trainjob-override-idx: {}
      f:spec:
        f:podSpecOverrides: {}
        f:suspend: {}
    manager: kueue
    operation: Update
    time: "2025-10-02T13:34:49Z"
```

I'll be following up the use a dedicated "manager" field in the `PodSpecOverrides`

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-12-28T22:49:22Z

PR in the trainer project adding the 'manager' field: https://github.com/kubeflow/trainer/pull/3020

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-28T22:53:54Z

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

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-04-07T21:11:43Z

/remove-lifecycle stale
