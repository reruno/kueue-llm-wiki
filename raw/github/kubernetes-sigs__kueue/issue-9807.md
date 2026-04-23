# Issue #9807: Requeue disable on preemption

**Summary**: Requeue disable on preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9807

**Last updated**: 2026-03-24T13:11:48Z

---

## Metadata

- **State**: open
- **Author**: [@noammualmiw](https://github.com/noammualmiw)
- **Created**: 2026-03-11T15:30:09Z
- **Updated**: 2026-03-24T13:11:48Z
- **Closed**: —
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 2

## Description

Hello all,

We want to start using Kueue for our production servers.
I want to be able to stop Re-Queue when preemption happens.
I saw the [WaitForPodsReady] but it seems weird solution for me.
Case:  
1. Low priority job start.
2. High priority job start
3. High preempt low (duo to low resources)
4. Low Re-queue again - i want to be able to control this part and to have strategy (per cluster/queue is preferred).

In the end i have many cases that i don't want the job to start again at all. (Like github workflows), etc.
Please help, it's important for us.

Regards, :)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-11T16:00:10Z

Hi @noammualmiw, indeed currently here is no such native mechanism in Kueue. What is your usecase to stop re-queing and thus re-admitting low priority Jobs?

One mechanism you can get close to is workload deactivation - write a small external controller which would deactivate any preempted workload.

### Comment by [@noammualmiw](https://github.com/noammualmiw) — 2026-03-24T13:06:53Z

We using Kueue for AI reference and GitHub runners.
Most of the item if a runner got evicted by high priority we won't need it to be Requeued, only run it separately from GitHub again (i fear it will cause integration issues).
Also another use-case is Kubevirt VM's (using pods resources Kueue) ,  we won't need it readmitted after preemption.
