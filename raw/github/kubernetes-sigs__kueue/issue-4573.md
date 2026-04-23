# Issue #4573: TAS: rank-based ordering does not work for implicit requests

**Summary**: TAS: rank-based ordering does not work for implicit requests

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4573

**Last updated**: 2025-03-13T16:26:35Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-03-12T15:45:22Z
- **Updated**: 2025-03-13T16:26:35Z
- **Closed**: 2025-03-13T16:26:33Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 3

## Description

**What happened**:

When using TAS with implicit request defaults (new in the coming 0.11), the rank-based ordering does not work as the PodSetTopologyRequest information about the PodIndexLabel etc. is not populated, see [here](https://github.com/kubernetes-sigs/kueue/blob/843e4df0a871cb83d0e1ed0b26bbe6f65e171a06/pkg/controller/jobframework/tas.go#L30-L42).

The issue is not released yet.

**What you expected to happen**:

The rank-based ordering works normal for workloads using implicit TAS scheduling.

**How to reproduce it (as minimally and precisely as possible)**:

1. Configure TAS
2. Create a Job without the TAS podset annotations
Issue: the job is scheduled without the rank-based ordering

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-12T15:45:56Z

cc @PBundyra @mwysokin 
/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-03-13T16:26:27Z

/close
Closing as it is not a problem we aim to tackle in 0.11. We may or may not return to it when "preferred" becomes the default in the future. For now, the default is "unconstrained" which does not make users expected rank-based ordering: or packing, see also: https://github.com/kubernetes-sigs/kueue/pull/4574#issuecomment-2721156510.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-03-13T16:26:34Z

@mimowo: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/4573#issuecomment-2721885802):

>/close
>Closing as it is not a problem we aim to tackle in 0.11. We may or may not return to it when "preferred" becomes the default in the future. For now, the default is "unconstrained" which does not make users expected rank-based ordering: or packing, see also: https://github.com/kubernetes-sigs/kueue/pull/4574#issuecomment-2721156510.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
