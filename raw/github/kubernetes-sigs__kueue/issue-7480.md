# Issue #7480: Transition QuotaReserved to false whenever setting Finished or Deactivated conditions

**Summary**: Transition QuotaReserved to false whenever setting Finished or Deactivated conditions

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7480

**Last updated**: 2026-04-15T18:38:53Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-31T11:20:13Z
- **Updated**: 2026-04-15T18:38:53Z
- **Closed**: —
- **Labels**: `priority/important-soon`, `lifecycle/stale`, `kind/cleanup`
- **Assignees**: [@amy](https://github.com/amy), [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 12

## Description


**What would you like to be cleaned**:

I would like to make sure the Workloads which release quota (Finished or Deactivated) have it reflected in the status.

**Why is this needed**:

Currently workloads which release quota still have QuotaReserved=True, I think this is confusing to users.

It would also simplify the effort around https://github.com/kubernetes-sigs/kueue/pull/6477

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-31T11:20:27Z

/cc @amy @ichekrygin @PBundyra

### Comment by [@amy](https://github.com/amy) — 2025-11-03T16:49:16Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-18T08:04:16Z

I think @mbobrovskyi can help with the first part of the task (possibly also the second):
1. transition to QuotaReserved=False for finished workloads
2. transition to QuotaReserved=False for deactived workloads

These can be separete PRs for the ease of reviewing

/assign @mbobrovskyi

### Comment by [@amy](https://github.com/amy) — 2025-11-18T22:28:11Z

Sorry! Was at kubecon last week! I would like to pick up "transition to QuotaReserved=False for deactived workloads" to finish up my existing pr (https://github.com/kubernetes-sigs/kueue/pull/7532) if that's okay with everyone. I can remove the stuff related to Finished conditions. Thank you so much for the help and guidance so far! 🙏 

cc/ @mbobrovskyi @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-19T09:25:12Z

> Was at kubecon last week!

Sure, I know this is why we decided to help in the meanwhile, so that we can try to make the new metric for 0.15. However, as we are planning 0.15 next week it is at risk, and may slit to 0.16. wdyt? 

> I would like to pick up "transition to QuotaReserved=False for deactived workloads" to finish up my existing pr (https://github.com/kubernetes-sigs/kueue/pull/7532) if that's okay with everyone. I can remove the stuff related to Finished conditions.

sgtm. I think @mbobrovskyi is facing some complications wrt SyncAdmittedCondition. So you may also wait until this is fixed.

### Comment by [@amy](https://github.com/amy) — 2025-11-19T21:47:18Z

Really appreciate the help to move this forward! And yeah slipping to 0.16 sounds alright! 

> complications wrt SyncAdmittedCondition

oh cool, will keep track of this 👀

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:39:11Z

/priority important-longterm

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-12-29T15:25:18Z

@amy, are you planning to finish this?

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T16:07:57Z

/priority important-soon
Bumping the priority as we have a user interested in that, and also for consistency with handing the Finished workloads.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-14T16:08:22Z

/remove-priority important-longterm

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-15T17:55:01Z

To do this right this is much more work than on a surface, see discussion under: https://github.com/kubernetes-sigs/kueue/issues/8596

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-15T18:38:50Z

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
