# Issue #4151: Replace pkg/util/maps and pkg/util/slices with standard maps and slices libs

**Summary**: Replace pkg/util/maps and pkg/util/slices with standard maps and slices libs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4151

**Last updated**: 2025-02-11T10:34:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-02-05T13:04:43Z
- **Updated**: 2025-02-11T10:34:03Z
- **Closed**: 2025-02-11T10:34:03Z
- **Labels**: `good first issue`, `help wanted`, `kind/cleanup`
- **Assignees**: [@adarshagrawal38](https://github.com/adarshagrawal38)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
We would like to replace Kueue [`utilmaps`](https://github.com/kubernetes-sigs/kueue/tree/9faabed5096f8b754373971bfffa343e3ba14d9f/pkg/util/maps) and [`utilslices`](https://github.com/kubernetes-sigs/kueue/tree/9faabed5096f8b754373971bfffa343e3ba14d9f/pkg/util/slices) with Go standard maps and slices libraries as much as possible.

The biggest obstacle is the iterator. Some Go standard `maps` and `slices` libs depend on the `iter.Seq[E]` or `iter.Seq2[E]`.
So, when we introduce some standard libs, we need to adapt our related codes to Go Iterator.

**Why is this needed**:

Standard libraries allow us to reduce the maintenance costs.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-02-06T01:31:54Z

/help
/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-02-06T01:31:57Z

@kannon92: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4151):

>/help
>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@adarshagrawal38](https://github.com/adarshagrawal38) — 2025-02-06T07:03:00Z

/assign

### Comment by [@adarshagrawal38](https://github.com/adarshagrawal38) — 2025-02-07T05:24:02Z

Hi @tenzen-y @kannon92 @mbobrovskyi 

Based on my understanding, I need to replace utilmaps.NewSyncMap() with a standard Go map, like:
map[string]*kueue.Workload{}

at this location: https://github.com/kubernetes-sigs/kueue/blob/9faabed5096f8b754373971bfffa343e3ba14d9f/pkg/controller/admissionchecks/multikueue/workload.go#L477

Am I heading in the right direction?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-07T11:32:14Z

> Hi [@tenzen-y](https://github.com/tenzen-y) [@kannon92](https://github.com/kannon92) [@mbobrovskyi](https://github.com/mbobrovskyi)
> 
> Based on my understanding, I need to replace utilmaps.NewSyncMap() with a standard Go map, like: map[string]*kueue.Workload{}
> 
> at this location:
> 
> [kueue/pkg/controller/admissionchecks/multikueue/workload.go](https://github.com/kubernetes-sigs/kueue/blob/9faabed5096f8b754373971bfffa343e3ba14d9f/pkg/controller/admissionchecks/multikueue/workload.go#L477)
> 
> Line 477 in [9faabed](/kubernetes-sigs/kueue/commit/9faabed5096f8b754373971bfffa343e3ba14d9f)
> 
>  deletedWlCache:    utilmaps.NewSyncMap[string, *kueue.Workload](0), 
> Am I heading in the right direction?

I meant that wondering if we can directly convert our function to standard lib.
For example, we have [`Keys`](https://github.com/kubernetes-sigs/kueue/blob/9faabed5096f8b754373971bfffa343e3ba14d9f/pkg/util/maps/maps.go#L73), but standard lib provides [`Keys`](https://pkg.go.dev/maps#Keys) as well.

So, I never want to mention replacing `utilmaps.NewSyncMap` with Go map.
