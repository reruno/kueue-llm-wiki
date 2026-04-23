# Issue #407: Avoid resource fragmentation at the node level

**Summary**: Avoid resource fragmentation at the node level

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/407

**Last updated**: 2023-01-09T13:30:27Z

---

## Metadata

- **State**: open
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-09-30T16:22:52Z
- **Updated**: 2023-01-09T13:30:27Z
- **Closed**: —
- **Labels**: `kind/feature`, `lifecycle/frozen`
- **Assignees**: _none_
- **Comments**: 5

## Description

This is copied from a thread on wg-batch slack channel


We schedule jobs on a set of nodes that vary in capacity (i.e. RAM, CPUs).  Ideally, a queued job should run on the smallest node with sufficient unused capacity, but it should not be admitted by Kueue if there is not such a node.
For example, suppose I have nodes 1=1CPU and 2=2CPU.  If I submit the following jobs:
Job A: 0.5 CPU
Job B: 1 CPU
Job C: 1.5 CPU
Job D : 0.5 CPU

I would like job A to be started on node 1, job B to be started on node 2, and job C to wait patiently until there's room on node 2.  Finally, when Job D is submitted, it should be admitted to schedule (ideally on node 1).

In testing the above scenario, if I define a single ClusterQueue with a default ResourceFlavor, containing in total 3 CPUs, Kueue will admit job C immediately, but once admitted, it will wait in a pending status.  Job D will not be admitted, because job C has allocated the remaining CPUs -- even though it is not using them, because it cannot cobble together capacity across multiple nodes.

One workaround is to instead create a ResourceFlavor for each individual node in my cluster, so that individual jobs are only admitted if there is capacity to run them on one of the individual nodes alongside whatever other jobs are already present?  E.g. above, I would create ResourceFlavors "small" and "large", with capacity of 1/2 CPUs, and label the nodes similarly.

Another solution is to group nodes of the same size as one flavor. This will work if the nodes sizes are multiple of the job sizes.

Both solutions above are fairly hacks, the first will not scale and the scale is too restrictive.

How can we enhance Kueue to solve this problem in a better way? For example, for each quota, I wonder if we can bubble up information related to available fragments

## Discussion

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-30T16:24:04Z

/cc @eskaug

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-10-10T03:04:02Z

Node resources awareness seems the concern of scheduler, but yes back and forth the allocation is a great waste. At the least, we should support something like https://github.com/kubernetes-sigs/kueue/issues/349 for basically.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-10-10T03:13:17Z

Maybe the key point locates at the integration with scheduler(not blocking the optimizations in kueue). Currently we support semantic all-or-nothing allocation in kueue, if we can get the scheduling result from scheduler(like through the ongoing pod group api), we can suspend the job again for insufficient resources.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-01-08T03:50:20Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-09T13:30:24Z

/lifecycle frozen
