# Issue #6992: Introduce Retry mechanism to PATCH client

**Summary**: Introduce Retry mechanism to PATCH client

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6992

**Last updated**: 2025-11-26T12:00:37Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@tenzen-y](https://github.com/tenzen-y)
- **Created**: 2025-09-24T13:08:22Z
- **Updated**: 2025-11-26T12:00:37Z
- **Closed**: 2025-11-26T12:00:37Z
- **Labels**: `kind/feature`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to introduce Retry mechanism to utilclient library: https://github.com/kubernetes-sigs/kueue/blob/77590bb5af3817b86b108b46ff26773c834efe44/pkg/util/client/client.go

The retry mechanism is similar to client-go library: https://github.com/kubernetes/client-go/blob/master/util/retry/util.go

**Why is this needed**:

As we discussed in https://github.com/kubernetes-sigs/kueue/pull/6962#discussion_r2372503647, we are trying to replace Apply operation with Patch operation which will introduce many CONFLICT error when Kueue updates resources, and fail to update Admission and Preemption.

It is significant problems for our ATOMIC operation.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-24T13:08:42Z

cc @mimowo @mbobrovskyi @mszadkow @mwysokin

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-25T02:52:48Z

cc @ichekrygin

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-09-25T07:12:08Z

/assign
