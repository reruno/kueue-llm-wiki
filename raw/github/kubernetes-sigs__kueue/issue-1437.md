# Issue #1437: Implement cache dump via signals

**Summary**: Implement cache dump via signals

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1437

**Last updated**: 2024-01-03T18:52:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-12-11T21:39:11Z
- **Updated**: 2024-01-03T18:52:11Z
- **Closed**: 2024-01-03T18:52:10Z
- **Labels**: `kind/feature`
- **Assignees**: [@alculquicondor](https://github.com/alculquicondor)
- **Comments**: 4

## Description

**What would you like to be added**:

A cache dump that is activated through a signal, similar to kube-scheduler:

https://github.com/kubernetes/kubernetes/blob/0c645922edcc06adff43c70c02fb56751364bbb5/pkg/scheduler/internal/cache/debugger/debugger.go#L59

**Why is this needed**:

To debug complex issues

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-11T21:41:45Z

Or we could maybe use the apiserver extension?
But I'm not too eager to use this mechanism for debugging purposes, only for things that end-users might care about visualizing.

wdyt @mimowo?

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-12T11:04:41Z

> Or we could maybe use the apiserver extension?
> But I'm not too eager to use this mechanism for debugging purposes, only for things that end-users might care about visualizing.

Yes, I prefer signals, at least as the first iteration. If we add the endpoint we commit to secure and maintain the endpoint, so substantially more work.

### Comment by [@mimowo](https://github.com/mimowo) — 2023-12-13T08:52:21Z

> Yes, I prefer signals, at least as the first iteration. If we add the endpoint we commit to secure and maintain the endpoint, so substantially more work.

OTOH, the endpoint might be useful when there is no direct access to the VM running Kueue, so I don't hold a strong view.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-28T22:12:23Z

/assign @alculquicondor
