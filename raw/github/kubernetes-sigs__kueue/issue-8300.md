# Issue #8300: WaitForPodsReady: use timeout as the fallback when recoveryTimeout is not specified

**Summary**: WaitForPodsReady: use timeout as the fallback when recoveryTimeout is not specified

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/8300

**Last updated**: 2026-01-19T17:25:49Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-12-17T13:02:17Z
- **Updated**: 2026-01-19T17:25:49Z
- **Closed**: 2026-01-19T17:25:49Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 11

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would prefer if we use the `waitForPodsReady.timeout` as the fallback if `waitForPodsReady.recoveryTimeout` is not specified.

It is not a top priority issue, but it seems natural to me to assume `waitForPodsReady.recoveryTimeout <= waitForPodsReady.timeout`

**Why is this needed**:

Sometimes users may forget setting `waitForPodsReady.recoveryTimeout`, and then the Jobs are kept for very long in the broken state (jobs which already passed startup timeout.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-17T13:03:32Z

We have missed this as a potential change in v1beta2, but maybe we could still handle that as an omission and do in 0.16. I think the main question if we think this is the right thing to have.

cc @tenzen-y @PBundyra @kannon92 any opinions?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T08:31:35Z

/priority important-longterm

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-09T09:02:15Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T13:19:37Z

I opened the issue because I think it makes sense, but it is not top priority. I think we need start with KEP update(might be the same PR). wdyt @tenzen-y about this idea?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T14:30:45Z

> I opened the issue because I think it makes sense, but it is not top priority. I think we need start with KEP update(might be the same PR). wdyt [@tenzen-y](https://github.com/tenzen-y) about this idea?

SGTM. One thing is how to make a room to disable recoveryTimeout.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-09T14:33:21Z

Yeah, if we go with that proposal we assume there is no way to disable it other than setting a very high value. 

I'm not sure this is a problem though. More issues is probably if someone forgets to set it.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T14:41:23Z

> Yeah, if we go with that proposal we assume there is no way to disable it other than setting a very high value.
> 
> I'm not sure this is a problem though. More issues is probably if someone forgets to set it.

When they want to operate a strict policy, I guess they want to disable recoveryTimeout. The admins enforces evictions on crashing workloads w/ any reason.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-09T14:42:58Z

I didn't say that recoveryTimeout shouldn't be specified by default. The default recoveryTimeout is helpful, but it would be better to leave the opportunity to disable that.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2026-01-12T09:25:21Z

Would setting the timeout to `0` be a valid way to disable `recoveryTimeout`? If so, the behavior would be:

1. When `recoveryTimeout1` is not specified, it defaults to the value of timeout.
2. Setting `recoveryTimeou: 0s` explicitly disables recovery timeout checking.

WDYT?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-12T11:00:02Z

sgtm, wdyt @tenzen-y ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-01-13T16:48:54Z

> Would setting the timeout to `0` be a valid way to disable `recoveryTimeout`? If so, the behavior would be:
> 
> 1. When `recoveryTimeout1` is not specified, it defaults to the value of timeout.
> 2. Setting `recoveryTimeou: 0s` explicitly disables recovery timeout checking.
> 
> WDYT?

That sounds great to me, thank you 👍
