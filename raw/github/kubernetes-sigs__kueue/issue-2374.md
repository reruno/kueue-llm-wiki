# Issue #2374: Vendor dependencies

**Summary**: Vendor dependencies

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2374

**Last updated**: 2024-06-25T18:15:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@alculquicondor](https://github.com/alculquicondor)
- **Created**: 2024-06-06T18:19:04Z
- **Updated**: 2024-06-25T18:15:46Z
- **Closed**: 2024-06-25T18:15:45Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 11

## Description

**What would you like to be added**:

We are trying to build images in a different infrastructure that requires vendoring the dependencies.

Do you have any strong opinions against vendoring?

**Why is this needed**:

Maybe a side benefit could be to improve CI times? But we would have to test it.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Design doc
- [ ] API change
- [ ] Docs update

The artifacts should be linked in subsequent comments.

## Discussion

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-06T18:19:19Z

cc @tenzen-y @kerthcet @trasc

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-06T18:32:32Z

You indicated to the Go module vendor like https://github.com/kubernetes/kubernetes/tree/master/vendor.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-06T18:54:58Z

Yes, exactly

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-06T19:07:38Z

TBH, I don't prefer to use the vendor since vendors will increase git diff... 
Actually, the cluster-autoscaler removes vendoring recently: https://github.com/kubernetes/autoscaler/pull/6572

I'd like to avoid the vendoring as far as possible, but if vendoring is needed in your building environments, I'm ok with vendoring...

### Comment by [@jasonsmithio](https://github.com/jasonsmithio) — 2024-06-06T23:31:01Z

I would be interested in the pros and cons of having some kind of vendoring for kueue.

### Comment by [@kerthcet](https://github.com/kerthcet) — 2024-06-07T06:06:18Z

We do use vendor to accelerate the CI and offline build for some projects internally, but not a buyer for this if we can avoid.

### Comment by [@trasc](https://github.com/trasc) — 2024-06-07T12:31:40Z

Also on the con side, the dependencies of kueue are not just a few and some of them (`hack/internal/tools`) are not related to the kueue's code but only the tools used.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-07T14:18:37Z

I'm hoping we can just vendor the main go module and not `/hack/internal/tools` or `/site`. Basically anything to build the main binary.

I also asked @liggitt about any plans for k/k to remove /vendor, and he said there are none.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-20T13:41:50Z

#2403 is ready for merge, if there are no strong opinions against

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-06-25T18:15:41Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T18:15:45Z

@tenzen-y: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/2374#issuecomment-2189662679):

>/close
>


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
