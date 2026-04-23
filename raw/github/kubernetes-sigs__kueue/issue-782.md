# Issue #782: Add additional jobframework  util functions

**Summary**: Add additional jobframework  util functions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/782

**Last updated**: 2023-06-29T12:07:39Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-05-19T08:18:55Z
- **Updated**: 2023-06-29T12:07:39Z
- **Closed**: 2023-06-29T12:07:39Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@trasc](https://github.com/trasc)
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Add a set of util functions to be used in NodeSelector/PodSetInfo operations 

See: https://github.com/kubernetes-sigs/kueue/pull/667/files#r1197979881

Add a helper function to check if a generic job is managed by kueue.

https://github.com/kubernetes-sigs/kueue/pull/667/files#r1199797983
**Why is this needed**:

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-05-22T18:03:08Z

+ https://github.com/kubernetes-sigs/kueue/pull/667#issuecomment-1556919374

### Comment by [@trasc](https://github.com/trasc) — 2023-05-25T13:26:14Z

+ Chech if  `EquivalentTo..` interface method can be dropped:  https://github.com/kubernetes-sigs/kueue/pull/763/files#r1202427399

### Comment by [@trasc](https://github.com/trasc) — 2023-05-31T08:27:16Z

/assign

### Comment by [@trasc](https://github.com/trasc) — 2023-06-09T12:00:17Z

#841 covers 
> Add a set of util functions to be used in NodeSelector/PodSetInfo operations
> See: https://github.com/kubernetes-sigs/kueue/pull/667/files#r1197979881

#842 covers
> Add a helper function to check if a generic job is managed by kueue.
however I'm not convinced that we should too involved in reconciling jobs that are managed by other jubs,  https://github.com/kubernetes-sigs/kueue/issues/800#issuecomment-1584300879

### Comment by [@trasc](https://github.com/trasc) — 2023-06-09T12:19:11Z

> Add a helper function to check if a generic job is managed by kueue.

the check is just an OR, and since `manageJobsWithoutQueueName`  is not globally available, I see very little added value in creating a function just for that OR.
