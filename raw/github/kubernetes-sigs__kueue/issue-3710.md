# Issue #3710: Workload gets in infinite loop with PendingFlavors even when best fit flavor is not last

**Summary**: Workload gets in infinite loop with PendingFlavors even when best fit flavor is not last

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3710

**Last updated**: 2025-05-11T16:26:27Z

---

## Metadata

- **State**: closed (not_planned)
- **Author**: [@CecileRobertMichon](https://github.com/CecileRobertMichon)
- **Created**: 2024-12-02T16:48:34Z
- **Updated**: 2025-05-11T16:26:27Z
- **Closed**: 2025-05-11T16:26:25Z
- **Labels**: `kind/bug`, `lifecycle/rotten`
- **Assignees**: [@PBundyra](https://github.com/PBundyra)
- **Comments**: 14

## Description

<!-- Please use this template while reporting a bug and provide as much info as possible. Not doing so may result in your bug not being addressed in a timely manner. Thanks!

If the matter is security related, please disclose it privately via https://kubernetes.io/security/
-->


**What happened**:

When a workload has two `PodSets`, one which can't get admitted because of quota, and the other which can get admitted, the workload is reconciled in an infinite loop until it can be admitted which causes other smaller workloads in the queue that could be admitted to not get admitted as expected when the `queueingStrategy` is `BestEffortFIFO`.

After adding some debug statements in the code, this seems to happen because `wInfo.LastAssignment.PendingFlavors()` return true [here](https://github.com/kubernetes-sigs/kueue/blob/v0.8.1/pkg/queue/cluster_queue.go#L233) causing the workload to always be re-queued as "immediate".

The issue is specifically that there are two podSets in the workload: one that requires GPUs and doesn't have enough quota to be admitted, and one that only needs CPU and can be admitted based on queue quota usage. For the CPU only podSet that has enough quota, Kueue looks at the CPU flavor first, finds a fit, then keeps going and looks at the GPU node flavor and breaks [here](https://github.com/kubernetes-sigs/kueue/blob/v0.8.1/pkg/scheduler/flavorassigner/flavorassigner.go#L447) because the flavor selector doesn't match. Issue is that we never reach [this line](https://github.com/kubernetes-sigs/kueue/blob/v0.8.1/pkg/scheduler/flavorassigner/flavorassigner.go#L507) because bestAssignment is empty for the GPU flavor, and for CPU flavor it's not the last one in the list so it keeps setting TriedFlavorIdx to 0 instead of -1 [here](https://github.com/kubernetes-sigs/kueue/blob/v0.8.1/pkg/scheduler/flavorassigner/flavorassigner.go#L509), causing `PendingFlavors()` to remain true even though we've gone through all the available flavors and found a match.

Verified that flipping the order of the flavors and putting the `cpu` flavor last in the CQ definition works around the issue. 

**What you expected to happen**: 

I would not expect order of the `flavors` list to matter.

When using `BestEffortFIFO`, workloads that are not first in the queue that can be admitted immediately should get admitted even if the first workload in the queue is too big to get admitted.

**How to reproduce it (as minimally and precisely as possible)**:

Define the following `ResourceFlavors`

```
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: cpu
spec:
  nodeLabels:
    example.com/mode: cpu
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: gpu
spec:
  nodeLabels:
    example.com/gpu: true
```

Define a `ClusterQueue` with two flavors in the following order (CPU first) and `BestEffortFIFO` queuing strategy:

```
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources:
    - memory
    - cpu
    - nvidia.com/gpu
      flavors:
      - name: cpu
        resources:
        - name: memory
          nominalQuota: "<some number>"
        - name: cpu
          nominalQuota: "<some number>"
        - name: nvidia.com/gpu
          nominalQuota: "0"
      - name: gpu
        resources:
        - name: memory
          nominalQuota: "<some number>"
        - name: cpu
          nominalQuota: "<some number>"
        - name: nvidia.com/gpu
          nominalQuota: "<some number>"
```

Submit some JobSets to the queue with 2 `replicatedJobs`, `head` and `worker` where `worker` is requesting GPU resource whereas `head` only requests CPU and memory.

Notice that when the queue is full, only the first pending workload is getting reconciled in a loop and the following event is emitted on repeat: `couldn't assign flavors to pod set head: flavor gpu doesn't match node affinity`.

**Anything else we need to know?**:

**Environment**:
- Kubernetes version (use `kubectl version`):  v1.29.1
- Kueue version (use `git describe --tags --dirty --always`): v0.8.1
- Cloud provider or hardware configuration:
- OS (e.g: `cat /etc/os-release`):
- Kernel (e.g. `uname -a`):
- Install tools:
- Others:

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-03T09:39:35Z

cc @gabesaba PTAL

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-05T13:18:36Z

@CecileRobertMichon can you maybe check if this is a recent regression, or the same behavior is present on 0.7, 0.8 or 0.9? I'm curious also about 0.7 because 0.8 and 0.9 contain some significant changes to the Kueue scheduler logic. 

EDIT: Ah I see you test it on 0.8.1, in that case you may still check one before and also check the issue still exists in 0.9.

### Comment by [@CecileRobertMichon](https://github.com/CecileRobertMichon) — 2024-12-06T16:23:31Z

@mimowo the issue still exists in main branch. The problem code is here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L516

The issue is that we don't update `assignment.TriedFlavorIdx` when `bestAssignment` is empty, which is the case when the best assignment was already found and [returned](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L510) on an earlier attempt, and then we look again because there are flavors remaining (because `TriedFlavorIdx` was not `-1` if the best fit wasn't the last Flavor and there's another podSet that doesn't fit), and we are looking at a flavor where there's no fit possible with the last flavor (because of a taint or label mismatch).

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-10T07:21:16Z

Thank you for the detailed summary, this is very useful. Do you have some idea(s) / proposals how this could be fixed? Also, would you like to send a PR for that? I will try to get deeper into this problem in the coming days.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-11T13:59:05Z

Hi @CecileRobertMichon, thanks for bringing this problem up, and for the detailed explanation!

> @mimowo the issue still exists in main branch. The problem code is here: https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L516
> 
> The issue is that we don't update `assignment.TriedFlavorIdx` when `bestAssignment` is empty, which is the case when the best assignment was already found and [returned](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L510) on an earlier attempt, and then we look again because there are flavors remaining (because `TriedFlavorIdx` was not `-1` if the best fit wasn't the last Flavor and there's another podSet that doesn't fit), and we are looking at a flavor where there's no fit possible with the last flavor (because of a taint or label mismatch).

Have you disabled the FlavorFungibility feature gate? [The first line you linked](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L516) can only happen if the feature is enabled, however [the second line you linked](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L510) can only happen if the opposite is true

### Comment by [@CecileRobertMichon](https://github.com/CecileRobertMichon) — 2024-12-11T14:28:43Z

@PBundyra I did not disable `FlavorFungibility`, I linked the wrong return line, it should be [this one](https://github.com/kubernetes-sigs/kueue/blob/main/pkg/scheduler/flavorassigner/flavorassigner.go#L525) instead 

@mimowo I would love to open a PR if there is agreement that this is indeed a bug and not just me doing something wrong

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-11T14:41:39Z

The described behaviour certainly is a bug as it violates the BestEffortFIFO semantics. However, I'm not yet understanding the problem deeply enough to know what is the best approach for fixing it. We need to be careful about some scenarios which can be affected as a side effect by the fix. Feel free to propose something.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-12-12T09:04:42Z

I think it would be great if the next step is an integration test which reproduces the issue. I believe your description is detailed enough to reproduce it at that level. I synced with @PBundyra who will start with writing the test. 
/assign @PBundyra 

> @mimowo I would love to open a PR if there is agreement that this is indeed a bug and not just me doing something wrong

sure, your PR would be welcome, or review of Patryk's PR if this turns out a simple addition to the test.

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-12T14:18:32Z

Hi @CecileRobertMichon 

I'm working on reproducing the issue but seems like there are some gaps in my configuration. Could you provide specific yamls you used when facing this?

### Comment by [@PBundyra](https://github.com/PBundyra) — 2024-12-12T14:22:39Z

Those are my yamls, can you spot any differences from yours?

```
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  queueingStrategy: BestEffortFIFO
  resourceGroups:
  - coveredResources:
    - memory
    - cpu
    - nvidia.com/gpu
    flavors:
    - name: cpu
      resources:
      - name: memory
        nominalQuota: 10000Gi
      - name: cpu
        nominalQuota: 10000
      - name: nvidia.com/gpu
        nominalQuota: 0
    - name: gpu
      resources:
      - name: memory
        nominalQuota: 10000Gi
      - name: cpu
        nominalQuota: 100000
      - name: nvidia.com/gpu
        nominalQuota: 4
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: cpu
spec:
  nodeLabels:
    example.com/mode: cpu
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: gpu
spec:
  nodeLabels:
    example.com/gpu: "true"
```

Jobset requesting 3 gpus
```
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  generateName: jobset-big-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  # label and annotate jobs and pods with stable network endpoint of the designated
  # coordinator pod:
  # jobset.sigs.k8s.io/coordinator=coordinator-example-driver-0-0.coordinator-example
  coordinator:
    replicatedJob: head
    jobIndex: 0
    podIndex: 0
  replicatedJobs:
  - name: head
    template:
      spec:
        parallelism: 3
        completions: 3
        suspend: true
        template:
          spec:
            nodeSelector:
              example.com/cpu: "true"
            containers:
            - name: dummy-job
              image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
              args: ["30000s"]
              resources:
                requests:
                  cpu: 1
                  memory: "200Mi"
            restartPolicy: Never
  - name: workers
    template:
      spec:
        parallelism: 1
        completions: 1
        suspend: true
        template:
          spec:
            nodeSelector:
              example.com/gpu: "true"
            containers:
            - name: dummy-job
              image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
              args: ["30000s"]
              resources:
                requests:
                  cpu: 1
                  memory: "200Mi"
                  nvidia.com/gpu: 3
                limits:
                  nvidia.com/gpu: 3
            restartPolicy: Never
```

Jobset requesting 1 gpu

```
apiVersion: jobset.x-k8s.io/v1alpha2
kind: JobSet
metadata:
  generateName: jobset-small-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  # label and annotate jobs and pods with stable network endpoint of the designated
  # coordinator pod:
  # jobset.sigs.k8s.io/coordinator=coordinator-example-driver-0-0.coordinator-example
  coordinator:
    replicatedJob: head
    jobIndex: 0
    podIndex: 0
  replicatedJobs:
  - name: head
    template:
      spec:
        parallelism: 3
        completions: 3
        suspend: true
        template:
          spec:
            nodeSelector:
              example.com/cpu: "true"
            containers:
            - name: dummy-job
              image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
              args: ["30000s"]
              resources:
                requests:
                  cpu: 1
                  memory: "200Mi"
            restartPolicy: Never
  - name: workers
    template:
      spec:
        parallelism: 1
        completions: 1
        suspend: true
        template:
          spec:
            nodeSelector:
              example.com/gpu: "true"
            containers:
            - name: dummy-job
              image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
              args: ["30000s"]
              resources:
                requests:
                  cpu: 1
                  memory: "200Mi"
                  nvidia.com/gpu: 1
                limits:
                  nvidia.com/gpu: 1
            restartPolicy: Never
```

When creating 2 big jobsets, one gets admitted and the other one waits in the queue. After that I've created a small jobset and it was successfully admitted:

```
NAME                              QUEUE        RESERVED IN     ADMITTED   FINISHED   AGE
jobset-jobset-big-4k4m4-eb4a3     user-queue   cluster-queue   True                  26s
jobset-jobset-big-jzm79-db47b     user-queue                                         21s
jobset-jobset-small-nvzpw-a6ee0   user-queue   cluster-queue   True                  10s
```

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-03-12T14:50:02Z

The Kubernetes project currently lacks enough contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle stale`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle stale

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-04-11T15:42:33Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues.

This bot triages un-triaged issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Close this issue with `/close`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/lifecycle rotten

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-05-11T16:26:21Z

The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.

This bot triages issues according to the following rules:
- After 90d of inactivity, `lifecycle/stale` is applied
- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed

You can:
- Reopen this issue with `/reopen`
- Mark this issue as fresh with `/remove-lifecycle rotten`
- Offer to help out with [Issue Triage][1]

Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).

/close not-planned

[1]: https://www.kubernetes.dev/docs/guide/issue-triage/

### Comment by [@k8s-ci-robot](https://github.com/k8s-ci-robot) — 2025-05-11T16:26:26Z

@k8s-triage-robot: Closing this issue, marking it as "Not Planned".

<details>

In response to [this](https://github.com/kubernetes-sigs/kueue/issues/3710#issuecomment-2869967037):

>The Kubernetes project currently lacks enough active contributors to adequately respond to all issues and PRs.
>
>This bot triages issues according to the following rules:
>- After 90d of inactivity, `lifecycle/stale` is applied
>- After 30d of inactivity since `lifecycle/stale` was applied, `lifecycle/rotten` is applied
>- After 30d of inactivity since `lifecycle/rotten` was applied, the issue is closed
>
>You can:
>- Reopen this issue with `/reopen`
>- Mark this issue as fresh with `/remove-lifecycle rotten`
>- Offer to help out with [Issue Triage][1]
>
>Please send feedback to sig-contributor-experience at [kubernetes/community](https://github.com/kubernetes/community).
>
>/close not-planned
>
>[1]: https://www.kubernetes.dev/docs/guide/issue-triage/


Instructions for interacting with me using PR comments are available [here](https://git.k8s.io/community/contributors/guide/pull-requests.md).  If you have questions or suggestions related to my behavior, please file an issue against the [kubernetes-sigs/prow](https://github.com/kubernetes-sigs/prow/issues/new?title=Prow%20issue:) repository.
</details>
