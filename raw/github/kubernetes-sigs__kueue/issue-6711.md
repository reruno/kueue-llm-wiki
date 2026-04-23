# Issue #6711: Inactive workloads are occasionally admitted

**Summary**: Inactive workloads are occasionally admitted

**Sources**: https://github.com/kubernetes-sigs/kueue/issues/6711

**Last updated**: 2025-11-26T17:02:45Z

---

## Metadata

- **State**: closed (completed)
- **Author**: [@dhenkel92](https://github.com/dhenkel92)
- **Created**: 2025-09-03T08:51:03Z
- **Updated**: 2025-11-26T17:02:45Z
- **Closed**: 2025-11-26T17:02:45Z
- **Labels**: `kind/bug`
- **Assignees**: [@olekzabl](https://github.com/olekzabl)
- **Comments**: 7

## Description

**What happened**:

We've observed that inactive workloads (`.spec.active=false`) occasionally get admitted and are then immediately evicted.

After investigation, we found this is triggered by runtime class reconciliation, which pushes all pending workloads back onto the internal heap, regardless of their active status. This causes the scheduler to consider them, even though they're inactive.

The main [workload controller correctly checks](https://github.com/kubernetes-sigs/kueue/blob/v0.13.3/pkg/controller/core/workload_controller.go#L633-L634) .spec.active before adding workloads to the heap. However, this check is missing in [other situations](https://github.com/kubernetes-sigs/kueue/blob/v0.13.3/pkg/controller/core/workload_controller.go#L928).

**What you expected to happen**:

We’d expect Kueue to consistently avoid scheduling inactive workloads, regardless of the trigger.

**How to reproduce it (as minimally and precisely as possible)**:

1. Apply the test setup below.
2. Annotate the RuntimeClass:
   ```
   kubectl annotate runtimeclass test-kueue-class foo=bar
   ```

This will trigger the code mentioned above, and you’ll see the following events in the workload:

```
  Type    Reason                   Age   From                       Message
  ----    ------                   ----  ----                       -------
  Normal  QuotaReserved            2s    kueue-admission            Quota reserved in ClusterQueue test-cluster-queue, wait time since queued was 14s
  Normal  Admitted                 2s    kueue-admission            Admitted by ClusterQueue test-cluster-queue, wait time since reservation was 0s
  Normal  EvictedDueToDeactivated  2s    kueue-workload-controller  The workload is deactivated
```

Example spec:

```
---
apiVersion: node.k8s.io/v1
kind: RuntimeClass
metadata:
  name: test-kueue-class
handler: myconfiguration
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: test-rf
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: test-cluster-queue
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
    - coveredResources: ["cpu", "memory"]
      flavors:
        - name: "test-rf"
          resources:
            - name: "cpu"
              nominalQuota: 10
            - name: "memory"
              nominalQuota: 2Gi
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  name: test-local-queue
spec:
  clusterQueue: test-cluster-queue
---
apiVersion: kueue.x-k8s.io/v1beta1
kind: Workload
metadata:
  name: test-wl-1
spec:
  active: false
  podSets:
    - count: 1
      name: main
      template:
        spec:
          runtimeClassName: test-kueue-class
          containers:
            - name: demo
              resources:
                limits:
                  cpu: "1"
                  memory: 128Mi
                requests:
                  cpu: "1"
                  memory: 128Mi
  queueName: test-local-queue
```

**Environment**:

- Kubernetes version (use `kubectl version`): v1.31.6
- Kueue version (use `git describe --tags --dirty --always`): 0.13.0

## Discussion

### Comment by [@mimowo](https://github.com/mimowo) — 2025-09-03T10:06:26Z

Thank you for reporting!

### Comment by [@jyotilakra92](https://github.com/jyotilakra92) — 2025-09-06T23:50:22Z

Hey, I am new to this open source community and would love to pick this up as my first task.

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-24T23:32:42Z

/assign

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-25T15:13:32Z

Hello. I've looked at #6737, in particular at [this review comment](https://github.com/kubernetes-sigs/kueue/pull/6737#issuecomment-3270625707) and I'm thinking how to address that generally.
Let me share my findings & thoughts.

1. Looking through all calls to `AddOrUpdateWorkloadWithoutLock`, I see:

   * 3 places which **do pre-check** `IsActive`
      (as well as "has no quota reservation", or alternatively "has status pending", which implies the former):
      
     https://github.com/kubernetes-sigs/kueue/blob/c4143a4946758c5888005a6b364e3970b7d4553f/pkg/controller/core/workload_controller.go#L259-L264

     https://github.com/kubernetes-sigs/kueue/blob/c4143a4946758c5888005a6b364e3970b7d4553f/pkg/controller/core/workload_controller.go#L300

     https://github.com/kubernetes-sigs/kueue/blob/c4143a4946758c5888005a6b364e3970b7d4553f/pkg/controller/core/workload_controller.go#L795-L800

     Note that, in snippets # 1 and 3, `IsActive` influences not only whether we'll call `AddOrUpdateWorkload()`, but also the subsequent flow of the code.
     Which means that we _can't just move_ the check deeper down the call stack.

   * 3 places which **don't pre-check** `IsActive`
      (still, they all do pre-check "having no quota reservation" in some way):

     * In `WorkloadReconciler.Update()`:

       https://github.com/kubernetes-sigs/kueue/blob/c4143a4946758c5888005a6b364e3970b7d4553f/pkg/controller/core/workload_controller.go#L893

       https://github.com/kubernetes-sigs/kueue/blob/c4143a4946758c5888005a6b364e3970b7d4553f/pkg/controller/core/workload_controller.go#L928

     * In `queueReconcileForPending()` (the one originally discussed in this issue)
   
       https://github.com/kubernetes-sigs/kueue/blob/c4143a4946758c5888005a6b364e3970b7d4553f/pkg/controller/core/workload_controller.go#L1111

2. For the latter 3 cases, we have a choice between:

   - **A**: adding a pre-check check for `IsActive`, like for the former 3 cases, and like it's coded in #6737;
   - **B**: putting a pre-check for `IsActive` (and no quota reserved as well?) down the stack, as proposed in [the comment](https://github.com/kubernetes-sigs/kueue/pull/6737#issuecomment-3270625707).

   At first, I was stylistically tempted to propose **A** - so that the code is more self-consistent overall.

   However, now I'm thinking **B** may be *more correct* - in that, if a Workload just got updated by switching its `Spec.Active` from `true` (or empty) to `false`, and if it was present in `r.queues` so far, **B** will result in removing it from there, while **A** would just make no action.

3. Then, the question of "nice code" strikes back - if we just do **B**, then - on some code paths - we'll be checking `IsActive` twice. The performance cost is (I think) negligible; still, this could be considered not very nice.
   However, I don't see a nicer (and simple) way.

Summing up, I'd do just **B**.
Plus returning an _error_ if "no quota reserved" is not met. (IIUC this will never happen for current code - so this is to warn against potential future regressions).
Plus an integration test as requested. 
Plus maybe another integration test to make sure that workload deactivation removes it from the queue heap. (Unless I find out that it's hard to test, or already tested).

Does it make sense?

@mimowo @dhenkel92

### Comment by [@mimowo](https://github.com/mimowo) — 2025-11-25T15:23:52Z

> Summing up, I'd do just B. 

Ideally, yes, but if you encounter issues then the benefit of A is the minimal impact, which might be in plus just before release

> Plus an integration test as requested.

Yes, I would even start here with the TDD approach, even if the test is flaky (say 1/20 repeats) it will already give us signal that we fixed the issue - once fixed.

> Does it make sense?

yes

### Comment by [@olekzabl](https://github.com/olekzabl) — 2025-11-26T10:17:26Z

Update: my speculation about **A** being incorrect turned out _false_.

Both problematic cases (inside `WorkloadReconciler.Update()`) are in fact also guarded by a check of `IsActive`, which happens much higher up:

https://github.com/kubernetes-sigs/kueue/blob/b47e06e493eb0325434150f159234dcac6ec4d06/pkg/controller/core/workload_controller.go#L870-L871

If a workload is not active, we'll enter the `switch` branch above, and hence not enter the other branches containing the calls to `[AddOr]UpdateWorkload()`.

This is also confirmed by an already existing integration test:

https://github.com/kubernetes-sigs/kueue/blob/b47e06e493eb0325434150f159234dcac6ec4d06/test/integration/singlecluster/controller/core/workload_controller_test.go#L167

So, at this point, my preference goes back to solution **A**.

### Comment by [@Singularity23x0](https://github.com/Singularity23x0) — 2025-11-26T11:43:34Z

> However, now I'm thinking B may be more correct - in that, if a Workload just got updated by switching its Spec.Active from true (or empty) to false, and if it was present in r.queues so far, B will result in removing it from there, while A would just make no action.

From the perspective of #5310 this would complicate moving the logic to the Reconciler due to increasing the amount of places which rely on the past state of the workload.

Based on that I recommend going with option A.
