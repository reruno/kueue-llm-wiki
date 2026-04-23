# Issue #9782: TAS: improve performance of the addNode function

**Summary**: TAS: improve performance of the addNode function

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9782

**Last updated**: 2026-03-11T08:09:36Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-03-10T11:55:35Z
- **Updated**: 2026-03-11T08:09:36Z
- **Closed**: 2026-03-11T08:09:36Z
- **Labels**: `kind/cleanup`
- **Assignees**: [@mbobrovskyi](https://github.com/mbobrovskyi)
- **Comments**: 1

## Description

<!-- Please only use this template for submitting clean up requests -->

**What would you like to be cleaned**:

The addNode function is pretty simple https://github.com/kubernetes-sigs/kueue/blob/5fd2aa1291aa02429b2770a3dd474bf4455325af/pkg/cache/scheduler/tas_flavor_snapshot.go#L156-L177

Yet, the function shows up on the pprof graphs, see:
- https://github.com/kubernetes-sigs/kueue/issues/9337
- https://github.com/kubernetes-sigs/kueue/pull/9712#issuecomment-4023895532

I think we could easily optimize the case when `kubernetes.io/hostname` is the lowest level. This would help to reduce the time spent 2x based on : 

<img width="358" height="398" alt="Image" src="https://github.com/user-attachments/assets/27550ca2-879e-4e18-ba10-925fe33370d9" />


**Why is this needed**:

To improve TAS performance for snapshot building.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-10T11:55:54Z

/assign @mbobrovskyi 
tentatively
