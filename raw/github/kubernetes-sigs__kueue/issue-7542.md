# Issue #7542: waitForPodsReady feature takes effect in  different scope

**Summary**: waitForPodsReady feature takes effect in  different scope

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7542

**Last updated**: 2026-04-18T12:16:56Z

---

## Metadata

- **State**: open
- **Author**: [@olderTaoist](https://github.com/olderTaoist)
- **Created**: 2025-11-05T11:46:16Z
- **Updated**: 2026-04-18T12:16:56Z
- **Closed**: —
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

the `waitForPodsReady` feature takes effect globally, and I think it should be able to take effect in different scope: 
- cluster scope(present status)
- cohort scope 
- clusterqueue scope (e.g. categorized using labels).


**Why is this needed**:

In a GPU cluster, there are many heterogeneous GPU resources. When the resources of one type of GPU are insufficient, resulting in job's pod scheduling fail,  jobs that use other types of GPUs should not be blocked.


**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-11-05T14:42:47Z

This is also related https://github.com/kubernetes-sigs/kueue/issues/4803.

### Comment by [@olderTaoist](https://github.com/olderTaoist) — 2025-11-06T02:09:04Z

I have reviewed the relevant discussions and kep. Below is our scenario:
1. A team's training tasks are divided into high-priority and low-priority jobs.
2. If high-priority jobs exceed the team's quota, they need to be queued.
3. Low-priority jobs can borrow unused quotas from other teams.

Implementation based on Kueue:
1. The high-priority and low-priority jobs of a team correspond to one `ClusterQueue` respectively.
2. All ClusterQueues belong to the same project-level `Cohort`.
3. All project-level Cohorts are part of the root-level `Cohort`.
4. The `waitPodsReady` feature is enabled for all ClusterQueues that belong high-priority jobs.
5. The "waitPodsReady" feature is enabled for all ClusterQueues that belong low-priority jobs.

The aforementioned `Cohort` and `ClusterQueue` both belong to the same `ResourceFlavor`, and this `ResourceFlavor` contains only one type of GPU resource. With the "waitPodsReady" feature enabled, this implementation offers the following benefits:
1. It resolves the issue where job scheduling for job using one type of GPU resource is blocked due to insufficient availability of another type of GPU resource.
2. Jobs with different priorities that use the same type of GPU resource do not interfere with each other.

Therefore, I believe it is more appropriate to enable `waitPodsReady` feature based on the ClusterQueue or ResourceFlavor dimension.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-12-19T10:36:51Z

/priority important-longterm

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-03-19T11:47:19Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-04-18T12:16:53Z

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
