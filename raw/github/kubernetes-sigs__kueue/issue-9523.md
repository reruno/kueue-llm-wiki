# Issue #9523: Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay]

**Summary**: Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay]

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/9523

**Last updated**: 2026-03-27T12:46:50Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2026-02-26T13:44:38Z
- **Updated**: 2026-03-27T12:46:50Z
- **Closed**: 2026-03-27T12:46:50Z
- **Labels**: `kind/bug`, `kind/flake`
- **Assignees**: _none_
- **Comments**: 13

## Description

<!--
Please use this template for reporting flaky tests.
Links to specific failures in Prow are appreciated.
-->

**Which test is flaking?**:
] Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay]
**Link to failed CI job or steps to reproduce locally**:
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9521/pull-kueue-test-e2e-main-1-33/2027007885115920384
https://prow.k8s.io/view/gs/kubernetes-ci-logs/pr-logs/pull/kubernetes-sigs_kueue/9521/pull-kueue-test-e2e-main-1-34/2027007885233360896
**Failure message or logs**:
```

End To End Suite: kindest/node:v1.33.7: [It] Kuberay Should run a rayjob with InTreeAutoscaling [area:singlecluster, feature:kuberay] expand_less	6m10s
{Timed out after 300.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/kuberay_test.go:334 with:
Expected exactly 5 pods with 'workers' in the name
Expected
    <[]string | len:0, cap:0>: nil
to have length 5 failed [FAILED] Timed out after 300.001s.
The function passed to Eventually failed at /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/kuberay_test.go:334 with:
Expected exactly 5 pods with 'workers' in the name
Expected
    <[]string | len:0, cap:0>: nil
to have length 5
In [It] at: /home/prow/go/src/sigs.k8s.io/kueue/test/e2e/singlecluster/kuberay_test.go:342 @ 02/26/26 13:33:38.392
}
```

**Anything else we need to know?**:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-05T10:15:25Z

FYI @sohankunkerkar analyzed the issue, and we are now thinking how to solve it. The discussion is currently there: https://github.com/kubernetes-sigs/kueue/pull/9570#discussion_r2889031059.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-19T11:12:45Z

Folks, as we have the annotation with the PodSet sizes added in https://github.com/kubernetes-sigs/kueue/pull/9726, can we follow up with the bugfix, wdyt? cc @sohankunkerkar @hiboyang

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-03-19T20:35:29Z

/assign @PannagaRao

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-03-20T00:32:02Z

I have this PR https://github.com/kubernetes-sigs/kueue/pull/9960, it might fix this test issue

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-03-20T16:48:29Z

Thanks @hiboyang for picking this up with #9960! I'll review that PR instead of duplicating the effort.

### Comment by [@PannagaRao](https://github.com/PannagaRao) — 2026-03-20T16:49:01Z

/unassign

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-24T07:45:02Z

@sohankunkerkar we already have the fix PR which takes into consideration also thee generation of the RayCluster, ptal: https://github.com/kubernetes-sigs/kueue/pull/9960

One thing I'm not yet certain based on the analysis in https://github.com/kubernetes-sigs/kueue/pull/9570#discussion_r2870525278 is why it would even work sometimes, or most of the time. I would expect that if generation of the RayJob is not changing during autoscaling then the test would fail consistently. Do  you know the answer @sohankunkerkar or @hiboyang ?

### Comment by [@sohankunkerkar](https://github.com/sohankunkerkar) — 2026-03-24T10:04:42Z

After scanning through the logs again, I suspect when Kueue admits the RayJob, its generation bumps from 1→2. The first scale-up after admission works because `newWorkloadName` hashes gen=2, which differs from the initial workload's gen=1. But subsequent scale-ups only touch the RayCluster, not the RayJob itself, so gen stays at 2 and the hash collides with the existing workload. It flakes because the Ray autoscaler in aggressive mode usually jumps 1→5 directly (one scale-up after the gen bump = works), but under CI load sometimes goes 1→3→5 and that second step hits the `AlreadyExists` loop.

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-03-24T16:39:29Z

@sohankunkerkar , thanks for the investigation and information! PR https://github.com/kubernetes-sigs/kueue/pull/9960 should fix this issue now.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-25T07:26:29Z

Thank you for the analysis @sohankunkerkar. One missing piece I wanted to establish is why does this work at all when scaling 1->5 directly, ie. why the second workload corresponding to size 5 is created since no generation change. After running the test locally I discovered the generation is changed, because the first generated workload corresponds to RayJob with still `suspend: true`. So once the RayJob is unsuspended the generation is bumped, but the new workload creation is skipped because sizes are the same. Still, the update to the RayJob status triggers new workload creation later on when the PodSet sizes change. 

This also explains why the double scale up (like 1->3->5) is broken. I'm wondering if we could put the tasks into the RayJob queue in two steps to make that scaling more likely.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-25T08:16:14Z

Ok so I was able to make the issue more reproducible with the following task:

```
import os

ray.init()

# Explicitly request 1 CPU per task to ensure deterministic resource demand.
# Without num_cpus, Ray may detect high logical CPU count from the host
# and not trigger autoscaling.
@ray.remote(num_cpus=1)
def my_task(x, s):
    import time
    time.sleep(s)
    return x * x

# run tasks in sequence to avoid triggering autoscaling in the beginning
print([ray.get(my_task.remote(i, 1)) for i in range(4)])

# run tasks in with low parallelism to trigger autoscaling (scaling up)
# but to still not scale up to the max size
print(ray.get([my_task.remote(i, 8) for i in range(4)]))

# run tasks in parallel to trigger autoscaling (scaling up)
# Use longer sleep (8s) to give autoscaler time to detect demand,
# create workload slices, and schedule new workers.
print(ray.get([my_task.remote(i, 8) for i in range(16)]))

# run tasks in sequence to trigger scaling down
print([ray.get(my_task.remote(i, 1)) for i in range(32)])`,
```

However after running on the new branch I see the issue remains:

```
❯ k get pods -nkuberay-e2e-zmr7r
NAME                                                    READY   STATUS            RESTARTS   AGE
rayjob-autoscaling-8xn94-head-jptvb                     2/2     Running           0          2m29s
rayjob-autoscaling-8xn94-workers-group-0-worker-65hbj   0/1     Running           0          39s
rayjob-autoscaling-8xn94-workers-group-0-worker-dbv2s   0/1     Running           0          39s
rayjob-autoscaling-8xn94-workers-group-0-worker-h4jr9   1/1     Running           0          2m29s
rayjob-autoscaling-8xn94-workers-group-0-worker-kqjvh   0/1     SchedulingGated   0          19s
rayjob-autoscaling-8xn94-workers-group-0-worker-nfk22   0/1     SchedulingGated   0          19s
rayjob-autoscaling-c5vx2                                1/1     Running           0          100s
```

I don't yet know why, but it seems the second scale up remains broken. I can see many logs like
```
2026-03-25T07:52:06.900921717Z	LEVEL(-2)	rayjob	jobframework/reconciler.go:424	Reconciling Job	{"replica-role": "leader", "namespace": "kuberay-e2e-zmr7r", "name": "rayjob-autoscaling", "reconcileID": "e9ce2696-11fd-4e5e-a09f-1b8533253316", "job": "kuberay-e2e-zmr7r/rayjob-autoscaling", "gvk": "ray.io/v1, Kind=RayJob"}
2026-03-25T07:52:06.900977157Z	LEVEL(-2)	rayjob	raycluster/common.go:138	Updated PodSet worker count from RayCluster	{"replica-role": "leader", "namespace": "kuberay-e2e-zmr7r", "name": "rayjob-autoscaling", "reconcileID": "e9ce2696-11fd-4e5e-a09f-1b8533253316", "job": "kuberay-e2e-zmr7r/rayjob-autoscaling", "gvk": "ray.io/v1, Kind=RayJob", "rayObject": "rayjob-autoscaling", "rayCluster": "rayjob-autoscaling-8xn94", "workerGroup": "workers-group-0", "oldCount": 1, "newCount": 5}
2026-03-25T07:52:06.901055087Z	LEVEL(-3)	rayjob	jobframework/reconciler.go:506	The workload is nil, handle job with no workload	{"replica-role": "leader", "namespace": "kuberay-e2e-zmr7r", "name": "rayjob-autoscaling", "reconcileID": "e9ce2696-11fd-4e5e-a09f-1b8533253316", "job": "kuberay-e2e-zmr7r/rayjob-autoscaling", "gvk": "ray.io/v1, Kind=RayJob"}
2026-03-25T07:52:06.901101797Z	LEVEL(-2)	rayjob	raycluster/common.go:138	Updated PodSet worker count from RayCluster	{"replica-role": "leader", "namespace": "kuberay-e2e-zmr7r", "name": "rayjob-autoscaling", "reconcileID": "e9ce2696-11fd-4e5e-a09f-1b8533253316", "job": "kuberay-e2e-zmr7r/rayjob-autoscaling", "gvk": "ray.io/v1, Kind=RayJob", "rayObject": "rayjob-autoscaling", "rayCluster": "rayjob-autoscaling-8xn94", "workerGroup": "workers-group-0", "oldCount": 1, "newCount": 5}
2026-03-25T07:52:06.941625825Z	LEVEL(-3)	rayjob	jobframework/reconciler.go:510	Handling job with no workload found an existing workload	{"replica-role": "leader", "namespace": "kuberay-e2e-zmr7r", "name": "rayjob-autoscaling", "reconcileID": "e9ce2696-11fd-4e5e-a09f-1b8533253316", "job": "kuberay-e2e-zmr7r/rayjob-autoscaling", "gvk": "ray.io/v1, Kind=RayJob"}
2026-03-25T07:52:06.941813305Z	LEVEL(-3)	rayjob	jobframework/reconciler.go:804	stop walking up as the owner is not found	{"replica-role": "leader", "namespace": "kuberay-e2e-zmr7r", "name": "rayjob-autoscaling", "reconcileID": "bd86ab1f-e4f7-446a-8657-40b96aaebf1a", "job": "kuberay-e2e-zmr7r/rayjob-autoscaling", "gvk": "ray.io/v1, Kind=RayJob", "currentObj": {"name":"rayjob-autoscaling","namespace":"kuberay-e2e-zmr7r"}}
```
The direction in https://github.com/kubernetes-sigs/kueue/pull/9960 is probably ok because at least we can get the generations right, but the issue from user perspective remains, and so I think the flake would remain. Let's investigate what is missing here.

cc @hiboyang @sohankunkerkar

### Comment by [@hiboyang](https://github.com/hiboyang) — 2026-03-25T16:05:13Z

Thanks for the finding @mimowo! Let me add a new e2e test based on your RayJob script and do more testing.

### Comment by [@mimowo](https://github.com/mimowo) — 2026-03-25T16:51:53Z

@hiboyang @sohankunkerkar I don't fully know the problem but I think since we have the annotations with the RayCluster size maybe we should read those first as the source of trouth.
