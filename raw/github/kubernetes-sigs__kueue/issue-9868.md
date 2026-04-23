# Issue #9868: Support DRA Extended Resources (KEP-5004) in Kueue

**Summary**: Support DRA Extended Resources (KEP-5004) in Kueue

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9868

**Last updated**: 2026-04-01T11:16:16Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Created**: 2026-03-13T13:41:28Z
- **Updated**: 2026-04-01T11:16:16Z
- **Closed**: 2026-04-01T11:16:16Z
- **Labels**: `kind/feature`
- **Assignees**: [@sohankunkerkar](https://github.com/sohankunkerkar)
- **Comments**: 4

## Description

 **What would you like to be added**:
When a DeviceClass has `spec.extendedResourceName` set ([KEP-5004](https://github.com/kubernetes/enhancements/issues/5004), Alpha in K8s 1.34), the kube-scheduler automatically converts extended resource requests (e.g., `nvidia.com/gpu: 1`) into ResourceClaims. Kueue needs to handle this to avoid double counting. The workload's pod spec has the extended resource request, and the scheduler also creates a ResourceClaim. Without proper handling, Kueue charges quota for both.

  **Why is this needed**:
Extended resources are the bridge between the legacy device plugin model (`resources.requests: nvidia.com/gpu: 1`) and DRA. As vendors migrate their drivers from device plugins to DRA, existing workloads using extended resource syntax should continue working with Kueue quota management. Without this, workloads using extended resources with DRA-backed DeviceClasses would either be double-counted or not counted at all.

 **This enhancement requires the following artifacts**:

  - [x] Design doc — https://github.com/kubernetes-sigs/kueue/pull/8734
  - [x] Implementation — https://github.com/kubernetes-sigs/kueue/pull/8597
  - [ ] Docs update

  Part of #8243

## Discussion

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-13T13:41:44Z

/assign

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-13T13:41:52Z

/kind feature

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2026-03-21T23:59:19Z

/reopen
for documentations @sohankunkerkar

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2026-03-21T23:59:25Z

@tenzen-y: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/9868#issuecomment-4104951082):

>/reopen
>for documentations @sohankunkerkar 


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
