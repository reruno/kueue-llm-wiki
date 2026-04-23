# Issue #16: Make the process of `calculateRequirementsForAssignments` parallel.

**Summary**: Make the process of `calculateRequirementsForAssignments` parallel.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/16

**Last updated**: 2024-06-25T21:08:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@denkensk](https://github.com/denkensk)
- **Created**: 2022-02-18T11:00:46Z
- **Updated**: 2024-06-25T21:08:10Z
- **Closed**: 2024-06-25T21:07:41Z
- **Labels**: `kind/feature`, `help wanted`, `priority/backlog`, `lifecycle/frozen`, `kind/productionization`
- **Assignees**: _none_
- **Comments**: 17

## Description

This can be done in parallel

https://github.com/kubernetes-sigs/kueue/blob/f3b25fd960ec04eaa973cc318965e0d50d36b3f8/pkg/scheduler/scheduler.go#L74-L76

We should check what else can be parallelized and set the number of threads via configuration.

/kind feature

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-18T11:01:06Z

/cc @ahg-g @alculquicondor 
/assign @denkensk

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T14:23:11Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T14:30:54Z

/lifecycle frozen

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-08-11T21:07:07Z

This should be simple enough

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-08-11T21:07:08Z

@alculquicondor: 
	This request has been marked as needing help from a contributor.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-help` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/16):

>This should be simple enough
>
>/help


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-01T20:21:50Z

Hello!  I'm interested in pulling this issue.  

I think the code changed a bit since this was posted.  

Is https://github.com/kubernetes-sigs/kueue/blob/6eeb73b1c6b9338f101ab095a39b1434a2f926ba/pkg/scheduler/scheduler.go#L185 this the code that we want to run in parallel now?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-01T20:38:13Z

Thanks Kevin and welcome to Kueue :)

Until we create scalability tests to understand where the bottlenecks are, this issue may not be a priority.

But another issue that needs some attention is https://github.com/kubernetes-sigs/kueue/issues/259; would you be interested in that one?

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-01T20:47:14Z

Yea, that sounds great!  And thank you!  

I've been attending the calls for the working group so I'm interested in helping out where I can.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-01T20:50:44Z

Sounds good, feel free to assign it to yourself, for some reason I can't.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-11T14:21:15Z

@kannon92 any progress on this?

### Comment by [@kannon92](https://github.com/kannon92) — 2023-01-11T14:24:58Z

I have made 0 progress on this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-11T14:52:25Z

Should we leave it open for other contributors or can you still handle it?

### Comment by [@kannon92](https://github.com/kannon92) — 2023-01-11T14:58:06Z

Yea, anyone who is interested should feel free to take it.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-11T15:24:40Z

/help

### Comment by [@kannon92](https://github.com/kannon92) — 2023-01-11T15:26:50Z

/unassign @denkensk

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T21:07:37Z

/close

So far the biggest bottlenecks in Kueue have been the API calls, which @gabesaba optimized.

I don't think we need to introduce parallel computations yet.

EDIT: using locks could even cause performance regressions.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T21:07:41Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/16#issuecomment-2189972026):

>/close
>
>So far the biggest bottlenecks in Kueue have been the API calls, which @gabesaba optimized.
>
>I don't think we need to introduce parallel computations yet.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
