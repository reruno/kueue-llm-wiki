# Issue #922: Extend the unit-test coverage for jobframework,

**Summary**: Extend the unit-test coverage for jobframework,

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/922

**Last updated**: 2023-07-27T15:48:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2023-06-29T08:55:32Z
- **Updated**: 2023-07-27T15:48:11Z
- **Closed**: 2023-07-27T15:48:11Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 4

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
Extend the unit-test coverage for jobframework,
ref: https://github.com/kubernetes-sigs/kueue/pull/762/files#r1245444318
**Why is this needed**:

## Discussion

### Comment by [@stuton](https://github.com/stuton) — 2023-06-29T11:04:36Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-29T12:00:26Z

There are two alternatives:
- Create a FakeJob implementation to test the jobframework package itself.
- Test each of the job packages (job, mpijob, jobset) using a fake client and the reconciler code.

I have a preference for the second.

### Comment by [@trasc](https://github.com/trasc) — 2023-06-30T13:40:51Z





> There are two alternatives:
> 
> * Create a FakeJob implementation to test the jobframework package itself.
> * Test each of the job packages (job, mpijob, jobset) using a fake client and the reconciler code.
> 
> I have a preference for the second.

going with the second one we will have a lot of duplicate tests.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-06-30T14:14:33Z

It's not really duplicate, as some jobs might behave differently and implement optional extensions.
