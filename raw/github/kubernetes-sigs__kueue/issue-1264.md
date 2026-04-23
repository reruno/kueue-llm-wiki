# Issue #1264: Adding toleration to the job doesn't trigger workload change.

**Summary**: Adding toleration to the job doesn't trigger workload change.

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/1264

**Last updated**: 2024-01-16T05:49:30Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yaroslava-serdiuk](https://github.com/yaroslava-serdiuk)
- **Created**: 2023-10-26T09:36:54Z
- **Updated**: 2024-01-16T05:49:30Z
- **Closed**: 2024-01-16T05:49:30Z
- **Labels**: `kind/support`
- **Assignees**: [@stuton](https://github.com/stuton)
- **Comments**: 2

## Description

Due to [documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/#mutable-scheduling-directives) 
> The fields in a Job's pod template that can be updated are node affinity, node selector, tolerations, labels, annotations and scheduling gates

However modifying those fields doesn't trigger any change in job reconciler, because workload identified as matched to the updated job (https://github.com/kubernetes-sigs/kueue/blob/main/pkg/controller/jobframework/reconciler.go#L409)

We already have a todo to fix this https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/equality/podset.go#L27

## Discussion

### Comment by [@trasc](https://github.com/trasc) — 2023-10-26T12:11:36Z

> We already have a todo to fix this https://github.com/kubernetes-sigs/kueue/blob/main/pkg/util/equality/podset.go#L27

Indeed, at least for tolerations which could influence the flavor assigned, we should update the podsets, however the toleratoins can also be changed (in the job) by Kueue on startJob()/stopJob(), this should be taken into account and propagate the change only when the workload is not reserving quota.

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2023-10-26T17:56:41Z

/assign stuton
