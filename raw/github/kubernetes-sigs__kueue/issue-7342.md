# Issue #7342: v1beta2: change the API for Workload's spec.priorityClassSource

**Summary**: v1beta2: change the API for Workload's spec.priorityClassSource

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7342

**Last updated**: 2025-11-07T12:22:54Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-22T14:33:10Z
- **Updated**: 2025-11-07T12:22:54Z
- **Closed**: 2025-11-07T12:22:54Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Two possibilities are disucssed:
1. `priorityClassSource` field as *string.
2. `priorityClassRef`


**Why is this needed**:

Part of https://github.com/kubernetes-sigs/kueue/issues/7113

The field is causing troubles when conversion webhooks are enabled: https://github.com/kubernetes-sigs/kueue/pull/7318#discussion_r2450893646

Also, ptr (optional) would better reflect the intention since the field may not necessarily be specified.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T12:24:28Z

/retitle v1beta2: change the API for Workload's spec.priorityClassSource

The priorityClassSource is located in spec.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T12:27:33Z

Let me expand (2) here a bit more
The original motivation is to align with the Kubernetes API recommendation: https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md#multiple-resource-reference

We can consider the following new structure:

```yaml
spec:
  priority: 123456
  priorityClassRef:
    group: kueue.x-k8s.io | scheduling.k8s.io
    kind: PriorityClass | WorkloadPriorityClass
    name: high
```

If we select the above objectRef pattern, we will remove `.spec.priorityClassName` since the name will be included in the `.spec.priorityClassRef.name`.

Initially posted in https://github.com/kubernetes-sigs/kueue/pull/7318#issuecomment-3432748098

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-23T12:36:01Z

+1, the only consideration I think is that when we convert in webhooks from v1beta1, then we will not be able to populate `priorityClassRef.name` directly based on the old object. 

Some options I can see:
1. keep the `name ` as ptr for this reason
2. don't use ptr, but just add comment / docs disclaimer that for workloads created in v1beta1 it may be empty string "" (which may not be accurate)
3. lookup the priority class name

I think we can safely exclude (3.). I think (2.) makes sense actually because this is a problem only in transition period.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-23T12:47:28Z

> I think we can safely exclude (3.). I think (2.) makes sense actually because this is a problem only in transition period.

LGTM for opt (2).

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-05T08:06:40Z

/assign
