# Issue #1150: [RayJob] Update the workload status when suspended

**Summary**: [RayJob] Update the workload status when suspended

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1150

**Last updated**: 2023-10-09T10:27:57Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-09-22T03:51:47Z
- **Updated**: 2023-10-09T10:27:57Z
- **Closed**: 2023-10-09T10:27:57Z
- **Labels**: `kind/bug`
- **Assignees**: _none_
- **Comments**: 2

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

When job(rayjob specifically) is suspended transferred from running, the workload status return from `kubectl get workload -o wide` still marked as `Admitted`, see

```
NAME                      QUEUE     ADMITTED BY       AGE
rayjob-rayjob-low-fb3cd   queue-1   cluster-queue-1   29m
```

Should we update the status synchronously?

**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-09-22T07:22:10Z

I guess this is a bug because batch job is worked as expected.
/remove-kind feature
/kind bug

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-09-22T09:03:39Z

This is somehow related to https://github.com/kubernetes-sigs/kueue/issues/1146
