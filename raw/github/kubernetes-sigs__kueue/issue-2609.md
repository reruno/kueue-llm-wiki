# Issue #2609: Add a column to workload indicating if it is finished

**Summary**: Add a column to workload indicating if it is finished

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/2609

**Last updated**: 2024-07-16T00:39:11Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-07-15T07:26:09Z
- **Updated**: 2024-07-16T00:39:11Z
- **Closed**: 2024-07-16T00:39:11Z
- **Labels**: `kind/feature`
- **Assignees**: [@highpon](https://github.com/highpon)
- **Comments**: 3

## Description

<!-- Please only use this template for submitting enhancement requests -->

**What would you like to be added**:

A column indicating if a workload is finished. Similarly as we do for Admitted column. I think it is relevant enough that it does not need to be under "wide".

**Why is this needed**:

Currently using `kubectl get wl -owide` I cannot tell quickly if the reserving workloads are finished or not.

Example output, here 3/6 "admitted" workloads are actually finished: 

```
> k get wl -owide                                                             
NAME                        QUEUE        RESERVED IN     ADMITTED   AGE
job-sample-job4qjzj-f764e   user-queue                              4m24s
job-sample-jobc64zt-36632   user-queue   cluster-queue   True       5m48s
job-sample-jobdlx8d-a7632   user-queue   cluster-queue   True       5m24s
job-sample-jobdzsxc-c59bb   user-queue   cluster-queue   True       5m9s
job-sample-jobjnnfc-02e58   user-queue                              4m15s
job-sample-jobllnr5-b9c9b   user-queue   cluster-queue   True       5m26s
job-sample-jobshpdq-4abf0   user-queue   cluster-queue   True       5m49s
job-sample-jobxjqdx-135e1   user-queue   cluster-queue   True       5m25s
job-sample-jobxzqqn-a74a9   user-queue                              4m7s
job-sample-jobzdjwb-b9051   user-queue                              4m41s
```

## Discussion

### Comment by [@highpon](https://github.com/highpon) — 2024-07-15T12:30:25Z

@mimowo 
Very interesting feature!
I would like to implement this feature if you allow me.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-07-15T12:43:31Z

@highpon feel free to propose a PR

### Comment by [@highpon](https://github.com/highpon) — 2024-07-15T12:45:13Z

Thanks!

/assign
