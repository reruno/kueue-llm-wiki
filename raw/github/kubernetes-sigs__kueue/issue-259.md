# Issue #259: Add number of AdmittedWorkloads to LocalQueue status

**Summary**: Add number of AdmittedWorkloads to LocalQueue status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/259

**Last updated**: 2022-09-09T17:31:25Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2022-05-12T18:28:27Z
- **Updated**: 2022-09-09T17:31:25Z
- **Closed**: 2022-09-09T17:31:25Z
- **Labels**: `kind/feature`, `kind/ux`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 14

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A field containing the number of active workloads.

We abandoned this idea earlier because the cache was not queue aware. But we already need to make it queue aware for the purpose of metrics #199 

**Why is this needed**:

Improve UX around observability

/kind ux

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [x] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@nayihz](https://github.com/nayihz) — 2022-05-23T09:37:13Z

The `active workloads` are the workloads which have been admitted by scheduler. Do I understand it correctly?
https://github.com/kubernetes-sigs/kueue/blob/afabae912eb3da09f810ca6bf0fd5fe5bf49874a/pkg/scheduler/scheduler.go#L304-L308

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-05-31T13:57:18Z

not assumed, but actually part of the cache. But please don't work on this yet. I'm working on a change to add the metric with the same data. We can reuse that code to include it in the status.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-07-11T15:28:07Z

I did some progress on this #259. After it merges, feel free to take over.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-01T20:35:50Z

This would be similar to the AdmittedWorkloads in ClusterQueue

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-01T20:50:07Z

/assign @kannon92

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-09-01T20:50:09Z

@ahg-g: GitHub didn't allow me to assign the following users: kannon92.

Note that only [kubernetes-sigs members](https://github.com/orgs/kubernetes-sigs/people), repo collaborators and people who have commented on this issue/PR can be assigned. Additionally, issues/PRs can only have 10 assignees at the same time.
For more information please see [the contributor guide](https://git.k8s.io/community/contributors/guide/first-contribution.md#issue-assignment-in-github)

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/259#issuecomment-1234765802):

>/assign @kannon92


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-01T20:52:11Z

/assign @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-01T21:30:33Z

I am getting up to speed in this repo.  

AdmittedWorkloads is the same as ActiveWorkloads?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-01T21:39:19Z

yes, we are using the term admitted now.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-02T18:22:10Z

Hello.  So I made progress on this but I realize I'm unclear on the ask.  The issue reads very simple as add a new field.  

So here is my research:

1) Add a new field for AdmittedWorkloads in [Apis](https://github.com/kubernetes-sigs/kueue/blob/main/apis/kueue/v1alpha2/localqueue_types.go#L33)
2) Update the [CRD](https://github.com/kubernetes-sigs/kueue/blob/main/config/components/crd/bases/kueue.x-k8s.io_localqueues.yaml) to reflect the new field

If I read the ticket exactly, then I believe my work is done?  

Is the intent that future features will update this API field?  Or should I also tackle this as part of the issue?

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-09-02T19:22:08Z

Not only add the field, we need to do populate it as well. Kueue is the one responsible for updating the status of both LocalQueue and ClusterQueue.  Take a look at the AdmittedWorkloads field in ClusterQueue and how we populate it as an example.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-06T14:01:43Z

Sounds good!  I am making progress on this.  Do we want these fields as added into metrics also?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-09-06T17:58:36Z

No, we actually did that initially and reverted the change #293.

Just the status field should be good.

### Comment by [@kannon92](https://github.com/kannon92) — 2022-09-08T18:16:41Z

Alright.  I think I have something for you all to review.  https://github.com/kubernetes-sigs/kueue/pull/382

Sorry about the spamming the repo with a few opens.
