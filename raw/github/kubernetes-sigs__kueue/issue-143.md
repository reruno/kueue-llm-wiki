# Issue #143: Should we move QueuedWorkload.Admission to Status?

**Summary**: Should we move QueuedWorkload.Admission to Status?

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/143

**Last updated**: 2022-03-28T17:43:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-03-23T22:21:54Z
- **Updated**: 2022-03-28T17:43:46Z
- **Closed**: 2022-03-28T17:43:26Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 5

## Description

With the recent re-definition of object Status semantics, it is now acceptable to have persistent fields there. Given that, it seems more appropriate to have the `Admission` field of QueuedWorkload in the Status field rather than the Spec.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-03-24T13:17:58Z

My main motivation for putting it in the spec is to give break-glass capabilities to administrators to start jobs directly assigned to a QC. It's not easy to "apply" the status from a yaml.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-24T13:27:10Z

I keep forgetting that reason! Worth documenting it in the docs.

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-28T17:42:13Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2022-03-28T17:43:26Z

@ahg-g: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/143#issuecomment-1080955307):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes/test-infra](https://github.com/kubernetes/test-infra/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@ahg-g](https://github.com/ahg-g) — 2022-03-28T17:43:45Z

> is to give break-glass capabilities to administrators to start jobs directly assigned to a QC

They need to set the flavors as well, which is not a pretty experience.
