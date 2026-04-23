# Issue #7172: [flaky integration test] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited

**Summary**: [flaky integration test] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/7172

**Last updated**: 2025-10-16T10:20:47Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-10-06T08:56:10Z
- **Updated**: 2025-10-16T10:20:47Z
- **Closed**: 2025-10-16T10:20:46Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@IrvingMg](https://github.com/IrvingMg)
- **Comments**: 12

## Description

/kind flake

**What happened**:

failed on periodic build from "main" branch: https://prow.k8s.io/view/gs/kubernetes-ci-logs/logs/periodic-kueue-test-integration-main/1974547138524221440

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:
```
Scheduler Fair Sharing Suite: [It] Scheduler when Using AdmissionFairSharing at ClusterQueue level admits one workload from each LocalQueue when quota is limited expand_less	17s
{Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:366 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1 failed [FAILED] Timed out after 10.000s.
The function passed to Eventually failed at /home/prow/go/src/kubernetes-sigs/kueue/test/util/util.go:366 with:
Not enough workloads are admitted
Expected
    <int>: 0
to equal
    <int>: 1
In [It] at: /home/prow/go/src/kubernetes-sigs/kueue/test/integration/singlecluster/scheduler/fairsharing/fair_sharing_test.go:717 @ 10/04/25 19:06:54.077
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-06T08:56:56Z

cc @PBundyra @IrvingMg ptal, maybe the AFS logs we added can help to understand the issue

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-06T10:01:28Z

/assign

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-14T08:27:28Z

This issue is hard to reproduce. I’ve run the test several times, but I haven’t been able to catch it on my local. The only way I’ve seen it happen is by lowering the values of the usage parameters.

However, we talked before about using small values: https://github.com/kubernetes-sigs/kueue/pull/5933#issuecomment-3117543330. In that discussion, it was suggested that small values might cause the penalty to decrease very quickly.

Right now, we are using 1 second for both `UsageHalfLifeTime` and `UsageSamplingInterval`. I think that the bigger these values are, the less likely the error will happen.

I’m not sure if using very small values is an edge case. But if it is, maybe we need to improve how penalties, usage calculation, and admissions work together.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-14T08:57:53Z

cc @PBundyra wdyt?

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-14T09:03:36Z

@IrvingMg can we establish based on the log analysis which workloads, from which LQ / CQ where admitted / preempted during execution of he test?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2025-10-14T09:17:54Z

Looking at my comment back then I proposed 1s interval and 10s half-life. Now I see that in code some tests use 1s interval+1 half-life and some use 1s interval+10 half-life. Let's be consistent and use 10s half-life everywhere. @IrvingMg please update the half life and run this particular test ~200 times

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-14T11:31:42Z

> [@IrvingMg](https://github.com/IrvingMg) can we establish based on the log analysis which workloads, from which LQ / CQ where admitted / preempted during execution of he test?

Yes, for context: we start by filling the ClusterQueue with one workload per LocalQueue (lq-a and lq-b), both requesting the same amount of resources. Then we create two more workloads per queue, which stay pending until resources become available.

Before finishing any workloads:
- `lq-a` usage: 3939m
- `lq-b` usage: 3982m
```
2025-10-04T19:06:44.009357565Z  LEVEL(-3)  localqueue-reconciler  core/localqueue_controller.go:310  
Updated LocalQueue fair sharing status  {"namespace": "core-6n6tl", "name": "lq-a", "consumedResources": {"cpu":"3939m"}}

2025-10-04T19:06:44.041732951Z  LEVEL(-3)  localqueue-reconciler  core/localqueue_controller.go:310  
Updated LocalQueue fair sharing status  {"namespace": "core-6n6tl", "name": "lq-b", "consumedResources": {"cpu":"3982m"}}
```

Then, we finish one workload per LocalQueue:

```
2025-10-04T19:06:44.046561562Z  LEVEL(-2)  workload-reconciler  core/workload_controller.go:812  
Workload update event  {"workload": {"name":"workload-rs75t","namespace":"core-6n6tl"}, "queue": "lq-a", "status": "finished", "prevStatus": "admitted", "prevClusterQueue": "cq1"}

2025-10-04T19:06:44.069377087Z  LEVEL(-2)  workload-reconciler  core/workload_controller.go:812  
Workload update event  {"workload": {"name":"workload-jf7vc","namespace":"core-6n6tl"}, "queue": "lq-b", "status": "finished", "prevStatus": "admitted", "prevClusterQueue": "cq1"}
```

But usage still shows:
- `lq-a` usage: 3.939
- `lq-b` usage: 3.982
```
2025-10-04T19:06:44.070378709Z  LEVEL(-3)  cluster-queue-reconciler  queue/cluster_queue.go:478  
Resource usage from LocalQueue  {"clusterQueue": {"name":"cq1"}, "LocalQueue": "lq-a", "Usage": 3.939}

2025-10-04T19:06:44.07046112Z  LEVEL(-3)  cluster-queue-reconciler  queue/cluster_queue.go:479  
Resource usage from LocalQueue  {"clusterQueue": {"name":"cq1"}, "LocalQueue": "lq-b", "Usage": 3.982}
```

Then, this workload from `lq-a` is admitted:

```
2025-10-04T19:06:44.069116554Z  LEVEL(-2)  scheduler  scheduler/scheduler.go:652  
Workload successfully admitted and assigned flavors  {"schedulingCycle": 337, "workload": {"name":"workload-nnvk7","namespace":"core-6n6tl"}, "clusterQueue": {"name":"cq1"}, "assignments": [{"name":"main","flavors":{"cpu":"default"},"resourceUsage":{"cpu":"4"},"count":1}]}
```

And another from `lq-a` right after:
```
2025-10-04T19:06:44.089376178Z  LEVEL(-2)  scheduler  scheduler/scheduler.go:652  
Workload successfully admitted and assigned flavors  {"schedulingCycle": 341, "workload": {"name":"workload-mkktx","namespace":"core-6n6tl"}, "clusterQueue": {"name":"cq1"}, "assignments": [{"name":"main","flavors":{"cpu":"default"},"resourceUsage":{"cpu":"4"},"count":1}]}
```

After both admissions, usage is finally updated to:
- `lq-a` usage: 8073m
- `lq-b` usage: 1932m
```
2025-10-04T19:06:44.097280637Z  LEVEL(-3)  localqueue-reconciler  core/localqueue_controller.go:310  
Updated LocalQueue fair sharing status  {"namespace": "core-6n6tl", "name": "lq-a", "consumedResources": {"cpu":"8073m"}}

2025-10-04T19:06:45.043253772Z  LEVEL(-3)  localqueue-reconciler  core/localqueue_controller.go:310  
Updated LocalQueue fair sharing status  {"namespace": "core-6n6tl", "name": "lq-b", "consumedResources": {"cpu":"1932m"}}
```

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-14T11:42:50Z

> Looking at my comment back then I proposed 1s interval and 10s half-life. Now I see that in code some tests use 1s interval+1 half-life and some use 1s interval+10 half-life. Let's be consistent and use 10s half-life everywhere. [@IrvingMg](https://github.com/IrvingMg) please update the half life and run this particular test ~200 times

Okay, I'm running with a 5s half-life. (Using 10s causes a timeout issue in the following assertion:

`util.ExpectLocalQueueFairSharingUsageToBe(ctx, k8sClient, client.ObjectKeyFromObject(lqA), ">", 3_900).)`

However, I'm wondering how we can estimate a proper minimum value for these parameters. I ran the tests over 200 times with 1s for both parameters, but I couldn’t reproduce the failure locally.

So, I would assume that with 5s the error shouldn’t happen either, but I'm not sure which values are truly safe to avoid failures like the one we’re seeing in the periodic build.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-14T11:59:46Z

@IrvingMg @PBundyra thank you for looking int this. I'm also thinking that some issue may be stemming from using this metric: ExpectReservingActiveWorkloadsMetric, as it is bumped before the request for "Admission" actually succeeds. We have a discovered and fixed flake due to this: https://github.com/kubernetes-sigs/kueue/pull/7155

Could you maybe Irving submit a PR which starts to use ExpectAdmittedWorkloadsTotalMetric consistently whenever possible?

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-15T16:49:47Z

> Could you maybe Irving submit a PR which starts to use ExpectAdmittedWorkloadsTotalMetric consistently whenever possible?

Open #7281

### Comment by [@IrvingMg](https://github.com/IrvingMg) — 2025-10-16T10:20:41Z

/close

Closing this issue for now. Let's see if the test flakes again after #7281.

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-10-16T10:20:47Z

@IrvingMg: Closing this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/7172#issuecomment-3410185883):

>/close
>
>Closing this issue for now. Let's see if the test flakes again after #7281.


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
