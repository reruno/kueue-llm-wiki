# Issue #7468: v1beta2: change .spec.flavorFungibility, .spec.preemption, .spec.preemption.borrowWithinCohort type from pointer to value

**Summary**: v1beta2: change .spec.flavorFungibility, .spec.preemption, .spec.preemption.borrowWithinCohort type from pointer to value

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7468

**Last updated**: 2025-10-31T07:28:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Created**: 2025-10-31T00:57:44Z
- **Updated**: 2025-10-31T07:28:30Z
- **Closed**: 2025-10-31T07:28:29Z
- **Labels**: `kind/cleanup`
- **Assignees**: _none_
- **Comments**: 5

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:
As we discussed [here](https://github.com/kubernetes-sigs/kueue/issues/768#issuecomment-2056975821) we should change .spec.flavorFungibility, .spec.preemption, .spec.preemption.borrowWithinCohort type from pointer to value for ClusterQueueSpec.

**Why is this needed**:
To avoid using `// +kubebuilder:default={}`.

## Discussion

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-31T00:57:54Z

/cc @IrvingMg @mimowo

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-10-31T06:03:17Z

We are planning to keep those fields as pointers. Please see this one: https://docs.google.com/document/d/1VpSKMZP5cWXvr7NbVM2ay2HyQA6XeymwVGXxdqdhE6Q/edit?resourcekey=0-Eh7NXzwXtZnyAqKlOeTKmA&disco=AAABs86RKxc

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-31T07:28:21Z

Ah, I see. Thank you!

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-10-31T07:28:24Z

/close

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-31T07:28:30Z

@mbobrovskyi: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7468#issuecomment-3471626238):

>/close


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
