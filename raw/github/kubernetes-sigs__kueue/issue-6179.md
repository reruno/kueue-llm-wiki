# Issue #6179: MK Dispatcher: Extract Incremental mode to a separate controller

**Summary**: MK Dispatcher: Extract Incremental mode to a separate controller

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6179

**Last updated**: 2025-09-12T10:22:05Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mszadkow](https://github.com/mszadkow)
- **Created**: 2025-07-25T08:00:08Z
- **Updated**: 2025-09-12T10:22:05Z
- **Closed**: 2025-09-12T02:36:09Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 9

## Description

**What would you like to be added**:
Based on the [comment](https://github.com/kubernetes-sigs/kueue/pull/5782#discussion_r2201609035)
We would like to continue  to work on the MK Dispatcher and move Incremental mode implementation into separate controller.

**Why is this needed**:
The reference implementation would be proving that:
A. an external dispatcher can be written,
B. serving an example of how to write one
**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T12:13:12Z

Let me break it down into two separate issues:
- Move the incremental to a separate controller, but inside Kueue
- Create a separate blueprint project outside of Kueue binary implementing the dispatcher. For example adding clusters one-by-one

Let me retitle then
/retitle MK Dispatcher: Extract Incremental mode to a separate controller

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-29T12:16:26Z

Split out the second point as: https://github.com/kubernetes-sigs/kueue/issues/6238

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-08-01T13:48:37Z

/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-01T17:54:28Z

Can we move the AllAtOnce dispatcher to a separate controller as well?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-02T05:57:13Z

> Can we move the AllAtOnce dispatcher to a separate controller as well?

I don't see a blocker, might be a good idea to decompose the code more.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-12T02:45:25Z

> > Can we move the AllAtOnce dispatcher to a separate controller as well?
> 
> I don't see a blocker, might be a good idea to decompose the code more.

I would still like to decouple the AllAtOnce dispatcher from AC MultiKueue Workload controller to a dedicated reconciler within the kueue-controller-manager the same as incremental dispatcher.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T06:11:33Z

sgtm, would you like to open a follow up issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-12T09:42:18Z

Actually, I just opened: https://github.com/kubernetes-sigs/kueue/issues/6803

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-09-12T10:22:04Z

> Actually, I just opened: [#6803](https://github.com/kubernetes-sigs/kueue/issues/6803)

Thank you!
