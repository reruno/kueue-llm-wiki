# Issue #3134: Dedicated documentation folder for running Jobs in MultiKueue

**Summary**: Dedicated documentation folder for running Jobs in MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3134

**Last updated**: 2024-11-15T11:05:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-25T10:48:25Z
- **Updated**: 2024-11-15T11:05:10Z
- **Closed**: 2024-11-15T11:05:07Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 10

## Description

**What would you like to be added**:

A dedicated docs folder to group together sub-pages of running different Job CRDs on MultiKueue.

Sub-pages documenting Job and JobSet could be the starting point as supported in 0.8.1.

**Why is this needed**:

We already support JobSet, Job, MPIJob, Training Operator, but all the jobs have different level of support, so I think a dedicated page per CRD is justified. Running workloads on MultiKueue is complicated, so having the information in one place rather than scattered will be useful.

It would be a nice place to host the information for the content in https://github.com/kubernetes-sigs/kueue/pull/3126.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-25T10:48:41Z

/assign @mszadkow 
/cc @mwielgus @alculquicondor @tenzen-y

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-25T17:23:02Z

That sounds good to me. Is there any recommendation for the directory structure?
I'm wondering if we can create 2 directories:

- /Tasks/Run Workloads/Single Cluster
- /Tasks/Run Workloads/Multiple Clusters

Any thoughts?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-26T07:00:05Z

>  Is there any recommendation for the directory structure?

I'm proposing in the PR review to just have "/Tasks/Run Workloads/Using MultiKueue" folder, and under it put: Job, JobSet, TrainingOperator/MPIJob.

> I'm wondering if we can create 2 directories:

This could work, but it will mean one more level of nesting (click) to get to the most typical places (single jobs). Also, the MultiKueue folder may not be needed in the long run if we have full support for managedBy across all CRDs (one day).

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-26T15:27:41Z

> > Is there any recommendation for the directory structure?
> 
> I'm proposing in the PR review to just have "/Tasks/Run Workloads/Using MultiKueue" folder, and under it put: Job, JobSet, TrainingOperator/MPIJob.

In that case, I would propose using the "/Tasks/Run Workloads/Job Dispatching to MultiCluter" since the "MultiKueue" is no generic term. It would be helpful to look for the page for the MultiCluster support.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-27T13:52:27Z

"Job Dispatching to MultiCluster" is fine for me, but how about "Multi-cluster Job dispatching"?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-27T13:54:56Z

> "Job Dispatching to MultiCluster" is fine for me, but how about "Multi-cluster Job dispatching"?

SGTM I just wanted to say that using the generic term would be better.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2024-11-15T10:09:32Z

@mimowo what do you think is needed to close this issue?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-15T10:31:12Z

I think we are done.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-15T11:05:02Z

/close
We can open another issue or directly a PR if something needs more care.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-11-15T11:05:08Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3134#issuecomment-2478572226):

>/close
>We can open another issue or directly a PR if something needs more care.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
