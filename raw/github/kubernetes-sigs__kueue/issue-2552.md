# Issue #2552: Support Kubeflow Jobs in MultiKueue

**Summary**: Support Kubeflow Jobs in MultiKueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2552

**Last updated**: 2025-02-14T10:04:23Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-07-08T15:06:31Z
- **Updated**: 2025-02-14T10:04:23Z
- **Closed**: 2025-02-14T10:04:23Z
- **Labels**: `kind/feature`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 18

## Description

**What would you like to be added**:

Support for Kubeflow Jobs in MultiKueue, in particular, for TFJob and PyTorchJob.
Ideally, the implementation should be mostly common among all job types.

Kubeflow Job doesn't have support for managedBy, so, for now, we can only support the scenario where the manager cluster doesn't have the controller installed.

**Why is this needed**:

To continue the incremental improvement of MK and satisfy the needs of early adopters.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-08T15:07:10Z

/assign @mszadkow

### Comment by [@kannon92](https://github.com/kannon92) — 2024-07-15T12:33:49Z

The hope is to implement a new version of Trainingoperator called TrainJob that would use JobSet as the base.

I think if rhat is done then one could use the ManagedField in JobSet for this.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-15T15:24:58Z

Right, but we have users requesting this feature today.

### Comment by [@kannon92](https://github.com/kannon92) — 2024-07-15T15:45:29Z

Should there be some work done to add managedField to the KubeFlow API? Or are we trying to avoid that to satisfy a solution that bypasses KubeFlow releases?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-07-15T17:00:49Z

We don't need it in the current version of MultiKueue. We can just recommend users not to install the operator in the dispatcher cluster.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-12T07:06:04Z

/reopen
Let's close it when the ongoing effort of supporting `managedBy` is complete for the `training-operator` and MPIJob.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-09-12T07:06:08Z

@mimowo: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2552#issuecomment-2345435267):

>/reopen
>Let's close it when the ongoing effort of supporting `managedBy` is complete for the `training-operator` and MPIJob.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-09-18T18:15:44Z

FYI: https://github.com/kubeflow/training-operator/pull/2203 was merged right now.
We will include the feature in the next training-operator minor release.

RC.0 with the managedBy feature will be released on January 20th, 2025.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-12-17T19:13:51Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T07:33:47Z

/remove-lifecycle stale

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-18T07:34:38Z

> RC.0 with the managedBy feature will be released on January 20th, 2025.

@tenzen-y does the plan for Jan 20th still holds?

cc @mszadkow

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-12-18T15:10:30Z

> /reopen Let's close it when the ongoing effort of supporting `managedBy` is complete for the `training-operator` and MPIJob.

We plan to release the final Kubeflow v1 API release within this year.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-23T10:44:23Z

FYI we already have the training-operator rc1 with the managedBy field: https://github.com/kubeflow/training-operator/releases/tag/v1.9.0-rc.0. 

So, we can prepare the PR for the integration already. Depending on the timeline of the full release we can either merge the support using rc1 or wait for the full release, but starting the work early and discovering potential roadblocks would be great.

cc @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-01-27T09:06:27Z

> FYI we already have the training-operator rc1 with the managedBy field: https://github.com/kubeflow/training-operator/releases/tag/v1.9.0-rc.0.
> 
> So, we can prepare the PR for the integration already. Depending on the timeline of the full release we can either merge the support using rc1 or wait for the full release, but starting the work early and discovering potential roadblocks would be great.
> 
> cc [@mszadkow](https://github.com/mszadkow)

ACK

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-12T17:58:20Z

I guess that this has already been completed. @mszadkow @mimowo Do you have any remaining tasks?

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-13T08:03:45Z

I think only documentation left, I will push PR today.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-02-13T08:11:41Z

Please also x-ref the documentation in Kueue with the pending PR for the documentation in kubeflow: https://github.com/kubeflow/website/pull/3956

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-02-13T08:13:19Z

> I think only documentation left, I will push PR today.

Thank you!
