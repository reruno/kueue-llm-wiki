# Issue #7361: v1beta2: In FlavorFungibility API migrate Preempt/Borrow to MayStopSearch

**Summary**: v1beta2: In FlavorFungibility API migrate Preempt/Borrow to MayStopSearch

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7361

**Last updated**: 2025-11-05T07:28:56Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-23T11:19:15Z
- **Updated**: 2025-11-05T07:28:56Z
- **Closed**: 2025-11-05T07:28:56Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 8

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

In FlavorFungibility API, WhenCanPreempt should have options TryNextFlavor and MayStopSearch (instead of Preempt). Currently Preempt option is confusing: [#6187](https://github.com/kubernetes-sigs/kueue/issues/6187)

**Why is this needed**:

Part of the plan for https://docs.google.com/document/d/1VpSKMZP5cWXvr7NbVM2ay2HyQA6XeymwVGXxdqdhE6Q

https://github.com/kubernetes-sigs/kueue/issues/7113

## Discussion

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2025-10-27T03:16:08Z

if you can throw more details into that needs to be done here, i will like to take it

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2025-10-27T03:16:15Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T11:57:15Z

> if you can throw more details into that needs to be done here, i will like to take it

Sure, basically in v1beta2 we no longer have whenCanPreempt: Preempt, and whenCanBorrow: Borrow. Both of these options are replaced by MayStopSearch. So, the conversion v1beta1-> v1beta2 for ClusterQueue should replace Preempt with MayStopSearch and Borrow with MayStopSearch. Conversion from v1beta2 to v1beta1 can be no-op since v1beta1 already introduced MayStopSearch.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-27T11:57:30Z

cc @pajakd

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-04T09:39:41Z

@nerdeveloper let us know if this is work-in-progress, I would like this to get merged this week to leave safe buffer before the release

### Comment by [@nerdeveloper](https://github.com/nerdeveloper) — 2025-11-04T12:06:35Z

I haven’t started working on it. If it’s urgent. You can definitely take it. I plan to do it next week

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-04T12:41:10Z

/assign

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-11-04T12:41:25Z

/unassign nerdeveloper
