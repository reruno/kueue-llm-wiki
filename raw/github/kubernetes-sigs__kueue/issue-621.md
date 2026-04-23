# Issue #621: Will the CRD’s v1beta1 of the master branch change before release-0.3.0 is released?

**Summary**: Will the CRD’s v1beta1 of the master branch change before release-0.3.0 is released?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/621

**Last updated**: 2023-03-10T14:00:00Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@fjding](https://github.com/fjding)
- **Created**: 2023-03-10T09:44:56Z
- **Updated**: 2023-03-10T14:00:00Z
- **Closed**: 2023-03-10T13:59:59Z
- **Labels**: _none_
- **Assignees**: _none_
- **Comments**: 7

## Description

Hi, I found that there is a big difference between v1alpha2 and v1beta1. I want to know whether the crd of v1beta1 has been confirmed? Will there be changes before release-0.3.0?

## Discussion

### Comment by [@fjding](https://github.com/fjding) — 2023-03-10T09:50:17Z

We plan to use kueue as the batch scheduling component, but found that v1alpha2 is outdated, so we want to use the master branch as the online version.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-10T10:12:04Z

Thank you for creating this issue!

We plan to include v1beta1 in release-0.3.0.

https://github.com/kubernetes-sigs/kueue/issues/360

> I want to know whether the crd of v1beta1 has been confirmed?

Does that mean you want to know that v1beta1 is tested? If so, we confirmed v1beta1 using the KinD cluster.

https://github.com/kubernetes-sigs/kueue/pull/604

### Comment by [@fjding](https://github.com/fjding) — 2023-03-10T10:58:21Z

> > I want to know whether the crd of v1beta1 has been confirmed?
> 
> Does that mean you want to know that v1beta1 is tested? If so, we confirmed v1beta1 using the KinD cluster.
> 
> #604
I means whether the structure of the CRD will have any  change before release 0.3.0?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2023-03-10T11:03:28Z

We will not release any patch versions for v0.2. So you can deploy v1beta1 using the main branch or v0.3.0.

cc: @alculquicondor @kerthcet

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-10T13:58:54Z

If you have a big need for some patches in v0.2, please send the cherry-picks and we can add a new release.

But our efforts are on v0.3, and yes, it's not backwards compatible. I would appreciate it if you can be an early adopter of v0.3. My plan is to have a release by the end of next week.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-03-10T13:59:55Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2023-03-10T14:00:00Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/621#issuecomment-1463843994):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>
