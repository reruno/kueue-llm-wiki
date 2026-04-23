# Issue #3984: Kueue state

**Summary**: Kueue state

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3984

**Last updated**: 2025-01-19T07:25:10Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@gbenhaim](https://github.com/gbenhaim)
- **Created**: 2025-01-16T10:11:34Z
- **Updated**: 2025-01-19T07:25:10Z
- **Closed**: 2025-01-19T07:25:10Z
- **Labels**: `kind/support`
- **Assignees**: _none_
- **Comments**: 8

## Description

Where does kueue stores its state? how the queue is recovered if the controllers restart? I've tried to look for this information in the docs but I didn't find it.

Thanks !

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-16T10:46:11Z

Hi @gbenhaim, Kueue stores its state in-memory cache (eg. used for ordering of workloads for scheduling) which is constructed and maintained based on the state of the API objects (like Jobs and Workloads). The API objects are stored in etcd (like any other k8s API objects). Does it answer your questions, or would you like to know more details?

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2025-01-17T06:44:50Z

A question suddenly came to mind the previous API objects cached ( like Job, Workloads) order how to recover it if the kueue-controller restarted?  @mimowo

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-17T06:49:37Z

When kueue controller is restarted it receives the ADDED events for all API objects it has informers ( workloads Jobs etc.). Based on the even handlers it rebuilds the cache. This way it does not require any dedicated routine to populate the cache on startup.

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2025-01-17T07:06:25Z

> When kueue controller is restarted it receives the ADDED events for all API objects it has informers ( workloads Jobs etc.). Based on the even handlers it rebuilds the cache. This way it does not require any dedicated routine to populate the cache on startup.

Thank you reply so quickly.  Let us think this scenario:

there are  5 workloads in the queue that need to be admitted.  the order is workload1, workload3, workload2, workload5, workload4. After restarting,  the 5 workloads re-cached will be in the same order as before restarting?

According to your answer, IIUC the order cannot be guaranteed. It that correct? 

@mimowo Thank your again.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-17T07:31:21Z

After the events about the workloads are received by kueue it will order them in the same deterministic order based on priorities and creation timestamps.

However, you got me thinking. I think it is possible that kueue starts scheduling after restart when knowing only about a subset of workloads. And as a result there is probably indeed a small time window when a lower priority workload may slip in. 

To mitigate you may configure preemptions or use kueue with 2 replicas. In that setup the fail over replica constantly maintains its cache so it will not need to rebuild it from scratch when the main replica fails.

### Comment by [@bobsongplus](https://github.com/bobsongplus) — 2025-01-17T07:37:30Z

> After the events about the workloads are received by kueue it will order them in the same deterministic order based on priorities and creation timestamps.
> 
> However, you got me thinking. I think it is possible that kueue starts scheduling after restart when knowing only about a subset of workloads. And as a result there is probably indeed a small time window when a lower priority workload may slip in.
> 
> To mitigate you may configure preemptions or use kueue with 2 replicas. In that setup the fail over replica constantly maintains its cache so it will not need to rebuild it from scratch when the main replica fails.

Same as you think, In the product environment, we need a highly available deployment mode.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-17T17:54:24Z

Let me know if you need more info here, or would like to document some of the discussion on the website. Otherwise I think we can just close the issue as resolved?

### Comment by [@gbenhaim](https://github.com/gbenhaim) — 2025-01-19T07:25:01Z

@mimowo thank you very much for your response. yes this issue can be closed.
