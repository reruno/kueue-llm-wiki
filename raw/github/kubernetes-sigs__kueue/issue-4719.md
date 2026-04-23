# Issue #4719: Support PodGroups for  MultiKueue, including e2e testing & docs

**Summary**: Support PodGroups for  MultiKueue, including e2e testing & docs

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4719

**Last updated**: 2025-04-16T18:27:19Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-20T14:27:35Z
- **Updated**: 2025-04-16T18:27:19Z
- **Closed**: 2025-04-16T18:27:19Z
- **Labels**: `kind/bug`, `kind/cleanup`, `kind/documentation`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 8

## Description

/kind documentation
/kind bug

**What would you like to be added**:

Support for Pod groups.

Include a dedicated e2e test for PodGroups.

Also, update documentation for PodGroups in https://kueue.sigs.k8s.io/docs/tasks/run/multikueue/plain_pods/

**Why is this needed**:

To make sure PodGroups work with MK and there is no regression in future.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T14:44:42Z

/kind feature
as it seems not being supported actually
cc @mszadkow @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T14:52:19Z

/assign @mszadkow 
tentatively

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-20T15:08:45Z

/kind bug
/remove-kind feature
Actualy, it probably does not require any API changes, we just need to make sure we create mirror copies of all Pods.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-28T11:40:28Z

I think I got it...
Pod-group fails in `multikueue/workload.go` with `No multikueue adapter found` and that's because the `.OwnerReference.Controller` is not set.
The difference there is `OwnerReference` for pod groups is set with `SetOwnerReference` while for single pod it's `SetControllerReference`.

It works fine for single-cluster env, because there is no Multikueue wl reconciler which sets `kueue.CheckStateRejected` for the pod-group workload.

Question: Why was it OwnerReference instead of OwnerController for pod group in the first place?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-28T11:44:47Z

> Question: Why was it OwnerReference instead of OwnerController for pod group in the first place?

ControllerReference implies there is only one owners IIRC. You can have multiple OwnerReferences.

However, I think this is a technical detail, the main issue it does not work is that in the SyncJob we need to create mirror pods for the entire group, and our code assumes always creating only one "mirror" job / pod.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-03-28T11:55:11Z

We do not pass this point - https://kueue.sigs.k8s.io/docs/concepts/multikueue/#job-flow
`When the job’s Workload gets a QuotaReservation in the manager cluster, a copy of that Workload will be created in all the configured worker clusters.`
Our workload gets rejected before the copy is created in workers.
Sure possibly there is another issue, but this one is not a detail

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T06:31:22Z

/reopen
Let's also add some note indicating pod groups are supported in the docs, as of 0.11.4. We may need to time the release of website and the 0.11.4.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-04-08T06:31:27Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4719#issuecomment-2785371105):

>/reopen
>Let's also add some note indicating pod groups are supported in the docs, as of 0.11.4. We may need to time the release of website and the 0.11.4.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
