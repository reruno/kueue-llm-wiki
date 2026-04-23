# Issue #405: Add support for max runtime for workloads

**Summary**: Add support for max runtime for workloads

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/405

**Last updated**: 2023-01-26T21:21:20Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@kannon92](https://github.com/kannon92)
- **Created**: 2022-09-26T19:13:36Z
- **Updated**: 2023-01-26T21:21:20Z
- **Closed**: 2023-01-26T00:57:55Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: _none_
- **Comments**: 10

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:
It would be useful if ClusterQueues had a way to enforce walltime limit. 

This would enforce a walltime limit for any workload that is admitted into the ClusterQueue.   

**Why is this needed**:

In HPC schedulers, it is common to have multiple layers where users can request a job with a set walltime limit.  It is also common for admins to set up walltime limits.

A Batch user can submit a workload and should also be able to request a walltime limit for their job.  This can be useful because it allows a user to have greater control over how long their job will run for.  

An admin can design queues with various lengths for run time.  I've seen this in some HPC centers as a way to have dedicated queues for short lived jobs.  

One question I have is where should the user requested walltime limit live?   

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-27T07:00:20Z

What do you need in addition to terminating the job once the deadline is hit?

Such field already exists in Job: https://kubernetes.io/docs/concepts/workloads/controllers/job/#job-termination-and-cleanup
Although we don't utilize that information in kueue.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-27T14:17:07Z

Yea I saw that as I posted this.  In the Kueue design docs, it talks about having workloads as an abstraction for Jobs/CustomJobObjects.  That link is obviously specific to Jobs but I was wondering for other custom controllers.  But maybe we can call it solved for the JobController at the moment.  And other Job implementations would need their own deadline implemented.  

And are you okay with the addition to CQ?  Even if most users puts a deadline on their job, it may be good to have default limits on Queues for those that do not.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-27T16:10:55Z

#83 discusses this topic a bit, however, as a signal for preemption, instead of a hard deadline. We can certainly discuss making it more aggressive.

As for defaults, probably LocalQueue might be enough.

I'm working on a KEP for preemption that I hope to share next week.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-12-26T16:21:30Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-12-27T00:43:24Z

/lifecycle rotten

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2023-01-26T00:57:52Z

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

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-01-26T00:57:56Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/405#issuecomment-1404428953):

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


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-26T13:32:31Z

@kannon92 please have a look at the preemption KEP https://github.com/kubernetes-sigs/kueue/tree/main/keps/83-workload-preemption #83 

Please reopen if you would like to still have some form of max runtime even with preemption.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-26T13:33:20Z

Also you could have a look at #477

### Comment by [@kannon92](https://github.com/kannon92) — 2023-01-26T21:21:19Z

Yea no worries.   I created this when I was thinking a bit about interactive jobs.  But not sure if there was a strong interest from anyone on that one.  I think it'd be nice to eventually have a max walltime on a queueing solution but I think there are higher priority items that are more useful atm
