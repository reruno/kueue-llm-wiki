# Issue #9596: Preemtion toleration support

**Summary**: Preemtion toleration support

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9596

**Last updated**: 2026-06-18T08:33:16Z

---

## Metadata

- **State**: open
- **Author**: [@lukasmrtvy](https://github.com/lukasmrtvy)
- **Created**: 2026-02-28T07:25:42Z
- **Updated**: 2026-06-18T08:33:16Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
It would be nice to have support for Preemption toleration https://scheduler-plugins.sigs.k8s.io/docs/plugins/preemptiontoleration/, as Kueue works differently from the default scheduler

**Why is this needed**:
With annotations similar to:
```
    preemption-toleration.scheduling.x-k8s.io/minimum-preemptable-priority: "10000"
    preemption-toleration.scheduling.x-k8s.io/toleration-seconds: "3600"
```
one can define the minimum run time of the workload before preemption can happen

Related https://github.com/kubernetes-sigs/kueue/issues/7990

Ref 
https://scheduler-plugins.sigs.k8s.io/docs/kep/205-preemption-toleration/readme/

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2026-03-01T18:47:34Z

I wonder if we could leverage https://github.com/kubernetes-sigs/kueue/pull/9120 instead.

Changing "boost" upon runtime seems like another good use case.

cc @mimowo @vladikkuzn

### Comment by [@mukund-wayve](https://github.com/mukund-wayve) — 2026-03-08T15:56:17Z

We would like to have something similar as well. The priority boost introduced in #9120 could help, for example by setting a high priority boost immediately after a workload starts and then reducing it after a checkpoint is made or the minimum duration is reached. However, this is hard to reason about, and the workload could still be preempted for reasons such as fair sharing. It is currently not possible to guarantee that a workload will run for at least X minutes, which would be very helpful

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-03-20T03:30:50Z

Please review https://github.com/epam/kubernetes-kueue/blob/priority-boost-controller/cmd/experimental/priority-boost-controller/README.md
I think we can continue the collaboration on https://github.com/kubernetes-sigs/kueue/pull/9959 if it suites your needs

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-06-18T04:18:32Z

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

### Comment by [@vladikkuzn](https://github.com/vladikkuzn) — 2026-06-18T08:33:16Z

@lukasmrtvy please close the issue if priority booster has suited you
