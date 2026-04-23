# Issue #6486: TAS: Kueue crashes with panic when PodSet count is 0

**Summary**: TAS: Kueue crashes with panic when PodSet count is 0

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6486

**Last updated**: 2025-08-11T11:31:07Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2025-08-06T16:58:18Z
- **Updated**: 2025-08-11T11:31:07Z
- **Closed**: 2025-08-11T11:31:07Z
- **Labels**: `kind/bug`
- **Assignees**: [@mimowo](https://github.com/mimowo)
- **Comments**: 6

## Description

**What happened**:

On using 0.13.1, but probably also older versions Kueue may crash with the logs: 

```
E0805 20:13:04.320850       1 panic.go:241] "Observed a panic" panic="runtime error: integer divide by zero" panicGoValue="\"integer divide by zero\"" stacktrace=<
    goroutine 1178 [running]:
    k8s.io/apimachinery/pkg/util/runtime.logPanic({0x34475f0, 0xc00205d7d0}, {0x2a4c520, 0x4fc9130})
        /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:132 +0xbc
    k8s.io/apimachinery/pkg/util/runtime.handleCrash({0x3448fe0, 0xc000c0a930}, {0x2a4c520, 0x4fc9130}, {0x0, 0x0, 0x440fe0?})
        /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:107 +0x116
    k8s.io/apimachinery/pkg/util/runtime.HandleCrashWithContext({0x3448fe0, 0xc000c0a930}, {0x0, 0x0, 0x0})
        /workspace/vendor/k8s.io/apimachinery/pkg/util/runtime/runtime.go:78 +0x5a
    panic({0x2a4c520?, 0x4fc9130?})
        /usr/local/go/src/runtime/panic.go:787 +0x132
    sigs.k8s.io/kueue/pkg/resources.Requests.Divide(...)
        /workspace/pkg/resources/requests.go:61
    sigs.k8s.io/kueue/pkg/resources.Requests.ScaledDown(...)
        /workspace/pkg/resources/requests.go:55
    sigs.k8s.io/kueue/pkg/workload.(*PodSetResources).SinglePodRequests(0x5062da0?)
        /workspace/pkg/workload/workload.go:200 +0x10a
    sigs.k8s.io/kueue/pkg/scheduler/flavorassigner.podSetTopologyRequest(0xc0012c2de0, 0xc000a901e0, 0xc00186a280, 0x1, 0x1)
        /workspace/pkg/scheduler/flavorassigner/tas_flavorassigner.go:81 +0xcb
    sigs.k8s.io/kueue/pkg/scheduler/flavorassigner.(*Assignment).WorkloadsTopologyRequests(0xc0005d2760, 0xc000a901e0, 0xc00186a280)
        /workspace/pkg/scheduler/flavorassigner/tas_flavorassigner.go:48 +0x39b
    sigs.k8s.io/kueue/pkg/scheduler/flavorassigner.(*FlavorAssigner).assignFlavors(0xc0005d2f30, {{0x3453070?, 0xc00205d1a0?}, 0x2fd7f77?}, {0x0?, 0xc0004aa240?, 0x20000000037ea80?})
        /workspace/pkg/scheduler/flavorassigner/flavorassigner.go:576 +0xd12
    sigs.k8s.io/kueue/pkg/scheduler/flavorassigner.(*FlavorAssigner).Assign(0xc000b3cb40?, {{0x3453070?, 0xc00205d1a0?}, 0x2703451?}, {0x0?, 0x0?, 0x7f?})
        /workspace/pkg/scheduler/flavorassigner/flavorassigner.go:453 +0x2ba
    sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).getInitialAssignments(0xc00058a6e0, {{0x3453070?, 0xc00205d1a0?}, 0x2184697?}, 0xc000a901e0, 0xc0017417a0)
        /workspace/pkg/scheduler/scheduler.go:529 +0x205
    sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).getAssignments(0xc000a4edc0?, {{0x3453070?, 0xc00205d1a0?}, 0xc0005d34b8?}, 0xc000a901e0, 0xc0017417a0)
        /workspace/pkg/scheduler/scheduler.go:495 +0xa5
    sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).nominate(0xc00058a6e0, {0x34475f0, 0xc001741620}, {0xc001868b40, 0x1, 0x0?}, 0xc0017417a0)
        /workspace/pkg/scheduler/scheduler.go:431 +0xb4e
    sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule(0xc00058a6e0, {0x34475f0, 0xc001741560})
        /workspace/pkg/scheduler/scheduler.go:221 +0x3d3
    sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1()
        /workspace/pkg/util/wait/backoff.go:43 +0x2b
    k8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1({0x156d0d6?, 0xc0003bee70?})
        /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233 +0x13
    k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext.func1({0x3448fe0?, 0xc000c0a930?}, 0x486459?)
        /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:255 +0x51
    k8s.io/apimachinery/pkg/util/wait.BackoffUntilWithContext({0x3448fe0, 0xc000c0a930}, 0xc0005d3ee8, {0x340f9a0, 0xc0014cf728}, 0x0)
        /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:256 +0xe5
    k8s.io/apimachinery/pkg/util/wait.BackoffUntil(0xc0016d7f38?, {0x340f9a0?, 0xc0014cf728?}, 0xc0?, 0x0?)
        /workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:233 +0x46
    sigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff({0x34475f0, 0xc001741560}, 0xc001451dd0, {0x343bd90, 0xc0004be3b0})
        /workspace/pkg/util/wait/backoff.go:42 +0xd3
    sigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff({0x34475f0, 0xc001741560}, 0xc001451dd0)
        /workspace/pkg/util/wait/backoff.go:34 +0x8c
    created by sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).Start in goroutine 1174
        /workspace/pkg/scheduler/scheduler.go:162 +0x131
```

**What you expected to happen**:

No crash for sure. 

Probably we should admit the workload, following what quota-only Kueue does without TAS.

**How to reproduce it (as minimally and precisely as possible)**:

1. Enable Topology AwareScheduling
2. Create the following LWS:

```yaml
apiVersion: leaderworkerset.x-k8s.io/v1
kind: LeaderWorkerSet
metadata:
  name: leaderworkerset-multi-template
  labels:
    kueue.x-k8s.io/queue-name: tas-user-queue
spec:
  replicas: 1
  leaderWorkerTemplate:
    leaderTemplate:
      spec:
        containers:
        - name: nginx2
          image: nginx:1.14.2
          resources:
            limits:
              cpu: "100m"
            requests:
              cpu: "50m"
          ports:
          - containerPort: 8080
    size: 1
    workerTemplate:
      spec:
        containers:
        - name: nginx
          image: nginx:1.14.2
          resources:
            limits:
              cpu: "100m"
            requests:
              cpu: "50m"
          ports:
          - containerPort: 8080
```

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T16:58:30Z

cc @mwysokin

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-06T16:59:00Z

@lchrzaszcz

### Comment by [@mwysokin](https://github.com/mwysokin) — 2025-08-06T17:05:19Z

Yep, I just checked with 0.12 and it happens also.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-08T09:39:57Z

/assign
seems like a fun and useful quick fix before vacation :)

### Comment by [@ichekrygin](https://github.com/ichekrygin) — 2025-08-08T18:11:10Z

Is it a valid assumption that this impacts configuration with multiple pod sets?
I couldn't reproduce it with a single pod set.

### Comment by [@mimowo](https://github.com/mimowo) — 2025-08-11T11:12:09Z

> Is it a valid assumption that this impacts configuration with multiple pod sets?
I couldn't reproduce it with a single pod set.

It can be reproduced for Job with single PodSet, for example this JobSet:

```yaml
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  name: example
  labels:
    kueue.x-k8s.io/queue-name: tas-user-queue
spec:
  suspend: true
  successPolicy:
    operator: All 
    targetReplicatedJobs:
    - main
  replicatedJobs:
  - name: main
    replicas: 0
    template:
      spec:
        completions: 1
        parallelism: 1
        template:
          metadata:
            annotations:
              kueue.x-k8s.io/podset-preferred-topology: "kubernetes.io/hostname"
          spec:
            containers:
            - name: leader
              image: bash:latest
              command: ["bash", "-xc", "sleep 10000"]
              resources:
                requests:
                  cpu: 1
```
