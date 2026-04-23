# Issue #2359: [multikueue] Add a no GC integration tests suite.

**Summary**: [multikueue] Add a no GC integration tests suite.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2359

**Last updated**: 2024-06-12T05:05:08Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@trasc](https://github.com/trasc)
- **Created**: 2024-06-05T09:33:05Z
- **Updated**: 2024-06-12T05:05:08Z
- **Closed**: 2024-06-12T05:05:08Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow), [@trasc](https://github.com/trasc)
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Add a multikueue integration tests suite in which the garbage collector is not running.

**Why is this needed**:

Ideally

https://github.com/kubernetes-sigs/kueue/blob/cd6dc529074256408f0f04ad4a9ebd5d4d24db59/test/integration/multikueue/multikueue_test.go#L653-L708

should verify the synchronous remote object removal functionality, however since the GC is also running it is not guaranteed that the remote objects are removed synchronously and not by GC.

**Completion requirements**:

`ginkgo.It("Should remove the worker's workload and job when managers job is deleted"`...` performs the same way in a no GC environment.

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2024-06-05T09:33:14Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-06-05T13:13:34Z

/assign
