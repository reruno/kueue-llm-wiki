# Issue #8434: Waiting queue lock issue

**Summary**: Waiting queue lock issue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8434

**Last updated**: 2026-02-13T01:40:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@flysee100](https://github.com/flysee100)
- **Created**: 2026-01-01T04:31:18Z
- **Updated**: 2026-02-13T01:40:01Z
- **Closed**: 2026-02-13T01:40:01Z
- **Labels**: `kind/bug`, `priority/important-longterm`
- **Assignees**: [@yashnib](https://github.com/yashnib)
- **Comments**: 4

## Description

May I ask…
In the sigs.k8s.io/kueue/pkg/cache/queue package, the CleanUpOnContext function does not acquire a lock on the broadcast when it is called, which may lead to conflicts.
If the waiting queue has not yet entered wait, then the Broadcast signal will be lost, causing it to remain stuck in wait.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-07T10:26:31Z

I think you are right. Would you like to submit a PR?

/kind bug

Still, it seems not urgent as it would only affect Kueue which is already stopping anyway, and the new replica should take over the work.
/priority important-longterm

### Comment by [@yashnib](https://github.com/yashnib) — 2026-01-12T21:46:40Z

I’d like to take this issue. I think that there’s a lost-broadcast race in Heads() due to the select { default: m.cond.Wait() } pattern: the context can be canceled after the default branch is chosen but before Wait() begins, so CleanUpOnContext()’s broadcast can be missed and Heads() may block indefinitely.

Plan: update Heads() to check ctx.Err() under the mutex before waiting (no select/default), and update CleanUpOnContext() to acquire m.Lock() before broadcasting (without changing Manager.Broadcast() to avoid deadlocks since many callers already hold the lock). I’ll also add a regression test that would previously hang and now returns when the context is canceled. 

Does that sound OK, or is there a preferred approach/test pattern you’d like me to follow?

### Comment by [@flysee100](https://github.com/flysee100) — 2026-01-16T11:40:29Z

I think this approach makes sense. Since this lock affects core functionality, I suggest running more tests.

### Comment by [@yashnib](https://github.com/yashnib) — 2026-02-12T03:42:47Z

/assign
