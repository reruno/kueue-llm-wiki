# Issue #1463: Improve integration coverage for jobset integration

**Summary**: Improve integration coverage for jobset integration

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1463

**Last updated**: 2025-04-22T11:52:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-12-15T15:37:31Z
- **Updated**: 2025-04-22T11:52:01Z
- **Closed**: 2025-04-22T11:51:59Z
- **Labels**: `kind/feature`, `lifecycle/stale`
- **Assignees**: _none_
- **Comments**: 25

## Description

**What would you like to be added**:

The integration tests for JobSet are very basic. We should have more coverage around queuing multiple jobsets, preemptions, eviction due to timeout, etc.

A simple E2E test would be useful as well.

**Why is this needed**:

As an important investment for k8s, we need to ensure the jobset integration has the highest level of coverage possible.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-15T15:37:53Z

@danielvegamyhre @kannon92 can any of you take this?

### Comment by [@dejanzele](https://github.com/dejanzele) — 2023-12-15T16:49:27Z

I also have capacity to help if they are currently unavailable

### Comment by [@danielvegamyhre](https://github.com/danielvegamyhre) — 2023-12-15T16:51:29Z

@dejanzele go ahead, it would be much appreciated

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-12-15T18:13:27Z

As part of the test cases, it would be good to include jobsets that have multiple resources, and use both parallelism and replicas.

### Comment by [@dejanzele](https://github.com/dejanzele) — 2023-12-17T23:48:49Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-03-17T00:29:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-03-26T20:39:07Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-24T21:00:40Z

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

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T14:48:48Z

@dejanzele are you still working on this?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-25T15:45:42Z

/remove-lifecycle stale

### Comment by [@dejanzele](https://github.com/dejanzele) — 2024-07-01T08:36:52Z

@alculquicondor currently I don't have capacity in the following couple of weeks due to other work so I'll unassign myself. If it is still unassigned when I get more capacitiy, I will revisit this.

/unassign

### Comment by [@highpon](https://github.com/highpon) — 2024-07-14T17:56:04Z

/assign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-10-12T18:34:23Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-14T07:42:01Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-14T07:42:34Z

@highpon any progress on that?

### Comment by [@highpon](https://github.com/highpon) — 2024-10-21T12:59:43Z

@mimowo 
Sorry, I am not able to start this task at this time.
I remove my assignment.

### Comment by [@highpon](https://github.com/highpon) — 2024-10-21T13:00:03Z

/unassign

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-19T13:10:09Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-01-20T06:39:00Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-20T07:05:41Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-22T06:37:28Z

@tenzen-y I suggest we can already close it, let's break down the description

> The integration tests for JobSet are very basic. We should have more coverage around queuing multiple jobsets, preemptions, eviction due to timeout, etc.

1. [queuing multiple jobsets](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/controller/jobs/jobset/jobset_controller_test.go#L1034-L1080)
2. [preemptions](https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/test/integration/singlecluster/controller/jobs/jobset/jobset_controller_test.go#L355-L360)
3. [eviction due to timeout](https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/test/integration/singlecluster/controller/jobs/jobset/jobset_controller_test.go#L736) 

> A simple E2E test would be useful as well.

- [test/e2e/singlecluster/jobset_test.go](https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/singlecluster/jobset_test.go)

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-22T11:35:02Z

> [@tenzen-y](https://github.com/tenzen-y) I suggest we can already close it, let's break down the description
> 
> > The integration tests for JobSet are very basic. We should have more coverage around queuing multiple jobsets, preemptions, eviction due to timeout, etc.
> 
> 1. [queuing multiple jobsets](https://github.com/kubernetes-sigs/kueue/blob/main/test/integration/singlecluster/controller/jobs/jobset/jobset_controller_test.go#L1034-L1080)
> 2. [preemptions](https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/test/integration/singlecluster/controller/jobs/jobset/jobset_controller_test.go#L355-L360)
> 3. [eviction due to timeout](https://github.com/kubernetes-sigs/kueue/blob/3279d9c05817e465229fac6bdc64250c890ea7dd/test/integration/singlecluster/controller/jobs/jobset/jobset_controller_test.go#L736)
> 
> > A simple E2E test would be useful as well.
> 
> * [test/e2e/singlecluster/jobset_test.go](https://github.com/kubernetes-sigs/kueue/blob/main/test/e2e/singlecluster/jobset_test.go)

IIRC, we aimed to implement every case for multi-podTemplate Jobs in JobSet. Currently, we implement every integration test case only in the batch/v1 Job. However, if we are ok without adding every cases to JobSet integration tests, we can close this issue.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-22T11:43:58Z

Given we already have sanity integration and E2e tests, I think we can add the integration test cases to JobSet as we go. 

The logic for Jobset and Job is mostly commonized by the GenericJob reconciler. There are exceptions (test scenarios different for Job and JobSet) but I believe most of them are already covered by the dedicated tests.

So I'm ok without the strict rule saying that every test case needs to be duplicated.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-22T11:51:55Z

> Given we already have sanity integration and E2e tests, I think we can add the integration test cases to JobSet as we go.
> 
> The logic for Jobset and Job is mostly commonized by the GenericJob reconciler. There are exceptions (test scenarios different for Job and JobSet) but I believe most of them are already covered by the dedicated tests.
> 
> So I'm ok without the strict rule saying that every test case needs to be duplicated.

SGTM, if we find other requests for implementing every cases in JobSet, we can revisit here.
Thank you for summarizing cases.
/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-22T11:52:00Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1463#issuecomment-2821083196):

>> Given we already have sanity integration and E2e tests, I think we can add the integration test cases to JobSet as we go.
>> 
>> The logic for Jobset and Job is mostly commonized by the GenericJob reconciler. There are exceptions (test scenarios different for Job and JobSet) but I believe most of them are already covered by the dedicated tests.
>> 
>> So I'm ok without the strict rule saying that every test case needs to be duplicated.
>
>SGTM, if we find other requests for implementing every cases in JobSet, we can revisit here.
>Thank you for summarizing cases.
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
