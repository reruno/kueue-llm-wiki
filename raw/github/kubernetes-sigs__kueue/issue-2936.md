# Issue #2936: Default LocalQueue

**Summary**: Default LocalQueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2936

**Last updated**: 2024-12-13T07:22:29Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@KPostOffice](https://github.com/KPostOffice)
- **Created**: 2024-08-29T18:51:10Z
- **Updated**: 2024-12-13T07:22:29Z
- **Closed**: 2024-12-13T07:22:29Z
- **Labels**: `kind/feature`
- **Assignees**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Comments**: 17

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

I would like to be able to indicate a default LocalQueue per namespace to be used for a workload

**Why is this needed**:

If an administrator creates a single LocalQueue per namespace that all workloads are expected to use, defaulting the queue let's quota consumers ignore the need to include Queue specific request labels in their workloads and enforces the need to be associated with a Queue in order to be scheduled.

**Completion requirements**:

- [ ] API changes to LocalQueue spec which allow admin to specify it as default
- [ ] Mutating webhook which will get the default LocalQueue and apply the appropriate label
- [ ] Validating webhook which ensures that only one LocalQueue is marked as default

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-08T16:12:58Z

@KPostOffice Do you assume that automatically https://kueue.sigs.k8s.io/docs/tasks/manage/setup_job_admission_policy/ generation?

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-10-10T22:44:07Z

> @KPostOffice Do you assume that automatically https://kueue.sigs.k8s.io/docs/tasks/manage/setup_job_admission_policy/ generation?

Are you referring to the example AdmissionPolicy outlined in the documentation?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-11T08:12:24Z

> https://kueue.sigs.k8s.io/docs/tasks/manage/setup_job_admission_policy/

Yes, I indicated the ValidatingAdmissionPolicy.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-10-14T09:45:25Z

/assign

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-10-14T14:22:03Z

Yeah, the assumption here would be that the policy would be in place

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-11-15T12:22:28Z

If we are going to modify API to have "default" field, it might be tricky to validate that only one LQ is a default. Are we going to abandon setting LQ as default if another default LQ is present in the namespace (in this case we do not validate the object itself)? If we can have multiple default LQs, which one is an actual default? It could be a first one or the last one.

To avoid those questions and the API change, I suggest to default LocalQueue that has `default` name, WDYT? 
However this might be a breaking change for someone.

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-11-18T14:12:15Z

@KPostOffice could you please tell if https://github.com/kubernetes-sigs/kueue/issues/2936#issuecomment-2478698423 makes sense

### Comment by [@mwielgus](https://github.com/mwielgus) — 2024-11-19T12:19:16Z

Let's have the "default" default LocalQueue and put the whole feature behind a feature gate, so we don't break anyone by accident.

### Comment by [@KPostOffice](https://github.com/KPostOffice) — 2024-11-19T14:17:54Z

Using the `default` LQ name behind a feature gate would be a fine solution from my perspective

### Comment by [@mimowo](https://github.com/mimowo) — 2024-11-25T07:57:29Z

It feels this feature requires a KEP, even if there is no "API" changed, we still introduce a feature-gate. Also, I feel the mechanism will evolve in the future, so having some reference we can update will be useful. It does not need to be long, just one pager to collect the use-cases and the proposed solution.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-11-25T14:43:34Z

> It feels this feature requires a KEP, even if there is no "API" changed, we still introduce a feature-gate. Also, I feel the mechanism will evolve in the future, so having some reference we can update will be useful. It does not need to be long, just one pager to collect the use-cases and the proposed solution.

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-09T15:12:31Z

/reopen
For the documentation update

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-12-09T15:12:37Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2936#issuecomment-2528289484):

>/reopen
>For the documentation update


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-12-10T11:04:42Z

@mimowo could you specify what should be added to documentation?

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-10T11:12:13Z

Basically, we want to have all features documented. Two places come to my mind (could be separate PRs): 
- LocalQueue page: https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/concepts/local_queue.md?plain=1
- a new section in the administrative tasks: https://github.com/kubernetes-sigs/kueue/tree/main/site/content/en/docs/tasks/manage/enforce_job_management, could be entitled "Setup Local Queue defaulting"

cc @PBundyra wdyt?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-10T11:25:08Z

> Basically, we want to have all features documented. Two places come to my mind (could be separate PRs):
> 
> * LocalQueue page: https://github.com/kubernetes-sigs/kueue/blob/main/site/content/en/docs/concepts/local_queue.md?plain=1
> * a new section in the administrative tasks: https://github.com/kubernetes-sigs/kueue/tree/main/site/content/en/docs/tasks/manage/enforce_job_management, could be entitled "Setup Local Queue defaulting"
> 
> cc @PBundyra wdyt?

Agreed, I would also consider adding some note to the [Run A Kubernetes Job](https://kueue.sigs.k8s.io/docs/tasks/run/jobs/) page. However, I believe the note shouldn't be limited only to default LQ but it should also cover jobs without the LQ

### Comment by [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk) — 2024-12-10T11:36:35Z

>Agreed, I would also consider adding some note to the [Run A Kubernetes Job](https://kueue.sigs.k8s.io/docs/tasks/run/jobs/) page. However, I believe the note shouldn't be limited only to default LQ but it should also cover jobs without the LQ

LocalQueueDefaulting is not limited to Kubernetes Job only, seems [sigs/kueue/tree/main/site/content/en/docs/tasks/manage/enforce_job_management](https://github.com/kubernetes-sigs/kueue/tree/main/site/content/en/docs/tasks/manage/enforce_job_management) is the best place.
