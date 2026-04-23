# Issue #1587: Add documentation page on preemption

**Summary**: Add documentation page on preemption

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1587

**Last updated**: 2024-06-25T20:58:01Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-01-16T11:38:21Z
- **Updated**: 2024-06-25T20:58:01Z
- **Closed**: 2024-06-25T20:57:59Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 9

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A page for documentation of preemption. Preferably with some examples and diagrams.


**Why is this needed**:

Currently, the only available documentation on preemption is API reference. This is hard to digest without supporting diagrams and examples.

**Completion requirements**:

This enhancement requires the following artifacts:

- [ ] Docs update

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-16T11:40:36Z

cc @alculquicondor @mwielgus 
The remaining question is, do we want to as Concepts, Tasks, or idependent page, such as `Admission Checks`. 

I think we could go under "Tasks" as "Configure preemption".

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-16T14:38:51Z

@mimowo We have documentation for the preemption here: https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption

### Comment by [@mimowo](https://github.com/mimowo) — 2024-01-16T14:47:43Z

@tenzen-y thank you! So, from the perspective of completing https://github.com/kubernetes-sigs/kueue/issues/1337 it should be enough to extend that page, right/

Still, I think it makes sense to keep the Issue open, because the page is pretty much just API. I imagine it would be nice to have the documentations with diagrams such as https://github.com/kubernetes-sigs/kueue/issues/1283#issuecomment-1834370396. WDYT?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-01-16T15:31:57Z

Yeah, a Task page would be great in the future, describing multiple scenarios.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-01-16T16:13:26Z

> @tenzen-y thank you! So, from the perspective of completing #1337 it should be enough to extend that page, right/

It's correct.

> Still, I think it makes sense to keep the Issue open, because the page is pretty much just API. I imagine it would be nice to have the documentations with diagrams such as [#1283 (comment)](https://github.com/kubernetes-sigs/kueue/issues/1283#issuecomment-1834370396). WDYT?

SGTM

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-04-16T12:19:47Z

Another alternative would be a concept page under ClusterQueue?

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:57:52Z

This is done in #2322

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2024-06-25T20:57:56Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2024-06-25T20:58:00Z

@alculquicondor: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/1587#issuecomment-2189956247):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
