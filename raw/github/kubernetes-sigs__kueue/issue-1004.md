# Issue #1004: Compose a Workload object using PodTemplate objects

**Summary**: Compose a Workload object using PodTemplate objects

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1004

**Last updated**: 2024-06-24T21:44:46Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2023-07-20T18:47:37Z
- **Updated**: 2024-06-24T21:44:46Z
- **Closed**: 2024-06-24T21:44:45Z
- **Labels**: `kind/feature`, `lifecycle/rotten`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 9

## Description

**What would you like to be added**:

A field in the `PodSet` struct that references a Pod or [PodTemplate object](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-template-v1/)

```golang
type PodSet struct {
  Name string
  Count int32
  Template *corev1.PodTemplateSpec // keep for backwards compatibility
  PodRef *TemplateReference
  PodTemplateRef *TemplateReference
}
```

Only one of (Template, PodRef or PodTemplateRef) can be set.

Caveats:
- A Workload wouldn't be ready for admission until Kueue has seen all the referenced PodTemplate objects.
- The PodTemplate objects should have a label that allows to:
    - reference the Job/MPIJob/etc object
    - filter from a webhook so that we can implement immutability checks.
 - The Job/MPIJob/etc should be the owner of the PodTemplate object so that it can be deleted in cascade when the job is deleted.

**Why is this needed**:

1. We can rely on the apiserver validation for the PodTemplate object.
2. Avoid duplication of the template on a ProvisioningRequest https://github.com/kubernetes/autoscaler/pull/5848 
3. Allow the Workload object to host more specs without worrying about etcd size limits
4. For #976, it feels overkill to have to duplicate the entire podspec just to represent one Pod

If JobSet were to implement a similar approach, we would also reuse the same PodTemplate objects created by users.

**Completion requirements**:

This enhancement requires the following artifacts:

- [x] Design doc
- [x] API change
- [x] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-07-20T18:49:38Z

cc @ahg-g

### Comment by [@stuton](https://github.com/stuton) — 2023-07-21T15:02:17Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-08-10T15:53:25Z

I discussed this offline with @mwielgus and he suggested to drop the `PodRef` field, as it adds extra complication around watchers, while providing marginal benefit.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-01-26T05:27:57Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-26T20:23:37Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-04-25T21:17:44Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-05-25T21:26:17Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2024-06-24T21:44:41Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-24T21:44:45Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1004#issuecomment-2187462590):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
