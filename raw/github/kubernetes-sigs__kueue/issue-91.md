# Issue #91: Create an event and update workload status when failing to schedule a workload

**Summary**: Create an event and update workload status when failing to schedule a workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/91

**Last updated**: 2022-04-01T18:06:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-03T02:45:50Z
- **Updated**: 2022-04-01T18:06:47Z
- **Closed**: 2022-04-01T18:06:47Z
- **Labels**: `kind/feature`, `good first issue`, `help wanted`, `priority/important-soon`
- **Assignees**: [@uroy-personal](https://github.com/uroy-personal), [@ArangoGutierrez](https://github.com/ArangoGutierrez)
- **Comments**: 17

## Description

Probably for the workloads that wasn't returned in this loop: https://github.com/kubernetes-sigs/kueue/blob/9912f26234f40a9b43f48b5f2cf3abfde15c55bf/pkg/scheduler/scheduler.go#L142

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-03T14:07:44Z

Let's block this on #87

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-08T21:14:36Z

Actually, it shouldn't conflict much.

Related: #102

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-08T21:19:45Z

/help

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-08T21:19:46Z

@ahg-g: 
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

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/91):

>/help 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-08T21:21:14Z

/good-first-issue

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-08T21:21:15Z

@ahg-g: 
	This request has been marked as suitable for new contributors.

### Guidelines
Please ensure that the issue body includes answers to the following questions:
- Why are we solving this issue?
- To address this issue, are there any code changes? If there are code changes, what needs to be done in the code and what places can the assignee treat as reference points?
- Does this issue have zero to low barrier of entry?
- How can the assignee reach out to you for help?


For more details on the requirements of such an issue, please see [here](https://git.k8s.io/community/contributors/guide/help-wanted.md#good-first-issue) and ensure that they are met.

If this request no longer meets these requirements, the label can be removed
by commenting with the `/remove-good-first-issue` command.


<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/91):

>/good-first-issue


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@uroy-personal](https://github.com/uroy-personal) — 2022-03-14T15:36:01Z

Hi @ahg-g,

I am interested on working on this issue if it is not being worked upon at the moment.  Please let me know if I can assign this issue to myself.
Thanks,
Have a nice Day..

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-14T15:37:38Z

if it's not assigned and it's marked as "good first issue" it's free to take :)

### Comment by [@uroy-personal](https://github.com/uroy-personal) — 2022-03-14T15:46:18Z

> marked

Thanks @alculquicondor..

### Comment by [@uroy-personal](https://github.com/uroy-personal) — 2022-03-14T15:46:28Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-14T17:49:35Z

This is great, thanks @uroy-personal , please let us know if you need help; are you planning on working on it soon?

### Comment by [@uroy-personal](https://github.com/uroy-personal) — 2022-03-14T17:51:53Z

> This is great, thanks @uroy-personal , please let us know if you need help; are you planning on working on it soon?

Yes of course. I will start later today. Will keep you posted on progress and will reach out to you on slack if I get any queries. Thanks for providing me the opportunity to be part of this project.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-21T16:59:51Z

@ArangoGutierrez for this one, I guess we could simply create an event in the same place where you are updating the conditions, right?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-21T17:01:33Z

yup, the wrapper func looks like the right place

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-21T17:01:40Z

/assign

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-28T00:59:09Z

@ArangoGutierrez I assume you will be working on this, correct?

### Comment by [@ArangoGutierrez](https://github.com/ArangoGutierrez) — 2022-03-28T01:10:23Z

Yes, i started working on this late Friday, planning on opening PR tomorrow Monday.
