# Issue #7394: v1beta2: introduce unit tests for the conversions

**Summary**: v1beta2: introduce unit tests for the conversions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7394

**Last updated**: 2025-11-06T17:29:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-27T09:02:51Z
- **Updated**: 2025-11-06T17:29:03Z
- **Closed**: 2025-11-06T17:29:03Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Add unit tests for localqueue_conversion.go, clusterqueue_conversion.go and workload_conversion.go

**Why is this needed**:

To make sure the logic is solid, and prevent bugs like for example https://github.com/kubernetes-sigs/kueue/pull/7369#discussion_r2464736602

## Discussion

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2025-10-28T10:07:19Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T16:02:11Z

@bobsongplus any progress here?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T16:04:41Z

/unassign bobsongplus 
because this is getting important for https://github.com/kubernetes-sigs/kueue/pull/7544/

if you have some progress made please continue and let's merge it with the other testing efforts.

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2025-11-05T19:13:21Z

/assign sohankunkerkar

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-05T19:41:23Z

Let's focus on a basic unit test for workload first. 

We can add the unit tests for LQ and CQ in separate PRs.
