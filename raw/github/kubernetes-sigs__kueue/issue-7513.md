# Issue #7513: Provide a way to specify in the configuration what resources kueue will manage

**Summary**: Provide a way to specify in the configuration what resources kueue will manage

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7513

**Last updated**: 2026-03-19T14:39:53Z

---

## Metadata

- **State**: open
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2025-11-04T03:32:41Z
- **Updated**: 2026-03-19T14:39:53Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@MaysaMacedo](https://github.com/MaysaMacedo)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a configuration field that will be an allow list of resources that kueue can manage.

This is similar to excludeResourcePrefixes but we want something like includeResourcePrefixes.

This can be a list of allowed resources that Kueue can manage and anything else would not be counted in admission of the workload (everything else is excluded from quota counts).

**Why is this needed**:

I was discussing #5800 with @amy  and she mentioned a separate problem with the excludeResourcePrefixes.

It seems that most people are really using Kueue to manage a resources like cpu, memory and GPUs while any field that gets added to the pod spec has to keep being added to this excludeResourcePrefixes.

If someone adopts a new webhook or a controller adds a new resource to requests/limits then kueue will not allow anything to be scheduled.

So what happens is that admins keep adding fields to this list to prevent workloads from being scheduled.


**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-11-04T15:56:07Z

@kannon92 Already covered it. But in more detail... 

an example issue is:
- we get provided a k8s cluster + control plane
- the cluster operator then installs mutating webhooks to adjust pod request/limit resources across the fleet
- separately, the training platform operator then realizes every new workload submission is schedulegated bc there's a new unrecognized resource added. When the reality is, we just care about managing the quota for an explicit subset of resources

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2025-12-11T15:00:54Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:38:39Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:20Z

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

### Comment by [@MaysaMacedo](https://github.com/MaysaMacedo) — 2026-03-19T14:39:50Z

/remove-lifecycle stale
