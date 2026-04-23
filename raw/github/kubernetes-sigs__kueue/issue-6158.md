# Issue #6158: Replace using SSA with Patch for all Workload requests

**Summary**: Replace using SSA with Patch for all Workload requests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6158

**Last updated**: 2025-10-02T08:50:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-24T07:51:11Z
- **Updated**: 2025-10-02T08:50:57Z
- **Closed**: 2025-10-02T08:50:57Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Replace SSA with Patch for all modifications on the Workload objects.

**Why is this needed**:

1. It causes this bug: https://github.com/kubernetes-sigs/kueue/issues/3540 (the upstream [issue](https://github.com/kubernetes/kubernetes/issues/113482) is unsolved for 3 years and unlikely to be solved any time soon)
2. It makes some features harder than expected, for example MultiKueue clearing of nominatedClusterNames field. This field is expected to be set by external controller, and so Kueue cannot clear it on eviction, or when setting clusterName using SSA. Ticketed under: https://github.com/kubernetes-sigs/kueue/issues/6185

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-24T07:54:58Z

cc @tenzen-y wdyt? Maybe it would even be an option for 0.13, maybe behind a feature gate?

Patch is a very stable k8s mechanism, so I don't expect issues. We just need to make sure to pass the fieldManager, but it is possible. For admission we also currently use strict=true, so I don't think it will matter for performance or correctness.

@mbobrovskyi @mszadkow

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-07-29T08:41:19Z

/assign @mszadkow

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T12:11:58Z

> Patch is a very stable k8s mechanism, so I don't expect issues. We just need to make sure to pass the fieldManager, but it is possible. For admission we also currently use strict=true, so I don't think it will matter for performance or correctness.

Thank you for moving this forward > @mimowo @mbobrovskyi @mszadkow 
I'm ok with introducing the switch for PATCH operation.

But, recently, k/k tries to improve SSA mechanism. So, if the operation seems to improve and resolve our problems, let's revisit the SSA status updates. I guess that the core problem is that we don't use ApplyConfiguration, then use the typed Object.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-23T12:20:19Z

> But, recently, k/k tries to improve SSA mechanism. 

Do you have some issue tracking the effort? This upstream [issue](https://github.com/kubernetes/kubernetes/issues/113482) was open in 2022 and has not comments for a year, but maybe there is another issue tracking the recent efforts.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-23T12:25:16Z

> > But, recently, k/k tries to improve SSA mechanism.
> 
> Do you have some issue tracking the effort? This upstream [issue](https://github.com/kubernetes/kubernetes/issues/113482) was open in 2022 and has not comments for a year, but maybe there is another issue tracking the recent efforts.

I didn't point the specific one. For example, k/k introduced the interface for ApplyConfiguration in v1.34 so that the external library (e.g., controller-runtime) can correctly handle Apply operation.
So, I am expecting that the improvement will come in steps.
