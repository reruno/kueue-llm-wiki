# Issue #9: Add events that tracks a workload's status

**Summary**: Add events that tracks a workload's status

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9

**Last updated**: 2022-02-23T18:34:20Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@ahg-g](https://github.com/ahg-g)
- **Created**: 2022-02-17T22:21:54Z
- **Updated**: 2022-02-23T18:34:20Z
- **Closed**: 2022-02-23T18:34:20Z
- **Labels**: `kind/feature`, `priority/important-soon`, `size/M`
- **Assignees**: [@denkensk](https://github.com/denkensk)
- **Comments**: 5

## Description

Two possible locations to issue events:
- when it is assigned a capacity in the scheduling loop.
- in the job-controller when a corresponding workload is created.

/kind feature

## Discussion

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-18T14:39:33Z

/assign

### Comment by [@alculquicondor](https://github.com/alculquicondor) — 2022-02-18T15:15:07Z

also when a workload fails to schedule? Although it might be too noisy now as we don't have a backoff policy.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-18T15:18:50Z

I think we can start by providing the assigned event. 
Scheduling Failed is easy to add after we have a backoff policy. Step by step.

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-19T00:22:35Z

> in the job-controller when a corresponding workload is created.

 Is the created event patched to `job`, right? @ahg-g

### Comment by [@denkensk](https://github.com/denkensk) — 2022-02-19T03:36:05Z

1. when it is assigned a capacity in the scheduling loop #26 
2. in the job-controller when a corresponding workload is created. #36
