# Issue #1149: Reclaim consumed resources once quit from cohort

**Summary**: Reclaim consumed resources once quit from cohort

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1149

**Last updated**: 2024-04-18T09:11:16Z

---

## Metadata

- **State**: open
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2023-09-22T03:38:08Z
- **Updated**: 2024-04-18T09:11:16Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

![image](https://github.com/kubernetes-sigs/kueue/assets/18364341/b87c4ded-73c5-480e-8541-ca0837546467)

When clusterQueue quits from the cohort, the resources consumed will not be reclaimed.

1. rayjob-high and rayjob-low both submitted to the cluster-queue-1
2. cluster-queue-1 and cluster-queue-2 belong to the same cohort `cohort-pool` at first
3. resources(rayjob-high) + resources(rayjob-low) > capacity(cluster-queue-1)
4. then remove the cohort from cluster-queue-1
5. rayjob-high and rayjob-low will keep running



**What you expected to happen**:

high priority rayjob will preempt the lower one.

**How to reproduce it (as minimally and precisely as possible)**:

The process described above.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):
- Kueue version (use `git describe --tags --dirty --always`): main
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-09-27T18:17:01Z

This is somewhat analogous to scheduler vs descheduler. We don't have a process that checks that the decisions taken before still hold.
So far, the effect is that no new workloads would be admitted in this scenario.
I would label this a feature request instead.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-12-21T09:30:23Z

Agree, more like a feature.
/remove-kind bug
/kind feature

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-12-28T22:19:01Z

I think that this feature request isn't only for RayJob.

/retitle Reclaim consumed resources once quit from cohort

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-27T22:33:00Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-04-18T09:11:13Z

/lifecycle frozen
Wait for more feedbacks.
