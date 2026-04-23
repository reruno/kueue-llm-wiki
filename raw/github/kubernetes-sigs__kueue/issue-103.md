# Issue #103: ClusterQueue updates/deletions and running workloads

**Summary**: ClusterQueue updates/deletions and running workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/103

**Last updated**: 2022-09-01T20:43:43Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-09T01:21:57Z
- **Updated**: 2022-09-01T20:43:43Z
- **Closed**: 2022-09-01T20:43:43Z
- **Labels**: `kind/feature`, `priority/important-longterm`
- **Assignees**: _none_
- **Comments**: 10

## Description

With regards to CQ deletions, perhaps we can inject finalizers to block the delete until all running workloads finish, at the same time stop admitting new workloads.

What about CQ updates? One simple solution is to make everything immutable, and so updating a CQ is only possible by recreating it, hence we reduce update to a delete which we already handled above. We can relax this a little by allowing the following updates:
1) an increase to existing quota 
2) adding new resources and/or flavors
3) setting a cohort only if it was not set before

all of those updates don't impact running workloads and can be done without checking for current usage levels.

/kind feature

## Discussion

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-06-07T02:08:46Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues and PRs.

This bot triages issues and PRs according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue or PR as fresh with `/remove-lifecycle stale`
- Mark this issue or PR as rotten with `/lifecycle rotten`
- Close this issue or PR with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-13T10:36:52Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-13T14:19:44Z

I think resizing a CQ is a valid use case. For example, when you have a cluster that is used for batch and non-batch workloads, you could have a controller that resizes the quotas based on the usage from no-batch workloads.

Prohibiting downsizing might make it very hard. As it currently is implemented, when you downsize a CQ, the behavior would be similar to when you borrow resources from another CQ: wait for jobs to finish. Maybe we can reclaim some resources once we implement preemption.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-21T14:14:56Z

Perhaps starting from making everything including updates immutable and relax later those special update cases is a reasonable first step, what do you think?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-21T14:25:32Z

My hesitation is that it would make a simple use case, increase/decrease quotas, much harder to do.

But we could start with adding a finalizer to restrict deletion and stop admitting workloads into a CQ if it has a deletionTimestamp

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-21T14:37:01Z

what do we do with downsizing then in the meantime?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-21T14:46:54Z

You just wait for some workloads to finish and the remaining ones to fit in the smaller quota.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-06-21T14:52:18Z

ok, and I am guessing we don't need to do anything to support this path, it is already what we do; we probably still need to make sure that there are no assumptions on the cohort quota being greater than or equal to the sum of running workloads requests.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-06-21T14:58:54Z

We only look at the (sum of) quotas when scheduling, so the behavior is the same for cohorts.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-01T20:43:43Z

Done.
