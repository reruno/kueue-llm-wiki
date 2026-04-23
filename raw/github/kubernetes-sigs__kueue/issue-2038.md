# Issue #2038: Fix transitions of Requeued condition

**Summary**: Fix transitions of Requeued condition

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2038

**Last updated**: 2024-05-03T19:04:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-04-23T06:40:20Z
- **Updated**: 2024-05-03T19:04:10Z
- **Closed**: 2024-05-03T19:04:09Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 3

## Description

The `Requeued` condition should transition to `False` in the following scenarios:

- When workload.spec.active=false. It should return to True when it's reactivated.
- When evicted due to WaitForPodsReady, the workload will temporarily be in backoff. During this time, Requeued should be false.

As per [comment](https://github.com/kubernetes-sigs/kueue/pull/1977#discussion_r1574949456).

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-04-23T07:11:02Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-23T13:26:53Z

Also, once the transitions are fixed, we can use the timestamp of the `Requeued` condition for scheduling sorting.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-23T14:05:53Z

One thing to keep in mind regarding the transition after backoff:
Currently, the backoff is acted on in the event handlers. This is fine, as it's a quick in-memory operation.
OTOH, doing an API update within an event handler is not acceptable. So the update needs to happen somewhere inside the `Reconcile` method.

If you wanna bounce some ideas of how to get that implemented, feel free to reach out to me or @mimowo over slack.
