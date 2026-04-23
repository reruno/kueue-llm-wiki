# Issue #7418: Topology does not support 16 levels as expected

**Summary**: Topology does not support 16 levels as expected

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7418

**Last updated**: 2025-10-29T06:22:03Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-28T13:15:16Z
- **Updated**: 2025-10-29T06:22:03Z
- **Closed**: 2025-10-29T06:22:03Z
- **Labels**: `kind/bug`
- **Assignees**: [@kannon92](https://github.com/kannon92)
- **Comments**: 1

## Description

**What happened**:

We have bumped the number of Topology levels to 16: https://github.com/kubernetes-sigs/kueue/blob/2274d7926454fc51150ced4f7128ca010a0014b8/apis/kueue/v1beta2/topology_types.go#L102

However, this cannot work well because we have also these constraints: 
https://github.com/kubernetes-sigs/kueue/blob/2274d7926454fc51150ced4f7128ca010a0014b8/apis/kueue/v1beta2/workload_types.go#L272

https://github.com/kubernetes-sigs/kueue/blob/2274d7926454fc51150ced4f7128ca010a0014b8/apis/kueue/v1beta2/workload_types.go#L290

https://github.com/kubernetes-sigs/kueue/blob/2274d7926454fc51150ced4f7128ca010a0014b8/apis/kueue/v1beta2/localqueue_types.go#L108

same for v1beta1

**What you expected to happen**:

16 levels is properly supported

## Discussion

### Comment by [@kannon92](https://github.com/kannon92) — 2025-10-28T20:51:18Z

/assign 

opened up https://github.com/kubernetes-sigs/kueue/pull/7423
