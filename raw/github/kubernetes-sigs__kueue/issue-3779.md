# Issue #3779: Infinite preemption loop in fair sharing

**Summary**: Infinite preemption loop in fair sharing

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3779

**Last updated**: 2025-03-07T19:37:46Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@yuvalaz99](https://github.com/yuvalaz99)
- **Created**: 2024-12-09T23:18:57Z
- **Updated**: 2025-03-07T19:37:46Z
- **Closed**: 2025-03-07T19:37:46Z
- **Labels**: `kind/bug`
- **Assignees**: [@gabesaba](https://github.com/gabesaba), [@vladikkuzn](https://github.com/vladikkuzn)
- **Comments**: 17

## Description

**What happened**:

An infinite preemption loop occurs in a hierarchical cohort scenario with Kueue's Pod integration.
When a higher-priority workload preempts a lower-priority one from a different queue, the Deployment controller recreates the preempted workload, causing it to be readmitted. 
Once readmitted, the preemption occurs again, triggering this infinite loop.

I'll show an edge case where this infinite preemption behavior occurs. Not all preemption operations using hierarchical cohorts behave in this way.

Cohort Structure
--- Cohort Root (NM: 0m)
-------- Cohort Guaranteed (NM: 300m)
------------- Clusterqueue Guaranteed (NM: 0m)
-------- ClusterQueue BestEffortTenantA (NM: 0m)
--------  ClusterQueue BestEffortTenantB (NM: 0m)

Event Sequence Leading to the Issue
   1. BestEffortTenantA1 (100m) admitted
   2. BestEffortTenantA2 (100m) admitted
   3. BestEffortTenantB1 (50m) admitted
   4. BestEffortTenantB2 (50m) admitted
   5. Guaranteed1 (50m) created → preempts BestEffortTenantA2
   6. Guaranteed1 (50m) admitted
   7. Guaranteed2 (100m) created → triggers infinite loop:
      - BestEffortTenantB2 preempted
      - Guaranteed2 remains SchedulingGated
      - BestEffortTenantB2 recreated by Deployment
      - BestEffortTenantB2 admitted
      - Loop repeats
   8. After a few minutes, BestEffortTenantB2 resumes running without being preempted, while Guaranteed2 remains in the SchedulingGated state.
      
 -------------------------------------------------------
  
Pods status

```
> kubectl get pods
NAME                                        READY   STATUS            RESTARTS   AGE
best-effort-tenant-a-1-5576db6f68-nms98     1/1     Running           0          55s
best-effort-tenant-a-2-695bd7b4c-b5n4l      0/1     SchedulingGated   0          43s
best-effort-tenant-b-1-68596f9f8b-52p5z     1/1     Running           0          50s
best-effort-tenant-b-2-69dc4f5797-l4vq6     0/1     Terminating       0          5s
best-effort-tenant-b-2-69dc4f5797-l4vq6     0/1     SchedulingGated   0          2s
guaranteed-1-7c96f8db5-n6575                1/1     Running           0          43s
guaranteed-2-79f59d8b74-7ft4b               0/1     SchedulingGated   0          39s

```

**What you expected to happen**:

Preemption should complete successfully without entering an infinite loop.

**How to reproduce it (as minimally and precisely as possible)**:

1. Apply core configuration (cohorts, queues, and priority classes):
```
---
# Root Cohort
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Cohort
metadata:
  name: root
---
# Guaranteed Cohort
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Cohort
metadata:
  name: guaranteed
spec:
  parent: root
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "300m"
---
# Guaranteed ClusterQueue
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "guaranteed"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: LowerPriority
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 100
    withinClusterQueue: Never
  cohort: guaranteed
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "0m"
---
# Best-effort ClusterQueues
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "best-effort-tenant-a"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Never
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: Never
  cohort: root
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "0m"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "best-effort-tenant-b"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Never
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: Never
  cohort: root
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "0m"
---
# LocalQueues
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: guaranteed
spec:
  clusterQueue: guaranteed
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: best-effort-tenant-a
spec:
  clusterQueue: best-effort-tenant-a
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: best-effort-tenant-b
spec:
  clusterQueue: best-effort-tenant-b
---
# Priority Classes
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low
value: 70
globalDefault: false
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: medium
value: 102
globalDefault: false
---
# Resource Flavor
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
---
```
2. Create best-effort workloads:
```
# Workloads - Best Effort A
apiVersion: apps/v1
kind: Deployment
metadata:
  name: best-effort-tenant-a-1
  labels: {app: best-effort-tenant-a-1, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort-tenant-a}
spec:
  replicas: 1
  selector:
    matchLabels: {app: best-effort-tenant-a-1}
  template:
    metadata:
      labels: {app: best-effort-tenant-a-1, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort-tenant-a}
    spec:
      priorityClassName: low
      terminationGracePeriodSeconds: 1
      containers:
      - name: main
        image: registry.k8s.io/pause:3.9
        resources:
          requests:
            cpu: "100m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: best-effort-tenant-a-2
  labels: {app: best-effort-tenant-a-2, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort-tenant-a}
spec:
  replicas: 1
  selector:
    matchLabels: {app: best-effort-tenant-a-2}
  template:
    metadata:
      labels: {app: best-effort-tenant-a-2, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort-tenant-a}
    spec:
      priorityClassName: low
      terminationGracePeriodSeconds: 1
      containers:
      - name: main
        image: registry.k8s.io/pause:3.9
        resources:
          requests:
            cpu: "100m"
---
# Workloads - Best Effort B
apiVersion: apps/v1
kind: Deployment
metadata:
  name: best-effort-tenant-b-1
  labels: {app: best-effort-tenant-b-1, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort-tenant-b}
spec:
  replicas: 1
  selector:
    matchLabels: {app: best-effort-tenant-b-1}
  template:
    metadata:
      labels: {app: best-effort-tenant-b-1, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort-tenant-b}
    spec:
      priorityClassName: low
      terminationGracePeriodSeconds: 1
      containers:
      - name: main
        image: registry.k8s.io/pause:3.9
        resources:
          requests:
            cpu: "50m"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: best-effort-tenant-b-2
  labels: {app: best-effort-tenant-b-2, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort-tenant-b}
spec:
  replicas: 1
  selector:
    matchLabels: {app: best-effort-tenant-b-2}
  template:
    metadata:
      labels: {app: best-effort-tenant-b-2, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort-tenant-b}
    spec:
      priorityClassName: low
      terminationGracePeriodSeconds: 1
      containers:
      - name: main
        image: registry.k8s.io/pause:3.9
        resources:
          requests:
            cpu: "50m"
 ```
 3. Create first guaranteed workload (triggers normal preemption):
 ```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: guaranteed-1
  labels: {app: guaranteed-1, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed}
spec:
  replicas: 1
  selector:
    matchLabels: {app: guaranteed-1}
  template:
    metadata:
      labels: {app: guaranteed-1, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed}
    spec:
      priorityClassName: medium
      terminationGracePeriodSeconds: 1
      containers:
      - name: main
        image: registry.k8s.io/pause:3.9
        resources:
          requests:
            cpu: "50m"
```
4. Create second guaranteed workload (triggers infinite loop):
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: guaranteed-2
  labels: {app: guaranteed-2, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed}
spec:
  replicas: 1
  selector:
    matchLabels: {app: guaranteed-2}
  template:
    metadata:
      labels: {app: guaranteed-2, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed}
    spec:
      priorityClassName: medium
      terminationGracePeriodSeconds: 1
      containers:
      - name: main
        image: registry.k8s.io/pause:3.9
        resources:
          requests:
            cpu: "100m"
```

**Anything else we need to know?**:

kueue-manager logs
```
{"level":"Level(-2)","ts":"2024-12-09T21:21:39.997044887Z","logger":"workload-reconciler","caller":"queue/manager.go:528","msg":"Attempting to move workloads","workload":{"name":"pod-best-effort-tenant-b-2-69dc4f5797-gbndl-be03a","namespace":"default"},"queue":"best-effort-tenant-b","status":"admitted","cohort":"root","root":"root"}
{"level":"Level(-2)","ts":"2024-12-09T21:21:39.997158095Z","logger":"scheduler","caller":"scheduler/scheduler.go:543","msg":"Workload assumed in the cache","attemptCount":115,"workload":{"name":"pod-best-effort-tenant-b-2-69dc4f5797-2jpd6-289ea","namespace":"default"},"clusterQueue":{"name":"best-effort-tenant-b"}}
{"level":"info","ts":"2024-12-09T21:21:39.997385095Z","logger":"scheduler","caller":"scheduler/scheduler.go:365","msg":"Workload skipped from admission because it's already assumed or admitted","attemptCount":116,"workload":{"name":"pod-best-effort-tenant-b-2-69dc4f5797-2jpd6-289ea","namespace":"default"},"clusterQueue":{"name":"best-effort-tenant-b"},"workload":{"name":"pod-best-effort-tenant-b-2-69dc4f5797-2jpd6-289ea","namespace":"default"}}
{"level":"error","ts":"2024-12-09T21:21:40.00190772Z","logger":"scheduler","caller":"scheduler/scheduler.go:263","msg":"Failed to preempt workloads","attemptCount":116,"workload":{"name":"pod-guranateed-2-788b9dd5bb-zbvmc-667aa","namespace":"default"},"clusterQueue":{"name":"guranateed"},"error":"Operation cannot be fulfilled on workloads.kueue.x-k8s.io \"pod-best-effort-tenant-b-2-69dc4f5797-2jpd6-289ea\": the object has been modified; please apply your changes to the latest version and try again","stacktrace":"sigs.k8s.io/kueue/pkg/scheduler.(*Scheduler).schedule\n\t/workspace/pkg/scheduler/scheduler.go:263\nsigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff.func1\n\t/workspace/pkg/util/wait/backoff.go:43\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil.func1\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:226\nk8s.io/apimachinery/pkg/util/wait.BackoffUntil\n\t/workspace/vendor/k8s.io/apimachinery/pkg/util/wait/backoff.go:227\nsigs.k8s.io/kueue/pkg/util/wait.untilWithBackoff\n\t/workspace/pkg/util/wait/backoff.go:42\nsigs.k8s.io/kueue/pkg/util/wait.UntilWithBackoff\n\t/workspace/pkg/util/wait/backoff.go:34"}
{"level":"Level(-2)","ts":"2024-12-09T21:21:40.002000345Z","logger":"scheduler","caller":"scheduler/scheduler.go:645","msg":"Workload re-queued","attemptCount":116,"workload":{"name":"pod-best-effort-tenant-a-1-5576db6f68-hjsv2-9fc95","namespace":"default"},"clusterQueue":{"name":"best-effort-tenant-a"},"queue":{"name":"best-effort-tenant-a","namespace":"default"},"requeueReason":"","added":true,"status":""}
{"level":"Level(-2)","ts":"2024-12-09T21:21:40.006699845Z","logger":"scheduler","caller":"scheduler/scheduler.go:567","msg":"Workload successfully admitted and assigned flavors","attemptCount":115,"workload":{"name":"pod-best-effort-tenant-b-2-69dc4f5797-2jpd6-289ea","namespace":"default"},"clusterQueue":{"name":"best-effort-tenant-b"},"assignments":[{"name":"main","flavors":{"cpu":"default"},"resourceUsage":{"cpu":"50m"},"count":1}]}
{"level":"debug","ts":"2024-12-09T21:21:40.006734262Z","logger":"events","caller":"recorder/recorder.go:104","msg":"Quota reserved in ClusterQueue best-effort-tenant-b, wait time since queued was 2s","type":"Normal","object":{"kind":"Workload","namespace":"default","name":"pod-best-effort-tenant-b-2-69dc4f5797-2jpd6-289ea","uid":"df8be6f5-0bba-4bd4-9f00-39b3209aa82c","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"556812"},"reason":"QuotaReserved"}
{"level":"debug","ts":"2024-12-09T21:21:40.006753928Z","logger":"events","caller":"recorder/recorder.go:104","msg":"Admitted by ClusterQueue best-effort-tenant-b, wait time since reservation was 0s","type":"Normal","object":{"kind":"Workload","namespace":"default","name":"pod-best-effort-tenant-b-2-69dc4f5797-2jpd6-289ea","uid":"df8be6f5-0bba-4bd4-9f00-39b3209aa82c","apiVersion":"kueue.x-k8s.io/v1beta1","resourceVersion":"556812"},"reason":"Admitted"}
```
**Environment**:
- Kubernetes version: v1.31.0
- Kueue version: v0.10.0-rc.3-20-g6df4a225-dirty
- Cloud provider or hardware configuration: local setup ( minikube ) & gke
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-10T07:37:33Z

@yuvalaz99 thank you for reporting the issue with the detailed scenario. Let me ask some questions to triage it. I could probably look into this closer by EOW, or next week.

There are a couple of features used here: HierarchicalCohorts, Deployments, borrowWithinCohort. Do you have some evidence for which one is the actual culprit? Do you have a temporary workaround for the issue? Would you like to work on the fix?

### Comment by [@yuvalaz99](https://github.com/yuvalaz99) — 2024-12-10T08:04:34Z

> @yuvalaz99 thank you for reporting the issue with the detailed scenario. Let me ask some questions to triage it. I could probably look into this closer by EOW, or next week.
> 
> There are a couple of features used here: HierarchicalCohorts, Deployments, borrowWithinCohort. Do you have some evidence for which one is the actual culprit? Do you have a temporary workaround for the issue? Would you like to work on the fix?

Thank you for the quick response :)
So iv'e verified that with the same setup and without HierarchicalCohorts this issue does not occur.

Cohort Structure
--- Cohort Root (NM: 0m)
-------- Clusterqueue Guaranteed (NM: 300m)
-------- ClusterQueue BestEffortTenantA (NM: 0m)
-------- ClusterQueue BestEffortTenantB (NM: 0m)

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T10:08:51Z

I see, thank you for the update, it feels the next step will be to replicate, preferably in integration tests, and debug where is the culprit.

### Comment by [@mbobrovskyi](https://github.com/mbobrovskyi) — 2024-12-11T10:10:13Z

/assign @vladikkuzn

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-07T14:48:37Z

cc @gabesaba

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-08T14:47:35Z

Hi @yuvalaz99, I was unable to reproduce the issue. Were there any additional options/feature gates you configured when running Kueue? Are you still able to reproduce this issue using Kueue 0.10.0?

**Setup:**
I ran Kueue 0.10.0 on GKE 1.31, enabling the pod and deployment integrations.

**Steps:**

I applied the configurations you provided, in order. I observed different preemptions: best-effort-tenant-b-2 when guaranteed-1 was created, and best-effort-tenant-b-1 when guaranteed-2 was created. guaranteed-1 and guaranteed-2 admitted and scheduled successfully, with best-effort-tenant-b-1 and best-effort-tenant-b-2 remaining gated post preemption.

To match your description more closely, I also created the best effort workloads sequentially (since we [sort preemption candidates based on admission timestamp](https://github.com/kubernetes-sigs/kueue/blob/bf4657adc4e82b1458a8e0f78e0e21af15486d7b/pkg/scheduler/preemption/preemption.go#L587)) [a1, b1, b2, a2], to reproduce the preemptions of a2 and b2 you mentioned. In this case, guaranteed-1 and guaranteed-2 were still able to admit and schedule.

### Comment by [@yuvalaz99](https://github.com/yuvalaz99) — 2025-01-12T12:41:47Z

Hi @gabesaba,
After some further investigation, I believe the issue is broader than just hierarchical cohorts.

The core problem appears to be that when the preempting ClusterQueue has a higher weighted share than the target ClusterQueue. The workload that was preempted gets admitted again to maintain fairness in the system ( which will be again preempted ).

I’ll provide a minimal configuration to reproduce this issue.

Cohort Structure
--- Cohort Root (NM: 0m)
-------- Clusterqueue GuaranteedTenantA (NM: 150m)
-------- Clusterqueue GuaranteedTenantB (NM: 150m)
-------- ClusterQueue BestEffort (NM: 0m)

**Event Sequence Leading to the Issue**

GuaranteedTenantA1 (250m) admitted
BestEffort1 (50m) admitted
GuaranteedTenantA2 (50m) created → triggers infinite loop:
- BestEffort1 preempted
- BestEffort1 recreated by its Deployment
- BestEffort1 & GuaranteedTenantA2 remain in SchedulingGated
- BestEffort1 admitted again **( because ClusterQueue BestEffort has lower Wighted Share value than ClusterQueue GuaranteedTenantA )**

**How to reproduce the issue:**

1. Apply core configuration (cohorts, queues, resourceflavors and priority classes):
```
---
# Root Cohort
apiVersion: kueue.x-k8s.io/v1alpha1
kind: Cohort
metadata:
  name: testing
---
# Guaranteed ClusterQueue
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "guaranteed-tenant-a"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: LowerPriority
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 100
    withinClusterQueue: Never
  cohort: testing
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "150m"
---
# Guaranteed ClusterQueue
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "guaranteed-tenant-b"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: LowerPriority
    borrowWithinCohort:
      policy: LowerPriority
      maxPriorityThreshold: 100
    withinClusterQueue: Never
  cohort: testing
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "150m"        
---
# Best-effort ClusterQueues
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "best-effort"
spec:
  namespaceSelector: {}
  preemption:
    reclaimWithinCohort: Never
    borrowWithinCohort:
      policy: Never
    withinClusterQueue: Never
  cohort: testing
  resourceGroups:
  - coveredResources: ["cpu"]
    flavors:
    - name: "default"
      resources:
      - name: "cpu"
        nominalQuota: "0m"
---
# LocalQueues
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: guaranteed-tenant-a
spec:
  clusterQueue: guaranteed-tenant-a
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: guaranteed-tenant-b
spec:
  clusterQueue: guaranteed-tenant-b
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: best-effort
spec:
  clusterQueue: best-effort
---
# Priority Classes
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: low
value: 70
globalDefault: false
---
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: medium
value: 102
globalDefault: false
---
# Resource Flavor
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: default
```

2. Create workloads that will utilize the available quota
```
---
# Workloads - Guaranteed Tenant A
apiVersion: apps/v1
kind: Deployment
metadata:
 name: guaranteed-tenant-a-1
 labels: {app: guaranteed-tenant-a-1, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed-tenant-a}
spec:
 replicas: 1
 selector:
   matchLabels: {app: guaranteed-tenant-a-1}
 template:
   metadata:
     labels: {app: guaranteed-tenant-a-1, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed-tenant-a}
   spec:
     priorityClassName: medium
     terminationGracePeriodSeconds: 1
     containers:
     - name: main
       image: registry.k8s.io/pause:3.9
       resources:
         requests:
           cpu: "250m"
---
# Workloads - Best Effort 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: best-effort-1
  labels: {app: best-effort-1, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort}
spec:
  replicas: 1
  selector:
    matchLabels: {app: best-effort-1}
  template:
    metadata:
      labels: {app: best-effort-1, kueue-job: "true", kueue.x-k8s.io/queue-name: best-effort}
    spec:
      priorityClassName: low
      terminationGracePeriodSeconds: 1
      containers:
      - name: main
        image: registry.k8s.io/pause:3.9
        resources:
          requests:
            cpu: "50m"
```

3. Create workload that will trigger infinite preemption loop
```
---
# Workloads - Guaranteed Tenant A
apiVersion: apps/v1
kind: Deployment
metadata:
 name: guaranteed-tenant-a-2
 labels: {app: guaranteed-tenant-a-2, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed-tenant-a}
spec:
 replicas: 1
 selector:
   matchLabels: {app: guaranteed-tenant-a-2}
 template:
   metadata:
     labels: {app: guaranteed-tenant-a-2, kueue-job: "true", kueue.x-k8s.io/queue-name: guaranteed-tenant-a}
   spec:
     priorityClassName: medium
     terminationGracePeriodSeconds: 1
     containers:
     - name: main
       image: registry.k8s.io/pause:3.9
       resources:
         requests:
           cpu: "50m"
```

**Expected pods status**
```
> kubectl get pods
NAME                                     READY   STATUS            RESTARTS   AGE
best-effort-1-6467566f99-9mcxj           0/1     Terminating       0          3s
best-effort-1-6467566f99-bglnp           0/1     SchedulingGated   0          0s
guaranteed-tenant-a-1-78bf7b9448-ps98v   1/1     Running           0          76s
guaranteed-tenant-a-2-d9cf8dc5-fxx69     0/1     SchedulingGated   0          65s
```

**Our Kueue configuration:**
```
  managerConfig:
    controllerManagerConfigYaml: |-
      apiVersion: config.kueue.x-k8s.io/v1beta1
      kind: Configuration
      metrics:
        enableClusterQueueResources: true
      waitForPodsReady:
       enable: true
       timeout: 168h
       blockAdmission: false
      integrations:
        frameworks:
        - "pod"
        podOptions:
          namespaceSelector:
            matchExpressions:
            - key: kubernetes.io/metadata.name
              operator: In
              values:
              - default
          podSelector:
            matchExpressions:
            - key: kueue.x-k8s.io/queue-name
              operator: Exists
      fairSharing:
        enable: true
        preemptionStrategies: [LessThanInitialShare]
      resources:
        excludeResourcePrefixes: [
          ephemeral-storage,
          memory,
          networking.gke.io.networks
        ]
```

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-13T10:48:45Z

Thanks for the additional info, @yuvalaz99. I'll take a look this week into this more generalized issue you described.

I want to note: in the current state, Hierarchical Cohorts and Fair Sharing are incompatible - their usage together results in undefined behavior. We are working on making Fair Sharing and Hierarchical Cohorts compatible now. That may be a culprit in the initial issue you described, but not the latest, as the cohort structure in your latest issue description is flat.

### Comment by [@yuvalaz99](https://github.com/yuvalaz99) — 2025-01-13T11:03:27Z

@gabesaba Thank you for your response and for looking into this!

Please note that the new information shows this unexpected behavior also occurs when hierarchical cohorts are not used.

If you need any more information, I’ll be happy to help :)

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-17T15:58:12Z

> [@gabesaba](https://github.com/gabesaba) Thank you for your response and for looking into this!
> 
> Please note that the new information shows this unexpected behavior also occurs when hierarchical cohorts are not used.
> 
> If you need any more information, I’ll be happy to help :)

I was able to reproduce the issue - though it didn't result in an infinite preemption loop, but some unnecessary preemptions (`best-effort-1` workload was preempted a few times, before it was left alone by `guaranteed-tenant-a-2`). I'll provide an estimate next week of by when we can get this fixed.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-29T10:41:27Z

We're reproducing the bug in an integration test (#4030). Afterwords, we'll implement a fix.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-01-29T10:43:44Z

> After some further investigation, I believe the issue is broader than just hierarchical cohorts.

@yuvalaz99, could you update the issue title please, to more accurately reflect this? Something like "Preemption Loop in Fair Sharing"

### Comment by [@yuvalaz99](https://github.com/yuvalaz99) — 2025-01-29T10:56:18Z

> We're reproducing the bug in an integration test ([#4030](https://github.com/kubernetes-sigs/kueue/pull/4030)). Afterwords, we'll implement a fix.

I'm glad you were able to reproduce it. Thanks :)

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-03T16:32:24Z

The root cause is the below-threshold logic:
https://github.com/kubernetes-sigs/kueue/blob/d02a7649e63fba77d546adaa8be11c72624009f5/pkg/scheduler/preemption/preemption.go#L378-L381

When doing fair preemptions, even though best effort queue + workload has a lower DominantResourceShare than guaranteed queue + workload, this logic is short circuited by belowThreshold, and causing Kueue to preempt anyway. Then, when we get to scheduling, best effort Kueue has a lower DominantResourceShare than guaranteed-1, so it is scheduled. Then the loop occurs.

I will think about how to fix this. In the mean time, can you try removing `spec.preemption.borrowWithinCohort` from the guaranteed queues? This should resolve the problem - and hopefully be compatible with your setup otherwise

### Comment by [@yuvalaz99](https://github.com/yuvalaz99) — 2025-02-04T10:46:53Z

> The root cause is the below-threshold logic:
> 
> [kueue/pkg/scheduler/preemption/preemption.go](https://github.com/kubernetes-sigs/kueue/blob/d02a7649e63fba77d546adaa8be11c72624009f5/pkg/scheduler/preemption/preemption.go#L378-L381)
> 
> Lines 378 to 381 in [d02a764](/kubernetes-sigs/kueue/commit/d02a7649e63fba77d546adaa8be11c72624009f5)
> 
>  belowThreshold := allowBorrowingBelowPriority != nil && priority.Priority(candWl.Obj) < *allowBorrowingBelowPriority 
>  newCandShareVal, _ := candCQ.cq.DominantResourceShareWithout(candWl.FlavorResourceUsage()) 
>  strategy := p.fsStrategies[0](newNominatedShareValue, candCQ.share, newCandShareVal) 
>  if belowThreshold || strategy { 
> When doing fair preemptions, even though best effort queue + workload has a lower DominantResourceShare than guaranteed queue + workload, this logic is short circuited by belowThreshold, and causing Kueue to preempt anyway. Then, when we get to scheduling, best effort Kueue has a lower DominantResourceShare than guaranteed-1, so it is scheduled. Then the loop occurs.
> 
> I will think about how to fix this. In the mean time, can you try removing `spec.preemption.borrowWithinCohort` from the guaranteed queues? This should resolve the problem - and hopefully be compatible with your setup otherwise

@gabesaba Thanks for your reply :) 

Currently, we are required to use this parameter to meet our business requirements.
Until Kueue introduces either:
- Fair sharing between LQ’s
- CQ preemption protection

we won’t be able to remove this parameter.

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-06T14:38:21Z

/assign

### Comment by [@gabesaba](https://github.com/gabesaba) — 2025-02-06T16:26:18Z

@yuvalaz99, please take a look at #4165, and see if you think it resolves your issue. Please note that this change will make `spec.preemption.borrowWithinCohort` not have any effect when `FairSharing` is enabled. Furthermore, if this PR merges, we will likely make this parameter combination invalid, if we don't find a compelling and understandable/intuitive way to make these features work together.

Was this preemption below priority, while ignoring fair sharing value, something that you were relying on for your business requirements?
