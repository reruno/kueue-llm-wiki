# Issue #3141: [PartialAdmission] Job does not reclaim free resources properly if partially admitted

**Summary**: [PartialAdmission] Job does not reclaim free resources properly if partially admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/3141

**Last updated**: 2026-01-30T07:26:22Z

---

## Metadata

- **State**: open
- **Author**: [@mimowo](https://github.com/mimowo)
- **Created**: 2024-09-26T09:13:11Z
- **Updated**: 2026-01-30T07:26:22Z
- **Closed**: —
- **Labels**: `kind/bug`
- **Assignees**: [@mszadkow](https://github.com/mszadkow), [@mimowo](https://github.com/mimowo)
- **Comments**: 16

## Description

**What happened**:

Free resources are reclaimed with unnecessary delay when using partial admission.

**What you expected to happen**:

Allow to use free resources as soon as available.

**How to reproduce it (as minimally and precisely as possible)**:

1. Create the following config:

```yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 9
      - name: "memory"
        nominalQuota: 36Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "user-queue"
spec:
  clusterQueue: "cluster-queue"
```
2. Submit the small.yaml Job:
```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
spec:
  parallelism: 3
  completions: 3
  suspend: true
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:v0.1.0
        args: ["1800s"]
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
3. create the `big.yaml`:

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-big-
  labels:
    kueue.x-k8s.io/queue-name: user-queue
  annotations:
    kueue.x-k8s.io/job-min-parallelism: "3"
spec:
  parallelism: 9
  completions: 9
  completionMode: Indexed
  suspend: true
  template:
    spec:
      containers:
      - name: job-longrun
        image: python
        command:
        - python3
        - -c
        - |
          import os
          import time
          import sys
          id = int(os.environ.get("JOB_COMPLETION_INDEX"))
          time.sleep(5 + id*5)
        imagePullPolicy: IfNotPresent
        resources:
          requests:
            cpu: "1"
            memory: "200Mi"
      restartPolicy: Never
```
Then, monitoring the usage of the CQ:
```
> k get cq -w --output-watch-events -ocustom-columns="TYPE:.type,NAME:.object.metadata.name,USAGE:.object.status.flavorsUsage[0].resources[0].total" | ts "%H:%M:%.S"
11:30:02.801519 TYPE    NAME            USAGE
11:30:02.801689 ADDED   cluster-queue   0
11:30:28.388297 MODIFIED   cluster-queue   3
11:30:42.878975 MODIFIED   cluster-queue   9
11:31:29.980804 MODIFIED   cluster-queue   8
11:31:40.010289 MODIFIED   cluster-queue   7
11:31:50.030854 MODIFIED   cluster-queue   3
```

Notably, the drop of usage (7->3) in the last two lines corresponds to just one pod completing. In other words when the declared usage is 7, there are only 4 pods running (1 from big, and 3 from small workload).

**Anything else we need to know?**:

I tested a fix for the scenario locally by changing this line: https://github.com/kubernetes-sigs/kueue/blob/23dec6d1d1f1a0e8fa51bb63349af84f6f52d9dd/pkg/controller/jobs/job/job_controller.go#L229 to 
`Count: j.Status.Succeeded`. I believe this makes sense as a fix. It would also be consistent with formulas for other job CRDs, like JobSet.

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2024-09-26T10:29:55Z

/assign
Assigning initially to myself, feel free to ping me on slack if you are interested to take it

### Comment by [@trasc](https://github.com/trasc) — 2024-10-01T13:37:38Z

> tested a fix for the scenario locally by changing this line:
>  Count: parallelism - remaining, 
> to
> Count: j.Status.Succeeded. I believe this makes sense as a fix. It would also be consistent with formulas for other job CRDs, like JobSet.

I don't think this works if the completions ( and eventually j.Status.Succeeded)  > parallelism.

What might work (without involving any API change) is to reset the reclaimable pods count of the workload after it gets readmitted.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-17T18:33:06Z

@mimowo What is the status of this? I believe that this should be fixed before the next release.

### Comment by [@mimowo](https://github.com/mimowo) — 2024-10-24T05:37:01Z

I can see why my initially approach does not work as in the @trasc comment, when completions >parallelism, and I can think the idea to clear the reclaimable pods will probably work, but it will probably require a KEP update.

In any case the issue does not seem high priority because the only known impact is the reclaimablePods lagging behind the actual amount of free resources when partial admission is used. Also, I don't know about any user raising this so I assume it is safe to fix it in 0.10.

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2024-10-28T17:32:12Z

> In any case the issue does not seem high priority because the only known impact is the reclaimablePods lagging behind the actual amount of free resources when partial admission is used.

I guess that the situation could easily happen in the fixed cluster when they overcommit the resources between ClusterQueue and actual Cluster Capacity.
So, this should be fixed.

But, we do not have enough bandwidth for this now.
Hence, I agree with updating the KEP and fixing this issue in the 0.10. We might want to cherry-pick the change to release-0.9 branch, though.

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-01-26T17:56:47Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-01-27T06:25:44Z

/remove-lifecycle stale

### Comment by [@mszadkow](https://github.com/mszadkow) — 2025-02-27T12:19:00Z

/assign

### Comment by [@cheng-ml](https://github.com/cheng-ml) — 2025-04-01T00:32:40Z

Hi I have workloads (Job) admitted with partial admission,  even the reclaimable  pods are non zero, but newly submitted job won't get admitted and it doesn't decrease the counts, any suggestions? Thank you!

Status:
  Admission:
    Cluster Queue:  cluster-queue
    Pod Set Assignments:
      Count:  456
      Flavors:
        Ephemeral - Storage:  pool1
        nvidia.com/gpu:      pool1
      Name:                   main
      Resource Usage:
        Ephemeral - Storage:  171000Gi
        nvidia.com/gpu:       456
  Conditions:
    Last Transition Time:  2025-03-31T22:51:10Z
    Message:               Quota reserved in ClusterQueue cluster-queue
    Observed Generation:   1
    Reason:                QuotaReserved
    Status:                True
    Type:                  QuotaReserved
    Last Transition Time:  2025-03-31T22:51:10Z
    Message:               The workload is admitted
    Observed Generation:   1
    Reason:                Admitted
    Status:                True
    Type:                  Admitted
  Reclaimable Pods:
    Count:  454
    Name:   main

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-06-30T00:57:52Z

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

### Comment by [@tenzen-y](https://github.com/tenzen-y) — 2025-06-30T12:08:19Z

/remove-lifecycle stale

@mszadkow What about progressing?

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-09-28T12:34:56Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2025-10-02T06:47:24Z

/remove-lifecycle stale

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2025-12-31T07:23:08Z

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

### Comment by [@k8s-triage-robot](https://github.com/k8s-triage-robot) — 2026-01-30T07:24:35Z

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

### Comment by [@mimowo](https://github.com/mimowo) — 2026-01-30T07:26:19Z

/remove-lifecycle rotten
