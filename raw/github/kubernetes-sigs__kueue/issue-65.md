# Issue #65: Support kubeflow's MPIJob

**Summary**: Support kubeflow's MPIJob

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/65

**Last updated**: 2023-03-03T14:56:59Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-02-24T19:12:56Z
- **Updated**: 2023-03-03T14:56:59Z
- **Closed**: 2023-03-03T14:56:59Z
- **Labels**: `kind/feature`, `priority/important-longterm`, `lifecycle/frozen`, `kind/grand-feature`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 15

## Description

That is kubeflow's mpi-operator. We could have started with other custom jobs, but this one seems important enough for our audience.

They currently don't have a suspend field, so we need to add it. Then, we program the controller based on the existing kueue job-controller.

/label feature
/size L
/priority important-longterm

## Discussion

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-02-24T19:12:58Z

@alculquicondor: The label(s) `/label feature` cannot be applied. These labels are supported: `api-review, tide/merge-method-merge, tide/merge-method-rebase, tide/merge-method-squash, team/katacoda, refactor`

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/65):

>That is kubeflow's mpi-operator. We could have started with other custom jobs, but this one seems important enough for our audience.
>
>They currently don't have a suspend field, so we need to add it. Then, we program the controller based on the existing kueue job-controller.
>
>/label feature
>/size L
>/priority important-longterm


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-24T19:13:08Z

/kind feature

### Comment by [@zvonkok](https://github.com/zvonkok) — 2022-02-25T08:57:03Z

Just out of curiosity how many ranks are you going to test? Are you also looking into different distributions frameworks besides Horovod?

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-25T10:47:04Z

> Just out of curiosity how many ranks are you going to test? 

Any suggestions? I think our first step is to choose a small number of ranks (for example 3 ) to ensure that the whole process is feasible.

> Are you also looking into different distributions frameworks besides Horovod?

I think Kueue is agnostic about the framework. Whether it is Horovrd or pytorch, as long as it can be launched by MPI through mpi-operator, it is fine.

### Comment by [@zvonkok](https://github.com/zvonkok) — 2022-02-25T11:07:46Z

@ArangoGutierrez Help me out, what was the critical amount of ranks aka nodes where we have seen bad scaling for the MPI operator?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-25T14:55:30Z

Sorry, we are not planning to implement an MPIJob. We are planning to support queuing for the existing kubeflow mpi-operator https://github.com/kubeflow/mpi-operator/tree/master/v2

I think your questions fit better in that repository.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2022-07-12T03:12:11Z

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

### Comment by [@kerthcet](https://github.com/kerthcet) — 2022-07-12T03:15:02Z

/remove-lifecycle stale

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-12T13:21:42Z

/lifecycle frozen

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-01-24T16:18:58Z

Work on mpi-operator will initiate soon https://github.com/kubeflow/mpi-operator/issues/504

The kueue size of things is currently blocked on #369

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-16T09:17:13Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2023-02-16T09:27:25Z

Starting the work under https://github.com/kubernetes-sigs/kueue/pull/578.

IIUC the work isn't strictly blocked on https://github.com/kubernetes-sigs/kueue/issues/369. Moreover, the working initial implementation of the MPI integration may help us to better abstract out the interfaces, which could happen as a follow up. Adding the interfaces prior to the MPI integration also makes sense, but we then may need to adapt them, but this may anyway happen with future framework integrations, so maybe there is no point block over another, but just try to align in the process.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-02-16T09:58:31Z

> Starting the work under #578.
> 
> IIUC the work isn't strictly blocked on #369. Moreover, the working initial implementation of the MPI integration may help us to better abstract out the interfaces, which could happen as a follow up. Adding the interfaces prior to the MPI integration also makes sense, but we then may need to adapt them, but this may anyway happen with future framework integrations, so maybe there is no point block over another, but just try to align in the process.

I'm ok with either using the job interface or not since releasing v0.3 isn't blocked by this feature.
cc: @kerthcet @alculquicondor

### Comment by [@kerthcet](https://github.com/kerthcet) — 2023-02-16T10:28:26Z

Either, just hope to avoid repetitive work.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-02-16T16:57:37Z

I think @kerthcet and @mimowo can make progress in parallel. Please stay in touch.
