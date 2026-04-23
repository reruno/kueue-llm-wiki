# Issue #369: Add Job interface to restrain the behaviors of different Job implementations

**Summary**: Add Job interface to restrain the behaviors of different Job implementations

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/369

**Last updated**: 2023-05-11T13:31:12Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@kerthcet](https://github.com/kerthcet)
- **Created**: 2022-09-05T07:29:16Z
- **Updated**: 2023-05-11T13:31:12Z
- **Closed**: 2023-05-11T13:31:11Z
- **Labels**: `kind/feature`, `lifecycle/frozen`
- **Assignees**: [@kerthcet](https://github.com/kerthcet)
- **Comments**: 21

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

Currently, we have a default integrated implementation of batchv1 job, we achieve the expected behaviors by the experiences of kubernetes, and most importantly, we know the project well.  

But for people who wants to implement a special controller in kueue, they have little knowledges and they may don't know where to start. Documents are great and always needed, but they're not binding. 

So we should make a contract known as interface in golang, which defines the behaviors of the various jobs. E.g.:

```
type Job interface {
	Suspend()
	UnSuspend()
	QueueName()
	IsSuspend() bool
	Start() error
	Stop() error
	ConstructWorkload() (*kueue.Workload, error)
}
````

And we can wrap batch job like below, `BatchJob` is an  implement of kueue.Job

```
type BatchJob struct {
	job batchv1.Job
}
```      


**Why is this needed**:

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-09-05T18:38:05Z

That sounds great!
The job interface helps support Kueue with custom jobs such as TFJob, PytorchJob, and MPIJob in `kubeflow/training-operator` and `kubeflow/mpi-operator/v2`.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-06T14:00:25Z

I would also add some form of `InjectNodeAffinity`

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-09-12T14:14:22Z

> I would also add some form of `InjectNodeAffinity`

Does this mean the following?

https://github.com/kubernetes-sigs/kueue/blob/6e403b517b8a3bfcc71b7ded10be9ca9d8634c5b/pkg/controller/workload/job/job_controller.go#L263-L278

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-12T14:17:05Z

yes

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-09-12T14:17:37Z

SGTM

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-12-11T14:21:14Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2022-12-11T14:25:32Z

/lifecycle frozen

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-01-09T02:29:39Z

We have a plan to integrate with other workloads, also see https://github.com/kubernetes-sigs/kueue/issues/499, I'd like to write a design doc at first.
/assign

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-01-09T03:02:22Z

I'm also working on the kubeflow project.

So I'm thinking of giving feedback on the design doc since I'd like to support Kueue with training-operator and mpi-operator v2.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-01-09T03:10:58Z

Thanks @tenzen-y , when you're ready, plz also cc me, thanks.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-09T13:35:37Z

From the messages above, I'm not sure who is writing the design doc. It sounds like @kerthcet, is that correct?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-01-09T13:38:27Z

> From the messages above, I'm not sure who is writing the design doc. It sounds like @kerthcet, is that correct?

Probably, @kerthcet is writing the doc.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-01-09T13:41:07Z

If @kerthcet doesn't have enough time, I can write it.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-01-09T14:30:09Z

Yes, I'm writing now, almost finished.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-01-09T14:56:57Z

Sounds great.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-20T20:13:47Z

@kerthcet do you have a draft to share? It might be beneficial to provide you feedback already.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-24T16:19:46Z

Oh, from slack, it seems that Kante is OOO until the end of the month

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-01-24T16:20:47Z

Thank you for letting us know.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-01-30T10:28:28Z

FYI https://github.com/kubernetes-sigs/kueue/pull/537 KEP is ready for first round of review.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-05-11T13:31:05Z

This is completed

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-05-11T13:31:12Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/369#issuecomment-1544017310):

>This is completed
>
>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
