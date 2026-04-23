# Issue #7301: Higher-priority workloads are blocked while a “sticky” low-priority workload is pinned to the head of the queue

**Summary**: Higher-priority workloads are blocked while a “sticky” low-priority workload is pinned to the head of the queue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7301

**Last updated**: 2026-03-16T16:58:45Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@ichekrygin](https://github.com/ichekrygin)
- **Created**: 2025-10-17T04:51:31Z
- **Updated**: 2026-03-16T16:58:45Z
- **Closed**: 2026-03-16T16:58:44Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 13

## Description

**Related issues and PRs:**

* Root cause discussion: [#6929](https://github.com/kubernetes-sigs/kueue/issues/6929)
* Sticky workload introduction: [#7157](https://github.com/kubernetes-sigs/kueue/pull/7157)

### Summary

After the “sticky pending workload” fix introduced in [#7157](https://github.com/kubernetes-sigs/kueue/pull/7157), higher-priority workloads may become blocked behind a lower-priority workload that is pinned to the head of the queue.

The intent of the sticky behavior was to prevent starvation by keeping the workload that initiated preemption at the queue head until its preemption sequence completes. However, this also prevents newly added, higher-priority workloads from being scheduled while the sticky workload is still waiting for preemption to finish.

### Setup

The setup is similar to [#6929](https://github.com/kubernetes-sigs/kueue/issues/6929).

**ClusterQueues:**

* `cq1`:

    * nominal CPU = 3
    * borrowingLimit = 0
    * preemption:

      ```yaml
      preemption:
        reclaimWithinCohort: Any
        withinClusterQueue: LowerPriority
      ```
* `cq2`: nominal CPU = 0, borrowingLimit = 3

**LocalQueues:**

* `lq1` and `lq2`, corresponding to `cq1` and `cq2`

**PriorityClasses:**

* `high` = 10000
* `low` = 1000

**Jobs:**

| Job | CPU | Priority  | ClusterQueue |
| --- | --- | --------- | ------------ |
| j01 | 2   | (default) | cq2          |
| j02 | 4   | low       | cq1          |
| j03 | 2   | low       | cq1         |
| j04 | 2   | high      | cq1          |

---

### Repro Steps

1. Submit `j01` → **admitted**
2. Submit `j02` → **pending** (exceeds available CPU)
3. Submit `j03`, then `j04` in order

**Observed behavior:**

* `j03` enters scheduling cycle first and triggers preemption of `j01`
* Due to sticky logic, `j03` is pinned at the head of the queue until preemption completes
* Meanwhile, `j04` (higher priority) cannot proceed
* After several scheduling cycles `j03` is eventually admitted
* When `j04` runs next, it preempts `j03`

### Expected behavior

When a higher-priority workload (`j04`) enters the queue, it should preempt or take precedence over lower-priority workloads, even if one of them is currently “sticky.” The sticky behavior should not override priority-based scheduling order.

### Impact

This can lead to:

* Unintended scheduling delays for higher-priority workloads
* Inversion of expected priority ordering
* Reduced responsiveness of the scheduler under preemption-heavy workloads
* **Unordered scheduling may result in preemption churn**, as illustrated in the example where `j03` blocks `j04`, with eventual `j04` preemption of `j03`

## Discussion

### Comment by [@amy](https://github.com/amy) — 2025-10-17T15:19:53Z

cc/ @mimowo @gabesaba @mwysokin

### Comment by [@amy](https://github.com/amy) — 2025-10-17T15:36:19Z

@ichekrygin Mainly concerned about this part: "Unordered scheduling may result in preemption churn, as illustrated in the example where j03 blocks j04, with eventual j04 preemption of j03"

To clarify, do you see rapid preemption churn in your repro? 🙏 thank you for further validating the original fix.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-17T15:48:51Z

> To clarify, do you see rapid preemption churn in your repro? 🙏 Thank you for further validating the original fix.

The key point here is that if the scheduler correctly respects priority order, then `j04` should precede `j03` and therefore should not require an additional preemption in this specific example.

It’s important to recognize that if our choices are limited to either:
a. a “head-of-the-queue” blocker, or
b. suboptimal scheduling as a result of “sticky” workloads,
I would take **(b)** over **(a)** any time.

That said, I think we should explore potential scheduling and queuing designs that avoid being constrained to these two options altogether.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T15:50:17Z

Thank you for reporting, I believe there is indeed  some potential for improvement, but I think it requires more careful investigation, so that we do not to re-introduce the bugs fixed by the "sticky" head approach. 

If I remember correctly the main issue with considering other workloads during preemption is that it may lead to re-admitting the just preempted workloads, because they can be winning in terms of DRS with the "new head" even though they were losing in terms of DRS with the previous head. This scenario of losing DRS to one "head" workload, but winning DRS to another "head" workload was the root cause for infinite preemption loops.

I assume this follow up issue is less severe than the original ones, but let me know if you think the situation is worsened on your setup?

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-17T15:53:27Z

> I assume this follow up issue is less severe than the original ones, 

💯 correct (IMHO).

Update: less severe

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T15:53:29Z

cc @mwysokin who may also help to prioritize

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-17T15:54:18Z

Sorry, correct that it is worse or correct that less severe?

EDIT: ah, ok I see update that it is "less severe" . This is great, but we should still think how to coverage on something better.

### Comment by [@amy](https://github.com/amy) — 2025-10-17T16:11:44Z

> The key point here is that if the scheduler correctly respects priority order, then j04 should precede j03 and therefore should not require an additional preemption in this specific example.

To clarify, you notice this resulting in what looks like 1 extra preemption. But does not result in: `infinite preemption loops`.

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-10-17T16:25:47Z

> To clarify, you notice this resulting in what looks like 1 extra preemption. But does not result in: infinite preemption loops.

That is correct.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-15T16:26:49Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-02-14T16:41:07Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-16T16:58:37Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-16T16:58:45Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7301#issuecomment-4069175987):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
