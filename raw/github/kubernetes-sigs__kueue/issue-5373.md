# Issue #5373: Consolidate unit tests for TestFindTopologyAssignment

**Summary**: Consolidate unit tests for TestFindTopologyAssignment

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5373

**Last updated**: 2025-08-05T14:19:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-27T09:42:15Z
- **Updated**: 2025-08-05T14:19:41Z
- **Closed**: 2025-08-05T14:19:41Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 12

## Description

**What would you like to be cleaned**:

Currently we have two tests TestFindTopologyAssignmentForTwoPodSets and TestFindTopologyAssignment.

I like to consolidate into one which allows to write test cases for an arbitrary number of PodSets.

**Why is this needed**:

To make it clear where to add new tests of similar nature, and don't require yet another test if we need to support 3 podsets.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T09:43:12Z

it is a follow up to the comment https://github.com/kubernetes-sigs/kueue/pull/5325#discussion_r2104686113

cc @lchrzaszcz @mbobrovskyi @kaisoz

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-27T09:43:40Z

cc @PBundyra

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-05-27T09:48:09Z

/assign

I can take care of this one if that's ok for you guys :blush:

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-28T12:47:13Z

I agree with @mimowo 
The following is what I expect:

1. Consolidate `TestFindTopologyAssignmentForTwoPodSets` (*1 to `TestFindTopologyAssignment`
2. Remove builders (*2

*1) https://github.com/kubernetes-sigs/kueue/blob/23700491fa890b769a96ab5d056728fd1b5e799b/pkg/cache/tas_cache_test.go#L2132
*2) https://github.com/kubernetes-sigs/kueue/blob/23700491fa890b769a96ab5d056728fd1b5e799b/pkg/cache/tas_cache_test.go#L2225-L2273

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-06-16T11:53:48Z

Hi @kaisoz 👋 What is the status of this issue? I would like to add another test that contains 2 PodSets. I could work around it or fix it myself, but I do not want to conflict with your work.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T07:29:45Z

@kaisoz Kindly ping, again. What is this your work status?
I would like to resolve this issue soon.

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-06-20T07:45:27Z

@lchrzaszcz @tenzen-y Apologies to both of you for this late reply, I've been busy lately (family issues) and couldn't pay attention to GH...

With regards to the issue, I've started with it but I don't want to be a blocker so please @lchrzaszcz feel free to take over if you need to, since I have low bandwidth atm

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T07:50:38Z

> [@lchrzaszcz](https://github.com/lchrzaszcz) [@tenzen-y](https://github.com/tenzen-y) Apologies to both of you for this late reply, I've been busy lately (family issues) and couldn't pay attention to GH...
> 
> With regards to the issue, I've started with it but I don't want to be a blocker so please [@lchrzaszcz](https://github.com/lchrzaszcz) feel free to take over if you need to, since I have low bandwidth atm

Thank you for letting us know! @lchrzaszcz Could you take this issue?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-06-20T09:07:04Z

/unassign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-20T12:59:12Z

/assign @lchrzaszcz

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2025-07-10T12:53:13Z

/assign

### Comment by [@lchrzaszcz](https://github.com/lchrzaszcz) — 2025-07-11T07:32:27Z

/unassign
