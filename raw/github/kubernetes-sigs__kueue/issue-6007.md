# Issue #6007: Relax number of Resources per ResourceGroup and limit the maximal number of Resources in CQ rather

**Summary**: Relax number of Resources per ResourceGroup and limit the maximal number of Resources in CQ rather

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6007

**Last updated**: 2025-10-14T11:03:14Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-07-17T07:34:16Z
- **Updated**: 2025-10-14T11:03:14Z
- **Closed**: 2025-10-14T11:03:13Z
- **Labels**: `kind/feature`
- **Assignees**: _none_
- **Comments**: 4

## Description

**What would you like to be added**:

Currently we limit the number of Resources per ResourceGroup to 16 (see [here](https://github.com/kubernetes-sigs/kueue/blob/03e2b04cdebe66fc58a38663e567254d748aa843/apis/kueue/v1beta1/clusterqueue_types.go#L184)).

This is too constraining for production use as discussed in the [thread](https://github.com/kubernetes-sigs/kueue/issues/5877#issuecomment-3080005818) and creates incentive to artificially split the Resources into Groups.

**Why is this needed**:

Instead of validating number of resources per group, we could assert the total number of resources. My proposal, under discussion:
- limit the total number of resources in all groups to 256 (current max as 16*16 is only allowed)
- relax the number of Resources per ResourceGroup to 64 or 128 (optional, but still might be useful to have some control)

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-07-17T07:34:54Z

cc @gbenhaim @tenzen-y @kannon92

### Comment by [@kannon92](https://github.com/kannon92) — 2025-07-17T11:36:19Z

+1 on this. I think if we want to multiple static mig with different configurations on a node this would be essential.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-14T11:03:08Z

/close
This is addressed in https://github.com/kubernetes-sigs/kueue/pull/6906

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-14T11:03:14Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/6007#issuecomment-3401255867):

>/close
>This is addressed in https://github.com/kubernetes-sigs/kueue/pull/6906


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
