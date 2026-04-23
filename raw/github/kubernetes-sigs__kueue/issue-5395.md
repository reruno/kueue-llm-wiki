# Issue #5395: [flaky integration test] Preemption is enabled within ClusterQueue should preempt the low and mid priority workloads to fit the high-priority workload

**Summary**: [flaky integration test] Preemption is enabled within ClusterQueue should preempt the low and mid priority workloads to fit the high-priority workload

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/5395

**Last updated**: 2025-06-05T11:38:44Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-05-28T09:29:11Z
- **Updated**: 2025-06-05T11:38:44Z
- **Closed**: 2025-06-05T11:38:44Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: [@mszadkow](https://github.com/mszadkow)
- **Comments**: 20

## Description

/kind flake 

**What happened**:

failure on unrelated branch https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5394/pull-kueue-test-integration-baseline-main/1927649254336106496

**What you expected to happen**:
no failure
**How to reproduce it (as minimally and precisely as possible)**:
ci
**Anything else we need to know?**:

```
TopologyAwareScheduling Suite: [It] Topology Aware Scheduling when Single TAS Resource Flavor when Preemption is enabled within ClusterQueue should preempt the low and mid priority workloads to fit the high-priority workload expand_less	13s
{Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:365 with:
Not enough workloads are admitted
Expected
    <int>: 1
to equal
    <int>: 2 failed [FAILED] Timed out after 10.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/util/util.go:365 with:
Not enough workloads are admitted
Expected
    <int>: 1
to equal
    <int>: 2
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/integration/singlecluster/tas/tas_test.go:1374 @ 05/28/25 09:06:47.971
}
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-28T09:31:24Z

cc @mbobrovskyi @mykysha ptal

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-05-30T06:01:37Z

We observed the same failure on #5416, again.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T06:06:50Z

cc @mszadkow

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-30T06:56:27Z

/assign

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-30T11:49:39Z

Something very strange happened in that test run.
`wl1` got admitted and later it was verified, when `wl2` was evaluated for admission `wl1` disappeared without a trace...
What I mean is there was no `delete` or `preemption` recorded, maybe just this attempt to preempt `wl1` which meanwhile disappear.
 
```
2025-05-28T09:06:37.97242884Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:226	Attempting to schedule workload	{"schedulingCycle": 38, "workload": {"name":"wl2","namespace":"tas-94dv5"}, "clusterQueue": {"name":"cluster-queue"}}
  2025-05-28T09:06:37.975342209Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:572	Workload not admitted because it was deleted	{"schedulingCycle": 37, "workload": {"name":"wl1","namespace":"tas-7vrc8"}, "clusterQueue": {"name":"cluster-queue"}}
  2025-05-28T09:06:37.978364299Z	ERROR	scheduler	scheduler/scheduler.go:268	Failed to preempt workloads	{"schedulingCycle": 38, "workload": {"name":"wl2","namespace":"tas-94dv5"}, "clusterQueue": {"name":"cluster-queue"}, "error": "workloads.kueue.x-k8s.io \"wl1\" not found"}
  sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule
  	/home/prow/go/src/sigs.k8s.io/kueue/pkg/scheduler/scheduler.go:268
  sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1
  	/home/prow/go/src/sigs.k8s.io/kueue/pkg/util/wait/backoff.go:43
  k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1
  	/home/prow/go/src/sigs.k8s.io/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233
  k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1
  	/home/prow/go/src/sigs.k8s.io/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255
  k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext
  	/home/prow/go/src/sigs.k8s.io/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256
  k8s.io/apimachinery/pkg/util/wait.BackoffUntil
  	/home/prow/go/src/sigs.k8s.io/kueue/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233
  sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff
  	/home/prow/go/src/sigs.k8s.io/kueue/pkg/util/wait/backoff.go:42
  sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff
  	/home/prow/go/src/sigs.k8s.io/kueue/pkg/util/wait/backoff.go:34
  2025-05-28T09:06:37.978562602Z	LEVEL(-3)	scheduler	scheduler/logging.go:43	Workload evaluated for admission	{"schedulingCycle": 38, "workload": {"name":"wl2","namespace":"tas-94dv5"}, "clusterQueue": {"name":"cluster-queue"}, "status": "", "reason": "couldn't assign flavors to pod set worker: topology \"default\" doesn't allow to fit any of 1 pod(s)"}
```

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T11:55:44Z

Could you try to repro locally by looping the test under some load? Maybe we could capture it locally.

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-05-30T12:06:33Z

I have tried already, nothing happens, works smoothly.
But I will keep trying, I just wanted to share this "weird" thing that `wl1` namespace somehow got changed.
From `tas-94dv5` to `tas-7vrc8`, which is from the previous test case...

```
  2025-05-28T09:06:37.710423748Z	LEVEL(-2)	workload-reconciler	core/workload_controller.go:747	Workload update event	{"workload": {"name":"wl1","namespace":"tas-94dv5"}, "queue": "local-queue", "status": "admitted", "prevStatus": "pending", "clusterQueue": "cluster-queue"}
...
2025-05-28T09:06:37.975342209Z	LEVEL(-2)	scheduler	scheduler/scheduler.go:572	Workload not admitted because it was deleted	{"schedulingCycle": 37, "workload": {"name":"wl1","namespace":"tas-7vrc8"}, "clusterQueue": {"name":"cluster-queue"}}
```
My suspect is that we share lq and cq as pointers between tests...
But I would like to get repro anyway

### Comment by [@mimowo](https://github.com/mimowo) — 2025-05-30T12:21:15Z

Thank you for investigating that. Indeed, I don't exclude the possibility of cross-test interaction, this would be hard to capture. Even if you are out of ideas for now, please think if we could improve the logging (either in tests) or in code which could be helpful next time.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-02T07:51:01Z

another recent occurence: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5433/pull-kueue-test-integration-baseline-release-0-12/1929436649175912448

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-06-02T08:28:01Z

Yes, I believe the fix is ready to be merged - https://github.com/kubernetes-sigs/kueue/pull/5423

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-02T11:04:36Z

Looks like we still have an issue https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5443/pull-kueue-test-integration-baseline-main/1929489390048907264.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-02T11:04:40Z

/reopen

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-06-02T11:04:45Z

@mbobrovskyi: Reopened this issue.

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/5395#issuecomment-2930073887):

>/reopen


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2025-06-02T11:10:42Z

One more

https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5225/pull-kueue-test-integration-baseline-main/1929477214840033280

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-06-02T11:17:03Z

ack, looking into logs

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-02T11:28:30Z

same here: https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5440/pull-kueue-test-integration-baseline-main/1929495861822230528

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-06-02T15:37:30Z

The next suspect is the `queue manager` as it seems that `wl1` from the previous test is considered for preemption.
While it should be `wl1` from the current test and `wl1` from previous test should be removed from the queue already.
Investigating there...although still it's not possible to reproduce locally.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-06-02T16:20:51Z

Hmm, this might be a bug related to this code: https://github.com/kubernetes-sigs/kueue/blob/e3bbc66fa7c95df49668a33934e9ae9c97d9b65a/pkg/queue/manager.go#L793-L795

It might be the goroutine is spawned to add the workload after 1s and it does not consider the context is already cancelled when test ended.

Another fix might be to do not enqueue if the CQ no longer exists. 

To test this hypothesis locally maybe you could extend 1s to 2s.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T04:11:35Z

We observed this again.

https://github.com/kubernetes-sigs/kueue/pull/5432
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5432/pull-kueue-test-integration-baseline-main/1930110922383167488

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-04T04:54:16Z

Once more:

- https://github.com/kubernetes-sigs/kueue/pull/5491
- https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/5491/pull-kueue-test-integration-baseline-release-0-12/1930119799250096128
