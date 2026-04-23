# Issue #5494: Address follow ups to the Kueue ownership traversal fix

**Summary**: Address follow ups to the Kueue ownership traversal fix

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5494

**Last updated**: 2026-02-22T20:45:32Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-06-04T08:15:28Z
- **Updated**: 2026-02-22T20:45:32Z
- **Closed**: —
- **Labels**: `kind/cleanup`
- **Assignees**: [@kaisoz](https://github.com/kaisoz)
- **Comments**: 13

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

Address the post-merge comments to https://github.com/kubernetes-sigs/kueue/pull/5252

**Why is this needed**:

To cleanup the code.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-04T08:15:41Z

cc @kaisoz @tenzen-y

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-06-04T08:17:47Z

/assign 

I can take this one if there's no objection :blush:

### Comment by [@kannon92](https://github.com/kannon92) — 2025-08-24T19:40:38Z

Was this completed?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T10:59:46Z

> Was this completed?

Not yet. @kaisoz What about progressing?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-08-26T12:57:03Z

Hey @tenzen-y !

Actually I have everything done in local branch. After a chat with @mimowo I was waiting for your response to this [comment](https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2135775689). And indeed I see that you just responded so I'll finish the work :D 

cc @kannon92

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-08-26T15:35:52Z

> Hey [@tenzen-y](https://github.com/tenzen-y) !
> 
> Actually I have everything done in local branch. After a chat with [@mimowo](https://github.com/mimowo) I was waiting for your response to this [comment](https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2135775689). And indeed I see that you just responded so I'll finish the work :D
> 
> cc [@kannon92](https://github.com/kannon92)

Oh, I see. Thank you!

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-07T08:09:24Z

@kaisoz is this already done or not?

IIUC this is the main pending thing: https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2092279627

### Comment by [@kaisoz](https://github.com/kaisoz) — 2025-10-08T12:57:43Z

> [@kaisoz](https://github.com/kaisoz) is this already done or not?
> 
> IIUC this is the main pending thing: [#5252 (comment)](https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2092279627)

@mimowo  The NITs were addressed in #7192 , right now only the CronJob move (see [comment](https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2092279627)) is missing

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-06T13:39:01Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-08T03:49:42Z

@kaisoz Are we able to close this issue?

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-01-22T14:42:24Z

> [@kaisoz](https://github.com/kaisoz) Are we able to close this issue?

Hi @tenzen-y ! sorry for the late reply. I think it can be closed. The only thing missing was [this comment](https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2092279627), but as @mimowo answers [here](https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2409949365), it seems that it would require a new issue on its own because of the complexity. WDYT?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-21T15:05:14Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@kaisoz](https://github.com/kaisoz) — 2026-02-22T20:45:29Z

/remove-lifecycle rotten

> > [@kaisoz](https://github.com/kaisoz) Are we able to close this issue?
> 
> Hi [@tenzen-y](https://github.com/tenzen-y) ! sorry for the late reply. I think it can be closed. The only thing missing was [this comment](https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2092279627), but as [@mimowo](https://github.com/mimowo) answers [here](https://github.com/kubernetes-sigs/kueue/pull/5252#discussion_r2409949365), it seems that it would require a new issue on its own because of the complexity. WDYT?

@tenzen-y I think we could close this issue. WDYT?
