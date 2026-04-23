# Issue #4851: Flaky perf scheduling test

**Summary**: Flaky perf scheduling test

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/4851

**Last updated**: 2025-04-24T12:48:41Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-04-01T07:17:59Z
- **Updated**: 2025-04-24T12:48:41Z
- **Closed**: 2025-04-24T12:48:41Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 17

## Description

/kind flake

**What happened**:

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4845/pull-kueue-test-scheduling-perf-main/1906781402901254144

**What you expected to happen**:

no failures

**How to reproduce it (as minimally and precisely as possible)**:

ci

**Anything else we need to know?**:

```
{Failed  === RUN   TestScalability/CommandStats
    checker_test.go:87: Average CPU usage 538mCpu is greater than maximum expected 535mCPU
--- FAIL: TestScalability/CommandStats (0.00s)
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-01T07:21:47Z


This might be related to https://github.com/kubernetes-sigs/kueue/pull/4813 as it is using reclaimWithinCohort: Any. 

cc @mbobrovskyi ptal, maybe the cpu got higher recently, but the execution time dropped? If this is the case, I think it is WAI and I'm ok to bump the thresholds to make it stable.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-07T06:58:38Z

Another occurrence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4837/pull-kueue-test-scheduling-perf-main/1906685554880155648

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-08T09:08:20Z

cc @gabesaba as this might be related to the recent scheduling changes

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T14:00:26Z

another occurrence https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4929/pull-kueue-test-scheduling-perf-main/1912139065210179584

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T14:03:02Z

I would suggest to just bump the CPU to 550m. I don't like the CPU metric anyway and would be ok with dropping the threshold completely, as discussed before when introducing it. 

WDYT @tenzen-y @gabesaba @mbobrovskyi ?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-15T14:05:44Z

I would speculate the CPU consumption increased after the fix by @gabesaba of reclamation, and this is an expected change, but it is hard to confirm now

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-04-16T08:26:06Z

I would either: 

1) increase the threshold with the goal of replacing it very soon
2) delete it now

I lean towards option 2, and open a bug to track creating a better metric

> I don't like the CPU metric anyway and would be ok with dropping the threshold completely, as discussed before when introducing it.

+1

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-16T08:29:42Z

> I lean towards option 2, and open a bug to track creating a better metric

+1, but we already have [maxWallMs](https://github.com/kubernetes-sigs/kueue/blob/d68df3a996c1ef1f6dc4abeb156cc0f934141def/test/performance/scheduler/default_rangespec.yaml#L9) which is the total execution time. Do you have anything else on your mind?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-16T08:35:35Z

What metrics are used in kube-scheduler perf-test? Doesn't it use CPU threshold?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-16T08:40:16Z

It currently does use [mCPU: 535](https://github.com/kubernetes-sigs/kueue/blob/d68df3a996c1ef1f6dc4abeb156cc0f934141def/test/performance/scheduler/default_rangespec.yaml#L12C3-L12C12), and this is the reason for the flakes, because occasionally this is exceeded as in this case it was 538mCpu.

Note that 535 is not the original value which was 500 (iirc), but later bumped.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-16T08:42:27Z

I meant kube-scheduler perf-test instead of kueue scheduler perf-test

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-16T08:51:51Z

cc @macsko who is likely to know

### Comment by [@macsko](https://github.com/macsko) — 2025-04-16T09:01:51Z

> What metrics are used in kube-scheduler perf-test? Doesn't it use CPU threshold?

kube-scheduler perf tests ([scheduler_perf](https://github.com/kubernetes/kubernetes/tree/master/test/integration/scheduler_perf)) verify only the scheduling throughput, without checking cpu/memory usage. Code that calculates the throughput is [here](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L468-L615). It is done using [event handler subscribed on Pod/Add and Pod/Update events](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L486-L511). For statistical purposes, and not for calculating throughput itself, we use the [`scheduler_schedule_attempts_total` metric](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L597).

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-16T11:24:00Z

> kube-scheduler perf tests ([scheduler_perf](https://github.com/kubernetes/kubernetes/tree/master/test/integration/scheduler_perf)) verify only the scheduling throughput, without checking cpu/memory usage.

So, I think we don't need it either.

> Code that calculates the throughput is [here](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L468-L615). It is done using [event handler subscribed on Pod/Add and Pod/Update events](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L486-L511). For statistical purposes, and not for calculating throughput itself, we use the [scheduler_schedule_attempts_total metric](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L597).

I would say that we also measure throughput in our tests, where ` maxWallMs` is a proxy, and more granual is `wlClassesMaxAvgTimeToAdmissionMs`. 

Probably we also don't need then cmd.maxrss and `clusterQueueClassesMinUsage` (though we haven't had flakes with them yet. WDYT @tenzen-y ?

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-04-18T09:27:25Z

> > kube-scheduler perf tests ([scheduler_perf](https://github.com/kubernetes/kubernetes/tree/master/test/integration/scheduler_perf)) verify only the scheduling throughput, without checking cpu/memory usage.
> 
> So, I think we don't need it either.
> 
> > Code that calculates the throughput is [here](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L468-L615). It is done using [event handler subscribed on Pod/Add and Pod/Update events](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L486-L511). For statistical purposes, and not for calculating throughput itself, we use the [scheduler_schedule_attempts_total metric](https://github.com/kubernetes/kubernetes/blob/44c230bf5c321056e8bc89300b37c497f464f113/test/integration/scheduler_perf/util.go#L597).
> 
> I would say that we also measure throughput in our tests, where ` maxWallMs` is a proxy, and more granual is `wlClassesMaxAvgTimeToAdmissionMs`.
> 
> Probably we also don't need then cmd.maxrss and `clusterQueueClassesMinUsage` (though we haven't had flakes with them yet. WDYT [@tenzen-y](https://github.com/tenzen-y) ?

I synced with @mimowo offline. In conclusion, we agree with dropping the assertion based on the threshold for CPU and memory usage.
However, we keep collecting those metrics during CI and push the result to artifacts since those are still useful to evaluate Kueue project.

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-04-22T09:20:51Z

/assign

### Comment by [@mimowo](https://github.com/mimowo) — 2025-04-24T10:24:21Z

new occurrence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/4989/pull-kueue-test-scheduling-perf-main/1915345602112131072
