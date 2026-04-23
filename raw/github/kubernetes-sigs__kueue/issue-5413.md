# Issue #5413: GoDoc for reconcileCheckBasedEviction inaccurately describes return behavior

**Summary**: GoDoc for reconcileCheckBasedEviction inaccurately describes return behavior

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5413

**Last updated**: 2025-06-02T07:52:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-05-30T00:58:52Z
- **Updated**: 2025-06-02T07:52:43Z
- **Closed**: 2025-06-02T07:52:43Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@ichekrygin](https://github.com/ichekrygin)
- **Comments**: 7

## Description

The current GoDoc for [reconcileCheckBasedEviction](https://github.com/kubernetes-sigs/kueue/blob/cf39c49e72dcf190b062b459e46157ec1fe2cc33/pkg/controller/core/workload_controller.go#L410) inaccurately states:

"returns true if Workload has been deactivated or evicted"
This is misleading. The function does not return true merely because the workload is in a deactivated or evicted state—it returns true only if it actively triggers eviction or deactivation based on admission check status.

A more accurate summary would be:

"Checks whether the given Workload should be evicted or deactivated based on admission checks. Returns true if eviction or deactivation was triggered by this function."
Updating this GoDoc would better reflect the function’s logic and side effects (such as status updates, event recording, and metric reporting), and help avoid confusion for future contributors.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T05:22:20Z

cc @kaisoz would you like to grab it?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-05-30T05:41:25Z

/assign

@mimowo thanks for the ping!

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-05-30T05:43:25Z

@mimowo + @kaisoz - I finally got my GitHub sign-off straight :) - would it be ok to create a PR with this change?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-05-30T05:49:09Z

> [@mimowo](https://github.com/mimowo) + [@kaisoz](https://github.com/kaisoz) - I finally got my GitHub sign-off straight :) - would it be ok to create a PR with this change?

@ichekrygin Sure! Please assign this issue to yourself and create the PR so that we can review it 😊

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T05:50:13Z

Awesome, so I propose that you send and @kaisoz reviews. I will stamp the final review & approve.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-05-30T06:03:45Z

@mimowo, @kaisoz - it appears I can neither assign the issue to myself nor assign the reviewer to the PR :/

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T06:06:01Z

/assign ichekrygin
